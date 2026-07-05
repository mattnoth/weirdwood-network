#!/usr/bin/env python3
"""
Tests for stage4-formalize-edges.py

Covers:
  - Selection rule: emit_edge + non-null edge_type
  - Endpoint gate integration (junk endpoint dropped)
  - Dedup key + tie-break preference
  - Three tail-violation detectors (HOLDS_TITLE place, ENCOUNTERS verb, SPOUSE_OF missing qualifier)
  - Precision filter: gated-type quarantine
  - Precision filter: CONTEMPORARY_WITH person→person low-value quarantine

Usage:
    python3 -m pytest tests/test_stage4_formalize_edges.py
    python3 tests/test_stage4_formalize_edges.py   # direct runner still works

Relocated from scripts/stage4-formalize-edges-test.py (S191) — pytest never
discovered it there. `_assert` now raises on failure so pytest can't
silently pass a failing check; the direct-runner tally is preserved.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _helpers import load_script  # noqa: E402

_mod = load_script("stage4-formalize-edges.py")

passes_selection = _mod.passes_selection
apply_endpoint_gate = _mod.apply_endpoint_gate
apply_tail_violation_cleanup = _mod.apply_tail_violation_cleanup
deduplicate = _mod.deduplicate
_dedup_key = _mod._dedup_key
_dedup_score = _mod._dedup_score
is_low_quality_endpoint = _mod.is_low_quality_endpoint
apply_precision_filter = _mod.apply_precision_filter
build_character_slug_set = _mod.build_character_slug_set
_GATED_TYPES = _mod._GATED_TYPES


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------

_PASS_COUNT = 0
_FAIL_COUNT = 0


def _assert(condition: bool, msg: str) -> None:
    global _PASS_COUNT, _FAIL_COUNT
    if condition:
        _PASS_COUNT += 1
        print(f"  PASS: {msg}")
    else:
        _FAIL_COUNT += 1
        print(f"  FAIL: {msg}", file=sys.stderr)
        raise AssertionError(msg)


def _make_row(**kwargs) -> dict:
    """Return a minimal valid spine-style emit_edge row, with overrides."""
    base = {
        "decision": "emit_edge",
        "candidate_kind": "pass1_relationship",
        "edge_type": "LOVES",
        "source_slug": "arya-stark",
        "target_slug": "jon-snow",
        "evidence_kind": "book-pass1",
        "evidence_book": "agot",
        "evidence_chapter": "agot-arya-01",
        "evidence_quote": "She loved him well.",
        "confidence_tier": 1,
        "typed_by": "python-map",
        "locate_status": "verbatim",
        "evidence_ref": "sources/chapters/agot/agot-arya-01.md:11",
        "source_set": "spine",
    }
    base.update(kwargs)
    return base


# ---------------------------------------------------------------------------
# Test: Selection rule
# ---------------------------------------------------------------------------

def test_selection_rule() -> None:
    print("\n--- Selection rule ---")

    # Normal emit_edge with edge_type → passes
    r = _make_row(decision="emit_edge", edge_type="LOVES")
    _assert(passes_selection(r), "emit_edge + edge_type passes")

    # Wrong decision → fails
    r = _make_row(decision="rejected", edge_type="LOVES")
    _assert(not passes_selection(r), "rejected decision fails")

    # Missing edge_type (None) → fails
    r = _make_row(decision="emit_edge", edge_type=None)
    _assert(not passes_selection(r), "emit_edge + None edge_type fails")

    # Empty string edge_type → fails
    r = _make_row(decision="emit_edge", edge_type="")
    _assert(not passes_selection(r), "emit_edge + empty edge_type fails")

    # Whitespace-only edge_type → fails
    r = _make_row(decision="emit_edge", edge_type="   ")
    _assert(not passes_selection(r), "emit_edge + whitespace edge_type fails")

    # Hospitality row (no decision field set, but we set it via normalization) → passes
    r = _make_row(decision="emit_edge", edge_type="GUEST_OF", source_set="hospitality")
    _assert(passes_selection(r), "hospitality emit_edge + GUEST_OF passes")

    # Hospitality row with VIOLATES_GUEST_RIGHT → passes
    r = _make_row(decision="emit_edge", edge_type="VIOLATES_GUEST_RIGHT", source_set="hospitality")
    _assert(passes_selection(r), "hospitality + VIOLATES_GUEST_RIGHT passes")


# ---------------------------------------------------------------------------
# Test: Endpoint gate
# ---------------------------------------------------------------------------

def test_endpoint_gate() -> None:
    print("\n--- Endpoint gate ---")

    # Clean row → passes
    rows = [_make_row(source_slug="arya-stark", target_slug="jon-snow")]
    surviving, dropped = apply_endpoint_gate(rows)
    _assert(len(surviving) == 1, "clean row passes endpoint gate")
    _assert(len(dropped) == 0, "no drops for clean row")

    # Junk source (bare title) → dropped
    rows = [_make_row(source_slug="ser", target_slug="jon-snow")]
    surviving, dropped = apply_endpoint_gate(rows)
    _assert(len(surviving) == 0, "junk source 'ser' is dropped")
    _assert(len(dropped) == 1, "one row in dropped for junk source")
    _assert("low_quality_source" in dropped[0].get("drop_reason", ""), "'low_quality_source' in drop_reason")

    # Known alias source (alayne) → dropped
    rows = [_make_row(source_slug="alayne", target_slug="jon-snow")]
    surviving, dropped = apply_endpoint_gate(rows)
    _assert(len(dropped) == 1, "alias 'alayne' as source is dropped")

    # Junk target (reek) → dropped
    rows = [_make_row(source_slug="arya-stark", target_slug="reek")]
    surviving, dropped = apply_endpoint_gate(rows)
    _assert(len(dropped) == 1, "alias 'reek' as target is dropped")
    _assert("low_quality_target" in dropped[0].get("drop_reason", ""), "'low_quality_target' in drop_reason")

    # Empty slug → dropped
    rows = [_make_row(source_slug="", target_slug="jon-snow")]
    surviving, dropped = apply_endpoint_gate(rows)
    _assert(len(dropped) == 1, "empty source slug is dropped")

    # Demonym → dropped
    rows = [_make_row(source_slug="dothraki", target_slug="jon-snow")]
    surviving, dropped = apply_endpoint_gate(rows)
    _assert(len(dropped) == 1, "demonym 'dothraki' as source is dropped")

    # Both bad → dropped once with both reasons
    rows = [_make_row(source_slug="ser", target_slug="lord")]
    surviving, dropped = apply_endpoint_gate(rows)
    _assert(len(dropped) == 1, "both-bad endpoints → one dropped row")
    drop_reason = dropped[0].get("drop_reason", "")
    _assert("low_quality_source" in drop_reason, "drop_reason mentions source")
    _assert("low_quality_target" in drop_reason, "drop_reason mentions target")

    # Arya junk target (her-little-flower) → passes gate (not in known_alias_slugs, not a bare title)
    # This is a descriptive slug, not in the block-list — should survive endpoint gate.
    rows = [_make_row(source_slug="arya-stark", target_slug="her-little-flower")]
    surviving, dropped = apply_endpoint_gate(rows)
    _assert(len(surviving) == 1, "'her-little-flower' is not in endpoint gate (passes through)")


# ---------------------------------------------------------------------------
# Test: Tail-violation detectors
# ---------------------------------------------------------------------------

def test_tail_violations() -> None:
    print("\n--- Tail violation detectors ---")

    # Minimal node type index for tests
    node_type_index = {
        "harrenhal": "place.location",
        "lord-commander": "title",
        "hand-of-the-king": "title",
        "white-harbor": "place.location",
    }

    # --- (a) HOLDS_TITLE → place target ---

    # HOLDS_TITLE targeting a place → quarantined
    r = _make_row(
        source_set="tail",
        edge_type="HOLDS_TITLE",
        target_slug="harrenhal",
        qualifier="current",
    )
    surviving, violations = apply_tail_violation_cleanup([r], node_type_index)
    _assert(len(violations) == 1, "HOLDS_TITLE + place target is quarantined")
    _assert("holds_title_place_target" in violations[0].get("violation_kind", ""), "violation_kind is holds_title_place_target")

    # HOLDS_TITLE targeting a title → survives
    r = _make_row(
        source_set="tail",
        edge_type="HOLDS_TITLE",
        target_slug="lord-commander",
        qualifier="current",
    )
    surviving, violations = apply_tail_violation_cleanup([r], node_type_index)
    _assert(len(surviving) == 1, "HOLDS_TITLE + title target survives")
    _assert(len(violations) == 0, "HOLDS_TITLE + title target has no violations")

    # HOLDS_TITLE targeting unknown slug (not in index) → survives (skip-when-not-found policy)
    r = _make_row(
        source_set="tail",
        edge_type="HOLDS_TITLE",
        target_slug="some-unknown-title",
        qualifier="current",
    )
    surviving, violations = apply_tail_violation_cleanup([r], node_type_index)
    _assert(len(surviving) == 1, "HOLDS_TITLE + unknown target (not in index) survives")

    # --- (b) ENCOUNTERS → verb gate ---

    # ENCOUNTERS with no staging verb in quote → quarantined
    r = _make_row(
        source_set="tail",
        edge_type="ENCOUNTERS",
        source_slug="ghost",
        target_slug="nymeria",
        evidence_quote="Ghost smelled her and settled back down.",
    )
    surviving, violations = apply_tail_violation_cleanup([r], node_type_index)
    _assert(len(violations) == 1, "ENCOUNTERS + no verb is quarantined")
    _assert("encounters_no_verb" in violations[0].get("violation_kind", ""), "violation_kind is encounters_no_verb")

    # ENCOUNTERS with 'met' → survives
    r = _make_row(
        source_set="tail",
        edge_type="ENCOUNTERS",
        source_slug="arya-stark",
        target_slug="sandor-clegane",
        evidence_quote="She met him on the kingsroad.",
    )
    surviving, violations = apply_tail_violation_cleanup([r], node_type_index)
    _assert(len(surviving) == 1, "ENCOUNTERS + 'met' verb survives")

    # ENCOUNTERS with 'encountered' → survives
    r = _make_row(
        source_set="tail",
        edge_type="ENCOUNTERS",
        source_slug="jon-snow",
        target_slug="mance-rayder",
        evidence_quote="Jon encountered the King-Beyond-the-Wall at the Frostfangs.",
    )
    surviving, violations = apply_tail_violation_cleanup([r], node_type_index)
    _assert(len(surviving) == 1, "ENCOUNTERS + 'encountered' verb survives")

    # --- (c) SPOUSE_OF → missing qualifier ---

    # SPOUSE_OF with no qualifier → quarantined
    r = _make_row(
        source_set="tail",
        edge_type="SPOUSE_OF",
        source_slug="ned-stark",
        target_slug="catelyn-tully",
        qualifier=None,
    )
    surviving, violations = apply_tail_violation_cleanup([r], node_type_index)
    _assert(len(violations) == 1, "SPOUSE_OF + no qualifier is quarantined")
    _assert("spouse_of_missing_qualifier" in violations[0].get("violation_kind", ""), "violation_kind is spouse_of_missing_qualifier")

    # SPOUSE_OF with empty string qualifier → quarantined
    r = _make_row(
        source_set="tail",
        edge_type="SPOUSE_OF",
        source_slug="ned-stark",
        target_slug="catelyn-tully",
        qualifier="",
    )
    surviving, violations = apply_tail_violation_cleanup([r], node_type_index)
    _assert(len(violations) == 1, "SPOUSE_OF + empty qualifier is quarantined")

    # SPOUSE_OF with valid qualifier → survives
    r = _make_row(
        source_set="tail",
        edge_type="SPOUSE_OF",
        source_slug="ned-stark",
        target_slug="catelyn-tully",
        qualifier="current",
    )
    surviving, violations = apply_tail_violation_cleanup([r], node_type_index)
    _assert(len(surviving) == 1, "SPOUSE_OF + 'current' qualifier survives")

    # --- Spine rows are NOT checked for violations ---
    r = _make_row(
        source_set="spine",  # NOT tail — should not be checked
        edge_type="HOLDS_TITLE",
        target_slug="harrenhal",
        qualifier="current",
    )
    surviving, violations = apply_tail_violation_cleanup([r], node_type_index)
    _assert(len(surviving) == 1, "HOLDS_TITLE place target in spine is NOT quarantined (only tail is checked)")

    # --- Hospitality rows are NOT checked for violations ---
    r = _make_row(
        source_set="hospitality",
        edge_type="GUEST_OF",
        source_slug="arya-stark",
        target_slug="frey",
    )
    surviving, violations = apply_tail_violation_cleanup([r], node_type_index)
    _assert(len(surviving) == 1, "Hospitality row passes violation check (only tail is checked)")


# ---------------------------------------------------------------------------
# Test: Deduplication
# ---------------------------------------------------------------------------

def test_dedup() -> None:
    print("\n--- Deduplication ---")

    # Two identical-key rows → keep one with dup_count = 1
    r1 = _make_row(
        source_slug="arya-stark",
        edge_type="SIBLING_OF",
        target_slug="jon-snow",
        qualifier="full",
        locate_status="verbatim",
        confidence_tier=1,
        evidence_ref="sources/chapters/agot/agot-arya-01.md:11",
        source_set="spine",
    )
    r2 = _make_row(
        source_slug="arya-stark",
        edge_type="SIBLING_OF",
        target_slug="jon-snow",
        qualifier="full",
        locate_status="paraphrase",
        confidence_tier=2,
        evidence_ref=None,
        source_set="tail",
    )
    surviving, total_dups = deduplicate([r1, r2])
    _assert(len(surviving) == 1, "two duplicate rows collapse to one")
    _assert(total_dups == 1, "dup_count total is 1")
    _assert(surviving[0].get("dup_count") == 1, "surviving row has dup_count=1")

    # Tie-break: verbatim beats paraphrase
    winner = surviving[0]
    _assert(winner.get("locate_status") == "verbatim", "verbatim row wins tie-break")

    # Three rows: one verbatim tier-1 with ref, two paraphrase tier-2 no-ref
    r3 = _make_row(
        source_slug="tyrion-lannister",
        edge_type="LOVES",
        target_slug="shae",
        qualifier=None,
        locate_status="verbatim",
        confidence_tier=1,
        evidence_ref="sources/chapters/acok/acok-tyrion-01.md:5",
    )
    r4 = _make_row(
        source_slug="tyrion-lannister",
        edge_type="LOVES",
        target_slug="shae",
        qualifier=None,
        locate_status="paraphrase",
        confidence_tier=2,
        evidence_ref=None,
    )
    r5 = _make_row(
        source_slug="tyrion-lannister",
        edge_type="LOVES",
        target_slug="shae",
        qualifier=None,
        locate_status="paraphrase",
        confidence_tier=3,
        evidence_ref=None,
    )
    surviving, total_dups = deduplicate([r3, r4, r5])
    _assert(len(surviving) == 1, "three duplicate rows collapse to one")
    _assert(total_dups == 2, "total_dups is 2")
    _assert(surviving[0].get("dup_count") == 2, "surviving dup_count=2")
    _assert(surviving[0].get("locate_status") == "verbatim", "verbatim row wins 3-way tie")

    # Qualifier None vs empty string → same key (both normalize to None)
    ra = _make_row(source_slug="a", edge_type="LOVES", target_slug="b", qualifier=None)
    rb = _make_row(source_slug="a", edge_type="LOVES", target_slug="b", qualifier="")
    _assert(_dedup_key(ra) == _dedup_key(rb), "qualifier=None and qualifier='' have same dedup key")

    # Non-duplicate rows → all survive
    r6 = _make_row(source_slug="jon-snow", edge_type="LOVES", target_slug="ygritte")
    r7 = _make_row(source_slug="jon-snow", edge_type="TRUSTS", target_slug="ygritte")
    r8 = _make_row(source_slug="jon-snow", edge_type="LOVES", target_slug="ghost")
    surviving, total_dups = deduplicate([r6, r7, r8])
    _assert(len(surviving) == 3, "three distinct rows all survive")
    _assert(total_dups == 0, "no dups when all keys distinct")

    # Qualifier difference → different dedup key (not duplicates)
    rq1 = _make_row(source_slug="ned", edge_type="SPOUSE_OF", target_slug="catelyn", qualifier="current")
    rq2 = _make_row(source_slug="ned", edge_type="SPOUSE_OF", target_slug="catelyn", qualifier="former")
    surviving, total_dups = deduplicate([rq1, rq2])
    _assert(len(surviving) == 2, "different qualifiers → different dedup keys → both survive")

    # Evidence-ref tie-break (verbatim tie: ref > no-ref)
    no_ref = _make_row(locate_status="verbatim", confidence_tier=1, evidence_ref=None)
    with_ref = _make_row(locate_status="verbatim", confidence_tier=1, evidence_ref="some/path.md:10")
    _assert(
        _dedup_score(with_ref) > _dedup_score(no_ref),
        "row with evidence_ref scores higher than row without (verbatim tier-1)"
    )


# ---------------------------------------------------------------------------
# Test: Precision filter — gated-type quarantine
# ---------------------------------------------------------------------------

def test_precision_filter_gated() -> None:
    print("\n--- Precision filter: gated-type quarantine ---")

    # All five gated types should land in quarantine_gated regardless of source_set
    char_slugs: frozenset[str] = frozenset({"arya-stark", "jon-snow", "tyrion-lannister"})

    for et in ("INFORMS", "ADVISES", "MANIPULATES", "SUPPORTS", "ALIAS_OF"):
        for src in ("spine", "tail", "hospitality"):
            row = _make_row(edge_type=et, source_set=src)
            v1, gated, lowvalue = apply_precision_filter([row], char_slugs)
            _assert(
                len(gated) == 1 and len(v1) == 0 and len(lowvalue) == 0,
                f"{et} ({src}) goes to quarantine_gated",
            )
            _assert(
                gated[0].get("source_set") == src,
                f"{et} ({src}) preserves source_set in quarantine_gated",
            )

    # Non-gated edge type → survives to v1
    row = _make_row(edge_type="LOVES", source_set="spine")
    v1, gated, lowvalue = apply_precision_filter([row], char_slugs)
    _assert(len(v1) == 1 and len(gated) == 0, "LOVES is not gated → goes to v1")

    # COMPANION_OF is NOT gated (explicit: from reliable Pass-1 hints, must be retained)
    row = _make_row(edge_type="COMPANION_OF", source_set="spine")
    v1, gated, lowvalue = apply_precision_filter([row], char_slugs)
    _assert(len(v1) == 1 and len(gated) == 0, "COMPANION_OF is NOT gated → retained in v1")

    row = _make_row(edge_type="COMPANION_OF", source_set="tail")
    v1, gated, lowvalue = apply_precision_filter([row], char_slugs)
    _assert(len(v1) == 1 and len(gated) == 0, "COMPANION_OF (tail) is NOT gated → retained in v1")

    # Gated type check is case-sensitive — lowercase should NOT be quarantined
    row = _make_row(edge_type="advises", source_set="tail")
    v1, gated, lowvalue = apply_precision_filter([row], char_slugs)
    _assert(len(v1) == 1 and len(gated) == 0, "lowercase 'advises' is not matched by gated-type check")

    # Mixed batch: 2 gated, 1 not → correct split
    rows = [
        _make_row(edge_type="MANIPULATES", source_set="tail"),
        _make_row(edge_type="LOVES", source_set="spine"),
        _make_row(edge_type="INFORMS", source_set="tail"),
    ]
    v1, gated, lowvalue = apply_precision_filter(rows, char_slugs)
    _assert(len(v1) == 1, "mixed batch: 1 non-gated → v1")
    _assert(len(gated) == 2, "mixed batch: 2 gated → quarantine_gated")
    _assert(len(lowvalue) == 0, "mixed batch: 0 lowvalue")

    # Verify _GATED_TYPES constant has exactly the five expected types
    _assert(
        _GATED_TYPES == frozenset({"INFORMS", "ADVISES", "MANIPULATES", "SUPPORTS", "ALIAS_OF"}),
        "_GATED_TYPES constant contains exactly the five expected types",
    )


# ---------------------------------------------------------------------------
# Test: Precision filter — CONTEMPORARY_WITH person→person
# ---------------------------------------------------------------------------

def test_precision_filter_contemporary_with() -> None:
    print("\n--- Precision filter: CONTEMPORARY_WITH person→person ---")

    char_slugs: frozenset[str] = frozenset({
        "eddard-stark",
        "rhaegar-targaryen",
        "jon-snow",
    })

    # Both endpoints are characters → quarantine_lowvalue
    row = _make_row(
        edge_type="CONTEMPORARY_WITH",
        source_slug="eddard-stark",
        target_slug="rhaegar-targaryen",
        source_set="tail",
    )
    v1, gated, lowvalue = apply_precision_filter([row], char_slugs)
    _assert(len(lowvalue) == 1 and len(v1) == 0 and len(gated) == 0,
            "CONTEMPORARY_WITH + both chars → quarantine_lowvalue")

    # Source is a character, target is NOT → survives to v1
    row = _make_row(
        edge_type="CONTEMPORARY_WITH",
        source_slug="eddard-stark",
        target_slug="war-of-the-five-kings",
        source_set="tail",
    )
    v1, gated, lowvalue = apply_precision_filter([row], char_slugs)
    _assert(len(v1) == 1 and len(lowvalue) == 0,
            "CONTEMPORARY_WITH + src char + tgt non-char → v1")

    # Target is a character, source is NOT → survives to v1
    row = _make_row(
        edge_type="CONTEMPORARY_WITH",
        source_slug="battle-of-the-blackwater",
        target_slug="jon-snow",
        source_set="tail",
    )
    v1, gated, lowvalue = apply_precision_filter([row], char_slugs)
    _assert(len(v1) == 1 and len(lowvalue) == 0,
            "CONTEMPORARY_WITH + src non-char + tgt char → v1")

    # Neither endpoint is a character → survives to v1
    row = _make_row(
        edge_type="CONTEMPORARY_WITH",
        source_slug="war-of-five-kings",
        target_slug="red-wedding",
        source_set="tail",
    )
    v1, gated, lowvalue = apply_precision_filter([row], char_slugs)
    _assert(len(v1) == 1 and len(lowvalue) == 0,
            "CONTEMPORARY_WITH + both non-chars → v1")

    # Gated type takes priority: ADVISES even if hypothetically CONTEMPORARY_WITH-shaped
    # (Can't really test this with CONTEMPORARY_WITH since it's not in GATED_TYPES, but
    #  verify that a gated type is NOT also evaluated for CONTEMPORARY_WITH rule)
    row = _make_row(
        edge_type="ADVISES",
        source_slug="eddard-stark",
        target_slug="rhaegar-targaryen",
        source_set="spine",
    )
    v1, gated, lowvalue = apply_precision_filter([row], char_slugs)
    _assert(len(gated) == 1 and len(lowvalue) == 0,
            "ADVISES (gated) + both chars → quarantine_gated only (Rule 1 beats Rule 2)")

    # Empty character slug set: no slug matches → CONTEMPORARY_WITH survives to v1
    row = _make_row(
        edge_type="CONTEMPORARY_WITH",
        source_slug="eddard-stark",
        target_slug="rhaegar-targaryen",
        source_set="tail",
    )
    v1, gated, lowvalue = apply_precision_filter([row], frozenset())
    _assert(len(v1) == 1 and len(lowvalue) == 0,
            "CONTEMPORARY_WITH with empty char_slugs → v1 (no matches)")

    # build_character_slug_set with missing directory returns empty frozenset
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        from pathlib import Path as P
        result = build_character_slug_set(P(tmpdir))
        _assert(isinstance(result, frozenset), "build_character_slug_set returns frozenset")
        _assert(len(result) == 0, "build_character_slug_set with missing characters/ returns empty set")

    # build_character_slug_set with actual node files
    with tempfile.TemporaryDirectory() as tmpdir:
        from pathlib import Path as P
        chars_dir = P(tmpdir) / "characters"
        chars_dir.mkdir()
        (chars_dir / "jon-snow.node.md").write_text("---\nslug: jon-snow\ntype: character\n---\n")
        (chars_dir / "arya-stark.node.md").write_text("---\nslug: arya-stark\ntype: character\n---\n")
        (chars_dir / "not-a-match.txt").write_text("this is not a .node.md file")
        result = build_character_slug_set(P(tmpdir))
        _assert("jon-snow" in result, "jon-snow.node.md → slug 'jon-snow' in set")
        _assert("arya-stark" in result, "arya-stark.node.md → slug 'arya-stark' in set")
        _assert("not-a-match" not in result, ".txt file not included in character slug set")
        _assert(len(result) == 2, "only .node.md files counted (2 total)")


# ---------------------------------------------------------------------------
# Run all tests
# ---------------------------------------------------------------------------

def main() -> None:
    test_selection_rule()
    test_endpoint_gate()
    test_tail_violations()
    test_dedup()
    test_precision_filter_gated()
    test_precision_filter_contemporary_with()

    print()
    print("=" * 50)
    print(f"Tests passed: {_PASS_COUNT}")
    print(f"Tests failed: {_FAIL_COUNT}")
    if _FAIL_COUNT > 0:
        print("SOME TESTS FAILED", file=sys.stderr)
        sys.exit(1)
    else:
        print("All tests passed.")


if __name__ == "__main__":
    main()
