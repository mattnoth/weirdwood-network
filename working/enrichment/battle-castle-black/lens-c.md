# Lens C — descriptive/quote/object depth — proposals
# Battle of Castle Black enrichment dip (S153)

---

## PROPOSED NODES (object.artifact only, STRICT)

### 1. `longclaw`
- **slug:** longclaw
- **type:** object.artifact
- **status:** LIKELY EXISTS — check `graph/nodes/artifacts/longclaw.node.md`. Wiki confirms node should exist (Longclaw page, ANCESTRAL_WEAPON_OF house-mormont). Verify before minting.
- **description:** Valyrian steel bastard sword, ancestral weapon of House Mormont, given to Jon Snow by Jeor Mormont. Pommel: pale stone wolf's head with garnet eyes (recarved from original bear's head after the fire in AGOT). Three fullers in the blade. Named for its owner: wolves have claws.
- **evidence_ref:** asos-jon-05.md:175 (Queenscrown escape); asos-jon-07.md (battle, trapdoor kill); asos-jon-08.md:19 (slung before second night battle); wiki:Longclaw.json
- **note:** WIELDED_IN `attack-on-the-wildlings` (acok) already exists in internal-edges.txt (line 47). Need WIELDED_IN for southern Thenn assault + northern gate battle (ASOS). See PROPOSED EDGES below.

### 2. `horn-of-winter`
- **slug:** horn-of-winter
- **type:** object.artifact
- **status:** CHECK — node may exist already. If not, this is a high-value artifact node.
- **description:** Eight feet along the curve, wide enough at the mouth to fit a man's arm to the elbow. Bands of old gold (more brown than yellow) graven with runes. Claimed by Mance Rayder to be Joramun's horn — the instrument said to wake giants from the earth and bring the Wall down.
- **evidence_ref:** asos-jon-10.md:161 (Jon's sighting in Mance's tent), asos-jon-10.md:187 (Mance describes its purpose); wiki:Horn_of_Winter.json
- **tier:** 1 (the physical object Jon sees) / 3 (Joramun provenance claim)
- **note:** This is narratively LOAD-BEARING and NAMED. Strongly recommend minting if not present. Relevant edges: HELD_BY mance-rayder (asos-jon-10), SOUGHT_BY mance-rayder (asos-jon-06:119 — Milkwater excavation), potential FORESHADOWS wall-breach-threat.

### Objects recommended as node-prose ONLY (not standalone artifact nodes)

- **Scarecrow sentinels** — straw stuffed into spare black cloaks, propped with crossbows and spears on towers and window sills. Maester Aemon's ruse. GENERIC defensive prop → NOT a named artifact node. Attach as descriptive prose to `attack-on-castle-black` node or `night-battle-atop-the-wall` node.
- **Two trebuchets** — Bowen Marsh restored two great trebuchets to working order before departing. One breaks during the battle (counterweight crashes free). UNNAMED/GENERIC → NOT artifact nodes. Node-prose on `attack-on-castle-black` hub.
- **Scorpions** — multiple; unnamed. "Scorpions, load with fire spears and loose at my command" (asos-jon-08). GENERIC → node-prose.
- **Catapults** — multiple smaller catapults. GENERIC → node-prose.
- **Oil/pitch barrels** — barrels of lamp oil and pitch rolled over the Wall edge. GENERIC → node-prose on `mammoth-attacks-gate-below` and `night-battle-atop-the-wall`.
- **Frozen gravel barrels** — Jon's improvised boulders: oak barrels filled with crushed rock and water, frozen solid overnight, rolled onto the turtle. INGENIOUS but UNNAMED/IMPROVISED → NOT artifact nodes. Node-prose on relevant sub-beat.
- **The Turtle** — Mance's siege engine: wooden frame on eight huge wheels, rounded roof covered in mammoth hide and sheepskins. Named only by type ("the turtle"), not a unique proper name → NOT an artifact node. Node-prose, possibly a brief sub-beat event node if synthesis judges it worth reifying.
- **Longbow (Jon's)** — Jon uses a "Dornish yew" longbow throughout the battle. Generic/unnamed → NOT a node. Node-prose.
- **Ygritte's arrows** — fletched with pale grey goose feathers. Generic arrows with notable descriptive detail → node-prose on ygritte node (## Description or ## Quotes), NOT a node. Jon examines the arrow that pierced his thigh: "Was the fletching grey, or white? Ygritte fletched her arrows with pale grey goose feathers" (asos-jon-05.md:223).

---

## PROPOSED EDGES (WIELDED_IN / OWNS / WIELDS / MADE_OF)

### E1 — Longclaw WIELDED_IN southern Thenn assault
- **source_slug:** longclaw
- **EDGE_TYPE:** WIELDED_IN
- **target_slug:** [new event node: southern-thenn-assault-castle-black] (to be minted by synthesis per baseline gap A.3)
- **tier=1**
- **evidence_ref:** asos-jon-07.md:143 (trapdoor fight); asos-jon-07.md:144 (boiling oil + trapdoor scene)
- **quote:** "Jon dropped his bow, reached back over his shoulder, ripped Longclaw from its sheath, and buried the blade in the middle of the first head to pop out of the tower. Bronze was no match for Valyrian steel."
- **status:** NEW (depends on synthesis minting the event hub first)
- **note:** This is the battle's single most explicit Longclaw-in-combat moment. Valyrian steel vs Thenn bronze is textually foregrounded.

### E2 — jon-snow WIELDS longclaw (in southern assault)
- **source_slug:** jon-snow
- **EDGE_TYPE:** WIELDS
- **target_slug:** longclaw
- **tier=1**
- **evidence_ref:** asos-jon-07.md:143
- **quote:** "Jon dropped his bow, reached back over his shoulder, ripped Longclaw from its sheath, and buried the blade in the middle of the first head to pop out of the tower."
- **status:** CHECK — a `jon-snow WIELDS longclaw` edge may already exist from ACOK (attack-on-the-wildlings). If so, this cite upgrades the ASOS evidence. If absent, NEW.

### E3 — Longclaw WIELDED_IN northern gate battle (night battle atop the Wall)
- **source_slug:** longclaw
- **EDGE_TYPE:** WIELDED_IN
- **target_slug:** night-battle-atop-the-wall
- **tier=1**
- **evidence_ref:** asos-jon-08.md:19
- **quote:** "he slung Longclaw over one shoulder, found his crutch, and hobbled down the steps"
- **status:** NEW (weaker cite — Longclaw is present but the primary weapons atop the Wall are bows; propose with tier=1 but note the sword is carried, not actively used, during the atop-Wall phase)

### E4 — Longclaw WIELDED_IN Jon's sortie to Mance (asos-jon-10)
- **source_slug:** longclaw
- **EDGE_TYPE:** WIELDED_IN
- **target_slug:** [jon-sorties-to-mance event — to be minted by synthesis per baseline gap A.6]
- **tier=1**
- **evidence_ref:** asos-jon-10.md:57 (rattles hilt before cage descent); asos-jon-10.md:235 (draws Longclaw in Mance's camp during Stannis's charge)
- **quote:** "rattled Longclaw's hilt to loosen the bastard blade in its scabbard" / "Jon reached back over his shoulder and drew Longclaw just as a thin line of rangers emerged from the fringes of the wood"
- **status:** NEW (depends on synthesis minting this event node)

### E5 — horn-of-winter HELD_BY mance-rayder
- **source_slug:** horn-of-winter
- **EDGE_TYPE:** HELD_BY
- **target_slug:** mance-rayder
- **tier=1**
- **evidence_ref:** asos-jon-10.md:161
- **quote:** "A warhorn, a bloody great warhorn. 'Yes,' Mance said. 'The Horn of Winter, that Joramun once blew to wake giants from the earth.'"
- **status:** CHECK — may exist; if not, NEW

### E6 — mance-rayder OWNS horn-of-winter
- **source_slug:** mance-rayder
- **EDGE_TYPE:** OWNS
- **target_slug:** horn-of-winter
- **tier=1**
- **evidence_ref:** asos-jon-10.md:161
- **quote:** same as E5
- **status:** CHECK / NEW (complement to E5; OWNS = broader possession)

---

## PROPOSED QUOTE ATTACHMENTS (verbatim quotes to attach to existing/new nodes)

### Q1 — Ygritte's final words (death scene)
- **target_node_slug:** ygritte (character node) + [new event.death node: death-of-ygritte]
- **quote:** "Oh. You know nothing, Jon Snow," she sighed, dying.
- **evidence_ref:** asos-jon-07.md:205
- **what it captures:** Ygritte's last words — iconic valediction. "Oh" prefix is textually load-bearing (softer than her living uses of the phrase). Verbatim including the "Oh" opener.
- **note:** Full surrounding context passage (Q2 below) should also be attached for the death scene. This single line is the valediction; Q2 is the death scene proper.

### Q2 — Ygritte death scene (full passage)
- **target_node_slug:** ygritte; [new event.death node: death-of-ygritte]; jon-snow
- **quote:** "He found Ygritte sprawled across a patch of old snow beneath the Lord Commander's Tower, with an arrow between her breasts. The ice crystals had settled over her face, and in the moonlight it looked as though she wore a glittering silver mask."
- **evidence_ref:** asos-jon-07.md:189–190
- **what it captures:** Physical description of Ygritte's death — the silver-mask image, the placement beneath the Lord Commander's Tower, the arrow fletched with white duck feathers (NOT Jon's grey goose fletching, but he felt it were). The most visually iconic single image of the battle's human cost.

### Q3 — Ygritte death scene continuation (dialogue with Jon)
- **target_node_slug:** ygritte; [new event.death node: death-of-ygritte]
- **quote:** "When he knelt in the snow beside her, her eyes opened. 'Jon Snow,' she said, very softly. It sounded as though the arrow had found a lung. 'Is this a proper castle now? Not just a tower?'"
- **evidence_ref:** asos-jon-07.md:193
- **what it captures:** Ygritte's dying recognition of Jon; her lung wound; her final reference to castles (echoes the whole Jon/Ygritte Queenscrown conversation about proper castles). Strong emotional beat and thematic callback.

### Q4 — Ygritte's cave line (thematic callback)
- **target_node_slug:** ygritte; [new event.death node: death-of-ygritte]
- **quote:** "She just smiled at that. 'D'you remember that cave? We should have stayed in that cave. I told you so.'"
- **evidence_ref:** asos-jon-07.md:201
- **what it captures:** Ygritte's final spoken line before the valediction — the cave as symbol of what they lost by returning to war. Pairs with Jon's parallel thought in asos-jon-10.md: "I should have stayed in that cave with Ygritte."

### Q5 — Jon burns Ygritte (burial beat)
- **target_node_slug:** [new event.death node: death-of-ygritte]; jon-snow
- **quote:** "He had burned Ygritte himself, as he knew she would have wanted"
- **evidence_ref:** asos-jon-08.md:13
- **what it captures:** Jon burns Ygritte north of the Wall per free folk custom. Short but narratively complete — establishes the burial and Jon's knowledge of wildling death practice. Grounds the mourning.

### Q6 — Mag the Mighty / tunnel death scene (mutual kill)
- **target_node_slug:** mag-mar-tun-doh-weg; donal-noye; [new event hub: death-of-donal-noye-and-mag]
- **quote:** "Noye's sword was sunk deep in the giant's throat, halfway to the hilt. The armorer had always seemed such a big man to Jon, but locked in the giant's massive arms he looked almost like a child. 'The giant crushed his spine. I don't know who died first.'"
- **evidence_ref:** asos-jon-08.md:171
- **what it captures:** The mutual kill in the tunnel — the visual of Noye's sword in Mag's throat + Mag's arms around Noye's body. Jon's "I don't know who died first." This is the scene that already generates the two-direction KILLS edges; this quote is the verbatim evidence behind both.

### Q7 — Mag the Mighty's physical description (gate attack)
- **target_node_slug:** mag-mar-tun-doh-weg
- **quote:** "The two crossbows had gotten off a dozen quarrels as the giant struggled toward them. Then the spearmen must have come to the fore, stabbing through the bars. Still the giant found the strength to reach through, twist the head off Spotted Pate, seize the iron gate, and wrench the bars apart. Links of broken chain lay strewn across the floor. One giant. All this was the work of one giant."
- **evidence_ref:** asos-jon-08.md:167
- **what it captures:** Mag's devastating physical power — twisting off a head, wrenching iron bars apart, absorbing a dozen crossbow quarrels and spear thrusts. The repeated "one giant" is the text's own astonishment. Essential node-prose for Mag.

### Q8 — Jon learns it is Mag the Mighty
- **target_node_slug:** mag-mar-tun-doh-weg; [new event hub: death-of-donal-noye-and-mag]
- **quote:** "'Mag.' I am the last of the giants. He could feel the sadness there, but he had no time for sadness."
- **evidence_ref:** asos-jon-08.md:171
- **what it captures:** Jon's naming of Mag + the elegiac "I am the last of the giants" thought. Establishes that Jon RESPECTS mag-mar-tun-doh-weg (already an edge in internal-edges.txt at line 87). This is the evidence quote that grounds that edge.

### Q9 — Tormund's tribute to Noye and Mag
- **target_node_slug:** donal-noye; mag-mar-tun-doh-weg; [new event hub: death-of-donal-noye-and-mag]; tormund-giantsbane
- **quote:** "'Mag himself went in that gate o' yours and never did come out.' 'He died on the sword of a brave man named Donal Noye.' 'Aye? Some great lord was he, this Donal Noye? One of your shiny knights in their steel smallclothes?' 'A blacksmith. He only had one arm.' 'A one-armed smith slew Mag the Mighty? Har! That must o' been a fight to see. Mance will make a song of it, see if he don't.'"
- **evidence_ref:** asos-jon-10.md:77–85
- **what it captures:** Tormund's oral tribute — Jon's elegy for Noye delivered as understatement ("a blacksmith, one arm"), Tormund's astonished "Har!" The promise of a song. Free folk perspective on the event. Also capture the shared toast: "To Donal Noye, and Mag the Mighty." Attach to both character nodes and the proposed event hub.

### Q10 — Donal Noye's description / armorer at work
- **target_node_slug:** donal-noye
- **quote:** "Warmth poured out the open door like the hot breath of summer. Within, one-armed Donal Noye was working his bellows at the fire. He looked up at the noise. 'Jon Snow?'"
- **evidence_ref:** asos-jon-06.md:25
- **what it captures:** First encounter at Castle Black — the warmth metaphor ("hot breath of summer"), Noye's working posture, one-armed physicality. The homecoming image.

### Q11 — Donal Noye's authority (voice as weapon)
- **target_node_slug:** donal-noye; attack-on-castle-black
- **quote:** "'No,' Donal Noye roared at three of the Mole's Town men, down below. 'The pitch goes to the hoist, the oil up the steps, crossbow bolts to the fourth, fifth, and sixth landings, spears to first and second. Stack the lard under the stair, yes, there, behind the planks. The casks of meat are for the barricade. Now, you poxy plow pushers, NOW!'"
- **evidence_ref:** asos-jon-07.md:57
- **what it captures:** Noye's command voice — the specific logistical order, the "poxy plow pushers" epithet. Jon's observation follows: "He has a lord's voice." This is Noye as de facto battle commander before the actual fighting.

### Q12 — Donal Noye's battle plan (defense of the gate)
- **target_node_slug:** donal-noye; attack-on-castle-black
- **quote:** "'The castle does them no good,' the armorer told his little garrison. 'Kitchens, common hall, stables, even the towers . . . let them take it all. We'll empty the armory and move what stores we can to the top of the Wall, and make our stand around the gate.'"
- **evidence_ref:** asos-jon-07.md:47
- **what it captures:** The core tactical decision that defines the battle. Noye abandons the buildings, concentrates on the gate. The crescent barricade of stores ("casks of nails and barrels of salt mutton, crates, bales of black broadcloth, stacked logs, sawn timbers, fire-hardened stakes, and sacks and sacks of grain") flows from this.

### Q13 — Donal Noye hands command to Jon (atop the Wall)
- **target_node_slug:** donal-noye; jon-snow; night-battle-atop-the-wall
- **quote:** "'Jon, you have the Wall till I return.' For a moment Jon thought he had misheard. It had sounded as if Noye were leaving him in command. 'My lord?' 'Lord? I'm a blacksmith. I said, the Wall is yours.'"
- **evidence_ref:** asos-jon-08.md:77–83
- **what it captures:** Noye's last command — the laconic "I'm a blacksmith" understatement, the transfer of authority. This is the moment Noye descends to die in the tunnel. Strong valediction for the character.

### Q14 — Maester Aemon confirms Jon must lead
- **target_node_slug:** aemon-targaryen-son-of-maekar-i; jon-snow; [new event: jon-takes-command-of-castle-black-defense]
- **quote:** "'Someone must—' 'You. You must lead.' 'No.' 'Yes, Jon. It need not be for long. Only until such time as the garrison returns. Donal chose you, and Qhorin Halfhand before him. Lord Commander Mormont made you his steward. You are a son of Winterfell, a nephew of Benjen Stark. It must be you or no one. The Wall is yours, Jon Snow.'"
- **evidence_ref:** asos-jon-08.md:185–192
- **what it captures:** Aemon's authority investing Jon as commander — "The Wall is yours, Jon Snow" echoes Noye's "The Wall is yours." The lineage of command is verbal: Noye → Aemon → Jon. This is the basis for `aemon-targaryen-son-of-maekar-i PROTECTS jon-snow` (already in internal-edges.txt) and grounds the command-transfer event.

### Q15 — Jon's speech atop the Wall (holding fear at bay)
- **target_node_slug:** attack-on-castle-black; jon-snow; night-battle-atop-the-wall
- **quote:** "'The Wall will stop them. The Wall defends itself.' Hollow words, but he needed to say them, almost as much as his brothers needed to hear them. 'Mance wants to unman us with his numbers. Does he think we're stupid?' He was shouting now, his leg forgotten, and every man was listening. 'The chariots, the horsemen, all those fools on foot . . . what are they going to do to us up here? Any of you ever see a mammoth climb a wall?'"
- **evidence_ref:** asos-jon-08.md:111
- **what it captures:** Jon's battle speech — "hollow words" self-awareness + the genuine defiance. The mammoth-climb-a-wall punchline. Attach to the battle hub and to jon-snow's character node.

### Q16 — Wildling army description at dawn (scale + composition)
- **target_node_slug:** attack-on-castle-black; mance-rayder
- **quote:** "Beneath the trees were all the wildlings in the world; raiders and giants, wargs and skinchangers, mountain men, salt sea sailors, ice river cannibals, cave dwellers with dyed faces, dog chariots from the Frozen Shore, Hornfoot men with their soles like boiled leather, all the queer wild folk Mance had gathered to break the Wall."
- **evidence_ref:** asos-jon-08.md:97
- **what it captures:** The full enumeration of Mance's assembled host as seen at dawn. The best single sentence describing the scale and diversity of the wildling army. Essential descriptive depth for the battle hub node.

### Q17 — Mammoth and giant charge (sensory texture)
- **target_node_slug:** mammoth-attacks-gate-below; night-battle-atop-the-wall
- **quote:** "Mammoths centered the wildling line, he saw, a hundred or more with giants on their backs clutching mauls and huge stone axes. More giants loped beside them, pushing along a tree trunk on great wooden wheels, its end sharpened to a point."
- **evidence_ref:** asos-jon-08.md:107
- **what it captures:** Visual of the second-day assault — mammoths with giants on their backs, the wooden ram. Key description for the mammoth-attacks-gate-below node and any giant/mammoth nodes.

### Q18 — Trebuchet scene / burning pitch (sensory texture)
- **target_node_slug:** night-battle-atop-the-wall; attack-on-castle-black
- **quote:** "Barrels of pitch were loaded hastily into the slings and set afire with a torch. The wind fanned the flames to a brisk red fury. 'NOW!' Noye bellowed. The counterweights plunged downward, the throwing arms rose to thud against the padded crossbars. The burning pitch went tumbling through the darkness, casting an eerie flickering light upon the ground below."
- **evidence_ref:** asos-jon-08.md:47
- **what it captures:** The trebuchet firing sequence — physical mechanics + the visual of burning pitch in the dark. The only detailed description of the Wall's heavy weapons in action.

### Q19 — Styr's appearance and death (southern assault)
- **target_node_slug:** styr; [new event: southern-thenn-assault-castle-black]
- **quote:** "It was then that he saw Styr. The Magnar was climbing up the barricade, over the gutted corn sacks and smashed barrels and the bodies of friends and foe alike. His bronze scale armor gleamed darkly in the firelight. Styr had taken off his helm to survey the scene of his triumph, and the bald earless whoreson was smiling. In his hand was a long weirwood spear with an ornate bronze head."
- **evidence_ref:** asos-jon-07.md:171
- **what it captures:** Styr's only physical description — bronze scale armor, bald, earless, weirwood spear with bronze head. Then his death follows from the burning of the steps beneath him. The spear is notable (weirwood + ornate bronze), but it's Styr's weapon not a named artifact — node-prose.

### Q20 — Styr's death (fire on the stairs)
- **target_node_slug:** styr; [new event: southern-thenn-assault-castle-black]
- **quote:** "Twenty-odd Thenns were still huddled together between the fires when the ice cracked from the heat, and the whole lower third of the stair broke off, along with several tons of ice. That was the last that Jon Snow saw of Styr, the Magnar of Thenn. The Wall defends itself, he thought."
- **evidence_ref:** asos-jon-07.md:181
- **what it captures:** Styr's death — not killed by Jon directly but by the burning stairs and ice. The "Wall defends itself" line is also the thematic climax of the southern assault. Styr's body is never confirmed separately; he's among the Thenns on the broken stair.

### Q21 — Horn of Winter physical description
- **target_node_slug:** horn-of-winter
- **quote:** "The horn was huge, eight feet along the curve and so wide at the mouth that he could have put his arm inside up to the elbow. If this came from an aurochs, it was the biggest that ever lived. At first he thought the bands around it were bronze, but when he moved closer he realized they were gold. Old gold, more brown than yellow, and graven with runes."
- **evidence_ref:** asos-jon-10.md:161
- **what it captures:** Complete physical description of the Horn of Winter. Essential node-prose if the artifact node is minted.

### Q22 — Mance on the Horn (strategic deterrent)
- **target_node_slug:** horn-of-winter; mance-rayder
- **quote:** "'If I sound the Horn of Winter, the Wall will fall. Or so the songs would have me believe. There are those among my people who want nothing more . . .' 'But once the Wall is fallen,' Dalla said, 'what will stop the Others?'"
- **evidence_ref:** asos-jon-10.md:187–189
- **what it captures:** The horn's claimed power and Mance/Dalla's restraint — the Others argument. Dalla's line is particularly important and often overlooked. Attach to horn-of-winter node and mance-rayder.

### Q23 — Donal Noye's description (physical)
- **target_node_slug:** donal-noye
- **quote:** "It was good to be back, good to see Noye with his big belly and pinned-up sleeve, his jaw bristling with black stubble."
- **evidence_ref:** asos-jon-06.md:27
- **what it captures:** Jon's affectionate physical description of Noye on return to Castle Black. Matches wiki description (big gut, barrel chest, black stubble, pinned sleeve). Book-level Tier-1 cite for the wiki prose.

### Q24 — Stannis on Noye and Robert's warhammer (posthumous tribute)
- **target_node_slug:** donal-noye
- **quote:** "'Noye made my first sword for me, and Robert's warhammer as well. Had the god seen fit to spare him, he would have made a better Lord Commander for your order than any of these fools who are squabbling over it now.'"
- **evidence_ref:** asos-jon-11.md:61
- **what it captures:** Stannis's tribute — Noye as maker of both Stannis's first sword and Robert's warhammer. Also a counterfactual Lord Commander assessment. This is from the scene directly after the battle, not during it, but it's primary book evidence for Noye's identity. (Note: robert's-warhammer is an artifact mentioned here — GENERIC / unnamed → node-prose only.)

### Q25 — Jon on Longclaw / Valyrian steel vs. bronze
- **target_node_slug:** longclaw; [new event: southern-thenn-assault-castle-black]
- **quote:** "Jon dropped his bow, reached back over his shoulder, ripped Longclaw from its sheath, and buried the blade in the middle of the first head to pop out of the tower. Bronze was no match for Valyrian steel. The blow sheared right through the Thenn's helm and deep into his skull, and he went crashing back down where he'd come from."
- **evidence_ref:** asos-jon-07.md:143
- **what it captures:** The material superiority of Valyrian steel foregrounded narratively. Also the clearest book cite for WIELDED_IN in the southern assault. This is the load-bearing quote for E1 above.

### Q26 — Scarecrow sentinels (descriptive / Aemon's ruse)
- **target_node_slug:** attack-on-castle-black; aemon-targaryen-son-of-maekar-i
- **quote:** "'The scarecrow sentinels,' Donal Noye called them. Only we're the crows, Jon mused, and most of us were scared enough."
- **evidence_ref:** asos-jon-07.md:33
- **what it captures:** Noye's name for the ruse + Jon's dark pun. The fuller sentence context: "Noye had placed them on every tower and in half the windows. Some were even clutching spears, or had crossbows cocked under their arms." Attach to attack-on-castle-black hub.

### Q27 — Night battle sound/sensory texture (Wall atop)
- **target_node_slug:** night-battle-atop-the-wall
- **quote:** "The wind was whipping at the black cloaks of the scarecrow sentinels who stood along the ramparts, spears in hand. [...] North of the Wall was a sea of darkness that seemed to stretch forever. Jon could make out the faint red glimmer of distant fires moving through the wood."
- **evidence_ref:** asos-jon-08.md:35–41
- **what it captures:** The sensory atmosphere of the night before the northern gate assault — cold, darkness, distant fires, mammoth sound. Sets up the trebuchet scene that follows.

### Q28 — Satin's fear / human texture
- **target_node_slug:** satin; attack-on-castle-black
- **quote:** "Satin pissed himself when the horns blew, but Jon pretended not to notice. 'Go shake Dick by the shoulder,' he told the Oldtown boy, 'else he's liable to sleep through the fight.' 'I'm frightened.' Satin's face was a ghastly white. 'So are they.'"
- **evidence_ref:** asos-jon-07.md:109–113
- **what it captures:** Satin's fear + Jon's response. Human texture of the battle's opening — the literal pissing himself, Jon's compassion in pretending not to notice. Attach to satin node.

### Q29 — Longclaw in Queenscrown escape (asos-jon-05)
- **target_node_slug:** longclaw; jon-snow
- **quote:** "Jon drew Longclaw from its sheath. Rain washed the steel, and the firelight traced a sullen orange line along the edge."
- **evidence_ref:** asos-jon-05.md:175
- **what it captures:** Visual description of Longclaw in the moment of decision (whether to kill the old man). "Rain washed the steel" + "sullen orange line" — the most evocative image of the blade. Not the battle proper, but the Queenscrown beat that precedes it.

---

## NOTES / UNCERTAINTIES

1. **Styr's death attribution:** The text says "That was the last that Jon Snow saw of Styr" — the stair collapse is visually confirmed, but Styr's body is not separately found. Jon never explicitly says "I saw Styr die." Tormund later confirms Styr is gone ("The Magnar swore he'd have the gate wide open... He brought down part, on his head" — asos-jon-10.md:89–91). Safe to treat as canonical death but the immediate cause is the burning staircase/ice collapse, not Jon's hand directly. A new event node should note this: `styr VICTIM_IN southern-thenn-assault-castle-black` with kill-mechanism = burning-stairs. Do NOT mint `jon-snow KILLS styr` — this is absent from internal-edges and NOT established by the text (Jon fires fire-arrows at the steps, not directly at Styr).

2. **Who shot Ygritte:** Jon explicitly says "The arrow was black... but it was fletched with white duck feathers. Not mine, not one of mine. But he felt as if it were." (asos-jon-07.md:191). The shooter is unknown — possibly a Night's Watch brother. The internal edge `SUSPECTED_OF` would apply here but without a target. No KILLS edge can be created from this. In asos-jon-10, Jon says "My brother" when Tormund asks — meaning a black brother of the Watch, unidentified. Do NOT assert a KILLS edge.

3. **Longclaw node check:** The internal-edges.txt includes `longclaw WIELDED_IN attack-on-the-wildlings` (line 47 = the ACOK WIELDED_IN edge). The wiki confirms Longclaw used in the ASOS battle. Check whether a `longclaw` node already exists in `graph/nodes/artifacts/` before minting.

4. **Horn of Winter node check:** Check `graph/nodes/artifacts/horn-of-winter.node.md` or similar. The horn is a major artifact with a dedicated wiki page. If a node exists, Q21, Q22, and edges E5/E6 are enrichment; if absent, mint the node.

5. **The Turtle as event vs. node-prose:** The turtle siege engine appears in asos-jon-09 as a distinct tactical beat. It is named ("the turtle") but generically, not as a unique proper name. It could be a sub-beat event (`turtle-assault-on-the-gate`) rather than an artifact node. If synthesis mints this sub-beat, the quote "It doesn't really look much like a turtle. Turtles don't have fur." (asos-jon-09.md:53–54) is good node-prose.

6. **Pyp's death:** Pyp does not die in asos-jon-07 or asos-jon-08 — he appears alive through asos-jon-09. He is alive at the end of this battle sequence. Do NOT create a Pyp death node from this dip (wiki says he dies in ADWD or later; out of scope here).

7. **Deaf Dick Follard's death:** The death of Deaf Dick Follard (`deaf-dick-follard-killed` node) is in the internal edge set with `deaf-dick-follard-killed SUB_BEAT_OF attack-on-castle-black`. The quote evidence: "Follard never made a sound, only toppled forward headlong over the parapet" (asos-jon-07.md:132). This is textually captured but not in the Lens C scope — it's already a node. The WITNESS_IN edge `jon-snow WITNESS_IN deaf-dick-follard-killed` might be worth adding.

8. **Grenn holding the gate:** The baseline (gap A.4) notes that "Grenn holds the inner gate" is a distinct beat from `mammoth-attacks-gate-below`. In asos-jon-09, Grenn is assigned command of the Wall. The tunnel-hold by "the boys" against the giant is *actually* Donal Noye's last stand in asos-jon-08 (Noye + 4 men in the tunnel). There is no separate Grenn-holds-the-inner-gate scene in the text as a *distinct* event — what happens is: (a) Noye + small party go down, (b) they all die vs. Mag. Grenn does push gravel barrels but is not in the tunnel fight. The "hold the gate" beat may be partially apocryphal from show adaptation. Flag for synthesis verification.

---

## HARVEST
(Format: chapter:line / kind / note — POINT only, harvest pass attaches)

**asos-jon-05:**
- 81 / food-grim / Jon has "no sense" of Ghost; feels alone even sleeping next to Ygritte — psychological isolation before battle
- 103-105 / character-sketch / Del dreams of stealing a girl "kissed by fire"; Jon learns raider names against his will (Grigg/Errok/Quort/Bodger/Hempen Dan/Henk the Helm/Toefinger/Big Boil)
- 109 / weather-omen / Storm coming from the west; wildling Lenn (woods witch's son) forecasts it — wildling weather lore note
- 119 / food-practice / Styr's standing order: any kneeler found must be killed "at once, to make certain they could not raise the alarm" — contrast with NW customs
- 170-175 / food-ritual / the hearth fire at the inn; broken branches generating "more smoke than heat"; the old man's horse; the apple squishing underfoot
- 223 / object-fletching / Ygritte's arrows "fletched with pale grey goose feathers" — a load-bearing detail (Jon wonders if her arrow hit him)

**asos-jon-06:**
- 19 / food / Mole's Town stable boys give Jon "a skin of wine as well, and half a loaf of brown bread" — last food before reaching Castle Black
- 51 / food / Jon riding feverish, almost misses Mole's Town — "Most of the village was hidden underground, only a handful of small hovels"
- 83 / medical / Maester Aemon's chain described: "gold and silver links glinting amongst iron, lead, tin, and other base metals" — physical detail for Aemon's node
- 95 / food-siege / Donal Noye reports surviving rangers back: Dywen, Giant, Dolorous Edd, Sweet Donnel Hill, Ulmer, Left Hand Lew, Garth Greyfeather — 12 of 200 who went with Mormont
- 99 / food / Clydas brings milk of the poppy: "a green flask and a rounded stone cup" — medical prop description
- 171 / medical / Aemon's wound treatment: "boiling wine" to drown wound + "poultice of nettle, mustard seed and moldy bread" — wildly specific medieval medicine

**asos-jon-07:**
- 11 / grim-register / "They woke to the smoke of Mole's Town burning" — opening line of the battle chapter; the smell of smoke as alarm
- 34-36 / physical / Scarecrow sentinels with crossbows cocked under their arms — Aemon's ruse; EVERY tower and half the windows
- 57-63 / logistics / Noye's full supply staging order: pitch to hoist, oil up the steps, crossbow bolts to 4th/5th/6th landings, spears to 1st/2nd, lard under the stair, salt mutton casks to barricade
- 73-77 / food / Owen brings buns ("still warm from the oven") + wheel of cheese + bag of onions, midday; Dick Follard finds a crock of butter, spreads it; raisins and pine nuts and dried apple in the buns — Jon takes two, tells Satin to eat ("There's no knowing when you'll have another chance")
- 95-96 / food / Owen arrives at sunset with "a loaf of black bread and a pail of Hobb's best mutton, cooked in a thick broth of ale and onions" — last meal before battle; "They ate every bit of it, using chunks of bread to wipe the bottom of the pail"
- 100-101 / food / Jon tells Satin to light the fire and fill the kettle with oil; then bars the tower door and visits the privy ("it might well be his last chance") — the mundane human detail
- 115 / fletching-detail / Jon's own arrows: "The shaft was black, the fletching grey" — Theon's "grey goose feather" quote recalled ("There's nothing half so mortal as a grey goose feather")
- 119 / visual / Wildling shields described: "skulls and bones, serpents, bear claws, twisted demonic faces" (raiders); Thenn shields = "black boiled leather with bronze rims and bosses, plain and unadorned"
- 126 / food-grim / Mole's Town women and children flee up the Wall; Jon sees "a mother pulling along two children"; two whores with crossbow skill given fighting posts
- 137 / battle-logistics / Thenns in attack: "bronze scale armor"; "bronze axes"; "short stabbing spears with leaf-shaped heads"; shields black boiled leather with bronze rims
- 181 / wall-physics / When the stairs burned, "the ice cracked from the heat, and the whole lower third of the stair broke off, along with several tons of ice" — the Wall defends itself

**asos-jon-08:**
- 11-13 / psychological / Jon's dream: stone kings of Winterfell ("You are no Stark, there is no place for you here"), falling in the crypts, calling for Ghost / Ygritte → wakes in his own cell, Ghost gone, Ygritte dead
- 23-25 / food / Before riding up: Clydas brings "cups of hot mulled wine, while Three-Finger Hobb passed out chunks of black bread. Jon took a heel from him and gnawed on it"
- 35-36 / logistics / Wall top supplies inventoried: "Bundles of quarrels, arrows, spears, and scorpion bolts stood ready on every hand. Rocks were piled ten feet high, big wooden barrels of pitch and lamp oil lined up beside them"
- 55-58 / gate-structure / The gate tunnel described: "smaller than any castle gate in the Seven Kingdoms, so narrow that rangers must lead their garrons through single file. Three iron grates closed the inner passage, each locked and chained and protected by a murder hole. The outer door was old oak, nine inches thick and studded with iron"
- 85-86 / food / Night battle: Hobb rides up the chain with "cups of onion broth"; Owen and Clydas serve the archers so they can "gulp them down between arrows" — the siege-ration hospitality
- 93-99 / Wall-physics / After first night battle, Jon describes the trebuchet: right-hand one breaks (counterweight crashes free, throws arm sideways, "splintering crash"); left-hand trebuchet kept throwing
- 159-162 / atmosphere / The tunnel approach: "The ice pressed close around them, and he could feel the cold seeping into his bones, the weight of the Wall above his head. It felt like walking down the gullet of an ice dragon."

**asos-jon-09:**
- 11-13 / siege / Day-and-night axes ringing; Mance has "sledgehammers at work as well, and long saws with teeth of bone and flint" — the sound of prolonged siege heard from the warming shed
- 21 / character-change / Grenn described: "grown half a foot, chest and shoulders thickened, not cut his hair nor trimmed his beard since the Fist of the First Men. It made him look as huge and shaggy as an aurochs"
- 29 / siege-object / The Turtle described in full: "a rounded top and eight huge wheels, and under the hides was a stout wooden frame... a hull turned upside down and opened fore and aft; a longhall on wheels" — Satin thought they were building a ship
- 44-46 / food / Tormund Giantsbane eating "the roast leg of a goat and bellowing orders" at his sons working on the turtle; Val milking a she-goat by Mance's tent — the wildling camp's normalcy
- 51 / food-grim / Jon registers their depleted stores: "Their oil was all but gone, and the last barrel of pitch had been rolled off the Wall two nights ago. They would soon run short of arrows as well, and there were no fletchers making more."
- 51-52 / food / Jon makes himself eat: "bread, bacon, onions, and cheese when he heard Horse shout..." — the last breakfast before the turtle assault
- 79-91 / siege-invention / Jon's frozen-gravel barrel tactic: crushes rock into oak barrels, pours water, freezes overnight; then tips and rolls them along the Wall surface (melts a thin film of ice to help them slide) — Grenn's key role pushing the barrels
- 99 / visual / After turtle is crushed: "the front of Mance's turtle was a crushed and splintered ruin, and wildlings were spilling out the other end and scrambling for their camp" — the payoff of the barrel tactic
- 119-123 / wildling-camp / Jon's walk through Mance's camp after his ice-cell release: "children squatting by the fires, old women in dog carts, cave dwellers with painted faces, raiders with claws and snakes and severed heads painted on their shields"

**asos-jon-10:**
- 57-58 / atmosphere / Jon walking north past the dead after release from ice cell: "There were other corpses too, strewn amidst broken barrels, hardened pitch, and patches of burnt grass, all shadowed by the Wall. Jon had no wish to linger here. He started walking toward the wildling camp, past the body of a dead giant whose head had been crushed by a stone. A raven was pulling out bits of brain from the giant's shattered skull. It looked up as he walked by. 'Snow,' it screamed at him."
- 87 / drink-ritual / Tormund's toast: the shared mead-skin "so potent that it made Jon's eyes water and sent tendrils of fire snaking through his chest" — Tormund's casual tribute to dead enemies
- 119-122 / wildling-camp / Descriptive sweep of Mance's camp: "cookfires and piss pits, children and goats wandering freely, sheep bleating among the trees, horse hides pegged up to dry. There was no plan to it, no order, no defenses." — contrast with the disciplined assault on Castle Black
- 161 / artifact / Horn of Winter first seen by Jon: full physical description (see Q21 above)
- 163-165 / foreshadowing / Mance admits he lied about the horn to Ygritte — "Did you think only crows could lie?" — undermines Jon's intelligence and complicates everything Ygritte told him
- 282-283 / visual / Stannis's banners as seen by Jon before recognizing them: "a seahorse, a field of birds, a ring of flowers. And yellow, so much yellow, yellow banners with a red device" — Jon doesn't know who they are until the name "Stannis" is cried
- 285 / visual / "a yellow one with long pointed tongues that showed a flaming heart, and another like a sheet of beaten gold, with a black stag prancing and rippling in the wind" — Stannis's royal standards at the charge

**asos-jon-11:**
- 33-35 / atmosphere / Melisandre's scent in the cage: "She even smells red. The scent reminded him of Mikken's forge, of the way iron smelled when red-hot; the scent was smoke and blood. Kissed by fire, he thought, remembering Ygritte." — the olfactory memory link between Melisandre and Ygritte
- 39 / tribute / Stannis on Noye: "Noye made my first sword for me, and Robert's warhammer as well" (see Q24 above) — also: Robert's warhammer as Noye's work, mentioned in passing; significant for the Robert's Rebellion arc
- 61-62 / tribute / Stannis to Jon: "Donal Noye held the gate. He died below in the tunnel, fighting the king of the giants." — Stannis knows the full story and attributes it correctly to Noye, not Jon
