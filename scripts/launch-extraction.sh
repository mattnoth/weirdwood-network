#!/usr/bin/env bash
# launch-extraction.sh — Open iTerm2 tabs and run extraction waves in parallel
#
# Usage:
#   ./scripts/launch-extraction.sh <book> <terminals> [start_wave]
#   ./scripts/launch-extraction.sh --chain <book> <terminals> [start_wave]
#   ./scripts/launch-extraction.sh --chain --max <N> <book> <terminals> [start_wave]
#
# Default: each terminal runs ONE wave, then stops.
#   4 terminals from wave 1 = waves 1,2,3,4 (one per terminal)
#
# With --chain: terminals cycle through all remaining waves.
#   4 terminals from wave 1 = T1 gets 1,5,9,13... T2 gets 2,6,10,14... etc.
#   Touch /tmp/extraction-stop to halt after the current wave.
#
# With --max N: each terminal runs at most N waves, then stops.
#   Combine with --chain to limit how far each terminal goes.
#
# Examples:
#   ./scripts/launch-extraction.sh agot 4          # Waves 1-4, one each
#   ./scripts/launch-extraction.sh agot 4 9        # Waves 9-12, one each
#   ./scripts/launch-extraction.sh --chain agot 4  # All waves, chained across 4 terminals
#   ./scripts/launch-extraction.sh --chain agot 4 9  # Chain from wave 9
#   ./scripts/launch-extraction.sh --chain --max 2 agot 2 3  # 2 terminals, 2 waves each

set -euo pipefail
cd "$(dirname "$0")/.."

CHAIN=false
MAX_PER_TERMINAL=0  # 0 = unlimited
while [[ "${1:-}" == --* ]]; do
  case "$1" in
    --chain) CHAIN=true; shift ;;
    --max)   MAX_PER_TERMINAL=${2:?--max requires a number}; shift 2 ;;
    *)       echo "Unknown flag: $1"; exit 1 ;;
  esac
done

BOOK=${1:?Usage: $0 [--chain] [--max N] <book> <terminals> [start_wave]}
TERMINALS=${2:?Usage: $0 [--chain] [--max N] <book> <terminals> [start_wave]}
START_WAVE=${3:-1}

CHAPTER_DIR="sources/chapters/${BOOK}"

if [[ ! -d "$CHAPTER_DIR" ]]; then
  echo "ERROR: Chapter directory not found: $CHAPTER_DIR"
  exit 1
fi

# Count chapters and compute total waves
CHAPTER_COUNT=$(ls "$CHAPTER_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')
WAVE_SIZE=5
TOTAL_WAVES=$(( (CHAPTER_COUNT + WAVE_SIZE - 1) / WAVE_SIZE ))

if (( START_WAVE > TOTAL_WAVES )); then
  echo "ERROR: Start wave $START_WAVE exceeds total waves $TOTAL_WAVES for $BOOK ($CHAPTER_COUNT chapters)"
  exit 1
fi

echo "${BOOK^^}: $CHAPTER_COUNT chapters, $TOTAL_WAVES waves, $TERMINALS terminals (starting at wave $START_WAVE)"
echo ""

# Clear any stale stop file from a previous run (only relevant in chain mode)
if [[ "$CHAIN" == true ]]; then
  rm -f /tmp/extraction-stop
fi

PROJECT_DIR="$(pwd)"
SCRIPT="./scripts/run-extraction-wave.sh"

# Build command chain for each terminal
for (( t=0; t<TERMINALS; t++ )); do
  CMD=""
  WAVE_LIST=""
  WAVES_ARR=()

  if [[ "$CHAIN" == true ]]; then
    # Chained: terminal cycles through waves (1,5,9,13... for terminal 1 of 4)
    for (( w=START_WAVE+t; w<=TOTAL_WAVES; w+=TERMINALS )); do
      if (( MAX_PER_TERMINAL > 0 && ${#WAVES_ARR[@]} >= MAX_PER_TERMINAL )); then
        break
      fi
      WAVES_ARR+=("$w")
      WAVE_LIST="${WAVE_LIST} ${w}"
    done
  else
    # Default: one wave per terminal
    w=$(( START_WAVE + t ))
    if (( w <= TOTAL_WAVES )); then
      WAVES_ARR+=("$w")
      WAVE_LIST=" ${w}"
    fi
  fi

  # Build command — chained mode uses a loop with stop-file check
  if (( ${#WAVES_ARR[@]} == 0 )); then
    :
  elif (( ${#WAVES_ARR[@]} == 1 )); then
    CMD="${SCRIPT} ${BOOK} ${WAVES_ARR[0]}"
  else
    CMD="for w in ${WAVES_ARR[*]}; do "
    CMD+="if [[ -f /tmp/extraction-stop ]]; then echo '⏸  Stop file detected (/tmp/extraction-stop) — halting before wave '\$w; break; fi; "
    CMD+="${SCRIPT} ${BOOK} \$w; "
    CMD+="done"
  fi

  if [[ -z "$CMD" ]]; then
    echo "Terminal $((t+1)): (no waves)"
    continue
  fi

  # Format wave list with commas: "3, 5, 7" instead of " 3 5 7"
  WAVE_DISPLAY=$(echo "$WAVE_LIST" | xargs | tr ' ' ', ')
  echo "Terminal $((t+1)): waves [${WAVE_DISPLAY}]"

  # Open iTerm2 tab and run the command
  osascript <<EOF
tell application "iTerm2"
  activate
  tell current window
    create tab with default profile
    tell current session of current tab
      write text "cd ${PROJECT_DIR} && ${CMD}"
    end tell
  end tell
end tell
EOF

done

echo ""
echo "Launched $TERMINALS iTerm2 tabs. Monitor progress in each tab."
if [[ "$CHAIN" == true ]]; then
  echo ""
  echo "To stop after the current wave finishes:"
  echo "  touch /tmp/extraction-stop"
fi
