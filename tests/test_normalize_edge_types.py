"""Tests for scripts/stage4-haiku-normalize-edge-types.py.

The Session 60 worklog flagged: "a first build over-reached with a synonym
table — `ATTACKED_BY`→`KILLED_BY` etc. — caught and removed; silently laundering
semantic errors would destroy the Haiku-vs-Sonnet drift signal."

These tests freeze the contract:
  - ALIAS_TABLE entries must be morphological (same English word, different
    inflection) OR marked as explicit Session-61 SYNONYM exceptions
  - SEMANTIC_DISTINCT_TYPES must NOT get fuzzy-matched
  - The 0.80 difflib threshold catches inflection variants but not cross-lemma

Run: python3 -m unittest tests.test_normalize_edge_types -v
"""

import unittest

from tests._helpers import load_script

norm = load_script("stage4-haiku-normalize-edge-types.py")


class TestAliasTableContents(unittest.TestCase):
    """Contract: ALIAS_TABLE is morphological-or-explicit-synonym only.
    Regression for Session 60's over-reach incident."""

    def test_known_morphological_aliases_present(self):
        """The 5 morphological + 1 deprecated-synonym entries from Session 60."""
        for raw, canon in [
            ("TRAVELED_TO", "TRAVELS_TO"),
            ("DIES_AT", "DIED_AT"),
            ("ALLIED_WITH", "ALLIES_WITH"),
            ("ATTENDED", "ATTENDS"),
            ("LOCATEDOCATED_AT", "LOCATED_AT"),
            ("LOCATED_IN", "LOCATED_AT"),
        ]:
            self.assertEqual(norm.ALIAS_TABLE.get(raw), canon,
                             f"Expected ALIAS_TABLE[{raw!r}] == {canon!r}")

    def test_session_61_accompanies_alias(self):
        """Session 61 added ACCOMPANIES → TRAVELS_WITH as the first explicit
        semantic-synonym entry. Both sides have same directionality (per docstring)."""
        self.assertEqual(norm.ALIAS_TABLE.get("ACCOMPANIES"), "TRAVELS_WITH")

    def test_no_dangerous_semantic_remaps(self):
        """The Session 60 over-reach: ATTACKED_BY was almost auto-mapped to KILLED_BY.
        ATTACKED_BY must NOT be in ALIAS_TABLE — it's semantically distinct
        (attack ≠ kill). It belongs in SEMANTIC_DISTINCT_TYPES."""
        self.assertNotIn("ATTACKED_BY", norm.ALIAS_TABLE,
                         "ATTACKED_BY would silently launder semantic error → must NOT be in ALIAS_TABLE")
        self.assertIn("ATTACKED_BY", norm.SEMANTIC_DISTINCT_TYPES)

    def test_fostered_by_handled_via_semantic_distinct(self):
        """FOSTERED_BY is reverse-of-WARD_OF — direction-unsafe to auto-rewrite.
        Must be in SEMANTIC_DISTINCT_TYPES, not ALIAS_TABLE."""
        # FOSTERED_BY_INVERSE is the actual sentinel listed; FOSTERED_BY itself
        # is omitted from ALIAS_TABLE because direction-coupling makes it unsafe.
        self.assertNotIn("FOSTERED_BY", norm.ALIAS_TABLE,
                         "FOSTERED_BY is direction-coupled to WARD_OF; auto-rewrite unsafe")


class TestNormalizeEdgeType(unittest.TestCase):
    """Pure function behavior."""

    CANONICAL = frozenset(["LOCATED_AT", "TRAVELS_TO", "TRAVELS_WITH",
                           "SIBLING_OF", "KILLED_BY", "ATTENDS"])

    def test_exact_match_returns_score_1(self):
        result, score = norm.normalize_edge_type("LOCATED_AT", self.CANONICAL)
        self.assertEqual(result, "LOCATED_AT")
        self.assertEqual(score, 1.0)

    def test_lowercase_input_normalizes_to_uppercase(self):
        result, score = norm.normalize_edge_type("located_at", self.CANONICAL)
        self.assertEqual(result, "LOCATED_AT")
        self.assertEqual(score, 1.0)

    def test_morphological_alias_returns_score_1(self):
        """TRAVELED_TO (past) is in ALIAS_TABLE → TRAVELS_TO; score 1.0."""
        result, score = norm.normalize_edge_type("TRAVELED_TO", self.CANONICAL)
        self.assertEqual(result, "TRAVELS_TO")
        self.assertEqual(score, 1.0)

    def test_semantic_distinct_returns_sentinel(self):
        """ATTACKED_BY is semantic-distinct — must NOT be fuzzy-matched to KILLED_BY.
        Returns the __SEMANTIC_DISTINCT__ sentinel so caller can route correctly."""
        result, score = norm.normalize_edge_type("ATTACKED_BY", self.CANONICAL)
        self.assertEqual(result, "__SEMANTIC_DISTINCT__")
        self.assertEqual(score, 0.0)

    def test_completely_unknown_returns_none(self):
        result, score = norm.normalize_edge_type("FROBNICATES_THE", self.CANONICAL)
        self.assertIsNone(result)
        self.assertEqual(score, 0.0)

    def test_empty_input_returns_none(self):
        result, score = norm.normalize_edge_type("", self.CANONICAL)
        self.assertIsNone(result)
        self.assertEqual(score, 0.0)

    def test_fuzzy_match_at_threshold(self):
        """Difflib fallback above SIMILARITY_THRESHOLD."""
        # Single-char typo on a canonical type — should fuzzy-match at >0.80
        result, score = norm.normalize_edge_type("LOCATED_ATX", self.CANONICAL)
        self.assertEqual(result, "LOCATED_AT")
        self.assertGreaterEqual(score, norm.SIMILARITY_THRESHOLD)


if __name__ == "__main__":
    unittest.main()
