# Red Wedding Enrichment — Lens 1: Downstream Causal / Consequence Chain
# Session S134

> All proposals are NET-NEW: deduped against `baseline.md` and verified `find` non-existence for NEW_NODE proposals.
> Line references are open-the-file confirmed.

---

## P1 — NEW_EDGE: `the-rains-of-castamere` TRIGGERS `red-wedding`

- **kind**: NEW_EDGE
- **source → type → target**: `the-rains-of-castamere --TRIGGERS--> red-wedding`
- **tier**: Tier-1
- **evidence**: `sources/chapters/asos/asos-catelyn-07.md:99`
  > "No one sang the words, but Catelyn knew 'The Rains of Castamere' when she heard it. Edwyn was hurrying toward a door … She grabbed Edwyn by the arm to turn him and went cold all over when she felt the iron rings beneath his silken sleeve."
- **rationale**: The Rains of Castamere is NOT simply co-incident with the Red Wedding — it is the pre-planned signal that fires the massacre. Lothar Frey chose the song specifically as the start signal (confirmed by the Epilogue: "it had been Lame Lothar who had plotted it out with Roose Bolton, all the way down to which songs would be played"). The song starting is what triggers the crossbowmen and the hall to erupt. `the-rains-of-castamere` (the song played at that moment) TRIGGERS `red-wedding` (the massacre that follows). This is a real causal mechanism in the prose, not mere succession — the song IS the signal.
- **check**: `the-rains-of-castamere` EXISTS (`graph/nodes/texts/the-rains-of-castamere.node.md`). Zero outbound causal edges from it to the RW cluster. `red-wedding` EXISTS. Edge not in `edges.jsonl` (grepped, 0 hits for `rains-of-castamere` → `red-wedding`).

---

## P2 — NEW_NODE: `grey-wind-killed-at-the-twins`

- **kind**: NEW_NODE
- **proposed slug**: `grey-wind-killed-at-the-twins`
- **type**: `event.incident`
- **1-line identity**: Grey Wind, Robb Stark's direwolf, is killed by Frey crossbowmen outside the Twins during the Red Wedding massacre, his head later sewn onto Robb's corpse.
- **role + causal edges needed**:
  - `grey-wind VICTIM_IN grey-wind-killed-at-the-twins` (Tier-1)
  - `house-frey AGENT_IN grey-wind-killed-at-the-twins` (Tier-1)
  - `grey-wind-killed-at-the-twins SUB_BEAT_OF red-wedding` (Tier-1) — the killing is a distinct beat of the massacre, co-incident with the hall slaughter but located outside the hall
  - `red-wedding CAUSES grey-wind-killed-at-the-twins` — **REJECTED** per agency-collapse rule: the killing is a sibling beat concurrent with the RW, not caused by it. Use `SUB_BEAT_OF` only.
- **evidence**: `sources/chapters/asos/asos-epilogue.md:161-163`
  > "Stark's direwolf killed four of our wolfhounds and tore the kennelmaster's arm off his shoulder, even after we'd filled him full of quarrels … So you sewed his head on Robb Stark's neck after both o' them were dead"
  (Merrett's defense, relaying Frey account of the kennel battle + the desecration)
- **evidence 2** (desecration relayed): `sources/chapters/asos/asos-arya-11.md:19`
  > "Somewhere far off she heard a wolf howling. It wasn't very loud compared to the camp noise and the music and the low ominous growl of the river running wild, but she heard it all the same."
- **non-existence confirmed**: `find graph/nodes -iname "*grey-wind-killed*" -o -iname "*grey-wind-desecrat*" -o -iname "*head-sewn*" -o -iname "*wolf-head*"` → 0 results. `grey-wind-attacks` EXISTS but it is a Plate 3 stub for a DIFFERENT event (Grey Wind attacking Frey men earlier, evidenced from ASOS Catelyn VI). This is a NEW node for the killing event at the Twins.

---

## P3 — NEW_EDGE: `red-wedding CAUSES siege-of-riverrun`

- **kind**: NEW_EDGE
- **source → type → target**: `red-wedding --CAUSES--> siege-of-riverrun`
- **tier**: Tier-1
- **evidence**: `sources/chapters/asos/asos-tyrion-06.md:53`
  > "Riverrun remains, but so long as Walder Frey holds Edmure Tully hostage, the Blackfish dare not mount a threat."
  (Tywin explaining the post-RW political situation; the RW is what produced Edmure's captivity, which is what makes the eventual siege possible)
- **rationale**: The RW kills Robb, collapses the Stark-Tully war effort, and simultaneously delivers Edmure Tully as hostage (he was at the feast). With the northern army destroyed and Edmure captive, the remaining Tully holdout at Riverrun becomes the last target and Lannister-Frey forces move to besiege it. The siege-of-riverrun exists because the RW eliminated every other blocking obstacle. This is a real causal chain: `red-wedding` (destroys Robb + delivers Edmure as hostage) CAUSES `siege-of-riverrun` (the Lannister-Frey move to eliminate the last Tully hold). Mechanism is explicit in Tywin's speech.
- **check**: `siege-of-riverrun` EXISTS (`graph/nodes/events/siege-of-riverrun.node.md`). `red-wedding` EXISTS. No causal edge between them in `edges.jsonl` (grepped, 0 hits for `CAUSES.*siege-of-riverrun`).

---

## P4 — NEW_NODE: `edmure-taken-hostage-at-the-twins`

- **kind**: NEW_NODE
- **proposed slug**: `edmure-taken-hostage-at-the-twins`
- **type**: `event.incident`
- **1-line identity**: Edmure Tully is taken captive by Walder Frey at the Twins during the Red Wedding, becoming the hostage that later forces Riverrun to yield.
- **role + causal edges needed**:
  - `edmure-tully VICTIM_IN edmure-taken-hostage-at-the-twins` (Tier-1)
  - `walder-frey AGENT_IN edmure-taken-hostage-at-the-twins` (Tier-1)
  - `house-frey AGENT_IN edmure-taken-hostage-at-the-twins` (Tier-1)
  - `edmure-taken-hostage-at-the-twins SUB_BEAT_OF red-wedding` (Tier-1)
  - `edmure-taken-hostage-at-the-twins ENABLES siege-of-riverrun` (Tier-1) — Edmure's captivity is what makes the Blackfish unable to threaten a breakout, enabling the siege to proceed to a surrender
- **evidence**: `sources/chapters/asos/asos-catelyn-07.md:119`
  > "Keep me for a hostage, Edmure as well if you haven't killed him."
  (Catelyn's plea confirms Edmure was targeted for capture — his fate as hostage is the explicit design)
- **evidence 2**: `sources/chapters/asos/asos-tyrion-06.md:53`
  > "Riverrun remains, but so long as Walder Frey holds Edmure Tully hostage, the Blackfish dare not mount a threat."
- **non-existence confirmed**: `find graph/nodes -iname "*edmure-taken*" -o -iname "*edmure-hostage*" -o -iname "*edmure-captive*"` → 0 results.

---

## P5 — NEW_EDGE: `edmure-taken-hostage-at-the-twins ENABLES siege-of-riverrun`

- **kind**: NEW_EDGE (also listed under P4; separate entry for clarity)
- **source → type → target**: `edmure-taken-hostage-at-the-twins --ENABLES--> siege-of-riverrun`
- **tier**: Tier-1
- **evidence**: `sources/chapters/asos/asos-tyrion-06.md:53`
  > "Riverrun remains, but so long as Walder Frey holds Edmure Tully hostage, the Blackfish dare not mount a threat."
- **rationale**: Tywin explicitly names the mechanism: Edmure's captivity ENABLES the siege to proceed without Brynden Tully being able to break out to relieve or threaten the besiegers. Without the hostage, the Blackfish (a capable military commander) could sortie or seek relief. With it, he is constrained. This is the precise causal mechanism that ENABLES the siege to work.
- **note**: Depends on P4 (new node). Wire after P4 is minted.

---

## P6 — NEW_NODE: `blackfish-escapes-the-twins`

- **kind**: NEW_NODE
- **proposed slug**: `blackfish-escapes-the-twins`
- **type**: `event.incident`
- **1-line identity**: Brynden "Blackfish" Tully escapes the Twins during the Red Wedding massacre, surviving to hold Riverrun for the Tully cause.
- **role + causal edges needed**:
  - `brynden-tully AGENT_IN blackfish-escapes-the-twins` (Tier-1)
  - `blackfish-escapes-the-twins SUB_BEAT_OF red-wedding` (Tier-1) — escape is co-incident with the massacre
  - `blackfish-escapes-the-twins ENABLES siege-of-riverrun` (Tier-1) — Brynden's escape is what takes him to Riverrun to hold it; without his escape, there is no Blackfish to defend it
- **evidence**: `sources/chapters/asos/asos-tyrion-06.md:53`
  > "Riverrun remains, but so long as Walder Frey holds Edmure Tully hostage, the Blackfish dare not mount a threat."
  (Tywin's framing confirms Brynden is free and holding Riverrun — his escape is the implicit backstory)
- **note (UNSURE on chapter:line for the escape itself)**: The escape is not narrated in ASOS; it is reported as accomplished fact in ASOS Tyrion VI (line 53) and AFFC. Brynden's escape during the massacre is Tier-2 inferred from ASOS text + later confirmed in AFFC. Tywin's line is the best ASOS cite. Proposer recommends Tier-2 for the escape event itself; the ENABLES → `siege-of-riverrun` edge can be Tier-1 (Brynden does hold Riverrun, confirmed in AFFC `siege-of-riverrun` node prose).
- **non-existence confirmed**: `find graph/nodes -iname "*blackfish-escapes*" -o -iname "*brynden-escapes*"` → 0 results.

---

## P7 — NEW_EDGE: `red-wedding MOTIVATES wyman-manderly-stages-fake-execution-of-davos`

- **kind**: NEW_EDGE
- **source → type → target**: `red-wedding --MOTIVATES--> wyman-manderly-stages-fake-execution-of-davos`
- **tier**: Tier-1
- **evidence**: `sources/chapters/asos/asos-epilogue.md:155`
  > "That Young Wolf never will," said the one-eyed outlaw.
  (BWB's invocation of Robb's death as justification for hanging Merrett — the RW is the event that turned Lady Stoneheart and the BWB toward vengeance)
- **evidence 2 (Manderly motivation)**: `graph/nodes/customs/guest-right.node.md` (wiki prose, confirmed):
  > "Wyman desires vengeance against House Frey for the death of his son, Wendel, who was killed at the Twins as a guest during the Red Wedding."
- **rationale**: `wyman-manderly-stages-fake-execution-of-davos` already exists as a built node (S93) with ZERO causal edges. Wyman's entire covert revenge operation — the fake execution, the Frey-bait, the Rickon mandate — is explicitly motivated by Wendel Manderly's death at the Red Wedding. The RW is the direct motivating cause of Wyman's decision to play the "mummer's farce" (he needs to appear loyal to the Freys while secretly working against them because the RW put him in a politically exposed position). Causal mechanism: Red Wedding kills Wendel (a SUB_BEAT_OF beat already built: `ser-wendel-manderly-is-killed`), which MOTIVATES Wyman's revenge deception.
- **check**: `wyman-manderly-stages-fake-execution-of-davos` EXISTS. `red-wedding` EXISTS. No MOTIVATES edge between them in `edges.jsonl`.

---

## P8 — NEW_EDGE: `ser-wendel-manderly-is-killed MOTIVATES wyman-manderly-stages-fake-execution-of-davos`

- **kind**: NEW_EDGE
- **source → type → target**: `ser-wendel-manderly-is-killed --MOTIVATES--> wyman-manderly-stages-fake-execution-of-davos`
- **tier**: Tier-1
- **evidence**: wiki prose in `guest-right.node.md` (verified above):
  > "Wyman desires vengeance against House Frey for the death of his son, Wendel, who was killed at the Twins as a guest during the Red Wedding."
- **rationale**: The specific sub-beat (`ser-wendel-manderly-is-killed`) — not just the RW in aggregate — is what MOTIVATES Wyman's plot. Wendel's death is the personal wound that drives Wyman's revenge. This is a tighter, more precise edge than P7 (both can coexist: the RW motivates at the macro level; Wendel's death motivates at the personal level). P8 is the higher-precision, higher-value edge.
- **note**: Both P7 and P8 may be proposed; orchestrator should choose P8 as primary if only one is minted (it is the more precise causal claim).

---

## P9 — NEW_EDGE: `red-wedding CAUSES guest-right VIOLATED` (as a state-change / edge to `guest-right` node)

- **kind**: NEW_EDGE
- **source → type → target**: `red-wedding --CAUSES--> guest-right` (edge label: violation / rupture)
- **UNSURE — needs schema decision**: The locked vocabulary has no `VIOLATES` edge type. The closest is `CAUSES`. Proposer suggests: `red-wedding --CAUSES--> guest-right-violated-at-the-twins` as a NEW_NODE (event.incident, "The violation of guest right at the Twins"), OR a simple `red-wedding CAUSES guest-right` edge with rationale that the RW caused a widespread collapse of guest-right observance in the Riverlands.
- **Alternatively**: An `ATTACH_QUOTE` to the existing `guest-right` node is lower-risk and still captures the connection.
- **evidence**: `sources/chapters/asos/asos-tyrion-06.md:201`
  > "So much for guest right."
  (Tyrion, explicitly naming the RW's guest-right violation)
- **evidence 2** (downstream effect): `graph/nodes/customs/guest-right.node.md` Narrative Arc AFFC:
  > "The massacre ruins the Freys' reputation even among allies." / "Trust in guest right has declined in the riverlands in the aftermath of the Red Wedding."
- **recommendation**: Mint as `ATTACH_QUOTE` on `guest-right` node (the verbatim Tyrion quote) AND propose a `red-wedding --CAUSES--> guest-right` edge with tier-1 rationale (the prose link is explicit). Flag for schema review re: `CAUSES` between event and concept node (novel pattern, orchestrator decides).

---

## P10 — ATTACH_QUOTE: `grey-wind` node — the desecration quote

- **kind**: ATTACH_QUOTE
- **node slug**: `grey-wind`
- **quote** (verbatim, line-confirmed `asos-epilogue.md:161-163`):
  > "Stark's direwolf killed four of our wolfhounds and tore the kennelmaster's arm off his shoulder, even after we'd filled him full of quarrels … So you sewed his head on Robb Stark's neck after both o' them were dead."
- **chapter:line**: `sources/chapters/asos/asos-epilogue.md:161-163`
- **note**: The `grey-wind` node mentions the desecration in its wiki-sourced `## Narrative Arc` but lacks a verbatim book quote for it. This is the only first-person account (Merrett/yellow-cloak exchange), making it the primary cite for the desecration. HIGH VALUE — upgrades wiki Tier-2 prose to Tier-1 book quote.

---

## P11 — ATTACH_QUOTE: `the-rains-of-castamere` node — the signal moment

- **kind**: ATTACH_QUOTE
- **node slug**: `the-rains-of-castamere`
- **quote** (verbatim, line-confirmed `asos-catelyn-07.md:99`):
  > "No one sang the words, but Catelyn knew 'The Rains of Castamere' when she heard it."
- **chapter:line**: `sources/chapters/asos/asos-catelyn-07.md:99`
- **note**: The node already quotes this from the wiki, but this is the BOOK version with the exact ASOS Catelyn VII chapter:line. Upgrading from wiki-ref to navigable book cite.

---

## P12 — ATTACH_QUOTE: `guest-right` node — Tyrion's one-liner

- **kind**: ATTACH_QUOTE
- **node slug**: `guest-right`
- **quote** (verbatim, line-confirmed `asos-tyrion-06.md:201`):
  > "So much for guest right."
- **chapter:line**: `sources/chapters/asos/asos-tyrion-06.md:201`
- **note**: The `guest-right` node cites Tyrion from the wiki but lacks the direct chapter:line cite. This is Tyrion's immediate reaction to learning Catelyn was killed after invoking guest right — the most economical on-page statement of the RW's sacred-law violation.

---

## P13 — NEW_EDGE: `roose-named-warden-of-the-north ENABLES wedding-of-ramsay-bolton-and-arya-stark`

- **kind**: NEW_EDGE
- **source → type → target**: `roose-named-warden-of-the-north --ENABLES--> wedding-of-ramsay-bolton-and-arya-stark`
- **tier**: Tier-1
- **evidence**: `sources/chapters/asos/asos-tyrion-06.md:207`
  > "Roose Bolton becomes Warden of the North and takes home Arya Stark … Lord Bolton will wed the girl to his bastard son."
- **rationale**: Tywin's settlement explicitly bundles the wardenship with the fArya Stark marriage as a single package. The wardenship ENABLES the Bolton political authority to carry out the marriage, which is the mechanism by which Bolton consolidates the North. `roose-named-warden-of-the-north` was flagged in baseline.md as having 0 downstream edges; this is the highest-value wire. Causal mechanism: the wardenship gives Roose the legal standing (and crown backing) to deliver "Arya Stark" to his bastard son as a political marriage.
- **check**: `roose-named-warden-of-the-north` EXISTS (built, S125). `wedding-of-ramsay-bolton-and-arya-stark` EXISTS (found in event nodes). No ENABLES edge between them in `edges.jsonl`.

---

## Summary (≤200 words)

**Counts**: 4 NEW_NODE proposals (P2, P4, P6, and the optional guest-right violation event embedded in P9); 7 NEW_EDGE proposals (P1, P3, P5, P7, P8, P9-edge, P13); 3 ATTACH_QUOTE proposals (P10, P11, P12).

**3 highest-value items**:

1. **P8 / P7** (`ser-wendel-manderly-is-killed MOTIVATES wyman-manderly-stages-fake-execution-of-davos`): Wires a key causal island (Manderly's revenge arc) to the RW cluster at the personal beat level. The Wyman node has 0 causal inbound edges despite being a major downstream consequence.

2. **P13** (`roose-named-warden-of-the-north ENABLES wedding-of-ramsay-bolton-and-arya-stark`): Closes the gap between Tywin's reward clause and the Bolton political spine. Baseline flagged this node as 0-downstream; this is the primary wire.

3. **P1** (`the-rains-of-castamere TRIGGERS red-wedding`): The song IS the massacre signal — the causal mechanism is explicit in both the catelyn-07 text (Catelyn recognizes it and knows it's too late) and the epilogue (Lothar planned the song selection). Wires an existing text node directly into the RW cluster for the first time.

**Flag**: P9 (guest-right edge) needs schema decision — `CAUSES` between an event and a concept node is a novel pattern; flag for orchestrator to decide type or defer to an ATTACH_QUOTE fallback.
