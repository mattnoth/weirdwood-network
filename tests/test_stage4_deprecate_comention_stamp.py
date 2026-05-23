"""Tests for scripts/stage4-deprecate-comention-stamp.py.

Covers the four contracts required by design step 4 of the Pass-1-derived pivot:
  (a) stamps all non-blank rows with the three deprecation fields
  (b) idempotency — running twice produces no further changes
  (c) blank lines are preserved exactly
  (d) existing fields on stamped rows are left untouched

Run: python3 -m unittest tests.test_stage4_deprecate_comention_stamp -v
"""

import json
import tempfile
import unittest
from pathlib import Path

from tests._helpers import load_script

stamper = load_script("stage4-deprecate-comention-stamp.py")


class TestStampRow(unittest.TestCase):
    """Unit tests for the stamp_row() helper."""

    def _make_row(self, extra=None):
        row = {
            "candidate_kind": "comention",
            "evidence_chapter": "a-clash-of-kings-chapter-2",
            "pair_a": "aegon-i-targaryen",
            "pair_b": "catelyn-stark",
            "reason": "mentioned-in-summary",
        }
        if extra:
            row.update(extra)
        return row

    def test_stamps_all_rows(self):
        """(a) A fresh row receives all three deprecation fields."""
        row = self._make_row()
        result = stamper.stamp_row(row)

        self.assertEqual(result["status"], "superseded")
        self.assertEqual(result["superseded_by"], "pass1-derived")
        self.assertTrue(result["do_not_promote"])

    def test_existing_fields_untouched(self):
        """(d) Existing fields survive stamping without modification."""
        row = self._make_row()
        result = stamper.stamp_row(row)

        self.assertEqual(result["candidate_kind"], "comention")
        self.assertEqual(result["evidence_chapter"], "a-clash-of-kings-chapter-2")
        self.assertEqual(result["pair_a"], "aegon-i-targaryen")
        self.assertEqual(result["pair_b"], "catelyn-stark")
        self.assertEqual(result["reason"], "mentioned-in-summary")

    def test_idempotent_already_stamped(self):
        """(b) stamp_row on an already-stamped row returns it unchanged."""
        already = self._make_row({"status": "superseded",
                                   "superseded_by": "pass1-derived",
                                   "do_not_promote": True})
        result = stamper.stamp_row(already)
        # Should be the exact same object (not re-processed)
        self.assertIs(result, already)


class TestProcessFile(unittest.TestCase):
    """Integration tests for process_file() against a temp JSONL file."""

    def _write_jsonl(self, tmp_dir: Path, name: str, rows: list) -> Path:
        """Write rows (dicts or None for blank lines) to a JSONL file."""
        path = tmp_dir / name
        lines = []
        for r in rows:
            if r is None:
                lines.append("\n")
            else:
                lines.append(json.dumps(r) + "\n")
        path.write_text("".join(lines), encoding="utf-8")
        return path

    def test_stamps_all_rows_in_file(self):
        """(a) Every non-blank row in the file gets the three stamp fields."""
        rows = [
            {"candidate_kind": "comention", "pair_a": "jon-snow", "pair_b": "ghost"},
            {"candidate_kind": "comention", "pair_a": "arya-stark", "pair_b": "needle"},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_jsonl(Path(tmp), "test.comention-edges.jsonl", rows)
            total, changed, already = stamper.process_file(path, apply=True)

            self.assertEqual(total, 2)
            self.assertEqual(changed, 2)
            self.assertEqual(already, 0)

            # Read back and verify
            written = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
            for obj in written:
                self.assertEqual(obj["status"], "superseded")
                self.assertEqual(obj["superseded_by"], "pass1-derived")
                self.assertTrue(obj["do_not_promote"])

    def test_idempotency(self):
        """(b) Running process_file twice leaves the file identical on the second pass."""
        rows = [
            {"candidate_kind": "comention", "pair_a": "tyrion-lannister", "pair_b": "shae"},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_jsonl(Path(tmp), "test.comention-edges.jsonl", rows)

            # First pass
            total1, changed1, already1 = stamper.process_file(path, apply=True)
            content_after_first = path.read_text()

            # Second pass
            total2, changed2, already2 = stamper.process_file(path, apply=True)
            content_after_second = path.read_text()

            self.assertEqual(changed1, 1, "First pass should stamp 1 row")
            self.assertEqual(already1, 0, "First pass: nothing pre-stamped")

            self.assertEqual(changed2, 0, "Second pass should stamp 0 rows (idempotent)")
            self.assertEqual(already2, 1, "Second pass should report 1 already-stamped")

            self.assertEqual(content_after_first, content_after_second,
                             "File content must be identical after second pass")

    def test_blank_line_preservation(self):
        """(c) Blank lines in the JSONL are preserved exactly."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.comention-edges.jsonl"
            # Write a file with a blank line between two rows
            original = (
                '{"candidate_kind": "comention", "pair_a": "a", "pair_b": "b"}\n'
                "\n"
                '{"candidate_kind": "comention", "pair_a": "c", "pair_b": "d"}\n'
            )
            path.write_text(original, encoding="utf-8")

            total, changed, already = stamper.process_file(path, apply=True)

            # Two JSON rows, zero blank-line rows counted
            self.assertEqual(total, 2)
            self.assertEqual(changed, 2)

            # The blank line must still be present in the output
            result_lines = path.read_text().splitlines(keepends=True)
            blank_lines = [l for l in result_lines if l.strip() == ""]
            self.assertEqual(len(blank_lines), 1,
                             "Blank line must be preserved in stamped output")

    def test_existing_fields_untouched_in_file(self):
        """(d) No existing fields are removed or mutated by process_file."""
        row = {
            "candidate_kind": "comention",
            "evidence_chapter": "some-chapter",
            "evidence_chapter_bucket": "meta-chapters-acok",
            "pair_a": "ned-stark",
            "pair_b": "robert-baratheon",
            "reason": "mentioned-in-summary",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_jsonl(Path(tmp), "test.comention-edges.jsonl", [row])
            stamper.process_file(path, apply=True)

            result = json.loads(path.read_text().splitlines()[0])
            self.assertEqual(result["candidate_kind"], "comention")
            self.assertEqual(result["evidence_chapter"], "some-chapter")
            self.assertEqual(result["evidence_chapter_bucket"], "meta-chapters-acok")
            self.assertEqual(result["pair_a"], "ned-stark")
            self.assertEqual(result["pair_b"], "robert-baratheon")
            self.assertEqual(result["reason"], "mentioned-in-summary")
            # Plus the three stamp fields
            self.assertEqual(result["status"], "superseded")
            self.assertEqual(result["superseded_by"], "pass1-derived")
            self.assertTrue(result["do_not_promote"])

    def test_dry_run_does_not_write(self):
        """Dry-run mode must not modify the file."""
        rows = [{"candidate_kind": "comention", "pair_a": "x", "pair_b": "y"}]
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_jsonl(Path(tmp), "test.comention-edges.jsonl", rows)
            original_content = path.read_text()

            total, changed, already = stamper.process_file(path, apply=False)

            self.assertEqual(changed, 1, "Dry-run should still report 1 row to change")
            self.assertEqual(path.read_text(), original_content,
                             "Dry-run must not modify the file on disk")


if __name__ == "__main__":
    unittest.main()
