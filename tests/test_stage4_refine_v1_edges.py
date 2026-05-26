"""Tests for scripts/stage4-refine-v1-edges.py — stdlib unittest.

Covers the four required invariants:
  1. Type-contract DROP happens for violating rows.
  2. QR soft-flag is added (not dropped) for relevance failures.
  3. Passing rows are unannotated.
  4. output count = input count - hard drops.

No filesystem access required for core tests (all slugs/indexes injected).

Run: python3 -m unittest tests.test_stage4_refine_v1_edges -v
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from tests._helpers import load_script

refine = load_script("stage4-refine-v1-edges.py")
# Load the real sibling modules the same way load_script does (importlib,
# hyphen-safe) so the stubs can delegate to their real implementations.
_tcv_real = load_script("stage4-type-contract-validator.py")
_qrf_real = load_script("stage4-quote-relevance-filter.py")


# ---------------------------------------------------------------------------
# Minimal stub modules
# ---------------------------------------------------------------------------

# We pass thin wrappers around the already-loaded real modules so tests
# don't hit the filesystem (alias files, character nodes) unless explicitly
# required.

class _StubTCV:
    """Type-contract-validator stub — delegates to the real implementation."""

    @staticmethod
    def type_contract_pass(row: dict, character_slugs: frozenset,
                           slug_category_index=None) -> tuple[bool, str]:
        return _tcv_real.type_contract_pass(row, character_slugs, slug_category_index)

    @staticmethod
    def build_character_slugs(nodes_dir) -> frozenset:
        return frozenset()

    @staticmethod
    def build_slug_category_index(nodes_dir) -> dict:
        return {}


class _StubQRF:
    """Quote-relevance-filter stub — delegates to the real implementation."""

    @staticmethod
    def build_stoplist() -> frozenset:
        return frozenset({"the", "a", "an", "of", "and", "or", "in", "at"})

    @staticmethod
    def build_slug_token_index(slugs, *, stoplist=None, **kwargs):
        sl = stoplist or frozenset()
        index = {}
        for slug in (slugs or []):
            toks = frozenset(
                t.lower() for t in slug.split("-")
                if len(t) > 2 and t.lower() not in sl
            )
            index[slug] = toks
        return index

    @staticmethod
    def quote_relevance_pass(row, slug_token_index, stoplist, *, quote_field="evidence_quote"):
        return _qrf_real.quote_relevance_pass(row, slug_token_index, stoplist,
                                              quote_field=quote_field)


_stub_tcv = _StubTCV()
_stub_qrf = _StubQRF()

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_CHARS = frozenset({
    "arya-stark", "jon-snow", "tyrion-lannister", "cersei-lannister",
    "eddard-stark", "catelyn-stark", "robb-stark", "sansa-stark",
    "joffrey-baratheon", "sandor-clegane",
})

_STOPLIST: frozenset[str] = frozenset({
    "the", "a", "an", "of", "and", "or", "in", "at",
})


def _make_row(
    src: str,
    tgt: str,
    et: str,
    quote: str = "",
    **extra,
) -> dict:
    return {
        "source_slug": src,
        "target_slug": tgt,
        "edge_type": et,
        "evidence_quote": quote,
        **extra,
    }


def _make_token_index(slugs: list[str], stoplist: frozenset[str]) -> dict[str, frozenset[str]]:
    """Build a minimal slug->token index from slug tokens (no alias files)."""
    index = {}
    for slug in slugs:
        toks = frozenset(
            t.lower() for t in slug.split("-")
            if len(t) > 2 and t.lower() not in stoplist
        )
        index[slug] = toks
    return index


# ---------------------------------------------------------------------------
# Test 1: Type-contract hard drop
# ---------------------------------------------------------------------------

class TestTypeContractHardDrop(unittest.TestCase):
    """Invariant 1: Rows violating type contracts are dropped (not soft-flagged)."""

    def _run(self, rows):
        all_slugs = list({r.get("source_slug", "") for r in rows} |
                         {r.get("target_slug", "") for r in rows})
        idx = _make_token_index(all_slugs, _STOPLIST)
        return refine.refine_edges(
            rows, _CHARS, idx, _STOPLIST,
            tcv_module=_stub_tcv, qrf_module=_stub_qrf,
        )

    def test_echoes_char_char_kept(self):
        """ECHOES char<->char must be KEPT (not dropped).

        Architecture (Narrative section): ECHOES = 'Weaker than PARALLELS — structural
        or verbal similarity.'  Both types apply to characters.  The old DROP contract
        was wrong and has been removed.  ECHOES char<->char is a valid literary edge.
        """
        row = _make_row(
            "arya-stark", "jon-snow", "ECHOES",
            quote="Arya and Jon shared the same fire.",
        )
        output, dropped = self._run([row])
        self.assertEqual(len(dropped), 0, "ECHOES char<->char must NOT be dropped")
        self.assertEqual(len(output), 1, "ECHOES char<->char must be kept in output")
        self.assertNotIn("_contract_reason", output[0])

    def test_kinship_non_char_endpoint_flagged(self):
        """SIBLING_OF with one non-char endpoint is now a FLAG (kept with warning), not a DROP.

        robb-stark IS a character; house-stark is not.  The new contract logic treats this
        as a probable slug-alias problem (true relationship, wrong slug) and FLAGS rather
        than dropping.  The row goes to output with _contract_warning=True.
        """
        row = _make_row(
            "robb-stark", "house-stark", "SIBLING_OF",
            quote="Robb and House Stark were inseparable.",
        )
        output, dropped = self._run([row])
        self.assertEqual(len(dropped), 0, "One-sided kinship non-char should FLAG, not DROP")
        self.assertEqual(len(output), 1)
        self.assertTrue(output[0].get("_contract_warning"),
                        "Flagged row must carry _contract_warning=True")

    def test_kinship_both_non_char_endpoints_dropped(self):
        """SIBLING_OF where NEITHER endpoint is a character -> DROP (genuinely wrong)."""
        row = _make_row(
            "house-stark", "the-wall", "SIBLING_OF",
            quote="House Stark and the Wall shared a long history.",
        )
        chars = _CHARS  # neither house-stark nor the-wall is in _CHARS
        all_slugs = [row["source_slug"], row["target_slug"]]
        idx = _make_token_index(all_slugs, _STOPLIST)
        output, dropped = refine.refine_edges(
            [row], chars, idx, _STOPLIST,
            tcv_module=_stub_tcv, qrf_module=_stub_qrf,
        )
        self.assertEqual(len(dropped), 1, "Both-non-char kinship should DROP")
        self.assertEqual(len(output), 0)
        self.assertIn("CONTRACT_VIOLATED", dropped[0]["_contract_reason"])

    def test_holds_title_char_target_dropped(self):
        """HOLDS_TITLE targeting a character must be dropped."""
        row = _make_row(
            "eddard-stark", "jon-snow", "HOLDS_TITLE",
            quote="Eddard told Jon about the north.",
        )
        output, dropped = self._run([row])
        self.assertEqual(len(dropped), 1)
        self.assertEqual(len(output), 0)

    def test_valid_row_not_dropped(self):
        """A valid SIBLING_OF char<->char row must NOT be dropped."""
        row = _make_row(
            "robb-stark", "arya-stark", "SIBLING_OF",
            quote="Robb watched Arya spar in the yard.",
        )
        output, dropped = self._run([row])
        self.assertEqual(len(dropped), 0, f"Expected 0 drops, got: {dropped}")
        self.assertEqual(len(output), 1)

    def test_dropped_row_has_contract_reason_field(self):
        """Dropped rows carry the '_contract_reason' field."""
        row = _make_row(
            "arya-stark", "cersei-lannister", "CONTEMPORARY_WITH",
            quote="Arya and Cersei both lived in King's Landing.",
        )
        _, dropped = self._run([row])
        self.assertGreater(len(dropped), 0)
        self.assertIn("_contract_reason", dropped[0])

    def test_no_qr_fields_on_dropped_row(self):
        """Dropped rows must not have _qr_warning or _qr_reason (they never reach QR).

        Uses CONTEMPORARY_WITH char<->char as the canonical hard-drop case
        (ECHOES char<->char is now KEEP per architecture fix).
        """
        row = _make_row(
            "arya-stark", "jon-snow", "CONTEMPORARY_WITH",
            quote="Arya and Jon both lived in Westeros.",
        )
        _, dropped = self._run([row])
        self.assertEqual(len(dropped), 1)
        self.assertNotIn("_qr_warning", dropped[0])
        self.assertNotIn("_qr_reason", dropped[0])


# ---------------------------------------------------------------------------
# Test 2: QR soft-flag added, not dropped
# ---------------------------------------------------------------------------

class TestQRSoftFlag(unittest.TestCase):
    """Invariant 2: QR-failing rows are annotated and KEPT (not dropped)."""

    def _run(self, rows):
        all_slugs = list({r.get("source_slug", "") for r in rows} |
                         {r.get("target_slug", "") for r in rows})
        idx = _make_token_index(all_slugs, _STOPLIST)
        return refine.refine_edges(
            rows, _CHARS, idx, _STOPLIST,
            tcv_module=_stub_tcv, qrf_module=_stub_qrf,
        )

    def test_qr_fail_row_kept_in_output(self):
        """A row that fails QR must be in output_rows (soft-flag only, not dropped)."""
        # Quote mentions only source (arya) but not target (jon)
        row = _make_row(
            "arya-stark", "jon-snow", "LOVES",
            quote="Arya walked through the dark forest alone.",
        )
        output, dropped = self._run([row])
        self.assertEqual(len(dropped), 0, "QR failure must NOT go to dropped_rows")
        self.assertEqual(len(output), 1, "QR failure must appear in output_rows")

    def test_qr_fail_row_has_warning_flag(self):
        """QR-failing rows must have _qr_warning=True."""
        row = _make_row(
            "arya-stark", "jon-snow", "LOVES",
            quote="Arya walked alone in the woods, thinking of nothing.",
        )
        output, _ = self._run([row])
        self.assertEqual(len(output), 1)
        self.assertTrue(output[0].get("_qr_warning"), "Expected _qr_warning=True")

    def test_qr_fail_row_has_qr_reason(self):
        """QR-failing rows must have a non-empty _qr_reason."""
        row = _make_row(
            "arya-stark", "jon-snow", "LOVES",
            quote="Someone walked alone.",  # neither arya nor jon named
        )
        output, _ = self._run([row])
        self.assertEqual(len(output), 1)
        qr_reason = output[0].get("_qr_reason", "")
        self.assertTrue(qr_reason, "Expected non-empty _qr_reason")

    def test_qr_reason_values_are_valid(self):
        """_qr_reason must be one of the documented values."""
        valid = {
            "unmatched_source", "unmatched_target", "both",
            "unmatchable", "no_quote", "missing_endpoint", "other",
        }
        # Test a variety of failure modes
        cases = [
            # Neither named
            _make_row("arya-stark", "jon-snow", "LOVES",
                      quote="Someone walked into the hall."),
            # Source only
            _make_row("arya-stark", "jon-snow", "LOVES",
                      quote="Arya crept down the corridor."),
            # Empty quote
            _make_row("arya-stark", "jon-snow", "LOVES", quote=""),
        ]
        all_slugs = list({r.get("source_slug", "") for r in cases} |
                         {r.get("target_slug", "") for r in cases})
        idx = _make_token_index(all_slugs, _STOPLIST)
        output, _ = refine.refine_edges(
            cases, _CHARS, idx, _STOPLIST,
            tcv_module=_stub_tcv, qrf_module=_stub_qrf,
        )
        for row in output:
            if row.get("_qr_warning"):
                self.assertIn(
                    row["_qr_reason"], valid,
                    f"Unexpected _qr_reason value: {row['_qr_reason']!r}",
                )

    def test_empty_quote_is_dropped_by_contract_not_qr(self):
        """Empty evidence_quote is hard-dropped by Contract 6 (not soft-flagged by QR).

        Previously this test expected the row to reach QR and receive _qr_reason='no_quote'.
        Contract 6 (empty evidence_quote => DROP) fires first, so the row never reaches QR.
        The correct behaviour: output=0, dropped=1, no _qr_reason on the dropped row.
        """
        row = _make_row("arya-stark", "jon-snow", "LOVES", quote="")
        all_slugs = ["arya-stark", "jon-snow"]
        idx = _make_token_index(all_slugs, _STOPLIST)
        output, dropped = refine.refine_edges(
            [row], _CHARS, idx, _STOPLIST,
            tcv_module=_stub_tcv, qrf_module=_stub_qrf,
        )
        self.assertEqual(len(output), 0,
                         "Empty-quote row should be hard-dropped, not kept")
        self.assertEqual(len(dropped), 1)
        self.assertIn("evidence_quote is empty", dropped[0].get("_contract_reason", ""),
                      "Dropped row should carry the empty-quote contract reason")
        self.assertNotIn("_qr_reason", dropped[0],
                         "Dropped row must not have _qr_reason — it never reached QR")

    def test_unmatched_source_label(self):
        """Quote names only target -> _qr_reason='unmatched_source'."""
        row = _make_row(
            "arya-stark", "jon-snow", "LOVES",
            quote="Jon Snow rode north through the snowstorm.",
        )
        all_slugs = ["arya-stark", "jon-snow"]
        idx = _make_token_index(all_slugs, _STOPLIST)
        output, _ = refine.refine_edges(
            [row], _CHARS, idx, _STOPLIST,
            tcv_module=_stub_tcv, qrf_module=_stub_qrf,
        )
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0].get("_qr_reason"), "unmatched_source")

    def test_unmatched_target_label(self):
        """Quote names only source -> _qr_reason='unmatched_target'."""
        row = _make_row(
            "arya-stark", "jon-snow", "LOVES",
            quote="Arya crept through the shadows of the Red Keep.",
        )
        all_slugs = ["arya-stark", "jon-snow"]
        idx = _make_token_index(all_slugs, _STOPLIST)
        output, _ = refine.refine_edges(
            [row], _CHARS, idx, _STOPLIST,
            tcv_module=_stub_tcv, qrf_module=_stub_qrf,
        )
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0].get("_qr_reason"), "unmatched_target")

    def test_both_label(self):
        """Quote names neither endpoint -> _qr_reason='both'."""
        row = _make_row(
            "arya-stark", "jon-snow", "LOVES",
            quote="The crow flew over the Wall and disappeared.",
        )
        all_slugs = ["arya-stark", "jon-snow"]
        idx = _make_token_index(all_slugs, _STOPLIST)
        output, _ = refine.refine_edges(
            [row], _CHARS, idx, _STOPLIST,
            tcv_module=_stub_tcv, qrf_module=_stub_qrf,
        )
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0].get("_qr_reason"), "both")


# ---------------------------------------------------------------------------
# Test 3: Passing rows are unannotated
# ---------------------------------------------------------------------------

class TestPassingRowsUnannotated(unittest.TestCase):
    """Invariant 3: Rows that pass both filters have no _qr_warning or _qr_reason."""

    def test_clean_row_has_no_annotation(self):
        """A row that passes both TC and QR must have no extra annotation fields."""
        row = _make_row(
            "arya-stark", "jon-snow", "LOVES",
            quote="Jon told Arya he was proud of her.",
        )
        all_slugs = ["arya-stark", "jon-snow"]
        idx = _make_token_index(all_slugs, _STOPLIST)
        output, dropped = refine.refine_edges(
            [row], _CHARS, idx, _STOPLIST,
            tcv_module=_stub_tcv, qrf_module=_stub_qrf,
        )
        self.assertEqual(len(dropped), 0)
        self.assertEqual(len(output), 1)
        out_row = output[0]
        self.assertNotIn("_qr_warning", out_row)
        self.assertNotIn("_qr_reason", out_row)
        self.assertNotIn("_contract_reason", out_row)

    def test_clean_row_preserves_original_fields(self):
        """Original fields are preserved unchanged on passing rows."""
        row = _make_row(
            "tyrion-lannister", "cersei-lannister", "DISTRUSTS",
            quote="Tyrion watched Cersei pour the wine.",
            confidence_tier=1,
            evidence_book="agot",
        )
        all_slugs = ["tyrion-lannister", "cersei-lannister"]
        idx = _make_token_index(all_slugs, _STOPLIST)
        output, _ = refine.refine_edges(
            [row], _CHARS, idx, _STOPLIST,
            tcv_module=_stub_tcv, qrf_module=_stub_qrf,
        )
        self.assertEqual(len(output), 1)
        out_row = output[0]
        self.assertEqual(out_row["confidence_tier"], 1)
        self.assertEqual(out_row["evidence_book"], "agot")


# ---------------------------------------------------------------------------
# Test 4: Output count = input - hard drops
# ---------------------------------------------------------------------------

class TestOutputCount(unittest.TestCase):
    """Invariant 4: len(output) + len(dropped) == len(input)."""

    def test_count_equation_all_pass(self):
        """All-passing batch: dropped=0, output=N."""
        rows = [
            _make_row("arya-stark", "jon-snow", "LOVES",
                      quote="Jon told Arya he was proud of her."),
            _make_row("tyrion-lannister", "cersei-lannister", "DISTRUSTS",
                      quote="Tyrion watched Cersei with narrowed eyes."),
            _make_row("robb-stark", "arya-stark", "SIBLING_OF",
                      quote="Robb wrestled Arya to the ground."),
        ]
        all_slugs = list({r.get("source_slug", "") for r in rows} |
                         {r.get("target_slug", "") for r in rows})
        idx = _make_token_index(all_slugs, _STOPLIST)
        output, dropped = refine.refine_edges(
            rows, _CHARS, idx, _STOPLIST,
            tcv_module=_stub_tcv, qrf_module=_stub_qrf,
        )
        self.assertEqual(len(output) + len(dropped), len(rows))
        self.assertEqual(len(dropped), 0)

    def test_count_equation_with_drops(self):
        """Mix of valid, dropped, and flagged rows: count invariant holds.

        Row breakdown:
          1. arya LOVES jon              — KEEP (clean)
          2. arya CONTEMPORARY_WITH jon  — DROP (CONTEMPORARY_WITH char<->char)
          3. arya HATES jon              — KEEP (QR soft-flag — only arya named in quote)
          4. robb SIBLING_OF house-stark — FLAG (one char endpoint; probable alias problem;
             kept+annotated with _contract_warning=True)
        Expect: 1 drop, 3 output (1 clean + 1 QR-flagged + 1 contract-flagged).

        Note: ECHOES char<->char is now KEEP per architecture fix — use CONTEMPORARY_WITH
        char<->char as the canonical hard-drop case instead.
        """
        rows = [
            # PASS (TC + QR)
            _make_row("arya-stark", "jon-snow", "LOVES",
                      quote="Jon told Arya he was proud."),
            # DROP (TC: CONTEMPORARY_WITH char<->char — genuinely wrong edge)
            _make_row("arya-stark", "jon-snow", "CONTEMPORARY_WITH",
                      quote="Arya and Jon both lived in Westeros at the same time."),
            # PASS TC, QR soft-flag (only arya named)
            _make_row("arya-stark", "jon-snow", "HATES",
                      quote="Arya walked alone through the castle."),
            # FLAG (TC: SIBLING_OF one-non-char endpoint — probable alias; kept+annotated)
            _make_row("robb-stark", "house-stark", "SIBLING_OF",
                      quote="Robb and house-stark fought."),
        ]
        all_slugs = list({r.get("source_slug", "") for r in rows} |
                         {r.get("target_slug", "") for r in rows})
        idx = _make_token_index(all_slugs, _STOPLIST)
        output, dropped = refine.refine_edges(
            rows, _CHARS, idx, _STOPLIST,
            tcv_module=_stub_tcv, qrf_module=_stub_qrf,
        )
        self.assertEqual(
            len(output) + len(dropped), len(rows),
            f"Count invariant broken: {len(output)} output + {len(dropped)} dropped"
            f" != {len(rows)} input",
        )
        self.assertEqual(len(dropped), 1, "Expected 1 hard drop (CONTEMPORARY_WITH char<->char)")
        self.assertEqual(len(output), 3, "Expected 3 survivors (LOVES + HATES QR-flag + SIBLING_OF contract-flag)")

    def test_count_equation_all_dropped(self):
        """All rows drop: output=0, dropped=N.

        Uses two CONTEMPORARY_WITH char<->char rows as the hard-drop cases.
        (ECHOES char<->char is now KEEP — cannot use it for an all-dropped test.)
        """
        rows = [
            _make_row("arya-stark", "jon-snow", "CONTEMPORARY_WITH",
                      quote="Arya and Jon both lived in Westeros at the same time."),
            _make_row("eddard-stark", "catelyn-stark", "CONTEMPORARY_WITH",
                      quote="Eddard and Catelyn stood together."),
        ]
        all_slugs = list({r.get("source_slug", "") for r in rows} |
                         {r.get("target_slug", "") for r in rows})
        idx = _make_token_index(all_slugs, _STOPLIST)
        output, dropped = refine.refine_edges(
            rows, _CHARS, idx, _STOPLIST,
            tcv_module=_stub_tcv, qrf_module=_stub_qrf,
        )
        self.assertEqual(len(output) + len(dropped), len(rows))
        self.assertEqual(len(output), 0)
        self.assertEqual(len(dropped), len(rows))

    def test_count_equation_empty_input(self):
        """Empty input: both lists empty."""
        output, dropped = refine.refine_edges(
            [], _CHARS, {}, _STOPLIST,
            tcv_module=_stub_tcv, qrf_module=_stub_qrf,
        )
        self.assertEqual(len(output), 0)
        self.assertEqual(len(dropped), 0)


# ---------------------------------------------------------------------------
# Test 5: classify_qr_reason helper
# ---------------------------------------------------------------------------

class TestClassifyQRReason(unittest.TestCase):
    """Unit tests for the classify_qr_reason helper."""

    def test_unmatched_source(self):
        self.assertEqual(refine.classify_qr_reason("UNMATCHED_SOURCE: 'arya-stark'"),
                         "unmatched_source")

    def test_unmatched_target(self):
        self.assertEqual(refine.classify_qr_reason("UNMATCHED_TARGET: 'jon-snow'"),
                         "unmatched_target")

    def test_unmatched_both(self):
        self.assertEqual(refine.classify_qr_reason("UNMATCHED_BOTH: src='x' tgt='y'"),
                         "both")

    def test_unmatchable_source(self):
        self.assertEqual(refine.classify_qr_reason("UNMATCHABLE_SOURCE: 'ab' has no usable tokens"),
                         "unmatchable")

    def test_unmatchable_target(self):
        self.assertEqual(refine.classify_qr_reason("UNMATCHABLE_TARGET: 'cd' has no usable tokens"),
                         "unmatchable")

    def test_no_quote(self):
        self.assertEqual(refine.classify_qr_reason("NO_QUOTE: evidence_quote is empty"),
                         "no_quote")

    def test_missing_endpoint(self):
        self.assertEqual(refine.classify_qr_reason("MISSING_ENDPOINT: source or target slug is empty"),
                         "missing_endpoint")

    def test_unknown_falls_back_to_other(self):
        self.assertEqual(refine.classify_qr_reason("SOME_UNKNOWN_REASON"), "other")


# ---------------------------------------------------------------------------
# Test 6: Dry-run safety (no file writes)
# ---------------------------------------------------------------------------

class TestDryRunSafety(unittest.TestCase):
    """Dry-run must not create any output files."""

    def test_dry_run_writes_nothing(self):
        """Running with --dry-run (default) must produce no files in scratch dir."""
        scratch = refine._SCRATCH_DIR
        candidate = refine._CANDIDATE_PATH
        dropped   = refine._DROPPED_PATH

        existed_before = {
            "candidate": candidate.exists(),
            "dropped":   dropped.exists(),
        }
        try:
            refine.main(["--dry-run", "--input", str(refine._EDGES_V1)])
        except SystemExit:
            pass  # OK if input is missing in test env

        # If they didn't exist before, they must not exist after dry-run
        if not existed_before["candidate"]:
            self.assertFalse(candidate.exists(), "Dry-run must not create candidate file")
        if not existed_before["dropped"]:
            self.assertFalse(dropped.exists(), "Dry-run must not create dropped file")


if __name__ == "__main__":
    unittest.main()
