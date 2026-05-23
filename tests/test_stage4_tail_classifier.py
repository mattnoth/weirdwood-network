"""Tests for scripts/stage4-tail-classifier.py — hermetic, stdlib unittest.

No real claude -p calls are made. All subprocess invocations are mocked.

Run: python3 -m unittest tests.test_stage4_tail_classifier -v
"""

from __future__ import annotations

import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path

from tests._helpers import load_script

# Load the module under test
tc = load_script("stage4-tail-classifier.py")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SAMPLE_VOCAB = frozenset({
    "PARENT_OF", "SIBLING_OF", "SPOUSE_OF", "WARD_OF", "HOLDS_TITLE",
    "VOWS_TO", "MANIPULATES", "SWORN_TO",  # all Tier-1
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
    """Build a minimal tail row for testing."""
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
        "produced_at": "2026-05-23T00:00:00+00:00",
    }
    row.update(overrides)
    return row


def _mock_claude_response(objects: list[dict], cost: float = 0.001) -> dict:
    """Build a mock invoke_claude return value wrapping a JSON array."""
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


# ---------------------------------------------------------------------------
# Tests: prompt assembly
# ---------------------------------------------------------------------------

class TestPromptAssembly(unittest.TestCase):
    """Verify prompt structure and idx injection."""

    def test_idx_injected_in_prompt(self):
        rows = [_make_tail_row(), _make_tail_row(source_slug="ned-stark", target_slug="jon-snow")]
        prompt = tc.render_classify_prompt(rows, _SAMPLE_VOCAB)
        # Both idx values must appear
        self.assertIn('"idx": 0', prompt)
        self.assertIn('"idx": 1', prompt)

    def test_vocab_list_present(self):
        rows = [_make_tail_row()]
        prompt = tc.render_classify_prompt(rows, _SAMPLE_VOCAB)
        # At least some vocab types should appear in the prompt
        self.assertIn("SERVES", prompt)
        self.assertIn("LOVES", prompt)
        self.assertIn("PARENT_OF", prompt)

    def test_tier1_instructions_present(self):
        rows = [_make_tail_row()]
        prompt = tc.render_classify_prompt(rows, _SAMPLE_VOCAB)
        # Tier-1 qualifier instructions must appear
        self.assertIn("SIBLING_OF", prompt)
        self.assertIn("PARENT_OF", prompt)
        # Qualifier is REQUIRED (prompt uses "REQUIRE" phrasing)
        self.assertIn("REQUIRE", prompt)

    def test_source_target_names_in_prompt(self):
        row = _make_tail_row(source_slug="ned-stark", target_slug="catelyn-stark")
        # Patch display name resolution to return predictable names
        with patch.object(tc, "get_display_name", side_effect=lambda s: s.replace("-", " ").title()):
            prompt = tc.render_classify_prompt([row], _SAMPLE_VOCAB)
        self.assertIn("Ned Stark", prompt)
        self.assertIn("Catelyn Stark", prompt)

    def test_evidence_quote_in_prompt(self):
        row = _make_tail_row(evidence_quote="She had sworn an oath to Lady Stark.")
        prompt = tc.render_classify_prompt([row], _SAMPLE_VOCAB)
        self.assertIn("She had sworn an oath to Lady Stark.", prompt)

    def test_hint_in_prompt(self):
        row = _make_tail_row(hint_raw="sworn loyalty")
        prompt = tc.render_classify_prompt([row], _SAMPLE_VOCAB)
        self.assertIn("sworn loyalty", prompt)

    def test_chapter_in_prompt(self):
        row = _make_tail_row(evidence_chapter="affc-brienne-03")
        prompt = tc.render_classify_prompt([row], _SAMPLE_VOCAB)
        self.assertIn("affc-brienne-03", prompt)

    def test_reject_instructions_present(self):
        rows = [_make_tail_row()]
        prompt = tc.render_classify_prompt(rows, _SAMPLE_VOCAB)
        self.assertIn("REJECT", prompt)


# ---------------------------------------------------------------------------
# Tests: JSON parse of well-formed batch response
# ---------------------------------------------------------------------------

class TestParseBatchResponse(unittest.TestCase):
    """parse_batch_response: well-formed and edge-case inputs."""

    def _wrap(self, objects: list[dict]) -> str:
        """Wrap model output in claude's JSON envelope."""
        return json.dumps({"result": json.dumps(objects), "total_cost_usd": 0.001})

    def test_well_formed_batch(self):
        objects = [{"idx": 0, "edge_type": "SERVES"}, {"idx": 1, "edge_type": "LOVES"}]
        raw = self._wrap(objects)
        parsed, err = tc.parse_batch_response(raw, 2)
        self.assertIsNone(err)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]["edge_type"], "SERVES")

    def test_empty_response(self):
        raw = json.dumps({"result": "", "total_cost_usd": 0.0})
        parsed, err = tc.parse_batch_response(raw, 1)
        self.assertEqual(parsed, [])
        self.assertIsNotNone(err)

    def test_malformed_json(self):
        raw = json.dumps({"result": "[{not valid json", "total_cost_usd": 0.0})
        parsed, err = tc.parse_batch_response(raw, 1)
        self.assertEqual(parsed, [])
        self.assertIsNotNone(err)

    def test_model_returns_non_array(self):
        raw = json.dumps({"result": json.dumps({"edge_type": "SERVES"}), "total_cost_usd": 0.0})
        parsed, err = tc.parse_batch_response(raw, 1)
        self.assertEqual(parsed, [])
        self.assertIsNotNone(err)

    def test_strips_code_fence(self):
        model_text = "```json\n[{\"idx\": 0, \"edge_type\": \"SERVES\"}]\n```"
        raw = json.dumps({"result": model_text, "total_cost_usd": 0.0})
        parsed, err = tc.parse_batch_response(raw, 1)
        self.assertIsNone(err)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["edge_type"], "SERVES")

    def test_totally_invalid_outer(self):
        """Even if outer JSON is invalid, fallback to raw as model text."""
        # If raw output is itself just a JSON array (rare fallback)
        objects = [{"idx": 0, "edge_type": "LOVES"}]
        raw = json.dumps(objects)  # no outer envelope
        parsed, err = tc.parse_batch_response(raw, 1)
        # raw is a valid JSON array — should parse
        self.assertIsNone(err)
        self.assertEqual(len(parsed), 1)


# ---------------------------------------------------------------------------
# Tests: idx alignment
# ---------------------------------------------------------------------------

class TestAlignBatchOutput(unittest.TestCase):
    """align_batch_output: idx alignment logic."""

    def _rows(self, n: int) -> list[dict]:
        return [_make_tail_row() for _ in range(n)]

    def test_happy_path(self):
        objects = [{"idx": 0, "edge_type": "LOVES"}, {"idx": 1, "edge_type": "FEARS"}]
        rows = self._rows(2)
        aligned = tc.align_batch_output(objects, rows)
        self.assertEqual(set(aligned.keys()), {0, 1})

    def test_missing_idx_excluded(self):
        objects = [{"idx": 0, "edge_type": "LOVES"}]
        rows = self._rows(2)
        aligned = tc.align_batch_output(objects, rows)
        self.assertIn(0, aligned)
        self.assertNotIn(1, aligned)  # row 1 has no model output

    def test_extra_idx_ignored(self):
        """Out-of-range idx is silently dropped."""
        objects = [{"idx": 0, "edge_type": "LOVES"}, {"idx": 99, "edge_type": "FEARS"}]
        rows = self._rows(2)
        aligned = tc.align_batch_output(objects, rows)
        self.assertIn(0, aligned)
        self.assertNotIn(99, aligned)

    def test_duplicate_idx_excluded(self):
        """Duplicate idx: neither copy should appear in aligned output."""
        objects = [
            {"idx": 0, "edge_type": "LOVES"},
            {"idx": 0, "edge_type": "FEARS"},  # duplicate
        ]
        rows = self._rows(2)
        aligned = tc.align_batch_output(objects, rows)
        # idx 0 was duplicated → both dropped
        self.assertNotIn(0, aligned)

    def test_no_idx_field(self):
        objects = [{"edge_type": "LOVES"}]  # missing idx
        rows = self._rows(1)
        aligned = tc.align_batch_output(objects, rows)
        self.assertEqual(aligned, {})

    def test_non_integer_idx_ignored(self):
        objects = [{"idx": "zero", "edge_type": "LOVES"}]
        rows = self._rows(1)
        aligned = tc.align_batch_output(objects, rows)
        self.assertEqual(aligned, {})


# ---------------------------------------------------------------------------
# Tests: conform_edge_type
# ---------------------------------------------------------------------------

class TestConformEdgeType(unittest.TestCase):
    """conform_edge_type: vocab conformance and routing."""

    def test_valid_tier3_type(self):
        decision, err = tc.conform_edge_type("SERVES", _SAMPLE_VOCAB, _TIER1, None)
        self.assertEqual(decision, "emit_edge")
        self.assertIsNone(err)

    def test_reject(self):
        decision, err = tc.conform_edge_type("REJECT", _SAMPLE_VOCAB, _TIER1, None)
        self.assertEqual(decision, "rejected")

    def test_out_of_vocab(self):
        decision, err = tc.conform_edge_type("KNOWS_ABOUT", _SAMPLE_VOCAB, _TIER1, None)
        self.assertEqual(decision, "classify_failed")
        self.assertIn("not in locked vocab", err)

    def test_tier1_without_qualifier(self):
        decision, err = tc.conform_edge_type("PARENT_OF", _SAMPLE_VOCAB, _TIER1, None)
        self.assertEqual(decision, "needs_qualifier")
        self.assertIsNone(err)

    def test_tier1_with_qualifier(self):
        decision, err = tc.conform_edge_type("PARENT_OF", _SAMPLE_VOCAB, _TIER1, "biological")
        self.assertEqual(decision, "emit_edge")
        self.assertIsNone(err)

    def test_tier3_with_qualifier_still_emits(self):
        """Tier-3 types: qualifier is silently accepted at conform time.
        The validator (separate) rejects tier-3 qualifiers; conform just checks vocab.
        """
        decision, err = tc.conform_edge_type("SERVES", _SAMPLE_VOCAB, _TIER1, "some_qualifier")
        # conform_edge_type doesn't check tier-3 qualifier presence — that's the validator's job
        self.assertEqual(decision, "emit_edge")

    def test_empty_string_edge_type(self):
        decision, err = tc.conform_edge_type("", _SAMPLE_VOCAB, _TIER1, None)
        self.assertEqual(decision, "classify_failed")


# ---------------------------------------------------------------------------
# Tests: process_batch — missing/extra/duplicate idx → classify_failed
# ---------------------------------------------------------------------------

class TestProcessBatch(unittest.TestCase):
    """process_batch: end-to-end with mocked invoke_claude."""

    def _call_process_batch(self, batch: list[dict], mock_objects: list[dict], cost: float = 0.002):
        """Run process_batch with mocked claude invocation."""
        mock_resp = _mock_claude_response(mock_objects, cost=cost)
        with patch.object(tc, "invoke_claude", return_value=mock_resp):
            return tc.process_batch(
                batch=batch,
                batch_idx=0,
                locked_vocab=_SAMPLE_VOCAB,
                tier1_types=_TIER1,
                model="claude-test",
                run_id="test-run",
                apply=True,
            )

    def test_happy_path_emit(self):
        batch = [_make_tail_row()]
        model_objects = [{"idx": 0, "edge_type": "LOVES"}]
        result = self._call_process_batch(batch, model_objects)
        self.assertEqual(result["typed"], 1)
        self.assertEqual(result["rejected"], 0)
        self.assertEqual(result["classify_failed"], 0)
        self.assertEqual(result["needs_qualifier"], 0)
        self.assertEqual(len(result["emit_rows"]), 1)

    def test_reject_routing(self):
        batch = [_make_tail_row()]
        model_objects = [{"idx": 0, "edge_type": "REJECT"}]
        result = self._call_process_batch(batch, model_objects)
        self.assertEqual(result["rejected"], 1)
        self.assertEqual(result["typed"], 0)
        self.assertEqual(len(result["rejected_rows"]), 1)

    def test_out_of_vocab_type(self):
        batch = [_make_tail_row()]
        model_objects = [{"idx": 0, "edge_type": "KNOWS_ABOUT"}]
        result = self._call_process_batch(batch, model_objects)
        self.assertEqual(result["classify_failed"], 1)
        self.assertEqual(result["conform_violations"], 1)

    def test_tier1_without_qualifier_to_needs_qualifier(self):
        batch = [_make_tail_row()]
        model_objects = [{"idx": 0, "edge_type": "PARENT_OF"}]  # no qualifier
        result = self._call_process_batch(batch, model_objects)
        self.assertEqual(result["needs_qualifier"], 1)
        self.assertEqual(result["typed"], 0)
        self.assertEqual(len(result["needs_qualifier_rows"]), 1)

    def test_tier1_with_qualifier_emits(self):
        batch = [_make_tail_row()]
        model_objects = [{"idx": 0, "edge_type": "PARENT_OF", "qualifier": "biological"}]
        result = self._call_process_batch(batch, model_objects)
        self.assertEqual(result["typed"], 1)
        self.assertEqual(result["needs_qualifier"], 0)
        emit = result["emit_rows"][0]
        self.assertEqual(emit["qualifier"], "biological")

    def test_missing_idx_yields_classify_failed(self):
        batch = [_make_tail_row(), _make_tail_row(hint_raw="another")]
        model_objects = [{"idx": 0, "edge_type": "LOVES"}]  # idx 1 missing
        result = self._call_process_batch(batch, model_objects)
        self.assertEqual(result["typed"], 1)
        self.assertEqual(result["classify_failed"], 1)

    def test_duplicate_idx_yields_classify_failed(self):
        batch = [_make_tail_row()]
        model_objects = [
            {"idx": 0, "edge_type": "LOVES"},
            {"idx": 0, "edge_type": "FEARS"},  # duplicate
        ]
        result = self._call_process_batch(batch, model_objects)
        # idx 0 duplicated → both dropped → classify_failed
        self.assertEqual(result["classify_failed"], 1)
        self.assertEqual(result["typed"], 0)

    def test_parse_error_entire_batch_fails(self):
        batch = [_make_tail_row(), _make_tail_row(hint_raw="other")]
        bad_resp = {
            "returncode": 0,
            "raw_output": json.dumps({"result": "not a json array", "total_cost_usd": 0.001}),
            "result_json": None,
            "total_cost_usd": 0.001,
            "error_message": None,
            "duration_s": 0.1,
        }
        with patch.object(tc, "invoke_claude", return_value=bad_resp):
            result = tc.process_batch(
                batch=batch,
                batch_idx=0,
                locked_vocab=_SAMPLE_VOCAB,
                tier1_types=_TIER1,
                model="claude-test",
                run_id="test-run",
                apply=True,
            )
        self.assertEqual(result["classify_failed"], 2)
        self.assertEqual(result["typed"], 0)

    def test_dry_run_returns_no_rows(self):
        batch = [_make_tail_row()]
        result = tc.process_batch(
            batch=batch,
            batch_idx=0,
            locked_vocab=_SAMPLE_VOCAB,
            tier1_types=_TIER1,
            model="claude-test",
            run_id="test-run",
            apply=False,
        )
        self.assertEqual(result["typed"], 0)
        self.assertIn("prompt", result)  # dry-run includes rendered prompt


# ---------------------------------------------------------------------------
# Tests: emitted-edge schema matches deterministic schema keys
# ---------------------------------------------------------------------------

class TestEmitEdgeSchema(unittest.TestCase):
    """Emitted edges must carry the same field set as the deterministic edges."""

    # The exact set of keys in a deterministic emit_edge row
    _DETERMINISTIC_KEYS = {
        "decision", "candidate_kind", "edge_type", "source_slug",
        "source_resolution_status", "target_slug", "target_resolution_status",
        "evidence_kind", "evidence_book", "evidence_chapter", "evidence_section",
        "evidence_quote", "evidence_ref", "asserted_relation", "hint_raw",
        "extraction_file", "confidence_tier", "typed_by", "corroborates_known_edge",
        "wiki_edge_type", "locate_status", "run_id", "schema_version", "produced_at",
    }

    def test_emit_row_contains_deterministic_keys(self):
        tail_row = _make_tail_row()
        row = tc.build_emit_edge_row(
            tail_row=tail_row,
            edge_type="LOVES",
            qualifier=None,
            model="claude-sonnet-4-6",
            run_id="test-run",
        )
        for key in self._DETERMINISTIC_KEYS:
            self.assertIn(key, row, f"Missing key: {key}")

    def test_typed_by_is_sonnet(self):
        tail_row = _make_tail_row()
        row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-sonnet-4-6", "r1")
        self.assertEqual(row["typed_by"], "sonnet")

    def test_decision_is_emit_edge(self):
        tail_row = _make_tail_row()
        row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-sonnet-4-6", "r1")
        self.assertEqual(row["decision"], "emit_edge")

    def test_evidence_book_derived_from_chapter(self):
        tail_row = _make_tail_row(evidence_chapter="asos-jon-05")
        row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-sonnet-4-6", "r1")
        self.assertEqual(row["evidence_book"], "asos")

    def test_qualifier_present_when_set(self):
        tail_row = _make_tail_row()
        row = tc.build_emit_edge_row(tail_row, "PARENT_OF", "biological", "claude-sonnet-4-6", "r1")
        self.assertEqual(row["qualifier"], "biological")

    def test_qualifier_absent_when_not_set(self):
        tail_row = _make_tail_row()
        row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-sonnet-4-6", "r1")
        self.assertNotIn("qualifier", row)

    def test_candidate_kind_is_pass1_relationship(self):
        tail_row = _make_tail_row()
        row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-sonnet-4-6", "r1")
        self.assertEqual(row["candidate_kind"], "pass1_relationship")

    def test_source_resolution_status_is_tail_llm(self):
        tail_row = _make_tail_row()
        row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-sonnet-4-6", "r1")
        self.assertEqual(row["source_resolution_status"], "tail-llm")
        self.assertEqual(row["target_resolution_status"], "tail-llm")

    def test_confidence_tier_is_1(self):
        tail_row = _make_tail_row()
        row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-sonnet-4-6", "r1")
        self.assertEqual(row["confidence_tier"], 1)


# ---------------------------------------------------------------------------
# Tests: multi-row batches, --smoke behavior
# ---------------------------------------------------------------------------

class TestBatchSizeAndSmoke(unittest.TestCase):
    """Chunking + smoke limit."""

    def test_smoke_limits_rows(self):
        """load_tail_rows with smoke=3 returns at most 3 rows."""
        # Use real tail files if they exist, else mock the glob
        tail_dir = Path(__file__).resolve().parent.parent / "working/wiki/pass2-buckets/pass1-derived/_tail"
        if not tail_dir.exists():
            self.skipTest("Tail dir not present in this environment")

        rows = tc.load_tail_rows(tc.BOOKS, smoke=3)
        self.assertLessEqual(len(rows), 3)

    def test_chunk_boundary_exact(self):
        """With 6 rows and chunk_size=3, we get exactly 2 chunks."""
        rows = [_make_tail_row() for _ in range(6)]
        chunks = [rows[i:i+3] for i in range(0, len(rows), 3)]
        self.assertEqual(len(chunks), 2)
        self.assertEqual(all(len(c) == 3 for c in chunks), True)

    def test_chunk_boundary_uneven(self):
        """With 7 rows and chunk_size=3, last chunk has 1 row."""
        rows = [_make_tail_row() for _ in range(7)]
        chunks = [rows[i:i+3] for i in range(0, len(rows), 3)]
        self.assertEqual(len(chunks), 3)
        self.assertEqual(len(chunks[-1]), 1)


# ---------------------------------------------------------------------------
# Tests: --skip-existing
# ---------------------------------------------------------------------------

class TestSkipExisting(unittest.TestCase):
    """row_skip_key and skip-existing filtering logic."""

    def test_skip_key_structure(self):
        row = _make_tail_row()
        key = tc.row_skip_key(row)
        self.assertEqual(key, ("brienne-tarth", "catelyn-stark", "affc-brienne-03"))

    def test_skip_key_missing_chapter(self):
        row = _make_tail_row()
        del row["evidence_chapter"]
        key = tc.row_skip_key(row)
        self.assertEqual(key[2], "")

    def test_filtering_logic(self):
        rows = [
            _make_tail_row(source_slug="a", target_slug="b", evidence_chapter="agot-test-01"),
            _make_tail_row(source_slug="c", target_slug="d", evidence_chapter="agot-test-02"),
        ]
        existing = {("a", "b", "agot-test-01")}
        filtered = [r for r in rows if tc.row_skip_key(r) not in existing]
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["source_slug"], "c")


# ---------------------------------------------------------------------------
# Tests: load_locked_vocab and load_tier1_edge_types
# ---------------------------------------------------------------------------

class TestVocabLoading(unittest.TestCase):
    """Vocab and Tier-1 loading from real reference files."""

    @classmethod
    def setUpClass(cls):
        arch = Path(__file__).resolve().parent.parent / "reference/architecture.md"
        qual = Path(__file__).resolve().parent.parent / "reference/edge-qualifier-vocab.md"
        if not arch.exists() or not qual.exists():
            raise unittest.SkipTest("Reference files not present")
        cls.vocab = tc.load_locked_vocab(arch)
        cls.tier1 = tc.load_tier1_edge_types(qual)

    def test_vocab_contains_known_types(self):
        for t in ["PARENT_OF", "KILLS", "SERVES", "LOVES", "MEMBER_OF"]:
            self.assertIn(t, self.vocab, f"{t} should be in vocab")

    def test_vocab_excludes_book_abbreviations(self):
        for t in ["AGOT", "ACOK", "ASOS", "AFFC", "ADWD"]:
            self.assertNotIn(t, self.vocab)

    # ------------------------------------------------------------------
    # Regression: load_locked_vocab must return the canonical 163-type set,
    # not the naive backtick-scrape which yields 170 polluted tokens.
    # Pollutants dropped: ACCOMPANIES, ADWD, FIELD_EDGE_MAP, FOSTERED_BY,
    # KNOWS, LOCATED_IN, MARRIED_TO, POV, RELIGION_OF
    # ------------------------------------------------------------------

    def test_vocab_count_is_163(self):
        """Canonical locked vocab must contain exactly 163 types."""
        self.assertEqual(
            len(self.vocab),
            163,
            f"Expected 163 canonical types, got {len(self.vocab)}. "
            f"Extra: {sorted(self.vocab - frozenset())}",
        )

    def test_vocab_excludes_deprecated_and_pollutant_tokens(self):
        """Nine tokens that the naive backtick-scrape included must be absent."""
        pollutants = {
            "ACCOMPANIES", "ADWD", "FIELD_EDGE_MAP", "FOSTERED_BY",
            "KNOWS", "LOCATED_IN", "MARRIED_TO", "POV", "RELIGION_OF",
        }
        found = pollutants & self.vocab
        self.assertEqual(
            found, set(),
            f"Pollutant tokens still present in locked vocab: {sorted(found)}",
        )

    def test_knows_adwd_pov_excluded(self):
        """Spot-check the three most dangerous pollutants explicitly."""
        self.assertNotIn("KNOWS", self.vocab, "Deprecated KNOWS must not be in vocab")
        self.assertNotIn("ADWD", self.vocab, "Book-code ADWD must not be in vocab")
        self.assertNotIn("POV", self.vocab, "POV must not be in vocab")

    def test_valid_active_types_included(self):
        """Spot-check that active canonical types are present."""
        for t in ["CONTRASTS", "SIBLING_OF", "ENCOUNTERS", "TRAVELS_WITH"]:
            self.assertIn(t, self.vocab, f"{t} must be in canonical vocab")

    def test_tier1_contains_required_types(self):
        for t in ["SIBLING_OF", "SPOUSE_OF", "PARENT_OF", "WARD_OF",
                  "HOLDS_TITLE", "VOWS_TO", "MANIPULATES", "SWORN_TO"]:
            self.assertIn(t, self.tier1, f"{t} should be Tier-1")

    def test_tier1_is_subset_of_vocab(self):
        self.assertTrue(self.tier1.issubset(self.vocab))


# ---------------------------------------------------------------------------
# Tests: invoke_claude — verifies cwd=/tmp in subprocess call
# ---------------------------------------------------------------------------

class TestInvokeClaude(unittest.TestCase):
    """invoke_claude: verify cwd=/tmp and subprocess pattern."""

    def test_cwd_is_tmp(self):
        """subprocess.run must be called with cwd='/tmp'."""
        captured_kwargs: dict = {}

        def fake_run(cmd, **kwargs):
            captured_kwargs.update(kwargs)
            # Return minimal subprocess result
            mock = MagicMock()
            mock.returncode = 0
            mock.stdout = json.dumps({"result": "[]", "total_cost_usd": 0.001})
            mock.stderr = ""
            return mock

        with patch("subprocess.run", side_effect=fake_run):
            tc.invoke_claude("test prompt", "claude-test")

        self.assertEqual(captured_kwargs.get("cwd"), "/tmp",
                         "cwd must be /tmp to avoid loading repo's CLAUDE.md")

    def test_model_passed_to_command(self):
        """The --model flag must be passed to the claude -p command."""
        captured_cmd: list = []

        def fake_run(cmd, **kwargs):
            captured_cmd.extend(cmd)
            mock = MagicMock()
            mock.returncode = 0
            mock.stdout = json.dumps({"result": "[]", "total_cost_usd": 0.0})
            mock.stderr = ""
            return mock

        with patch("subprocess.run", side_effect=fake_run):
            tc.invoke_claude("test prompt", "claude-haiku-4-5")

        self.assertIn("--model", captured_cmd)
        model_idx = captured_cmd.index("--model")
        self.assertEqual(captured_cmd[model_idx + 1], "claude-haiku-4-5")

    def test_output_format_json(self):
        """--output-format json must be in the command."""
        captured_cmd: list = []

        def fake_run(cmd, **kwargs):
            captured_cmd.extend(cmd)
            mock = MagicMock()
            mock.returncode = 0
            mock.stdout = json.dumps({"result": "[]", "total_cost_usd": 0.0})
            mock.stderr = ""
            return mock

        with patch("subprocess.run", side_effect=fake_run):
            tc.invoke_claude("test prompt", "claude-sonnet-4-6")

        self.assertIn("--output-format", captured_cmd)
        fmt_idx = captured_cmd.index("--output-format")
        self.assertEqual(captured_cmd[fmt_idx + 1], "json")


# ---------------------------------------------------------------------------
# Tests: build_vocab_block — sorted, dedented
# ---------------------------------------------------------------------------

class TestBuildVocabBlock(unittest.TestCase):
    def test_sorted(self):
        vocab = frozenset({"SERVES", "LOVES", "KILLS"})
        block = tc.build_vocab_block(vocab)
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        self.assertEqual(lines, sorted(lines))

    def test_all_vocab_in_block(self):
        vocab = frozenset({"SERVES", "LOVES", "KILLS"})
        block = tc.build_vocab_block(vocab)
        for t in vocab:
            self.assertIn(t, block)


if __name__ == "__main__":
    unittest.main()
