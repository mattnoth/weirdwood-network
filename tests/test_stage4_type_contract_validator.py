"""Tests for scripts/stage4-type-contract-validator.py — stdlib unittest.

No filesystem access required for core tests (character set is passed in directly).

Run: python3 -m unittest tests.test_stage4_type_contract_validator -v

API change (2026-05-25): type_contract_pass now returns (disposition, reason) where
disposition is one of: "keep", "drop", "flip", "flag", "retype".
"""

from __future__ import annotations

import unittest

from tests._helpers import load_script

tcv = load_script("stage4-type-contract-validator.py")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_row(src: str, tgt: str, et: str, quote: str = "Stub quote for contract testing.") -> dict:
    """Build a minimal edge row.  Includes a non-empty evidence_quote by default so
    tests focused on other contracts are not inadvertently failed by the empty-quote
    check.  Pass quote="" to specifically test the empty-quote contract."""
    return {
        "source_slug":   src,
        "target_slug":   tgt,
        "edge_type":     et,
        "evidence_quote": quote,
    }


def _disp(row, chars, cat_index=None):
    """Helper: return (disposition, reason) tuple."""
    return tcv.type_contract_pass(row, chars, cat_index)


def _is_drop(row, chars, cat_index=None):
    d, _ = _disp(row, chars, cat_index)
    return d == "drop"


def _is_keep(row, chars, cat_index=None):
    d, _ = _disp(row, chars, cat_index)
    return d == "keep"


def _is_flip(row, chars, cat_index=None):
    d, _ = _disp(row, chars, cat_index)
    return d == "flip"


def _is_retype(row, chars, cat_index=None):
    d, _ = _disp(row, chars, cat_index)
    return d == "retype"


def _is_flag(row, chars, cat_index=None):
    d, _ = _disp(row, chars, cat_index)
    return d == "flag"


# Minimal character set for tests
_CHARS = frozenset({
    "arya-stark", "jon-snow", "tyrion-lannister", "cersei-lannister",
    "eddard-stark", "catelyn-stark", "bran-stark", "daenerys-targaryen",
    "robb-stark", "sansa-stark", "bronn", "joffrey-baratheon",
    "loras-tyrell", "brienne-tarth", "barristan-selmy",
})

# Non-character slugs
_NON_CHARS = {
    "faith-of-the-seven",  # religion
    "house-stark",          # house
    "warden-of-the-north",  # title
    "winterfell",           # location
    "the-wall",             # location
    "lord-commander",       # title
    "battle-of-the-blackwater",  # event
    "war-of-the-five-kings",     # event
}


class TestEchoesContract(unittest.TestCase):
    """ECHOES char<->char is VALID per architecture.

    Architecture (Narrative section):
      PARALLELS = "Event/character A mirrors character B thematically"
      ECHOES    = "Weaker than PARALLELS — structural or verbal similarity"
    Both types apply to characters.  The old DROP contract was WRONG and has been removed.
    """

    def test_echoes_char_char_keep(self):
        """ECHOES: both endpoints chars -> KEEP (valid literary echo between characters).

        This is the canonical Robb/Eddard parallel case — a genuine literary observation.
        The old validator incorrectly dropped this; now it must pass.
        """
        row = _make_row("arya-stark", "jon-snow", "ECHOES")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep: ECHOES char<->char is valid")
        d, reason = _disp(row, _CHARS)
        self.assertEqual(d, "keep", f"Must keep ECHOES char<->char, got {d!r}: {reason}")

    def test_echoes_robb_eddard_keep(self):
        """ECHOES: robb-stark -> eddard-stark -> KEEP (the v1 case that was wrongly dropped)."""
        row = _make_row("robb-stark", "eddard-stark", "ECHOES",
                        quote="Lord Rickard Karstark glowered in silence.")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep: Robb/Eddard echo is valid")

    def test_echoes_char_event_keep(self):
        """ECHOES: char->event -> keep (not char<->char, and char<->char also keeps)."""
        row = _make_row("arya-stark", "battle-of-the-blackwater", "ECHOES")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")

    def test_echoes_event_event_keep(self):
        """ECHOES: event->event -> keep."""
        row = _make_row("battle-of-the-blackwater", "war-of-the-five-kings", "ECHOES")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")


class TestContemporaryWithContract(unittest.TestCase):
    """CONTEMPORARY_WITH must not connect two characters."""

    def test_contemporary_with_char_char_drop(self):
        """CONTEMPORARY_WITH: both chars -> DROP."""
        row = _make_row("eddard-stark", "catelyn-stark", "CONTEMPORARY_WITH")
        self.assertTrue(_is_drop(row, _CHARS))
        d, reason = _disp(row, _CHARS)
        self.assertIn("CONTRACT_VIOLATED", reason)

    def test_contemporary_with_event_event_pass(self):
        """CONTEMPORARY_WITH: two events -> keep."""
        row = _make_row("battle-of-the-blackwater", "war-of-the-five-kings", "CONTEMPORARY_WITH")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")


class TestKinshipContract(unittest.TestCase):
    """Kinship edges require char<->char.

    When one endpoint is char and the other is not: FLAG (slug-alias problem, true relationship).
    When neither endpoint is char: DROP (genuinely wrong).
    """

    def test_sibling_of_char_char_keep(self):
        """SIBLING_OF: both chars -> keep."""
        row = _make_row("robb-stark", "arya-stark", "SIBLING_OF")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")

    def test_sibling_of_non_char_source_flag(self):
        """SIBLING_OF: source is non-char but target IS char -> FLAG (not DROP)."""
        row = _make_row("house-stark", "arya-stark", "SIBLING_OF")
        self.assertTrue(_is_flag(row, _CHARS), "Expected FLAG for one-sided non-char kinship")
        d, reason = _disp(row, _CHARS)
        self.assertIn("CONTRACT_WARNING", reason)
        self.assertIn("source", reason)

    def test_sibling_of_non_char_target_flag(self):
        """SIBLING_OF: target is non-char but source IS char -> FLAG (not DROP)."""
        row = _make_row("robb-stark", "house-stark", "SIBLING_OF")
        self.assertTrue(_is_flag(row, _CHARS), "Expected FLAG for one-sided non-char kinship")
        d, reason = _disp(row, _CHARS)
        self.assertIn("CONTRACT_WARNING", reason)
        self.assertIn("target", reason)

    def test_sibling_of_both_non_char_drop(self):
        """SIBLING_OF: neither endpoint is a char -> DROP (genuinely wrong)."""
        row = _make_row("house-stark", "the-wall", "SIBLING_OF")
        self.assertTrue(_is_drop(row, _CHARS), "Expected DROP: both non-char kinship")
        d, reason = _disp(row, _CHARS)
        self.assertIn("CONTRACT_VIOLATED", reason)
        self.assertIn("neither", reason)

    def test_parent_of_char_char_keep(self):
        """PARENT_OF: both chars -> keep."""
        row = _make_row("eddard-stark", "robb-stark", "PARENT_OF")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")

    def test_spouse_of_char_char_keep(self):
        """SPOUSE_OF: both chars -> keep."""
        row = _make_row("eddard-stark", "catelyn-stark", "SPOUSE_OF")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")

    def test_spouse_of_non_char_source_char_target_flag(self):
        """SPOUSE_OF: source non-char but target IS char -> FLAG.

        This is the queen-cersei/robert smoke5 case: queen-cersei is a real
        person but her slug doesn't resolve to a character node.  The
        relationship is TRUE — flag it instead of dropping.
        """
        row = _make_row("queen-cersei", "robert-baratheon", "SPOUSE_OF")
        chars_with_robert = _CHARS | {"robert-baratheon"}
        self.assertTrue(_is_flag(row, chars_with_robert),
                        "Expected FLAG: queen-cersei not in char_slugs but robert is")
        d, reason = _disp(row, chars_with_robert)
        self.assertIn("CONTRACT_WARNING", reason)

    def test_spouse_of_char_non_char_target_flag(self):
        """SPOUSE_OF: source is char but target is non-char -> FLAG (not DROP)."""
        row = _make_row("eddard-stark", "winterfell", "SPOUSE_OF")
        self.assertTrue(_is_flag(row, _CHARS),
                        "Expected FLAG: one char endpoint means possible alias issue")

    def test_child_of_non_char_source_char_target_flag(self):
        """CHILD_OF: non-char source, char target -> FLAG."""
        row = _make_row("house-stark", "eddard-stark", "CHILD_OF")
        self.assertTrue(_is_flag(row, _CHARS),
                        "Expected FLAG: house-stark not char but eddard is")

    def test_lover_of_char_char_keep(self):
        """LOVER_OF: both chars -> keep."""
        row = _make_row("cersei-lannister", "jaime-lannister", "LOVER_OF")
        self.assertTrue(_is_keep(row, _CHARS | {"jaime-lannister"}), "Expected keep")

    def test_ygritte_loves_jon_keep(self):
        """LOVES: ygritte LOVES jon-snow — both chars -> keep (smoke5 row 25)."""
        # LOVES is not a kinship type, so no contract fires; both are chars anyway.
        row = _make_row("ygritte", "jon-snow", "LOVES")
        chars = _CHARS | {"ygritte"}
        self.assertTrue(_is_keep(row, chars), "Expected keep: LOVES has no char<->char contract")


class TestNonCharTargetContract(unittest.TestCase):
    """HOLDS_TITLE, GUEST_OF, RULES, SEAT_OF targets must not be characters."""

    def test_holds_title_char_target_drop(self):
        """HOLDS_TITLE: target is a character -> DROP."""
        row = _make_row("eddard-stark", "jon-snow", "HOLDS_TITLE")
        self.assertTrue(_is_drop(row, _CHARS))
        d, reason = _disp(row, _CHARS)
        self.assertIn("CONTRACT_VIOLATED", reason)

    def test_holds_title_title_target_keep(self):
        """HOLDS_TITLE: target is a title (non-char) -> keep."""
        row = _make_row("eddard-stark", "warden-of-the-north", "HOLDS_TITLE")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")

    def test_guest_of_char_target_keep(self):
        """GUEST_OF: target is a character -> keep (host is frequently a person: Guest -> Host)."""
        row = _make_row("tyrion-lannister", "catelyn-stark", "GUEST_OF")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep: GUEST_OF host can be a character")

    def test_guest_of_location_target_keep(self):
        """GUEST_OF: target is location (non-char) -> keep."""
        row = _make_row("tyrion-lannister", "winterfell", "GUEST_OF")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")

    def test_rules_char_target_retype(self):
        """RULES: target is a character -> RETYPE to COMMANDS (not DROP).

        Architecture: RULES = "Holds authority over a location or domain" (Ruler→Location).
                      COMMANDS = "Military or organizational command" (Commander→Subordinate).
        When the model emits RULES with a character target it confused interpersonal
        command with territorial rule.  The correct edge is COMMANDS, same direction.
        """
        row = _make_row("eddard-stark", "robb-stark", "RULES")
        self.assertTrue(_is_retype(row, _CHARS),
                        "Expected RETYPE: RULES with char target should become COMMANDS")
        d, reason = _disp(row, _CHARS)
        self.assertEqual(d, "retype", f"Must retype RULES→char, got {d!r}: {reason}")
        self.assertIn("COMMANDS", reason)
        self.assertIn("CONTRACT_RETYPE", reason)

    def test_rules_char_target_retype_v1_cases(self):
        """RULES char-target RETYPE: daenerys->barristan and daenerys->grey-worm (v1 cases)."""
        for tgt in ("barristan-selmy", "grey-worm", "tommen-baratheon"):
            chars = _CHARS | {tgt}
            row = _make_row("daenerys-targaryen", tgt, "RULES")
            d, reason = _disp(row, chars)
            self.assertEqual(d, "retype",
                             f"RULES->{tgt} should RETYPE to COMMANDS, got {d!r}: {reason}")
            self.assertIn("COMMANDS", reason)

    def test_rules_location_target_keep(self):
        """RULES: target is location (non-char) -> keep (no contract fires)."""
        row = _make_row("eddard-stark", "winterfell", "RULES")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep: RULES->location is valid")

    def test_seat_of_char_target_drop(self):
        """SEAT_OF: target is a character -> DROP."""
        row = _make_row("winterfell", "eddard-stark", "SEAT_OF")
        self.assertTrue(_is_drop(row, _CHARS))

    def test_seat_of_house_target_keep(self):
        """SEAT_OF: target is house (non-char) -> keep."""
        row = _make_row("winterfell", "house-stark", "SEAT_OF")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")


class TestRulesRetypeContract(unittest.TestCase):
    """RULES + character target → RETYPE to COMMANDS.

    Architecture: RULES = Ruler→Location; COMMANDS = Commander→Subordinate (character).
    When RULES has a character target the model confused interpersonal command with
    territorial rule.  The correct edge is COMMANDS (same direction, character target).
    """

    def test_rules_char_target_retype(self):
        """RULES: char target -> RETYPE (not DROP, not KEEP)."""
        row = _make_row("eddard-stark", "robb-stark", "RULES")
        self.assertTrue(_is_retype(row, _CHARS))
        d, reason = _disp(row, _CHARS)
        self.assertEqual(d, "retype")
        self.assertIn("CONTRACT_RETYPE", reason)
        self.assertIn("COMMANDS", reason)

    def test_rules_char_target_retype_daenerys_barristan(self):
        """RULES->barristan-selmy (v1 case): RETYPE to COMMANDS."""
        chars = _CHARS  # barristan-selmy already in _CHARS
        row = _make_row("daenerys-targaryen", "barristan-selmy", "RULES")
        d, reason = _disp(row, chars)
        self.assertEqual(d, "retype", f"Expected retype, got {d!r}: {reason}")
        self.assertIn("COMMANDS", reason)

    def test_rules_location_target_keep(self):
        """RULES: non-char target (location) -> KEEP (no contract fires)."""
        row = _make_row("eddard-stark", "winterfell", "RULES")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep: RULES->location is valid")

    def test_rules_location_target_keep_meereen(self):
        """RULES->meereen (v1 case): KEEP (meereen is a location, not a character)."""
        row = _make_row("daenerys-targaryen", "meereen", "RULES")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep: meereen is a location")

    def test_rules_non_char_target_keep_vale(self):
        """RULES->vale-of-arryn (v1 case): KEEP."""
        row = _make_row("petyr-baelish", "vale-of-arryn", "RULES")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep: vale-of-arryn is not a char")


class TestRetypePayload(unittest.TestCase):
    """Verify the retype reason payload encodes the new edge_type for the CLI to apply."""

    def test_retype_reason_encodes_new_type(self):
        """Retype reason must contain 'retype_to=COMMANDS' for the CLI to parse."""
        row = _make_row("daenerys-targaryen", "barristan-selmy", "RULES")
        chars = _CHARS  # barristan-selmy in _CHARS
        d, reason = _disp(row, chars)
        self.assertEqual(d, "retype")
        self.assertIn("retype_to=COMMANDS", reason)

    def test_retype_preserves_source_and_target(self):
        """CLI retype logic: applying retype rewrites edge_type; source/target unchanged."""
        row = _make_row("daenerys-targaryen", "barristan-selmy", "RULES",
                        quote="Ser Barristan knelt before her.")
        chars = _CHARS
        d, reason = _disp(row, chars)
        self.assertEqual(d, "retype")
        # Simulate CLI retype logic
        retyped = dict(row)
        orig_et = retyped["edge_type"]
        new_et = "COMMANDS"
        if "retype_to=" in reason:
            new_et = reason.split("retype_to=")[-1].strip().rstrip(")")
        retyped["edge_type"]     = new_et
        retyped["_retyped_from"] = orig_et
        retyped["_retype_reason"] = reason
        # edge_type is now COMMANDS
        self.assertEqual(retyped["edge_type"], "COMMANDS")
        # Original edge_type preserved in _retyped_from
        self.assertEqual(retyped["_retyped_from"], "RULES")
        # source/target unchanged
        self.assertEqual(retyped["source_slug"], "daenerys-targaryen")
        self.assertEqual(retyped["target_slug"], "barristan-selmy")
        # evidence_quote preserved
        self.assertIn("Ser Barristan", retyped["evidence_quote"])


class TestValidRowsKeep(unittest.TestCase):
    """Edge types with no contract violations must keep."""

    def test_opposes_char_char_keep(self):
        row = _make_row("arya-stark", "joffrey-baratheon", "OPPOSES")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")

    def test_serves_char_char_keep(self):
        row = _make_row("bronn", "tyrion-lannister", "SERVES")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")

    def test_respects_char_char_keep(self):
        """RESPECTS has no contract restriction — must keep."""
        row = _make_row("brienne-tarth", "catelyn-stark", "RESPECTS")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")

    def test_member_of_char_faction_keep(self):
        row = _make_row("jon-snow", "house-stark", "MEMBER_OF")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")

    def test_no_edge_type_keep(self):
        """Row with no edge_type has no contract to enforce -> keep."""
        row = {"source_slug": "arya-stark", "target_slug": "jon-snow", "edge_type": ""}
        self.assertTrue(_is_keep(row, _CHARS))


class TestCommandsContract(unittest.TestCase):
    """COMMANDS target must be a character (the person being commanded)."""

    def test_commands_char_target_keep(self):
        """COMMANDS: target is a character (the commanded person) -> keep."""
        row = _make_row("mormont", "jon-snow", "COMMANDS")
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")

    def test_commands_non_char_target_drop(self):
        """COMMANDS: target is a non-character (place/group/faction) -> DROP (two-hop collapse)."""
        row = _make_row("robert-baratheon", "kingsguard", "COMMANDS")
        # kingsguard is not in _CHARS (it's a group, not a character)
        chars_with_robert = _CHARS | {"robert-baratheon"}
        self.assertTrue(_is_drop(row, chars_with_robert))
        d, reason = _disp(row, chars_with_robert)
        self.assertIn("CONTRACT_VIOLATED", reason)
        self.assertIn("two-hop", reason)

    def test_commands_non_char_target_faction_drop(self):
        """COMMANDS: target is a faction slug -> DROP."""
        row = _make_row("cersei-lannister", "faith-of-the-seven", "COMMANDS")
        self.assertTrue(_is_drop(row, _CHARS))
        d, reason = _disp(row, _CHARS)
        self.assertIn("CONTRACT_VIOLATED", reason)

    def test_commands_location_target_drop(self):
        """COMMANDS: target is a location -> DROP."""
        row = _make_row("tyrion-lannister", "winterfell", "COMMANDS")
        self.assertTrue(_is_drop(row, _CHARS))
        d, reason = _disp(row, _CHARS)
        self.assertIn("CONTRACT_VIOLATED", reason)


class TestMotivatesContract(unittest.TestCase):
    """MOTIVATES source must NOT be a character (event/condition -> actor)."""

    def test_motivates_char_source_drop(self):
        """MOTIVATES: source is a character -> DROP (person-as-source direction error)."""
        row = _make_row("jon-snow", "arya-stark", "MOTIVATES")
        row["evidence_quote"] = "He rallied them all."
        self.assertTrue(_is_drop(row, _CHARS))
        d, reason = _disp(row, _CHARS)
        self.assertIn("CONTRACT_VIOLATED", reason)
        self.assertIn("direction error", reason)

    def test_motivates_event_source_char_target_keep(self):
        """MOTIVATES: source is an event (non-char) -> keep (correct event->actor direction)."""
        row = _make_row("red-wedding", "arya-stark", "MOTIVATES")
        row["evidence_quote"] = "The Red Wedding changed everything for her."
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")

    def test_motivates_event_source_non_char_target_keep(self):
        """MOTIVATES: event source, non-char target -> keep (no source-type violation)."""
        row = _make_row("war-of-the-five-kings", "house-stark", "MOTIVATES")
        row["evidence_quote"] = "The war shattered the North."
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")

    def test_motivates_char_char_drop(self):
        """MOTIVATES: both endpoints are characters -> DROP (char source fires first)."""
        row = _make_row("tyrion-lannister", "cersei-lannister", "MOTIVATES")
        row["evidence_quote"] = "His scheming drove her to act."
        self.assertTrue(_is_drop(row, _CHARS))
        d, reason = _disp(row, _CHARS)
        self.assertIn("CONTRACT_VIOLATED", reason)


class TestEmptyEvidenceContract(unittest.TestCase):
    """Any edge whose evidence_quote is empty or whitespace is dropped."""

    def test_empty_quote_drop(self):
        """Empty evidence_quote -> DROP."""
        row = {
            "source_slug": "jon-connington",
            "target_slug": "tyrion-lannister",
            "edge_type": "COMMANDS",
            "evidence_quote": "",
        }
        chars = _CHARS | {"jon-connington", "tyrion-lannister"}
        self.assertTrue(_is_drop(row, chars))
        d, reason = _disp(row, chars)
        self.assertIn("evidence_quote is empty", reason)

    def test_whitespace_only_quote_drop(self):
        """Whitespace-only evidence_quote -> DROP."""
        row = {
            "source_slug": "arya-stark",
            "target_slug": "jon-snow",
            "edge_type": "RESPECTS",
            "evidence_quote": "   \t  ",
        }
        self.assertTrue(_is_drop(row, _CHARS))
        d, reason = _disp(row, _CHARS)
        self.assertIn("evidence_quote is empty", reason)

    def test_missing_quote_key_drop(self):
        """Missing evidence_quote key (key absent entirely) -> DROP (treated as empty)."""
        row = {
            "source_slug": "arya-stark",
            "target_slug": "jon-snow",
            "edge_type": "RESPECTS",
            # evidence_quote key intentionally absent
        }
        self.assertTrue(_is_drop(row, _CHARS))
        d, reason = _disp(row, _CHARS)
        self.assertIn("evidence_quote is empty", reason)

    def test_nonempty_quote_passes_contract(self):
        """Non-empty evidence_quote does not trigger empty-quote contract."""
        row = {
            "source_slug": "arya-stark",
            "target_slug": "jon-snow",
            "edge_type": "RESPECTS",
            "evidence_quote": "She missed him every day.",
        }
        self.assertTrue(_is_keep(row, _CHARS), "Expected keep")


class TestBuildCharacterSlugs(unittest.TestCase):
    """build_character_slugs: basic filesystem check (uses real graph/nodes if available)."""

    def test_returns_frozenset(self):
        """Function returns a frozenset."""
        from pathlib import Path
        nodes_dir = Path(__file__).resolve().parent.parent / "graph" / "nodes"
        if not nodes_dir.is_dir():
            self.skipTest("graph/nodes not available")
        result = tcv.build_character_slugs(nodes_dir)
        self.assertIsInstance(result, frozenset)

    def test_known_characters_present(self):
        """Spot-check that a few well-known character slugs are in the set."""
        from pathlib import Path
        nodes_dir = Path(__file__).resolve().parent.parent / "graph" / "nodes"
        if not (nodes_dir / "characters").is_dir():
            self.skipTest("graph/nodes/characters not available")
        result = tcv.build_character_slugs(nodes_dir)
        for slug in ("eddard-stark", "cersei-lannister", "tyrion-lannister"):
            self.assertIn(slug, result, f"Expected {slug!r} in character slugs")

    def test_missing_nodes_dir_returns_empty(self):
        """Missing nodes dir -> empty frozenset (no crash)."""
        from pathlib import Path
        result = tcv.build_character_slugs(Path("/nonexistent/graph/nodes"))
        self.assertIsInstance(result, frozenset)
        self.assertEqual(len(result), 0)


# ---------------------------------------------------------------------------
# Helpers for category-based contract tests
# ---------------------------------------------------------------------------

# Minimal slug→category index for in-memory tests.
# Covers the smoke5 error cases and conservative unknown-slug cases.
_CAT_INDEX = {
    # artifacts (object-ish)
    "summer-sun":           "artifacts",
    "josos-prank":          "artifacts",
    "needle":               "artifacts",
    # locations
    "north":                "locations",
    "winterfell":           "locations",
    "kings-landing":        "locations",
    # factions / houses (org sources)
    "nights-watch":         "factions",
    "house-stark":          "houses",
    "lannister-army":       "factions",
    # characters (present in _CHARS too)
    "jon-snow":             "characters",
    "tyrion-lannister":     "characters",
    "robb-stark":           "characters",
    "daenerys-targaryen":   "characters",
    "illyrio-mopatis":      "characters",
}


class TestContractedWithTargetNotObject(unittest.TestCase):
    """Contract 7: CONTRACTED_WITH target must not be an object-ish category."""

    def _d(self, src, tgt):
        row = _make_row(src, tgt, "CONTRACTED_WITH")
        return _disp(row, _CHARS | {src}, _CAT_INDEX)

    def test_contracted_with_artifact_target_drop(self):
        """CONTRACTED_WITH target is an artifact -> DROP."""
        d, reason = self._d("illyrio-mopatis", "summer-sun")
        self.assertEqual(d, "drop", "Expected DROP: artifact target")
        self.assertIn("CONTRACT_VIOLATED", reason)
        self.assertIn("object category", reason)

    def test_contracted_with_artifact_target_josos_drop(self):
        """CONTRACTED_WITH target is another artifact (josos-prank) -> DROP."""
        d, reason = self._d("illyrio-mopatis", "josos-prank")
        self.assertEqual(d, "drop", "Expected DROP: artifact target")
        self.assertIn("CONTRACT_VIOLATED", reason)

    def test_contracted_with_person_target_keep(self):
        """CONTRACTED_WITH target is a character -> keep."""
        d, reason = self._d("illyrio-mopatis", "tyrion-lannister")
        self.assertEqual(d, "keep", f"Expected keep: {reason}")

    def test_contracted_with_unknown_target_no_drop(self):
        """CONTRACTED_WITH target has no node (unknown) -> keep (conservative: no drop on unknown)."""
        row = _make_row("illyrio-mopatis", "unknown-smuggler", "CONTRACTED_WITH")
        d, reason = _disp(row, _CHARS | {"illyrio-mopatis"}, _CAT_INDEX)
        self.assertEqual(d, "keep", f"Expected keep for unknown target: {reason}")

    def test_contracted_with_no_index_no_drop(self):
        """CONTRACTED_WITH with slug_category_index=None -> keep (contracts skipped)."""
        row = _make_row("illyrio-mopatis", "summer-sun", "CONTRACTED_WITH")
        d, reason = _disp(row, _CHARS | {"illyrio-mopatis"}, None)
        self.assertEqual(d, "keep", f"Expected keep when no index: {reason}")


class TestMemberOfDirectionContract(unittest.TestCase):
    """Contract 8: MEMBER_OF direction — faction/house source -> character target is reversed.

    Now returns FLIP instead of DROP.
    """

    def _d(self, src, tgt):
        row = _make_row(src, tgt, "MEMBER_OF")
        return _disp(row, _CHARS, _CAT_INDEX)

    def test_member_of_faction_source_char_target_flip(self):
        """MEMBER_OF: faction source -> character target -> FLIP (not DROP)."""
        d, reason = self._d("nights-watch", "jon-snow")
        self.assertEqual(d, "flip", "Expected FLIP: reversed MEMBER_OF direction")
        self.assertIn("CONTRACT_FLIP", reason)
        self.assertIn("direction reversed", reason)

    def test_member_of_house_source_char_target_flip(self):
        """MEMBER_OF: house source -> character target -> FLIP."""
        d, reason = self._d("house-stark", "robb-stark")
        self.assertEqual(d, "flip", "Expected FLIP: reversed MEMBER_OF direction")
        self.assertIn("CONTRACT_FLIP", reason)

    def test_member_of_char_faction_target_keep(self):
        """MEMBER_OF: character source -> faction target -> keep (correct direction)."""
        d, reason = self._d("jon-snow", "nights-watch")
        self.assertEqual(d, "keep", f"Expected keep: {reason}")

    def test_member_of_unknown_source_no_flip(self):
        """MEMBER_OF: unknown source slug -> keep (conservative: don't flip on unknown)."""
        row = _make_row("some-unknown-group", "jon-snow", "MEMBER_OF")
        d, reason = _disp(row, _CHARS, _CAT_INDEX)
        self.assertEqual(d, "keep", f"Expected keep for unknown source: {reason}")

    def test_member_of_faction_unknown_target_no_flip(self):
        """MEMBER_OF: faction source + unknown target -> keep (target must resolve to chars to flip)."""
        row = _make_row("nights-watch", "unknown-recruit", "MEMBER_OF")
        d, reason = _disp(row, _CHARS, _CAT_INDEX)
        self.assertEqual(d, "keep", f"Expected keep for unknown target: {reason}")

    def test_member_of_no_index_no_flip(self):
        """MEMBER_OF with slug_category_index=None -> keep (contracts skipped)."""
        row = _make_row("nights-watch", "jon-snow", "MEMBER_OF")
        d, reason = _disp(row, _CHARS, None)
        self.assertEqual(d, "keep", f"Expected keep when no index: {reason}")


class TestMemberOfFlipPayload(unittest.TestCase):
    """When type_contract_pass returns 'flip' for MEMBER_OF, the CLI should swap endpoints.

    These tests verify the flip reason contains enough info for the CLI to perform the swap.
    """

    def test_flip_reason_contains_reversed_slugs(self):
        """Flip reason mentions both original source and target for swap context."""
        row = _make_row("nights-watch", "jon-snow", "MEMBER_OF")
        d, reason = _disp(row, _CHARS, _CAT_INDEX)
        self.assertEqual(d, "flip")
        # Reason should identify what the correct direction is
        self.assertIn("jon-snow", reason)
        self.assertIn("nights-watch", reason)

    def test_flipped_row_has_swapped_endpoints(self):
        """CLI flip logic: applying the flip should yield jon-snow -> nights-watch."""
        row = _make_row("nights-watch", "jon-snow", "MEMBER_OF")
        d, reason = _disp(row, _CHARS, _CAT_INDEX)
        self.assertEqual(d, "flip")
        # Simulate what the CLI does on a flip
        flipped = dict(row)
        orig_src = flipped["source_slug"]
        orig_tgt = flipped["target_slug"]
        flipped["source_slug"] = orig_tgt   # jon-snow
        flipped["target_slug"] = orig_src   # nights-watch
        flipped["_flipped"] = True
        flipped["_flip_reason"] = reason
        self.assertEqual(flipped["source_slug"], "jon-snow")
        self.assertEqual(flipped["target_slug"], "nights-watch")
        self.assertTrue(flipped["_flipped"])


class TestHoldsTitleTargetNotPlace(unittest.TestCase):
    """Contract 9: HOLDS_TITLE target must not be a location/region.

    Now returns FLAG (not DROP) for location targets — the relationship is TRUE
    but needs retargeting.
    """

    def _d(self, src, tgt):
        row = _make_row(src, tgt, "HOLDS_TITLE")
        return _disp(row, _CHARS, _CAT_INDEX)

    def test_holds_title_location_target_flag(self):
        """HOLDS_TITLE: target is a location (north) -> FLAG (not DROP).

        'robb HOLDS_TITLE north' = King in the North — a TRUE relationship.
        The target needs retargeting to a title node, not deletion.
        """
        d, reason = self._d("robb-stark", "north")
        self.assertEqual(d, "flag", "Expected FLAG: location target is true relationship needing retarget")
        self.assertIn("CONTRACT_WARNING", reason)
        self.assertIn("location", reason)

    def test_holds_title_winterfell_location_flag(self):
        """HOLDS_TITLE: target is another location -> FLAG."""
        d, reason = self._d("eddard-stark", "winterfell")
        self.assertEqual(d, "flag", "Expected FLAG: location target")
        self.assertIn("CONTRACT_WARNING", reason)

    def test_holds_title_title_slug_keep(self):
        """HOLDS_TITLE: target is a title/non-location -> keep."""
        # "warden-of-the-north" is not in _CAT_INDEX (no node), so no location flag fires
        row = _make_row("eddard-stark", "warden-of-the-north", "HOLDS_TITLE")
        d, reason = _disp(row, _CHARS, _CAT_INDEX)
        self.assertEqual(d, "keep", f"Expected keep: {reason}")

    def test_holds_title_char_target_still_drops(self):
        """HOLDS_TITLE: char target still drops (Contract 3 fires before Contract 9)."""
        d, reason = self._d("eddard-stark", "jon-snow")
        self.assertEqual(d, "drop", "Expected DROP: char target (existing contract)")
        self.assertIn("CONTRACT_VIOLATED", reason)

    def test_holds_title_no_index_location_no_flag(self):
        """HOLDS_TITLE with slug_category_index=None: location target is NOT flagged (contracts skipped)."""
        row = _make_row("robb-stark", "north", "HOLDS_TITLE")
        # "north" is NOT a character, so Contract 3 won't fire; Contract 9 also skipped (no index)
        d, reason = _disp(row, _CHARS, None)
        self.assertEqual(d, "keep", f"Expected keep when no index: {reason}")

    def test_flagged_row_has_retarget_hint(self):
        """Flagged HOLDS_TITLE/location row should mention retargeting in reason."""
        d, reason = self._d("robb-stark", "north")
        self.assertEqual(d, "flag")
        self.assertIn("retarget", reason.lower())


class TestHoldsTitleFlagAnnotation(unittest.TestCase):
    """Verify the flag annotation fields are correct when the CLI processes a flagged row."""

    def test_flag_annotation_fields(self):
        """CLI flag logic: flagged row gets _contract_warning=True and _contract_reason."""
        row = _make_row("robb-stark", "north", "HOLDS_TITLE")
        d, reason = _disp(row, _CHARS, _CAT_INDEX)
        self.assertEqual(d, "flag")
        # Simulate CLI annotation
        annotated = dict(row)
        annotated["_contract_warning"] = True
        annotated["_contract_reason"] = reason
        self.assertTrue(annotated["_contract_warning"])
        self.assertIn("CONTRACT_WARNING", annotated["_contract_reason"])
        # Original fields preserved
        self.assertEqual(annotated["source_slug"], "robb-stark")
        self.assertEqual(annotated["target_slug"], "north")
        self.assertEqual(annotated["edge_type"], "HOLDS_TITLE")


class TestBuildSlugCategoryIndex(unittest.TestCase):
    """build_slug_category_index: filesystem scan."""

    def test_real_graph_nodes(self):
        """Real graph/nodes: summer-sun→artifacts, north→locations, jon-snow→characters."""
        from pathlib import Path
        nodes_dir = Path(__file__).resolve().parent.parent / "graph" / "nodes"
        if not nodes_dir.is_dir():
            self.skipTest("graph/nodes not available")
        idx = tcv.build_slug_category_index(nodes_dir)
        self.assertIsInstance(idx, dict)
        # The smoke5 error cases must resolve correctly
        self.assertEqual(idx.get("summer-sun"),  "artifacts",  "summer-sun must be artifacts")
        self.assertEqual(idx.get("josos-prank"), "artifacts",  "josos-prank must be artifacts")
        self.assertEqual(idx.get("north"),        "locations",  "north must be locations")
        self.assertEqual(idx.get("jon-snow"),     "characters", "jon-snow must be characters")
        self.assertEqual(idx.get("nights-watch"), "factions",   "nights-watch must be factions")

    def test_missing_nodes_dir_returns_empty(self):
        """Missing nodes dir -> empty dict (no crash)."""
        from pathlib import Path
        idx = tcv.build_slug_category_index(Path("/nonexistent/graph/nodes"))
        self.assertIsInstance(idx, dict)
        self.assertEqual(len(idx), 0)

    def test_underscore_dirs_excluded(self):
        """Dirs starting with '_' (e.g. _unclassified) are not indexed."""
        from pathlib import Path
        nodes_dir = Path(__file__).resolve().parent.parent / "graph" / "nodes"
        if not nodes_dir.is_dir():
            self.skipTest("graph/nodes not available")
        idx = tcv.build_slug_category_index(nodes_dir)
        for slug, cat in idx.items():
            self.assertFalse(cat.startswith("_"), f"Category {cat!r} for {slug!r} starts with '_'")


class TestDispositionAPIContract(unittest.TestCase):
    """type_contract_pass always returns (str, str) with disposition in the valid set."""

    _VALID_DISPOSITIONS = {"keep", "drop", "flip", "flag", "retype"}

    def _check(self, row, chars, cat=None):
        result = tcv.type_contract_pass(row, chars, cat)
        self.assertIsInstance(result, tuple, "Must return a tuple")
        self.assertEqual(len(result), 2, "Must return a 2-tuple")
        d, reason = result
        self.assertIsInstance(d, str, "Disposition must be str")
        self.assertIsInstance(reason, str, "Reason must be str")
        self.assertIn(d, self._VALID_DISPOSITIONS, f"Disposition {d!r} not in valid set")
        return d, reason

    def test_keep_row_returns_str(self):
        row = _make_row("arya-stark", "jon-snow", "RESPECTS")
        self._check(row, _CHARS)

    def test_drop_row_returns_str(self):
        # Use CONTEMPORARY_WITH char<->char as the canonical DROP case
        # (ECHOES char<->char is now KEEP per architecture fix)
        row = _make_row("arya-stark", "jon-snow", "CONTEMPORARY_WITH")
        self._check(row, _CHARS)

    def test_flip_row_returns_str(self):
        row = _make_row("nights-watch", "jon-snow", "MEMBER_OF")
        self._check(row, _CHARS, _CAT_INDEX)

    def test_flag_row_returns_str(self):
        row = _make_row("robb-stark", "north", "HOLDS_TITLE")
        self._check(row, _CHARS, _CAT_INDEX)

    def test_retype_row_returns_str(self):
        """RULES->char returns retype disposition."""
        row = _make_row("daenerys-targaryen", "barristan-selmy", "RULES")
        chars = _CHARS | {"barristan-selmy"}
        self._check(row, chars)

    def test_all_dispositions_reachable(self):
        """Confirm all five dispositions are reachable via distinct inputs."""
        chars_extended = _CHARS | {"barristan-selmy"}
        rows_by_expected = {
            "keep":   (_make_row("arya-stark", "jon-snow", "RESPECTS"), _CHARS, _CAT_INDEX),
            # ECHOES char<->char now KEEPS; use CONTEMPORARY_WITH for a DROP case
            "drop":   (_make_row("arya-stark", "jon-snow", "CONTEMPORARY_WITH"), _CHARS, _CAT_INDEX),
            "flip":   (_make_row("nights-watch", "jon-snow", "MEMBER_OF"), _CHARS, _CAT_INDEX),
            "flag":   (_make_row("robb-stark", "north", "HOLDS_TITLE"), _CHARS, _CAT_INDEX),
            "retype": (_make_row("daenerys-targaryen", "barristan-selmy", "RULES"),
                       chars_extended, _CAT_INDEX),
        }
        seen = set()
        for expected, (row, chars, cat) in rows_by_expected.items():
            d, _ = _disp(row, chars, cat)
            self.assertEqual(d, expected, f"Expected {expected!r} but got {d!r}")
            seen.add(d)
        self.assertEqual(seen, self._VALID_DISPOSITIONS)


class TestSmoke5KnownCases(unittest.TestCase):
    """Regression tests for the specific smoke5 rows that drove this refactor.

    These use the real graph/nodes filesystem.
    """

    @classmethod
    def setUpClass(cls):
        from pathlib import Path
        nodes_dir = Path(__file__).resolve().parent.parent / "graph" / "nodes"
        if not nodes_dir.is_dir():
            cls._skip = True
            return
        cls._skip = False
        cls.char_slugs = tcv.build_character_slugs(nodes_dir)
        cls.cat_index = tcv.build_slug_category_index(nodes_dir)

    def _d(self, src, tgt, et, quote="Test quote supporting this edge."):
        if self._skip:
            self.skipTest("graph/nodes not available")
        row = _make_row(src, tgt, et, quote)
        return _disp(row, self.char_slugs, self.cat_index)

    # --- CORRECT DROPS (genuinely wrong edges, should still DROP) ---

    def test_illyrio_contracted_with_summer_sun_drop(self):
        """illyrio CONTRACTED_WITH summer-sun: artifact target -> still DROP."""
        d, reason = self._d("illyrio-mopatis", "summer-sun", "CONTRACTED_WITH")
        self.assertEqual(d, "drop", "Ships are not contracting parties — must DROP")

    def test_illyrio_contracted_with_josos_prank_drop(self):
        """illyrio CONTRACTED_WITH josos-prank: artifact target -> still DROP."""
        d, reason = self._d("illyrio-mopatis", "josos-prank", "CONTRACTED_WITH")
        self.assertEqual(d, "drop", "Ships are not contracting parties — must DROP")

    # --- TRUE EDGES NOW PRESERVED ---

    def test_nights_watch_member_of_jon_flips(self):
        """nights-watch MEMBER_OF jon-snow: direction reversed -> FLIP (not DROP).

        The true edge is jon-snow MEMBER_OF nights-watch.
        """
        d, reason = self._d("nights-watch", "jon-snow", "MEMBER_OF")
        self.assertEqual(d, "flip",
                         "nights-watch→jon MEMBER_OF is reversed; should FLIP to jon→nights-watch")

    def test_robb_holds_title_north_flags(self):
        """robb-stark HOLDS_TITLE north: King in the North is TRUE -> FLAG (not DROP)."""
        d, reason = self._d("robb-stark", "north", "HOLDS_TITLE")
        self.assertEqual(d, "flag",
                         "King in the North is a real relationship; should FLAG not DROP")
        self.assertIn("retarget", reason.lower())

    def test_queen_cersei_spouse_of_robert_flags(self):
        """queen-cersei SPOUSE_OF robert-i-baratheon: TRUE but slug alias -> FLAG (not DROP).

        queen-cersei resolves to 'artifacts' in the graph (redirect stub),
        not to characters.  The marriage is canonically true.
        """
        d, reason = self._d("queen-cersei", "robert-i-baratheon", "SPOUSE_OF")
        self.assertEqual(d, "flag",
                         "Cersei IS Robert's spouse; queen-cersei slug alias should FLAG not DROP")

    def test_daenerys_spouse_of_drogo_keeps(self):
        """daenerys-targaryen SPOUSE_OF drogo: both in chars -> keep (smoke5 row 3)."""
        d, reason = self._d("daenerys-targaryen", "drogo", "SPOUSE_OF")
        self.assertEqual(d, "keep", f"daenerys/drogo are both chars: {reason}")

    def test_cersei_lannister_spouse_of_robert_keeps(self):
        """cersei-lannister SPOUSE_OF robert-i-baratheon: correct slug, both chars -> keep."""
        d, reason = self._d("cersei-lannister", "robert-i-baratheon", "SPOUSE_OF")
        self.assertEqual(d, "keep",
                         "cersei-lannister (not queen-cersei) is the correct slug and both are chars")


if __name__ == "__main__":
    unittest.main()
