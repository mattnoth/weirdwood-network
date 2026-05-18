# Stage 4 Bulk Run — Watcher Continue Prompt

> **Recommended model:** Sonnet 4.6 for the watcher (`/model claude-sonnet-4-6`). Opus is overkill — the watcher reads state files and reports; no reasoning depth required. **The WORKER is also Sonnet 4.6** (set via `STAGE4_MODEL` default in `scripts/stage4.sh`).
>
> **Drafted:** 2026-05-17 evening.
> **Updated:** 2026-05-18 — added run-forever wrapper, post-burst-experiment config (270s sleep), batch-claim-helper todo reference.

---

## Self-contained context

You are checking on the Stage 4 v1 prose-edge classifier bulk run for the Weirwood Network (ASOIAF knowledge graph). One worker terminal is running, processing 5-file batches from a 1,089-batch manifest, with a 270-second sleep between batches.

**The terminal runs `scripts/stage4-run-forever.sh` (new 2026-05-17), not `stage4.sh run` directly.** The wrapper auto-resumes after rate-limit walls by sleeping until reset + 60s buffer, then re-launching the worker. It only exits when (a) `/tmp/stage4-stop` exists or (b) the manifest has 0 queued batches. This is the unattended-overnight mode.

The mission directory is `working/missions/2026-05-14-stage4-v1-bulk-sonnet/`. The worker prompt is `.claude/commands/worker-stage4.md`. Base launch script is `scripts/stage4.sh`. Forever-wrapper is `scripts/stage4-run-forever.sh`.

## What "healthy" looks like

| Signal | Healthy value |
|---|---|
| Process tree | 3 procs: `stage4-run-forever.sh` (wrapper) → `stage4.sh run` (worker loop) → `claude -p ... claude-sonnet-4-6` (current batch) |
| Lock files | 0 or 1 (1 = current batch in progress, 0 = sleeping or between batches) |
| Per-batch cost | $2.40–$2.80 |
| Per-batch wall-clock | 8–23 min (high variance: depends on batch content; 1219s = ~20min lifetime avg) |
| Cache_read per batch | 2M+ (warm cache; sleep ≤270s keeps it warm — TTL is 5min) |
| Pace at 270s sleep | ~3 batches/hr → ~$8/hr → ~$3,000 total at completion |
| file_done events | 5 per batch (one per file in the 5-file batch) |
| Rate-limit events | Some are normal under burst pacing — wrapper auto-recovers. Watch for cascading walls (3+ in a row). |

## Status check (one command)

```bash
weirwood stage4 status
```

That's the canonical health snapshot — manifest progress, token/cost totals, rate-limit events, stuck batches.

For more depth:

```bash
# Recent batches completed
grep '"event": "release"' working/missions/2026-05-14-stage4-v1-bulk-sonnet/state.jsonl | tail -5

# Wrapper + worker + claude all running?
ps -ef | grep -E "stage4-run-forever|stage4\.sh run|claude.*sonnet" | grep -v grep

# Recent rate-limit events (auto-recovered if wrapper is up)
tail -5 working/missions/2026-05-14-stage4-v1-bulk-sonnet/rate-limit-events.jsonl

# file_done events in last hour
python3 -c "
import json
from datetime import datetime, timezone, timedelta
cutoff = datetime.now(tz=timezone.utc) - timedelta(hours=1)
count = 0
batches = {}
for l in open('working/missions/2026-05-14-stage4-v1-bulk-sonnet/state.jsonl'):
    if '\"file_done\"' not in l: continue
    try:
        d = json.loads(l)
        ts = d.get('timestamp','')
        if 'T' in ts:
            dt = datetime.fromisoformat(ts.replace('Z','+00:00'))
            if dt > cutoff:
                count += 1
                batches[d.get('batch_id','?')] = batches.get(d.get('batch_id','?'),0) + 1
    except: pass
print(f'{count} file_done events in last hour across {len(batches)} batches')
"
```

## Things to watch for

### 1. Wrapper died (whole stack gone)

Symptoms: `ps` shows neither `stage4-run-forever.sh` nor `stage4.sh run`. Latest run-log hasn't been written to in >30 min.

Action: Check if the wrapper exited cleanly (mission complete OR `/tmp/stage4-stop` set). If neither — investigate the iTerm tab (Matt may have closed it). Relaunch:

```bash
osascript <<'EOF'
tell application "iTerm2"
  activate
  tell current window
    create tab with default profile
    tell current session of current tab
      write text "cd '/Users/mnoth/source/asoiaf-chat' && STAGE4_SLEEP_BETWEEN=270 bash scripts/stage4-run-forever.sh"
    end tell
  end tell
end tell
EOF
```

### 2. Worker died but wrapper still running

Symptoms: `stage4-run-forever.sh` PID present, but no `stage4.sh run` and no `claude -p`. The wrapper is in its 5s inter-iteration sleep OR mid rate-limit pre-sleep.

Action: Wait 30 seconds and re-check. If wrapper is in rate-limit pre-sleep, it'll log a line like `rate-limit in effect. Sleeping NNNs until ...`. Check the iTerm tab output.

### 3. Stale lock (worker died mid-batch)

Symptoms: a `.lock` file exists in `working/missions/2026-05-14-stage4-v1-bulk-sonnet/locks/` but no worker process is running and no current batch is being claimed.

Action: delete the stale lock. The L2 resume-check in the worker prompt means the next worker to claim that batch will skip already-finished files via `file_done` events.

```bash
rm working/missions/2026-05-14-stage4-v1-bulk-sonnet/locks/batch-NNNN.lock
# OR use the unstick helper which also flips manifest status back to queued:
weirwood stage4 unstick batch-NNNN
```

### 4. Rate-limit wall hit (auto-recovered by wrapper)

Symptoms: new entry in `rate-limit-events.jsonl`, `next-eligible.txt` updated, worker logs `🚫 RATE LIMIT` and exits.

**Expected behavior with the wrapper in place:** Wrapper detects exit, reads `next-eligible.txt`, sleeps until reset + 60s, re-launches. No action needed.

Action only required if: the wrapper itself isn't running (see #1) OR if rate-limits are cascading (3+ in a row, suggesting cap reduced).

```bash
# Check current eligibility
python3 -c "
import datetime
ts = int(open('working/missions/2026-05-14-stage4-v1-bulk-sonnet/next-eligible.txt').read().strip())
dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
now = datetime.datetime.now(tz=datetime.timezone.utc)
delta = (dt - now).total_seconds()
print(f'Reset: {dt}, delta: {int(delta/60)} min {\"passed\" if delta<0 else \"to go\"}')
"
```

### 5. Duplicate-claim race (parallel only — should not happen under single-tab)

The Write-tool-based lock is not fully atomic when multiple workers race. The 2026-05-17 3-tab burst experiment saw batch-0034 double-claimed. **Single-tab (the current configuration) cannot race with itself.** If duplicate claims appear in `state.jsonl`, something is wrong — escalate.

## Knobs you can tweak

### Stop the worker gracefully

```bash
weirwood stage4 stop   # touches /tmp/stage4-stop
# Wrapper checks the stop file every iteration AND after rate-limit pre-sleeps.
# Worker exits cleanly at top of next inner loop iteration (after current batch).
# Wrapper exits cleanly on its next loop check.
```

### Relaunch with different throttle

| Sleep | Pace | Notes |
|---|---|---|
| 60s | ~4.3 batches/hr | max throughput; cache stays warm; may saturate 5h cap under heavy daytime use |
| 270s | ~3 batches/hr | **current config** — cache still warm (TTL = 300s); good unattended-overnight pace |
| 600s | ~2.1 batches/hr | cache goes cold each batch (pays full cache-creation tokens); avoid unless saving budget |
| 1200s | ~1.5 batches/hr | **script default; parallel-safe**: Matt actively using Claude alongside |
| 3600+ | ~1/hr | conservative; for heavy parallel Claude work |

To relaunch with a different throttle:
```bash
weirwood stage4 stop          # halt the wrapper + worker
# Wait for both PIDs to disappear (check ps)
# Then relaunch via osascript (see Section 1 above), substituting the desired STAGE4_SLEEP_BETWEEN value
```

### Burst (outage credit / temporary cap lift)

If Matt has temporary cap lift, parallel can help — but only with L1+L2 in place (already shipped). The race-condition risk is real (2026-05-17 saw 1 duplicate in 3-tab burst). Recommendation: max 2 tabs to limit races, with 60s sleep (not 0).

```bash
STAGE4_SLEEP_BETWEEN=60 bash scripts/stage4.sh launch -t 2
```

Note: `stage4.sh launch -t N` uses the **non-wrapped** `stage4.sh run` per tab (no auto-resume on rate-limit). For parallel + auto-resume, multiple wrapper tabs are needed — but the wrapper was designed for single-tab; multi-tab parallel against shared `next-eligible.txt` may double-sleep. Single-tab wrapper is the proven configuration.

## L1 + L2 background (key invariants)

- **Batches are 5 files each** (re-partitioned 2026-05-17 — `scripts/wiki-pass2-repartition-manifest.py`)
- **Each file is checkpointed independently** to `state.jsonl` as `file_done` event
- **Resume-on-claim**: a new worker claiming a batch reads `state.jsonl` for prior `file_done` events on that batch_id, builds a skip_set, and skips finished files. Verified working 2026-05-16.
- **Per-batch wall-loss is capped at one file (~$0.50)** because each file flushes before the next starts.

## Known per-batch inefficiency (deferred fix)

Every worker invocation re-scans `batch-manifest.jsonl` (~1089 rows) via Read/Glob/Grep/Bash to find the first `status:queued` row at the highest unmet priority tier — costs ~10+ pre-flight tool calls per batch. Filed as a follow-up in `working/todos.md` → Extraction Infrastructure: "Stage 4 worker: deterministic batch-claim helper" (write `scripts/stage4-claim.py` → swap the manual scan for a single python call). Expected ~20-30% per-batch pre-flight token reduction. **Do not implement mid-corpus** — the drift-detection rule requires smoke-test on 1-2 batches first.

## Current state at handoff (2026-05-18 ~03:00 UTC / 2026-05-17 22:00 CDT)

- **Manifest:** 69 done / 1020 queued (6% complete)
- **Cumulative cost:** ~$194 across 65 timed batches
- **Avg per-batch elapsed:** 1219s (~20min — lifetime avg includes high-variance batches; recent burst batches were 467–1377s)
- **Process tree:**
  - Wrapper: `bash scripts/stage4-run-forever.sh` (originally PID 89706, may have respawned the worker layer)
  - Worker layer: `bash scripts/stage4.sh run` (changes PID each rate-limit cycle)
  - Claude: `claude -p ... claude-sonnet-4-6` (changes per batch)
- **Throttle:** `STAGE4_SLEEP_BETWEEN=270` (4.5min, cache-warm)
- **Rate-limit events:** 6 total in mission history (3 from 2026-05-16 3-tab burst experiment, 1+ from 2026-05-17 60s-sleep burst, more under wrapper auto-recovery). Wrapper handles transparently.
- **2026-05-17 session summary:** Burst-mode experiment — soft-stopped 4x to tune sleep (1200 → 600 → 270 → 60 → 270 with wrapper). Hit rate-limit at 60s sleep with 1h to go on the 5h cap. Reverted to 270s under `stage4-run-forever.sh` for unattended overnight. Script default changed from 5400s → 1200s in the same session.

## Recent script + config changes (2026-05-17)

- **`scripts/stage4.sh`**: default `STAGE4_SLEEP_BETWEEN` changed from 5400s (90min) → 1200s (20min, parallel-safe). Help text and `launch` subcommand updated.
- **`scripts/stage4-run-forever.sh`**: NEW. Wraps `stage4.sh run` in an auto-resume loop. Reads `next-eligible.txt`, sleeps through rate-limit walls, re-launches worker. Exits on stop file or 0-queued.
- **`working/todos.md`**: new item under "Extraction Infrastructure" — deterministic batch-claim helper (deferred).

## Memory rules to honor

- **Never auto-run `/endsession`** — requires explicit Matt permission.
- **Never run extractions without asking** — but the bulk run is already authorized and running; just observe. New launches DO require asking.
- **Cheapest viable model** — Sonnet 4.6 is the choice here for both watcher and worker.
- **Python before Agent** — for any analysis (cost projections, pace math), prefer python over delegation.
- **Show commands being run** — surface the exact bash, not summaries.
- **Drift detection mandatory for bulk LLM runs** — do NOT change worker model or batch-claim mechanism mid-corpus without a smoke test.

## When to escalate to Matt

- Multiple rate-limit walls in a row that the wrapper doesn't recover from (cap might have shrunk, or wrapper died)
- Validator errors recurring (data quality issue surfaced)
- Cost spike (>$3.50/batch) — could mean prompt-cache miss pattern
- Wrapper exited but manifest still has queued batches (unexpected — check log)
- `state.jsonl` shows duplicate claims (single-tab should make this impossible)

Otherwise: let it run. The bulk is steady-state ops. Check every few hours, ensure pace is roughly 3 batches/hr at the current 270s sleep.
