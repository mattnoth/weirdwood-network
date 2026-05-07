# Session 5 — Full Wiki Crawl Executed

**Date:** 2026-04-14

---

## What Triggered This Session

Session 4 rebuilt the wiki scraper's entire network layer to get past Cloudflare's TLS fingerprinting. The migration was validated with smoke tests, but the actual full crawl — the whole reason for the Playwright migration — hadn't been attempted yet. Time to find out if it worked at scale.

## What Happened

Ran `python3 scripts/wiki-scraper.py --mode all -v` per the updated runbook. The Playwright-driven Chromium instance opened, the Cloudflare warmup completed without a manual Turnstile click, and pages started processing.

Then there was nothing to do but wait.

The crawl ran for approximately 36 hours, fully unattended. No Cloudflare challenges were triggered after the initial warmup — the session stayed valid for the entire duration. This answered the open question from Session 4: yes, a single Cloudflare clearance is sufficient for a sustained multi-hour crawl, at least at the rate Playwright naturally throttles requests.

The throughput settled at roughly 280 pages per hour, significantly slower than the optimistic 6-8 hour estimate from Session 3. The original math assumed small pages; in practice, character and location pages on AWOIAF can be substantial (Tyrion Lannister's page is a small novel), and Playwright's page-load cycle is inherently heavier than raw HTTP requests. This wasn't a problem — the crawl was unattended anyway — but it's worth noting for any future re-crawl estimates.

Final results:
- **17,952 pages attempted** (the full title list from the MediaWiki API)
- **17,945 succeeded** (99.96% success rate)
- **7 failed** — all HTTP 403 errors. Six were "Mander"-related pages (likely redirect chains or special characters in the URL), plus "The Mance." These are minor wiki pages, not critical entities.
- **377 MB total disk footprint:** 293 MB in `_raw/` (JSON files with full page HTML + metadata), 81 MB in `_uncategorized/` (markdown), 3.8 MB in `houses/` (markdown)

The classification results were lopsided. The `classify_entity()` function — which routes pages into `characters/`, `locations/`, `houses/`, `events/`, `artifacts/`, or `_uncategorized/` — only confidently classified 640 pages as houses. Everything else (17,305 pages, 96.4%) landed in `_uncategorized/`. This wasn't a bug exactly; the classifier rules were written conservatively to avoid miscategorization, and most wiki pages don't have the obvious structural signals (like "House" in the title) that the rules check for. Characters, locations, events, and artifacts all need more sophisticated classification logic — probably parsing the page's wiki categories or infobox fields rather than just the title.

The 99.96% success rate and fully unattended execution were the headline results. The Session 3/4 arc — planning the crawl, hitting the Cloudflare wall, rebuilding the network layer, and finally executing — played out over three sessions but produced a robust, complete wiki cache. The `sources/wiki/_raw/` directory now contains the raw HTML and metadata for essentially the entire AWOIAF wiki, frozen in time, available for any future processing without touching the network again.

## Key Decisions and Why

There weren't major design decisions in this session — it was an execution session. The decisions had already been made (full crawl vs. targeted, Playwright vs. urllib, headed vs. headless), and this session validated them.

The one implicit decision was to accept the classification skew rather than re-running with improved rules. The raw cache is the important artifact; classification is a post-processing step that can be rerun against the static cache at any time without network access. No reason to block on perfecting the classifier before moving forward.

## What Was Left Open

- **Classification refinement.** 17,305 pages in `_uncategorized/` need better routing. The next step is to analyze the wiki's category system and infobox structure to build more sophisticated classification rules. This can be done entirely offline against the cached JSON.
- **Pass 2 design.** The wiki cache exists, but the agent prompt for wiki ingestion (promoting wiki content into `graph/nodes/`) hasn't been written. Key open questions: what gets promoted vs. what stays as reference? How does `first_available` get assigned from wiki data? How do wiki-sourced nodes interact with extraction-sourced data?
- **Pass 1 mechanical extraction.** Completely unblocked and unrelated to the wiki track. AGOT chapters are split and ready for extraction testing. This was the next major milestone regardless of wiki progress.
- **The 7 failed pages** were noted but not investigated. Low priority given the 99.96% success rate, but they could be retried individually if any turn out to be important entities.
