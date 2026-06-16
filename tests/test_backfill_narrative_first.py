"""Tests for scripts/backfill-narrative-first.py

Covers:
  - Chapter index building from fixture chapter files
  - Ref normalization: both kebab and roman -> same (book_order, chapter_number)
  - Resolve-all-or-skip: one bad ref -> event skipped (unresolved)
  - Idempotency: second apply is a no-op
  - Sub-field insertion: narrative_first lands inside occurred: block,
    rest of block + body preserved byte-for-byte
  - No-edges events produce no output

All fixtures live in tmp_path — no real graph files mutated.
"""

import hashlib
import json
import textwrap
from pathlib import Path

import pytest

from tests._helpers import load_script

mod = load_script("backfill-narrative-first.py")

ChapterIndex = mod.ChapterIndex
RefResult = mod.RefResult


# ---------------------------------------------------------------------------
# Fixtures helpers
# ---------------------------------------------------------------------------

BOOK_ORDER = {"agot": 1, "acok": 2, "asos": 3, "affc": 4, "adwd": 5}


def make_chapter_file(
    book_dir: Path,
    book: str,
    pov_character: str,
    pov_chapter_number: int,
    chapter_number: int,
    file_slug: str,
) -> Path:
    """Write a minimal chapter .md file with correct frontmatter."""
    fname = f"{book}-{file_slug}-{pov_chapter_number:02d}.md"
    p = book_dir / fname
    fm = textwrap.dedent(f"""\
        ---
        book: {book.upper()}
        chapter_number: {chapter_number}
        pov_character: {pov_character}
        pov_chapter_number: {pov_chapter_number}
        pov_label: "{pov_character} {'I' * pov_chapter_number}"
        file_name: {fname}
        ---

        Chapter text here.
    """)
    p.write_text(fm, encoding="utf-8")
    return p


def make_chapters_dir(tmp_path: Path) -> Path:
    """Create a minimal sources/chapters directory with several chapter files.

    Layout (abbreviated):
      agot/agot-eddard-01.md  chapter_number=2   pov_character=Eddard  pov_chapter_number=1
      agot/agot-arya-01.md    chapter_number=4   pov_character=Arya    pov_chapter_number=1
      asos/asos-catelyn-07.md chapter_number=52  pov_character=Catelyn pov_chapter_number=7
      adwd/adwd-the-prince-of-winterfell-01.md  chapter_number=38  pov=The Prince of Winterfell  pov_ch=1
    """
    chapters = tmp_path / "sources" / "chapters"

    # AGOT
    agot = chapters / "agot"
    agot.mkdir(parents=True)
    # agot-eddard-01: chapter_number=2
    (agot / "agot-eddard-01.md").write_text(textwrap.dedent("""\
        ---
        book: AGOT
        chapter_number: 2
        pov_character: Eddard
        pov_chapter_number: 1
        pov_label: "Eddard I"
        file_name: agot-eddard-01.md
        ---

        Text.
    """), encoding="utf-8")
    # agot-arya-01: chapter_number=4
    (agot / "agot-arya-01.md").write_text(textwrap.dedent("""\
        ---
        book: AGOT
        chapter_number: 4
        pov_character: Arya
        pov_chapter_number: 1
        pov_label: "Arya I"
        file_name: agot-arya-01.md
        ---

        Text.
    """), encoding="utf-8")
    # agot-catelyn-10: chapter_number=55
    (agot / "agot-catelyn-10.md").write_text(textwrap.dedent("""\
        ---
        book: AGOT
        chapter_number: 55
        pov_character: Catelyn
        pov_chapter_number: 10
        pov_label: "Catelyn X"
        file_name: agot-catelyn-10.md
        ---

        Text.
    """), encoding="utf-8")

    # ASOS
    asos = chapters / "asos"
    asos.mkdir(parents=True)
    # asos-catelyn-07: chapter_number=52
    (asos / "asos-catelyn-07.md").write_text(textwrap.dedent("""\
        ---
        book: ASOS
        chapter_number: 52
        pov_character: Catelyn
        pov_chapter_number: 7
        pov_label: "Catelyn VII"
        file_name: asos-catelyn-07.md
        ---

        Text.
    """), encoding="utf-8")
    # asos-arya-07: chapter_number=36
    (asos / "asos-arya-07.md").write_text(textwrap.dedent("""\
        ---
        book: ASOS
        chapter_number: 36
        pov_character: Arya
        pov_chapter_number: 7
        pov_label: "Arya VII"
        file_name: asos-arya-07.md
        ---

        Text.
    """), encoding="utf-8")

    # ADWD
    adwd = chapters / "adwd"
    adwd.mkdir(parents=True)
    # adwd-the-prince-of-winterfell-01: chapter_number=38
    (adwd / "adwd-the-prince-of-winterfell-01.md").write_text(textwrap.dedent("""\
        ---
        book: ADWD
        chapter_number: 38
        pov_character: The Prince of Winterfell
        pov_chapter_number: 1
        pov_label: "The Prince of Winterfell"
        file_name: adwd-the-prince-of-winterfell-01.md
        ---

        Text.
    """), encoding="utf-8")

    return chapters


def make_event_node(
    events_dir: Path,
    slug: str,
    ac_year: int = 299,
    extra_occurred: str = "",
    body: str = "",
) -> Path:
    """Write a minimal dated event node file."""
    p = events_dir / f"{slug}.node.md"
    fm = textwrap.dedent(f"""\
        ---
        name: "{slug.replace('-', ' ').title()}"
        type: event.battle
        slug: {slug}
        aliases: []
        confidence: tier-1
        occurred:
          ac_year: {ac_year}
          precision: year
          basis_source: wiki-year-page
          basis_reliability: tertiary-fan
          date_confidence: tier-3
        """)
    if extra_occurred:
        fm += extra_occurred
    fm += "---\n"
    p.write_text(fm + body, encoding="utf-8")
    return p


def make_edges_file(edges_path: Path, edges: list[dict]) -> None:
    """Write an edges.jsonl fixture."""
    edges_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(e) for e in edges]
    edges_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# ChapterIndex tests
# ---------------------------------------------------------------------------

class TestChapterIndex:
    def test_builds_from_fixture_chapters(self, tmp_path):
        chapters = make_chapters_dir(tmp_path)
        idx = ChapterIndex(chapters)
        assert idx.available

    def test_kebab_lookup_agot_eddard_01(self, tmp_path):
        """agot-eddard-01 should map to (1, 2) — AGOT chapter 2."""
        chapters = make_chapters_dir(tmp_path)
        idx = ChapterIndex(chapters)
        result = idx.lookup_kebab("agot", "eddard", 1)
        assert result == (1, 2)

    def test_kebab_lookup_asos_catelyn_07(self, tmp_path):
        """asos-catelyn-07 should map to (3, 52) — ASOS chapter 52."""
        chapters = make_chapters_dir(tmp_path)
        idx = ChapterIndex(chapters)
        result = idx.lookup_kebab("asos", "catelyn", 7)
        assert result == (3, 52)

    def test_roman_lookup_agot_eddard_i(self, tmp_path):
        """AGOT Eddard I should map to (1, 2) — same as kebab."""
        chapters = make_chapters_dir(tmp_path)
        idx = ChapterIndex(chapters)
        result = idx.lookup_roman("agot", "Eddard", 1)
        assert result == (1, 2)

    def test_roman_lookup_asos_catelyn_vii(self, tmp_path):
        """ASOS Catelyn VII should map to (3, 52)."""
        chapters = make_chapters_dir(tmp_path)
        idx = ChapterIndex(chapters)
        result = idx.lookup_roman("asos", "Catelyn", 7)
        assert result == (3, 52)

    def test_roman_lookup_multiword_pov(self, tmp_path):
        """'ADWD The Prince of Winterfell I' -> (5, 38)."""
        chapters = make_chapters_dir(tmp_path)
        idx = ChapterIndex(chapters)
        result = idx.lookup_roman("adwd", "The Prince of Winterfell", 1)
        assert result == (5, 38)

    def test_missing_chapter_returns_none(self, tmp_path):
        """Non-existent chapter returns None."""
        chapters = make_chapters_dir(tmp_path)
        idx = ChapterIndex(chapters)
        result = idx.lookup_kebab("agot", "tyrion", 99)
        assert result is None

    def test_unavailable_when_dir_missing(self, tmp_path):
        idx = ChapterIndex(tmp_path / "nonexistent")
        assert not idx.available


# ---------------------------------------------------------------------------
# normalize_chapter_ref tests
# ---------------------------------------------------------------------------

@pytest.fixture
def shared_index(tmp_path):
    chapters = make_chapters_dir(tmp_path)
    return ChapterIndex(chapters)


class TestNormalizeChapterRef:
    def test_kebab_and_roman_same_result_catelyn(self, shared_index):
        """Both 'asos-catelyn-07' and 'ASOS Catelyn VII' resolve to (3, 52)."""
        kebab = mod.normalize_chapter_ref("asos-catelyn-07", shared_index)
        roman = mod.normalize_chapter_ref("ASOS Catelyn VII", shared_index)
        assert kebab is not None
        assert roman is not None
        assert kebab == roman == (3, 52)

    def test_kebab_and_roman_same_result_eddard(self, shared_index):
        """Both 'agot-eddard-01' and 'AGOT Eddard I' resolve to (1, 2)."""
        kebab = mod.normalize_chapter_ref("agot-eddard-01", shared_index)
        roman = mod.normalize_chapter_ref("AGOT Eddard I", shared_index)
        assert kebab == roman == (1, 2)

    def test_multiword_roman_resolves(self, shared_index):
        """'ADWD The Prince of Winterfell I' resolves to (5, 38)."""
        result = mod.normalize_chapter_ref("ADWD The Prince of Winterfell I", shared_index)
        assert result == (5, 38)

    def test_none_input_returns_none(self, shared_index):
        assert mod.normalize_chapter_ref(None, shared_index) is None

    def test_empty_string_returns_none(self, shared_index):
        assert mod.normalize_chapter_ref("", shared_index) is None

    def test_unknown_format_returns_none(self, shared_index):
        assert mod.normalize_chapter_ref("chapter five of something", shared_index) is None

    def test_unknown_pov_returns_none(self, shared_index):
        """An unknown POV name not in the index returns None."""
        assert mod.normalize_chapter_ref("AGOT Unknown Person I", shared_index) is None

    def test_mixed_case_kebab_resolves(self, shared_index):
        """Kebab refs with uppercase book prefix still resolve."""
        result = mod.normalize_chapter_ref("ASOS-catelyn-07", shared_index)
        assert result == (3, 52)


# ---------------------------------------------------------------------------
# Resolve-all-or-skip tests
# ---------------------------------------------------------------------------

@pytest.fixture
def skip_setup(tmp_path):
    chapters = make_chapters_dir(tmp_path)
    idx = ChapterIndex(chapters)
    events_dir = tmp_path / "graph" / "nodes" / "events"
    events_dir.mkdir(parents=True)
    edges_path = tmp_path / "graph" / "edges" / "edges.jsonl"
    return {"idx": idx, "events_dir": events_dir, "edges_path": edges_path}


class TestResolveAllOrSkip:
    def test_all_good_refs_produce_will_write(self, skip_setup):
        """When all refs resolve, event is classified as will_write."""
        make_event_node(skip_setup["events_dir"], "red-wedding")
        make_edges_file(skip_setup["edges_path"], [
            {
                "source_slug": "robb-stark",
                "target_slug": "red-wedding",
                "evidence_chapter": "ASOS Catelyn VII",
            }
        ])
        results = mod.compute_narrative_first_for_events(
            {"red-wedding"}, skip_setup["idx"], edges_file=skip_setup["edges_path"]
        )
        assert results["red-wedding"].status == "will_write"
        assert results["red-wedding"].value == (3, 52)

    def test_one_bad_ref_causes_skip(self, skip_setup):
        """If ANY ref fails to resolve, the event is skipped (unresolved)."""
        make_event_node(skip_setup["events_dir"], "mixed-event")
        make_edges_file(skip_setup["edges_path"], [
            {
                "source_slug": "some-char",
                "target_slug": "mixed-event",
                "evidence_chapter": "ASOS Catelyn VII",  # good
            },
            {
                "source_slug": "another-char",
                "target_slug": "mixed-event",
                "evidence_chapter": "ASOS Unknown Person MCMXCIX",  # bad roman numeral
            },
        ])
        results = mod.compute_narrative_first_for_events(
            {"mixed-event"}, skip_setup["idx"], edges_file=skip_setup["edges_path"]
        )
        assert results["mixed-event"].status == "unresolved"
        assert results["mixed-event"].value is None
        assert len(results["mixed-event"].unresolved_refs) >= 1

    def test_no_edges_produces_no_edges_status(self, skip_setup):
        """Event with no chapter-cited edges -> no_edges, not will_write."""
        make_event_node(skip_setup["events_dir"], "no-edge-event")
        make_edges_file(skip_setup["edges_path"], [
            {
                "source_slug": "no-edge-event",
                "target_slug": "some-target",
                # no evidence_chapter field
            }
        ])
        results = mod.compute_narrative_first_for_events(
            {"no-edge-event"}, skip_setup["idx"], edges_file=skip_setup["edges_path"]
        )
        assert results["no-edge-event"].status == "no_edges"

    def test_minimum_chapter_selected(self, skip_setup):
        """Multiple refs -> minimum (book_order, chapter_number) wins."""
        make_event_node(skip_setup["events_dir"], "battle-trident")
        make_edges_file(skip_setup["edges_path"], [
            {
                "source_slug": "robert",
                "target_slug": "battle-trident",
                "evidence_chapter": "asos-catelyn-07",  # (3, 52)
            },
            {
                "source_slug": "ned",
                "target_slug": "battle-trident",
                "evidence_chapter": "agot-eddard-01",  # (1, 2) — earlier
            },
        ])
        results = mod.compute_narrative_first_for_events(
            {"battle-trident"}, skip_setup["idx"], edges_file=skip_setup["edges_path"]
        )
        assert results["battle-trident"].status == "will_write"
        assert results["battle-trident"].value == (1, 2)
        assert results["battle-trident"].human_ref == "agot-eddard-01"

    def test_event_as_source_slug_counted(self, skip_setup):
        """Edges where event is the SOURCE slug are also scanned."""
        make_event_node(skip_setup["events_dir"], "battle-test")
        make_edges_file(skip_setup["edges_path"], [
            {
                "source_slug": "battle-test",  # event as source
                "target_slug": "some-place",
                "evidence_chapter": "agot-arya-01",  # (1, 4)
            }
        ])
        results = mod.compute_narrative_first_for_events(
            {"battle-test"}, skip_setup["idx"], edges_file=skip_setup["edges_path"]
        )
        assert results["battle-test"].status == "will_write"
        assert results["battle-test"].value == (1, 4)


# ---------------------------------------------------------------------------
# Idempotency tests
# ---------------------------------------------------------------------------

@pytest.fixture
def idempotent_events_dir(tmp_path):
    events_dir = tmp_path / "graph" / "nodes" / "events"
    events_dir.mkdir(parents=True)
    return events_dir


class TestIdempotency:
    def test_second_apply_is_noop(self, idempotent_events_dir):
        """After --apply, narrative_first exists; second patch returns (False, 'already has')."""
        p = make_event_node(idempotent_events_dir, "idempotent-event", body="## Identity\n\nSome event.\n")
        # First apply
        written, msg = mod.patch_node_file_narrative_first(p, "asos-52", apply=True)
        assert written is True
        text_after = p.read_text(encoding="utf-8")
        assert 'narrative_first: "asos-52"' in text_after

        # Second apply: should skip
        written2, msg2 = mod.patch_node_file_narrative_first(p, "asos-52", apply=True)
        assert written2 is False
        assert "already has" in msg2

        # File content unchanged by second call
        text_after2 = p.read_text(encoding="utf-8")
        assert text_after2 == text_after

    def test_dry_run_does_not_write(self, idempotent_events_dir):
        """Dry-run (apply=False) does not modify the file."""
        body = "## Identity\n\nAn event.\n"
        p = make_event_node(idempotent_events_dir, "dry-run-event", body=body)
        original = p.read_text(encoding="utf-8")
        written, _ = mod.patch_node_file_narrative_first(p, "agot-1", apply=False)
        assert written is False
        assert p.read_text(encoding="utf-8") == original


# ---------------------------------------------------------------------------
# Sub-field insertion and body preservation tests
# ---------------------------------------------------------------------------

@pytest.fixture
def insert_events_dir(tmp_path):
    events_dir = tmp_path / "graph" / "nodes" / "events"
    events_dir.mkdir(parents=True)
    return events_dir


class TestSubFieldInsertion:
    def test_narrative_first_inserted_under_occurred(self, insert_events_dir):
        """narrative_first appears as a sub-field of occurred:, not at top level."""
        body = "## Identity\n\nThe Battle of the Trident.\n\n## Edges\n\n- FIGHTS_IN: roberts-rebellion\n"
        p = make_event_node(insert_events_dir, "insert-test", ac_year=283, body=body)

        mod.patch_node_file_narrative_first(p, "agot-2", apply=True)

        text = p.read_text(encoding="utf-8")
        raw_yaml = text.split("---\n", 2)[1]

        # narrative_first is a sub-field (indented) under occurred:
        assert "  narrative_first: " in raw_yaml
        # Not a top-level key
        assert "\nnarrative_first:" not in raw_yaml
        assert raw_yaml.count("occurred:") == 1

    def test_body_preserved_byte_for_byte(self, insert_events_dir):
        """The markdown body is unchanged after frontmatter patch."""
        body = textwrap.dedent("""\
            ## Identity

            The Red Wedding was a massacre at the Twins.

            ## Edges

            - SUB_BEAT_OF: war-of-the-five-kings
            - LOCATED_AT: the-twins

            ## Quotes

            > The North remembers.
            >
            > — Lady Barbrey Dustin

            ## Origins

            Unicode content: Æ ö → ↔ ≤
        """)
        p = make_event_node(insert_events_dir, "body-preserve-test", body=body)
        before_hash = hashlib.sha256(body.encode()).hexdigest()

        mod.patch_node_file_narrative_first(p, "asos-52", apply=True)

        new_text = p.read_text(encoding="utf-8")
        _, new_body, _ = mod.split_frontmatter(new_text)
        after_hash = hashlib.sha256(new_body.encode()).hexdigest()
        assert before_hash == after_hash, "Body was modified by frontmatter patch"

    def test_occurred_block_rest_intact(self, insert_events_dir):
        """Existing occurred: sub-fields are preserved after narrative_first insertion."""
        body = "## Identity\n\nAn event.\n"
        p = make_event_node(insert_events_dir, "fields-intact-test", ac_year=299, body=body)

        mod.patch_node_file_narrative_first(p, "asos-52", apply=True)

        text = p.read_text(encoding="utf-8")
        # All original occurred sub-fields must still be present
        assert "ac_year: 299" in text
        assert "precision: year" in text
        assert "basis_source: wiki-year-page" in text
        assert "basis_reliability: tertiary-fan" in text
        assert "date_confidence: tier-3" in text
        assert 'narrative_first: "asos-52"' in text

    def test_narrative_first_value_format(self):
        """narrative_first_str formats correctly as '{book}-{chapter_number}'."""
        result = RefResult("will_write", value=(3, 52), human_ref="ASOS Catelyn VII")
        assert result.narrative_first_str == "asos-52"

    def test_narrative_first_value_format_agot(self):
        result = RefResult("will_write", value=(1, 2), human_ref="agot-eddard-01")
        assert result.narrative_first_str == "agot-2"

    def test_none_value_gives_none_str(self):
        result = RefResult("no_edges")
        assert result.narrative_first_str is None

    def test_no_occurred_block_returns_false(self, insert_events_dir):
        """If the node has no occurred: block, patch returns (False, message)."""
        # Write a node WITHOUT occurred:
        p = insert_events_dir / "no-occurred.node.md"
        p.write_text(textwrap.dedent("""\
            ---
            name: "No Occurred"
            slug: no-occurred
            type: event.battle
            confidence: tier-1
            ---

            ## Identity

            No occurred block here.
        """), encoding="utf-8")
        written, msg = mod.patch_node_file_narrative_first(p, "agot-2", apply=True)
        assert written is False
        assert "no occurred" in msg.lower()


# ---------------------------------------------------------------------------
# insert_narrative_first_into_yaml unit tests
# ---------------------------------------------------------------------------

class TestInsertYaml:
    def test_inserts_after_last_occurred_subfield(self):
        """The new sub-field appears after the last line of occurred: block."""
        raw_yaml = textwrap.dedent("""\
            name: "Battle of the Trident"
            type: event.battle
            slug: battle-of-the-trident
            occurred:
              ac_year: 283
              precision: year
              basis_source: wiki-year-page
              basis_reliability: tertiary-fan
              date_confidence: tier-3""")
        result = mod.insert_narrative_first_into_yaml(raw_yaml, "agot-2")
        assert '  narrative_first: "agot-2"' in result
        # The field appears after date_confidence
        idx_date = result.index("date_confidence:")
        idx_nf = result.index("narrative_first:")
        assert idx_nf > idx_date

    def test_raises_if_no_occurred_block(self):
        """ValueError raised if occurred: block not present."""
        raw_yaml = "name: Foo\ntype: event.battle\n"
        with pytest.raises(ValueError, match="occurred"):
            mod.insert_narrative_first_into_yaml(raw_yaml, "agot-2")

    def test_only_one_narrative_first_inserted(self):
        """Calling insert again on already-modified yaml would add a duplicate.

        The idempotency check in patch_node_file_narrative_first prevents this
        from reaching insert_narrative_first_into_yaml in normal flow.
        """
        raw_yaml = textwrap.dedent("""\
            name: "Test"
            occurred:
              ac_year: 283
              date_confidence: tier-3""")
        result = mod.insert_narrative_first_into_yaml(raw_yaml, "agot-2")
        assert result.count("narrative_first:") == 1
