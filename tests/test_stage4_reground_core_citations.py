"""Tests for stage4-reground-core-citations.py.

Covers:
- Synthetic chapter file with a known quote on a known line → script sets
  evidence_ref to that line.
- A [PARAPHRASE] quote → edge left unchanged (skipped-no-quote).
- A quote not in the chapter → edge left unchanged + recorded as unresolved.
- Safety contract: only evidence_ref may differ; all other fields byte-identical;
  row count preserved.
- Short head (<15 chars) requires full quote match.
- Already-correct evidence_ref → counted as unchanged_correct, not regrounded.

Run: python3 -m unittest tests.test_stage4_reground_core_citations -v
"""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tests._helpers import load_script, REPO_ROOT

mod = load_script("stage4-reground-core-citations.py")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_chapter(tmp_dir: Path, book: str, slug: str, prose_lines: list[str]) -> Path:
    """Write a chapter .md with YAML frontmatter + given prose lines.

    Returns the chapter Path.  The frontmatter occupies lines 1-5 (---, 3 fields,
    ---) and a blank line 6, so prose starts at line 7.  Caller must account for
    this when asserting expected line numbers.
    """
    chapter_dir = tmp_dir / "sources" / "chapters" / book
    chapter_dir.mkdir(parents=True, exist_ok=True)
    path = chapter_dir / f"{slug}.md"
    frontmatter = "---\nbook: TEST\nchapter_number: 1\npov_character: Test\n---\n\n"
    path.write_text(frontmatter + "\n".join(prose_lines) + "\n", encoding="utf-8")
    return path


def _make_edge(chapter_rel: str, quote: str, old_line: int = 11, **kwargs) -> dict:
    """Return a minimal edge dict with the given evidence_ref and evidence_quote."""
    row = {
        "decision": "emit_edge",
        "candidate_kind": "pass1_relationship",
        "edge_type": "LOVES",
        "source_slug": "arya-stark",
        "source_resolution_status": "resolved-exact",
        "target_slug": "jon-snow",
        "target_resolution_status": "resolved-exact",
        "evidence_kind": "book-pass1",
        "evidence_book": "agot",
        "evidence_chapter": "agot-arya-01",
        "evidence_section": "Relationships Observed",
        "evidence_quote": quote,
        "evidence_ref": f"{chapter_rel}:{old_line}",
        "asserted_relation": "deep closeness",
        "hint_raw": "deep closeness",
        "extraction_file": "extractions/mechanical/agot/agot-arya-01.extraction.md",
        "confidence_tier": 1,
        "typed_by": "python-map",
        "corroborates_known_edge": True,
        "wiki_edge_type": "SIBLING_OF",
        "locate_status": "verbatim",
        "run_id": "pass1-derived-test",
        "schema_version": "pass1-derived-v1",
        "produced_at": "2026-05-26T00:00:00+00:00",
        "source_set": "spine",
        "dup_count": 1,
    }
    row.update(kwargs)
    return row


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestNormalize(unittest.TestCase):
    """normalize() must unify quote glyphs and collapse whitespace."""

    def test_curly_double_quotes(self):
        result = mod.normalize("“Hello world”")
        self.assertEqual(result, '"hello world"')

    def test_curly_single_quotes(self):
        result = mod.normalize("don’t")
        self.assertEqual(result, "don't")

    def test_em_dash(self):
        result = mod.normalize("foo—bar")
        self.assertEqual(result, "foo-bar")

    def test_whitespace_collapse(self):
        result = mod.normalize("  hello   world  ")
        self.assertEqual(result, "hello world")

    def test_lowercase(self):
        result = mod.normalize("Arya STARK")
        self.assertEqual(result, "arya stark")


class TestFindQuoteLine(unittest.TestCase):
    """find_quote_line() must locate the correct 1-based line."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def _write_chapter(self, lines: list[str]) -> Path:
        """Write a chapter file and return its path."""
        p = self.tmp / "test_chapter.md"
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return p

    def test_exact_match_line(self):
        # Quote is on line 5 (1-based)
        lines = [
            "line 1 content",
            "line 2 content",
            "line 3 content",
            "line 4 content",
            "The wolf pup loved her, even if no one else did.",
            "line 6 content",
        ]
        path = self._write_chapter(lines)
        result = mod.find_quote_line(
            "The wolf pup loved her, even if no one else did.", path
        )
        self.assertEqual(result, 5)

    def test_curly_quote_normalization(self):
        # File has curly quotes; query has straight quotes — should still match
        lines = [
            "plain line",
            "“Jon says he looks like a girl,” Arya said.",
        ]
        path = self._write_chapter(lines)
        result = mod.find_quote_line(
            '"Jon says he looks like a girl," Arya said.', path
        )
        self.assertEqual(result, 2)

    def test_substring_match(self):
        # Quote is contained mid-line (longer surrounding text)
        lines = [
            "prefix text The wolf pup loved her, even if no one else did. suffix text",
        ]
        path = self._write_chapter(lines)
        result = mod.find_quote_line("The wolf pup loved her, even if no one else did.", path)
        self.assertEqual(result, 1)

    def test_not_found_returns_none(self):
        lines = [
            "completely different content here",
            "nothing matching at all",
        ]
        path = self._write_chapter(lines)
        result = mod.find_quote_line("The wolf pup loved her, even if no one else did.", path)
        self.assertIsNone(result)

    def test_first_match_wins(self):
        # Quote appears on lines 2 and 4; should return 2
        quote = "repeated phrase here"
        lines = [
            "line 1",
            "prefix repeated phrase here suffix",
            "line 3",
            "another repeated phrase here suffix",
        ]
        path = self._write_chapter(lines)
        result = mod.find_quote_line(quote, path)
        self.assertEqual(result, 2)

    def test_short_head_requires_full_match(self):
        # Head is < SHORT_HEAD_THRESHOLD (15 chars); should still find
        short_quote = "Arya"
        # "Arya" is too short a head, so full quote match is required
        lines = [
            "line one no match",
            "Arya is brave and fierce.",
        ]
        path = self._write_chapter(lines)
        result = mod.find_quote_line(short_quote, path)
        self.assertEqual(result, 2)

    def test_multi_line_dialogue_first_sentence_fallback(self):
        # Quote spans two physical lines joined by '" " pattern.
        # The first part ends on line 2; second part on line 4.
        # Should anchor to line 2 via first-sentence fallback.
        lines = [
            "line 1 unrelated.",
            'He’s very gallant, don’t you think?"”',  # line 2 (ends with closing quote)
            "",
            '"Jon says he looks like a girl," Arya said.',             # line 4
        ]
        path = self._write_chapter(lines)
        # Combined quote as produced by the evidence locator
        combined = 'He’s very gallant, don’t you think?” “Jon says he looks like a girl,” Arya said.'
        result = mod.find_quote_line(combined, path)
        # Should find line 2 (where first sentence ends)
        self.assertEqual(result, 2)


class TestRegroundEdges(unittest.TestCase):
    """reground_edges() end-to-end with synthetic chapter files."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def _make_chapters_dir(self):
        """Return the chapters dir inside self.tmp."""
        d = self.tmp / "sources" / "chapters"
        d.mkdir(parents=True, exist_ok=True)
        return d

    def test_correct_reground_to_known_line(self):
        """Quote at line 9 of a chapter → evidence_ref updated from :11 to :9."""
        chapters_dir = self._make_chapters_dir()
        # Frontmatter = lines 1-5; blank = line 6; prose from line 7
        # We want the quote at line 9 (3rd prose line)
        chapter_path = _make_chapter(
            self.tmp, "agot", "agot-arya-01",
            [
                "Line 7 first prose line.",
                "Line 8 second prose line.",
                "The wolf pup loved her, even if no one else did.",  # line 9
                "Line 10 fourth prose line.",
            ],
        )

        chapter_rel = "sources/chapters/agot/agot-arya-01.md"
        row = _make_edge(chapter_rel, "The wolf pup loved her, even if no one else did.", old_line=11)

        # Monkey-patch REPO_ROOT to use self.tmp
        original_root = mod.REPO_ROOT
        mod.REPO_ROOT = self.tmp
        try:
            output_rows, stats = mod.reground_edges([row], chapters_dir)
        finally:
            mod.REPO_ROOT = original_root

        self.assertEqual(len(output_rows), 1)
        self.assertEqual(output_rows[0]["evidence_ref"], f"{chapter_rel}:9")
        self.assertEqual(stats["regrounded"], 1)
        self.assertEqual(stats["skipped_no_quote"], 0)
        self.assertEqual(stats["unresolved"], 0)

    def test_paraphrase_quote_skipped(self):
        """[PARAPHRASE] quote → edge unchanged, counted as skipped_no_quote."""
        chapters_dir = self._make_chapters_dir()
        chapter_rel = "sources/chapters/agot/agot-arya-01.md"
        row = _make_edge(chapter_rel, "[PARAPHRASE] deep closeness", old_line=11)

        original_root = mod.REPO_ROOT
        mod.REPO_ROOT = self.tmp
        try:
            output_rows, stats = mod.reground_edges([row], chapters_dir)
        finally:
            mod.REPO_ROOT = original_root

        self.assertEqual(output_rows[0]["evidence_ref"], f"{chapter_rel}:11")
        self.assertEqual(output_rows[0]["evidence_quote"], "[PARAPHRASE] deep closeness")
        self.assertEqual(stats["skipped_no_quote"], 1)
        self.assertEqual(stats["regrounded"], 0)

    def test_no_evidence_ref_skipped(self):
        """Edge with no ':' in evidence_ref → skipped."""
        chapters_dir = self._make_chapters_dir()
        row = _make_edge("sources/chapters/agot/agot-arya-01.md", "Some quote")
        row["evidence_ref"] = "sources/chapters/agot/agot-arya-01.md"  # no :line

        original_root = mod.REPO_ROOT
        mod.REPO_ROOT = self.tmp
        try:
            output_rows, stats = mod.reground_edges([row], chapters_dir)
        finally:
            mod.REPO_ROOT = original_root

        self.assertEqual(output_rows[0]["evidence_ref"], "sources/chapters/agot/agot-arya-01.md")
        self.assertEqual(stats["skipped_no_quote"], 1)

    def test_quote_not_found_unresolved(self):
        """Quote not present in chapter → edge unchanged, recorded as unresolved."""
        chapters_dir = self._make_chapters_dir()
        _make_chapter(
            self.tmp, "agot", "agot-arya-01",
            ["This chapter contains completely different text."],
        )
        chapter_rel = "sources/chapters/agot/agot-arya-01.md"
        row = _make_edge(chapter_rel, "The wolf pup loved her, even if no one else did.", old_line=11)

        original_root = mod.REPO_ROOT
        mod.REPO_ROOT = self.tmp
        try:
            output_rows, stats = mod.reground_edges([row], chapters_dir)
        finally:
            mod.REPO_ROOT = original_root

        self.assertEqual(output_rows[0]["evidence_ref"], f"{chapter_rel}:11")
        self.assertEqual(stats["unresolved"], 1)
        self.assertEqual(stats["regrounded"], 0)
        self.assertEqual(len(stats["unresolved_list"]), 1)
        self.assertEqual(stats["unresolved_list"][0]["source_slug"], "arya-stark")

    def test_already_correct_ref_not_counted_as_regrounded(self):
        """If the existing evidence_ref already points to the correct line → unchanged_correct."""
        chapters_dir = self._make_chapters_dir()
        chapter_path = _make_chapter(
            self.tmp, "agot", "agot-arya-01",
            [
                "Line 7 content.",
                "Line 8 content.",
                "The wolf pup loved her, even if no one else did.",  # line 9
            ],
        )
        chapter_rel = "sources/chapters/agot/agot-arya-01.md"
        # Feed the already-correct ref (:9)
        row = _make_edge(chapter_rel, "The wolf pup loved her, even if no one else did.", old_line=9)

        original_root = mod.REPO_ROOT
        mod.REPO_ROOT = self.tmp
        try:
            output_rows, stats = mod.reground_edges([row], chapters_dir)
        finally:
            mod.REPO_ROOT = original_root

        self.assertEqual(output_rows[0]["evidence_ref"], f"{chapter_rel}:9")
        self.assertEqual(stats["regrounded"], 0)
        self.assertEqual(stats["unchanged_correct"], 1)


class TestSafetyAssertion(unittest.TestCase):
    """assert_safety() must catch field mutations and count mismatches."""

    def _base_row(self) -> dict:
        return {
            "source_slug": "arya-stark",
            "target_slug": "jon-snow",
            "edge_type": "LOVES",
            "evidence_quote": "They were close.",
            "evidence_ref": "sources/chapters/agot/agot-arya-01.md:11",
            "confidence_tier": 1,
        }

    def test_passes_when_only_evidence_ref_changes(self):
        inp = self._base_row()
        out = copy.deepcopy(inp)
        out["evidence_ref"] = "sources/chapters/agot/agot-arya-01.md:35"
        # Should not raise
        mod.assert_safety([inp], [out])

    def test_fails_on_row_count_mismatch(self):
        inp = self._base_row()
        out = copy.deepcopy(inp)
        with self.assertRaises(AssertionError) as ctx:
            mod.assert_safety([inp], [out, out])
        self.assertIn("count", str(ctx.exception).lower())

    def test_fails_when_non_ref_field_changes(self):
        inp = self._base_row()
        out = copy.deepcopy(inp)
        out["evidence_quote"] = "CHANGED QUOTE"
        with self.assertRaises(AssertionError) as ctx:
            mod.assert_safety([inp], [out])
        self.assertIn("evidence_quote", str(ctx.exception))

    def test_fails_when_edge_type_changes(self):
        inp = self._base_row()
        out = copy.deepcopy(inp)
        out["edge_type"] = "HATES"
        with self.assertRaises(AssertionError) as ctx:
            mod.assert_safety([inp], [out])
        self.assertIn("edge_type", str(ctx.exception))

    def test_passes_with_identical_rows(self):
        inp = self._base_row()
        out = copy.deepcopy(inp)
        mod.assert_safety([inp], [out])


class TestMultipleEdges(unittest.TestCase):
    """Mixed batch: some regrounded, some skipped, some unresolved."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_mixed_batch(self):
        chapters_dir = self.tmp / "sources" / "chapters"
        chapters_dir.mkdir(parents=True, exist_ok=True)

        _make_chapter(
            self.tmp, "agot", "agot-arya-01",
            [
                "First prose line here.",       # line 7
                "Second prose line here.",      # line 8
                "Arya loved her wolf dearly.",  # line 9
            ],
        )
        chapter_rel = "sources/chapters/agot/agot-arya-01.md"

        rows = [
            # Row 0: should reground :11 → :9
            _make_edge(chapter_rel, "Arya loved her wolf dearly.", old_line=11),
            # Row 1: paraphrase → skip
            _make_edge(chapter_rel, "[PARAPHRASE] wolf bond", old_line=11,
                       source_slug="arya-stark", target_slug="nymeria",
                       edge_type="BONDED_TO"),
            # Row 2: quote not in chapter → unresolved
            _make_edge(chapter_rel, "A phrase that does not appear anywhere in this chapter text.",
                       old_line=11, source_slug="ned-stark", target_slug="robb-stark",
                       edge_type="PARENT_OF"),
        ]

        original_root = mod.REPO_ROOT
        mod.REPO_ROOT = self.tmp
        try:
            output_rows, stats = mod.reground_edges(rows, chapters_dir)
        finally:
            mod.REPO_ROOT = original_root

        self.assertEqual(len(output_rows), 3)
        self.assertEqual(stats["regrounded"], 1)
        self.assertEqual(stats["skipped_no_quote"], 1)
        self.assertEqual(stats["unresolved"], 1)

        # Row 0 updated
        self.assertEqual(output_rows[0]["evidence_ref"], f"{chapter_rel}:9")
        # Row 1 unchanged
        self.assertEqual(output_rows[1]["evidence_ref"], f"{chapter_rel}:11")
        self.assertEqual(output_rows[1]["evidence_quote"], "[PARAPHRASE] wolf bond")
        # Row 2 unchanged
        self.assertEqual(output_rows[2]["evidence_ref"], f"{chapter_rel}:11")

        # Safety contract holds for the mixed batch
        mod.assert_safety(rows, output_rows)


if __name__ == "__main__":
    unittest.main()
