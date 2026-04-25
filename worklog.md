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
- [x] Custom slash commands (.claude/commands/endsession.md, continue.md)
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
- [x] Pass 1 v2 run on AGOT (73/73, archived to `extractions/archives/agot-v2/` — 4-category Raw Entity List)
- [x] Pass 1 v2 run on ACOK (50/70, archived to `extractions/archives/acok-v2/` — 4-category Raw Entity List)
- [x] Pass 1 v3 prompt update: expanded Raw Entity List to 12 categories (10 + Other catch-all), added strict formatting rules (all headers required, no merging/renaming, "None" for empty categories)
- [x] Pass 1 v3 run on AGOT (73/73 — complete)
- [ ] Pass 1 v3 run on ACOK (0/70)
- [ ] Pass 1 v3 run on remaining books (ASOS 0/82, AFFC 0/46, ADWD 0/73)
- [ ] Wiki infobox parser script: extract `first_available` (cite_ref chapter tags + Books infobox) and relationship fields from cached wiki HTML
- [ ] AGOT/ACOK supplementary entity index: script to scan existing extractions and categorize candidate entity types from narrative sections
- [ ] Pass 1 run on remaining books (ASOS, AFFC, ADWD) — blocked on prompt update + wiki parser groundwork
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

### Session 12 — AGOT v3 Complete, Rate-Limit Detection, Commit Catchup (2026-04-25)
**Detail:** `working/session-details/session-012.md`
**Changes made:**
- `scripts/extract.sh` — rate-limit detection: checks JSON for `status:rejected`, halts wave immediately, marks remaining chapters as `skip-rate-limit`; replaced `tail -3` preview with structured extraction summary; added emoji indicators (✅ ❌ 🚫 ⏭️ 🔄 ⚠️); removed raw JSON dump on failures
- `extractions/mechanical/agot/` — all 73 chapters now v3 complete (26 chapters extracted this session, finishing waves 8, 10, 12-15)
- 3 commits landed: infrastructure (sessions 8-11), extraction tooling, AGOT v3 extractions + archives
- Memory updated: extraction rule strengthened to absolute prohibition on agent-triggered extractions

**Decisions:** Rate-limit detection halts the wave (not the terminal) — stop-file handles cross-wave halting. Emoji in terminal output only, never in extraction content. Structured summary (line count, table rows, events, relationships) replaces raw preview. All historical stat CSVs (v1, v2, v3) kept. One minor schema gap: eddard-01 missing `### Other` header — cosmetic, not blocking.

**What's next:**
- ACOK v3 extraction: `weirwood acok` to see starting point, then `weirwood acok <tabs> <waves>` to run (0/70, user triggers)
- Track B (wiki infobox parser) remains independent: `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`
- Schema review of AGOT v3 output quality (next session)

### Session 11 — Extract.sh Instrumentation: Worklog Auto-Update & Versioned CSV (2026-04-24)
**Detail:** `working/session-details/session-011.md`
**Changes made:**
- `scripts/extract.sh` — stats CSV now per-book versioned (`working/extraction-stats/extraction-stats-{book}-pass1-v3.csv`); new `update_worklog()` function auto-updates `worklog.md` checklist after each wave
- `scripts/extraction-status.sh` — updated to use per-book CSV path
- `working/extraction-stats.csv` — split: v2 rows (Apr 23) back to v2 CSV, v3 rows (Apr 24) to new v3 CSV
- `worklog.md` — updated AGOT v3 progress to 30/73 (was stale at 0/73)

**Decisions:** PASS/VERSION hardcoded at script top (not CLI flags) — prompt version changes are rare and deliberate. Worklog update uses filesystem truth via `is_complete`, not CSV row counts. Stats CSVs versioned per book/pass/version so they archive with their extraction run.

**What's next:**
- Continue AGOT v3 extraction (30/73 done, waves 7-15 remaining)
- Track B (wiki infobox parser) remains independent: `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`

### Session 10 — Prompt Update v3, Archive Prior Extractions, Process Lessons (2026-04-24)
**Detail:** `working/session-details/session-010.md`
**Changes made:**
- `.claude/agents/mechanical-extractor.md` — Raw Entity List expanded to 12 categories (10 named + Other catch-all), added strict formatting rules (all headers required, no merging/renaming, "None" for empty)
- `reference/architecture.md` — Pass 1 schema table updated to reflect 12 categories
- `extractions/archives/agot-v2/` — archived 73 AGOT v2 extractions (4-category format)
- `extractions/archives/acok-v2/` — archived 50 ACOK v2 extractions (4-category format)
- `extractions/mechanical/agot/` and `acok/` — now empty, ready for v3 runs
- `cspell.json` — created project-level cSpell dictionary for ASOIAF terms
- 3 new memory entries (no-extraction-without-asking, check-existing-knowledge-first, knowledge-index-deferred)

**Decisions:** Extractions must go through `weirwood` pipeline only, never background subagents. Raw Entity List locked at 12 categories with strict no-rename/no-merge formatting rules. All prior extractions archived; v3 starts fresh. Trust wiki organization as authority for entity type categories. `Other` catch-all handles edge cases without agent improvisation. Behavioral rules for checking existing knowledge saved; structural index deferred.

**What's next:**
- Run AGOT extraction via `weirwood agot` with v3 prompt (Matt will trigger manually)
- After AGOT v3 validates, run ACOK and remaining books
- Track B (wiki infobox parser) remains independent: `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`

### Session 9 — /continue Command, Todo-Prompt Linking, Session Backfill (2026-04-24)
**Detail:** `working/session-details/session-009.md`
**Changes made:**
- Created `.claude/commands/continue.md` — priority-aware `/continue` slash command
- Updated `working/todos.md` — added `→ continue:` references linking two todo items to their continue prompts
- Updated `.claude/commands/endsession.md` — added depth-scaling guidance for session details, continue prompt lifecycle (create + cleanup), removed handoffs.md references
- Updated `CLAUDE.md` — removed handoffs.md, pass1-agot.md, taxonomy-candidates.md from directory tree
- Created `working/session-details/session-000.md` through `session-007.md` — backfilled all pre-documentation sessions
- Deleted 7 stale files: `progress/handoffs.md`, `progress/pass1-agot.md`, `progress/README.md`, `working/progress.md`, `working/taxonomy-candidates.md`, `working/extraction-stats-agot-pass1-v1.csv`, `scratch`
- Deleted completed continue prompt: `2026-04-24-backfill-session-details.md`

**Decisions:** Todos.md is the priority authority; continue prompts link from todos via `→ continue:` lines (one-directional). handoffs.md retired — redundant with todos + continue prompts. Session detail depth should scale to session type (design = full narrative, execution = decisions + surprises). Endsession owns the continue prompt lifecycle (create new, delete completed).

**What's next:**
- Track A: Update extractor Raw Entity List 4→10 categories, finish ACOK + start ASOS (`progress/continue-prompts/2026-04-24-track-a-extraction-prompt-update.md`)
- Track B: Write wiki infobox parser script, design Pass 2 (`progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`)

### Session 8 — Architecture Refactor, Edge/Entity Taxonomy, Wiki Discovery (2026-04-24)

**Detail:** `working/session-details/session-008.md`

**Changes made:**
- `reference/architecture.md` → pure agent schema reference (removed directory tree, current state, project overview)
- Entity types: flat list → hierarchical taxonomy with inheritance (18 leaf types across 8 parent categories)
- Edge types: 26 → ~80 across 14 categories (normalized from v1's 127 ad-hoc types + wiki infobox fields)
- Edge taxonomy is for graph layer only — Pass 1 stays free-text
- Wiki `cite_ref` anchors discovered: `R{book}{chapter}` encoding gives chapter-level `first_available`
- Wiki infobox → edge type mapping table added to architecture.md
- CLAUDE.md: pipeline status updated, directory tree refreshed
- Coverage analysis: Raw Entity List has 4 categories, needs 10. Magic/Species/War severely under-indexed.
- ACOK confirmed at 50/70 (same prompt gap as AGOT)

**Decisions:** architecture.md is agent-only; `house` is its own type under Organization; AGOT/ACOK don't need re-runs (supplementary index instead); prompt update before any further extraction; wiki confidence-tier mapping is a Pass 2 problem; two independent work tracks (A: extraction, B: wiki/Pass 2).

**What's next:**
- **Track A** (continue prompt: `progress/continue-prompts/2026-04-24-track-a-extraction-prompt-update.md`): Update extractor Raw Entity List 4→10 categories, then finish ACOK + start ASOS
- **Track B** (continue prompt: `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`): Write wiki infobox parser script, then design Pass 2
- Tracks converge at graph building

> Sessions 5–7 archived to `working/worklog-archives/archive002.md`
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
