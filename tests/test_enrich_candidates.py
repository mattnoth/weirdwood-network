"""Tests for scripts/wiki-pass2-enrich-candidates.py (Session 63).

The enrichment script pre-computes per-row context so Haiku doesn't have to
read node files. These tests freeze the contracts:

- target_type lookup via node-type-index
- evidence_paragraph extraction (clean of cite_ref noise; wiki links → «anchor»)
- valid_edge_types filtered by target_type
- staging_verbs_present regex on whitelisted verbs
- _python_prereject markers for unresolved targets / missing paragraphs

Run: python3 -m unittest tests.test_enrich_candidates -v
"""

import unittest

from tests._helpers import load_script

enrich = load_script("wiki-pass2-enrich-candidates.py")


class TestCleanParagraph(unittest.TestCase):
    """clean_paragraph strips MediaWiki cite_ref noise and normalizes wiki links."""

    def test_strips_cite_ref_noise(self):
        raw = "Jory has a wry smile,(wiki:Jory_Cassel.cite_ref-Ragot35.7B.7B.7B3.7D.7D.7D_5-0) which he often shows."
        out = enrich.clean_paragraph(raw)
        self.assertNotIn("cite_ref", out)
        self.assertNotIn("7B.7B", out)
        self.assertIn("Jory has a wry smile", out)

    def test_normalizes_wiki_links_to_anchors(self):
        raw = "[Arya Stark](wiki:Arya_Stark) and [Sansa](wiki:Sansa_Stark) walked."
        out = enrich.clean_paragraph(raw)
        self.assertIn("«Arya Stark»", out)
        self.assertIn("«Sansa»", out)
        self.assertNotIn("wiki:", out)

    def test_collapses_whitespace(self):
        raw = "hello    world\t\twith   spaces"
        out = enrich.clean_paragraph(raw)
        self.assertEqual(out, "hello world with spaces")

    def test_full_paragraph_round_trip(self):
        raw = (
            "Jory has a wry smile,(wiki:Jory_Cassel.cite_ref-Ragot35.7B.7B_5-0) "
            "which he often shows to [Arya Stark](wiki:Arya_Stark),"
            "(wiki:Jory_Cassel.cite_ref-Rasos17.7B.7B_6-0) and he jokes."
        )
        out = enrich.clean_paragraph(raw)
        self.assertEqual(
            out,
            "Jory has a wry smile, which he often shows to «Arya Stark», and he jokes.",
        )


class TestExtractParagraphsBySection(unittest.TestCase):
    """Section parser groups paragraphs by H2 header."""

    def test_basic_section_split(self):
        md = (
            "# Title\n\n"
            "preamble\n\n"
            "## Section A\n\n"
            "Paragraph A1.\n\n"
            "Paragraph A2.\n\n"
            "## Section B\n\n"
            "Paragraph B1.\n"
        )
        out = enrich.extract_paragraphs_by_section(md)
        self.assertIn("## Section A", out)
        self.assertIn("## Section B", out)
        self.assertEqual(out["## Section A"], ["Paragraph A1.", "Paragraph A2."])
        self.assertEqual(out["## Section B"], ["Paragraph B1."])

    def test_handles_blank_section(self):
        md = "## Empty\n\n## Real\n\nbody.\n"
        out = enrich.extract_paragraphs_by_section(md)
        self.assertEqual(out["## Empty"], [])
        self.assertEqual(out["## Real"], ["body."])


class TestFindAnchorParagraph(unittest.TestCase):
    """find_anchor_paragraph locates the paragraph containing a wiki link."""

    def test_finds_by_wiki_link(self):
        paragraphs = [
            "Some unrelated paragraph.",
            "Jory shows wry smile to [Arya Stark](wiki:Arya_Stark) here.",
            "Another paragraph.",
        ]
        result = enrich.find_anchor_paragraph(paragraphs, "Arya_Stark", "Arya Stark")
        self.assertIn("Arya Stark", result)

    def test_returns_none_when_absent(self):
        paragraphs = ["nothing about anyone here."]
        result = enrich.find_anchor_paragraph(paragraphs, "Tyrion_Lannister", "Tyrion")
        self.assertIsNone(result)

    def test_fallback_to_anchor_text(self):
        # No link, just anchor text appearing literally
        paragraphs = ["Plain text mentioning Arya Stark."]
        result = enrich.find_anchor_paragraph(paragraphs, "Arya_Stark", "Arya Stark")
        self.assertIsNotNone(result)


class TestValidEdgeTypes(unittest.TestCase):
    """valid_edge_types filters the vocab by target type-contract."""

    def setUp(self):
        self.contracts = {
            "WIELDS": ("character.", ("object.artifact",)),
            "BORN_AT": ("character.", ("place.location",)),
            "SEAT_OF": ("place.location", ("organization.house",)),
        }
        self.vocab = {"WIELDS", "BORN_AT", "SEAT_OF", "KILLS", "SPOUSE_OF"}

    def test_unconstrained_types_always_valid(self):
        result = enrich.compute_valid_edge_types("character.human", self.contracts, self.vocab)
        # KILLS and SPOUSE_OF have no contract — always valid
        self.assertIn("KILLS", result)
        self.assertIn("SPOUSE_OF", result)

    def test_contracted_types_filtered_by_target(self):
        # target = character.human — WIELDS requires object.artifact target
        result = enrich.compute_valid_edge_types("character.human", self.contracts, self.vocab)
        self.assertNotIn("WIELDS", result)  # target type wrong
        self.assertNotIn("BORN_AT", result)  # target type wrong (need place.location)
        self.assertNotIn("SEAT_OF", result)  # target type wrong

    def test_artifact_target_permits_wields(self):
        result = enrich.compute_valid_edge_types("object.artifact", self.contracts, self.vocab)
        self.assertIn("WIELDS", result)
        self.assertNotIn("BORN_AT", result)

    def test_no_target_type_returns_all(self):
        result = enrich.compute_valid_edge_types(None, self.contracts, self.vocab)
        self.assertEqual(set(result), self.vocab)


class TestDetectStagingVerbs(unittest.TestCase):
    """Staging-verb detection mirrors validator's VERB_GATE whitelist."""

    def test_finds_met_past_tense(self):
        result = enrich.detect_staging_verbs("Jon met Tyrion at Winterfell.")
        self.assertIn("met ", result)

    def test_finds_confronted(self):
        result = enrich.detect_staging_verbs("Brienne confronted Randyll Tarly in the great hall.")
        self.assertIn("confronted", result)

    def test_rejects_to_meet_infinitive(self):
        # "to meet" is intent, not staging — should NOT be detected
        result = enrich.detect_staging_verbs("Daemon traveled to meet Lord Connington.")
        # "met " (with trailing space) should not match in "to meet"
        # "meets " also should not match the bare "meet"
        self.assertEqual(result, [])

    def test_empty_paragraph_returns_empty(self):
        self.assertEqual(enrich.detect_staging_verbs(""), [])

    def test_case_insensitive(self):
        result = enrich.detect_staging_verbs("They MET in the throne room.")
        self.assertIn("met ", result)
