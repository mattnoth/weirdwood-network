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
classifier_mod = load_script("stage4-tail-classifier.py")


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
        valid_quality = {
            "both-named", "one-named", "nearest-fallback", "chapter-level",
            "hint-anchored-both-named", "hint-anchored-one-named", "hint-anchored-none",
        }
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


# ---------------------------------------------------------------------------
# Tests: v3 locator — hint-verbatim, hint-fuzzy, no-fabrication rule
# ---------------------------------------------------------------------------

class TestHintVerbatimPath(unittest.TestCase):
    """locate_evidence Path A: hint-verbatim takes priority when hint contains a quoted fragment."""

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

    def test_hint_verbatim_match_timeon_style(self):
        """When hint_raw contains a quoted fragment, evidence_quote should be that sentence.

        Mirrors the timeon→brienne-tarth failure case: hint has "You did for Vargo..."
        but old locator attached an unrelated both-named sentence.  The fixed locator
        should return the sentence containing the verbatim quote.
        """
        prose = (
            "Brienne raised her sword and prepared to strike.\n"
            "\"You did for Vargo with that bite, you know.\n"
            "His ear turned black and started leaking pus.\n"
            "Brienne stabbed him through the throat and Timeon fell.\n"
        )
        chapter_path = self._write_chapter("affc", "affc-brienne-test", prose)

        candidate = {
            "source_slug": "timeon",
            "target_slug": "brienne-tarth",
            "hint_raw": '"You did for Vargo with that bite, you know." [Telling Brienne about Hoat\'s fate',
            "evidence_text": "",
            "evidence_chapter": "affc-brienne-test",
            "evidence_book": "affc",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)

        self.assertEqual(result["locate_status"], "verbatim")
        self.assertEqual(result["quote_source"], "hint-verbatim",
                         f"Expected hint-verbatim, got {result['quote_source']!r}")
        # The evidence_quote must contain the verbatim fragment, NOT some other sentence
        self.assertIn("Vargo", result["evidence_quote"],
                      f"Quote should contain 'Vargo': {result['evidence_quote']!r}")
        # Must NOT be the unrelated both-named sentence about Brienne stabbing Timeon
        self.assertNotIn("stabbed him through the throat", result["evidence_quote"],
                         "Should not have grabbed the unrelated both-named sentence")

    def test_hint_verbatim_uses_quote_source_field(self):
        """quote_source must be emitted on every return path."""
        prose = "Arya watched as Yoren cut her hair carefully.\n"
        chapter_path = self._write_chapter("acok", "acok-qs-test", prose)

        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "yoren",
            "hint_raw": '"Yoren cut her hair" [while disguising Arya]',
            "evidence_text": "Yoren disguised her",
            "evidence_chapter": "acok-qs-test",
            "evidence_book": "acok",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)

        self.assertIn("quote_source", result, "quote_source field must be present")
        valid_qs = {"hint-verbatim", "hint-fuzzy", "both-named-window", "nearest-fallback", "chapter-level"}
        self.assertIn(result["quote_source"], valid_qs,
                      f"Invalid quote_source: {result['quote_source']!r}")

    def test_hint_verbatim_anchored_both_named_when_both_in_quote(self):
        """When the hint's verbatim sentence names both endpoints, quality=hint-anchored-both-named."""
        prose = (
            "Nothing relevant here at all.\n"
            '"Arya followed Yoren toward the gate." [Describing their escape]\n'
            "Then they departed the city entirely.\n"
        )
        chapter_path = self._write_chapter("acok", "acok-anchored-both", prose)

        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "yoren",
            "hint_raw": '"Arya followed Yoren toward the gate." [Describing their escape]',
            "evidence_text": "",
            "evidence_chapter": "acok-anchored-both",
            "evidence_book": "acok",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)

        if result["quote_source"] == "hint-verbatim":
            self.assertEqual(result["locate_quality"], "hint-anchored-both-named",
                             "Both names in quote sentence → hint-anchored-both-named")


class TestHintFuzzyPath(unittest.TestCase):
    """locate_evidence Path B: hint-fuzzy when no quoted fragment but key tokens match."""

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

    def test_hint_fuzzy_matches_event_paraphrase(self):
        """Hint with **Bold** — paraphrase style uses fuzzy matching to find the right sentence."""
        prose = (
            "The fire burned low in the hearth.\n"
            "Bran asked Old Nan about the three-eyed crow appearing in his dreams.\n"
            "She did not answer immediately and looked away.\n"
        )
        chapter_path = self._write_chapter("agot", "agot-bran-fuzzy", prose)

        candidate = {
            "source_slug": "bran-stark",
            "target_slug": "old-nan",
            "hint_raw": "**Bran asks about the crows** — Bran asks Old Nan about the three-eyed crow in his dreams.",
            "evidence_text": "",
            "evidence_chapter": "agot-bran-fuzzy",
            "evidence_book": "agot",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)

        self.assertEqual(result["locate_status"], "verbatim")
        # Should have found the sentence with crow / Bran / Old Nan
        if result["quote_source"] == "hint-fuzzy":
            self.assertIn("crow", result["evidence_quote"].lower(),
                          "Fuzzy match should point to the crow sentence")

    def test_fall_through_to_both_named_when_hint_has_no_usable_content(self):
        """When hint has no quoted fragment and no distinctive content words, fall through to C."""
        # Hint with only stopwords and a single common word — fuzzy threshold won't fire
        prose = (
            "Arya walked toward Yoren carefully.\n"
            "She was afraid but followed him.\n"
        )
        chapter_path = self._write_chapter("acok", "acok-fallthrough", prose)

        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "yoren",
            "hint_raw": "follows",  # single word, not enough for fuzzy threshold
            "evidence_text": "Arya followed Yoren",
            "evidence_chapter": "acok-fallthrough",
            "evidence_book": "acok",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)

        # Should still get a verbatim result via path C (both-named-window)
        self.assertEqual(result["locate_status"], "verbatim")
        # quote_source may be both-named-window, nearest-fallback, or hint-fuzzy
        # but NOT hint-verbatim (no quoted fragment)
        self.assertNotEqual(result["quote_source"], "hint-verbatim",
                            "No quoted fragment → should not use hint-verbatim path")


class TestNoFabricationRule(unittest.TestCase):
    """Critical rule: hint-anchored quotes never get replaced by a fabricated both-named window.

    If the hint's true sentence names only one (or zero) endpoints, the locator
    must return that honest quote with a low locate_quality, NOT silently swap in
    a different both-named sentence from elsewhere in the chapter.
    """

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

    def test_no_fabrication_one_named(self):
        """Hint quote names only source (Timeon-style dialogue) → hint-anchored-one-named.

        Downstream must be able to filter on this, so locate_quality must accurately
        reflect that the quote is NOT both-named.  The locator must NOT replace it
        with a both-named sentence from elsewhere.
        """
        prose = (
            '"You did for Vargo with that bite, you know.\n'
            "His ear turned black and started leaking pus.\n"
            # Elsewhere in the chapter: a sentence naming both endpoints
            "Brienne stabbed Timeon through the throat and he fell.\n"
        )
        chapter_path = self._write_chapter("affc", "affc-no-fab", prose)

        candidate = {
            "source_slug": "timeon",
            "target_slug": "brienne-tarth",
            "hint_raw": '"You did for Vargo with that bite, you know." [Telling Brienne about Hoat\'s fate',
            "evidence_text": "",
            "evidence_chapter": "affc-no-fab",
            "evidence_book": "affc",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)

        # The quote must be the hint's verbatim sentence (or the adjacent merged pair)
        # and NOT the fabricated both-named sentence about stabbing
        self.assertEqual(result["quote_source"], "hint-verbatim",
                         "Hint has a quoted fragment → must go via hint-verbatim path")
        self.assertIn("Vargo", result["evidence_quote"],
                      "Evidence quote must contain the hint's verbatim text")
        self.assertNotIn("stabbed", result["evidence_quote"],
                         "Must NOT fabricate the both-named 'stabbed' sentence as the quote")
        # locate_quality must be honest (NOT both-named)
        self.assertNotEqual(result["locate_quality"], "both-named",
                            "locate_quality must NOT be both-named when hint sentence "
                            "does not contain both names")
        # Should be one of the hint-anchored variants
        self.assertIn(result["locate_quality"],
                      {"hint-anchored-none", "hint-anchored-one-named"},
                      f"Expected low hint-anchored quality, got {result['locate_quality']!r}")

    def test_quote_source_field_on_chapter_level_fallback(self):
        """quote_source='chapter-level' must appear even on chapter-level returns."""
        prose = "Completely unrelated prose about the Wall and winter.\n"
        chapter_path = self._write_chapter("agot", "agot-cl-qs", prose)

        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "cersei-lannister",
            "hint_raw": "hates",
            "evidence_text": "Arya despises Cersei",
            "evidence_chapter": "agot-cl-qs",
            "evidence_book": "agot",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)

        self.assertIn("quote_source", result)
        # No match → chapter-level or nearest-fallback
        self.assertIn(result["quote_source"],
                      {"chapter-level", "nearest-fallback", "hint-fuzzy", "hint-verbatim"})


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


# ---------------------------------------------------------------------------
# BUG 1 fix: evidence_ref line number must point to the actual file line
#            containing the start of evidence_quote.
# ---------------------------------------------------------------------------

class TestEvidenceRefLineNumber(unittest.TestCase):
    """BUG 1 regression: evidence_ref line suffix must point to the file line
    where the matched evidence_quote actually begins.

    The fix: split_into_sentences must detect paragraph boundaries from
    line-number gaps (blank lines filtered by read_chapter_prose), so
    sentences carry accurate per-paragraph start line numbers rather than
    all defaulting to the first prose line (line 11 for most chapters).

    Assertion contract: read the file at the line number in evidence_ref and
    confirm it contains the start of evidence_quote (case-insensitive prefix
    overlap of at least 10 characters).
    """

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._tmp_path = Path(self._tmp)

    def _write_chapter_multiline(
        self,
        book: str,
        chapter_slug: str,
        paragraphs: list[str],
    ) -> Path:
        """Write a chapter with YAML frontmatter and multiple blank-line-separated paragraphs.

        Returns the Path to the written file.
        The YAML frontmatter occupies lines 1-5 (3 header lines + 1 blank = 4 actual lines,
        then line 5 is blank); first paragraph starts at line 6.
        We use a minimal 3-line frontmatter: '---', 'book: TEST', '---'.
        With a blank line after it the layout is:
          1: ---
          2: book: TEST
          3: ---
          4: (blank)
          5: paragraph 0 text
          6: (blank)
          7: paragraph 1 text
          ...
        """
        chapter_dir = self._tmp_path / "sources" / "chapters" / book
        chapter_dir.mkdir(parents=True, exist_ok=True)
        lines = ["---", "book: TEST", "---", ""]
        for i, para in enumerate(paragraphs):
            lines.append(para)
            if i < len(paragraphs) - 1:
                lines.append("")  # blank separator between paragraphs
        content = "\n".join(lines) + "\n"
        path = chapter_dir / f"{chapter_slug}.md"
        path.write_text(content, encoding="utf-8")
        return path

    def _read_file_line(self, path: Path, lineno: int) -> str:
        """Return the text of the given 1-based line from the file."""
        raw_lines = path.read_text(encoding="utf-8").splitlines()
        if lineno < 1 or lineno > len(raw_lines):
            return ""
        return raw_lines[lineno - 1]

    def _extract_line_suffix(self, evidence_ref: str) -> int | None:
        """Extract the line number from 'path/to/file.md:N', or None if absent."""
        if ":" not in evidence_ref:
            return None
        suffix = evidence_ref.rsplit(":", 1)[-1]
        try:
            return int(suffix)
        except ValueError:
            return None

    def _assert_ref_points_to_quote(self, result: dict, chapter_path: Path, path_label: str):
        """Core assertion: file[lineno] contains the start of evidence_quote."""
        self.assertEqual(result["locate_status"], "verbatim",
                         f"{path_label}: expected verbatim, got {result['locate_status']!r}")
        lineno = self._extract_line_suffix(result["evidence_ref"])
        self.assertIsNotNone(lineno,
                             f"{path_label}: evidence_ref has no line suffix: {result['evidence_ref']!r}")
        # The line must NOT be 11 (or any first-prose-line default)
        # — it must be the actual line in the file
        file_line = self._read_file_line(chapter_path, lineno)
        quote_head = result["evidence_quote"][:20].lower().strip()
        self.assertTrue(
            quote_head in file_line.lower() or file_line.lower().startswith(quote_head[:10]),
            f"{path_label}: file line {lineno} does not contain the quote head.\n"
            f"  evidence_ref:   {result['evidence_ref']!r}\n"
            f"  evidence_quote: {result['evidence_quote']!r}\n"
            f"  file line {lineno}: {file_line!r}",
        )

    def test_hint_verbatim_correct_line_number(self):
        """hint-verbatim path: evidence_ref line must point to the sentence containing
        the quoted fragment, NOT to the first prose line.

        Layout (each numbered item is a file line):
          1: ---
          2: book: TEST
          3: ---
          4: (blank)
          5: Paragraph one. An early scene in the chapter.
          6: (blank)
          7: Paragraph two. Arya woke and thought about the war.
          8: (blank)
          9: "It is Catelyn who wants this peace, not the boy." Tyrion read on.
          10: (blank)
          11: Paragraph four. The litter rocked like a ship.
        """
        paragraphs = [
            "Paragraph one. An early scene in the chapter.",
            "Paragraph two. Arya woke and thought about the war.",
            '"It is Catelyn who wants this peace, not the boy." Tyrion read on.',
            "Paragraph four. The litter rocked like a ship.",
        ]
        chapter_path = self._write_chapter_multiline("acok", "acok-tyrion-bugtest-v", paragraphs)

        candidate = {
            "source_slug": "cleos-frey",
            "target_slug": "tyrion-lannister",
            "hint_raw": '"It is Catelyn who wants this peace, not the boy."',
            "evidence_text": "",
            "evidence_chapter": "acok-tyrion-bugtest-v",
            "evidence_book": "acok",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)

        self.assertEqual(result.get("quote_source"), "hint-verbatim",
                         f"Expected hint-verbatim path, got {result.get('quote_source')!r}")
        self._assert_ref_points_to_quote(result, chapter_path, "hint-verbatim")
        # Confirm it's NOT pointing at line 5 (first prose line)
        lineno = self._extract_line_suffix(result["evidence_ref"])
        self.assertNotEqual(lineno, 5,
                            "hint-verbatim returned first-prose-line number; paragraph boundary detection failed")

    def test_hint_fuzzy_correct_line_number(self):
        """hint-fuzzy path: evidence_ref line must match the fuzzy-matched sentence, not line 1.

        Layout:
          5: Paragraph one. The castle stood on a hill.
          7: Paragraph two. Cersei dismissed her ladies for the evening.
          9: Bran asked Old Nan about the three-eyed crow appearing in his dreams.
          11: Paragraph four. The fire burned low in the hearth.
        """
        paragraphs = [
            "The castle stood on a hill.",
            "Cersei dismissed her ladies for the evening.",
            "Bran asked Old Nan about the three-eyed crow appearing in his dreams.",
            "The fire burned low in the hearth.",
        ]
        chapter_path = self._write_chapter_multiline("agot", "agot-bran-bugtest-f", paragraphs)

        candidate = {
            "source_slug": "bran-stark",
            "target_slug": "old-nan",
            # hint has no quoted fragment, so verbatim path won't fire → fuzzy path
            "hint_raw": "**Bran asks about the crows** — Bran asks Old Nan about the three-eyed crow dreams.",
            "evidence_text": "",
            "evidence_chapter": "agot-bran-bugtest-f",
            "evidence_book": "agot",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)

        if result["locate_status"] == "verbatim":
            self._assert_ref_points_to_quote(result, chapter_path, "hint-fuzzy")
            lineno = self._extract_line_suffix(result["evidence_ref"])
            # First prose line is 5; the crow sentence is at line 9
            self.assertNotEqual(lineno, 5,
                                "hint-fuzzy returned first-prose-line; paragraph gap detection failed")

    def test_both_named_window_correct_line_number(self):
        """both-named-window path: evidence_ref line must point into the chapter, not line 1.

        Layout (paragraph 3 names both Arya and Yoren):
          5: Paragraph one. The road stretched long before them.
          7: Paragraph two. She was afraid but kept walking.
          9: Arya followed Yoren toward the city gate.
          11: Paragraph four. The night air was cold and damp.
        """
        paragraphs = [
            "The road stretched long before them.",
            "She was afraid but kept walking.",
            "Arya followed Yoren toward the city gate.",
            "The night air was cold and damp.",
        ]
        chapter_path = self._write_chapter_multiline("acok", "acok-arya-bugtest-w", paragraphs)

        candidate = {
            "source_slug": "arya-stark",
            "target_slug": "yoren",
            "hint_raw": "follows",
            "evidence_text": "Arya followed Yoren",
            "evidence_chapter": "acok-arya-bugtest-w",
            "evidence_book": "acok",
        }
        result = locator_mod.locate_evidence(candidate, chapter_path)

        if result["locate_status"] == "verbatim":
            self._assert_ref_points_to_quote(result, chapter_path, "both-named-window")
            lineno = self._extract_line_suffix(result["evidence_ref"])
            # First prose line is 5; the both-named sentence is at line 9
            self.assertNotEqual(lineno, 5,
                                "both-named-window returned first-prose-line; paragraph gap detection failed")


class TestParagraphBoundaryDetection(unittest.TestCase):
    """split_into_sentences must flush paragraph on line-number gaps (blank-line-filtered input).

    The fix is in split_into_sentences: when read_chapter_prose strips blank lines,
    consecutive paragraphs appear as non-consecutive line numbers.  The function must
    detect this gap and flush the accumulated paragraph before starting a new one.
    """

    def test_gap_triggers_paragraph_flush(self):
        """Lines with a gap (e.g. 11, 13) cause a flush between them.

        Without the fix, both lines would be merged into one paragraph with start
        line = 11, so every sentence gets lineno=11.  With the fix, the second
        paragraph starts fresh at lineno=13.
        """
        # Simulate two paragraphs after blank-line stripping:
        # Line 11: first paragraph
        # Line 13: second paragraph (gap = 2 → paragraph boundary)
        prose_lines = [
            (11, "Paragraph one begins here."),
            (13, "Paragraph two begins separately."),
        ]
        sents = locator_mod.split_into_sentences(prose_lines)
        linenos = [ln for ln, _ in sents]
        # Both sentences should appear
        self.assertEqual(len(sents), 2)
        # Crucially, the second sentence must have lineno=13, not 11
        self.assertEqual(linenos[0], 11, "First sentence should be at line 11")
        self.assertEqual(linenos[1], 13, "Second sentence should be at line 13 (gap flush)")

    def test_adjacent_lines_merged_into_paragraph(self):
        """Lines with consecutive numbers (no gap) belong to the same paragraph."""
        prose_lines = [
            (11, "Line one of the same paragraph."),
            (12, "Line two, still the same paragraph."),
        ]
        sents = locator_mod.split_into_sentences(prose_lines)
        # Both lines merged → sentences all have lineno=11
        linenos = [ln for ln, _ in sents]
        for ln in linenos:
            self.assertEqual(ln, 11, f"Sentence from adjacent lines should have lineno=11, got {ln}")

    def test_multi_paragraph_chapter_has_distinct_line_numbers(self):
        """A multi-paragraph prose excerpt should yield sentences with distinct linenos."""
        # Simulate a chapter with 5 paragraphs at lines 11, 14, 17, 20, 23
        # (each separated by 2 blank lines → line-number gap of 3)
        prose_lines = [
            (11, "First paragraph. It is the opening."),
            (14, "Second paragraph. More content here."),
            (17, "Third paragraph. Characters speak."),
            (20, "Fourth paragraph. Action happens."),
            (23, "Fifth paragraph. The chapter ends."),
        ]
        sents = locator_mod.split_into_sentences(prose_lines)
        linenos = [ln for ln, _ in sents]
        # Each paragraph should produce at least one sentence with its own lineno
        self.assertIn(11, linenos)
        self.assertIn(14, linenos)
        self.assertIn(17, linenos)
        self.assertIn(20, linenos)
        self.assertIn(23, linenos)


# ---------------------------------------------------------------------------
# BUG 2 fix: quote_source and locate_quality must survive into ALL classifier
#            output row types (emitted, rejected, needs-qualifier, classify_failed).
# ---------------------------------------------------------------------------

class TestClassifierRowPassthrough(unittest.TestCase):
    """BUG 2 regression: quote_source and locate_quality must be carried through
    from the input tail_row into every classifier output row type.

    Tests all four builders: build_emit_edge_row, build_rejected_row,
    build_needs_qualifier_row, build_classify_failed_row.
    """

    def _make_tail_row(self, quote_source="hint-verbatim", locate_quality="hint-anchored-both-named"):
        """Return a minimal tail_row dict carrying the two passthrough fields."""
        return {
            "source_slug": "arya-stark",
            "target_slug": "yoren",
            "hint_raw": '"Yoren cut her hair" [disguise]',
            "evidence_chapter": "acok-arya-01",
            "evidence_quote": "Yoren cut her hair carefully.",
            "evidence_ref": "sources/chapters/acok/acok-arya-01.md:141",
            "evidence_section": "Relationships Observed",
            "evidence_kind": "book-pass1",
            "locate_status": "verbatim",
            "locate_quality": locate_quality,
            "quote_source": quote_source,
            "corroborates_known_edge": False,
            "wiki_edge_type": None,
            "candidate_kind": "pass1_relationship",
        }

    def test_emit_edge_carries_quote_source(self):
        """build_emit_edge_row must include quote_source from input row."""
        row = self._make_tail_row(quote_source="hint-verbatim")
        result = classifier_mod.build_emit_edge_row(
            tail_row=row,
            edge_type="PROTECTS",
            qualifier=None,
            model="claude-sonnet-4-6",
            run_id="test-run",
        )
        self.assertIn("quote_source", result,
                      "build_emit_edge_row must include quote_source")
        self.assertEqual(result["quote_source"], "hint-verbatim")

    def test_emit_edge_carries_locate_quality(self):
        """build_emit_edge_row must include locate_quality from input row."""
        row = self._make_tail_row(locate_quality="hint-anchored-both-named")
        result = classifier_mod.build_emit_edge_row(
            tail_row=row,
            edge_type="PROTECTS",
            qualifier=None,
            model="claude-sonnet-4-6",
            run_id="test-run",
        )
        self.assertIn("locate_quality", result,
                      "build_emit_edge_row must include locate_quality")
        self.assertEqual(result["locate_quality"], "hint-anchored-both-named")

    def test_rejected_row_carries_quote_source(self):
        """build_rejected_row must include quote_source from input row."""
        row = self._make_tail_row(quote_source="hint-fuzzy")
        result = classifier_mod.build_rejected_row(tail_row=row, run_id="test-run")
        self.assertIn("quote_source", result,
                      "build_rejected_row must include quote_source")
        self.assertEqual(result["quote_source"], "hint-fuzzy")

    def test_rejected_row_carries_locate_quality(self):
        """build_rejected_row must include locate_quality from input row."""
        row = self._make_tail_row(locate_quality="one-named")
        result = classifier_mod.build_rejected_row(tail_row=row, run_id="test-run")
        self.assertIn("locate_quality", result,
                      "build_rejected_row must include locate_quality")
        self.assertEqual(result["locate_quality"], "one-named")

    def test_needs_qualifier_row_carries_quote_source(self):
        """build_needs_qualifier_row must include quote_source from input row."""
        row = self._make_tail_row(quote_source="both-named-window")
        result = classifier_mod.build_needs_qualifier_row(
            tail_row=row, edge_type="PARENT_OF", run_id="test-run"
        )
        self.assertIn("quote_source", result,
                      "build_needs_qualifier_row must include quote_source")
        self.assertEqual(result["quote_source"], "both-named-window")

    def test_needs_qualifier_row_carries_locate_quality(self):
        """build_needs_qualifier_row must include locate_quality from input row."""
        row = self._make_tail_row(locate_quality="both-named")
        result = classifier_mod.build_needs_qualifier_row(
            tail_row=row, edge_type="PARENT_OF", run_id="test-run"
        )
        self.assertIn("locate_quality", result,
                      "build_needs_qualifier_row must include locate_quality")
        self.assertEqual(result["locate_quality"], "both-named")

    def test_classify_failed_row_carries_quote_source(self):
        """build_classify_failed_row must include quote_source from input row."""
        row = self._make_tail_row(quote_source="nearest-fallback")
        result = classifier_mod.build_classify_failed_row(
            tail_row=row, reason="not in vocab", run_id="test-run"
        )
        self.assertIn("quote_source", result,
                      "build_classify_failed_row must include quote_source")
        self.assertEqual(result["quote_source"], "nearest-fallback")

    def test_classify_failed_row_carries_locate_quality(self):
        """build_classify_failed_row must include locate_quality from input row."""
        row = self._make_tail_row(locate_quality="nearest-fallback")
        result = classifier_mod.build_classify_failed_row(
            tail_row=row, reason="not in vocab", run_id="test-run"
        )
        self.assertIn("locate_quality", result,
                      "build_classify_failed_row must include locate_quality")
        self.assertEqual(result["locate_quality"], "nearest-fallback")

    def test_all_four_builders_have_both_fields(self):
        """Omnibus: all four builders must carry both quote_source and locate_quality."""
        row = self._make_tail_row(quote_source="hint-verbatim", locate_quality="hint-anchored-both-named")
        builders_results = [
            ("emit_edge", classifier_mod.build_emit_edge_row(
                tail_row=row, edge_type="PROTECTS", qualifier=None,
                model="claude-sonnet-4-6", run_id="test-run")),
            ("rejected", classifier_mod.build_rejected_row(
                tail_row=row, run_id="test-run")),
            ("needs_qualifier", classifier_mod.build_needs_qualifier_row(
                tail_row=row, edge_type="PARENT_OF", run_id="test-run")),
            ("classify_failed", classifier_mod.build_classify_failed_row(
                tail_row=row, reason="test", run_id="test-run")),
        ]
        for label, result in builders_results:
            with self.subTest(builder=label):
                self.assertIn("quote_source", result,
                              f"{label}: quote_source missing from output row")
                self.assertIn("locate_quality", result,
                              f"{label}: locate_quality missing from output row")
                self.assertEqual(result["quote_source"], "hint-verbatim",
                                 f"{label}: quote_source value wrong")
                self.assertEqual(result["locate_quality"], "hint-anchored-both-named",
                                 f"{label}: locate_quality value wrong")


if __name__ == "__main__":
    unittest.main()
