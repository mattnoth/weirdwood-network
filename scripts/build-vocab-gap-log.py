"""
build-vocab-gap-log.py

Aggregate vocabulary-gap questions filed by agents to working/wiki/pass2-buckets/
and produce a human-readable review log plus a structured JSON summary.

Inputs:
  All questions-for-matt.jsonl files under working/wiki/pass2-buckets/
  (the global one at the directory root plus any per-bucket ones in subdirs).

Outputs:
  working/edge-vocabulary-gaps.md        -- human-readable review log
  working/wiki/data/vocab-gap-counts.json -- structured summary

Run: python scripts/build-vocab-gap-log.py [--verbose]
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PASS2_BUCKETS = REPO_ROOT / "working" / "wiki" / "pass2-buckets"
OUT_MD = REPO_ROOT / "working" / "edge-vocabulary-gaps.md"
OUT_JSON = REPO_ROOT / "working" / "wiki" / "data" / "vocab-gap-counts.json"

SNIPPET_MAX = 90   # chars for example snippet truncation in table
TEXT_PREVIEW = 120 # chars for representative text in subsections


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def find_jsonl_files(verbose: bool) -> list[Path]:
    """Return all questions-for-matt.jsonl paths under PASS2_BUCKETS."""
    if not PASS2_BUCKETS.exists():
        return []
    paths = sorted(PASS2_BUCKETS.rglob("questions-for-matt.jsonl"))
    if verbose:
        print(f"[scan] found {len(paths)} questions-for-matt.jsonl file(s)")
    return paths


def parse_all_questions(paths: list[Path], verbose: bool) -> tuple[list[dict], int]:
    """
    Parse every line from every file.  Return (all_rows, total_lines_seen).
    Lines that fail JSON parsing are warned and skipped.
    """
    rows: list[dict] = []
    total_lines = 0

    for path in paths:
        file_rows = 0
        with path.open("r", encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, start=1):
                line = line.strip()
                if not line:
                    continue
                total_lines += 1
                try:
                    obj = json.loads(line)
                    rows.append(obj)
                    file_rows += 1
                except json.JSONDecodeError as exc:
                    print(
                        f"[warn] {path.relative_to(REPO_ROOT)}:{lineno} — "
                        f"JSON parse error: {exc}",
                        file=sys.stderr,
                    )
        if verbose:
            print(f"  {path.relative_to(REPO_ROOT)}: {file_rows} row(s)")

    return rows, total_lines


# ---------------------------------------------------------------------------
# Grouping
# ---------------------------------------------------------------------------

def _gap_key(row: dict) -> str:
    """
    Proposed edge type → group key.
    Falls back to a stable truncated prefix of the text if absent.
    """
    ctx = row.get("context") or {}
    proposed = ctx.get("proposed_edge_type") or ""
    if proposed and proposed.strip():
        return proposed.strip().upper()
    # Unnamed: use a truncated text hash label so each distinct text groups together
    text = (row.get("text") or "").strip()
    if text:
        # Use first 60 chars as a human-readable unnamed key
        return "(unnamed) " + text[:60].replace("\n", " ")
    return "(unnamed)"


def group_vocabulary_gaps(rows: list[dict]) -> dict:
    """
    Group vocabulary-gap rows by proposed edge type.
    Returns dict keyed by group_key → group info dict.
    """
    groups: dict[str, dict] = {}

    for row in rows:
        key = _gap_key(row)
        if key not in groups:
            groups[key] = {
                "proposed_type": key,
                "instances": [],
                "first_asked": None,
                "last_asked": None,
                "all_resolved": True,  # flipped false if any open row
                "resolutions": [],     # list of non-null resolutions
            }

        g = groups[key]
        g["instances"].append(row)

        # Track timestamps
        asked = row.get("asked_at") or ""
        if asked:
            if g["first_asked"] is None or asked < g["first_asked"]:
                g["first_asked"] = asked
            if g["last_asked"] is None or asked > g["last_asked"]:
                g["last_asked"] = asked

        # Track resolution status
        if row.get("resolved_at") is None:
            g["all_resolved"] = False
        else:
            res = row.get("resolution")
            if res:
                g["resolutions"].append(res)

    return groups


# ---------------------------------------------------------------------------
# Markdown rendering helpers
# ---------------------------------------------------------------------------

def _trunc(s: str, n: int) -> str:
    s = (s or "").replace("\n", " ").strip()
    return s[:n] + "…" if len(s) > n else s


def _fmt_ts(ts: str | None) -> str:
    if not ts:
        return "—"
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return ts


def _pick_representative_text(instances: list[dict]) -> str:
    """Return the longest non-empty text field among instances."""
    texts = [(row.get("text") or "").strip() for row in instances]
    texts = [t for t in texts if t]
    if not texts:
        return "(no description text)"
    return max(texts, key=len)


def render_example_table(instances: list[dict]) -> str:
    """Render a markdown table of example snippets for one gap group."""
    lines = [
        "| Bucket | Source → Target | Snippet | Agent |",
        "|--------|-----------------|---------|-------|",
    ]
    for row in instances:
        ctx = row.get("context") or {}
        bucket = row.get("bucket_id") or "—"
        source = ctx.get("source") or "—"
        target = ctx.get("target") or "—"
        snippet = _trunc(ctx.get("snippet") or "", SNIPPET_MAX)
        agent = row.get("agent") or "—"
        lines.append(
            f"| `{bucket}` | {source} → {target} | {snippet} | {agent} |"
        )
    return "\n".join(lines)


def render_open_gap_section(groups: dict) -> str:
    """Render the Open Gaps section, sorted by instance count desc."""
    open_groups = [g for g in groups.values() if not g["all_resolved"]]
    open_groups.sort(key=lambda g: len(g["instances"]), reverse=True)

    if not open_groups:
        return "_No open vocabulary-gap questions._\n"

    parts = []
    for g in open_groups:
        key = g["proposed_type"]
        count = len(g["instances"])
        display = key if not key.startswith("(unnamed)") else "(unnamed)"
        rep_text = _pick_representative_text(g["instances"])
        first = _fmt_ts(g["first_asked"])
        last = _fmt_ts(g["last_asked"])

        parts.append(f"### `{display}`\n")
        parts.append(f"**Instance count:** {count}  ")
        parts.append(f"**First filed:** {first}  ")
        parts.append(f"**Last filed:** {last}\n")
        parts.append(f"\n{rep_text}\n")
        parts.append("\n" + render_example_table(g["instances"]) + "\n")
        parts.append(f"\n**Status:** open\n")

    return "\n".join(parts)


def render_resolved_gap_section(groups: dict) -> str:
    """Render the Resolved Gaps section as a compact table."""
    resolved = [g for g in groups.values() if g["all_resolved"]]
    if not resolved:
        return "_No resolved vocabulary-gap questions._\n"

    lines = [
        "| Proposed Type | Instance Count | Resolved | Resolution Note |",
        "|---------------|---------------|----------|-----------------|",
    ]
    for g in sorted(resolved, key=lambda g: g["last_asked"] or ""):
        key = g["proposed_type"]
        display = key if not key.startswith("(unnamed)") else "(unnamed)"
        count = len(g["instances"])
        res_date = _fmt_ts(g["last_asked"])
        note = _trunc("; ".join(g["resolutions"]), SNIPPET_MAX) if g["resolutions"] else "—"
        lines.append(f"| `{display}` | {count} | {res_date} | {note} |")
    return "\n".join(lines) + "\n"


def render_stats_section(
    gap_rows: list[dict],
    all_rows: list[dict],
    total_files: int,
) -> str:
    """Render counts-by-agent, by-bucket, by-month."""
    by_agent: dict[str, int] = defaultdict(int)
    by_bucket: dict[str, int] = defaultdict(int)
    by_month: dict[str, int] = defaultdict(int)

    for row in gap_rows:
        by_agent[row.get("agent") or "(unknown)"] += 1
        by_bucket[row.get("bucket_id") or "(unknown)"] += 1
        asked = row.get("asked_at") or ""
        if asked:
            month = asked[:7]  # YYYY-MM
            by_month[month] += 1

    lines = [f"**Source files scanned:** {total_files}\n"]
    lines.append(f"**Total rows (all types):** {len(all_rows)}\n")
    lines.append(f"**Vocabulary-gap rows:** {len(gap_rows)}\n")

    if by_agent:
        lines.append("\n#### By Agent\n")
        lines.append("| Agent | Gap Questions |")
        lines.append("|-------|--------------|")
        for agent, cnt in sorted(by_agent.items(), key=lambda x: -x[1]):
            lines.append(f"| {agent} | {cnt} |")

    if by_bucket:
        lines.append("\n#### By Bucket\n")
        lines.append("| Bucket | Gap Questions |")
        lines.append("|--------|--------------|")
        for bucket, cnt in sorted(by_bucket.items(), key=lambda x: -x[1]):
            lines.append(f"| `{bucket}` | {cnt} |")

    if by_month:
        lines.append("\n#### By Month Filed\n")
        lines.append("| Month | Gap Questions |")
        lines.append("|-------|--------------|")
        for month, cnt in sorted(by_month.items()):
            lines.append(f"| {month} | {cnt} |")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Markdown document assembly
# ---------------------------------------------------------------------------

def build_markdown(
    groups: dict,
    gap_rows: list[dict],
    all_rows: list[dict],
    total_files: int,
    computed_at: str,
) -> str:
    open_count = sum(1 for g in groups.values() if not g["all_resolved"])
    resolved_count = sum(1 for g in groups.values() if g["all_resolved"])
    total_gap = len(gap_rows)

    header_lines = [
        "# Edge Vocabulary Gaps — Review Log",
        "",
        f"> Generated: {computed_at}  ",
        f"> Open gaps: **{open_count}**  |  Resolved gaps: **{resolved_count}**  "
        f"|  Total vocabulary-gap questions: **{total_gap}**  ",
        f"> Source files scanned: {total_files}",
        "",
    ]

    if total_gap == 0:
        other_count = len(all_rows)
        if total_files == 0:
            seed_note = (
                "No `questions-for-matt.jsonl` files found under "
                "`working/wiki/pass2-buckets/`. "
                "This file will populate as Stage 4 agents run and flag missing edge types."
            )
        else:
            seed_note = (
                f"No `vocabulary-gap` questions found in {total_files} scanned file(s) "
                f"({other_count} other-type question(s) seen). "
                "This file will populate as Stage 4 agents run and flag missing edge types."
            )
        header_lines += [
            "> **Note:** " + seed_note,
            "",
        ]

    sections = [
        "---",
        "",
        "## Open Gaps",
        "",
        "Sorted by instance count (most-cited first). Each gap is a relationship type "
        "that one or more agents could not fit into the ~96 locked edge-type vocabulary. "
        "Review these before each vocabulary expansion decision.",
        "",
        render_open_gap_section(groups),
        "",
        "---",
        "",
        "## Resolved Gaps",
        "",
        render_resolved_gap_section(groups),
        "",
        "---",
        "",
        "## Stats",
        "",
        render_stats_section(gap_rows, all_rows, total_files),
        "",
        "---",
        "",
        "_To expand the vocabulary: edit `reference/architecture.md` § "
        "\"Edge Types (Relationship Categories)\", mark the gap resolved here, "
        "then re-run any affected Stage 4 classifier jobs._",
        "",
    ]

    return "\n".join(header_lines + sections)


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------

def build_json(
    groups: dict,
    gap_rows: list[dict],
    all_rows: list[dict],
    computed_at: str,
) -> dict:
    open_count = sum(1 for g in groups.values() if not g["all_resolved"])
    resolved_count = sum(1 for g in groups.values() if g["all_resolved"])

    by_agent: dict[str, int] = defaultdict(int)
    by_bucket: dict[str, int] = defaultdict(int)
    for row in gap_rows:
        by_agent[row.get("agent") or "(unknown)"] += 1
        by_bucket[row.get("bucket_id") or "(unknown)"] += 1

    by_proposed: dict[str, dict] = {}
    for key, g in groups.items():
        display = key if not key.startswith("(unnamed)") else "(unnamed)"
        status = "resolved" if g["all_resolved"] else "open"
        buckets = sorted({r.get("bucket_id") or "(unknown)" for r in g["instances"]})
        by_proposed[display] = {
            "instance_count": len(g["instances"]),
            "status": status,
            "first_asked": g["first_asked"],
            "last_asked": g["last_asked"],
            "buckets": buckets,
        }

    return {
        "version": "v1",
        "computed_at": computed_at,
        "open_count": open_count,
        "resolved_count": resolved_count,
        "total_questions": len(gap_rows),
        "by_proposed_type": by_proposed,
        "by_agent": dict(by_agent),
        "by_bucket": dict(by_bucket),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aggregate vocabulary-gap questions and produce a review log."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print parsing progress per jsonl file.",
    )
    args = parser.parse_args()

    computed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # 1. Discover + parse
    paths = find_jsonl_files(args.verbose)
    all_rows, _ = parse_all_questions(paths, args.verbose)

    # 2. Filter to vocabulary-gap
    gap_rows = [r for r in all_rows if r.get("type") == "vocabulary-gap"]

    if args.verbose:
        print(
            f"[filter] {len(all_rows)} total rows → "
            f"{len(gap_rows)} vocabulary-gap row(s)"
        )

    # 3. Group
    groups = group_vocabulary_gaps(gap_rows)

    # 4. Render markdown
    md = build_markdown(groups, gap_rows, all_rows, len(paths), computed_at)

    # 5. Render JSON
    out_json = build_json(groups, gap_rows, all_rows, computed_at)

    # 6. Write outputs
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(md, encoding="utf-8")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out_json, indent=2), encoding="utf-8")

    # 7. Summary
    open_count = out_json["open_count"]
    resolved_count = out_json["resolved_count"]
    total_gap = out_json["total_questions"]
    total_all = len(all_rows)

    print(f"Done.")
    print(f"  Files scanned      : {len(paths)}")
    print(f"  All-type questions : {total_all}")
    print(f"  Vocabulary-gap     : {total_gap}  (open: {open_count}, resolved: {resolved_count})")
    print(f"  Distinct gap types : {len(groups)}")
    print(f"  Wrote: {OUT_MD.relative_to(REPO_ROOT)}")
    print(f"  Wrote: {OUT_JSON.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
