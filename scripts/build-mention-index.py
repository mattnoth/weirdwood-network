#!/usr/bin/env python3
"""build-mention-index.py

Pass 1.7 — Per-chapter mention index (pure deterministic Python, no LLM, no HTTP).

Reads every Pass 1 extraction file under extractions/mechanical/<book>/, resolves
named entities to graph node slugs, and writes one JSON mention file per chapter
under graph/index/chapters/<book>/<chapter_id>.mentions.json.

Also writes a top-level summary to graph/index/chapters/_summary.json.

Resolution algorithm:
  1. Strip parenthetical asides, role suffixes, trailing notes.
  2. Compute slug via to_kebab().
  3. Direct lookup in graph/nodes slug index.
  4. Alias lookup via working/wiki-parsed/alias-resolver.json.
  5. Emit as unresolved if both fail — still recorded.

Sections parsed:
  Tables (col 1 = entity name):
    Characters Present, Character Appearances, Characters Referenced,
    Locations, Location Descriptions, Artifacts & Objects of Significance
  Raw Entity List (bullet lists under ### subsections):
    Characters, Locations, Houses, Factions & Organizations, Religions & Faiths,
    Cultures & Peoples, Artifacts & Objects, In-world Texts & Songs,
    Magic & Phenomena, Wars & Conflicts, Titles & Offices, Other

Usage:
    python3 scripts/build-mention-index.py [--book agot] [--all] [--dry-run]
                                           [--log path/to/log.txt]
"""

import argparse
import json
import re
import sys
import warnings
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
EXTRACTIONS_DIR = REPO_ROOT / "extractions" / "mechanical"
GRAPH_NODES_DIR = REPO_ROOT / "graph" / "nodes"
ALIAS_RESOLVER_PATH = REPO_ROOT / "working" / "wiki-parsed" / "alias-resolver.json"
INDEX_DIR = REPO_ROOT / "graph" / "index" / "chapters"
DEFAULT_LOG_PATH = REPO_ROOT / "working" / "mention-index-build-log.txt"

BOOKS = ["agot", "acok", "asos", "affc", "adwd"]

# Directories inside graph/nodes/ to skip
EXCLUDED_NODE_DIRS = {"_conflicts", "_unclassified"}

# Section headers that are pipe tables (entity name in column 1)
TABLE_SECTIONS = {
    "Characters Present",
    "Character Appearances",
    "Characters Referenced",
    "Locations",
    "Location Descriptions",
    "Artifacts & Objects of Significance",
}

# Raw Entity List subsections (bullet lists)
RAW_ENTITY_SUBSECTIONS = {
    "Characters",
    "Locations",
    "Houses",
    "Factions & Organizations",
    "Religions & Faiths",
    "Cultures & Peoples",
    "Artifacts & Objects",
    "In-world Texts & Songs",
    "Magic & Phenomena",
    "Wars & Conflicts",
    "Titles & Offices",
    "Other",
}

# Map graph/nodes/ directory names to node_type labels
DIR_TO_NODE_TYPE = {
    "characters": "character",
    "locations": "place.location",
    "houses": "organization.house",
    "factions": "organization.faction",
    "religions": "organization.religion",
    "concepts": "concept",
    "customs": "concept.custom",
    "events": "event",
    "artifacts": "object.artifact",
    "texts": "object.text",
    "foods": "object.food",
    "materials": "object.material",
    "species": "species",
    "titles": "title",
    "theories": "concept.theory",
    "prophecies": "concept.prophecy",
    "languages": "concept.language",
    "medical": "concept.medical",
}


# ---------------------------------------------------------------------------
# Slug computation — verbatim copy from wiki-pass2-build-alias-resolver.py
# ---------------------------------------------------------------------------

def to_kebab(text: str) -> str:
    """Convert an alias string to the canonical kebab slug format.

    Rules:
    1. Lowercase
    2. Strip apostrophes, quotes, commas (these merge words, not separate them)
    3. Replace spaces and underscores with hyphens
    4. Replace remaining characters not in [a-z0-9-] with hyphens
    5. Collapse runs of hyphens into single hyphen
    6. Strip leading/trailing hyphens
    """
    s = text.lower()
    s = re.sub(r"['\",]", "", s)
    s = re.sub(r"[ _]+", "-", s)
    s = re.sub(r"[^a-z0-9-]", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


# ---------------------------------------------------------------------------
# Name cleaning
# ---------------------------------------------------------------------------

# Patterns to strip from raw names before slugifying
_PAREN_RE = re.compile(r"\s*\([^)]*\)")          # (parenthetical aside)
_EMDASH_RE = re.compile(r"\s*[—–].*$")           # em-dash / en-dash trailing notes
_ROLE_SUFFIX_RE = re.compile(
    r"\s*(POV|deceased|dead|referenced|inferred|unnamed|historical|off-page|presumed dead"
    r"|historical referenced|historical figure|historical character)\s*$",
    re.IGNORECASE,
)

def clean_raw_name(raw: str) -> str:
    """Strip parentheticals, role suffixes, and trailing notes from an entity name.

    Returns the cleaned string, or empty string if the result is trivially short.
    """
    s = raw.strip()
    # Remove parenthetical asides
    s = _PAREN_RE.sub("", s)
    # Remove em-dash / en-dash trailing notes
    s = _EMDASH_RE.sub("", s)
    # Remove known role suffixes (POV, deceased, etc.) at end
    s = _ROLE_SUFFIX_RE.sub("", s)
    return s.strip()


# ---------------------------------------------------------------------------
# Graph node index
# ---------------------------------------------------------------------------

def build_node_index() -> dict[str, tuple[str, str]]:
    """Glob graph/nodes/**/*.node.md (excluding _conflicts and _unclassified).

    Returns: {slug: (node_type, relative_path_str)}
    The slug is the stem of the filename (everything before .node.md).
    """
    index: dict[str, tuple[str, str]] = {}
    for node_file in GRAPH_NODES_DIR.rglob("*.node.md"):
        # Determine the type-directory (first component after GRAPH_NODES_DIR)
        try:
            rel = node_file.relative_to(GRAPH_NODES_DIR)
        except ValueError:
            continue
        type_dir = rel.parts[0]
        if type_dir in EXCLUDED_NODE_DIRS:
            continue
        slug = node_file.name.removesuffix(".node.md")
        node_type = DIR_TO_NODE_TYPE.get(type_dir, type_dir)
        rel_path = str(node_file.relative_to(REPO_ROOT))
        if slug in index:
            # Conflict: slug appears in multiple directories — keep first seen
            pass
        else:
            index[slug] = (node_type, rel_path)
    return index


# ---------------------------------------------------------------------------
# Alias resolver
# ---------------------------------------------------------------------------

def load_alias_resolver() -> dict[str, str]:
    """Load alias_to_canonical from working/wiki-parsed/alias-resolver.json."""
    if not ALIAS_RESOLVER_PATH.exists():
        warnings.warn(f"alias-resolver.json not found at {ALIAS_RESOLVER_PATH}")
        return {}
    with ALIAS_RESOLVER_PATH.open() as f:
        data = json.load(f)
    return data.get("alias_to_canonical", {})


# ---------------------------------------------------------------------------
# Title prefix stripping (fallback before marking unresolved)
# ---------------------------------------------------------------------------

# Ordered longest-first so "grand-maester-" is tried before "maester-"
_TITLE_PREFIXES = [
    "grand-maester-",
    "maester-",
    "lord-commander-",
    "lord-",
    "lady-",
    "king-",
    "queen-",
    "prince-",
    "princess-",
    "ser-",
    "septa-",
    "septon-",
    "khal-",
    "khaleesi-",
    "the-",
    "a-",
]

def strip_title_prefix(slug: str) -> str | None:
    """Try stripping known title/honorific prefixes from a slug.

    Returns the stripped slug, or None if no prefix matched.
    """
    for prefix in _TITLE_PREFIXES:
        if slug.startswith(prefix):
            stripped = slug[len(prefix):]
            if stripped:  # don't return empty string
                return stripped
    return None


# ---------------------------------------------------------------------------
# Entity resolution
# ---------------------------------------------------------------------------

def resolve(
    raw_name: str,
    node_index: dict[str, tuple[str, str]],
    alias_map: dict[str, str],
) -> tuple[str | None, str, str | None, str | None]:
    """Resolve a raw entity name string.

    Returns: (slug, resolved_via, node_type, node_path)
    resolved_via is one of: "direct", "alias", "unresolved"
    """
    cleaned = clean_raw_name(raw_name)
    if not cleaned:
        return None, "unresolved", None, None

    slug = to_kebab(cleaned)
    if not slug:
        return None, "unresolved", None, None

    # 1. Direct lookup
    if slug in node_index:
        node_type, node_path = node_index[slug]
        return slug, "direct", node_type, node_path

    # 2. Alias lookup
    if slug in alias_map:
        canonical = alias_map[slug]
        if canonical in node_index:
            node_type, node_path = node_index[canonical]
            return canonical, "alias", node_type, node_path
        # Alias resolves to something not in the index — still record canonical
        return canonical, "alias", None, None

    # 3. Prefix-stripped direct lookup (e.g. "Ser Rodrik Cassel" -> "rodrik-cassel")
    stripped = strip_title_prefix(slug)
    if stripped is not None:
        if stripped in node_index:
            node_type, node_path = node_index[stripped]
            return stripped, "direct", node_type, node_path
        # 4. Prefix-stripped alias lookup
        if stripped in alias_map:
            canonical = alias_map[stripped]
            if canonical in node_index:
                node_type, node_path = node_index[canonical]
                return canonical, "alias", node_type, node_path
            return canonical, "alias", None, None

    return slug, "unresolved", None, None


# ---------------------------------------------------------------------------
# Extraction parsing
# ---------------------------------------------------------------------------

def parse_table_row_col1(line: str) -> str | None:
    """Extract column 1 (entity name) from a markdown pipe table row.

    Returns None for header rows, separator rows, or unparseable lines.
    """
    line = line.strip()
    if not line.startswith("|"):
        return None
    cells = [c.strip() for c in line.split("|")]
    # cells[0] is empty (before first |), cells[1] is col1
    if len(cells) < 2:
        return None
    col1 = cells[1].strip()
    if not col1:
        return None
    # Skip separator rows like |---|---|
    if re.fullmatch(r"[-:| ]+", col1):
        return None
    # Skip header rows — they typically contain the column name words
    # We detect them as rows where col1 is a known column label
    # (rough heuristic: header if it matches a known label pattern exactly)
    KNOWN_HEADERS = {
        "character", "location", "artifact", "role in chapter",
        "role", "context of reference", "context", "meal/occasion",
        "event", "type", "host", "phase", "who", "information",
        "speaker", "character a", "question", "character appearances",
        "hair", "phase",
    }
    if col1.lower() in KNOWN_HEADERS:
        return None
    return col1


def parse_bullet_line(line: str) -> str | None:
    """Extract entity name from a bullet list line.

    Handles lines starting with '- ' (markdown bullets).
    Returns None for non-bullet lines or empty entries.
    """
    stripped = line.strip()
    if not stripped.startswith("-"):
        return None
    content = stripped[1:].strip()
    if not content or content.lower() == "none":
        return None
    return content


# ---------------------------------------------------------------------------
# Extraction file parser
# ---------------------------------------------------------------------------

def parse_extraction(
    extraction_path: Path,
    node_index: dict[str, tuple[str, str]],
    alias_map: dict[str, str],
    log_lines: list[str],
) -> list[dict]:
    """Parse one extraction file and return a list of mention records.

    Each record is a dict with keys:
        raw_name, slug, resolved_via, node_type, node_path, section, line
    """
    try:
        content = extraction_path.read_text(encoding="utf-8")
    except OSError as e:
        log_lines.append(f"ERROR: cannot read {extraction_path}: {e}")
        return []

    lines = content.splitlines()
    mentions: list[dict] = []
    # Track (section, raw_name) pairs to deduplicate within a file
    seen: set[tuple[str, str]] = set()

    current_section: str | None = None
    in_raw_entity_list = False
    current_subsection: str | None = None
    in_table_section = False

    for lineno, line in enumerate(lines, start=1):
        # Detect top-level section (##)
        if line.startswith("## "):
            section_name = line[3:].strip()
            in_raw_entity_list = (section_name == "Raw Entity List")
            current_section = section_name
            current_subsection = None
            in_table_section = (section_name in TABLE_SECTIONS)
            continue

        # Detect Raw Entity List subsections (###)
        if line.startswith("### ") and in_raw_entity_list:
            current_subsection = line[4:].strip()
            continue

        # Parse table rows in table sections
        if in_table_section and "|" in line:
            col1 = parse_table_row_col1(line)
            if col1 and col1.lower() != "none":
                key = (current_section or "", col1)
                if key not in seen:
                    seen.add(key)
                    slug, resolved_via, node_type, node_path = resolve(col1, node_index, alias_map)
                    if slug:
                        mentions.append({
                            "raw_name": col1,
                            "slug": slug,
                            "resolved_via": resolved_via,
                            "node_type": node_type,
                            "node_path": node_path,
                            "section": current_section,
                            "line": lineno,
                        })
            continue

        # Parse bullet items in Raw Entity List subsections
        if in_raw_entity_list and current_subsection in RAW_ENTITY_SUBSECTIONS:
            item = parse_bullet_line(line)
            if item:
                section_label = f"Raw Entity List > {current_subsection}"
                key = (section_label, item)
                if key not in seen:
                    seen.add(key)
                    slug, resolved_via, node_type, node_path = resolve(item, node_index, alias_map)
                    if slug:
                        mentions.append({
                            "raw_name": item,
                            "slug": slug,
                            "resolved_via": resolved_via,
                            "node_type": node_type,
                            "node_path": node_path,
                            "section": section_label,
                            "line": lineno,
                        })

    return mentions


# ---------------------------------------------------------------------------
# Chapter ID extraction from filename
# ---------------------------------------------------------------------------

def chapter_id_from_path(extraction_path: Path) -> str:
    """Derive chapter_id from extraction filename.

    e.g. agot-arya-01.extraction.md -> agot-arya-01
    """
    name = extraction_path.name
    return name.removesuffix(".extraction.md")


def pov_character_from_chapter_id(chapter_id: str) -> str:
    """Extract pov_character slug from chapter_id.

    e.g. agot-arya-01 -> arya
         agot-a-ghost-in-winterfell-01 -> a-ghost-in-winterfell
    """
    # Split on first '-' (book), then find last component (chapter number)
    parts = chapter_id.split("-")
    if len(parts) < 3:
        return chapter_id
    # Remove book prefix and trailing chapter number
    # e.g. ["agot", "arya", "01"] -> "arya"
    # e.g. ["adwd", "a", "ghost", "in", "winterfell", "01"] -> "a-ghost-in-winterfell"
    book = parts[0]
    # Last part is the number (01, 02, ...)
    pov_parts = parts[1:-1]
    return "-".join(pov_parts)


# ---------------------------------------------------------------------------
# Process one chapter
# ---------------------------------------------------------------------------

def process_chapter(
    extraction_path: Path,
    book: str,
    node_index: dict[str, tuple[str, str]],
    alias_map: dict[str, str],
    log_lines: list[str],
    dry_run: bool,
) -> dict | None:
    """Parse one extraction, resolve mentions, optionally write output JSON.

    Returns the output record dict (useful for summary stats), or None on failure.
    """
    chapter_id = chapter_id_from_path(extraction_path)
    pov_character = pov_character_from_chapter_id(chapter_id)

    mentions = parse_extraction(extraction_path, node_index, alias_map, log_lines)

    direct = sum(1 for m in mentions if m["resolved_via"] == "direct")
    alias = sum(1 for m in mentions if m["resolved_via"] == "alias")
    unresolved = sum(1 for m in mentions if m["resolved_via"] == "unresolved")
    total = len(mentions)

    output = {
        "chapter_id": chapter_id,
        "book": book,
        "pov_character": pov_character,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "extraction_path": str(extraction_path.relative_to(REPO_ROOT)),
        "stats": {
            "total_mentions": total,
            "resolved_to_node": direct + alias,
            "direct": direct,
            "alias": alias,
            "unresolved": unresolved,
        },
        "mentions": mentions,
    }

    if not dry_run:
        out_dir = INDEX_DIR / book
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{chapter_id}.mentions.json"
        out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    return output


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run(books: list[str], dry_run: bool, log_path: Path) -> None:
    print(f"Building mention index for books: {', '.join(books)}")
    print(f"Dry run: {dry_run}")
    print()

    log_lines: list[str] = []

    # 1. Build node index
    print("Loading graph node index...", end=" ", flush=True)
    node_index = build_node_index()
    print(f"{len(node_index):,} nodes indexed.")

    # 2. Load alias resolver
    print("Loading alias resolver...", end=" ", flush=True)
    alias_map = load_alias_resolver()
    print(f"{len(alias_map):,} aliases loaded.")
    print()

    # 3. Process chapters
    total_chapters = 0
    total_mentions = 0
    total_direct = 0
    total_alias = 0
    total_unresolved = 0
    unresolved_counter: Counter = Counter()

    for book in books:
        book_dir = EXTRACTIONS_DIR / book
        if not book_dir.exists():
            log_lines.append(f"WARN: extraction directory not found: {book_dir}")
            print(f"  {book}: directory not found, skipping.")
            continue

        extraction_files = sorted(book_dir.glob("*.extraction.md"))
        if not extraction_files:
            log_lines.append(f"WARN: no extraction files in {book_dir}")
            print(f"  {book}: no extraction files found.")
            continue

        book_mentions = 0
        print(f"  Processing {book} ({len(extraction_files)} chapters)...")
        for ef in extraction_files:
            result = process_chapter(ef, book, node_index, alias_map, log_lines, dry_run)
            if result is None:
                continue
            total_chapters += 1
            book_mentions += result["stats"]["total_mentions"]
            total_direct += result["stats"]["direct"]
            total_alias += result["stats"]["alias"]
            total_unresolved += result["stats"]["unresolved"]
            for m in result["mentions"]:
                if m["resolved_via"] == "unresolved":
                    unresolved_counter[m["slug"]] += 1

        total_mentions += book_mentions
        print(f"    {len(extraction_files)} chapters, {book_mentions:,} mentions.")

    print()

    # 4. Compute summary stats
    resolved = total_direct + total_alias
    resolution_rate = (resolved / total_mentions * 100) if total_mentions else 0.0
    direct_pct = (total_direct / total_mentions * 100) if total_mentions else 0.0
    alias_pct = (total_alias / total_mentions * 100) if total_mentions else 0.0
    unresolved_pct = (total_unresolved / total_mentions * 100) if total_mentions else 0.0

    top_unresolved = unresolved_counter.most_common(20)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "books_processed": books,
        "dry_run": dry_run,
        "chapters_processed": total_chapters,
        "total_mentions": total_mentions,
        "resolved": resolved,
        "direct": total_direct,
        "alias": total_alias,
        "unresolved": total_unresolved,
        "resolution_rate_pct": round(resolution_rate, 1),
        "direct_pct": round(direct_pct, 1),
        "alias_pct": round(alias_pct, 1),
        "unresolved_pct": round(unresolved_pct, 1),
        "top_unresolved": [{"slug": s, "count": c} for s, c in top_unresolved],
    }

    # 5. Write summary JSON
    if not dry_run:
        INDEX_DIR.mkdir(parents=True, exist_ok=True)
        summary_path = INDEX_DIR / "_summary.json"
        summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Summary written to: {summary_path.relative_to(REPO_ROOT)}")

    # 6. Write log
    if log_lines:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("w", encoding="utf-8") as f:
            f.write(f"mention-index build log — {datetime.now(timezone.utc).isoformat()}\n")
            f.write(f"books: {', '.join(books)}\n\n")
            for line in log_lines:
                f.write(line + "\n")
        print(f"Log written to: {log_path.relative_to(REPO_ROOT)} ({len(log_lines)} warnings/errors)")
    else:
        print("No warnings or errors.")

    # 7. Print summary to stdout
    print()
    print("=" * 60)
    print("MENTION INDEX BUILD SUMMARY")
    print("=" * 60)
    print(f"  Chapters processed : {total_chapters}")
    print(f"  Total mentions     : {total_mentions:,}")
    print(f"  Resolved           : {resolved:,}  ({resolution_rate:.1f}%)")
    print(f"    Direct           : {total_direct:,}  ({direct_pct:.1f}%)")
    print(f"    Via alias        : {total_alias:,}  ({alias_pct:.1f}%)")
    print(f"  Unresolved         : {total_unresolved:,}  ({unresolved_pct:.1f}%)")
    print()
    print("Top 20 unresolved slugs (by frequency):")
    if top_unresolved:
        for rank, (slug, count) in enumerate(top_unresolved, start=1):
            print(f"  {rank:>2}. {slug:<40}  {count}")
    else:
        print("  (none)")
    print("=" * 60)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build per-chapter mention index from Pass 1 extractions."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--book",
        choices=BOOKS,
        metavar="BOOK",
        help=f"Process a single book ({', '.join(BOOKS)})",
    )
    group.add_argument(
        "--all",
        action="store_true",
        dest="all_books",
        help="Process all books (default)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse everything but don't write output files",
    )
    parser.add_argument(
        "--log",
        type=Path,
        default=DEFAULT_LOG_PATH,
        metavar="PATH",
        help=f"Log file path (default: {DEFAULT_LOG_PATH.relative_to(REPO_ROOT)})",
    )
    args = parser.parse_args()

    if args.book:
        books = [args.book]
    else:
        # Default to --all
        books = BOOKS

    run(books=books, dry_run=args.dry_run, log_path=args.log)


if __name__ == "__main__":
    main()
