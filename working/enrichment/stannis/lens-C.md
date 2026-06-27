# Lens C — Descriptive / Quote / Object Depth — A2.7 Stannis proposal (S155)

## Proposed NEW nodes

### 1. `burning-of-the-seven-at-dragonstone` (event.ritual)
The burning of the seven statues of the Seven at Dragonstone's gates, conducted by Melisandre while Stannis pulled a sword from the fire and the queen's men proclaimed it "Lightbringer." Septon Barre and the Rambton family resisted and were imprisoned; Guncer Sunglass withdrew his support. This is the public conversion ceremony, the founding act of Stannis's R'hllor devotion, and the context in which Lightbringer was first "drawn."
Anchor quote: "The morning air was dark with the smoke of burning gods." (acok-davos-01:12)

### 2. `leeching-of-edric-storm` (event.ritual)
Melisandre draining three leeches fat with Edric Storm's blood into a brazier, while Stannis named the three "usurper" kings into the flames. A TEXT EVENT the graph lacks entirely. The king's-blood-magic reading is gated (theory-only); the ritual action itself is canon.
Anchor quote: "I saw you burn some leeches." (asos-davos-05:89)

---

## Proposed NEW edges

| source_slug | EDGE_TYPE | target_slug | Tier | qualifier/evidence | one-line rationale |
|---|---|---|---|---|---|
| `stannis-baratheon` | `WIELDS` | `lightbringer` | Tier 1 | — | Stannis pulls the sword from the burning pyre: "He went straight to the Mother, grasped the sword with his gloved hand, and wrenched it free of the burning wood with a single hard jerk." (acok-davos-01:45) |
| `lightbringer` | `WIELDED_IN` | `burning-of-the-seven-at-dragonstone` | Tier 1 | — | The sword is drawn from the fire at this ritual: "jade-green flames swirling around cherry-red steel" (acok-davos-01:45) |
| `melisandre` | `AGENT_IN` | `burning-of-the-seven-at-dragonstone` | Tier 1 | — | Melisandre leads the ceremony: "The red woman walked round the fire three times, praying once in the speech of Asshai, once in High Valyrian, and once in the Common Tongue." (acok-davos-01:21) |
| `stannis-baratheon` | `PARTICIPATES_IN` | `burning-of-the-seven-at-dragonstone` | Tier 1 | — | Stannis draws the sword from the fire before the assembled host; is present and active: "Stannis Baratheon strode forward like a soldier marching into battle." (acok-davos-01:43) |
| `stannis-baratheon` | `WORSHIPS` | `rhllor` | Tier 1 | — | The burning of the Seven is his public conversion act; Davos explicitly names this as Stannis's new god: "I know little and care less of gods, but the red priestess has power. … It is time I tried another hawk, Davos. A red hawk." (acok-davos-01:257–263) |
| `melisandre` | `ADVISES` | `stannis-baratheon` | Tier 1 | — | Mel counsels Stannis throughout; Stannis explicitly says he will "hear hers" (her counsel) instead of Cressen's: "I have heard your counsel, Cressen. Now I will hear hers." (acok-prologue:257) |
| `selyse-baratheon` | `AGENT_IN` | `burning-of-the-seven-at-dragonstone` | Tier 1 | — | Selyse echoes Mel's prayers and is present and participatory: "Queen Selyse echoed the words." (acok-davos-01:21) |
| `melisandre` | `AGENT_IN` | `leeching-of-edric-storm` | Tier 1 | — | Melisandre conducts the ritual: "Give me the boy for R'hllor … and the ancient prophecy shall be fulfilled." (asos-davos-05:61); the leeching is her act (asos-davos-05:87–91) |
| `edric-storm` | `VICTIM_IN` | `leeching-of-edric-storm` | Tier 1 | — | Edric is the blood source; Davos: "I saw you burn some leeches." / "You have seen what even a little of that blood could do—" (asos-davos-05:89–91) |
| `stannis-baratheon` | `PARTICIPATES_IN` | `leeching-of-edric-storm` | Tier 2 | — | Stannis names the three kings into the fire as Mel throws the leeches: "the usurper Joffrey / the usurper Balon / the usurper Robb" — the ritual requires his royal voice; implied by Davos's witness account (asos-davos-05:87–99) **[BORDERLINE: Stannis's exact role at the moment of burning is narrated by Davos in summary — he isn't on the page watching it happen; Tier 2 warranted]** |
| `davos-seaworth` | `WITNESS_IN` | `leeching-of-edric-storm` | Tier 1 | — | Davos is present and directly references witnessing the leeching: "I saw you burn some leeches." (asos-davos-05:89) |
| `cressen` | `VICTIM_IN` | `burning-of-the-seven-at-dragonstone` | Tier 2 | — | Cressen attempts to poison Mel during the feast that follows/is concurrent with the burning; he dies as a direct result of the ritual context **[BORDERLINE — the feast is distinct from the burning ceremony itself; the banner event is cressen-tries-to-poison-melisandre which is presumably its own node; drop if that node already exists]** |

---

## Quotes to attach

These are verbatim single-line quotes suitable for the `## Quotes` sections of existing nodes.

### → `stannis-baratheon`
1. "Hard was the word men used when they spoke of Stannis, and hard he was." (acok-prologue:169) — physical/character description
2. "His mouth would have given despair to even the drollest of fools; it was a mouth made for frowns and scowls and sharply worded commands, all thin pale lips and clenched muscles, a mouth that had forgotten how to smile and had never known how to laugh." (acok-prologue:169)
3. "Sometimes when the world grew very still and silent of a night, Maester Cressen fancied he could hear Lord Stannis grinding his teeth half a castle away." (acok-prologue:169)
4. "A tight-laced leather jerkin and breeches of roughspun brown wool." (acok-prologue:167) — characteristic plain dress
5. "I know little and care less of gods, but the red priestess has power." (acok-davos-01:257)
6. "I stopped believing in gods the day I saw the Windproud break up across the bay." (acok-davos-01:253)
7. "How can I lose something I have never owned?" (acok-davos-01:253) — on being unloved
8. "For a moment it seemed as though the king had not heard. Stannis showed no pleasure at the news, no anger, no disbelief, not even relief. He stared at his Painted Table with teeth clenched hard." (asos-davos-05:11) — characteristic reaction to Robb Stark's death news
9. "I dream of it sometimes. Of Renly's dying. A green tent, candles, a woman screaming. And blood." (acok-davos-02:189)
10. "I was still abed when he died … I was in my tent when Renly died, and when I woke my hands were clean." (acok-davos-02:189)
11. "Renly offered me a peach. At our parley … When he spoke of how sweet the peach was, did his words have some hidden meaning? … I will go to my grave thinking of my brother's peach." (acok-davos-02:193)
12. "I did love him, Davos. I know that now." (acok-davos-02:193) — on Renly
13. "Melisandre swears that she has seen me in her flames, facing the dark with Lightbringer raised on high. Lightbringer! It glimmers prettily, I'll grant you, but on the Blackwater this magic sword served me no better than any common steel." (asos-davos-05:147)
14. "We do not choose our destinies. Yet we must … we must do our duty, no? Great or small, we must do our duty." (asos-davos-05:147)

### → `melisandre`
1. "As ever, she wore red head to heel, a long loose gown of flowing silk as bright as fire, with dagged sleeves and deep slashes in the bodice that showed glimpses of a darker bloodred fabric beneath. Around her throat was a red gold choker tighter than any maester's chain, ornamented with a single great ruby." (acok-prologue:295) — fullest single-line description
2. "She was not beautiful. She was red, and terrible, and red." (acok-prologue:295)
3. "Her eyes were hot coals, and the sweat that dappled her skin seemed to glow with a light of its own. Melisandre shone." (acok-davos-02:351) — shadow-birth scene, her transformation
4. "Melisandre of Asshai, sorceress, shadowbinder, and priestess to R'hllor, the Lord of Light, the Heart of Fire, the God of Flame and Shadow." (acok-prologue:265)
5. "It was never truly dark in Melisandre's chambers." (adwd-melisandre-01:11) — opening line, her fire ritual
6. "Some nights she drowsed, but never for more than an hour … She feared to dream. Sleep is a little death, dreams the whisperings of the Other, who would drag us all into his eternal night." (adwd-melisandre-01:57)
7. "She was stronger at the Wall, stronger even than in Asshai." (adwd-melisandre-01:79)
8. "Blood trickled down her thigh, black and smoking. The fire was inside her, an agony, an ecstasy, filling her, searing her, transforming her." (adwd-melisandre-01:23) — vision-gazing cost
9. "R'hllor provided her with all the nourishment her body needed, but that was something best concealed from mortal men." (adwd-melisandre-01:65)

### → `davos-seaworth`
1. "Davos was a slight man, his low birth written plain upon a common face." (acok-prologue:127)
2. "It is not for us to question him. We sail his ships and do his bidding. That is all." (acok-davos-01:79)
3. "I am a man. I am kind to my wife, but I have known other women … I never felt evil until tonight. I would say my parts are mixed, m'lady. Good and bad." (acok-davos-02:293)
4. "I serve King Stannis. Gods be good, I serve King Stannis." (asos-davos-01:79)
5. "The last time it was life I brought to Storm's End, shaped to look like onions. This time it is death, in the shape of Melisandre of Asshai." (acok-davos-02:279) — marquee quote on the shadow-birth night

### → `dragonstone`
1. "Grim places needed lightening, not solemnity, and Dragonstone was grim beyond a doubt, a lonely citadel in the wet waste surrounded by storm and salt, with the smoking shadow of the mountain at its back." (acok-prologue:37)
2. "The kitchens were a dragon curled up in a ball, with the smoke and steam of the ovens vented through its nostrils. The towers were dragons hunched above the walls or poised for flight … Dragon claws emerged from walls to grasp at torches, great stone wings enfolded the smith and armory, and tails formed arches, bridges, and exterior stairs." (asos-davos-05:162)
3. "In the center of the chamber was the great table from which it took its name, a massive slab of carved wood fashioned at the command of Aegon Targaryen in the days before the Conquest." (acok-prologue:165) — the Painted Table (for dragonstone node OR painted-table node)
4. "The gargoyles and stone dragons on the castle walls seemed blurred, as if Davos were seeing them through a veil of tears. Or as if the beasts were trembling, stirring …" (acok-davos-01:14) — the burning-gods light effect on the stone dragons

### → `lightbringer`
1. "In ancient books of Asshai it is written that there will come a day after a long summer when the stars bleed and the cold breath of darkness falls heavy on the world. In this dread hour a warrior shall draw from the fire a burning sword. And that sword shall be Lightbringer, the Red Sword of Heroes, and he who clasps it shall be Azor Ahai come again, and the darkness shall flee before him." (acok-davos-01:41) — Melisandre's proclamation at the burning
2. "jade-green flames swirling around cherry-red steel" (acok-davos-01:45) — description of the sword drawn from the fire
3. "That sword was not Lightbringer, my friend." (acok-davos-01:125) — Salladhor Saan's verdict; the false Lightbringer declaration
4. "The Red Sword of Heroes looks a proper mess, thought Davos." (acok-davos-01:59) — Davos's private observation after the ceremony
5. "Lightbringer! It glimmers prettily, I'll grant you, but on the Blackwater this magic sword served me no better than any common steel." (asos-davos-05:147) — Stannis himself dismissing it

### → `melisandres-ruby` (the choker ruby)
1. "Around her throat was a red gold choker tighter than any maester's chain, ornamented with a single great ruby." (acok-prologue:295)
2. "The ruby at Melisandre's throat caught the light as she turned her head, and for an instant it seemed to glow bright as the comet." (acok-prologue:351)
3. "The ruby at Melisandre's throat shone redly." (asos-davos-05:23) — the ruby's consistent presence as a motif
4. "Melisandre felt the warmth in the hollow of her throat as her ruby stirred at the closeness of its slave." (adwd-melisandre-01:87) — confirms the ruby as a tool of the glamor over the Lord of Bones
5. "When the flames had licked at Rattleshirt, the ruby at her throat had grown so hot that she had feared her own flesh might start to smoke and blacken." (adwd-melisandre-01:269) — the cost of the glamor to Mel

### → `patchface`
1. "He was soft and obese, subject to twitches and trembles, incoherent as often as not." (acok-prologue:41)
2. "The shadows come to dance, my lord, dance my lord, dance my lord … The shadows come to stay, my lord, stay my lord, stay my lord." (acok-prologue:79) — the prophetic song, first instance (and acok-prologue:95 repeats it)
3. "Under the sea, smoke rises in bubbles, and flames burn green and blue and black." (acok-davos-01:43) — sung during the burning of the Seven

### → `storms-end` (the cave/shadow-birth context)
1. "There are spells woven into the stones. Dark walls that no shadow can pass—ancient, forgotten, yet still in place." (acok-davos-02:332) — Mel explaining why she had to enter physically
2. "The seaward side of Storm's End perched upon a pale white cliff, the chalky stone sloping up steeply to half again the height of the massive curtain wall." (acok-davos-02:337)

---

## Dropped / considered-but-rejected

1. **`lightbringer MADE_OF [material]`** — Text describes the sword as "cherry-red steel" (acok-davos-01:45) and "burnt and blackened" (acok-davos-01:59) after the ceremony. No material other than steel is named; MADE_OF steel is trivial and not graph-worthy. Dropped.

2. **`patchface FORESHADOWS shadow-assassination-of-renly`** — "The shadows come to dance/stay" clearly resonates with the shadow-baby killings (especially as it's sung repeatedly during shadow-related scenes). However, FORESHADOWS is a theory-adjacent edge for Patchface songs — his prophetic capacity is not explicitly confirmed in these chapters (Cressen dismisses it). Node-prose only; dropped per hard rules on theory-gated edges.

3. **`patchface OWNS [costume / helm]`** — Not edge-worthy; costume detail, not a named artifact node.

4. **`dragonstone BUILT_BY [valyrians]`** — Architecture detail in acok-prologue:47 and asos-davos-05:162. The Valyrians are a culture node, not obviously needing a new edge here; the detail belongs in node prose. Dropped.

5. **Cressen as VICTIM_IN burning-of-the-seven** — The burning and Cressen's poisoning attempt/death happen at the same feast. But Cressen's death is a separate event (there is likely a `cressen-death` or `cressen-poison-attempt` event node). I dropped the edge above as borderline — if the existing node is `cressen-death` or similar, it would supersede this. Flag for synthesis.

6. **`selyse-baratheon WORSHIPS rhllor`** — Already confirmed to exist in baseline: "selyse WORSHIPS rhllor" is in the wired web (baseline.md:47). Dropped as duplicate.

7. **`lightbringer REPUTED_AS [false lightbringer]`** — REPUTED_AS is a valid type but takes a target slug (an entity), not a qualifier phrase. There is no `false-lightbringer` node. The "not Lightbringer" descriptor belongs in node prose. Dropped; the quotes section above serves this purpose.

8. **Mance-glamour / Rattleshirt edges from adwd-melisandre-01** — adwd-melisandre-01 confirmed the glamor thread is active (S145 owns it). I read it for descriptive depth only (nightfires, ruby-cost, Mel's age/power) and extracted only quotes and harvest pointers. No edges proposed touching the Mance/Rattleshirt thread per hard rules.

9. **`melisandre PRACTICES shadowbinding`** — Cressen calls her "shadowbinder" (acok-prologue:265) and the text confirms she births a shadow. PRACTICES is in vocab. However, `shadowbinding` may not exist as a node. Dropped pending node existence; if `shadowbinding` or `shadow-magic` is an existing `concept.magic` node, this edge is Tier 1 (acok-prologue:265 + acok-davos-02:333–335). Flag for synthesis.

10. **`stannis-baratheon REPUTED_AS [azor-ahai-reborn]`** — Mel explicitly calls him "Azor Ahai reborn" (adwd-melisandre-01:15) but the Azor-Ahai reading is explicitly THEORY-GATED. The text-event is Mel's proclamation; the prophecy assertion is gated. Node-prose + harvest pointer only.

11. **`davos-seaworth RESCUES edric-storm`** — This is a Gap item (baseline.md:89) and was on Lens C's radar. Text in asos-davos-05 shows Davos working to protect Edric but the actual rescue/smuggling-away happens in asos-davos-06, outside my assigned chapters. I cannot confirm with a verbatim quote from my chapters. Left for another lens or synthesis to confirm with asos-davos-06 text.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|------|------|
| food/feast | ACOK | acok-prologue:287 | Stannis's bannermen feast in the Great Hall; "tearing apart loaves of black bread to soak in their fish stew" — black bread and fish stew, the Dragonstone feast |
| food/drink | ACOK | acok-davos-01:91 | Salladhor Saan eating grapes from a wooden bowl at the inn; "marvelously sweet" grapes; Davos orders ale |
| food/dinner | ACOK | acok-davos-01:147 | Salladhor's dinner on the Valyrian: "Minced lamb with pepper and roasted gull stuffed with mushrooms and fennel and onion" — vivid Lyseni feast description |
| food/drink | ACOK | acok-davos-01:149 | Thoros of Myr's flaming sword: red robes, "pale green flames" on the blade — flavored as a food-adjacent pyromancer detail |
| food/foraging | ASOS | asos-davos-01:19 | Davos on the rock eating tiny crabs: "smashed them apart on the rocks to suck the meat from their claws" — grim survival eating |
| hospitality | ACOK | acok-davos-01:95 | Davos patting the eroded gargoyle outside the inn and murmuring "Luck" — repeated good-luck ritual |
| food/starvation | ACOK | acok-prologue:155 | Storm's End siege backstory: garrison "was down to roots and rats" before Davos's onions arrived |
| food/onions | ACOK | acok-prologue:155 | Davos's black-sailed ship with "a hold crammed with onions and salt fish" breaking the Redwyne blockade — the origin of the Onion Knight name |
| physical description | ACOK | acok-prologue:169 | Stannis's full physical description: "broad of shoulder and sinewy of limb … only a fringe of thin black hair … his whiskers cropped tight and short … eyes were open wounds beneath his heavy brows, a blue as dark as the sea by night" — best single passage |
| physical description | ACOK | acok-prologue:295 | Melisandre's fullest physical description in one passage: red gown, dagged sleeves, bloodred fabric beneath, red gold choker, single great ruby, "deep burnished copper" hair, red eyes, "smooth and white, unblemished, pale as cream" skin |
| descriptive/architecture | ACOK | acok-prologue:37 | Dragonstone called "a lonely citadel in the wet waste surrounded by storm and salt, with the smoking shadow of the mountain at its back" |
| descriptive/architecture | ACOK | acok-prologue:115 | Chamber of the Painted Table reached via Stone Drum: "across the gallery, past through the middle and inner walls with their guardian gargoyles and black iron gates" — spatial layout of Dragonstone |
| descriptive/architecture | ACOK | acok-prologue:165 | Painted Table description: "more than fifty feet long, perhaps half that wide at its widest point … shaped after the land of Westeros … darkened by near three hundred years of varnish" |
| descriptive/artifact | ACOK | acok-davos-01:45 | Lightbringer drawn from the fire: "jade-green flames swirling around cherry-red steel"; "The Red Sword of Heroes looks a proper mess" (line 59) — vivid; suitable for lightbringer node prose |
| descriptive/artifact | ACOK | acok-davos-01:125 | Salladhor: "That sword was not Lightbringer, my friend" — the false-Lightbringer declaration; also the full Nissa-Nissa legend (lines 133–139) for lightbringer node |
| foreshadowing | ACOK | acok-prologue:79 | Patchface's "shadows come to dance/stay" song — direct foreshadowing of shadow-baby births; sung again at the burning ceremony (acok-davos-01:43) |
| descriptive/object | ACOK | acok-davos-02:351 | Mel's shadow-birth: "Melisandre shone" — she is naked, huge with child, blood runs down her thighs "black as ink," eyes are "hot coals," sweat seems to glow |
| descriptive/object | ACOK | acok-davos-02:353 | The shadow itself: "Two arms wriggled free, grasping, black fingers coiling around Melisandre's straining thighs … the whole of the shadow slid out into the world and rose taller than Davos, tall as the tunnel, towering above the boat" |
| descriptive/object | ADWD | adwd-melisandre-01:77 | Mel's powder chest: "powders to turn fire green or blue or silver … a smoke for truth, a smoke for lust, a smoke for fear, and the thick black smoke that could kill a man outright" — her toolkit |
| descriptive/visions | ADWD | adwd-melisandre-01:17 | Mel's vision: "towers by the sea, crumbling as the dark tide came sweeping over them, rising from the depths" — confirms the Eastwatch vision |
| descriptive/visions | ADWD | adwd-melisandre-01:21 | "A face took shape within the hearth … A wooden face, corpse white. Was this the enemy?" — the wooden/weirwood face vision (Bloodraven? the enemy?) |
| descriptive/age-glamour | ADWD | adwd-melisandre-01:23 | "Blood trickled down her thigh, black and smoking. The fire was inside her, an agony, an ecstasy, filling her, searing her, transforming her" — vision-gazing's physical cost on Mel |
| descriptive/age-glamour | ADWD | adwd-melisandre-01:57 | Mel fears sleep: "Sleep is a little death, dreams the whisperings of the Other" — her age/existential fear of sleep; "Melony … Lot Seven" fragments |
| descriptive/nightfires | ADWD | adwd-melisandre-01:11 | Mel's fire protocol: "three tallow candles burned upon her windowsill … Four more flickered beside her bed … In the hearth a fire was kept burning day and night" — nightfires as constant domestic practice |
| descriptive/ruby-cost | ADWD | adwd-melisandre-01:87 | "Melisandre felt the warmth in the hollow of her throat as her ruby stirred at the closeness of its slave" — ruby as glamor-anchor over the Lord of Bones; pulsing with each step |
| descriptive/ruby-cost | ADWD | adwd-melisandre-01:269 | "When the flames had licked at Rattleshirt, the ruby at her throat had grown so hot that she had feared her own flesh might start to smoke and blacken" — the toll of the glamor on Mel |
| hospitality | ADWD | adwd-melisandre-01:63–65 | Devan brings Mel breakfast: "nettle tea, a boiled egg, and bread with butter. Fresh bread, if you please, not fried." Then Mel forgets to eat it; the wildling eats it instead — grim hospitality irony |
| food/wildling | ADWD | adwd-melisandre-01:228 | Mance/Lord of Bones eating Mel's breakfast: "spreading butter on a ragged chunk of warm brown bread with his dagger" while Jon Snow refuses to "break bread" with him |
