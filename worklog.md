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
This is your project memory. When you come back after a break, **STATUS — at a glance** (top of Current State) is the single "where am I" surface: what's shipped, what's in flight, what's gated on what, what you review next. The checklists below it and the last few Session Log entries carry the detail. Add ideas to the backlog whenever they occur to you, even outside of Claude Code sessions.

---

## Current State

### STATUS — at a glance (verified 2026-06-12)

**SHIPPED**
- Pass 1 mechanical extraction: **344/344 chapters, all 5 books** (done 2026-05-06, all Opus)
- Wiki cache local (17,945 fetched → 17,657 unique files) + Pass 2 promotion: **graph/nodes/ = 8,263** (events 583; excl. `_conflicts/` staging)
- Entity + chapter indexes: **all 21 categories** (S72)
- Edge layer LIVE: **`graph/edges/edges.jsonl` = 4,760 cited edges** (deterministic core v1.3 → Plate 5 reification S87 → S91 renames + 3 deception pilots). Node connectivity **14.7%**.
- S92 Fable audit: doc truth-pass, project-story 8 chapters, infobox-merge spec v2 + script + **dry-run complete** (`working/infobox-merge/dry-run-report-2026-06-12.md`). Expected post-merge: edges 21,766 / connectivity 71.0%.

**IN FLIGHT**
- (none — S92 audit session complete)

**NEXT TRACK (Matt-greenlit 2026-06-11)**
- **Infobox-structural wiki merge**: dry-run DONE, awaiting Matt review + 11 open-question answers → ship. → `progress/continue-prompts/2026-06-12-infobox-merge-ship.md`
- **THEN Mode 3 grounded-agent dip** on the merged graph (`progress/continue-prompts/2026-06-11-phase2-mode3-dip.md`)

**GATED / QUEUED**
- 2 structural restructures (Wyman-execution, Jaime-sheathes) — Matt ratification (`progress/continue-prompts/2026-06-12-deferred-structural-restructures.md`)
- Design-doc consolidation build (~3-4 sessions) — GATED on Matt's Option A/B/C pick
- Nomenclature sweep — GATED on Matt's scheme pick
- Repo-reorg P1/P2 (~1-1.5 sessions) — per `working/repo-reorg-plan-2026-06-12.md`
- Backfill Tracks A/B/C (~$25–75) — gated on what the Mode 3 dip reveals
- Events-Haiku 1,617 typed rows + Dialogue tail — SHELVED (absorbed into backfill Track B)
- Spoiler gating (`first_available`) — DEFERRED post-first-release; prose-comention wiki edges — DEPRECATED, stays dead

**MATT REVIEWS NEXT:** `working/infobox-merge/dry-run-report-2026-06-12.md` (incl. 11 YOUR-DECISIONS items + 2 semantic-remap flags) → S91 look-at-twice items (Session 91 entry) → restructure decision packets

### Infrastructure (all shipped)
- [x] Repo scaffold: directory structure, CLAUDE.md, reference files (`architecture.md`, `foreshadowing-events.md`, `pov-characters.md`), slash commands, working/ + progress/ conventions
- [x] Chapter splitter (`scripts/chapter-splitter.py`) — all 5 books split (344 chapters: AGOT 73, ACOK 70, ASOS 82, AFFC 46, ADWD 73) + 3 D&E novellas; TWOIAF OCR'd to plaintext (179K words)
- [x] Full wiki crawl executed once: 17,945/17,952 pages fetched → 17,657 unique JSON files on disk (case-collision/redirect overwrites account for the delta), 377 MB; Playwright scraper retired to `scripts/archive/`
- [x] Subagent definitions in `.claude/agents/` — 28 agents as of 2026-06-11 (fleet expansion S26; inventory in `reference/agents.md`)

### Extraction Pipeline
- [x] Pass 1 (mechanical) — **COMPLETE, all 5 books, 344/344 chapters (2026-05-06), v3 prompt (12-category Raw Entity List), all Opus.** v1/v2 runs archived under `extractions/archives/`; prompt-version history in `history/worklog-archives/`.
- [ ] Pass 1 on Tales of Dunk and Egg (THK, TSS, TMK) — **deferred (enrichment pass for main-arc nodes)**. Not on the critical path; not dropped. Decision 2026-05-06 (Session 37 Q11=b).
- [x] Wiki infobox parser (Track B) — `scripts/wiki-infobox-parser.py` → `working/wiki/data/{infobox-data.jsonl (5,279 pages / 20,614 relationship rows), page-index.jsonl (17,657), parse-stats.md}`. **This layer is the source for the 2026-06-11 greenlit infobox merge.** Open parser issues: `books` field undercount (matters only for the deferred `first_available` backfill); unmapped fields (`dynasty`, `vassal`, `cadet branch`…) worth edge-taxonomy review at merge time. (The `categories[]` gap was fixed by the Path B backfill, S28.)
- [x] Pass 2 wiki ingestion — **COMPLETE (prompt written S19; ran S22–S29).** Stage 1 core: 855 agent-promoted nodes ($95.33). Stages 3/3c/Path B: ~7,000+ deterministic Python promotions ($0); `unknown` pages 70.4% → ~7%; 9 new entity types + dirs bootstrapped. Cumulative `graph/nodes/` ≈ 8,263. Canonical pipeline: `working/runbooks/wiki-pass2-pipeline.md`. Per-stage detail: `history/worklog-archives/archive005-006.md`. Chronology side-product: 2,245 events in `working/wiki/data/chronology-events.jsonl` (not graph edges yet).
- [x] Stage 4 prose-edge pipeline (Pass-1-derived) — **SHIPPED; this produced the canonical edge core.** S65 pivot to Pass-1-derived deterministic pipeline (wiki-comention DEPRECATED); S66–S69 built spine + LLM tail + extra-tables recall (5,219 book-pass1 edges + 32,194 untyped candidate rows staged); formalized into `graph/edges/edges.jsonl` S70–S74 (see Index & Graph below). Build detail: `history/worklog-archives/archive014-015.md` + `progress/continue-prompts/2026-05-25-stage4-smoke-fixes-and-formalize.md`. Untyped Events/Info/Food/Dialogue candidate pools remain staged (Events ran S80 → shelved; rest queued behind Mode-3-dip findings).
- [ ] Pass 3 voice/perception agent prompt written
- [ ] Pass 4 foreshadowing agent prompt written
- [ ] Pass 5 theory-informed agent prompt written
- [ ] Pass 6 discovery agent prompt written

### Index & Graph
- [ ] Trigger table v1
- [x] Entity index — **REBUILT to all 21 categories (Session 72).** `graph/index/` previously covered only characters/houses/locations/artifacts/chapters; `scripts/build-entity-indexes.py` extended with 14 more `TYPE_CONFIGS` → **+1,847 new `*.index.json`** at the S72 rebuild (todos.md cites +1,861 for the same rebuild — a ±14 counting discrepancy never reconciled; one S72 event either way, not two rebuilds; index now totals ~7,850 files across 21 category dirs). This was the real "entities aren't there" gap (the nodes always existed; the index didn't cover them).
- [x] Chapter index (per-chapter `*.mentions.json` under `graph/index/chapters/`)
- [x] Graph edges formalized + SHIPPED — **v1.3 core = 3,811 cited Pass-1-derived edges, ~78% strict precision, 0 orphans** (v1 3,842 → v1.2 type-contract revalidation S72 → v1.3 title-person resolver pass; citations re-grounded S74 fixing the latent `:11` locator bug; commit `63b8b461a`). Haiku Events+Dialogue enrichment NO-GO'd at the 75% gate and shelved (S74). Decision detail: Active Decisions S72/S74 entries below + `history/worklog-archives/archive015-016.md`.
- [x] Graph query + audit tooling — **NEW (Session 75; extended S89 overnight).** `scripts/graph-query.py` (S39 node-inspection EXTENDED with `--neighbors`/`--path`/`--health`/`--edges` over canonical `edges.jsonl`; S89 added `--event-participants <hub>` beat-union primitive) + NEW `scripts/graph-conflict-pairs.py` (read-only precision-cleanup review queue → `working/wiki/data/graph-conflict-pairs.{md,jsonl}`; 32 flagged pairs, mostly temporal arcs). + S89: `scripts/event_alias_resolver.py` + `working/wiki/data/event-alias-lookup.json` (876 phrases at build; 922 after the S91 rebuild, 1 pre-existing collision). 920 tests green. `--health` confirms 0 orphans / 100% traversable.
- [x] Edge temporal-scoping — **NEW (Session 76).** `scripts/stage4-edge-temporal-scope.py` (+58 tests) annotates all 3,811 edges with `(book_order, chapter_number)` + temporal-aware conflict re-audit → **31/32 flagged pairs are temporal arcs** (`--window chapter`), 1 true same-window (`cersei↔tyrion`). Read-only on `edges.jsonl`. Outputs `working/wiki/data/edges-temporal-scoped.jsonl` + `graph-conflict-pairs-temporal.{md,jsonl}`.
- [x] Edge-modeling reification (Plate sequence, S82-S87) — **ALL PLATES SHIPPED including Plate 5 (2026-06-09, S87).** `graph/edges/edges.jsonl` **3,811 → 4,757 (+946)**; `graph/nodes/events/` **371 → 583 (+212)**; `graph/nodes/_conflicts/` **+6** (1 aerys + 5 collision losers). Backup: `graph/edges/_regrounding/edges-pre-reification-2026-06-09.jsonl`. Phases: Plate 0 normalizer 10 flips + 3 aerys repoints; Plate 2.5 27 wiki schema retypes + 12 drift retypes + 4 high-conf collision merges; Plate 4 51 SUB_BEAT_OF + 2 DUPLICATE_OF (1 skipped — meta.chapter target); Plate 3 217 mints (`title:`→`name:` rewrite) + 897 role edges + 55 supersede stamps; S77 carryover 2 LOVES drops + 21 ASSAULTS→ATTACKS retypes. Validators: 4,725 kept / 32 dropped (all SUB_BEAT_OF empty-evidence — read-only audit, rows remain). Red Wedding smoke test ✓ (8 SUB_BEAT_OF, 2-hop participant traversal works). Followups: display-bullet regen, 32 SUB_BEAT_OF empty-quote backfill, 109 hub-review-queue triage, post-Plate-5 tracks A/B/C ($25-75). Diff doc: `working/edge-modeling/plate5-merge-diff.md`. Script: `scripts/plate5-merge.py`.
- [x] Post-Plate-5 graph validation + rename batch (S89-S91) — Mode 1 probes done, 9 event-node renames + alias work applied, **3 curator deception-pilot edges minted → `edges.jsonl` = 4,760 (current canonical count)**. 2 structural restructures deferred to `progress/continue-prompts/2026-06-12-deferred-structural-restructures.md`. See Session Log S89-S91.

  *(Pre-Plate-5 design/staging history — Plates 0+1+2+2.5, D2/D8 decisions, vocab 163→165, Contract 10, audit loop, alignment audits — lives in `history/session-details/session-082.md`–`session-085.md`, `history/worklog-archives/archive017-018.md`, and `working/edge-modeling/SESSION-LOG.md` + `edge-modeling-reification-design.md`. The former HISTORICAL [~] entry here was collapsed 2026-06-11; nothing in it was unique to this file.)*
- [~] Events edge enrichment (Events-Haiku bulk, S78-S81) — **SHELVED 2026-06-11.** Bulk run completed S80 (16,502 candidates → 1,617 typed + 14,884 rejected at `_events-haiku-bulk/`, ~$50, 0 conform_violations) but the S81 drift audit returned **NO-GO (borderline)** — triple 48%/pair 56% vs 70%/85% gates; fresh-eyes review adjusted to ≈56-70%, still at/below gate. **NOT merged into `edges.jsonl`.** The escalation pick is now absorbed into post-Plate-5 backfill Track B + Mode-3-dip sequencing (no standalone pick pending). Full detail: `working/audits/events-haiku-bulk-2026-05-29/{analysis.md,cross-model-audit.md}`, runbook `working/runbooks/stage4-events-haiku-bulk.md`, promotion chain `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/`, S78-S81 narratives in `history/worklog-archives/archive017.md`. Known loose ends carried in todos: `classify_failed` skip-key parse-fail block; rejected rows lack `reject_reason` (Dialogue prep).
- [ ] Convergence maps

### Reference Materials
- [x] Foreshadowing events list (`reference/foreshadowing-events.md`)
- [ ] Theory seeds file
- [ ] Taxonomy reference doc
- [x] Architecture spec (original outline exists, needs refinement)

---

## Active Decisions

> Design questions that need resolution. Tag with status: OPEN, DECIDED, DEFERRED.

### DECIDED: Infobox-structural wiki edges greenlit for merge (2026-06-11, Fable audit)
- **Decision (Matt, `working/reply-to-audit-session-2026-06-11.md`):** merge the wiki infobox-structural layer (~20,614 parsed relationship rows in `working/wiki/data/infobox-data.jsonl`) into `graph/edges/` as deterministic edges — **Tier 2 maximum, never Tier 1** (Tier 1 stays earned-by-book-quote), `evidence_kind: wiki-infobox`, `typed_by: python-infobox-map`, cite `wiki:<Page>`. ~18-19k edges expected after filtering multi-value speculative fields (Jon's two listed mothers) and Unknown/None/Extinct targets; folds in 2 hygiene fixes (115 orphan endpoint slugs, 948 role edges missing `typed_by`/file:line). Moves node connectivity 14.7% → ~72%.
- **Sequence:** spec → dry-run → Matt review → ship. **Mode 3 grounded-agent dip runs AFTER the merge**, on the merged graph; its failures drive backfill Tracks A/B/C priorities.
- **Prose-comention wiki edges stay DEPRECATED** (all three layer verdicts in `working/audits/fable-audit-2026-06-11/synthesis.md`).

### OPEN: Events Haiku bulk — drift audit returned NO-GO (borderline); chain halted at step 1, awaiting Matt's escalation pick (2026-06-01, Session 81)
- **STATUS 2026-06-11:** no standalone escalation pick pending anymore — the 1,617-row artifact is absorbed into post-Plate-5 backfill **Track B** + Mode-3-dip sequencing (revisited only if the dip proves a gap it would fill). Entry kept as the decision record.
- **Bulk artifact is complete and clean** (S80): 1,617 typed edges + 14,884 rejected over 16,502 candidates at `_events-haiku-bulk/`; single prompt_sha `d31ca56c4768`, all `typed_by=haiku`, 0 conform_violations.
- **BUT step 1 drift audit (S81) returned NO-GO** — triple-level 48 % (gate 70 %), pair-level 56 % (gate 85 %); 22/50 sampled Haiku emits rejected by Sonnet judge. Failure concentrates in structural-edge types: TRAVELS_TO 17 %, TRAVELS_WITH 0 %, LOCATED_AT 20 % triple agreement.
- **Fresh-eyes pressure-test (S81) corrected the framing:** ~11 of 22 REJECTs are clear Haiku drift (Rule 4a hint-as-evidence, V5-R2 quote-doesn't-support, Rule 12 co-presence); ~3-4 are confirmed Sonnet over-rejections (judge_idx 2/6/14/16); ~7-8 ambiguous. Adjusted triple ≈ 56-70 % — at or below the gate. **No-Go stands but is borderline, not catastrophic.** The S69 vs S77 smoke-session contradiction was a misciting + a measurement-shape mismatch (S77 measured hand-read precision on fresh candidates, NOT Sonnet-judges-Haiku-emit on stratified emits) — both can be true.
- **The 3 chain-startup decisions Matt made up front still hold IF a path leads to promotion:** (1) full re-merge, not additive overlay; (2) ship Events-only as v2.0 now, Dialogue v2.1 separate; (3) `reject_reason` schema fix deferred to Dialogue prep.
- **Pick required (5 escalation paths, full discussion in `cross-model-audit.md §6` + `2026-06-01-events-bulk-escalation-pick.md`):** (A) re-run bulk on Sonnet ~$340; (B) promote long-tail-only; (C) Sonnet-filter the named-type rows only ~$2-5 (audit's recommendation); (D) tighten Haiku to v6 + re-run; (E) abandon Events for v2.0; wait for Dialogue.
- **Known loose end carried forward:** the `classify_failed`-not-a-skip-key parse-fail block from S79 still pending. Non-blocking for the escalation pick.
- **Reports:** `working/audits/events-haiku-bulk-2026-05-29/analysis.md` (S80 bulk analysis) + `cross-model-audit.md` (S81 drift audit).

### OPEN: 3 gated core-cleanups — still await Matt's before/after sign-off (carried from Session 76)
- **STATUS 2026-06-11: RESOLVED — all 3 cleanups were applied at Plate 5 (S87):** 2 cersei↔tyrion LOVES drops, 21 ASSAULTS→ATTACKS retypes (11 stay — sexual-violence canon), OWNS→BONDED_TO no-op (0 rows). Entry kept as the decision record.
- Model decision RESOLVED (→ Haiku, see above). Still pending Matt's OK (do NOT touch `edges.jsonl` without before/after sign-off):
- **3 gated core-cleanups — await Matt's before/after sign-off (do NOT touch `edges.jsonl` without it):** (1) drop the 2 `cersei↔tyrion` LOVES mis-types (3,811→3,809); (2) retype the ~22 physical `ASSAULTS`→`ATTACKS` (`ASSAULTS`=sexual only per architecture.md:233; fix the spine phrase→type map too); (3) merge-time `OWNS→BONDED_TO` for direwolf/dragon targets (Events output, not core). The Events v5 prompt already obeys the ASSAULTS rule (emitted 0).
- **Operational:** long unattended runs MUST use a sleep-until-reset auto-resume wrapper — S76's bare worker sat idle all night after one cap wall.

### AMENDED: Enrichment is DEFERRED, not abandoned — Events is the next surface (2026-05-26, Session 75)
- **STATUS 2026-06-11:** the Events bulk subsequently ran (S80) and was NO-GO'd (S81, see above); enrichment now sequences as **infobox merge → Mode 3 dip → dip-driven backfill** per the 2026-06-11 DECIDED entry.
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
- **STATUS 2026-06-11:** built and SHIPPED — this pipeline produced the canonical `edges.jsonl` core (v1→v1.3, S66-S74). Entry kept as the pivot record.

### OPEN: Storage Format — Pure Markdown vs. Graph DB
- **STATUS 2026-06-11:** de facto settled on the lean — markdown nodes + `edges.jsonl` + `scripts/graph-query.py` (0 orphans, fully traversable); no graph-DB need has emerged. Formally still open if query complexity grows.
- **Question:** Does the graph live as pure markdown files with edges represented as YAML/frontmatter references, or do we use a lightweight graph DB (Neo4j, SQLite with graph extensions)?
- **Leaning:** Start with pure markdown. The context base pattern works well for agentic access. Graph DB can come later if query complexity demands it.
- **Trade-off:** Markdown is portable, version-controlled, and readable by Claude Code natively. Graph DB gives real traversal queries but adds infrastructure.

### DECIDED: Wiki Ingestion Scope — Full Crawl, Then Triage
- **Decision (2026-04-13):** Scrape the entire AWOIAF wiki once (~17,952 pages, ~5–6 hrs, ~1–2 GB), store as a *reference layer* in `sources/wiki/` (gitignored). Pass 2 (wiki-ingester) decides what gets promoted into `graph/nodes/` with proper `first_available` spoiler tags.
- **Rationale:** Targeted scraping required us to predict relevance up front. Full crawl is a one-time cost (~5 hrs, ~1.5 GB) and lets us refine classification rules against a static cache for free. Cache + resume means the crawl is interruption-tolerant. The graph is still curated — only the *source layer* is exhaustive.
- **Open downstream question:** How does Pass 2 decide what to promote? Likely a combination of (a) categories the page belongs to, (b) whether the page subject appears in any chapter extraction, (c) page length / infobox richness as a quality signal. To be designed when Pass 2 prompt is written.
- **STATUS 2026-06-11:** answered in practice — Pass 2 ran to completion S22-S29 (tier rules + category promotion; ~8.3k nodes). Entry kept as the scope-decision record.

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

> Groomed 2026-06-11: shipped items pruned (chapter splitter, Pass 1 AGOT PoC, Pass 2 prompt, node-file schema — all long done); survivors reframed to current reality.

### HIGH
- [ ] Create theory seeds file (top 20-30 theories with confidence tiers) — prerequisite for Pass 5 AND for connecting the all-dark `theories/` layer (45 nodes, ~0 real edges; the infobox merge contributes nothing there — see synthesis 2026-06-11)

### MEDIUM
- [ ] Design the trigger table schema (what columns, what routing logic) — the one unshipped piece of the index layer
- [ ] Write Pass 3 voice analysis prompt — cross-POV perception dimension; feeds the talk-to-a-character goal
- [ ] Write Pass 4 foreshadowing prompt — agent receives `reference/foreshadowing-events.md` and scans chapter extractions for matches
- [ ] Build convergence map for Oldtown as proof of concept (`graph/convergence-maps/` still empty)
- [ ] Prophecy node layer is undercounted (2 nodes, 0 edges) — mint the canon prophecies (Azor Ahai, valonqar, dragon-has-three-heads…) from existing wiki pages

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

### Session 92 — Fable audit execution: doc truth-pass, project story, infobox merge spec→script→dry-run (2026-06-11 → 2026-06-12)

**Model:** Fable 5 orchestrator; ~40 subagents (Fable for judgment/prose, Sonnet for mechanical/scripts; EVERY major deliverable reviewed by a fresh-eyes critic, all findings applied). **Spend:** hit the monthly extra-usage cap twice mid-session; resumed across plan windows; zero lost/broken work (verified). **Detail:** `history/session-details/session-092.md` (full narrative incl. wall postmortem + critic-loop catches). **Commit:** this endsession commit.
- **Closeout additions (2026-06-12):** dry-run report rewritten self-explaining at Matt's request (preamble + TL;DR + 13-term glossary incl. `direction_corrected` + fill-in answer lines on all 11 decisions; 275→594 lines); NEW `progress/continue-prompts/2026-06-12-graph-cleanup.md` (double-gated: merge shipped + Matt's curation marks; executes FIX-22 + small followups + the 3 missing Red Wedding SUB_BEAT_OF links); **Olenna verified BOOK-derived** (Pass 1 ASOS Sansa chains, not wiki/show — inference + Littlefinger testimony) → cleanup prompt pins `olenna AGENT_IN death-of-joffrey-baratheon` at Tier 2, never Tier 1; new memory rule: sequential/2-3-batch subagent dispatch when quota headroom low.

- First Fable session. Commissioned by Matt's audit ask + reply file (`working/reply-to-audit-session-2026-06-11.md`). Full 91-session history audit + graph deep-dive persisted to `working/audits/fable-audit-2026-06-11/` (synthesis, history-audit, graph-deep-dive, doc-rot punch list, worth-assessment v2, design-doc proposal, SESSION-CHECKPOINT).
- **DECIDED (Matt 2026-06-11):** infobox-structural wiki layer (20,614 parsed rows, 98.4% additive) greenlit for merge — Tier 2 max, `evidence_kind: wiki-infobox`; prose-comention stays deprecated; Mode 3 dip runs AFTER the merge.
- Doc truth-pass: CLAUDE.md pipeline table fixed; worklog rebuilt around the new STATUS block; Principles #4 corrected; todos.md 420→232 (resolved blocks → `history/todo-archives/`); `progress/continue-prompts/README.md` manifest; `reference/schema-legend.md`; `reference/roadmap.md`; nomenclature reform proposal (Matt picks); design-doc structure proposal (Option A recommended, Matt picks).
- Human-readable layer: `history/project-story/` (8 chapters incl. the reification explainer with a live Red Wedding walkthrough); history/ READMEs; `scripts/README.md` (146 scripts inventoried, 6 LEGACY wrappers); `weirwood run` subcommand banked on longrun.sh (tested, shellcheck-clean).
- **INFOBOX MERGE TRACK:** spec v2 (adversarial critic CONFIRMED the FIELD_EDGE_MAP direction-inversion on 10 fields; fact-key quarantine closes the Joffrey-mirror leak) → `scripts/infobox-merge.py` + 75 tests → **dry-run reproduces spec v2 EXACTLY** (20,614 → 17,006 merged / 1,128 filtered / 1,037 quarantined / 1,356 deduped / 87 corroborations; edges.jsonl would go 4,760 → 21,766; connectivity 14.7% → 71.0%). NO graph writes this session. Report: `working/infobox-merge/dry-run-report-2026-06-12.md` (11 decided-by-default open questions for Matt).
- Curation proposals: `curation/hub-review-triage-2026-06-12.md` (FIX 22 / QUARANTINE 10 / KEEP 81 — incl. live Plate-5 leak F1c and the Purple-Wedding tier-1 false-confession edge) + `curation/plate5-small-followups-2026-06-12.md` (2 collision proposals; donal-noye↔mag reverse edge; 32-empty-quote memo, rec = Contract-6 exemption; display-bullet regen, rec = defer until post-merge).
- **Graph defects newly surfaced (NOT fixed — no graph writes):** F1c dangling edge (`siege-of-storm-s-end-recalled` source never minted); 3 Red Wedding beats with role edges but no SUB_BEAT_OF link (Dacey Mormont's death missing from beat-union); `robb-is-killed SUB_BEAT_OF red-wedding` carries a wiki display-bullet as its quote; `donal-noye KILLS mag` quote mismatch; LOCATED_AT direction contradicts the design glossary (live data is event→location).
- Pre-existing test failures noted (predate session): `test_vocab_count_is_163` ×2 (vocab is now 166) + `test_cwd_is_tmp`.
- **What's next (the chain):** (1) Matt marks the dry-run report's 11 decisions → `progress/continue-prompts/2026-06-12-infobox-merge-ship.md` (Sonnet); (2) Matt marks the 2 curation files → `progress/continue-prompts/2026-06-12-graph-cleanup.md` (Sonnet; gated on merge shipped); (3) Mode 3 dip (`2026-06-11-phase2-mode3-dip.md`, Opus; gated on merge). Parallel-safe anytime: `2026-06-12-deferred-structural-restructures.md` (Opus). Matt's picks (non-blocking): design-doc Option A/B/C, nomenclature scheme, archive018 S86-append judgment, repo-reorg P1/P2 (`working/repo-reorg-plan-2026-06-12.md`). All session files KEPT in place per Matt ("until we are well and truly done").

> Session 87 archived to `history/worklog-archives/archive019.md` (archive019 started — 1/5)

### Session 91 — Rename execution batch + DECEIVES pilot edges + structural restructures queued (2026-06-11)

**Model:** Opus 4.7 (orchestrator + applied 9 renames + minted 3 pilot edges; 9 background sub-agents delegated for rename analysis / source verification / deception-feasibility). **Detail:** none (execution-heavy; subagent decision packets reproduced into the deferred-restructures continue prompt). **Commit:** this endsession commit.

**Changes made:**
- `graph/nodes/events/` — 9 file renames + 11 files patched (H1, mint-prose, inline-form aliases): Sand Snakes, Slynt, Dontos, Symon, Kerwin, cersei→execution-of-the-blackwater-deserters, qhorin→jon-spares-ygritte, cersei→cersei-s-plot-to-assassinate-jon-snow, wyman→wyman-publicly-arrests-davos-at-white-harbor; plus aliases-only on `ned-orders-janos-slynt-to-arrest-cersei` + sibling `gold-cloaks-betray-ned` (subagent KEEP rec).
- `graph/edges/edges.jsonl` — atomic field updates across 33 rows + 3 manual `plate5_superseded_note` free-text patches (Bug 3 — Slynt, Symon, Qhorin) + **3 curator pilot edges appended**. Count: **4,757 → 4,760**.
- 3 pilot edges: BETRAYS janos-slynt→eddard-stark (accepts-bribe-then-defects, AGOT Eddard XIV); DECEIVES cersei-lannister→jon-snow (contract-assassination, AFFC Cersei IV); DECEIVES wyman-manderly→house-frey (staged-arrest, ADWD Davos IV). Tagged `candidate_kind=curator-s91-deception-pilot`, `typed_by=curator-s91`.
- `graph/index/events/` — rebuilt via `scripts/build-entity-indexes.py --type events --all`.
- `working/wiki/data/event-alias-lookup.json` — rebuilt: 876 → 922 phrases, 1 pre-existing ambiguous collision (`conquest-of-dorne` duplicate node, NOT introduced by S91).
- CREATE `working/session-results/2026-06-11-rename-execution.md` + `progress/continue-prompts/2026-06-12-deferred-structural-restructures.md`. DELETE `progress/continue-prompts/2026-06-11-execute-rename-decisions.md` (task complete).
- `working/todos.md` — closed POST-PLATE-5 followup #10.

**Decisions:** 9 renames applied + 1 aliases-only treatment per the 9 subagent decision packets (5 ambiguous-flagged subagents launched mid-session per Matt's "use fresh sub agents for open questions"). 2 structural restructures **deferred** (Wyman-execution arc + Jaime-sheathes arc) — bigger than rename: new parent events + SUB_BEAT_OF restructure + multi-edge mints + type-field decisions; subagent decision packets reproduced verbatim into the continue prompt for Matt's ratification. Side-asks verified inline: Tyrion ordered Symon (Bronn=agent, ASOS Tyrion IV); Kerwin source backed up (ADWD Iron Suitor + wiki); WIELDS longclaw→Slynt-execution edge already existed. Deception-edges feasibility: `DECEIVES` (11 live) + `BETRAYS` (38 live) already in locked vocab — zero schema cost — pilot 3 edges now, queue scripted surfacer for ~30-50 medium-confidence retypes.

**Verification:** 10/10 alias-chain probes HIT; `--neighbors` confirms full role-edge sets attached on all 9 renamed slugs; `--health` clean; final `grep -r '<old-slug>' graph/` returns only deliberate old-slug-as-alias backrefs. Bug 1 (inline-form aliases only) + Bug 3 (body-text + plate5_superseded_note manual patches) workarounds held per rename. Mid-session surprise: alias resolver doesn't auto-convert kebab→spaces; Wyman + Qhorin aliases re-spelled in space-form.

**Look-at-twice items for Matt:** (a) `jon-spares-ygritte` typed `event.execution` (execution doesn't happen); (b) `cersei-s-plot-to-assassinate-jon-snow` typed `event.death` (Jon doesn't die); (c) `execution-of-the-blackwater-deserters` missing VICTIM_IN edge; (d) stale `status: minted-plate3` + "Staging only" body notes on all renamed nodes (Plate 5 merged but script doesn't flip status); (e) pre-existing `conquest-of-dorne` duplicate; (f) `cersei-claims-ned-s-men-attacked-first` flagged as DECEIVES candidate by 2 independent subagents (not minted — not being renamed).

**What's next:**
- → `progress/continue-prompts/2026-06-12-deferred-structural-restructures.md` (**Opus 4.7**) — apply Wyman-execution + Jaime-sheathes restructures per the verbatim subagent decision packets in-prompt. Open questions enumerated for Matt's ratification.
- → `progress/continue-prompts/2026-06-11-phase2-mode3-dip.md` (**Opus 4.7**) — Phase 2 Mode 3 grounded-agent dip. Unblocked. Can run before OR after restructures (parallel-safe).
- Backlog (deception-edges scaling): 3 pilot edges done, 7 to go per subagent C rec; then build `scripts/surface-deception-candidates.py` to mine the broader 30-50 retypes from `hint_raw` markers.

> Session 86 archived to `history/worklog-archives/archive018.md` (archive018 now full at 5/5)

### Session 90 — S89 overnight review + primary rename applied + remaining rename decisions queued for Opus (2026-06-11)

**Model:** Opus 4.7 (orchestrator + applied the primary rename). **Detail:** none (review + small apply + handoff session). **Commit:** this endsession commit.

**What this session was:** post-overnight review of Phase 1 results from S89 + first real apply against the renamed-rebuilt graph. Matt read the 3 overnight result files, did slug-vs-victim disambiguation explainers (Ned/Eddard alias chain, "what's a hit", S89 probe count semantics, chapter→graph→dialog query chain). Then applied the **primary** rename himself (`joffrey-orders-execution` → `execution-of-eddard-stark`) — touched 7 artifacts (1 node move + 6 edge rows). Surfaced 2 #8-deliverable bugs + a #10-script gap during apply (postmortem in todos.md #10).

**Bugs found during primary apply (2026-06-11):**
1. **`event_alias_resolver.py` (Agent #8) parser bug:** only parses inline `aliases: [...]` YAML form; block-style YAML list (`aliases:\n  - "..."`) silently corrupts to a single key. Harden the parser OR enforce inline convention as the canonical form. Matt used inline form for the apply.
2. **Agent #8's "auto-resolve on rebuild" prediction was wrong:** "Ned's execution" did NOT auto-resolve from the new slug `execution-of-eddard-stark`. It needs an explicit `aliases:` frontmatter entry — which Matt added (`aliases: ["Ned's execution"]`). Lesson: the deterministic resolver is phrase-lookup only; no semantic substitution; reader-natural phrasings must be enumerated.
3. **`rename-event-node.py` (Agent #10) coverage gap:** script rewrites frontmatter + slug-form refs in JSONL/JSON/MD files, but does NOT touch (a) the renamed node's own H1 + mint-prose body text, (b) free-text `plate5_superseded_note` fields in edge rows. Matt fixed both manually post-apply. Extend the script before any batch run.

**Verification post-primary-apply:** 0 residual old-slug refs in `graph/`; `edges.jsonl` row count unchanged at 4,757; `--health` 0 new orphans; new node's 5 edges traverse; both "Ned's execution" and "execution of eddard stark" resolve to the new slug; old action phrase is dead.

**Documentation polish:** added a plain-English preamble + TL;DR + "Your decisions" scannable table to `working/session-results/2026-06-10-overnight-rename-dryrun.md` so it's not a wall of agent output. Matt filled in his per-slug yes/no/different-suggestion decisions in that same file's "Your decisions" table — for the **5 secondary clean** candidates + **9 flagged** candidates. Those remain queued.

**No further graph writes this session beyond the primary.** `edges.jsonl` 4,757; `events/` 583. The remaining ~14 rename decisions are queued for a fresh Opus session via the new continue prompt.

**What's next:**
- → `progress/continue-prompts/2026-06-11-execute-rename-decisions.md` (**Opus 4.7**) — fresh Opus reads Matt's filled-in decisions, runs per-slug dry-run-then-apply, adds curated `aliases:` (inline form only — bug #1), patches body H1 + mint-prose + plate5_superseded_note free-text per rename (bug #3), rebuilds events index + event-alias-resolver at the end, verifies alias-chain works. Hardening of bug #1 and bug #3 in-script is OPTIONAL upgrade — work-around pattern documented in the continue prompt.
- → `progress/continue-prompts/2026-06-11-phase2-mode3-dip.md` (**Opus 4.7**) — Mode 3 grounded-agent dip. **After** remaining renames land.

### Session 89 — Mode 1 graph-validation probes complete + Phase 1 overnight kickoff (2026-06-10)

**Model:** Opus 4.7 (orchestrator + probe interpretation). 3 `script-builder` agents launched in background at end-of-session for overnight autonomous work. **Detail:** none — full narrative in `working/session-results/2026-06-09-graph-validation.md`. **Commit:** this endsession commit.

**Probes 5-8 finished:** (5) historical-events dark zone CONFIRMED — 8/10 anchors have 0 edges; 5 exist as nodes but isolated; `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` fires exactly 1× (Rhaegar→Lyanna from AGOT Eddard XV — Pass-1 caught the dyadic act but didn't attach it to the `tourney-at-harrenhal` hub; **refines NEW TODO #9 to "structural attachment" not "extraction"**). (6) Tywin↔Mountain — 4 direct + 6 2-hop, all person-mediated, zero event bridges (Sack-of-KL absent — same dark zone). (7) Red Wedding beat-union: Walder Frey 7/8 + Roose 1, Tywin absent (off-page architect); 3 NEW wrong-direction role edges for hub-review #3. (8) `robb-is-killed` has roles + structural but NO WIELDED_IN (weapon class dark — dagger, not a named sword; continue-prompt-stated "longsword" was wrong, fixed in writeup).

**Writeup landed:** `working/session-results/2026-06-09-graph-validation.md` (full 8-probe narrative + Mode 1→Mode 3 readiness call recommending **hybrid**: build #7+#8 + apply #10 first, then light Mode 3 dip drives Track B priorities). 5 NEW TODOs (#7 `--event-participants` primitive, #8 event-alias-resolver, #9 historical-anchor structural-backfill, #10 rename `joffrey-orders-execution`, #11 role-edge citation harmonization). Plus 4 NEW hub-review-queue items (S87 followup #3 grew).

**Overnight autonomous kickoff (Matt 2026-06-10, going to bed):** 3 `script-builder` agents launched in background:
- **Agent 1 — `--event-participants` primitive (#7): DONE.** `scripts/graph-query.py` extended with `cmd_event_participants()`. 4/4 smoke tests pass: red-wedding (8 beats, 29 role edges, 13 distinct participants), tourney-at-harrenhal (clean "no beats" message), nonexistent slug (clean "hub not found"), --json (valid). Results: `working/session-results/2026-06-10-overnight-event-participants.md`.
- **Agent 2 — Event-alias-resolver (#8): DONE.** `scripts/event_alias_resolver.py` + `working/wiki/data/event-alias-lookup.json` (876 phrases, 1 correct collision on `conquest-of-dorne`). 7/9 smoke tests HIT; 2 MISS are correct ("Ned's execution" auto-resolves after #10 rename + rebuild; "the Trident" needs editorial `aliases:` entry). Results: `working/session-results/2026-06-10-overnight-alias-resolver.md`.
- **Agent 3 — Rename script + DRY-RUN (#10): DONE post-commit.** `scripts/rename-event-node.py` (513 lines, `--dry-run`/`--apply`, atomic writes). Dry-run clean: 1 node file + **6 edge rows** (5 source/target + 1 superseded_by — **matches S89 probe count exactly**) + 0 reference-file hits. Action-slug audit: 29 candidates → 6 rename / 14 keep / 9 flagged for Matt. Results: `working/session-results/2026-06-10-overnight-rename-dryrun.md`. APPLY command queued in todos #10.

**Hard rules carried:** no writes to `edges.jsonl` or `graph/nodes/`, no auto-/endsession, no progression past Phase 1. All probe commands were read-only. Plate 5 state preserved: edges.jsonl=4,757, events/=583.

**What's next:**
- Matt wakes up → review 3 overnight result files → run `--apply` for #10 if dry-run is clean → fire continue prompt to start Phase 2.
- → `progress/continue-prompts/2026-06-11-phase2-mode3-dip.md` (**Opus 4.7**) — light Mode 3 grounded-agent dip (5-10 queries against the graph), failure modes drive Track B priorities. Depends on #7+#8 agents completing successfully overnight.

### Session 88 — Plate 5 recap + validation track scoped + S87 endsession gap-fill (2026-06-09 → 2026-06-10)

**Model:** Opus 4.7 (orchestrator + execution; no agents delegated). **Detail:** none (light session — wrap-up after S87 cutoff + design substance captured in the validation continue prompt). **Commits:** `cd1f362dc` (WIP gap-fill), this endsession commit.

**Context:** S87 ended abruptly mid-endsession (chat got cut off after the Plate 5 commit landed). Matt returned, asked how Plate 5 went + what the `quoted_evidence` vs `evidence_quote` field-rename was about, then asked to scope the next track ("actually using the graph to do some validation") and to make a WIP commit + push for the missed endsession steps.

**Wrap-up conversation:**
- Plate 5 recap: `edges.jsonl` 3,811 → **4,757 (+946)**; `events/` 371 → 583 (+212); validator 4,725 kept / 32 dropped (SUB_BEAT_OF empty-evidence rows remain in JSONL as read-only audit); Red Wedding 2-hop smoke passes end-to-end.
- `quoted_evidence` vs `evidence_quote`: same semantics (verbatim book quote grounding an edge); `evidence_quote` is canonical across the whole schema; `quoted_evidence` was a divergent name in Plate 4 cluster staging; fix-in-place during merge renamed 51 SUB_BEAT_OF rows (19 retained text, 32 got explanatory `plate5_evidence_note` for inference-only Pass-B/Pass-C emissions).

**Validation track scoped:** Four modes — (1) capability validation (does the new structure work; 8 probe queries on reified event hubs); (2) canonical accuracy (fact-check vs. books; partially absorbed by Track A backfill); (3) agent grounding (the real project goal — agent with `graph-query.py` as a tool answers real ASOIAF questions); (4) surprise/discovery (aggregate queries impossible pre-Plate-5). Recommendation: Mode 1 first (cheapest, isolates the graph layer; misses route cleanly to the 6 post-Plate-5 follow-up TODOs or backfill Tracks A/B/C). Mode 3 is the real test but needs Mode 1 to settle first so debugging is tractable.

**S87 endsession gap-fill (WIP commit `cd1f362dc`, pushed):**
- `working/todos.md`: EDGE/EVENT MODELING entry flipped [~]→[x] "ALL PLATES SHIPPED INCLUDING PLATE 5 (S82-S87)"; added 6 post-Plate-5 follow-up TODOs (display bullets, 32 empty-quote SUB_BEAT_OF, 109 hub-review-queue, 2 deferred collisions, donal-noye↔mag mutual-kill reverse, backfill tracks A/B/C); replaced obsolete `→ continue:` links with new validation prompt.
- `progress/continue-prompts/2026-06-09-graph-validation.md` (NEW): 4 modes, 8 Mode-1 probes, decision points listed, recommendation noted.
- `working/edge-modeling/plate3-revalidation/` (NEW): S85-era artifacts (2 minted event nodes, role-edge staging, skipped clean dyads, supersede candidates) committed for the record.
- `~/.claude/.../project_edge_modeling_reification_direction.md` (memory, outside repo): updated S84 status → S87 ship state with the 6-followup-TODO summary.

**This endsession (additional):**
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-5-merge.md` DELETED — Plate 5 shipped, prompt obsolete.
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-4-haiku-disposition.md` KEPT — its 1,617-row re-bucketing under reify lens is still part of post-Plate-5 backfill Track B; `→ continue:` link re-added under that TODO in todos.md (was accidentally removed during gap-fill edit).
- Session 83 (Edge-modeling Plates 0+1+2) archived to `history/worklog-archives/archive018.md` (archive018 now 2/5; co-located with S83-/tmp-paths).

**Out of scope (preserved untouched):** Matt's IDE edits to `progress/continue-prompts/2026-06-08-alias-and-display-design.md`; scratch deletions; `Untitled 6.rtf` deletion; `scr` untracked file at repo root.

**What's next:** → `progress/continue-prompts/2026-06-09-graph-validation.md` (**Opus 4.7** — design judgment in interpreting probe results; deterministic query work is `graph-query.py`). Matt picks Mode 1 vs straight-to-Mode-3.

> **Archive map** (`history/worklog-archives/`, 5 entries per file; per-session pointer lines collapsed to this map 2026-06-11):
> archive019 = S87 · archive018 = S83(×2: /tmp-paths + Plates 0-2)–S86 · archive017 = S78–82 · archive016 = S73–77 · archive015 = S68–72
> archive014 = S63–67 · archive013 = S58–62 · archive012 = S53–57 · archive011 = S49 (incl. 49b)–52 · archive010 = S44–48
> archive009 = S39–43 · archive008 = S34–38 · archive007 = S30–33 · archive006 = S25–29 · archive005 = S22–24
> archive004 = S16–21 · archive003 = S8–15 · archive002 = S5–7 · archive001 = S0–4

---

## Principles

> Guiding principles for the project. Reference these when making design decisions.

1. **The chapter text is immutable.** Source files in `sources/chapters/` never change. Everything else layers on top.
2. **Facts before interpretations.** Mechanical extraction before analytical. Tier 1 before Tier 4.
3. **Agents propose, humans decide.** Analytical findings go to the curation queue. Matt assigns confidence.
4. **Spoiler gating is deferred, not dropped.** `first_available` is optional in v1 nodes and backfills via deterministic script post-first-release (DEFERRED decision, 2026-04-27/S24). Don't spend context reasoning out individual values; the wiki cite_ref/infobox sources for the backfill are documented in architecture.md.
5. **The index and the graph are complementary.** The index routes. The graph traverses. Both are needed.
6. **Each token should be productive.** Structure exists to reduce waste — agents should read relevant, trustworthy content, not re-derive known relationships.
7. **Start with the foundation, not the flashiest feature.** Chapter files → mechanical extraction → wiki → index → graph → analytical passes. In that order.
