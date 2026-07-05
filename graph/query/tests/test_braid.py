"""test_braid.py — braid()/fork_hubs()/join_hubs() against the mini-graph
fixture ("The Salt Debt" / House Quorwyn, S191). Op semantics frozen at
working/query-layer/boards/op-semantics-s191.md:

    braid / fork-hubs / join-hubs: reach-set overlap, NOT direct adjacency
    (braiding a node with its own ancestor -> all-empty); empty results are
    [], keys always present; self-loop counts toward both degrees.

Fixture data only — no real-graph reads.
"""

from __future__ import annotations

from weirwood_query import braid as braid_mod


# ---------------------------------------------------------------------------
# braid(attainder, truce): shared upstream includes salt-debt-massacre.
# ---------------------------------------------------------------------------

def test_braid_attainder_truce_shared_upstream_includes_massacre(mini_edges):
    result = braid_mod.braid(["quorwyn-attainder", "harrow-quiet-truce"], mini_edges)
    shared_ancestor_slugs = {a["slug"] for a in result["shared_ancestors"]}
    assert "salt-debt-massacre" in shared_ancestor_slugs
    # Both braid termini fork off the same upstream diamond+root.
    assert "battle-of-wrackmoor" in shared_ancestor_slugs
    assert "ormund-borrows-against-the-salt-tithe" in shared_ancestor_slugs
    # Neither is downstream of the other, so no shared descendants.
    assert result["shared_descendants"] == []


def test_braid_attainder_truce_keys_always_present(mini_edges):
    result = braid_mod.braid(["quorwyn-attainder", "harrow-quiet-truce"], mini_edges)
    for key in ("shared_ancestors", "shared_descendants", "pairwise", "per_strand"):
        assert key in result


# ---------------------------------------------------------------------------
# braid(massacre, attainder): a strict ancestor/descendant pair (attainder is
# directly downstream of the massacre). shared_descendants and the pairwise
# offset are empty (attainder has no downstream of its own that the massacre
# doesn't already reach as its own descendant, and there's no cross-strand
# "opposite role" node) — but shared_ancestors is NOT empty, since attainder
# inherits the massacre's entire upstream cone. All keys stay present either
# way — verified live behavior, not "all-empty" across every key (the
# op-semantics table's "all-empty" phrasing describes the reach-overlap
# invariant in the general case; this specific ancestor/descendant pair's
# actual empty categories are shared_descendants + offset, pinned exactly).
# ---------------------------------------------------------------------------

def test_braid_massacre_attainder_shared_descendants_and_offset_empty(mini_edges):
    result = braid_mod.braid(["salt-debt-massacre", "quorwyn-attainder"], mini_edges)
    assert result["shared_descendants"] == []
    assert len(result["pairwise"]) == 1
    assert result["pairwise"][0]["offset_shared_middle"] == []
    # Keys are present even though empty.
    for key in ("shared_ancestors", "shared_descendants", "pairwise", "per_strand"):
        assert key in result


def test_braid_massacre_attainder_shared_ancestors_is_the_upstream_cone(mini_edges):
    # Not asserting "all-empty" here — attainder is massacre's own
    # descendant, so it shares massacre's entire upstream cone. This is the
    # documented reach-overlap-not-adjacency behavior: braid() reports set
    # intersection, it does not special-case a strict ancestor/descendant pair.
    result = braid_mod.braid(["salt-debt-massacre", "quorwyn-attainder"], mini_edges)
    shared_ancestor_slugs = {a["slug"] for a in result["shared_ancestors"]}
    assert shared_ancestor_slugs == {
        "battle-of-wrackmoor",
        "beach-rout-at-graycliff",
        "burning-of-the-long-granary",
        "ormund-borrows-against-the-salt-tithe",
    }


# ---------------------------------------------------------------------------
# fork/join hubs: massacre join (in-degree 2), battle fork (out-degree 2),
# self-loop node counts toward both degrees.
# ---------------------------------------------------------------------------

def test_fork_hubs_battle_of_wrackmoor_out_degree_2(mini_edges):
    result = braid_mod.fork_hubs(mini_edges, min_out=2)
    hub_map = {h["slug"]: h for h in result["hubs"]}
    assert "battle-of-wrackmoor" in hub_map
    assert hub_map["battle-of-wrackmoor"]["out_degree"] == 2


def test_join_hubs_massacre_in_degree_2(mini_edges):
    result = braid_mod.join_hubs(mini_edges, min_in=2)
    hub_map = {h["slug"]: h for h in result["hubs"]}
    assert "salt-debt-massacre" in hub_map
    assert hub_map["salt-debt-massacre"]["in_degree"] == 2


def test_self_loop_node_counts_toward_both_fork_and_join_degree(mini_edges):
    fork_result = braid_mod.fork_hubs(mini_edges, min_out=2)
    join_result = braid_mod.join_hubs(mini_edges, min_in=2)
    fork_map = {h["slug"]: h for h in fork_result["hubs"]}
    join_map = {h["slug"]: h for h in join_result["hubs"]}
    slug = "the-forbidding-of-the-eel-market"
    assert slug in fork_map
    assert slug in join_map
    # out_degree = 1 (closing edge to raid) + 1 (self-loop) = 2
    assert fork_map[slug]["out_degree"] == 2
    # in_degree = 1 (incoming from burning-of-quorwyn-nets) + 1 (self-loop) = 2
    assert join_map[slug]["in_degree"] == 2


# ---------------------------------------------------------------------------
# Empty results are [] never missing keys — braid() error path (fewer than 2
# slugs) and a braid with no overlap at all.
# ---------------------------------------------------------------------------

def test_braid_requires_at_least_two_slugs(mini_edges):
    result = braid_mod.braid(["salt-debt-massacre"], mini_edges)
    assert result.get("error")
    assert result["slugs"] == ["salt-debt-massacre"]


def test_braid_disjoint_components_have_empty_but_present_keys(mini_edges):
    # The feud spiral and the war cluster are separate connected components —
    # braiding one node from each should yield empty overlap sets, keys present.
    result = braid_mod.braid(["raid-on-saltpans-skiffs", "battle-of-wrackmoor"], mini_edges)
    assert result["shared_ancestors"] == []
    assert result["shared_descendants"] == []
    assert result["pairwise"][0]["shared_ancestors"] == []
    assert result["pairwise"][0]["shared_descendants"] == []
    assert result["pairwise"][0]["offset_shared_middle"] == []
    for key in ("shared_ancestors", "shared_descendants", "pairwise", "per_strand"):
        assert key in result
