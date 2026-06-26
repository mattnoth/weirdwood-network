# Lens A — Spine + Secondary-Character Sub-arcs
## Theon/Reek Enrichment Dip · S149

> **Lens scope:** causal-spine edges (CAUSES/TRIGGERS/ENABLES/MOTIVATES) + PARTICIPANT role edges
> (AGENT_IN / VICTIM_IN / WITNESS_IN / COMMANDS_IN / FIGHTS_IN / SUB_BEAT_OF) for the braided
> secondary cast. Source chapters: ACOK Theon I–VI + ADWD Reek I–III / Prince of Winterfell /
> Ghost in Winterfell / Theon.

---

## Proposed NODES

| slug | type | one-line gloss | book/chapter | why it's needed |
|------|------|----------------|--------------|-----------------|
| `theon-fakes-the-deaths-of-bran-and-rickon` | event.deception | Theon displays the tarred heads of two miller's sons as proof of Bran and Rickon's deaths; Reek (Ramsay) flays their faces | ACOK acok-theon-05 | Baseline GAP A — the ACT is unbuilt; `robb-receives-false-news-of-brans-death` and `bran-and-rickon-survive-the-sack-in-the-crypts` exist downstream but nothing models the deception itself; moral nadir of Theon's ACOK arc |
| `breaking-of-theon-at-the-dreadfort` | event.captivity | Ramsay imprisons and systematically tortures Theon at the Dreadfort, destroying his identity and renaming him "Reek" | ADWD adwd-reek-01 | Baseline GAP B — the identity-destruction at the core of the entire ADWD arc; no captivity/torture edges on ramsay→theon exist; first-use of TORTURES/IMPRISONS in this arc |
| `theon-and-jeyne-escape-winterfell` | event.escape | Theon (reclaiming his name) and Jeyne Poole leap from Winterfell's battlements; Holly and Frenya die covering the escape | ADWD adwd-theon-01 | Baseline GAP C — `theon-carries-jeyne-up-battlements-stairs` is dead-ended (0 out / 3 in); the leap + identity-reclaim are uncaptured; this node wires the escape forward to stannis-march-on-winterfell and pink-letter-delivered |
| `theon-reclaims-his-name` | event.identity | At the Battlements Gate threshold, Theon says "Theon Greyjoy" aloud to the guard instead of "Reek," marking the identity-reclaim | ADWD adwd-theon-01 | SUB_BEAT_OF the escape node; the weirwood prayer ("Let me die as Theon, not as Reek") in adwd-a-ghost-in-winterfell-01 is the narrative pivot; the reclaim phrase occurs one chapter later at the gate |
| `winterfell-murders-under-snow` | event.violence | During the snowbound siege, Abel's spearwives kill Yellow Dick, push Roger Ryswell's groom off the wall, kill Ser Aenys's squire, and kill Little Walder Frey, each framed as accident or unknown killer | ADWD adwd-a-ghost-in-winterfell-01 / adwd-theon-01 | Baseline GAP D confirmed load-bearing: the murders catalyze the Frey–Manderly brawl that clears the hall for the escape; `wedding-guests-observed-in-torchlight` is the wedding-night node but does not cover these post-wedding killings |

---

## Proposed EDGES

### ACOK spine — causal wiring

| source_slug | EDGE_TYPE | target_slug | tier | book | chapter-file | line | verbatim quote | note |
|-------------|-----------|-------------|------|------|--------------|------|----------------|------|
| `ironborn-invasion-of-the-north` | ENABLES | `capture-of-winterfell` | 1 | ACOK | acok-theon-03 | 163 | "I am a Greyjoy, and I mean to be my father's heir." | Theon's raid on Stony Shore is the feint that empties Winterfell; exists as event node; propose the causal link; DEDUP? (check if ENABLES already present) |
| `capture-of-winterfell` | ENABLES | `theon-fakes-the-deaths-of-bran-and-rickon` | 1 | ACOK | acok-theon-05 | 155 | "The miller's boys had been of an age with Bran and Rickon, alike in size and coloring, and once Reek had flayed the skin from their faces and dipped their heads in tar, it was easy to see familiar features in those misshapen lumps of rotting flesh." | Holding Winterfell creates the political need for the fake-deaths when the real boys escape |
| `theon-fakes-the-deaths-of-bran-and-rickon` | CAUSES | `robb-receives-false-news-of-brans-death` | 1 | ACOK | acok-theon-05 | 155 | "The miller's boys had been of an age with Bran and Rickon, alike in size and coloring, and once Reek had flayed the skin from their faces and dipped their heads in tar, it was easy to see familiar features in those misshapen lumps of rotting flesh." | Core causal link to the existing downstream node |
| `battle-outside-the-gates-of-winterfell` | ENABLES | `bolton-forces-attack` | 1 | ACOK | acok-theon-06 | 207–210 | "More men came up, hundreds of them, and at first they made to join the others. But now they've fallen on them! … These are northmen, I tell you. With a bloody man on their banner." | Rodrik's host assembles → Ramsay's Dreadfort men attack from within; DEDUP? |
| `bolton-forces-attack` | CAUSES | `sack-of-winterfell` | 1 | ACOK | acok-theon-06 | 261 | '"Burn it, burn it all," said the Bastard.' | The attack IS the sack; these are near-synonymous events — propose as direct chain or verify if already wired |
| `theon-fakes-the-deaths-of-bran-and-rickon` | MOTIVATES | `rodrik-cassel` | 2 | ACOK | acok-theon-06 | 97 | '"Would that I had thrust a sword through your belly instead of placing one in your hand."' | The apparent murder of Bran & Rickon hardens Rodrik's determination to retake Winterfell; secondary motivation chain |
| `sack-of-winterfell` | CAUSES | `breaking-of-theon-at-the-dreadfort` | 1 | ADWD | adwd-reek-01 | 77 | "It had been scourged from him, starved from him, flayed from him." | Theon captured at Winterfell → transferred to Dreadfort; the sack is the moment of capture |
| `breaking-of-theon-at-the-dreadfort` | ENABLES | `fall-of-moat-cailin` | 1 | ADWD | adwd-reek-02 | 25–26 | '"You will pretend to be a prince," Lord Ramsay told him last night … "but we know the truth. You're Reek."' | Ramsay uses the broken Theon (posing as Lord Balon's son) as the negotiator who talks the garrison into surrendering |
| `fall-of-moat-cailin` | ENABLES | `wedding-of-ramsay-bolton-and-arya-stark` | 1 | ADWD | adwd-reek-02 / adwd-reek-03 | 207 / 155 | "Three days later, the vanguard of Roose Bolton's host threaded its way through the ruins … Lord Roose glanced at Reek. 'Oh, and unchain your pet. I am taking him.'" | Clearing the Neck lets Roose's host march north and stage the wedding at Winterfell; Theon/Reek is transferred to Roose for the wedding role |
| `wedding-of-ramsay-bolton-and-arya-stark` | TRIGGERS | `winterfell-murders-under-snow` | 1 | ADWD | adwd-a-ghost-in-winterfell-01 | 101–103 | "This one could not be waved away as some drunken tumble or the kick of a horse. The dead man was one of Ramsay's favorites, the squat, scrofulous, ill-favored man-at-arms called Yellow Dick. Whether his dick had actually been yellow was hard to determine, as someone had sliced it off and stuffed it into his mouth …" | Wedding brings the northern lords + Abel's spearwives into Winterfell; murders begin immediately post-wedding |
| `winterfell-murders-under-snow` | ENABLES | `theon-and-jeyne-escape-winterfell` | 1 | ADWD | adwd-theon-01 | 75–76 | '"Rather than use our swords upon each other, you might try them on Lord Stannis … Ser Hosteen, assemble your knights and men-at-arms by the main gates … Lord Wyman, gather your White Harbor men by the east gate."' | The final Frey–Manderly brawl (triggered by Little Walder's murder) sends the garrison out to fight; the commotion and depleted guard coverage is what makes the escape possible |
| `theon-carries-jeyne-up-battlements-stairs` | SUB_BEAT_OF | `theon-and-jeyne-escape-winterfell` | 1 | ADWD | adwd-theon-01 | 278 | "Theon was staggering by the time he reached the foot of the stair. He slung the girl over his shoulder and began to climb." | Wires the dead-end node forward into the new escape hub |
| `theon-reclaims-his-name` | SUB_BEAT_OF | `theon-and-jeyne-escape-winterfell` | 1 | ADWD | adwd-theon-01 | 265 | '"Theon Greyjoy. I … I have brought some women for you."' | The reclaim beat happens at the Battlements Gate during the escape; it's a narrative climax embedded in the event |
| `theon-and-jeyne-escape-winterfell` | ENABLES | `pink-letter-delivered` | 1 | ADWD | adwd-theon-01 / (pink-letter chapter) | 289 | "Theon grabbed Jeyne about the waist and jumped." | Ramsay's letter demands return of "his Reek" and "his bride" — impossible without the escape having occurred first; the escape is the direct cause of the letter |

---

### ACOK identity tangle — Ramsay/Reek cross-identity

| source_slug | EDGE_TYPE | target_slug | tier | book | chapter-file | line | verbatim quote | note |
|-------------|-----------|-------------|------|------|--------------|------|----------------|------|
| `ramsay-snow` | IMPERSONATES | `reek` | 1 | ACOK | acok-theon-06 | 247 | '"The wretch is dead." He stepped closer. "The girl's fault. If she had not run so far, his horse would not have lamed, and we might have been able to flee. I gave him mine when I saw the riders from the ridge … Ride for the Dreadfort, I told him, bring all the help you can … By the time they put that arrow through his back, I'd smeared myself with the girl's filth and dressed in his rags."' | ACOK Ramsay-as-Reek: Ramsay reveals how he swapped clothes with the dead original Reek, pretended to be "Reek," was captured, and manipulated Theon. First-use IMPERSONATES in graph. Baseline GAP confirmed. |
| `ramsay-snow` | DECEIVES | `theon-greyjoy` | 1 | ACOK | acok-theon-06 | 109 | "Reek," he said. "Snow, my wife called me before she ate her fingers, but I say Bolton." | ALREADY EXISTS per baseline (acok-theon-06:109 noted as existing). DEDUP — do not re-propose. |

---

### ACOK secondary cast — role edges

| source_slug | EDGE_TYPE | target_slug | tier | book | chapter-file | line | verbatim quote | note |
|-------------|-----------|-------------|------|------|--------------|------|----------------|------|
| `dagmer` | AGENT_IN | `harrying-of-the-stony-shore` | 1 | ACOK | acok-theon-03 | 65 | "Dagmer Cleftjaw stood by the high carved prow of his longship, Foamdrinker. Theon had assigned him the task of guarding the ships." | Dagmer commands the ships during Stony Shore; DEDUP? (check if agent already present) |
| `dagmer` | COMMANDS_IN | `capture-of-torrhens-square` | 1 | ACOK | acok-theon-05 | 81 | '"The old castellan broke his shield wall, yes … Dagmer lives, be grateful for that much. He's leading the survivors back toward the Stony Shore."' | Dagmer leads the Torrhen's Square siege feint; DEDUP? |
| `black-lorren` | AGENT_IN | `capture-of-winterfell` | 1 | ACOK | acok-theon-04 | 46–48 | '"The Hunter's Gate," Lorren said. "Best come see." … Black Lorren had his sword out, but there were already four of them pressing in on him.' | Black Lorren is Theon's enforcer inside Winterfell throughout the occupation; role at capture + sack |
| `black-lorren` | VICTIM_IN | `sack-of-winterfell` | 1 | ACOK | acok-theon-06 | 261 | "Black Lorren had his sword out, but there were already four of them pressing in on him." | Lorren fights during the sack; existing baseline notes him as VICTIM_IN; DEDUP? |
| `wex-pyke` | WITNESS_IN | `capture-of-winterfell` | 1 | ACOK | acok-theon-04 | 29 | '"Make certain Bran Stark and his little brother are in their beds, and be quick about it." … Wex returned the quickest, shaking his head side to side.' | Wex is Theon's squire throughout the Winterfell occupation; WITNESS across multiple events |
| `wex-pyke` | PARTICIPATES_IN | `trail-followed-north-northwest` | 1 | ACOK | acok-theon-04 | 170 | "Wex clapped his hands together loudly … The mute boy pointed … 'A man the size of Hodor ought to have left a deep print in this mud.'" | Wex's sign-language deduction that Osha split from the direwolves is the key finding in the hunt |
| `farlen` | AGENT_IN | `trail-followed-north-northwest` | 1 | ACOK | acok-theon-04 | 110–112 | '"Farlen, I'll want hounds, and you to handle them."' | Farlen leads the hounds during the hunt for Bran and Rickon |
| `farlen` | VICTIM_IN | `theon-fakes-the-deaths-of-bran-and-rickon` | 1 | ACOK | acok-theon-05 | 32–33 | '"As he knelt to the block, the kennelmaster said, 'M'lord Eddard always did his own killings.' Theon had to take the axe himself … It took three more cuts to hack through all that bone and muscle and sever the head from the body."' | Farlen executed by Theon after the fake-deaths cover-up; Theon suspects him of the ironborn murders at Winterfell |
| `luwin` | WITNESS_IN | `theon-fakes-the-deaths-of-bran-and-rickon` | 1 | ACOK | acok-theon-05 | 61 | "Only Maester Luwin had the stomach to come near. Stone-faced, the small grey man had begged leave to sew the boys' heads back onto their shoulders, so they might be laid in the crypts below with the other Stark dead." | Luwin witnesses the display of the tarred heads; his reaction is the moral counterpoint |
| `luwin` | VICTIM_IN | `sack-of-winterfell` | 1 | ACOK | acok-theon-06 | 261 | "Maester Luwin was trying to reach him when a knight on a warhorse planted a spear between his shoulders, then swung back to ride over him." | Luwin is speared during the sack; baseline notes him as VICTIM_IN; DEDUP? |
| `osha` | AGENT_IN | `trail-followed-north-northwest` | 1 | ACOK | acok-theon-04 | 90–93 | '"Six." Reek stepped up behind him … "Both Starks, that bog boy and his sister, the halfwit from the stables, and your wildling woman." … Osha. He had suspected her from the moment he saw that second cup.' | Osha engineers the escape from Winterfell; she is the primary agent in the flight |
| `osha` | AGENT_IN | `bran-and-rickon-survive-the-sack-in-the-crypts` | 1 | ACOK | acok-theon-04 | 93 | 'Osha. He had suspected her from the moment he saw that second cup. I should have known better than to trust that one.' | The wildling's betrayal of Theon's trust is what saves Bran and Rickon |
| `bran-stark` | VICTIM_IN | `theon-fakes-the-deaths-of-bran-and-rickon` | 2 | ACOK | acok-theon-05 | 155 | "The miller's boys had been of an age with Bran and Rickon, alike in size and coloring, and once Reek had flayed the skin from their faces and dipped their heads in tar …" | Theon reports the false deaths specifically to prevent search parties and consolidate his rule; Bran is the named target of the deception |
| `rickon-stark` | VICTIM_IN | `theon-fakes-the-deaths-of-bran-and-rickon` | 2 | ACOK | acok-theon-05 | 155 | "The miller's boys had been of an age with Bran and Rickon, alike in size and coloring …" | Same as Bran above; Rickon named jointly as the supposed victim |
| `rodrik-cassel` | COMMANDS_IN | `battle-outside-the-gates-of-winterfell` | 1 | ACOK | acok-theon-06 | 119 | '"I have near two thousand men with me," Ser Rodrik said … "You have until evenfall to disperse."' | Rodrik commands the relief host before Ramsay's betrayal |
| `rodrik-cassel` | VICTIM_IN | `bolton-forces-attack` | 1 | ACOK | acok-theon-06 | 229 | '"The old castellan," said Black Lorren. "With Leobald Tallhart and Cley Cerwyn." … "The old castellan broke his shield wall, yes … When the old fool gave me his hand, I took half his arm instead."' | Ramsay kills Rodrik during the betrayal; described explicitly |
| `aeron-greyjoy` | PARTICIPATES_IN | `harrying-of-the-stony-shore` | 1 | ACOK | acok-theon-02 | 399 | '"You are to harry the Stony Shore, raiding the fishing villages and sinking any ships you chance to meet … Aeron will accompany you, and Dagmer Cleftjaw."' | Aeron assigned to the Stony Shore; DEDUP? |
| `reek` | AGENT_IN | `theon-fakes-the-deaths-of-bran-and-rickon` | 1 | ACOK | acok-theon-05 | 155 | "once Reek had flayed the skin from their faces and dipped their heads in tar" | The original Reek (the servant) physically performs the face-flaying and tarring that makes the deception work |
| `reek` | AGENT_IN | `capture-of-winterfell` | 2 | ACOK | acok-theon-04 | 91 | '"Six." Reek stepped up behind him, smelling of soap, his long hair moving in the wind. "Both Starks, that bog boy and his sister, the halfwit from the stables, and your wildling woman."' | Reek (the servant) serves as Theon's informant and fixer during the Winterfell occupation |

---

### ADWD secondary cast — role edges

| source_slug | EDGE_TYPE | target_slug | tier | book | chapter-file | line | verbatim quote | note |
|-------------|-----------|-------------|------|------|--------------|------|----------------|------|
| `ramsay-snow` | TORTURES | `theon-greyjoy` | 1 | ADWD | adwd-reek-01 | 115 | "It was the sort of pain that drove men mad, and it could not be endured for long. Soon or late the victim would scream, 'Please, no more, no more, stop it hurting, cut it off,' and Lord Ramsay would oblige. It was a game they played." | Core captivity edge — first-use TORTURES on ramsay→theon; describes systematic flaying/mutilation |
| `ramsay-snow` | IMPRISONS | `theon-greyjoy` | 1 | ADWD | adwd-reek-01 | 15 | "It had been two days since he had eaten, or maybe three. Down here in the dark it was hard to tell." | Theon held in Dreadfort dungeons; complements TORTURES |
| `theon-greyjoy` | IMPRISONED_AT | `dreadfort` | 1 | ADWD | adwd-reek-01 | 13 | "He listened in terror, stiff as stone, to the scuff of boots and the clanking of iron keys." | Theon's location during the captivity arc |
| `theon-greyjoy` | PRISONER_OF | `ramsay-snow` | 1 | ADWD | adwd-reek-01 | 77 | "It had been scourged from him, starved from him, flayed from him." | Status edge; pairs with IMPRISONS |
| `ramsay-snow` | KILLS | `kyra` | 1 | ADWD | adwd-reek-01 | 67 | '"You must be punished," he said … [Kyra] seized a stone and threw it at his head. It missed by a good foot, and Ramsay smiled.' — then: 'If she had not run so far, his horse would not have lamed …' | Kyra killed after being hunted; POV-confirmed; baseline notes kyra as ramsay KILLS target |
| `theon-greyjoy` | PARTICIPATES_IN | `breaking-of-theon-at-the-dreadfort` | 1 | ADWD | adwd-reek-01 | 53 | '"My name is Reek. It rhymes with leek." He had not been born with that name. In another life he had been someone else …' | Theon's identity dissolution is the core of this event |
| `ramsay-snow` | AGENT_IN | `breaking-of-theon-at-the-dreadfort` | 1 | ADWD | adwd-reek-01 | 105 | '"Oh, he's been skinned, here and there," said Ramsay.' | Ramsay explicitly named as the actor who performed the torture |
| `skinner` | PARTICIPATES_IN | `breaking-of-theon-at-the-dreadfort` | 1 | ADWD | adwd-reek-01 / adwd-reek-02 | 31 | '"Betray me if you want, it makes no matter … but count your fingers first and know the cost … Seven fingers. A man can make do with seven fingers … [Ramsay] commanded Skinner to lay his ring finger bare."' | Skinner performs the actual flayings under Ramsay's direction |
| `damon-dance-for-me` | PARTICIPATES_IN | `breaking-of-theon-at-the-dreadfort` | 1 | ADWD | adwd-reek-01 | 87 | "Damon, called Damon Dance-for-Me, fair-haired and boyish." (among the Bastard's Boys who enforce) | Damon is the whip-wielding enforcer; later adwd-reek-02 shows him giving Reek the horse and making threats |
| `yellow-dick` | PARTICIPATES_IN | `breaking-of-theon-at-the-dreadfort` | 1 | ADWD | adwd-reek-01 | 87 | "Damon, called Damon Dance-for-Me, fair-haired and boyish. Grunt … Sour Alyn. Skinner. Yellow Dick." | Part of Bastard's Boys who oversee Theon at the Dreadfort |
| `sour-alyn` | PARTICIPATES_IN | `breaking-of-theon-at-the-dreadfort` | 1 | ADWD | adwd-reek-01 | 87 | "Grunt, who had lost his tongue for speaking carelessly in Lord Roose's hearing. Sour Alyn." | Same Bastard's Boys group |
| `ben-bones` | PARTICIPATES_IN | `breaking-of-theon-at-the-dreadfort` | 1 | ADWD | adwd-reek-01 | 87 | "Ben Bones, the old man who kept his lordship's beloved hunting hounds." | Ben Bones holds the collar for Reek after Moat Cailin; participant in the Dreadfort regime |
| `theon-greyjoy` | AGENT_IN | `fall-of-moat-cailin` | 1 | ADWD | adwd-reek-02 | 163 | '"Reek. My lord, Moat Cailin is yours. Here are its last defenders."' | Theon/Reek talking the ironborn garrison into surrender — his only active role in the Bolton war effort |
| `ramsay-snow` | COMMANDS_IN | `bolton-banner-raised-prisoners-killed` | 1 | ADWD | adwd-reek-02 | 207 | "Along the rotting-plank road, wooden stakes were driven deep into the boggy ground; there the corpses festered, red and dripping. Sixty-three, he knew, there are sixty-three of them." | Ramsay flays the surrendered garrison after the safe-conduct; adwd-reek-02 confirms; DEDUP? |
| `theon-greyjoy` | AGENT_IN | `wedding-of-ramsay-bolton-and-arya-stark` | 1 | ADWD | adwd-the-prince-of-winterfell-01 | 67–71 | '"Arya of House Stark comes here to be wed. A woman grown and flowered, trueborn and noble, she comes to beg the blessings of the gods. Who comes to claim her?" … "Theon of House Greyjoy, who was her father's ward."' | Theon gives away the false Arya; existing but worth verifying if AGENT_IN already wired; DEDUP? |
| `jeyne-poole` | VICTIM_IN | `wedding-of-ramsay-bolton-and-arya-stark` | 1 | ADWD | adwd-the-prince-of-winterfell-01 | 15–16 | '"I will be a good wife to him, and t-true … I will be a better wife than the real Arya could have been, he'll see."' | Jeyne is compelled into the false-Arya marriage; DEDUP? |
| `jeyne-poole` | VICTIM_IN | `breaking-of-theon-at-the-dreadfort` | 2 | ADWD | adwd-reek-01 / adwd-the-prince-of-winterfell-01 | 235 | '"That is not Lord Eddard's daughter … That's Sansa's little friend, the steward's girl. Jeyne, that was her name. Jeyne Poole."' | Jeyne was apparently already in Bolton custody / being groomed; the Dreadfort context envelops her; Tier-2 as exact captivity-start point unclear from these chapters |
| `harwood-stout` | WITNESS_IN | `wedding-of-ramsay-bolton-and-arya-stark` | 1 | ADWD | adwd-reek-03 / adwd-the-prince-of-winterfell-01 | 59 | "Their host, a grizzled one-armed petty lord by the name of Harwood Stout, knew better than to refuse him …" / wedding scene shows lords present | Stout hosts Ramsay at Barrowton; present at the wedding feast |
| `hother-umber` | WITNESS_IN | `wedding-of-ramsay-bolton-and-arya-stark` | 1 | ADWD | adwd-the-prince-of-winterfell-01 | 175 | "Hother Umber, the gaunt old man called Whoresbane, went grim-faced and scowling." | Whoresbane present at wedding feast; leaves for the war-council |
| `wyman-manderly` | WITNESS_IN | `wedding-of-ramsay-bolton-and-arya-stark` | 1 | ADWD | adwd-the-prince-of-winterfell-01 | 129 | "Lord Manderly devoured six portions, two from each of the three pies, smacking his lips and slapping his belly …" | Manderly at the wedding feast, serving the suspect pies |
| `hosteen-frey` | WITNESS_IN | `wedding-of-ramsay-bolton-and-arya-stark` | 1 | ADWD | adwd-the-prince-of-winterfell-01 | 129 | "Ramsay hacked off slices with his falchion and Wyman Manderly himself served, presenting the first steaming portions to Roose Bolton and his fat Frey wife, the next to Ser Hosteen and Ser Aenys, the sons of Walder Frey." | Hosteen present and served first at the wedding |
| `aenys-frey` | WITNESS_IN | `wedding-of-ramsay-bolton-and-arya-stark` | 1 | ADWD | adwd-the-prince-of-winterfell-01 | 129 | "… the next to Ser Hosteen and Ser Aenys, the sons of Walder Frey." | Same as Hosteen |

---

### ADWD spearwives — role edges in the escape

| source_slug | EDGE_TYPE | target_slug | tier | book | chapter-file | line | verbatim quote | note |
|-------------|-----------|-------------|------|------|--------------|------|----------------|------|
| `mance-rayder` | COMMANDS_IN | `theon-and-jeyne-escape-winterfell` | 1 | ADWD | adwd-a-ghost-in-winterfell-01 | 267 | '"You prayed, and the gods sent us. You want to die as Theon? We'll give you that."' (Rowan, Abel's woman; Abel = mance-rayder) | Abel / Mance commands the spearwives; DEDUP? (Abel=mance already in graph) |
| `rowan` | AGENT_IN | `winterfell-murders-under-snow` | 1 | ADWD | adwd-a-ghost-in-winterfell-01 | 114 | '"You killed the others, why not him? Yellow Dick—" "—stank as bad as you. A pig of a man."' | Rowan confesses Yellow Dick; Holly also implicated; Rowan's admission is Theon's POV-confirmed |
| `rowan` | AGENT_IN | `theon-and-jeyne-escape-winterfell` | 1 | ADWD | adwd-theon-01 | 89 | '"The bath. It must be now." … Rowan grasped Theon's arm.' | Rowan coordinates the bath-trick deception and escape plan |
| `holly` | AGENT_IN | `theon-and-jeyne-escape-winterfell` | 1 | ADWD | adwd-theon-01 | 267 | '"Theon Greyjoy. I … I have brought some women for you." … Holly slipped past the guard's spearpoint and reached up to his face … her blade slid through the meat of his neck, just below the ear.' | Holly kills the gate guard; then dies from crossbow bolts on the battlements |
| `holly` | VICTIM_IN | `theon-and-jeyne-escape-winterfell` | 1 | ADWD | adwd-theon-01 | 283 | '"Oh, fuck me bloody. The rope." She gave a hysterical laugh. "Frenya has the rope." Then she grunted and grabbed her stomach. A quarrel had sprouted from her gut … a second shaft appeared between her breasts. Holly grabbed for the nearest merlon and fell.' | Holly killed by crossbowmen on the inner wall |
| `frenya` | AGENT_IN | `theon-and-jeyne-escape-winterfell` | 1 | ADWD | adwd-theon-01 | 277 | '"Go on. I will hold the kneelers here." The bloody spear was still clutched in her big hands.' | Frenya holds the drawbridge against the guards, sacrificing herself |
| `frenya` | VICTIM_IN | `theon-and-jeyne-escape-winterfell` | 1 | ADWD | adwd-theon-01 | 282 | 'From below them came shouting from where Frenya was fighting half a dozen guardsmen in the snow.' | Frenya overwhelmed by guards; implied dead or captured |
| `squirrel-free-folk` | AGENT_IN | `theon-and-jeyne-escape-winterfell` | 1 | ADWD | adwd-theon-01 | 152–153 | '"Out a window, and straight down to the godswood … I've done that Wall six times since, over and back again. I think I can climb down some stone tower."' | Squirrel's role: stay behind as the decoy Arya in the bed, then climb out independently |
| `myrtle` | AGENT_IN | `theon-and-jeyne-escape-winterfell` | 1 | ADWD | adwd-theon-01 | 141 | "Myrtle had servant's garb for Rowan. 'The yards are crawling with fools,' she warned them." | Myrtle brings Rowan's disguise for the escape |
| `willow-witch-eye` | AGENT_IN | `theon-and-jeyne-escape-winterfell` | 1 | ADWD | adwd-theon-01 | 247 | "Grunt gave Willow's breast a squeeze as she went by … Willow simply twisted away and past him." | Willow participates in the escape through the gate; draws guard attention |
| `willow-witch-eye` | AGENT_IN | `winterfell-murders-under-snow` | 2 | ADWD | adwd-a-ghost-in-winterfell-01 | 114 | '"You killed the others, why not him? Yellow Dick—" "—stank as bad as you."' (Rowan speaking for the group) | Part of the spearwife group Theon accuses of the murders; Tier-2 as no direct on-page confirmation per individual |
| `jeyne-poole` | VICTIM_IN | `theon-and-jeyne-escape-winterfell` | 1 | ADWD | adwd-theon-01 | 213–215 | '"I'll do what he wants … whatever he wants … with him or … or with the dog or … please … he doesn't need to cut my feet off, I won't try to run away …"' | Jeyne is the rescued captive; her terror-state emphasizes the cost of the captivity |
| `jeyne-poole` | RESCUES | `jeyne-poole` | — | — | — | — | — | WRONG edge shape; see note below — RESCUES goes theon→jeyne |
| `theon-greyjoy` | RESCUES | `jeyne-poole` | 1 | ADWD | adwd-theon-01 | 228–233 | '"You know me. I'm Theon, you remember. I know you too. I know your name." … He put a finger to her lips. "We can talk about that later. You need to be quiet now. Come with me. We will take you away from here."' | Theon chooses to rescue Jeyne despite knowing it will doom him if caught; a key moral-redemption beat |

---

### Bolton-men role edges (additional on-page appearances)

| source_slug | EDGE_TYPE | target_slug | tier | book | chapter-file | line | verbatim quote | note |
|-------------|-----------|-------------|------|------|--------------|------|----------------|------|
| `skinner` | PARTICIPATES_IN | `bolton-banner-raised-prisoners-killed` | 1 | ADWD | adwd-reek-02 | 183–184 | '"Damon, Alyn, see to them. Wine and ale, and all the food that they can eat. Skinner, show their wounded to our maesters." "Aye, my lord."' | Skinner deployed at Moat Cailin post-surrender; ironic hospitality before the flaying |
| `yellow-dick` | VICTIM_IN | `winterfell-murders-under-snow` | 1 | ADWD | adwd-a-ghost-in-winterfell-01 | 101–103 | "The dead man was one of Ramsay's favorites, the squat, scrofulous, ill-favored man-at-arms called Yellow Dick … someone had sliced it off and stuffed it into his mouth …" | Yellow Dick killed by the spearwives |
| `damon-dance-for-me` | AGENT_IN | `breaking-of-theon-at-the-dreadfort` | 1 | ADWD | adwd-reek-02 | 11–12 | '"Come back with that castle," said Damon Dance-for-Me as he helped Reek climb shaking into the saddle, "or keep going and see how far you get before we catch you."' | Damon's role as enforcer/torturer at the Dreadfort established |
| `sour-alyn` | AGENT_IN | `theon-and-jeyne-escape-winterfell` | 1 | ADWD | adwd-theon-01 | 195 | '"Try a wash yourself, Reek," said Sour Alyn. "You smell like horse piss." … But Alyn unlocked the door to the bedchamber …' | Sour Alyn guards Ramsay's bedchamber; his unlocking the door enables the rescue of Jeyne |

---

## HARVEST

> One-line pointers for notable-but-not-task finds encountered while reading.

### Food / meals (wide open per project rule)
- `acok-theon-02:365` / food / feast at Pyke: "a succession of fish stews, black bread, and spiceless goat. The tastiest thing Theon found to eat was an onion pie." — ironborn feast; hospitality context of Balon's war council
- `acok-theon-02:343` / food / Asha at feast: "Theon hacked a loaf of bread in half, hollowed out a trencher, and summoned a cook to fill it with fish stew."
- `acok-theon-05:41` / food-memory / nightmare-feast: Theon dreams of feasting Ned Stark threw for King Robert; "all wine and roast meat" turns to dining with the dead; load-bearing foreshadowing dream sequence
- `adwd-reek-01:1–19` / starvation / Reek eating a rat in the dungeon: the Dreadfort captivity is marked first by rat-eating; contrast to feasts above — graphic register of captive's food
- `adwd-reek-01:17` / starvation / Lady Hornwood allusion: "whenever he closed his eyes, he found himself remembering Lady Hornwood … locked her away in a tower and starved her to death. In the end she had eaten her own fingers." — eating fingers as parallel to Reek's rat; load-bearing cross-reference
- `adwd-reek-02:203` / meat / post-Moat Cailin reward: "half a chicken. Reek had to fight the dogs for the meat, but it was the best meal he'd had since Winterfell." — the chicken as reward; dogs as peers
- `adwd-reek-03:61` / feast / Barrowton feast (Stout's hall): ox slaughtered; "roasts and ribs, barley bread, a mash of carrots and pease, washing it all down with prodigious quantities of ale" — Ramsay commands a feast on depleted winter stores; cook's complaint about "we're the ones who'll be fucked when the snows come"
- `adwd-the-prince-of-winterfell-01:129–131` / wedding feast / Winterfell: "cod cakes and winter squash, hills of neeps and great round wheels of cheese, smoking slabs of mutton and beef ribs charred almost black, and lastly on three great wedding pies … chunks of seasoned pork swimming in a savory brown gravy … Manderly devoured six portions, two from each of the three pies" — THE Manderly pie scene; Theon cannot eat (broken teeth); "Ramsay hacked off slices with his falchion"
- `adwd-the-prince-of-winterfell-01:137` / eating difficulty / broken teeth: "Eating was hard for him. Ramsay had left him with so many broken teeth that chewing was an agony." — physical reminder of torture at feast
- `adwd-a-ghost-in-winterfell-01:15` / meal / garrison: "stale bread fried in bacon grease (the lords and knights ate the bacon)" — rationing hierarchy during the siege; pointed class distinction
- `adwd-a-ghost-in-winterfell-01:47` / meal / garrison: "Supper was pease porridge and yesterday's bread … above the salt, the lords and knights were seen to be eating ham." — continued rationing; muttering among common men
- `adwd-a-ghost-in-winterfell-01:105` / horsemeat feast: "great slabs of fresh horsemeat, charred outside and bloody red within, with roast onions and neeps … the common soldiers ate as well as the lords and knights" — stable collapse forces horsemeat; brief egalitarian meal
- `adwd-a-ghost-in-winterfell-01:107` / eating difficulty / Theon again: "The horsemeat was too tough for the ruins of Theon's teeth … he mashed the neeps and onions up together with the flat of his dagger and made a meal of that … The bone was beyond him."
- `adwd-theon-01:17` / breakfast / escape morning: "Abel, Rowan, and a mousy brown-haired washerwoman called Squirrel attack slabs of stale brown bread fried in bacon grease" — pre-escape meal; Theon drinks dark ale only

### Hospitality violations
- `acok-theon-03:57–61` / hospitality / Stony Shore villagers: "The men had been put to the sword, all but a handful that Theon had allowed to flee … Their wives and daughters had been claimed for salt wives … The crones and the ugly ones had simply been raped and killed …" — ironborn raid as inverse hospitality
- `acok-theon-06:99–101` / hospitality / Rodrik's terms: Theon's counter-offer to those who "swear fealty" contrasted with the violation of Winterfell's hosting; the Dreadfort men accepted Theon's gates as guests then betrayed him

### Descriptions / physical
- `acok-theon-01:291` / description / Balon Greyjoy: "He was smaller than Theon remembered … gaunt … nothing remained but hair and skin. Bone thin and bone hard he was, with a face that might have been chipped from flint. His eyes were flinty too, black and sharp, but the years and the salt winds had turned his hair the grey of a winter sea, flecked with whitecaps."
- `adwd-reek-01:83` / description / Theon's hands post-Dreadfort: "When he raised a hand, he was shocked to see how white it was, how fleshless. Skin and bones … I have an old man's hands."
- `adwd-the-prince-of-winterfell-01:51` / description / Theon at the wedding: "under the hood, his hair was white and thin, and his flesh had an old man's greyish undertone. A Stark at last, he thought."

### Foreshadowing / load-bearing quotes
- `acok-theon-05:11` / foreshadowing / wolf-nightmare: "great wolves the size of horses with the heads of small children … Their eyes were laughing at him, laughing, and the howl came again." — Theon's guilt manifests as direwolf nightmare; "They're dead, dead, I saw them killed" — Theon is already haunted by the truth
- `acok-theon-05:136–141` / foreshadowing / feast-with-the-dead nightmare: Theon dreams of the corpses of everyone killed in the war; "Robb came walking out of the night … man and wolf alike bled from half a hundred savage wounds." — foreshadows Red Wedding from Theon's perspective
- `adwd-a-ghost-in-winterfell-01:241–245` / foreshadowing / weirwood prayer: "'Please.' He fell to his knees … 'A sword, that's all I ask. Let me die as Theon, not as Reek.' … 'Bran,' the tree murmured." — Bran's greenseer connection to Winterfell; weirwood hears / knows the fake-deaths ("They know. The gods know. They saw what I did.")
- `adwd-the-prince-of-winterfell-01:87` / foreshadowing / weirwood at the wedding: '"Theon," a voice seemed to whisper. His head snapped up. "Who said that?"' — the weirwood speaks Theon's true name at the moment of the false wedding; parallel to the later godswood prayer scene

### Homeless quotes
- `acok-theon-06:131` / quote / Theon to Rodrik on hostage-taking: '"I was ten when I was taken from my father's house, to make certain he would raise no more rebellions." … "The noose I wore was not made of hempen rope, that's true enough, but I felt it all the same. And it chafed, Ser Rodrik. It chafed me raw."' — Theon's own articulation of his hostage trauma; one of the clearest self-aware moments
- `adwd-the-prince-of-winterfell-01:104` / quote / Theon on his ghost-making: "once Ramsay put Reek's face aside he'd slain all the men, and Theon's ironborn as well … None of them would help me. I had known them all for half my life, and not one of them would help me."
- `adwd-theon-01:186–187` / quote / Theon on Robb: "Robb who had been more a brother to Theon than any son born of Balon Greyjoy's loins. Murdered at the Red Wedding … I should have been with him. Where was I? I should have died with him."

---

## Notes

### Structural observations

1. **PRECEDES chain fragmentation.** The existing `battle-outside-the-gates-of-winterfell` → `bolton-forces-attack` → `sack-of-winterfell` sequence appears to be connected by old PRECEDES edges rather than causal edges. The three new CAUSES/ENABLES proposed above should replace or supplement these.

2. **`theon-carries-jeyne-up-battlements-stairs` dead-end confirmed.** This node has 0 outbound edges. The `SUB_BEAT_OF theon-and-jeyne-escape-winterfell` edge I propose wires it forward. The new `theon-and-jeyne-escape-winterfell` node then carries the downstream → `pink-letter-delivered` and → `stannis-march-on-winterfell` links.

3. **The Reek servant / Ramsay-as-Reek split.** The `reek` node (the original servant) appears in ACOK as a named, active character who physically performs the face-flaying and later provides the plan that exposes Ramsay's true identity. His edges should be on `reek`, not on `ramsay-snow`. The `ramsay-snow IMPERSONATES reek` edge is the load-bearing identity edge.

4. **Rowan / Holly / Frenya on-page murder assignments.** The text gives clear Tier-1 for Rowan on Yellow Dick ("stank as bad as you. A pig of a man." — first-person in-group admission). Holly kills the gate guard (on-page). Frenya holds the bridge (on-page). The other murders (groom pushed off wall, Ser Aenys's squire) are implied as the group; individual attribution is Tier-2. I've flagged accordingly.

5. **Little Walder Frey (no node).** The body brought into the hall by Ser Hosteen and Big Walder is identified as Little Walder. Per baseline rules, I do not mint a node. The murder is load-bearing (it triggers the Frey–Manderly brawl → the escape window). I have hung this event on `winterfell-murders-under-snow` and used existing slug `big-walder-frey` as WITNESS_IN (he found the body and reports it). VERIFY whether `big-walder-frey` has a node — if not, leave as orphan-targeted edge with a flag.

6. **Abel / Mance disambiguation.** The text confirms Abel = mance-rayder (bard with lute, six washerwoman "sisters," all spearwives). I use `mance-rayder` throughout per the baseline dedup map.

7. **`aenys-frey` slug** — listed in the baseline dedup map; used for the wedding WITNESS edge. `hosteen-frey` also in baseline. Used as-is.

8. **Theon's Moat Cailin role is unbuilt** (confirmed from baseline note 8). The proposed `theon-greyjoy AGENT_IN fall-of-moat-cailin` edge fills this gap; the text explicitly shows Theon talking the garrison into surrender using a forged safe-conduct from Ramsay.

9. **`big-walder-frey` slug.** Big Walder is mentioned in adwd-reek-01 and adwd-theon-01 (finds Little Walder's body). Baseline lists him only implicitly via "no node" for the Walders. VERIFY if a node exists before minting a WITNESS_IN edge; if no node, flag as orphan-targeted.

10. **`qarl-the-maid`** — listed in the baseline but does not appear in any of the twelve source chapters. No edge proposed.
