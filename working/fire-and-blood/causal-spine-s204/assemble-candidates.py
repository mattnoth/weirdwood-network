#!/usr/bin/env python3
"""S204: assemble proposer outputs into a mint-ready candidates.json.

Reads working/fire-and-blood/causal-spine-s204/proposals/*.json, then:
  - validates rows (type in locked vocab, slugs resolve to node files or to
    new_nodes, required fields present)
  - dedups against edges.jsonl (same type+source+target already live)
  - dedups across proposals
  - locates every quote with the same norm() as mint_enrichment.py
  - writes apply/fab-causal-spine-s204/candidates.json + nodes/ stubs report

Rows that fail land in review-queue.jsonl with a reason — nothing is dropped
silently. Run repeatedly; it rebuilds from scratch each time.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "working/fire-and-blood/causal-spine-s204"
PROPS = BASE / "proposals"
APPLY = ROOT / "working/fire-and-blood/apply/fab-causal-spine-s204"
EDGES = ROOT / "graph/edges/edges.jsonl"
NODES = ROOT / "graph/nodes"

CAUSAL = {"CAUSES", "TRIGGERS", "MOTIVATES", "ENABLES", "PREVENTS"}
STRUCT = {"PART_OF", "SUB_BEAT_OF", "PRECEDES"}
ROLE = {"AGENT_IN", "VICTIM_IN", "WITNESS_IN", "COMMANDS_IN", "FIGHTS_IN",
        "PARTICIPATES_IN", "ATTENDS", "OFFICIATES", "WIELDED_IN", "HONORED_AT"}
DYAD = {"KILLS", "KILLED_BY", "POISONS", "EXECUTES", "CAPTURES", "PRISONER_OF",
        "IMPRISONS", "BANISHES", "BETRAYS", "DECEIVES", "MANIPULATES",
        "CONSPIRES_WITH", "SUSPECTED_OF", "APPOINTS", "DEPOSES", "SUCCEEDS",
        "CONTRACTED_WITH", "RESCUES", "TORTURES", "ATTACKS", "OPPOSES",
        "MARRIES_OFF", "HEALS", "SPOUSE_OF", "BETROTHED_TO", "PROPOSED_AS_BRIDE",
        "LOCATED_AT", "DIED_AT", "DIED_OF", "AFFLICTED_BY", "TRAVELS_TO",
        "GIFTED_TO", "INHERITED_BY", "REVEALS_TO", "SEEKS", "GRANTS_SAFE_CONDUCT",
        "CLAIMS", "HOLDS_TITLE", "VOWS_TO", "BREAKS_VOW", "FORESHADOWS",
        "PARALLELS", "MOURNS", "LOVES", "HATES", "FEARS", "DISTRUSTS", "TRUSTS"}
ALLOWED = CAUSAL | STRUCT | ROLE | DYAD


def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def locate(chapter, quote):
    f = ROOT / "sources/chapters/fab" / f"{chapter}.md"
    if not f.exists():
        return None, "chapter file missing"
    lines = f.read_text(encoding="utf-8").splitlines()
    q = norm(quote)
    if not q:
        return None, "empty quote"
    for i, ln in enumerate(lines, 1):
        if q in norm(ln):
            return i, None
    for i in range(len(lines) - 1):
        if q in norm(lines[i] + " " + lines[i + 1]):
            return i + 1, None
    return None, "quote not located (must sit in 1 line or span 2 adjacent lines)"


def node_exists(slug):
    return bool(list(NODES.glob(f"*/{slug}.node.md")))


def main():
    live = set()
    with EDGES.open(encoding="utf-8") as f:
        for line in f:
            e = json.loads(line)
            et = e.get("edge_type") or e.get("type")
            s = e.get("source_slug") or e.get("source")
            t = e.get("target_slug") or e.get("target")
            live.add((et, s, t))

    all_edges, all_nodes, review = [], {}, []
    harvest, flags, unwired = [], [], []
    seen = set()
    for p in sorted(PROPS.glob("*.json")):
        try:
            prop = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as ex:
            review.append({"file": p.name, "reason": f"JSON parse error: {ex}"})
            continue
        for n in prop.get("new_nodes", []):
            slug = n.get("slug")
            if not slug:
                review.append({"file": p.name, "node": n, "reason": "new_node missing slug"})
                continue
            if node_exists(slug):
                review.append({"file": p.name, "node": slug,
                               "reason": "new_node already exists in graph — check intent"})
                continue
            if slug in all_nodes and all_nodes[slug] != n:
                review.append({"file": p.name, "node": slug,
                               "reason": "conflicting duplicate new_node across proposals"})
            all_nodes[slug] = n
        harvest += prop.get("harvest", [])
        flags += [f"{p.stem}: {fl}" for fl in prop.get("flags", [])]
        unwired += prop.get("unwired_stubs", [])
        for e in prop.get("edges", []):
            e["_file"] = p.stem
            key = (e.get("type"), e.get("source"), e.get("target"))
            problems = []
            if e.get("type") not in ALLOWED:
                problems.append(f"type {e.get('type')} not in locked vocab")
            for field in ("source", "target", "chapter", "quote", "tier", "id"):
                if not e.get(field):
                    problems.append(f"missing {field}")
            if key in live:
                problems.append("edge already live in edges.jsonl")
            if key in seen:
                problems.append("duplicate across proposals")
            if e.get("disputed") and e.get("tier") == "tier-1":
                problems.append("disputed=true must be tier-2")
            if not problems:
                ln, err = locate(e["chapter"], e["quote"])
                if err:
                    problems.append(err)
                else:
                    e["line_located"] = ln
            for endpoint in ("source", "target"):
                slug = e.get(endpoint)
                if slug and not node_exists(slug) and slug not in all_nodes:
                    problems.append(f"{endpoint} slug {slug} resolves to no node and no new_node")
            if problems:
                review.append({**e, "reasons": problems})
            else:
                seen.add(key)
                all_edges.append(e)

    APPLY.mkdir(parents=True, exist_ok=True)
    pack = {
        "_meta": {
            "unit": "fab-causal-spine-s204",
            "session": "S204",
            "run_id": "fab-causal-spine-s204-2026-07-10",
            "evidence_kind": "book-fab",
            "new_node_slugs": sorted(all_nodes),
            "note": "S204 causal spine: 53 S203 harvest seeds + marquee Dance chains + 38 zero-edge stubs. Proposers Sonnet x10, orchestrator-adjudicated, Haiku fresh-verified.",
            "produced_at": "2026-07-10T00:00:00+00:00",
        },
        "edges": [{k: v for k, v in e.items() if not k.startswith("_")} for e in all_edges],
        "new_nodes": list(all_nodes.values()),
    }
    (APPLY / "candidates-draft.json").write_text(
        json.dumps(pack, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    with (BASE / "review-queue.jsonl").open("w", encoding="utf-8") as f:
        for r in review:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    (BASE / "assembly-extras.json").write_text(json.dumps(
        {"harvest": harvest, "flags": flags, "unwired_stubs": unwired},
        indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    by_type = defaultdict(int)
    for e in all_edges:
        by_type[e["type"]] += 1
    print(f"proposals: {len(list(PROPS.glob('*.json')))} files")
    print(f"clean edges: {len(all_edges)}  | new nodes: {len(all_nodes)} "
          f"| review-queue: {len(review)} | flags: {len(flags)} "
          f"| unwired stubs: {len(unwired)} | harvest: {len(harvest)}")
    for t, n in sorted(by_type.items(), key=lambda kv: -kv[1]):
        print(f"  {t:20} {n}")


if __name__ == "__main__":
    main()
