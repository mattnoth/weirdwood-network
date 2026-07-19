#!/usr/bin/env python3
"""dunk-egg-harvest-locate.py — D&E harvest sidecar drain prep: locate step.

Parses `working/dunk-egg-pass1/harvest-dunk-egg.jsonl` (372 SLASH-delimited
rows, misnamed .jsonl — format `BOOK / pointer-or-quote / kind / note`),
routes `causal-spine` rows to a seed file for a later event-wiring slice,
and for every other row greps its candidate verbatim fragments against the
whole-novella source file to find a chapter:line grounding.

DETERMINISTIC. STDLIB-ONLY. NO NETWORK. NO GRAPH WRITES — this script only
locates evidence; it does not resolve names, type edges, or touch graph/.

Row parsing:
    Split on ' / '. Two of the 372 rows have a literal ' / ' embedded inside
    a quoted field (a mid-quote line break in the source harvest), which
    breaks a naive 3-way split. Robust fix: split on ALL ' / ' occurrences,
    then find the part that is an EXACT known-kind token (there must be
    exactly one) — everything before it (rejoined with ' / ') is the
    pointer field, everything after is the note field. This self-corrects
    both the textbook 4-part rows and the embedded-slash rows without any
    special-casing.

Candidate fragment collection (per non-causal-spine row):
    - Every double-quoted substring (straight " or curly “ ”) in the
      pointer field (field 2).
    - Every double-quoted substring in the note field (field 4).
    - The pointer field itself, verbatim, IF it contains no double-quote
      character at all AND is >= 5 words — covers the unquoted descriptive
      pointers common to food/hospitality/description rows (e.g. "lamb
      roasted with a crust of herbs, duck cooked with cherries and
      lemons"). Field 4 never contributes this raw-prose fallback (spec
      scopes it to field 2 only).

Grounding: for each distinct candidate fragment, three tiers are tried in
order against the whole-novella source file
(sources/chapters/{book}/{book}-dunk-01.md, book lowercased, frontmatter
skipped, one paragraph per prose line):

    Tier 1 — whole-fragment grep:
        a. EXACT literal substring search (byte-for-byte, case-sensitive).
        b. If zero hits, LIGHT-NORMALIZED search: curly<->straight quotes
           and apostrophes, ellipsis glyph -> "...", em/en dash -> hyphen,
           collapsed whitespace, case-insensitive.

    Tier 2 — ellipsis segmentation (S222 follow-up; only tried when Tier 1
    found nothing AND the fragment contains "..."/"…"): split the fragment
    on the ellipsis marker into sub-parts and grep each sub-part
    independently (same Tier-1 normalization). Sub-parts under 4 words are
    filtered to only the hit lines that land within 6 lines of some >=4-word
    sibling part's hit (guards against a short filler sub-part like "she
    said" matching anywhere in the book). If, after filtering, every
    sub-part still has >=1 hit line AND some combination of hit lines (one
    per sub-part) spans <= 6 lines, that combination grounds the row — cite
    line = the FIRST sub-part's line in the chosen combination, and the
    sub-parts + their lines are stored alongside the fragment.

    Tier 3 — dialogue-tag-strip split (S222 follow-up; only tried when
    Tiers 1-2 both found nothing): some harvest quotes silently splice two
    separately-quoted book spans together across a dropped dialogue tag
    with NO ellipsis marker (e.g. `"Ser Damon Lannister!" he shouted. "The
    Grey Lion!..."` harvested as one continuous quote). Try every internal
    sentence-boundary (`. `/`! `/`? `) as a split point; if both halves are
    >=4 words and each greps to a hit line, and some pairing of their hit
    lines lands on the same or an adjacent source line (|line_a-line_b|<=1),
    that pairing grounds the row the same way Tier 2 does.

Every grounded candidate fragment gets a `hit_count` (the TRUE number of
matching lines/combinations, uncapped) and up to 5 stored hit lines
(`hit_lines`, capped — this is a display cap only, `hit_count` is never
capped). Per row:
    `located`           = True iff any candidate fragment has hit_count == 1
                           (an unambiguous, unique grounding).
    `located_ambiguous` = True iff NOT located, but the best candidate
                           fragment has hit_count in [2, 5] — multiple
                           plausible locations a human/agent can disambiguate
                           from context.
    Fragments with hit_count > 5 are marked `unusable: true` and never
    drive `located`/`located_ambiguous` — too generic to be worth surfacing
    as a location candidate.

Outputs:
    working/dunk-egg-graph-ingest/harvest/causal-spine-seeds.jsonl
    working/dunk-egg-graph-ingest/harvest/located.jsonl
    working/dunk-egg-graph-ingest/harvest/LOCATE-STATS.md

Usage:
    python3 scripts/dunk-egg-harvest-locate.py
    python3 scripts/dunk-egg-harvest-locate.py --harvest PATH --out-dir DIR
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

DEFAULT_HARVEST_PATH = REPO_ROOT / "working" / "dunk-egg-pass1" / "harvest-dunk-egg.jsonl"
DEFAULT_OUT_DIR = REPO_ROOT / "working" / "dunk-egg-graph-ingest" / "harvest"
CHAPTERS_DIR = REPO_ROOT / "sources" / "chapters"

BOOKS = ["thk", "tss", "tmk"]

KNOWN_KINDS = frozenset({
    "cross-identity", "targaryen-history", "prophecy", "causal-spine",
    "food", "hospitality", "description", "foreshadow-hook", "other",
})

MIN_PROSE_WORDS = 5
MIN_FRAGMENT_CHARS = 3

# S222 follow-up: ellipsis segmentation + dialogue-tag-strip tuning
MAX_SPAN_LINES = 6          # sub-part hit lines must cluster within this many lines
MAX_STORED_HITS = 5         # display cap on hit_lines; hit_count itself is never capped
SHORT_PART_WORD_MAX = 3     # sub-parts with <= this many words are "short" (filtered by proximity)
DIALOGUE_TAG_MIN_PART_WORDS = 3   # each half of a dialogue-tag-strip split must clear this


# ---------------------------------------------------------------------------
# Row parsing (with embedded-slash self-correction)
# ---------------------------------------------------------------------------
def parse_harvest_line(line: str, lineno: int) -> dict | None:
    """Parse one SLASH-delimited harvest row.

    Returns {book, pointer, kind, note, rejoined, source_line} or None if
    the row is unparseable (logged by the caller as an anomaly).
    """
    parts = line.split(" / ")
    if len(parts) < 4:
        return None

    book = parts[0].strip()
    rejoined = False

    if len(parts) == 4 and parts[2].strip() in KNOWN_KINDS:
        pointer, kind, note = parts[1], parts[2].strip(), parts[3]
    else:
        # Embedded ' / ' somewhere in the pointer or note field: find the
        # part that is an exact known-kind token. Search from the LEFT so
        # the first plausible kind boundary wins (kind field never itself
        # contains ' / ', by construction of the source vocabulary).
        kind_candidates = [i for i in range(1, len(parts) - 1) if parts[i].strip() in KNOWN_KINDS]
        if len(kind_candidates) != 1:
            return None
        idx = kind_candidates[0]
        pointer = " / ".join(parts[1:idx])
        kind = parts[idx].strip()
        note = " / ".join(parts[idx + 1:])
        rejoined = True

    return {
        "book": book,
        "pointer": pointer.strip(),
        "kind": kind,
        "note": note.strip(),
        "rejoined": rejoined,
        "source_line": lineno,
    }


# ---------------------------------------------------------------------------
# Fragment extraction
# ---------------------------------------------------------------------------
_STRAIGHT_QUOTE_RE = re.compile(r'"([^"]{%d,})"' % MIN_FRAGMENT_CHARS)
_CURLY_QUOTE_RE = re.compile(r"“([^”]{%d,})”" % MIN_FRAGMENT_CHARS)
_ANY_QUOTE_CHAR_RE = re.compile(r'["“”]')


def extract_quoted_fragments(text: str) -> list[str]:
    frags = _STRAIGHT_QUOTE_RE.findall(text) + _CURLY_QUOTE_RE.findall(text)
    return [f.strip() for f in frags if f.strip()]


def collect_candidate_fragments(pointer: str, note: str) -> list[str]:
    """Ordered, de-duplicated candidate fragment list per the spec:
    quoted substrings in pointer + quoted substrings in note, plus the
    raw pointer text if it's quote-free prose of >= 5 words."""
    seen: set[str] = set()
    ordered: list[str] = []

    def add(frag: str) -> None:
        frag = frag.strip()
        if len(frag) < MIN_FRAGMENT_CHARS or frag in seen:
            return
        seen.add(frag)
        ordered.append(frag)

    for f in extract_quoted_fragments(pointer):
        add(f)
    for f in extract_quoted_fragments(note):
        add(f)

    if not _ANY_QUOTE_CHAR_RE.search(pointer) and len(pointer.split()) >= MIN_PROSE_WORDS:
        add(pointer)

    return ordered


# ---------------------------------------------------------------------------
# Source-file reading + grep (exact, then light-normalized)
# ---------------------------------------------------------------------------
_QUOTE_NORM_TABLE = str.maketrans({
    "“": '"', "”": '"', "‘": "'", "’": "'",
    "′": "'", "″": '"', "«": '"', "»": '"',
    "—": "-", "–": "-", " ": " ",
})


def normalize_for_match(text: str) -> str:
    text = text.translate(_QUOTE_NORM_TABLE)
    text = text.replace("…", "...")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def read_prose_lines(path: Path) -> list[tuple[int, str]]:
    """Frontmatter-skipping line reader. One paragraph per source line, so
    line-level substring search is sufficient granularity for this pass."""
    try:
        raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        print(f"  WARNING: cannot read {path}: {exc}", file=sys.stderr)
        return []
    in_fm = False
    result: list[tuple[int, str]] = []
    for i, line in enumerate(raw_lines, start=1):
        s = line.strip()
        if i == 1 and s == "---":
            in_fm = True
            continue
        if in_fm:
            if s == "---":
                in_fm = False
            continue
        if s:
            result.append((i, line))
    return result


def grep_fragment(fragment: str, prose_lines: list[tuple[int, str]]) -> tuple[list[int], str]:
    """Returns (hit_line_numbers, stage) where stage is 'exact' or
    'normalized' (whichever stage actually produced the hits), or
    ([], 'none') if neither stage found anything."""
    frag_clean = fragment.strip()

    exact_hits = [lineno for lineno, line in prose_lines if frag_clean in line]
    if exact_hits:
        return exact_hits, "exact"

    norm_frag = normalize_for_match(frag_clean).lower()
    norm_hits = [
        lineno for lineno, line in prose_lines
        if norm_frag in normalize_for_match(line).lower()
    ]
    if norm_hits:
        return norm_hits, "normalized"

    return [], "none"


# ---------------------------------------------------------------------------
# S222 follow-up — Tier 2: ellipsis segmentation, Tier 3: dialogue-tag-strip
# ---------------------------------------------------------------------------
_ELLIPSIS_SPLIT_RE = re.compile(r"\.\.\.|…")
_SENTENCE_BOUNDARY_RE = re.compile(r"[.!?]\s+")


def word_count(text: str) -> int:
    return len(text.split())


def split_on_ellipsis(fragment: str) -> list[str]:
    parts = _ELLIPSIS_SPLIT_RE.split(fragment)
    return [p.strip(" ,;:—–") for p in parts if p.strip(" ,;:—–")]


def find_sentence_split_points(fragment: str) -> list[int]:
    """Character offsets immediately after an internal '. '/'! '/'? ' —
    candidate positions where a harvest quote may have silently elided a
    dialogue tag ('X!" he shouted. "Y') with no ellipsis marker at all."""
    points = []
    for m in _SENTENCE_BOUNDARY_RE.finditer(fragment):
        pos = m.end()
        if 0 < pos < len(fragment):
            points.append(pos)
    return points


def _build_result(text: str, hit_lines: list[int], stage: str, cite_line: int | None = None,
                   extra: dict | None = None) -> dict:
    hits_sorted = sorted(set(hit_lines))
    result = {
        "text": text,
        "hit_lines": hits_sorted[:MAX_STORED_HITS],
        "hit_count": len(hits_sorted),
        "cite_line": cite_line if cite_line is not None else hits_sorted[0],
        "stage": stage,
    }
    if extra:
        result.update(extra)
    return result


def locate_ellipsis_segmented(fragment: str, prose_lines: list[tuple[int, str]]) -> dict | None:
    """Tier 2: split on '...'/'…', require every sub-part to hit, and that
    some one-hit-line-per-part combination clusters within MAX_SPAN_LINES."""
    parts = split_on_ellipsis(fragment)
    if len(parts) < 2:
        return None

    raw_hits: list[list[int]] = []
    for p in parts:
        hits, _stage = grep_fragment(p, prose_lines)
        raw_hits.append(sorted(set(hits)))
    if any(not h for h in raw_hits):
        return None  # not all sub-parts hit at all

    long_indices = [i for i, p in enumerate(parts) if word_count(p) > SHORT_PART_WORD_MAX]
    if long_indices:
        long_pool = sorted({ln for i in long_indices for ln in raw_hits[i]})
        filtered: list[list[int]] = []
        for i, p in enumerate(parts):
            if word_count(p) > SHORT_PART_WORD_MAX:
                filtered.append(raw_hits[i])
            else:
                kept = [ln for ln in raw_hits[i] if any(abs(ln - m) <= MAX_SPAN_LINES for m in long_pool)]
                filtered.append(kept)
        if any(not h for h in filtered):
            return None  # a short sub-part had no hit near any long sibling
    else:
        filtered = raw_hits

    # Bound the combinatorics (small corpus -> this practically never fires,
    # but stay cheap/deterministic if a generic sub-part has many hits).
    combo_size = 1
    for h in filtered:
        combo_size *= len(h)
    if combo_size > 2000:
        filtered = [[h[0]] for h in filtered]

    passing = [c for c in itertools.product(*filtered) if max(c) - min(c) <= MAX_SPAN_LINES]
    if not passing:
        return None

    passing.sort(key=lambda c: (max(c) - min(c), c[0]))
    best = passing[0]
    distinct_combos = set(passing)

    parts_out = [{"text": parts[i], "line": best[i]} for i in range(len(parts))]
    hit_count = 1 if len(distinct_combos) == 1 else len(distinct_combos)

    return _build_result(
        fragment, list(best), "ellipsis-segmented", cite_line=best[0],
        extra={"parts": parts_out, "span": max(best) - min(best), "hit_count": hit_count},
    )


def locate_dialogue_tag_split(fragment: str, prose_lines: list[tuple[int, str]]) -> dict | None:
    """Tier 3: try each internal sentence boundary as a dropped-dialogue-tag
    split point; both halves must independently hit, with some pairing
    landing on the same or an adjacent source line."""
    best: dict | None = None
    best_span = None

    for pos in find_sentence_split_points(fragment):
        left = fragment[:pos].strip()
        right = fragment[pos:].strip()
        if word_count(left) < DIALOGUE_TAG_MIN_PART_WORDS or word_count(right) < DIALOGUE_TAG_MIN_PART_WORDS:
            continue

        left_hits, _ = grep_fragment(left, prose_lines)
        if not left_hits:
            continue
        right_hits, _ = grep_fragment(right, prose_lines)
        if not right_hits:
            continue

        pairs = sorted(
            ((a, b) for a in left_hits for b in right_hits if abs(a - b) <= 1),
            key=lambda ab: (abs(ab[0] - ab[1]), ab[0]),
        )
        if not pairs:
            continue

        a, b = pairs[0]
        span = abs(a - b)
        distinct_pairs = set(pairs)
        hit_count = 1 if (len(left_hits) == 1 and len(right_hits) == 1 and len(distinct_pairs) == 1) \
            else len(distinct_pairs)

        candidate = _build_result(
            fragment, [a, b], "dialogue-tag-strip", cite_line=a,
            extra={
                "parts": [{"text": left, "line": a}, {"text": right, "line": b}],
                "span": span, "hit_count": hit_count,
            },
        )
        if best is None or span < best_span:
            best, best_span = candidate, span

    return best


def locate_candidate(fragment: str, prose_lines: list[tuple[int, str]]) -> dict | None:
    """Tiered grounding for one candidate fragment: whole-fragment grep,
    then (if it contains an ellipsis) segmented grep, then a cheap
    dialogue-tag-strip split. Returns None if nothing grounds."""
    hits, stage = grep_fragment(fragment, prose_lines)
    if hits:
        return _build_result(fragment, hits, stage)

    if _ELLIPSIS_SPLIT_RE.search(fragment):
        seg = locate_ellipsis_segmented(fragment, prose_lines)
        if seg is not None:
            return seg

    return locate_dialogue_tag_split(fragment, prose_lines)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="D&E harvest sidecar drain prep — locate step (deterministic, stdlib-only).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--harvest", default=str(DEFAULT_HARVEST_PATH), metavar="PATH",
                         help=f"Harvest sidecar file. Default: {DEFAULT_HARVEST_PATH}")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), metavar="DIR",
                         help=f"Output directory. Default: {DEFAULT_OUT_DIR}")
    args = parser.parse_args()

    harvest_path = Path(args.harvest)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    produced_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    print(f"Reading {harvest_path} ...")
    raw_lines = harvest_path.read_text(encoding="utf-8", errors="replace").splitlines()
    print(f"  {len(raw_lines):,} raw lines")

    print("Loading whole-novella source files...")
    prose_cache: dict[str, list[tuple[int, str]]] = {}
    for book in BOOKS:
        path = CHAPTERS_DIR / book / f"{book}-dunk-01.md"
        prose_cache[book] = read_prose_lines(path)
        print(f"  {book}: {len(prose_cache[book]):,} prose lines from {path}")

    # -------------------------------------------------------------------
    # Parse rows
    # -------------------------------------------------------------------
    parsed_rows: list[dict] = []
    unparseable: list[tuple[int, str]] = []

    for i, raw in enumerate(raw_lines, start=1):
        if not raw.strip():
            continue
        row = parse_harvest_line(raw, i)
        if row is None:
            unparseable.append((i, raw))
            continue
        parsed_rows.append(row)

    print(f"\nParsed {len(parsed_rows):,} rows ({sum(1 for r in parsed_rows if r['rejoined']):,} "
          f"needed embedded-slash rejoin); {len(unparseable):,} unparseable")
    if unparseable:
        for i, raw in unparseable:
            print(f"  UNPARSEABLE line {i}: {raw!r}", file=sys.stderr)

    kind_counts = Counter(r["kind"] for r in parsed_rows)
    book_counts = Counter(r["book"] for r in parsed_rows)

    # -------------------------------------------------------------------
    # Route: causal-spine -> seeds file (not drained this session)
    # -------------------------------------------------------------------
    causal_spine_rows = [r for r in parsed_rows if r["kind"] == "causal-spine"]
    drainable_rows = [r for r in parsed_rows if r["kind"] != "causal-spine"]

    # -------------------------------------------------------------------
    # Locate step for drainable rows
    # -------------------------------------------------------------------
    located_rows: list[dict] = []
    per_kind_stats: dict[str, Counter] = {}
    no_candidate_rows: list[dict] = []
    ungrounded_examples: list[dict] = []
    ambiguous_examples: list[dict] = []
    recovery_examples: list[dict] = []  # Tier 2/3 recoveries, for transparency in STATS

    match_stage_counts: Counter = Counter()

    for row in drainable_rows:
        book = row["book"].strip().lower()
        prose_lines = prose_cache.get(book)
        kind = row["kind"]
        per_kind_stats.setdefault(kind, Counter())["total"] += 1

        if prose_lines is None:
            print(f"  WARNING: unknown book {row['book']!r} at harvest line {row['source_line']}",
                  file=sys.stderr)
            prose_lines = []

        candidates = collect_candidate_fragments(row["pointer"], row["note"])

        grounded_results: list[dict] = []
        for frag in candidates:
            res = locate_candidate(frag, prose_lines)
            if res is None:
                match_stage_counts["none"] += 1
                continue
            match_stage_counts[res["stage"]] += 1
            grounded_results.append(res)
            if res["stage"] in ("ellipsis-segmented", "dialogue-tag-strip") and len(recovery_examples) < 30:
                recovery_examples.append({**row, "kind": kind, "match": res})

        unique_results = [r for r in grounded_results if r["hit_count"] == 1]
        ambiguous_results = [r for r in grounded_results if 2 <= r["hit_count"] <= 5]

        located = len(unique_results) > 0
        located_ambiguous = (not located) and len(ambiguous_results) > 0

        fragments_out: list[dict] = []
        for r in grounded_results:
            unique = r["hit_count"] == 1
            unusable = r["hit_count"] > 5
            entry_base = {"text": r["text"], "unique": unique, "total_hits": r["hit_count"]}
            if r["stage"] in ("ellipsis-segmented", "dialogue-tag-strip"):
                entry_base["stage"] = r["stage"]
                entry_base["parts"] = r["parts"]
                entry_base["span"] = r["span"]
            if unusable:
                entry_base["unusable"] = True
            for lineno in r["hit_lines"]:
                e = dict(entry_base)
                e["line"] = lineno
                fragments_out.append(e)

        out_row = {
            "book": row["book"],
            "kind": kind,
            "pointer": row["pointer"],
            "note": row["note"],
            "fragments": fragments_out,
            "located": located,
            "located_ambiguous": located_ambiguous,
            "source_line": row["source_line"],
            "rejoined": row["rejoined"],
        }
        located_rows.append(out_row)

        if located:
            per_kind_stats[kind]["located"] += 1
        elif located_ambiguous:
            per_kind_stats[kind]["located_ambiguous"] += 1
            if len(ambiguous_examples) < 30:
                ambiguous_examples.append(out_row)
        else:
            per_kind_stats[kind]["not_located"] += 1
            if not candidates:
                per_kind_stats[kind]["no_candidate_fragments"] += 1
                no_candidate_rows.append(out_row)
            if len(ungrounded_examples) < 50:
                ungrounded_examples.append(out_row)

    # -------------------------------------------------------------------
    # Write outputs
    # -------------------------------------------------------------------
    def write_jsonl(path: Path, rows: list[dict]) -> None:
        with path.open("w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    write_jsonl(out_dir / "causal-spine-seeds.jsonl", causal_spine_rows)
    write_jsonl(out_dir / "located.jsonl", located_rows)

    total_drainable = len(drainable_rows)
    total_located = sum(1 for r in located_rows if r["located"])
    total_ambiguous = sum(1 for r in located_rows if r["located_ambiguous"])
    total_not_located = total_drainable - total_located - total_ambiguous

    lines = [
        "# D&E Harvest Sidecar — LOCATE-STATS",
        "",
        f"> Generated: {produced_at}  ",
        f"> harvest source: {harvest_path}  ",
        "> S222 follow-up: ellipsis segmentation (Tier 2) + dialogue-tag-strip split (Tier 3) "
        "+ located_ambiguous (2-5 hit fragments) added.  ",
        "",
        "## Totals",
        "",
        "| Stage | Count |",
        "|-------|-------|",
        f"| Raw harvest lines | {len(raw_lines):,} |",
        f"| Parsed rows | {len(parsed_rows):,} |",
        f"|  -> needed embedded-slash rejoin | {sum(1 for r in parsed_rows if r['rejoined']):,} |",
        f"| Unparseable rows | {len(unparseable):,} |",
        f"| Routed to causal-spine-seeds.jsonl (NOT drained this session) | {len(causal_spine_rows):,} |",
        f"| Drainable rows (locate attempted) | {total_drainable:,} |",
        f"|  -> located (unique hit) | {total_located:,} |",
        f"|  -> located_ambiguous (2-5 hits, best fragment) | {total_ambiguous:,} |",
        f"|  -> NOT located | {total_not_located:,} |",
        "",
        "## Per-book totals (parsed rows)",
        "",
        "| Book | Count |",
        "|------|-------|",
    ]
    for book, cnt in book_counts.most_common():
        lines.append(f"| {book} | {cnt:,} |")

    lines += [
        "",
        "## Per-kind breakdown (drainable kinds only; causal-spine excluded)",
        "",
        "| Kind | Total | Located | Ambiguous | Not Located | Located % | Located+Ambiguous % | No-candidate rows |",
        "|------|-------|---------|-----------|-------------|-----------|----------------------|--------------------|",
    ]
    for kind in sorted(per_kind_stats, key=lambda k: -per_kind_stats[k]["total"]):
        c = per_kind_stats[kind]
        total = c["total"]
        loc = c["located"]
        amb = c["located_ambiguous"]
        notloc = c["not_located"]
        pct = 100.0 * loc / total if total else 0.0
        pct_both = 100.0 * (loc + amb) / total if total else 0.0
        lines.append(
            f"| {kind} | {total:,} | {loc:,} | {amb:,} | {notloc:,} | {pct:.1f}% | {pct_both:.1f}% | "
            f"{c['no_candidate_fragments']:,} |"
        )

    lines += [
        "",
        "## causal-spine (staged, not drained)",
        "",
        f"{len(causal_spine_rows):,} rows written to `causal-spine-seeds.jsonl` — "
        "these seed a future event-wiring slice, not processed further this session.",
        "",
        "## Fragment grep-stage counts (candidate-level, across all drainable rows)",
        "",
        "| Stage | Count |",
        "|-------|-------|",
        f"| exact (Tier 1) | {match_stage_counts['exact']:,} |",
        f"| normalized (Tier 1 fallback) | {match_stage_counts['normalized']:,} |",
        f"| ellipsis-segmented (Tier 2) | {match_stage_counts['ellipsis-segmented']:,} |",
        f"| dialogue-tag-strip (Tier 3) | {match_stage_counts['dialogue-tag-strip']:,} |",
        f"| none (fragment ungrounded on every tier) | {match_stage_counts['none']:,} |",
        "",
        "## Not-located rows with ZERO candidate fragments (no quotes, pointer <5 words)",
        "",
        f"{len(no_candidate_rows):,} row(s):",
        "",
    ]
    if no_candidate_rows:
        lines.append("| Book | Kind | Pointer | Note | Harvest Line |")
        lines.append("|------|------|---------|------|--------------|")
        for r in no_candidate_rows[:30]:
            lines.append(f"| {r['book']} | {r['kind']} | {r['pointer']} | {r['note'][:80]} | {r['source_line']} |")
    else:
        lines.append("(none)")

    lines += [
        "",
        "## Tier 2/3 recoveries (first 30) — ellipsis-segmented / dialogue-tag-strip hits",
        "",
        f"{len(recovery_examples):,} shown (of {match_stage_counts['ellipsis-segmented'] + match_stage_counts['dialogue-tag-strip']:,} total Tier-2/3 grounded candidates):",
        "",
    ]
    if recovery_examples:
        lines.append("| Book | Kind | Stage | Cite Line | Span | Parts | Harvest Line |")
        lines.append("|------|------|-------|-----------|------|-------|--------------|")
        for r in recovery_examples:
            m = r["match"]
            parts_str = " | ".join(f"{p['text'][:40]}@{p['line']}" for p in m["parts"])
            lines.append(
                f"| {r['book']} | {r['kind']} | {m['stage']} | {m['cite_line']} | {m['span']} | "
                f"{parts_str} | {r['source_line']} |"
            )
    else:
        lines.append("(none)")

    lines += [
        "",
        "## located_ambiguous examples (first 30)",
        "",
        f"{len(ambiguous_examples):,} shown (of {total_ambiguous:,} total):",
        "",
    ]
    if ambiguous_examples:
        lines.append("| Book | Kind | Pointer | Best Fragment Hit-Count | Harvest Line |")
        lines.append("|------|------|---------|--------------------------|--------------|")
        for r in ambiguous_examples:
            best = min((f["total_hits"] for f in r["fragments"] if 2 <= f["total_hits"] <= 5), default="?")
            lines.append(f"| {r['book']} | {r['kind']} | {r['pointer'][:90]} | {best} | {r['source_line']} |")
    else:
        lines.append("(none)")

    lines += [
        "",
        "## Not-located examples (first 50, includes rows WITH candidates that failed to ground on every tier)",
        "",
        "| Book | Kind | Pointer | # Candidates Tried | Harvest Line |",
        "|------|------|---------|---------------------|--------------|",
    ]
    for r in ungrounded_examples:
        n_candidates = len(collect_candidate_fragments(r["pointer"], r["note"]))
        lines.append(f"| {r['book']} | {r['kind']} | {r['pointer'][:90]} | {n_candidates} | {r['source_line']} |")

    lines += [
        "",
        "## Commands run",
        "",
        "```",
        f"python3 scripts/dunk-egg-harvest-locate.py --harvest {harvest_path} --out-dir {out_dir}",
        "```",
        "",
    ]

    (out_dir / "LOCATE-STATS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # -------------------------------------------------------------------
    # Console summary
    # -------------------------------------------------------------------
    print()
    print("=" * 70)
    print("D&E HARVEST LOCATE — RUN SUMMARY (no graph writes)")
    print("=" * 70)
    print(f"  Raw harvest lines:           {len(raw_lines):>6,}")
    print(f"  Parsed rows:                 {len(parsed_rows):>6,}")
    print(f"  Unparseable:                 {len(unparseable):>6,}")
    print(f"  causal-spine (staged):       {len(causal_spine_rows):>6,}")
    print(f"  Drainable rows:              {total_drainable:>6,}")
    print(f"    located:                   {total_located:>6,}")
    print(f"    located_ambiguous:         {total_ambiguous:>6,}")
    print(f"    NOT located:               {total_not_located:>6,}")
    print()
    print("Fragment grep-stage counts:")
    for stage in ("exact", "normalized", "ellipsis-segmented", "dialogue-tag-strip", "none"):
        print(f"  {stage:<20} {match_stage_counts[stage]:>5,}")
    print()
    print("Per-kind (drainable only):")
    for kind in sorted(per_kind_stats, key=lambda k: -per_kind_stats[k]["total"]):
        c = per_kind_stats[kind]
        print(f"  {kind:<18} total={c['total']:>4,}  located={c['located']:>4,}  "
              f"ambiguous={c['located_ambiguous']:>4,}  not_located={c['not_located']:>4,}  "
              f"no-candidates={c['no_candidate_fragments']:>3,}")
    print()
    print(f"Outputs written to: {out_dir}")
    for fname in ["causal-spine-seeds.jsonl", "located.jsonl", "LOCATE-STATS.md"]:
        fpath = out_dir / fname
        n = sum(1 for _ in fpath.open(encoding="utf-8")) if fpath.suffix != ".md" else None
        print(f"  {fname:<26} {n:>6,} lines" if n is not None else f"  {fname}")


if __name__ == "__main__":
    main()
