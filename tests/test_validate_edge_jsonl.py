"""Tests for scripts/wiki-pass2-validate-edge-jsonl.py.

The validator is our QA tool — its correctness is what we trust the graph against.
Session 60 had a vocab-parser bug (161 → corrected to 159) that tests would have
caught instantly; this is the regression suite.

Run: python3 -m unittest tests.test_validate_edge_jsonl -v
"""

import tempfile
import unittest
from pathlib import Path

from tests._helpers import load_script, REPO_ROOT

validator = load_script("wiki-pass2-validate-edge-jsonl.py")


class TestLoadCanonicalVocab(unittest.TestCase):
    """The vocab loader is regression-critical: a parser bug in Session 60
    counted 161 instead of 159 by scraping deprecated synonyms from
    description prose. The fix was a stricter regex matching only
    table-row keys. These tests freeze that contract."""

    def test_parses_real_architecture_at_167(self):
        """Vocab count history: S63 = 163 (KNOWS deprecated); S82–S87 reification
        added AGENT_IN, VICTIM_IN, SUB_BEAT_OF → 166 (reconciled S102 2026-06-16);
        S104 (2026-06-17) added PRECEDES (temporal ordering edges) → 167."""
        vocab = validator.load_canonical_vocab(REPO_ROOT / "reference/architecture.md")
        # Current canonical count; if vocab changes again, update this number.
        self.assertEqual(len(vocab), 167,
                         f"Expected 167 canonical edge types, got {len(vocab)}. "
                         f"Update this test if vocab has changed.")

    def test_excludes_deprecated_synonyms(self):
        """LOCATED_IN is in LOCATED_AT's description as a deprecated synonym — must NOT count."""
        vocab = validator.load_canonical_vocab(REPO_ROOT / "reference/architecture.md")
        self.assertNotIn("LOCATED_IN", vocab,
                         "LOCATED_IN should be excluded (deprecated synonym in description prose)")

    def test_knows_deprecated_session_63(self):
        """KNOWS was removed from active vocab in Session 63 (2026-05-21) — 82.3% fallback rate
        in Stage 4 wiki-prose classification. Must not appear in canonical vocab."""
        vocab = validator.load_canonical_vocab(REPO_ROOT / "reference/architecture.md")
        self.assertNotIn("KNOWS", vocab,
                         "KNOWS should be excluded (deprecated Session 63 — see architecture.md "
                         "Knowledge & Information section preamble)")

    def test_excludes_reverse_direction_labels(self):
        """FOSTERED_BY is mentioned in WARD_OF's description as a permitted reverse — not canonical."""
        vocab = validator.load_canonical_vocab(REPO_ROOT / "reference/architecture.md")
        self.assertNotIn("FOSTERED_BY", vocab)

    def test_includes_session_61_new_types(self):
        """5 types added in Session 61."""
        vocab = validator.load_canonical_vocab(REPO_ROOT / "reference/architecture.md")
        for t in ("IMPRISONED_AT", "TRAVELS_WITH", "PRISONER_EXCHANGE_FOR", "GUARDS", "ENCOUNTERS"):
            self.assertIn(t, vocab, f"Session 61 added {t} — should be in canonical vocab")

    def test_synthetic_table_parses(self):
        """Backticked tokens in description cells should not be counted."""
        synth = """## Edge Types

| Type | Description |
|------|-------------|
| `REAL_TYPE` | A real type. |
| `ANOTHER` | Synonym `FAKE_ONE` is deprecated, just noted in prose. |

## Next Section

| `IGNORED_ROW` | should not be counted (different section) |
"""
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(synth)
            tmp_arch = Path(f.name)
        try:
            vocab = validator.load_canonical_vocab(tmp_arch)
            self.assertEqual(vocab, {"REAL_TYPE", "ANOTHER"})
            self.assertNotIn("FAKE_ONE", vocab)
            self.assertNotIn("IGNORED_ROW", vocab)
        finally:
            tmp_arch.unlink()


class TestLoadQualifierVocab(unittest.TestCase):
    """Qualifier-enum loader (Session 58 STEP 1.6)."""

    def test_parses_real_qualifier_vocab(self):
        result = validator.load_qualifier_vocab(REPO_ROOT / "reference/edge-qualifier-vocab.md")
        # Session 63 (KNOWS deprecation): 17 enum-bearing types (8 Tier-1 + 9 Tier-2)
        self.assertGreaterEqual(len(result), 17,
                                f"Expected ≥17 enum-bearing types, got {len(result)}")
        # Tier-1 REQUIRED types should be present
        self.assertIn("SIBLING_OF", result)
        self.assertEqual(result["SIBLING_OF"][0], 1, "SIBLING_OF should be Tier 1")
        # Tier-2 OPTIONAL types
        self.assertIn("KILLS", result)
        self.assertEqual(result["KILLS"][0], 2, "KILLS should be Tier 2")
        # KNOWS deprecated Session 63 — should NOT be in qualifier vocab
        self.assertNotIn("KNOWS", result,
                         "KNOWS should be excluded from qualifier vocab (deprecated Session 63)")


class TestBuildNodeTypeIndex(unittest.TestCase):
    """slug → type frontmatter scan, used for type-contract checks."""

    def test_scans_node_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # Create a fake node file
            (tmp_path / "char").mkdir()
            (tmp_path / "char" / "jon-snow.node.md").write_text(
                "---\n"
                "slug: jon-snow\n"
                "type: person.character\n"
                "name: Jon Snow\n"
                "---\n"
                "Body text here.\n"
            )
            (tmp_path / "loc").mkdir()
            (tmp_path / "loc" / "winterfell.node.md").write_text(
                "---\nslug: winterfell\ntype: place.castle\n---\nbody\n"
            )
            # File without proper frontmatter — should be skipped
            (tmp_path / "char" / "broken.node.md").write_text("no frontmatter here\n")

            idx = validator.build_node_type_index(tmp_path)
            self.assertEqual(idx.get("jon-snow"), "person.character")
            self.assertEqual(idx.get("winterfell"), "place.castle")
            self.assertNotIn("broken", idx)


class TestVerbGate(unittest.TestCase):
    """Verb-gate check (Session 61 ENCOUNTERS Rule 6).

    The verb gate caught 61/76 ENCOUNTERS emissions in the overnight run —
    these tests freeze the contract so future agent prompt changes can't
    accidentally remove the safety net."""

    def test_encounters_in_verb_gate(self):
        self.assertIn("ENCOUNTERS", validator.VERB_GATE)

    def test_encounters_passes_with_staging_verb(self):
        vocab = {"ENCOUNTERS"}
        row = {
            "decision": "emit_edge",
            "candidate_kind": "source_target",
            "evidence_kind": "wiki-entity",
            "source_slug": "jon-snow",
            "target_slug": "ygritte",
            "edge_type": "ENCOUNTERS",
            "evidence_snippet": "Jon met Ygritte beyond the Wall.",
            "evidence_section": "## Beyond the Wall",
            "confidence_tier": 1,
        }
        violations = validator.validate_edge_row(row, "test.jsonl", 1, vocab)
        verb_gate_violations = [v for v in violations if v.kind == "verb-gate-failure"]
        self.assertEqual(len(verb_gate_violations), 0,
                         "Row with 'met' should pass verb gate")

    def test_encounters_fails_without_staging_verb(self):
        """The 80% case from the overnight run: ENCOUNTERS without proper verb language."""
        vocab = {"ENCOUNTERS"}
        row = {
            "decision": "emit_edge",
            "candidate_kind": "source_target",
            "evidence_kind": "wiki-entity",
            "source_slug": "daemon-sand",
            "target_slug": "aegon-targaryen-young-griff",
            "edge_type": "ENCOUNTERS",
            "evidence_snippet": "Both fought in the Greenblood campaign.",  # no staging verb
            "evidence_section": "## Greenblood",
            "confidence_tier": 2,
        }
        violations = validator.validate_edge_row(row, "test.jsonl", 1, vocab)
        verb_gate_violations = [v for v in violations if v.kind == "verb-gate-failure"]
        self.assertEqual(len(verb_gate_violations), 1)
        self.assertIn("staging verb", verb_gate_violations[0].detail)


class TestValidateEdgeRowBasics(unittest.TestCase):
    """Core row-validation contract."""

    def test_invalid_decision_short_circuits(self):
        violations = validator.validate_edge_row(
            {"decision": "frobnicate", "candidate_kind": "source_target"},
            "test.jsonl", 1, set()
        )
        kinds = [v.kind for v in violations]
        self.assertIn("invalid-decision", kinds)

    def test_invalid_candidate_kind(self):
        violations = validator.validate_edge_row(
            {"decision": "emit_edge", "candidate_kind": "made_up_shape"},
            "test.jsonl", 1, set()
        )
        kinds = [v.kind for v in violations]
        self.assertIn("invalid-candidate-kind", kinds)

    def test_missing_required_fields(self):
        violations = validator.validate_edge_row(
            {"decision": "emit_edge", "candidate_kind": "source_target"},
            # missing edge_type, evidence_snippet, etc.
            "test.jsonl", 1, set()
        )
        kinds = [v.kind for v in violations]
        self.assertIn("missing-required-fields", kinds)

    def test_edge_type_not_canonical(self):
        vocab = {"LOCATED_AT", "TRAVELS_TO"}
        row = {
            "decision": "emit_edge",
            "candidate_kind": "source_target",
            "evidence_kind": "wiki-entity",
            "source_slug": "a", "target_slug": "b",
            "edge_type": "FAKE_TYPE",
            "evidence_snippet": "some snippet",
            "evidence_section": "## Section",
            "confidence_tier": 2,
        }
        violations = validator.validate_edge_row(row, "test.jsonl", 1, vocab)
        kinds = [v.kind for v in violations]
        self.assertIn("edge-type-not-canonical", kinds)

    def test_bad_confidence_tier(self):
        vocab = {"LOCATED_AT"}
        row = {
            "decision": "emit_edge",
            "candidate_kind": "source_target",
            "evidence_kind": "wiki-entity",
            "source_slug": "a", "target_slug": "b",
            "edge_type": "LOCATED_AT",
            "evidence_snippet": "some snippet text",
            "evidence_section": "## Section",
            "confidence_tier": "high",  # should be int 1/2/3
        }
        violations = validator.validate_edge_row(row, "test.jsonl", 1, vocab)
        kinds = [v.kind for v in violations]
        self.assertIn("bad-confidence-tier", kinds)

    def test_bad_evidence_kind(self):
        vocab = {"LOCATED_AT"}
        row = {
            "decision": "emit_edge",
            "candidate_kind": "source_target",
            "evidence_kind": "book-pass1",  # source_target should be wiki-entity
            "source_slug": "a", "target_slug": "b",
            "edge_type": "LOCATED_AT",
            "evidence_snippet": "some snippet text",
            "evidence_section": "## Section",
            "confidence_tier": 1,
        }
        violations = validator.validate_edge_row(row, "test.jsonl", 1, vocab)
        kinds = [v.kind for v in violations]
        self.assertIn("bad-evidence-kind", kinds)

    def test_clean_emit_edge_row_passes(self):
        vocab = {"LOCATED_AT"}
        row = {
            "decision": "emit_edge",
            "candidate_kind": "source_target",
            "evidence_kind": "wiki-entity",
            "source_slug": "jon-snow", "target_slug": "winterfell",
            "edge_type": "LOCATED_AT",
            "evidence_snippet": "Jon grew up at Winterfell with his siblings.",
            "evidence_section": "## Background",
            "confidence_tier": 1,
        }
        violations = validator.validate_edge_row(row, "test.jsonl", 1, vocab)
        self.assertEqual(violations, [], f"Clean row should pass; got: {[str(v) for v in violations]}")


class TestNotesRejection(unittest.TestCase):
    """Session 57: notes field DELETED ENTIRELY from schema.
    Any row carrying `notes` is a schema violation."""

    def test_notes_field_rejected(self):
        vocab = {"LOCATED_AT"}
        row = {
            "decision": "emit_edge",
            "candidate_kind": "source_target",
            "evidence_kind": "wiki-entity",
            "source_slug": "a", "target_slug": "b",
            "edge_type": "LOCATED_AT",
            "evidence_snippet": "snippet text here",
            "evidence_section": "## Section",
            "confidence_tier": 1,
            "notes": "this field should be gone",  # ← schema violation
        }
        violations = validator.validate_edge_row(row, "test.jsonl", 1, vocab)
        kinds = [v.kind for v in violations]
        self.assertIn("notes-field-present", kinds)


if __name__ == "__main__":
    unittest.main()
