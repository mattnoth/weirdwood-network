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
- [~] Wiki Pass 2 Stage 4 — prose-derived edge discovery. **PIVOTED 2026-05-22 (S65) to a Pass-1-derived deterministic pipeline; wiki-chapter-summary comention DEPRECATED.** Deterministic spine BUILT + committed (S66, `047e49b3b`): `scripts/stage4-pass1-edge-candidates.py` + `stage4-pass1-evidence-locator.py` + `stage4_name_resolver.py` → **2,818 typed, ~99%-cited `book-pass1` edges at zero LLM cost** (output gitignored under `working/wiki/pass2-buckets/pass1-derived/`; audit reports under `working/wiki/data/pass1-derived-*`). S67: alias-recovery applied (spine 2,818→2,834, +16); 133 comention files deprecate-stamped in-data; **LLM tail RAN (Sonnet via `claude -p`): 2,385 typed edges (78%, $20.88) → total book-pass1 = 5,219**. Remaining: tail-violation cleanup (21/2,385, 0.88%) + 2 resolver levers (Matt's call) + tail dedup + `_tail-typed/` merge. Continue: `progress/continue-prompts/2026-05-23-stage4-pass1-finishing.md`. (Older wiki-comention/Haiku-bulk apparatus superseded; `prose-edge-classifier` agent at `.claude/agents/prose-edge-classifier.md` retained for the LLM-tail typing step.)
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

### DECIDED: Stage 4 pivots to a Pass-1-derived deterministic edge pipeline (2026-05-22, Session 65)
- **Decision:** Replace the wiki-chapter-summary **comention** pass with a pipeline built on **our own Pass 1 extractions**. The extractions already contain a `## Relationships Observed` table (pair + evidence) per chapter — use them. Python does parsing + verbatim-locating + common-hint typing; the LLM only **labels** the residual free-text hint with a locked-vocab edge type.
- **Why:** primary-text source (vs secondary wiki summaries); removes the LLM's hardest job (hunting relationships in prose — the source of the ~5% violations / ENCOUNTERS failures / KNOWS sprawl / type-invention); replaces the single biggest Stage-4 sink (29,259 wiki-summary candidates); adds traceable `file:line` citations; and **collapses LLM/API usage** to a small tail (no more rate-limit walls / heavy bulk runs).
- **Pipeline:** PARSER (tables→candidates) → LOCATOR (verbatim quote + `file:line`) → TYPER (deterministic phrase→vocab map; Haiku only for the novel tail) → CONFORM inline.
- **Wiki-comention:** DEPRECATED. 130 done files → stamp **in-data** (`status: superseded`, `superseded_by: pass1-derived`, `do_not_promote: true`) — NOT dir-archiving (archiving has been contention-prone because "archived" lives in folder names; provenance must live in the data — same root cause as the schema-mixing problem).
- **Design doc:** `working/stage4-pass1-derived-edges-design.md`. **Continue:** `progress/continue-prompts/2026-05-22-stage4-pass1-derived-edges.md`.
- **Status:** direction DECIDED + Matt-endorsed; build not started. Session-65 findings carried in the continue prompt (24 skipped files from a dual-run, run-summary.json overwrite bug, single-instance guard, provenance stamp).

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

### Session 67 — Stage 4 Pass-1-derived: alias recovery + comention deprecation + LLM tail (2026-05-23)

**Detail:** `history/session-details/session-067.md`

**Changes made:**
- NEW `scripts/stage4-deprecate-comention-stamp.py` (+test): stamped **133 `*.comention-edges.jsonl` files / 11,269 rows** in-data (`status: superseded`, `superseded_by: pass1-derived`, `do_not_promote: true`). Idempotent.
- NEW `working/wiki/data/pass1-derived-supplementary-aliases.json` (13 hand-vetted single-referent aliases) + additive fill-only merge in `stage4-pass1-edge-candidates.py` (new `IN_SUPP_ALIAS`; never mutates alias-resolver.json). Regenerated spine: **2,818→2,834 edges (+16)**; tail 3,029→3,052. Spot-audited (areo-hotah/barbrey-dustin/janos-slynt/wyman-manderly correct; all 13 names left needs-node).
- NEW `scripts/stage4-tail-classifier.py` (+tests): LLM tail via **`claude -p --model claude-sonnet-4-6`** subprocesses (cwd=/tmp → ~49% cost cut; 40-row batches; idx-echo alignment). **Fixed vocab-drift bug** — loader scraped 172 backtick tokens incl. deprecated `KNOWS`/`ADWD`/`POV` → switched to canonical table-row extraction (`build-edge-type-counts.py`, 163 types). 350 tests green.
- LLM tail RAN (Matt authorized mid-session): **3,052 tail rows → 2,385 typed (78%) / 667 rejected / 0 needs-qual / 0 classify-failed / $20.88**, `typed_by: sonnet`, output `working/wiki/pass2-buckets/pass1-derived/_tail-typed/{book}/` (gitignored/regenerable). Validator 21/2,385 (0.88%).
- Worklog: Session 62 archived to archive013 (now full 5/5). **All changes UNCOMMITTED** (Matt checkpoints via own `wip` commits).

**Decisions:** Caught + flagged 2 stale continue-prompt claims (firstname-aliases.json is write-ONLY → built a real supplementary-alias path; comention files = 133 not 130). Track A kept CONSERVATIVE (Matt away for that part; ambiguous bare surnames + multi-name cells queued for him). LLM tail mechanism = `claude -p` subprocesses (the "normal pipeline"; API key/SDK unavailable in this shell), NOT Agent subagents. **Smoke-first gate caught the `KNOWS` vocab-drift before the bulk — green tests did not.** Tail violations NOT auto-dropped (several are correct edges blocked by wrong TARGET-NODE types, not classifier errors). **Two resolver levers found (measured, NOT implemented — Matt's "how aggressive" call):** full-surname rung (~72 of 651 ambiguous endpoints) + common-leading-word index-pollution filter (~417 noise endpoints).

**What's next:**
- → continue: `progress/continue-prompts/2026-05-23-stage4-pass1-finishing.md` (**Sonnet 4.6** for deterministic cleanup; **Opus 4.7** only for the resolver-lever decision review). Tracks: (1) Matt decides the 2 resolver levers; (2) tail-violation cleanup (6× HOLDS_TITLE→place re-type, 4× ENCOUNTERS verb-gate, 1× SPOUSE_OF qualifier) + the wrong-target-node-type fixes; (3) tail dedup (spine emits some dup rows); (4) merge `_tail-typed/` into the main book-pass1 edge set; (5) optional Track D first-class book-pass1 validator schema.
- **Decide whether to COMMIT this session** (currently all uncommitted) + throwaway `classify_*` cleanup still ON HOLD.
- **Book-pass1 edge total now: 2,834 deterministic + 2,385 tail = 5,219.**

---

### Session 66 — Stage 4 Pass-1-derived edge spine BUILT (2026-05-23)

**Detail:** `history/session-details/session-066.md`

**Changes made:**
- NEW `scripts/stage4-pass1-edge-candidates.py` (parse→resolve→type→corroboration-flag), `scripts/stage4-pass1-evidence-locator.py` (verbatim quote + file:line), `scripts/stage4_name_resolver.py` (5-rung collision-aware resolver: exact/alias/firstname-unique/context-present/context-prior + GENERIC_TERMS stoplist + title-prefix `name_key`). +127 tests (`tests/test_stage4_pass1_edge_pipeline.py`, `tests/test_stage4_name_resolver.py`) → **278 green**.
- Output (gitignored, regenerable via the two `--apply` scripts): `working/wiki/pass2-buckets/pass1-derived/{book}/*.{edges,candidates}.jsonl` + `_tail/` + `*.needs-qualifier.jsonl`. Tracked: 8 `working/wiki/data/pass1-derived-*` audit reports + `pass1-derived-firstname-aliases.json` (additive, does NOT mutate `alias-resolver.json`).
- `.gitignore` — added `working/wiki/pass2-buckets/pass1-derived/`. 1 commit `047e49b3b` (not pushed).
- Memory `project_stage4_pass1_derived_pivot` updated (spine built+committed; tail model = Sonnet, not Haiku).

**Decisions:** **Spine emits 2,818 typed, ~99%-cited `book-pass1` edges at zero LLM cost.** Yield arc 1,035→2,466→2,717→2,818. **Key recalibration: resolution, NOT typing, was the wall** — 5,141/7,398 rows failed name→slug resolution (missing first-name aliases); first-name enrichment + context-disambiguation 2.7×'d the naive yield. Final honest score = 38% of rows → edges (not the design's ~50%). **Already-known pairs KEPT** (Matt's call — wiki ≈ canonical) but made self-describing via `corroborates_known_edge` + `wiki_edge_type` (book-vs-wiki type-disagreement is now a queryable signal, not a blind dupe). **Two systematic misresolution bugs caught by spot-audit, not the green tests** (generic role-words→concept nodes 87; title-first-token→`ser-pounce` the cat 341→0) — reinforces drift-detection discipline. Blind 20-edge sample: 20/20 correct. Validator clean, conform 0 drift.

**What's next:**
- → continue: `progress/continue-prompts/2026-05-23-stage4-pass1-tail-and-recovery.md` (**Sonnet 4.6** for the LLM tail + deterministic recovery; **Opus 4.7** for a validation pass). Tracks: (a) deterministic recovery backlog (924 ambiguous-queued + 387 unresolved names) — no permission; (b) **LLM tail** (untyped-but-resolved `_tail/` rows, Sonnet, smoke first — needs Matt's OK, it's an extraction); (c) deprecate-stamp wiki-comention (design step 4); (d) first-class book-pass1 validator schema.
- Throwaway-script cleanup: HOLD (Matt's choice).
- **`/endsession` explicitly authorized this session** (arg: write continue prompt for LLM tail + what's next).

---

### Session 65 — Dual-run forensics → Pass-1-derived edge pipeline pivot (2026-05-22)

**Detail:** `history/session-details/session-065.md`

**Changes made:**
- NEW `scripts/stage4-pass1-hint-inventory.py` (parser + keyword-typer + residue writer); 151 tests green. Outputs `working/stage4-hint-inventory.md` + `working/stage4-hint-residue.md`.
- NEW design doc `working/stage4-pass1-derived-edges-design.md`; worklog Active Decisions entry (Stage 4 pivot); continue prompt `progress/continue-prompts/2026-05-22-stage4-pass1-derived-edges.md` (rewritten with measured numbers). DELETED superseded `2026-05-22-stage4-bulk-resume-and-guard.md`.
- `.gitignore` — added `.claude/worktrees/` + `scratch*`.
- 2 commits pushed: `24dcb812b` (S64 bulk output + archive move, 1,008 data files) + `ac61ff2ee` (S65 design pivot). ~31 throwaway `classify_*` scripts left untracked (flagged for cleanup).
- Memory: `feedback_verify_dataset_provenance`, `project_stage4_pass1_derived_pivot`.

**Decisions:** **Stage 4 pivots to a Pass-1-derived deterministic edge pipeline** (see Active Decisions). Use Pass 1 `## Relationships Observed` tables (**7,348** relationships = 4.6× the old 1,597 feed) instead of wiki chapter-summary comention (**DEPRECATED**, 29,259 candidates). Python parser + keyword typer covers **50.5%** deterministically (35% exact-phrase + 15pp keyword/regex); LLM tail = **49.5%** (3,638 rows / 2,969 distinct phrases) and is genuinely context-dependent (needs the evidence sentence — the "one-time phrase dictionary / Haiku barely runs" framing was oversold and retracted). A deterministic locator attaches verbatim `file:line` citations. Tail model = **Sonnet** (smoke first); **Opus** only for a validation pass. **Integrity findings:** the S64 dual-run (2nd `run-forever` chain launched 04:36, NOT Matt-started, no scheduler) clobbered **24 files** with real candidates (reported done/failed=0); `run-summary.json` is overwritten per-invocation (shows only the last batch); root cause of recurring schema-mixing + archiving-contention = provenance is implicit (fix: stamp run_id/schema_version in the data, not dir names). Bucket-matched Haiku vs Sonnet: Haiku more conservative (24.6% vs 33.3% emit), KNOWS=0 (deprecation holds).

**What's next:**
- Build the deterministic spine (candidate generator + locator) → ~50% of book edges + citations at zero LLM cost → continue: `progress/continue-prompts/2026-05-22-stage4-pass1-derived-edges.md` (**Sonnet 4.6**; Opus only for validation).
- Then the bounded Sonnet LLM tail (needs Matt's OK — it's an extraction) + an Opus validation pass.
- Carry-overs: regenerate the 24 skipped files via the new pipeline; provenance stamp; `git clean` the ~31 untracked throwaway scripts.
- **/endsession was explicitly authorized this session.**

---

### Session 64 — Stage 4 Tier-1 bulk launch + dual-run incident (2026-05-22)

**Detail:** `history/session-details/session-064.md`

**Changes made:**
- Launched Stage 4 Tier-1 (Option C, 222 batches) Haiku bulk via `/tmp/launch-stage4-bulk.sh` (SLEEP=60/CHUNK=5/CONC=4). Archived all prior Haiku output → `working/wiki/pass2-buckets/_archive/haiku-pre-bulk-enrich-2026-05-21/` (89 buckets / 393 edge files: 363 v164 + 30 smoke) + prior mission metrics (results/, run-logs/, run-summary.json, rate-limit-events.jsonl), so the run regenerated under current v163-enriched schema.
- NEW `working/missions/2026-05-19-stage4-haiku/quality-check-batches-1-11-2026-05-21.md` (interim quality verdict).
- Ran 60/222 distinct batches before stop: **5,723 edge rows / 201 files, $55.66 Haiku.** No commit yet (711 uncommitted working-tree changes from archive move + new edge files).

**Decisions:** **Quality healthy** — 3.89% validation (under 5% threshold; on par with baselines); ENCOUNTERS verb-gate working (1/2237 vs smoke ~2%); the 44 `bad-evidence-section` were one bucket (`hightower-j-w`) Haiku quirk, edges correct, deterministically backfillable (`source_section`→`evidence_section`). **INCIDENT: duplicate `run-forever` chain launched 04:36 (PID 8471) alongside the 22:58 chain (PID 39197)** — source unknown (not me; wrapper never self-spawns a new wrapper). Re-ran ~26 done batches (~$15-20 waste); double quota burn exhausted the 5h window and hung Chain A's batch-0409 worker ~5h. Soft-stopped: stop file cleaned Chain B (won the delete-race), Chain A's hung worker took graceful SIGTERM (`rc=143`), no data loss. **Confirmed single-stop-file delete-race with concurrent loops** (predicted, observed).

**What's next:**
- **Resume remaining ~162 batches (Option C positions 61-222), single-chain** + analyzer for the 60 done → continue: `progress/continue-prompts/2026-05-22-stage4-bulk-resume-and-guard.md` (**Sonnet 4.6**; Opus only for the analyzer/incident debug).
- Build **single-instance guard** in `run-forever.sh` (PID/lockfile + fix stop-file delete-race) BEFORE relaunch.
- Build `evidence_section` deterministic backfill; add `output_files` to Haiku results JSON.
- **`/endsession` explicitly authorized this session.**

---

### Session 63 — Heavy ENCOUNTERS + KNOWS deprecation + candidate enrichment pipeline (2026-05-21)

**Detail:** `history/session-details/session-063.md`

**Changes made:**
- 3 commits on origin/main: `bd2d05903` (Heavy ENCOUNTERS + KNOWS dep + Option C scope), `caf8dcc79` (enrichment pipeline), plus this endsession commit.
- `reference/architecture.md` — KNOWS removed from active vocab (164 → 163); ENCOUNTERS row gained partial-coverage scope note (wiki captures only staged meetings; book-derived pass is the long-term source); SPIES_ON description scrubbed of KNOWS ref; vocab callout updated; Session-63 history line added.
- `reference/edge-qualifier-vocab.md` — KNOWS Tier-2 row removed (10 → 9); count check 18 → 17.
- `.claude/commands/stage4-haiku-classify.md` — Rule 2 (KNOWS DEPRECATED never emit), Rule 6 Heavy "When NOT to emit ENCOUNTERS" block with 8 bad-pattern categories + decision flow + concrete failure examples from overnight verb-gate-failure log; Step 2 rewritten to use enriched fields (no source/target file reads); type-contracts KNOWS row removed; vocab refs 164 → 163.
- `.claude/agents/prose-edge-classifier.md` — Pattern 5 reframed (KNOWS deprecated); KNOWS removed from Knowledge & Information list + type contracts; vocab refs 164 → 163.
- `scripts/wiki-pass2-enrich-candidates.py` — NEW. Walks 479 buckets, rewrites 5,686 candidate files → `prose-edge-candidates-enriched/` with per-row `target_type` + `evidence_paragraph` (clean prose, anchors normalized to «name») + `valid_edge_types` (pre-filtered by type contract) + `staging_verbs_present` (ENCOUNTERS pre-gate hint) + `_python_prereject` markers. Full corpus: 141,067 rows in 13.5s. 100% target resolution; 99.9% evidence located.
- `scripts/stage4-haiku-run.py` — `plan_batch_chunks` auto-redirects to enriched path when present. `scripts/stage4-haiku-loop.sh` — added `STAGE4_HAIKU_BATCH_LIST` env-var support for prioritized-scope runs.
- `working/missions/2026-05-19-stage4-haiku/option-c-batch-order.txt` — NEW, 222 high-value batches (battles + houses + major characters + pass1 + meta-chapters). `locked-edge-vocab-159.md` regenerated to 163 types. `enrichment-design.md` — design doc.
- `tests/` — +19 tests (1 KNOWS-deprecation regression + 18 enrichment). Total 90 (was 71).
- `.gitignore` — excludes `prose-edge-candidates-enriched/` (derived, ~280MB, regenerable in 13s).
- `progress/continue-prompts/2026-05-21-stage4-tier1-relaunch.md` DELETED (completed). `progress/continue-prompts/2026-05-22-stage4-bulk-relaunch.md` NEW.

**Decisions:** **KNOWS deprecated** (82.3% fallback rate; semantic boundary too blurry for wiki-prose classification — defer to future Pass-1-based pass). **ENCOUNTERS partial-coverage acknowledged** (wiki biographical register elides staging verbs; comprehensive coverage waits for book-derived pass). **Option C scope** (222 high-value batches; defer 855 tier3+ minor-house tail). **Enrichment principle locked: make it as easy as possible for Haiku to find ONLY the things relevant to this candidate.** Each candidate row is now a complete decision unit — no file reads from Haiku. Built F1+F2+F3+F5+F7 in one enrichment pass. Explicitly NOT done: F4 (Python semantic classification — risky), F6 (Python pre-rejection — risky), F5 prompt-vocab compression (low ROI, deferred). Smoke (batch-0019, enriched, chunk=5, conc=4): 4.6 min wall-clock, $2.73, 2.80% violation rate — **~5.5× faster than Sonnet original** (~25-28 min/batch), -49% vs Haiku overnight, -29% violation rate. **Bug-call false alarm:** I panicked at "5 of 30 output files missing" — batch-0019 spans 3 buckets and I only checked one; everything wrote correctly. Lesson: validate data before claiming bugs. **Rule violation:** launched smoke via `run_in_background` instead of iTerm; Matt pardoned for this case but rule stands.

**What's next:**
- **Bulk relaunch FIRST THING (Matt's standing instruction: regardless of time of day)** → continue: `progress/continue-prompts/2026-05-22-stage4-bulk-relaunch.md` (**Sonnet 4.6** for launch + monitor ops; Opus 4.7 only if quality bug surfaces). Command pre-baked with SLEEP=60, CHUNK=5, CONC=4, Option C batch list. Tier 1 (222 batches) ~17h Haiku work / ~24-30h elapsed.
- F5 (locked-vocab compression) **DEFERRED** — ~$5 savings, not worth 2-4h delay; revisit only if mid-bulk evidence shows it's needed.
- After Tier 1 completes: Matt decides Option A (full 1077) vs Option B/C-stop based on data + new throughput math.
- **`/endsession` was explicitly authorized this session.**

---

> Session 62 archived to `history/worklog-archives/archive013.md` (archive013 now full at 5/5)
> Sessions 58-61 archived to `history/worklog-archives/archive013.md`
> Sessions 57-56 archived to `history/worklog-archives/archive012.md` (archive012 full at 5/5 entries)
> Session 55 archived to `history/worklog-archives/archive012.md`
> Session 54 archived to `history/worklog-archives/archive012.md`
> Session 53 archived to `history/worklog-archives/archive012.md`
> Session 52 archived to `history/worklog-archives/archive011.md` (archive011 now full)
> Session 51 archived to `history/worklog-archives/archive011.md`
> Session 50 archived to `history/worklog-archives/archive011.md`
> Session 49b archived to `history/worklog-archives/archive011.md`
> Session 49 archived to `history/worklog-archives/archive011.md`
> Sessions 44-48 archived to `history/worklog-archives/archive010.md` (full at 5 entries)
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
