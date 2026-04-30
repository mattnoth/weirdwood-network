#!/usr/bin/env python3
"""graph-query.py — Read-only inspection primitive for Weirwood Network graph nodes.

Prints a human-readable (or machine-readable) report for a single node:
  1. Node header: slug, name, type, file path, aliases.
  2. Outbound edges: parsed from ## Edges section, with target slug resolution
     and file-existence checks (OK / ORPHAN / ALIAS→canonical).
  3. Inbound references: rows from cross-references.jsonl where target_slug
     matches this node. Top 20 by default.
  4. Summary line.

Usage:
  python3 scripts/graph-query.py <slug>
  python3 scripts/graph-query.py <slug> --edges-only
  python3 scripts/graph-query.py <slug> --inbound-only
  python3 scripts/graph-query.py <slug> --json
  python3 scripts/graph-query.py --help
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
NODES_DIR = PROJECT_ROOT / "graph" / "nodes"
CROSS_REFS_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "cross-references.jsonl"
ALIAS_RESOLVER_FILE = PROJECT_ROOT / "working" / "wiki-parsed" / "alias-resolver.json"

# ---------------------------------------------------------------------------
# Slug generation — must match wiki-pass2-emit-deterministic.py exactly
# ---------------------------------------------------------------------------

def title_to_slug(title: str) -> str:
    """Convert a node title/name to a filesystem slug.

    Matches the convention in wiki-pass2-emit-deterministic.py::page_to_slug.
    """
    slug = title.lower()
    slug = re.sub(r"['\",]", "", slug)
    slug = re.sub(r"[ _]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


# ---------------------------------------------------------------------------
# File system helpers
# ---------------------------------------------------------------------------

def find_node_file(slug: str) -> Path | None:
    """Search all type subdirectories for <slug>.node.md. Return Path or None."""
    for type_dir in NODES_DIR.iterdir():
        if not type_dir.is_dir():
            continue
        candidate = type_dir / f"{slug}.node.md"
        if candidate.exists():
            return candidate
    return None


def build_node_index() -> dict[str, Path]:
    """Return {slug: path} for every .node.md in the graph. Used by slow alias search."""
    index: dict[str, Path] = {}
    if not NODES_DIR.exists():
        return index
    for type_dir in NODES_DIR.iterdir():
        if not type_dir.is_dir():
            continue
        for node_file in type_dir.glob("*.node.md"):
            slug = node_file.stem.replace(".node", "")
            index[slug] = node_file
    return index


# ---------------------------------------------------------------------------
# YAML frontmatter parser (stdlib only — no pyyaml needed for this structure)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and return (fields_dict, body_text).

    Handles only the simple key: value and key:\n  - item list structures
    present in node files. Does not attempt full YAML parsing to keep stdlib-only.
    Falls back to pyyaml if available, otherwise uses the simple parser.
    """
    if not text.startswith("---"):
        return {}, text

    end = text.find("\n---", 3)
    if end == -1:
        return {}, text

    yaml_block = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")

    # Try pyyaml first for correctness; fall back to simple parser on any error
    try:
        import yaml  # type: ignore
        try:
            fields = yaml.safe_load(yaml_block) or {}
        except Exception:
            fields = _simple_yaml_parse(yaml_block)
    except ImportError:
        fields = _simple_yaml_parse(yaml_block)

    return fields, body


def _simple_yaml_parse(yaml_text: str) -> dict:
    """Minimal YAML parser for node frontmatter (no nested dicts, just scalars and lists)."""
    result: dict = {}
    lines = yaml_text.splitlines()
    current_key: str | None = None
    current_list: list | None = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # List item under a key
        if stripped.startswith("- ") and current_key and current_list is not None:
            current_list.append(stripped[2:].strip().strip('"'))
            continue

        # key: value or key: (start of list)
        if ":" in stripped:
            if current_key and current_list is not None:
                result[current_key] = current_list
                current_list = None
                current_key = None

            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip().strip('"')

            if value == "" or value == "[]":
                current_key = key
                current_list = []
            else:
                result[key] = value
                current_key = None
                current_list = None

    if current_key and current_list is not None:
        result[current_key] = current_list

    return result


# ---------------------------------------------------------------------------
# Edge parser
# ---------------------------------------------------------------------------

# Matches: - EDGE_TYPE[ (reverse)]: rest
_EDGE_LINE_RE = re.compile(
    r"^-\s+"
    r"(?P<edge_type>[A-Z_]+)"
    r"(?P<reverse>\s+\(reverse\))?"
    r"\s*:\s*"
    r"(?P<rest>.+)$"
)

# From the rest, extract target title (everything before optional (track_b:...) or [qualifier])
# Also handles " → TargetName" style seen in some edges (e.g. arrow-separated)
_TARGET_RE = re.compile(
    r"^(?P<target>.+?)(?:\s+\(track_b:.*\))?(?:\s+\[.*\])?$"
)


def parse_edge_line(line: str) -> dict | None:
    """Parse a single edge bullet line. Returns dict or None if not an edge."""
    m = _EDGE_LINE_RE.match(line.strip())
    if not m:
        return None

    edge_type = m.group("edge_type")
    is_reverse = bool(m.group("reverse"))
    rest = m.group("rest").strip()

    # Extract qualifier bracket if present at end
    qualifier_match = re.search(r"\[([^\]]+)\]$", rest)
    qualifier = qualifier_match.group(1) if qualifier_match else None

    # Extract track_b if present
    track_b_match = re.search(r"\(track_b:\s*([^)]+)\)", rest)
    track_b = track_b_match.group(1).strip() if track_b_match else None

    # Extract target: everything before first (track_b: or [qualifier at end
    # Some edges use "X → Y" format; we want only the displayed target name part
    target_raw = rest
    # Strip track_b
    target_raw = re.sub(r"\s*\(track_b:[^)]*\)", "", target_raw).strip()
    # Strip trailing bracket
    target_raw = re.sub(r"\s*\[[^\]]*\]$", "", target_raw).strip()
    # Strip trailing qualifier-style parens that aren't track_b
    target_raw = re.sub(r"\s*\(qualifier:[^)]*\)", "", target_raw).strip()
    # Strip trailing wiki: refs in parens
    target_raw = re.sub(r"\s*\(wiki:[^)]*\)", "", target_raw).strip()
    # Some edges have "X → Y" format (e.g. PARENT_OF (reverse): Rickard Stark → Eddard Stark).
    # The arrow separates parent→child; for a reverse edge the logical target is
    # the *first* segment (the parent being identified). Take the first segment.
    if " → " in target_raw:
        target_raw = target_raw.split(" → ")[0].strip()

    # Final cleanup
    target_title = target_raw.strip().strip('"')

    return {
        "edge_type": edge_type,
        "is_reverse": is_reverse,
        "target_title": target_title,
        "qualifier": qualifier,
        "track_b": track_b,
        "raw": line.strip(),
    }


def extract_edges(body: str) -> list[dict]:
    """Parse all edge bullets from the ## Edges section of a node body."""
    edges: list[dict] = []
    in_edges = False

    for line in body.splitlines():
        stripped = line.strip()
        if re.match(r"^##\s+Edges", stripped):
            in_edges = True
            continue
        if in_edges:
            if stripped.startswith("## ") and not re.match(r"^##\s+Edges", stripped):
                break  # Next section
            if stripped.startswith("- "):
                parsed = parse_edge_line(stripped)
                if parsed:
                    edges.append(parsed)
    return edges


# ---------------------------------------------------------------------------
# Alias resolver loader
# ---------------------------------------------------------------------------

def load_alias_resolver() -> dict[str, str]:
    """Return the alias_to_canonical dict from alias-resolver.json."""
    if not ALIAS_RESOLVER_FILE.exists():
        return {}
    try:
        data = json.loads(ALIAS_RESOLVER_FILE.read_text(encoding="utf-8"))
        return data.get("alias_to_canonical", {})
    except (json.JSONDecodeError, KeyError):
        return {}


# ---------------------------------------------------------------------------
# Cross-reference loader (streaming)
# ---------------------------------------------------------------------------

def stream_inbound_refs(target_slug: str, limit: int = 20) -> tuple[list[dict], int]:
    """Stream cross-references.jsonl and collect rows where target_slug matches.

    Returns (top_rows_up_to_limit, total_count).
    """
    if not CROSS_REFS_FILE.exists():
        return [], 0

    results: list[dict] = []
    total = 0

    with open(CROSS_REFS_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue

            if row.get("target_slug") == target_slug:
                total += 1
                if len(results) < limit:
                    results.append(row)

    return results, total


# ---------------------------------------------------------------------------
# Edge resolution
# ---------------------------------------------------------------------------

def resolve_edge_target(
    target_title: str,
    alias_map: dict[str, str],
) -> tuple[str, str, str | None]:
    """Resolve a target title to (slug, status, canonical_slug_if_alias).

    status is one of: "OK", "ORPHAN", "ALIAS→<canonical>"
    """
    raw_slug = title_to_slug(target_title)

    # 1. Try the slug directly
    file_path = find_node_file(raw_slug)
    if file_path:
        return raw_slug, "OK", None

    # 2. Try alias resolver
    canonical = alias_map.get(raw_slug)
    if canonical:
        canon_file = find_node_file(canonical)
        if canon_file:
            return raw_slug, f"ALIAS→{canonical}", canonical
        else:
            # Alias exists but canonical has no file either
            return raw_slug, f"ALIAS→{canonical} [ORPHAN]", canonical

    # 3. Not found
    return raw_slug, "ORPHAN", None


# ---------------------------------------------------------------------------
# Slow alias search (slug not found — check all node frontmatter aliases)
# ---------------------------------------------------------------------------

def slow_alias_search(missing_slug: str) -> list[str]:
    """Search all node frontmatter for the missing_slug in aliases list.

    Returns list of canonical slugs that have this as an alias.
    This is O(nodes * aliases) — only used on the not-found path.
    """
    matches: list[str] = []
    if not NODES_DIR.exists():
        return matches

    for type_dir in NODES_DIR.iterdir():
        if not type_dir.is_dir():
            continue
        for node_file in type_dir.glob("*.node.md"):
            try:
                text = node_file.read_text(encoding="utf-8")
            except OSError:
                continue
            try:
                fields, _ = parse_frontmatter(text)
            except Exception:
                continue
            aliases_raw = fields.get("aliases", [])
            if not isinstance(aliases_raw, list):
                if aliases_raw:
                    aliases_raw = [aliases_raw]
                else:
                    aliases_raw = []
            for alias in aliases_raw:
                if title_to_slug(str(alias)) == missing_slug:
                    node_slug = fields.get("slug") or node_file.stem.replace(".node", "")
                    matches.append(node_slug)
    return matches


# ---------------------------------------------------------------------------
# Slug prefix / substring suggestions (fast path for typos)
# ---------------------------------------------------------------------------

def slug_prefix_suggestions(missing_slug: str, max_results: int = 5) -> list[str]:
    """Return up to max_results existing slugs that share significant tokens
    with the missing slug.

    Strategy:
    1. First try ALL tokens matching (exact multi-token overlap).
    2. If empty, fall back to ANY token matching, ranked by hit count.
    Tokens shorter than 3 chars are skipped (too common to be useful).
    """
    if not NODES_DIR.exists():
        return []

    tokens = [t for t in missing_slug.split("-") if len(t) >= 3]
    if not tokens:
        return []

    all_slugs: list[tuple[int, str]] = []  # (hit_count, slug)

    for type_dir in NODES_DIR.iterdir():
        if not type_dir.is_dir():
            continue
        for node_file in type_dir.glob("*.node.md"):
            slug = node_file.stem.replace(".node", "")
            hits = sum(1 for t in tokens if t in slug)
            if hits > 0:
                all_slugs.append((hits, slug))

    # Sort descending by hit count, then alphabetically for stability
    all_slugs.sort(key=lambda x: (-x[0], x[1]))
    return [slug for _, slug in all_slugs[:max_results]]


# ---------------------------------------------------------------------------
# Main report functions
# ---------------------------------------------------------------------------

def build_report(
    slug: str,
    *,
    edges_only: bool = False,
    inbound_only: bool = False,
    inbound_limit: int = 20,
) -> dict:
    """Build a structured report dict for the given slug.

    Returns a dict with keys: node, edges, inbound, summary, error, suggestions.
    """
    alias_map = load_alias_resolver()

    # Resolve alias at the top level — if the user passed an alias slug, redirect
    top_level_alias: str | None = None
    resolved_slug = slug
    if slug not in [p.stem.replace(".node", "") for p in NODES_DIR.rglob("*.node.md") if False]:
        pass  # done via find_node_file below

    node_file = find_node_file(slug)

    # If not found by slug, check alias resolver
    if node_file is None and slug in alias_map:
        resolved_slug = alias_map[slug]
        top_level_alias = resolved_slug
        node_file = find_node_file(resolved_slug)

    if node_file is None:
        # Slow path: search frontmatter aliases
        print(
            f"Warning: no node file for slug '{slug}'. "
            "Searching frontmatter aliases (slow)...",
            file=sys.stderr,
        )
        suggestions = slow_alias_search(slug)
        # Also add slug-prefix suggestions from the node index
        if not suggestions:
            suggestions = slug_prefix_suggestions(slug)
        return {
            "error": f"No node found for slug '{slug}'",
            "suggestions": suggestions,
            "node": None,
            "edges": [],
            "inbound": [],
            "inbound_total": 0,
            "summary": None,
        }

    # Parse the file
    text = node_file.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(text)

    node_info = {
        "slug": fields.get("slug", resolved_slug),
        "name": fields.get("name", ""),
        "type": fields.get("type", ""),
        "file_path": str(node_file),
        "aliases": fields.get("aliases", []),
        "top_level_alias": top_level_alias,
    }

    # Edges
    edges_data: list[dict] = []
    if not inbound_only:
        raw_edges = extract_edges(body)
        for edge in raw_edges:
            target_slug, status, canonical = resolve_edge_target(
                edge["target_title"], alias_map
            )
            edges_data.append({
                **edge,
                "target_slug": target_slug,
                "resolution_status": status,
                "canonical_slug": canonical,
            })

    # Inbound refs
    inbound_data: list[dict] = []
    inbound_total = 0
    if not edges_only:
        query_slug = fields.get("slug", resolved_slug)
        inbound_data, inbound_total = stream_inbound_refs(query_slug, limit=inbound_limit)

    # Summary
    if not inbound_only:
        ok_count = sum(1 for e in edges_data if e["resolution_status"] == "OK")
        alias_count = sum(1 for e in edges_data if "ALIAS" in e["resolution_status"])
        orphan_count = sum(1 for e in edges_data if "ORPHAN" in e["resolution_status"] and "ALIAS" not in e["resolution_status"])
        summary = (
            f"{len(edges_data)} outbound edges "
            f"({ok_count} OK, {alias_count} alias-resolved, {orphan_count} orphan), "
            f"{inbound_total} inbound references."
        )
    else:
        ok_count = alias_count = orphan_count = 0
        summary = f"{inbound_total} inbound references."

    return {
        "error": None,
        "suggestions": [],
        "node": node_info,
        "edges": edges_data,
        "inbound": inbound_data,
        "inbound_total": inbound_total,
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# Human-readable printer
# ---------------------------------------------------------------------------

def print_report(report: dict, *, inbound_only: bool = False, edges_only: bool = False) -> None:
    """Print a human-readable report to stdout."""

    if report["error"]:
        print(f"ERROR: {report['error']}")
        suggestions = report.get("suggestions", [])
        if suggestions:
            print(f"\nDid you mean:")
            for s in suggestions:
                print(f"  {s}")
        else:
            print("  No alias matches found.")
        return

    node = report["node"]

    # Header
    print("=" * 70)
    print(f"NODE: {node['slug']}")
    if node.get("top_level_alias"):
        print(f"  (resolved from alias → {node['top_level_alias']})")
    print(f"  Name : {node['name']}")
    print(f"  Type : {node['type']}")
    print(f"  File : {node['file_path']}")
    aliases = node.get("aliases", [])
    if aliases:
        alias_strs = aliases if isinstance(aliases, list) else [aliases]
        print(f"  Aliases: {', '.join(str(a) for a in alias_strs)}")
    else:
        print("  Aliases: (none)")

    # Edges
    if not inbound_only:
        edges = report["edges"]
        print()
        print(f"OUTBOUND EDGES ({len(edges)} total)")
        print("-" * 70)
        if not edges:
            print("  (no edges found)")
        for edge in edges:
            status = edge["resolution_status"]
            status_tag = f"[{status}]"
            rev = " (reverse)" if edge["is_reverse"] else ""
            print(f"  {edge['edge_type']}{rev}")
            print(f"    Target title : {edge['target_title']}")
            print(f"    Target slug  : {edge['target_slug']}  {status_tag}")
            print(f"    Raw line     : {edge['raw']}")
            print()

    # Inbound refs
    if not edges_only:
        total = report["inbound_total"]
        refs = report["inbound"]
        print()
        print(f"INBOUND REFERENCES ({total} total, showing {len(refs)})")
        print("-" * 70)
        if not refs:
            print("  (none found)")
        for ref in refs:
            src = ref.get("source_slug", "?")
            anchor = ref.get("anchor_text", "?")
            snippet = ref.get("snippet", ref.get("context_snippet", ""))
            snippet_short = (snippet[:60] + "...") if len(snippet) > 60 else snippet
            print(f"  [{src}]  anchor='{anchor}'")
            print(f"    {snippet_short}")
        print()

    # Summary
    print("=" * 70)
    print(f"SUMMARY: {report['summary']}")


# ---------------------------------------------------------------------------
# JSON printer
# ---------------------------------------------------------------------------

def print_json(report: dict) -> None:
    """Print machine-readable JSON report."""
    # Make file path serializable
    if report.get("node"):
        report["node"]["file_path"] = str(report["node"]["file_path"])
    print(json.dumps(report, indent=2, default=str))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect a single Weirwood Network graph node. "
            "Prints node header, outbound edges with resolution status, "
            "and inbound cross-references."
        )
    )
    parser.add_argument("slug", help="Node slug (e.g. house-stark, eddard-stark)")
    parser.add_argument(
        "--edges-only",
        action="store_true",
        help="Print only outbound edges, skip inbound references.",
    )
    parser.add_argument(
        "--inbound-only",
        action="store_true",
        help="Print only inbound references (top 50).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output machine-readable JSON instead of formatted text.",
    )

    args = parser.parse_args()

    if args.edges_only and args.inbound_only:
        parser.error("--edges-only and --inbound-only are mutually exclusive.")

    inbound_limit = 50 if args.inbound_only else 20

    report = build_report(
        args.slug,
        edges_only=args.edges_only,
        inbound_only=args.inbound_only,
        inbound_limit=inbound_limit,
    )

    if args.json_output:
        print_json(report)
    else:
        print_report(report, inbound_only=args.inbound_only, edges_only=args.edges_only)

    # Exit code: 1 if node not found
    if report["error"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
