#!/usr/bin/env python3
"""A2.6 Jaime / Riverlands baseline edge pull (S159) — dedup the existing internal web before proposing.

Jaime is a saturated POV (156 out-edges) with a dense dyad web, but his AFFC Riverlands COMMAND
event-layer is thin/islanded. The siege-of-riverrun hub already has 13 incoming (S100 historical-anchor
+ AFFC role wiring) but its RESOLUTION (Edmure's surrender, the Blackfish's escape) is UNBUILT, and the
Cersei-letter rupture has no node. This is a BUILD + ENRICH with a HEAVY dedup.

DEDUP HOT ZONES (do NOT re-mint — these are LIVE):
  - S100 siege-of-riverrun historical-anchor wave (the 13-edge hub web below)
  - S141 Brienne→Stoneheart arc (oathkeeper WIELDED_IN brienne's fights; the Saltpans/hound-helm thread)
  - S142 Sack-of-KL wildfire thread (wildfire-plot, aerys-commands-the-city-burned, jaime KILLS belis/garigus,
    jaime-found-seated-on-the-iron-throne, the throne-tableau witnesses)
  - S109 Tywin's-death (jaime-frees-tyrion-from-the-black-cells, jaime-reveals-the-truth-of-tysha)

EXCLUDES TWOW. Only the 5 published books.

Dumps: INTERNAL edges (both endpoints in core), the CAUSAL sub-web, per-node degree w/ islanded flags,
boundary counts.
"""
import json, collections, pathlib

EDGES = pathlib.Path("graph/edges/edges.jsonl")
CAUSAL = {"CAUSES", "TRIGGERS", "MOTIVATES", "ENABLES"}

# ── CORE node set (Jaime's Riverlands command + the Riverrun siege + Harrenhal + ASOS backstory) ──
EVENTS = {
    # Riverrun siege + its resolution (the marquee — resolution mostly UNBUILT)
    "siege-of-riverrun", "jaime-orders-siege-equipment-and-gallows-burned",
    "karstark-murders-prisoners-at-riverrun", "battle-under-the-walls-of-riverrun",
    "battle-of-the-camps", "jaime-demands-the-red-wedding-captives", "jaime-lies-about-cleos-s-death",
    # Jaime's wider AFFC Riverlands tour
    "siege-of-raventree", "siege-of-darry", "siege-of-seagard", "hostage-negotiation",
    "gregor-raids-the-riverlands",
    # Harrenhal cluster
    "capture-of-harrenhal", "fall-of-harrenhal", "yielding-of-harrenhal", "burning-of-harrenhal",
    "assault-on-harrenhal", "arya-escapes-harrenhal", "aemonds-march-on-harrenhal",
    # Upstream causes already wired
    "red-wedding", "edmure-taken-hostage-at-the-twins", "war-of-the-five-kings",
    # ASOS backstory (DEDUP vs S141/S142/S109 — included to surface what is already wired)
    "slaying-of-aerys-ii-the-kingslaying", "jaime-found-seated-on-the-iron-throne", "wildfire-plot",
    "aerys-commands-the-city-burned", "jaime-frees-tyrion-from-the-black-cells",
    "jaime-reveals-the-truth-of-tysha", "sack-of-kings-landing", "jaime-s-kills-are-revealed",
}
CAST = {
    "jaime-lannister", "edmure-tully", "brynden-tully", "cersei-lannister", "brienne-tarth",
    "tyrion-lannister",
    # Lannister host / officers
    "daven-lannister", "addam-marbrand", "lancel-lannister", "ilyn-payne", "genna-lannister",
    "strongboar", "lyle-crakehall",
    # Freys at Riverrun / the Twins
    "ryman-frey", "edwyn-frey", "walder-frey", "emmon-frey", "cleos-frey", "walder-rivers",
    # Riverlords / Tully cause
    "tytos-blackwood", "jonos-bracken", "hoster-tully", "desmond-grell", "robin-ryger",
    "jeyne-westerling", "vargo-hoat", "pia",
}
PLACES_ARTIFACTS = {
    "riverrun", "harrenhal", "raventree-hall", "riverlands", "great-hall-of-riverrun",
    "godswood-of-riverrun", "the-twins", "darry", "seagard",
    "oathkeeper", "ice", "widows-wail",
    "house-tully", "house-frey", "house-lannister", "house-blackwood", "house-bracken",
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
    flag = "  <-- CAUSALLY ISLANDED" if (o + i) == 0 else ""
    exists = "   [NO edges at all in core]" if (to + ti) == 0 else ""
    print(f"  {n:48s} cOut={o:2d} cIn={i:2d}  (tot out={to:2d} in={ti:2d}){flag}{exists}")

print()
print("=" * 78)
print("CAST/PLACE degree (out/in within core + boundary)")
print("=" * 78)
for n in sorted(CAST | PLACES_ARTIFACTS):
    o, i, b = deg_out.get(n, 0), deg_in.get(n, 0), boundary.get(n, 0)
    print(f"  {n:36s} core_out={o:2d} core_in={i:2d}  boundary={b:3d}")
