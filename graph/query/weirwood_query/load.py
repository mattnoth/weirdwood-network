"""load.py — ONE loader for the Weirwood query engine.

Consolidates three previously-separate loaders (design.md step 1 / G12):
  - scripts/graph-query.py's pyyaml-with-fallback frontmatter parser (WINS —
    design decision: pyyaml first, falling back to a hand-rolled scalar/list
    parser only when pyyaml is unavailable or the block fails to parse).
  - scripts/event_alias_resolver.py's own regex frontmatter parser is NOT
    reused here; its BUILD OUTPUT is preserved exactly by build/
    build_alias_table.py re-deriving the same fields via this module's parser
    (verified by diffing rebuilt output against the live table — see that
    module's docstring).
  - scripts/build-chat-export.py's node-body section splitter + quote parser
    (`## Identity`, `## Quotes`, sort_keys) — absorbed as `split_sections` /
    `parse_quotes` / `parse_sort_keys` so this loader can serve that builder
    too.

Path resolution: the repo root is derived from `Path(__file__).resolve()`
parents (this file lives at <repo>/graph/query/weirwood_query/load.py, so
`parents[3]` is <repo>), NOT from cwd — every path below is absolute,
independent of where the caller's process started.

Edge source of truth: `graph/edges/edges.jsonl` ONLY (G16). The legacy
`## Edges` markdown inside node bodies is display prose; `read_node_edges_
markdown` is provided for callers that want to print it (graph-query.py's
positional node-report mode), but `Edge` objects always come from edges.jsonl.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

from .model import Edge, Node

# ---------------------------------------------------------------------------
# Repo paths — derived from this file's location, not cwd.
# ---------------------------------------------------------------------------

_THIS_FILE = Path(__file__).resolve()
# <repo>/graph/query/weirwood_query/load.py -> parents[0]=weirwood_query,
# [1]=query, [2]=graph, [3]=<repo>
REPO_ROOT = _THIS_FILE.parents[3]

NODES_DIR = REPO_ROOT / "graph" / "nodes"
EDGES_FILE = REPO_ROOT / "graph" / "edges" / "edges.jsonl"
CROSS_REFS_FILE = REPO_ROOT / "working" / "wiki" / "data" / "cross-references.jsonl"

# Alias-table locations (absorbed from event_alias_resolver.py — paths
# UNCHANGED, this is a read path, not a relocation).
EVENT_ALIAS_LOOKUP_FILE = REPO_ROOT / "working" / "wiki" / "data" / "event-alias-lookup.json"
ALL_NODE_ALIAS_LOOKUP_FILE = REPO_ROOT / "working" / "wiki" / "data" / "all-node-alias-lookup.json"

# Legacy alias-resolver.json used by graph-query.py's node-inspection mode
# (a different, older, flatter alias map than the event/all-node lookups
# above — kept distinct, both are read-only inputs here).
LEGACY_ALIAS_RESOLVER_FILE = REPO_ROOT / "working" / "wiki" / "data" / "alias-resolver.json"


# ---------------------------------------------------------------------------
# Frontmatter parsing — pyyaml-with-fallback (graph-query.py's parser wins)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Extract YAML frontmatter and return (fields_dict, body_text).

    Tries pyyaml first for correctness; falls back to a hand-rolled scalar/
    list parser (`_simple_yaml_parse`) if pyyaml is unavailable or the block
    fails to parse. Absorbed verbatim from scripts/graph-query.py.
    """
    if not text.startswith("---"):
        return {}, text

    end = text.find("\n---", 3)
    if end == -1:
        return {}, text

    yaml_block = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")

    try:
        import yaml  # type: ignore

        try:
            fields = yaml.safe_load(yaml_block) or {}
        except Exception:
            fields = _simple_yaml_parse(yaml_block)
    except ImportError:
        fields = _simple_yaml_parse(yaml_block)

    return fields, body


def _simple_yaml_parse(yaml_text: str) -> dict[str, Any]:
    """Minimal YAML parser for node frontmatter (no nested dicts, just
    scalars and lists). Absorbed verbatim from scripts/graph-query.py."""
    result: dict[str, Any] = {}
    lines = yaml_text.splitlines()
    current_key: str | None = None
    current_list: list | None = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("- ") and current_key and current_list is not None:
            current_list.append(stripped[2:].strip().strip('"'))
            continue

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
# Node loading
# ---------------------------------------------------------------------------

def find_node_file(slug: str, nodes_dir: Path = NODES_DIR) -> Path | None:
    """Search all type subdirectories for <slug>.node.md. Return Path or None.

    Path-escape guard (S191): a slug containing a path separator or a `..`
    segment could make `type_dir / f"{slug}.node.md"` resolve OUTSIDE
    nodes_dir (pathlib walks `..` on .exists()). Deliberately NARROWER than
    traverse._is_valid_slug — 247 legacy on-disk slugs carry an uppercase
    timestamp suffix and must keep resolving; only path-dangerous input is
    rejected here."""
    if not isinstance(slug, str) or not slug or "/" in slug or "\\" in slug or ".." in slug:
        return None
    if not nodes_dir.exists():
        return None
    # Deterministic sorted walk + collision warning (S192 hardening): iterdir()
    # order is filesystem-dependent, so a cross-category dup slug used to
    # resolve to an ARBITRARY copy. Now every match is collected; a collision
    # warns on stderr and the alphabetically-first category wins, every run,
    # every machine.
    matches = []
    for type_dir in sorted(nodes_dir.iterdir()):
        if not type_dir.is_dir():
            continue
        candidate = type_dir / f"{slug}.node.md"
        if candidate.exists():
            matches.append(candidate)
    if len(matches) > 1:
        cats = ", ".join(m.parent.name for m in matches)
        print(
            f"WARNING: slug '{slug}' exists in multiple categories ({cats}); "
            f"returning {matches[0].parent.name}/ — resolve the duplicate.",
            file=sys.stderr,
        )
    return matches[0] if matches else None


def build_node_index(nodes_dir: Path = NODES_DIR) -> dict[str, Path]:
    """Return {slug: path} for every .node.md in the graph.

    Sorted walk + collision warning (S192 hardening, same rationale as
    find_node_file): on a cross-category dup slug the alphabetically-FIRST
    category wins deterministically and a warning goes to stderr — the engine
    keeps working (warn, don't die at query time; the builders are the
    fail-loud gate)."""
    index: dict[str, Path] = {}
    if not nodes_dir.exists():
        return index
    for type_dir in sorted(nodes_dir.iterdir()):
        if not type_dir.is_dir():
            continue
        for node_file in sorted(type_dir.glob("*.node.md")):
            slug = node_file.stem.replace(".node", "")
            if slug in index:
                print(
                    f"WARNING: slug '{slug}' exists in multiple categories "
                    f"({index[slug].parent.name}, {type_dir.name}); keeping "
                    f"{index[slug].parent.name}/ — resolve the duplicate.",
                    file=sys.stderr,
                )
                continue
            index[slug] = node_file
    return index


def load_node(slug: str, nodes_dir: Path = NODES_DIR) -> Node | None:
    """Load and parse a single node file by slug. Returns None if not found."""
    path = find_node_file(slug, nodes_dir)
    if path is None:
        return None
    return load_node_from_path(path)


def load_node_from_path(path: Path) -> Node:
    """Parse a node file at a known path into a Node."""
    text = path.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(text)
    fallback_slug = path.stem.replace(".node", "")
    return Node.from_frontmatter(fields, body, path, fallback_slug=fallback_slug)


def iter_all_nodes(nodes_dir: Path = NODES_DIR) -> Iterable[Node]:
    """Yield every Node in the graph (all category subdirectories)."""
    if not nodes_dir.exists():
        return
    for type_dir in sorted(nodes_dir.iterdir()):
        if not type_dir.is_dir():
            continue
        for node_file in sorted(type_dir.glob("*.node.md")):
            yield load_node_from_path(node_file)


# ---------------------------------------------------------------------------
# Edge loading — graph/edges/edges.jsonl is the ONLY edge source of truth (G16)
# ---------------------------------------------------------------------------

def load_edges(edges_path: Path = EDGES_FILE) -> list[dict[str, Any]]:
    """Load all edges from a JSONL file as plain dicts.

    Returns plain dicts (not Edge objects) by default to match the calling
    convention every absorbed traversal function (graph-query.py's cmd_*)
    already uses (`edges: list[dict]`, `.get("source_slug")`, ...). Use
    `load_edges_typed` for Edge dataclass instances.

    Raises FileNotFoundError with a clear message if the file is missing.
    """
    if not edges_path.exists():
        raise FileNotFoundError(
            f"edges.jsonl not found at {edges_path}. "
            "Run the Stage 4 pipeline first to produce this file."
        )
    rows: list[dict[str, Any]] = []
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


def load_edges_typed(edges_path: Path = EDGES_FILE) -> list[Edge]:
    """Like load_edges, but returns typed Edge dataclass instances."""
    return [Edge.from_dict(row) for row in load_edges(edges_path)]


# ---------------------------------------------------------------------------
# Node body sections — absorbed from scripts/build-chat-export.py
# ---------------------------------------------------------------------------

_CITE_RE = re.compile(r"`?(sources/chapters/[a-z0-9/_-]+?\.md:\d+)`?", re.I)


def split_sections(body: str) -> dict[str, str]:
    """Return {heading_lower: text} for `## Heading` sections in a node body."""
    sections: dict[str, str] = {}
    cur: str | None = None
    buf: list[str] = []
    for line in body.splitlines():
        h = re.match(r"^##\s+(.+?)\s*$", line)
        if h:
            if cur is not None:
                sections[cur] = "\n".join(buf).strip()
            cur = h.group(1).strip().lower()
            buf = []
        else:
            buf.append(line)
    if cur is not None:
        sections[cur] = "\n".join(buf).strip()
    return sections


def parse_quotes(quotes_text: str) -> list[dict[str, str | None]]:
    """Parse a `## Quotes` section body into [{text, attribution, cite}].

    A quote = one-or-more consecutive `> ` lines (joined), optionally followed
    by (or containing) an attribution line starting with `—` that may carry a
    `chapter:line` cite. Absorbed verbatim from scripts/build-chat-export.py.
    """
    if not quotes_text:
        return []
    quotes: list[dict[str, str | None]] = []
    lines = quotes_text.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        if lines[i].lstrip().startswith(">"):
            block = []
            while i < n and lines[i].lstrip().startswith(">"):
                block.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            attribution, cite = None, None
            attr_idx = next(
                (j for j in range(len(block) - 1, -1, -1)
                 if block[j].lstrip().startswith("—")),
                None,
            )
            if attr_idx is not None:
                attr_line = block[attr_idx]
                attribution = attr_line.strip().lstrip("—").strip()
                cm = _CITE_RE.search(attr_line)
                if cm:
                    cite = cm.group(1)
                block = block[:attr_idx]
            text = " ".join(s.strip() for s in block if s.strip()).strip()
            while i < n and not lines[i].strip():
                i += 1
            if attribution is None and i < n and lines[i].lstrip().startswith("—"):
                attribution = lines[i].strip().lstrip("—").strip()
                cm = _CITE_RE.search(lines[i])
                if cm:
                    cite = cm.group(1)
                i += 1
            if text:
                quotes.append({"text": text, "attribution": attribution, "cite": cite})
        else:
            i += 1
    return quotes


def parse_sort_keys(fm_text: str) -> tuple[str | None, str | None]:
    """Grab the chronological sort anchors from an event node's `sort_keys:`
    block. Returns (composite, reading_order). Absorbed verbatim from
    scripts/build-chat-export.py."""
    m = re.search(r"^sort_keys:\s*\n((?:[ \t]+\S.*\n?)+)", fm_text, re.MULTILINE)
    if not m:
        return None, None
    block = m.group(1)

    def grab(key: str) -> str | None:
        km = re.search(rf"^\s+{key}:\s*(.+?)\s*$", block, re.MULTILINE)
        if not km:
            return None
        v = km.group(1).strip()
        if v in ("null", "~", ""):
            return None
        if v[0] in "\"'" and v[-1] == v[0]:
            v = v[1:-1]
        return v or None

    return grab("composite"), grab("reading_order")


def read_node_edges_markdown(node: Node) -> str:
    """Return the raw `## Edges` section text from a node's body (display
    prose only — NOT the edge source of truth; see module docstring / G16)."""
    return split_sections(node.body).get("edges", "")


# ---------------------------------------------------------------------------
# Alias-table loading (read-only; building is build/build_alias_table.py)
# ---------------------------------------------------------------------------

def load_alias_lookup(path: Path = EVENT_ALIAS_LOOKUP_FILE) -> dict[str, str]:
    """Load the {normalized_phrase -> canonical_slug} table. Empty dict if
    the file doesn't exist (caller decides whether to trigger a build)."""
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return data.get("alias_to_canonical", {})


def load_alias_collisions(path: Path = EVENT_ALIAS_LOOKUP_FILE) -> dict[str, list[dict]]:
    """Load the {normalized_phrase -> [conflicting entries]} collision table."""
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return data.get("ambiguous_collisions", {})


def load_all_node_index(path: Path = ALL_NODE_ALIAS_LOOKUP_FILE) -> dict[str, list[dict]]:
    """Load the {normalized_phrase -> [{canonical_slug, node_category,
    node_type, source}]} all-node candidate index."""
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return data.get("phrase_to_nodes", {})


def load_legacy_alias_resolver(path: Path = LEGACY_ALIAS_RESOLVER_FILE) -> dict[str, str]:
    """Return the alias_to_canonical dict from the legacy alias-resolver.json
    (used by graph-query.py's node-inspection / edge-target-resolution path —
    distinct from the event/all-node lookup tables above)."""
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("alias_to_canonical", {})
    except (json.JSONDecodeError, KeyError):
        return {}


# ---------------------------------------------------------------------------
# Cross-reference loader (streaming) — absorbed from scripts/graph-query.py
# ---------------------------------------------------------------------------

def stream_inbound_refs(
    target_slug: str, limit: int = 20, path: Path = CROSS_REFS_FILE
) -> tuple[list[dict], int]:
    """Stream cross-references.jsonl and collect rows where target_slug
    matches. Returns (top_rows_up_to_limit, total_count)."""
    if not path.exists():
        return [], 0

    results: list[dict] = []
    total = 0

    with open(path, encoding="utf-8") as f:
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
