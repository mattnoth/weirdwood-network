#!/usr/bin/env bash
# stage4-haiku-loop.sh — Sequential Haiku batch runner with stop-file support.
#
# Loops through Sonnet manifest batches in order, running each through Haiku.
# Sleeps STAGE4_HAIKU_SLEEP_BETWEEN seconds between batches.
# Checks stop file before each batch and on rate-limit failure.
#
# Usage:
#   bash scripts/stage4-haiku-loop.sh                # start from batch-0001
#   bash scripts/stage4-haiku-loop.sh batch-0050     # resume from batch-0050
#
# Stop:
#   touch $HOME/source/claude-cwd/tmp/stage4-haiku-stop                     # graceful stop after current batch
#
# Env overrides:
#   STAGE4_HAIKU_SLEEP_BETWEEN  inter-batch sleep seconds (default 1200 = 20 min)
#   STAGE4_HAIKU_CONCURRENCY    chunks-in-parallel within a batch (default 4)
#   STAGE4_HAIKU_CHUNK_SIZE     files per Haiku invocation (default 3)
#   STAGE4_HAIKU_RATE_LIMIT_SLEEP  sleep after a failed batch (default 3600 = 1h)

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

STOP_FILE="$HOME/source/claude-cwd/tmp/stage4-haiku-stop"
SLEEP_BETWEEN="${STAGE4_HAIKU_SLEEP_BETWEEN:-1200}"
CONCURRENCY="${STAGE4_HAIKU_CONCURRENCY:-4}"
CHUNK_SIZE="${STAGE4_HAIKU_CHUNK_SIZE:-3}"
RATE_LIMIT_SLEEP="${STAGE4_HAIKU_RATE_LIMIT_SLEEP:-3600}"
START_BATCH="${1:-batch-0001}"
MANIFEST="working/missions/2026-05-14-stage4-v1-bulk-sonnet/batch-manifest.jsonl"
LOOP_LOG_DIR="working/missions/2026-05-19-stage4-haiku/loop-logs"
mkdir -p "$LOOP_LOG_DIR"
LOOP_LOG="$LOOP_LOG_DIR/loop-$(date -u +%Y%m%dT%H%M%SZ).log"

# Clear any stale stop file
rm -f "$STOP_FILE"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] $*" | tee -a "$LOOP_LOG"
}

# Get ordered batch IDs.
#
# If STAGE4_HAIKU_BATCH_LIST is set, read batch IDs from that file (one per line;
# `# comments` and blank lines ignored; first column is the batch ID, anything
# after tab/space is ignored). Used for prioritized-scope runs (Option C, etc.)
# where manifest order is the wrong order.
#
# Otherwise, walk the Sonnet manifest from START_BATCH onward (default behavior).
if [[ -n "${STAGE4_HAIKU_BATCH_LIST:-}" ]]; then
  if [[ ! -f "$STAGE4_HAIKU_BATCH_LIST" ]]; then
    log "ERROR: STAGE4_HAIKU_BATCH_LIST=$STAGE4_HAIKU_BATCH_LIST not found"
    exit 1
  fi
  mapfile -t BATCHES < <(awk '/^[[:space:]]*(#|$)/ {next} {print $1}' "$STAGE4_HAIKU_BATCH_LIST")
  log "Using prioritized batch list: $STAGE4_HAIKU_BATCH_LIST (${#BATCHES[@]} batches)"
else
  mapfile -t BATCHES < <(python3 -c "
import json
import sys
start = sys.argv[1]
seen = False
with open('$MANIFEST') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        bid = d.get('batch_id', '')
        if bid == start:
            seen = True
        if seen and bid:
            print(bid)
" "$START_BATCH")
fi

if (( ${#BATCHES[@]} == 0 )); then
  log "ERROR: No batches found starting at $START_BATCH in $MANIFEST"
  exit 1
fi

log "─────────────────────────────────────────────────────────────"
log "  stage4-haiku-loop"
log "  Start batch:       $START_BATCH"
log "  Total queued:      ${#BATCHES[@]} batches"
log "  Sleep/batch:       ${SLEEP_BETWEEN}s ($((SLEEP_BETWEEN / 60))min)"
log "  Concurrency:       $CONCURRENCY chunks in parallel"
log "  Chunk size:        $CHUNK_SIZE files per Haiku call"
log "  Rate-limit sleep:  ${RATE_LIMIT_SLEEP}s ($((RATE_LIMIT_SLEEP / 60))min) after failures"
log "  Stop file:         $STOP_FILE  (touch to stop cleanly)"
log "  Loop log:          $LOOP_LOG"
log "─────────────────────────────────────────────────────────────"

RESULTS_DIR="working/missions/2026-05-19-stage4-haiku/results"
MISSION_RATE_LIMIT_LOG="working/missions/2026-05-19-stage4-haiku/rate-limit-events.jsonl"

# sleep_with_stop_check $seconds — sleep in 60s chunks; exit if stop file appears.
sleep_with_stop_check() {
  local remaining=$1
  while (( remaining > 0 )); do
    if [[ -f "$STOP_FILE" ]]; then
      log "Stop file detected mid-sleep — exiting."
      rm -f "$STOP_FILE"
      exit 0
    fi
    local step=60
    (( step > remaining )) && step=$remaining
    sleep "$step"
    remaining=$((remaining - step))
  done
}

idx=0
total=${#BATCHES[@]}
while (( idx < total )); do
  batch="${BATCHES[idx]}"
  human_idx=$((idx + 1))

  if [[ -f "$STOP_FILE" ]]; then
    log "Stop file detected ($STOP_FILE) — exiting cleanly. Stopped at $batch."
    rm -f "$STOP_FILE"
    exit 0
  fi

  log "═══════════════════════════════════════════════════════════════"
  log "  Batch $human_idx/$total  →  $batch"
  log "═══════════════════════════════════════════════════════════════"

  # On re-run after a prior rate-limit interruption (idx didn't advance), skip
  # files whose output already exists — avoids re-processing the partial-batch
  # done files. Tracked via $current_batch_attempt_count.
  skip_existing_flag=""
  if (( ${current_batch_attempt_count:-0} > 0 )); then
    skip_existing_flag="--skip-existing"
  fi

  start_ts=$(date +%s)
  python3 scripts/stage4-haiku-run.py \
        --batches "$batch" \
        --concurrency "$CONCURRENCY" \
        --chunk-size "$CHUNK_SIZE" \
        $skip_existing_flag 2>&1 | tee -a "$LOOP_LOG"
  run_rc=${PIPESTATUS[0]}
  current_batch_attempt_count=$((${current_batch_attempt_count:-0} + 1))
  elapsed=$(( $(date +%s) - start_ts ))

  # Inspect this batch's result JSON: did it hit a rate-limit, and if so when does it reset?
  # Echoes "<rate_limit_events_count> <latest_resets_at_ts>" on stdout. 0 0 if no signal.
  result_json="$RESULTS_DIR/${batch}.json"
  read -r rate_limited reset_ts < <(python3 - <<PYEOF
import json
result_json = "$result_json"
mission_log = "$MISSION_RATE_LIMIT_LOG"
try:
    d = json.load(open(result_json))
except Exception:
    print("0 0"); raise SystemExit
cnt = d.get("rate_limit_events_count", 0) or 0
if cnt <= 0:
    print(f"{cnt} 0"); raise SystemExit
batch_id = d.get("batch_id", "")
latest_ts = 0
try:
    for line in open(mission_log):
        line = line.strip()
        if not line:
            continue
        e = json.loads(line)
        if e.get("batch_id") != batch_id:
            continue
        ts = e.get("resets_at_ts") or 0
        if ts > latest_ts:
            latest_ts = ts
except FileNotFoundError:
    pass
print(f"{cnt} {latest_ts}")
PYEOF
)
  rate_limited=${rate_limited:-0}
  reset_ts=${reset_ts:-0}

  do_advance=1
  inter_sleep="$SLEEP_BETWEEN"

  if (( rate_limited > 0 )); then
    do_advance=0  # re-run same batch after reset; orchestrator skips files that already have .edges.jsonl
    if (( reset_ts > 0 )); then
      now=$(date +%s)
      inter_sleep=$(( reset_ts - now + 60 ))  # +60s buffer past reset
      (( inter_sleep < 60 )) && inter_sleep=60  # reset may have just fired — short re-try delay
      log "$batch hit rate-limit ($rate_limited events) after ${elapsed}s. Sleeping ${inter_sleep}s until reset+60s. Will re-run $batch on resume."
    else
      inter_sleep="$RATE_LIMIT_SLEEP"
      log "$batch hit rate-limit ($rate_limited events) after ${elapsed}s but no reset_ts found in $MISSION_RATE_LIMIT_LOG. Falling back to fixed ${inter_sleep}s. Will re-run $batch on resume."
    fi
  elif (( run_rc == 0 )); then
    log "$batch completed in ${elapsed}s"
  else
    inter_sleep="$RATE_LIMIT_SLEEP"
    log "WARNING: $batch exited rc=$run_rc after ${elapsed}s (non-rate-limit failure). Sleeping ${inter_sleep}s; advancing to next batch."
  fi

  # Sleep before next iteration. Always sleep if rate-limited (we'd just hit the wall again).
  # Otherwise, skip sleep if this was the last batch.
  if (( rate_limited > 0 )) || (( idx < total - 1 )); then
    if [[ -f "$STOP_FILE" ]]; then
      log "Stop file detected before post-batch sleep — exiting."
      rm -f "$STOP_FILE"
      exit 0
    fi
    log "Sleeping ${inter_sleep}s before next iteration..."
    sleep_with_stop_check "$inter_sleep"
  fi

  if (( do_advance == 1 )); then
    idx=$((idx + 1))
    current_batch_attempt_count=0  # reset for the next batch
  fi
done

log "All ${#BATCHES[@]} batches complete."
