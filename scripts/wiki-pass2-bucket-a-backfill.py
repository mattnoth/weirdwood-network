#!/usr/bin/env python3
"""Backfill emitter for the 138 Bucket A unpromoted wiki pages.

Bucket A = wiki pages that Pass 1 actively references but never got a graph node.
All 138 were routed to 'unknown' by the original categorizer (no infobox, no
category match). This script promotes them directly from sources/wiki/_raw/.

Three actions per slug:
  1. alias    -- redirect → existing node: add the slug as an alias to the existing file
  2. new_node -- has wiki content: emit skeleton + prose into graph/nodes/<dir>/<slug>.node.md
  3. stub     -- circular redirect / no content: emit skeleton-only stub

Usage:
  python3 scripts/wiki-pass2-bucket-a-backfill.py             # dry-run
  python3 scripts/wiki-pass2-bucket-a-backfill.py --apply     # write files
  python3 scripts/wiki-pass2-bucket-a-backfill.py -v          # verbose
"""

import argparse
import html as html_lib
import json
import os
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
WIKI_RAW_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
GRAPH_NODES_DIR = PROJECT_ROOT / "graph" / "nodes"
AUDIT_FILE = (
    PROJECT_ROOT
    / "working"
    / "audits"
    / "missing-nodes-2026-05-11"
    / "execution"
    / "missing-nodes.json"
)

WIKI_BASE_URL = "https://awoiaf.westeros.org/index.php/"

# ---------------------------------------------------------------------------
# TYPE_DIR_MAP — mirrors wiki-pass2-repromote-targeted-2.py exactly
# ---------------------------------------------------------------------------
TYPE_DIR_MAP: dict[str, str] = {
    "character.human":       "characters",
    "character.direwolf":    "characters",
    "character.dragon":      "characters",
    "character":             "characters",
    "organization.house":    "houses",
    "organization.faction":  "factions",
    "organization.cult":     "factions",
    "organization.religion": "religions",
    "organization":          "factions",
    "place.location":        "locations",
    "place.region":          "locations",
    "place.castle":          "locations",
    "place.city":            "locations",
    "place":                 "locations",
    "artifact":              "artifacts",
    "artifact.weapon":       "artifacts",
    "object":                "artifacts",
    "object.artifact":       "artifacts",
    "object.text":           "texts",
    "object.material":       "materials",
    "object.food":           "foods",
    "event.battle":          "events",
    "event.tournament":      "events",
    "event.war":             "events",
    "event":                 "events",
    "battle":                "events",
    "war":                   "events",
    "concept":               "concepts",
    "concept.culture":       "concepts",
    "concept.magic":         "concepts",
    "concept.prophecy":      "prophecies",
    "concept.theory":        "theories",
    "species":               "species",
    "title":                 "titles",
    "prophecy":              "prophecies",
    "theory":                "theories",
    "text":                  "texts",
}


def resolve_type_dir(entity_type: str) -> str:
    if entity_type in TYPE_DIR_MAP:
        return TYPE_DIR_MAP[entity_type]
    parent = entity_type.split(".")[0]
    if parent in TYPE_DIR_MAP:
        return TYPE_DIR_MAP[parent]
    return "concepts"  # safe fallback


# ---------------------------------------------------------------------------
# Category → entity_type mapping
# ---------------------------------------------------------------------------
# Priority order matters: first match wins.
CATEGORY_TYPE_RULES: list[tuple[str, str]] = [
    # Specific faction categories
    ("Slave soldiers",      "organization.faction"),
    ("Khalasars",           "organization.faction"),
    ("Spearwives",          "organization.faction"),
    ("Graces",              "organization.faction"),
    ("Drowned men",         "organization.faction"),
    # Buildings with religious association → place.location (must come before religion rules)
    ("Red temples",         "place.location"),
    ("Septries",            "place.location"),
    ("Religious buildings", "place.location"),
    # Religion (for actual religious organizations/faiths, not buildings)
    ("R'hllor",             "organization.religion"),
    ("Faith of the Seven",  "organization.religion"),
    ("Drowned God",         "organization.religion"),
    # Ships → artifact
    ("Swan ships",          "object.artifact"),
    ("Ironborn longships",  "object.artifact"),
    ("Ships of the Iron Fleet", "object.artifact"),
    ("Galleases",           "object.artifact"),
    ("House Greyjoy ships", "object.artifact"),
    ("House Targaryen ships", "object.artifact"),
    ("Redwyne fleet",       "object.artifact"),
    # Weapons / siege
    ("Thrones",             "object.artifact"),
    ("Trebuchets",          "object.artifact"),
    ("Swords",              "object.artifact"),
    ("Musical instruments", "object.artifact"),
    # Transport (palanquin, wayn, hathay)
    ("Transport",           "object.artifact"),
    # Clothing → material
    ("Clothing",            "object.material"),
    # Animals → species
    ("Pigs",                "species"),
    ("Fish",                "species"),
    ("Legendary dragons",   "species"),
    ("Ravens",              "species"),
    # Place categories
    ("Godswoods",           "place.location"),
    ("Brothels in King's Landing", "place.location"),
    ("Brothels in Braavos", "place.location"),
    ("Prisons",             "place.location"),
    ("Buildings",           "place.location"),
    ("Stairs",              "place.location"),
    ("Streets",             "place.location"),
    ("Harbors",             "place.location"),
    ("Palaces",             "place.location"),
    ("Walls",               "place.location"),
    ("Wonders Made by Man", "place.location"),
    # Region
    ("Places beyond the Wall", "place.region"),
    # Cultures
    ("Dothraki culture",    "concept.culture"),
    ("Ironborn culture",    "concept.culture"),
    ("Ghiscari culture",    "concept.culture"),
    # Prophecy
    ("Prophecy",            "concept.prophecy"),
    # Games → concept
    ("Games",               "concept"),
    ("Cannibalism",         "concept"),
    # Titles
    ("Kingsguard",          "concept"),
    ("Night's Watch",       "concept"),
]

# Per-slug overrides that take precedence over category rules
SLUG_TYPE_OVERRIDES: dict[str, str] = {
    # Location overrides (categories don't fire cleanly for these)
    "flea-bottom":               "place.location",
    "rookery":                   "place.location",
    "scribes-hearth":            "place.location",
    "wormways":                  "place.location",
    "red-temple":                "place.location",
    "septry":                    "place.location",
    "hair-shirts":               "object.material",
    # Document
    "secret-marriage-pact":      "object.text",
    "kingsmoot":                 "concept.culture",
    "night-lands":               "concept.culture",
    "spearwife":                 "concept.culture",
    "sunset-kingdoms":           "place.region",
    "sworn-brother":             "concept",
    "kneelers":                  "concept.culture",
    "southron":                  "concept.culture",
    "usurper":                   "concept",
    "wolf-blood":                "concept",
    "battle-fever":              "concept",
    "tiles":                     "concept",
    "monsters-and-maidens":      "concept",
    "cyvasse":                   "concept",
    "the-prince-that-was-promised": "concept.prophecy",
    "cannibalism":               "concept",
    "drogos-khalasar":           "organization.faction",
    "blue-graces":               "organization.faction",
    "white-graces":              "organization.faction",
    "frozen-shore":              "place.region",
    "land-of-always-winter":     "place.region",
    # Stub cases
    "queens-men":                "organization.faction",
    "valar-morghulis":           "concept",
    "valar-dohaeris":            "concept",
    "crossroads-inn":            "place.location",
    "red-waste":                 "place.region",
    "sky-cells":                 "place.location",
    "ruby-ford":                 "place.location",
    "queen-of-love-and-beauty":  "concept",
    "spears-of-the-merling-king": "place.location",
    "the-song-of-ice-and-fire":  "concept.prophecy",
    "naggas-hill":               "place.location",
    "drowned-men":               "organization.faction",
    "high-king":                 "title",
    "all-for-joffrey":           "character.human",
    "rolfe-the-dwarf":           "character.human",
    "bethany-fair-fingers":      "character.human",
    "goodwife-maerie":           "character.human",
}


def classify_type(slug: str, categories: list[str]) -> str:
    if slug in SLUG_TYPE_OVERRIDES:
        return SLUG_TYPE_OVERRIDES[slug]
    for cat, etype in CATEGORY_TYPE_RULES:
        if cat in categories:
            return etype
    # Fallbacks by slug pattern
    if any(slug.endswith(suf) for suf in ["-ship", "-galley", "-longship"]):
        return "object.artifact"
    return "concept"  # safe default


# ---------------------------------------------------------------------------
# Wiki cache helpers
# ---------------------------------------------------------------------------

def find_wiki_file(page: str) -> Path | None:
    fname = page.replace(" ", "_") + ".json"
    path = WIKI_RAW_DIR / fname
    if path.exists():
        return path
    fname2 = html_lib.unescape(fname)
    path2 = WIKI_RAW_DIR / fname2
    if path2.exists():
        return path2
    return None


def get_redirect_target(html_content: str) -> str | None:
    if "redirectMsg" not in html_content:
        return None
    m = re.search(r'redirectText.*?title="([^"]+)"', html_content, re.DOTALL)
    if m:
        return html_lib.unescape(m.group(1))
    return None


def follow_redirect(page: str, max_depth: int = 2) -> tuple[str, bool, Path | None]:
    """Follow redirect chain; returns (final_page, has_content, path)."""
    seen: set[str] = set()
    for _ in range(max_depth + 1):
        if page in seen:
            return page, False, None  # circular
        seen.add(page)
        path = find_wiki_file(page)
        if not path:
            return page, False, None
        raw = json.loads(path.read_text(encoding="utf-8"))
        html = raw.get("html", "")
        target = get_redirect_target(html)
        if target is None:
            return page, True, path  # has content
        page = target
    return page, False, None


def page_to_slug(page_name: str) -> str:
    slug = page_name.lower()
    slug = re.sub(r"['\",]", "", slug)
    slug = re.sub(r"[ _]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def wiki_url(page_name: str) -> str:
    encoded = page_name.replace(" ", "_")
    return WIKI_BASE_URL + encoded


def find_existing_node(slug: str) -> Path | None:
    for dirpath in GRAPH_NODES_DIR.iterdir():
        if not dirpath.is_dir():
            continue
        candidate = dirpath / f"{slug}.node.md"
        if candidate.exists():
            return candidate
    return None


# ---------------------------------------------------------------------------
# Prose extraction (adapted from wiki-pass2-extract-prose.py)
# ---------------------------------------------------------------------------

SCHEMA_HEADING_MAP: dict[str, str] = {
    "history":                    "## Origins",
    "background":                 "## Origins",
    "prelude":                    "## Origins",
    "legend":                     "## Origins",
    "appearance and character":   "## Appearances & Description",
    "character and appearance":   "## Appearances & Description",
    "appearance":                 "## Appearances & Description",
    "character":                  "## Appearances & Description",
    "layout":                     "## Appearances & Description",
    "city":                       "## Appearances & Description",
    "culture":                    "## Culture",
    "organization":               "## Organization",
    "structure":                  "## Organization",
    "recent events":              "## Narrative Arc",
    "battle":                     "## Narrative Arc",
    "siege":                      "## Narrative Arc",
    "synopsis":                   "## Narrative Arc",
    "aftermath":                  "## Aftermath",
    "quotes":                     "## Quotes",
}

SKIP_HEADINGS: frozenset[str] = frozenset([
    "family", "behind the scenes", "references", "external links",
    "external link", "references and notes", "contents", "members",
    "notable members", "historical members", "notes", "see also",
    "theories", "game of thrones",
])

SCHEMA_ORDER = [
    "## Origins",
    "## Culture",
    "## Organization",
    "## Appearances & Description",
    "## Narrative Arc",
    "## Aftermath",
    "## Quotes",
]


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"[ \t\r\n]+", " ", text).strip()


def _convert_cite_ref(tag: Tag, page_name: str) -> str:
    ref_id = tag.get("id", "")
    page_key = page_name.replace(" ", "_")
    if ref_id:
        return f"(wiki:{page_key}.{ref_id})"
    return ""


def _convert_internal_link(tag: Tag) -> str:
    from urllib.parse import unquote
    href = tag.get("href", "")
    text = tag.get_text()
    if href.startswith("/index.php/"):
        page = href[len("/index.php/"):]
        page = unquote(page)
        if "#" in page:
            page = page[: page.index("#")]
        return f"[{text}](wiki:{page})"
    return text


def _node_to_md(node, page_name: str) -> str:
    if isinstance(node, NavigableString):
        return html_lib.unescape(str(node))
    if not isinstance(node, Tag):
        return ""
    name = node.name

    if name in ("p", "div"):
        parts = [_node_to_md(c, page_name) for c in node.children]
        return _normalize_whitespace("".join(parts))

    if name in ("b", "strong"):
        inner = "".join(_node_to_md(c, page_name) for c in node.children)
        return f"**{inner.strip()}**"

    if name in ("i", "em"):
        inner = "".join(_node_to_md(c, page_name) for c in node.children)
        return f"*{inner.strip()}*"

    if name == "a":
        return _convert_internal_link(node)

    if name == "sup" and "reference" in node.get("class", []):
        return _convert_cite_ref(node, page_name)

    if name in ("ul", "ol"):
        items = []
        for li in node.find_all("li", recursive=False):
            text = _normalize_whitespace(
                "".join(_node_to_md(c, page_name) for c in li.children)
            )
            if text:
                items.append(f"- {text}")
        return "\n".join(items)

    if name == "li":
        inner = _normalize_whitespace(
            "".join(_node_to_md(c, page_name) for c in node.children)
        )
        return f"- {inner}" if inner else ""

    if name == "br":
        return "\n"

    if name == "span":
        return "".join(_node_to_md(c, page_name) for c in node.children)

    if name in ("table", "figure", "img", "style", "script"):
        return ""

    # Fallback: get all text
    return html_lib.unescape(node.get_text())


def _strip_edit_suffix(heading_text: str) -> str:
    return re.sub(r"\s*\[edit\]\s*$", "", heading_text)


def extract_prose(html_content: str, page_name: str) -> str:
    """Extract and render prose sections from wiki HTML."""
    soup = BeautifulSoup(html_content, "html.parser")
    main_div = soup.find("div", class_="mw-parser-output")
    if not main_div:
        return ""

    sections: dict[str, list[str]] = {h: [] for h in SCHEMA_ORDER}
    current_schema_heading: str | None = None
    current_blocks: list[str] = []

    def flush_current():
        nonlocal current_blocks
        if current_schema_heading and current_blocks:
            sections[current_schema_heading].extend(current_blocks)
        current_blocks = []

    children = list(main_div.children)
    i = 0
    while i < len(children):
        child = children[i]
        if not isinstance(child, Tag):
            i += 1
            continue

        if child.name == "h2":
            flush_current()
            # Use mw-headline span text if present (avoids picking up [edit] brackets)
            headline_span = child.find("span", class_="mw-headline")
            if headline_span:
                wiki_h2 = headline_span.get_text(strip=True)
            else:
                wiki_h2 = _strip_edit_suffix(child.get_text(strip=True)).strip()
            wiki_h2_lower = wiki_h2.lower()

            quotes_by_match = re.match(r"quotes\s+(by|about)\s+(.+)", wiki_h2_lower)
            if wiki_h2_lower in SCHEMA_HEADING_MAP:
                current_schema_heading = SCHEMA_HEADING_MAP[wiki_h2_lower]
            elif quotes_by_match:
                current_schema_heading = "## Quotes"
                current_blocks = [f"### {wiki_h2}"]
            elif wiki_h2_lower in SKIP_HEADINGS:
                current_schema_heading = None
            else:
                current_schema_heading = None
            i += 1
            continue

        if child.name == "h3" and current_schema_heading:
            headline_span = child.find("span", class_="mw-headline")
            if headline_span:
                h3_text = headline_span.get_text(strip=True)
            else:
                h3_text = _strip_edit_suffix(child.get_text(strip=True)).strip()
            current_blocks.append(f"### {h3_text}")
            i += 1
            continue

        if child.name == "h4" and current_schema_heading:
            headline_span = child.find("span", class_="mw-headline")
            if headline_span:
                h4_text = headline_span.get_text(strip=True)
            else:
                h4_text = _strip_edit_suffix(child.get_text(strip=True)).strip()
            current_blocks.append(f"#### {h4_text}")
            i += 1
            continue

        if child.name == "table" and "infobox" in child.get("class", []):
            i += 1
            continue

        if child.name == "div" and "toc" in child.get("class", []):
            i += 1
            continue

        if child.name == "div" and "thumb" in child.get("class", []):
            i += 1
            continue

        if current_schema_heading is None:
            i += 1
            continue

        md = _node_to_md(child, page_name)
        if md and md.strip():
            current_blocks.append(md.strip())
        i += 1

    flush_current()

    output_parts: list[str] = []
    for heading in SCHEMA_ORDER:
        blocks = sections.get(heading, [])
        if not blocks:
            continue
        output_parts.append(heading)
        output_parts.append("")
        for block in blocks:
            output_parts.append(block)
            output_parts.append("")

    return "\n".join(output_parts).rstrip() + "\n" if output_parts else ""


# ---------------------------------------------------------------------------
# Node rendering
# ---------------------------------------------------------------------------

def render_skeleton(
    page_name: str,
    slug: str,
    entity_type: str,
    aliases: list[str],
) -> str:
    url = wiki_url(page_name)
    if aliases:
        alias_items = ", ".join(f'"{a}"' for a in aliases)
        aliases_yaml = f"[{alias_items}]"
    else:
        aliases_yaml = "[]"

    dir_name = resolve_type_dir(entity_type)
    type_label = entity_type.split(".")[-1] if "." in entity_type else entity_type

    lines = [
        "---",
        f'name: "{page_name}"',
        f"type: {entity_type}",
        f"slug: {slug}",
        f"aliases: {aliases_yaml}",
        "confidence: tier-2",
        f'wiki_source: "{url}"',
        "bucket_id: bucket-a-backfill",
        "prompt_version: v1-python",
        "node_version: 1",
        "pass_origin: pass2-wiki-bucket-a-backfill",
        "---",
        "",
        "## Identity",
        "",
        f"{page_name} is a {type_label} from the AWOIAF wiki.",
        "",
        "## Edges",
        "",
    ]
    return "\n".join(lines)


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_path = tempfile.mkstemp(dir=path.parent, prefix=".tmp_")
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


# ---------------------------------------------------------------------------
# Alias addition
# ---------------------------------------------------------------------------

def add_alias_to_node(node_path: Path, new_alias: str, apply: bool, verbose: bool) -> bool:
    """Add new_alias to the aliases: field in node_path's frontmatter.

    Handles both inline format (aliases: ["a", "b"]) and YAML block format
    (aliases:\n  - a\n  - b).

    Returns True if the alias was added (or would be added in dry-run).
    """
    content = node_path.read_text(encoding="utf-8")

    # --- Try inline format: aliases: ["a", "b"] or aliases: [] ---
    m_inline = re.search(r'^(aliases:\s*)(\[.*?\])\s*$', content, re.MULTILINE)
    if m_inline:
        existing_yaml = m_inline.group(2)
        existing = re.findall(r'"([^"]+)"', existing_yaml)
        if new_alias in existing:
            if verbose:
                print(f"    SKIP: alias '{new_alias}' already in {node_path.name}")
            return False
        existing.append(new_alias)
        alias_items = ", ".join(f'"{a}"' for a in existing)
        new_aliases_yaml = f"[{alias_items}]"
        new_content = content[: m_inline.start(2)] + new_aliases_yaml + content[m_inline.end(2):]
        if apply:
            node_path.write_text(new_content, encoding="utf-8")
        return True

    # --- Try YAML block format: aliases:\n  - value ---
    # Matches `aliases:` optionally followed by block list items until next key
    m_block = re.search(
        r'^(aliases:)((?:\n[ \t]+-[^\n]*)*)(\n)',
        content,
        re.MULTILINE,
    )
    if m_block:
        block_body = m_block.group(2)
        # Extract existing values
        existing = re.findall(r'-\s+(.+)', block_body)
        if new_alias in existing:
            if verbose:
                print(f"    SKIP: alias '{new_alias}' already in {node_path.name}")
            return False
        new_block_body = block_body + f"\n  - {new_alias}"
        new_content = (
            content[: m_block.start(2)]
            + new_block_body
            + content[m_block.end(2):]
        )
        if apply:
            node_path.write_text(new_content, encoding="utf-8")
        return True

    # --- aliases: with no value (bare null) ---
    m_null = re.search(r'^aliases:\s*$', content, re.MULTILINE)
    if m_null:
        new_content = content[: m_null.end()] + f"\n  - {new_alias}" + content[m_null.end():]
        if apply:
            node_path.write_text(new_content, encoding="utf-8")
        return True

    if verbose:
        print(f"    WARNING: no aliases field found in {node_path.name}")
    return False


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def build_plan() -> dict:
    """Build the full action plan for all 138 Bucket A slugs."""
    with AUDIT_FILE.open(encoding="utf-8") as f:
        audit = json.load(f)
    bucket_a: list[dict] = audit["bucket_a"]

    plan = {
        "alias": [],    # (slug, target_slug, existing_path, cnt)
        "new_node": [], # (slug, canonical_page, content_path, categories, cnt)
        "stub": [],     # (slug, page, entity_type, cnt)
    }

    for item in bucket_a:
        slug = item["slug"]
        page = item["page"]
        cats = item["categories"]
        cnt = item["pass1_mention_count"]

        path = find_wiki_file(page)
        if not path:
            plan["stub"].append((slug, page, classify_type(slug, cats), cnt))
            continue

        raw = json.loads(path.read_text(encoding="utf-8"))
        html = raw.get("html", "")

        if "redirectMsg" not in html:
            # Content page
            existing = find_existing_node(slug)
            if existing:
                # Already promoted under the same slug — skip
                pass
            else:
                plan["new_node"].append((slug, page, path, cats, cnt))
        else:
            # Redirect page — follow chain
            canonical_page, has_content, canonical_path = follow_redirect(page)

            # Special case: old-gods → alias to old-gods-of-the-forest
            if slug == "old-gods" and not has_content:
                existing = find_existing_node("old-gods-of-the-forest")
                if existing:
                    plan["alias"].append((slug, "old-gods-of-the-forest", existing, cnt))
                    continue
                # Fallback to stub
                plan["stub"].append((slug, page, classify_type(slug, cats), cnt))
                continue

            if has_content:
                canonical_slug = page_to_slug(canonical_page)
                existing = find_existing_node(canonical_slug)
                if existing:
                    plan["alias"].append((slug, canonical_slug, existing, cnt))
                else:
                    plan["new_node"].append((slug, canonical_page, canonical_path, cats, cnt))
            else:
                # Circular redirect or missing target — check original slug first
                existing = find_existing_node(slug)
                if existing:
                    pass  # already in graph
                else:
                    plan["stub"].append((slug, page, classify_type(slug, cats), cnt))

    return plan


def run(apply: bool, verbose: bool) -> None:
    mode = "APPLY" if apply else "DRY-RUN"
    print(f"=== wiki-pass2-bucket-a-backfill.py [{mode}] ===\n")

    plan = build_plan()
    alias_cases = plan["alias"]
    new_node_cases = plan["new_node"]
    stub_cases = plan["stub"]

    total = len(alias_cases) + len(new_node_cases) + len(stub_cases)
    print(f"Plan:")
    print(f"  Alias additions:     {len(alias_cases)}")
    print(f"  New nodes (prose):   {len(new_node_cases)}")
    print(f"  New stubs:           {len(stub_cases)}")
    print(f"  Total:               {total}")
    print()

    stats = Counter()

    # --- 1. Alias additions ---
    print(f"--- Alias additions ({len(alias_cases)}) ---")
    for slug, target_slug, existing_path, cnt in sorted(alias_cases, key=lambda x: -x[3]):
        added = add_alias_to_node(existing_path, slug, apply=apply, verbose=verbose)
        if added:
            stats["aliases_added"] += 1
            if verbose:
                print(f"  + alias '{slug}' → {existing_path.relative_to(GRAPH_NODES_DIR)} [{cnt} mentions]")
        else:
            stats["aliases_skipped"] += 1
    print(f"  Added: {stats['aliases_added']}, Skipped (already present): {stats['aliases_skipped']}")
    print()

    # --- 2. New nodes ---
    print(f"--- New nodes ({len(new_node_cases)}) ---")
    for slug, canon_page, content_path, cats, cnt in sorted(new_node_cases, key=lambda x: -x[4]):
        entity_type = classify_type(slug, cats)
        dir_name = resolve_type_dir(entity_type)
        dest = GRAPH_NODES_DIR / dir_name / f"{slug}.node.md"

        if dest.exists():
            stats["new_node_skipped"] += 1
            if verbose:
                print(f"  SKIP (exists): {slug}")
            continue

        skeleton = render_skeleton(
            page_name=canon_page,
            slug=slug,
            entity_type=entity_type,
            aliases=[],
        )

        # Extract prose from wiki HTML
        raw = json.loads(content_path.read_text(encoding="utf-8"))
        html_content = raw.get("html", "")
        prose = extract_prose(html_content, canon_page) if html_content else ""

        # Combine
        if prose:
            node_content = skeleton + "\n" + prose
        else:
            node_content = skeleton + "\n"

        if apply:
            atomic_write(dest, node_content)
        stats["new_nodes_written"] += 1
        if verbose:
            prose_label = f" +{len(prose)} prose chars" if prose else " (skeleton only)"
            print(f"  + {slug} → {dir_name}/ [{entity_type}]{prose_label} [{cnt} mentions]")

    print(f"  Written: {stats['new_nodes_written']}, Skipped (exists): {stats['new_node_skipped']}")
    print()

    # --- 3. Stubs ---
    print(f"--- Stub nodes ({len(stub_cases)}) ---")
    for slug, page, entity_type, cnt in sorted(stub_cases, key=lambda x: -x[3]):
        dir_name = resolve_type_dir(entity_type)
        dest = GRAPH_NODES_DIR / dir_name / f"{slug}.node.md"

        if dest.exists():
            stats["stub_skipped"] += 1
            if verbose:
                print(f"  SKIP (exists): {slug}")
            continue

        # Use a display name derived from the slug
        display_name = slug.replace("-", " ").title()
        skeleton = render_skeleton(
            page_name=display_name,
            slug=slug,
            entity_type=entity_type,
            aliases=[],
        )
        node_content = skeleton + "\n"

        if apply:
            atomic_write(dest, node_content)
        stats["stubs_written"] += 1
        if verbose:
            print(f"  + {slug} → {dir_name}/ [{entity_type}] [{cnt} mentions] (stub)")

    print(f"  Written: {stats['stubs_written']}, Skipped (exists): {stats['stub_skipped']}")
    print()

    # --- Summary ---
    print("=== SUMMARY ===")
    total_written = (
        stats["aliases_added"]
        + stats["new_nodes_written"]
        + stats["stubs_written"]
    )
    total_skipped = (
        stats["aliases_skipped"]
        + stats["new_node_skipped"]
        + stats["stub_skipped"]
    )
    print(f"Total changes: {total_written}")
    print(f"  Alias additions:  {stats['aliases_added']}")
    print(f"  New nodes:        {stats['new_nodes_written']}")
    print(f"  Stubs:            {stats['stubs_written']}")
    print(f"Total skipped:    {total_skipped}")
    if not apply:
        print("\n[dry-run] No files written. Rerun with --apply to execute.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply", action="store_true", help="Write files (default: dry-run)"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose per-item output"
    )
    args = parser.parse_args()
    run(apply=args.apply, verbose=args.verbose)


if __name__ == "__main__":
    main()
