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
