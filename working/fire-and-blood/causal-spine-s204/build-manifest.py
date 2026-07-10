#!/usr/bin/env python3
"""S204 causal-spine deterministic prep (feedback_python_before_agent).

Builds the work manifest for the F&B causal-spine session:
  1. Inventory every fab-layer event node (pass_origin: pass-fab-enrichment OR
     era in the Targaryen-history set) with occurred/sort_keys years.
  2. Per-node edge census from edges.jsonl split by class (causal / structural /
     role / other) so causally-dark nodes are visible.
  3. Re-verify the 38 zero-edge stubs are still zero-edge.
  4. Parse the 53 causal-spine seeds and attach best-guess slug candidates for
     each beat mentioned in the note (token-overlap match, no LLM).
  5. Year-ordered listing per era to guide chain construction.

Outputs (all under working/fire-and-blood/causal-spine-s204/):
  manifest-nodes.jsonl   one row per fab-layer event node
  manifest-seeds.jsonl   one row per seed with slug candidates
  manifest-summary.md    human-readable summary
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "working/fire-and-blood/causal-spine-s204"
NODES = ROOT / "graph/nodes"
EDGES = ROOT / "graph/edges/edges.jsonl"
SEEDS = ROOT / "working/fire-and-blood/causal-spine-seeds-s203.jsonl"
STUBS = ROOT / "working/fire-and-blood/apply/zero-edge-stubs-s203.jsonl"

FAB_ERAS = {"targaryen-conquest", "targaryen-rule", "dance-of-dragons"}
CAUSAL = {"CAUSES", "TRIGGERS", "MOTIVATES", "ENABLES", "PREVENTS"}
STRUCT = {"PART_OF", "SUB_BEAT_OF", "PRECEDES"}
ROLE = {"AGENT_IN", "VICTIM_IN", "WITNESS_IN", "COMMANDS_IN", "FIGHTS_IN",
        "PARTICIPATES_IN", "ATTENDS", "OFFICIATES", "WIELDED_IN", "HONORED_AT"}
DEPRECATED = {"KNOWS"}

STOP = {"the", "of", "a", "an", "and", "to", "in", "at", "for", "on", "by",
        "then", "leads", "lead", "his", "her", "as", "with", "not", "will"}


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    fm: dict = {}
    block = m.group(1)
    # slug, era, pass_origin, type, name (simple scalars)
    for key in ("slug", "era", "pass_origin", "type", "name", "confidence"):
        km = re.search(rf"^{key}:\s*\"?([^\"\n]+)\"?\s*$", block, re.MULTILINE)
        if km:
            fm[key] = km.group(1).strip()
    ym = re.search(r"^occurred:\s*\n((?:\s{2,}.*\n?)+)", block, re.MULTILINE)
    if ym:
        ac = re.search(r"ac_year:\s*(-?\d+)", ym.group(1))
        if ac:
            fm["ac_year"] = int(ac.group(1))
    sk = re.search(r"^sort_keys:\s*\n((?:\s{2,}.*\n?)+)", block, re.MULTILINE)
    if sk:
        yr = re.search(r"year:\s*(-?\d+)", sk.group(1))
        if yr:
            fm["sort_year"] = int(yr.group(1))
    return fm


def main() -> None:
    # --- 0. slugs touched by book-fab edges (catches era-less wiki shells) ---
    fab_touched = set()
    with EDGES.open(encoding="utf-8") as f:
        for line in f:
            if '"book-fab"' not in line:
                continue
            e = json.loads(line)
            if e.get("evidence_kind") == "book-fab":
                for s in (e.get("source_slug") or e.get("source"),
                          e.get("target_slug") or e.get("target")):
                    if s:
                        fab_touched.add(s)

    # --- 1. fab-layer event nodes -----------------------------------------
    fab_nodes = {}
    for p in sorted((NODES / "events").glob("*.node.md")):
        fm = parse_frontmatter(p)
        slug = fm.get("slug") or p.stem.replace(".node", "")
        is_fab = (fm.get("pass_origin") == "pass-fab-enrichment"
                  or fm.get("era") in FAB_ERAS
                  or slug in fab_touched)
        if is_fab:
            fab_nodes[slug] = {
                "slug": slug,
                "name": fm.get("name", slug),
                "type": fm.get("type"),
                "era": fm.get("era"),
                "pass_origin": fm.get("pass_origin"),
                "fab_touched": slug in fab_touched,
                "ac_year": fm.get("ac_year") or fm.get("sort_year"),
            }

    # --- 2. edge census ----------------------------------------------------
    census = defaultdict(lambda: {"causal_in": 0, "causal_out": 0,
                                  "struct": 0, "role": 0, "other": 0})
    fab_causal_edges = 0
    with EDGES.open(encoding="utf-8") as f:
        for line in f:
            e = json.loads(line)
            if e.get("decision") not in (None, "emit_edge"):
                continue
            et = e.get("edge_type") or e.get("type")
            if not et or et in DEPRECATED:
                continue
            src = e.get("source_slug") or e.get("source")
            tgt = e.get("target_slug") or e.get("target")
            for slug, direction in ((src, "out"), (tgt, "in")):
                if slug not in fab_nodes:
                    continue
                c = census[slug]
                if et in CAUSAL:
                    c["causal_out" if direction == "out" else "causal_in"] += 1
                elif et in STRUCT:
                    c["struct"] += 1
                elif et in ROLE:
                    c["role"] += 1
                else:
                    c["other"] += 1
            if et in CAUSAL and (src in fab_nodes or tgt in fab_nodes):
                fab_causal_edges += 1

    for slug, meta in fab_nodes.items():
        meta.update(census[slug])
        meta["causally_dark"] = (meta["causal_in"] + meta["causal_out"]) == 0

    # --- 3. zero-edge stubs re-check ----------------------------------------
    stubs = []
    for line in STUBS.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if not row.get("slug"):
            continue  # future-mint candidates at the foot
        slug = row["slug"]
        c = census.get(slug)
        total = sum(c.values()) if c else 0
        # stub may live outside events/ (e.g. medical) — census only covers events
        stubs.append({**row, "event_edges_now": total,
                      "in_event_inventory": slug in fab_nodes})

    # --- 4. seeds with slug candidates --------------------------------------
    # token index over fab node names+slugs
    def tokens(s: str) -> set:
        return {t for t in re.split(r"[^a-z0-9]+", s.lower()) if t and t not in STOP}

    node_tokens = {slug: tokens(meta["name"]) | tokens(slug)
                   for slug, meta in fab_nodes.items()}

    seeds = []
    for line in SEEDS.read_text(encoding="utf-8").splitlines():
        seed = json.loads(line)
        want = tokens(seed.get("note") or "") | tokens(seed.get("snippet") or "")
        scored = []
        for slug, ntok in node_tokens.items():
            ov = len(want & ntok)
            if ov >= 2:
                scored.append((ov / max(len(ntok), 1) + ov * 0.1, ov, slug))
        scored.sort(reverse=True)
        seed["slug_candidates"] = [s for _, _, s in scored[:8]]
        seeds.append(seed)

    # --- write outputs -------------------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "manifest-nodes.jsonl").open("w", encoding="utf-8") as f:
        for meta in sorted(fab_nodes.values(),
                           key=lambda m: (m["ac_year"] is None, m["ac_year"] or 0, m["slug"])):
            f.write(json.dumps(meta, ensure_ascii=False) + "\n")
    with (OUT / "manifest-seeds.jsonl").open("w", encoding="utf-8") as f:
        for seed in seeds:
            f.write(json.dumps(seed, ensure_ascii=False) + "\n")

    dark = [m for m in fab_nodes.values() if m["causally_dark"]]
    dated = [m for m in fab_nodes.values() if m["ac_year"] is not None]
    lines = [
        "# S204 causal-spine work manifest — summary",
        "",
        f"- fab-layer event nodes: **{len(fab_nodes)}** "
        f"({sum(1 for m in fab_nodes.values() if m['pass_origin'] == 'pass-fab-enrichment')} "
        f"pass-fab-enrichment + era-matched wiki nodes)",
        f"- dated (occurred/sort_keys year): {len(dated)}",
        f"- causal edges touching the fab layer: {fab_causal_edges}",
        f"- **causally dark** (0 causal in+out): **{len(dark)}**",
        f"- zero-edge stubs re-checked: {len(stubs)} "
        f"(still-zero: {sum(1 for s in stubs if s['event_edges_now'] == 0)})",
        f"- seeds parsed: {len(seeds)} "
        f"(with >=1 slug candidate: {sum(1 for s in seeds if s['slug_candidates'])})",
        "",
        "## Causally dark, by era",
    ]
    by_era = defaultdict(int)
    for m in dark:
        by_era[m["era"] or "?"] += 1
    for era, n in sorted(by_era.items(), key=lambda kv: -kv[1]):
        lines.append(f"- {era}: {n}")
    (OUT / "manifest-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
