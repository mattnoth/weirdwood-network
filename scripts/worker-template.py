#!/usr/bin/env python3
"""worker-template.py — Reference resumable worker (COPY-ME template).

This file demonstrates the §4 worker contract + §13 M-amendments from the
Weirwood orchestration design (working/orchestration-pacer-design-2026-06-15.md).
It is NOT a production worker — it processes fake units from a queue file so
the contract is concrete and runnable. Copy it and replace the fake work loop
with your real task.

EXIT-CODE CONTRACT (§3)
-----------------------
  0   — all work complete (queue fully drained)
  2   — POSITIVE rate-limit wall detected (longrun.sh sleeps LONGRUN_WALL_SLEEP, relaunches)
  10  — this chunk done, more work remains (longrun.sh sleeps LONGRUN_SLEEP_BETWEEN, relaunches)
  other — crash (longrun.sh retries up to LONGRUN_MAX_CRASHES, then gives up)

IMPORTANT (§13 M1): exit(2) is ONLY emitted when the worker has confirmed a
positive rate-limit signal. If the failure reason is ambiguous, exit with
crash (non-0/2/10). A spurious exit(2) silently burns a full LONGRUN_WALL_SLEEP.

LAUNCH LINE
-----------
  weirwood run start custom -- python3 scripts/worker-template.py --resume

CHUNK SIZING (§13 S5)
---------------------
  Size a chunk to finish comfortably under LONGRUN_SLEEP_BETWEEN.
  Lose ≤1 chunk on crash. Typical: Pass-1 chapter ~250s, Haiku chunk ~157s.
  At LONGRUN_SLEEP_BETWEEN=1200s, a safe chunk is ~5 Pass-1 chapters or
  ~7 Haiku batches.

STATE FILES (§13 M2 — atomic writes)
--------------------------------------
  All multi-byte state files (progress manifest, claim markers) use
  write-to-tmp-then-os.replace() (atomic rename). A SIGTERM mid-write
  (from `weirwood run stop`) must not corrupt progress.
  Telemetry JSONL appends are single-line → POSIX-atomic → append directly.

CONCURRENT CLAIMING (§4.3)
---------------------------
  Units are claimed via os.open(O_CREAT|O_EXCL) lock files — the OS kernel
  makes this atomic even with concurrent workers. Future fan-out can share
  one queue safely.

WALL DETECTION (§13 M1, M4)
----------------------------
  In a real claude -p worker, detect the wall by grepping the stream for:
      {"type":"result","subtype":"error","is_error":true}
  with  "rateLimitType" in the JSON (as scripts/stage4.sh:403 does).
  On detection:
    1. Write reset timestamp to working/telemetry/<track>.next-eligible
       so ALL supervisors of this track wake at the authoritative reset.
    2. exit(2) so longrun.sh sleeps LONGRUN_WALL_SLEEP then relaunches.
  If the failure reason is ambiguous → exit with crash code, NEVER exit(2).
  v1 ships single-worker-durable; multi-worker burst is gated on M4 being
  implemented (all supervisors reading the shared next-eligible file).
"""

import argparse
import json
import os
import sys
import time
import uuid
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: locate the repo root and import pace.emit_telemetry_row.
# When copied to a real worker, adjust this path or use importlib.
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Add scripts/ to sys.path so we can import pace as a module
sys.path.insert(0, str(SCRIPT_DIR))
import importlib.util as _ilu

def _load_pace():
    spec = _ilu.spec_from_file_location("pace", SCRIPT_DIR / "pace.py")
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_pace = _load_pace()
emit_telemetry_row = _pace.emit_telemetry_row

# ---------------------------------------------------------------------------
# Configuration — adjust per worker
# ---------------------------------------------------------------------------
TRACK = "demo-worker"          # Telemetry track name
CHUNK_SIZE = 3                 # Units per chunk (before exiting 10)
DEFAULT_QUEUE_FILE = PROJECT_ROOT / "working" / "telemetry" / "demo-queue.jsonl"
DEFAULT_MANIFEST_FILE = PROJECT_ROOT / "working" / "telemetry" / "demo-manifest.json"
TELEMETRY_DIR = PROJECT_ROOT / "working" / "telemetry"

# ---------------------------------------------------------------------------
# Atomic state write (§13 M2)
# ---------------------------------------------------------------------------

def _atomic_write_json(path: Path, data: dict) -> None:
    """Write JSON to path atomically via tmp-then-rename.

    A SIGTERM between the write and the rename leaves the old file intact.
    Never leaves a partially-written file at the target path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n")
    os.replace(tmp, path)  # atomic rename on POSIX


def _load_json(path: Path, default: dict) -> dict:
    """Load JSON from path, returning default if missing or corrupt."""
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return default


# ---------------------------------------------------------------------------
# Queue (demo — real workers use a chapter list, edge queue, etc.)
# ---------------------------------------------------------------------------

def _ensure_demo_queue(queue_file: Path, n_units: int = 10) -> None:
    """Create a demo queue of fake units if it does not already exist."""
    if queue_file.exists():
        return
    queue_file.parent.mkdir(parents=True, exist_ok=True)
    with open(queue_file, "w") as fh:
        for i in range(n_units):
            fh.write(json.dumps({"unit_id": f"demo-unit-{i:03d}", "payload": f"data-{i}"}) + "\n")


def _load_queue(queue_file: Path) -> list[dict]:
    """Load all units from the queue JSONL file."""
    if not queue_file.exists():
        return []
    units = []
    with open(queue_file) as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    units.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return units


# ---------------------------------------------------------------------------
# Atomic unit claiming (§4.3)
# ---------------------------------------------------------------------------

def _claim_unit(unit_id: str, lock_dir: Path) -> bool:
    """Atomically claim a unit via O_CREAT|O_EXCL lock file.

    Returns True if this worker successfully claimed the unit.
    Returns False if another worker already claimed it.
    This is POSIX-atomic — safe for concurrent processes sharing the same dir.
    """
    lock_dir.mkdir(parents=True, exist_ok=True)
    lock_file = lock_dir / f"{unit_id}.lock"
    try:
        fd = os.open(str(lock_file), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        return True
    except FileExistsError:
        return False


def _is_done(unit_id: str, manifest: dict) -> bool:
    """Return True if unit_id is already marked done in the manifest."""
    return unit_id in manifest.get("done", [])


def _mark_done(unit_id: str, manifest: dict, manifest_file: Path) -> dict:
    """Mark unit_id as done in the manifest and atomically persist it."""
    done_list = manifest.get("done", [])
    if unit_id not in done_list:
        done_list.append(unit_id)
    manifest["done"] = done_list
    _atomic_write_json(manifest_file, manifest)
    return manifest


# ---------------------------------------------------------------------------
# Rate-limit wall handling (§13 M1, M4)
# ---------------------------------------------------------------------------

def _write_next_eligible(track: str, reset_ts: str | None = None) -> None:
    """Write the authoritative rate-limit reset timestamp to the next-eligible sidecar.

    All supervisors of this track should read this file when they wake, so
    they don't re-storm the API before the window resets.
    Format: ISO-8601 string or unix timestamp string.
    """
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
    eligible_file = TELEMETRY_DIR / f"{track}.next-eligible"
    ts = reset_ts or str(int(time.time()) + 3600)  # default: 1h from now
    eligible_file.write_text(ts + "\n")
    print(f"  [wall] Wrote next-eligible reset time: {ts}", file=sys.stderr)


def _simulate_rate_limit_check(unit_id: str, env: dict) -> bool:
    """Simulate rate-limit detection for the template demo.

    In a REAL worker, you would:
      1. Run:  proc = subprocess.run(["claude", "-p", ...], capture_output=True)
      2. Parse proc.stdout for lines containing '"is_error":true'
         and '"rateLimitType"' (as scripts/stage4.sh:403 does).
      3. Return True ONLY if that pattern is found.

    Returning True here when SIMULATE_RATE_LIMIT=1 lets you exercise the
    exit(2) path without a real API call.
    """
    return env.get("SIMULATE_RATE_LIMIT", "0") == "1" and unit_id.endswith("004")


def _do_real_work(unit: dict) -> dict:
    """Placeholder: do the actual unit processing.

    Returns a result dict. In a real worker this calls claude -p, runs an
    extraction, etc. Replace this with your task logic.
    """
    # Simulate some work taking 0.05s per unit (fast for demo)
    time.sleep(0.05)
    return {"status": "ok", "unit_id": unit["unit_id"]}


# ---------------------------------------------------------------------------
# Worker main loop (§4)
# ---------------------------------------------------------------------------

def run_worker(args: argparse.Namespace) -> int:
    """Main worker loop. Returns the exit code (0/2/10/crash)."""

    queue_file = Path(args.queue)
    manifest_file = Path(args.manifest)
    lock_dir = manifest_file.parent / "locks"

    # --- Ensure demo queue exists (remove this block in a real worker) ---
    _ensure_demo_queue(queue_file, n_units=10)

    # --- Load or initialise manifest (resumable — §4.1) ---
    manifest = _load_json(manifest_file, {"done": [], "run_id": str(uuid.uuid4())})
    run_id = manifest.get("run_id", str(uuid.uuid4()))

    # --- Generate a stable worker_id for this process ---
    ts = time.strftime("%Y%m%d-%H%M%S")
    worker_id = f"worker-{ts}-{os.getpid()}"

    # --- Load queue ---
    all_units = _load_queue(queue_file)
    if not all_units:
        print("Queue is empty. Nothing to do.")
        return 0

    # --- Filter to pending units (idempotent — §4.1) ---
    pending = [u for u in all_units if not _is_done(u["unit_id"], manifest)]
    if not pending:
        print(f"All {len(all_units)} units already done. Queue drained.")
        return 0

    print(f"Worker {worker_id} starting: {len(pending)} pending / {len(all_units)} total")

    env = dict(os.environ)
    units_this_chunk = 0
    detected_wall = False

    for unit in pending:
        unit_id = unit["unit_id"]

        # Skip already-done (belt-and-suspenders — manifest may be fresher than pending list)
        if _is_done(unit_id, manifest):
            continue

        # --- Atomic claim (§4.3) ---
        if not _claim_unit(unit_id, lock_dir):
            print(f"  {unit_id}: already claimed by another worker, skipping.")
            continue

        # --- Rate-limit check (§13 M1) — POSITIVE signal only ---
        # In real usage: this check happens AFTER the claude -p call, by
        # inspecting its output. Here we simulate it pre-call for demo clarity.
        if _simulate_rate_limit_check(unit_id, env):
            # POSITIVE wall detected — write next-eligible, exit(2)
            print(f"  {unit_id}: rate-limit wall detected.")
            _write_next_eligible(TRACK)
            return 2  # exit code 2 = wall

        # --- Do the real work ---
        started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        t0 = time.monotonic()

        result = _do_real_work(unit)
        ok = result.get("status") == "ok"

        elapsed_s = time.monotonic() - t0

        # --- Emit one telemetry row per unit (§4.4) ---
        emit_telemetry_row(TRACK, {
            "run_id": run_id,
            "track": TRACK,
            "worker_id": worker_id,
            "unit": unit_id,
            "unit_type": "chunk",   # adjust to "chapter"/"batch"/etc. in your worker
            "started_at": started_at,
            "elapsed_s": round(elapsed_s, 3),
            "input_tokens": None,    # set from your claude -p response
            "cache_creation": None,
            "cache_read": None,
            "output_tokens": None,
            "cost_usd": None,
            "exit_reason": "ok" if ok else "crash",
            "rate_limited": False,
            "sleep_taken_s": None,
            "model": "demo",         # set from your actual model
        }, telemetry_dir=TELEMETRY_DIR)

        if not ok:
            print(f"  {unit_id}: FAILED (result={result}). Exiting with crash code.")
            return 1  # crash — longrun.sh will retry

        # --- Mark done atomically (§13 M2) ---
        manifest = _mark_done(unit_id, manifest, manifest_file)
        print(f"  {unit_id}: done in {elapsed_s:.2f}s")

        units_this_chunk += 1

        # --- Chunk boundary: exit(10) if chunk full (§4.2) ---
        if units_this_chunk >= args.chunk_size:
            remaining = len(pending) - units_this_chunk
            print(f"Chunk complete: {units_this_chunk} units done. "
                  f"~{remaining} remaining. Exiting 10 for supervisor to relaunch.")
            return 10  # more work remains

    # All units processed
    print(f"Queue fully drained ({len(all_units)} units). Exiting 0.")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="worker-template.py",
        description=(
            "Reference resumable worker (COPY-ME template). "
            "Implements §4 worker contract + §13 M-amendments. "
            "Processes fake demo units — replace _do_real_work() with your task."
        ),
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from existing manifest (idempotent — always safe to pass).",
    )
    parser.add_argument(
        "--queue",
        default=str(DEFAULT_QUEUE_FILE),
        metavar="PATH",
        help=f"Path to queue JSONL file (default: {DEFAULT_QUEUE_FILE}).",
    )
    parser.add_argument(
        "--manifest",
        default=str(DEFAULT_MANIFEST_FILE),
        metavar="PATH",
        help=f"Path to progress manifest JSON (default: {DEFAULT_MANIFEST_FILE}).",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=CHUNK_SIZE,
        metavar="N",
        help=f"Units to process per invocation before exit(10) (default: {CHUNK_SIZE}).",
    )
    return parser


if __name__ == "__main__":
    parser = _build_parser()
    args = parser.parse_args()

    exit_code = run_worker(args)
    sys.exit(exit_code)
