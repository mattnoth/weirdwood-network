#!/usr/bin/env python3
"""stage4-reground-core-citations.py — Deterministic citation re-grounding pass.

The shipped core edge layer (graph/edges/edges.jsonl) has a line-number bug:
almost all evidence_ref values end in ':11' (the chapter's first prose line),
but the evidence_quote TEXT is correct and lives elsewhere in the file.

This script re-grounds every edge by finding the TRUE 1-based file line where
the existing evidence_quote appears, and rewrites ONLY the line suffix of
evidence_ref.  No LLM.  No network.  Read-only on sources/.

Algorithm per edge:
  1. If evidence_quote is empty, starts with [PARAPHRASE], or evidence_ref has
     no ':' separator → leave UNCHANGED, count as skipped-no-quote.
  2. Extract chapter path = part of evidence_ref before ':' (already correct).
  3. Normalize for matching: collapse whitespace, unify curly/straight quotes
     and apostrophes, lowercase.  Take the HEAD (first HEAD_CHARS chars of the
     normalized quote, or the full quote if shorter).
  4. Find the FIRST 1-based file line whose normalized content contains the
     normalized quote-head.  If HEAD_CHARS applies and head is shorter than
     SHORT_HEAD_THRESHOLD, require a full-quote match instead.
  5. Found → rewrite evidence_ref to {same_path}:{true_line}.
     Not found → leave UNCHANGED, record in unresolved list.

Safety contract (asserted before writing):
  - ONLY evidence_ref may change on any row.
  - All other fields are byte-identical.
  - Output row count == input row count (3,811 in → 3,811 out).

Outputs (written only with --apply):
  graph/edges/_regrounding/edges-regrounded-candidate.jsonl
  graph/edges/_regrounding/regrounding-report.md

Usage:
  python3 scripts/stage4-reground-core-citations.py          # dry-run (plan)
  python3 scripts/stage4-reground-core-citations.py --apply  # write outputs
  python3 scripts/stage4-reground-core-citations.py --apply --edges-file PATH

$0, no LLM.  Read-only on sources/.  Delete nothing.
"""

import argparse
import copy
import json
import re
import sys
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
EDGES_IN = REPO_ROOT / "graph" / "edges" / "edges.jsonl"
REGROUNDING_DIR = REPO_ROOT / "graph" / "edges" / "_regrounding"
EDGES_OUT = REGROUNDING_DIR / "edges-regrounded-candidate.jsonl"
REPORT_OUT = REGROUNDING_DIR / "regrounding-report.md"
CHAPTERS_DIR = REPO_ROOT / "sources" / "chapters"

# Matching parameters
HEAD_CHARS = 40          # chars from the normalized quote used as the search head
SHORT_HEAD_THRESHOLD = 15  # if head is shorter than this, require full-quote match


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------
_QUOTE_NORM_TABLE = str.maketrans({
    "“": '"',   # LEFT DOUBLE QUOTATION MARK
    "”": '"',   # RIGHT DOUBLE QUOTATION MARK
    "‘": "'",   # LEFT SINGLE QUOTATION MARK
    "’": "'",   # RIGHT SINGLE QUOTATION MARK / apostrophe
    "′": "'",   # PRIME
    "″": '"',   # DOUBLE PRIME
    "«": '"',   # LEFT-POINTING DOUBLE ANGLE QUOTATION
    "»": '"',   # RIGHT-POINTING DOUBLE ANGLE QUOTATION
    "—": "-",   # EM DASH
    "–": "-",   # EN DASH
    " ": " ",   # NON-BREAKING SPACE
    "…": "...", # HORIZONTAL ELLIPSIS
})


def normalize(text: str) -> str:
    """Normalize text for matching: translate quote glyphs, collapse whitespace,
    strip, lowercase."""
    text = text.translate(_QUOTE_NORM_TABLE)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


# ---------------------------------------------------------------------------
# Chapter file reader (returns all lines with 1-based line numbers)
# ---------------------------------------------------------------------------
def read_chapter_lines(chapter_path: Path) -> list[tuple[int, str]]:
    """Read a chapter file and return all lines as (1-based-lineno, raw_text).

    Does NOT skip frontmatter — we use raw 1-based line numbers matching the
    actual file, so any citation lineno refers to the physical file line.
    """
    try:
        raw = chapter_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"  WARNING: Cannot read {chapter_path}: {exc}", file=sys.stderr)
        return []
    return [(i + 1, line) for i, line in enumerate(raw.splitlines())]


# ---------------------------------------------------------------------------
# Core search function
# ---------------------------------------------------------------------------
def _candidate_search_strings(norm_quote: str) -> list[str]:
    """Generate candidate search strings from a normalized quote, in priority order.

    The evidence locator sometimes assembles a quote that spans two physical file
    lines (e.g. a dialogue line ending with !" or ?" followed by narration on the
    next line).  The 40-char head may therefore cross the line boundary and fail
    to match any single line.

    We generate multiple search strings:
    1. Full 40-char head (exact HEAD_CHARS).
    2. Head truncated at the last dialogue-ending marker before HEAD_CHARS:
       the rightmost `!"`, `?"`, or `."` within the head — this recovers the
       portion that fits on a single line.
    3. Head truncated at the last `" "` (end-of-line join pattern) — the first
       sentence of a multi-sentence joined quote.
    4. For very short quotes (< SHORT_HEAD_THRESHOLD), the full quote itself.

    Returns a deduplicated list of strings (length >= SHORT_HEAD_THRESHOLD) in
    priority order (longest / most specific first).
    """
    if len(norm_quote) < SHORT_HEAD_THRESHOLD:
        return [norm_quote]

    candidates: list[str] = []

    head = norm_quote[:HEAD_CHARS]
    candidates.append(head)  # priority 1: full head

    # Priority 2: truncate at last !" or ?" or ." within head
    for marker in ('!"', '?"', '."', '!"'):
        idx = head.rfind(marker)
        if idx >= SHORT_HEAD_THRESHOLD:
            trunc = head[:idx + len(marker)]
            candidates.append(trunc)
            break  # take the first (rightmost) hit

    # Priority 3a: first sentence of a multi-sentence joined quote (" " split)
    join_idx = norm_quote.find('" "')
    if join_idx >= SHORT_HEAD_THRESHOLD:
        first_sent = norm_quote[:join_idx + 1]  # include the closing "
        candidates.append(first_sent[:HEAD_CHARS])

    # Priority 3b: if first sentence is SHORT (< SHORT_HEAD_THRESHOLD), try
    # anchoring to the SECOND sentence (the part after the '" "' join).
    # This handles quotes like '"I know it." "You Starks are hard to kill," Jon agreed.'
    # where the second sentence is on a separate physical line.
    if join_idx >= 0:
        second_part = norm_quote[join_idx + 3:]  # skip '" "'
        if len(second_part) >= SHORT_HEAD_THRESHOLD:
            candidates.append(second_part[:HEAD_CHARS])

    # (Priority 4 short-fragment case is handled in find_quote_line's
    # two-part proximity search — not via candidates list, to avoid false positives.)

    # Deduplicate while preserving order
    seen: set[str] = set()
    result: list[str] = []
    for c in candidates:
        if c and len(c) >= SHORT_HEAD_THRESHOLD and c not in seen:
            seen.add(c)
            result.append(c)
    return result


def find_quote_line(quote: str, chapter_path: Path) -> int | None:
    """Find the 1-based line number in chapter_path where quote appears.

    Uses normalized substring match on each line.  Returns the FIRST matching
    line number, or None if not found.

    Strategy:
    1. Generate multiple candidate search strings (full head, truncated at
       dialogue-end markers, first sentence of joined quote) via
       _candidate_search_strings().
    2. For each candidate (in priority order), scan every file line for a
       substring match.  Return the line number on first hit.
    3. Two-part proximity search: for quotes that join two short dialogue
       lines (e.g. '"Nymeria!" The direwolf...'), the joining cross-line
       boundary may defeat every HEAD_CHARS-based candidate.  If all
       candidates fail and the quote contains '" "' or ends a short
       utterance with !" / ?" / .", extract the part BEFORE and AFTER the
       join and verify they appear within PROXIMITY_LINES of each other.
       Return the lineno of whichever part appears first.
    4. Return None if all strategies fail.

    Lines are searched in order; first match wins.
    """
    PROXIMITY_LINES = 5  # max gap between the two parts of a joined quote

    norm_quote = normalize(quote)
    if not norm_quote:
        return None

    candidates = _candidate_search_strings(norm_quote)
    lines = read_chapter_lines(chapter_path)
    lineno_list = [lineno for lineno, _ in lines]
    norm_lines = [(lineno, normalize(raw)) for lineno, raw in lines]

    # Pass 1: candidate-list search
    for search_str in candidates:
        for lineno, norm_line in norm_lines:
            if search_str in norm_line:
                return lineno

    # Pass 2: two-part proximity search for short-fragment joined quotes.
    # Extract part-A (everything up to and including the first dialogue-end
    # marker !" / ?" / .") and part-B (the text after the join).
    # Accept if part-A appears on line X and part-B appears within
    # PROXIMITY_LINES of X.
    # part-B is tried at multiple lengths (HEAD_CHARS, then truncated at its
    # own first dialogue-end marker, then a short 15-char minimum) to handle
    # cases where part-B itself also crosses a line boundary.
    for end_marker in ('!"', '?"', '."'):
        em_idx = norm_quote.find(end_marker)
        if em_idx < 2:
            continue
        part_a = norm_quote[:em_idx + len(end_marker)]  # includes the marker
        # part_b is the text after the join (skip leading space / quote-open)
        remainder = norm_quote[em_idx + len(end_marker):].lstrip(' "')
        if not remainder or len(remainder) < 5:
            continue

        # Build multiple part_b candidates at different lengths
        part_b_candidates = [remainder[:HEAD_CHARS]]
        # Also try truncating at part-B's own end marker
        for em2 in ('!"', '?"', '."'):
            idx2 = remainder.find(em2)
            if idx2 >= 5:
                part_b_candidates.append(remainder[:idx2 + len(em2)])
                break
        # Also try a shorter 15-char slice
        if len(remainder) >= SHORT_HEAD_THRESHOLD:
            part_b_candidates.append(remainder[:SHORT_HEAD_THRESHOLD])

        # Deduplicate
        seen_pb: set[str] = set()
        pb_list = []
        for pb in part_b_candidates:
            if pb and pb not in seen_pb:
                seen_pb.add(pb)
                pb_list.append(pb)

        # Find all lines containing part_a
        for idx_a, (lineno_a, norm_line_a) in enumerate(norm_lines):
            if part_a not in norm_line_a:
                continue
            # Scan nearby lines for any part_b candidate
            for idx_b, (lineno_b, norm_line_b) in enumerate(norm_lines):
                if abs(lineno_b - lineno_a) > PROXIMITY_LINES:
                    continue
                for pb in pb_list:
                    if pb in norm_line_b:
                        return min(lineno_a, lineno_b)
        break  # only try the first matching end_marker

    return None


# ---------------------------------------------------------------------------
# Safety assertion
# ---------------------------------------------------------------------------
def assert_safety(input_rows: list[dict], output_rows: list[dict]) -> None:
    """Assert the safety contract: only evidence_ref changed; row count identical.

    Raises AssertionError with a descriptive message if any violation found.
    Compares each row with evidence_ref removed — all other fields must be
    deep-equal.
    """
    if len(input_rows) != len(output_rows):
        raise AssertionError(
            f"Row count mismatch: {len(input_rows)} in → {len(output_rows)} out"
        )
    for i, (inp, out) in enumerate(zip(input_rows, output_rows)):
        inp_minus = {k: v for k, v in inp.items() if k != "evidence_ref"}
        out_minus = {k: v for k, v in out.items() if k != "evidence_ref"}
        if inp_minus != out_minus:
            # Find which keys differ
            all_keys = set(inp_minus) | set(out_minus)
            diffs = [
                k for k in all_keys
                if inp_minus.get(k) != out_minus.get(k)
            ]
            raise AssertionError(
                f"Row {i}: non-evidence_ref fields changed: {diffs}\n"
                f"  src={inp.get('source_slug')} tgt={inp.get('target_slug')}"
            )


# ---------------------------------------------------------------------------
# Main re-grounding logic
# ---------------------------------------------------------------------------
def reground_edges(
    input_rows: list[dict],
    chapters_dir: Path,
) -> tuple[list[dict], dict]:
    """Re-ground all edges.  Returns (output_rows, stats).

    stats keys:
      regrounded      — count where line suffix was updated
      skipped_no_quote — count where edge was left unchanged (no searchable quote)
      unresolved      — count where quote not found in chapter
      unchanged_correct — count where :11 was already correct (quote is at line 11)
      unresolved_list — list of dicts with details on unresolved edges
    """
    output_rows: list[dict] = []
    count_regrounded = 0
    count_skipped = 0
    count_unresolved = 0
    count_unchanged_correct = 0
    unresolved_list: list[dict] = []

    # Cache chapter lines to avoid re-reading the same file repeatedly
    chapter_cache: dict[str, list[tuple[int, str]]] = {}

    for row in input_rows:
        quote = row.get("evidence_quote", "")
        evidence_ref = row.get("evidence_ref", "")

        # Condition 1: skip if no searchable quote
        if (
            not quote
            or not quote.strip()
            or quote.startswith("[PARAPHRASE]")
            or not evidence_ref
            or ":" not in evidence_ref
        ):
            output_rows.append(copy.deepcopy(row))
            count_skipped += 1
            continue

        # Extract chapter path (part before ':')
        chapter_rel, _, old_lineno_str = evidence_ref.rpartition(":")
        chapter_path = chapters_dir.parent.parent / chapter_rel  # repo-root relative
        # Resolve relative to REPO_ROOT
        if not chapter_path.is_absolute():
            chapter_path = REPO_ROOT / chapter_rel

        # Find the true line
        true_lineno = find_quote_line(quote, chapter_path)

        out_row = copy.deepcopy(row)

        if true_lineno is not None:
            new_ref = f"{chapter_rel}:{true_lineno}"
            if new_ref != evidence_ref:
                out_row["evidence_ref"] = new_ref
                count_regrounded += 1
            else:
                # Old ref was already correct
                count_unchanged_correct += 1
        else:
            # Quote not found — leave unchanged
            count_unresolved += 1
            unresolved_list.append({
                "source_slug": row.get("source_slug", ""),
                "target_slug": row.get("target_slug", ""),
                "edge_type": row.get("edge_type", ""),
                "chapter": chapter_rel,
                "evidence_quote": quote[:120],
                "old_evidence_ref": evidence_ref,
            })

        output_rows.append(out_row)

    stats = {
        "regrounded": count_regrounded,
        "skipped_no_quote": count_skipped,
        "unresolved": count_unresolved,
        "unchanged_correct": count_unchanged_correct,
        "unresolved_list": unresolved_list,
    }
    return output_rows, stats


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------
def build_report(
    input_rows: list[dict],
    output_rows: list[dict],
    stats: dict,
    chapters_dir: Path,
) -> str:
    """Build a markdown regrounding report."""
    lines = [
        "# Core Edge Citation Re-grounding Report",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total edges in | {len(input_rows):,} |",
        f"| Total edges out | {len(output_rows):,} |",
        f"| Regrounded (line suffix updated) | {stats['regrounded']:,} |",
        f"| Skipped (no searchable quote / paraphrase) | {stats['skipped_no_quote']:,} |",
        f"| Already correct (line unchanged) | {stats['unchanged_correct']:,} |",
        f"| Unresolved (quote not found in chapter) | {stats['unresolved']:,} |",
        "",
    ]

    # New line-suffix distribution in output
    new_suffix_counts: Counter = Counter()
    for row in output_rows:
        ref = row.get("evidence_ref", "")
        if ":" in ref:
            new_suffix_counts[ref.split(":")[-1]] += 1
        else:
            new_suffix_counts["(no suffix)"] += 1

    lines += [
        "## New Line-Suffix Distribution (top 20)",
        "",
        "| Line | Count |",
        "|------|-------|",
    ]
    for suffix, cnt in new_suffix_counts.most_common(20):
        lines.append(f"| {suffix} | {cnt:,} |")
    lines.append("")

    # Before/after table — 10 representative regrounded edges
    before_after: list[tuple[dict, dict]] = []
    for inp, out in zip(input_rows, output_rows):
        if inp.get("evidence_ref") != out.get("evidence_ref"):
            before_after.append((inp, out))
        if len(before_after) >= 10:
            break

    if before_after:
        lines += [
            "## Before/After Sample (first 10 regrounded edges)",
            "",
            "| source→target | edge_type | OLD ref | NEW ref | Line content at NEW ref |",
            "|---------------|-----------|---------|---------|-------------------------|",
        ]
        for inp, out in before_after:
            src = inp.get("source_slug", "")
            tgt = inp.get("target_slug", "")
            etype = inp.get("edge_type", "")
            old_ref = inp.get("evidence_ref", "")
            new_ref = out.get("evidence_ref", "")

            # Read the actual content at the new line
            new_chapter_rel, _, new_lineno_str = new_ref.rpartition(":")
            new_chapter_path = REPO_ROOT / new_chapter_rel
            line_content = ""
            try:
                lineno = int(new_lineno_str)
                file_lines = new_chapter_path.read_text(encoding="utf-8", errors="replace").splitlines()
                if 1 <= lineno <= len(file_lines):
                    line_content = file_lines[lineno - 1].strip()[:80]
            except (ValueError, OSError):
                line_content = "(unreadable)"

            # Truncate for table
            src_tgt = f"{src}→{tgt}"
            if len(src_tgt) > 40:
                src_tgt = src_tgt[:37] + "..."

            old_suffix = old_ref.split(":")[-1] if ":" in old_ref else old_ref
            new_suffix = new_ref.split(":")[-1] if ":" in new_ref else new_ref
            # Show just the line numbers in the ref columns to keep table narrow
            old_display = f"...:{old_suffix}"
            new_display = f"...:{new_suffix}"
            lc = line_content.replace("|", "\\|")

            lines.append(f"| {src_tgt} | {etype} | {old_display} | {new_display} | {lc} |")
        lines.append("")

    # Unresolved list
    unresolved = stats["unresolved_list"]
    lines += [
        f"## Unresolved Edges (quote not found in chapter) — {len(unresolved)} total",
        "",
    ]
    if not unresolved:
        lines.append("None. All quotes were located successfully.")
        lines.append("")
    else:
        display = unresolved[:20]
        lines += [
            "| source→target | edge_type | chapter | quote head |",
            "|---------------|-----------|---------|------------|",
        ]
        for item in display:
            src_tgt = f"{item['source_slug']}→{item['target_slug']}"
            etype = item.get("edge_type", "")
            chap = item.get("chapter", "").split("/")[-1]  # just filename
            qhead = item.get("evidence_quote", "")[:60].replace("|", "\\|")
            lines.append(f"| {src_tgt} | {etype} | {chap} | {qhead} |")
        if len(unresolved) > 20:
            lines.append(f"| ... | | | ({len(unresolved) - 20} more) |")
        lines.append("")

    lines += [
        "## Safety Assertion",
        "",
        "PASSED — only `evidence_ref` changed; all other fields byte-identical; "
        f"{len(input_rows):,} → {len(output_rows):,} rows.",
        "",
    ]

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Deterministic citation re-grounding pass for graph/edges/edges.jsonl.\n"
            "Finds the TRUE file line for each evidence_quote and rewrites the\n"
            "line suffix of evidence_ref.  Only evidence_ref changes; all other\n"
            "fields are preserved verbatim.\n\n"
            "Default: plan (dry-run).  Use --apply to write output files."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write outputs to graph/edges/_regrounding/.  Default: plan (dry-run).",
    )
    parser.add_argument(
        "--edges-file",
        type=Path,
        default=None,
        metavar="PATH",
        help=f"Override input edges file (default: {EDGES_IN})",
    )
    args = parser.parse_args()

    edges_file = args.edges_file or EDGES_IN

    # -----------------------------------------------------------------------
    # Load input
    # -----------------------------------------------------------------------
    if not edges_file.exists():
        print(f"ERROR: edges file not found: {edges_file}", file=sys.stderr)
        sys.exit(1)

    input_rows: list[dict] = []
    with edges_file.open(encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                input_rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(f"  WARNING: JSON parse error on line {lineno}: {exc}", file=sys.stderr)

    print(f"Loaded {len(input_rows):,} edges from {edges_file}")

    # -----------------------------------------------------------------------
    # Re-ground
    # -----------------------------------------------------------------------
    print("Re-grounding citations...")
    output_rows, stats = reground_edges(input_rows, CHAPTERS_DIR)

    # -----------------------------------------------------------------------
    # Safety assertion (always runs; abort before writing if violated)
    # -----------------------------------------------------------------------
    print("Running safety assertion...")
    try:
        assert_safety(input_rows, output_rows)
        print("  Safety assertion PASSED.")
    except AssertionError as exc:
        print(f"  SAFETY ASSERTION FAILED: {exc}", file=sys.stderr)
        sys.exit(2)

    # -----------------------------------------------------------------------
    # Print summary
    # -----------------------------------------------------------------------
    total = len(input_rows)
    n_regrounded = stats["regrounded"]
    n_skipped = stats["skipped_no_quote"]
    n_unresolved = stats["unresolved"]
    n_correct = stats["unchanged_correct"]

    print()
    print("=" * 60)
    print("CITATION RE-GROUNDING SUMMARY")
    print("=" * 60)
    print(f"  Total edges:               {total:>6,}")
    print(f"  Regrounded:                {n_regrounded:>6,}  ({100*n_regrounded/total:.1f}%)")
    print(f"  Already correct:           {n_correct:>6,}  ({100*n_correct/total:.1f}%)")
    print(f"  Skipped (no/paraphrase):   {n_skipped:>6,}  ({100*n_skipped/total:.1f}%)")
    print(f"  Unresolved (not found):    {n_unresolved:>6,}  ({100*n_unresolved/total:.1f}%)")
    print()

    # New line-suffix distribution
    new_suffix_counts: Counter = Counter()
    for row in output_rows:
        ref = row.get("evidence_ref", "")
        if ":" in ref:
            new_suffix_counts[ref.split(":")[-1]] += 1
        else:
            new_suffix_counts["(no-suffix)"] += 1

    print("New line-suffix distribution (top 20):")
    for suffix, cnt in new_suffix_counts.most_common(20):
        print(f"  :{suffix:<8}  {cnt:>5,}")
    print()

    # Before/after sample
    before_after_shown = 0
    print("Before/After sample (first 10 regrounded edges):")
    print(f"  {'source→target':<40}  {'edge_type':<16}  {'OLD ref':<30}  {'NEW ref':<30}")
    print(f"  {'-'*40}  {'-'*16}  {'-'*30}  {'-'*30}")
    for inp, out in zip(input_rows, output_rows):
        if inp.get("evidence_ref") != out.get("evidence_ref"):
            src_tgt = f"{inp.get('source_slug','')}→{inp.get('target_slug','')}"
            # Show the actual line content at the new ref
            new_ref = out.get("evidence_ref", "")
            new_chapter_rel, _, new_lineno_str = new_ref.rpartition(":")
            line_content = ""
            try:
                lineno_int = int(new_lineno_str)
                ch_path = REPO_ROOT / new_chapter_rel
                file_lines = ch_path.read_text(encoding="utf-8", errors="replace").splitlines()
                if 1 <= lineno_int <= len(file_lines):
                    line_content = file_lines[lineno_int - 1].strip()[:60]
            except (ValueError, OSError):
                line_content = "(unreadable)"
            print(f"  {src_tgt:<40}  {inp.get('edge_type',''):<16}  "
                  f"{inp.get('evidence_ref',''):<30}  {new_ref:<30}")
            print(f"    line content: {line_content!r}")
            before_after_shown += 1
            if before_after_shown >= 10:
                break
    print()

    # Unresolved list
    unresolved = stats["unresolved_list"]
    if unresolved:
        print(f"Unresolved edges ({len(unresolved)} total"
              + (f"; showing first 20" if len(unresolved) > 20 else "") + "):")
        for item in unresolved[:20]:
            print(f"  {item['source_slug']}→{item['target_slug']}  "
                  f"[{item.get('edge_type','')}]  "
                  f"chapter={item.get('chapter','').split('/')[-1]}  "
                  f"quote={item.get('evidence_quote','')[:60]!r}")
        if len(unresolved) > 20:
            print(f"  ... ({len(unresolved) - 20} more in report)")
    else:
        print("Unresolved: none — all quotes located.")
    print()

    # -----------------------------------------------------------------------
    # Write outputs (--apply only)
    # -----------------------------------------------------------------------
    if not args.apply:
        print("Plan mode — nothing written. Re-run with --apply to write outputs.")
        return

    REGROUNDING_DIR.mkdir(parents=True, exist_ok=True)

    # Write regrounded edges
    with EDGES_OUT.open("w", encoding="utf-8") as fh:
        for row in output_rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Written: {EDGES_OUT}")

    # Write report
    report_text = build_report(input_rows, output_rows, stats, CHAPTERS_DIR)
    REPORT_OUT.write_text(report_text, encoding="utf-8")
    print(f"Written: {REPORT_OUT}")

    print()
    print(f"Done. {n_regrounded:,} edges regrounded; safety assertion passed.")


if __name__ == "__main__":
    main()
