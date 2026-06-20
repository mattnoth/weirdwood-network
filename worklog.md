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

### STATUS — at a glance (verified 2026-06-19, S109)

**SHIPPED**
- Pass 1 mechanical extraction: **344/344 chapters, all 5 books** (done 2026-05-06, all Opus)
- Wiki cache local (17,945 fetched → 17,657 unique files) + Pass 2 promotion: **graph/nodes/ = 8,545** (events incl. S104 RR spark-beats + 5 S105 Bran's-fall beats + 8 S106 arc beats [4 Sack-of-KL + 4 Purple-Wedding] + 6 S107 beats [5 B1 Red-Wedding-upstream + 1 B2 Theon-ward] + 3 S108 beats [B3 Ned's-downfall] + **3 S109 beats [Tywin's-death arc: jaime-frees-tyrion + tysha-revelation + tyrion-kills-shae; the `assassination-of-tywin-lannister` hub repaired in place — retyped event.assassination]**; excl. `_conflicts/` staging)
- Entity + chapter indexes: **all 21 categories** (S72)
- Edge layer LIVE: **`graph/edges/edges.jsonl` = 22,272 cited edges** (deterministic core v1.3 → … → S106 +41 two Tier-A arcs → S107 +26 two Tier-B arcs [B1/B2] → S108 +14 B3 Ned's-downfall → **S109 +17: Tywin's-death arc (fresh-dip-gated, Q14) — 6 causal Tier-2: `trial TRIGGERS gregor-kills-oberyn CAUSES jaime-frees CAUSES tysha-revelation CAUSES assassination`, Shae sibling-branch `tysha-revelation CAUSES tyrion-kills-shae`, agency `tysha-revelation MOTIVATES tyrion`; role edges Tier-1 (Tyrion AGENT_IN, Tywin VICTIM_IN, Jaime AGENT_IN + Varys COMMANDS_IN the freeing); hub `assassination-of-tywin-lannister` repaired (retype + alias + junk-prose removal); hard-stops short of WO5K**). The Tywin chain joins the Purple-Wedding arc → `--causal-chain assassination-of-tywin-lannister` walks 7 upstream edges back to Sansa's hairnet. Query primitive **`graph-query.py --causal-chain`** (walks CAUSES/TRIGGERS/MOTIVATES both directions). Node connectivity **~71%**. **7 evidence kinds** (incl. **`derived-chronology`** Tier-3 S104; **`wiki-historical-anchor`** Tier-2): wiki-infobox 17,006 / book-pass1 ~4,010 / book-pass1-reified 897 / derived-chronology 174 / plate4-wiki-cluster 51 / wiki-historical-anchor ~29 / book-curator 11 (+ causal-curator-arc ~57). **128 edge types** (no new types since `MOTIVATES`, S105). Vocab **167**.
- S92 Fable audit: doc truth-pass, project-story 8 chapters, infobox-merge spec v2 + script.
- S93 deferred-restructures DONE: Wyman fake-execution arc (4-beat `event.deception` parent + 2 new sub-beats + 1 rename) + Jaime street-brawl merge (renamed survivor → `attack-on-ned-stark-in-the-streets-of-kings-landing`, sibling deleted, edges deduped). New vocab type: `event.deception`. See Session 93 entry.
- **S94 (2026-06-13) infobox merge SHIPPED**: spec v2 → dry-run reproduction gate → apply. 20,614 wiki-infobox rows → 17,006 merged / 1,128 filtered / 1,037 quarantined / 1,356 deduped / 87 corroborations (bucket sum 20,614 ✓). Hygiene fixes folded in (52 slug remaps + 944 typed_by stamps). Backup at `graph/edges/_regrounding/edges-pre-infobox-merge-2026-06-13.jsonl`. See Session 94 entry.
- **Event in-world dating (S101–S102):** **118 `event.*` nodes** carry an `occurred:` block (`ac_year`, optional `ac_year_end` span; signed int = AC/BC; `precision` enum; tier-3 from wiki year-pages) + 29 carry `narrative_first`. Schema in architecture.md §459. S102 closed the tail: 5 spans + `long-night` (null/`relative-only`) dated; **10 mis-promoted year-page nodes deleted** (year-lookup now via `occurred.ac_year`, not year nodes). Ordering edges (`PRECEDES`/`FOLLOWS`) deliberately NOT authored — derived/gated (decision #1).

- **Orchestration/pacer + script consolidation DONE (S98+S99)**: `scripts/pace.py` v1 (backfill+report-only) + telemetry ledger (`working/telemetry/`, 476 work rows + 8 wall events / 9 tracks) + `scripts/worker-template.py` (M1/M2/M4) + `longrun.sh` supervisor (S97). **S99 cleanup:** 30 one-offs/wrappers `git mv`→`scripts/archive/` (32 total); 9 frozen CSVs→`_archive/`; `weirwood graph/resolve/refresh` aliased (+ `scripts/weirwood-refresh.sh`); `scripts/README.md` rewritten as universal index (Class A/B/C/D + provenance, all 124 live + 32 archived covered); design §0 fully BUILT. pytest 1231 pass / 3 documented fails.

**IN FLIGHT**
- (none — S109 work complete, awaiting Matt's commit OK.) **S109 ran a FRESH arc-weighted dip (14 Qs, 7 new probes) — confirmed the track is NOT at a pause (3 new failures) — then built+verified the Tywin's-death arc (Q14, the #1 fumble): double failure (discoverability + 0 causal edges) → both fixed.** Continue prompt `2026-06-18-causal-arc-execution.md` updated with the post-S109 re-ranked queue (still the ONE live prompt).

**NEXT TRACK (S109 → S110)**
- **Dip-driven, do NOT mass-mint.** Fresh-dip re-ranking (`working/session-results/2026-06-19-fresh-arc-dip.md`): **#1 = Q12 Battle-of-the-Blackwater downstream** (cheapest — `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` node EXISTS, 2–3 CAUSES edges to wire); **#2 = Q11 Daenerys / fall-of-Astapor → Slaver's-Bay** (new Essos territory, larger ~3–5 beats; alias gap on `targaryen-campaign-in-slavers-bay`); **#3 = Q5 `robb-weds-jeyne-westerling` upstream** (storming-of-the-Crag beat; extends B1; 1–2 beats); also Q6 Trident inbound CAUSES (1 edge), Q13 Sack-of-Winterfell (extends B2). **Re-run an arc-weighted dip before building each** to confirm demand. Strategy + rubric: `working/causal-arc-strategy-2026-06-18.md`. **Verification (FIRM, Matt):** interpretive/causal edges checked by fresh subagents vs LOCAL cache; Matt gates at policy, not per-edge. (**Sonnet 4.6**)
- Reusable arc-mint machine now proven 8× (RR, Bran, Sack, PW, B1, B2, B3, Tywin): research subagent (dedup + quotes + edge proposal; VERIFY vs `edges.jsonl` not node prose) → orchestrator trims/mints via a `scripts/mint_*_arc.py` script (backup + re-run guard) → **node aliases as natural SPACED phrases, not kebab** (S109 resolver lesson) → targeted index + alias rebuild → fresh-subagent verify (causal `verified_by: pending` until CONFIRM; verifier adjudicates CAUSES/TRIGGERS) → `--causal-chain` smoke test → re-dip.
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
- [ ] **Harvest pass — consume `working/harvest-queue.md`** (NEW S108 2026-06-19, Matt). The deferred-capture ledger collects cheap `chapter:line / kind / note` pointers that any agent drops while already in the text during a dip/research/audit (homeless quotes, food/hospitality, physical descriptions, foreshadowing). A harvest pass reads `status: open` rows, opens each line, attaches to the graph (node `## Quotes`, `object.food` nodes, description fields, edges), and flips rows to `done`. Run when the queue accumulates enough rows to be worth a batched pass — don't run per-row. Convention + push-mechanism: memory `feedback_harvest_queue` + the arc-mint machine (continue prompt). Serves [[project_real_goal_graph_for_agents]] + the food/description-are-first-class value.
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

### Session 109 — Causal-arc: fresh arc-weighted dip → Tywin's-death arc (Q14) (2026-06-19)
**Detail:** worklog entry sufficient (execution session). **Model:** Opus 4.8 orchestrator + 3 Sonnet 4.6 `general-purpose` subagents (1 fresh arc-weighted dip + 1 arc-research + 1 fresh edge-verification). **Commit:** pending Matt's OK.

**Changes made:**
- **Step A — FRESH arc-weighted dip RAN (the handoff's "re-dip FIRST" gate)** (`working/session-results/2026-06-19-fresh-arc-dip.md`). The S108 post-B3 re-dip reused the same 10 questions on an unchanged graph, so instead I posed **14 questions — 5 controls + 2 known partials + 7 genuinely NEW probes** across untouched parts of the saga. Result: **7 correct/stop-short · 4 partial · 3 failed.** All 5 built-arc controls passed (no regressions). The 3 failures were ALL new probes → the track is **NOT at a natural pause**; demand confirmed. **#1 fumble = Q14 Tywin's death** (double failure).
- **Step B — Tywin's-death causal arc MINTED + verified** (the dip's clear #1). It was a *double* failure: (a) the phrase "death of Tywin" resolved to the WRONG node (`tyrion-processes-the-assassination-attempt`, score 1.00) because the assassination node had empty aliases; (b) `assassination-of-tywin-lannister` had ZERO causal edges. **3 new beat-nodes** (`jaime-frees-tyrion-from-the-black-cells` [event.incident], `jaime-reveals-the-truth-of-tysha` [event.incident], `tyrion-kills-shae-in-tywins-bed` [event.death]) + **node repair** of `assassination-of-tywin-lannister` (retyped `event.battle`→`event.assassination` per architecture's canonical example; junk misparsed-infobox `## Edges` prose removed; `occurred: 300 AC` added) + **17 edges** (11 role Tier-1 + **6 causal Tier-2**, all fresh-subagent CONFIRMED). Mint `scripts/mint_tywin_death_arc.py` + verify-stamp `scripts/stamp_tywin_arc_verify.py`; backups `_regrounding/edges-pre-tywin-death-arc-2026-06-19.jsonl` + `…-pre-tywin-verify-stamp-2026-06-19.jsonl`. All quotes ASOS Tyrion XI (`asos-tyrion-11`) + Tyrion X, **every line number spot-checked before minting** (research agent was accurate this time).
- **Causal spine (chain-as-arc, NO umbrella parent):** `trial-of-tyrion-lannister --TRIGGERS--> gregor-confesses-and-kills-oberyn --CAUSES--> jaime-frees-tyrion --CAUSES--> tysha-revelation --CAUSES--> assassination-of-tywin-lannister`; plus the Shae sibling-branch `tysha-revelation --CAUSES--> tyrion-kills-shae` and agency `tysha-revelation --MOTIVATES--> tyrion-lannister`. **`--causal-chain assassination-of-tywin-lannister` now returns a 7-edge upstream chain spanning Sansa's poisoned hairnet → Joffrey's death → trial → Oberyn's death → freeing → Tysha → patricide — connecting the already-built Purple-Wedding arc straight through to Tywin's death.** Agency on role edges (Tyrion AGENT_IN; Tywin VICTIM_IN; Jaime AGENT_IN + Varys COMMANDS_IN the freeing). HARD-STOP held (no edge into war-of-the-five-kings; the pre-existing PART_OF is untouched).
- **Totals:** nodes **8,542 → 8,545** (+3 beats); edges **22,255 → 22,272** (+17); orphans **62 unchanged**; edge types **128** (no new types). All new + repaired nodes natural-phrase discoverable. pytest **1307 pass / 1 documented `cwd-is-tmp` fail**.

**Decisions:**
- **Discoverability fix — non-obvious resolver lesson (reusable):** frontmatter `aliases:` must be **natural SPACED phrases** ("death of Tywin"), NOT kebab slugs ("death-of-tywin"). `normalize()` keeps hyphens, so a kebab alias only matches a kebab query — a user's "death of Tywin" → `death of tywin` never matches `death-of-tywin`. The prior arc nodes (incl. B3's `death-of-robert-baratheon`) used kebab aliases and have the SAME latent weakness; their natural-phrase discoverability came from the node-NAME (spaced), not the aliases. Rewrote all 4 Tywin nodes' aliases spaced. **Baked into the continue prompt's arc-mint machine** so every future arc uses spaced aliases. (Memory `project_node_alias_spaced_phrases`.)
- **Verifier adjudicated edge #1 CAUSES→TRIGGERS** (fresh subagent, per the FIRM verify-not-Matt rule): the trial-by-combat death IS the trial's immediate unmediated decisive act. Borderline vs the S104 "coarse source → CAUSES" rule; deferred to the verifier (no policy violation either way, Tier-2). Edges #2–#6 + node retype + role edges + hard-stop: all CONFIRM/CLEAN.
- **Shae killing modeled as a SIBLING beat** (caused-by the same revelation, NOT causing the patricide — Tysha is the patricide's motive). Avoids granularity-overclaim; verifier concurred.
- **Downstream consequences DEFERRED** (Cersei's regency, Tommen's reign) — those beat-nodes don't exist; a long-distance ASOS→ADWD CAUSES would be "a thesis, not an edge." Logged for the next dip-gated batch.
- **Dip-driven cadence held** — built ONE validating batch (Tywin), re-confirmed Q14 fixed, did NOT mass-mint Q11/Q12. **Harvest-queue 2-dip review done** (Matt's smoke test): 28 open rows, push works, buckets healthy, no split/merge, push stays memory-only; queue now big enough for a batched harvest pass.

### Session 108 — Causal-arc B3: Ned's-downfall arc (Q10 gap) + post-B3 re-dip (2026-06-19)
**Detail:** worklog entry sufficient (execution session). **Model:** Opus 4.8 orchestrator + 3 Sonnet 4.6 `general-purpose` subagents (1 arc-research + 1 fresh edge-verification + 1 graph-only re-dip). **Commit:** pending Matt's OK.

**Changes made:**
- **B3 "Ned's-downfall arc" MINTED + verified** — the re-dip's clearest remaining gap (Q10: `execution-of-eddard-stark` had rich role edges but ZERO upstream causal chain — "what set Ned's execution in motion / who is to blame" returned nothing causal). The arrest cluster already existed densely (`arrest-of-eddard-stark` hub + 3 SUB_BEAT_OF children, all with role edges) + `execution-of-eddard-stark` with full role edges, but carried no causal edges. **3 new beat-nodes** (`death-of-robert-baratheon` [event.assassination — the boar hunt; missing entirely; architecture's canonical `event.assassination` example], `ned-discovers-the-truth-of-joffrey-s-parentage` [event.incident — the ROOT], `ned-confesses-to-treason` [event.incident — forced false confession, SUB_BEAT_OF execution]) + **14 edges** (9 role/structural + **5 causal Tier-2**, all fresh-subagent CONFIRMED). Mint script `scripts/mint_b3_ned_downfall_arc.py`; backups `_regrounding/edges-pre-b3-ned-downfall-arc-2026-06-19.jsonl` + `…-pre-b3-verify-stamp-2026-06-19.jsonl`.
- **Causal spine (all Tier-2):** `ned-discovers-the-truth-of-joffrey-s-parentage --MOTIVATES--> {eddard-stark, cersei-lannister}` (root motivations); `death-of-robert-baratheon --CAUSES--> arrest-of-eddard-stark --CAUSES--> execution-of-eddard-stark`; `ned-confesses-to-treason --TRIGGERS--> execution-of-eddard-stark`. **Agency-collapse handled on role edges, not collapsed arrows:** Robert's death = Lancel AGENT_IN (strongwine) + Cersei COMMANDS_IN (Tier-2); Littlefinger's betrayal = **additive** `petyr-baelish COMMANDS_IN gold-cloaks-betray-ned` (Tier-2 — the beat previously credited only Cersei; the `petyr-baelish BETRAYS eddard-stark` dyad ALREADY EXISTED and was NOT re-minted); Joffrey's choice = pre-existing `joffrey-baratheon COMMANDS_IN execution-of-eddard-stark`. HARD-STOP: no edge into war-of-the-five-kings.
- **Totals:** nodes **8,539 → 8,542** (+3 beats); edges **22,241 → 22,255** (+14); orphans **62 unchanged**; edge types **128** (no new types). All 3 new beats natural-phrase discoverable (resolver: "death of Robert Baratheon"/"the boar hunt"/"Ned discovers Joffrey is a bastard"/"Ned confesses to treason" all resolve). pytest **1307 pass / 1 documented `cwd-is-tmp` fail**.
- **Capture-quotes-during-research rule applied** (memory `feedback_capture_quotes_during_research`): while in the AGOT chapters for B3, attached 2 incidental load-bearing quotes that lacked a home — Littlefinger's bribe-setup + the knife-to-chin betrayal (added a `## Quotes` block to the thin Plate-3 stub `gold-cloaks-betray-ned`), and Varys's "or he could bring you Sansa's head" coercion (the *why* of the confession → `ned-confesses-to-treason` `## Quotes`). Node-file enrichment only, no edge-structure change.
- **NEW deferred-capture mechanism: `working/harvest-queue.md`** (Matt-directed). A cheap append-only ledger: any agent already reading a passage (dip/research/audit) drops one-line `book / chapter:line / kind / note` pointers to *notable-but-not-task* finds (homeless quotes, food/hospitality, character appearance, place/object description, foreshadowing) — POINT don't extract; a later **harvest pass** (NEW MEDIUM backlog item) batches them into the graph. Saves context: the expensive part (slug-resolve/dedup/mint) moves off the in-passage agent. `kind` enum kept as a deliberate *projection* of the architecture node/edge taxonomy (anti-shadow-vocab); `description` split into `appearance`/`place`/`object` per Matt. Reliability = **push** (canonical paste-snippet lives in the file; orchestrator pastes it into every text-reading subagent — they don't load CLAUDE.md) + memory `feedback_harvest_queue` + the arc-mint machine (continue-prompt steps 1+5+6). Seeded with 6 real S108 finds.
- **Post-B3 re-dip RAN** (`working/session-results/2026-06-19-post-b3-redip.md`, graph-only agent, graded vs local cache): **Q10 partial → CORRECT** (`--causal-chain execution-of-eddard-stark` returns the 3-edge upstream chain; blame distributed across Joffrey/Littlefinger/Cersei/Lancel role edges + the discovery's MOTIVATES roots) AND **Q8 partial → CORRECT** (first re-dip to measure the post-B2 graph — `greyjoy-rebellion CAUSES theon-greyjoy-taken-as-ward` traversable). 8 correct / 1 policy-stop-short (Q6) / 2 partial (Q3 Trident-upstream; Q7 re-graded partial on a *strict* reading — the dip agent flagged it as grading-strictness, NOT graph regression: B1 structure unchanged).

**Decisions:**
- **`event.assassination` for `death-of-robert-baratheon`** (not the research agent's suggested `event.death`, which is NOT a schema type) — the architecture type table literally lists "Death of Robert I via boar hunt" as the canonical `event.assassination` example; the weaponized-accident (Cersei's strongwine via Lancel) is exactly what the type covers. Fresh verifier concurred.
- **Slug discipline (verified vs `edges.jsonl`, not node prose):** used `robert-baratheon` (58 AGOT in-saga edges) for the death beat, NOT the `robert-i-baratheon` wiki/historical dup; caught the pre-existing `petyr-baelish BETRAYS eddard-stark` dyad (avoided a re-mint). The research subagent's quotes were all accurate this time (spot-checked every load-bearing line number before minting).
- **Dip-driven cadence held** — B3 was the richest remaining gap (Q10); now closed. Re-ranking from the post-B3 re-dip (do NOT mass-mint): #1 = Q7 `robb-weds-jeyne-westerling` upstream refinement (why Robb married Jeyne — extends B1); #2 = Q3 Trident inbound CAUSES; #3 = execution-of-eddard-stark downstream (lower priority — the asked facet is covered).
- **Harvest-queue is an *affordance*, not auto-magic** (Matt corrected the framing): it only becomes opportunistic "Pass 0.5" extraction IF the snippet keeps getting pasted AND harvest passes get run; the markdown file is inert (a destination + a copy-source), memory is the propagation channel. **Decision: smoke-test the buckets over the next ~2 dips, keep the push memory-only for now** — don't promote to CLAUDE.md/hook or re-cut buckets until real rows show what holds (review gate written into the file + memory). The `kind` buckets "sound like entities" because 7 of 9 *are* the node/edge taxonomy viewed coarsely; `quote`+`appearance` are the attach-to-existing (evidence/attribute) exceptions.

### Session 107 — Arc-weighted dip → B1 Red Wedding upstream arc (Tier-B, dip-gated) (2026-06-19)
**Detail:** worklog entry sufficient (execution session). **Model:** Opus 4.8 orchestrator + 3 Sonnet 4.6 `general-purpose` subagents (1 dip + 1 arc-research + 1 fresh edge-verification). **Commit:** pending Matt's OK.

**Changes made:**
- **Step A — arc-weighted Mode-3 dip RAN** (10 consequence/"what-set-X-in-motion" questions, graph-only agent, graded vs local cache). Result **5 correct / 3 partial / 2 failed** (up from 4/10 in the S96 dip). **All four shipped arcs validated** (RR/Bran/Sack/Purple-Wedding answer Q1/Q2/Q4/Q5/Q9 correctly; the Bran arc answers Q1+Q5 from one chain). Results: `working/session-results/2026-06-19-arc-weighted-dip.md`. **Two hard failures = the re-ranking signal:** Q7 (Red Wedding had ZERO upstream causal edges) → **B1**; Q6 (war-of-five-kings causal-dark) → **NOT a gap: hard-stop policy says never assert `X CAUSES war-of-five-kings`** (overruled the dip agent's attach-sparks suggestion; WO5K staying causal-dark is correct-by-policy).
- **Step B — B1 "Red Wedding upstream" arc MINTED + verified** (the dip's clearest fumble, Q7). **5 new beat-nodes** (`catelyn-releases-jaime-lannister` [event.incident], `karstark-murders-prisoners-at-riverrun` [event.assassination], `execution-of-rickard-karstark` [event.execution], `robb-weds-jeyne-westerling` [event.wedding], `red-wedding-conspiracy` [event.conspiracy]) + enriched the thin `robb-is-killed` Plate-3 stub. **21 edges** (16 role Tier-1 + **5 causal Tier-2**, all fresh-subagent CONFIRMED). Modeled as **two parallel chains** (source-confirmed parallel, not sequential): *Catelyn frees Jaime → CAUSES → Karstark murders → CAUSES → Rickard's execution* and *Robb weds Jeyne → TRIGGERS → Red Wedding conspiracy → CAUSES → red-wedding / robb-is-killed*. Mint script `scripts/mint_b1_red_wedding_arc.py`; backups `_regrounding/edges-pre-b1-red-wedding-arc-2026-06-19.jsonl` + `…-pre-b1-verify-stamp-2026-06-19.jsonl`.
- **Step B (cont) — B2 "Greyjoy→Theon-ward" arc MINTED + verified** (the re-dip's Q8 partial; small quick-win). 1 new beat-node `theon-greyjoy-taken-as-ward` (event.incident) + **5 edges** (4 role + 1 causal Tier-2: `greyjoy-rebellion CAUSES theon-greyjoy-taken-as-ward`, fresh-subagent CONFIRMED). Hard-stop at the wardship (no edge to Theon's ACOK invasion). Reused the existing `theon-greyjoy WARD_OF eddard-stark` dyad (not re-minted). Mint script `scripts/mint_b2_greyjoy_theon_arc.py`; backup `_regrounding/edges-pre-b2-greyjoy-theon-arc-2026-06-19.jsonl`.
- **Totals (B1+B2):** nodes **8,533 → 8,539** (+6 beats); edges **22,215 → 22,241** (+26); orphans **62 unchanged**; edge types **128** (no new types). All new beats natural-phrase discoverable (resolver ≥1.00 — Track-7 gap stays closed). `--causal-chain red-wedding`/`robb-is-killed` (Q7) + `--causal-chain greyjoy-rebellion` (Q8) now return their chains. pytest **1307 pass / 1 documented `cwd-is-tmp` fail**.

**Decisions:**
- **B1 built, B2 deferred.** Dip re-ranked Tier B: B1 (Red Wedding upstream) is the unambiguous fumble (Q7 failed); B2 (Greyjoy→Theon-as-ward) was only *partial* (Q8 — the `theon-greyjoy WARD_OF eddard-stark` dyad already answers the core fact), so per dip-driven cadence it waits for a future dip to show genuine fumbling.
- **`event.conspiracy` beat is consistent with chain-as-arc.** `red-wedding-conspiracy` is wired CAUSALLY into `red-wedding` (not as a SUB_BEAT_OF umbrella parent); the type is sanctioned (7 prior nodes, architecture cites "Grand Northern Conspiracy"). The S105/S106 supersession was about conspiracy-as-containment-parent, not causal conspiracy beats. It also IS the agency-collapse fix — carries the conspirators' decisions as role edges (Walder COMMANDS_IN, Roose AGENT_IN, Tywin COMMANDS_IN-Tier-2) instead of a blunt event→event arrow.
- **Discipline held end-to-end:** pre-mint dedup (4 reuse / 6 skip — caught `plot-to-free-jaime-lannister`=Tyrion's ACOK plot ≠ Catelyn's release; reused the existing Roose-Walda wedding + red-wedding hub + robb-is-killed). Quote verification caught the research agent's mis-cited confession (acok-catelyn-07→asos-catelyn-01) + 2 wrong slugs (`crag`, `brienne-tarth`) before minting. Hard-stop confirmed (no edge to WO5K). Causal Tier-2, role Tier-1.

**Post-B1 verification re-dip (same session, S107):** re-ran the 10-question arc dip on the post-B1 graph → **6 correct / 3 partial / 0 failed** (was 5/3/2). **Q7 confirmed FIXED** (`--causal-chain red-wedding` returns the upstream chain); Q6 correctly re-graded correct-to-stop-short (WO5K hard-stop policy, not a failure). Results: `working/session-results/2026-06-19-arc-weighted-redip.md`. Re-ranking: Q8 (Greyjoy→Theon) → **B2 (BUILT, see above)**; **Q10 (Ned's execution has no upstream causal chain — NEW candidate "B3 Ned's downfall arc": Ned discovers Joffrey's bastardy → Littlefinger betrays → arrest → execution; richest remaining gap, NOT built — next session)**.

**Verification discipline note (S107):** the research subagents proposed several facts that were WRONG against `edges.jsonl` and were caught at the orchestrator gate before minting — B1: a mis-cited confession quote + 2 wrong slugs; B2: claimed the WRONG canonical Greyjoy hub (`greyjoys-rebellion`) and claimed the `theon WARD_OF eddard` dyad was absent (it exists). Root cause both times: the agent read the **stale node-file `## Edges` prose** instead of canonical `edges.jsonl`. Lesson reinforced (memory `feedback_verify_dataset_provenance` / `rebuild-derived-artifacts`): always verify hub/edge claims against `edges.jsonl` (or `--neighbors`), never the node-file display bullets.

**What's next (Matt's call):**
- **B3 (Ned's-downfall arc — Q10)** is the richest remaining gap (3–4 beats); build next session, then re-dip. Per dip-driven cadence, one batch then re-dip; don't mass-mint. Strategy: `working/causal-arc-strategy-2026-06-18.md`; continue prompt `progress/continue-prompts/2026-06-18-causal-arc-execution.md`. (**Sonnet 4.6**)
- Small cleanups (→ todos § Small Fixes): **NEW — `greyjoys-rebellion` dup of `greyjoy-rebellion`** (7 stray edges, mistyped `event.battle`; merge into canonical `greyjoy-rebellion`); duplicate `robert-baratheon`/`robert-i-baratheon`; sack hub junk `DEFEATS` infobox edge; `roberts-rebellion`/`dance-of-the-dragons` mistyped `event.battle`.

### Session 106 — Causal-arc execution: `--causal-chain` primitive + Sack-of-KL & Purple-Wedding arcs (2026-06-19)
**Detail:** `history/session-details/session-106.md`
**Model:** Opus 4.8 orchestrator + 1 background `general-purpose` doc agent + 4 `general-purpose` subagents (2 arc-research + 2 fresh edge-verification). **Commit:** this endsession commit.

**Changes made:**
- **Step 1 — `--causal-chain <slug>` traversal primitive SHIPPED** in `scripts/graph-query.py` (walks CAUSES/TRIGGERS/MOTIVATES transitively, both directions; PRECEDES deliberately excluded as pure-chronology). +10 tests (`tests/test_graph_query_edges.py`). The Track-7 prerequisite that makes causal arcs queryable from any beat — and what made the chain-as-arc decision real ("show me the whole arc" without an umbrella node).
- **NEW `reference/narrative-arc-glossary.md`** (~28 terms, 5 sections) — data-model/method companion to `glossary.md` (process vocab) + `architecture.md` (schema). Written by a background agent.
- **Sack of King's Landing arc** — 4 new beat nodes (`pycelle-opens-the-gates-of-kings-landing` [event.deception], `aerys-commands-the-city-burned` [event.incident], `slaying-of-aerys-ii-the-kingslaying` [event.assassination], `murder-of-elia-martell-and-rhaegars-children` [event.assassination]) + **21 edges** (14 role Tier-1 + 4 SUB_BEAT_OF + 3 causal Tier-2). Mint script `scripts/mint_sack_kl_arc.py`; backup `_regrounding/edges-pre-sack-kl-arc-2026-06-19.jsonl`.
- **Purple Wedding arc** — 4 new beat nodes (`sansa-receives-the-poisoned-hairnet` [event.deception], `tyrion-accused-of-poisoning-joffrey` [event.incident], `trial-of-tyrion-lannister` [event.trial], `littlefinger-smuggles-sansa-out-of-kings-landing` [event.deception]) + **20 edges** (14 role + 3 SUB_BEAT_OF + 3 causal Tier-2). Mint script `scripts/mint_purple_wedding_arc.py`; backup `_regrounding/edges-pre-purple-wedding-arc-2026-06-19.jsonl`.
- **Totals:** nodes **8,525 → 8,533** (+8 beats); edges **22,174 → 22,215** (+41); orphans **62 unchanged**; edge types **128** (no new types); **0 pending** verified_by (all 6 causal edges fresh-subagent CONFIRMED). pytest **1307 pass / 1 documented `cwd-is-tmp` fail**.

**Decisions:**
- **Parent-node rec ratified by Matt → chain-as-arc, NO `event.arc` umbrella nodes** (the `--causal-chain` primitive delivers the whole-arc query; supersedes the umbrella-vs-chain fork in the parked arc-wave1 prompt).
- **Scope = 2 Tier-A arcs as one validating batch** (Matt), NOT a minting fleet — a fleet was considered and rejected as wrong-shaped (arc-minting is low-volume + judgment-heavy + write-conflicting; the agency-collapse check and pre-mint dedup don't parallelize). **D&E noted as main-arc in priority** (Bloodraven-in-the-flesh seeds theory anchors); it stays after in-saga arcs only because its chapters aren't Pass-1-extracted yet.
- **Discipline held end-to-end:** pre-mint dedup gate caught 2 real collisions (`fall-of-kings-landing` = the Dance-era fall, kept distinct; the existing flat role-layer on the sack hub + the existing Littlefinger/Olenna conspiracy on the death node — NOT duplicated). Agency-collapse modeled (Tywin COMMANDS_IN vs Gregor/Amory AGENT_IN; PW whodunnit = zero `tyrion POISONS joffrey`, Tyrion VICTIM_IN only). Causal edges Tier-2-capped; role Tier-1. All 8 beats natural-phrase discoverable (closes the S105 Track-7 gap). Both fresh verifiers returned ALL-CONFIRM.

**What's next:**
- → **Per the strategy's dip-driven cadence: re-run an arc-weighted Mode-3 dip before committing Tier B** (Catelyn-frees-Jaime→Red-Wedding-feed; Greyjoy→Theon-hostage→Northern-invasion). Don't mass-mint. Strategy: `working/causal-arc-strategy-2026-06-18.md`; continue prompt `progress/continue-prompts/2026-06-18-causal-arc-execution.md` (Step 1 done; Step 2 ongoing, dip-gated). (**Sonnet 4.6**)
- Small cleanups surfaced by verifiers (→ todos § Small Fixes): duplicate `robert-baratheon` vs `robert-i-baratheon` node; sack hub's junk `DEFEATS: Elia of Dorne` infobox edge.

### Session 105 — Causal-arc scaling strategy + Bran's-fall smoke test #2 + advisory board (2026-06-18)
**Detail:** `history/session-details/session-105.md`
**Model:** Opus 4.8 (1M context) orchestrator + 5 Sonnet 4.6 `general-purpose` subagents (2 edge-verification + 4-lens advisory board). **Commit:** this endsession commit.

**Changes made:**
- **NEW `working/causal-arc-strategy-2026-06-18.md`** — the causal/narrative-arc scaling plan (rubric + prioritized arc list + cost model + 7 policy Qs + the smoke-test analysis + advisory-board outcome + the agency-collapse lesson). This is the deliverable of the continue prompt.
- **Built the "Bran's fall" causal arc (smoke test #2)** — `edges.jsonl` **22,157 → 22,174**, nodes 8,521 → **8,525**, edge types **127 → 128** (`MOTIVATES` now live). Chain: `bran-witnesses-jaime-and-cersei →TRIGGERS→ jaime-pushes-bran-from-the-tower →CAUSES→ bran-s-direwolf-kills-the-assassin →CAUSES→ littlefinger-names-the-dagger-as-tyrion-s →CAUSES→ catelyn-seizes-the-moment-and-arrests-tyrion →CAUSES→ gregor-raids-the-riverlands` (HARD STOP, no edge to WO5K). Plus role edges on all new beats + `capture MOTIVATES tywin` + `petyr DECEIVES catelyn`. 5 new nodes minted (`bran-witnesses…`, `jaime-pushes…`, `littlefinger-names-the-dagger…` [event.deception], `gregor-raids-the-riverlands` [event.incident]; 1 dup `catelyn-captures-tyrion-at-the-crossroads-inn` minted-then-deleted). 2 pre-existing beats enriched (`bran-s-direwolf-kills-the-assassin`, `catelyn-seizes-the-moment-and-arrests-tyrion`). All causal edges Tier-2 + fresh-subagent-verified; role edges Tier-1.
- Backups: `_regrounding/edges-pre-bran-arc-2026-06-18.jsonl`, `…-littlefinger-fix-2026-06-18.jsonl`. Targeted index builds (`--slug`) + alias rebuild. 62 orphans unchanged; pytest 1297 pass / 1 documented `cwd-is-tmp` fail.

**Decisions:**
- Session started as pure-analysis (per continue prompt); Matt expanded scope to a live smoke test + a 4-lens advisory board (narrative-craft / graph-modeling / canon / skeptic). **Parent-node recommendation (awaits Matt's ratification): causal-chain-as-arc, NO umbrella parent nodes** — deliver "show me the whole arc" via a `--causal-chain` traversal primitive, not a parent hub (dissolves the multi-parent-ownership trap; supersedes the umbrella-vs-chain fork in the parked arc-wave1 prompt). **Tier policy:** causal edges capped Tier-2 (interpretive). **Three reusable lessons banked:** (1) **pre-mint dedup lookup** is mandatory (a dup was minted this session); (2) **agency-collapse check** — before `A CAUSES B`, model the human decision between them (insert a beat node OR `MOTIVATES`→actor + COMMANDS_IN); (3) cost model is "patchwork mint," not "pure wiring."

**What's next:**
- → **Matt ratifies the parent-node rec**, then: build the `--causal-chain` directed-traversal primitive (Track 7 prerequisite), then run the first Tier-A arc batch (Sack of KL, Purple Wedding) dip-gated. Continue: `progress/continue-prompts/2026-06-18-causal-arc-execution.md`.

> **Archive map** (`history/worklog-archives/`, 5 entries per file; per-session pointer lines collapsed to this map 2026-06-11):
> archive022 = S102–S104 (FILLING, 3/5) · archive021 = S97–S101 (FULL) · archive020 = S92–96 · archive019 = S87–S91 · archive018 = S83(×2: /tmp-paths + Plates 0-2)–S86 · archive017 = S78–82 · archive016 = S73–77 · archive015 = S68–72
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
