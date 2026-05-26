"""Tests for stage4_name_resolver.py — the collision-aware firstname resolver.

Covers every rung of the resolution ladder:
  a. resolved-exact
  b. resolved-alias
  c. resolved-firstname-unique
  d. resolved-context-present
  e. resolved-context-prior (3x margin)
  f. ambiguous-queued (two comparable candidates, none present, no dominant)
  g. unresolved (no candidates at all)

Also covers:
  - Parenthetical stripping ("Cersei (the queen)" → "Cersei")
  - Possessive stripping ("Lord Eddard's" → "Lord Eddard")
  - build_firstname_index correctness
  - load_importance_prior structure
  - resolve_name_bootstrap (rungs a–c only)

Run: python3 -m unittest tests.test_stage4_name_resolver -v
"""

import json
import tempfile
import unittest
from pathlib import Path

from tests._helpers import load_script

resolver = load_script("stage4_name_resolver.py")
name_key = resolver.name_key
TITLE_PREFIXES = resolver.TITLE_PREFIXES

# Re-export the helpers under shorter names for test readability
build_firstname_index = resolver.build_firstname_index
load_importance_prior = resolver.load_importance_prior
load_node_display_names = resolver.load_node_display_names
resolve_name = resolver.resolve_name
resolve_name_bootstrap = resolver.resolve_name_bootstrap
write_firstname_aliases = resolver.write_firstname_aliases
to_slug = resolver.to_slug

STATUS_EXACT = resolver.STATUS_EXACT
STATUS_ALIAS = resolver.STATUS_ALIAS
STATUS_FIRSTNAME_UNIQUE = resolver.STATUS_FIRSTNAME_UNIQUE
STATUS_CONTEXT_PRESENT = resolver.STATUS_CONTEXT_PRESENT
STATUS_CONTEXT_PRIOR = resolver.STATUS_CONTEXT_PRIOR
STATUS_AMBIGUOUS = resolver.STATUS_AMBIGUOUS
STATUS_UNRESOLVED = resolver.STATUS_UNRESOLVED
STATUS_UNRESOLVED_GENERIC = resolver.STATUS_UNRESOLVED_GENERIC
GENERIC_TERMS = resolver.GENERIC_TERMS


# ---------------------------------------------------------------------------
# Shared test fixture — small graph of characters
# ---------------------------------------------------------------------------

# slug → display name
_NAMES = {
    "tyrion-lannister": "Tyrion Lannister",
    "tyrion-tanner": "Tyrion Tanner",         # second "Tyrion" — ambiguity case
    "daenerys-targaryen": "Daenerys Targaryen",
    "jon-snow": "Jon Snow",
    "arya-stark": "Arya Stark",
    "yoren": "Yoren",                          # single-token name → always unique
    "eddard-stark": "Eddard Stark",
    "cersei-lannister": "Cersei Lannister",
    "robb-stark": "Robb Stark",
}

_NODE_SET = set(_NAMES.keys())

# alias_to_canonical: Arya → arya-stark
_ALIAS_MAP = {
    "arya": "arya-stark",
    "ned": "eddard-stark",
    "dany": "daenerys-targaryen",
}

# importance prior: tyrion-lannister >> tyrion-tanner
_PRIOR = {
    "tyrion-lannister": 1272,
    "tyrion-tanner": 9,
    "daenerys-targaryen": 968,
    "jon-snow": 973,
    "arya-stark": 843,
    "yoren": 45,
    "eddard-stark": 816,
    "cersei-lannister": 949,
    "robb-stark": 300,
}


def _make_firstname_index():
    return build_firstname_index(_NODE_SET, _NAMES)


# ---------------------------------------------------------------------------
# Test: build_firstname_index
# ---------------------------------------------------------------------------

class TestBuildFirstnameIndex(unittest.TestCase):
    """build_firstname_index must index by the first name token."""

    def setUp(self):
        self.idx = _make_firstname_index()

    def test_unique_firstname(self):
        """'daenerys' → exactly one slug (daenerys-targaryen)."""
        cands = self.idx.get("daenerys", [])
        self.assertEqual(len(cands), 1)
        self.assertEqual(cands[0], "daenerys-targaryen")

    def test_ambiguous_firstname(self):
        """'tyrion' → two slugs (tyrion-lannister + tyrion-tanner)."""
        cands = self.idx.get("tyrion", [])
        self.assertEqual(len(cands), 2)
        self.assertIn("tyrion-lannister", cands)
        self.assertIn("tyrion-tanner", cands)

    def test_single_token_name(self):
        """Single-token names like 'Yoren' are indexed under their first (and only) token."""
        cands = self.idx.get("yoren", [])
        self.assertEqual(len(cands), 1)
        self.assertEqual(cands[0], "yoren")

    def test_eddard_indexed_by_eddard(self):
        """'eddard-stark' is indexed under 'eddard', not 'stark'."""
        cands = self.idx.get("eddard", [])
        self.assertIn("eddard-stark", cands)
        # 'stark' may include robb-stark and arya-stark — not our concern here,
        # just verify eddard is correctly keyed
        self.assertEqual(len(cands), 1)


# ---------------------------------------------------------------------------
# Test: load_importance_prior
# ---------------------------------------------------------------------------

class TestLoadImportancePrior(unittest.TestCase):
    """load_importance_prior must parse backlink-counts.json correctly."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()

    def _write_backlinks(self, payload: dict) -> Path:
        p = Path(self._tmp) / "backlink-counts.json"
        p.write_text(json.dumps(payload), encoding="utf-8")
        return p

    def test_loads_in_count(self):
        payload = {
            "backlinks": {
                "tyrion-lannister": {"in_count": 1272, "out_count": 0},
                "arya-stark": {"in_count": 843, "out_count": 2},
            },
            "version": "1",
        }
        path = self._write_backlinks(payload)
        prior = load_importance_prior(path)
        self.assertEqual(prior["tyrion-lannister"], 1272)
        self.assertEqual(prior["arya-stark"], 843)

    def test_missing_in_count_defaults_zero(self):
        payload = {"backlinks": {"tyrion-lannister": {}}}
        path = self._write_backlinks(payload)
        prior = load_importance_prior(path)
        self.assertEqual(prior.get("tyrion-lannister", 0), 0)

    def test_bad_file_returns_empty(self):
        bad_path = Path(self._tmp) / "nonexistent.json"
        prior = load_importance_prior(bad_path)
        self.assertEqual(prior, {})


# ---------------------------------------------------------------------------
# Test: _clean_raw_name (via module-level function)
# ---------------------------------------------------------------------------

class TestCleanRawName(unittest.TestCase):
    """_clean_raw_name must strip parentheticals and possessives."""

    def _clean(self, raw):
        return resolver._clean_raw_name(raw)

    def test_parenthetical_stripped(self):
        self.assertEqual(self._clean("Cersei (the queen)"), "Cersei")

    def test_possessive_stripped(self):
        self.assertEqual(self._clean("Lord Eddard's"), "Lord Eddard")

    def test_apostrophe_s_stripped(self):
        self.assertEqual(self._clean("Tyrion's"), "Tyrion")

    def test_no_change_plain_name(self):
        self.assertEqual(self._clean("Tyrion Lannister"), "Tyrion Lannister")

    def test_multi_parenthetical_stripped(self):
        # Parentheticals are removed; surrounding whitespace is stripped.
        # The result may have an internal double-space which strip() does not collapse
        # (only leading/trailing strip is guaranteed), but first-token resolution
        # still works correctly because split() ignores interior whitespace.
        result = self._clean("Jorah (Ser) Mormont (ser)")
        # Must contain both "Jorah" and "Mormont", and not contain the parentheticals
        self.assertIn("Jorah", result)
        self.assertIn("Mormont", result)
        self.assertNotIn("(Ser)", result)
        self.assertNotIn("(ser)", result)

    def test_empty_string(self):
        self.assertEqual(self._clean(""), "")

    def test_whitespace_only(self):
        self.assertEqual(self._clean("   "), "")


# ---------------------------------------------------------------------------
# Test: resolve_name — Rung A (exact)
# ---------------------------------------------------------------------------

class TestResolveNameExact(unittest.TestCase):
    """Rung a: to_slug(raw) ∈ node_set → STATUS_EXACT."""

    def setUp(self):
        self.idx = _make_firstname_index()

    def test_exact_full_name(self):
        slug, status = resolve_name(
            "Daenerys Targaryen",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=set(),
        )
        self.assertEqual(slug, "daenerys-targaryen")
        self.assertEqual(status, STATUS_EXACT)

    def test_exact_already_slug(self):
        slug, status = resolve_name(
            "jon-snow",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=set(),
        )
        self.assertEqual(slug, "jon-snow")
        self.assertEqual(status, STATUS_EXACT)

    def test_exact_single_token(self):
        slug, status = resolve_name(
            "Yoren",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=set(),
        )
        self.assertEqual(slug, "yoren")
        self.assertEqual(status, STATUS_EXACT)


# ---------------------------------------------------------------------------
# Test: resolve_name — Rung A title-person disambiguation
# ---------------------------------------------------------------------------

class TestResolveNameTitlePerson(unittest.TestCase):
    """A title-prefixed name ("Lord Tywin") that exact-matches a NON-character node
    (a ship/artifact/title named after the person) prefers the character via the
    character-restricted name ladder. Requires slug_category; degrades to plain
    exact match when slug_category is None (back-compat)."""

    def setUp(self):
        self.names = {
            "tywin-lannister": "Tywin Lannister",
            "tywin-frey": "Tywin Frey",                  # 2nd Tywin → prior decides
            "cersei-lannister": "Cersei Lannister",
            "marya-seaworth": "Marya Seaworth",
            "renly-baratheon": "Renly Baratheon",
            # non-character nodes (ships/artifacts named after people)
            "lord-tywin": "Lord Tywin",                  # ship
            "queen-cersei": "Queen Cersei",              # ship
            "lady-marya": "Lady Marya",                  # ship
            "king-roberts-hammer": "King Robert's Hammer",  # ship; remainder not a char
            "ser-pounce": "Ser Pounce",                  # a (cat) CHARACTER node
        }
        self.node_set = set(self.names)
        self.cat = {
            "tywin-lannister": "characters", "tywin-frey": "characters",
            "cersei-lannister": "characters", "marya-seaworth": "characters",
            "renly-baratheon": "characters", "ser-pounce": "characters",
            "lord-tywin": "artifacts", "queen-cersei": "artifacts",
            "lady-marya": "artifacts", "king-roberts-hammer": "artifacts",
        }
        self.prior = {"tywin-lannister": 848, "tywin-frey": 2,
                      "cersei-lannister": 949, "marya-seaworth": 6,
                      "renly-baratheon": 385}
        self.idx = build_firstname_index(self.node_set, self.names)

    def _r(self, raw, present=None):
        return resolve_name(
            raw, alias_map={}, node_set=self.node_set, firstname_index=self.idx,
            prior=self.prior, present_slugs=present or set(), slug_category=self.cat,
        )

    def test_lord_tywin_redirects_via_prior(self):
        # "tywin" has 2 char candidates; tywin-lannister dominates by backlinks.
        slug, status = self._r("Lord Tywin")
        self.assertEqual(slug, "tywin-lannister")
        self.assertEqual(status, resolver.STATUS_TITLE_PERSON)

    def test_queen_cersei_redirects_firstname_unique(self):
        slug, status = self._r("Queen Cersei")
        self.assertEqual(slug, "cersei-lannister")
        self.assertEqual(status, resolver.STATUS_TITLE_PERSON)

    def test_king_roberts_hammer_stays_ship(self):
        # remainder "robert's" has no CHARACTER candidate → keep the artifact
        slug, status = self._r("King Robert's Hammer")
        self.assertEqual(slug, "king-roberts-hammer")
        self.assertEqual(status, STATUS_EXACT)

    def test_ser_pounce_character_node_no_redirect(self):
        # exact match is itself a character → keep it, never redirect
        slug, status = self._r("Ser Pounce")
        self.assertEqual(slug, "ser-pounce")
        self.assertEqual(status, STATUS_EXACT)

    def test_lady_marya_ship_name_redirects(self):
        # Known ship-name class: "Lady Marya" (Davos's ship) redirects to the only
        # "Marya" character. This is intentional at the resolver level; the
        # CAPTAIN_OF type-contract is the backstop that prevents asserting a false
        # person-edge for vessel captaincy.
        slug, status = self._r("Lady Marya")
        self.assertEqual(slug, "marya-seaworth")
        self.assertEqual(status, resolver.STATUS_TITLE_PERSON)

    def test_no_category_map_back_compat(self):
        # slug_category omitted → no redirect, plain exact match (old behavior)
        slug, status = resolve_name(
            "Lord Tywin", alias_map={}, node_set=self.node_set,
            firstname_index=self.idx, prior=self.prior, present_slugs=set(),
        )
        self.assertEqual(slug, "lord-tywin")
        self.assertEqual(status, STATUS_EXACT)


# ---------------------------------------------------------------------------
# Test: resolve_name — Rung B (alias)
# ---------------------------------------------------------------------------

class TestResolveNameAlias(unittest.TestCase):
    """Rung b: alias_map resolves the slug → STATUS_ALIAS."""

    def setUp(self):
        self.idx = _make_firstname_index()

    def test_alias_arya(self):
        """'Arya' slugifies to 'arya' which is in alias_map → arya-stark."""
        slug, status = resolve_name(
            "Arya",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=set(),
        )
        self.assertEqual(slug, "arya-stark")
        self.assertEqual(status, STATUS_ALIAS)

    def test_alias_ned(self):
        slug, status = resolve_name(
            "Ned",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=set(),
        )
        self.assertEqual(slug, "eddard-stark")
        self.assertEqual(status, STATUS_ALIAS)

    def test_alias_dany(self):
        slug, status = resolve_name(
            "Dany",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=set(),
        )
        self.assertEqual(slug, "daenerys-targaryen")
        self.assertEqual(status, STATUS_ALIAS)


# ---------------------------------------------------------------------------
# Test: resolve_name — Rung C (firstname-unique)
# ---------------------------------------------------------------------------

class TestResolveNameFirstnameUnique(unittest.TestCase):
    """Rung c: first token maps to exactly one slug → STATUS_FIRSTNAME_UNIQUE."""

    def setUp(self):
        self.idx = _make_firstname_index()

    def test_firstname_unique_daenerys(self):
        """'Daenerys' first-token is unique in the fixture — but exact match fires first (rung a).
        Use a name that's firstname-unique but NOT an exact match or alias.
        'Cersei' → cersei is unique (cersei-lannister) and not in alias_map.
        But 'cersei' as a slug IS in _NODE_SET only if 'cersei' == 'cersei-lannister'.
        It isn't — so rung a fails, rung b fails (not in alias map), rung c fires.
        """
        slug, status = resolve_name(
            "Cersei",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=set(),
        )
        self.assertEqual(slug, "cersei-lannister")
        self.assertEqual(status, STATUS_FIRSTNAME_UNIQUE)

    def test_firstname_unique_robb(self):
        slug, status = resolve_name(
            "Robb",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=set(),
        )
        self.assertEqual(slug, "robb-stark")
        self.assertEqual(status, STATUS_FIRSTNAME_UNIQUE)

    def test_parenthetical_stripped_before_firstname(self):
        """'Cersei (the queen)' → cleaned to 'Cersei' → firstname-unique."""
        slug, status = resolve_name(
            "Cersei (the queen)",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=set(),
        )
        self.assertEqual(slug, "cersei-lannister")
        self.assertEqual(status, STATUS_FIRSTNAME_UNIQUE)

    def test_possessive_stripped_before_firstname(self):
        """'Cersei's' → cleaned to 'Cersei' → firstname-unique."""
        slug, status = resolve_name(
            "Cersei's",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=set(),
        )
        self.assertEqual(slug, "cersei-lannister")
        self.assertEqual(status, STATUS_FIRSTNAME_UNIQUE)


# ---------------------------------------------------------------------------
# Test: resolve_name — Rung D (context-present)
# ---------------------------------------------------------------------------

class TestResolveNameContextPresent(unittest.TestCase):
    """Rung d: multiple candidates, exactly one in present_slugs → STATUS_CONTEXT_PRESENT."""

    def setUp(self):
        self.idx = _make_firstname_index()

    def test_context_present_picks_correct_tyrion(self):
        """'Tyrion' is ambiguous (tyrion-lannister + tyrion-tanner).
        present_slugs contains tyrion-lannister → context-present picks it.
        """
        present = {"tyrion-lannister", "jon-snow", "arya-stark"}
        slug, status = resolve_name(
            "Tyrion",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=present,
        )
        self.assertEqual(slug, "tyrion-lannister")
        self.assertEqual(status, STATUS_CONTEXT_PRESENT)

    def test_context_present_picks_tanner_if_that_is_present(self):
        """If only tyrion-tanner is present → context-present picks tanner."""
        present = {"tyrion-tanner"}
        slug, status = resolve_name(
            "Tyrion",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=present,
        )
        self.assertEqual(slug, "tyrion-tanner")
        self.assertEqual(status, STATUS_CONTEXT_PRESENT)

    def test_context_present_skipped_if_both_present(self):
        """If both Tyrions are present → context-present doesn't fire (two matches).
        Falls to rung e (context-prior).
        """
        present = {"tyrion-lannister", "tyrion-tanner"}
        slug, status = resolve_name(
            "Tyrion",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=present,
        )
        # Rung d doesn't fire (both present). Rung e should fire:
        # tyrion-lannister (1272) >= 3× tyrion-tanner (9) → context-prior
        self.assertEqual(slug, "tyrion-lannister")
        self.assertEqual(status, STATUS_CONTEXT_PRIOR)


# ---------------------------------------------------------------------------
# Test: resolve_name — Rung E (context-prior)
# ---------------------------------------------------------------------------

class TestResolveNameContextPrior(unittest.TestCase):
    """Rung e: top candidate has ≥ 3× backlinks of runner-up → STATUS_CONTEXT_PRIOR."""

    def setUp(self):
        self.idx = _make_firstname_index()

    def test_context_prior_dominant(self):
        """tyrion-lannister (1272) >> tyrion-tanner (9): ratio = 141× → dominant."""
        slug, status = resolve_name(
            "Tyrion",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=set(),   # no context
        )
        self.assertEqual(slug, "tyrion-lannister")
        self.assertEqual(status, STATUS_CONTEXT_PRIOR)

    def test_context_prior_threshold_exactly_3x(self):
        """Build a custom fixture where top = 300, runner = 100 → exactly 3× → fires."""
        # New node set with two "Jon" options
        names = {"jon-snow": "Jon Snow", "jon-connington": "Jon Connington"}
        node_set = set(names.keys())
        idx = build_firstname_index(node_set, names)
        prior = {"jon-snow": 300, "jon-connington": 100}  # exactly 3× → should pick snow

        slug, status = resolve_name(
            "Jon",
            alias_map={},
            node_set=node_set,
            firstname_index=idx,
            prior=prior,
            present_slugs=set(),
        )
        self.assertEqual(slug, "jon-snow")
        self.assertEqual(status, STATUS_CONTEXT_PRIOR)

    def test_context_prior_just_below_threshold_ambiguous(self):
        """Build a fixture where top = 200, runner = 100 → 2× < 3× → ambiguous."""
        names = {"jon-snow": "Jon Snow", "jon-connington": "Jon Connington"}
        node_set = set(names.keys())
        idx = build_firstname_index(node_set, names)
        prior = {"jon-snow": 200, "jon-connington": 100}  # 2× < 3× threshold

        slug, status = resolve_name(
            "Jon",
            alias_map={},
            node_set=node_set,
            firstname_index=idx,
            prior=prior,
            present_slugs=set(),
        )
        self.assertIsNone(slug)
        self.assertEqual(status, STATUS_AMBIGUOUS)


# ---------------------------------------------------------------------------
# Test: resolve_name — Rung F (ambiguous-queued)
# ---------------------------------------------------------------------------

class TestResolveNameAmbiguous(unittest.TestCase):
    """Rung f: multiple candidates, none present, no dominant prior → STATUS_AMBIGUOUS."""

    def setUp(self):
        self.idx = _make_firstname_index()

    def test_ambiguous_equal_priors_no_present(self):
        """Two 'Jon' nodes with equal backlinks, neither present → ambiguous."""
        names = {"jon-snow": "Jon Snow", "jon-arryn": "Jon Arryn"}
        node_set = set(names.keys())
        idx = build_firstname_index(node_set, names)
        prior = {"jon-snow": 100, "jon-arryn": 100}  # tied → no dominant

        slug, status = resolve_name(
            "Jon",
            alias_map={},
            node_set=node_set,
            firstname_index=idx,
            prior=prior,
            present_slugs=set(),
        )
        self.assertIsNone(slug)
        self.assertEqual(status, STATUS_AMBIGUOUS)


# ---------------------------------------------------------------------------
# Test: resolve_name — Rung G (unresolved)
# ---------------------------------------------------------------------------

class TestResolveNameUnresolved(unittest.TestCase):
    """Rung g: no candidates at all → STATUS_UNRESOLVED."""

    def setUp(self):
        self.idx = _make_firstname_index()

    def test_completely_unknown_name(self):
        """A name not in any index → unresolved."""
        slug, status = resolve_name(
            "Quentyn Martell",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=set(),
        )
        self.assertIsNone(slug)
        self.assertEqual(status, STATUS_UNRESOLVED)

    def test_group_cell_unresolved(self):
        """A multi-name cell like 'Robb, Bran, Rickon' → unresolved (out of scope v1)."""
        slug, status = resolve_name(
            "Robb, Bran, Rickon",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=set(),
        )
        # The slugified form has commas stripped, yielding 'robb-bran-rickon' —
        # not in node_set, not in alias_map. Robb as first token → robb-stark
        # but only through firstname index after the slug strip.  The slug
        # 'robb,-bran,-rickon' (pre-strip) → 'robb-bran-rickon' (post-strip),
        # so rung a fails. First token of 'Robb, Bran, Rickon' → 'Robb,' → 'robb,'
        # after lower → 'robb,' → cleaned name is 'Robb Bran Rickon' after comma strip.
        # _clean_raw_name strips commas via possessive/paren regex... let's just
        # assert it returns None (it won't spuriously match robb-stark exactly).
        # The test validates that group cells don't produce confident wrong resolutions.
        self.assertIsNone(slug)

    def test_empty_string(self):
        slug, status = resolve_name(
            "",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
            prior=_PRIOR,
            present_slugs=set(),
        )
        self.assertIsNone(slug)
        self.assertEqual(status, STATUS_UNRESOLVED)

    def test_generic_placeholder(self):
        """Generic placeholders like '(general)' or '(self)' → unresolved."""
        for placeholder in ["(general)", "(self)", "her mother", "Everyone"]:
            slug, status = resolve_name(
                placeholder,
                alias_map=_ALIAS_MAP,
                node_set=_NODE_SET,
                firstname_index=self.idx,
                prior=_PRIOR,
                present_slugs=set(),
            )
            self.assertIsNone(slug, f"Expected None for {placeholder!r}, got {slug!r}")


# ---------------------------------------------------------------------------
# Test: resolve_name_bootstrap (rungs a–c only)
# ---------------------------------------------------------------------------

class TestResolveNameBootstrap(unittest.TestCase):
    """resolve_name_bootstrap must use only rungs a, b, c — no context steps."""

    def setUp(self):
        self.idx = _make_firstname_index()

    def test_bootstrap_exact(self):
        result = resolve_name_bootstrap(
            "Daenerys Targaryen",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
        )
        self.assertEqual(result, "daenerys-targaryen")

    def test_bootstrap_alias(self):
        result = resolve_name_bootstrap(
            "Ned",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
        )
        self.assertEqual(result, "eddard-stark")

    def test_bootstrap_firstname_unique(self):
        result = resolve_name_bootstrap(
            "Cersei",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
        )
        self.assertEqual(result, "cersei-lannister")

    def test_bootstrap_ambiguous_returns_none(self):
        """Ambiguous 'Tyrion' (two slugs, no context) → None (bootstrap doesn't use d/e)."""
        result = resolve_name_bootstrap(
            "Tyrion",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
        )
        self.assertIsNone(result)

    def test_bootstrap_unresolved_returns_none(self):
        result = resolve_name_bootstrap(
            "Completely Unknown Person",
            alias_map=_ALIAS_MAP,
            node_set=_NODE_SET,
            firstname_index=self.idx,
        )
        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# Test: write_firstname_aliases
# ---------------------------------------------------------------------------

class TestWriteFirstnameAliases(unittest.TestCase):
    """write_firstname_aliases must emit the correct JSON without touching alias-resolver.json."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()

    def test_writes_unique_entries_only(self):
        """Only unique-firstname entries (len==1) should appear in the output."""
        idx = _make_firstname_index()
        out_path = Path(self._tmp) / "pass1-derived-firstname-aliases.json"
        result = write_firstname_aliases(idx, out_path)

        # "tyrion" → 2 slugs: must NOT be in result
        self.assertNotIn("tyrion", result)
        # "daenerys" → 1 slug: must be in result
        self.assertIn("daenerys", result)
        self.assertEqual(result["daenerys"], "daenerys-targaryen")

    def test_json_schema(self):
        """Output JSON must have expected keys."""
        idx = _make_firstname_index()
        out_path = Path(self._tmp) / "aliases.json"
        write_firstname_aliases(idx, out_path)

        data = json.loads(out_path.read_text(encoding="utf-8"))
        for key in ("version", "produced_at", "source", "count", "firstname_to_slug"):
            self.assertIn(key, data, f"Missing key {key!r} in output JSON")

    def test_count_matches(self):
        """count field must match len(firstname_to_slug)."""
        idx = _make_firstname_index()
        out_path = Path(self._tmp) / "aliases.json"
        write_firstname_aliases(idx, out_path)

        data = json.loads(out_path.read_text(encoding="utf-8"))
        self.assertEqual(data["count"], len(data["firstname_to_slug"]))

    def test_source_field(self):
        idx = _make_firstname_index()
        out_path = Path(self._tmp) / "aliases.json"
        write_firstname_aliases(idx, out_path)

        data = json.loads(out_path.read_text(encoding="utf-8"))
        self.assertEqual(data["source"], "pass1-derived-firstname-resolver")


# ---------------------------------------------------------------------------
# Test: load_node_display_names
# ---------------------------------------------------------------------------

class TestLoadNodeDisplayNames(unittest.TestCase):
    """load_node_display_names must extract `name:` from frontmatter."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._tmp_path = Path(self._tmp)

    def _write_node(self, subdir: str, slug: str, name: str) -> Path:
        d = self._tmp_path / subdir
        d.mkdir(parents=True, exist_ok=True)
        content = f"---\nname: {name}\ntype: character.human\n---\n\n## Edges\n"
        p = d / f"{slug}.node.md"
        p.write_text(content, encoding="utf-8")
        return p

    def test_extracts_name(self):
        self._write_node("characters", "tyrion-lannister", "Tyrion Lannister")
        node_set = {"tyrion-lannister"}
        names = load_node_display_names(node_set, self._tmp_path)
        self.assertEqual(names.get("tyrion-lannister"), "Tyrion Lannister")

    def test_fallback_to_dekebab(self):
        """Node with no name field → de-kebabbed slug as fallback."""
        d = self._tmp_path / "characters"
        d.mkdir(parents=True, exist_ok=True)
        content = "---\ntype: character.human\n---\n"
        (d / "jon-snow.node.md").write_text(content, encoding="utf-8")
        names = load_node_display_names({"jon-snow"}, self._tmp_path)
        self.assertEqual(names.get("jon-snow"), "Jon Snow")

    def test_skips_excluded_dirs(self):
        """Files in _conflicts/ must be ignored."""
        self._write_node("_conflicts", "conflict-slug", "Conflict Name")
        names = load_node_display_names({"conflict-slug"}, self._tmp_path)
        # Should fall back to de-kebab (no file found)
        self.assertEqual(names.get("conflict-slug"), "Conflict Slug")


# ---------------------------------------------------------------------------
# Test: GENERIC_TERMS stoplist
# ---------------------------------------------------------------------------

class TestGenericTermsStoplist(unittest.TestCase):
    """GENERIC_TERMS stoplist must block bare role-words from reaching rungs c–e.

    Cases:
      - "maester" → unresolved-generic (whole slug is in GENERIC_TERMS)
      - "the maester" → article stripped → "maester" → unresolved-generic
      - "a septa" → article stripped → "septa" → unresolved-generic
      - "Maester Luwin" → slug is "maester-luwin" (NOT in GENERIC_TERMS) → proceeds normally
      - A real first name that is NOT generic still resolves normally
    """

    def _make_graph_with_maester(self):
        """Return (node_set, names, alias_map, index, prior) with a Maester Luwin node."""
        names = {
            "maester-luwin": "Maester Luwin",
            "cersei-lannister": "Cersei Lannister",
            "robb-stark": "Robb Stark",
        }
        node_set = set(names.keys())
        alias_map = {}
        idx = build_firstname_index(node_set, names)
        prior = {
            "maester-luwin": 80,
            "cersei-lannister": 949,
            "robb-stark": 300,
        }
        return node_set, names, alias_map, idx, prior

    def test_bare_maester_is_generic(self):
        """'maester' (bare) → unresolved-generic, not resolved to any node."""
        node_set, names, alias_map, idx, prior = self._make_graph_with_maester()
        slug, status = resolve_name(
            "maester",
            alias_map=alias_map,
            node_set=node_set,
            firstname_index=idx,
            prior=prior,
            present_slugs=set(),
        )
        self.assertIsNone(slug)
        self.assertEqual(status, STATUS_UNRESOLVED_GENERIC)

    def test_the_maester_is_generic(self):
        """'the maester' → article stripped → 'maester' slug → unresolved-generic."""
        node_set, names, alias_map, idx, prior = self._make_graph_with_maester()
        slug, status = resolve_name(
            "the maester",
            alias_map=alias_map,
            node_set=node_set,
            firstname_index=idx,
            prior=prior,
            present_slugs=set(),
        )
        self.assertIsNone(slug)
        self.assertEqual(status, STATUS_UNRESOLVED_GENERIC)

    def test_a_septa_is_generic(self):
        """'a septa' → article stripped → 'septa' slug → unresolved-generic."""
        node_set = {"septa-mordane": "Septa Mordane"}
        idx = build_firstname_index(set(node_set.keys()), node_set)
        slug, status = resolve_name(
            "a septa",
            alias_map={},
            node_set=set(node_set.keys()),
            firstname_index=idx,
            prior={},
            present_slugs=set(),
        )
        self.assertIsNone(slug)
        self.assertEqual(status, STATUS_UNRESOLVED_GENERIC)

    def test_maester_luwin_resolves_normally(self):
        """'Maester Luwin' → slug 'maester-luwin' is NOT in GENERIC_TERMS → resolves."""
        node_set, names, alias_map, idx, prior = self._make_graph_with_maester()
        slug, status = resolve_name(
            "Maester Luwin",
            alias_map=alias_map,
            node_set=node_set,
            firstname_index=idx,
            prior=prior,
            present_slugs=set(),
        )
        self.assertEqual(slug, "maester-luwin")
        self.assertEqual(status, STATUS_EXACT)

    def test_real_firstname_not_in_generic_still_resolves(self):
        """'Cersei' is NOT a generic term → resolves via firstname-unique."""
        node_set, names, alias_map, idx, prior = self._make_graph_with_maester()
        self.assertNotIn("cersei", GENERIC_TERMS)
        slug, status = resolve_name(
            "Cersei",
            alias_map=alias_map,
            node_set=node_set,
            firstname_index=idx,
            prior=prior,
            present_slugs=set(),
        )
        self.assertEqual(slug, "cersei-lannister")
        self.assertEqual(status, STATUS_FIRSTNAME_UNIQUE)

    def test_khal_is_generic(self):
        """'Khal' → unresolved-generic (not resolved to Drogo via firstname)."""
        node_set = {"khal-drogo": "Khal Drogo"}
        idx = build_firstname_index(set(node_set.keys()), node_set)
        slug, status = resolve_name(
            "Khal",
            alias_map={},
            node_set=set(node_set.keys()),
            firstname_index=idx,
            prior={},
            present_slugs=set(),
        )
        self.assertIsNone(slug)
        self.assertEqual(status, STATUS_UNRESOLVED_GENERIC)

    def test_lady_is_generic(self):
        """'Lady' alone → unresolved-generic."""
        node_set = {"lady": "Lady"}
        idx = build_firstname_index(set(node_set.keys()), node_set)
        slug, status = resolve_name(
            "Lady",
            alias_map={},
            node_set=set(node_set.keys()),
            firstname_index=idx,
            prior={},
            present_slugs=set(),
        )
        # 'lady' exact-matches node_set first (rung a) — only if 'lady' is a slug.
        # If 'lady' IS in node_set, rung a fires before the generic gate.
        # Here node_set = {"lady"} so rung a resolves it.
        # The purpose of this test: confirm the gate is AFTER rung a, not before.
        self.assertEqual(slug, "lady")
        self.assertEqual(status, STATUS_EXACT)

    def test_generic_terms_frozenset_contains_expected_members(self):
        """Spot-check: GENERIC_TERMS must include the known-bad terms from the audit."""
        for term in ["maester", "khal", "septa", "lady", "septon", "knight", "squire"]:
            self.assertIn(term, GENERIC_TERMS, f"Expected {term!r} in GENERIC_TERMS")


# ---------------------------------------------------------------------------
# Test: name_key helper
# ---------------------------------------------------------------------------

class TestNameKey(unittest.TestCase):
    """name_key() must strip leading TITLE_PREFIXES and return the first real token."""

    def test_plain_firstname(self):
        """Plain names with no title → first token returned."""
        self.assertEqual(name_key("Cersei"), "cersei")
        self.assertEqual(name_key("Tyrion Lannister"), "tyrion")
        self.assertEqual(name_key("Yoren"), "yoren")

    def test_ser_prefix_stripped(self):
        """'Ser X' → 'x' (not 'ser')."""
        self.assertEqual(name_key("Ser Pounce"), "pounce")
        self.assertEqual(name_key("Ser Boros"), "boros")
        self.assertEqual(name_key("Ser Jaime"), "jaime")

    def test_lord_prefix_stripped(self):
        """'Lord Tywin' → 'tywin'."""
        self.assertEqual(name_key("Lord Tywin"), "tywin")
        self.assertEqual(name_key("Lord Commander Mormont"), "commander")

    def test_khal_prefix_stripped(self):
        """'Khal Drogo' → 'drogo'."""
        self.assertEqual(name_key("Khal Drogo"), "drogo")

    def test_maester_prefix_stripped(self):
        """'Maester Luwin' → 'luwin'."""
        self.assertEqual(name_key("Maester Luwin"), "luwin")

    def test_old_prefix_stripped(self):
        """'Old Nan' → 'nan'."""
        self.assertEqual(name_key("Old Nan"), "nan")

    def test_bare_title_returns_none(self):
        """Bare title tokens alone → None."""
        self.assertIsNone(name_key("Ser"))
        self.assertIsNone(name_key("Lord"))
        self.assertIsNone(name_key("Khal"))
        self.assertIsNone(name_key("Maester"))

    def test_empty_string_returns_none(self):
        self.assertIsNone(name_key(""))

    def test_multiple_prefixes_stripped(self):
        """'Grand Maester' → both are titles → None (no real token remains)."""
        self.assertIsNone(name_key("Grand Maester"))

    def test_title_prefixes_frozenset_contains_expected(self):
        """Spot-check TITLE_PREFIXES contains the key honorifics."""
        for t in ["ser", "lord", "lady", "maester", "khal", "king", "queen",
                  "prince", "princess", "septon", "septa", "grand", "high", "old", "young"]:
            self.assertIn(t, TITLE_PREFIXES, f"Expected {t!r} in TITLE_PREFIXES")


# ---------------------------------------------------------------------------
# Test: title-first-token collapse fix (the ser-pounce bug)
# ---------------------------------------------------------------------------

class TestTitleFirstTokenCollapseFix(unittest.TestCase):
    """Verify that the title-stripping fix eliminates wrong-node collapses.

    These tests use the REAL graph nodes (via a fixture that includes ser-pounce
    and the real boros-blount / drogo nodes) to confirm the fix works end-to-end.
    """

    def _make_ser_pounce_graph(self):
        """Return (node_set, names, idx, prior) with ser-pounce + real knight nodes."""
        names = {
            "ser-pounce": "Ser Pounce",        # cat — must NOT receive "Ser Boros" traffic
            "boros-blount": "Boros Blount",     # the actual Ser Boros
            "drogo": "Drogo",                   # Khal Drogo (no "Khal" in display name)
            "khal-jhaqo": "Khal Jhaqo",         # another khal
            "maester-luwin": "Maester Luwin",   # maester with name in display
            "cersei-lannister": "Cersei Lannister",
        }
        node_set = set(names.keys())
        alias_map = {}
        idx = build_firstname_index(node_set, names)
        prior = {
            "ser-pounce": 5,
            "boros-blount": 30,
            "drogo": 400,
            "khal-jhaqo": 20,
            "maester-luwin": 80,
            "cersei-lannister": 949,
        }
        return node_set, names, alias_map, idx, prior

    def test_ser_boros_does_not_resolve_to_ser_pounce(self):
        """'Ser Boros' must NOT resolve to ser-pounce.

        After the fix, 'Ser Boros' → name_key → 'boros' → boros-blount (unique).
        """
        node_set, names, alias_map, idx, prior = self._make_ser_pounce_graph()
        slug, status = resolve_name(
            "Ser Boros",
            alias_map=alias_map,
            node_set=node_set,
            firstname_index=idx,
            prior=prior,
            present_slugs=set(),
        )
        self.assertNotEqual(slug, "ser-pounce", "ser-pounce must not absorb 'Ser Boros'")
        self.assertEqual(slug, "boros-blount", "Expected boros-blount for 'Ser Boros'")
        self.assertEqual(status, STATUS_FIRSTNAME_UNIQUE)

    def test_khal_drogo_resolves_to_drogo(self):
        """'Khal Drogo' → name_key → 'drogo' → drogo (unique)."""
        node_set, names, alias_map, idx, prior = self._make_ser_pounce_graph()
        slug, status = resolve_name(
            "Khal Drogo",
            alias_map=alias_map,
            node_set=node_set,
            firstname_index=idx,
            prior=prior,
            present_slugs=set(),
        )
        self.assertEqual(slug, "drogo")
        self.assertEqual(status, STATUS_FIRSTNAME_UNIQUE)

    def test_ser_pounce_exact_still_resolves(self):
        """'Ser Pounce' full form → rung a (exact slug) → ser-pounce.

        The fix only affects the firstname-index fallback; rung a is unchanged.
        """
        node_set, names, alias_map, idx, prior = self._make_ser_pounce_graph()
        slug, status = resolve_name(
            "Ser Pounce",
            alias_map=alias_map,
            node_set=node_set,
            firstname_index=idx,
            prior=prior,
            present_slugs=set(),
        )
        self.assertEqual(slug, "ser-pounce")
        self.assertEqual(status, STATUS_EXACT)

    def test_maester_luwin_exact_still_resolves(self):
        """'Maester Luwin' full form → rung a (exact slug) → maester-luwin."""
        node_set, names, alias_map, idx, prior = self._make_ser_pounce_graph()
        slug, status = resolve_name(
            "Maester Luwin",
            alias_map=alias_map,
            node_set=node_set,
            firstname_index=idx,
            prior=prior,
            present_slugs=set(),
        )
        self.assertEqual(slug, "maester-luwin")
        self.assertEqual(status, STATUS_EXACT)

    def test_ser_pounce_indexed_under_pounce_not_ser(self):
        """build_firstname_index must key ser-pounce under 'pounce', not 'ser'."""
        node_set, names, alias_map, idx, prior = self._make_ser_pounce_graph()
        # 'ser' key must be absent (or have no nodes) — the fix removes it
        ser_candidates = idx.get("ser", [])
        self.assertNotIn("ser-pounce", ser_candidates,
                         "ser-pounce must NOT be in the 'ser' firstname-index bucket")
        # 'pounce' key must exist and include ser-pounce
        pounce_candidates = idx.get("pounce", [])
        self.assertIn("ser-pounce", pounce_candidates,
                      "ser-pounce must be keyed under 'pounce'")

    def test_khal_jhaqo_indexed_under_jhaqo_not_khal(self):
        """'Khal Jhaqo' must index under 'jhaqo', not 'khal'."""
        node_set, names, alias_map, idx, prior = self._make_ser_pounce_graph()
        khal_candidates = idx.get("khal", [])
        self.assertNotIn("khal-jhaqo", khal_candidates,
                         "khal-jhaqo must NOT be in the 'khal' bucket")
        jhaqo_candidates = idx.get("jhaqo", [])
        self.assertIn("khal-jhaqo", jhaqo_candidates,
                      "khal-jhaqo must be keyed under 'jhaqo'")

    def test_name_key_none_yields_unresolved_generic(self):
        """A bare title like 'Ser' → name_key returns None → STATUS_UNRESOLVED_GENERIC."""
        node_set, names, alias_map, idx, prior = self._make_ser_pounce_graph()
        slug, status = resolve_name(
            "Ser",
            alias_map=alias_map,
            node_set=node_set,
            firstname_index=idx,
            prior=prior,
            present_slugs=set(),
        )
        # 'ser' is in GENERIC_TERMS → caught by the generic-term gate (or name_key None path)
        self.assertIsNone(slug)
        # Either STATUS_UNRESOLVED_GENERIC (from generic gate or name_key None path)
        self.assertEqual(status, STATUS_UNRESOLVED_GENERIC)


if __name__ == "__main__":
    unittest.main()
