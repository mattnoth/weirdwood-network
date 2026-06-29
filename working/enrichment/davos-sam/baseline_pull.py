#!/usr/bin/env python3
"""A2.8 Davos / Sam residual baseline edge pull (S167) — the LAST A-roundup unit.

Heavy dedup expected: both halves are Stannis/Jon-adjacent and substantially pre-wired.
  HALF A (Davos): Blackwater near-death -> washed up -> rescued by Salladhor/Khorane;
    the Manderly mission (White Harbor -> imprisoned -> Wyman's STAGED execution -> Skagos/Rickon).
    DEDUP HARD vs the S93 Wyman/Davos deception spine (4 beats) + the S138 Blackwater cluster.
  HALF B (Sam): the Fist of the First Men (Others' attack / Great Ranging retreat);
    Craster's-Keep mutiny + Gilly/baby/Coldhands flight; the Citadel road (Sam/Gilly/Aemon to
    Oldtown via Braavos, Aemon's death) -- this last leg is likely UNBUILT -> build+enrich.
    DEDUP vs fight-at-the-fist / battle-of-the-fist-of-the-first-men (KNOWN DUP — resolve canonical).

EXCLUDES TWOW. Only the 5 published books.
"""
import json, collections, pathlib

EDGES = pathlib.Path("graph/edges/edges.jsonl")
CAUSAL = {"CAUSES", "TRIGGERS", "MOTIVATES", "ENABLES"}

DAVOS_EVENTS = {
    "battle-of-the-blackwater", "wildfire-trap-on-the-blackwater",
    "execution-of-the-blackwater-deserters", "blackwater-chain-boom",
    "leeching-of-edric-storm",
    # the Manderly mission deception spine (S93) — wire FROM, do NOT rebuild
    "davos-seaworth-captured", "ser-axell-florent-arrests-davos",
    "wyman-publicly-arrests-davos-at-white-harbor", "wyman-publicly-orders-davos-execution",
    "wyman-manderly-stages-fake-execution-of-davos", "execution-of-davos-lookalike-at-white-harbor",
    "frey-witnesses-attest-davos-dead-at-small-council", "learning-about-manderly-s-hostage",
    "manderly-bakes-the-frey-pies", "ser-wendel-manderly-is-killed",
    # candidate new beats (likely missing)
    "davos-rescued-after-the-blackwater", "davos-sent-to-fetch-rickon-from-skagos",
}
SAM_EVENTS = {
    "fight-at-the-fist", "battle-of-the-fist-of-the-first-men", "great-ranging",
    "mutiny-at-crasters-keep", "mutiny-at-castle-black", "bran-meets-coldhands",
    # candidate new beats (Citadel road — likely missing)
    "death-of-maester-aemon", "sam-and-gilly-reach-oldtown",
    "sam-kills-the-other", "coldhands-rescues-sam-and-gilly",
}
EVENTS = DAVOS_EVENTS | SAM_EVENTS

DAVOS_CAST = {
    "davos-seaworth", "salladhor-saan", "khorane-sathmantes", "stannis-baratheon",
    "melisandre", "axell-florent", "imry-florent",
    "wyman-manderly", "wylis-manderly", "wendel-manderly", "marlon-manderly", "bartimus",
    "robett-glover", "rickon-stark", "edric-storm", "osha",
    "devan-seaworth", "dale-seaworth", "allard-seaworth", "maric-seaworth", "matthos-seaworth",
    "marya-seaworth",
}
SAM_CAST = {
    "samwell-tarly", "gilly", "gillys-mother", "craster", "crasters-sons", "crasters-wives",
    "aemon-targaryen-son-of-maekar-i", "aemon-targaryen", "coldhands", "jon-snow",
    "jeor-mormont", "dareon", "mance-rayder", "grenn", "small-paul", "chett",
    "bowen-marsh",
}
CAST = DAVOS_CAST | SAM_CAST

PLACES = {
    "white-harbor", "dragonstone", "skagos", "the-wolfs-den", "wolfs-den",
    "blackwater-rush", "blackwater-bay", "kings-landing",
    "the-fist-of-the-first-men", "crasters-keep", "the-wall", "castle-black",
    "oldtown", "the-citadel", "braavos", "eastwatch-by-the-sea", "eastwatch",
}
HOUSES = {"house-manderly", "house-seaworth", "house-baratheon-of-dragonstone",
          "house-tarly", "house-stark", "nights-watch"}
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
    print(f"  {n:48s} cOut={o:2d} cIn={i:2d}  (tot out={to:2d} in={ti:2d}){flag}{exists}")

print()
print("=" * 78)
print("CAST/HOUSE/PLACE degree (out/in within core + boundary)")
print("=" * 78)
for n in sorted(CAST | HOUSES | PLACES):
    o, i, b = deg_out.get(n, 0), deg_in.get(n, 0), boundary.get(n, 0)
    miss = "  [NO node file]" if n in missing else ""
    print(f"  {n:40s} core_out={o:2d} core_in={i:2d}  boundary={b:3d}{miss}")

print()
print("=" * 78)
print("FULL EDGE DUMP for dedup-sensitive nodes (the two Fist dups + Davos beats + key cast)")
print("=" * 78)
focus = ["fight-at-the-fist", "battle-of-the-fist-of-the-first-men", "great-ranging",
         "mutiny-at-crasters-keep", "bran-meets-coldhands",
         "davos-seaworth", "khorane-sathmantes", "salladhor-saan",
         "wyman-manderly-stages-fake-execution-of-davos", "rickon-stark",
         "samwell-tarly", "gilly", "coldhands", "aemon-targaryen-son-of-maekar-i", "aemon-targaryen",
         "craster", "dareon"]
for fn in focus:
    rows = [e for e in edges if e.get("source_slug") == fn or e.get("target_slug") == fn]
    print(f"\n--- {fn}  ({len(rows)} edges) ---")
    for e in rows:
        d = "OUT" if e.get("source_slug") == fn else " IN"
        other = e.get("target_slug") if d == "OUT" else e.get("source_slug")
        print(f"  [{d}] {e.get('edge_type'):20s} {other:46s} | {e.get('confidence_tier','')} | {e.get('evidence_chapter','')}")
