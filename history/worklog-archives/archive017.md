# Worklog Archive 017

> Archived Session Log entries (oldest-first within this file). Each archive holds 5 entries.
> Sessions: 78 (1/5 — start), 79 (2/5).

---

### Session 78 — Events Haiku bulk: monitor checkpoints (healthy) + continue-prompt refresh (2026-05-28)

**Model:** Opus 4.7 (orchestrator; read + light doc-writes). **Detail:** none (pure monitoring/admin session). **Commit:** this endsession commit.

**Changes made (no code, no graph — doc writes + worklog + hygiene):**
- NEW `working/session-results/2026-05-27-events-haiku-bulk-monitor-log.md` — durable checkpoint log (precision + reject-recall baseline for the completion read).
- REFRESHED `progress/continue-prompts/2026-05-27-events-haiku-bulk-monitor.md` — current state baked in; **relaxed the read-only framing per Matt ("it can write if it needs to"; only `edges.jsonl` is gated)**; added a "why ~90% reject is healthy" section + a **REQUIRED reject-recall (false-reject) step** in the completion validation (Matt's call — expect unique-edge recall loss <~15%).
- Worklog Current State Events line → LAUNCHED + MONITORED HEALTHY.
- HYGIENE: `.claude/scheduled_tasks.lock` (stale per-process lock accidentally committed S76, dead pid) untracked + added to `.gitignore`.

**Monitoring (read-only on the in-flight run — never touched it):**
- Run alive (PIDs 65068/65078), 600s pacing. Matt relaunched the temp-1800s start at 600s himself → the worklog "lower sleep before travel" action item is already done.
- First-flush human precision read (58 edges): **~93–96% strict**; 2 clear + 2 borderline errors, all candidate-slug / over-eager-moment class (`bran TEACHES joseth-maester`, `robb FEARS sansa`, `jaime RESCUES bran`, `bran LOCATED_AT winterfell`), NOT vocab drift. Schema clean (`typed_by=haiku`, 0 ASSAULTS).
- Automated validate@25/50/75 all OK (reject_rate ~0.90, unresolved=0; no walls, no drift).
- **Reject-recall check (Matt flagged "most rows getting rejected"):** ~90% reject is by-design (high-recall candidates × precision filter, inflated by the same real pair recurring across event rows). 25 random rejects → **~0 clear missed edges, ~4 borderline** (each already captured from a cleaner row or a group/bad slug) → **unique-edge recall loss <~15%**, acceptable per the Haiku trade.

**Decisions:** (1) **Pacing is NOT a cost lever** — 600s spreads the SAME ~$50 token spend over ~3 days; it's a weekly-usage-rate lever (splits spend across weeks). Total Haiku run ~$50 vs Sonnet's ~$270 for the same rows. (2) Next session **MAY write** (Matt) — only `edges.jsonl` modification stays gated on before/after sign-off. (3) **Reject-recall is now a required validation dimension** (not just emit-precision) — the high reject rate is healthy, but completion must quantify false-rejects, not assume.

**What's next:** Run self-driving (~2.7 days; exit-43 drift halt guards it). → `progress/continue-prompts/2026-05-27-events-haiku-bulk-monitor.md` (**Opus 4.7**): owed = completion read + slug long-tail triage + MERGE into `edges.jsonl` (gated). Still gated on Matt: 3 core-cleanups (drop 2 `cersei↔tyrion` LOVES / ~22 `ASSAULTS`→`ATTACKS` / merge-time `OWNS→BONDED_TO`).

---

### Session 79 — Events Haiku bulk: parse-error diagnosis + sleep lowered 240→120 for unattended run (2026-05-28)

**Model:** Opus 4.7 (orchestrator; diagnosis + operational doc-writes, no code/graph). **Detail:** none (operational/diagnostic). **Commit:** this endsession commit.

**What happened:** Matt re-launched the Events Haiku bulk himself in iTerm (at 240s, then asked to lower to 120s for the unattended phase before travel). Diagnosed the recurring `[batch N] Parse error: JSON parse error: Expecting value: line 1 column 1 (char 0)` he saw in the log, then stopped the 240s run cleanly and handed back the 120s launch command (Matt re-launched it himself).

**Parse-error diagnosis (no fix applied — logged as a todo):** the error is Haiku returning non-JSON for a batch. `parse_batch_response` (`stage4-tail-classifier.py:645`) does `json.loads()` on the model's `result` text; `Expecting value: line 1 column 1 (char 0)` = the text didn't begin with a JSON value (prose/preamble/empty). On parse failure the classifier fails the **whole batch all-or-nothing** (`:1185`) → all 40 rows → `*.classify_failed.jsonl`. **Rare** (2 parse errors in ~700 batches across both runs) BUT the failed block **recurs**: `count_remaining` + `--skip-existing` treat only `edges`+`rejected` as done — **`classify_failed` is NOT a skip-key** (`stage4-events-bulk-run.sh` count_remaining; classifier `:1090` load_existing_keys), so the same ~40 acok rows (joffrey↔mandon-moore etc.) get re-fed as batch 1 every run and fail again. Non-fatal, non-degrading (batches 2+ all `failed=0`); just never self-resolves.

**Sleep change mechanics (confirmed):** no live knob — `--sleep-between` is baked into the running process. Lowering it = `touch $HOME/source/claude-cwd/tmp/stage4-stop` (classifier checks the stop-file in 30s chunks during its inter-batch sleep, `:2009`, and after each batch, `:2026`) → wait for clean exit (wrapper sees exit 130, `rm -f` the stop-file) → relaunch SAME `STAGE4_OUT` with new `STAGE4_SLEEP_BETWEEN` (`--skip-existing` resumes losslessly). `setsid` is NOT on macOS (use `nohup`/iTerm for detach). Verified resume: relaunch skipped 5,239 already-done rows, 11,263 remaining / 282 batches, same `v5-precision-rules` sha — genuine resume, not restart.

**Decisions:** (1) **Sleep = 120s** for the unattended phase (Matt's call; the S78 "lower to 600/300 before travel" action item is now DONE at 120s). Pacing is a weekly-usage-rate lever, not a cost lever — same ~$50 total spend, finishes faster. (2) Parse-fail block left as a logged loose end, not fixed live (run is healthy; fix is a one-liner for a later session).

**What's next:** Run self-driving in Matt's iTerm at 120s (drift-halt exit 43 guards it). → `progress/continue-prompts/2026-05-27-events-haiku-bulk-monitor.md` (**Opus 4.7**): completion read (precision + reject-recall) + slug long-tail triage + MERGE into `edges.jsonl` (gated). New loose end → `working/todos.md` "Stage 4" section: make `classify_failed` a skip-key OR add a one-shot batch retry so the recurring ~40-row parse-fail block resolves. Still gated on Matt: 3 core-cleanups.

### Session 80 — Events Haiku bulk DONE: wrapper bug fixed, run analyzed, v2.0 promotion chain authored (2026-05-31)

**Model:** Opus 4.7 (analysis + planning + prompt authoring; one Python bugfix to a wrapper script). **Detail:** `history/session-details/session-080.md`. **Commit:** this endsession commit.

**Changes made:**
- `scripts/stage4-events-bulk-run.sh::count_remaining` — fixed wrapper false-alarm: total was counted as raw rows, done as deduped `(src,tgt,chapter)` keys; the delta = duplicate input keys, NOT real remaining work. Patched so both sides count the same way. Verified: returns 0 on current state.
- NEW `working/audits/events-haiku-bulk-2026-05-29/analysis.md` — full Events bulk run analysis (completeness, cost, edge-type distribution, schema-field health, v1.3 overlap).
- NEW `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/` — 7-step self-contained prompt chain to promote Events to `graph/edges/edges.jsonl` v2.0 (README + 7 step prompts).

**Events bulk RESULT:** **complete and clean.** All 16,502 candidate rows accounted for: **1,617 typed edges** + 14,884 rejected + 1 needs-qualifier. Single prompt_sha (`d31ca56c4768`), single model (haiku), 0 conform_violations, 0 classify_failed. Tier-1 256 / tier-2 1,342 / tier-3 19 (real calibration, unlike v1's all-tier-1). 99.6% verbatim quotes. Vs v1.3: 444 pair-overlaps, 289 triple-overlaps, **988 net-new triples** if promoted — dominated by event-shaped predicates (TRAVELS_WITH/TO 242, LOCATED_AT 90, COMMANDS 121, REVEALS_TO 66, ATTACKS 43, DREAMS_OF 36) that the v1 relationship-spine doesn't carry. Schema gap noted: rejected rows have no `reject_reason` field — fix-later, in Dialogue prep.

**Decisions (Matt confirmed all three up front):** (1) **Full re-merge** (one consolidated v2 jsonl, not additive overlay). (2) **Ship Events-only as v2.0 now**; Dialogue lands as v2.1 via a parallel chain spawned by step 7. (3) **`reject_reason` schema fix deferred to Dialogue prep** (not blocking v2.0). Chain shape: 7 self-contained prompts, each declaring prerequisite + deliverable + gate + recommended model. Mechanical steps (contracts, resolver) → Sonnet 4.6; judgment steps (drift audit, precision audit, sensitive write) → Opus 4.7. Hard rule carried: never modify `edges.jsonl` without Matt's before/after sign-off.

**What's next:** Begin the chain. → `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/01-drift-audit.md` (**Sonnet 4.6 + Opus 4.7**) — cross-model audit on a stratified ~50-row sample; gates v2.0 promotion at ≥70% triple / ≥85% pair agreement. Stale: `progress/continue-prompts/2026-05-27-events-haiku-bulk-monitor.md` (the in-flight run it monitored is now complete; obligations absorbed by the new chain) — to archive.

### Session 81 — Events Haiku bulk drift audit → NO-GO (borderline); fresh-eyes corrected the framing (2026-05-31 → 2026-06-01)

**Model:** Opus 4.7 (orchestrator + audit-script author) + general-purpose subagent (cold fresh-eyes review) + Sonnet 4.6 (judge via `claude -p` cwd=/tmp). **Detail:** `history/session-details/session-081.md`. **Commit:** this endsession commit.

**Changes made:**
- NEW `scripts/events-drift-audit.py` (sha `576cc815649c`, 327 lines, throwaway single-purpose) — reuses canonical `render_classify_prompt` / `invoke_claude` / `parse_batch_response` / `align_batch_output` from `stage4-tail-classifier.py` for byte-identical prompt parity with Haiku's bulk run; custom stratified sampler (≥3 of each of 6 named structural types; remainder proportional by book); seed=531; `--dry-run` default, `--apply` required for spend.
- NEW `working/audits/events-haiku-bulk-2026-05-29/{audit-sample-50.jsonl, audit-sample-50-judged.jsonl, cross-model-audit.md}` — all carry metadata header (judge_model, judge_cwd, sample_seed, prompt_sha, script_sha, timestamps, judged_count, cost). cross-model-audit.md amended with fresh-eyes banner at top.
- NEW `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/step-01-status.md` (amended with No-Go + fresh-eyes correction).
- NEW `progress/continue-prompts/2026-06-01-events-bulk-escalation-pick.md` — next-session entry point, lists 5 escalation paths.

**Audit result:** Stratified 50-row sample (seed=531); Sonnet 4.6 judge, $0.93 total. Triple-level **48 %** (24/50; floor 70 %), pair-level **56 %** (28/50; floor 85 %). 22/50 Haiku emits rejected by Sonnet. Named-type breakdown: TRAVELS_TO 17 % (1/6), TRAVELS_WITH 0 % (0/4), LOCATED_AT 20 % (1/5), COMMANDS 50 %, SERVES 67 %, REVEALS_TO 67 %. Prompt SHA byte-identical to Haiku bulk run (`d31ca56c4768`). Methodology bugs: **none** (verified by fresh-eyes subagent).

**Fresh-eyes pressure-test corrected the framing** (Matt didn't trust the 48 % number; subagent was instructed to read rules cold, then cold-judge the 22 REJECTs, then locate the smoke session):
- ~11 of 22 REJECTs **are clear Haiku drift** (Rule 4a hint-as-evidence, V5-R2 quote-doesn't-support-both-endpoints, Rule 12 co-presence) — Sonnet correct.
- **~3-4 are clear Sonnet over-rejections** (judge_idx 2 Edmure TRAVELS_WITH Lymond "on the march"; 6 Jaime TRAVELS_TO Harrenhal "when he came to Harrenhal"; 14 Ramsay REVEALS_TO Roose dispatched riders; 16 Haldon TRAVELS_WITH Duck co-riders).
- ~7-8 genuinely ambiguous, most lean V5-defensible-reject.
- **The audit's S69 smoke citation was WRONG** — actual session is **S77**, and S77 measured *hand-read precision on fresh candidates* (Matt's eye), NOT *Sonnet-judges-Haiku-emit on stratified emits-only*. Different metric on different sample shape. The apparent contradiction between the smoke (~85-90 %) and this audit (48 %) is **measurement-shape, not drift**.
- Adjusted triple agreement crediting all over-rejections + all ambiguous ≈ 56-70 % — at or below the 70 % gate.

**Decisions:** (1) **No-Go stands but is borderline**, not catastrophic. Promoting `_events-haiku-bulk/` as v2.0 would inject systematic noise into the structural-edge types (TRAVELS_TO/WITH/LOCATED_AT), where Haiku's hint-as-evidence failure mode concentrates. (2) **The 7-step promotion chain is halted at step 1** until Matt picks an escalation path. (3) **Audit script is THROWAWAY** — single-purpose, not generalized into a framework (per chain spec); reused canonical prompt code for parity. (4) **Cost discipline observed** — `--dry-run` default, `--apply` only after explicit Matt-go ($0.93 total spend).

**What's next:** Matt picks one of the 5 escalation paths in `cross-model-audit.md §6`: (A) re-run on Sonnet (~$340), (B) promote long-tail-only, (C) Sonnet-filter named-type rows only (~$2-5, **audit's recommendation**), (D) tighten Haiku prompt to v6 + re-run, (E) abandon Events for v2.0; wait for Dialogue. → `progress/continue-prompts/2026-06-01-events-bulk-escalation-pick.md` (**Opus 4.7** for the pick, then Sonnet 4.6 for whatever mechanical work follows). Stale: the 7 step prompts at `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/02-06-*.md` likely need rewrites once path is picked, or supersede the chain if (E). Still gated on Matt: 3 core-cleanups (drop 2 `cersei↔tyrion` LOVES; ~22 ASSAULTS→ATTACKS; merge-time OWNS→BONDED_TO).


---
