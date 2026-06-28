# Lens A — spine + commander/combatant cast — A2.5 WO5K-battles proposal (S164, PASS 2)

## Proposed NEW nodes

None. All load-bearing entities (robb-stark, grey-wind, jon-umber-son-of-jon, walder-frey-son-of-ryman,
rolph-spicer, jeyne-westerling, lymond-vikary, crag, battle-of-oxcross, storming-of-the-crag,
taking-of-ashemark) have existing nodes per baseline. No genuinely-missing beat lacks a home.

---

## Proposed NEW edges

### A. Causal raid spine (the three islanded hubs — ENABLES chain)

1. `battle-of-the-camps` **ENABLES** `battle-of-oxcross` | Tier-2 |
   > "Your northerners won a crushing victory. We received word only this morning." (acok-sansa-03:145)
   Rationale: Robb's relief of Riverrun and crowning (battle-of-the-camps / robb-proclaimed-king-in-the-north)
   freed him to carry the war west past the Golden Tooth and fall on Stafford Lannister's raw levies at Oxcross.
   The battle-of-the-camps node is the cleaner antecedent (PASS-1 seam) — the relief-rise is what opened the
   westward lane. This is a precondition Robb's free offensive choice then activated → ENABLES, not CAUSES.

2. `battle-of-oxcross` **ENABLES** `taking-of-ashemark` | Tier-2 |
   > "At last word he was marching toward the Crag, the seat of House Westerling," said Maester Vyman. "If I
   > dispatched a raven to Ashemark, it may be that they could send a rider after him." (acok-catelyn-06:79)
   Rationale: Stafford's green host destroyed at Oxcross → the Westerlands lay open; Robb's host swept on
   through Ashemark. The raven-to-Ashemark routing in acok-catelyn-06:79 confirms Ashemark as the next waypoint
   on the westward march after Oxcross. Free offensive choice → ENABLES.

3. `taking-of-ashemark` **ENABLES** `storming-of-the-crag` | Tier-2 |
   > "At last word he was marching toward the Crag, the seat of House Westerling," said Maester Vyman. "If I
   > dispatched a raven to Ashemark, it may be that they could send a rider after him." (acok-catelyn-06:79)
   Rationale: The Crag was the next military objective after Ashemark — Maester Vyman confirms the march
   progression (Ashemark → Crag). The raid rolling through Ashemark is what laid the Crag open for storming.
   Free offensive choice → ENABLES.

### B. Storming-of-the-Crag roster — participant roles (Crag node currently has ZERO)

4. `robb-stark` **COMMANDS_IN** `storming-of-the-crag` | Tier-1 |
   > "I took her castle and she took my heart." (asos-catelyn-02:143)
   Rationale: Robb led the storm and personally directed the ram assault on the main gate. He is the commander
   of the attacking force at the Crag.

5. `robb-stark` **AGENT_IN** `storming-of-the-crag` | Tier-1 |
   > "I broke the main gate with a ram." (asos-catelyn-02:143)
   Rationale: Robb personally acted (directed/co-executed the ram strike on the gate) — separate from his
   command role. Both COMMANDS_IN (as army commander) and AGENT_IN (as direct participant in the gate-break)
   are supported by the text. Over-propose flag: if synthesis collapses these to one, COMMANDS_IN is the
   stronger pick.

6. `jon-umber-son-of-jon` **AGENT_IN** `storming-of-the-crag` | Tier-1 |
   > "Black Walder and the Smalljon led scaling parties over the walls" (asos-catelyn-02:143)
   Rationale: The Smalljon (= jon-umber-son-of-jon, NOT the Greatjon jon-umber) led one of the scaling parties
   over the walls during the storm of the Crag. Direct participant role.

7. `walder-frey-son-of-ryman` **AGENT_IN** `storming-of-the-crag` | Tier-1 |
   > "Black Walder and the Smalljon led scaling parties over the walls" (asos-catelyn-02:143)
   Rationale: Black Walder (= walder-frey-son-of-ryman, alias-bearing — NOT the black-walder-frey twin) led
   the other scaling party. Direct participant role. **Node-dup flag (small-fix, not this dip):** two nodes
   exist for Black Walder; target the alias-bearing walder-frey-son-of-ryman.

8. `grey-wind` **FIGHTS_IN** `storming-of-the-crag` | Tier-1 |
   > "Grey Wind killed a man at the Crag" (asos-catelyn-02:185)
   Rationale: Grey Wind killed at least one combatant during the storming of the Crag. Direct combat
   participation. (The fuller kill-list quote at :185: "Grey Wind killed a man at the Crag, another at
   Ashemark, and six or seven at Oxcross" — each is a separate edge; this one covers the Crag.)

9. `rolph-spicer` **COMMANDS_IN** `storming-of-the-crag` | Tier-1 |
   > "I took an arrow in the arm just before Ser Rolph yielded us the castle." (asos-catelyn-02:143)
   Rationale: Rolph Spicer was the defending castellan who commanded the Crag's garrison and ultimately
   yielded the castle to Robb. **Side note in rationale: COMMANDS_IN as the DEFENDER, not the attacker.**
   His COMMANDS_IN should carry a rationale note distinguishing him from Robb's attacking command role.

10. `storming-of-the-crag` **LOCATED_AT** `crag` | Tier-1 |
    > "The Crag was weakly garrisoned, so we took it by storm one night." (asos-catelyn-02:143)
    Rationale: The Crag node has NO location edge at all (baseline gap). The storming self-evidently occurred
    at the Crag (Gawen Westerling's seat). The quote anchors the event to the castle.

### C. Jeyne Westerling heals Robb Stark (clean gap)

11. `jeyne-westerling` **HEALS** `robb-stark` | Tier-1 |
    > "Jeyne had me taken to her own bed, and she nursed me until the fever passed." (asos-catelyn-02:143)
    Rationale: Robb took an arrow wound in the arm that festered; Jeyne nursed him through the fever. Clean
    gap per baseline. Edge direction: HEALS (healer → healed) = jeyne-westerling → robb-stark.

### D. Oxcross VICTIM_IN gap (only the missing one — dedup'd everything else)

12. `lymond-vikary` **VICTIM_IN** `battle-of-oxcross` | Tier-1 |
    > "Ser Lymond Vikary is also dead" (acok-sansa-03:153)
    Rationale: Tyrion explicitly lists Ser Lymond Vikary among the dead at Oxcross. The node lymond-vikary
    EXISTS (per baseline: core_in=0, i.e., no incoming edges). This is a confirmed gap. The longer Tyrion
    quote for context: "Ser Rubert Brax is also dead, along with Ser Lymond Vikary, Lord Crakehall, and Lord
    Jast." — Ser Lymond Vikary is the only one with a confirmed clean live node.

### E. Grey Wind kills at Ashemark (bonus gap — same kill-list line)

13. `grey-wind` **FIGHTS_IN** `taking-of-ashemark` | Tier-1 |
    > "Grey Wind killed a man at the Crag, another at Ashemark, and six or seven at Oxcross." (asos-catelyn-02:185)
    Rationale: Grey Wind killed at least one combatant at Ashemark. The taking-of-ashemark node exists and is
    islanded (3 total edges, none participant roles). This is a genuine gap on the Ashemark hub, in the same
    sentence as the Crag kill.

### F. Grey Wind kills at Oxcross — verify vs existing AGENT_IN

14. **[BORDERLINE — verify dedup]** `grey-wind` **FIGHTS_IN** `battle-of-oxcross` | Tier-1 |
    > "Grey Wind killed a man at the Crag, another at Ashemark, and six or seven at Oxcross." (asos-catelyn-02:185)
    Rationale: Grey Wind killed 6–7 at Oxcross. Baseline says grey-wind AGENT_IN battle-of-oxcross EXISTS —
    but AGENT_IN and FIGHTS_IN are different edge types. If only AGENT_IN exists, a FIGHTS_IN edge adds
    specificity (active combat kill vs. general presence). Mark **[BORDERLINE]**: if AGENT_IN already covers
    the combat act sufficiently, drop this; otherwise add FIGHTS_IN as the kill-specific type.

---

## Dropped / considered-but-rejected

- **Rubert Brax VICTIM_IN oxcross** — mentioned in the same Tyrion list (acok-sansa-03:153: "Ser Rubert Brax
  is also dead"). Baseline explicitly flags: "Rubert Brax / Lord Crakehall / Lord Jast / Jast's sons — NO
  clean live single-character nodes; skip or node-prose." Dropped.

- **Lord Crakehall VICTIM_IN oxcross / Lord Jast VICTIM_IN oxcross / Jast's sons** — same issue; no confirmed
  clean live nodes. Dropped per baseline instruction.

- **robb-stark VICTIM_IN storming-of-the-crag (arrow wound)** — Robb took an arrow in the arm at the Crag
  (asos-catelyn-02:143; asos-catelyn-01:101: "His Grace took a wound storming the Crag"). However, VICTIM_IN
  means "had it done to them" in the reification sense. Robb was the attacker/commander; his wound is
  incidental. The vocabulary does not have a WOUNDED_IN type. The wound is better captured as node prose
  or the HEALS edge (already proposed, edge 11). Dropped as a direct edge.

- **robb-stark DEFEATS stafford-lannister** — A DEFEATS edge would be legitimate (victor → defeated), but
  robb-stark COMMANDS_IN battle-of-oxcross + stafford-lannister VICTIM_IN already wire the relationship
  through the event node. Adding DEFEATS would be redundant via the hub, not genuinely new. Dropped.

- **rickard-karstark KILLS stafford-lannister** — "Lord Rickard Karstark drove a lance through his chest"
  (acok-sansa-03:153). Baseline states rickard-karstark AGENT_IN EXISTS. Does a KILLS edge exist? If not,
  this is a genuine gap — but baseline also says stafford-lannister VICTIM_IN + DIED_AT oxcross EXIST, and
  the existing AGENT_IN is specifically Karstark's lance-kill (given baseline identifies this as already
  wired). **[NOTE for synthesis: verify whether rickard-karstark KILLS stafford-lannister exists as a direct
  dyadic edge — if not, it is a gap that Lens A nominally covers. Dropped here conservatively given
  AGENT_IN + VICTIM_IN routing through the hub.]**

- **Rymund the Rhymer DEPICTS/PERFORMS** — Rymund's Oxcross victory song appears in acok-catelyn-06:181.
  The song and its performance are hospitality/harvest-tier finds, not graph edges. No clean DEPICTS or
  PERFORMS type maps cleanly to a song about a battle. Dropped as out-of-scope for this lens; noted in Harvest.

- **storming-of-the-crag ENABLES robb-weds-jeyne-westerling** — ALREADY EXISTS per baseline. DO NOT
  re-propose. The seam closes here.

- **Spicer betrayal / SUSPECTED_OF edges** — grey-wind OPPOSES rolph-spicer + sybell-spicer CONSPIRES_WITH
  tywin-lannister BOTH EXIST per baseline. The full Tywin-pardon/Castamere/barren-jeyne payoff is AFFC =
  PASS 3. Default is zero new SUSPECTED_OF per LENS-SHARED.md. Dropped entirely.

- **battle-of-the-camps vs robb-proclaimed-king-in-the-north as ENABLES antecedent** — Both are valid PASS-1
  antecedents for the westward offensive. I chose battle-of-the-camps as the cleaner hub (the military
  event that clinched Riverrun's relief), but robb-proclaimed-king-in-the-north works too. Synthesis can
  pick; I propose battle-of-the-camps.

- **Grey Wind among the horse lines at Oxcross (acok-sansa-03:153)** — "Lord Stark sent his wolf among them.
  Even war-trained destriers went mad." This is the founding description of the Oxcross wolf-rout. However,
  grey-wind AGENT_IN battle-of-oxcross ALREADY EXISTS per baseline. The horse-line-cutting quote belongs in
  a node ## Quotes section (harvest), not a new edge. Dropped as a new edge.

- **Victory roll-call "At Stone Mill, at Oxcross, in the Battle of the Camps…" (acok-catelyn-06:217)** —
  A narrative enumerator, not an edge. Noted for harvest only.

- **Frey departure from Robb's host** — Perwyn Frey and Martyn Rivers (note: Martyn Rivers is a bastard,
  not the same as martyn-lannister) leaving Robb's host (asos-catelyn-02:17) is a PASS-3 downstream of the
  marriage blunder. Not a PASS-2 raid edge. Dropped as PASS-3 scope.

- **Black Walder's threat ("his sisters would not be loath to wed a widower")** — asos-catelyn-02:155.
  PASS-3 / Frey-rupture material. Dropped.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|-------------|------|
| quote | ACOK | acok-sansa-03:153 | Tyrion's full Oxcross account verbatim: "The northmen crept into my uncle's camp and cut his horse lines, and Lord Stark sent his wolf among them. Even war-trained destriers went mad. Knights were trampled to death in their pavilions, and the rabble woke in terror and fled, casting aside their weapons to run the faster. Ser Stafford was slain as he chased after a horse." — load-bearing for battle-of-oxcross node ## Quotes |
| quote | ACOK | acok-sansa-03:153 | Tyrion on Oxcross propaganda vs reality: "Sorcery is the sauce fools spoon over failure to hide the flavor of their own incompetence." — character voice, also Lancel's "army of wargs" line at acok-sansa-03:39 |
| quote | ASOS | asos-catelyn-02:143 | Robb's Crag account verbatim: "The Crag was weakly garrisoned, so we took it by storm one night. Black Walder and the Smalljon led scaling parties over the walls, while I broke the main gate with a ram." — load-bearing for storming-of-the-crag node ## Quotes |
| quote | ASOS | asos-catelyn-02:143 | "I took her castle and she took my heart." — Robb's summary of the Crag/Jeyne nexus; high-value for robb-stark ## Quotes and robb-weds-jeyne-westerling |
| quote | ASOS | asos-catelyn-02:185 | Grey Wind kill-list: "Grey Wind killed a man at the Crag, another at Ashemark, and six or seven at Oxcross." — load-bearing for grey-wind ## Quotes and all three battle nodes |
| food/hospitality | ACOK | acok-catelyn-07:13 | "the smallfolk were celebrating Edmure's imminent return and Robb's conquest of the Crag by hoisting horns of nut-brown ale" — casks of nut-brown ale opened from the cellars; celebration of the Crag conquest |
| food/hospitality | ACOK | acok-catelyn-07:15 | Catelyn's supper in the Great Hall: "trout wrapped in bacon, salad of turnip greens and red fennel and sweetgrass, pease and onions and hot bread" — served during the Crag-conquest celebration feast |
| food/hospitality | ACOK | acok-catelyn-06:181 | "Rymund the Rhymer sang through all the courses" at the Great Hall supper celebrating Oxcross — meal accompaniment during the victory song performance |
| food/hospitality | ASOS | asos-catelyn-01:81 | Maester Vyman brings Catelyn "a modest supper of bread, cheese, and boiled beef with horseradish" while Robb is at the Crag wounded |
| song/performance | ACOK | acok-catelyn-06:181 | Rymund the Rhymer closes the supper "with the song he had written about Robb's victory at Oxcross. 'And the stars in the night were the eyes of his wolves, and the wind itself was their song.'" — Oxcross victory song; audience howled along incl. Desmond Grell |
| description | ACOK | acok-sansa-03:153 | Oxcross aftermath: "Knights were trampled to death in their pavilions, and the rabble woke in terror and fled, casting aside their weapons to run the faster" — vivid physical description of the maddened-destrier rout |
| description | ASOS | asos-catelyn-02:47 | Robb's appearance on his return from the Crag: "War had melted all the softness from his face and left him hard and lean. He had shaved his beard away, but his auburn hair fell uncut to his shoulders. The recent rains had rusted his mail and left brown stains on the white of his cloak and surcoat." — physical description |
| description | ASOS | asos-catelyn-02:37 | Jeyne Westerling's banner note: Robb's dais has "a young knight in a sand-colored surcoat blazoned with seashells" (Raynald) and "an older one who wore three black pepperpots on a saffron bend, across a field of green and silver stripes" (Rolph Spicer) — heraldic descriptions |
| wound | ASOS | asos-catelyn-01:101 | "His Grace took a wound storming the Crag" — Maester Vyman's first report of the wound; supports the HEALS edge |
| wound | ASOS | asos-catelyn-02:47 | "I took an arrow through the arm while storming the Crag," he said. "It's healed well, though. I had the best of care." — Robb confirms the wound type (arrow through arm) and recovery |
| quote | ASOS | asos-catelyn-02:143 | "It seemed nothing at first, but it festered." — Robb on the arrow wound at the Crag; context for the HEALS edge |
| intelligence | ASOS | asos-catelyn-02:185 | "Grey Wind doesn't like her uncle either. He bares his teeth every time Ser Rolph comes near him." — wolf-sense signal pointing to Rolph Spicer betrayal (already wired in graph; this is the prose evidence anchor for the node) |
