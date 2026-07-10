#!/usr/bin/env python3
"""S204 step 2 of deterministic prep: per-unit work packets.

Maps every fab-layer event node to the F&B unit(s) whose book-fab edges cite it
(evidence_chapter), then writes one packet per unit-group containing:
  - the unit's causal-spine seeds (with slug candidates)
  - the unit's zero-edge stubs
  - the unit's event-node roster (slug / name / year / causally_dark)
Packets land in working/fire-and-blood/causal-spine-s204/packets/.
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "working/fire-and-blood/causal-spine-s204"
EDGES = ROOT / "graph/edges/edges.jsonl"
STUBS = ROOT / "working/fire-and-blood/apply/zero-edge-stubs-s203.jsonl"

nodes = {}
for line in (OUT / "manifest-nodes.jsonl").read_text(encoding="utf-8").splitlines():
    m = json.loads(line)
    nodes[m["slug"]] = m

# node -> units via book-fab edge chapters
node_units = defaultdict(set)
with EDGES.open(encoding="utf-8") as f:
    for line in f:
        if '"book-fab"' not in line:
            continue
        e = json.loads(line)
        if e.get("evidence_kind") != "book-fab":
            continue
        ch = e.get("evidence_chapter") or e.get("chapter") or ""
        if not ch.startswith("fab-"):
            continue
        for s in (e.get("source_slug") or e.get("source"),
                  e.get("target_slug") or e.get("target")):
            if s in nodes:
                node_units[s].add(ch)

seeds = [json.loads(l) for l in
         (OUT / "manifest-seeds.jsonl").read_text(encoding="utf-8").splitlines()]
stubs = [json.loads(l) for l in
         STUBS.read_text(encoding="utf-8").splitlines() if '"slug": null' not in l]

# collapse sub-splits: fab-x-NN-pMM -> section key fab-x-NN
def section(unit: str) -> str:
    import re
    return re.sub(r"-p\d+$", "", unit) if unit else "UNMAPPED"

by_section = defaultdict(lambda: {"seeds": [], "stubs": [], "units": set()})
for s in seeds:
    sec = section(s.get("unit") or "")
    by_section[sec]["seeds"].append(s)
    if s.get("unit"):
        by_section[sec]["units"].add(s["unit"])
for s in stubs:
    sec = section(s["unit"])
    by_section[sec]["stubs"].append(s)
    by_section[sec]["units"].add(s["unit"])

# roster per section
for slug, units in node_units.items():
    for u in units:
        sec = section(u)
        if sec in by_section:
            by_section[sec].setdefault("roster", {})[slug] = nodes[slug]

pk = OUT / "packets"
pk.mkdir(exist_ok=True)
index = []
for sec, data in sorted(by_section.items()):
    roster = data.get("roster", {})
    packet = {
        "section": sec,
        "units": sorted(data["units"]),
        "seeds": data["seeds"],
        "stubs": data["stubs"],
        "roster": sorted(roster.values(),
                         key=lambda m: (m["ac_year"] is None, m["ac_year"] or 0, m["slug"])),
    }
    (pk / f"{sec}.json").write_text(
        json.dumps(packet, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    index.append((sec, len(data["seeds"]), len(data["stubs"]), len(roster)))

print(f"{'section':55} seeds stubs roster")
for sec, ns, nst, nr in index:
    print(f"{sec:55} {ns:5} {nst:5} {nr:6}")
print(f"\n{len(index)} sections; unmapped-unit seeds: "
      f"{sum(1 for s in seeds if not s.get('unit'))}")
