#!/usr/bin/env python3
"""
wiki-pass2-build-comention-candidates.py — Stage 4 Phase 2 Step B: Co-mention candidate generator

For each meta.chapter prose file, walk paragraph-by-paragraph and emit
entity-pair co-mention candidates — for every pair of [anchor](wiki:Page)
links that co-occur in the same paragraph, emit a candidate
{entityA, entityB, chapter_evidence, ...}.

The classifier decides which edge type (if any) exists between A and B
based on the paragraph context.  This script is purely enumeration.

Output: one JSONL file per chapter at:
  working/wiki/pass2-buckets/<bucket_id>/comention-candidates/<chapter-slug>.candidates.jsonl

Row schema:
  {
    "candidate_kind": "comention",
    "evidence_chapter": "<chapter-slug>",
    "evidence_chapter_bucket": "<bucket-id>",
    "pair_a": "<canonical slug, alphabetically first>",
    "pair_b": "<canonical slug, alphabetically second>",
    "pair_a_in_count": <int>,
    "pair_b_in_count": <int>,
    "evidence_paragraphs": [
      {"section": "## Narrative Arc", "paragraph_index": 3, "snippet": "<~200 char excerpt>"},
      ...
    ],
    "evidence_truncated": false,
    "total_paragraph_count": <int>
  }

Usage:
  python3 scripts/wiki-pass2-build-comention-candidates.py --plan
      Read everything, compute survivors, print stats to stdout. Write NOTHING.
  python3 scripts/wiki-pass2-build-comention-candidates.py --apply
      Same as --plan, plus write per-chapter JSONL outputs + summary files.
  python3 scripts/wiki-pass2-build-comention-candidates.py --plan --book asos
      Restrict to one book's chapters (smoke test).
  python3 scripts/wiki-pass2-build-comention-candidates.py --plan --chapter-slug a-storm-of-swords-chapter-71
      Restrict to a single chapter (debugging).
"""

import argparse
import collections
import itertools
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

IN_ALIAS = WIKI_DATA_DIR / "alias-resolver.json"
IN_BACKLINKS = WIKI_DATA_DIR / "backlink-counts.json"

OUT_SUMMARY_MD = WIKI_DATA_DIR / "comention-candidates-summary.md"
OUT_SUMMARY_JSON = WIKI_DATA_DIR / "comention-candidates-stats.json"

# Bucket name pattern for meta.chapter buckets
BOOK_TO_BUCKET = {
    "agot": "meta-chapters-agot",
    "acok": "meta-chapters-acok",
    "asos": "meta-chapters-asos",
    "affc": "meta-chapters-affc",
    "adwd": "meta-chapters-adwd",
}

# Maximum evidence paragraphs to keep per pair per chapter
MAX_EVIDENCE_PARAGRAPHS = 5

# Skip these graph subdirectories (special/conflict folders)
_SKIP_DIRS = {"_conflicts", "_unclassified", "_stage3-preview"}


# ---------------------------------------------------------------------------
# Slugify — mirrors wiki-pass2-build-cross-refs.py::to_slug exactly
# ---------------------------------------------------------------------------
def to_slug(raw: str) -> str:
    """Convert a wiki page name or display name to a kebab-case slug.

    Must match the canonical convention used by the cross-refs builder:
    - Lowercase
    - Strip apostrophes, quotes, commas
    - Replace spaces/underscores with hyphens
    - Replace remaining non-alphanumeric chars with hyphens
    - Collapse consecutive hyphens, strip leading/trailing hyphens
    """
    s = raw.lower()
    s = re.sub(r"['\",]", "", s)           # strip possessives/quotes/commas
    s = re.sub(r"[ _]+", "-", s)           # spaces and underscores → hyphens
    s = re.sub(r"[^a-z0-9-]", "-", s)     # anything else → hyphen
    s = re.sub(r"-+", "-", s).strip("-")
    return s


# ---------------------------------------------------------------------------
# YAML frontmatter reader (minimal — reads only the --- block)
# ---------------------------------------------------------------------------
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def read_frontmatter(path: Path) -> dict:
    """Read the YAML frontmatter from a .node.md file.

    Returns a dict of key: value pairs (values kept as strings).
    Multi-line / list values returned as the raw string after the colon.
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
# Edges section parser — mirrors wiki-pass2-build-edge-candidates.py exactly
# ---------------------------------------------------------------------------
_EDGE_LINE_RE = re.compile(r"^- [A-Z_]+(?: \([^)]+\))?:\s+(.+)$")


def _extract_target_from_edge_line(line: str) -> str | None:
    """Parse a single edge bullet line and return raw target display name, or None."""
    m = _EDGE_LINE_RE.match(line.strip())
    if not m:
        return None
    rest = m.group(1)
    paren = rest.find("(")
    bracket = rest.find("[")
    delimiters = [p for p in (paren, bracket) if p != -1]
    if delimiters:
        end = min(delimiters)
        target_raw = rest[:end].strip()
    else:
        target_raw = rest.strip()
    return target_raw if target_raw else None


def parse_existing_edges(node_path: Path) -> set[str]:
    """Return the set of target slugs from ## Edges / ## Edges (prose-derived) sections."""
    try:
        text = node_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()

    targets: set[str] = set()
    in_edges_section = False

    for line in text.splitlines():
        if line.startswith("## Edges"):
            in_edges_section = True
            continue
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
# Graph index builder
# ---------------------------------------------------------------------------
def build_graph_index() -> tuple[set[str], dict[str, dict], dict[str, set]]:
    """Walk graph/nodes/**/*.node.md and return:
      - node_slug_set:   set of all canonical slugs
      - node_metadata:   {slug: {"bucket_id": str, "node_path": Path, "node_type": str}}
      - existing_edges:  {slug: set(target_slugs)}  (raw slugs, alias-resolved after load)
    """
    node_slug_set: set[str] = set()
    node_metadata: dict[str, dict] = {}
    existing_edges_raw: dict[str, set] = {}

    for node_file in sorted(GRAPH_NODES_DIR.rglob("*.node.md")):
        parts = node_file.relative_to(GRAPH_NODES_DIR).parts
        if any(p in _SKIP_DIRS for p in parts):
            continue

        slug = node_file.stem  # stem strips .node.md if stem == slug.  Actually name[:-8]
        # .node.md is 8 chars
        slug = node_file.name[: -len(".node.md")]
        if not slug:
            continue

        node_slug_set.add(slug)
        fm = read_frontmatter(node_file)

        node_metadata[slug] = {
            "bucket_id": fm.get("bucket_id", "_no-bucket"),
            "node_path": node_file,
            "node_type": fm.get("type", ""),
        }
        existing_edges_raw[slug] = parse_existing_edges(node_file)

    return node_slug_set, node_metadata, existing_edges_raw


# ---------------------------------------------------------------------------
# Wiki-link extractor for prose paragraphs
# Matches [anchor text](wiki:Page_Name) syntax
# ---------------------------------------------------------------------------
_WIKI_LINK_RE = re.compile(r"\[([^\]]*)\]\(wiki:([^)]+)\)")


def extract_wiki_links(text: str) -> list[tuple[str, str]]:
    """Return list of (anchor_text, wiki_page_name) from [anchor](wiki:Page) links."""
    return [(m.group(1), m.group(2)) for m in _WIKI_LINK_RE.finditer(text)]


# ---------------------------------------------------------------------------
# Prose file paragraph splitter
# Returns list of (section_heading, paragraph_index_within_section, paragraph_text)
# ---------------------------------------------------------------------------
_HEADING_RE = re.compile(r"^#{1,6}\s+.+$")


def split_prose_paragraphs(
    text: str,
) -> list[tuple[str, int, str]]:
    """Split a prose markdown body into (section, para_index_global, text) tuples.

    Rules:
    - Lines are split on blank lines (one or more consecutive empty lines).
    - A line matching ^#{1,6} is a section heading boundary; it becomes the
      current section label for subsequent paragraphs but is NOT itself emitted
      as a paragraph.
    - Paragraphs with no [anchor](wiki:...) links are still emitted (filtered
      later at the caller level).
    - paragraph_index is 0-based and global (not reset per section).
    """
    paragraphs: list[tuple[str, int, str]] = []
    current_section = "(no section)"
    current_lines: list[str] = []
    para_index = 0

    def flush() -> None:
        nonlocal para_index
        chunk = "\n".join(current_lines).strip()
        if chunk:
            paragraphs.append((current_section, para_index, chunk))
            para_index += 1
        current_lines.clear()

    for raw_line in text.splitlines():
        if _HEADING_RE.match(raw_line):
            flush()
            current_section = raw_line.strip()
        elif raw_line.strip() == "":
            flush()
        else:
            current_lines.append(raw_line)

    flush()  # final chunk
    return paragraphs


# ---------------------------------------------------------------------------
# Snippet builder — ~200 char excerpt from paragraph text
# ---------------------------------------------------------------------------
def make_snippet(text: str, max_len: int = 200) -> str:
    """Return up to max_len chars of text, truncating at a word boundary."""
    text = text.strip()
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    last_space = truncated.rfind(" ")
    if last_space > max_len // 2:
        truncated = truncated[:last_space]
    return truncated + "..."


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Stage 4 Phase 2 Step B: Build co-mention candidates from chapter prose files."
        )
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--plan",
        action="store_true",
        default=True,
        help="Dry-run: compute survivors, print stats, write NOTHING (default).",
    )
    mode_group.add_argument(
        "--apply",
        action="store_true",
        help="Also write per-chapter JSONL outputs + summary files.",
    )
    parser.add_argument(
        "--book",
        choices=["agot", "acok", "asos", "affc", "adwd"],
        default=None,
        metavar="BOOK",
        help="Restrict to one book (agot|acok|asos|affc|adwd).",
    )
    parser.add_argument(
        "--chapter-slug",
        default=None,
        metavar="SLUG",
        help="Restrict to a single chapter slug (e.g. a-storm-of-swords-chapter-71).",
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
    # Step 3: Build graph index
    # -----------------------------------------------------------------------
    print("Building graph node index...")
    node_slug_set, node_metadata, existing_edges_raw = build_graph_index()
    print(f"  {len(node_slug_set):,} canonical graph nodes")

    # Alias-resolve existing edge targets (parsed as raw slugified display names)
    print("  Alias-resolving existing edge targets...")
    existing_edges: dict[str, set] = {}
    for slug, raw_targets in existing_edges_raw.items():
        resolved: set[str] = set()
        for t in raw_targets:
            resolved.add(alias_to_canonical.get(t, t))
        existing_edges[slug] = resolved

    # -----------------------------------------------------------------------
    # Step 4: Enumerate chapter prose files
    # -----------------------------------------------------------------------
    # Determine which buckets to scan
    if args.book:
        bucket_names = [BOOK_TO_BUCKET[args.book]]
    else:
        bucket_names = sorted(BOOK_TO_BUCKET.values())

    prose_files: list[tuple[str, Path]] = []  # (bucket_id, prose_path)
    for bucket_name in bucket_names:
        prose_dir = PASS2_BUCKETS_DIR / bucket_name / "prose"
        if not prose_dir.exists():
            print(f"  WARNING: prose dir not found: {prose_dir}", file=sys.stderr)
            continue
        for prose_file in sorted(prose_dir.glob("*.prose.md")):
            chapter_slug = prose_file.name[: -len(".prose.md")]
            if args.chapter_slug and chapter_slug != args.chapter_slug:
                continue
            prose_files.append((bucket_name, prose_file))

    print(f"  {len(prose_files):,} chapter prose files to process")

    # -----------------------------------------------------------------------
    # Step 5: Walk paragraphs, extract pairs, apply filters
    # -----------------------------------------------------------------------
    # Counters
    count_chapters = 0
    count_paragraphs = 0
    count_raw_pair_occurrences = 0      # before any filtering
    count_drop_broken = 0               # broken-link (not in graph after alias resolve)
    count_drop_self = 0                 # self-edge
    count_drop_known = 0                # edge already known
    count_drop_low_conf = 0             # both endpoints low backlink count
    count_unique_pairs_pre_consolidate = 0  # unique (chapter, pair_a, pair_b) combos
    count_survivors = 0                 # final consolidated candidates

    # Aggregated stats
    section_counts: dict[str, int] = collections.Counter()
    broken_links: list[str] = []        # for summary (sample)

    # Per-chapter output: {chapter_slug: [candidate_row, ...]}
    chapter_candidates: dict[str, list[dict]] = {}

    for bucket_id, prose_path in prose_files:
        chapter_slug = prose_path.name[: -len(".prose.md")]
        count_chapters += 1

        # Read prose body
        try:
            prose_text = prose_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"  WARNING: Cannot read {prose_path}: {exc}", file=sys.stderr)
            continue

        # Split into paragraphs
        paragraphs = split_prose_paragraphs(prose_text)
        count_paragraphs += len(paragraphs)

        # Accumulate evidence per (pair_a, pair_b) for this chapter
        # pair_key = (min_slug, max_slug) -> list of evidence dicts
        pair_evidence: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)

        for section, para_idx, para_text in paragraphs:
            links = extract_wiki_links(para_text)
            if len(links) < 2:
                continue  # no pair possible in this paragraph

            # Deduplicate links by wiki page (keep first anchor text seen)
            seen_pages: dict[str, str] = {}  # page_name -> anchor_text
            for anchor, page_name in links:
                if page_name not in seen_pages:
                    seen_pages[page_name] = anchor

            if len(seen_pages) < 2:
                continue  # all links point to same page

            # Resolve each page to a canonical slug
            resolved_page_slugs: dict[str, str] = {}  # page_name -> canonical_slug
            for page_name in seen_pages:
                raw_slug = to_slug(page_name)
                canonical = alias_to_canonical.get(raw_slug, raw_slug)
                resolved_page_slugs[page_name] = canonical

            # Enumerate all unordered pairs of distinct page names
            page_names = list(seen_pages.keys())
            snippet = make_snippet(para_text)

            for page_a, page_b in itertools.combinations(page_names, 2):
                count_raw_pair_occurrences += 1

                slug_a = resolved_page_slugs[page_a]
                slug_b = resolved_page_slugs[page_b]

                # Filter: source-and-target must be in graph
                a_missing = slug_a not in node_slug_set
                b_missing = slug_b not in node_slug_set
                if a_missing or b_missing:
                    count_drop_broken += 1
                    missing_slug = slug_a if a_missing else slug_b
                    if len(broken_links) < 200:
                        broken_links.append(missing_slug)
                    continue

                # Filter: self-edge (same entity after alias resolution)
                if slug_a == slug_b:
                    count_drop_self += 1
                    continue

                # Filter: already-known edge (either direction)
                known_from_a = existing_edges.get(slug_a, set())
                known_from_b = existing_edges.get(slug_b, set())
                if slug_b in known_from_a or slug_a in known_from_b:
                    count_drop_known += 1
                    continue

                # Filter: low-confidence (both endpoints obscure)
                a_in = backlinks.get(slug_a, {}).get("in_count", 0)
                b_in = backlinks.get(slug_b, {}).get("in_count", 0)
                if a_in < 2 and b_in < 2:
                    count_drop_low_conf += 1
                    continue

                # Canonical pair key (alphabetically ordered)
                pair_key = (min(slug_a, slug_b), max(slug_a, slug_b))

                evidence_entry = {
                    "section": section,
                    "paragraph_index": para_idx,
                    "snippet": snippet,
                }
                pair_evidence[pair_key].append(evidence_entry)
                section_counts[section] += 1

        # Consolidate: one candidate row per (pair_a, pair_b) per chapter
        candidates_this_chapter: list[dict] = []
        for (pair_a, pair_b), evidence_list in pair_evidence.items():
            count_unique_pairs_pre_consolidate += 1  # distinct (chapter, pair) combos
            count_survivors += 1

            total_para_count = len(evidence_list)
            truncated = total_para_count > MAX_EVIDENCE_PARAGRAPHS
            evidence_to_emit = evidence_list[:MAX_EVIDENCE_PARAGRAPHS]

            a_in = backlinks.get(pair_a, {}).get("in_count", 0)
            b_in = backlinks.get(pair_b, {}).get("in_count", 0)

            row = {
                "candidate_kind": "comention",
                "evidence_chapter": chapter_slug,
                "evidence_chapter_bucket": bucket_id,
                "pair_a": pair_a,
                "pair_b": pair_b,
                "pair_a_in_count": a_in,
                "pair_b_in_count": b_in,
                "evidence_paragraphs": evidence_to_emit,
                "evidence_truncated": truncated,
                "total_paragraph_count": total_para_count,
            }
            candidates_this_chapter.append(row)

        # Sort within chapter by (pair_a, pair_b) for stable output
        candidates_this_chapter.sort(key=lambda r: (r["pair_a"], r["pair_b"]))
        if candidates_this_chapter:
            chapter_candidates[chapter_slug] = (bucket_id, candidates_this_chapter)

    # -----------------------------------------------------------------------
    # Step 6: Summary stats
    # -----------------------------------------------------------------------
    # Top 20 chapters by survivor count
    top_chapters = sorted(
        [
            (slug, bucket_id, candidates)
            for slug, (bucket_id, candidates) in chapter_candidates.items()
        ],
        key=lambda t: len(t[2]),
        reverse=True,
    )[:20]

    # Top 20 most-paired (A, B) tuples across all chapters
    global_pair_counts: dict[tuple[str, str], int] = collections.Counter()
    for slug, (bucket_id, candidates) in chapter_candidates.items():
        for row in candidates:
            global_pair_counts[(row["pair_a"], row["pair_b"])] += 1
    top_pairs = global_pair_counts.most_common(20)

    # Backlink distribution of survivor endpoints
    bl_buckets_count: dict[str, int] = collections.Counter()
    for slug, (bucket_id, candidates) in chapter_candidates.items():
        for row in candidates:
            for in_count in (row["pair_a_in_count"], row["pair_b_in_count"]):
                if in_count <= 1:
                    label = "0-1"
                elif in_count <= 5:
                    label = "2-5"
                elif in_count <= 10:
                    label = "6-10"
                elif in_count <= 25:
                    label = "11-25"
                elif in_count <= 100:
                    label = "26-100"
                else:
                    label = "101+"
                bl_buckets_count[label] += 1

    # -----------------------------------------------------------------------
    # Step 7: Print plan summary
    # -----------------------------------------------------------------------
    print()
    print("=" * 70)
    print("CO-MENTION CANDIDATE GENERATOR — RUN SUMMARY")
    print("=" * 70)
    print(f"  Chapters scanned:              {count_chapters:>8,}")
    print(f"  Paragraphs walked:             {count_paragraphs:>8,}")
    print(f"  Raw pair-paragraph occurrences:{count_raw_pair_occurrences:>8,}")
    print(f"  Drop (broken-link):            {count_drop_broken:>8,}")
    print(f"  Drop (self-edge):              {count_drop_self:>8,}")
    print(f"  Drop (already-edge):           {count_drop_known:>8,}")
    print(f"  Drop (low-confidence):         {count_drop_low_conf:>8,}")
    print(f"  Unique pairs (pre-consolidate):{count_unique_pairs_pre_consolidate:>8,}")
    print(f"  SURVIVORS (consolidated):      {count_survivors:>8,}")
    print()

    print("Top 20 chapters by survivor count:")
    for slug, bucket_id, candidates in top_chapters:
        print(f"  {len(candidates):>5,}  {slug}")
    print()

    print("Top 10 most-paired (A, B) tuples across all chapters:")
    for (a, b), cnt in top_pairs[:10]:
        print(f"  {cnt:>4,}x  ({a}, {b})")
    print()

    bl_order = ["0-1", "2-5", "6-10", "11-25", "26-100", "101+"]
    print("Backlink-count distribution of survivor endpoints (both endpoints counted):")
    for label in bl_order:
        cnt = bl_buckets_count.get(label, 0)
        if cnt:
            print(f"  {label:>8}  {cnt:,}")
    print()

    print("Top 10 section-of-origin:")
    for sec, cnt in section_counts.most_common(10):
        print(f"  {cnt:>7,}  {sec}")
    print()

    # -----------------------------------------------------------------------
    # Step 8: Write outputs (--apply only)
    # -----------------------------------------------------------------------
    if not write_output:
        print("Plan mode — nothing written. Re-run with --apply to write outputs.")
        return

    run_ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # 8a. Per-chapter JSONL files
    print("Writing per-chapter candidate files...")
    files_written = 0
    total_rows_written = 0
    for chapter_slug, (bucket_id, candidates) in sorted(chapter_candidates.items()):
        out_dir = PASS2_BUCKETS_DIR / bucket_id / "comention-candidates"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{chapter_slug}.candidates.jsonl"
        with out_file.open("w", encoding="utf-8") as fh:
            for row in candidates:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        files_written += 1
        total_rows_written += len(candidates)

    print(f"  {files_written:,} candidate files written")
    print(f"  {total_rows_written:,} total candidate rows written")

    # 8b. Summary markdown
    print(f"Writing {OUT_SUMMARY_MD} ...")
    summary_lines = [
        "# Co-mention Candidates Summary",
        "",
        f"Generated: {run_ts}",
        "",
        "## Counts",
        "",
        "| Stage | Count |",
        "|-------|-------|",
        f"| Chapters scanned | {count_chapters:,} |",
        f"| Paragraphs walked | {count_paragraphs:,} |",
        f"| Raw pair-paragraph occurrences | {count_raw_pair_occurrences:,} |",
        f"| Drop: broken-link | {count_drop_broken:,} |",
        f"| Drop: self-edge | {count_drop_self:,} |",
        f"| Drop: already-known edge | {count_drop_known:,} |",
        f"| Drop: low-confidence | {count_drop_low_conf:,} |",
        f"| Unique pairs (pre-consolidate) | {count_unique_pairs_pre_consolidate:,} |",
        f"| **Survivors (consolidated)** | **{count_survivors:,}** |",
        "",
        "## Top 20 Chapters by Survivor Count",
        "",
        "| Chapter | Bucket | Candidates |",
        "|---------|--------|-----------|",
    ]
    for slug, bucket_id, candidates in top_chapters:
        summary_lines.append(f"| {slug} | {bucket_id} | {len(candidates):,} |")

    summary_lines += [
        "",
        "## Top 20 Most-Paired (A, B) Tuples Across All Chapters",
        "",
        "| Pair A | Pair B | Co-chapter count |",
        "|--------|--------|-----------------|",
    ]
    for (a, b), cnt in top_pairs:
        summary_lines.append(f"| {a} | {b} | {cnt:,} |")

    summary_lines += [
        "",
        "## Backlink-Count Distribution of Survivor Endpoints",
        "",
        "| in_count range | endpoint count |",
        "|----------------|---------------|",
    ]
    for label in bl_order:
        cnt = bl_buckets_count.get(label, 0)
        summary_lines.append(f"| {label} | {cnt:,} |")

    summary_lines += [
        "",
        "## Section-of-Origin Distribution",
        "",
        "| Section (heading) | Count |",
        "|-------------------|-------|",
    ]
    for sec, cnt in section_counts.most_common(30):
        summary_lines.append(f"| {sec} | {cnt:,} |")

    WIKI_DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_SUMMARY_MD.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print(f"  Written: {OUT_SUMMARY_MD}")

    # 8c. Stats JSON
    print(f"Writing {OUT_SUMMARY_JSON} ...")
    stats = {
        "generated_at": run_ts,
        "counts": {
            "chapters_scanned": count_chapters,
            "paragraphs_walked": count_paragraphs,
            "raw_pair_paragraph_occurrences": count_raw_pair_occurrences,
            "drop_broken_link": count_drop_broken,
            "drop_self_edge": count_drop_self,
            "drop_known_edge": count_drop_known,
            "drop_low_confidence": count_drop_low_conf,
            "unique_pairs_pre_consolidate": count_unique_pairs_pre_consolidate,
            "survivors": count_survivors,
        },
        "top_chapters": [
            {"chapter_slug": slug, "bucket_id": bucket_id, "candidate_count": len(candidates)}
            for slug, bucket_id, candidates in top_chapters
        ],
        "top_pairs": [
            {"pair_a": a, "pair_b": b, "co_chapter_count": cnt}
            for (a, b), cnt in top_pairs
        ],
        "backlink_distribution": dict(bl_buckets_count),
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
