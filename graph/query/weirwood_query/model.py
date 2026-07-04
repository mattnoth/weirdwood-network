"""model.py — Node / Edge dataclasses for the Weirwood query engine.

Provenance: new module (query-layer Track, step 1, S189). The canonical field
set is derived from live sampling of `graph/edges/edges.jsonl` and from the
frontmatter fields `scripts/graph-query.py` and `scripts/event_alias_resolver.py`
already read. Nothing here changes on-disk data shape — these are typed VIEWS
over the existing JSONL/markdown-frontmatter records.

Both dataclasses are permissive: `Edge` and `Node` keep an `extra` dict for any
field present on disk that isn't promoted to a named attribute, so no data is
silently dropped by round-tripping through these types. Most call sites in the
absorbed scripts operate on plain dicts (`edges: list[dict]`), so `Edge`/`Node`
provide `.to_dict()` / `.from_dict()` for interop without forcing a rewrite of
every traversal function to dataclass-only access.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Edge
# ---------------------------------------------------------------------------

# The ~9-field canonical set every consumer (graph-query.py, event_alias_
# resolver.py, build-chat-export.py) actually reads off an edges.jsonl row.
# Everything else present on disk (decision, evidence_kind, typed_by,
# dup_count, run_id, schema_version, produced_at, source_set, qualifier,
# superseded_by, ...) is provenance/pipeline bookkeeping — preserved in
# `extra`, not promoted here.
_EDGE_CORE_FIELDS = (
    "edge_type",
    "source_slug",
    "target_slug",
    "confidence_tier",
    "evidence_ref",
    "evidence_quote",
    "evidence_book",
    "evidence_chapter",
    "asserted_relation",
)


@dataclass
class Edge:
    """One row of graph/edges/edges.jsonl.

    `edge_type` / `source_slug` / `target_slug` are the traversal-critical
    fields every mode in graph-query.py keys off. `extra` retains every other
    on-disk field (decision, evidence_kind, dup_count, run_id, ...) so
    round-tripping through Edge never loses data the pipeline needs.
    """

    edge_type: str
    source_slug: str
    target_slug: str
    confidence_tier: int | None = None
    evidence_ref: str | None = None
    evidence_quote: str | None = None
    evidence_book: str | None = None
    evidence_chapter: str | None = None
    asserted_relation: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, row: dict[str, Any]) -> "Edge":
        core = {k: row.get(k) for k in _EDGE_CORE_FIELDS}
        extra = {k: v for k, v in row.items() if k not in _EDGE_CORE_FIELDS}
        return cls(**core, extra=extra)

    def to_dict(self) -> dict[str, Any]:
        """Round-trip back to a plain dict, core fields first (matches the
        shape traversal functions ported from graph-query.py expect: a dict
        with .get('source_slug') etc.)."""
        out = {k: getattr(self, k) for k in _EDGE_CORE_FIELDS}
        out.update(self.extra)
        return out


# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------

@dataclass
class Node:
    """A parsed graph/nodes/**/*.node.md file: frontmatter fields + body text.

    `body` is the raw markdown after the frontmatter block — callers that want
    the legacy `## Edges` prose (display-only; edges.jsonl is the source of
    truth, see G16) or other sections (`## Identity`, `## Quotes`, `## Narrative
    Arc`) parse `body` themselves (see load.py's section splitter, absorbed
    from build-chat-export.py).
    """

    slug: str
    name: str
    type: str
    file_path: Path
    aliases: list[str] = field(default_factory=list)
    containers: list[str] = field(default_factory=list)
    body: str = ""
    frontmatter: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_frontmatter(
        cls,
        fields: dict[str, Any],
        body: str,
        file_path: Path,
        *,
        fallback_slug: str,
    ) -> "Node":
        aliases_raw = fields.get("aliases", [])
        if not isinstance(aliases_raw, list):
            aliases_raw = [aliases_raw] if aliases_raw else []
        containers_raw = fields.get("containers", [])
        if not isinstance(containers_raw, list):
            containers_raw = [containers_raw] if containers_raw else []
        return cls(
            slug=fields.get("slug") or fallback_slug,
            name=fields.get("name", ""),
            type=fields.get("type", ""),
            file_path=file_path,
            aliases=[str(a) for a in aliases_raw],
            containers=[str(c) for c in containers_raw],
            body=body,
            frontmatter=fields,
        )
