# Blackwater enrichment dip (S138) — BASELINE (dedup reference)

> Built from `graph-query.py --neighbors / --full-chain battle-of-the-blackwater` + node reads, 2026-06-23.
> **Every lens dedups against this.** If a node/edge is listed here, it already exists — do NOT re-propose it; propose only NEW substrate.

## Hub node: `battle-of-the-blackwater` (event.battle, containers: [wo5k])
Rich wiki-derived Narrative Arc + Aftermath + 11 Quotes already on the node (wildfire wall, Renly's-ghost/Dontos, the chain, Mace "that chain was cunning", Melisandre/Davos, Tyrion "I thought I won the bloody battle"). The PROSE texture is largely captured on the node body; the GAP is the **graph edges** (causal + role/participant) and any NEW beat-nodes for off-spine moments.

## Existing causal spine (DO NOT re-propose)
UPSTREAM (ENABLES preconditions):
- `stannis-absorbs-renly-s-host` ENABLES `battle-of-the-blackwater`
- `littlefinger-brokers-tyrell-lannister-alliance` ENABLES `battle-of-the-blackwater`
- (further up: `shadow-assassination-of-renly` CAUSES stannis-absorbs-host; ENABLES littlefinger-brokers...)

DOWNSTREAM (CAUSES — S111):
- `battle-of-the-blackwater` CAUSES `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery`
- `battle-of-the-blackwater` CAUSES `stannis-retreats-to-dragonstone`
- `battle-of-the-blackwater` CAUSES `tywin-named-savior-of-the-city`
- (downstream chain continues: stannis-retreats → stannis-moves-to-the-wall → battle-beneath-the-wall → … NORTH spine)

Other existing edges on hub: PART_OF war-of-the-five-kings; PRECEDES battle-outside-the-gates-of-winterfell; fall-of-harrenhal PRECEDES it; DIED_AT (kennet-flea-bottom, richard-farrow).

## Existing SUB_BEAT_OF children (bare Plate-3 stubs — exist but near-empty bodies)
- `fleet-forms-battle-lines` (event.battle, ACOK Davos III) — SUB_BEAT_OF blackwater
- `a-knight-attacks-tyrion-s-shield` (event.incident, ACOK Tyrion XIV) — SUB_BEAT_OF blackwater
These are skeletal stubs (status minted-plate3, empty `## Edges`). They can be ENRICHED with role edges if useful, but the bodies are not load-bearing.

## CRITICAL dedup traps
- **`wildfire-plot` is NOT the Blackwater wildfire.** It is the **Aerys II / Robert's-Rebellion 283 AC** wildfire-cache plot (FIGHTS_IN Robert's Rebellion; `wildfire-plot MOTIVATES slaying-of-aerys-ii` from RR-S133). The **Blackwater wildfire trap has NO node** — if you propose one, give it a Blackwater-specific slug (e.g. `wildfire-trap-on-the-blackwater`) and never wire it to `wildfire-plot`.
- `the-antler-men-conspiracy` (event.conspiracy, ACOK Tyrion XII) EXISTS as a bare Plate-3 stub — has NO role edges. Wiring its participants/victims is fair game.
- `tyrion-fights-and-kills` (AGOT Tyrion IV) and `tyrion-s-battle-dream` (ADWD Tyrion II) are NOT Blackwater — ignore.
- `shadow-assassination-of-renly` is the Storm's End shadow-killing (already upstream). Garlan-wearing-Renly's-armor at the Blackwater is a DIFFERENT thing (the "Renly's ghost" rout) — no node for it yet.

## Confirmed existing participant/person nodes (use these exact slugs)
tyrion-lannister, cersei-lannister, joffrey-baratheon, sansa-stark, stannis-baratheon, davos-seaworth,
sandor-clegane, bronn, podrick-payne, mandon-moore (NOT "ser-mandon-moore"), garlan-tyrell, imry-florent,
guyard-morrigen, salladhor-saan, hallyne (NOT "hallyne-the-pyromancer"), lancel-lannister, osney-kettleblack,
osfryd-kettleblack, balon-swann, jacelyn-bywater, ilyn-payne, renly-baratheon, tywin-lannister, mace-tyrell,
randyll-tarly, lothor-brune, josmyn-peckledon, petyr-baelish.

## Key chapter files (Blackwater core)
- `sources/chapters/acok/acok-davos-03.md` — Davos III: the fleet enters, the wildfire wall, the chain raised (fleet trapped). [the wildfire/chain POV]
- `sources/chapters/acok/acok-tyrion-13.md` — Tyrion XIII: prep + battle opens, the chain, Joffrey on the walls.
- `sources/chapters/acok/acok-tyrion-14.md` — Tyrion XIV: the King's Gate sortie, Sandor's failure of nerve, Tyrion leads the sortie, the burning, Mandon Moore's treachery, Pod saves him, Garlan/Tywin arrive.
- `sources/chapters/acok/acok-tyrion-15.md` — Tyrion XV: wakes after, aftermath, disfigured.
- `sources/chapters/acok/acok-sansa-06.md` — Sansa VI: Maegor's Holdfast, Cersei & the women, Ilyn Payne, Cersei's drinking/threats.
- `sources/chapters/acok/acok-sansa-07.md` — Sansa VII: the queen's ballroom during battle, Cersei leaves, Lancel wounded, Sansa comforts the women, the arrival of relief (Dontos "Renly's ghost" line at :145).
- `sources/chapters/acok/acok-tyrion-12.md` — Tyrion XII: the Antler Men exposed, Cersei has them flung from the walls.
- `sources/chapters/acok/acok-sansa-08.md` — Sansa VIII: aftermath court (Tywin Savior, Sansa-set-aside) — already wired.

## THE GAP (what this dip is for)
The hub is causally wired up/down and has rich prose, but the **off-spine battle substrate is unbuilt as graph edges/nodes**:
1. The **wildfire trap** (the green-fire wall) — no node; Hallyne/the Alchemists' Guild + Tyrion's role; the Antler-Men/Cersei wildfire arrangement.
2. The **chain boom** — Tyrion commissioned it; Bronn at the winch towers ("Ser Bronn of the Blackwater"). No object node / no WIELDED_IN-style wiring.
3. **Tyrion's sortie** at the King's Gate + the burning + **Sandor's failure of nerve / retreat** (he quits; "Fuck the water" / asks for wine). No node/edges.
4. **Mandon Moore's attempt on Tyrion** + **Pod kills Mandon** — `a-knight-attacks-tyrion-s-shield` stub exists; KILLS/role edges missing.
5. **Garlan-as-Renly's-ghost** rout (the green armor) — the decisive psychological break that routed Stannis. No node/edge.
6. **Stannis's assault / the fleet burning** — Imry Florent's command error (rowing past the chain), Davos's sons burned.
7. **Participants/witnesses**: FIGHTS_IN / COMMANDS_IN / WITNESS_IN slots on the hub (Tyrion COMMANDS_IN, Sandor/Bronn/Stannis/Imry/Garlan, Sansa WITNESS_IN the burning from Maegor's? — text-anchor gate).
8. **The Antler Men** — participants flung to their deaths (Cersei's order).
