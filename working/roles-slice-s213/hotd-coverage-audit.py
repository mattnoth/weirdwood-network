#!/usr/bin/env python3
"""S213 — HotD-viewer coverage audit (read-only).

For every entity a House of the Dragon viewer is likely to ask about, report
what the graph holds: node? quotes? role edges? causal wiring? identity prose?
Gaps at the bottom. Names resolve through the alias lookup + slug guesses.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# name -> optional slug hint
PEOPLE = [
    "Rhaenyra Targaryen", "Daemon Targaryen", "Alicent Hightower", "Otto Hightower",
    "Viserys I Targaryen", "Aegon II Targaryen", "Aemond Targaryen", "Helaena Targaryen",
    "Criston Cole", "Corlys Velaryon", "Rhaenys Targaryen", "Larys Strong",
    "Harwin Strong", "Lyonel Strong", "Mysaria", "Jacaerys Velaryon",
    "Lucerys Velaryon", "Joffrey Velaryon", "Baela Targaryen", "Rhaena Targaryen",
    "Aegon III Targaryen", "Laenor Velaryon", "Laena Velaryon", "Vaemond Velaryon",
    "Alys Rivers", "Hugh Hammer", "Ulf the White", "Addam Velaryon", "Nettles",
    "Cregan Stark", "Borros Baratheon", "Daeron Targaryen", "Jason Lannister",
    "Jeyne Arryn", "Willem Blackwood", "Aegon the Elder",
]
DRAGONS = [
    "Syrax", "Caraxes", "Vhagar", "Sunfyre", "Dreamfyre", "Seasmoke", "Vermithor",
    "Silverwing", "Meleys", "Moondancer", "Vermax", "Arrax", "Tyraxes",
    "Sheepstealer", "Cannibal", "Grey Ghost", "Tessarion", "Morghul", "Shrykos",
]
EVENTS = [
    "Dance of the Dragons", "Great Council of 101", "Blood and Cheese",
    "Battle of Rook's Rest", "Storming of the Dragonpit",
    "Battle Above the Gods Eye", "Butcher's Ball", "Battle by the Lakeshore",
    "Fishfeed", "the Sowing", "Fall of Dragonstone", "Fall of King's Landing",
    "Death of Rhaenyra", "Death of Lucerys Velaryon", "Death of Viserys I",
    "Hour of the Wolf", "First Battle of Tumbleton", "Second Battle of Tumbleton",
    "Battle of the Gullet", "Battle of the Honeywine", "Red Sowing",
    "Aemond's march on Harrenhal", "Daughter's War", "the Dragon's Wroth",
]

ROLE_TYPES = {"AGENT_IN", "VICTIM_IN", "WITNESS_IN", "COMMANDS_IN",
              "PARTICIPATES_IN", "FIGHTS_IN", "ATTENDS", "OFFICIATES", "HONORED_AT"}
CAUSAL = {"CAUSES", "TRIGGERS", "MOTIVATES", "ENABLES"}

alias = json.loads((REPO / "working/wiki/data/all-node-alias-lookup.json").read_text())
# alias maps normalized phrase -> slug or {slug,...}; normalize like resolver: lower, strip
def norm(s):
    return re.sub(r"\s+", " ", s.lower().strip())

# build slug -> file map
slug_file = {}
for p in (REPO / "graph/nodes").rglob("*.node.md"):
    slug_file[p.name[:-8]] = p

def resolve_name(name):
    n = norm(name)
    v = alias.get(n)
    if isinstance(v, str) and v in slug_file:
        return v
    if isinstance(v, dict):
        s = v.get("slug")
        if s in slug_file:
            return s
    if isinstance(v, list) and v:
        s = v[0] if isinstance(v[0], str) else v[0].get("slug")
        if s in slug_file:
            return s
    # slug guesses
    g = re.sub(r"[^a-z0-9]+", "-", n).strip("-")
    for cand in (g, g.replace("-i-", "-1-"), "the-" + g, g + "-targaryen"):
        if cand in slug_file:
            return cand
    # relaxed: any slug containing all tokens
    toks = [t for t in g.split("-") if t not in ("the", "of", "i", "ii", "iii")]
    hits = [s for s in slug_file if all(t in s for t in toks)]
    return hits[0] if len(hits) == 1 else (hits if hits else None)

# edge stats
by_slug_roles = defaultdict(int)
by_slug_causal = defaultdict(int)
by_slug_deg = defaultdict(int)
with open(REPO / "graph/edges/edges.jsonl") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        e = json.loads(line)
        t, s, tg = e.get("edge_type"), e.get("source_slug"), e.get("target_slug")
        by_slug_deg[s] += 1
        by_slug_deg[tg] += 1
        if t in ROLE_TYPES:
            by_slug_roles[tg] += 1
            by_slug_roles[s] += 1  # person side counts too
        if t in CAUSAL:
            by_slug_causal[s] += 1
            by_slug_causal[tg] += 1

def quotes_and_prose(slug):
    text = slug_file[slug].read_text()
    q = sum(1 for ln in text.splitlines() if ln.lstrip().startswith(">"))
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    prose = len([ln for ln in body.splitlines() if ln.strip() and not ln.startswith(("#", ">"))])
    return q, prose

def report(names, label):
    print(f"\n=== {label} ===")
    print(f"{'name':<32} {'slug':<42} {'deg':>4} {'role':>4} {'caus':>4} {'quo':>4} {'prose':>5}")
    gaps = []
    for name in names:
        r = resolve_name(name)
        if r is None or isinstance(r, list):
            extra = f" (multi: {r[:3]})" if isinstance(r, list) else ""
            print(f"{name:<32} {'*** NO NODE ***' + extra}")
            gaps.append((name, "no-node" if r is None else f"ambiguous:{r[:4]}"))
            continue
        q, prose = quotes_and_prose(r)
        deg, ro, ca = by_slug_deg[r], by_slug_roles[r], by_slug_causal[r]
        mark = ""
        if q == 0:
            mark += " NOQUOTES"
        if ro == 0:
            mark += " NOROLES"
        if ca == 0:
            mark += " NOCAUSAL"
        print(f"{name:<32} {r:<42} {deg:>4} {ro:>4} {ca:>4} {q:>4} {prose:>5}{mark}")
        if q == 0 or deg <= 2:
            gaps.append((name, f"thin (deg={deg}, quotes={q})"))
    return gaps

g1 = report(PEOPLE, "HotD PEOPLE")
g2 = report(DRAGONS, "DRAGONS")
g3 = report(EVENTS, "DANCE EVENTS")

print("\n=== GAP SUMMARY ===")
for name, why in g1 + g2 + g3:
    print(f"  {name}: {why}")
