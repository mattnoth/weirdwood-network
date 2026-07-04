"""traverse.py — Graph traversal operations for the Weirwood query engine.

Absorbs the CANONICAL EDGE LAYER modes from scripts/graph-query.py:
  --neighbors, --path, --health, --event-participants, --causal-chain,
  --full-chain, --expand-beats (modifier), --container.

Also ports `familyTree` TS -> Python (design.md step 1, the first parity op):
a verbatim algorithmic port of web/src/lib/graph.ts::familyTree, adapted to
the Python edge-dict convention (`edges: list[dict]`) instead of the TS
`GraphData` shape. Same caps (GENEALOGY_UP/DOWN_DEFAULT, MAX_FAMILY_MEMBERS,
DEEP_SPINE_MAX_DEPTH, DEEP_SPINE_ANCHORS), same algorithm (breadth BFS +
deep-spine threading via prominence = degree + 4*quoteCount), same output
shape translated to Python dicts.

ZERO BEHAVIOR CHANGE for everything else: every function below is a
line-for-line port of graph-query.py's corresponding cmd_*/helper function,
operating on plain edge dicts (not Edge dataclass instances) to match the
exact calling convention the absorbed unit tests already exercise
(tests/test_graph_query_edges.py, tests/test_graph_query_hardening.py).
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .load import (
    NODES_DIR,
    build_node_index,
    find_node_file,
    iter_all_nodes,
    parse_frontmatter,
    parse_quotes,
    split_sections,
)

# Trust boundary for node slugs — verbatim port of web/src/lib/validate.ts's
# SLUG_RE (kebab-case, lowercase alphanumerics + hyphens, <= 200 chars). Any
# slug that fails this regex is untrusted input (e.g. "../etc/passwd") and
# must yield the fully-empty result shape, never a lookup attempt.
_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,199}$")


def _is_valid_slug(slug: object) -> bool:
    """True if `slug` is a well-formed node slug — same semantics as
    web/src/lib/validate.ts::isValidSlug."""
    return isinstance(slug, str) and bool(_SLUG_RE.match(slug))

# ---------------------------------------------------------------------------
# Node header helper
# ---------------------------------------------------------------------------

def node_header(slug: str, nodes_dir: Path = NODES_DIR) -> str:
    """Return a one-line description of a slug: 'name (type)' or just slug."""
    node_file = find_node_file(slug, nodes_dir)
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


def _short_quote(quote: str, max_len: int = 80) -> str:
    """Truncate a quote to max_len with an ellipsis if needed."""
    if not quote:
        return ""
    quote = quote.replace("\n", " ").strip()
    return (quote[:max_len] + "...") if len(quote) > max_len else quote


# ---------------------------------------------------------------------------
# neighbors(slug)
# ---------------------------------------------------------------------------

def neighbors(slug: str, edges: list[dict], nodes_dir: Path = NODES_DIR) -> dict[str, Any]:
    """All edges touching `slug`, split outgoing/incoming, grouped by
    edge_type. Absorbed from graph-query.py::cmd_neighbors (JSON shape).

    `node_file` (str or None) is carried in the result so text-mode printers
    can reproduce the old script's "File: <path>" line without a second
    filesystem lookup — JSON output does not include it (matches the old
    script's JSON shape exactly, which never emitted node_file either)."""
    outgoing: list[dict] = [e for e in edges if e.get("source_slug") == slug]
    incoming: list[dict] = [e for e in edges if e.get("target_slug") == slug]

    node_file = find_node_file(slug, nodes_dir)

    return {
        "slug": slug,
        "node_header": node_header(slug, nodes_dir),
        "node_file": str(node_file) if node_file else None,
        "outgoing_count": len(outgoing),
        "incoming_count": len(incoming),
        "outgoing": _edges_to_neighbor_records(outgoing, direction="outgoing"),
        "incoming": _edges_to_neighbor_records(incoming, direction="incoming"),
    }


def _edges_to_neighbor_records(edges: list[dict], *, direction: str) -> list[dict]:
    """Convert edge dicts to lean neighbor records."""
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
# path(slug_a, slug_b)
# ---------------------------------------------------------------------------

BRIDGE_CAP = 50


def path(slug_a: str, slug_b: str, edges: list[dict]) -> dict[str, Any]:
    """Direct edges between A and B, then 2-hop bridges. Absorbed from
    graph-query.py::cmd_path (JSON shape)."""
    direct: list[dict] = [
        e for e in edges
        if (e.get("source_slug") == slug_a and e.get("target_slug") == slug_b)
        or (e.get("source_slug") == slug_b and e.get("target_slug") == slug_a)
    ]

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

    bridge_slugs = (set(neighbors_a.keys()) & set(neighbors_b.keys())) - {slug_a, slug_b}
    total_bridges = len(bridge_slugs)

    bridges: list[dict] = []
    for bridge in sorted(bridge_slugs):
        leg_a = neighbors_a[bridge]
        leg_b = neighbors_b[bridge]
        a_types = sorted({e.get("edge_type", "?") for e in leg_a})
        b_types = sorted({e.get("edge_type", "?") for e in leg_b})

        a_dir = _leg_direction(slug_a, leg_a)
        b_dir = _leg_direction(slug_b, leg_b)

        bridges.append({
            "bridge": bridge,
            "a_types": a_types,
            "b_types": b_types,
            "a_dir": a_dir,
            "b_dir": b_dir,
            "a_edge_count": len(leg_a),
            "b_edge_count": len(leg_b),
        })

    bridges.sort(key=lambda x: -(x["a_edge_count"] + x["b_edge_count"]))
    displayed_bridges = bridges[:BRIDGE_CAP]

    return {
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


def _leg_direction(pivot: str, leg_edges: list[dict]) -> str:
    """Determine the dominant direction on a leg ('out', 'in', or 'both')."""
    out_count = sum(1 for e in leg_edges if e.get("source_slug") == pivot)
    in_count = sum(1 for e in leg_edges if e.get("target_slug") == pivot)
    if out_count > 0 and in_count > 0:
        return "both"
    if out_count > 0:
        return "out"
    return "in"


# ---------------------------------------------------------------------------
# health()
# ---------------------------------------------------------------------------

DEGREE_TOP_N = 20


def health(edges: list[dict], nodes_dir: Path = NODES_DIR) -> dict[str, Any]:
    """Graph-wide health stats: node count, edge count, type distribution,
    orphan endpoints, degree leaders. Absorbed from
    graph-query.py::cmd_health (JSON shape)."""
    node_files = list(nodes_dir.rglob("*.node.md")) if nodes_dir.exists() else []
    node_count = len(node_files)
    node_slugs: set[str] = {f.stem.replace(".node", "") for f in node_files}

    edge_count = len(edges)
    type_counter: Counter = Counter(e.get("edge_type", "?") for e in edges)

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

    orphan_endpoints = sorted(all_endpoints - node_slugs)
    orphan_count = len(orphan_endpoints)

    degree_leaders = degree.most_common(DEGREE_TOP_N)

    return {
        "node_count": node_count,
        "edge_count": edge_count,
        "unique_endpoints": endpoint_count,
        "orphan_endpoint_count": orphan_count,
        "orphan_endpoints": orphan_endpoints,
        "edge_type_distribution": type_counter.most_common(),
        "degree_leaders": [{"slug": s, "degree": d} for s, d in degree_leaders],
    }


# ---------------------------------------------------------------------------
# event_participants(hub_slug)
# ---------------------------------------------------------------------------

PARTICIPANT_ROLE_TYPES: frozenset[str] = frozenset(
    {"AGENT_IN", "COMMANDS_IN", "VICTIM_IN", "WIELDED_IN", "ATTENDS", "LOCATED_AT"}
)


def slug_prefix_suggestions(missing_slug: str, nodes_dir: Path = NODES_DIR, max_results: int = 5) -> list[str]:
    """Return up to max_results existing slugs sharing significant tokens
    with the missing slug. Absorbed from graph-query.py."""
    if not nodes_dir.exists():
        return []

    tokens = [t for t in missing_slug.split("-") if len(t) >= 3]
    if not tokens:
        return []

    all_slugs: list[tuple[int, str]] = []

    for type_dir in nodes_dir.iterdir():
        if not type_dir.is_dir():
            continue
        for node_file in type_dir.glob("*.node.md"):
            slug = node_file.stem.replace(".node", "")
            hits = sum(1 for t in tokens if t in slug)
            if hits > 0:
                all_slugs.append((hits, slug))

    all_slugs.sort(key=lambda x: (-x[0], x[1]))
    return [slug for _, slug in all_slugs[:max_results]]


def event_participants(
    hub_slug: str, edges: list[dict], nodes_dir: Path = NODES_DIR
) -> dict[str, Any]:
    """Union the participant role edges across all SUB_BEAT_OF children of
    hub_slug. Absorbed from graph-query.py::cmd_event_participants (JSON
    shape, error branch included)."""
    hub_node_file = find_node_file(hub_slug, nodes_dir)
    if hub_node_file is None:
        suggestions = slug_prefix_suggestions(hub_slug, nodes_dir, max_results=5)
        return {
            "error": f"hub not found: '{hub_slug}'",
            "hint": "Check spelling — no node file found for this slug.",
            "suggestions": suggestions,
        }

    beat_edges: list[dict] = [
        e for e in edges
        if e.get("edge_type") == "SUB_BEAT_OF" and e.get("target_slug") == hub_slug
    ]
    beat_slugs: list[str] = [e["source_slug"] for e in beat_edges]

    if not beat_slugs:
        return {
            "hub_slug": hub_slug,
            "hub_node": node_header(hub_slug, nodes_dir),
            "beat_count": 0,
            "participant_count": 0,
            "participants": [],
            "message": (
                "no beats found; this hub has no reified children "
                "(no SUB_BEAT_OF edges incoming)"
            ),
        }

    participant_records: list[dict] = []
    beat_slug_set = set(beat_slugs)
    for e in edges:
        if e.get("edge_type") in PARTICIPANT_ROLE_TYPES and e.get("target_slug") in beat_slug_set:
            participant_records.append({
                "role_type": e["edge_type"],
                "source_slug": e.get("source_slug", "?"),
                "beat_slug": e.get("target_slug", "?"),
                "evidence_book": e.get("evidence_book", ""),
                "evidence_chapter": e.get("evidence_chapter", ""),
                "evidence_quote": e.get("evidence_quote", ""),
                "confidence_tier": e.get("confidence_tier"),
            })

    return {
        "hub_slug": hub_slug,
        "hub_node": node_header(hub_slug, nodes_dir),
        "beat_count": len(beat_slugs),
        "beats": beat_slugs,
        "participant_count": len(participant_records),
        "participants": [
            {**r, "evidence_quote": _short_quote(r["evidence_quote"], 120)}
            for r in participant_records
        ],
    }


# ---------------------------------------------------------------------------
# causal_chain(slug)
# ---------------------------------------------------------------------------

CAUSAL_EDGE_TYPES: frozenset[str] = frozenset({"CAUSES", "TRIGGERS", "MOTIVATES"})
FULL_CHAIN_EDGE_TYPES: frozenset[str] = CAUSAL_EDGE_TYPES | frozenset({"ENABLES"})
ROLE_EDGE_TYPES: frozenset[str] = frozenset(
    {"AGENT_IN", "VICTIM_IN", "COMMANDS_IN", "WITNESS_IN", "WIELDED_IN"}
)


def _walk_causal(
    start: str,
    edges: list[dict],
    *,
    direction: str,
    edge_types: frozenset[str] = CAUSAL_EDGE_TYPES,
) -> list[dict]:
    """BFS-walk causal edges transitively from `start`. Absorbed verbatim
    from graph-query.py::_walk_causal."""
    causal = [e for e in edges if e.get("edge_type") in edge_types]
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
    """Compact view of a causal edge. Absorbed verbatim."""
    return {
        "edge_type": e.get("edge_type"),
        "source_slug": e.get("source_slug"),
        "target_slug": e.get("target_slug"),
        "depth": e.get("depth"),
        "confidence_tier": e.get("confidence_tier"),
        "evidence_ref": e.get("evidence_ref"),
        "evidence_quote": _short_quote(e.get("evidence_quote", ""), 120),
    }


def _edge_label(e: dict) -> str:
    """Render an edge_type, tagging ENABLES as a precondition. Absorbed
    verbatim."""
    et = e.get("edge_type", "")
    return "ENABLES (precondition)" if et == "ENABLES" else et


def _beats_for_node(node: str, edges: list[dict]) -> list[dict]:
    """Return the SUB_BEAT_OF children of `node`, each annotated with its
    role edges. Absorbed verbatim from graph-query.py::_beats_for_node."""
    children = sorted(
        e["source_slug"]
        for e in edges
        if e.get("edge_type") == "SUB_BEAT_OF" and e.get("target_slug") == node
    )
    out: list[dict] = []
    for child in children:
        roles = sorted(
            (e["edge_type"], e["source_slug"])
            for e in edges
            if e.get("target_slug") == child and e.get("edge_type") in ROLE_EDGE_TYPES
        )
        out.append({"beat": child, "roles": roles})
    return out


def causal_chain(
    slug: str,
    edges: list[dict],
    *,
    edge_types: frozenset[str] = CAUSAL_EDGE_TYPES,
    expand_beats: bool = False,
) -> dict[str, Any]:
    """Walk causal edges both directions from `slug`. Absorbed from
    graph-query.py::cmd_causal_chain (JSON shape)."""
    upstream = _walk_causal(slug, edges, direction="up", edge_types=edge_types)
    downstream = _walk_causal(slug, edges, direction="down", edge_types=edge_types)

    upstream_nodes = sorted({e["source_slug"] for e in upstream})
    downstream_nodes = sorted({e["target_slug"] for e in downstream})
    full = "ENABLES" in edge_types
    mode = "full-chain" if full else "causal-chain"

    chain_nodes: list[str] = [slug]
    seen = {slug}
    for e in upstream + downstream:
        for s in (e["source_slug"], e["target_slug"]):
            if s not in seen:
                seen.add(s)
                chain_nodes.append(s)
    beat_map = (
        {n: b for n in chain_nodes if (b := _beats_for_node(n, edges))}
        if expand_beats else {}
    )

    result = {
        "slug": slug,
        "mode": mode,
        "edge_types": sorted(edge_types),
        "upstream_count": len(upstream),
        "downstream_count": len(downstream),
        "upstream": [_causal_brief(e) for e in upstream],
        "downstream": [_causal_brief(e) for e in downstream],
        "upstream_nodes": upstream_nodes,
        "downstream_nodes": downstream_nodes,
    }
    if expand_beats:
        result["beats"] = beat_map
    return result


# ---------------------------------------------------------------------------
# container(name)
# ---------------------------------------------------------------------------

def _node_containers(fields: dict) -> list[str]:
    """Normalize a node's `containers:` frontmatter into a list of names.
    Absorbed verbatim from graph-query.py::_node_containers."""
    raw = fields.get("containers")
    if raw is None:
        return []
    if isinstance(raw, list):
        return [str(x).strip().strip("'\"") for x in raw if str(x).strip()]
    if isinstance(raw, str):
        s = raw.strip()
        if s in ("", "null", "~", "[]"):
            return []
        s = s.strip("[]")
        return [x.strip().strip("'\"") for x in s.split(",") if x.strip()]
    return []


def container(name: str, nodes_dir: Path = NODES_DIR) -> dict[str, Any]:
    """Bag-retrieval: list every node whose `containers:` array contains
    `name` (unordered). Absorbed from graph-query.py::cmd_container (JSON
    shape)."""
    target = name.strip().lower()
    index = build_node_index(nodes_dir)
    matches: list[dict] = []
    for slug, path_ in index.items():
        try:
            fields, _ = parse_frontmatter(path_.read_text(encoding="utf-8"))
        except Exception:
            continue
        names = [c.lower() for c in _node_containers(fields)]
        if target in names:
            matches.append({
                "slug": slug,
                "type": fields.get("type", ""),
                "name": fields.get("name", slug),
                "containers": _node_containers(fields),
            })
    matches.sort(key=lambda m: (m["type"], m["slug"]))

    return {"container": name, "count": len(matches), "nodes": matches}


# ---------------------------------------------------------------------------
# familyTree(slug) — ported from web/src/lib/graph.ts (design.md step 1,
# the first Python<->TS parity op). Operates on plain edge dicts (source_slug/
# target_slug/edge_type/...) and a nodes map ({slug: {name, type, quotes}})
# rather than the TS GraphData shape.
# ---------------------------------------------------------------------------

GENEALOGY_DOWN_DEFAULT = 4
GENEALOGY_UP_DEFAULT = 2
MAX_FAMILY_MEMBERS = 96
DEEP_SPINE_MAX_DEPTH = 14
DEEP_SPINE_ANCHORS = 24


def _humanize_slug(slug: str) -> str:
    """'aerion-targaryen-son-of-daemion' -> 'Aerion Targaryen Son Of Daemion'."""
    return " ".join(w[:1].upper() + w[1:] if w else w for w in slug.split("-"))


def build_family_nodes_map(nodes_dir: Path = NODES_DIR) -> dict[str, dict]:
    """Build the {slug: {name, type, quotes: [...]}} map `family_tree` reads
    for display enrichment + the prominence proxy (degree + 4*quoteCount).

    Reads every graph/nodes/**/*.node.md (~8.7k files, ~2-3s) via
    load.iter_all_nodes + the `## Quotes` section parser — the same fields
    web/data/nodes.json's bundle build derives from the same source files, so
    results match the TS-side nodes map on live data. Callers on a hot path
    that don't need family_tree should not call this (it is only invoked from
    the --family-tree / `family` CLI paths)."""
    nodes: dict[str, dict] = {}
    for node in iter_all_nodes(nodes_dir):
        quotes_text = split_sections(node.body).get("quotes", "")
        nodes[node.slug] = {
            "name": node.name,
            "type": node.type,
            "quotes": parse_quotes(quotes_text),
        }
    return nodes


def family_tree(
    slug: str,
    edges: list[dict],
    nodes: dict[str, dict] | None = None,
    *,
    generations_up: int = GENEALOGY_UP_DEFAULT,
    generations_down: int = GENEALOGY_DOWN_DEFAULT,
) -> dict[str, Any]:
    """Walk the lineage around `slug`: descendants (down, via PARENT_OF
    source->target) and ancestors (up), with spouses attached at each
    member's generation. Ported from web/src/lib/graph.ts::familyTree —
    same algorithm, same caps, same prominence formula (degree + 4*quoteCount).

    `nodes` is an optional {slug: {name, type, quotes: [...]}} map used only
    for display enrichment (name/type/quoteCount) — the traversal itself is
    edge-only. Absent entries fall back to a humanized slug, `hasNode=False`.
    """
    if nodes is None:
        nodes = {}

    empty = {
        "root": str(slug),
        "generations_up": generations_up,
        "generations_down": generations_down,
        "members": [],
        "parent_bonds": [],
        "spouse_bonds": [],
        "member_count": 0,
        "truncated": False,
    }
    if not _is_valid_slug(slug):
        return empty

    children_of: dict[str, list[dict]] = defaultdict(list)
    parents_of: dict[str, list[dict]] = defaultdict(list)
    spouses_of: dict[str, list[dict]] = defaultdict(list)
    degree: dict[str, int] = defaultdict(int)
    for e in edges:
        src, tgt = e.get("source_slug"), e.get("target_slug")
        if src:
            degree[src] += 1
        if tgt:
            degree[tgt] += 1
        if e.get("edge_type") == "PARENT_OF":
            if src:
                children_of[src].append(e)
            if tgt:
                parents_of[tgt].append(e)
        elif e.get("edge_type") == "SPOUSE_OF":
            if src:
                spouses_of[src].append(e)
            if tgt:
                spouses_of[tgt].append(e)

    generation: dict[str, int] = {slug: 0}
    truncated = False

    def cap_reached() -> bool:
        return len(generation) >= MAX_FAMILY_MEMBERS

    # BFS descendants (down)
    down: list[tuple[str, int]] = [(slug, 0)]
    while down:
        node, gen = down.pop(0)
        if gen >= generations_down:
            continue
        for e in children_of.get(node, []):
            tgt = e.get("target_slug")
            if tgt is None or tgt in generation:
                continue
            if cap_reached():
                truncated = True
                break
            generation[tgt] = gen + 1
            down.append((tgt, gen + 1))

    # BFS ancestors (up)
    up: list[tuple[str, int]] = [(slug, 0)]
    while up:
        node, gen = up.pop(0)
        if -gen >= generations_up:
            continue
        for e in parents_of.get(node, []):
            src = e.get("source_slug")
            if src is None or src in generation:
                continue
            if cap_reached():
                truncated = True
                break
            generation[src] = gen - 1
            up.append((src, gen - 1))

    # Deep main-line spine (additive; only when a full/deep view was asked for)
    if generations_down >= GENEALOGY_DOWN_DEFAULT and not cap_reached():
        desc_depth: dict[str, int] = {slug: 0}
        desc_parent: dict[str, str] = {}
        dq: list[tuple[str, int]] = [(slug, 0)]
        while dq:
            node, d = dq.pop(0)
            if d >= DEEP_SPINE_MAX_DEPTH:
                continue
            for e in children_of.get(node, []):
                tgt = e.get("target_slug")
                if tgt is None or tgt in desc_depth:
                    continue
                desc_depth[tgt] = d + 1
                desc_parent[tgt] = node
                dq.append((tgt, d + 1))

        def prominence(s: str) -> float:
            quote_count = len((nodes.get(s) or {}).get("quotes") or [])
            return degree.get(s, 0) + 4 * quote_count

        deep_anchors = sorted(
            (s for s in desc_depth if desc_depth[s] > generations_down and s not in generation),
            key=prominence,
            reverse=True,
        )[:DEEP_SPINE_ANCHORS]

        for anchor in deep_anchors:
            path_: list[str] = []
            n: str | None = anchor
            while n is not None and n not in generation:
                path_.append(n)
                n = desc_parent.get(n)
            hit_cap = False
            for s in reversed(path_):
                if s in generation:
                    continue
                if cap_reached():
                    truncated = True
                    hit_cap = True
                    break
                generation[s] = desc_depth[s]
            if hit_cap:
                break

    # Attach spouses at the same generation as their partner.
    for member in list(generation.keys()):
        for e in spouses_of.get(member, []):
            src, tgt = e.get("source_slug"), e.get("target_slug")
            spouse = tgt if src == member else src
            if spouse is None or spouse in generation:
                continue
            if cap_reached():
                truncated = True
                break
            generation[spouse] = generation[member]

    # Collect bonds whose both endpoints are members.
    parent_bonds: list[dict] = []
    spouse_seen: set[str] = set()
    spouse_bonds: list[dict] = []
    for e in edges:
        if e.get("edge_type") == "PARENT_OF":
            src, tgt = e.get("source_slug"), e.get("target_slug")
            if src in generation and tgt in generation:
                parent_bonds.append({
                    "parent": src,
                    "child": tgt,
                    "ref": e.get("evidence_ref"),
                    "tier": e.get("confidence_tier"),
                })
        elif e.get("edge_type") == "SPOUSE_OF":
            src, tgt = e.get("source_slug"), e.get("target_slug")
            if src not in generation or tgt not in generation:
                continue
            a, b = (src, tgt) if src < tgt else (tgt, src)
            key = f"{a} {b}"
            if key in spouse_seen:
                continue
            spouse_seen.add(key)
            spouse_bonds.append({
                "a": a, "b": b,
                "ref": e.get("evidence_ref"),
                "tier": e.get("confidence_tier"),
            })

    members: list[dict] = []
    for s, gen in sorted(generation.items(), key=lambda kv: kv[1]):
        rec = nodes.get(s)
        quote_count = len((rec or {}).get("quotes") or [])
        deg = degree.get(s, 0)
        members.append({
            "slug": s,
            "name": (rec or {}).get("name") or _humanize_slug(s),
            "type": (rec or {}).get("type"),
            "generation": gen,
            "has_node": rec is not None,
            "degree": deg,
            "quote_count": quote_count,
            "prominence": deg + 4 * quote_count,
        })

    return {
        "root": slug,
        "root_name": (nodes.get(slug) or {}).get("name"),
        "generations_up": generations_up,
        "generations_down": generations_down,
        "members": members,
        "parent_bonds": parent_bonds,
        "spouse_bonds": spouse_bonds,
        "member_count": len(members),
        "truncated": truncated,
    }
