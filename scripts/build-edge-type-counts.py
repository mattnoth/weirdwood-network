#!/usr/bin/env python3
"""
build-edge-type-counts.py — Weirwood Network edge-type inventory

Scans all canonical .node.md files under graph/nodes/ and tallies how many
instances of each edge type are present. Compares against the locked master
vocabulary in reference/architecture.md to surface populated vs unpopulated
types and any drift types (emitted by a source that violated the vocabulary
lock).

Outputs:
  working/wiki/data/edge-type-counts.json  — structured counts artifact
  working/wiki/data/edge-type-counts.md    — human-readable summary

Usage:
  python scripts/build-edge-type-counts.py
  python scripts/build-edge-type-counts.py --verbose
  python scripts/build-edge-type-counts.py --check-only
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHITECTURE_MD = REPO_ROOT / "reference" / "architecture.md"
NODES_DIR = REPO_ROOT / "graph" / "nodes"
OUTPUT_JSON = REPO_ROOT / "working" / "wiki" / "data" / "edge-type-counts.json"
OUTPUT_MD = REPO_ROOT / "working" / "wiki" / "data" / "edge-type-counts.md"

# Pipeline holding zones — skip these
SKIP_DIRS = {"_conflicts", "_unclassified", "_stage3-preview"}


# ---------------------------------------------------------------------------
# Step 1: Extract canonical vocabulary from architecture.md
# ---------------------------------------------------------------------------

def extract_canonical_types(arch_path: Path) -> tuple[dict[str, str], dict[str, list[str]]]:
    """
    Parse reference/architecture.md to extract the master edge vocabulary.

    Returns:
        type_to_category: {edge_type: category_name}
        category_to_types: {category_name: [edge_type, ...]}  (ordered)
    """
    text = arch_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    in_edge_section = False
    current_category = None
    type_to_category: dict[str, str] = {}
    category_to_types: dict[str, list[str]] = {}

    # Match the start of the Edge Types section and its end
    edge_section_start = re.compile(r"^## Edge Types \(Relationship Categories\)")
    # Stop at the next same-level heading (## Edge Metadata or any other ##)
    edge_section_end = re.compile(r"^## (?!Edge Types)")
    # Subsection headings: ### Kinship & Family, etc.
    subsection_re = re.compile(r"^### (.+)")
    # Table rows with backtick-wrapped edge types in the first column:
    #   | `EDGE_TYPE` | description | ...
    table_row_re = re.compile(r"^\|\s*`([A-Z][A-Z0-9_]*)`\s*\|")

    for line in lines:
        if edge_section_start.match(line):
            in_edge_section = True
            continue

        if in_edge_section and edge_section_end.match(line):
            break

        if not in_edge_section:
            continue

        sub_match = subsection_re.match(line)
        if sub_match:
            current_category = sub_match.group(1).strip()
            if current_category not in category_to_types:
                category_to_types[current_category] = []
            continue

        row_match = table_row_re.match(line)
        if row_match and current_category:
            edge_type = row_match.group(1)
            type_to_category[edge_type] = current_category
            category_to_types[current_category].append(edge_type)

    # Drop categories with no types (e.g., "Design Principles" which is a
    # prose subsection with no table rows)
    category_to_types = {k: v for k, v in category_to_types.items() if v}

    return type_to_category, category_to_types


# ---------------------------------------------------------------------------
# Step 2: Walk node files and tally edge instances
# ---------------------------------------------------------------------------

# Regex: matches edge lines like:
#   - HOLDS_TITLE: ...
#   - SUCCEEDS (reverse): ...
#   - PARENT_OF (reverse): ...
# Captures the ALL_CAPS token before the optional " (reverse)" and ":"
EDGE_LINE_RE = re.compile(r"^-\s+([A-Z][A-Z0-9_]*)(?:\s+\([^)]+\))?\s*:")

# Heading patterns that start/end edge sections
EDGE_SECTION_START_RE = re.compile(r"^##\s+Edges(\s+\(.*\))?$")
NEXT_SECTION_RE = re.compile(r"^##\s+")  # any ## heading ends the section


def classify_section(heading_line: str) -> str:
    """Return 'infobox' or 'prose_derived' based on the ## Edges heading."""
    if "prose" in heading_line.lower() or "prose-derived" in heading_line.lower():
        return "prose_derived"
    return "infobox"


def scan_node_file(path: Path) -> list[tuple[str, str]]:
    """
    Scan a single .node.md file.

    Returns a list of (edge_type, section) tuples where section is
    'infobox' or 'prose_derived'.
    """
    results: list[tuple[str, str]] = []
    current_section: str | None = None

    for line in path.read_text(encoding="utf-8").splitlines():
        if EDGE_SECTION_START_RE.match(line):
            current_section = classify_section(line)
            continue
        # Any other ## heading ends the current edge section
        if NEXT_SECTION_RE.match(line) and current_section is not None:
            current_section = None
            continue

        if current_section is None:
            continue

        m = EDGE_LINE_RE.match(line)
        if m:
            results.append((m.group(1), current_section))

    return results


def walk_nodes(
    nodes_dir: Path,
    verbose: bool = False,
) -> tuple[
    dict[str, dict],          # type_counts: {edge_type: {total, infobox, prose_derived, by_node_type}}
    int,                       # files_scanned
    dict[str, int],            # by_section totals
]:
    """Walk all canonical node directories and tally edge instances."""
    type_counts: dict[str, dict] = defaultdict(
        lambda: {"total": 0, "infobox": 0, "prose_derived": 0, "by_node_type": defaultdict(int)}
    )
    by_section = {"infobox": 0, "prose_derived": 0}
    files_scanned = 0

    for type_dir in sorted(nodes_dir.iterdir()):
        if not type_dir.is_dir():
            continue
        if type_dir.name in SKIP_DIRS:
            continue

        node_type_name = type_dir.name
        dir_files = list(type_dir.glob("*.node.md"))

        if verbose:
            print(f"  Scanning {node_type_name}/ ({len(dir_files)} files) ...", flush=True)

        for node_path in dir_files:
            files_scanned += 1
            for edge_type, section in scan_node_file(node_path):
                type_counts[edge_type]["total"] += 1
                type_counts[edge_type][section] += 1
                type_counts[edge_type]["by_node_type"][node_type_name] += 1
                by_section[section] += 1

    return type_counts, files_scanned, by_section


# ---------------------------------------------------------------------------
# Step 3: Compute derived statistics
# ---------------------------------------------------------------------------

def compute_stats(
    type_to_category: dict[str, str],
    category_to_types: dict[str, list[str]],
    type_counts: dict[str, dict],
    files_scanned: int,
    by_section: dict[str, int],
) -> dict:
    """Assemble the full stats dict for JSON output."""
    canonical_set = set(type_to_category.keys())
    found_set = set(type_counts.keys())

    populated_types = {t for t in canonical_set if type_counts.get(t, {}).get("total", 0) > 0}
    unpopulated_types = sorted(canonical_set - populated_types)
    drift_types_raw = found_set - canonical_set

    # Build drift type entries with sample nodes — we need to re-walk briefly
    # to collect samples. We'll embed the sample collection in walk results
    # above, but for now reconstruct from what we have. Since we didn't store
    # node paths in type_counts, we do a targeted re-scan for drift types only.
    drift_entries = []
    if drift_types_raw:
        drift_samples: dict[str, list[str]] = defaultdict(list)
        for type_dir in sorted(NODES_DIR.iterdir()):
            if not type_dir.is_dir() or type_dir.name in SKIP_DIRS:
                continue
            for node_path in type_dir.glob("*.node.md"):
                for edge_type, _ in scan_node_file(node_path):
                    if edge_type in drift_types_raw and len(drift_samples[edge_type]) < 5:
                        drift_samples[edge_type].append(
                            str(node_path.relative_to(REPO_ROOT))
                        )
        for dt in sorted(drift_types_raw):
            drift_entries.append({
                "type": dt,
                "instance_count": type_counts[dt]["total"],
                "sample_nodes": drift_samples[dt],
            })

    # Per-category stats
    categories = {}
    for cat, types_in_cat in category_to_types.items():
        pop = sum(1 for t in types_in_cat if type_counts.get(t, {}).get("total", 0) > 0)
        unpop = len(types_in_cat) - pop
        total_inst = sum(type_counts.get(t, {}).get("total", 0) for t in types_in_cat)
        categories[cat] = {
            "populated": pop,
            "unpopulated": unpop,
            "total_types": len(types_in_cat),
            "total_instances": total_inst,
        }

    # Serialize type_counts — convert defaultdicts to plain dicts
    serialized_counts = {}
    for edge_type in sorted(canonical_set | found_set):
        raw = type_counts.get(edge_type, {})
        serialized_counts[edge_type] = {
            "total": raw.get("total", 0),
            "infobox": raw.get("infobox", 0),
            "prose_derived": raw.get("prose_derived", 0),
            "by_node_type": dict(raw.get("by_node_type", {})),
        }

    total_instances = sum(v["total"] for v in type_counts.values())

    return {
        "version": "v1",
        "computed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "graph_nodes_scanned": files_scanned,
        "canonical_type_count": len(canonical_set),
        "populated_type_count": len(populated_types),
        "unpopulated_type_count": len(unpopulated_types),
        "drift_type_count": len(drift_types_raw),
        "total_edge_instances": total_instances,
        "edges_by_section": by_section,
        "type_counts": serialized_counts,
        "unpopulated_types": unpopulated_types,
        "drift_types": drift_entries,
        "categories": categories,
    }


# ---------------------------------------------------------------------------
# Step 4: Render human-readable markdown
# ---------------------------------------------------------------------------

def render_markdown(stats: dict, type_to_category: dict, category_to_types: dict) -> str:
    lines = []

    ts = stats["computed_at"]
    lines.append(f"# Edge Type Counts — Weirwood Network")
    lines.append(f"")
    lines.append(f"Generated: {ts}")
    lines.append(f"")
    lines.append(f"## Summary")
    lines.append(f"")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Node files scanned | {stats['graph_nodes_scanned']:,} |")
    lines.append(f"| Canonical edge types | {stats['canonical_type_count']} |")
    lines.append(f"| Populated types (≥1 instance) | {stats['populated_type_count']} |")
    lines.append(f"| Unpopulated types (0 instances) | {stats['unpopulated_type_count']} |")
    lines.append(f"| Drift types (not in canonical) | {stats['drift_type_count']} |")
    lines.append(f"| Total edge instances | {stats['total_edge_instances']:,} |")
    lines.append(f"| Infobox edges | {stats['edges_by_section']['infobox']:,} |")
    lines.append(f"| Prose-derived edges | {stats['edges_by_section']['prose_derived']:,} |")
    lines.append(f"")

    # By Category
    lines.append(f"## By Category")
    lines.append(f"")
    for cat, types_in_cat in category_to_types.items():
        cat_stats = stats["categories"][cat]
        lines.append(
            f"### {cat} — {cat_stats['populated']}/{cat_stats['total_types']} populated, "
            f"{cat_stats['total_instances']:,} instances"
        )
        lines.append(f"")
        lines.append(f"| Edge Type | Instances | Infobox | Prose |")
        lines.append(f"|-----------|-----------|---------|-------|")
        # Sort by instance count descending
        sorted_types = sorted(
            types_in_cat,
            key=lambda t: stats["type_counts"].get(t, {}).get("total", 0),
            reverse=True,
        )
        for t in sorted_types:
            tc = stats["type_counts"].get(t, {"total": 0, "infobox": 0, "prose_derived": 0})
            marker = "" if tc["total"] > 0 else " *(unpopulated)*"
            lines.append(
                f"| `{t}`{marker} | {tc['total']:,} | {tc['infobox']:,} | {tc['prose_derived']:,} |"
            )
        lines.append(f"")

    # Unpopulated Types
    lines.append(f"## Unpopulated Types ({stats['unpopulated_type_count']} total — Stage 4 targets)")
    lines.append(f"")
    lines.append(f"These are the types with zero instances in the current graph.")
    lines.append(f"They are the primary targets for Stage 4 (prose-edge classification).")
    lines.append(f"")

    # Group by category
    unpop_by_cat: dict[str, list[str]] = defaultdict(list)
    for t in stats["unpopulated_types"]:
        cat = type_to_category.get(t, "Unknown")
        unpop_by_cat[cat].append(t)

    for cat in category_to_types:
        if cat in unpop_by_cat:
            types_list = ", ".join(f"`{t}`" for t in unpop_by_cat[cat])
            lines.append(f"- **{cat}:** {types_list}")
    lines.append(f"")

    # Drift Types
    lines.append(f"## Drift Types")
    lines.append(f"")
    if not stats["drift_types"]:
        lines.append(f"None. All emitted edge types are in the canonical vocabulary.")
    else:
        lines.append(
            f"**{stats['drift_type_count']} drift type(s) found** — these are NOT in the locked "
            f"master vocabulary. Each is a potential vocabulary-lock violation."
        )
        lines.append(f"")
        lines.append(f"| Type | Instances | Sample Nodes |")
        lines.append(f"|------|-----------|-------------|")
        for entry in stats["drift_types"]:
            samples = "; ".join(entry["sample_nodes"][:3])
            lines.append(f"| `{entry['type']}` | {entry['instance_count']:,} | {samples} |")
    lines.append(f"")

    # Top 20 by instance count
    lines.append(f"## Top 20 By Instance Count")
    lines.append(f"")
    lines.append(f"| Rank | Edge Type | Category | Instances |")
    lines.append(f"|------|-----------|----------|-----------|")
    all_types_sorted = sorted(
        stats["type_counts"].items(),
        key=lambda kv: kv[1]["total"],
        reverse=True,
    )
    for rank, (t, tc) in enumerate(all_types_sorted[:20], 1):
        cat = type_to_category.get(t, "*(drift)*")
        lines.append(f"| {rank} | `{t}` | {cat} | {tc['total']:,} |")
    lines.append(f"")

    # Bottom 20 populated (>0 instances) by instance count
    populated_sorted = [
        (t, tc) for t, tc in all_types_sorted if tc["total"] > 0
    ]
    bottom_populated = populated_sorted[-20:][::-1]  # lowest first, then reverse for table
    if bottom_populated:
        lines.append(f"## Bottom 20 Populated Types (lowest instance count)")
        lines.append(f"")
        lines.append(f"| Rank | Edge Type | Category | Instances |")
        lines.append(f"|------|-----------|----------|-----------|")
        for rank, (t, tc) in enumerate(
            sorted(bottom_populated, key=lambda kv: kv[1]["total"]), 1
        ):
            cat = type_to_category.get(t, "*(drift)*")
            lines.append(f"| {rank} | `{t}` | {cat} | {tc['total']:,} |")
        lines.append(f"")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def print_stdout_summary(stats: dict, type_to_category: dict) -> None:
    """Print a compact summary to stdout."""
    print(f"Nodes scanned:        {stats['graph_nodes_scanned']:,}")
    print(f"Total edge instances: {stats['total_edge_instances']:,}")
    print(f"  Infobox:            {stats['edges_by_section']['infobox']:,}")
    print(f"  Prose-derived:      {stats['edges_by_section']['prose_derived']:,}")
    print(f"Canonical types:      {stats['canonical_type_count']}")
    print(f"Populated:            {stats['populated_type_count']}")
    print(f"Unpopulated:          {stats['unpopulated_type_count']}")
    print(f"Drift types:          {stats['drift_type_count']}")
    print()

    all_sorted = sorted(
        stats["type_counts"].items(),
        key=lambda kv: kv[1]["total"],
        reverse=True,
    )
    print("Top 10 edge types by instance count:")
    for t, tc in all_sorted[:10]:
        cat = type_to_category.get(t, "DRIFT")
        print(f"  {t:<30} {tc['total']:>6}  ({cat})")
    print()

    if stats["drift_types"]:
        print(f"Drift types ({stats['drift_type_count']}):")
        for entry in stats["drift_types"]:
            print(f"  {entry['type']:<30} {entry['instance_count']:>6} instances")
            for s in entry["sample_nodes"][:2]:
                print(f"    sample: {s}")
    else:
        print("Drift types: none")
    print()

    print(f"Unpopulated types ({stats['unpopulated_type_count']}):")
    # Group by category
    unpop_by_cat: dict[str, list[str]] = defaultdict(list)
    for t in stats["unpopulated_types"]:
        cat = type_to_category.get(t, "Unknown")
        unpop_by_cat[cat].append(t)
    for cat, types_list in unpop_by_cat.items():
        print(f"  {cat}: {', '.join(types_list)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build edge-type instance counts for the Weirwood Network graph."
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print progress per node-type directory.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Print stdout summary without writing output files.",
    )
    args = parser.parse_args()

    # Validate inputs
    if not ARCHITECTURE_MD.exists():
        print(f"ERROR: architecture.md not found at {ARCHITECTURE_MD}", file=sys.stderr)
        sys.exit(1)
    if not NODES_DIR.exists():
        print(f"ERROR: nodes directory not found at {NODES_DIR}", file=sys.stderr)
        sys.exit(1)

    # Step 1: Extract canonical vocabulary
    if args.verbose:
        print("Parsing canonical edge vocabulary from architecture.md ...")
    type_to_category, category_to_types = extract_canonical_types(ARCHITECTURE_MD)

    if not type_to_category:
        print("ERROR: No edge types extracted from architecture.md. Check parsing logic.", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"  Found {len(type_to_category)} canonical edge types across {len(category_to_types)} categories.")
        print()
        print("Scanning node files ...")

    # Step 2: Walk nodes
    type_counts, files_scanned, by_section = walk_nodes(NODES_DIR, verbose=args.verbose)

    if args.verbose:
        print()

    # Step 3: Compute stats
    stats = compute_stats(
        type_to_category,
        category_to_types,
        type_counts,
        files_scanned,
        by_section,
    )

    # Step 4: Output
    if args.check_only:
        print_stdout_summary(stats, type_to_category)
        print("(check-only mode: no files written)")
        return

    # Write JSON
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(stats, indent=2, default=str),
        encoding="utf-8",
    )

    # Write markdown
    md_content = render_markdown(stats, type_to_category, category_to_types)
    OUTPUT_MD.write_text(md_content, encoding="utf-8")

    # Always print a compact summary to stdout
    print_stdout_summary(stats, type_to_category)

    print(f"Outputs written:")
    print(f"  {OUTPUT_JSON}")
    print(f"  {OUTPUT_MD}")


if __name__ == "__main__":
    main()
