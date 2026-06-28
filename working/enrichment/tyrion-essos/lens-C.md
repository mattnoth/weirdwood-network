# Lens C — Descriptive / Quote / Object Depth — A2.4 Tyrion / Essos proposal (S161)

Chapters read: adwd-tyrion-03, adwd-tyrion-04, adwd-tyrion-05, adwd-tyrion-09, adwd-tyrion-10, adwd-tyrion-11

---

## Proposed NEW nodes

### 1. `tyrion-kills-nurse` (event.incident)
**Name:** Tyrion poisons Nurse  
**Type:** event.incident  
**Body:** Tyrion Lannister attends the ailing Nurse after the pale mare strikes the overseer. While other slaves refuse to go near him, Tyrion brings him dogtail soup laced with his poisonous mushrooms. Nurse's last word is "No"; Tyrion's last words to him are "A Lannister always pays his debts." The death is staged to look like pale-mare flux, enabling Tyrion's escape. This is the primary use of tyrions-mushrooms and the first confirmed kill that clears a path to freedom.  
**Anchor quote:** `"A Lannister always pays his debts."` — adwd-tyrion-11:69

### 2. `tyrion-aegon-cyvasse-game` (event.incident)
**Name:** Tyrion plays cyvasse with Young Griff  
**Type:** event.incident  
**Body:** Aboard the Shy Maid on the Rhoyne, Tyrion plays cyvasse against Young Griff (Aegon). The game is the vehicle through which Tyrion deploys strategic advice to Aegon — go directly to Westeros, do not detour to Dany — and signals Tyrion's growing grasp of the board of thrones. The game is distinct from the Haldon game (secrets wager) and from the Qavo Nogarys defeat (Selhorys, off-page, covered by other lenses).  
**Anchor quote:** `"I hope Your Grace will pardon me. Your king is trapped. Death in four."` — adwd-tyrion-04 cyvasse node (confirmed from wiki; line not in these 6 chapters directly — this game is narrated in adwd-tyrion-06/07, NOT in my chapters; see Dropped section)

> **NOTE:** The Tyrion-vs-Aegon cyvasse game is described in adwd-tyrion-06 (Selhorys chapter), which is NOT my assigned reading. I can surface the Tyrion-vs-Haldon wager game from adwd-tyrion-04 as a distinct event. The Aegon game must be flagged for the appropriate lens (Lens B covers tyrion-06).

### 2. `tyrion-haldon-cyvasse-wager` (event.incident) — REVISED
**Name:** Tyrion defeats Haldon at cyvasse (secrets wager)  
**Type:** event.incident  
**Body:** Aboard the Shy Maid, Tyrion proposes a secrets wager with Haldon Halfmaester — play for secrets instead of coin. After some three hours of play, Tyrion wins. This is the game referenced in the cyvasse node as where Tyrion "learns from Haldon the true identity of Young Griff." The game serves Tyrion's intelligence-gathering against the household. The cyvasse node body describes this at adwd-tyrion-04.  
**Anchor quote:** `"Fancy another game of cyvasse?" The Halfmaester always defeated him, but it was a way to pass the time.` — adwd-tyrion-04:137  
**Second anchor (result):** `"He's taken to his bed, in some discomfort. There are turtles crawling out his arse."` — adwd-tyrion-04:207 (Tyrion's aside confirming he won)

### 3. `tyrion-plumm-cyvasse-games` (event.incident)
**Name:** Tyrion defeats Brown Ben Plumm at cyvasse (5 games)  
**Type:** event.incident  
**Body:** In Yezzan zo Qaggaz's tent at the Yunkish siege camp, Tyrion plays five cyvasse games against Brown Ben Plumm after beating the unnamed Yunkish lord in blue (who upends the table in fury). Tyrion wins games one, three, four, and five; Plumm takes game two at double stakes. Tyrion reads Plumm's play as "stolid and tenacious" — "he plays so as not to lose" — information he later weaponizes when recruiting Plumm to switch sides. Yezzan zo Qaggaz profits handsomely.  
**Anchor quote:** `"Yollo wins again. Death in four."` — adwd-tyrion-10:277  
**Second anchor (reading Plumm):** `"He does not play to win," Tyrion realized. "He plays so as not to lose."` — adwd-tyrion-10:275

### 4. `pale-mare-sweeps-yunkish-camp` (event.incident)
**Name:** Pale mare sweeps the Yunkish camp  
**Type:** event.incident  
**Body:** The bloody flux (pale mare) tears through the Yunkish siege camp outside Meereen. Nurse contracts it and dies within two days; Yezzan zo Qaggaz follows immediately after. The disease is characterized vividly: fever, brown slime streaked with blood, uncontrollable diarrhea, unquenchable thirst. Tyrion observes the camp burning its dead in dark plumes of smoke. The outbreak creates the window through which Tyrion, Penny, and Jorah escape to the Second Sons.  
**Anchor quote:** `"Much and more can change in two days. Two days ago Nurse had been hale and healthy. Two days ago Yezzan had not heard the pale mare's ghostly hoofbeats."` — adwd-tyrion-11:25

---

## Proposed NEW edges

| Source | Edge type | Target | Tier | Qualifier | Evidence quote + chapter:line | Rationale |
|--------|-----------|--------|------|-----------|-------------------------------|-----------|
| tyrion-lannister | OWNS | tyrions-mushrooms | Tier-1 | — | "Tyrion still had the poison mushrooms he had plucked from the grounds of Illyrio's manse" adwd-tyrion-05:99 | Establishes Tyrion's possession — node has 0 edges; this is the book-confirmed ownership |
| tyrion-lannister | WIELDS | tyrions-mushrooms | Tier-1 | — | "Watered wine and lemonsweet and some nice hot dogtail soup, with slivers of mushroom in the broth." adwd-tyrion-11:69 | The actual deployment — mushrooms used as a weapon against Nurse |
| tyrions-mushrooms | KILLS | nurse | Tier-2 | — | "The last word Nurse ever said was, 'No.' The last words he ever heard were, 'A Lannister always pays his debts.'" adwd-tyrion-11:69 | Implied kill — Tyrion feeds mushrooms in soup; Nurse dies; text strongly implies intentional poisoning (Tier-2, not Tier-1, because GRRM leaves it ambiguous whether flux alone vs. mushrooms killed him) |
| tyrion-lannister | KILLS | nurse | Tier-2 | — | "Watered wine and lemonsweet and some nice hot dogtail soup, with slivers of mushroom in the broth." adwd-tyrion-11:69 | Tyrion is the agent of Nurse's death via poisoning; same Tier-2 caution as above |
| tyrions-mushrooms | OWNED | yezzan-zo-qaggaz | Tier-2 | — | [BORDERLINE — prop skipped; see Dropped] | — |
| tyrion-lannister | OWNS | pretty-pig | Tier-1 | — | "he found himself clad in Groat's painted wooden armor, astride Groat's sow" adwd-tyrion-09:28; "Tyrion kicked at Pretty's haunches to speed her to a charge" adwd-tyrion-09:21 | Tyrion uses and rides Pretty Pig aboard the Selaesori Qhoran; node has 0 edges |
| pretty-pig | OWNED | penny | Tier-1 | — | "She had been trained to saddle and bridle since she was a piglet." adwd-tyrion-09:13; "Her name was Pretty, short for Pretty Pig" adwd-tyrion-09:13 | Pretty Pig is Penny's pig (Groat's originally, inherited by Penny) |
| crunch | OWNED | penny | Tier-1 | — | "Penny collected her dog and pig and led them both below." adwd-tyrion-09:59 | Crunch (the dog) belongs to Penny; wiki node for Crunch already has OWNS → Penny but with wrong direction — this verifies/corrects the direction |
| tyrion-lannister | PARTICIPATES_IN | tyrion-haldon-cyvasse-wager | Tier-1 | — | "Fancy another game of cyvasse?" adwd-tyrion-04:137 | Tyrion proposes and plays the secrets-wager game |
| haldon | PARTICIPATES_IN | tyrion-haldon-cyvasse-wager | Tier-1 | — | "The day you defeat me at cyvasse will be the day turtles crawl out my arse." adwd-tyrion-04:199 | Haldon accepts the wager |
| tyrion-lannister | DEFEATS | haldon | Tier-1 | — | "He's taken to his bed, in some discomfort. There are turtles crawling out his arse." adwd-tyrion-04:207 | Tyrion wins; Haldon's discomfort is comic confirmation |
| tyrion-lannister | PARTICIPATES_IN | tyrion-plumm-cyvasse-games | Tier-1 | — | "Brown Ben Plumm lifted the fallen table, smiling. 'Try me next, dwarf.'" adwd-tyrion-10:261 | Tyrion plays Plumm at cyvasse in Yezzan's tent |
| brown-ben-plumm | PARTICIPATES_IN | tyrion-plumm-cyvasse-games | Tier-1 | — | "Yollo wins again. Death in four." adwd-tyrion-10:277 | Plumm participates and loses final game |
| tyrion-lannister | DEFEATS | brown-ben-plumm | Tier-1 | — | "Yollo wins again. Death in four." adwd-tyrion-10:277 | Final-game verdict explicit; Tyrion wins 4 of 5 |
| shy-maid | CREW_OF | yandry | Tier-1 | — | "Yandry stole a glance at Septa Lemore from time to time as he was checking the lines." adwd-tyrion-04:51 | Yandry is established as crew — node has 0 edges; book-cite upgrade |
| shy-maid | CREW_OF | ysilla | Tier-1 | — | "Ysilla had the tiller." adwd-tyrion-05:13 | Ysilla operates the tiller — crew confirmed |
| stone-men-attack-the-shy-maid | CAUSES | jon-connington AFFLICTED_BY greyscale | Tier-2 | — | [See note] | The attack is the WHERE of Connington's infection — he pulls Tyrion from the river. The causal chain: attack → Connington drags Tyrion up → greyscale exposure. However, the actual pulling-from-river beat and infection are NOT described in adwd-tyrion-05 (which ends with Tyrion sinking). This edge is proposed by inference from what we know about Connington's chapters. Mark **[BORDERLINE]** — the causal wiring from Tyrion's POV ends before he surfaces. |
| **[BORDERLINE]** stone-men-attack-the-shy-maid | CAUSES | jon-connington AFFLICTED_BY greyscale | Tier-2 | — | "A stone man staggered forward, his hands outstretched and grasping. Tyrion drove a shoulder into him. … They hit the river with a towering splash, and Mother Rhoyne swallowed up the two of them." adwd-tyrion-05:229-231 | Tyrion's chapter ends as he sinks; Jon Connington's chapter (not in my assigned set) confirms he pulled Tyrion out. The event = the vector of infection. Wiring lens should confirm. |
| pale-mare-sweeps-yunkish-camp | KILLS | nurse | Tier-1 | — | "Much and more can change in two days. Two days ago Nurse had been hale and healthy." adwd-tyrion-11:25 | Nurse dies in the outbreak (Tyrion's mushrooms likely hastened it, but the pale mare is the listed cause) |
| pale-mare-sweeps-yunkish-camp | KILLS | yezzan-zo-qaggaz | Tier-1 | — | "The pale mare," the man told Sweets." adwd-tyrion-11:11 | Yezzan diagnosed with pale mare and is moribund |
| bloody-flux | AFFLICTED_BY | nurse | Tier-1 | — | "Much and more can change in two days. Two days ago Nurse had been hale and healthy." adwd-tyrion-11:25 | Nurse contracts the flux |
| bloody-flux | AFFLICTED_BY | yezzan-zo-qaggaz | Tier-1 | — | "'The pale mare,' the man told Sweets." adwd-tyrion-11:11 | Yezzan zo Qaggaz diagnosed |
| pale-mare-sweeps-yunkish-camp | ENABLES | tyrion-penny-jorah-join-second-sons | Tier-1 | — | "Yezzan has more urgent matters to concern him than three missing slaves. He's riding the pale mare." adwd-tyrion-11:294 | The chaos of the outbreak is the precondition that makes escape possible; Tyrion explicitly articulates this |
| tyrion-lannister | MANIPULATES | brown-ben-plumm | Tier-1 | via_flattery | "I do enjoy defeating you. I hear you're twice a turncloak, Plumm. A man after mine own heart." adwd-tyrion-11:287 | Tyrion actively recruits Plumm using flattery + dragon-blood lore + cyvasse intelligence; new MANIPULATES edge distinct from any existing ones (Plumm not in baseline dedup hot zones) |
| tyrion-lannister | REVEALS_TO | brown-ben-plumm | Tier-1 | — | "Not only do I know that the queen's dragons took to you, but I know why." adwd-tyrion-11:311 | Tyrion reveals his knowledge of Plumm's dragon-blood lineage as the persuasion hook; this is not a theory assertion — it's Tyrion stating information to Plumm |
| selaesori-qhoran | CREW_OF | moqorro | Tier-1 | — | "He was surprised to find that Moqorro and two of his fiery fingers had joined them on the sterncastle." adwd-tyrion-09:119 | Moqorro is a named passenger/religious leader aboard the Selaesori Qhoran; shipwreck node should include this |

---

## Dropped / considered-but-rejected

**Tyrion-vs-Aegon cyvasse game:** The game where Tyrion tells Aegon "Your king is trapped. Death in four" / "go to Westeros" is not in my assigned chapters (adwd-tyrion-03–05, 09–11). It occurs in adwd-tyrion-06, which is Lens B's chapter. Flagged for Lens B to pick up. `tyrion MANIPULATES aegon` already exists per baseline dedup.

**Jon Connington pulls Tyrion from the river:** adwd-tyrion-05 ends with Tyrion sinking unconscious — the moment of rescue is in JON CONNINGTON's chapters, not Tyrion's. I cannot quote the rescue from these 6 chapters. The causal edge (attack → infection) is proposed as BORDERLINE above, sourced from Tyrion's sinking beat as the clear precondition.

**Tyrion AFFLICTED_BY greyscale:** Explicitly ruled out in LENS-SHARED.md. Tyrion fears it, washes obsessively, but is NOT infected. Not proposed.

**Tyrion OWNS selaesori-qhoran:** Tyrion is a passenger, not an owner. Not proposed.

**The mummer's joust show (dwarf show):** `tyrion PARTICIPATES_IN dwarf-show-meereen` — this event node may or may not exist. If it doesn't, building it belongs to Lens A or Lens D (ch12 is theirs). The adwd-tyrion-09 and -10 show aboard the Selaesori Qhoran is a shipboard performance, distinct from the Great Pit show. I note both happened but the Pit performance (ch12) is outside my chapters.

**Selaesori Qhoran shipwreck:** A major event but adwd-tyrion-09 ends right before the storm fully destroys the ship. The shipwreck itself is fully described at the end of tyrion-09. This is a proposed event for Lens A (ch11 baseline notes it as a BUILD candidate). I surface it here only as a harvest note and do not propose a new event node since it crosses into Lens A territory.

**Pretty Pig's ownership chain:** Groat → Penny. Groat (Penny's dead brother, also named Oppo per baseline) owned Pretty Pig first. I note Tyrion calls the armor "Groat's" in ch09. But Oppo's ownership is prior; what matters for the live graph is Penny's possession now. Proposed Penny → Pretty Pig above.

**Crunch OWNS direction:** The wiki node says `crunch OWNS penny` (incorrect direction — Penny owns Crunch). This may be a wiki parsing artifact. I propose the correct `crunch OWNED penny` but since the corrective is implicit in `pretty-pig OWNED penny` by parallel, I flag it but don't re-propose the OWNS with wrong direction.

**Tyrion-Jorah dynamic edges (DISTRUSTS, RESENTS):** These dyads are likely in the saturated Tyrion web (224+ edges). The confrontation where Jorah hits Tyrion (ch09) is vivid but `jorah ASSAULTS tyrion` is implied-existing. Not proposed without baseline confirmation.

**Tryion FEARS greyscale / Shy Maid:** Internal psychological edge — FEARS is in the vocab but the target would need to be a node (`greyscale`). If a greyscale node exists I'd propose it but it doesn't appear in baseline; this is node-prose territory.

**Stone-men individual description as objects:** The stone men's physical appearance (calcified grey flesh, blood oozing from knuckles, black skin where the Summer Islander's greyscale hadn't fully taken) — vivid but the stone-men node exists as a character group. Description goes into Harvest not as an edge.

**Shrouded Lord:** Referenced in adwd-tyrion-03 and -05 as a legend. Not a confirmed graph node in my scope; leave as node-prose.

**Yezzan's grotesquerie members (goat-boy, two-headed girl, bearded woman, Sweets):** Sweets has a node (mentioned in baseline as `sweets`). The others may or may not. No explicit edge opportunities for my lens targets. Sweets edges go to Lens A/D.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|--------------|------|
| food | ADWD | adwd-tyrion-03:147 | "simple supper of salt pork and cold white beans, washed down with ale" — first shipboard meal after meeting Duck/Haldon, described as "pleasant change from all the rich food" |
| food | ADWD | adwd-tyrion-04:65 | "Some days she cooked biscuits and bacon; some days bacon and biscuits. Once every fortnight there might be a fish" — Ysilla's shipboard cooking routine |
| food | ADWD | adwd-tyrion-04:67 | "They were best when eaten hot, dripping with honey and butter" — Tyrion steals a hot biscuit off the brazier |
| food | ADWD | adwd-tyrion-04:83 | "She fed them on the afterdeck, pressing honeyed biscuits on Young Griff and hitting Duck's hand with her spoon whenever he made a grab for more bacon" — breakfast scene, Ysilla's wooden spoon |
| food | ADWD | adwd-tyrion-03:53 | "There is a gift for the boy in one of the chests. Some candied ginger. He was always fond of it." — Illyrio's parting gift to Young Griff, foreshadowing Illyrio's affection |
| drink | ADWD | adwd-tyrion-04:13 | "he drank water, and was condemned to sleepless nights and days of sweats and shakes" — Griff forbids wine; Tyrion's withdrawal described |
| drink | ADWD | adwd-tyrion-04:27 | "I would kill for a cup of wine" — Tyrion's flat longing for wine |
| food | ADWD | adwd-tyrion-05:87 | "What word from old Volantis? … 'War'" — exchange with passing Kingfisher poleboat in the Sorrows |
| food/drink | ADWD | adwd-tyrion-09:25 | "The captain's wine had been the first thing to run out. You could get drunk much quicker on rum than on wine" — shipboard rationing on Selaesori Qhoran; rum replaces wine |
| food | ADWD | adwd-tyrion-09:169 | "Pretty and Crunch were both half-mad with fear. The dog was barking … The sow had been shitting everywhere" — storm scene; animals' distress, no food |
| food | ADWD | adwd-tyrion-09:189 | "Who do you suppose they'll carve up first … the pig, the dog, or me?" — Tyrion's gallows humor about being eaten; crew eyeing the animals |
| food | ADWD | adwd-tyrion-10:199 | "the air smelled of roasting meat, and he saw one man skinning a dog for his stewpot" — Yunkish camp; dog-eating detail |
| food | ADWD | adwd-tyrion-10:195 | "The Yunkish encampment was not one camp but a hundred camps … Between the siege lines and the bay, tents had sprouted up like yellow mushrooms" — siege-camp geography; "yellow mushroom" simile |
| food/drink | ADWD | adwd-tyrion-10:63 | "He looked as large as four Illyrios … The way those yellow eyes were fixed upon the block made Tyrion uncomfortable" — Yezzan at auction, described consuming lemon drink from slave's hand |
| food | ADWD | adwd-tyrion-10:243-253 | post-performance feast in Yezzan's tent; dwarfs serve and pour wine; Tyrion gets "purple wine" flagon, Penny water; they eat "leavings" of the feast afterward, Nurse: "Eat quickly. All this must be clean again before you sleep" |
| food | ADWD | adwd-tyrion-11:13-15 | Yezzan's pale-mare symptoms: "brown slime streaked with blood" and uncontrollable diarrhea; healer orders "clean fresh water, as much as he will drink" — vivid disease description |
| food/drink | ADWD | adwd-tyrion-11:69 | Nurse's death soup: "Watered wine and lemonsweet and some nice hot dogtail soup, with slivers of mushroom in the broth" — the poisoned meal; vivid and load-bearing |
| description | ADWD | adwd-tyrion-03:185 | Shy Maid's appearance: "Her paintwork was a muddy greyish brown, mottled and flaking; her big curved tiller, plain and unadorned. She looks like dirt" — physical description of the vessel |
| description | ADWD | adwd-tyrion-03:183 | Young Griff's appearance: "a lithe and well-made youth … a shock of dark blue hair. The dwarf put his age at fifteen, sixteen" — first description |
| description | ADWD | adwd-tyrion-03:193 | Griff's appearance: "Griff's cloak was made from the hide and head of a red wolf of the Rhoyne. Under the pelt he wore brown leather stiffened with iron rings" + "ice blue, pale, cold" eyes |
| description | ADWD | adwd-tyrion-04:49 | Lemore's stretch marks: "She had stretch marks on her belly that could only have come from childbirth" — clue about her past identity |
| description | ADWD | adwd-tyrion-04:55 | Turtle variety on the Rhoyne: "flatbacks and red-ears, softshells and bonesnappers, brown turtles, green turtles, black turtles, clawed turtles and horned turtles, turtles whose ridged and patterned shells were covered with whorls of gold and jade and cream" — lavish natural description |
| description | ADWD | adwd-tyrion-04:225-226 | The Old Man of the River: enormous horned turtle, "its dark green shell mottled with brown and overgrown with water moss and crusty black river molluscs" — bellowed louder than a warhorn; Ysilla weeps |
| description | ADWD | adwd-tyrion-05:11 | Opening image: "The Shy Maid moved through the fog like a blind man groping his way down an unfamiliar hall" — load-bearing atmospheric simile |
| description | ADWD | adwd-tyrion-05:127 | Bridge of Dream physical description: "Half of them had collapsed, pulled down by the weight of the grey moss … Pale stone arches marched off into the fog … The broad wooden span of the bridge had rotted through, but some of the lamps that lined the way were still aglow" |
| description | ADWD | adwd-tyrion-05:127 | Stone men: "shuffling aimlessly around the lamps like slow grey moths. Some were naked, others clad in shrouds" — first visual of stone men on the bridge |
| description | ADWD | adwd-tyrion-05:211 | Stone man's injury: "The leap had shattered one of his legs, and a jagged piece of pale bone jutted out through the rotted cloth of his breeches and the grey meat beneath. The broken bone was speckled with brown blood" — most vivid physical description of stone men |
| description | ADWD | adwd-tyrion-05:225 | Stone man's skin: "he had been a Summer Islander … his skin was black as midnight where it was not grey. Where he had grasped the torch, his skin had cracked and split. Blood was seeping from his knuckles though he did not seem to feel it" — greyscale's physical toll |
| description | ADWD | adwd-tyrion-04:119 | Tyrion's jester motley: "His doublet was divided down the middle; the left side was purple velvet with bronze studs; the right, yellow wool embroidered in green floral patterns. His breeches were similarly split; the right leg was solid green, the left leg striped in red and white" — Lemore's handiwork |
| description | ADWD | adwd-tyrion-09:13-15 | Pretty Pig physical: "Patient and sure-footed, she accepted Tyrion with hardly a squeal … The painted wooden armor clattered as Pretty trotted across the deck" |
| description | ADWD | adwd-tyrion-09:19 | Penny on Crunch: "Penny rode her big grey dog, her striped lance waving drunkenly as the beast bounded across the deck. Her shield and armor had been painted red, though the paint was chipped and fading; his own armor was blue." |
| description | ADWD | adwd-tyrion-10:123-129 | Yezzan's golden collar: "The collars were made of iron, lightly gilded to make them glitter in the light. Yezzan's name was incised into the metal in Valyrian glyphs, and a pair of tiny bells were affixed below the ears, so the wearer's every step produced a merry little tinkling sound" |
| description | ADWD | adwd-tyrion-10:91 | Yezzan zo Qaggaz at auction: "covered all in yellow silk fringed with gold, he looked as large as four Illyrios" + "piggy yellow eyes and breasts big as Pretty Pig pushing at the silk of his tokar" |
| description | ADWD | adwd-tyrion-10:123 | Nurse's appearance: "a long narrow face and a chin beard bound about with golden wire, and his stiff red-black hair swept out from his temples to form a pair of taloned hands" |
| description | ADWD | adwd-tyrion-10:139 | Jorah's branding and state: "Upon one cheek he bore a brand: a demon's mask. … Both his eyes were blackened, two dark pits in that grotesquely swollen face" |
| description | ADWD | adwd-tyrion-11:33 | Yezzan in death throes: "squirming fitfully in a pool of his own excrement. His shit had turned to brown slime streaked with blood" — pale mare's symptoms on Yezzan |
| quote | ADWD | adwd-tyrion-03:131 | "The Shrouded Lord is just a legend, he told himself, no more real than the ghost of Lann the Clever that some claim haunts Casterly Rock" — Tyrion's self-reassurance in the Sorrows (load-bearing for Shrouded Lord node if minted) |
| quote | ADWD | adwd-tyrion-03:257 | "Of course it is, thought Tyrion. The game of thrones." — Tyrion's internal response to Griff's warning; load-bearing character insight |
| quote | ADWD | adwd-tyrion-04:161 | "If you want to conquer the world, you best have dragons." — Young Griff's lesson conclusion; excellent ## Quotes candidate for aegon-targaryen-young-griff node |
| quote | ADWD | adwd-tyrion-05:99 | "Tyrion still had the poison mushrooms he had plucked from the grounds of Illyrio's manse, and there were days when he was sore tempted to slip them into Griff's supper" — confirms mushroom possession aboard Shy Maid; tyrions-mushrooms anchor |
| quote | ADWD | adwd-tyrion-05:235 | "There are worse ways to die than drowning. And if truth be told, he had perished long ago, back in King's Landing" — Tyrion sinking, his near-death reflection; excellent anchor for Tyrion's psychological state node-prose |
| quote | ADWD | adwd-tyrion-09:103 | "Prophecy is like a half-trained mule … it looks as though it might be useful, but the moment you trust in it, it kicks you in the head" — Tyrion to Jorah after the shipwreck; anchor for Tyrion's worldview node |
| quote | ADWD | adwd-tyrion-10:103 | "I joust, I sing, I say amusing things. I'll fuck your wife and make her scream. … men three times my size quail and tremble when we meet across a cyvasse table. … My father told me I must always pay my debts." — auction-block speech; cyvasse node and Tyrion character node |
| quote | ADWD | adwd-tyrion-11:69 | "The last word Nurse ever said was, 'No.' The last words he ever heard were, 'A Lannister always pays his debts.'" — tyrions-mushrooms node and tyrion-kills-nurse event anchor |
| quote | ADWD | adwd-tyrion-11:155 | "If I dance just right, maybe I can ring 'The Rains of Castamere.'" — Tyrion's bitter irony about his collared bells; excellent Tyrion character quote |
| object | ADWD | adwd-tyrion-10:197 | The trebuchets: "Dragonbreaker, Harridan, Harpy's Daughter, Wicked Sister, Ghost of Astapor, Mazdhan's Fist" — six named Yunkish trebuchets; harvest for a siege-of-meereen node |
| object | ADWD | adwd-tyrion-09:17 | Selaesori Qhoran's figurehead: "even her figurehead had not escaped; one of his arms had broken off, the one with all his scrolls" — physical damage after the storm |
| object | ADWD | adwd-tyrion-04:143 | Haldon's cabin on Shy Maid: "One wall was lined with bookshelves and bins stacked with old scrolls and parchments; another held racks of ointments, herbs, and potions" — enrichment for haldon node |
| object | ADWD | adwd-tyrion-10:223 | Yezzan's grotesquerie members: "a boy with twisted, hairy 'goat legs,' a two-headed girl out of Mantarys, a bearded woman, and a willowy creature called Sweets who dressed in moonstones and Myrish lace" — grotesquerie ensemble; Sweets description |
| greyscale | ADWD | adwd-tyrion-05:35-36 | Tyrion's clinical greyscale knowledge: "limes, mustard poultices, and scalding-hot baths (the maesters said) or by prayer, sacrifice, and fasting (the septons insisted)" — his medical-textbook summary |
| greyscale | ADWD | adwd-tyrion-05:125 | "He had heard it said that there were three good cures for greyscale: axe and sword and cleaver" — Tyrion's grim humor + knowledge |
| foreshadowing | ADWD | adwd-tyrion-04:233 | "Gods and wonders always appear, to attend the birth of kings" — Tyrion's internal reaction to the Old Man of the River's appearance; foreshadowing Aegon's destiny? |
| hospitality | ADWD | adwd-tyrion-10:155 | "In Yunkai you will dwell in the golden pyramid of Qaggaz and dine off silver plates, but here we live simply, in the humble tents of soldiers" — Nurse's ironic promise of hospitality as a slave |
| hospitality | ADWD | adwd-tyrion-10:281-282 | After Yezzan's feast, servers eat leavings: "Nurse reappeared to tell the servers that they might make their own feast from the leavings" — inverted hospitality; slaves eat what masters discard |
