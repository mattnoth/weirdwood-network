#!/usr/bin/env bash
# edge-reify-run-forever.sh — 5-hour-wall-safe wrapper for the Plate 3
# reification full sweep.
#
# Why this script exists:
#   The Python runner (scripts/edge-reify-backfill.py --all --resume) fails
#   fast on a hard rate-limit / quota wall (exit code 2), leaving its ledger
#   and partial outputs intact. This wrapper picks up after the wall: sleeps
#   for ${EDGE_REIFY_WALL_SLEEP} seconds, then relaunches with --resume.
#   The cycle survives the 5-hour usage window: each relaunch exits in <~90s
#   if the wall is still up, so wasted LLM cost across the window is minimal.
#
# Modeled on scripts/stage4-events-bulk-run.sh (proven for multi-day bulk runs).
#
# Exit codes from edge-reify-backfill.py:
#   0   — clean completion (all events done OR --max-events cap reached)
#   2   — rate-limit wall (sleep ${EDGE_REIFY_WALL_SLEEP}s then resume)
#   130 — SIGINT / SIGTERM (do NOT relaunch; user interrupted)
#   other non-zero — crash (sleep 300s and retry, up to MAX_CRASHES consecutive)
#
# Stop-file: touch $HOME/source/claude-cwd/tmp/edge-reify-stop to stop
# cleanly between iterations. Ctrl-C also stops cleanly.
#
# Usage:
#   bash scripts/edge-reify-run-forever.sh
#
# Env overrides:
#   EDGE_REIFY_OUT          — output dir (default: working/edge-modeling/plate3-full)
#   EDGE_REIFY_MODEL        — model (default: claude-sonnet-4-6)
#   EDGE_REIFY_CONCURRENCY  — internal claude -p concurrency (default: 5)
#   EDGE_REIFY_MAX_EVENTS   — cap events per invocation (default: unbounded;
#                             set to e.g. 200 for a calibration chunk)
#   EDGE_REIFY_WALL_SLEEP   — seconds to sleep after exit 2 (default: 3600,
#                             = 1hr; a 5hr wall costs 5 wakeup cycles)
#   EDGE_REIFY_MAX_ITER     — wrapper iteration cap (default: 50)
#   EDGE_REIFY_INTER_RUN    — seconds between successful iterations (default: 30)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

STOP_FILE="$HOME/source/claude-cwd/tmp/edge-reify-stop"
mkdir -p "$(dirname "$STOP_FILE")"

OUT="${EDGE_REIFY_OUT:-${REPO_ROOT}/working/edge-modeling/plate3-full}"
MODEL="${EDGE_REIFY_MODEL:-claude-sonnet-4-6}"
CONCURRENCY="${EDGE_REIFY_CONCURRENCY:-5}"
MAX_EVENTS="${EDGE_REIFY_MAX_EVENTS:-}"
WALL_SLEEP="${EDGE_REIFY_WALL_SLEEP:-3600}"
MAX_ITER="${EDGE_REIFY_MAX_ITER:-50}"
INTER_RUN="${EDGE_REIFY_INTER_RUN:-30}"
MAX_CRASHES=5

mkdir -p "$OUT"
LOG="$OUT/run.log"

echo "═══════════════════════════════════════════════════════════════"
echo "  edge-reify-run-forever — Plate 3 full sweep wrapper"
echo "  Output:        $OUT"
echo "  Log:           $LOG"
echo "  Model:         $MODEL"
echo "  Concurrency:   $CONCURRENCY"
echo "  Max events:    ${MAX_EVENTS:-<unbounded>}"
echo "  Wall sleep:    ${WALL_SLEEP}s ($((WALL_SLEEP / 60))min) after exit 2"
echo "  Inter-run:     ${INTER_RUN}s between successful iters"
echo "  Max iter:      $MAX_ITER"
echo "  Started:       $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "  Stop file:     $STOP_FILE  (touch to stop cleanly)"
echo "═══════════════════════════════════════════════════════════════"

{
echo "═══════════════════════════════════════════════════════════════"
echo "  edge-reify-run-forever — start $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "  Output: $OUT | Model: $MODEL | Concurrency: $CONCURRENCY"
echo "  Max events: ${MAX_EVENTS:-<unbounded>} | Wall sleep: ${WALL_SLEEP}s"
echo "═══════════════════════════════════════════════════════════════"
} >> "$LOG" 2>&1

# Sleep in 60s chunks; break if stop-file appears mid-sleep.
sleep_with_stop_check() {
  local remaining=$1
  while (( remaining > 0 )); do
    if [[ -f "$STOP_FILE" ]]; then
      return 1
    fi
    local step=60
    (( step > remaining )) && step=$remaining
    sleep "$step"
    remaining=$((remaining - step))
  done
  return 0
}

# Trap SIGINT so user Ctrl-C exits cleanly without an extra relaunch.
trap 'echo "[$(date +%H:%M:%S)] SIGINT received — exiting wrapper" | tee -a "$LOG"; rm -f "$STOP_FILE"; exit 130' INT TERM

iteration=0
crash_streak=0
first_run=true

while true; do
  iteration=$((iteration + 1))

  # ── Max-iteration cap ──────────────────────────────────────────
  if (( iteration > MAX_ITER )); then
    echo "[$(date '+%H:%M:%S')] MAX_ITER=${MAX_ITER} reached — stopping." | tee -a "$LOG"
    break
  fi

  # ── Stop-file check ────────────────────────────────────────────
  if [[ -f "$STOP_FILE" ]]; then
    echo "[$(date '+%H:%M:%S')] Stop file detected — exiting cleanly." | tee -a "$LOG"
    break
  fi

  # ── Build the Python command ────────────────────────────────────
  # First run uses --resume to be safe (no-op if ledger absent).
  # All subsequent runs MUST use --resume.
  CMD_ARGS=(
    "python3" "scripts/edge-reify-backfill.py"
    "--all" "--resume"
    "--output-dir" "$OUT"
    "--model" "$MODEL"
    "--concurrency" "$CONCURRENCY"
  )
  if [[ -n "$MAX_EVENTS" ]]; then
    CMD_ARGS+=("--max-events" "$MAX_EVENTS")
  fi

  echo "[$(date '+%H:%M:%S')] iter=$iteration — launching: ${CMD_ARGS[*]}" | tee -a "$LOG"

  # ── Run the Python runner ──────────────────────────────────────
  set +e
  "${CMD_ARGS[@]}" 2>&1 | tee -a "$LOG"
  EXIT_CODE=${PIPESTATUS[0]}
  set -e

  echo "[$(date '+%H:%M:%S')] iter=$iteration exited code=$EXIT_CODE" | tee -a "$LOG"

  # ── Immediate stop-file check (caught after Python returned) ───
  if [[ -f "$STOP_FILE" ]]; then
    echo "[$(date '+%H:%M:%S')] Stop file detected after Python returned — exiting." | tee -a "$LOG"
    break
  fi

  # ── Interpret exit code ─────────────────────────────────────────

  if [[ "$EXIT_CODE" -eq 130 ]]; then
    echo "[$(date '+%H:%M:%S')] Interrupted (exit 130) — exiting wrapper without relaunch." | tee -a "$LOG"
    break
  fi

  if [[ "$EXIT_CODE" -eq 2 ]]; then
    # Rate-limit wall.
    crash_streak=0

    # If MAX_EVENTS is set (calibration / bounded chunk), do NOT resume across
    # the wall — that would silently overshoot the cap by processing ANOTHER
    # full chunk after each wall recovery. Exit cleanly; user inspects partial
    # ledger + decides whether to re-launch.
    if [[ -n "$MAX_EVENTS" ]]; then
      echo "[$(date '+%H:%M:%S')] Rate-limit wall (exit 2) on a bounded MAX_EVENTS=${MAX_EVENTS} run." | tee -a "$LOG"
      echo "[$(date '+%H:%M:%S')] NOT auto-resuming (would overshoot cap). Exiting." | tee -a "$LOG"
      echo "[$(date '+%H:%M:%S')] To continue, inspect $OUT/processed-events.jsonl then re-launch:" | tee -a "$LOG"
      echo "[$(date '+%H:%M:%S')]   EDGE_REIFY_MAX_EVENTS=N bash scripts/edge-reify-run-forever.sh" | tee -a "$LOG"
      break
    fi

    echo "[$(date '+%H:%M:%S')] Rate-limit wall (exit 2). Sleeping ${WALL_SLEEP}s..." | tee -a "$LOG"
    if ! sleep_with_stop_check "$WALL_SLEEP"; then
      echo "[$(date '+%H:%M:%S')] Stop file appeared during wall sleep — exiting." | tee -a "$LOG"
      break
    fi
    continue
  fi

  if [[ "$EXIT_CODE" -eq 0 ]]; then
    # Clean exit. Either truly done OR --max-events cap was hit.
    # On --max-events runs the wrapper still loops; the second iteration's
    # --resume will skip the same events and hit "All events already processed"
    # on the next pass, exiting 0 again. Cleanup the stop file and exit.
    crash_streak=0
    echo "[$(date '+%H:%M:%S')] Clean exit (code 0)." | tee -a "$LOG"

    # If we have a max-events cap, exit immediately after first successful
    # invocation — we did our bounded chunk, the user wants to inspect.
    if [[ -n "$MAX_EVENTS" ]]; then
      echo "[$(date '+%H:%M:%S')] MAX_EVENTS=${MAX_EVENTS} cap reached. Stopping after one successful chunk." | tee -a "$LOG"
      break
    fi

    # No cap: check if there's actually more work. If the run-summary shows
    # "events_attempted_this_run": 0, we're truly done.
    if [[ -f "$OUT/plate3-full-summary.json" ]]; then
      attempted=$(python3 -c "
import json
try:
    d = json.load(open('$OUT/plate3-full-summary.json'))
    print(d.get('events_attempted_this_run', 0))
except Exception:
    print(0)
" 2>/dev/null || echo "0")
      if [[ "$attempted" -eq 0 ]]; then
        echo "[$(date '+%H:%M:%S')] 0 events attempted this run — mission complete!" | tee -a "$LOG"
        break
      fi
    fi

    # More work might remain; brief breather then loop.
    if ! sleep_with_stop_check "$INTER_RUN"; then
      echo "[$(date '+%H:%M:%S')] Stop file detected — exiting cleanly." | tee -a "$LOG"
      break
    fi
    continue
  fi

  # Any other non-zero = crash. Cap streak.
  crash_streak=$((crash_streak + 1))
  echo "[$(date '+%H:%M:%S')] CRASH (exit $EXIT_CODE, streak=$crash_streak/$MAX_CRASHES). Sleeping 300s..." | tee -a "$LOG"
  if [[ "$crash_streak" -ge "$MAX_CRASHES" ]]; then
    echo "[$(date '+%H:%M:%S')] $MAX_CRASHES consecutive crashes — giving up." | tee -a "$LOG"
    rm -f "$STOP_FILE"
    exit "$EXIT_CODE"
  fi
  if ! sleep_with_stop_check 300; then
    echo "[$(date '+%H:%M:%S')] Stop file detected during crash sleep — exiting." | tee -a "$LOG"
    break
  fi

done

rm -f "$STOP_FILE"

echo "═══════════════════════════════════════════════════════════════" | tee -a "$LOG"
echo "  edge-reify-run-forever finished at $(date '+%Y-%m-%d %H:%M:%S %Z')" | tee -a "$LOG"
echo "  Output: $OUT" | tee -a "$LOG"
echo "  Log:    $LOG" | tee -a "$LOG"
echo "═══════════════════════════════════════════════════════════════" | tee -a "$LOG"
