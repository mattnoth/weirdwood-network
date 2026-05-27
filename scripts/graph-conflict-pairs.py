#!/usr/bin/env python3
"""graph-conflict-pairs.py — Read-only semantic-conflict audit for Weirwood edge layer.

Scans graph/edges/edges.jsonl for entity pairs that carry semantically incompatible
edge types (e.g. LOVES + HATES on the same pair).  Produces a human/Opus review queue
with full citations so a reviewer can click straight to the source line.

This is a $0, NO-LLM, deterministic tool.  It does NOT modify edges.jsonl.

Sentiment legitimately coexists across 5 books (Tyrion loves and hates Cersei at
different times).  The output is a PRIORITIZED REVIEW QUEUE, not an auto-delete list.
Flag counts should be treated as "needs human review" rather than "definitely wrong".

Usage:
  # Default: reads graph/edges/edges.jsonl, writes working/wiki/data/
  python3 scripts/graph-conflict-pairs.py

  # Custom paths:
  python3 scripts/graph-conflict-pairs.py --edges PATH/TO/edges.jsonl
  python3 scripts/graph-conflict-pairs.py --out-md PATH/TO/report.md
  python3 scripts/graph-conflict-pairs.py --out-jsonl PATH/TO/conflicts.jsonl
  python3 scripts/graph-conflict-pairs.py --edges PATH --out-md PATH --out-jsonl PATH

$0, no LLM.  Read-only on graph/edges/edges.jsonl.  Delete nothing.
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

DEFAULT_EDGES_FILE = PROJECT_ROOT / "graph" / "edges" / "edges.jsonl"
DEFAULT_OUT_MD = PROJECT_ROOT / "working" / "wiki" / "data" / "graph-conflict-pairs.md"
DEFAULT_OUT_JSONL = PROJECT_ROOT / "working" / "wiki" / "data" / "graph-conflict-pairs.jsonl"

# ---------------------------------------------------------------------------
# Semantic incompatibility table
# ---------------------------------------------------------------------------
# Each frozenset({TYPE_A, TYPE_B}) means: if an entity pair carries BOTH types
# (in ANY direction), flag it for review.
#
# Design principles:
#   1. CONSERVATIVE — ASOIAF relationships are genuinely complex across 5 books.
#      Only add a pair here if you would be surprised to see both types on the
#      same entity pair within a single book, let alone the full series.
#   2. DIRECTIONAL NUANCE — opposite-direction instances (A loves B, B hates A)
#      are weaker signals than same-direction (A loves B, A hates B); we detect
#      and label both but sort same-direction first.
#   3. HOW TO EXTEND — add a new frozenset to this set only when:
#      a. The types are semantic antonyms, not just different valences
#      b. You have verified both types actually exist in the data (run with
#         --edges <path> and read the vocabulary header it prints)
#      c. You accept that legitimate co-occurrence will generate false-positives
#         (e.g. war-period TRUSTS followed by post-betrayal DISTRUSTS IS
#         legitimate but still flagged — the reviewer resolves it)
#
# Types verified to exist in data (all 9 confirmed present):
#   LOVES (121), HATES (173), ALLIES_WITH (91), OPPOSES (265),
#   TRUSTS (84), DISTRUSTS (204), PROTECTS (157), ATTACKS (22), ASSAULTS (32)
INCOMPATIBLE_PAIRS: set[frozenset] = {
    frozenset({"LOVES", "HATES"}),
    frozenset({"ALLIES_WITH", "OPPOSES"}),
    frozenset({"TRUSTS", "DISTRUSTS"}),
    frozenset({"PROTECTS", "ATTACKS"}),
    frozenset({"PROTECTS", "ASSAULTS"}),
}


# ---------------------------------------------------------------------------
# Core logic
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
                print(f"  WARNING: skipping malformed JSON on line {lineno}: {exc}", file=sys.stderr)
    return edges


def group_by_pair(edges: list[dict]) -> dict[frozenset, list[dict]]:
    """Group edges by unordered entity pair {source_slug, target_slug}.

    Self-loops (source == target) are excluded — they cannot produce a
    directional conflict in any meaningful sense.
    """
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


def detect_conflicts(pair: frozenset, edges: list[dict]) -> dict | None:
    """Detect incompatible edge-type combinations on a single entity pair.

    Returns a conflict record dict or None if no incompatibilities found.

    Conflict directionality categories:
      same      — e.g. A LOVES B + A HATES B  (strongest mis-type signal)
      opposite  — e.g. A LOVES B + B HATES A  (weaker; both can be true)
      both      — both same-direction AND opposite-direction conflicts present
    """
    # Collect type sets by direction.
    # For each edge, normalize direction: we sort slugs to define "canonical A"
    # but preserve the actual direction label.
    slugs = sorted(pair)  # deterministic ordering: slugs[0] is "A", slugs[1] is "B"
    a_slug, b_slug = slugs[0], slugs[1]

    # direction buckets: "a_to_b" and "b_to_a"
    a_to_b_types: set[str] = set()
    b_to_a_types: set[str] = set()
    for edge in edges:
        etype = edge.get("edge_type", "")
        src = edge.get("source_slug", "")
        if src == a_slug:
            a_to_b_types.add(etype)
        else:
            b_to_a_types.add(etype)

    all_types = a_to_b_types | b_to_a_types

    # Check each incompatible pair against this entity pair's type set.
    found_incompatible: list[frozenset] = []
    for incompat in INCOMPATIBLE_PAIRS:
        if incompat.issubset(all_types):
            found_incompatible.append(incompat)

    if not found_incompatible:
        return None

    # Classify directionality of each conflict.
    has_same = False
    has_opposite = False

    for incompat in found_incompatible:
        type_a, type_b = sorted(incompat)  # stable order for reporting
        # same-direction: both types appear from the same source slug
        if (type_a in a_to_b_types and type_b in a_to_b_types) or \
           (type_a in b_to_a_types and type_b in b_to_a_types):
            has_same = True
        # opposite-direction: one type from A→B, other from B→A
        if (type_a in a_to_b_types and type_b in b_to_a_types) or \
           (type_a in b_to_a_types and type_b in a_to_b_types):
            has_opposite = True

    if has_same and has_opposite:
        directionality = "both"
    elif has_same:
        directionality = "same"
    else:
        directionality = "opposite"

    # Build sorted edge detail list — keep only edges whose type is in any
    # incompatible pair we detected (avoids flooding with unrelated edges).
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
        })

    # Sort: same-direction contributors first (source==a_slug and lower-sorted types first)
    conflict_edges.sort(key=lambda e: (e["edge_type"], e["direction"]))

    return {
        "slug_a": a_slug,
        "slug_b": b_slug,
        "conflict_directionality": directionality,
        "incompatible_type_pairs": [sorted(list(ip)) for ip in found_incompatible],
        "all_edge_types_on_pair": sorted(all_types),
        "total_edges_on_pair": len(edges),
        "conflict_edges": conflict_edges,
    }


def _sort_key(record: dict) -> tuple:
    """Sort key for output: same-direction conflicts first, then by pair slugs."""
    order = {"same": 0, "both": 1, "opposite": 2}
    return (order.get(record["conflict_directionality"], 3), record["slug_a"], record["slug_b"])


def find_all_conflicts(grouped: dict[frozenset, list[dict]]) -> list[dict]:
    """Run conflict detection across all entity pairs.  Returns sorted list."""
    conflicts = []
    for pair, edges in grouped.items():
        result = detect_conflicts(pair, edges)
        if result is not None:
            conflicts.append(result)
    conflicts.sort(key=_sort_key)
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


def write_markdown(conflicts: list[dict], total_pairs: int, out_path: Path) -> None:
    """Write reviewer-facing markdown report."""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Breakdown stats
    same_count = sum(1 for c in conflicts if c["conflict_directionality"] == "same")
    opposite_count = sum(1 for c in conflicts if c["conflict_directionality"] == "opposite")
    both_count = sum(1 for c in conflicts if c["conflict_directionality"] == "both")

    # Count by incompatible pair type
    type_pair_counts: dict[str, int] = defaultdict(int)
    for c in conflicts:
        for ip in c["incompatible_type_pairs"]:
            key = " × ".join(sorted(ip))
            type_pair_counts[key] += 1

    lines = []
    lines.append("# Graph Conflict Pairs — Review Queue")
    lines.append("")
    lines.append("Generated by `scripts/graph-conflict-pairs.py`.  Read-only audit — "
                 "**do not auto-delete**.  Sentiment legitimately coexists across 5 books;  "
                 "each flagged pair needs human review.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Metric | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total entity pairs analyzed | {total_pairs:,} |")
    lines.append(f"| Flagged pairs (any conflict) | {len(conflicts):,} |")
    lines.append(f"| — same-direction (strongest signal) | {same_count} |")
    lines.append(f"| — opposite-direction only | {opposite_count} |")
    lines.append(f"| — both same + opposite | {both_count} |")
    lines.append("")
    lines.append("### Breakdown by conflict type")
    lines.append("")
    lines.append("| Incompatible Type Pair | Flagged Pairs |")
    lines.append("|------------------------|--------------|")
    for key, cnt in sorted(type_pair_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {key} | {cnt} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Flagged Pairs")
    lines.append("")
    lines.append("> Same-direction conflicts listed first (strongest mis-type signal).")
    lines.append("")

    for i, c in enumerate(conflicts, 1):
        dir_label = c["conflict_directionality"].upper()
        incompat_str = ", ".join(" × ".join(sorted(ip)) for ip in c["incompatible_type_pairs"])
        lines.append(f"### {i}. `{c['slug_a']}` ↔ `{c['slug_b']}`")
        lines.append("")
        lines.append(f"- **Conflict directionality:** {dir_label}")
        lines.append(f"- **Incompatible type pairs:** {incompat_str}")
        lines.append(f"- **All edge types on this pair:** "
                     f"{', '.join(c['all_edge_types_on_pair'])}")
        lines.append(f"- **Total edges between pair:** {c['total_edges_on_pair']}")
        lines.append("")
        lines.append("| Direction | Type | Confidence | Evidence Ref | Quote |")
        lines.append("|-----------|------|-----------|-------------|-------|")
        for edge in c["conflict_edges"]:
            quote = _truncate(edge["evidence_quote"], 120)
            quote = quote.replace("|", "\\|")  # escape pipe chars for Markdown table
            lines.append(
                f"| `{edge['direction']}` "
                f"| {edge['edge_type']} "
                f"| T{edge['confidence_tier']} "
                f"| `{edge['evidence_ref']}` "
                f"| {quote} |"
            )
        lines.append("")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_jsonl(conflicts: list[dict], out_path: Path) -> None:
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
        description="Audit graph/edges/edges.jsonl for semantically incompatible edge-type pairs."
    )
    p.add_argument(
        "--edges",
        type=Path,
        default=DEFAULT_EDGES_FILE,
        metavar="PATH",
        help=f"Path to edges.jsonl (default: {DEFAULT_EDGES_FILE})",
    )
    p.add_argument(
        "--out-md",
        type=Path,
        default=DEFAULT_OUT_MD,
        metavar="PATH",
        help=f"Output markdown report path (default: {DEFAULT_OUT_MD})",
    )
    p.add_argument(
        "--out-jsonl",
        type=Path,
        default=DEFAULT_OUT_JSONL,
        metavar="PATH",
        help=f"Output machine-readable JSONL path (default: {DEFAULT_OUT_JSONL})",
    )
    return p


def main() -> None:
    args = build_parser().parse_args()

    # Validate input
    if not args.edges.exists():
        print(f"ERROR: edges file not found: {args.edges}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading edges from: {args.edges}")
    edges = load_edges(args.edges)
    print(f"  Loaded {len(edges):,} edges.")

    # Print vocabulary coverage for the flagged types (grounding check)
    from collections import Counter
    type_counts = Counter(e.get("edge_type", "") for e in edges)
    flagged_in_data = []
    flagged_absent = []
    all_flagged_types: set[str] = set()
    for pair in INCOMPATIBLE_PAIRS:
        all_flagged_types |= pair
    for t in sorted(all_flagged_types):
        if type_counts[t] > 0:
            flagged_in_data.append(f"{t}({type_counts[t]})")
        else:
            flagged_absent.append(t)
    print(f"\n  Incompatible types present in data: {', '.join(flagged_in_data)}")
    if flagged_absent:
        print(f"  WARNING: types in INCOMPATIBLE_PAIRS NOT found in data: {', '.join(flagged_absent)}")
        print("  (These pairs will never fire — consider pruning INCOMPATIBLE_PAIRS.)")

    print("\nGrouping by entity pair...")
    grouped = group_by_pair(edges)
    total_pairs = len(grouped)
    print(f"  {total_pairs:,} unique entity pairs.")

    print("Detecting conflicts...")
    conflicts = find_all_conflicts(grouped)
    same_count = sum(1 for c in conflicts if c["conflict_directionality"] == "same")
    opposite_count = sum(1 for c in conflicts if c["conflict_directionality"] == "opposite")
    both_count = sum(1 for c in conflicts if c["conflict_directionality"] == "both")
    print(f"  Flagged: {len(conflicts)} pairs")
    print(f"    same-direction:     {same_count}")
    print(f"    opposite-direction: {opposite_count}")
    print(f"    both:               {both_count}")

    print(f"\nWriting markdown report to: {args.out_md}")
    write_markdown(conflicts, total_pairs, args.out_md)

    print(f"Writing JSONL output to:    {args.out_jsonl}")
    write_jsonl(conflicts, args.out_jsonl)

    print(f"\nDone.")
    print(f"  {len(edges):,} edges read | {total_pairs:,} pairs | {len(conflicts)} flagged")
    print(f"  same-direction: {same_count} | opposite-direction: {opposite_count} | both: {both_count}")
    print(f"  MD:    {args.out_md}")
    print(f"  JSONL: {args.out_jsonl}")


if __name__ == "__main__":
    main()
