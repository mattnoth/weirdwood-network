"""test_resolve.py — pins resolve()'s 5-status contract against the mini-graph
fixture ("The Salt Debt" / House Quorwyn, S191). Op semantics frozen at
working/query-layer/boards/op-semantics-s191.md:

    resolve: 5 statuses (hit / hit-character / candidates / ambiguous / miss);
    precedence = event-alias table -> character exact -> fuzzy; possessives
    resolve via alias table (no stemming magic); collision phrases return
    ambiguous with no top slug.

Every case here passes the fixture's alias_lookup / all_node_index /
collisions tables explicitly (via the conftest fixtures) — resolve() must
never be allowed to fall back to the real graph's on-disk tables.
"""

from __future__ import annotations

import pytest

from weirwood_query import resolve as resolve_mod
from weirwood_query.normalize import normalize, title_to_slug

# ---------------------------------------------------------------------------
# A1 — all 5 statuses, parametrized against the fixture tables
# ---------------------------------------------------------------------------

# (phrase, expected_status, expected_slug_or_None)
STATUS_CASES = [
    # hit — exact normalized match in the event-alias table. Note: the
    # fixture's alias table stores several keys with "the" literally embedded
    # ("the salt debt", "the quiet mile") — since normalize() strips exactly
    # one leading article from the QUERY side, those specific keys are only
    # reachable via a doubled-article query ("the the salt debt") and are not
    # used here as hit examples; "Quorwyn Attainder" has no leading article
    # in its stored key and hits cleanly.
    ("Ormund's death", "hit", "the-eel-kings-fall"),
    ("Quorwyn Attainder", "hit", "quorwyn-attainder"),
    ("Wrackmoor rout", "hit", "battle-of-wrackmoor"),
    # hit-character — exact match to a full character name via the all-node index.
    ("Alys Quorwyn", "hit-character", "alys-quorwyn"),
    ("Tomm Quorwyn", "hit-character", "tomm-quorwyn"),
    # candidates — fuzzy match that clears the top-score/margin gate, so a top
    # slug IS returned (score 1.0 token-overlap on a non-exact-alias phrasing).
    ("the battle at wrackmoor", "candidates", "battle-of-wrackmoor"),
    # candidates — fuzzy match that does NOT clear the margin gate (bare
    # "Ormund" ties across two fuzzy candidates under the 0.75 top-score
    # floor), so status is "candidates" but the top slug is None.
    ("Ormund", "candidates", None),
    # ambiguous — collision table phrase, no single top slug.
    ("the Eel King", "ambiguous", None),
    # miss — no match at any level.
    ("quite obviously nothing at all", "miss", None),
]


@pytest.mark.parametrize(
    "phrase, expected_status, expected_slug",
    STATUS_CASES,
    ids=[c[0] for c in STATUS_CASES],
)
def test_resolve_status(
    phrase, expected_status, expected_slug, mini_alias_lookup, mini_all_node_index, mini_collisions
):
    slug, status, _candidates = resolve_mod.resolve(
        phrase, mini_alias_lookup, mini_all_node_index, collisions=mini_collisions
    )
    assert status == expected_status
    assert slug == expected_slug


def test_ambiguous_candidates_list_is_empty(mini_alias_lookup, mini_all_node_index, mini_collisions):
    # ambiguous short-circuits before the fuzzy pass — no candidates at all.
    _slug, status, candidates = resolve_mod.resolve(
        "the Eel King", mini_alias_lookup, mini_all_node_index, collisions=mini_collisions
    )
    assert status == "ambiguous"
    assert candidates == []


def test_bare_ormund_has_two_fuzzy_candidates(mini_alias_lookup, mini_all_node_index, mini_collisions):
    _slug, status, candidates = resolve_mod.resolve(
        "Ormund", mini_alias_lookup, mini_all_node_index, collisions=mini_collisions
    )
    assert status == "candidates"
    slugs = {c["slug"] for c in candidates}
    assert "ormund-quorwyn" in slugs


# ---------------------------------------------------------------------------
# A2 — possessive hit: "Ormund's death" is a direct alias-table hit, no
# stemming/apostrophe magic involved (it's a literal key in alias_to_canonical).
# ---------------------------------------------------------------------------

def test_possessive_ormunds_death_is_a_direct_alias_hit(mini_alias_lookup, mini_all_node_index, mini_collisions):
    slug, status, candidates = resolve_mod.resolve(
        "Ormund's death", mini_alias_lookup, mini_all_node_index, collisions=mini_collisions
    )
    assert status == "hit"
    assert slug == "the-eel-kings-fall"
    assert candidates == []


# ---------------------------------------------------------------------------
# A3 — ambiguous collision: "the Eel King" maps to both myrcella-quorwyn and
# ormund-quorwyn in the fixture's ambiguous_collisions block.
# ---------------------------------------------------------------------------

def test_the_eel_king_is_ambiguous_not_a_silent_pick(mini_alias_lookup, mini_all_node_index, mini_collisions):
    slug, status, _candidates = resolve_mod.resolve(
        "the Eel King", mini_alias_lookup, mini_all_node_index, collisions=mini_collisions
    )
    assert status == "ambiguous"
    assert slug is None


# ---------------------------------------------------------------------------
# B1 — resolve() precedence: event-alias table beats character exact on a
# colliding normalized key. Hand-built lookup dicts (board unit-level case) —
# NOT the fixture's real tables, since the fixture's tables don't happen to
# collide this way; this proves the ORDER of resolution, independent of any
# specific data.
# ---------------------------------------------------------------------------

def test_event_alias_beats_character_exact_on_colliding_key():
    lookup = {"ormund quorwyn": "ormund-quorwyn-the-event-alias-wins"}
    all_node_index = {
        "ormund quorwyn": [
            {
                "canonical_slug": "ormund-quorwyn-character",
                "node_category": "characters",
                "node_type": "character.human",
            }
        ]
    }
    slug, status, candidates = resolve_mod.resolve(
        "Ormund Quorwyn", lookup, all_node_index, collisions={}
    )
    assert status == "hit"
    assert slug == "ormund-quorwyn-the-event-alias-wins"
    assert candidates == []


# ---------------------------------------------------------------------------
# B2 — normalize() facts: leading-article strip, hyphen-variants NOT
# auto-unified, straight-vs-curly apostrophe divergence in title_to_slug.
# Imported directly from weirwood_query.normalize — no fixture data involved.
# ---------------------------------------------------------------------------

def test_normalize_strips_one_leading_article():
    assert normalize("The Salt Debt") == "salt debt"
    assert normalize("a salt debt") == "salt debt"
    assert normalize("an eel king") == "eel king"


def test_normalize_collapses_whitespace():
    assert normalize("  The   Salt Debt  ") == "salt debt"


def test_normalize_does_not_unify_hyphen_variants():
    # normalize() does NOT convert hyphens to spaces — "salt-debt" and
    # "salt debt" normalize to DIFFERENT keys. (slug_to_normalized() is the
    # separate helper that does the hyphen->space conversion before calling
    # normalize(); normalize() itself stays naive.)
    assert normalize("salt-debt") == "salt-debt"
    assert normalize("salt debt") == "salt debt"
    assert normalize("salt-debt") != normalize("salt debt")


def test_title_to_slug_diverges_on_straight_vs_curly_apostrophe():
    # A real, silent divergence: title_to_slug strips a straight apostrophe
    # entirely but treats a curly apostrophe as an unknown char -> hyphen.
    straight = title_to_slug("Oldtown's Citadel")
    curly = title_to_slug("Oldtown’s Citadel")
    assert straight == "oldtowns-citadel"
    assert curly == "oldtown-s-citadel"
    assert straight != curly
