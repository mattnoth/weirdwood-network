"""
wiki-event-alias-harvester.py

Harvests event-name aliases from the local MediaWiki cache so a downstream
resolver can match Pass-1 chapter-beat slugs to existing wiki event-nodes.

Two alias sources are used:
  1. Redirect pages — other wiki titles that point to an event page
  2. Infobox title row — the displayed event name (often different from the URL slug)

Output: working/wiki/data/event-node-aliases.json

Shape:
{
  "red-wedding": {
    "canonical_name": "Red Wedding",
    "aliases": ["the-red-wedding"],
    "alias_count": 1,
    "redirect_sources": ["The_Red_Wedding"]
  },
  ...
}

Usage:
  python scripts/wiki-event-alias-harvester.py
  python scripts/wiki-event-alias-harvester.py --verbose
"""

import argparse
import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup


# ---------------------------------------------------------------------------
# Event categories — pages in any of these category buckets are treated as
# confirmed event-class pages (in addition to those already in graph/nodes/events/)
# ---------------------------------------------------------------------------
EVENT_CATEGORIES = {
    "Events",
    "Battles",
    "Andal invasion",
    "Aegon's Conquest",
    "Blackfyre Rebellions",
    "Conflict beyond the Wall",
    "Conquest of Dorne",
    "Dance of the Dragons",
    "First Dornish War",
    "Greyjoy's Rebellion",
    "Robert's Rebellion",
    "War of the Five Kings",
    "War of the Ninepenny Kings",
    "Assassinations",
    "Tourneys",
    "Kingsmoots",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slug_from_page_title(title: str) -> str:
    """Convert a wiki page title to a kebab-case slug (same convention as node files)."""
    slug = title.lower()
    slug = re.sub(r"[''']", "", slug)       # drop apostrophes
    slug = re.sub(r"[^a-z0-9]+", "-", slug) # non-alphanum → hyphen
    slug = slug.strip("-")
    return slug


def extract_redirect_target(html: str) -> str | None:
    """Return the redirect target page title, or None if this is not a redirect page."""
    if "redirectMsg" not in html:
        return None
    # Pattern: <li><a href="..." title="Page Title">...</a></li> inside redirectMsg div
    m = re.search(r'<div class="redirectMsg".*?<li><a [^>]*title="([^"]+)"', html, re.DOTALL)
    if m:
        raw = m.group(1)
        # Unescape HTML entities (&#039; → ', &amp; → &, etc.)
        raw = raw.replace("&#039;", "'").replace("&amp;", "&").replace("&quot;", '"')
        return raw
    return None


def extract_infobox_title(html: str) -> str | None:
    """Return the bold header cell text from the infobox, if present."""
    soup = BeautifulSoup(html, "html.parser")
    ib = soup.find("table", class_="infobox")
    if not ib:
        return None
    # First <th colspan="2"> with font-size:125% is the event title
    th = ib.find("th", attrs={"colspan": "2"})
    if th:
        text = th.get_text(strip=True)
        if text:
            return text
    return None


def normalize_alias(text: str) -> str:
    """Return kebab-slug form of an alias text."""
    return slug_from_page_title(text)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--verbose", action="store_true", help="Print per-page progress")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    raw_dir = repo_root / "sources" / "wiki" / "_raw"
    events_dir = repo_root / "graph" / "nodes" / "events"
    categories_jsonl = repo_root / "working" / "wiki" / "data" / "page-categories.jsonl"
    output_path = repo_root / "working" / "wiki" / "data" / "event-node-aliases.json"

    if not raw_dir.exists():
        print(f"ERROR: wiki cache not found at {raw_dir}", file=sys.stderr)
        sys.exit(1)

    # ------------------------------------------------------------------
    # Step 1 — Build the set of confirmed event-node slugs from graph/nodes/events/
    # ------------------------------------------------------------------
    confirmed_event_slugs: set[str] = set()
    slug_to_node_filename: dict[str, str] = {}  # slug → "red-wedding.node.md"
    for f in events_dir.glob("*.node.md"):
        slug = f.stem.replace(".node", "")
        confirmed_event_slugs.add(slug)
        slug_to_node_filename[slug] = f.name

    print(f"Confirmed event-node slugs from graph/nodes/events/: {len(confirmed_event_slugs)}")

    # ------------------------------------------------------------------
    # Step 2 — Load page-categories.jsonl; build two indexes:
    #   category_pages: slug → set of categories
    #   title_to_slug: wiki page title (as stored in JSONL) → slug
    # ------------------------------------------------------------------
    page_categories: dict[str, list[str]] = {}   # "Red Wedding" → [...]
    if categories_jsonl.exists():
        with open(categories_jsonl) as f:
            for line in f:
                d = json.loads(line)
                page_categories[d["page"]] = d.get("categories", [])
    else:
        print(f"WARNING: {categories_jsonl} not found — category-based event detection disabled", file=sys.stderr)

    # Pages that are event-class via category membership
    category_event_titles: set[str] = set()
    for title, cats in page_categories.items():
        if any(c in EVENT_CATEGORIES for c in cats):
            category_event_titles.add(title)

    print(f"Category-identified event pages: {len(category_event_titles)}")

    # Map wiki page title → slug for all known pages
    def title_to_slug(title: str) -> str:
        return slug_from_page_title(title)

    # Build the union of "event-class" wiki page titles we want to collect aliases for.
    # A title is event-class if:
    #   (a) its slug is in confirmed_event_slugs, OR
    #   (b) it appears in category_event_titles
    all_event_titles: set[str] = set(category_event_titles)
    # Also add titles that map to confirmed slugs (for round-trip).
    # We'll match these from the raw JSON files during the scan below.

    # ------------------------------------------------------------------
    # Step 3 — Single-pass scan of _raw/*.json
    # Build:
    #   redirect_index: canonical_title → list of redirect_source_filenames
    #   page_canonical_name: slug → infobox display name
    # ------------------------------------------------------------------
    raw_files = sorted(raw_dir.glob("*.json"))
    total_files = len(raw_files)
    print(f"Scanning {total_files} wiki JSON files...")

    # redirect_index maps the TITLE of the target page to a list of redirecting page
    # filenames (the source page names, without .json)
    redirect_index: dict[str, list[str]] = {}   # "Red Wedding" → ["The_Red_Wedding", ...]
    page_infobox_title: dict[str, str] = {}     # "Red Wedding" slug → "Red Wedding" display name

    scanned = 0
    for json_path in raw_files:
        scanned += 1
        if args.verbose and scanned % 1000 == 0:
            print(f"  ...{scanned}/{total_files}")

        # File stem is the URL-encoded page name
        page_filename_stem = json_path.stem   # e.g. "The_Red_Wedding"

        try:
            with open(json_path) as f:
                d = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"WARNING: Could not read {json_path.name}: {e}", file=sys.stderr)
            continue

        page_title: str = d.get("page", page_filename_stem)
        html: str = d.get("html", "")

        # --- Redirect detection ---
        redirect_target = extract_redirect_target(html)
        if redirect_target:
            redirect_index.setdefault(redirect_target, []).append(page_filename_stem)
            continue  # redirect pages have no infobox of their own

        # --- Infobox title extraction (for non-redirect pages only) ---
        slug = title_to_slug(page_title)
        is_event = (slug in confirmed_event_slugs) or (page_title in all_event_titles)
        if not is_event:
            continue

        ib_title = extract_infobox_title(html)
        if ib_title and ib_title != page_title:
            page_infobox_title[slug] = ib_title
        else:
            page_infobox_title[slug] = page_title

    print(f"Redirects indexed: {sum(len(v) for v in redirect_index.values())} across {len(redirect_index)} target titles")

    # ------------------------------------------------------------------
    # Step 4 — For each confirmed event-node, collect aliases
    # ------------------------------------------------------------------

    # Build title → slug lookup for event pages (both confirmed + category-based)
    # We need to know the wiki page title for each event node slug.
    # The most reliable source is page_infobox_title (built above).
    # For slugs we didn't scan an infobox for, reconstruct from slug.

    def slug_to_likely_wiki_title(slug: str) -> list[str]:
        """Heuristic: generate candidate wiki titles from a slug."""
        # Title-case each word
        words = slug.replace("-", " ").split()
        title_cased = " ".join(w.capitalize() for w in words)
        # Also try apostrophe variants — "roberts rebellion" → "Robert's Rebellion"
        # The infobox scan already handles exact matches; these are fallbacks.
        return [title_cased]

    # Invert page_infobox_title: slug → display name (already built above)
    # Also build: display_name → slug
    display_to_slug: dict[str, str] = {}
    for slug, display in page_infobox_title.items():
        display_to_slug[display] = slug

    # Build alias dict
    alias_output: dict[str, dict] = {}

    for slug in sorted(confirmed_event_slugs):
        canonical_name = page_infobox_title.get(slug)
        if canonical_name is None:
            # Fall back to title-casing the slug
            canonical_name = slug.replace("-", " ").title()

        # Find redirects: look up redirect_index by canonical_name and by
        # any title-cased variant of the slug
        redirect_sources: list[str] = []
        candidates = [canonical_name] + slug_to_likely_wiki_title(slug)
        for cand in candidates:
            for src in redirect_index.get(cand, []):
                if src not in redirect_sources:
                    redirect_sources.append(src)

        # Convert redirect source filenames to alias slugs
        alias_slugs: list[str] = []
        for src in redirect_sources:
            # src is something like "The_Red_Wedding"
            src_title = src.replace("_", " ")
            # Unescape common URL encodings
            src_title = src_title.replace("%27", "'").replace("%26", "&")
            a_slug = normalize_alias(src_title)
            if a_slug and a_slug != slug:
                alias_slugs.append(a_slug)

        alias_output[slug] = {
            "canonical_name": canonical_name,
            "aliases": alias_slugs,
            "alias_count": len(alias_slugs),
            "redirect_sources": redirect_sources,
        }

    # ------------------------------------------------------------------
    # Step 5 — Write output
    # ------------------------------------------------------------------
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(alias_output, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {output_path}")

    # ------------------------------------------------------------------
    # Step 6 — Print stats
    # ------------------------------------------------------------------
    total_aliases = sum(e["alias_count"] for e in alias_output.values())
    print(f"\n--- Summary ---")
    print(f"Event-nodes scanned:   {len(alias_output)}")
    print(f"Total aliases harvested: {total_aliases}")
    print(f"  (from redirects only — infobox 'also known as' field not present in cache)")

    # Top 10 by alias count
    top10 = sorted(alias_output.items(), key=lambda x: x[1]["alias_count"], reverse=True)[:10]
    print("\nTop 10 events by alias count:")
    for slug, data in top10:
        print(f"  {slug:55s}  {data['alias_count']:3d}  aliases: {data['aliases']}")

    return alias_output


if __name__ == "__main__":
    main()
