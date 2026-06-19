#!/usr/bin/env python3
"""graph-query.py — Read-only inspection primitive for Weirwood Network graph nodes.

Prints a human-readable (or machine-readable) report for a single node:
  1. Node header: slug, name, type, file path, aliases.
  2. Outbound edges: parsed from ## Edges section, with target slug resolution
     and file-existence checks (OK / ORPHAN / ALIAS→canonical).
  3. Inbound references: rows from cross-references.jsonl where target_slug
     matches this node. Top 20 by default.
  4. Summary line.

NODE INSPECTION (original modes):
  python3 scripts/graph-query.py <slug>
  python3 scripts/graph-query.py <slug> --edges-only
  python3 scripts/graph-query.py <slug> --inbound-only
  python3 scripts/graph-query.py <slug> --json

CANONICAL EDGE LAYER (graph/edges/edges.jsonl):
  python3 scripts/graph-query.py --neighbors <slug>
  python3 scripts/graph-query.py --path <slugA> <slugB>
  python3 scripts/graph-query.py --health
  python3 scripts/graph-query.py --event-participants <hub-slug>
  python3 scripts/graph-query.py --edges <path>   # override edges.jsonl location
  python3 scripts/graph-query.py --help
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
NODES_DIR = PROJECT_ROOT / "graph" / "nodes"
CROSS_REFS_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "cross-references.jsonl"
ALIAS_RESOLVER_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "alias-resolver.json"
DEFAULT_EDGES_FILE = PROJECT_ROOT / "graph" / "edges" / "edges.jsonl"

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


# ===========================================================================
# CANONICAL EDGE LAYER — graph/edges/edges.jsonl
# All functions below read the canonical edge file and are independent of
# the legacy node-inspection code above.
# ===========================================================================

# ---------------------------------------------------------------------------
# edges.jsonl loader
# ---------------------------------------------------------------------------

def load_edges(edges_path: Path) -> list[dict]:
    """Load all edges from a JSONL file.  Returns list of dicts.

    Raises FileNotFoundError with a clear message if the file is missing.
    """
    if not edges_path.exists():
        raise FileNotFoundError(
            f"edges.jsonl not found at {edges_path}. "
            "Run the Stage 4 pipeline first to produce this file."
        )
    rows: list[dict] = []
    with open(edges_path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(
                    f"Warning: JSON decode error on line {lineno} of {edges_path}: {exc}",
                    file=sys.stderr,
                )
    return rows


def _short_quote(quote: str, max_len: int = 80) -> str:
    """Truncate a quote to max_len with an ellipsis if needed."""
    if not quote:
        return ""
    quote = quote.replace("\n", " ").strip()
    return (quote[:max_len] + "...") if len(quote) > max_len else quote


# ---------------------------------------------------------------------------
# Node header helper (for --neighbors / --path output)
# ---------------------------------------------------------------------------

def _node_header(slug: str) -> str:
    """Return a one-line description of a slug: 'name (type)' or just slug if not found."""
    node_file = find_node_file(slug)
    if node_file is None:
        return slug
    try:
        text = node_file.read_text(encoding="utf-8")
        fields, _ = parse_frontmatter(text)
        name = fields.get("name", slug)
        ntype = fields.get("type", "")
        return f"{name} ({ntype})" if ntype else name
    except Exception:
        return slug


# ---------------------------------------------------------------------------
# --neighbors <slug>
# ---------------------------------------------------------------------------

def cmd_neighbors(slug: str, edges: list[dict], *, json_output: bool = False) -> None:
    """Print all edges touching <slug>, grouped by direction and edge_type."""

    outgoing: list[dict] = [e for e in edges if e.get("source_slug") == slug]
    incoming: list[dict] = [e for e in edges if e.get("target_slug") == slug]

    if json_output:
        result = {
            "slug": slug,
            "node_header": _node_header(slug),
            "outgoing_count": len(outgoing),
            "incoming_count": len(incoming),
            "outgoing": _edges_to_neighbor_records(outgoing, direction="outgoing", pivot=slug),
            "incoming": _edges_to_neighbor_records(incoming, direction="incoming", pivot=slug),
        }
        print(json.dumps(result, indent=2, default=str))
        return

    node_file = find_node_file(slug)
    print("=" * 72)
    print(f"NEIGHBORS: {slug}")
    if node_file:
        print(f"  {_node_header(slug)}")
        print(f"  File: {node_file}")
    else:
        print("  (no node file found for this slug)")
    print()

    # OUTGOING
    print(f"OUTGOING ({len(outgoing)} edges — {slug} is source)")
    print("-" * 72)
    if not outgoing:
        print("  (none)")
    else:
        by_type: dict[str, list[dict]] = defaultdict(list)
        for e in outgoing:
            by_type[e.get("edge_type", "?")].append(e)
        for etype in sorted(by_type):
            group = by_type[etype]
            print(f"  [{etype}]  ({len(group)} edge{'s' if len(group) != 1 else ''})")
            for e in group:
                target = e.get("target_slug", "?")
                ref = e.get("evidence_ref", "")
                quote = _short_quote(e.get("evidence_quote", ""), 80)
                print(f"    -> {target}")
                if ref:
                    print(f"       ref  : {ref}")
                if quote:
                    print(f"       quote: \"{quote}\"")

    print()

    # INCOMING
    print(f"INCOMING ({len(incoming)} edges — {slug} is target)")
    print("-" * 72)
    if not incoming:
        print("  (none)")
    else:
        by_type_in: dict[str, list[dict]] = defaultdict(list)
        for e in incoming:
            by_type_in[e.get("edge_type", "?")].append(e)
        for etype in sorted(by_type_in):
            group = by_type_in[etype]
            print(f"  [{etype}]  ({len(group)} edge{'s' if len(group) != 1 else ''})")
            for e in group:
                source = e.get("source_slug", "?")
                ref = e.get("evidence_ref", "")
                quote = _short_quote(e.get("evidence_quote", ""), 80)
                print(f"    <- {source}")
                if ref:
                    print(f"       ref  : {ref}")
                if quote:
                    print(f"       quote: \"{quote}\"")

    print()
    print("=" * 72)
    print(
        f"SUMMARY: {slug}  |  {len(outgoing)} outgoing, {len(incoming)} incoming"
        f"  ({len(outgoing) + len(incoming)} total)"
    )


def _edges_to_neighbor_records(
    edges: list[dict], *, direction: str, pivot: str
) -> list[dict]:
    """Convert edge dicts to lean neighbor records for JSON output."""
    records = []
    for e in edges:
        other = e.get("target_slug") if direction == "outgoing" else e.get("source_slug")
        records.append({
            "edge_type": e.get("edge_type"),
            "other_slug": other,
            "evidence_ref": e.get("evidence_ref"),
            "evidence_quote": _short_quote(e.get("evidence_quote", ""), 120),
            "confidence_tier": e.get("confidence_tier"),
        })
    return records


# ---------------------------------------------------------------------------
# --path <slugA> <slugB>
# ---------------------------------------------------------------------------

BRIDGE_CAP = 50  # maximum bridges to display


def cmd_path(slug_a: str, slug_b: str, edges: list[dict], *, json_output: bool = False) -> None:
    """Print direct edges between A and B, then 2-hop bridges."""

    # (a) Direct edges in either direction
    direct: list[dict] = [
        e for e in edges
        if (e.get("source_slug") == slug_a and e.get("target_slug") == slug_b)
        or (e.get("source_slug") == slug_b and e.get("target_slug") == slug_a)
    ]

    # (b) 2-hop bridges: neighbors of A and neighbors of B, intersected
    # Build neighbor sets: slug → {neighbor_slug: [edges]}
    neighbors_a: dict[str, list[dict]] = defaultdict(list)
    for e in edges:
        if e.get("source_slug") == slug_a:
            neighbors_a[e["target_slug"]].append(e)
        elif e.get("target_slug") == slug_a:
            neighbors_a[e["source_slug"]].append(e)

    neighbors_b: dict[str, list[dict]] = defaultdict(list)
    for e in edges:
        if e.get("source_slug") == slug_b:
            neighbors_b[e["target_slug"]].append(e)
        elif e.get("target_slug") == slug_b:
            neighbors_b[e["source_slug"]].append(e)

    # Common neighbors (bridges), excluding slug_a and slug_b themselves
    bridge_slugs = (set(neighbors_a.keys()) & set(neighbors_b.keys())) - {slug_a, slug_b}
    total_bridges = len(bridge_slugs)

    # For each bridge, collect representative edge types (first edge on each leg)
    bridges: list[dict] = []
    for bridge in sorted(bridge_slugs):
        leg_a = neighbors_a[bridge]
        leg_b = neighbors_b[bridge]
        # Summarize leg types
        a_types = sorted({e.get("edge_type", "?") for e in leg_a})
        b_types = sorted({e.get("edge_type", "?") for e in leg_b})

        # Edge directions from slug_a's perspective on this bridge
        a_dir = _leg_direction(slug_a, bridge, leg_a)
        b_dir = _leg_direction(slug_b, bridge, leg_b)

        bridges.append({
            "bridge": bridge,
            "a_types": a_types,
            "b_types": b_types,
            "a_dir": a_dir,
            "b_dir": b_dir,
            "a_edge_count": len(leg_a),
            "b_edge_count": len(leg_b),
        })

    # Sort bridges by total edge count on both legs (richest connections first)
    bridges.sort(key=lambda x: -(x["a_edge_count"] + x["b_edge_count"]))
    displayed_bridges = bridges[:BRIDGE_CAP]

    if json_output:
        result = {
            "slug_a": slug_a,
            "slug_b": slug_b,
            "direct_edges": [
                {
                    "edge_type": e.get("edge_type"),
                    "source_slug": e.get("source_slug"),
                    "target_slug": e.get("target_slug"),
                    "evidence_ref": e.get("evidence_ref"),
                    "evidence_quote": _short_quote(e.get("evidence_quote", ""), 120),
                    "confidence_tier": e.get("confidence_tier"),
                }
                for e in direct
            ],
            "total_bridges": total_bridges,
            "bridges_shown": len(displayed_bridges),
            "bridges": displayed_bridges,
        }
        print(json.dumps(result, indent=2, default=str))
        return

    print("=" * 72)
    print(f"PATH: {slug_a}  -->  {slug_b}")
    print(f"  A: {_node_header(slug_a)}")
    print(f"  B: {_node_header(slug_b)}")
    print()

    # Direct edges
    print(f"DIRECT EDGES ({len(direct)})")
    print("-" * 72)
    if not direct:
        print("  (no direct edges between these nodes)")
    for e in direct:
        src = e.get("source_slug", "?")
        tgt = e.get("target_slug", "?")
        etype = e.get("edge_type", "?")
        ref = e.get("evidence_ref", "")
        quote = _short_quote(e.get("evidence_quote", ""), 80)
        print(f"  {src}  --[{etype}]-->  {tgt}")
        if ref:
            print(f"    ref  : {ref}")
        if quote:
            print(f"    quote: \"{quote}\"")
        print()

    # 2-hop bridges
    print(
        f"2-HOP BRIDGES ({total_bridges} common neighbors"
        + (f", showing top {BRIDGE_CAP}" if total_bridges > BRIDGE_CAP else "")
        + ")"
    )
    print("-" * 72)
    if not bridges:
        print("  (no common neighbors)")
    for b in displayed_bridges:
        bridge = b["bridge"]
        a_arrow = _format_arrow(slug_a, bridge, b["a_dir"], b["a_types"])
        b_arrow = _format_arrow(slug_b, bridge, b["b_dir"], b["b_types"])
        print(f"  {a_arrow}  --[{bridge}]--  {b_arrow}")

    print()
    print("=" * 72)
    print(
        f"SUMMARY: {slug_a} → {slug_b}  |  "
        f"{len(direct)} direct edges, {total_bridges} 2-hop bridges"
    )


def _leg_direction(pivot: str, other: str, leg_edges: list[dict]) -> str:
    """Determine the dominant direction on a leg ('out', 'in', or 'both')."""
    out_count = sum(1 for e in leg_edges if e.get("source_slug") == pivot)
    in_count = sum(1 for e in leg_edges if e.get("target_slug") == pivot)
    if out_count > 0 and in_count > 0:
        return "both"
    if out_count > 0:
        return "out"
    return "in"


def _format_arrow(pivot: str, bridge: str, direction: str, types: list[str]) -> str:
    """Format a leg as 'pivot --[TYPES]--> bridge' (or reverse)."""
    type_str = "|".join(types) if types else "?"
    if direction == "out":
        return f"{pivot} --[{type_str}]--> {bridge}"
    elif direction == "in":
        return f"{bridge} --[{type_str}]--> {pivot}"
    else:
        return f"{pivot} <-[{type_str}]-> {bridge}"


# ---------------------------------------------------------------------------
# --health
# ---------------------------------------------------------------------------

DEGREE_TOP_N = 20


def cmd_health(
    edges: list[dict],
    nodes_dir: Path,
    *,
    json_output: bool = False,
) -> None:
    """Print graph-wide health stats: node count, edge count, type distribution,
    orphan endpoints, and degree leaders."""

    # Node count
    node_files = list(nodes_dir.rglob("*.node.md")) if nodes_dir.exists() else []
    node_count = len(node_files)
    node_slugs: set[str] = {f.stem.replace(".node", "") for f in node_files}

    # Edge stats
    edge_count = len(edges)
    type_counter: Counter = Counter(e.get("edge_type", "?") for e in edges)

    # Degree
    degree: Counter = Counter()
    for e in edges:
        src = e.get("source_slug")
        tgt = e.get("target_slug")
        if src:
            degree[src] += 1
        if tgt:
            degree[tgt] += 1

    all_endpoints = set(degree.keys())
    endpoint_count = len(all_endpoints)

    # Orphan endpoints: slugs that appear in edges but have NO node file
    orphan_endpoints = sorted(all_endpoints - node_slugs)
    orphan_count = len(orphan_endpoints)

    # Top degree
    degree_leaders = degree.most_common(DEGREE_TOP_N)

    if json_output:
        result = {
            "node_count": node_count,
            "edge_count": edge_count,
            "unique_endpoints": endpoint_count,
            "orphan_endpoint_count": orphan_count,
            "orphan_endpoints": orphan_endpoints,
            "edge_type_distribution": type_counter.most_common(),
            "degree_leaders": [
                {"slug": s, "degree": d} for s, d in degree_leaders
            ],
        }
        print(json.dumps(result, indent=2, default=str))
        return

    print("=" * 72)
    print("GRAPH HEALTH REPORT")
    print("=" * 72)
    print(f"  Node files (*.node.md)  : {node_count:>7,}")
    print(f"  Edge count              : {edge_count:>7,}")
    print(f"  Unique edge endpoints   : {endpoint_count:>7,}")
    print(f"  Orphan endpoints        : {orphan_count:>7,}  "
          f"(endpoints with no node file)")
    print()

    # Edge-type distribution
    print(f"EDGE-TYPE DISTRIBUTION  ({len(type_counter)} types)")
    print("-" * 72)
    for etype, cnt in type_counter.most_common():
        bar = "#" * min(cnt // 5, 40)
        print(f"  {etype:<30}  {cnt:>5}  {bar}")
    print()

    # Orphans list (truncate if very long)
    if orphan_count == 0:
        print("ORPHAN ENDPOINTS: none — all edge endpoints have node files")
    else:
        print(f"ORPHAN ENDPOINTS ({orphan_count})")
        print("-" * 72)
        display_orphans = orphan_endpoints[:50]
        for slug in display_orphans:
            print(f"  {slug}")
        if orphan_count > 50:
            print(f"  ... and {orphan_count - 50} more")
    print()

    # Degree leaders
    print(f"DEGREE LEADERS (top {DEGREE_TOP_N} — total edges touching each entity)")
    print("-" * 72)
    for rank, (slug, deg) in enumerate(degree_leaders, 1):
        bar = "#" * min(deg // 10, 35)
        print(f"  {rank:>2}. {slug:<40}  {deg:>5}  {bar}")

    print()
    print("=" * 72)
    print(f"SUMMARY: {node_count:,} nodes, {edge_count:,} edges, "
          f"{orphan_count} orphan endpoints, "
          f"{len(type_counter)} edge types")


# ---------------------------------------------------------------------------
# --event-participants <hub-slug>
# ---------------------------------------------------------------------------

# Role edge types that represent event participants at the beat level.
# LOCATED_AT is included because it attaches place-nodes (and sometimes
# character-nodes) to beats and is meaningful for "who/what was at the event".
PARTICIPANT_ROLE_TYPES: frozenset[str] = frozenset(
    {
        "AGENT_IN",
        "COMMANDS_IN",
        "VICTIM_IN",
        "WIELDED_IN",
        "ATTENDS",
        "LOCATED_AT",
    }
)


def cmd_event_participants(
    hub_slug: str,
    edges: list[dict],
    *,
    json_output: bool = False,
) -> None:
    """Union the participant role edges across all SUB_BEAT_OF children of hub_slug
    and present them as if directly attached to the hub.

    Algorithm:
      1. Validate hub exists as a node (warn + exit 1 if not).
      2. Find all edges where target_slug == hub_slug AND edge_type == SUB_BEAT_OF.
         Those edges' source_slugs are the beat children.
      3. For each beat child, collect every edge where target_slug == <beat>
         AND edge_type in PARTICIPANT_ROLE_TYPES.
      4. Union the tuples and group by role_type for display.

    Edge cases:
      - Hub not found as a node: "hub not found" message + hint.
      - Hub found but 0 SUB_BEAT_OF incoming: clean "no beats found" message.
    """
    # 1. Hub existence check
    hub_node_file = find_node_file(hub_slug)
    if hub_node_file is None:
        # Try slug-prefix suggestions for a helpful hint
        suggestions = slug_prefix_suggestions(hub_slug, max_results=5)
        if json_output:
            result: dict = {
                "error": f"hub not found: '{hub_slug}'",
                "hint": "Check spelling — no node file found for this slug.",
                "suggestions": suggestions,
            }
            print(json.dumps(result, indent=2))
        else:
            print(f"ERROR: hub not found: '{hub_slug}'")
            print("  No node file found for this slug. Check spelling.")
            if suggestions:
                print("  Did you mean:")
                for s in suggestions:
                    print(f"    {s}")
        return

    # 2. Find beat children (edges where source SUB_BEAT_OF hub)
    beat_edges: list[dict] = [
        e
        for e in edges
        if e.get("edge_type") == "SUB_BEAT_OF" and e.get("target_slug") == hub_slug
    ]
    beat_slugs: list[str] = [e["source_slug"] for e in beat_edges]

    if not beat_slugs:
        if json_output:
            result = {
                "hub_slug": hub_slug,
                "hub_node": _node_header(hub_slug),
                "beat_count": 0,
                "participant_count": 0,
                "participants": [],
                "message": (
                    "no beats found; this hub has no reified children "
                    "(no SUB_BEAT_OF edges incoming)"
                ),
            }
            print(json.dumps(result, indent=2))
        else:
            hub_label = _node_header(hub_slug)
            print("=" * 72)
            print(f"EVENT PARTICIPANTS: {hub_slug}")
            print(f"  {hub_label}")
            print()
            print(
                "  No beats found — this hub has no reified children "
                "(no SUB_BEAT_OF edges incoming)."
            )
            print(
                "  All role edges must be directly on the hub itself (check "
                "--neighbors) or the event has not been mined yet."
            )
            print()
            print("=" * 72)
            print(f"SUMMARY: 0 beats, 0 participants")
        return

    # 3. For each beat, collect participant role edges
    # A "participant record" tracks one (role_type, source_slug, beat_slug) tuple.
    # We keep full edge data for display / JSON.
    participant_records: list[dict] = []

    beat_slug_set = set(beat_slugs)
    for e in edges:
        if e.get("edge_type") in PARTICIPANT_ROLE_TYPES and e.get("target_slug") in beat_slug_set:
            participant_records.append(
                {
                    "role_type": e["edge_type"],
                    "source_slug": e.get("source_slug", "?"),
                    "beat_slug": e.get("target_slug", "?"),
                    "evidence_book": e.get("evidence_book", ""),
                    "evidence_chapter": e.get("evidence_chapter", ""),
                    "evidence_quote": e.get("evidence_quote", ""),
                    "confidence_tier": e.get("confidence_tier"),
                }
            )

    # 4. Output

    if json_output:
        result = {
            "hub_slug": hub_slug,
            "hub_node": _node_header(hub_slug),
            "beat_count": len(beat_slugs),
            "beats": beat_slugs,
            "participant_count": len(participant_records),
            "participants": [
                {
                    **r,
                    "evidence_quote": _short_quote(r["evidence_quote"], 120),
                }
                for r in participant_records
            ],
        }
        print(json.dumps(result, indent=2))
        return

    # Human-readable output — group by role type
    hub_label = _node_header(hub_slug)
    print("=" * 72)
    print(f"EVENT PARTICIPANTS: {hub_slug}")
    print(f"  {hub_label}")
    print(f"  Beats ({len(beat_slugs)}): {', '.join(beat_slugs)}")
    print()

    if not participant_records:
        print("  (beats found but no participant role edges on any beat)")
        print()
        print("=" * 72)
        print(f"SUMMARY: {len(beat_slugs)} beats, 0 participant edges")
        return

    # Group by role_type
    by_role: dict[str, list[dict]] = defaultdict(list)
    for r in participant_records:
        by_role[r["role_type"]].append(r)

    print(f"PARTICIPANTS BY ROLE  ({len(participant_records)} total role edges)")
    print("-" * 72)

    for role_type in sorted(by_role):
        group = by_role[role_type]
        print(f"\n  [{role_type}]  ({len(group)} edge{'s' if len(group) != 1 else ''})")
        for rec in group:
            source = rec["source_slug"]
            beat = rec["beat_slug"]
            chapter = rec.get("evidence_chapter") or rec.get("evidence_book") or ""
            quote_raw = rec.get("evidence_quote", "")
            quote = _short_quote(quote_raw, 120)
            print(f"    {source}")
            print(f"      via beat : {beat}")
            if chapter:
                print(f"      chapter  : {chapter}")
            if quote:
                print(f"      quote    : \"{quote}\"")

    print()
    print("=" * 72)

    # Count distinct participants (source_slugs) across all roles
    distinct_sources = {r["source_slug"] for r in participant_records}
    print(
        f"SUMMARY: {hub_slug}  |  "
        f"{len(beat_slugs)} beats, "
        f"{len(participant_records)} role edges, "
        f"{len(distinct_sources)} distinct participants"
    )


# ---------------------------------------------------------------------------
# --causal-chain <slug>
# ---------------------------------------------------------------------------

# Edge types that carry causal consequence (vs. PRECEDES, which is pure
# chronology). MOTIVATES is event-or-condition → actor; CAUSES/TRIGGERS are
# event → event. Walking all three reconstructs a narrative-arc consequence
# chain ("what set X in motion / what did X lead to") that no single edge holds.
CAUSAL_EDGE_TYPES: frozenset[str] = frozenset({"CAUSES", "TRIGGERS", "MOTIVATES"})


def _walk_causal(start: str, edges: list[dict], *, direction: str) -> list[dict]:
    """BFS-walk causal edges transitively from `start`.

    direction='down' follows edges where source_slug == current node (effects).
    direction='up'   follows edges where target_slug == current node (causes).

    Returns a list of edge dicts, each with an added `depth` key (1 = adjacent
    to `start`), in breadth-first order. Cycle-safe: each node is expanded at
    most once, so every edge is emitted exactly once even across diamonds.
    """
    causal = [e for e in edges if e.get("edge_type") in CAUSAL_EDGE_TYPES]
    adj: dict[str, list[dict]] = defaultdict(list)
    if direction == "down":
        key_here, key_next = "source_slug", "target_slug"
    elif direction == "up":
        key_here, key_next = "target_slug", "source_slug"
    else:  # pragma: no cover - guarded by caller
        raise ValueError(f"direction must be 'up' or 'down', got {direction!r}")
    for e in causal:
        adj[e.get(key_here)].append(e)

    visited: set[str] = {start}
    result: list[dict] = []
    frontier: list[tuple[str, int]] = [(start, 0)]
    while frontier:
        node, depth = frontier.pop(0)
        for e in adj.get(node, []):
            rec = dict(e)
            rec["depth"] = depth + 1
            result.append(rec)
            nxt = e.get(key_next)
            if nxt and nxt not in visited:
                visited.add(nxt)
                frontier.append((nxt, depth + 1))
    return result


def _causal_brief(e: dict) -> dict:
    """Compact JSON-serializable view of a causal edge for --json output."""
    return {
        "edge_type": e.get("edge_type"),
        "source_slug": e.get("source_slug"),
        "target_slug": e.get("target_slug"),
        "depth": e.get("depth"),
        "confidence_tier": e.get("confidence_tier"),
        "evidence_ref": e.get("evidence_ref"),
        "evidence_quote": _short_quote(e.get("evidence_quote", ""), 120),
    }


def cmd_causal_chain(
    slug: str,
    edges: list[dict],
    *,
    json_output: bool = False,
) -> None:
    """Walk CAUSES/TRIGGERS/MOTIVATES both directions from `slug` and print the
    transitive consequence-chain (upstream causes + downstream effects)."""
    upstream = _walk_causal(slug, edges, direction="up")
    downstream = _walk_causal(slug, edges, direction="down")

    upstream_nodes = sorted({e["source_slug"] for e in upstream})
    downstream_nodes = sorted({e["target_slug"] for e in downstream})

    if json_output:
        result = {
            "slug": slug,
            "causal_edge_types": sorted(CAUSAL_EDGE_TYPES),
            "upstream_count": len(upstream),
            "downstream_count": len(downstream),
            "upstream": [_causal_brief(e) for e in upstream],
            "downstream": [_causal_brief(e) for e in downstream],
            "upstream_nodes": upstream_nodes,
            "downstream_nodes": downstream_nodes,
        }
        print(json.dumps(result, indent=2, default=str))
        return

    type_label = " / ".join(sorted(CAUSAL_EDGE_TYPES))
    print("=" * 72)
    print(f"CAUSAL CHAIN: {slug}")
    print(f"  {_node_header(slug)}")
    print(f"  walks {type_label} (transitive, both directions)")
    print()

    # Upstream: render furthest-cause first so the chain reads INTO the node.
    n_up = len(upstream)
    print(f"UPSTREAM — what led to this  ({n_up} edge{'s' if n_up != 1 else ''})")
    print("-" * 72)
    if not upstream:
        print("  (none — no causal antecedents)")
    else:
        for e in sorted(upstream, key=lambda r: (-r["depth"], r["source_slug"])):
            indent = "  " * (e["depth"] - 1)
            print(f"  {indent}{e['source_slug']} --[{e['edge_type']}]--> "
                  f"{e['target_slug']}")
    print()

    # Downstream: render nearest-effect first, chain reads OUT of the node.
    n_down = len(downstream)
    print(f"DOWNSTREAM — what this led to  ({n_down} edge{'s' if n_down != 1 else ''})")
    print("-" * 72)
    if not downstream:
        print("  (none — no causal consequences)")
    else:
        for e in sorted(downstream, key=lambda r: (r["depth"], r["target_slug"])):
            indent = "  " * (e["depth"] - 1)
            print(f"  {indent}{e['source_slug']} --[{e['edge_type']}]--> "
                  f"{e['target_slug']}")
    print()
    print("=" * 72)
    total = n_up + n_down
    print(
        f"SUMMARY: {slug}  |  {n_up} upstream + {n_down} downstream "
        f"= {total} causal edge{'s' if total != 1 else ''}"
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect Weirwood Network graph nodes and edges.\n\n"
            "NODE INSPECTION (original):\n"
            "  graph-query.py <slug> [--edges-only] [--inbound-only] [--json]\n\n"
            "CANONICAL EDGE LAYER:\n"
            "  graph-query.py --neighbors <slug>\n"
            "  graph-query.py --path <slugA> <slugB>\n"
            "  graph-query.py --health\n"
            "  graph-query.py --event-participants <hub-slug>\n"
            "  graph-query.py --causal-chain <slug>\n"
            "  graph-query.py --edges <path>   (override edges.jsonl location)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Positional slug — optional so new modes work without it
    parser.add_argument(
        "slug",
        nargs="?",
        default=None,
        help="Node slug for node inspection (e.g. house-stark, eddard-stark)",
    )

    # --- original flags ---
    parser.add_argument(
        "--edges-only",
        action="store_true",
        help="(node inspection) Print only outbound edges, skip inbound references.",
    )
    parser.add_argument(
        "--inbound-only",
        action="store_true",
        help="(node inspection) Print only inbound references (top 50).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output machine-readable JSON instead of formatted text.",
    )

    # --- new edge-layer flags ---
    parser.add_argument(
        "--neighbors",
        metavar="SLUG",
        default=None,
        help="Show all edges touching SLUG, split into OUTGOING and INCOMING, "
             "grouped by edge_type.",
    )
    parser.add_argument(
        "--path",
        nargs=2,
        metavar=("SLUG_A", "SLUG_B"),
        default=None,
        help="Show direct edges between SLUG_A and SLUG_B, plus 2-hop common "
             "neighbors (bridges).",
    )
    parser.add_argument(
        "--health",
        action="store_true",
        help="Print graph-wide stats: node count, edge count, type distribution, "
             "orphan endpoints, and degree leaders.",
    )
    parser.add_argument(
        "--event-participants",
        metavar="HUB_SLUG",
        default=None,
        dest="event_participants",
        help=(
            "Union the participant role edges (AGENT_IN, COMMANDS_IN, VICTIM_IN, "
            "WIELDED_IN, ATTENDS, LOCATED_AT) across all SUB_BEAT_OF children of "
            "HUB_SLUG and display them as if attached to the hub. Handles reified "
            "event hubs where participants live on beat children, not the parent."
        ),
    )
    parser.add_argument(
        "--causal-chain",
        metavar="SLUG",
        default=None,
        dest="causal_chain",
        help=(
            "Walk CAUSES / TRIGGERS / MOTIVATES edges transitively, both "
            "directions, from SLUG. Returns the upstream causes and downstream "
            "effects — the consequence-chain of a narrative arc that no single "
            "edge holds (e.g. 'what set Tyrion's capture in motion, 3 steps back')."
        ),
    )
    parser.add_argument(
        "--edges",
        metavar="PATH",
        default=None,
        help=f"Override path to edges.jsonl (default: {DEFAULT_EDGES_FILE})",
    )

    args = parser.parse_args()

    # Validate: at most one mode active
    new_mode = (
        args.neighbors
        or args.path
        or args.health
        or args.event_participants
        or args.causal_chain
    )
    old_mode = args.slug is not None

    if new_mode and old_mode:
        parser.error(
            "Cannot combine a positional slug with "
            "--neighbors / --path / --health / --event-participants / "
            "--causal-chain. Use one mode at a time."
        )

    if not new_mode and not old_mode:
        parser.print_help()
        sys.exit(0)

    # ------------------------------------------------------------------
    # NEW EDGE-LAYER MODES
    # ------------------------------------------------------------------
    if new_mode:
        edges_path = Path(args.edges) if args.edges else DEFAULT_EDGES_FILE
        try:
            edges = load_edges(edges_path)
        except FileNotFoundError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            sys.exit(1)

        if args.neighbors:
            cmd_neighbors(args.neighbors, edges, json_output=args.json_output)

        elif args.path:
            cmd_path(args.path[0], args.path[1], edges, json_output=args.json_output)

        elif args.health:
            cmd_health(edges, NODES_DIR, json_output=args.json_output)

        elif args.event_participants:
            cmd_event_participants(
                args.event_participants, edges, json_output=args.json_output
            )

        elif args.causal_chain:
            cmd_causal_chain(
                args.causal_chain, edges, json_output=args.json_output
            )

        sys.exit(0)

    # ------------------------------------------------------------------
    # ORIGINAL NODE-INSPECTION MODE (unchanged behaviour)
    # ------------------------------------------------------------------
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
