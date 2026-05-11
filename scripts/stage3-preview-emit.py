#!/usr/bin/env python3
"""Spot-check Stage 3 preview emitter.

Generates Stage 3-style node files for 3 specific target nodes and writes
them to graph/nodes/_stage3-preview/ for side-by-side comparison with the
existing Stage-1 nodes. Does NOT modify any existing nodes.

Usage:
    python3 scripts/stage3-preview-emit.py

Target nodes:
    eddard-stark  (characters-house-stark-b-h)
    jon-snow      (characters-house-stark-h-p)
    house-stark   (houses-north-house-stark)

Output:
    graph/nodes/_stage3-preview/characters/eddard-stark.node.md
    graph/nodes/_stage3-preview/characters/jon-snow.node.md
    graph/nodes/_stage3-preview/houses/house-stark.node.md
"""

import html as html_module
import json
import re
import urllib.parse
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INFOBOX_DATA_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "infobox-data.jsonl"
WIKI_RAW_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
PREVIEW_DIR = PROJECT_ROOT / "graph" / "nodes" / "_stage3-preview"

# ---------------------------------------------------------------------------
# Target definitions
# ---------------------------------------------------------------------------
TARGETS = [
    {
        "page_name": "Eddard Stark",
        "slug": "eddard-stark",
        "bucket_id": "characters-house-stark-b-h",
        "confidence": "tier-1",
        "type_dir": "characters",
    },
    {
        "page_name": "Jon Snow",
        "slug": "jon-snow",
        "bucket_id": "characters-house-stark-h-p",
        "confidence": "tier-1",
        "type_dir": "characters",
    },
    {
        "page_name": "House Stark",
        "slug": "house-stark",
        "bucket_id": "houses-north-house-stark",
        "confidence": "tier-1",
        "type_dir": "houses",
    },
]

# ---------------------------------------------------------------------------
# Skeleton rendering (from wiki-pass2-emit-deterministic.py)
# ---------------------------------------------------------------------------

def wiki_url(page_name: str) -> str:
    encoded = urllib.parse.quote(page_name.replace(" ", "_"), safe="/:@!$&'()*+,;=")
    return f"https://awoiaf.westeros.org/index.php/{encoded}"


def render_edge_line(rel: dict) -> str:
    """Render one relationship dict into an edge bullet line."""
    edge_type = rel.get("edge_type", "UNKNOWN_EDGE")
    target = rel.get("target", "")
    field = rel.get("field", "")
    direction = rel.get("direction", "forward")
    qualifier = rel.get("qualifier", "")

    if direction == "reverse":
        edge_label = f"{edge_type} (reverse)"
    else:
        edge_label = edge_type

    line = f"- {edge_label}: {target} (track_b: {field})"
    if qualifier:
        line += f" [{qualifier}]"
    return line


def render_skeleton(page_name, slug, entity_type, aliases, confidence, bucket_id, relationships, infobox_found):
    url = wiki_url(page_name)

    if aliases:
        alias_items = ", ".join(f'"{a}"' for a in aliases)
        aliases_yaml = f"[{alias_items}]"
    else:
        aliases_yaml = "[]"

    lines = [
        "---",
        f'name: "{page_name}"',
        f"type: {entity_type}",
        f"slug: {slug}",
        f"aliases: {aliases_yaml}",
        f"confidence: {confidence}",
        f'wiki_source: "{url}"',
        f"bucket_id: {bucket_id}",
        "prompt_version: v1-python",
        "node_version: 1",
        "pass_origin: pass2-wiki-deterministic",
        "---",
        "",
        "## Identity",
        "",
        f"{page_name} is a {entity_type} from the AWOIAF wiki.",
        "",
        "## Edges",
        "",
    ]

    if relationships and infobox_found:
        for rel in relationships:
            lines.append(render_edge_line(rel))

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Prose extraction (from wiki-pass2-extract-prose.py)
# ---------------------------------------------------------------------------

SCHEMA_HEADING_MAP: dict[str, str] = {
    "history": "## Origins",
    "background": "## Origins",
    "prelude": "## Origins",
    "legend": "## Origins",
    "appearance and character": "## Appearances & Description",
    "character and appearance": "## Appearances & Description",
    "appearance": "## Appearances & Description",
    "character": "## Appearances & Description",
    "layout": "## Appearances & Description",
    "city": "## Appearances & Description",
    "culture": "## Culture",
    "organization": "## Organization",
    "structure": "## Organization",
    "recent events": "## Narrative Arc",
    "battle": "## Narrative Arc",
    "siege": "## Narrative Arc",
    "synopsis": "## Narrative Arc",
    "aftermath": "## Aftermath",
    "quotes": "## Quotes",
}

SKIP_HEADINGS = frozenset([
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
    href = tag.get("href", "")
    text = tag.get_text()
    if href.startswith("/index.php/"):
        page = href[len("/index.php/"):]
        from urllib.parse import unquote
        page = unquote(page)
        if "#" in page:
            page = page[: page.index("#")]
        return f"[{text}](wiki:{page})"
    return text


def _node_to_md(node, page_name: str) -> str:
    if isinstance(node, NavigableString):
        return html_module.unescape(str(node))

    if not isinstance(node, Tag):
        return ""

    name = node.name

    if name in ("table", "img", "figure", "style", "script"):
        return ""
    if name == "div" and "thumb" in node.get("class", []):
        return ""
    if name == "div" and "hatnote" in node.get("class", []):
        return ""
    if name == "div" and "toc" in node.get("class", []):
        return ""
    if name == "sup" and "reference" in node.get("class", []):
        return _convert_cite_ref(node, page_name)

    if name in ("b", "strong"):
        inner = "".join(_node_to_md(c, page_name) for c in node.children)
        inner = inner.strip()
        return f"**{inner}**" if inner else ""
    if name in ("i", "em"):
        inner = "".join(_node_to_md(c, page_name) for c in node.children)
        inner = inner.strip()
        return f"*{inner}*" if inner else ""
    if name == "a":
        href = node.get("href", "")
        if href.startswith("/index.php/"):
            return _convert_internal_link(node)
        return node.get_text()
    if name == "span":
        if "mw-editsection" in node.get("class", []):
            return ""
        return "".join(_node_to_md(c, page_name) for c in node.children)
    if name == "br":
        return "\n"

    if name == "p":
        inner = "".join(_node_to_md(c, page_name) for c in node.children)
        inner = _normalize_whitespace(inner)
        stripped = inner.strip("() \t")
        if re.match(r"^see\s+\S", stripped, re.IGNORECASE) and len(inner) < 30:
            return ""
        return inner if inner else ""

    if name in ("ul", "ol"):
        prefix = "1." if name == "ol" else "-"
        items = []
        for li in node.find_all("li", recursive=False):
            text = "".join(_node_to_md(c, page_name) for c in li.children)
            text = _normalize_whitespace(text)
            if text:
                items.append(f"{prefix} {text}")
        return "\n".join(items)

    if name == "li":
        inner = "".join(_node_to_md(c, page_name) for c in node.children)
        return _normalize_whitespace(inner)

    if name == "blockquote":
        quote_div = node.find("div", class_="templatequotetext")
        cite_div = node.find("div", class_="templatequotecite")
        if quote_div:
            body_parts = []
            for child in quote_div.children:
                if isinstance(child, Tag) and child.name == "p":
                    text = "".join(_node_to_md(c, page_name) for c in child.children)
                    text = _normalize_whitespace(text)
                    if text:
                        body_parts.append(text)
            body = "\n>\n> ".join(body_parts)
            result = f"> {body}"
            if cite_div:
                cite_text = cite_div.get_text().strip()
                if cite_text:
                    result += f"\n>\n> — {cite_text}"
            return result
        return ""

    if name in ("h2", "h3", "h4", "h5", "h6"):
        text = "".join(_node_to_md(c, page_name) for c in node.children)
        text = re.sub(r"\s*\[\s*\]\s*$", "", text).strip()
        text = re.sub(r"\[edit\]", "", text, flags=re.IGNORECASE).strip()
        return text

    # Generic container — recurse
    return "".join(_node_to_md(c, page_name) for c in node.children)


def extract_prose(page_name: str) -> str:
    """Extract prose from the wiki HTML for a page, returning markdown."""
    raw_file = WIKI_RAW_DIR / (page_name.replace(" ", "_") + ".json")
    if not raw_file.exists():
        return f"<!-- prose extraction failed: {raw_file} not found -->\n"

    try:
        data = json.loads(raw_file.read_text(encoding="utf-8"))
    except Exception as e:
        return f"<!-- prose extraction failed: {e} -->\n"

    html_str = data.get("html", "")
    if not html_str:
        return f"<!-- prose extraction failed: empty html -->\n"

    soup = BeautifulSoup(html_str, "html.parser")
    content_div = soup.find("div", class_="mw-parser-output")
    if not content_div:
        return f"<!-- prose extraction failed: no mw-parser-output div -->\n"

    # Collect sections: {schema_heading: [paragraph strings]}
    sections: dict[str, list[str]] = {}
    current_schema = None

    for child in content_div.children:
        if not isinstance(child, Tag):
            continue

        tag = child.name

        # H2 heading — decide section mapping
        if tag == "h2":
            raw_text = child.get_text()
            # Strip mw-editsection [] markers (wiki uses "[ ]" not "[edit]")
            clean = re.sub(r"\s*\[\s*\]\s*$", "", raw_text).strip()
            clean = re.sub(r"\[edit\]", "", clean, flags=re.IGNORECASE).strip()
            clean = clean.lower()
            if clean in SKIP_HEADINGS:
                current_schema = None
                continue
            # Quotes-by/about special case
            if clean.startswith("quotes"):
                current_schema = "## Quotes"
                sections.setdefault(current_schema, [])
                continue
            current_schema = SCHEMA_HEADING_MAP.get(clean)
            if current_schema:
                sections.setdefault(current_schema, [])
            continue

        # H3 under active schema — add as sub-heading
        if tag == "h3" and current_schema:
            raw_text = child.get_text()
            clean = re.sub(r"\s*\[\s*\]\s*$", "", raw_text).strip()
            clean = re.sub(r"\[edit\]", "", clean, flags=re.IGNORECASE).strip()
            if clean.lower() not in SKIP_HEADINGS:
                sections[current_schema].append(f"### {clean}")
            continue

        # Content under active schema
        if current_schema is None:
            continue

        if tag in ("p", "ul", "ol", "blockquote"):
            md = _node_to_md(child, page_name)
            if md and md.strip():
                sections[current_schema].append(md.strip())

    # Build output in schema order
    output_parts: list[str] = []
    for schema_heading in SCHEMA_ORDER:
        paras = sections.get(schema_heading)
        if not paras:
            continue
        output_parts.append(schema_heading)
        output_parts.append("")
        for para in paras:
            output_parts.append(para)
            output_parts.append("")

    return "\n".join(output_parts) if output_parts else "<!-- no prose sections found -->\n"


# ---------------------------------------------------------------------------
# Load infobox data
# ---------------------------------------------------------------------------

def load_infobox_data() -> dict[str, dict]:
    data: dict[str, dict] = {}
    with open(INFOBOX_DATA_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            data[rec["page"]] = rec
    return data


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Loading infobox data...")
    infobox_data = load_infobox_data()
    print(f"  Loaded {len(infobox_data)} infobox records")

    results = []

    for target in TARGETS:
        page_name = target["page_name"]
        slug = target["slug"]
        bucket_id = target["bucket_id"]
        confidence = target["confidence"]
        type_dir = target["type_dir"]

        print(f"\nProcessing: {page_name} ({slug})")

        # Infobox record
        infobox_rec = infobox_data.get(page_name)
        if not infobox_rec:
            print(f"  WARNING: no infobox record found for '{page_name}'")
            infobox_found = False
            entity_type = "unknown"
            aliases = []
            relationships = []
        else:
            infobox_found = True
            entity_type = infobox_rec.get("entity_type", "unknown")
            aliases = infobox_rec.get("aliases", [])
            relationships = infobox_rec.get("relationships", [])

        print(f"  entity_type: {entity_type}")
        print(f"  aliases: {aliases}")
        print(f"  relationships: {len(relationships)} edges")

        # Generate skeleton
        skeleton_md = render_skeleton(
            page_name=page_name,
            slug=slug,
            entity_type=entity_type,
            aliases=aliases,
            confidence=confidence,
            bucket_id=bucket_id,
            relationships=relationships,
            infobox_found=infobox_found,
        )

        # Extract prose
        print(f"  Extracting prose from wiki HTML...")
        prose_md = extract_prose(page_name)
        prose_len = len(prose_md.strip())
        print(f"  Prose length: {prose_len} chars")

        # Combine
        combined = skeleton_md + "\n" + prose_md

        # Write to preview directory
        out_dir = PREVIEW_DIR / type_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{slug}.node.md"
        out_path.write_text(combined, encoding="utf-8")
        print(f"  Written: {out_path}")

        results.append({
            "slug": slug,
            "page_name": page_name,
            "entity_type": entity_type,
            "edge_count": len(relationships),
            "prose_len": prose_len,
            "path": str(out_path),
        })

    # Summary
    print("\n" + "=" * 60)
    print("Stage 3 Preview Emission — Complete")
    print("=" * 60)
    for r in results:
        print(f"\n  {r['slug']}")
        print(f"    type: {r['entity_type']}")
        print(f"    edges: {r['edge_count']}")
        print(f"    prose: {r['prose_len']} chars")
        print(f"    path: {r['path']}")
    print()
    print(f"Preview directory: {PREVIEW_DIR}")
    print("  DO NOT promote these files. Review vs. existing Stage-1 nodes first.")


if __name__ == "__main__":
    main()
