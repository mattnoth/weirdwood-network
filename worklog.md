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

### STATUS — at a glance (verified 2026-06-15)

**SHIPPED**
- Pass 1 mechanical extraction: **344/344 chapters, all 5 books** (done 2026-05-06, all Opus)
- Wiki cache local (17,945 fetched → 17,657 unique files) + Pass 2 promotion: **graph/nodes/ = 8,518** (events 585; excl. `_conflicts/` staging)
- Entity + chapter indexes: **all 21 categories** (S72)
- Edge layer LIVE: **`graph/edges/edges.jsonl` = 21,950 cited edges** (deterministic core v1.3 → Plate 5 reification S87 → S91 renames + deception pilots → S93 Wyman + Jaime restructures → S94 infobox merge +17,006 wiki-infobox → S96 graph-cleanup +59 (FIX-22 + plate5 + 27 S95 edges incl. first narrative-arc reification `incident-at-the-trident`) → **S97 historical-anchor #9 wave 1 +121: 8 isolated R+L=J/Robert's-Rebellion hubs attached (tourney-at-harrenhal 0→25, the-hands-tourney 0→33, battle-of-the-trident 2→16) + Trident commanders**). Node connectivity **~71%**. **6 evidence kinds** (now incl. **`wiki-historical-anchor`** Tier-2, +~19 S97): wiki-infobox 17,006 / book-pass1 ~3,963 / book-pass1-reified 897 / plate4-wiki-cluster 51 / book-curator 11 / wiki-historical-anchor 19.
- S92 Fable audit: doc truth-pass, project-story 8 chapters, infobox-merge spec v2 + script.
- S93 deferred-restructures DONE: Wyman fake-execution arc (4-beat `event.deception` parent + 2 new sub-beats + 1 rename) + Jaime street-brawl merge (renamed survivor → `attack-on-ned-stark-in-the-streets-of-kings-landing`, sibling deleted, edges deduped). New vocab type: `event.deception`. See Session 93 entry.
- **S94 (2026-06-13) infobox merge SHIPPED**: spec v2 → dry-run reproduction gate → apply. 20,614 wiki-infobox rows → 17,006 merged / 1,128 filtered / 1,037 quarantined / 1,356 deduped / 87 corroborations (bucket sum 20,614 ✓). Hygiene fixes folded in (52 slug remaps + 944 typed_by stamps). Backup at `graph/edges/_regrounding/edges-pre-infobox-merge-2026-06-13.jsonl`. See Session 94 entry.

**IN FLIGHT**
- (none — S94 ship session complete)

**NEXT TRACK (S97)**
- **Script consolidation — Session 1 (orchestration/pacer)** — RECOMMENDED NEXT. Build `pace.py` v1 + worker-contract template + telemetry ledger per `working/orchestration-pacer-design-2026-06-15.md` (§13 must-fixes binding). Continue: `progress/continue-prompts/2026-06-15-script-consolidation.md` (Sonnet 4.6). Then Session 2 = script cleanup/aliasing/README.
- **historical-anchor #9 wave 2** (`2026-06-15-historical-anchor-wave2.md`, Sonnet) + **narrative-arc wave 1 mint** (`2026-06-15-arc-wave1-mint.md`, Sonnet — GATED on Matt's 3 decisions) remain queued.
- DONE prior: Track 7 alias-resolver fix (S96 commit `c58770549`); Mode 3 dip + graph-cleanup (S96); historical-anchor #9 wave 1 (S97).

**GATED / QUEUED**
- Design-doc consolidation build (~3-4 sessions) — GATED on Matt's Option A/B/C pick
- Nomenclature sweep — GATED on Matt's scheme pick
- Repo-reorg P1/P2 (~1-1.5 sessions) — per `working/repo-reorg-plan-2026-06-12.md`
- Backfill Tracks A/B/C (~$25–75) — gated on what the Mode 3 dip reveals
- Events-Haiku 1,617 typed rows + Dialogue tail — SHELVED (absorbed into backfill Track B)
- Spoiler gating (`first_available`) — DEFERRED post-first-release; prose-comention wiki edges — DEPRECATED, stays dead

**MATT REVIEWS NEXT:** `working/infobox-merge/dry-run-report-2026-06-12.md` (incl. 11 YOUR-DECISIONS items + 2 semantic-remap flags) → S93 look-at-twice items (Session 93 entry, 5 items) → S91 look-at-twice items (Session 91 entry)

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
- [ ] **Narrative-arc reification track (NEW S95 2026-06-13)** — apply the S87 Plate-5 event-hub reification pattern ONE LEVEL UP to causal/narrative arcs. The graph carries event hubs densely (585 events) but NOT the consequence-chains GRRM actually writes in. Reader feels Trident → Lady-and-Mycah → Sansa-Arya rift as one arc; agent sees only isolated beats. Reification pattern: parent event hub + SUB_BEAT_OF children attaching existing/new hubs + TRIGGERS/PRECEDES between sub-beats; role edges live at beat level (Red Wedding precedent). **First instance shipped S95 (Q5 in `curation/s95-quarantine-resolutions-2026-06-13.md`):** `incident-at-the-trident` parent + `death-of-mycah` new sub-beat + retroactive SUB_BEAT_OF for 3 existing Lady-arc hubs. **Sequencing: DIP-DRIVEN, not mass-mint** — Mode 3 dip surfaces which arc-shaped queries agents fumble on; that prioritizes arc-mint order. Memo: `working/narrative-arcs-design-memo-2026-06-13.md`. Memory: `project_narrative_arc_reification`. Connects to [[project_real_goal_graph_for_agents]] + [[project_stage4_richest_form]] + [[user_asoiaf_design_values]].
- [ ] Create theory seeds file (top 20-30 theories with confidence tiers) — prerequisite for Pass 5 AND for connecting the all-dark `theories/` layer (45 nodes, ~0 real edges; the infobox merge contributes nothing there — see synthesis 2026-06-11)

### MEDIUM
- [ ] Design the trigger table schema (what columns, what routing logic) — the one unshipped piece of the index layer
- [ ] Write Pass 3 voice analysis prompt — cross-POV perception dimension; feeds the talk-to-a-character goal
- [ ] Write Pass 4 foreshadowing prompt — agent receives `reference/foreshadowing-events.md` and scans chapter extractions for matches
- [ ] Build convergence map for Oldtown as proof of concept (`graph/convergence-maps/` still empty)
- [ ] Prophecy node layer is undercounted (2 nodes, 0 edges) — mint the canon prophecies (Azor Ahai, valonqar, dragon-has-three-heads…) from existing wiki pages
- [ ] **Non-saga source ingestion — TWOIAF (6th source) + Fire & Blood (7th source)** (NEW S97 2026-06-15, Matt). Would convert the ~300 deep-lore isolated historical hubs (Doom of Valyria, Blackfyre Rebellions, Targaryen Conquest, Dance of the Dragons) from `wiki-historical-anchor` (Tier-2) to book-grounded dyads. **TWOIAF is already on disk** (`sources/raw/TWOIAF.txt`, 179K-word OCR) but never Pass-1-extracted → cheaper first step. **F&B is NOT on disk** (only wiki *pages about* it in `_raw/`) → must acquire text first. Caveat: both are non-POV history register (Yandel / Gyldayn), closer to the wiki than a chapter, and the wiki cache is largely derived from them — unique value is verbatim primary-text Tier-1 quotes + detail the wiki compressed. Own ingestion track (different extraction shape than a POV novel). **For now: use the wiki for those hubs (Matt 2026-06-15); enrich with TWOIAF/F&B later.** Connects to historical-anchor #9 wave 2 + the theory-node layer (pre-series events anchor R+L=J / KotLT theories).

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

### Session 97 — Historical-anchor #9 wave 1 SHIPPED + Orchestration/Pacer design doc (2026-06-15)
**Detail:** `history/session-details/session-097.md`
**Model:** Opus 4.8 orchestrator + Sonnet 4.6 subagents (8 historical-anchor research + 1 sequencing advisor + 1 design reviewer). **Commit:** uncommitted at endsession (Matt to decide).

**Changes made:**
- `graph/edges/edges.jsonl` **21,829 → 21,950 (+121)**: historical-anchor #9 wave 1 (+118 across 8 isolated R+L=J/Robert's-Rebellion hubs) + 3 Trident COMMANDS_IN (Robert/Rhaegar/Lewyn). Hubs: `tourney-at-harrenhal` 0→25, `the-hands-tourney` 0→33, `battle-of-the-trident` 2→16, `sack-of-kings-landing`, `combat-at-the-tower-of-joy`, `greyjoy-rebellion`, `defiance-of-duskendale`, `tragedy-at-summerhall`. **NEW evidence_kind `wiki-historical-anchor`** (Tier-2 max; 19 edges). Backups in `_regrounding/`.
- NEW scripts: `scripts/historical-anchor-{candidates,validate,mint}.py` + `working/historical-anchor/SPEC.md` + per-hub candidate/notes files. NEW `tests/test_longrun_supervisor.py` (6 tests, longrun exit-10/2/0/crash/resume verified).
- NEW `working/orchestration-pacer-design-2026-06-15.md` — design doc (supervisor/worker/pacer architecture, exit-code contract, telemetry ledger, §1.5 script taxonomy A/B/C/D, §11 Script Org Standard, §13 review amendments, §14 two-session scope). Fresh-reviewed.
- NEW memory `project_rebuild_derived_artifacts_after_node_mutation` (+ MEMORY.md index). NEW continue prompts: `2026-06-15-historical-anchor-wave2.md`, `2026-06-15-script-consolidation.md` (2-session split).
- `worklog.md` (this entry; S92 archived → `archive020.md`), `working/todos.md` (#9 wave1 done, script-consolidation pointer), `working/historical-anchor/`.

**Decisions:**
- **Pivoted from the queued arc-mint to followup #9** (fresh advisor + worklog order both said #9-first; arc mint maps to 0 dip questions). **Arc wave-1 mint stays drafted-but-unminted, still gated on Matt's 3 decisions** (RW-4 role edges / arc boundaries / RECIPIENT_IN). #9 method: curate the main-saga-recalled cluster (the ~300 deep-lore hubs are wiki-only, out of scope), per-hub Sonnet subagent → JSON attach edges → 2-stage verbatim validation → curator drop/fix (6 dropped, 4 fixed). Provenance: book-pass1 tier-1/2 earned by chapter quote; wiki-only → `wiki-historical-anchor` tier-2 max.
- **Script consolidation = design-doc-first** (Matt). Architecture: bash `longrun.sh` wraps a resumable Python worker (emits 0/2/10) + a Python `pace.py` pacer mining past run-stats; `weirwood` CLI front door; per-worker JSONL telemetry (fixes the real CSV-append race). Review found 4 must-fix spec gaps (positive wall-detect-or-crash; atomic state writes; honest thin wall-cadence backfill; shared next-eligible for concurrency → v1 single-worker). **Honest scope = TWO sessions** (pacer, then cleanup).
- **TWOIAF (6th source, on disk unextracted) + F&B (7th, not on disk) backlogged**; use wiki for deep-lore hubs now.

**What's next:**
- → **Script consolidation Session 1 (orchestration/pacer)** — `progress/continue-prompts/2026-06-15-script-consolidation.md` (Sonnet 4.6). Recommended next.
- → historical-anchor #9 wave 2 — `progress/continue-prompts/2026-06-15-historical-anchor-wave2.md` (Sonnet 4.6).
- → narrative-arc wave 1 mint — `progress/continue-prompts/2026-06-15-arc-wave1-mint.md` (Sonnet 4.6) — **GATED on Matt's 3 decisions**.

### Session 96 — Mode 3 dip + graph-cleanup/promotion SHIPPED (FIX-22 + plate5 + S95 incl. Trident & Joffrey arcs) (2026-06-14)

**Model:** Opus 4.8 (orchestrator) + fresh `general-purpose` subagents — one ran the Mode 3 dip and reached its own findings ("ask a fresh subagent… have it decide"); one (Sonnet) executed the graph-cleanup under Opus orchestration + verification. **Detail:** dip findings in `working/session-results/2026-06-14-mode3-dip-results.md`. **Commit:** this commit (also captures the previously-uncommitted S94 infobox merge + S95 research).

**Changes made:**
- **NEW** `working/session-results/2026-06-14-mode3-dip-results.md` — full dip: 10 grounded Qs, per-query results table, failure-mode taxonomy, routing decision, + §6 post-dip Q4/Q5 corrections.
- `working/todos.md` — Track 2 (Mode 3 dip) marked **DONE**; **NEW Track 7** (query-layer tooling — alias-resolver fix, dip primary); POST-PLATE-5 followup #9 **ungated** as dip secondary; at-a-glance line updated.
- `worklog.md` — this entry; **Session 91 archived to `history/worklog-archives/archive019.md` (now full 5/5)**.
- **NO graph writes** — the dip is read-only (verified: `edges.jsonl` mtime unchanged, untouched 2026-06-13 10:00; `graph/` `M` marks predate this session, from the S94 merge).

**Findings & decisions:**
- **Score: 4 correct / 2 partial / 4 failed.** The graph is genuinely useful to a consumer agent **today** for the two highest-frequency shapes: relationship queries (`--path`, best-in-class) and on-page-event queries (`--event-participants` over beat-reified hubs). Post-infobox kinship/allegiance/title/culture is dense and reliable.
- **(D1) Dominant failure = slug-discoverability.** In Q1/Q3/Q7 the perfect, quote-cited answer was already in the graph; the ONLY failure was the alias resolver MISSing natural phrasings ("Robb Stark's death", "Ned Stark's execution"). A deployed agent can't fs-grep around that. → **Primary next track = fix the alias resolver** (fuzzy fallback + index death/execution hubs by victim + return character-node candidates). ~4/10 → ~7/10 for $0. (NEW Track 7.)
- **(D2) Secondary = historical structural-attachment (followup #9, ungated).** Isolated hubs (`tourney-at-harrenhal` 0 edges; `battle-of-the-trident` only PART_OF) whose underlying facts already exist elsewhere as dyads. Q5 is the worked example: the `rhaegar-targaryen → lyanna-stark` CROWNS edge exists with a quote that literally names Harrenhal — it's just not attached to the tourney hub. Fix = attach existing dyads, no new extraction.
- **(D3) Narrative-arc reification DE-PRIORITIZED** for now — only 2 Qs were arc-shaped, one already scheduled (Trident); the dominant problem is a lookup bug sitting on correct data, not missing arcs. Arc track stays HIGH long-term but slots behind Track 7 + #9.
- **(D4) Q4 correction (Matt 2026-06-14):** re-graded `failed` → not-applicable. The weapon that killed Robb IS known (Roose's longsword, asos-catelyn-07.md:135) but it's unnamed — not an `object.artifact` — so `WIELDED_IN` is correctly absent. No defect, no backfill. (Contrast: Ned's execution carries `WIELDED_IN → Ice` because Ice is named.)

**Look-at-twice for Matt:** none new — the dip was read-only and made no graph claims to ratify.

**Graph cleanup / promotion SHIPPED (same session, both gates cleared):**
- `edges.jsonl` **21,770 → 21,829 (+59 net)**: FIX-22 (F1 siege repair, F2 wrong-direction retypes/drop, F3a+b Purple Wedding beats, F4a Red Wedding guest-right, F5 Tyrion→Joffrey demoted tier-1→tier-4 false-confession, F6a–l 12 canon-death dyads incl. **F6h `rhaegal KILLS quentyn-martell`** resolved from text not generic) + plate5 small-followups (A1 conquest-of-dorne→object.text, A2 maidenpool merge, B mutual-kill reverse edge, C-1 Contract-6 SUB_BEAT_OF quote-exemption + C-2 quote fix) + **27 S95 edges** (Q1–Q5).
- **10 new nodes**: 3 wedding beats (incl. `death-of-joffrey-baratheon` event.assassination w/ `## Quotes` block) + 7 S95 (postern-guard, ghiscari-galley-crews, stallion-who-mounts-the-world prophecy, stallion-heart-ceremony, wedding-feast-at-the-red-keep, **incident-at-the-trident**, **death-of-mycah**).
- **First narrative-arc reification live**: `incident-at-the-trident` parent + 4 sub-beats (Cersei/Lady/Mycah cluster), beat-union traverses end-to-end. Joffrey cluster: Olenna AGENT_IN tier-2 + **Littlefinger COMMANDS_IN** both carrying his ASOS Sansa VI reveal quote (marquee-dialogue capture per new firm rule [[feedback_capture_quotes_during_research]]).
- `architecture.md` gained `event.incident` row; validator gained SUB_BEAT_OF Contract-6 exemption. Backup: `_regrounding/edges-pre-graph-cleanup-2026-06-14T15-26-24.jsonl`. Verification: `--health` clean (62 orphans, −1), pytest 1144 pass + 3 documented pre-existing failures only.
- **Minor look-at-twice:** `death-of-joffrey-baratheon LOCATED_AT red-keep` edge carries the Olenna-wine quote instead of a location line (cosmetic; correct target/tier).

**New standing rules (S96):** (1) **Capture load-bearing quotes during research** — FIRM rule, any time a session is in chapter/wiki text for ANY purpose (researched or happenstance) and finds a quotable death/feast/description/dialogue/prophecy line, attach it to the graph (edge `evidence_quote` or node `## Quotes`) before moving on; lightweight `working/quote-capture-queue.md` backlog allowed when full inline capture would derail the task. Memory `feedback_capture_quotes_during_research`. (2) **Arc parent-shape** — arc parent = NEW `event.conspiracy` hub WRAPPING the existing event hub (event becomes one sub-beat); pre/post-event beats attach to the conspiracy, in-feast beats to the event (scope test). Memory `project_narrative_arc_reification`.

**What's next (dip-driven sequencing):**
- → **NEW Track 7** alias-resolver fix — the dip's PRIMARY, highest-leverage $0/deterministic move (~4/10→~7/10); makes the just-shipped Trident/Joffrey arcs findable by natural phrasing. Recommend NEXT, ahead of arc-minting. Needs a continue prompt. (**Sonnet 4.6**)
- → followup #9 historical structural-attachment — dip's secondary, ungated. (**Sonnet 4.6**)
- → narrative-arc wave 1 — **DRAFTS STAGED FOR MATT REVIEW (S96, 2026-06-14):** `curation/narrative-arc-wave1-red-wedding-draft-2026-06-14.md` (proposes `red-wedding-conspiracy` parent, 5 new mints + 22 edges) + `curation/narrative-arc-wave1-joffrey-draft-2026-06-14.md` (proposes `joffrey-poisoning-conspiracy` parent, 4 new nodes + 18 edges). Both are DRAFT-ONLY (nothing minted). Each has open design Qs for Matt (arc boundaries; a vocab gap — no role type for Sansa's "unwitting instrument"). After Matt's review → a mint session applies them (S95-style). Track 7 resolver fix landed first so new arcs are discoverable.

### Session 95 — Post-merge research: 5 QUARANTINE items resolved + Trident-incident reification + **narrative-arc track surfaced** (2026-06-13)

**Model:** Opus 4.7 (orchestrator + design judgment) + 4 parallel Sonnet 4.6 research subagents. **Detail:** none separate — the design content is in the memo (`working/narrative-arcs-design-memo-2026-06-13.md`). **Commit:** this endsession commit.

**Changes made:**
- **NEW** `curation/s95-quarantine-resolutions-2026-06-13.md` — single source-of-truth file for the cleanup session: 5 dossiers (eagle, postern-guard, galley-crews, stallion-heart, wedding-feast) + **Q5 Trident-incident reification (Matt-added 2026-06-13)** + slug-naming confirmations. **27 JSON-ready edges + 7 new node files**, all verbatim-grounded.
- `curation/hub-review-triage-2026-06-12.md` — QUARANTINE table updated with per-item S95 status column (5 RESOLVED, 2 SKIP w/ rationale, 3 remain Track-B routed); a-boy-is-run-down clarification (NOT Mycah — Lhazareen-boy from Drogo sack; Mycah's death reified separately as Q5).
- `progress/continue-prompts/2026-06-12-graph-cleanup.md` — source-files list updated to point at S95 resolutions; 3 out-of-scope flags added (Varamyr-eagle-attacks-Jon followup, `the-stallion-is-brought-in-and-sacrificed` mis-slug rename, `a-captive-girl-is-beheaded` Pass-1 audit).
- **NEW** `working/narrative-arcs-design-memo-2026-06-13.md` — design memo for the narrative-arc reification track: pattern (parent event hub + SUB_BEAT_OF children + TRIGGERS for causal direction), 15 candidate-arc seeds (small/medium/epic), 6 open design questions, fit with current queue.
- **NEW** memory entry `project_narrative_arc_reification.md` + MEMORY.md index updated.
- `worklog.md` — Ideas & Backlog HIGH gained narrative-arc track at top (above theory-seeds).
- Continue-prompt updates for SEQUENTIAL EXECUTION (Matt 2026-06-13): Mode 3 dip prompt + graph-cleanup prompt + README manifest now reflect sequential rather than parallel-safe; arc-question script enhancement added to dip prompt.

**Decisions:**
- **(D1) 5 QUARANTINE items resolved via subagent research, 2 SKIP, 3 stay Track-B-routed.** Eagle ATTACKS attaches to Orell (only scene is ACOK Jon VII, Orell still alive — Varamyr post-takeover is later). Unnamed-victim policy = P4 mixed: mint for narrative-role-significant kills (Arya postern-guard, Victarion galley-crews), skip for atrocity-flavor (Lhazareen boy, Harrenhal captive girl — latter also flagged as possible Pass-1 paraphrase). Stallion-heart ceremony mints as distinct event + Stallion-Who-Mounts-the-World prophecy node + SUBJECT_OF_PROPHECY/PROPHESIED_BY edges. Wedding-feast attaches as new sub-beat under existing Tommen-Margaery hub.
- **(D2) Q5 Trident-incident reification (Matt-added).** New parent `incident-at-the-trident` (event.incident) + new sub-beat `death-of-mycah` (event.death) + retroactive SUB_BEAT_OF for 3 existing standalone hubs (cersei-maneuvers / ned-kills-lady / ned-claims-the-execution). Bride/groom = AGENT_IN their own wedding, not ATTENDS (Matt clarification — applied to Tommen/Margaery wedding-feast roles; convention noted in resolution file).
- **(D3) NARRATIVE-ARC REIFICATION as a new HIGH-priority track.** Apply the S87 Plate-5 event-hub pattern ONE LEVEL UP to causal chains spanning multiple existing event hubs. The graph carries events; it does NOT carry the consequence-chains GRRM writes in. First instance = Q5 Trident incident. No new vocab needed (SUB_BEAT_OF + TRIGGERS + existing event types suffice). Sequencing: **dip-driven, NOT mass-mint** — Mode 3 dip's arc-question failures become the priority signal.
- **(D4) Execution order = SEQUENTIAL (Matt 2026-06-13).** Mode 3 dip → graph cleanup (incl. all S95 resolutions) → narrative-arc track wave 1. NOT parallel-safe. Continue prompts updated to reflect.

**Look-at-twice items for Matt (S95):**
- `event.incident` type — confirm in vocab list before cleanup mints `incident-at-the-trident` (was original type for the Jaime-ambush hub before S93 promoted to `event.battle`; should still be available)
- The 4 Mode 3 dip arc-questions (added in script enhancement) — review/edit before launching the dip; current set is a placeholder
- Mycah death-of-mycah is now reified BUT the existing `sandor-clegane KILLS mycah` Tier-1 dyad stays — sibling per S87 convention. Confirm both layers coexist cleanly post-cleanup.
- The Mode 3 dip will likely also surface arc-shaped gaps for: Tower of Joy (all-dark zone per S89), Sack of King's Landing (no causal chain to Mountain's later acts), Robert's Rebellion (no chain to Joffrey coronation). Those become arc-track wave 1 candidates.

**What's next (SEQUENTIAL per Matt 2026-06-13):**
- 1️⃣ → `progress/continue-prompts/2026-06-11-phase2-mode3-dip.md` (**Opus 4.7**) — Mode 3 grounded-agent dip on the merged graph. Now includes 2-3 arc-shaped questions per Matt's narrative-arc track decision.
- 2️⃣ → `progress/continue-prompts/2026-06-12-graph-cleanup.md` (**Sonnet 4.6**) — FIX-22 + S95 resolutions (incl. Q5 Trident reification) + plate5 followups. Run AFTER Mode 3 dip lands.
- 3️⃣ → narrative-arc track wave 1 — gets a continue prompt after the dip's findings sharpen the candidate list. ~3-5 small arcs minted using S95's parallel-research-subagent pattern.

### Session 94 — Infobox merge SHIPPED + 2 bug-fixes (continue-prompt schema, script report-rewrite guard) (2026-06-13)

**Model:** Opus 4.7 (deterministic apply + verification + 2 small fixes; Matt-preferred override of the continue-prompt's Sonnet 4.6 recommendation, taken for insurance value during a 4-step graph-mutating run). **Detail:** none (execution-heavy). **Commit:** this endsession commit.

**Changes made:**
- `graph/edges/edges.jsonl` — applied infobox merge: **4,764 → 21,770 rows (+17,006 wiki-infobox, +52 hygiene A slug remaps, +944 hygiene B typed_by stamps)**. Backup at `graph/edges/_regrounding/edges-pre-infobox-merge-2026-06-13.jsonl`.
- `graph/index/` — rebuilt all 18 category indexes (locations, artifacts, houses, factions, titles, events, religions, species, texts, concepts, materials, foods, theories, customs, languages, medical, prophecies via `build-entity-indexes.py`; characters via `build-character-indexes.py`).
- `working/wiki/data/event-alias-lookup.json` — rebuilt: 953 unambiguous + 1 pre-existing collision (954 unique phrases, unchanged from S93).
- `progress/continue-prompts/2026-06-12-infobox-merge-ship.md` — step 3c snippets corrected: `type` → `edge_type`, `source`/`target` → `source_slug`/`target_slug` (matches actual edges.jsonl schema; old field names returned `UNKNOWN: 21770` until corrected).
- `scripts/infobox-merge.py` — guarded `write_dry_run_report()` behind `if not apply_mode:`. `--apply` was silently rewriting the curated dry-run report on every run, wiping Matt's S93 closeout banner + 11 `[x] accept default` marks. Marks restored from git after each rewrite this session; the guard prevents recurrence. 75 infobox-merge tests still green.
- `working/infobox-merge/dry-run-report-2026-06-12.md` — restored to its committed marked form (script wiped it twice mid-session; git checkout each time).
- `worklog.md` STATUS block — connectivity 14.7% → 71.0%; edges 4,764 → 21,770; evidence_kind breakdown documented (wiki-infobox 17,006 / book-pass1 3,809 / book-pass1-reified 893 / plate4-wiki-cluster 51 / book-curator 11).
- `working/todos.md` Track 1 — Ship item marked DONE; Track 2 (Mode 3 dip) flipped from GATED to READY.
- `progress/continue-prompts/2026-06-11-phase2-mode3-dip.md` — "GATE CLEARED 2026-06-13 (S94)" banner added under the existing gate note.

**Decisions:** Followed the handoff's hard rule (re-run dry-run first; halt if counts deviate). Dry-run reproduced spec v2 EXACTLY (17,006 / 1,128 / 1,037 / 1,356 / 87, bucket sum 20,614 ✓), so applied immediately. Verification gates all passed: `--health` reports only the 63 documented orphans (spec §5), 123 edge types, 0 UNKNOWN; pytest 1144 pass + 3 documented pre-existing failures (vocab-163 ×2 — now 166 since S93's `event.deception`; cwd ≠ /tmp). No new structural defects surfaced. The continue-prompt field-name mismatch and the script's unconditional report-rewrite both qualify as quality-of-life bugs introduced earlier — fixed inline rather than queued.

**Look-at-twice items for Matt:** none. Apply was clean. Backup is intact at `_regrounding/edges-pre-infobox-merge-2026-06-13.jsonl` if any post-hoc revert is wanted.

**What's next:**
- → `progress/continue-prompts/2026-06-11-phase2-mode3-dip.md` (**Opus 4.7**) — Mode 3 grounded-agent dip on the now-merged graph. Gate cleared today; the prompt's banner notes the new counts.
- Parallel-safe: `progress/continue-prompts/2026-06-12-graph-cleanup.md` (FIX-22 + small followups + 3 missing Red Wedding SUB_BEAT_OF links). Still double-gated on Matt's curation marks in `curation/hub-review-triage-2026-06-12.md` + `curation/plate5-small-followups-2026-06-12.md`.
- `progress/continue-prompts/2026-06-12-infobox-merge-ship.md` — completed this session; delete in step 3 below.

### Session 93 — Deferred structural restructures: Wyman fake-execution arc + Jaime street-brawl merge; `event.deception` vocab added (2026-06-12)

**Model:** Opus 4.7 (orchestrator + all writes; no agents delegated — structural work too tightly coupled to fan out). **Detail:** `history/session-details/session-093.md` (design narrative — wiki research methodology, `event.deception` vocab rationale, Jaime-collapse decision, Q11 reframing). **Execution writeup:** `working/session-results/2026-06-12-deferred-restructures.md` (file paths, edge JSON, verification commands, hard-rule audit). **Commit:** this endsession commit.

- **Vocab change (cheap):** Added **`event.deception`** to entity-type table (`reference/architecture.md:118`) + `schema-legend.md:295` events row. Cost: 2-line documentation update. No TYPE_DIR_MAP / validator / drift-detection change (no global event-subtype validator exists; events route to one dir; hand-minted not bulk LLM). Definition: "Named discrete act-of-deceiving as event-hub — single staged moment whose purpose is to propagate a false belief to a specific audience. Distinct from event.conspiracy (ongoing scheme) and DECEIVES (dyadic edge). Nested INSIDE event.conspiracy hubs (Wyman's farce sits inside Grand Northern Conspiracy)." Schema row lists 4 canonical seed examples (Wyman, Cersei's false-attack claim, Theon's burned boys, Jeyne-as-Arya).
- **Wyman arc — 4 beats not 2:** Wiki research (`Wyman_Manderly.json`) revealed the canonical arc has 4 distinct beats. Minted parent `wyman-manderly-stages-fake-execution-of-davos` (`event.deception`) + 2 new sub-beats (`execution-of-davos-lookalike-at-white-harbor` for the substitute beheading; `frey-witnesses-attest-davos-dead-at-small-council` for Cersei's small-council propagation in AFFC Cersei IV). Renamed `lord-wyman-orders-execution` → `wyman-publicly-orders-davos-execution`. Patched arrest-beat body to reference all siblings + parent. 6 edges appended: 4 × SUB_BEAT_OF + 1 × DECEIVES wyman→cersei (qualifier="by_false_witness", AFFC Cersei IV) + 1 × CONSPIRES_WITH wyman↔stannis (Tier-3 no qualifier; rickon-return clause + via-davos-envoy in rationale).
- **Jaime arc — collapse to single hub, not parent+children:** AWOIAF has NO discrete event page for the street brawl (treated as "melee" in Ned's biography). Renamed `jaime-lannister-ambushes-ned-s-party` → `attack-on-ned-stark-in-the-streets-of-kings-landing` (event.battle, was event.incident). Deleted sibling `jaime-sheathes-his-sword-but-orders-ned-s-men-killed.node.md`. Of its 5 role edges: 1 unique COMMANDS_IN repointed to the renamed hub (tagged `merged_from_sheathes_sibling`); 4 duplicates (AGENT_IN house-lannister, VICTIM_IN jory/heward/wyl) dropped. 2 new edges appended: DECEIVES jaime→ned qualifier="by_omission" (sheathe-and-order cinematic pivot, AGOT Eddard IX); TRIGGERS attack→`cersei-claims-ned-s-men-attacked-first` (causal link to Cersei's downstream lie, AGOT Eddard X). No separate parent layer minted — survivor IS the canonical hub.
- **Counts:** `edges.jsonl` **4,760 → 4,764 (+4 net: +6 Wyman, +2 Jaime, −4 dups)**. `events/` **583 → 585 (+2: +3 Wyman mints, −1 Jaime sibling delete)**. `event-alias-lookup.json` **922 → 954 (+32)**. Orphan endpoints **115 (unchanged)**. Edge types active **112 (unchanged)**.
- **Verification:** `--health` clean (8,518 nodes, 4,764 edges); `--event-participants wyman-manderly-stages-fake-execution-of-davos` traverses all 4 beats and surfaces 5 distinct participants end-to-end; `--neighbors attack-on-ned-stark-in-the-streets-of-kings-landing` shows 2 outgoing + 8 incoming (3 AGENT_IN + 1 COMMANDS_IN + 4 VICTIM_IN, no double-counting); 16/16 alias-chain probes HIT (resolver convention strips leading "the "); 0 stale source/target/superseded_by refs to old slugs in edges.jsonl. Cleaned up 3 stale index files (renamed/deleted node leftovers).

**Look-at-twice items for Matt:** (a) `lord-wyman-manderly` slug-collision visible in beat-union traversal (pre-existing from S87 Plate 3 mints, NOT introduced by S93; candidate for slug-merge cleanup); (b) S91 pilot `DECEIVES wyman→house-frey` uses non-enum qualifier `"staged-arrest"` while my new wyman→cersei uses enum-conforming `by_false_witness` — normalize the S91 row to `by_omission` or leave? (c) 2 new SUB_BEAT_OF rows carry `plate5_evidence_note` instead of verbatim quotes (substitute beheading off-page; Frey small-council in summary-register) — falls under the existing 32-empty-quote Contract-6-exemption followup, not S93-specific; (d) `event.deception` has 2 instances so far (Wyman parent + Frey small-council); future passes could promote 3 more canonical examples deliberately; (e) Jaime DECEIVES target choice — picked Ned per original subagent rec; alternative read is Robert (plausible deniability) — Cersei-claim TRIGGERS edge already captures Robert as the downstream-deception audience.

**Hard rules held:** rename `--dry-run` before `--apply` (both renames); no auto-/endsession (stopped at writeup + worklog); old slugs preserved as final alias entries; Bug 1 inline aliases throughout; Bug 3 plate5_superseded_note patches applied (2 stale free-text notes patched: 1 Wyman, 1 Jaime).

**What's next (HANDOFFs from session start unchanged):**
- HANDOFF 1: `progress/continue-prompts/2026-06-12-infobox-merge-ship.md` — still gated on Matt marking the dry-run report's 11 decisions
- HANDOFF 2: `progress/continue-prompts/2026-06-12-graph-cleanup.md` — gated on HANDOFF 1 shipping + curation marks
- HANDOFF 3: `progress/continue-prompts/2026-06-11-phase2-mode3-dip.md` — gated on infobox merge shipping
- Parallel-safe restructures track (this session) — **DONE**, prompt can be retired
- `progress/continue-prompts/2026-06-12-deferred-structural-restructures.md` can be deleted after Matt confirms the writeup.

> **Archive map** (`history/worklog-archives/`, 5 entries per file; per-session pointer lines collapsed to this map 2026-06-11):
> archive020 = S92 · archive019 = S87–S91 · archive018 = S83(×2: /tmp-paths + Plates 0-2)–S86 · archive017 = S78–82 · archive016 = S73–77 · archive015 = S68–72
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
