#!/usr/bin/env bash
# extract.sh — Unified extraction script for the Weirwood Network project
#
# Subcommands:
#   run     Run extraction on a single wave (called by iTerm tabs)
#   status  Show extraction progress
#   launch  Open iTerm tabs to run waves in parallel
#
# The shell function `weirwood` in terminal-collection wraps this.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

STATS_DIR="working/extraction-stats"
PROGRESS_FILE="working/progress.md"
WORKLOG_FILE="worklog.md"
WAVE_SIZE=5
DEFAULT_MODEL="claude-opus-4-6"
PASS="pass1"
VERSION="v3"
TERMINAL_ID="${HOSTNAME}-$$"

# Per-book stats file: working/extraction-stats/extraction-stats-{book}-{pass}-{version}.csv
stats_file_for() {
  echo "${STATS_DIR}/extraction-stats-${1}-${PASS}-${VERSION}.csv"
}

# ── Helpers ───────────────────────────────────────────────────────────────────

format_duration() {
  local secs=$1
  local h=$(( secs / 3600 )) m=$(( (secs % 3600) / 60 )) s=$(( secs % 60 ))
  if (( h > 0 )); then printf "%dh %dm %ds" "$h" "$m" "$s"
  elif (( m > 0 )); then printf "%dm %ds" "$m" "$s"
  else printf "%ds" "$s"; fi
}

format_number() { printf "%'d" "$1" 2>/dev/null || echo "$1"; }

now_iso() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }

# ── CSV locking (mkdir is POSIX-atomic, zero brew dependencies) ───────────────
#
# Uses ${STATS_FILE}.lockdir as the lock primitive.
# STATS_FILE is set as a local in cmd_run; bash's dynamic scoping makes it
# accessible from these helpers when called within cmd_run's call stack.

acquire_stats_lock() {
  local lockdir="${STATS_FILE}.lockdir"
  local tries=0
  while ! mkdir "$lockdir" 2>/dev/null; do
    tries=$(( tries + 1 ))
    if (( tries > 40 )); then
      echo "ERROR: CSV lock timeout (${lockdir})" >&2
      return 1
    fi
    sleep 0.5
  done
}

release_stats_lock() {
  rmdir "${STATS_FILE}.lockdir" 2>/dev/null || true
}

# ── Atomic chapter claim (Bug B fix) ─────────────────────────────────────────
#
# Acquires the CSV lock, delegates to claim-chapter.py (which reads/modifies
# the CSV atomically), releases the lock. Prints the claim result.
#
# Outputs one of:
#   claim              — chapter was free; started row appended
#   claim-after-stale  — stale claim cleared; started row appended
#   skip-already-done  — latest row is done/skipped-done
#   skip-claimed:<tid> — another terminal holds an active claim

claim_chapter() {
  local ch="$1" wave_num="$2" now
  now=$(now_iso)
  acquire_stats_lock || { echo "skip-claimed:lock-error"; return 1; }
  local result
  result=$(python3 scripts/claim-chapter.py \
    "$STATS_FILE" "$ch" "$wave_num" "$now" "$TERMINAL_ID" "$book" 2>/dev/null) || result="claim"
  release_stats_lock
  echo "$result"
}

# ── Update worklog.md checklist ───────────────────────────────────────────────

update_worklog() {
  local book=$1
  local extract_dir="extractions/mechanical/${book}"

  local done=0 total=0
  local chapter_dir="sources/chapters/${book}"
  for f in "$chapter_dir"/*.md; do
    total=$(( total + 1 ))
    local stem
    stem=$(basename "$f" .md)
    if is_complete "${extract_dir}/${stem}.extraction.md"; then
      done=$(( done + 1 ))
    fi
  done

  local new_line
  if (( done == total )); then
    new_line="- [x] Pass 1 ${VERSION} run on ${book^^} (${done}/${total} — complete)"
  else
    local completed_waves=""
    discover_chapters "$book"
    for (( w=1; w<=TOTAL_WAVES; w++ )); do
      local ws=$(( (w - 1) * WAVE_SIZE ))
      local we=$(( ws + WAVE_SIZE ))
      (( we > ${#CHAPTERS[@]} )) && we=${#CHAPTERS[@]}
      local wave_ok=true
      for (( i=ws; i<we; i++ )); do
        if ! is_complete "${extract_dir}/${CHAPTERS[$i]}.extraction.md"; then
          wave_ok=false; break
        fi
      done
      if $wave_ok; then
        completed_waves="${completed_waves:+$completed_waves, }$w"
      fi
    done
    if [[ -n "$completed_waves" ]]; then
      new_line="- [ ] Pass 1 ${VERSION} run on ${book^^} (${done}/${total} — waves ${completed_waves} complete)"
    else
      new_line="- [ ] Pass 1 ${VERSION} run on ${book^^} (${done}/${total})"
    fi
  fi

  local book_upper="${book^^}"
  if grep -q "Pass 1 ${VERSION} run on ${book_upper}" "$WORKLOG_FILE" 2>/dev/null; then
    sed -i '' "s|^- \[.\] Pass 1 ${VERSION} run on ${book_upper}.*|${new_line}|" "$WORKLOG_FILE"
    echo "Updated worklog: ${new_line}"
  else
    echo "Warning: no worklog line found for 'Pass 1 ${VERSION} run on ${book_upper}'"
  fi
}

# ── is_complete / discover_chapters / find_incomplete_waves ───────────────────

is_complete() {
  local outfile=$1
  [[ ! -f "$outfile" ]] && return 1
  local line_count
  line_count=$(wc -l < "$outfile" | tr -d ' ')
  (( line_count < 100 )) && return 1
  for section in "## Characters" "## Events" "## Locations" "## Relationships"; do
    grep -q "$section" "$outfile" || return 1
  done
  return 0
}

discover_chapters() {
  local book=$1
  local chapter_dir="sources/chapters/${book}"
  if [[ ! -d "$chapter_dir" ]]; then
    echo "ERROR: Chapter directory not found: $chapter_dir" >&2
    exit 1
  fi
  CHAPTERS=()
  for f in "$chapter_dir"/*.md; do
    CHAPTERS+=("$(basename "$f" .md)")
  done
  if (( ${#CHAPTERS[@]} == 0 )); then
    echo "ERROR: No .md files found in $chapter_dir" >&2
    exit 1
  fi
  TOTAL_WAVES=$(( (${#CHAPTERS[@]} + WAVE_SIZE - 1) / WAVE_SIZE ))
}

find_incomplete_waves() {
  local book=$1
  local extract_dir="extractions/mechanical/${book}"
  INCOMPLETE_WAVES=()
  for (( w=1; w<=TOTAL_WAVES; w++ )); do
    local start=$(( (w - 1) * WAVE_SIZE ))
    local end=$(( start + WAVE_SIZE ))
    (( end > ${#CHAPTERS[@]} )) && end=${#CHAPTERS[@]}
    local wave_complete=true
    for (( i=start; i<end; i++ )); do
      local ch="${CHAPTERS[$i]}"
      if ! is_complete "${extract_dir}/${ch}.extraction.md"; then
        wave_complete=false
        break
      fi
    done
    if [[ "$wave_complete" == false ]]; then
      INCOMPLETE_WAVES+=("$w")
    fi
  done
}

# ── Usage ─────────────────────────────────────────────────────────────────────

usage() {
  cat <<'EOF'
extract.sh — Unified extraction for the Weirwood Network

Subcommands:
  extract.sh check                                   Verify source files & prerequisites
  extract.sh status <book>                           Show progress (wave table)
  extract.sh launch <book> -t <N> -w <N> [-m model]  Open iTerm tabs to run waves
  extract.sh run <book> --wave <N> [-m model]        Run a single wave (used by iTerm tabs)

Shortcut (via shell function — use this instead):
  weirwood                 # help + all-books overview
  weirwood acok            # detailed status for one book
  weirwood acok 2 3        # launch: 2 terminals, 3 waves each
  weirwood acok 2 3 claude-sonnet-4-6  # launch with specific model
  weirwood stop            # soft stop — halt after current wave

Race protection:
  Each chapter is claimed atomically via a CSV-based lock before extraction
  starts. A second terminal starting the same wave will see the claim and
  skip already-claimed chapters. Stale claims (from crashed terminals) are
  automatically cleared on startup via extract-status-sweep.py.

Soft stop:
  'weirwood stop' (or 'touch /tmp/extraction-stop') creates a marker file.
  Terminals check for it between waves. The current wave finishes normally,
  then the terminal exits instead of starting the next wave. Never interrupts
  mid-chapter. The marker is cleared automatically on the next launch.

Books: agot acok asos affc adwd
Default model: claude-opus-4-6
EOF
}

# ── CMD: status ───────────────────────────────────────────────────────────────

cmd_status() {
  local book="${1:-agot}"
  local extract_dir="extractions/mechanical/${book}"
  mkdir -p "$extract_dir"

  discover_chapters "$book"

  local done_count=0 missing_count=0
  local -a missing_chapters
  for ch in "${CHAPTERS[@]}"; do
    if is_complete "${extract_dir}/${ch}.extraction.md"; then
      done_count=$(( done_count + 1 ))
    else
      missing_count=$(( missing_count + 1 ))
      missing_chapters+=("$ch")
    fi
  done

  # Token summary from stats CSV
  local STATS_FILE
  STATS_FILE=$(stats_file_for "$book")
  local cost_summary=""
  if [[ -f "$STATS_FILE" ]]; then
    cost_summary=$(python3 -c "
import csv
total_input = 0; total_output = 0; chapters_tracked = 0
with open('$STATS_FILE') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('status') not in ('done', 'ok'): continue
        chapters_tracked += 1
        try: total_input += int(row.get('cache_read_tokens', 0)) + int(row.get('cache_creation_tokens', 0)) + int(row.get('input_tokens', 0))
        except: pass
        try: total_output += int(row.get('output_tokens', 0))
        except: pass
if chapters_tracked > 0:
    print(f'Tokens so far: {total_input:,} in / {total_output:,} out across {chapters_tracked} chapters')
" 2>/dev/null || echo "")
  fi

  echo ""
  echo "=== ${book^^} Extraction Status ==="
  echo ""
  echo "${done_count} of ${#CHAPTERS[@]} chapters extracted. ${missing_count} remaining. (${TOTAL_WAVES} waves total)"
  echo ""

  if [[ -n "$cost_summary" ]]; then
    echo "$cost_summary"
    echo ""
  fi

  if (( missing_count == 0 )); then
    echo "All chapters extracted! Ready for the next pass."
    return 0
  fi

  declare -A wave_missing
  local -a wave_order
  for (( i=0; i<${#CHAPTERS[@]}; i++ )); do
    local ch="${CHAPTERS[$i]}"
    local w=$(( i / WAVE_SIZE + 1 ))
    if ! is_complete "${extract_dir}/${ch}.extraction.md"; then
      if [[ -z "${wave_missing[$w]:-}" ]]; then
        wave_missing[$w]="$ch"
        wave_order+=("$w")
      else
        wave_missing[$w]="${wave_missing[$w]}, $ch"
      fi
    fi
  done

  local -a done_waves=()
  for (( w=1; w<=TOTAL_WAVES; w++ )); do
    [[ -z "${wave_missing[$w]:-}" ]] && done_waves+=("$w")
  done
  if (( ${#done_waves[@]} > 0 )); then
    echo "Completed waves: $(IFS=', '; echo "${done_waves[*]}")"
    echo ""
  fi

  local wcol=5 ccol=10
  for w in "${wave_order[@]}"; do
    (( ${#wave_missing[$w]} > ccol )) && ccol=${#wave_missing[$w]}
  done

  printf "%-${wcol}s | %-${ccol}s | %s\n" "Wave" "Missing Chapters" "Count"
  printf "%${wcol}s-+-%${ccol}s-+------\n" "" "" | tr ' ' '-'

  for w in "${wave_order[@]}"; do
    local chapters="${wave_missing[$w]}"
    local count
    count=$(echo "$chapters" | tr ',' '\n' | wc -l | tr -d ' ')
    local ws=$(( (w - 1) * WAVE_SIZE ))
    local we=$(( ws + WAVE_SIZE ))
    (( we > ${#CHAPTERS[@]} )) && we=${#CHAPTERS[@]}
    local wt=$(( we - ws ))
    local label="$w"
    (( count < wt )) && label="$w (partial)"
    printf "%-${wcol}s | %-${ccol}s | %s\n" "$label" "$chapters" "$count"
  done

  echo ""
  echo "To run:"
  echo "  weirwood ${book} 2 3    # 2 terminals, 3 waves each"
  echo ""
}

# ── CMD: run ──────────────────────────────────────────────────────────────────

cmd_run() {
  local book="" wave="" model="$DEFAULT_MODEL" force=false

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --wave|-w)   wave="$2";  shift 2 ;;
      --model|-m)  model="$2"; shift 2 ;;
      --force)     force=true; shift   ;;
      --help|-h)   echo "Usage: extract.sh run <book> --wave <N> [--model <model>] [--force]"; return 0 ;;
      -*)          echo "Unknown option: $1" >&2; return 1 ;;
      *)           book="$1";  shift   ;;
    esac
  done

  if [[ -z "$book" || -z "$wave" ]]; then
    echo "ERROR: book and --wave are required" >&2
    echo "Usage: extract.sh run <book> --wave <N>" >&2
    return 1
  fi

  local chapter_dir="sources/chapters/${book}"
  local extract_dir="extractions/mechanical/${book}"
  mkdir -p "$extract_dir"

  discover_chapters "$book"

  mkdir -p "$STATS_DIR"
  local STATS_FILE
  STATS_FILE=$(stats_file_for "$book")

  # Migrate old-schema CSV to new schema (idempotent)
  python3 scripts/migrate-stats-csv.py "$STATS_FILE" 2>/dev/null || true

  # Sweep stale started/working rows from crashed terminals
  python3 scripts/extract-status-sweep.py "$STATS_FILE" \
    --heartbeat-max-age 90 --row-max-age 1800 2>/dev/null || true

  # Create CSV with new header if it doesn't exist yet
  if [[ ! -f "$STATS_FILE" ]]; then
    echo "chapter,book,wave,status,start_time,end_time,duration_s,input_tokens,cache_creation_tokens,cache_read_tokens,output_tokens,total_tokens,cost_usd,last_heartbeat,terminal_id,retry_at" > "$STATS_FILE"
  fi

  # Slice chapters for this wave
  local start=$(( (wave - 1) * WAVE_SIZE ))
  local end=$(( start + WAVE_SIZE ))
  (( end > ${#CHAPTERS[@]} )) && end=${#CHAPTERS[@]}

  if (( start >= ${#CHAPTERS[@]} )); then
    echo "Wave $wave is out of range (max $TOTAL_WAVES for $book with ${#CHAPTERS[@]} chapters)"
    return 1
  fi

  local -a wave_chapters=("${CHAPTERS[@]:$start:$((end - start))}")

  echo "═════════════════════════════════════════════════════════════════"
  echo "${book^^} Wave ${wave}/${TOTAL_WAVES} — chapters $((start+1))–${end} of ${#CHAPTERS[@]}"
  echo "Model: $model"
  echo "═════════════════════════════════════════════════════════════════"
  echo ""

  local wave_start successes=0 failures=0 wave_input=0 wave_output=0
  local ch_idx=0
  local -a failed_list
  wave_start=$(date +%s)

  # Heartbeat PID (set/cleared per chapter; accessible from _cleanup via dynamic scope)
  local _HEARTBEAT_PID=""

  # Cleanup trap: kill heartbeat and release any held lock on exit/interrupt
  _cleanup() {
    [[ -n "${_HEARTBEAT_PID:-}" ]] && kill "$_HEARTBEAT_PID" 2>/dev/null || true
    _HEARTBEAT_PID=""
    release_stats_lock 2>/dev/null || true
  }
  trap _cleanup INT TERM EXIT

  for ch in "${wave_chapters[@]}"; do
    local src="${chapter_dir}/${ch}.md"
    local out="${extract_dir}/${ch}.extraction.md"

    if [[ ! -f "$src" ]]; then
      echo "⏭️  SKIP: $src not found"
      failures=$((failures + 1))
      failed_list+=("$ch (source missing)")
      echo "$ch,$book,$wave,skipped-no-source,,,,,,,,,,,," >> "$STATS_FILE"
      continue
    fi

    # ── Atomic claim (Bug B fix) ──────────────────────────────────────────────
    # --force bypasses the done-check but still respects active claims.
    local claim_result
    if [[ "$force" == true ]]; then
      # For --force: treat skip-already-done as claimable; still block on active claims
      claim_result=$(claim_chapter "$ch" "$wave")
      [[ "$claim_result" == "skip-already-done" ]] && claim_result="claim"
    else
      claim_result=$(claim_chapter "$ch" "$wave")
    fi

    case "$claim_result" in
      skip-already-done)
        local lc; lc=$(wc -l < "$out" 2>/dev/null | tr -d ' ') || lc="?"
        echo "⏭️  SKIP: $ch already done (${lc} lines)"
        successes=$((successes + 1))
        continue ;;
      skip-claimed:*)
        local claimant="${claim_result#skip-claimed:}"
        echo "⏭️  SKIP: $ch claimed by ${claimant}"
        continue ;;
      claim-after-stale)
        echo "🔄 Re-claiming: $ch (stale claim cleared)" ;;
      *)
        ;; # claim — proceed normally
    esac

    # Informational: warn if the output file already exists but is incomplete
    if [[ -f "$out" ]]; then
      local reason="" lc
      lc=$(wc -l < "$out" | tr -d ' ')
      (( lc < 100 )) && reason="only ${lc} lines"
      local missing_sections=""
      for section in "## Characters" "## Events" "## Locations" "## Relationships"; do
        grep -q "$section" "$out" || missing_sections+="${section#### }, "
      done
      [[ -n "$missing_sections" ]] && reason="${reason:+$reason, }missing: ${missing_sections%, }"
      [[ -n "$reason" ]] && echo "🔄 RE-EXTRACTING: $ch (incomplete: $reason)"
    fi

    ch_idx=$(( ch_idx + 1 ))

    local logfile="/tmp/extraction-${ch}.log"
    local jsonfile="/tmp/extraction-${ch}.json"
    local ch_start ch_start_fmt
    ch_start=$(date +%s)
    ch_start_fmt=$(date '+%Y-%m-%d %H:%M:%S')

    echo "─────────────────────────────────────────────────────────────────"
    echo "Chapter ${ch_idx} of ${#wave_chapters[@]}: ${ch}"
    echo "─────────────────────────────────────────────────────────────────"
    echo ""
    echo "[1/3] Preparing"
    echo "  Source:   ${src}"
    echo "  Output:   ${out}"
    echo "  Model:    ${model}"
    echo "  Started:  ${ch_start_fmt}"
    echo ""
    echo "[2/3] Extracting (claude -p running)"

    local prompt="You are a mechanical extraction agent for the Weirwood Network project.

First, read reference/architecture.md for entity types, edge types, confidence tiers, and file naming conventions.
Then read .claude/agents/mechanical-extractor.md for your full extraction schema and rules.
Then read the chapter file: ${src}

Produce the extraction and write it to: ${out}

Follow the schema exactly. Overwrite any existing file. Do not reference other chapters — treat this chapter in complete isolation."

    # Heartbeat: append a 'working' row every 30s so the sweep can detect live terminals
    local _ch_hb="$ch" _wave_hb="$wave"
    (
      while sleep 30; do
        local hb_now; hb_now=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
        echo "${_ch_hb},${book},${_wave_hb},working,,,,,,,,,,${hb_now},${TERMINAL_ID}," >> "$STATS_FILE"
      done
    ) &
    _HEARTBEAT_PID=$!

    local status claude_exit
    claude -p --dangerously-skip-permissions --model "$model" --verbose \
      --output-format stream-json "$prompt" 2>&1 \
      | tee "$jsonfile" \
      | python3 scripts/stream-claude-output.py
    claude_exit=${PIPESTATUS[0]}
    if [[ $claude_exit -eq 0 ]]; then
      status="ok"
    else
      status="fail"
    fi

    kill "$_HEARTBEAT_PID" 2>/dev/null || true
    _HEARTBEAT_PID=""

    local ch_end ch_end_fmt elapsed
    ch_end=$(date +%s)
    ch_end_fmt=$(date '+%Y-%m-%d %H:%M:%S')
    elapsed=$(( ch_end - ch_start ))

    # Extract token usage from the stream-json result event
    local INPUT_TOKENS=0 CACHE_CREATION=0 CACHE_READ=0 OUTPUT_TOKENS=0 COST_USD=0
    eval $(python3 -c "
import json
found = False
for line in open('$jsonfile'):
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
    print('INPUT_TOKENS=0'); print('CACHE_CREATION=0'); print('CACHE_READ=0')
    print('OUTPUT_TOKENS=0'); print('COST_USD=0')
" 2>/dev/null)
    local total_tokens=$(( INPUT_TOKENS + CACHE_CREATION + CACHE_READ + OUTPUT_TOKENS ))

    # Extract readable text for the log file
    python3 -c "
import json
for line in open('$jsonfile'):
    line = line.strip()
    if not line: continue
    try:
        obj = json.loads(line)
        if obj.get('type') == 'assistant' and 'message' in obj:
            for block in obj['message'].get('content', []):
                if block.get('type') == 'text': print(block['text'])
    except: pass
" > "$logfile" 2>/dev/null || true

    # Check for rate limit rejection
    local rate_limited=false
    if grep -q '"status":"rejected"' "$jsonfile" 2>/dev/null && \
       grep -q '"rateLimitType"' "$jsonfile" 2>/dev/null; then
      rate_limited=true
    fi

    local final_status retry_at=""
    if [[ "$status" == "ok" ]]; then
      final_status="done"
      local n_lines=0
      [[ -f "$out" ]] && n_lines=$(wc -l < "$out" | tr -d ' ')
      echo ""
      echo "[3/3] Complete"
      echo "  Duration: ${elapsed}s"
      echo "  Tokens:   in:${INPUT_TOKENS}  cache_create:${CACHE_CREATION}  cache_read:${CACHE_READ}  out:${OUTPUT_TOKENS}"
      echo "  Output:   ${n_lines} lines"
      echo ""
      successes=$((successes + 1))
      wave_input=$(( wave_input + INPUT_TOKENS + CACHE_CREATION + CACHE_READ ))
      wave_output=$(( wave_output + OUTPUT_TOKENS ))
      echo "$ch,$book,$wave,${final_status},${ch_start_fmt},${ch_end_fmt},${elapsed},${INPUT_TOKENS},${CACHE_CREATION},${CACHE_READ},${OUTPUT_TOKENS},${total_tokens},${COST_USD},,${TERMINAL_ID}," >> "$STATS_FILE"
    else
      echo "  ❌ $ch (${elapsed}s)"
      failures=$((failures + 1))
      failed_list+=("$ch")

      if [[ "$rate_limited" == true ]]; then
        final_status="failed-rate"
        local reset_info="" resets_at_ts=""
        eval $(python3 -c "
import json
for line in open('$jsonfile'):
    line = line.strip()
    if not line: continue
    try:
        obj = json.loads(line)
        if obj.get('type') == 'rate_limit_event':
            info = obj.get('rate_limit_info', {})
            if info.get('status') == 'rejected':
                ts = info.get('resetsAt', 0)
                rtype = info.get('rateLimitType', 'unknown')
                if ts > 0:
                    import datetime
                    reset_dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
                    print(f'reset_info=\"{rtype} limit — resets at {reset_dt.strftime(\"%H:%M UTC\")}\"')
                    print(f'resets_at_ts={ts}')
                else:
                    print(f'reset_info=\"{rtype} limit hit\"')
                break
    except: pass
" 2>/dev/null || true)
        [[ -z "${reset_info:-}" ]] && reset_info="rate limit hit"
        if [[ -n "${resets_at_ts:-}" ]]; then
          retry_at=$(python3 -c "import datetime; print(datetime.datetime.fromtimestamp(${resets_at_ts}, tz=datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))" 2>/dev/null || echo "")
        fi
        echo ""
        echo "  🚫 RATE LIMIT: ${reset_info}"
        echo "     Halting wave — remaining chapters would all fail immediately."
        echo ""
        echo "$ch,$book,$wave,${final_status},${ch_start_fmt},${ch_end_fmt},${elapsed},${INPUT_TOKENS},${CACHE_CREATION},${CACHE_READ},${OUTPUT_TOKENS},${total_tokens},${COST_USD},,${TERMINAL_ID},${retry_at}" >> "$STATS_FILE"
        local hit_limit=false
        for remaining_ch in "${wave_chapters[@]}"; do
          if [[ "$hit_limit" == true ]]; then
            echo "$remaining_ch,$book,$wave,failed-rate,,,,,,,,,,,," >> "$STATS_FILE"
          fi
          [[ "$remaining_ch" == "$ch" ]] && hit_limit=true
        done
        break
      else
        final_status="failed-error"
        echo "$ch,$book,$wave,${final_status},${ch_start_fmt},${ch_end_fmt},${elapsed},${INPUT_TOKENS},${CACHE_CREATION},${CACHE_READ},${OUTPUT_TOKENS},${total_tokens},${COST_USD},,${TERMINAL_ID}," >> "$STATS_FILE"
      fi
    fi
  done

  # Disable the cleanup trap before normal exit
  trap - INT TERM EXIT

  local wave_elapsed wave_total_tokens
  wave_elapsed=$(( $(date +%s) - wave_start ))
  wave_total_tokens=$(( wave_input + wave_output ))

  echo ""
  echo "═════════════════════════════════════════════════════════════════"
  if (( failures == 0 )); then
    echo "✅ ${book^^} Wave ${wave}/${TOTAL_WAVES} complete"
  else
    echo "⚠️  ${book^^} Wave ${wave}/${TOTAL_WAVES} complete (with failures)"
  fi
  echo "═════════════════════════════════════════════════════════════════"
  echo "  Succeeded:  ${successes} / ${#wave_chapters[@]}"
  echo "  Failed:     ${failures}"
  echo "  Wall time:  $(format_duration "$wave_elapsed")"
  printf "  Tokens:     %s in  /  %s out\n" \
    "$(printf "%'d" "$wave_input")" "$(printf "%'d" "$wave_output")"
  if (( failures > 0 )); then
    echo "  Failed:     ${failed_list[*]}"
  fi
  echo ""

  local timestamp chapter_list
  timestamp=$(date '+%Y-%m-%d %H:%M')
  chapter_list=$(IFS=', '; echo "${wave_chapters[*]}")
  if (( failures == 0 )); then
    echo "- **${book^^} Wave $wave** ($timestamp) — $chapter_list (${#wave_chapters[@]}/${#wave_chapters[@]} ok) [$(format_duration "$wave_elapsed"), ${wave_total_tokens} tokens]" >> "$PROGRESS_FILE"
  else
    local fail_str
    fail_str=$(IFS=', '; echo "${failed_list[*]}")
    echo "- **${book^^} Wave $wave** ($timestamp) — $chapter_list ($successes/${#wave_chapters[@]} ok, failed: $fail_str) [$(format_duration "$wave_elapsed"), ${wave_total_tokens} tokens]" >> "$PROGRESS_FILE"
  fi

  update_worklog "$book"
}

# ── CMD: launch ───────────────────────────────────────────────────────────────

cmd_launch() {
  local book="" terminals="" waves_per="" model="$DEFAULT_MODEL"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --terminals|-t) terminals="$2"; shift 2 ;;
      --waves|-w)     waves_per="$2"; shift 2 ;;
      --model|-m)     model="$2";     shift 2 ;;
      --help|-h)      echo "Usage: extract.sh launch <book> -t <terminals> -w <waves_per_terminal> [-m model]"; return 0 ;;
      --chain|--delay) echo "ERROR: --chain and --delay were removed. Launch separate runs instead." >&2; return 1 ;;
      -*)             echo "Unknown option: $1" >&2; return 1 ;;
      *)              book="$1";      shift   ;;
    esac
  done

  if [[ -z "$book" || -z "$terminals" || -z "$waves_per" ]]; then
    echo "ERROR: book, --terminals, and --waves are required" >&2
    echo "Usage: extract.sh launch <book> -t <terminals> -w <waves_per_terminal>" >&2
    return 1
  fi

  discover_chapters "$book"
  find_incomplete_waves "$book"

  local total_needed=$(( terminals * waves_per ))
  local available=${#INCOMPLETE_WAVES[@]}

  if (( available == 0 )); then
    echo "${book^^}: All waves complete! Nothing to launch."
    return 0
  fi

  if (( total_needed > available )); then
    echo "Note: only $available incomplete waves remain (requested $total_needed)"
    if (( available <= terminals )); then
      terminals=$available
      waves_per=1
    else
      waves_per=$(( (available + terminals - 1) / terminals ))
    fi
    total_needed=$(( terminals * waves_per ))
  fi

  # Clear stale stop file
  rm -f /tmp/extraction-stop

  echo "${book^^}: ${#CHAPTERS[@]} chapters, ${TOTAL_WAVES} waves total, $available incomplete"
  echo "Launching $terminals terminals, $waves_per waves each"
  echo ""

  local project_dir="$REPO_ROOT"
  local idx=0

  for (( t=0; t<terminals; t++ )); do
    local -a term_waves=()
    for (( j=0; j<waves_per && idx<available; j++, idx++ )); do
      term_waves+=("${INCOMPLETE_WAVES[$idx]}")
    done

    if (( ${#term_waves[@]} == 0 )); then
      continue
    fi

    local wave_display
    wave_display=$(IFS=', '; echo "${term_waves[*]}")
    echo "Terminal $((t+1)): waves [${wave_display}]"

    local cmd=""
    if (( ${#term_waves[@]} == 1 )); then
      cmd="./scripts/extract.sh run ${book} --wave ${term_waves[0]} --model ${model}"
    else
      cmd="for w in ${term_waves[*]}; do "
      cmd+="if [[ -f /tmp/extraction-stop ]]; then echo 'Stop file detected — halting before wave '\$w; break; fi; "
      cmd+="./scripts/extract.sh run ${book} --wave \$w --model ${model}; "
      cmd+="done"
    fi

    osascript <<EOF
tell application "iTerm2"
  activate
  tell current window
    create tab with default profile
    tell current session of current tab
      write text "cd ${project_dir} && ${cmd}"
    end tell
  end tell
end tell
EOF
  done

  echo ""
  echo "Launched $terminals iTerm2 tabs."
  if (( waves_per > 1 )); then
    echo "To stop after the current wave: weirwood stop"
  fi
}

# ── CMD: check ─────────────────────────────────────────────────────────────────

cmd_check() {
  local all_ok=true

  echo ""
  echo "🔍 Checking source files and prerequisites..."
  echo ""

  local -A RAW_FILES=(
    [agot]="GoT.txt"
    [acok]="ACOK.txt"
    [asos]="ASOS.txt"
    [affc]="AFFC.txt"
    [adwd]="ADWD.txt"
  )

  local -A EXPECTED_CHAPTERS=(
    [agot]=73
    [acok]=70
    [asos]=82
    [affc]=46
    [adwd]=73
  )

  echo "Raw source files (sources/raw/):"
  for book in agot acok asos affc adwd; do
    local raw="sources/raw/${RAW_FILES[$book]}"
    if [[ -f "$raw" ]]; then
      local size
      size=$(du -h "$raw" | cut -f1)
      echo "  ✅ ${RAW_FILES[$book]} ($size)"
    else
      echo "  ❌ ${RAW_FILES[$book]} — MISSING"
      all_ok=false
    fi
  done

  echo ""
  echo "Split chapter files (sources/chapters/):"
  for book in agot acok asos affc adwd; do
    local chapter_dir="sources/chapters/${book}"
    local expected=${EXPECTED_CHAPTERS[$book]}
    if [[ ! -d "$chapter_dir" ]]; then
      echo "  ❌ ${book^^}: directory missing"
      all_ok=false
    else
      local count
      count=$(ls "$chapter_dir"/*.md 2>/dev/null | wc -l | tr -d ' ')
      if (( count == expected )); then
        echo "  ✅ ${book^^}: ${count}/${expected} chapters"
      elif (( count > 0 )); then
        echo "  ⚠️  ${book^^}: ${count}/${expected} chapters"
        all_ok=false
      else
        echo "  ❌ ${book^^}: no chapter files"
        all_ok=false
      fi
    fi
  done

  echo ""
  echo "Extraction outputs (extractions/mechanical/):"
  for book in agot acok asos affc adwd; do
    local extract_dir="extractions/mechanical/${book}"
    local chapter_dir="sources/chapters/${book}"
    if [[ ! -d "$chapter_dir" ]]; then
      echo "  ⏭️  ${book^^}: no chapters to extract"
      continue
    fi
    local total=0 done=0
    for f in "$chapter_dir"/*.md; do
      total=$(( total + 1 ))
      local stem
      stem=$(basename "$f" .md)
      if is_complete "${extract_dir}/${stem}.extraction.md"; then
        done=$(( done + 1 ))
      fi
    done
    if (( done == total )); then
      echo "  ✅ ${book^^}: ${done}/${total} complete"
    elif (( done > 0 )); then
      echo "  🔶 ${book^^}: ${done}/${total} ($((total - done)) remaining)"
    else
      echo "  ⬜ ${book^^}: 0/${total} (not started)"
    fi
  done

  echo ""
  echo "Prerequisites:"
  if command -v claude &>/dev/null; then
    echo "  ✅ claude CLI found"
  else
    echo "  ❌ claude CLI not found — install from https://claude.ai/code"
    all_ok=false
  fi

  if [[ -d /Applications/iTerm.app ]] || command -v osascript &>/dev/null; then
    echo "  ✅ iTerm2 / osascript available"
  else
    echo "  ⚠️  iTerm2 not found — launch command won't work"
  fi

  if command -v python3 &>/dev/null; then
    echo "  ✅ python3 found"
  else
    echo "  ❌ python3 not found — needed for chapter splitting and stats"
    all_ok=false
  fi

  echo ""
  if [[ "$all_ok" == true ]]; then
    echo "✅ All checks passed. Ready to extract."
  else
    echo "⚠️  Some issues found. See above."
    echo ""
    echo "If you have raw .txt source files but chapters aren't split yet:"
    echo "  python3 scripts/chapter-splitter.py sources/raw/GoT.txt agot"
    echo "  python3 scripts/chapter-splitter.py sources/raw/ACOK.txt acok"
    echo "  python3 scripts/chapter-splitter.py sources/raw/ASOS.txt asos"
    echo "  python3 scripts/chapter-splitter.py sources/raw/AFFC.txt affc"
    echo "  python3 scripts/chapter-splitter.py sources/raw/ADWD.txt adwd"
  fi
  echo ""
}

# ── Dispatch ──────────────────────────────────────────────────────────────────

case "${1:-}" in
  run)    shift; cmd_run "$@" ;;
  status) shift; cmd_status "$@" ;;
  launch) shift; cmd_launch "$@" ;;
  check)  shift; cmd_check "$@" ;;
  --help|-h) usage ;;
  *)      usage ;;
esac
