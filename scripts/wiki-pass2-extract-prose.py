#!/usr/bin/env python3
"""Stage 3b: Deterministic prose extractor for Wiki Pass 2.

Reads every secondary-tier bucket manifest, extracts Tier A and Tier B pages
(skips Tier C entirely), and writes one prose file per page to:
  working/wiki-pass2/<bucket_id>/prose/<slug>.prose.md

Prose is extracted from the locally cached wiki HTML at:
  sources/wiki/_raw/<Page_Name>.json

The slug is determined by reading the matching skeleton filename from
  working/wiki-pass2/<bucket_id>/skeleton/
to guarantee byte-perfect slug consistency with Stage 3a.

No HTTP calls. No agent involvement. No writes outside the prose/ directory.
Idempotent: re-running --apply twice produces byte-identical output.

H2 → schema heading mapping
-----------------------------
  History                          → ## Origins
  Background                       → ## Origins
  Prelude                          → ## Origins  (battle pages)
  Legend                           → ## Origins  (mythical/legendary entities)
  Appearance and Character         → ## Appearances & Description
  Appearance / Character           → ## Appearances & Description
  Character and Appearance         → ## Appearances & Description
  Layout                           → ## Appearances & Description  (location pages)
  City                             → ## Appearances & Description  (location pages)
  Culture                          → ## Culture
  Organization / Structure         → ## Organization
  Recent Events                    → ## Narrative Arc
  Battle                           → ## Narrative Arc  (battle pages)
  Siege                            → ## Narrative Arc  (battle pages)
  Synopsis                         → ## Narrative Arc  (battle pages)
  Aftermath                        → ## Aftermath  (battle outcome and consequences)
  Quotes                           → ## Quotes
  Quotes by <X>                    → ## Quotes  (with ### Quotes by <X> sub)
  Quotes about <X>                 → ## Quotes  (with ### Quotes about <X> sub)
  Family, Behind the Scenes,
    References, External Links,
    Contents, Members,
    Notable Members, Notes         → skipped entirely

Usage:
  python3 scripts/wiki-pass2-extract-prose.py             # dry-run
  python3 scripts/wiki-pass2-extract-prose.py --apply     # write files
  python3 scripts/wiki-pass2-extract-prose.py --bucket houses-other-h-w
  python3 scripts/wiki-pass2-extract-prose.py --bucket houses-other-h-w --apply
  python3 scripts/wiki-pass2-extract-prose.py -v          # verbose per-page
"""

import argparse
import html as html_module
import json
import re
import statistics
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
WIKI_RAW_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
WIKI_PASS2_DIR = PROJECT_ROOT / "working" / "wiki-pass2"
STAGE3B_SUMMARY_FILE = (
    PROJECT_ROOT / "working" / "wiki-parsed" / "stage3b-extraction-summary.json"
)

# ---------------------------------------------------------------------------
# H2 heading mapping table
# ---------------------------------------------------------------------------
# Keys are lowercased, [edit] stripped. Values are our schema headings.
# Order matters for the "Quotes by/about" special cases (checked separately).

SCHEMA_HEADING_MAP: dict[str, str] = {
    # Origins — what came before / history / myth
    "history": "## Origins",
    "background": "## Origins",
    "prelude": "## Origins",
    "legend": "## Origins",
    # Appearances & Description — physical description and layout
    "appearance and character": "## Appearances & Description",
    "character and appearance": "## Appearances & Description",
    "appearance": "## Appearances & Description",
    "character": "## Appearances & Description",
    "layout": "## Appearances & Description",
    "city": "## Appearances & Description",
    # Culture / Organization
    "culture": "## Culture",
    "organization": "## Organization",
    "structure": "## Organization",
    # Narrative Arc — the events themselves (battles, sieges, summaries)
    "recent events": "## Narrative Arc",
    "battle": "## Narrative Arc",
    "siege": "## Narrative Arc",
    "synopsis": "## Narrative Arc",
    # Aftermath — what followed (battle outcome, consequences)
    "aftermath": "## Aftermath",
    # Quotes
    "quotes": "## Quotes",
}

# Headings to skip silently (no unmapped counter bump)
SKIP_HEADINGS: frozenset[str] = frozenset(
    [
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
        "theories",           # speculation — intentionally excluded
        "game of thrones",    # TV show content — excluded
    ]
)

# Schema heading emit order (controls output section order)
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
    """Convert a wiki page name to a filesystem slug.

    Matches the convention in wiki-pass2-triage.py and wiki-pass2-emit-deterministic.py.
    """
    slug = page_name.lower()
    slug = re.sub(r"['\",]", "", slug)
    slug = re.sub(r"[ _]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def find_skeleton_slug(skeleton_dir: Path, page_name: str) -> str | None:
    """Return the slug by reading the matching skeleton filename.

    We reuse the skeleton filename rather than recomputing to guarantee
    byte-identical slug matching with Stage 3a output.
    """
    expected = page_to_slug(page_name)
    candidate = skeleton_dir / f"{expected}.node.md"
    if candidate.exists():
        return expected
    # Fallback: scan directory for any file whose slug matches
    if skeleton_dir.exists():
        for path in skeleton_dir.iterdir():
            if path.suffix == ".md" and path.stem == expected:
                return path.stem
    return None


# ---------------------------------------------------------------------------
# HTML → Markdown conversion helpers
# ---------------------------------------------------------------------------

def raw_file_path(page_name: str) -> Path:
    """Return the local cache path for a wiki page (spaces → underscores)."""
    filename = page_name.replace(" ", "_") + ".json"
    return WIKI_RAW_DIR / filename


def _normalize_whitespace(text: str) -> str:
    """Collapse internal whitespace runs; preserve no leading/trailing space."""
    return re.sub(r"[ \t\r\n]+", " ", text).strip()


def _convert_cite_ref(tag: Tag, page_name: str) -> str:
    """Convert a <sup class='reference'> to (wiki:PageName.cite_ref-ID)."""
    ref_id = tag.get("id", "")
    page_key = page_name.replace(" ", "_")
    if ref_id:
        return f"(wiki:{page_key}.{ref_id})"
    return ""


def _convert_internal_link(tag: Tag) -> str:
    """Convert a wiki internal <a> tag to [text](wiki:Page) markdown."""
    href = tag.get("href", "")
    text = tag.get_text()
    # Internal wiki links start with /index.php/
    if href.startswith("/index.php/"):
        page = href[len("/index.php/"):]
        # Decode URL encoding
        from urllib.parse import unquote
        page = unquote(page)
        # Strip anchor
        if "#" in page:
            page = page[: page.index("#")]
        return f"[{text}](wiki:{page})"
    # External links: keep text only
    return text


def _node_to_md(node, page_name: str) -> str:
    """Recursively convert a BeautifulSoup node to markdown text."""
    if isinstance(node, NavigableString):
        return html_module.unescape(str(node))

    if not isinstance(node, Tag):
        return ""

    name = node.name

    # --- skip these entirely ---
    if name in ("table", "img", "figure", "style", "script"):
        return ""
    if name == "div" and "thumb" in node.get("class", []):
        return ""  # image thumbnails
    if name == "div" and "hatnote" in node.get("class", []):
        return ""  # hatnote redirects
    if name == "div" and "toc" in node.get("class", []):
        return ""  # table of contents
    if name == "sup" and "reference" in node.get("class", []):
        return _convert_cite_ref(node, page_name)

    # --- inline formatting ---
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
        # External link or File link: keep text
        return node.get_text()
    if name == "span":
        # mw-editsection spans (the [edit] links) — drop
        if "mw-editsection" in node.get("class", []):
            return ""
        return "".join(_node_to_md(c, page_name) for c in node.children)
    if name == "br":
        return "\n"

    # --- block elements ---
    if name == "p":
        inner = "".join(_node_to_md(c, page_name) for c in node.children)
        inner = _normalize_whitespace(inner)
        # Skip cross-reference-only paragraphs like "(see X)"
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
        # templatequotetext holds the quote body; templatequotecite holds attribution
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
                # Convert cite contents via _node_to_md to preserve links and spacing.
                # The cite tag typically already begins with an em-dash (—), so we
                # do NOT add another one.
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
        # Plain blockquote
        inner = "".join(_node_to_md(c, page_name) for c in node.children)
        inner = _normalize_whitespace(inner)
        return f"> {inner}" if inner else ""

    if name == "dl":
        lines = []
        for dd in node.find_all("dd", recursive=False):
            # Skip hatnote divs inside dd
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

    # Headings within content (h3, h4) — handled at section level, not here
    if name in ("h3", "h4"):
        # These are handled by the section iterator, but if encountered inline
        # (shouldn't happen in well-formed MediaWiki HTML), emit as-is
        inner = "".join(_node_to_md(c, page_name) for c in node.children)
        inner = _normalize_whitespace(inner)
        prefix = "###" if name == "h3" else "####"
        return f"{prefix} {inner}"

    if name == "div":
        # Generic div: recurse into children
        return "".join(_node_to_md(c, page_name) for c in node.children)

    # Default: recurse
    return "".join(_node_to_md(c, page_name) for c in node.children)


def _strip_edit_suffix(heading_text: str) -> str:
    """Strip trailing [] edit markers from heading text."""
    return re.sub(r"\s*\[\s*\]\s*$", "", heading_text).strip()


# ---------------------------------------------------------------------------
# Section extraction
# ---------------------------------------------------------------------------

def extract_sections(soup: BeautifulSoup, page_name: str) -> tuple[dict[str, list[str]], Counter]:
    """Extract prose sections from a parsed page.

    Returns:
        sections: {schema_heading: [block_strings]}  — ordered within each heading
        unmapped: Counter of unrecognized h2 section names
    """
    main_div = soup.find("div", class_="mw-parser-output")
    if not main_div:
        return {}, Counter()

    # We accumulate blocks per schema heading. Each schema heading may be
    # populated by multiple wiki h2 sections (e.g., "Quotes by X" + "Quotes about X").
    sections: dict[str, list[str]] = {h: [] for h in SCHEMA_ORDER}
    unmapped: Counter = Counter()

    children = list(main_div.children)

    current_schema_heading: str | None = None
    current_wiki_h2: str | None = None  # for Quotes by/about subheading injection
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

            # Check for "Quotes by X" or "Quotes about X"
            quotes_by_match = re.match(
                r"quotes\s+(by|about)\s+(.+)", wiki_h2_lower
            )

            if wiki_h2_lower in SCHEMA_HEADING_MAP:
                current_schema_heading = SCHEMA_HEADING_MAP[wiki_h2_lower]
                current_wiki_h2 = None
            elif quotes_by_match:
                current_schema_heading = "## Quotes"
                # Inject a subheading block
                current_wiki_h2 = wiki_h2  # preserve original casing
                current_blocks = [f"### {wiki_h2}"]
            elif wiki_h2_lower in SKIP_HEADINGS:
                current_schema_heading = None
                current_wiki_h2 = None
            else:
                # Unknown section: log to unmapped, skip
                unmapped[wiki_h2] += 1
                current_schema_heading = None
                current_wiki_h2 = None

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

        # Skip infobox table at top level
        if child.name == "table" and "infobox" in child.get("class", []):
            i += 1
            continue

        # Skip toc div
        if child.name == "div" and "toc" in child.get("class", []):
            i += 1
            continue

        # Skip image thumbnail divs
        if child.name == "div" and "thumb" in child.get("class", []):
            i += 1
            continue

        if current_schema_heading is None:
            i += 1
            continue

        # Convert the node to markdown
        md = _node_to_md(child, page_name)
        if md and md.strip():
            current_blocks.append(md.strip())

        i += 1

    flush_current()
    return sections, unmapped


# ---------------------------------------------------------------------------
# Prose file rendering
# ---------------------------------------------------------------------------

def render_prose(sections: dict[str, list[str]]) -> str:
    """Render extracted sections into a prose markdown string.

    Output begins with the first populated ## heading. No frontmatter.
    Returns empty string if no sections have content.
    """
    output_parts: list[str] = []

    for heading in SCHEMA_ORDER:
        blocks = sections.get(heading, [])
        if not blocks:
            continue
        output_parts.append(heading)
        output_parts.append("")  # blank line after heading
        for block in blocks:
            output_parts.append(block)
            output_parts.append("")  # blank line after each block

    if not output_parts:
        return ""

    # Join and ensure exactly one trailing newline
    content = "\n".join(output_parts)
    content = re.sub(r"\n{3,}", "\n\n", content)
    if not content.endswith("\n"):
        content += "\n"
    return content


# ---------------------------------------------------------------------------
# Per-bucket processing
# ---------------------------------------------------------------------------

def process_bucket(
    manifest_path: Path,
    apply: bool,
    verbose: bool,
) -> dict:
    """Process one bucket. Returns stats dict."""
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"  ERROR reading {manifest_path}: {e}", file=sys.stderr)
        return {"bucket_id": str(manifest_path.parent.name), "error": str(e)}

    bucket_id = manifest["bucket_id"]

    # Check priority field exists
    priority = manifest.get("priority")
    if priority is None:
        print(
            f"  ERROR: bucket {bucket_id} has no 'priority' field in manifest — "
            "run wiki-pass2-prioritize.py first.",
            file=sys.stderr,
        )
        return {"bucket_id": bucket_id, "error": "missing_priority_field"}

    tier_a_pages: list[str] = priority.get("tier_a", [])
    tier_b_pages: list[str] = priority.get("tier_b", [])
    pages_to_process = [(p, "A") for p in tier_a_pages] + [(p, "B") for p in tier_b_pages]

    skeleton_dir = manifest_path.parent / "skeleton"
    prose_dir = manifest_path.parent / "prose"

    stats = {
        "bucket_id": bucket_id,
        "tier_a_count": len(tier_a_pages),
        "tier_b_count": len(tier_b_pages),
        "prose_emitted": 0,
        "pages_skipped_no_content": 0,
        "missing_html": [],
        "missing_skeleton": [],
        "word_counts": [],
        "unmapped_sections": Counter(),
    }

    if apply:
        prose_dir.mkdir(parents=True, exist_ok=True)

    for page_name, tier in pages_to_process:
        # Find skeleton slug (guarantees match with Stage 3a output)
        slug = find_skeleton_slug(skeleton_dir, page_name)
        if slug is None:
            stats["missing_skeleton"].append(page_name)
            if verbose:
                print(f"    [{tier}] {page_name!r} — no skeleton file, skipping")
            continue

        # Locate raw HTML cache file
        raw_path = raw_file_path(page_name)
        if not raw_path.exists():
            stats["missing_html"].append(page_name)
            if verbose:
                print(f"    [{tier}] {page_name!r} — no HTML cache at {raw_path.name}")
            continue

        # Parse HTML
        try:
            raw_json = json.loads(raw_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            stats["missing_html"].append(page_name)
            if verbose:
                print(f"    [{tier}] {page_name!r} — error reading cache: {e}")
            continue

        html_str = raw_json.get("html", "")
        soup = BeautifulSoup(html_str, "html.parser")

        sections, unmapped = extract_sections(soup, page_name)
        stats["unmapped_sections"].update(unmapped)

        prose_content = render_prose(sections)

        out_path = prose_dir / f"{slug}.prose.md"

        has_content = bool(prose_content.strip())

        if apply:
            if has_content:
                out_path.write_text(prose_content, encoding="utf-8")
            else:
                # Remove any stale file from a previous run
                if out_path.exists():
                    out_path.unlink()

        word_count = len(prose_content.split()) if has_content else 0
        stats["word_counts"].append(word_count)

        if has_content:
            stats["prose_emitted"] += 1
        else:
            stats["pages_skipped_no_content"] += 1

        if verbose:
            if has_content:
                mapped_secs = [h for h in SCHEMA_ORDER if sections.get(h)]
                unmapped_count = sum(unmapped.values())
                print(
                    f"    [{tier}] {page_name!r:50s} → {slug}.prose.md "
                    f"({word_count} words, sections={[s[3:] for s in mapped_secs]}, "
                    f"unmapped={unmapped_count})"
                )
            else:
                print(
                    f"    [{tier}] {page_name!r:50s} → skipped (no mapped content)"
                )

    return stats


# ---------------------------------------------------------------------------
# Core bucket detection (same patterns as Stage 3a)
# ---------------------------------------------------------------------------

_SPLIT_SUFFIX = r"(-[a-z]([0-9]+)?(-[a-z]([0-9]+)?)?)?$"
CORE_TIER_PATTERNS = [
    re.compile(r"^direwolves" + _SPLIT_SUFFIX),
    re.compile(
        r"^characters-house-(stark|lannister|targaryen|baratheon|"
        r"greyjoy|tully|arryn|tyrell|martell)" + _SPLIT_SUFFIX
    ),
    re.compile(
        r"^houses-(north|westerlands|crownlands|riverlands|vale|"
        r"reach|stormlands|dorne|iron-islands)" + _SPLIT_SUFFIX
    ),
    re.compile(
        r"^(north|westerlands|crownlands|riverlands|vale|reach|"
        r"stormlands|dorne|iron-islands)-locations" + _SPLIT_SUFFIX
    ),
]


def is_core_bucket(bucket_id: str) -> bool:
    for pat in CORE_TIER_PATTERNS:
        if pat.match(bucket_id):
            return True
    return False


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
        help="Write prose files. Without --apply, prints stats only (dry-run).",
    )
    parser.add_argument(
        "--bucket",
        metavar="BUCKET_ID",
        default=None,
        help="Process a single bucket only.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Print per-page stats within each bucket.",
    )
    args = parser.parse_args()

    # Discover bucket manifests
    if args.bucket:
        bucket_dir = WIKI_PASS2_DIR / args.bucket
        manifest_path = bucket_dir / "manifest.json"
        if not manifest_path.exists():
            print(f"ERROR: No manifest found at {manifest_path}", file=sys.stderr)
            sys.exit(1)
        manifest_paths = [manifest_path]
    else:
        manifest_paths = sorted(WIKI_PASS2_DIR.glob("*/manifest.json"))

    # Filter to secondary buckets
    secondary_manifests: list[Path] = []
    skipped_core = 0
    for mpath in manifest_paths:
        bucket_id = mpath.parent.name
        try:
            manifest = json.loads(mpath.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if manifest.get("tier") == "core" or is_core_bucket(bucket_id):
            skipped_core += 1
            continue
        secondary_manifests.append(mpath)

    mode_label = "APPLY" if args.apply else "DRY-RUN"
    print(f"\n=== Stage 3b prose extraction [{mode_label}] ===")
    print(f"Secondary buckets found: {len(secondary_manifests)}")
    if skipped_core and not args.bucket:
        print(f"Core buckets skipped:    {skipped_core}")

    # Process buckets
    all_stats: list[dict] = []
    total_errors = 0

    for mpath in secondary_manifests:
        bucket_id = mpath.parent.name
        if args.verbose:
            print(f"\n  Bucket: {bucket_id}")

        stats = process_bucket(
            manifest_path=mpath,
            apply=args.apply,
            verbose=args.verbose,
        )
        if "error" in stats:
            total_errors += 1
        all_stats.append(stats)

    # Aggregate
    total_buckets = len(all_stats)
    total_emitted = sum(s.get("prose_emitted", 0) for s in all_stats)
    total_skipped_no_content = sum(s.get("pages_skipped_no_content", 0) for s in all_stats)
    all_word_counts = []
    for s in all_stats:
        all_word_counts.extend(s.get("word_counts", []))
    all_missing_html: list[str] = []
    for s in all_stats:
        all_missing_html.extend(s.get("missing_html", []))
    all_missing_skeleton: list[str] = []
    for s in all_stats:
        all_missing_skeleton.extend(s.get("missing_skeleton", []))

    unmapped_total: Counter = Counter()
    for s in all_stats:
        unmapped_total.update(s.get("unmapped_sections", {}))

    mean_wc = sum(all_word_counts) / len(all_word_counts) if all_word_counts else 0.0
    median_wc = int(statistics.median(all_word_counts)) if all_word_counts else 0

    print()
    print(f"Buckets processed:       {total_buckets}")
    print(f"Prose files emitted:     {total_emitted}")
    print(f"Pages skipped (no content): {total_skipped_no_content}")
    print(f"Mean word count:         {mean_wc:.1f}")
    print(f"Median word count:       {median_wc}")
    if all_missing_html:
        print(f"Missing HTML cache:      {len(all_missing_html)}")
        for pg in all_missing_html[:5]:
            print(f"  - {pg}")
    if all_missing_skeleton:
        print(f"Missing skeletons (Stage 3a bug): {len(all_missing_skeleton)}")
        for pg in all_missing_skeleton[:5]:
            print(f"  - {pg}")

    if unmapped_total:
        print()
        print("Top 20 unmapped section names (skipped):")
        for section_name, count in unmapped_total.most_common(20):
            print(f"  {count:4d}  {section_name!r}")

    if total_errors:
        print(f"\nWARNING: {total_errors} bucket(s) had errors.")

    print("=" * 50)

    # Write summary JSON on --apply runs (global run only, not per-bucket)
    if args.apply and not args.bucket:
        summary = {
            "version": "v1",
            "ran_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "buckets_processed": total_buckets,
            "pages_processed": total_emitted + total_skipped_no_content,
            "prose_files_emitted": total_emitted,
            "pages_skipped_no_content": total_skipped_no_content,
            "mean_word_count": round(mean_wc, 2),
            "median_word_count": median_wc,
            "unmapped_sections_top_20": [
                {"section_name": name, "count": count}
                for name, count in unmapped_total.most_common(20)
            ],
            "missing_html_pages": all_missing_html,
            "missing_skeleton_pages": all_missing_skeleton,
        }
        STAGE3B_SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
        STAGE3B_SUMMARY_FILE.write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"\nSummary written to: {STAGE3B_SUMMARY_FILE}")

    if total_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
