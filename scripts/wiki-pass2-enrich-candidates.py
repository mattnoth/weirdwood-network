#!/usr/bin/env python3
"""
Stage 4 candidate enrichment — Session 63 (2026-05-21).

Reads each existing *.candidates.jsonl in
working/wiki/pass2-buckets/<bucket>/prose-edge-candidates/ and rewrites with
these added per-row fields:

  target_type            looked up via build_node_type_index(graph/nodes/)
  evidence_paragraph     clean prose paragraph containing the anchor link;
                         cite_ref noise stripped; other wiki links normalized to «anchor»
  valid_edge_types       edge types whose target type-contract permits target_type,
                         plus all unconstrained types (typically ~140-160 per row)
  staging_verbs_present  list of ENCOUNTERS staging verbs detected in evidence_paragraph
                         (empty list means ENCOUNTERS is impossible per Rule 6)
  _python_prereject      reason string if target slug doesn't resolve to any node
                         (else field absent)

Output goes to prose-edge-candidates-enriched/ alongside the source dir.
Idempotent: re-run produces byte-identical output.

Design principle:
  Make it as easy as possible for Haiku to find ONLY the things relevant to this
  candidate. Each row is a complete decision unit — Haiku reads the row, decides,
  done. No file reads from Haiku.

Usage:
  python3 scripts/wiki-pass2-enrich-candidates.py                       # dry-run (count + sample)
  python3 scripts/wiki-pass2-enrich-candidates.py --apply               # write enriched files
  python3 scripts/wiki-pass2-enrich-candidates.py --bucket <name>       # one bucket
  python3 scripts/wiki-pass2-enrich-candidates.py --bucket <name> --apply
  python3 scripts/wiki-pass2-enrich-candidates.py --verbose             # per-file logging
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NODES_DIR = REPO / "graph" / "nodes"
BUCKETS_DIR = REPO / "working" / "wiki" / "pass2-buckets"
ARCH_MD = REPO / "reference" / "architecture.md"
VALIDATOR_PY = REPO / "scripts" / "wiki-pass2-validate-edge-jsonl.py"


# ── Load validator helpers (node-type index, type contracts, vocab) ────────
def _load_validator():
    spec = importlib.util.spec_from_file_location("validator", VALIDATOR_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── Staging verb whitelist (mirrors validator's VERB_GATE for ENCOUNTERS) ──
STAGING_VERBS = (
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


# ── Prose cleanup ──────────────────────────────────────────────────────────
# Strip `(wiki:PageName.cite_ref-...)` noise that MediaWiki injects into wiki HTML.
CITE_REF_RE = re.compile(r"\(wiki:[^)\s]+?\.cite_ref[^)]*\)")

# Match wiki links: [anchor text](wiki:Page_Name) — possibly with #anchor or other suffix
WIKI_LINK_RE = re.compile(r"\[([^\]]+?)\]\(wiki:[^)]+?\)")


def clean_paragraph(text: str) -> str:
    """Strip cite_ref junk; normalize wiki links to «anchor»; collapse whitespace."""
    text = CITE_REF_RE.sub("", text)
    text = WIKI_LINK_RE.sub(lambda m: f"«{m.group(1)}»", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


# ── Paragraph extraction by section ────────────────────────────────────────
def extract_paragraphs_by_section(node_md: str) -> dict[str, list[str]]:
    """Parse markdown by H2 sections; return {section_header: [paragraphs]}.

    Section header includes the leading "## " for matching against candidate's
    source_section field.
    """
    sections = re.split(r"^(## .+)$", node_md, flags=re.MULTILINE)
    # sections = [preamble, "## Section A", body A, "## Section B", body B, ...]
    out: dict[str, list[str]] = {}
    for i in range(1, len(sections), 2):
        header = sections[i].strip()
        body = sections[i + 1] if i + 1 < len(sections) else ""
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
        out[header] = paragraphs
    return out


def find_anchor_paragraph(
    paragraphs: list[str], target_page: str, anchor_text: str
) -> str | None:
    """Return the first paragraph (raw, uncleaned) containing the target link.

    Matches `[<anchor>](wiki:<page>)`. Falls back to anchor-text-only match if
    no link pattern hits.
    """
    page_link_re = re.compile(
        r"\[[^\]]+\]\(wiki:" + re.escape(target_page) + r"[^)]*?\)"
    )
    for p in paragraphs:
        if page_link_re.search(p):
            return p
    # Fallback: just the anchor text (case-insensitive)
    if anchor_text:
        anchor_re = re.compile(re.escape(anchor_text), re.IGNORECASE)
        for p in paragraphs:
            if anchor_re.search(p):
                return p
    return None


# ── valid_edge_types per target type ───────────────────────────────────────
def compute_valid_edge_types(
    target_type: str | None,
    type_contracts: dict[str, tuple[str | None, tuple[str, ...]]],
    canonical_vocab: set[str],
) -> list[str]:
    """For each edge type in canonical_vocab, include it if either:
      (a) it has no entry in type_contracts (no constraint on target), or
      (b) its contract permits target_type via prefix match.

    Returns sorted list. If target_type is None or '' returns the full vocab.
    """
    if not target_type:
        return sorted(canonical_vocab)
    result: list[str] = []
    for et in sorted(canonical_vocab):
        contract = type_contracts.get(et)
        if contract is None:
            result.append(et)
            continue
        _src, target_patterns = contract
        if any(target_type.startswith(p) for p in target_patterns):
            result.append(et)
    return result


# ── Staging-verb detection ─────────────────────────────────────────────────
def detect_staging_verbs(paragraph: str) -> list[str]:
    """Return list of whitelist verbs/phrases found in paragraph (case-insensitive)."""
    if not paragraph:
        return []
    lower = paragraph.lower()
    return [v for v in STAGING_VERBS if v in lower]


# ── Source-node lookup (memoized) ──────────────────────────────────────────
_NODE_CACHE: dict[str, str] = {}


def load_source_node(slug: str) -> str | None:
    """Find the node file for `slug` under graph/nodes/*/ and return its text.

    Cached. Returns None if not found.
    """
    if slug in _NODE_CACHE:
        return _NODE_CACHE[slug]
    for subdir in NODES_DIR.iterdir():
        if not subdir.is_dir():
            continue
        candidate = subdir / f"{slug}.node.md"
        if candidate.exists():
            text = candidate.read_text()
            _NODE_CACHE[slug] = text
            return text
    _NODE_CACHE[slug] = ""
    return None


# ── Enrichment per row ─────────────────────────────────────────────────────
def enrich_row(
    row: dict,
    node_type_index: dict[str, str],
    type_contracts: dict[str, tuple[str | None, tuple[str, ...]]],
    canonical_vocab: set[str],
    source_paragraphs_cache: dict[str, dict[str, list[str]]],
) -> dict:
    """Return a new row with enrichment fields added. Original fields preserved."""
    out = dict(row)  # shallow copy
    candidate_kind = row.get("candidate_kind")

    # F1 + F3: target_type lookup
    target_slug = row.get("target_slug")
    target_type: str | None = None
    if target_slug:
        target_type = node_type_index.get(target_slug)
    out["target_type"] = target_type
    if target_slug and target_type is None:
        out["_python_prereject"] = "target-slug-unresolved"

    # F2: evidence_paragraph (source_target candidates only — others have their own schema)
    if candidate_kind == "source_target":
        source_slug = row.get("source_slug")
        source_section = row.get("source_section")
        target_page = row.get("target_page") or ""
        anchor_text = row.get("anchor_text") or ""

        # Load + parse the source node once per slug
        if source_slug not in source_paragraphs_cache:
            node_md = load_source_node(source_slug) or ""
            source_paragraphs_cache[source_slug] = (
                extract_paragraphs_by_section(node_md) if node_md else {}
            )

        sections = source_paragraphs_cache[source_slug]
        paragraph_raw = None
        if source_section and source_section in sections:
            paragraph_raw = find_anchor_paragraph(
                sections[source_section], target_page, anchor_text
            )
        # Fallback: scan ALL sections
        if not paragraph_raw:
            for sect_paras in sections.values():
                paragraph_raw = find_anchor_paragraph(sect_paras, target_page, anchor_text)
                if paragraph_raw:
                    break

        evidence_paragraph = clean_paragraph(paragraph_raw) if paragraph_raw else ""
        out["evidence_paragraph"] = evidence_paragraph
        if not evidence_paragraph and "_python_prereject" not in out:
            out["_python_prereject"] = "evidence-paragraph-not-found"

        # F7: staging_verbs_present (only meaningful when evidence_paragraph present)
        out["staging_verbs_present"] = detect_staging_verbs(evidence_paragraph)

    # F5: valid_edge_types per target_type
    out["valid_edge_types"] = compute_valid_edge_types(
        target_type, type_contracts, canonical_vocab
    )

    return out


# ── Per-file processing ────────────────────────────────────────────────────
def enrich_file(
    in_path: Path,
    out_path: Path,
    node_type_index: dict[str, str],
    type_contracts: dict,
    canonical_vocab: set[str],
    apply: bool,
) -> dict:
    """Process one candidate file. Returns stats dict."""
    rows = []
    source_paragraphs_cache: dict[str, dict[str, list[str]]] = {}
    with open(in_path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"WARN: {in_path}: bad JSON: {e}", file=sys.stderr)

    enriched_rows = [
        enrich_row(
            r,
            node_type_index,
            type_contracts,
            canonical_vocab,
            source_paragraphs_cache,
        )
        for r in rows
    ]

    stats = {
        "input_rows": len(rows),
        "enriched_rows": len(enriched_rows),
        "target_resolved": sum(1 for r in enriched_rows if r.get("target_type")),
        "target_unresolved": sum(
            1 for r in enriched_rows if r.get("_python_prereject") == "target-slug-unresolved"
        ),
        "evidence_found": sum(
            1
            for r in enriched_rows
            if r.get("candidate_kind") == "source_target" and r.get("evidence_paragraph")
        ),
        "evidence_missing": sum(
            1
            for r in enriched_rows
            if r.get("_python_prereject") == "evidence-paragraph-not-found"
        ),
        "with_staging_verb": sum(
            1 for r in enriched_rows if r.get("staging_verbs_present")
        ),
    }

    if apply:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as fh:
            for r in enriched_rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    return stats


# ── Bucket walker ──────────────────────────────────────────────────────────
def walk_buckets(
    bucket_filter: str | None,
    apply: bool,
    verbose: bool,
    node_type_index: dict[str, str],
    type_contracts: dict,
    canonical_vocab: set[str],
) -> dict:
    totals = {
        "buckets_processed": 0,
        "files_processed": 0,
        "files_skipped": 0,
        "input_rows": 0,
        "enriched_rows": 0,
        "target_resolved": 0,
        "target_unresolved": 0,
        "evidence_found": 0,
        "evidence_missing": 0,
        "with_staging_verb": 0,
    }

    for bucket_dir in sorted(BUCKETS_DIR.iterdir()):
        if not bucket_dir.is_dir():
            continue
        if bucket_filter and bucket_dir.name != bucket_filter:
            continue
        src = bucket_dir / "prose-edge-candidates"
        if not src.is_dir():
            continue
        out_dir = bucket_dir / "prose-edge-candidates-enriched"

        files = sorted(src.glob("*.candidates.jsonl"))
        if not files:
            continue
        totals["buckets_processed"] += 1
        if verbose:
            print(f"\n[{bucket_dir.name}] {len(files)} file(s)")

        for in_path in files:
            out_path = out_dir / in_path.name
            stats = enrich_file(
                in_path, out_path, node_type_index, type_contracts, canonical_vocab, apply
            )
            totals["files_processed"] += 1
            for k in (
                "input_rows",
                "enriched_rows",
                "target_resolved",
                "target_unresolved",
                "evidence_found",
                "evidence_missing",
                "with_staging_verb",
            ):
                totals[k] += stats[k]
            if verbose:
                print(
                    f"  {in_path.name}: {stats['input_rows']} rows; "
                    f"resolved {stats['target_resolved']}, "
                    f"unresolved {stats['target_unresolved']}, "
                    f"evidence-found {stats['evidence_found']}/"
                    f"{stats['enriched_rows']}, "
                    f"staging-verb {stats['with_staging_verb']}"
                )

    return totals


# ── Main ───────────────────────────────────────────────────────────────────
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write enriched files (default: dry-run).")
    parser.add_argument("--bucket", help="Process only this bucket (default: all).")
    parser.add_argument("--verbose", "-v", action="store_true", help="Per-file logging.")
    args = parser.parse_args()

    t0 = time.perf_counter()
    print(f"Loading validator helpers...")
    validator = _load_validator()
    print(f"Loading node-type index from {NODES_DIR}...")
    node_type_index = validator.build_node_type_index(NODES_DIR)
    print(f"  {len(node_type_index)} slugs in node-type index")
    print(f"Loading canonical vocab from {ARCH_MD}...")
    canonical_vocab = validator.load_canonical_vocab(ARCH_MD)
    print(f"  {len(canonical_vocab)} canonical edge types")
    type_contracts = validator.TYPE_CONTRACTS
    print(f"  {len(type_contracts)} type-contract entries")
    print(f"Mode: {'APPLY (writing files)' if args.apply else 'DRY-RUN (no writes)'}")
    if args.bucket:
        print(f"Bucket filter: {args.bucket}")

    totals = walk_buckets(
        args.bucket,
        args.apply,
        args.verbose,
        node_type_index,
        type_contracts,
        canonical_vocab,
    )

    elapsed = time.perf_counter() - t0
    print(f"\n{'=' * 60}")
    print(f"ENRICHMENT {'APPLIED' if args.apply else 'DRY-RUN'} — {elapsed:.1f}s")
    print(f"{'=' * 60}")
    print(f"  Buckets processed:       {totals['buckets_processed']}")
    print(f"  Files processed:         {totals['files_processed']}")
    print(f"  Input rows:              {totals['input_rows']}")
    print(f"  Target resolved:         {totals['target_resolved']}  "
          f"({100*totals['target_resolved']/max(totals['input_rows'],1):.1f}%)")
    print(f"  Target unresolved:       {totals['target_unresolved']}  "
          f"({100*totals['target_unresolved']/max(totals['input_rows'],1):.1f}%)")
    print(f"  Source_target candidates with evidence_paragraph: "
          f"{totals['evidence_found']}")
    print(f"  Evidence missing (could not locate paragraph):    "
          f"{totals['evidence_missing']}")
    print(f"  Rows with staging-verb present (ENCOUNTERS pre-gate hint): "
          f"{totals['with_staging_verb']}")
    if not args.apply:
        print(f"\n  Re-run with --apply to write enriched files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
