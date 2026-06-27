# Lens D — Existing-node↔Existing-node Causal Wiring — A2.7 Stannis proposal (S155)

> **Chapters read:** acok-davos-02, acok-davos-03, asos-davos-05 (consulted for NW letter), asos-davos-06, agot-eddard-15, adwd-the-kings-prize-01, adwd-jon-04
> **Dedup baseline:** 409 internal edges + 10-edge causal spine verified against edges.jsonl before any proposal.
> **Lens focus:** cross-container causal seams between TWO already-built nodes — the dyadic web the topic-lenses each call "not mine."

---

## Proposed NEW nodes

None. This lens found no node gaps — all the candidate events anchor to existing slugs. Proposing edges only, as expected for Lens D.

---

## Proposed NEW edges

### D1 — murder-of-jon-arryn MOTIVATES stannis-baratheon

| field | value |
|---|---|
| source_slug | murder-of-jon-arryn |
| edge_type | MOTIVATES |
| target_slug | stannis-baratheon |
| Tier | Tier-2 |
| qualifier | none (MOTIVATES takes none) |
| verbatim quote | "Lord Stannis in particular. His claim is the true one, he is known for his prowess as a battle commander, and he is utterly without mercy. No one knows what Stannis has been doing on Dragonstone" |
| cite | agot-eddard-15:127 |

**Rationale:** Stannis and Jon Arryn investigated the twincest together (established in AGOT/ACOK backstory; Stannis explicitly names Jon Arryn alongside Ned Stark as someone he will have justice for — acok-davos-02:185: "I will have justice for him. Aye, and for Ned Stark and Jon Arryn as well"). Arryn's murder is what panicked Stannis into fleeing to Dragonstone before AGOT opens, sealing his posture of righteous outrage that drives the entire arc. This wires `murder-of-jon-arryn` (currently only outgoing to `lysa-accuses-tyrion`) into the Stannis cluster across the wo5k→Stannis container seam.

**[BORDERLINE]** — the direct Stannis-investigation chapter is not in my assigned files; this is confirmed via cross-book backstory + acok-davos-02:185 quote (Stannis names Jon Arryn as one he will avenge). The MOTIVATES link is strong but requires the synthesizer to confirm the backstory chain is documented in node prose before minting.

---

### D2 — renly-s-death-reflection MOTIVATES stannis-baratheon

| field | value |
|---|---|
| source_slug | renly-s-death-reflection |
| edge_type | MOTIVATES |
| target_slug | stannis-baratheon |
| Tier | Tier-1 |
| qualifier | none (MOTIVATES takes none) |
| verbatim quote | "I dream of it sometimes. Of Renly's dying. A green tent, candles, a woman screaming. And blood." |
| cite | acok-davos-02:189 |

**Rationale:** This closes the MARQUEE gap named in the baseline (gap #3): `renly-s-death-reflection` is causally islanded with cIn=0 and cOut=0. The guilt Stannis carries for his brother's death is text-explicit in the confession Davos receives — "I did love him, Davos. I know that now. I swear, I will go to my grave thinking of my brother's peach." (acok-davos-02:193). The guilt haunts his nightmares and is mediated through Melisandre ("Only the Lady Melisandre can soothe him to sleep" — acok-davos-02:17). MOTIVATES correctly routes the guilt through the character (target = stannis-baratheon, not an event). Tier-1: verbatim text quote, Davos POV at close range. This is the highest-confidence edge in this proposal.

---

### D3 — davos-seaworth MOTIVATES stannis-baratheon [re: the Wall decision]

| field | value |
|---|---|
| source_slug | davos-seaworth |
| edge_type | MOTIVATES |
| target_slug | stannis-baratheon |
| Tier | Tier-2 |
| qualifier | none |
| verbatim quote | "A King's Hand should be able to read and write. Maester Pylos has been teaching me." |
| cite | asos-davos-06:211 |

**Rationale (structural gap — WHY-STANNIS-MARCHES-NORTH, baseline gap #4):** The existing spine has `stannis-retreats-to-dragonstone ENABLES stannis-moves-to-the-wall` but the MOTIVATES (the efficient cause of Stannis's decision to go north) is missing. In asos-davos-06, Davos reads the Night's Watch plea letter aloud to Stannis — this is the "save the realm to win the throne" argument. The scene is textually confirmed: Davos draws out "the crinkled sheet of parchment" and reads it "by the light of the magic sword" (Lightbringer). The Night's Watch letter exists as a prop; Davos-as-persuader is the character who routes the decision. MOTIVATES goes from the persuader (person) to the persuaded (person). Tier-2: the persuasion chapter is confirmed in text but the letter's content isn't shown in full; the persuasion inference is grounded by the asos-davos-05 chapter where Davos reads the letter and decides to bring it to Stannis.

**[BORDERLINE]** — This proposes that `davos-seaworth` motivates `stannis-baratheon` on the specific Wall decision; however, the MOTIVATES edges are person→person and the synthesizer may prefer a more specific framing. The alternative is to flag this as node-prose (in the `stannis-moves-to-the-wall` node's body). Flag for synthesizer judgment.

---

### D4 — the-antler-men-conspiracy ENABLES battle-of-the-blackwater

| field | value |
|---|---|
| source_slug | the-antler-men-conspiracy |
| edge_type | ENABLES |
| target_slug | battle-of-the-blackwater |
| Tier | Tier-2 |
| qualifier | none |
| verbatim quote | "conspiracy of men plotting to open the gates for Stannis" |
| cite | (from existing edge evidence on `the-antler-men-conspiracy` node — not directly in my assigned chapter files) |

**LIGHT TOUCH per baseline instruction (gap #9).** The conspiracy was specifically intended to be Stannis's fifth column inside KL — opening the gates from within to enable his assault. The ENABLES relationship is structural: the Antler Men's existence as an activated fifth column was a precondition Stannis counted on (Tyrion discovers and arrests them). The `the-antler-men-conspiracy` node has AGENT_IN/COMMANDS_IN/LOCATED_AT but no outgoing causal edge. `stannis-baratheon COMMANDS_IN the-antler-men-conspiracy` already exists, and the conspiracy ENABLES the battle assault scenario.

**[BORDERLINE]** — The supporting text (acok-tyrion chapters) is not in my assigned files. Do NOT build out the conspiracy further. Synthesizer: verify from existing `the-antler-men-conspiracy` node prose before minting. If the node prose confirms the fifth-column role, this is a clean Tier-2 structural fix.

---

### D5 — renly-s-death-reflection CAUSES stannis-absorbs-renly-s-host [DROPPED — see below]

Considered but rejected: `shadow-assassination-of-renly CAUSES stannis-absorbs-renly-s-host` already exists. `renly-s-death-reflection` is a separate node (Stannis's nightmare/guilt, not the death itself). Routing `renly-s-death-reflection CAUSES stannis-absorbs-renly-s-host` would be an agency-collapse error — the absorbing of the host was caused by the assassination, not by the guilt. Dropped.

---

## Dropped / considered-but-rejected

**`battle-beneath-the-wall ENABLES stannis-march-on-winterfell`** — Considered (baseline gap #2, my candidate #2). Dropped: the graph already has a complete two-hop path `battle-beneath-the-wall ENABLES fight-by-deepwood-motte ENABLES stannis-march-on-winterfell`. The direct edge would be a redundant shortcut, not a seam fix. Correctly excluded.

**`murder-of-jon-arryn INVESTIGATES / stannis-baratheon INVESTIGATES`** — Considered. The `INVESTIGATES` edge type exists in the vocabulary, but the investigation is already backstory-stated in AGOT and would need dedicated chapter files (agot-eddard chapters, specifically agot-eddard-07 and the investigation arc). Not in my assigned chapters. Edge D1 (MOTIVATES) covers the causal consequence; the investigation step itself is Lens A territory or a future dip. Dropped.

**`siege-of-storms-end-299 ENABLES shadow-assassination-of-renly`** — Considered (baseline gap #2). This is already identified in the baseline as a Lens A/B candidate (gap #2: "shadow-assassination-of-renly has cIn=0"). The `shadow-assassination-of-renly` node and `siege-of-storms-end-299` are both in the dense dyadic web but not in my Lens D scope (no cross-container seam). Dropped — Lens A territory.

**`davos-seaworth RESCUES edric-storm`** — Considered. asos-davos-06 text confirms this: Davos smuggles Edric out on the Mad Prendos. `RESCUES` is in the vocabulary and takes no qualifier. However, this is a PERSON↔PERSON dyadic edge (Lens A/B territory), not a cross-container causal seam. Baseline gap #5 notes it as a candidate. Dropped from Lens D — offer to synthesizer as an add.

**`stannis-baratheon INVESTIGATES incest-of-cersei-and-jaime`** — The discovery is referenced in backstory but the `incest-of-cersei-and-jaime` node (if it exists) is not confirmed. agot-eddard-15 is silent on Stannis's investigation; the chapter is Ned in prison. Dropped — would require a node check + AGOT chapter verification outside my files.

**`the-antler-men-conspiracy PART_OF battle-of-the-blackwater`** — Considered as alternative to ENABLES. PART_OF would imply the conspiracy is a constitutive element of the battle itself. More defensible that it is a precondition (ENABLES) since the conspiracy was neutralized before the battle by Tyrion; it didn't actually execute its opening-the-gates plan. ENABLES wins over PART_OF. (Kept in proposal as D4 with ENABLES.)

**`jon-snow ALLIES_WITH stannis-baratheon` re causal wiring** — Already wired as a dyadic edge. The MOTIVATES substrate (what drove the alliance) is in the existing `battle-beneath-the-wall` chain. The specific Jon-counsel-to-recruit-mountain-clans scene (adwd-jon-04:293: "Jon spread his burned hand across the map, west of the kingsroad and south of the Gift") is already in the Stannis web. The mountain-clans tip ENABLES Deepwood, already wired. No new causal seam here.

---

## Harvest

| kind | book | chapter:line | note |
|---|---|---|---|
| food | acok | acok-davos-02:195 | "the stink of horse dung was heavy in the air, mingled with the woodsmoke and the smell of cooking meat" — camp smell at Storm's End siege; grim register |
| food | acok | acok-davos-02:209 | "Devan set the tray on the table and filled two clay cups. The king sprinkled a pinch of salt in his cup before he drank; Davos took his water straight, wishing it were wine." — Stannis's sparse table habits; salt in water |
| quote | acok | acok-davos-02:193 | "Renly offered me a peach. At our parley. Mocked me, defied me, threatened me, and offered me a peach. I thought he was drawing a blade and went for mine own." — the peach anecdote (for stannis-baratheon ## Quotes or the parley node) |
| quote | acok | acok-davos-02:193 | "Only Renly could vex me so with a piece of fruit. He brought his doom on himself with his treason, but I did love him, Davos. I know that now. I swear, I will go to my grave thinking of my brother's peach." — Stannis's love for Renly, verbatim |
| description | acok | acok-davos-02:107 | "Seen at close hand, Stannis looked worse than Davos had realized from afar. His face had grown haggard, and he had dark circles under his eyes." — physical description of Stannis during Storm's End siege |
| description | acok | acok-davos-02:17 | "He looks half a corpse too, years older than when I left Dragonstone... Devan said the king scarcely slept of late. 'Since Lord Renly died, he has been troubled by terrible nightmares'" — Stannis's nightmares; Mel soothes him |
| description | adwd | adwd-the-kings-prize-01:135 | "His eyes were sunk in deep pits, his close-cropped beard no more than a shadow across his hollow cheeks and bony jawbone. Yet there was power in his stare, an iron ferocity that told Asha this man would never, ever turn back from his course." — Stannis during the march, physical description |
| food | adwd | adwd-the-kings-prize-01:157 | "They supped that night on a venison stew made from a scrawny hart that a scout called Benjicot Branch had brought down. But only in the royal tent. Beyond those canvas walls, each man got a heel of bread and a chunk of black sausage no longer than a finger, washed down with the last of Galbart Glover's ale." — army rations during march, contrast between king's table and common soldiers |
| food | adwd | adwd-the-kings-prize-01:179 | "King Stannis... a dish of onion soup cooled before him, hardly tasted, staring at the flame of the nearest candle" — Stannis not eating during march; the queen's men urging sacrifice |
| food | adwd | adwd-the-kings-prize-01:221 | "On the twenty-sixth day of the fifteen-day march, the last of the vegetables was consumed. On the thirty-second day, the last of the grain and fodder. Asha wondered how long a man could live on raw, half-frozen horse meat." — starvation conditions during march |
| food | adwd | adwd-the-kings-prize-01:191 | "destriers began to perish of exhaustion and exposure... Any horse that went down was butchered on the spot for meat." — horsemeat eaten during march; grim register |
| hospitality | adwd | adwd-the-kings-prize-01:129 | "When Ser Justin Massey rode up, he told them to butcher the dead horse for meat and break up the wagon for firewood." — hospitality inverted (the "host" consumes its own transport) |
| description | adwd | adwd-the-kings-prize-01:131 | "Atop its center pole flew the royal standard, golden, with a stag's head within a burning heart. On three sides the pavilions of the southron lordlings who had come north with Stannis surrounded it. On the fourth side the nightfire roared" — Stannis's tent and nightfire layout during the march |
| quote | asos | asos-davos-06:195 | "I never asked for this crown. Gold is cold and heavy on the head, but so long as I am the king, I have a duty . . . If I must sacrifice one child to the flames to save a million from the dark . . . Sacrifice . . . is never easy, Davos. Or it is no true sacrifice." — Stannis on duty; for stannis-baratheon ## Quotes |
| description | adwd | adwd-jon-04:81 | "Rattleshirt tapped the ruby on his wrist. 'Ask your red witch, bastard.' Melisandre spoke softly in a strange tongue. The ruby at her throat throbbed slowly, and Jon saw that the smaller stone on Rattleshirt's wrist was brightening and darkening as well." — Mel's ruby control of Rattleshirt; ruby description |
| food | adwd | adwd-jon-04:313 | "'For three thousand men, I suppose I can endure some pipes and porridge,' the king said, though his tone begrudged even that." — Stannis on feasting with mountain clans; food as politics |
| quote | acok | acok-davos-02:185 | "I have no doubt that Cersei had a hand in Robert's death. I will have justice for him. Aye, and for Ned Stark and Jon Arryn as well." — Stannis names those he'll avenge; book-cite for justice motive |
| foreshadowing | acok | acok-davos-02:235 | "'So did my brother, the day before his death. The night is dark and full of terrors, Davos.' // Davos Seaworth felt the small hairs rising on the back of his neck. 'My lord, I do not understand you.'" — Stannis foreshadowing Cortnay's death via Mel's flames |
| description | acok | acok-davos-02:351 | "Melisandre had thrown back her cowl and shrugged out of the smothering robe. Beneath, she was naked, and huge with child. Swollen breasts hung heavy against her chest, and her belly bulged as if near to bursting." — shadow-birth; Mel's description during birth scene |
| description | acok | acok-davos-02:353 | "He had only an instant to look at it before it was gone, twisting between the bars of the portcullis and racing across the surface of the water, but that instant was long enough. He knew that shadow. As he knew the man who'd cast it." — shadow identified as Stannis by Davos; load-bearing witness line |
