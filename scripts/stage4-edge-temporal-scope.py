#!/usr/bin/env python3
"""stage4-edge-temporal-scope.py — Temporal scoping and time-aware conflict audit for Weirwood edges.

Each edge in graph/edges/edges.jsonl carries `evidence_book` and `evidence_chapter`.
Each chapter file at sources/chapters/<book>/<slug>.md has YAML frontmatter with
`chapter_number` (global in-book reading order).  Combining these produces a total
temporal order across the series:

    book_order × chapter_number
    agot=1, acok=2, asos=3, affc=4, adwd=5

This script has two modes (both run by default):

  ANNOTATE mode
    Emits an annotated copy of edges.jsonl to a new file (default
    working/wiki/data/edges-temporal-scoped.jsonl) where every row gains
    three fields:
      - book_order      : int 1-5 (null if unresolvable)
      - chapter_number  : int from frontmatter (null if unresolvable)
      - temporal_key    : "b{book_order}-c{N:03d}" string, or null

    NEVER writes to graph/edges/edges.jsonl.

  TEMPORAL-AWARE CONFLICT AUDIT
    Re-runs the same incompatible-type detection from graph-conflict-pairs.py,
    but for each flagged incompatible type-pair on an entity pair, classifies it:

      CROSS-WINDOW (resolved temporal arc)
          Incompatible edges occur in DIFFERENT time windows — legitimate because
          ASOIAF relationships evolve across 5 books.  E.g. Daenerys TRUSTS Jorah
          in AGOT but DISTRUSTS him in ADWD after the betrayal reveal.

      SAME-WINDOW (true conflict)
          Incompatible edges occur in the SAME time window — genuine anomaly
          needing human review.

    Window granularity is set by --window:
      book    (default) — window = evidence_book; different books → cross-window
      chapter           — window = exact (book_order, chapter_number); same chapter only

    Outputs:
      - working/wiki/data/graph-conflict-pairs-temporal.md   (reviewer-facing)
      - working/wiki/data/graph-conflict-pairs-temporal.jsonl (machine-readable)

Both --window=book and --window=chapter counts are always printed in the stdout
summary so you can see the sensitivity at a glance.

Usage:
  # Defaults (--window book, standard output paths):
  python3 scripts/stage4-edge-temporal-scope.py

  # Override window:
  python3 scripts/stage4-edge-temporal-scope.py --window chapter

  # Override all paths:
  python3 scripts/stage4-edge-temporal-scope.py \\
      --edges graph/edges/edges.jsonl \\
      --annotated-out working/wiki/data/edges-temporal-scoped.jsonl \\
      --out-md working/wiki/data/graph-conflict-pairs-temporal.md \\
      --out-jsonl working/wiki/data/graph-conflict-pairs-temporal.jsonl

$0, no LLM, no network.  Read-only on graph/edges/edges.jsonl.  Delete nothing.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

DEFAULT_EDGES_FILE    = PROJECT_ROOT / "graph" / "edges" / "edges.jsonl"
DEFAULT_CHAPTERS_ROOT = PROJECT_ROOT / "sources" / "chapters"
DEFAULT_ANNOTATED_OUT = PROJECT_ROOT / "working" / "wiki" / "data" / "edges-temporal-scoped.jsonl"
DEFAULT_OUT_MD        = PROJECT_ROOT / "working" / "wiki" / "data" / "graph-conflict-pairs-temporal.md"
DEFAULT_OUT_JSONL     = PROJECT_ROOT / "working" / "wiki" / "data" / "graph-conflict-pairs-temporal.jsonl"

# ---------------------------------------------------------------------------
# Book ordering
# ---------------------------------------------------------------------------
BOOK_ORDER: dict[str, int] = {
    "agot": 1,
    "acok": 2,
    "asos": 3,
    "affc": 4,
    "adwd": 5,
}

# ---------------------------------------------------------------------------
# Semantic incompatibility table — kept in sync with graph-conflict-pairs.py.
#
# Each frozenset({TYPE_A, TYPE_B}) means: if an entity pair carries BOTH types
# (in ANY direction), flag it for review.  See graph-conflict-pairs.py for the
# full design commentary and the "how to extend" guidance.
# ---------------------------------------------------------------------------
INCOMPATIBLE_PAIRS: set[frozenset] = {
    frozenset({"LOVES", "HATES"}),
    frozenset({"ALLIES_WITH", "OPPOSES"}),
    frozenset({"TRUSTS", "DISTRUSTS"}),
    frozenset({"PROTECTS", "ATTACKS"}),
    frozenset({"PROTECTS", "ASSAULTS"}),
}

# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------
_FM_PATTERN = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
_FIELD_PATTERN = re.compile(r"^(\w+)\s*:\s*(.+)$", re.MULTILINE)


def parse_frontmatter_fields(text: str) -> dict[str, str]:
    """Extract key/value pairs from a YAML-style frontmatter block.

    Only handles simple scalar fields (no nested YAML).  Quoted values
    have their outer quotes stripped.  Returns {} if no frontmatter found.
    """
    m = _FM_PATTERN.match(text)
    if not m:
        return {}
    fm_body = m.group(1)
    result: dict[str, str] = {}
    for field_m in _FIELD_PATTERN.finditer(fm_body):
        key = field_m.group(1).strip()
        val = field_m.group(2).strip().strip('"').strip("'")
        result[key] = val
    return result


# ---------------------------------------------------------------------------
# Chapter lookup — build once from sources/chapters/<book>/*.md
# ---------------------------------------------------------------------------

def build_chapter_lookup(chapters_root: Path) -> tuple[dict[str, tuple[int | None, int | None]], int, int]:
    """Scan all chapter frontmatter files and return a slug → (book_order, chapter_number) map.

    Returns:
        lookup: dict mapping evidence_chapter slug (e.g. "agot-bran-01") to
                (book_order, chapter_number).  Both values are ints when resolved;
                the tuple is (None, None) if frontmatter is unreadable.
        resolved: count of successfully resolved chapters
        unresolved: count of files whose frontmatter was incomplete/missing
    """
    lookup: dict[str, tuple[int | None, int | None]] = {}
    resolved = 0
    unresolved = 0

    for book_slug, order in BOOK_ORDER.items():
        book_dir = chapters_root / book_slug
        if not book_dir.is_dir():
            continue
        for md_file in sorted(book_dir.glob("*.md")):
            slug = md_file.stem  # e.g. "agot-bran-01"
            try:
                text = md_file.read_text(encoding="utf-8")
            except OSError as exc:
                print(f"  WARNING: could not read {md_file}: {exc}", file=sys.stderr)
                lookup[slug] = (None, None)
                unresolved += 1
                continue

            fields = parse_frontmatter_fields(text)
            cn_raw = fields.get("chapter_number", "")
            if cn_raw:
                try:
                    cn = int(cn_raw)
                    lookup[slug] = (order, cn)
                    resolved += 1
                    continue
                except ValueError:
                    pass  # fall through to unresolved

            print(
                f"  WARNING: missing/invalid chapter_number in frontmatter: {md_file.name}",
                file=sys.stderr,
            )
            lookup[slug] = (None, None)
            unresolved += 1

    return lookup, resolved, unresolved


# ---------------------------------------------------------------------------
# Temporal key helpers
# ---------------------------------------------------------------------------

def temporal_key_string(book_order: int | None, chapter_number: int | None) -> str | None:
    """Return a sortable temporal key string like 'b1-c008', or None if unresolvable."""
    if book_order is None or chapter_number is None:
        return None
    return f"b{book_order}-c{chapter_number:03d}"


def annotate_edge(edge: dict, chapter_lookup: dict) -> dict:
    """Return a new edge dict with book_order, chapter_number, temporal_key added."""
    chapter_slug = edge.get("evidence_chapter", "")
    if chapter_slug and chapter_slug in chapter_lookup:
        bo, cn = chapter_lookup[chapter_slug]
    else:
        bo, cn = None, None
    annotated = dict(edge)
    annotated["book_order"] = bo
    annotated["chapter_number"] = cn
    annotated["temporal_key"] = temporal_key_string(bo, cn)
    return annotated


# ---------------------------------------------------------------------------
# Window-based classification helpers
# ---------------------------------------------------------------------------

def window_key(edge: dict, window: str) -> object:
    """Return the window bucket for an annotated edge.

    With --window book  : returns the evidence_book string (e.g. "agot")
                          — or book_order int if evidence_book is missing.
    With --window chapter: returns the temporal_key string (e.g. "b1-c008")
                          — or None if unresolvable (treated as its own bucket,
                            null_window, which never matches any real window).

    Two edges share a window if window_key(e1) == window_key(e2) AND neither
    is None/null (null keys are treated as "unresolvable — conservatively
    do NOT classify as same-window so we don't generate false true-conflicts").
    """
    if window == "book":
        # Prefer the raw evidence_book string for readability; it's always present.
        return edge.get("evidence_book") or edge.get("book_order")
    else:  # "chapter"
        return edge.get("temporal_key")  # None if unresolvable


def same_window(key_a: object, key_b: object) -> bool:
    """True if both keys are non-None and equal (i.e. same time window)."""
    if key_a is None or key_b is None:
        return False
    return key_a == key_b


# ---------------------------------------------------------------------------
# Edge loading
# ---------------------------------------------------------------------------

def load_edges(edges_path: Path) -> list[dict]:
    """Load all edges from a JSONL file.  Returns list of dicts."""
    edges = []
    with open(edges_path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                edges.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(
                    f"  WARNING: skipping malformed JSON on line {lineno}: {exc}",
                    file=sys.stderr,
                )
    return edges


# ---------------------------------------------------------------------------
# Annotated output writer
# ---------------------------------------------------------------------------

def write_annotated_edges(annotated: list[dict], out_path: Path) -> None:
    """Write annotated edges to JSONL (one row per edge)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        for edge in annotated:
            fh.write(json.dumps(edge, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Temporal-aware conflict detection
# ---------------------------------------------------------------------------

def classify_incompatible_pair_window(
    type_a: str,
    type_b: str,
    edges_for_pair: list[dict],
    window: str,
) -> str:
    """Classify a single incompatible type-pair as SAME_WINDOW or CROSS_WINDOW.

    An incompatible type-pair (e.g. TRUSTS + DISTRUSTS) on an entity pair is:
      SAME_WINDOW   — at least one TRUSTS edge and at least one DISTRUSTS edge
                      share the same window key (true conflict).
      CROSS_WINDOW  — all TRUSTS edges are in different windows from all DISTRUSTS
                      edges (resolved temporal arc).
      SAME_WINDOW   — if any edge for either type has a null temporal key, we
                      conservatively do NOT claim it's cross-window (could be
                      same-window but unverifiable).  Flag as SAME_WINDOW so a
                      human reviews it.
    """
    a_keys = [window_key(e, window) for e in edges_for_pair if e.get("edge_type") == type_a]
    b_keys = [window_key(e, window) for e in edges_for_pair if e.get("edge_type") == type_b]

    if not a_keys or not b_keys:
        # One side has no edges — can't classify (shouldn't happen if we got here)
        return "CROSS_WINDOW"

    # If any key is None, we can't prove cross-window → conservative SAME_WINDOW
    if any(k is None for k in a_keys) or any(k is None for k in b_keys):
        return "SAME_WINDOW"

    # Check: does any (a_key, b_key) pair share a window?
    a_set = set(a_keys)
    b_set = set(b_keys)
    if a_set & b_set:
        return "SAME_WINDOW"
    return "CROSS_WINDOW"


def detect_temporal_conflicts(
    pair: frozenset,
    edges: list[dict],
    window: str,
) -> dict | None:
    """Temporal-aware conflict detection for a single entity pair.

    Returns a conflict record (dict) or None if no incompatibilities found.
    The record includes each incompatible type-pair annotated as
    SAME_WINDOW or CROSS_WINDOW.
    """
    slugs = sorted(pair)
    a_slug, b_slug = slugs[0], slugs[1]

    # Collect all edge types for this pair (across directions).
    all_types: set[str] = {e.get("edge_type", "") for e in edges}

    # Find which INCOMPATIBLE_PAIRS fire.
    found_incompatible: list[frozenset] = []
    for incompat in INCOMPATIBLE_PAIRS:
        if incompat.issubset(all_types):
            found_incompatible.append(incompat)

    if not found_incompatible:
        return None

    # Classify each incompatible pair as SAME_WINDOW or CROSS_WINDOW.
    classified: list[dict] = []
    has_same_window = False
    for incompat in found_incompatible:
        type_a, type_b = sorted(incompat)  # stable string order
        classification = classify_incompatible_pair_window(type_a, type_b, edges, window)
        if classification == "SAME_WINDOW":
            has_same_window = True
        classified.append({
            "type_a": type_a,
            "type_b": type_b,
            "classification": classification,
        })

    # Build flagged edge details (only types involved in some incompatible pair).
    flagged_types: set[str] = set()
    for incompat in found_incompatible:
        flagged_types |= incompat

    conflict_edges = []
    for edge in edges:
        etype = edge.get("edge_type", "")
        if etype not in flagged_types:
            continue
        src = edge.get("source_slug", "")
        tgt = edge.get("target_slug", "")
        conflict_edges.append({
            "direction": f"{src} -> {tgt}",
            "edge_type": etype,
            "evidence_ref": edge.get("evidence_ref", ""),
            "evidence_quote": edge.get("evidence_quote", ""),
            "confidence_tier": edge.get("confidence_tier", ""),
            "evidence_book": edge.get("evidence_book", ""),
            "evidence_chapter": edge.get("evidence_chapter", ""),
            "temporal_key": edge.get("temporal_key"),
        })

    conflict_edges.sort(key=lambda e: (e["edge_type"], e["direction"]))

    overall_classification = "SAME_WINDOW" if has_same_window else "CROSS_WINDOW"

    return {
        "slug_a": a_slug,
        "slug_b": b_slug,
        "overall_classification": overall_classification,
        "window": window,
        "classified_incompatible_pairs": classified,
        "all_edge_types_on_pair": sorted(all_types),
        "total_edges_on_pair": len(edges),
        "conflict_edges": conflict_edges,
    }


def group_by_pair(edges: list[dict]) -> dict[frozenset, list[dict]]:
    """Group annotated edges by unordered entity pair.  Self-loops excluded."""
    groups: dict = defaultdict(list)
    self_loop_count = 0
    for edge in edges:
        src = edge.get("source_slug", "")
        tgt = edge.get("target_slug", "")
        if not src or not tgt:
            continue
        if src == tgt:
            self_loop_count += 1
            continue
        pair = frozenset({src, tgt})
        groups[pair].append(edge)
    if self_loop_count:
        print(f"  NOTE: skipped {self_loop_count} self-loop edge(s).", file=sys.stderr)
    return dict(groups)


def find_temporal_conflicts(
    grouped: dict[frozenset, list[dict]],
    window: str,
) -> list[dict]:
    """Run temporal-aware conflict detection across all entity pairs."""
    conflicts = []
    for pair, edges in grouped.items():
        result = detect_temporal_conflicts(pair, edges, window)
        if result is not None:
            conflicts.append(result)

    # Sort: SAME_WINDOW (true conflicts) first, then by slug pair.
    def sort_key(rec: dict) -> tuple:
        order = {"SAME_WINDOW": 0, "CROSS_WINDOW": 1}
        return (order.get(rec["overall_classification"], 2), rec["slug_a"], rec["slug_b"])

    conflicts.sort(key=sort_key)
    return conflicts


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def _truncate(text: str, max_len: int = 200) -> str:
    """Truncate long strings for display."""
    if not text:
        return "(none)"
    text = text.replace("\n", " ").strip()
    if len(text) > max_len:
        return text[:max_len] + "…"
    return text


def write_temporal_markdown(
    conflicts: list[dict],
    total_pairs: int,
    original_flagged: int,
    window: str,
    out_path: Path,
    # Also pass the "other window" summary for sensitivity reporting
    other_window_true_count: int,
    other_window_arc_count: int,
    other_window_label: str,
) -> None:
    """Write temporal-aware reviewer-facing markdown report."""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    true_conflicts = [c for c in conflicts if c["overall_classification"] == "SAME_WINDOW"]
    arcs = [c for c in conflicts if c["overall_classification"] == "CROSS_WINDOW"]

    # Count breakdown by incompatible type pair within true conflicts
    type_pair_counts: dict[str, int] = defaultdict(int)
    for c in true_conflicts:
        for cp in c["classified_incompatible_pairs"]:
            if cp["classification"] == "SAME_WINDOW":
                key = f"{cp['type_a']} × {cp['type_b']}"
                type_pair_counts[key] += 1

    lines: list[str] = []
    lines.append("# Graph Conflict Pairs — Temporal-Aware Review Queue")
    lines.append("")
    lines.append(
        "Generated by `scripts/stage4-edge-temporal-scope.py`.  Read-only audit — "
        "**do not auto-delete**.  Incompatible edge types in DIFFERENT time windows are "
        "legitimate temporal arcs (ASOIAF relationships evolve across 5 books).  Only "
        "SAME-WINDOW incompatibilities are true conflicts needing human review."
    )
    lines.append("")
    lines.append(f"**Window granularity used for this report:** `--window {window}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|--------|-------|")
    lines.append(f"| Total entity pairs analyzed | {total_pairs:,} |")
    lines.append(f"| Originally flagged pairs (any incompatibility) | {original_flagged:,} |")
    lines.append(f"| Resolved as temporal arcs (`--window {window}`) | {len(arcs)} |")
    lines.append(f"| **TRUE same-window conflicts (`--window {window}`)** | **{len(true_conflicts)}** |")
    lines.append("")
    lines.append("### Sensitivity across window granularities")
    lines.append("")
    lines.append("| Window | True Conflicts | Resolved Arcs |")
    lines.append("|--------|---------------|---------------|")
    lines.append(f"| `--window {window}` (this report) | {len(true_conflicts)} | {len(arcs)} |")
    lines.append(f"| `--window {other_window_label}` | {other_window_true_count} | {other_window_arc_count} |")
    lines.append("")
    if type_pair_counts:
        lines.append("### True-conflict breakdown by incompatible type pair")
        lines.append("")
        lines.append("| Incompatible Type Pair | Flagged Pairs |")
        lines.append("|------------------------|--------------|")
        for key, cnt in sorted(type_pair_counts.items(), key=lambda x: -x[1]):
            lines.append(f"| {key} | {cnt} |")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## TRUE Same-Window Conflicts (human review queue)")
    lines.append("")
    if not true_conflicts:
        lines.append("*No true same-window conflicts detected under this window granularity.*")
        lines.append("")
    else:
        lines.append(
            "> These are the pairs where semantically incompatible edge types appear "
            "within the SAME time window.  These are the real review queue."
        )
        lines.append("")
        for i, c in enumerate(true_conflicts, 1):
            same_pairs = [
                cp for cp in c["classified_incompatible_pairs"]
                if cp["classification"] == "SAME_WINDOW"
            ]
            incompat_str = ", ".join(f"{cp['type_a']} × {cp['type_b']}" for cp in same_pairs)
            lines.append(f"### {i}. `{c['slug_a']}` ↔ `{c['slug_b']}`")
            lines.append("")
            lines.append(f"- **Overall classification:** TRUE CONFLICT (SAME-WINDOW)")
            lines.append(f"- **Same-window incompatible pairs:** {incompat_str}")
            lines.append(f"- **All edge types on this pair:** {', '.join(c['all_edge_types_on_pair'])}")
            lines.append(f"- **Total edges between pair:** {c['total_edges_on_pair']}")
            lines.append("")
            lines.append("| Direction | Type | Confidence | Temporal Key | Evidence Ref | Quote |")
            lines.append("|-----------|------|-----------|-------------|-------------|-------|")
            for edge in c["conflict_edges"]:
                quote = _truncate(edge["evidence_quote"], 120)
                quote = quote.replace("|", "\\|")
                tk = edge["temporal_key"] or "(null)"
                lines.append(
                    f"| `{edge['direction']}` "
                    f"| {edge['edge_type']} "
                    f"| T{edge['confidence_tier']} "
                    f"| `{tk}` "
                    f"| `{edge['evidence_ref']}` "
                    f"| {quote} |"
                )
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Resolved Temporal Arcs")
    lines.append("")
    if not arcs:
        lines.append("*No pairs classified as resolved arcs under this window granularity.*")
        lines.append("")
    else:
        lines.append(
            "> These pairs have incompatible edge types but in DIFFERENT time windows — "
            "legitimate because the relationship evolved.  Listed for completeness; "
            "no human review needed unless the temporal separation looks wrong."
        )
        lines.append("")
        lines.append("| Entity Pair | Incompatible Types | Windows Spanned |")
        lines.append("|-------------|-------------------|-----------------|")
        for c in arcs:
            pair_str = f"`{c['slug_a']}` ↔ `{c['slug_b']}`"
            incompat_str = ", ".join(
                f"{cp['type_a']} × {cp['type_b']}"
                for cp in c["classified_incompatible_pairs"]
            )
            # Collect temporal keys present in flagged edges
            tkeys = sorted({
                e["temporal_key"] for e in c["conflict_edges"]
                if e["temporal_key"]
            })
            tkeys_str = ", ".join(tkeys) if tkeys else "(null)"
            lines.append(f"| {pair_str} | {incompat_str} | {tkeys_str} |")
        lines.append("")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_temporal_jsonl(conflicts: list[dict], out_path: Path) -> None:
    """Write machine-readable JSONL (one record per flagged pair)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        for record in conflicts:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Annotate graph edges with temporal keys and run a temporal-aware "
            "incompatible-type conflict audit."
        )
    )
    p.add_argument(
        "--edges",
        type=Path,
        default=DEFAULT_EDGES_FILE,
        metavar="PATH",
        help=f"Path to edges.jsonl (default: {DEFAULT_EDGES_FILE})",
    )
    p.add_argument(
        "--chapters-root",
        type=Path,
        default=DEFAULT_CHAPTERS_ROOT,
        metavar="PATH",
        help=f"Root directory for chapter files (default: {DEFAULT_CHAPTERS_ROOT})",
    )
    p.add_argument(
        "--annotated-out",
        type=Path,
        default=DEFAULT_ANNOTATED_OUT,
        metavar="PATH",
        help=f"Output path for annotated edges JSONL (default: {DEFAULT_ANNOTATED_OUT})",
    )
    p.add_argument(
        "--out-md",
        type=Path,
        default=DEFAULT_OUT_MD,
        metavar="PATH",
        help=f"Output markdown conflict report path (default: {DEFAULT_OUT_MD})",
    )
    p.add_argument(
        "--out-jsonl",
        type=Path,
        default=DEFAULT_OUT_JSONL,
        metavar="PATH",
        help=f"Output JSONL conflict report path (default: {DEFAULT_OUT_JSONL})",
    )
    p.add_argument(
        "--window",
        choices=["book", "chapter"],
        default="book",
        metavar="GRANULARITY",
        help="Window granularity for conflict classification: 'book' (default) or 'chapter'.",
    )
    return p


def main() -> None:
    args = build_parser().parse_args()

    # ------------------------------------------------------------------
    # Validate inputs
    # ------------------------------------------------------------------
    if not args.edges.exists():
        print(f"ERROR: edges file not found: {args.edges}", file=sys.stderr)
        sys.exit(1)
    if not args.chapters_root.exists():
        print(f"ERROR: chapters root not found: {args.chapters_root}", file=sys.stderr)
        sys.exit(1)

    # Confirm we are NOT writing to the canonical edges file.
    canonical_edges = PROJECT_ROOT / "graph" / "edges" / "edges.jsonl"
    if args.annotated_out.resolve() == canonical_edges.resolve():
        print(
            "ERROR: --annotated-out must not point to graph/edges/edges.jsonl. "
            "This script never mutates the canonical edge file.",
            file=sys.stderr,
        )
        sys.exit(1)

    # ------------------------------------------------------------------
    # Step 1: Build chapter → (book_order, chapter_number) lookup
    # ------------------------------------------------------------------
    print(f"Building chapter lookup from: {args.chapters_root}")
    chapter_lookup, resolved, unresolved = build_chapter_lookup(args.chapters_root)
    print(f"  {resolved + unresolved} chapter files found: "
          f"{resolved} resolved, {unresolved} unresolved.")

    # ------------------------------------------------------------------
    # Step 2: Load edges
    # ------------------------------------------------------------------
    print(f"\nLoading edges from: {args.edges}")
    edges = load_edges(args.edges)
    print(f"  Loaded {len(edges):,} edges.")

    # ------------------------------------------------------------------
    # Step 3: Annotate with temporal keys
    # ------------------------------------------------------------------
    print("\nAnnotating edges with temporal keys...")
    annotated = [annotate_edge(e, chapter_lookup) for e in edges]

    # Count null temporal keys
    null_count = sum(1 for e in annotated if e["temporal_key"] is None)
    resolvable_count = len(annotated) - null_count

    # Report unresolvable evidence_chapter slugs (distinct)
    unresolvable_slugs = sorted({
        e.get("evidence_chapter", "(missing)")
        for e in annotated
        if e["temporal_key"] is None
    })
    print(f"  {resolvable_count:,} edges with resolved temporal key.")
    print(f"  {null_count:,} edges with null temporal key.")
    if unresolvable_slugs:
        print(f"  Unresolvable chapter slugs ({len(unresolvable_slugs)}):")
        for slug in unresolvable_slugs[:20]:
            print(f"    - {slug!r}")
        if len(unresolvable_slugs) > 20:
            print(f"    ... and {len(unresolvable_slugs) - 20} more")

    # ------------------------------------------------------------------
    # Step 4: Write annotated edges output
    # ------------------------------------------------------------------
    print(f"\nWriting annotated edges to: {args.annotated_out}")
    write_annotated_edges(annotated, args.annotated_out)

    # ------------------------------------------------------------------
    # Step 5: Temporal-aware conflict audit (primary window)
    # ------------------------------------------------------------------
    print(f"\nRunning temporal-aware conflict audit (--window {args.window})...")
    grouped = group_by_pair(annotated)
    total_pairs = len(grouped)
    print(f"  {total_pairs:,} unique entity pairs.")

    conflicts_primary = find_temporal_conflicts(grouped, args.window)
    true_primary = [c for c in conflicts_primary if c["overall_classification"] == "SAME_WINDOW"]
    arc_primary = [c for c in conflicts_primary if c["overall_classification"] == "CROSS_WINDOW"]
    print(f"  Total flagged pairs (any incompatibility): {len(conflicts_primary)}")
    print(f"  → TRUE same-window conflicts:   {len(true_primary)}")
    print(f"  → Resolved temporal arcs:       {len(arc_primary)}")

    # ------------------------------------------------------------------
    # Step 6: Run other window for sensitivity comparison
    # ------------------------------------------------------------------
    other_window = "chapter" if args.window == "book" else "book"
    print(f"\nRunning sensitivity check (--window {other_window})...")
    conflicts_other = find_temporal_conflicts(grouped, other_window)
    true_other = [c for c in conflicts_other if c["overall_classification"] == "SAME_WINDOW"]
    arc_other = [c for c in conflicts_other if c["overall_classification"] == "CROSS_WINDOW"]
    print(f"  → TRUE same-window conflicts:   {len(true_other)}")
    print(f"  → Resolved temporal arcs:       {len(arc_other)}")

    # ------------------------------------------------------------------
    # Step 7: Write conflict report outputs
    # ------------------------------------------------------------------
    original_flagged = len(conflicts_primary)  # same total regardless of window

    print(f"\nWriting temporal conflict markdown to: {args.out_md}")
    write_temporal_markdown(
        conflicts=conflicts_primary,
        total_pairs=total_pairs,
        original_flagged=original_flagged,
        window=args.window,
        out_path=args.out_md,
        other_window_true_count=len(true_other),
        other_window_arc_count=len(arc_other),
        other_window_label=other_window,
    )

    print(f"Writing temporal conflict JSONL to:    {args.out_jsonl}")
    write_temporal_jsonl(conflicts_primary, args.out_jsonl)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  {len(edges):,} edges read (source: {args.edges})")
    print(f"  {resolvable_count:,} / {len(edges):,} edges with resolved temporal key")
    print(f"  {total_pairs:,} unique entity pairs")
    print(f"  {original_flagged} pairs with ANY incompatible type combination")
    print()
    print(f"  Window = '{args.window}':")
    print(f"    TRUE same-window conflicts : {len(true_primary)}")
    print(f"    Resolved temporal arcs     : {len(arc_primary)}")
    print()
    print(f"  Window = '{other_window}' (sensitivity):")
    print(f"    TRUE same-window conflicts : {len(true_other)}")
    print(f"    Resolved temporal arcs     : {len(arc_other)}")
    print()
    if true_primary:
        print(f"  TRUE CONFLICT PAIRS (review queue under --window {args.window}):")
        for c in true_primary:
            same_pairs = [
                cp for cp in c["classified_incompatible_pairs"]
                if cp["classification"] == "SAME_WINDOW"
            ]
            incompat_str = ", ".join(f"{cp['type_a']}+{cp['type_b']}" for cp in same_pairs)
            tkeys = sorted({
                e["temporal_key"] for e in c["conflict_edges"] if e["temporal_key"]
            })
            print(f"    {c['slug_a']} ↔ {c['slug_b']}")
            print(f"      types: {incompat_str}")
            print(f"      keys:  {', '.join(tkeys) if tkeys else '(null)'}")
    else:
        print(f"  No true same-window conflicts under --window {args.window}.")
    print()
    print(f"  Outputs:")
    print(f"    Annotated edges : {args.annotated_out}")
    print(f"    Conflict MD     : {args.out_md}")
    print(f"    Conflict JSONL  : {args.out_jsonl}")
    print("=" * 60)
    print("Done.")


if __name__ == "__main__":
    main()
