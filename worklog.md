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

### STATUS — at a glance (verified 2026-06-17, S104)

**SHIPPED**
- Pass 1 mechanical extraction: **344/344 chapters, all 5 books** (done 2026-05-06, all Opus)
- Wiki cache local (17,945 fetched → 17,657 unique files) + Pass 2 promotion: **graph/nodes/ = 8,521** (events 588 incl. 3 S104 Rebellion spark-beats; excl. `_conflicts/` staging)
- Entity + chapter indexes: **all 21 categories** (S72)
- Edge layer LIVE: **`graph/edges/edges.jsonl` = 22,157 cited edges** (deterministic core v1.3 → … → S100 historical-anchor #9 wave 2 +43 → **S104 net +164: PRECEDES temporal-ordering (174, derived-chronology) + causal edges (6 total: Trident→Sack→Coronation pilot + the Robert's-Rebellion spark chain tourney→abduction→executions→demand→rebellion) − 16 inverted PART_OF dropped**). Node connectivity **~71%**. **7 evidence kinds** (incl. **`derived-chronology`** Tier-3 NEW S104, 174; **`wiki-historical-anchor`** Tier-2 ~29): wiki-infobox 17,006 / book-pass1 ~3,996 / book-pass1-reified 897 / derived-chronology 174 / plate4-wiki-cluster 51 / wiki-historical-anchor ~29 / book-curator 11 (+2 causal-curator-pilot). **127 edge types** (PRECEDES + CAUSES now have instances). Vocab **167** (PRECEDES added S104).
- S92 Fable audit: doc truth-pass, project-story 8 chapters, infobox-merge spec v2 + script.
- S93 deferred-restructures DONE: Wyman fake-execution arc (4-beat `event.deception` parent + 2 new sub-beats + 1 rename) + Jaime street-brawl merge (renamed survivor → `attack-on-ned-stark-in-the-streets-of-kings-landing`, sibling deleted, edges deduped). New vocab type: `event.deception`. See Session 93 entry.
- **S94 (2026-06-13) infobox merge SHIPPED**: spec v2 → dry-run reproduction gate → apply. 20,614 wiki-infobox rows → 17,006 merged / 1,128 filtered / 1,037 quarantined / 1,356 deduped / 87 corroborations (bucket sum 20,614 ✓). Hygiene fixes folded in (52 slug remaps + 944 typed_by stamps). Backup at `graph/edges/_regrounding/edges-pre-infobox-merge-2026-06-13.jsonl`. See Session 94 entry.
- **Event in-world dating (S101–S102):** **118 `event.*` nodes** carry an `occurred:` block (`ac_year`, optional `ac_year_end` span; signed int = AC/BC; `precision` enum; tier-3 from wiki year-pages) + 29 carry `narrative_first`. Schema in architecture.md §459. S102 closed the tail: 5 spans + `long-night` (null/`relative-only`) dated; **10 mis-promoted year-page nodes deleted** (year-lookup now via `occurred.ac_year`, not year nodes). Ordering edges (`PRECEDES`/`FOLLOWS`) deliberately NOT authored — derived/gated (decision #1).

- **Orchestration/pacer + script consolidation DONE (S98+S99)**: `scripts/pace.py` v1 (backfill+report-only) + telemetry ledger (`working/telemetry/`, 476 work rows + 8 wall events / 9 tracks) + `scripts/worker-template.py` (M1/M2/M4) + `longrun.sh` supervisor (S97). **S99 cleanup:** 30 one-offs/wrappers `git mv`→`scripts/archive/` (32 total); 9 frozen CSVs→`_archive/`; `weirwood graph/resolve/refresh` aliased (+ `scripts/weirwood-refresh.sh`); `scripts/README.md` rewritten as universal index (Class A/B/C/D + provenance, all 124 live + 32 archived covered); design §0 fully BUILT. pytest 1231 pass / 3 documented fails.

**IN FLIGHT**
- (none — S104 endsession complete.) **S104 closed both remaining next-move decisions:** #1 `PRECEDES` ordering edges SHIPPED (174, deterministic); #2 causal pilot SHIPPED small (2 `CAUSES` edges, Trident→Sack→Coronation, subagent-verified). The next-move-decisions prompt is fully consumed → archived. New live track = causal-edges + spark-node minting (see NEXT TRACK).

**NEXT TRACK (S104 → S105)**
- **START AT `progress/continue-prompts/2026-06-17-causal-edges-and-spark-nodes.md` (LIVE, Sonnet 4.6 + fresh-subagent verify).** Continuation of decision #2: mint the 3 missing Robert's Rebellion spark-beat nodes (`abduction-of-lyanna`, `execution-of-brandon-and-rickard-stark`, `aerys-demands-ned-and-robert`) from local-source evidence → rebuild indexes/alias-resolver (node ADD) → wire the full causal chain as `TRIGGERS` at beat granularity. Then scale to other historical hubs. **Verification model (Matt S104, FIRM):** interpretive/causal edges are checked by fresh subagents against the LOCAL wiki/book cache; Matt gates at policy level, not per-edge. This is the narrative-arc-reification pattern (`project_narrative_arc_reification`) on a historical arc.
- Background task spawned: fix 9 inverted `PART_OF` (war→battle) edges on `roberts-rebellion`, audit graph-wide + check the emitter (`task_e0a62b08`).
- Still parked (restore from `archive/` when next): arc-wave1 mint (gated on Matt's 3 decisions); Fable repo-reorg (`working/repo-reorg-plan-2026-06-12.md`); 2 narrow vocab follow-ups (todos: live non-confidence "Tier"→class/level; pull-channel pointer in ~8 agents).
- **narrative-arc wave 1 mint** — RECOMMENDED NEXT, but **GATED on Matt's 3 decisions** (RW-4 role edges / arc boundaries / RECIPIENT_IN). Prompt PARKED in `progress/continue-prompts/archive/2026-06-15-arc-wave1-mint.md` (one-live-prompt policy S99); restore to live when Matt decides. (**Sonnet 4.6**)
- historical-anchor #9 **wave 3 (optional, low)** — deep-lore wiki-only set (approach b); `siege-of-storms-end` cluster needs dedup first. Defer until a dip shows demand. Wave-2 prompt archived S100.
- Loose end: wire `weirwood refresh --check` into a git pre-commit hook (design §13 S8) — needs Matt's workflow buy-in (in todos).
- **Continue-prompt hygiene (FIRM, Matt S99):** live `continue-prompts/` dir = the ONE actionable next track only; gated/backlog prompts park in `archive/` (recoverable). Never present a menu of "next" prompts.
- DONE prior: historical-anchor #9 wave 2 (S100); script consolidation S1+S2 (S98/S99); historical-anchor #9 wave 1 (S97); Track 7 alias-resolver fix + Mode 3 dip + graph-cleanup (S96).

**GATED / QUEUED**
- Design-doc consolidation build (~3-4 sessions) — GATED on Matt's Option A/B/C pick
- Nomenclature: **scheme DECIDED S103** (3 terms — Pass/Track/Tier + lowercase `step`; `reference/glossary.md`). Full retroactive sweep DECLINED as churn; 2 narrow follow-ups queued in todos (rename live non-confidence "Tier"→class/level; pull-channel pointer in ~8 live agents)
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

### DECIDED: Canonical vocabulary — 3 terms, not 6 (2026-06-16, S103 — Fable cleanup, nomenclature half)
- **Decision (Matt, after a 4-lens advisory fan-out):** the 2026-06-12 six-term proposal was **rejected as overkill** ("six is too many, I don't know what they mean"). The empirical advisor measured living docs and found the famous collisions are mostly already tidied (S99/S101/S102) — the only genuine live ambiguity was **Track** (number-vs-letter), plus one *data* hazard (**Tier** overloading). So the canon is **three capitalized terms + one default lowercase word**:
  - **Pass** — big numbered corpus sweeps (1–6), grandfathered (baked into pipeline/`extractions/`).
  - **Track** — a *named* workstream toward a deliverable; the lettered/numbered idiom (`Track A/B/C`) is **retired going forward**, use the name.
  - **step** (lowercase) — ordered piece inside a Track; **replaces** the Stage/Plate/Phase/Wave proliferation.
  - **Tier** — confidence **1–5 only**; never work/process/promotion-class/qualifier-level (stamped on data → stray meaning = graph corruption). This is the one rule with teeth.
- **Landed this session:** `reference/glossary.md` (canonical forward vocab + retired-term decode + the consistency mechanism) + `CLAUDE.md` "## Vocabulary" stub (with the "paste terms into naming/sequencing subagents" instruction) + memory `feedback_vocabulary_canon` + this entry. The 2026-06-12 six-term proposal got a superseded preamble.
- **The mechanism (Matt's "keep it consistent + give it necessary info"):** one source of truth (`reference/glossary.md`); orchestrator gets it via CLAUDE.md every session; **subagent gap** closed by **push** (orchestrator pastes vocab into naming/sequencing subagent prompts — the only channel for `claude -p` cwd=/tmp workers) + **pull** (queued: one-line pointer in live `.claude/agents/*` defs). Grep linter **deferred** until drift recurs.
- **NOT done (deliberately): the ~175–250-edit retroactive doc sweep** — judged churn-for-tidiness (re-creates the S102 "timestamp diffs bury the real change" problem); the history glossary decodes old docs, we move forward. **Queued narrow follow-ups** in todos: rename live non-confidence "Tier" uses → class/level (the only data-error fix); add the pull-channel pointer to ~8 live agents.
- **Repo-reorg half of the Fable decision NOT taken up** (Matt picked nomenclature only). Mostly overtaken by S99/S101 hygiene; remaining leftovers + deferred MATT register stay in `working/repo-reorg-plan-2026-06-12.md`.

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

### Session 104 — PRECEDES ordering edges + causal CAUSES pilot (the 2 remaining next-move decisions) (2026-06-17)
**Detail:** `history/session-details/session-104.md`
**Model:** Opus 4.8 orchestrator + 1 fresh `general-purpose` verification subagent. **Commit:** this endsession commit.

**Changes made (edges + vocab + docs; +176 edges):**
- **Decision #1 — `PRECEDES` ordering edges SHIPPED.** Added `PRECEDES` only to the locked vocab (new "Temporal & Sequencing" subsection in `architecture.md`; `FOLLOWS`/`OCCURRED_IN_YEAR` deliberately NOT added); vocab **166 → 167**, both count-tests updated. New `scripts/build-precedes-edges.py` → **174 edges** (17 same-book narrative + 157 cross-year), Tier-3, `evidence_kind: derived-chronology` (7th kind), `typed_by: python-chronology-chain`, each tagged `order_basis`. Basis: global year-chain by `occurred.ac_year`; same-year tiebreak by `narrative_first` but **restricted to same-book** (reading-order proxy inverts cross-book — caught + fixed the wrong `red-wedding→renly-wedding` edge). Unit model (each `(year,book)` nf-run = a unit, bridged cross-year to adjacent-year reps) keeps all 117 events in one connected timeline; also fixed consecutive-floater-year ordering.
- **Decision #2 — causal pilot SHIPPED (small).** 2 `CAUSES` edges (Tier-2, `candidate_kind: causal-curator-pilot`): `battle-of-the-trident → sack-of-kings-landing → coronation-of-robert-i-baratheon`. Typed `CAUSES` not `TRIGGERS` (coarse battle-node granularity; the specific spark = Tywin's gate-opening, no node). Both `verified_by` a fresh subagent against the local cache; EDGE 2 re-cited to `Coronation_of_Robert_I_Baratheon` per the verdict.
- `edges.jsonl`: **21,993 → 22,169**; edge types 125 → **127**; orphans **62 unchanged**. Backups: `_regrounding/edges-pre-{precedes,causal-pilot,recite}-2026-06-17.jsonl`. pytest 1297 pass / 1 documented `cwd-is-tmp` fail.

**Decisions:**
- Matt picked **#1 first**, then **#2**. #1 sub-calls: PRECEDES-only / global-year-chain / P2-floater-bridged / **same-book narrative only** (chosen after a fresh-eyes case showed `narrative_first` inverts across books). #2: emit as **CAUSES** (not TRIGGERS — overclaims at this granularity); **defer** minting the 3 Rebellion spark-beat nodes (abduction/executions/demand) to a dedicated track. **NEW standing method (Matt):** interpretive/causal edges are verified by **fresh subagents against the LOCAL wiki/book cache** — Matt gates at policy level, not per-edge (memory `feedback_subagent_verify_not_matt`). Unblocks scaling causal work.

**Post-endsession continuation (same day, S104):** Matt asked for unattended follow-up work; a background agent died to a network error so this ran inline.
- **Inverted `PART_OF` fix SHIPPED** (commit `e6c031015`): dropped 16 war→battle inversions graph-wide (15 with correct forward edge + 1 malformed `roberts-rebellion→tower-of-joy`, target is a location); left 1 flagged (`shadow-war→targaryen-campaign-in-slavers-bay`, ambiguous war-vs-campaign). Root cause = S94 infobox merge (no direction guard on conflict/part-of field). edges 22,169→22,153.
- **Causal track Phase 1+2 for Robert's Rebellion DONE** (was "deferred"): minted **3 spark-beat nodes** (`abduction-of-lyanna`, `execution-of-brandon-and-rickard-stark`, `aerys-demands-ned-and-robert`; `event.incident`/`event.execution`, tier-1, 282 AC, local-source `## Quotes`) + targeted index + alias rebuild (nodes 8,518→8,521). Wired the full spark chain **verified by a fresh subagent** (all CONFIRM): `tourney-at-harrenhal —CAUSES→ abduction —CAUSES→ executions —TRIGGERS→ demand —TRIGGERS→ roberts-rebellion` (E1/E2 CAUSES not TRIGGERS per verifier — mediated). edges 22,153→22,157. All `verified_by: subagent-local-source-check-20260617`.
- State now: **8,521 nodes / 22,157 edges**, 62 orphans, pytest 1297 pass / 1 documented fail.

**What's next:**
- → **NEXT = a PURE-ANALYSIS session (Matt's call, S104)** on the strategy for causal/narrative-arc edges across the WHOLE graph (scaling beyond Robert's Rebellion). No graph writes — produce a prioritized plan. This affects all of narrative-arc reification, so it's analysis-first. `progress/continue-prompts/2026-06-17-causal-edges-and-spark-nodes.md` (**Opus or Sonnet 4.6**, analysis only).
- `shadow-war→targaryen-campaign-in-slavers-bay` **RESOLVED S104** (subagent vs local wiki): KEEP as-is — the shadow war (Sons of the Harpy insurgency in Meereen) is a wiki-attested component of the broader Slaver's Bay campaign. No change.
- Small-fix backlog (subagent-surfaced S104): `shadow-war` + `targaryen-campaign-in-slavers-bay` carry junk `DEFEATS`/`FIGHTS_IN` edges (misparsed infobox Result/Conflict/Strength fields) and are mistyped `event.battle` (should be war/campaign). → todos § Small Fixes.
- Still parked: arc-wave1 mint (gated on Matt's 3 decisions); Fable repo-reorg; 2 vocab follow-ups (todos).

### Session 103 — Fable cleanup: canonical vocabulary DECIDED (3 terms, not 6) (2026-06-16)
**Detail:** `history/session-details/session-103.md`
**Model:** Opus 4.8 (1M context) orchestrator + 4 parallel Sonnet 4.6 `general-purpose` advisors (minimalist / empirical / mechanism / ROI-skeptic). **Commit:** this endsession commit.

**Changes made (additive docs only, +33/−3, no code/graph change):**
- **NEW `reference/glossary.md`** — canonical forward vocabulary + retired-term decode + the consistency mechanism + queued follow-ups.
- `CLAUDE.md` — NEW `## Vocabulary` stub (3 terms + `step`) with the "paste terms into naming/sequencing subagents" instruction (closes the subagent-doesn't-load-CLAUDE.md gap = the "give it necessary info" answer).
- `working/nomenclature-reform-proposal.md` — superseded preamble (the 6-term scheme is no longer live).
- **NEW memory `feedback_vocabulary_canon`** (+ MEMORY.md index). `working/todos.md` — scheme marked DONE + 2 narrow follow-ups queued. Current State GATED line updated.

**Decisions:**
- Matt rejected the 2026-06-12 **six-term** scheme as overkill ("six is too many, I don't know what they mean") and ran a 4-lens advisory fan-out. Result: **3 capitalized terms + 1 lowercase word** — **Pass** (grandfathered numbered corpus sweeps) · **Track** (named workstream; lettered idiom retired) · **step** (lowercase, ordered sub-unit; replaces Stage/Plate/Phase/Wave) · **Tier** (confidence **1–5 only**, never work/process — the one rule with teeth, since Tier is stamped on edge data). Empirical advisor confirmed the famous collisions are mostly already tidied (S99/S101/S102); the only live ambiguity was Track, the only data hazard was Tier overload.
- **Full ~175–250-edit retroactive doc sweep DECLINED** as churn-for-tidiness (re-creates the S102 "timestamp diffs bury the real change" problem). History glossary decodes old docs; move forward. Two narrow follow-ups queued instead: rename live non-confidence "Tier"→class/level (the only data-error fix); pull-channel pointer in ~8 live agents. Grep linter deferred until drift recurs.
- **Mechanism** (Matt's "keep it consistent + give it necessary info"): one source of truth (`reference/glossary.md`) + CLAUDE.md stub + **push** (orchestrator pastes vocab into naming/sequencing subagent prompts) + **pull** (queued agent-def pointers). Reuses existing vocab-lockdown / drift-detection patterns, no new infra.
- **Repo-reorg half of Fable cleanup NOT taken up** (Matt's scope choice); mostly overtaken by S99/S101 hygiene anyway.

**What's next** — 2 of the 3 next-move decisions remain, both Matt's (board order #1 → #2):
- → **#1 `PRECEDES`/`FOLLOWS`** — needs vocab-add OK (D3; absent from vocab; bumps the 166 count) + grouping basis (0 dated events share a `PART_OF` parent). $0 deterministic.
- → **#2 causal `TRIGGERS`** — already in vocab; needs sign-off on the Robert's Rebellion pilot (interpretive/pollution-sensitive). Continue: `progress/continue-prompts/2026-06-16-next-move-decisions.md` (**Sonnet 4.6**).

### Session 102 — Advisory board → Track 3 dating-leftovers finished + vocab-test reconcile (2026-06-16)
**Detail:** `history/session-details/session-102.md`
**Model:** Opus 4.8 (1M context) orchestrator + 4 parallel Sonnet 4.6 `general-purpose` advisors. **Commit:** this endsession commit.

**Changes made (deterministic, $0, +0 edges):**
- **5 multi-year span events dated** via existing `ac_year_end` field: `dance-of-the-dragons` 129→132, `war-of-the-five-kings` 298→300, `greyjoy-rebellion` 289→290, `regency-of-aegon-iii` 131→136; `first-blackfyre-rebellion` = single-year **196** (dropped wiki cross-link error 212). `long-night` → `ac_year:null`/`precision:relative-only` (architecture.md:476; wiki's spurious 297 AC noted+excluded). `conquest-of-dorne` **verified** (date on `event.battle` node; book is separate `texts/` node — no change). Event nodes with `occurred:` block **112 → 118**.
- **10 mistyped year-page nodes DELETED** (`{129,130,131,134,143,157,209,283,286,298}-ac.node.md`, all `character.human`/0-edges/boilerplate) + their 10 index files + alias-resolver resync (`all-node-alias-lookup.json` dropped 10 slugs) + `characters/_summary.json` `year_pages_emitted_as_characters: 10→0`. Nodes **8,528 → 8,518**; edges/orphans unchanged (21,993/62).
- **Vocab-count test reconciled 163 → 166** (`tests/test_stage4_tail_classifier.py` + `tests/test_validate_edge_jsonl.py`; +3 = reification AGENT_IN/VICTIM_IN/SUB_BEAT_OF). **pytest 1297 pass / 1 fail** (only the environmental `cwd-is-tmp`; the 2 vocab fails now green — net 3 documented fails → 1).
- Reverted **7,921 timestamp-only** `weirwood refresh` index churns; kept only real content diffs. Final staged diff: 22 files, +25/−439.

**Decisions:**
- Matt declined a direct pick and ran an **advisory board** (4 Sonnet advisors: query-value / cost-risk / schema / curatorial). **3 of 4 → Track 3 (dating leftovers); top rec won.** Board roadmap (broadly endorsed): **#3 now → #1 ordering → #2 causal pilot → #4 Fable.** Two board findings actioned: **`TRIGGERS` already in vocab** (#2 needs no vocab add); **`PRECEDES`/`FOLLOWS` absent** (#1 needs one). Year-nodes: **delete** (Matt) — aligns with chronology-extractor design ("year pages aren't nodes"); year-lookup now via `occurred.ac_year`. Vocab-test: **reconcile to 166** (Matt) — restores the drift-detector.

**What's next** (live continue prompt updated: `progress/continue-prompts/2026-06-16-next-move-decisions.md`, **Sonnet 4.6**):
- → **3 decisions remain, all Matt's:** (1) `PRECEDES`/`FOLLOWS` vocab-add (D3) + grouping basis (0 dated events share a `PART_OF` parent) · (2) causal `TRIGGERS` sign-off (Robert's Rebellion pilot; no vocab add) · (3) Fable cleanup (nomenclature scheme + repo-reorg). Track 3 (dating leftovers) is DONE.

### Session 101 — Events/time design + deterministic event dating SHIPPED + Mode-3 dip re-run (2026-06-16)
**Detail:** `history/session-details/session-101.md`
**Model:** Opus 4.8 (1M context) orchestrator + ~14 Sonnet 4.6 subagents (dip re-run; 4-lens events/time panel; era research→analysis pipeline; 4-stance next-move panel; worklog-rotation advisor; 2 script-builder runs). **Commits:** `36abaabf` (archival) + `2eacbf7c` (dating+design) + this endsession commit.

**Changes made:**
- **Event in-world dating SHIPPED (deterministic, $0, +0 edges):** 112 `event.*` nodes gained an `occurred:` block (`ac_year` + `precision:year` + `basis_source:wiki-year-page` + `basis_reliability:tertiary-fan` + `date_confidence:tier-3`) from `chronology-events.jsonl` (single attested year + exact slug match); **29 also gained `narrative_first`** (`{book}-{chapter_number}`, min reader-encounter, resolve-all-or-skip across both edge ref formats). NEW `scripts/date-event-nodes.py` + `scripts/backfill-narrative-first.py` (+64 tests; **pytest 1295 pass / 3 documented fails**). Frontmatter-only, idempotent, bodies byte-preserved, `--health` unchanged (8,528/21,993/62). `reference/architecture.md`: `occurred:` schema + sub-field table documented.
- **Mode-3 dip RE-RUN** → `working/session-results/2026-06-15-mode3-dip-rerun.md`: **4 correct / 6 partial / 0 failed** (was 4/2/4). + temporal mini-probe (4/5 time queries fail today → motivated dating).
- **Design trail:** `working/design-opinions/` (events/time 4-lens panel + SYNTHESIS; era research + analysis) · `working/next-move-decisions-2026-06-16.md` (the 4 entry points) · `working/session-results/2026-06-16-event-dating-{dryrun,APPLIED}.md` + `2026-06-16-narrative-first-dryrun.md`.
- **Repo hygiene:** 4 historic top-level markdowns `git mv` → `history/archive/` (BEFORE-LEAVE-RESUME, EDGE_MODELING_VALIDATOR_LOG, STAGE4-SMOKE-REVIEW, next.md). Top level keeps CLAUDE/worklog/README + clusters-primer + scr.

**Decisions:**
- **Re-ran the S96 Mode-3 dip (now in archive020) on the current graph** — its arc DE-PRIORITIZATION (S96 D3) CONFIRMED a 2nd time (the measured gaps are causal-edge + `ATTENDS`, not missing arcs); recent work paid off (4 fails→0; Tourney-at-Harrenhal 0→25 edges; S96 Track-7 resolver fix verified shipped). Arc wave 1 stays parked; shipped **event dating** instead (dip-driven sequencing).
- **Events/time = TWO axes** (in-world `ac_year` vs narrative `narrative_first`); time lives in node frontmatter; ordering edges DERIVED not authored. **Era schema: signed `ac_year` (negative=BC), NO `era:AC|BC`** (collides with the existing epoch `era` field, architecture.md:438); 9-invariant validator. `long-night` excluded (wiki mention-index error — prehistoric, not 297 AC).
- **`PRECEDES`/`FOLLOWS` is GATED, not mechanical:** not in the locked vocab (deferred schema decision, roadmap D3) AND 0 dated events share a `PART_OF` parent → no cluster to order within. Needs Matt's vocab + grouping call. **Causal `TRIGGERS`** = the dip's measured gap; interpretive → Matt sign-off.
- **Worklog rotation:** archived S96 normally (→ archive020, 5/5) + anchored the S96-dip reference in this entry, rather than pausing rotation (fresh-advisor call: a paused rotation silently lapses after one context reset — a documented failure mode here). Optional future safeguard logged in todos (pytest session-count guard).

**What's next — 4 decisions, ALL for Matt** (`working/next-move-decisions-2026-06-16.md`):
- → **resolve all 4:** (1) `PRECEDES`/`FOLLOWS` vocab D3 + grouping basis · (2) causal `TRIGGERS` sign-off (Robert's Rebellion pilot) · (3) dating leftovers (5 spans / `long-night`-as-era / `conquest-of-dorne` book-vs-event / 10 mistyped `*-ac` year nodes) · (4) Fable cleanup (nomenclature scheme + repo-reorg). Continue: `progress/continue-prompts/2026-06-16-next-move-decisions.md` (**Sonnet 4.6**) — opens by asking Matt to answer them.

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

> **Archive map** (`history/worklog-archives/`, 5 entries per file; per-session pointer lines collapsed to this map 2026-06-11):
> archive021 = S97–S99 (current, 3/5) · archive020 = S92–96 · archive019 = S87–S91 · archive018 = S83(×2: /tmp-paths + Plates 0-2)–S86 · archive017 = S78–82 · archive016 = S73–77 · archive015 = S68–72
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
