"""Tests for scripts/stage4-edge-temporal-scope.py.

Covers:
  - parse_frontmatter_fields: extracts chapter_number from YAML frontmatter
  - build_chapter_lookup: scans a directory tree and produces correct slug → (book_order, cn)
  - temporal_key_string: correct string format, None when either input is None
  - annotate_edge: adds book_order / chapter_number / temporal_key to an edge dict
  - window_key: book vs chapter granularity
  - same_window: equality + None handling
  - classify_incompatible_pair_window: arc vs true conflict across books / same chapter
  - find_temporal_conflicts: arc pairs classified as CROSS_WINDOW; same-chapter pairs as SAME_WINDOW
  - null temporal-key edges handled conservatively (classified SAME_WINDOW, not CROSS_WINDOW)
  - edges.jsonl is NEVER written (annotated output goes to a different path)
  - INCOMPATIBLE_PAIRS is the same table as in graph-conflict-pairs.py

Run: python3 -m pytest tests/test_stage4_edge_temporal_scope.py -q
"""

import json
import textwrap
from pathlib import Path

import pytest

from tests._helpers import load_script

mod = load_script("stage4-edge-temporal-scope.py")

# Public API under test
parse_frontmatter_fields        = mod.parse_frontmatter_fields
build_chapter_lookup            = mod.build_chapter_lookup
temporal_key_string             = mod.temporal_key_string
annotate_edge                   = mod.annotate_edge
window_key                      = mod.window_key
same_window                     = mod.same_window
classify_incompatible_pair_window = mod.classify_incompatible_pair_window
detect_temporal_conflicts       = mod.detect_temporal_conflicts
find_temporal_conflicts         = mod.find_temporal_conflicts
group_by_pair                   = mod.group_by_pair
load_edges                      = mod.load_edges
write_annotated_edges           = mod.write_annotated_edges
INCOMPATIBLE_PAIRS              = mod.INCOMPATIBLE_PAIRS
BOOK_ORDER                      = mod.BOOK_ORDER


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_edge(src: str, tgt: str, etype: str, book: str = "agot", chapter: str = "agot-test-01", **extra) -> dict:
    """Build a minimal edge dict for testing."""
    return {
        "decision": "emit_edge",
        "edge_type": etype,
        "source_slug": src,
        "target_slug": tgt,
        "evidence_ref": f"sources/chapters/{book}/{chapter}.md:10",
        "evidence_quote": f"Test quote for {etype}.",
        "evidence_book": book,
        "evidence_chapter": chapter,
        "confidence_tier": 1,
        "dup_count": 1,
        **extra,
    }


def make_annotated_edge(src: str, tgt: str, etype: str, book_order: int | None, chapter_number: int | None, **extra) -> dict:
    """Build an edge that already has temporal annotation fields."""
    book_lookup = {1: "agot", 2: "acok", 3: "asos", 4: "affc", 5: "adwd"}
    book = book_lookup.get(book_order, "agot") if book_order else "agot"
    chapter = f"{book}-test-{chapter_number:02d}" if chapter_number else "unknown"
    e = make_edge(src, tgt, etype, book=book, chapter=chapter, **extra)
    e["book_order"] = book_order
    e["chapter_number"] = chapter_number
    e["temporal_key"] = temporal_key_string(book_order, chapter_number)
    return e


def write_chapter_file(directory: Path, slug: str, book_upper: str, chapter_number: int) -> Path:
    """Write a minimal chapter markdown file with frontmatter to a tmp directory."""
    content = textwrap.dedent(f"""\
        ---
        book: {book_upper}
        chapter_number: {chapter_number}
        pov_character: TestPov
        real_identity: Test Character
        ---
        Chapter body text.
    """)
    path = directory / f"{slug}.md"
    path.write_text(content, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# parse_frontmatter_fields
# ---------------------------------------------------------------------------

class TestParseFrontmatterFields:
    def test_extracts_chapter_number(self):
        text = "---\nbook: AGOT\nchapter_number: 8\npov_character: Bran\n---\nBody."
        fields = parse_frontmatter_fields(text)
        assert fields["chapter_number"] == "8"
        assert fields["book"] == "AGOT"
        assert fields["pov_character"] == "Bran"

    def test_returns_empty_if_no_frontmatter(self):
        text = "This is just body text without frontmatter."
        fields = parse_frontmatter_fields(text)
        assert fields == {}

    def test_strips_quotes_from_values(self):
        text = '---\npov_label: "Bran I"\n---\n'
        fields = parse_frontmatter_fields(text)
        assert fields["pov_label"] == "Bran I"

    def test_multiline_frontmatter(self):
        text = "---\nbook: ASOS\nchapter_number: 42\npov_character: Jon\nfile_name: asos-jon-01.md\n---\n"
        fields = parse_frontmatter_fields(text)
        assert fields["chapter_number"] == "42"
        assert fields["pov_character"] == "Jon"

    def test_missing_chapter_number_returns_empty_string(self):
        text = "---\nbook: AGOT\npov_character: Prologue\n---\n"
        fields = parse_frontmatter_fields(text)
        assert "chapter_number" not in fields


# ---------------------------------------------------------------------------
# build_chapter_lookup
# ---------------------------------------------------------------------------

class TestBuildChapterLookup:
    def test_resolves_agot_chapter(self, tmp_path):
        """A valid agot chapter file must produce (book_order=1, chapter_number=N)."""
        agot_dir = tmp_path / "agot"
        agot_dir.mkdir()
        write_chapter_file(agot_dir, "agot-bran-01", "AGOT", 2)

        lookup, resolved, unresolved = build_chapter_lookup(tmp_path)
        assert "agot-bran-01" in lookup
        assert lookup["agot-bran-01"] == (1, 2)
        assert resolved == 1
        assert unresolved == 0

    def test_book_order_matches_series_order(self, tmp_path):
        """agot < acok < asos < affc < adwd."""
        for book_slug, upper, cn in [("agot", "AGOT", 1), ("acok", "ACOK", 1),
                                      ("asos", "ASOS", 1), ("affc", "AFFC", 1),
                                      ("adwd", "ADWD", 1)]:
            d = tmp_path / book_slug
            d.mkdir()
            write_chapter_file(d, f"{book_slug}-test-01", upper, cn)

        lookup, resolved, unresolved = build_chapter_lookup(tmp_path)
        assert lookup["agot-test-01"][0] == 1
        assert lookup["acok-test-01"][0] == 2
        assert lookup["asos-test-01"][0] == 3
        assert lookup["affc-test-01"][0] == 4
        assert lookup["adwd-test-01"][0] == 5
        assert resolved == 5
        assert unresolved == 0

    def test_missing_chapter_number_counts_as_unresolved(self, tmp_path):
        """A file without chapter_number in frontmatter yields (None, None)."""
        agot_dir = tmp_path / "agot"
        agot_dir.mkdir()
        content = "---\nbook: AGOT\npov_character: Prologue\n---\nBody."
        (agot_dir / "agot-prologue.md").write_text(content, encoding="utf-8")

        lookup, resolved, unresolved = build_chapter_lookup(tmp_path)
        assert lookup["agot-prologue"] == (None, None)
        assert resolved == 0
        assert unresolved == 1

    def test_empty_chapters_root(self, tmp_path):
        lookup, resolved, unresolved = build_chapter_lookup(tmp_path)
        assert lookup == {}
        assert resolved == 0
        assert unresolved == 0

    def test_unknown_book_directory_ignored(self, tmp_path):
        """Directories not in BOOK_ORDER (e.g. 'thk') are not scanned."""
        thk_dir = tmp_path / "thk"
        thk_dir.mkdir()
        write_chapter_file(thk_dir, "thk-dunk-01", "THK", 1)

        lookup, resolved, unresolved = build_chapter_lookup(tmp_path)
        assert "thk-dunk-01" not in lookup
        assert resolved == 0
        assert unresolved == 0

    def test_multiple_chapters_same_book(self, tmp_path):
        agot_dir = tmp_path / "agot"
        agot_dir.mkdir()
        write_chapter_file(agot_dir, "agot-bran-01", "AGOT", 2)
        write_chapter_file(agot_dir, "agot-jon-01", "AGOT", 5)
        write_chapter_file(agot_dir, "agot-tyrion-01", "AGOT", 9)

        lookup, resolved, _ = build_chapter_lookup(tmp_path)
        assert lookup["agot-bran-01"] == (1, 2)
        assert lookup["agot-jon-01"] == (1, 5)
        assert lookup["agot-tyrion-01"] == (1, 9)
        assert resolved == 3


# ---------------------------------------------------------------------------
# temporal_key_string
# ---------------------------------------------------------------------------

class TestTemporalKeyString:
    def test_valid_book_1_chapter_8(self):
        assert temporal_key_string(1, 8) == "b1-c008"

    def test_valid_book_5_chapter_73(self):
        assert temporal_key_string(5, 73) == "b5-c073"

    def test_none_book_order_returns_none(self):
        assert temporal_key_string(None, 8) is None

    def test_none_chapter_number_returns_none(self):
        assert temporal_key_string(1, None) is None

    def test_both_none_returns_none(self):
        assert temporal_key_string(None, None) is None

    def test_zero_pads_chapter_to_three_digits(self):
        assert temporal_key_string(2, 1) == "b2-c001"
        assert temporal_key_string(3, 99) == "b3-c099"
        assert temporal_key_string(4, 100) == "b4-c100"


# ---------------------------------------------------------------------------
# annotate_edge
# ---------------------------------------------------------------------------

class TestAnnotateEdge:
    def test_resolves_known_chapter(self):
        edge = make_edge("arya-stark", "jon-snow", "LOVES", book="agot", chapter="agot-arya-01")
        lookup = {"agot-arya-01": (1, 5)}
        result = annotate_edge(edge, lookup)
        assert result["book_order"] == 1
        assert result["chapter_number"] == 5
        assert result["temporal_key"] == "b1-c005"

    def test_unknown_chapter_slug_yields_null_key(self):
        edge = make_edge("x", "y", "LOVES", chapter="no-such-chapter")
        lookup = {}
        result = annotate_edge(edge, lookup)
        assert result["book_order"] is None
        assert result["chapter_number"] is None
        assert result["temporal_key"] is None

    def test_original_edge_fields_preserved(self):
        edge = make_edge("a", "b", "TRUSTS", chapter="agot-a-01")
        lookup = {"agot-a-01": (1, 3)}
        result = annotate_edge(edge, lookup)
        assert result["edge_type"] == "TRUSTS"
        assert result["source_slug"] == "a"
        assert result["target_slug"] == "b"

    def test_does_not_mutate_original_edge(self):
        edge = make_edge("a", "b", "HATES", chapter="agot-a-01")
        original_keys = set(edge.keys())
        lookup = {"agot-a-01": (1, 10)}
        result = annotate_edge(edge, lookup)
        # Original dict should be unchanged
        assert set(edge.keys()) == original_keys
        assert "temporal_key" not in edge
        # Annotated result has new fields
        assert "temporal_key" in result


# ---------------------------------------------------------------------------
# window_key
# ---------------------------------------------------------------------------

class TestWindowKey:
    def test_book_window_uses_evidence_book(self):
        edge = make_annotated_edge("a", "b", "LOVES", book_order=1, chapter_number=5)
        assert window_key(edge, "book") == "agot"

    def test_chapter_window_uses_temporal_key(self):
        edge = make_annotated_edge("a", "b", "LOVES", book_order=1, chapter_number=5)
        assert window_key(edge, "chapter") == "b1-c005"

    def test_chapter_window_null_key_returns_none(self):
        edge = make_edge("a", "b", "LOVES")
        edge["book_order"] = None
        edge["chapter_number"] = None
        edge["temporal_key"] = None
        assert window_key(edge, "chapter") is None

    def test_book_window_null_book_falls_back_to_book_order(self):
        """If evidence_book is absent, book window falls back to book_order."""
        edge = make_annotated_edge("a", "b", "LOVES", book_order=3, chapter_number=10)
        del edge["evidence_book"]
        result = window_key(edge, "book")
        # Should return book_order (3) since evidence_book missing
        assert result == 3


# ---------------------------------------------------------------------------
# same_window
# ---------------------------------------------------------------------------

class TestSameWindow:
    def test_equal_non_none_keys_are_same(self):
        assert same_window("agot", "agot") is True
        assert same_window("b1-c005", "b1-c005") is True

    def test_different_non_none_keys_are_not_same(self):
        assert same_window("agot", "adwd") is False
        assert same_window("b1-c005", "b5-c073") is False

    def test_none_a_is_never_same(self):
        assert same_window(None, "agot") is False

    def test_none_b_is_never_same(self):
        assert same_window("agot", None) is False

    def test_both_none_is_not_same(self):
        assert same_window(None, None) is False


# ---------------------------------------------------------------------------
# classify_incompatible_pair_window — the core temporal logic
# ---------------------------------------------------------------------------

class TestClassifyIncompatiblePairWindow:
    """Tests for classify_incompatible_pair_window(type_a, type_b, edges, window)."""

    def test_different_books_is_cross_window(self):
        """TRUSTS in AGOT + DISTRUSTS in ADWD → CROSS_WINDOW under 'book'."""
        edges = [
            make_annotated_edge("daenerys-targaryen", "jorah-mormont", "TRUSTS",
                                book_order=1, chapter_number=10),
            make_annotated_edge("daenerys-targaryen", "jorah-mormont", "DISTRUSTS",
                                book_order=5, chapter_number=20),
        ]
        result = classify_incompatible_pair_window("DISTRUSTS", "TRUSTS", edges, "book")
        assert result == "CROSS_WINDOW"

    def test_same_book_is_same_window(self):
        """TRUSTS + DISTRUSTS both in AGOT → SAME_WINDOW under 'book'."""
        edges = [
            make_annotated_edge("ned-stark", "petyr-baelish", "TRUSTS",
                                book_order=1, chapter_number=3),
            make_annotated_edge("ned-stark", "petyr-baelish", "DISTRUSTS",
                                book_order=1, chapter_number=9),
        ]
        result = classify_incompatible_pair_window("DISTRUSTS", "TRUSTS", edges, "book")
        assert result == "SAME_WINDOW"

    def test_same_chapter_is_same_window_under_chapter_granularity(self):
        """Two incompatible edges with the same temporal_key → SAME_WINDOW."""
        edges = [
            make_annotated_edge("a", "b", "LOVES", book_order=1, chapter_number=5),
            make_annotated_edge("a", "b", "HATES", book_order=1, chapter_number=5),
        ]
        result = classify_incompatible_pair_window("HATES", "LOVES", edges, "chapter")
        assert result == "SAME_WINDOW"

    def test_different_chapters_is_cross_window_under_chapter_granularity(self):
        """Same book but different chapters → CROSS_WINDOW under 'chapter'."""
        edges = [
            make_annotated_edge("a", "b", "ALLIES_WITH", book_order=1, chapter_number=5),
            make_annotated_edge("a", "b", "OPPOSES", book_order=1, chapter_number=8),
        ]
        result = classify_incompatible_pair_window("ALLIES_WITH", "OPPOSES", edges, "chapter")
        assert result == "CROSS_WINDOW"

    def test_null_temporal_key_under_chapter_window_is_conservatively_same_window(self):
        """Under --window chapter, a null temporal_key means chapter is unresolvable.
        We cannot prove the pair is CROSS_WINDOW, so we classify conservatively as SAME_WINDOW.
        """
        edges = [
            {
                "edge_type": "TRUSTS",
                "source_slug": "a", "target_slug": "b",
                "evidence_book": "agot",
                "temporal_key": None,          # unresolvable chapter
                "book_order": None, "chapter_number": None,
            },
            {
                "edge_type": "DISTRUSTS",
                "source_slug": "a", "target_slug": "b",
                "evidence_book": "adwd",
                "temporal_key": "b5-c020",
                "book_order": 5, "chapter_number": 20,
            },
        ]
        # Under 'chapter' granularity: null temporal_key → conservative SAME_WINDOW
        result = classify_incompatible_pair_window("DISTRUSTS", "TRUSTS", edges, "chapter")
        assert result == "SAME_WINDOW"

    def test_null_temporal_key_under_book_window_uses_evidence_book(self):
        """Under --window book, evidence_book is used (always present/reliable).
        A null temporal_key does NOT make it conservative under book granularity;
        the raw evidence_book field resolves the window reliably.
        """
        edges = [
            {
                "edge_type": "TRUSTS",
                "source_slug": "a", "target_slug": "b",
                "evidence_book": "agot",       # reliable even without temporal_key
                "temporal_key": None,
                "book_order": None, "chapter_number": None,
            },
            {
                "edge_type": "DISTRUSTS",
                "source_slug": "a", "target_slug": "b",
                "evidence_book": "adwd",
                "temporal_key": "b5-c020",
                "book_order": 5, "chapter_number": 20,
            },
        ]
        # Under 'book' granularity: agot != adwd → CROSS_WINDOW (not conservative SAME_WINDOW)
        result = classify_incompatible_pair_window("DISTRUSTS", "TRUSTS", edges, "book")
        assert result == "CROSS_WINDOW"

    def test_arc_across_all_five_books(self):
        """Cross-book arc: allies early, opposes late — must be CROSS_WINDOW."""
        edges = [
            make_annotated_edge("robb-stark", "walder-frey", "ALLIES_WITH",
                                book_order=2, chapter_number=10),
            make_annotated_edge("robb-stark", "walder-frey", "OPPOSES",
                                book_order=3, chapter_number=50),
        ]
        result = classify_incompatible_pair_window("ALLIES_WITH", "OPPOSES", edges, "book")
        assert result == "CROSS_WINDOW"


# ---------------------------------------------------------------------------
# detect_temporal_conflicts + find_temporal_conflicts
# ---------------------------------------------------------------------------

class TestDetectTemporalConflicts:
    def test_cross_book_arc_is_cross_window(self):
        """Daenerys/Jorah arc across AGOT→ADWD must be CROSS_WINDOW."""
        pair = frozenset({"daenerys-targaryen", "jorah-mormont"})
        edges = [
            make_annotated_edge("daenerys-targaryen", "jorah-mormont", "TRUSTS",
                                book_order=1, chapter_number=10),
            make_annotated_edge("daenerys-targaryen", "jorah-mormont", "DISTRUSTS",
                                book_order=5, chapter_number=20),
        ]
        result = detect_temporal_conflicts(pair, edges, "book")
        assert result is not None
        assert result["overall_classification"] == "CROSS_WINDOW"

    def test_same_book_conflict_is_same_window(self):
        """Two incompatible edges in the same book → SAME_WINDOW."""
        pair = frozenset({"ned-stark", "petyr-baelish"})
        edges = [
            make_annotated_edge("ned-stark", "petyr-baelish", "TRUSTS",
                                book_order=1, chapter_number=3),
            make_annotated_edge("ned-stark", "petyr-baelish", "DISTRUSTS",
                                book_order=1, chapter_number=9),
        ]
        result = detect_temporal_conflicts(pair, edges, "book")
        assert result is not None
        assert result["overall_classification"] == "SAME_WINDOW"

    def test_no_incompatible_types_returns_none(self):
        pair = frozenset({"jon-snow", "ghost"})
        edges = [
            make_annotated_edge("jon-snow", "ghost", "BONDED_TO",
                                book_order=1, chapter_number=3),
        ]
        result = detect_temporal_conflicts(pair, edges, "book")
        assert result is None

    def test_result_contains_expected_fields(self):
        pair = frozenset({"a", "b"})
        edges = [
            make_annotated_edge("a", "b", "LOVES", book_order=1, chapter_number=5),
            make_annotated_edge("a", "b", "HATES", book_order=1, chapter_number=5),
        ]
        result = detect_temporal_conflicts(pair, edges, "book")
        assert result is not None
        for field in ("slug_a", "slug_b", "overall_classification", "window",
                      "classified_incompatible_pairs", "all_edge_types_on_pair",
                      "total_edges_on_pair", "conflict_edges"):
            assert field in result, f"Missing field: {field}"

    def test_conflict_edges_include_temporal_key_field(self):
        pair = frozenset({"a", "b"})
        edges = [
            make_annotated_edge("a", "b", "LOVES", book_order=1, chapter_number=5),
            make_annotated_edge("a", "b", "HATES", book_order=1, chapter_number=5),
        ]
        result = detect_temporal_conflicts(pair, edges, "book")
        assert result is not None
        for ce in result["conflict_edges"]:
            assert "temporal_key" in ce


class TestFindTemporalConflicts:
    def test_cross_book_arc_classified_as_cross_window(self):
        """An arc pair (TRUSTS early, DISTRUSTS late) must produce CROSS_WINDOW."""
        grouped = {
            frozenset({"daenerys-targaryen", "jorah-mormont"}): [
                make_annotated_edge("daenerys-targaryen", "jorah-mormont", "TRUSTS",
                                    book_order=1, chapter_number=10),
                make_annotated_edge("daenerys-targaryen", "jorah-mormont", "DISTRUSTS",
                                    book_order=5, chapter_number=20),
            ]
        }
        conflicts = find_temporal_conflicts(grouped, "book")
        assert len(conflicts) == 1
        assert conflicts[0]["overall_classification"] == "CROSS_WINDOW"

    def test_same_book_conflict_is_same_window(self):
        grouped = {
            frozenset({"ned-stark", "petyr-baelish"}): [
                make_annotated_edge("ned-stark", "petyr-baelish", "TRUSTS",
                                    book_order=1, chapter_number=3),
                make_annotated_edge("ned-stark", "petyr-baelish", "DISTRUSTS",
                                    book_order=1, chapter_number=9),
            ]
        }
        conflicts = find_temporal_conflicts(grouped, "book")
        assert len(conflicts) == 1
        assert conflicts[0]["overall_classification"] == "SAME_WINDOW"

    def test_true_conflicts_sorted_before_arcs(self):
        """find_temporal_conflicts must return SAME_WINDOW records before CROSS_WINDOW."""
        grouped = {
            # Arc (cross-window)
            frozenset({"daenerys-targaryen", "jorah-mormont"}): [
                make_annotated_edge("daenerys-targaryen", "jorah-mormont", "TRUSTS",
                                    book_order=1, chapter_number=10),
                make_annotated_edge("daenerys-targaryen", "jorah-mormont", "DISTRUSTS",
                                    book_order=5, chapter_number=20),
            ],
            # True conflict (same-window)
            frozenset({"ned-stark", "petyr-baelish"}): [
                make_annotated_edge("ned-stark", "petyr-baelish", "TRUSTS",
                                    book_order=1, chapter_number=3),
                make_annotated_edge("ned-stark", "petyr-baelish", "DISTRUSTS",
                                    book_order=1, chapter_number=9),
            ],
        }
        conflicts = find_temporal_conflicts(grouped, "book")
        assert len(conflicts) == 2
        assert conflicts[0]["overall_classification"] == "SAME_WINDOW"
        assert conflicts[1]["overall_classification"] == "CROSS_WINDOW"

    def test_clean_pairs_not_flagged(self):
        grouped = {
            frozenset({"jon-snow", "ghost"}): [
                make_annotated_edge("jon-snow", "ghost", "BONDED_TO",
                                    book_order=1, chapter_number=1),
            ]
        }
        conflicts = find_temporal_conflicts(grouped, "book")
        assert conflicts == []

    def test_null_temporal_key_under_chapter_window_classified_conservatively(self):
        """Under --window chapter: a null temporal_key cannot prove CROSS_WINDOW → SAME_WINDOW."""
        pair = frozenset({"x", "y"})
        grouped = {
            pair: [
                {
                    "edge_type": "TRUSTS",
                    "source_slug": "x", "target_slug": "y",
                    "evidence_book": "agot",
                    "evidence_chapter": "unknown-slug",
                    "evidence_ref": "?",
                    "evidence_quote": "",
                    "confidence_tier": 1,
                    "temporal_key": None,          # unresolvable
                    "book_order": None, "chapter_number": None,
                },
                {
                    "edge_type": "DISTRUSTS",
                    "source_slug": "x", "target_slug": "y",
                    "evidence_book": "adwd",
                    "evidence_chapter": "adwd-x-01",
                    "evidence_ref": "sources/chapters/adwd/adwd-x-01.md:5",
                    "evidence_quote": "",
                    "confidence_tier": 1,
                    "temporal_key": "b5-c010",
                    "book_order": 5, "chapter_number": 10,
                },
            ]
        }
        # Under 'chapter' granularity: null key → conservative SAME_WINDOW
        conflicts = find_temporal_conflicts(grouped, "chapter")
        assert len(conflicts) == 1
        assert conflicts[0]["overall_classification"] == "SAME_WINDOW"

    def test_null_temporal_key_under_book_window_uses_evidence_book_field(self):
        """Under --window book: evidence_book is the reliable raw field.
        Different evidence_book values → CROSS_WINDOW even if temporal_key is null.
        """
        pair = frozenset({"x", "y"})
        grouped = {
            pair: [
                {
                    "edge_type": "TRUSTS",
                    "source_slug": "x", "target_slug": "y",
                    "evidence_book": "agot",
                    "evidence_chapter": "unknown-slug",
                    "evidence_ref": "?",
                    "evidence_quote": "",
                    "confidence_tier": 1,
                    "temporal_key": None,
                    "book_order": None, "chapter_number": None,
                },
                {
                    "edge_type": "DISTRUSTS",
                    "source_slug": "x", "target_slug": "y",
                    "evidence_book": "adwd",
                    "evidence_chapter": "adwd-x-01",
                    "evidence_ref": "sources/chapters/adwd/adwd-x-01.md:5",
                    "evidence_quote": "",
                    "confidence_tier": 1,
                    "temporal_key": "b5-c010",
                    "book_order": 5, "chapter_number": 10,
                },
            ]
        }
        # Under 'book' granularity: agot != adwd → CROSS_WINDOW
        conflicts = find_temporal_conflicts(grouped, "book")
        assert len(conflicts) == 1
        assert conflicts[0]["overall_classification"] == "CROSS_WINDOW"

    def test_chapter_window_finer_than_book(self):
        """Under 'chapter' granularity, edges in same book but different chapters = CROSS_WINDOW."""
        grouped = {
            frozenset({"a", "b"}): [
                make_annotated_edge("a", "b", "ALLIES_WITH", book_order=2, chapter_number=5),
                make_annotated_edge("a", "b", "OPPOSES",     book_order=2, chapter_number=9),
            ]
        }
        # Under 'book' → same book → SAME_WINDOW
        book_conflicts = find_temporal_conflicts(grouped, "book")
        assert book_conflicts[0]["overall_classification"] == "SAME_WINDOW"
        # Under 'chapter' → different chapters → CROSS_WINDOW
        chap_conflicts = find_temporal_conflicts(grouped, "chapter")
        assert chap_conflicts[0]["overall_classification"] == "CROSS_WINDOW"


# ---------------------------------------------------------------------------
# INCOMPATIBLE_PAIRS constant — same table as graph-conflict-pairs.py
# ---------------------------------------------------------------------------

class TestIncompatiblePairsConsistency:
    def test_same_pairs_as_conflict_pairs_script(self):
        """The INCOMPATIBLE_PAIRS table must be identical to graph-conflict-pairs.py's."""
        conflict_pairs_mod = load_script("graph-conflict-pairs.py")
        assert INCOMPATIBLE_PAIRS == conflict_pairs_mod.INCOMPATIBLE_PAIRS

    def test_is_set_of_frozensets(self):
        assert isinstance(INCOMPATIBLE_PAIRS, set)
        for item in INCOMPATIBLE_PAIRS:
            assert isinstance(item, frozenset)

    def test_all_expected_pairs_present(self):
        assert frozenset({"LOVES", "HATES"}) in INCOMPATIBLE_PAIRS
        assert frozenset({"ALLIES_WITH", "OPPOSES"}) in INCOMPATIBLE_PAIRS
        assert frozenset({"TRUSTS", "DISTRUSTS"}) in INCOMPATIBLE_PAIRS
        assert frozenset({"PROTECTS", "ATTACKS"}) in INCOMPATIBLE_PAIRS
        assert frozenset({"PROTECTS", "ASSAULTS"}) in INCOMPATIBLE_PAIRS


# ---------------------------------------------------------------------------
# edges.jsonl is NEVER written (safety guard)
# ---------------------------------------------------------------------------

class TestEdgesJSONLNotMutated:
    def test_write_annotated_does_not_write_to_edges_jsonl(self, tmp_path):
        """write_annotated_edges must write to the specified path, not edges.jsonl."""
        canonical = tmp_path / "graph" / "edges" / "edges.jsonl"
        canonical.parent.mkdir(parents=True)
        canonical.write_text("{}\n", encoding="utf-8")
        original_mtime = canonical.stat().st_mtime

        out_path = tmp_path / "annotated.jsonl"
        annotated = [
            make_annotated_edge("a", "b", "LOVES", book_order=1, chapter_number=5),
        ]
        write_annotated_edges(annotated, out_path)

        # Canonical file untouched
        assert canonical.stat().st_mtime == original_mtime
        # Annotated output written
        assert out_path.exists()
        rows = [json.loads(l) for l in out_path.read_text().splitlines() if l.strip()]
        assert len(rows) == 1
        assert rows[0]["temporal_key"] == "b1-c005"

    def test_annotated_output_contains_temporal_fields(self, tmp_path):
        out_path = tmp_path / "annotated.jsonl"
        annotated = [
            make_annotated_edge("a", "b", "TRUSTS", book_order=3, chapter_number=12),
        ]
        write_annotated_edges(annotated, out_path)
        row = json.loads(out_path.read_text().splitlines()[0])
        assert row["book_order"] == 3
        assert row["chapter_number"] == 12
        assert row["temporal_key"] == "b3-c012"


# ---------------------------------------------------------------------------
# load_edges (JSONL I/O) — verify it doesn't mutate source
# ---------------------------------------------------------------------------

class TestLoadEdgesReadOnly:
    def test_load_does_not_modify_file(self, tmp_path):
        edge = make_edge("arya-stark", "jon-snow", "LOVES")
        f = tmp_path / "edges.jsonl"
        f.write_text(json.dumps(edge) + "\n", encoding="utf-8")
        original_mtime = f.stat().st_mtime
        loaded = load_edges(f)
        assert f.stat().st_mtime == original_mtime
        assert len(loaded) == 1

    def test_skips_blank_lines(self, tmp_path):
        edge = make_edge("a", "b", "LOVES")
        f = tmp_path / "edges.jsonl"
        f.write_text("\n" + json.dumps(edge) + "\n\n", encoding="utf-8")
        loaded = load_edges(f)
        assert len(loaded) == 1


# ---------------------------------------------------------------------------
# BOOK_ORDER constant sanity
# ---------------------------------------------------------------------------

class TestBookOrder:
    def test_five_books_in_order(self):
        assert BOOK_ORDER["agot"] == 1
        assert BOOK_ORDER["acok"] == 2
        assert BOOK_ORDER["asos"] == 3
        assert BOOK_ORDER["affc"] == 4
        assert BOOK_ORDER["adwd"] == 5

    def test_books_are_monotonically_increasing(self):
        order = sorted(BOOK_ORDER.values())
        assert order == list(range(1, len(order) + 1))
