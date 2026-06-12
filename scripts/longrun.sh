#!/usr/bin/env bash
# longrun.sh — Generic long-run supervisor for the Weirwood Network project.
#
# Supervises any command, relaunching it on rate-limit walls and crashes while
# exiting cleanly on success. Resume semantics (--resume, --skip-existing, etc.)
# belong to the supervised command — the supervisor just relaunches the same argv.
#
# Usage:
#   bash scripts/longrun.sh <command> [args...]
#
# Examples:
#   bash scripts/longrun.sh python3 scripts/edge-reify-backfill.py --all --resume
#   LONGRUN_SLEEP_BETWEEN=900 bash scripts/longrun.sh python3 scripts/stage4-classifier.py \
#       --apply --skip-existing --model claude-haiku-4-5
#
# Exit-code contract for the supervised command:
#   0   — all work complete; supervisor exits 0 (does NOT loop)
#   2   — rate-limit wall; supervisor sleeps LONGRUN_WALL_SLEEP then relaunches
#   10  — iteration succeeded, more work remains; sleeps LONGRUN_SLEEP_BETWEEN then relaunches
#   any other nonzero — crash; sleeps LONGRUN_CRASH_SLEEP then relaunches;
#                        gives up after LONGRUN_MAX_CRASHES consecutive crashes (supervisor exits 1)
#
# Environment variables (all optional):
#   LONGRUN_SLEEP_BETWEEN  — seconds between successful iterations (default: 1200 = 20 min)
#   LONGRUN_WALL_SLEEP     — seconds to sleep after a rate-limit wall, exit code 2 (default: 3600 = 1 hr)
#   LONGRUN_CRASH_SLEEP    — seconds to sleep after a crash (default: 300 = 5 min)
#   LONGRUN_MAX_CRASHES    — max consecutive crashes before giving up (default: 5)
#   LONGRUN_MAX_ITER       — stop after N iterations regardless of outcome, 0 = unbounded (default: 0)
#   LONGRUN_LOG            — if set, tee all output to this file (appended)
#
# Legacy wrappers (stage4-run-forever.sh, edge-reify-run-forever.sh, etc.) remain
# untouched and can migrate to thin call-throughs using this script track-by-track
# as each finishes its current run.

set -uo pipefail

# ---------------------------------------------------------------------------
# Guard: require at least one argument (the command to supervise)
# ---------------------------------------------------------------------------
if [[ $# -eq 0 ]]; then
    echo "Usage: bash longrun.sh <command> [args...]" >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SLEEP_BETWEEN="${LONGRUN_SLEEP_BETWEEN:-1200}"
WALL_SLEEP="${LONGRUN_WALL_SLEEP:-3600}"
CRASH_SLEEP="${LONGRUN_CRASH_SLEEP:-300}"
MAX_CRASHES="${LONGRUN_MAX_CRASHES:-5}"
MAX_ITER="${LONGRUN_MAX_ITER:-0}"
LONGRUN_LOG="${LONGRUN_LOG:-}"

# ---------------------------------------------------------------------------
# Logging helper — writes to stdout (and tees to LONGRUN_LOG if set)
# ---------------------------------------------------------------------------
log() {
    local msg
    msg="[$(date -Iseconds)] $*"
    if [[ -n "$LONGRUN_LOG" ]]; then
        echo "$msg" | tee -a "$LONGRUN_LOG"
    else
        echo "$msg"
    fi
}

# ---------------------------------------------------------------------------
# Startup banner
# ---------------------------------------------------------------------------
log "═══════════════════════════════════════════════════════════════"
log "  longrun.sh — generic long-run supervisor"
log "  Command:       $*"
log "  sleep_between: ${SLEEP_BETWEEN}s ($((SLEEP_BETWEEN / 60))min) after exit 10"
log "  wall_sleep:    ${WALL_SLEEP}s ($((WALL_SLEEP / 60))min) after exit 2"
log "  crash_sleep:   ${CRASH_SLEEP}s ($((CRASH_SLEEP / 60))min) after crash"
log "  max_crashes:   ${MAX_CRASHES} consecutive before giving up"
log "  max_iter:      ${MAX_ITER} (0 = unbounded)"
log "  log_file:      ${LONGRUN_LOG:-<stdout only>}"
log "═══════════════════════════════════════════════════════════════"

# ---------------------------------------------------------------------------
# SIGINT / SIGTERM — exit cleanly without relaunching
# ---------------------------------------------------------------------------
trap 'log "Signal received — exiting supervisor cleanly."; exit 130' INT TERM

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
iter=0
crash_streak=0

while true; do
    iter=$((iter + 1))

    # -- Max-iteration cap --
    if [[ "$MAX_ITER" -gt 0 && "$iter" -gt "$MAX_ITER" ]]; then
        log "MAX_ITER=${MAX_ITER} reached — stopping supervisor."
        exit 0
    fi

    # -- Run the supervised command --
    iter_start=$(date +%s)
    log "iter=${iter} start — launching: $*"

    exit_code=0
    if [[ -n "$LONGRUN_LOG" ]]; then
        "$@" 2>&1 | tee -a "$LONGRUN_LOG"; exit_code=${PIPESTATUS[0]}
    else
        "$@" || exit_code=$?
    fi

    iter_elapsed=$(( $(date +%s) - iter_start ))
    log "iter=${iter} done — exit_code=${exit_code} elapsed=${iter_elapsed}s"

    # -- Interpret exit code --

    if [[ "$exit_code" -eq 0 ]]; then
        # All work complete — stop.
        crash_streak=0
        log "exit 0: work complete. Supervisor exiting 0."
        exit 0
    fi

    if [[ "$exit_code" -eq 2 ]]; then
        # Rate-limit wall.
        crash_streak=0
        log "exit 2: rate-limit wall. Sleeping ${WALL_SLEEP}s ($((WALL_SLEEP / 60))min)..."
        sleep "$WALL_SLEEP"
        continue
    fi

    if [[ "$exit_code" -eq 10 ]]; then
        # Iteration succeeded, more work remains.
        crash_streak=0
        log "exit 10: iteration complete, more work remains. Sleeping ${SLEEP_BETWEEN}s ($((SLEEP_BETWEEN / 60))min)..."
        sleep "$SLEEP_BETWEEN"
        continue
    fi

    # Any other nonzero = crash.
    crash_streak=$((crash_streak + 1))
    log "exit ${exit_code}: crash (streak=${crash_streak}/${MAX_CRASHES}). Sleeping ${CRASH_SLEEP}s..."
    if [[ "$crash_streak" -ge "$MAX_CRASHES" ]]; then
        log "${MAX_CRASHES} consecutive crashes — giving up. Supervisor exiting 1."
        exit 1
    fi
    sleep "$CRASH_SLEEP"
done
