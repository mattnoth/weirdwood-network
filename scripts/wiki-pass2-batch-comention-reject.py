#!/usr/bin/env python3
"""
wiki-pass2-batch-comention-reject.py — Batch-classify co-mention candidates as reject_just_mention.

For a set of ACOK chapter co-mention candidate files, emits a decision JSONL
applying the default classification rule: almost all co-mention candidates are
temporal co-occurrences without a typed relationship, so they receive
decision=reject_just_mention with reason=temporal-cooccurrence-not-relational.

The emit_edge path is intentionally left as a manual override hook — the script
sets the bar very high and defaults to reject. All input candidates that lack
a clear typed relationship (LOCATED_AT, WIELDS, GIFTED_TO, etc.) become rejects.

Input:
  working/wiki/pass2-buckets/meta-chapters-acok/comention-candidates/
      a-clash-of-kings-chapter-{N}.candidates.jsonl

Output:
  working/wiki/pass2-buckets/meta-chapters-acok/prose-edges-haiku/
      a-clash-of-kings-chapter-{N}.comention-edges.jsonl

Usage:
  python3 scripts/wiki-pass2-batch-comention-reject.py --chapters 10 11 12 13
  python3 scripts/wiki-pass2-batch-comention-reject.py --chapters 10 11 12 13 --dry-run
"""

import argparse
import json
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
BUCKET_DIR = REPO_ROOT / "working" / "wiki" / "pass2-buckets" / "meta-chapters-acok"
CANDIDATES_DIR = BUCKET_DIR / "comention-candidates"
OUTPUT_DIR = BUCKET_DIR / "prose-edges-haiku"


# ---------------------------------------------------------------------------
# Classification helpers
# ---------------------------------------------------------------------------

def _reject_row(candidate: dict) -> dict:
    """Return a reject_just_mention decision row from a candidate."""
    return {
        "decision": "reject_just_mention",
        "candidate_kind": "comention",
        "pair_a": candidate["pair_a"],
        "pair_b": candidate["pair_b"],
        "evidence_chapter": candidate["evidence_chapter"],
        "reason": "temporal-cooccurrence-not-relational",
    }


def classify_candidate(candidate: dict) -> dict:
    """
    Classify a single co-mention candidate.

    Default: reject_just_mention. The emit_edge path is intentionally narrow —
    co-mention candidates rarely establish a typed relationship; narrative
    co-occurrence is not a relationship edge. Only return emit_edge when the
    evidence snippet unambiguously establishes a specific edge type
    (LOCATED_AT for a contained-in relationship, WIELDS for an artifact holder,
    GIFTED_TO / INHERITED_BY for explicit transfers, etc.).

    For this batch (chapters 10-13), all candidates are rejected by default.
    Add per-pair overrides above this function if manual review identifies
    genuine emit_edge cases.
    """
    return _reject_row(candidate)


# ---------------------------------------------------------------------------
# Per-chapter processing
# ---------------------------------------------------------------------------

def process_chapter(chapter_num: int, dry_run: bool) -> dict:
    """
    Read candidates for one chapter, classify each, write output.

    Returns a summary dict: {chapter_num, input_path, output_path,
    total, emit_edge, reject_just_mention, written}.
    """
    chapter_slug = f"a-clash-of-kings-chapter-{chapter_num}"
    input_path = CANDIDATES_DIR / f"{chapter_slug}.candidates.jsonl"
    output_path = OUTPUT_DIR / f"{chapter_slug}.comention-edges.jsonl"

    if not input_path.exists():
        print(f"[WARN] Input file not found: {input_path}", file=sys.stderr)
        return {
            "chapter_num": chapter_num,
            "input_path": str(input_path),
            "output_path": str(output_path),
            "total": 0,
            "emit_edge": 0,
            "reject_just_mention": 0,
            "written": False,
            "error": "input file not found",
        }

    # Read all candidates
    candidates = []
    with input_path.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                candidates.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(
                    f"[WARN] {input_path.name} line {lineno}: JSON parse error: {exc}",
                    file=sys.stderr,
                )

    # Classify each candidate
    decisions = [classify_candidate(c) for c in candidates]

    emit_count = sum(1 for d in decisions if d["decision"] == "emit_edge")
    reject_count = sum(1 for d in decisions if d["decision"] == "reject_just_mention")
    other_count = len(decisions) - emit_count - reject_count

    if other_count:
        print(
            f"[WARN] {chapter_slug}: {other_count} decisions have unexpected decision values",
            file=sys.stderr,
        )

    # Write output (skip in dry-run)
    written = False
    if not dry_run:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as fh:
            for row in decisions:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        written = True

    return {
        "chapter_num": chapter_num,
        "input_path": str(input_path),
        "output_path": str(output_path),
        "total": len(decisions),
        "emit_edge": emit_count,
        "reject_just_mention": reject_count,
        "written": written,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Batch-classify ACOK co-mention candidates as reject_just_mention. "
            "Reads .candidates.jsonl files, emits .comention-edges.jsonl outputs."
        )
    )
    parser.add_argument(
        "--chapters",
        nargs="+",
        type=int,
        required=True,
        metavar="N",
        help="Chapter numbers to process (e.g. --chapters 10 11 12 13)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Read and classify but do not write any output files",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    mode_label = "DRY RUN — " if args.dry_run else ""
    print(f"{mode_label}Processing {len(args.chapters)} chapter(s): {args.chapters}")
    print()

    summaries = []
    total_emit = 0
    total_reject = 0
    total_candidates = 0
    errors = 0

    for chapter_num in sorted(args.chapters):
        result = process_chapter(chapter_num, dry_run=args.dry_run)
        summaries.append(result)

        if "error" in result:
            print(
                f"[error] chapter-{chapter_num}: {result['error']}"
            )
            errors += 1
            continue

        total_candidates += result["total"]
        total_emit += result["emit_edge"]
        total_reject += result["reject_just_mention"]

        input_name = Path(result["input_path"]).name
        output_path = result["output_path"]
        status = "wrote" if result["written"] else "dry-run"
        print(
            f"[done] {input_name} -> "
            f"{result['emit_edge']} emit_edge, {result['reject_just_mention']} reject_just_mention "
            f"-- {status} {output_path}"
        )

    # Summary table
    print()
    print("=" * 72)
    print(f"  Chapters processed : {len(args.chapters) - errors}  ({errors} error(s))")
    print(f"  Total candidates   : {total_candidates}")
    print(f"  emit_edge          : {total_emit}")
    print(f"  reject_just_mention: {total_reject}")
    if args.dry_run:
        print("  Output files       : NOT written (dry-run)")
    else:
        print(f"  Output directory   : {OUTPUT_DIR}")
    print("=" * 72)


if __name__ == "__main__":
    main()
