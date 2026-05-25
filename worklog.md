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
- [~] Wiki Pass 2 Stage 4 — prose-derived edge discovery. **PIVOTED 2026-05-22 (S65) to a Pass-1-derived deterministic pipeline; wiki-chapter-summary comention DEPRECATED.** Deterministic spine BUILT + committed (S66, `047e49b3b`): `scripts/stage4-pass1-edge-candidates.py` + `stage4-pass1-evidence-locator.py` + `stage4_name_resolver.py` → **2,818 typed, ~99%-cited `book-pass1` edges at zero LLM cost** (output gitignored under `working/wiki/pass2-buckets/pass1-derived/`; audit reports under `working/wiki/data/pass1-derived-*`). S67: alias-recovery applied (spine 2,818→2,834, +16); 133 comention files deprecate-stamped in-data; **LLM tail RAN (Sonnet via `claude -p`): 2,385 typed edges (78%, $20.88) → total book-pass1 = 5,219**. Remaining: tail-violation cleanup (21/2,385, 0.88%) + 2 resolver levers (Matt's call) + tail dedup + `_tail-typed/` merge. **S68 RECALL EXPANSION:** built `scripts/stage4-pass1-extra-tables.py` (mines the OTHER relational tables; opt-in `--extra-tables`; separate `_extra-tables/` staging, canonical spine untouched) → **+529 deterministic $0 edges from Hospitality (460 GUEST_OF + 69 VIOLATES_GUEST_RIGHT)** + 4,422 Dialogue tail rows (~$30 to type) + Food/Events/Info counted-only. Recall-sample: **A 64% caught now / B 28% table-mineable / C 9% prose-only** — but the high-recall B tables (Events/Info) are prose-shaped (need ~$95+ LLM pass), Hospitality is the deterministic win, Dialogue is lowest-yield. 529 edges NOT yet merged (need endpoint filter; inherit `all-for-joffrey`-class noise). **S69 SMOKES (held at spend gate):** built Events/Info/Food candidate generators + locator-anchored all `_extra-tables` rows to `sources/chapters:line` + `--output-dir` safety flag; wrote **32,194 untyped candidate rows** (Dialogue 4,422 / Events 20,321 / Info 6,653 / Food 798); smoked Dialogue + Events/Info/Food (~$3.60, Sonnet) → both reviewer verdicts **SYSTEMATIC** (strict precision ~60-66%; reject ~90%; Events fan-out ~18% / direction-error ~7% / bare-slug ~15%). Full run re-baselined to **~$270-290 + ~3-4 days wall-clock** — **NOT launched.** 3 $0 fixes needed first: prompt vocab-restriction+anti-patterns; generator direction-validation+slug-quality gate (= endpoint filter, also cleans the 529); `candidate_kind` provenance (`stage4-tail-classifier.py:502`). `graph/edges/` still EMPTY — the FORMALIZE/merge is the milestone. Continue: `progress/continue-prompts/2026-05-25-stage4-smoke-fixes-and-formalize.md` (review doc: `STAGE4-SMOKE-REVIEW.md`). (Older wiki-comention/Haiku-bulk apparatus superseded; `prose-edge-classifier` agent at `.claude/agents/prose-edge-classifier.md` retained for the LLM-tail typing step.)
- [ ] Pass 3 voice/perception agent prompt written
- [ ] Pass 4 foreshadowing agent prompt written
- [ ] Pass 5 theory-informed agent prompt written
- [ ] Pass 6 discovery agent prompt written

### Index & Graph
- [ ] Trigger table v1
- [ ] Entity index
- [ ] Chapter index
- [x] Graph edges formalized — **v1 LANDED** (`graph/edges/edges.jsonl`, 3,842 cited Pass-1-derived edges, ~78% strict precision, all `evidence_ref`-carrying; Session 70, 2026-05-25). Haiku Events+Dialogue enrichment = v2 (in progress). See `graph/edges/README.md`.
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

### Session 69 — Stage 4 recall expansion: table-mining smokes + 2 reviews, held at $270 gate (2026-05-24)

**Detail:** `history/session-details/session-069.md`

**Changes made:**
- Committed S68 (`304192ffb`) after flagging a CLAUDE.md #9 stale-prompt contradiction (S67 was already committed; only S68 was pending — not "both uncommitted" as the prompt claimed).
- script-builder (Sonnet) extended `scripts/stage4-pass1-extra-tables.py` with Events/Info/Food candidate generators (entity-match via resolver, ≥2-entity filter, first-actor fan-out) + locator-anchored ALL `_extra-tables` rows to `sources/chapters/{book}/{chapter}.md:line`; smoke-enabled `scripts/stage4-tail-classifier.py` to read `_extra-tables` rows + added ENCOUNTERS Rule-6 verb-gate to the prompt + `--sample-n` stratified smoke. `--apply` wrote **32,194 untyped candidate rows** (Dialogue 4,422 / Events 20,321 / Info 6,653 / Food 798).
- Added `--output-dir` (+ `.resolve()` + defensive `relative_to`) to the tail-classifier so smokes NEVER append into canonical `_tail-typed/`; + redirect test. 273 tests green.
- Ran 2 smokes (Sonnet `claude -p`, ~$3.60 total): Dialogue 144 typed/56 rej/$1.68; Events/Info/Food 123 typed/77 rej/$1.89. Measured ~$0.009/row → full run re-baselined to **$270-290** (not ~$100; the Events fan-out) + ~3-4 days wall-clock (needs parallel wrapper).
- 2 `prose-edge-reviewer` audits — both **SYSTEMATIC**. Strict precision Dialogue ~60% / Events ~66%; reject ~90%; Events direction-error ~7%, fan-out spurious ~18%, bare-slug ~15%.
- NEW: `STAGE4-SMOKE-REVIEW.md` (repo root, for Matt), `working/wiki/data/pass1-derived-smoke-report.md`, continue prompt `progress/continue-prompts/2026-05-25-stage4-smoke-fixes-and-formalize.md`. Deleted superseded `2026-05-24-stage4-recall-expansion.md`.

**Decisions:** Matt's call: type all 4 tables (Dialogue/Events/Info/Food; fights ∈ Events) before formalizing; **full source-chapter re-read DEFERRED** (table-mining now, enrich later — additive "build then enrich"). **HELD at the $270 spend gate** — the smokes did their job, catching 3 systematic, fixable ($0) problem classes: (1) prompt over-types `INFORMS` (~100% wrong — it's spy→handler)/`ADVISES`/`MANIPULATES`/`SUPPORTS`/`ALIAS_OF` + uniform Tier-1; (2) generator direction-heuristic/fan-out/bare-slug emission = the SAME `all-for-joffrey` endpoint-pollution class as the 529 Hospitality edges (one fix cleans both); (3) `candidate_kind` hardcoded → provenance loss (`stage4-tail-classifier.py:502`). Reject discipline (~90%) + relationship-revealing types (SIBLING_OF/KILLS/VOWS_TO/DUELS/REVEALS_TO/CONSPIRES_WITH/FIGHTS_IN) are solid. Canonical `_tail-typed/` (2,385 edges) untouched all session. Two bugs caught by doing, not by the 273 green tests.

**What's next:** → continue: `progress/continue-prompts/2026-05-25-stage4-smoke-fixes-and-formalize.md` (**Opus 4.7** — decisions A/B/C; Sonnet for the $0 fixes). Track 1: 3 fixes (prompt vocab restriction+anti-patterns; generator direction-validation+slug-quality gate = endpoint filter; candidate_kind provenance). Track 2: re-smoke ~$4 → confirm ≥80% strict precision. Track 3: scoped full run (Events+Dialogue first; defer Info; Food separate-audit) via `run-forever` wrapper, drift-detection mandatory. Track 4: **FORMALIZE into `graph/edges/`** — the milestone; absorbs the still-open S66/S67 merge/dedup/resolver-lever finishing work (`2026-05-23-stage4-pass1-finishing.md`). 3 decisions for Matt: (A) restricted vocab, (B) table scope, (C) full-run approval after re-smoke.

---

### Session 68 — Stage 4 recall ceiling: mine all Pass 1 tables + recall-sample (2026-05-24)

**Detail:** `history/session-details/session-068.md`

**Changes made:**
- Answered Matt's two S67 questions: (a) **wiki comparison** — 1,973/6,239 resolved pairs (32%) corroborate an existing wiki edge, 4,266 (68%) are NEW; vs the deprecated comention path (29,259-candidate sink, 5,723 rows from 60/222 batches @ $55.66), Pass-1-derived = 5,219 edges @ $20.88 primary-source+cited. (b) **line marking** — locator attached verbatim quote + `file:line` to **5,816/5,886 = 98.8%** (70 chapter-level fallbacks); match-rate, not verified-correct.
- NEW `scripts/stage4-pass1-extra-tables.py` (opt-in `--extra-tables`; separate staging `pass1-derived/_extra-tables/{book}/`; **canonical spine untouched**) + `tests/test_stage4_extra_tables.py` (+81 → **431 green**) + report `working/wiki/data/pass1-derived-extra-tables-report.md`. Yield: **Hospitality → 529 deterministic $0 edges** (460 GUEST_OF + 69 VIOLATES_GUEST_RIGHT; Red Wedding correct); **Dialogue → 4,422 tail rows** (~$30 to type); Food/Events/Info **counted-only** (prose-shaped: 1,263 / 8,384 / 5,654 rows).
- Recall-sample check (`working/wiki/data/pass1-derived-recall-sample.md`, 7 chapters / 196 rels): **A=64% caught now · B=28% table-mineable · C=9% prose-only** (~3% of C high-value: Gregor/Aegon, Cersei/Maggy, Dany/Viserys).
- todos.md: added "Stage 4 — Recall Expansion" block. **All S68 work uncommitted** (Matt checkpoints).

**Decisions:** **Key tension found** — recall-sample ranks bucket-B productivity Events & Actions > Information Revealed > Hospitality > Dialogue, but the miner can only emit cheap deterministic edges from **Hospitality (#3)**; the #1/#2 recall tables are **prose-shaped (counted-only)** and need a bounded LLM pass (~14k rows, ~$95+); Dialogue ($30) is the **lowest-yield**. So 1a-as-built = A + Hospitality (~free), NOT the full ~92% the sample implied — the rest is an explicit LLM cost call. Spot-check of the Red Wedding output caught `walder-frey VIOLATES all-for-joffrey` (a toast resolved to a junk node — same index-pollution class as the pending resolver levers; 529 edges inherit it → endpoint filter before merge). **Full prose reading NOT warranted; targeted narrative-aside audit recovers the ~3% high-value C.** Nothing run beyond the deterministic miner.

**What's next:** → continue: `progress/continue-prompts/2026-05-24-stage4-recall-expansion.md` (**Opus 4.7** — decisions + merge coordination; references the finishing prompt for resolver-lever/tail-cleanup detail). Tracks: (1) merge 529 Hospitality/VIOLATES edges after endpoint filter; (2) smoke ~200 Dialogue rows before the $30; (3) **Matt decides** the bounded Events/Info LLM pass (~$95+); plus the S67 finishing work (resolver levers, tail cleanup/dedup, canonical merge) now also covering the 529 edges. #2 (fast narrow wiki layer) logged in todos.

---

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

> Session 64 archived to `history/worklog-archives/archive014.md` (archive014 now 2/5)
> Session 63 archived to `history/worklog-archives/archive014.md` (archive014 started — 1/5)
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
