#!/usr/bin/env python3
"""A2.7 Stannis baseline edge pull (S155) — dedup the existing internal web before proposing.

Stannis is HEAVILY pre-wired (stannis-baratheon alone: 89 out / 65 in) via the Blackwater (S138)
and NORTH (S125-126) spines — so the dip is WIRE + ENRICH, and the dedup is expected to kill many
lens proposals. This pull dumps:
  - INTERNAL edges (both endpoints in the core set), unique
  - CAUSAL sub-web (CAUSES/TRIGGERS/MOTIVATES/ENABLES) within the core — to find causally-islanded hubs
  - DEGREE per core node (out/in) with dead-end flags
  - BOUNDARY edge counts (one endpoint in core)
"""
import json, collections, pathlib

EDGES = pathlib.Path("graph/edges/edges.jsonl")
CAUSAL = {"CAUSES", "TRIGGERS", "MOTIVATES", "ENABLES"}

# ── CORE node set ────────────────────────────────────────────────────────────
EVENTS = {
    # Renly's war / shadow-baby / Storm's End
    "shadow-assassination-of-renly", "renly-s-death-reflection", "stannis-absorbs-renly-s-host",
    "siege-of-storms-end-299", "siege-of-storms-end-300", "siege-of-storms-end", "taking-of-storms-end",
    "tourney-at-storms-end", "shadow-war", "brienne-asks-to-arm-renly-for-battle",
    "taena-recounts-renly-s-wedding-night", "wedding-of-renly-baratheon-and-margaery-tyrell",
    # Dragonstone / R'hllor
    "assault-on-dragonstone", "siege-of-dragonstone", "fall-of-dragonstone", "flight-to-dragonstone",
    "wedding-of-stannis-baratheon-and-selyse-florent",
    "the-queen-s-faction-urges-sacrifice-of-edric-storm",
    "queen-s-men-begin-calling-for-sacrifice", "queen-s-men-push-stannis-harder-for-sacrifice",
    # Blackwater (mostly built S138 — DO NOT re-touch wildfire)
    "battle-of-the-blackwater", "the-antler-men-conspiracy", "stannis-retreats-to-dragonstone",
    "garlan-tyrell-routs-stannis-as-renly-s-ghost", "wildfire-trap-on-the-blackwater",
    # The Wall + the march (built via NORTH)
    "stannis-moves-to-the-wall", "battle-beneath-the-wall", "mance-rayder-brought-to-execution",
    "stannis-march-on-winterfell", "stannis-s-army-stalls-at-crofters-village",
    "jon-argues-against-the-dreadfort-attack",
    "wedding-of-ramsay-bolton-and-arya-stark",  # MOTIVATES stannis (already wired)
    # Greyjoy rebellion backstory
    "greyjoy-rebellion",
}
CAST = {
    "stannis-baratheon", "melisandre", "renly-baratheon", "davos-seaworth", "shireen-baratheon",
    "selyse-florent", "edric-storm", "mance-rayder", "axell-florent", "alester-florent",
    "salladhor-saan", "cressen", "patchface", "cortnay-penrose", "catelyn-stark", "brienne-tarth",
    "loras-tyrell", "margaery-tyrell", "imry-florent", "guyard-morrigen", "jon-snow",
    "robert-baratheon", "cersei-lannister", "roose-bolton", "tycho-nestoris", "asha-greyjoy",
    "val", "devan-seaworth", "pylos", "guncer-sunglass", "jon-arryn", "justin-massey",
    "godry-farring", "clayton-suggs", "rolland-storm", "arnolf-karstark", "alysane-mormont",
    "mors-umber",
}
PLACES_ARTIFACTS = {
    "dragonstone", "storms-end", "the-wall", "castle-black", "winterfell", "deepwood-motte",
    "cape-wrath", "eastwatch-by-the-sea", "iron-bank-of-braavos", "the-nightfort",
    "lightbringer", "melisandres-ruby", "proudwing", "iron-throne", "rhllor",
    "house-baratheon", "house-baratheon-of-dragonstone", "house-florent", "house-tyrell",
}
CORE = EVENTS | CAST | PLACES_ARTIFACTS

edges = [json.loads(l) for l in EDGES.read_text().splitlines() if l.strip()]


def key(e):
    return (e.get("source_slug"), e.get("edge_type"), e.get("target_slug"))


internal, causal_internal = [], []
deg_out = collections.Counter(); deg_in = collections.Counter()
cdeg_out = collections.Counter(); cdeg_in = collections.Counter()
boundary = collections.Counter()
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
        if s in CORE: deg_out[s] += 1
        if t in CORE: deg_in[t] += 1

print("=" * 78)
print(f"INTERNAL EDGES (both endpoints in core): {len(internal)} unique")
print("=" * 78)
for e in sorted(internal, key=lambda x: (x.get("source_slug") or "", x.get("edge_type") or "")):
    print(f"  {e.get('source_slug')}  [{e.get('edge_type')}]  {e.get('target_slug')}  | {e.get('confidence_tier','')}")

print()
print("=" * 78)
print(f"CAUSAL INTERNAL SUB-WEB (CAUSES/TRIGGERS/MOTIVATES/ENABLES): {len(causal_internal)}")
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
    flag = ""
    if (o + i) == 0:
        flag = "  <-- CAUSALLY ISLANDED"
    exists = "   [NO edges at all in core]" if (to + ti) == 0 else ""
    print(f"  {n:52s} cOut={o:2d} cIn={i:2d}  (tot out={to:2d} in={ti:2d}){flag}{exists}")

print()
print("=" * 78)
print("CAST/PLACE degree (out/in within core + boundary)")
print("=" * 78)
for n in sorted(CAST | PLACES_ARTIFACTS):
    o, i, b = deg_out.get(n, 0), deg_in.get(n, 0), boundary.get(n, 0)
    print(f"  {n:42s} core_out={o:2d} core_in={i:2d}  boundary={b:3d}")
