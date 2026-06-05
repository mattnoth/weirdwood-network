#!/usr/bin/env bash
# stage4-run-forever.sh — Wraps stage4.sh run with rate-limit-aware auto-resume.
#
# Behavior:
#   - Loops calling 'stage4.sh run' (which processes one batch + sleeps + repeats internally)
#   - When 'stage4.sh run' exits (rate-limit, manifest empty, or any other reason),
#     this wrapper inspects next-eligible.txt + manifest, sleeps until reset if needed,
#     and re-launches the worker.
#   - Stops cleanly on:
#       (a) $HOME/source/claude-cwd/tmp/stage4-stop exists (manual soft-stop)
#       (b) 0 queued batches in manifest (mission complete)
#
# Usage:
#   STAGE4_SLEEP_BETWEEN=270 bash scripts/stage4-run-forever.sh
#
# Designed to be left running in an iTerm tab and survive rate-limit walls overnight.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${WEIRWOOD_PROJECT_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"
cd "$REPO_ROOT"

STOP_FILE="$HOME/source/claude-cwd/tmp/stage4-stop"

# Mission discovery — mirror stage4.sh logic.
discover_mission_dir() {
  if [[ -n "${STAGE4_MISSION_DIR:-}" ]]; then
    echo "$STAGE4_MISSION_DIR"
    return 0
  fi
  find "$REPO_ROOT/working/missions" -mindepth 1 -maxdepth 1 -type d 2>/dev/null \
    | sort \
    | while read -r d; do
        [[ -f "$d/batch-manifest.jsonl" ]] && echo "$d"
      done \
    | tail -1
}

MISSION_DIR=$(discover_mission_dir)
if [[ -z "$MISSION_DIR" ]]; then
  echo "ERROR: No mission found under $REPO_ROOT/working/missions" >&2
  exit 1
fi

MISSION_NAME=$(basename "$MISSION_DIR")
SLEEP_BETWEEN="${STAGE4_SLEEP_BETWEEN:-1200}"

echo "─────────────────────────────────────────────────────────────"
echo "  stage4-run-forever wrapper"
echo "  Mission:        $MISSION_NAME"
echo "  Sleep/batch:    ${SLEEP_BETWEEN}s ($((SLEEP_BETWEEN / 60))min)"
echo "  Started:        $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "  Stop file:      $STOP_FILE  (touch to stop cleanly)"
echo "─────────────────────────────────────────────────────────────"

count_queued() {
  python3 -c "
import json
c = 0
try:
    for l in open('$MISSION_DIR/batch-manifest.jsonl'):
        l = l.strip()
        if not l: continue
        try:
            if json.loads(l).get('status') == 'queued': c += 1
        except: pass
except: pass
print(c)
" 2>/dev/null || echo "0"
}

iteration=0
while true; do
  iteration=$((iteration + 1))

  # ── Stop-file check ──────────────────────────────────────────
  if [[ -f "$STOP_FILE" ]]; then
    echo "[$(date '+%H:%M:%S')] stop file detected — exiting wrapper cleanly."
    break
  fi

  # ── Mission-complete check ──────────────────────────────────
  queued=$(count_queued)
  if [[ "$queued" -eq 0 ]]; then
    echo "[$(date '+%H:%M:%S')] 0 queued batches — mission complete. Exiting wrapper."
    break
  fi

  # ── Rate-limit pre-sleep ────────────────────────────────────
  ne_file="$MISSION_DIR/next-eligible.txt"
  if [[ -f "$ne_file" ]]; then
    reset_ts=$(cat "$ne_file" 2>/dev/null | tr -d ' \n\r')
    now=$(date +%s)
    if [[ "$reset_ts" =~ ^[0-9]+$ ]] && (( reset_ts > now )); then
      wait_s=$(( reset_ts - now + 60 ))  # 60s buffer past the reset
      reset_dt=$(date -r "$reset_ts" -u '+%Y-%m-%d %H:%M UTC')
      echo "[$(date '+%H:%M:%S')] rate-limit in effect. Sleeping ${wait_s}s until ${reset_dt} (+60s buffer)..."
      sleep "$wait_s"
      # Re-check stop file after the long sleep
      if [[ -f "$STOP_FILE" ]]; then
        echo "[$(date '+%H:%M:%S')] stop file appeared during rate-limit sleep — exiting."
        break
      fi
    fi
  fi

  # ── Run worker ──────────────────────────────────────────────
  echo "[$(date '+%H:%M:%S')] iter=$iteration queued=$queued — launching stage4.sh run"
  # Don't let worker's non-zero exit kill the wrapper
  STAGE4_SLEEP_BETWEEN="$SLEEP_BETWEEN" bash "$REPO_ROOT/scripts/stage4.sh" run || true
  echo "[$(date '+%H:%M:%S')] worker exited — looping back to check resume conditions"

  # Small breather between iterations
  sleep 5
done

echo "─────────────────────────────────────────────────────────────"
echo "  stage4-run-forever exiting at $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "─────────────────────────────────────────────────────────────"
