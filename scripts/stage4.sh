#!/usr/bin/env bash
# stage4.sh — Stage 4 prose-edge classification worker controller
#
# Subcommands:
#   status              Show mission progress, token stats, stuck batches
#   run                 Run one worker loop (called in each iTerm tab)
#   launch -t N         Open N iTerm2 tabs each running 'stage4.sh run'
#   unstick <batch_id>  Release an orphaned batch lock + revert to queued
#
# The shell function `weirwood stage4` in weirwood.zsh wraps this.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${WEIRWOOD_PROJECT_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"
cd "$REPO_ROOT"

MODEL="${STAGE4_MODEL:-claude-sonnet-4-6}"
STOP_FILE="/tmp/stage4-stop"
WORKER_PROMPT="$REPO_ROOT/.claude/commands/worker-stage4.md"
# Inter-batch sleep in seconds (throttle to share Max 5h cap with other Claude work).
# Default 1200 = 20 min ("parallel-safe": Matt working alongside the bulk run).
# Burst mode (Matt AFK overnight, weekly headroom available): STAGE4_SLEEP_BETWEEN=600 (10min) or lower.
# Conservative (heavy parallel use): STAGE4_SLEEP_BETWEEN=3600+ (60min+).
SLEEP_BETWEEN="${STAGE4_SLEEP_BETWEEN:-1200}"

# Global — set in cmd_run, used by _log
LOG_FILE=""

# ── Helpers ────────────────────────────────────────────────────────────────────

format_duration() {
  local secs=$1
  local h=$(( secs / 3600 )) m=$(( (secs % 3600) / 60 )) s=$(( secs % 60 ))
  if (( h > 0 )); then printf "%dh %dm %ds" "$h" "$m" "$s"
  elif (( m > 0 )); then printf "%dm %ds" "$m" "$s"
  else printf "%ds" "$s"; fi
}

now_iso() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }

_log() {
  local msg="$1"
  echo "$msg"
  if [[ -n "$LOG_FILE" ]]; then
    echo "$(now_iso)  $msg" >> "$LOG_FILE"
  fi
}

# ── Mission discovery ──────────────────────────────────────────────────────────

discover_mission_dir() {
  # Env override
  if [[ -n "${STAGE4_MISSION_DIR:-}" ]]; then
    echo "$STAGE4_MISSION_DIR"
    return 0
  fi
  # Find most recent dir under working/missions/ that contains batch-manifest.jsonl.
  # Dirs are date-prefixed; lexicographic sort gives most-recent-last, so use tail -1.
  local missions_root="$REPO_ROOT/working/missions"
  if [[ ! -d "$missions_root" ]]; then
    return 1
  fi
  local found
  found=$(find "$missions_root" -mindepth 1 -maxdepth 1 -type d \
    | sort \
    | while read -r d; do
        [[ -f "$d/batch-manifest.jsonl" ]] && echo "$d"
      done \
    | tail -1)
  if [[ -z "$found" ]]; then
    return 1
  fi
  echo "$found"
}

get_mission_dir() {
  local dir
  if ! dir=$(discover_mission_dir); then
    echo "ERROR: No mission found. Run mission-stage4-init.py to create one." >&2
    echo "  Or set STAGE4_MISSION_DIR to the mission directory." >&2
    exit 1
  fi
  echo "$dir"
}

# ── CMD: status ───────────────────────────────────────────────────────────────

cmd_status() {
  local MISSION_DIR
  MISSION_DIR=$(get_mission_dir)
  local MISSION_NAME
  MISSION_NAME=$(basename "$MISSION_DIR")
  local MANIFEST="$MISSION_DIR/batch-manifest.jsonl"

  python3 - <<PYEOF
import json, os, sys
from pathlib import Path
from datetime import datetime, timezone

mission_dir = Path("$MISSION_DIR")
mission_name = "$MISSION_NAME"
manifest_path = mission_dir / "batch-manifest.jsonl"
results_dir = mission_dir / "results"
locks_dir = mission_dir / "locks"
timing_path = mission_dir / "timing.jsonl"
run_logs_dir = mission_dir / "run-logs"
questions_path = Path("$REPO_ROOT/working/wiki/pass2-buckets/questions-for-matt.jsonl")

# ── Read manifest ─────────────────────────────────────────────────────────────
batches = []
with open(manifest_path) as f:
    for line in f:
        line = line.strip()
        if line:
            batches.append(json.loads(line))

total = len(batches)
counts = {"done": 0, "in-progress": 0, "queued": 0, "other": 0}
for b in batches:
    s = b.get("status", "queued")
    if s in counts:
        counts[s] += 1
    else:
        counts["other"] += 1

pct = int(counts["done"] / total * 100) if total > 0 else 0

print()
print(f"=== Stage 4 Status: {mission_name} ===")
print()
print(f"Manifest: {manifest_path}")
print()
print(f"Batches: {counts['done']} done / {counts['in-progress']} in-progress / {counts['queued']} queued  ({total} total, {pct}% complete)")
print()

# ── Decision / edge totals from results/ ─────────────────────────────────────
total_edges = 0
total_vocab_gaps = 0
total_escalations = 0
total_errors = 0
results_found = 0
if results_dir.exists():
    for rf in sorted(results_dir.glob("*.json")):
        try:
            d = json.loads(rf.read_text())
            if isinstance(d, dict):
                total_edges += d.get("total_edges_emitted", 0)
                total_vocab_gaps += d.get("vocab_gap_questions_filed", 0)
                total_escalations += d.get("escalations", 0)
                total_errors += d.get("errors", 0)
                results_found += 1
        except Exception:
            pass

if results_found > 0:
    print(f"Results ({results_found} batches complete):")
    print(f"  Edges emitted:    {total_edges:,}")
    print(f"  Vocab-gap Qs:     {total_vocab_gaps:,}")
    print(f"  Escalations:      {total_escalations:,}")
    print(f"  Errors:           {total_errors:,}")
    print()

# ── Token / cost totals from timing.jsonl ────────────────────────────────────
if timing_path.exists():
    timing_rows = []
    with open(timing_path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    timing_rows.append(json.loads(line))
                except Exception:
                    pass
    if timing_rows:
        tot_input = sum(r.get("input_tokens", 0) for r in timing_rows)
        tot_cache_read = sum(r.get("cache_read", 0) for r in timing_rows)
        tot_output = sum(r.get("output_tokens", 0) for r in timing_rows)
        tot_cost = sum(r.get("cost_usd", 0.0) for r in timing_rows)
        tot_elapsed = sum(r.get("elapsed_s", 0) for r in timing_rows)
        avg_elapsed = tot_elapsed / len(timing_rows) if timing_rows else 0
        print(f"Tokens (across {len(timing_rows)} timed batches):")
        print(f"  Input:         {tot_input:>12,}")
        print(f"  Cache read:    {tot_cache_read:>12,}")
        print(f"  Output:        {tot_output:>12,}")
        print(f"  Total cost:    \${tot_cost:>10.4f}")
        print(f"  Avg elapsed:   {avg_elapsed:.0f}s / batch")
        print()

# ── Active workers ────────────────────────────────────────────────────────────
now = datetime.now(tz=timezone.utc).timestamp()
active_workers = 0
if run_logs_dir.exists():
    for lf in run_logs_dir.glob("*.log"):
        try:
            mtime = lf.stat().st_mtime
            if now - mtime < 300:  # modified in last 5 minutes
                active_workers += 1
        except Exception:
            pass
print(f"Active workers (log modified <5 min): {active_workers}")
print()

# ── Stuck batches ─────────────────────────────────────────────────────────────
stuck = []
for b in batches:
    if b.get("status") == "in-progress":
        bid = b["batch_id"]
        lock_file = locks_dir / f"{bid}.lock" if locks_dir.exists() else None
        if lock_file is None or not lock_file.exists():
            stuck.append(bid)

if stuck:
    print(f"Stuck batches ({len(stuck)} in-progress with no lock file):")
    for bid in stuck:
        print(f"  {bid}  →  weirwood stage4 unstick {bid}")
    print()
else:
    print("No stuck batches.")
    print()

# ── Rate-limit events ─────────────────────────────────────────────────────────
rl_path = mission_dir / "rate-limit-events.jsonl"
if rl_path.exists():
    rl_rows = []
    with open(rl_path) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try: rl_rows.append(json.loads(line))
            except Exception: pass
    if rl_rows:
        print(f"Rate-limit events: {len(rl_rows)} total")
        for r in rl_rows[-5:]:
            ts = r.get("resets_at_ts", "")
            reset_str = ""
            if ts:
                try:
                    reset_dt = datetime.fromtimestamp(int(ts), tz=timezone.utc)
                    reset_str = f" → resets {reset_dt.strftime('%Y-%m-%d %H:%M UTC')}"
                except Exception:
                    pass
            print(f"  {r.get('detected_at','')}  worker={r.get('worker_id','?')}  type={r.get('rate_limit_type','?')}{reset_str}")
        print()

next_eligible = mission_dir / "next-eligible.txt"
if next_eligible.exists():
    try:
        ts = int(next_eligible.read_text().strip())
        reset_dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        now = datetime.now(tz=timezone.utc)
        delta = (reset_dt - now).total_seconds()
        if delta > 0:
            print(f"Next-eligible (from last rate-limit): {reset_dt.strftime('%Y-%m-%d %H:%M UTC')} (in {int(delta//60)} min)")
        else:
            print(f"Next-eligible: {reset_dt.strftime('%Y-%m-%d %H:%M UTC')} (already passed — safe to relaunch)")
        print()
    except Exception:
        pass

# ── Vocab-gap questions ───────────────────────────────────────────────────────
if questions_path.exists():
    try:
        q_count = sum(1 for ln in questions_path.open() if ln.strip())
        print(f"Vocab-gap questions file: {q_count} lines  ({questions_path})")
    except Exception:
        pass

print()
PYEOF
}

# ── CMD: run ──────────────────────────────────────────────────────────────────

cmd_run() {
  local MISSION_DIR
  MISSION_DIR=$(get_mission_dir)
  local MISSION_NAME
  MISSION_NAME=$(basename "$MISSION_DIR")

  local worker_id
  worker_id="worker-$(date '+%Y%m%d-%H%M%S')-$$"

  local run_logs_dir="$MISSION_DIR/run-logs"
  mkdir -p "$run_logs_dir"
  LOG_FILE="$run_logs_dir/${worker_id}.log"

  _log "Stage 4 worker starting: $worker_id"
  _log "Mission: $MISSION_NAME"
  _log "Model: $MODEL"
  _log "Worker prompt: $WORKER_PROMPT"

  if [[ ! -f "$WORKER_PROMPT" ]]; then
    _log "ERROR: Worker prompt not found: $WORKER_PROMPT"
    exit 1
  fi

  # Worker loop
  while true; do
    # Check stop file
    if [[ -f "$STOP_FILE" ]]; then
      _log "Stop file detected ($STOP_FILE) — exiting cleanly."
      break
    fi

    # Check how many queued batches remain
    local queued_count
    queued_count=$(python3 -c "
import json
count = 0
with open('$MISSION_DIR/batch-manifest.jsonl') as f:
    for line in f:
        line = line.strip()
        if line:
            d = json.loads(line)
            if d.get('status') == 'queued':
                count += 1
print(count)
" 2>/dev/null || echo "0")

    if [[ "$queued_count" -eq 0 ]]; then
      _log "Mission complete or no batches available (0 queued). Exiting."
      break
    fi

    _log "Queued batches remaining: $queued_count — starting Claude run"

    local tmp_json
    tmp_json=$(mktemp /tmp/stage4-stream-XXXXXX)

    local batch_start
    batch_start=$(date +%s)
    local started_at
    started_at=$(now_iso)

    local claude_exit=0
    # Disable -e around the pipeline so non-zero exits don't kill the loop
    # before we get to log + cleanup. pipefail + set -e was silently terminating
    # workers when claude hit the wall, leaving orphan locks.
    set +e
    claude -p --dangerously-skip-permissions \
      --model "$MODEL" \
      --verbose \
      --output-format stream-json \
      "$(cat "$WORKER_PROMPT")" 2>&1 \
      | tee "$tmp_json" \
      | python3 scripts/stream-claude-output.py
    claude_exit=${PIPESTATUS[0]}
    set -e

    local batch_end elapsed
    batch_end=$(date +%s)
    elapsed=$(( batch_end - batch_start ))

    # Extract token stats from the stream-json result event
    local INPUT_TOKENS=0 CACHE_CREATION=0 CACHE_READ=0 OUTPUT_TOKENS=0 COST_USD=0
    eval $(python3 -c "
import json
found = False
try:
    for line in open('$tmp_json'):
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
except: pass
if not found:
    print('INPUT_TOKENS=0'); print('CACHE_CREATION=0'); print('CACHE_READ=0')
    print('OUTPUT_TOKENS=0'); print('COST_USD=0')
" 2>/dev/null)

    # Determine which batch_id was just processed: read the last release event from state.jsonl
    local batch_id="unknown"
    if [[ -f "$MISSION_DIR/state.jsonl" ]]; then
      batch_id=$(python3 -c "
import json
last_bid = 'unknown'
try:
    with open('$MISSION_DIR/state.jsonl') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try:
                d = json.loads(line)
                if d.get('event') == 'release':
                    last_bid = d.get('batch_id', 'unknown')
            except: pass
except: pass
print(last_bid)
" 2>/dev/null || echo "unknown")
    fi

    # ── Detect rate limit in stream-json output (ported from extract.sh) ──
    local rate_limited=false reset_info="" resets_at_ts="" rate_limit_type=""
    if grep -q '"status":"rejected"' "$tmp_json" 2>/dev/null && \
       grep -q '"rateLimitType"' "$tmp_json" 2>/dev/null; then
      rate_limited=true
      eval $(python3 -c "
import json
for line in open('$tmp_json'):
    line = line.strip()
    if not line: continue
    try:
        obj = json.loads(line)
        if obj.get('type') == 'rate_limit_event':
            info = obj.get('rate_limit_info', {})
            if info.get('status') == 'rejected':
                ts = info.get('resetsAt', 0)
                rtype = info.get('rateLimitType', 'unknown')
                print(f'rate_limit_type=\"{rtype}\"')
                if ts > 0:
                    import datetime
                    reset_dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
                    print(f'reset_info=\"{rtype} limit — resets at {reset_dt.strftime(\"%Y-%m-%d %H:%M UTC\")}\"')
                    print(f'resets_at_ts={ts}')
                else:
                    print(f'reset_info=\"{rtype} limit hit\"')
                break
    except: pass
" 2>/dev/null || true)
    fi

    # Append timing entry (with rate-limit fields)
    python3 -c "
import json
row = {
    'batch_id': '$batch_id',
    'worker_id': '$worker_id',
    'started_at': '$started_at',
    'elapsed_s': $elapsed,
    'input_tokens': $INPUT_TOKENS,
    'cache_creation': $CACHE_CREATION,
    'cache_read': $CACHE_READ,
    'output_tokens': $OUTPUT_TOKENS,
    'cost_usd': $COST_USD,
    'claude_exit': $claude_exit,
    'rate_limited': '$rate_limited' == 'true',
    'rate_limit_type': '${rate_limit_type}',
    'resets_at_ts': '${resets_at_ts}',
}
with open('$MISSION_DIR/timing.jsonl', 'a') as f:
    f.write(json.dumps(row) + '\n')
" 2>/dev/null || true

    # Log summary
    _log "Batch complete: batch_id=$batch_id elapsed=${elapsed}s input=$INPUT_TOKENS cache_read=$CACHE_READ output=$OUTPUT_TOKENS cost=\$$COST_USD exit=$claude_exit"

    rm -f "$tmp_json"

    if [[ "$rate_limited" == "true" ]]; then
      # Persist rate-limit event for post-mortem + scheduling
      python3 -c "
import json
row = {
    'worker_id': '$worker_id',
    'batch_id': '$batch_id',
    'detected_at': '$(now_iso)',
    'rate_limit_type': '${rate_limit_type:-unknown}',
    'resets_at_ts': '${resets_at_ts}',
    'reset_info': '${reset_info}',
    'cumulative_elapsed_s': $elapsed,
    'cumulative_cost_usd': $COST_USD,
}
with open('$MISSION_DIR/rate-limit-events.jsonl', 'a') as f:
    f.write(json.dumps(row) + '\n')
" 2>/dev/null || true
      _log "🚫 RATE LIMIT: ${reset_info:-rate limit hit} — exiting worker cleanly (no retry burn)."
      if [[ -n "${resets_at_ts}" ]]; then
        echo "$resets_at_ts" > "$MISSION_DIR/next-eligible.txt"
        _log "Wrote $MISSION_DIR/next-eligible.txt: $resets_at_ts (epoch seconds, UTC)"
      fi
      break
    fi

    if [[ "$claude_exit" -ne 0 ]]; then
      _log "WARNING: non-zero exit ($claude_exit) — retrying in 30s"
      sleep 30
      continue
    fi

    # Throttle: sleep N min between batches so we don't saturate Max 5h cap.
    # Configure via STAGE4_SLEEP_BETWEEN env var (default 5400 = 90 min).
    _log "Sleeping ${SLEEP_BETWEEN}s (≈$((SLEEP_BETWEEN / 60)) min) before next batch — throttle to share 5h cap"
    sleep "$SLEEP_BETWEEN"
  done

  _log "Worker $worker_id exiting."
}

# ── CMD: launch ───────────────────────────────────────────────────────────────

cmd_launch() {
  local num_tabs=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -t|--tabs) num_tabs="$2"; shift 2 ;;
      --help|-h) echo "Usage: stage4.sh launch -t <N>"; return 0 ;;
      -*)        echo "Unknown option: $1" >&2; return 1 ;;
      *)         echo "Unknown argument: $1" >&2; return 1 ;;
    esac
  done

  if [[ -z "$num_tabs" ]]; then
    echo "ERROR: -t <N> is required" >&2
    echo "Usage: stage4.sh launch -t <N>" >&2
    return 1
  fi

  local MISSION_DIR
  MISSION_DIR=$(get_mission_dir)
  local MISSION_NAME
  MISSION_NAME=$(basename "$MISSION_DIR")

  # Clear stop file
  rm -f "$STOP_FILE"

  echo "Stage 4: launching $num_tabs worker tabs — $MISSION_NAME"

  local project_dir="$REPO_ROOT"
  # Forward STAGE4_SLEEP_BETWEEN into each tab's shell so the parent shell's
  # env value reaches the worker (osascript opens a fresh shell that does not
  # inherit the parent's env). Default falls back to script default (1200 = 20min, parallel-safe).
  local sleep_forward="${STAGE4_SLEEP_BETWEEN:-1200}"

  for (( i=0; i<num_tabs; i++ )); do
    osascript <<EOF
tell application "iTerm2"
  activate
  tell current window
    create tab with default profile
    tell current session of current tab
      write text "cd '${project_dir}' && STAGE4_SLEEP_BETWEEN=${sleep_forward} bash scripts/stage4.sh run"
    end tell
  end tell
end tell
EOF
  done

  echo "$num_tabs workers launched. To stop: weirwood stage4 stop"
}

# ── CMD: unstick ──────────────────────────────────────────────────────────────

cmd_unstick() {
  local batch_id="${1:-}"
  if [[ -z "$batch_id" ]]; then
    echo "ERROR: batch_id is required" >&2
    echo "Usage: stage4.sh unstick <batch_id>" >&2
    return 1
  fi

  local MISSION_DIR
  MISSION_DIR=$(get_mission_dir)
  local MANIFEST="$MISSION_DIR/batch-manifest.jsonl"
  local LOCKS_DIR="$MISSION_DIR/locks"

  # Delete lock file if it exists
  local lock_file="$LOCKS_DIR/${batch_id}.lock"
  if [[ -f "$lock_file" ]]; then
    rm -f "$lock_file"
    echo "Removed lock file: $lock_file"
  else
    echo "No lock file found for $batch_id (already clear)"
  fi

  # Rewrite manifest: change status of matching batch_id to "queued"
  local tmp_manifest
  tmp_manifest=$(mktemp /tmp/stage4-manifest-XXXXXX)

  local changed=false
  local old_status=""
  while IFS= read -r line; do
    if [[ -z "$line" ]]; then
      continue
    fi
    local row_id row_status
    row_id=$(python3 -c "import json,sys; d=json.loads(sys.stdin.read()); print(d.get('batch_id',''))" <<< "$line" 2>/dev/null || echo "")
    if [[ "$row_id" == "$batch_id" ]]; then
      old_status=$(python3 -c "import json,sys; d=json.loads(sys.stdin.read()); print(d.get('status',''))" <<< "$line" 2>/dev/null || echo "")
      line=$(python3 -c "
import json, sys
d = json.loads(sys.stdin.read())
d['status'] = 'queued'
d.pop('completed_at', None)
print(json.dumps(d))
" <<< "$line" 2>/dev/null || echo "$line")
      changed=true
    fi
    echo "$line" >> "$tmp_manifest"
  done < "$MANIFEST"

  if [[ "$changed" == true ]]; then
    mv "$tmp_manifest" "$MANIFEST"
    echo "Batch $batch_id: status '$old_status' → 'queued'"
  else
    rm -f "$tmp_manifest"
    echo "WARNING: batch_id '$batch_id' not found in manifest"
    return 1
  fi
}

# ── Dispatch ──────────────────────────────────────────────────────────────────

cmd="${1:-status}"
case "$cmd" in
  status)  shift; cmd_status "$@" ;;
  run)     shift; cmd_run "$@" ;;
  launch)  shift; cmd_launch "$@" ;;
  unstick) shift; cmd_unstick "$@" ;;
  --help|-h)
    cat <<'EOF'
stage4.sh — Stage 4 prose-edge classification worker controller

Subcommands:
  stage4.sh status              Show mission progress, token stats, stuck batches
  stage4.sh run                 Run one worker loop (called in each iTerm tab)
  stage4.sh launch -t N         Open N iTerm2 tabs each running 'stage4.sh run'
  stage4.sh unstick <batch_id>  Release an orphaned batch lock + revert to queued

Environment:
  WEIRWOOD_PROJECT_DIR   Override repo root (default: parent of this script)
  STAGE4_MODEL           Override model (default: claude-sonnet-4-6)
  STAGE4_MISSION_DIR     Override mission dir (default: most-recent under working/missions/)
  STAGE4_SLEEP_BETWEEN   Seconds to sleep between batches.
                         Default: 1200 (20min, parallel-safe — Matt working alongside).
                         Burst (Matt AFK): 600 (10min) or lower.
                         Conservative (heavy parallel use): 3600+ (60min+).
                         Lower = faster but more likely to saturate 5h Max cap.

Soft stop:
  'weirwood stage4 stop' (or 'touch /tmp/stage4-stop') creates a marker file.
  Workers check it at the top of each loop. The current batch finishes
  normally, then the worker exits instead of claiming another batch.
  The marker is cleared automatically on the next launch.
EOF
    ;;
  *) echo "Unknown subcommand: $cmd" >&2; echo "Run 'stage4.sh --help' for usage." >&2; exit 1 ;;
esac
