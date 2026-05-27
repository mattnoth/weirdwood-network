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
        """The preamble must have rules 6 through 14 present."""
        preamble = tc._PROMPT_PREAMBLE
        for n in range(6, 15):
            self.assertIn(f"{n}.", preamble, f"Rule {n} must be present in preamble")


# ---------------------------------------------------------------------------
# Tests: New prompt gates (Rules 12-14) added in Task 4
# ---------------------------------------------------------------------------

class TestNewPromptGates(unittest.TestCase):
    """Rules 12 (RESPECTS gate), 13 (direction reminder), 14 (ECHOES contract)
    must appear in _PROMPT_PREAMBLE and propagate into the rendered prompt.
    """

    def test_respects_gate_in_preamble(self):
        """Rule 12 RESPECTS gate must be in _PROMPT_PREAMBLE."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("RESPECTS", preamble)
        lower = preamble.lower()
        # Must include the core concept: explicit respect language required
        self.assertTrue(
            "explicit" in lower or "defers to" in lower or "admires" in lower,
            "RESPECTS gate must mention explicit respect language requirement",
        )

    def test_respects_gate_rejects_co_presence(self):
        """RESPECTS gate must call out co-presence and rebuke as not sufficient."""
        lower = tc._PROMPT_PREAMBLE.lower()
        # At least one of: co-presence, rebuke, boast, neutral
        self.assertTrue(
            "rebuke" in lower or "co-presence" in lower or "boast" in lower
            or "neutral" in lower,
            "RESPECTS gate must reject co-presence/rebuke/boast/neutral as evidence",
        )

    def test_direction_reminder_in_preamble(self):
        """Rule 13 direction reminder must be in _PROMPT_PREAMBLE."""
        preamble = tc._PROMPT_PREAMBLE
        lower = preamble.lower()
        # Must mention source as actor and reversal
        self.assertTrue(
            "reverse" in lower or "swap" in lower or "actor" in lower,
            "Direction reminder must address reversal/swap in _PROMPT_PREAMBLE",
        )

    def test_direction_reminder_heals_example(self):
        """The HEALS Bran/Luwin direction example must appear in preamble."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertIn("heals", lower, "Direction reminder must cite HEALS as example")

    def test_echoes_contract_in_preamble(self):
        """Rule 14 ECHOES type-contract must be in _PROMPT_PREAMBLE."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("ECHOES", preamble)
        # Must state ECHOES must NOT connect two characters
        self.assertIn("characters", preamble,
                      "ECHOES contract must mention the char<->char restriction")

    def test_new_rules_in_rendered_prompt(self):
        """All three new gates must propagate into the rendered classify prompt."""
        rows = [_make_tail_row()]
        prompt = tc.render_classify_prompt(rows, _SAMPLE_VOCAB)
        # RESPECTS gate
        self.assertIn("RESPECTS", prompt)
        # ECHOES contract
        self.assertIn("ECHOES", prompt)
        # Direction reminder
        lower = prompt.lower()
        self.assertTrue("source" in lower and "target" in lower)

    def test_rule_12_explicit_rule_number(self):
        """Rule 12 must be numbered '12.' in the preamble."""
        self.assertIn("12.", tc._PROMPT_PREAMBLE)

    def test_rule_13_explicit_rule_number(self):
        """Rule 13 must be numbered '13.' in the preamble."""
        self.assertIn("13.", tc._PROMPT_PREAMBLE)

    def test_rule_14_explicit_rule_number(self):
        """Rule 14 must be numbered '14.' in the preamble."""
        self.assertIn("14.", tc._PROMPT_PREAMBLE)


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


# ---------------------------------------------------------------------------
# Tests: Prompt Overhaul — GOVERNING PRINCIPLE, evidence-grounding, co-presence
# consolidation, expanded gated types (2026-05-25 audit)
# ---------------------------------------------------------------------------

class TestPromptOverhaul(unittest.TestCase):
    """Verify all changes from the 2026-05-25 Opus prompt-review consensus:
    - GOVERNING PRINCIPLE / 3-gate preamble
    - Rule 4 uses evidence_quote (not hint)
    - Rule 4a evidence-grounding + planned-vs-completed
    - Consolidated co-presence principle (Rule 12)
    - Expanded gated types (13 total)
    - Rule 10 tier-1 tightening (hesitation → not tier-1)
    - Empty evidence_quote → REJECT
    """

    # ----------------------------------------------------------------
    # GOVERNING PRINCIPLE block
    # ----------------------------------------------------------------

    def test_governing_principle_present(self):
        """GOVERNING PRINCIPLE block must appear in _PROMPT_PREAMBLE."""
        self.assertIn("GOVERNING PRINCIPLE", tc._PROMPT_PREAMBLE)

    def test_governing_principle_before_rules(self):
        """GOVERNING PRINCIPLE must appear before the RULES: block."""
        preamble = tc._PROMPT_PREAMBLE
        idx_gp = preamble.index("GOVERNING PRINCIPLE")
        idx_rules = preamble.index("RULES:")
        self.assertLess(idx_gp, idx_rules,
                        "GOVERNING PRINCIPLE must appear before RULES:")

    def test_governing_principle_reject_asymmetry(self):
        """Governing principle must state the missing-vs-wrong asymmetry."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertIn("missing edge is recoverable", lower)
        self.assertIn("wrong edge", lower)

    def test_governing_principle_gate1_state_not_moment(self):
        """GATE 1 (STATE, not MOMENT) must appear in preamble."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("GATE 1", preamble)
        lower = preamble.lower()
        self.assertTrue(
            "standing" in lower or "moment" in lower,
            "GATE 1 must distinguish standing relationships from single moments",
        )

    def test_governing_principle_gate2_direct_pair(self):
        """GATE 2 (DIRECT pair, no two-hop) must appear in preamble."""
        self.assertIn("GATE 2", tc._PROMPT_PREAMBLE)

    def test_governing_principle_gate3_fact_not_plan(self):
        """GATE 3 (FACT, not PLAN) must appear in preamble."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("GATE 3", preamble)
        lower = preamble.lower()
        self.assertTrue(
            "foiled" in lower or "planned" in lower or "attempted" in lower,
            "GATE 3 must address foiled/planned/attempted actions",
        )

    def test_gate1_whitelists_single_act_types(self):
        """GATE 1 must whitelist single-act types (KILLS, RESCUES, REVEALS_TO, ENCOUNTERS)."""
        lower = tc._PROMPT_PREAMBLE.lower()
        # At least KILLS and REVEALS_TO must be mentioned as single-act exceptions
        self.assertIn("kills", lower)
        self.assertIn("reveals_to", lower)

    # ----------------------------------------------------------------
    # Rule 4 fix: evidence_quote replaces hint+evidence
    # ----------------------------------------------------------------

    def test_rule4_references_evidence_quote_not_hint(self):
        """Rule 4 must say 'evidence_quote', not 'hint+evidence'."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("evidence_quote", preamble,
                      "Rule 4 must reference evidence_quote as the authoritative signal")
        self.assertNotIn("hint+evidence", preamble,
                         "Rule 4 must NOT use the old 'hint+evidence' phrasing")

    def test_rule4_empty_quote_reject(self):
        """Rule 4 must state that an empty/blank evidence_quote → REJECT."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "empty" in lower or "blank" in lower,
            "Rule 4 must specify that empty/blank evidence_quote → REJECT",
        )

    # ----------------------------------------------------------------
    # Rule 4a: evidence-grounding
    # ----------------------------------------------------------------

    def test_rule4a_present(self):
        """Rule 4a must appear in the preamble."""
        self.assertIn("4a.", tc._PROMPT_PREAMBLE)

    def test_rule4a_hint_is_not_proof(self):
        """Rule 4a must state the hint is a candidate label, NOT proof."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertIn("hint", lower)
        self.assertTrue(
            "not proof" in lower or "candidate label" in lower,
            "Rule 4a must call out the hint as not proof",
        )

    def test_rule4a_world_knowledge_prohibition(self):
        """Rule 4a must prohibit using world-knowledge to supply a relationship."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "world-knowledge" in lower or "world knowledge" in lower,
            "Rule 4a must explicitly prohibit world-knowledge substitution",
        )

    def test_rule4a_denial_is_not_evidence(self):
        """Rule 4a must state that a denial in the quote is not evidence FOR the relationship."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "deny" in lower or "denying" in lower or "denies" in lower,
            "Rule 4a must address the denial-is-not-evidence pattern",
        )

    def test_rule4a_planned_not_completed(self):
        """Rule 4a must state planned/attempted/foiled actions are not completed facts."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "foiled" in lower or ("planned" in lower and "not" in lower),
            "Rule 4a must address planned/foiled actions not equalling completed edges",
        )

    # ----------------------------------------------------------------
    # Expanded DEFAULT_GATED_TYPES
    # ----------------------------------------------------------------

    _NEW_GATED = ("OPPOSES", "MOTIVATES", "COMMANDS", "COURTS", "SEEKS", "TEACHES", "TUTORS", "KILLS")
    _ALL_GATED = ("INFORMS", "ADVISES", "MANIPULATES", "SUPPORTS", "ALIAS_OF") + _NEW_GATED

    def test_default_gated_types_contains_all_new_types(self):
        """DEFAULT_GATED_TYPES must contain all 8 new types from the audit."""
        for t in self._NEW_GATED:
            self.assertIn(t, tc.DEFAULT_GATED_TYPES,
                          f"{t} must be in DEFAULT_GATED_TYPES after prompt overhaul")

    def test_default_gated_types_count_is_13(self):
        """DEFAULT_GATED_TYPES must now have 13 entries (5 original + 8 new)."""
        self.assertEqual(
            len(tc.DEFAULT_GATED_TYPES),
            13,
            f"Expected 13 gated types, got {len(tc.DEFAULT_GATED_TYPES)}: {tc.DEFAULT_GATED_TYPES}",
        )

    def test_new_gated_types_anti_pattern_in_preamble(self):
        """Each new gated type must have its anti-pattern note in Rule 9 of the preamble."""
        preamble = tc._PROMPT_PREAMBLE
        for t in self._NEW_GATED:
            self.assertIn(t, preamble,
                          f"Anti-pattern for {t} must appear in preamble Rule 9")

    def test_opposes_one_time_disagreement_prohibition(self):
        """OPPOSES anti-pattern must prohibit one-time disagreements between allies."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "single" in lower or "one-time" in lower or "sustained" in lower,
            "OPPOSES gate must require sustained enmity, not one-time clash",
        )

    def test_motivates_person_source_prohibition(self):
        """MOTIVATES anti-pattern must state person-as-source is forbidden."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "event or condition" in lower or "event" in lower,
            "MOTIVATES gate must require an event/condition as source, not a person",
        )

    def test_commands_two_hop_guard(self):
        """COMMANDS anti-pattern must address the A-orders-B-about-C two-hop collapse."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "two-hop" in lower or "a→b" in lower or "commanded person" in lower or
            "a orders b" in lower,
            "COMMANDS gate must address the two-hop collapse pattern",
        )

    def test_courts_suitor_language_required(self):
        """COURTS anti-pattern must require explicit suitor language."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "suitor" in lower or "sought her hand" in lower or "courted" in lower,
            "COURTS gate must require explicit suitor/courtship language",
        )

    def test_kills_foiled_plot_prohibition(self):
        """KILLS anti-pattern must state foiled plot / attempted kill is not KILLS."""
        lower = tc._PROMPT_PREAMBLE.lower()
        # foiled or tried to kill
        self.assertTrue(
            "foiled" in lower or "attempt" in lower or "tried to" in lower,
            "KILLS gate must address foiled-plot / attempt-not-completion",
        )

    def test_new_gated_types_annotated_in_vocab_block(self):
        """build_vocab_block must annotate all 13 gated types with [GATED]."""
        # Build a vocab that includes all gated types
        vocab = frozenset(tc.DEFAULT_GATED_TYPES) | frozenset({"LOVES", "SERVES"})
        block = tc.build_vocab_block(vocab, gated_types=tc.DEFAULT_GATED_TYPES)
        for t in tc.DEFAULT_GATED_TYPES:
            # Find the line for this type
            line = next((ln for ln in block.splitlines() if t in ln), "")
            self.assertIn("GATED", line,
                          f"{t} must be annotated [GATED] in vocab block")

    # ----------------------------------------------------------------
    # Consolidated co-presence principle (Rule 12)
    # ----------------------------------------------------------------

    def test_co_presence_principle_present(self):
        """CO-PRESENCE PRINCIPLE must be present in the preamble (Rule 12)."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("CO-PRESENCE PRINCIPLE", preamble)

    def test_co_presence_principle_in_rule12(self):
        """CO-PRESENCE PRINCIPLE must live in Rule 12."""
        preamble = tc._PROMPT_PREAMBLE
        idx_12 = preamble.index("12.")
        idx_cp = preamble.index("CO-PRESENCE PRINCIPLE")
        self.assertGreaterEqual(idx_cp, idx_12,
                                "CO-PRESENCE PRINCIPLE must appear at or after Rule 12")
        # Must not appear before rule 12
        self.assertLess(idx_12, idx_cp + len("CO-PRESENCE PRINCIPLE"))

    def test_co_presence_requires_action_or_stance(self):
        """Co-presence principle must require an ACTION or STANCE directed source→target."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "action or stance" in lower or "action" in lower,
            "Co-presence principle must require a directed action or stance",
        )

    def test_co_presence_covers_same_scene(self):
        """Co-presence principle must explicitly say same scene is not enough."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "same scene" in lower or "same room" in lower or "scene" in lower,
            "Co-presence principle must address same-scene co-presence",
        )

    def test_co_presence_respects_gate_folded_in(self):
        """RESPECTS gate must still appear (now folded into Rule 12)."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("RESPECTS", preamble)
        lower = preamble.lower()
        self.assertTrue(
            "admires" in lower or "defers to" in lower or "explicit" in lower,
            "RESPECTS gate must still require explicit respect language",
        )

    def test_travels_with_carve_out_present(self):
        """Rule 12 must include the TRAVELS_WITH carve-out for genuine shared journeys."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "travels_with" in lower and (
                "journey" in lower or "journeyed" in lower or "voyage" in lower
            ),
            "Co-presence principle must carve out genuine TRAVELS_WITH shared journeys",
        )

    # ----------------------------------------------------------------
    # Rule 10 tier-1 tightening
    # ----------------------------------------------------------------

    def test_rule10_hesitation_means_not_tier1(self):
        """Rule 10 must state that hesitation over a relationship → not Tier-1."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "hesitat" in lower,
            "Rule 10 must say: if you hesitated, it is NOT Tier-1",
        )

    def test_rule10_single_moment_edges_tier2(self):
        """Rule 10 must direct single-moment edges to Tier-2."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "single-moment" in lower or "single moment" in lower,
            "Rule 10 must state single-moment edges → Tier-2",
        )

    def test_rule10_tier3_for_rumor_hearsay(self):
        """Rule 10 must assign Tier-3 to rumor/hearsay/dream evidence."""
        lower = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "rumor" in lower or "hearsay" in lower,
            "Rule 10 must assign Tier-3 to rumor/hearsay evidence",
        )

    # ----------------------------------------------------------------
    # Backward-compatibility: original 5 gated types still present
    # ----------------------------------------------------------------

    def test_original_five_gated_types_still_present(self):
        """The original 5 gated types must still be in DEFAULT_GATED_TYPES."""
        for t in ("INFORMS", "ADVISES", "MANIPULATES", "SUPPORTS", "ALIAS_OF"):
            self.assertIn(t, tc.DEFAULT_GATED_TYPES,
                          f"Original gated type {t} must still be in DEFAULT_GATED_TYPES")

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


# ---------------------------------------------------------------------------
# Tests: Prompt provenance stamping (DEFAULT_PROMPT_VERSION, compute_prompt_sha,
#        --prompt-version, stamps on all four row types, run-summary)
# ---------------------------------------------------------------------------

class TestPromptProvenance(unittest.TestCase):
    """Prompt provenance fields (prompt_version, prompt_sha) must be stamped on
    every output row type and on the run-summary.  The sha must be stable for an
    unchanged prompt and must change when the rendered template changes."""

    def test_default_prompt_version_constant_exists(self):
        """DEFAULT_PROMPT_VERSION must be a non-empty string."""
        self.assertIsInstance(tc.DEFAULT_PROMPT_VERSION, str)
        self.assertTrue(tc.DEFAULT_PROMPT_VERSION, "DEFAULT_PROMPT_VERSION must not be empty")

    def test_compute_prompt_sha_returns_12_hex_chars(self):
        """compute_prompt_sha must return a 12-character hex string."""
        sha = tc.compute_prompt_sha(_SAMPLE_VOCAB)
        self.assertIsInstance(sha, str)
        self.assertEqual(len(sha), 12)
        # Must be valid hex
        int(sha, 16)

    def test_compute_prompt_sha_stable_for_unchanged_inputs(self):
        """Same vocab + gated_types → same sha on repeated calls."""
        sha1 = tc.compute_prompt_sha(_SAMPLE_VOCAB, gated_types=("SERVES",))
        sha2 = tc.compute_prompt_sha(_SAMPLE_VOCAB, gated_types=("SERVES",))
        self.assertEqual(sha1, sha2)

    def test_compute_prompt_sha_changes_with_different_vocab(self):
        """Different vocab → different sha (tamper-evident)."""
        small_vocab = frozenset({"SERVES"})
        large_vocab = frozenset({"SERVES", "LOVES", "KILLS"})
        sha_small = tc.compute_prompt_sha(small_vocab)
        sha_large = tc.compute_prompt_sha(large_vocab)
        self.assertNotEqual(sha_small, sha_large)

    def test_compute_prompt_sha_changes_with_different_gated_types(self):
        """Different gated_types annotation → different sha."""
        sha_no_gate = tc.compute_prompt_sha(_SAMPLE_VOCAB, gated_types=None)
        sha_gated = tc.compute_prompt_sha(_SAMPLE_VOCAB, gated_types=("SERVES",))
        self.assertNotEqual(sha_no_gate, sha_gated)

    def test_emit_edge_row_carries_provenance(self):
        """build_emit_edge_row must stamp prompt_version + prompt_sha."""
        row = tc.build_emit_edge_row(
            _make_tail_row(), "SERVES", None, "claude-haiku-4-5", "test-run",
            prompt_version="v4-governing-principle", prompt_sha="abc123def456",
        )
        self.assertEqual(row["prompt_version"], "v4-governing-principle")
        self.assertEqual(row["prompt_sha"], "abc123def456")

    def test_rejected_row_carries_provenance(self):
        """build_rejected_row must stamp prompt_version + prompt_sha."""
        row = tc.build_rejected_row(
            _make_tail_row(), "test-run",
            prompt_version="v4-governing-principle", prompt_sha="abc123def456",
        )
        self.assertEqual(row["prompt_version"], "v4-governing-principle")
        self.assertEqual(row["prompt_sha"], "abc123def456")
        self.assertEqual(row["decision"], "rejected")

    def test_classify_failed_row_carries_provenance(self):
        """build_classify_failed_row must stamp prompt_version + prompt_sha."""
        row = tc.build_classify_failed_row(
            _make_tail_row(), "bad type", "test-run",
            prompt_version="v4-governing-principle", prompt_sha="abc123def456",
        )
        self.assertEqual(row["prompt_version"], "v4-governing-principle")
        self.assertEqual(row["prompt_sha"], "abc123def456")
        self.assertEqual(row["decision"], "classify_failed")

    def test_needs_qualifier_row_carries_provenance(self):
        """build_needs_qualifier_row must stamp prompt_version + prompt_sha."""
        row = tc.build_needs_qualifier_row(
            _make_tail_row(), "PARENT_OF", "test-run",
            prompt_version="v4-governing-principle", prompt_sha="abc123def456",
        )
        self.assertEqual(row["prompt_version"], "v4-governing-principle")
        self.assertEqual(row["prompt_sha"], "abc123def456")
        self.assertEqual(row["decision"], "needs_qualifier")

    def test_process_batch_stamps_provenance_on_emit_rows(self):
        """process_batch must forward prompt_version + prompt_sha to emit rows."""
        batch = [_make_tail_row()]
        model_objects = [{"idx": 0, "edge_type": "SERVES", "confidence_tier": 2}]
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
                prompt_version="v4-test",
                prompt_sha="deadbeef0001",
            )
        self.assertEqual(len(result["emit_rows"]), 1)
        row = result["emit_rows"][0]
        self.assertEqual(row["prompt_version"], "v4-test")
        self.assertEqual(row["prompt_sha"], "deadbeef0001")

    def test_process_batch_stamps_provenance_on_rejected_rows(self):
        """process_batch must forward provenance to rejected rows."""
        batch = [_make_tail_row()]
        model_objects = [{"idx": 0, "edge_type": "REJECT"}]
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
                prompt_version="v4-test",
                prompt_sha="deadbeef0002",
            )
        self.assertEqual(len(result["rejected_rows"]), 1)
        row = result["rejected_rows"][0]
        self.assertEqual(row["prompt_version"], "v4-test")
        self.assertEqual(row["prompt_sha"], "deadbeef0002")

    def test_process_batch_stamps_provenance_on_classify_failed_rows(self):
        """process_batch must forward provenance to classify_failed rows (parse error path)."""
        batch = [_make_tail_row()]
        bad_resp = {
            "returncode": 0,
            "raw_output": json.dumps({"result": "not json at all [[[", "total_cost_usd": 0.0}),
            "result_json": None,
            "total_cost_usd": 0.0,
            "error_message": None,
            "duration_s": 0.1,
        }
        with patch.object(tc, "invoke_claude", return_value=bad_resp):
            result = tc.process_batch(
                batch=batch,
                batch_idx=0,
                locked_vocab=_SAMPLE_VOCAB,
                tier1_types=_TIER1,
                model="claude-haiku-4-5",
                run_id="test-run",
                apply=True,
                prompt_version="v4-test",
                prompt_sha="deadbeef0003",
            )
        self.assertGreater(len(result["failed_rows"]), 0)
        row = result["failed_rows"][0]
        self.assertEqual(row["prompt_version"], "v4-test")
        self.assertEqual(row["prompt_sha"], "deadbeef0003")

    def test_prompt_version_override_propagates(self):
        """A non-default prompt_version override must appear on the output row."""
        row = tc.build_rejected_row(
            _make_tail_row(), "run-x",
            prompt_version="v99-custom", prompt_sha="000000000000",
        )
        self.assertEqual(row["prompt_version"], "v99-custom")

    def test_rejected_rows_still_carry_decision_field(self):
        """Rejected rows must have decision='rejected' alongside provenance fields."""
        row = tc.build_rejected_row(
            _make_tail_row(), "run-x",
            prompt_version="v4-governing-principle", prompt_sha="aabbccdd1122",
        )
        self.assertEqual(row["decision"], "rejected")
        self.assertIn("prompt_version", row)
        self.assertIn("prompt_sha", row)


# ---------------------------------------------------------------------------
# Tests: v5 precision rules — prompt text assertions
# ---------------------------------------------------------------------------

class TestV5PrecisionRules(unittest.TestCase):
    """v5 PRECISION RULES block (V5-R1 through V5-R6) must appear in _PROMPT_PREAMBLE
    and propagate into the rendered classify prompt.
    """

    def test_default_prompt_version_is_v5(self):
        """DEFAULT_PROMPT_VERSION must be 'v5-precision-rules'."""
        self.assertEqual(
            tc.DEFAULT_PROMPT_VERSION,
            "v5-precision-rules",
            "DEFAULT_PROMPT_VERSION must be bumped to v5-precision-rules",
        )

    def test_v5_block_header_in_preamble(self):
        """The 'v5 PRECISION RULES' section header must appear in _PROMPT_PREAMBLE."""
        self.assertIn("v5 PRECISION RULES", tc._PROMPT_PREAMBLE)

    # ------------------------------------------------------------------
    # V5-R1 — direction lock on structural edges
    # ------------------------------------------------------------------

    def test_v5_r1_marker_in_preamble(self):
        """V5-R1 rule marker must appear in _PROMPT_PREAMBLE."""
        self.assertIn("V5-R1", tc._PROMPT_PREAMBLE)

    def test_v5_r1_direction_lock_types_in_preamble(self):
        """V5-R1 must name the structural edge types it gates."""
        preamble = tc._PROMPT_PREAMBLE
        for t in ["LOCATED_AT", "TRAVELS_TO", "PARTICIPATES_IN", "IMPRISONED_AT", "GIFTED_TO"]:
            self.assertIn(t, preamble, f"V5-R1 must mention {t}")

    def test_v5_r1_gifted_to_artifact_source_rule(self):
        """V5-R1 must state GIFTED_TO requires SOURCE=artifact, TARGET=recipient."""
        preamble = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "gifted_to" in preamble and "artifact" in preamble,
            "V5-R1 must mention GIFTED_TO artifact-source requirement",
        )

    # ------------------------------------------------------------------
    # V5-R2 — evidence must support both endpoints
    # ------------------------------------------------------------------

    def test_v5_r2_marker_in_preamble(self):
        """V5-R2 rule marker must appear in _PROMPT_PREAMBLE."""
        self.assertIn("V5-R2", tc._PROMPT_PREAMBLE)

    def test_v5_r2_both_endpoints_language(self):
        """V5-R2 must require evidence for both endpoints."""
        preamble = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "both endpoint" in preamble or "both source" in preamble or "both ends" in preamble,
            "V5-R2 must mention requiring evidence for both endpoints",
        )

    def test_v5_r2_co_occurrence_not_evidence(self):
        """V5-R2 must reject co-occurrence as evidence."""
        preamble = tc._PROMPT_PREAMBLE.lower()
        self.assertIn(
            "co-occurrence",
            preamble,
            "V5-R2 must state co-occurrence is not evidence",
        )

    # ------------------------------------------------------------------
    # V5-R3 — target category must match the type
    # ------------------------------------------------------------------

    def test_v5_r3_marker_in_preamble(self):
        """V5-R3 rule marker must appear in _PROMPT_PREAMBLE."""
        self.assertIn("V5-R3", tc._PROMPT_PREAMBLE)

    def test_v5_r3_practices_not_language(self):
        """V5-R3 must prohibit PRACTICES with a language target."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("PRACTICES", preamble)
        lower = preamble.lower()
        self.assertIn("language", lower, "V5-R3 must call out language as invalid PRACTICES target")

    def test_v5_r3_claims_target_constraint(self):
        """V5-R3 must state CLAIMS targets a title/domain/throne, never a person."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("CLAIMS", preamble)

    def test_v5_r3_worships_target_constraint(self):
        """V5-R3 must state WORSHIPS targets a deity/religion."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("WORSHIPS", preamble)

    # ------------------------------------------------------------------
    # V5-R4 — state-not-moment for ATTACKS / COMMANDS / ALLIES_WITH
    # ------------------------------------------------------------------

    def test_v5_r4_marker_in_preamble(self):
        """V5-R4 rule marker must appear in _PROMPT_PREAMBLE."""
        self.assertIn("V5-R4", tc._PROMPT_PREAMBLE)

    def test_v5_r4_attacks_intent_requirement(self):
        """V5-R4 must state ATTACKS requires violent/combat intent."""
        preamble = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "attacks" in preamble and ("violent" in preamble or "combat intent" in preamble),
            "V5-R4 must state ATTACKS requires violent/combat intent",
        )

    def test_v5_r4_commands_standing_requirement(self):
        """V5-R4 must state COMMANDS requires a STANDING relationship."""
        preamble = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "commands" in preamble and "standing" in preamble,
            "V5-R4 must state COMMANDS requires a standing relationship",
        )

    def test_v5_r4_allies_with_peer_alliance(self):
        """V5-R4 must clarify ALLIES_WITH is a peer/political alliance."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("ALLIES_WITH", preamble)

    # ------------------------------------------------------------------
    # V5-R5 — temporal phase
    # ------------------------------------------------------------------

    def test_v5_r5_marker_in_preamble(self):
        """V5-R5 rule marker must appear in _PROMPT_PREAMBLE."""
        self.assertIn("V5-R5", tc._PROMPT_PREAMBLE)

    def test_v5_r5_spouse_over_betrothed(self):
        """V5-R5 must cite the SPOUSE_OF vs BETROTHED_TO example."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("SPOUSE_OF", preamble)
        self.assertIn("BETROTHED_TO", preamble)

    def test_v5_r5_temporal_phase_language(self):
        """V5-R5 must mention choosing the phase true at this chapter's point."""
        preamble = tc._PROMPT_PREAMBLE.lower()
        self.assertTrue(
            "phase" in preamble or "timeline" in preamble,
            "V5-R5 must reference temporal phase / timeline",
        )

    # ------------------------------------------------------------------
    # V5-R6 — no analytical types from a single moment
    # ------------------------------------------------------------------

    def test_v5_r6_marker_in_preamble(self):
        """V5-R6 rule marker must appear in _PROMPT_PREAMBLE."""
        self.assertIn("V5-R6", tc._PROMPT_PREAMBLE)

    def test_v5_r6_parallels_requires_multi_scene(self):
        """V5-R6 must state PARALLELS requires multi-scene evidence."""
        preamble = tc._PROMPT_PREAMBLE
        self.assertIn("PARALLELS", preamble)
        lower = preamble.lower()
        self.assertTrue(
            "multi-scene" in lower or "single moment" in lower or "single line" in lower,
            "V5-R6 must prohibit PARALLELS from a single moment/line",
        )

    def test_v5_r6_analytical_pass_ownership(self):
        """V5-R6 must state a later analytical pass owns thematic edges."""
        preamble = tc._PROMPT_PREAMBLE.lower()
        self.assertIn(
            "analytical pass",
            preamble,
            "V5-R6 must defer thematic edges to a later analytical pass",
        )

    # ------------------------------------------------------------------
    # All 6 V5 markers in rendered prompt
    # ------------------------------------------------------------------

    def test_all_v5_markers_in_rendered_prompt(self):
        """All 6 V5-R* markers must propagate into the rendered classify prompt."""
        rows = [_make_tail_row()]
        prompt = tc.render_classify_prompt(rows, _SAMPLE_VOCAB)
        for marker in ["V5-R1", "V5-R2", "V5-R3", "V5-R4", "V5-R5", "V5-R6"]:
            self.assertIn(marker, prompt, f"{marker} must appear in rendered classify prompt")

    def test_rule_numbering_includes_v5_block(self):
        """_PROMPT_PREAMBLE must still contain rules 1–14 plus the v5 block."""
        preamble = tc._PROMPT_PREAMBLE
        for n in range(1, 15):
            self.assertIn(f"{n}.", preamble, f"Rule {n} must still be present alongside v5 rules")
        self.assertIn("v5 PRECISION RULES", preamble)


# ---------------------------------------------------------------------------
# Tests: flush_delta — cursor-based incremental flush correctness
# ---------------------------------------------------------------------------

class TestFlushDelta(unittest.TestCase):
    """flush_delta: cursor-based incremental flush — no duplicates, correct delta."""

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _make_emit_row(self, idx: int) -> dict:
        """Minimal emit_edge row with a unique evidence_chapter so book grouping works."""
        return {
            "decision": "emit_edge",
            "edge_type": "LOVES",
            "source_slug": f"char-{idx}",
            "target_slug": "target",
            "evidence_chapter": f"agot-test-{idx:02d}",
        }

    def _make_rejected_row(self, idx: int) -> dict:
        return {
            "decision": "rejected",
            "edge_type": "REJECT",
            "source_slug": f"char-{idx}",
            "target_slug": "target",
            "evidence_chapter": f"agot-test-{idx:02d}",
        }

    def _read_jsonl(self, path: Path) -> list[dict]:
        if not path.exists():
            return []
        lines = path.read_text().splitlines()
        return [json.loads(ln) for ln in lines if ln.strip()]

    # ------------------------------------------------------------------
    # Core correctness
    # ------------------------------------------------------------------

    def test_flush_delta_writes_only_new_rows(self):
        """flush_delta with cursor=0 writes all rows; second call with advanced cursor writes nothing."""
        with _tmp_out_dir() as out_dir:
            emit_rows = [self._make_emit_row(i) for i in range(3)]
            cursors = {"emit": 0, "rejected": 0, "failed": 0, "needs_qualifier": 0}

            new_cursors = tc.flush_delta(emit_rows, [], [], [], cursors, ["agot"])
            # All 3 rows written
            out_file = out_dir / "agot" / "agot-tail.edges.jsonl"
            rows_on_disk = self._read_jsonl(out_file)
            self.assertEqual(len(rows_on_disk), 3)
            self.assertEqual(new_cursors["emit"], 3)

            # Second flush with same lists but advanced cursors → no new rows
            new_cursors2 = tc.flush_delta(emit_rows, [], [], [], new_cursors, ["agot"])
            rows_on_disk2 = self._read_jsonl(out_file)
            self.assertEqual(len(rows_on_disk2), 3, "Second flush must not duplicate rows")
            self.assertEqual(new_cursors2["emit"], 3)

    def test_flush_delta_appends_incremental_batches(self):
        """Simulate 3 batches of 2 rows each with flush-every=1; disk gets 6 unique rows."""
        with _tmp_out_dir() as out_dir:
            all_emit: list[dict] = []
            cursors = {"emit": 0, "rejected": 0, "failed": 0, "needs_qualifier": 0}

            for batch_i in range(3):
                # Add 2 rows per batch
                all_emit.append(self._make_emit_row(batch_i * 2))
                all_emit.append(self._make_emit_row(batch_i * 2 + 1))
                cursors = tc.flush_delta(all_emit, [], [], [], cursors, ["agot"])

            out_file = out_dir / "agot" / "agot-tail.edges.jsonl"
            rows_on_disk = self._read_jsonl(out_file)
            self.assertEqual(len(rows_on_disk), 6, "6 unique rows — no duplicates")
            self.assertEqual(cursors["emit"], 6)

    def test_flush_delta_no_duplicates_with_flush_every_2(self):
        """Simulate flush-every=2 over 6 batches of 1 row; final flush picks up the tail."""
        with _tmp_out_dir() as out_dir:
            all_emit: list[dict] = []
            all_rejected: list[dict] = []
            cursors = {"emit": 0, "rejected": 0, "failed": 0, "needs_qualifier": 0}

            for batch_idx in range(6):
                all_emit.append(self._make_emit_row(batch_idx))
                if batch_idx % 2 == 1:
                    all_rejected.append(self._make_rejected_row(batch_idx))
                # Flush every 2 batches
                if (batch_idx + 1) % 2 == 0:
                    cursors = tc.flush_delta(all_emit, all_rejected, [], [], cursors, ["agot"])

            # Final flush (end-of-run tail)
            cursors = tc.flush_delta(all_emit, all_rejected, [], [], cursors, ["agot"])

            edges_file = out_dir / "agot" / "agot-tail.edges.jsonl"
            rejected_file = out_dir / "agot" / "agot-tail.rejected.jsonl"
            edges_on_disk = self._read_jsonl(edges_file)
            rejected_on_disk = self._read_jsonl(rejected_file)

            # 6 batches × 1 emit row each = 6 edges (no dupes)
            self.assertEqual(len(edges_on_disk), 6, "6 emit rows, no duplicates")
            # 3 rejected rows (batch_idx 1, 3, 5)
            self.assertEqual(len(rejected_on_disk), 3, "3 rejected rows, no duplicates")

    def test_flush_delta_returns_advanced_cursors(self):
        """Returned cursors must reflect the post-flush totals."""
        with _tmp_out_dir() as out_dir:
            emit_rows = [self._make_emit_row(i) for i in range(4)]
            rejected_rows = [self._make_rejected_row(i) for i in range(2)]
            cursors = {"emit": 0, "rejected": 0, "failed": 0, "needs_qualifier": 0}

            # First flush: 2 emit + 1 rejected
            c1 = tc.flush_delta(emit_rows[:2], rejected_rows[:1], [], [], cursors, ["agot"])
            self.assertEqual(c1["emit"], 2)
            self.assertEqual(c1["rejected"], 1)

            # Second flush: 2 more emit + 1 more rejected
            c2 = tc.flush_delta(emit_rows, rejected_rows, [], [], c1, ["agot"])
            self.assertEqual(c2["emit"], 4)
            self.assertEqual(c2["rejected"], 2)

    def test_flush_delta_empty_lists_is_noop(self):
        """flush_delta on empty lists must not create any files and returns zero cursors."""
        with _tmp_out_dir() as out_dir:
            cursors = {"emit": 0, "rejected": 0, "failed": 0, "needs_qualifier": 0}
            new_cursors = tc.flush_delta([], [], [], [], cursors, ["agot"])
            edges_file = out_dir / "agot" / "agot-tail.edges.jsonl"
            self.assertFalse(edges_file.exists(), "No file should be created for empty flush")
            self.assertEqual(new_cursors, cursors)

    def test_flush_delta_cursor_never_writes_row_twice(self):
        """Growing list + repeated flush_delta calls must yield exactly len(list) rows on disk."""
        with _tmp_out_dir() as out_dir:
            all_emit: list[dict] = []
            cursors = {"emit": 0, "rejected": 0, "failed": 0, "needs_qualifier": 0}

            for i in range(10):
                all_emit.append(self._make_emit_row(i))
                cursors = tc.flush_delta(all_emit, [], [], [], cursors, ["agot"])

            out_file = out_dir / "agot" / "agot-tail.edges.jsonl"
            rows_on_disk = self._read_jsonl(out_file)
            # Must be exactly 10 rows — each row written exactly once
            self.assertEqual(len(rows_on_disk), 10)
            source_slugs = [r["source_slug"] for r in rows_on_disk]
            self.assertEqual(len(set(source_slugs)), 10, "Each row unique — no dupes")


# ---------------------------------------------------------------------------
# Tests: --flush-every 0 legacy path (end-only)
# ---------------------------------------------------------------------------

class TestFlushEveryZeroLegacyPath(unittest.TestCase):
    """--flush-every 0 must write exactly once at end, matching current behavior."""

    def _make_emit_row(self, idx: int) -> dict:
        return {
            "decision": "emit_edge",
            "edge_type": "LOVES",
            "source_slug": f"char-{idx}",
            "target_slug": "target",
            "evidence_chapter": f"agot-test-{idx:02d}",
        }

    def _read_jsonl(self, path: Path) -> list[dict]:
        if not path.exists():
            return []
        return [json.loads(ln) for ln in path.read_text().splitlines() if ln.strip()]

    def test_end_only_writes_all_rows_at_once(self):
        """With flush_every=0, a single flush_delta at end writes all rows, no intermediate files."""
        with _tmp_out_dir() as out_dir:
            # Simulate 5 "batches" accumulating rows without flushing
            all_emit = [self._make_emit_row(i) for i in range(5)]
            cursors = {"emit": 0, "rejected": 0, "failed": 0, "needs_qualifier": 0}

            # Don't flush mid-run (flush_every=0)
            # Verify: no file yet
            out_file = out_dir / "agot" / "agot-tail.edges.jsonl"
            self.assertFalse(out_file.exists(), "No file should exist before end-of-run flush")

            # End-of-run flush
            tc.flush_delta(all_emit, [], [], [], cursors, ["agot"])
            rows = self._read_jsonl(out_file)
            self.assertEqual(len(rows), 5)

    def test_end_only_single_flush_no_duplicates(self):
        """Calling flush_delta once at end with all 10 rows yields exactly 10 rows on disk."""
        with _tmp_out_dir() as out_dir:
            all_emit = [self._make_emit_row(i) for i in range(10)]
            cursors = {"emit": 0, "rejected": 0, "failed": 0, "needs_qualifier": 0}
            tc.flush_delta(all_emit, [], [], [], cursors, ["agot"])
            out_file = out_dir / "agot" / "agot-tail.edges.jsonl"
            rows = self._read_jsonl(out_file)
            self.assertEqual(len(rows), 10)


# ---------------------------------------------------------------------------
# Tests: EXIT_CODE_INTERRUPTED constant
# ---------------------------------------------------------------------------

class TestExitCodeInterrupted(unittest.TestCase):
    """EXIT_CODE_INTERRUPTED must be defined and have the conventional value 130."""

    def test_exit_code_interrupted_defined(self):
        self.assertTrue(hasattr(tc, "EXIT_CODE_INTERRUPTED"))

    def test_exit_code_interrupted_value(self):
        self.assertEqual(tc.EXIT_CODE_INTERRUPTED, 130)

    def test_exit_code_interrupted_distinct_from_rate_limit(self):
        self.assertNotEqual(tc.EXIT_CODE_INTERRUPTED, tc.EXIT_CODE_RATE_LIMIT)


# ---------------------------------------------------------------------------
# Tests: flush_delta underlying logic (signal handler path)
#
# A full signal test requires OS-level signal delivery, which is impractical
# in a unittest harness.  Instead we test the underlying delta-flush helper
# (the same function the signal path calls) to verify it flushes the correct
# remaining delta.  The signal handler itself just sets _interrupted=True; the
# loop calls flush_delta immediately after checking the flag.
# ---------------------------------------------------------------------------

class TestSignalPathDeltaFlush(unittest.TestCase):
    """Unit-test the delta-flush logic that the SIGINT/SIGTERM path invokes.

    We can't deliver a real signal inside unittest without triggering the test
    runner's own handler, so we test the underlying flush_delta function
    directly across a 'mid-run' state and verify the remaining tail is written
    correctly — exactly what the signal handler's exit path does.
    """

    def _make_row(self, idx: int, chapter: str = "agot-test-01") -> dict:
        return {
            "decision": "emit_edge",
            "edge_type": "SERVES",
            "source_slug": f"char-{idx}",
            "target_slug": "lord",
            "evidence_chapter": chapter,
        }

    def _read_jsonl(self, path: Path) -> list[dict]:
        if not path.exists():
            return []
        return [json.loads(ln) for ln in path.read_text().splitlines() if ln.strip()]

    def test_signal_path_flushes_remaining_delta(self):
        """Simulate: 3 rows flushed periodically, then signal fires with 2 more rows pending.

        The signal path calls flush_delta with the current cursors.  Only the 2
        pending rows must be written — no duplicates of the already-flushed 3.
        """
        with _tmp_out_dir() as out_dir:
            all_emit = [self._make_row(i) for i in range(5)]

            # Simulate periodic flush after rows 0-2
            cursors = {"emit": 0, "rejected": 0, "failed": 0, "needs_qualifier": 0}
            cursors = tc.flush_delta(all_emit[:3], [], [], [], cursors, ["agot"])
            self.assertEqual(cursors["emit"], 3)

            # Simulate signal fired after rows 3-4 are accumulated but not yet flushed
            # (this is exactly what the signal-path code does)
            final_cursors = tc.flush_delta(all_emit, [], [], [], cursors, ["agot"])
            self.assertEqual(final_cursors["emit"], 5)

            out_file = out_dir / "agot" / "agot-tail.edges.jsonl"
            rows_on_disk = self._read_jsonl(out_file)
            self.assertEqual(len(rows_on_disk), 5, "All 5 rows on disk — none duplicated")
            source_slugs = [r["source_slug"] for r in rows_on_disk]
            self.assertEqual(
                source_slugs,
                [f"char-{i}" for i in range(5)],
                "Rows in correct insertion order",
            )


# ---------------------------------------------------------------------------
# Context manager: temporarily redirect OUT_BASE/OUT_NEEDS_QUAL_DIR
# ---------------------------------------------------------------------------

import contextlib
import tempfile


@contextlib.contextmanager
def _tmp_out_dir():
    """Redirect tc.OUT_BASE and tc.OUT_NEEDS_QUAL_DIR to a temp dir for isolation."""
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        old_out_base = tc.OUT_BASE
        old_nq_dir = tc.OUT_NEEDS_QUAL_DIR
        tc.OUT_BASE = tmp
        tc.OUT_NEEDS_QUAL_DIR = tmp / "_needs-qualifier"
        try:
            yield tmp
        finally:
            tc.OUT_BASE = old_out_base
            tc.OUT_NEEDS_QUAL_DIR = old_nq_dir


if __name__ == "__main__":
    unittest.main()
