#!/usr/bin/env python3
"""A2.5 WO5K-battles PASS 3 baseline edge pull (S166) — dedup the existing web before proposing.

PASS 3 cut = THE UNRAVELLING:
  (A) the Spicer-betrayal MECHANISM revealed in AFFC (affc-jaime-05/07): Tywin set the terms,
      Sybell betrayed Robb, Jeyne was bait + kept barren, Rolph rewarded with Castamere.
  (B) the ARMY-THINNING losses that gut Robb's host before the Red Wedding: the Battle of
      Duskendale (Robett Glover & Helman Tallhart, ordered by Roose Bolton) + the Battle of
      the Ruby Ford / the Fords (Roose Bolton vs Tywin at the Trident) -> Roose's pre-RW defection.
  These wire into the B1 RW-upstream spine (already built).

DEDUP HOT ZONES (LIVE — do NOT re-mint):
  - The MARRIAGE SPINE is built (storming-of-the-crag ENABLES robb-weds-jeyne-westerling,
    robb-weds-jeyne-westerling TRIGGERS red-wedding-conspiracy, etc.).
  - The Spicer-trap whodunit is partly wired: grey-wind OPPOSES rolph-spicer +
    sybell-spicer CONSPIRES_WITH tywin-lannister already EXIST.
  - PASS-1/2 hubs (whispering-wood, camps, king-in-the-north, oxcross, ashemark, the-crag).

NODE-DUP MINEFIELD (the Fords/Duskendale cluster — RESOLVE which slug is canonical, do NOT
  create a 5th duplicate). Known same_as redirects:
    battle-of-the-fords-of-the-trident  --same_as--> fighting-at-the-fords-of-the-trident
    battle-of-the-ruby-ford             --same_as--> fighting-at-the-fords-of-the-trident
  Open question: battle-of-the-fords (299 AC, NO same_as) vs fighting-at-the-fords-of-the-trident.
  first-lannister-attack-on-the-ford-daytime = ACOK Catelyn VI (Edmure/Tywin Red-Fork fords) —
    likely a DIFFERENT battle from the ASOS Roose/Ruby-Ford fight.

EXCLUDES TWOW. Only the 5 published books.
"""
import json, collections, pathlib

EDGES = pathlib.Path("graph/edges/edges.jsonl")
CAUSAL = {"CAUSES", "TRIGGERS", "MOTIVATES", "ENABLES"}

EVENTS = {
    # Spicer / marriage / RW-upstream spine
    "robb-weds-jeyne-westerling",
    "robb-receives-false-news-of-brans-death",
    "red-wedding-conspiracy", "red-wedding", "red-wedding-revealed",
    "storming-of-the-crag",
    "grey-wind-killed-at-the-twins",
    "karstark-host-deserts-robb",
    "execution-of-rickard-karstark",
    # the army-thinning losses — the Fords/Duskendale dedup minefield
    "battle-at-duskendale", "sack-of-duskendale", "defiance-of-duskendale",
    "battle-of-the-fords", "battle-of-the-fords-of-the-trident",
    "battle-of-the-ruby-ford", "fighting-at-the-fords-of-the-trident",
    "first-lannister-attack-on-the-ford-daytime",
    # PASS-1/2 antecedent hubs (wire FROM, do NOT rebuild)
    "battle-in-the-whispering-wood", "battle-of-the-camps",
    "robb-proclaimed-king-in-the-north", "battle-of-oxcross", "taking-of-ashemark",
}
CAST = {
    "sybell-spicer", "rolph-spicer", "samwell-spicer",
    "jeyne-westerling", "raynald-westerling", "rollam-westerling", "gawen-westerling",
    "tywin-lannister", "kevan-lannister", "jaime-lannister", "gregor-clegane",
    "robb-stark", "grey-wind", "catelyn-stark",
    "roose-bolton", "robett-glover", "helman-tallhart", "rickard-karstark",
    "walder-frey", "randyll-tarly",
}
PLACES = {"castamere", "crag", "ruby-ford", "duskendale", "twins", "the-twins"}
TITLES = {"lord-of-castamere", "lord-of-the-crag"}
HOUSES = {"house-spicer", "house-westerling", "house-bolton", "house-frey",
          "house-lannister", "house-stark", "house-glover", "house-tallhart", "house-karstark"}
CORE = EVENTS | CAST | PLACES | TITLES | HOUSES

node_files = {p.stem.replace(".node", "") for p in pathlib.Path("graph/nodes").rglob("*.node.md")
              if "_conflicts" not in p.parts and "_unclassified" not in p.parts}
missing = sorted(s for s in CORE if s not in node_files)

edges = [json.loads(l) for l in EDGES.read_text().splitlines() if l.strip()]


def key(e):
    return (e.get("source_slug"), e.get("edge_type"), e.get("target_slug"))


internal, causal_internal = [], []
deg_out = collections.Counter(); deg_in = collections.Counter()
cdeg_out = collections.Counter(); cdeg_in = collections.Counter()
boundary = collections.Counter()
boundary_edges = collections.defaultdict(list)
seen = set()
for e in edges:
    s, t, et = e.get("source_slug"), e.get("target_slug"), e.get("edge_type")
    if s in CORE and t in CORE:
        k = key(e)
        if k in seen:
            continue
        seen.add(k)
        internal.append(e)
        deg_out[s] += 1; deg_in[t] += 1
        if et in CAUSAL:
            causal_internal.append(e)
            cdeg_out[s] += 1; cdeg_in[t] += 1
    elif s in CORE or t in CORE:
        core_node = s if s in CORE else t
        boundary[core_node] += 1
        boundary_edges[core_node].append(e)
        if s in CORE: deg_out[s] += 1
        if t in CORE: deg_in[t] += 1

print("=" * 78)
print(f"CORE slugs WITHOUT a live node file ({len(missing)}) — candidates to BUILD if load-bearing:")
print("  " + (", ".join(missing) if missing else "(none)"))
print("=" * 78)
print()
print(f"INTERNAL EDGES (both endpoints in core): {len(internal)} unique")
print("=" * 78)
for e in sorted(internal, key=lambda x: (x.get("source_slug") or "", x.get("edge_type") or "")):
    print(f"  {e.get('source_slug')}  [{e.get('edge_type')}]  {e.get('target_slug')}  | {e.get('confidence_tier','')}")

print()
print("=" * 78)
print(f"CAUSAL INTERNAL SUB-WEB: {len(causal_internal)}")
print("=" * 78)
for e in sorted(causal_internal, key=lambda x: (x.get("edge_type"), x.get("source_slug") or "")):
    print(f"  {e.get('source_slug')}  [{e.get('edge_type')}]  {e.get('target_slug')}")

print()
print("=" * 78)
print("EVENT-NODE causal degree (cOut/cIn) — 0/0 = causally ISLANDED hub (gap candidate)")
print("=" * 78)
for n in sorted(EVENTS):
    o, i = cdeg_out.get(n, 0), cdeg_in.get(n, 0)
    to, ti = deg_out.get(n, 0), deg_in.get(n, 0)
    flag = "  <-- CAUSALLY ISLANDED" if (o + i) == 0 else ""
    exists = "   [NO node file]" if n in missing else ("   [0 edges in core]" if (to + ti) == 0 else "")
    print(f"  {n:42s} cOut={o:2d} cIn={i:2d}  (tot out={to:2d} in={ti:2d}){flag}{exists}")

print()
print("=" * 78)
print("CAST/TITLE/HOUSE degree (out/in within core + boundary)")
print("=" * 78)
for n in sorted(CAST | TITLES | HOUSES | PLACES):
    o, i, b = deg_out.get(n, 0), deg_in.get(n, 0), boundary.get(n, 0)
    miss = "  [NO node file]" if n in missing else ""
    print(f"  {n:36s} core_out={o:2d} core_in={i:2d}  boundary={b:3d}{miss}")

# Surface the FULL edge list for the most dedup-sensitive battle nodes
print()
print("=" * 78)
print("FULL EDGE DUMP for the Fords/Duskendale dedup minefield + Spicer entities")
print("=" * 78)
focus = ["battle-of-the-fords", "battle-of-the-fords-of-the-trident", "battle-of-the-ruby-ford",
         "fighting-at-the-fords-of-the-trident", "first-lannister-attack-on-the-ford-daytime",
         "battle-at-duskendale", "sack-of-duskendale", "defiance-of-duskendale",
         "roose-bolton", "robett-glover", "helman-tallhart",
         "sybell-spicer", "rolph-spicer", "jeyne-westerling", "raynald-westerling",
         "lord-of-castamere", "castamere"]
for fn in focus:
    rows = [e for e in edges if e.get("source_slug") == fn or e.get("target_slug") == fn]
    print(f"\n--- {fn}  ({len(rows)} edges) ---")
    for e in rows:
        d = "OUT" if e.get("source_slug") == fn else " IN"
        other = e.get("target_slug") if d == "OUT" else e.get("source_slug")
        print(f"  [{d}] {e.get('edge_type'):20s} {other:42s} | {e.get('confidence_tier','')} | {e.get('evidence_chapter','')}")
