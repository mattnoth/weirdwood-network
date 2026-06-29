# Lens B — Samwell Tarly enrichment proposals
# Davos/Sam residual enrichment dip
# Source chapters: asos-samwell-01..03, affc-samwell-01..05
# Written: 2026-06-29

---

## PROPOSED EDGES

Format: id | TYPE | source_slug | target_slug | book | chapter | VERBATIM QUOTE | tier | qualifier | verify | note

---

### SUB-THREAD 1: Fight at the Fist (ASOS Samwell I)

**E-01** | PARTICIPATES_IN | samwell-tarly | fight-at-the-fist | ASOS | asos-samwell-01 | "We had been fifty when we fled the Fist, maybe more, but some had wandered off in the snow" | tier-1 | role=survivor/witness | no | Sam was present throughout — fled with the survivors, his POV chapter is the primary account. Gap: no PARTICIPATES_IN edge wires him to the hub he narrates.

**E-02** | WITNESS_IN | samwell-tarly | fight-at-the-fist | ASOS | asos-samwell-01 | "He remembered the dead coming over the stones with arrows in their faces and through their throats" | tier-1 | | no | Sam directly saw the wights breach the ringwall; WITNESS_IN is justified (text SHOWS him seeing the charged moment). Distinct from PARTICIPATES_IN — both apply because he witnessed the breach and survived.

**E-03** | COMMANDS_IN | jeor-mormont | fight-at-the-fist | ASOS | asos-samwell-01 | "'Fire arrows,' the Lord Commander roared that night on the Fist, when he appeared suddenly astride his horse, 'give them flame.'" | tier-1 | | no | Mormont commanded the rearguard breakout. His COMMANDS_IN at the Fist is not yet explicitly wired in the fight-at-the-fist node (node only has wiki-sourced edges).

**E-04** | PARTICIPATES_IN | grenn | fight-at-the-fist | ASOS | asos-samwell-01 | "Small Paul had no answer for him. The big man gave a grunt and sank to his knees." | tier-2 | | no | Grenn is named as present during the retreat from the Fist; he carries Sam through the snow. He PARTICIPATES_IN the fight and its aftermath.

**E-05** | KILLS | thoren-smallwood | bear-wight | ASOS | asos-samwell-01 | "Thoren Smallwood charged, his longsword shining all orange and red from the light of the fire. His swing near took the bear's head off. And then the bear took his." | tier-1 | qualifier=mutual-kill | no | Thoren kills the bear-wight AND is killed by it in the same exchange. NOTE: bear-wight is a concept, not a named node; propose in NEW NODES if needed. This establishes the kill-exchange event at the Fist.

**E-06** | DIED_AT | thoren-smallwood | fist-of-the-first-men | ASOS | asos-samwell-01 | "Thoren Smallwood charged, his longsword shining all orange and red from the light of the fire. His swing near took the bear's head off. And then the bear took his." | tier-1 | | no | Thoren dies at the Fist. DIED_AT wires him to the location.

**E-07** | REVEALS_TO | samwell-tarly | jeor-mormont | ASOS | asos-samwell-02 | "The dragonglass dagger had melted the pale thing in the woods, true" / Mormont: "I've been thinking about this dragonglass of yours." | tier-1 | | no | Sam tells Mormont (and the Watch) that dragonglass killed the Other — a critical intelligence reveal. Distinct from the kill itself; this is the REVEALS_TO edge (sam → mormont, subject = dragonglass efficacy).

---

### SUB-THREAD 2a: Sam Kills the Other (ASOS Samwell I, in the woods post-Fist)

**E-08** | KILLS | samwell-tarly | the-other-at-the-fist | ASOS | asos-samwell-01 | "He heard a crack, like the sound ice makes when it breaks beneath a man's foot, and then a screech so shrill and sharp that he went staggering backward with his hands over his muffled ears, and fell hard on his arse." | tier-1 | | no | Sam stabs the Other with dragonglass. Distinct from samwell-tarly KILLS small-paul (which is already built). This is the **Other-kill** — the marquee gap identified in the brief.

**E-09** | KILLS | samwell-tarly | small-paul-wight | ASOS | asos-samwell-03 | "There was no time to think or pray or be afraid. Samwell Tarly threw himself forward and plunged the dagger down into Small Paul's back." + "Sam smashed it into Paul's mouth, so hard he felt teeth shatter… Then the dead man's face burst into flame, and the hands were gone." | tier-1 | | no | DEDUP CHECK: brief says "samwell-tarly KILLS small-paul (the wight — already exists)." This edge is confirmed BUILT. Noting verbatim quotes for the node's ## Quotes section in HARVEST. Do NOT re-propose.

**E-10** | WIELDED_IN | dragonglass | the-other-at-the-fist | ASOS | asos-samwell-01 | "the Other's armor was running down its legs in rivulets as pale blue blood hissed and steamed around the black dragonglass dagger in its throat" | tier-1 | | no | The dragonglass dagger (node: dragonglass) WIELDED_IN the Other-kill event. Pays off the cache find. High narrative value.

**E-11** | FORESHADOWS | dragonglass | the-other-at-the-fist | ASOS | asos-samwell-01 | "He did have two knives; the dragonglass dagger Jon had given him and the steel one he cut his meat with." | tier-2 | | no | The dragonglass dagger is planted in the flight-from-the-Fist scene before the kill scene; classic Chekhov's gun pay-off. FORESHADOWS is a narrative-craft edge, tier-2.

**E-12** | GIFTED_TO | jon-snow | samwell-tarly | ASOS | asos-samwell-01 | "the dragonglass dagger Jon had given him" | tier-1 | qualifier=object=dragonglass | no | Jon gave Sam the dragonglass dagger before the Fist. This wires jon-snow → samwell-tarly via GIFTED_TO with the dragonglass object. Precondition of E-08.

**E-13** | ENABLES | the-other-at-the-fist | fight-at-the-fist | ASOS | asos-samwell-01 | (causal chain: the Other ambushes the straggling survivors of fight-at-the-fist immediately after the rout) | tier-2 | direction=fight-at-the-fist ENABLES the-other-at-the-fist (rout causes the straggling survivors to be isolated) | yes | The fight and the subsequent Other-encounter are causally linked: the rout leaves Sam, Grenn, and Small Paul isolated, enabling the Other encounter. ENABLES direction: fight-at-the-fist → sam-kills-the-other.

**E-14** | PARALLELS | samwell-tarly | jon-snow | ASOS | asos-samwell-01 | "He had a dragonglass dagger too, but did he think to use it? Is he lying dead and frozen in some ravine" | tier-3 | | no | Sam's Other-kill with dragonglass mirrors/foreshadows Jon's later encounters with the dead. Narrative-craft edge. Low priority.

---

### SUB-THREAD 2b: Coldhands Rescues Sam and Gilly (ASOS Samwell III)

**E-15** | RESCUES | coldhands | samwell-tarly | ASOS | asos-samwell-03 | "'Brother!' The shout cut through the night, through the shrieks of a thousand ravens. Beneath the trees, a man muffled head to heels in mottled blacks and greys sat astride an elk." | tier-1 | | no | Coldhands physically rescues Sam and Gilly at Whitetree village, surrounded by wights. First and primary Coldhands → Sam edge. Distinct from bran-meets-coldhands (which is ADWD).

**E-16** | RESCUES | coldhands | gilly | ASOS | asos-samwell-03 | "'Here,' the rider said, reaching down with a gloved hand to pull Gilly up behind him." | tier-1 | | no | Gilly is explicitly pulled up first; both Sam and Gilly are rescued. Separate RESCUES edge for Gilly.

**E-17** | COMMANDS_IN | coldhands | coldhands-rescues-sam-and-gilly | ASOS | asos-samwell-03 | "The starlight itself seemed to stir, and all around them the trees groaned and creaked… Ravens! They were in the weirwood, hundreds of them, thousands… they descended on the wights in angry clouds." | tier-1 | | no | Coldhands commands the raven-swarm that drives off the wights. His control of the ravens is the mechanism of rescue. COMMANDS_IN on the event hub.

**E-18** | TRAVELS_WITH | coldhands | samwell-tarly | ASOS | asos-samwell-03 to asos-samwell-04 | "He takes the two under his protection and brings them to the Black Gate of the Nightfort" (ASOS IV recap) | tier-1 | | no | Coldhands escorts Sam and Gilly from Whitetree to the Nightfort/Black Gate. Confirmed in asos-samwell-04.

**E-19** | TRAVELS_WITH | coldhands | gilly | ASOS | asos-samwell-03 to asos-samwell-04 | (same ASOS IV recap reference) | tier-1 | | no | Gilly also travels with Coldhands. Separate edge for Gilly.

**E-20** | DECEIVES | samwell-tarly | jon-snow | ASOS | asos-samwell-04 | "Swear it, Samwell of the Night's Watch. Swear it for the life you owe me." / "Bran's not dead, Jon, he wanted to say… but he would have blurted it out anyway, if he had not given his word." | tier-1 | qualifier=concealment=Bran's survival | no | Sam keeps the secret of Bran's survival from Jon, which Jon explicitly grieves ("I don't even dream of Ghost anymore"). Sam DECEIVES Jon by omission, coerced by Coldhands's oath demand. Verify=no — text is unambiguous.

**E-21** | MANIPULATES | coldhands | samwell-tarly | ASOS | asos-samwell-04 | "We want no seekers coming after us. Swear it, Samwell of the Night's Watch. Swear it for the life you owe me." | tier-2 | qualifier=coercion-via-life-debt | yes | Coldhands extracts an oath from Sam under threat (life debt leverage). MANIPULATES is appropriate with qualifier. Verify because "manipulate" is interpretive — the text supports it as coercion.

**E-22** | CAUSES | coldhands-rescues-sam-and-gilly | bran-passes-the-black-gate | ASOS | asos-samwell-03/04 | (causal chain: Coldhands rescues Sam → guides them to the Nightfort → Sam opens the Black Gate for Bran's party) | tier-2 | | yes | The rescue causes Sam to reach the Nightfort, which enables Sam to open the Black Gate for Bran. Verify because it is a multi-step causal chain.

---

### SUB-THREAD 3: The Citadel Road (AFFC Samwell I–V)

#### The Journey Setup

**E-23** | TRAVELS_WITH | samwell-tarly | aemon-targaryen-son-of-maekar-i | AFFC | affc-samwell-01 | "Aemon as well… You're going with Gilly." / "Eastwatch. The Blackbird will deliver you to Braavos. From there you'll arrange your own passage to Oldtown." | tier-1 | | no | Jon orders Sam, Aemon, Gilly, and Dareon to travel together to Oldtown. The TRAVELS_WITH edge for the whole Citadel-road journey.

**E-24** | TRAVELS_WITH | samwell-tarly | gilly | AFFC | affc-samwell-01 | "You're going with Gilly." | tier-1 | | no | Sam explicitly assigned to travel with Gilly.

**E-25** | TRAVELS_WITH | samwell-tarly | dareon | AFFC | affc-samwell-01 | "Dareon will join you at Eastwatch." | tier-1 | | no | Dareon assigned to the voyage group.

**E-26** | MOTIVATES | death-of-maester-aemon | samwell-tarly | AFFC | affc-samwell-04/05 | "I will be your new maester" / "You must tell them, Sam… Tell the archmaesters." | tier-1 | qualifier=aemon's dying charge drives Sam to reach the Citadel | no | Aemon's death MOTIVATES Sam's mission to deliver warnings to the Citadel archmaesters. Causal.

**E-27** | TRAVELS_TO | samwell-tarly | braavos | AFFC | affc-samwell-02 | "The Blackbird will deliver you to Braavos." (affc-samwell-01); "the first ten days were calm enough, as Blackbird crept across the Bay of Seals" (affc-samwell-02) | tier-1 | | no | Sam's party reaches Braavos. First major port on the Citadel road.

**E-28** | TRAVELS_TO | samwell-tarly | oldtown | AFFC | affc-samwell-05 | "They reached Oldtown on a cold damp morning, when the fog was so thick that the beacon of the Hightower was the only part of the city to be seen." | tier-1 | | no | Sam reaches Oldtown — destination of the entire Citadel-road arc.

**E-29** | TRAVELS_TO | samwell-tarly | the-citadel | AFFC | affc-samwell-05 | "I came from the Wall with Maester Aemon, but he died during the voyage. If I could speak with the Seneschal…" / "They heard his boots stomping down the steps." | tier-1 | | no | Sam arrives at and enters the Citadel. Arc endpoint.

---

#### Death of Maester Aemon

**E-30** | WITNESS_IN | samwell-tarly | death-of-maester-aemon | AFFC | affc-samwell-04 | "She had a no septon aboard her to lead them in the prayers of passing, so the task fell to Samwell Tarly" | tier-1 | | no | Sam was present at and officiated Aemon's funeral. WITNESS_IN is appropriate — he was the only Night's Watch brother present.

**E-31** | OFFICIATES | samwell-tarly | death-of-maester-aemon | AFFC | affc-samwell-04 | "Sam donned his blacks to say the words… 'He was a great man. A maester of the Citadel, chained and sworn, and Sworn Brother of the Night's Watch, ever faithful… He was Aemon Targaryen. And now his watch is ended.'" | tier-1 | | no | Sam gives the eulogy. OFFICIATES is the right role edge (he performs the ceremony, not merely watches it).

**E-32** | MOURNS | samwell-tarly | aemon-targaryen-son-of-maekar-i | AFFC | affc-samwell-04 | "Sam hung his head and began to weep, his sobs so loud and wrenching that they made his whole body shake." | tier-1 | | no | Sam's grief is overt and load-bearing (shapes his entire Oldtown mission).

**E-33** | MOURNS | gilly | aemon-targaryen-son-of-maekar-i | AFFC | affc-samwell-04 | "Gilly came and stood beside him and let him cry upon her shoulder. There were tears in her eyes as well." | tier-1 | | no | Gilly also mourns Aemon.

**E-34** | AFFLICTED_BY | aemon-targaryen-son-of-maekar-i | fever-and-congestion | AFFC | affc-samwell-03 | "A chill had gotten inside Maester Aemon during the voyage and settled in his chest. By the time they got to Braavos, he had been so weak they'd had to carry him ashore." | tier-1 | qualifier=cause-of-death | no | Aemon's cause of death is a chill (respiratory illness) contracted on the sea voyage. For the `death-of-maester-aemon` event hub, Aemon AFFLICTED_BY (or DIED_OF) this illness. Target should be a `concept.medical` node; propose in NEW NODES.

**E-35** | DIED_AT | aemon-targaryen-son-of-maekar-i | cinnamon-wind-at-sea | AFFC | affc-samwell-04 | "The Cinnamon Wind was a swan ship out of Tall Trees Town on the Summer Isles… She had no septon aboard her to lead them in the prayers of passing" (implies he died at sea) + "somewhere off the sun-scorched southern coast of Dorne" | tier-1 | qualifier=at-sea-near-Dorne | no | Aemon dies at sea, between Tyrosh and Dorne, aboard the Cinnamon Wind. Not in Braavos proper. NOTE: a `DIED_AT braavos` edge would be wrong — he died after Braavos, near Dorne.

**E-36** | VICTIM_IN | aemon-targaryen-son-of-maekar-i | death-of-maester-aemon | AFFC | affc-samwell-04 | "He was Aemon Targaryen. And now his watch is ended." | tier-1 | | no | Aemon is VICTIM_IN his own death-event hub. Standard role edge.

**E-37** | REVEALS_TO | aemon-targaryen-son-of-maekar-i | samwell-tarly | AFFC | affc-samwell-04 | "'No one ever looked for a girl,' he said. 'It was a prince that was promised, not a princess… Daenerys is the one, born amidst salt and smoke.'" | tier-1 | qualifier=subject=Daenerys-as-TPTWP | no | Aemon's dying prophecy-revelation to Sam: Daenerys, not Rhaegar or Stannis, is the prince that was promised. Huge load-bearing edge — this is what Sam must carry to the Citadel.

**E-38** | REVEALS_TO | samwell-tarly | alleras-the-sphinx | AFFC | affc-samwell-05 | "and before he knew what was happening, all the rest came spilling out; the wights at the Fist of First Men, the Other on his dead horse, the murder of the Old Bear at Craster's Keep, Gilly and their flight, Whitetree and Small Paul, Coldhands and the ravens… Daenerys is the only hope" | tier-1 | qualifier=full-Wall-intelligence-dump | no | Sam dumps everything — Others, dragonglass, Coldhands, Aemon's dying words — to Alleras. First Watch intelligence to reach the Citadel in centuries.

**E-39** | ENABLES | death-of-maester-aemon | marwyn-sails-to-daenerys | AFFC | affc-samwell-05 | "Get myself to Slaver's Bay, in Aemon's place." | tier-2 | | yes | Aemon's death (and Sam's account of it) directly enables Archmaester Marwyn to decide to sail to Daenerys. Without Sam's arrival and report, Marwyn wouldn't have moved. Verify because it requires holding together multiple steps.

---

#### Dareon's Desertion

**E-40** | BETRAYS | dareon | nights-watch | AFFC | affc-samwell-03 | "'I'm done with you. I'm done with black.' Dareon tore his cloak off his naked bride and tossed it in Sam's face." | tier-1 | qualifier=deserts-vows | no | Dareon explicitly renounces his Night's Watch vows in front of Sam. BETRAYS nights-watch. DEDUP: killing-of-dareon node already has BETRAYS. This edge is the specific speech-act moment — verify whether it's already on the node; probably fine to propose separately as a book-pass1 dyad.

**E-41** | OPPOSES | samwell-tarly | dareon | AFFC | affc-samwell-03 | "Sam hit him. He did not think about it. His hand came up, curled into a fist, and crashed into the singer's mouth." | tier-1 | | no | Sam physically confronts Dareon over desertion. OPPOSES captures the active antagonism.

**E-42** | ATTACKS | samwell-tarly | dareon | AFFC | affc-samwell-03 | "He punched the singer in the face and in the belly, then began to pummel him about the shoulders with both hands." | tier-1 | qualifier=fistfight | no | Sam physically attacks Dareon. More specific than OPPOSES. Both apply; ATTACKS is the event-level edge.

**E-43** | RESCUES | xhondo | samwell-tarly | AFFC | affc-samwell-03 | "His rescuer leaned over him, huge and black and dripping. 'You owe Xhondo many feathers. The water ruined Xhondo's fine cloak.'" | tier-1 | | no | Xhondo (Summer Islander mate of the Cinnamon Wind) pulls Sam from the canal after the brawl. Introduce xhondo as a new node if not yet in graph.

---

#### Sam Reaches the Citadel

**E-44** | MEMBER_OF | samwell-tarly | the-citadel | AFFC | affc-samwell-05 | "'B-b-but,' Sam sputtered… 'Find Slayer a dry cell. He'll sleep here, and help you tend the ravens.'" | tier-2 | qualifier=novice/inducted | no | Sam is given quarters and duties at the Citadel — he has effectively joined the institution.

**E-45** | REVEALS_TO | samwell-tarly | archmaester-marwyn | AFFC | affc-samwell-05 | "Tell me all you told our Dornish sphinx. I know much of it and more, but some small parts may have escaped my notice." | tier-1 | qualifier=subject=wights+dragonglass+Aemon-prophecy | no | Sam delivers his full account again to Marwyn. The intelligence transfer that triggers Marwyn's departure.

**E-46** | LOVES | samwell-tarly | gilly | AFFC | affc-samwell-04 | "She pushed him back onto her pallet, hiked her skirts up around her thighs, and lowered herself onto him with a little whimpery sound… 'I am your wife now,' she whispered" | tier-1 | qualifier=consummated-at-sea | no | Sam and Gilly consummate their relationship. LOVES is the correct edge (LOVER_OF is already built per dedup list; verify exact edge type that's built — the brief says LOVER_OF exists, so this may be redundant unless the book-chapter evidence quote is missing from the existing dyad).

---

## NEW NODES NEEDED

### N-01: sam-kills-the-other
- slug: `sam-kills-the-other`
- type: `event.battle`
- containers: [north]
- Summary: Samwell Tarly kills an Other (White Walker) in the haunted forest south of the Fist of the First Men, using the obsidian dagger Jon Snow had given him. The Other ambushes Sam, Grenn, and Small Paul in a wildling village during the retreat from the Fist. Paul charges with an axe and is impaled on the Other's crystal sword; Sam, weeping and "falling more than running," stabs the dragonglass dagger blindly into the Other's throat. The armor dissolves "in rivulets as pale blue blood hissed and steamed." It is the first Other slain by a human in centuries and the pivotal pay-off of the dragonglass Chekhov's gun planted in ACOK (the cache Jon found beneath the Fist). Sam is mockingly nicknamed "Sam the Slayer" by his brothers.
- Key verbatim quote: `"the Other's armor was running down its legs in rivulets as pale blue blood hissed and steamed around the black dragonglass dagger in its throat"`
- Source: asos-samwell-01, lines 205–211
- Roster: samwell-tarly AGENT_IN, small-paul VICTIM_IN (Paul is killed by the Other immediately before this), grenn WITNESS_IN
- Proposed edges from this node: sam-kills-the-other CAUSES (or ENABLES) mormont-learns-of-dragonglass-efficacy; fight-at-the-fist ENABLES sam-kills-the-other

---

### N-02: coldhands-rescues-sam-and-gilly
- slug: `coldhands-rescues-sam-and-gilly`
- type: `event.incident`
- containers: [north]
- Summary: At the abandoned wildling village of Whitetree (south of the Fist), Samwell Tarly and Gilly (with her newborn son) are surrounded by a score of wights including former Night's Watch brothers. After Sam kills Small Paul's wight with fire, he emerges to find Gilly backed against the weirwood, surrounded. Coldhands, riding a great elk in mottled blacks and greys, commands a flock of ravens that swarms the wights and drives them off. Coldhands rescues both Sam and Gilly, helps them mount his elk, and begins guiding them south toward the Wall.
- Key verbatim quote: `"'Brother!' The shout cut through the night, through the shrieks of a thousand ravens. Beneath the trees, a man muffled head to heels in mottled blacks and greys sat astride an elk."`
- Source: asos-samwell-03, line 185
- Roster: coldhands AGENT_IN/COMMANDS_IN, samwell-tarly VICTIM_IN (saved), gilly VICTIM_IN (saved)
- Dedup note: DISTINCT from bran-meets-coldhands (adwd-bran-01). This is ASOS; Coldhands rescues Sam/Gilly before he ever meets Bran.

---

### N-03: death-of-maester-aemon
- slug: `death-of-maester-aemon`
- type: `event.death`
- containers: [] (UNTAGGED — death occurs at sea off the coast of Dorne, not in any of the 5 approved containers)
- Summary: Maester Aemon Targaryen (son of Maekar I, age 102) dies at sea aboard the Cinnamon Wind, somewhere off the southern coast of Dorne, from a chill contracted during the storm-wracked voyage from Braavos. His decline is traced across affc-samwell-02 (voyage) through affc-samwell-03 (bedridden in Braavos, "death is in his lungs") to affc-samwell-04 (funeral eulogy). Before dying he delivers his key revelation to Sam: Daenerys Targaryen, not Rhaegar or Stannis, is the prince(ss) that was promised. His body is preserved in a cask of blackbelly rum to be burned in Oldtown. Samwell Tarly officiates the funeral prayers. The "Egg, I dreamed I was old" moment (affc-samwell-02) is the marquee deathbed beat.
- Key verbatim quotes:
  - `"Egg?" he said, as the rain streamed down his cheeks. "Egg, I dreamed that I was old."` (affc-samwell-02, line 101)
  - `"He was Aemon Targaryen. And now his watch is ended."` (affc-samwell-04, line 13)
  - `"I shall not see Oldtown again. I know that now."` (affc-samwell-03, line 89)
- Source: affc-samwell-02 (deathbed scene); affc-samwell-03 (slow decline in Braavos); affc-samwell-04 (funeral)
- Roster: aemon-targaryen-son-of-maekar-i VICTIM_IN, samwell-tarly WITNESS_IN + OFFICIATES, gilly WITNESS_IN

---

### N-04: voyage-to-oldtown (optional — may be too thin for a hub)
**JUDGMENT CALL: skip hub; wire journey edges as direct dyads on characters.** The Citadel-road journey is best represented by TRAVELS_TO and TRAVELS_WITH dyads rather than a dedicated event node, as there is no single defining incident (unlike the Other-kill or Aemon's death). The death-of-maester-aemon node already anchors the marquee beat. Propose NO voyage-hub.

---

### N-05: sea-voyage-illness (concept.medical)
- slug: `aemon-sea-voyage-illness`
- type: `concept.medical`
- containers: []
- Summary: The respiratory illness (chill settling into the lungs) that Aemon Targaryen contracted during the storm-wracked voyage from Eastwatch to Braavos, which caused his death. Named in text as "death is in his lungs" (Braavosi healer, affc-samwell-03) and "a chill had gotten inside Maester Aemon during the voyage and settled in his chest." Target of the AFFLICTED_BY / DIED_OF edge from Aemon.
- Key verbatim quote: `"A chill had gotten inside Maester Aemon during the voyage and settled in his chest."`
- Source: affc-samwell-03, line 47

---

### N-06: xhondo (may already exist — check before minting)
- slug: `xhondo`
- type: `character.human`
- containers: []
- Summary: Summer Islander mate of the Cinnamon Wind who rescues Sam from drowning in a Braavosi canal after the brawl with Dareon, and who first reports the rumor of dragons in Qarth that re-animates Maester Aemon. His multilingual skills and connections make him a key facilitator.
- Key verbatim quote: `"Xhondo knows these dragons."` (affc-samwell-03)
- CHECK: `find /Users/mnoth/source/asoiaf-chat/graph/nodes -name "xhondo*"` before minting.

---

### N-07: alleras-the-sphinx (may already exist — check before minting)
- slug: `alleras-the-sphinx`
- type: `character.human`
- containers: []
- Summary: Half-Dornish Citadel acolyte, known as "the Sphinx," who intercepts Sam in the Seneschal's Court and brings him to Archmaester Marwyn. He speaks for Marwyn: "Ours was no chance encounter, Sam. The Mage sent me to snatch you up before you spoke to Theobald." A glass candle let Marwyn know Sam was coming.
- Key verbatim quote: `"Samwell. A new novice, come to see the Mage."` / `"I have a confession. Ours was no chance encounter, Sam."`
- CHECK before minting.

---

### N-08: archmaester-marwyn (may already exist — check before minting)
- slug: `archmaester-marwyn`
- type: `character.human`
- containers: []
- Summary: "The Mage" — archmaester at the Citadel who receives Sam's intelligence about wights, dragonglass, and Daenerys, then immediately sails for Slaver's Bay to reach Daenerys before the grey sheep's envoy. Possesses a functioning glass candle (Valyrian dragonglass scrying artifact). Implied enemy of the archmaesters who killed the dragons.
- Key verbatim quote: `"Who do you think killed all the dragons the last time around? Gallant dragonslayers armed with swords? The world the Citadel is building has no place in it for sorcery or prophecy or glass candles, much less for dragons."`
- CHECK before minting.

---

## HARVEST

<!-- kind | book | chapter:line | note/snippet -->

quote | ASOS | asos-samwell-01:17 | load-bearing dragonglass plant — "He did have two knives; the dragonglass dagger Jon had given him and the steel one he cut his meat with." → wire to dragonglass node ## Quotes; evidence for GIFTED_TO edge (jon-snow → samwell-tarly)

quote | ASOS | asos-samwell-01:165 | bear-wight description, Thoren's death — "Thoren Smallwood charged, his longsword shining all orange and red from the light of the fire. His swing near took the bear's head off. And then the bear took his." → attach to fight-at-the-fist node as a quote

quote | ASOS | asos-samwell-01:191 | Other description (iconic) — "The Other slid gracefully from the saddle to stand upon the snow. Sword-slim it was, and milky white. Its armor rippled and shifted as it moved, and its feet did not break the crust of the new-fallen snow." → attach to any existing `the-others` or `white-walkers` node

quote | ASOS | asos-samwell-01:207 | dragonglass kill mechanism — "the Other's armor was running down its legs in rivulets as pale blue blood hissed and steamed around the black dragonglass dagger in its throat" → dragonglass node ## Quotes; sam-kills-the-other node ## Quotes

quote | ASOS | asos-samwell-01:217 | "Sam the Slayer" named — "So craven you killed an Other." / "Grenn pointed with the knife." → samwell-tarly node ## Quotes

quote | ASOS | asos-samwell-02:153 | Mormont's Night's Watch purpose speech (dragonglass importance) — "The Night's Watch has forgotten its true purpose, Tarly. You don't build a wall seven hundred feet high to keep savages in skins from stealing women. The Wall was made to guard the realms of men… Too many years, Tarly, too many hundreds and thousands of years. We lost sight of the true enemy." → jeor-mormont node ## Quotes; load-bearing for fight-at-the-fist node context

quote | ASOS | asos-samwell-02:311 | Mormont dying — "'Tarly.' When he tried to speak, the blood dribbled from the Old Bear's mouth down into his beard. 'Tarly, go. Go.'" → mutiny-at-crasters-keep node ## Quotes; jeor-mormont node ## Quotes

quote | ASOS | asos-samwell-03:185 | Coldhands first appearance — "'Brother!' The shout cut through the night, through the shrieks of a thousand ravens. Beneath the trees, a man muffled head to heels in mottled blacks and greys sat astride an elk." → coldhands node ## Quotes

quote | ASOS | asos-samwell-03:187 | Coldhands cold hand — "Only when he grasped the offered hand did he realize that the rider wore no glove. His hand was black and cold, with fingers hard as stone." → coldhands node ## Quotes; appearance-class note

appearance | ASOS | asos-samwell-03:187 | Coldhands: "mottled blacks and greys," rides a great elk, black cold hands "hard as stone," hood shadowing face → coldhands node ## Appearances & Description

food | ASOS | asos-samwell-03:125 | Sam and Gilly eating the black sausages from Craster's wives in the abandoned wildling village — "Nothing was left but a few black sausages, as hard as wood. Sam sawed off a few thin slices for each of them." → food harvest note

food | AFFC | affc-samwell-02:47 | sea voyage food description — "They ate oaten porridge in the mornings, pease porridge in the afternoons, and salt beef, salt cod, and salt mutton at night" → food harvest note

quote | AFFC | affc-samwell-02:101 | Aemon's "Egg, I dreamed I was old" — `"Egg?" he said, as the rain streamed down his cheeks. "Egg, I dreamed that I was old."` → death-of-maester-aemon node ## Quotes; aemon-targaryen-son-of-maekar-i node ## Quotes — MARQUEE quote, must be attached to node before close

quote | AFFC | affc-samwell-03:89 | Aemon's "I shall not see Oldtown again" — "I shall not see Oldtown again. I know that now." → death-of-maester-aemon ## Quotes

quote | AFFC | affc-samwell-04:13 | Sam's eulogy for Aemon — "He was a great man. A maester of the Citadel, chained and sworn, and Sworn Brother of the Night's Watch, ever faithful." → death-of-maester-aemon ## Quotes; aemon-targaryen-son-of-maekar-i ## Quotes

quote | AFFC | affc-samwell-04:21 | Aemon's dying revelation re: Daenerys — "'No one ever looked for a girl,' he said. 'It was a prince that was promised, not a princess… Daenerys is the one, born amidst salt and smoke. The dragons prove it.'" → death-of-maester-aemon ## Quotes; attach to any prophecy-of-azor-ahai or tptwp node

foreshadowing | AFFC | affc-samwell-04:21 | Aemon's TPTWP correction re: translation error — "The language misled us all for a thousand years. Daenerys is the one" — this is a FORESHADOWS edge from this event to Daenerys's arc → harvest, don't propose now

quote | AFFC | affc-samwell-05:217 | Marwyn on Citadel killing dragons — "Who do you think killed all the dragons the last time around? Gallant dragonslayers armed with swords? The world the Citadel is building has no place in it for sorcery or prophecy or glass candles, much less for dragons." → archmaester-marwyn ## Quotes; attach to any citadel-conspiracy or glass-candle node

object | AFFC | affc-samwell-05:193 | glass candle in Marwyn's tower — "The candle itself was three feet tall and slender as a sword, ridged and twisted, glittering black… It burns but is not consumed." — glass candle is a significant artifact; if a node exists, add this cite → harvest pointer

relationship | AFFC | affc-samwell-04:45 | Gilly proposes naming Dalla's boy "Aemon Battleborn / Aemon Steelsong" — "Dalla brought him forth during battle, as the swords sang all around her. That should be his name." → gilly node / dalla's-son node relationship note

---

## DEDUP NOTES

1. **`samwell-tarly KILLS small-paul`** — brief confirms this is ALREADY BUILT. The quotes at asos-samwell-03 lines 159, 165–167 are verbatim evidence for that existing edge. Added to HARVEST so the minting step can attach them as evidence_quotes if missing from the built edge.

2. **`battle-of-the-fist-of-the-first-men`** — confirmed 0-edge wiki-shell DUPLICATE of `fight-at-the-fist`. All E-01 through E-07 edges use `fight-at-the-fist` as canonical target. The orchestrator will need to redirect the duplicate via same_as before any merge.

3. **`bran-meets-coldhands`** — that node covers ADWD. E-15 through E-22 target `coldhands-rescues-sam-and-gilly` (proposed new ASOS hub). The rescue scene is Sam's POV; Bran's later meeting is entirely distinct.

4. **`dareon BETRAYS nights-watch`** — the killing-of-dareon node already exists and mentions BETRAYS. E-40 proposes the specific *speech-act moment* in Sam's POV (affc-samwell-03). The orchestrator should check whether the existing dyad has a book-chapter evidence quote from Sam's POV; if not, E-40 fills that gap.

5. **`dareon DIES_AT braavos`** — already built per dedup list. E-40..E-42 do NOT re-propose this. These are Sam's direct-observation/interaction edges only.

6. **`samwell-tarly LOVER_OF gilly`** — brief says BUILT. E-46 proposes the consummation quote (affc-samwell-04:75) as evidence that may be missing from the built edge. Orchestrator should verify whether the existing LOVER_OF edge has a book-chapter evidence_quote.

7. **`aemon-targaryen-son-of-maekar-i TUTORS samwell-tarly`** — BUILT per brief. No re-proposal.

8. **`samwell-tarly SERVES aemon-targaryen-son-of-maekar-i`** — BUILT per brief. No re-proposal.
