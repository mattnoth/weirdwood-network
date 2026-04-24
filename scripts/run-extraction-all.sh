#!/usr/bin/env bash
# chmod +x scripts/run-extraction-all.sh
#
# run-extraction-all.sh — Run Pass 1 mechanical extraction across any ASOIAF book
#
# Usage:
#   ./scripts/run-extraction-all.sh --book agot
#   ./scripts/run-extraction-all.sh --book agot --force          # re-run everything
#   ./scripts/run-extraction-all.sh --book agot --dry-run        # show plan, no execution
#   ./scripts/run-extraction-all.sh --book agot --workers 3      # 3 parallel workers
#   ./scripts/run-extraction-all.sh --book agot --chapters agot-bran-01,agot-catelyn-01
#   ./scripts/run-extraction-all.sh --book agot --model claude-opus-4-6
#
# Resumability:
#   An extraction is considered complete if it contains "## Raw Entity List".
#   Files that exist but lack this section are "tarnished" and will be re-run.
#   Use --force to re-run all chapters regardless.
#
# Outputs:
#   extractions/mechanical/{book}/{chapter}.extraction.md  — the extraction
#   /tmp/extraction-{chapter}.log                          — claude stdout (text)
#   /tmp/extraction-{chapter}.json                         — full stream-json (token usage)
#   working/extraction-stats.csv                           — per-chapter timing & token log
#   working/progress.md                                    — appended wave summaries

set -euo pipefail

# ── Script location — all paths are relative to the repo root ──────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

# ── Defaults ───────────────────────────────────────────────────────────────────
BOOK=""
WORKERS=2
WAVE_SIZE=5
FORCE=false
DRY_RUN=false
MODEL="claude-opus-4-6"
CHERRY_PICK=""

STATS_FILE="working/extraction-stats.csv"
PROGRESS_FILE="working/progress.md"

# ── Helpers ────────────────────────────────────────────────────────────────────
usage() {
  cat <<EOF
Usage: $0 --book <book> [OPTIONS]

Required:
  --book <book>          One of: agot acok asos affc adwd

Options:
  --workers N            Parallel workers (default: 2)
  --wave-size N          Chapters per wave for progress reporting (default: 5)
  --force                Re-run all chapters, even complete ones
  --dry-run              Show what would run without executing
  --model <model>        Claude model to use (default: claude-opus-4-6)
  --chapters ch1,ch2     Run only specific chapters (comma-separated, no .md extension)
  --help                 Show this help message

Examples:
  $0 --book agot
  $0 --book agot --force --workers 3
  $0 --book agot --dry-run
  $0 --book agot --chapters agot-prologue,agot-bran-01
  $0 --book acok --model claude-opus-4-6
EOF
}

# Format seconds into Xh Ym Zs
format_duration() {
  local secs=$1
  local h=$(( secs / 3600 ))
  local m=$(( (secs % 3600) / 60 ))
  local s=$(( secs % 60 ))
  if (( h > 0 )); then
    printf "%dh %dm %ds" "$h" "$m" "$s"
  elif (( m > 0 )); then
    printf "%dm %ds" "$m" "$s"
  else
    printf "%ds" "$s"
  fi
}

# Format a large integer with commas
format_number() {
  printf "%'d" "$1" 2>/dev/null || echo "$1"
}

# Check whether an extraction file is complete (contains the final schema section)
is_complete() {
  local outfile=$1
  [[ -f "$outfile" ]] && grep -q "## Raw Entity List" "$outfile"
}

# ── Argument parsing ───────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --book)       BOOK="$2";        shift 2 ;;
    --workers)    WORKERS="$2";     shift 2 ;;
    --wave-size)  WAVE_SIZE="$2";   shift 2 ;;
    --force)      FORCE=true;       shift   ;;
    --dry-run)    DRY_RUN=true;     shift   ;;
    --model)      MODEL="$2";       shift 2 ;;
    --chapters)   CHERRY_PICK="$2"; shift 2 ;;
    --help|-h)    usage; exit 0 ;;
    *)
      echo "ERROR: Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$BOOK" ]]; then
  echo "ERROR: --book is required" >&2
  usage >&2
  exit 1
fi

case "$BOOK" in
  agot|acok|asos|affc|adwd) ;;
  *)
    echo "ERROR: Unknown book '$BOOK'. Must be one of: agot acok asos affc adwd" >&2
    exit 1
    ;;
esac

BOOK_UPPER="${BOOK^^}"

# ── Discover chapters ──────────────────────────────────────────────────────────
CHAPTER_DIR="sources/chapters/${BOOK}"
EXTRACTION_DIR="extractions/mechanical/${BOOK}"

if [[ ! -d "$CHAPTER_DIR" ]]; then
  echo "ERROR: Chapter directory not found: $CHAPTER_DIR" >&2
  exit 1
fi

mkdir -p "$EXTRACTION_DIR"

# Build chapter list
if [[ -n "$CHERRY_PICK" ]]; then
  # Cherry-pick mode: user supplies comma-separated chapter stems
  IFS=',' read -ra ALL_CHAPTERS <<< "$CHERRY_PICK"
  # Trim whitespace from each entry
  CHAPTERS=()
  for ch in "${ALL_CHAPTERS[@]}"; do
    ch="${ch// /}"
    CHAPTERS+=("$ch")
  done
else
  # Auto-discover: glob and sort (filenames already sort correctly)
  mapfile -t CHAPTER_PATHS < <(ls "${CHAPTER_DIR}"/*.md 2>/dev/null | sort)
  if [[ ${#CHAPTER_PATHS[@]} -eq 0 ]]; then
    echo "ERROR: No chapter files found in $CHAPTER_DIR" >&2
    exit 1
  fi
  CHAPTERS=()
  for p in "${CHAPTER_PATHS[@]}"; do
    stem="$(basename "$p" .md)"
    CHAPTERS+=("$stem")
  done
fi

TOTAL_CHAPTERS=${#CHAPTERS[@]}

# ── Classify chapters ──────────────────────────────────────────────────────────
# Each chapter is: skip | tarnished | pending
declare -A CH_STATUS

COUNT_SKIP=0
COUNT_TARNISHED=0
COUNT_PENDING=0

for ch in "${CHAPTERS[@]}"; do
  outfile="${EXTRACTION_DIR}/${ch}.extraction.md"
  srcfile="${CHAPTER_DIR}/${ch}.md"

  if [[ ! -f "$srcfile" ]]; then
    CH_STATUS[$ch]="missing_source"
    continue
  fi

  if $FORCE; then
    CH_STATUS[$ch]="pending"
    COUNT_PENDING=$(( COUNT_PENDING + 1 ))
  elif is_complete "$outfile"; then
    CH_STATUS[$ch]="skip"
    COUNT_SKIP=$(( COUNT_SKIP + 1 ))
  elif [[ -f "$outfile" ]]; then
    CH_STATUS[$ch]="tarnished"
    COUNT_TARNISHED=$(( COUNT_TARNISHED + 1 ))
  else
    CH_STATUS[$ch]="pending"
    COUNT_PENDING=$(( COUNT_PENDING + 1 ))
  fi
done

COUNT_MISSING_SOURCE=0
for ch in "${CHAPTERS[@]}"; do
  if [[ "${CH_STATUS[$ch]:-}" == "missing_source" ]]; then
    COUNT_MISSING_SOURCE=$(( COUNT_MISSING_SOURCE + 1 ))
  fi
done

# ── Dry run ────────────────────────────────────────────────────────────────────
if $DRY_RUN; then
  echo "=== Dry run: ${BOOK_UPPER} extraction plan ==="
  echo "Book:          $BOOK_UPPER"
  echo "Model:         $MODEL"
  echo "Workers:       $WORKERS"
  echo "Wave size:     $WAVE_SIZE"
  echo "Force:         $FORCE"
  echo ""
  echo "Total chapters:       $TOTAL_CHAPTERS"
  echo "Skip (complete):      $COUNT_SKIP"
  echo "Re-run (tarnished):   $COUNT_TARNISHED"
  echo "Run (pending):        $COUNT_PENDING"
  echo "Missing source:       $COUNT_MISSING_SOURCE"
  echo ""

  WILL_RUN=0
  for ch in "${CHAPTERS[@]}"; do
    status="${CH_STATUS[$ch]:-missing_source}"
    case "$status" in
      skip)
        echo "  SKIP      $ch"
        ;;
      tarnished)
        echo "  TARNISHED $ch  (incomplete, will re-run)"
        WILL_RUN=$(( WILL_RUN + 1 ))
        ;;
      pending)
        echo "  RUN       $ch"
        WILL_RUN=$(( WILL_RUN + 1 ))
        ;;
      missing_source)
        echo "  ERROR     $ch  (source file not found)"
        ;;
    esac
  done
  echo ""
  echo "Chapters that will be run: $WILL_RUN"
  exit 0
fi

# ── Stats CSV ──────────────────────────────────────────────────────────────────
if [[ ! -f "$STATS_FILE" ]]; then
  echo "chapter,wave,status,start_time,end_time,duration_s,input_tokens,output_tokens,total_tokens" > "$STATS_FILE"
fi

# ── Concurrency infrastructure ─────────────────────────────────────────────────
# We use a simple semaphore: a temp directory where each running job drops a
# lock file named after its PID. The main loop waits when the slot count is full.

JOB_DIR=$(mktemp -d /tmp/extraction-jobs-XXXXXX)
cleanup() {
  rm -rf "$JOB_DIR"
}
trap cleanup EXIT

# Track per-job results via temp files so subshells can communicate to parent
RESULT_DIR=$(mktemp -d /tmp/extraction-results-XXXXXX)
trap 'rm -rf "$RESULT_DIR"' EXIT

running_jobs() {
  # Count lock files in JOB_DIR
  shopt -s nullglob
  local files=("$JOB_DIR"/*.lock)
  echo "${#files[@]}"
}

wait_for_slot() {
  while (( $(running_jobs) >= WORKERS )); do
    # Reap any finished background processes
    wait -n 2>/dev/null || true
  done
}

acquire_slot() {
  local pid=$1
  touch "$JOB_DIR/${pid}.lock"
}

release_slot() {
  local pid=$1
  rm -f "$JOB_DIR/${pid}.lock"
}

# ── Per-chapter extraction function ───────────────────────────────────────────
# Runs in a subshell (background). Writes a result file to RESULT_DIR.
run_chapter() {
  local ch=$1
  local wave=$2
  local original_status=$3

  local srcfile="${CHAPTER_DIR}/${ch}.md"
  local outfile="${EXTRACTION_DIR}/${ch}.extraction.md"
  local logfile="/tmp/extraction-${ch}.log"
  local jsonfile="/tmp/extraction-${ch}.json"
  local resultfile="${RESULT_DIR}/${ch}.result"

  local CH_START CH_START_FMT CH_END CH_END_FMT ELAPSED
  CH_START=$(date +%s)
  CH_START_FMT=$(date '+%Y-%m-%d %H:%M:%S')

  echo "--- [Wave ${wave}] Extracting: $ch ---"
  echo "    Status before: $original_status | Started: $CH_START_FMT"

  local PROMPT
  PROMPT="You are a mechanical extraction agent for the Weirwood Network project.

First, read reference/architecture.md for entity types, edge types, confidence tiers, and file naming conventions.
Then read .claude/agents/mechanical-extractor.md for your full extraction schema and rules.
Then read the chapter source file: ${srcfile}

Produce the extraction and write it to: ${outfile}

Follow the schema exactly. Overwrite any existing file at that path.
Treat this chapter in complete isolation — do not reference other chapters or use external ASOIAF knowledge to make inferences beyond what the text shows."

  local STATUS
  # Run claude; capture stream-json for token counting
  if claude -p --dangerously-skip-permissions \
       --model "$MODEL" \
       --verbose \
       --output-format stream-json \
       "$PROMPT" > "$jsonfile" 2>&1; then
    STATUS="ok"
  else
    STATUS="fail"
  fi

  CH_END=$(date +%s)
  CH_END_FMT=$(date '+%Y-%m-%d %H:%M:%S')
  ELAPSED=$(( CH_END - CH_START ))

  # Extract token usage from the last occurrence of each key in the stream-json
  local INPUT_TOKENS OUTPUT_TOKENS TOTAL_TOKENS
  INPUT_TOKENS=$(grep -o '"input_tokens":[0-9]*' "$jsonfile" 2>/dev/null | tail -1 | cut -d: -f2 || echo "0")
  OUTPUT_TOKENS=$(grep -o '"output_tokens":[0-9]*' "$jsonfile" 2>/dev/null | tail -1 | cut -d: -f2 || echo "0")
  INPUT_TOKENS=${INPUT_TOKENS:-0}
  OUTPUT_TOKENS=${OUTPUT_TOKENS:-0}
  TOTAL_TOKENS=$(( INPUT_TOKENS + OUTPUT_TOKENS ))

  # Extract readable text from stream-json into the log file
  python3 -c "
import json, sys
for line in open('$jsonfile'):
    line = line.strip()
    if not line: continue
    try:
        obj = json.loads(line)
        if obj.get('type') == 'assistant' and 'message' in obj:
            for block in obj['message'].get('content', []):
                if block.get('type') == 'text':
                    print(block['text'])
    except: pass
" > "$logfile" 2>/dev/null || true

  # Validate completeness even on "ok" exit — truncation can produce exit 0
  local FINAL_STATUS="$STATUS"
  if [[ "$STATUS" == "ok" ]]; then
    if is_complete "$outfile"; then
      FINAL_STATUS="ok"
    else
      FINAL_STATUS="tarnished"
    fi
  fi

  # Print result line
  if [[ "$FINAL_STATUS" == "ok" ]]; then
    echo "  OK        $ch (${ELAPSED}s | in:${INPUT_TOKENS} out:${OUTPUT_TOKENS} total:${TOTAL_TOKENS})"
    tail -3 "$logfile" 2>/dev/null | sed 's/^/              /' || true
  elif [[ "$FINAL_STATUS" == "tarnished" ]]; then
    echo "  TARNISHED $ch — completed but output missing '## Raw Entity List' (${ELAPSED}s)"
    tail -5 "$jsonfile" 2>/dev/null | sed 's/^/              /' || true
  else
    echo "  FAILED    $ch (${ELAPSED}s)"
    tail -10 "$jsonfile" 2>/dev/null | sed 's/^/              /' || true
  fi

  # Write result file for parent to pick up
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$ch" "$wave" "$FINAL_STATUS" \
    "$CH_START_FMT" "$CH_END_FMT" "$ELAPSED" \
    "$INPUT_TOKENS" "$OUTPUT_TOKENS" "$TOTAL_TOKENS" \
    > "$resultfile"
}

# ── Build the run list (pending + tarnished) ───────────────────────────────────
RUN_LIST=()
for ch in "${CHAPTERS[@]}"; do
  status="${CH_STATUS[$ch]:-missing_source}"
  if [[ "$status" == "pending" || "$status" == "tarnished" ]]; then
    RUN_LIST+=("$ch")
  fi
done

COUNT_TO_RUN=${#RUN_LIST[@]}

# ── Header ─────────────────────────────────────────────────────────────────────
echo ""
echo "=== ${BOOK_UPPER} Pass 1 Mechanical Extraction ==="
echo "Model:         $MODEL"
echo "Workers:       $WORKERS"
echo "Wave size:     $WAVE_SIZE"
echo "Force:         $FORCE"
echo ""
echo "Total chapters:       $TOTAL_CHAPTERS"
echo "Skip (complete):      $COUNT_SKIP"
echo "Tarnished (re-run):   $COUNT_TARNISHED"
echo "Pending (new):        $COUNT_PENDING"
echo "Missing source:       $COUNT_MISSING_SOURCE"
echo "Will run now:         $COUNT_TO_RUN"
echo ""

if (( COUNT_TO_RUN == 0 )); then
  echo "Nothing to do. All chapters are complete. Use --force to re-run."
  exit 0
fi

# ── Main extraction loop ───────────────────────────────────────────────────────
RUN_START=$(date +%s)

# Counters — updated after each job completes
SUCCEEDED=0
FAILED=0
TARNISHED_OUTPUT=0
FAILED_LIST=()

WAVE_NUM=0
WAVE_SUCCEEDED=0
WAVE_FAILED=0
WAVE_INPUT=0
WAVE_OUTPUT=0
WAVE_START_TIME=$(date +%s)
WAVE_CHAPTERS_IN_WAVE=()

# We need to process jobs in order but allow parallel execution.
# Strategy: launch up to WORKERS jobs at once; for each completed job, collect results.
# We track launched PIDs in order.

declare -a LAUNCHED_PIDS
declare -A PID_TO_CHAPTER

collect_result() {
  local ch=$1
  local resultfile="${RESULT_DIR}/${ch}.result"
  if [[ ! -f "$resultfile" ]]; then
    echo "WARNING: No result file for $ch" >&2
    return
  fi

  IFS=$'\t' read -r _ch wave final_status ch_start ch_end elapsed in_tok out_tok total_tok < "$resultfile"

  # Append to stats CSV
  echo "${ch},${wave},${final_status},${ch_start},${ch_end},${elapsed},${in_tok},${out_tok},${total_tok}" >> "$STATS_FILE"

  # Update counters
  case "$final_status" in
    ok)
      SUCCEEDED=$(( SUCCEEDED + 1 ))
      WAVE_SUCCEEDED=$(( WAVE_SUCCEEDED + 1 ))
      WAVE_INPUT=$(( WAVE_INPUT + in_tok ))
      WAVE_OUTPUT=$(( WAVE_OUTPUT + out_tok ))
      ;;
    tarnished)
      TARNISHED_OUTPUT=$(( TARNISHED_OUTPUT + 1 ))
      WAVE_FAILED=$(( WAVE_FAILED + 1 ))
      FAILED_LIST+=("$ch (tarnished output)")
      WAVE_INPUT=$(( WAVE_INPUT + in_tok ))
      WAVE_OUTPUT=$(( WAVE_OUTPUT + out_tok ))
      ;;
    fail)
      FAILED=$(( FAILED + 1 ))
      WAVE_FAILED=$(( WAVE_FAILED + 1 ))
      FAILED_LIST+=("$ch")
      ;;
  esac
}

flush_wave_summary() {
  local wave=$1
  local wave_elapsed=$(( $(date +%s) - WAVE_START_TIME ))
  local wave_total_tokens=$(( WAVE_INPUT + WAVE_OUTPUT ))
  local wave_ch_count=${#WAVE_CHAPTERS_IN_WAVE[@]}
  local timestamp
  timestamp=$(date '+%Y-%m-%d %H:%M')
  local chapter_list
  chapter_list=$(IFS=', '; echo "${WAVE_CHAPTERS_IN_WAVE[*]}")

  if (( WAVE_FAILED == 0 )); then
    echo "- **${BOOK_UPPER} Wave ${wave}** (${timestamp}) — ${chapter_list} (${wave_ch_count}/${wave_ch_count} ok) [$(format_duration "$wave_elapsed"), in:${WAVE_INPUT} out:${WAVE_OUTPUT} total:${wave_total_tokens}]" >> "$PROGRESS_FILE"
  else
    echo "- **${BOOK_UPPER} Wave ${wave}** (${timestamp}) — ${chapter_list} (${WAVE_SUCCEEDED}/${wave_ch_count} ok, failed: $(IFS=', '; echo "${FAILED_LIST[*]}")) [$(format_duration "$wave_elapsed"), in:${WAVE_INPUT} out:${WAVE_OUTPUT} total:${wave_total_tokens}]" >> "$PROGRESS_FILE"
  fi

  echo ""
  echo "--- Wave ${wave} summary: ${WAVE_SUCCEEDED}/${wave_ch_count} ok | $(format_duration "$wave_elapsed") | tokens in:${WAVE_INPUT} out:${WAVE_OUTPUT} ---"
  echo ""
}

reset_wave() {
  WAVE_SUCCEEDED=0
  WAVE_FAILED=0
  WAVE_INPUT=0
  WAVE_OUTPUT=0
  WAVE_START_TIME=$(date +%s)
  WAVE_CHAPTERS_IN_WAVE=()
}

CHAPTER_IDX=0
CURRENT_WAVE_IDX=0

# We process jobs in-order using a simple pipeline approach:
# Launch up to WORKERS at once. When a worker slot frees, launch the next chapter.
# After every WAVE_SIZE completions, flush the wave summary.

# Use an ordered queue of (ch, original_status, wave_num) and a PID queue
declare -a PENDING_QUEUE_CH
declare -a PENDING_QUEUE_STATUS
declare -a PENDING_QUEUE_WAVE

for ch in "${RUN_LIST[@]}"; do
  CHAPTER_IDX=$(( CHAPTER_IDX + 1 ))
  wave_for_ch=$(( (CHAPTER_IDX - 1) / WAVE_SIZE + 1 ))
  PENDING_QUEUE_CH+=("$ch")
  PENDING_QUEUE_STATUS+=("${CH_STATUS[$ch]}")
  PENDING_QUEUE_WAVE+=("$wave_for_ch")
done

# Reset counters for actual wave tracking
WAVE_NUM=1
CHAPTERS_COMPLETED=0

# Running jobs: pid -> chapter name
declare -A RUNNING_PID_TO_CH
declare -a RUNNING_PIDS

launch_next=0  # index into PENDING_QUEUE

# Drain all remaining pending chapters
while (( launch_next < COUNT_TO_RUN || ${#RUNNING_PIDS[@]} > 0 )); do

  # Launch jobs while slots are available and work remains
  while (( launch_next < COUNT_TO_RUN && ${#RUNNING_PIDS[@]} < WORKERS )); do
    ch="${PENDING_QUEUE_CH[$launch_next]}"
    orig_status="${PENDING_QUEUE_STATUS[$launch_next]}"
    ch_wave="${PENDING_QUEUE_WAVE[$launch_next]}"
    launch_next=$(( launch_next + 1 ))

    WAVE_CHAPTERS_IN_WAVE+=("$ch")

    # Launch in background subshell
    run_chapter "$ch" "$ch_wave" "$orig_status" &
    bg_pid=$!
    RUNNING_PIDS+=("$bg_pid")
    RUNNING_PID_TO_CH[$bg_pid]="$ch"
    acquire_slot "$bg_pid"
  done

  # Wait for at least one job to finish
  if (( ${#RUNNING_PIDS[@]} > 0 )); then
    # Wait for any child to finish
    finished_pid=""
    for pid in "${RUNNING_PIDS[@]}"; do
      if ! kill -0 "$pid" 2>/dev/null; then
        finished_pid="$pid"
        break
      fi
    done

    if [[ -z "$finished_pid" ]]; then
      # All still running — wait for any one
      wait -n "${RUNNING_PIDS[@]}" 2>/dev/null || true
      # Find which one finished
      for pid in "${RUNNING_PIDS[@]}"; do
        if ! kill -0 "$pid" 2>/dev/null; then
          finished_pid="$pid"
          break
        fi
      done
    fi

    if [[ -n "$finished_pid" ]]; then
      finished_ch="${RUNNING_PID_TO_CH[$finished_pid]}"
      release_slot "$finished_pid"
      # Remove from RUNNING arrays
      new_pids=()
      for pid in "${RUNNING_PIDS[@]}"; do
        [[ "$pid" != "$finished_pid" ]] && new_pids+=("$pid")
      done
      RUNNING_PIDS=("${new_pids[@]}")
      unset "RUNNING_PID_TO_CH[$finished_pid]"

      collect_result "$finished_ch"
      CHAPTERS_COMPLETED=$(( CHAPTERS_COMPLETED + 1 ))

      # Check if we've completed a full wave
      if (( CHAPTERS_COMPLETED % WAVE_SIZE == 0 || CHAPTERS_COMPLETED == COUNT_TO_RUN )); then
        # Only flush if this wave has chapters
        if (( ${#WAVE_CHAPTERS_IN_WAVE[@]} > 0 )); then
          flush_wave_summary "$WAVE_NUM"
          WAVE_NUM=$(( WAVE_NUM + 1 ))
          reset_wave
        fi
      fi
    fi
  fi

done

# ── Final summary ──────────────────────────────────────────────────────────────
RUN_END=$(date +%s)
RUN_ELAPSED=$(( RUN_END - RUN_START ))

TOTAL_SKIPPED=$COUNT_SKIP
TOTAL_TARNISHED_INPUT=$COUNT_TARNISHED
TOTAL_SUCCEEDED=$SUCCEEDED
TOTAL_FAILED=$(( FAILED + TARNISHED_OUTPUT ))

# Tally all token counts from stats CSV for this run session only
# (Only rows appended this session — keyed by chapters in RUN_LIST)
GRAND_INPUT=0
GRAND_OUTPUT=0
for ch in "${RUN_LIST[@]}"; do
  resultfile="${RESULT_DIR}/${ch}.result"
  if [[ -f "$resultfile" ]]; then
    IFS=$'\t' read -r _ch _wave _status _cs _ce _elapsed in_tok out_tok _total < "$resultfile"
    GRAND_INPUT=$(( GRAND_INPUT + in_tok ))
    GRAND_OUTPUT=$(( GRAND_OUTPUT + out_tok ))
  fi
done
GRAND_TOTAL=$(( GRAND_INPUT + GRAND_OUTPUT ))

echo ""
echo "=== Extraction complete: ${BOOK_UPPER} ==="
echo "Total chapters:          $TOTAL_CHAPTERS"
echo "Skipped (complete):      $TOTAL_SKIPPED"
echo "Re-run (tarnished in):   $TOTAL_TARNISHED_INPUT"
echo "Succeeded:               $TOTAL_SUCCEEDED"
echo "Failed:                  $TOTAL_FAILED"
if (( COUNT_MISSING_SOURCE > 0 )); then
echo "Missing source files:    $COUNT_MISSING_SOURCE"
fi
echo "Wall time:               $(format_duration "$RUN_ELAPSED")"
echo "Tokens — input: $(format_number "$GRAND_INPUT") | output: $(format_number "$GRAND_OUTPUT") | total: $(format_number "$GRAND_TOTAL")"

if (( ${#FAILED_LIST[@]} > 0 )); then
  echo ""
  echo "Failed chapters (re-run with --chapters flag):"
  for fc in "${FAILED_LIST[@]}"; do
    echo "  $fc"
  done
  echo ""
  # Build comma-separated list for copy-paste
  FAILED_STEMS=()
  for fc in "${FAILED_LIST[@]}"; do
    # Strip any trailing parenthetical note like " (tarnished output)"
    stem="${fc%% (*}"
    FAILED_STEMS+=("$stem")
  done
  IFS=','
  echo "  --chapters ${FAILED_STEMS[*]}"
  unset IFS
fi

# Append final summary to progress.md
{
  echo ""
  echo "### ${BOOK_UPPER} Pass 1 run — $(date '+%Y-%m-%d %H:%M')"
  echo "- Total: $TOTAL_CHAPTERS | Skipped: $TOTAL_SKIPPED | Succeeded: $TOTAL_SUCCEEDED | Failed: $TOTAL_FAILED | Wall time: $(format_duration "$RUN_ELAPSED")"
  echo "- Tokens: input=$(format_number "$GRAND_INPUT") output=$(format_number "$GRAND_OUTPUT") total=$(format_number "$GRAND_TOTAL")"
  if (( ${#FAILED_LIST[@]} > 0 )); then
    echo "- Failed: ${FAILED_LIST[*]}"
  fi
} >> "$PROGRESS_FILE"

# Exit with non-zero if any failures
if (( TOTAL_FAILED > 0 )); then
  exit 1
fi
