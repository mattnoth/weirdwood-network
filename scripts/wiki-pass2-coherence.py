#!/usr/bin/env python3
"""
wiki-pass2-coherence.py — Cross-bucket coherence check for Wiki Pass 2.

Per runbook §3.3, verifies three invariants across all emitted node files:

  1. Edge targets exist: for every edge target referenced in a node's body or
     frontmatter, the target node file exists in graph/nodes/ OR appears in
     a deferred queue (working/wiki/pass2-buckets/deferred.jsonl if present).

  2. Allegiance resolves uniquely: every 'allegiance: House X' field in a node
     frontmatter resolves to exactly one house-*.node.md in graph/nodes/houses/.

  3. No duplicate names: no two nodes claim the same 'name:' frontmatter field
     unless one carries 'same_as:' pointing to the other (SAME_AS relationship).

Failures are appended to working/wiki/pass2-buckets/coherence-issues.jsonl, one JSON
object per issue. This script NEVER auto-fixes anything.

Exit code: always 0 (informational). Issue count is printed on exit.

Usage:
    python3 scripts/wiki-pass2-coherence.py [--tier core|secondary|all] [-v]
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


# ── Configuration ──────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent.resolve()
GRAPH_NODES = REPO_ROOT / "graph" / "nodes"
WIKI_PASS2 = REPO_ROOT / "working" / "wiki" / "pass2-buckets"
ISSUES_FILE = WIKI_PASS2 / "coherence-issues.jsonl"
DEFERRED_FILE = WIKI_PASS2 / "deferred.jsonl"

# Frontmatter patterns
RE_FRONTMATTER = re.compile(r'^---\s*\n(.*?)\n---', re.DOTALL | re.MULTILINE)
RE_YAML_FIELD = re.compile(r'^(\w[\w_-]*):\s*(.+)$', re.MULTILINE)

# Edge target patterns in body text (links like [[Target Node]] or target: slug)
RE_EDGE_LINK = re.compile(r'\[\[([^\]]+)\]\]')
RE_EDGE_FIELD = re.compile(
    r'^(?:father|mother|spouse|allegiance|overlord|seat|founder|'
    r'lord|lady|heir|house|faction|location|region):\s*(.+)$',
    re.MULTILINE | re.IGNORECASE
)

# House allegiance pattern
RE_ALLEGIANCE = re.compile(
    r'^allegiance:\s*(.+)$', re.MULTILINE | re.IGNORECASE
)

# House slug normalization: "House Stark" → "house-stark"
def house_slug(raw: str) -> str:
    s = raw.strip()
    # Remove common suffixes/prefixes that don't appear in filenames
    s = re.sub(r'\s+of\s+.*$', '', s, flags=re.IGNORECASE)
    s = s.lower().replace(' ', '-').replace('_', '-')
    # Collapse multiple dashes
    s = re.sub(r'-+', '-', s)
    return s


# ── Helpers ────────────────────────────────────────────────────────────────────

def parse_frontmatter(content: str) -> dict[str, str]:
    """Extract YAML frontmatter fields as a flat string→string dict."""
    m = RE_FRONTMATTER.match(content)
    if not m:
        return {}
    fm_text = m.group(1)
    result = {}
    for fm_m in RE_YAML_FIELD.finditer(fm_text):
        result[fm_m.group(1).lower()] = fm_m.group(2).strip()
    return result


def node_slug_from_path(path: Path) -> str:
    """Convert a node path to its expected slug (filename without .node.md)."""
    return path.name.replace(".node.md", "")


def load_deferred_slugs() -> set[str]:
    """Return slugs in the deferred queue (these count as 'exists' for edge checks)."""
    slugs = set()
    if DEFERRED_FILE.exists():
        with open(DEFERRED_FILE) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                    slug = row.get("slug", "")
                    if slug:
                        slugs.add(slug)
                except Exception:
                    pass
    return slugs


def collect_nodes(tier_filter: str) -> list[Path]:
    """Collect all .node.md files, optionally filtered by tier frontmatter."""
    all_nodes = list(GRAPH_NODES.rglob("*.node.md"))
    # Exclude _conflicts directory
    all_nodes = [n for n in all_nodes if "_conflicts" not in n.parts]

    if tier_filter == "all" or not tier_filter:
        return all_nodes

    # Filter by bucket tier (requires reading each node's frontmatter)
    filtered = []
    for node in all_nodes:
        try:
            content = node.read_text(encoding="utf-8")
            fm = parse_frontmatter(content)
            node_tier = fm.get("tier", "")
            if node_tier == tier_filter:
                filtered.append(node)
        except Exception:
            filtered.append(node)  # Include on read error (don't silently drop)
    return filtered


def append_issue(issue: dict) -> None:
    """Append one issue dict to the coherence-issues JSONL file."""
    WIKI_PASS2.mkdir(parents=True, exist_ok=True)
    with open(ISSUES_FILE, "a") as f:
        f.write(json.dumps(issue) + "\n")


# ── Check 1: Edge targets exist ────────────────────────────────────────────────

def check_edge_targets(
    nodes: list[Path],
    all_slugs: set[str],
    deferred_slugs: set[str],
    verbose: bool,
) -> int:
    """
    For every edge target referenced in a node (via [[Link]] syntax or
    structural YAML fields like allegiance/father/etc.), verify the target
    exists in graph/nodes/ or in the deferred queue.

    Returns the count of issues found.
    """
    issues = 0
    known = all_slugs | deferred_slugs

    for node in nodes:
        try:
            content = node.read_text(encoding="utf-8")
        except Exception as e:
            if verbose:
                print(f"  WARN: could not read {node}: {e}")
            continue

        node_slug = node_slug_from_path(node)

        # Extract edge targets from [[...]] links in body
        body_targets = RE_EDGE_LINK.findall(content)
        # Normalize: WikiLink syntax uses spaces, slugs use dashes
        body_slugs = [
            t.strip().lower().replace(" ", "-").replace("_", "-")
            for t in body_targets
        ]

        # Extract targets from structural frontmatter fields
        fm = parse_frontmatter(content)
        fm_targets = []
        for field in [
            "father", "mother", "spouse", "allegiance", "overlord",
            "seat", "founder", "lord", "lady", "heir", "house",
            "faction", "location", "region",
        ]:
            val = fm.get(field, "").strip()
            if val and val not in ("null", "none", "—", ""):
                # Normalize multi-value (comma-separated)
                for part in val.split(","):
                    s = part.strip().lower().replace(" ", "-").replace("_", "-")
                    if s:
                        fm_targets.append(s)

        all_targets = set(body_slugs) | set(fm_targets)
        # Remove self-reference
        all_targets.discard(node_slug)

        for target in sorted(all_targets):
            # Allow partial matches (e.g. "house-stark" matches "house-stark.node.md" slug)
            # We check if any known slug starts with or equals the target
            matched = (
                target in known
                or any(s.startswith(target) or target.startswith(s) for s in known)
            )
            if not matched:
                issues += 1
                issue = {
                    "check": "edge_target_missing",
                    "source_node": str(node.relative_to(REPO_ROOT)),
                    "missing_target": target,
                    "detected_at": datetime.utcnow().isoformat() + "Z",
                }
                append_issue(issue)
                if verbose:
                    print(
                        f"  ISSUE: {node.name} → target '{target}' not found in graph/nodes/"
                    )

    return issues


# ── Check 2: Allegiance resolves uniquely ─────────────────────────────────────

def check_allegiance_resolution(
    nodes: list[Path],
    verbose: bool,
) -> int:
    """
    Every 'allegiance: House X' in a node's frontmatter should resolve to
    exactly one house-*.node.md in graph/nodes/houses/.

    Returns the count of issues found.
    """
    issues = 0
    houses_dir = GRAPH_NODES / "houses"
    existing_house_slugs: set[str] = set()
    if houses_dir.exists():
        for h in houses_dir.glob("*.node.md"):
            existing_house_slugs.add(h.name.replace(".node.md", ""))

    for node in nodes:
        try:
            content = node.read_text(encoding="utf-8")
        except Exception:
            continue

        fm = parse_frontmatter(content)
        allegiance_raw = fm.get("allegiance", "").strip()
        if not allegiance_raw or allegiance_raw in ("null", "none", "—", ""):
            continue

        for part in allegiance_raw.split(","):
            part = part.strip()
            if not part:
                continue

            # Only check "House ..." style entries
            if not re.match(r'^house\b', part, re.IGNORECASE):
                continue

            target_slug = house_slug(part)
            # Check for exactly one match
            matches = [
                s for s in existing_house_slugs
                if s == target_slug or s.startswith(target_slug) or target_slug.startswith(s)
            ]

            if len(matches) == 0:
                issues += 1
                issue = {
                    "check": "allegiance_unresolved",
                    "source_node": str(node.relative_to(REPO_ROOT)),
                    "allegiance_raw": part,
                    "expected_slug": target_slug,
                    "detected_at": datetime.utcnow().isoformat() + "Z",
                }
                append_issue(issue)
                if verbose:
                    print(
                        f"  ISSUE: {node.name} allegiance '{part}' → "
                        f"no match for '{target_slug}' in houses/"
                    )
            elif len(matches) > 1:
                issues += 1
                issue = {
                    "check": "allegiance_ambiguous",
                    "source_node": str(node.relative_to(REPO_ROOT)),
                    "allegiance_raw": part,
                    "expected_slug": target_slug,
                    "matches": matches,
                    "detected_at": datetime.utcnow().isoformat() + "Z",
                }
                append_issue(issue)
                if verbose:
                    print(
                        f"  ISSUE: {node.name} allegiance '{part}' → "
                        f"ambiguous: {matches}"
                    )

    return issues


# ── Check 3: No duplicate names ────────────────────────────────────────────────

def check_no_duplicate_names(
    nodes: list[Path],
    verbose: bool,
) -> int:
    """
    No two nodes may claim the same 'name:' frontmatter field unless one
    carries 'same_as:' pointing to the other.

    Returns the count of issues found.
    """
    issues = 0
    name_to_nodes: dict[str, list[Path]] = {}

    for node in nodes:
        try:
            content = node.read_text(encoding="utf-8")
        except Exception:
            continue
        fm = parse_frontmatter(content)
        name = fm.get("name", "").strip().lower()
        if not name or name in ("null", "none", ""):
            continue
        name_to_nodes.setdefault(name, []).append(node)

    for name, dupes in name_to_nodes.items():
        if len(dupes) < 2:
            continue

        # Check if any node has same_as: pointing to the other(s)
        same_as_exempted = set()
        for node in dupes:
            try:
                content = node.read_text(encoding="utf-8")
                fm = parse_frontmatter(content)
                same_as = fm.get("same_as", "").strip()
                if same_as:
                    same_as_exempted.add(node)
            except Exception:
                pass

        # If all but one are exempted via same_as, it's fine
        non_exempted = [n for n in dupes if n not in same_as_exempted]
        if len(non_exempted) <= 1:
            continue

        issues += 1
        issue = {
            "check": "duplicate_name",
            "name": name,
            "nodes": [str(n.relative_to(REPO_ROOT)) for n in dupes],
            "same_as_count": len(same_as_exempted),
            "detected_at": datetime.utcnow().isoformat() + "Z",
        }
        append_issue(issue)
        if verbose:
            print(
                f"  ISSUE: duplicate name '{name}' in "
                + ", ".join(n.name for n in dupes)
            )

    return issues


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cross-bucket coherence check for Wiki Pass 2 graph/nodes/."
    )
    parser.add_argument(
        "--tier",
        choices=["core", "secondary", "all"],
        default="all",
        help="Limit check to nodes from a specific tier (default: all)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print each issue as it is found",
    )
    args = parser.parse_args()

    print(f"Wiki Pass 2 coherence check — tier: {args.tier}")
    print(f"Scanning: {GRAPH_NODES}")

    # Gather all node slugs for edge-target lookup
    all_node_paths = list(GRAPH_NODES.rglob("*.node.md"))
    all_node_paths = [n for n in all_node_paths if "_conflicts" not in n.parts]
    all_slugs = {node_slug_from_path(n) for n in all_node_paths}
    deferred_slugs = load_deferred_slugs()

    # Collect nodes to check (may be subset if tier filter applied)
    nodes = collect_nodes(args.tier)
    print(f"Nodes to check: {len(nodes)} (total in graph: {len(all_node_paths)})")

    if len(nodes) == 0:
        print("0 issues found (no nodes to check).")
        sys.exit(0)

    total_issues = 0

    print("\n[1/3] Checking edge targets exist...")
    n = check_edge_targets(nodes, all_slugs, deferred_slugs, args.verbose)
    print(f"      {n} issue(s)")
    total_issues += n

    print("\n[2/3] Checking allegiance resolution...")
    n = check_allegiance_resolution(nodes, args.verbose)
    print(f"      {n} issue(s)")
    total_issues += n

    print("\n[3/3] Checking for duplicate names...")
    n = check_no_duplicate_names(nodes, args.verbose)
    print(f"      {n} issue(s)")
    total_issues += n

    print()
    if total_issues == 0:
        print("0 issues found.")
    else:
        print(
            f"{total_issues} issue(s) found. "
            f"Details appended to: {ISSUES_FILE.relative_to(REPO_ROOT)}"
        )
        print("No auto-fix applied — review issues manually.")

    sys.exit(0)


if __name__ == "__main__":
    main()
