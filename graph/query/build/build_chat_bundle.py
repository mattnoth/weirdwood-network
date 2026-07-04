#!/usr/bin/env python3
"""build_chat_bundle.py — Build the static data bundle for the Weirwood chat-UI alpha.

Absorbs scripts/build-chat-export.py (query-layer Track, step 1, S189/S190). Reads
the live graph (graph/nodes/, graph/edges/edges.jsonl) + the prebuilt alias index,
and writes an ALLOWLISTED set of compact JSON files into web/data/ (gitignored,
regenerated) that the Netlify Edge function loads at cold start. NO LLM, NO network.

The allowlist exists for bundle SIZE, not for any publish concern (the repo is private;
book text bundles fine) — in particular we NEVER ship the 1.8 GB graph/edges/ backup
directory, only the single edges.jsonl.

Outputs (web/data/ by default; override with --out-dir for verification runs):
  alias-map.json      {phrase: [{slug, category}]}            — resolve(phrase) -> slugs
  nodes.json          {slug: {name, type, category, identity, quotes}} — read_node(slug) / listNodes()
  edges.json          [{edge_type, source, target, quote, ref, tier, relation}] — walk_chain / neighbors
  search-index.json   compact BM25 inverted index (query-layer step 5a) — searchQuotes(query)
                       BUILT BY build/build_search_index.py, not this module — this module only
                       measures it into the manifest (see `_search_index_size` below); the two
                       builders write independently, `weirwood refresh` runs both.
  manifest.json       {built_at?, counts, sizes}              — provenance / sanity

Usage:
  python3 graph/query/build/build_chat_bundle.py                 # build everything
  python3 graph/query/build/build_chat_bundle.py --built-at ISO   # stamp manifest (optional)
  python3 graph/query/build/build_chat_bundle.py --out-dir DIR    # write elsewhere (verification)

Parser provenance (ZERO OUTPUT CHANGE — query-layer Track, step 1): this module
reuses `weirwood_query.load`'s `split_sections` / `parse_quotes` / `parse_sort_keys`
(already absorbed verbatim from build-chat-export.py in that module) and its
pyyaml-with-fallback `parse_frontmatter` for frontmatter, IN PLACE of the old
script's own hand-rolled `parse_frontmatter_scalar` regex grab. This is safe, not
a parity risk: verified by running both parsers over all 8,727 live node files and
diffing the extracted `name`/`type`/`slug` scalars — zero mismatches. (Contrast
with `build/build_alias_table.py`, which deliberately keeps ITS OWN regex parser
because that case has 5 known-differing files — no such case exists here.)

Design: working/chat-ui/alpha-design.md §8 (Foundation chunk, Session 171);
working/query-layer/design.md step 1 (move to graph/query/build/).

No LLM in the loop. Ever.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_THIS_FILE = Path(__file__).resolve()
# <repo>/graph/query/build/build_chat_bundle.py -> parents[0]=build,
# [1]=query, [2]=graph, [3]=<repo>
REPO_ROOT = _THIS_FILE.parents[3]

sys.path.insert(0, str(REPO_ROOT / "graph" / "query"))

from weirwood_query.load import (  # noqa: E402
    parse_frontmatter,
    parse_quotes,
    parse_sort_keys,
    split_sections,
)

NODES_DIR = REPO_ROOT / "graph/nodes"
EDGES_FILE = REPO_ROOT / "graph/edges/edges.jsonl"
ALIAS_LOOKUP = REPO_ROOT / "working/wiki/data/all-node-alias-lookup.json"
OUT_DIR = REPO_ROOT / "web/data"


# Edge fields we keep in the slim export (drop provenance noise).
# Renamed on the wire to short keys to shrink the bundle.
def slim_edge(e):
    return {
        "type": e.get("edge_type"),
        "source": e.get("source_slug"),
        "target": e.get("target_slug"),
        "quote": e.get("evidence_quote") or None,
        "ref": e.get("evidence_ref") or None,
        "tier": e.get("confidence_tier"),
        "relation": e.get("asserted_relation") or None,
    }


# --- node .md parsing -------------------------------------------------------
# (frontmatter/section/quote/sort-key parsing delegated to weirwood_query.load —
# see module docstring for the parity verification that makes this safe.)


def load_nodes(nodes_dir: Path = NODES_DIR):
    """slug -> {name, type, category, identity, quotes}. Slim: drop the heavy
    ## Edges prose.

    `category` (query-layer step 5d, added for listNodes()'s --type filter):
    the graph/nodes/ TYPE-DIRECTORY name (e.g. "foods") — path.parent.name,
    always exactly one level under nodes_dir (verified: no node file nests
    deeper). DIFFERENT from `type` (the frontmatter `type:` scalar, e.g.
    "object.food" — see build_search_index.py's own comment on why the two
    vocabularies aren't 1:1: 5 of 41 frontmatter types map to >1 directory,
    e.g. concept.custom -> customs/concepts, event.war -> events/characters).
    """
    import re

    nodes = {}
    for path in sorted(nodes_dir.rglob("*.node.md")):
        raw = path.read_text(encoding="utf-8")
        fields, body = parse_frontmatter(raw)
        if not fields and not raw.startswith("---"):
            continue
        fallback = path.name.replace(".node.md", "")
        slug = fields.get("slug") or fallback
        name = fields.get("name") or slug
        ntype = fields.get("type") or ""
        category = path.parent.name
        sections = split_sections(body)
        identity = sections.get("identity", "")
        # Strip inline markdown link syntax [text](slug) -> text for clean prose.
        identity = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", identity).strip()
        quotes = parse_quotes(sections.get("quotes", ""))
        rec = {
            "name": str(name),
            "type": str(ntype),
            "category": category,
            "identity": identity,
            "quotes": quotes,
        }
        # Chronological sort anchors (event nodes only). Carried onto the node so
        # walkChain() can order a causal chain by story-time instead of graph hop-
        # depth (S185). Only emitted when present — keeps the bundle small and
        # non-event nodes clean. parse_sort_keys reads the RAW frontmatter text
        # (its own scoped regex over the `sort_keys:` block), so re-slice it here
        # rather than from the parsed `fields` dict.
        fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", raw, re.DOTALL)
        fm_text = fm_match.group(1) if fm_match else ""
        composite, reading_order = parse_sort_keys(fm_text)
        if composite is not None:
            rec["composite"] = composite
        if reading_order is not None:
            rec["reading_order"] = reading_order
        nodes[slug] = rec
    return nodes


def load_edges(edges_file: Path = EDGES_FILE):
    edges = []
    with edges_file.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            if e.get("decision") and e.get("decision") != "emit_edge":
                continue
            if not e.get("source_slug") or not e.get("target_slug"):
                continue
            edges.append(slim_edge(e))
    return edges


def build_alias_map(alias_lookup: Path = ALIAS_LOOKUP):
    """phrase -> [{slug, category}] from the prebuilt all-node-alias index."""
    data = json.loads(alias_lookup.read_text(encoding="utf-8"))
    p2n = data.get("phrase_to_nodes", {})
    out = {}
    for phrase, cands in p2n.items():
        slim = []
        seen = set()
        for c in cands:
            slug = c.get("canonical_slug")
            if not slug or slug in seen:
                continue
            seen.add(slug)
            slim.append({"slug": slug, "category": c.get("node_category") or ""})
        if slim:
            out[phrase] = slim
    return out


def write_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return path.stat().st_size


def human(nbytes):
    for unit in ("B", "KB", "MB"):
        if nbytes < 1024 or unit == "MB":
            return f"{nbytes:.1f}{unit}" if unit != "B" else f"{nbytes}B"
        nbytes /= 1024


def main():
    ap = argparse.ArgumentParser(description="Build the chat-UI static data bundle.")
    ap.add_argument("--built-at", default=None, help="ISO timestamp to stamp into manifest.json")
    ap.add_argument(
        "--out-dir",
        default=None,
        help="Override output directory (default: web/data/). Used by verification runs "
        "that must not touch the live bundle.",
    )
    args = ap.parse_args()

    out_dir = Path(args.out_dir) if args.out_dir else OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Building chat export -> {out_dir}/")

    print("  · parsing nodes ...")
    nodes = load_nodes()
    print("  · parsing edges ...")
    edges = load_edges()
    print("  · building alias map ...")
    alias_map = build_alias_map()

    sizes = {}
    sizes["nodes.json"] = write_json(out_dir / "nodes.json", nodes)
    sizes["edges.json"] = write_json(out_dir / "edges.json", edges)
    sizes["alias-map.json"] = write_json(out_dir / "alias-map.json", alias_map)

    # search-index.json is built by build/build_search_index.py, a separate
    # builder (query-layer step 5a) — this module does NOT regenerate it, it
    # only measures whatever copy is already on disk into the manifest, so a
    # caller that forgets to run build_search_index.py first sees a manifest
    # gap (0 / absent) rather than a silently stale-but-present number.
    search_index_path = out_dir / "search-index.json"
    if search_index_path.exists():
        sizes["search-index.json"] = search_index_path.stat().st_size

    # theme-index.json — same "measure, don't regenerate" pattern (query-layer
    # step 8a's build/build_theme_index.py is the separate builder).
    theme_index_path = out_dir / "theme-index.json"
    if theme_index_path.exists():
        sizes["theme-index.json"] = theme_index_path.stat().st_size

    quotes_total = sum(len(n["quotes"]) for n in nodes.values())
    nodes_with_quotes = sum(1 for n in nodes.values() if n["quotes"])
    manifest = {
        "built_at": args.built_at,
        "counts": {
            "nodes": len(nodes),
            "nodes_with_quotes": nodes_with_quotes,
            "quotes_total": quotes_total,
            "edges": len(edges),
            "alias_phrases": len(alias_map),
        },
        "sizes_bytes": sizes,
    }
    sizes["manifest.json"] = write_json(out_dir / "manifest.json", manifest)

    print("\nBUILD COMPLETE")
    print(f"  nodes={len(nodes)}  (with quotes={nodes_with_quotes}, quotes={quotes_total})")
    print(f"  edges={len(edges)}  alias_phrases={len(alias_map)}")
    print("\nFile sizes:")
    total = 0
    for fn, sz in sizes.items():
        total += sz
        print(f"  {fn:24s} {human(sz):>10s}")
    print(f"  {'TOTAL':24s} {human(total):>10s}")


if __name__ == "__main__":
    main()
