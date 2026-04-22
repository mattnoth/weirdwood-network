# The Weirwood Network — Project Worklog

> **Purpose:** This is the living history of the project. Every Claude Code session should read this file to understand what has been done, what decisions have been made, what's in progress, and what's queued. Update this file at the end of every work session.
>
> **Convention:** Newest entries at the top. Each entry is dated and tagged with what was done.

---

## How To Use This File

### For Claude Code Agents
Load this file alongside `reference/architecture.md` at the start of every session. Before doing any work:
1. Read the **Current State** section to understand what exists
2. Read the **Active Decisions** section for unresolved design questions
3. Read the **Ideas & Backlog** section for queued work
4. Check the **Session Log** for what happened recently

After completing work, update:
- **Current State** to reflect what now exists
- **Session Log** with a new entry describing what was done
- **Active Decisions** if new questions arose
- **Ideas & Backlog** if new ideas or tasks surfaced

### For Matt
This is your project memory. When you come back after a break, read Current State and the last few Session Log entries to get back up to speed. Add ideas to the backlog whenever they occur to you, even outside of Claude Code sessions.

---

## Current State

### Infrastructure
- [x] Repository initialized
- [x] project-context.md in place (master architecture spec)
- [x] CLAUDE.md in place (orchestration guide)
- [x] .gitignore protecting copyrighted content (sources/raw/, sources/chapters/, full-txt-files/, epubs/)
- [x] Directory structure created (sources/, extractions/, graph/, index/, curation/, reference/, scripts/)
- [x] Source .txt files moved to sources/raw/
- [x] Subagent definitions in .claude/agents/ (2 full: mechanical-extractor, script-builder; 5 stubs: wiki-ingester, voice-analyzer, foreshadowing-scanner, theory-extractor, discovery-agent)
- [x] Custom slash commands (.claude/commands/endsession.md)
- [x] Working directory with progress.md + todos.md
- [x] Reference files organized (reference/architecture.md, foreshadowing-events.md, pov-characters.md)
- [x] Chapter splitter script written (`scripts/chapter-splitter.py`)
- [x] Chapter splitter tested on one book (AGOT: 73/73)
- [x] All five books split into chapter files (344 total: AGOT 73, ACOK 70, ASOS 82, AFFC 46, ADWD 73)
- [x] Wiki scraper script written (`scripts/wiki-scraper.py`) — migrated from urllib to Playwright for Cloudflare bypass
- [x] Wiki scraper extended with `--mode all` + `--limit N` for full unattended crawl
- [x] Wiki directory structure created (`sources/wiki/`) — now fully gitignored
- [x] Full-crawl runbook drafted and updated for Playwright (`working/runbooks/wiki-full-crawl.md`)
- [x] Full wiki crawl executed (17,945/17,952 pages succeeded, 377 MB on disk)
- [x] Taxonomy candidates template created (`working/taxonomy-candidates.md`)
- [x] POV reference table corrected (6 missing chapter headings added)
- [x] D&E novellas split into chapter files (3 total: THK 1, TSS 1, TMK 1 — each novella is one continuous chapter)
- [x] TWOIAF OCR'd and extracted to plaintext (179K words, 164MB OCR'd PDF)
- [x] ocrmypdf + poppler installed (Tesseract, Ghostscript, pdftotext)

### Extraction Pipeline
- [ ] Pass 1 agent prompt finalized (draft complete — `agents/pass-1-mechanical.md`)
- [ ] Pass 1 run on AGOT
- [ ] Pass 1 run on all books
- [ ] Pass 2 wiki ingestion agent prompt written
- [ ] Pass 2 wiki ingestion complete
- [ ] Pass 3 voice/perception agent prompt written
- [ ] Pass 4 foreshadowing agent prompt written
- [ ] Pass 5 theory-informed agent prompt written
- [ ] Pass 6 discovery agent prompt written

### Index & Graph
- [ ] Trigger table v1
- [ ] Entity index
- [ ] Chapter index
- [ ] Graph edges formalized
- [ ] Convergence maps

### Reference Materials
- [x] Foreshadowing events list (`reference/foreshadowing-events.md`)
- [ ] Theory seeds file
- [ ] Taxonomy reference doc
- [x] Architecture spec (original outline exists, needs refinement)

---

## Active Decisions

> Design questions that need resolution. Tag with status: OPEN, DECIDED, DEFERRED.

### OPEN: Storage Format — Pure Markdown vs. Graph DB
- **Question:** Does the graph live as pure markdown files with edges represented as YAML/frontmatter references, or do we use a lightweight graph DB (Neo4j, SQLite with graph extensions)?
- **Leaning:** Start with pure markdown. The context base pattern works well for agentic access. Graph DB can come later if query complexity demands it.
- **Trade-off:** Markdown is portable, version-controlled, and readable by Claude Code natively. Graph DB gives real traversal queries but adds infrastructure.

### DECIDED: Wiki Ingestion Scope — Full Crawl, Then Triage
- **Decision (2026-04-13):** Scrape the entire AWOIAF wiki once (~17,952 pages, ~5–6 hrs, ~1–2 GB), store as a *reference layer* in `sources/wiki/` (gitignored). Pass 2 (wiki-ingester) decides what gets promoted into `graph/nodes/` with proper `first_available` spoiler tags.
- **Rationale:** Targeted scraping required us to predict relevance up front. Full crawl is a one-time cost (~5 hrs, ~1.5 GB) and lets us refine classification rules against a static cache for free. Cache + resume means the crawl is interruption-tolerant. The graph is still curated — only the *source layer* is exhaustive.
- **Open downstream question:** How does Pass 2 decide what to promote? Likely a combination of (a) categories the page belongs to, (b) whether the page subject appears in any chapter extraction, (c) page length / infobox richness as a quality signal. To be designed when Pass 2 prompt is written.

### OPEN: Descriptive Chapter Title Mapping
- **Question:** AFFC and ADWD use descriptive chapter titles (THE PROPHET, REEK, THE UGLY LITTLE GIRL) that map to known characters. Should the extraction system normalize these to the character's real name or preserve the title?
- **Leaning:** Preserve the title in the filename and frontmatter, but add a `real_identity` field in frontmatter. "THE UGLY LITTLE GIRL" → `real_identity: Arya Stark`. This preserves GRRM's thematic intention (Theon losing his identity as "Reek") while keeping the graph navigable.
- **Note:** This matters for the voice analysis pass — "Reek" chapters have a fundamentally different internal voice than "Theon" chapters even though it's the same character.

### DECIDED: Chapter Splitter — Source Format
- **Decision:** Source files are plain .txt (converted from EPUB). Splitter targets .txt input.
- **Location:** `sources/raw/` contains GoT.txt, ACOK.txt, ASOS.txt, AFFC.txt, ADWD.txt

### DECIDED: Spoiler Gating Architecture
- **Decision:** `first_available` field is required on every node and edge from the start. Not retrofittable.
- **Rationale:** Discussed at length. Omitting now would require manually tagging hundreds of nodes later.

### DECIDED: Extraction Pass Order
- **Decision:** Six passes in sequence: Mechanical → Wiki → Voice/Perception → Foreshadowing → Theory-Informed → Discovery
- **Rationale:** Each pass builds on the structured outputs of prior passes. Cross-chapter analysis (Passes 3+) requires the chapter-level extractions from Pass 1 as input.

---

## Ideas & Backlog

> Capture every idea here, even half-formed ones. Tag with priority: HIGH, MEDIUM, LOW, SOMEDAY.

### HIGH
- [ ] Write the chapter splitter script (agent prompt ready)
- [ ] Run Pass 1 on AGOT as proof of concept
- [ ] Write Pass 2 wiki ingestion agent prompt
- [ ] Create theory seeds file (top 20-30 theories with confidence tiers)

### MEDIUM
- [ ] Design the trigger table schema (what columns, what routing logic)
- [ ] Write Pass 3 voice analysis prompt — include the cross-POV perception dimension (how Character X is perceived by Character Y's POV vs. their own self-perception)
- [ ] Write Pass 4 foreshadowing prompt — agent receives the foreshadowing events list and scans chapter extractions for matches
- [ ] Design the node file schema (what does a single entity file look like in `graph/nodes/`)
- [ ] Build convergence map for Oldtown as proof of concept

### LOW
- [ ] Explore fan fiction generation as a downstream use case — voice profiles + relationship graph + location descriptions = grounded creative generation
- [ ] Portfolio README and demo design
- [ ] Consider MCP server for programmatic graph access
- [ ] Explore cybersecurity knowledge graph as a parallel project using the same architecture

### SOMEDAY
- [ ] Graph DB migration if markdown doesn't scale
- [ ] UI for graph exploration (React app?)
- [ ] Automated theory confidence scoring based on evidence density
- [ ] Ingest theory content from YouTube transcripts (Alt Shift X, Glidus, etc.)
- [ ] Community contribution pipeline — let other ASOIAF nerds submit nodes/edges through PRs

---

## Session Log

> Newest first. One entry per work session.

### Session 6 — Book Integration: Dunk & Egg + TWOIAF (2026-04-16)
**What happened:**
- Followed runbook at `working/runbooks/book-integration.md` to integrate two new source artifacts.
- **Dunk & Egg (D&E):**
  - Converted `The Tales of Dunk & Egg.epub` to plaintext via Calibre `ebook-convert` → `sources/raw/TDAE.txt`
  - Structure deviated from runbook expectations: Calibre output used mixed-case titles (not ALL CAPS) and had **no internal chapter/section divisions** (no Roman numerals). Each novella is one continuous block of prose.
  - Wrote `scripts/dunk-egg-splitter.py` via script-builder subagent. Imports `normalize()` from `chapter-splitter.py` via importlib (hyphenated filename workaround).
  - Produced 3 files total (one per novella):
    - `thk-dunk-01.md` — The Hedge Knight (~31,600 words)
    - `tss-dunk-01.md` — The Sworn Sword (~36,600 words)
    - `tmk-dunk-01.md` — The Mystery Knight (~36,800 words)
  - All files have valid YAML frontmatter with `collection: tales-of-dunk-and-egg`, `first_available: pre-agot`, `real_identity: Duncan the Tall`
- **TWOIAF (The World of Ice and Fire):**
  - Installed `ocrmypdf` + `poppler` via Homebrew (Tesseract, Ghostscript, pdftotext, dependencies)
  - OCR'd 344-page scanned PDF: `ocrmypdf --output-type pdf --optimize 1 --jobs 8` → `sources/raw/TWOIAF.ocr.pdf` (164MB, 5.7% smaller than input)
  - Tesseract warnings on ~15 pages ("lots of diacritics" — decorative pages, maps) but no fatal errors
  - Extracted text: `pdftotext -layout` → `sources/raw/TWOIAF.txt` (179,397 words)
  - Quality spot-check: "valyrian" 129 hits, "targaryen" 309 hits, "long night" 14 hits — all pass
  - OCR quality: title/TOC pages have garbled decorative text (expected for scanned ornamental fonts), but prose content is clean and readable
- Updated `.gitignore` with `sources/reference/` exclusion
- Updated `reference/architecture.md` with D&E book codes, `collection:` field, `first_available: pre-agot` convention, and `sources/reference/` layer
- Updated `reference/pov-characters.md` with Duncan the Tall entry and per-novella chapter counts

**Anomalies / follow-ups:**
- D&E novellas have no internal chapter divisions — if future analysis needs finer granularity, a subdivider script could split on scene breaks (blank-line gaps in prose), but not needed now
- TWOIAF OCR: decorative cover pages and TOC dotted-leader lines are garbled, but this is cosmetic — the prose content that matters for the reference layer is clean
- TWOIAF structural splitter was explicitly deferred per plan — needs a planning session once we decide how to segment the reference material (by region? by era? by topic heading?)
- The `pre-agot` value for `first_available` is a new convention not previously in the architecture — flagged in architecture.md, can be renamed later if a more specific scheme is needed

**What's next:**
- Pass 1 mechanical extraction on AGOT remains the primary unblocked work
- TWOIAF structural splitter is deferred until OCR quality reviewed and segmentation strategy decided
- D&E chapters are available for Pass 1 extraction whenever the main-series pipeline is proven

---

### Session 5 — Full Wiki Crawl Executed (2026-04-14)
**What happened:**
- Ran `python3 scripts/wiki-scraper.py --mode all -v` per runbook (`working/runbooks/wiki-full-crawl.md`). Crawl completed fully unattended — no Cloudflare challenges triggered. All 17,952 pages processed: 17,945 succeeded, 7 failed (all HTTP 403 — 6 "Mander"-related pages + "The Mance", likely redirect/special-character edge cases). Final disk footprint: 377 MB total (293 MB raw cache, 81 MB uncategorized markdown, 3.8 MB houses). Only 640 pages classified as `houses/`; 17,305 landed in `_uncategorized/` due to conservative classifier rules. No anomalies beyond the classification skew. Crawl took approximately 36 hours wall clock (slower than the 6–8 hour estimate due to sustained ~280 pages/hour rate on larger character/location pages).

**What's next:**
- Refine `classify_entity()` rules against the static cache to reduce `_uncategorized/` count before designing Pass 2
- Design Pass 2 (wiki-ingester) prompt — what gets promoted from `sources/wiki/` into `graph/nodes/` and how `first_available` gets assigned
- Begin Pass 1 mechanical extraction testing on AGOT chapters (unblocked)

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

**What's next:**
- Matt launches the full crawl from a new session: `claude --dangerously-skip-permissions "Follow the runbook at working/runbooks/wiki-full-crawl.md"`
- First page load may require one manual "Verify I am human" click, then the crawl is fully automated
- Estimated 6–8 hours for 17,952 pages

---

### Session 3 — Wiki Crawl Planning + Smoke Test (2026-04-13)
**What happened:**
- Reviewed `scripts/wiki-scraper.py` and confirmed it already extracts full page text (not just summaries) — the `## Full Text` section in each output file gets the cleaned article body.
- Discussed scope: shifted from targeted scraping to **full crawl, then triage**. Rationale: scraping is cheap, classification can be refined against a static cache, and `sources/wiki/` is a reference layer not the graph itself.
- Updated `.gitignore` to exclude all of `sources/wiki/` (was previously only excluding `_raw/`). Wiki content is regenerable from cache; graph nodes (which are committed) are the canonical artifact.
- Delegated to `script-builder` to add `--mode all` and `--limit N` to the scraper:
  - New `fetch_all_page_titles()` uses MediaWiki `list=allpages&apnamespace=0`, paginates, caches title list to `_raw/.all-pages.json`
  - New dispatch branch iterates `scrape_entity` over every title, streams progress to `_raw/.crawl-progress.log`
  - Aborts cleanly after 3 consecutive failures (Cloudflare cookie expired) with cookie-refresh instructions
- Matt provided a fresh `cf_clearance` cookie; saved to `sources/wiki/_raw/.cookies`.
- Ran 5-page smoke test (`--mode all --limit 5 -v`):
  - **All 5 pages succeeded.** No Cloudflare issues.
  - **Title list fetched: 17,952 total pages** (significantly more than my initial 10–15k estimate).
  - **Per-page footprint (smoke sample, biased small):** raw cache 4–24 KB, processed markdown 0.3–2.7 KB. Real character/location pages will be much larger (50–300 KB raw).
  - **Realistic full-crawl projection:** 1.0–1.8 GB on disk, ~5–6 hours wall clock.
  - **Classifier observation:** all 5 smoke pages landed in `_uncategorized/` because they're alphabetical edge cases (numeric dates, stubs). Expect a lot of `_uncategorized/` content in the full crawl — fine, classification is re-runnable against the cache.
  - **Discovery:** the AWOIAF page "10,000 Ships" is about a planned HBO spinoff TV show, not the in-universe fleet. Wiki has out-of-universe meta content (TV, actors, production) mixed with canon. Pass 2 will need to filter these.
- Wrote runbook at `working/runbooks/wiki-full-crawl.md` so the full crawl can be launched from a fresh `claude --dangerously-skip-permissions` session by pointing the agent at the file. Includes pre-flight checks, expected failure modes, cookie-refresh procedure, and required final report format.

**Key decisions made:**
- Wiki ingestion scope: **full crawl, not targeted** (now logged as DECIDED above)
- `sources/wiki/` is fully gitignored — reference layer, not graph artifact
- Long-running unattended tasks get runbooks in `working/runbooks/` rather than ad-hoc prompts; the runbook directory is now the home for any future agent-driven batch operations
- The Cloudflare cookie problem has no "fix" beyond manual refresh — accepted as operational reality, mitigated by per-page caching that makes resume free

**What's next:**
- Matt launches the full crawl from a Claude CLI session: `claude --dangerously-skip-permissions "Follow the runbook at working/runbooks/wiki-full-crawl.md"`
- Cookie may need refresh once or twice mid-run depending on Cloudflare's TTL
- After crawl completes: review `_uncategorized/` count, decide whether to refine `classify_entity()` rules before designing Pass 2
- Pass 2 (wiki-ingester) prompt design is the next non-trivial planning task — needs to answer "what gets promoted from `sources/wiki/` into `graph/nodes/` and how does `first_available` get assigned"

---

### Session 2 — Foundation Builder: Chapter Splitter + Wiki Scraper (2026-04-13)
**What happened:**
- Wrote `scripts/chapter-splitter.py` — splits source .txt files into per-chapter markdown with YAML frontmatter
  - Handles ALL CAPS headings, descriptive titles (AFFC/ADWD), prologues/epilogues
  - Normalizes smart quotes (U+2019) to straight apostrophes for heading matching
  - Detects TOC vs. actual chapters via narrative-text heuristic (prose lines >30 chars with lowercase letters)
  - Stops at APPENDIX/ACKNOWLEDGMENTS/MEANWHILE end markers
- Ran splitter on all 5 books — all counts match expected: AGOT 73, ACOK 70, ASOS 82, AFFC 46, ADWD 73 (344 total)
- Fixed `is_narrative()` bug: all-caps lines like "APPENDIX: THE KINGS AND THEIR COURTS" in ASOS/AFFC TOC were incorrectly classified as narrative text. Added lowercase-letter requirement.
- Discovered 6 missing chapter headings in `reference/pov-characters.md`: THE REAVER (AFFC), THE BLIND GIRL, A GHOST IN WINTERFELL, THE IRON SUITOR, THE KINGBREAKER, THE QUEEN'S HAND (all ADWD). Added all to reference file and splitter.
- Wrote `scripts/wiki-scraper.py` (1213 lines, stdlib-only) — scrapes AWOIAF MediaWiki API
  - Modes: single entity, category, targeted batches (characters/locations/houses/events/artifacts), category discovery
  - Caches all API responses in `sources/wiki/_raw/` (gitignored)
  - Rate-limited (1 req/sec), graceful error handling
  - Handles Cloudflare challenge detection with clear user instructions for cookie setup
- Created wiki directory structure (`sources/wiki/{characters,locations,houses,events,artifacts,_uncategorized,_raw,_category-reports}`)
- Created `working/taxonomy-candidates.md` template for wiki-derived taxonomy expansion
- Added `sources/wiki/_raw/` to `.gitignore`

**Blockers:**
- Wiki scraper is blocked on Cloudflare. AWOIAF uses managed challenges that require browser cookies (`cf_clearance`). Script detects this and provides setup instructions. Matt needs to:
  1. Visit https://awoiaf.westeros.org in browser
  2. Copy `cf_clearance` cookie value
  3. Save to `sources/wiki/_raw/.cookies`

**Key decisions made:**
- Chapter splitter uses prose-detection heuristic (not gap-based) to distinguish TOC from chapters — more robust across different file structures
- Wiki scraper is stdlib-only (no pip dependencies) — uses urllib, json, html.parser, re
- Cloudflare cookie approach: manual browser session → cookie export → file-based auto-loading

**What's next:**
- Matt provides Cloudflare cookies so wiki scraper can run
- Run `--mode targeted --batch characters` first, then locations, houses, events, artifacts
- Run `--mode categories` for taxonomy discovery
- Begin Pass 1 mechanical extraction testing on AGOT chapters (unblocked, doesn't depend on wiki)

---

### Session 1 — Project Scaffolding & Cleanup (2026-04-13)
**What happened:**
- Created full directory skeleton from architecture spec (sources/, extractions/, graph/, index/, curation/, reference/, scripts/, .claude/agents/)
- Created .gitignore FIRST — protects sources/raw/, sources/chapters/, full-txt-files/, epubs/ from ever being committed
- Moved 5 .txt book files from full-txt-files/ to sources/raw/
- Installed CLAUDE.md at project root (adapted from scaffold, references correct filenames)
- Set up .claude/agents/ with 7 subagent definitions:
  - **Full agents:** mechanical-extractor (Pass 1), script-builder (tooling)
  - **Stub agents:** wiki-ingester (Pass 2), voice-analyzer (Pass 3), foreshadowing-scanner (Pass 4), theory-extractor (Pass 5), discovery-agent (Pass 6)
- Removed claude-chat-scaffold/ directory (contents integrated)
- Resolved open decision: source format is .txt (not PDF/EPUB)
- Cleaned up root: moved specs to `reference/`, deleted files whose content was fully captured in agents
  - `project-context.md` → `reference/architecture.md`
  - `foreshadowing-events.md` → `reference/foreshadowing-events.md`
  - POV lookup table extracted to `reference/pov-characters.md`
  - `pass-1-mechanical.md` deleted (schema in agent def, worked example + verbose rules noted as TODOs)
  - `agent-chapter-splitter.md` deleted (requirements in script-builder agent)
- Created `working/` directory with `progress.md` (agent handoffs) and `todos.md` (actionable items by topic)
- Created `/endsession` custom slash command (`.claude/commands/endsession.md`)

**Key decisions made:**
- Local directory stays as `asoiaf-chat`; GitHub repo will be `the-weirwood-network` (set via git remote)
- Copyrighted content (full books AND split chapters) must NEVER enter git history
- Later-pass agents (3-6) organized as stubs with purpose/inputs/outputs/TODOs — full prompts deferred
- `working/` directory serves as scratchpad for in-progress work, agent handoffs, and anything uncertain
- Root kept minimal: just CLAUDE.md + worklog.md

**What's next:**
- Write the chapter splitter Python script (scripts/chapter-splitter.py)
- Test on AGOT first
- Test mechanical extraction variations on a few chapters before committing to schema
- Run Pass 1 mechanical extraction on a handful of AGOT chapters as proof of concept

---

### Session 0 — Project Genesis (Date: ______)
**What happened:**
- Designed the overall system architecture in conversation with Claude
- Produced the initial architecture spec document (to be placed at `reference/architecture-spec.md`)
- Designed the six-pass extraction pipeline
- Created three foundational documents:
  - `CONTEXT.md` — master project context for all agents
  - `agents/pass-1-mechanical.md` — Pass 1 mechanical extraction agent prompt
  - `reference/foreshadowing-events.md` — 30 major events + 15 unfired Chekhov's guns
  - `agents/agent-chapter-splitter.md` — Agent prompt for writing the chapter splitter script
  - `WORKLOG.md` — this file

**Key design decisions made:**
- Two-layer architecture: trigger table (index) + knowledge graph working together
- Spoiler gating via `first_available` field on all nodes/edges, required from the start
- Six extraction passes in sequence, each building on prior outputs
- Confidence tier system (5 levels) for all claims
- `PERCEIVED_AS` edge type for cross-POV character perception
- Descriptive chapter titles preserved in filenames with `real_identity` mapping in frontmatter
- Project worklog as living context base for continuity across sessions

**Ideas that surfaced:**
- Theories serve as both output AND input to the extraction pipeline — they tell analytical agents what patterns to watch for
- The bottom-up extraction pass might surface patterns that don't match any existing theory → new candidate theories
- Fan fiction generation as a downstream use case (voice profiles + relationship graph)
- The architecture generalizes beyond ASOIAF — same pattern could work for codebases, other fiction, cybersecurity domains

**What's next:**
- Matt to confirm ebook file format (PDF vs. EPUB)
- Initialize the repository with the directory structure from CONTEXT.md
- Run the chapter splitter agent to produce the script
- Test the script on AGOT
- Run Pass 1 on a handful of AGOT chapters to validate the extraction schema

---

## Principles

> Guiding principles for the project. Reference these when making design decisions.

1. **The chapter text is immutable.** Source files in `sources/chapters/` never change. Everything else layers on top.
2. **Facts before interpretations.** Mechanical extraction before analytical. Tier 1 before Tier 4.
3. **Agents propose, humans decide.** Analytical findings go to the curation queue. Matt assigns confidence.
4. **Spoiler gating is architectural.** Every node has `first_available`. This is not a feature to add later.
5. **The index and the graph are complementary.** The index routes. The graph traverses. Both are needed.
6. **Each token should be productive.** Structure exists to reduce waste — agents should read relevant, trustworthy content, not re-derive known relationships.
7. **Start with the foundation, not the flashiest feature.** Chapter files → mechanical extraction → wiki → index → graph → analytical passes. In that order.
