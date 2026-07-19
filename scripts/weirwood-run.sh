#!/usr/bin/env bash
# weirwood-run.sh — Declarative long-run track registry for the Weirwood Network.
#
# Wraps scripts/longrun.sh: every track launch gets a timestamped log, a
# latest-symlink, and a pidfile under working/logs/longrun/.
#
# Usage (called via weirwood.zsh):
#   bash scripts/weirwood-run.sh list
#   bash scripts/weirwood-run.sh start <track>
#   bash scripts/weirwood-run.sh start custom -- <cmd...>
#   bash scripts/weirwood-run.sh logs   <track>
#   bash scripts/weirwood-run.sh status <track>
#   bash scripts/weirwood-run.sh stop   <track>
#
# Exit-code contract for supervised commands (enforced by longrun.sh):
#   0   — work complete; supervisor exits
#   2   — rate-limit wall; supervisor sleeps LONGRUN_WALL_SLEEP then relaunches
#   10  — iteration done, more work remains; sleeps LONGRUN_SLEEP_BETWEEN then relaunches
#   other nonzero — crash; supervisor retries up to LONGRUN_MAX_CRASHES times
#
# LEGACY tracks listed here are NOT launchable here — their tracks are
# shelved/shipped and the wrappers were archived to scripts/archive/ during the
# 2026-06-15 script consolidation (Session 2). The legacy wrappers
# (scripts/archive/stage4-tail-bulk-forever.sh, scripts/archive/stage4-haiku-run-forever.sh,
# scripts/archive/stage4-events-bulk-run.sh) use their own exit codes (42/43/130)
# and bespoke loop logic. Their good ideas (rate-limit detect, sleep defaults)
# are folded into pace.py + scripts/worker-template.py; revive from archive only
# if a track is reopened and migrated to the longrun.sh 0/2/10 contract.

set -uo pipefail

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LONGRUN_SH="$SCRIPT_DIR/longrun.sh"
LOG_DIR="$REPO_ROOT/working/logs/longrun"

# ---------------------------------------------------------------------------
# Track registry
#
# Format per entry:
#   TRACK_NAMES+=("name")
#   TRACK_STATUS+=("READY | LEGACY-not-yet-migrated | PLANNED")
#   TRACK_DESC+=("human description")
#   TRACK_CMD+=("command string to eval — empty for LEGACY/PLANNED")
#
# READY    — runner exists and honours the 0/2/10 exit-code contract
# PLANNED  — runner exists but uses a different exit-code protocol; migration todo
# LEGACY-not-yet-migrated — pre-longrun.sh wrapper; do not launch via this registry
# ---------------------------------------------------------------------------

TRACK_NAMES=()
TRACK_STATUS=()
TRACK_DESC=()
TRACK_CMD=()

# ── Active tracks ──────────────────────────────────────────────────────────

# edge-reify: runner exists (scripts/edge-reify-backfill.py) but the current
# wrapper (edge-reify-run-forever.sh) uses exit codes 0/2/130/crash — close
# to the longrun.sh contract (2=wall maps directly) EXCEPT exit 10 is never
# emitted (the script loops internally rather than returning 10).  Mark PLANNED
# until the Python runner emits exit 10 for "more work remains".
TRACK_NAMES+=("edge-reify")
TRACK_STATUS+=("PLANNED")
TRACK_DESC+=("Plate 3 edge reification backfill (scripts/edge-reify-backfill.py) — runner needs exit 10 before migration")
TRACK_CMD+=("")

# dunk-egg-pass1: worker graduated to scripts/ at the DE-3 fire-gate (2026-07-18) after the v4/THK+TSS
# smoke judges both returned PROMOTE-READY (8/8 checklist PASS each). Prompt pinned v4; queue pinned to
# the scene-split parts queue (split decision A — parts verified lossless, delta-0 words vs originals).
# Absolute paths because _launch_track does not cd (--queue resolves cwd-relative in the worker).
TRACK_NAMES+=("dunk-egg-pass1")
TRACK_STATUS+=("READY")
TRACK_DESC+=("Dunk & Egg Pass-1 full extraction (THK/TSS/TMK, 24 scene-split part-units) — scripts/dunk-egg-pass1-extraction.py, prompt v4")
TRACK_CMD+=("python3 $REPO_ROOT/scripts/dunk-egg-pass1-extraction.py --resume --prompt-version v4 --queue $REPO_ROOT/working/dunk-egg-pass1/queue-parts.jsonl")

# fire-and-blood: worker exists (working/fire-and-blood/fire-and-blood-extraction.py, built S198) and
# already honors the 0/2/10/crash contract, but mirrors dunk-egg-pass1's convention above — it stays
# unregistered while the worker lives in working/ (pre-graduation scaffold), so this entry is PLANNED
# rather than a live READY pointing at a not-yet-graduated script. Once Matt greenlights the full run:
#   1. git mv working/fire-and-blood/fire-and-blood-extraction.py scripts/
#   2. flip TRACK_STATUS below to "READY"
#   3. TRACK_CMD -> "python3 scripts/fire-and-blood-extraction.py --resume --prompt-version v1"
#      (pin the winning --prompt-version once smoke-testing picks it)
TRACK_NAMES+=("fire-and-blood")
TRACK_STATUS+=("PLANNED")
TRACK_DESC+=("Fire & Blood node-first enrichment (39 units) — working/fire-and-blood/fire-and-blood-extraction.py; PLANNED until graduated to scripts/ + Matt greenlight. Full command: bash scripts/longrun.sh python3 working/fire-and-blood/fire-and-blood-extraction.py --resume --prompt-version v1")
TRACK_CMD+=("")

# ── Legacy tracks (pre-longrun.sh wrappers; do not launch) ────────────────

TRACK_NAMES+=("stage4-tail")
TRACK_STATUS+=("LEGACY-not-yet-migrated")
TRACK_DESC+=("Stage 4 tail-model bulk classifier — scripts/archive/stage4-tail-bulk-forever.sh (archived; exit codes 42/43/130 — not longrun.sh compatible)")
TRACK_CMD+=("")

TRACK_NAMES+=("stage4-haiku")
TRACK_STATUS+=("LEGACY-not-yet-migrated")
TRACK_DESC+=("Stage 4 Haiku bulk classifier — scripts/archive/stage4-haiku-run-forever.sh (archived; exit codes 42/43/130 — not longrun.sh compatible)")
TRACK_CMD+=("")

TRACK_NAMES+=("stage4-events")
TRACK_STATUS+=("LEGACY-not-yet-migrated")
TRACK_DESC+=("Stage 4 pass1_events Haiku typing run — scripts/archive/stage4-events-bulk-run.sh (archived; exit codes 42/43/130 — not longrun.sh compatible)")
TRACK_CMD+=("")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

die() { echo "ERROR: $*" >&2; exit 1; }

# Look up a track index by name; print index to stdout, return 1 if not found.
find_track() {
    local name="$1"
    local i
    for i in "${!TRACK_NAMES[@]}"; do
        if [[ "${TRACK_NAMES[$i]}" == "$name" ]]; then
            echo "$i"
            return 0
        fi
    done
    return 1
}

pid_file()    { echo "$LOG_DIR/$1.pid"; }
latest_log()  { echo "$LOG_DIR/$1-latest.log"; }

# Read the pid from a pidfile; returns empty string if file missing or empty.
read_pid() {
    local pf
    pf="$(pid_file "$1")"
    [[ -f "$pf" ]] && cat "$pf" || echo ""
}

# Return 0 if process is alive, 1 otherwise.
pid_alive() {
    local pid="$1"
    [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

# Clean up a stale pidfile (process gone); prints a notice.
clean_stale_pid() {
    local track="$1" pid="$2"
    echo "Notice: stale pidfile for '$track' (pid $pid no longer running) — cleaning up."
    rm -f "$(pid_file "$track")"
}

# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------
cmd_list() {
    printf "%-22s  %-30s  %s\n" "TRACK" "STATUS" "DESCRIPTION"
    printf "%-22s  %-30s  %s\n" "------" "------" "-----------"
    local i
    for i in "${!TRACK_NAMES[@]}"; do
        printf "%-22s  %-30s  %s\n" \
            "${TRACK_NAMES[$i]}" \
            "${TRACK_STATUS[$i]}" \
            "${TRACK_DESC[$i]}"
    done
    echo ""
    echo "Launch: weirwood run start <track>"
    echo "        weirwood run start custom -- <command...>"
}

# ---------------------------------------------------------------------------
# start
# ---------------------------------------------------------------------------
cmd_start() {
    local track="$1"
    shift  # remaining args are the command for 'custom'

    mkdir -p "$LOG_DIR"

    # ── custom escape hatch ──────────────────────────────────────────────────
    if [[ "$track" == "custom" ]]; then
        # Expect: start custom -- <cmd...>
        if [[ "${1:-}" != "--" ]]; then
            die "Usage: weirwood run start custom -- <command...>"
        fi
        shift  # consume '--'
        if [[ $# -eq 0 ]]; then
            die "start custom: no command specified after '--'"
        fi
        _launch_track "custom" "$@"
        return
    fi

    # ── registry track ───────────────────────────────────────────────────────
    local idx
    idx="$(find_track "$track")" || die "Unknown track '$track'. Run 'weirwood run list' to see available tracks."

    local status="${TRACK_STATUS[$idx]}"
    case "$status" in
        LEGACY-not-yet-migrated)
            echo "ERROR: track '$track' is LEGACY-not-yet-migrated and cannot be launched here." >&2
            echo "" >&2
            echo "  The legacy wrapper for this track uses a non-standard exit-code protocol" >&2
            echo "  (exit 42/43/130 instead of longrun.sh's 0/2/10 contract)." >&2
            echo "  Migration todo: update the runner to emit exit 10 for 'more work remains'," >&2
            echo "  exit 2 for rate-limit wall, and exit 0 for completion; then change its" >&2
            echo "  status to READY in the TRACK_STATUS registry in scripts/weirwood-run.sh." >&2
            echo "" >&2
            echo "  To run the (archived) legacy wrapper directly:" >&2
            echo "    bash scripts/archive/stage4-events-bulk-run.sh   (for stage4-events)" >&2
            echo "    bash scripts/archive/stage4-haiku-run-forever.sh  (for stage4-haiku)" >&2
            echo "    bash scripts/archive/stage4-tail-bulk-forever.sh  (for stage4-tail)" >&2
            return 1
            ;;
        PLANNED)
            echo "ERROR: track '$track' is PLANNED — the runner exists but has not yet been" >&2
            echo "  updated to emit longrun.sh exit codes (0=done, 2=wall, 10=more-work)." >&2
            echo "  See the track description for migration notes:" >&2
            echo "    ${TRACK_DESC[$idx]}" >&2
            return 1
            ;;
        READY)
            local cmd="${TRACK_CMD[$idx]}"
            if [[ -z "$cmd" ]]; then
                die "Track '$track' is marked READY but has no command configured — update TRACK_CMD in weirwood-run.sh."
            fi
            # Split command string into array (simple word-split; no fancy quoting)
            # shellcheck disable=SC2086
            _launch_track "$track" $cmd
            ;;
        *)
            die "Track '$track' has unknown status '$status'."
            ;;
    esac
}

# _launch_track <track_name> <cmd...>
# Checks for double-start, builds log path + pidfile, launches via longrun.sh.
_launch_track() {
    local track="$1"
    shift
    local cmd=("$@")

    local pf
    pf="$(pid_file "$track")"
    local existing_pid
    existing_pid="$(read_pid "$track")"

    if [[ -n "$existing_pid" ]]; then
        if pid_alive "$existing_pid"; then
            echo "ERROR: track '$track' is already running (pid $existing_pid)." >&2
            echo "  Use 'weirwood run stop $track' to stop it, or 'weirwood run status $track' to check." >&2
            return 1
        else
            clean_stale_pid "$track" "$existing_pid"
        fi
    fi

    local ts
    ts="$(date '+%Y%m%d-%H%M%S')"
    local log_file="$LOG_DIR/${track}-${ts}.log"
    local latest
    latest="$(latest_log "$track")"

    # Write pidfile placeholder (will be overwritten with real pid below)
    touch "$log_file"
    ln -sf "$log_file" "$latest"

    echo "Starting track '$track'..."
    echo "  Command:  ${cmd[*]}"
    echo "  Log:      $log_file"
    echo "  Latest:   $latest"
    echo "  Pidfile:  $pf"

    # Launch longrun.sh in background.  LONGRUN_LOG tells longrun.sh to tee
    # everything to the file itself — do NOT also redirect stdout/stderr to the
    # same file or every line will be doubled.
    export LONGRUN_LOG="$log_file"
    nohup bash "$LONGRUN_SH" "${cmd[@]}" > /dev/null 2>&1 &
    local bgpid=$!
    disown "$bgpid" 2>/dev/null || true

    echo "$bgpid" > "$pf"
    echo "  PID:      $bgpid"
    echo ""
    echo "Track '$track' launched (pid $bgpid). Follow with:"
    echo "  weirwood run logs $track"
}

# ---------------------------------------------------------------------------
# logs
# ---------------------------------------------------------------------------
cmd_logs() {
    local track="$1"
    local latest
    latest="$(latest_log "$track")"
    if [[ ! -L "$latest" && ! -f "$latest" ]]; then
        die "No log found for track '$track'. Has it been started? (expected: $latest)"
    fi
    echo "Tailing $latest  (Ctrl-C to stop)"
    echo ""
    tail -f "$latest"
}

# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------
cmd_status() {
    local track="$1"
    local pf
    pf="$(pid_file "$track")"
    local pid
    pid="$(read_pid "$track")"
    local latest
    latest="$(latest_log "$track")"

    echo "Track: $track"

    # Registry info (skip for 'custom')
    local idx
    if idx="$(find_track "$track")" 2>/dev/null; then
        echo "  Status (registry): ${TRACK_STATUS[$idx]}"
        echo "  Description:       ${TRACK_DESC[$idx]}"
    fi

    # Process status
    if [[ -z "$pid" ]]; then
        echo "  Process: not running (no pidfile)"
    elif pid_alive "$pid"; then
        echo "  Process: RUNNING (pid $pid)"
    else
        echo "  Process: STOPPED (pid $pid — stale pidfile)"
        clean_stale_pid "$track" "$pid"
    fi

    # Log tail
    if [[ -L "$latest" || -f "$latest" ]]; then
        echo "  Log: $latest"
        echo "  --- last 10 lines ---"
        tail -10 "$latest" 2>/dev/null | sed 's/^/  /'
    else
        echo "  Log: (none found)"
    fi
}

# ---------------------------------------------------------------------------
# stop
# ---------------------------------------------------------------------------
cmd_stop() {
    local track="$1"
    local pid
    pid="$(read_pid "$track")"

    if [[ -z "$pid" ]]; then
        echo "Track '$track' has no pidfile — not running (or already stopped)."
        return 0
    fi

    if ! pid_alive "$pid"; then
        clean_stale_pid "$track" "$pid"
        echo "Track '$track' was not running (stale pidfile cleaned up)."
        return 0
    fi

    echo "Sending SIGTERM to '$track' (pid $pid)..."
    kill -TERM "$pid" 2>/dev/null || true

    # Wait briefly for graceful exit
    local waited=0
    while pid_alive "$pid" && (( waited < 10 )); do
        sleep 1
        waited=$((waited + 1))
    done

    if pid_alive "$pid"; then
        echo "Process $pid still alive after ${waited}s — it may be sleeping between iterations."
        echo "longrun.sh will exit cleanly once its current sleep/iteration completes."
        echo "To force-kill: kill -9 $pid"
    else
        rm -f "$(pid_file "$track")"
        echo "Track '$track' stopped."
    fi
}

# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------
SUB="${1:-}"
shift || true

case "$SUB" in
    list)
        cmd_list
        ;;
    start)
        TRACK="${1:-}"
        [[ -z "$TRACK" ]] && die "Usage: weirwood run start <track>  OR  weirwood run start custom -- <cmd...>"
        shift
        cmd_start "$TRACK" "$@"
        ;;
    logs)
        TRACK="${1:-}"
        [[ -z "$TRACK" ]] && die "Usage: weirwood run logs <track>"
        cmd_logs "$TRACK"
        ;;
    status)
        TRACK="${1:-}"
        [[ -z "$TRACK" ]] && die "Usage: weirwood run status <track>"
        cmd_status "$TRACK"
        ;;
    stop)
        TRACK="${1:-}"
        [[ -z "$TRACK" ]] && die "Usage: weirwood run stop <track>"
        cmd_stop "$TRACK"
        ;;
    ""|--help|-h)
        echo "weirwood run — declarative long-run track launcher"
        echo ""
        echo "Commands:"
        echo "  weirwood run list                   List all tracks and their status"
        echo "  weirwood run start <track>           Launch a READY track via longrun.sh"
        echo "  weirwood run start custom -- <cmd>   Launch any command via longrun.sh"
        echo "  weirwood run logs <track>            Tail the latest log (Ctrl-C to stop)"
        echo "  weirwood run status <track>          PID alive? last log lines? pidfile?"
        echo "  weirwood run stop <track>            SIGTERM via pidfile; report result"
        echo ""
        echo "Log location: working/logs/longrun/<track>-<YYYYmmdd-HHMMSS>.log"
        echo "  Symlink:    working/logs/longrun/<track>-latest.log"
        echo "  Pidfile:    working/logs/longrun/<track>.pid"
        echo ""
        echo "Exit-code contract (required by supervised commands):"
        echo "  0   — all work complete"
        echo "  2   — rate-limit wall (supervisor sleeps LONGRUN_WALL_SLEEP then retries)"
        echo "  10  — iteration done, more work remains (sleeps LONGRUN_SLEEP_BETWEEN)"
        echo "  other — crash (retries up to LONGRUN_MAX_CRASHES times)"
        echo ""
        echo "Examples:"
        echo "  weirwood run list"
        echo "  weirwood run start custom -- python3 scripts/my-runner.py --resume"
        echo "  weirwood run logs custom"
        echo "  weirwood run status custom"
        echo "  weirwood run stop custom"
        ;;
    *)
        die "Unknown subcommand '$SUB'. Run 'weirwood run --help' for usage."
        ;;
esac
