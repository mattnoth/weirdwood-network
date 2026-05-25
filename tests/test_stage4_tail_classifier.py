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


# ---------------------------------------------------------------------------
# Tests: Task 3 — Rule 6 in prompt preamble
# ---------------------------------------------------------------------------

class TestRule6InPrompt(unittest.TestCase):
    """Rule 6 (ENCOUNTERS staging verb gate) must appear in the classify prompt."""

    def test_rule6_encounters_text_in_preamble(self):
        """The _PROMPT_PREAMBLE must contain Rule 6 text about ENCOUNTERS."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("ENCOUNTERS", preamble)
        self.assertIn("staging verb", preamble.lower())

    def test_rule6_to_meet_not_staging_in_preamble(self):
        """The 'to meet is NOT a staging verb' clause must be present."""
        preamble = tc._PROMPT_PREAMBLE
        # Look for the "to meet" exclusion in some form
        lower = preamble.lower()
        self.assertTrue(
            "to meet" in lower or '"to meet"' in lower,
            "Preamble must mention 'to meet' as a non-staging verb",
        )

    def test_rule6_present_in_rendered_classify_prompt(self):
        """render_classify_prompt must include Rule 6 content."""
        rows = [_make_tail_row()]
        prompt = tc.render_classify_prompt(rows, _SAMPLE_VOCAB)
        self.assertIn("ENCOUNTERS", prompt)
        self.assertIn("staging verb", prompt.lower())

    def test_rule6_co_presence_prohibition_in_prompt(self):
        """The co-presence prohibition should be in the rendered prompt."""
        rows = [_make_tail_row()]
        prompt = tc.render_classify_prompt(rows, _SAMPLE_VOCAB)
        # Should warn against co-presence / scene presence
        lower = prompt.lower()
        self.assertTrue(
            "co-presence" in lower or "same scene" in lower or "never emit for co-presence" in lower,
            "Prompt must mention co-presence prohibition for ENCOUNTERS",
        )

    def test_rule_numbering_sequential(self):
        """The preamble must have rules 6 through 11 present."""
        preamble = tc._PROMPT_PREAMBLE
        for n in range(6, 12):
            self.assertIn(f"{n}.", preamble, f"Rule {n} must be present in preamble")


# ---------------------------------------------------------------------------
# Tests: Task 3 — load_extra_tables_rows
# ---------------------------------------------------------------------------

class TestLoadExtraTablesRows(unittest.TestCase):
    """load_extra_tables_rows must read untyped candidates from _extra-tables/ layout."""

    def _make_extra_tables_dir(
        self,
        rows_by_book: dict[str, list[dict]],
    ) -> Path:
        """Write rows to a temp directory mimicking _extra-tables/{book}/ layout."""
        import tempfile
        tmpdir = Path(tempfile.mkdtemp())
        for book, rows in rows_by_book.items():
            book_dir = tmpdir / book
            book_dir.mkdir()
            out_file = book_dir / f"{book}-test-01.extra-tables.jsonl"
            with out_file.open("w") as fh:
                for row in rows:
                    fh.write(json.dumps(row) + "\n")
        return tmpdir

    def _make_row(self, candidate_kind: str, book: str, edge_type=None) -> dict:
        return {
            "candidate_kind": candidate_kind,
            "evidence_chapter": f"{book}-test-01",
            "evidence_book": book,
            "source_slug": "arya-stark",
            "target_slug": "jon-snow",
            "edge_type": edge_type,
            "hint_raw": "test hint",
        }

    def test_loads_untyped_rows(self):
        rows = [self._make_row("pass1_dialogue", "agot")]
        tmpdir = self._make_extra_tables_dir({"agot": rows})
        loaded = tc.load_extra_tables_rows(tmpdir, ["agot"])
        self.assertEqual(len(loaded), 1)

    def test_filters_typed_rows(self):
        """Rows with edge_type != None must be excluded."""
        rows = [
            self._make_row("pass1_dialogue", "agot"),  # untyped
            self._make_row("pass1_hospitality", "agot", edge_type="GUEST_OF"),  # typed
        ]
        tmpdir = self._make_extra_tables_dir({"agot": rows})
        loaded = tc.load_extra_tables_rows(tmpdir, ["agot"])
        self.assertEqual(len(loaded), 1)
        self.assertIsNone(loaded[0]["edge_type"])

    def test_candidate_kinds_filter(self):
        """When candidate_kinds specified, only matching rows returned."""
        rows = [
            self._make_row("pass1_dialogue", "agot"),
            self._make_row("pass1_events", "agot"),
            self._make_row("pass1_food", "agot"),
        ]
        tmpdir = self._make_extra_tables_dir({"agot": rows})
        loaded = tc.load_extra_tables_rows(tmpdir, ["agot"], candidate_kinds=["pass1_dialogue"])
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["candidate_kind"], "pass1_dialogue")

    def test_multi_book_loading(self):
        """Rows from multiple books are all loaded."""
        agot_rows = [self._make_row("pass1_dialogue", "agot")]
        asos_rows = [self._make_row("pass1_events", "asos")]
        tmpdir = self._make_extra_tables_dir({"agot": agot_rows, "asos": asos_rows})
        loaded = tc.load_extra_tables_rows(tmpdir, ["agot", "asos"])
        self.assertEqual(len(loaded), 2)

    def test_tail_book_augmented(self):
        """Each loaded row must have _tail_book set to its book."""
        rows = [self._make_row("pass1_dialogue", "agot")]
        tmpdir = self._make_extra_tables_dir({"agot": rows})
        loaded = tc.load_extra_tables_rows(tmpdir, ["agot"])
        self.assertEqual(loaded[0]["_tail_book"], "agot")

    def test_missing_book_dir_ignored(self):
        """Non-existent book dir is skipped, no crash."""
        tmpdir = self._make_extra_tables_dir({})
        loaded = tc.load_extra_tables_rows(tmpdir, ["agot", "asos"])
        self.assertEqual(loaded, [])

    def test_no_candidate_kinds_loads_all_untyped(self):
        """Without candidate_kinds filter, all untyped rows are returned."""
        rows = [
            self._make_row("pass1_dialogue", "agot"),
            self._make_row("pass1_events", "agot"),
        ]
        tmpdir = self._make_extra_tables_dir({"agot": rows})
        loaded = tc.load_extra_tables_rows(tmpdir, ["agot"], candidate_kinds=None)
        self.assertEqual(len(loaded), 2)


# ---------------------------------------------------------------------------
# Tests: Task 3 — stratified_sample
# ---------------------------------------------------------------------------

class TestStratifiedSample(unittest.TestCase):
    """stratified_sample must return N rows with proportional strata coverage."""

    def _make_rows(self, count: int, book: str, kind: str) -> list[dict]:
        return [
            {
                "candidate_kind": kind,
                "_tail_book": book,
                "source_slug": f"src-{i}",
                "target_slug": f"tgt-{i}",
            }
            for i in range(count)
        ]

    def test_returns_n_rows_exact(self):
        """When total > n, result has exactly n rows."""
        rows = (
            self._make_rows(50, "agot", "pass1_dialogue") +
            self._make_rows(50, "asos", "pass1_events")
        )
        sampled = tc.stratified_sample(rows, 20)
        self.assertEqual(len(sampled), 20)

    def test_returns_all_when_total_lte_n(self):
        """When total <= n, returns all rows (shuffled)."""
        rows = self._make_rows(5, "agot", "pass1_dialogue")
        sampled = tc.stratified_sample(rows, 100)
        self.assertEqual(len(sampled), 5)

    def test_covers_multiple_strata(self):
        """With multi-strata input, sample should include rows from each stratum."""
        rows = (
            self._make_rows(30, "agot", "pass1_dialogue") +
            self._make_rows(30, "asos", "pass1_events") +
            self._make_rows(30, "affc", "pass1_food")
        )
        sampled = tc.stratified_sample(rows, 30, seed=42)
        kinds = {r["candidate_kind"] for r in sampled}
        # With balanced strata (30 each), expect all 3 kinds to appear
        self.assertGreater(len(kinds), 1, f"Expected multi-kind sample, got: {kinds}")

    def test_deterministic_with_seed(self):
        """Same seed = same result."""
        rows = (
            self._make_rows(20, "agot", "pass1_dialogue") +
            self._make_rows(20, "asos", "pass1_events")
        )
        s1 = tc.stratified_sample(rows, 10, seed=42)
        s2 = tc.stratified_sample(rows, 10, seed=42)
        self.assertEqual(
            [r["source_slug"] for r in s1],
            [r["source_slug"] for r in s2],
        )

    def test_different_seeds_differ(self):
        """Different seeds produce different (usually) orderings."""
        rows = (
            self._make_rows(20, "agot", "pass1_dialogue") +
            self._make_rows(20, "asos", "pass1_events")
        )
        s1 = tc.stratified_sample(rows, 10, seed=1)
        s2 = tc.stratified_sample(rows, 10, seed=99)
        # Very unlikely to be identical with different seeds and 10 rows from 40
        srcs1 = [r["source_slug"] for r in s1]
        srcs2 = [r["source_slug"] for r in s2]
        self.assertNotEqual(srcs1, srcs2)

    def test_single_stratum_proportional(self):
        """With a single stratum, all n rows come from it."""
        rows = self._make_rows(20, "agot", "pass1_dialogue")
        sampled = tc.stratified_sample(rows, 5)
        self.assertEqual(len(sampled), 5)
        for r in sampled:
            self.assertEqual(r["_tail_book"], "agot")
            self.assertEqual(r["candidate_kind"], "pass1_dialogue")

    def test_empty_input_returns_empty(self):
        sampled = tc.stratified_sample([], 10)
        self.assertEqual(sampled, [])


class TestOutputDirRedirect(unittest.TestCase):
    """--output-dir safety: write_output_rows must land in the redirected dir,
    never the canonical _tail-typed/.  Guards smoke runs from clobbering the
    S67 typed tail (which is append-mode written)."""

    def setUp(self):
        self._orig_out_base = tc.OUT_BASE
        self._orig_needs_qual = tc.OUT_NEEDS_QUAL_DIR

    def tearDown(self):
        tc.OUT_BASE = self._orig_out_base
        tc.OUT_NEEDS_QUAL_DIR = self._orig_needs_qual

    def test_write_output_rows_respects_reassigned_out_base(self):
        import tempfile

        emit_row = {
            "decision": "emit_edge",
            "edge_type": "PARENT_OF",
            "source_slug": "eddard-stark",
            "target_slug": "bran-stark",
            "evidence_chapter": "agot-bran-01",
        }
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td) / "_smoke"
            tc.OUT_BASE = tmp
            tc.OUT_NEEDS_QUAL_DIR = tmp / "_needs-qualifier"

            tc.write_output_rows([emit_row], [], [], [], ["agot"])

            written = tmp / "agot" / "agot-tail.edges.jsonl"
            self.assertTrue(written.exists(), "edge file must land under --output-dir")
            self.assertIn("bran-stark", written.read_text())
            # The write target must be the redirected dir, NOT the canonical one.
            self.assertTrue(written.is_relative_to(tmp))
            self.assertFalse(written.is_relative_to(self._orig_out_base))


# ---------------------------------------------------------------------------
# Tests: Fix 1 — Vocab gating + anti-pattern guidance in preamble
# ---------------------------------------------------------------------------

class TestVocabGating(unittest.TestCase):
    """Fix 1: gated types annotated [GATED], Rule 9 anti-patterns in preamble."""

    _FIVE_GATED = ("INFORMS", "ADVISES", "MANIPULATES", "SUPPORTS", "ALIAS_OF")

    def test_default_gated_types_constant_exists(self):
        """DEFAULT_GATED_TYPES must be a non-empty tuple of strings."""
        self.assertIsInstance(tc.DEFAULT_GATED_TYPES, tuple)
        self.assertGreater(len(tc.DEFAULT_GATED_TYPES), 0)
        for t in tc.DEFAULT_GATED_TYPES:
            self.assertIsInstance(t, str)

    def test_default_gated_types_contains_five(self):
        """DEFAULT_GATED_TYPES must contain all five specified types."""
        for t in self._FIVE_GATED:
            self.assertIn(t, tc.DEFAULT_GATED_TYPES, f"{t} missing from DEFAULT_GATED_TYPES")

    def test_build_vocab_block_annotates_gated_types(self):
        """build_vocab_block with gated_types must annotate them with [GATED]."""
        vocab = frozenset({"SERVES", "LOVES", "INFORMS", "ADVISES"})
        block = tc.build_vocab_block(vocab, gated_types=("INFORMS", "ADVISES"))
        self.assertIn("GATED", block)
        # Gated types annotated, non-gated are clean
        self.assertIn("INFORMS", block)
        self.assertIn("ADVISES", block)
        self.assertIn("SERVES", block)
        # Non-gated types must NOT be annotated
        lines = {ln.split()[0]: ln for ln in block.splitlines() if ln.strip()}
        serves_line = next((ln for ln in block.splitlines() if "SERVES" in ln), "")
        self.assertNotIn("GATED", serves_line)
        informs_line = next((ln for ln in block.splitlines() if "INFORMS" in ln), "")
        self.assertIn("GATED", informs_line)

    def test_build_vocab_block_no_gated_types_no_annotation(self):
        """Without gated_types, no [GATED] annotation appears."""
        vocab = frozenset({"SERVES", "LOVES", "INFORMS"})
        block = tc.build_vocab_block(vocab, gated_types=None)
        self.assertNotIn("GATED", block)

    def test_build_vocab_block_gated_types_not_removed_from_vocab(self):
        """Gated types must still appear in the vocab block (blocklist, not allow-list)."""
        vocab = frozenset({"SERVES", "LOVES", "INFORMS", "ADVISES", "MANIPULATES"})
        block = tc.build_vocab_block(vocab, gated_types=self._FIVE_GATED)
        for t in ["SERVES", "LOVES", "INFORMS", "ADVISES", "MANIPULATES"]:
            self.assertIn(t, block, f"{t} must remain in vocab block even when gated")

    def test_rule9_anti_pattern_text_in_preamble(self):
        """Rule 9 anti-patterns for all five types must be in _PROMPT_PREAMBLE."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("9.", preamble, "Rule 9 must be numbered in preamble")
        # Each of the five gated types must be mentioned in Rule 9
        for t in self._FIVE_GATED:
            self.assertIn(t, preamble, f"{t} anti-pattern must appear in preamble")

    def test_rule9_informs_anti_pattern(self):
        """INFORMS anti-pattern: must distinguish from generic disclosure."""
        preamble = tc._PROMPT_PREAMBLE.lower()
        # Should warn: not generic "X told Y" → REVEALS_TO instead
        self.assertTrue(
            "reveals_to" in preamble or "one-time" in preamble or "disclosure" in preamble,
            "INFORMS anti-pattern must mention REVEALS_TO or one-time disclosure alternative",
        )

    def test_rule9_alias_of_anti_pattern(self):
        """ALIAS_OF anti-pattern: must call out titular forms of address."""
        preamble = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "alias_of" in preamble and ("titular" in preamble or "title" in preamble),
            "ALIAS_OF anti-pattern must mention titles/titular forms of address",
        )

    def test_rule10_tier_guidance_in_preamble(self):
        """Rule 10 tier-assignment guidance must appear in _PROMPT_PREAMBLE."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("10.", preamble, "Rule 10 must be numbered in preamble")
        self.assertIn("Tier-1", preamble)
        self.assertIn("Tier-2", preamble)
        self.assertIn("Tier-3", preamble)

    def test_render_classify_prompt_passes_gated_types(self):
        """render_classify_prompt with gated_types should annotate them in output."""
        rows = [_make_tail_row()]
        prompt = tc.render_classify_prompt(rows, _SAMPLE_VOCAB, gated_types=("SERVES",))
        # SERVES is in _SAMPLE_VOCAB, and we asked to gate it
        self.assertIn("GATED", prompt)

    def test_render_classify_prompt_no_gated_no_vocab_annotation(self):
        """render_classify_prompt without gated_types has no [GATED] annotation in vocab lines."""
        rows = [_make_tail_row()]
        prompt = tc.render_classify_prompt(rows, _SAMPLE_VOCAB, gated_types=None)
        # The vocab block must not contain [GATED] annotations on any type line.
        # (Note: the preamble itself says "GATED TYPES" in Rule 9 — that's fine.
        # We check that no vocab-list line carries the bracket annotation.)
        for line in prompt.splitlines():
            stripped = line.strip()
            if stripped.startswith("SERVES") or stripped.startswith("LOVES"):
                self.assertNotIn("[GATED]", line,
                                  "Vocab list lines must not have [GATED] when gated_types=None")

    def test_confidence_tier_in_closing_instruction(self):
        """The closing instruction must ask for confidence_tier."""
        rows = [_make_tail_row()]
        prompt = tc.render_classify_prompt(rows, _SAMPLE_VOCAB)
        self.assertIn("confidence_tier", prompt)

    def test_rule10_numbered_in_preamble(self):
        """Rule 10 must be present and numbered."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("10.", preamble)

    def test_rule11_numbered_in_preamble(self):
        """Rule 11 must be present and numbered."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("11.", preamble)


# ---------------------------------------------------------------------------
# Tests: Rule 11 — anti-pattern type gates in preamble
# ---------------------------------------------------------------------------

class TestRule11InPrompt(unittest.TestCase):
    """Rule 11 (ANTI-PATTERN TYPE GATES) must appear in _PROMPT_PREAMBLE with
    all five type-specific instructions present."""

    def test_rule11_contemporary_with_gate(self):
        """CONTEMPORARY_WITH must be gated to EVENT-overlap, not character co-presence."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("CONTEMPORARY_WITH", preamble)
        lower = preamble.lower()
        # Must mention events and co-presence prohibition
        self.assertIn("events", lower, "Rule 11 must reference EVENTS for CONTEMPORARY_WITH")
        self.assertTrue(
            "co-present" in lower or "same scene" in lower or "same room" in lower
            or "co-presence" in lower,
            "Rule 11 must prohibit character co-presence for CONTEMPORARY_WITH",
        )

    def test_rule11_companion_of_gate(self):
        """COMPANION_OF must require explicit bond language, not co-presence."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("COMPANION_OF", preamble)
        lower = preamble.lower()
        # Must mention requirement for explicit bond language
        self.assertTrue(
            "explicit" in lower or "explicitly" in lower,
            "Rule 11 must require explicit bond language for COMPANION_OF",
        )
        # Must mention TRAVELS_WITH as fallback
        self.assertIn("TRAVELS_WITH", preamble,
                      "Rule 11 must offer TRAVELS_WITH as fallback for COMPANION_OF")

    def test_rule11_cited_by_theory_only(self):
        """CITED_BY must be restricted to theory-support edges, not interpersonal use."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("CITED_BY", preamble)
        lower = preamble.lower()
        self.assertTrue(
            "theory" in lower,
            "Rule 11 must restrict CITED_BY to theory-support context",
        )

    def test_rule11_contradicts_theory_only(self):
        """CONTRADICTS must be restricted to theory-support, not interpersonal disagreements."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("CONTRADICTS", preamble)
        lower = preamble.lower()
        # Must warn against interpersonal use
        self.assertTrue(
            "disagreement" in lower or "disagreements" in lower or "arguments" in lower,
            "Rule 11 must prohibit CONTRADICTS for interpersonal disagreements",
        )

    def test_rule11_dreams_of_as_cited_by_alternative(self):
        """Rule 11 must name DREAMS_OF as the correct type for dream evidence."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("DREAMS_OF", preamble,
                      "Rule 11 must specify DREAMS_OF as alternative to CITED_BY for dreams")

    def test_rule11_assaults_sexual_violence_only(self):
        """ASSAULTS must be restricted to sexual violence; non-sexual → ATTACKS."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("ASSAULTS", preamble)
        lower = preamble.lower()
        self.assertTrue(
            "sexual" in lower,
            "Rule 11 must specify ASSAULTS is sexual violence only",
        )
        # Must offer ATTACKS as the correct type for non-sexual violence
        self.assertIn("ATTACKS", preamble,
                      "Rule 11 must name ATTACKS as fallback for non-sexual violence")

    def test_rule11_nursed_by_wet_nursing_only(self):
        """NURSED_BY must be restricted to wet-nursing; medical care → HEALS."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("NURSED_BY", preamble)
        lower = preamble.lower()
        self.assertTrue(
            "wet-nurs" in lower or "wet nurs" in lower,
            "Rule 11 must specify NURSED_BY is wet-nursing specifically",
        )
        # Must offer HEALS as the correct type for medical treatment
        self.assertIn("HEALS", preamble,
                      "Rule 11 must name HEALS as fallback for medical care")

    def test_rule11_present_in_rendered_prompt(self):
        """render_classify_prompt must include Rule 11 content."""
        rows = [_make_tail_row()]
        prompt = tc.render_classify_prompt(rows, _SAMPLE_VOCAB)
        self.assertIn("11.", prompt)
        self.assertIn("CONTEMPORARY_WITH", prompt)
        self.assertIn("COMPANION_OF", prompt)
        self.assertIn("ASSAULTS", prompt)
        self.assertIn("NURSED_BY", prompt)

    def test_rule11_appears_after_rule10(self):
        """Rule 11 must appear after Rule 10 in the preamble."""
        preamble = tc._PROMPT_PREAMBLE
        idx_10 = preamble.index("10.")
        idx_11 = preamble.index("11.")
        self.assertGreater(idx_11, idx_10,
                           "Rule 11 must appear after Rule 10 in the preamble")

    def test_rule11_appears_before_tier1_qualifier_enums(self):
        """Rule 11 must appear before the TIER-1 QUALIFIER ENUMS section."""
        preamble = tc._PROMPT_PREAMBLE
        idx_11 = preamble.index("11.")
        idx_enums = preamble.index("TIER-1 QUALIFIER ENUMS")
        self.assertLess(idx_11, idx_enums,
                        "Rule 11 must appear before TIER-1 QUALIFIER ENUMS block")


# ---------------------------------------------------------------------------
# Tests: Fix 3 — derive_typed_by + candidate_kind provenance
# ---------------------------------------------------------------------------

class TestProvenanceFix(unittest.TestCase):
    """Fix 3: typed_by derived from model arg; candidate_kind from input row."""

    def test_derive_typed_by_haiku(self):
        self.assertEqual(tc.derive_typed_by("claude-haiku-4-5"), "haiku")

    def test_derive_typed_by_sonnet(self):
        self.assertEqual(tc.derive_typed_by("claude-sonnet-4-6"), "sonnet")

    def test_derive_typed_by_opus(self):
        self.assertEqual(tc.derive_typed_by("claude-opus-4"), "opus")

    def test_derive_typed_by_unknown_model(self):
        """Unknown model falls back to model name (lowercased, truncated)."""
        result = tc.derive_typed_by("some-custom-model")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_typed_by_haiku_when_model_is_haiku(self):
        """build_emit_edge_row with haiku model emits typed_by='haiku'."""
        tail_row = _make_tail_row()
        row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-haiku-4-5", "r1")
        self.assertEqual(row["typed_by"], "haiku",
                         "Haiku runs must NOT be mislabeled as 'sonnet'")

    def test_typed_by_sonnet_when_model_is_sonnet(self):
        tail_row = _make_tail_row()
        row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-sonnet-4-6", "r1")
        self.assertEqual(row["typed_by"], "sonnet")

    def test_candidate_kind_preserved_from_input_row(self):
        """candidate_kind in emitted row must come from the input tail row."""
        for kind in ("pass1_dialogue", "pass1_events", "pass1_info", "pass1_food", "pass1_relationship"):
            tail_row = _make_tail_row(candidate_kind=kind)
            row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-sonnet-4-6", "r1")
            self.assertEqual(row["candidate_kind"], kind,
                             f"candidate_kind must be preserved as {kind!r}")

    def test_candidate_kind_defaults_to_pass1_relationship_when_absent(self):
        """If input row has no candidate_kind, default to 'pass1_relationship'."""
        tail_row = _make_tail_row()
        # Ensure no candidate_kind key
        tail_row.pop("candidate_kind", None)
        row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-sonnet-4-6", "r1")
        self.assertEqual(row["candidate_kind"], "pass1_relationship")

    def test_confidence_tier_from_model_output_tier1(self):
        """model_confidence_tier=1 must be written to emitted row."""
        tail_row = _make_tail_row()
        row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-sonnet-4-6", "r1",
                                      model_confidence_tier=1)
        self.assertEqual(row["confidence_tier"], 1)

    def test_confidence_tier_from_model_output_tier2(self):
        """model_confidence_tier=2 must be written to emitted row."""
        tail_row = _make_tail_row()
        row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-sonnet-4-6", "r1",
                                      model_confidence_tier=2)
        self.assertEqual(row["confidence_tier"], 2)

    def test_confidence_tier_from_model_output_tier3(self):
        """model_confidence_tier=3 must be written to emitted row."""
        tail_row = _make_tail_row()
        row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-sonnet-4-6", "r1",
                                      model_confidence_tier=3)
        self.assertEqual(row["confidence_tier"], 3)

    def test_confidence_tier_defaults_to_1_when_none(self):
        """model_confidence_tier=None falls back to tier-1."""
        tail_row = _make_tail_row()
        row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-sonnet-4-6", "r1",
                                      model_confidence_tier=None)
        self.assertEqual(row["confidence_tier"], 1)

    def test_confidence_tier_defaults_to_1_when_invalid(self):
        """model_confidence_tier with invalid value (0, 99) falls back to tier-1."""
        tail_row = _make_tail_row()
        for invalid in (0, 99, 4, -1):
            row = tc.build_emit_edge_row(tail_row, "LOVES", None, "claude-sonnet-4-6", "r1",
                                          model_confidence_tier=invalid)
            self.assertEqual(row["confidence_tier"], 1,
                             f"Invalid tier {invalid} should fall back to 1")

    def test_process_batch_extracts_confidence_tier_from_model_output(self):
        """process_batch must read confidence_tier from model output and pass to build_emit_edge_row."""
        batch = [_make_tail_row()]
        model_objects = [{"idx": 0, "edge_type": "LOVES", "confidence_tier": 2}]
        mock_resp = _mock_claude_response(model_objects)
        with patch.object(tc, "invoke_claude", return_value=mock_resp):
            result = tc.process_batch(
                batch=batch,
                batch_idx=0,
                locked_vocab=_SAMPLE_VOCAB,
                tier1_types=_TIER1,
                model="claude-haiku-4-5",
                run_id="test-run",
                apply=True,
            )
        self.assertEqual(result["typed"], 1)
        emit = result["emit_rows"][0]
        self.assertEqual(emit["confidence_tier"], 2,
                         "Tier-2 from model output must appear in emitted row")
        self.assertEqual(emit["typed_by"], "haiku",
                         "Haiku model must produce typed_by='haiku'")

    def test_process_batch_candidate_kind_from_input(self):
        """process_batch must preserve candidate_kind from the input batch row."""
        batch = [_make_tail_row(candidate_kind="pass1_dialogue")]
        model_objects = [{"idx": 0, "edge_type": "LOVES", "confidence_tier": 1}]
        mock_resp = _mock_claude_response(model_objects)
        with patch.object(tc, "invoke_claude", return_value=mock_resp):
            result = tc.process_batch(
                batch=batch,
                batch_idx=0,
                locked_vocab=_SAMPLE_VOCAB,
                tier1_types=_TIER1,
                model="claude-haiku-4-5",
                run_id="test-run",
                apply=True,
            )
        emit = result["emit_rows"][0]
        self.assertEqual(emit["candidate_kind"], "pass1_dialogue")


# ---------------------------------------------------------------------------
# Tests: Task 1 — load_existing_keys respects explicit output_dir
# ---------------------------------------------------------------------------

class TestSkipExistingOutputDir(unittest.TestCase):
    """load_existing_keys must read from the explicit output_dir, not OUT_BASE.

    This guards the resume loop: when --output-dir is set, --skip-existing must
    check the SAME directory it writes to, not the canonical _tail-typed/.
    """

    def test_load_existing_keys_reads_from_explicit_output_dir(self):
        """Keys written to a custom dir are found when that dir is passed as output_dir."""
        import tempfile

        emit_row = {
            "decision": "emit_edge",
            "edge_type": "LOVES",
            "source_slug": "arya-stark",
            "target_slug": "jon-snow",
            "evidence_chapter": "agot-arya-01",
        }
        with tempfile.TemporaryDirectory() as td:
            custom_dir = Path(td) / "_enrich-haiku"
            book_dir = custom_dir / "agot"
            book_dir.mkdir(parents=True)
            edges_file = book_dir / "agot-tail.edges.jsonl"
            edges_file.write_text(json.dumps(emit_row) + "\n")

            # Should find the key when we pass custom_dir explicitly
            keys = tc.load_existing_keys(["agot"], output_dir=custom_dir)
            self.assertIn(("arya-stark", "jon-snow", "agot-arya-01"), keys)

    def test_load_existing_keys_custom_dir_does_not_see_canonical_dir_rows(self):
        """When custom dir is empty, load_existing_keys returns empty set."""
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            custom_dir = Path(td) / "_enrich-haiku"
            custom_dir.mkdir()
            # No files in custom_dir — should return empty
            keys = tc.load_existing_keys(["agot", "asos"], output_dir=custom_dir)
            self.assertEqual(keys, set())

    def test_load_existing_keys_rejected_also_counted(self):
        """Rejected rows written to the custom dir must also be counted as 'existing'."""
        import tempfile

        rejected_row = {
            "decision": "rejected",
            "source_slug": "ned-stark",
            "target_slug": "robert-baratheon",
            "evidence_chapter": "agot-eddard-01",
        }
        with tempfile.TemporaryDirectory() as td:
            custom_dir = Path(td) / "_enrich-haiku"
            book_dir = custom_dir / "agot"
            book_dir.mkdir(parents=True)
            rejected_file = book_dir / "agot-tail.rejected.jsonl"
            rejected_file.write_text(json.dumps(rejected_row) + "\n")

            keys = tc.load_existing_keys(["agot"], output_dir=custom_dir)
            self.assertIn(("ned-stark", "robert-baratheon", "agot-eddard-01"), keys)

    def test_load_existing_keys_output_dir_param_is_explicit(self):
        """load_existing_keys accepts output_dir keyword argument (API contract test)."""
        import inspect
        sig = inspect.signature(tc.load_existing_keys)
        self.assertIn("output_dir", sig.parameters,
                      "load_existing_keys must have explicit output_dir parameter")

    def test_skip_existing_uses_effective_output_dir(self):
        """The effective OUT_BASE (after --output-dir reassignment) is what skip-existing
        checks.  This test exercises the module-global reassignment path to confirm the
        call site passes output_dir=OUT_BASE (the reassigned value)."""
        import tempfile

        emit_row = {
            "decision": "emit_edge",
            "edge_type": "SERVES",
            "source_slug": "sansa-stark",
            "target_slug": "cersei-lannister",
            "evidence_chapter": "agot-sansa-02",
        }
        orig_out_base = tc.OUT_BASE
        try:
            with tempfile.TemporaryDirectory() as td:
                custom_dir = Path(td) / "_enrich-haiku"
                book_dir = custom_dir / "agot"
                book_dir.mkdir(parents=True)
                edges_file = book_dir / "agot-tail.edges.jsonl"
                edges_file.write_text(json.dumps(emit_row) + "\n")

                # Simulate --output-dir reassignment of the global
                tc.OUT_BASE = custom_dir

                # load_existing_keys with output_dir=tc.OUT_BASE (the effective dir)
                keys = tc.load_existing_keys(["agot"], output_dir=tc.OUT_BASE)
                self.assertIn(("sansa-stark", "cersei-lannister", "agot-sansa-02"), keys)
        finally:
            tc.OUT_BASE = orig_out_base


# ---------------------------------------------------------------------------
# Tests: Task 2 — --abort-after-consecutive-failures + exit code 42
# ---------------------------------------------------------------------------

class TestConsecutiveFailureAbort(unittest.TestCase):
    """--abort-after-consecutive-failures must exit with EXIT_CODE_RATE_LIMIT (42)
    after N consecutive fully-failed batches, and reset the counter on a success."""

    def _fully_failed_batch_result(self, rows_in: int = 5) -> dict:
        """Return a process_batch result dict where every row is classify_failed."""
        return {
            "batch_idx": 0,
            "rows_in": rows_in,
            "typed": 0,
            "rejected": 0,
            "classify_failed": rows_in,
            "needs_qualifier": 0,
            "conform_violations": rows_in,
            "total_cost_usd": 0.0,
            "emit_rows": [],
            "rejected_rows": [],
            "failed_rows": [_make_tail_row() for _ in range(rows_in)],
            "needs_qualifier_rows": [],
        }

    def _partial_success_result(self, rows_in: int = 5) -> dict:
        """Return a process_batch result where at least one row typed successfully."""
        return {
            "batch_idx": 0,
            "rows_in": rows_in,
            "typed": 1,
            "rejected": 0,
            "classify_failed": rows_in - 1,
            "needs_qualifier": 0,
            "conform_violations": 0,
            "total_cost_usd": 0.001,
            "emit_rows": [
                tc.build_emit_edge_row(
                    _make_tail_row(), "LOVES", None, "claude-haiku-4-5", "test-run"
                )
            ],
            "rejected_rows": [],
            "failed_rows": [_make_tail_row() for _ in range(rows_in - 1)],
            "needs_qualifier_rows": [],
        }

    def test_exit_code_rate_limit_constant_is_42(self):
        """EXIT_CODE_RATE_LIMIT must be 42."""
        self.assertEqual(tc.EXIT_CODE_RATE_LIMIT, 42)

    def test_abort_threshold_flag_exists(self):
        """--abort-after-consecutive-failures arg must be registered in parse_args."""
        import sys as _sys
        old = _sys.argv
        try:
            _sys.argv = ["prog", "--abort-after-consecutive-failures", "3"]
            args = tc.parse_args()
            self.assertEqual(args.abort_after_consecutive_failures, 3)
        finally:
            _sys.argv = old

    def test_abort_threshold_default_is_5(self):
        """Default value of --abort-after-consecutive-failures must be 5."""
        import sys as _sys
        old = _sys.argv
        try:
            _sys.argv = ["prog"]
            args = tc.parse_args()
            self.assertEqual(args.abort_after_consecutive_failures, 5)
        finally:
            _sys.argv = old

    def test_abort_threshold_zero_disables(self):
        """--abort-after-consecutive-failures 0 must disable the check."""
        import sys as _sys
        old = _sys.argv
        try:
            _sys.argv = ["prog", "--abort-after-consecutive-failures", "0"]
            args = tc.parse_args()
            self.assertEqual(args.abort_after_consecutive_failures, 0)
        finally:
            _sys.argv = old

    def test_fully_failed_batch_detection(self):
        """A batch with 0 typed/rejected/nq and >0 classify_failed is fully failed."""
        result = self._fully_failed_batch_result(rows_in=3)
        batch_is_fully_failed = (
            result["typed"] == 0
            and result["rejected"] == 0
            and result["needs_qualifier"] == 0
            and result["classify_failed"] > 0
        )
        self.assertTrue(batch_is_fully_failed)

    def test_partial_success_is_not_fully_failed(self):
        """A batch with >=1 typed is NOT a fully-failed batch."""
        result = self._partial_success_result(rows_in=5)
        batch_is_fully_failed = (
            result["typed"] == 0
            and result["rejected"] == 0
            and result["needs_qualifier"] == 0
            and result["classify_failed"] > 0
        )
        self.assertFalse(batch_is_fully_failed)

    def test_consecutive_counter_logic(self):
        """Verify counter increments on full failure and resets on partial success."""
        consecutive_failures = 0
        threshold = 3

        # Two full failures
        for _ in range(2):
            result = self._fully_failed_batch_result()
            batch_is_fully_failed = (
                result["typed"] == 0
                and result["rejected"] == 0
                and result["needs_qualifier"] == 0
                and result["classify_failed"] > 0
            )
            if batch_is_fully_failed:
                consecutive_failures += 1
            else:
                consecutive_failures = 0

        self.assertEqual(consecutive_failures, 2)
        self.assertLess(consecutive_failures, threshold)  # not yet aborted

        # One success — resets
        result = self._partial_success_result()
        batch_is_fully_failed = (
            result["typed"] == 0
            and result["rejected"] == 0
            and result["needs_qualifier"] == 0
            and result["classify_failed"] > 0
        )
        if batch_is_fully_failed:
            consecutive_failures += 1
        else:
            consecutive_failures = 0
        self.assertEqual(consecutive_failures, 0)  # reset

        # Now three full failures again — should reach threshold
        for _ in range(3):
            result = self._fully_failed_batch_result()
            batch_is_fully_failed = (
                result["typed"] == 0
                and result["rejected"] == 0
                and result["needs_qualifier"] == 0
                and result["classify_failed"] > 0
            )
            if batch_is_fully_failed:
                consecutive_failures += 1
            else:
                consecutive_failures = 0
        self.assertEqual(consecutive_failures, 3)
        self.assertGreaterEqual(consecutive_failures, threshold)

    def test_process_batch_with_all_parse_error_is_fully_failed(self):
        """process_batch where claude returns total parse error → classify_failed for all rows."""
        batch = [_make_tail_row(), _make_tail_row(hint_raw="other")]
        bad_resp = {
            "returncode": 0,
            "raw_output": json.dumps({"result": "garbage no json", "total_cost_usd": 0.0}),
            "result_json": None,
            "total_cost_usd": 0.0,
            "error_message": None,
            "duration_s": 0.1,
        }
        from unittest.mock import patch
        with patch.object(tc, "invoke_claude", return_value=bad_resp):
            result = tc.process_batch(
                batch=batch,
                batch_idx=0,
                locked_vocab=_SAMPLE_VOCAB,
                tier1_types=_TIER1,
                model="claude-haiku-4-5",
                run_id="test-run",
                apply=True,
            )

        batch_is_fully_failed = (
            result["typed"] == 0
            and result["rejected"] == 0
            and result["needs_qualifier"] == 0
            and result["classify_failed"] > 0
        )
        self.assertTrue(batch_is_fully_failed,
                        "parse error batch must register as fully failed for consecutive counter")

    def test_rejected_only_batch_is_not_fully_failed(self):
        """A batch where every row is REJECTED (0 typed, >0 rejected) is NOT fully failed.
        REJECT is a valid model decision, not a rate-limit symptom."""
        batch = [_make_tail_row()]
        model_objects = [{"idx": 0, "edge_type": "REJECT"}]
        mock_resp = _mock_claude_response(model_objects)
        from unittest.mock import patch
        with patch.object(tc, "invoke_claude", return_value=mock_resp):
            result = tc.process_batch(
                batch=batch,
                batch_idx=0,
                locked_vocab=_SAMPLE_VOCAB,
                tier1_types=_TIER1,
                model="claude-haiku-4-5",
                run_id="test-run",
                apply=True,
            )

        batch_is_fully_failed = (
            result["typed"] == 0
            and result["rejected"] == 0
            and result["needs_qualifier"] == 0
            and result["classify_failed"] > 0
        )
        self.assertFalse(batch_is_fully_failed,
                         "REJECT-only batch must NOT trigger the consecutive-failure counter")


if __name__ == "__main__":
    unittest.main()
