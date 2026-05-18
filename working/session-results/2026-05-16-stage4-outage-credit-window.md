---
session: 2026-05-16 (outage-credit window)
mission: 2026-05-14-stage4-v1-bulk-sonnet
purpose: relaunch parallel Stage 4 workers during 1-hour outage-credit window
status: 3 workers launched, env-var bug found and patched, stop file set
---

# Stage 4 outage-credit relaunch — handoff

## TL;DR

You stepped away while 3 workers (out of the 4 you requested) were processing their current batches. Stop file is set so they'll exit cleanly when done. The launch script had a bug — env vars from your parent shell weren't reaching the iTerm tabs, so they were going to sleep 90 min between batches instead of back-to-back. **Bug is now patched.** When you return, you can relaunch in one command and the workers will go back-to-back.

## What happened

1. **15:10 CDT** — `STAGE4_SLEEP_BETWEEN=0 bash scripts/stage4.sh launch -t 4`. osascript opened 4 tabs but only 3 got the `write text` command (common iTerm activation hiccup). 3 workers started, claimed batches 0022/0023 (+ one mid-claim).
2. **15:11 CDT** — Noticed env-var bug: `STAGE4_SLEEP_BETWEEN=0` did NOT propagate to the fresh shells osascript opens. Workers would each do 1 batch then sleep 5400s (90 min) — wasting the outage window.
3. **15:11 CDT** — Set `/tmp/stage4-stop` so workers exit cleanly after their current batch (no wasted sleep).
4. **15:13 CDT** — Patched `scripts/stage4.sh` `cmd_launch` to embed `STAGE4_SLEEP_BETWEEN=${sleep_forward}` into the `write text` command. Diff:
   - Reads parent shell's `STAGE4_SLEEP_BETWEEN` (default 5400 if unset).
   - Prepends it to the per-tab command so each worker shell has the env var when it reads the script.

## State when you return

- **3 batches likely complete** (started 15:10, ~25 min each, done ~15:35 CDT).
- **Workers exited cleanly** (stop file set).
- **Manifest:** expect 24/201 done if all 3 succeeded. Check with `weirwood stage4 status`.
- **Stop file:** `/tmp/stage4-stop` exists — must be removed before relaunch (the patched `cmd_launch` does this automatically at line 522: `rm -f "$STOP_FILE"`).

## Relaunch command

If you still have outage credit when you return:

```bash
STAGE4_SLEEP_BETWEEN=0 weirwood stage4 launch -t 4
```

With the patch, each worker will go back-to-back (no 90-min sleep). 4 tabs × ~25 min/batch = ~10 batches in the next hour at ~$3.42 each ≈ $34.

If you want even fewer tabs to stay under credit, drop `-t` to 2 or 3.

## Verification commands

```bash
# How many batches completed
weirwood stage4 status

# Confirm workers exited
ls working/missions/2026-05-14-stage4-v1-bulk-sonnet/locks/   # should be empty

# Verify patched script
grep "STAGE4_SLEEP_BETWEEN=" scripts/stage4.sh   # should show the new "STAGE4_SLEEP_BETWEEN=${sleep_forward}" line in cmd_launch
```

## Why I didn't auto-relaunch

I have no scheduled-wakeup mechanism without `/loop` dynamic mode, and the user-friendly parallel-tabs workflow is 4 iTerm tabs which `/loop` (single session) doesn't deliver. Honest stop here was the right call rather than spawn something half-aligned with your ask.
