# Lens 3 — Descriptive / Quote / Object Depth
## Cersei's-downfall enrichment — S140 proposal

---

## NEW NODES

### 1. `maggy-the-frog-prophecy`
- **type:** event.revelation
- **identity:** Maggy the Frog delivers her three-question prophecy to young Cersei (and Melara Hetherspoon) in Lannisport — the moment that plants the valonqar/younger-queen curse that drives Cersei's AFFC downfall
- **anchor quote:** "Queen you shall be . . . until there comes another, younger and more beautiful, to cast you down and take all that you hold dear." / "And when your tears have drowned you, the valonqar shall wrap his hands about your pale white throat and choke the life from you."
- **chapter:line:** `affc-cersei-08.md:243–251`
- **note:** Text establishes this happened when Cersei was ten (affc-cersei-05.md:389), years before the story opens. Maggy is already dead in AFFC; this is a flashback/dream. Anchor the node to the AFFC dream recollection.

### 2. `murder-of-the-old-high-septon`
- **type:** event.killing
- **identity:** Osney Kettleblack smothers the previous High Septon with a pillow, on Cersei's order — the crime that Osney's confession to the new High Septon eventually reveals, triggering Cersei's arrest
- **anchor quote:** "She's the queen I fucked, the one sent me to kill the old High Septon. He never had no guards. I just come in when he was sleeping and pushed a pillow down across his face."
- **chapter:line:** `affc-cersei-10.md:243`
- **note:** This event is referenced in the baseline's `osney-kettleblack-confesses` edge (same quote). Proposing the murder-event node to give it a proper anchor; the confession edge already uses the same line, so the quote is confirmed correct.

### 3. `cersei-s-walk-of-atonement` (stub node — barely in scope for AFFC)
- **type:** custom.walk_of_atonement (if no suitable type) → suggest `event.punishment`
- **identity:** Cersei's future walk of atonement — not yet occurred in AFFC but is the downstream consequence of her imprisonment; mentioned only in architecture context as a known node gap
- **anchor:** NOT anchored in AFFC text (chapter 10 ends before the walk). SKIP — do not propose without an AFFC text anchor.
- **verdict: WITHDRAWN** — no textual grounding in these 10 chapters. Flag for a later ADWD/AFFC epilogue enrichment pass.

---

## EDGES

### E1 — Prophecy motivates Cersei psychologically (AFFC-wide)
```
maggy-the-frog-prophecy --[MOTIVATES]--> cersei-lannister
```
- **Tier:** 1
- **chapter:line:** `affc-cersei-08.md:251`
- **quote:** "And when your tears have drowned you, the valonqar shall wrap his hands about your pale white throat and choke the life from you."
- **rationale:** The prophecy is Cersei's persistent psychological engine throughout all 10 chapters — her plots against Margaery are explicitly framed as pre-empting the "younger and more beautiful" queen. MOTIVATES targets a character (Cersei), which is correct per agency rules.

### E2 — Prophecy subjects Cersei
```
cersei-lannister --[SUBJECT_OF_PROPHECY]--> maggy-the-frog-prophecy
```
- **Tier:** 1
- **chapter:line:** `affc-cersei-08.md:243`
- **quote:** "Queen you shall be . . . until there comes another, younger and more beautiful, to cast you down and take all that you hold dear."
- **rationale:** Cersei is the named subject of the foretelling; standard prophecy tagging.

### E3 — Maggy prophesied to Cersei
```
maggy-the-frog --[PROPHESIED_BY]--> maggy-the-frog-prophecy
```
- **Tier:** 1
- **chapter:line:** `affc-cersei-08.md:227–251`
- **quote:** "Three questions may you ask," the crone said, once she'd had her drink. "You will not like my answers."
- **rationale:** Maggy is the author/source of the prophecy.

### E4 — Prophecy foreshadows Cersei's downfall arc
```
maggy-the-frog-prophecy --[FORESHADOWS]--> cersei-is-captured-in-the-sept
```
- **Tier:** 2
- **chapter:line:** `affc-cersei-10.md:49`
- **quote:** "Maggy the Frog should have been in motley too, for all she knew about the morrow. Cersei prayed the old fraud was screaming down in hell. The younger queen whose coming she'd foretold was finished, and if that prophecy could fail, so could the rest."
- **rationale:** Cersei explicitly links the prophecy to her present situation and her capture is the fulfillment of the arc Maggy set in motion; FORESHADOWS is appropriate as the prophecy precedes and anticipates the capture event.

### E5 — Murder of old High Septon: Cersei orders, Osney executes
```
cersei-lannister --[SUSPECTED_OF]--> murder-of-the-old-high-septon
```
- **Tier:** 2
- **chapter:line:** `affc-cersei-10.md:243`
- **quote:** "She's the queen I fucked, the one sent me to kill the old High Septon."
- **rationale:** Osney confesses this under torture/duress; the text doesn't give us Cersei's explicit earlier order on-page (she arranged it off-page). SUSPECTED_OF is the right hedge — Osney's tortured confession is in-world contested evidence, not author-narrated fact. This is a Tier-2 unproven-but-load-bearing attribution.

```
osney-kettleblack --[AGENT_IN]--> murder-of-the-old-high-septon
```
- **Tier:** 1
- **chapter:line:** `affc-cersei-10.md:243`
- **quote:** "I just come in when he was sleeping and pushed a pillow down across his face."
- **rationale:** Osney confesses the act directly; AGENT_IN is correct.

### E6 — Murder-event TRIGGERS the confession
```
murder-of-the-old-high-septon --[ENABLES]--> osney-kettleblack-confesses-to-high-sparrow
```
- **Tier:** 1
- **chapter:line:** `affc-cersei-10.md:243`
- **quote:** "She's the queen I fucked, the one sent me to kill the old High Septon."
- **rationale:** The murder is the crime Osney confesses; it is a precondition / door-opener for the confession's explosive power — without it, his "bedding the queen" confession is merely adultery, not murder+treason. ENABLES (a precondition) fits better than CAUSES here.

### E7 — Cersei-fills-in-arrest-warrants CAUSES arrest of the ten men (causal wiring)
```
cersei-fills-in-the-arrest-warrants --[CAUSES]--> cersei-plots-against-margaery
```
- **verdict: REJECTED** — `cersei-fills-in-the-arrest-warrants` is a constitutive beat of `cersei-plots-against-margaery`, not a downstream consequence. Would be agency-collapse (SUB_BEAT_OF at best). The correct wiring is:

```
cersei-plots-against-margaery --[CAUSES]--> cersei-fills-in-the-arrest-warrants
```
- **Tier:** 1
- **chapter:line:** `affc-cersei-10.md:77`
- **quote:** "Cersei had written in the names herself: Ser Tallad the Tall, Jalabhar Xho, Hamish the Harper, Hugh Clifton, Mark Mullendore, Bayard Norcross, Lambert Turnberry, Horas Redwyne, Hobber Redwyne, and a certain churl named Wat, who called himself the Blue Bard."
- **rationale:** The arrest warrants flow causally from the plot; this wires the islanded event into the causal spine.

### E8 — Cersei-is-stripped-and-imprisoned ENABLES cersei-s-walk-of-atonement (downstream)
- **verdict: DEFERRED** — walk-of-atonement node doesn't exist and AFFC ends before the walk. Cannot ground this in AFFC text. Flag for later pass.

### E9 — Robert Strong creation: Qyburn proposes the champion
```
qyburn --[ADVISES]--> cersei-lannister
```
(re: the creation of robert-strong as Cersei's champion)
- **Tier:** 1
- **chapter:line:** `affc-cersei-10.md:307`
- **quote:** "My queen, your champion stands ready. There is no man in all the Seven Kingdoms who can hope to stand against him."
- **rationale:** Qyburn advises Cersei about her champion (robert-strong) in the prison cell. ADVISES targets a character correctly. This is a new edge not in the baseline.

### E10 — Cersei imprisoned-at Great Sept, downstream node (dead-end fix)
```
cersei-is-stripped-and-imprisoned --[CAUSES]--> cersei-sends-message-to-jaime
```
- **verdict: WITHDRAWN** — there is no existing node for "cersei sends message to jaime." This is a real event but minting a new event node is beyond my propose-only lens. Flag for orchestrator: Cersei's plea to Jaime (affc-cersei-10.md:313–317) is a clear downstream consequence of her imprisonment and a new event worth minting.

---

## EDGES (final confirmed list — 8 edges)

| # | Source | Type | Target | Tier | Line |
|---|--------|------|--------|------|------|
| E1 | maggy-the-frog-prophecy | MOTIVATES | cersei-lannister | 1 | cersei-08:251 |
| E2 | cersei-lannister | SUBJECT_OF_PROPHECY | maggy-the-frog-prophecy | 1 | cersei-08:243 |
| E3 | maggy-the-frog | PROPHESIED_BY | maggy-the-frog-prophecy | 1 | cersei-08:227 |
| E4 | maggy-the-frog-prophecy | FORESHADOWS | cersei-is-captured-in-the-sept | 2 | cersei-10:49 |
| E5a | cersei-lannister | SUSPECTED_OF | murder-of-the-old-high-septon | 2 | cersei-10:243 |
| E5b | osney-kettleblack | AGENT_IN | murder-of-the-old-high-septon | 1 | cersei-10:243 |
| E6 | murder-of-the-old-high-septon | ENABLES | osney-kettleblack-confesses-to-high-sparrow | 1 | cersei-10:243 |
| E7 | cersei-plots-against-margaery | CAUSES | cersei-fills-in-the-arrest-warrants | 1 | cersei-10:77 |
| E9 | qyburn | ADVISES | cersei-lannister | 1 | cersei-10:307 |

---

## HARVEST

### OBJECTS / ARTIFACTS

`affc-cersei-02.md:183` / object / Old Gardener gold coin found under Rugen's chamber pot — "On one side was a king's face in profile, on the other side the imprint of a hand." — Garth the Twelfth / House Gardener sigil; Cersei reads it as Tyrell conspiracy

`affc-cersei-03.md:148` / object-lute / Margaery's wedding where "the Blue Bard" first appears playing love songs — the same lute Cersei later smashes

`affc-cersei-09.md:143–163` / object-lute / The Blue Bard's lute described before Cersei uses it as a weapon: "Beneath the courtesy, there was a faint hint of unease, but he handed her the lute all the same. One does not refuse the queen's request." — then "Cersei smashed the lute across the singer's face so hard the painted wood exploded into shards and splinters."

`affc-cersei-04.md:187` / debt / Crown's debt to the Iron Bank: "I have decided to defer our repayment of the sums owed the Holy Faith and the Iron Bank of Braavos until war's end." — exact sum not stated here; contrast with affc-cersei-06.md:269 where High Septon states "Nine hundred thousand six hundred and seventy-four dragons" (the Faith debt figure)

`affc-cersei-06.md:269` / debt / Crown's debt to the Faith: "Nine hundred thousand six hundred and seventy-four dragons. Gold that could feed the hungry and rebuild a thousand septs." — exact figure spoken by High Sparrow; forgiven in the rearming deal

`affc-cersei-06.md:186–187` / crown-sold / The crystal crown Lord Tywin gave the old High Septon, now sold by the new one: "My lord father gave your predecessor a crown of rare beauty, wrought in crystal and spun gold." / "And for that gift we honor him in our prayers . . . but the poor need food in their bellies more than we need gold and crystal on our head. That crown has been sold."

`affc-cersei-10.md:253` / cell-objects / Cersei smashes the ewer and chamber pot in her sept cell after stripping: "She tore the shift into a hundred pieces, found a ewer of water and smashed it against the wall, then did the same with the chamber pot."

`affc-cersei-10.md:267` / food-in-cell / Cell food: "Septa Moelle brought her a bowl of some waterly grey gruel as the sun was coming up. Cersei flung it at her head. When they brought a fresh ewer of water, though, she was so thirsty that she had no choice but to drink. When they brought another shift . . . that evening when Moelle appeared again she ate the bread and fish and demanded wine to wash it down. No wine appeared"

`affc-cersei-10.md:265` / prison-humiliation / Cersei forced to squat in corner without chamber pot: "She had smashed the chamber pot, so she had to squat in a corner to make her water and watch it trickle across the floor."

### DESCRIPTION — HIGH SPARROW / SPARROWS

`affc-cersei-06.md:109` / description / Sparrows filling the plaza of Baelor's Sept: "Hundreds were encamped upon the plaza, hundreds more in the gardens. Their cookfires filled the air with smoke and stinks. Roughspun tents and miserable hovels made of mud and scrap wood besmirched the pristine white marble. They were even huddled on the steps"

`affc-cersei-06.md:167–169` / description-high-sparrow / First description of the High Sparrow: "The man's beard was grey and brown and closely trimmed, his hair tied up in a hard knot behind his head. Though his robes were clean, they were frayed and patched as well. He had rolled his sleeves up to his elbows as he scrubbed, but below the knees the cloth was soaked and sodden. His face was sharply pointed, with deep-set eyes as brown as mud. His feet are bare, she saw with dismay. They were hideous as well, hard and horny things, thick with callus."

`affc-cersei-06.md:187` / description-high-sparrow-crown / High Sparrow sold the crystal crown: "We have no crown, Your Grace." / "That crown has been sold. So have the others in our vaults, and all our rings, and our robes of cloth-of-gold and cloth-of-silver."

`affc-cersei-06.md:163` / description / Septon Raynard on his knees scrubbing: "His face was red as a beet, and there were broken blisters on his hands, bleeding." — the sparrows have put the Most Devout to cleaning floors

`affc-cersei-06.md:131–132` / description-bones / Bones piled at Baelor's statue: "The great marble statue that had smiled serenely over the plaza for a hundred years was waist-deep in a heap of bones and skulls. Some of the skulls had scraps of flesh still clinging to them. A crow sat atop one such, enjoying a dry, leathery feast. Flies were everywhere."

`affc-cersei-08.md:145` / description-sept-cell / Margaery's sept cell: "Her cell was eight feet long and six feet wide, with no furnishings but a straw-stuffed pallet and a bench for prayer, a ewer of water, a copy of The Seven-Pointed Star, and a candle to read it by. The only window was hardly wider than an arrow slit."

`affc-cersei-10.md:249–251` / description-sept-cell-cersei / Cersei's strip and cell: "Inside the cell three silent sisters held her down as a septa named Scolera stripped her bare. She even took her smallclothes." / "The queen should pray," said Septa Scolera"

### DESCRIPTION — GREAT SEPT

`affc-cersei-02.md:31` / description-great-sept / The old High Septon at Tywin's wake: "A bent old man with a wispy grey beard, he was so stooped by the weight of his ornate embroidered robes that his eyes were on a level with the queen's breasts . . . though his crown, an airy confection of cut crystal and spun gold, added a good foot and a half to his height." — old High Septon + the crystal crown (now sold)

`affc-cersei-02.md:38–42` / description-great-sept / Interior at Tywin's wake: "Under the Great Sept's lofty dome of glass and gold and crystal, Lord Tywin Lannister's body rested upon a stepped marble bier." / "seventy-seven septas gathered before the altar of the Mother and began to sing to her for mercy"

`affc-cersei-06.md:195` / description-great-sept-interior / Hall of Lamps interior: "Their footsteps echoed off the marble floor. Dust motes swam in the beams of colored light slanting down through the leaded glass of the great dome. Incense sweetened the air, and beside the seven altars candles shone like stars. A thousand twinkled for the Mother and near as many for the Maid, but you could count the Stranger's candles on two hands and still have fingers left."

### DESCRIPTION — MAGGY THE FROG (flashback)

`affc-cersei-08.md:205–212` / description-maggy / Maggy's tent interior: "The inside of the tent was full of smells. Cinnamon and nutmeg. Pepper, red and white and black. Almond milk and onions. Cloves and lemongrass and precious saffron, and stranger spices, rarer still. The only light came from an iron brazier shaped like a basilisk's head, a dim green light that made the walls of the tent look cold and dead and rotten."

`affc-cersei-08.md:211` / description-maggy / Maggy's appearance: "She was short, squat, and warty, with pebbly greenish jowls. Her teeth were gone and her dugs hung down to her knees. You could smell sickness on her if you stood too close, and when she spoke her breath was strange and strong and foul."

`affc-cersei-08.md:231` / description-maggy-blood / Blood ritual: "In the dim green tent, the blood seemed more black than red. Maggy's toothless mouth trembled at the sight of it. 'Here,' she whispered, 'give it here.' When Cersei offered her hand, she sucked away the blood with gums as soft as a newborn babe's."

### DESCRIPTION — CERSEI'S WINE / DRINK REGISTER

`affc-cersei-01.md:25` / drink / Ch.1, Cersei wakes with Tywin dead: "I drank too much last night, these fears are only humors born of wine."

`affc-cersei-02.md:227` / drink / Ch.2, Cersei alone after meeting with Qyburn: "When he was gone, Cersei poured herself a cup of strongwine and drank it by the window, watching the shadows lengthen across the yard"

`affc-cersei-02.md:233` / food / Cersei's supper with Ser Kevan: "They ate a simple supper of beets and bread and bloody beef with a flagon of Dornish red to wash it all down. Ser Kevan said little and scarce touched his wine cup."

`affc-cersei-03.md:17` / food-rejected / Wedding morning, failed breakfast: "she sent to the kitchens for two boiled eggs, a loaf of bread, and a pot of honey. But when she cracked the first egg and found a bloody half-formed chick inside, her stomach roiled. 'Take this away and bring me hot spiced wine'"

`affc-cersei-03.md:152–153` / drink / Tommen's wedding feast: "Cersei drank several cups of wine and pushed her food around a golden plate." / "The wine tastes of bile."

`affc-cersei-04.md:97–99` / drink / Small council meeting: "Do we have wine?" / "We have Dornish red and Arbor gold, and a fine sweet hippocras from Highgarden." / "The gold, I think. I find Dornish wines as sour as the Dornish."

`affc-cersei-05.md:373–374` / food-supper / Cersei's supper with Falyse and Balman: "The rest was hippocras and buttered beets, hot-baked bread, herb-crusted pike, and ribs of wild boar. Cersei had become very fond of boar since Robert's death." — notable: fond of boar after Robert was killed by one

`affc-cersei-07.md:229` / drink / After Falyse affair, Cersei alone: "When the door closed behind them Cersei poured herself another cup of wine."

`affc-cersei-09.md:121` / food-supper / Supper with Merryweathers and Blue Bard: "the kitchens proved to have no wild boar on hand . . . the cooks butchered one of the castle sows, and served them ham studded with cloves and basted with honey and dried cherries . . . Afterward they had baked apples with a sharp white cheese."

`affc-cersei-09.md:231` / drink / After the Blue Bard's torture: "My throat is raw. Be a sweet and pour me some wine." — the throat rawness echoes the valonqar's strangling hands (inadvertent echo)

`affc-cersei-10.md:265–267` / food-prison / Cell food sequence: "waterly grey gruel . . . Cersei flung it at her head" / "she was so thirsty that she had no choice but to drink" / "she ate the bread and fish and demanded wine to wash it down. No wine appeared"

`affc-cersei-03.md:225` / fire / Wildfire description: "The tower went up with a whoosh. In half a heartbeat its interior was alive with light, red, yellow, orange . . . and green, an ominous dark green, the color of bile and jade and pyromancer's piss."

`affc-cersei-03.md:225` / fire / Cersei's emotional response to wildfire: "It is beautiful, she thought, as beautiful as Joffrey, when they laid him in my arms. No man had ever made her feel as good as she had felt when he took her nipple in his mouth to nurse." — remarkable comparison

`affc-cersei-04.md:97` / drink-council / "The queen turned to her Hand. 'What were you speaking of when I arrived, Ser Harys?'" — she takes Arbor gold at the council meeting, sets the pattern for all council drinking

### DESCRIPTION — BLUE BARD

`affc-cersei-09.md:143–145` / description-blue-bard / Blue Bard's appearance in detail: "The singer's boots were supple blue calfskin, his breeches fine blue wool. The tunic he wore was pale blue silk slashed with shiny blue satin. He had even gone so far as to dye his hair blue, in the Tyroshi fashion. Long and curly, it fell to his shoulders and smelled as if it had been washed in rosewater."

`affc-cersei-09.md:149` / quote-blue-bard / His real name revealed: "'As a boy, I was called Wat. A fine name for a plowboy, less fitting for a singer.'"

`affc-cersei-09.md:173` / description-torture / Blue Bard in the black cells: "Even in the black cells, all they got from him were denials, prayers, and pleas for mercy. Before long, blood was streaming down his chin from all his broken teeth, and he wet his dark blue breeches three times over"

### DESCRIPTION — SPARROW POVERTY / FOOD IMAGERY

`affc-cersei-06.md:125` / poverty / "Some of the sparrows looked gaunt and hollow-eyed enough to eat her horses."

`affc-cersei-06.md:217` / sparrow-poverty / High Sparrow's account of the villages: "Those villages are no more, Your Grace. Weeds and thorns grow where gardens once flourished, and bones litter the roadsides." — famine/war devastation context for the sparrows

`affc-cersei-08.md:8` / description / Warrior's Sons described: "Their rainbow-striped robes of the Warrior's Sons . . . crystals adorned the pommels of their longswords and the crests of their greathelms . . . a rainbow sword shining bright upon a field of darkness"

### FORESHADOWING

`affc-cersei-01.md:173` / foreshadowing-valonqar / First AFFC instance of "valonqar" in Cersei's explicit thoughts: "It is blood I need, not water. Tyrion's blood, the blood of the valonqar. The torches spun around her. Cersei closed her eyes, and saw the dwarf grinning at her. No, she thought, no, I was almost rid of you. But his fingers had closed around her neck, and she could feel them beginning to tighten."

`affc-cersei-03.md:149` / foreshadowing-maggy / First full articulation of the "younger and more beautiful queen" prophecy in AFFC: "Queen you shall be, the old woman had promised, with her lips still wet and red and glistening, until there comes another, younger and more beautiful, to cast you down and take all that you hold dear."

`affc-cersei-06.md:87` / foreshadowing-valonqar-physical / Cersei's physical memory of the prophecy triggered by watching Tommen cough at the wedding: "a drop of red blood hissing in a candle flame, a croaking voice that spoke of crowns and shrouds, of death at the hands of the valonqar"

`affc-cersei-08.md:263` / foreshadowing-valonqar-dream / Nightmare where Tyrion strangles her: "The hands emerged from the mists of her dream and coiled around her neck; thick hands, and strong. Above them floated his face, leering down at her with his mismatched eyes . . . Before long she was making the same sound her son had made, the terrible thin sucking sound that marked Joff's last breath on earth." — echoes Joffrey's death

`affc-cersei-08.md:251` / foreshadowing / Full Maggy prophecy delivered in chapter: "Gold shall be their crowns and gold their shrouds," she said. "And when your tears have drowned you, the valonqar shall wrap his hands about your pale white throat and choke the life from you."

`affc-cersei-09.md:267` / foreshadowing / Cersei names valonqar to Taena: "Tyrion is the valonqar . . . it means little brother." — Cersei explicitly translates and assigns the word to Tyrion

`affc-cersei-09.md:231` / foreshadowing-echo / Cersei's raw throat after the torture session: "My throat is raw" — immediately after overseeing Blue Bard's strangulation/torture session; the throat-and-hands imagery accumulates

`affc-cersei-10.md:49` / foreshadowing-reversal / Cersei prematurely declares the prophecy void: "The younger queen whose coming she'd foretold was finished, and if that prophecy could fail, so could the rest. No golden shrouds, no valonqar, I am free of your croaking malice at last." — hubris line; she is captured in the next scene

---

## NOTES

**Dedup catches:**
- `maggy-the-frog` node already exists (in baseline character list). I am proposing the *prophecy-event* node separately, which is new.
- `cersei-rearms-the-faith-and-forgives-the-debt` and `cersei-plots-against-margaery` exist; no re-proposal of those.
- The `faith-militant-uprising` WARNING was heeded — the rearming under Cersei is NOT wired to that historical node.

**Considered and rejected edges:**
- `cersei-lannister --[WIELDED_IN]--> cersei-confronts-and-arrests-the-blue-bard` (the lute as a weapon): the lute is not an owned artifact with its own node, and WIELDED_IN needs an artifact node. The lute-smash is already in the arrest event's AGENT_IN edge. Skip.
- `cersei-is-stripped-and-imprisoned --[CAUSES]--> cersei-sends-raven-to-jaime`: No existing event node for this. Flag for orchestrator as a gap — the imprisoned-arc has zero outgoing edges and Cersei's plea to Jaime is the clearest downstream.
- The Gardener coin (affc-cersei-02.md:183): interesting object but does not warrant an artifact node — it is a clue/prop in Cersei's paranoia, not a load-bearing object with its own arc.

**New node the orchestrator should consider minting (not in my scope to propose fully):**
- `cersei-pleads-for-jaime` or `cersei-sends-message-to-jaime` — happens at affc-cersei-10.md:313–317; this is the direct downstream consequence of `cersei-is-stripped-and-imprisoned` (which has 0 outgoing causal edges). Quote: "Come at once. Help me. Save me. I need you now as I have never needed you before. I love you. I love you. I love you. Come at once." — would fix the dead-end.

**`maggy-the-frog-prophecy` node type:** The locked vocabulary doesn't include `event.revelation` — suggest `event.incident` or use whatever type the orchestrator determines fits prophecy-delivery events. The content is a revelation/foretelling; closest existing analogues in the graph would determine the right type.
