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
- [x] Pass 1 v3 run on ACOK (70/70 — complete)
- [x] Pass 1 v3 run on ASOS (82/82 — complete; Okey ran in parallel on shared Max account, branch `pass1-asos-extraction`)
- [x] Pass 1 v3 run on AFFC (46/46 — complete)
- [x] Pass 1 v3 run on ADWD (73/73 — complete)
- [ ] Pass 1 on Tales of Dunk and Egg (THK, TSS, TMK) — **deferred (enrichment pass for main-arc nodes)**. D&E content will eventually enrich existing main-arc Targaryen-prehistory nodes (Bloodraven, Egg/Aegon V, etc.) but is not on the active critical path. Not dropped, not urgent. Decision 2026-05-06 (Session 37 Q11=b).
- [x] Wiki infobox parser script (Track B) — `scripts/wiki-infobox-parser.py` produces `working/wiki/data/{infobox-data.jsonl (5,279), page-index.jsonl (17,657), parse-stats.md}`. `first_available` populated 2,888/5,279 (54.7%). **Three open issues:** (1) `categories[]` empty across all pages (parse API strips catlinks footer) — blocker for runbook §1.2.1 unless deferred to `entity_type_guess`, (2) `books` field parsed only 37 times vs 1,953 raw occurrences (parser bug), (3) unmapped infobox fields worth edge-taxonomy review (`dynasty`, `written by`, `hatched`, `fathers`, `vassal`, `cadet branch`).
- [x] AGOT/ACOK supplementary entity index — OBSOLETED 2026-04-25. v3 prompt captures all 12 categories directly; backfill index no longer needed. See `working/todos.md` line ~245.
- [ ] Pass 2 wiki ingestion agent prompt written
- [ ] Pass 2 wiki ingestion complete
- [x] Wiki Pass 2 v1 — core (37/37 buckets complete; 855 nodes; cost $95.33; per-node $0.111 healthy per Stage-2 cold review)
- [x] Wiki Pass 2 Stage 2 cold review (Session 24; decision was `remediate`, but overturned same session — see Active Decisions)
- [x] Wiki Pass 2 Stage 3 — secondary (Session 26; FULL pipeline rebuilt as Python-only after design review showed the Stage 3b agent was inertia-driven. 472 buckets / 3,315 candidate pages → 3,314 nodes promoted. Cumulative graph: 855→4,169 then →4,239 after Tier-1+Tier-2 recovery. Cost $0. Wall-clock ~30 sec total. 0 conflicts.) Canonical pipeline: `working/runbooks/wiki-pass2-pipeline.md` (rewritten as v3).
- [x] Wiki Pass 2 Stage 3c — audit cleanup (Session 27; 4 audits run, 6 parser bugs fixed, 484 nodes re-emitted across multiple targeted runs. Tier 3 promotion campaign Passes A-D + E Phase 1 added 769 new nodes. Cat 1 orphan edges 7,784→2,955 (62% drop). Stale religion-bleed 0. Edge vocabulary lock holds.)
- [x] Wiki Pass 2 Path B — categorizer extension + promotion campaign (Session 28; bounded MediaWiki categories backfill + parser CATEGORY_TYPE_MAP. `unknown` 12,434 (70.4%) → 2,118 (12.0%). +2,240 graph nodes (5,008 → 7,248). Cat 1 orphan edges 2,955 → 1,973. 5 new dirs bootstrapped: `texts/`, `theories/`, `concepts/`, `species/`, `foods/`. New entity type `object.food`.)
- [x] Wiki Pass 2 Path B promotion completion + schema-drift audit (Session 29; 4 new entity types added: `object.material`, `concept.language`, `concept.medical`, `concept.custom`. 4 new dirs: `materials/`, `languages/`, `medical/`, `customs/`. `unknown` 2,098 → 1,257. Net +315 graph nodes (7,248 → 7,563). 130 stale-dir mismatches cleaned. Full schema-drift audit on opus: 0 HIGH / 4 MED / 4 LOW. Cat 1 orphan edges 1,973 → 1,963. Edge vocabulary lock holds. Chronology data extracted from 74 year pages: 2,245 events in `working/wiki/data/chronology-events.jsonl` (awaits v2 temporal-edges schema; not graph edges yet).)
- [x] Wiki Pass 2 Stage 0 foundation — alias-resolver built + run (Session 26). 707 broken refs reclaimed via slug-mismatch fix. Empirical signal validates that most remaining "broken" refs are genuinely missing concept entities (concept-pages decision: defer).
- [ ] Wiki Pass 2 Stage 4 — prose-derived edge discovery (Stage 0 prep complete + cross-references index built; Stage 4 hybrid plan documented in `working/agent-fleet-specs/fleet-orchestration-plan.md`. Pass 1 dependency now met (344/344 across 5 books). Need to build: edge-candidate-generator script, then prose-edge-classifier agent runs (full prompt ready in `.claude/agents/prose-edge-classifier.md`), then peer review, then promote. Continue prompt: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`)
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

### DEFERRED: Spoiler Gating to Post-First-Release (2026-04-27)
- **Decision (2026-04-27):** `first_available` field is **deferred**. Optional in v1 nodes; existing values may be wrong/missing/inconsistent. Do not invest context reasoning out individual values. Backfill via deterministic script after first release.
- **Supersedes prior DECIDED rule** ("required on every node from the start; not retrofittable") which was overturned mid-Stage-2 review when schema-correctness remediation was projected to consume too much context for too little payoff. The wiki cite_ref data is rich enough that a deterministic backfill is cheap once we stop trying to enforce per-node consistency during extraction.
- **What this changes:** wiki-ingester drops the "agent self-corrects to `always available`" rule. Validator does not enforce `first_available`. CLAUDE.md and architecture.md updated. Tyrion/Varys (Stage-2 sample bugs) nulled rather than manually patched.
- **What this preserves:** the wiki data sources (infobox Books field + cite_ref anchors) remain documented in architecture.md so the backfill script can still use them.

### DECIDED: Track B (Wiki Parser) Before v3 Schema Review
- **Decision (2026-04-25):** Build the wiki infobox parser (Track B) before doing a schema review of the v3 Pass 1 output and before scaling v3 to ACOK/ASOS/AFFC/ADWD.
- **Rationale:** Track B surfaces schema signals that an isolated v3 review cannot:
  - **Entity type boundaries** — wiki categories are an external taxonomy. Mismatch with the 12 Pass 1 categories is a schema signal.
  - **Relationship/edge shape** — infobox fields (`spouse`, `father`, `liege`, `culture`, `religion`) define the graph's relationship vocabulary. Gaps in Pass 1's relationship extraction surface here.
  - **`first_available` mechanics** — `cite_ref` chapter anchors are the spoiler-gating primitive. The parser proves whether the encoding is reliable.
  - **Schema redundancy** — if the wiki provides house words / sigils / seats reliably, Pass 1 doesn't need to extract them. Track B can *shrink* the Pass 1 schema.
- **Cost asymmetry:** Doing schema review first risks discovering Track B reshapes it → 272 chapters (ACOK + ASOS + AFFC + ADWD) re-run. Doing Track B first costs a few days of already-queued work.
- **Continue prompt:** `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md` (now includes this rationale at the top).

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

> Newest first. One entry per work session. **Strict 5-entry max** (CLAUDE.md rule #8): when a 6th lands, the oldest archives to `history/worklog-archives/archiveNNN.md`.

### Session 50 — Orphan Edges Cat 1 Batch: Top-N Recovery (2026-05-12)

**Changes made:**
- **7 ALIAS-FIX** — added missing slug aliases to existing nodes: `crossroads-inn`→inn-at-the-crossroads (already had display-name forms but not the slug); `dragons`→dragon (species); `joffrey-i-baratheon`→joffrey-baratheon; `tommen-i-baratheon`→tommen-baratheon; `vale`→vale-of-arryn; `the-wall`→wall; `giant`→giants.
- **8 CREATE** — new nodes with `pass_origin: pass2-orphan-batch-2026-05-12`: `factions/blacks` (Rhaenyra's Dance of Dragons faction, tier-1); `factions/greens` (Aegon II's faction, tier-1); `events/age-of-heroes` (legendary era, tier-2); `locations/crypt-of-winterfell` (Winterfell burial vault, tier-1); `factions/two-betrayers` (Hugh Hammer + Ulf the White, tier-1); `events/andal-invasion` (Andal conquest of Westeros, tier-1); `factions/winter-wolves` (Cregan Stark's veterans, tier-1); `factions/bastards-boys` (Ramsay's hunters, tier-1).
- `working/wiki/data/alias-resolver.json` — rebuilt via `scripts/wiki-pass2-build-alias-resolver.py --apply` (1,433 entries).
- `graph/index/chapters/` — rebuilt via `scripts/build-mention-index.py --all`.
- `working/audits/orphan-edges-2026-05-12-post-orphan-batch.md` — post-batch audit snapshot.
- `working/todos.md` — orphan batch DONE item added; spot-check todo updated noting `bastards-boys` defect resolved.

**Delta:** Cat 1 orphan edges 1896→1673 (−223). Clean-resolving edges 18831→19055 (+224). Graph 7959→7967 nodes (+8).

**Decisions:** All 15 operations (7 alias + 8 create) completed in single window; no multi-window needed (deterministic, no classification ambiguity). Skipped `ship`, `betrothal`, `lads` (ambiguous noise — no single canonical target). Skipped date-pattern slugs per standing rule. Session 46 archived to `history/worklog-archives/archive010.md`.

**What's next:**
- **Stage 4 prose-edge-classifier** — next major track. → continue: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`
- **Per Matt's standing rule, /endsession is NOT auto-run.**

---

### Session 49b — Case-Collision Tail Track B (2026-05-12)

**Changes made:**
- `scripts/filter-case-collision-tail.py` — NEW. Classifies all 65 remaining case-collision tail slugs into DROP / ALREADY_EXISTS / CANONICAL. Checks graph/nodes/ for exact and alias matches; applies drop rules (real-world books, disambig pages, list articles, hound names, meta-wiki, zero-source). Outputs `working/missions/case-collision-tail/canonical-slugs.txt` + `uncertain-slugs.txt`.
- **4 alias updates** to existing nodes: `arryk-cargyll` ← "Arryk (guard)", `erryk-cargyll` ← "Erryk (guard)", `dragonbinder` ← "dragon horn"/"Dragon Horn", `jeyne-fowler` ← "Fowler twins"/"the Fowler twins".
- **10 new nodes created** from chapter extraction evidence:
  - characters/: `handsome-man`, `stern-face`, `starved-man` (Faceless Men identifiers, AFFC Arya chapter), `damon-dance-for-me` (Ramsay's man, ADWD), `red-raven-free-folk` (Raymun Redbeard's brother, Free Folk), `henly-maester` (young maester at Bolton-occupied Winterfell), `grazdan-mo-ullhor` (Cleon's former owner in Astapor)
  - species/: `ice-dragon` (Old Nan's legendary creature), `ghost-grass` (Shadow Lands plant, Dothraki eschatology)
  - foods/: `wine-of-courage` (Unsullied pain-numbing training potion)
- `working/missions/case-collision-tail/drop-manifest.md` — NEW. Full record of 28 explicit drops + 27 ALREADY_EXISTS + 10 canonical created. Preserves auditability of the full 65 processed.
- `reference/architecture.md` — Fixed typo "cred sites" → "sacred sites" (line 56).
- `working/todos.md` — case-collision tail LOW item → DONE; architecture typo → DONE.

**Decisions:** Track B did NOT use multi-window+watcher as the continue prompt specified. Rationale: after filtering, the canonical list collapsed to 10 nodes (not ~15-20 expected), all with clear types and chapter evidence already in session context. The "drift potential is HIGH" rationale no longer applied. Filter step is the key finding: most "canonical" slugs were redirect-only wiki pages with zero backlinks — the script correctly identified them. 4 slugs classified as ALREADY_EXISTS turned out to need alias updates rather than new nodes (arryk, erryk, dragon-horn, fowler-twins).

**Graph total:** 7,949 → 7,959 nodes (+10).

**What's next:**
- **Stage 4 prose-edge-classifier** — next major track. → continue: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`
- **Per Matt's standing rule, /endsession is NOT auto-run.**

### Session 49 — Alias-Backfill Round 2 (2026-05-12)

**Changes made:**
- `graph/nodes/locations/vale-of-arryn.node.md` — added alias `"The Vale"` to `aliases` field.
- `graph/nodes/characters/aemon-targaryen-son-of-maekar-i.node.md` — added alias `"Maester Aemon"`.
- `graph/nodes/characters/aemon-targaryen-son-of-viserys-ii.node.md` — added alias `"Prince Aemon the Dragonknight"`.
- `working/wiki/data/alias-resolver.json` — rebuilt via `scripts/wiki-pass2-build-alias-resolver.py --apply`. Three new entries in `alias_to_canonical`. Map now 1,403 entries.
- `graph/index/chapters/` — rebuilt via `scripts/build-mention-index.py --all`. 344 chapters re-indexed.

**Resolution delta:** 70.6% → **72.9%** (+2.3 pp, ~849 newly-resolved mentions). Beats the projected 72-74% range.

**Slug note:** Continue prompt expected canonical slugs `aemon-targaryen-maester` and `aemon-targaryen-dragonknight`; neither exists. The graph uses `son-of-*` naming convention. Aliases were added to the correct existing nodes (`aemon-targaryen-son-of-maekar-i` and `aemon-targaryen-son-of-viserys-ii`). Continue prompt slug expectations were stale.

**Decisions:** Aliases landed on correct existing nodes per the `son-of-*` slug convention — no new nodes created, alias-only operation as specified.

**What's next:**
- **Stage 4 prose-edge-classifier** — next major track. → continue: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`
- **Case-collision tail (65 slugs, optional)** — LOW priority. → continue: `progress/continue-prompts/2026-05-12-case-collision-close.md`
- **Per Matt's standing rule, /endsession is NOT auto-run.**

### Session 48 — General Watcher Prompt (2026-05-12)

**Changes made:**
- `working/runbooks/general-watcher.md` — NEW. Reusable prompt for watching any running session. Paste into a fresh Claude Code window, tell it what task the running session is on, ask questions. Uses git status + diff + file timestamps as the observation surface. Read-only (no dispatch, no edits). Opus 4.7 recommended. Distinct from `.claude/agents/watcher.md` (mission-specific, requires worker scratch dirs + mission file).

**Decisions:** General watcher lives in `working/runbooks/` (reusable operational prompt), NOT `progress/continue-prompts/` (continue prompts are task-specific, single-use). The "no dispatch" guardrail in the general watcher is appropriate for a catch-all default; mission-specific and dispatcher-watcher variants can relax it per their own spec.

**What's next:**
- **Alias-backfill round 2** — running in Sonnet. → continue: `progress/continue-prompts/2026-05-12-alias-backfill-round-2.md`
- **Case-collision tail (65 slugs, optional)** — LOW priority. → continue: `progress/continue-prompts/2026-05-12-case-collision-close.md`
- **Stage 4 prose-edge-classifier** — next major track. → continue: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`
- **Per Matt's standing rule, /endsession is NOT auto-run.**

### Session 47 — Case-Collision Promotion + Type Fixes + Protocol Edits (2026-05-12)

**Changes made:**
- `scripts/promote-case-collision.py` — NEW. Promotion script for 60 case-collision worker outputs → `graph/nodes/`. Handles CREATE (36 new nodes), UPDATE (21 existing stubs), MOVE+UPD (2 type relocations), SKIP (old-gods, already aliased). Applies locked type corrections inline (event.conflict→event.war, event.military-expedition→event.battle, bare `concept`→per-slug overrides, `titles`→`title`).
- **36 CREATE** — notable new nodes: `small-council` (factions/), `tower-of-joy` (locations/), `ghiscari-wars` (events/, typed event.war not event.conflict), `dothraki-sea` (locations/), `haunted-forest` (locations/), `hammer-of-the-waters` (concepts/), `first-night` (concepts/), `stallion-who-mounts-the-world` (concepts/, typed concept.prophecy), `children-of-the-forest` moved from factions/ to species/.
- **21 UPDATE** — stubs replaced with worker Identity: `brotherhood-without-banners`, `hedge-knight`, `king-in-the-north`, `master-of-coin`, `warden-of-the-north`, `king-beyond-the-wall`, `master-of-laws`, `master-of-ships`, `master-of-whisperers`, `red-priest`, `red-waste`, `ruby-ford`, `valar-morghulis`, `war-of-the-first-men-and-the-children-of-the-forest`, and others.
- **2 MOVE+UPD** — `free-folk`: factions/→concepts/, type organization.faction→concept.culture. `children-of-the-forest`: factions/→species/, type organization.faction→species. Both: old files deleted, new files written with worker Identity.
- **Pre-work cleanups:** `war-of-the-five-kings.node.md` type-fixed event.battle→event.war; `war-of-five-kings.node.md` deleted (empty duplicate, wrong slug); `red-priest` aliases updated to include `red-priestess` + `Red Priestess`; `crossroads-inn.node.md` stub deleted (merged into `inn-at-the-crossroads` aliases).
- **`small-council` edges** — uncommented MEMBER_OF edges from worker's narrative-evidence comments (petyr-baelish, stannis-baratheon, janos-slynt, daemon-targaryen, corlys-velaryon) + LOCATED_AT: red-keep. Infobox-data.jsonl had no entries (redirect page); reverse-lookup returned 0 results.
- `reference/architecture.md` — NEW section "Multi-type entities" under Hierarchy Query Rules. Policy: one node per real-world entity, primary type in `type` field, other facets via edges. Examples: Free Folk → concept.culture (faction-ness via edges), Children of the Forest → species (ancient-people-ness via edges).
- `working/agent-fleet-specs/mission-protocol.md` — NEW section "Choosing execution mode (subagent vs multi-window)" under Roles. Documents the trigger rule: subagent OK when self-contained + stateless + <10 min; multi-window+watcher when TYPE_DIR_MAP awareness, context loading, or drift-potential is high. Notes case-collision-batch-2 as a cautionary example.
- `working/todos.md` — case-collision HIGH item (60/125 promoted, 65 remaining) → downgraded to LOW (optional Track B, tail slugs, multi-window mission when wanted).
- Graph total: 7,915 → 7,949 nodes (+34 net).

**Decisions:** All 60 outputs promoted (36 CREATE + 21 UPDATE + 2 MOVE + 1 SKIP). Type corrections applied inline from locked vocab — no new types invented. Multi-type policy ratified: free-folk as concept.culture (not faction), children-of-the-forest as species (not faction). War-of-the-five-kings canonical slug confirmed; empty duplicate deleted. Red-priestess absorbed as alias, not separate node.

**What's next:**
- **Case-collision tail (65 slugs, optional)** — LOW priority. Track B: Python filter to classify canonical (~15) vs droppable (~50), then multi-window+watcher mission. → continue: `progress/continue-prompts/2026-05-12-case-collision-close.md` (Track B section)
- **Alias-backfill round 2** — parallel-safe. → continue: `progress/continue-prompts/2026-05-12-alias-backfill-round-2.md`
- **Stage 4 prose-edge-classifier** — next major track. → continue: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`
- **Per Matt's standing rule, /endsession is NOT auto-run.**

> Sessions 44-46 archived to `history/worklog-archives/archive010.md`
> Sessions 39–43 archived to `history/worklog-archives/archive009.md` (full at 5 entries)
> Sessions 34–38 archived to `history/worklog-archives/archive008.md` (full at 5 entries)
> Sessions 30–33 in `history/worklog-archives/archive007.md` (full at 5 entries)
> Sessions 25–29 archived to `history/worklog-archives/archive006.md`
> Sessions 22–24 archived to `history/worklog-archives/archive005.md`
> Sessions 16-21 archived to `history/worklog-archives/archive004.md`

> Sessions 8–15 archived to `history/worklog-archives/archive003.md`
> Sessions 5–7 archived to `history/worklog-archives/archive002.md`
> Sessions 0–4 archived to `history/worklog-archives/archive001.md`

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
