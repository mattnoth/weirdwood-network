#!/usr/bin/env python3
"""
wiki-pass2-build-pass1-relationship-candidates.py — Stage 4 Phase 2 Step C:
Pass 1 relationship candidate generator.

Walks all 344 Pass 1 extraction files under extractions/mechanical/{book}/.
For each file, parses the "## Relationships Observed" markdown table.
Each table row becomes a structured candidate edge for the prose-edge classifier.

The key advantage of these candidates over co-mention candidates: the relationship
is PRE-ASSERTED in natural language by Opus reading the actual chapter text.
The classifier's job is to map the asserted_relation string to a vocabulary type,
not to discover whether a relationship exists.

Output: one JSONL file per chapter at:
  working/wiki/pass2-buckets/extractions-pass1/{book}/{chapter-slug}.candidates.jsonl

Row schema:
  {
    "candidate_kind": "pass1_relationship",
    "evidence_chapter": "agot-bran-01",
    "evidence_book": "agot",
    "evidence_pov": "bran-stark",
    "source_slug": "eddard-stark",
    "target_slug": "bran-stark",
    "asserted_relation": "father — protective, carries Bran on shoulder",
    "evidence_quote": "(positioning notes)",
    "extraction_file": "extractions/mechanical/agot/agot-bran-01.extraction.md"
  }

Usage:
  python3 scripts/wiki-pass2-build-pass1-relationship-candidates.py --plan
      Read everything, compute survivors, print stats to stdout. Write NOTHING.
  python3 scripts/wiki-pass2-build-pass1-relationship-candidates.py --apply
      Same as --plan, plus write per-chapter JSONL + summary files.
  python3 scripts/wiki-pass2-build-pass1-relationship-candidates.py --plan --book agot
      Restrict to one book (smoke test).
  python3 scripts/wiki-pass2-build-pass1-relationship-candidates.py --plan --chapter-slug agot-bran-01
      Restrict to a single chapter (debugging).
"""

import argparse
import collections
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
EXTRACTIONS_DIR = REPO_ROOT / "extractions" / "mechanical"
WIKI_DATA_DIR = REPO_ROOT / "working" / "wiki" / "data"
PASS2_BUCKETS_DIR = REPO_ROOT / "working" / "wiki" / "pass2-buckets"

IN_ALIAS = WIKI_DATA_DIR / "alias-resolver.json"

OUT_BASE_DIR = PASS2_BUCKETS_DIR / "extractions-pass1"
OUT_SUMMARY_MD = WIKI_DATA_DIR / "pass1-relationship-candidates-summary.md"
OUT_SUMMARY_JSON = WIKI_DATA_DIR / "pass1-relationship-candidates-stats.json"

BOOKS = ["agot", "acok", "asos", "affc", "adwd"]

# Skip these graph subdirectories (special/conflict folders)
_SKIP_DIRS = {"_conflicts", "_unclassified", "_stage3-preview"}


# ---------------------------------------------------------------------------
# Slugify — mirrors wiki-pass2-build-cross-refs.py::to_slug exactly
# ---------------------------------------------------------------------------
def to_slug(raw: str) -> str:
    """Convert a display name to a kebab-case slug.

    Must match the canonical convention:
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
# Extraction file metadata parser
#
# Pass 1 extractions do NOT have YAML frontmatter. They use a markdown-prose
# header section like:
#
#   # AGOT — Bran I
#
#   ## Chapter Metadata
#   - **book:** AGOT
#   - **chapter_number:** 2
#   - **pov_character:** Bran Stark
#   - **pov_chapter_number:** Bran I
#   ...
#
# We parse the ## Chapter Metadata section as key-value bullet lines.
# ---------------------------------------------------------------------------
_METADATA_KEY_RE = re.compile(r"^\s*-\s+\*\*([^*]+)\*\*:\s*(.+)$")
_HEADING_RE = re.compile(r"^##\s+(.+)$")


def parse_extraction_metadata(text: str) -> dict:
    """Parse the ## Chapter Metadata section from an extraction file body.

    Returns a dict with at minimum: book, chapter_number, pov_character.
    Values are stripped strings.
    """
    meta: dict = {}
    in_metadata = False

    for line in text.splitlines():
        # Detect section entry/exit
        h2_match = _HEADING_RE.match(line)
        if h2_match:
            section_name = h2_match.group(1).strip()
            in_metadata = section_name.lower() == "chapter metadata"
            continue

        if not in_metadata:
            continue

        m = _METADATA_KEY_RE.match(line)
        if m:
            key = m.group(1).strip().lower().replace(" ", "_")
            val = m.group(2).strip()
            if key and key not in meta:
                meta[key] = val

    return meta


def derive_chapter_slug(extraction_path: Path) -> str:
    """Derive chapter slug from the extraction filename.

    Filenames follow: {book}-{pov-slug}-{NN}.extraction.md
    e.g. agot-bran-01.extraction.md → agot-bran-01
    """
    return extraction_path.name[: -len(".extraction.md")]


def derive_pov_slug(pov_character: str) -> str:
    """Slugify the pov_character value from metadata.

    e.g. "Bran Stark" → "bran-stark"
    """
    return to_slug(pov_character)


# ---------------------------------------------------------------------------
# Relationships Observed table parser
#
# Expected format (header line):
#   | Character A | Relationship | Character B | Evidence |
#   |-------------|-------------|-------------|----------|
#   | Bran Stark  | Son of      | Eddard Stark| "..."    |
#
# The spec says "From | To | Relationship | Evidence" but actual files all use
# "Character A | Relationship | Character B | Evidence" (verified across 344 files).
# We match liberally on any table that follows a heading containing "relationship".
# ---------------------------------------------------------------------------
_RELATIONSHIP_HEADING_RE = re.compile(r"^##\s+.*relationship", re.IGNORECASE)
_TABLE_ROW_RE = re.compile(r"^\|(.+)\|$")


def _split_table_row(line: str) -> list[str]:
    """Split a pipe-delimited markdown table row into cell strings.

    Handles escaped pipes (rare) by naive split — good enough for extraction data.
    Returns list of stripped cell values, not including the outer empty strings
    from the leading/trailing pipe.
    """
    # Strip the outer pipes, then split
    inner = line.strip().strip("|")
    cells = [c.strip() for c in inner.split("|")]
    return cells


def _is_separator_row(cells: list[str]) -> bool:
    """Return True if this is a table separator row (--- dashes)."""
    return all(re.match(r"^[-: ]+$", c) for c in cells if c)


def parse_relationships_table(text: str) -> list[dict]:
    """Parse the ## Relationships Observed table from an extraction file.

    Returns a list of dicts with keys:
      char_a, relationship, char_b, evidence

    Column order is inferred from the header row. Supported column name variants:
      - Character A / From → char_a
      - Character B / To   → char_b
      - Relationship       → relationship
      - Evidence           → evidence

    If the section or table is missing, returns [].
    If no valid rows are found, returns [].
    """
    in_relationships_section = False
    header_cols: list[str] = []  # normalized column names
    col_index_char_a = -1
    col_index_relationship = -1
    col_index_char_b = -1
    col_index_evidence = -1
    rows: list[dict] = []

    for line in text.splitlines():
        # Section detection: enter on relationship heading, exit on any other ##
        h2_match = _HEADING_RE.match(line)
        if h2_match:
            section_label = h2_match.group(1).strip()
            if re.search(r"relationship", section_label, re.IGNORECASE):
                in_relationships_section = True
                header_cols = []  # reset for this section
                col_index_char_a = col_index_relationship = col_index_char_b = col_index_evidence = -1
            else:
                in_relationships_section = False
            continue

        if not in_relationships_section:
            continue

        # Must be a table row
        if not _TABLE_ROW_RE.match(line.strip()):
            continue

        cells = _split_table_row(line)
        if not cells:
            continue

        # Separator row — skip
        if _is_separator_row(cells):
            continue

        # Header row — detect columns (first non-separator table row)
        if not header_cols:
            header_cols = [c.lower() for c in cells]
            for i, h in enumerate(header_cols):
                if h in ("character a", "from"):
                    col_index_char_a = i
                elif h in ("character b", "to"):
                    col_index_char_b = i
                elif "relationship" in h:
                    col_index_relationship = i
                elif "evidence" in h:
                    col_index_evidence = i
            # Validate we found the essential columns
            if col_index_char_a < 0 or col_index_relationship < 0 or col_index_char_b < 0:
                # Unrecognized header — warn and stop parsing this section
                print(
                    f"  WARNING: Unrecognized Relationships Observed header: {cells}",
                    file=sys.stderr,
                )
                in_relationships_section = False
            continue

        # Data row — extract cells by index
        def safe_get(idx: int) -> str:
            if idx < 0 or idx >= len(cells):
                return ""
            return cells[idx].strip()

        char_a = safe_get(col_index_char_a)
        relationship = safe_get(col_index_relationship)
        char_b = safe_get(col_index_char_b)
        evidence = safe_get(col_index_evidence)

        # Skip rows where key fields are empty or look like continuation lines
        if not char_a or not char_b or not relationship:
            continue

        rows.append(
            {
                "char_a": char_a,
                "relationship": relationship,
                "char_b": char_b,
                "evidence": evidence,
            }
        )

    return rows


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
def build_graph_index() -> tuple[set[str], dict[str, set]]:
    """Walk graph/nodes/**/*.node.md and return:
      - node_slug_set:   set of all canonical slugs
      - existing_edges:  {slug: set(target_slugs)}  (raw slugs; alias-resolve after load)
    """
    node_slug_set: set[str] = set()
    node_paths: dict[str, Path] = {}
    existing_edges_raw: dict[str, set] = {}

    for node_file in sorted(GRAPH_NODES_DIR.rglob("*.node.md")):
        parts = node_file.relative_to(GRAPH_NODES_DIR).parts
        if any(p in _SKIP_DIRS for p in parts):
            continue

        slug = node_file.name[: -len(".node.md")]
        if not slug:
            continue

        node_slug_set.add(slug)
        node_paths[slug] = node_file
        existing_edges_raw[slug] = parse_existing_edges(node_file)

    return node_slug_set, existing_edges_raw


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Stage 4 Phase 2 Step C: Build Pass 1 relationship candidates "
            "from extraction Relationships Observed tables."
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
        choices=BOOKS,
        default=None,
        metavar="BOOK",
        help="Restrict to one book (agot|acok|asos|affc|adwd).",
    )
    parser.add_argument(
        "--chapter-slug",
        default=None,
        metavar="SLUG",
        help="Restrict to a single chapter slug (e.g. agot-bran-01).",
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
    # Step 2: Build graph index (slug set + existing edges)
    # -----------------------------------------------------------------------
    print("Building graph node index...")
    node_slug_set, existing_edges_raw = build_graph_index()
    print(f"  {len(node_slug_set):,} canonical graph nodes")

    # Alias-resolve existing edge targets
    print("  Alias-resolving existing edge targets...")
    existing_edges: dict[str, set] = {}
    for slug, raw_targets in existing_edges_raw.items():
        resolved: set[str] = set()
        for t in raw_targets:
            resolved.add(alias_to_canonical.get(t, t))
        existing_edges[slug] = resolved

    # -----------------------------------------------------------------------
    # Step 3: Enumerate extraction files
    # -----------------------------------------------------------------------
    books_to_scan = [args.book] if args.book else BOOKS

    extraction_files: list[Path] = []
    for book in books_to_scan:
        book_dir = EXTRACTIONS_DIR / book
        if not book_dir.exists():
            print(f"  WARNING: extraction dir not found: {book_dir}", file=sys.stderr)
            continue
        for f in sorted(book_dir.glob("*.extraction.md")):
            chapter_slug = derive_chapter_slug(f)
            if args.chapter_slug and chapter_slug != args.chapter_slug:
                continue
            extraction_files.append(f)

    print(f"  {len(extraction_files):,} extraction files to process")

    # -----------------------------------------------------------------------
    # Step 4: Process each extraction file
    # -----------------------------------------------------------------------
    # Counters
    count_files_walked = 0
    count_no_relationships_section = 0
    count_rows_seen = 0
    count_drop_unresolved_source = 0
    count_drop_unresolved_target = 0
    count_drop_self = 0
    count_drop_known = 0
    count_survivors = 0

    # Unresolved entity tracking: {raw_name: count}
    unresolved_counter: dict[str, int] = collections.Counter()

    # Per-chapter output: {chapter_slug: (book, [candidate_row, ...])}
    chapter_candidates: dict[str, tuple[str, list[dict]]] = {}

    # Book distribution: {book: count_survivors}
    book_survivors: dict[str, int] = collections.Counter()

    # Top sources by survivor count (across all chapters)
    source_survivor_counts: dict[str, int] = collections.Counter()
    target_inbound_counts: dict[str, int] = collections.Counter()

    # Sample survivors for reporting (up to 20)
    sample_survivors: list[dict] = []

    for extraction_path in extraction_files:
        count_files_walked += 1

        # Derive chapter metadata from the file
        chapter_slug = derive_chapter_slug(extraction_path)
        # Book from directory name
        book_abbrev = extraction_path.parent.name.lower()

        try:
            text = extraction_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"  WARNING: Cannot read {extraction_path}: {exc}", file=sys.stderr)
            continue

        # Parse Chapter Metadata section
        meta = parse_extraction_metadata(text)
        pov_character_raw = meta.get("pov_character", "")
        if pov_character_raw:
            pov_slug = derive_pov_slug(pov_character_raw)
        else:
            # Fall back to deriving pov from filename: {book}-{pov}-{NN}.extraction.md
            parts = chapter_slug.split("-")
            if len(parts) >= 3:
                # book is first part, number is last, pov is middle
                pov_slug = "-".join(parts[1:-1])
            else:
                pov_slug = ""

        # Parse Relationships Observed table
        rows = parse_relationships_table(text)

        if not rows:
            count_no_relationships_section += 1
            # Check whether the section exists at all
            if "relationship" not in text.lower():
                print(
                    f"  WARNING: No Relationships Observed section in {extraction_path.name}",
                    file=sys.stderr,
                )
            continue

        count_rows_seen += len(rows)

        # Process each table row
        candidates_this_chapter: list[dict] = []
        extraction_rel = str(extraction_path.relative_to(REPO_ROOT))

        for row in rows:
            char_a_raw = row["char_a"]
            char_b_raw = row["char_b"]
            relationship = row["relationship"]
            evidence = row["evidence"]

            # Slugify both entity names
            source_slug_candidate = to_slug(char_a_raw)
            target_slug_candidate = to_slug(char_b_raw)

            # Alias-resolve both
            source_slug = alias_to_canonical.get(source_slug_candidate, source_slug_candidate)
            target_slug = alias_to_canonical.get(target_slug_candidate, target_slug_candidate)

            # Filter: source must be in graph
            if source_slug not in node_slug_set:
                count_drop_unresolved_source += 1
                unresolved_counter[char_a_raw] += 1
                continue

            # Filter: target must be in graph
            if target_slug not in node_slug_set:
                count_drop_unresolved_target += 1
                unresolved_counter[char_b_raw] += 1
                continue

            # Filter: self-edge
            if source_slug == target_slug:
                count_drop_self += 1
                continue

            # Filter: already-known edge (either direction)
            known_from_source = existing_edges.get(source_slug, set())
            known_from_target = existing_edges.get(target_slug, set())
            if target_slug in known_from_source or source_slug in known_from_target:
                count_drop_known += 1
                continue

            # Survivor
            count_survivors += 1
            book_survivors[book_abbrev] += 1
            source_survivor_counts[source_slug] += 1
            target_inbound_counts[target_slug] += 1

            candidate = {
                "candidate_kind": "pass1_relationship",
                "evidence_chapter": chapter_slug,
                "evidence_book": book_abbrev,
                "evidence_pov": pov_slug,
                "source_slug": source_slug,
                "target_slug": target_slug,
                "asserted_relation": relationship,
                "evidence_quote": evidence,
                "extraction_file": extraction_rel,
            }
            candidates_this_chapter.append(candidate)

            if len(sample_survivors) < 20:
                sample_survivors.append(candidate)

        if candidates_this_chapter:
            # Sort within chapter by (source_slug, target_slug) for stable output
            candidates_this_chapter.sort(key=lambda r: (r["source_slug"], r["target_slug"]))
            chapter_candidates[chapter_slug] = (book_abbrev, candidates_this_chapter)

    # -----------------------------------------------------------------------
    # Step 5: Summary stats
    # -----------------------------------------------------------------------
    top_sources = source_survivor_counts.most_common(20)
    top_targets = target_inbound_counts.most_common(20)
    top_unresolved = unresolved_counter.most_common(30)

    total_drops = (
        count_drop_unresolved_source
        + count_drop_unresolved_target
        + count_drop_self
        + count_drop_known
    )

    # -----------------------------------------------------------------------
    # Step 6: Print plan summary
    # -----------------------------------------------------------------------
    print()
    print("=" * 70)
    print("PASS 1 RELATIONSHIP CANDIDATE GENERATOR — RUN SUMMARY")
    print("=" * 70)
    print(f"  Extraction files walked:       {count_files_walked:>8,}")
    print(f"  Files with no rel. section:    {count_no_relationships_section:>8,}")
    print(f"  Total Relationships rows seen: {count_rows_seen:>8,}")
    print(f"  Drop (source unresolved):      {count_drop_unresolved_source:>8,}")
    print(f"  Drop (target unresolved):      {count_drop_unresolved_target:>8,}")
    print(f"  Drop (self-edge):              {count_drop_self:>8,}")
    print(f"  Drop (already-known edge):     {count_drop_known:>8,}")
    print(f"  Total dropped:                 {total_drops:>8,}")
    print(f"  SURVIVORS:                     {count_survivors:>8,}")
    print(f"  Chapters with ≥1 survivor:     {len(chapter_candidates):>8,}")
    print()

    print("Survivors by book:")
    for book in BOOKS:
        if args.book and book != args.book:
            continue
        cnt = book_survivors.get(book, 0)
        print(f"  {book.upper():<6} {cnt:>6,}")
    print()

    print("Top 10 source nodes by survivor count:")
    for slug, cnt in top_sources[:10]:
        print(f"  {cnt:>5,}  {slug}")
    print()

    print("Top 10 target nodes by inbound-candidate count:")
    for slug, cnt in top_targets[:10]:
        print(f"  {cnt:>5,}  {slug}")
    print()

    print("Top 10 unresolved entity names (candidates for alias/node gaps):")
    for name, cnt in top_unresolved[:10]:
        print(f"  {cnt:>5,}  {name!r}")
    print()

    if sample_survivors:
        print("Sample survivors (up to 5):")
        for s in sample_survivors[:5]:
            print(f"  chapter: {s['evidence_chapter']}")
            print(f"    source:   {s['source_slug']}")
            print(f"    target:   {s['target_slug']}")
            print(f"    relation: {s['asserted_relation']}")
            print(f"    evidence: {s['evidence_quote']}")
            print()

    # -----------------------------------------------------------------------
    # Step 7: Write outputs (--apply only)
    # -----------------------------------------------------------------------
    if not write_output:
        print("Plan mode — nothing written. Re-run with --apply to write outputs.")
        return

    run_ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # 7a. Per-chapter JSONL files
    print("Writing per-chapter candidate files...")
    files_written = 0
    total_rows_written = 0

    for chapter_slug, (book_abbrev, candidates) in sorted(chapter_candidates.items()):
        out_dir = OUT_BASE_DIR / book_abbrev
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{chapter_slug}.candidates.jsonl"
        with out_file.open("w", encoding="utf-8") as fh:
            for row in candidates:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        files_written += 1
        total_rows_written += len(candidates)

    print(f"  {files_written:,} candidate files written")
    print(f"  {total_rows_written:,} total candidate rows written")

    # 7b. Summary markdown
    print(f"Writing {OUT_SUMMARY_MD} ...")
    summary_lines = [
        "# Pass 1 Relationship Candidates Summary",
        "",
        f"Generated: {run_ts}",
        "",
        "## Counts",
        "",
        "| Stage | Count |",
        "|-------|-------|",
        f"| Extraction files walked | {count_files_walked:,} |",
        f"| Files with no Relationships Observed section | {count_no_relationships_section:,} |",
        f"| Total Relationships Observed rows seen | {count_rows_seen:,} |",
        f"| Drop: source unresolved | {count_drop_unresolved_source:,} |",
        f"| Drop: target unresolved | {count_drop_unresolved_target:,} |",
        f"| Drop: self-edge | {count_drop_self:,} |",
        f"| Drop: already-known edge | {count_drop_known:,} |",
        f"| **Survivors** | **{count_survivors:,}** |",
        f"| Chapters with ≥1 survivor | {len(chapter_candidates):,} |",
        "",
        "## Distribution by Book",
        "",
        "| Book | Survivors |",
        "|------|----------|",
    ]
    for book in BOOKS:
        cnt = book_survivors.get(book, 0)
        summary_lines.append(f"| {book.upper()} | {cnt:,} |")

    summary_lines += [
        "",
        "## Top 20 Source Nodes by Survivor Count",
        "",
        "| Source Slug | Survivor Count |",
        "|-------------|---------------|",
    ]
    for slug, cnt in top_sources:
        summary_lines.append(f"| {slug} | {cnt:,} |")

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
        "## Top 30 Unresolved Entity Names",
        "",
        "These names appeared in Relationships Observed tables but could not be",
        "resolved to a graph node. They are candidates for new nodes or alias additions.",
        "",
        "| Entity Name | Drop Count |",
        "|-------------|-----------|",
    ]
    for name, cnt in top_unresolved:
        summary_lines.append(f"| {name} | {cnt:,} |")

    summary_lines += [
        "",
        "## Sample of Up to 20 Surviving Rows",
        "",
        "| Chapter | Source | Target | Asserted Relation | Evidence |",
        "|---------|--------|--------|-------------------|---------|",
    ]
    for s in sample_survivors[:20]:
        # Truncate long fields for readability in the table
        rel = s["asserted_relation"][:80] + "..." if len(s["asserted_relation"]) > 80 else s["asserted_relation"]
        ev = s["evidence_quote"][:60] + "..." if len(s["evidence_quote"]) > 60 else s["evidence_quote"]
        summary_lines.append(
            f"| {s['evidence_chapter']} | {s['source_slug']} | {s['target_slug']} | {rel} | {ev} |"
        )

    WIKI_DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_SUMMARY_MD.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print(f"  Written: {OUT_SUMMARY_MD}")

    # 7c. Stats JSON
    print(f"Writing {OUT_SUMMARY_JSON} ...")
    stats = {
        "generated_at": run_ts,
        "counts": {
            "extraction_files_walked": count_files_walked,
            "files_no_relationships_section": count_no_relationships_section,
            "total_rows_seen": count_rows_seen,
            "drop_source_unresolved": count_drop_unresolved_source,
            "drop_target_unresolved": count_drop_unresolved_target,
            "drop_self_edge": count_drop_self,
            "drop_known_edge": count_drop_known,
            "survivors": count_survivors,
            "chapters_with_survivors": len(chapter_candidates),
        },
        "book_distribution": dict(book_survivors),
        "top_sources": [
            {"slug": slug, "survivor_count": cnt}
            for slug, cnt in top_sources
        ],
        "top_targets": [
            {"slug": slug, "inbound_count": cnt}
            for slug, cnt in top_targets
        ],
        "top_unresolved": [
            {"name": name, "drop_count": cnt}
            for name, cnt in top_unresolved
        ],
    }
    OUT_SUMMARY_JSON.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"  Written: {OUT_SUMMARY_JSON}")

    print()
    print(f"Done. {count_survivors:,} candidates written to {files_written:,} files.")
    print(f"  Output dir: {OUT_BASE_DIR}")
    print(f"  Summary:    {OUT_SUMMARY_MD}")
    print(f"  Stats:      {OUT_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
