#!/usr/bin/env python3
"""stage4-pass1-evidence-locator.py — Stage 4 Pass-1-Derived Edge Pipeline: Script 2.

Reads the per-chapter candidate JSONL files produced by Script 1
(stage4-pass1-edge-candidates.py) and, for each candidate, locates the best
verbatim supporting passage in the corresponding chapter prose file.

The evidence_text cell from the extraction is usually PARAPHRASED (e.g.
"Yoren cut her hair, disguised her, protects her identity, disciplines her"),
so matching is fuzzy: we score sentences by overlap with entity surface forms
+ distinctive content words from the evidence_text and hint_raw.

For typed candidates → emits to {chapter}.edges.jsonl (the "win" file).
For untyped candidates → emits to {chapter}.tail.jsonl (staged for future LLM pass).
Both files carry the located citation (evidence_quote + evidence_ref + locate_status).

Outputs (--apply mode):
  - Typed edges:
      working/wiki/pass2-buckets/pass1-derived/{book}/{chapter}.edges.jsonl
  - Untyped tail:
      working/wiki/pass2-buckets/pass1-derived/_tail/{book}/{chapter}.tail.jsonl
  - Locator stats (md + json):
      working/wiki/data/pass1-derived-locator-stats.md
      working/wiki/data/pass1-derived-locator-stats.json

Usage:
  python3 scripts/stage4-pass1-evidence-locator.py --plan
      Read candidate files + prose, compute stats, print to stdout. Write NOTHING.
  python3 scripts/stage4-pass1-evidence-locator.py --apply
      Same as --plan, plus write all output files.
  python3 scripts/stage4-pass1-evidence-locator.py --plan --book acok
  python3 scripts/stage4-pass1-evidence-locator.py --plan --chapter-slug acok-arya-01

No LLM calls. No network. Deterministic.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
CHAPTERS_DIR = REPO_ROOT / "sources" / "chapters"
PASS2_BUCKETS_DIR = REPO_ROOT / "working" / "wiki" / "pass2-buckets"
WIKI_DATA_DIR = REPO_ROOT / "working" / "wiki" / "data"

IN_BASE_DIR = PASS2_BUCKETS_DIR / "pass1-derived"
OUT_TAIL_DIR = IN_BASE_DIR / "_tail"
OUT_LOCATOR_STATS_MD = WIKI_DATA_DIR / "pass1-derived-locator-stats.md"
OUT_LOCATOR_STATS_JSON = WIKI_DATA_DIR / "pass1-derived-locator-stats.json"

BOOKS = ["agot", "acok", "asos", "affc", "adwd"]


# ---------------------------------------------------------------------------
# English stopwords — words to exclude from content-word scoring
# ---------------------------------------------------------------------------
_STOPWORDS = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "must", "shall", "can",
    "not", "no", "nor", "so", "yet", "both", "either", "neither",
    "he", "she", "it", "they", "we", "you", "i", "his", "her", "its",
    "their", "our", "your", "my", "him", "them", "us", "me",
    "that", "this", "these", "those", "which", "who", "whom", "whose",
    "what", "when", "where", "why", "how", "all", "each", "every",
    "any", "some", "more", "most", "other", "then", "than", "too",
    "just", "up", "out", "about", "after", "before", "while", "also",
    "into", "through", "during", "between", "against", "over", "under",
    "again", "there", "here", "even", "down", "only", "very", "still",
    "back", "now", "always", "never", "once",
})


def _content_words(text: str) -> set[str]:
    """Extract lowercased non-stopword words of length >= 3 from text."""
    tokens = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    return {t for t in tokens if t not in _STOPWORDS}


# ---------------------------------------------------------------------------
# Name surface forms extractor
# ---------------------------------------------------------------------------
def _name_forms(slug: str) -> set[str]:
    """Generate surface forms of a slug for name matching.

    E.g. 'arya-stark' → {'arya', 'stark', 'arya stark', 'arya-stark'}
    """
    forms: set[str] = set()
    parts = slug.split("-")
    forms.add(slug.lower())
    forms.add(slug.replace("-", " ").lower())
    for p in parts:
        if len(p) >= 3:
            forms.add(p.lower())
    return forms


# ---------------------------------------------------------------------------
# Chapter prose reader
# ---------------------------------------------------------------------------
def read_chapter_prose(chapter_path: Path) -> list[tuple[int, str]]:
    """Read a chapter file, skip YAML frontmatter, return (line_number, line_text).

    YAML frontmatter = lines between opening '---' and closing '---'.
    Lines are 1-based.

    Returns list of (line_number, stripped_line) for non-empty prose lines.
    """
    try:
        raw_lines = chapter_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        print(f"  WARNING: Cannot read chapter {chapter_path}: {exc}", file=sys.stderr)
        return []

    # Skip YAML frontmatter
    in_frontmatter = False
    frontmatter_done = False
    prose_lines: list[tuple[int, str]] = []

    for lineno, line in enumerate(raw_lines, start=1):
        stripped = line.strip()
        if lineno == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
                frontmatter_done = True
            continue
        if stripped:
            prose_lines.append((lineno, line))  # Keep original line (don't strip for quote)

    return prose_lines


# ---------------------------------------------------------------------------
# Sentence splitter
# ---------------------------------------------------------------------------
# We use a simple rule: split on sentence-ending punctuation followed by whitespace.
_SENTENCE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')


def split_into_sentences(prose_lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Split prose lines into sentences, tracking the line number of each sentence's start.

    Returns list of (line_number, sentence_text) where line_number is 1-based and
    refers to the source line where the sentence began.
    """
    sentences: list[tuple[int, str]] = []

    # First, join adjacent lines into paragraphs to avoid intra-sentence line breaks
    # While tracking the start line of each paragraph
    i = 0
    lines = prose_lines

    # Approach: work line by line, accumulate text per paragraph
    current_start_line: int | None = None
    current_text: list[str] = []

    def flush_paragraph():
        nonlocal current_start_line, current_text
        if current_text:
            para_text = " ".join(current_text)
            # Split into sentences within the paragraph
            parts = _SENTENCE_SPLIT_RE.split(para_text)
            for part in parts:
                part = part.strip()
                if part:
                    sentences.append((current_start_line, part))
            current_text = []
            current_start_line = None

    for lineno, line in lines:
        text = line.strip()
        if not text:
            flush_paragraph()
            continue
        if current_start_line is None:
            current_start_line = lineno
        current_text.append(text)

    flush_paragraph()
    return sentences


# ---------------------------------------------------------------------------
# Evidence locator
# ---------------------------------------------------------------------------
# Minimum score threshold to qualify as a verbatim match.
# Score = (name_hits * 2 + content_word_hits) / max(total_query_terms, 1)
# We require at least 0.15 (roughly: at least 1 content match in a 6-term query).
_MIN_SCORE_THRESHOLD = 0.15


def locate_evidence(
    candidate: dict,
    chapter_path: Path,
) -> dict:
    """Find the best verbatim passage in the chapter prose for a candidate.

    Returns a dict with keys added to the candidate:
      evidence_quote, evidence_ref, locate_status

    locate_status is "verbatim" (sentence-level match) or "chapter-level" (fallback).
    """
    source_slug = candidate["source_slug"]
    target_slug = candidate["target_slug"]
    hint_raw = candidate.get("hint_raw", "")
    evidence_text = candidate.get("evidence_text", "")
    chapter_id = candidate["evidence_chapter"]
    book = candidate["evidence_book"]

    chapter_rel = f"sources/chapters/{book}/{chapter_id}.md"
    chapter_ref_base = chapter_rel  # without line suffix

    # Build query terms: name surface forms + content words from evidence + hint
    source_forms = _name_forms(source_slug)
    target_forms = _name_forms(target_slug)
    evidence_content_words = _content_words(f"{evidence_text} {hint_raw}")

    all_query_terms = source_forms | target_forms | evidence_content_words
    n_query = max(len(all_query_terms), 1)

    # Read prose
    prose_lines = read_chapter_prose(chapter_path)
    if not prose_lines:
        return {
            "evidence_quote": f"[PARAPHRASE] {evidence_text}" if evidence_text else "",
            "evidence_ref": chapter_ref_base,
            "locate_status": "chapter-level",
        }

    sentences = split_into_sentences(prose_lines)
    if not sentences:
        return {
            "evidence_quote": f"[PARAPHRASE] {evidence_text}" if evidence_text else "",
            "evidence_ref": chapter_ref_base,
            "locate_status": "chapter-level",
        }

    best_score = -1.0
    best_sentence = ""
    best_lineno = 0

    for lineno, sent_text in sentences:
        sent_lower = sent_text.lower()
        sent_tokens = set(re.findall(r"\b[a-zA-Z]{2,}\b", sent_lower))

        # Name hits: check if any surface form appears in the sentence
        name_hits = 0
        # Check source forms
        for form in source_forms:
            if form in sent_lower:
                name_hits += 1
                break
        # Check target forms
        for form in target_forms:
            if form in sent_lower:
                name_hits += 1
                break

        # Content word hits
        content_hits = len(evidence_content_words & sent_tokens)

        score = (name_hits * 2 + content_hits) / n_query

        if score > best_score:
            best_score = score
            best_sentence = sent_text.strip()
            best_lineno = lineno

    if best_score >= _MIN_SCORE_THRESHOLD:
        return {
            "evidence_quote": best_sentence,
            "evidence_ref": f"{chapter_ref_base}:{best_lineno}",
            "locate_status": "verbatim",
        }
    else:
        # Chapter-level fallback: use paraphrased evidence_text with marker
        fallback_quote = f"[PARAPHRASE] {evidence_text}" if evidence_text else ""
        return {
            "evidence_quote": fallback_quote,
            "evidence_ref": chapter_ref_base,
            "locate_status": "chapter-level",
        }


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Stage 4 Pass-1-Derived Edge Pipeline — Script 2: evidence locator.\n"
            "Reads Script 1's candidate JSONL files, locates verbatim evidence in\n"
            "chapter prose, and emits final typed edges + untyped tail JSONL files."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--plan",
        action="store_true",
        default=True,
        help="Dry-run: compute stats, print to stdout. Write NOTHING (default).",
    )
    mode_group.add_argument(
        "--apply",
        action="store_true",
        help="Compute + write all output files.",
    )
    parser.add_argument(
        "--book",
        choices=BOOKS,
        default=None,
        metavar="BOOK",
        help="Restrict to one book.",
    )
    parser.add_argument(
        "--chapter-slug",
        default=None,
        metavar="SLUG",
        help="Restrict to one chapter slug (e.g. acok-arya-01).",
    )
    args = parser.parse_args()
    write_output = args.apply

    produced_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    run_date = datetime.now(timezone.utc).strftime("%Y%m%d")

    # -----------------------------------------------------------------------
    # Step 1: Enumerate input candidate JSONL files
    # -----------------------------------------------------------------------
    books_to_scan = [args.book] if args.book else BOOKS

    candidate_files: list[Path] = []
    for book in books_to_scan:
        book_dir = IN_BASE_DIR / book
        if not book_dir.exists():
            continue
        for f in sorted(book_dir.glob("*.candidates.jsonl")):
            chapter_slug = f.name[: -len(".candidates.jsonl")]
            if args.chapter_slug and chapter_slug != args.chapter_slug:
                continue
            candidate_files.append(f)

    print(f"  {len(candidate_files):,} candidate files to process")

    if not candidate_files:
        print("No candidate files found. Run Script 1 (--apply) first.", file=sys.stderr)
        sys.exit(1)

    # -----------------------------------------------------------------------
    # Step 2: Process each chapter
    # -----------------------------------------------------------------------
    count_candidates = 0
    count_typed = 0
    count_untyped = 0
    count_verbatim = 0
    count_chapter_level = 0

    # Per-book stats
    book_stats: dict[str, dict] = {
        b: {"candidates": 0, "typed": 0, "untyped": 0, "verbatim": 0, "chapter_level": 0}
        for b in BOOKS
    }

    # Per-chapter output collections
    chapter_edges: dict[str, tuple[str, list[dict]]] = {}
    chapter_tails: dict[str, tuple[str, list[dict]]] = {}

    for cand_file in candidate_files:
        chapter_slug = cand_file.name[: -len(".candidates.jsonl")]
        book_abbrev = cand_file.parent.name

        # Find corresponding chapter prose file
        chapter_path = CHAPTERS_DIR / book_abbrev / f"{chapter_slug}.md"
        chapter_exists = chapter_path.exists()
        if not chapter_exists:
            print(
                f"  WARNING: Chapter prose not found: {chapter_path}",
                file=sys.stderr,
            )

        # Read candidates
        try:
            candidates = []
            with cand_file.open(encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        candidates.append(json.loads(line))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"  WARNING: Cannot read {cand_file}: {exc}", file=sys.stderr)
            continue

        count_candidates += len(candidates)
        book_stats[book_abbrev]["candidates"] += len(candidates)

        edges_this_chapter: list[dict] = []
        tail_this_chapter: list[dict] = []

        for cand in candidates:
            is_typed = cand.get("edge_type") is not None

            # Locate evidence
            if chapter_exists:
                loc = locate_evidence(cand, chapter_path)
            else:
                # No prose file — chapter-level fallback
                evidence_text = cand.get("evidence_text", "")
                chapter_rel = f"sources/chapters/{book_abbrev}/{chapter_slug}.md"
                loc = {
                    "evidence_quote": f"[PARAPHRASE] {evidence_text}" if evidence_text else "",
                    "evidence_ref": chapter_rel,
                    "locate_status": "chapter-level",
                }

            # Track stats
            if loc["locate_status"] == "verbatim":
                count_verbatim += 1
                book_stats[book_abbrev]["verbatim"] += 1
            else:
                count_chapter_level += 1
                book_stats[book_abbrev]["chapter_level"] += 1

            if is_typed:
                count_typed += 1
                book_stats[book_abbrev]["typed"] += 1

                # Build edges row (typed only → emitted as final edge).
                # Fields named to be compatible with wiki-pass2-validate-edge-jsonl.py:
                # - candidate_kind: "pass1_relationship"
                # - evidence_kind: "book-pass1"
                # - asserted_relation: the raw hint text (validator looks for this field)
                # - extraction_file: path to source extraction
                # - confidence_tier: 1 (book-primary source; reviewer may adjust)
                # - evidence_book: book abbreviation
                # Note: v1 emits no `qualifier` field (by design — see architecture.md).
                edge_row = {
                    "decision": "emit_edge",
                    "candidate_kind": "pass1_relationship",
                    "edge_type": cand["edge_type"],
                    "source_slug": cand["source_slug"],
                    "source_resolution_status": cand.get("source_resolution_status"),
                    "target_slug": cand["target_slug"],
                    "target_resolution_status": cand.get("target_resolution_status"),
                    "evidence_kind": "book-pass1",
                    "evidence_book": cand["evidence_book"],
                    "evidence_chapter": cand["evidence_chapter"],
                    "evidence_section": "Relationships Observed",
                    "evidence_quote": loc["evidence_quote"],
                    "evidence_ref": loc["evidence_ref"],
                    "asserted_relation": cand.get("hint_raw", ""),
                    "hint_raw": cand.get("hint_raw", ""),
                    "extraction_file": cand.get("extraction_file", ""),
                    "confidence_tier": 1,
                    "typed_by": cand.get("typed_by"),
                    "corroborates_known_edge": cand.get("corroborates_known_edge", False),
                    "wiki_edge_type": cand.get("wiki_edge_type"),
                    "locate_status": loc["locate_status"],
                    "run_id": cand.get("run_id", ""),
                    "schema_version": cand.get("schema_version", ""),
                    "produced_at": cand.get("produced_at", produced_at),
                }
                edges_this_chapter.append(edge_row)

            else:
                count_untyped += 1
                book_stats[book_abbrev]["untyped"] += 1

                # Build tail row (untyped → staged for future LLM pass)
                tail_row = {
                    "decision": "needs_type",
                    "source_slug": cand["source_slug"],
                    "target_slug": cand["target_slug"],
                    "evidence_kind": "book-pass1",
                    "evidence_chapter": cand["evidence_chapter"],
                    "evidence_section": "Relationships Observed",
                    "evidence_quote": loc["evidence_quote"],
                    "evidence_ref": loc["evidence_ref"],
                    "hint_raw": cand.get("hint_raw", ""),
                    "corroborates_known_edge": cand.get("corroborates_known_edge", False),
                    "wiki_edge_type": cand.get("wiki_edge_type"),
                    "locate_status": loc["locate_status"],
                    "run_id": cand.get("run_id", ""),
                    "schema_version": cand.get("schema_version", ""),
                    "produced_at": cand.get("produced_at", produced_at),
                }
                tail_this_chapter.append(tail_row)

        if edges_this_chapter:
            chapter_edges[chapter_slug] = (book_abbrev, edges_this_chapter)
        if tail_this_chapter:
            chapter_tails[chapter_slug] = (book_abbrev, tail_this_chapter)

    # -----------------------------------------------------------------------
    # Step 3: Print summary
    # -----------------------------------------------------------------------
    verbatim_pct = 100.0 * count_verbatim / count_candidates if count_candidates else 0.0
    typed_pct = 100.0 * count_typed / count_candidates if count_candidates else 0.0

    print()
    print("=" * 70)
    print("STAGE 4 PASS-1-DERIVED EVIDENCE LOCATOR — RUN SUMMARY")
    print("=" * 70)
    print(f"  Candidate files processed:     {len(candidate_files):>8,}")
    print(f"  Total candidates:              {count_candidates:>8,}")
    print(f"  Typed candidates → edges:      {count_typed:>8,}  ({typed_pct:.1f}%)")
    print(f"  Untyped candidates → tail:     {count_untyped:>8,}  ({100 - typed_pct:.1f}%)")
    print(f"  Verbatim match:                {count_verbatim:>8,}  ({verbatim_pct:.1f}%)")
    print(f"  Chapter-level fallback:        {count_chapter_level:>8,}  ({100 - verbatim_pct:.1f}%)")
    print()

    print("Per-book breakdown:")
    for book in BOOKS:
        if args.book and book != args.book:
            continue
        bs = book_stats[book]
        n = bs["candidates"]
        if n == 0:
            continue
        vb_pct = 100.0 * bs["verbatim"] / n if n else 0.0
        print(
            f"  {book.upper():<6}  candidates={n:,}  "
            f"typed={bs['typed']:,}  untyped={bs['untyped']:,}  "
            f"verbatim={bs['verbatim']:,} ({vb_pct:.1f}%)"
        )
    print()

    # -----------------------------------------------------------------------
    # Step 4: Write outputs (--apply only)
    # -----------------------------------------------------------------------
    if not write_output:
        print("Plan mode — nothing written. Re-run with --apply to write outputs.")
        return

    print("Writing outputs...")

    # 4a. Per-chapter edges JSONL
    edges_files_written = 0
    edges_rows_written = 0
    for chapter_slug, (book_abbrev, edges) in sorted(chapter_edges.items()):
        out_dir = IN_BASE_DIR / book_abbrev
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{chapter_slug}.edges.jsonl"
        with out_file.open("w", encoding="utf-8") as fh:
            for row in edges:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        edges_files_written += 1
        edges_rows_written += len(edges)
    print(f"  {edges_files_written:,} edge files, {edges_rows_written:,} rows")

    # 4b. Per-chapter tail JSONL
    tail_files_written = 0
    tail_rows_written = 0
    for chapter_slug, (book_abbrev, tail_rows) in sorted(chapter_tails.items()):
        out_dir = OUT_TAIL_DIR / book_abbrev
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{chapter_slug}.tail.jsonl"
        with out_file.open("w", encoding="utf-8") as fh:
            for row in tail_rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        tail_files_written += 1
        tail_rows_written += len(tail_rows)
    print(f"  {tail_files_written:,} tail files, {tail_rows_written:,} rows")

    # 4c. Locator stats markdown
    WIKI_DATA_DIR.mkdir(parents=True, exist_ok=True)
    stats_lines = [
        "# Pass-1-Derived: Locator Stats",
        "",
        f"> Generated: {produced_at}  ",
        "",
        "## Overall",
        "",
        "| Metric | Count | % |",
        "|--------|-------|---|",
        f"| Candidate files processed | {len(candidate_files):,} | — |",
        f"| Total candidates | {count_candidates:,} | 100% |",
        f"| Typed → edges | {count_typed:,} | {typed_pct:.1f}% |",
        f"| Untyped → tail | {count_untyped:,} | {100 - typed_pct:.1f}% |",
        f"| Verbatim match | {count_verbatim:,} | {verbatim_pct:.1f}% |",
        f"| Chapter-level fallback | {count_chapter_level:,} | {100 - verbatim_pct:.1f}% |",
        "",
        "## Per-Book",
        "",
        "| Book | Candidates | Typed | Untyped | Verbatim | Verbatim% |",
        "|------|------------|-------|---------|---------|-----------|",
    ]
    for book in BOOKS:
        bs = book_stats[book]
        n = bs["candidates"]
        if n == 0:
            continue
        vb_pct = 100.0 * bs["verbatim"] / n if n else 0.0
        stats_lines.append(
            f"| {book.upper()} | {n:,} | {bs['typed']:,} | {bs['untyped']:,} | "
            f"{bs['verbatim']:,} | {vb_pct:.1f}% |"
        )
    OUT_LOCATOR_STATS_MD.write_text("\n".join(stats_lines) + "\n", encoding="utf-8")
    print(f"  Written: {OUT_LOCATOR_STATS_MD}")

    # 4d. Locator stats JSON
    locator_stats = {
        "generated_at": produced_at,
        "total_candidate_files": len(candidate_files),
        "total_candidates": count_candidates,
        "typed_to_edges": count_typed,
        "untyped_to_tail": count_untyped,
        "verbatim_match": count_verbatim,
        "chapter_level_fallback": count_chapter_level,
        "verbatim_pct": round(verbatim_pct, 2),
        "per_book": {book: dict(book_stats[book]) for book in BOOKS},
    }
    OUT_LOCATOR_STATS_JSON.write_text(
        json.dumps(locator_stats, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"  Written: {OUT_LOCATOR_STATS_JSON}")

    print()
    print(f"Done. {edges_rows_written:,} edges written, {tail_rows_written:,} tail rows staged.")
    print(f"  Verbatim match rate: {verbatim_pct:.1f}%")


if __name__ == "__main__":
    main()
