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
  featured-tywin.json {question, chain[], beats[], closing}   — pre-rendered landing exchange
  manifest.json       {built_at?, counts, sizes}              — provenance / sanity

Usage:
  python3 scripts/build-chat-export.py                 # build everything
  python3 scripts/build-chat-export.py --built-at ISO  # stamp manifest (optional)

Design: working/chat-ui/alpha-design.md §8 (Foundation chunk, Session 171).
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NODES_DIR = REPO / "graph/nodes"
EDGES_FILE = REPO / "graph/edges/edges.jsonl"
ALIAS_LOOKUP = REPO / "working/wiki/data/all-node-alias-lookup.json"
GRAPH_QUERY = REPO / "scripts/graph-query.py"
OUT_DIR = REPO / "web/data"

FEATURED_SLUG = "assassination-of-tywin-lannister"

# Causal edge types that form a "chain walked" (must match graph-query --causal-chain).
CAUSAL_TYPES = {"CAUSES", "TRIGGERS", "MOTIVATES"}

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
# A cite token: `sources/chapters/<book>/<file>.md:NNN`  (also tolerate plain wiki refs)
CITE_RE = re.compile(r"`(sources/chapters/[^`]+?:\d+)`")


def parse_frontmatter_scalar(fm_text, key):
    """Tiny YAML-ish scalar grab for name/type/slug (avoids a yaml dep)."""
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", fm_text, re.MULTILINE)
    if not m:
        return None
    val = m.group(1).strip()
    if val and val[0] in "\"'" and val[-1] == val[0]:
        val = val[1:-1]
    return val


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
            text = " ".join(s.strip() for s in block if s.strip()).strip()
            # skip blank lines, then look for an attribution line
            while i < n and not lines[i].strip():
                i += 1
            attribution, cite = None, None
            if i < n and lines[i].lstrip().startswith("—"):
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
        nodes[slug] = {
            "name": name,
            "type": ntype,
            "identity": identity,
            "quotes": quotes,
        }
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


def build_featured(nodes):
    """Pre-render the Tywin landing exchange from graph-query --causal-chain --json.

    Produces the typed-edge chain (oldest cause -> the assassination) plus, for each
    beat node, its name + quotes, so the page can render a static transcript with
    real receipts without a live API call.
    """
    res = subprocess.run(
        [sys.executable, str(GRAPH_QUERY), "--causal-chain", FEATURED_SLUG, "--json"],
        capture_output=True, text=True, cwd=str(REPO),
    )
    if res.returncode != 0:
        print(f"  ! graph-query failed for {FEATURED_SLUG}:\n{res.stderr}", file=sys.stderr)
        return None
    chain = json.loads(res.stdout)

    def node_name(slug):
        return nodes.get(slug, {}).get("name", slug)

    # upstream is returned deepest-first; reverse to read oldest-cause -> assassination.
    upstream = list(reversed(chain.get("upstream", [])))
    links = []
    beat_slugs = []
    for link in upstream:
        s, t = link["source_slug"], link["target_slug"]
        links.append({
            "source": s, "source_name": node_name(s),
            "edge_type": link["edge_type"],
            "target": t, "target_name": node_name(t),
            "evidence_quote": link.get("evidence_quote"),
            "evidence_ref": link.get("evidence_ref"),
            "tier": link.get("confidence_tier"),
        })
        for sl in (s, t):
            if sl not in beat_slugs:
                beat_slugs.append(sl)

    beats = []
    for sl in beat_slugs:
        nd = nodes.get(sl, {})
        beats.append({
            "slug": sl,
            "name": nd.get("name", sl),
            "type": nd.get("type", ""),
            "quotes": nd.get("quotes", []),
        })

    # The landing one-liner: prefer the famous closing quote on the target node.
    closing = None
    for q in nodes.get(FEATURED_SLUG, {}).get("quotes", []):
        if "shit gold" in q["text"].lower():
            closing = q
            break

    return {
        "slug": FEATURED_SLUG,
        "question": "Who killed Tywin Lannister, and why?",
        "title": node_name(FEATURED_SLUG),
        "chain": links,
        "beats": beats,
        "closing": closing,
    }


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
    print("  · pre-rendering featured Tywin exchange ...")
    featured = build_featured(nodes)

    sizes = {}
    sizes["nodes.json"] = write_json(OUT_DIR / "nodes.json", nodes)
    sizes["edges.json"] = write_json(OUT_DIR / "edges.json", edges)
    sizes["alias-map.json"] = write_json(OUT_DIR / "alias-map.json", alias_map)
    if featured:
        sizes["featured-tywin.json"] = write_json(OUT_DIR / "featured-tywin.json", featured)

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
            "featured_chain_links": len(featured["chain"]) if featured else 0,
        },
        "sizes_bytes": sizes,
    }
    sizes["manifest.json"] = write_json(OUT_DIR / "manifest.json", manifest)

    print("\nBUILD COMPLETE")
    print(f"  nodes={len(nodes)}  (with quotes={nodes_with_quotes}, quotes={quotes_total})")
    print(f"  edges={len(edges)}  alias_phrases={len(alias_map)}")
    if featured:
        print(f"  featured chain links={len(featured['chain'])}  beats={len(featured['beats'])}")
        if featured.get("closing"):
            print(f"  featured closing: \"{featured['closing']['text'][:60]}...\"")
    print("\nFile sizes:")
    total = 0
    for fn, sz in sizes.items():
        total += sz
        print(f"  {fn:24s} {human(sz):>10s}")
    print(f"  {'TOTAL':24s} {human(total):>10s}")


if __name__ == "__main__":
    main()
