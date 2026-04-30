# [ARCHIVED — DO NOT EXECUTE] Runbook: Full AWOIAF Wiki Crawl

> **STATUS: COMPLETE.** The full crawl ran in April 2026. All 17,945 pages are cached locally at `sources/wiki/_raw/`. Do NOT re-run this crawl. The Playwright scraper (`scripts/wiki-scraper.py`) has been moved to `scripts/archive/wiki-scraper.py.archive`. Pass 2+ work uses local cache only.
>
> Kept for historical reference only.

---

**Original purpose:** One-time unattended crawl of every page on A Wiki of Ice and Fire
into `sources/wiki/`. Run from a Claude CLI session launched with
`--dangerously-skip-permissions` so it can run without supervision.

**Expected runtime:** ~6–8 hours (17,952 pages × ~1.5 sec/page with Playwright overhead)
**Expected disk:** 1.0–1.8 GB in `sources/wiki/` (gitignored)

---

## Instructions for the Claude CLI agent following this runbook

You are running a long shell task. Do not delegate to subagents. Do not modify
[scripts/wiki-scraper.py](../../scripts/wiki-scraper.py). Do not run any
extraction passes. Do not promote anything into `graph/nodes/`. Do not commit
anything. Your only job is to run the scraper and report results.

### Step 1 — Pre-flight checks

Before starting the crawl, verify:

1. **Playwright installed.** Confirm with:
   `python3 -c "from playwright.sync_api import sync_playwright; print('OK')"`
   If it fails, run: `pip3 install playwright && playwright install chromium`
2. **Title list cache.** Check whether `sources/wiki/_raw/.all-pages.json`
   exists. If it does, the crawl will reuse it (no re-fetch of the title
   list). If it doesn't, the script will fetch it fresh — that's fine, just
   adds ~30 seconds.
3. **Disk space.** Run `df -h .` and confirm at least 5 GB free. The crawl
   will likely use 1–2 GB but headroom matters for cache + parsing.

If any check fails, stop and report. Do not try to "fix" things.

### Step 2 — Launch the crawl

Run in the foreground (NOT background — you need to monitor it):

```
python3 scripts/wiki-scraper.py --mode all -v
```

A Chromium browser window will open. The first page load may show a Cloudflare
"Just a moment..." challenge. If it auto-resolves within a few seconds, great.
If you see a "Verify you are human" button, **tell the user to click it** —
the script will wait up to 120 seconds for the challenge to resolve.

Once the warmup passes, the script installs a cookie injector and the crawl
proceeds automatically.

The script will:
- Reuse the cached title list if present
- Skip any page already cached in `sources/wiki/_raw/` (so prior runs are
  free to resume)
- Stream per-page status to `sources/wiki/_raw/.crawl-progress.log`
- Abort cleanly after 3 consecutive failures

### Step 3 — Handling expected failure modes

**Cloudflare interactive challenge:** If the script detects a Cloudflare
challenge during warmup, it will print instructions and wait for the user to
click "Verify you are human" in the browser window. If running headless, try
re-running without `--headless`.

**Network errors / transient failures:** The script's per-request error
handling already covers these. If the crawl runs to completion despite some
individual page failures showing in the output, that's normal — report them
in the summary but don't retry manually.

**3 consecutive failures:** The script aborts to prevent spinning. This usually
means Cloudflare is requiring a new interactive challenge or there's a network
issue. Re-run the same command — cached pages are skipped automatically.

**Anything else weird:** Stop and report. Do not improvise.

### Step 4 — Final report

When the crawl finishes (or aborts), report:

- Total pages successfully scraped (from the script's summary)
- Total pages failed (with a sample of failure reasons if any)
- Final disk footprint: `du -sh sources/wiki/` and the breakdown of
  `sources/wiki/_raw/` vs the per-entity-type subdirectories
- Pages-per-entity-type breakdown (the script prints this)
- Count of pages that landed in `sources/wiki/_uncategorized/` (just the
  count — do not list them)
- Any anomalies you noticed (lots of failures clustered around one letter,
  unexpected page types, etc.)

### Step 5 — Worklog update

Append a one-paragraph entry to [worklog.md](../../worklog.md) noting:
- Date (today)
- Total pages scraped
- Final disk footprint
- Any anomalies or follow-ups for the next session

That's it. Stop there. Pass 2 (wiki ingestion → graph nodes) is a separate
decision for a later session — do not start it.

---

## Notes for the human iterating this runbook

- **Browser window:** The scraper runs in headed mode (visible browser) by
  default. This is the most reliable against Cloudflare. Pass `--headless`
  if you need headless, but it may trigger more challenges.
- **Cloudflare challenges:** If the initial warmup triggers a Turnstile
  challenge, you need to click it once. After that the session persists for
  the full crawl.
- **Script changes:** if you want to change crawl behavior (different rate
  limit, different namespaces, etc.), edit [scripts/wiki-scraper.py](../../scripts/wiki-scraper.py)
  in a planning session first. Don't tell the runbook agent to modify it.
- **Re-running with a fresh start:** the title list is cached at
  `sources/wiki/_raw/.all-pages.json` and individual pages at
  `sources/wiki/_raw/{slug}.json`. To force a full refetch, delete those
  files first. To resume after interruption, just re-run — cached pages are
  skipped automatically.
- **Smoke testing the runbook itself:** add `--limit 5` to the python
  command in Step 2 if you want to sanity-check the runbook before
  committing to the full ~6–8hr run.
