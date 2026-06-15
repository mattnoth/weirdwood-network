#!/usr/bin/env python3
"""pace.py — Telemetry ledger + pacer for Weirwood Network long-run jobs.

Ingests historical stats from heterogeneous CSV/JSONL/JSON sources, normalises
them to a single canonical ledger schema, and reports per-track baselines so
you can set LONGRUN_SLEEP_BETWEEN from data rather than guessing.

SUBCOMMANDS
-----------
  backfill [--dry-run]
      Scan all known stats files, normalise to the ledger schema, dedup, and
      write per-track JSONL to working/telemetry/<track>.jsonl.
      Idempotent: rewrites from scratch on each call.

  report [--track NAME]
      Read working/telemetry/*.jsonl, group by (track, model, unit_type),
      print median baselines, a conservative recommended LONGRUN_SLEEP_BETWEEN,
      and an honest wall-cadence note (v1 — wall data is thin).

IMPORTABLE HELPER
-----------------
  emit_telemetry_row(track, row_dict, telemetry_dir=None)
      Append one atomic JSONL line to working/telemetry/<track>.jsonl.
      Called by workers after each unit completes.

LEDGER SCHEMA (canonical row keys)
-----------------------------------
  run_id            str   — optional; backfill rows use the source filename
  track             str   — e.g. "pass1-agot", "wiki-pass2-core", "stage4-haiku"
  worker_id         str   — e.g. "worker-20260514-193254-9043"
  unit              str   — chapter slug, batch id, chunk id, bucket name
  unit_type         str   — "chapter" | "bucket" | "batch" | "chunk"
  started_at        str   — ISO-8601 or "YYYY-MM-DD HH:MM:SS" (stored as-is)
  elapsed_s         float — wall seconds for this unit
  input_tokens      int   — null if unknown
  cache_creation    int   — null if unknown
  cache_read        int   — null if unknown
  output_tokens     int   — null if unknown
  cost_usd          float — null if unknown
  exit_reason       str   — "ok" | "wall" | "crash" | null
  rate_limited      bool  — null if unknown (Pass-1 CSVs have no such column)
  sleep_taken_s     float — null if not recorded
  model             str   — e.g. "claude-opus", "claude-sonnet", "claude-haiku"

Design notes:
  - Per §12 of the design doc: one JSONL file per track under working/telemetry/
    (avoids unbounded growth + concurrent-append contention).
  - Per §13 M3: wall-cadence data is thin at backfill time (~4 events across 2
    missions, none in Pass-1). v1 reports baselines + conservative default sleep.
    Genuine wall-cadence prediction waits for live rows.
  - emit_telemetry_row() single-line append is POSIX-atomic for small lines.
  - For multi-byte state files (progress manifests) workers MUST use
    write-to-tmp-then-rename (see worker-template.py).
"""

import argparse
import csv
import json
import os
import statistics
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
TELEMETRY_DIR = PROJECT_ROOT / "working" / "telemetry"
STATS_DIR = PROJECT_ROOT / "working" / "extraction-stats"
MISSIONS_DIR = PROJECT_ROOT / "working" / "missions"

# ---------------------------------------------------------------------------
# Canonical ledger schema — keys in output order
# ---------------------------------------------------------------------------
LEDGER_KEYS = [
    "run_id",
    "track",
    "worker_id",
    "unit",
    "unit_type",
    "started_at",
    "elapsed_s",
    "input_tokens",
    "cache_creation",
    "cache_read",
    "output_tokens",
    "cost_usd",
    "exit_reason",
    "rate_limited",
    "sleep_taken_s",
    "model",
]

# unit_type values (§13 S6)
VALID_UNIT_TYPES = {"chapter", "bucket", "batch", "chunk"}

# Statuses that represent a real completed unit with timing data
COMPLETED_STATUSES = {"ok", "done"}


# ---------------------------------------------------------------------------
# Public helper — called by workers
# ---------------------------------------------------------------------------

def emit_telemetry_row(track: str, row_dict: dict, telemetry_dir: Path | None = None) -> None:
    """Append one atomic JSONL line to working/telemetry/<track>.jsonl.

    Workers call this after each unit completes. Single-line json.dumps + "\\n"
    append is POSIX-atomic for lines under ~4KB — safe for concurrent workers
    writing different lines (each is one atomic write syscall).

    Args:
        track:         Track name, e.g. "pass1-agot".
        row_dict:      Dict with ledger keys. Missing keys are silently omitted.
        telemetry_dir: Override for the telemetry directory (default:
                       working/telemetry/ relative to this script's repo root).
    """
    if telemetry_dir is None:
        telemetry_dir = TELEMETRY_DIR
    telemetry_dir = Path(telemetry_dir)
    telemetry_dir.mkdir(parents=True, exist_ok=True)

    out_path = telemetry_dir / f"{track}.jsonl"
    # Normalise: keep only known ledger keys, preserve None as null
    row = {k: row_dict.get(k) for k in LEDGER_KEYS if k in row_dict or k in ("track",)}
    row["track"] = track  # always stamp the track

    line = json.dumps(row, default=str) + "\n"
    with open(out_path, "a") as fh:
        fh.write(line)


# ---------------------------------------------------------------------------
# Backfill normaliser helpers
# ---------------------------------------------------------------------------

def _int_or_none(val):
    """Convert to int, returning None for empty/null/whitespace."""
    if val is None:
        return None
    s = str(val).strip()
    if not s or s.lower() in ("null", "none", ""):
        return None
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return None


def _float_or_none(val):
    """Convert to float, returning None for empty/null/whitespace."""
    if val is None:
        return None
    s = str(val).strip()
    if not s or s.lower() in ("null", "none", ""):
        return None
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def _exit_reason_from_status(status: str) -> str | None:
    """Map CSV status string to ledger exit_reason."""
    s = status.strip().lower()
    if s in ("ok", "done", "skipped-done", "skip-done"):
        return "ok"
    if s in ("fail", "failed-error", "failed-stale"):
        return "crash"
    if s in ("skip-rate-limit",):
        return "wall"
    return None


def _has_timing(row: dict) -> bool:
    """Return True if this row has a non-empty, non-zero duration."""
    dur = str(row.get("duration_s", "")).strip()
    if not dur:
        return False
    try:
        return float(dur) > 0
    except ValueError:
        return False


def _make_ledger_row(**kwargs) -> dict:
    """Build a canonical ledger row, filling missing keys with None."""
    return {k: kwargs.get(k) for k in LEDGER_KEYS}


# ---------------------------------------------------------------------------
# Input schema (a): Pass-1 CSV 13-col  (agot, asos, affc)
# Input schema (b): Pass-1 CSV 16-col  (acok, ADWD)
# Both handled by the same function since we use csv.DictReader.
# ---------------------------------------------------------------------------

def _normalise_pass1_csv(path: Path, track: str, run_id: str) -> tuple[list[dict], dict]:
    """Normalise a Pass-1 per-chapter CSV to ledger rows.

    Returns (rows, stats) where stats = {
        "rows_in", "rows_kept", "rows_dropped_status", "rows_deduped"
    }.
    """
    rows_in: list[dict] = []
    with open(path, newline="") as fh:
        rows_in = list(csv.DictReader(fh))

    rows_dropped_status = 0
    candidates: list[dict] = []

    for row in rows_in:
        status = row.get("status", "").strip().lower()
        if status not in COMPLETED_STATUSES:
            rows_dropped_status += 1
            continue
        if not _has_timing(row):
            rows_dropped_status += 1
            continue

        ledger = _make_ledger_row(
            run_id=run_id,
            track=track,
            worker_id=None,
            unit=row.get("chapter", "").strip(),
            unit_type="chapter",
            started_at=row.get("start_time", "").strip() or None,
            elapsed_s=_float_or_none(row.get("duration_s")),
            input_tokens=_int_or_none(row.get("input_tokens")),
            # header drift: CSV uses "cache_creation_tokens", ledger uses "cache_creation"
            cache_creation=_int_or_none(row.get("cache_creation_tokens")),
            cache_read=_int_or_none(row.get("cache_read_tokens")),
            output_tokens=_int_or_none(row.get("output_tokens")),
            cost_usd=_float_or_none(row.get("cost_usd")),
            exit_reason=_exit_reason_from_status(status),
            rate_limited=None,   # §13 M3: Pass-1 CSVs have no rate_limited column
            sleep_taken_s=None,
            model="claude-opus",  # project fact: all Pass-1 was Opus
        )
        candidates.append(ledger)

    # Dedup: key = (track, unit); keep the row with larger elapsed_s.
    # This catches the acok-davos-02 race (6s placeholder vs 247s real row)
    # and any other multi-terminal append races.
    seen: dict[tuple, dict] = {}
    rows_deduped = 0
    for r in candidates:
        key = (r["track"], r["unit"])
        if key in seen:
            existing_elapsed = seen[key].get("elapsed_s") or 0
            new_elapsed = r.get("elapsed_s") or 0
            if new_elapsed > existing_elapsed:
                seen[key] = r
            rows_deduped += 1
        else:
            seen[key] = r

    kept = list(seen.values())
    return kept, {
        "rows_in": len(rows_in),
        "rows_kept": len(kept),
        "rows_dropped_status": rows_dropped_status,
        "rows_deduped": rows_deduped,
    }


# ---------------------------------------------------------------------------
# Input schema (c): wiki-pass2 CSV
# ---------------------------------------------------------------------------

def _normalise_wiki_pass2_csv(path: Path, tier: str, run_id: str) -> tuple[list[dict], dict]:
    """Normalise a wiki-pass2 per-bucket CSV to ledger rows."""
    track = f"wiki-pass2-{tier}"
    rows_in: list[dict] = []
    with open(path, newline="") as fh:
        rows_in = list(csv.DictReader(fh))

    rows_dropped_status = 0
    candidates: list[dict] = []

    for row in rows_in:
        status = row.get("status", "").strip().lower()
        if status not in COMPLETED_STATUSES:
            rows_dropped_status += 1
            continue
        if not _has_timing(row):
            rows_dropped_status += 1
            continue

        ledger = _make_ledger_row(
            run_id=run_id,
            track=track,
            worker_id=None,
            unit=row.get("bucket", "").strip(),
            unit_type="bucket",
            started_at=row.get("start_time", "").strip() or None,
            elapsed_s=_float_or_none(row.get("duration_s")),
            input_tokens=_int_or_none(row.get("input_tokens")),
            cache_creation=_int_or_none(row.get("cache_creation_tokens")),
            cache_read=_int_or_none(row.get("cache_read_tokens")),
            output_tokens=_int_or_none(row.get("output_tokens")),
            cost_usd=_float_or_none(row.get("cost_usd")),
            exit_reason=_exit_reason_from_status(status),
            rate_limited=None,
            sleep_taken_s=None,
            model="claude-opus",  # Pass-2 Stage 1 was Opus
        )
        candidates.append(ledger)

    # Dedup by (track, unit) — keep larger elapsed
    seen: dict[tuple, dict] = {}
    rows_deduped = 0
    for r in candidates:
        key = (r["track"], r["unit"])
        if key in seen:
            existing_elapsed = seen[key].get("elapsed_s") or 0
            new_elapsed = r.get("elapsed_s") or 0
            if new_elapsed > existing_elapsed:
                seen[key] = r
            rows_deduped += 1
        else:
            seen[key] = r

    kept = list(seen.values())
    return kept, {
        "rows_in": len(rows_in),
        "rows_kept": len(kept),
        "rows_dropped_status": rows_dropped_status,
        "rows_deduped": rows_deduped,
    }


# ---------------------------------------------------------------------------
# Input schema (d): Stage-4 timing.jsonl (per-batch rows)
# ---------------------------------------------------------------------------

def _normalise_timing_jsonl(path: Path, mission_dir: str, run_id: str) -> tuple[list[dict], dict]:
    """Normalise a Stage-4 timing.jsonl to ledger rows.

    The mission dir name (e.g. "2026-05-14-stage4-v1-bulk-sonnet") becomes the
    track with leading date stripped: "stage4-v1-bulk-sonnet".
    Model is "claude-sonnet" for this mission (hardcoded — the data predates the
    model field).
    """
    # Strip leading date (YYYY-MM-DD-)
    parts = mission_dir.split("-", 3)
    if len(parts) >= 4 and parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
        track = parts[3]
    else:
        track = mission_dir

    # Model inference from track name
    if "haiku" in track.lower():
        model = "claude-haiku"
    elif "sonnet" in track.lower():
        model = "claude-sonnet"
    else:
        model = "claude-opus"

    rows_in = 0
    rows_dropped_status = 0
    candidates: list[dict] = []

    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows_in += 1
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                rows_dropped_status += 1
                continue

            elapsed = _float_or_none(obj.get("elapsed_s"))
            if elapsed is None or elapsed <= 0:
                rows_dropped_status += 1
                continue

            claude_exit = obj.get("claude_exit")
            if claude_exit == 0:
                exit_reason = "ok"
            elif claude_exit == 2:
                exit_reason = "wall"
            elif claude_exit is None:
                exit_reason = None
            else:
                exit_reason = "crash"

            ledger = _make_ledger_row(
                run_id=run_id,
                track=track,
                worker_id=obj.get("worker_id"),
                unit=obj.get("batch_id"),
                unit_type="batch",
                started_at=obj.get("started_at"),
                elapsed_s=elapsed,
                input_tokens=_int_or_none(obj.get("input_tokens")),
                cache_creation=_int_or_none(obj.get("cache_creation")),
                cache_read=_int_or_none(obj.get("cache_read")),
                output_tokens=_int_or_none(obj.get("output_tokens")),
                cost_usd=_float_or_none(obj.get("cost_usd")),
                exit_reason=exit_reason,
                rate_limited=None,
                sleep_taken_s=None,
                model=model,
            )
            candidates.append(ledger)

    # Dedup by (track, unit, worker_id) — timing.jsonl is per-worker so same
    # batch_id can appear from multiple workers; keep the largest elapsed.
    seen: dict[tuple, dict] = {}
    rows_deduped = 0
    for r in candidates:
        # batch_id is not unique across workers — key includes worker_id
        key = (r["track"], r["unit"], r.get("worker_id"))
        if key in seen:
            existing_elapsed = seen[key].get("elapsed_s") or 0
            new_elapsed = r.get("elapsed_s") or 0
            if new_elapsed > existing_elapsed:
                seen[key] = r
            rows_deduped += 1
        else:
            seen[key] = r

    kept = list(seen.values())
    return kept, {
        "rows_in": rows_in,
        "rows_kept": len(kept),
        "rows_dropped_status": rows_dropped_status,
        "rows_deduped": rows_deduped,
    }


# ---------------------------------------------------------------------------
# Input schema (e): run-summary.json (chunk_timings array)
# ---------------------------------------------------------------------------

def _normalise_run_summary(path: Path, mission_dir: str, run_id: str) -> tuple[list[dict], dict]:
    """Normalise a run-summary.json chunk_timings array to ledger rows.

    Emits ONE ledger row per entry in chunk_timings. Token fields are null
    (chunk timings don't carry per-chunk token counts).
    """
    parts = mission_dir.split("-", 3)
    if len(parts) >= 4 and parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
        track = parts[3]
    else:
        track = mission_dir

    with open(path) as fh:
        summary = json.load(fh)

    model_raw = summary.get("model", "")
    if "haiku" in model_raw.lower():
        model = "claude-haiku"
    elif "sonnet" in model_raw.lower():
        model = "claude-sonnet"
    elif "opus" in model_raw.lower():
        model = "claude-opus"
    else:
        model = model_raw or None

    chunk_timings = summary.get("chunk_timings", [])
    rows_in = len(chunk_timings)
    rows_dropped_status = 0
    candidates: list[dict] = []

    for chunk in chunk_timings:
        elapsed = _float_or_none(chunk.get("duration_s"))
        if elapsed is None or elapsed <= 0:
            rows_dropped_status += 1
            continue

        rate_limited = chunk.get("rate_limited")
        if isinstance(rate_limited, bool):
            pass  # keep as-is
        else:
            rate_limited = None

        ledger = _make_ledger_row(
            run_id=run_id,
            track=track,
            worker_id=None,
            unit=chunk.get("chunk_id"),
            unit_type="chunk",
            started_at=None,
            elapsed_s=elapsed,
            input_tokens=None,
            cache_creation=None,
            cache_read=None,
            output_tokens=None,
            cost_usd=_float_or_none(chunk.get("cost_usd")),
            exit_reason="ok" if not rate_limited else "wall",
            rate_limited=rate_limited,
            sleep_taken_s=None,
            model=model,
        )
        candidates.append(ledger)

    # Dedup by (track, unit)
    seen: dict[tuple, dict] = {}
    rows_deduped = 0
    for r in candidates:
        key = (r["track"], r["unit"])
        if key in seen:
            existing_elapsed = seen[key].get("elapsed_s") or 0
            new_elapsed = r.get("elapsed_s") or 0
            if new_elapsed > existing_elapsed:
                seen[key] = r
            rows_deduped += 1
        else:
            seen[key] = r

    kept = list(seen.values())
    return kept, {
        "rows_in": rows_in,
        "rows_kept": len(kept),
        "rows_dropped_status": rows_dropped_status,
        "rows_deduped": rows_deduped,
    }


# ---------------------------------------------------------------------------
# Rate-limit events — wall events, NOT work rows
# ---------------------------------------------------------------------------

def _load_rate_limit_events(path: Path, mission_dir: str) -> list[dict]:
    """Load rate-limit-events.jsonl as wall events (NOT emitted as ledger rows).

    Returns list of raw event dicts, augmented with 'track' field.
    """
    parts = mission_dir.split("-", 3)
    if len(parts) >= 4 and parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
        track = parts[3]
    else:
        track = mission_dir

    events = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                obj["track"] = track
                events.append(obj)
            except json.JSONDecodeError:
                pass
    return events


# ---------------------------------------------------------------------------
# Wall events writer (per-track .walls.jsonl sidecar)
# ---------------------------------------------------------------------------

def _write_wall_sidecar(track: str, events: list[dict], telemetry_dir: Path) -> None:
    """Write rate-limit wall events to working/telemetry/<track>.walls.jsonl."""
    if not events:
        return
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    wall_path = telemetry_dir / f"{track}.walls.jsonl"
    with open(wall_path, "w") as fh:
        for ev in events:
            fh.write(json.dumps(ev, default=str) + "\n")


# ---------------------------------------------------------------------------
# Backfill — main logic
# ---------------------------------------------------------------------------

def cmd_backfill(dry_run: bool = False) -> None:
    """Ingest all known stats files, normalise, dedup, write per-track JSONL."""

    print(f"Backfill {'[DRY RUN] ' if dry_run else ''}— scanning source files …")
    print()

    all_rows: dict[str, list[dict]] = {}   # track → rows
    all_wall_events: dict[str, list[dict]] = {}  # track → wall events
    total_stats: dict[str, dict] = {}  # source label → stats dict

    def _accumulate(track: str, rows: list[dict], label: str, stats: dict) -> None:
        all_rows.setdefault(track, []).extend(rows)
        total_stats[label] = stats

    # ---- (a)+(b) Pass-1 CSVs ----
    pass1_books = [
        ("extraction-stats-agot-pass1-v3.csv", "agot"),
        ("extraction-stats-asos-pass1-v3.csv", "asos"),
        ("extraction-stats-affc-pass1-v3.csv", "affc"),
        ("extraction-stats-acok-pass1-v3.csv", "acok"),
        ("extraction-stats-ADWD-pass1-v3.csv", "adwd"),
    ]
    for fname, book in pass1_books:
        path = STATS_DIR / fname
        if not path.exists():
            path = STATS_DIR / "_archive" / fname   # frozen CSVs archived once Pass 1 completed (344/344)
        if not path.exists():
            print(f"  SKIP (not found): {path}")
            continue
        track = f"pass1-{book}"
        rows, stats = _normalise_pass1_csv(path, track, run_id=fname)
        _accumulate(track, rows, fname, stats)
        print(f"  {fname}: in={stats['rows_in']}  kept={stats['rows_kept']}"
              f"  dropped={stats['rows_dropped_status']}  deduped={stats['rows_deduped']}")

    # ---- (c) wiki-pass2 CSVs ----
    wiki_files = [
        ("wiki-pass2-stats-core-v1.csv", "core"),
        ("wiki-pass2-stats-secondary-v1.csv", "secondary"),
    ]
    for fname, tier in wiki_files:
        path = STATS_DIR / fname
        if not path.exists():
            path = STATS_DIR / "_archive" / fname   # frozen CSVs archived once Pass 2 completed
        if not path.exists():
            print(f"  SKIP (not found): {path}")
            continue
        rows, stats = _normalise_wiki_pass2_csv(path, tier, run_id=fname)
        track = f"wiki-pass2-{tier}"
        _accumulate(track, rows, fname, stats)
        print(f"  {fname}: in={stats['rows_in']}  kept={stats['rows_kept']}"
              f"  dropped={stats['rows_dropped_status']}  deduped={stats['rows_deduped']}")

    # ---- (d) timing.jsonl from mission dirs ----
    # ---- (e) run-summary.json from mission dirs ----
    # ---- (f) rate-limit-events.jsonl from mission dirs ----
    if MISSIONS_DIR.exists():
        for mission_dir in sorted(MISSIONS_DIR.iterdir()):
            if not mission_dir.is_dir():
                continue
            dir_name = mission_dir.name

            timing_path = mission_dir / "timing.jsonl"
            if timing_path.exists():
                rows, stats = _normalise_timing_jsonl(timing_path, dir_name, run_id=dir_name)
                # Derive track name same way as normaliser
                parts = dir_name.split("-", 3)
                track = parts[3] if (len(parts) >= 4 and parts[0].isdigit()) else dir_name
                _accumulate(track, rows, f"{dir_name}/timing.jsonl", stats)
                print(f"  {dir_name}/timing.jsonl: in={stats['rows_in']}"
                      f"  kept={stats['rows_kept']}"
                      f"  dropped={stats['rows_dropped_status']}"
                      f"  deduped={stats['rows_deduped']}")

            summary_path = mission_dir / "run-summary.json"
            if summary_path.exists():
                rows, stats = _normalise_run_summary(summary_path, dir_name, run_id=dir_name)
                parts = dir_name.split("-", 3)
                track = parts[3] if (len(parts) >= 4 and parts[0].isdigit()) else dir_name
                _accumulate(track, rows, f"{dir_name}/run-summary.json", stats)
                print(f"  {dir_name}/run-summary.json: in={stats['rows_in']}"
                      f"  kept={stats['rows_kept']}"
                      f"  dropped={stats['rows_dropped_status']}"
                      f"  deduped={stats['rows_deduped']}")

            wall_path = mission_dir / "rate-limit-events.jsonl"
            if wall_path.exists():
                parts = dir_name.split("-", 3)
                track = parts[3] if (len(parts) >= 4 and parts[0].isdigit()) else dir_name
                events = _load_rate_limit_events(wall_path, dir_name)
                all_wall_events.setdefault(track, []).extend(events)
                print(f"  {dir_name}/rate-limit-events.jsonl: {len(events)} wall events"
                      f"  (stored in <track>.walls.jsonl, NOT as work rows)")

    print()

    # ---- Write ledger files ----
    if not dry_run:
        TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)

    total_rows_written = 0
    per_track_counts: dict[str, int] = {}

    for track, rows in sorted(all_rows.items()):
        per_track_counts[track] = len(rows)
        total_rows_written += len(rows)
        if not dry_run:
            out_path = TELEMETRY_DIR / f"{track}.jsonl"
            with open(out_path, "w") as fh:
                for row in rows:
                    fh.write(json.dumps(row, default=str) + "\n")

    # Write wall event sidecars
    if not dry_run:
        for track, events in all_wall_events.items():
            _write_wall_sidecar(track, events, TELEMETRY_DIR)

    # ---- Summary ----
    total_in = sum(s["rows_in"] for s in total_stats.values())
    total_kept = sum(s["rows_kept"] for s in total_stats.values())
    total_dropped = sum(s["rows_dropped_status"] for s in total_stats.values())
    total_deduped = sum(s["rows_deduped"] for s in total_stats.values())

    print("=" * 60)
    print(f"BACKFILL SUMMARY {'(DRY RUN)' if dry_run else ''}")
    print("=" * 60)
    print(f"  Sources processed : {len(total_stats)}")
    print(f"  Rows in           : {total_in}")
    print(f"  Rows kept         : {total_kept}")
    print(f"  Rows dropped      : {total_dropped}  (failed-stale / no timing)")
    print(f"  Rows deduped      : {total_deduped}  (kept larger-elapsed winner)")
    print()
    print("  Per-track counts:")
    for track, count in sorted(per_track_counts.items()):
        print(f"    {track:<35}  {count:>4} rows")
    print()
    if dry_run:
        print("  [DRY RUN] No files written.")
    else:
        print(f"  Output directory  : {TELEMETRY_DIR}")
        print(f"  Total rows written: {total_rows_written}")


# ---------------------------------------------------------------------------
# Report — read ledger, compute baselines, print table
# ---------------------------------------------------------------------------

def _median(vals: list) -> float | None:
    """Return median of a list, filtering None/NaN."""
    clean = [v for v in vals if v is not None]
    if not clean:
        return None
    return statistics.median(clean)


def cmd_report(track_filter: str | None = None) -> None:
    """Read telemetry JSONL files and print per-(track, model, unit_type) baselines."""

    if not TELEMETRY_DIR.exists():
        print("No telemetry directory found. Run `pace.py backfill` first.")
        sys.exit(1)

    # Load all rows
    by_group: dict[tuple, list[dict]] = {}  # (track, model, unit_type) → rows
    wall_counts: dict[str, int] = {}  # track → count of wall events

    jsonl_files = sorted(TELEMETRY_DIR.glob("*.jsonl"))
    if not jsonl_files:
        print("No telemetry JSONL files found. Run `pace.py backfill` first.")
        sys.exit(1)

    for jf in jsonl_files:
        # Skip wall sidecars
        if jf.name.endswith(".walls.jsonl"):
            # Count wall events per track
            track_name = jf.stem.replace(".walls", "")
            count = sum(1 for line in open(jf) if line.strip())
            wall_counts[track_name] = count
            continue

        track_name = jf.stem
        if track_filter and track_name != track_filter:
            continue

        with open(jf) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue

                track = row.get("track") or track_name
                model = row.get("model") or "unknown"
                unit_type = row.get("unit_type") or "unknown"
                group = (track, model, unit_type)
                by_group.setdefault(group, []).append(row)

    if not by_group:
        print("No rows loaded (check --track filter or re-run backfill).")
        sys.exit(1)

    # Also load wall event counts from .walls.jsonl files
    for jf in TELEMETRY_DIR.glob("*.walls.jsonl"):
        track_name = jf.stem.replace(".walls", "")
        if track_filter and track_name != track_filter:
            continue
        count = sum(1 for line in open(jf) if line.strip())
        wall_counts[track_name] = wall_counts.get(track_name, 0) + count

    # Compute and print table
    print()
    print("=" * 90)
    print(f"{'WEIRWOOD TELEMETRY BASELINES':^90}")
    print("=" * 90)
    hdr = f"{'Track':<30} {'Model':<16} {'Type':<8} {'N':>4}  {'Med elap(s)':>11}  {'Med $':>8}  {'Med out_tok':>11}"
    print(hdr)
    print("-" * 90)

    # Sort groups for stable output
    conservative_sleep_candidates: list[float] = []

    for group in sorted(by_group.keys()):
        track, model, unit_type = group
        rows = by_group[group]

        elapsed_vals = [r.get("elapsed_s") for r in rows]
        cost_vals = [r.get("cost_usd") for r in rows]
        out_tok_vals = [r.get("output_tokens") for r in rows]

        med_elapsed = _median(elapsed_vals)
        med_cost = _median(cost_vals)
        med_out_tok = _median(out_tok_vals)

        elapsed_str = f"{med_elapsed:>11.0f}" if med_elapsed is not None else f"{'—':>11}"
        cost_str = f"{med_cost:>8.4f}" if med_cost is not None else f"{'—':>8}"
        outtok_str = f"{med_out_tok:>11.0f}" if med_out_tok is not None else f"{'—':>11}"

        print(f"{track:<30} {model:<16} {unit_type:<8} {len(rows):>4}  {elapsed_str}  {cost_str}  {outtok_str}")

        # Collect elapsed values for sleep recommendation (chapters only)
        if unit_type == "chapter" and med_elapsed is not None:
            conservative_sleep_candidates.append(med_elapsed)

    print("-" * 90)
    print()

    # ---- Recommended sleep (§12, §13 M3) ----
    # Conservative = 2× median chapter duration, floored at 600s.
    # v1 does NOT use wall-cadence (data too thin — M3).
    print("RECOMMENDED LONGRUN_SLEEP_BETWEEN")
    print("-" * 40)
    if conservative_sleep_candidates:
        overall_median_elapsed = statistics.median(conservative_sleep_candidates)
        recommended = max(600, int(overall_median_elapsed * 2))
        print(f"  Median chapter elapsed (across all tracks): {overall_median_elapsed:.0f}s")
        print(f"  Conservative recommended sleep            : {recommended}s"
              f"  (2× median, min 600s)")
        print(f"  Set via: LONGRUN_SLEEP_BETWEEN={recommended} weirwood run start <track>")
    else:
        print("  No chapter-level timing data available.")
        print("  Recommended default: LONGRUN_SLEEP_BETWEEN=1200  (20 minutes, project default)")
    print()

    # ---- Honest wall-cadence note (§13 M3) ----
    print("WALL-CADENCE NOTE (v1 — data is thin)")
    print("-" * 40)
    total_wall_events = sum(wall_counts.values())
    if total_wall_events:
        print(f"  Rate-limit wall events in ledger: {total_wall_events} across {len(wall_counts)} track(s).")
        for t, cnt in sorted(wall_counts.items()):
            print(f"    {t}: {cnt} wall event(s)")
    else:
        print("  No wall events found in ledger.")
    print()
    print("  IMPORTANT: v1 does not compute wall-cadence prediction. The wall-event")
    print("  dataset is too thin (~4-8 events; Pass-1 CSVs carry no rate_limited column).")
    print("  Recommended sleep is derived from unit duration only — a conservative")
    print("  heuristic, not a data-driven cadence estimate. Wall-cadence prediction")
    print("  will be added once live workers accumulate sufficient telemetry rows.")
    print()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pace.py",
        description="Weirwood telemetry ledger + pacer. Ingests stats files, reports baselines.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_backfill = sub.add_parser(
        "backfill",
        help="Ingest all existing stats files and write per-track telemetry JSONL.",
    )
    p_backfill.add_argument(
        "--dry-run",
        action="store_true",
        help="Normalise and report but do not write any files.",
    )

    p_report = sub.add_parser(
        "report",
        help="Print per-(track, model, unit_type) baselines from the telemetry ledger.",
    )
    p_report.add_argument(
        "--track",
        metavar="NAME",
        help="Only report on this track (e.g. pass1-agot).",
    )

    return parser


if __name__ == "__main__":
    parser = _build_parser()
    args = parser.parse_args()

    if args.cmd == "backfill":
        cmd_backfill(dry_run=args.dry_run)
    elif args.cmd == "report":
        cmd_report(track_filter=args.track)
    else:
        parser.print_help()
        sys.exit(1)
