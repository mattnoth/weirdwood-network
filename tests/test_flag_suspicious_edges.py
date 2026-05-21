"""Tests for scripts/wiki-pass2-flag-suspicious-edges.py.

Six pattern detectors (Session 58 STEP 4). The flagger drives the
post-Stage-4 Opus review prioritization, so false-positive and false-negative
behavior matters.

Run: python3 -m unittest tests.test_flag_suspicious_edges -v
"""

import unittest

from tests._helpers import load_script

flagger = load_script("wiki-pass2-flag-suspicious-edges.py")


def emit(edge_type: str, **extra) -> dict:
    """Build a minimal emit_edge row for testing pattern checks."""
    return {
        "decision": "emit_edge",
        "edge_type": edge_type,
        "source_slug": extra.pop("source", "src-slug"),
        "target_slug": extra.pop("target", "tgt-slug"),
        "evidence_snippet": extra.pop("snippet", "Some evidence text here, longer than twenty chars."),
        "confidence_tier": extra.pop("confidence_tier", 1),
        **extra,
    }


class TestKnowsAsFallback(unittest.TestCase):
    """Pattern 1: KNOWS without a knowing-verb in the snippet."""

    def test_knows_with_knowing_verb_passes(self):
        row = emit("KNOWS", snippet="Tyrion knew Bronn from his sellsword days.")
        self.assertEqual(flagger.check_patterns(row, slug_type={}), [])

    def test_knows_without_verb_flagged(self):
        row = emit("KNOWS", snippet="Both appear in chapter seven, walking the battlements.")
        flags = flagger.check_patterns(row, slug_type={})
        self.assertIn("knows_as_fallback", flags)

    def test_knows_recognized_passes(self):
        row = emit("KNOWS", snippet="Sansa recognized the sigil on his cloak.")
        self.assertEqual(flagger.check_patterns(row, slug_type={}), [])

    def test_non_knows_edge_unaffected(self):
        row = emit("LOCATED_AT", snippet="No knowing verb here.")
        self.assertNotIn("knows_as_fallback", flagger.check_patterns(row, slug_type={}))


class TestAttendsNonEvent(unittest.TestCase):
    """Pattern 2: ATTENDS targeting a non-event entity."""

    def test_attends_event_target_passes(self):
        row = emit("ATTENDS", target="purple-wedding")
        slug_type = {"purple-wedding": "event.feast"}
        self.assertEqual(flagger.check_patterns(row, slug_type), [])

    def test_attends_character_target_flagged(self):
        row = emit("ATTENDS", target="cersei-lannister")
        slug_type = {"cersei-lannister": "character"}
        self.assertIn("attends_non_event", flagger.check_patterns(row, slug_type))

    def test_attends_unknown_target_flagged_conservative(self):
        """Conservative: target slug present but not in index → flag."""
        row = emit("ATTENDS", target="unknown-thing")
        self.assertIn("attends_non_event", flagger.check_patterns(row, slug_type={}))


class TestFightsInNonEvent(unittest.TestCase):
    """Pattern 3: FIGHTS_IN targeting a non-event entity."""

    def test_fights_in_battle_passes(self):
        row = emit("FIGHTS_IN", target="battle-of-the-blackwater")
        slug_type = {"battle-of-the-blackwater": "event.battle"}
        self.assertEqual(flagger.check_patterns(row, slug_type), [])

    def test_fights_in_place_flagged(self):
        row = emit("FIGHTS_IN", target="kings-landing")
        slug_type = {"kings-landing": "place.city"}
        self.assertIn("fights_in_non_event", flagger.check_patterns(row, slug_type))


class TestKilledByNonPerson(unittest.TestCase):
    """Pattern 4: KILLED_BY with non-person source (allowed: character, creature, artifact/weapon)."""

    def test_killed_by_character_passes(self):
        row = emit("KILLED_BY", source="bronn", target="ser-vardis")
        slug_type = {"bronn": "character", "ser-vardis": "character"}
        self.assertEqual(flagger.check_patterns(row, slug_type), [])

    def test_killed_by_creature_passes(self):
        row = emit("KILLED_BY", source="drogon", target="warlock")
        slug_type = {"drogon": "creature.dragon", "warlock": "character"}
        self.assertEqual(flagger.check_patterns(row, slug_type), [])

    def test_killed_by_artifact_passes(self):
        """Weapons are valid KILLED_BY sources."""
        row = emit("KILLED_BY", source="ice", target="ned-stark")
        slug_type = {"ice": "object.artifact", "ned-stark": "character"}
        self.assertEqual(flagger.check_patterns(row, slug_type), [])

    def test_killed_by_place_flagged(self):
        row = emit("KILLED_BY", source="winterfell", target="someone")
        slug_type = {"winterfell": "place.castle"}
        self.assertIn("killed_by_non_person", flagger.check_patterns(row, slug_type))


class TestTier3WeakEvidence(unittest.TestCase):
    """Pattern 5: Tier-3 confidence with weak/absent snippet."""

    def test_tier3_with_long_snippet_passes(self):
        row = emit("LOCATED_AT",
                   snippet="A long enough piece of evidence text to clear the 20-char minimum.",
                   confidence_tier=3)
        self.assertNotIn("tier3_weak_evidence", flagger.check_patterns(row, slug_type={}))

    def test_tier3_with_short_snippet_flagged(self):
        row = emit("LOCATED_AT", snippet="too short", confidence_tier=3)
        self.assertIn("tier3_weak_evidence", flagger.check_patterns(row, slug_type={}))

    def test_tier1_short_snippet_unaffected(self):
        """Pattern 5 only fires on Tier-3."""
        row = emit("LOCATED_AT", snippet="hi", confidence_tier=1)
        self.assertNotIn("tier3_weak_evidence", flagger.check_patterns(row, slug_type={}))


class TestContemporaryWithCharPair(unittest.TestCase):
    """Pattern 6: CONTEMPORARY_WITH on character pairs."""

    def test_char_pair_flagged(self):
        row = emit("CONTEMPORARY_WITH", source="cersei-lannister", target="catelyn-stark")
        slug_type = {"cersei-lannister": "character", "catelyn-stark": "character"}
        self.assertIn("contemporary_with_char_pair", flagger.check_patterns(row, slug_type))

    def test_event_pair_unaffected(self):
        row = emit("CONTEMPORARY_WITH", source="war-of-five-kings", target="dance-of-dragons")
        slug_type = {"war-of-five-kings": "event.war", "dance-of-dragons": "event.war"}
        self.assertEqual(flagger.check_patterns(row, slug_type), [])

    def test_char_to_event_unaffected(self):
        row = emit("CONTEMPORARY_WITH", source="jon-snow", target="battle-of-castle-black")
        slug_type = {"jon-snow": "character", "battle-of-castle-black": "event.battle"}
        self.assertEqual(flagger.check_patterns(row, slug_type), [])


class TestNonEmitRowsIgnored(unittest.TestCase):
    """Patterns only apply to emit_edge decisions."""

    def test_reject_row_returns_no_flags(self):
        row = {"decision": "reject_just_mention", "edge_type": "KNOWS"}
        self.assertEqual(flagger.check_patterns(row, slug_type={}), [])

    def test_escalate_row_returns_no_flags(self):
        row = {"decision": "escalate_cross_identity", "edge_type": "KNOWS"}
        self.assertEqual(flagger.check_patterns(row, slug_type={}), [])


if __name__ == "__main__":
    unittest.main()
