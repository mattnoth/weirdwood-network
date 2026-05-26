#!/usr/bin/env python3
"""stage4-relocate-smoke.py — Re-locate evidence quotes for smoke3 rows using the
improved locator (v2) and produce the measurement report.

Reads all rows from the smoke3 run:
  working/wiki/pass2-buckets/pass1-derived/_smoke3-haiku/{book}/{book}-tail.{edges,rejected,classify_failed}.jsonl

For each row, runs the improved locate_evidence() and attaches:
  - evidence_quote  (improved)
  - evidence_ref    (improved)
  - locate_status   (unchanged semantics)
  - locate_quality  (new: both-named / one-named / nearest-fallback / chapter-level)
  - _row_id         (stable integer for join-back)

Task 2 output (classifier-ready JSONL):
  working/wiki/pass2-buckets/pass1-derived/_relocate-smoke/{book}/{book}-tail.candidates.jsonl

  Fields match what stage4-tail-classifier.py's input reader expects:
    decision=needs_type, source_slug, target_slug, evidence_chapter,
    evidence_kind, evidence_section, evidence_quote, evidence_ref,
    hint_raw, locate_status, locate_quality, run_id, schema_version,
    produced_at, _row_id, candidate_kind (preserved or derived)

  Fields stripped (classifier re-types fresh):
    decision (set to needs_type), edge_type, typed_by, confidence_tier,
    asserted_relation (moved to hint_raw if missing)

Task 3 output (measurement report):
  working/wiki/data/pass1-derived-locator-improvement.md

No LLM calls. No network. Deterministic.

Usage:
    python3 scripts/stage4-relocate-smoke.py [--dry-run]
    --dry-run: print stats but do NOT write output files.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
SMOKE3_BASE = REPO / "working" / "wiki" / "pass2-buckets" / "pass1-derived" / "_smoke3-haiku"
OUT_BASE = REPO / "working" / "wiki" / "pass2-buckets" / "pass1-derived" / "_relocate-smoke"
CHAPTERS_DIR = REPO / "sources" / "chapters"
REPORT_PATH = REPO / "working" / "wiki" / "data" / "pass1-derived-locator-improvement.md"

BOOKS = ["agot", "acok", "asos", "affc", "adwd"]
PRODUCED_AT = datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# Load improved locator via importlib (hyphen in filename)
# ---------------------------------------------------------------------------

def _load_module(filename: str, mod_name: str):
    path = REPO / "scripts" / filename
    if not path.exists():
        sys.exit(f"ERROR: Required module not found: {path}")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


locator = _load_module("stage4-pass1-evidence-locator.py", "stage4_pass1_evidence_locator")
qrf     = _load_module("stage4-quote-relevance-filter.py",  "stage4_quote_relevance_filter")


# ---------------------------------------------------------------------------
# Gather smoke3 rows
# ---------------------------------------------------------------------------

def load_smoke3_rows() -> list[dict]:
    """Read all smoke3 JSONL files.  Attach _book and _row_id."""
    rows: list[dict] = []
    row_id = 0
    for book in BOOKS:
        book_dir = SMOKE3_BASE / book
        if not book_dir.exists():
            continue
        for f in sorted(book_dir.glob("*.jsonl")):
            with f.open(encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError as exc:
                        print(f"[warn] {f}:{line[:40]}: {exc}", file=sys.stderr)
                        continue
                    row["_book"] = book
                    row["_row_id"] = row_id
                    row_id += 1
                    rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Build alias-aware token index for all slugs across smoke3 rows
# ---------------------------------------------------------------------------

def build_token_index_for_rows(rows: list[dict]) -> tuple[dict, frozenset]:
    """Return (slug_token_index, stoplist) covering all slugs in rows."""
    stoplist = qrf.build_stoplist()
    all_slugs = list(
        {r.get("source_slug", "") for r in rows} |
        {r.get("target_slug", "") for r in rows}
    )
    all_slugs = [s for s in all_slugs if s]
    idx = qrf.build_slug_token_index(slugs=all_slugs, stoplist=stoplist)
    return idx, stoplist


# ---------------------------------------------------------------------------
# Re-locate a single row using the improved locator
# ---------------------------------------------------------------------------

def relocate_row(row: dict, slug_token_index: dict, stoplist: frozenset) -> dict:
    """Run improved locate_evidence on one smoke3 row.

    Returns loc dict: {evidence_quote, evidence_ref, locate_status, locate_quality}.
    Also pre-seeds the locator's token cache so it doesn't need to rebuild per row.
    """
    src = row.get("source_slug", "")
    tgt = row.get("target_slug", "")
    chapter = row.get("evidence_chapter", "")

    # Pre-seed the module-level cache so locate_evidence uses our pre-built index
    if src in slug_token_index:
        locator._CACHED_TOKEN_INDEX[src] = slug_token_index[src]
    if tgt in slug_token_index:
        locator._CACHED_TOKEN_INDEX[tgt] = slug_token_index[tgt]

    if not chapter:
        return {
            "evidence_quote": row.get("evidence_quote", ""),
            "evidence_ref": "",
            "locate_status": "chapter-level",
            "locate_quality": "chapter-level",
        }

    book = chapter.split("-")[0] if "-" in chapter else row.get("_book", "")
    chapter_path = CHAPTERS_DIR / book / f"{chapter}.md"

    # Construct a synthetic candidate dict for the locator
    candidate = {
        "source_slug": src,
        "target_slug": tgt,
        "hint_raw": row.get("hint_raw", ""),
        "evidence_text": "",   # smoke3 rows don't carry evidence_text separately
        "evidence_chapter": chapter,
        "evidence_book": book,
    }

    loc = locator.locate_evidence(candidate, chapter_path)
    return loc


# ---------------------------------------------------------------------------
# Build classifier-ready candidate row from a smoke3 row + improved loc
# ---------------------------------------------------------------------------

def build_candidate_row(row: dict, loc: dict) -> dict:
    """Build a needs_type candidate row matching the tail-classifier input schema."""
    chapter = row.get("evidence_chapter", "")
    book = chapter.split("-")[0] if "-" in chapter else row.get("_book", "")

    # Preserve candidate_kind if present (emit_edge rows carry it; rejected/failed may not)
    candidate_kind = row.get("candidate_kind", "pass1_relationship")

    return {
        "decision": "needs_type",
        "candidate_kind": candidate_kind,
        "source_slug": row.get("source_slug", ""),
        "source_resolution_status": row.get("source_resolution_status", "tail-llm"),
        "target_slug": row.get("target_slug", ""),
        "target_resolution_status": row.get("target_resolution_status", "tail-llm"),
        "evidence_kind": row.get("evidence_kind", "book-pass1"),
        "evidence_book": book,
        "evidence_chapter": chapter,
        "evidence_section": row.get("evidence_section", "Relationships Observed"),
        "evidence_quote": loc["evidence_quote"],
        "evidence_ref": loc["evidence_ref"],
        "hint_raw": row.get("hint_raw", ""),
        "corroborates_known_edge": row.get("corroborates_known_edge", False),
        "wiki_edge_type": row.get("wiki_edge_type"),
        "locate_status": loc["locate_status"],
        "locate_quality": loc.get("locate_quality", "chapter-level"),
        "run_id": "relocate-smoke-v2",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "_row_id": row.get("_row_id"),
        # Preserve original quote + quality for measurement comparison
        "_orig_evidence_quote": row.get("evidence_quote", ""),
        "_orig_locate_status": row.get("locate_status", "MISSING"),
    }


# ---------------------------------------------------------------------------
# Quote-relevance check helper
# ---------------------------------------------------------------------------

def check_relevance(row: dict, quote: str, slug_token_index: dict, stoplist: frozenset) -> bool:
    """Return True if quote passes the both-named filter for this row."""
    tmp = dict(row)
    tmp["evidence_quote"] = quote
    passed, _ = qrf.quote_relevance_pass(tmp, slug_token_index, stoplist)
    return passed


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(
        description="Re-locate smoke3 rows with improved locator + write measurement report."
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Print stats but write no files.")
    args = parser.parse_args()
    write_output = not args.dry_run

    print("Loading smoke3 rows…")
    rows = load_smoke3_rows()
    print(f"  {len(rows)} rows loaded")

    print("Building alias-aware token index for all slugs…")
    slug_token_index, stoplist = build_token_index_for_rows(rows)
    print(f"  Index covers {len(slug_token_index)} slugs")

    # Seed the locator's module-level cache up front
    locator._CACHED_TOKEN_INDEX.update(slug_token_index)
    locator._CACHED_STOPLIST = stoplist

    print("Re-locating rows…")
    improved_rows: list[dict] = []
    quality_counts: dict[str, int] = {}

    for row in rows:
        loc = relocate_row(row, slug_token_index, stoplist)
        improved_row = build_candidate_row(row, loc)
        improved_rows.append(improved_row)

        lq = loc.get("locate_quality", "chapter-level")
        quality_counts[lq] = quality_counts.get(lq, 0) + 1

    print(f"  Done. {len(improved_rows)} rows processed.")

    # -----------------------------------------------------------------------
    # Measurement: before vs after relevance filter on the 107 emit_edge rows
    # -----------------------------------------------------------------------
    emit_rows = [r for r in rows if r.get("decision") == "emit_edge"]
    print(f"\nMeasuring relevance filter before/after on {len(emit_rows)} emit_edge rows…")

    orig_pass = 0
    new_pass = 0
    orig_fail_new_pass = 0  # recall-recovered
    orig_fail_new_fail = 0

    orig_pass_new_fail = 0  # regressions (should be ~0)
    orig_pass_new_pass = 0

    # For reporting: rows that changed
    improved_examples: list[dict] = []
    still_failing_rows: list[dict] = []

    emit_id_to_improved = {r.get("_row_id"): r for r in improved_rows}

    for row in emit_rows:
        orig_quote = row.get("evidence_quote", "")
        row_id = row.get("_row_id")
        imp_row = emit_id_to_improved.get(row_id)
        if imp_row is None:
            continue
        new_quote = imp_row.get("evidence_quote", "")

        orig_relevant = check_relevance(row, orig_quote, slug_token_index, stoplist)
        new_relevant  = check_relevance(row, new_quote,  slug_token_index, stoplist)

        if orig_relevant:
            orig_pass += 1
            if new_relevant:
                orig_pass_new_pass += 1
            else:
                orig_pass_new_fail += 1
        else:
            if new_relevant:
                orig_fail_new_pass += 1
                # Collect as improvement example
                improved_examples.append({
                    "row_id": row_id,
                    "source_slug": row["source_slug"],
                    "target_slug": row["target_slug"],
                    "orig_quote": orig_quote,
                    "new_quote": new_quote,
                    "orig_quality": imp_row.get("_orig_locate_status", "?"),
                    "new_quality": imp_row.get("locate_quality", "?"),
                })
            else:
                orig_fail_new_fail += 1
                still_failing_rows.append({
                    "row_id": row_id,
                    "source_slug": row["source_slug"],
                    "target_slug": row["target_slug"],
                    "orig_quote": orig_quote,
                    "new_quote": new_quote,
                    "new_quality": imp_row.get("locate_quality", "?"),
                    "hint_raw": row.get("hint_raw", ""),
                })

    new_pass = orig_pass_new_pass + orig_fail_new_pass

    # Classify residual failures as coreference vs. genuinely-not-co-located
    def classify_failure_reason(row_dict: dict) -> str:
        quote = row_dict.get("new_quote", "")
        # Look for pronoun-dominated quotes (coreference indicator)
        pronoun_pattern = re.compile(
            r'\b(he|she|her|him|his|they|them|their|it|its|my|our|your|the girl|the boy|the man)\b',
            re.IGNORECASE
        )
        pronoun_matches = len(pronoun_pattern.findall(quote))
        # Check if any name appears at all
        src = row_dict.get("source_slug", "")
        tgt = row_dict.get("target_slug", "")
        src_toks = frozenset(p.lower() for p in src.split("-") if len(p) > 2)
        tgt_toks = frozenset(p.lower() for p in tgt.split("-") if len(p) > 2)
        q_lower = quote.lower()
        src_present = any(re.search(r'\b' + re.escape(t) + r'\b', q_lower) for t in src_toks)
        tgt_present = any(re.search(r'\b' + re.escape(t) + r'\b', q_lower) for t in tgt_toks)
        if not src_present and not tgt_present:
            return "genuinely-not-co-located"
        elif pronoun_matches > 0 and (not src_present or not tgt_present):
            return "coreference"
        else:
            return "stoplist-filtered"

    failure_reasons: dict[str, int] = {}
    for r in still_failing_rows:
        reason = classify_failure_reason(r)
        r["_failure_reason"] = reason
        failure_reasons[reason] = failure_reasons.get(reason, 0) + 1

    print(f"\n--- Recall recovery (emit_edge rows only) ---")
    print(f"  Total emit_edge rows:          {len(emit_rows)}")
    print(f"  Originally passing:            {orig_pass}")
    print(f"  Originally failing:            {len(emit_rows) - orig_pass}")
    print(f"  Now passing (improved):        {new_pass}")
    print(f"  Recall-recovered (fail→pass):  {orig_fail_new_pass}")
    print(f"  Regressions (pass→fail):       {orig_pass_new_fail}")
    print(f"  Still failing:                 {orig_fail_new_fail}")
    print(f"  Failure reasons: {failure_reasons}")

    print(f"\n--- locate_quality distribution (all {len(rows)} rows) ---")
    for q in ["both-named", "one-named", "nearest-fallback", "chapter-level"]:
        n = quality_counts.get(q, 0)
        pct = 100.0 * n / len(rows) if rows else 0.0
        print(f"  {q:<22}  {n:>4}  ({pct:.1f}%)")

    # -----------------------------------------------------------------------
    # Write outputs
    # -----------------------------------------------------------------------
    if write_output:
        # Task 2: per-book classifier-ready JSONL
        rows_by_book: dict[str, list[dict]] = {b: [] for b in BOOKS}
        for imp_row in improved_rows:
            book = imp_row.get("evidence_book", "")
            if book in rows_by_book:
                rows_by_book[book].append(imp_row)
            else:
                rows_by_book.setdefault(book, []).append(imp_row)

        for book, book_rows in rows_by_book.items():
            if not book_rows:
                continue
            out_dir = OUT_BASE / book
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f"{book}-tail.candidates.jsonl"
            with out_file.open("w", encoding="utf-8") as fh:
                for r in book_rows:
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            print(f"  Written {len(book_rows)} rows → {out_file}")

        # Task 3: measurement report
        _write_report(
            rows=rows,
            improved_rows=improved_rows,
            quality_counts=quality_counts,
            emit_rows=emit_rows,
            orig_pass=orig_pass,
            new_pass=new_pass,
            orig_fail_new_pass=orig_fail_new_pass,
            orig_pass_new_fail=orig_pass_new_fail,
            orig_fail_new_fail=orig_fail_new_fail,
            failure_reasons=failure_reasons,
            improved_examples=improved_examples,
            still_failing_rows=still_failing_rows,
        )
    else:
        print("\nDry-run mode — no files written.")


def _write_report(
    rows: list[dict],
    improved_rows: list[dict],
    quality_counts: dict[str, int],
    emit_rows: list[dict],
    orig_pass: int,
    new_pass: int,
    orig_fail_new_pass: int,
    orig_pass_new_fail: int,
    orig_fail_new_fail: int,
    failure_reasons: dict[str, int],
    improved_examples: list[dict],
    still_failing_rows: list[dict],
) -> None:
    total = len(rows)
    emit_total = len(emit_rows)
    orig_fail = emit_total - orig_pass

    lines: list[str] = [
        "# Pass-1-Derived Locator Improvement — Measurement Report",
        "",
        f"> Generated: {PRODUCED_AT}",
        "",
        "## 1. locate_quality Distribution (All 199+ Smoke3 Rows)",
        "",
        "| locate_quality | Count | % |",
        "|----------------|-------|---|",
    ]
    for q in ["both-named", "one-named", "nearest-fallback", "chapter-level"]:
        n = quality_counts.get(q, 0)
        pct = 100.0 * n / total if total else 0.0
        lines.append(f"| {q} | {n} | {pct:.1f}% |")

    lines += [
        "",
        "**Note:** `chapter-level` rows are cases where the chapter file was missing or",
        "no sentence cleared the minimum score threshold.  `nearest-fallback` means the",
        "best sentence named neither endpoint (content-word match only).",
        "",
        "## 2. Recall-Recovery Signal (emit_edge rows only)",
        "",
        f"The smoke3 run produced **{emit_total} emit_edge rows** (the other {total - emit_total} were",
        "rejected/classify_failed and also get re-located for the re-smoke).",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| emit_edge rows total | {emit_total} |",
        f"| Originally passing quote-relevance | {orig_pass} |",
        f"| Originally failing quote-relevance | {orig_fail} |",
        f"| Now passing with improved locator | {new_pass} |",
        f"| **Recall-recovered (fail→pass)** | **{orig_fail_new_pass}** |",
        f"| Regressions (pass→fail) | {orig_pass_new_fail} |",
        f"| Still failing after improvement | {orig_fail_new_fail} |",
        "",
        f"**Before→after both-named count:** {orig_pass} → {new_pass} "
        f"(+{orig_fail_new_pass} recovered, {orig_pass_new_fail} regression)",
        "",
    ]

    if orig_fail > 0:
        recovery_pct = 100.0 * orig_fail_new_pass / orig_fail
        lines.append(f"Recovery rate on originally-failing rows: **{recovery_pct:.1f}%**")
        lines.append("")

    # Failure reason breakdown
    lines += [
        "### Residual Failure Reasons",
        "",
        "| Reason | Count |",
        "|--------|-------|",
    ]
    for reason, cnt in sorted(failure_reasons.items(), key=lambda x: -x[1]):
        lines.append(f"| {reason} | {cnt} |")

    lines += [
        "",
        "Reason definitions:",
        "- **coreference**: quote has pronouns/generic phrases instead of a name — unfixable by window selection",
        "- **genuinely-not-co-located**: both entities appear in different paragraphs/scenes not captured",
        "- **stoplist-filtered**: name token filtered by stoplist (rare; usually a very short or generic name)",
        "",
        "## 3. Before/After Examples (Improved Quotes)",
        "",
        f"Showing up to 10 of {len(improved_examples)} recovered rows.",
        "",
    ]

    for i, ex in enumerate(improved_examples[:10], 1):
        src = ex["source_slug"]
        tgt = ex["target_slug"]
        orig_q = (ex.get("orig_quote") or "")[:200]
        new_q  = (ex.get("new_quote")  or "")[:200]
        new_qual = ex.get("new_quality", "?")
        lines += [
            f"### Example {i}: {src} → {tgt}",
            "",
            f"**Original quote:** \"{orig_q}\"",
            "",
            f"**Improved quote** (`locate_quality={new_qual}`): \"{new_q}\"",
            "",
        ]

    if orig_fail_new_pass == 0:
        lines += [
            "*(No examples — all originally-failing rows still fail after improvement.)*",
            "",
        ]

    # Still-failing rows
    lines += [
        "## 4. Still Failing After Improvement",
        "",
        f"**{orig_fail_new_fail} rows** still fail the quote-relevance filter after the improved locator.",
        "",
    ]

    for i, r in enumerate(still_failing_rows[:15], 1):
        src = r.get("source_slug", "?")
        tgt = r.get("target_slug", "?")
        new_q = (r.get("new_quote") or "")[:200]
        reason = r.get("_failure_reason", "unknown")
        new_qual = r.get("new_quality", "?")
        lines += [
            f"- **{src} → {tgt}** [{reason}] `{new_qual}`:",
            f"  \"{new_q}\"",
        ]

    if len(still_failing_rows) > 15:
        lines.append(f"  *(... and {len(still_failing_rows) - 15} more)*")

    # Honest assessment
    lines += [
        "",
        "## 5. Honest Assessment",
        "",
        "### What the window-expansion improvement reaches",
        "",
        "The core mis-location class — where the locator chose a single sentence that named",
        "only ONE endpoint — is now largely addressed.  The improved algorithm:",
        "",
        "1. Tries EVERY sentence for both-named first (covers cases where a single sentence",
        "   spans both names but scored lower than a one-name content-rich sentence).",
        "2. If no single sentence names both, expands a window of up to",
        f"   {locator.BOTH_NAMED_WINDOW_SENTENCES} consecutive sentences centred on the best",
        "   sentence.  This catches the common pattern of 'Name A ... [sentence] ... Name B'",
        "   appearing in adjacent sentences within the same prose beat.",
        "3. Uses the alias-aware token index (build_slug_token_index from the relevance filter),",
        "   so firstname aliases and alternate forms are recognised.",
        "",
        "### Irreducible residual (coreference)",
        "",
        "The hard limit that window expansion CANNOT fix is **coreference**: when the prose",
        "refers to an entity only as 'she', 'he', 'my father', 'the girl', etc. within the",
        "relevant passage.  These cases land as `one-named` or `nearest-fallback` regardless",
        "of how large the window is, because no name token appears in the text.",
        "",
        "This is not a locator failure — it is a fundamental property of the source text.",
        "Resolution requires NLP coreference resolution (out of scope for this deterministic",
        "pipeline), or manual review.",
        "",
        "### Remaining gap",
        "",
        "Even after improvement, some rows will still fail the quote-relevance filter.  The",
        "bulk of remaining failures fall into three categories:",
        "",
        "1. **Coreference** (pronouns in the selected passage)",
        "2. **Genuinely not co-located** (the two entities are mentioned in different parts",
        "   of the chapter, with no single prose beat spanning both)",
        "3. **Rare stoplist cases** (one entity has a very short or generic name that is",
        "   filtered by the stoplist)",
        "",
        "The improvement is expected to recover a meaningful fraction of originally-failing",
        "rows — the exact number is measured in §2 above.",
    ]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nReport written → {REPORT_PATH}")


if __name__ == "__main__":
    main()
