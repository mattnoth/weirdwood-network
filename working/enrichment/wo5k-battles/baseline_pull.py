#!/usr/bin/env python3
"""A2.5 WO5K-battles baseline edge pull (S163, PASS 1) — dedup the existing web before proposing.

PASS 1 cut = Robb's Riverlands-relief rise:
  the Whispering Wood (Jaime captured) -> the Battle of the Camps (Riverrun relieved)
  -> the seam into robb-proclaimed-king-in-the-north (the Young Wolf / WO5K Northern front).

This is the LAST A-roundup unit and an explicitly MULTI-PASS mini-track:
  PASS 1 (this dip): Whispering Wood + Battle of the Camps + the king-in-the-north seam.
  PASS 2 (deferred):  the Westerlands raid (Oxcross / the Crag / the Jeyne-Westerling blunder).
  PASS 3 (deferred):  the unravelling (the Fords / Duskendale -> the Red-Wedding upstream).

DEDUP HOT ZONES (do NOT re-mint — these are LIVE):
  - battle-of-the-camps: S100 historical-anchor wave 2 attached 43 edges across 4 hubs. DEDUP HARD.
    Pull in only the islanded Robb-side beats + the causal wiring forward to king-in-the-north.
  - battle-on-the-green-fork: already rich (29 edges). DEDUP — the diversion that drew Tywin off,
    enabling the Whispering Wood. Only the ENABLES seam (green-fork -> whispering-wood) is new.
  - robb-proclaimed-king-in-the-north: S113 causal-track (CAUSES from execution-of-eddard-stark,
    AGENT_IN robb, MOTIVATES). Seam TARGET — wire the battles into it, do NOT rebuild it.
  - siege-of-riverrun: S159 Jaime/Riverlands enriched the AFFC *resolution*. This pass touches the
    AGOT *origin* of the siege (Jaime besieges after the battle under the walls). DEDUP vs S159.
  - the B1 Red-Wedding-upstream spine (Robb's victories -> marriage blunder -> Frey betrayal) is built.

KEY GAP: the Whispering Wood battle has NO live event-hub node. `whispering-wood` is only a thin
place.location (the FOREST). The battle (Robb's 6,000 vs Jaime's host, the night trap, Jaime taken)
is the marquee BUILD this pass -> new node `battle-of-the-whispering-wood` (event.battle).
(NB: a quarantined wiki twin exists in graph/nodes/_conflicts/ but is excluded from index/query/resolver;
minting the live node into events/ is safe.)

EXCLUDES TWOW. Only the 5 published books.

Dumps: INTERNAL edges (both endpoints in core), the CAUSAL sub-web, per-node degree w/ islanded flags.
"""
import json, collections, pathlib

EDGES = pathlib.Path("graph/edges/edges.jsonl")
CAUSAL = {"CAUSES", "TRIGGERS", "MOTIVATES", "ENABLES"}

EVENTS = {
    # PASS-1 battle hubs + seams
    "battle-of-the-camps",                 # S100 — DEDUP HARD
    "robb-proclaimed-king-in-the-north",   # S113 — seam TARGET
    "siege-of-riverrun",                   # S159 — DEDUP (AFFC resolution); AGOT origin is new
    "battle-on-the-green-fork",            # 29 edges — DEDUP; only the ENABLES seam is new
    "execution-of-eddard-stark",           # the CAUSES source of king-in-the-north
    # adjacent battle hubs (PASS 2/3 — pull for awareness, do NOT build this pass)
    "battle-of-oxcross",                   # PASS 2
    "battle-of-the-fords",                 # PASS 3
    # the MARQUEE gap (no live node yet — will be the new build)
    "battle-of-the-whispering-wood",
}
CAST = {
    "robb-stark", "jaime-lannister", "catelyn-stark", "brynden-tully", "jon-umber",
    "rickard-karstark", "maege-mormont", "galbart-glover", "roose-bolton", "tytos-blackwood",
    "edmure-tully", "hoster-tully", "grey-wind", "marq-piper", "karyl-vance", "andros-brax",
    "forley-prester", "tywin-lannister", "stafford-lannister", "kevan-lannister", "harys-swyft",
    "cleos-frey", "walder-frey",
}
PLACES = {
    "riverrun", "twins", "green-fork", "golden-tooth", "tumblestone", "whispering-wood",
    "casterly-rock",
}
CORE = EVENTS | CAST | PLACES

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
print("  " + ", ".join(missing))
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
print("CAST/PLACE degree (out/in within core + boundary)")
print("=" * 78)
for n in sorted(CAST | PLACES):
    o, i, b = deg_out.get(n, 0), deg_in.get(n, 0), boundary.get(n, 0)
    miss = "  [NO node file]" if n in missing else ""
    print(f"  {n:28s} core_out={o:2d} core_in={i:2d}  boundary={b:3d}{miss}")
