#!/usr/bin/env python3
"""S213 Dance arc — deterministic causal-gap map (read-only).

Lists every causal edge (CAUSES/TRIGGERS/MOTIVATES/ENABLES) among the Dance-era
event set, then prints the canonical F&B story-order chain with each link marked
PRESENT or MISSING. Also dumps role coverage on the umbrella + missed events.
"""
import json
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CAUSAL = {"CAUSES", "TRIGGERS", "MOTIVATES", "ENABLES"}
ROLE_TYPES = {"AGENT_IN", "VICTIM_IN", "WITNESS_IN", "COMMANDS_IN",
              "PARTICIPATES_IN", "FIGHTS_IN", "ATTENDS", "OFFICIATES", "HONORED_AT"}

DANCE_EVENTS = [
    "death-of-viserys-i", "coronation-of-aegon-ii", "dance-of-the-dragons",
    "death-of-lucerys-velaryon", "battle-at-rooks-rest", "battle-of-the-gullet",
    "battle-of-the-honeywine", "fall-of-kings-landing", "the-sowing",
    "battle-by-the-lakeshore", "butchers-ball", "aemonds-march-on-harrenhal",
    "battle-above-the-gods-eye", "first-battle-of-tumbleton",
    "second-battle-of-tumbleton", "storming-of-the-dragonpit",
    "fall-of-dragonstone", "death-of-queen-rhaenyra", "hour-of-the-wolf",
    "the-dragons-wroth", "daughters-war",
]

# canonical story-order adjacencies a HotD viewer would walk (loose, not exhaustive)
EXPECTED_LINKS = [
    ("death-of-viserys-i", "coronation-of-aegon-ii"),
    ("coronation-of-aegon-ii", "dance-of-the-dragons"),
    ("death-of-viserys-i", "dance-of-the-dragons"),
    ("dance-of-the-dragons", "death-of-lucerys-velaryon"),
    ("death-of-lucerys-velaryon", "blood-and-cheese"),  # node MISSING today
    ("battle-at-rooks-rest", "fall-of-kings-landing"),
    ("the-sowing", "battle-of-the-gullet"),
    ("fall-of-kings-landing", "storming-of-the-dragonpit"),
    ("butchers-ball", "battle-above-the-gods-eye"),
    ("aemonds-march-on-harrenhal", "battle-above-the-gods-eye"),
    ("first-battle-of-tumbleton", "second-battle-of-tumbleton"),
    ("storming-of-the-dragonpit", "death-of-queen-rhaenyra"),
    ("fall-of-dragonstone", "death-of-queen-rhaenyra"),
    ("death-of-queen-rhaenyra", "hour-of-the-wolf"),
    ("second-battle-of-tumbleton", "hour-of-the-wolf"),
]

exists = set()
for p in (REPO / "graph/nodes/events").glob("*.node.md"):
    exists.add(p.name[:-8])

causal_edges = []
roles = defaultdict(list)
with open(REPO / "graph/edges/edges.jsonl") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        e = json.loads(line)
        t, s, tg = e.get("edge_type"), e.get("source_slug"), e.get("target_slug")
        if t in CAUSAL and (s in DANCE_EVENTS or tg in DANCE_EVENTS):
            causal_edges.append((s, t, tg))
        if t in ROLE_TYPES and tg in DANCE_EVENTS:
            roles[tg].append((t, s))

print("=== existing causal edges touching the Dance set ===")
for s, t, tg in sorted(causal_edges):
    print(f"  {s} -{t}-> {tg}")

pair_set = {(s, tg) for s, _, tg in causal_edges}
print("\n=== expected HotD-walk links ===")
for a, b in EXPECTED_LINKS:
    state = "PRESENT" if (a, b) in pair_set else "MISSING"
    missing_node = "".join(f" [{x}: NO NODE]" for x in (a, b) if x not in exists)
    print(f"  {a} -> {b}: {state}{missing_node}")

print("\n=== role coverage on umbrella + weak events ===")
for ev in ["dance-of-the-dragons", "aemonds-march-on-harrenhal", "daughters-war",
           "death-of-viserys-i", "coronation-of-aegon-ii", "death-of-lucerys-velaryon"]:
    print(f"  {ev}: {roles.get(ev, '(none)')}"
          + ("" if ev in exists else "  [NO NODE]"))
