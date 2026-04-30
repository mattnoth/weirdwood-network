#!/usr/bin/env python3
"""
wiki-pass2-build-cross-refs.py — Stage 4 prep: cross-reference index builder

Walks all prose files in working/wiki-pass2/<bucket_id>/prose/<slug>.prose.md,
extracts every [anchor text](wiki:Page_Name) markdown link, and produces three
corpus-wide artifacts:

  working/wiki-parsed/cross-references.jsonl  — one row per link found
  working/wiki-parsed/backlink-counts.json    — inverted index + stats
  working/wiki-parsed/cross-refs-summary.md   — human-readable leaderboard

Usage:
  python3 scripts/wiki-pass2-build-cross-refs.py           # dry-run (no files written)
  python3 scripts/wiki-pass2-build-cross-refs.py --apply   # write all 3 outputs
"""

import argparse
import collections
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
WIKI_PASS2_DIR = REPO_ROOT / "working" / "wiki-pass2"
GRAPH_NODES_DIR = REPO_ROOT / "graph" / "nodes"
WIKI_PARSED_DIR = REPO_ROOT / "working" / "wiki-parsed"

OUT_XREFS = WIKI_PARSED_DIR / "cross-references.jsonl"
OUT_BACKLINKS = WIKI_PARSED_DIR / "backlink-counts.json"
OUT_SUMMARY = WIKI_PARSED_DIR / "cross-refs-summary.md"

# ---------------------------------------------------------------------------
# Slug computation (same rule as Stage 3a/3b)
# ---------------------------------------------------------------------------
def to_slug(raw: str) -> str:
    """Convert a wiki page name or display name to a kebab-case slug.

    Must match the canonical convention in wiki-pass2-triage.py::page_to_slug
    and wiki-pass2-emit-deterministic.py::page_to_slug:
    - Lowercase
    - Strip apostrophes, quotes, commas (so King's -> kings, not king-s)
    - Replace spaces/underscores with hyphens
    - Replace remaining non-alphanumeric chars with hyphens
    - Collapse consecutive hyphens, strip leading/trailing hyphens
    """
    s = raw.lower()
    s = re.sub(r"['\",]", "", s)          # strip possessives/quotes before hyphenating
    s = re.sub(r"[ _]+", "-", s)          # spaces and underscores -> hyphens
    s = re.sub(r"[^a-z0-9-]", "-", s)    # anything else -> hyphen
    s = re.sub(r"-+", "-", s).strip("-")
    return s


# ---------------------------------------------------------------------------
# Link extraction
# ---------------------------------------------------------------------------
# Matches [anchor text](wiki:Page_Name) — captures anchor in group 1, page in group 2.
# Deliberately does NOT match bare (wiki:Page.cite_ref-...) footnote patterns.
LINK_RE = re.compile(r"\[([^\]]+)\]\(wiki:([^)]+)\)")

# Heading patterns
H2_RE = re.compile(r"^## (.+)$")
H3_RE = re.compile(r"^### (.+)$")

SNIPPET_RADIUS = 75


def extract_snippet(line: str, match_start: int, match_end: int) -> str:
    """
    Extract up to SNIPPET_RADIUS chars on each side of the matched link,
    on the same line, collapsing internal whitespace to single spaces.
    Returns empty string if there's no surrounding context.
    """
    before = line[:match_start].strip()
    after = line[match_end:].strip()

    # Collapse whitespace
    before = re.sub(r"\s+", " ", before)
    after = re.sub(r"\s+", " ", after)

    if not before and not after:
        return ""

    parts = []
    if before:
        parts.append(("..." if len(before) > SNIPPET_RADIUS else "") + before[-SNIPPET_RADIUS:])
    parts.append("[LINK]")
    if after:
        parts.append(after[:SNIPPET_RADIUS] + ("..." if len(after) > SNIPPET_RADIUS else ""))
    return " ".join(parts)


def extract_links_from_prose(prose_path: Path) -> list[dict]:
    """
    Parse a single .prose.md file and return a list of link dicts.
    Each dict has keys: source_slug, source_section, target_page,
    target_slug, anchor_text, snippet.
    (target_in_graph is filled in later after the graph set is built.)
    """
    source_slug = prose_path.stem  # e.g. "petyr-frey" from "petyr-frey.prose.md"
    links = []
    current_h2 = None
    current_h3 = None

    try:
        text = prose_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"  WARNING: Cannot read {prose_path}: {exc}", file=sys.stderr)
        return []

    for line in text.splitlines():
        # Track headings
        m2 = H2_RE.match(line)
        if m2:
            current_h2 = m2.group(1).strip()
            current_h3 = None
            continue
        m3 = H3_RE.match(line)
        if m3:
            current_h3 = m3.group(1).strip()
            continue

        # Section label
        if current_h2 and current_h3:
            section = f"## {current_h2} / ### {current_h3}"
        elif current_h2:
            section = f"## {current_h2}"
        else:
            section = None

        # Extract all links on this line
        for match in LINK_RE.finditer(line):
            anchor_text = match.group(1)
            target_page = match.group(2)

            # Skip citation footnotes that somehow ended up inside a link
            # (shouldn't happen with proper cite_ref formatting, but be safe)
            if ".cite_ref" in target_page:
                continue

            target_slug = to_slug(target_page)
            snippet = extract_snippet(line, match.start(), match.end())

            row = {
                "source_slug": source_slug,
                "source_section": section,
                "target_page": target_page,
                "target_slug": target_slug,
                "anchor_text": anchor_text,
                "snippet": snippet if snippet else None,
            }
            links.append(row)

    return links


# ---------------------------------------------------------------------------
# Graph node membership set
# ---------------------------------------------------------------------------
def build_graph_slug_set() -> set[str]:
    """
    Walk graph/nodes/**/*.node.md, excluding _conflicts/ and _unclassified/.
    Returns a set of slug strings (filename stem without .node.md).
    """
    slugs = set()
    for node_file in GRAPH_NODES_DIR.rglob("*.node.md"):
        # Skip conflict/unclassified subdirs
        parts = node_file.relative_to(GRAPH_NODES_DIR).parts
        if "_conflicts" in parts or "_unclassified" in parts:
            continue
        slug = node_file.name
        if slug.endswith(".node.md"):
            slug = slug[: -len(".node.md")]
        slugs.add(slug)
    return slugs


# ---------------------------------------------------------------------------
# Backlink index computation
# ---------------------------------------------------------------------------
def build_backlink_index(
    rows: list[dict],
) -> tuple[dict, dict]:
    """
    Returns:
      backlinks: {target_slug: {in_count, sources: Counter}}
      out_counts: {source_slug: set of distinct target_slugs}
    """
    # in_count per target + source tracking
    target_sources: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    # distinct targets per source
    source_targets: dict[str, set] = collections.defaultdict(set)

    for row in rows:
        src = row["source_slug"]
        tgt = row["target_slug"]
        target_sources[tgt][src] += 1
        source_targets[src].add(tgt)

    return target_sources, source_targets


# ---------------------------------------------------------------------------
# Summary markdown generation
# ---------------------------------------------------------------------------
def _histogram(in_counts: list[int]) -> str:
    """Rough log-scale histogram of in_count values."""
    if not in_counts:
        return "(no data)"
    buckets = collections.Counter()
    for c in in_counts:
        if c == 1:
            bucket = "1"
        elif c <= 5:
            bucket = "2-5"
        elif c <= 10:
            bucket = "6-10"
        elif c <= 25:
            bucket = "11-25"
        elif c <= 50:
            bucket = "26-50"
        elif c <= 100:
            bucket = "51-100"
        elif c <= 250:
            bucket = "101-250"
        elif c <= 500:
            bucket = "251-500"
        else:
            bucket = "500+"
    buckets[bucket] += 1
    # rebuild with all rows
    buckets = collections.Counter()
    for c in in_counts:
        if c == 1:
            bucket = "1"
        elif c <= 5:
            bucket = "2-5"
        elif c <= 10:
            bucket = "6-10"
        elif c <= 25:
            bucket = "11-25"
        elif c <= 50:
            bucket = "26-50"
        elif c <= 100:
            bucket = "51-100"
        elif c <= 250:
            bucket = "101-250"
        elif c <= 500:
            bucket = "251-500"
        else:
            bucket = "500+"
        buckets[bucket] += 1

    order = ["1", "2-5", "6-10", "11-25", "26-50", "51-100", "101-250", "251-500", "500+"]
    lines = ["| in_count range | slug count |", "|----------------|------------|"]
    for b in order:
        if b in buckets:
            lines.append(f"| {b:>14} | {buckets[b]:>10,} |")
    return "\n".join(lines)


def build_summary_md(
    backlinks_json: dict,
    broken_sample: list[dict],
) -> str:
    """Produce the human-readable summary markdown."""
    totals = backlinks_json["totals"]
    backlinks = backlinks_json["backlinks"]

    # Top 50 by in_count
    ranked = sorted(backlinks.items(), key=lambda kv: kv[1]["in_count"], reverse=True)[:50]

    lines = [
        "# Cross-Reference Index — Summary",
        "",
        f"Generated: {backlinks_json['computed_at']}",
        "",
        "## Totals",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Unique source slugs | {totals['unique_sources']:,} |",
        f"| Unique target slugs | {totals['unique_targets']:,} |",
        f"| Total link references | {totals['total_references']:,} |",
        f"| Broken links (target not in graph) | {totals['broken_links']:,} |",
        f"| Self-references (source == target) | {totals['self_references']:,} |",
        "",
        "## Top 50 Most-Referenced Entities (in_count leaderboard)",
        "",
        "| Rank | Slug | in_count | out_count | ratio |",
        "|------|------|----------|-----------|-------|",
    ]
    for rank, (slug, data) in enumerate(ranked, 1):
        lines.append(
            f"| {rank} | {slug} | {data['in_count']:,} | {data['out_count']:,} | {data['ratio']:.2f} |"
        )

    # Histogram
    in_counts = [v["in_count"] for v in backlinks.values()]
    lines += [
        "",
        "## in_count Distribution",
        "",
        _histogram(in_counts),
        "",
        "## Broken Link Sample (target not in graph)",
        "",
    ]
    if broken_sample:
        lines.append("| source_slug | target_page | target_slug |")
        lines.append("|-------------|-------------|-------------|")
        for row in broken_sample[:25]:
            lines.append(
                f"| {row['source_slug']} | {row['target_page']} | {row['target_slug']} |"
            )
    else:
        lines.append("(none)")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build cross-reference index from Wiki Pass 2 prose files."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write output files. Without this flag, runs dry-run and prints stats only.",
    )
    args = parser.parse_args()

    # -----------------------------------------------------------------------
    # Step 1: Build graph slug membership set
    # -----------------------------------------------------------------------
    print("Building graph slug membership set...")
    graph_slugs = build_graph_slug_set()
    print(f"  {len(graph_slugs):,} valid slugs in graph/nodes/ (excluding _conflicts, _unclassified)")

    # -----------------------------------------------------------------------
    # Step 2: Walk all prose files
    # -----------------------------------------------------------------------
    print("Scanning prose files...")
    prose_files = sorted(WIKI_PASS2_DIR.rglob("prose/*.prose.md"))
    print(f"  Found {len(prose_files):,} prose files")

    if not prose_files:
        print("ERROR: No prose files found. Check WIKI_PASS2_DIR path.", file=sys.stderr)
        sys.exit(1)

    # -----------------------------------------------------------------------
    # Step 3: Extract links from all prose files
    # -----------------------------------------------------------------------
    print("Extracting links...")
    all_rows: list[dict] = []
    files_with_links = 0
    files_without_links = 0

    for prose_path in prose_files:
        rows = extract_links_from_prose(prose_path)
        if rows:
            files_with_links += 1
        else:
            files_without_links += 1
        all_rows.extend(rows)

    print(f"  {len(all_rows):,} total links extracted")
    print(f"  {files_with_links:,} files with links, {files_without_links:,} files without")

    # -----------------------------------------------------------------------
    # Step 4: Annotate target_in_graph
    # -----------------------------------------------------------------------
    print("Annotating target_in_graph...")
    broken_links = 0
    self_references = 0
    broken_sample: list[dict] = []

    for row in all_rows:
        in_graph = row["target_slug"] in graph_slugs
        row["target_in_graph"] = in_graph
        if not in_graph:
            broken_links += 1
            if len(broken_sample) < 50:
                broken_sample.append(row)
        if row["source_slug"] == row["target_slug"]:
            self_references += 1

    unique_sources = len({r["source_slug"] for r in all_rows})
    unique_targets = len({r["target_slug"] for r in all_rows})

    print(f"  {broken_links:,} broken links (target not in graph)")
    print(f"  {self_references:,} self-references")
    print(f"  {unique_sources:,} unique source slugs")
    print(f"  {unique_targets:,} unique target slugs")

    # -----------------------------------------------------------------------
    # Step 5: Build backlink index
    # -----------------------------------------------------------------------
    print("Building backlink index...")
    target_sources, source_targets = build_backlink_index(all_rows)

    # out_counts: for each slug that appears as a SOURCE, count distinct targets
    # We want this keyed by target slug for the backlinks dict, but also need
    # it available for any slug that might only be a target.
    # Strategy: build out_count for every source slug that appears in prose.
    out_count_map: dict[str, int] = {
        slug: len(tgts) for slug, tgts in source_targets.items()
    }

    # Build backlinks dict (sorted deterministically)
    backlinks: dict[str, dict] = {}
    for target_slug in sorted(target_sources.keys()):
        sources_counter = target_sources[target_slug]
        in_count = sum(sources_counter.values())
        out_count = out_count_map.get(target_slug, 0)
        ratio = round(in_count / max(out_count, 1), 4)
        # Top 10 sources by frequency
        top_sources = [slug for slug, _ in sources_counter.most_common(10)]
        backlinks[target_slug] = {
            "in_count": in_count,
            "out_count": out_count,
            "ratio": ratio,
            "top_sources": top_sources,
        }

    # -----------------------------------------------------------------------
    # Step 6: Print dry-run report
    # -----------------------------------------------------------------------
    print()
    print("=" * 60)
    print("CROSS-REFERENCE INDEX — DRY-RUN REPORT")
    print("=" * 60)
    print(f"  Total link references : {len(all_rows):,}")
    print(f"  Unique source slugs   : {unique_sources:,}")
    print(f"  Unique target slugs   : {unique_targets:,}")
    print(f"  Broken links          : {broken_links:,}")
    print(f"  Self-references       : {self_references:,}")
    print()

    # Top 20 leaderboard
    ranked = sorted(backlinks.items(), key=lambda kv: kv[1]["in_count"], reverse=True)
    print("Top 20 most-referenced slugs:")
    print(f"  {'Rank':>4}  {'in':>6}  {'out':>5}  {'ratio':>6}  slug")
    print(f"  {'----':>4}  {'------':>6}  {'-----':>5}  {'------':>6}  ----")
    for rank, (slug, data) in enumerate(ranked[:20], 1):
        print(
            f"  {rank:>4}  {data['in_count']:>6,}  {data['out_count']:>5,}  "
            f"{data['ratio']:>6.2f}  {slug}"
        )

    print()
    print("Broken link sample (first 10):")
    for row in broken_sample[:10]:
        print(f"  {row['source_slug']} -> {row['target_page']} (slug: {row['target_slug']})")

    # Sanity check — each entry is a set of acceptable slugs for that character
    # (wiki may use "Robert_I_Baratheon" or "Robert_Baratheon" as the canonical page)
    expected_top_alternatives = [
        {"eddard-stark"},
        {"tyrion-lannister"},
        {"robert-baratheon", "robert-i-baratheon"},
        {"daenerys-targaryen"},
        {"jon-snow"},
        {"cersei-lannister"},
    ]
    top_50_slugs = {slug for slug, _ in ranked[:50]}
    missing_expected = []
    for alt_set in expected_top_alternatives:
        if not alt_set & top_50_slugs:
            missing_expected.append(" or ".join(sorted(alt_set)))
    if missing_expected:
        print()
        print(f"  WARNING: Expected top-50 slugs not found in leaderboard: {missing_expected}")
        print("  This may indicate a slug normalization issue or missing prose files.")
    else:
        print()
        print("  Sanity check PASSED: all expected major characters in top-50 leaderboard.")

    if not args.apply:
        print()
        print("Dry-run complete. Run with --apply to write output files.")
        return

    # -----------------------------------------------------------------------
    # Step 7: Write outputs (--apply only)
    # -----------------------------------------------------------------------
    WIKI_PARSED_DIR.mkdir(parents=True, exist_ok=True)

    # 7a. cross-references.jsonl
    print()
    print(f"Writing {OUT_XREFS} ...")
    # Canonical field order for deterministic output
    canonical_keys = [
        "source_slug", "source_section", "target_page", "target_slug",
        "target_in_graph", "anchor_text", "snippet",
    ]
    with OUT_XREFS.open("w", encoding="utf-8") as fh:
        for row in all_rows:
            ordered = {k: row.get(k) for k in canonical_keys}
            fh.write(json.dumps(ordered, ensure_ascii=False) + "\n")
    print(f"  Written: {len(all_rows):,} rows")

    # 7b. backlink-counts.json
    print(f"Writing {OUT_BACKLINKS} ...")
    computed_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    backlinks_doc = {
        "version": "v1",
        "computed_at": computed_at,
        "totals": {
            "unique_sources": unique_sources,
            "unique_targets": unique_targets,
            "total_references": len(all_rows),
            "broken_links": broken_links,
            "self_references": self_references,
        },
        "backlinks": backlinks,
    }
    with OUT_BACKLINKS.open("w", encoding="utf-8") as fh:
        json.dump(backlinks_doc, fh, ensure_ascii=False, sort_keys=True, indent=2)
        fh.write("\n")
    print(f"  Written: {len(backlinks):,} slug entries")

    # 7c. cross-refs-summary.md
    print(f"Writing {OUT_SUMMARY} ...")
    summary_text = build_summary_md(backlinks_doc, broken_sample)
    OUT_SUMMARY.write_text(summary_text, encoding="utf-8")
    print(f"  Written: {OUT_SUMMARY.name}")

    print()
    print("Done. All 3 output files written.")
    print(f"  {OUT_XREFS}")
    print(f"  {OUT_BACKLINKS}")
    print(f"  {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
