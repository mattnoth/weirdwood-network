"""Tests for the S121 hardening additions to the causal-walk layer.

Covers:
  - full-chain / FULL_CHAIN_EDGE_TYPES: the causal walk follows ENABLES too,
    while the default chain walk still excludes it.
  - _edge_label: ENABLES is tagged "(precondition)".
  - _beats_for_node: SUB_BEAT_OF children + their role edges (expand-beats).
  - _node_containers: normalizes list / inline-string / null / absent.

In-memory fixtures only; does NOT depend on the real edges.jsonl.
S191 (shim retirement Tier B): imports the weirwood_query package directly —
previously loaded the scripts/graph-query.py compat shim via _helpers.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "graph" / "query"))
from weirwood_query import traverse as gq  # noqa: E402


def _edge(et, src, tgt):
    return {"edge_type": et, "source_slug": src, "target_slug": tgt}


# A spine with an ENABLES hinge in the middle:
#   a --CAUSES--> b --ENABLES--> c --TRIGGERS--> d
EDGES = [
    _edge("CAUSES", "a", "b"),
    _edge("ENABLES", "b", "c"),
    _edge("TRIGGERS", "c", "d"),
    # sub-beats + roles on b
    _edge("SUB_BEAT_OF", "b1", "b"),
    _edge("AGENT_IN", "p1", "b1"),
    _edge("VICTIM_IN", "p2", "b1"),
    _edge("LOCATED_AT", "b1", "somewhere"),  # not a role edge — must be ignored
]


# --- ENABLES exclusion / inclusion -----------------------------------------

def test_causal_walk_default_stops_at_enables():
    """Default causal walk from 'a' reaches b but NOT past the ENABLES hinge."""
    down = gq._walk_causal("a", EDGES, direction="down")
    reached = {e["target_slug"] for e in down}
    assert "b" in reached
    assert "c" not in reached   # ENABLES not followed
    assert "d" not in reached


def test_full_chain_walk_crosses_enables():
    """Full-chain walk follows ENABLES, reaching the whole spine."""
    down = gq._walk_causal(
        "a", EDGES, direction="down", edge_types=gq.FULL_CHAIN_EDGE_TYPES
    )
    reached = {e["target_slug"] for e in down}
    assert {"b", "c", "d"} <= reached


def test_full_chain_edge_types_superset():
    assert gq.CAUSAL_EDGE_TYPES <= gq.FULL_CHAIN_EDGE_TYPES
    assert "ENABLES" in gq.FULL_CHAIN_EDGE_TYPES
    assert "ENABLES" not in gq.CAUSAL_EDGE_TYPES


# --- edge label -------------------------------------------------------------

def test_edge_label_tags_enables():
    assert gq._edge_label({"edge_type": "ENABLES"}) == "ENABLES (precondition)"
    assert gq._edge_label({"edge_type": "CAUSES"}) == "CAUSES"
    assert gq._edge_label({"edge_type": "TRIGGERS"}) == "TRIGGERS"


# --- beat expansion ---------------------------------------------------------

def test_beats_for_node_returns_children_and_roles():
    beats = gq._beats_for_node("b", EDGES)
    assert len(beats) == 1
    beat = beats[0]
    assert beat["beat"] == "b1"
    role_types = {rt for rt, _ in beat["roles"]}
    assert role_types == {"AGENT_IN", "VICTIM_IN"}   # LOCATED_AT excluded
    participants = {p for _, p in beat["roles"]}
    assert participants == {"p1", "p2"}


def test_beats_for_node_empty_when_no_subbeats():
    assert gq._beats_for_node("d", EDGES) == []


# --- containers normalization ----------------------------------------------

def test_node_containers_list():
    assert gq._node_containers({"containers": ["essos", "wo5k"]}) == ["essos", "wo5k"]


def test_node_containers_inline_string():
    # the simple-yaml fallback may hand us a raw string
    assert gq._node_containers({"containers": "[essos, wo5k]"}) == ["essos", "wo5k"]


def test_node_containers_null_and_absent_and_empty():
    assert gq._node_containers({"containers": None}) == []
    assert gq._node_containers({}) == []
    assert gq._node_containers({"containers": "[]"}) == []
    assert gq._node_containers({"containers": "null"}) == []
