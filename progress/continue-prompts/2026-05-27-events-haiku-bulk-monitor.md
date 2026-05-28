# Events Haiku bulk — monitor in-flight run, then validate + merge

> **Recommended model:** **Opus 4.7** — the work is judgment (precision spot-reads, drift interpretation, the merge/formalize decision + the 3 gated core-cleanups). Deterministic sub-steps (dedup, validators) can go to script-builder/Sonnet. **The session MAY write** (update the monitor log, fix scripts, stage merge artifacts, write progress notes) — it is NOT restricted to read-only (Matt, 2026-05-28). The ONE hard gate: never modify `graph/edges/edges.jsonl` without Matt's before/after sign-off.
>
> **Trust `worklog.md` over this prompt if they disagree** (CLAUDE.md #9).
> **REFRESHED 2026-05-28 10:26 CDT** (orig written Session 77, 2026-05-27). State below is current as of the refresh.

## What's running (started by Matt in his iTerm, Session 77)
- **Fresh all-Haiku** typing pass over the **16,502 cleaned `pass1_events`** candidate rows (`working/wiki/pass2-buckets/pass1-derived/_extra-tables/`, `candidate_kind=pass1_events`).
- Command (the relaunch Matt is actually running — note 600s, not the worklog's temp-1800s):
  ```
  STAGE4_OUT=.../_events-haiku-bulk STAGE4_SLEEP_BETWEEN=600 STAGE4_VALIDATE_EVERY=25 \
  bash scripts/stage4-events-bulk-run.sh
  ```
- Output: `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk/` (gitignored). Log: `…/_events-haiku-bulk/run.log`. PIDs at refresh: 65068 (wrapper) / 65078 (classifier).
- ~411 batches @ ≤40 rows, 600s between batches. Auto-resumes rate-limit walls (exit 42 → 1h sleep); **hard-stops on drift (exit 43)**; `touch /tmp/stage4-stop` or Ctrl-C stops cleanly + resumable via `--skip-existing`.
- Model = Haiku (`claude-haiku-4-5-20251001`), `prompt_version=v5-precision-rules` (sha `d31ca56c4768`). Pre-run validated **~85% (AGOT) / ~90% (ACOK) strict** across 2 fresh samples. Report: `working/session-results/2026-05-27-haiku-vs-sonnet-events.md`.

## CURRENT STATE @ 2026-05-28 10:26 CDT (read this first — much is already done)
- **Position: batch 92/411 (319 remaining). $11.34 spent, avg $0.122/batch → proj total ~$50, ~$39 + ~2.7 days left.**
- **389 edges on disk** (AGOT 236, ACOK 153; ASOS/AFFC/ADWD still 0 — candidates are book-ordered, later books not yet reached). All `typed_by=haiku`, **0 ASSAULTS** (v5 sexual-only rule holding).
- **Owed early reads = DONE, both clean** (see `working/session-results/2026-05-27-events-haiku-bulk-monitor-log.md`):
  - First-flush human precision read (58 edges): **~93–96% strict.** 2 clear + 2 borderline errors, all the *candidate-slug / over-eager-moment* class (`bran TEACHES joseth-maester` bad slug+reversed; `robb FEARS sansa` = fears-for-not-of; `jaime RESCUES bran` pull-before-push; `bran LOCATED_AT winterfell` read off a name-title), NOT vocab drift.
  - Automated validates @ 25/50/75: reject_rate 0.907/0.908/0.901, unresolved=0, all **OK** (> 0.70 floor). No walls, no drift.
- **So the remaining monitoring is light: occasional spot-checks + the completion read. The run is self-driving with its own exit-43 drift halt — do not anxiously poll.**

## Why ~90% of rows get REJECTED (this is healthy, by design — do not raise it as an alarm)
- `pass1_events` candidates are deliberately **high-recall**: ~one row per event/action line in Pass 1's tables ("Summer and Shaggydog howl", "Bran sees visions"). **Most events are NOT a typed relationship**, so the classifier's job is to reject the non-edges and keep the ~10% that are real edges. The S69 smokes predicted ~90% reject; validate@25/50/75 confirm it (reject_rate ~0.90).
- The rate is further inflated because the **same real pair recurs across many event rows** (siblings, spouses, parent/child) — only ONE needs to type; the redundant rows are rejected **without losing the edge**.
- **Reject-recall spot-check (2026-05-28, 25 random AGOT rejects): ~0 clear missed edges, ~4 borderline (each either already captured from a cleaner row or carrying a group/bad slug like `lhazareen`/`tyroshi`/`royal-fleet`) → unique-edge recall loss well under ~15%.** Acceptable per the Haiku trade (missing edge recoverable; wrong edge = pollution).
- The automated `--validate-every` gate has a reject **FLOOR** (halts if reject_rate <0.70 = over-emitting/drift). There is intentionally **no ceiling** — high reject is expected. Over-rejection is a recall question, judged by the spot-check below, not an automated halt.

## Your job — MONITOR (while it runs)
1. **Read `run.log`.** Healthy: each batch ~90% reject, ~$0.10–0.14, then `sleeping 600s before next batch...`. `[validate@batch N: … reject_rate=.. OK]` prints every 25.
2. **Remaining precision spot-read owed at completion** (the batch-5 + 25/50/75 reads are done — see above). Optional mid-run re-read fine but not required. Method: `python3` over `_events-haiku-bulk/**/*.edges.jsonl`; check `edge_type` vs `evidence_quote`. **Bar = EDGE CORRECTNESS** (is the relationship right?) — do NOT down-flag for a less-than-verbatim quote (Matt's S77 calibration).
3. **If you see `DRIFT HALT (exit 43)`** in the log: the run stopped itself (reject-rate <0.70 or schema break). Inspect `_events-haiku-bulk/` + the run.log validate line; diagnose before any resume.
4. **Sleep change (only if Matt asks):** stop (`touch /tmp/stage4-stop`), wait for clean exit, relaunch SAME command with new `STAGE4_SLEEP_BETWEEN` and the **same `STAGE4_OUT`**. NOTE pacing spreads the SAME token spend over more days — it is NOT a cost lever, only a weekly-usage-rate lever.

## Your job — on COMPLETION (run.log shows the wrapper "finished" with all 411 batches done)
1. **Full validation (BOTH sides — precision AND recall):**
   - **Precision:** total typed/rejected/failed across all 5 books, cumulative reject-rate, total cost; a final ~25-**emit** strict precision read (bar = edge correctness); confirm `typed_by=haiku` throughout.
   - **Reject-recall (false-reject) check — REQUIRED, per Matt (2026-05-28):** pull a random ~25-row sample from the `*.rejected.jsonl` files and judge each: *real missed edge* vs *correctly a non-edge*. Discount pairs whose edge is already captured from a cleaner row (siblings/spouses/parent recur across many event rows) and bad/group slugs (those SHOULD be rejected). **Expectation: unique-edge recall loss < ~15%.** If materially higher, surface it to Matt (it'd suggest the prompt is over-rejecting a recoverable class) — do NOT silently accept. Baseline from S78 (batch ~94): ~0 clear / ~4 borderline of 25.
2. **Slug long-tail triage** (deferred from S77, NOT garbage — mixed): `cat`(62) `wolf`(36) `others`(30) `gold`(24) `dragon`(23) `duck`(23) `bear`(18). `others`=White Walkers is CORRECT; `duck`=Rolly Duckfield + `gold`=City Watch are correct referents with MISSING nodes; `cat/wolf/dragon/bear` are mixed. Decide per-class: drop / remap / create-node — do NOT blanket-drop (loses real edges).
3. **MERGE / FORMALIZE into `graph/edges/edges.jsonl`** — the gated milestone. Sub-steps: dedup (collapse same `(source,target,chapter)`; the pass de-dups within itself but cross-check); apply merge-time `OWNS→BONDED_TO` for direwolf/dragon targets (core-cleanup #3); run the type-contract validator; **before/after edge counts to Matt for sign-off** (do NOT modify `edges.jsonl` without it).

## DO NOT
- Modify `graph/edges/edges.jsonl` without Matt's before/after sign-off.
- Touch the Sonnet baseline `_events-run-20260527/` or the two cmp dirs (`_events-haiku-cmp-20260527/`, `_events-haiku-cmp2-acok-20260527/`).
- Re-run candidate generation (candidates are fixed + clean; backup at `_extra-tables.pre-slugfix-20260527/`).
- Run `/endsession` without explicit permission.
- Restart/kill the run unless Matt asks — it is alive and healthy at the refresh.

## Also gated on Matt (carried from S76 — independent of this run)
3 core-cleanups to `edges.jsonl`, await before/after sign-off: (1) drop 2 `cersei↔tyrion` LOVES mis-types; (2) retype ~22 physical `ASSAULTS`→`ATTACKS` (+ fix the spine phrase→type map; `ASSAULTS`=sexual only, architecture.md:233); (3) merge-time `OWNS→BONDED_TO` (folds into the merge above).

## Watcher note
This run logs to `run.log`, NOT a mission-manifest, so `/watcher` (mission-protocol) does not directly apply. Lightweight monitoring = read `run.log` + the `_events-haiku-bulk/**/*.jsonl` tallies + the monitor log `working/session-results/2026-05-27-events-haiku-bulk-monitor-log.md`. If formal watcher-style monitoring is wanted, wiring the run as a `working/missions/` entry is a small follow-up — not required.
