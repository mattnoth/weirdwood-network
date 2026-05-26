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
- [x] Entity index — **REBUILT to all categories (Session 72).** `graph/index/` previously covered only characters/houses/locations/artifacts/chapters; `scripts/build-entity-indexes.py` extended with 14 more `TYPE_CONFIGS` → **1,847 new `*.index.json`** (factions, titles, events, religions, species, texts, concepts, materials, foods, theories, customs, languages, medical, prophecies). This was the real "entities aren't there" gap (the nodes always existed; the index didn't cover them). Mention-stats zero for wiki-sourced entities Pass 1 never tagged (expected).
- [x] Chapter index (per-chapter `*.mentions.json` under `graph/index/chapters/`)
- [x] Graph edges formalized — **v1.3 (Session 72)** (`graph/edges/edges.jsonl` = **3,811** cited Pass-1-derived edges; v1 3,842→v1.2 3,825→v1.3 3,811). **v1.2:** type-contract re-validation vs complete node set (−17 wrong, +3 RULES→COMMANDS retype, kept 16 real `COMMANDS→faction`). **v1.3 resolver pass:** title-person disambiguation — 6 ship/artifact/title nodes named after people (`lord-tywin`=Cersei's dromond, `queen-cersei`, `lord-renly`, `princess-myrcella`, `lady-olenna`, `khal-jhaqo`) were capturing person references via exact slug-match; remapped → their characters (−12 dups) + new `CAPTAIN_OF`/`CREW_OF` target-not-character contract dropped 2 mis-typed "captain of the guard" edges. ~78% strict precision; all `evidence_ref`-carrying. Haiku Events+Dialogue enrichment = v2, separately NOT-YET (~62% out-of-sample; `progress/continue-prompts/2026-05-25-stage4-locator-grounding.md`).
- [ ] Convergence maps

### Reference Materials
- [x] Foreshadowing events list (`reference/foreshadowing-events.md`)
- [ ] Theory seeds file
- [ ] Taxonomy reference doc
- [x] Architecture spec (original outline exists, needs refinement)

---

## Active Decisions

> Design questions that need resolution. Tag with status: OPEN, DECIDED, DEFERRED.

### RESOLVED/CORRECTED: The "unpromoted-node gap" was a FALSE ALARM — node layer is whole (2026-05-25, Session 72)
- **S71 claimed** ~7,251 staged `.node.md` were never promoted and PAUSED edges until "the node layer is whole." **That was a file count without a slug intersection — and it was wrong.** S72 verified three ways: (1) slug reconciliation — **7,039 of 7,047** unique staged-skeleton slugs are ALREADY in `graph/nodes/`; only **8** truly net-new. (2) `promote.py` dry-run — of ~3,730 promotable Tier-A/B pages: **43 net-new / 2,367 byte-equal / 1,307 byte-different**. (3) promoted (8,299) > staged (7,047). **No backlog. The skeletons are stale intermediate artifacts; promoted nodes are canonical (and in substantive conflicts, RICHER).**
- **What was actually wrong (all FIXED S72, $0/deterministic):** (a) **the INDEX, not the nodes** — `graph/index/` only had builder configs for characters/houses/locations/artifacts; 14 categories were never indexed → "entities weren't there." Extended `build-entity-indexes.py` + rebuilt (1,847 new index files). (b) **type-contract validator** false-dropped `COMMANDS→faction` because Contract 4 only checked `graph/nodes/characters/` (the factions existed all along). Fixed: COMMANDS accepts character OR faction/house targets. (c) **`refine-v1-edges.py` never passed `slug_category_index`** → category-based contracts never fired. Fixed.
- **Edge re-validation + v1.2 APPLIED (Matt's "re-resolve + re-validate, not re-extract"):** re-ran refine with the fixed validator → applied to **`graph/edges/edges.jsonl` = 3,825** (was v1 3,842). 16 faction-COMMANDS recovered, 17 wrong rows dropped, 3 RULES→COMMANDS retyped. Clean schema preserved. Re-resolve was a no-op (nodes never missing). **COMMITTED Session 72.**
- **Lesson for next time:** the health check is a **slug intersection** (staged-vs-promoted by slug), NOT a file count — a file count is exactly what produced this false alarm. 805 tests green.
- **Resolved this session:** ① v1.2 applied + committed. ② net-new "promotion" CANCELLED — all 8 are singular/variant **dups** of existing canonical nodes (andals/dornishmen/free-folk/war-of-the-five-kings/stormlanders/lhazareen/lyseni), not promotable. ③ `lord-tywin` = a real ship artifact (Cersei's dromond), NOT a mis-type; the bad edge referencing it was correctly dropped — no node action.
- **Resolver pass DONE (2026-05-26, edges v1.3):** title-person disambiguation in `stage4_name_resolver.py` (a title-prefixed name that exact-matches a NON-character node now prefers the character via a char-restricted ladder; `resolved-title-person` rung) + `CAPTAIN_OF`/`CREW_OF` target-not-character contract. Applied to `edges.jsonl` (3,825→3,811): remapped 6 collision slugs, dropped 2 mis-typed CAPTAIN_OF. 814 tests green.
- **Still open (next sessions):** folder reorg (wiki/scripts dumps + leftover worktrees); scratch: 2 scratch files git-tracked (`git rm --cached`). Possible deeper resolver work: alias completeness for the S67 unresolved/ambiguous endpoints. See `CONTINUE-node-recovery-and-edges.md`.

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

### Session 72 — CORRECTION: "unpromoted-node gap" was a false alarm; index + validator + resolver FIXED; edges v1→v1.3 (2026-05-25→26)

**Model:** Opus 4.7 (autonomous stretches — Matt stepped away mid-session with "do all of this"). **Detail:** `history/session-details/session-072.md`. **Commits:** `eb3c6b18b`, `4f149f7b6`.

**The correction (CLAUDE.md #9 in action):** S71 handed off "~7,251 staged nodes never promoted → edges PAUSED." **Verified false this session** — it was a file count without a slug check. Slug reconciliation: **7,039/7,047** staged-skeleton slugs ALREADY in `graph/nodes/`; only **8** net-new. `promote.py` dry-run: 43 net-new / 2,367 byte-equal / 1,307 byte-diff. Promoted (8,299) > staged (7,047). **No backlog; node layer whole.** Did NOT mass-promote on the false premise.

**What was actually wrong — all FIXED ($0/deterministic):**
- **The index, not the nodes** (what Matt actually saw). `graph/index/` only had configs for characters/houses/locations/artifacts; 14 categories never indexed. script-builder extended `scripts/build-entity-indexes.py` + rebuilt → **1,847 new `*.index.json`** (factions 191, titles 542, events 371, …).
- **Type-contract validator** false-dropped `COMMANDS→faction` (Contract 4 only checked `graph/nodes/characters/`; the factions existed all along). Fixed `stage4-type-contract-validator.py`: COMMANDS accepts character OR commandable unit (faction/house); drops place(two-hop)/object; flags unknown. `TestCommandsContract` rewritten.
- **`refine-v1-edges.py` never passed `slug_category_index`** → category-based contracts never fired (latent bug). Fixed (builds + passes index; test stub updated). **805 tests green.**

**Edge re-validation (Matt's "re-resolve + re-validate, not re-extract"):** re-ran refine with the fixed validator over READ-ONLY `edges.jsonl` → **corrected v1.2 candidate 3,825 rows** (`_v1-refine/edges-v1.1-candidate.jsonl`); **16 faction-COMMANDS recovered** (gunthor→stone-crows, victarion→iron-fleet, …), 17 hard-drops (13 wrong COMMANDS + 1 MOTIVATES + 3 VIOLATES_GUEST_RIGHT). Pre-fix v1.1 preserved in `_v1-refine/superseded-2026-05-25-preCommandsFix/`. **`graph/edges/edges.jsonl` = 3,842 FROZEN/untouched** (md5 `9617c73b…`).

**Decisions/findings:** 1,307 skeleton↔node "conflicts" = stale staging vs canonical (richer) nodes → **NO ACTION** (re-promoting would downgrade). Data-smell tail: `lord-tywin` resolves to `graph/nodes/artifacts/` (alias/mis-type). 0.1 scratch: `endsession.md` already says don't triage scratch + `.gitignore scratch*` covers it, BUT 2 scratch files are git-tracked (`git rm --cached`). **Nothing committed; did NOT run /endsession** (no permission). Health-check lesson: use a **slug intersection**, not a file count.

**Then (same session, Matt back — "go for 1,2,3, commit"):** ① **applied v1.2 → `edges.jsonl` = 3,825 + committed.** ② net-new promotion CANCELLED (all 8 are dups of canonical nodes). ③ `lord-tywin` = real ship artifact, bad edge already dropped — no-op. Answered Matt's Q: fixing `graph/index/` does NOT help the edge scripts (they read `graph/nodes/`, not the index); the next real edge-quality lever is the **resolver/name-disambiguation** layer (the `lord-tywin` ship-vs-man class), a scoped follow-up.

**Resolver pass (2026-05-26, continued same session → edges v1.3 = 3,811):** title-person disambiguation in `stage4_name_resolver.py` + `CAPTAIN_OF`/`CREW_OF` validator guard. Measured 42 collision edges, simulated to de-risk (6 clean wins, ship `lady-marya` protected), applied to `edges.jsonl`. 814 tests green. Answered Matt's Q on whether the index helps edge scripts: no (decoupled) — the resolver is the lever.

**What's next:** → `CONTINUE-node-recovery-and-edges.md`. Open: folder reorg (wiki/scripts dumps + leftover worktrees); scratch untrack (`git rm --cached` 2 files); optional deeper resolver work (alias completeness for S67 unresolved/ambiguous endpoints).

---

### Session 71 — Stage 4 accuracy suite + prompt overhaul → PIVOT: unpromoted-node gap found, edges PAUSED (2026-05-25)

**Detail:** `history/session-details/session-071.md` + tracked docs: `working/wiki/data/readiness-review-fresh.md`, `prompt-review-opus-1.md`/`-2.md`, `pass1-derived-staging-manifest.md`, `pass1-derived-v1.1-applied.md`.

**Changes made (all $0/deterministic except 3 smokes ~$3.4 Haiku; NOTHING committed; `graph/edges/edges.jsonl` untouched):**
- **Deterministic accuracy suite (NEW, tested):** `stage4-{quote-relevance-filter,type-contract-validator,fresh-relocate-sample,refine-v1-edges,produce-v1-1-candidate}.py`; improved `stage4-pass1-evidence-locator.py` (locator v2 + `locate_quality`); `stage4-tail-classifier.py` prompt v4 (GOVERNING PRINCIPLE + GATE1/2/3, evidence-grounding, gated types 5→13, `prompt_version`/`prompt_sha` stamping). 119+ tests green.
- **Smokes:** smoke4 (60%), smoke5 (seed-4242, **72.5% raw**; post-filter looked ~80-91% but OVERFIT), **smoke6 (seed-7777 OUT-OF-SAMPLE = ~62% raw)**. v1.1 refinement candidate built (`_v1-refine/edges-v1.1-candidate.jsonl`) — **NOT applied.**
- NEW top-level continue prompt `CONTINUE-node-recovery-and-edges.md` + staging manifest.

**Decisions:** **PIVOT — edge formalization PAUSED.** Edge work surfaced that a large chunk of the wiki Pass-2 entity schema was **never promoted**: `graph/nodes/` = **8,299** nodes but **~7,251 staged `.node.md` sit unpromoted in `working/wiki/pass2-buckets/*/skeleton/`** (the "staging nodes ready" Matt remembered — NOT lost). Smoking gun: the type-contract validator false-dropped real `COMMANDS→faction` edges (stone-crows/second-sons/iron-fleet/brotherhood) because those factions aren't in `graph/nodes/characters/` — the node gap producing false edge-drops. So edges can't be finalized until nodes are whole. **Enrichment (Events+Dialogue Haiku) separately = NOT-YET** (~62% out-of-sample; root cause = locator hint↔quote decoupling; fresh-Opus-review caught my ~80-91% overfit claim). **Will edges be fully redone? No** — re-resolve + re-type-check (deterministic, $0) over existing candidates, NOT re-extract. Core v1 (3,842) FROZEN.

**What's next:** → **PRIMARY: `CONTINUE-node-recovery-and-edges.md`** (top-level; **Opus 4.7** "fixer & finder"). Stream 1 = node accounting + promote the ~7,251 staged skeletons; Stream 2 = edge re-validation against complete nodes; Stream 3 = folder reorg (wiki/scripts are dumps); Stream 4 = scratch-check (no project hook found — IDE-selection surfacing). SECONDARY (gated behind nodes): `progress/continue-prompts/2026-05-25-stage4-locator-grounding.md`. All Stage-4 scripts UNCOMMITTED.

---

### Session 70 — graph/edges/ v1 LANDED + Haiku enrichment gate (NO-GO) (2026-05-25)

**Detail:** `working/wiki/data/pass1-derived-enrichment-gate-result.md` + `pass1-derived-smoke2-headtohead-review.md` serve as the detail (no separate session file).

**Changes made:**
- **graph/edges/ v1 COMMITTED (`c3880e160`)** — `graph/edges/edges.jsonl` (3,842 cited Pass-1-derived edges) + `graph/edges/README.md`. First populated edge layer; graph is now traversable.
- NEW `scripts/stage4-formalize-edges.py` (+test, 99 green): merge spine(2,834 emit)+S67 tail(2,385 emit)+Hospitality(529)=5,748 → endpoint-gate −109, tail-violation quarantine −10, dedup −1,543 → 4,086 → `--precision-filter` (gated-type −234, CONTEMPORARY_WITH person↔person −10) → **3,842**. Quarantines preserved in `_formalized/` (gitignored).
- 3 $0 fixes to `stage4-tail-classifier.py` + `stage4-pass1-extra-tables.py` (+tests): vocab gating (5 types)+tier guidance; generator direction-validation + reusable `is_low_quality_endpoint()`; provenance (candidate_kind preserved, typed_by from `--model`). Rule-11 anti-pattern patches (CONTEMPORARY_WITH/COMPANION_OF/CITED_BY/CONTRADICTS/ASSAULTS/NURSED_BY). `--abort-after-consecutive-failures` (exit 42) + `--skip-existing`/`--output-dir` hardening.
- NEW `scripts/stage4-tail-bulk-forever.sh` (rate-limit-surviving overnight loop). **UNCOMMITTED** (classifier hardening + wrapper; 137 cls tests green) — commit with whichever path Matt picks.
- NEW reviews: `pass1-derived-smoke2-headtohead-review.md`, `pass1-derived-enrichment-gate-result.md`. Deleted continue prompt `2026-05-25-stage4-smoke-fixes-and-formalize.md` (executed).

**Decisions:** Matt: **deliverable-first** + head-to-head re-smoke (not Sonnet-only). Head-to-head (same 200 rows, post-lockdown): **Haiku 76% / Sonnet 78% strict** — neither cleared 80%; Sonnet's 2pt edge NOT worth 4.4× cost → **Decision C = enrich with Haiku**. Rule-11 patches cleanly eliminated the 2 target biases (CONTEMPORARY_WITH/COMPANION_OF→0) but post-patch precision = **~70%** (new RESPECTS drift + structural candidate-noise: evidence-mis-pairing, direction flips — the same ceiling as the v1 core; prompt can't reach it). **Bulk HELD overnight, $0 spent** — honored the agreed ≥80% gate. The deterministic core (explicit Pass-1 Relationships pairs) is the higher-quality layer; the extra-tables enrichment has a ~70-80% ceiling.

**What's next:** → continue: `progress/continue-prompts/2026-05-25-stage4-enrichment-decision.md` (**Opus 4.7** — A/B/C decision + review; Sonnet for the $0 builds). Options (full detail in `working/wiki/data/pass1-derived-enrichment-gate-result.md`): **A** one iteration (RESPECTS gate + direction reminder + deterministic quote-relevance filter — also cleans v1) then re-smoke; **B** run bulk at ~70% + heavy filters + runtime verify (~$60); **C** ship core-only, defer enrichment. Rec: **A one-shot → fall back to C**; quote-relevance filter is highest-value next build either way. Commit the uncommitted classifier hardening + wrapper with whichever path.

---

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

> Session 67 archived to `history/worklog-archives/archive014.md` (archive014 now full at 5/5)
> Session 66 archived to `history/worklog-archives/archive014.md`
> Session 65 archived to `history/worklog-archives/archive014.md` (archive014 now 3/5)
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
