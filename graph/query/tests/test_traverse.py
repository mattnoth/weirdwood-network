"""test_traverse.py — the big traversal-op suite against the mini-graph
fixture ("The Salt Debt" / House Quorwyn, S191). Op semantics frozen at
working/query-layer/boards/op-semantics-s191.md and the fixture's own
"What each op asserts" section (working/query-layer/boards/fixture-design.md).

Fixture data only — no real-graph reads. Session-scoped fixtures
(mini_edges, mini_nodes_dir, ...) come from graph/query/tests/conftest.py.
"""

from __future__ import annotations

import pytest

from weirwood_query import traverse
from weirwood_query.load import find_node_file, iter_all_nodes, parse_quotes, split_sections


# ---------------------------------------------------------------------------
# Shared helper: the family-tree nodes map, built the same way
# traverse.build_family_nodes_map does, but scoped to the fixture's nodes_dir.
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def mini_family_nodes(mini_nodes_dir):
    nodes: dict[str, dict] = {}
    for node in iter_all_nodes(mini_nodes_dir):
        quotes_text = split_sections(node.body).get("quotes", "")
        nodes[node.slug] = {
            "name": node.name,
            "type": node.type,
            "quotes": parse_quotes(quotes_text),
        }
    return nodes


# ---------------------------------------------------------------------------
# Causal diamond depths + join at the massacre
# ---------------------------------------------------------------------------

def test_causal_diamond_depths_from_battle(mini_edges):
    result = traverse.causal_chain("battle-of-wrackmoor", mini_edges)
    # Depth 1 downstream: the two diamond legs.
    depth1_targets = {e["target_slug"] for e in result["downstream"] if e["depth"] == 1}
    assert depth1_targets == {"beach-rout-at-graycliff", "burning-of-the-long-granary"}
    # Depth 2 downstream: both legs converge at the massacre — a single join,
    # not a doubled edge in the node set (though two edges land there).
    depth2_targets = {e["target_slug"] for e in result["downstream"] if e["depth"] == 2}
    assert depth2_targets == {"salt-debt-massacre"}
    massacre_edges_at_depth2 = [e for e in result["downstream"] if e["depth"] == 2]
    assert len(massacre_edges_at_depth2) == 2  # both legs' CAUSES edges land here
    # Depth 3 downstream: the braid pair.
    depth3_targets = {e["target_slug"] for e in result["downstream"] if e["depth"] == 3}
    assert depth3_targets == {"quorwyn-attainder", "harrow-quiet-truce"}
    # Upstream: the chain root.
    assert result["upstream_nodes"] == ["ormund-borrows-against-the-salt-tithe"]


def test_causal_chain_root_is_included_once_in_downstream_nodes(mini_edges):
    result = traverse.causal_chain("battle-of-wrackmoor", mini_edges)
    downstream_nodes = result["downstream_nodes"]
    assert len(downstream_nodes) == len(set(downstream_nodes))  # no dupes
    assert downstream_nodes == sorted(downstream_nodes)  # sorted per traverse.py


# ---------------------------------------------------------------------------
# chain vs full-chain ENABLES divergence — asserted from salt-debt-massacre,
# NOT battle-of-wrackmoor (the leg attaches at the massacre per fixture-design.md).
# ---------------------------------------------------------------------------

def test_chain_excludes_enables_leg_from_massacre(mini_edges):
    causal_only = traverse.causal_chain("salt-debt-massacre", mini_edges)
    upstream = set(causal_only["upstream_nodes"])
    assert "the-quiet-mile-crossing" not in upstream
    assert "alys-weds-perrin" not in upstream


def test_full_chain_includes_enables_leg_from_massacre(mini_edges):
    full = traverse.causal_chain(
        "salt-debt-massacre", mini_edges, edge_types=traverse.FULL_CHAIN_EDGE_TYPES
    )
    upstream = set(full["upstream_nodes"])
    assert "the-quiet-mile-crossing" in upstream
    assert "alys-weds-perrin" in upstream


def test_chain_excludes_enables_leg_from_battle_too(mini_edges):
    # The leg attaches at the massacre, not the battle — but plain `chain`
    # from the battle must ALSO never surface it (it's simply unreachable
    # via CAUSES/TRIGGERS/MOTIVATES from either root).
    causal_only = traverse.causal_chain("battle-of-wrackmoor", mini_edges)
    assert "alys-weds-perrin" not in set(causal_only["downstream_nodes"])
    assert "the-quiet-mile-crossing" not in set(causal_only["downstream_nodes"])


# ---------------------------------------------------------------------------
# Cycle terminates with closing edge kept exactly once; self-loop appears
# once at depth 1 in chain.
# ---------------------------------------------------------------------------

def test_feud_cycle_terminates_and_closing_edge_kept_once(mini_edges):
    result = traverse.causal_chain("the-forbidding-of-the-eel-market", mini_edges)
    # The self-loop CAUSES edge (forbidding -> forbidding) must appear exactly
    # once in each direction's edge list, at depth 1.
    up_self_loops = [
        e for e in result["upstream"]
        if e["source_slug"] == "the-forbidding-of-the-eel-market"
        and e["target_slug"] == "the-forbidding-of-the-eel-market"
    ]
    down_self_loops = [
        e for e in result["downstream"]
        if e["source_slug"] == "the-forbidding-of-the-eel-market"
        and e["target_slug"] == "the-forbidding-of-the-eel-market"
    ]
    assert len(up_self_loops) == 1 and up_self_loops[0]["depth"] == 1
    assert len(down_self_loops) == 1 and down_self_loops[0]["depth"] == 1

    # The cycle-closing edge (forbidding -> raid) must appear exactly once in
    # the downstream walk, not repeat as the BFS wraps around.
    closing_edges_down = [
        e for e in result["downstream"]
        if e["source_slug"] == "the-forbidding-of-the-eel-market"
        and e["target_slug"] == "raid-on-saltpans-skiffs"
    ]
    assert len(closing_edges_down) == 1

    # The walk must terminate (finite result), reaching all 3 spiral nodes.
    assert set(result["downstream_nodes"]) == {
        "raid-on-saltpans-skiffs", "burning-of-quorwyn-nets", "the-forbidding-of-the-eel-market",
    }
    assert set(result["upstream_nodes"]) == {
        "raid-on-saltpans-skiffs", "burning-of-quorwyn-nets", "the-forbidding-of-the-eel-market",
    }


# ---------------------------------------------------------------------------
# Self-loop: neighbors() counts it once outgoing + once incoming.
# ---------------------------------------------------------------------------

def test_neighbors_self_loop_counts_once_each_direction(mini_edges, mini_nodes_dir):
    result = traverse.neighbors("the-forbidding-of-the-eel-market", mini_edges, mini_nodes_dir)
    assert result["outgoing_count"] == 2
    assert result["incoming_count"] == 2
    self_loop_out = [
        r for r in result["outgoing"]
        if r["other_slug"] == "the-forbidding-of-the-eel-market"
    ]
    self_loop_in = [
        r for r in result["incoming"]
        if r["other_slug"] == "the-forbidding-of-the-eel-market"
    ]
    assert len(self_loop_out) == 1
    assert len(self_loop_in) == 1


# ---------------------------------------------------------------------------
# participants vs expand-beats role-set divergence on the same hub
# (salt-debt-massacre).
# ---------------------------------------------------------------------------

def test_participants_on_massacre_excludes_witness_and_hub_level_agent(mini_edges, mini_nodes_dir):
    result = traverse.event_participants("salt-debt-massacre", mini_edges, mini_nodes_dir)
    assert result["beat_count"] == 2
    assert result["participant_count"] == 2
    sources_and_roles = {(p["source_slug"], p["role_type"]) for p in result["participants"]}
    assert sources_and_roles == {
        ("dagon-quorwyn", "COMMANDS_IN"),
        ("ormund-quorwyn", "VICTIM_IN"),
    }
    # WITNESS_IN participants (Tam, Crell) must NOT appear — participants()
    # reads PARTICIPANT_ROLE_TYPES, which excludes WITNESS_IN.
    sources = {p["source_slug"] for p in result["participants"]}
    assert "tam-salter" not in sources
    assert "maester-crell" not in sources
    # Hub-level AGENT_IN (Dagon, directly on the massacre, not a beat) must
    # NOT appear — participants() only unions BEAT-attached roles.
    dagon_roles = {p["role_type"] for p in result["participants"] if p["source_slug"] == "dagon-quorwyn"}
    assert dagon_roles == {"COMMANDS_IN"}  # not also AGENT_IN


def test_expand_beats_on_massacre_includes_witness_in(mini_edges):
    result = traverse.causal_chain("salt-debt-massacre", mini_edges, expand_beats=True)
    beats = result["beats"]["salt-debt-massacre"]
    all_roles = {(role_type, participant) for beat in beats for role_type, participant in beat["roles"]}
    assert ("WITNESS_IN", "maester-crell") in all_roles
    assert ("WITNESS_IN", "tam-salter") in all_roles
    assert ("COMMANDS_IN", "dagon-quorwyn") in all_roles
    assert ("VICTIM_IN", "ormund-quorwyn") in all_roles


def test_tam_salters_participates_in_is_in_neither_role_set(mini_edges, mini_nodes_dir):
    # tam-salter PARTICIPATES_IN battle-of-wrackmoor is in NEITHER
    # PARTICIPANT_ROLE_TYPES nor ROLE_EDGE_TYPES — both walkers must silently
    # ignore it. battle-of-wrackmoor has no SUB_BEAT_OF children, so
    # participants() returns the zero-beats shape.
    result = traverse.event_participants("battle-of-wrackmoor", mini_edges, mini_nodes_dir)
    assert result["beat_count"] == 0
    assert "message" in result

    chain = traverse.causal_chain("battle-of-wrackmoor", mini_edges, expand_beats=True)
    beats_map = chain["beats"]
    # battle-of-wrackmoor itself has no beats, so it should not appear as a
    # key with any roles that include tam-salter's PARTICIPATES_IN edge.
    for node, beats in beats_map.items():
        for beat in beats:
            assert "PARTICIPATES_IN" not in {rt for rt, _ in beat["roles"]}


# ---------------------------------------------------------------------------
# hub-with-beats-but-zero-roles (the wedding) vs unknown hub — two distinct
# shapes.
# ---------------------------------------------------------------------------

def test_wedding_hub_has_beats_but_zero_participants_distinct_shape(mini_edges, mini_nodes_dir):
    result = traverse.event_participants("alys-weds-perrin", mini_edges, mini_nodes_dir)
    assert result["beat_count"] == 1
    assert result["participant_count"] == 0
    assert result["participants"] == []
    # This is the "beats but no roles" shape — it must NOT carry the
    # "message"/error key that a true beats-less hub returns.
    assert "message" not in result
    assert "error" not in result


def test_unknown_hub_returns_error_and_suggestions(mini_edges, mini_nodes_dir):
    result = traverse.event_participants("nonexistent-hub-xyz", mini_edges, mini_nodes_dir)
    assert "error" in result
    assert "suggestions" in result
    assert "beat_count" not in result
    assert "participant_count" not in result


def test_true_beatless_hub_returns_message_shape(mini_edges, mini_nodes_dir):
    # battle-of-wrackmoor exists but has zero SUB_BEAT_OF children — this is
    # the OTHER distinct empty shape (not the wedding's beats-but-no-roles).
    result = traverse.event_participants("battle-of-wrackmoor", mini_edges, mini_nodes_dir)
    assert result["beat_count"] == 0
    assert result["participant_count"] == 0
    assert "message" in result
    assert "error" not in result


# ---------------------------------------------------------------------------
# Dangling crells-lost-chronicle in health() orphan endpoints.
# ---------------------------------------------------------------------------

def test_health_counts_the_one_dangling_endpoint(mini_edges, mini_nodes_dir):
    result = traverse.health(mini_edges, mini_nodes_dir)
    assert result["orphan_endpoint_count"] == 1
    assert result["orphan_endpoints"] == ["crells-lost-chronicle"]
    assert result["node_count"] == 35
    assert result["edge_count"] == 39


def test_participants_on_dangling_slug_fails_soft(mini_edges, mini_nodes_dir):
    result = traverse.event_participants("crells-lost-chronicle", mini_edges, mini_nodes_dir)
    assert "error" in result
    assert "suggestions" in result


# ---------------------------------------------------------------------------
# family: remarriage keeps 2 spouse bonds; single-parent Dagon; marry-in
# Jonna is a leaf; deep-spine threads Tomm at defaults; tight window opts
# out; up-cap truncation from Tomm.
# ---------------------------------------------------------------------------

def test_remarriage_keeps_both_spouse_bonds(mini_edges, mini_family_nodes):
    result = traverse.family_tree("baelic-quorwyn", mini_edges, mini_family_nodes)
    spouse_pairs = {frozenset((b["a"], b["b"])) for b in result["spouse_bonds"]}
    assert frozenset(("baelic-quorwyn", "sella-harrow")) in spouse_pairs
    assert frozenset(("baelic-quorwyn", "morra-saltpans")) in spouse_pairs


def test_single_parent_child_dagon(mini_edges, mini_family_nodes):
    result = traverse.family_tree("rodrik-quorwyn", mini_edges, mini_family_nodes, generations_down=1)
    member_slugs = {m["slug"] for m in result["members"]}
    assert "dagon-quorwyn" in member_slugs
    # Only one PARENT_OF bond into dagon-quorwyn (from Rodrik) — no mother edge.
    dagon_parent_bonds = [b for b in result["parent_bonds"] if b["child"] == "dagon-quorwyn"]
    assert len(dagon_parent_bonds) == 1
    assert dagon_parent_bonds[0]["parent"] == "rodrik-quorwyn"


def test_marry_in_jonna_is_a_leaf_no_ancestor_walk(mini_edges, mini_family_nodes):
    result = traverse.family_tree("jonna-harrow", mini_edges, mini_family_nodes)
    member_slugs = {m["slug"] for m in result["members"]}
    # Jonna has zero PARENT_OF edges anywhere — rooting the tree at her
    # should not surface any ancestors beyond herself and her spouse's line.
    jonna_member = next(m for m in result["members"] if m["slug"] == "jonna-harrow")
    assert jonna_member["generation"] == 0
    # No PARENT_OF bond has jonna-harrow as a child.
    assert not any(b["child"] == "jonna-harrow" for b in result["parent_bonds"])


def test_deep_spine_threads_tomm_at_default_caps_from_quor(mini_edges, mini_family_nodes):
    # Rooting at quor-quorwyn-the-elder (gen 0), Tomm sits at depth 5 — one
    # past the default generations_down=4 horizon. His prominence
    # (degree + 4*quoteCount) wins him a deep-spine anchor slot.
    result = traverse.family_tree("quor-quorwyn-the-elder", mini_edges, mini_family_nodes)
    member_slugs = {m["slug"] for m in result["members"]}
    assert "tomm-quorwyn" in member_slugs
    tomm = next(m for m in result["members"] if m["slug"] == "tomm-quorwyn")
    assert tomm["generation"] == 5


def test_tight_window_opts_out_of_deep_spine(mini_edges, mini_family_nodes):
    # An explicit tight window (generations_down=1, below the default of 4)
    # opts OUT of the deep-spine mechanism entirely — Tomm must not appear.
    result = traverse.family_tree(
        "quor-quorwyn-the-elder", mini_edges, mini_family_nodes,
        generations_up=0, generations_down=1,
    )
    member_slugs = {m["slug"] for m in result["members"]}
    assert "tomm-quorwyn" not in member_slugs


def test_up_cap_truncation_from_tomm(mini_edges, mini_family_nodes):
    # Rooting at tomm-quorwyn with generations_up=2 truncates at
    # Harwin/Jonna and excludes Rodrik (one generation further up).
    result = traverse.family_tree("tomm-quorwyn", mini_edges, mini_family_nodes, generations_up=2)
    member_slugs = {m["slug"] for m in result["members"]}
    assert member_slugs == {"harwin-quorwyn", "jonna-harrow", "ormund-quorwyn", "tomm-quorwyn"}
    assert "rodrik-quorwyn" not in member_slugs


def test_family_tree_path_escape_returns_fully_empty_shape(mini_edges, mini_family_nodes):
    result = traverse.family_tree("../../etc/passwd", mini_edges, mini_family_nodes)
    assert result["members"] == []
    assert result["member_count"] == 0
    assert result["truncated"] is False


def test_family_tree_nonexistent_but_valid_slug_returns_synthetic_stub(mini_edges, mini_family_nodes):
    # A well-formed slug with no backing node is NOT the same as an invalid
    # slug — it returns a single-member synthetic stub, per graph.ts's
    # documented (non-obvious) behavior.
    result = traverse.family_tree("nonexistent-quorwyn-cousin", mini_edges, mini_family_nodes)
    assert result["member_count"] == 1
    member = result["members"][0]
    assert member["slug"] == "nonexistent-quorwyn-cousin"
    assert member["has_node"] is False
    assert member["generation"] == 0


# ---------------------------------------------------------------------------
# container: exact sets (31 wrackmoor / 3 eel-feud, boot in neither).
# ---------------------------------------------------------------------------

def test_container_wrackmoor_exact_count(mini_nodes_dir):
    result = traverse.container("wrackmoor", mini_nodes_dir)
    assert result["count"] == 31
    member_slugs = {n["slug"] for n in result["nodes"]}
    assert "lord-quorwyns-good-boot" not in member_slugs


def test_container_eel_feud_exact_set(mini_nodes_dir):
    result = traverse.container("eel-feud", mini_nodes_dir)
    member_slugs = {n["slug"] for n in result["nodes"]}
    assert member_slugs == {
        "raid-on-saltpans-skiffs",
        "burning-of-quorwyn-nets",
        "the-forbidding-of-the-eel-market",
    }
    assert result["count"] == 3


def test_boot_is_in_neither_container(mini_nodes_dir):
    wrackmoor = {n["slug"] for n in traverse.container("wrackmoor", mini_nodes_dir)["nodes"]}
    eel_feud = {n["slug"] for n in traverse.container("eel-feud", mini_nodes_dir)["nodes"]}
    assert "lord-quorwyns-good-boot" not in wrackmoor
    assert "lord-quorwyns-good-boot" not in eel_feud


# ---------------------------------------------------------------------------
# path: cross-component zero shape; path(a,a) leg symmetry.
# ---------------------------------------------------------------------------

def test_path_cross_component_zero_shape(mini_edges):
    result = traverse.path("raid-on-saltpans-skiffs", "battle-of-wrackmoor", mini_edges)
    assert result["direct_edges"] == []
    assert result["total_bridges"] == 0
    assert result["bridges_shown"] == 0
    assert result["bridges"] == []


def test_path_a_a_self_loop_legal_and_symmetric(mini_edges):
    result = traverse.path(
        "the-forbidding-of-the-eel-market", "the-forbidding-of-the-eel-market", mini_edges
    )
    # Must not crash; direct_edges should surface the self-loop.
    assert len(result["direct_edges"]) == 1
    assert result["direct_edges"][0]["source_slug"] == "the-forbidding-of-the-eel-market"
    assert result["direct_edges"][0]["target_slug"] == "the-forbidding-of-the-eel-market"
    # Bridges (feud-spiral neighbors) should be symmetric: since slug_a ==
    # slug_b, every bridge's a_dir/b_dir pair must mirror each other exactly
    # (same neighbor set on both "sides").
    for bridge in result["bridges"]:
        assert bridge["a_types"] == bridge["b_types"]
        assert bridge["a_dir"] == bridge["b_dir"]
        assert bridge["a_edge_count"] == bridge["b_edge_count"]


# ---------------------------------------------------------------------------
# RESENTS visible in neighbors but absent from chain/family/braid walks.
# ---------------------------------------------------------------------------

def test_resents_visible_in_neighbors(mini_edges, mini_nodes_dir):
    result = traverse.neighbors("myrcella-quorwyn", mini_edges, mini_nodes_dir)
    outgoing_types = {r["edge_type"] for r in result["outgoing"]}
    assert "RESENTS" in outgoing_types


def test_resents_absent_from_chain(mini_edges):
    # RESENTS is not CAUSES/TRIGGERS/MOTIVATES/ENABLES — a causal chain
    # rooted at myrcella-quorwyn must not touch ormund-quorwyn via it (there
    # is no causal edge at all here, so both directions should be empty).
    result = traverse.causal_chain("myrcella-quorwyn", mini_edges, edge_types=traverse.FULL_CHAIN_EDGE_TYPES)
    assert result["upstream_nodes"] == []
    assert result["downstream_nodes"] == []


def test_resents_absent_from_family(mini_edges, mini_family_nodes):
    # RESENTS is not PARENT_OF/SPOUSE_OF — family_tree rooted at myrcella
    # must never include ormund-quorwyn via the RESENTS edge (only via an
    # actual family bond, and there is none directly between them).
    result = traverse.family_tree("myrcella-quorwyn", mini_edges, mini_family_nodes)
    member_slugs = {m["slug"] for m in result["members"]}
    assert "ormund-quorwyn" not in member_slugs


def test_resents_absent_from_braid_reach_sets(mini_edges):
    from weirwood_query import braid as braid_mod

    up, down = braid_mod._reach_sets("myrcella-quorwyn", mini_edges, traverse.FULL_CHAIN_EDGE_TYPES)
    assert "ormund-quorwyn" not in up
    assert "ormund-quorwyn" not in down


# ---------------------------------------------------------------------------
# find_node_file path-escape guard (already implemented in load.py).
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("dangerous_slug", ["../../../etc/passwd", "a/../b", ""])
def test_find_node_file_rejects_path_dangerous_slugs(dangerous_slug, mini_nodes_dir):
    assert find_node_file(dangerous_slug, mini_nodes_dir) is None
