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
- [x] Pass 1 agent prompt v1 (draft complete — `agents/pass-1-mechanical.md`)
- [x] Pass 1 v1 run on AGOT (73/73 chapters, archived to `extractions/archives/agot-v1/`)
- [x] Pass 1 agent prompt v2 — added: Physical Environment, Character Appearances, Food & Drink, Hospitality & Guest Right, Location Descriptions, Spatial Layout & Movement, time_markers, direwolves/dragons-as-characters rule
- [ ] Pass 1 v2 run on AGOT (in progress)
- [ ] Pass 1 run on remaining books (ACOK, ASOS, AFFC, ADWD)
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

### Session 7 — Mechanical Extraction Schema v2 + Tooling (2026-04-22)
**What happened:**
- Reviewed all 73 AGOT v1 extractions for quality and coverage gaps
- Identified physical vector gaps: character appearances, food/drink, hospitality, location descriptions, spatial layout, weather/environment, time markers
- Updated mechanical-extractor agent prompt (`.claude/agents/mechanical-extractor.md`) with 6 new schema sections:
  - **Physical Environment** — weather, season, time of day, lighting, sounds, smells
  - **Character Appearances** — hair, eyes, build, scars, clothing, weapons, age (per-chapter, not assumed)
  - **Food & Drink** — dishes, ingredients, who eats with whom, preparation details
  - **Hospitality & Guest Right** — bread and salt, guest right, violations, shelter offered/denied
  - **Location Descriptions** — defensive features, architecture, interiors, scale, condition, terrain
  - **Spatial Layout & Movement** — phase-based scene graph with controlled vocabulary (Advance, Ambush, Assembly, etc.)
- Added `time_markers` field to Chapter Metadata
- Added direwolves and dragons as characters rule (Ghost, Grey Wind, Lady, Nymeria, Summer, Shaggydog, Drogon, Rhaegal, Viserion)
- Changed extraction philosophy from "leave empty if N/A" to "be expansive, never invent" — variance between runs is a feature
- Archived AGOT v1 extractions to `extractions/archives/agot-v1/` for comparison
- Updated `scripts/run-extraction-wave.sh` to take book as first argument, auto-discover chapters from directory
- Created `scripts/launch-extraction.sh` — opens N iTerm2 tabs and distributes waves automatically
- Created `weirwood-mechanical` shell function in `terminal-collection/functions/` for easy launching
- Created extraction runbook at `working/runbooks/extraction-pass1.md`
- Added orchestration rules to CLAUDE.md: agent prompt ↔ architecture.md sync rule, worklog archival rule
- Archived Sessions 0–4 to `working/worklog-archives/archive001.md` to reduce context load
- Updated `working/todos.md` with timeline reconstruction and direwolves/dragons items

**Key decisions made:**
- Food and Hospitality are separate concerns: food is GRRM's detailed descriptions (queryable data), hospitality is the moral/narrative framework (guest right, violations)
- Physical character descriptions need to be granular enough for cross-identity matching (Jaqen/Alchemist use case)
- Spatial Layout phases are directed-graph edges (Advance, Ambush, etc.) — mini scene graphs per chapter
- Extraction runs use Opus for quality; 4 iTerm2 terminals with 5-chapter waves
- v1 extractions preserved in archives for schema progression comparison

**What's next:**
- AGOT v2 extraction run in progress (launched via `weirwood-mechanical agot 4`)
- Compare v1 vs v2 output quality on key chapters
- Update `reference/architecture.md` to reflect new extraction schema sections (sync rule)
- Begin ACOK extraction once AGOT v2 is validated

---

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

> Sessions 0–4 archived to `working/worklog-archives/archive001.md`

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
