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
- [x] Graph edges formalized — **v1.3 (Session 72)** (`graph/edges/edges.jsonl` = **3,811** cited Pass-1-derived edges; v1 3,842→v1.2 3,825→v1.3 3,811). **v1.2:** type-contract re-validation vs complete node set (−17 wrong, +3 RULES→COMMANDS retype, kept 16 real `COMMANDS→faction`). **v1.3 resolver pass:** title-person disambiguation — 6 ship/artifact/title nodes named after people (`lord-tywin`=Cersei's dromond, `queen-cersei`, `lord-renly`, `princess-myrcella`, `lady-olenna`, `khal-jhaqo`) were capturing person references via exact slug-match; remapped → their characters (−12 dups) + new `CAPTAIN_OF`/`CREW_OF` target-not-character contract dropped 2 mis-typed "captain of the guard" edges. ~78% strict precision; all `evidence_ref`-carrying. **S74: core SHIPPED — citations re-grounded** (`scripts/stage4-reground-core-citations.py` corrected 3,676/3,811 `evidence_ref` line numbers; quote text + edge set byte-identical; fixed the latent `:11` locator bug — `read_chapter_prose` stripped blanks so all refs pinned to the first prose line). **Graph exercised: 100% of 898 edge endpoints resolve to a node, 0 orphans, fully traversable.** **Haiku Events+Dialogue enrichment = NO-GO, SHELVED** (post-locator-fix out-of-sample smokes 74.5%/62.5%, <75% gate; v5 precision rules authored + kept for any future revisit). Commit `63b8b461a`.
- [x] Graph query + audit tooling — **NEW (Session 75).** `scripts/graph-query.py` (S39 node-inspection EXTENDED with `--neighbors`/`--path`/`--health`/`--edges` over canonical `edges.jsonl`) + NEW `scripts/graph-conflict-pairs.py` (read-only precision-cleanup review queue → `working/wiki/data/graph-conflict-pairs.{md,jsonl}`; 32 flagged pairs, mostly temporal arcs). 920 tests green. `--health` confirms 0 orphans / 100% traversable.
- [x] Edge temporal-scoping — **NEW (Session 76).** `scripts/stage4-edge-temporal-scope.py` (+58 tests) annotates all 3,811 edges with `(book_order, chapter_number)` + temporal-aware conflict re-audit → **31/32 flagged pairs are temporal arcs** (`--window chapter`), 1 true same-window (`cersei↔tyrion`). Read-only on `edges.jsonl`. Outputs `working/wiki/data/edges-temporal-scoped.jsonl` + `graph-conflict-pairs-temporal.{md,jsonl}`.
- [~] Events edge enrichment (Stage 4) — **MODEL DECIDED + RUNNER READY, NOT LAUNCHED (Session 77, 2026-05-27).** Haiku-vs-Sonnet comparison done on the SAME rows (AGOT 600 + ACOK 600 out-of-sample): **Haiku ~85% / ~90% strict** (vs Sonnet's 82-86%), 0 walls, ~$1.8/run → **DECISION: Haiku** for the full run (fresh all-Haiku, single provenance; Sonnet partial `_events-run-20260527/` superseded). Residual errors were **bad candidate slugs** (disambiguation, not model error) → **FIXED**: `stage4-pass1-extra-tables.py` now passes `slug_category` so the title-person rung fires (lord-tywin→tywin-lannister) + endpoint blocklist (bastard/dog/four-storms/hunt) → pass1_events **16,572→16,502 clean rows** (backup `_extra-tables.pre-slugfix-20260527/`). Runner BUILT + HARDENED: `scripts/stage4-tail-classifier.py` gained `--sleep-between` (chunked, stop-file-aware) + `--validate-every`/`--reject-rate-floor` (drift-halt exit 43); wrapper `scripts/stage4-events-bulk-run.sh` (paced auto-resume, `sleep_with_stop_check`, SIGINT-terminal, MAX_ITER, stop-file). **1072 tests green.** Comparison report: `working/session-results/2026-05-27-haiku-vs-sonnet-events.md`. Runbook: `working/runbooks/stage4-events-haiku-bulk.md`. NOT merged into `edges.jsonl` (separate gated milestone).
- [ ] Convergence maps

### Reference Materials
- [x] Foreshadowing events list (`reference/foreshadowing-events.md`)
- [ ] Theory seeds file
- [ ] Taxonomy reference doc
- [x] Architecture spec (original outline exists, needs refinement)

---

## Active Decisions

> Design questions that need resolution. Tag with status: OPEN, DECIDED, DEFERRED.

### OPEN: Events Haiku bulk — TEMP SLEEP, must lower before Matt travels (2026-05-27, Session 77)
- **OPERATIONAL — a future session must act on this.** Matt starts the Events Haiku bulk himself in iTerm **today/tomorrow** with a **TEMPORARY long sleep (`STAGE4_SLEEP_BETWEEN=1800`, 30 min)** so it runs gently alongside his concurrent Opus work. **Before he leaves (~2026-05-29), a session must LOWER the sleep to `600` (or `300`) for the unattended phase** so it finishes in reasonable time.
- **Launch command (stable output dir so cross-day resume works — do NOT rely on the datestamp default):**
  ```
  STAGE4_OUT=/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk \
  STAGE4_SLEEP_BETWEEN=1800 STAGE4_VALIDATE_EVERY=25 \
  bash /Users/mnoth/source/asoiaf-chat/scripts/stage4-events-bulk-run.sh
  ```
- **To change the sleep (the future session's job):** `touch /tmp/stage4-stop` (stops cleanly within ~1 batch+60s) → wait for clean exit → relaunch the SAME command with `STAGE4_SLEEP_BETWEEN=600` and the **same `STAGE4_OUT`** (`--skip-existing` resumes). Runbook: `working/runbooks/stage4-events-haiku-bulk.md`.
- Drift safety: `--validate-every 25` hard-stops (exit 43) on schema drift / reject-rate <0.70. First-checkpoint precision spot-read + completion read owed (orchestrator).

### OPEN: 3 gated core-cleanups — still await Matt's before/after sign-off (carried from Session 76)
- Model decision RESOLVED (→ Haiku, see above). Still pending Matt's OK (do NOT touch `edges.jsonl` without before/after sign-off):
- **3 gated core-cleanups — await Matt's before/after sign-off (do NOT touch `edges.jsonl` without it):** (1) drop the 2 `cersei↔tyrion` LOVES mis-types (3,811→3,809); (2) retype the ~22 physical `ASSAULTS`→`ATTACKS` (`ASSAULTS`=sexual only per architecture.md:233; fix the spine phrase→type map too); (3) merge-time `OWNS→BONDED_TO` for direwolf/dragon targets (Events output, not core). The Events v5 prompt already obeys the ASSAULTS rule (emitted 0).
- **Operational:** long unattended runs MUST use a sleep-until-reset auto-resume wrapper — S76's bare worker sat idle all night after one cap wall.

### AMENDED: Enrichment is DEFERRED, not abandoned — Events is the next surface (2026-05-26, Session 75)
- **Decision (Matt):** Softens the S74 "SHELVE enrichment" below. Matt **does want to enrich the graph** — step by step, with **Events as the next surface**, but **gated behind the precision changes landing first** (the conflict-pair cleanup built this session + the kept v5 precision rules). **Not launched this session** (Matt chose to end + queue it).
- **Temporal flagging endorsed** — per-edge "when does this apply" is the right structural answer to the contradictory-edges problem, and it's largely deterministic (every edge carries `evidence_book`+`evidence_chapter`; chapter frontmatter has `chapter_number`).
- **DO NOT** run the ~$270 Events bulk blind — it failed the 75% precision gate (S74). The next Events pass must fold in the precision precursors. Continue: `progress/continue-prompts/2026-05-26-stage4-events-enrichment.md`. Memory: `project_enrichment_wanted_events_next`.

### DECIDED: Ship the deterministic core; SHELVE Events+Dialogue LLM enrichment (2026-05-26, Session 74)
- **Decision (Matt):** Ship `graph/edges/edges.jsonl` (3,811 cited deterministic edges, ~78%) as THE edge layer. **Do NOT run the ~$75 Events+Dialogue Haiku enrichment.**
- **Why:** After fixing the locator's hint↔quote decoupling (the gate-opener), two fresh out-of-sample smokes came in **74.5% / 62.5%** strict — unstable and below the 75% gate. Clear-case precision is 83-89% but the model over-emits borderline inferences. A ~70-74% enrichment layer is *noisier than the spine it sits on*, with no scheduled patcher; per the project value "a wrong cited edge is graph pollution — worse than no edge." The ~78% deterministic core is the better artifact.
- **What's kept:** the locator fix (hint-anchored grounding + `:11` line-number fix), the `quote_source` passthrough, and the **v5 precision rules** (`v5-precision-rules`) — all harmless improvements retained in case enrichment is ever revisited. The v5 re-smoke was killed mid-flight when the decision landed (~$0 extra).
- **Citation re-grounding (same session):** verifying the core revealed it carried the SAME latent `:11` bug (3,784/3,811). Re-grounded deterministically (line-numbers-only; quote text + edge set byte-identical) so the shipped core's citations are navigable. The core is **still v1.3** — same edges/types, repaired citations.
- **Next (deferred levers, NOT enrichment):** conflict-pair audit (precision cleanup), `scripts/graph-query.py`, edge temporal-scoping. See `progress/continue-prompts/2026-05-26-graph-exercise-followups.md`.

### RESOLVED/CORRECTED: The "unpromoted-node gap" was a FALSE ALARM — node layer is whole (2026-05-25, Session 72)
- **S71 claimed** ~7,251 staged `.node.md` were never promoted and PAUSED edges until "the node layer is whole." **That was a file count without a slug intersection — and it was wrong.** S72 verified three ways: (1) slug reconciliation — **7,039 of 7,047** unique staged-skeleton slugs are ALREADY in `graph/nodes/`; only **8** truly net-new. (2) `promote.py` dry-run — of ~3,730 promotable Tier-A/B pages: **43 net-new / 2,367 byte-equal / 1,307 byte-different**. (3) promoted (8,299) > staged (7,047). **No backlog. The skeletons are stale intermediate artifacts; promoted nodes are canonical (and in substantive conflicts, RICHER).**
- **What was actually wrong (all FIXED S72, $0/deterministic):** (a) **the INDEX, not the nodes** — `graph/index/` only had builder configs for characters/houses/locations/artifacts; 14 categories were never indexed → "entities weren't there." Extended `build-entity-indexes.py` + rebuilt (1,847 new index files). (b) **type-contract validator** false-dropped `COMMANDS→faction` because Contract 4 only checked `graph/nodes/characters/` (the factions existed all along). Fixed: COMMANDS accepts character OR faction/house targets. (c) **`refine-v1-edges.py` never passed `slug_category_index`** → category-based contracts never fired. Fixed.
- **Edge re-validation + v1.2 APPLIED (Matt's "re-resolve + re-validate, not re-extract"):** re-ran refine with the fixed validator → applied to **`graph/edges/edges.jsonl` = 3,825** (was v1 3,842). 16 faction-COMMANDS recovered, 17 wrong rows dropped, 3 RULES→COMMANDS retyped. Clean schema preserved. Re-resolve was a no-op (nodes never missing). **COMMITTED Session 72.**
- **Lesson for next time:** the health check is a **slug intersection** (staged-vs-promoted by slug), NOT a file count — a file count is exactly what produced this false alarm. 805 tests green.
- **Resolved this session:** ① v1.2 applied + committed. ② net-new "promotion" CANCELLED — all 8 are singular/variant **dups** of existing canonical nodes (andals/dornishmen/free-folk/war-of-the-five-kings/stormlanders/lhazareen/lyseni), not promotable. ③ `lord-tywin` = a real ship artifact (Cersei's dromond), NOT a mis-type; the bad edge referencing it was correctly dropped — no node action.
- **Resolver pass DONE (2026-05-26, edges v1.3):** title-person disambiguation in `stage4_name_resolver.py` (a title-prefixed name that exact-matches a NON-character node now prefers the character via a char-restricted ladder; `resolved-title-person` rung) + `CAPTAIN_OF`/`CREW_OF` target-not-character contract. Applied to `edges.jsonl` (3,825→3,811): remapped 6 collision slugs, dropped 2 mis-typed CAPTAIN_OF. 814 tests green.
- **Still open (updated S73):** worktrees REMOVED; scripts folderization DEFERRED (low value / high import-coupling risk); 27 comention scripts KEPT (revival recall lever — do NOT re-propose archiving); scratch left tracked per Matt. Deferred levers: **skeleton-untrack** (7,180 tracked stale `skeleton/*.node.md`, entangled w/ ~24 promotion scripts — its own decision); resolver alias completeness for S67 unresolved/ambiguous endpoints (`progress/continue-prompts/2026-05-23-stage4-pass1-finishing.md`). Edge enrichment gate-opener: `progress/continue-prompts/2026-05-25-stage4-locator-grounding.md`.

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

### Session 77 — Events: model DECIDED (Haiku), candidate slug-fix, paced runner built+hardened, bulk LAUNCHED (2026-05-27)

**Model:** Opus 4.7 (orchestrator) + script-builder (Sonnet 4.6) ×3. **Detail:** `history/session-details/session-077.md`. **Commit:** this endsession commit.

**Changes made:**
- NEW `scripts/stage4-model-run-diff.py` — diffs two classifier runs on the SAME rows (match key `(source,target,chapter,hint_raw)`, NOT `evidence_ref` which only exists on emits). Self-diff = 100%.
- `scripts/stage4-tail-classifier.py`: fixed `--smoke` silently ignored under `--input-dir` (had started a full 415-batch run instead of 600; killed at $0); added `--sleep-between` (chunked, stop-file-aware), `--validate-every`/`--reject-rate-floor` (drift-halt **exit 43**), `STOP_FILE` honoring mid-sleep + between batches. **1072 tests green.**
- `scripts/stage4-pass1-extra-tables.py`: SLUG-FIX — now passes `slug_category` so the S72 title-person rung fires (`lord-tywin`→`tywin-lannister`) + `ENDPOINT_BLOCKLIST` (bastard/dog/four-storms/hunt). Regenerated: pass1_events **16,572→16,502 clean** (5 bad-slug classes →0; 44 `lord-tywin` remapped, 15 dropped). Backup `_extra-tables.pre-slugfix-20260527/`.
- NEW `scripts/stage4-events-bulk-run.sh` — paced auto-resume wrapper; hardened against "sleeps-but-never-restarts" via `sleep_with_stop_check` (pattern from `stage4-haiku-loop.sh`), exit-130(Ctrl-C)-terminal, `MAX_ITER=200`. Runbook `working/runbooks/stage4-events-haiku-bulk.md`. Comparison report `working/session-results/2026-05-27-haiku-vs-sonnet-events.md`.

**Decisions:** **(1) Model = HAIKU** for the full Events run — validated on 2 fresh out-of-sample samples (AGOT 600 ~85%, ACOK 600 ~90% strict; 0 walls; ~$1.8/run) vs Sonnet's 82-86%. Haiku's cost is lower RECALL (acceptable per project values: missing edge recoverable, wrong edge = pollution), not extra pollution. **(2) Fix candidates first** — residual errors in BOTH samples were bad candidate SLUGS (a disambiguation miss that survives the existence-gate AND a merge-time orphan-filter), not model error → fixed before the bulk. **(3) Run = fresh all-Haiku** (single provenance; Sonnet partial `_events-run-20260527/` superseded). New collision classes (cat/wolf/duck/gold/others/dragon/bear) left for merge-time triage (mixed = real refs + a few wrong; some have missing nodes). **(4) Calibration:** precision reads judge EDGE CORRECTNESS as the bar; flag a quote only when it actively fails to support the type (not when merely less-direct).

**What's next:** Events Haiku bulk RUNNING in Matt's iTerm (`_events-haiku-bulk/`, 600s pacing, validate-every 25; ~411 batches, ~3.5 days; auto-resumes walls, hard-stops drift at exit 43). → `progress/continue-prompts/2026-05-27-events-haiku-bulk-monitor.md` (**Opus 4.7** — checkpoint precision reads + completion→merge). Owed: precision spot-read at first/25-batch checkpoint + at completion. Still gated on Matt: 3 core-cleanups (drop 2 cersei↔tyrion LOVES / ~22 ASSAULTS→ATTACKS / merge-time OWNS→BONDED_TO). Merge of Events edges into `graph/edges/edges.jsonl` = separate milestone.

### Session 76 — Events enrichment launched (Sonnet); flush-fix + rate-limit wall; ASSAULTS mis-type caught (2026-05-27)

**Model:** Opus 4.7 (orchestrator) + script-builder (Sonnet 4.6) ×2. **Detail:** `history/session-details/session-076.md`. **Commit:** uncommitted at endsession (Matt to confirm).

**Changes made (Step 1 precursors + Events run, all staging — `graph/edges/edges.jsonl` UNTOUCHED):**
- NEW `scripts/stage4-edge-temporal-scope.py` (+58 tests; 999 suite green): annotates all 3,811 edges with `(book_order, chapter_number)`; temporal-aware conflict re-audit → **`--window chapter`: 31/32 flagged pairs are temporal arcs, 1 true same-window** (`cersei↔tyrion`); `--window book`: 24/8. Outputs `working/wiki/data/edges-temporal-scoped.jsonl` + `graph-conflict-pairs-temporal.{md,jsonl}`.
- `scripts/stage4-tail-classifier.py` (+tests, **1011 green**): NEW `--flush-every N` (default 5; **cursor-based delta** flush — dodged the append-mode duplication trap) + SIGINT/SIGTERM flush handler → kill-to-tune is lossless + resumable. Rate-limit/end paths made cursor-safe.
- **Events run (Sonnet, `pass1_events`, 16,572 cands/415 batches):** 75 batches done → **369 typed / 2,631 rejected / 240 classify_failed; 273 unique; $20.81** in `working/wiki/pass2-buckets/pass1-derived/_events-run-20260527/` (gitignored). 5 accuracy checkpoints, **~82-86% strict, zero drift**; vocab lockdown correct even on MANIPULATES/ADVISES/CROWNS_QUEEN_OF_LOVE_AND_BEAUTY. Paused on a shared-account rate-limit wall (~75 batches/5h window; exit 42, partial flushed).
- NEW continue prompt `progress/continue-prompts/2026-05-27-haiku-events-comparison.md`.

**Decisions:** (1) Matt converted his S75 hard 75% gate to a **monitored iterative loop** ("run it, continue even if <75%, tune the prompt every couple batches"); precision held ~82-86% so no tuning was needed. (2) **Conflict-pair review:** only genuine mis-types = the **2 `cersei↔tyrion` LOVES** edges (sarcasm/accusation); `catelyn→tyrion`/`ghost↔tyrion` are real arcs (KEEP). (3) **ASSAULTS bug (Matt-caught):** `ASSAULTS`=sexual only (architecture.md:233); **~22/32 core ASSAULTS are physical → mis-typed, should be `ATTACKS`** (root cause: spine phrase→type map pre-dates the split). v5 Events prompt obeys it (emitted 0 ASSAULTS). (4) **Model for remaining ~82% UNDECIDED** — Sonnet ≈ 2 days of session-blocking 5h-bursts vs Haiku (lighter, untested on current setup) → Haiku comparison queued. (5) **Auto-resume miss:** bare classifier didn't sleep-and-relaunch overnight; use a sleep-until-reset wrapper next time.

**What's next:** → `progress/continue-prompts/2026-05-27-haiku-events-comparison.md` (**Opus 4.7** conductor; Haiku 4.5 worker-under-test) — same-rows Haiku-vs-Sonnet comparison to pick the model, then resume the remaining ~82% with a sleep-until-reset wrapper. **3 gated core-cleanups await Matt's before/after OK:** drop 2 `cersei↔tyrion` LOVES (3,811→3,809); retype ~22 physical `ASSAULTS`→`ATTACKS` (+ fix spine map); merge-time `OWNS→BONDED_TO` for direwolf/dragon targets. None modify `edges.jsonl` without sign-off. Broader track context: `progress/continue-prompts/2026-05-26-stage4-events-enrichment.md` (Step 1 DONE).

### Session 75 — Graph-exercise follow-ups: conflict-pair audit + graph-query tool; enrichment un-shelved (2026-05-26)

**Model:** Opus 4.7 (orchestrator) + script-builder (Sonnet 4.6) ×2 parallel. **Detail:** `history/session-details/session-075.md`. **Session-results:** `working/session-results/2026-05-26-graph-followups.md`. **Commit:** this endsession commit.

**Changes made (all $0/deterministic, no LLM):**
- NEW `scripts/graph-conflict-pairs.py` (+`tests/test_graph_conflict_pairs.py`, 29 green) — read-only audit; flags entity pairs with semantically incompatible co-occurring edge types into a REVIEW QUEUE (does NOT modify `edges.jsonl`). Output `working/wiki/data/graph-conflict-pairs.{md,jsonl}`. **1,978 pairs → 32 flagged** (14 same-direction / 11 opposite / 7 both; DISTRUSTS×TRUSTS 15, ALLIES_WITH×OPPOSES 12, LOVES×HATES 5, PROTECTS×ASSAULTS 3).
- EXTENDED `scripts/graph-query.py` — already existed from S39 (node-inspection over node `## Edges` + `cross-references.jsonl`); preserved all S39 modes, added `--neighbors`/`--path`/`--health`/`--edges` over canonical `edges.jsonl`. `tests/test_graph_query_edges.py` (29 green); full suite **920 green**, no regressions.
- `--health`: 8,299 node files · 3,811 edges · 898 endpoints · **0 orphans** · 105 edge types (GUEST_OF 404, OPPOSES 265, SERVES 255 lead); degree leaders jon-snow 317, tyrion 315, dany 248, cersei 229, arya 198.

**Decisions:** (1) **Enrichment UN-SHELVED** — Matt confirmed he DOES want enrichment; softens the S74 "NO-GO" to a *deferral*. Step by step, **Events is the next surface**, gated behind the precision changes landing first (the conflict-pair cleanup + kept v5 precision rules). Memory `project_enrichment_wanted_events_next`. (2) **Temporal flagging endorsed** ("when an edge applies — shrewd"). Verified it's largely DETERMINISTIC: all 3,811 edges carry `evidence_book`+`evidence_chapter`; chapter frontmatter has `chapter_number` → a `(book_order, chapter_number)` key is derivable at $0. The 32 conflicts are mostly *temporal arcs* (Dany→Jorah TRUSTS@AGOT+DISTRUSTS@ADWD), not errors → real fix is temporal scoping, not deletion. (3) `graph-query.py` collision surfaced before touching it (S74 prompt assumed the file didn't exist) → extended, not overwritten.

**What's next:** → `progress/continue-prompts/2026-05-26-stage4-events-enrichment.md` (**edge enrichment with Events**, precision-gated). Folds in the precision precursors: review/apply the 32-pair true mis-attributions + build deterministic temporal scoping + keep v5 rules; THEN a gated Events pass. NOT launched this session (Matt's call to end + queue). DO NOT run the ~$270 Events bulk blind (failed 75% gate).

### Session 74 — Locator grounding fix, enrichment NO-GO, core citations re-grounded, graph exercised (2026-05-26)

**Model:** Opus 4.7 + script-builder (Sonnet) + prose-edge-reviewer ×2. **Detail:** `history/session-details/session-074.md`. **Commit:** `63b8b461a`.

**Changes made:**
- `scripts/stage4-pass1-evidence-locator.py` — hint-anchored quote grounding (hint-verbatim→hint-fuzzy→both-named-window) + new `quote_source` field; **fixed `:11` line-number bug** (`read_chapter_prose` stripped blanks → `split_into_sentences` never saw paragraph breaks → all refs pinned to first prose line; fixed via gap-detection).
- `scripts/stage4-tail-classifier.py` — `quote_source`/`locate_quality` passthrough into all 4 output builders; **v5 precision rules** (`prompt_version=v5-precision-rules`, sha `d31ca56c4768`): R1 direction-lock, R2 evidence-supports-both-endpoints, R3 target-category, R4 state-not-moment, R5 temporal-phase, R6 no-analytical-from-moment.
- NEW `scripts/stage4-reground-core-citations.py` (+test) — re-grounded the SHIPPED core: **`graph/edges/edges.jsonl` 3,676/3,811 `evidence_ref` line numbers corrected** (quote text + edge set byte-identical, 3,811→3,811, safety-asserted; 9 left honestly unresolved). Edges are still v1.3 — same edges/types, citations now navigable.
- `.gitignore` — ignore regrounding backup/candidate (report tracked). 883 tests green.

**Decisions:** **Enrichment NO-GO → ship core-only.** Post-locator-fix out-of-sample smokes = **74.5% / 62.5%** strict (unstable, <75% gate; clear-case 83-89% but borderline over-emits sink it). The ~78% deterministic core is the better artifact than a ~70% LLM layer with no scheduled patcher (project value: a wrong cited edge is graph pollution). v5 rules authored + kept for any future revisit; v5 smokes killed mid-flight on Matt's "ship the core" call (~$0 extra). **Then discovered the committed core carried the SAME latent `:11` citation bug** (3,784/3,811) → re-grounded deterministically before declaring shipped.

**Graph exercised (the payoff):** nodes+edges+index **compose; 100% of 898 edge endpoints resolve to a node, 0 orphans, fully traversable.** Cersei/Tyrion query returned rich neighborhoods + 18 direct + 27 two-hop. Surfaced: mis-typed edges now *clickable* via the fixed citations (`cersei LOVES tyrion`=Varys-line; `tyrion LOVES cersei`=sarcasm; `ALLIES_WITH`=grudging submission); structural gap = **no temporal scoping → contradictory edges coexist** (LOVES+HATES same pair). Conflicting-type pairs concentrate the mis-types.

**What's next:** → `progress/continue-prompts/2026-05-26-graph-exercise-followups.md` (**Sonnet 4.6** builds; Opus review). (1) $0 **conflict-pair audit** — flag pairs with incompatible edge types as a precision-cleanup queue (attacks the ~22%). (2) Formalize the ad-hoc traversal into reusable `scripts/graph-query.py`. (3) Deferred: temporal/chapter scoping on edges; SIBLING_OF-class weak-evidence backfill. Spend: ~$2.5.

### Session 73 — Cleanup-and-reorg triage: worktrees removed, CLAUDE.md #9 finding, scripts KEPT (2026-05-26)

**Model:** Opus 4.7. **Detail:** `history/session-details/session-073.md`. **Commit:** this endsession commit.

**The session:** `/continue cleanup-and-reorg` — became a triage/decision session; most of the "reorg" dissolved on inspection.

**Changes made:**
- Removed both leftover worktrees (`.claude/worktrees/{admiring-benz-fa26f8, mystifying-burnell-56ee9c}`, clean) + deleted the 2 fully-merged `claude/*` branches (reversible). `.claude/worktrees/` empty.
- Fixed the stale "gitignored" claim in `progress/continue-prompts/2026-05-26-cleanup-and-reorg.md` (corrected to the tracked-files reality below).
- Scratch files untouched (Matt: "ignore scratch files"). Memory: `project_pass1_all_opus` (Pass 1 = all Opus, Matt-confirmed; not derivable from extraction files).

**Decisions:**
- **Scripts folderization DEFERRED indefinitely** — cosmetic, high-risk: `stage4-*`↔`wiki-pass2-*` cross-import via hardcoded `_REPO/"scripts"/"<name>"` paths (4 bridges), and `tests/_helpers.py:load_script` loads by flat filename (~30 call-sites). Nothing's broken; payoff is navigational only.
- **27 comention / wiki-prose-edge scripts KEPT (do NOT re-propose archiving)** — they implement the pre-S65 wiki-comention approach (**superseded, not dead**) + one-off per-house classifiers + Haiku-bulk apparatus; inert but a plausible **future recall lever** (~9% prose-only relationships, S68 recall-sample). The only driver for archiving was "cleanup" → not enough.
- **CLAUDE.md #9 finding:** the continue prompt said `pass2-buckets/` is gitignored. Reality = **23,081 TRACKED files**, incl. **7,180 stale `skeleton/*.node.md`** (~28 MB, S72-verified redundant with `graph/nodes/`). Only `pass1-derived/` is gitignored. **Skeleton-untrack DEFERRED to its own decision** (entangled — ~24 `wiki-pass2-*` promotion scripts read `skeleton/`).
- **Edge state confirmed for Matt:** 3,811 promoted (v1.3 frozen); 5,886 core candidates worked through; **27,305** extra-table candidates held at the ~$270 / ≥80%-precision spend gate (smokes ~62-66%). Strategy (deterministic spine to minimize Haiku work + validation stack + prompt hardening) confirmed correct.

**What's next:** → **edge enrichment gate-opener** = the $0 deterministic **locator quote-grounding fix** → ~$1.4 re-smoke; if ≥~75% across 2 fresh samples, enrichment unlocks, else ship core-only. Continue: `progress/continue-prompts/2026-05-25-stage4-locator-grounding.md` (**Sonnet 4.6** build/smoke; Opus review only). **NOTE both stage4 continue prompts say edges=3,842 — STALE; it's 3,811 v1.3 after S72.** Downstream framework: `2026-05-25-stage4-enrichment-decision.md` (A/B/C). Deferred levers: skeleton-untrack; S67 resolver recall levers (`2026-05-23-stage4-pass1-finishing.md`).

---

> Session 72 archived to `history/worklog-archives/archive015.md` (archive015 now full at 5/5)
> Session 71 archived to `history/worklog-archives/archive015.md` (archive015 now 4/5)
> Session 70 archived to `history/worklog-archives/archive015.md` (archive015 now 3/5)
> Session 69 archived to `history/worklog-archives/archive015.md` (archive015 now 2/5)
> Session 68 archived to `history/worklog-archives/archive015.md`
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
