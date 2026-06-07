# Plate 3 — RESUME the reification full sweep

> **Recommended model:** Sonnet (the runner shells out to `claude -p` per event; the orchestrating session just launches + watches). No Opus needed.
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
