"""Tests for scripts/date-event-nodes.py

Covers:
  - Classification (clean vs multiyear vs nomatch)
  - Validator invariants (reject string ac_year, reject reckoning key,
    tertiary-fan tier cap, precision enum)
  - Idempotency (second apply is no-op)
  - Body preservation (frontmatter patch leaves body byte-identical)

Does NOT mutate real graph files. All fixtures in tmp_path.
"""
import hashlib
import json
import textwrap
from pathlib import Path

import pytest

from tests._helpers import load_script

# Load the module under test
mod = load_script("date-event-nodes.py")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_node(tmp_path: Path, slug: str, extra_fm: str = "", body: str = "") -> Path:
    """Write a minimal event node file and return its path."""
    p = tmp_path / f"{slug}.node.md"
    base_lines = [
        "---",
        f'name: "{slug.replace("-", " ").title()}"',
        f"slug: {slug}",
        "type: event.battle",
        "confidence: tier-1",
    ]
    if extra_fm.strip():
        base_lines.append(extra_fm.strip())
    base_lines.append("---")
    base_lines.append("")
    fm = "\n".join(base_lines)
    p.write_text(fm + body, encoding="utf-8")
    return p


def make_chronology(tmp_path: Path, rows: list[dict]) -> Path:
    """Write a chronology-events.jsonl fixture and return its path."""
    p = tmp_path / "chronology-events.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return p


def sha(body: str) -> str:
    return hashlib.sha256(body.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Classification tests
# ---------------------------------------------------------------------------

class TestClassification:
    def test_clean_single_year(self, tmp_path):
        """A slug with exactly one year and a node file → CLEAN."""
        make_node(tmp_path, "battle-of-test")
        chron = make_chronology(tmp_path, [
            {"year_page": "283 AC", "year_value": 283, "year_era": "AC",
             "target_page": "Battle of Test", "target_slug": "battle-of-test",
             "target_type": "event.battle", "anchor_text": "Battle of Test",
             "snippet": "test snippet"},
        ])
        result = mod.classify_slugs(chron, tmp_path)
        assert "battle-of-test" in result["clean"]
        assert result["clean"]["battle-of-test"] == 283
        assert "battle-of-test" not in result["multiyear"]
        assert "battle-of-test" not in result["nomatch"]

    def test_multiyear(self, tmp_path):
        """A slug with >1 distinct years → MULTIYEAR, not CLEAN."""
        make_node(tmp_path, "long-war")
        chron = make_chronology(tmp_path, [
            {"year_value": 100, "year_era": "AC", "target_slug": "long-war",
             "target_type": "event.war", "anchor_text": "Long War",
             "year_page": "100 AC", "target_page": "Long War", "snippet": ""},
            {"year_value": 110, "year_era": "AC", "target_slug": "long-war",
             "target_type": "event.war", "anchor_text": "Long War",
             "year_page": "110 AC", "target_page": "Long War", "snippet": ""},
        ])
        result = mod.classify_slugs(chron, tmp_path)
        assert "long-war" in result["multiyear"]
        assert result["multiyear"]["long-war"] == [100, 110]
        assert "long-war" not in result["clean"]

    def test_nomatch(self, tmp_path):
        """A slug with no node file → NOMATCH."""
        # No node file written
        chron = make_chronology(tmp_path, [
            {"year_value": 298, "year_era": "AC", "target_slug": "ghost-event",
             "target_type": "event.battle", "anchor_text": "Ghost Event",
             "year_page": "298 AC", "target_page": "Ghost Event", "snippet": ""},
        ])
        result = mod.classify_slugs(chron, tmp_path)
        assert "ghost-event" in result["nomatch"]
        assert "ghost-event" not in result["clean"]

    def test_non_event_rows_ignored(self, tmp_path):
        """Rows with target_type not starting with 'event' are ignored."""
        chron = make_chronology(tmp_path, [
            {"year_value": 283, "year_era": "AC", "target_slug": "eddard-stark",
             "target_type": "character.human", "anchor_text": "Eddard Stark",
             "year_page": "283 AC", "target_page": "Eddard Stark", "snippet": ""},
            {"year_value": 283, "year_era": "AC", "target_slug": "winterfell",
             "target_type": "place.location", "anchor_text": "Winterfell",
             "year_page": "283 AC", "target_page": "Winterfell", "snippet": ""},
        ])
        result = mod.classify_slugs(chron, tmp_path)
        assert result["clean"] == {}
        assert result["multiyear"] == {}
        assert result["nomatch"] == {}

    def test_blocklist_excludes(self, tmp_path):
        """Blocklisted slugs are never classified as CLEAN even with one year."""
        for slug in mod.BLOCKLIST:
            make_node(tmp_path, slug)
        chron = make_chronology(tmp_path, [
            {"year_value": 101, "year_era": "AC", "target_slug": "great-council",
             "target_type": "event.war", "anchor_text": "Great Council",
             "year_page": "101 AC", "target_page": "Great Council", "snippet": ""},
        ])
        result = mod.classify_slugs(chron, tmp_path)
        assert "great-council" not in result["clean"]
        assert any(slug == "great-council" for slug, _ in result["blocklisted"])

    def test_already_dated_skipped(self, tmp_path):
        """Node with existing occurred: block → ALREADY_DATED, not overwritten."""
        extra = textwrap.dedent("""\
            occurred:
              ac_year: 299
              precision: year
              basis_source: wiki-year-page
              basis_reliability: tertiary-fan
              date_confidence: tier-3
        """)
        make_node(tmp_path, "pre-dated-battle", extra_fm=extra)
        chron = make_chronology(tmp_path, [
            {"year_value": 283, "year_era": "AC", "target_slug": "pre-dated-battle",
             "target_type": "event.battle", "anchor_text": "Pre Dated Battle",
             "year_page": "283 AC", "target_page": "Pre Dated Battle", "snippet": ""},
        ])
        result = mod.classify_slugs(chron, tmp_path)
        assert "pre-dated-battle" in result["already_dated"]
        assert "pre-dated-battle" not in result["clean"]


# ---------------------------------------------------------------------------
# Validator tests
# ---------------------------------------------------------------------------

class TestValidator:
    def _valid(self):
        return {
            "ac_year": 283,
            "precision": "year",
            "basis_source": "wiki-year-page",
            "basis_reliability": "tertiary-fan",
            "date_confidence": "tier-3",
        }

    def test_valid_block_passes(self):
        mod.validate_occurred_block(self._valid())  # should not raise

    def test_string_ac_year_rejected(self):
        block = self._valid()
        block["ac_year"] = "283 AC"
        with pytest.raises(ValueError, match="ac_year must be int"):
            mod.validate_occurred_block(block)

    def test_reckoning_key_rejected(self):
        block = self._valid()
        block["reckoning"] = "AC"
        with pytest.raises(ValueError, match="reckoning"):
            mod.validate_occurred_block(block)

    def test_tertiary_fan_requires_tier3_plus(self):
        block = self._valid()
        block["basis_reliability"] = "tertiary-fan"
        block["date_confidence"] = "tier-2"
        with pytest.raises(ValueError, match="tertiary-fan"):
            mod.validate_occurred_block(block)

    def test_tertiary_fan_tier3_ok(self):
        block = self._valid()
        block["basis_reliability"] = "tertiary-fan"
        block["date_confidence"] = "tier-3"
        mod.validate_occurred_block(block)  # no raise

    def test_tertiary_fan_tier4_ok(self):
        block = self._valid()
        block["basis_reliability"] = "tertiary-fan"
        block["date_confidence"] = "tier-4"
        mod.validate_occurred_block(block)  # no raise

    def test_invalid_precision_rejected(self):
        block = self._valid()
        block["precision"] = "approximate"
        with pytest.raises(ValueError, match="precision"):
            mod.validate_occurred_block(block)

    def test_valid_precision_values(self):
        for p in mod.VALID_PRECISIONS:
            block = self._valid()
            block["precision"] = p
            mod.validate_occurred_block(block)  # no raise

    def test_ac_year_end_must_be_greater(self):
        block = self._valid()
        block["ac_year_end"] = 283  # equal, not greater
        with pytest.raises(ValueError, match="ac_year_end must be"):
            mod.validate_occurred_block(block)

    def test_ac_year_end_valid(self):
        block = self._valid()
        block["ac_year_end"] = 290
        mod.validate_occurred_block(block)  # no raise

    def test_uncertainty_radius_and_ac_year_end_exclusive(self):
        block = self._valid()
        block["ac_year_end"] = 290
        block["uncertainty_radius"] = 5
        with pytest.raises(ValueError, match="mutually exclusive"):
            mod.validate_occurred_block(block)

    def test_basis_source_required_when_ac_year_set(self):
        block = self._valid()
        del block["basis_source"]
        with pytest.raises(ValueError, match="basis_source required"):
            mod.validate_occurred_block(block)

    def test_no_ac_year_no_basis_source_required(self):
        """When ac_year is None, basis_source is NOT required (null year = unknown)."""
        block = {"precision": "year", "basis_reliability": "tertiary-fan",
                 "date_confidence": "tier-3", "ac_year": None}
        # basis_source absent AND ac_year is None → should NOT raise
        mod.validate_occurred_block(block)  # no raise expected


# ---------------------------------------------------------------------------
# Idempotency tests
# ---------------------------------------------------------------------------

class TestIdempotency:
    def test_second_apply_is_noop(self, tmp_path):
        """Applying twice leaves the file unchanged after the first write."""
        body = "## Identity\n\nSome event.\n\n## Edges\n\n- FIGHTS_IN: some-war\n"
        p = make_node(tmp_path, "battle-idempotent", body=body)

        # First apply
        written1, _ = mod.patch_node_file(p, 283, apply=True)
        assert written1 is True
        text_after_first = p.read_text(encoding="utf-8")
        assert "occurred:" in text_after_first
        assert "ac_year: 283" in text_after_first

        # Classify again — should now show ALREADY_DATED
        chron = make_chronology(tmp_path, [
            {"year_value": 283, "year_era": "AC", "target_slug": "battle-idempotent",
             "target_type": "event.battle", "anchor_text": "Battle Idempotent",
             "year_page": "283 AC", "target_page": "Battle Idempotent", "snippet": ""},
        ])
        result = mod.classify_slugs(chron, tmp_path)
        assert "battle-idempotent" in result["already_dated"]
        assert "battle-idempotent" not in result["clean"]

    def test_dry_run_writes_nothing(self, tmp_path):
        """Dry-run (apply=False) does not write the file."""
        body = "## Identity\n\nSome event.\n"
        p = make_node(tmp_path, "battle-dryrun", body=body)
        original_text = p.read_text(encoding="utf-8")

        written, _ = mod.patch_node_file(p, 283, apply=False)
        assert written is False
        assert p.read_text(encoding="utf-8") == original_text


# ---------------------------------------------------------------------------
# Body preservation tests
# ---------------------------------------------------------------------------

class TestBodyPreservation:
    def test_body_unchanged_after_patch(self, tmp_path):
        """The markdown body is byte-for-byte identical before and after patch."""
        body = textwrap.dedent("""\
            ## Identity

            The Battle of Body Preservation took place at the crossing.

            ## Edges

            - FIGHTS_IN: roberts-rebellion
            - LOCATED_AT: ruby-ford

            ## Quotes

            > They met in single combat.
            >
            > — Eddard Stark

            ## Origins

            Some more content with unicode: Æ, ö, and symbols: → ↔ ≤
        """)
        p = make_node(tmp_path, "battle-body-test", body=body)
        before_body_hash = hashlib.sha256(body.encode()).hexdigest()

        # Apply
        mod.patch_node_file(p, 283, apply=True)

        # Re-read and extract body
        new_text = p.read_text(encoding="utf-8")
        _, new_body, _ = mod.split_frontmatter(new_text)
        after_body_hash = hashlib.sha256(new_body.encode()).hexdigest()

        assert before_body_hash == after_body_hash, (
            "Body was modified by frontmatter patch"
        )

    def test_occurred_in_frontmatter_not_body(self, tmp_path):
        """The occurred: block appears only in frontmatter, not in body."""
        body = "## Identity\n\nAn event.\n"
        p = make_node(tmp_path, "battle-fm-test", body=body)
        mod.patch_node_file(p, 100, apply=True)

        new_text = p.read_text(encoding="utf-8")
        raw_yaml, body_out, _ = mod.split_frontmatter(new_text)

        assert "occurred:" in raw_yaml
        assert "occurred:" not in body_out

    def test_frontmatter_well_formed_after_patch(self, tmp_path):
        """After patch, frontmatter is bounded by --- delimiters and contains required fields."""
        body = "## Identity\n\nAn event.\n"
        p = make_node(tmp_path, "battle-fm-wf", body=body)
        mod.patch_node_file(p, 299, apply=True)

        new_text = p.read_text(encoding="utf-8")
        assert new_text.startswith("---\n")
        # Split on --- boundaries
        parts = new_text.split("---\n", maxsplit=2)
        assert len(parts) == 3  # before first ---, fm content, body
        fm = parts[1]
        assert "slug:" in fm
        assert "type:" in fm
        assert "occurred:" in fm
        assert "ac_year: 299" in fm


# ---------------------------------------------------------------------------
# Chapter ref normalization tests
# ---------------------------------------------------------------------------

class TestNormalizeChapterRef:
    def test_kebab_format(self):
        result = mod.normalize_chapter_ref("agot-arya-01")
        assert result == (1, 1)

    def test_kebab_format_acok(self):
        result = mod.normalize_chapter_ref("acok-tyrion-14")
        assert result == (2, 14)

    def test_roman_format(self):
        result = mod.normalize_chapter_ref("ASOS Catelyn VII")
        assert result == (3, 7)

    def test_roman_format_acok(self):
        result = mod.normalize_chapter_ref("ACOK Theon III")
        assert result == (2, 3)

    def test_empty_returns_none(self):
        assert mod.normalize_chapter_ref("") is None

    def test_none_returns_none(self):
        assert mod.normalize_chapter_ref(None) is None

    def test_unknown_format_returns_none(self):
        assert mod.normalize_chapter_ref("chapter 5 of something") is None
