#!/usr/bin/env python3
"""
wiki-pass2-build-edge-candidates.py — Stage 4 Step 2: Edge candidate generator

Reads cross-references.jsonl (91k rows of prose cross-references) and filters
them down to the subset that are genuine candidate edges for LLM classification.
Outputs one JSONL file per source node at:
  working/wiki/pass2-buckets/<bucket_id>/prose-edge-candidates/<slug>.candidates.jsonl

Filter pipeline (in order):
  1. Source must be a graph node (not a chapter summary page)
  2. Target resolved through alias map
  3. Target must be in graph
  4. Self-edges dropped
  5. Already-known edges dropped (any edge type already in ## Edges section)
  6. Low-confidence drop (target.in_count < 2 AND section is Quotes or Notes)

This script is deterministic and free (~$0). It reads local files only.

Usage:
  python3 scripts/wiki-pass2-build-edge-candidates.py --plan
      Read everything, run filters, print stats to stdout, write NOTHING to disk.
  python3 scripts/wiki-pass2-build-edge-candidates.py --apply
      Same as --plan, plus write per-source JSONL + summary files.
  python3 scripts/wiki-pass2-build-edge-candidates.py --plan --source-glob 'daenerys-*'
      Restrict to source slugs matching glob (smoke test).
  python3 scripts/wiki-pass2-build-edge-candidates.py --plan --limit-buckets 5
      Restrict to first N buckets alphabetically.
"""

import argparse
import collections
import fnmatch
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
GRAPH_NODES_DIR = REPO_ROOT / "graph" / "nodes"
WIKI_DATA_DIR = REPO_ROOT / "working" / "wiki" / "data"
PASS2_BUCKETS_DIR = REPO_ROOT / "working" / "wiki" / "pass2-buckets"

IN_XREFS = WIKI_DATA_DIR / "cross-references.jsonl"
IN_ALIAS = WIKI_DATA_DIR / "alias-resolver.json"
IN_BACKLINKS = WIKI_DATA_DIR / "backlink-counts.json"

OUT_SUMMARY_MD = WIKI_DATA_DIR / "edge-candidates-summary.md"
OUT_SUMMARY_JSON = WIKI_DATA_DIR / "edge-candidates-stats.json"

# ---------------------------------------------------------------------------
# Slugify — mirror of wiki-pass2-build-cross-refs.py::to_slug exactly
# ---------------------------------------------------------------------------
def to_slug(raw: str) -> str:
    """Convert a wiki page name or display name to a kebab-case slug.

    Must match the canonical convention:
    - Lowercase
    - Strip apostrophes, quotes, commas (so King's -> kings, not king-s)
    - Replace spaces/underscores with hyphens
    - Replace remaining non-alphanumeric chars with hyphens
    - Collapse consecutive hyphens, strip leading/trailing hyphens
    """
    s = raw.lower()
    s = re.sub(r"['\",]", "", s)           # strip possessives/quotes before hyphenating
    s = re.sub(r"[ _]+", "-", s)           # spaces and underscores -> hyphens
    s = re.sub(r"[^a-z0-9-]", "-", s)     # anything else -> hyphen
    s = re.sub(r"-+", "-", s).strip("-")
    return s


# ---------------------------------------------------------------------------
# YAML frontmatter reader (minimal — read only the --- block)
# ---------------------------------------------------------------------------
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def read_frontmatter(path: Path) -> dict:
    """Read the YAML frontmatter from a .node.md file.

    Returns a dict of key: value pairs. Values are kept as strings.
    No full YAML parse — just extract simple `key: value` pairs.
    Multi-line / list values are returned as the raw string after the colon.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}

    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}

    fm: dict = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in fm:  # take first occurrence only
            fm[key] = val
    return fm


# ---------------------------------------------------------------------------
# Edges section parser
# Extract target display names from lines like:
#   - EDGE_TYPE: Target Name (... context ...)
#   - EDGE_TYPE (reverse): Target Name [qualifier]
#   - EDGE_TYPE: Target Name [qualifier]
# The target is the text after ': ' and before the FIRST '(' or '[', trimmed.
# Then slugify to match the graph slug convention.
# ---------------------------------------------------------------------------
_EDGE_LINE_RE = re.compile(r"^- [A-Z_]+(?: \([^)]+\))?:\s+(.+)$")


def _extract_target_from_edge_line(line: str) -> str | None:
    """Parse a single edge bullet line and return the raw target display name, or None."""
    m = _EDGE_LINE_RE.match(line.strip())
    if not m:
        return None
    rest = m.group(1)
    # Target is text before first '(' or '[', whichever comes first
    paren = rest.find("(")
    bracket = rest.find("[")
    # Pick the earlier delimiter, ignoring -1 (not found)
    delimiters = [p for p in (paren, bracket) if p != -1]
    if delimiters:
        end = min(delimiters)
        target_raw = rest[:end].strip()
    else:
        target_raw = rest.strip()
    return target_raw if target_raw else None


def parse_existing_edges(node_path: Path) -> set[str]:
    """Return the set of target slugs from the ## Edges section of a node file.

    Reads both `## Edges` and `## Edges (prose-derived)` for completeness.
    Slugifies each target and alias-resolves through the provided map.
    """
    try:
        text = node_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()

    targets: set[str] = set()
    in_edges_section = False

    for line in text.splitlines():
        # Enter edges section on any heading starting with "## Edges"
        if line.startswith("## Edges"):
            in_edges_section = True
            continue
        # Exit on any other ## heading
        if line.startswith("## ") and not line.startswith("## Edges"):
            in_edges_section = False
            continue
        if not in_edges_section:
            continue
        target_raw = _extract_target_from_edge_line(line)
        if target_raw:
            targets.add(to_slug(target_raw))

    return targets


# ---------------------------------------------------------------------------
# Graph node walker
# Returns:
#   node_slug_set:      set of all canonical graph slugs
#   node_metadata:      {slug: {"bucket_id": ..., "node_path": Path}}
#   existing_edges:     {slug: set of target_slugs}
# ---------------------------------------------------------------------------
_SKIP_DIRS = {"_conflicts", "_unclassified", "_stage3-preview"}


def build_graph_index() -> tuple[set[str], dict, dict]:
    """Walk graph/nodes/**/*.node.md and build lookup tables."""
    node_slug_set: set[str] = set()
    node_metadata: dict[str, dict] = {}
    existing_edges: dict[str, set] = {}

    for node_file in sorted(GRAPH_NODES_DIR.rglob("*.node.md")):
        parts = node_file.relative_to(GRAPH_NODES_DIR).parts
        # Skip special dirs
        if any(p in _SKIP_DIRS for p in parts):
            continue

        slug = node_file.name[: -len(".node.md")]
        if not slug:
            continue

        node_slug_set.add(slug)

        fm = read_frontmatter(node_file)
        bucket_id = fm.get("bucket_id", "_no-bucket")

        node_metadata[slug] = {
            "bucket_id": bucket_id,
            "node_path": node_file,
        }

    # Parse existing edges separately (after slug set is built so we can alias-resolve
    # in a second pass; we store raw slugs here and alias-resolve after alias map loaded)
    for slug, meta in node_metadata.items():
        existing_edges[slug] = parse_existing_edges(meta["node_path"])

    return node_slug_set, node_metadata, existing_edges


# ---------------------------------------------------------------------------
# Low-confidence section filter
# ---------------------------------------------------------------------------
_LOW_CONF_SECTIONS = re.compile(r"^## (Quotes?|Notes?)[\s]*$", re.IGNORECASE)


def is_low_confidence_section(source_section: str | None) -> bool:
    """Return True if this section heading is Quotes or Notes (low-confidence)."""
    if not source_section:
        return False
    # source_section may be "## Quotes" or "## Notes / ### sub" — check the H2 part
    h2_part = source_section.split("/")[0].strip()
    return bool(_LOW_CONF_SECTIONS.match(h2_part))


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stage 4 Step 2: Build prose edge candidates from cross-references."
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--plan",
        action="store_true",
        default=True,
        help="Dry-run: read everything, print stats, write nothing (default).",
    )
    mode_group.add_argument(
        "--apply",
        action="store_true",
        help="Run filters AND write per-source JSONL + summary files.",
    )
    parser.add_argument(
        "--source-glob",
        metavar="PATTERN",
        default=None,
        help="Restrict to source slugs matching this glob (e.g. 'daenerys-*').",
    )
    parser.add_argument(
        "--limit-buckets",
        metavar="N",
        type=int,
        default=None,
        help="Restrict to first N buckets alphabetically.",
    )
    args = parser.parse_args()

    write_output = args.apply

    # -----------------------------------------------------------------------
    # Step 1: Load alias resolver
    # -----------------------------------------------------------------------
    print("Loading alias resolver...")
    try:
        alias_data = json.loads(IN_ALIAS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: Cannot load {IN_ALIAS}: {exc}", file=sys.stderr)
        sys.exit(1)
    alias_to_canonical: dict[str, str] = alias_data.get("alias_to_canonical", {})
    print(f"  {len(alias_to_canonical):,} aliases loaded")

    # -----------------------------------------------------------------------
    # Step 2: Load backlink counts
    # -----------------------------------------------------------------------
    print("Loading backlink counts...")
    try:
        backlink_data = json.loads(IN_BACKLINKS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: Cannot load {IN_BACKLINKS}: {exc}", file=sys.stderr)
        sys.exit(1)
    backlinks: dict[str, dict] = backlink_data.get("backlinks", {})
    print(f"  {len(backlinks):,} target slugs with backlink data")

    # -----------------------------------------------------------------------
    # Step 3: Build graph index (slug set, metadata, existing edges)
    # -----------------------------------------------------------------------
    print("Building graph node index...")
    node_slug_set, node_metadata, existing_edges_raw = build_graph_index()
    print(f"  {len(node_slug_set):,} canonical graph nodes")

    # Alias-resolve existing edge targets (they were parsed as raw slugs from
    # display names; resolve them through the alias map so comparisons work)
    print("  Alias-resolving existing edge targets...")
    existing_edges: dict[str, set] = {}
    for slug, raw_targets in existing_edges_raw.items():
        resolved: set[str] = set()
        for t in raw_targets:
            resolved.add(alias_to_canonical.get(t, t))
        existing_edges[slug] = resolved

    # -----------------------------------------------------------------------
    # Step 4: Determine bucket filter (--limit-buckets)
    # -----------------------------------------------------------------------
    allowed_buckets: set[str] | None = None
    if args.limit_buckets is not None:
        all_buckets = sorted({
            meta["bucket_id"]
            for meta in node_metadata.values()
            if meta["bucket_id"] != "_no-bucket"
        })
        allowed_buckets = set(all_buckets[: args.limit_buckets])
        print(f"  Limiting to {len(allowed_buckets)} buckets: {sorted(allowed_buckets)[:5]}{'...' if len(allowed_buckets) > 5 else ''}")

    # -----------------------------------------------------------------------
    # Step 5: Stream cross-references.jsonl through filter pipeline
    # -----------------------------------------------------------------------
    print(f"Processing cross-references from {IN_XREFS} ...")

    # Counters
    count_in = 0
    count_drop_not_node = 0        # Filter 1: source not a graph node
    count_drop_broken_target = 0   # Filter 3: target not in graph after alias resolve
    count_drop_self = 0            # Filter 4: self-edge
    count_drop_known = 0           # Filter 5: edge already exists
    count_drop_low_conf = 0        # Filter 6: low-confidence section + low backlink
    count_survivors = 0

    broken_links: list[dict] = []  # For summary

    # Collect survivors per source slug
    survivors_by_source: dict[str, list[dict]] = collections.defaultdict(list)

    try:
        xref_file = IN_XREFS.open(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: Cannot open {IN_XREFS}: {exc}", file=sys.stderr)
        sys.exit(1)

    with xref_file:
        for raw_line in xref_file:
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                row = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                print(f"  WARNING: Skipping malformed JSON line: {exc}", file=sys.stderr)
                continue

            count_in += 1

            # -- Filter 1: source must be a graph node --
            raw_source_slug = row.get("source_slug", "")
            # Strip .prose suffix (always present per analysis)
            if raw_source_slug.endswith(".prose"):
                source_slug = raw_source_slug[: -len(".prose")]
            else:
                source_slug = raw_source_slug

            if source_slug not in node_slug_set:
                count_drop_not_node += 1
                continue

            # -- Source glob filter (CLI option) --
            if args.source_glob and not fnmatch.fnmatch(source_slug, args.source_glob):
                count_drop_not_node += 1  # count as skipped-not-node for simplicity
                continue

            # -- Bucket filter (CLI option) --
            source_bucket = node_metadata[source_slug]["bucket_id"]
            if allowed_buckets is not None and source_bucket not in allowed_buckets:
                count_drop_not_node += 1
                continue

            # -- Filter 2 + 3: resolve target through alias map, then check graph membership --
            raw_target_slug = row.get("target_slug", "")
            resolved_target = alias_to_canonical.get(raw_target_slug, raw_target_slug)

            if resolved_target not in node_slug_set:
                count_drop_broken_target += 1
                if len(broken_links) < 500:
                    broken_links.append({
                        "source_slug": source_slug,
                        "target_page": row.get("target_page", ""),
                        "raw_target_slug": raw_target_slug,
                        "resolved_target_slug": resolved_target,
                    })
                continue

            # -- Filter 4: self-edge --
            if source_slug == resolved_target:
                count_drop_self += 1
                continue

            # -- Filter 5: already-known edge --
            known = existing_edges.get(source_slug, set())
            if resolved_target in known:
                count_drop_known += 1
                continue

            # -- Filter 6: low-confidence --
            target_bl = backlinks.get(resolved_target, {}).get("in_count", 0)
            if target_bl < 2 and is_low_confidence_section(row.get("source_section")):
                count_drop_low_conf += 1
                continue

            # -- Survivor: build output row --
            count_survivors += 1
            candidate = {
                "candidate_kind": "source_target",
                "source_slug": source_slug,
                "source_bucket": source_bucket,
                "source_section": row.get("source_section"),
                "target_slug": resolved_target,
                "target_page": row.get("target_page", ""),
                "anchor_text": row.get("anchor_text", ""),
                "snippet": row.get("snippet"),
                "backlink_count": target_bl,
            }
            survivors_by_source[source_slug].append(candidate)

    print(f"  {count_in:,} rows read")
    print(f"  {count_drop_not_node:,} dropped: source not graph node (or filtered by --source-glob / --limit-buckets)")
    print(f"  {count_drop_broken_target:,} dropped: broken target (not in graph after alias resolve)")
    print(f"  {count_drop_self:,} dropped: self-edge")
    print(f"  {count_drop_known:,} dropped: edge already known")
    print(f"  {count_drop_low_conf:,} dropped: low-confidence (Notes/Quotes + in_count < 2)")
    print(f"  {count_survivors:,} surviving candidates across {len(survivors_by_source):,} source nodes")

    # -----------------------------------------------------------------------
    # Step 6: Sort survivors within each source for stable output
    # -----------------------------------------------------------------------
    for source_slug in survivors_by_source:
        survivors_by_source[source_slug].sort(
            key=lambda r: (r.get("source_section") or "", r["target_slug"])
        )

    # -----------------------------------------------------------------------
    # Step 7: Build summary stats
    # -----------------------------------------------------------------------
    # Top 20 sources by survivor count
    top_sources = sorted(
        survivors_by_source.items(),
        key=lambda kv: len(kv[1]),
        reverse=True,
    )[:20]

    # Top 20 targets by inbound-candidate count
    target_inbound: dict[str, int] = collections.Counter()
    for candidates in survivors_by_source.values():
        for c in candidates:
            target_inbound[c["target_slug"]] += 1
    top_targets = target_inbound.most_common(20)

    # Backlink distribution of survivors' targets
    bl_buckets: dict[str, int] = collections.Counter()
    for candidates in survivors_by_source.values():
        for c in candidates:
            bl = c["backlink_count"]
            if bl <= 1:
                bucket_label = "1"
            elif bl <= 5:
                bucket_label = "2-5"
            elif bl <= 10:
                bucket_label = "6-10"
            elif bl <= 25:
                bucket_label = "11-25"
            elif bl <= 100:
                bucket_label = "26-100"
            else:
                bucket_label = "101+"
            bl_buckets[bucket_label] += 1

    # Section-of-origin distribution
    section_counts: dict[str, int] = collections.Counter()
    for candidates in survivors_by_source.values():
        for c in candidates:
            sec = c.get("source_section") or "(none)"
            # Normalize to H2 only
            h2 = sec.split("/")[0].strip() if "/" in sec else sec.strip()
            section_counts[h2] += 1

    # -----------------------------------------------------------------------
    # Step 8: Print plan summary
    # -----------------------------------------------------------------------
    print()
    print("=" * 70)
    print("EDGE CANDIDATE GENERATOR — RUN SUMMARY")
    print("=" * 70)
    print(f"  Rows in:               {count_in:>8,}")
    print(f"  Drop (source filter):  {count_drop_not_node:>8,}")
    print(f"  Drop (broken target):  {count_drop_broken_target:>8,}")
    print(f"  Drop (self-edge):      {count_drop_self:>8,}")
    print(f"  Drop (known edge):     {count_drop_known:>8,}")
    print(f"  Drop (low-confidence): {count_drop_low_conf:>8,}")
    print(f"  SURVIVORS:             {count_survivors:>8,}")
    print(f"  Distinct source nodes: {len(survivors_by_source):>8,}")
    print()

    print("Top 5 source nodes by survivor count:")
    for slug, cands in top_sources[:5]:
        print(f"  {len(cands):>5,}  {slug}")
    print()

    print("Top 5 target nodes by inbound-candidate count:")
    for slug, cnt in top_targets[:5]:
        print(f"  {cnt:>5,}  {slug}")
    print()

    print("Backlink distribution of survivor targets:")
    bl_order = ["1", "2-5", "6-10", "11-25", "26-100", "101+"]
    for label in bl_order:
        cnt = bl_buckets.get(label, 0)
        if cnt:
            print(f"  {label:>8}  {cnt:,}")
    print()

    # -----------------------------------------------------------------------
    # Step 9: Write outputs (--apply only)
    # -----------------------------------------------------------------------
    if not write_output:
        print("Plan mode — nothing written. Re-run with --apply to write outputs.")
        return

    run_ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # 9a. Per-source JSONL files
    print("Writing per-source candidate files...")
    files_written = 0
    for source_slug, candidates in survivors_by_source.items():
        source_bucket = node_metadata[source_slug]["bucket_id"]
        out_dir = PASS2_BUCKETS_DIR / source_bucket / "prose-edge-candidates"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{source_slug}.candidates.jsonl"
        with out_file.open("w", encoding="utf-8") as fh:
            for c in candidates:
                fh.write(json.dumps(c, ensure_ascii=False) + "\n")
        files_written += 1

    print(f"  {files_written:,} candidate files written")

    # 9b. Summary markdown
    print(f"Writing {OUT_SUMMARY_MD} ...")
    summary_lines = [
        "# Edge Candidates Summary",
        "",
        f"Generated: {run_ts}",
        "",
        "## Counts",
        "",
        "| Stage | Count |",
        "|-------|-------|",
        f"| Cross-refs rows in | {count_in:,} |",
        f"| Drop: source not graph node | {count_drop_not_node:,} |",
        f"| Drop: broken target | {count_drop_broken_target:,} |",
        f"| Drop: self-edge | {count_drop_self:,} |",
        f"| Drop: already-known edge | {count_drop_known:,} |",
        f"| Drop: low-confidence | {count_drop_low_conf:,} |",
        f"| **Survivors** | **{count_survivors:,}** |",
        f"| Distinct source nodes | {len(survivors_by_source):,} |",
        "",
        "## Top 20 Source Nodes by Survivor Count",
        "",
        "| Source Slug | Candidates |",
        "|-------------|-----------|",
    ]
    for slug, cands in top_sources:
        summary_lines.append(f"| {slug} | {len(cands):,} |")

    summary_lines += [
        "",
        "## Top 20 Target Nodes by Inbound-Candidate Count",
        "",
        "| Target Slug | Inbound Candidates |",
        "|-------------|-------------------|",
    ]
    for slug, cnt in top_targets:
        summary_lines.append(f"| {slug} | {cnt:,} |")

    summary_lines += [
        "",
        "## Backlink Distribution of Survivor Targets",
        "",
        "| in_count range | candidate count |",
        "|----------------|----------------|",
    ]
    for label in bl_order:
        cnt = bl_buckets.get(label, 0)
        summary_lines.append(f"| {label} | {cnt:,} |")

    summary_lines += [
        "",
        "## Section-of-Origin Distribution",
        "",
        "| Section (H2) | Count |",
        "|--------------|-------|",
    ]
    for sec, cnt in section_counts.most_common(30):
        summary_lines.append(f"| {sec} | {cnt:,} |")

    # Broken link list (unique target_page → resolved slug, for debugging)
    unique_broken: dict[str, str] = {}
    for bl in broken_links:
        key = bl["target_page"]
        if key not in unique_broken:
            unique_broken[key] = bl["resolved_target_slug"]

    summary_lines += [
        "",
        f"## Broken-Link Resolutions (sample, {len(unique_broken):,} unique target pages)",
        "",
        "| target_page | resolved_slug |",
        "|-------------|---------------|",
    ]
    for page, slug in list(unique_broken.items())[:50]:
        summary_lines.append(f"| {page} | {slug} |")

    WIKI_DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_SUMMARY_MD.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print(f"  Written: {OUT_SUMMARY_MD}")

    # 9c. Stats JSON
    print(f"Writing {OUT_SUMMARY_JSON} ...")
    stats = {
        "generated_at": run_ts,
        "counts": {
            "rows_in": count_in,
            "drop_source_filter": count_drop_not_node,
            "drop_broken_target": count_drop_broken_target,
            "drop_self_edge": count_drop_self,
            "drop_known_edge": count_drop_known,
            "drop_low_confidence": count_drop_low_conf,
            "survivors": count_survivors,
            "distinct_source_nodes": len(survivors_by_source),
        },
        "top_sources": [
            {"slug": slug, "candidate_count": len(cands)}
            for slug, cands in top_sources
        ],
        "top_targets": [
            {"slug": slug, "inbound_count": cnt}
            for slug, cnt in top_targets
        ],
        "backlink_distribution": dict(bl_buckets),
        "section_distribution": dict(section_counts.most_common(30)),
    }
    OUT_SUMMARY_JSON.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"  Written: {OUT_SUMMARY_JSON}")

    print()
    print(f"Done. {count_survivors:,} candidates written to {files_written:,} files.")
    print(f"  Summary: {OUT_SUMMARY_MD}")
    print(f"  Stats:   {OUT_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
