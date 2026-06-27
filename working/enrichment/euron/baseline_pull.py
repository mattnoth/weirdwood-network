#!/usr/bin/env python3
"""A1.6 Kingsmoot / Euron baseline edge pull (S157) — dedup the existing internal web before proposing.

Unlike the other A1s, the Kingsmoot/Euron arc already has a spine (S116) + ONE early enrichment (S116,
pre-formal-L1) + a remainder voyage-wire (S132 Victarion → Slaver's Bay, [essos]-tagged). So this is a
WIRE + ENRICH with a HEAVY dedup — much of the kingsmoot is already built. The dedup is EXPECTED to kill
several lens proposals (the S116 spine wired death-of-balon → euron-seizes-the-seastone-chair → kingsmoot
→ taking-of-the-shields; euron SUSPECTED_OF death-of-balon; the 3 S116 bridge nodes; the S132 voyage cluster).

Dumps:
  - INTERNAL edges (both endpoints in the core set), unique
  - CAUSAL sub-web (CAUSES/TRIGGERS/MOTIVATES/ENABLES) within the core — to find causally-islanded hubs
  - DEGREE per core node (out/in) with dead-end flags
  - BOUNDARY edge counts (one endpoint in core)

EXCLUDES TWOW nodes (victarion-i-the-winds-of-winter) + the redirect stub battle-of-the-shield-islands
(same_as taking-of-the-shields). falia-flowers is TWOW-only (The Forsaken) — kept OUT of core; do NOT mint
edges for her. Only the 5 published books are in scope.
"""
import json, collections, pathlib

EDGES = pathlib.Path("graph/edges/edges.jsonl")
CAUSAL = {"CAUSES", "TRIGGERS", "MOTIVATES", "ENABLES"}

# ── CORE node set (published Iron Islands / Kingsmoot / Euron arc only) ───────
EVENTS = {
    # The kingsmoot spine (S116) + its collapse / Euron's seizure (AFFC)
    "death-of-balon-greyjoy", "euron-seizes-the-seastone-chair", "kingsmoot-on-old-wyk",
    "taking-of-the-shields", "asha-claims-the-kingsmoot", "aeron-vows-to-raise-the-ironborn-smallfolk",
    "victarion-slays-multiple-defenders",
    # ACOK Greyjoy-invasion roots / Iron-Islands-cast events
    "balon-declares-himself-king", "aeron-damphair-demands-benfred-s-death",
    # The 3 S116 bridge nodes (DEDUP — do not re-mint)
    "euron-weds-asha-to-erik-ironmaker-in-absentia", "euron-commissions-victarion-to-fetch-daenerys",
    "euron-hunts-aeron-damphair", "victarion-admits-euron-s-role-in-his-wife-s-death",
    # The S132 Victarion-voyage cluster ([essos]-tagged — DEDUP)
    "iron-fleet-departs-for-slavers-bay", "iron-fleet-captures-ghiscari-dawn",
    "iron-fleet-captures-myrish-cog-dove", "moqorro-reads-dragonbinder-glyphs",
    "the-crew-calls-for-moqorro-s-death",
}
CAST = {
    # House Greyjoy core
    "euron-greyjoy", "victarion-greyjoy", "aeron-greyjoy", "asha-greyjoy", "balon-greyjoy",
    "theon-greyjoy", "quellon-greyjoy", "alannys-harlaw",
    # The Harlaw faction (the Reader = rodrik-harlaw)
    "rodrik-harlaw", "gwynesse-harlaw", "hotho-harlaw", "harras-harlaw", "sigfryd-harlaw",
    # Other kingsmoot / vassal lords
    "baelor-blacktyde", "gorold-goodbrother", "nute-the-barber", "hagen-the-horn",
    "erik-ironmaker", "sawane-botley", "tristifer-botley", "quellon-botley", "balon-botley",
    "maron-volmark",
    # Euron's household / the Silence
    "moqorro", "eurons-mongrel-sons", "dusky-woman",
    # Cross-arc
    "daenerys-targaryen",
}
PLACES_ARTIFACTS = {
    "pyke", "pyke-island", "great-keep-of-pyke", "old-wyk", "lordsport", "naggas-hill", "naggas-cradle",
    "shield-islands", "greenshield", "greyshield", "southshield", "oldtown", "lonely-light",
    "ten-towers", "harlaw", "harlaw-hall", "hammerhorn", "iron-islands",
    "seastone-chair", "dragonbinder", "silence", "iron-victory", "great-kraken",
    "house-greyjoy", "house-harlaw", "house-blacktyde", "house-botley", "house-goodbrother",
    "house-volmark", "house-ironmaker", "house-merlyn", "house-sparr", "house-stonehouse",
    "house-drumm", "iron-fleet", "ironborn", "drowned-god",
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
    print(f"  {n:50s} cOut={o:2d} cIn={i:2d}  (tot out={to:2d} in={ti:2d}){flag}{exists}")

print()
print("=" * 78)
print("CAST/PLACE degree (out/in within core + boundary)")
print("=" * 78)
for n in sorted(CAST | PLACES_ARTIFACTS):
    o, i, b = deg_out.get(n, 0), deg_in.get(n, 0), boundary.get(n, 0)
    print(f"  {n:42s} core_out={o:2d} core_in={i:2d}  boundary={b:3d}")
