#!/usr/bin/env python3
"""
Stage 4 Edge Formalizer — Weirwood Network

Merges, deduplicates, and endpoint-gates all already-computed Stage 4 edges
from three sources into a single clean edge set, written to a STAGING directory
for human review before promotion to graph/edges/.

Sources:
  1. SPINE       — working/wiki/pass2-buckets/pass1-derived/{book}/*.edges.jsonl
  2. S67 TAIL    — working/wiki/pass2-buckets/pass1-derived/_tail-typed/{book}/*.jsonl
  3. HOSPITALITY — working/wiki/pass2-buckets/pass1-derived/_extra-tables/{book}/*.extra-tables.jsonl
                   (only rows with candidate_kind in pass1_hospitality / pass1_hospitality_violation)

Selection rule: include a row only if decision == "emit_edge" (or no decision field, for
hospitality rows which are deterministically typed) AND edge_type is non-null/non-empty.

Output — all written to STAGING dir (never graph/edges/):
  _formalized/edges.jsonl             — consolidated surviving edges
  _formalized/dropped-endpoints.jsonl — rows dropped by endpoint gate
  _formalized/tail-violations.jsonl   — tail rows quarantined by violation detectors
  _formalized/formalize-report.md     — aggregate stats report
  _formalized/audit-sample-30.jsonl   — deterministic random sample of 30 surviving edges

Precision filter mode (--precision-filter):
  Reads _formalized/edges.jsonl and splits into three files:
  _formalized/edges-v1.jsonl          — surviving v1 edges (the deliverable candidate)
  _formalized/quarantine-gated.jsonl  — gated-type edges (pre-lockdown types, queued for re-typing)
  _formalized/quarantine-lowvalue.jsonl — CONTEMPORARY_WITH person→person edges
  _formalized/precision-filter-report.md — stats report
  _formalized/audit-sample-v1-30.jsonl   — deterministic random sample (seed=43) of 30 v1 edges

Usage:
    python3 scripts/stage4-formalize-edges.py [--dry-run]
    python3 scripts/stage4-formalize-edges.py --precision-filter [--dry-run]

Options:
    --dry-run          Print stats but do not write output files.
    --precision-filter Run the precision filter pass (reads _formalized/edges.jsonl).
    --graph-nodes PATH Path to graph/nodes dir (for HOLDS_TITLE place detection and
                       CONTEMPORARY_WITH person detection).
                       Defaults to graph/nodes relative to repo root.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Repo root and paths
# ---------------------------------------------------------------------------

_REPO = Path(__file__).resolve().parent.parent
_PASS1_DERIVED = _REPO / "working" / "wiki" / "pass2-buckets" / "pass1-derived"
_STAGING = _PASS1_DERIVED / "_formalized"
_BOOKS = ("agot", "acok", "asos", "affc", "adwd")

# ---------------------------------------------------------------------------
# Import is_low_quality_endpoint from stage4-pass1-extra-tables.py
# (importlib required because the filename contains hyphens)
# ---------------------------------------------------------------------------

def _load_extra_tables_module():
    """Load stage4-pass1-extra-tables.py via importlib."""
    mod_path = _REPO / "scripts" / "stage4-pass1-extra-tables.py"
    spec = importlib.util.spec_from_file_location(
        "stage4_pass1_extra_tables", mod_path
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_extra_tables_mod = _load_extra_tables_module()
is_low_quality_endpoint = _extra_tables_mod.is_low_quality_endpoint


# ---------------------------------------------------------------------------
# Verb gate for ENCOUNTERS (mirrors wiki-pass2-validate-edge-jsonl.py)
# ---------------------------------------------------------------------------

_ENCOUNTERS_VERBS: tuple[str, ...] = (
    "met ",
    "meets ",
    "meeting ",
    "came face to face",
    "face-to-face",
    "face to face",
    "confronted",
    "found himself before",
    "found herself before",
    "stood before",
    "appeared before",
    "encountered",
    "encounter ",
)


def _encounters_verb_present(row: dict) -> bool:
    """Return True if any ENCOUNTERS staging verb appears in the evidence text."""
    text = (row.get("evidence_quote") or row.get("evidence_snippet") or "").lower()
    return any(v in text for v in _ENCOUNTERS_VERBS)


# ---------------------------------------------------------------------------
# Node type index — for HOLDS_TITLE place-target detection
# ---------------------------------------------------------------------------

def build_node_type_index(nodes_dir: Path) -> dict[str, str]:
    """Walk graph/nodes/ and return slug -> type from YAML frontmatter."""
    index: dict[str, str] = {}
    slug_re = re.compile(r"^slug:\s*(.+)$", re.MULTILINE)
    type_re = re.compile(r"^type:\s*(.+)$", re.MULTILINE)
    for p in nodes_dir.rglob("*.node.md"):
        try:
            text = p.read_text(errors="replace")
            parts = text.split("---", 2)
            if len(parts) < 3:
                continue
            fm = parts[1]
            sm = slug_re.search(fm)
            tm = type_re.search(fm)
            if sm and tm:
                index[sm.group(1).strip()] = tm.group(1).strip()
        except Exception:
            pass
    return index


# ---------------------------------------------------------------------------
# Source loaders
# ---------------------------------------------------------------------------

def load_spine() -> list[dict]:
    """Load all spine edges — {book}/*.edges.jsonl, decision == emit_edge."""
    rows: list[dict] = []
    for book in _BOOKS:
        book_dir = _PASS1_DERIVED / book
        if not book_dir.is_dir():
            print(f"  [warn] spine dir missing: {book_dir}", file=sys.stderr)
            continue
        for f in sorted(book_dir.glob("*.edges.jsonl")):
            with open(f) as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    row = json.loads(line)
                    if row.get("decision") == "emit_edge":
                        row["source_set"] = "spine"
                        rows.append(row)
    return rows


def load_tail() -> list[dict]:
    """Load all S67 tail edges — _tail-typed/{book}/*.jsonl, decision == emit_edge."""
    rows: list[dict] = []
    tail_dir = _PASS1_DERIVED / "_tail-typed"
    if not tail_dir.is_dir():
        print(f"  [warn] tail dir missing: {tail_dir}", file=sys.stderr)
        return rows
    for book in _BOOKS:
        book_dir = tail_dir / book
        if not book_dir.is_dir():
            continue
        for f in sorted(book_dir.glob("*.jsonl")):
            with open(f) as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    row = json.loads(line)
                    if row.get("decision") == "emit_edge":
                        row["source_set"] = "tail"
                        rows.append(row)
    return rows


def load_hospitality() -> list[dict]:
    """Load hospitality rows from _extra-tables/{book}/*.extra-tables.jsonl.

    Only rows with candidate_kind in (pass1_hospitality, pass1_hospitality_violation).
    These rows are deterministically typed — no 'decision' field present.
    """
    rows: list[dict] = []
    extra_dir = _PASS1_DERIVED / "_extra-tables"
    if not extra_dir.is_dir():
        print(f"  [warn] extra-tables dir missing: {extra_dir}", file=sys.stderr)
        return rows
    hospitality_kinds = {"pass1_hospitality", "pass1_hospitality_violation"}
    for book in _BOOKS:
        book_dir = extra_dir / book
        if not book_dir.is_dir():
            continue
        for f in sorted(book_dir.glob("*.extra-tables.jsonl")):
            with open(f) as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    row = json.loads(line)
                    if row.get("candidate_kind") in hospitality_kinds:
                        row["source_set"] = "hospitality"
                        # Normalize missing fields so pipeline code can treat all rows uniformly
                        row.setdefault("decision", "emit_edge")
                        row.setdefault("evidence_kind", "book-pass1")
                        row.setdefault("evidence_section", "Hospitality & Guest Right")
                        row.setdefault("confidence_tier", 1)
                        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Selection rule: emit_edge + non-null/non-empty edge_type
# ---------------------------------------------------------------------------

def passes_selection(row: dict) -> bool:
    """Return True if the row should enter the pipeline."""
    if row.get("decision") != "emit_edge":
        return False
    et = row.get("edge_type")
    if not et or not et.strip():
        return False
    return True


# ---------------------------------------------------------------------------
# Step 2 — Endpoint gate
# ---------------------------------------------------------------------------

def apply_endpoint_gate(
    rows: list[dict],
) -> tuple[list[dict], list[dict]]:
    """Apply is_low_quality_endpoint to both endpoints.

    Returns (surviving_rows, dropped_rows).
    Dropped rows have 'drop_reason' added.
    """
    surviving: list[dict] = []
    dropped: list[dict] = []

    for row in rows:
        src = row.get("source_slug") or ""
        tgt = row.get("target_slug") or ""
        src_bad = is_low_quality_endpoint(src)
        tgt_bad = is_low_quality_endpoint(tgt)

        if src_bad or tgt_bad:
            reasons = []
            if src_bad:
                reasons.append(f"low_quality_source:{src}")
            if tgt_bad:
                reasons.append(f"low_quality_target:{tgt}")
            row = dict(row)
            row["drop_reason"] = "; ".join(reasons)
            dropped.append(row)
        else:
            surviving.append(row)

    return surviving, dropped


# ---------------------------------------------------------------------------
# Step 3 — S67 tail-violation cleanup
# ---------------------------------------------------------------------------

def apply_tail_violation_cleanup(
    rows: list[dict],
    node_type_index: dict[str, str],
) -> tuple[list[dict], list[dict]]:
    """Quarantine known tail violation patterns.

    (a) HOLDS_TITLE edges whose target resolves to a place (not a title).
    (b) ENCOUNTERS edges that fail the verb gate.
    (c) SPOUSE_OF edges missing a required qualifier field.

    Only applied to source_set == 'tail'. Spine and hospitality are not checked here.

    Returns (surviving_rows, violation_rows).
    Violation rows have 'violation_kind' added.
    """
    surviving: list[dict] = []
    violations: list[dict] = []

    for row in rows:
        if row.get("source_set") != "tail":
            surviving.append(row)
            continue

        et = row.get("edge_type", "")
        row_copy = None

        if et == "HOLDS_TITLE":
            tgt = row.get("target_slug", "")
            tgt_type = node_type_index.get(tgt, "")
            if tgt_type.startswith("place."):
                row_copy = dict(row)
                row_copy["violation_kind"] = (
                    f"holds_title_place_target: target_slug={tgt!r} resolves to type={tgt_type!r}"
                )
        elif et == "ENCOUNTERS":
            if not _encounters_verb_present(row):
                row_copy = dict(row)
                row_copy["violation_kind"] = "encounters_no_verb: no staging verb found in evidence"
        elif et == "SPOUSE_OF":
            qualifier = row.get("qualifier")
            if not qualifier or not str(qualifier).strip():
                row_copy = dict(row)
                row_copy["violation_kind"] = "spouse_of_missing_qualifier: SPOUSE_OF requires qualifier"

        if row_copy is not None:
            violations.append(row_copy)
        else:
            surviving.append(row)

    return surviving, violations


# ---------------------------------------------------------------------------
# Step 4 — Deduplication
# ---------------------------------------------------------------------------

def _dedup_key(row: dict) -> tuple:
    """Return the dedup identity key for a row."""
    qualifier = row.get("qualifier")
    # Normalize null/empty qualifier to None
    if qualifier is not None and not str(qualifier).strip():
        qualifier = None
    return (
        row.get("source_slug", ""),
        row.get("edge_type", ""),
        row.get("target_slug", ""),
        qualifier,
    )


def _dedup_score(row: dict) -> tuple:
    """Return a score tuple for tie-breaking (higher = preferred).

    Priority:
      1. locate_status == "verbatim" (best evidence quality)
      2. confidence_tier == 1 (vs 2, 3, ...)
      3. evidence_ref present (not null/empty)
    """
    verbatim = 1 if row.get("locate_status") == "verbatim" else 0
    tier = row.get("confidence_tier", 99)
    tier_score = -tier  # lower tier number = better, negate for max-sort
    has_ref = 1 if row.get("evidence_ref") else 0
    return (verbatim, tier_score, has_ref)


def deduplicate(rows: list[dict]) -> tuple[list[dict], int]:
    """Deduplicate rows by (source_slug, edge_type, target_slug, qualifier).

    When duplicates exist, keep the row with the best dedup_score.
    Records dup_count on the surviving row.

    Returns (surviving_rows, total_dup_count).
    """
    buckets: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        key = _dedup_key(row)
        buckets[key].append(row)

    surviving: list[dict] = []
    total_dups = 0

    for key, group in buckets.items():
        if len(group) == 1:
            row = dict(group[0])
            row["dup_count"] = 0
            surviving.append(row)
        else:
            group_sorted = sorted(group, key=_dedup_score, reverse=True)
            winner = dict(group_sorted[0])
            winner["dup_count"] = len(group) - 1
            total_dups += len(group) - 1
            surviving.append(winner)

    return surviving, total_dups


# ---------------------------------------------------------------------------
# Step 5 — Write outputs
# ---------------------------------------------------------------------------

def write_jsonl(path: Path, rows: list[dict]) -> None:
    """Write rows as newline-delimited JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _top_n_histogram(rows: list[dict], field: str, n: int) -> list[tuple[str, int]]:
    """Return top-N (value, count) pairs sorted descending."""
    counts: Counter = Counter()
    for row in rows:
        val = row.get(field) or "(none)"
        counts[val] += 1
    return counts.most_common(n)


def write_report(
    path: Path,
    *,
    total_in: int,
    total_out: int,
    spine_in: int,
    tail_in: int,
    hosp_in: int,
    dropped_by_reason: Counter,
    dropped_by_source: Counter,
    violation_by_kind: Counter,
    dup_count: int,
    surviving: list[dict],
    run_ts: str,
) -> None:
    """Write a formalize-report.md with aggregate stats."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    a = lines.append

    a("# Stage 4 Edge Formalization Report")
    a("")
    a(f"Generated: {run_ts}")
    a("")
    a("## Totals")
    a("")
    a(f"| Metric | Count |")
    a(f"|--------|-------|")
    a(f"| Total rows loaded (pre-gate) | {total_in:,} |")
    a(f"| Spine rows | {spine_in:,} |")
    a(f"| Tail rows | {tail_in:,} |")
    a(f"| Hospitality rows | {hosp_in:,} |")
    a(f"| Dropped by endpoint gate | {sum(dropped_by_reason.values()):,} |")
    a(f"| Quarantined by tail violations | {sum(violation_by_kind.values()):,} |")
    a(f"| Duplicate rows collapsed | {dup_count:,} |")
    a(f"| **Final surviving edges** | **{total_out:,}** |")
    a("")

    a("## Drops by Source Set")
    a("")
    a("| Source Set | Dropped |")
    a("|------------|---------|")
    for src in ("spine", "tail", "hospitality"):
        a(f"| {src} | {dropped_by_source.get(src, 0):,} |")
    a("")

    a("## Drops by Reason Category")
    a("")
    a("| Reason | Count |")
    a("|--------|-------|")
    for reason, cnt in sorted(dropped_by_reason.items(), key=lambda x: -x[1]):
        a(f"| {reason} | {cnt:,} |")
    a("")

    a("## Tail Violation Quarantine")
    a("")
    a("| Violation Kind | Count |")
    a("|----------------|-------|")
    for kind, cnt in sorted(violation_by_kind.items(), key=lambda x: -x[1]):
        a(f"| {kind} | {cnt:,} |")
    a("")

    a("## Top 25 Edge Types in Final Set")
    a("")
    a("| Edge Type | Count |")
    a("|-----------|-------|")
    for et, cnt in _top_n_histogram(surviving, "edge_type", 25):
        a(f"| {et} | {cnt:,} |")
    a("")

    a("## By Source Set")
    a("")
    a("| Source Set | Count |")
    a("|------------|-------|")
    for src, cnt in _top_n_histogram(surviving, "source_set", 10):
        a(f"| {src} | {cnt:,} |")
    a("")

    a("## By Confidence Tier")
    a("")
    a("| Tier | Count |")
    a("|------|-------|")
    for tier, cnt in sorted(_top_n_histogram(surviving, "confidence_tier", 10)):
        a(f"| {tier} | {cnt:,} |")
    a("")

    a("## By typed_by")
    a("")
    a("| typed_by | Count |")
    a("|----------|-------|")
    for tb, cnt in _top_n_histogram(surviving, "typed_by", 15):
        a(f"| {tb} | {cnt:,} |")
    a("")

    a("## By evidence_kind")
    a("")
    a("| evidence_kind | Count |")
    a("|---------------|-------|")
    for ek, cnt in _top_n_histogram(surviving, "evidence_kind", 10):
        a(f"| {ek} | {cnt:,} |")
    a("")

    path.write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# Step 6 — Audit sample
# ---------------------------------------------------------------------------

def write_audit_sample(path: Path, surviving: list[dict], seed: int = 42) -> list[dict]:
    """Write a deterministic random sample of 30 surviving edges."""
    rng = random.Random(seed)
    n = min(30, len(surviving))
    sample = rng.sample(surviving, n)
    path.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(path, sample)
    return sample


# ---------------------------------------------------------------------------
# Precision filter constants and helpers
# ---------------------------------------------------------------------------

# Edge types produced before the lockdown pass that need a dedicated re-typing
# pass before they can be trusted.  These are quarantined, NOT deleted — they
# carry source_set information so spine-sourced rows (Pass-1-hint derived,
# more reliable) can be distinguished from tail-sourced (pre-lockdown LLM).
_GATED_TYPES: frozenset[str] = frozenset({
    "INFORMS",
    "ADVISES",
    "MANIPULATES",
    "SUPPORTS",
    "ALIAS_OF",
})


def build_character_slug_set(nodes_dir: Path) -> frozenset[str]:
    """Return the set of slugs that have a node file under nodes_dir/characters/.

    A slug is present iff graph/nodes/characters/<slug>.node.md exists.
    This is a pure filesystem check — no YAML parsing required.
    """
    chars_dir = nodes_dir / "characters"
    if not chars_dir.is_dir():
        print(
            f"  [warn] characters dir missing: {chars_dir}",
            file=sys.stderr,
        )
        return frozenset()
    return frozenset(
        p.stem.replace(".node", "")
        for p in chars_dir.glob("*.node.md")
    )


def apply_precision_filter(
    rows: list[dict],
    character_slugs: frozenset[str],
) -> tuple[list[dict], list[dict], list[dict]]:
    """Split rows into (v1_edges, quarantine_gated, quarantine_lowvalue).

    Rule 1 — GATED-TYPE QUARANTINE:
        Any edge whose edge_type is in _GATED_TYPES → quarantine_gated.
        source_set is preserved so callers can distinguish spine from tail.

    Rule 2 — LOW-VALUE QUARANTINE:
        Any CONTEMPORARY_WITH edge where BOTH endpoints resolve to character
        slugs → quarantine_lowvalue.  Determined by presence in
        graph/nodes/characters/<slug>.node.md.

    Rule 3 — Everything else → v1_edges.

    Rules are evaluated in order; a row that matches Rule 1 is NOT also
    tested for Rule 2.
    """
    v1: list[dict] = []
    gated: list[dict] = []
    lowvalue: list[dict] = []

    for row in rows:
        et = row.get("edge_type", "")

        if et in _GATED_TYPES:
            gated.append(row)
            continue

        if et == "CONTEMPORARY_WITH":
            src = row.get("source_slug", "")
            tgt = row.get("target_slug", "")
            if src in character_slugs and tgt in character_slugs:
                lowvalue.append(row)
                continue

        v1.append(row)

    return v1, gated, lowvalue


def write_precision_filter_report(
    path: Path,
    *,
    total_in: int,
    v1_count: int,
    gated_count: int,
    lowvalue_count: int,
    gated_by_source: Counter,
    gated_by_type_source: Counter,
    v1_rows: list[dict],
    run_ts: str,
) -> None:
    """Write precision-filter-report.md."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    a = lines.append

    a("# Stage 4 Precision Filter Report")
    a("")
    a(f"Generated: {run_ts}")
    a("")
    a("## Counts")
    a("")
    a("| Metric | Count |")
    a("|--------|-------|")
    a(f"| Input edges (from edges.jsonl) | {total_in:,} |")
    a(f"| **edges-v1.jsonl (surviving)** | **{v1_count:,}** |")
    a(f"| quarantine-gated.jsonl | {gated_count:,} |")
    a(f"| quarantine-lowvalue.jsonl | {lowvalue_count:,} |")
    a("")

    a("## Gated-Type Quarantine by source_set")
    a("")
    a("| source_set | Count |")
    a("|------------|-------|")
    for src in ("spine", "tail", "hospitality"):
        cnt = gated_by_source.get(src, 0)
        a(f"| {src} | {cnt:,} |")
    a("")

    a("## Gated-Type Quarantine by (edge_type, source_set)")
    a("")
    a("| edge_type | source_set | Count |")
    a("|-----------|------------|-------|")
    for (et, src), cnt in sorted(gated_by_type_source.items(), key=lambda x: -x[1]):
        a(f"| {et} | {src} | {cnt:,} |")
    a("")

    a("## edges-v1.jsonl Breakdowns")
    a("")

    a("### By edge_type (top 25)")
    a("")
    a("| edge_type | Count |")
    a("|-----------|-------|")
    for et, cnt in _top_n_histogram(v1_rows, "edge_type", 25):
        a(f"| {et} | {cnt:,} |")
    a("")

    a("### By source_set")
    a("")
    a("| source_set | Count |")
    a("|------------|-------|")
    for src, cnt in _top_n_histogram(v1_rows, "source_set", 10):
        a(f"| {src} | {cnt:,} |")
    a("")

    a("### By confidence_tier")
    a("")
    a("| confidence_tier | Count |")
    a("|-----------------|-------|")
    for tier, cnt in sorted(_top_n_histogram(v1_rows, "confidence_tier", 10)):
        a(f"| {tier} | {cnt:,} |")
    a("")

    a("### By typed_by")
    a("")
    a("| typed_by | Count |")
    a("|----------|-------|")
    for tb, cnt in _top_n_histogram(v1_rows, "typed_by", 15):
        a(f"| {tb} | {cnt:,} |")
    a("")

    a("### By evidence_kind")
    a("")
    a("| evidence_kind | Count |")
    a("|---------------|-------|")
    for ek, cnt in _top_n_histogram(v1_rows, "evidence_kind", 10):
        a(f"| {ek} | {cnt:,} |")
    a("")

    path.write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# Precision filter main pipeline
# ---------------------------------------------------------------------------

def run_precision_filter(args: argparse.Namespace) -> None:
    """--precision-filter mode: read edges.jsonl, produce v1 + quarantine files."""
    dry_run = args.dry_run
    nodes_dir = Path(args.graph_nodes) if args.graph_nodes else _REPO / "graph" / "nodes"

    run_ts = datetime.now(timezone.utc).isoformat()
    print(f"Stage 4 Precision Filter — {run_ts}")
    print(f"  STAGING: {_STAGING}")
    print(f"  dry_run: {dry_run}")
    print()

    # ------------------------------------------------------------------
    # Load edges.jsonl (output of the formalize pass)
    # ------------------------------------------------------------------
    edges_path = _STAGING / "edges.jsonl"
    if not edges_path.exists():
        print(f"ERROR: Input not found: {edges_path}", file=sys.stderr)
        print("  Run without --precision-filter first to produce edges.jsonl.", file=sys.stderr)
        sys.exit(1)

    rows: list[dict] = []
    with open(edges_path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    total_in = len(rows)
    print(f"  Loaded {total_in:,} edges from {edges_path}")
    print()

    # ------------------------------------------------------------------
    # Build character slug set
    # ------------------------------------------------------------------
    print(f"  Loading character slug set from {nodes_dir / 'characters'}...")
    character_slugs = build_character_slug_set(nodes_dir)
    print(f"  Character slugs: {len(character_slugs):,}")
    print()

    # ------------------------------------------------------------------
    # Apply precision filter
    # ------------------------------------------------------------------
    print("Applying precision filter...")
    v1_rows, gated_rows, lowvalue_rows = apply_precision_filter(rows, character_slugs)

    # Tally gated by source_set and by (edge_type, source_set)
    gated_by_source: Counter = Counter()
    gated_by_type_source: Counter = Counter()
    for row in gated_rows:
        src = row.get("source_set", "unknown")
        et = row.get("edge_type", "(none)")
        gated_by_source[src] += 1
        gated_by_type_source[(et, src)] += 1

    v1_count = len(v1_rows)
    gated_count = len(gated_rows)
    lowvalue_count = len(lowvalue_rows)

    print(f"  Input:              {total_in:,}")
    print(f"  edges-v1.jsonl:     {v1_count:,}")
    print(f"  quarantine-gated:   {gated_count:,}  (expect ~234)")
    print(f"  quarantine-lowvalue:{lowvalue_count:,}  (expect ~10)")
    print()
    print("  Gated by source_set:")
    for src in ("spine", "tail", "hospitality"):
        print(f"    {src}: {gated_by_source.get(src, 0):,}")
    print()
    print("  Gated by (edge_type, source_set):")
    for (et, src), cnt in sorted(gated_by_type_source.items(), key=lambda x: -x[1]):
        print(f"    {et:<20} {src:<12} {cnt:,}")
    print()

    # Top-15 edge_type histogram for v1
    print("Top 15 edge types in edges-v1.jsonl:")
    for et, cnt in _top_n_histogram(v1_rows, "edge_type", 15):
        print(f"  {et:<35} {cnt:>5,}")
    print()

    if dry_run:
        print("[dry-run] Not writing output files.")
        return

    # ------------------------------------------------------------------
    # Write outputs
    # ------------------------------------------------------------------
    print("Writing outputs...")

    write_jsonl(_STAGING / "edges-v1.jsonl", v1_rows)
    print(f"  Wrote {v1_count:,} edges → {_STAGING / 'edges-v1.jsonl'}")

    write_jsonl(_STAGING / "quarantine-gated.jsonl", gated_rows)
    print(f"  Wrote {gated_count:,} rows  → {_STAGING / 'quarantine-gated.jsonl'}")

    write_jsonl(_STAGING / "quarantine-lowvalue.jsonl", lowvalue_rows)
    print(f"  Wrote {lowvalue_count:,} rows  → {_STAGING / 'quarantine-lowvalue.jsonl'}")

    report_path = _STAGING / "precision-filter-report.md"
    write_precision_filter_report(
        report_path,
        total_in=total_in,
        v1_count=v1_count,
        gated_count=gated_count,
        lowvalue_count=lowvalue_count,
        gated_by_source=gated_by_source,
        gated_by_type_source=gated_by_type_source,
        v1_rows=v1_rows,
        run_ts=run_ts,
    )
    print(f"  Wrote report → {report_path}")

    # Audit sample (seed=43, as specified)
    sample_path = _STAGING / "audit-sample-v1-30.jsonl"
    sample = write_audit_sample(sample_path, v1_rows, seed=43)
    print(f"  Wrote {len(sample)} rows → {sample_path}")
    print()

    # Print audit sample to stdout for human review
    print("=" * 70)
    print("Audit sample — 30 random edges from edges-v1.jsonl (seed=43)")
    print("=" * 70)
    print(f"{'source_slug':<30} {'edge_type':<25} {'target_slug':<30} {'tier':<5} evidence_quote[:80]")
    print("-" * 70)
    for row in sample:
        src = (row.get("source_slug") or "")[:29]
        et = (row.get("edge_type") or "")[:24]
        tgt = (row.get("target_slug") or "")[:29]
        tier = str(row.get("confidence_tier") or "?")
        quote = (row.get("evidence_quote") or row.get("evidence_snippet") or "")[:80]
        print(f"{src:<30} {et:<25} {tgt:<30} {tier:<5} {quote!r}")
    print("=" * 70)
    print()


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main(args: argparse.Namespace) -> None:
    if args.precision_filter:
        run_precision_filter(args)
        return

    dry_run = args.dry_run
    nodes_dir = Path(args.graph_nodes) if args.graph_nodes else _REPO / "graph" / "nodes"

    run_ts = datetime.now(timezone.utc).isoformat()
    print(f"Stage 4 Edge Formalizer — {run_ts}")
    print(f"  STAGING: {_STAGING}")
    print(f"  dry_run: {dry_run}")
    print()

    # ------------------------------------------------------------------
    # Step 1 — Load all three sources
    # ------------------------------------------------------------------
    print("Step 1: Loading sources...")
    spine_rows = load_spine()
    tail_rows = load_tail()
    hosp_rows = load_hospitality()

    print(f"  Spine:       {len(spine_rows):>6,} rows (all emit_edge)")
    print(f"  Tail:        {len(tail_rows):>6,} rows (emit_edge only)")
    print(f"  Hospitality: {len(hosp_rows):>6,} rows (deterministic)")

    # Apply selection rule (emit_edge + non-null edge_type)
    all_rows = []
    for row in spine_rows + tail_rows + hosp_rows:
        if passes_selection(row):
            all_rows.append(row)

    spine_in = sum(1 for r in all_rows if r.get("source_set") == "spine")
    tail_in = sum(1 for r in all_rows if r.get("source_set") == "tail")
    hosp_in = sum(1 for r in all_rows if r.get("source_set") == "hospitality")
    total_in = len(all_rows)

    print(f"\n  After selection rule:")
    print(f"    Spine: {spine_in:,}  Tail: {tail_in:,}  Hospitality: {hosp_in:,}  Total: {total_in:,}")
    print()

    # ------------------------------------------------------------------
    # Step 2 — Endpoint gate
    # ------------------------------------------------------------------
    print("Step 2: Applying endpoint gate...")
    surviving, dropped_ep = apply_endpoint_gate(all_rows)

    # Tally drops
    dropped_by_reason: Counter = Counter()
    dropped_by_source: Counter = Counter()
    for row in dropped_ep:
        reason = row.get("drop_reason", "unknown")
        # Normalize to category: low_quality_source vs low_quality_target
        if "low_quality_source" in reason and "low_quality_target" in reason:
            cat = "both_endpoints_low_quality"
        elif "low_quality_source" in reason:
            cat = "low_quality_source"
        else:
            cat = "low_quality_target"
        dropped_by_reason[cat] += 1
        dropped_by_source[row.get("source_set", "unknown")] += 1

    print(f"  Dropped {len(dropped_ep):,} rows; {len(surviving):,} survive")
    for reason, cnt in sorted(dropped_by_reason.items(), key=lambda x: -x[1]):
        print(f"    {reason}: {cnt:,}")
    print(f"  Drops by source_set: {dict(dropped_by_source)}")
    print()

    # ------------------------------------------------------------------
    # Step 3 — Tail-violation cleanup
    # ------------------------------------------------------------------
    print("Step 3: Applying tail-violation cleanup...")
    print(f"  Loading node type index from {nodes_dir}...")
    node_type_index = build_node_type_index(nodes_dir)
    print(f"  Node index: {len(node_type_index):,} entries")

    surviving, violations = apply_tail_violation_cleanup(surviving, node_type_index)

    violation_by_kind: Counter = Counter()
    for row in violations:
        kind_raw = row.get("violation_kind", "unknown")
        # Normalize to the category prefix before ':'
        kind_cat = kind_raw.split(":")[0]
        violation_by_kind[kind_cat] += 1

    print(f"  Quarantined {len(violations):,} tail violations; {len(surviving):,} remain")
    for kind, cnt in sorted(violation_by_kind.items(), key=lambda x: -x[1]):
        print(f"    {kind}: {cnt:,}")
    print()

    # ------------------------------------------------------------------
    # Step 4 — Deduplication
    # ------------------------------------------------------------------
    print("Step 4: Deduplicating...")
    surviving, dup_count = deduplicate(surviving)
    total_out = len(surviving)
    print(f"  Collapsed {dup_count:,} duplicate rows; {total_out:,} unique edges remain")
    print()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("=" * 60)
    print(f"  Total in:   {total_in:,}")
    print(f"  Total out:  {total_out:,}")
    print(f"  Dropped (endpoint gate):   {len(dropped_ep):,}")
    print(f"  Quarantined (violations):  {len(violations):,}")
    print(f"  Deduplicated:              {dup_count:,}")
    print("=" * 60)
    print()

    # Top-15 edge_type histogram
    print("Top 15 edge types in final set:")
    for et, cnt in _top_n_histogram(surviving, "edge_type", 15):
        print(f"  {et:<35} {cnt:>5,}")
    print()

    if dry_run:
        print("[dry-run] Not writing output files.")
        return

    # ------------------------------------------------------------------
    # Step 5 — Write outputs
    # ------------------------------------------------------------------
    print("Step 5: Writing outputs to staging...")
    write_jsonl(_STAGING / "edges.jsonl", surviving)
    print(f"  Wrote {total_out:,} edges → {_STAGING / 'edges.jsonl'}")

    write_jsonl(_STAGING / "dropped-endpoints.jsonl", dropped_ep)
    print(f"  Wrote {len(dropped_ep):,} dropped → {_STAGING / 'dropped-endpoints.jsonl'}")

    write_jsonl(_STAGING / "tail-violations.jsonl", violations)
    print(f"  Wrote {len(violations):,} violations → {_STAGING / 'tail-violations.jsonl'}")

    report_path = _STAGING / "formalize-report.md"
    write_report(
        report_path,
        total_in=total_in,
        total_out=total_out,
        spine_in=spine_in,
        tail_in=tail_in,
        hosp_in=hosp_in,
        dropped_by_reason=dropped_by_reason,
        dropped_by_source=dropped_by_source,
        violation_by_kind=violation_by_kind,
        dup_count=dup_count,
        surviving=surviving,
        run_ts=run_ts,
    )
    print(f"  Wrote report → {report_path}")

    # ------------------------------------------------------------------
    # Step 6 — Audit sample
    # ------------------------------------------------------------------
    print("Step 6: Writing audit sample...")
    sample_path = _STAGING / "audit-sample-30.jsonl"
    sample = write_audit_sample(sample_path, surviving, seed=42)
    print(f"  Wrote {len(sample)} rows → {sample_path}")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Formalize Stage 4 edges into a clean, merged, deduped, endpoint-gated set."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print stats but do not write output files.",
    )
    parser.add_argument(
        "--precision-filter",
        action="store_true",
        help="Run the precision filter pass against _formalized/edges.jsonl to produce "
             "edges-v1.jsonl, quarantine-gated.jsonl, and quarantine-lowvalue.jsonl.",
    )
    parser.add_argument(
        "--graph-nodes",
        default=None,
        metavar="PATH",
        help="Path to graph/nodes dir (for HOLDS_TITLE type contract and "
             "CONTEMPORARY_WITH person detection). "
             "Defaults to <repo>/graph/nodes.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
