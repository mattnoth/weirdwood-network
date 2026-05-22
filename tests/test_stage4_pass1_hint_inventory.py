"""Tests for scripts/stage4-pass1-hint-inventory.py.

Validates:
- Table parsing from inline fixture (including the real acok-arya-01 section)
- Separator / header row detection
- Hint normalization
- HINT_TO_EDGE deterministic mapping (layers 1+2: exact+prefix)
- Keyword/regex layer (layer 3): positive matches, exclusion rules,
  precedence ordering (in-law before sibling, lover before love, etc.)
- Combined map_hint_to_edge covers all three layers in order
- Edge-case robustness (extra spaces, missing trailing pipe, short rows)

Run: python3 -m unittest tests.test_stage4_pass1_hint_inventory -v
"""

import unittest

from tests._helpers import load_script

inv = load_script("stage4-pass1-hint-inventory.py")


# ---------------------------------------------------------------------------
# Fixture: real acok-arya-01 Relationships Observed section body
# (everything after the '## Relationships Observed' line, before the next ##)
# ---------------------------------------------------------------------------

ACOK_ARYA_01_SECTION = """\
| Character A | Relationship | Character B | Evidence |
|-------------|-------------|-------------|----------|
| Arya | Disguised protégée of | Yoren | Yoren cut her hair, disguised her, protects her identity, disciplines her |
| Arya | Deep love and longing for | Jon Snow | Thinks of him most; dreams of him calling her "little sister"; Needle is his gift to her |
| Arya | Mourning | Eddard Stark | Cries in her sleep dreaming of him; associates the red comet with Ice and his blood |
| Arya | Hatred toward | Joffrey | "Someone should kill him!" |
| Arya | Hatred toward | Cersei (the queen) | Wishes the city would wash her away |
| Arya | Complicated feelings toward | Sansa | Would wish the city destroyed but stops because Sansa is still there |
| Arya | Longing for | Robb, Bran, Rickon, her mother | Yearns to see them at Winterfell |
| Arya | Student of (recalled) | Syrio Forel | Uses his teaching ("Calm as still water"); fights in water dancer's stance |
| Arya | Antagonized by | Lommy Greenhands | Lommy names her "Lumpyhead," taunts her, eggs Hot Pie on |
| Arya | Antagonized by, then dominates | Hot Pie | Hot Pie bullies her, tries to take Needle; Arya beats him severely |
| The Bull | Protects / defends | Arya | Tells bullies to leave her alone; warns her during the fight |
| Lommy | Fears | The Bull | "Lommy didn't dare mock the Bull" — he's older and bigger |
| Lommy | Fears (after fight) | Arya | Twitches every time she looks at him; stays far away |
| Yoren | Recruiter/escort for | Night's Watch | Taking men and boys to the Wall; wears the black |
| Yoren | Disciplinarian over | Arya | Beats her with the stick for fighting; threatens consequences |
| Yoren | Connected to unnamed messenger regarding | Eddard Stark | Someone brought word that Eddard would take the black; Yoren was waiting |
| Jon Snow | Gave Needle to | Arya | Arya recalls Jon giving her Needle |
"""


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

class TestParseTableRow(unittest.TestCase):
    """parse_table_row should split pipe-delimited markdown rows."""

    def test_standard_row(self):
        row = "| Arya | Deep love and longing for | Jon Snow | Evidence text |"
        cells = inv.parse_table_row(row)
        self.assertIsNotNone(cells)
        self.assertEqual(cells[0], "Arya")
        self.assertEqual(cells[1], "Deep love and longing for")
        self.assertEqual(cells[2], "Jon Snow")

    def test_non_table_line(self):
        self.assertIsNone(inv.parse_table_row("This is not a table row"))
        self.assertIsNone(inv.parse_table_row(""))

    def test_separator_detection(self):
        sep = "|-------------|-------------|-------------|----------|"
        cells = inv.parse_table_row(sep)
        self.assertTrue(inv.is_separator_row(cells))

    def test_header_detection(self):
        header = "| Character A | Relationship | Character B | Evidence |"
        cells = inv.parse_table_row(header)
        self.assertTrue(inv.is_header_row(cells))


class TestAcokArya01(unittest.TestCase):
    """Validate parser against the real acok-arya-01 table — must find exactly 17 rows
    (the section has 17 data rows in the actual file)."""

    def setUp(self):
        self.rows, self.warnings = inv.parse_relationships_from_section(
            ACOK_ARYA_01_SECTION, "acok-arya-01", "acok"
        )

    def test_row_count(self):
        """The fixture has 17 relationship rows (not 14 — re-counted from real file)."""
        # The real file has 17 rows (lines 177-193 inclusive = 17 data rows)
        self.assertEqual(
            len(self.rows),
            17,
            f"Expected 17 rows, got {len(self.rows)}. Rows: {[r['hint_original'] for r in self.rows]}",
        )

    def test_no_warnings(self):
        self.assertEqual(self.warnings, [], f"Unexpected warnings: {self.warnings}")

    def test_first_row_fields(self):
        row = self.rows[0]
        self.assertEqual(row["source"], "Arya")
        self.assertIn("Disguised", row["hint_original"])
        self.assertEqual(row["target"], "Yoren")
        self.assertEqual(row["chapter_id"], "acok-arya-01")
        self.assertEqual(row["book"], "acok")

    def test_hint_normalization(self):
        """hint_norm is lowercased and stripped."""
        for row in self.rows:
            self.assertEqual(row["hint_norm"], row["hint_original"].strip().lower())

    def test_specific_hints_present(self):
        hints = {r["hint_norm"] for r in self.rows}
        self.assertIn("mourning", hints)
        self.assertIn("hatred toward", hints)
        self.assertIn("deep love and longing for", hints)
        self.assertIn("fears", hints)

    def test_all_chapter_ids_set(self):
        for row in self.rows:
            self.assertEqual(row["chapter_id"], "acok-arya-01")


class TestNormalizeHint(unittest.TestCase):
    def test_strips_and_lowercases(self):
        self.assertEqual(inv.normalize_hint("  Deep Love  "), "deep love")
        self.assertEqual(inv.normalize_hint("MOURNING"), "mourning")
        self.assertEqual(inv.normalize_hint("Student of (recalled)"), "student of (recalled)")


class TestMapHintToEdgeExactPrefix(unittest.TestCase):
    """Layers 1+2 (exact + prefix map) should cover unambiguous common cases."""

    def test_exact_matches(self):
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("mourning"), "MOURNS")
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("deep love and longing for"), "LOVES")
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("hatred toward"), "HATES")
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("fears"), "FEARS")
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("student of (recalled)"), "TUTORS")
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("fears (after fight)"), "FEARS")
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("disciplinarian over"), "COMMANDS")
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("antagonized by"), "OPPOSES")
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("protects / defends"), "PROTECTS")
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("recruiter/escort for"), "MEMBER_OF")
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("gave needle to"), "GIFTED_TO")

    def test_prefix_matches(self):
        # Parenthesized suffixes are fine (no comma outside parens)
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("kills (self-described)"), "KILLS")
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("mourns/grieves deeply"), "MOURNS")
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("serves reluctantly"), "SERVES")
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("brother of (paternal)"), "SIBLING_OF")
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("father of (adoptive)"), "PARENT_OF")
        # Comma outside parens → compound → None (LLM)
        self.assertIsNone(inv.map_hint_to_edge_exact_prefix("father of, protects"))

    def test_not_reached_by_keyword_layer(self):
        """Phrases resolved by layers 1+2 should not need keyword layer."""
        # These exact phrases are in the exact map; confirm they resolve quickly.
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("bonded to"), "BONDED_TO")
        self.assertEqual(inv.map_hint_to_edge_exact_prefix("wargs into"), "WARGS_INTO")


class TestMapHintKeyword(unittest.TestCase):
    """Layer 3 keyword/regex classifier — positive matches and exclusions."""

    # --- Kinship ---
    def test_in_law_before_sibling(self):
        """brother-in-law must map to IN_LAW_OF, not SIBLING_OF."""
        self.assertEqual(inv.map_hint_keyword("brother-in-law of"), "IN_LAW_OF")
        self.assertEqual(inv.map_hint_keyword("sister-in-law of"), "IN_LAW_OF")
        self.assertEqual(inv.map_hint_keyword("father-in-law (grudging)"), "IN_LAW_OF")

    def test_widow_of(self):
        self.assertEqual(inv.map_hint_keyword("widow of"), "SPOUSE_OF")

    def test_betrothed_variants(self):
        self.assertEqual(inv.map_hint_keyword("was betrothed to"), "BETROTHED_TO")
        self.assertEqual(inv.map_hint_keyword("former betrothed of"), "BETROTHED_TO")

    def test_grand_kin(self):
        self.assertEqual(inv.map_hint_keyword("grandson of"), "PARENT_OF")
        self.assertEqual(inv.map_hint_keyword("granddaughter of"), "PARENT_OF")
        self.assertEqual(inv.map_hint_keyword("grandfather of"), "PARENT_OF")

    def test_great_kin(self):
        self.assertEqual(inv.map_hint_keyword("great-niece of"), "PARENT_OF")
        self.assertEqual(inv.map_hint_keyword("great-grandmother of"), "PARENT_OF")

    def test_cousin(self):
        self.assertEqual(inv.map_hint_keyword("cousin to"), "COUSIN_OF")
        self.assertEqual(inv.map_hint_keyword("cousin of"), "COUSIN_OF")

    def test_nephew_niece(self):
        self.assertEqual(inv.map_hint_keyword("nephew of"), "NEPHEW_OF")
        self.assertEqual(inv.map_hint_keyword("great-niece of"), "PARENT_OF")  # great- fires first
        self.assertEqual(inv.map_hint_keyword("niece, warmly affectionate"), "UNCLE_OF")

    def test_uncle_aunt(self):
        self.assertEqual(inv.map_hint_keyword("uncle to"), "UNCLE_OF")
        # "aunt" with word boundary — "taunts" must NOT match
        self.assertNotEqual(inv.map_hint_keyword("taunts"), "UNCLE_OF")

    def test_sibling_variants(self):
        self.assertEqual(inv.map_hint_keyword("brother to"), "SIBLING_OF")
        self.assertEqual(inv.map_hint_keyword("sister to"), "SIBLING_OF")
        self.assertEqual(inv.map_hint_keyword("protective older brother"), "SIBLING_OF")
        # brotherhood has \bbrother\b inside it? No — "brotherhood" word boundary test
        # "brotherhood" → \bbrother\b does NOT match because "brother" is a proper word
        # Actually \bbrother\b DOES match inside "brotherhood" only if at a boundary
        # "brotherhood" = b-r-o-t-h-e-r-h-o-o-d, no boundary after "brother" → no match
        self.assertIsNone(inv.map_hint_keyword("brotherhood with"))

    # --- Emotional: mourning/grief ---
    def test_grief_mourning(self):
        self.assertEqual(inv.map_hint_keyword("grief for"), "MOURNS")
        self.assertEqual(inv.map_hint_keyword("grieving for"), "MOURNS")
        self.assertEqual(inv.map_hint_keyword("misses"), "MOURNS")
        self.assertEqual(inv.map_hint_keyword("misses/mourns"), "MOURNS")
        self.assertEqual(inv.map_hint_keyword("longs for"), "MOURNS")
        self.assertEqual(inv.map_hint_keyword("longs for / loves"), "MOURNS")  # first match wins

    def test_miss_word_boundary(self):
        """'dismiss' must not match the misses/missing rule."""
        self.assertIsNone(inv.map_hint_keyword("dismisses"))

    # --- Emotional: LOVER_OF before LOVES ---
    def test_lover_before_loves(self):
        """'former lover of' should map to LOVER_OF, not LOVES."""
        self.assertEqual(inv.map_hint_keyword("former lover of"), "LOVER_OF")
        self.assertEqual(inv.map_hint_keyword("secret lover of"), "LOVER_OF")

    def test_love_loved(self):
        self.assertEqual(inv.map_hint_keyword("loved"), "LOVES")
        self.assertEqual(inv.map_hint_keyword("loved (past)"), "LOVES")
        self.assertEqual(inv.map_hint_keyword("fond of"), "LOVES")
        self.assertEqual(inv.map_hint_keyword("affectionate toward"), "LOVES")

    # --- Emotional: FEARS ---
    def test_fears(self):
        self.assertEqual(inv.map_hint_keyword("fearful of"), "FEARS")
        self.assertEqual(inv.map_hint_keyword("fear of"), "FEARS")

    def test_excl_feared_by(self):
        """'feared by' is the wrong direction — must not map to FEARS."""
        self.assertIsNone(inv.map_hint_keyword("feared by"))
        self.assertIsNone(inv.map_hint_keyword("feared by grey wind"))

    # --- Emotional: HATES ---
    def test_hates(self):
        self.assertEqual(inv.map_hint_keyword("despises"), "HATES")
        self.assertEqual(inv.map_hint_keyword("disdains"), "HATES")
        self.assertEqual(inv.map_hint_keyword("disdain for"), "HATES")

    # --- Emotional: RESENTS ---
    def test_resents(self):
        self.assertEqual(inv.map_hint_keyword("bitter toward"), "RESENTS")
        self.assertEqual(inv.map_hint_keyword("resentful toward"), "RESENTS")
        self.assertEqual(inv.map_hint_keyword("bitter resentment"), "RESENTS")

    # --- Emotional: DISTRUSTS ---
    def test_distrusts(self):
        self.assertEqual(inv.map_hint_keyword("mistrusts"), "DISTRUSTS")
        self.assertEqual(inv.map_hint_keyword("deep mistrust of"), "DISTRUSTS")

    # --- Emotional: RESPECTS ---
    def test_respects(self):
        self.assertEqual(inv.map_hint_keyword("admires"), "RESPECTS")
        self.assertEqual(inv.map_hint_keyword("grudging respect for"), "RESPECTS")
        self.assertEqual(inv.map_hint_keyword("recalls with respect"), "RESPECTS")

    def test_excl_disrespects(self):
        """'disrespects' must NOT map to RESPECTS."""
        self.assertIsNone(inv.map_hint_keyword("disrespects"))
        self.assertIsNone(inv.map_hint_keyword("disrespectful toward"))

    # --- Emotional: COMPANION_OF ---
    def test_companion(self):
        self.assertEqual(inv.map_hint_keyword("childhood companion of"), "COMPANION_OF")
        self.assertEqual(inv.map_hint_keyword("friendly with"), "COMPANION_OF")
        self.assertEqual(inv.map_hint_keyword("friendship"), "COMPANION_OF")
        self.assertEqual(inv.map_hint_keyword("camaraderie"), "COMPANION_OF")

    # --- Knowledge: TUTORS ---
    def test_tutors(self):
        self.assertEqual(inv.map_hint_keyword("mentors"), "TUTORS")
        self.assertEqual(inv.map_hint_keyword("mentor figure to"), "TUTORS")

    # --- Political: COMMANDS ---
    def test_commands(self):
        self.assertEqual(inv.map_hint_keyword("commander"), "COMMANDS")
        self.assertEqual(inv.map_hint_keyword("commander of"), "COMMANDS")

    # --- Political: SERVES ---
    def test_serves(self):
        self.assertEqual(inv.map_hint_keyword("obeys"), "SERVES")
        self.assertEqual(inv.map_hint_keyword("subordinate to"), "SERVES")
        self.assertEqual(inv.map_hint_keyword("loyal subordinate to"), "SERVES")

    # --- Political: ADVISES ---
    def test_advises(self):
        self.assertEqual(inv.map_hint_keyword("warns"), "ADVISES")
        self.assertEqual(inv.map_hint_keyword("warns/advises"), "ADVISES")
        self.assertEqual(inv.map_hint_keyword("relies on counsel of"), "ADVISES")

    # --- Political: ALLIES_WITH ---
    def test_allies_with(self):
        self.assertEqual(inv.map_hint_keyword("uneasy alliance"), "ALLIES_WITH")
        self.assertEqual(inv.map_hint_keyword("secretly allied with"), "ALLIES_WITH")
        self.assertEqual(inv.map_hint_keyword("reluctant political ally"), "ALLIES_WITH")
        # "ally" substring without word boundary must NOT match words like "physically"
        self.assertNotEqual(inv.map_hint_keyword("physically abuses"), "ALLIES_WITH")

    # --- Political: CONSPIRES_WITH ---
    def test_conspires(self):
        self.assertEqual(inv.map_hint_keyword("conspired with"), "CONSPIRES_WITH")
        self.assertEqual(inv.map_hint_keyword("co-conspirator with"), "CONSPIRES_WITH")

    # --- Military: KILLS ---
    def test_kills(self):
        self.assertEqual(inv.map_hint_keyword("murdered"), "KILLS")
        self.assertEqual(inv.map_hint_keyword("murderer of"), "KILLS")
        self.assertEqual(inv.map_hint_keyword("murders"), "KILLS")

    def test_excl_murderous(self):
        """'murderous intent' should NOT map to KILLS (no act yet)."""
        self.assertIsNone(inv.map_hint_keyword("murderous intent toward"))
        self.assertIsNone(inv.map_hint_keyword("murderous hatred toward"))

    def test_excl_accuses_of_murder(self):
        """'accuses of murder' is not the killer — must stay in LLM tail."""
        self.assertIsNone(inv.map_hint_keyword("accuses of murder"))

    # --- Military: CAPTURES ---
    def test_captures(self):
        self.assertEqual(inv.map_hint_keyword("captor of"), "CAPTURES")

    # --- Military: PRISONER_OF ---
    def test_prisoner(self):
        self.assertEqual(inv.map_hint_keyword("holds captive"), "PRISONER_OF")
        self.assertEqual(inv.map_hint_keyword("holds hostage"), "PRISONER_OF")

    # --- Political: IMPRISONS ---
    def test_imprisons(self):
        self.assertEqual(inv.map_hint_keyword("imprisons"), "IMPRISONS")
        self.assertEqual(inv.map_hint_keyword("imprisoned"), "IMPRISONS")

    # --- Magic: WARGS_INTO ---
    def test_wargs(self):
        self.assertEqual(inv.map_hint_keyword("warg bond with"), "WARGS_INTO")
        self.assertEqual(inv.map_hint_keyword("warging bond with"), "WARGS_INTO")
        self.assertEqual(inv.map_hint_keyword("warges into (first time)"), "WARGS_INTO")

    # --- Magic: BONDED_TO ---
    def test_bonded(self):
        self.assertEqual(inv.map_hint_keyword("bonded with"), "BONDED_TO")
        # "warg-bonded to" contains "warg" so it hits WARGS_INTO first (correct:
        # a warg bond is an active warg relationship, not a generic bond).
        self.assertEqual(inv.map_hint_keyword("warg-bonded to"), "WARGS_INTO")
        # Pure "bonded" without "warg" → BONDED_TO
        self.assertEqual(inv.map_hint_keyword("spiritually bonded with"), "BONDED_TO")

    def test_bond_with_not_mapped(self):
        """'bond with' alone (no 'bonded') is too ambiguous — LLM tail."""
        self.assertIsNone(inv.map_hint_keyword("bond with"))

    # --- None for unrecognized phrases ---
    def test_genuinely_ambiguous_phrases(self):
        self.assertIsNone(inv.map_hint_keyword("complicated feelings toward"))
        self.assertIsNone(inv.map_hint_keyword("longing for"))
        self.assertIsNone(inv.map_hint_keyword("relies on"))
        self.assertIsNone(inv.map_hint_keyword("remembers fondly"))
        self.assertIsNone(inv.map_hint_keyword("supports"))
        self.assertIsNone(inv.map_hint_keyword("pities"))


class TestMapHintToEdge(unittest.TestCase):
    """Combined map_hint_to_edge covers layers 1, 2, and 3 in order."""

    def test_exact_match_still_works(self):
        """Layer 1 (exact) still fires for its phrases."""
        self.assertEqual(inv.map_hint_to_edge("mourning"), "MOURNS")
        self.assertEqual(inv.map_hint_to_edge("deep love and longing for"), "LOVES")
        self.assertEqual(inv.map_hint_to_edge("antagonized by"), "OPPOSES")

    def test_prefix_match_still_works(self):
        """Layer 2 (prefix) still fires for its phrases."""
        self.assertEqual(inv.map_hint_to_edge("kills (self-described)"), "KILLS")
        self.assertEqual(inv.map_hint_to_edge("brother of (paternal)"), "SIBLING_OF")
        self.assertEqual(inv.map_hint_to_edge("father of (adoptive)"), "PARENT_OF")

    def test_keyword_layer_picks_up_residue(self):
        """Layer 3 (keyword) handles phrases that escaped layers 1+2."""
        self.assertEqual(inv.map_hint_to_edge("grief for"), "MOURNS")
        self.assertEqual(inv.map_hint_to_edge("misses"), "MOURNS")
        self.assertEqual(inv.map_hint_to_edge("former lover of"), "LOVER_OF")
        self.assertEqual(inv.map_hint_to_edge("grudging respect for"), "RESPECTS")
        self.assertEqual(inv.map_hint_to_edge("warg bond with"), "WARGS_INTO")
        self.assertEqual(inv.map_hint_to_edge("bonded with"), "BONDED_TO")
        self.assertEqual(inv.map_hint_to_edge("commander"), "COMMANDS")
        self.assertEqual(inv.map_hint_to_edge("uneasy alliance"), "ALLIES_WITH")
        self.assertEqual(inv.map_hint_to_edge("murdered"), "KILLS")
        self.assertEqual(inv.map_hint_to_edge("cousin to"), "COUSIN_OF")
        self.assertEqual(inv.map_hint_to_edge("brother to"), "SIBLING_OF")
        self.assertEqual(inv.map_hint_to_edge("brother-in-law of"), "IN_LAW_OF")

    def test_exclusions_propagate_to_none(self):
        """Exclusion rules in layer 3 must cause map_hint_to_edge to return None."""
        self.assertIsNone(inv.map_hint_to_edge("feared by"))
        self.assertIsNone(inv.map_hint_to_edge("disrespects"))
        self.assertIsNone(inv.map_hint_to_edge("murderous intent toward"))
        self.assertIsNone(inv.map_hint_to_edge("accuses of murder"))

    def test_genuinely_unmapped(self):
        """Phrases that no layer should touch."""
        self.assertIsNone(inv.map_hint_to_edge("complicated feelings toward"))
        self.assertIsNone(inv.map_hint_to_edge("longing for"))
        self.assertIsNone(inv.map_hint_to_edge("connected to unnamed messenger regarding"))
        self.assertIsNone(inv.map_hint_to_edge("antagonized by, then dominates"))


class TestEdgeCaseRows(unittest.TestCase):
    """Parser should handle edge cases gracefully."""

    def test_missing_evidence_column(self):
        """Row with only 3 columns should still parse."""
        section = (
            "| Character A | Relationship | Character B | Evidence |\n"
            "|-------------|-------------|-------------|----------|\n"
            "| Jon | Loves | Ygritte |\n"
        )
        rows, warnings = inv.parse_relationships_from_section(section, "test", "agot")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["source"], "Jon")
        self.assertEqual(rows[0]["hint_original"], "Loves")

    def test_extra_whitespace_in_cells(self):
        section = (
            "| Character A | Relationship | Character B | Evidence |\n"
            "|-------------|-------------|-------------|----------|\n"
            "|  Arya  |  Mourning  |  Eddard  |  text  |\n"
        )
        rows, _ = inv.parse_relationships_from_section(section, "test", "agot")
        self.assertEqual(rows[0]["source"], "Arya")
        self.assertEqual(rows[0]["hint_original"], "Mourning")
        self.assertEqual(rows[0]["hint_norm"], "mourning")

    def test_empty_section(self):
        """Section with only header/separator should produce no rows."""
        section = (
            "| Character A | Relationship | Character B | Evidence |\n"
            "|-------------|-------------|-------------|----------|\n"
        )
        rows, warnings = inv.parse_relationships_from_section(section, "test", "agot")
        self.assertEqual(rows, [])
        self.assertEqual(warnings, [])

    def test_no_section_returns_none(self):
        text = "## Some Other Section\nstuff\n## Raw Entity List\nmore stuff"
        result = inv.extract_relationships_section(text)
        self.assertIsNone(result)

    def test_section_extraction(self):
        text = (
            "## Relationships Observed\n"
            "| A | B | C | D |\n"
            "|---|---|---|---|\n"
            "| X | Y | Z | W |\n"
            "\n"
            "## Next Section\n"
            "stuff\n"
        )
        section = inv.extract_relationships_section(text)
        self.assertIsNotNone(section)
        self.assertIn("X | Y | Z", section)
        self.assertNotIn("Next Section", section)


if __name__ == "__main__":
    unittest.main()
