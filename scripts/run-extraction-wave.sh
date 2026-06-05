#!/usr/bin/env bash
# run-extraction-wave.sh — Run Pass 1 mechanical extraction on a wave of chapters
#
# Usage:
#   ./scripts/run-extraction-wave.sh <book> <wave_number>
#
# Example:
#   ./scripts/run-extraction-wave.sh agot 3
#
# Books: agot, acok, asos, affc, adwd
# Chapters are auto-discovered from sources/chapters/<book>/
# Waves are groups of 5 chapters (last wave may be smaller).
#
# Run different waves in separate terminals for parallelism:
#   Terminal 1: ./scripts/run-extraction-wave.sh agot 1
#   Terminal 2: ./scripts/run-extraction-wave.sh agot 2
#   Terminal 3: ./scripts/run-extraction-wave.sh agot 3
#   Terminal 4: ./scripts/run-extraction-wave.sh agot 4
#
# See working/runbooks/extraction-pass1.md for full copy-paste runbook.
#
# Outputs:
#   extractions/mechanical/<book>/{chapter}.extraction.md  — the extraction
#   $HOME/source/claude-cwd/tmp/extraction-{chapter}.log                          — claude stdout (text)
#   $HOME/source/claude-cwd/tmp/extraction-{chapter}.json                         — full stream-json (token usage)
#   working/extraction-stats.csv                           — per-chapter timing & token log

set -euo pipefail
cd "$(dirname "$0")/.."

BOOK=${1:?Usage: $0 <book> <wave_number>  (e.g., $0 agot 3)}
WAVE=${2:?Usage: $0 <book> <wave_number>  (e.g., $0 agot 3)}

CHAPTER_DIR="sources/chapters/${BOOK}"
EXTRACT_DIR="extractions/mechanical/${BOOK}"
STATS_FILE="working/extraction-stats.csv"

if [[ ! -d "$CHAPTER_DIR" ]]; then
  echo "ERROR: Chapter directory not found: $CHAPTER_DIR"
  exit 1
fi

# Create extraction output directory if needed
mkdir -p "$EXTRACT_DIR"

# Create stats CSV with header if it doesn't exist
if [[ ! -f "$STATS_FILE" ]]; then
  echo "chapter,book,wave,status,start_time,end_time,duration_s,input_tokens,cache_creation_tokens,cache_read_tokens,output_tokens,total_tokens,cost_usd" > "$STATS_FILE"
fi

# Auto-discover chapters from directory (sorted — filenames sort correctly)
CHAPTERS=()
for f in "$CHAPTER_DIR"/*.md; do
  basename=$(basename "$f" .md)
  CHAPTERS+=("$basename")
done

if (( ${#CHAPTERS[@]} == 0 )); then
  echo "ERROR: No .md files found in $CHAPTER_DIR"
  exit 1
fi

WAVE_SIZE=5

# Calculate slice
START=$(( (WAVE - 1) * WAVE_SIZE ))
END=$(( START + WAVE_SIZE ))
if (( END > ${#CHAPTERS[@]} )); then
  END=${#CHAPTERS[@]}
fi

TOTAL_WAVES=$(( (${#CHAPTERS[@]} + WAVE_SIZE - 1) / WAVE_SIZE ))

if (( START >= ${#CHAPTERS[@]} )); then
  echo "Wave $WAVE is out of range (max $TOTAL_WAVES for $BOOK with ${#CHAPTERS[@]} chapters)"
  exit 1
fi

WAVE_CHAPTERS=("${CHAPTERS[@]:$START:$((END - START))}")

echo "=== ${BOOK^^} Wave $WAVE/$TOTAL_WAVES: chapters $((START+1))-$END of ${#CHAPTERS[@]} ==="
echo "Chapters: ${WAVE_CHAPTERS[*]}"
echo ""

WAVE_START=$(date +%s)
SUCCESSES=0
FAILURES=0
FAILED_LIST=()
WAVE_INPUT_TOKENS=0
WAVE_OUTPUT_TOKENS=0
WAVE_COST=""

for ch in "${WAVE_CHAPTERS[@]}"; do
  SRC="sources/chapters/${BOOK}/${ch}.md"
  OUT="extractions/mechanical/${BOOK}/${ch}.extraction.md"

  if [[ ! -f "$SRC" ]]; then
    echo "SKIP: $SRC not found"
    FAILURES=$((FAILURES + 1))
    FAILED_LIST+=("$ch (source missing)")
    echo "$ch,$BOOK,$WAVE,skip-no-source,,,,,,,,," >> "$STATS_FILE"
    continue
  fi

  # Check if extraction already exists and is complete
  if [[ -f "$OUT" ]]; then
    VALID=true
    LINE_COUNT=$(wc -l < "$OUT" | tr -d ' ')
    MISSING_SECTIONS=""
    for section in "## Characters" "## Events" "## Locations" "## Relationships"; do
      if ! grep -q "$section" "$OUT"; then
        MISSING_SECTIONS+="${section#### }, "
        VALID=false
      fi
    done
    if (( LINE_COUNT < 100 )); then
      VALID=false
    fi

    if [[ "$VALID" == true ]]; then
      echo "SKIP: $ch already extracted (${LINE_COUNT} lines, all sections present)"
      echo "$ch,$BOOK,$WAVE,skip-done,,,,,,,,," >> "$STATS_FILE"
      SUCCESSES=$((SUCCESSES + 1))
      continue
    else
      REASON=""
      if (( LINE_COUNT < 100 )); then
        REASON="only ${LINE_COUNT} lines"
      fi
      if [[ -n "$MISSING_SECTIONS" ]]; then
        REASON="${REASON:+$REASON, }missing: ${MISSING_SECTIONS%, }"
      fi
      echo "RE-EXTRACTING: $ch (incomplete: $REASON)"
    fi
  fi

  LOGFILE="$HOME/source/claude-cwd/tmp/extraction-${ch}.log"
  JSONFILE="$HOME/source/claude-cwd/tmp/extraction-${ch}.json"
  CH_START=$(date +%s)
  CH_START_FMT=$(date '+%Y-%m-%d %H:%M:%S')
  echo "--- Extracting: $ch ---"
  echo "    Started at $CH_START_FMT"

  PROMPT="You are a mechanical extraction agent for the Weirwood Network project.

First, read reference/architecture.md for entity types, edge types, confidence tiers, and file naming conventions.
Then read .claude/agents/mechanical-extractor.md for your full extraction schema and rules.
Then read the chapter file: ${SRC}

Produce the extraction and write it to: ${OUT}

Follow the schema exactly. Overwrite any existing file. Do not reference other chapters — treat this chapter in complete isolation."

  # Run claude with stream-json to capture token usage, tee text to log
  if claude -p --dangerously-skip-permissions --model claude-opus-4-6 --verbose \
       --output-format stream-json "$PROMPT" > "$JSONFILE" 2>&1; then
    STATUS="ok"
  else
    STATUS="fail"
  fi

  CH_END=$(date +%s)
  CH_END_FMT=$(date '+%Y-%m-%d %H:%M:%S')
  ELAPSED=$(( CH_END - CH_START ))

  # Extract token usage from the result event in stream-json output
  eval $(python3 -c "
import json
found = False
for line in open('$JSONFILE'):
    line = line.strip()
    if not line: continue
    try:
        obj = json.loads(line)
        if obj.get('type') == 'result' and not found:
            found = True
            u = obj.get('usage', {})
            print(f'INPUT_TOKENS={u.get(\"input_tokens\", 0)}')
            print(f'CACHE_CREATION={u.get(\"cache_creation_input_tokens\", 0)}')
            print(f'CACHE_READ={u.get(\"cache_read_input_tokens\", 0)}')
            print(f'OUTPUT_TOKENS={u.get(\"output_tokens\", 0)}')
            print(f'COST_USD={obj.get(\"total_cost_usd\", 0)}')
    except: pass
if not found:
    print('INPUT_TOKENS=0')
    print('CACHE_CREATION=0')
    print('CACHE_READ=0')
    print('OUTPUT_TOKENS=0')
    print('COST_USD=0')
" 2>/dev/null)
  TOTAL_TOKENS=$(( INPUT_TOKENS + CACHE_CREATION + CACHE_READ + OUTPUT_TOKENS ))

  # Extract readable text from the json for the text log
  python3 -c "
import json, sys
for line in open('$JSONFILE'):
    line = line.strip()
    if not line: continue
    try:
        obj = json.loads(line)
        if obj.get('type') == 'assistant' and 'message' in obj:
            for block in obj['message'].get('content', []):
                if block.get('type') == 'text':
                    print(block['text'])
    except: pass
" > "$LOGFILE" 2>/dev/null || true

  if [[ "$STATUS" == "ok" ]]; then
    echo "  ✅ $ch (${ELAPSED}s | in:${INPUT_TOKENS} cache_create:${CACHE_CREATION} cache_read:${CACHE_READ} out:${OUTPUT_TOKENS} | \$${COST_USD})"
    tail -3 "$LOGFILE" | sed 's/^/    /'
    SUCCESSES=$((SUCCESSES + 1))
    WAVE_INPUT_TOKENS=$(( WAVE_INPUT_TOKENS + INPUT_TOKENS + CACHE_CREATION + CACHE_READ ))
    WAVE_OUTPUT_TOKENS=$(( WAVE_OUTPUT_TOKENS + OUTPUT_TOKENS ))
  else
    echo "  ❌ $ch FAILED (${ELAPSED}s)"
    tail -10 "$JSONFILE" | sed 's/^/    /'
    FAILURES=$((FAILURES + 1))
    FAILED_LIST+=("$ch")
  fi

  # Append to stats CSV
  echo "$ch,$BOOK,$WAVE,$STATUS,$CH_START_FMT,$CH_END_FMT,$ELAPSED,$INPUT_TOKENS,$CACHE_CREATION,$CACHE_READ,$OUTPUT_TOKENS,$TOTAL_TOKENS,$COST_USD" >> "$STATS_FILE"
done

WAVE_ELAPSED=$(( $(date +%s) - WAVE_START ))
WAVE_TOTAL_TOKENS=$(( WAVE_INPUT_TOKENS + WAVE_OUTPUT_TOKENS ))

# Sum costs from this wave's CSV entries
WAVE_COST=$(python3 -c "
import csv, sys
total = 0.0
with open('$STATS_FILE') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('wave') == '$WAVE' and row.get('book') == '$BOOK':
            try: total += float(row.get('cost_usd', 0))
            except: pass
print(f'{total:.4f}')
" 2>/dev/null || echo "0")

echo ""
echo "=== ${BOOK^^} Wave $WAVE/$TOTAL_WAVES complete ==="
echo "Succeeded: $SUCCESSES / ${#WAVE_CHAPTERS[@]}"
echo "Failed: $FAILURES"
echo "Wall time: ${WAVE_ELAPSED}s"
echo "Tokens — input: $WAVE_INPUT_TOKENS | output: $WAVE_OUTPUT_TOKENS | total: $WAVE_TOTAL_TOKENS"
echo "Cost: \$${WAVE_COST}"
if (( FAILURES > 0 )); then
  echo "Failed chapters: ${FAILED_LIST[*]}"
fi

# Append to progress log
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
CHAPTER_LIST=$(IFS=', '; echo "${WAVE_CHAPTERS[*]}")
if (( FAILURES == 0 )); then
  echo "- **${BOOK^^} Wave $WAVE** ($TIMESTAMP) — $CHAPTER_LIST ✅ (${#WAVE_CHAPTERS[@]}/${#WAVE_CHAPTERS[@]}) [${WAVE_ELAPSED}s, ${WAVE_TOTAL_TOKENS} tokens]" >> working/progress.md
else
  FAIL_LIST_STR=$(IFS=', '; echo "${FAILED_LIST[*]}")
  echo "- **${BOOK^^} Wave $WAVE** ($TIMESTAMP) — $CHAPTER_LIST ⚠️ ($SUCCESSES/${#WAVE_CHAPTERS[@]}, failed: $FAIL_LIST_STR) [${WAVE_ELAPSED}s, ${WAVE_TOTAL_TOKENS} tokens]" >> working/progress.md
fi
