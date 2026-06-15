#!/usr/bin/env bash
# stage4-tail-bulk-forever.sh — Rate-limit-surviving overnight loop for the
# Stage 4 tail-classifier bulk enrichment run.
#
# Behavior:
#   Loop:
#     1. Invoke the tail classifier with --skip-existing so each resume picks up
#        exactly where the previous run left off.
#     2. Compute REMAINING = input rows (for the target candidate_kinds) minus
#        rows already decided (typed OR rejected) in the output dir.
#     3. Stop cleanly when: REMAINING==0, $HOME/source/claude-cwd/tmp/stage4-tail-stop exists, or
#        the max-iteration cap is reached (default 60).
#     4. Otherwise sleep STAGE4_SLEEP_BETWEEN seconds (default 1800) and retry.
#        If the classifier exited with the rate-limit code (42) OR two consecutive
#        iterations made ZERO progress, sleep STAGE4_WALL_SLEEP (default 3600).
#
# Per-iteration log line appended to:
#   working/wiki/data/smoke2-logs/enrich-haiku-forever.log
#
# Environment variables:
#   WEIRWOOD_PROJECT_DIR   — repo root (defaults to the script's parent dir)
#   STAGE4_MODEL           — model to use (default: claude-haiku-4-5)
#   STAGE4_KINDS           — comma-sep candidate_kinds (default: pass1_dialogue,pass1_events)
#   STAGE4_SLEEP_BETWEEN   — normal sleep seconds between iterations (default: 1800)
#   STAGE4_WALL_SLEEP      — extended sleep after rate-limit wall (default: 3600)
#   STAGE4_MAX_ITER        — maximum loop iterations before giving up (default: 60)
#
# Usage:
#   # Run in background, output to a log:
#   nohup bash scripts/stage4-tail-bulk-forever.sh >> working/wiki/data/smoke2-logs/enrich-haiku-forever.log 2>&1 &
#
#   # Soft-stop after the current iteration finishes:
#   touch $HOME/source/claude-cwd/tmp/stage4-tail-stop
#
set -uo pipefail

# ---------------------------------------------------------------------------
# Resolve repo root
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="${WEIRWOOD_PROJECT_DIR:-$(dirname "$SCRIPT_DIR")}"

# ---------------------------------------------------------------------------
# Configuration (overridable via environment)
# ---------------------------------------------------------------------------
MODEL="${STAGE4_MODEL:-claude-haiku-4-5}"
KINDS="${STAGE4_KINDS:-pass1_dialogue,pass1_events}"
SLEEP_BETWEEN="${STAGE4_SLEEP_BETWEEN:-1800}"
WALL_SLEEP="${STAGE4_WALL_SLEEP:-3600}"
MAX_ITER="${STAGE4_MAX_ITER:-60}"

INPUT_DIR="${REPO}/working/wiki/pass2-buckets/pass1-derived/_extra-tables"
OUTPUT_DIR="${REPO}/working/wiki/pass2-buckets/pass1-derived/_enrich-haiku"
LOG_FILE="${REPO}/working/wiki/data/smoke2-logs/enrich-haiku-forever.log"

# Rate-limit sentinel exit code (must match EXIT_CODE_RATE_LIMIT in the classifier)
RATE_LIMIT_CODE=42

# Soft-stop sentinel file
STOP_SENTINEL="$HOME/source/claude-cwd/tmp/stage4-tail-stop"

# ---------------------------------------------------------------------------
# Helper: count total input rows for the target candidate_kinds
# ---------------------------------------------------------------------------
count_input_rows() {
    python3 - <<PYEOF
import json
from pathlib import Path

base = Path("${INPUT_DIR}")
kinds = set("${KINDS}".split(","))
total = 0
for book_dir in sorted(base.iterdir()):
    if not book_dir.is_dir():
        continue
    for f in book_dir.glob("*.extra-tables.jsonl"):
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("edge_type") is not None:
                continue
            if row.get("candidate_kind") in kinds:
                total += 1
print(total)
PYEOF
}

# ---------------------------------------------------------------------------
# Helper: count decided rows already in the output dir
# (edges.jsonl = typed, rejected.jsonl = rejected — both count as "done")
# classify_failed rows are NOT counted so they are retried.
# ---------------------------------------------------------------------------
count_decided_rows() {
    python3 - <<PYEOF
import json
from pathlib import Path

base = Path("${OUTPUT_DIR}")
seen = set()
if base.exists():
    for book_dir in sorted(base.iterdir()):
        if not book_dir.is_dir():
            continue
        for f in list(book_dir.glob("*.edges.jsonl")) + list(book_dir.glob("*.rejected.jsonl")):
            for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                key = (
                    row.get("source_slug", ""),
                    row.get("target_slug", ""),
                    row.get("evidence_chapter", ""),
                )
                seen.add(key)
print(len(seen))
PYEOF
}

# ---------------------------------------------------------------------------
# Helper: count decided rows added THIS iteration (before vs after)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
echo "[$(date -Iseconds)] stage4-tail-bulk-forever.sh starting"
echo "[$(date -Iseconds)] repo:        ${REPO}"
echo "[$(date -Iseconds)] model:       ${MODEL}"
echo "[$(date -Iseconds)] kinds:       ${KINDS}"
echo "[$(date -Iseconds)] input_dir:   ${INPUT_DIR}"
echo "[$(date -Iseconds)] output_dir:  ${OUTPUT_DIR}"
echo "[$(date -Iseconds)] sleep_between: ${SLEEP_BETWEEN}s  wall_sleep: ${WALL_SLEEP}s  max_iter: ${MAX_ITER}"

TOTAL_INPUT="$(count_input_rows)"
echo "[$(date -Iseconds)] total input rows for kinds (${KINDS}): ${TOTAL_INPUT}"

consecutive_zero_progress=0
iter=0

while true; do
    iter=$((iter + 1))

    # -- Max-iteration cap --
    if [ "$iter" -gt "$MAX_ITER" ]; then
        echo "[$(date -Iseconds)] ITER ${iter}: max iterations (${MAX_ITER}) reached — stopping."
        echo "$(date -Iseconds) iter=${iter} reason=max_iter_cap" >> "${LOG_FILE}"
        exit 0
    fi

    # -- Soft-stop check (before running) --
    if [ -f "${STOP_SENTINEL}" ]; then
        echo "[$(date -Iseconds)] ITER ${iter}: stop sentinel found (${STOP_SENTINEL}) — stopping cleanly."
        echo "$(date -Iseconds) iter=${iter} reason=stop_sentinel" >> "${LOG_FILE}"
        exit 0
    fi

    # -- Compute REMAINING before this run --
    decided_before="$(count_decided_rows)"
    remaining_before=$((TOTAL_INPUT - decided_before))

    if [ "$remaining_before" -le 0 ]; then
        echo "[$(date -Iseconds)] ITER ${iter}: REMAINING=0 — all rows decided. Done!"
        echo "$(date -Iseconds) iter=${iter} remaining=0 decided=${decided_before} reason=complete" >> "${LOG_FILE}"
        exit 0
    fi

    echo "[$(date -Iseconds)] ITER ${iter}: remaining=${remaining_before} (decided=${decided_before}/${TOTAL_INPUT})"

    # -- Run the classifier --
    classifier_cmd=(
        python3 "${REPO}/scripts/stage4-tail-classifier.py"
        --apply
        --skip-existing
        --abort-after-consecutive-failures 5
        --model "${MODEL}"
        --input-dir "${INPUT_DIR}"
        --candidate-kinds "${KINDS}"
        --output-dir "${OUTPUT_DIR}"
    )

    echo "[$(date -Iseconds)] ITER ${iter}: running: ${classifier_cmd[*]}"
    exit_code=0
    "${classifier_cmd[@]}" || exit_code=$?

    # -- Compute progress this iteration --
    decided_after="$(count_decided_rows)"
    typed_this_iter=$((decided_after - decided_before))
    remaining_after=$((TOTAL_INPUT - decided_after))

    echo "[$(date -Iseconds)] ITER ${iter}: exit_code=${exit_code} typed_this_iter=${typed_this_iter} remaining=${remaining_after}"

    # -- Append to persistent log --
    echo "$(date -Iseconds) iter=${iter} exit_code=${exit_code} typed_this_iter=${typed_this_iter} remaining=${remaining_after} decided=${decided_after}/${TOTAL_INPUT}" >> "${LOG_FILE}"

    # -- Completion check --
    if [ "$remaining_after" -le 0 ]; then
        echo "[$(date -Iseconds)] ITER ${iter}: REMAINING=0 after run — all rows decided. Done!"
        echo "$(date -Iseconds) iter=${iter} remaining=0 reason=complete" >> "${LOG_FILE}"
        exit 0
    fi

    # -- Soft-stop check (after running) --
    if [ -f "${STOP_SENTINEL}" ]; then
        echo "[$(date -Iseconds)] ITER ${iter}: stop sentinel found after run — stopping cleanly."
        echo "$(date -Iseconds) iter=${iter} reason=stop_sentinel_post_run" >> "${LOG_FILE}"
        exit 0
    fi

    # -- Decide sleep duration --
    sleep_duration="${SLEEP_BETWEEN}"
    sleep_reason="normal"

    if [ "$exit_code" -eq "$RATE_LIMIT_CODE" ]; then
        # Classifier hit rate-limit wall — use extended sleep
        sleep_duration="${WALL_SLEEP}"
        sleep_reason="rate_limit_wall(exit=${exit_code})"
        consecutive_zero_progress=0  # rate-limit exit resets the zero-progress counter
    elif [ "$typed_this_iter" -eq 0 ]; then
        consecutive_zero_progress=$((consecutive_zero_progress + 1))
        if [ "$consecutive_zero_progress" -ge 2 ]; then
            sleep_duration="${WALL_SLEEP}"
            sleep_reason="zero_progress_x${consecutive_zero_progress}"
        fi
    else
        consecutive_zero_progress=0
    fi

    echo "[$(date -Iseconds)] ITER ${iter}: sleeping ${sleep_duration}s (${sleep_reason})..."
    echo "$(date -Iseconds) iter=${iter} sleeping=${sleep_duration}s reason=${sleep_reason}" >> "${LOG_FILE}"
    sleep "${sleep_duration}"
done
