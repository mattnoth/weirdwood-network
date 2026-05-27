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
- generate_events_candidates / generate_info_candidates / generate_food_candidates (Task 1):
    * emit candidate pairs when >=2 entities resolved
    * drop rows with <2 resolved entities
    * candidate_kind, edge_type==None, hint_raw populated
- locate_evidence_for_candidate (Task 2):
    * verbatim match returns evidence_ref with :LINE suffix
    * chapter-level fallback when no prose match
- _anchor_candidate_locator (Task 2):
    * adds evidence_ref + locate_status to a candidate dict
    * idempotent (does not overwrite existing evidence_ref)

Run: python3 -m unittest tests.test_stage4_extra_tables -v
"""

import unittest
from pathlib import Path

import tempfile
import json
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

# Task 1 generators
generate_events_candidates = extra_mod.generate_events_candidates
generate_info_candidates = extra_mod.generate_info_candidates
generate_food_candidates = extra_mod.generate_food_candidates

# Task 2 locator
locate_evidence_for_candidate = extra_mod.locate_evidence_for_candidate
_anchor_candidate_locator = extra_mod._anchor_candidate_locator

# ---------------------------------------------------------------------------
# Minimal resolver stubs for Task 1 generator tests
# (We don't need a real alias_map / node_set; we use a mock that resolves
# known test names.)
# ---------------------------------------------------------------------------

# Build a stub resolver environment: resolve known names to predictable slugs.
_STUB_NODE_SET = {
    "arya-stark", "jon-snow", "eddard-stark", "robb-stark",
    "catelyn-stark", "sansa-stark", "tyrion-lannister",
    "samwell-tarly", "yoren", "cersei-lannister",
}
_STUB_ALIAS_MAP = {
    "Arya": "arya-stark",
    "Jon": "jon-snow",
    "Jon Snow": "jon-snow",
    "Ned": "eddard-stark",
    "Eddard": "eddard-stark",
    "Eddard Stark": "eddard-stark",
    "Lord Stark": "eddard-stark",
    "Robb": "robb-stark",
    "Robb Stark": "robb-stark",
    "Catelyn": "catelyn-stark",
    "Catelyn Stark": "catelyn-stark",
    "Sansa": "sansa-stark",
    "Sansa Stark": "sansa-stark",
    "Tyrion": "tyrion-lannister",
    "Tyrion Lannister": "tyrion-lannister",
    "Sam": "samwell-tarly",
    "Samwell": "samwell-tarly",
    "Samwell Tarly": "samwell-tarly",
    "Yoren": "yoren",
    "Cersei": "cersei-lannister",
}
# Build a minimal firstname_index: first name → [slug]
_STUB_FIRSTNAME_INDEX = {
    "arya": ["arya-stark"],
    "jon": ["jon-snow"],
    "ned": ["eddard-stark"],
    "eddard": ["eddard-stark"],
    "robb": ["robb-stark"],
    "catelyn": ["catelyn-stark"],
    "sansa": ["sansa-stark"],
    "tyrion": ["tyrion-lannister"],
    "sam": ["samwell-tarly"],
    "samwell": ["samwell-tarly"],
    "yoren": ["yoren"],
    "cersei": ["cersei-lannister"],
}
_STUB_IMPORTANCE_PRIOR: dict = {}
_STUB_PRESENT_SLUGS: set = set(_STUB_NODE_SET)


# Shared kwargs for generator calls
def _gen_kwargs(chapter_path: Path, chapter_rel: str) -> dict:
    return dict(
        chapter_slug="agot-bran-01",
        book_abbrev="agot",
        pov_slug="bran-stark",
        extraction_rel="extractions/mechanical/agot/agot-bran-01.extraction.md",
        alias_map=_STUB_ALIAS_MAP,
        node_set=_STUB_NODE_SET,
        firstname_index=_STUB_FIRSTNAME_INDEX,
        importance_prior=_STUB_IMPORTANCE_PRIOR,
        present_slugs=_STUB_PRESENT_SLUGS,
        chapter_path=chapter_path,
        chapter_rel=chapter_rel,
        run_id="test-run",
        schema_version="pass1-extra-tables-v1",
        produced_at="2026-05-24T00:00:00+00:00",
    )


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


# ---------------------------------------------------------------------------
# Tests: generate_events_candidates (Task 1)
# ---------------------------------------------------------------------------

class TestGenerateEventsCandidates(unittest.TestCase):
    """generate_events_candidates must emit pairs when >=2 entities resolved."""

    def _make_chapter_file(self, content: str) -> tuple[Path, str]:
        """Write temp chapter file; return (path, chapter_rel)."""
        tmpdir = tempfile.mkdtemp()
        p = Path(tmpdir) / "agot-bran-01.md"
        p.write_text(content, encoding="utf-8")
        return p, f"sources/chapters/agot/agot-bran-01.md"

    def test_two_entity_item_emits_pair(self):
        """An item mentioning Arya and Jon should emit one candidate pair."""
        items = ["1. **Test** — Arya and Jon Snow spoke together in the yard."]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfrontmatter: yes\n---\nArya and Jon Snow spoke together in the yard.\n"
        )
        cands, rows_2plus, rows_dropped, rows_escalated, escals = generate_events_candidates(
            event_items=items,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        self.assertGreaterEqual(len(cands), 1)
        self.assertEqual(rows_2plus, 1)
        self.assertEqual(rows_dropped, 0)

    def test_candidate_kind_is_pass1_events(self):
        items = ["1. **Test** — Robb Stark and Catelyn Stark planned the march."]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nRobb and Catelyn planned.\n"
        )
        cands, _, _, _, _ = generate_events_candidates(
            event_items=items,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        if cands:
            self.assertEqual(cands[0]["candidate_kind"], "pass1_events")

    def test_edge_type_is_none(self):
        items = ["1. **Act** — Eddard Stark and Robb Stark rode north."]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nEddard and Robb rode north.\n"
        )
        cands, _, _, _, _ = generate_events_candidates(
            event_items=items,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        for c in cands:
            self.assertIsNone(c["edge_type"])

    def test_single_entity_item_dropped(self):
        """Item with only one resolvable entity → dropped, no candidate."""
        items = ["1. **Monologue** — Some unnamed person walked by."]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nSome unnamed person walked by.\n"
        )
        cands, rows_2plus, rows_dropped, rows_escalated, escals = generate_events_candidates(
            event_items=items,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        self.assertEqual(len(cands), 0)
        self.assertEqual(rows_2plus, 0)
        self.assertEqual(rows_dropped, 1)

    def test_hint_raw_populated(self):
        """hint_raw should contain the item text (minus number prefix)."""
        items = ["1. **Act** — Arya and Jon Snow sparred in the yard."]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya and Jon Snow sparred in the yard.\n"
        )
        cands, _, _, _, _ = generate_events_candidates(
            event_items=items,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        if cands:
            self.assertIn("Arya", cands[0]["hint_raw"])

    def test_fan_out_first_actor_only(self):
        """With 3 entities, should fan-out from first → second and first → third."""
        items = ["1. **Council** — Eddard Stark and Catelyn Stark and Robb Stark met."]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nEddard Stark and Catelyn Stark and Robb Stark met.\n"
        )
        cands, _, _, _, _ = generate_events_candidates(
            event_items=items,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        # All candidates should have same source (first resolved entity)
        if len(cands) >= 2:
            sources = {c["source_slug"] for c in cands}
            self.assertEqual(len(sources), 1, f"Expected single source, got: {sources}")

    def test_evidence_ref_present(self):
        """Candidates must carry evidence_ref field."""
        items = ["1. **Act** — Arya and Jon Snow sparred."]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya and Jon Snow sparred.\n"
        )
        cands, _, _, _, _ = generate_events_candidates(
            event_items=items,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        for c in cands:
            self.assertIn("evidence_ref", c)
            self.assertTrue(c["evidence_ref"], "evidence_ref must be non-empty")

    def test_locate_status_present(self):
        """Candidates must carry locate_status."""
        items = ["1. **Act** — Arya and Jon Snow sparred in the yard."]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya and Jon Snow sparred in the yard.\n"
        )
        cands, _, _, _, _ = generate_events_candidates(
            event_items=items,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        for c in cands:
            self.assertIn(c["locate_status"], ("verbatim", "chapter-level"))


# ---------------------------------------------------------------------------
# Tests: generate_info_candidates (Task 1)
# ---------------------------------------------------------------------------

class TestGenerateInfoCandidates(unittest.TestCase):
    """generate_info_candidates must emit pairs from Information Revealed rows."""

    def _make_chapter_file(self, content: str) -> tuple[Path, str]:
        tmpdir = tempfile.mkdtemp()
        p = Path(tmpdir) / "agot-bran-01.md"
        p.write_text(content, encoding="utf-8")
        return p, "sources/chapters/agot/agot-bran-01.md"

    def test_two_entity_row_emits_pair(self):
        info_rows = [
            {
                "information": "Arya is Eddard Stark's daughter",
                "how revealed": "Narration",
                "known to (characters)": "Jon Snow",
                "known to (reader only?)": "No",
            }
        ]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya is Lord Stark's daughter.\n"
        )
        cands, rows_2plus, rows_dropped, rows_escalated, escals = generate_info_candidates(
            info_rows=info_rows,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        self.assertGreaterEqual(len(cands), 1)
        self.assertEqual(rows_2plus, 1)

    def test_candidate_kind_is_pass1_info(self):
        info_rows = [
            {
                "information": "Sansa and Tyrion Lannister are wed",
                "how revealed": "Direct observation",
                "known to (characters)": "Catelyn Stark",
                "known to (reader only?)": "No",
            }
        ]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nSansa and Tyrion are wed.\n"
        )
        cands, _, _, _, _ = generate_info_candidates(
            info_rows=info_rows,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        if cands:
            self.assertEqual(cands[0]["candidate_kind"], "pass1_info")

    def test_edge_type_none(self):
        info_rows = [
            {"information": "Arya and Jon Snow trained", "how revealed": "Scene", "known to (characters)": "Robb Stark"}
        ]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya and Jon trained.\n"
        )
        cands, _, _, _, _ = generate_info_candidates(
            info_rows=info_rows,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        for c in cands:
            self.assertIsNone(c["edge_type"])

    def test_single_entity_dropped(self):
        info_rows = [
            {"information": "The keep is old", "how revealed": "Description", "known to (characters)": "Everyone"}
        ]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nThe keep is old.\n"
        )
        cands, rows_2plus, rows_dropped, rows_escalated, escals = generate_info_candidates(
            info_rows=info_rows,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        self.assertEqual(len(cands), 0)
        self.assertEqual(rows_2plus, 0)
        self.assertEqual(rows_dropped, 1)

    def test_evidence_ref_present(self):
        info_rows = [
            {"information": "Arya and Jon Snow trained", "how revealed": "Scene", "known to (characters)": "Robb Stark"}
        ]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya and Jon trained.\n"
        )
        cands, _, _, _, _ = generate_info_candidates(
            info_rows=info_rows,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        for c in cands:
            self.assertIn("evidence_ref", c)


# ---------------------------------------------------------------------------
# Tests: generate_food_candidates (Task 1)
# ---------------------------------------------------------------------------

class TestGenerateFoodCandidates(unittest.TestCase):
    """generate_food_candidates must emit pairs from Food & Drink rows."""

    def _make_chapter_file(self, content: str) -> tuple[Path, str]:
        tmpdir = tempfile.mkdtemp()
        p = Path(tmpdir) / "agot-bran-01.md"
        p.write_text(content, encoding="utf-8")
        return p, "sources/chapters/agot/agot-bran-01.md"

    def test_two_diners_emit_pair(self):
        food_rows = [
            {
                "meal/occasion": "Breakfast",
                "food items described": "Bread",
                "drink": "Ale",
                "who is eating/drinking": "Arya, Jon Snow",
                "where": "Great Hall",
                "preparation/presentation notes": "",
            }
        ]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya and Jon Snow ate breakfast.\n"
        )
        cands, rows_2plus, rows_dropped, rows_escalated, escals = generate_food_candidates(
            food_rows=food_rows,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        self.assertGreaterEqual(len(cands), 1)
        self.assertEqual(rows_2plus, 1)
        self.assertEqual(rows_dropped, 0)

    def test_candidate_kind_is_pass1_food(self):
        food_rows = [
            {"meal/occasion": "Feast", "who is eating/drinking": "Robb Stark and Catelyn Stark"}
        ]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nRobb and Catelyn feasted.\n"
        )
        cands, _, _, _, _ = generate_food_candidates(
            food_rows=food_rows,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        if cands:
            self.assertEqual(cands[0]["candidate_kind"], "pass1_food")

    def test_edge_type_none(self):
        food_rows = [{"meal/occasion": "Supper", "who is eating/drinking": "Arya, Sansa Stark"}]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya and Sansa ate supper.\n"
        )
        cands, _, _, _, _ = generate_food_candidates(
            food_rows=food_rows,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        for c in cands:
            self.assertIsNone(c["edge_type"])

    def test_single_entity_dropped(self):
        food_rows = [{"meal/occasion": "Snack", "who is eating/drinking": "some unnamed guard"}]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nA guard snacked.\n"
        )
        cands, rows_2plus, rows_dropped, rows_escalated, escals = generate_food_candidates(
            food_rows=food_rows,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        self.assertEqual(len(cands), 0)
        self.assertEqual(rows_dropped, 1)

    def test_evidence_ref_present(self):
        food_rows = [{"meal/occasion": "Feast", "who is eating/drinking": "Catelyn Stark, Robb Stark"}]
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nCatelyn and Robb feasted.\n"
        )
        cands, _, _, _, _ = generate_food_candidates(
            food_rows=food_rows,
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        for c in cands:
            self.assertIn("evidence_ref", c)


# ---------------------------------------------------------------------------
# Tests: locate_evidence_for_candidate + _anchor_candidate_locator (Task 2)
# ---------------------------------------------------------------------------

class TestLocateEvidence(unittest.TestCase):
    """locate_evidence_for_candidate must find verbatim lines or fall back."""

    def _make_chapter_file(self, content: str) -> Path:
        tmpdir = tempfile.mkdtemp()
        p = Path(tmpdir) / "agot-bran-01.md"
        p.write_text(content, encoding="utf-8")
        return p

    def test_verbatim_match_found(self):
        """When chapter contains both names + hint word, locate_status=verbatim."""
        chapter = (
            "---\nfrontmatter: yes\n---\n"
            "Arya and Jon Snow sparred together in the yard.\n"
        )
        chapter_path = self._make_chapter_file(chapter)
        result = locate_evidence_for_candidate(
            source_slug="arya-stark",
            target_slug="jon-snow",
            hint_text="sparred yard",
            chapter_path=chapter_path,
            chapter_rel="sources/chapters/agot/agot-bran-01.md",
        )
        self.assertEqual(result["locate_status"], "verbatim")
        self.assertIn(":", result["evidence_ref"])  # has :LINE suffix
        self.assertIn("arya", result["evidence_quote"].lower())

    def test_chapter_level_fallback_when_no_match(self):
        """When chapter prose doesn't match, locate_status=chapter-level."""
        chapter = (
            "---\nfrontmatter: yes\n---\n"
            "The sun rose over the mountains.\n"
        )
        chapter_path = self._make_chapter_file(chapter)
        result = locate_evidence_for_candidate(
            source_slug="arya-stark",
            target_slug="jon-snow",
            hint_text="completely unrelated stuff zxyzxy",
            chapter_path=chapter_path,
            chapter_rel="sources/chapters/agot/agot-bran-01.md",
        )
        self.assertEqual(result["locate_status"], "chapter-level")
        self.assertNotIn(":", result["evidence_ref"])  # no line number

    def test_missing_chapter_file_returns_chapter_level(self):
        """Missing chapter file → chapter-level fallback, no crash."""
        result = locate_evidence_for_candidate(
            source_slug="arya-stark",
            target_slug="jon-snow",
            hint_text="some hint",
            chapter_path=Path("/nonexistent/path/chapter.md"),
            chapter_rel="sources/chapters/agot/agot-bran-01.md",
        )
        self.assertEqual(result["locate_status"], "chapter-level")

    def test_evidence_ref_format(self):
        """evidence_ref must be 'chapter_rel' or 'chapter_rel:LINENO'."""
        chapter = (
            "---\nfrontmatter: yes\n---\n"
            "Arya and Jon Snow sparred together in the yard.\n"
        )
        chapter_path = self._make_chapter_file(chapter)
        result = locate_evidence_for_candidate(
            source_slug="arya-stark",
            target_slug="jon-snow",
            hint_text="sparred",
            chapter_path=chapter_path,
            chapter_rel="sources/chapters/agot/agot-bran-01.md",
        )
        ref = result["evidence_ref"]
        self.assertTrue(
            ref == "sources/chapters/agot/agot-bran-01.md" or
            ref.startswith("sources/chapters/agot/agot-bran-01.md:"),
            f"Unexpected evidence_ref format: {ref!r}",
        )


class TestAnchorCandidateLocator(unittest.TestCase):
    """_anchor_candidate_locator must attach evidence_ref + locate_status."""

    def _make_chapter_file(self, content: str) -> Path:
        tmpdir = tempfile.mkdtemp()
        p = Path(tmpdir) / "agot-bran-01.md"
        p.write_text(content, encoding="utf-8")
        return p

    def _base_cand(self) -> dict:
        return {
            "candidate_kind": "pass1_dialogue",
            "source_slug": "arya-stark",
            "target_slug": "jon-snow",
            "hint_raw": "sparred yard",
            "evidence_quote": "",
            "evidence_context": "",
        }

    def test_evidence_ref_added(self):
        chapter_path = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya and Jon Snow sparred in the yard.\n"
        )
        cand = self._base_cand()
        _anchor_candidate_locator(cand, chapter_path, "sources/chapters/agot/agot-bran-01.md")
        self.assertIn("evidence_ref", cand)
        self.assertTrue(cand["evidence_ref"])

    def test_locate_status_added(self):
        chapter_path = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya and Jon Snow sparred in the yard.\n"
        )
        cand = self._base_cand()
        _anchor_candidate_locator(cand, chapter_path, "sources/chapters/agot/agot-bran-01.md")
        self.assertIn(cand["locate_status"], ("verbatim", "chapter-level"))

    def test_idempotent_does_not_overwrite_existing(self):
        """If evidence_ref already set, _anchor_candidate_locator is a no-op."""
        chapter_path = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya and Jon sparred.\n"
        )
        cand = self._base_cand()
        cand["evidence_ref"] = "already/set.md:99"
        _anchor_candidate_locator(cand, chapter_path, "sources/chapters/agot/agot-bran-01.md")
        self.assertEqual(cand["evidence_ref"], "already/set.md:99")


# ---------------------------------------------------------------------------
# Tests: Fix 2 — is_low_quality_endpoint + _has_passive_voice
# ---------------------------------------------------------------------------

# Import the new functions
is_low_quality_endpoint = extra_mod.is_low_quality_endpoint
_has_passive_voice = extra_mod._has_passive_voice


class TestIsLowQualityEndpoint(unittest.TestCase):
    """is_low_quality_endpoint must gate bare titles, aliases, demonyms, toasts."""

    # --- Bare titles ---
    def test_bare_ser_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint("ser"))

    def test_bare_lord_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint("lord"))

    def test_bare_king_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint("king"))

    def test_bare_maester_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint("maester"))

    def test_bare_queen_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint("queen"))

    def test_bare_septon_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint("septon"))

    def test_bare_septa_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint("septa"))

    # --- Real character slugs are NOT low quality ---
    def test_eddard_stark_not_low_quality(self):
        self.assertFalse(is_low_quality_endpoint("eddard-stark"))

    def test_tyrion_lannister_not_low_quality(self):
        self.assertFalse(is_low_quality_endpoint("tyrion-lannister"))

    def test_arya_stark_not_low_quality(self):
        self.assertFalse(is_low_quality_endpoint("arya-stark"))

    def test_jon_snow_not_low_quality(self):
        self.assertFalse(is_low_quality_endpoint("jon-snow"))

    # --- Known aliases ---
    def test_alayne_is_low_quality(self):
        """alayne (Sansa alias) must route to escalation."""
        self.assertTrue(is_low_quality_endpoint("alayne"))

    def test_alayne_stone_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint("alayne-stone"))

    def test_arry_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint("arry"))

    def test_no_one_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint("no-one"))

    # --- Demonyms ---
    def test_dothraki_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint("dothraki"))

    def test_wildling_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint("wildling"))

    def test_ironborn_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint("ironborn"))

    def test_unsullied_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint("unsullied"))

    # --- Toast/phrase patterns ---
    def test_all_for_joffrey_is_low_quality(self):
        """The 'all-for-joffrey' toast pattern must be gated."""
        self.assertTrue(is_low_quality_endpoint("all-for-joffrey"))

    def test_all_for_any_name_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint("all-for-the-king"))

    # --- Empty string ---
    def test_empty_slug_is_low_quality(self):
        self.assertTrue(is_low_quality_endpoint(""))

    # --- Case insensitivity ---
    def test_case_insensitive_title(self):
        self.assertTrue(is_low_quality_endpoint("LORD"))
        self.assertTrue(is_low_quality_endpoint("Lord"))

    def test_case_insensitive_alias(self):
        self.assertTrue(is_low_quality_endpoint("ALAYNE"))


class TestHasPassiveVoice(unittest.TestCase):
    """_has_passive_voice must detect passive constructions."""

    def test_was_killed_is_passive(self):
        self.assertTrue(_has_passive_voice("Ned was killed by Ilyn Payne."))

    def test_was_told_is_passive(self):
        self.assertTrue(_has_passive_voice("Arya was told to stay inside."))

    def test_were_betrayed_is_passive(self):
        self.assertTrue(_has_passive_voice("They were betrayed at the Red Wedding."))

    def test_is_named_is_passive(self):
        self.assertTrue(_has_passive_voice("Jon is named Lord Commander."))

    def test_was_sent_is_passive(self):
        self.assertTrue(_has_passive_voice("The raven was sent to Dragonstone."))

    def test_active_voice_not_passive(self):
        self.assertFalse(_has_passive_voice("Ned killed the direwolf."))

    def test_simple_declarative_not_passive(self):
        self.assertFalse(_has_passive_voice("Arya and Jon Snow sparred in the yard."))

    def test_empty_string_not_passive(self):
        self.assertFalse(_has_passive_voice(""))

    def test_was_revealed_to_is_passive(self):
        self.assertTrue(_has_passive_voice("The secret was revealed to Sansa."))


class TestSlugGateInGenerator(unittest.TestCase):
    """Escalation routing when slug-quality or passive-voice gate triggers."""

    def _make_chapter_file(self, content: str) -> tuple[Path, str]:
        import tempfile
        tmpdir = tempfile.mkdtemp()
        p = Path(tmpdir) / "agot-bran-01.md"
        p.write_text(content, encoding="utf-8")
        return p, "sources/chapters/agot/agot-bran-01.md"

    def test_low_quality_source_slug_routes_to_escalation(self):
        """An event item where first entity resolves to a bare title slug is escalated."""
        # We use a stub that resolves "Lord" → "lord" (a low-quality slug)
        # Rather than testing the full resolver (complex), we test _emit_entity_pair_candidates
        # directly with a known low-quality slug.
        from tests._helpers import load_script
        et = load_script("stage4-pass1-extra-tables.py")
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya and Jon sparred.\n"
        )
        emit_rows, escals = et._emit_entity_pair_candidates(
            slugs=["lord", "arya-stark"],  # "lord" is low-quality source
            candidate_kind="pass1_events",
            source_section="Events & Actions",
            hint_raw="lord ordered Arya something",
            evidence_quote="",
            evidence_context="",
            chapter_slug="agot-bran-01",
            book_abbrev="agot",
            pov_slug="bran-stark",
            extraction_rel="extractions/mechanical/agot/agot-bran-01.extraction.md",
            run_id="test",
            schema_version="v1",
            produced_at="2026-05-24T00:00:00+00:00",
            chapter_path=chapter_path,
            chapter_rel=chapter_rel,
        )
        self.assertEqual(len(emit_rows), 0, "Low-quality source slug must not emit a candidate")
        self.assertEqual(len(escals), 1, "Low-quality source slug must route to escalation")
        self.assertIn("low-quality", escals[0]["escalation_reason"])

    def test_low_quality_target_slug_routes_to_escalation(self):
        """An event where target slug is a bare title is escalated."""
        from tests._helpers import load_script
        et = load_script("stage4-pass1-extra-tables.py")
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya and Jon sparred.\n"
        )
        emit_rows, escals = et._emit_entity_pair_candidates(
            slugs=["arya-stark", "ser"],  # "ser" is low-quality target
            candidate_kind="pass1_events",
            source_section="Events & Actions",
            hint_raw="Arya spoke to ser",
            evidence_quote="",
            evidence_context="",
            chapter_slug="agot-bran-01",
            book_abbrev="agot",
            pov_slug="bran-stark",
            extraction_rel="extractions/mechanical/agot/agot-bran-01.extraction.md",
            run_id="test",
            schema_version="v1",
            produced_at="2026-05-24T00:00:00+00:00",
            chapter_path=chapter_path,
            chapter_rel=chapter_rel,
        )
        self.assertEqual(len(emit_rows), 0, "Low-quality target slug must not emit a candidate")
        self.assertEqual(len(escals), 1)
        self.assertIn("low-quality", escals[0]["escalation_reason"])

    def test_passive_voice_routes_to_escalation(self):
        """A hint with passive voice routes to escalation (direction uncertain)."""
        from tests._helpers import load_script
        et = load_script("stage4-pass1-extra-tables.py")
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya and Jon sparred.\n"
        )
        emit_rows, escals = et._emit_entity_pair_candidates(
            slugs=["arya-stark", "jon-snow"],
            candidate_kind="pass1_events",
            source_section="Events & Actions",
            hint_raw="Jon was told by Arya to stop.",  # passive voice
            evidence_quote="",
            evidence_context="",
            chapter_slug="agot-bran-01",
            book_abbrev="agot",
            pov_slug="bran-stark",
            extraction_rel="extractions/mechanical/agot/agot-bran-01.extraction.md",
            run_id="test",
            schema_version="v1",
            produced_at="2026-05-24T00:00:00+00:00",
            chapter_path=chapter_path,
            chapter_rel=chapter_rel,
        )
        self.assertEqual(len(emit_rows), 0, "Passive voice must not emit a candidate")
        self.assertEqual(len(escals), 1)
        self.assertIn("passive", escals[0]["escalation_reason"])

    def test_clean_active_pair_emits(self):
        """A clean active-voice pair with good slugs must emit (not escalate)."""
        from tests._helpers import load_script
        et = load_script("stage4-pass1-extra-tables.py")
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya and Jon Snow sparred in the yard.\n"
        )
        emit_rows, escals = et._emit_entity_pair_candidates(
            slugs=["arya-stark", "jon-snow"],
            candidate_kind="pass1_events",
            source_section="Events & Actions",
            hint_raw="Arya and Jon Snow sparred in the yard.",
            evidence_quote="",
            evidence_context="",
            chapter_slug="agot-bran-01",
            book_abbrev="agot",
            pov_slug="bran-stark",
            extraction_rel="extractions/mechanical/agot/agot-bran-01.extraction.md",
            run_id="test",
            schema_version="v1",
            produced_at="2026-05-24T00:00:00+00:00",
            chapter_path=chapter_path,
            chapter_rel=chapter_rel,
        )
        self.assertGreaterEqual(len(emit_rows), 1, "Clean active pair must emit")
        self.assertEqual(len(escals), 0, "Clean pair must not escalate")

    def test_escalation_row_has_decision_field(self):
        """Escalation rows must carry decision='escalate'."""
        from tests._helpers import load_script
        et = load_script("stage4-pass1-extra-tables.py")
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nSomeone spoke.\n"
        )
        _, escals = et._emit_entity_pair_candidates(
            slugs=["lord", "arya-stark"],
            candidate_kind="pass1_dialogue",
            source_section="Dialogue of Note",
            hint_raw="lord said hello",
            evidence_quote="",
            evidence_context="",
            chapter_slug="agot-bran-01",
            book_abbrev="agot",
            pov_slug="bran-stark",
            extraction_rel="x.md",
            run_id="test",
            schema_version="v1",
            produced_at="2026-05-24T00:00:00+00:00",
            chapter_path=chapter_path,
            chapter_rel=chapter_rel,
        )
        for escal in escals:
            self.assertEqual(escal["decision"], "escalate")
            self.assertIn("escalation_reason", escal)

    def test_is_low_quality_endpoint_importable(self):
        """is_low_quality_endpoint must be importable from the module (for formalize step)."""
        self.assertTrue(hasattr(extra_mod, "is_low_quality_endpoint"))
        self.assertTrue(callable(extra_mod.is_low_quality_endpoint))

    def test_generator_returns_5_tuple(self):
        """generate_events_candidates must return a 5-tuple (cands, 2plus, dropped, escalated, escal_rows)."""
        chapter_path, chapter_rel = self._make_chapter_file(
            "---\nfoo: bar\n---\nArya and Jon Snow sparred in the yard.\n"
        )
        result = generate_events_candidates(
            event_items=["1. **Act** — Arya and Jon Snow sparred in the yard."],
            **_gen_kwargs(chapter_path, chapter_rel),
        )
        self.assertEqual(len(result), 5, "generate_events_candidates must return 5-tuple")
        cands, rows_2plus, rows_dropped, rows_escalated, escal_rows = result
        self.assertIsInstance(cands, list)
        self.assertIsInstance(rows_2plus, int)
        self.assertIsInstance(rows_dropped, int)
        self.assertIsInstance(rows_escalated, int)
        self.assertIsInstance(escal_rows, list)


# ---------------------------------------------------------------------------
# Tests: Fix 3 — ENDPOINT_BLOCKLIST (Problem B)
# ---------------------------------------------------------------------------

ENDPOINT_BLOCKLIST = extra_mod.ENDPOINT_BLOCKLIST
_scan_text_for_entities = extra_mod._scan_text_for_entities


class TestEndpointBlocklist(unittest.TestCase):
    """ENDPOINT_BLOCKLIST slugs must be rejected by is_low_quality_endpoint."""

    def test_bastard_blocked(self):
        """'bastard' resolves to a titles node but should never be an endpoint."""
        self.assertTrue(is_low_quality_endpoint("bastard"))

    def test_dog_blocked(self):
        """'dog' resolves to a species node but should never be an endpoint."""
        self.assertTrue(is_low_quality_endpoint("dog"))

    def test_four_storms_blocked(self):
        """'four-storms' is a fuzzy mis-resolution from 'four brothers'."""
        self.assertTrue(is_low_quality_endpoint("four-storms"))

    def test_hunt_of_the_poor_fellows_blocked(self):
        """'hunt-of-the-poor-fellows' is wrong node for Robert's boar hunt."""
        self.assertTrue(is_low_quality_endpoint("hunt-of-the-poor-fellows"))

    def test_blocklist_has_exactly_four_entries(self):
        """Blocklist is conservative: exactly 4 confirmed mis-resolutions."""
        self.assertEqual(len(ENDPOINT_BLOCKLIST), 4)

    def test_tywin_lannister_not_blocked(self):
        """tywin-lannister is a real character endpoint — must NOT be blocked."""
        self.assertFalse(is_low_quality_endpoint("tywin-lannister"))

    def test_eddard_stark_not_blocked(self):
        """eddard-stark must not be blocked."""
        self.assertFalse(is_low_quality_endpoint("eddard-stark"))

    def test_blocklist_drops_in_generator(self):
        """Candidates whose source or target is a blocklisted slug are escalated."""
        import tempfile
        tmpdir = tempfile.mkdtemp()
        chapter_path = Path(tmpdir) / "agot-bran-01.md"
        chapter_path.write_text("---\nfoo: bar\n---\nSome text.\n", encoding="utf-8")
        # We inject pre-resolved slugs directly into _emit_entity_pair_candidates.
        # "bastard" is in ENDPOINT_BLOCKLIST → escalated, not emitted.
        emit_rows, escals = extra_mod._emit_entity_pair_candidates(
            slugs=["arya-stark", "bastard"],
            candidate_kind="pass1_events",
            source_section="Events & Actions",
            hint_raw="Arya was called a bastard.",
            evidence_quote="",
            evidence_context="",
            chapter_slug="agot-bran-01",
            book_abbrev="agot",
            pov_slug="bran-stark",
            extraction_rel="extractions/mechanical/agot/agot-bran-01.extraction.md",
            run_id="test",
            schema_version="v1",
            produced_at="2026-05-27T00:00:00+00:00",
            chapter_path=chapter_path,
            chapter_rel="sources/chapters/agot/agot-bran-01.md",
        )
        self.assertEqual(len(emit_rows), 0, "Blocklisted target must not emit")
        self.assertEqual(len(escals), 1, "Blocklisted target must escalate")

    def test_dog_drops_in_generator(self):
        """'dog' endpoint is blocked even though dog.node.md exists."""
        import tempfile
        tmpdir = tempfile.mkdtemp()
        chapter_path = Path(tmpdir) / "agot-bran-01.md"
        chapter_path.write_text("---\nfoo: bar\n---\nSome text.\n", encoding="utf-8")
        emit_rows, escals = extra_mod._emit_entity_pair_candidates(
            slugs=["dog", "arya-stark"],
            candidate_kind="pass1_events",
            source_section="Events & Actions",
            hint_raw="A dog followed Arya.",
            evidence_quote="",
            evidence_context="",
            chapter_slug="agot-bran-01",
            book_abbrev="agot",
            pov_slug="bran-stark",
            extraction_rel="extractions/mechanical/agot/agot-bran-01.extraction.md",
            run_id="test",
            schema_version="v1",
            produced_at="2026-05-27T00:00:00+00:00",
            chapter_path=chapter_path,
            chapter_rel="sources/chapters/agot/agot-bran-01.md",
        )
        self.assertEqual(len(emit_rows), 0, "Blocklisted source must not emit")
        self.assertEqual(len(escals), 1)


# ---------------------------------------------------------------------------
# Tests: Fix 4 — title-person disambiguation in _build_present_slugs
# (Problem A — root cause: bootstrap seeds wrong slug into present_slugs)
# ---------------------------------------------------------------------------

_build_present_slugs = extra_mod._build_present_slugs


class TestBuildPresentSlugsBootstrapTitlePerson(unittest.TestCase):
    """_build_present_slugs must remap bootstrapped non-character artifact slugs
    when slug_category is provided (the lord-tywin → tywin-lannister case).
    """

    # Same stub environment as TestTitlePersonDisambiguation
    _NODE_SET = {"lord-tywin", "tywin-lannister", "cersei-lannister", "eddard-stark"}
    _ALIAS_MAP = {}
    _FIRSTNAME_INDEX = {
        "tywin": ["tywin-lannister", "lord-tywin"],  # multiple → remap needed
        "cersei": ["cersei-lannister"],
        "eddard": ["eddard-stark"],
    }
    _PRIOR = {"tywin-lannister": 500, "lord-tywin": 10}
    _SLUG_CATEGORY = {
        "lord-tywin": "artifacts",
        "tywin-lannister": "characters",
        "cersei-lannister": "characters",
        "eddard-stark": "characters",
    }

    def _text_with_chars(self, *names) -> str:
        """Minimal extraction text with a Characters Present table."""
        rows = "\n".join(
            f"| {name} | Present | No | |" for name in names
        )
        return (
            "## Characters Present\n"
            "| Character | Role | First? | Notes |\n"
            "|-----------|------|--------|-------|\n"
            + rows + "\n\n## Events & Actions\n1. Something.\n"
        )

    def test_lord_tywin_bootstrap_without_slug_category_seeds_artifact(self):
        """Without slug_category, 'Lord Tywin' bootstrap seeds lord-tywin (artifact)."""
        text = self._text_with_chars("Lord Tywin")
        # Inject "Lord Tywin" as a dialogue speaker too
        diag_rows = [{"speaker": "Lord Tywin", "listener": "Cersei", "quote": "", "context": ""}]
        present = _build_present_slugs(
            text, [], diag_rows,
            self._ALIAS_MAP, self._NODE_SET, self._FIRSTNAME_INDEX,
            # No slug_category
        )
        # Without fix, lord-tywin (the artifact) is seeded
        self.assertIn("lord-tywin", present)
        self.assertNotIn("tywin-lannister", present)

    def test_lord_tywin_bootstrap_with_slug_category_seeds_character(self):
        """With slug_category, 'Lord Tywin' bootstrap seeds tywin-lannister (char)."""
        diag_rows = [{"speaker": "Lord Tywin", "listener": "Cersei", "quote": "", "context": ""}]
        text = self._text_with_chars("Lord Tywin")
        present = _build_present_slugs(
            text, [], diag_rows,
            self._ALIAS_MAP, self._NODE_SET, self._FIRSTNAME_INDEX,
            slug_category=self._SLUG_CATEGORY,
            importance_prior=self._PRIOR,
        )
        self.assertIn("tywin-lannister", present)
        self.assertNotIn("lord-tywin", present)


class TestTitlePersonDisambiguation(unittest.TestCase):
    """_scan_text_for_entities must use slug_category to resolve 'Lord Tywin'
    → tywin-lannister (not lord-tywin the ship artifact).
    """

    # Minimal stub environment mirroring the actual collision.
    # lord-tywin is an artifact; tywin-lannister is a character.
    _NODE_SET = {"lord-tywin", "tywin-lannister", "cersei-lannister", "eddard-stark"}
    _ALIAS_MAP = {}
    _FIRSTNAME_INDEX = {
        "tywin": ["tywin-lannister"],
        "cersei": ["cersei-lannister"],
        "eddard": ["eddard-stark"],
    }
    _PRIOR = {"tywin-lannister": 500, "lord-tywin": 10}
    _PRESENT = set(_NODE_SET)
    _SLUG_CATEGORY = {
        "lord-tywin": "artifacts",          # The ship — NOT a character
        "tywin-lannister": "characters",
        "cersei-lannister": "characters",
        "eddard-stark": "characters",
    }

    def test_lord_tywin_without_slug_category_returns_ship(self):
        """Without slug_category, 'Lord Tywin' exact-matches the artifact node."""
        slugs = _scan_text_for_entities(
            "Lord Tywin ordered Cersei to comply.",
            self._ALIAS_MAP, self._NODE_SET, self._FIRSTNAME_INDEX,
            self._PRIOR, self._PRESENT,
            # No slug_category
        )
        # Without the fix, lord-tywin (the ship) is resolved
        self.assertIn("lord-tywin", slugs)
        self.assertNotIn("tywin-lannister", slugs)

    def test_lord_tywin_with_slug_category_returns_person(self):
        """With slug_category, 'Lord Tywin' is redirected to tywin-lannister."""
        slugs = _scan_text_for_entities(
            "Lord Tywin ordered Cersei to comply.",
            self._ALIAS_MAP, self._NODE_SET, self._FIRSTNAME_INDEX,
            self._PRIOR, self._PRESENT,
            slug_category=self._SLUG_CATEGORY,
        )
        self.assertIn("tywin-lannister", slugs)
        self.assertNotIn("lord-tywin", slugs)

    def test_lord_tywin_not_doubled_in_results(self):
        """After title-person redirect, the cursor advances past both tokens
        so 'Tywin' doesn't produce a second tywin-lannister slug."""
        slugs = _scan_text_for_entities(
            "Lord Tywin arrived.",
            self._ALIAS_MAP, self._NODE_SET, self._FIRSTNAME_INDEX,
            self._PRIOR, self._PRESENT,
            slug_category=self._SLUG_CATEGORY,
        )
        # Only one occurrence of tywin-lannister
        self.assertEqual(slugs.count("tywin-lannister"), 1)

    def test_pair_emitted_with_slug_category(self):
        """An event item with 'Lord Tywin' and another character should emit a
        candidate with tywin-lannister (not lord-tywin) as an endpoint."""
        import tempfile
        tmpdir = tempfile.mkdtemp()
        chapter_path = Path(tmpdir) / "agot-tywin-01.md"
        chapter_path.write_text(
            "---\nfoo: bar\n---\nLord Tywin ordered Cersei to comply.\n",
            encoding="utf-8",
        )
        chapter_rel = "sources/chapters/agot/agot-tywin-01.md"
        items = ["1. **Order** — Lord Tywin ordered Cersei to comply."]
        cands, _, _, _, _ = generate_events_candidates(
            event_items=items,
            chapter_slug="agot-tywin-01",
            book_abbrev="agot",
            pov_slug="tyrion-lannister",
            extraction_rel="extractions/mechanical/agot/agot-tywin-01.extraction.md",
            alias_map=self._ALIAS_MAP,
            node_set=self._NODE_SET,
            firstname_index=self._FIRSTNAME_INDEX,
            importance_prior=self._PRIOR,
            present_slugs=self._PRESENT,
            chapter_path=chapter_path,
            chapter_rel=chapter_rel,
            run_id="test",
            schema_version="v1",
            produced_at="2026-05-27T00:00:00+00:00",
            slug_category=self._SLUG_CATEGORY,
        )
        all_slugs = {c["source_slug"] for c in cands} | {c["target_slug"] for c in cands}
        self.assertIn("tywin-lannister", all_slugs,
                      f"Expected tywin-lannister in endpoints; got {all_slugs}")
        self.assertNotIn("lord-tywin", all_slugs,
                         f"lord-tywin (ship artifact) must not appear; got {all_slugs}")


if __name__ == "__main__":
    unittest.main()
