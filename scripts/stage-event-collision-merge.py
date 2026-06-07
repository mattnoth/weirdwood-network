"""
stage-event-collision-merge.py

Reads working/edge-modeling/event-node-reuse-lookup.json, finds every
normalized key that maps to more than one event-node slug (collision groups),
and produces merge candidates for human review.

For each collision group:
  - Reads the involved graph/nodes/events/<slug>.node.md files
  - Proposes a CANONICAL slug (highest-confidence, richer content)
  - Lists edges in graph/edges/edges.jsonl that would need re-pointing
  - Assigns confidence (high / medium / low) + rationale
  - Low-confidence groups go to a "needs human judgment" list

Outputs:
  working/edge-modeling/collision-merge-candidates.jsonl
  working/edge-modeling/collision-merge-summary.md

READ-ONLY on graph/ -- produces staging candidates only.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
LOOKUP_PATH = REPO_ROOT / "working" / "edge-modeling" / "event-node-reuse-lookup.json"
NODES_DIR   = REPO_ROOT / "graph" / "nodes" / "events"
EDGES_FILE  = REPO_ROOT / "graph" / "edges" / "edges.jsonl"
OUT_JSONL   = REPO_ROOT / "working" / "edge-modeling" / "collision-merge-candidates.jsonl"
OUT_MD      = REPO_ROOT / "working" / "edge-modeling" / "collision-merge-summary.md"


# ── YAML frontmatter helpers ──────────────────────────────────────────────────

def parse_frontmatter(text: str) -> dict:
    """Extract simple key:value pairs from YAML frontmatter block."""
    fm = {}
    if not text.startswith("---"):
        return fm
    end = text.find("\n---", 3)
    if end == -1:
        return fm
    block = text[3:end].strip()
    for line in block.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"')
    return fm


def body_after_frontmatter(text: str) -> str:
    """Return everything after the closing --- of the frontmatter."""
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    return text[end + 4:].strip()


def count_edge_bullets(body: str) -> int:
    """Count lines in the Edges section that start with '- '."""
    in_edges = False
    count = 0
    for line in body.splitlines():
        if re.match(r"^## Edges", line):
            in_edges = True
            continue
        if in_edges and line.startswith("## "):
            break
        if in_edges and line.startswith("- "):
            count += 1
    return count


def read_node(slug: str) -> dict:
    """Read a node file and return a dict with metadata useful for merge decisions."""
    path = NODES_DIR / f"{slug}.node.md"
    if not path.exists():
        return {"slug": slug, "exists": False}

    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    body = body_after_frontmatter(text)

    # Is this node itself a redirect/alias?
    is_redirect = (
        "redirect" in body.lower()[:200]
        or "same_as" in fm
        or "alias" in body.lower()[:200]
    )

    return {
        "slug": slug,
        "exists": True,
        "name": fm.get("name", ""),
        "type": fm.get("type", ""),
        "confidence": fm.get("confidence", ""),
        "wiki_source": fm.get("wiki_source", ""),
        "pass_origin": fm.get("pass_origin", ""),
        "prompt_version": fm.get("prompt_version", ""),
        "bucket_id": fm.get("bucket_id", ""),
        "same_as": fm.get("same_as", ""),
        "is_redirect": is_redirect,
        "body_length": len(body),
        "edge_bullet_count": count_edge_bullets(body),
        "body_preview": body[:120].replace("\n", " "),
    }


# ── Collision group extraction ────────────────────────────────────────────────

def find_collision_groups(lookup: dict) -> list[dict]:
    """
    Return distinct collision groups: each is a list of 2+ slugs that share
    a normalized collision key.  De-duplicate so each frozenset appears once.
    """
    seen = {}
    for key, val in lookup.items():
        if not isinstance(val, list):
            continue
        frozen = frozenset(val)
        if frozen not in seen:
            seen[frozen] = {"slugs": sorted(val), "collision_keys": []}
        seen[frozen]["collision_keys"].append(key)
    return list(seen.values())


# ── Canonical selection logic ─────────────────────────────────────────────────

def select_canonical(nodes: list[dict]) -> tuple[str, str, str]:
    """
    Given a list of node dicts (for one collision group), pick the canonical
    slug and return (canonical_slug, confidence, rationale).

    Priority rules (applied in order, first decisive rule wins):
    1. Node already has same_as pointing to another slug in the group →
       the target of same_as is canonical (the ingestion pipeline already
       decided; high confidence).
    2. Exactly one node is NOT a redirect (richer content) →
       that node is canonical (high confidence).
    3. Node with pass_origin=pass2-wiki-deterministic (Python-minted, richer)
       over pass2-wiki (LLM-minted) → that node is canonical (high confidence).
    4. Node with more edge bullets → canonical (medium confidence).
    5. Node with longer body → canonical (medium confidence).
    6. Otherwise → low confidence, needs human judgment.
    """
    slug_map = {n["slug"]: n for n in nodes}

    # Rule 1: explicit same_as pointers
    pointers = {}
    for n in nodes:
        if n.get("same_as") and n["same_as"] in slug_map:
            pointers[n["slug"]] = n["same_as"]
    if pointers:
        # All pointers should converge to the same target
        targets = set(pointers.values())
        if len(targets) == 1:
            canonical = targets.pop()
            redirect_slugs = [s for s in pointers]
            rationale = (
                f"Node(s) {redirect_slugs} carry same_as: {canonical!r} in "
                f"their frontmatter, indicating the ingestion pipeline already "
                f"resolved this as a wiki-redirect pair."
            )
            return canonical, "high", rationale
        else:
            # Conflicting pointers — shouldn't happen but flag it
            rationale = (
                f"Conflicting same_as pointers found: {pointers}. "
                f"Human review required."
            )
            return nodes[0]["slug"], "low", rationale

    # Rule 2: only one non-redirect node
    non_redirects = [n for n in nodes if not n["is_redirect"]]
    if len(non_redirects) == 1:
        canonical = non_redirects[0]["slug"]
        redirect_names = [n["slug"] for n in nodes if n["slug"] != canonical]
        rationale = (
            f"Only {canonical!r} has substantive content; "
            f"{redirect_names} appear to be stub/redirect nodes."
        )
        return canonical, "high", rationale

    if len(non_redirects) == 0:
        rationale = "All nodes appear to be redirects/stubs. Cannot auto-resolve canonical."
        return nodes[0]["slug"], "low", rationale

    # Rule 3: pass_origin tie-breaker (deterministic > LLM)
    deterministic = [n for n in non_redirects if "deterministic" in n.get("pass_origin", "")]
    if len(deterministic) == 1:
        canonical = deterministic[0]["slug"]
        others = [n["slug"] for n in non_redirects if n["slug"] != canonical]
        rationale = (
            f"{canonical!r} was minted by the deterministic Python pass "
            f"(pass_origin={deterministic[0]['pass_origin']!r}), giving it "
            f"higher provenance confidence over {others} (LLM-minted)."
        )
        return canonical, "high", rationale

    # Rule 4: most edge bullets
    sorted_by_edges = sorted(non_redirects, key=lambda n: n["edge_bullet_count"], reverse=True)
    if sorted_by_edges[0]["edge_bullet_count"] > sorted_by_edges[1]["edge_bullet_count"]:
        canonical = sorted_by_edges[0]["slug"]
        rationale = (
            f"{canonical!r} has more structured edge bullets "
            f"({sorted_by_edges[0]['edge_bullet_count']}) than "
            f"{sorted_by_edges[1]['slug']!r} "
            f"({sorted_by_edges[1]['edge_bullet_count']})."
        )
        return canonical, "medium", rationale

    # Rule 5: longer body
    sorted_by_body = sorted(non_redirects, key=lambda n: n["body_length"], reverse=True)
    if sorted_by_body[0]["body_length"] > sorted_by_body[1]["body_length"] * 1.3:
        canonical = sorted_by_body[0]["slug"]
        rationale = (
            f"{canonical!r} has substantially more body content "
            f"({sorted_by_body[0]['body_length']} chars) than "
            f"{sorted_by_body[1]['slug']!r} "
            f"({sorted_by_body[1]['body_length']} chars)."
        )
        return canonical, "medium", rationale

    # Rule 6: too close to call — flag for human judgment
    all_slugs = [n["slug"] for n in non_redirects]
    rationale = (
        f"Multiple non-redirect nodes with similar content: {all_slugs}. "
        f"Body lengths: { {n['slug']: n['body_length'] for n in non_redirects} }. "
        f"Human review required to confirm canonical name/scope."
    )
    return all_slugs[0], "low", rationale


# ── Edge scanning ─────────────────────────────────────────────────────────────

def scan_affected_edges(all_slugs: list[str]) -> list[dict]:
    """
    Return a list of edge dicts (with line number) where source_slug or
    target_slug appears in all_slugs.
    """
    slug_set = set(all_slugs)
    affected = []
    if not EDGES_FILE.exists():
        return affected
    with EDGES_FILE.open(encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                edge = json.loads(raw)
            except json.JSONDecodeError:
                continue
            src = edge.get("source_slug", "")
            tgt = edge.get("target_slug", "")
            if src in slug_set or tgt in slug_set:
                affected.append({
                    "line": lineno,
                    "edge_type": edge.get("edge_type", "?"),
                    "source_slug": src,
                    "target_slug": tgt,
                })
    return affected


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lookup",
        default=str(LOOKUP_PATH),
        help="Path to event-node-reuse-lookup.json",
    )
    args = parser.parse_args()

    lookup_path = Path(args.lookup)
    if not lookup_path.exists():
        print(f"ERROR: lookup file not found: {lookup_path}", file=sys.stderr)
        sys.exit(1)

    with lookup_path.open(encoding="utf-8") as fh:
        data = json.load(fh)

    lookup = data.get("lookup", data)  # support both wrapped and bare formats
    collision_groups = find_collision_groups(lookup)

    if not collision_groups:
        print("No collision groups found. Nothing to do.")
        sys.exit(0)

    # ── Build merge candidates ─────────────────────────────────────────────
    candidates = []
    for group in collision_groups:
        slugs = group["slugs"]
        nodes = [read_node(s) for s in slugs]

        missing = [n["slug"] for n in nodes if not n["exists"]]
        if missing:
            print(f"WARNING: node file(s) not found: {missing}", file=sys.stderr)

        canonical, confidence, rationale = select_canonical(nodes)
        merge_slugs = [s for s in slugs if s != canonical]
        affected_edges = scan_affected_edges(slugs)

        candidates.append({
            "canonical_slug": canonical,
            "merge_slugs": merge_slugs,
            "all_slugs": slugs,
            "collision_keys": group["collision_keys"],
            "confidence": confidence,
            "rationale": rationale,
            "node_details": {
                n["slug"]: {
                    "name": n.get("name", ""),
                    "type": n.get("type", ""),
                    "pass_origin": n.get("pass_origin", ""),
                    "same_as": n.get("same_as", ""),
                    "is_redirect": n.get("is_redirect", False),
                    "body_length": n.get("body_length", 0),
                    "edge_bullet_count": n.get("edge_bullet_count", 0),
                    "wiki_source": n.get("wiki_source", ""),
                }
                for n in nodes
            },
            "affected_edges": affected_edges,
            "merge_mechanism": (
                "SAME_AS edge from each merge_slug to canonical_slug; "
                "re-point all affected_edges to canonical_slug; "
                "merge_slug nodes are NOT deleted (redirect/quarantine only)."
            ),
        })

    # Sort: high-confidence first, then medium, then low
    order = {"high": 0, "medium": 1, "low": 2}
    candidates.sort(key=lambda c: order[c["confidence"]])

    # ── Write JSONL ───────────────────────────────────────────────────────
    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSONL.open("w", encoding="utf-8") as fh:
        for c in candidates:
            row = {
                "canonical_slug": c["canonical_slug"],
                "merge_slugs": c["merge_slugs"],
                "confidence": c["confidence"],
                "rationale": c["rationale"],
                "affected_edges": c["affected_edges"],
            }
            fh.write(json.dumps(row) + "\n")
    print(f"Wrote {len(candidates)} rows → {OUT_JSONL}")

    # ── Write Markdown summary ────────────────────────────────────────────
    high = [c for c in candidates if c["confidence"] == "high"]
    medium = [c for c in candidates if c["confidence"] == "medium"]
    low = [c for c in candidates if c["confidence"] == "low"]
    total_edges = sum(len(c["affected_edges"]) for c in candidates)

    lines = [
        "# Event Node Collision Merge Candidates",
        "",
        "> Generated by `scripts/stage-event-collision-merge.py`",
        "> READ-ONLY analysis — no graph/ files modified.",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Collision groups | {len(candidates)} |",
        f"| High-confidence merges | {len(high)} |",
        f"| Medium-confidence merges | {len(medium)} |",
        f"| Needs human judgment (low) | {len(low)} |",
        f"| Total affected edges | {total_edges} |",
        "",
        "---",
        "",
    ]

    def section(title: str, group: list[dict]) -> list[str]:
        out = [f"## {title}", ""]
        if not group:
            out.append("_None._")
            out.append("")
            return out
        for c in group:
            out.append(f"### `{c['canonical_slug']}` ← merge {c['merge_slugs']}")
            out.append("")
            out.append(f"**Confidence:** {c['confidence']}")
            out.append("")
            out.append(f"**Rationale:** {c['rationale']}")
            out.append("")
            out.append(f"**Collision key(s):** {c['collision_keys']}")
            out.append("")
            out.append("**Node details:**")
            out.append("")
            out.append("| Slug | Name | Type | Pass Origin | Is Redirect | Body Len | Edge Bullets | same_as |")
            out.append("|------|------|------|-------------|-------------|----------|--------------|---------|")
            for slug, nd in c["node_details"].items():
                marker = " *(canonical)*" if slug == c["canonical_slug"] else ""
                out.append(
                    f"| `{slug}`{marker} | {nd['name']} | {nd['type']} | {nd['pass_origin']} "
                    f"| {nd['is_redirect']} | {nd['body_length']} | {nd['edge_bullet_count']} | {nd['same_as']} |"
                )
            out.append("")
            if c["affected_edges"]:
                out.append(f"**Affected edges ({len(c['affected_edges'])}):**")
                out.append("")
                out.append("| Line | Edge Type | Source | Target |")
                out.append("|------|-----------|--------|--------|")
                for ae in c["affected_edges"]:
                    out.append(
                        f"| {ae['line']} | {ae['edge_type']} "
                        f"| `{ae['source_slug']}` | `{ae['target_slug']}` |"
                    )
                out.append("")
            else:
                out.append("**Affected edges:** _none in edges.jsonl_")
                out.append("")
            out.append(f"**Merge mechanism:** {c['merge_mechanism']}")
            out.append("")
            out.append("---")
            out.append("")
        return out

    lines += section("High-Confidence Merges", high)
    lines += section("Medium-Confidence Merges", medium)
    lines += section("Needs Human Judgment (Low Confidence)", low)

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote summary    → {OUT_MD}")

    # ── Console summary ───────────────────────────────────────────────────
    print()
    print(f"{'='*60}")
    print(f"COLLISION MERGE REPORT")
    print(f"{'='*60}")
    print(f"  Collision groups:        {len(candidates)}")
    print(f"  High-confidence:         {len(high)}")
    print(f"  Medium-confidence:       {len(medium)}")
    print(f"  Needs human judgment:    {len(low)}")
    print(f"  Total affected edges:    {total_edges}")
    print()
    print("Groups:")
    for c in candidates:
        edge_note = f"{len(c['affected_edges'])} edges affected" if c["affected_edges"] else "no edges affected"
        print(f"  [{c['confidence'].upper():6s}] {c['canonical_slug']} <- {c['merge_slugs']}  ({edge_note})")
    print()


if __name__ == "__main__":
    main()
