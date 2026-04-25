#!/usr/bin/env bash
# extraction-status.sh — Show extraction progress and next steps
#
# Usage:
#   ./scripts/extraction-status.sh [book]
#   ./scripts/extraction-status.sh agot
#
# Defaults to agot if no book specified.

set -euo pipefail
cd "$(dirname "$0")/.."

BOOK=${1:-agot}
CHAPTER_DIR="sources/chapters/${BOOK}"
EXTRACT_DIR="extractions/mechanical/${BOOK}"
STATS_FILE="working/extraction-stats/extraction-stats-${BOOK}-pass1-v3.csv"
WAVE_SIZE=5

if [[ ! -d "$CHAPTER_DIR" ]]; then
  echo "ERROR: Chapter directory not found: $CHAPTER_DIR"
  exit 1
fi

mkdir -p "$EXTRACT_DIR"

# Discover all chapters and what's done
ALL_CHAPTERS=()
for f in "$CHAPTER_DIR"/*.md; do
  ALL_CHAPTERS+=("$(basename "$f" .md)")
done
TOTAL=${#ALL_CHAPTERS[@]}

DONE=()
MISSING=()
for ch in "${ALL_CHAPTERS[@]}"; do
  if [[ -f "$EXTRACT_DIR/${ch}.extraction.md" ]]; then
    DONE+=("$ch")
  else
    MISSING+=("$ch")
  fi
done

DONE_COUNT=${#DONE[@]}
MISSING_COUNT=${#MISSING[@]}
TOTAL_WAVES=$(( (TOTAL + WAVE_SIZE - 1) / WAVE_SIZE ))

# --- Cost summary from stats CSV ---
COST_SUMMARY=""
if [[ -f "$STATS_FILE" ]]; then
  COST_SUMMARY=$(python3 -c "
import csv
total_cost = 0.0
total_input = 0
total_output = 0
chapters_tracked = 0
with open('$STATS_FILE') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('book') != '$BOOK': continue
        if row.get('status') != 'ok': continue
        cost = row.get('cost_usd', '0')
        try:
            c = float(cost)
            if c > 0:
                total_cost += c
                chapters_tracked += 1
        except: pass
        try: total_input += int(row.get('cache_read_tokens', 0)) + int(row.get('cache_creation_tokens', 0)) + int(row.get('input_tokens', 0))
        except: pass
        try: total_output += int(row.get('output_tokens', 0))
        except: pass
if chapters_tracked > 0:
    avg = total_cost / chapters_tracked
    est_remaining = avg * $MISSING_COUNT
    print(f'Cost so far: \${total_cost:.2f} across {chapters_tracked} chapters (avg \${avg:.2f}/chapter)')
    print(f'Estimated remaining: ~\${est_remaining:.0f} for $MISSING_COUNT chapters')
elif total_output > 0:
    print(f'Token stats: {total_input:,} input, {total_output:,} output (cost tracking added — will show on next runs)')
else:
    print('No cost data yet (will appear after next extraction run)')
" 2>/dev/null || echo "")
fi

# --- Header ---
echo ""
echo "=== ${BOOK^^} Extraction Status ==="
echo ""
echo "${DONE_COUNT} of ${TOTAL} chapters extracted. ${MISSING_COUNT} remaining. (${TOTAL_WAVES} waves total)"
echo ""

if [[ -n "$COST_SUMMARY" ]]; then
  echo "$COST_SUMMARY"
  echo ""
fi

# --- Missing chapters table grouped by wave ---
if (( MISSING_COUNT == 0 )); then
  echo "All chapters extracted! Ready for the next pass."
  exit 0
fi

# Build wave → missing chapters mapping
declare -A WAVE_MISSING
WAVE_ORDER=()
for (( i=0; i<TOTAL; i++ )); do
  ch="${ALL_CHAPTERS[$i]}"
  wave=$(( i / WAVE_SIZE + 1 ))
  if [[ ! -f "$EXTRACT_DIR/${ch}.extraction.md" ]]; then
    if [[ -z "${WAVE_MISSING[$wave]:-}" ]]; then
      WAVE_MISSING[$wave]="$ch"
      WAVE_ORDER+=("$wave")
    else
      WAVE_MISSING[$wave]="${WAVE_MISSING[$wave]}, $ch"
    fi
  fi
done

# Show which waves are fully complete
DONE_WAVES=()
for (( w=1; w<=TOTAL_WAVES; w++ )); do
  if [[ -z "${WAVE_MISSING[$w]:-}" ]]; then
    DONE_WAVES+=("$w")
  fi
done
if (( ${#DONE_WAVES[@]} > 0 )); then
  echo "Completed waves: $(IFS=', '; echo "${DONE_WAVES[*]}")"
  echo ""
fi

# Calculate column widths
WAVE_COL_W=5
CHAPTERS_COL_W=10
COUNT_COL_W=5
for w in "${WAVE_ORDER[@]}"; do
  chapters="${WAVE_MISSING[$w]}"
  # Count items
  count=$(echo "$chapters" | tr ',' '\n' | wc -l | tr -d ' ')
  # Check if this wave is partial (some chapters in wave are done)
  wave_start=$(( (w - 1) * WAVE_SIZE ))
  wave_end=$(( wave_start + WAVE_SIZE ))
  if (( wave_end > TOTAL )); then wave_end=$TOTAL; fi
  wave_total=$(( wave_end - wave_start ))
  if (( count < wave_total )); then
    label="$w (partial)"
  else
    label="$w"
  fi
  (( ${#label} > WAVE_COL_W )) && WAVE_COL_W=${#label}
  (( ${#chapters} > CHAPTERS_COL_W )) && CHAPTERS_COL_W=${#chapters}
done

# Draw table
printf "%-${WAVE_COL_W}s | %-${CHAPTERS_COL_W}s | %s\n" "Wave" "Missing Chapters" "Count"
printf "%${WAVE_COL_W}s-+-%${CHAPTERS_COL_W}s-+-%s\n" "" "" "" | tr ' ' '-'

for w in "${WAVE_ORDER[@]}"; do
  chapters="${WAVE_MISSING[$w]}"
  count=$(echo "$chapters" | tr ',' '\n' | wc -l | tr -d ' ')
  wave_start=$(( (w - 1) * WAVE_SIZE ))
  wave_end=$(( wave_start + WAVE_SIZE ))
  if (( wave_end > TOTAL )); then wave_end=$TOTAL; fi
  wave_total=$(( wave_end - wave_start ))
  if (( count < wave_total )); then
    label="$w (partial)"
  else
    label="$w"
  fi
  printf "%-${WAVE_COL_W}s | %-${CHAPTERS_COL_W}s | %s\n" "$label" "$chapters" "$count"
done

echo ""

# --- Suggested commands ---
# Split missing waves into rounds of ~4 waves (2 terminals x 2 max each).
# Partial/orphan waves get a single mop-up command at the end.

echo "To run the remaining chapters:"
echo ""

# Separate: contiguous main run vs isolated partial waves
MAIN_WAVES=()
PARTIAL_WAVES=()

# Find the largest contiguous block of missing waves
BEST_START=0
BEST_LEN=0
CUR_START=0
CUR_LEN=0
for (( i=0; i<${#WAVE_ORDER[@]}; i++ )); do
  if (( i == 0 )); then
    CUR_START=0; CUR_LEN=1
  elif (( WAVE_ORDER[i] == WAVE_ORDER[i-1] + 1 )); then
    CUR_LEN=$(( CUR_LEN + 1 ))
  else
    if (( CUR_LEN > BEST_LEN )); then BEST_START=$CUR_START; BEST_LEN=$CUR_LEN; fi
    CUR_START=$i; CUR_LEN=1
  fi
done
if (( CUR_LEN > BEST_LEN )); then BEST_START=$CUR_START; BEST_LEN=$CUR_LEN; fi

# Main block = contiguous run, everything else = partial mop-up
for (( i=0; i<${#WAVE_ORDER[@]}; i++ )); do
  if (( i >= BEST_START && i < BEST_START + BEST_LEN )); then
    MAIN_WAVES+=("${WAVE_ORDER[$i]}")
  else
    PARTIAL_WAVES+=("${WAVE_ORDER[$i]}")
  fi
done

# Emit rounds for the main contiguous block (4 waves per round, 2 terminals x 2 max)
round=1
i=0
while (( i < ${#MAIN_WAVES[@]} )); do
  batch_start="${MAIN_WAVES[$i]}"
  remaining=$(( ${#MAIN_WAVES[@]} - i ))
  batch=$(( remaining < 4 ? remaining : 4 ))
  batch_end="${MAIN_WAVES[$((i + batch - 1))]}"

  # Label: "waves 9-12" or "waves 13-15"
  if (( batch_start == batch_end )); then
    label="wave ${batch_start}"
  else
    label="waves ${batch_start}-${batch_end}"
  fi

  terms=$(( batch < 2 ? 1 : 2 ))
  max_per=$(( (batch + terms - 1) / terms ))

  echo "  # Round $round: ${label}"
  echo "  ./scripts/launch-extraction.sh --chain --max ${max_per} ${BOOK} ${terms} ${batch_start}"
  echo ""

  i=$(( i + batch ))
  round=$(( round + 1 ))
done

# Emit mop-up commands for any isolated partial waves
for pw in "${PARTIAL_WAVES[@]}"; do
  # Count how many chapters are missing in this wave
  pw_chapters="${WAVE_MISSING[$pw]}"
  pw_count=$(echo "$pw_chapters" | tr ',' '\n' | wc -l | tr -d ' ')
  echo "  # Mop up wave ${pw} (${pw_count} chapter$( (( pw_count > 1 )) && echo s))"
  echo "  ./scripts/run-extraction-wave.sh ${BOOK} ${pw}"
  echo ""
done
