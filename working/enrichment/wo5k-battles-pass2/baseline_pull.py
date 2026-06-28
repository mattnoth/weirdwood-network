#!/usr/bin/env python3
"""A2.5 WO5K-battles PASS 2 baseline edge pull (S164) — dedup the existing web before proposing.

PASS 2 cut = THE WESTERLANDS RAID:
  Robb carries the war west past the Golden Tooth into the Lannister heartland:
  Oxcross (the night victory over Stafford's green host) -> the raid (Ashemark, the gold
  mines, the burning coast) -> the storming of the Crag (Gawen Westerling's seat) -> (EXISTING)
  the Jeyne-Westerling marriage blunder -> (EXISTING) the Red-Wedding-upstream spine.

This is the LAST A-roundup unit's MULTI-PASS mini-track:
  PASS 1 (S163, DONE): Robb's Riverlands-relief rise (Whispering Wood + Camps + king-in-the-north).
  PASS 2 (this dip):   the Westerlands raid (Oxcross / Ashemark / the Crag / the marriage seam).
  PASS 3 (deferred):   the unravelling (the Fords / Duskendale -> the Red-Wedding upstream).

DEDUP HOT ZONES (do NOT re-mint -- these are LIVE):
  - robb-weds-jeyne-westerling: the B1 RW-upstream MARRIAGE SPINE IS BUILT.
    `storming-of-the-crag ENABLES robb-weds-jeyne-westerling`,
    `robb-receives-false-news-of-brans-death TRIGGERS robb-weds-jeyne-westerling`,
    `robb-weds-jeyne-westerling TRIGGERS red-wedding-conspiracy` all EXIST. DEDUP HARD.
    PASS-2 value = wire the BATTLE/raid HALF *into* this spine; do NOT rebuild marriage->RW.
  - robb-proclaimed-king-in-the-north / battle-of-the-camps / battle-in-the-whispering-wood:
    PASS-1 hubs. The relief-rise is the causal ANTECEDENT of the westward war -- wire FROM it,
    do NOT rebuild it. (battle-in-the-whispering-wood carries the PASS-1 gawen-westerling seam.)

KEY GAPS (aim here):
  - battle-of-oxcross is CAUSALLY ISLANDED (0 upstream + 0 downstream causal edges; only
    PART_OF + PRECEDES). Wire its causal IN (the relief-rise/king-in-the-north ENABLES the
    westward war -> Oxcross) and its causal OUT (Oxcross ENABLES the raid -> the Crag).
  - taking-of-ashemark is ALSO causally islanded (only PART_OF + PRECEDES noise) -- the raid beat.
  - storming-of-the-crag has its ENABLES-OUT to the marriage but NO causal IN, and is roster-EMPTY
    (4 edges, no participants). Its wiki prose is rich (Smalljon + Black Walder scaling parties,
    Robb's ram + arrow wound, Grey Wind's kill, Rolph Spicer the castellan) but BOOK-uncited.
    This is the PASS-1 Whispering-Wood pattern: convert wiki-cited prose -> BOOK-cited edges.

NODE-DUP FLAG (NOT this dip's job -- small-fix): `black-walder-frey` AND `walder-frey-son-of-ryman`
  (alias "Black Walder") are twins. Target the wiki-canonical, alias-bearing `walder-frey-son-of-ryman`.
The Smalljon = `jon-umber-son-of-jon` (aliases "The Smalljon"/"Smalljon Umber").
`harrying-of-the-stony-shore` is the IRONBORN raid on the North -- the oxcross PRECEDES it edge is
  temporal noise; EXCLUDE it from the Westerlands raid.

EXCLUDES TWOW. Only the 5 published books.
Dumps: INTERNAL edges (both endpoints in core), the CAUSAL sub-web, per-node degree w/ islanded flags.
"""
import json, collections, pathlib

EDGES = pathlib.Path("graph/edges/edges.jsonl")
CAUSAL = {"CAUSES", "TRIGGERS", "MOTIVATES", "ENABLES"}

EVENTS = {
    # the PASS-2 raid cluster
    "battle-of-oxcross",                  # CAUSALLY ISLANDED -- the fix
    "taking-of-ashemark",                 # CAUSALLY ISLANDED -- the raid beat
    "storming-of-the-crag",               # roster-EMPTY + no causal IN -- the marquee enrich
    # the BUILT marriage spine -- DEDUP HARD
    "robb-weds-jeyne-westerling",
    "robb-receives-false-news-of-brans-death",
    "red-wedding-conspiracy",
    # PASS-1 antecedents (wire FROM, do NOT rebuild)
    "robb-proclaimed-king-in-the-north",
    "battle-of-the-camps",
    "battle-in-the-whispering-wood",
    # ironborn noise (exclude from the raid; pull for PRECEDES awareness)
    "harrying-of-the-stony-shore",
}
CAST = {
    "robb-stark", "grey-wind", "rickard-karstark", "stafford-lannister", "martyn-lannister",
    "stevron-frey", "lymond-vikary",
    "jon-umber", "jon-umber-son-of-jon", "walder-frey-son-of-ryman", "black-walder-frey",
    "jeyne-westerling", "gawen-westerling", "sybell-spicer", "rolph-spicer",
    "raynald-westerling", "rollam-westerling",
    "tywin-lannister", "kevan-lannister", "jaime-lannister",
}
PLACES = {
    "crag", "oxcross", "ashemark", "casterly-rock", "lannisport", "golden-tooth",
    "castamere", "stone-mill",
}
HOUSES = {"house-westerling", "house-spicer", "house-lannister", "house-stark"}
CORE = EVENTS | CAST | PLACES | HOUSES

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
print(f"CORE slugs WITHOUT a live node file ({len(missing)}) — candidates to BUILD if load-bearing:")
print("  " + (", ".join(missing) if missing else "(none — all core slugs resolve to live nodes)"))
print("=" * 78)
print()
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
    exists = "   [NO node file]" if n in missing else ("   [0 edges in core]" if (to + ti) == 0 else "")
    print(f"  {n:42s} cOut={o:2d} cIn={i:2d}  (tot out={to:2d} in={ti:2d}){flag}{exists}")

print()
print("=" * 78)
print("CAST/PLACE/HOUSE degree (out/in within core + boundary)")
print("=" * 78)
for n in sorted(CAST | PLACES | HOUSES):
    o, i, b = deg_out.get(n, 0), deg_in.get(n, 0), boundary.get(n, 0)
    miss = "  [NO node file]" if n in missing else ""
    print(f"  {n:28s} core_out={o:2d} core_in={i:2d}  boundary={b:3d}{miss}")
