#!/usr/bin/env python3
"""
Stage 4 Haiku — deterministic edge-type-name normalizer.

Scans every `emit_edge` row in prose-edges-haiku/*.edges.jsonl files and
normalizes the `edge_type` field to the closest canonical type from the
locked vocabulary in reference/architecture.md.

This is a PURE PYTHON, NO-MODEL script. All decisions are deterministic.

Normalization strategy (applied in order):
  (a) Exact match against canonical set — pass through unchanged.
  (b) Case/whitespace normalization (upper-strip) — silent fix.
  (c) Explicit alias/morphology table — hardcoded near-miss corrections
      (e.g. TRAVELED_TO → TRAVELS_TO, DIES_AT → DIED_AT).
  (d) difflib similarity against canonical set — rewrite if score ≥ threshold.

Rows below the similarity threshold are left UNCHANGED and recorded as
"unresolved — needs escalation". No model is called for these.

`reject_just_mention` and other non-emit-edge rows pass through untouched.

Rewrites are ATOMIC (write temp + rename) and IDEMPOTENT (second run = no-op).

HARD CONSTRAINTS:
  - Only reads/writes prose-edges-haiku/ directories.
  - Never touches prose-edges/ (Sonnet output) or anything under
    working/missions/2026-05-14-stage4-v1-bulk-sonnet/.

Usage:
    # Dry run (no file writes):
    python3 scripts/stage4-haiku-normalize-edge-types.py --dry-run

    # Real run (rewrites files in place):
    python3 scripts/stage4-haiku-normalize-edge-types.py

    # Narrow scope to one bucket:
    python3 scripts/stage4-haiku-normalize-edge-types.py \\
        --dir working/wiki/pass2-buckets/characters-house-lorch/prose-edges-haiku/

    # Glob override:
    python3 scripts/stage4-haiku-normalize-edge-types.py \\
        --glob 'working/wiki/pass2-buckets/characters-*/prose-edges-haiku/*.edges.jsonl'

    # Dump self-contained vocab reference (regenerate whenever architecture.md changes):
    python3 scripts/stage4-haiku-normalize-edge-types.py \\
        --dump-vocab working/missions/2026-05-19-stage4-haiku/locked-edge-vocab-159.md
"""

from __future__ import annotations

import argparse
import difflib
import glob as glob_module
import importlib.util
import json
import os
import re
import sys
import tempfile
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO = Path(__file__).resolve().parent.parent

# Default glob for Haiku output files only — never Sonnet prose-edges/
DEFAULT_GLOB = "working/wiki/pass2-buckets/*/prose-edges-haiku/*.edges.jsonl"

# Forbidden path substring — never touch Sonnet bulk run artifacts
FORBIDDEN_PATH_SUBSTR = "2026-05-14-stage4-v1-bulk-sonnet"

# Similarity threshold for difflib fuzzy match (0.0–1.0).
# Chosen as 0.80:
#   - Catches clear tense/morphology variants (TRAVELED_TO→TRAVELS_TO: ~0.87,
#     ALLIED_WITH→ALLIES_WITH: ~0.85, ATTENDED→ATTENDS: ~0.86)
#   - Does NOT misfire on short names that differ by 2 chars but mean something
#     completely different (e.g. USES → RULES: ratio ≈ 0.44; GUARDS → KNOWS: 0.30)
#   - Empirically validated against the full drift set found in this corpus.
#     See docstring for judgment call note.
SIMILARITY_THRESHOLD = 0.80

# ---------------------------------------------------------------------------
# Hardcoded alias/morphology table (strategy c).
# These are cases where difflib alone might not hit threshold, OR where we want
# a guaranteed correct mapping regardless of similarity score.
# Key = raw string (upper-cased), value = canonical type.
# ---------------------------------------------------------------------------

ALIAS_TABLE: dict[str, str] = {
    # Morphological variants only: same English verb/noun, differing only by
    # inflection (tense/voice/number) or a literal string corruption.
    # Rule: raw and canonical must be the SAME word — different word = not here.
    # Exception (Session 61, 2026-05-19): semantic-synonym entries are permitted
    # ONLY for cases where (a) the synonym is itself a real English word, (b) the
    # mapping has been explicitly approved (not auto-discovered), and (c) both
    # sides have the same directionality. Marked with `# SYNONYM` below.

    # Verb-tense variants
    "TRAVELED_TO": "TRAVELS_TO",       # past tense → present tense
    "DIES_AT": "DIED_AT",              # present → past tense
    "ALLIED_WITH": "ALLIES_WITH",      # past tense → present tense
    "ATTENDED": "ATTENDS",             # past tense → present tense

    # Typo / string corruption
    "LOCATEDOCATED_AT": "LOCATED_AT",  # doubled-syllable corruption

    # Deprecated synonym — architecture.md § LOCATED_AT:
    # "Deprecated synonym `LOCATED_IN` was emitted by an early parser variant;
    #  normalize on read."
    # LOCATED_IN is NOT a canonical type (excluded from vocab count);
    # deterministically rewrite it to LOCATED_AT.
    "LOCATED_IN": "LOCATED_AT",

    # Semantic synonyms (Session 61, 2026-05-19)
    "ACCOMPANIES": "TRAVELS_WITH",     # SYNONYM — both symmetric; approved Session 61

}

# Types that Haiku invented which are semantically distinct from any canonical type.
# These are NOT alias-table candidates — different words/concepts, not inflections.
# They must stay visible as classification errors (not be silently rewritten),
# so the drift-measurement signal against Sonnet output remains uncorrupted.
SEMANTIC_DISTINCT_TYPES: set[str] = {
    "GRANDCHILD_OF",
    "SUPERVISES",
    "REPORTS_TO",
    "TRADED_FOR",          # maps to PRISONER_EXCHANGE_FOR case-by-case via residual-resolve
    "USES",
    "ATTACKED_BY",
    "FOSTERED_BY_INVERSE",
    # FOSTERED_BY is NOT a morphological variant of WARD_OF — it is the reverse
    # DIRECTION (architecture.md line 158: "Reverse-direction FOSTERED_BY (Guardian → Ward)").
    # A type-only rewrite to WARD_OF is direction-unsafe in general; only coincidentally
    # correct for the single current corpus instance. Route to unresolved log with a
    # direction-specific reason rather than silently rewriting.
    "FOSTERED_BY",
    # IMPRISONED_AT, TRAVELS_WITH, ENCOUNTERS, GUARDS removed Session 61 (2026-05-19)
    # — these are now canonical edge types in the locked vocabulary.
    # ACCOMPANIES moved to ALIAS_TABLE → TRAVELS_WITH (semantic synonym).
}

# Per-type reason overrides for the unresolved-edges-log.
# When a type appears here its reason string overrides the default bucket reason.
SEMANTIC_DISTINCT_REASON_OVERRIDES: dict[str, str] = {
    "FOSTERED_BY": "reverse-direction-of-ward-of-needs-direction-aware-handling",
}

# ---------------------------------------------------------------------------
# Vocab loader (imported from validator to ensure single source of truth)
# ---------------------------------------------------------------------------

def _load_validator_module() -> object:
    """Load wiki-pass2-validate-edge-jsonl.py via importlib (filename has hyphens)."""
    validator_path = REPO / "scripts" / "wiki-pass2-validate-edge-jsonl.py"
    spec = importlib.util.spec_from_file_location(
        "wiki_pass2_validate_edge_jsonl", validator_path
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_canonical_vocab(arch_path: Path) -> frozenset[str]:
    """Load canonical edge types from architecture.md via the validator's parser."""
    mod = _load_validator_module()
    return frozenset(mod.load_canonical_vocab(arch_path))


# ---------------------------------------------------------------------------
# Core normalization logic (importable)
# ---------------------------------------------------------------------------

def normalize_edge_type(
    raw: str,
    canonical: frozenset[str],
) -> tuple[Optional[str], float]:
    """Normalize a raw edge_type string to the nearest canonical type.

    Returns (canonical_name_or_None, score):
      - score = 1.0 for exact/alias match
      - score = difflib ratio for fuzzy match
      - score = 0.0 for unresolved (returned value is None)

    Does NOT mutate anything — pure function.
    """
    if not raw:
        return None, 0.0

    # (a) Exact match (already canonical)
    if raw in canonical:
        return raw, 1.0

    # (b) Case/whitespace normalization
    normalized = raw.strip().upper()
    if normalized in canonical:
        return normalized, 1.0

    # (c) Alias/morphology table
    if normalized in ALIAS_TABLE:
        alias_target = ALIAS_TABLE[normalized]
        if alias_target in canonical:
            return alias_target, 1.0
        # Alias target itself not canonical — fall through to fuzzy
        # (shouldn't happen if ALIAS_TABLE is maintained correctly)

    # (c2) Semantically-distinct invented types — do NOT rewrite, do NOT fuzzy-match.
    # Return a special sentinel so the caller can route to the semantic-distinct bucket.
    if normalized in SEMANTIC_DISTINCT_TYPES:
        return "__SEMANTIC_DISTINCT__", 0.0

    # (d) difflib fuzzy match against canonical set
    matches = difflib.get_close_matches(
        normalized, canonical, n=1, cutoff=SIMILARITY_THRESHOLD
    )
    if matches:
        best = matches[0]
        score = difflib.SequenceMatcher(None, normalized, best).ratio()
        return best, score

    return None, 0.0


# ---------------------------------------------------------------------------
# File-level normalization
# ---------------------------------------------------------------------------

def normalize_file(
    path: Path,
    canonical: frozenset[str],
    dry_run: bool = False,
) -> dict:
    """Normalize all emit_edge rows in a single .edges.jsonl file.

    Returns a stats dict:
      {
        'total_rows': int,
        'emit_edge_rows': int,
        'already_canonical': int,
        'rewritten': list[{raw, canonical, score, strategy, line_no}],
        'semantic_distinct': list[{raw, line_no}],   # non-canonical, cross-lemma — NOT rewritten
        'schema_violations': list[{raw, line_no}],   # missing edge_type field entirely
        'unresolved': list[{raw, line_no}],           # below difflib threshold
        'skipped_non_emit': int,
      }
    """
    stats = {
        "total_rows": 0,
        "emit_edge_rows": 0,
        "already_canonical": 0,
        "rewritten": [],
        "semantic_distinct": [],
        "schema_violations": [],
        "unresolved": [],
        "skipped_non_emit": 0,
    }

    lines_in = path.read_text(encoding="utf-8").splitlines(keepends=True)
    lines_out = []
    changed = False

    for line_no, raw_line in enumerate(lines_in, 1):
        stats["total_rows"] += 1
        stripped = raw_line.strip()
        if not stripped:
            lines_out.append(raw_line)
            continue

        try:
            row = json.loads(stripped)
        except json.JSONDecodeError:
            # Pass through unparseable lines unchanged
            lines_out.append(raw_line)
            continue

        decision = row.get("decision")
        if decision != "emit_edge":
            stats["skipped_non_emit"] += 1
            lines_out.append(raw_line)
            continue

        stats["emit_edge_rows"] += 1

        # Distinguish "field absent" from "field present but empty"
        if "edge_type" not in row:
            # Missing required field — schema violation, pass through unchanged
            stats["schema_violations"].append({
                "raw": "<missing>",
                "line_no": line_no,
                "source_slug": row.get("source_slug", ""),
                "target_slug": row.get("target_slug", ""),
                "evidence_snippet": row.get("evidence_snippet", ""),
            })
            lines_out.append(raw_line)
            continue

        raw_et = row.get("edge_type", "")

        if raw_et in canonical:
            stats["already_canonical"] += 1
            lines_out.append(raw_line)
            continue

        canonical_name, score = normalize_edge_type(raw_et, canonical)

        if canonical_name == "__SEMANTIC_DISTINCT__":
            # Non-canonical invented type — semantically different word, NOT a morphological
            # variant. Do NOT rewrite. Route to report-only bucket so drift signal is visible.
            stats["semantic_distinct"].append({
                "raw": raw_et,
                "line_no": line_no,
                "source_slug": row.get("source_slug", ""),
                "target_slug": row.get("target_slug", ""),
                "evidence_snippet": row.get("evidence_snippet", ""),
            })
            lines_out.append(raw_line)
        elif canonical_name is not None:
            # Morphological variant or difflib hit — rewrite
            normalized_raw = raw_et.strip().upper()
            if normalized_raw == canonical_name:
                strategy = "case-normalize"
            elif normalized_raw in ALIAS_TABLE and ALIAS_TABLE[normalized_raw] == canonical_name:
                strategy = "alias-table"
            else:
                strategy = f"difflib({score:.2f})"

            stats["rewritten"].append({
                "raw": raw_et,
                "canonical": canonical_name,
                "score": score,
                "strategy": strategy,
                "line_no": line_no,
            })
            row["edge_type"] = canonical_name
            new_line = json.dumps(row, ensure_ascii=False) + "\n"
            lines_out.append(new_line)
            changed = True
        else:
            # Below difflib threshold — unresolved
            stats["unresolved"].append({
                "raw": raw_et,
                "line_no": line_no,
                "source_slug": row.get("source_slug", ""),
                "target_slug": row.get("target_slug", ""),
                "evidence_snippet": row.get("evidence_snippet", ""),
            })
            lines_out.append(raw_line)

    if changed and not dry_run:
        _write_atomic(path, lines_out)

    return stats


def _write_atomic(path: Path, lines: list[str]) -> None:
    """Write lines to path atomically (temp file + rename)."""
    tmp_fd, tmp_path = tempfile.mkstemp(
        dir=path.parent, prefix=".tmp-norm-", suffix=".jsonl"
    )
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            f.writelines(lines)
        os.replace(tmp_path, path)
    except Exception:
        # Clean up temp on failure
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


# ---------------------------------------------------------------------------
# Persistent unresolved-edges log
# ---------------------------------------------------------------------------

# Deduplication key fields — a row is "the same" if all five match.
# Using a tuple so it can be used as a dict key or set member.
_LOG_DEDUP_FIELDS = ("file", "source_slug", "target_slug", "raw_edge_type", "stage")


def _derive_batch_id(file_path: Path) -> Optional[str]:
    """Best-effort: derive a batch_id from the file path.

    Haiku paths look like:
      .../pass2-buckets/<bucket>/prose-edges-haiku/<slug>.edges.jsonl
    We return the <bucket> segment as the batch_id surrogate.
    Returns None if the structure is not recognisable.
    """
    parts = file_path.parts
    for i, part in enumerate(parts):
        if part == "prose-edges-haiku" and i >= 1:
            return parts[i - 1]  # the bucket directory name
    return None


def load_existing_log_keys(log_path: Path) -> set[tuple]:
    """Read an existing unresolved-edges-log.jsonl and return the set of dedup keys.

    Returns an empty set if the file does not exist or is unreadable.
    """
    keys: set[tuple] = set()
    if not log_path.exists():
        return keys
    try:
        with log_path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                    key = tuple(row.get(field, "") for field in _LOG_DEDUP_FIELDS)
                    keys.add(key)
                except json.JSONDecodeError:
                    continue
    except OSError:
        pass
    return keys


def build_unresolved_log_rows(
    file_results: list[tuple[Path, dict]],
    existing_keys: set[tuple],
    stage: str = "normalizer-residual",
) -> list[dict]:
    """Build new unresolved-edges-log rows from file_results, deduplicating against existing_keys.

    Covers two classes of unresolved rows:
      1. semantic_distinct — Haiku invented a type that is semantically distinct from any
         canonical type; not rewritten, must be resolved by a later pass.
         reason: "semantically-distinct-no-safe-match"
      2. schema_violations — emit_edge rows missing the edge_type field entirely.
         reason: "missing-edge-type-field"
    (The "unresolved — below difflib threshold" bucket is also included if it has entries,
    though the current corpus has none.)

    Returns a list of new rows to append (does NOT include duplicates).
    """
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new_rows: list[dict] = []
    seen_new: set[tuple] = set()  # dedup within this run too

    def _add(file_path: Path, entry: dict, raw_et: str, reason: str) -> None:
        file_str = str(file_path)
        source_slug = entry.get("source_slug", "")
        target_slug = entry.get("target_slug", "")
        key = (file_str, source_slug, target_slug, raw_et, stage)
        if key in existing_keys or key in seen_new:
            return
        seen_new.add(key)
        snippet = entry.get("evidence_snippet", "")
        if isinstance(snippet, str) and len(snippet) > 200:
            snippet = snippet[:200] + "…"
        batch_id = _derive_batch_id(file_path)
        new_rows.append({
            "timestamp": ts,
            "stage": stage,
            "batch_id": batch_id,
            "file": file_str,
            "source_slug": source_slug,
            "target_slug": target_slug,
            "raw_edge_type": raw_et,
            "evidence_snippet": snippet,
            "reason": reason,
        })

    for path, stats in file_results:
        for entry in stats.get("semantic_distinct", []):
            raw = entry["raw"]
            reason = SEMANTIC_DISTINCT_REASON_OVERRIDES.get(
                raw.strip().upper(), "semantically-distinct-no-safe-match"
            )
            _add(path, entry, raw, reason)
        for entry in stats.get("schema_violations", []):
            _add(path, entry, entry["raw"], "missing-edge-type-field")
        for entry in stats.get("unresolved", []):
            _add(path, entry, entry["raw"], "below-difflib-threshold")

    return new_rows


def append_unresolved_log(log_path: Path, new_rows: list[dict], dry_run: bool) -> int:
    """Append new_rows to log_path.  Returns number of rows appended (0 in dry_run).

    Uses atomic append via temp+rename to avoid partial writes.
    If log_path exists, reads it first so we can combine old + new into a single
    consistent file (preserving idempotency on second run).
    """
    if not new_rows:
        return 0
    if dry_run:
        return 0

    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Read existing content verbatim
    existing_content = b""
    if log_path.exists():
        existing_content = log_path.read_bytes()

    # Write existing + new rows atomically
    tmp_fd, tmp_path_str = tempfile.mkstemp(
        dir=log_path.parent, prefix=".tmp-unresolvedlog-", suffix=".jsonl"
    )
    try:
        with os.fdopen(tmp_fd, "wb") as f:
            if existing_content:
                f.write(existing_content)
                if not existing_content.endswith(b"\n"):
                    f.write(b"\n")
            for row in new_rows:
                f.write((json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8"))
        os.replace(tmp_path_str, log_path)
    except Exception:
        try:
            os.unlink(tmp_path_str)
        except OSError:
            pass
        raise

    return len(new_rows)


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def discover_files(args: argparse.Namespace) -> list[Path]:
    """Return list of .edges.jsonl paths to process, based on CLI args."""
    if hasattr(args, "dir") and args.dir:
        base = REPO / args.dir if not Path(args.dir).is_absolute() else Path(args.dir)
        paths = sorted(base.glob("*.edges.jsonl"))
    elif hasattr(args, "glob") and args.glob:
        pattern = args.glob
        # Support both relative (from repo root) and absolute
        if not Path(pattern).is_absolute():
            pattern = str(REPO / pattern)
        paths = sorted(Path(p) for p in glob_module.glob(pattern))
    else:
        pattern = str(REPO / DEFAULT_GLOB)
        paths = sorted(Path(p) for p in glob_module.glob(pattern))

    # Safety: filter out any path in the forbidden Sonnet mission dir
    safe = []
    for p in paths:
        if FORBIDDEN_PATH_SUBSTR in str(p):
            print(
                f"WARNING: skipping {p} — matches forbidden path substring "
                f"'{FORBIDDEN_PATH_SUBSTR}'",
                file=sys.stderr,
            )
            continue
        # Also guard against accidentally hitting non-haiku prose-edges/
        if "/prose-edges/" in str(p) and "/prose-edges-haiku/" not in str(p):
            print(
                f"WARNING: skipping {p} — is in prose-edges/ (Sonnet), not prose-edges-haiku/",
                file=sys.stderr,
            )
            continue
        safe.append(p)

    return safe


# ---------------------------------------------------------------------------
# Aggregation and report generation
# ---------------------------------------------------------------------------

def aggregate_results(
    file_results: list[tuple[Path, dict]],
    canonical: frozenset[str],
) -> dict:
    """Aggregate per-file stats into a corpus-level summary."""
    total_files = len(file_results)
    total_rows = 0
    total_emit = 0
    total_already = 0
    total_unresolved_count = 0
    total_schema_violation_count = 0

    # mapping_table: raw → {canonical, strategy, count, files}
    mapping_table: dict[str, dict] = {}
    # semantic_distinct_table: raw → {count, example_file}
    semantic_distinct_table: dict[str, dict] = {}
    # schema_violation_table: raw → {count, example_file}
    schema_violation_table: dict[str, dict] = {}
    # unresolved_table: raw → {count, example_file}
    unresolved_table: dict[str, dict] = {}

    for path, stats in file_results:
        total_rows += stats["total_rows"]
        total_emit += stats["emit_edge_rows"]
        total_already += stats["already_canonical"]

        for rw in stats["rewritten"]:
            raw = rw["raw"]
            if raw not in mapping_table:
                mapping_table[raw] = {
                    "canonical": rw["canonical"],
                    "strategy": rw["strategy"],
                    "count": 0,
                    "files": [],
                }
            mapping_table[raw]["count"] += 1
            rel_path = _rel(path)
            if rel_path not in mapping_table[raw]["files"]:
                mapping_table[raw]["files"].append(rel_path)

        for sd in stats.get("semantic_distinct", []):
            raw = sd["raw"]
            if raw not in semantic_distinct_table:
                semantic_distinct_table[raw] = {"count": 0, "example_file": _rel(path)}
            semantic_distinct_table[raw]["count"] += 1

        for sv in stats.get("schema_violations", []):
            raw = sv["raw"]
            total_schema_violation_count += 1
            if raw not in schema_violation_table:
                schema_violation_table[raw] = {"count": 0, "example_file": _rel(path)}
            schema_violation_table[raw]["count"] += 1

        for ur in stats["unresolved"]:
            raw = ur["raw"]
            total_unresolved_count += 1
            if raw not in unresolved_table:
                unresolved_table[raw] = {"count": 0, "example_file": _rel(path)}
            unresolved_table[raw]["count"] += 1

    total_rewritten = sum(v["count"] for v in mapping_table.values())
    total_semantic_distinct = sum(v["count"] for v in semantic_distinct_table.values())

    return {
        "total_files": total_files,
        "total_rows": total_rows,
        "total_emit_edge_rows": total_emit,
        "already_canonical": total_already,
        "rewritten": total_rewritten,
        "semantic_distinct": total_semantic_distinct,
        "schema_violations": total_schema_violation_count,
        "unresolved": total_unresolved_count,
        "mapping_table": mapping_table,
        "semantic_distinct_table": semantic_distinct_table,
        "schema_violation_table": schema_violation_table,
        "unresolved_table": unresolved_table,
        "vocab_size": len(canonical),
        "canonical_sorted": sorted(canonical),
    }


def _rel(path: Path) -> str:
    """Return path relative to repo root for display."""
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


def build_report(agg: dict, dry_run: bool) -> str:
    """Generate the markdown normalizer report — three-bucket variant section."""
    today = date.today().isoformat()
    mode = "DRY RUN — no files were modified" if dry_run else "LIVE RUN — files rewritten in place"

    lines = [
        f"# Stage 4 Haiku Edge-Type Normalizer Report — {today}",
        f"",
        f"> **Mode:** {mode}",
        f"",
        f"## Summary",
        f"",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Canonical vocab size | {agg['vocab_size']} |",
        f"| Files scanned | {agg['total_files']} |",
        f"| Total rows scanned | {agg['total_rows']} |",
        f"| `emit_edge` rows | {agg['total_emit_edge_rows']} |",
        f"| Already canonical | {agg['already_canonical']} |",
        f"| Morphological — auto-rewritten | {agg['rewritten']} |",
        f"| Semantically distinct — NOT rewritten | {agg['semantic_distinct']} |",
        f"| Schema violations (missing field) | {agg['schema_violations']} |",
        f"| Below difflib threshold — unresolved | {agg['unresolved']} |",
        f"",
    ]

    # ------------------------------------------------------------------
    # Bucket 1: Morphological — auto-rewritten
    # ------------------------------------------------------------------
    mt = agg["mapping_table"]
    lines += [
        "## Bucket 1 — Morphological: auto-rewritten",
        "",
        "Same English verb/noun, differing only by inflection (tense) or literal string corruption.",
        "These are the ONLY rows the normalizer actually rewrites.",
        "",
    ]
    if mt:
        lines += [
            "| Raw (Haiku output) | Canonical | Strategy | Count | Affected files |",
            "|--------------------|-----------|----------|-------|----------------|",
        ]
        for raw, info in sorted(mt.items(), key=lambda kv: -kv[1]["count"]):
            files_str = ", ".join(f"`{f}`" for f in info["files"][:3])
            if len(info["files"]) > 3:
                files_str += f" (+{len(info['files']) - 3} more)"
            lines.append(
                f"| `{raw}` | `{info['canonical']}` | {info['strategy']} "
                f"| {info['count']} | {files_str} |"
            )
        lines.append("")
    else:
        lines += ["_No morphological rewrites in this run._", ""]

    # ------------------------------------------------------------------
    # Bucket 2: Non-canonical, semantically distinct — NOT rewritten
    # ------------------------------------------------------------------
    sdt = agg["semantic_distinct_table"]
    lines += [
        "## Bucket 2 — Non-canonical, semantically distinct: NOT rewritten",
        "",
        "These types are different words/concepts — not inflections of a canonical type.",
        "They must stay visible as classification errors so drift-measurement signal",
        "against Sonnet output is not corrupted. Needs re-classification or model escalation.",
        "",
    ]
    if sdt:
        lines += [
            "| Raw | Count | Example file |",
            "|-----|-------|-------------|",
        ]
        for raw, info in sorted(sdt.items(), key=lambda kv: -kv[1]["count"]):
            lines.append(
                f"| `{raw}` | {info['count']} | `{info['example_file']}` |"
            )
        lines.append("")
    else:
        lines += ["_No semantically-distinct non-canonical types found._", ""]

    # ------------------------------------------------------------------
    # Bucket 3: Schema violations (missing edge_type field entirely)
    # ------------------------------------------------------------------
    svt = agg["schema_violation_table"]
    lines += [
        "## Bucket 3 — Schema violations: missing `edge_type` field",
        "",
        "emit_edge rows that are missing the `edge_type` field entirely.",
        "Passed through unchanged — these are structural errors, not normalization targets.",
        "",
    ]
    if svt:
        lines += [
            "| Raw | Count | Example file |",
            "|-----|-------|-------------|",
        ]
        for raw, info in sorted(svt.items(), key=lambda kv: -kv[1]["count"]):
            lines.append(
                f"| `{raw}` | {info['count']} | `{info['example_file']}` |"
            )
        lines.append("")
    else:
        lines += ["_No schema violations found._", ""]

    # ------------------------------------------------------------------
    # Below-threshold unresolved (difflib could not match)
    # ------------------------------------------------------------------
    ut = agg["unresolved_table"]
    if ut:
        lines += [
            "## Below-Threshold Unresolved (difflib could not match)",
            "",
            "These types fell below the 0.80 difflib threshold and are not in SEMANTIC_DISTINCT_TYPES.",
            "They are left unchanged. If this bucket is non-empty, review whether they should be",
            "added to SEMANTIC_DISTINCT_TYPES or the alias table.",
            "",
            "| Raw | Count | Example file |",
            "|-----|-------|-------------|",
        ]
        for raw, info in sorted(ut.items(), key=lambda kv: -kv[1]["count"]):
            lines.append(
                f"| `{raw}` | {info['count']} | `{info['example_file']}` |"
            )
        lines.append("")

    # ------------------------------------------------------------------
    # Canonical edge-type list (full sorted, for eyeball check)
    # ------------------------------------------------------------------
    canonical_sorted = agg.get("canonical_sorted", [])
    lines += [
        "## Canonical Edge-Type List (full sorted, for eyeball check)",
        "",
        f"Parser returned {len(canonical_sorted)} types. Locked count of record is 164.",
        "If the count differs by ±2, check for non-edge-type backticked tokens in the",
        "Edge Types section of architecture.md (book abbreviations, file extensions, etc.).",
        "",
    ]
    for i, et in enumerate(canonical_sorted, 1):
        lines.append(f"{i:3d}. `{et}`")
    lines.append("")

    lines += [
        "---",
        f"",
        f"*Generated by `scripts/stage4-haiku-normalize-edge-types.py` — {today}*",
    ]

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Vocab reference dump (--dump-vocab)
# ---------------------------------------------------------------------------

def _parse_edge_tables(arch_path: Path) -> list[dict]:
    """Parse architecture.md Edge Types section and return one dict per canonical edge type.

    Each dict has keys: type_name, description, directionality, subsection.

    Only rows whose FIRST backticked token is the edge type name (i.e., first cell of
    a table row) are included — same filter as load_canonical_vocab().  Description prose
    and non-type mentions in description cells are not extracted as separate entries.
    """
    text = arch_path.read_text()
    start = text.find("## Edge Types")
    if start < 0:
        raise RuntimeError("Could not find ## Edge Types section in architecture.md")
    end_match = re.search(r"\n## [^#]", text[start + 5:])
    end = (start + 5 + end_match.start()) if end_match else len(text)
    section = text[start:end]

    entries: list[dict] = []
    current_subsection = "General"

    for line in section.splitlines():
        # Track subsection headings (### ...)
        if line.startswith("### "):
            current_subsection = line[4:].strip()
            continue

        # Table row starting with | `TYPE_NAME` |
        m = re.match(r"^\| `([A-Z][A-Z_]+)` \| (.+)$", line)
        if not m:
            continue

        type_name = m.group(1)
        remainder = m.group(2)  # "Description | Directionality | ..."

        # Split on " | " — be careful with embedded pipes inside description text
        # The column order in architecture.md tables is:
        #   Edge Type | Description | Directionality | Wiki Source
        # We split on the first two " | " separators.
        parts = remainder.split(" | ")
        if len(parts) < 2:
            description = remainder.strip().rstrip(" |")
            directionality = ""
        else:
            # Strip markdown from description (bold, links, backticks) for readability
            description = parts[0].strip()
            # Remove leading/trailing pipe if present
            description = description.strip(" |")
            directionality = parts[1].strip(" |") if len(parts) > 1 else ""

        entries.append({
            "type_name": type_name,
            "description": description,
            "directionality": directionality,
            "subsection": current_subsection,
        })

    return entries


def dump_vocab_reference(arch_path: Path, out_path: Path) -> int:
    """Generate a self-contained edge-type vocab reference and write it to out_path.

    Returns the number of canonical edge types written.
    Sorted alphabetically by type name (not by subsection order) so the downstream
    second-Haiku pass can binary-scan or Ctrl-F by name.
    """
    entries = _parse_edge_tables(arch_path)
    # Deduplicate (same-direction entries only; validator-excluded types won't appear
    # because they're only in description cells, not as first-cell tokens)
    seen: set[str] = set()
    deduped: list[dict] = []
    for e in entries:
        if e["type_name"] not in seen:
            seen.add(e["type_name"])
            deduped.append(e)

    deduped.sort(key=lambda e: e["type_name"])

    today = date.today().isoformat()
    lines = [
        f"# Locked Edge-Type Vocabulary Reference — {len(deduped)} types",
        f"",
        f"> Auto-generated {today} from `reference/architecture.md`.",
        f"> Regenerate: `python3 scripts/stage4-haiku-normalize-edge-types.py --dump-vocab <path>`",
        f">",
        f"> **Do not edit this file by hand.** Update `reference/architecture.md` and regenerate.",
        f">",
        f"> Design intent: neither the second-Haiku residual-resolution pass nor the final",
        f"> targeted Opus review should need to open `architecture.md` or the classification",
        f"> manual. This file alone is sufficient to pick the correct canonical edge type.",
        f"",
        f"## Format",
        f"",
        f"Each entry: `TYPE_NAME` — Description. *Source → Target*",
        f"",
        f"---",
        f"",
    ]

    for e in deduped:
        direction_str = f" *{e['directionality']}*" if e['directionality'] else ""
        desc = e['description']
        lines.append(f"**`{e['type_name']}`** — {desc}{direction_str}  ")
        lines.append(f"*(subsection: {e['subsection']})*")
        lines.append(f"")

    lines += [
        "---",
        f"",
        f"*{len(deduped)} canonical edge types. Generated by "
        f"`scripts/stage4-haiku-normalize-edge-types.py --dump-vocab`. "
        f"Do not hand-edit — regenerate from architecture.md.*",
    ]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(deduped)


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument(
        "--dir",
        help="Process only .edges.jsonl files in this single directory (absolute or relative to repo root)",
    )
    scope.add_argument(
        "--glob",
        help="Custom glob pattern (relative to repo root, or absolute). "
             f"Default: {DEFAULT_GLOB}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Produce report without writing any file changes",
    )
    parser.add_argument(
        "--arch",
        default=str(REPO / "reference/architecture.md"),
        help="Path to architecture.md for vocab loading",
    )
    parser.add_argument(
        "--report-out",
        help="Path for the markdown report. Defaults to "
             "working/missions/2026-05-19-stage4-haiku/normalizer-report-YYYY-MM-DD.md",
    )
    parser.add_argument(
        "--unresolved-log",
        help="Path for the persistent machine-readable unresolved-edges-log.jsonl. "
             "Defaults to working/missions/2026-05-19-stage4-haiku/unresolved-edges-log.jsonl. "
             "Append-style with deduplication; idempotent across runs.",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print per-file progress to stderr",
    )
    parser.add_argument(
        "--dump-vocab",
        metavar="PATH",
        help="Generate self-contained vocab reference at PATH and exit. "
             "Regenerate whenever architecture.md changes. "
             "Example: working/missions/2026-05-19-stage4-haiku/locked-edge-vocab-159.md",
    )
    args = parser.parse_args()

    # --dump-vocab early-exit mode
    if args.dump_vocab:
        arch_path = Path(args.arch)
        if not arch_path.is_absolute():
            arch_path = REPO / arch_path
        out_path = Path(args.dump_vocab)
        if not out_path.is_absolute():
            out_path = REPO / out_path
        try:
            count = dump_vocab_reference(arch_path, out_path)
            print(f"Vocab reference written: {out_path}")
            print(f"  {count} canonical edge types")
        except Exception as e:
            print(f"ERROR generating vocab reference: {e}", file=sys.stderr)
            return 2
        return 0

    # Load canonical vocab
    arch_path = Path(args.arch)
    if not arch_path.is_absolute():
        arch_path = REPO / arch_path
    try:
        canonical = load_canonical_vocab(arch_path)
    except Exception as e:
        print(f"ERROR: could not load canonical vocab from {arch_path}: {e}", file=sys.stderr)
        return 2

    print(f"Canonical vocab: {len(canonical)} types loaded from {_rel(arch_path)}", file=sys.stderr)

    # Discover files
    files = discover_files(args)
    if not files:
        print("No .edges.jsonl files found matching scope. Nothing to do.", file=sys.stderr)
        return 0

    print(f"Files to process: {len(files)}", file=sys.stderr)
    if args.dry_run:
        print("DRY RUN — no files will be modified.", file=sys.stderr)

    # Process files
    file_results: list[tuple[Path, dict]] = []
    for path in files:
        if args.verbose:
            print(f"  {_rel(path)}", file=sys.stderr)
        try:
            stats = normalize_file(path, canonical, dry_run=args.dry_run)
            file_results.append((path, stats))
        except Exception as e:
            print(f"ERROR processing {path}: {e}", file=sys.stderr)
            # Record as empty result so we don't silently drop it
            file_results.append((path, {
                "total_rows": 0, "emit_edge_rows": 0, "already_canonical": 0,
                "rewritten": [], "semantic_distinct": [], "schema_violations": [],
                "unresolved": [], "skipped_non_emit": 0,
            }))

    # Aggregate
    agg = aggregate_results(file_results, canonical)

    # Print summary to stdout
    print(f"\nNormalizer summary:")
    print(f"  Files scanned:                       {agg['total_files']}")
    print(f"  Total rows scanned:                  {agg['total_rows']}")
    print(f"  emit_edge rows:                      {agg['total_emit_edge_rows']}")
    print(f"  Already canonical:                   {agg['already_canonical']}")
    print(f"  Morphological — rewritten:           {agg['rewritten']}")
    print(f"  Semantically distinct — NOT rewritten: {agg['semantic_distinct']}")
    print(f"  Schema violations (missing field):   {agg['schema_violations']}")
    print(f"  Below difflib threshold — unresolved: {agg['unresolved']}")

    # -----------------------------------------------------------------------
    # Persistent unresolved-edges-log.jsonl
    # -----------------------------------------------------------------------
    if args.unresolved_log:
        log_path = Path(args.unresolved_log)
        if not log_path.is_absolute():
            log_path = REPO / log_path
    else:
        mission_dir_for_log = REPO / "working/missions/2026-05-19-stage4-haiku"
        log_path = mission_dir_for_log / "unresolved-edges-log.jsonl"

    existing_keys = load_existing_log_keys(log_path)
    new_log_rows = build_unresolved_log_rows(file_results, existing_keys)
    appended_count = append_unresolved_log(log_path, new_log_rows, dry_run=args.dry_run)

    if args.dry_run:
        print(f"\nUnresolved-edges-log (DRY RUN — not written): {_rel(log_path)}")
        print(f"  Existing entries: {len(existing_keys)}")
        print(f"  New entries that WOULD be appended: {len(new_log_rows)}")
        if new_log_rows:
            print(f"  Sample new rows:")
            for row in new_log_rows[:3]:
                print(f"    {row['source_slug']} --{row['raw_edge_type']}--> {row['target_slug']}"
                      f"  reason={row['reason']}")
    else:
        print(f"\nUnresolved-edges-log: {_rel(log_path)}")
        print(f"  Appended {appended_count} new entries ({len(existing_keys)} already in log)")

    # -----------------------------------------------------------------------
    # Build and write markdown report
    # -----------------------------------------------------------------------
    report_text = build_report(agg, args.dry_run)

    # Determine report output path
    if args.report_out:
        report_path = Path(args.report_out)
        if not report_path.is_absolute():
            report_path = REPO / report_path
    else:
        today = date.today().isoformat()
        mission_dir = REPO / "working/missions/2026-05-19-stage4-haiku"
        mission_dir.mkdir(parents=True, exist_ok=True)
        report_path = mission_dir / f"normalizer-report-{today}.md"

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8")
    print(f"\nReport written to: {_rel(report_path)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
