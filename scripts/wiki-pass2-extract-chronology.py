#!/usr/bin/env python3
"""Year-page chronology extraction (Tier 3 deferred work).

Walks the 76 in-world year pages (130 AC, 209 AC, 298 AC, etc.) — all
classified as `skip` by the parser — and extracts internal-link
references with their surrounding context. Emits a JSONL data file
(NOT graph edges) for v2 temporal-edge backfill.

The locked 22-type edge vocabulary in architecture.md does not include
OCCURRED_IN_YEAR, and the v2 temporal-edges design (Session 26 TODO)
plans structured per-edge `start_year` / `end_year` / `precision`
fields rather than a dedicated edge type. This extractor produces the
input data for that future backfill — does NOT modify graph nodes.

Output: working/wiki-parsed/chronology-events.jsonl
Row shape: {
  "year_page": "298 AC",
  "year_value": 298,
  "year_era": "AC",  # Aegon's Conquest reference frame
  "target_page": "Eddard Stark",
  "target_slug": "eddard-stark",
  "anchor_text": "Eddard Stark",
  "section": "Events",
  "snippet": "Eddard Stark is named Hand of the King by Robert Baratheon.",
  "citation": null  # cite_ref if present in the surrounding sentence
}

Run:
  python3 scripts/wiki-pass2-extract-chronology.py           # dry-run summary
  python3 scripts/wiki-pass2-extract-chronology.py --apply   # write JSONL
"""

import argparse
import html as html_module
import json
import re
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

PAGE_CATEGORIES_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "page-categories.jsonl"
PAGE_INDEX_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "page-index.jsonl"
WIKI_RAW_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
OUTPUT_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "chronology-events.jsonl"

YEAR_RE = re.compile(r"^(\d{1,4})\s+(AC|BC)$", re.IGNORECASE)


def load_year_pages():
    """Find all wiki pages whose categories include 'Years' (76 pages)."""
    year_pages = []
    with open(PAGE_CATEGORIES_FILE, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if "Years" in r.get("categories", []):
                m = YEAR_RE.match(r["page"])
                if m:
                    year_pages.append((r["page"], int(m.group(1)), m.group(2).upper()))
    return year_pages


def page_to_slug(name: str) -> str:
    name = re.sub(r"['\",]", "", name.lower())
    name = re.sub(r"[ _]+", "-", name)
    name = re.sub(r"[^a-z0-9-]", "-", name)
    return re.sub(r"-+", "-", name).strip("-")


# Match <a href="/index.php/PageName" title="..."> ... </a>
LINK_RE = re.compile(
    r'<a\s+href="/index\.php/([^"#]+)"[^>]*>([^<]+)</a>',
    re.IGNORECASE,
)
# Match the surrounding "sentence" — coarse: text from previous . or > to next . or <
SENTENCE_BREAK = re.compile(r"[.!?]\s+|<[^>]+>")


def extract_links_from_page(html: str, year_page: str):
    """Yield (target_page, anchor_text, snippet) for each internal link."""
    # First, get a plain-text view of the body for snippet extraction.
    # We strip HTML but keep the link tokens recognizable.
    seen_targets = set()
    for m in LINK_RE.finditer(html):
        target_url = html_module.unescape(m.group(1))
        target_page = target_url.replace("_", " ")
        anchor = html_module.unescape(m.group(2)).strip()

        # Skip self-references and common nav links
        if target_page == year_page:
            continue
        # Skip year pages themselves (they nav to each other extensively)
        if YEAR_RE.match(target_page):
            continue
        # Skip duplicate first-occurrences (year pages reference some entities
        # multiple times; keep first occurrence per page for snippet stability)
        key = (target_page, anchor)
        if key in seen_targets:
            continue
        seen_targets.add(key)

        # Snippet: 200 chars of context around the match position
        start = max(0, m.start() - 200)
        end = min(len(html), m.end() + 100)
        ctx = html[start:end]
        # Strip HTML for snippet
        snippet = re.sub(r"<[^>]+>", " ", ctx)
        snippet = re.sub(r"\s+", " ", snippet).strip()

        yield target_page, anchor, snippet


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true",
                    help="Write JSONL output (default: summary only)")
    args = ap.parse_args()

    year_pages = load_year_pages()
    print(f"Year pages found: {len(year_pages)}")

    # Load page-index for target-existence + entity-type filtering
    page_to_type = {}
    with open(PAGE_INDEX_FILE, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            page_to_type[r["page"]] = r.get("entity_type_guess")

    rows = []
    target_type_counts = Counter()
    broken_links = 0

    for year_page, year_value, year_era in sorted(year_pages,
                                                   key=lambda x: (x[2], x[1])):
        fname = year_page.replace(" ", "_") + ".json"
        fpath = WIKI_RAW_DIR / fname
        if not fpath.exists():
            continue
        with open(fpath, encoding="utf-8") as f:
            d = json.load(f)
        html = d.get("html", "")

        for target_page, anchor, snippet in extract_links_from_page(html, year_page):
            target_type = page_to_type.get(target_page)
            if target_type is None:
                broken_links += 1
                continue
            if target_type == "skip":
                continue
            target_type_counts[target_type] += 1
            rows.append({
                "year_page": year_page,
                "year_value": year_value,
                "year_era": year_era,
                "target_page": target_page,
                "target_slug": page_to_slug(target_page),
                "target_type": target_type,
                "anchor_text": anchor,
                "snippet": snippet[:300],
            })

    print(f"\n=== Summary ===")
    print(f"  Total chronology events extracted: {len(rows)}")
    print(f"  Broken links (target not in page-index): {broken_links}")
    print(f"\n=== By target type ===")
    for t, n in target_type_counts.most_common():
        print(f"  {t:30s} {n:>5}")

    # Year coverage
    by_year = Counter(r["year_value"] for r in rows)
    print(f"\n=== Year coverage ({len(by_year)} distinct years) ===")
    print(f"  Min year: {min(by_year)} {next(iter(year_pages))[2]}")
    print(f"  Max year: {max(by_year)}")
    print(f"  Top 10 dense years: {by_year.most_common(10)}")

    if args.apply:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"\nWrote {len(rows)} rows to {OUTPUT_FILE}")
    else:
        print(f"\n(Dry run; pass --apply to write {OUTPUT_FILE})")
        # Show 5 sample rows
        print("\n=== Sample rows ===")
        for r in rows[:5]:
            print(f"  [{r['year_value']} {r['year_era']}] "
                  f"{r['anchor_text']!r} ({r['target_type']}) — "
                  f"{r['snippet'][:120]!r}")


if __name__ == "__main__":
    main()
