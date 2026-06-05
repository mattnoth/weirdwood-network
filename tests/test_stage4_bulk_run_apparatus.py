"""Tests for Stage 4 bulk-run apparatus — Pieces 1, 2 & 3.

Piece 1: --sleep-between flag on stage4-tail-classifier.py
Piece 2: --validate-every / --reject-rate-floor + drift-stop (exit 43)
Piece 3: Stop-file awareness in --sleep-between (chunked sleep, mid-sleep stop,
         between-batch stop, STOP_FILE constant exists)

No real claude -p calls are made.  All subprocess invocations are mocked.
No real sleeps are performed (time.sleep is patched where needed).
No real ~/source/claude-cwd/tmp/stage4-stop file is created — tests use a temp path
via monkeypatching tc.STOP_FILE so a leftover stop-file never affects other tests.

Run: python3 -m unittest tests.test_stage4_bulk_run_apparatus -v
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch, call

from tests._helpers import load_script

tc = load_script("stage4-tail-classifier.py")

# ---------------------------------------------------------------------------
# Shared sample vocab / tier-1 (same as existing test suite)
# ---------------------------------------------------------------------------

_SAMPLE_VOCAB = frozenset({
    "PARENT_OF", "SIBLING_OF", "SPOUSE_OF", "WARD_OF", "HOLDS_TITLE",
    "VOWS_TO", "MANIPULATES", "SWORN_TO",
    "SERVES", "LOVES", "FEARS", "KILLS", "MEMBER_OF", "TRUSTS",
    "PERCEIVED_AS", "ADVISES", "GUARDS", "BETRAYS", "TEACHES",
    "TUTORS", "PROTECTS", "COMPANION_OF", "ALLIED_WITH",
    "LOCATED_AT", "TRAVELS_WITH", "GUEST_OF",
})

_TIER1 = frozenset({
    "SIBLING_OF", "SPOUSE_OF", "PARENT_OF", "WARD_OF",
    "HOLDS_TITLE", "VOWS_TO", "MANIPULATES", "SWORN_TO",
})


def _make_tail_row(**overrides) -> dict:
    row = {
        "decision": "needs_type",
        "source_slug": "brienne-tarth",
        "target_slug": "catelyn-stark",
        "evidence_kind": "book-pass1",
        "evidence_chapter": "affc-brienne-03",
        "evidence_section": "Relationships Observed",
        "evidence_quote": "Lady Stark had been kind to her.",
        "evidence_ref": "sources/chapters/affc/affc-brienne-03.md:11",
        "hint_raw": "loyalty and gratitude",
        "corroborates_known_edge": False,
        "wiki_edge_type": None,
        "locate_status": "verbatim",
        "run_id": "pass1-derived-test",
        "schema_version": "pass1-derived-v1",
        "produced_at": "2026-05-27T00:00:00+00:00",
    }
    row.update(overrides)
    return row


def _mock_claude_response(objects: list[dict], cost: float = 0.001) -> dict:
    model_text = json.dumps(objects)
    outer = {"result": model_text, "total_cost_usd": cost}
    return {
        "returncode": 0,
        "raw_output": json.dumps(outer),
        "result_json": outer,
        "total_cost_usd": cost,
        "error_message": None,
        "duration_s": 0.5,
    }


def _process_batch_returns(emit=0, rejected=1, failed=0, needs_qualifier=0):
    """Build a minimal process_batch result dict."""
    emit_rows = [
        {
            "decision": "emit_edge",
            "edge_type": "LOVES",
            "source_slug": f"src-{i}",
            "target_slug": f"tgt-{i}",
            "evidence_chapter": "affc-brienne-03",
            "confidence_tier": 2,
            "typed_by": "haiku",
        }
        for i in range(emit)
    ]
    rejected_rows = [
        {
            "decision": "rejected",
            "source_slug": f"rsrc-{i}",
            "target_slug": f"rtgt-{i}",
            "evidence_chapter": "affc-brienne-03",
        }
        for i in range(rejected)
    ]
    return {
        "batch_idx": 0,
        "rows_in": emit + rejected + failed + needs_qualifier,
        "typed": emit,
        "rejected": rejected,
        "classify_failed": failed,
        "needs_qualifier": needs_qualifier,
        "conform_violations": 0,
        "total_cost_usd": 0.001,
        "emit_rows": emit_rows,
        "rejected_rows": rejected_rows,
        "failed_rows": [],
        "needs_qualifier_rows": [],
    }


# ===========================================================================
# Piece 1: --sleep-between flag
# ===========================================================================

class TestSleepBetweenArgDefault(unittest.TestCase):
    """--sleep-between must default to 0 (no sleep)."""

    def test_default_is_zero(self):
        # parse_args() with no extra flags
        saved = sys.argv[:]
        try:
            sys.argv = ["stage4-tail-classifier.py"]
            args = tc.parse_args()
        finally:
            sys.argv = saved
        self.assertEqual(args.sleep_between, 0)

    def test_explicit_nonzero_parses(self):
        saved = sys.argv[:]
        try:
            sys.argv = ["stage4-tail-classifier.py", "--sleep-between", "120"]
            args = tc.parse_args()
        finally:
            sys.argv = saved
        self.assertEqual(args.sleep_between, 120)

    def test_explicit_zero_parses(self):
        saved = sys.argv[:]
        try:
            sys.argv = ["stage4-tail-classifier.py", "--sleep-between", "0"]
            args = tc.parse_args()
        finally:
            sys.argv = saved
        self.assertEqual(args.sleep_between, 0)


class TestSleepBetweenBehavior(unittest.TestCase):
    """When --sleep-between > 0, time.sleep is called between (but not after) batches."""

    def setUp(self):
        # Save and restore OUT_BASE / OUT_NEEDS_QUAL_DIR to guard against
        # module-global mutation from other tests (e.g. TestOutputDirRedirect).
        self._orig_out_base = tc.OUT_BASE
        self._orig_needs_qual = tc.OUT_NEEDS_QUAL_DIR

    def tearDown(self):
        tc.OUT_BASE = self._orig_out_base
        tc.OUT_NEEDS_QUAL_DIR = self._orig_needs_qual

    def _run_main_with_sleep(
        self,
        n_batches: int,
        sleep_between: int,
        emit_per_batch: int = 0,
        rejected_per_batch: int = 1,
    ):
        """Run main() with mocked process_batch and time.sleep; return sleep call count."""
        rows = [_make_tail_row() for _ in range(n_batches)]

        import tempfile
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            out_dir.mkdir()

            saved = sys.argv[:]
            try:
                sys.argv = [
                    "stage4-tail-classifier.py",
                    "--apply",
                    "--output-dir", str(out_dir),
                    "--sleep-between", str(sleep_between),
                    "--chunk-size", "1",   # 1 row per batch = n_batches batches
                    "--flush-every", "0",
                ]

                pb_result = _process_batch_returns(
                    emit=emit_per_batch,
                    rejected=rejected_per_batch,
                )

                sleep_calls = []

                def fake_sleep(s):
                    sleep_calls.append(s)

                with patch.object(tc, "load_locked_vocab", return_value=_SAMPLE_VOCAB), \
                     patch.object(tc, "load_tier1_edge_types", return_value=_TIER1), \
                     patch.object(tc, "build_display_name_map", return_value={}), \
                     patch.object(tc, "load_tail_rows", return_value=rows), \
                     patch.object(tc, "process_batch", return_value=pb_result), \
                     patch("time.sleep", side_effect=fake_sleep):
                    tc.main()

            finally:
                sys.argv = saved

        return sleep_calls

    def test_sleep_not_called_when_zero(self):
        """Default sleep_between=0 must not call time.sleep (for batches)."""
        # Use 3 batches to make sure
        sleep_calls = self._run_main_with_sleep(n_batches=3, sleep_between=0)
        # time.sleep may be called 0 or more times for unrelated reasons, but
        # we specifically care that our sleep_between path is silent.
        # Since we patch time.sleep globally, any call here is ours.
        self.assertEqual(sleep_calls, [],
                         "sleep_between=0 must not call time.sleep")

    def test_sleep_called_n_minus_1_times(self):
        """With N batches and sleep_between>0, sleep is called exactly N-1 times."""
        n = 4
        sleep_calls = self._run_main_with_sleep(n_batches=n, sleep_between=30)
        self.assertEqual(len(sleep_calls), n - 1,
                         f"Expected {n-1} sleeps for {n} batches, got {len(sleep_calls)}")

    def test_sleep_called_with_correct_total_duration(self):
        """The total sleep time across all calls must equal (n_batches-1) * sleep_between.

        Note: sleep is now chunked (≤30s per call) for stop-file responsiveness,
        so individual calls may be <sleep_between.  The SUM across all inter-batch
        sleep calls must equal the configured duration.
        """
        n = 3
        sleep_between = 42
        sleep_calls = self._run_main_with_sleep(n_batches=n, sleep_between=sleep_between)
        total = sum(sleep_calls)
        self.assertEqual(total, (n - 1) * sleep_between,
                         f"Total sleep time must be {(n-1)*sleep_between}s; got {total}")

    def test_no_sleep_after_last_batch(self):
        """Sleep must NOT fire after the final batch.

        With 2 batches and sleep_between=99s, the inter-batch sleep is chunked
        into [30, 30, 30, 9] calls (4 chunks) for stop-file responsiveness.
        The total must equal 99s and no sleep happens for the last batch.
        """
        sleep_calls = self._run_main_with_sleep(n_batches=2, sleep_between=99)
        total = sum(sleep_calls)
        self.assertEqual(total, 99,
                         f"Total sleep between 2 batches must equal 99s; got {total}")

    def test_no_sleep_when_single_batch(self):
        """Single batch → zero sleeps regardless of sleep_between."""
        sleep_calls = self._run_main_with_sleep(n_batches=1, sleep_between=60)
        self.assertEqual(sleep_calls, [])

    def test_no_sleep_after_rate_limit_exit(self):
        """When --abort-after-consecutive-failures fires (exit 42), no sleep must occur."""
        rows = [_make_tail_row() for _ in range(3)]

        import tempfile
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            out_dir.mkdir()

            saved = sys.argv[:]
            try:
                # Reset module global so parse_args() help text doesn't crash
                tc.OUT_BASE = self._orig_out_base
                tc.OUT_NEEDS_QUAL_DIR = self._orig_needs_qual

                sys.argv = [
                    "stage4-tail-classifier.py",
                    "--apply",
                    "--output-dir", str(out_dir),
                    "--sleep-between", "60",
                    "--chunk-size", "1",
                    "--flush-every", "0",
                    "--abort-after-consecutive-failures", "1",  # immediately fire
                ]

                # Every batch fully failed → triggers rate-limit exit on first batch
                fully_failed_result = _process_batch_returns(emit=0, rejected=0, failed=1)
                sleep_calls = []

                def fake_sleep(s):
                    sleep_calls.append(s)

                with patch.object(tc, "load_locked_vocab", return_value=_SAMPLE_VOCAB), \
                     patch.object(tc, "load_tier1_edge_types", return_value=_TIER1), \
                     patch.object(tc, "build_display_name_map", return_value={}), \
                     patch.object(tc, "load_tail_rows", return_value=rows), \
                     patch.object(tc, "process_batch", return_value=fully_failed_result), \
                     patch("time.sleep", side_effect=fake_sleep):
                    rc = tc.main()

            finally:
                sys.argv = saved

        # Exit code must be 42 (rate-limit wall)
        self.assertEqual(rc, 42)
        # No inter-batch sleep should have fired (the rate-limit exit happens
        # BEFORE the sleep point in the loop)
        self.assertEqual(sleep_calls, [],
                         "No sleep should occur before a rate-limit exit")


# ===========================================================================
# Piece 2: --validate-every + drift-stop
# ===========================================================================

class TestValidateEveryArgDefault(unittest.TestCase):
    """--validate-every must default to 0 (disabled)."""

    def setUp(self):
        self._orig_out_base = tc.OUT_BASE
        self._orig_needs_qual = tc.OUT_NEEDS_QUAL_DIR

    def tearDown(self):
        tc.OUT_BASE = self._orig_out_base
        tc.OUT_NEEDS_QUAL_DIR = self._orig_needs_qual

    def test_default_is_zero(self):
        saved = sys.argv[:]
        try:
            sys.argv = ["stage4-tail-classifier.py"]
            args = tc.parse_args()
        finally:
            sys.argv = saved
        self.assertEqual(args.validate_every, 0)

    def test_explicit_value_parses(self):
        saved = sys.argv[:]
        try:
            sys.argv = ["stage4-tail-classifier.py", "--validate-every", "25"]
            args = tc.parse_args()
        finally:
            sys.argv = saved
        self.assertEqual(args.validate_every, 25)

    def test_reject_rate_floor_default(self):
        saved = sys.argv[:]
        try:
            sys.argv = ["stage4-tail-classifier.py"]
            args = tc.parse_args()
        finally:
            sys.argv = saved
        self.assertAlmostEqual(args.reject_rate_floor, 0.70)

    def test_reject_rate_floor_custom(self):
        saved = sys.argv[:]
        try:
            sys.argv = ["stage4-tail-classifier.py", "--reject-rate-floor", "0.80"]
            args = tc.parse_args()
        finally:
            sys.argv = saved
        self.assertAlmostEqual(args.reject_rate_floor, 0.80)


class TestRunDriftValidationUnit(unittest.TestCase):
    """Unit tests for the run_drift_validation() function."""

    def _make_emit_row(self, edge_type="LOVES", source="src-a", target="tgt-b"):
        return {
            "decision": "emit_edge",
            "edge_type": edge_type,
            "source_slug": source,
            "target_slug": target,
            "evidence_chapter": "affc-brienne-03",
            "confidence_tier": 2,
            "typed_by": "haiku",
        }

    def _make_rejected_row(self):
        return {
            "decision": "rejected",
            "source_slug": "x",
            "target_slug": "y",
            "evidence_chapter": "affc-brienne-03",
        }

    # ── Schema conformance ──────────────────────────────────────────────

    def test_healthy_output_passes(self):
        """Normal healthy output (high reject rate, valid schema) should pass."""
        emits = [self._make_emit_row() for _ in range(10)]
        rejecteds = [self._make_rejected_row() for _ in range(90)]
        ok, reason = tc.run_drift_validation(
            all_emit_rows=emits,
            all_rejected_rows=rejecteds,
            locked_vocab=_SAMPLE_VOCAB,
            batch_num=10,
            reject_rate_floor=0.70,
        )
        self.assertTrue(ok, f"Expected OK but got HALT: {reason}")

    def test_missing_required_field_fails(self):
        """A row missing a required field → schema_violations > 0 → HALT."""
        bad_row = self._make_emit_row()
        del bad_row["edge_type"]  # remove required field
        ok, reason = tc.run_drift_validation(
            all_emit_rows=[bad_row],
            all_rejected_rows=[self._make_rejected_row()] * 9,
            locked_vocab=_SAMPLE_VOCAB,
            batch_num=10,
            reject_rate_floor=0.70,
        )
        self.assertFalse(ok)
        self.assertIn("schema_violations", reason)

    def test_out_of_vocab_edge_type_fails(self):
        """An emit row with edge_type not in locked_vocab → OOV HALT."""
        bad_row = self._make_emit_row(edge_type="TOTALLY_MADE_UP")
        ok, reason = tc.run_drift_validation(
            all_emit_rows=[bad_row],
            all_rejected_rows=[self._make_rejected_row()] * 9,
            locked_vocab=_SAMPLE_VOCAB,
            batch_num=10,
            reject_rate_floor=0.70,
        )
        self.assertFalse(ok)
        self.assertIn("out_of_vocab", reason)

    def test_empty_source_slug_fails(self):
        """An emit row with empty source_slug → empty_endpoints > 0 → HALT."""
        bad_row = self._make_emit_row(source="")
        ok, reason = tc.run_drift_validation(
            all_emit_rows=[bad_row],
            all_rejected_rows=[self._make_rejected_row()] * 9,
            locked_vocab=_SAMPLE_VOCAB,
            batch_num=10,
            reject_rate_floor=0.70,
        )
        self.assertFalse(ok)
        self.assertIn("empty_endpoints", reason)

    def test_empty_target_slug_fails(self):
        """An emit row with empty target_slug → empty_endpoints > 0 → HALT."""
        bad_row = self._make_emit_row(target="")
        ok, reason = tc.run_drift_validation(
            all_emit_rows=[bad_row],
            all_rejected_rows=[self._make_rejected_row()] * 9,
            locked_vocab=_SAMPLE_VOCAB,
            batch_num=10,
            reject_rate_floor=0.70,
        )
        self.assertFalse(ok)
        self.assertIn("empty_endpoints", reason)

    # ── Reject-rate monitor ─────────────────────────────────────────────

    def test_low_reject_rate_fires_after_min_batches(self):
        """Reject rate below floor after >= min_batches_for_rate_check → HALT."""
        # 50% reject rate (well below 0.70 floor), 10 batches of data
        emits = [self._make_emit_row() for _ in range(50)]
        rejecteds = [self._make_rejected_row() for _ in range(50)]
        ok, reason = tc.run_drift_validation(
            all_emit_rows=emits,
            all_rejected_rows=rejecteds,
            locked_vocab=_SAMPLE_VOCAB,
            batch_num=10,
            reject_rate_floor=0.70,
        )
        self.assertFalse(ok)
        self.assertIn("reject_rate", reason)

    def test_low_reject_rate_ignored_before_min_batches(self):
        """Reject rate check is skipped before min_batches_for_rate_check (default 5)."""
        # 50% reject rate but only batch_num=3 (< 5)
        emits = [self._make_emit_row() for _ in range(5)]
        rejecteds = [self._make_rejected_row() for _ in range(5)]
        ok, reason = tc.run_drift_validation(
            all_emit_rows=emits,
            all_rejected_rows=rejecteds,
            locked_vocab=_SAMPLE_VOCAB,
            batch_num=3,  # below min_batches_for_rate_check=5
            reject_rate_floor=0.70,
        )
        self.assertTrue(ok, f"Rate check should be skipped before min_batches; got: {reason}")

    def test_high_reject_rate_passes(self):
        """Reject rate of 0.88 is above 0.70 floor → OK."""
        emits = [self._make_emit_row() for _ in range(12)]
        rejecteds = [self._make_rejected_row() for _ in range(88)]
        ok, reason = tc.run_drift_validation(
            all_emit_rows=emits,
            all_rejected_rows=rejecteds,
            locked_vocab=_SAMPLE_VOCAB,
            batch_num=10,
            reject_rate_floor=0.70,
        )
        self.assertTrue(ok, f"Expected OK for 88% reject rate, got: {reason}")

    def test_empty_output_passes(self):
        """No rows yet (both lists empty) → passes (denominator == 0, rate check skipped)."""
        ok, reason = tc.run_drift_validation(
            all_emit_rows=[],
            all_rejected_rows=[],
            locked_vocab=_SAMPLE_VOCAB,
            batch_num=10,
            reject_rate_floor=0.70,
        )
        self.assertTrue(ok, f"Empty output should pass: {reason}")

    def test_custom_floor_zero(self):
        """With floor=0.0, even 0% reject rate passes the rate check."""
        emits = [self._make_emit_row() for _ in range(100)]
        rejecteds = []  # 0% reject rate
        ok, reason = tc.run_drift_validation(
            all_emit_rows=emits,
            all_rejected_rows=rejecteds,
            locked_vocab=_SAMPLE_VOCAB,
            batch_num=10,
            reject_rate_floor=0.0,
        )
        self.assertTrue(ok, f"floor=0 should always pass rate check; got: {reason}")


class TestDriftStopExitCode(unittest.TestCase):
    """Integration: main() must exit with EXIT_CODE_DRIFT_HALT (43) when drift fires."""

    def setUp(self):
        self._orig_out_base = tc.OUT_BASE
        self._orig_needs_qual = tc.OUT_NEEDS_QUAL_DIR

    def tearDown(self):
        tc.OUT_BASE = self._orig_out_base
        tc.OUT_NEEDS_QUAL_DIR = self._orig_needs_qual

    def test_drift_halt_exit_code_is_43(self):
        """EXIT_CODE_DRIFT_HALT must equal 43."""
        self.assertEqual(tc.EXIT_CODE_DRIFT_HALT, 43)

    def test_exit_code_43_distinct_from_42(self):
        """Exit code 43 must be distinct from EXIT_CODE_RATE_LIMIT (42)."""
        self.assertNotEqual(tc.EXIT_CODE_DRIFT_HALT, tc.EXIT_CODE_RATE_LIMIT)

    def test_exit_code_43_distinct_from_130(self):
        """Exit code 43 must be distinct from EXIT_CODE_INTERRUPTED (130)."""
        self.assertNotEqual(tc.EXIT_CODE_DRIFT_HALT, tc.EXIT_CODE_INTERRUPTED)

    def test_drift_halt_fires_and_returns_43(self):
        """main() must return 43 when drift validation fires."""
        # Use 5 batches with validate_every=5 and a catastrophically low reject rate
        # (0 rejects, lots of emits → rate=0.0 < floor=0.70)
        rows = [_make_tail_row() for _ in range(5)]

        import tempfile
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            out_dir.mkdir()

            saved = sys.argv[:]
            try:
                sys.argv = [
                    "stage4-tail-classifier.py",
                    "--apply",
                    "--output-dir", str(out_dir),
                    "--chunk-size", "1",
                    "--flush-every", "5",
                    "--validate-every", "5",
                    "--reject-rate-floor", "0.70",
                    "--sleep-between", "0",
                ]

                # Every batch emits 1 row and rejects 0 → reject_rate = 0.0
                bad_result = _process_batch_returns(emit=1, rejected=0, failed=0)

                with patch.object(tc, "load_locked_vocab", return_value=_SAMPLE_VOCAB), \
                     patch.object(tc, "load_tier1_edge_types", return_value=_TIER1), \
                     patch.object(tc, "build_display_name_map", return_value={}), \
                     patch.object(tc, "load_tail_rows", return_value=rows), \
                     patch.object(tc, "process_batch", return_value=bad_result), \
                     patch("time.sleep"):
                    rc = tc.main()

            finally:
                sys.argv = saved

        self.assertEqual(rc, 43,
                         f"Expected exit code 43 (DRIFT_HALT), got {rc}")

    def test_healthy_run_does_not_fire_drift(self):
        """A healthy run (high reject rate, valid schema) must NOT fire drift halt."""
        rows = [_make_tail_row() for _ in range(5)]

        import tempfile
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            out_dir.mkdir()

            saved = sys.argv[:]
            try:
                sys.argv = [
                    "stage4-tail-classifier.py",
                    "--apply",
                    "--output-dir", str(out_dir),
                    "--chunk-size", "1",
                    "--flush-every", "5",
                    "--validate-every", "5",
                    "--reject-rate-floor", "0.70",
                    "--sleep-between", "0",
                ]

                # Healthy: 1 emit, 9 rejects per batch → ~90% reject rate
                healthy_result = _process_batch_returns(emit=1, rejected=9, failed=0)

                with patch.object(tc, "load_locked_vocab", return_value=_SAMPLE_VOCAB), \
                     patch.object(tc, "load_tier1_edge_types", return_value=_TIER1), \
                     patch.object(tc, "build_display_name_map", return_value={}), \
                     patch.object(tc, "load_tail_rows", return_value=rows), \
                     patch.object(tc, "process_batch", return_value=healthy_result), \
                     patch("time.sleep"):
                    rc = tc.main()

            finally:
                sys.argv = saved

        self.assertNotEqual(rc, 43,
                            f"Healthy run should NOT exit with 43, got {rc}")
        self.assertEqual(rc, 0, f"Healthy run should exit 0, got {rc}")

    def test_validate_every_zero_never_fires_drift(self):
        """When --validate-every 0 (default), drift validation is completely disabled."""
        rows = [_make_tail_row() for _ in range(5)]

        import tempfile
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            out_dir.mkdir()

            saved = sys.argv[:]
            try:
                sys.argv = [
                    "stage4-tail-classifier.py",
                    "--apply",
                    "--output-dir", str(out_dir),
                    "--chunk-size", "1",
                    "--flush-every", "0",
                    # --validate-every not set (defaults to 0 = disabled)
                    "--reject-rate-floor", "0.70",
                    "--sleep-between", "0",
                ]

                # Pathological: all emits, no rejects
                bad_result = _process_batch_returns(emit=1, rejected=0, failed=0)

                with patch.object(tc, "load_locked_vocab", return_value=_SAMPLE_VOCAB), \
                     patch.object(tc, "load_tier1_edge_types", return_value=_TIER1), \
                     patch.object(tc, "build_display_name_map", return_value={}), \
                     patch.object(tc, "load_tail_rows", return_value=rows), \
                     patch.object(tc, "process_batch", return_value=bad_result), \
                     patch("time.sleep"):
                    rc = tc.main()

            finally:
                sys.argv = saved

        # With validation disabled, the bad output must NOT trigger exit 43
        self.assertNotEqual(rc, 43,
                            "validate_every=0 must disable drift validation entirely")


class TestDryRunShowsNewFlags(unittest.TestCase):
    """--dry-run output must show the new flags."""

    def setUp(self):
        self._orig_out_base = tc.OUT_BASE
        self._orig_needs_qual = tc.OUT_NEEDS_QUAL_DIR

    def tearDown(self):
        tc.OUT_BASE = self._orig_out_base
        tc.OUT_NEEDS_QUAL_DIR = self._orig_needs_qual

    def test_dry_run_shows_sleep_between(self):
        """Dry-run plan must include sleep_between."""
        rows = [_make_tail_row()]
        import tempfile, io
        with tempfile.TemporaryDirectory() as td:
            saved = sys.argv[:]
            try:
                sys.argv = [
                    "stage4-tail-classifier.py",
                    "--dry-run",
                    "--sleep-between", "600",
                    "--validate-every", "25",
                ]
                captured = io.StringIO()
                with patch.object(tc, "load_locked_vocab", return_value=_SAMPLE_VOCAB), \
                     patch.object(tc, "load_tier1_edge_types", return_value=_TIER1), \
                     patch.object(tc, "build_display_name_map", return_value={}), \
                     patch.object(tc, "load_tail_rows", return_value=rows), \
                     patch("sys.stdout", captured):
                    tc.main()
            finally:
                sys.argv = saved

        out = captured.getvalue()
        self.assertIn("sleep_between", out)
        self.assertIn("validate_every", out)


# ===========================================================================
# Piece 3: Stop-file awareness in --sleep-between
# ===========================================================================

class TestStopFileConstant(unittest.TestCase):
    """STOP_FILE module constant must exist and be the expected path."""

    def test_stop_file_constant_exists(self):
        self.assertTrue(hasattr(tc, "STOP_FILE"),
                        "tc.STOP_FILE constant must be defined")

    def test_stop_file_constant_value(self):
        self.assertEqual(
            tc.STOP_FILE,
            os.path.expanduser("~/source/claude-cwd/tmp/stage4-stop"),
        )

    def test_stop_file_constant_is_string(self):
        self.assertIsInstance(tc.STOP_FILE, str)


class TestStopFileMidSleep(unittest.TestCase):
    """Stop-file detected during --sleep-between must: exit cleanly (exit 130),
    flush partial output, and leave the stop-file present (wrapper owns removal)."""

    def setUp(self):
        self._orig_out_base = tc.OUT_BASE
        self._orig_needs_qual = tc.OUT_NEEDS_QUAL_DIR
        # Create a temp dir for the fake stop file so we never touch the real stop-file path.
        self._tmp = tempfile.TemporaryDirectory()
        self._fake_stop = str(Path(self._tmp.name) / "stage4-stop")
        self._orig_stop_file = tc.STOP_FILE
        tc.STOP_FILE = self._fake_stop  # monkeypatch to temp path

    def tearDown(self):
        tc.OUT_BASE = self._orig_out_base
        tc.OUT_NEEDS_QUAL_DIR = self._orig_needs_qual
        tc.STOP_FILE = self._orig_stop_file
        self._tmp.cleanup()

    def test_stop_file_mid_sleep_exits_130(self):
        """When the stop-file appears mid-sleep, main() must return EXIT_CODE_INTERRUPTED (130)."""
        # 3 rows → 3 batches; after the first batch's sleep starts, the stop-file appears.
        rows = [_make_tail_row() for _ in range(3)]

        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            out_dir.mkdir()

            saved = sys.argv[:]
            try:
                sys.argv = [
                    "stage4-tail-classifier.py",
                    "--apply",
                    "--output-dir", str(out_dir),
                    "--sleep-between", "120",   # long enough that chunking kicks in
                    "--chunk-size", "1",         # 1 row per batch
                    "--flush-every", "0",
                ]

                pb_result = _process_batch_returns(emit=0, rejected=1, failed=0)

                sleep_calls = []
                call_count = [0]

                def fake_sleep(s):
                    sleep_calls.append(s)
                    # After the first sleep chunk fires, create the stop file.
                    # This simulates the stop file being touched mid-sleep.
                    if call_count[0] == 0:
                        Path(self._fake_stop).touch()
                    call_count[0] += 1

                with patch.object(tc, "load_locked_vocab", return_value=_SAMPLE_VOCAB), \
                     patch.object(tc, "load_tier1_edge_types", return_value=_TIER1), \
                     patch.object(tc, "build_display_name_map", return_value={}), \
                     patch.object(tc, "load_tail_rows", return_value=rows), \
                     patch.object(tc, "process_batch", return_value=pb_result), \
                     patch("time.sleep", side_effect=fake_sleep):
                    rc = tc.main()

            finally:
                sys.argv = saved

        self.assertEqual(rc, tc.EXIT_CODE_INTERRUPTED,
                         f"Stop-file mid-sleep must exit {tc.EXIT_CODE_INTERRUPTED}, got {rc}")

    def test_stop_file_mid_sleep_does_not_process_all_batches(self):
        """Once the stop-file fires mid-sleep, remaining batches must not be processed."""
        # 5 rows → 5 batches; stop fires after first sleep chunk.
        rows = [_make_tail_row() for _ in range(5)]

        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            out_dir.mkdir()

            saved = sys.argv[:]
            batches_processed = [0]
            try:
                sys.argv = [
                    "stage4-tail-classifier.py",
                    "--apply",
                    "--output-dir", str(out_dir),
                    "--sleep-between", "120",
                    "--chunk-size", "1",
                    "--flush-every", "0",
                ]

                def counting_pb(batch, **kwargs):
                    batches_processed[0] += 1
                    return _process_batch_returns(emit=0, rejected=1, failed=0)

                call_count = [0]

                def fake_sleep(s):
                    if call_count[0] == 0:
                        Path(self._fake_stop).touch()
                    call_count[0] += 1

                with patch.object(tc, "load_locked_vocab", return_value=_SAMPLE_VOCAB), \
                     patch.object(tc, "load_tier1_edge_types", return_value=_TIER1), \
                     patch.object(tc, "build_display_name_map", return_value={}), \
                     patch.object(tc, "load_tail_rows", return_value=rows), \
                     patch.object(tc, "process_batch", side_effect=counting_pb), \
                     patch("time.sleep", side_effect=fake_sleep):
                    tc.main()

            finally:
                sys.argv = saved

        self.assertLess(batches_processed[0], 5,
                        f"Not all 5 batches should run; ran {batches_processed[0]}")

    def test_stop_file_left_present_after_mid_sleep_exit(self):
        """The classifier must NOT remove the stop-file (wrapper owns removal)."""
        rows = [_make_tail_row() for _ in range(3)]

        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            out_dir.mkdir()

            saved = sys.argv[:]
            try:
                sys.argv = [
                    "stage4-tail-classifier.py",
                    "--apply",
                    "--output-dir", str(out_dir),
                    "--sleep-between", "120",
                    "--chunk-size", "1",
                    "--flush-every", "0",
                ]

                pb_result = _process_batch_returns(emit=0, rejected=1, failed=0)
                call_count = [0]

                def fake_sleep(s):
                    if call_count[0] == 0:
                        Path(self._fake_stop).touch()
                    call_count[0] += 1

                with patch.object(tc, "load_locked_vocab", return_value=_SAMPLE_VOCAB), \
                     patch.object(tc, "load_tier1_edge_types", return_value=_TIER1), \
                     patch.object(tc, "build_display_name_map", return_value={}), \
                     patch.object(tc, "load_tail_rows", return_value=rows), \
                     patch.object(tc, "process_batch", return_value=pb_result), \
                     patch("time.sleep", side_effect=fake_sleep):
                    tc.main()

            finally:
                sys.argv = saved

        self.assertTrue(Path(self._fake_stop).exists(),
                        "Stop-file must remain present after classifier exits — wrapper owns removal")

    def test_stop_file_flushes_partial_output_mid_sleep(self):
        """When the stop-file fires mid-sleep, output already accumulated must be flushed."""
        rows = [_make_tail_row() for _ in range(3)]

        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            out_dir.mkdir()

            saved = sys.argv[:]
            try:
                sys.argv = [
                    "stage4-tail-classifier.py",
                    "--apply",
                    "--output-dir", str(out_dir),
                    "--sleep-between", "120",
                    "--chunk-size", "1",
                    "--flush-every", "0",  # end-only mode; flush_delta called on stop
                ]

                # First batch produces 1 rejected row.
                pb_result = _process_batch_returns(emit=0, rejected=1, failed=0)
                call_count = [0]

                def fake_sleep(s):
                    if call_count[0] == 0:
                        Path(self._fake_stop).touch()
                    call_count[0] += 1

                with patch.object(tc, "load_locked_vocab", return_value=_SAMPLE_VOCAB), \
                     patch.object(tc, "load_tier1_edge_types", return_value=_TIER1), \
                     patch.object(tc, "build_display_name_map", return_value={}), \
                     patch.object(tc, "load_tail_rows", return_value=rows), \
                     patch.object(tc, "process_batch", return_value=pb_result), \
                     patch("time.sleep", side_effect=fake_sleep):
                    tc.main()

            finally:
                sys.argv = saved

            # At least one rejected.jsonl file must exist and have content.
            # Assertions are inside the `with` block so the tempdir is still live.
            rejected_files = list(out_dir.rglob("*.rejected.jsonl"))
            self.assertTrue(
                len(rejected_files) > 0,
                "Partial output (rejected rows) must be flushed on stop-file mid-sleep",
            )
            total_lines = sum(
                1 for f in rejected_files
                for line in f.read_text(errors="replace").splitlines()
                if line.strip()
            )
            self.assertGreater(total_lines, 0,
                               "Flushed rejected.jsonl must contain at least one row")


class TestStopFileBetweenBatches(unittest.TestCase):
    """Stop-file checked between batches (not just during sleep) must also exit cleanly."""

    def setUp(self):
        self._orig_out_base = tc.OUT_BASE
        self._orig_needs_qual = tc.OUT_NEEDS_QUAL_DIR
        self._tmp = tempfile.TemporaryDirectory()
        self._fake_stop = str(Path(self._tmp.name) / "stage4-stop")
        self._orig_stop_file = tc.STOP_FILE
        tc.STOP_FILE = self._fake_stop

    def tearDown(self):
        tc.OUT_BASE = self._orig_out_base
        tc.OUT_NEEDS_QUAL_DIR = self._orig_needs_qual
        tc.STOP_FILE = self._orig_stop_file
        self._tmp.cleanup()

    def test_stop_file_between_batches_with_sleep_zero(self):
        """With sleep_between=0, stop-file still detected between batches → exits 130."""
        # Create the stop-file BEFORE the run starts so it's detected between batches.
        Path(self._fake_stop).touch()

        rows = [_make_tail_row() for _ in range(3)]

        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            out_dir.mkdir()

            saved = sys.argv[:]
            batches_processed = [0]
            try:
                sys.argv = [
                    "stage4-tail-classifier.py",
                    "--apply",
                    "--output-dir", str(out_dir),
                    "--sleep-between", "0",   # no sleep — tests the between-batch check
                    "--chunk-size", "1",
                    "--flush-every", "0",
                ]

                def counting_pb(batch, **kwargs):
                    batches_processed[0] += 1
                    return _process_batch_returns(emit=0, rejected=1, failed=0)

                with patch.object(tc, "load_locked_vocab", return_value=_SAMPLE_VOCAB), \
                     patch.object(tc, "load_tier1_edge_types", return_value=_TIER1), \
                     patch.object(tc, "build_display_name_map", return_value={}), \
                     patch.object(tc, "load_tail_rows", return_value=rows), \
                     patch.object(tc, "process_batch", side_effect=counting_pb):
                    rc = tc.main()

            finally:
                sys.argv = saved

        # Must exit with EXIT_CODE_INTERRUPTED and not process all 3 batches.
        self.assertEqual(rc, tc.EXIT_CODE_INTERRUPTED,
                         f"Between-batch stop-file must exit {tc.EXIT_CODE_INTERRUPTED}, got {rc}")
        self.assertLess(batches_processed[0], 3,
                        f"Not all batches should run with stop-file present; ran {batches_processed[0]}")

    def test_stop_file_created_after_first_batch_stops_cleanly(self):
        """Stop-file created after the first batch completes stops before the second batch."""
        rows = [_make_tail_row() for _ in range(4)]

        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            out_dir.mkdir()

            saved = sys.argv[:]
            batches_processed = [0]
            fake_stop = self._fake_stop
            try:
                sys.argv = [
                    "stage4-tail-classifier.py",
                    "--apply",
                    "--output-dir", str(out_dir),
                    "--sleep-between", "0",
                    "--chunk-size", "1",
                    "--flush-every", "0",
                ]

                def counting_pb(batch, **kwargs):
                    count = batches_processed[0]
                    batches_processed[0] += 1
                    # After the first batch, touch the stop file.
                    if count == 0:
                        Path(fake_stop).touch()
                    return _process_batch_returns(emit=0, rejected=1, failed=0)

                with patch.object(tc, "load_locked_vocab", return_value=_SAMPLE_VOCAB), \
                     patch.object(tc, "load_tier1_edge_types", return_value=_TIER1), \
                     patch.object(tc, "build_display_name_map", return_value={}), \
                     patch.object(tc, "load_tail_rows", return_value=rows), \
                     patch.object(tc, "process_batch", side_effect=counting_pb):
                    rc = tc.main()

            finally:
                sys.argv = saved

        # Should stop after batch 1 (or at most batch 2) — not run all 4.
        self.assertLess(batches_processed[0], 4,
                        f"Should have stopped early; ran {batches_processed[0]} batches")
        self.assertEqual(rc, tc.EXIT_CODE_INTERRUPTED,
                         f"Expected exit {tc.EXIT_CODE_INTERRUPTED}, got {rc}")

    def test_stop_file_left_present_after_between_batch_exit(self):
        """Classifier must NOT remove the stop-file when exiting via between-batch check."""
        Path(self._fake_stop).touch()

        rows = [_make_tail_row() for _ in range(2)]

        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            out_dir.mkdir()

            saved = sys.argv[:]
            try:
                sys.argv = [
                    "stage4-tail-classifier.py",
                    "--apply",
                    "--output-dir", str(out_dir),
                    "--sleep-between", "0",
                    "--chunk-size", "1",
                    "--flush-every", "0",
                ]

                pb_result = _process_batch_returns(emit=0, rejected=1, failed=0)

                with patch.object(tc, "load_locked_vocab", return_value=_SAMPLE_VOCAB), \
                     patch.object(tc, "load_tier1_edge_types", return_value=_TIER1), \
                     patch.object(tc, "build_display_name_map", return_value={}), \
                     patch.object(tc, "load_tail_rows", return_value=rows), \
                     patch.object(tc, "process_batch", return_value=pb_result):
                    tc.main()

            finally:
                sys.argv = saved

        self.assertTrue(Path(self._fake_stop).exists(),
                        "Stop-file must remain present after between-batch exit — wrapper owns removal")


class TestSleepBetweenChunkedBehavior(unittest.TestCase):
    """sleep_between sleep is chunked (≤30s steps) so it can be interrupted promptly."""

    def setUp(self):
        self._orig_out_base = tc.OUT_BASE
        self._orig_needs_qual = tc.OUT_NEEDS_QUAL_DIR
        self._tmp = tempfile.TemporaryDirectory()
        self._fake_stop = str(Path(self._tmp.name) / "stage4-stop")
        self._orig_stop_file = tc.STOP_FILE
        tc.STOP_FILE = self._fake_stop

    def tearDown(self):
        tc.OUT_BASE = self._orig_out_base
        tc.OUT_NEEDS_QUAL_DIR = self._orig_needs_qual
        tc.STOP_FILE = self._orig_stop_file
        self._tmp.cleanup()

    def test_sleep_between_uses_chunks_not_one_big_sleep(self):
        """With sleep_between=120 and 2 batches, time.sleep must be called with ≤30s each call."""
        rows = [_make_tail_row() for _ in range(2)]

        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            out_dir.mkdir()

            saved = sys.argv[:]
            sleep_durations = []
            try:
                sys.argv = [
                    "stage4-tail-classifier.py",
                    "--apply",
                    "--output-dir", str(out_dir),
                    "--sleep-between", "120",  # should be split into ≥4 x 30s chunks
                    "--chunk-size", "1",
                    "--flush-every", "0",
                ]

                pb_result = _process_batch_returns(emit=0, rejected=1, failed=0)

                def fake_sleep(s):
                    sleep_durations.append(s)

                with patch.object(tc, "load_locked_vocab", return_value=_SAMPLE_VOCAB), \
                     patch.object(tc, "load_tier1_edge_types", return_value=_TIER1), \
                     patch.object(tc, "build_display_name_map", return_value={}), \
                     patch.object(tc, "load_tail_rows", return_value=rows), \
                     patch.object(tc, "process_batch", return_value=pb_result), \
                     patch("time.sleep", side_effect=fake_sleep):
                    tc.main()

            finally:
                sys.argv = saved

        # Each individual sleep call must be ≤30s.
        self.assertTrue(len(sleep_durations) > 0,
                        "sleep_between=120 should produce at least one time.sleep call")
        for dur in sleep_durations:
            self.assertLessEqual(dur, 30,
                                 f"Each sleep chunk must be ≤30s, got {dur}")

    def test_sleep_between_chunks_sum_to_full_duration_when_no_stop(self):
        """Without a stop-file, all chunks must sum to approximately sleep_between."""
        rows = [_make_tail_row() for _ in range(2)]

        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            out_dir.mkdir()

            saved = sys.argv[:]
            sleep_durations = []
            try:
                sys.argv = [
                    "stage4-tail-classifier.py",
                    "--apply",
                    "--output-dir", str(out_dir),
                    "--sleep-between", "90",
                    "--chunk-size", "1",
                    "--flush-every", "0",
                ]

                pb_result = _process_batch_returns(emit=0, rejected=1, failed=0)

                def fake_sleep(s):
                    sleep_durations.append(s)

                with patch.object(tc, "load_locked_vocab", return_value=_SAMPLE_VOCAB), \
                     patch.object(tc, "load_tier1_edge_types", return_value=_TIER1), \
                     patch.object(tc, "build_display_name_map", return_value={}), \
                     patch.object(tc, "load_tail_rows", return_value=rows), \
                     patch.object(tc, "process_batch", return_value=pb_result), \
                     patch("time.sleep", side_effect=fake_sleep):
                    tc.main()

            finally:
                sys.argv = saved

        total = sum(sleep_durations)
        self.assertEqual(total, 90,
                         f"All chunks should sum to sleep_between=90s; got {total}")


if __name__ == "__main__":
    unittest.main()
