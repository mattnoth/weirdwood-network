"""Tests for stage4-pass1-extra-tables.py extra table parsers.

Covers:
- parse_hospitality_table:
    * multi-guest split from Guest(s) cell
    * qualifier normalization (each enum value + unknown fallback)
    * None / empty table → returns []
    * VIOLATES_GUEST_RIGHT detection (Red Wedding style)
    * guest_right_invoked row detection
- parse_dialogue_table:
    * speaker / listener extraction
    * group-listener skip via _looks_like_group
    * empty/None table → returns []
- normalize_hospitality_qualifier:
    * each mapped variant
    * unknown fallback
- split_guests:
    * comma-separated
    * "and"-separated
    * mixed with parentheticals
- parse_food_table / parse_info_table / parse_events_section:
    * return non-empty lists on real fixture snippets

Run: python3 -m unittest tests.test_stage4_extra_tables -v
"""

import unittest
from pathlib import Path

from tests._helpers import load_script

extra_mod = load_script("stage4-pass1-extra-tables.py")

parse_hospitality_table = extra_mod.parse_hospitality_table
parse_dialogue_table = extra_mod.parse_dialogue_table
parse_food_table = extra_mod.parse_food_table
parse_events_section = extra_mod.parse_events_section
parse_info_table = extra_mod.parse_info_table
normalize_hospitality_qualifier = extra_mod.normalize_hospitality_qualifier
split_guests = extra_mod.split_guests
_looks_like_group = extra_mod._looks_like_group
_is_violation_row = extra_mod._is_violation_row
_is_guest_right_invoked = extra_mod._is_guest_right_invoked
count_food_multi_named = extra_mod.count_food_multi_named


# ---------------------------------------------------------------------------
# Fixture snippets
# ---------------------------------------------------------------------------

_HOSP_FIXTURE_SINGLE_GUEST = """\
## Hospitality & Guest Right
| Event | Type | Host | Guest(s) | Details |
|-------|------|------|----------|---------|
| Royal visit planned | feast_given | Eddard Stark | King Robert | Ned plans a feast |

## Events & Actions
1. Something.
"""

_HOSP_FIXTURE_MULTI_GUEST = """\
## Hospitality & Guest Right
| Event | Type | Host | Guest(s) | Details |
|-------|------|------|----------|---------|
| Feast at Winterfell | feast_given | Ned Stark | Catelyn, Robb, Arya | Great hall feast |

## Raw Entity List
"""

_HOSP_FIXTURE_AND_SEPARATOR = """\
## Hospitality & Guest Right
| Event | Type | Host | Guest(s) | Details |
|-------|------|------|----------|---------|
| Small supper | shelter_offered | Hodor | Bran and Rickon | Quiet meal |

## Events
"""

_HOSP_FIXTURE_NONE = """\
## Hospitality & Guest Right
| Event | Type | Host | Guest(s) | Details |
|-------|------|------|----------|---------|
None explicitly invoked in this chapter.

## Events & Actions
1. Something happened.
"""

_HOSP_FIXTURE_NONE_NO_TABLE = """\
## Hospitality & Guest Right
None explicitly invoked in this chapter.

## Events & Actions
1. Something happened.
"""

_HOSP_FIXTURE_VIOLATION = """\
## Hospitality & Guest Right
| Event | Type | Host | Guest(s) | Details |
|-------|------|------|----------|---------|
| Wedding feast massacre | hospitality_violated | Walder Frey | Robb Stark, Catelyn | Musicians fire crossbows |

## Events & Actions
"""

_HOSP_FIXTURE_REFUSAL = """\
## Hospitality & Guest Right
| Event | Type | Host | Guest(s) | Details |
|-------|------|------|----------|---------|
| Gates closed | shelter_denied | Cersei Lannister | Refugees | The queen refused entry |

## Events & Actions
"""

_HOSP_FIXTURE_GUEST_RIGHT_INVOKED = """\
## Hospitality & Guest Right
| Event | Type | Host | Guest(s) | Details |
|-------|------|------|----------|---------|
| Catelyn appeals to guest right | guest_right_invoked | Catelyn | Herself, Robb | She invokes the sacred compact |

## Events & Actions
"""

_HOSP_FIXTURE_BREAD_SALT = """\
## Hospitality & Guest Right
| Event | Type | Host | Guest(s) | Details |
|-------|------|------|----------|---------|
| Sacred compact invoked | bread_and_salt | Lord Manderly | Davos | Bread and salt exchanged formally |

## Events & Actions
"""

_HOSP_FIXTURE_SAFE_CONDUCT = """\
## Hospitality & Guest Right
| Event | Type | Host | Guest(s) | Details |
|-------|------|------|----------|---------|
| Envoy passage | safe_conduct | Stannis | Renly's envoy | Safe passage promised |

## Events & Actions
"""

_HOSP_FIXTURE_GIFT_EXCHANGE = """\
## Hospitality & Guest Right
| Event | Type | Host | Guest(s) | Details |
|-------|------|------|----------|---------|
| Gift ceremony | gift_exchange | Daenerys | Jorah Mormont | Khalasar gifts given |

## Events & Actions
"""

_HOSP_FIXTURE_PARENTHETICAL_GUESTS = """\
## Hospitality & Guest Right
| Event | Type | Host | Guest(s) | Details |
|-------|------|------|----------|---------|
| Great feast | feast_given | Jon Snow | Sam, Grenn (and their companions) | Wall feast |

## Events & Actions
"""

_DIALOGUE_FIXTURE = """\
## Dialogue of Note
| Speaker | Listener | Quote/Paraphrase | Context |
|---------|----------|------------------|---------|
| Yoren | Arya | "Hold still, boy." | Cutting her hair |
| Arya | Yoren | "Joffrey. Someone should kill him!" | After hearing about Ned |
| The Bull | Arya | "Behind you." | Warning during fight |

## POV Character's Internal State
"""

_DIALOGUE_FIXTURE_GROUP_LISTENER = """\
## Dialogue of Note
| Speaker | Listener | Quote/Paraphrase | Context |
|---------|----------|------------------|---------|
| Yoren | Recruits | "The Watch needs good men, but you lot will have to do." | Setting out |
| Yoren | Arya | "Lord Eddard's to take the black." | Private warning |
| Commander | the men | "Hold the line!" | Battle order |

## POV Character's Internal State
"""

_DIALOGUE_FIXTURE_NONE = """\
## Dialogue of Note
| Speaker | Listener | Quote/Paraphrase | Context |
|---------|----------|------------------|---------|

## POV Character's Internal State
"""

_FOOD_FIXTURE = """\
## Food & Drink
| Meal/Occasion | Food Items Described | Drink | Who Is Eating/Drinking | Where | Notes |
|--------------|---------------------|-------|----------------------|-------|-------|
| Morning meal | Bread, butter | Ale | Arya, Jon Snow | Great Hall | Simple fare |
| Feast | Roast boar, lemons | Wine | Catelyn Stark alone | Solar | Lavish |

## Hospitality
"""

_EVENTS_FIXTURE = """\
## Events & Actions
1. **First event** — Something happened here.
2. **Second event** — Another thing occurred.
3. **Third event** — A third occurrence.

## Spatial Layout
"""

_INFO_FIXTURE = """\
## Information Revealed
| Information | How Revealed | Known To (Characters) | Known To (Reader Only?) |
|-------------|-------------|----------------------|------------------------|
| Arya is disguised | Narration | Yoren | No |
| Needle is castle-forged | Arya's thoughts | Arya | Yes |

## Raw Entity List
"""


# ---------------------------------------------------------------------------
# Tests: parse_hospitality_table
# ---------------------------------------------------------------------------

class TestParseHospitalityTable(unittest.TestCase):
    """parse_hospitality_table must extract rows from ## Hospitality & Guest Right."""

    def test_single_guest_extracted(self):
        rows = parse_hospitality_table(_HOSP_FIXTURE_SINGLE_GUEST)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["host"], "Eddard Stark")
        self.assertEqual(rows[0]["guests_raw"], "King Robert")
        self.assertEqual(rows[0]["type_raw"], "feast_given")

    def test_multi_guest_row_raw_field(self):
        """The guests_raw field must contain the full cell value (split happens via split_guests)."""
        rows = parse_hospitality_table(_HOSP_FIXTURE_MULTI_GUEST)
        self.assertEqual(len(rows), 1)
        self.assertIn("Catelyn", rows[0]["guests_raw"])
        self.assertIn("Robb", rows[0]["guests_raw"])
        self.assertIn("Arya", rows[0]["guests_raw"])

    def test_and_separator_in_guests(self):
        rows = parse_hospitality_table(_HOSP_FIXTURE_AND_SEPARATOR)
        self.assertEqual(len(rows), 1)
        self.assertIn("Bran", rows[0]["guests_raw"])
        self.assertIn("Rickon", rows[0]["guests_raw"])

    def test_none_prose_returns_empty(self):
        """'None explicitly invoked...' prose line → no data rows."""
        rows = parse_hospitality_table(_HOSP_FIXTURE_NONE)
        self.assertEqual(rows, [])

    def test_none_no_table_returns_empty(self):
        """Section with no table rows at all → empty list."""
        rows = parse_hospitality_table(_HOSP_FIXTURE_NONE_NO_TABLE)
        self.assertEqual(rows, [])

    def test_violation_row_detected(self):
        rows = parse_hospitality_table(_HOSP_FIXTURE_VIOLATION)
        self.assertEqual(len(rows), 1)
        self.assertTrue(_is_violation_row(rows[0]["event"], rows[0]["type_raw"], rows[0]["details"]))

    def test_refusal_row_parsed(self):
        rows = parse_hospitality_table(_HOSP_FIXTURE_REFUSAL)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["type_raw"], "shelter_denied")

    def test_guest_right_invoked_detected(self):
        rows = parse_hospitality_table(_HOSP_FIXTURE_GUEST_RIGHT_INVOKED)
        self.assertEqual(len(rows), 1)
        self.assertTrue(_is_guest_right_invoked(rows[0]["type_raw"]))

    def test_no_section_returns_empty(self):
        text = "## Other Section\nSome content.\n"
        self.assertEqual(parse_hospitality_table(text), [])

    def test_details_field_populated(self):
        rows = parse_hospitality_table(_HOSP_FIXTURE_SINGLE_GUEST)
        self.assertEqual(rows[0]["details"], "Ned plans a feast")


# ---------------------------------------------------------------------------
# Tests: split_guests
# ---------------------------------------------------------------------------

class TestSplitGuests(unittest.TestCase):
    """split_guests must split Guest(s) cell into individual name strings."""

    def test_comma_separated(self):
        result = split_guests("Robb Stark, Catelyn, Edmure")
        self.assertEqual(len(result), 3)
        self.assertIn("Robb Stark", result)
        self.assertIn("Catelyn", result)
        self.assertIn("Edmure", result)

    def test_and_separated(self):
        result = split_guests("Bran and Rickon")
        self.assertEqual(len(result), 2)
        self.assertIn("Bran", result)
        self.assertIn("Rickon", result)

    def test_single_guest(self):
        result = split_guests("King Robert")
        self.assertEqual(result, ["King Robert"])

    def test_parenthetical_stripped(self):
        result = split_guests("Sam, Grenn (and their companions)")
        # Parenthetical removed from Grenn; Sam is clean
        self.assertIn("Sam", result)
        grenn_result = [r for r in result if "Grenn" in r]
        self.assertTrue(grenn_result)
        # Parenthetical must be stripped from Grenn entry
        self.assertNotIn("(", grenn_result[0])

    def test_empty_string(self):
        result = split_guests("")
        self.assertEqual(result, [])

    def test_semicolon_separator(self):
        result = split_guests("Jon Snow; Samwell Tarly")
        self.assertEqual(len(result), 2)
        self.assertIn("Jon Snow", result)
        self.assertIn("Samwell Tarly", result)

    def test_mixed_separators(self):
        result = split_guests("Arya, Sansa and Bran")
        self.assertEqual(len(result), 3)

    def test_none_value_skipped(self):
        """'None' in the guest cell should not produce a guest entry."""
        result = split_guests("None")
        self.assertEqual(result, [])


# ---------------------------------------------------------------------------
# Tests: normalize_hospitality_qualifier
# ---------------------------------------------------------------------------

class TestNormalizeHospitalityQualifier(unittest.TestCase):
    """normalize_hospitality_qualifier must map Type column values to the enum."""

    def test_shelter_offered(self):
        self.assertEqual(normalize_hospitality_qualifier("shelter_offered"), "shelter")

    def test_shelter_partial(self):
        self.assertEqual(normalize_hospitality_qualifier("shelter_offered (conditional)"), "shelter")

    def test_feast_given(self):
        self.assertEqual(normalize_hospitality_qualifier("feast_given"), "feast")

    def test_feast_planned(self):
        self.assertEqual(normalize_hospitality_qualifier("feast_given (planned)"), "feast")

    def test_bread_and_salt(self):
        self.assertEqual(normalize_hospitality_qualifier("bread_and_salt"), "bread_and_salt")

    def test_bread_salt_with_space(self):
        self.assertEqual(normalize_hospitality_qualifier("bread and salt"), "bread_and_salt")

    def test_safe_conduct(self):
        self.assertEqual(normalize_hospitality_qualifier("safe_conduct"), "safe_conduct")

    def test_safe_conduct_with_space(self):
        self.assertEqual(normalize_hospitality_qualifier("safe conduct"), "safe_conduct")

    def test_gift_exchange(self):
        self.assertEqual(normalize_hospitality_qualifier("gift_exchange"), "gift_exchange")

    def test_gift_exchange_with_space(self):
        self.assertEqual(normalize_hospitality_qualifier("gift exchange"), "gift_exchange")

    def test_refusal_to_host(self):
        self.assertEqual(normalize_hospitality_qualifier("refusal_to_host"), "refused")

    def test_shelter_denied(self):
        self.assertEqual(normalize_hospitality_qualifier("shelter_denied"), "refused")

    def test_denied_variant(self):
        self.assertEqual(normalize_hospitality_qualifier("denied entry"), "refused")

    def test_unknown_fallback(self):
        self.assertEqual(normalize_hospitality_qualifier("hospitality_given"), "unknown")

    def test_empty_string(self):
        self.assertEqual(normalize_hospitality_qualifier(""), "unknown")

    def test_dash_fallback(self):
        self.assertEqual(normalize_hospitality_qualifier("—"), "unknown")

    def test_custom_fallback(self):
        self.assertEqual(normalize_hospitality_qualifier("custom"), "unknown")


# ---------------------------------------------------------------------------
# Tests: violation detection
# ---------------------------------------------------------------------------

class TestViolationDetection(unittest.TestCase):
    """_is_violation_row must detect Red Wedding style violations."""

    def test_hospitality_violated_type(self):
        self.assertTrue(_is_violation_row("", "hospitality_violated", ""))

    def test_red_wedding_event_name(self):
        self.assertTrue(_is_violation_row("The Red Wedding massacre", "", ""))

    def test_massacre_in_event(self):
        self.assertTrue(_is_violation_row("Wedding feast massacre", "", ""))

    def test_violation_in_details(self):
        self.assertTrue(_is_violation_row("", "", "musicians fired crossbows — violation of guest right"))

    def test_shelter_offered_not_violation(self):
        self.assertFalse(_is_violation_row("Shelter at castle", "shelter_offered", "Normal hosting"))

    def test_feast_not_violation(self):
        self.assertFalse(_is_violation_row("Feast given", "feast_given", "Great meal"))

    def test_guest_right_invoked_detection(self):
        self.assertTrue(_is_guest_right_invoked("guest_right_invoked"))
        self.assertTrue(_is_guest_right_invoked("guest_right_invoked (negatively)"))
        self.assertFalse(_is_guest_right_invoked("shelter_offered"))
        self.assertFalse(_is_guest_right_invoked("hospitality_violated"))


# ---------------------------------------------------------------------------
# Tests: parse_dialogue_table
# ---------------------------------------------------------------------------

class TestParseDialogueTable(unittest.TestCase):
    """parse_dialogue_table must extract speaker/listener pairs."""

    def test_rows_extracted(self):
        rows = parse_dialogue_table(_DIALOGUE_FIXTURE)
        self.assertEqual(len(rows), 3)

    def test_speaker_listener(self):
        rows = parse_dialogue_table(_DIALOGUE_FIXTURE)
        self.assertEqual(rows[0]["speaker"], "Yoren")
        self.assertEqual(rows[0]["listener"], "Arya")

    def test_quote_field(self):
        rows = parse_dialogue_table(_DIALOGUE_FIXTURE)
        self.assertIn("Hold still", rows[0]["quote"])

    def test_context_field(self):
        rows = parse_dialogue_table(_DIALOGUE_FIXTURE)
        self.assertEqual(rows[0]["context"], "Cutting her hair")

    def test_no_section_returns_empty(self):
        text = "## Other Section\nSome text.\n"
        self.assertEqual(parse_dialogue_table(text), [])

    def test_empty_table_returns_empty(self):
        rows = parse_dialogue_table(_DIALOGUE_FIXTURE_NONE)
        self.assertEqual(rows, [])


# ---------------------------------------------------------------------------
# Tests: group-listener detection
# ---------------------------------------------------------------------------

class TestGroupListenerDetection(unittest.TestCase):
    """_looks_like_group must identify obvious group listeners."""

    def test_recruits_is_group(self):
        self.assertTrue(_looks_like_group("Recruits"))

    def test_the_recruits_is_group(self):
        self.assertTrue(_looks_like_group("the recruits"))

    def test_the_men_is_group(self):
        self.assertTrue(_looks_like_group("the men"))

    def test_the_boys_is_group(self):
        self.assertTrue(_looks_like_group("the boys"))

    def test_all_is_group(self):
        self.assertTrue(_looks_like_group("all"))

    def test_everyone_is_group(self):
        self.assertTrue(_looks_like_group("everyone"))

    def test_council_is_group(self):
        self.assertTrue(_looks_like_group("Council"))

    def test_arya_is_not_group(self):
        self.assertFalse(_looks_like_group("Arya"))

    def test_jon_snow_is_not_group(self):
        self.assertFalse(_looks_like_group("Jon Snow"))

    def test_yoren_is_not_group(self):
        self.assertFalse(_looks_like_group("Yoren"))

    def test_group_dialogue_rows_skipped_via_parser_filter(self):
        """Rows with group listeners in _DIALOGUE_FIXTURE_GROUP_LISTENER are caught."""
        # Yoren→Recruits should be a group listener; Yoren→Arya should not
        group_rows = [
            r for r in parse_dialogue_table(_DIALOGUE_FIXTURE_GROUP_LISTENER)
            if _looks_like_group(r["listener"])
        ]
        non_group_rows = [
            r for r in parse_dialogue_table(_DIALOGUE_FIXTURE_GROUP_LISTENER)
            if not _looks_like_group(r["listener"])
        ]
        # "Recruits" and "the men" are groups; "Arya" is not
        self.assertGreater(len(group_rows), 0)
        # Yoren→Arya should be in non-group rows
        arya_row = next((r for r in non_group_rows if r["listener"] == "Arya"), None)
        self.assertIsNotNone(arya_row)


# ---------------------------------------------------------------------------
# Tests: parse_food_table
# ---------------------------------------------------------------------------

class TestParseFoodTable(unittest.TestCase):
    """parse_food_table must extract rows from ## Food & Drink."""

    def test_rows_extracted(self):
        rows = parse_food_table(_FOOD_FIXTURE)
        self.assertEqual(len(rows), 2)

    def test_row_is_dict(self):
        rows = parse_food_table(_FOOD_FIXTURE)
        self.assertIsInstance(rows[0], dict)

    def test_no_section_returns_empty(self):
        text = "## Other\nstuff\n"
        self.assertEqual(parse_food_table(text), [])

    def test_count_food_multi_named_two_people(self):
        """Row with 'Arya, Jon Snow' counts as multi-named."""
        rows = parse_food_table(_FOOD_FIXTURE)
        count = count_food_multi_named(rows)
        # First row has 'Arya, Jon Snow' = 2 named → should count
        self.assertGreaterEqual(count, 1)

    def test_count_food_single_named(self):
        """Row with only one named person doesn't count."""
        single = """\
## Food & Drink
| Meal/Occasion | Food Items Described | Drink | Who Is Eating/Drinking | Where | Notes |
|--------------|---------------------|-------|----------------------|-------|-------|
| Meal | Bread | Water | Catelyn alone | Solar | |

## Next Section
"""
        rows = parse_food_table(single)
        count = count_food_multi_named(rows)
        self.assertEqual(count, 0)


# ---------------------------------------------------------------------------
# Tests: parse_events_section
# ---------------------------------------------------------------------------

class TestParseEventsSection(unittest.TestCase):
    """parse_events_section must extract numbered items."""

    def test_items_extracted(self):
        items = parse_events_section(_EVENTS_FIXTURE)
        self.assertEqual(len(items), 3)

    def test_items_are_strings(self):
        items = parse_events_section(_EVENTS_FIXTURE)
        for item in items:
            self.assertIsInstance(item, str)
            self.assertRegex(item, r"^\d+\.")

    def test_no_section_returns_empty(self):
        text = "## Other Section\nsome text\n"
        self.assertEqual(parse_events_section(text), [])

    def test_item_content(self):
        items = parse_events_section(_EVENTS_FIXTURE)
        self.assertIn("First event", items[0])


# ---------------------------------------------------------------------------
# Tests: parse_info_table
# ---------------------------------------------------------------------------

class TestParseInfoTable(unittest.TestCase):
    """parse_info_table must extract rows from ## Information Revealed."""

    def test_rows_extracted(self):
        rows = parse_info_table(_INFO_FIXTURE)
        self.assertEqual(len(rows), 2)

    def test_row_is_dict(self):
        rows = parse_info_table(_INFO_FIXTURE)
        self.assertIsInstance(rows[0], dict)

    def test_no_section_returns_empty(self):
        text = "## Other\nstuff\n"
        self.assertEqual(parse_info_table(text), [])

    def test_how_revealed_field_present(self):
        rows = parse_info_table(_INFO_FIXTURE)
        # At least one row should have a 'how revealed' column
        all_keys = set()
        for r in rows:
            all_keys.update(r.keys())
        how_keys = [k for k in all_keys if "how" in k]
        self.assertTrue(how_keys, f"Expected a 'how revealed' column, got keys: {all_keys}")


# ---------------------------------------------------------------------------
# Integration: real extraction file
# ---------------------------------------------------------------------------

class TestRealExtractionFile(unittest.TestCase):
    """Smoke test parsers against the real acok-arya-01.extraction.md fixture."""

    _FIXTURE_PATH = (
        Path(__file__).parent.parent
        / "extractions" / "mechanical" / "acok" / "acok-arya-01.extraction.md"
    )

    def setUp(self):
        if not self._FIXTURE_PATH.exists():
            self.skipTest(f"Real extraction file not found: {self._FIXTURE_PATH}")
        self._text = self._FIXTURE_PATH.read_text(encoding="utf-8")

    def test_hospitality_none_returns_empty(self):
        """acok-arya-01 has 'None' in hospitality section — should return []."""
        rows = parse_hospitality_table(self._text)
        self.assertEqual(rows, [])

    def test_dialogue_has_rows(self):
        """acok-arya-01 has 12+ dialogue rows."""
        rows = parse_dialogue_table(self._text)
        self.assertGreater(len(rows), 5)

    def test_dialogue_yoren_arya(self):
        rows = parse_dialogue_table(self._text)
        yoren_arya = [r for r in rows if r["speaker"] == "Yoren" and r["listener"] == "Arya"]
        self.assertGreater(len(yoren_arya), 0)

    def test_food_has_rows(self):
        rows = parse_food_table(self._text)
        self.assertGreater(len(rows), 0)

    def test_events_has_items(self):
        items = parse_events_section(self._text)
        self.assertGreater(len(items), 10)

    def test_info_has_rows(self):
        rows = parse_info_table(self._text)
        self.assertGreater(len(rows), 5)


# ---------------------------------------------------------------------------
# Red Wedding integration
# ---------------------------------------------------------------------------

class TestRedWeddingViolation(unittest.TestCase):
    """asos-catelyn-07 should produce VIOLATES_GUEST_RIGHT entries."""

    _FIXTURE_PATH = (
        Path(__file__).parent.parent
        / "extractions" / "mechanical" / "asos" / "asos-catelyn-07.extraction.md"
    )

    def setUp(self):
        if not self._FIXTURE_PATH.exists():
            self.skipTest(f"Red Wedding extraction file not found: {self._FIXTURE_PATH}")
        self._text = self._FIXTURE_PATH.read_text(encoding="utf-8")

    def test_hospitality_rows_present(self):
        rows = parse_hospitality_table(self._text)
        self.assertGreater(len(rows), 0)

    def test_violation_row_found(self):
        rows = parse_hospitality_table(self._text)
        violations = [
            r for r in rows
            if _is_violation_row(r["event"], r["type_raw"], r["details"])
        ]
        self.assertGreater(len(violations), 0, "Expected at least one violation row for the Red Wedding")

    def test_walder_frey_is_host_in_violation(self):
        rows = parse_hospitality_table(self._text)
        violations = [
            r for r in rows
            if _is_violation_row(r["event"], r["type_raw"], r["details"])
        ]
        hosts = [r["host"] for r in violations]
        walder = [h for h in hosts if "Frey" in h or "Walder" in h]
        self.assertTrue(walder, f"Expected Walder Frey as host, got hosts: {hosts}")


if __name__ == "__main__":
    unittest.main()
