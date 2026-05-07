# Worklog Archive — Sessions 0–4

> Archived 2026-04-22. These sessions cover project genesis through wiki crawl completion.

---

### Session 4 — Playwright Migration for Wiki Scraper (2026-04-13)
**What happened:**
- Attempted full wiki crawl per runbook — immediately failed. The `cf_clearance` cookie from Session 3 had expired, and a fresh cookie also failed.
- Diagnosed the root cause: Cloudflare blocks ALL requests from urllib/curl regardless of cookies — TLS fingerprinting rejects non-browser connections.
- Migrated `scripts/wiki-scraper.py` from stdlib urllib to Playwright (browser automation):
  - Removed: `ssl`, `urllib.request`, `urllib.error` imports; `_build_ssl_context()`, `load_cookies_from_file()` functions; `COOKIES_FILE`, `_COOKIES`, `_SSL_CONTEXT` variables; `--cookies` CLI arg
  - Added: Playwright browser lifecycle (`_launch_browser`, `_close_browser`), Cloudflare warmup with Turnstile polling (`_warmup_cloudflare`), `--headless` CLI flag (default: headed for Cloudflare reliability)
  - All parsing, classification, caching, and markdown-writing code untouched
- Discovered and fixed a Chromium/Playwright bug: `cf_clearance` cookie (httpOnly + sameSite=None) was stored in the browser context but NOT sent on subsequent navigations. Workaround: route interceptor that manually injects the cookie header on every outgoing request.
- Smoke tested: `--entity "Tyrion Lannister"` (1/1 success) and `--mode all --limit 10` (10/10 success, including the 3 pages that previously failed with urllib).
- Updated runbook for Playwright (no more cookie file, browser window opens, may need one manual Turnstile click).
- New dependency: `pip3 install playwright && playwright install chromium` (Chromium ~91 MB in `~/.cache/ms-playwright/`)

**Key decisions made:**
- Playwright headed mode is the default — headless is detectable by Cloudflare
- Cookie file approach (`sources/wiki/_raw/.cookies`) is dead — Playwright handles sessions natively
- Route-based cookie injection is the workaround for the Chromium cookie-sending bug

---

### Session 3 — Wiki Crawl Planning + Smoke Test (2026-04-13)
**What happened:**
- Reviewed `scripts/wiki-scraper.py` and confirmed it already extracts full page text (not just summaries) — the `## Full Text` section in each output file gets the cleaned article body.
- Discussed scope: shifted from targeted scraping to **full crawl, then triage**. Rationale: scraping is cheap, classification can be refined against a static cache, and `sources/wiki/` is a reference layer not the graph itself.
- Updated `.gitignore` to exclude all of `sources/wiki/` (was previously only excluding `_raw/`). Wiki content is regenerable from cache; graph nodes (which are committed) are the canonical artifact.
- Delegated to `script-builder` to add `--mode all` and `--limit N` to the scraper.
- Ran 5-page smoke test (`--mode all --limit 5 -v`): all 5 succeeded. Title list fetched: 17,952 total pages.
- Wrote runbook at `working/runbooks/wiki-full-crawl.md`.

**Key decisions made:**
- Wiki ingestion scope: **full crawl, not targeted**
- `sources/wiki/` is fully gitignored — reference layer, not graph artifact
- Long-running unattended tasks get runbooks in `working/runbooks/`

---

### Session 2 — Foundation Builder: Chapter Splitter + Wiki Scraper (2026-04-13)
**What happened:**
- Wrote `scripts/chapter-splitter.py` — splits source .txt files into per-chapter markdown with YAML frontmatter
- Ran splitter on all 5 books — all counts match expected: AGOT 73, ACOK 70, ASOS 82, AFFC 46, ADWD 73 (344 total)
- Discovered 6 missing chapter headings in `reference/pov-characters.md`. Added all.
- Wrote `scripts/wiki-scraper.py` (1213 lines, stdlib-only) — scrapes AWOIAF MediaWiki API
- Created wiki directory structure and taxonomy candidates template

**Blockers:** Wiki scraper blocked on Cloudflare cookies.

**Key decisions made:**
- Chapter splitter uses prose-detection heuristic (not gap-based)
- Wiki scraper is stdlib-only (no pip dependencies)

---

### Session 1 — Project Scaffolding & Cleanup (2026-04-13)
**What happened:**
- Created full directory skeleton from architecture spec
- Created .gitignore FIRST — protects copyrighted content
- Set up .claude/agents/ with 7 subagent definitions
- Cleaned up root: moved specs to `reference/`, deleted integrated files
- Created `working/` directory with `progress.md` and `todos.md`

**Key decisions made:**
- Local directory stays as `asoiaf-chat`; GitHub repo will be `the-weirwood-network`
- Copyrighted content must NEVER enter git history
- Later-pass agents organized as stubs with TODOs

---

### Session 0 — Project Genesis
**What happened:**
- Designed overall system architecture with Claude
- Designed six-pass extraction pipeline
- Created foundational documents: CONTEXT.md, pass-1 agent prompt, foreshadowing events, chapter splitter agent, worklog

**Key design decisions:**
- Two-layer architecture: trigger table + knowledge graph
- Spoiler gating via `first_available` on all nodes/edges, required from the start
- Six extraction passes in sequence
- Confidence tier system (5 levels)
- `PERCEIVED_AS` edge type for cross-POV perception
- Descriptive chapter titles preserved with `real_identity` mapping

**Ideas that surfaced:**
- Theories as both output AND input to extraction pipeline
- Fan fiction generation as downstream use case
- Architecture generalizes beyond ASOIAF
