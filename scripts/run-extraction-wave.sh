#!/usr/bin/env bash
# run-extraction-wave.sh — Run Pass 1 mechanical extraction on a wave of AGOT chapters
#
# Usage:
#   ./scripts/run-extraction-wave.sh <wave_number>
#
# Waves are groups of 5 chapters (last wave has 3). Wave 1-5 already done.
# Run different waves in separate terminals for parallelism.
#
#   Terminal 1: ./scripts/run-extraction-wave.sh 6
#   Terminal 2: ./scripts/run-extraction-wave.sh 7
#   Terminal 3: ./scripts/run-extraction-wave.sh 8
#   ...
#
# Or run all remaining waves sequentially:
#   for w in $(seq 6 15); do ./scripts/run-extraction-wave.sh "$w"; done
#
# Outputs:
#   extractions/mechanical/agot/{chapter}.extraction.md  — the extraction
#   /tmp/extraction-{chapter}.log                        — claude stdout (text)
#   /tmp/extraction-{chapter}.json                       — full stream-json (token usage)
#   working/extraction-stats.csv                         — per-chapter timing & token log

set -euo pipefail
cd "$(dirname "$0")/.."

STATS_FILE="working/extraction-stats.csv"

# Create stats CSV with header if it doesn't exist
if [[ ! -f "$STATS_FILE" ]]; then
  echo "chapter,wave,status,start_time,end_time,duration_s,input_tokens,output_tokens,total_tokens" > "$STATS_FILE"
fi

# All 73 AGOT chapters in order
CHAPTERS=(
  agot-prologue
  agot-bran-01
  agot-catelyn-01
  agot-daenerys-01
  agot-eddard-01
  agot-jon-01
  agot-catelyn-02
  agot-arya-01
  agot-bran-02
  agot-tyrion-01
  agot-jon-02
  agot-daenerys-02
  agot-eddard-02
  agot-tyrion-02
  agot-catelyn-03
  agot-sansa-01
  agot-eddard-03
  agot-bran-03
  agot-catelyn-04
  agot-jon-03
  agot-eddard-04
  agot-tyrion-03
  agot-arya-02
  agot-daenerys-03
  agot-bran-04
  agot-eddard-05
  agot-jon-04
  agot-eddard-06
  agot-catelyn-05
  agot-sansa-02
  agot-eddard-07
  agot-tyrion-04
  agot-arya-03
  agot-eddard-08
  agot-catelyn-06
  agot-eddard-09
  agot-daenerys-04
  agot-bran-05
  agot-tyrion-05
  agot-eddard-10
  agot-catelyn-07
  agot-jon-05
  agot-tyrion-06
  agot-eddard-11
  agot-sansa-03
  agot-eddard-12
  agot-daenerys-05
  agot-eddard-13
  agot-jon-06
  agot-eddard-14
  agot-arya-04
  agot-sansa-04
  agot-jon-07
  agot-bran-06
  agot-daenerys-06
  agot-catelyn-08
  agot-tyrion-07
  agot-sansa-05
  agot-eddard-15
  agot-catelyn-09
  agot-jon-08
  agot-daenerys-07
  agot-tyrion-08
  agot-catelyn-10
  agot-daenerys-08
  agot-arya-05
  agot-bran-07
  agot-sansa-06
  agot-daenerys-09
  agot-tyrion-09
  agot-jon-09
  agot-catelyn-11
  agot-daenerys-10
)

WAVE_SIZE=5
WAVE=${1:?Usage: $0 <wave_number> (1-15)}

# Calculate slice
START=$(( (WAVE - 1) * WAVE_SIZE ))
END=$(( START + WAVE_SIZE ))
if (( END > ${#CHAPTERS[@]} )); then
  END=${#CHAPTERS[@]}
fi

if (( START >= ${#CHAPTERS[@]} )); then
  echo "Wave $WAVE is out of range (max 15)"
  exit 1
fi

WAVE_CHAPTERS=("${CHAPTERS[@]:$START:$((END - START))}")

echo "=== Wave $WAVE: chapters $((START+1))-$END of ${#CHAPTERS[@]} ==="
echo "Chapters: ${WAVE_CHAPTERS[*]}"
echo ""

WAVE_START=$(date +%s)
SUCCESSES=0
FAILURES=0
FAILED_LIST=()
WAVE_INPUT_TOKENS=0
WAVE_OUTPUT_TOKENS=0

for ch in "${WAVE_CHAPTERS[@]}"; do
  SRC="sources/chapters/agot/${ch}.md"
  OUT="extractions/mechanical/agot/${ch}.extraction.md"

  if [[ ! -f "$SRC" ]]; then
    echo "SKIP: $SRC not found"
    FAILURES=$((FAILURES + 1))
    FAILED_LIST+=("$ch (source missing)")
    echo "$ch,$WAVE,skip,,,,,," >> "$STATS_FILE"
    continue
  fi

  LOGFILE="/tmp/extraction-${ch}.log"
  JSONFILE="/tmp/extraction-${ch}.json"
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

  # Extract token usage from stream-json output
  # Look for the result message which contains usage stats
  INPUT_TOKENS=$(grep -o '"input_tokens":[0-9]*' "$JSONFILE" 2>/dev/null | tail -1 | cut -d: -f2)
  OUTPUT_TOKENS=$(grep -o '"output_tokens":[0-9]*' "$JSONFILE" 2>/dev/null | tail -1 | cut -d: -f2)
  INPUT_TOKENS=${INPUT_TOKENS:-0}
  OUTPUT_TOKENS=${OUTPUT_TOKENS:-0}
  TOTAL_TOKENS=$(( INPUT_TOKENS + OUTPUT_TOKENS ))

  # Also extract readable text from the json for the text log
  # Pull out assistant text content for readable log
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
    echo "  ✅ $ch (${ELAPSED}s | in:${INPUT_TOKENS} out:${OUTPUT_TOKENS} total:${TOTAL_TOKENS})"
    tail -3 "$LOGFILE" | sed 's/^/    /'
    SUCCESSES=$((SUCCESSES + 1))
    WAVE_INPUT_TOKENS=$(( WAVE_INPUT_TOKENS + INPUT_TOKENS ))
    WAVE_OUTPUT_TOKENS=$(( WAVE_OUTPUT_TOKENS + OUTPUT_TOKENS ))
  else
    echo "  ❌ $ch FAILED (${ELAPSED}s)"
    tail -10 "$JSONFILE" | sed 's/^/    /'
    FAILURES=$((FAILURES + 1))
    FAILED_LIST+=("$ch")
  fi

  # Append to stats CSV
  echo "$ch,$WAVE,$STATUS,$CH_START_FMT,$CH_END_FMT,$ELAPSED,$INPUT_TOKENS,$OUTPUT_TOKENS,$TOTAL_TOKENS" >> "$STATS_FILE"
done

WAVE_ELAPSED=$(( $(date +%s) - WAVE_START ))
WAVE_TOTAL_TOKENS=$(( WAVE_INPUT_TOKENS + WAVE_OUTPUT_TOKENS ))

echo ""
echo "=== Wave $WAVE complete ==="
echo "Succeeded: $SUCCESSES / ${#WAVE_CHAPTERS[@]}"
echo "Failed: $FAILURES"
echo "Wall time: ${WAVE_ELAPSED}s"
echo "Tokens — input: $WAVE_INPUT_TOKENS | output: $WAVE_OUTPUT_TOKENS | total: $WAVE_TOTAL_TOKENS"
if (( FAILURES > 0 )); then
  echo "Failed chapters: ${FAILED_LIST[*]}"
fi

# Append to progress log
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
CHAPTER_LIST=$(IFS=', '; echo "${WAVE_CHAPTERS[*]}")
if (( FAILURES == 0 )); then
  echo "- **Wave $WAVE** ($TIMESTAMP) — $CHAPTER_LIST ✅ (${#WAVE_CHAPTERS[@]}/${#WAVE_CHAPTERS[@]}) [${WAVE_ELAPSED}s, ${WAVE_TOTAL_TOKENS} tokens]" >> working/progress.md
else
  FAIL_LIST_STR=$(IFS=', '; echo "${FAILED_LIST[*]}")
  echo "- **Wave $WAVE** ($TIMESTAMP) — $CHAPTER_LIST ⚠️ ($SUCCESSES/${#WAVE_CHAPTERS[@]}, failed: $FAIL_LIST_STR) [${WAVE_ELAPSED}s, ${WAVE_TOTAL_TOKENS} tokens]" >> working/progress.md
fi
