# Worklog Archive 016

> Archived Session Log entries (oldest-first within this file). Each archive holds 5 entries.
> Sessions: 73, 74, 75, 76, 77 (5/5 — FULL).

---

### Session 75 — Graph-exercise follow-ups: conflict-pair audit + graph-query tool; enrichment un-shelved (2026-05-26)

**Model:** Opus 4.7 (orchestrator) + script-builder (Sonnet 4.6) ×2 parallel. **Detail:** `history/session-details/session-075.md`. **Session-results:** `working/session-results/2026-05-26-graph-followups.md`. **Commit:** this endsession commit.

**Changes made (all $0/deterministic, no LLM):**
- NEW `scripts/graph-conflict-pairs.py` (+`tests/test_graph_conflict_pairs.py`, 29 green) — read-only audit; flags entity pairs with semantically incompatible co-occurring edge types into a REVIEW QUEUE (does NOT modify `edges.jsonl`). Output `working/wiki/data/graph-conflict-pairs.{md,jsonl}`. **1,978 pairs → 32 flagged** (14 same-direction / 11 opposite / 7 both; DISTRUSTS×TRUSTS 15, ALLIES_WITH×OPPOSES 12, LOVES×HATES 5, PROTECTS×ASSAULTS 3).
- EXTENDED `scripts/graph-query.py` — already existed from S39 (node-inspection over node `## Edges` + `cross-references.jsonl`); preserved all S39 modes, added `--neighbors`/`--path`/`--health`/`--edges` over canonical `edges.jsonl`. `tests/test_graph_query_edges.py` (29 green); full suite **920 green**, no regressions.
- `--health`: 8,299 node files · 3,811 edges · 898 endpoints · **0 orphans** · 105 edge types (GUEST_OF 404, OPPOSES 265, SERVES 255 lead); degree leaders jon-snow 317, tyrion 315, dany 248, cersei 229, arya 198.

**Decisions:** (1) **Enrichment UN-SHELVED** — Matt confirmed he DOES want enrichment; softens the S74 "NO-GO" to a *deferral*. Step by step, **Events is the next surface**, gated behind the precision changes landing first (the conflict-pair cleanup + kept v5 precision rules). Memory `project_enrichment_wanted_events_next`. (2) **Temporal flagging endorsed** ("when an edge applies — shrewd"). Verified it's largely DETERMINISTIC: all 3,811 edges carry `evidence_book`+`evidence_chapter`; chapter frontmatter has `chapter_number` → a `(book_order, chapter_number)` key is derivable at $0. The 32 conflicts are mostly *temporal arcs* (Dany→Jorah TRUSTS@AGOT+DISTRUSTS@ADWD), not errors → real fix is temporal scoping, not deletion. (3) `graph-query.py` collision surfaced before touching it (S74 prompt assumed the file didn't exist) → extended, not overwritten.

**What's next:** → `progress/continue-prompts/2026-05-26-stage4-events-enrichment.md` (**edge enrichment with Events**, precision-gated). Folds in the precision precursors: review/apply the 32-pair true mis-attributions + build deterministic temporal scoping + keep v5 rules; THEN a gated Events pass. NOT launched this session (Matt's call to end + queue). DO NOT run the ~$270 Events bulk blind (failed 75% gate).

---

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

---

### Session 76 — Events enrichment launched (Sonnet); flush-fix + rate-limit wall; ASSAULTS mis-type caught (2026-05-27)

**Model:** Opus 4.7 (orchestrator) + script-builder (Sonnet 4.6) ×2. **Detail:** `history/session-details/session-076.md`. **Commit:** uncommitted at endsession (Matt to confirm).

**Changes made (Step 1 precursors + Events run, all staging — `graph/edges/edges.jsonl` UNTOUCHED):**
- NEW `scripts/stage4-edge-temporal-scope.py` (+58 tests; 999 suite green): annotates all 3,811 edges with `(book_order, chapter_number)`; temporal-aware conflict re-audit → **`--window chapter`: 31/32 flagged pairs are temporal arcs, 1 true same-window** (`cersei↔tyrion`); `--window book`: 24/8. Outputs `working/wiki/data/edges-temporal-scoped.jsonl` + `graph-conflict-pairs-temporal.{md,jsonl}`.
- `scripts/stage4-tail-classifier.py` (+tests, **1011 green**): NEW `--flush-every N` (default 5; **cursor-based delta** flush — dodged the append-mode duplication trap) + SIGINT/SIGTERM flush handler → kill-to-tune is lossless + resumable. Rate-limit/end paths made cursor-safe.
- **Events run (Sonnet, `pass1_events`, 16,572 cands/415 batches):** 75 batches done → **369 typed / 2,631 rejected / 240 classify_failed; 273 unique; $20.81** in `working/wiki/pass2-buckets/pass1-derived/_events-run-20260527/` (gitignored). 5 accuracy checkpoints, **~82-86% strict, zero drift**; vocab lockdown correct even on MANIPULATES/ADVISES/CROWNS_QUEEN_OF_LOVE_AND_BEAUTY. Paused on a shared-account rate-limit wall (~75 batches/5h window; exit 42, partial flushed).
- NEW continue prompt `progress/continue-prompts/2026-05-27-haiku-events-comparison.md`.

**Decisions:** (1) Matt converted his S75 hard 75% gate to a **monitored iterative loop** ("run it, continue even if <75%, tune the prompt every couple batches"); precision held ~82-86% so no tuning was needed. (2) **Conflict-pair review:** only genuine mis-types = the **2 `cersei↔tyrion` LOVES** edges (sarcasm/accusation); `catelyn→tyrion`/`ghost↔tyrion` are real arcs (KEEP). (3) **ASSAULTS bug (Matt-caught):** `ASSAULTS`=sexual only (architecture.md:233); **~22/32 core ASSAULTS are physical → mis-typed, should be `ATTACKS`** (root cause: spine phrase→type map pre-dates the split). v5 Events prompt obeys it (emitted 0 ASSAULTS). (4) **Model for remaining ~82% UNDECIDED** — Sonnet ≈ 2 days of session-blocking 5h-bursts vs Haiku (lighter, untested on current setup) → Haiku comparison queued. (5) **Auto-resume miss:** bare classifier didn't sleep-and-relaunch overnight; use a sleep-until-reset wrapper next time.

**What's next:** → `progress/continue-prompts/2026-05-27-haiku-events-comparison.md` (**Opus 4.7** conductor; Haiku 4.5 worker-under-test) — same-rows Haiku-vs-Sonnet comparison to pick the model, then resume the remaining ~82% with a sleep-until-reset wrapper. **3 gated core-cleanups await Matt's before/after OK:** drop 2 `cersei↔tyrion` LOVES (3,811→3,809); retype ~22 physical `ASSAULTS`→`ATTACKS` (+ fix spine map); merge-time `OWNS→BONDED_TO` for direwolf/dragon targets. None modify `edges.jsonl` without sign-off. Broader track context: `progress/continue-prompts/2026-05-26-stage4-events-enrichment.md` (Step 1 DONE).

---

### Session 77 — Events: model DECIDED (Haiku), candidate slug-fix, paced runner built+hardened, bulk LAUNCHED (2026-05-27)

**Model:** Opus 4.7 (orchestrator) + script-builder (Sonnet 4.6) ×3. **Detail:** `history/session-details/session-077.md`. **Commit:** this endsession commit.

**Changes made:**
- NEW `scripts/stage4-model-run-diff.py` — diffs two classifier runs on the SAME rows (match key `(source,target,chapter,hint_raw)`, NOT `evidence_ref` which only exists on emits). Self-diff = 100%.
- `scripts/stage4-tail-classifier.py`: fixed `--smoke` silently ignored under `--input-dir` (had started a full 415-batch run instead of 600; killed at $0); added `--sleep-between` (chunked, stop-file-aware), `--validate-every`/`--reject-rate-floor` (drift-halt **exit 43**), `STOP_FILE` honoring mid-sleep + between batches. **1072 tests green.**
- `scripts/stage4-pass1-extra-tables.py`: SLUG-FIX — now passes `slug_category` so the S72 title-person rung fires (`lord-tywin`→`tywin-lannister`) + `ENDPOINT_BLOCKLIST` (bastard/dog/four-storms/hunt). Regenerated: pass1_events **16,572→16,502 clean** (5 bad-slug classes →0; 44 `lord-tywin` remapped, 15 dropped). Backup `_extra-tables.pre-slugfix-20260527/`.
- NEW `scripts/stage4-events-bulk-run.sh` — paced auto-resume wrapper; hardened against "sleeps-but-never-restarts" via `sleep_with_stop_check` (pattern from `stage4-haiku-loop.sh`), exit-130(Ctrl-C)-terminal, `MAX_ITER=200`. Runbook `working/runbooks/stage4-events-haiku-bulk.md`. Comparison report `working/session-results/2026-05-27-haiku-vs-sonnet-events.md`.

**Decisions:** **(1) Model = HAIKU** for the full Events run — validated on 2 fresh out-of-sample samples (AGOT 600 ~85%, ACOK 600 ~90% strict; 0 walls; ~$1.8/run) vs Sonnet's 82-86%. Haiku's cost is lower RECALL (acceptable per project values: missing edge recoverable, wrong edge = pollution), not extra pollution. **(2) Fix candidates first** — residual errors in BOTH samples were bad candidate SLUGS (a disambiguation miss that survives the existence-gate AND a merge-time orphan-filter), not model error → fixed before the bulk. **(3) Run = fresh all-Haiku** (single provenance; Sonnet partial `_events-run-20260527/` superseded). New collision classes (cat/wolf/duck/gold/others/dragon/bear) left for merge-time triage (mixed = real refs + a few wrong; some have missing nodes). **(4) Calibration:** precision reads judge EDGE CORRECTNESS as the bar; flag a quote only when it actively fails to support the type (not when merely less-direct).

**What's next:** Events Haiku bulk RUNNING in Matt's iTerm (`_events-haiku-bulk/`, 600s pacing, validate-every 25; ~411 batches, ~3.5 days; auto-resumes walls, hard-stops drift at exit 43). → `progress/continue-prompts/2026-05-27-events-haiku-bulk-monitor.md` (**Opus 4.7** — checkpoint precision reads + completion→merge). Owed: precision spot-read at first/25-batch checkpoint + at completion. Still gated on Matt: 3 core-cleanups (drop 2 cersei↔tyrion LOVES / ~22 ASSAULTS→ATTACKS / merge-time OWNS→BONDED_TO). Merge of Events edges into `graph/edges/edges.jsonl` = separate milestone.
