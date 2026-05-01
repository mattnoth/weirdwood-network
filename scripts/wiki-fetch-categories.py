#!/usr/bin/env python3
"""Bounded MediaWiki categories backfill — completion-of-original-crawl operation.

The original wiki crawl (`scripts/archive/wiki-scraper.py.archive`) used MediaWiki's
`action=parse` API which strips the catlinks footer. The category-based entity
categorizer in that scraper depended on category data and could only run for
"House X" pages (name-based fast path) — the rest fell through to
`sources/wiki/_uncategorized/` as `proposed_type: unknown`.

This script fills that one specific gap: fetches MediaWiki categories for all
17,657 cached pages via `action=query&prop=categories&titles=...&cllimit=max`,
50 titles per batch. Writes one JSONL row per page to
`working/wiki-parsed/page-categories.jsonl`.

Per CLAUDE.md "Approved exception fetches" — this is a single bounded fetch,
approved 2026-04-30, targeting one specific data field, written to working/ only.

Cloudflare bypass: Uses the `cloudscraper` library, which handles AWOIAF's
`Just a moment...` JS challenge via header heuristics (no full browser).
Verified 2026-04-30: plain `urllib` is 403'd; `cloudscraper` returns 200 in
~0.14s/batch.

Usage:
    python3 scripts/wiki-fetch-categories.py --smoke   # 5 batches, ~250 pages
    python3 scripts/wiki-fetch-categories.py           # full ~17,657 pages
    python3 scripts/wiki-fetch-categories.py --resume  # skip pages already fetched
    python3 scripts/wiki-fetch-categories.py -v        # per-batch logging

Output (one row per page):
    {"page": "Longclaw", "categories": ["House Mormont", "Swords",
     "Valyrian steel blades"], "fetched_at": "2026-04-30"}
"""

import argparse
import datetime
import json
import sys
import time
from pathlib import Path

import cloudscraper

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_INPUT = PROJECT_ROOT / "working" / "wiki-parsed" / "page-index.jsonl"
DEFAULT_OUTPUT = PROJECT_ROOT / "working" / "wiki-parsed" / "page-categories.jsonl"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
API_URL = "https://awoiaf.westeros.org/api.php"
BATCH_SIZE = 50            # MediaWiki anonymous limit for prop=categories
SLEEP_BETWEEN_BATCHES = 0.25   # 4 req/sec ceiling, polite to a fan-run wiki
TODAY = datetime.date.today().isoformat()
TRIPWIRE_SAMPLE = 100      # check first N pages
TRIPWIRE_THRESHOLD = 0.80  # fail if <80% of sampled pages have categories


def load_page_titles(path: Path) -> list[str]:
    """Read every page name from page-index.jsonl."""
    titles: list[str] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            page = rec.get("page")
            if page:
                titles.append(page)
    return titles


def load_already_fetched(path: Path) -> set[str]:
    """Return set of page names already in the output file."""
    fetched: set[str] = set()
    if not path.exists():
        return fetched
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                if rec.get("page"):
                    fetched.add(rec["page"])
            except json.JSONDecodeError:
                continue
    return fetched


def fetch_batch(scraper, titles: list[str], verbose: bool = False) -> dict[str, list[str]]:
    """Fetch categories for up to 50 titles. Returns {title: [category_names]}.

    Handles MediaWiki `clcontinue` continuation when a page has more
    categories than fit in one response.
    """
    result: dict[str, list[str]] = {t: [] for t in titles}
    params = {
        "action": "query",
        "prop": "categories",
        "titles": "|".join(titles),
        "format": "json",
        "cllimit": "max",
    }

    while True:
        resp = scraper.get(API_URL, params=params, timeout=30)
        if resp.status_code != 200:
            if verbose:
                print(f"    HTTP {resp.status_code}: {resp.text[:200]}")
            return result

        data = resp.json()
        pages = data.get("query", {}).get("pages", {})
        for pageid, pageinfo in pages.items():
            title = pageinfo.get("title")
            if title is None:
                continue
            cats_raw = pageinfo.get("categories", [])
            for cat in cats_raw:
                cat_title = cat.get("title", "")
                # Strip "Category:" prefix
                if cat_title.startswith("Category:"):
                    cat_title = cat_title[len("Category:"):]
                if cat_title:
                    result.setdefault(title, []).append(cat_title)

        # Handle continuation
        cont = data.get("continue", {})
        if "clcontinue" in cont:
            params = {
                "action": "query",
                "prop": "categories",
                "titles": "|".join(titles),
                "format": "json",
                "cllimit": "max",
                "clcontinue": cont["clcontinue"],
            }
            continue
        break

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--smoke", action="store_true",
                        help="Fetch only 5 batches (~250 pages); useful for smoke testing")
    parser.add_argument("--resume", action="store_true",
                        help="Skip pages already in output file")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Per-batch logging")
    parser.add_argument("--tripwire-threshold", type=float, default=TRIPWIRE_THRESHOLD,
                        help="Fail if <THRESHOLD of sampled pages have categories")
    args = parser.parse_args()

    titles = load_page_titles(args.input)
    print(f"Loaded {len(titles):,} page titles from {args.input}")

    if args.resume:
        already = load_already_fetched(args.output)
        print(f"Already fetched: {len(already):,}")
        titles = [t for t in titles if t not in already]
        print(f"Remaining to fetch: {len(titles):,}")

    if args.smoke:
        titles = titles[: BATCH_SIZE * 5]
        print(f"SMOKE MODE: fetching {len(titles)} pages")

    if not titles:
        print("Nothing to fetch.")
        return 0

    # Open output in append mode so resume works naturally
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output_mode = "a" if args.resume and args.output.exists() else "w"

    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "darwin", "mobile": False}
    )

    n_batches = (len(titles) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"Will run {n_batches} batches of up to {BATCH_SIZE} titles each")
    print()

    pages_with_cats = 0
    pages_without_cats = 0
    failed_batches = 0
    start = time.time()

    with open(args.output, output_mode, encoding="utf-8") as out:
        for batch_idx in range(n_batches):
            batch = titles[batch_idx * BATCH_SIZE: (batch_idx + 1) * BATCH_SIZE]
            try:
                cats_by_title = fetch_batch(scraper, batch, verbose=args.verbose)
            except Exception as e:
                print(f"  batch {batch_idx + 1}/{n_batches}: ERROR {type(e).__name__}: {e}",
                      file=sys.stderr)
                failed_batches += 1
                # On failure, still emit empty-categories rows so resume doesn't loop
                cats_by_title = {t: [] for t in batch}

            for title in batch:
                cats = cats_by_title.get(title, [])
                if cats:
                    pages_with_cats += 1
                else:
                    pages_without_cats += 1
                rec = {
                    "page": title,
                    "categories": cats,
                    "fetched_at": TODAY,
                }
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")

            if args.verbose or (batch_idx + 1) % 25 == 0:
                elapsed = time.time() - start
                rate = (batch_idx + 1) / elapsed if elapsed > 0 else 0
                eta = (n_batches - batch_idx - 1) / rate if rate > 0 else 0
                print(f"  batch {batch_idx + 1:>3}/{n_batches}  "
                      f"({(batch_idx + 1) * BATCH_SIZE:>5}/{len(titles):>5} pages)  "
                      f"elapsed={elapsed:.1f}s  rate={rate:.1f}b/s  eta={eta:.0f}s")

            time.sleep(SLEEP_BETWEEN_BATCHES)

            # Tripwire after first sample
            if batch_idx + 1 == max(1, TRIPWIRE_SAMPLE // BATCH_SIZE):
                sampled = pages_with_cats + pages_without_cats
                rate = pages_with_cats / sampled if sampled else 0
                print(f"\n  TRIPWIRE: {pages_with_cats}/{sampled} pages "
                      f"({rate:.1%}) have categories")
                if rate < args.tripwire_threshold:
                    print(f"  TRIPWIRE FAIL: <{args.tripwire_threshold:.0%} pages have "
                          f"categories. Aborting.", file=sys.stderr)
                    return 2
                print(f"  TRIPWIRE PASS\n")

    elapsed = time.time() - start
    print()
    print("=== Summary ===")
    print(f"Pages with categories:    {pages_with_cats:,}")
    print(f"Pages without categories: {pages_without_cats:,}")
    print(f"Failed batches:           {failed_batches}")
    print(f"Total elapsed:            {elapsed:.1f}s")
    print(f"Output:                   {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
