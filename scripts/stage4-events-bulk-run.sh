#!/usr/bin/env bash
# stage4-events-bulk-run.sh — Paced multi-day wrapper for the Stage 4
# pass1_events Haiku bulk typing run.  Uses inter-batch --sleep-between pacing
# (gentler for concurrent interactive / Opus use).
#
# See also: scripts/stage4-tail-bulk-forever.sh — burst-model predecessor
# (runs flat-out until a rate-limit wall, then sleeps; no inter-batch pacing).
#
# Loops calling stage4-tail-classifier.py --apply until all 16,502 pass1_events
# candidate rows are processed (or a non-resumable condition is detected).
#
# Exit codes from the classifier:
#   0   — normal completion (all rows done, or no rows left)
#   42  — rate-limit wall (sleep ${STAGE4_WALL_SLEEP:-3600}s then resume)
#   43  — drift halt (DO NOT auto-resume — inspect output)
#   130 — SIGINT/SIGTERM or stop-file detected inside the classifier
#   other non-zero — crash (sleep 300s and retry, up to MAX_CRASHES consecutive)
#
# Stop-file: touch /tmp/stage4-stop to stop cleanly between iterations.
# Ctrl-C (SIGINT) also stops cleanly and does NOT relaunch.
#
# Usage (one-liner for iTerm):
#   STAGE4_SLEEP_BETWEEN=600 STAGE4_VALIDATE_EVERY=25 bash scripts/stage4-events-bulk-run.sh
#
# Env overrides:
#   STAGE4_OUT              — output dir (default: working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk-YYYYMMDD)
#   STAGE4_SLEEP_BETWEEN    — seconds between batches (default: 600)
#   STAGE4_VALIDATE_EVERY   — validation cadence in batches (default: 25)
#   STAGE4_WALL_SLEEP       — seconds to sleep after rate-limit wall exit (default: 3600)
#   STAGE4_MAX_ITER         — max loop iterations before giving up (default: 200)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

STOP_FILE="/tmp/stage4-stop"
SLEEP_BETWEEN="${STAGE4_SLEEP_BETWEEN:-600}"
VALIDATE_EVERY="${STAGE4_VALIDATE_EVERY:-25}"
WALL_SLEEP="${STAGE4_WALL_SLEEP:-3600}"
MAX_CRASHES=5
MAX_ITER="${STAGE4_MAX_ITER:-200}"

# Fresh output dir, datestamped (allow override via env)
OUT="${STAGE4_OUT:-${REPO_ROOT}/working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk-$(date +%Y%m%d)}"
mkdir -p "$OUT"

LOG="$OUT/run.log"

INPUT_DIR="${REPO_ROOT}/working/wiki/pass2-buckets/pass1-derived/_extra-tables"

echo "═══════════════════════════════════════════════════════════════"
echo "  stage4-events-bulk-run — Haiku pass1_events bulk typing"
echo "  Output dir:   $OUT"
echo "  Log:          $LOG"
echo "  Sleep/batch:  ${SLEEP_BETWEEN}s"
echo "  Validate-every: ${VALIDATE_EVERY} batches"
echo "  Wall sleep:   ${WALL_SLEEP}s (after exit 42)"
echo "  Max iter:     ${MAX_ITER}"
echo "  Started:      $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "  Stop file:    $STOP_FILE  (touch to stop cleanly)"
echo "═══════════════════════════════════════════════════════════════"

# Mirror to log
{
echo "═══════════════════════════════════════════════════════════════"
echo "  stage4-events-bulk-run — Haiku pass1_events bulk typing"
echo "  Output dir:   $OUT"
echo "  Sleep/batch:  ${SLEEP_BETWEEN}s"
echo "  Validate-every: ${VALIDATE_EVERY} batches"
echo "  Wall sleep:   ${WALL_SLEEP}s (after exit 42)"
echo "  Max iter:     ${MAX_ITER}"
echo "  Started:      $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "  Stop file:    $STOP_FILE"
echo "═══════════════════════════════════════════════════════════════"
} >> "$LOG" 2>&1

# ---------------------------------------------------------------------------
# sleep_with_stop_check $seconds
# Sleep in 60s chunks; break and return 1 if stop file appears mid-sleep.
# Returns 0 if the full duration elapsed without a stop-file.
# Caller is responsible for acting on the return code.
# ---------------------------------------------------------------------------
sleep_with_stop_check() {
  local remaining=$1
  while (( remaining > 0 )); do
    if [[ -f "$STOP_FILE" ]]; then
      return 1  # stop-file detected; caller breaks the main loop
    fi
    local step=60
    (( step > remaining )) && step=$remaining
    sleep "$step"
    remaining=$((remaining - step))
  done
  return 0
}

# ---------------------------------------------------------------------------
# Count remaining work: candidates minus done-keys (emit + rejected).
# Returns the count on stdout; prints nothing on error (returns 0).
#
# Both sides are counted as unique (source_slug, target_slug, evidence_chapter)
# keys so that duplicate input rows don't show as phantom "remaining" work.
# ---------------------------------------------------------------------------
count_remaining() {
  python3 - <<'PYEOF' "$INPUT_DIR" "$OUT" 2>/dev/null || echo "0"
import json, sys
from pathlib import Path

input_dir = Path(sys.argv[1])
out_dir = Path(sys.argv[2])
books = ["agot", "acok", "asos", "affc", "adwd"]

def key_of(r):
    return (r.get("source_slug",""), r.get("target_slug",""), r.get("evidence_chapter",""))

# Count total candidate KEYS (pass1_events, edge_type=null)
total_keys = set()
for book in books:
    bd = input_dir / book
    if not bd.exists():
        continue
    for f in bd.glob("*.extra-tables.jsonl"):
        for line in f.read_text(errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
                if r.get("edge_type") is None and r.get("candidate_kind") == "pass1_events":
                    total_keys.add(key_of(r))
            except Exception:
                pass

# Count done KEYS from edges + rejected outputs
done_keys = set()
for book in books:
    bd = out_dir / book
    if not bd.exists():
        continue
    for pattern in ["*.edges.jsonl", "*.rejected.jsonl"]:
        for f in bd.glob(pattern):
            for line in f.read_text(errors="replace").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                    done_keys.add(key_of(r))
                except Exception:
                    pass

remaining = max(0, len(total_keys) - len(done_keys))
print(remaining)
PYEOF
}

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
iteration=0
prev_remaining=-1
no_progress_streak=0
crash_streak=0

while true; do
  iteration=$((iteration + 1))

  # ── Max-iteration cap ────────────────────────────────────────────────────
  if (( iteration > MAX_ITER )); then
    echo "[$(date '+%H:%M:%S')] MAX_ITER=${MAX_ITER} reached — stopping." | tee -a "$LOG"
    break
  fi

  # ── Stop-file check ──────────────────────────────────────────────────────
  if [[ -f "$STOP_FILE" ]]; then
    echo "[$(date '+%H:%M:%S')] Stop file detected — exiting cleanly." | tee -a "$LOG"
    break
  fi

  echo "[$(date '+%H:%M:%S')] iter=$iteration — launching classifier..." | tee -a "$LOG"

  # ── Run the classifier ───────────────────────────────────────────────────
  set +e
  python3 scripts/stage4-tail-classifier.py --apply \
    --input-dir "$INPUT_DIR" \
    --candidate-kinds pass1_events \
    --model claude-haiku-4-5-20251001 \
    --output-dir "$OUT" --skip-existing \
    --chunk-size 40 --flush-every 5 \
    --sleep-between "${SLEEP_BETWEEN}" \
    --validate-every "${VALIDATE_EVERY}" \
    --abort-after-consecutive-failures 5 \
    2>&1 | tee -a "$LOG"
  EXIT_CODE=${PIPESTATUS[0]}
  set -e

  echo "[$(date '+%H:%M:%S')] classifier exited with code $EXIT_CODE" | tee -a "$LOG"

  # ── Immediate stop-file check (before interpreting exit code) ────────────
  # Catches a stop-file that was touched while the classifier was running.
  if [[ -f "$STOP_FILE" ]]; then
    echo "[$(date '+%H:%M:%S')] Stop file detected after classifier returned — exiting cleanly." | tee -a "$LOG"
    break
  fi

  # ── Interpret exit code ──────────────────────────────────────────────────

  if [[ "$EXIT_CODE" -eq 43 ]]; then
    # DRIFT HALT — do NOT resume
    cat <<EOF | tee -a "$LOG"

████████████████████████████████████████████████████████████████
  DRIFT HALT (exit 43) — classifier detected output drift.
  Do NOT resume without inspecting $OUT/
  Check: run-summary.json, *.classify_failed.jsonl, run.log
  To resume after fixing, re-run manually with --skip-existing.
████████████████████████████████████████████████████████████████
EOF
    exit 43
  fi

  if [[ "$EXIT_CODE" -eq 130 ]]; then
    # SIGINT / SIGTERM / stop-file inside the classifier — user interrupted.
    # Do NOT relaunch. Log and exit.
    echo "[$(date '+%H:%M:%S')] interrupted by signal (exit 130) — stopping (not relaunching)." | tee -a "$LOG"
    break
  fi

  if [[ "$EXIT_CODE" -eq 42 ]]; then
    # RATE-LIMIT WALL — sleep then resume
    echo "[$(date '+%H:%M:%S')] Rate-limit wall (exit 42). Sleeping ${WALL_SLEEP}s..." | tee -a "$LOG"
    crash_streak=0
    no_progress_streak=0
    if ! sleep_with_stop_check "$WALL_SLEEP"; then
      echo "[$(date '+%H:%M:%S')] Stop file appeared during wall sleep — exiting." | tee -a "$LOG"
      break
    fi
    continue
  fi

  if [[ "$EXIT_CODE" -eq 0 ]]; then
    # Normal exit — check if truly done
    crash_streak=0
    remaining=$(count_remaining)
    echo "[$(date '+%H:%M:%S')] Exit 0. Remaining: $remaining rows." | tee -a "$LOG"

    if [[ "$remaining" -eq 0 ]]; then
      echo "[$(date '+%H:%M:%S')] All rows processed — mission complete!" | tee -a "$LOG"
      break
    fi

    # Rows remain — check for no-progress (persistent classify_failed rows that
    # will never be retried by --skip-existing logic).
    if [[ "$remaining" -eq "$prev_remaining" ]]; then
      no_progress_streak=$((no_progress_streak + 1))
      echo "[$(date '+%H:%M:%S')] No progress (remaining=$remaining, streak=$no_progress_streak)." | tee -a "$LOG"
      if [[ "$no_progress_streak" -ge 2 ]]; then
        echo "[$(date '+%H:%M:%S')] 2 consecutive no-progress iterations. Stuck on $remaining rows (likely classify_failed). Stopping." | tee -a "$LOG"
        break
      fi
    else
      no_progress_streak=0
    fi
    prev_remaining=$remaining

    # Brief yield before next iteration (chunked so stop-file is responsive).
    if ! sleep_with_stop_check 5; then
      echo "[$(date '+%H:%M:%S')] Stop file detected — exiting cleanly." | tee -a "$LOG"
      break
    fi
    continue
  fi

  # Any other non-zero exit code = crash
  crash_streak=$((crash_streak + 1))
  echo "[$(date '+%H:%M:%S')] Crash (exit $EXIT_CODE, streak=$crash_streak/$MAX_CRASHES). Sleeping 300s..." | tee -a "$LOG"
  if [[ "$crash_streak" -ge "$MAX_CRASHES" ]]; then
    echo "[$(date '+%H:%M:%S')] $MAX_CRASHES consecutive crashes — giving up." | tee -a "$LOG"
    # Clean up stop file so a future run isn't blocked, then exit.
    rm -f "$STOP_FILE"
    exit "$EXIT_CODE"
  fi
  if ! sleep_with_stop_check 300; then
    echo "[$(date '+%H:%M:%S')] Stop file detected during crash sleep — exiting." | tee -a "$LOG"
    break
  fi

done

# Remove stop file so a future run isn't blocked by a stale sentinel.
rm -f "$STOP_FILE"

echo "═══════════════════════════════════════════════════════════════" | tee -a "$LOG"
echo "  stage4-events-bulk-run finished at $(date '+%Y-%m-%d %H:%M:%S %Z')" | tee -a "$LOG"
echo "  Output: $OUT" | tee -a "$LOG"
echo "  Log:    $LOG" | tee -a "$LOG"
echo "═══════════════════════════════════════════════════════════════" | tee -a "$LOG"
