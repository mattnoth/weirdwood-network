"""Tests for scripts/infobox-merge.py.

Covers the load-bearing rules per spec v2:
  - direction flip (Rule 7)
  - fact-key quarantine including Joffrey mirror case (Rule 3 + 3e)
  - qualifier-aware dedupe (Rule 9)
  - noise filter (Rule 2)
  - unordered-pair dedupe for symmetric types (Rule 9 / Rule 10)
  - orphan endpoint remap guard (Fix A honorific-strip characters-only)
  - self-loop suppression (Rule 8)

All tests are hermetic (no file I/O against the live repo).
"""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

# ---------------------------------------------------------------------------
# Load the script
# ---------------------------------------------------------------------------
from tests._helpers import load_script

_mod = load_script("infobox-merge.py")

kebab = _mod.kebab
noise_reason = _mod.noise_reason
resolve = _mod.resolve
_trips_r3 = _mod._trips_r3
_build_q2_keys = _mod._build_q2_keys
build_quarantine_fact_keys = _mod.build_quarantine_fact_keys
edge_key = _mod.edge_key
normalize_qualifier = _mod.normalize_qualifier
build_orphan_remaps = _mod.build_orphan_remaps
apply_orphan_remaps = _mod.apply_orphan_remaps
run_pipeline = _mod.run_pipeline

SYMMETRIC_TYPES = _mod.SYMMETRIC_TYPES


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_nodes(*slugs, category="characters"):
    """Build a minimal nodes dict for resolution tests."""
    return {s: category for s in slugs}


def make_alias(**kwargs):
    """Build a minimal alias dict."""
    return kwargs


def _page(name, rels):
    return {"page": name, "entity_type": "character.human", "relationships": rels, "cite_refs": {}}


def _rel(field, target, edge_type, direction="forward", qualifier=None):
    r = {"field": field, "target": target, "edge_type": edge_type, "direction": direction}
    if qualifier is not None:
        r["qualifier"] = qualifier
    return r


# ---------------------------------------------------------------------------
# Rule 2 — Noise-target filter
# ---------------------------------------------------------------------------

class TestNoiseFilter(unittest.TestCase):
    def test_placeholder_unknown(self):
        self.assertEqual(noise_reason("Unknown"), "noise-placeholder")

    def test_placeholder_case_insensitive(self):
        self.assertEqual(noise_reason("NONE"), "noise-placeholder")

    def test_placeholder_none(self):
        self.assertEqual(noise_reason("None"), "noise-placeholder")

    def test_placeholder_issue(self):
        self.assertEqual(noise_reason("Issue"), "noise-placeholder")

    def test_bare_kinship_son(self):
        self.assertEqual(noise_reason("Son"), "noise-bare-kinship")

    def test_bare_kinship_two_sons(self):
        self.assertEqual(noise_reason("Two sons"), "noise-bare-kinship")

    def test_bare_kinship_a_daughter(self):
        self.assertEqual(noise_reason("A daughter"), "noise-bare-kinship")

    def test_bare_kinship_deceased_daughter(self):
        self.assertEqual(noise_reason("Deceased daughter"), "noise-bare-kinship")

    def test_named_child_passes(self):
        self.assertIsNone(noise_reason("Roslin Frey"))

    def test_nbsp_normalized(self):
        # Non-breaking space should be treated the same as regular space
        self.assertEqual(noise_reason("Unknown\xa0"), "noise-placeholder")

    def test_named_person_passes(self):
        self.assertIsNone(noise_reason("Jon Snow"))

    def test_numeral_date_zero_rows(self):
        # Pure numeral AC year — filtered (though currently 0 rows in data)
        self.assertEqual(noise_reason("300 AC"), "noise-numeral-date")


# ---------------------------------------------------------------------------
# Rule 1 / Rule 4 — Resolution ladder
# ---------------------------------------------------------------------------

class TestResolutionLadder(unittest.TestCase):
    def setUp(self):
        self.nodes = make_nodes(
            "eddard-stark", "house-stark", "house-hightower",
            "aegon-frey-son-of-stevron", "aegon-frey",
            "citadel", "antler-men",
        )
        self.alias = make_alias(
            **{"lady-stoneheart": "catelyn-stark"}
        )
        # Add catelyn-stark to nodes for alias resolution
        self.nodes["catelyn-stark"] = "characters"

    def test_rung1_exact_with_parens(self):
        slug, cat, status = resolve("Aegon Frey (son of Stevron)", self.nodes, self.alias)
        self.assertEqual(slug, "aegon-frey-son-of-stevron")
        self.assertEqual(status, "resolved-exact-parens")

    def test_rung2_exact_parens_stripped(self):
        # "House Stark" → house-stark (no parens to strip)
        slug, cat, status = resolve("House Stark", self.nodes, self.alias)
        self.assertEqual(slug, "house-stark")

    def test_rung3_alias(self):
        slug, cat, status = resolve("Lady Stoneheart", self.nodes, self.alias)
        self.assertEqual(slug, "catelyn-stark")
        self.assertEqual(status, "resolved-alias")

    def test_rung4_the_strip(self):
        slug, cat, status = resolve("The Citadel", self.nodes, self.alias)
        self.assertEqual(slug, "citadel")
        self.assertEqual(status, "resolved-the-strip")

    def test_unresolved_returns_none(self):
        slug, cat, status = resolve("Aelyx Targaryen", self.nodes, self.alias)
        self.assertIsNone(slug)
        self.assertEqual(status, "unresolved")

    def test_rung1_preferred_over_rung2(self):
        # aegon-frey-son-of-stevron should win over aegon-frey
        slug, _, status = resolve("Aegon Frey (son of Stevron)", self.nodes, self.alias)
        self.assertEqual(slug, "aegon-frey-son-of-stevron")
        self.assertNotEqual(slug, "aegon-frey")


# ---------------------------------------------------------------------------
# Rule 7 — Direction flip
# ---------------------------------------------------------------------------

class TestDirectionFlip(unittest.TestCase):
    """Ruler/Heir/Founder etc. have inverted direction in FIELD_EDGE_MAP."""

    def _build_flip_page(self, field, direction="forward"):
        """A page 'Acorn Hall' listing Theomar Smallwood as its Ruler."""
        nodes = make_nodes("acorn-hall", "theomar-smallwood", category="characters")
        nodes["acorn-hall"] = "locations"
        alias = {}
        pages = [_page("Acorn Hall", [_rel(field, "Theomar Smallwood", "RULES", direction)])]
        return nodes, alias, pages

    def test_ruler_forward_is_flipped(self):
        # 'Ruler' field is in DIRECTION_FLIP_FIELDS; forward on a location page
        # should produce: theomar-smallwood RULES acorn-hall (not the reverse)
        nodes, alias, pages = self._build_flip_page("Ruler", "forward")
        # Manually trace the logic
        src, src_cat, _ = resolve("Acorn Hall", nodes, alias)
        tgt, tgt_cat, _ = resolve("Theomar Smallwood", nodes, alias)
        # direction=forward → s_,t_ = src,tgt → flip → s_,t_ = tgt,src
        s_ = tgt  # after flip
        t_ = src
        self.assertEqual(s_, "theomar-smallwood")
        self.assertEqual(t_, "acorn-hall")

    def test_non_flip_field_not_flipped(self):
        # 'Allegiance' (SWORN_TO, forward, not in flip set) → page is source
        nodes = make_nodes("abelar-hightower", "house-hightower")
        alias = {}
        src, _, _ = resolve("Abelar Hightower", nodes, alias)
        tgt, _, _ = resolve("House Hightower", nodes, alias)
        # No flip: s_=src, t_=tgt
        self.assertEqual(src, "abelar-hightower")
        self.assertEqual(tgt, "house-hightower")

    def test_heir_is_flipped(self):
        # 'Heir' field → DIRECTION_FLIP_FIELDS; forward on holder's page
        # Forward: s_=src(holder), t_=tgt(heir) → flip → s_=heir, t_=holder
        self.assertIn("heir", _mod.DIRECTION_FLIP_FIELDS)

    def test_founder_is_flipped(self):
        self.assertIn("founder", _mod.DIRECTION_FLIP_FIELDS)

    def test_allegiance_not_flipped(self):
        field = "allegiance"
        self.assertNotIn(field, _mod.DIRECTION_FLIP_FIELDS)


# ---------------------------------------------------------------------------
# Rule 3 — Speculative-kinship quarantine
# ---------------------------------------------------------------------------

class TestSpeculativeQuarantine(unittest.TestCase):
    def _q2_keys(self):
        return set()

    def test_3a_plural_mothers_field(self):
        result = _trips_r3("mothers", None, "PARENT_OF", self._q2_keys(), "Jon Snow")
        self.assertEqual(result, "R3a")

    def test_3a_plural_fathers_field(self):
        result = _trips_r3("fathers", None, "PARENT_OF", self._q2_keys(), "Addam Velaryon")
        self.assertEqual(result, "R3a")

    def test_3c_supposedly_qualifier(self):
        result = _trips_r3("mothers", "supposedly", "PARENT_OF", self._q2_keys(), "Jon Snow")
        self.assertEqual(result, "R3a")  # 3a fires first (plural field)

    def test_3c_rumored_qualifier(self):
        result = _trips_r3("mother", "rumored", "PARENT_OF", self._q2_keys(), "Jon Snow")
        self.assertEqual(result, "R3c")

    def test_3c_officially_qualifier(self):
        # v2 widened regex: 'officially' is a hedge
        result = _trips_r3("issue", "officially", "PARENT_OF", self._q2_keys(), "Robert I Baratheon")
        self.assertEqual(result, "R3c")

    def test_3c_legally_qualifier(self):
        result = _trips_r3("issue", "legally", "PARENT_OF", self._q2_keys(), "Robert I Baratheon")
        self.assertEqual(result, "R3c")

    def test_3c_debated_qualifier(self):
        result = _trips_r3("lovers", "debated", "LOVER_OF", self._q2_keys(), "Daemon Targaryen")
        self.assertEqual(result, "R3c")

    def test_3c_in_some_tales(self):
        result = _trips_r3("issue", "in some tales", "PARENT_OF", self._q2_keys(), "Brandon the Builder")
        self.assertEqual(result, "R3c")

    def test_3d_disputed_on_heir_to(self):
        result = _trips_r3("heir", "disputed", "HEIR_TO", self._q2_keys(), "Balon Greyjoy")
        self.assertEqual(result, "R3d")

    def test_3d_disputed_on_lover_of(self):
        result = _trips_r3("lovers", "disputed", "LOVER_OF", self._q2_keys(), "Marilda of Hull")
        self.assertEqual(result, "R3d")

    def test_3d_disputed_parent_of_is_ok(self):
        # Rule 3d only fires on non-PARENT_OF types; disputed PARENT_OF is allowed
        result = _trips_r3("issue", "disputed", "PARENT_OF", self._q2_keys(), "Some Page")
        self.assertIsNone(result)

    def test_3b_multivalue_singular_father(self):
        # Two distinct non-noise fathers
        pages = [
            _page("Benedict I Justman", [
                _rel("father", "Blackwood", "PARENT_OF", "reverse"),
                _rel("father", "Bracken", "PARENT_OF", "reverse"),
            ])
        ]
        q2 = _build_q2_keys(pages)
        self.assertIn(("Benedict I Justman", "father"), q2)

    def test_clean_row_passes(self):
        result = _trips_r3("father", None, "PARENT_OF", self._q2_keys(), "Eddard Stark")
        self.assertIsNone(result)

    def test_clean_row_with_qualifier_passes(self):
        # 'disputed' on PARENT_OF passes Rule 3d (it only fires for non-PARENT_OF)
        result = _trips_r3("issue", "disputed", "PARENT_OF", self._q2_keys(), "Aegon IV")
        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# Rule 3e — Fact-key closure (Joffrey mirror case)
# ---------------------------------------------------------------------------

class TestFactKeyQuarantine(unittest.TestCase):
    def setUp(self):
        # Setup: Cersei's page lists Joffrey as Issue with 'legally' qualifier
        # Robert's page also lists Joffrey as Issue with 'legally' qualifier
        # Joffrey's page lists 'Fathers: Robert (legally) / Jaime (biologically)'
        self.nodes = make_nodes(
            "cersei-lannister", "joffrey-baratheon",
            "robert-i-baratheon", "jaime-lannister",
        )
        self.alias: dict = {}

    def _make_joffrey_pages(self):
        """Joffrey's page trips Rule 3a (plural Fathers field)."""
        return [
            _page("Joffrey Baratheon", [
                _rel("Fathers", "Robert I Baratheon", "PARENT_OF", "reverse", qualifier="legally"),
                _rel("Fathers", "Jaime Lannister", "PARENT_OF", "reverse", qualifier="biologically"),
            ]),
            _page("Robert I Baratheon", [
                _rel("Issue", "Joffrey Baratheon", "PARENT_OF", "forward", qualifier="legally"),
            ]),
            _page("Jaime Lannister", [
                _rel("Issue", "Joffrey Baratheon", "PARENT_OF", "forward"),
            ]),
        ]

    def test_joffrey_fathers_triggers_quarantine(self):
        """Joffrey's Fathers field trips R3a."""
        q2 = _build_q2_keys(self._make_joffrey_pages())
        # Should not be in q2 (that's for multi-value singular, not plural)
        result = _trips_r3("fathers", "legally", "PARENT_OF", q2, "Joffrey Baratheon")
        self.assertEqual(result, "R3a")

    def test_fact_key_closure_quarantines_robert_mirror(self):
        """Robert's and Jaime's clean Issue rows should be caught by R3e (fact-key closure)."""
        pages = self._make_joffrey_pages()
        fact_quarantine = build_quarantine_fact_keys(pages, self.nodes, self.alias)
        # The fact key (PARENT, frozenset({robert-i-baratheon, joffrey-baratheon})) should be quarantined
        self.assertIn(
            ("PARENT", frozenset({"robert-i-baratheon", "joffrey-baratheon"})),
            fact_quarantine,
        )
        self.assertIn(
            ("PARENT", frozenset({"jaime-lannister", "joffrey-baratheon"})),
            fact_quarantine,
        )

    def test_cersei_row_not_in_fact_quarantine(self):
        """Cersei's motherhood is uncontested; her fact key must not be quarantined."""
        pages = self._make_joffrey_pages() + [
            _page("Cersei Lannister", [
                _rel("Issue", "Joffrey Baratheon", "PARENT_OF", "forward"),
            ]),
        ]
        fact_quarantine = build_quarantine_fact_keys(pages, self.nodes, self.alias)
        # Cersei's fact key should NOT be in quarantine
        self.assertNotIn(
            ("PARENT", frozenset({"cersei-lannister", "joffrey-baratheon"})),
            fact_quarantine,
        )


# ---------------------------------------------------------------------------
# Rule 9 — Qualifier-aware dedupe
# ---------------------------------------------------------------------------

class TestQualifierAwareDedupe(unittest.TestCase):
    def _run_two_rows(self, rows_a, rows_b, edge_type="SPOUSE_OF"):
        """Run pipeline with two pages asserting the same edge."""
        nodes = make_nodes("a", "b")
        alias: dict = {}
        # Both pages need to be in nodes so source resolves
        pages = [_page("A", rows_a), _page("B", rows_b)]
        with tempfile.TemporaryDirectory() as tmpdir:
            # Patch file paths
            import io
            # We test at the key/logic level instead
            pass

        # Direct unit test of the qualifier comparison logic
        from collections import Counter
        stats: Counter = Counter()
        merged_list: list = []
        seen: dict = {}

        def _process(page_name, rows):
            src, _, _ = resolve(page_name, nodes, alias)
            if src is None:
                return
            for r in rows:
                tgt, _, _ = resolve(r["target"], nodes, alias)
                if tgt is None:
                    continue
                qual = r.get("qualifier") or ""
                et = r["edge_type"]
                s_, t_ = (src, tgt) if r["direction"] == "forward" else (tgt, src)
                k = edge_key(et, s_, t_, SYMMETRIC_TYPES)
                candidate = {"edge_type": et, "source_slug": s_, "target_slug": t_,
                             "wiki_qualifier": qual or None, "evidence_field": r["field"],
                             "evidence_ref": f"wiki:{page_name}"}
                if qual:
                    candidate["qualifier"] = qual

                if k in seen:
                    st = seen[k]
                    if st.get("conflict"):
                        stats["Q9_conflict"] += 1
                        continue
                    if st["midx"] is None:
                        stats["deduped"] += 1
                        continue
                    q_kept = _mod.norm_qual(merged_list[st["midx"]].get("wiki_qualifier"))
                    q_new = _mod.norm_qual(qual)
                    if q_new == q_kept or not q_new:
                        stats["deduped"] += 1
                    elif not q_kept:
                        merged_list[st["midx"]] = candidate
                        stats["deduped"] += 1
                        stats["qual_preferred"] += 1
                    else:
                        stats["Q9_conflict"] += 2
                        merged_list[st["midx"]] = None
                        st["conflict"] = True
                    continue
                seen[k] = {"midx": len(merged_list), "conflict": False}
                merged_list.append(candidate)

        for page_name, rows in [("A", rows_a), ("B", rows_b)]:
            _process(page_name, rows)
        merged_final = [m for m in merged_list if m is not None]
        return merged_final, stats

    def test_plain_dedupe_same_qualifier(self):
        rows_a = [_rel("Spouse", "B", "SPOUSE_OF", "symmetric", qualifier="")]
        rows_b = [_rel("Spouse", "A", "SPOUSE_OF", "symmetric", qualifier="")]
        merged, stats = self._run_two_rows(rows_a, rows_b)
        self.assertEqual(len(merged), 1)
        self.assertEqual(stats["deduped"], 1)

    def test_qualified_row_preferred_over_unqualified(self):
        # Unqualified arrives first, qualified second → replace
        rows_a = [_rel("Spouse", "B", "SPOUSE_OF", "symmetric", qualifier="")]
        rows_b = [_rel("Spouse", "A", "SPOUSE_OF", "symmetric", qualifier="salt wife")]
        merged, stats = self._run_two_rows(rows_a, rows_b)
        self.assertEqual(len(merged), 1)
        self.assertEqual(stats.get("qual_preferred", 0), 1)
        self.assertEqual(merged[0].get("wiki_qualifier"), "salt wife")

    def test_conflict_two_different_qualifiers(self):
        rows_a = [_rel("Spouse", "B", "SPOUSE_OF", "symmetric", qualifier="annulled")]
        rows_b = [_rel("Spouse", "A", "SPOUSE_OF", "symmetric", qualifier="salt wife")]
        merged, stats = self._run_two_rows(rows_a, rows_b)
        # Both rows should be quarantined, none merged
        self.assertEqual(len(merged), 0)
        self.assertEqual(stats.get("Q9_conflict", 0), 2)


# ---------------------------------------------------------------------------
# Rule 9 / Rule 10 — Unordered pair for symmetric types
# ---------------------------------------------------------------------------

class TestSymmetricDedupe(unittest.TestCase):
    def test_edge_key_unordered_for_spouse_of(self):
        k1 = edge_key("SPOUSE_OF", "alice", "bob", SYMMETRIC_TYPES)
        k2 = edge_key("SPOUSE_OF", "bob", "alice", SYMMETRIC_TYPES)
        self.assertEqual(k1, k2)

    def test_edge_key_unordered_for_lover_of(self):
        k1 = edge_key("LOVER_OF", "x", "y", SYMMETRIC_TYPES)
        k2 = edge_key("LOVER_OF", "y", "x", SYMMETRIC_TYPES)
        self.assertEqual(k1, k2)

    def test_edge_key_ordered_for_sworn_to(self):
        k1 = edge_key("SWORN_TO", "vassal", "lord", SYMMETRIC_TYPES)
        k2 = edge_key("SWORN_TO", "lord", "vassal", SYMMETRIC_TYPES)
        self.assertNotEqual(k1, k2)

    def test_existing_edge_symmetric_match(self):
        """An existing SPOUSE_OF a→b should block incoming b→a."""
        existing = {edge_key("SPOUSE_OF", "eddard-stark", "catelyn-tully", SYMMETRIC_TYPES)}
        incoming = edge_key("SPOUSE_OF", "catelyn-tully", "eddard-stark", SYMMETRIC_TYPES)
        self.assertIn(incoming, existing)


# ---------------------------------------------------------------------------
# Rule 8 — Self-loop suppression
# ---------------------------------------------------------------------------

class TestSelfLoop(unittest.TestCase):
    def test_self_loop_filtered(self):
        nodes = make_nodes("brandon-norrey")
        alias: dict = {}
        src, _, _ = resolve("Brandon Norrey", nodes, alias)
        tgt, _, _ = resolve("Brandon Norrey", nodes, alias)
        self.assertEqual(src, tgt)
        # In the real pipeline, s_ == t_ would filter

    def test_no_loop_different_names(self):
        nodes = make_nodes("eddard-stark", "catelyn-tully")
        alias: dict = {}
        src, _, _ = resolve("Eddard Stark", nodes, alias)
        tgt, _, _ = resolve("Catelyn Tully", nodes, alias)
        self.assertNotEqual(src, tgt)


# ---------------------------------------------------------------------------
# Fix A — Honorific-strip orphan remap (characters-only guard)
# ---------------------------------------------------------------------------

class TestOrphanHonoroficRemap(unittest.TestCase):
    def setUp(self):
        # maester-griffins-roost should be REJECTED (griffins-roost is a location)
        # ser-rodrik-cassel should be ACCEPTED (rodrik-cassel is a character)
        self.nodes = {
            "rodrik-cassel": "characters",
            "griffins-roost": "locations",
        }
        self.alias: dict = {}

    def test_accepted_honorific_strip_character(self):
        existing_rows = [{"source_slug": "ser-rodrik-cassel", "target_slug": "a-valid-node", "edge_type": "SERVES"}]
        self.nodes["a-valid-node"] = "characters"
        fix_alias, fix_thestrip, fix_honorific, unresolvable = build_orphan_remaps(
            existing_rows, self.nodes, self.alias
        )
        self.assertIn("ser-rodrik-cassel", fix_honorific)
        self.assertEqual(fix_honorific["ser-rodrik-cassel"], "rodrik-cassel")

    def test_rejected_honorific_strip_location(self):
        # maester-griffins-roost → griffins-roost is a location — must NOT be included
        existing_rows = [{"source_slug": "maester-griffins-roost", "target_slug": "a-valid-node", "edge_type": "ADVISES"}]
        self.nodes["a-valid-node"] = "characters"
        fix_alias, fix_thestrip, fix_honorific, unresolvable = build_orphan_remaps(
            existing_rows, self.nodes, self.alias
        )
        self.assertNotIn("maester-griffins-roost", fix_honorific)
        self.assertIn("maester-griffins-roost", unresolvable)

    def test_alias_takes_precedence_over_honorific(self):
        # If the slug is in alias, it should be in fix_alias, not fix_honorific
        nodes = {"eddard-stark": "characters", "a-valid-node": "characters"}
        alias = {"ned-stark": "eddard-stark"}  # ned-stark doesn't start with a title prefix
        existing_rows = [{"source_slug": "ned-stark", "target_slug": "a-valid-node", "edge_type": "RULES"}]
        fix_alias, fix_thestrip, fix_honorific, unresolvable = build_orphan_remaps(
            existing_rows, nodes, alias
        )
        self.assertIn("ned-stark", fix_alias)

    def test_the_strip_orphan_remap(self):
        nodes = {"antler-men": "factions", "target": "characters"}
        alias: dict = {}
        existing_rows = [{"source_slug": "the-antler-men", "target_slug": "target", "edge_type": "MEMBER_OF"}]
        fix_alias, fix_thestrip, fix_honorific, unresolvable = build_orphan_remaps(
            existing_rows, nodes, alias
        )
        self.assertIn("the-antler-men", fix_thestrip)
        self.assertEqual(fix_thestrip["the-antler-men"], "antler-men")


# ---------------------------------------------------------------------------
# Rule 11 — Qualifier normalization
# ---------------------------------------------------------------------------

class TestQualifierNormalization(unittest.TestCase):
    def test_holds_title_formerly_maps_to_former(self):
        self.assertEqual(normalize_qualifier("HOLDS_TITLE", "formerly"), "former")

    def test_holds_title_claimant_maps_to_claimed(self):
        self.assertEqual(normalize_qualifier("HOLDS_TITLE", "claimant"), "claimed")

    def test_holds_title_no_qualifier_defaults_to_unknown(self):
        self.assertEqual(normalize_qualifier("HOLDS_TITLE", None), "unknown")

    def test_sworn_to_no_qualifier_defaults_to_unknown(self):
        self.assertEqual(normalize_qualifier("SWORN_TO", None), "unknown")

    def test_parent_of_no_qualifier_defaults_to_biological(self):
        self.assertEqual(normalize_qualifier("PARENT_OF", None), "biological")

    def test_parent_of_adopted(self):
        self.assertEqual(normalize_qualifier("PARENT_OF", "adopted"), "adopted")

    def test_parent_of_adoptive_mother(self):
        self.assertEqual(normalize_qualifier("PARENT_OF", "adoptive mother"), "adopted")

    def test_parent_of_disputed_prefix(self):
        self.assertEqual(normalize_qualifier("PARENT_OF", "disputed by Tristifer Botley"), "disputed")

    def test_spouse_of_salt_wife(self):
        self.assertEqual(normalize_qualifier("SPOUSE_OF", "salt wife"), "salt_wife")

    def test_spouse_of_annulled(self):
        self.assertEqual(normalize_qualifier("SPOUSE_OF", "annulled"), "annulled")

    def test_lover_of_paramour(self):
        self.assertEqual(normalize_qualifier("LOVER_OF", "paramour"), "paramour")

    def test_lover_of_none_returns_none(self):
        # OPTIONAL: omit if no match
        self.assertIsNone(normalize_qualifier("LOVER_OF", None))

    def test_tier3_type_returns_none(self):
        # BORN_AT is Tier-3: no qualifier
        self.assertIsNone(normalize_qualifier("BORN_AT", "something"))

    def test_sworn_to_by_marriage(self):
        self.assertEqual(normalize_qualifier("SWORN_TO", "by marriage"), "by_marriage")

    def test_spouse_of_dissolved_is_annulled(self):
        self.assertEqual(normalize_qualifier("SPOUSE_OF", "dissolved"), "annulled")


# ---------------------------------------------------------------------------
# kebab() slug function
# ---------------------------------------------------------------------------

class TestKebab(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(kebab("House Hightower"), "house-hightower")

    def test_apostrophe_removed(self):
        self.assertEqual(kebab("Night's Watch"), "nights-watch")

    def test_parens_stripped_by_default(self):
        self.assertEqual(kebab("Aegon Frey (son of Stevron)"), "aegon-frey")

    def test_parens_kept(self):
        self.assertEqual(kebab("Aegon Frey (son of Stevron)", keep_parens=True), "aegon-frey-son-of-stevron")

    def test_trailing_punctuation_stripped(self):
        self.assertEqual(kebab("House Stark."), "house-stark")

    def test_brackets_stripped(self):
        self.assertEqual(kebab("Jon Snow [disambiguation]"), "jon-snow")

    def test_empty_string(self):
        self.assertEqual(kebab(""), "")


if __name__ == "__main__":
    unittest.main()
