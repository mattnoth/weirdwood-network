"""list_nodes.py — trivial browse surface over graph/nodes/ (query-layer
Track, step 5d; design.md G6 "no browse surface").

Named `list_nodes` (not `list`, a Python builtin) at the module level; the
CLI subcommand and the TS twin are both still called `list` per the design
doc's contract (`weirwood query list --type foods`, `listNodes()` in TS) —
only this module's file/function name avoids shadowing the builtin.

Purpose: "list every node of type X" (optionally filtered by whether it
carries any curated quotes), paged. Companion to `search` — once search
finds a topic, `list` answers "what ELSE exists in this category" (a browse
axis search doesn't cover: it needs query terms, list needs none).

Filters:
  - `category` — the graph/nodes/ type-directory name (e.g. "foods") — same
    vocabulary as `search`'s `--type`/`node_type` (see build_search_index.py's
    comment on category vs. the frontmatter `type:` scalar). Required (no
    "list everything across all 8,727 nodes" mode — that's what `--health`'s
    node_count is for; a categoryless list has no useful ordering).
  - `has_quotes` — keep only nodes whose `## Quotes` section parsed at least
    one quote (a proxy for "this node has curated book content", the same
    thing the search index's substrate depends on).
  - `container` — keep only nodes whose `containers:` frontmatter array
    contains this name (reuses `traverse._node_containers`'s parsing — the
    same bag-retrieval semantics as the `container` op, scoped to one
    category instead of the whole graph).
  - `limit` / `offset` — simple pagination over the deterministic sort order
    (slug ascending — stable across runs, independent of filesystem mtime).

No LLM in the loop. Ever.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .load import NODES_DIR, parse_frontmatter, parse_quotes, split_sections
from .traverse import _node_containers

DEFAULT_LIMIT = 50


def list_nodes(
    category: str,
    *,
    has_quotes: bool = False,
    container: str | None = None,
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
    nodes_dir: Path = NODES_DIR,
) -> dict[str, Any]:
    """Return `{category, total, offset, limit, items: [{slug, name, quote_count}]}`
    for every node under `graph/nodes/<category>/`, sorted by slug.

    `total` is the count AFTER filtering (has_quotes/container), BEFORE
    paging — so a caller can tell "there are 37 more" from
    `total - offset - len(items)`. An unknown category (no such directory)
    returns `total: 0, items: []`, not an error — mirrors container()'s
    "no matches" convention rather than raising, since a category typo is a
    query mistake, not a system fault.
    """
    type_dir = nodes_dir / category
    items: list[dict[str, Any]] = []
    container_target = container.strip().lower() if container else None

    if type_dir.is_dir():
        for node_file in sorted(type_dir.glob("*.node.md")):
            raw = node_file.read_text(encoding="utf-8")
            fields, body = parse_frontmatter(raw)
            fallback = node_file.name.replace(".node.md", "")
            slug = fields.get("slug") or fallback
            name = fields.get("name") or slug

            if container_target is not None:
                containers = [c.lower() for c in _node_containers(fields)]
                if container_target not in containers:
                    continue

            sections = split_sections(body)
            quotes = parse_quotes(sections.get("quotes", ""))
            if has_quotes and not quotes:
                continue
            items.append({
                "slug": slug,
                "name": str(name),
                "quote_count": len(quotes),
            })

    items.sort(key=lambda it: it["slug"])
    total = len(items)
    page = items[offset:offset + limit]

    return {
        "category": category,
        "total": total,
        "offset": offset,
        "limit": limit,
        "items": page,
    }
