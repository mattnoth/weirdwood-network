#!/usr/bin/env python3
"""A1.5 Dorne / Queenmaker baseline edge pull (S156) — dedup the existing internal web before proposing.

The Dorne spine was BUILT S117 (the Queenmaker plot, rooted cross-book at Oberyn's death) but has had
**0 enrichment dips** — and 19 harvest rows were already pushed S117. So this is WIRE + ENRICH on a thin
causal spine + an under-wired conspirator web. The dedup is EXPECTED to kill several lens proposals (the
S117 spine already wired arianne/arys/darkstar AGENT_IN the plot, myrcella VICTIM_IN, the ambush chain,
arianne WITNESS_IN the maiming).

Dumps:
  - INTERNAL edges (both endpoints in the core set), unique
  - CAUSAL sub-web (CAUSES/TRIGGERS/MOTIVATES/ENABLES) within the core — to find causally-islanded hubs
  - DEGREE per core node (out/in) with dead-end flags
  - BOUNDARY edge counts (one endpoint in core)

EXCLUDES historical-conquest + TWOW nodes (conquest-of-dorne, *-dornish-war, defenestration-of-sunspear,
arianne-{i,ii}-the-winds-of-winter) — only the 5 published books are in scope.
"""
import json, collections, pathlib

EDGES = pathlib.Path("graph/edges/edges.jsonl")
CAUSAL = {"CAUSES", "TRIGGERS", "MOTIVATES", "ENABLES"}

# ── CORE node set (published Dorne arc only) ─────────────────────────────────
EVENTS = {
    # The Queenmaker plot + its collapse (AFFC)
    "the-queenmaker-plot", "areo-hotah-springs-the-ambush",
    "arianne-collapses-and-is-captured", "myrcella-is-maimed-by-darkstar",
    "arrest-of-the-sand-snakes",
    # Doran's long game (ADWD) + cross-arc roots
    "doran-reveals-fire-and-blood-pact", "gregor-confesses-and-kills-oberyn",
    "death-of-quentyn-martell", "quentyn-orders-the-attack", "quentyn-contracts-tattered-prince",
}
CAST = {
    # Conspiracy core
    "arianne-martell", "arys-oakheart", "gerold-dayne", "andrey-dalt", "sylva-santagar",
    "obara-sand", "nymeria-sand", "tyene-sand", "sand-snakes", "ellaria-sand",
    # Sunspear court
    "doran-martell", "areo-hotah", "trystane-martell", "caleotte", "ricasso", "manfrey-martell",
    "gascoyne-of-the-greenblood", "oberyn-martell", "quentyn-martell",
    # Outside players (the captives / kin / cross-arc)
    "myrcella-baratheon", "balon-swann", "cersei-lannister", "tommen-baratheon",
    "jaime-lannister", "tywin-lannister", "gregor-clegane",
    "daenerys-targaryen", "aegon-targaryen",
}
PLACES_ARTIFACTS = {
    "sunspear", "water-gardens", "old-palace", "greenblood", "high-hermitage", "ghaston-grey",
    "dorne", "sea-of-dorne", "iron-throne",
    "house-martell", "house-dayne-of-high-hermitage", "house-santagar", "orphans-of-the-greenblood",
    "oberyn-spear", "princess-myrcella",
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
    print(f"  {n:46s} cOut={o:2d} cIn={i:2d}  (tot out={to:2d} in={ti:2d}){flag}{exists}")

print()
print("=" * 78)
print("CAST/PLACE degree (out/in within core + boundary)")
print("=" * 78)
for n in sorted(CAST | PLACES_ARTIFACTS):
    o, i, b = deg_out.get(n, 0), deg_in.get(n, 0), boundary.get(n, 0)
    print(f"  {n:42s} core_out={o:2d} core_in={i:2d}  boundary={b:3d}")
