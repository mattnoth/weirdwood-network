"""Tests for scripts/mint_enrichment.py's edge-level skip-if-exists dedup (S200 board
fix): identical (edge_type, source_slug, target_slug, normalized_quote) rows are
skipped; the SAME triple with a DIFFERENT quote is multi-provenance and is kept.

Unit tests exercise the pure helpers directly. The integration test drives the real
CLI end-to-end via subprocess against a tmp copy of edges.jsonl (never the live
graph/edges/edges.jsonl) using two REAL, already-existing node slugs
(aegon-i-targaryen, visenya-targaryen) and two REAL quotes pulled verbatim from the
already-tracked sources/chapters/fab/fab-aegons-conquest-03.md, so authoritative_line's
real (non-overridable) chapter lookup succeeds without needing a chapter-dir override.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _helpers import load_script, REPO_ROOT

me = load_script("mint_enrichment.py")

CHAPTER_BOOK = "fab"
CHAPTER = "fab-aegons-conquest-03"
QUOTE_A = "Aegon's Conquest as their touchstone for the past three hundred years"
QUOTE_B = "More than two years passed between Aegon's landing and his Oldtown coronation"
SRC_SLUG = "aegon-i-targaryen"
TGT_SLUG = "visenya-targaryen"


# --- normalize_quote_for_dedup -----------------------------------------------------

def test_normalize_quote_strips_wrapping_quotes():
    assert me.normalize_quote_for_dedup('"Winter is coming."') == "winter is coming"


def test_normalize_quote_strips_trailing_punct_without_wrapping_quotes():
    assert me.normalize_quote_for_dedup("Winter is coming.") == "winter is coming"
    assert me.normalize_quote_for_dedup("Winter is coming") == "winter is coming"
    assert (me.normalize_quote_for_dedup("Winter is coming.")
            == me.normalize_quote_for_dedup("Winter is coming"))


def test_normalize_quote_collapses_whitespace_and_case():
    assert me.normalize_quote_for_dedup("  Winter   IS\ncoming!  ") == "winter is coming"


def test_normalize_quote_smart_quotes_and_dashes_match_norm():
    # normalize_quote_for_dedup is built on top of norm() — smart-quote/dash handling
    # must match norm() exactly (byte-identical to fab-reconcile-candidates.py's norm()).
    assert me.normalize_quote_for_dedup("“Winter is coming.”") == "winter is coming"
    assert me.normalize_quote_for_dedup('"foo—bar"') == "foo-bar"


# --- edge_dedup_key / load_existing_edge_keys / dedupe_edge_rows -------------------

def test_edge_dedup_key_same_triple_different_quote_are_different_keys():
    k1 = me.edge_dedup_key("SIBLING_OF", SRC_SLUG, TGT_SLUG, QUOTE_A)
    k2 = me.edge_dedup_key("SIBLING_OF", SRC_SLUG, TGT_SLUG, QUOTE_B)
    assert k1 != k2


def test_edge_dedup_key_same_triple_same_quote_diff_punct_are_same_key():
    k1 = me.edge_dedup_key("SIBLING_OF", SRC_SLUG, TGT_SLUG, QUOTE_A + ".")
    k2 = me.edge_dedup_key("SIBLING_OF", SRC_SLUG, TGT_SLUG, QUOTE_A)
    assert k1 == k2


def test_load_existing_edge_keys_skips_quoteless_and_malformed_lines():
    lines = [
        json.dumps({"edge_type": "SWORN_TO", "source_slug": "a", "target_slug": "b"}),  # no quote
        "not json {{{",  # malformed
        json.dumps({"edge_type": "SIBLING_OF", "source_slug": SRC_SLUG,
                    "target_slug": TGT_SLUG, "evidence_quote": QUOTE_A}),
    ]
    keys = me.load_existing_edge_keys(lines)
    assert keys == {me.edge_dedup_key("SIBLING_OF", SRC_SLUG, TGT_SLUG, QUOTE_A)}


def test_dedupe_edge_rows_skips_exact_dup_keeps_multi_provenance():
    seen = {me.edge_dedup_key("SIBLING_OF", SRC_SLUG, TGT_SLUG, QUOTE_A)}
    rows = [
        {"edge_type": "SIBLING_OF", "source_slug": SRC_SLUG, "target_slug": TGT_SLUG,
         "evidence_quote": QUOTE_A, "candidate_id": "E1-dup"},
        {"edge_type": "SIBLING_OF", "source_slug": SRC_SLUG, "target_slug": TGT_SLUG,
         "evidence_quote": QUOTE_B, "candidate_id": "E2-multiprov"},
    ]
    kept, skipped = me.dedupe_edge_rows(rows, seen)
    assert [r["candidate_id"] for r in kept] == ["E2-multiprov"]
    assert [r["candidate_id"] for r in skipped] == ["E1-dup"]


def test_dedupe_edge_rows_catches_intra_run_same_quote_dup():
    """Two rows in the SAME candidate list asserting the same triple+quote — the
    second must be caught even though neither was on disk beforehand."""
    seen = set()
    rows = [
        {"edge_type": "SIBLING_OF", "source_slug": SRC_SLUG, "target_slug": TGT_SLUG,
         "evidence_quote": QUOTE_A, "candidate_id": "E1"},
        {"edge_type": "SIBLING_OF", "source_slug": SRC_SLUG, "target_slug": TGT_SLUG,
         "evidence_quote": QUOTE_A, "candidate_id": "E2-intra-run-dup"},
    ]
    kept, skipped = me.dedupe_edge_rows(rows, seen)
    assert [r["candidate_id"] for r in kept] == ["E1"]
    assert [r["candidate_id"] for r in skipped] == ["E2-intra-run-dup"]


# --- end-to-end CLI: (a) skip exact dup, (b) keep multi-provenance, (c) report counts

def test_cli_skips_exact_dup_and_keeps_multi_provenance(tmp_path):
    edges_path = tmp_path / "edges.jsonl"
    backup_path = tmp_path / "backup.jsonl"
    nodes_root = tmp_path / "nodes-root"  # unused (no new nodes) — never the real graph

    pre_existing_row = {
        "edge_type": "SIBLING_OF",
        "source_slug": SRC_SLUG,
        "target_slug": TGT_SLUG,
        "decision": "emit_edge",
        "candidate_kind": "enrichment-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-prior-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": "2026-07-01T00:00:00+00:00",
        "run_id": "prior-enrichment-s199",
        "evidence_book": CHAPTER_BOOK,
        "evidence_chapter": CHAPTER,
        "evidence_ref": f"sources/chapters/{CHAPTER_BOOK}/{CHAPTER}.md:1",
        "evidence_quote": QUOTE_A,
        "confidence_tier": "tier-1",
        "asserted_relation": "prior batch's assertion",
        "candidate_id": "PRIOR-E1",
    }
    edges_path.write_text(json.dumps(pre_existing_row) + "\n", encoding="utf-8")

    candidates = {
        "_meta": {
            "unit": "test-dedup-unit",
            "run_id": "test-dedup-s200",
            "new_node_slugs": [],
            "produced_at": "2026-07-09T00:00:00+00:00",
        },
        "edges": [
            {"id": "E1", "type": "SIBLING_OF", "source": SRC_SLUG, "target": TGT_SLUG,
             "book": CHAPTER_BOOK, "chapter": CHAPTER, "quote": QUOTE_A,
             "tier": "tier-1", "note": "same quote as a prior batch — must be skipped"},
            {"id": "E2", "type": "SIBLING_OF", "source": SRC_SLUG, "target": TGT_SLUG,
             "book": CHAPTER_BOOK, "chapter": CHAPTER, "quote": QUOTE_B,
             "tier": "tier-1", "note": "different quote, same triple — multi-provenance, must be kept"},
        ],
    }
    candidates_path = tmp_path / "candidates.json"
    candidates_path.write_text(json.dumps(candidates), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "mint_enrichment.py"),
         "--candidates", str(candidates_path),
         "--edges", str(edges_path),
         "--backup", str(backup_path),
         "--nodes-root", str(nodes_root),
         "--produced-at", "2026-07-09T00:00:00+00:00"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    # (c) the run summary reports both counts, observably.
    assert "edges_appended=1" in result.stdout
    assert "edges_skipped_dup=1" in result.stdout
    assert "SKIP dup edge: SIBLING_OF" in result.stdout

    # (a)+(b): edges.jsonl now holds the pre-existing row + exactly ONE new row (the
    # multi-provenance E2), never a second copy of E1.
    lines = [ln for ln in edges_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == 2
    rows = [json.loads(ln) for ln in lines]
    quotes = sorted(r["evidence_quote"] for r in rows)
    assert quotes == sorted([QUOTE_A, QUOTE_B])
    new_row = next(r for r in rows if r.get("candidate_id") == "E2")
    assert new_row["run_id"] == "test-dedup-s200"

    # the real graph is untouched — this test only ever wrote into tmp_path.
    assert not nodes_root.exists() or not any(nodes_root.rglob("*.node.md"))
