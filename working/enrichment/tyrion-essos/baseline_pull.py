#!/usr/bin/env python3
"""A2.4 Tyrion / Essos baseline edge pull (S161) — dedup the existing internal web before proposing.

Tyrion is a saturated POV (362 edges) but his ADWD-Essos EVENT spine is likely thin/islanded.
The Shy Maid voyage household + Volantis cast were ALREADY built by the S147 AEGON/Golden Company dip
(shy-maid, haldon, lemore, duck/rolly-duckfield, yandry, ysilla, qavo-nogarys, kasporio, meris,
bridge-of-dream, stone-men-attack-the-shy-maid). The Meereen destination spine was built S144.
This is a BUILD + ENRICH with a HEAVY dedup — pull in only the Tyrion-SIDE beats those dips left islanded.

DEDUP HOT ZONES (do NOT re-mint — these are LIVE):
  - S147 AEGON/Golden Company: the Shy Maid household + fAegon reveal + stone-men-attack-the-shy-maid
  - S144 Daenerys/Meereen: siege-of-meereen, ben-plumm-defects-to-yunkai (the THIRD treason, Dany-side),
    wedding-of-hizdahr, battle-near-yunkai, fall-of-astapor, sons-of-the-harpy web
  - S109/S139 Tywin's-death: assassination-of-tywin, tyrion-kills-shae, trial, jaime-frees-tyrion,
    jaime-reveals-tysha, varys-smuggles-tyrion-out-of-kings-landing (the launch of the exile)

EXCLUDES TWOW. Only the 5 published books. (The Second-Sons-turn-cloaks-BACK is TWOW — node-prose only;
in ADWD Tyrion only JOINS/buys into the company.)

Dumps: INTERNAL edges (both endpoints in core), the CAUSAL sub-web, per-node degree w/ islanded flags.
"""
import json, collections, pathlib

EDGES = pathlib.Path("graph/edges/edges.jsonl")
CAUSAL = {"CAUSES", "TRIGGERS", "MOTIVATES", "ENABLES"}

EVENTS = {
    # Meereen destination + Yunkish siege (S144 — DEDUP)
    "siege-of-meereen", "second-siege-of-meereen", "battle-near-yunkai", "battle-of-yunkai",
    "ben-plumm-defects-to-yunkai", "wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen",
    "fall-of-astapor",
    # Shy Maid voyage (S147 — DEDUP)
    "stone-men-attack-the-shy-maid", "exile-of-jon-connington",
    "aegon-revealed-to-the-golden-company", "golden-company-sails-for-westeros",
    "landing-of-the-golden-company",
    # The launch (S109/S139 Tywin's death — DEDUP)
    "varys-smuggles-tyrion-out-of-kings-landing", "assassination-of-tywin-lannister",
    "tyrion-kills-shae-in-tywins-bed", "trial-of-tyrion-lannister",
    "jaime-frees-tyrion-from-the-black-cells", "jaime-reveals-the-truth-of-tysha",
    "arstan-kills-mero",
}
CAST = {
    "tyrion-lannister", "illyrio-mopatis", "jon-connington", "aegon-targaryen-young-griff",
    "haldon", "lemore", "duck", "rolly-duckfield", "yandry", "ysilla",
    "penny", "oppo", "jorah-mormont", "nurse", "ben-plumm", "kasporio", "meris",
    "qavo-nogarys", "widow-of-the-waterfront", "daenerys-targaryen", "varys", "mero",
}
PLACES_ARTIFACTS = {
    "pentos", "illyrios-manse", "rhoyne", "little-rhoyne", "upper-rhoyne", "mother-rhoyne",
    "selhorys", "volantis", "meereen", "yunkai", "slavers-bay", "bridge-of-dream",
    "shy-maid", "cyvasse", "tyrions-mushrooms", "illyrios-ruby-chain", "illyrios-chests",
    "second-sons", "golden-company", "stone-men", "greyscale", "bloody-flux",
}
CORE = EVENTS | CAST | PLACES_ARTIFACTS

# which CORE slugs actually have a node file?
node_files = {p.stem.replace(".node", "") for p in pathlib.Path("graph/nodes").rglob("*.node.md")}
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
print(f"CORE slugs WITHOUT a node file ({len(missing)}) — candidates to BUILD if load-bearing:")
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
    print(f"  {n:52s} cOut={o:2d} cIn={i:2d}  (tot out={to:2d} in={ti:2d}){flag}{exists}")

print()
print("=" * 78)
print("CAST/PLACE degree (out/in within core + boundary)")
print("=" * 78)
for n in sorted(CAST | PLACES_ARTIFACTS):
    o, i, b = deg_out.get(n, 0), deg_in.get(n, 0), boundary.get(n, 0)
    miss = "  [NO node file]" if n in missing else ""
    print(f"  {n:30s} core_out={o:2d} core_in={i:2d}  boundary={b:3d}{miss}")
