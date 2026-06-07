# Plate 3 — RESUME the reification full sweep

> **Recommended model:** Opus 4.7 — this session LEADS with a reasoning task: diagnose + fix the `--all` selective-gate bug (see "⚠️ BEFORE YOU RUN" below — the overnight `--all` minted narrative micro-beat hubs because the D8/Q1 gate wasn't enforced in that path; the dry-run stub bypassed it, so it's UNVERIFIED), then make the calibration cost call. The per-event role typing still shells out to `claude -p` (Sonnet) inside the runner. **Bug status: OPEN — not fixed, only diagnosed.**
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9). This is a resumption snapshot.
> **Context docs:** `working/edge-modeling/SESSION-LOG.md` (read the "Plate 3 Full-Sweep — Status Report — 2026-06-07" entry first), `working/edge-modeling/edge-modeling-reification-design.md` §3 (D2/D7/D8), `progress/continue-prompts/2026-06-05-edge-modeling-plate-3-backfill.md` (full spec + engineering notes).

## State at handoff (2026-06-07)
- Plate 3 logic is **built, validated (12-event mini-batch, $0.81), and debugged** (supersede chapter-overlap fix landed + re-validated).
- The runner `scripts/edge-reify-backfill.py` is now **crash-resilient + resumable**: fail-fast on the rate wall (exits <~90s, no retry-loop burn), incremental per-event flush, `processed-events.jsonl` ledger, `--resume` (verified 0 duplicates).
- **The real full sweep has NOT run.** A 6-min overnight `--all` partial left `working/edge-modeling/plate3-full/` with 37 minted nodes + 11 hub-review-queue entries — **but that output is STALE JUNK and is NOT in git.** The 37 minted nodes are narrative micro-beats (`departure-at-daybreak`, `arya-confesses-about-mycah`, `discussion-of-giants`) — i.e. the overnight `--all` path minted hubs WITHOUT applying the D8/Q1 selective gate. **Treat `plate3-full/` as contaminated.**

## ⚠️ BEFORE YOU RUN — two must-dos (added 2026-06-07)
1. **Fix/verify the `--all` selective gate.** The overnight run minted micro-beat hubs, which means the D8 n-ary gate + Q1 trigger-family filter were NOT enforced in the `--all` minting path (they WERE in `--batch`/mini-batch, which was clean). Inspect `scripts/edge-reify-backfill.py`'s `--all` path: confirm minting happens AFTER the trigger-family filter + D8 reify/skip decision, not before. Smoke 5-10 events and eyeball the minted slugs — if you see "departure-at-daybreak"-style beats, the gate is still wrong; do NOT proceed.
2. **Clear the contaminated partial:** `rm -rf working/edge-modeling/plate3-full/` then start FRESH (`--all`, no `--resume` — there's no valid ledger from the buggy run). Resume (`--resume`) only matters for continuing a CLEAN run after a wall.
- **Graph untouched:** edges.jsonl = 3811, 0 nodes minted into `graph/`, `git status graph/` clean. Nothing in this plate writes `graph/` — that is Plate 5 only.

## DECISION REQUIRED BEFORE RUNNING (cost)
The dry-run enumerated **~2,056 trigger-family candidate events** (not the earlier 200-300 estimate). Many skip as clean dyads via the D8 gate, but cost is uncertain: **~$50-$160** depending on the skip ratio. **Do not blindly run all 2,056.** Choose:
- **(A) Calibration chunk first (RECOMMENDED):** run a bounded slice (one book, or first ~200 events), read the actual reify/skip ratio + measured cost from the ledger, then extrapolate and decide whether to finish. The runner is resumable, so this is free to chunk.
- **(B) Full run, attended:** only if the calibrated cost is acceptable. Watch the per-10-event progress + running-cost line; the fail-fast leaves the ledger so you re-run the same command after any wall.

## Steps
1. Confirm preconditions (read the SESSION-LOG 2026-06-07 entry). Verify `graph/edges/edges.jsonl` is still 3811 (staging discipline).
2. Run the sweep **attended** (watch usage):
       python3 scripts/edge-reify-backfill.py --all --resume
   - For a calibration chunk, use whatever slice flag the runner supports (e.g. `--book` / `--limit`) or stop it after ~200 events and read `processed-events.jsonl` for the reify/skip ratio + summed cost.
   - If it hits the wall, it exits cleanly leaving the ledger — re-run the SAME command to continue.
3. When the sweep is complete, write `working/edge-modeling/plate3-full/plate3-full-summary.md` (the runner does this on clean completion; if it exited via wall, note % done).
4. **Audit cadence:** run the Reporter (`working/edge-modeling/audit-repo-reporter-prompt.md`, PLATE_JUST_RUN=3) -> then a FRESH-session Auditor (`audit-alignment-auditor-prompt.md`). Verdict must be ON COURSE before Plate 4/5.
5. **Human review** (Matt): `hub-review-queue.jsonl` (borderline n-ary + medium-confidence fuzzy hub matches) and `supersede-candidates.jsonl` (the edges Plate 5 will mark `superseded_by`).

## Out of scope
- Merging anything into `graph/` (that is Plate 5, separately gated with before/after sign-off).
- Plate 4 (Haiku-bulk disposition) and the staged cleanups (drift reclassify, collision merges) — those also merge at the Plate 5 gate.

## Files this session may create/modify
- `working/edge-modeling/plate3-full/*` (staging outputs + ledger)
- `scripts/edge-reify-backfill.py` (only if a bug needs fixing mid-run)
- APPEND to `working/edge-modeling/SESSION-LOG.md`
- DO NOT modify anything under `graph/`.

---

## OPERATIONAL ADDENDUM (2026-06-07) — survive the 5-hour window; run-strategy + recs

### The `--all` gate bug (FIX FIRST — see "⚠️ BEFORE YOU RUN" above)
`--batch` applies the D8/Q1 selective gate correctly (mini-batch was clean). `--all` does NOT — the overnight run minted narrative micro-beat hubs (`departure-at-daybreak`, `discussion-of-giants`), meaning minting happens before/independent of the trigger-family + D8 reify/skip filter in the `--all` path. The dry-run stub forces `is_nary=true`, so it BYPASSED the gate and never caught this. **Fix:** filter + decide reify/skip BEFORE minting in `--all`; mint only for passers. **Verify:** run 5-10 REAL events in `--all`, confirm zero micro-beat mints. Status: OPEN.

### Run strategy — DO NOT repeat last night's failure
Last night: the run hit the 5-hour wall → **retry-looped against the wall for hours, burning the usage window while producing nothing** → got killed at session end → did NOT auto-resume. The runner now has fail-fast (<~90s exit) + `--resume` + a `processed-events.jsonl` ledger, but you must wrap it:
- **Outer auto-resume wrapper** (adapt `scripts/stage4-run-forever.sh`, or add a `--forever` loop to the runner). Pattern: run `--all --resume` → on the hard-wall fail-fast exit, **sleep until the window resets**, then relaunch `--all --resume`. It survives the 5-hour boundary and keeps going after. (Memory: `project_stage4_run_forever_wrapper`, `project_stage4_sleep_defaults`.)
- **Pace within the window** with a SHORT inter-batch sleep (seconds-to-tens-of-seconds) to avoid tripping short-term rate limits — NOT a long idle (you have generous usage today; use the window, don't waste it). The LONG sleep is reserved for the hard-wall reset only.
- **NEVER let it retry-loop against the wall** — fail-fast then sleep-until-reset is the correct shape. That loop is exactly what burned last night.

### Wrapper spec (CANONICAL — reuse the existing apparatus, do NOT reinvent)
We already have battle-tested rate-limit-survival scripts. Model the reify wrapper on them rather than building from scratch:
- `scripts/stage4-run-forever.sh` — sleeps until the rate-limit window resets, then relaunches; survives walls unattended (the core pattern).
- `scripts/stage4-events-bulk-run.sh` — paced auto-resume reference: `sleep_with_stop_check`, stop-file handling, `MAX_ITER`, SIGINT-terminal.
- `scripts/stage4-tail-classifier.py` — `--sleep-between` (chunked, stop-file-aware) is the in-runner pacing precedent.
- Memory: `project_stage4_run_forever_wrapper`, `project_stage4_sleep_defaults` (STAGE4_SLEEP: 1200s parallel-safe / 600s burst / 3600+ conservative).

Required behavior (all of these):
1. **Internal concurrency** stays at the runner's `claude -p` cap (~5). The wrapper is the OUTER sequential loop.
2. **Pace** with a SHORT inter-batch sleep (seconds → low tens of seconds) to dodge burst limits — NOT a long idle. Usage is generous today; *use* the window.
3. **On the hard-wall fail-fast exit** (the runner already exits clean <~90s with the ledger intact): the wrapper **sleeps until the window resets**, then relaunches `--all --resume`. Survives the 5-hour boundary and keeps going after, unattended.
4. **Stop-file** so Matt can halt safely between batches (mirror `sleep_with_stop_check`).
5. **`MAX_ITER`** backstop so a pathological loop can't run unbounded.
6. **Fail GRACEFULLY everywhere:** clean exit + intact `processed-events.jsonl` on any wall/interruption; never a retry-loop against the wall (that's last night's failure).

### Sequence
1. Fix + verify the `--all` gate. 2. `rm -rf working/edge-modeling/plate3-full/` (stale junk). 3. **Calibration chunk first** (~200 events / one book) → read reify/skip ratio + summed cost from `processed-events.jsonl`; extrapolate (~2,056 candidates, ~$50-160) before committing. 4. Full sweep under the auto-resume wrapper. 5. After: Reporter → fresh Auditor → human-review `hub-review-queue.jsonl` + `supersede-candidates.jsonl` → Plate 5 gated merge.

### My recommendations on the open questions (RESOLVED — do not relitigate)
- **Q1 = reify-SELECTIVE** (trigger families only) + **D8** (reify on n-ary STRUCTURE not type; clean dyads stay direct edges).
- **Q2 = confidence-gated fuzzy reuse-before-mint** (auto-rebind high-confidence only; queue medium; mint last).
- **D2 = Replace** (pure 2-hop hub). STILL OWED: verify the 1-hop `--neighbors`/`--edges` modes also surface hub-mediated relations; if not, fall back to (c) Project for high-traffic types only.
- **D7 = one event node, two roles** (`AGENT_IN` executor + `COMMANDS_IN` orderer); no instigator→victim collapse.
- **Cleanups:** `conquest-of-dorne` vs `the-conquest-of-dorne` → don't merge, reclassify the BOOK to `object.text`. `tourney-at/of-maidenpool` → resolve canonical from the local wiki cache. 12 drift nodes → `graph/nodes/chapters/` + retype `meta.chapter`. `house.*` allowed as `AGENT_IN` for group actors. `donal-noye`↔`mag` mutual-kill → two directed KILLS edges, NO `MUTUAL_KILL` type.

### Guardrails
- **Staging only.** NEVER write `graph/` (Plate 5 is the single gated merge). `edges.jsonl` stays 3811.
- Do NOT auto-run `/endsession`.
