#!/usr/bin/env python3
"""
build-chat-export.py — Build the static data bundle for the Weirwood chat-UI alpha.

Reads the live graph (graph/nodes/, graph/edges/edges.jsonl) + the prebuilt alias
index, and writes an ALLOWLISTED set of compact JSON files into web/data/ (gitignored,
regenerated) that the Netlify Edge function loads at cold start. NO LLM, NO network.

The allowlist exists for bundle SIZE, not for any publish concern (the repo is private;
book text bundles fine) — in particular we NEVER ship the 1.8 GB graph/edges/ backup
directory, only the single edges.jsonl.

Outputs (web/data/):
  alias-map.json      {phrase: [{slug, category}]}            — resolve(phrase) -> slugs
  nodes.json          {slug: {name, type, identity, quotes}}  — read_node(slug)
  edges.json          [{edge_type, source, target, quote, ref, tier, relation}] — walk_chain / neighbors
  manifest.json       {built_at?, counts, sizes}              — provenance / sanity

Usage:
  python3 scripts/build-chat-export.py                 # build everything
  python3 scripts/build-chat-export.py --built-at ISO  # stamp manifest (optional)

Design: working/chat-ui/alpha-design.md §8 (Foundation chunk, Session 171).
"""

import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NODES_DIR = REPO / "graph/nodes"
EDGES_FILE = REPO / "graph/edges/edges.jsonl"
ALIAS_LOOKUP = REPO / "working/wiki/data/all-node-alias-lookup.json"
OUT_DIR = REPO / "web/data"

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

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
# A cite token: `sources/chapters/<book>/<file>.md:NNN`. Backticks optional — the
# book-cite overlay wrote some attributions bare (`— sources/…:25 · gloss`) and some
# backtick-wrapped (`… (\`sources/…:119\`)`); match both so neither leaks into .text.
CITE_RE = re.compile(r"`?(sources/chapters/[a-z0-9/_-]+?\.md:\d+)`?", re.I)


def parse_frontmatter_scalar(fm_text, key):
    """Tiny YAML-ish scalar grab for name/type/slug (avoids a yaml dep)."""
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", fm_text, re.MULTILINE)
    if not m:
        return None
    val = m.group(1).strip()
    if val and val[0] in "\"'" and val[-1] == val[0]:
        val = val[1:-1]
    return val


def parse_sort_keys(fm_text):
    """Grab the chronological sort anchors from an event node's `sort_keys:` block
    (built by scripts/build-event-sort-keys.py). Returns (composite, reading_order),
    each a string or None. Scoped to the block so we never pick up a stray key
    elsewhere in the frontmatter. Only event nodes carry this block."""
    m = re.search(r"^sort_keys:\s*\n((?:[ \t]+\S.*\n?)+)", fm_text, re.MULTILINE)
    if not m:
        return None, None
    block = m.group(1)

    def grab(key):
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


def split_sections(body):
    """Return {heading_lower: text} for `## Heading` sections."""
    sections = {}
    cur = None
    buf = []
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


def parse_quotes(quotes_text):
    """Parse the `## Quotes` block into [{text, attribution, cite}].

    A quote = one-or-more consecutive `> ` lines (joined), optionally followed by
    an attribution line starting with `—` that may carry a `chapter:line` cite.
    """
    if not quotes_text:
        return []
    quotes = []
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
            # The attribution line (leading —) may sit INSIDE the > block
            # (`> — sources/…`) — the common book-cite-overlay shape. Peel the
            # trailing —-line out so its cite + gloss never collapse into .text.
            attr_idx = next(
                (j for j in range(len(block) - 1, -1, -1)
                 if block[j].lstrip().startswith("—")),
                None,
            )
            if attr_idx is not None:
                attr_line = block[attr_idx]
                attribution = attr_line.strip().lstrip("—").strip()
                cm = CITE_RE.search(attr_line)
                if cm:
                    cite = cm.group(1)
                block = block[:attr_idx]
            text = " ".join(s.strip() for s in block if s.strip()).strip()
            # skip blank lines, then look for an attribution line OUTSIDE the
            # block (the legacy shape: a bare —-line after the quote).
            while i < n and not lines[i].strip():
                i += 1
            if attribution is None and i < n and lines[i].lstrip().startswith("—"):
                attribution = lines[i].strip().lstrip("—").strip()
                cm = CITE_RE.search(lines[i])
                if cm:
                    cite = cm.group(1)
                i += 1
            if text:
                quotes.append({"text": text, "attribution": attribution, "cite": cite})
        else:
            i += 1
    return quotes


def load_nodes():
    """slug -> {name, type, identity, quotes}. Slim: drop the heavy ## Edges prose."""
    nodes = {}
    for path in sorted(NODES_DIR.rglob("*.node.md")):
        raw = path.read_text(encoding="utf-8")
        fm_m = FRONTMATTER_RE.match(raw)
        if not fm_m:
            continue
        fm = fm_m.group(1)
        body = raw[fm_m.end():]
        slug = parse_frontmatter_scalar(fm, "slug") or path.name.replace(".node.md", "")
        name = parse_frontmatter_scalar(fm, "name") or slug
        ntype = parse_frontmatter_scalar(fm, "type") or ""
        sections = split_sections(body)
        identity = sections.get("identity", "")
        # Strip inline markdown link syntax [text](slug) -> text for clean prose.
        identity = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", identity).strip()
        quotes = parse_quotes(sections.get("quotes", ""))
        rec = {
            "name": name,
            "type": ntype,
            "identity": identity,
            "quotes": quotes,
        }
        # Chronological sort anchors (event nodes only). Carried onto the node so
        # walkChain() can order a causal chain by story-time instead of graph hop-
        # depth (S185). Only emitted when present — keeps the bundle small and
        # non-event nodes clean.
        composite, reading_order = parse_sort_keys(fm)
        if composite is not None:
            rec["composite"] = composite
        if reading_order is not None:
            rec["reading_order"] = reading_order
        nodes[slug] = rec
    return nodes


def load_edges():
    edges = []
    with EDGES_FILE.open(encoding="utf-8") as f:
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


def build_alias_map():
    """phrase -> [{slug, category}] from the prebuilt all-node-alias index."""
    data = json.loads(ALIAS_LOOKUP.read_text(encoding="utf-8"))
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
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Building chat export -> {OUT_DIR.relative_to(REPO)}/")

    print("  · parsing nodes ...")
    nodes = load_nodes()
    print("  · parsing edges ...")
    edges = load_edges()
    print("  · building alias map ...")
    alias_map = build_alias_map()

    sizes = {}
    sizes["nodes.json"] = write_json(OUT_DIR / "nodes.json", nodes)
    sizes["edges.json"] = write_json(OUT_DIR / "edges.json", edges)
    sizes["alias-map.json"] = write_json(OUT_DIR / "alias-map.json", alias_map)

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
    sizes["manifest.json"] = write_json(OUT_DIR / "manifest.json", manifest)

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
