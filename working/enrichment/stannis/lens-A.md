# Lens A — spine + secondary-character sub-arcs — A2.7 Stannis proposal (S155)

## Proposed NEW nodes

### `burning-of-the-seven-at-dragonstone`
- **type:** event.incident
- **body:** The burning of the seven carved idols of the Faith of the Seven at Dragonstone's gates, conducted by Melisandre at Stannis's command. Melisandre walks the fire three times praying in three tongues; Stannis then draws the sword later called Lightbringer from the pyre. This is the public act of conversion that marks Stannis's adoption of R'hllor as his god and his break with the Faith of the Seven.
- **anchor quote:** "R'hllor, come to us in our darkness," she called. "Lord of Light, we offer you these false gods, these seven who are one, and him the enemy." — `acok-davos-01:21`

---

### `shadow-assassination-of-cortnay-penrose`
- **type:** event.death
- **body:** The killing of Ser Cortnay Penrose, castellan of Storm's End, by a shadow-creature born from Melisandre in the sea cave beneath the castle. Davos rows Melisandre into the cave; she births a shadow that slips through the portcullis bars into the castle and kills Cortnay before dawn. Command of Storm's End passes to young Lord Meadows, who then yields the castle to Stannis.
- **anchor quote:** "two arms wriggled free, grasping, black fingers coiling around Melisandre's straining thighs, pushing, until the whole of the shadow slid out into the world and rose taller than Davos, tall as the tunnel" — `acok-davos-02:353`

---

### `leeching-of-edric-storm`
- **type:** event.incident
- **body:** The ritual leeching of Edric Storm, supervised by Melisandre and conducted in Stannis's presence at Dragonstone. Three leeches fat with Edric's blood are named for "the usurper Joffrey Baratheon / the usurper Balon Greyjoy / the usurper Robb Stark" and thrown into the brazier. Melisandre presents this as a demonstration of king's-blood power; Stannis participates while Davos watches, horrified. Joffrey Baratheon and Balon Greyjoy are dead by the time this chapter ends; Robb Stark dies at the Red Wedding.
- **anchor quote:** "The usurper," he declared, louder this time. "Balon Greyjoy." He flipped it lightly onto the brazier, and its flesh split and cracked. — `asos-davos-04:281`
- **note (GATED):** Whether the leeching causes the three deaths is GATED — node-prose only; no `leeching FORESHADOWS/CAUSES` edges proposed.

---

### `davos-rescues-edric-storm`
- **type:** event.incident
- **body:** Davos Seaworth, as King's Hand, secretly smuggles Edric Storm out of Dragonstone onto Salladhor Saan's galley Mad Prendos while Stannis and Melisandre attend a nightfire. Davos organizes Ser Andrew Estermont, the Bastard of Nightsong, Ser Gerald Gower, Lewys the Fishwife, and Omer Blackberry as co-conspirators. He then presents himself to Stannis and reads the Night's Watch letter, pivoting Stannis's attention north.
- **anchor quote:** "Your Grace, you made me swear to give you honest counsel and swift obedience, to defend your realm against your foes, to protect your people. Is not Edric Storm one of your people? One of those I swore to protect? I kept my oath." — `asos-davos-06:193`

---

### `renly-s-death-reflection`
*NOTE: Checking baseline — this node is ALREADY named in the baseline as an existing islanded node ("renly-s-death-reflection is causally ISLANDED"). It exists in the graph. Do NOT re-propose the node itself, only wire it.*

---

### `storm-s-end-siege-starvation-299`
*NOTE: The baseline references `siege-of-storms-end-299` as an existing node. Do not re-mint.*

---

## Proposed NEW edges

### GAP 1 — The R'hllor conversion engine

**E1**
`stannis-baratheon` WORSHIPS `rhllor`
| Tier-1 | no qualifier |
"I know little and care less of gods, but the red priestess has power." — `acok-davos-01:257`
*Rationale: Stannis explicitly commits to R'hllor as his new "hawk," having burned the Seven. His own words frame the conversion as instrumental, but the burning-of-the-Seven is the public act. The above quote is the clearest direct statement of Stannis choosing this god.*

**E2**
`melisandre` ADVISES `stannis-baratheon`
| Tier-1 | no qualifier |
"I know little and care less of gods, but the red priestess has power … I mean to find out." — `acok-davos-01:257-263`
*Rationale: Stannis's own speech to Davos describing why he has chosen Melisandre as counsel — the canonical "red hawk" passage. No ADVISES edge currently exists per baseline; SERVES/COMPANION_OF/LOVER_OF do exist but ADVISES is the advisory role this passage establishes.*

**E3**
`melisandre` AGENT_IN `burning-of-the-seven-at-dragonstone`
| Tier-1 | no qualifier |
"The red woman walked round the fire three times, praying once in the speech of Asshai, once in High Valyrian, and once in the Common Tongue." — `acok-davos-01:21`
*Rationale: Melisandre physically conducts the ceremony.*

**E4**
`stannis-baratheon` AGENT_IN `burning-of-the-seven-at-dragonstone`
| Tier-1 | no qualifier |
"The king plunged into the fire with his teeth clenched, holding the leather cloak before him to keep off the flames. He went straight to the Mother, grasped the sword with his gloved hand, and wrenched it free of the burning wood with a single hard jerk." — `acok-davos-01:45`
*Rationale: Stannis performs the central physical act — drawing Lightbringer — and then walks away with the sword. He is clearly agent/co-participant.*

**E5**
`selyse-baratheon` PARTICIPATES_IN `burning-of-the-seven-at-dragonstone`
| Tier-1 | no qualifier |
"Queen Selyse echoed the words." — `acok-davos-01:21`
*Rationale: Selyse joins the responses, confirming active participation. Already WORSHIPS rhllor per baseline, but her role in this specific event is unrecorded.*

**E6**
`davos-seaworth` WITNESS_IN `burning-of-the-seven-at-dragonstone`
| Tier-1 | no qualifier |
"Hundreds had come to the castle gates to bear witness to the burning of the Seven … Davos watched them burn, and not only from the smoke." — `acok-davos-01:19, 25`
*Rationale: Davos is present and watching at the burning; this is a load-bearing perception (it grounds his misgivings and his later opposition to Melisandre). He explicitly watches; not shielded.*

**E7**
`lightbringer` WIELDED_IN `burning-of-the-seven-at-dragonstone`
| Tier-1 | no qualifier |
"He went straight to the Mother, grasped the sword with his gloved hand, and wrenched it free of the burning wood with a single hard jerk. Then he was retreating, the sword held high, jade-green flames swirling around cherry-red steel." — `acok-davos-01:45`
*Rationale: Lightbringer is drawn from the fire as the ceremonial act's climax.*

**E8**
`stannis-baratheon` WIELDS `lightbringer`
| Tier-1 | no qualifier |
"Stannis drew his longsword. Lightbringer, Melisandre had named it; the red sword of heroes, drawn from the fires where the seven gods were consumed. The room seemed to grow brighter as the blade slid from its scabbard." — `asos-davos-04:195`
*Rationale: Lightbringer has 0 edges graph-wide per baseline; this is explicitly listed as a target.*

**E9**
`burning-of-the-seven-at-dragonstone` ENABLES `shadow-assassination-of-renly`
| Tier-2 |
"I know little and care less of gods, but the red priestess has power … The red woman. Half my knights are afraid even to say her name … if she can do nothing else, a sorceress who can inspire such dread in grown men is not to be despised. And perhaps she can do more. I mean to find out." — `acok-davos-01:261`
*Rationale: The burning of the Seven formalizes Stannis's alliance with Melisandre and makes the shadow-births possible — it is the precondition that enables Melisandre's full power to operate on Stannis's behalf. Human choices (Stannis's decision to deploy her) intervene, so ENABLES not CAUSES.*

---

### GAP 2 — The Renly's-war upstream / shadow-baby spine

**E10**
`siege-of-storms-end-299` ENABLES `shadow-assassination-of-renly`
| Tier-2 |
"Lord Velaryon and your friend Salladhor Saan would have had me sail against Joffrey, but Melisandre told me that if I went to Storm's End, I would win the best part of my brother's power, and she was right." — `acok-davos-02:239`
*Rationale: The siege brought both armies to Storm's End; the parley followed from the siege, and the shadow killing was a direct consequence of Renly's arrival to relieve it. ENABLES because Renly's arrival (a free agent) and Melisandre's action are the actual causes.*

**E11**
`stannis-renly-parley` TRIGGERS `shadow-assassination-of-renly`
| Tier-2 |

**[BORDERLINE]** — I am proposing this as a new event node (`stannis-renly-parley`) which may not exist in the graph. The parley is the direct immediate precursor: parley fails → no agreement → assassination that same night. The text is strongly sequential: "Come the dawn, we shall see." (acok-catelyn-03:193); then in acok-catelyn-04 the shadow arrives before dawn. However, if `stannis-renly-parley` is not already a node, this requires minting a new event. Flagging for gate.
"We shall see, brother … Come the dawn, we shall see." — `acok-catelyn-03:193`
*Rationale: The parley is the turning point — Stannis offers terms, Renly refuses, dawn is set as the battle hour. The shadow strikes before that dawn. The parley is the final beat before the assassination; TRIGGERS (immediate spark) is warranted.*

**E12**
`catelyn-stark` WITNESS_IN `shadow-assassination-of-renly`
| Tier-1 | no qualifier |
"She thought she glimpsed movement, but when she turned her head, it was only the king's shadow shifting against the silken walls … and then she saw Renly's sword still in its scabbard, sheathed still, but the shadowsword …" — `acok-catelyn-04:93-95`
*Rationale: Catelyn is in the tent. She physically sees the shadow. This is a load-bearing perception — she names Stannis as the killer to Robar Royce on this basis: "I swear it, you know me, it was Stannis killed him." (`acok-catelyn-04:113`). WITNESS_IN is warranted.*

**E13**
`brienne-of-tarth` WITNESS_IN `shadow-assassination-of-renly`
| Tier-1 | no qualifier |
"'Your Gr—no!' cried Brienne the Blue when she saw that evil flow" — `acok-catelyn-04:97`
*Rationale: Brienne is present, holding Renly as he dies. She saw the shadow (Catelyn confirms this in her conversation with her: "I saw a shadow. I thought it was Renly's shadow at the first, but it was his brother's." `acok-catelyn-04:129-130`). Load-bearing — grounds her vow to kill Stannis.*

**E14**
`brienne-of-tarth` VOWS_TO `kill-stannis-baratheon`

**[BORDERLINE]** — `kill-stannis-baratheon` is not an entity node; it's a character's intent. The correct pattern is probably `brienne-of-tarth VOWS_TO stannis-baratheon` (the vow is directed at him as her target). But VOWS_TO as an edge type expects a character or place target. Check schema — if VOWS_TO[target = stannis-baratheon] is valid, emit it as Tier-1. If not, could also use `brienne-of-tarth HATES stannis-baratheon` (already in baseline? — check). The canon text is clear:
"'I will kill him,' the tall homely girl declared." — `acok-catelyn-04:135`
*Rationale: The vow is the direct consequence of her witnessing. Noting that HATES/RESENTS may already exist per baseline dense web; need gate to check.*

**E15**
`davos-seaworth` PARTICIPATES_IN `shadow-assassination-of-cortnay-penrose`
| Tier-1 | no qualifier |
"It is not for me to question the king's commands, and yet … And so it was that he found himself once more crossing Shipbreaker Bay in the dark of night, steering a tiny boat with a black sail." — `acok-davos-02:277`
*Rationale: Davos physically rows Melisandre into the cave. He does not cast the shadow; Melisandre does. PARTICIPATES_IN (non-combat involvement) is correct.*

**E16**
`melisandre` AGENT_IN `shadow-assassination-of-cortnay-penrose`
| Tier-1 | no qualifier |
"two arms wriggled free, grasping, black fingers coiling around Melisandre's straining thighs, pushing, until the whole of the shadow slid out into the world and rose taller than Davos" — `acok-davos-02:353`
*Rationale: Melisandre births the shadow that kills Cortnay. She is the agent.*

**E17**
`cortnay-penrose` VICTIM_IN `shadow-assassination-of-cortnay-penrose`
| Tier-1 | no qualifier |
"Ser Cortnay will be dead within the day. Melisandre has seen it in the flames of the future." — `acok-davos-02:239`
*Rationale: Cortnay is explicitly the target. He dies before dawn; Stannis is told of it; Storm's End falls.*

**E18**
`shadow-assassination-of-cortnay-penrose` ENABLES `stannis-absorbs-renly-s-host`
| Tier-2 |
"Ser Cortnay's lieutenant is cousin to the Fossoways. Lord Meadows, a green boy of twenty. Should some ill chance strike down Penrose, command of Storm's End would pass to this stripling, and his cousins believe he would accept my terms and yield up the castle." — `acok-davos-02:227-228`
*Rationale: Cortnay's death clears Storm's End, which Stannis needed as the base and symbol of his power to absorb the remnant southron lords who had followed Renly. The castle's fall contributes to the absorption.*

**E19**
`shadow-assassination-of-cortnay-penrose` LOCATED_AT `storms-end`
| Tier-1 | no qualifier |
"steering a tiny boat with a black sail … a mouth yawned in the cliff, and it was that Davos steered for … The tunnel opened on a cavern under the castle" — `acok-davos-02:337-341`
*Rationale: The event takes place in the sea cave beneath Storm's End.*

---

### GAP 3 — The Renly-kinslaying GUILT MOTIVATES substrate

**E20**
`renly-s-death-reflection` MOTIVATES `stannis-baratheon`
| Tier-1 | no qualifier |
"I dream of it sometimes. Of Renly's dying. A green tent, candles, a woman screaming. And blood." — `acok-davos-02:189`
*Rationale: This is the MOTIVATES target the baseline identifies as missing. Stannis's guilt/grief over Renly haunts him in dreams and shapes his psychology — the reflection is causally connected to his character. Target is stannis-baratheon (a character), honoring MOTIVATES contract.*

**E21**
`shadow-assassination-of-renly` MOTIVATES `stannis-baratheon`
| Tier-2 |
"Renly brought his doom on himself with his treason, but I did love him, Davos. I know that now. I swear, I will go to my grave thinking of my brother's peach." — `acok-davos-02:193`
*Rationale: The assassination haunts Stannis as a source of guilt/grief that motivates his driven severity — he loved Renly and cannot undo the act. MOTIVATES(→character), not an event CAUSES event.*

---

### GAP 4 — Why-Stannis-marches-north MOTIVATES

**E22**
`davos-seaworth` MOTIVATES `stannis-baratheon`
| Tier-1 | no qualifier |
"a king protects his people, or he is no king at all." — `asos-davos-06:203`
*Rationale: Davos's moral argument to Stannis — "a king protects his people" — is the direct cause that pivots Stannis from Edric Storm toward the Night's Watch letter and ultimately north. Davos reads the Wall letter to Stannis at the end of asos-davos-06; this is the persuasion moment. The edge reflects Davos as the agent who MOTIVATES Stannis's decision to go north. Note: there is also a `wedding-of-ramsay MOTIVATES stannis` in the existing spine; this is the Davos-argument predecessor to that.*

**E23**
`battle-beneath-the-wall` ENABLES `stannis-march-on-winterfell`
| Tier-2 |
"Stannis had smashed Mance Rayder's wildlings at the Wall and cleaned Asha and her ironborn out of Deepwood Motte; he was Robert's brother, victor in a famous sea battle off Fair Isle, the man who had held Storm's End all through Robert's Rebellion." — `adwd-the-kings-prize-01:67`
*Rationale: The victory at the Wall gives Stannis the credibility and the base (Castle Black) from which the march south begins. He cannot march on Winterfell without first being at the Wall. ENABLES (precondition; the march is still his own decision).*

**E24**
`iron-bank-loan` ENABLES `stannis-moves-to-the-wall`

**[BORDERLINE]** — The Iron Bank is referenced in baseline (`tycho-nestoris SEEKS stannis`); an `iron-bank-loan` event node may not exist. The text in asos-davos-06 does not directly name the loan in context of the north decision — the loan is more central to the Iron Bank track. Flagging as BORDERLINE. If the node exists, the edge is: the loan gives Stannis financial means to fund the northern campaign. Do NOT mint `iron-bank-loan` node here; gate should verify if it exists before wiring.

**E25**
`night-s-watch-appeal-for-aid`
**[NEW NODE — BORDERLINE]** — The letter that Davos reads aloud in asos-davos-06 is the Night's Watch plea to the "five kings" about Mormont's ravens and Mance Rayder's advance. Davos reads it to Stannis; this triggers Stannis's decision to go north. This may already be a node (checking baseline — not listed in the sampled existing edges). If it does not exist, it is the strongest TRIGGERS candidate for `stannis-moves-to-the-wall`. Flagging for gate.
Anchor: "To the five kings … The King beyond the Wall comes south. He leads a vast host of wildlings. Lord Mormont sent a raven from the haunted forest. He is under attack … We fear Mormont slain with all his strength." — `asos-davos-05:253-269`

If `night-s-watch-appeal-for-aid` can be minted:
`night-s-watch-appeal-for-aid` TRIGGERS `stannis-moves-to-the-wall`
| Tier-2 |
"Davos fumbled inside his cloak and drew out the crinkled sheet of parchment … and began to read by the light of the magic sword." — `asos-davos-06:211-212`
*Rationale: Davos reads this letter at the climactic moment of asos-davos-06; it is the final beat that causes Stannis to sail north rather than executing Davos or burning Edric Storm. This is as close to an immediate TRIGGERS as possible.*

---

### GAP 5 — Sacrifice / queen's-men / leeching

**E26**
`melisandre` AGENT_IN `leeching-of-edric-storm`
| Tier-1 | no qualifier |
"Reaching up her left sleeve with her right hand, she flung a handful of powder into the brazier … the red woman retrieved the silver dish and brought it to the king. Davos watched her lift the lid. Beneath were three large black leeches, fat with blood." — `asos-davos-04:271-273`
*Rationale: Melisandre retrieves and presents the leeches for the ritual.*

**E27**
`stannis-baratheon` AGENT_IN `leeching-of-edric-storm`
| Tier-1 | no qualifier |
"Stannis stretched forth a hand, and his fingers closed around one of the leeches … 'The usurper,' he said. 'Joffrey Baratheon.' When he tossed the leech into the fire, it curled up like an autumn leaf amidst the coals, and burned." — `asos-davos-04:275-279`
*Rationale: Stannis physically names and throws each leech. He is the active agent in the naming ritual.*

**E28**
`edric-storm` VICTIM_IN `leeching-of-edric-storm`
| Tier-1 | no qualifier |
"The boy is sick. Maester Pylos has been leeching him … It is Robert's bastard who is sick, the boy we took at Storm's End." — `asos-davos-04:165-169`
*Rationale: The blood in the leeches is Edric's — taken while he was being treated for his illness. He is the victim.*

**E29**
`davos-seaworth` WITNESS_IN `leeching-of-edric-storm`
| Tier-1 | no qualifier |
"Davos watched her lift the lid. Beneath were three large black leeches, fat with blood. The boy's blood, Davos knew. A king's blood." — `asos-davos-04:272-273`
*Rationale: Davos is present, explicitly watching the ritual and comprehending its significance. Load-bearing perception — the horror of this scene drives his decision to rescue Edric.*

**E30**
`leeching-of-edric-storm` MOTIVATES `davos-seaworth`
| Tier-1 | no qualifier |
"Sometimes the storm winds blow so strong a man has no choice but to furl his sails … part of him wanted nothing so much as to take Devan and go home. I cannot. Not yet. I am a lord now, and the King's Hand, I must not fail him." — `asos-davos-05:157-159`
*Rationale: The leeching scene crystallizes Davos's resolve to save Edric. The text of asos-davos-05 shows Davos agonizing over the leeching before deciding to act; asos-davos-06 shows him acting. MOTIVATES(→davos-seaworth) is correct type.*

**E31**
`leeching-of-edric-storm` ENABLES `davos-rescues-edric-storm`
| Tier-2 |
"He had not lied to his king's men, about that or any of it … 'The red woman may see what we intend,' he warned them." — `asos-davos-06:41`
*Rationale: The leeching is the event that convinces Davos to act; the decision to rescue Edric is made in light of knowing what Melisandre intends. ENABLES (precondition; Davos's decision is the intervening free choice).*

**E32**
`davos-seaworth` RESCUES `edric-storm`
| Tier-1 | no qualifier |
"He is aboard a Lyseni galley, safely out to sea." — `asos-davos-06:177`
*Rationale: Davos physically organizes and executes the rescue; Edric is smuggled out. RESCUES is exact type per LENS-SHARED vocab notes.*

**E33**
`selyse-baratheon` AGENT_IN `queen-s-faction-urges-sacrifice-of-edric-storm`

**[BORDERLINE]** — This node (`queen-s-faction-urges-sacrifice-of-edric-storm`) already exists per the baseline (melisandre AGENT_IN listed). Selyse's explicit role: "Lord husband, you have more men than Aegon did three hundred years ago. All you lack are dragons … Give the boy to me and you need never hear his name spoken again … On bended knee I beg you, sire. Wake the stone dragon" — `asos-davos-05:43-66`. Selyse is co-agent in the urging; if AGENT_IN is already wired for Melisandre and Ser Axell, Selyse may still be missing. Flag for gate dedup check.
"Queen Selyse went to the king's side. 'The Lord of Light sent Melisandre to guide you to your glory. Heed her, I beg you.'" — `asos-davos-05:35-36`

**E34**
`axell-florent` AGENT_IN `queen-s-faction-urges-sacrifice-of-edric-storm`

**[BORDERLINE]** — Same node, Ser Axell's explicit urging: "On bended knee I beg you, sire. Wake the stone dragon and let the traitors tremble." — `asos-davos-05:63`. Gate should check if Axell is already wired to this event.

---

### GAP 6 — Secondary characters: Cressen

**E35**
`maester-cressen` SUSPECTED_OF `poisoning-melisandre`

**[BORDERLINE]** — The text makes this essentially confirmed in-universe (Davos sees him do it: "He had seen the maester slip something into the wine cup. Poison. What else could it be?" — `acok-davos-01:27`). This is Tier-2 because it is Davos's inference, not an explicit authored statement. The result (Melisandre survives, Cressen dies) is confirmed. However, `maester-cressen` KILLS `melisandre` would be wrong (she survives). The correct edge is SUSPECTED_OF or we need `cressen POISONS melisandre` (attempt that failed). Per LENS-SHARED: SUSPECTED_OF is Tier-2 only, for genuinely unproven agency. This IS proven by Davos's eyewitness; the better edge is probably `cressen POISONS melisandre` (an attempt) or `cressen ATTACKS melisandre`. Let the gate decide the type. Proposing:

`maester-cressen` POISONS `melisandre`
| Tier-2 |
"He had seen the maester slip something into the wine cup. Poison. What else could it be? He drank a cup of death to free Stannis from Melisandre, but somehow her god shielded her." — `acok-davos-01:27`
*Rationale: Davos witnessed the act. Cressen attempts to poison Melisandre using the strangler; she drinks and survives; he drinks and dies. The attempt is textually confirmed by Davos's witness; the failure is confirmed by the outcome. POISONS is the correct type (per vocab: "POISONS: the act of poisoning, successful or not").*

**E36**
`maester-cressen` VICTIM_IN `cressen-s-death`

**[BORDERLINE]** — This may already be a node/edge. If `cressen-s-death` or a similar node exists, check. If it does not, proposing the event node and the VICTIM_IN edge. The death is directly described at acok-prologue:381. Flagging as BORDERLINE pending gate dedup.

**E37**
`melisandre` KILLS `maester-cressen`
| Tier-2 |
"His words caught in his throat. His cough became a terrible thin whistle as he strained to suck in air … while the red woman looked down on him in pity, the candle flames dancing in her red red eyes." — `acok-prologue:380-381`
*Rationale: Cressen dies because his own poison — intended for Melisandre — kills him instead. She does not directly administer it, but her resistance to the poison (via her god, per the text) causes his death. The baseline already has `melisandre KILLS cressen` listed. Dropping this edge — already in the web. DEDUP.*

---

### GAP 7 — Secondary character: Cortnay Penrose sub-arc

**E38**
`cortnay-penrose` GUARDS `storm-s-end`
| Tier-1 | no qualifier (event-role type) |
"Bring on your storm, my lord—and recall, if you do, the name of this castle." — `acok-davos-02:93`
*Rationale: Cortnay Penrose is the castellan defending Storm's End for Renly. His GUARDS role is the basis for the entire Shadow-assassination sub-arc. `GUARDS` takes no qualifier.*

**E39**
`cortnay-penrose` GUARDS `edric-storm`
| Tier-1 | no qualifier |
"Then my answer is still no, my lord." — `acok-davos-02:47` (in response to Stannis demanding Edric Storm)
*Rationale: Cortnay's entire refusal is predicated on his protection of Edric Storm: "And what of Edric Storm?" / "My brother's bastard must be surrendered to me." / "Then my answer is still no." He GUARDS the boy as well as the castle.*

**E40**
`stannis-baratheon` BESIEGES `storm-s-end` (at `siege-of-storms-end-299`)

**[BORDERLINE]** — The baseline already has `stannis BESIEGES storms-end` in the dense web. DEDUP. Dropping.

---

### GAP 8 — Davos's conversion misgivings wired

**E41**
`burning-of-the-seven-at-dragonstone` MOTIVATES `davos-seaworth`
| Tier-1 | no qualifier |
"The gods had never meant much to Davos the smuggler, though like most men he had been known to make offerings to the Warrior before battle … He felt ill as he watched them burn, and not only from the smoke." — `acok-davos-01:25`
*Rationale: The burning crystallizes Davos's misgivings about Melisandre and the R'hllor conversion — it becomes the seed of his opposition to Melisandre throughout the arc. MOTIVATES(→davos-seaworth) as a driver of his caution.*

---

### GAP 9 — Patchface as foreshadowing node (check if exists)

No edge proposed here — Patchface's songs are too interpretive for this lens. Harvest only (see below).

---

### GAP 10 — Jon Snow / Stannis at the Wall alliance

**E42**
`stannis-baratheon` ALLIES_WITH `jon-snow`
**DEDUP** — baseline already has `jon-snow ALLIES_WITH stannis` listed. Dropping.

**E43**
`jon-snow` ADVISES `stannis-baratheon`
| Tier-2 |
"'Your Grace, might I know if the Umbers have declared for you?' … Jon gave him the detailed strategic analysis of the Dreadfort march, the mountain clans, and Deepwood Motte." — `adwd-jon-04:123-323` (extended exchange)
*Rationale: Jon advises Stannis extensively at Castle Black: Mors Umber's terms, Dreadfort vulnerabilities, the mountain clans, Deepwood Motte strategy. This strategic counsel distinguishes from ALLIES_WITH. ADVISES(jon-snow→stannis-baratheon). Check if any such edge exists already; not listed in baseline samples.*

---

## Dropped / considered-but-rejected

1. **`stannis CAUSES shadow-assassination-of-renly` (direct causal)** — DEDUP; `stannis-baratheon AGENT_IN shadow-assassination-of-renly` already exists per baseline. AGENT_IN is the correct edge here; adding a CAUSES would be double-counting and incorrect (Stannis is agent, not cause in the abstract).

2. **`shadow-assassination-of-renly FORESHADOWS shadow-assassination-of-cortnay-penrose`** — Dropped. Too interpretive; the second shadow is textually ordered after the first but not presented as foreshadowing, just as a second use of the same power. Not an edge type warranted here.

3. **`leeching-of-edric-storm CAUSES/FORESHADOWS` deaths of Joffrey/Balon/Robb** — GATED. Hard rule from LENS-SHARED. Node-prose only. Not proposed.

4. **`stannis-baratheon PRACTICES shadowbinding`** — PRACTICES is `person→concept.magic discipline`. The `shadowbinding` concept node may not exist; Stannis is not the practitioner — Melisandre is. Dropping for Stannis; considering for Melisandre but out of scope for Lens A's focus.

5. **`melisandre PRACTICES shadowbinding`** — Out of scope for Lens A (Lens C covers objects/magic depth). Flagging as harvest note.

6. **`renly-baratheon VICTIM_IN shadow-assassination-of-renly`** — DEDUP; baseline already has `renly VICTIM_IN` the event. Dropping.

7. **`catelyn-stark SUSPECTED_OF shadow-assassination-of-renly`** — This is in-world accusation by Guyard Morrigen, not a true graph assertion. Dropped — Catelyn is innocent; a SUSPECTED_OF edge would propagate a false accusation without grounding. The text is clear Catelyn witnessed Stannis's shadow.

8. **Stannis's backstory — Storm's End starvation (eating rats during RR)** — Mentioned in baseline as a node-prose candidate (GAP 7: onion-smuggling backstory). The text reference is Renly telling Catelyn about it in acok-catelyn-04:61-63. No new node warranted from my chapters alone; this is historical backstory. Harvest-only.

9. **`brienne-of-tarth MOURNS renly-baratheon`** — The death scene strongly supports this. However, checking baseline: the dense web section doesn't explicitly list Brienne MOURNS Renly. This edge might be legitimate; however, MOURNS is a deep character-arc edge more suited to Lens B (character perception layer). Dropping from this lens to avoid scope creep.

10. **`stannis-baratheon KILLS cortnay-penrose`** — Stannis does not personally kill Cortnay; Melisandre's shadow does, by his indirect command. The COMMANDS_IN edge or AGENT_IN is the appropriate type. Checking baseline: baseline has `stannis AGENT_IN {shadow-assassination-of-renly}` but not shadow-assassination-of-cortnay-penrose. Proposing `stannis COMMANDS_IN shadow-assassination-of-cortnay-penrose` per E44 below.

**E44**
`stannis-baratheon` COMMANDS_IN `shadow-assassination-of-cortnay-penrose`
| Tier-2 |
"Ser Cortnay will be dead within the day. Melisandre has seen it in the flames of the future. His death and the manner of it … I do not require your understanding. Only your service." — `acok-davos-02:239-262`
*Rationale: Stannis orders Davos to row Melisandre in; he knows what will happen. He commands without personally executing. COMMANDS_IN is the role type.*

11. **`stannis-baratheon KILLS cressen`** — The baseline says `melisandre KILLS cressen`. The death is Cressen's own poison rebound. Stannis does not command Cressen's death; in fact the text says he "never wanted Cressen at that feast" and "had hoped he might be granted a few years of ease." (`acok-davos-01:209`). Dropping.

12. **`davos-seaworth PARTICIPATES_IN leeching-of-edric-storm`** — Davos is present but not a participant in the ritual; he is a witness. WITNESS_IN already proposed (E29). PARTICIPATES_IN would be double-counting.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|--------------|------|
| food/feast | ACOK | acok-prologue:287 | "the lower tables were crowded with knights, archers, and sellsword captains, tearing apart loaves of black bread to soak in their fish stew" — Dragonstone feast before Cressen's poison attempt |
| food/drink | ACOK | acok-davos-01:91 | Salladhor Saan eating "grapes from a wooden bowl" at Dragonstone inn — "Marvelously sweet" |
| food/feast | ACOK | acok-davos-01:147 | Salladhor Saan's dinner: "Minced lamb with pepper and roasted gull stuffed with mushrooms and fennel and onion" aboard Valyrian |
| drink | ACOK | acok-davos-01:100 | Davos orders "a tankard of ale" at the inn after the burning ceremony |
| food/hospitality | ACOK | acok-catelyn-02:205 | Renly's feast at Bitterbridge: "pears poached in wine … tiny savory fish rolled in salt and cooked crisp … capons stuffed with onions and mushrooms … immense hams and roast geese and trenchers dripping full of venison stewed with beer and barley … cream swans and spun-sugar unicorns, lemon cakes in the shape of roses, spiced honey biscuits and blackberry tarts, apple crisps and wheels of buttery cheese" — the extravagant last feast before Renly's death |
| drink/food | ACOK | acok-catelyn-03:155 | The peach — Renly produces a peach at the parley and eats it while mocking Stannis; Stannis later confesses to Davos he will go to his grave thinking of it |
| food/starvation | ACOK | acok-catelyn-04:61-63 | Renly tells Catelyn: "Near the end, Ser Gawen Wylde and three of his knights tried to steal out a postern gate to surrender. Stannis caught them … Maester Cressen told Stannis that we might be forced to eat our dead" — Storm's End starvation during Robert's Rebellion; rats-and-corpses detail |
| food/starvation | ACOK | acok-catelyn-03:15 | "Stannis Baratheon's foragers had cut the trees down for his siege towers and catapults" — the land stripped for wood; implicit supply pressure |
| food/starvation | ADWD | adwd-the-kings-prize-01:157 | "Beyond those canvas walls, each man got a heel of bread and a chunk of black sausage no longer than a finger, washed down with the last of Galbart Glover's ale" — winter march rations, day 3 |
| food/starvation | ADWD | adwd-the-kings-prize-01:192 | Destriers dying, being "butchered on the spot for meat"; horsemeat as emergency food on the Winterfell march |
| food/starvation | ADWD | adwd-the-kings-prize-01:221 | "On the twenty-sixth day of the fifteen-day march, the last of the vegetables was consumed. On the thirty-second day, the last of the grain and fodder." |
| food/hospitality | ADWD | adwd-the-kings-prize-01:157 | Venison stew — "supped that night on a venison stew made from a scrawny hart that a scout called Benjicot Branch had brought down" — king's table vs. rationed men |
| food | ADWD | adwd-jon-04:23 | Castle Black stores inventory: granaries (oats, wheat, barley), root cellars (onions, garlic, carrots, parsnips, radishes, turnips), cheese, salt beef/pork/mutton/cod, hams, sausages, spices, dried peas, dried figs, olives, pickled cabbage/beets/onions/eggs/herring, potted hare, haunch of deer in honey — exhaustive food census just before Stannis's winter march begins |
| physical description | ACOK | acok-prologue:169 | Extended physical description of Stannis: "broad of shoulder and sinewy of limb, with a tightness to his face and flesh … Hard was the word men used … only a fringe of thin black hair … They lay like a blue-black shadow across his square jaw and the bony hollows of his cheeks. His eyes were open wounds beneath his heavy brows, a blue as dark as the sea by night. His mouth … thin pale lips and clenched muscles, a mouth that had forgotten how to smile and had never known how to laugh." |
| physical description | ACOK | acok-prologue:295 | Melisandre physical description: "long loose gown of flowing silk as bright as fire … around her throat was a red gold choker … a single great ruby … deep burnished copper … her eyes were red … pale as cream … She was not beautiful. She was red, and terrible, and red." |
| physical description | ASOS | asos-davos-04:75 | Stannis after Blackwater: "He seemed ten years older than the man that Davos had left at Storm's End … The king's close-cropped beard was spiderwebbed with grey hairs, and he had dropped two stone or more of weight … the bones moved beneath his skin like spears … His eyes were blue pits lost in deep hollows, and the shape of a skull could be seen beneath his face." |
| physical description | ADWD | adwd-the-kings-prize-01:135 | Stannis during Winterfell march: "his jaw was clenched so hard Asha feared his teeth might shatter" / "skull could be seen under his skin" |
| description/setting | ACOK | acok-davos-01:13 | Dragonstone burning scene: "They were all afire now, Maid and Mother, Warrior and Smith, the Crone with her pearl eyes and the Father with his gilded beard … pale flames licked at the grey sky … behind, the gargoyles and stone dragons on the castle walls seemed blurred, as if Davos were seeing them through a veil of tears. Or as if the beasts were trembling, stirring …" |
| description/setting | ACOK | acok-davos-02:279 | The sea cave approach: "Cloaked in that darkness … His little ship had a black hull, black sails, black oars" — Davos smuggling imagery recycled for the shadow-birth |
| quote — load-bearing | ACOK | acok-davos-01:263 | "The Seven have never brought me so much as a sparrow. It is time I tried another hawk, Davos. A red hawk." — Stannis explains the R'hllor conversion to Davos; definitive conversion statement |
| quote — load-bearing | ACOK | acok-davos-02:193 | "Renly brought his doom on himself with his treason, but I did love him, Davos. I know that now. I swear, I will go to my grave thinking of my brother's peach." — Stannis on Renly; core guilt/grief line |
| quote — load-bearing | ASOS | asos-davos-06:203 | "I know that a king protects his people, or he is no king at all." — Davos's moral argument; the line that pivots Stannis north |
| quote — load-bearing | ACOK | acok-catelyn-04:129-130 | "I saw a shadow. I thought it was Renly's shadow at the first, but it was his brother's." — Catelyn to Brienne; eyewitness account of the shadow |
| hospitality | ADWD | adwd-jon-04:313 | Jon advises Stannis on mountain clan hospitality: "Eat their bread and salt, drink their ale, listen to their pipers, praise the beauty of their daughters and the courage of their sons, and you'll have their swords." — hospitality-as-diplomacy |
| foreshadowing | ACOK | acok-prologue:79 | Patchface's song: "The shadows come to dance, my lord, dance my lord, dance my lord … The shadows come to stay, my lord" — sung before the shadow-assassinations; foreshadowing of the shadow-births |
| foreshadowing | ACOK | acok-davos-01:43 | Patchface at the burning: "Under the sea, smoke rises in bubbles, and flames burn green and blue and black" — present at the Lightbringer ceremony |
