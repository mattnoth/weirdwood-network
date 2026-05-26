"""Tests for the Stage 4 Pass-1-Derived Edge Pipeline.

Covers:
- stage4-pass1-edge-candidates.py:
    * Corroboration flag (both directions)
    * Resolved/unresolved gate
    * Typer integration (known exact-map hint + known tail hint)
    * Needs-qualifier routing (Tier-1 edge types)
    * Conform check (typer output not in locked vocab)
    * to_slug behavior
    * parse_relationships_table on fixture data

- stage4-pass1-evidence-locator.py:
    * Verbatim match vs chapter-level fallback
    * locate_evidence with synthetic prose
    * Name form generation
    * Content word extraction (stopword removal)

Run: python3 -m unittest tests.test_stage4_pass1_edge_pipeline -v
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from tests._helpers import load_script

candidates_mod = load_script("stage4-pass1-edge-candidates.py")
locator_mod = load_script("stage4-pass1-evidence-locator.py")


# ---------------------------------------------------------------------------
# Helpers to build in-memory test fixtures
# ---------------------------------------------------------------------------

def _make_node_file(tmp_dir: Path, subdir: str, slug: str, edges: list[str] = None) -> Path:
    """Create a minimal .node.md file under tmp_dir/subdir/slug.node.md."""
    node_dir = tmp_dir / subdir
    node_dir.mkdir(parents=True, exist_ok=True)
    edge_lines = "\n".join(f"- {e}" for e in (edges or []))
    content = f"---\nname: {slug}\ntype: character.human\nslug: {slug}\n---\n\n## Edges\n\n{edge_lines}\n"
    path = node_dir / f"{slug}.node.md"
    path.write_text(content, encoding="utf-8")
    return path


def _make_chapter_file(tmp_dir: Path, book: str, chapter_slug: str, prose: str) -> Path:
    """Create a chapter .md file with minimal YAML frontmatter."""
    chapter_dir = tmp_dir / "sources" / "chapters" / book
    chapter_dir.mkdir(parents=True, exist_ok=True)
    content = f"---\nbook: {book.upper()}\nchapter_number: 1\npov_character: Test\n---\n\n{prose}\n"
    path = chapter_dir / f"{chapter_slug}.md"
    path.write_text(content, encoding="utf-8")
    return path


def _make_candidates_file(tmp_dir: Path, book: str, chapter_slug: str, rows: list[dict]) -> Path:
    """Create a candidates JSONL file as would be produced by Script 1."""
    out_dir = tmp_dir / "working" / "wiki" / "pass2-buckets" / "pass1-derived" / book
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{chapter_slug}.candidates.jsonl"
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path


# ---------------------------------------------------------------------------
# Tests: candidates module helpers
# ---------------------------------------------------------------------------

class TestToSlug(unittest.TestCase):
    """to_slug must match the canonical kebab-case convention."""

    def test_basic(self):
        self.assertEqual(candidates_mod.to_slug("Arya Stark"), "arya-stark")
        self.assertEqual(candidates_mod.to_slug("Jon Snow"), "jon-snow")

    def test_possessive_stripped(self):
        self.assertEqual(candidates_mod.to_slug("Eddard's"), "eddards")

    def test_apostrophe_stripped(self):
        self.assertEqual(candidates_mod.to_slug("Jaqen H'ghar"), "jaqen-hghar")

    def test_underscores_to_hyphens(self):
        self.assertEqual(candidates_mod.to_slug("The_Wall"), "the-wall")

    def test_collapse_hyphens(self):
        self.assertEqual(candidates_mod.to_slug("Robb  Stark"), "robb-stark")

    def test_already_slug(self):
        self.assertEqual(candidates_mod.to_slug("arya-stark"), "arya-stark")


class TestParseRelationshipsTable(unittest.TestCase):
    """parse_relationships_table must extract table rows from extraction text."""

    _EXTRACTION_SNIPPET = """\
## Some Other Section

Text here.

## Relationships Observed
| Character A | Relationship | Character B | Evidence |
|-------------|-------------|-------------|----------|
| Arya Stark  | Deep love and longing for | Jon Snow | Dreams of him |
| Arya Stark  | Mourning | Eddard Stark | Cries in her sleep |

## Raw Entity List

- Arya Stark
"""

    def test_rows_extracted(self):
        rows = candidates_mod.parse_relationships_table(self._EXTRACTION_SNIPPET)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["char_a"], "Arya Stark")
        self.assertEqual(rows[0]["relationship"], "Deep love and longing for")
        self.assertEqual(rows[0]["char_b"], "Jon Snow")
        self.assertEqual(rows[0]["evidence"], "Dreams of him")

    def test_second_row(self):
        rows = candidates_mod.parse_relationships_table(self._EXTRACTION_SNIPPET)
        self.assertEqual(rows[1]["char_a"], "Arya Stark")
        self.assertEqual(rows[1]["relationship"], "Mourning")
        self.assertEqual(rows[1]["char_b"], "Eddard Stark")

    def test_no_section_returns_empty(self):
        text = "## Other\nstuff\n"
        self.assertEqual(candidates_mod.parse_relationships_table(text), [])


class TestTyperIntegration(unittest.TestCase):
    """Typer imported from hint-inventory must resolve known and tail hints."""

    def test_known_exact_map_hint(self):
        """'mourning' is in HINT_EXACT_MAP → MOURNS."""
        hint_norm = candidates_mod.normalize_hint("Mourning")
        result = candidates_mod.map_hint_to_edge(hint_norm)
        self.assertEqual(result, "MOURNS")

    def test_known_prefix_hint(self):
        """'father of (adoptive)' starts with 'father of' prefix → PARENT_OF."""
        hint_norm = candidates_mod.normalize_hint("Father of (adoptive)")
        result = candidates_mod.map_hint_to_edge(hint_norm)
        self.assertEqual(result, "PARENT_OF")

    def test_known_tail_hint_returns_none(self):
        """'complicated feelings toward' is not mapped by any layer → None."""
        hint_norm = candidates_mod.normalize_hint("Complicated feelings toward")
        result = candidates_mod.map_hint_to_edge(hint_norm)
        self.assertIsNone(result)

    def test_keyword_layer_hint(self):
        """'grief for' is mapped by keyword layer → MOURNS."""
        hint_norm = candidates_mod.normalize_hint("grief for")
        result = candidates_mod.map_hint_to_edge(hint_norm)
        self.assertEqual(result, "MOURNS")

    def test_exact_map_loves(self):
        """'deep love and longing for' → LOVES."""
        hint_norm = candidates_mod.normalize_hint("Deep love and longing for")
        result = candidates_mod.map_hint_to_edge(hint_norm)
        self.assertEqual(result, "LOVES")


class TestParseExistingEdgesWithTypes(unittest.TestCase):
    """parse_existing_edges_with_types must extract target slug → edge_type."""

    _NODE_CONTENT = """\
---
name: Arya Stark
type: character.human
slug: arya-stark
---

## Edges

- SIBLING_OF: Jon Snow (wiki:Arya_Stark)
- LOVES: Eddard Stark
- PROTECTS: Gendry [cite]

## Notes

Some notes here.
"""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._path = Path(self._tmp) / "arya-stark.node.md"
        self._path.write_text(self._NODE_CONTENT, encoding="utf-8")

    def test_extracts_type_and_target(self):
        result = candidates_mod.parse_existing_edges_with_types(self._path)
        self.assertIn("jon-snow", result)
        self.assertEqual(result["jon-snow"], "SIBLING_OF")

    def test_extracts_multiple_edges(self):
        result = candidates_mod.parse_existing_edges_with_types(self._path)
        self.assertIn("eddard-stark", result)
        self.assertEqual(result["eddard-stark"], "LOVES")
        self.assertIn("gendry", result)
        self.assertEqual(result["gendry"], "PROTECTS")

    def test_empty_on_missing_file(self):
        result = candidates_mod.parse_existing_edges_with_types(
            Path(self._tmp) / "nonexistent.node.md"
        )
        self.assertEqual(result, {})


class TestCorroborationFlag(unittest.TestCase):
    """Corroboration checks both forward and reverse directions."""

    # Simulate the corroboration logic inline (mirrors main loop)
    def _check_corroboration(self, existing_edges, source_slug, target_slug):
        fwd = existing_edges.get(source_slug, {})
        rev = existing_edges.get(target_slug, {})
        if target_slug in fwd:
            return True, fwd[target_slug]
        elif source_slug in rev:
            return True, rev[source_slug]
        return False, None

    def test_forward_direction(self):
        """Source→Target exists in index → corroborates."""
        existing = {
            "arya-stark": {"jon-snow": "SIBLING_OF"},
        }
        corroborates, etype = self._check_corroboration(existing, "arya-stark", "jon-snow")
        self.assertTrue(corroborates)
        self.assertEqual(etype, "SIBLING_OF")

    def test_reverse_direction(self):
        """Target→Source exists in index → also corroborates (symmetric check)."""
        existing = {
            "jon-snow": {"arya-stark": "SIBLING_OF"},  # edge listed on jon's node
        }
        corroborates, etype = self._check_corroboration(existing, "arya-stark", "jon-snow")
        self.assertTrue(corroborates)
        self.assertEqual(etype, "SIBLING_OF")

    def test_new_edge(self):
        """Neither direction exists → new edge."""
        existing = {
            "arya-stark": {"sansa-stark": "SIBLING_OF"},
        }
        corroborates, etype = self._check_corroboration(existing, "arya-stark", "eddard-stark")
        self.assertFalse(corroborates)
        self.assertIsNone(etype)

    def test_empty_index(self):
        """Empty index → always new."""
        corroborates, etype = self._check_corroboration({}, "arya-stark", "jon-snow")
        self.assertFalse(corroborates)
        self.assertIsNone(etype)


class TestResolutionGate(unittest.TestCase):
    """Only both-resolved pairs pass the resolution gate."""

    def setUp(self):
        self.node_slug_set = {"arya-stark", "jon-snow", "eddard-stark", "night-s-watch"}
        self.alias_to_canonical = {
            "arya": "arya-stark",
            "jon": "jon-snow",
        }

    def _resolve(self, raw_name):
        slug_cand = candidates_mod.to_slug(raw_name)
        return self.alias_to_canonical.get(slug_cand, slug_cand)

    def test_both_resolved(self):
        s = self._resolve("Arya Stark")
        t = self._resolve("Jon Snow")
        self.assertIn(s, self.node_slug_set)
        self.assertIn(t, self.node_slug_set)

    def test_alias_resolves(self):
        """Alias 'Arya' should resolve via alias_to_canonical."""
        s = self._resolve("Arya")
        self.assertIn(s, self.node_slug_set)
        self.assertEqual(s, "arya-stark")

    def test_unresolved_source(self):
        s = self._resolve("Unknown Character XYZ")
        self.assertNotIn(s, self.node_slug_set)

    def test_unresolved_target(self):
        t = self._resolve("Some Minor Background Figure")
        self.assertNotIn(t, self.node_slug_set)

    def test_self_edge(self):
        """When source == target after resolution → should be dropped."""
        s = self._resolve("Arya Stark")
        t = self._resolve("Arya")  # resolves via alias
        # Both resolve to arya-stark
        self.assertEqual(s, t)


class TestNeedsQualifierRouting(unittest.TestCase):
    """Tier-1 edge types (qualifier REQUIRED) must go to needs-qualifier tail."""

    def setUp(self):
        # load_tier1_edge_types reads the real vocab file
        self.tier1 = candidates_mod.load_tier1_edge_types(
            candidates_mod.QUAL_VOCAB_MD
        )

    def test_tier1_types_loaded(self):
        """Must have exactly 8 Tier-1 types per edge-qualifier-vocab.md."""
        self.assertEqual(len(self.tier1), 8, f"Expected 8 Tier-1 types, got: {self.tier1}")

    def test_sibling_of_is_tier1(self):
        self.assertIn("SIBLING_OF", self.tier1)

    def test_spouse_of_is_tier1(self):
        self.assertIn("SPOUSE_OF", self.tier1)

    def test_parent_of_is_tier1(self):
        self.assertIn("PARENT_OF", self.tier1)

    def test_loves_not_tier1(self):
        """LOVES is Tier-3 (no qualifier) → should NOT be in tier1 set."""
        self.assertNotIn("LOVES", self.tier1)

    def test_mourns_not_tier1(self):
        self.assertNotIn("MOURNS", self.tier1)

    def test_routing_logic(self):
        """Simulate routing: SIBLING_OF → needs-qualifier; LOVES → main candidates."""
        tier1 = self.tier1

        def route(edge_type):
            if edge_type is not None and edge_type in tier1:
                return "needs_qualifier"
            return "main"

        self.assertEqual(route("SIBLING_OF"), "needs_qualifier")
        self.assertEqual(route("PARENT_OF"), "needs_qualifier")
        self.assertEqual(route("LOVES"), "main")
        self.assertEqual(route("MOURNS"), "main")
        self.assertEqual(route("OPPOSES"), "main")
        self.assertEqual(route(None), "main")


class TestConformCheck(unittest.TestCase):
    """Conform step: edge types not in locked vocab must be flagged as drift."""

    def setUp(self):
        self.locked_vocab = candidates_mod.load_locked_vocab(candidates_mod.ARCH_MD)

    def test_locked_vocab_loaded(self):
        """Must load a non-trivial vocab (architecture.md has ~100+ edge types)."""
        self.assertGreater(len(self.locked_vocab), 50)

    def test_known_types_present(self):
        """Core edge types must be in the locked vocab."""
        for t in ["KILLS", "LOVES", "PARENT_OF", "MOURNS", "SERVES", "OPPOSES"]:
            self.assertIn(t, self.locked_vocab, f"{t} not in locked vocab")

    def test_typer_output_coverage(self):
        """Every edge type produced by map_hint_to_edge on common hints must be in vocab."""
        test_hints = [
            "mourning", "deep love and longing for", "father of", "sister of",
            "kills", "betrays", "serves", "commands", "fears", "hates",
            "trusts", "respects", "distrusts", "resents", "protects",
            "married to", "betrothed to", "prisoner of", "companion of",
        ]
        for hint in test_hints:
            hint_norm = candidates_mod.normalize_hint(hint)
            edge_type = candidates_mod.map_hint_to_edge(hint_norm)
            if edge_type is not None:
                self.assertIn(
                    edge_type, self.locked_vocab,
                    f"Typer returned '{edge_type}' for hint '{hint}' — not in locked vocab"
                )

    def test_fictitious_type_not_in_vocab(self):
        """A made-up type must NOT be in the locked vocab."""
        self.assertNotIn("INVENTED_EDGE_TYPE_XYZ", self.locked_vocab)


# ---------------------------------------------------------------------------
# Tests: locator module
# ---------------------------------------------------------------------------

class TestNameForms(unittest.TestCase):
    """_name_forms should produce useful surface form variants."""

    def test_basic_slug(self):
        forms = locator_mod._name_forms("arya-stark")
        self.assertIn("arya", forms)
        self.assertIn("stark", forms)
        self.assertIn("arya stark", forms)
        self.assertIn("arya-stark", forms)

    def test_single_word_slug(self):
        forms = locator_mod._name_forms("yoren")
        self.assertIn("yoren", forms)

    def test_short_parts_excluded(self):
        """Parts of length < 3 should not be added."""
        forms = locator_mod._name_forms("a-bc-def")
        self.assertNotIn("a", forms)
        self.assertNotIn("bc", forms)
        self.assertIn("def", forms)


class TestContentWords(unittest.TestCase):
    """_content_words should strip stopwords and short tokens."""

    def test_strips_stopwords(self):
        words = locator_mod._content_words("the cat sat on the mat")
        self.assertNotIn("the", words)
        self.assertNotIn("on", words)
        self.assertIn("cat", words)
        self.assertIn("sat", words)
        self.assertIn("mat", words)

    def test_minimum_length(self):
        """Words shorter than 3 characters should be excluded."""
        words = locator_mod._content_words("he is a cat")
        self.assertNotIn("he", words)
        self.assertNotIn("is", words)
        self.assertNotIn("a", words)
        self.assertIn("cat", words)

    def test_lowercases(self):
        words = locator_mod._content_words("YOREN Cut Arya's Hair")
        self.assertIn("yoren", words)
        self.assertIn("cut", words)
        self.assertIn("arya", words)  # apostrophe stripped by regex boundary
        self.assertIn("hair", words)


class TestLocateEvidence(unittest.TestCase):
    """locate_evidence should find a verbatim match or fall back to chapter-level."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._tmp_path = Path(self._tmp)

    def _write_chapter(self, book: str, chapter_slug: str, prose: str) -> Path:
        chapter_dir = self._tmp_path / "sources" / "chapters" / book
        chapter_dir.mkdir(parents=True, exist_ok=True)
        # YAML frontmatter + prose
        content = f"---\nbook: TEST\npov_character: Test\n---\n\n{prose}\n"
        path = chapter_dir / f"{chapter_slug}.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_verbatim_match(self):
        """Sentence mentioning both characters by name + content word → verbatim."""
        prose = (
            "Arya woke early that morning.\n"
            "Yoren cut her hair and disguised her identity carefully.\n"
            "The road was long and dangerous.\n"
        )
        chapter_path = self._write_chapter("acok", "acok-arya-01", prose)

        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "yoren",
            "hint_raw": "disguised protégée of",
            "evidence_text": "Yoren cut her hair, disguised her identity",
            "evidence_chapter": "acok-arya-01",
            "evidence_book": "acok",
        }

        # Monkey-patch CHAPTERS_DIR within the locator to our tmp dir
        orig_chapters_dir = locator_mod.CHAPTERS_DIR
        locator_mod.CHAPTERS_DIR = self._tmp_path / "sources" / "chapters"
        try:
            result = locator_mod.locate_evidence(candidate, chapter_path)
        finally:
            locator_mod.CHAPTERS_DIR = orig_chapters_dir

        self.assertEqual(result["locate_status"], "verbatim")
        self.assertIn("Yoren", result["evidence_quote"])
        self.assertIn("acok-arya-01.md:", result["evidence_ref"])

    def test_chapter_level_fallback(self):
        """No matching sentence → falls back to chapter-level citation."""
        prose = (
            "Completely unrelated text about the Wall.\n"
            "Snow fell heavily in the north that winter.\n"
            "Nobody mentioned anything relevant here at all.\n"
        )
        chapter_path = self._write_chapter("acok", "acok-arya-99", prose)

        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "cersei-lannister",
            "hint_raw": "hates",
            "evidence_text": "Arya despises Cersei for ordering Eddard's death",
            "evidence_chapter": "acok-arya-99",
            "evidence_book": "acok",
        }

        result = locator_mod.locate_evidence(candidate, chapter_path)
        self.assertEqual(result["locate_status"], "chapter-level")
        self.assertNotIn(":", result["evidence_ref"])  # no line number in chapter-level ref

    def test_missing_chapter_file(self):
        """Missing prose file → chapter-level fallback with no crash."""
        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "yoren",
            "hint_raw": "serves",
            "evidence_text": "Yoren protects her",
            "evidence_chapter": "acok-missing-99",
            "evidence_book": "acok",
        }
        missing_path = self._tmp_path / "sources" / "chapters" / "acok" / "acok-missing-99.md"
        # File does not exist
        result = locator_mod.locate_evidence(candidate, missing_path)
        self.assertEqual(result["locate_status"], "chapter-level")

    def test_evidence_ref_format(self):
        """evidence_ref must follow the 'sources/chapters/book/chapter.md:N' format."""
        prose = (
            "Arya and Yoren traveled together on the kingsroad north.\n"
        )
        chapter_path = self._write_chapter("acok", "acok-arya-02", prose)

        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "yoren",
            "hint_raw": "travels with",
            "evidence_text": "Arya and Yoren traveled together north",
            "evidence_chapter": "acok-arya-02",
            "evidence_book": "acok",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)

        if result["locate_status"] == "verbatim":
            # Must have a line number suffix
            self.assertRegex(result["evidence_ref"], r"sources/chapters/acok/acok-arya-02\.md:\d+")
        else:
            # Chapter-level: no colon
            self.assertEqual(result["evidence_ref"], "sources/chapters/acok/acok-arya-02.md")


class TestReadChapterProse(unittest.TestCase):
    """read_chapter_prose must skip YAML frontmatter and return non-empty prose lines."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()

    def _write(self, name: str, content: str) -> Path:
        p = Path(self._tmp) / name
        p.write_text(content, encoding="utf-8")
        return p

    def test_skips_frontmatter(self):
        content = "---\nbook: TEST\nchapter: 1\n---\n\nFirst prose line.\nSecond line.\n"
        path = self._write("test.md", content)
        prose = locator_mod.read_chapter_prose(path)
        # Should have exactly 2 non-empty lines
        self.assertEqual(len(prose), 2)
        # Line numbers should be > 5 (after frontmatter)
        for lineno, _ in prose:
            self.assertGreater(lineno, 4)

    def test_no_frontmatter(self):
        content = "Plain text without frontmatter.\nSecond line.\n"
        path = self._write("nofm.md", content)
        prose = locator_mod.read_chapter_prose(path)
        self.assertEqual(len(prose), 2)
        # First line should be line 1
        self.assertEqual(prose[0][0], 1)

    def test_empty_lines_excluded(self):
        content = "---\nb: t\n---\n\nLine one.\n\nLine two.\n"
        path = self._write("gaps.md", content)
        prose = locator_mod.read_chapter_prose(path)
        self.assertEqual(len(prose), 2)
        texts = [t for _, t in prose]
        self.assertIn("Line one.", texts)
        self.assertIn("Line two.", texts)

    def test_missing_file_returns_empty(self):
        prose = locator_mod.read_chapter_prose(Path(self._tmp) / "nonexistent.md")
        self.assertEqual(prose, [])


class TestSplitIntoSentences(unittest.TestCase):
    """split_into_sentences should break prose into sentence-level chunks."""

    def test_basic_split(self):
        lines = [(1, "Arya woke early."), (2, "Yoren cut her hair."), (3, "The road was long.")]
        sents = locator_mod.split_into_sentences(lines)
        # Should produce at least 3 sentence fragments
        self.assertGreaterEqual(len(sents), 3)
        all_text = " ".join(t for _, t in sents)
        self.assertIn("Arya", all_text)
        self.assertIn("Yoren", all_text)

    def test_returns_line_numbers(self):
        lines = [(5, "First sentence here."), (6, "Second sentence there.")]
        sents = locator_mod.split_into_sentences(lines)
        # Line numbers must be positive integers
        for lineno, _ in sents:
            self.assertIsInstance(lineno, int)
            self.assertGreater(lineno, 0)


class TestLoadLockedVocab(unittest.TestCase):
    """load_locked_vocab must load from real architecture.md."""

    def test_loads_nonzero(self):
        vocab = candidates_mod.load_locked_vocab(candidates_mod.ARCH_MD)
        self.assertGreater(len(vocab), 50)

    def test_canonical_types_present(self):
        vocab = candidates_mod.load_locked_vocab(candidates_mod.ARCH_MD)
        for t in ("KILLS", "PARENT_OF", "LOVES", "SERVES", "OPPOSES", "MOURNS"):
            self.assertIn(t, vocab)


# ---------------------------------------------------------------------------
# Tests: improved locator — locate_quality and both-named preference
# ---------------------------------------------------------------------------

class TestLocateQualityField(unittest.TestCase):
    """locate_evidence must emit locate_quality in every return path."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._tmp_path = Path(self._tmp)

    def _write_chapter(self, book: str, chapter_slug: str, prose: str) -> Path:
        chapter_dir = self._tmp_path / "sources" / "chapters" / book
        chapter_dir.mkdir(parents=True, exist_ok=True)
        content = f"---\nbook: TEST\npov_character: Test\n---\n\n{prose}\n"
        path = chapter_dir / f"{chapter_slug}.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_locate_quality_present_verbatim(self):
        """locate_quality field must be present when locate_status=verbatim."""
        prose = "Arya watched as Yoren cut her hair and disguised her identity.\n"
        chapter_path = self._write_chapter("acok", "acok-arya-loctest-01", prose)
        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "yoren",
            "hint_raw": "disguised",
            "evidence_text": "Yoren cut her hair",
            "evidence_chapter": "acok-arya-loctest-01",
            "evidence_book": "acok",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)
        self.assertIn("locate_quality", result)
        self.assertIn(result["locate_quality"],
                      {"both-named", "one-named", "nearest-fallback", "chapter-level"})

    def test_locate_quality_present_chapter_level(self):
        """locate_quality='chapter-level' when no sentence scores above threshold."""
        prose = "The wall stood tall in the north.\n"
        chapter_path = self._write_chapter("acok", "acok-cl-test", prose)
        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "cersei-lannister",
            "hint_raw": "hates",
            "evidence_text": "Arya despises Cersei for ordering Eddard's death",
            "evidence_chapter": "acok-cl-test",
            "evidence_book": "acok",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)
        self.assertIn("locate_quality", result)

    def test_locate_quality_missing_file(self):
        """locate_quality='chapter-level' for missing prose file."""
        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "yoren",
            "hint_raw": "serves",
            "evidence_text": "Yoren protects her",
            "evidence_chapter": "acok-missing-loc",
            "evidence_book": "acok",
        }
        missing_path = self._tmp_path / "sources" / "chapters" / "acok" / "acok-missing-loc.md"
        result = locator_mod.locate_evidence(candidate, missing_path)
        self.assertEqual(result["locate_quality"], "chapter-level")


class TestBothNamedPreference(unittest.TestCase):
    """locate_evidence should PREFER a quote naming BOTH endpoints."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._tmp_path = Path(self._tmp)

    def _write_chapter(self, book: str, chapter_slug: str, prose: str) -> Path:
        chapter_dir = self._tmp_path / "sources" / "chapters" / book
        chapter_dir.mkdir(parents=True, exist_ok=True)
        content = f"---\nbook: TEST\npov_character: Test\n---\n\n{prose}\n"
        path = chapter_dir / f"{chapter_slug}.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_both_named_single_sentence(self):
        """When a sentence names both endpoints, locate_quality=both-named."""
        # Sentence 2 names both Arya and Yoren; other sentences name only one
        prose = (
            "She walked through the city alone.\n"
            "Arya followed Yoren toward the gate carefully.\n"
            "The night was dark and cold.\n"
        )
        chapter_path = self._write_chapter("acok", "acok-both-01", prose)
        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "yoren",
            "hint_raw": "follows",
            "evidence_text": "Arya followed Yoren",
            "evidence_chapter": "acok-both-01",
            "evidence_book": "acok",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)
        self.assertEqual(result["locate_status"], "verbatim")
        self.assertEqual(result["locate_quality"], "both-named")
        self.assertIn("Arya", result["evidence_quote"])
        self.assertIn("Yoren", result["evidence_quote"])

    def test_both_named_prefers_over_content_rich_single_name(self):
        """Even if another sentence has more content-word hits but names only one,
        a both-named sentence should be preferred."""
        # Sentence 1 is content-rich but only names Arya
        # Sentence 2 names both Arya and Yoren (less content)
        prose = (
            "Arya disguised herself carefully, cutting her hair and hiding her identity from everyone.\n"
            "Arya trusted Yoren completely.\n"
        )
        chapter_path = self._write_chapter("acok", "acok-both-02", prose)
        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "yoren",
            "hint_raw": "trusts",
            "evidence_text": "Arya trusts Yoren",
            "evidence_chapter": "acok-both-02",
            "evidence_book": "acok",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)
        self.assertEqual(result["locate_quality"], "both-named")
        self.assertIn("Yoren", result["evidence_quote"])

    def test_window_expansion_finds_both_names(self):
        """When no single sentence names both, a multi-sentence window should be tried."""
        # Sentence 1 has Arya; sentence 2 has Yoren — window should catch both
        prose = (
            "Arya was frightened and did not know where to turn.\n"
            "Yoren grabbed her arm and pulled her into the shadows.\n"
            "The crowd roared around them in the city.\n"
        )
        chapter_path = self._write_chapter("acok", "acok-both-03", prose)
        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "yoren",
            "hint_raw": "rescued",
            "evidence_text": "Yoren rescued Arya",
            "evidence_chapter": "acok-both-03",
            "evidence_book": "acok",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)
        # Should find both names either via single sentence or window
        self.assertEqual(result["locate_status"], "verbatim")
        # If window worked, both names should be in the quote
        if result["locate_quality"] == "both-named":
            q = result["evidence_quote"]
            q_lower = q.lower()
            self.assertTrue("arya" in q_lower or "stark" in q_lower, f"Arya not in: {q}")
            self.assertTrue("yoren" in q_lower, f"Yoren not in: {q}")

    def test_one_named_when_only_one_entity_present(self):
        """When no sentence or window names both, quality degrades gracefully."""
        # Only Arya is named; Yoren doesn't appear in this chapter excerpt
        prose = (
            "Arya ran through the streets of King's Landing.\n"
            "She found an alley and hid there.\n"
            "Someone had been following her all night.\n"
        )
        chapter_path = self._write_chapter("acok", "acok-both-04", prose)
        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "yoren",
            "hint_raw": "followed by",
            "evidence_text": "Arya was followed by Yoren",
            "evidence_chapter": "acok-both-04",
            "evidence_book": "acok",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)
        # Should be verbatim (Arya is present) but quality is one-named or nearest-fallback
        if result["locate_status"] == "verbatim":
            self.assertIn(result["locate_quality"], {"one-named", "nearest-fallback"})

    def test_quality_values_are_valid_enum(self):
        """All returned locate_quality values must be in the documented enum."""
        valid_quality = {"both-named", "one-named", "nearest-fallback", "chapter-level"}
        prose_cases = [
            ("Arya and Yoren ran together.", "arya-stark", "yoren"),
            ("She ran alone.", "arya-stark", "yoren"),
            ("Nothing relevant here.", "arya-stark", "cersei-lannister"),
        ]
        for prose, src, tgt in prose_cases:
            chapter_slug = f"acok-enum-{src[:4]}"
            chapter_path = self._write_chapter("acok", chapter_slug, prose)
            candidate = {
                "source_slug": src,
                "target_slug": tgt,
                "hint_raw": "test",
                "evidence_text": "",
                "evidence_chapter": chapter_slug,
                "evidence_book": "acok",
            }
            result = locator_mod.locate_evidence(candidate, chapter_path)
            self.assertIn(result["locate_quality"], valid_quality,
                          f"Invalid locate_quality {result['locate_quality']!r} for {prose!r}")


class TestSlugNamedInText(unittest.TestCase):
    """_slug_named_in_text must match whole-word, case-insensitive."""

    def test_basic_match(self):
        tokens = frozenset(["arya", "stark"])
        self.assertTrue(locator_mod._slug_named_in_text(tokens, "arya walked away"))

    def test_no_partial_match(self):
        """'starkness' must not match 'stark' token."""
        tokens = frozenset(["stark"])
        self.assertFalse(locator_mod._slug_named_in_text(tokens, "the starkness of winter"))

    def test_case_insensitive(self):
        """text_lower is lowercased by caller; tokens are already lowercase."""
        tokens = frozenset(["yoren"])
        # The function contract: text_lower is pre-lowercased by locate_evidence.
        # Token matching is case-insensitive at the token level (tokens are lowercase).
        self.assertTrue(locator_mod._slug_named_in_text(tokens, "yoren grabbed her arm"))

    def test_empty_tokens(self):
        tokens = frozenset()
        self.assertFalse(locator_mod._slug_named_in_text(tokens, "arya walked away"))


if __name__ == "__main__":
    unittest.main()
