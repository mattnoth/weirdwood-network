#!/usr/bin/env python3
"""
event-node-inventory.py — Weirwood Network Plate 2.5

Inventories existing event nodes in graph/nodes/events/ and produces two outputs:
  1. working/edge-modeling/event-node-inventory.md  — human-readable catalog grouped by type
  2. working/edge-modeling/event-node-reuse-lookup.json — reuse lookup dict (normalized keys → slug)

Also appends a secondary reuse-coverage report to the catalog, estimating how many
reify-family edges in edges.jsonl could plausibly map onto an existing event node.

READ-ONLY on graph/ — writes only to working/edge-modeling/.

Usage:
    python3 scripts/event-node-inventory.py [--generated-at LABEL]

Arguments:
    --generated-at  Optional label for the generated_at field in the JSON (e.g. "2026-06-06").
                    If omitted, the field is excluded from the JSON output.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
EVENTS_DIR = REPO_ROOT / "graph" / "nodes" / "events"
EDGES_JSONL = REPO_ROOT / "graph" / "edges" / "edges.jsonl"
OUT_DIR = REPO_ROOT / "working" / "edge-modeling"
CATALOG_PATH = OUT_DIR / "event-node-inventory.md"
LOOKUP_PATH = OUT_DIR / "event-node-reuse-lookup.json"

# ---------------------------------------------------------------------------
# Drift detection patterns
# ---------------------------------------------------------------------------
# Known book-title slug fragments that appear in chapter titles misfiled as events
BOOK_TITLE_FRAGMENTS = [
    "the-winds-of-winter",
    "a-dance-with-dragons",
    "a-feast-for-crows",
    "a-storm-of-swords",
    "a-clash-of-kings",
    "a-game-of-thrones",
    "the-hedge-knight",
    "the-sworn-sword",
    "the-mystery-knight",
    "the-world-of-ice-and-fire",
    "fire-and-blood",
]
_BOOK_ALT = "|".join(re.escape(b) for b in BOOK_TITLE_FRAGMENTS)

# Pattern 1: <name>-<roman-numeral>-<book-title>  e.g. alayne-i-the-winds-of-winter
_ROMAN = r"(?:i{1,3}|iv|vi{0,3}|ix|xi{0,3}|xiv|xv|xvi{0,3}|xix|xx)"
DRIFT_PATTERNS = [
    re.compile(rf"-{_ROMAN}-(?:{_BOOK_ALT})$"),
    # Pattern 2: <name>-<book-title> (no numeral)  e.g. mercy-the-winds-of-winter
    re.compile(rf"-(?:{_BOOK_ALT})$"),
    # Pattern 3: <book-title>-epilogue / <book-title>-prologue
    re.compile(rf"(?:{_BOOK_ALT})-(?:epilogue|prologue)$"),
    # Pattern 4: bare -epilogue or -prologue suffix (catches a-storm-of-swords-epilogue etc.)
    re.compile(r"-(?:epilogue|prologue)$"),
]


def is_drift(slug: str) -> bool:
    """Return True if the slug looks like a chapter/POV entry misfiled as an event node."""
    for pat in DRIFT_PATTERNS:
        if pat.search(slug):
            return True
    return False


# ---------------------------------------------------------------------------
# Frontmatter parser (stdlib only — no yaml dep)
# ---------------------------------------------------------------------------
def parse_frontmatter(text: str) -> dict:
    """
    Extract YAML frontmatter between the first pair of '---' delimiters.
    Returns a dict of string key → value. Handles bare strings and quoted strings.
    Lists (- item) are parsed into Python lists.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        return {}

    result: dict = {}
    current_key = None
    for line in lines[1:end]:
        # skip blank lines
        if not line.strip():
            continue
        # list item
        if line.startswith("  - ") or line.startswith("- "):
            stripped = line.lstrip("- ").strip()
            # remove surrounding quotes
            if (stripped.startswith('"') and stripped.endswith('"')) or \
               (stripped.startswith("'") and stripped.endswith("'")):
                stripped = stripped[1:-1]
            if current_key is not None:
                if isinstance(result.get(current_key), list):
                    result[current_key].append(stripped)
                else:
                    result[current_key] = [stripped]
            continue
        # key: value
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            # quoted value
            if (val.startswith('"') and val.endswith('"')) or \
               (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            # empty value → start of list
            if val == "[]":
                result[key] = []
                current_key = key
            elif val == "":
                result[key] = []
                current_key = key
            else:
                result[key] = val
                current_key = key
    return result


# ---------------------------------------------------------------------------
# Normalization helpers for reuse lookup
# ---------------------------------------------------------------------------
STOPWORDS = frozenset({
    "the", "a", "an", "of", "at", "and", "in", "to", "for", "on", "by",
    "with", "from", "into", "or", "but", "nor", "so", "yet",
})
PUNCT_RE = re.compile(r"[^\w\s]")
WS_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    t = text.lower()
    t = PUNCT_RE.sub(" ", t)
    t = WS_RE.sub(" ", t).strip()
    return t


def token_set_key(text: str) -> str:
    """
    Sorted significant-token key: drop stopwords, sort remaining tokens, join with space.
    E.g. "death of tywin lannister" → "death lannister tywin"
    """
    tokens = normalize_text(text).split()
    sig = sorted(t for t in tokens if t and t not in STOPWORDS)
    return " ".join(sig)


def keys_for_node(slug: str, name: str, aliases: list) -> list[str]:
    """
    Generate all lookup keys for an event node:
      (a) the slug itself
      (b) normalized name
      (c) normalized alias (each)
      (d) token-set key of name
      (e) token-set key of each alias
    Returns deduplicated list.
    """
    seen = set()
    results = []

    def add(k: str):
        k = k.strip()
        if k and k not in seen:
            seen.add(k)
            results.append(k)

    add(slug)
    norm_name = normalize_text(name)
    add(norm_name)
    add(token_set_key(name))

    for alias in aliases:
        if alias:
            add(normalize_text(alias))
            add(token_set_key(alias))

    return results


# ---------------------------------------------------------------------------
# Reify-family edge types for coverage check
# ---------------------------------------------------------------------------
REIFY_EDGE_TYPES = {
    "KILLS", "EXECUTES", "POISONS", "SACRIFICES", "ASSAULTS",
    "CAPTURES", "BETRAYS", "CONSPIRES_WITH", "BESIEGES", "VIOLATES_GUEST_RIGHT",
}


def load_reify_edges(path: Path) -> list[dict]:
    """Load reify-family edges from edges.jsonl."""
    edges = []
    if not path.exists():
        return edges
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("edge_type") in REIFY_EDGE_TYPES:
                edges.append(row)
    return edges


def coverage_check(reify_edges: list[dict], lookup: dict) -> dict:
    """
    Rough estimate: for each reify edge, check if any token from source_slug or target_slug
    overlap with the reuse lookup keys (using token-set from participant slugs).
    Returns dict with total, covered count, per-type counts.
    """
    per_type: dict[str, dict] = {}
    total = 0
    covered = 0

    for edge in reify_edges:
        etype = edge.get("edge_type", "UNKNOWN")
        src = edge.get("source_slug", "")
        tgt = edge.get("target_slug", "")
        total += 1

        # Build a token set from both participant slugs (hyphen = token boundary)
        participant_tokens = set(src.replace("-", " ").split() + tgt.replace("-", " ").split())
        participant_tokens -= STOPWORDS

        # Check lookup keys for any significant overlap
        matched = False
        for key in lookup:
            key_tokens = set(key.split())
            if len(key_tokens & participant_tokens) >= 2:
                matched = True
                break

        if matched:
            covered += 1

        if etype not in per_type:
            per_type[etype] = {"total": 0, "covered": 0}
        per_type[etype]["total"] += 1
        if matched:
            per_type[etype]["covered"] += 1

    return {"total": total, "covered": covered, "per_type": per_type}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--generated-at",
        metavar="LABEL",
        help="Optional label for the generated_at metadata field in the JSON output.",
    )
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # 1. Scan event nodes
    # ------------------------------------------------------------------
    node_files = sorted(EVENTS_DIR.glob("*.node.md"))
    if not node_files:
        print(f"ERROR: No event node files found in {EVENTS_DIR}", file=sys.stderr)
        sys.exit(1)

    nodes_by_type: dict[str, list[dict]] = defaultdict(list)
    drift_nodes: list[dict] = []
    all_nodes: list[dict] = []
    parse_errors: list[str] = []

    for fpath in node_files:
        text = fpath.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if not fm:
            parse_errors.append(fpath.name)
            continue

        slug = fm.get("slug") or fpath.stem.replace(".node", "")
        name = fm.get("name", slug)
        ntype = fm.get("type", "unknown")
        aliases = fm.get("aliases", [])
        if isinstance(aliases, str):
            aliases = [aliases] if aliases else []
        wiki_source = fm.get("wiki_source", "")
        pass_origin = fm.get("pass_origin", "")

        node = {
            "slug": slug,
            "name": name,
            "type": ntype,
            "aliases": aliases,
            "wiki_source": wiki_source,
            "pass_origin": pass_origin,
            "file": fpath.name,
        }
        all_nodes.append(node)

        if is_drift(slug):
            drift_nodes.append(node)
        else:
            nodes_by_type[ntype].append(node)

    # ------------------------------------------------------------------
    # 2. Build reuse lookup
    # ------------------------------------------------------------------
    lookup: dict[str, list[str]] = defaultdict(list)  # key → list of slugs (collisions possible)
    collision_keys: dict[str, list[str]] = {}

    for node in all_nodes:
        if is_drift(node["slug"]):
            continue  # skip drift nodes from reuse lookup
        ks = keys_for_node(node["slug"], node["name"], node["aliases"])
        for k in ks:
            lookup[k].append(node["slug"])

    # Identify collisions (key maps to >1 slug)
    for k, slugs in lookup.items():
        if len(slugs) > 1:
            collision_keys[k] = slugs

    # Flatten: key → slug (keep list for collisions, single string otherwise)
    lookup_final: dict[str, object] = {}
    for k, slugs in lookup.items():
        if len(slugs) == 1:
            lookup_final[k] = slugs[0]
        else:
            lookup_final[k] = slugs  # collision — preserve all candidates

    # ------------------------------------------------------------------
    # 3. Load reify edges + coverage check
    # ------------------------------------------------------------------
    reify_edges = load_reify_edges(EDGES_JSONL)
    coverage = coverage_check(reify_edges, lookup_final)

    # ------------------------------------------------------------------
    # 4. Write reuse lookup JSON
    # ------------------------------------------------------------------
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    metadata = {
        "description": "Weirwood Network event-node reuse lookup (Plate 2.5). "
                       "Maps normalized keys to event node slugs for reuse-before-mint. "
                       "Collision entries are lists; single-slug entries are strings.",
        "total_event_nodes": len(all_nodes),
        "drift_excluded": len(drift_nodes),
        "non_drift_nodes": len(all_nodes) - len(drift_nodes),
        "total_lookup_keys": len(lookup_final),
        "collision_key_count": len(collision_keys),
        "source": str(EVENTS_DIR.relative_to(REPO_ROOT)),
    }
    if args.generated_at:
        metadata["generated_at"] = args.generated_at

    json_out = {
        "_metadata": metadata,
        "lookup": lookup_final,
        "collisions": collision_keys,
    }

    LOOKUP_PATH.write_text(json.dumps(json_out, indent=2, ensure_ascii=False), encoding="utf-8")

    # ------------------------------------------------------------------
    # 5. Write catalog markdown
    # ------------------------------------------------------------------
    lines = []
    lines.append("# Event Node Inventory — Weirwood Network (Plate 2.5)")
    lines.append("")
    if args.generated_at:
        lines.append(f"Generated: {args.generated_at}")
        lines.append("")

    # Summary header
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total event nodes scanned:** {len(all_nodes)}")
    lines.append(f"- **Suspected category drift (excluded from reuse):** {len(drift_nodes)}")
    lines.append(f"- **Non-drift nodes available for reuse:** {len(all_nodes) - len(drift_nodes)}")
    lines.append(f"- **Reuse lookup keys generated:** {len(lookup_final)}")
    lines.append(f"- **Collision keys (multiple slugs per key):** {len(collision_keys)}")
    if parse_errors:
        lines.append(f"- **Parse errors (skipped):** {len(parse_errors)}: {', '.join(parse_errors)}")
    lines.append("")
    lines.append("### Counts by type")
    lines.append("")
    lines.append("| Type | Count |")
    lines.append("|------|-------|")
    type_order = sorted(nodes_by_type.keys())
    for t in type_order:
        lines.append(f"| `{t}` | {len(nodes_by_type[t])} |")
    lines.append(f"| *(drift / excluded)* | {len(drift_nodes)} |")
    lines.append(f"| **Total** | **{len(all_nodes)}** |")
    lines.append("")

    # Per-type sections
    lines.append("---")
    lines.append("")
    for t in type_order:
        nodes = nodes_by_type[t]
        lines.append(f"## Type: `{t}` ({len(nodes)} nodes)")
        lines.append("")
        lines.append("| Slug | Name | Aliases | wiki_source |")
        lines.append("|------|------|---------|-------------|")
        for node in sorted(nodes, key=lambda n: n["slug"]):
            alias_str = "; ".join(node["aliases"]) if node["aliases"] else "—"
            has_wiki = "yes" if node["wiki_source"] else "no"
            # Escape pipes in names/aliases
            name_esc = node["name"].replace("|", "\\|")
            alias_esc = alias_str.replace("|", "\\|")
            lines.append(f"| `{node['slug']}` | {name_esc} | {alias_esc} | {has_wiki} |")
        lines.append("")

    # Drift section
    lines.append("---")
    lines.append("")
    lines.append(f"## Suspected category drift (NOT real events) — {len(drift_nodes)} nodes")
    lines.append("")
    lines.append(
        "These slugs match the chapter-title pattern "
        "(`<name>-<roman-numeral>-<book-title>`, `<name>-<book-title>`, or `<book-title>-epilogue/prologue`) "
        "and are almost certainly POV-chapter pages misfiled under events. "
        "**The reuse lookup excludes these.** The backfill pass should skip them as reuse targets."
    )
    lines.append("")
    lines.append("| Slug | Name | Type |")
    lines.append("|------|------|------|")
    for node in sorted(drift_nodes, key=lambda n: n["slug"]):
        name_esc = node["name"].replace("|", "\\|")
        lines.append(f"| `{node['slug']}` | {name_esc} | `{node['type']}` |")
    lines.append("")

    # Collision report
    if collision_keys:
        lines.append("---")
        lines.append("")
        lines.append(f"## Lookup key collisions ({len(collision_keys)} keys map to multiple slugs)")
        lines.append("")
        lines.append("These keys matched more than one event node. The lookup preserves all candidates.")
        lines.append("")
        lines.append("| Key | Slugs |")
        lines.append("|-----|-------|")
        for k in sorted(collision_keys):
            slugs_str = ", ".join(f"`{s}`" for s in collision_keys[k])
            lines.append(f"| `{k}` | {slugs_str} |")
        lines.append("")

    # Secondary: reuse-coverage report
    lines.append("---")
    lines.append("")
    lines.append("## Secondary: Reify-family edge reuse-coverage estimate")
    lines.append("")
    lines.append(
        "For reify-family edge types (KILLS, EXECUTES, POISONS, SACRIFICES, ASSAULTS, CAPTURES, "
        "BETRAYS, CONSPIRES_WITH, BESIEGES, VIOLATES_GUEST_RIGHT), this section estimates how many "
        "distinct (source, target) pairs COULD plausibly map onto an existing event node via the "
        "reuse lookup (token overlap ≥ 2 significant tokens between participant slugs and lookup keys)."
    )
    lines.append("")
    lines.append(
        "> **Note:** This is a rough heuristic signal — token overlap on participant slugs vs. "
        "event-name keys. It over-counts (common tokens like 'battle', 'war') and under-counts "
        "(slug abbreviations). Use as an order-of-magnitude estimate only."
    )
    lines.append("")
    lines.append(f"- **Total reify-family edges in edges.jsonl:** {coverage['total']}")
    lines.append(
        f"- **Estimated edges with a plausible existing event-node match:** "
        f"{coverage['covered']} ({coverage['covered'] / max(coverage['total'], 1) * 100:.1f}%)"
    )
    lines.append("")
    lines.append("### Per edge type")
    lines.append("")
    lines.append("| Edge type | Total | Estimated covered | % |")
    lines.append("|-----------|-------|-------------------|---|")
    for etype in sorted(coverage["per_type"]):
        d = coverage["per_type"][etype]
        pct = d["covered"] / max(d["total"], 1) * 100
        lines.append(f"| `{etype}` | {d['total']} | {d['covered']} | {pct:.1f}% |")
    lines.append("")

    CATALOG_PATH.write_text("\n".join(lines), encoding="utf-8")

    # ------------------------------------------------------------------
    # 6. Stdout summary
    # ------------------------------------------------------------------
    print("=== Event Node Inventory — Plate 2.5 ===")
    print(f"  Total event nodes:            {len(all_nodes)}")
    for t in type_order:
        print(f"    {t:<25s}: {len(nodes_by_type[t])}")
    print(f"  Suspected category drift:     {len(drift_nodes)}")
    print(f"  Non-drift (reuse eligible):   {len(all_nodes) - len(drift_nodes)}")
    print(f"  Reuse lookup keys:            {len(lookup_final)}")
    print(f"  Collision keys:               {len(collision_keys)}")
    print(f"  Reify-family edges (total):   {coverage['total']}")
    print(
        f"  Approx. reuse-covered edges:  "
        f"{coverage['covered']} ({coverage['covered'] / max(coverage['total'], 1) * 100:.1f}%)"
    )
    if parse_errors:
        print(f"  Parse errors (skipped):       {len(parse_errors)}")
    print("")
    print(f"  Catalog:      {CATALOG_PATH}")
    print(f"  Reuse lookup: {LOOKUP_PATH}")


if __name__ == "__main__":
    main()
