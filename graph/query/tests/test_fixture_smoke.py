"""test_fixture_smoke.py — proves the mini-graph fixture ("The Salt Debt" /
House Quorwyn, S191, D-G checkpoint #1) loads and wires up as designed.

Fixture home: graph/query/tests/fixtures/mini/. See fixtures/mini/README.md
for the saga + trap map. This is a handful of smoke tests, not a full
traversal-op suite — it proves the fixture itself is sound (right node
count, right edge count, no accidental dangling endpoints beyond the one
deliberate trap, both container tags return their expected members, and
resolve() correctly reports "the Eel King" as ambiguous).
"""

from __future__ import annotations

from weirwood_query import resolve as resolve_mod
from weirwood_query import traverse

# Roster / edge-group counts pinned by working/query-layer/boards/fixture-design.md
EXPECTED_NODE_COUNT = 35
EXPECTED_EDGE_COUNT = 39
DANGLING_SLUG = "crells-lost-chronicle"


def _all_node_files(mini_nodes_dir):
    return list(mini_nodes_dir.rglob("*.node.md"))


def test_node_count_matches_roster(mini_nodes_dir):
    files = _all_node_files(mini_nodes_dir)
    assert len(files) == EXPECTED_NODE_COUNT


def test_edge_count_matches_design(mini_edges):
    assert len(mini_edges) == EXPECTED_EDGE_COUNT


def test_every_endpoint_has_a_node_file_except_the_one_dangling_slug(mini_edges, mini_nodes_dir):
    slugs = {f.stem.replace(".node", "") for f in _all_node_files(mini_nodes_dir)}
    endpoints: set[str] = set()
    for e in mini_edges:
        endpoints.add(e["source_slug"])
        endpoints.add(e["target_slug"])
    dangling = endpoints - slugs
    assert dangling == {DANGLING_SLUG}


def test_wrackmoor_container_returns_expected_members(mini_nodes_dir):
    result = traverse.container("wrackmoor", mini_nodes_dir)
    member_slugs = {n["slug"] for n in result["nodes"]}
    # Family + war cluster must be in; the untagged boot must be excluded;
    # the disjoint eel-feud trio must be excluded.
    assert "ormund-quorwyn" in member_slugs
    assert "salt-debt-massacre" in member_slugs
    assert "bowl-of-eel-and-barley" in member_slugs
    assert "lord-quorwyns-good-boot" not in member_slugs
    assert "raid-on-saltpans-skiffs" not in member_slugs
    assert result["count"] == len(member_slugs)


def test_eel_feud_container_returns_the_spiral_trio(mini_nodes_dir):
    result = traverse.container("eel-feud", mini_nodes_dir)
    member_slugs = {n["slug"] for n in result["nodes"]}
    assert member_slugs == {
        "raid-on-saltpans-skiffs",
        "burning-of-quorwyn-nets",
        "the-forbidding-of-the-eel-market",
    }
    assert result["count"] == 3


def test_containers_are_disjoint_bags(mini_nodes_dir):
    wrackmoor = {n["slug"] for n in traverse.container("wrackmoor", mini_nodes_dir)["nodes"]}
    eel_feud = {n["slug"] for n in traverse.container("eel-feud", mini_nodes_dir)["nodes"]}
    assert wrackmoor & eel_feud == set()


def test_the_eel_king_resolves_ambiguous(mini_alias_lookup, mini_all_node_index, mini_collisions):
    slug, status, candidates = resolve_mod.resolve(
        "the Eel King",
        mini_alias_lookup,
        mini_all_node_index,
        collisions=mini_collisions,
    )
    assert status == "ambiguous"
    assert slug is None


def test_ormunds_death_resolves_hit(mini_alias_lookup, mini_all_node_index, mini_collisions):
    slug, status, _candidates = resolve_mod.resolve(
        "Ormund's death",
        mini_alias_lookup,
        mini_all_node_index,
        collisions=mini_collisions,
    )
    assert status == "hit"
    assert slug == "the-eel-kings-fall"


def test_alys_quorwyn_resolves_hit_character(mini_alias_lookup, mini_all_node_index, mini_collisions):
    slug, status, candidates = resolve_mod.resolve(
        "Alys Quorwyn",
        mini_alias_lookup,
        mini_all_node_index,
        collisions=mini_collisions,
    )
    assert status == "hit-character"
    assert slug == "alys-quorwyn"


def test_self_loop_present_exactly_once(mini_edges):
    self_loops = [
        e for e in mini_edges
        if e["source_slug"] == "the-forbidding-of-the-eel-market"
        and e["target_slug"] == "the-forbidding-of-the-eel-market"
    ]
    assert len(self_loops) == 1
    assert self_loops[0]["edge_type"] == "CAUSES"


def test_causal_chain_diamond_terminates_and_reaches_braid(mini_edges):
    result = traverse.causal_chain("battle-of-wrackmoor", mini_edges)
    downstream_nodes = set(result["downstream_nodes"])
    upstream_nodes = set(result["upstream_nodes"])
    # Diamond join hub and both braid termini must be reachable downstream.
    assert "salt-debt-massacre" in downstream_nodes
    assert "quorwyn-attainder" in downstream_nodes
    assert "harrow-quiet-truce" in downstream_nodes
    # Upstream must reach the chain root.
    assert "ormund-borrows-against-the-salt-tithe" in upstream_nodes


def test_chain_excludes_the_enables_leg_but_full_chain_includes_it(mini_edges):
    # The ENABLES leg (wedding -> crossing) attaches to salt-debt-massacre,
    # not battle-of-wrackmoor — the divergence assertion belongs on the
    # join hub, per fixture-design.md's "ENABLES break" note.
    causal_only = traverse.causal_chain("salt-debt-massacre", mini_edges)
    assert "the-quiet-mile-crossing" not in set(causal_only["upstream_nodes"])
    assert "alys-weds-perrin" not in set(causal_only["upstream_nodes"])

    full = traverse.causal_chain(
        "salt-debt-massacre",
        mini_edges,
        edge_types=traverse.FULL_CHAIN_EDGE_TYPES,
    )
    full_upstream = set(full["upstream_nodes"])
    assert "the-quiet-mile-crossing" in full_upstream
    assert "alys-weds-perrin" in full_upstream
