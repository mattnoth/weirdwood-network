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
#   touch /tmp/stage4-haiku-stop                     # graceful stop after current batch
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

STOP_FILE="/tmp/stage4-haiku-stop"
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

# Get ordered batch IDs starting at START_BATCH from the Sonnet manifest.
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

idx=0
total=${#BATCHES[@]}
for batch in "${BATCHES[@]}"; do
  idx=$((idx + 1))

  if [[ -f "$STOP_FILE" ]]; then
    log "Stop file detected ($STOP_FILE) — exiting cleanly. Stopped at $batch (next would have been queued)."
    rm -f "$STOP_FILE"
    exit 0
  fi

  log "═══════════════════════════════════════════════════════════════"
  log "  Batch $idx/$total  →  $batch"
  log "═══════════════════════════════════════════════════════════════"

  start_ts=$(date +%s)
  if python3 scripts/stage4-haiku-run.py \
        --batches "$batch" \
        --concurrency "$CONCURRENCY" \
        --chunk-size "$CHUNK_SIZE" 2>&1 | tee -a "$LOOP_LOG"; then
    elapsed=$(( $(date +%s) - start_ts ))
    log "$batch completed in ${elapsed}s"
    inter_sleep="$SLEEP_BETWEEN"
  else
    elapsed=$(( $(date +%s) - start_ts ))
    log "WARNING: $batch failed after ${elapsed}s (likely rate-limit or transient). Sleeping ${RATE_LIMIT_SLEEP}s before next batch."
    inter_sleep="$RATE_LIMIT_SLEEP"
  fi

  # Sleep before next batch (skip on last)
  if (( idx < total )); then
    if [[ -f "$STOP_FILE" ]]; then
      log "Stop file detected during post-batch wait — exiting."
      rm -f "$STOP_FILE"
      exit 0
    fi
    log "Sleeping ${inter_sleep}s before next batch..."
    # Sleep in 60s chunks so stop file is checked frequently
    remaining=$inter_sleep
    while (( remaining > 0 )); do
      if [[ -f "$STOP_FILE" ]]; then
        log "Stop file detected mid-sleep — exiting."
        rm -f "$STOP_FILE"
        exit 0
      fi
      step=60
      (( step > remaining )) && step=$remaining
      sleep "$step"
      remaining=$((remaining - step))
    done
  fi
done

log "All ${#BATCHES[@]} batches complete."
