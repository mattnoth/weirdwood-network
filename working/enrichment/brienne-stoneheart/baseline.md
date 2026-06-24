# Baseline — Brienne → Stoneheart cluster (S141, the last clean L1 arc)

> Built from `graph-query.py --neighbors / --full-chain`. This is the dedup baseline — the
> lenses must NOT re-propose anything already present here.

## The spine (S115) — short and dead-ended

```
catelyn-is-killed --CAUSES--> catelyn-rises-as-lady-stoneheart --CAUSES--> brienne-brought-before-lady-stoneheart
```
- `catelyn-is-killed` (event.death): SUB_BEAT_OF red-wedding; LOCATED_AT twins; house-frey AGENT_IN, walder-frey COMMANDS_IN, catelyn-stark VICTIM_IN.
- `catelyn-rises-as-lady-stoneheart` (event.incident): beric-dondarrion + thoros + brotherhood-without-banners AGENT_IN (the resurrection kiss); catelyn-stark VICTIM_IN. **Only 1 outgoing (→ Brienne capture). NO vengeance-campaign downstream.**
- `brienne-brought-before-lady-stoneheart` (event.capture): **0 OUTGOING — the hanging-tree "sword or noose" choice goes nowhere.** brotherhood-without-banners AGENT_IN; catelyn-stark COMMANDS_IN (croaks "Hang them"); brienne-tarth + podrick-payne + hyle-hunt VICTIM_IN.

## The marquee gap — `raid-on-saltpans` is FULLY ISLANDED

`raid-on-saltpans` (event.battle): only PART_OF war-of-the-five-kings + a junk wiki `DEFEATS burning-of-town`. **ZERO participant edges.** The wiki node body (rich) establishes:
- Rorge + Biter, fleeing Brave Companions, sack Saltpans; **Rorge wears the Hound's helm** (found on Sandor's grave-heap, placed there by the Elder Brother) → the realm misattributes the atrocity to **Sandor Clegane** ("Mad Dog of Saltpans"; his accused-murder count rises 12→20).
- Randyll Tarly (from Maidenpool) spreads a counter-rumor blaming **Beric's Brotherhood** to turn the smallfolk against them.
- This false reputation is the engine of Brienne's whole AFFC hunt (she's chasing the Hound's-helm killer) AND the Brotherhood's blackened name under Stoneheart.

## Other thin/mis-wired event nodes
- `gendry-captured` (event.capture): only SUB_BEAT_OF the ACOK fight-at-the-holdfast — nothing wiring Gendry into his AFFC inn-smith life.
- `brienne-arrested` / `brienne-asks-to-arm-renly-for-battle`: ASOS/ACOK, peripheral.
- `battle-at-the-burning-septry` EXISTS as a node (the Brave-Companions atrocity Brienne hears of) — check wiring.
- `dog-fight-kills-stout-s-hound` EXISTS.

## Character layer — ALREADY DENSE (don't re-mint these)
- **brienne-tarth**: 73 outgoing / 45 incoming. Has: KILLS rorge/shagwell/pyg/timeon/dog; ATTACKS vargo-hoat; CAPTURES jaime; DUELS jaime; VOWS_TO catelyn+jaime; SEEKS sansa+sandor; COMPANION_OF pod/hyle/jaime; DISTRUSTS/RESENTS/OPPOSES hyle; FEARS/HATES randyll-tarly; biter ATTACKS her; VICTIM_IN both captures; HEALS (elder brother). Inn: GUEST_OF willow.
- **biter**: KILLED_BY gendry (affc-brienne-08:53); ATTACKS brienne + arya; AGENT_IN encounter-with-the-three-prisoners.
- **gendry**: KILLS biter (exists); COMPANION_OF arya; the ACOK/ASOS Brotherhood thread; smith. NOT wired to the inn or Saltpans aftermath.
- Existing char nodes available as edge endpoints: rorge, biter, shagwell, pyg, timeon, vargo-hoat, dick-crabb (Nimble Dick), hyle-hunt, podrick-payne, randyll-tarly, beric-dondarrion, thoros, lem-standfast, meribald (Septon Meribald), dog-meribald, owen-brother-of-meribald, elder-brother-quiet-isle, willow-heddle, jeyne-heddle, catelyn-stark, sandor-clegane, gendry.
- Places: saltpans, inn-at-the-crossroads, quiet-isle, whispers, maidenpool, crackclaw-point.
- Factions: brotherhood-without-banners, brave-companions.
- Objects: oathkeeper. (NO hound-helm node — candidate mint.)

## Where the yield is (gap thesis for the lenses)
1. **Wire the islanded `raid-on-saltpans`** — Rorge/Brave-Companions AGENT_IN, saltpans LOCATED_AT, the Hound's-helm DECEIVES/false-reputation engine (Rorge in Sandor's helm → realm blames Sandor; Randyll blames the Brotherhood). The single biggest structural fix.
2. **De-dead-end `brienne-brought-before-lady-stoneheart`** — the sword-or-noose choice; the Brotherhood's vigilante turn under Stoneheart (hanging Freys, hanging Brienne's party).
3. **Stoneheart's vengeance campaign downstream of the rise** — MOTIVATES / the hangings.
4. **Gendry's inn-smith life + the orphan/inn thread + the affc-brienne-08 inn ambush** (where Gendry kills Biter, Brienne kills Rorge).
5. **Secondary sub-arcs**: Hyle/Pod capture & hanging; the Brave-Companions remnant (Whispers fight — Shagwell/Pyg/Timeon, Nimble Dick's death); Septon Meribald + the Quiet Isle / Elder Brother / the broken-men road; Randyll Tarly at Maidenpool.
6. **Object/quote depth**: the Hound's helm, Oathkeeper, the noose/elm hanging-tree, the broken-men sermon.

## Chapter files (read these directly)
AFFC Brienne arc: `sources/chapters/affc/affc-brienne-01.md` … `affc-brienne-08.md`
Stoneheart reveal: `sources/chapters/asos/asos-epilogue.md`
Brienne arrest: `sources/chapters/asos/asos-jaime-07.md`
Saltpans wiki node body: `graph/nodes/events/raid-on-saltpans.node.md`
