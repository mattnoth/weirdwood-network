"""conftest.py — session-scoped fixtures over the mini-graph test fixture
("The Salt Debt" / House Quorwyn, S191, D-G checkpoint #1).

Fixture home: graph/query/tests/fixtures/mini/ — this is TEST DATA, not
graph data. It never touches graph/nodes/, graph/edges/, graph/index/,
sources/, or web/.

Engine import pattern mirrors graph/query/spec/run_cases.py: sys.path.insert
the graph/query directory (this file's grandparent) so `weirwood_query` is
importable regardless of caller cwd.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
QUERY_PKG_DIR = TESTS_DIR.parent  # graph/query
FIXTURE_DIR = TESTS_DIR / "fixtures" / "mini"

if str(QUERY_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(QUERY_PKG_DIR))

from weirwood_query.load import load_edges  # noqa: E402


@pytest.fixture(scope="session")
def mini_nodes_dir() -> Path:
    """Path to the mini fixture's nodes/ directory (category subdirs mirror
    the real graph/nodes/ layout: characters/, events/, factions/, foods/,
    artifacts/, texts/)."""
    return FIXTURE_DIR / "nodes"


@pytest.fixture(scope="session")
def mini_edges() -> list[dict]:
    """The mini fixture's edges, loaded via the real load_edges() — same
    parsing path production code uses, pointed at the fixture file."""
    return load_edges(FIXTURE_DIR / "edges.jsonl")


@pytest.fixture(scope="session")
def mini_alias_lookup() -> dict[str, str]:
    """The fixture's {normalized_phrase -> canonical_slug} table (the
    event-alias-lookup.json shape's alias_to_canonical block)."""
    data = json.loads((FIXTURE_DIR / "alias-lookup.json").read_text(encoding="utf-8"))
    return data.get("alias_to_canonical", {})


@pytest.fixture(scope="session")
def mini_collisions() -> dict[str, list[dict]]:
    """The fixture's {normalized_phrase -> [conflicting entries]} collision
    table (the event-alias-lookup.json shape's ambiguous_collisions block)."""
    data = json.loads((FIXTURE_DIR / "alias-lookup.json").read_text(encoding="utf-8"))
    return data.get("ambiguous_collisions", {})


@pytest.fixture(scope="session")
def mini_all_node_index() -> dict[str, list[dict]]:
    """The fixture's {normalized_phrase -> [{canonical_slug, node_category,
    node_type, source}]} all-node candidate index (the
    all-node-alias-lookup.json shape's phrase_to_nodes block)."""
    data = json.loads((FIXTURE_DIR / "all-node-index.json").read_text(encoding="utf-8"))
    return data.get("phrase_to_nodes", {})
