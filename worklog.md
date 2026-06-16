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

### STATUS — at a glance (verified 2026-06-15, S100)

**SHIPPED**
- Pass 1 mechanical extraction: **344/344 chapters, all 5 books** (done 2026-05-06, all Opus)
- Wiki cache local (17,945 fetched → 17,657 unique files) + Pass 2 promotion: **graph/nodes/ = 8,518** (events 585; excl. `_conflicts/` staging)
- Entity + chapter indexes: **all 21 categories** (S72)
- Edge layer LIVE: **`graph/edges/edges.jsonl` = 21,993 cited edges** (deterministic core v1.3 → Plate 5 reification S87 → S91 renames + deception pilots → S93 Wyman + Jaime restructures → S94 infobox merge +17,006 wiki-infobox → S96 graph-cleanup +59 (FIX-22 + plate5 + 27 S95 edges incl. first narrative-arc reification `incident-at-the-trident`) → S97 historical-anchor #9 wave 1 +121: 8 isolated R+L=J/Robert's-Rebellion hubs attached → **S100 historical-anchor #9 wave 2 +43: 4 WO5K hubs attached (siege-of-riverrun 2→13, battle-of-the-camps 1→12, melee-at-bitterbridge 0→14, battle-of-oxcross 1→8)**). Node connectivity **~71%**. **6 evidence kinds** (incl. **`wiki-historical-anchor`** Tier-2, ~29 total after S100 +10): wiki-infobox 17,006 / book-pass1 ~3,996 / book-pass1-reified 897 / plate4-wiki-cluster 51 / book-curator 11 / wiki-historical-anchor ~29.
- S92 Fable audit: doc truth-pass, project-story 8 chapters, infobox-merge spec v2 + script.
- S93 deferred-restructures DONE: Wyman fake-execution arc (4-beat `event.deception` parent + 2 new sub-beats + 1 rename) + Jaime street-brawl merge (renamed survivor → `attack-on-ned-stark-in-the-streets-of-kings-landing`, sibling deleted, edges deduped). New vocab type: `event.deception`. See Session 93 entry.
- **S94 (2026-06-13) infobox merge SHIPPED**: spec v2 → dry-run reproduction gate → apply. 20,614 wiki-infobox rows → 17,006 merged / 1,128 filtered / 1,037 quarantined / 1,356 deduped / 87 corroborations (bucket sum 20,614 ✓). Hygiene fixes folded in (52 slug remaps + 944 typed_by stamps). Backup at `graph/edges/_regrounding/edges-pre-infobox-merge-2026-06-13.jsonl`. See Session 94 entry.

- **Orchestration/pacer + script consolidation DONE (S98+S99)**: `scripts/pace.py` v1 (backfill+report-only) + telemetry ledger (`working/telemetry/`, 476 work rows + 8 wall events / 9 tracks) + `scripts/worker-template.py` (M1/M2/M4) + `longrun.sh` supervisor (S97). **S99 cleanup:** 30 one-offs/wrappers `git mv`→`scripts/archive/` (32 total); 9 frozen CSVs→`_archive/`; `weirwood graph/resolve/refresh` aliased (+ `scripts/weirwood-refresh.sh`); `scripts/README.md` rewritten as universal index (Class A/B/C/D + provenance, all 124 live + 32 archived covered); design §0 fully BUILT. pytest 1231 pass / 3 documented fails.

**IN FLIGHT**
- (none — S99 cleanup session complete)

**NEXT TRACK (S100 → S101)**
- ⚠️ **2026-06-16 (uncommitted, pre-/endsession): START AT `working/next-move-decisions-2026-06-16.md`.** This session re-ran the Mode 3 dip (arcs DE-PRIORITIZED a 2nd time), decided the events/time + era schema (signed `ac_year`, no `era:AC|BC` — collides with epoch `era`), and SHIPPED deterministic event dating: **112 `event.*` nodes gained an `occurred:` block (`ac_year`) + 29 gained `narrative_first`** (scripts `date-event-nodes.py` + `backfill-narrative-first.py`; pytest 1295/3; `architecture.md` amended). UNCOMMITTED; Session-101 log entry + STATUS refresh pending `/endsession`. The **4 next-move decisions** (1: PRECEDES/FOLLOWS vocab D3 + grouping · 2: causal TRIGGERS sign-off · 3: dating leftovers — 5 spans/long-night/conquest-of-dorne/10 mistyped year nodes · 4: Fable nomenclature + repo-reorg) live in that doc + `working/session-results/2026-06-16-event-dating-APPLIED.md`. The arc line below is SUPERSEDED as "recommended next."
- **narrative-arc wave 1 mint** — RECOMMENDED NEXT, but **GATED on Matt's 3 decisions** (RW-4 role edges / arc boundaries / RECIPIENT_IN). Prompt PARKED in `progress/continue-prompts/archive/2026-06-15-arc-wave1-mint.md` (one-live-prompt policy S99); restore to live when Matt decides. (**Sonnet 4.6**)
- historical-anchor #9 **wave 3 (optional, low)** — deep-lore wiki-only set (approach b); `siege-of-storms-end` cluster needs dedup first. Defer until a dip shows demand. Wave-2 prompt archived S100.
- Loose end: wire `weirwood refresh --check` into a git pre-commit hook (design §13 S8) — needs Matt's workflow buy-in (in todos).
- **Continue-prompt hygiene (FIRM, Matt S99):** live `continue-prompts/` dir = the ONE actionable next track only; gated/backlog prompts park in `archive/` (recoverable). Never present a menu of "next" prompts.
- DONE prior: historical-anchor #9 wave 2 (S100); script consolidation S1+S2 (S98/S99); historical-anchor #9 wave 1 (S97); Track 7 alias-resolver fix + Mode 3 dip + graph-cleanup (S96).

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

### Session 100 — Historical-anchor #9 wave 2 SHIPPED (4 WO5K hubs attached) (2026-06-15)
**Detail:** none (pure-execution session — wave-2 attach via the established S97 machine; worklog entry suffices).
**Model:** Opus 4.8 (1M context) orchestrator + 4 parallel Sonnet 4.6 `general-purpose` research subagents (one per hub). Continue prompt recommended Sonnet 4.6; Opus was the active session (graph-mutating-run insurance). **Commit:** uncommitted at write time (endsession pending Matt's permission).

**Changes made:**
- `graph/edges/edges.jsonl` **21,950 → 21,993 (+43)**: historical-anchor #9 wave 2 — attached 4 isolated WO5K hubs that POV chars witnessed/recall. **siege-of-riverrun** 2→13 (AFFC Jaime POV; 11 on-page tier-1: Daven/Jaime/Ryman/Blackfish COMMANDS_IN, Edmure VICTIM_IN, Frey-parley + garrison ATTENDS), **battle-of-the-camps** 1→12 (AGOT Catelyn; Robb/Brynden/Jaime COMMANDS_IN, Tytos/Umber/Forley/Grey-Wind FIGHTS_IN, Edmure/Brax VICTIM_IN, Hoster ATTENDS), **battle-of-oxcross** 1→8 (ACOK recalled, all tier-2: Stafford/Stevron/Martyn VICTIM_IN, Karstark/Grey-Wind AGENT_IN), **melee-at-bitterbridge** 0→14 (ACOK Catelyn; Brienne/Loras/Ronnet FIGHTS_IN, Renly/Catelyn/gallery + feast-night lords ATTENDS). Provenance: 33 book-pass1 (22 tier-1 / 11 tier-2 recalled) + 10 wiki-historical-anchor (tier-2 max). Backup `graph/edges/_regrounding/edges-pre-historical-anchor-2026-06-15T23-03-00.jsonl`.
- Tooling reused unchanged (`scripts/historical-anchor-{candidates,validate,mint}.py`). Candidates+notes in `working/historical-anchor/`; **wave-1 stale candidate artifacts archived** → `working/historical-anchor/wave1-archive/` (8 hub files + wave-1 `_merged`) so validate/mint only see wave-2.
- **Quote-enrichment follow-on (same session, Matt-requested re `capture-quotes-during-research` rule):** the 4 subagents had read real chapters but only edge-grounding quotes were captured. Re-swept the already-read chapters (acok-catelyn-02 feast, AFFC Jaime siege, agot-catelyn-11, acok-sansa-03) → **48 candidate quotes** (food/physical/identity) in `working/historical-anchor/quotes/*.quotes.jsonl`, then **applied 47 to 25 node `## Quotes` sections** (1 already present) via NEW `scripts/apply-node-quotes.py` (idempotent, dry-run-default, additive/node-scoped — safe alongside concurrent agents). Highlights: Aerys II's physical description (most detailed in text), Riverrun stone-ship architecture, Bitterbridge feast menu, Hoster Tully's decline. SPEC.md gained a standing "capture incidental load-bearing quotes as you go" step so future waves do this automatically. No edges.jsonl change; pytest unchanged.

**Decisions / judgment calls:**
- **Curated 4 hubs, deferred 3.** Skipped `battle-of-oxcross`-class hubs already well-connected by the S94 infobox merge (oxcross/camps were still isolated; `battle-of-the-fords`/`ashford` pair already connected or duplicate-tangled). **Deferred `siege-of-storms-end`** — it is part of a duplicate cluster (`-299`/`-300`/`-recalled`); attaching to one risks worsening fragmentation. Needs a dedup decision before attach.
- **2 curator fixes pre-mint:** (a) `battle-of-the-camps` Robb/Brynden COMMANDS_IN quote was non-verbatim (straight-vs-curly quotes) and over-tiered — repaired to a verbatim substring + downgraded tier-1→2 (Catelyn affirms outcome after arriving, not on-page command-witness). (b) DROPPED `melee` emmon-cuy ATTENDS — its quote was from a different chapter describing Rainbow-Guard sentry duty, not melee attendance (semantic-drift failure mode the SPEC warns against).
- **Verification:** validator 0 issues (43 edges); `--health` orphans unchanged at 62 (no new orphans, all endpoints node-resolved); flagship `--neighbors` confirm all 4 hubs traversable; pytest **1231 pass / 3 documented pre-existing fails** (vocab 166≠163 ×2, cwd-is-tmp). Consumer query for these direct-attach hubs is `--neighbors` (not `--event-participants`, which traverses SUB_BEAT_OF only).

**What's next:**
- → **narrative-arc wave 1 mint** — `progress/continue-prompts/2026-06-15-arc-wave1-mint.md` (**Sonnet 4.6**) — **GATED on Matt's 3 decisions** (RW-4 role edges / arc boundaries / RECIPIENT_IN).
- → historical-anchor #9 **wave 3 (optional, low priority):** the deep-lore wiki-only set (Doom of Valyria, Blackfyre Rebellions, etc.) is approach (b) — pure `wiki-historical-anchor`, defer until a dip shows agents asking about them. `siege-of-storms-end` cluster needs dedup first.
- → Track 6 script consolidation: the 3 `historical-anchor-*.py` scripts are one-offs to fold into the `weirwood` CLI per Matt's directive.

### Session 99 — Script consolidation Session 2: archive one-offs + weirwood CLI aliasing + README refresh (2026-06-15)
**Detail:** `history/session-details/session-099.md`
**Model:** Opus 4.8 (1M context) — mechanical work (continue prompt recommended Sonnet 4.6; Opus was the active session). **Commit:** this endsession commit.

**Changes made:**
- **Archived 30 scripts** `git mv` → `scripts/archive/` (24 verified-safe early Stage-4 `classify-*`/`temp-*` one-offs + `stage4-haiku-smoke-prep.py` sibling + `migrate-stats-csv.py` + 4 shelved wrappers: `stage4-haiku-run-forever.sh`, `stage4-haiku-loop.sh`, `stage4-tail-bulk-forever.sh`, `stage4-events-bulk-run.sh`). **KEPT** `stage4-run-forever.sh` (proven ref) + `edge-reify-run-forever.sh` (registry PLANNED) + 27 comention scripts. Archive now 32 files.
- **9 frozen stats CSVs** `git mv` → `working/extraction-stats/_archive/` (Pass 1 = 344/344; nothing appends). Added `_archive/` read-fallback to `pace.py backfill`, `extract.sh status`, `wiki-pass2.sh` cost glob so nothing silently degrades; fixed 2 `test_pace.py` skip-guards (suite back to 0 skips).
- `scripts/extract.sh` — de-referenced `migrate-stats-csv.py` call (one-time migration complete; breadcrumb comment).
- **NEW** `scripts/weirwood-refresh.sh` (rebuild all 17 entity-index types + character indexes + alias resolver; `--check` staleness warn per §13 S8). Wired `weirwood graph`/`resolve`/`refresh` into `scripts/weirwood.zsh` + help text on running any script under longrun.
- `scripts/weirwood-run.sh` — 3 archived-wrapper paths → `scripts/archive/`; header rewritten.
- `scripts/README.md` — **rewritten as universal index**: Class (A/B/C/D) column + `Added` git-date provenance + invocation + §11.5 new-script checklist. Existence-truth: all 124 live + 32 archived scripts have a row.
- `working/orchestration-pacer-design-2026-06-15.md` §0 — 4 Session-2 rows flipped to **BUILT S99** (file + verification); banner → BUILT; CSV-quirk RESOLVED; corrected "484 rows" → 476 work rows + 8 wall events.

**Decisions:** Three Matt-decisions (AskUserQuestion, all "Recommended"): de-reference+archive `migrate-stats-csv.py`; archive frozen CSVs to `_archive/`; archive the 4 shelved wrappers + update registry. One cross-scope judgment call flagged: the moved CSVs are read by 3 living status commands → added read-only `_archive/` fallbacks rather than accept silent degradation. pytest **1231 pass / 3 documented pre-existing fails** (vocab 166≠163 ×2; cwd-is-tmp), 0 skips. Orchestration/pacer track (design §0) now fully BUILT.

**What's next:**
- → **historical-anchor #9 wave 2** — `progress/continue-prompts/2026-06-15-historical-anchor-wave2.md` (**Sonnet 4.6**).
- → **narrative-arc wave 1 mint** — **GATED on Matt's 3 decisions** (RW-4 role edges / arc boundaries / RECIPIENT_IN). Prompt PARKED in `continue-prompts/archive/2026-06-15-arc-wave1-mint.md` (one-live-prompt policy, Matt S99); restore when decided. (**Sonnet 4.6**)
- Loose end (todos): wire `weirwood refresh --check` into a git pre-commit hook (design §13 S8) — needs Matt's workflow buy-in.

### Session 98 — Script consolidation Session 1: orchestration/pacer BUILT + design-doc anti-drift convention (2026-06-15)
**Detail:** `history/session-details/session-098.md`
**Model:** Opus 4.8 (orchestrator + direct verification) + script-builder subagent (the build). **Commit:** this endsession commit.

**Changes made:**
- **NEW** `scripts/pace.py` (Class A-pacer; v1 report-only): `backfill` normalizes 6 heterogeneous stat schemas → per-track `working/telemetry/<track>.jsonl`; `report` prints per-`(track,model,unit_type)` baselines + conservative `LONGRUN_SLEEP_BETWEEN=600` + honest M3 wall-cadence disclaimer; `emit_telemetry_row()` importable helper. **NO ETA/headroom/concurrency in v1** (wall data too thin, §13 M3).
- **NEW** `working/telemetry/` — backfilled ledger: 484 rows / 9 tracks (pass1-{agot,acok,asos,affc,adwd}, wiki-pass2-{core,secondary}, stage4-{haiku,v1-bulk-sonnet}) + 2 `.walls.jsonl` sidecars. Dup-race deduped (`acok-davos-02` kept 247s row, dropped 6s placeholder).
- **NEW** `scripts/worker-template.py` (copy-me reference worker): §4 contract + §13 M1 (positive-wall `exit(2)` only + `next-eligible`) / M2 (atomic `os.replace` + `O_EXCL` claim) / M4 (single-worker-durable v1). **NEW** `tests/test_pace.py` (40 tests).
- `working/orchestration-pacer-design-2026-06-15.md` — Status flipped DESIGN→PARTIALLY BUILT; **NEW §0 Implementation Status table** (anti-drift seam) + CSV-quirk note.
- `progress/continue-prompts/2026-06-15-script-consolidation.md` — Session 1 marked DONE; Session-2 carryover (CSV archival decision) + anti-drift definition-of-done gate added.
- **NEW** memory `feedback_design_doc_implementation_status` (+ MEMORY.md index). S93 archived → `archive020.md` (now 2/5).

**Decisions:**
- **§11 open questions NOT re-asked** — design §12 already resolved them (per-track files / advisory-only / sequential-default / v1 report-only) after fresh review; continue-prompt step-2 instruction was stale (CLAUDE.md rule #9 → trusted updated doc).
- **Verified the build directly** (not just subagent claim): grepped worker-template for M1/M2 implementation; confirmed dedup + report output. pytest **1231 pass / 3 documented pre-existing fails** (vocab 166≠163 ×2; cwd-is-tmp), was 1191.
- **Anti-drift convention** (Matt's drift concern): design docs get a §0 Implementation Status table (BUILT/DEFERRED/DRIFT + file + test); README = existence-truth; Fable doc-truth audit checks parity; def-of-done gate. The §0 table is a convention, not code-enforced — only `weirwood refresh --check` is mechanical; Fable audit = periodic backstop.
- **Honest scope held:** Session 2 (cleanup/CLI/README) NOT started — deferred per design §14.

**What's next:**
- → **Script consolidation Session 2** — `progress/continue-prompts/2026-06-15-script-consolidation.md` steps 5–8 (**Sonnet 4.6**): archive 24 one-offs + resolve 2 blocked; legacy-wrapper disposition (do NOT archive edge-reify); `weirwood graph/resolve/refresh` aliasing; README class/provenance refresh; CSV-archival decision; reconcile §0 anti-drift table.
- → historical-anchor #9 wave 2 (`2026-06-15-historical-anchor-wave2.md`, Sonnet) + narrative-arc wave 1 mint (`2026-06-15-arc-wave1-mint.md`, Sonnet — GATED on Matt's 3 decisions).

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

> **Archive map** (`history/worklog-archives/`, 5 entries per file; per-session pointer lines collapsed to this map 2026-06-11):
> archive020 = S92–95 · archive019 = S87–S91 · archive018 = S83(×2: /tmp-paths + Plates 0-2)–S86 · archive017 = S78–82 · archive016 = S73–77 · archive015 = S68–72
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
