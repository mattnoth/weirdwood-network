# A2.7 — Stannis — BASELINE (S155)

> **19th major-arc enrichment dip; first of the 🅰 A-roundup campaign** (Matt S154). Stannis is **NOT a POV** —
> his arc lives across Davos/Catelyn/Jon/Asha POVs and spreads across containers (wo5k, north, + Dragonstone). He
> is **heavily pre-wired** via the **Blackwater (S138)** and **NORTH (S125-126)** spines, so this is **WIRE + ENRICH**,
> NOT a from-scratch build. The dedup pull found **409 unique internal edges but only 10 internal CAUSAL edges** —
> the classic Class-D profile (dense dyadic/social web, causally-ISLANDED event hubs). **The dip's value = the
> MOTIVATES/causal substrate the spine lacks** (the R'hllor conversion engine, the Renly-kinslaying guilt thread,
> the why-Stannis-marches-north motive) + a few marquee object/event nodes (Lightbringer, the leeching).

## Source chapters (the Stannis span — Davos is the lens POV)
| file | content |
|------|---------|
| acok-prologue | **Cressen / Dragonstone / Melisandre.** The conversion setup; Cressen's poison-attempt & death; the burning of the Seven foreshadowed; Patchface; the queen's men vs Davos |
| acok-catelyn-02 | Renly's host at Storm's End; the storm lords; Stannis besieges Storm's End |
| acok-catelyn-03 | **The parley between Stannis & Renly** ("you have the better claim, but I have the larger army"); Catelyn negotiates; the peach |
| acok-catelyn-04 | **The shadow-baby kills Renly** (the green tent; Brienne & Catelyn witness; "Cold"; gorget parts like cheesecloth); Catelyn names Stannis the killer through sorcery |
| acok-catelyn-05 | Brienne flees with Catelyn; Brienne vows vengeance on Stannis |
| acok-davos-01 | **The burning of the Seven at Dragonstone**; Mel draws the "Lightbringer" (the red sword); Davos's misgivings; the queen's men |
| acok-davos-02 | **The shadow-birth at Storm's End**: Davos rows Mel into a sea cave; she births the shadow that kills Cortnay Penrose; Stannis & Cortnay's parley |
| acok-davos-03 | The assault on Dragonstone backstory (16 yrs); the fleet; Salladhor Saan |
| asos-davos-01 | Davos shipwrecked, rescued; rages that Mel burned him; the false Lightbringer |
| asos-davos-02 | Dragonstone; Mel burning godswood idols; Salladhor; Davos imprisoned |
| asos-davos-03 | Alester Florent's treason; the Florent leadership; the burning |
| asos-davos-04 | **Edric Storm**; the king's-blood argument begins; Davos resolves to save the boy |
| asos-davos-05 | **The leeching of Edric Storm** (3 leeches → "the usurper Joffrey / the usurper Balon / the usurper Robb"); the stone-dragon demand; the king's-blood thread |
| asos-davos-06 | **The Iron Bank / the Wall decision**: the letter from the Wall; Davos's "save the realm to win the throne" argument; Stannis sails north |
| adwd-davos-01..04 | Davos's own White Harbor/Manderly mission (Stannis context only — light) |
| adwd-melisandre-01 | Mel's nightfires/visions at the Wall; the Mance glamour (**S145 — DO NOT re-touch**) |
| adwd Jon / the-kings-prize / the-sacrifice | the march on Winterfell; Crofter's Village stall; the queen's-men sacrifice pressure |

## What's ALREADY built — the dense web (409 internal edges; dedup against ALL of it)

**The existing CAUSAL spine (only 10 internal causal edges — this IS the partial backbone; do NOT re-propose):**
```
shadow-assassination-of-renly  CAUSES   stannis-absorbs-renly-s-host  ENABLES  battle-of-the-blackwater
battle-of-the-blackwater       CAUSES   stannis-retreats-to-dragonstone   (also: garlan-routs CAUSES retreat [S138])
stannis-retreats-to-dragonstone ENABLES stannis-moves-to-the-wall  CAUSES  battle-beneath-the-wall
battle-beneath-the-wall        CAUSES   mance-rayder-brought-to-execution
stannis-march-on-winterfell    ENABLES  stannis-s-army-stalls-at-crofters-village
shadow-assassination-of-renly  MOTIVATES loras-tyrell
wedding-of-ramsay-bolton-and-arya-stark  MOTIVATES  stannis-baratheon   ("Stannis must march or lose them")
```

**Already wired (do NOT re-propose) — the rich dyadic layer, sampled:**
- stannis: AGENT_IN {shadow-assassination-of-renly, renly-s-death-reflection, stannis-absorbs-renly-s-host, stannis-moves-to-the-wall, stannis-march-on-winterfell}; KILLS/MOURNS/RESENTS/OPPOSES renly; LOVER_OF/TRUSTS/COMMANDS/COMPANION_OF melisandre; PROTECTS+UNCLE_OF edric-storm; PROTECTS+PARENT_OF shireen; COMMANDS_IN {antler-men, mance-execution, jon-argues-dreadfort, siege-storms-end-299, greyjoy-rebellion, blackwater}; EXECUTES mance; BESIEGES storms-end; VICTIM_IN {queen's-men ×2, crofters-stall}; RULES dragonstone/storms-end; BESTOWS_KNIGHTHOOD davos; DISTRUSTS cersei ("Cersei had a hand in Robert's death"); HEIR_TO robert; SIBLING_OF robert.
- melisandre: AGENT_IN {queen's-faction-urges-sacrifice, mance-execution}; COMMANDS_IN shadow-assassination-of-renly; **SACRIFICES edric-storm** + alester-florent; KILLS cressen + guncer-sunglass; SERVES stannis; FORESHADOWS jon-is-stabbed; COMMANDS/MANIPULATES lord-of-bones; FEARS rhllor [sic — odd existing edge].
- shadow-assassination-of-renly: stannis AGENT_IN; melisandre COMMANDS_IN; renly VICTIM_IN; CAUSES absorbs-host; ENABLES littlefinger-tyrell-alliance; MOTIVATES loras; SUB_BEAT_OF siege-storms-end-299; LOCATED_AT storms-end.
- selyse WORSHIPS rhllor; storms-end RELIGION_OF rhllor; tycho-nestoris SEEKS stannis (Iron Bank); wyman-manderly CONSPIRES_WITH stannis; davos SWORN_TO/SERVES/TRUSTS stannis; salladhor BETRAYS stannis; alester/arnolf BETRAYS stannis; jon-snow ALLIES_WITH/RESPECTS/OPPOSES stannis; the full Florent/queen's-men/Dragonstone-court web.

## DEAD-ENDS / GAPS — the dip targets (confirm each in-text; some are node-prose, not edges)

1. **MARQUEE — the R'HLLOR CONVERSION ENGINE is completely unwired.** No `stannis WORSHIPS rhllor`; no
   `melisandre ADVISES stannis` (she has SERVES/COMMANDED-by/COMPANION_OF/LOVER_OF/TRUSTS but **no ADVISES**);
   no `melisandre PRACTICES` anything; **`lightbringer` has 0 edges graph-wide**; `rhllor` is 0-out/11-in.
   Candidates: `stannis WORSHIPS rhllor` (the public conversion — burns the Seven, takes R'hllor as his god); a
   **`burning-of-the-seven-at-dragonstone`** event node (acok-davos-01: Mel burns the seven idols, Stannis draws
   the "Lightbringer" from the fire) with melisandre AGENT_IN / stannis AGENT_IN/PARTICIPATES_IN; `stannis WIELDS
   lightbringer` + `melisandre ADVISES stannis`; `melisandre PRACTICES shadowbinding` (concept node may not exist
   → node-prose). **The conversion is the engine of the whole arc and the spine has nothing on it.**

2. **MARQUEE — the shadow-baby spine: `shadow-assassination-of-renly` has cIn=0** (nothing causes it) and
   `siege-of-storms-end-299` is causally ISLANDED (despite the shadow being SUB_BEAT_OF it). The Renly's-war
   upstream is unwired: Renly crowns himself / claims the throne → Stannis besieges Storm's End → the **failed
   parley** (acok-catelyn-03) → Mel's shadow. Candidates: `siege-of-storms-end-299 ENABLES shadow-assassination`;
   a parley beat MOTIVATES; the **Catelyn + Brienne WITNESS_IN** layer of Renly's actual death (the green tent —
   they SEE it, acok-catelyn-04); the **SECOND shadow that kills Cortnay Penrose** at Storm's End (acok-davos-02:
   a separate shadow-birth — cortnay-penrose VICTIM_IN; Davos PARTICIPATES_IN rowing Mel in). Honor ENABLES-vs-CAUSES.

3. **MARQUEE — the Renly-KINSLAYING GUILT MOTIVATES substrate (continue-prompt-named).** `renly-s-death-reflection`
   (Stannis confides he dreams of Renly's dying — acok-davos-02) is causally ISLANDED. Candidate:
   `renly-s-death-reflection MOTIVATES stannis-baratheon` (the guilt that haunts him) or
   `shadow-assassination-of-renly MOTIVATES stannis`. Watch agency-collapse — route the guilt through MOTIVATES(→character).

4. **MARQUEE — the WHY-STANNIS-MARCHES-NORTH motive.** `stannis-moves-to-the-wall` cIn=1 (retreat ENABLES it) but
   the **MOTIVATES is missing**: Davos's **"save the realm to win the throne"** argument (asos-davos-06). The
   **Iron Bank loan** (tycho SEEKS stannis exists; the loan ENABLES the northern campaign). `stannis-march-on-winterfell`
   has cIn=0 — nothing causes/enables the march event (the `wedding-of-ramsay MOTIVATES stannis-the-person` exists
   but isn't tied to the march event). Candidates: `battle-beneath-the-wall ENABLES stannis-march-on-winterfell`
   (after relieving the Wall he marches south on the Boltons); a Davos-argument MOTIVATES; the Iron-Bank-loan ENABLES.

5. **The LEECH-SACRIFICE / Edric Storm (king's-blood — THEORY-GATED reading).** `melisandre SACRIFICES edric-storm`
   exists, but the **leeching** itself (asos-davos-05: Mel throws 3 leeches fat with Edric's blood into the brazier
   and names "the usurper Joffrey / the usurper Balon / the usurper Robb") has **no node**, and the queen's-men
   sacrifice-urging trio (the-queen-s-faction-urges-sacrifice-of-edric-storm + queen-s-men-begin/push) are all
   causally ISLANDED. Candidate: a `leeching-of-edric-storm` event.incident (melisandre AGENT_IN, edric VICTIM_IN,
   stannis COMMANDS_IN/PARTICIPATES_IN, the-three-leeches WIELDED_IN?); Davos rescues/smuggles Edric away
   (`davos RESCUES edric-storm`). **GATED:** the king's-blood-magic-WORKS reading, the three-kings-die-because-of-it
   causation, the stone-dragon, Azor-Ahai-reborn — all node-prose/evidence-only. The leeching is a TEXT EVENT; do
   NOT mint `leeching FORESHADOWS/CAUSES death-of-joffrey/robb/balon` (that asserts the magic — node-prose only).

6. **The TWINCEST-REVELATION / IRON-THRONE-CLAIM seam (RR backstory → his whole war; Lens D).** Stannis fled KL to
   Dragonstone after **Jon Arryn's death** because he & Jon Arryn uncovered the twincest (the Lannister children
   aren't Robert's) — the root of his claim. `jon-arryn COMPANION_OF stannis` exists; `murder-of-jon-arryn` node
   exists (S133/S148). Candidate seam: `murder-of-jon-arryn MOTIVATES stannis-baratheon` and/or a Stannis-discovers-
   the-truth beat → his claim. This wires Stannis into the RR / Ned's-downfall / Iron-Throne cluster.

7. **The ONION-KNIGHT / Storm's-End-siege backstory (RR; Stannis↔Davos origin).** During RR, Stannis held Storm's End
   against the Tyrell siege (ate rats), then Davos ran the blockade with onions → Stannis knighted him + shortened
   his fingers. `davos RESENTS stannis` ("before the onion ship, before Storm's End, before Stannis shortened my
   fingers"). The onion-smuggling is a marquee origin — likely node-prose / a small backstory event. `assault-on-
   dragonstone` (284 AC, Stannis takes Dragonstone from the Targaryens) is causally islanded RR-era backstory.

8. **`lightbringer` descriptive/object depth (Lens C).** The "red sword" that gives no heat — the **false Lightbringer**
   ("That sword was not Lightbringer, my friend"). stannis WIELDS it; MADE_OF? the nightfires; Mel's ruby (`melisandres-ruby`
   exists, 0-out/1-in); Patchface's prophetic songs; Stannis's gaunt physical description.

9. **`the-antler-men-conspiracy`** (causally islanded; stannis COMMANDS_IN) — the KL fifth column for the Blackwater.
   **This is the B5 L2 unit (its own dip) — LIGHT TOUCH ONLY** (e.g. `antler-men ENABLES/PART_OF blackwater` if text-direct); do NOT build out the conspiracy here.

## DO NOT (this dip)
- **Re-touch the Blackwater wildfire** (S138 — `wildfire-trap-on-the-blackwater`, the Renly's-ghost rout) or the
  **NORTH Mance-glamour / "Rattleshirt" thread** (S145, adwd-melisandre-01). Confirm-only the seams into them.
- Re-propose any of the 409 existing internal edges (deduped above) or the dense Dragonstone-court / Florent web.
- **Touch `flight-to-dragonstone` / `fall-of-dragonstone` / `shadow-war`** — these are **wiki name-collisions**:
  Dance-of-the-Dragons (130 AC) and Slaver's-Bay events, **NOT Stannis**. Excluded from scope.
- **Assert theory readings (GATED):** Azor Ahai / Stannis-as-the-prince-that-was-promised / R'hllor cosmology /
  the king's-blood-magic mechanics / Shireen-as-future-sacrifice / the stone dragon. The leeching, the burning of
  the Seven, the visions, "valar"-class words are TEXT EVENTS (mint the events + possession/agency edges); the
  theology/prophecy READING stays node-prose, evidence-only. NO `leeching FORESHADOWS/CAUSES` the three kings' deaths.
- Mint show-canon beats not in the books (check every beat against the chapter text).
- Over-mint speculative seam/foreshadowing edges — node-prose when unsure; honor ENABLES-vs-CAUSES; route human
  choices through MOTIVATES(→character), never a false A-CAUSES-B.
- **Container tags:** Stannis nodes spread across containers. Tag a NEW node only when it clearly belongs to one of
  the approved 5 (essos/wo5k/north/aegon/bran) AND is already wired into that container's spine. Dragonstone/Renly's-war
  nodes default to NO tag (like the S148-S150 A2 arcs); a Wall/march node may carry `[north]` if wired to the NORTH spine.

## Vocab: locked 170-type list (load from working/wiki/data/edge-type-counts.json)
Use ONLY these. Qualifier rule (validator-enforced) applies at MINT: Tier-1 types
(MANIPULATES/WARD_OF/SIBLING_OF/SPOUSE_OF/PARENT_OF/HOLDS_TITLE/VOWS_TO/SWORN_TO) REQUIRE an enum-valid qualifier;
Tier-3 must NOT; event-role + causal types take none. WORSHIPS/PRACTICES/SACRIFICES/ADVISES/RESCUES take no qualifier.
