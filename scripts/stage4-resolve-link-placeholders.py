#!/usr/bin/env python3
"""
stage4-resolve-link-placeholders.py — Substitute [LINK] placeholders in candidate snippets

Background
----------
The cross-reference builder (scripts/wiki-pass2-build-cross-refs.py) generates snippets
where the target wikilink itself is replaced with the literal token `[LINK]`, while the
link's display text is stored separately in `anchor_text`.  For example:

  snippet:    "Ser [LINK] captured Jaime at the Whispering Wood."
  anchor_text: "Brynden Tully"

The prose-edge-classifier has to mentally substitute `anchor_text` back into the snippet
to read the prose naturally.  This script burns the substitution into the candidate files
before classification, so the classifier sees:

  snippet:    "Ser «Brynden Tully» captured Jaime at the Whispering Wood."

Substitution marker
-------------------
`[LINK]` is replaced with `«anchor_text»` (angle quotes).  Plain brackets `[...]` are
already used extensively for OTHER wiki links in the same snippet (e.g.
`[Jaime](wiki:Jaime_Lannister)`), so using angle quotes prevents the classifier from
confusing the resolved target with an adjacent wikilink.  JSON encoding of `«»` is safe
(they are multi-byte UTF-8 but valid in JSON strings with ensure_ascii=False).

Scope
-----
- **Only processes queued candidate files** — buckets that have a `prose-edge-candidates/`
  directory but no completed `prose-edges/*.edges.jsonl` output.
- **Does NOT touch** completed batches (the 21-batch Sonnet freeform control arm).
- **Idempotent** — if a snippet already has no `[LINK]` token (either already substituted
  or the snippet was None), the row is written back unchanged.
- **--plan mode** (default) prints a summary without writing anything.
- **--apply mode** rewrites candidate files atomically (write to .tmp then rename).

Usage
-----
  python3 scripts/stage4-resolve-link-placeholders.py          # plan (dry-run)
  python3 scripts/stage4-resolve-link-placeholders.py --apply  # rewrite queued candidates
  python3 scripts/stage4-resolve-link-placeholders.py --apply --bucket characters-house-stark

Contract
--------
Input JSONL row (all candidate rows):
  {"candidate_kind": "source_target", "source_slug": "...", "snippet": "...Ser [LINK]...",
   "anchor_text": "Brynden Tully", ...}

Output JSONL row (after substitution):
  {"candidate_kind": "source_target", "source_slug": "...", "snippet": "...Ser «Brynden Tully»...",
   "anchor_text": "Brynden Tully", ...}

The `anchor_text` field is preserved unchanged so callers that want the raw text still have it.
"""

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
PASS2_BUCKETS_DIR = REPO_ROOT / "working" / "wiki" / "pass2-buckets"

LINK_TOKEN = "[LINK]"
OPEN_MARK = "«"   # «
CLOSE_MARK = "»"  # »


def format_resolved(anchor_text: str) -> str:
    """Wrap anchor_text in angle-quote markers."""
    return f"{OPEN_MARK}{anchor_text}{CLOSE_MARK}"


def substitute_snippet(snippet: str, anchor_text: str) -> str:
    """Replace the [LINK] token in snippet with «anchor_text».

    Returns the original snippet unchanged if [LINK] is not present.
    """
    if not snippet or LINK_TOKEN not in snippet:
        return snippet
    # Replace only the first occurrence — each snippet has exactly one [LINK]
    return snippet.replace(LINK_TOKEN, format_resolved(anchor_text), 1)


def is_bucket_queued(bucket_dir: Path) -> bool:
    """Return True if this bucket has candidates but no completed prose-edges."""
    cands_dir = bucket_dir / "prose-edge-candidates"
    if not cands_dir.exists():
        return False
    edges_dir = bucket_dir / "prose-edges"
    if not edges_dir.exists():
        return True
    # Has edges dir — check if any .edges.jsonl files exist
    return not any(edges_dir.glob("*.edges.jsonl"))


def process_candidate_file(
    cand_file: Path,
    write_output: bool,
) -> dict:
    """Process one candidate JSONL file.

    Returns a stats dict: {rows_total, rows_substituted, rows_skipped, rows_error}.
    """
    stats = {"rows_total": 0, "rows_substituted": 0, "rows_skipped": 0, "rows_error": 0}

    lines_out: list[str] = []
    changed = False

    try:
        raw_text = cand_file.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"  WARNING: Cannot read {cand_file}: {exc}", file=sys.stderr)
        stats["rows_error"] += 1
        return stats

    for raw_line in raw_text.splitlines():
        raw_line_stripped = raw_line.strip()
        if not raw_line_stripped:
            lines_out.append("")
            continue

        stats["rows_total"] += 1
        try:
            row = json.loads(raw_line_stripped)
        except json.JSONDecodeError as exc:
            print(f"  WARNING: Malformed JSON in {cand_file}: {exc}", file=sys.stderr)
            lines_out.append(raw_line_stripped)
            stats["rows_error"] += 1
            continue

        snippet = row.get("snippet")
        anchor_text = row.get("anchor_text", "")

        if snippet and LINK_TOKEN in snippet:
            if anchor_text:
                row["snippet"] = substitute_snippet(snippet, anchor_text)
                stats["rows_substituted"] += 1
                changed = True
            else:
                # anchor_text is missing — leave [LINK] in place, log warning
                print(
                    f"  WARNING: [LINK] in snippet but no anchor_text — "
                    f"{cand_file.name}: {row.get('source_slug','?')} -> {row.get('target_slug','?')}",
                    file=sys.stderr,
                )
                stats["rows_skipped"] += 1
        else:
            stats["rows_skipped"] += 1

        lines_out.append(json.dumps(row, ensure_ascii=False))

    if write_output and changed:
        # Atomic write: tmp file then rename
        tmp_file = cand_file.with_suffix(".tmp")
        try:
            tmp_file.write_text("\n".join(lines_out) + "\n", encoding="utf-8")
            tmp_file.rename(cand_file)
        except OSError as exc:
            print(f"  ERROR: Cannot write {cand_file}: {exc}", file=sys.stderr)
            stats["rows_error"] += 1
            # Clean up tmp if it exists
            if tmp_file.exists():
                tmp_file.unlink(missing_ok=True)

    return stats


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Substitute [LINK] placeholders in prose-edge-candidate snippets "
            "with the actual anchor_text, wrapped in «angle quotes»."
        )
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--plan",
        action="store_true",
        default=True,
        help="Dry-run: scan and print stats without writing (default).",
    )
    mode_group.add_argument(
        "--apply",
        action="store_true",
        help="Rewrite queued candidate files with [LINK] substituted.",
    )
    parser.add_argument(
        "--bucket",
        metavar="BUCKET_ID",
        default=None,
        help="Process only this specific bucket (e.g. 'characters-house-stark').",
    )
    args = parser.parse_args()
    write_output = args.apply

    # -----------------------------------------------------------------------
    # Discover queued buckets
    # -----------------------------------------------------------------------
    if args.bucket:
        bucket_dirs = [PASS2_BUCKETS_DIR / args.bucket]
        for bd in bucket_dirs:
            if not bd.is_dir():
                print(f"ERROR: Bucket directory not found: {bd}", file=sys.stderr)
                sys.exit(1)
    else:
        bucket_dirs = sorted(
            d for d in PASS2_BUCKETS_DIR.iterdir()
            if d.is_dir() and not d.name.startswith("_")
        )

    queued_buckets: list[Path] = []
    skipped_completed = 0
    for bd in bucket_dirs:
        if is_bucket_queued(bd):
            queued_buckets.append(bd)
        else:
            skipped_completed += 1

    print(f"Buckets found:          {len(bucket_dirs)}")
    print(f"  Queued (no edges):    {len(queued_buckets)}")
    print(f"  Completed (skipped):  {skipped_completed}")
    print()

    # -----------------------------------------------------------------------
    # Process candidate files
    # -----------------------------------------------------------------------
    total_files = 0
    total_rows = 0
    total_substituted = 0
    total_skipped = 0
    total_errors = 0

    for bd in queued_buckets:
        cands_dir = bd / "prose-edge-candidates"
        for cand_file in sorted(cands_dir.glob("*.candidates.jsonl")):
            stats = process_candidate_file(cand_file, write_output)
            total_files += 1
            total_rows += stats["rows_total"]
            total_substituted += stats["rows_substituted"]
            total_skipped += stats["rows_skipped"]
            total_errors += stats["rows_error"]

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    mode_label = "APPLY" if write_output else "PLAN (dry-run)"
    print("=" * 60)
    print(f"stage4-resolve-link-placeholders — {mode_label}")
    print("=" * 60)
    print(f"  Candidate files processed:    {total_files:>8,}")
    print(f"  Candidate rows read:          {total_rows:>8,}")
    print(f"  Rows with [LINK] substituted: {total_substituted:>8,}")
    print(f"  Rows unchanged (no [LINK]):   {total_skipped:>8,}")
    if total_errors:
        print(f"  Errors / warnings:            {total_errors:>8,}")
    print()
    if write_output:
        print(f"Done. {total_substituted:,} [LINK] placeholders resolved across {total_files:,} files.")
        print(f"Substitution pattern: [LINK] → «anchor_text»")
    else:
        print("Plan mode — nothing written. Re-run with --apply to rewrite candidate files.")
        if total_substituted > 0:
            print(f"  Would substitute {total_substituted:,} [LINK] tokens in {total_files:,} files.")


if __name__ == "__main__":
    main()
