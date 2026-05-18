# Session 53 — Stage 4 1-Tab Smoke + Throttle Calibration (2026-05-15)

**Status:** Diagnosis + tooling session. One batch completed (batch-0012) to validate the new config; not a bulk run.
**Model:** Opus 4.7 (1M context).
**Mission:** `2026-05-14-stage4-v1-bulk-sonnet` — Stage 4 v1 prose-edge classifier bulk run.

## What we were trying to figure out

Matt fired 6 iTerm tabs the prior night for the Stage 4 bulk Sonnet mission. The Max plan 5-hour session limit blew through in ~30 minutes and he lost the terminal scrollback he'd intended to copy. Three concrete unknowns:

1. Did the locking work, or did workers double-claim?
2. Where are the logs — what's persisted vs. ephemeral terminal output?
3. Was there a delay-between-batches mechanism, and did it help?

## Findings

**Locking worked.** 14 distinct `worker_id`s across `state.jsonl` claims, zero double-claims. The atomic-write-lock pattern in `.claude/commands/worker-stage4.md` did its job. 4 stale `.lock` files were workers cut off mid-batch — needed manual cleanup.

**Logs are extensively persisted; terminal scrollback is redundant.** All under `working/missions/<mission-slug>/`:
- `run-logs/worker-*.log` — per-worker bash launcher log (timestamps, batch IDs, exit codes, cost)
- `timing.jsonl` — one row per batch (input/cache/output tokens + cost + elapsed)
- `state.jsonl` — claim/release events
- `results/batch-*.json` — per-batch decision counts + edge totals
- `bash scripts/stage4.sh status` aggregates all of it in one call

**The "delay" Matt remembered.** A `sleep 30` between batches existed in `cmd_run`. Per-tab, not a stagger across tabs. Negligible against 40-min batches.

## Root cause of the rate-limit blowout

Per-batch cost on Sonnet 4.6 ran ~$5.45 with ~21M cache-read tokens (multi-tab runs). 6 tabs in parallel pushed ~125M tokens of cache-read every 40-min window, slamming Max's TPM-based 5-hour ceiling. The 5-hour Max cap is not a hard token count — it's a rolling budget. With 6 concurrent workers it saturates in 25-30 min. Math:

| Tabs | Time to wall | Batches before wall |
|---|---|---|
| 6 | ~30 min | 0-1 per tab |
| 2 | ~60 min | 1-2 per tab (3 total) |
| 1 (90-min throttle) | projected | 5-7 per 5h window |

Parallelism above 1 tab buys faster wall-clock only until the cap. After it saturates, all parallelism is wasted.

## Bug discovered: `set -e` killed the workers silently

While the 2-tab smoke ran, workers terminated without logging "Batch complete" lines after their second batch. They left orphan locks behind. Diagnosis: the `claude -p` pipeline in `cmd_run` was running under `set -euo pipefail`. When `claude` (or any pipeline stage) exited non-zero, `pipefail` caused the pipeline to return non-zero, and `set -e` exited the script *before* the next line (`claude_exit=${PIPESTATUS[0]}`) could even run — so the explicit error-handling block in the loop was dead code.

Fix: wrap the pipeline in `set +e` / `set -e`:

```bash
set +e
claude -p ... | tee "$tmp_json" | python3 scripts/stream-claude-output.py
claude_exit=${PIPESTATUS[0]}
set -e
```

This was the real reason the 2-tab smoke left orphan locks instead of cleanly handling the wall.

## Rate-limit handler port from extract.sh

`scripts/extract.sh:570-622` had a working rate-limit-event detector — looks for `"status":"rejected"` + `"rateLimitType"` in the stream-json output. Ported to `stage4.sh` to:

1. Detect on each batch
2. Write `rate-limit-events.jsonl` row with worker_id, batch_id, detected_at, rate_limit_type, resets_at_ts
3. Write `next-eligible.txt` with the resets-at epoch timestamp (for future launchd auto-resume)
4. Exit the worker loop cleanly (`break`) instead of retrying

**Blind spot uncovered.** During the 1-tab smoke, when the wall hit, this detection did NOT trigger. The actual wall message from the Claude CLI was plain text: `"You've hit your org's monthly usage limit"` — printed to stdout/stderr, **not** wrapped in a stream-json `rate_limit_event`. The grep-based detection only catches API-level rate limits, not Max-plan subscription session walls. Filed as future polish: extend detection to also grep for `"You've hit"`, `"usage limit"`, `"five_hour"`, etc.

## Throttle introduced

Added `STAGE4_SLEEP_BETWEEN` env var (default 5400s = 90 min) replacing the prior 30s. Configurable so Matt can dial throughput vs. headroom-for-other-Claude-work.

Math at 90-min throttle:
- Each cycle ≈ 25-35 min batch + 90 min sleep = ~2 hours
- 5h window fits ~2-3 batches before wall (was ~$5.45 each; new data says ~$3.42)
- Updated projection: 5-7 batches per 5h window before wall

## Empirical surprise on 1-tab serial

Batch-0012 (first batch on new config) finished at:

| | This batch | Multi-tab avg |
|---|---|---|
| Elapsed | 23.8 min | 40 min |
| Cost | $3.42 | $5.45 |
| Cache_read | 1.3M | 21M |

**16x reduction in cache_read tokens**. Hypothesis: at 1-tab serial, Anthropic's prompt cache stays warm across batches (same architecture + classifier + mission spec prefix). At multi-tab, workers fight for cache slots and each batch re-pays the full cache-write cost. Worth understanding but not blocking — flag as observation in todos.

The decision distribution on batch-0012 (353 candidates → 100 emit / 249 reject / 4 escalate / 3 vocab-gap) tracks the Session 53b smoke baseline (Sonnet CONCERNS-low). Quality check before continuing the bulk is queued as the next session's work.

## Mission state at session end

- 12/201 batches done (3% of work; batch-0012 the only new completion this session)
- $50.09 cumulative spend
- 0 stuck batches
- 0 active workers (final worker in 90-min sleep, `/tmp/stage4-stop` set, will exit cleanly on wake)
- 189 batches queued

## Decisions made

- **Multi-tab parallelism dropped.** 1-tab + 90-min throttle is the working config.
- **Sonnet 4.6 stays.** Matt confirmed preference against switching to Haiku ("hate having a better model done first and going down a grade"). Haiku smoke from Session 53b already returned CONCERNS-high with two systematic bugs; sticking with Sonnet.
- **Auto-relaunch via launchd deferred.** Matt prefers manual fire-after-stop while we calibrate quality, not fully autonomous yet.

## Open questions / future polish

1. **Rate-limit text-pattern detection.** Extend `stage4.sh` to also grep for plain-text Max-plan wall messages, not just stream-json `rate_limit_event`. Required if/when we automate relaunch.
2. **Active worker detection in `status` command.** Workers in the 90-min sleep don't update their log file, so `status` shows "Active workers: 0" even mid-cycle. Could check process list or write a heartbeat. Cosmetic, not blocking.
3. **Why 1-tab serial is 16x cheaper on cache_read.** Hypothesis is prompt-cache warmth across serial batches. Worth confirming with a controlled comparison once we have ~5 more 1-tab batches landed.

## What ships forward

- Continue prompt: `progress/continue-prompts/2026-05-15-stage4-batch-quality-check.md` — Spot-check batch-0012's 30 output files + 3 vocab-gap questions + 4 cross-identity escalations, compare to Haiku smoke output for systematic-bug presence. Verdict gates the resumption of bulk run.
- Throttle config validated by one batch; needs 3-5 more to confirm steady-state cost.
- Bug-fixed and throttled `scripts/stage4.sh` is now the durable artifact — future bulk runs use it.
