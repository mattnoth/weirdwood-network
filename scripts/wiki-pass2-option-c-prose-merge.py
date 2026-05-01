#!/usr/bin/env python3
"""Option C — Stage-1 character node prose-only re-emission.

For each of the 596 Stage-1 character nodes (prompt_version: v1) in
graph/nodes/characters/, this script:

  1. Reads the existing node file.
  2. Splits it into:
       - Frontmatter block (preserved verbatim, with node_version bumped 1→2)
       - Everything from "## Edges" to EOF (preserved byte-identical)
  3. Looks up the wiki page name from the wiki_source frontmatter field.
  4. Extracts fresh Stage-3 prose from sources/wiki/_raw/<Page_Name>.json
     using the same deterministic logic as wiki-pass2-extract-prose.py.
  5. Writes: frontmatter + "\\n" + stage3-prose + "\\n" + edges-tail
     via atomic rename (write to .tmp, then os.rename).

NEVER modifies the ## Edges section. Frontmatter is unchanged except
node_version: 1 → 2 to mark hybrid-origin nodes.

Nodes where the wiki page has no extractable prose are skipped and logged
to working/wiki-pass2/option-c-skipped-no-prose.jsonl.

Nodes where ## Notes appears BEFORE ## Edges (4 known edge cases) are
logged as warnings — their Notes content will be dropped when the prose
section replaces everything above ## Edges.

Usage:
    python3 scripts/wiki-pass2-option-c-prose-merge.py           # dry-run
    python3 scripts/wiki-pass2-option-c-prose-merge.py --apply   # write files
    python3 scripts/wiki-pass2-option-c-prose-merge.py -v        # verbose
    python3 scripts/wiki-pass2-option-c-prose-merge.py --slug eddard-stark --apply
"""

import argparse
import html as html_module
import json
import os
import re
import statistics
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

from bs4 import BeautifulSoup, NavigableString, Tag

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
WIKI_RAW_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
GRAPH_CHARS_DIR = PROJECT_ROOT / "graph" / "nodes" / "characters"
SKIP_LOG_PATH = PROJECT_ROOT / "working" / "wiki-pass2" / "option-c-skipped-no-prose.jsonl"
SUMMARY_PATH = PROJECT_ROOT / "working" / "wiki-pass2" / "option-c-summary.json"

# Cargyll twin slugs — manually fixed YAML aliases, must not be touched
CARGYLL_PROTECTED = frozenset(["arryk-cargyll", "erryk-cargyll"])

# ---------------------------------------------------------------------------
# H2 heading mapping (copied verbatim from wiki-pass2-extract-prose.py)
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

SKIP_HEADINGS: frozenset[str] = frozenset([
    "family",
    "behind the scenes",
    "references",
    "external links",
    "external link",
    "references and notes",
    "contents",
    "members",
    "notable members",
    "historical members",
    "notes",
    "see also",
    "theories",
    "game of thrones",
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


# ---------------------------------------------------------------------------
# Slug utilities
# ---------------------------------------------------------------------------

def page_to_slug(page_name: str) -> str:
    """Convert a wiki page name to a filesystem slug."""
    slug = page_name.lower()
    slug = re.sub(r"['\",]", "", slug)
    slug = re.sub(r"[ _]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def wiki_url_to_page_name(wiki_source: str) -> str | None:
    """Extract page name from a wiki URL like https://awoiaf.westeros.org/index.php/Eddard_Stark."""
    match = re.search(r"/index\.php/(.+)$", wiki_source)
    if not match:
        return None
    page_name = unquote(match.group(1)).replace("_", " ")
    return page_name


# ---------------------------------------------------------------------------
# HTML → Markdown conversion helpers (copied from wiki-pass2-extract-prose.py)
# ---------------------------------------------------------------------------

def raw_file_path(page_name: str) -> Path:
    """Return the local cache path for a wiki page."""
    filename = page_name.replace(" ", "_") + ".json"
    return WIKI_RAW_DIR / filename


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
        page = unquote(page)
        if "#" in page:
            page = page[: page.index("#")]
        return f"[{text}](wiki:{page})"
    return text


def _node_to_md(node, page_name: str) -> str:
    """Recursively convert a BeautifulSoup node to markdown text."""
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
            result = f"> {body}" if body else ""
            if cite_div and result:
                cite_tag = cite_div.find("cite")
                if cite_tag:
                    cite_text = "".join(
                        _node_to_md(c, page_name) for c in cite_tag.children
                    )
                else:
                    cite_text = "".join(
                        _node_to_md(c, page_name) for c in cite_div.children
                    )
                cite_text = _normalize_whitespace(cite_text)
                if cite_text:
                    result += f"\n>\n> {cite_text}"
            return result
        inner = "".join(_node_to_md(c, page_name) for c in node.children)
        inner = _normalize_whitespace(inner)
        return f"> {inner}" if inner else ""

    if name == "dl":
        lines = []
        for dd in node.find_all("dd", recursive=False):
            hatnote = dd.find("div", class_="hatnote")
            if hatnote:
                continue
            text = "".join(_node_to_md(c, page_name) for c in dd.children)
            text = _normalize_whitespace(text)
            if text:
                lines.append(f"> {text}")
        return "\n".join(lines)

    if name == "dd":
        inner = "".join(_node_to_md(c, page_name) for c in node.children)
        return _normalize_whitespace(inner)

    if name in ("h3", "h4"):
        inner = "".join(_node_to_md(c, page_name) for c in node.children)
        inner = _normalize_whitespace(inner)
        prefix = "###" if name == "h3" else "####"
        return f"{prefix} {inner}"

    if name == "div":
        return "".join(_node_to_md(c, page_name) for c in node.children)

    return "".join(_node_to_md(c, page_name) for c in node.children)


def _strip_edit_suffix(heading_text: str) -> str:
    return re.sub(r"\s*\[\s*\]\s*$", "", heading_text).strip()


# ---------------------------------------------------------------------------
# Section extraction (copied from wiki-pass2-extract-prose.py)
# ---------------------------------------------------------------------------

def extract_sections(soup: BeautifulSoup, page_name: str) -> tuple[dict[str, list[str]], Counter]:
    main_div = soup.find("div", class_="mw-parser-output")
    if not main_div:
        return {}, Counter()

    sections: dict[str, list[str]] = {h: [] for h in SCHEMA_ORDER}
    unmapped: Counter = Counter()

    children = list(main_div.children)
    current_schema_heading: str | None = None
    current_blocks: list[str] = []

    def flush_current():
        nonlocal current_blocks
        if current_schema_heading and current_blocks:
            sections[current_schema_heading].extend(current_blocks)
        current_blocks = []

    i = 0
    while i < len(children):
        child = children[i]

        if not isinstance(child, Tag):
            i += 1
            continue

        if child.name == "h2":
            flush_current()
            raw_text = child.get_text(strip=True)
            wiki_h2 = _strip_edit_suffix(raw_text).strip()
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
                unmapped[wiki_h2] += 1
                current_schema_heading = None

            i += 1
            continue

        if child.name == "h3" and current_schema_heading:
            raw_text = child.get_text(strip=True)
            h3_text = _strip_edit_suffix(raw_text).strip()
            current_blocks.append(f"### {h3_text}")
            i += 1
            continue

        if child.name == "h4" and current_schema_heading:
            raw_text = child.get_text(strip=True)
            h4_text = _strip_edit_suffix(raw_text).strip()
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
    return sections, unmapped


def render_prose(sections: dict[str, list[str]]) -> str:
    """Render extracted sections into a prose markdown string."""
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

    if not output_parts:
        return ""

    content = "\n".join(output_parts)
    content = re.sub(r"\n{3,}", "\n\n", content)
    if not content.endswith("\n"):
        content += "\n"
    return content


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

def split_node_file(text: str) -> tuple[str, str, str] | None:
    """Split a node file into (frontmatter_block, prose_body, edges_tail).

    frontmatter_block: the raw '---\\n...\\n---\\n' block (may or may not
                       include a trailing newline — we preserve the raw bytes).
    prose_body:        everything between frontmatter and '## Edges'
    edges_tail:        '## Edges' through EOF (preserved verbatim).

    Returns None if the file does not have the expected structure.
    """
    if not text.startswith("---\n"):
        return None

    # Find the closing '---'
    end_fm = text.find("\n---\n", 4)
    if end_fm == -1:
        return None

    frontmatter_block = text[: end_fm + 5]  # includes trailing newline after '---'
    after_fm = text[end_fm + 5:]

    # Find ## Edges
    edges_marker = "\n## Edges\n"
    edges_pos = after_fm.find(edges_marker)
    if edges_pos == -1:
        # Try at start of string (no preceding newline)
        if after_fm.startswith("## Edges\n"):
            edges_pos = -1  # special case
            prose_body = ""
            edges_tail = after_fm
            return frontmatter_block, prose_body, edges_tail
        return None

    prose_body = after_fm[: edges_pos + 1]  # +1 to include the leading newline
    edges_tail = after_fm[edges_pos + 1:]   # starts with '## Edges\n'

    return frontmatter_block, prose_body, edges_tail


def extract_frontmatter_fields(frontmatter_block: str) -> dict[str, str]:
    """Extract key: value pairs from the YAML frontmatter block.

    Does not attempt full YAML parsing — extracts simple scalar fields only.
    Returns a dict of {field_name: raw_value_string}.
    """
    fields: dict[str, str] = {}
    # Strip the '---' delimiters
    content = frontmatter_block.strip()
    if content.startswith("---"):
        content = content[3:]
    if content.endswith("---"):
        content = content[:-3]
    for line in content.splitlines():
        m = re.match(r'^(\w[\w_]*):\s*(.*)', line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def bump_node_version(frontmatter_block: str) -> str:
    """Replace 'node_version: 1' with 'node_version: 2' in the frontmatter block."""
    return re.sub(r'^(node_version:\s*)1(\s*)$', r'\g<1>2\g<2>', frontmatter_block, flags=re.MULTILINE)


# ---------------------------------------------------------------------------
# Notes-before-Edges detection
# ---------------------------------------------------------------------------

def has_notes_before_edges(prose_body: str) -> bool:
    """Return True if the prose body contains a ## Notes section."""
    return "\n## Notes\n" in prose_body or prose_body.startswith("## Notes\n")


# ---------------------------------------------------------------------------
# Per-node processing
# ---------------------------------------------------------------------------

def process_node(
    node_path: Path,
    apply: bool,
    verbose: bool,
) -> dict:
    """Process one Stage-1 character node.

    Returns a result dict with fields:
      slug, status, prose_chars_before, prose_chars_after, edge_lines_before,
      edge_lines_after, warning (optional)
    """
    slug = node_path.stem.replace(".node", "")
    result: dict = {"slug": slug, "status": "unknown"}

    # Cargyll protection
    if slug in CARGYLL_PROTECTED:
        result["status"] = "skipped_cargyll_protected"
        return result

    # Read file
    try:
        text = node_path.read_text(encoding="utf-8")
    except OSError as e:
        result["status"] = "error_read"
        result["error"] = str(e)
        return result

    # Split into frontmatter / prose_body / edges_tail
    parts = split_node_file(text)
    if parts is None:
        result["status"] = "error_parse"
        result["error"] = "Could not parse frontmatter/Edges split"
        return result

    frontmatter_block, prose_body, edges_tail = parts

    # Extract wiki_source → page_name
    fields = extract_frontmatter_fields(frontmatter_block)
    wiki_source = fields.get("wiki_source", "").strip('"\'')
    if not wiki_source:
        result["status"] = "skipped_no_wiki_source"
        return result

    page_name = wiki_url_to_page_name(wiki_source)
    if not page_name:
        result["status"] = "skipped_bad_wiki_source"
        result["wiki_source"] = wiki_source
        return result

    # Locate raw HTML cache
    raw_path = raw_file_path(page_name)
    if not raw_path.exists():
        result["status"] = "skipped_no_html_cache"
        result["page_name"] = page_name
        return result

    # Parse HTML and extract prose
    try:
        raw_json = json.loads(raw_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        result["status"] = "error_html_parse"
        result["error"] = str(e)
        return result

    html_str = raw_json.get("html", "")
    soup = BeautifulSoup(html_str, "html.parser")
    sections, unmapped = extract_sections(soup, page_name)
    prose_content = render_prose(sections)

    if not prose_content.strip():
        result["status"] = "skipped_no_prose"
        result["page_name"] = page_name
        return result

    # Measure before/after
    prose_chars_before = len(prose_body)
    prose_chars_after = len(prose_content)
    edge_lines_before = len([l for l in edges_tail.splitlines() if l.startswith("- ")])

    # Warn about Notes-before-Edges case
    notes_warning = None
    if has_notes_before_edges(prose_body):
        notes_warning = (
            f"WARNING: {slug} has ## Notes before ## Edges — "
            "Notes content will be dropped in prose replacement."
        )
        result["warning"] = notes_warning

    # Bump node_version 1 → 2
    new_frontmatter = bump_node_version(frontmatter_block)

    # Build new file content
    # Structure: frontmatter + "\n" + prose_content + "\n" + edges_tail
    # prose_content already ends with "\n"; edges_tail starts with "## Edges\n"
    new_text = new_frontmatter + "\n" + prose_content + "\n" + edges_tail

    result.update({
        "status": "processed",
        "page_name": page_name,
        "prose_chars_before": prose_chars_before,
        "prose_chars_after": prose_chars_after,
        "edge_lines_before": edge_lines_before,
        "edge_lines_after": len([l for l in edges_tail.splitlines() if l.startswith("- ")]),
        "unmapped_sections": dict(unmapped),
    })

    if notes_warning and verbose:
        print(f"  {notes_warning}", file=sys.stderr)

    if verbose:
        ratio = prose_chars_after / max(prose_chars_before, 1)
        print(
            f"  {slug:50s}  prose: {prose_chars_before:5d} → {prose_chars_after:6d} "
            f"(×{ratio:.1f})  edges: {edge_lines_before}"
        )

    if apply:
        # Atomic rename: write to .tmp then rename
        tmp_path = node_path.with_suffix(".tmp")
        try:
            tmp_path.write_text(new_text, encoding="utf-8")
            os.rename(tmp_path, node_path)
        except OSError as e:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)
            result["status"] = "error_write"
            result["error"] = str(e)

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        default=False,
        help="Write updated node files. Without --apply, prints stats only (dry-run).",
    )
    parser.add_argument(
        "--slug",
        metavar="SLUG",
        default=None,
        help="Process a single node by slug (e.g., eddard-stark).",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Print per-node stats.",
    )
    args = parser.parse_args()

    mode_label = "APPLY" if args.apply else "DRY-RUN"
    print(f"\n=== Option C: Stage-1 character prose merge [{mode_label}] ===")

    # Discover Stage-1 character nodes
    if args.slug:
        node_path = GRAPH_CHARS_DIR / f"{args.slug}.node.md"
        if not node_path.exists():
            print(f"ERROR: Node not found: {node_path}", file=sys.stderr)
            sys.exit(1)
        # Still verify it's Stage-1
        text = node_path.read_text(encoding="utf-8")
        if "prompt_version: v1\n" not in text:
            print(
                f"WARNING: {args.slug} does not appear to be a Stage-1 node "
                "(prompt_version: v1 not found). Processing anyway.",
                file=sys.stderr,
            )
        candidate_paths = [node_path]
    else:
        all_paths = sorted(GRAPH_CHARS_DIR.glob("*.node.md"))
        candidate_paths = []
        for p in all_paths:
            try:
                text = p.read_text(encoding="utf-8")
            except OSError:
                continue
            if "prompt_version: v1\n" in text:
                candidate_paths.append(p)

    print(f"Stage-1 character nodes found: {len(candidate_paths)}")
    if not args.apply:
        print("(dry-run — no files will be written)")

    # Process nodes
    results: list[dict] = []
    for node_path in candidate_paths:
        result = process_node(node_path, apply=args.apply, verbose=args.verbose)
        results.append(result)

    # Aggregate stats
    processed = [r for r in results if r["status"] == "processed"]
    skipped_no_prose = [r for r in results if r["status"] == "skipped_no_prose"]
    skipped_other = [r for r in results if r["status"] not in ("processed", "skipped_no_prose") and not r["status"].startswith("error")]
    errors = [r for r in results if r["status"].startswith("error")]
    warnings = [r for r in results if "warning" in r]
    protected = [r for r in results if r["status"] == "skipped_cargyll_protected"]

    print()
    print(f"Total scanned:           {len(results)}")
    print(f"Processed (prose merged): {len(processed)}")
    print(f"Skipped (no prose):      {len(skipped_no_prose)}")
    print(f"Skipped (other):         {len(skipped_other)}")
    print(f"Protected (Cargyll):     {len(protected)}")
    print(f"Errors:                  {len(errors)}")
    print(f"Warnings (Notes drop):   {len(warnings)}")

    if processed:
        before_lens = [r["prose_chars_before"] for r in processed]
        after_lens = [r["prose_chars_after"] for r in processed]
        mean_before = sum(before_lens) / len(before_lens)
        mean_after = sum(after_lens) / len(after_lens)
        median_before = statistics.median(before_lens)
        median_after = statistics.median(after_lens)
        total_edges_before = sum(r["edge_lines_before"] for r in processed)
        total_edges_after = sum(r["edge_lines_after"] for r in processed)

        print()
        print("Prose length stats (chars):")
        print(f"  Mean before:   {mean_before:8.0f}")
        print(f"  Mean after:    {mean_after:8.0f}  (×{mean_after/max(mean_before,1):.1f})")
        print(f"  Median before: {median_before:8.0f}")
        print(f"  Median after:  {median_after:8.0f}  (×{median_after/max(median_before,1):.1f})")
        print()
        print(f"Edge count before: {total_edges_before}")
        print(f"Edge count after:  {total_edges_after}  (diff: {total_edges_after - total_edges_before:+d})")

    if warnings:
        print()
        print("Nodes with ## Notes before ## Edges (Notes will be dropped):")
        for r in warnings:
            print(f"  - {r['slug']}")

    if errors:
        print()
        print("Errors:")
        for r in errors:
            print(f"  - {r['slug']}: {r['status']} — {r.get('error', '')}")

    if skipped_other:
        print()
        print("Other skips:")
        for r in skipped_other:
            print(f"  - {r['slug']}: {r['status']}")

    # Log skipped-no-prose to JSONL
    if args.apply and skipped_no_prose:
        SKIP_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with SKIP_LOG_PATH.open("w", encoding="utf-8") as f:
            for r in skipped_no_prose:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"\nSkip log: {SKIP_LOG_PATH}")

    # Write summary JSON
    if args.apply:
        summary = {
            "version": "v1",
            "ran_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "mode": "apply",
            "total_scanned": len(results),
            "processed": len(processed),
            "skipped_no_prose": len(skipped_no_prose),
            "skipped_other": len(skipped_other),
            "protected_cargyll": len(protected),
            "errors": len(errors),
            "warnings_notes_drop": len(warnings),
            "prose_mean_chars_before": round(mean_before, 0) if processed else 0,
            "prose_mean_chars_after": round(mean_after, 0) if processed else 0,
            "prose_median_chars_before": float(median_before) if processed else 0,
            "prose_median_chars_after": float(median_after) if processed else 0,
            "total_edges_before": total_edges_before if processed else 0,
            "total_edges_after": total_edges_after if processed else 0,
        }
        SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
        SUMMARY_PATH.write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Summary written to: {SUMMARY_PATH}")

    # Slug regression check: grep for any slug values ending in '.node'
    if args.apply and processed:
        print()
        slug_regression = 0
        for p in GRAPH_CHARS_DIR.glob("*.node.md"):
            text = p.read_text(encoding="utf-8")
            if re.search(r'^slug:.*\.node\b', text, re.MULTILINE):
                slug_regression += 1
                print(f"  SLUG REGRESSION: {p.name}")
        if slug_regression == 0:
            print("Slug regression check: PASS (0 nodes with slug ending in .node)")
        else:
            print(f"Slug regression check: FAIL ({slug_regression} node(s) with bad slug)")

    print("=" * 60)


if __name__ == "__main__":
    main()
