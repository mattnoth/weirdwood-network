#!/usr/bin/env python3
"""Bounded AWOIAF sigil (heraldry) image backfill — completion-of-original-crawl operation.

The original wiki crawl (`scripts/archive/wiki-scraper.py.archive`) saved page
HTML only — it never downloaded the image binaries referenced by that HTML
(sigils, portraits, maps). This script fills one specific gap: the sigil
(house heraldry) image for `organization.house` nodes.

For a given house page's cached raw JSON (`sources/wiki/_raw/House_<Name>.json`),
this script:
  1. Parses the `<table class="infobox">` in `data["html"]` and locates the
     first `<img>` inside the `infobox-image` cell (the sigil image).
  2. Derives the ORIGINAL (non-thumbnail) file URL by stripping the `/thumb/`
     segment and the trailing `NNNpx-...` resize segment from the thumbnail
     src, e.g.:
       thumb: /images/thumb/7/7e/House_Stark.svg/250px-House_Stark.svg.png
       orig:  /images/7/7e/House_Stark.svg
  3. Tries the original file first (usually a crisp .svg); falls back to the
     thumbnail .png if the original 404s or is otherwise unavailable.
  4. Verifies the downloaded bytes are a real image (SVG XML or PNG magic
     bytes) — not an HTML error page or a Cloudflare challenge page.

Per CLAUDE.md "Approved exception fetches" — this is a single bounded fetch,
approved 2026-06-30 (per-turn authorization), targeting one specific data
field (sigil images), written to `working/wiki/sigils/` ONLY — never to
`sources/`.

Cloudflare bypass: uses the `cloudscraper` library (verified working for this
project since 2026-04-30's category backfill).

SMOKE TEST MODE: --smoke5 fetches exactly the 5-house smoke set.

FULL-SCALE MODE (greenlit 2026-06-30 by Matt after smoke-test review):
--from-sigil-data reads `working/wiki/data/sigil-data.jsonl` (one record per
house: {"slug", "wiki_page", "sigil", "words", "sigil_image"}) and fetches a
sigil for every record whose `sigil_image` field is non-null/non-empty. The
`slug` field is used directly for the output filename (`<slug>.<ext>`) — it
does NOT need to be re-derived from `wiki_page`, since sigil-data.jsonl may
encode name variants (e.g. "house-arryn-of-gulltown" pointing at the same
underlying sigil file as "house-arryn"). Resumable: any slug that already has
a file (any extension) in the output dir is skipped.

Usage:
    python3 scripts/wiki-fetch-sigils.py --smoke5
    python3 scripts/wiki-fetch-sigils.py --houses House_Stark House_Lannister
    python3 scripts/wiki-fetch-sigils.py --from-sigil-data working/wiki/data/sigil-data.jsonl
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

import cloudscraper

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
RAW_WIKI_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
OUTPUT_DIR = PROJECT_ROOT / "working" / "wiki" / "sigils"
DEFAULT_SIGIL_DATA = PROJECT_ROOT / "working" / "wiki" / "data" / "sigil-data.jsonl"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BASE_URL = "https://awoiaf.westeros.org"
SLEEP_BETWEEN_REQUESTS = 1.8  # seconds; throttled per hard constraints
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# The 5-house smoke set (per task instructions).
SMOKE5_HOUSES = [
    "House_Stark",
    "House_Lannister",
    "House_Targaryen",
    "House_Baratheon",
    "House_Tyrell",
]

INFOBOX_IMG_RE = re.compile(
    r'infobox-image.*?<img[^>]+src="([^"]+)"', re.DOTALL
)


def house_to_slug(house_page_name: str) -> str:
    """'House_Stark' -> 'house-stark' (node-slug convention: lowercase kebab)."""
    return house_page_name.lower().replace("_", "-")


def thumb_src_to_original_url(thumb_src: str) -> str | None:
    """Derive the original (non-thumbnail) image URL from a thumbnail src.

    thumb: /images/thumb/7/7e/House_Stark.svg/250px-House_Stark.svg.png
    orig:  /images/7/7e/House_Stark.svg

    Returns None if the src doesn't look like a /images/thumb/... path
    (i.e. it's already a direct, non-thumbnail image).
    """
    m = re.match(r"^/images/thumb/(.+)/[0-9]+px-[^/]+$", thumb_src)
    if not m:
        return None
    return f"/images/{m.group(1)}"


def extract_sigil_thumb_src(html: str) -> str | None:
    """Find the sigil <img src> inside the infobox-image cell of the page HTML."""
    m = INFOBOX_IMG_RE.search(html)
    if not m:
        return None
    return m.group(1)


def classify_bytes(content: bytes) -> str:
    """Return 'svg', 'png', 'webp', 'jpg', 'html', or 'unknown' based on magic
    bytes / content sniff. The wiki occasionally serves WebP-encoded bytes at
    a URL that ends in .png — sniff by content, never trust the URL extension."""
    stripped = content.lstrip()
    if stripped.startswith(b"<?xml") or stripped.startswith(b"<svg") or b"<svg" in stripped[:500]:
        return "svg"
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if content[:4] == b"RIFF" and content[8:12] == b"WEBP":
        return "webp"
    if content.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if stripped[:15].lower().startswith(b"<!doctype html") or stripped[:5].lower().startswith(b"<html"):
        return "html"
    return "unknown"


def download(scraper, url: str, verbose: bool = False) -> tuple[int, bytes]:
    resp = scraper.get(url, timeout=30)
    if verbose:
        print(f"    GET {url} -> HTTP {resp.status_code}, {len(resp.content)} bytes")
    return resp.status_code, resp.content


def already_downloaded(slug: str, output_dir: Path) -> Path | None:
    """Return the existing file path for this slug if one is already on disk
    (any of the extensions this script can produce), else None."""
    for ext in ("svg", "png", "webp", "jpg", "jpeg"):
        candidate = output_dir / f"{slug}.{ext}"
        if candidate.exists() and candidate.stat().st_size > 0:
            return candidate
    return None


def load_sigil_data(path: Path) -> list[dict]:
    """Load sigil-data.jsonl records that have a non-null/non-empty sigil_image."""
    records = []
    with open(path, encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"  WARNING: skipping malformed line {line_num}: {e}", file=sys.stderr)
                continue
            if rec.get("sigil_image"):
                records.append(rec)
    return records


def fetch_house_sigil(scraper, house_page: str, slug: str, output_dir: Path, verbose: bool = False) -> dict:
    """Fetch and save the sigil image for one house. Returns a result record."""
    raw_path = RAW_WIKI_DIR / f"{house_page}.json"

    record = {
        "house_page": house_page,
        "slug": slug,
        "status": "error",
        "format": None,
        "url_tried": [],
        "saved_path": None,
        "size_bytes": None,
        "detail": None,
    }

    if not raw_path.exists():
        record["detail"] = f"raw JSON not found: {raw_path}"
        return record

    try:
        with open(raw_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        record["detail"] = f"failed to parse raw JSON: {e}"
        return record

    html = data.get("html", "")
    thumb_src = extract_sigil_thumb_src(html)
    if not thumb_src:
        record["detail"] = "no infobox-image <img> found in HTML"
        return record

    original_url_path = thumb_src_to_original_url(thumb_src)
    candidates = []
    if original_url_path:
        candidates.append(("svg-original", BASE_URL + original_url_path))
    candidates.append(("thumbnail-fallback", BASE_URL + thumb_src))

    for label, url in candidates:
        record["url_tried"].append({"label": label, "url": url})
        try:
            status_code, content = download(scraper, url, verbose=verbose)
        except Exception as e:
            record["detail"] = f"{label} request failed: {type(e).__name__}: {e}"
            time.sleep(SLEEP_BETWEEN_REQUESTS)
            continue

        time.sleep(SLEEP_BETWEEN_REQUESTS)

        if status_code != 200 or not content:
            record["detail"] = f"{label} returned HTTP {status_code}"
            continue

        kind = classify_bytes(content)
        if kind in ("svg", "png", "webp", "jpg"):
            ext = kind
        else:
            record["detail"] = f"{label} returned non-image content (sniffed as '{kind}')"
            continue

        out_path = output_dir / f"{slug}.{ext}"
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as out_f:
            out_f.write(content)

        record["status"] = "ok"
        record["format"] = ext
        record["saved_path"] = str(out_path)
        record["size_bytes"] = len(content)
        record["detail"] = f"downloaded via {label}"
        return record

    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--smoke5", action="store_true",
        help="Fetch exactly the 5-house smoke set (Stark/Lannister/Targaryen/Baratheon/Tyrell)",
    )
    parser.add_argument(
        "--houses", nargs="+", default=None,
        help="Explicit list of House_<Name> page names to fetch (e.g. House_Stark House_Frey)",
    )
    parser.add_argument(
        "--from-sigil-data", type=Path, default=None, nargs="?", const=DEFAULT_SIGIL_DATA,
        help=f"Read (wiki_page, slug) pairs from a sigil-data.jsonl file "
             f"(default: {DEFAULT_SIGIL_DATA}); fetches every record with a "
             f"non-null sigil_image. Resumable — skips slugs already on disk.",
    )
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument(
        "--no-resume", action="store_true",
        help="With --from-sigil-data, re-fetch even slugs that already have a file on disk",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    # Build the work list as (house_page, slug) pairs.
    if args.from_sigil_data:
        if not args.from_sigil_data.exists():
            print(f"sigil-data file not found: {args.from_sigil_data}", file=sys.stderr)
            return 1
        records = load_sigil_data(args.from_sigil_data)
        pairs = [(r["wiki_page"], r["slug"]) for r in records]
        print(f"Loaded {len(pairs)} record(s) with non-null sigil_image from {args.from_sigil_data}")
    elif args.houses:
        pairs = [(h, house_to_slug(h)) for h in args.houses]
    elif args.smoke5:
        pairs = [(h, house_to_slug(h)) for h in SMOKE5_HOUSES]
    else:
        print("Nothing to do — pass --smoke5, --houses <House_X> [...], or --from-sigil-data",
              file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Resumability: skip slugs that already have a downloaded file, unless
    # --no-resume was passed.
    skipped = []
    if not args.no_resume:
        remaining = []
        for house_page, slug in pairs:
            existing = already_downloaded(slug, args.output_dir)
            if existing:
                skipped.append((house_page, slug, existing))
            else:
                remaining.append((house_page, slug))
        pairs = remaining

    print(f"To fetch: {len(pairs)}   Already on disk (skipped): {len(skipped)}")
    print(f"Output dir: {args.output_dir}")
    if pairs:
        est_seconds = len(pairs) * SLEEP_BETWEEN_REQUESTS * 1.1  # rough, allows for 2nd-try fallback overhead
        print(f"Estimated time: ~{est_seconds / 60:.1f} min (at {SLEEP_BETWEEN_REQUESTS}s/request, 1 request typical)")
    print()

    if not pairs:
        print("Nothing to fetch — all requested houses already downloaded.")
        return 0

    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "darwin", "mobile": False}
    )
    scraper.headers.update({"User-Agent": USER_AGENT})

    results = []
    total = len(pairs)
    start = time.time()
    for i, (house_page, slug) in enumerate(pairs, start=1):
        if args.verbose:
            print(f"--- [{i}/{total}] {house_page} ({slug}) ---")
        rec = fetch_house_sigil(scraper, house_page, slug, args.output_dir, verbose=args.verbose)
        results.append(rec)
        if rec["status"] == "ok":
            if args.verbose:
                print(f"  OK: {rec['format'].upper()} ({rec['size_bytes']:,} bytes) -> {rec['saved_path']}")
        else:
            print(f"  [{i}/{total}] FAILED {house_page} ({slug}): {rec['detail']}")

        if not args.verbose and i % 25 == 0:
            elapsed = time.time() - start
            rate = i / elapsed if elapsed > 0 else 0
            eta = (total - i) / rate if rate > 0 else 0
            ok_so_far = sum(1 for r in results if r["status"] == "ok")
            print(f"  progress: {i}/{total}  ok={ok_so_far}  elapsed={elapsed:.0f}s  eta={eta:.0f}s")

    ok = [r for r in results if r["status"] == "ok"]
    failed = [r for r in results if r["status"] != "ok"]
    svg_count = sum(1 for r in ok if r["format"] == "svg")
    png_count = sum(1 for r in ok if r["format"] == "png")
    other_count = len(ok) - svg_count - png_count
    total_bytes = sum(r["size_bytes"] for r in ok)

    elapsed = time.time() - start
    print()
    print("=== Summary ===")
    print(f"Attempted this run:  {total}")
    print(f"Succeeded:           {len(ok)}")
    print(f"Failed:              {len(failed)}")
    print(f"Skipped (resumed):   {len(skipped)}")
    print(f"  SVG (original):    {svg_count}")
    print(f"  PNG (fallback):    {png_count}")
    if other_count:
        print(f"  Other format:      {other_count}")
    print(f"Total bytes (this run): {total_bytes:,} ({total_bytes / 1024:.1f} KB)")
    print(f"Elapsed: {elapsed:.1f}s")
    if failed:
        print()
        print(f"Failed houses ({len(failed)}):")
        for r in failed:
            urls = "; ".join(u["url"] for u in r["url_tried"]) if r["url_tried"] else "n/a"
            print(f"  {r['house_page']:<30} slug={r['slug']:<30} reason={r['detail']}  urls_tried=[{urls}]")

    return 0 if not failed else 2


if __name__ == "__main__":
    sys.exit(main())
