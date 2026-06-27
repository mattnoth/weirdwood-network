#!/usr/bin/env python3
"""D5 Arya/Harrenhal baseline edge pull — dedup the existing internal web before proposing."""
import json, collections, pathlib

EDGES = pathlib.Path("graph/edges/edges.jsonl")

CORE = {
    # event hubs / beats
    "fight-at-the-holdfast", "arya-captured", "gendry-captured", "arya-frees-the-prisoners",
    "lommy-yields-and-is-killed", "arya-gives-water-to-the-prisoners", "praed-s-death-and-burial",
    "chiswyck-dies-three-days-later", "guards-killed", "ser-amory-lorch-executed",
    "ser-amory-receives-the-prisoners", "fall-of-harrenhal", "capture-of-harrenhal",
    "burning-of-harrenhal", "death-of-mycah", "incident-at-the-trident",
    # cast
    "arya-stark", "yoren", "jaqen-hghar", "rorge", "biter", "gendry", "hot-pie",
    "lommy-greenhands", "weasel", "weese", "tickler", "chiswyck", "polliver", "rafford",
    "dunsen", "amory-lorch", "vargo-hoat", "gregor-clegane", "roose-bolton", "mycah",
    "cutjack", "dobber", "caged-northmen", "two-betrayers", "shagwell", "harwin",
    # places / artifacts
    "harrenhal", "gods-eye", "inn-at-the-crossroads", "holdfast", "needle", "iron-coin",
}

edges = [json.loads(l) for l in EDGES.read_text().splitlines() if l.strip()]

def key(e):
    return (e.get("source_slug"), e.get("edge_type"), e.get("target_slug"))

internal, boundary = [], collections.defaultdict(list)
deg_out = collections.Counter(); deg_in = collections.Counter()
seen = set()
for e in edges:
    s, t = e.get("source_slug"), e.get("target_slug")
    if s in CORE and t in CORE:
        k = key(e)
        if k in seen: continue
        seen.add(k)
        internal.append(e)
        deg_out[s]+=1; deg_in[t]+=1
    elif s in CORE or t in CORE:
        core_node = s if s in CORE else t
        boundary[core_node].append(e)
        if s in CORE: deg_out[s]+=1
        if t in CORE: deg_in[t]+=1

print("="*70)
print(f"INTERNAL EDGES (both endpoints in core set): {len(internal)} unique")
print("="*70)
for e in sorted(internal, key=lambda x:(x.get("source_slug") or "", x.get("edge_type") or "")):
    q = (e.get("evidence_quote") or e.get("quote") or "")[:55]
    print(f"  {e.get('source_slug')}  [{e.get('edge_type')}]  {e.get('target_slug')}  | {e.get('confidence','')}")

print()
print("="*70)
print("DEGREE per core node (out / in) — dead-ends (0/x or x/0) are gap candidates")
print("="*70)
for n in sorted(CORE):
    o, i = deg_out.get(n,0), deg_in.get(n,0)
    flag = "  <-- DEAD-END" if (o==0 or i==0) else ""
    exists = "" if (o or i) else "   [no edges at all]"
    print(f"  {n:45s} out={o:2d} in={i:2d}{flag}{exists}")
