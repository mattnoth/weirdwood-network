#!/usr/bin/env python3
"""Bounded AWOIAF character-portrait image backfill — completion-of-original-crawl operation.

The original wiki crawl (`scripts/archive/wiki-scraper.py.archive`) saved page
HTML only — it never downloaded the image binaries referenced by that HTML
(sigils, portraits, maps). `scripts/wiki-fetch-sigils.py` filled the house-sigil
gap; this script fills the sibling gap for `character.*` node portrait images.

For a given character page's cached raw JSON (`sources/wiki/_raw/<Page>.json`),
this script:
  1. Parses the `<table class="infobox">` in `data["html"]` and locates the
     first `<img>` inside the `infobox-image` cell (the portrait image).
     Follows a single level of MediaWiki redirect if the page itself is a
     redirect stub (e.g. `Robert_Baratheon` -> `Robert_I_Baratheon`).
  2. Derives the ORIGINAL (non-thumbnail) file URL by stripping the `/thumb/`
     segment and the trailing `NNNpx-...` resize segment from the thumbnail
     src, e.g.:
       thumb: /images/thumb/9/9e/Robert_Baratheon_by_Antonio_J_Manzanedo.jpg/350px-....jpg
       orig:  /images/9/9e/Robert_Baratheon_by_Antonio_J_Manzanedo.jpg
  3. Tries the original file first; falls back to the thumbnail if the
     original 404s or is otherwise unavailable.
  4. Verifies the downloaded bytes are a real image by magic-byte sniff (JPG,
     PNG, WebP, or SVG) — never trusts the URL extension, and never saves an
     HTML error / Cloudflare-challenge page.

Per CLAUDE.md "Approved exception fetches" — this is a single bounded fetch,
approved 2026-06-30 (per-turn authorization), targeting one specific data
field (portrait images), written to `working/wiki/portraits/` ONLY — never to
`sources/`.

Cloudflare bypass: uses the `cloudscraper` library (verified working for this
project since 2026-04-30's category backfill; reused unchanged from
wiki-fetch-sigils.py's approach).

SMOKE TEST MODE (the only mode exercised so far): --smoke-n N fetches exactly
the top N portrait-available candidates from a ranked manifest
(working/wiki/data/portrait-candidates.jsonl by default). Per the 2026-06-30
task, the smoke run is EXACTLY 5 and then STOPS — do not scale beyond 5
without a fresh Matt greenlight.

FULL-SCALE MODE (NOT yet greenlit): --from-candidates reads the same
manifest and fetches every record with `portrait_status == "ok"`. Resumable —
any slug that already has a file (any extension) in the output dir is
skipped.

Usage:
    python3 scripts/wiki-fetch-portraits.py --smoke-n 5
    python3 scripts/wiki-fetch-portraits.py --slugs jon-snow tyrion-lannister
    python3 scripts/wiki-fetch-portraits.py --from-candidates working/wiki/data/portrait-candidates.jsonl --limit 100
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import unquote

import cloudscraper

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
RAW_WIKI_DIR = PROJECT_ROOT / "sources" / "wiki" / "_raw"
OUTPUT_DIR = PROJECT_ROOT / "working" / "wiki" / "portraits"
DEFAULT_CANDIDATES = PROJECT_ROOT / "working" / "wiki" / "data" / "portrait-candidates.jsonl"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BASE_URL = "https://awoiaf.westeros.org"
SLEEP_BETWEEN_REQUESTS = 1.8  # seconds; throttled per hard constraints
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

INFOBOX_IMG_RE = re.compile(
    r'infobox-image.*?<img[^>]+src="([^"]+)"', re.DOTALL
)
REDIRECT_RE = re.compile(
    r'<div class="redirectMsg">.*?href="/index\.php/([^"]+)"', re.DOTALL
)


def thumb_src_to_original_url(thumb_src: str) -> str | None:
    """Derive the original (non-thumbnail) image URL from a thumbnail src.

    thumb: /images/thumb/9/9e/Robert_Baratheon_by_Antonio_J_Manzanedo.jpg/350px-....jpg
    orig:  /images/9/9e/Robert_Baratheon_by_Antonio_J_Manzanedo.jpg

    Returns None if the src doesn't look like a /images/thumb/... path
    (i.e. it's already a direct, non-thumbnail image).
    """
    m = re.match(r"^/images/thumb/(.+)/[0-9]+px-[^/]+$", thumb_src)
    if not m:
        return None
    return f"/images/{m.group(1)}"


def find_infobox_image_src(wiki_page: str, _redirected: bool = False) -> str | None:
    """Find the portrait <img src> for wiki_page, following one level of
    MediaWiki redirect if the page itself has no infobox image but is a
    redirect stub."""
    raw_path = RAW_WIKI_DIR / f"{wiki_page}.json"
    if not raw_path.exists():
        return None
    try:
        with open(raw_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return None
    html = data.get("html", "")
    m = INFOBOX_IMG_RE.search(html)
    if m:
        return m.group(1)
    if not _redirected:
        redirect_m = REDIRECT_RE.search(html)
        if redirect_m:
            target_page = unquote(redirect_m.group(1))
            return find_infobox_image_src(target_page, _redirected=True)
    return None


def classify_bytes(content: bytes) -> str:
    """Return 'jpg', 'png', 'webp', 'svg', 'html', or 'unknown' based on
    magic bytes / content sniff. Never trust the URL extension."""
    stripped = content.lstrip()
    if content.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if content[:4] == b"RIFF" and content[8:12] == b"WEBP":
        return "webp"
    if stripped.startswith(b"<?xml") or stripped.startswith(b"<svg") or b"<svg" in stripped[:500]:
        return "svg"
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
    for ext in ("jpg", "jpeg", "png", "webp", "svg"):
        candidate = output_dir / f"{slug}.{ext}"
        if candidate.exists() and candidate.stat().st_size > 0:
            return candidate
    return None


def load_candidates(path: Path, only_available: bool = True) -> list[dict]:
    """Load portrait-candidates.jsonl rows, optionally filtered to
    portrait_status == 'ok'."""
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
            if only_available and rec.get("portrait_status") != "ok":
                continue
            records.append(rec)
    return records


def fetch_portrait(scraper, wiki_page: str, slug: str, output_dir: Path, verbose: bool = False) -> dict:
    """Fetch and save the portrait image for one character. Returns a result record."""
    record = {
        "wiki_page": wiki_page,
        "slug": slug,
        "status": "error",
        "format": None,
        "url_tried": [],
        "saved_path": None,
        "size_bytes": None,
        "detail": None,
    }

    thumb_src = find_infobox_image_src(wiki_page)
    if not thumb_src:
        record["detail"] = "no infobox-image <img> found in HTML (incl. one redirect hop)"
        return record

    original_url_path = thumb_src_to_original_url(thumb_src)
    candidates = []
    if original_url_path:
        candidates.append(("original", BASE_URL + original_url_path))
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
        if kind in ("jpg", "png", "webp", "svg"):
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
        "--smoke-n", type=int, default=None,
        help="Fetch exactly the top N portrait-available candidates from the ranked manifest, then stop. "
             "Per the 2026-06-30 approved exception, use --smoke-n 5 and no more without a fresh greenlight.",
    )
    parser.add_argument(
        "--slugs", nargs="+", default=None,
        help="Explicit list of character slugs to fetch (looked up against the candidates manifest for wiki_page).",
    )
    parser.add_argument(
        "--from-candidates", type=Path, default=None, nargs="?", const=DEFAULT_CANDIDATES,
        help=f"Read (wiki_page, slug) pairs from a portrait-candidates.jsonl file "
             f"(default: {DEFAULT_CANDIDATES}); fetches every record with "
             f"portrait_status == 'ok', optionally capped by --limit. Resumable.",
    )
    parser.add_argument("--limit", type=int, default=None, help="Cap the number of records fetched with --from-candidates")
    parser.add_argument("--candidates-file", type=Path, default=DEFAULT_CANDIDATES,
                         help="Manifest path used by --smoke-n / --slugs lookups")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument(
        "--no-resume", action="store_true",
        help="Re-fetch even slugs that already have a file on disk",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    # Build the work list as (wiki_page, slug) pairs.
    if args.from_candidates:
        if not args.from_candidates.exists():
            print(f"candidates file not found: {args.from_candidates}", file=sys.stderr)
            return 1
        records = load_candidates(args.from_candidates, only_available=True)
        if args.limit:
            records = records[: args.limit]
        pairs = [(r["wiki_page"], r["slug"]) for r in records]
        print(f"Loaded {len(pairs)} record(s) with portrait_status=='ok' from {args.from_candidates}")
    elif args.smoke_n is not None:
        if not args.candidates_file.exists():
            print(f"candidates file not found: {args.candidates_file}", file=sys.stderr)
            return 1
        records = load_candidates(args.candidates_file, only_available=True)
        records = records[: args.smoke_n]
        pairs = [(r["wiki_page"], r["slug"]) for r in records]
        print(f"Smoke test: top {len(pairs)} portrait-available candidate(s) from {args.candidates_file}")
    elif args.slugs:
        if not args.candidates_file.exists():
            print(f"candidates file not found: {args.candidates_file}", file=sys.stderr)
            return 1
        by_slug = {}
        with open(args.candidates_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                by_slug[rec["slug"]] = rec
        pairs = []
        for slug in args.slugs:
            rec = by_slug.get(slug)
            if not rec or not rec.get("wiki_page"):
                print(f"  WARNING: slug '{slug}' not found in manifest or has no wiki_page — skipping", file=sys.stderr)
                continue
            pairs.append((rec["wiki_page"], slug))
    else:
        print("Nothing to do — pass --smoke-n N, --slugs <slug> [...], or --from-candidates",
              file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Resumability: skip slugs that already have a downloaded file, unless
    # --no-resume was passed.
    skipped = []
    if not args.no_resume:
        remaining = []
        for wiki_page, slug in pairs:
            existing = already_downloaded(slug, args.output_dir)
            if existing:
                skipped.append((wiki_page, slug, existing))
            else:
                remaining.append((wiki_page, slug))
        pairs = remaining

    print(f"To fetch: {len(pairs)}   Already on disk (skipped): {len(skipped)}")
    print(f"Output dir: {args.output_dir}")
    if pairs:
        est_seconds = len(pairs) * SLEEP_BETWEEN_REQUESTS * 1.1
        print(f"Estimated time: ~{est_seconds / 60:.1f} min (at {SLEEP_BETWEEN_REQUESTS}s/request, 1 request typical)")
    print()

    if not pairs:
        print("Nothing to fetch — all requested characters already downloaded.")
        return 0

    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "darwin", "mobile": False}
    )
    scraper.headers.update({"User-Agent": USER_AGENT})

    results = []
    total = len(pairs)
    start = time.time()
    for i, (wiki_page, slug) in enumerate(pairs, start=1):
        print(f"--- [{i}/{total}] {wiki_page} ({slug}) ---")
        rec = fetch_portrait(scraper, wiki_page, slug, args.output_dir, verbose=args.verbose)
        results.append(rec)
        if rec["status"] == "ok":
            print(f"  OK: {rec['format'].upper()} ({rec['size_bytes']:,} bytes) -> {rec['saved_path']}")
        else:
            print(f"  FAILED {wiki_page} ({slug}): {rec['detail']}")

        if not args.verbose and i % 25 == 0:
            elapsed = time.time() - start
            rate = i / elapsed if elapsed > 0 else 0
            eta = (total - i) / rate if rate > 0 else 0
            ok_so_far = sum(1 for r in results if r["status"] == "ok")
            print(f"  progress: {i}/{total}  ok={ok_so_far}  elapsed={elapsed:.0f}s  eta={eta:.0f}s")

    ok = [r for r in results if r["status"] == "ok"]
    failed = [r for r in results if r["status"] != "ok"]
    jpg_count = sum(1 for r in ok if r["format"] == "jpg")
    png_count = sum(1 for r in ok if r["format"] == "png")
    webp_count = sum(1 for r in ok if r["format"] == "webp")
    svg_count = sum(1 for r in ok if r["format"] == "svg")
    total_bytes = sum(r["size_bytes"] for r in ok)

    elapsed = time.time() - start
    print()
    print("=== Summary ===")
    print(f"Attempted this run:  {total}")
    print(f"Succeeded:           {len(ok)}")
    print(f"Failed:              {len(failed)}")
    print(f"Skipped (resumed):   {len(skipped)}")
    print(f"  JPG:               {jpg_count}")
    print(f"  PNG:               {png_count}")
    print(f"  WebP:              {webp_count}")
    print(f"  SVG:               {svg_count}")
    print(f"Total bytes (this run): {total_bytes:,} ({total_bytes / 1024:.1f} KB)")
    print(f"Elapsed: {elapsed:.1f}s")
    if failed:
        print()
        print(f"Failed characters ({len(failed)}):")
        for r in failed:
            urls = "; ".join(u["url"] for u in r["url_tried"]) if r["url_tried"] else "n/a"
            print(f"  {r['wiki_page']:<30} slug={r['slug']:<30} reason={r['detail']}  urls_tried=[{urls}]")

    return 0 if not failed else 2


if __name__ == "__main__":
    sys.exit(main())
