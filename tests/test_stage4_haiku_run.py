"""Tests for scripts/stage4-haiku-run.py — pure-Python orchestrator functions.

Excludes anything that calls `claude` (subprocess.run, invoke_haiku, run_chunk,
run_batch). Those are tested only by live runs.

Run: python3 -m unittest tests.test_stage4_haiku_run -v
"""

import json
import unittest
from pathlib import Path

from tests._helpers import load_script

runner = load_script("stage4-haiku-run.py")


class TestCandidateToHaikuOutput(unittest.TestCase):
    """Verify path routing for the three candidate shapes."""

    def test_source_target_shape(self):
        out = runner.candidate_to_haiku_output(
            "working/wiki/pass2-buckets/battles-a-b/prose-edge-candidates/battle-at-acorn-hall.candidates.jsonl"
        )
        self.assertTrue(str(out).endswith(
            "working/wiki/pass2-buckets/battles-a-b/prose-edges-haiku/battle-at-acorn-hall.edges.jsonl"
        ))

    def test_comention_shape(self):
        out = runner.candidate_to_haiku_output(
            "working/wiki/pass2-buckets/meta-chapters-agot/comention-candidates/agot-bran-01.candidates.jsonl"
        )
        self.assertTrue(str(out).endswith(
            "working/wiki/pass2-buckets/meta-chapters-agot/prose-edges-haiku/agot-bran-01.comention-edges.jsonl"
        ))

    def test_pass1_relationship_shape(self):
        out = runner.candidate_to_haiku_output(
            "working/wiki/pass2-buckets/extractions-pass1/agot/agot-bran-01.candidates.jsonl"
        )
        self.assertTrue(str(out).endswith(
            "working/wiki/pass2-buckets/extractions-pass1/agot/prose-edges-haiku/agot-bran-01.pass1-edges.jsonl"
        ))

    def test_malformed_path_raises(self):
        with self.assertRaises(ValueError):
            runner.candidate_to_haiku_output("too/short/path.jsonl")


class TestPlanBatchChunks(unittest.TestCase):
    """Verify chunking math + (after LEVER 2 fix) skip-existing-output filtering."""

    def _batch_row(self, n_files: int) -> dict:
        return {
            "batch_id": "batch-test",
            "shape": "source_target",
            "files": [
                f"working/wiki/pass2-buckets/test-bucket/prose-edge-candidates/file-{i:03d}.candidates.jsonl"
                for i in range(n_files)
            ],
        }

    def test_exact_multiple(self):
        chunks, warnings = runner.plan_batch_chunks(self._batch_row(9), chunk_size=3)
        self.assertEqual(len(chunks), 3)
        self.assertEqual(all(len(c) == 3 for c in chunks), True)
        self.assertEqual(warnings, [])

    def test_uneven_last_chunk(self):
        chunks, _ = runner.plan_batch_chunks(self._batch_row(7), chunk_size=3)
        self.assertEqual(len(chunks), 3)
        self.assertEqual([len(c) for c in chunks], [3, 3, 1])

    def test_chunk_size_larger_than_files(self):
        chunks, _ = runner.plan_batch_chunks(self._batch_row(3), chunk_size=10)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(len(chunks[0]), 3)

    def test_chunk_size_one(self):
        chunks, _ = runner.plan_batch_chunks(self._batch_row(5), chunk_size=1)
        self.assertEqual(len(chunks), 5)

    def test_empty_files(self):
        chunks, warnings = runner.plan_batch_chunks(
            {"batch_id": "b", "shape": "source_target", "files": []}, chunk_size=3
        )
        self.assertEqual(chunks, [])
        self.assertEqual(warnings, [])

    def test_unroutable_paths_warn_and_skip(self):
        row = {
            "batch_id": "b",
            "shape": "source_target",
            "files": [
                "working/wiki/pass2-buckets/ok-bucket/prose-edge-candidates/file-1.candidates.jsonl",
                "too/short/bad.jsonl",  # raises ValueError
                "working/wiki/pass2-buckets/ok-bucket/prose-edge-candidates/file-2.candidates.jsonl",
            ],
        }
        chunks, warnings = runner.plan_batch_chunks(row, chunk_size=3)
        # 2 valid files → 1 chunk of 2
        self.assertEqual(sum(len(c) for c in chunks), 2)
        self.assertEqual(len(warnings), 1)
        self.assertIn("Unexpected candidate path", warnings[0])


class TestPlanBatchChunksSkipExisting(unittest.TestCase):
    """LEVER 2 fix: when re-running a partially-completed batch after a
    rate-limit reset, the orchestrator should skip files whose .edges.jsonl
    output already exists. Saves tokens on the 12/30 done files of batch-0013
    when batch-0013 gets re-run."""

    def test_skip_existing_filters_out_done_files(self):
        """Files with already-existing outputs are filtered out when skip=True."""
        # Build a batch where the first file's output already exists (via tmp dir),
        # the second does not.
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # Simulate one file's output already existing — we use a real path
            # shape but redirect REPO to tmp for the duration of the test.
            bucket_dir = tmp_path / "working/wiki/pass2-buckets/test-bucket/prose-edges-haiku"
            bucket_dir.mkdir(parents=True)
            # File 1's output exists (non-empty)
            (bucket_dir / "file-001.edges.jsonl").write_text('{"decision":"emit_edge"}\n')
            # File 2's output does NOT exist

            row = {
                "batch_id": "batch-test",
                "shape": "source_target",
                "files": [
                    "working/wiki/pass2-buckets/test-bucket/prose-edge-candidates/file-001.candidates.jsonl",
                    "working/wiki/pass2-buckets/test-bucket/prose-edge-candidates/file-002.candidates.jsonl",
                ],
            }
            # Monkey-patch REPO so candidate_to_haiku_output writes to tmp.
            original_repo = runner.REPO
            runner.REPO = tmp_path
            try:
                chunks, warnings = runner.plan_batch_chunks(
                    row, chunk_size=3, skip_if_output_exists=True
                )
            finally:
                runner.REPO = original_repo

            # Only file-002 should remain — file-001's output already exists
            queued = [p for chunk in chunks for p, _ in chunk]
            self.assertEqual(len(queued), 1)
            self.assertTrue(queued[0].endswith("file-002.candidates.jsonl"))

    def test_skip_existing_default_false_preserves_old_behavior(self):
        """When skip flag is False (default), all files queued — old behavior preserved."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            bucket_dir = tmp_path / "working/wiki/pass2-buckets/test-bucket/prose-edges-haiku"
            bucket_dir.mkdir(parents=True)
            (bucket_dir / "file-001.edges.jsonl").write_text('{"x":1}\n')

            row = {
                "batch_id": "b",
                "shape": "source_target",
                "files": [
                    "working/wiki/pass2-buckets/test-bucket/prose-edge-candidates/file-001.candidates.jsonl",
                    "working/wiki/pass2-buckets/test-bucket/prose-edge-candidates/file-002.candidates.jsonl",
                ],
            }
            original_repo = runner.REPO
            runner.REPO = tmp_path
            try:
                # Default behavior (no skip flag): both files queued
                chunks, _ = runner.plan_batch_chunks(row, chunk_size=3)
            finally:
                runner.REPO = original_repo
            queued = [p for chunk in chunks for p, _ in chunk]
            self.assertEqual(len(queued), 2)


class TestDetectRateLimit(unittest.TestCase):
    """Verify rate-limit stream-json event parsing."""

    def _write(self, tmp_path: Path, lines: list[str]) -> Path:
        log = tmp_path / "stream.jsonl"
        log.write_text("\n".join(lines) + "\n")
        return log

    def test_missing_file_returns_none(self):
        self.assertIsNone(runner.detect_rate_limit(Path("/nonexistent/path.log")))

    def test_no_rate_limit_event(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            log = self._write(Path(tmp), [
                json.dumps({"type": "system", "subtype": "init"}),
                json.dumps({"type": "assistant", "message": {"content": []}}),
            ])
            self.assertIsNone(runner.detect_rate_limit(log))

    def test_ignores_allowed_warning(self):
        """allowed_warning is informational, not a rejection — should be skipped."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            log = self._write(Path(tmp), [
                json.dumps({
                    "type": "rate_limit_event",
                    "rate_limit_info": {
                        "status": "allowed_warning",
                        "resetsAt": 1779291600,
                        "rateLimitType": "five_hour",
                    },
                }),
            ])
            self.assertIsNone(runner.detect_rate_limit(log))

    def test_detects_rejection_with_reset_ts(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            log = self._write(Path(tmp), [
                json.dumps({
                    "type": "rate_limit_event",
                    "rate_limit_info": {
                        "status": "rejected",
                        "resetsAt": 1779291600,
                        "rateLimitType": "five_hour",
                    },
                }),
            ])
            result = runner.detect_rate_limit(log)
            self.assertIsNotNone(result)
            self.assertEqual(result["resets_at_ts"], 1779291600)
            self.assertEqual(result["rate_limit_type"], "five_hour")
            self.assertIn("resets at", result["reset_info"])

    def test_ignores_malformed_json_lines(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            log = self._write(Path(tmp), [
                "not json",
                json.dumps({"type": "rate_limit_event", "rate_limit_info": {"status": "rejected", "resetsAt": 1, "rateLimitType": "x"}}),
            ])
            result = runner.detect_rate_limit(log)
            self.assertIsNotNone(result)


class TestVerifyOutputs(unittest.TestCase):
    """Verify the post-Haiku output validation: file must exist, non-empty, valid JSONL."""

    def test_missing_file_is_bad(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            chunk_pairs = [("input.candidates.jsonl", tmp_path / "missing.edges.jsonl")]
            ok, bad = runner.verify_outputs(chunk_pairs)
            self.assertEqual(ok, [])
            self.assertEqual(len(bad), 1)

    def test_empty_file_is_bad(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            out = tmp_path / "empty.edges.jsonl"
            out.write_text("")
            ok, bad = runner.verify_outputs([("in.jsonl", out)])
            self.assertEqual(ok, [])
            self.assertEqual(len(bad), 1)

    def test_malformed_jsonl_is_bad(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            out = tmp_path / "bad.edges.jsonl"
            out.write_text("{not valid json\n")
            ok, bad = runner.verify_outputs([("in.jsonl", out)])
            self.assertEqual(ok, [])
            self.assertEqual(len(bad), 1)

    def test_valid_jsonl_is_ok(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            out = tmp_path / "good.edges.jsonl"
            out.write_text('{"decision":"emit_edge"}\n{"decision":"reject_just_mention"}\n')
            ok, bad = runner.verify_outputs([("in.jsonl", out)])
            self.assertEqual(len(ok), 1)
            self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
