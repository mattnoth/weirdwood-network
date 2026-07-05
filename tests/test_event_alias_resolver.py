"""Tests for event_alias_resolver.py — S96 slug-discoverability fixes.

Tests the three new mechanisms added in S96:
  (a) Fuzzy / substring fallback
  (b) Victim-indexing for death/execution hubs
  (c) Character-name fallback via all-node index

Also verifies:
  - All pre-existing exact resolutions still work (backward compatibility)
  - True garbage → MISS (fuzzy threshold guards)
  - Output format extensions are backward compatible (slug, status, candidates)

These tests use the real on-disk graph data where possible, and synthetic
fixtures where isolated unit testing is needed.
"""

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parent.parent

# S191 (shim retirement Tier B): imports the weirwood_query package + the
# build_alias_table builder directly — previously loaded the
# scripts/event_alias_resolver.py compat shim via _helpers. The shim's
# load_lookup()/load_all_node_index() build-if-missing wrappers are
# re-composed on the `ear` namespace so the test bodies are unchanged.
sys.path.insert(0, str(REPO_ROOT / "graph" / "query"))
from build import build_alias_table as _builder  # noqa: E402
from weirwood_query import load as _wq_load  # noqa: E402
from weirwood_query import resolve as _wq_resolve  # noqa: E402
from weirwood_query.normalize import normalize, tokenize  # noqa: E402


def _load_lookup():
    if not _builder.OUTPUT_FILE.exists():
        _builder.build_and_save(verbose=False)
    return _wq_load.load_alias_lookup()


def _load_all_node_index():
    if not _builder.ALL_NODES_OUTPUT_FILE.exists():
        _builder.build_and_save(verbose=False)
    return _wq_load.load_all_node_index()


ear = SimpleNamespace(
    normalize=normalize,
    tokenize=tokenize,
    resolve=_wq_resolve.resolve,
    build_and_save=_builder.build_and_save,
    OUTPUT_FILE=_builder.OUTPUT_FILE,
    ALL_NODES_OUTPUT_FILE=_builder.ALL_NODES_OUTPUT_FILE,
    load_lookup=_load_lookup,
    load_all_node_index=_load_all_node_index,
    _victim_phrases=_builder._victim_phrases,
    _event_is_primary_death_of_victim=_builder._event_is_primary_death_of_victim,
    _parse_frontmatter_aliases=_builder._parse_frontmatter_aliases,
    _parse_aliases_from_fm=_builder._parse_aliases_from_fm,
)

_victim_phrases = ear._victim_phrases
_event_is_primary_death_of_victim = ear._event_is_primary_death_of_victim
_parse_frontmatter_aliases = ear._parse_frontmatter_aliases
_parse_aliases_from_fm = ear._parse_aliases_from_fm


# ---------------------------------------------------------------------------
# Unit tests — normalize / tokenize
# ---------------------------------------------------------------------------

class TestNormalize(unittest.TestCase):
    def test_strips_leading_the(self):
        self.assertEqual(normalize("the Red Wedding"), "red wedding")

    def test_strips_leading_a(self):
        self.assertEqual(normalize("a battle"), "battle")

    def test_lowercase(self):
        self.assertEqual(normalize("BATTLE OF TRIDENT"), "battle of trident")

    def test_collapses_whitespace(self):
        self.assertEqual(normalize("battle  of   trident"), "battle of trident")

    def test_no_stripping_of_mid_the(self):
        self.assertEqual(normalize("battle of the trident"), "battle of the trident")


class TestTokenize(unittest.TestCase):
    def test_strips_stop_words(self):
        tokens = tokenize("battle of the trident")
        self.assertNotIn("of", tokens)
        self.assertNotIn("the", tokens)
        self.assertIn("battle", tokens)
        self.assertIn("trident", tokens)

    def test_strips_interrogatives(self):
        tokens = tokenize("who killed robb stark")
        self.assertNotIn("who", tokens)
        self.assertIn("killed", tokens)
        self.assertIn("robb", tokens)
        self.assertIn("stark", tokens)

    def test_strips_auxiliary_verbs(self):
        tokens = tokenize("who is robb stark")
        self.assertNotIn("who", tokens)
        self.assertNotIn("is", tokens)
        self.assertIn("robb", tokens)

    def test_empty_string(self):
        self.assertEqual(tokenize(""), set())


# ---------------------------------------------------------------------------
# Unit tests — victim-phrase generation
# ---------------------------------------------------------------------------

class TestVictimPhrases(unittest.TestCase):
    def test_generates_possessive_death(self):
        phrases = _victim_phrases("Robb Stark")
        self.assertIn("robb stark's death", phrases)

    def test_generates_death_of(self):
        phrases = _victim_phrases("Robb Stark")
        self.assertIn("death of robb stark", phrases)

    def test_generates_who_killed(self):
        phrases = _victim_phrases("Robb Stark")
        self.assertIn("who killed robb stark", phrases)

    def test_generates_execution_variants(self):
        phrases = _victim_phrases("Eddard Stark")
        self.assertIn("eddard stark's execution", phrases)
        self.assertIn("execution of eddard stark", phrases)

    def test_phrases_are_normalized(self):
        # All returned phrases should survive round-trip normalization unchanged
        for phrase in _victim_phrases("Ned Stark"):
            self.assertEqual(normalize(phrase), phrase)


# ---------------------------------------------------------------------------
# Unit tests — primary-death-of-victim check
# ---------------------------------------------------------------------------

class TestPrimaryDeathCheck(unittest.TestCase):
    def test_robb_is_killed_passes(self):
        result = _event_is_primary_death_of_victim(
            "robb-stark", "robb-is-killed", {"robb-is-killed": "Robb is killed"}
        )
        self.assertTrue(result)

    def test_theon_urges_fails(self):
        # theon-urges-robb-to-kill-jaime contains "kill" (infinitive, excluded)
        # → should NOT pass the death keyword check
        result = _event_is_primary_death_of_victim(
            "robb-stark",
            "theon-urges-robb-to-kill-jaime",
            {"theon-urges-robb-to-kill-jaime": "Theon urges Robb to kill Jaime"},
        )
        self.assertFalse(result)

    def test_execution_of_eddard_passes(self):
        result = _event_is_primary_death_of_victim(
            "eddard-stark",
            "execution-of-eddard-stark",
            {"execution-of-eddard-stark": "Execution of Eddard Stark"},
        )
        self.assertTrue(result)

    def test_victim_not_in_slug_fails(self):
        # Event has death keyword but victim name not in slug or name
        result = _event_is_primary_death_of_victim(
            "robb-stark",
            "catelyn-is-killed",
            {"catelyn-is-killed": "Catelyn is killed"},
        )
        self.assertFalse(result)


# ---------------------------------------------------------------------------
# Unit tests — YAML alias parser
# ---------------------------------------------------------------------------

class TestParseAliasesFromFM(unittest.TestCase):
    def test_inline_json_array(self):
        fm = 'name: Foo\naliases: ["Bar", "Baz"]\ntype: x'
        result = _parse_aliases_from_fm(fm)
        self.assertEqual(result, ["Bar", "Baz"])

    def test_block_sequence(self):
        fm = 'name: Foo\naliases:\n  - Bar\n  - Baz\ntype: x'
        result = _parse_aliases_from_fm(fm)
        self.assertEqual(result, ["Bar", "Baz"])

    def test_block_sequence_with_quotes(self):
        fm = 'name: Foo\naliases:\n  - "Ned Stark"\n  - Ned\ntype: x'
        result = _parse_aliases_from_fm(fm)
        self.assertEqual(result, ["Ned Stark", "Ned"])

    def test_empty_inline(self):
        fm = 'name: Foo\naliases: []\ntype: x'
        result = _parse_aliases_from_fm(fm)
        self.assertEqual(result, [])

    def test_no_aliases_field(self):
        fm = 'name: Foo\ntype: x'
        result = _parse_aliases_from_fm(fm)
        self.assertEqual(result, [])


class TestParseFrontmatterAliases(unittest.TestCase):
    def test_parses_eddard_stark_block_aliases(self):
        """Eddard Stark uses YAML block sequence — must parse 'Ned Stark' etc."""
        node_file = REPO_ROOT / "graph/nodes/characters/eddard-stark.node.md"
        if not node_file.exists():
            self.skipTest("eddard-stark node not found")
        content = node_file.read_text()
        slug, name, aliases, node_type = _parse_frontmatter_aliases(content)
        self.assertEqual(slug, "eddard-stark")
        self.assertEqual(name, "Eddard Stark")
        self.assertIn("Ned Stark", aliases)
        self.assertIn("Ned", aliases)

    def test_parses_execution_node_inline_aliases(self):
        """execution-of-eddard-stark uses inline JSON array for aliases."""
        node_file = REPO_ROOT / "graph/nodes/events/execution-of-eddard-stark.node.md"
        if not node_file.exists():
            self.skipTest("execution-of-eddard-stark node not found")
        content = node_file.read_text()
        slug, name, aliases, node_type = _parse_frontmatter_aliases(content)
        self.assertEqual(slug, "execution-of-eddard-stark")
        self.assertIn("Ned's execution", aliases)


# ---------------------------------------------------------------------------
# Integration tests — resolve() against real graph data
# ---------------------------------------------------------------------------

class TestResolveIntegration(unittest.TestCase):
    """
    Integration tests using the real on-disk lookup table.
    Requires: the alias table has been built (graph/query/build/build_alias_table.py --build).
    """

    @classmethod
    def setUpClass(cls):
        if not ear.OUTPUT_FILE.exists() or not ear.ALL_NODES_OUTPUT_FILE.exists():
            ear.build_and_save(verbose=False)
        cls.lookup = ear.load_lookup()
        cls.all_node_index = ear.load_all_node_index()

    def _resolve(self, phrase):
        return ear.resolve(phrase, self.lookup, self.all_node_index)

    # --- Pre-existing exact resolutions must still work ---

    def test_red_wedding_still_hits(self):
        slug, status, _ = self._resolve("the Red Wedding")
        self.assertEqual(status, "hit")
        self.assertEqual(slug, "red-wedding")

    def test_tourney_at_harrenhal_still_hits(self):
        slug, status, _ = self._resolve("Tourney at Harrenhal")
        self.assertEqual(status, "hit")
        self.assertEqual(slug, "tourney-at-harrenhal")

    def test_battle_of_the_trident_still_hits(self):
        slug, status, _ = self._resolve("Battle of the Trident")
        self.assertEqual(status, "hit")
        self.assertEqual(slug, "battle-of-the-trident")

    # --- (b) Victim-index: death/execution hub lookup ---

    def test_robb_starks_death_resolves(self):
        """Robb Stark's death → robb-is-killed (S96 victim-index)"""
        slug, status, _ = self._resolve("Robb Stark's death")
        self.assertIn(status, ("hit", "candidates"))
        self.assertEqual(slug, "robb-is-killed",
                         msg=f"Expected robb-is-killed, got {slug!r} (status={status})")

    def test_ned_starks_execution_resolves(self):
        """Ned Stark's execution → execution-of-eddard-stark (S96 victim-index + char alias)"""
        slug, status, _ = self._resolve("Ned Stark's execution")
        self.assertIn(status, ("hit", "candidates"))
        self.assertEqual(slug, "execution-of-eddard-stark",
                         msg=f"Expected execution-of-eddard-stark, got {slug!r} (status={status})")

    def test_eddard_starks_execution_resolves(self):
        """Eddard Stark's execution → execution-of-eddard-stark"""
        slug, status, _ = self._resolve("Eddard Stark's execution")
        self.assertIn(status, ("hit", "candidates"))
        self.assertEqual(slug, "execution-of-eddard-stark")

    def test_who_killed_robb_stark_resolves(self):
        """who killed Robb Stark → robb-is-killed"""
        slug, status, _ = self._resolve("who killed Robb Stark")
        self.assertIn(status, ("hit", "candidates"))
        self.assertEqual(slug, "robb-is-killed")

    # --- (a) Fuzzy fallback: plausible phrasings hit via token overlap ---

    def test_trident_incident_hits(self):
        """'the Trident incident' → incident-at-the-trident (exact hit via node slug)"""
        slug, status, _ = self._resolve("the Trident incident")
        self.assertEqual(status, "hit")
        self.assertEqual(slug, "incident-at-the-trident")

    def test_the_trident_returns_candidates(self):
        """'the Trident' alone is ambiguous — must return CANDIDATES, not MISS"""
        slug, status, candidates = self._resolve("the Trident")
        self.assertEqual(status, "candidates",
                         msg="Bare 'the Trident' should return CANDIDATES (ambiguous)")
        candidate_slugs = [c["slug"] for c in candidates]
        # Both key Trident nodes should appear
        self.assertIn("battle-of-the-trident", candidate_slugs)
        self.assertIn("incident-at-the-trident", candidate_slugs)

    # --- (c) Character-name fallback ---

    def test_lyanna_returns_lyanna_stark_as_candidate(self):
        """'Lyanna' is ambiguous but lyanna-stark must appear in CANDIDATES"""
        slug, status, candidates = self._resolve("Lyanna")
        self.assertIn(status, ("hit", "hit-character", "candidates"),
                      msg="'Lyanna' should not MISS")
        candidate_slugs = [c["slug"] for c in candidates] + ([slug] if slug else [])
        self.assertIn("lyanna-stark", candidate_slugs,
                      msg="lyanna-stark must be in candidates for 'Lyanna'")

    def test_who_crowned_lyanna_returns_lyanna_stark(self):
        """'who crowned Lyanna' → lyanna-stark should appear in candidates"""
        slug, status, candidates = self._resolve("who crowned Lyanna")
        self.assertNotEqual(status, "miss",
                            msg="'who crowned Lyanna' should not MISS")
        candidate_slugs = [c["slug"] for c in candidates] + ([slug] if slug else [])
        self.assertIn("lyanna-stark", candidate_slugs,
                      msg="lyanna-stark must be in candidates for 'who crowned Lyanna'")

    # --- Negative cases: true garbage → MISS ---

    def test_garbage_phrase_is_miss(self):
        slug, status, candidates = self._resolve("asdfqwer nonsense")
        self.assertEqual(status, "miss")
        self.assertIsNone(slug)
        self.assertEqual(candidates, [])

    def test_very_short_garbage_is_miss(self):
        slug, status, candidates = self._resolve("xyzzy")
        self.assertEqual(status, "miss")
        self.assertIsNone(slug)

    def test_empty_common_words_only_is_miss(self):
        """Phrase that reduces to no meaningful tokens → MISS"""
        slug, status, candidates = self._resolve("the a an of")
        self.assertEqual(status, "miss")
        self.assertIsNone(slug)

    # --- Backward compatibility: resolve() still unpacks cleanly ---

    def test_resolve_returns_three_element_tuple(self):
        result = self._resolve("the Red Wedding")
        self.assertEqual(len(result), 3)

    def test_hit_has_empty_candidates(self):
        """For exact HITs, candidates list should be empty."""
        slug, status, candidates = self._resolve("the Red Wedding")
        self.assertEqual(status, "hit")
        self.assertEqual(candidates, [])


if __name__ == "__main__":
    unittest.main()
