"""Tests for scripts/pace.py — telemetry ledger normaliser + pacer.

Covers:
  - Each of the 6 input schemas → correct canonical ledger rows + correct
    unit_type / track / model.
  - failed-stale / empty-timing rows are dropped.
  - (track, unit) dedup keeps the larger-elapsed row.
  - Header-drift mapping (cache_creation_tokens→cache_creation, duration_s→elapsed_s).
  - Baseline median computation returns correct value for a known set.
  - emit_telemetry_row() writes one atomic JSONL line.
  - Backfill writes per-track files to working/telemetry/.

All tests are hermetic — no network, no live graph mutations.
Real stats files are only read in the integration test marked explicitly.
"""

import csv
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# ---------------------------------------------------------------------------
# Load pace.py via importlib (hyphenated-file convention for this repo)
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"


def _load_pace():
    spec = importlib.util.spec_from_file_location("pace", SCRIPTS_DIR / "pace.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_pace = _load_pace()

# Re-export the functions under test
_normalise_pass1_csv = _pace._normalise_pass1_csv
_normalise_wiki_pass2_csv = _pace._normalise_wiki_pass2_csv
_normalise_timing_jsonl = _pace._normalise_timing_jsonl
_normalise_run_summary = _pace._normalise_run_summary
_load_rate_limit_events = _pace._load_rate_limit_events
emit_telemetry_row = _pace.emit_telemetry_row
LEDGER_KEYS = _pace.LEDGER_KEYS
_median = _pace._median


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)


# Common 13-col Pass-1 fieldnames (schema a)
PASS1_13_FIELDS = [
    "chapter", "book", "wave", "status", "start_time", "end_time",
    "duration_s", "input_tokens", "cache_creation_tokens",
    "cache_read_tokens", "output_tokens", "total_tokens", "cost_usd",
]

# Common 16-col Pass-1 fieldnames (schema b)
PASS1_16_FIELDS = PASS1_13_FIELDS + ["last_heartbeat", "terminal_id", "retry_at"]

WIKI_PASS2_FIELDS = [
    "bucket", "tier", "wave", "status", "start_time", "end_time",
    "duration_s", "input_tokens", "cache_creation_tokens",
    "cache_read_tokens", "output_tokens", "total_tokens", "cost_usd",
    "pages_in_bucket", "nodes_emitted", "validation_status", "notes",
    "questions_filed", "conflicts_filed", "pass1_contradictions_filed",
]

# A minimal "good" Pass-1 row dict
def _good_pass1_row(chapter="agot-bran-01", book="agot", status="ok",
                    duration_s="247", output_tokens="10131", cost_usd="0.50",
                    cache_creation_tokens="29353", cache_read_tokens="104310"):
    return {
        "chapter": chapter,
        "book": book,
        "wave": "1",
        "status": status,
        "start_time": "2026-04-24 00:15:23",
        "end_time": "2026-04-24 00:19:10",
        "duration_s": duration_s,
        "input_tokens": "3666",
        "cache_creation_tokens": cache_creation_tokens,
        "cache_read_tokens": cache_read_tokens,
        "output_tokens": output_tokens,
        "total_tokens": "147460",
        "cost_usd": cost_usd,
    }


# ---------------------------------------------------------------------------
# Schema (a): Pass-1 CSV 13-col
# ---------------------------------------------------------------------------

class TestNormalisePass1CSV13Col(unittest.TestCase):
    def test_basic_ok_row(self):
        """A single ok row with timing produces one ledger row."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test.csv"
            _write_csv(path, [_good_pass1_row()], PASS1_13_FIELDS)
            rows, stats = _normalise_pass1_csv(path, "pass1-agot", "test.csv")

        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(r["unit"], "agot-bran-01")
        self.assertEqual(r["unit_type"], "chapter")
        self.assertEqual(r["track"], "pass1-agot")
        self.assertEqual(r["model"], "claude-opus")
        self.assertEqual(r["elapsed_s"], 247.0)
        self.assertEqual(r["exit_reason"], "ok")
        # rate_limited is null for Pass-1 (§13 M3)
        self.assertIsNone(r["rate_limited"])

    def test_header_drift_cache_creation_tokens(self):
        """CSV 'cache_creation_tokens' maps to ledger 'cache_creation'."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test.csv"
            row = _good_pass1_row(cache_creation_tokens="12345")
            _write_csv(path, [row], PASS1_13_FIELDS)
            rows, _ = _normalise_pass1_csv(path, "pass1-agot", "test.csv")

        self.assertEqual(rows[0]["cache_creation"], 12345)
        # There must NOT be a "cache_creation_tokens" key
        self.assertNotIn("cache_creation_tokens", rows[0])

    def test_header_drift_duration_s_maps_to_elapsed_s(self):
        """CSV 'duration_s' maps to ledger 'elapsed_s'."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test.csv"
            _write_csv(path, [_good_pass1_row(duration_s="300")], PASS1_13_FIELDS)
            rows, _ = _normalise_pass1_csv(path, "pass1-agot", "test.csv")

        self.assertEqual(rows[0]["elapsed_s"], 300.0)
        # There must NOT be a "duration_s" key
        self.assertNotIn("duration_s", rows[0])

    def test_failed_stale_dropped(self):
        """Rows with status=failed-stale are dropped."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test.csv"
            rows_in = [
                _good_pass1_row(chapter="agot-bran-01", status="ok"),
                _good_pass1_row(chapter="agot-bran-02", status="failed-stale", duration_s=""),
                _good_pass1_row(chapter="agot-bran-03", status="failed-stale", duration_s="0"),
            ]
            _write_csv(path, rows_in, PASS1_13_FIELDS)
            rows, stats = _normalise_pass1_csv(path, "pass1-agot", "test.csv")

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["unit"], "agot-bran-01")
        self.assertEqual(stats["rows_dropped_status"], 2)

    def test_empty_timing_dropped(self):
        """Rows with empty duration_s are dropped even if status=ok."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test.csv"
            row = _good_pass1_row(duration_s="")
            _write_csv(path, [row], PASS1_13_FIELDS)
            rows, stats = _normalise_pass1_csv(path, "pass1-agot", "test.csv")

        self.assertEqual(len(rows), 0)
        self.assertEqual(stats["rows_dropped_status"], 1)

    def test_zero_timing_dropped(self):
        """Rows with duration_s=0 are dropped (no real work done)."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test.csv"
            row = _good_pass1_row(duration_s="0", output_tokens="0")
            _write_csv(path, [row], PASS1_13_FIELDS)
            rows, stats = _normalise_pass1_csv(path, "pass1-agot", "test.csv")

        self.assertEqual(len(rows), 0)

    def test_done_status_accepted(self):
        """status=done is treated the same as ok."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test.csv"
            _write_csv(path, [_good_pass1_row(status="done")], PASS1_13_FIELDS)
            rows, _ = _normalise_pass1_csv(path, "pass1-agot", "test.csv")

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["exit_reason"], "ok")


# ---------------------------------------------------------------------------
# Schema (b): Pass-1 CSV 16-col — same normaliser, just extra columns
# ---------------------------------------------------------------------------

class TestNormalisePass1CSV16Col(unittest.TestCase):
    def test_extra_columns_ignored(self):
        """16-col CSV (acok/ADWD) processes cleanly; extra cols don't appear in ledger."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test.csv"
            row = {**_good_pass1_row(status="done"), "last_heartbeat": "", "terminal_id": "T1", "retry_at": ""}
            _write_csv(path, [row], PASS1_16_FIELDS)
            rows, _ = _normalise_pass1_csv(path, "pass1-acok", "test.csv")

        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertNotIn("last_heartbeat", r)
        self.assertNotIn("terminal_id", r)
        self.assertEqual(r["unit_type"], "chapter")
        self.assertEqual(r["track"], "pass1-acok")


# ---------------------------------------------------------------------------
# Dedup: (track, unit) — keep larger elapsed_s
# ---------------------------------------------------------------------------

class TestDedupLargerElapsed(unittest.TestCase):
    def test_acok_davos02_race_kept_larger(self):
        """Dedup keeps the row with larger elapsed_s (the real work row)."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test.csv"
            rows_in = [
                _good_pass1_row(chapter="acok-davos-02", status="ok", duration_s="6",
                                output_tokens="0"),
                _good_pass1_row(chapter="acok-davos-02", status="ok", duration_s="247",
                                output_tokens="10131"),
            ]
            _write_csv(path, rows_in, PASS1_13_FIELDS)
            rows, stats = _normalise_pass1_csv(path, "pass1-acok", "test.csv")

        self.assertEqual(len(rows), 1, "Dedup should collapse 2 rows to 1")
        self.assertEqual(rows[0]["elapsed_s"], 247.0, "Should keep the 247s real row")
        self.assertEqual(stats["rows_deduped"], 1)

    def test_dedup_three_rows_keeps_largest(self):
        """When 3 rows share the same (track, unit), the largest elapsed wins."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test.csv"
            rows_in = [
                _good_pass1_row(chapter="agot-ned-01", status="ok", duration_s="50"),
                _good_pass1_row(chapter="agot-ned-01", status="ok", duration_s="300"),
                _good_pass1_row(chapter="agot-ned-01", status="ok", duration_s="100"),
            ]
            _write_csv(path, rows_in, PASS1_13_FIELDS)
            rows, stats = _normalise_pass1_csv(path, "pass1-agot", "test.csv")

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["elapsed_s"], 300.0)
        self.assertEqual(stats["rows_deduped"], 2)

    def test_different_units_not_deduped(self):
        """Different units are not collapsed."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test.csv"
            rows_in = [
                _good_pass1_row(chapter="agot-bran-01", status="ok", duration_s="200"),
                _good_pass1_row(chapter="agot-bran-02", status="ok", duration_s="250"),
            ]
            _write_csv(path, rows_in, PASS1_13_FIELDS)
            rows, stats = _normalise_pass1_csv(path, "pass1-agot", "test.csv")

        self.assertEqual(len(rows), 2)
        self.assertEqual(stats["rows_deduped"], 0)


# ---------------------------------------------------------------------------
# Schema (c): wiki-pass2 CSV
# ---------------------------------------------------------------------------

class TestNormaliseWikiPass2CSV(unittest.TestCase):
    def _good_wiki_row(self, bucket="direwolves", tier="core", status="ok",
                       duration_s="285"):
        return {
            "bucket": bucket, "tier": tier, "wave": "1", "status": status,
            "start_time": "2026-04-26 19:59:20", "end_time": "2026-04-26 20:04:05",
            "duration_s": duration_s, "input_tokens": "19",
            "cache_creation_tokens": "69049", "cache_read_tokens": "783304",
            "output_tokens": "13126", "total_tokens": "865498", "cost_usd": "1.152",
            "pages_in_bucket": "6", "nodes_emitted": "6", "validation_status": "pass",
            "notes": "", "questions_filed": "1", "conflicts_filed": "0",
            "pass1_contradictions_filed": "0",
        }

    def test_basic_ok_row(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "wiki.csv"
            _write_csv(path, [self._good_wiki_row()], WIKI_PASS2_FIELDS)
            rows, stats = _normalise_wiki_pass2_csv(path, "core", "wiki.csv")

        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(r["unit"], "direwolves")
        self.assertEqual(r["unit_type"], "bucket")
        self.assertEqual(r["track"], "wiki-pass2-core")
        self.assertEqual(r["model"], "claude-opus")
        self.assertEqual(r["elapsed_s"], 285.0)
        self.assertEqual(r["cache_creation"], 69049)
        self.assertEqual(r["cache_read"], 783304)

    def test_skip_rate_limit_dropped(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "wiki.csv"
            rows_in = [
                self._good_wiki_row(bucket="a", status="ok"),
                self._good_wiki_row(bucket="b", status="skip-rate-limit", duration_s=""),
            ]
            _write_csv(path, rows_in, WIKI_PASS2_FIELDS)
            rows, stats = _normalise_wiki_pass2_csv(path, "core", "wiki.csv")

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["unit"], "a")

    def test_secondary_tier_track_name(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "wiki.csv"
            _write_csv(path, [self._good_wiki_row(tier="secondary")], WIKI_PASS2_FIELDS)
            rows, _ = _normalise_wiki_pass2_csv(path, "secondary", "wiki.csv")

        self.assertEqual(rows[0]["track"], "wiki-pass2-secondary")


# ---------------------------------------------------------------------------
# Schema (d): Stage-4 timing.jsonl
# ---------------------------------------------------------------------------

class TestNormaliseTimingJsonl(unittest.TestCase):
    def _good_timing_row(self, batch_id="batch-0006", worker_id="worker-123",
                         elapsed_s=2004, output_tokens=106755, claude_exit=0):
        return {
            "batch_id": batch_id,
            "worker_id": worker_id,
            "started_at": "2026-05-15T00:32:54Z",
            "elapsed_s": elapsed_s,
            "input_tokens": 3702,
            "cache_creation": 533157,
            "cache_read": 2907759,
            "output_tokens": output_tokens,
            "cost_usd": 4.86,
            "claude_exit": claude_exit,
        }

    def _write_jsonl(self, path, rows):
        with open(path, "w") as fh:
            for r in rows:
                fh.write(json.dumps(r) + "\n")

    def test_basic_timing_row(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "timing.jsonl"
            self._write_jsonl(path, [self._good_timing_row()])
            rows, stats = _normalise_timing_jsonl(path, "2026-05-14-stage4-v1-bulk-sonnet", "run-id")

        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(r["unit"], "batch-0006")
        self.assertEqual(r["unit_type"], "batch")
        self.assertEqual(r["track"], "stage4-v1-bulk-sonnet")
        self.assertEqual(r["model"], "claude-sonnet")
        self.assertEqual(r["elapsed_s"], 2004.0)
        self.assertEqual(r["exit_reason"], "ok")
        self.assertEqual(r["cache_creation"], 533157)
        self.assertEqual(r["cache_read"], 2907759)

    def test_model_inferred_from_dir_name_haiku(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "timing.jsonl"
            self._write_jsonl(path, [self._good_timing_row()])
            rows, _ = _normalise_timing_jsonl(path, "2026-05-19-stage4-haiku", "run-id")

        self.assertEqual(rows[0]["model"], "claude-haiku")

    def test_nonzero_claude_exit_mapped_to_crash(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "timing.jsonl"
            self._write_jsonl(path, [self._good_timing_row(claude_exit=1)])
            rows, _ = _normalise_timing_jsonl(path, "2026-05-14-stage4-v1-bulk-sonnet", "run-id")

        self.assertEqual(rows[0]["exit_reason"], "crash")

    def test_zero_elapsed_dropped(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "timing.jsonl"
            self._write_jsonl(path, [self._good_timing_row(elapsed_s=0)])
            rows, stats = _normalise_timing_jsonl(path, "2026-05-14-stage4-v1-bulk-sonnet", "run-id")

        self.assertEqual(len(rows), 0)
        self.assertEqual(stats["rows_dropped_status"], 1)

    def test_mission_dir_without_date_prefix(self):
        """Mission dirs without YYYY-MM-DD prefix use the whole name as track."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "timing.jsonl"
            self._write_jsonl(path, [self._good_timing_row()])
            rows, _ = _normalise_timing_jsonl(path, "my-custom-track", "run-id")

        self.assertEqual(rows[0]["track"], "my-custom-track")


# ---------------------------------------------------------------------------
# Schema (e): run-summary.json chunk_timings
# ---------------------------------------------------------------------------

class TestNormaliseRunSummary(unittest.TestCase):
    def _good_summary(self, model="claude-haiku-20240307", n_chunks=3,
                      rate_limited=False):
        return {
            "run_completed_at": "2026-05-22T08:00:00Z",
            "model": model,
            "concurrency": 5,
            "chunk_size": 5,
            "chunk_timings": [
                {
                    "chunk_id": f"batch-{i:04d}-chunk-00",
                    "chunk_idx": i,
                    "duration_s": 157.34 + i,
                    "cost_usd": 0.45 + i * 0.01,
                    "files_done": 5,
                    "files_failed": 0,
                    "rate_limited": rate_limited,
                }
                for i in range(n_chunks)
            ],
        }

    def test_basic_summary(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "run-summary.json"
            path.write_text(json.dumps(self._good_summary()))
            rows, stats = _normalise_run_summary(path, "2026-05-19-stage4-haiku", "run-id")

        self.assertEqual(len(rows), 3)
        self.assertEqual(stats["rows_in"], 3)
        r = rows[0]
        self.assertEqual(r["unit_type"], "chunk")
        self.assertEqual(r["track"], "stage4-haiku")
        self.assertEqual(r["model"], "claude-haiku")
        self.assertEqual(r["unit"], "batch-0000-chunk-00")
        self.assertAlmostEqual(r["elapsed_s"], 157.34, places=2)
        # Token fields are null for chunk timings
        self.assertIsNone(r["input_tokens"])
        self.assertIsNone(r["output_tokens"])

    def test_rate_limited_chunk(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "run-summary.json"
            path.write_text(json.dumps(self._good_summary(rate_limited=True, n_chunks=1)))
            rows, _ = _normalise_run_summary(path, "2026-05-19-stage4-haiku", "run-id")

        self.assertTrue(rows[0]["rate_limited"])
        self.assertEqual(rows[0]["exit_reason"], "wall")

    def test_model_haiku_normalised(self):
        """Long model string containing 'haiku' normalises to 'claude-haiku'."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "run-summary.json"
            path.write_text(json.dumps(self._good_summary(model="claude-haiku-20240307")))
            rows, _ = _normalise_run_summary(path, "2026-05-19-stage4-haiku", "run-id")

        self.assertEqual(rows[0]["model"], "claude-haiku")


# ---------------------------------------------------------------------------
# Schema (f): rate-limit-events.jsonl — NOT emitted as work rows
# ---------------------------------------------------------------------------

class TestLoadRateLimitEvents(unittest.TestCase):
    def test_events_loaded_with_track(self):
        events_data = [
            {
                "worker_id": "worker-123", "batch_id": "batch-0020",
                "detected_at": "2026-05-16T20:45:27Z",
                "rate_limit_type": "five_hour", "resets_at_ts": "1778967000",
                "reset_info": "five_hour limit", "cumulative_elapsed_s": 2102,
                "cumulative_cost_usd": 5.60,
            }
        ]
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "rate-limit-events.jsonl"
            with open(path, "w") as fh:
                for e in events_data:
                    fh.write(json.dumps(e) + "\n")
            events = _load_rate_limit_events(path, "2026-05-14-stage4-v1-bulk-sonnet")

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["track"], "stage4-v1-bulk-sonnet")
        self.assertIn("detected_at", events[0])

    def test_events_are_not_ledger_rows(self):
        """Rate-limit events must NOT have ledger unit_type etc."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "rate-limit-events.jsonl"
            path.write_text(json.dumps({"worker_id": "w1", "batch_id": "b1"}) + "\n")
            events = _load_rate_limit_events(path, "2026-05-14-stage4-v1-bulk-sonnet")

        # They're raw dicts with extra 'track' field, not normalised ledger rows
        self.assertNotIn("unit_type", events[0])
        self.assertNotIn("elapsed_s", events[0])


# ---------------------------------------------------------------------------
# Baseline median computation
# ---------------------------------------------------------------------------

class TestMedianComputation(unittest.TestCase):
    def test_median_odd_count(self):
        vals = [100.0, 200.0, 300.0, 400.0, 500.0]
        self.assertEqual(_median(vals), 300.0)

    def test_median_even_count(self):
        vals = [100.0, 200.0, 300.0, 400.0]
        self.assertEqual(_median(vals), 250.0)

    def test_median_filters_none(self):
        vals = [None, 100.0, None, 300.0, None]
        self.assertEqual(_median(vals), 200.0)

    def test_median_all_none_returns_none(self):
        self.assertIsNone(_median([None, None]))

    def test_median_empty_returns_none(self):
        self.assertIsNone(_median([]))

    def test_median_single_value(self):
        self.assertEqual(_median([42.0]), 42.0)


# ---------------------------------------------------------------------------
# emit_telemetry_row — atomic append
# ---------------------------------------------------------------------------

class TestEmitTelemetryRow(unittest.TestCase):
    def test_emits_jsonl_line(self):
        with tempfile.TemporaryDirectory() as td:
            tel_dir = Path(td) / "telemetry"
            emit_telemetry_row("test-track", {
                "unit": "agot-bran-01",
                "unit_type": "chapter",
                "elapsed_s": 247.0,
                "model": "claude-opus",
            }, telemetry_dir=tel_dir)

            out = tel_dir / "test-track.jsonl"
            self.assertTrue(out.exists())
            lines = [l for l in out.read_text().splitlines() if l.strip()]
            self.assertEqual(len(lines), 1)
            row = json.loads(lines[0])
            self.assertEqual(row["track"], "test-track")
            self.assertEqual(row["unit"], "agot-bran-01")
            self.assertEqual(row["elapsed_s"], 247.0)

    def test_emits_multiple_rows_appended(self):
        with tempfile.TemporaryDirectory() as td:
            tel_dir = Path(td) / "telemetry"
            for i in range(5):
                emit_telemetry_row("test-track", {"unit": f"unit-{i}", "elapsed_s": float(i * 10)},
                                   telemetry_dir=tel_dir)

            out = tel_dir / "test-track.jsonl"
            lines = [l for l in out.read_text().splitlines() if l.strip()]
            self.assertEqual(len(lines), 5)

    def test_creates_dir_if_missing(self):
        with tempfile.TemporaryDirectory() as td:
            tel_dir = Path(td) / "deep" / "nested" / "telemetry"
            self.assertFalse(tel_dir.exists())
            emit_telemetry_row("x", {"unit": "u1"}, telemetry_dir=tel_dir)
            self.assertTrue(tel_dir.exists())

    def test_unknown_keys_not_in_output(self):
        """emit_telemetry_row only writes known LEDGER_KEYS."""
        with tempfile.TemporaryDirectory() as td:
            tel_dir = Path(td) / "telemetry"
            emit_telemetry_row("track", {"unit": "u1", "UNKNOWN_KEY": "oops"},
                               telemetry_dir=tel_dir)
            out = tel_dir / "track.jsonl"
            row = json.loads(out.read_text().strip())
            self.assertNotIn("UNKNOWN_KEY", row)


# ---------------------------------------------------------------------------
# Ledger schema contract
# ---------------------------------------------------------------------------

class TestLedgerSchema(unittest.TestCase):
    def test_ledger_keys_contains_unit_type(self):
        """unit_type must be in LEDGER_KEYS (§13 S6)."""
        self.assertIn("unit_type", LEDGER_KEYS)

    def test_ledger_keys_contains_rate_limited(self):
        """rate_limited must be in LEDGER_KEYS (§13 M1)."""
        self.assertIn("rate_limited", LEDGER_KEYS)

    def test_ledger_keys_contains_model(self):
        self.assertIn("model", LEDGER_KEYS)

    def test_pass1_rows_have_all_ledger_keys(self):
        """Every normalised Pass-1 row contains all LEDGER_KEYS (value may be None)."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test.csv"
            _write_csv(path, [_good_pass1_row()], PASS1_13_FIELDS)
            rows, _ = _normalise_pass1_csv(path, "pass1-agot", "test.csv")

        r = rows[0]
        for k in LEDGER_KEYS:
            self.assertIn(k, r, f"Missing ledger key: {k}")


# ---------------------------------------------------------------------------
# Integration: backfill against real stats files (read-only)
# ---------------------------------------------------------------------------

class TestBackfillIntegration(unittest.TestCase):
    """Run backfill against the real stats files and verify key expectations.

    These tests are read-only — they do NOT write to working/telemetry/.
    They use a temp directory as the output target.
    """

    def test_backfill_produces_per_track_files(self):
        """Backfill creates at least one JSONL file per known Pass-1 book."""
        stats_dir = REPO_ROOT / "working" / "extraction-stats"
        if not (stats_dir / "extraction-stats-agot-pass1-v3.csv").exists():
            self.skipTest("Real stats files not present")

        import io
        from contextlib import redirect_stdout

        with tempfile.TemporaryDirectory() as td:
            tel_dir = Path(td) / "telemetry"
            # Monkey-patch TELEMETRY_DIR and STATS_DIR for this test
            original_tel = _pace.TELEMETRY_DIR
            original_stats = _pace.STATS_DIR
            original_missions = _pace.MISSIONS_DIR
            _pace.TELEMETRY_DIR = tel_dir
            _pace.STATS_DIR = stats_dir
            _pace.MISSIONS_DIR = REPO_ROOT / "working" / "missions"
            try:
                f = io.StringIO()
                with redirect_stdout(f):
                    _pace.cmd_backfill(dry_run=False)
                output = f.getvalue()
            finally:
                _pace.TELEMETRY_DIR = original_tel
                _pace.STATS_DIR = original_stats
                _pace.MISSIONS_DIR = original_missions

            jsonl_files = list(tel_dir.glob("*.jsonl"))
            self.assertGreater(len(jsonl_files), 0, "Expected at least one JSONL file")

            # Check that per-book files exist
            track_names = {f.stem for f in jsonl_files}
            self.assertIn("pass1-agot", track_names)

    def test_acok_dedup_removes_failed_stale(self):
        """The real acok CSV's many failed-stale rows are all dropped."""
        acok_path = REPO_ROOT / "working" / "extraction-stats" / "extraction-stats-acok-pass1-v3.csv"
        if not acok_path.exists():
            self.skipTest("Real acok CSV not present")

        rows, stats = _normalise_pass1_csv(acok_path, "pass1-acok", "acok.csv")

        # All kept rows must have elapsed_s > 0
        for r in rows:
            self.assertIsNotNone(r["elapsed_s"])
            self.assertGreater(r["elapsed_s"], 0)

        # Every kept unit is unique
        units = [r["unit"] for r in rows]
        self.assertEqual(len(units), len(set(units)), "Duplicate units after dedup")

        # There should be substantially more dropped than kept (the CSV is very noisy)
        self.assertGreater(stats["rows_dropped_status"], stats["rows_kept"])


if __name__ == "__main__":
    unittest.main()
