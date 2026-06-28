# Baseline — A2.5 WO5K-battles (S163, PASS 1 of a multi-pass mini-track)

**Unit:** A2.5 WO5K-battles — the military arc that makes Robb Stark the Young Wolf. The LAST 🅰 A-roundup
unit and explicitly **multi-pass**. **THIS IS PASS 1.**

**PASS-1 cut = Robb's Riverlands-relief rise:**
the **Whispering Wood** (Jaime captured) → the **Battle of the Camps** (Riverrun relieved) → the seam into
**robb-proclaimed-king-in-the-north** (the Young Wolf / WO5K Northern front launches).
- **PASS 2 (deferred):** the Westerlands raid (Oxcross / the Crag / the Jeyne-Westerling marriage-blunder).
- **PASS 3 (deferred):** the unravelling (the Fords / Duskendale → the Red-Wedding upstream).

**Source chapters (PASS 1 — read IN FULL, cite `chapter:line`):**
- `agot-catelyn-08` — the war council at Moat Cailin; Robb's plan to **split the host** (foot down the kingsroad,
  horse across the Green Fork to relieve Riverrun); the cast (Greatjon, Glovers, Karstarks, Roose Bolton, Galbart
  Glover, the Blackfish). The plan that sets up the whole rise.
- `agot-catelyn-09` — the march south; the Frey crossing at the **Twins** (Walder's 4,000); news of the **battle
  under the walls of Riverrun** (Edmure's host smashed, Edmure captured, Blackwood besieged); the Blackfish screens.
- `agot-catelyn-10` — **THE WHISPERING WOOD.** Catelyn waits with 30 guards while Robb springs the night trap in
  the wood; the Blackfish's outriders blind Jaime; Jaime "restless, quick to anger"; Robb wins; **Jaime captured.**
- `agot-catelyn-11` — the return to Riverrun; the **Battle of the Camps** recounted ("Riverrun is free again");
  the reunion with the dying Hoster; and the **King in the North** proclamation at the war council.

The Green Fork (Tyrion's POV) is the **diversion** — `battle-on-the-green-fork` is ALREADY RICH (29 edges).
**DEDUP — do not rebuild it.** The only new thing is the **ENABLES seam** (the Green-Fork feint drew Tywin north,
leaving Jaime unsupported → the Whispering Wood possible). Read Robb's plan in cat-08 for that seam; do NOT re-mint
Green-Fork internals.

---

## THE GAPS (aim here)

### 1. `battle-of-the-whispering-wood` — NO LIVE NODE, 0 edges. **BUILD IT.** (the marquee)
The Whispering Wood battle has **no event-hub node** — only a thin `whispering-wood` **place.location** (the FOREST).
The night-ambush where Robb's 6,000 trap and smash Jaime's host and **take Jaime captive** is entirely unbuilt as an
event. Propose a NEW `event.battle` node `battle-of-the-whispering-wood` (container `[wo5k]`), and reify its roles:
- **robb-stark** COMMANDS_IN / AGENT_IN (sprang the trap), **grey-wind** FIGHTS_IN/AGENT_IN (the direwolf at the
  kill), **brynden-tully** (the Blackfish — screened the march, his outriders blinded Jaime), the northern lords
  who rode in the wood (**jon-umber** = the Greatjon, **rickard-karstark**, **maege-mormont**, **galbart-glover**).
- **jaime-lannister** VICTIM_IN (taken captive), and any Lannister knights cut down / captured (e.g. cleos-frey if
  the text supports — check). **DEFEATS** (robb DEFEATS jaime, or the battle's outcome).
- **LOCATED_AT** `whispering-wood`. A causal in (green-fork ENABLES it) and a causal out (it ENABLES the Camps).
- NB: a quarantined wiki twin exists in `graph/nodes/_conflicts/battle-of-the-whispering-wood.node.md` — it is
  EXCLUDED from index/query/resolver, so minting the live node into `events/` is safe (do not reference _conflicts).

### 2. THE CAUSAL SPINE IS EMPTY — only **2 causal edges** in the entire cluster. **WIRE IT.** (the high value)
Every battle hub is **causally ISLANDED** (rich in roles, zero in/out causation):
| hub | total edges | causal edges |
|-----|------------|--------------|
| `battle-on-the-green-fork` | 29 | **0** |
| `battle-of-the-camps` | 11 | **0** |
| `siege-of-riverrun` | 15 | **0** |
| `robb-proclaimed-king-in-the-north` | 2 | 1 in (from execution) |
| `battle-of-the-whispering-wood` | 0 | — (new) |

The **only** causal edges that exist: `execution-of-eddard-stark CAUSES robb-proclaimed-king-in-the-north` +
`execution MOTIVATES robb-stark` (S113). Propose the **relief-rise spine** (honor the ENABLES-vs-CAUSES contract —
these are preconditions opened by free military choices, so **ENABLES**, not CAUSES):
- `battle-on-the-green-fork` **ENABLES** `battle-of-the-whispering-wood` (the feint drew Tywin off; Jaime unsupported).
- `battle-of-the-whispering-wood` **ENABLES** `battle-of-the-camps` (Jaime captured + outriders eliminated → the
  leaderless, blind host is overrun; the text is explicit: "unaware of their commander's defeat").
- `battle-of-the-camps` **ENABLES** `robb-proclaimed-king-in-the-north` (the two victories + the relief of Riverrun
  gathered the lords who proclaimed him; `execution` already CAUSES the grievance — ENABLES is the military precondition).
- Consider the `siege-of-riverrun` seam (the Whispering Wood + Camps **broke** the siege — what edge, if any? gate it).

### 3. Islanded Camps-side beats (DEDUP HARD vs the 11 existing, add only the missing)
`battle-of-the-camps` already has: robb/jaime/brynden COMMANDS_IN, jon-umber/grey-wind/forley-prester/tytos-blackwood
FIGHTS_IN, edmure/andros-brax VICTIM_IN, hoster-tully WITNESS_IN, LOCATED_AT riverrun. **Do NOT re-propose these.**
Candidates to ADD only if text-anchored and missing: the Tyroshi-sellsword cloak-turn / Forley Prester's retreat,
Tytos Blackwood's sortie freeing Edmure, Lord Brax drowning on the rafts, the burned siege towers, Marq Piper /
Karyl Vance's raids (the harassment that masked Robb's approach).

---

## DEDUP HOT ZONES (LIVE — do NOT re-mint)
- **`battle-of-the-camps`** — S100 historical-anchor wave 2 (4-hub attach, 43 edges). The 11 core roles above are live.
- **`battle-on-the-green-fork`** — 29 edges. The Green-Fork diversion. Only the ENABLES seam out of it is new.
- **`robb-proclaimed-king-in-the-north`** — S113 causal-track (execution CAUSES it, robb AGENT_IN, MOTIVATES). Seam
  TARGET — wire INTO it, do not rebuild. Type is `event.ceremony`, container `[wo5k, north]`.
- **`siege-of-riverrun`** — S159 Jaime/Riverlands enriched the **AFFC resolution** (Edmure yields, Blackfish escapes).
  This pass touches only the **AGOT origin** (Jaime besieges Riverrun after smashing Edmure). DEDUP vs S159.
- **The B1 Red-Wedding-upstream spine** (Robb's victories → marriage blunder → Frey betrayal) is built. The
  Catelyn-foreboding / Frey-betrothal foreshadow already lives on `king-in-the-north`. Do not re-mint.
- The **dyad/role web is SATURATED** (catelyn 119 core-out, jaime 157, robb 76, roose 52, walder 66). Kinship,
  allegiance, perception dyads almost all exist. **The dedup WILL kill most cast-dyad proposals — aim at the GAPS.**

## SUSPICIOUS EXISTING EDGES (flag for the whodunit/wiring lens + fresh-verify — possible bug_drop)
- `roose-bolton CAPTURES jaime-lannister` (tier-1) — **likely WRONG.** Roose commanded the **Green Fork** host (the
  feint up the kingsroad); he was nowhere near the Whispering Wood. **Robb's cavalry** took Jaime. Verify and flag.
- `catelyn-stark CAPTURES jaime-lannister` (tier-1) — questionable. Catelyn did not capture Jaime; Robb's host did,
  and she received him at Riverrun. May be Pass-1 noise. Verify against cat-10/11.

## HARD RULES
- **EXCLUDE TWOW** — only the 5 published books. **No theory assertions (GATED)** — evidence/act/MOTIVATES→character
  edges only; readings stay node-prose. **No container tag** outside the approved 5 — `wo5k` IS approved; tag genuine
  WO5K-trigger-tree beats `[wo5k]`. **Verbatim quotes**, single contiguous substring of one line, with `chapter:line`.
- **PASS 1 ONLY** — scope the sub-cluster above. Do NOT reach into Oxcross (PASS 2) or the Fords/Duskendale (PASS 3)
  beyond the awareness pulls. Log the remainder for PASS 2/3.
