"""Tests for scripts/graph-conflict-pairs.py.

Covers:
  - pair grouping (unordered, self-loop exclusion)
  - same- vs opposite-direction conflict detection
  - INCOMPATIBLE_PAIRS matching
  - no-conflict case (clean pair)
  - self-loop handling
  - end-to-end find_all_conflicts with a tiny in-memory edge list

All tests use small in-memory edge lists or tmp files — no dependency on the
real 3,811-edge graph/edges/edges.jsonl.

Run: python3 -m pytest tests/test_graph_conflict_pairs.py -q
"""

import json
import tempfile
from pathlib import Path

import pytest

from tests._helpers import load_script

mod = load_script("graph-conflict-pairs.py")

group_by_pair = mod.group_by_pair
detect_conflicts = mod.detect_conflicts
find_all_conflicts = mod.find_all_conflicts
load_edges = mod.load_edges
INCOMPATIBLE_PAIRS = mod.INCOMPATIBLE_PAIRS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_edge(src: str, tgt: str, etype: str, **extra) -> dict:
    """Build a minimal edge dict for testing."""
    return {
        "decision": "emit_edge",
        "edge_type": etype,
        "source_slug": src,
        "target_slug": tgt,
        "evidence_ref": f"sources/chapters/agot/agot-test-01.md:10",
        "evidence_quote": f"Test quote for {etype}.",
        "evidence_book": "agot",
        "evidence_chapter": "agot-test-01",
        "confidence_tier": 1,
        "dup_count": 1,
        **extra,
    }


# ---------------------------------------------------------------------------
# Pair grouping
# ---------------------------------------------------------------------------

class TestGroupByPair:
    def test_unordered_grouping(self):
        """Edges A→B and B→A should land in the same group."""
        edges = [
            make_edge("arya-stark", "jon-snow", "LOVES"),
            make_edge("jon-snow", "arya-stark", "LOVES"),
        ]
        grouped = group_by_pair(edges)
        assert len(grouped) == 1
        pair_key = frozenset({"arya-stark", "jon-snow"})
        assert pair_key in grouped
        assert len(grouped[pair_key]) == 2

    def test_distinct_pairs_are_separate_groups(self):
        edges = [
            make_edge("cersei-lannister", "jaime-lannister", "LOVES"),
            make_edge("tyrion-lannister", "jaime-lannister", "TRUSTS"),
        ]
        grouped = group_by_pair(edges)
        assert len(grouped) == 2

    def test_self_loops_excluded(self):
        """Self-loops (src == tgt) must not appear in output."""
        edges = [
            make_edge("cersei-lannister", "cersei-lannister", "HATES"),
            make_edge("jon-snow", "arya-stark", "LOVES"),
        ]
        grouped = group_by_pair(edges)
        assert len(grouped) == 1
        assert frozenset({"cersei-lannister"}) not in grouped

    def test_empty_input(self):
        assert group_by_pair([]) == {}

    def test_edges_with_missing_slugs_skipped(self):
        """Edges with empty source or target slug are silently skipped."""
        edges = [
            make_edge("", "jon-snow", "LOVES"),
            make_edge("arya-stark", "", "HATES"),
            make_edge("arya-stark", "jon-snow", "TRUSTS"),
        ]
        grouped = group_by_pair(edges)
        assert len(grouped) == 1


# ---------------------------------------------------------------------------
# Conflict detection — no conflict
# ---------------------------------------------------------------------------

class TestNoConflict:
    def test_single_edge_no_conflict(self):
        pair = frozenset({"jon-snow", "ghost"})
        edges = [make_edge("jon-snow", "ghost", "BONDED_TO")]
        result = detect_conflicts(pair, edges)
        assert result is None

    def test_compatible_types_no_conflict(self):
        """LOVES + PROTECTS on the same pair is NOT incompatible."""
        pair = frozenset({"jon-snow", "arya-stark"})
        edges = [
            make_edge("jon-snow", "arya-stark", "LOVES"),
            make_edge("jon-snow", "arya-stark", "PROTECTS"),
        ]
        result = detect_conflicts(pair, edges)
        assert result is None

    def test_same_type_both_directions_no_conflict(self):
        """A LOVES B + B LOVES A — identical type, not incompatible."""
        pair = frozenset({"jon-snow", "arya-stark"})
        edges = [
            make_edge("jon-snow", "arya-stark", "LOVES"),
            make_edge("arya-stark", "jon-snow", "LOVES"),
        ]
        result = detect_conflicts(pair, edges)
        assert result is None


# ---------------------------------------------------------------------------
# Same-direction conflict detection
# ---------------------------------------------------------------------------

class TestSameDirectionConflict:
    def test_loves_hates_same_source(self):
        """cersei LOVES tyrion + cersei HATES tyrion → same-direction conflict."""
        pair = frozenset({"cersei-lannister", "tyrion-lannister"})
        edges = [
            make_edge("cersei-lannister", "tyrion-lannister", "LOVES"),
            make_edge("cersei-lannister", "tyrion-lannister", "HATES"),
        ]
        result = detect_conflicts(pair, edges)
        assert result is not None
        assert result["conflict_directionality"] == "same"

    def test_trusts_distrusts_same_source(self):
        pair = frozenset({"ned-stark", "petyr-baelish"})
        edges = [
            make_edge("ned-stark", "petyr-baelish", "TRUSTS"),
            make_edge("ned-stark", "petyr-baelish", "DISTRUSTS"),
        ]
        result = detect_conflicts(pair, edges)
        assert result is not None
        assert result["conflict_directionality"] == "same"

    def test_allies_with_opposes_same_source(self):
        pair = frozenset({"stannis-baratheon", "renly-baratheon"})
        edges = [
            make_edge("stannis-baratheon", "renly-baratheon", "ALLIES_WITH"),
            make_edge("stannis-baratheon", "renly-baratheon", "OPPOSES"),
        ]
        result = detect_conflicts(pair, edges)
        assert result is not None
        assert result["conflict_directionality"] == "same"

    def test_protects_attacks_same_source(self):
        pair = frozenset({"sandor-clegane", "sansa-stark"})
        edges = [
            make_edge("sandor-clegane", "sansa-stark", "PROTECTS"),
            make_edge("sandor-clegane", "sansa-stark", "ATTACKS"),
        ]
        result = detect_conflicts(pair, edges)
        assert result is not None
        assert result["conflict_directionality"] == "same"

    def test_protects_assaults_same_source(self):
        pair = frozenset({"sandor-clegane", "sansa-stark"})
        edges = [
            make_edge("sandor-clegane", "sansa-stark", "PROTECTS"),
            make_edge("sandor-clegane", "sansa-stark", "ASSAULTS"),
        ]
        result = detect_conflicts(pair, edges)
        assert result is not None
        assert result["conflict_directionality"] == "same"

    def test_conflict_record_contains_expected_fields(self):
        """Conflict record must have all expected fields."""
        pair = frozenset({"cersei-lannister", "tyrion-lannister"})
        edges = [
            make_edge("cersei-lannister", "tyrion-lannister", "LOVES"),
            make_edge("cersei-lannister", "tyrion-lannister", "HATES"),
        ]
        result = detect_conflicts(pair, edges)
        assert result is not None
        assert "slug_a" in result
        assert "slug_b" in result
        assert "conflict_directionality" in result
        assert "incompatible_type_pairs" in result
        assert "all_edge_types_on_pair" in result
        assert "total_edges_on_pair" in result
        assert "conflict_edges" in result

    def test_conflict_edges_include_only_flagged_types(self):
        """conflict_edges should NOT include BONDED_TO — only the incompatible types."""
        pair = frozenset({"jon-snow", "ghost"})
        edges = [
            make_edge("jon-snow", "ghost", "BONDED_TO"),
            make_edge("jon-snow", "ghost", "LOVES"),
            make_edge("jon-snow", "ghost", "HATES"),
        ]
        result = detect_conflicts(pair, edges)
        assert result is not None
        returned_types = {e["edge_type"] for e in result["conflict_edges"]}
        assert "BONDED_TO" not in returned_types
        assert "LOVES" in returned_types
        assert "HATES" in returned_types


# ---------------------------------------------------------------------------
# Opposite-direction conflict detection
# ---------------------------------------------------------------------------

class TestOppositeDirectionConflict:
    def test_loves_hates_opposite_directions(self):
        """A LOVES B + B HATES A → opposite-direction conflict (weaker signal)."""
        pair = frozenset({"cersei-lannister", "tyrion-lannister"})
        edges = [
            make_edge("cersei-lannister", "tyrion-lannister", "LOVES"),
            make_edge("tyrion-lannister", "cersei-lannister", "HATES"),
        ]
        result = detect_conflicts(pair, edges)
        assert result is not None
        assert result["conflict_directionality"] == "opposite"

    def test_trusts_distrusts_opposite_directions(self):
        pair = frozenset({"ned-stark", "petyr-baelish"})
        edges = [
            make_edge("ned-stark", "petyr-baelish", "TRUSTS"),
            make_edge("petyr-baelish", "ned-stark", "DISTRUSTS"),
        ]
        result = detect_conflicts(pair, edges)
        assert result is not None
        assert result["conflict_directionality"] == "opposite"


# ---------------------------------------------------------------------------
# Mixed same + opposite direction
# ---------------------------------------------------------------------------

class TestBothDirectionConflict:
    def test_both_when_same_and_opposite_present(self):
        """A LOVES B + A HATES B + B HATES A → 'both' (same + opposite)."""
        pair = frozenset({"cersei-lannister", "tyrion-lannister"})
        edges = [
            make_edge("cersei-lannister", "tyrion-lannister", "LOVES"),  # same side as below
            make_edge("cersei-lannister", "tyrion-lannister", "HATES"),  # same-direction conflict
            make_edge("tyrion-lannister", "cersei-lannister", "HATES"),  # also opposite to LOVES
        ]
        result = detect_conflicts(pair, edges)
        assert result is not None
        assert result["conflict_directionality"] == "both"


# ---------------------------------------------------------------------------
# INCOMPATIBLE_PAIRS constant structure
# ---------------------------------------------------------------------------

class TestIncompatiblePairsConstant:
    def test_is_set_of_frozensets(self):
        assert isinstance(INCOMPATIBLE_PAIRS, set)
        for item in INCOMPATIBLE_PAIRS:
            assert isinstance(item, frozenset), f"Expected frozenset, got {type(item)}"

    def test_each_pair_has_exactly_two_elements(self):
        for pair in INCOMPATIBLE_PAIRS:
            assert len(pair) == 2, f"Pair {pair} has {len(pair)} elements (expected 2)"

    def test_expected_pairs_present(self):
        assert frozenset({"LOVES", "HATES"}) in INCOMPATIBLE_PAIRS
        assert frozenset({"ALLIES_WITH", "OPPOSES"}) in INCOMPATIBLE_PAIRS
        assert frozenset({"TRUSTS", "DISTRUSTS"}) in INCOMPATIBLE_PAIRS
        assert frozenset({"PROTECTS", "ATTACKS"}) in INCOMPATIBLE_PAIRS
        assert frozenset({"PROTECTS", "ASSAULTS"}) in INCOMPATIBLE_PAIRS

    def test_all_types_in_pairs_are_uppercase_strings(self):
        for pair in INCOMPATIBLE_PAIRS:
            for t in pair:
                assert isinstance(t, str)
                assert t == t.upper(), f"Type {t!r} should be uppercase"


# ---------------------------------------------------------------------------
# End-to-end: find_all_conflicts sorting
# ---------------------------------------------------------------------------

class TestFindAllConflicts:
    def test_same_direction_sorted_first(self):
        """find_all_conflicts must return same-direction conflicts before opposite."""
        grouped = {
            # Pair 1: opposite-direction only
            frozenset({"a-slug", "b-slug"}): [
                make_edge("a-slug", "b-slug", "LOVES"),
                make_edge("b-slug", "a-slug", "HATES"),
            ],
            # Pair 2: same-direction
            frozenset({"c-slug", "d-slug"}): [
                make_edge("c-slug", "d-slug", "TRUSTS"),
                make_edge("c-slug", "d-slug", "DISTRUSTS"),
            ],
        }
        conflicts = find_all_conflicts(grouped)
        assert len(conflicts) == 2
        # same-direction should be first
        assert conflicts[0]["conflict_directionality"] == "same"
        assert conflicts[1]["conflict_directionality"] == "opposite"

    def test_no_conflicts_returns_empty(self):
        grouped = {
            frozenset({"jon-snow", "ghost"}): [
                make_edge("jon-snow", "ghost", "BONDED_TO"),
            ]
        }
        conflicts = find_all_conflicts(grouped)
        assert conflicts == []

    def test_multiple_incompatible_pairs_on_same_entity(self):
        """A single entity pair with BOTH loves/hates AND trusts/distrusts
        should produce ONE conflict record with two entries in incompatible_type_pairs."""
        pair = frozenset({"cersei-lannister", "tyrion-lannister"})
        edges = [
            make_edge("cersei-lannister", "tyrion-lannister", "LOVES"),
            make_edge("cersei-lannister", "tyrion-lannister", "HATES"),
            make_edge("cersei-lannister", "tyrion-lannister", "TRUSTS"),
            make_edge("cersei-lannister", "tyrion-lannister", "DISTRUSTS"),
        ]
        grouped = {pair: edges}
        conflicts = find_all_conflicts(grouped)
        assert len(conflicts) == 1  # one record per pair, not per incompatible-pair
        assert len(conflicts[0]["incompatible_type_pairs"]) == 2


# ---------------------------------------------------------------------------
# load_edges (JSONL I/O)
# ---------------------------------------------------------------------------

class TestLoadEdges:
    def test_loads_valid_jsonl(self, tmp_path):
        edge = make_edge("arya-stark", "jon-snow", "LOVES")
        f = tmp_path / "edges.jsonl"
        f.write_text(json.dumps(edge) + "\n", encoding="utf-8")
        loaded = load_edges(f)
        assert len(loaded) == 1
        assert loaded[0]["edge_type"] == "LOVES"

    def test_handles_curly_quotes(self, tmp_path):
        """Curly quotes and non-ASCII characters in evidence_quote must not crash."""
        edge = make_edge("arya-stark", "jon-snow", "LOVES",
                         evidence_quote="“You’re my family,” she said.")
        f = tmp_path / "edges.jsonl"
        f.write_text(json.dumps(edge, ensure_ascii=False) + "\n", encoding="utf-8")
        loaded = load_edges(f)
        assert len(loaded) == 1
        assert "“" in loaded[0]["evidence_quote"]

    def test_skips_blank_lines(self, tmp_path):
        edge = make_edge("arya-stark", "jon-snow", "LOVES")
        f = tmp_path / "edges.jsonl"
        f.write_text("\n" + json.dumps(edge) + "\n\n", encoding="utf-8")
        loaded = load_edges(f)
        assert len(loaded) == 1

    def test_multiple_edges(self, tmp_path):
        edges = [
            make_edge("arya-stark", "jon-snow", "LOVES"),
            make_edge("cersei-lannister", "tyrion-lannister", "HATES"),
            make_edge("ned-stark", "jon-snow", "PARENT_OF"),
        ]
        f = tmp_path / "edges.jsonl"
        f.write_text("\n".join(json.dumps(e) for e in edges) + "\n", encoding="utf-8")
        loaded = load_edges(f)
        assert len(loaded) == 3
