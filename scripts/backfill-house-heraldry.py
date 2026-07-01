#!/usr/bin/env python3
"""Backfill heraldry data (sigil blazon, words, sigil image filename) onto
house node files from the LOCAL wiki cache.

Text only. NO image downloads, NO network calls of any kind.

For each house node file in graph/nodes/houses/*.node.md:
  1. Read the `wiki_source` frontmatter field, derive the wiki page name
     (e.g. "House_Stark") from the URL.
  2. Open the matching sources/wiki/_raw/<page>.json (local cache — never
     fetched here).
  3. Parse the infobox HTML for:
       - "Coat of arms" row  -> blazon text (sigil)
       - the decorative words-banner inside the infobox-image cell -> words
       - the infobox-image <img src=...> -> sigil_image filename only
  4. Propose frontmatter additions (sigil / words / sigil_image) and a
     `## Heraldry & Sigil` markdown section (placed after `## Identity`),
     matching the shape of the two hand-built examples:
       graph/nodes/houses/house-westerling.node.md
       graph/nodes/houses/house-spicer.node.md

Default mode is DRY-RUN: no files under graph/nodes/ are modified. Dry-run
emits working/wiki/data/sigil-data.jsonl and prints the proposed frontmatter
+ section text for five sample houses (house-stark, house-lannister,
house-targaryen, house-baratheon, house-tyrell).

Use --apply to perform the real in-place node edits. The edit is idempotent:
if a node already has a `## Heraldry & Sigil` section or these frontmatter
keys, they are replaced in place (never duplicated).

Usage:
  python scripts/backfill-house-heraldry.py                 # dry-run (default)
  python scripts/backfill-house-heraldry.py --apply          # real edits
  python scripts/backfill-house-heraldry.py --limit 20        # smoke test
"""

import argparse
import html as html_module
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
HOUSES_DIR = PROJECT_ROOT / "graph" / "nodes" / "houses"
RAW_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
OUTPUT_DIR = PROJECT_ROOT / "working" / "wiki" / "data"
SIGIL_DATA_FILE = OUTPUT_DIR / "sigil-data.jsonl"

SAMPLE_SLUGS = [
    "house-stark",
    "house-lannister",
    "house-targaryen",
    "house-baratheon",
    "house-tyrell",
]

# ---------------------------------------------------------------------------
# Frontmatter helpers (surgical text-based edits — preserve everything else
# byte-for-byte; a concurrent agent may be editing other fields/sections)
# ---------------------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\n(.*?\n)---\n", re.DOTALL)


def split_frontmatter(content):
    """Return (frontmatter_text, frontmatter_block_incl_dashes, body_text) or
    (None, None, content) if no frontmatter found."""
    m = FRONTMATTER_RE.match(content)
    if not m:
        return None, None, content
    fm_text = m.group(1)
    fm_block = m.group(0)
    body = content[m.end():]
    return fm_text, fm_block, body


def get_wiki_source(fm_text):
    """Extract the wiki_source URL value from raw frontmatter text."""
    m = re.search(r'^wiki_source:\s*"?([^"\n]+)"?\s*$', fm_text, re.MULTILINE)
    if not m:
        return None
    return m.group(1).strip()


def page_name_from_wiki_source(url):
    """Derive the wiki page name (e.g. 'House_Stark') from a wiki_source URL."""
    if not url:
        return None
    m = re.search(r"/index\.php/([^#?]+)", url)
    if not m:
        return None
    return m.group(1).strip()


# ---------------------------------------------------------------------------
# Infobox HTML parsing (text-only; no image bytes ever touched)
# ---------------------------------------------------------------------------

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"[ \t]+")


SUP_REFERENCE_RE = re.compile(
    r'<sup[^>]*class="reference"[^>]*>.*?</sup>',
    re.DOTALL | re.IGNORECASE,
)


def clean_inline_html(fragment):
    """Strip tags from an inline HTML fragment, normalize whitespace/line
    breaks into a single readable line. <br/> becomes a single space.

    Also strips wiki citation-footnote markers (<sup class="reference">[N 1]
    </sup>) which otherwise leak through as literal "[N 1]" text, and fully
    HTML-unescapes entities (numeric refs like &#91; as well as named ones
    like &amp;) rather than hand-decoding a handful of common cases.
    """
    if fragment is None:
        return None
    # Drop citation-footnote markers entirely before anything else — they're
    # editorial wiki apparatus, not part of the blazon/words text.
    text = SUP_REFERENCE_RE.sub("", fragment)
    # Normalize <br> variants to a space before stripping remaining tags.
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = TAG_RE.sub("", text)
    text = html_module.unescape(text)
    text = text.replace("\xa0", " ")
    text = WS_RE.sub(" ", text)
    text = re.sub(r"\n\s*", " ", text)
    return text.strip()


COAT_OF_ARMS_RE = re.compile(
    r'<th scope="row">Coat of arms</th>\s*<td>(.*?)</td>',
    re.DOTALL | re.IGNORECASE,
)

# The house "Words" (motto) are rendered as a decorative ribbon INSIDE the
# infobox-image <td>, not as a normal <th>Words</th> infobox row. First
# table-cell div in that ribbon holds the motto text. Verified against
# House_Stark ("Winter Is Coming"), House_Lannister ("Hear Me Roar!"), etc.
# Houses without a rendered sigil banner (most minor/extinct houses) simply
# have no match — this is expected and handled gracefully.
WORDS_RE = re.compile(
    r'display:\s*table-cell;[^"]*"[^>]*>([^<]+)</div>',
    re.IGNORECASE,
)

INFOBOX_IMAGE_RE = re.compile(
    r'class="infobox-image"[^>]*>(.*?)</td>',
    re.DOTALL | re.IGNORECASE,
)

IMG_SRC_RE = re.compile(r'<img[^>]+src="([^"]+)"', re.IGNORECASE)
FILE_LINK_RE = re.compile(r'/index\.php/File:([^"#?]+)', re.IGNORECASE)


def extract_sigil_image_filename(html):
    """Return just the image filename (e.g. 'House_Stark.svg') from the
    infobox-image cell, or None. Never returns a URL/path — filename only."""
    img_cell_m = INFOBOX_IMAGE_RE.search(html)
    search_scope = img_cell_m.group(1) if img_cell_m else html[:4000]

    # Preferred: <img src="/images/thumb/.../House_Stark.svg/250px-....png">
    # The source filename is the path segment right before the final
    # "NNNpx-....ext" thumbnail segment.
    src_m = IMG_SRC_RE.search(search_scope)
    if src_m:
        src = src_m.group(1)
        parts = [p for p in src.split("/") if p]
        # .../thumb/<hash1>/<hash2>/<Filename.ext>/<NNNpx-Filename.ext>
        if "thumb" in parts:
            thumb_idx = parts.index("thumb")
            # filename is 2 segments after "thumb" (hash1, hash2, filename)
            if len(parts) > thumb_idx + 3:
                return parts[thumb_idx + 3]
        # Non-thumb src: last path segment is the filename directly.
        if parts:
            candidate = parts[-1]
            # Strip a leading "NNNpx-" thumbnail size prefix if present.
            candidate = re.sub(r"^\d+px-", "", candidate)
            return candidate

    # Fallback: a File: link with no <img> (rare).
    file_m = FILE_LINK_RE.search(search_scope)
    if file_m:
        return file_m.group(1)

    return None


def parse_house_heraldry(html):
    """Return dict {sigil, words, sigil_image} parsed from infobox HTML.
    Any field may be None if not present/parseable."""
    sigil = None
    m = COAT_OF_ARMS_RE.search(html)
    if m:
        sigil = clean_inline_html(m.group(1))
        if not sigil:
            sigil = None

    words = None
    wm = WORDS_RE.search(html)
    if wm:
        candidate = clean_inline_html(wm.group(1))
        # Guard against picking up unrelated ribbon-decoration text (the
        # regex is scoped tightly to the table-cell div so this is mostly
        # a defensive no-op, but empty/1-char matches are discarded).
        if candidate and len(candidate) > 1:
            words = candidate

    sigil_image = extract_sigil_image_filename(html)

    return {"sigil": sigil, "words": words, "sigil_image": sigil_image}


# ---------------------------------------------------------------------------
# Frontmatter + section rendering
# ---------------------------------------------------------------------------

FM_KEY_RE_TEMPLATE = r'^{key}:.*(?:\n(?:[ \t]+.*)?)*\n?'


def yaml_quote(value):
    """Quote a YAML scalar value if it contains characters that need it."""
    if re.search(r'[:#"\'\n]|^\s|\s$', value):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return value


def build_frontmatter_additions(heraldry):
    """Return list of (key, formatted_line) for non-null heraldry fields."""
    lines = []
    if heraldry.get("sigil"):
        lines.append(("sigil", f"sigil: {yaml_quote(heraldry['sigil'])}"))
    if heraldry.get("words"):
        lines.append(("words", f"words: {yaml_quote(heraldry['words'])}"))
    if heraldry.get("sigil_image"):
        lines.append(("sigil_image", f"sigil_image: {yaml_quote(heraldry['sigil_image'])}"))
    return lines


def build_heraldry_section(heraldry, wiki_page):
    """Render the '## Heraldry & Sigil' markdown section, matching the shape
    of the hand-built house-westerling / house-spicer examples (blazon prose
    + wiki citation; words noted when present)."""
    lines = ["## Heraldry & Sigil", ""]
    sigil = heraldry.get("sigil")
    words = heraldry.get("words")

    if sigil:
        lines.append(f"{sigil} (wiki:{wiki_page})")
    else:
        lines.append(f"No coat of arms description available. (wiki:{wiki_page})")

    if words:
        lines.append("")
        lines.append(f'Words: "{words}" (wiki:{wiki_page})')

    return "\n".join(lines) + "\n"


def remove_frontmatter_keys(fm_text, keys):
    """Remove existing top-level keys (and any indented continuation lines)
    for idempotent re-application."""
    for key in keys:
        pattern = re.compile(FM_KEY_RE_TEMPLATE.format(key=re.escape(key)), re.MULTILINE)
        fm_text = pattern.sub("", fm_text)
    return fm_text


def insert_frontmatter_additions(fm_text, addition_lines):
    """Append new frontmatter lines at the end of the frontmatter block,
    after removing any pre-existing versions of those keys (idempotent)."""
    keys = [k for k, _ in addition_lines]
    fm_text = remove_frontmatter_keys(fm_text, keys)
    if not fm_text.endswith("\n"):
        fm_text += "\n"
    for _, line in addition_lines:
        fm_text += line + "\n"
    return fm_text


HERALDRY_SECTION_RE = re.compile(
    r"## Heraldry & Sigil\n.*?(?=\n## |\Z)",
    re.DOTALL,
)


def insert_heraldry_section(body, section_text):
    """Insert (or replace, if already present) the '## Heraldry & Sigil'
    section, placed immediately after the '## Identity' section."""
    if HERALDRY_SECTION_RE.search(body):
        # Replace in place — strip trailing section text back to just before
        # the next '## ' heading or end of body.
        new_body = HERALDRY_SECTION_RE.sub(section_text.rstrip("\n") + "\n", body, count=1)
        return new_body

    identity_re = re.compile(r"(## Identity\n.*?)(?=\n## |\Z)", re.DOTALL)
    m = identity_re.search(body)
    if m:
        insertion_point = m.end()
        # Ensure exactly one blank line before the new section.
        before = body[:insertion_point]
        after = body[insertion_point:]
        before = before.rstrip("\n") + "\n\n"
        after = after.lstrip("\n")
        return before + section_text.rstrip("\n") + "\n\n" + after

    # No '## Identity' section found — append at the end as a fallback.
    return body.rstrip("\n") + "\n\n" + section_text.rstrip("\n") + "\n"


def has_existing_heraldry_data(fm_text, body):
    return bool(
        re.search(r"^(sigil|words|sigil_image):", fm_text, re.MULTILINE)
        or HERALDRY_SECTION_RE.search(body)
    )


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------


def process_node(node_path, apply_mode, results, warnings):
    slug = node_path.stem.replace(".node", "")
    content = node_path.read_text(encoding="utf-8")
    fm_text, fm_block, body = split_frontmatter(content)

    if fm_text is None:
        warnings.append(f"{slug}: no frontmatter block found — skipped")
        return None

    wiki_source = get_wiki_source(fm_text)
    if not wiki_source:
        warnings.append(f"{slug}: no wiki_source field — skipped")
        return None

    wiki_page = page_name_from_wiki_source(wiki_source)
    if not wiki_page:
        warnings.append(f"{slug}: could not derive page name from wiki_source '{wiki_source}'")
        return None

    raw_path = RAW_DIR / f"{wiki_page}.json"
    if not raw_path.exists():
        warnings.append(f"{slug}: no local wiki cache file for page '{wiki_page}' ({raw_path})")
        return None

    try:
        raw_data = json.loads(raw_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        warnings.append(f"{slug}: failed to read/parse {raw_path}: {e}")
        return None

    html = raw_data.get("html")
    if not html:
        warnings.append(f"{slug}: cached page '{wiki_page}' has no html field")
        return None

    heraldry = parse_house_heraldry(html)

    record = {
        "slug": slug,
        "wiki_page": wiki_page,
        "sigil": heraldry.get("sigil"),
        "words": heraldry.get("words"),
        "sigil_image": heraldry.get("sigil_image"),
    }

    if not (heraldry.get("sigil") or heraldry.get("words") or heraldry.get("sigil_image")):
        # Matched a page but found nothing usable — still record for coverage
        # stats, but nothing to write.
        return record

    addition_lines = build_frontmatter_additions(heraldry)
    section_text = build_heraldry_section(heraldry, wiki_page)

    record["_proposed_frontmatter"] = "\n".join(line for _, line in addition_lines)
    record["_proposed_section"] = section_text

    if apply_mode:
        new_fm_text = insert_frontmatter_additions(fm_text, addition_lines)
        new_body = insert_heraldry_section(body, section_text)
        new_content = f"---\n{new_fm_text}---\n{new_body}"
        node_path.write_text(new_content, encoding="utf-8")
        record["_applied"] = True

    return record


def main():
    parser = argparse.ArgumentParser(
        description="Backfill heraldry data onto house node files from the local wiki cache.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Perform real in-place node edits (default is dry-run — no graph/nodes/ writes).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only process the first N house node files (smoke testing).",
    )
    args = parser.parse_args()

    if not HOUSES_DIR.exists():
        print(f"ERROR: houses directory not found: {HOUSES_DIR}", file=sys.stderr)
        sys.exit(1)

    node_files = sorted(HOUSES_DIR.glob("*.node.md"))
    if args.limit:
        node_files = node_files[: args.limit]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    warnings = []
    sample_records = {}

    for node_path in node_files:
        rec = process_node(node_path, args.apply, results, warnings)
        if rec is not None:
            results.append(rec)
            if rec["slug"] in SAMPLE_SLUGS:
                sample_records[rec["slug"]] = rec

    # Emit sigil-data.jsonl (safe in both dry-run and apply mode — working/ dir).
    with open(SIGIL_DATA_FILE, "w", encoding="utf-8") as f:
        for rec in results:
            out = {
                "slug": rec["slug"],
                "wiki_page": rec["wiki_page"],
                "sigil": rec["sigil"],
                "words": rec["words"],
                "sigil_image": rec["sigil_image"],
            }
            f.write(json.dumps(out, ensure_ascii=False) + "\n")

    # -------------------------------------------------------------------
    # Coverage stats
    # -------------------------------------------------------------------
    total_nodes = len(node_files)
    matched_pages = len(results)
    n_sigil = sum(1 for r in results if r.get("sigil"))
    n_words = sum(1 for r in results if r.get("words"))
    n_image = sum(1 for r in results if r.get("sigil_image"))
    n_written = sum(1 for r in results if "_proposed_frontmatter" in r)

    print("=" * 70)
    print("HOUSE HERALDRY BACKFILL —", "APPLY MODE" if args.apply else "DRY-RUN (no graph/nodes/ writes)")
    print("=" * 70)
    print(f"House node files scanned:      {total_nodes}")
    print(f"Matched a local wiki cache page: {matched_pages}")
    print(f"  -> yielded sigil (blazon):     {n_sigil}")
    print(f"  -> yielded words:              {n_words}")
    print(f"  -> yielded sigil_image:        {n_image}")
    print(f"  -> had at least one field (would write): {n_written}")
    print(f"Warnings/skips:                 {len(warnings)}")
    print()

    if warnings:
        print("--- Warnings (first 25) ---")
        for w in warnings[:25]:
            print(f"  - {w}")
        if len(warnings) > 25:
            print(f"  ... and {len(warnings) - 25} more")
        print()

    # -------------------------------------------------------------------
    # Sample house dry-run printout
    # -------------------------------------------------------------------
    if not args.apply:
        print("=" * 70)
        print("SAMPLE HOUSE OUTPUT (dry-run preview)")
        print("=" * 70)
        for slug in SAMPLE_SLUGS:
            rec = sample_records.get(slug)
            print(f"\n----- {slug} -----")
            if rec is None:
                print("  (not matched / no data found)")
                continue
            print(f"  wiki_page: {rec['wiki_page']}")
            print("  --- proposed frontmatter additions ---")
            fm_preview = rec.get("_proposed_frontmatter")
            print(fm_preview if fm_preview else "  (none)")
            print("  --- proposed ## Heraldry & Sigil section ---")
            print(rec.get("_proposed_section", "  (none)"))

    print()
    print(f"Wrote {matched_pages} records to {SIGIL_DATA_FILE.relative_to(PROJECT_ROOT)}")
    if args.apply:
        n_applied = sum(1 for r in results if r.get("_applied"))
        print(f"Applied edits to {n_applied} house node files.")
    else:
        print("Dry-run only — no files under graph/nodes/ were modified. Re-run with --apply to write.")


if __name__ == "__main__":
    main()
