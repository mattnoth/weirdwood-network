#!/usr/bin/env python3
"""stage4-fresh-relocate-sample.py — Stratified fresh-sample re-location harness.

Draws a fresh stratified sample from the untyped _extra-tables candidate pool,
re-locates each row with the improved locator (v2), and writes classifier-ready
*.extra-tables.jsonl files per book so the tail-classifier's --input-dir reader
can consume them directly.

Key differences from stage4-relocate-smoke.py:
  - Source pool: working/wiki/pass2-buckets/pass1-derived/_extra-tables/
    (the full untyped candidate pool), NOT the smoke3 haiku run output.
  - Sample: stratified by book + candidate_kind, seed-controlled.
  - Output filename pattern: {book}.extra-tables.jsonl  (glob *.extra-tables.jsonl)
  - edge_type is intentionally absent (unset) so the classifier treats every row
    as a fresh untyped candidate.
  - _row_id is a stable string "{book}:{source_slug}:{target_slug}:{chapter}" to
    enable join-back without integer collision with the smoke3 row-id space.

Usage:
    python3 scripts/stage4-fresh-relocate-sample.py [options]

    --kinds           Comma-separated candidate_kind filter
                      (default: pass1_events,pass1_dialogue)
    --sample-n N      Total rows to sample  (default: 400)
    --seed S          RNG seed              (default: 4242)
    --output-dir DIR  Output root           (default: working/wiki/pass2-buckets/
                                             pass1-derived/_fresh-relocate-{seed}/)
    --dry-run         Print stats but write no files.
    --input-dir DIR   Override the _extra-tables source dir.
                      (default: working/wiki/pass2-buckets/pass1-derived/_extra-tables)

No LLM calls. No network. Deterministic given the same seed.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Repo root + module loading
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
EXTRA_TABLES_DIR = (
    REPO / "working" / "wiki" / "pass2-buckets" / "pass1-derived" / "_extra-tables"
)
CHAPTERS_DIR = REPO / "sources" / "chapters"
BOOKS = ["agot", "acok", "asos", "affc", "adwd"]
PRODUCED_AT = datetime.now(timezone.utc).isoformat(timespec="seconds")

DEFAULT_KINDS = "pass1_events,pass1_dialogue"
DEFAULT_SAMPLE_N = 400
DEFAULT_SEED = 4242


def _load_module(filename: str, mod_name: str):
    path = REPO / "scripts" / filename
    if not path.exists():
        sys.exit(f"ERROR: Required module not found: {path}")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


# Load the improved locator and relevance filter (same as relocate-smoke uses)
locator = _load_module("stage4-pass1-evidence-locator.py", "stage4_pass1_evidence_locator")
qrf = _load_module("stage4-quote-relevance-filter.py", "stage4_quote_relevance_filter")

# Load the classifier's stratified_sample + load_extra_tables_rows (single source of truth)
tc = _load_module("stage4-tail-classifier.py", "stage4_tail_classifier")
stratified_sample = tc.stratified_sample
load_extra_tables_rows = tc.load_extra_tables_rows


# ---------------------------------------------------------------------------
# Build stable _row_id from content (avoids collision with smoke3 integer IDs)
# ---------------------------------------------------------------------------

def make_row_id(row: dict) -> str:
    """Stable string row ID: '{book}:{source_slug}:{target_slug}:{chapter}'.

    This is intentionally different from the smoke3 integer row-id space so
    there is no ambiguity when the classifier processes both pools.
    """
    book = row.get("_tail_book") or row.get("evidence_book", "")
    src = row.get("source_slug", "")
    tgt = row.get("target_slug", "")
    chap = row.get("evidence_chapter", "")
    return f"{book}:{src}:{tgt}:{chap}"


# ---------------------------------------------------------------------------
# Build alias-aware token index
# ---------------------------------------------------------------------------

def build_token_index_for_rows(rows: list[dict]) -> tuple[dict, frozenset]:
    """Build alias-aware slug token index for all slugs in rows."""
    stoplist = qrf.build_stoplist()
    all_slugs = list(
        {r.get("source_slug", "") for r in rows} |
        {r.get("target_slug", "") for r in rows}
    )
    all_slugs = [s for s in all_slugs if s]
    idx = qrf.build_slug_token_index(slugs=all_slugs, stoplist=stoplist)
    return idx, stoplist


# ---------------------------------------------------------------------------
# Re-locate a single candidate row (same logic as stage4-relocate-smoke.py)
# ---------------------------------------------------------------------------

def relocate_row(row: dict, slug_token_index: dict, stoplist: frozenset) -> dict:
    """Run the improved locate_evidence on one candidate row.

    Returns loc dict: {evidence_quote, evidence_ref, locate_status, locate_quality}.
    """
    src = row.get("source_slug", "")
    tgt = row.get("target_slug", "")
    chapter = row.get("evidence_chapter", "")

    # Pre-seed the module-level cache so locate_evidence uses the pre-built index
    if src in slug_token_index:
        locator._CACHED_TOKEN_INDEX[src] = slug_token_index[src]
    if tgt in slug_token_index:
        locator._CACHED_TOKEN_INDEX[tgt] = slug_token_index[tgt]

    if not chapter:
        return {
            "evidence_quote": row.get("evidence_quote", ""),
            "evidence_ref": "",
            "locate_status": "chapter-level",
            "locate_quality": "chapter-level",
        }

    book = chapter.split("-")[0] if "-" in chapter else row.get("_tail_book", "")
    chapter_path = CHAPTERS_DIR / book / f"{chapter}.md"

    candidate = {
        "source_slug": src,
        "target_slug": tgt,
        "hint_raw": row.get("hint_raw", ""),
        "evidence_text": "",
        "evidence_chapter": chapter,
        "evidence_book": book,
    }

    loc = locator.locate_evidence(candidate, chapter_path)
    return loc


# ---------------------------------------------------------------------------
# Build classifier-ready output row
# ---------------------------------------------------------------------------

def build_output_row(row: dict, loc: dict) -> dict:
    """Build a classifier-ready row from a candidate + improved location.

    Mirrors stage4-tail-classifier.py's expected input schema.
    edge_type is intentionally omitted (not set) so load_extra_tables_rows
    treats the row as untyped and includes it.
    """
    chapter = row.get("evidence_chapter", "")
    book = chapter.split("-")[0] if "-" in chapter else row.get("_tail_book", "")

    return {
        "decision": "needs_type",
        "candidate_kind": row.get("candidate_kind", "pass1_events"),
        "source_slug": row.get("source_slug", ""),
        "source_resolution_status": row.get("source_resolution_status", "scan"),
        "target_slug": row.get("target_slug", ""),
        "target_resolution_status": row.get("target_resolution_status", "scan"),
        "evidence_kind": row.get("evidence_kind", "book-pass1"),
        "evidence_book": book,
        "evidence_chapter": chapter,
        "evidence_section": row.get("source_section", row.get("evidence_section", "")),
        "evidence_quote": loc["evidence_quote"],
        "evidence_ref": loc["evidence_ref"],
        "hint_raw": row.get("hint_raw", ""),
        "corroborates_known_edge": row.get("corroborates_known_edge", False),
        "wiki_edge_type": row.get("wiki_edge_type"),
        "locate_status": loc["locate_status"],
        "locate_quality": loc.get("locate_quality", "chapter-level"),
        "run_id": "fresh-relocate-v2",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "_row_id": make_row_id(row),
        "_orig_evidence_quote": row.get("evidence_quote", ""),
        # edge_type intentionally NOT set (classifier reads edge_type==null as untyped)
    }


# ---------------------------------------------------------------------------
# Overlap check with _relocate-smoke
# ---------------------------------------------------------------------------

def compute_overlap_with_smoke(
    sample_rows: list[dict],
    relocate_smoke_dir: Path,
) -> int:
    """Count how many sample rows have the same (source, target, chapter) triple
    as a row in the existing _relocate-smoke output.

    The _relocate-smoke rows come from a different source (smoke3 haiku run),
    but we compare on the shared (source_slug, target_slug, evidence_chapter)
    triple to measure true semantic overlap.
    """
    smoke_triples: set[tuple[str, str, str]] = set()
    for book in BOOKS:
        for jsonl in sorted((relocate_smoke_dir / book).glob("*.jsonl")) if (relocate_smoke_dir / book).exists() else []:
            for line in jsonl.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                    triple = (
                        r.get("source_slug", ""),
                        r.get("target_slug", ""),
                        r.get("evidence_chapter", ""),
                    )
                    smoke_triples.add(triple)
                except json.JSONDecodeError:
                    continue

    overlap = 0
    for row in sample_rows:
        triple = (
            row.get("source_slug", ""),
            row.get("target_slug", ""),
            row.get("evidence_chapter", ""),
        )
        if triple in smoke_triples:
            overlap += 1
    return overlap


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Stratified fresh-sample re-location harness. "
            "Samples from _extra-tables untyped candidates, re-locates with "
            "locator-v2, writes classifier-ready *.extra-tables.jsonl per book."
        )
    )
    parser.add_argument(
        "--kinds",
        default=DEFAULT_KINDS,
        help=f"Comma-separated candidate_kind filter (default: {DEFAULT_KINDS})",
    )
    parser.add_argument(
        "--sample-n",
        type=int,
        default=DEFAULT_SAMPLE_N,
        metavar="N",
        help=f"Total rows to sample (default: {DEFAULT_SAMPLE_N})",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        metavar="S",
        help=f"RNG seed (default: {DEFAULT_SEED})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        metavar="DIR",
        help=(
            "Output root directory. Defaults to "
            "working/wiki/pass2-buckets/pass1-derived/_fresh-relocate-{seed}/"
        ),
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=EXTRA_TABLES_DIR,
        metavar="DIR",
        help=f"Source _extra-tables directory (default: {EXTRA_TABLES_DIR})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print stats but write no files.",
    )
    args = parser.parse_args()

    # Resolve output dir: default is _fresh-relocate-{seed}/
    if args.output_dir is None:
        out_base = (
            REPO
            / "working"
            / "wiki"
            / "pass2-buckets"
            / "pass1-derived"
            / f"_fresh-relocate-{args.seed}"
        )
    else:
        out_base = args.output_dir

    kinds = [k.strip() for k in args.kinds.split(",") if k.strip()]
    write_output = not args.dry_run

    print(f"Loading untyped candidates from: {args.input_dir}")
    print(f"  kinds filter: {kinds}")
    all_rows = load_extra_tables_rows(
        input_dir=args.input_dir,
        books=BOOKS,
        candidate_kinds=kinds,
    )
    print(f"  {len(all_rows)} untyped candidate rows loaded")

    if not all_rows:
        print("ERROR: No rows loaded — check --input-dir and --kinds.", file=sys.stderr)
        sys.exit(1)

    print(f"\nStratified sampling: n={args.sample_n}, seed={args.seed}")
    sample = stratified_sample(
        rows=all_rows,
        n=args.sample_n,
        strat_keys=("_tail_book", "candidate_kind"),
        seed=args.seed,
    )
    print(f"  Sample size: {len(sample)} rows")

    # Per-book + per-kind breakdown
    sample_counts: Counter = Counter()
    for row in sample:
        sample_counts[(row.get("_tail_book", "?"), row.get("candidate_kind", "?"))] += 1

    print("\n  Per-book / per-kind breakdown:")
    for (book, kind), count in sorted(sample_counts.items()):
        print(f"    {book:<6}  {kind:<22}  {count:>4}")

    # Overlap check with _relocate-smoke
    relocate_smoke_dir = (
        REPO / "working" / "wiki" / "pass2-buckets" / "pass1-derived" / "_relocate-smoke"
    )
    overlap = compute_overlap_with_smoke(sample, relocate_smoke_dir)
    print(f"\n  Overlap with _relocate-smoke (same source/target/chapter triple): {overlap}")
    if len(sample) > 0:
        print(f"  ({100.0 * overlap / len(sample):.1f}% of sample)")

    # Build token index for all sampled slugs
    print("\nBuilding alias-aware token index for sampled slugs…")
    slug_token_index, stoplist = build_token_index_for_rows(sample)
    print(f"  Index covers {len(slug_token_index)} slugs")

    # Pre-seed the locator module-level cache
    locator._CACHED_TOKEN_INDEX.update(slug_token_index)
    locator._CACHED_STOPLIST = stoplist

    # Re-locate each sampled row
    print("Re-locating rows with locator-v2…")
    output_rows: list[dict] = []
    quality_counts: Counter = Counter()

    for row in sample:
        loc = relocate_row(row, slug_token_index, stoplist)
        out_row = build_output_row(row, loc)
        output_rows.append(out_row)
        quality_counts[loc.get("locate_quality", "chapter-level")] += 1

    print(f"  Done. {len(output_rows)} rows processed.")

    # locate_quality distribution
    print("\n--- locate_quality distribution ---")
    total = len(output_rows)
    for q in ["both-named", "one-named", "nearest-fallback", "chapter-level"]:
        n = quality_counts.get(q, 0)
        pct = 100.0 * n / total if total else 0.0
        print(f"  {q:<22}  {n:>4}  ({pct:.1f}%)")

    # Write outputs
    if write_output:
        rows_by_book: dict[str, list[dict]] = {b: [] for b in BOOKS}
        for out_row in output_rows:
            book = out_row.get("evidence_book", "")
            if book in rows_by_book:
                rows_by_book[book].append(out_row)
            else:
                rows_by_book.setdefault(book, []).append(out_row)

        total_written = 0
        for book, book_rows in rows_by_book.items():
            if not book_rows:
                continue
            out_dir = out_base / book
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f"{book}.extra-tables.jsonl"
            with out_file.open("w", encoding="utf-8") as fh:
                for r in book_rows:
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            print(f"  Written {len(book_rows):>4} rows → {out_file}")
            total_written += len(book_rows)

        print(f"\nTotal written: {total_written} rows")
        print(f"Output dir:   {out_base}")
        print(f"\nClassifier --input-dir: {out_base}")
    else:
        print("\nDry-run mode — no files written.")
        print(f"Would write to: {out_base}")


if __name__ == "__main__":
    main()
