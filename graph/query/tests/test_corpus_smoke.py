"""test_corpus_smoke.py — the two named pivots against the REAL graph
(query-layer Track, S191 D-G checkpoint, final session).

Marked `corpus`; skipif the live graph isn't present. These are smoke tests,
not exact-value pins — the real graph moves session to session, so assert on
shape/floor invariants only (see feedback_verify_dataset_provenance /
project_chronology_sort_keys in memory for why exact counts are the wrong
thing to pin here).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
QUERY_DIR = TESTS_DIR.parent  # graph/query
REPO_ROOT = QUERY_DIR.parent.parent

if str(QUERY_DIR) not in sys.path:
    sys.path.insert(0, str(QUERY_DIR))

EDGES_FILE = REPO_ROOT / "graph" / "edges" / "edges.jsonl"

pytestmark = [
    pytest.mark.corpus,
    pytest.mark.skipif(not EDGES_FILE.exists(), reason="graph/edges/edges.jsonl not present"),
]


@pytest.fixture(scope="module")
def real_edges():
    from weirwood_query.load import load_edges

    return load_edges()


@pytest.fixture(scope="module")
def real_family_nodes():
    from weirwood_query.traverse import build_family_nodes_map

    return build_family_nodes_map()


def test_tywin_chain_terminates_with_upstream_and_downstream(real_edges):
    from weirwood_query.traverse import causal_chain

    result = causal_chain("assassination-of-tywin-lannister", real_edges)
    assert result["upstream_nodes"], "expected non-empty upstream"
    assert result["downstream_nodes"], "expected non-empty downstream"
    # Terminates: both are finite plain lists (not generators/None).
    assert isinstance(result["upstream_nodes"], list)
    assert isinstance(result["downstream_nodes"], list)


def test_aegon_family_tree_at_defaults(real_family_nodes, real_edges):
    from weirwood_query.traverse import family_tree

    result = family_tree("aegon-i-targaryen", real_edges, real_family_nodes)
    assert result["member_count"] > 20
    member_slugs = {m["slug"] for m in result["members"]}
    assert "daenerys-targaryen" in member_slugs
    assert isinstance(result["truncated"], bool)


def test_resolve_red_wedding_smoke():
    from weirwood_query.resolve import resolve

    slug, status, _candidates = resolve("the Red Wedding")
    assert status == "hit"
    assert slug == "red-wedding"


def test_health_orphan_count_is_an_int(real_edges):
    from weirwood_query.traverse import health

    result = health(real_edges)
    assert isinstance(result["orphan_endpoint_count"], int)
    # Not pinning the exact value — the real graph moves. Just sane bounds.
    assert result["orphan_endpoint_count"] >= 0
