#!/usr/bin/env bash
# stage4-haiku-run-forever.sh — Resilient outer wrapper for stage4-haiku-loop.sh.
#
# Behavior:
#   - Loops calling stage4-haiku-loop.sh
#   - If the inner loop exits non-zero (crash, terminal disconnect, etc.), sleeps
#     RELAUNCH_SLEEP seconds and re-launches
#   - Stops cleanly when /tmp/stage4-haiku-stop exists
#
# Usage:
#   bash scripts/stage4-haiku-run-forever.sh                # start at batch-0001
#   bash scripts/stage4-haiku-run-forever.sh batch-0050     # resume at batch-0050
#
# Stop:
#   touch /tmp/stage4-haiku-stop  (will propagate through inner loop)
#
# Env (forwarded to inner loop):
#   STAGE4_HAIKU_SLEEP_BETWEEN, STAGE4_HAIKU_CONCURRENCY,
#   STAGE4_HAIKU_CHUNK_SIZE, STAGE4_HAIKU_RATE_LIMIT_SLEEP
#
# Env (this wrapper):
#   STAGE4_HAIKU_RELAUNCH_SLEEP   seconds to wait before re-launching after a crash (default 600 = 10 min)

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

STOP_FILE="/tmp/stage4-haiku-stop"
RELAUNCH_SLEEP="${STAGE4_HAIKU_RELAUNCH_SLEEP:-600}"
START_BATCH="${1:-batch-0001}"
WRAPPER_LOG_DIR="working/missions/2026-05-19-stage4-haiku/loop-logs"
mkdir -p "$WRAPPER_LOG_DIR"
WRAPPER_LOG="$WRAPPER_LOG_DIR/run-forever-$(date -u +%Y%m%dT%H%M%SZ).log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] $*" | tee -a "$WRAPPER_LOG"; }

log "─────────────────────────────────────────────────────────────"
log "  stage4-haiku-run-forever (outer resilience wrapper)"
log "  Start batch:       $START_BATCH"
log "  Relaunch sleep:    ${RELAUNCH_SLEEP}s ($((RELAUNCH_SLEEP / 60))min) after crashes"
log "  Stop file:         $STOP_FILE"
log "  Wrapper log:       $WRAPPER_LOG"
log "─────────────────────────────────────────────────────────────"

attempt=0
while true; do
  attempt=$((attempt + 1))

  if [[ -f "$STOP_FILE" ]]; then
    log "Stop file detected before launch — exiting."
    rm -f "$STOP_FILE"
    exit 0
  fi

  log "Launching inner loop (attempt $attempt) from $START_BATCH..."
  if bash scripts/stage4-haiku-loop.sh "$START_BATCH"; then
    log "Inner loop exited cleanly (all batches done or stop-file)."
    break
  else
    exit_code=$?
    log "Inner loop exited non-zero ($exit_code). Sleeping ${RELAUNCH_SLEEP}s before relaunch."
  fi

  # Sleep before relaunch, checking stop file each 60s
  remaining=$RELAUNCH_SLEEP
  while (( remaining > 0 )); do
    if [[ -f "$STOP_FILE" ]]; then
      log "Stop file detected during relaunch wait — exiting."
      rm -f "$STOP_FILE"
      exit 0
    fi
    step=60
    (( step > remaining )) && step=$remaining
    sleep "$step"
    remaining=$((remaining - step))
  done

  # On relaunch, figure out where to resume from by inspecting which batches have output.
  # We re-read manifest in inner loop's enumerator; for now, START_BATCH is sticky to
  # the user's original choice. The inner loop's own resume logic handles per-batch
  # restart by skipping ones that already wrote output (handled by stage4-haiku-run.py
  # itself which checks for existing prose-edges-haiku/ files).
done

log "stage4-haiku-run-forever complete at $(date '+%Y-%m-%d %H:%M:%S %Z')."
