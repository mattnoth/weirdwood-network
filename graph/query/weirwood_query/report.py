"""report.py — Reporting operations for the Weirwood query engine.

Absorbs scripts/graph-query.py's original node-INSPECTION mode (the
positional `<slug>` report: header + outbound `## Edges` markdown parse +
inbound cross-references + summary line). This is the ONE mode that reads the
legacy node-body `## Edges` markdown rather than edges.jsonl (G16) — kept
separate from traverse.py because it is fundamentally a different data
source (display prose vs. the canonical edge layer).

`traverse.health()` (graph-wide stats) lives in traverse.py, not here, since
it operates on edges.jsonl like the rest of that module; this module is
reserved for the node-prose report and future --explain support (step 9).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from .load import (
    NODES_DIR,
    find_node_file,
    load_legacy_alias_resolver,
    parse_frontmatter,
    stream_inbound_refs,
)
from .normalize import title_to_slug

# ---------------------------------------------------------------------------
# Edge-bullet parser (## Edges section prose) — absorbed verbatim from
# scripts/graph-query.py. Display-only; NOT the edge source of truth.
# ---------------------------------------------------------------------------

_EDGE_LINE_RE = re.compile(
    r"^-\s+"
    r"(?P<edge_type>[A-Z_]+)"
    r"(?P<reverse>\s+\(reverse\))?"
    r"\s*:\s*"
    r"(?P<rest>.+)$"
)


def parse_edge_line(line: str) -> dict | None:
    """Parse a single edge bullet line from node-body prose. Returns dict or
    None if not an edge. Absorbed verbatim from graph-query.py."""
    m = _EDGE_LINE_RE.match(line.strip())
    if not m:
        return None

    edge_type = m.group("edge_type")
    is_reverse = bool(m.group("reverse"))
    rest = m.group("rest").strip()

    qualifier_match = re.search(r"\[([^\]]+)\]$", rest)
    qualifier = qualifier_match.group(1) if qualifier_match else None

    track_b_match = re.search(r"\(track_b:\s*([^)]+)\)", rest)
    track_b = track_b_match.group(1).strip() if track_b_match else None

    target_raw = rest
    target_raw = re.sub(r"\s*\(track_b:[^)]*\)", "", target_raw).strip()
    target_raw = re.sub(r"\s*\[[^\]]*\]$", "", target_raw).strip()
    target_raw = re.sub(r"\s*\(qualifier:[^)]*\)", "", target_raw).strip()
    target_raw = re.sub(r"\s*\(wiki:[^)]*\)", "", target_raw).strip()
    if " → " in target_raw:
        target_raw = target_raw.split(" → ")[0].strip()

    target_title = target_raw.strip().strip('"')

    return {
        "edge_type": edge_type,
        "is_reverse": is_reverse,
        "target_title": target_title,
        "qualifier": qualifier,
        "track_b": track_b,
        "raw": line.strip(),
    }


def extract_edges_markdown(body: str) -> list[dict]:
    """Parse all edge bullets from the `## Edges` section of a node body
    (display prose — see module docstring / G16). Absorbed verbatim."""
    edges: list[dict] = []
    in_edges = False

    for line in body.splitlines():
        stripped = line.strip()
        if re.match(r"^##\s+Edges", stripped):
            in_edges = True
            continue
        if in_edges:
            if stripped.startswith("## ") and not re.match(r"^##\s+Edges", stripped):
                break
            if stripped.startswith("- "):
                parsed = parse_edge_line(stripped)
                if parsed:
                    edges.append(parsed)
    return edges


# ---------------------------------------------------------------------------
# Edge target resolution (against the node file layer, using the legacy
# alias-resolver.json — distinct from resolve.py's phrase resolver)
# ---------------------------------------------------------------------------

def resolve_edge_target(
    target_title: str,
    alias_map: dict[str, str],
    nodes_dir: Path = NODES_DIR,
) -> tuple[str, str, str | None]:
    """Resolve a target title to (slug, status, canonical_slug_if_alias).
    status is one of: "OK", "ORPHAN", "ALIAS→<canonical>". Absorbed verbatim."""
    raw_slug = title_to_slug(target_title)

    file_path = find_node_file(raw_slug, nodes_dir)
    if file_path:
        return raw_slug, "OK", None

    canonical = alias_map.get(raw_slug)
    if canonical:
        canon_file = find_node_file(canonical, nodes_dir)
        if canon_file:
            return raw_slug, f"ALIAS→{canonical}", canonical
        else:
            return raw_slug, f"ALIAS→{canonical} [ORPHAN]", canonical

    return raw_slug, "ORPHAN", None


def slow_alias_search(missing_slug: str, nodes_dir: Path = NODES_DIR) -> list[str]:
    """Search all node frontmatter for the missing_slug in aliases list.
    O(nodes * aliases) — only used on the not-found path. Absorbed verbatim."""
    matches: list[str] = []
    if not nodes_dir.exists():
        return matches

    for type_dir in nodes_dir.iterdir():
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
                aliases_raw = [aliases_raw] if aliases_raw else []
            for alias in aliases_raw:
                if title_to_slug(str(alias)) == missing_slug:
                    node_slug = fields.get("slug") or node_file.stem.replace(".node", "")
                    matches.append(node_slug)
    return matches


# ---------------------------------------------------------------------------
# build_report(slug) — the positional node-inspection report
# ---------------------------------------------------------------------------

def build_report(
    slug: str,
    *,
    edges_only: bool = False,
    inbound_only: bool = False,
    inbound_limit: int = 20,
    nodes_dir: Path = NODES_DIR,
) -> dict[str, Any]:
    """Build a structured node report dict. Reads the legacy `## Edges`
    node-body prose (NOT edges.jsonl — see module docstring / G16) for the
    outbound side, and cross-references.jsonl for inbound. Absorbed verbatim
    from graph-query.py::build_report."""
    alias_map = load_legacy_alias_resolver()

    top_level_alias: str | None = None
    resolved_slug = slug

    node_file = find_node_file(slug, nodes_dir)

    if node_file is None and slug in alias_map:
        resolved_slug = alias_map[slug]
        top_level_alias = resolved_slug
        node_file = find_node_file(resolved_slug, nodes_dir)

    if node_file is None:
        print(
            f"Warning: no node file for slug '{slug}'. "
            "Searching frontmatter aliases (slow)...",
            file=sys.stderr,
        )
        suggestions = slow_alias_search(slug, nodes_dir)
        if not suggestions:
            from .traverse import slug_prefix_suggestions
            suggestions = slug_prefix_suggestions(slug, nodes_dir)
        return {
            "error": f"No node found for slug '{slug}'",
            "suggestions": suggestions,
            "node": None,
            "edges": [],
            "inbound": [],
            "inbound_total": 0,
            "summary": None,
        }

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

    edges_data: list[dict] = []
    if not inbound_only:
        raw_edges = extract_edges_markdown(body)
        for edge in raw_edges:
            target_slug, status, canonical = resolve_edge_target(
                edge["target_title"], alias_map, nodes_dir
            )
            edges_data.append({
                **edge,
                "target_slug": target_slug,
                "resolution_status": status,
                "canonical_slug": canonical,
            })

    inbound_data: list[dict] = []
    inbound_total = 0
    if not edges_only:
        query_slug = fields.get("slug", resolved_slug)
        inbound_data, inbound_total = stream_inbound_refs(query_slug, limit=inbound_limit)

    if not inbound_only:
        ok_count = sum(1 for e in edges_data if e["resolution_status"] == "OK")
        alias_count = sum(1 for e in edges_data if "ALIAS" in e["resolution_status"])
        orphan_count = sum(
            1 for e in edges_data
            if "ORPHAN" in e["resolution_status"] and "ALIAS" not in e["resolution_status"]
        )
        summary = (
            f"{len(edges_data)} outbound edges "
            f"({ok_count} OK, {alias_count} alias-resolved, {orphan_count} orphan), "
            f"{inbound_total} inbound references."
        )
    else:
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
