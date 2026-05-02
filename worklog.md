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
- [ ] Pass 1 v3 run on ASOS (10/82 — waves 1, 2 complete)
- [x] Pass 1 v3 run on AFFC (46/46 — complete)
- [ ] Pass 1 v3 run on ADWD (0/73)
- [x] Wiki infobox parser script (Track B) — `scripts/wiki-infobox-parser.py` produces `working/wiki-parsed/{infobox-data.jsonl (5,279), page-index.jsonl (17,657), parse-stats.md}`. `first_available` populated 2,888/5,279 (54.7%). **Three open issues:** (1) `categories[]` empty across all pages (parse API strips catlinks footer) — blocker for runbook §1.2.1 unless deferred to `entity_type_guess`, (2) `books` field parsed only 37 times vs 1,953 raw occurrences (parser bug), (3) unmapped infobox fields worth edge-taxonomy review (`dynasty`, `written by`, `hatched`, `fathers`, `vassal`, `cadet branch`).
- [ ] AGOT/ACOK supplementary entity index: script to scan existing extractions and categorize candidate entity types from narrative sections
- [ ] Pass 1 run on remaining books (ASOS, AFFC, ADWD) — blocked on prompt update + wiki parser groundwork
- [ ] Pass 2 wiki ingestion agent prompt written
- [ ] Pass 2 wiki ingestion complete
- [x] Wiki Pass 2 v1 — core (37/37 buckets complete; 855 nodes; cost $95.33; per-node $0.111 healthy per Stage-2 cold review)
- [x] Wiki Pass 2 Stage 2 cold review (Session 24; decision was `remediate`, but overturned same session — see Active Decisions)
- [x] Wiki Pass 2 Stage 3 — secondary (Session 26; FULL pipeline rebuilt as Python-only after design review showed the Stage 3b agent was inertia-driven. 472 buckets / 3,315 candidate pages → 3,314 nodes promoted. Cumulative graph: 855→4,169 then →4,239 after Tier-1+Tier-2 recovery. Cost $0. Wall-clock ~30 sec total. 0 conflicts.) Canonical pipeline: `working/runbooks/wiki-pass2-pipeline.md` (rewritten as v3).
- [x] Wiki Pass 2 Stage 3c — audit cleanup (Session 27; 4 audits run, 6 parser bugs fixed, 484 nodes re-emitted across multiple targeted runs. Tier 3 promotion campaign Passes A-D + E Phase 1 added 769 new nodes. Cat 1 orphan edges 7,784→2,955 (62% drop). Stale religion-bleed 0. Edge vocabulary lock holds.)
- [x] Wiki Pass 2 Path B — categorizer extension + promotion campaign (Session 28; bounded MediaWiki categories backfill + parser CATEGORY_TYPE_MAP. `unknown` 12,434 (70.4%) → 2,118 (12.0%). +2,240 graph nodes (5,008 → 7,248). Cat 1 orphan edges 2,955 → 1,973. 5 new dirs bootstrapped: `texts/`, `theories/`, `concepts/`, `species/`, `foods/`. New entity type `object.food`.)
- [x] Wiki Pass 2 Path B promotion completion + schema-drift audit (Session 29; 4 new entity types added: `object.material`, `concept.language`, `concept.medical`, `concept.custom`. 4 new dirs: `materials/`, `languages/`, `medical/`, `customs/`. `unknown` 2,098 → 1,257. Net +315 graph nodes (7,248 → 7,563). 130 stale-dir mismatches cleaned. Full schema-drift audit on opus: 0 HIGH / 4 MED / 4 LOW. Cat 1 orphan edges 1,973 → 1,963. Edge vocabulary lock holds. Chronology data extracted from 74 year pages: 2,245 events in `working/wiki-parsed/chronology-events.jsonl` (awaits v2 temporal-edges schema; not graph edges yet).)
- [x] Wiki Pass 2 Stage 0 foundation — alias-resolver built + run (Session 26). 707 broken refs reclaimed via slug-mismatch fix. Empirical signal validates that most remaining "broken" refs are genuinely missing concept entities (concept-pages decision: defer).
- [ ] Wiki Pass 2 Stage 4 — prose-derived edge discovery (Stage 0 prep complete + cross-references index built; Stage 4 hybrid plan documented in `working/fleet-orchestration-plan.md`. Need to build: edge-candidate-generator script, then prose-edge-classifier agent runs (full prompt ready), then peer review, then promote. Skeleton: `2026-04-27-wiki-pass2-stage4-edge-discovery.md`)
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

> Newest first. One entry per work session.

### Session 30 — Pass-1-first sequencing decision + Stage 4 v1 prompt amended (2026-05-01)

**Changes made:**
- `progress/continue-prompts/2026-05-02-pass1-mechanical-remaining-books.md` — NEW. Self-contained continue prompt for Pass 1 mechanical extraction across ACOK/ASOS/AFFC/ADWD. Order: AFFC (canary, 46ch) → ACOK (70) → ASOS (82) → ADWD (73). 271 chapters / 56 waves / ~11.5 hrs at 4 terminals. Existing `weirwood` infra reused (soft-stop + wave checkpointing = graceful-fail). Hard pre-flight checks; per-book acceptance criteria; canary-quality-check after AFFC; both manual-batched and `--chain` launch options documented.
- `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md` — UPDATED. Pass-1 dependency now resolved up-front (no longer "AGOT-only v1 + back-fill v2"). Contradiction sweep now spans all 5 books in a single pass. Open question 3 marked RESOLVED. Pre-flight check for 344/344 chapter parity added.
- `worklog.md` — Session 29 "What's next" reordered: Pass 1 first, Stage 4 v1 second. New Session 30 entry (this).

**Decisions:** Sequence Pass 1 corpus completion BEFORE Stage 4 v1 (Matt-decision Session 30, "I need to get the books in then"). Reasoning: Stage 4's contradiction-sweep component compares wiki node prose to Pass-1 mentions; AGOT-only sweep would have to re-run for each later book as Pass 1 lands. Bundling the corpus-complete prep with Stage 4 v1 launch means a single clean deliverable instead of N back-fills. Pass 1 also unblocks Pass 3/4/5/6 + trigger-table + index work that Stage 4 doesn't touch. Stage 4 v1 (when it eventually launches) will include Tier-B nodes (Matt-decision Session 30: thin-infobox ≠ thin-prose; Tier-B is where prose-edge yield is proportionally MOST valuable since Python had less to extract there). Cross-identity escalation runs INLINE in Step 3 (single load of source prose) with flags batched to `cross-identity-queue.jsonl` for end-of-pass review (avoids double-load while preserving review batching). Usage-limit graceful-fail = the existing `weirwood` soft-stop (`/tmp/extraction-stop`) + wave-boundary checkpoint pattern — no new scripts needed for Pass 1; Stage 4 launcher will mirror this pattern when it ships.

**No code changes; no agent runs; no commits this session.** Planning + prompt-amendment only.

**What's next:** Launch Pass 1 per the new continue prompt. Open questions deferred to launch-time (in iTerm session): manual-batched vs `--chain`, 4 terminals vs 2, who launches, per-book vs end-commit cadence. Stage 4 v1 follows once 344/344 extractions exist.

### Session 29 — Promotion completion + schema-drift audit + chronology extraction (2026-05-01)
**Detail:** `working/session-details/session-029.md`

**Changes made:**
- `scripts/wiki-infobox-parser.py` — UPDATED: 4 new entity types (`object.material`, `concept.language`, `concept.medical`, `concept.custom`) + Animals/Birds/Apes/Mythical creatures/Plants → species + Occupations → title. Wiki-meta SKIP additions (Feature quotes, Feature articles, Did you know, A Song of Ice and Fire Errata, Appendices, Years). Religions reordered before Organizations (Faith of the Seven mistype fix). 5 new ENTITY_TYPE_OVERRIDES (Battle of Castle Black → SKIP, Dragon → species, Wildfire → object.artifact, Fiddle → SKIP, Battle of the Blackwater (song) → object.text). PAGE_NAME_EXCLUSION_PATTERNS added (chronology / "Account of" / parenthetical-qualifier filters). War/conquest/rebellion/invasion/tourney patterns end-anchored. `author`/`authors` → WRITTEN_BY in FIELD_EDGE_MAP.
- `reference/architecture.md` — 4 new Type Reference rows (`object.material`, `concept.language`, `concept.medical`, `concept.custom`). `species` description broadened to fauna kinds.
- `scripts/wiki-pass2-promote.py` — TYPE_DIR_MAP +4 (materials, languages, medical, customs).
- `scripts/wiki-pass2-tier3-pathb-longtail.py` — TYPE_TO_DIR +4. concept.culture → factions/ formalized.
- 2 NEW scripts: `scripts/wiki-pass2-stale-dir-cleanup.py` (with Stage-1 v1 carve-out protection), `scripts/wiki-pass2-extract-chronology.py`.
- `graph/nodes/` — 7,248 → 7,563 (+315 net). 4 new dirs: `materials/` (54), `languages/` (26), `medical/` (34), `customs/` (37). Migrations: 130 stale-dir cleanup (44 titles→locations, 36 titles→artifacts, 7 titles→factions, 5 chars→religions, etc.). 4 tree-foods migrated species/→foods/. Wildfire promoted to artifacts/. Battle of the Blackwater (song) migrated _unclassified/→texts/. _stage3-preview/ removed.
- `working/audits/` — NEW: `schema-drift-2026-05-02.md` (full-corpus opus audit, $50, 0 HIGH / 4 MED / 4 LOW), `orphan-edges-2026-05-02-pathb-final.md`, cat1-full TSV.
- `working/wiki-parsed/chronology-events.jsonl` — NEW. 2,245 chronology rows from 74 year pages (1 AC - 300 AC). NOT graph edges; awaits v2 temporal-edges schema.
- 3 commits: `896c5a3d` (promotion completion + cleanup), `e6e206fd` (Step 6 audit + cleanups + WRITTEN_BY parser fix), `d6362f74` (chronology + culture decision).

**Decisions (compressed):** Schema additions per Matt's "do not defer" — 4 new types over 1 session. Food precedes species in CATEGORY_TYPE_MAP for dual-tagged dishes/eaten-things ("anything that is eaten should be in object.food"). Religions before Organizations (Faith of the Seven mistype). War regex tightened with PAGE_NAME_EXCLUSION_PATTERNS — false positives caught structurally rather than via per-batch GLOSSARY_SKIP_PAGES. Wildfire = artifact (narrative weight, like Ice/Dawn). Fiddle = SKIP (not narrative). Dragon = species (distinct from named character.dragon individuals). 130 stale-dir mismatches surfaced + cleaned via new cleanup script with Stage-1 carve-out (the carve-out specifically protects `prompt_version: v1` agent prose, NOT `v1-python` Stage-3 deterministic emits). concept.culture canonical home = factions/ (Pass B precedent; Matt-decision 2026-05-02). WRITTEN_BY edges deferred to Stage 4 — wiki structurally lacks in-world authorship infoboxes (0/156 in-world texts have Author field). Chronology from year pages → JSONL data file, NOT graph edges (locked vocabulary doesn't include OCCURRED_IN_YEAR; v2 temporal-edges design uses structured per-edge fields).

**Counts:** unknown 2,098 → 1,257 (-841). skip 8,592 → 9,167 (+575). Cat 1 orphan edges 1,973 → 1,963. Edge vocabulary violations 0 → 0 (lock holds). Schema-drift HIGH 0. Total nodes 7,563.

**What's next:**
- **Pass 1 mechanical extraction on remaining 4 books FIRST** (271 chapters; AFFC→ACOK→ASOS→ADWD; via `weirwood` in iTerm). Order decision made Session 30. Continue prompt: `progress/continue-prompts/2026-05-02-pass1-mechanical-remaining-books.md`.
- THEN Stage 4 v1 — prose-edge-classifier + cross-identity detection + full-5-book contradiction sweep (AGOT-only carve-out dropped). Continue prompt: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`. ~$50-100, 3-5 hrs.
- v2 temporal-edges schema design — uses chronology-events.jsonl as input.

### Session 28 — Path B Promotion Campaign + Parser Iteration (2026-04-30 → 2026-05-01)
**Detail:** `working/session-details/session-028.md`

**Changes made:**
- `scripts/wiki-fetch-categories.py` — NEW (bounded one-time exception fetch via `cloudscraper`; populated `working/wiki-parsed/page-categories.jsonl` with MediaWiki categories for all 17,657 pages).
- `scripts/wiki-infobox-parser.py` — UPDATED across 3 iterations: (a) CATEGORY_TYPE_MAP added (resolution order ENTITY_TYPE_OVERRIDES → PAGE_NAME_TYPE_PATTERNS → categories → species → infobox-fields → unknown); (b) skip rules for real-world publications (`Books`-without-`Books and scrolls`) and chapter-summary pages (`A Song of Ice And Fire chapters`); (c) expanded category mappings (Tourneys/Tournaments→`event.tournament`, Weddings/Assassinations/Massacres/Coronations→`event.battle`, Theories→`concept.theory`, Streets/Halls/Gates/Squares→`place.location`, Mountain clans→`organization.faction`, Deities/Gods/Goddesses→`organization.religion`, Objects/Merchant ships→`object.artifact`, Trees→`species`, Food/Drinks→`object.food`); (d) `\btourney\b` page-name pattern; (e) ENTITY_TYPE_OVERRIDES additions: Iron Throne→artifact, Dragon egg→artifact, Knight of the Laughing Tree→character.
- 6 NEW promotion scripts: `scripts/wiki-pass2-tier3-pathb-{texts,artifacts,locations,events,orgs,characters,longtail}.py`. Per-type routing via TYPE_TO_DIR map for orgs/longtail.
- `scripts/wiki-pass2-promote.py` — TYPE_DIR_MAP gained `object.food` → `foods`.
- `reference/architecture.md` — `object.food` row added (in-world food/drink); `species` description broadened (now covers in-world flora kinds — weirwood, ironwood).
- `CLAUDE.md` — narrow re-fetch exception clause (the bounded MediaWiki categories backfill, audit-logged 2026-04-30).
- `graph/nodes/` — 5,008 → 7,248 (+2,240 net). 5 new dirs bootstrapped: `texts/` (150), `theories/` (45), `concepts/` (31), `species/` (38), `foods/` (69). All other dirs grew (locations 168→1,010, characters 3,557→3,938, houses 313→556, artifacts 1→230).
- `working/wiki-parsed/{page-categories,page-index,infobox-data,parse-stats}.*` — regenerated by parser re-runs.
- `working/wiki-pass2/tier3-pathb-*` — 7 new bucket dirs with skeleton/prose artifacts preserved.

**Decisions (compressed):** Real-world publications filtered via `Books`-without-`Books and scrolls` parser rule (zero false negatives across 31 pages). Weapon-type glossary (Arakh, Bastard sword, etc.) filtered via in-script set, NOT parser, because `Terms` category is too broad for global skip. Chapter-summary pages were a 338-node disaster (events Sub-task 3 reverted, then category-skip rule added, then re-run cleanly with in-script GLOSSARY_SKIP_PAGES filtering 26 more `\bwar\b`/`\bconquest\b` false positives). New `object.food` entity type per Matt's design-values priority (food/hospitality is first-class). Trees route to `species/` (broadens species dir to flora/fauna kinds; weirwood is first-class). Trees-before-Food in CATEGORY_TYPE_MAP for dual-tagged pages (Apple, Lemon, Orange, Chestnut tree). Cultures route to `factions/` per Pass B precedent. Knight of the Laughing Tree promoted as separate node from Lyanna (cross-identity SAME_AS edge is Stage 4 territory). Animals/Birds/Fish/Plants (~219 unknown pages) DEFERRED per Matt's "don't have to get into species right now". `\bwar\b` page-name regex too greedy — needs in-script skip list per batch (lesson). `--plan` sampling before `--apply` is mandatory going forward. 14 commits this session including 1 revert; net +2,240 nodes, Cat 1 −982.

**What's next:**
- Promotion completion + schema-drift continue prompt: `progress/continue-prompts/2026-05-02-promotion-completion-then-schema-drift.md` — keep promoting nodes (audit the 836 pages with NO categories, decide on Animals/Birds/Plants schema, sweep `\bwar\b` false positives, audit `Dragon` page reclassification) THEN run the full schema-drift audit on opus (~$50 prior approval). Matt's framing: "wouldn't it be better to get this part done well? we missed several important nodes, red wedding, ashford tourney, etc."
- Stage 4 prose-edge-classifier remains queued: `progress/continue-prompts/2026-04-27-wiki-pass2-stage4-edge-discovery.md`

### Session 27 — Stage 3c audit cleanup + Tier 3 promotion campaign + Option C (2026-04-30)
**Detail:** `working/session-details/session-027.md`

**Changes made:**
- `scripts/wiki-infobox-parser.py` — UPDATED. 6 parser bug fixes: `PAGE_NAME_TYPE_PATTERNS` regex (war/rebellion/conquest/invasion/guards), expanded `ENTITY_TYPE_OVERRIDES` (Iron Throne→artifact, Triarchy + sellsword companies→faction), `<small>`-aware qualifier handling for religion-bleed, `_DATE_TEXT_RE` extensions for date-bleed, `classify_by_species()` for dragon detection, HEIR/Heirs date-link filter.
- `scripts/wiki-pass2-build-alias-resolver.py` — UPDATED. `TITLE_WORD_SLUGS` filter + `BARE_DISAMBIGUATION_THRESHOLD=3` filter. Removed `ser → gregor-clegane` and `aegon-targaryen → pisswater-prince` bad mappings.
- New scripts: `graph-query.py` (read-only investigation CLI), `orphan-edges-audit.py`, `wiki-pass2-duplicate-detector.py`, `stage3-preview-emit.py`, `wiki-pass2-fix-date-bleed-remaining.py`, `wiki-pass2-stage3-house-location-reemit.py`, `wiki-pass2-repromote-targeted.py`, `wiki-pass2-repromote-targeted-2.py`, `wiki-pass2-pass-e-phase1.py`, `wiki-pass2-tier3-pass-{a-titles,b-cultures,c-religions,d-characters}.py`, `wiki-pass2-option-c-prose-merge.py`.
- 5 audit reports added: `working/audits/{schema-drift-sample,schema-drift-sample-characters,citation-issues,orphan-edges-2026-04-30,2026-04-30b/c/d/e/f,2026-05-01}.md`.
- 6 buckets: `working/wiki-pass2/tier3-{titles,cultures,religions,characters}/`.
- `graph/nodes/` — 769 new nodes net (5,008 total). Title 91→546, faction 37→97, religion 4→20, character 3,373→3,557. Plus deletions: 3 sub-page nodes (telltale ×2, theories ×1) + 6 culture variant duplicates merged. 484 nodes re-emitted across multiple targeted re-promotion runs. 544 Stage-1 character nodes had prose-only re-emission (Option C — preserves edges).
- `working/runbooks/wiki-pass2-pipeline.md` — added Stage 3a/3b/3c framing (corrective vs additive).
- `working/tier3-promotion-plan.md` — NEW. Multi-pass promotion strategy.
- `reference/architecture.md` — `graph-query.py` discovery note added.
- `working/todos.md` — Session 27 audit findings persisted; Stage 3c framing pointer; new sub-task entries for parser bugs + Tier 3 progress.
- `progress/continue-prompts/2026-05-01-tier3-pass-e-phase-2.md` — NEW. Phase 2 continue prompt with critical-first-step framing (books + named weapons + WRITTEN_BY gap).

**Decisions (compressed):** Stage 3a/3b/3c framing memorialized — corrective (Stage 3c) vs additive (Stage 4) cleanup boundary. Sample-based audits over full-corpus runs (8x cost reduction). Stage 1 character full re-emission deferred until Stage 4 prose-edge-classifier ships (preserves agent-derived narrative edges); Option C as hybrid (prose-only enrichment) approved instead. Variant culture duplicates accepted in Pass B then merged in Phase 1 with aliases on canonicals. `*-telltale` and `*-theories` sub-pages deleted per documented exclusion policy. `*-guards` retyped as `organization.faction` per Matt's call. Bare ambiguous aliases (`ser`, `aegon-targaryen`) filtered from resolver. The big architectural finding: 70.4% of wiki pages classify as `unknown` because the parser doesn't recognize their infobox templates (or they have NO infobox at all — verified Longclaw HTML has no `class="infobox"`). The Playwright scraper got everything; the parser is the bottleneck. ENTITY_TYPE_OVERRIDES is the cheapest fix path, mirroring the Session 27 Iron Throne pattern.

**Counts:** Cat 1 orphan edges 7,784 → 2,955 (62% drop). Cat 2 alias-mismatch 784 → 268. Stale religion-bleed 24 → 0. Date-bleed 199 → 41 (parser-floor). Edge vocabulary violations 0 → 0 (lock holds). Slug-format violations 0 → 0. 8 commits.

**What's next:** Phase 2 of Tier 3 — `progress/continue-prompts/2026-05-01-tier3-pass-e-phase-2.md`. Critical first step: books + named weapons + WRITTEN_BY edge gap (`graph/nodes/artifacts/` near-empty; ~30 books and ~20 named valyrian steel swords confirmed in wiki cache but classify as `unknown`; need ENTITY_TYPE_OVERRIDES + Stage 3 promotion). Then locations/events/factions completeness (~400-600 nodes), concept-page decision (lean defer), final full audits. Acceptance criteria: Cat 1 drops to <500 edges / <100 slugs.

> Sessions 25–26 archived to `working/worklog-archives/archive006.md`
> Sessions 22–24 archived to `working/worklog-archives/archive005.md`
> Sessions 16-21 archived to `working/worklog-archives/archive004.md`

> Sessions 8–15 archived to `working/worklog-archives/archive003.md`
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
