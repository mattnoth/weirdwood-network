# Session 3 — Wiki Crawl Planning + Smoke Test

**Date:** 2026-04-13

---

## What Triggered This Session

The wiki scraper existed but was blocked on Cloudflare (Session 2's ending blocker). Before tackling that problem, there was a strategic question to resolve: what should the scraper actually scrape? The original plan was targeted scraping — fetch pages for known entities (major characters, key locations) as needed. But was that the right approach?

## What Happened

### The Strategic Shift: Targeted vs. Full Crawl

This session's most important outcome wasn't code — it was a change in strategy.

The original scraping plan was surgical: identify entities from extraction outputs, scrape their wiki pages, use that data to enrich the graph. This sounds efficient. You only fetch what you need. But it has a fundamental problem: you don't know what you need until you've extracted it, and extraction is iterative. Every new pass might surface entities that weren't on the list. You'd be constantly going back to the wiki for pages you didn't think to scrape earlier.

The alternative: scrape the entire wiki upfront, then triage the cache. The AWOIAF wiki has roughly 18,000 pages. That sounds like a lot, but each page is a small JSON blob plus some markdown. The entire cache would fit comfortably on disk. Scraping is a one-time operation (with occasional refreshes); classification and ingestion can be refined indefinitely against the static cache.

The reasoning came down to a principle: **scraping is cheap, re-scraping is annoying, and the wiki is a reference layer, not the graph itself.** The cache in `sources/wiki/` is gitignored — it's working material, not a committed artifact. The graph nodes (in `graph/nodes/`) that get promoted from wiki data ARE committed. So there's no cost to having a large cache; the only thing that matters is the quality of the promotion pipeline from cache to graph.

Matt and Claude aligned on this: full crawl, then triage. This decision shaped everything downstream — the wiki became a comprehensive reference layer rather than a sparse supplement.

### Reviewing the Scraper's Capabilities

Before planning the crawl, the existing scraper code was reviewed to confirm it was up to the task. Key finding: it already extracted full page text, not just summaries. Each output file gets a `## Full Text` section containing the cleaned article body. This meant the full crawl would capture complete wiki content — infobox data, prose, cross-references, everything.

### Adding --mode all

The scraper needed a new mode. It had `--entity` (single page) and `--category` (all pages in a wiki category), but no way to enumerate and fetch every page on the wiki. The script-builder subagent was delegated to add:

- `--mode all` — fetches the complete title list from the MediaWiki API, then processes every page
- `--limit N` — process only the first N pages (for testing and incremental runs)

The MediaWiki API provides a `list=allpages` endpoint that returns all page titles, paginated. The scraper would fetch the full title list first, then iterate through it, skipping pages already in the cache (for resumability).

### The Smoke Test

With `--mode all` implemented, a 5-page smoke test was run:

```
python3 scripts/wiki-scraper.py --mode all --limit 5 -v
```

All 5 pages succeeded. The title list fetch also succeeded, returning 17,952 total pages on the wiki. This confirmed three things:
1. The `--mode all` enumeration worked correctly
2. The scraper could fetch, parse, classify, and write wiki pages end-to-end
3. The full crawl scope was ~18,000 pages — large but tractable

(Note: this smoke test presumably used `urllib` and happened to succeed, or the Cloudflare issue was intermittent. The consistent Cloudflare blocking that required the Playwright migration came when attempting the full unattended crawl in Session 4.)

### Gitignore Update

The `.gitignore` was updated to exclude all of `sources/wiki/`, not just `sources/wiki/_raw/`. The full wiki cache — classified pages in their entity-type subdirectories, uncategorized pages, raw API responses — is all regenerable from the scraper. None of it belongs in git. The graph nodes that eventually get promoted from wiki data are the committed artifacts; the wiki cache is working material.

### The Runbook

A runbook was written at `working/runbooks/wiki-full-crawl.md` with step-by-step instructions for running the full crawl. This established a pattern: long-running unattended tasks get runbooks.

The reasoning: the full crawl would take hours (18,000 pages, with rate limiting to avoid getting banned). It would run in a terminal while Matt did other things. If it failed partway through, someone (Matt or a future Claude session) needed to know how to resume it, what to check, and what success looks like. A runbook captures that operational knowledge.

The runbook included:
- Prerequisites (dependencies, disk space estimates)
- The exact command to run
- How to monitor progress
- How to resume after interruption (the scraper skips cached pages)
- Expected output and how to verify completeness
- Troubleshooting common failures

## Key Decisions and Why

| Decision | Reasoning |
|----------|-----------|
| Full crawl, not targeted scraping | Scraping is cheap and one-time; the cache is gitignored working material; targeted scraping requires knowing what you need before you need it |
| `sources/wiki/` fully gitignored | Wiki content is a reference layer, regenerable from cache. Graph nodes are the committed artifact. |
| Runbooks for long-running tasks | Operational knowledge needs to survive between sessions. A runbook means anyone can resume or re-run the task. |
| `--limit N` for incremental testing | Full crawl is 18,000 pages; you want to test with 5 before committing to hours of scraping |

## What Was Left Open

- The actual full crawl hadn't been run yet — just the 5-page smoke test. The full crawl attempt (Session 4) would immediately hit the Cloudflare wall, requiring a Playwright migration.
- Classification quality was untested at scale — the 5 smoke-test pages might not be representative. With ~18,000 pages, the `_uncategorized/` bucket would likely be very large (it ended up being ~17,305 of 17,657 pages, with only ~350 classifying into the five known entity types). This wasn't a failure — it was expected, since the wiki contains pages for battles, regions, songs, foods, customs, and dozens of other categories that the initial 5-type classification scheme didn't cover.
- The connection between wiki data and the extraction pipeline was still abstract. How exactly would wiki content enrich the graph? What would "Pass 2: Wiki Ingestion" actually do? These were design questions for a later session — the immediate priority was getting the data.
