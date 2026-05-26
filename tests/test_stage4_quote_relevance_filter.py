"""Tests for scripts/stage4-quote-relevance-filter.py — stdlib unittest, no I/O.

Run: python3 -m unittest tests.test_stage4_quote_relevance_filter -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

from tests._helpers import load_script

qrf = load_script("stage4-quote-relevance-filter.py")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_row(src: str, tgt: str, et: str = "LOVES", quote: str = "") -> dict:
    return {
        "source_slug":   src,
        "target_slug":   tgt,
        "edge_type":     et,
        "evidence_quote": quote,
    }


def _make_index(mapping: dict[str, list[str]], stoplist: frozenset[str]) -> dict[str, frozenset[str]]:
    """Build a minimal index from {slug: [token, ...]} for test isolation.

    Only includes tokens that pass _is_useful_token.
    """
    return {
        slug: frozenset(t.lower() for t in tokens
                        if qrf._is_useful_token(t, stoplist))
        for slug, tokens in mapping.items()
    }


# Build a minimal stoplist for testing (does not hit the filesystem)
_STOPLIST: frozenset[str] = frozenset({
    "the", "a", "an", "of", "and", "or", "in", "at", "to", "for",
    "his", "her", "him", "she", "he", "they", "them",
    "king", "queen", "lord", "lady", "ser",
    "man", "woman", "son", "daughter", "brother", "sister",
    "dragon", "wolf", "guard",
})


class TestQuoteRelevancePassFirstName(unittest.TestCase):
    """First-name-only match (the Arya/Jon sanity case)."""

    def _index(self) -> dict[str, frozenset[str]]:
        return _make_index({
            "arya-stark": ["arya", "stark"],
            "jon-snow":   ["jon", "snow"],
        }, _STOPLIST)

    def test_first_name_only_both_pass(self):
        """Quote names only first names -> PASS."""
        idx = self._index()
        row = _make_row("arya-stark", "jon-snow", quote="Jon told Arya to be careful.")
        passed, reason = qrf.quote_relevance_pass(row, idx, _STOPLIST)
        self.assertTrue(passed, f"Expected PASS, got DROP: {reason}")

    def test_full_name_both_pass(self):
        """Quote names full names -> PASS."""
        idx = self._index()
        row = _make_row("arya-stark", "jon-snow", quote="Arya Stark watched Jon Snow approach.")
        passed, reason = qrf.quote_relevance_pass(row, idx, _STOPLIST)
        self.assertTrue(passed, f"Expected PASS, got DROP: {reason}")

    def test_slug_token_match(self):
        """Slug token 'stark' found in quote -> PASS for source."""
        idx = self._index()
        row = _make_row("arya-stark", "jon-snow", quote="A Stark girl watched Jon ride past.")
        passed, reason = qrf.quote_relevance_pass(row, idx, _STOPLIST)
        self.assertTrue(passed, f"Expected PASS: {reason}")


class TestQuoteRelevancePassDropCases(unittest.TestCase):
    """Cases that must DROP."""

    def _index(self) -> dict[str, frozenset[str]]:
        return _make_index({
            "arya-stark": ["arya", "stark"],
            "jon-snow":   ["jon", "snow"],
            "tyrion-lannister": ["tyrion", "lannister"],
            "bronn":            ["bronn"],
        }, _STOPLIST)

    def test_only_source_named_drop(self):
        """Source named but target missing -> DROP."""
        idx = self._index()
        row = _make_row("arya-stark", "jon-snow",
                        quote="Arya walked through the dark forest alone.")
        passed, reason = qrf.quote_relevance_pass(row, idx, _STOPLIST)
        self.assertFalse(passed)
        self.assertIn("UNMATCHED_TARGET", reason)

    def test_only_target_named_drop(self):
        """Target named but source missing -> DROP."""
        idx = self._index()
        row = _make_row("arya-stark", "jon-snow",
                        quote="Jon Snow stood watch at Castle Black.")
        passed, reason = qrf.quote_relevance_pass(row, idx, _STOPLIST)
        self.assertFalse(passed)
        self.assertIn("UNMATCHED_SOURCE", reason)

    def test_neither_named_drop(self):
        """Neither endpoint named -> DROP."""
        idx = self._index()
        row = _make_row("arya-stark", "jon-snow",
                        quote="The crow flew over the wall and disappeared.")
        passed, reason = qrf.quote_relevance_pass(row, idx, _STOPLIST)
        self.assertFalse(passed)
        self.assertIn("UNMATCHED_BOTH", reason)

    def test_empty_quote_drop(self):
        """Empty quote -> DROP."""
        idx = self._index()
        row = _make_row("arya-stark", "jon-snow", quote="")
        passed, reason = qrf.quote_relevance_pass(row, idx, _STOPLIST)
        self.assertFalse(passed)
        self.assertIn("NO_QUOTE", reason)

    def test_generic_word_only_match_drop(self):
        """Quote containing only stoplist words (lord, king) -> DROP."""
        idx = self._index()
        row = _make_row("arya-stark", "jon-snow",
                        quote="The lord king said to the lady of the castle.")
        passed, reason = qrf.quote_relevance_pass(row, idx, _STOPLIST)
        self.assertFalse(passed)

    def test_missing_endpoint_drop(self):
        """Row with empty source slug -> DROP."""
        idx = self._index()
        row = _make_row("", "jon-snow", quote="Jon Snow was there.")
        passed, reason = qrf.quote_relevance_pass(row, idx, _STOPLIST)
        self.assertFalse(passed)
        self.assertIn("MISSING_ENDPOINT", reason)


class TestTokenLength(unittest.TestCase):
    """Tokens of length <= 2 must be silently ignored."""

    def test_two_char_token_ignored(self):
        """Tokens of length <=2 are filtered out; a slug with ONLY such tokens is UNMATCHABLE.

        We use a slug whose ONLY components are <=2-char tokens (no fallback possible),
        and verify the result is UNMATCHABLE_SOURCE rather than a spurious match.
        """
        stoplist = _STOPLIST
        # "jo-ed" -> tokens ["jo" (2), "ed" (2)] — both <=2 chars, both filtered out
        # The index entry will have an empty token set.
        # The fallback also uses _slug_tokens("jo-ed") = ["jo","ed"] -> also both filtered.
        idx = _make_index({
            "jo-ed": ["jo", "ed"],    # both 2-char tokens — not useful
            "arya-stark": ["arya"],
        }, stoplist)
        row = _make_row("jo-ed", "arya-stark", quote="Jo Ed and Arya talked.")
        passed, reason = qrf.quote_relevance_pass(row, idx, stoplist)
        # jo-ed token set after filtering should be empty -> UNMATCHABLE
        self.assertFalse(passed)
        self.assertIn("UNMATCHABLE_SOURCE", reason)

    def test_three_char_token_accepted(self):
        """'Jon' (3 chars) should be accepted."""
        stoplist = _STOPLIST
        idx = _make_index({
            "jon-snow":  ["jon", "snow"],
            "arya-stark": ["arya"],
        }, stoplist)
        row = _make_row("jon-snow", "arya-stark", quote="Jon met Arya.")
        passed, reason = qrf.quote_relevance_pass(row, idx, stoplist)
        self.assertTrue(passed, f"Expected PASS: {reason}")


class TestMissingAliasFallback(unittest.TestCase):
    """Slug not in index falls back to its own tokens."""

    def test_unknown_slug_fallback_pass(self):
        """A slug not in the index uses its own tokens as fallback."""
        idx: dict = {}  # empty — no index data
        stoplist = _STOPLIST
        # "sandor-clegane" not in index; fallback tokens = ["sandor", "clegane"]
        row = _make_row("sandor-clegane", "arya-stark",
                        quote="Sandor dragged Arya away from the riot.")
        passed, reason = qrf.quote_relevance_pass(row, idx, stoplist)
        self.assertTrue(passed, f"Expected PASS via fallback: {reason}")

    def test_unknown_slug_fallback_drop(self):
        """Fallback tokens present but not in quote -> DROP."""
        idx: dict = {}
        stoplist = _STOPLIST
        row = _make_row("sandor-clegane", "arya-stark",
                        quote="The hound carried the girl across the river.")
        passed, reason = qrf.quote_relevance_pass(row, idx, stoplist)
        self.assertFalse(passed)


class TestCaseInsensitive(unittest.TestCase):
    """Match must be case-insensitive."""

    def test_upper_in_quote(self):
        """ARYA in all caps should match arya token."""
        stoplist = _STOPLIST
        idx = _make_index({"arya-stark": ["arya"], "jon-snow": ["jon"]}, stoplist)
        row = _make_row("arya-stark", "jon-snow", quote="ARYA and JON ran together.")
        passed, reason = qrf.quote_relevance_pass(row, idx, stoplist)
        self.assertTrue(passed, f"Case-insensitive match failed: {reason}")


class TestWordBoundary(unittest.TestCase):
    """Substring of another word must NOT match."""

    def test_no_partial_match(self):
        """'stark' inside 'starkness' must not match token 'stark'."""
        stoplist = _STOPLIST
        idx = _make_index({"arya-stark": ["arya", "stark"], "jon-snow": ["jon"]}, stoplist)
        # 'starkness' contains 'stark' but not as a whole word
        row = _make_row("arya-stark", "jon-snow",
                        quote="Jon witnessed the starkness of winter.")
        # jon matches jon-snow; 'starkness' should NOT match 'stark' (word boundary)
        passed, reason = qrf.quote_relevance_pass(row, idx, stoplist)
        self.assertFalse(passed)
        self.assertIn("UNMATCHED_SOURCE", reason)


class TestBuildStoplist(unittest.TestCase):
    """build_stoplist() is importable and returns a frozenset with key words."""

    def test_returns_frozenset(self):
        sl = qrf.build_stoplist()
        self.assertIsInstance(sl, frozenset)

    def test_contains_generic_terms(self):
        sl = qrf.build_stoplist()
        for word in ("lord", "lady", "king", "queen", "ser", "maester"):
            self.assertIn(word, sl, f"Expected {word!r} in stoplist")

    def test_contains_function_words(self):
        sl = qrf.build_stoplist()
        for word in ("the", "and", "of", "his", "her"):
            self.assertIn(word, sl, f"Expected {word!r} in stoplist")


class TestBuildSlugTokenIndex(unittest.TestCase):
    """build_slug_token_index: slugs with no alias data fall back to slug tokens."""

    def test_slug_tokens_present_for_known_slug(self):
        """A slug that appears in any alias file should have usable tokens."""
        # We use real alias files — check that tyrion-lannister gets 'tyrion'
        try:
            stoplist = qrf.build_stoplist()
            idx = qrf.build_slug_token_index(
                slugs=["tyrion-lannister", "arya-stark"],
                stoplist=stoplist,
            )
            # tyrion-lannister: should have 'tyrion' from slug itself or alias
            self.assertIn("tyrion-lannister", idx)
            toks = idx["tyrion-lannister"]
            self.assertIn("tyrion", toks, f"Expected 'tyrion' in tokens, got: {toks}")
        except FileNotFoundError:
            self.skipTest("Alias files not available in this environment")

    def test_standalone_slug_uses_own_tokens(self):
        """A novel slug with no alias data still gets tokens from its own name."""
        stoplist = _STOPLIST
        idx = qrf.build_slug_token_index(
            slugs=["quellon-greyjoy"],
            alias_resolver_path=Path("/nonexistent/alias-resolver.json"),
            firstname_aliases_path=Path("/nonexistent/firstname.json"),
            supp_aliases_path=Path("/nonexistent/supp.json"),
            stoplist=stoplist,
        )
        self.assertIn("quellon-greyjoy", idx)
        toks = idx["quellon-greyjoy"]
        self.assertIn("quellon", toks)
        self.assertIn("greyjoy", toks)


if __name__ == "__main__":
    unittest.main()
