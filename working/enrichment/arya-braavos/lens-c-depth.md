# Lens C — Descriptive / Quote / Object Depth + Harvest Bar
## Unit: Arya Stark's Braavos / House of Black and White arc
## Date: 2026-06-26

Source chapters read:
- `asos-arya-13` (ASOS ch. 75)
- `affc-arya-01` (AFFC ch. 7)
- `affc-arya-02` (AFFC ch. 23)
- `affc-cat-of-the-canals-01` (AFFC ch. 35)
- `adwd-the-blind-girl-01` (ADWD ch. 46)
- `adwd-the-ugly-little-girl-01` (ADWD ch. 65)

---

## NEW NODES

### 1. `iron-coin`
- **Type:** object.artifact
- **Slug:** iron-coin
- **Aliases:** ["the iron coin", "coin of the Faceless Men"]
- **Confidence:** Tier 1
- **Rationale:** The coin is explicitly named "the small black iron coin that Jaqen H'ghar had given her" (asos-arya-13:255). It is not a generic coin — it is a specific named artifact that activates the Faceless Men's valar morghulis response (it functions as a letter of passage / identity token). It is load-bearing across four chapters. Does NOT exist in the graph.

### 2. `finger-knife`
- **Type:** object.artifact
- **Slug:** finger-knife
- **Aliases:** ["finger knife"]
- **Confidence:** Tier 1
- **Rationale:** Named weapon Cat of the Canals uses for self-defense and (later) for killing the insurance broker in ADWD. Red Roggo teaches her to hide it up her sleeve and use it as a concealed slashing tool (affc-cat-of-the-canals-01:65). It is the instrument of her first assassination. Distinct from any other dagger in the graph. Load-bearing and navigable. Does NOT exist in the graph.

### 3. `myrish-mirror`
- **Type:** object.artifact
- **Slug:** myrish-mirror
- **Aliases:** ["Myrish mirror"]
- **Confidence:** Tier 1
- **Rationale:** Specifically named object ("You will find a Myrish mirror in the vaults", affc-arya-02:291). Arya uses it daily for an hour training facial control — it is a key tool in her identity-dissolution arc. Navigable and load-bearing to the face-practice training step. Does NOT exist in the graph.

---

## EDGES

### A. IRON COIN — origin and use

**E-01**
`(jaqen-hghar, GIFTED_TO, iron-coin)` — wait, edge direction should be GIFTED_TO the recipient:
`(jaqen-hghar, GIFTED_TO, arya-stark)` already captures the relationship, but the OBJECT is not wired.

Correction — the correct new edge with the object as target:
`(iron-coin, GIFTED_TO, arya-stark)` — NEEDS_VOCAB: GIFTED_TO is subject→recipient not artifact→recipient. Use:
`(jaqen-hghar, GIFTED_TO, arya-stark)` — but this does not wire the coin node.

The locked vocab has no GIVEN_TO or CARRIED_BY. Propose:
- `(arya-stark, OWNS, iron-coin)` — Tier 1 | asos-arya-13:255 | "the small black iron coin that Jaqen H'ghar had given her" — arya possesses it through the departure from Westeros and into Braavos
- NEEDS_VOCAB: `jaqen-hghar GIFTED_TO iron-coin` — locked vocab GIFTED_TO takes artifact as subject, not giver. The node-to-node gift chain (who gave what to whom) can't be expressed precisely without a GAVE or SOURCE_OF edge. Flag: **NEEDS_VOCAB: SOURCE_OF** or accept that `(jaqen-hghar, GIFTED_TO, arya-stark)` plus `(arya-stark, OWNS, iron-coin)` covers the intent adequately.

**E-02**
`(arya-stark, WIELDS, iron-coin)` | Tier 1 | asos-arya-13:259 | "Arya crossed her arms against her chest. 'Valar morghulis,' she said, as loud as if she'd known what it meant."
Rationale: She uses the coin as an active instrument of passage — holding it up, presenting it to Ternesio Terys. "Wields" covers this functional use of an artifact.

**E-03**
`(iron-coin, WIELDED_IN, event-arya-departs-westeros)` — NEEDS_VOCAB: this event node does not exist. Propose event mint separately or note as harvest. The coin's use at Saltpans is the precipitating event of the entire Braavos arc.
**Flag: NEEDS_VOCAB — event node `event-arya-departs-westeros` does not exist; the coin-use event needs minting before this edge can be written.**

**E-04**
`(arya-stark, WIELDS, iron-coin)` at HoBaW arrival — second use:
`(iron-coin, WIELDED_IN, event-arya-arrives-hobaw)` — same issue, event node does not exist yet.
**Flag: same as E-03.**

### B. NEEDLE — event-wiring and identity-retention

**E-05**
`(arya-stark, WIELDS, needle)` — **DEDUPED** (exists per task brief, skip)

**E-06**
`(arya-stark, OWNS, needle)` — **DEDUPED** (exists per task brief, skip)

**E-07 — new outbound from needle**
`(needle, WIELDED_IN, event-arya-retrieves-needle-crossroads)` — event = the inn at the crossroads fight in ASOS ch.75 where she kills the pimply squire with Needle and retrieves it from Polliver.
| Tier 1 | asos-arya-13:153 | "Needle slipped between his ribs and gave it to him."
Rationale: First wiring of needle to an event node. Needle's outbound is confirmed empty. The retrieval and use is the last time Needle is openly wielded before being hidden.
**Flag: event node `event-inn-at-the-crossroads` or similar — does it exist? Propose wiring; event-mint separate.**

**E-08 — the hiding event (identity-retention anchor)**
`(needle, WIELDED_IN, event-arya-hides-needle-hobaw-steps)` — this event = Arya hiding Needle in the crack on the HoBaW stairs after divesting all other possessions.
| Tier 1 | affc-arya-02:167 | "'You'll be safe here,' she told Needle. 'No one will know where you are but me.' She pushed the sword and sheath behind the step, then shoved the stone back into place, so it looked like all the other stones."
Rationale: This is the constitutive identity moment — she surrenders EVERYTHING except Needle. The event is the sharpest instantiation of needle-as-identity. Event node likely does not exist; flag for mint.
**Flag: event node `event-arya-hides-needle` needed.**

**E-09 — needle PARALLELS arya's Stark identity**
`(needle, PARALLELS, arya-stark)` — NEEDS_VOCAB: PARALLELS links two entities but here the parallel is between the object and the character it embodies. More precisely this is a thematic link that the prose makes explicit.
| Tier 1 | affc-arya-02:161 | "Needle was Robb and Bran and Rickon, her mother and her father, even Sansa. Needle was Winterfell's grey walls, and the laughter of its people."
Rationale: The text explicitly makes needle a synecdoche for Arya's identity and family. PARALLELS is the closest vocab match; it is the strongest thematic edge in the arc.

### C. PLACE wiring — titan-of-braavos and braavos

**E-10**
`(titan-of-braavos, LOCATED_AT, braavos)` | Tier 1 | affc-arya-01:53 | "His legs bestrode the gap, one foot planted on each mountain, his shoulders looming tall above the jagged crests."
Rationale: Titan is the entrance gate to Braavos; LOCATED_AT is the correct structural edge. Currently 0 outbound edges on titan-of-braavos.

**E-11**
`(titan-of-braavos, REGION_OF, braavos)` | Tier 2 | wiki-node + affc-arya-01:53
Rationale: The Titan is a landmark that defines the Braavos approach channel. REGION_OF captures containment / territorial relation. (Either E-10 or E-11 — propose both, one may be redundant; Matt decides which fits the schema better.)

**E-12**
`(arya-stark, TRAVELS_TO, braavos)` | Tier 1 | affc-arya-01:21 | "Braavos might not be so bad."
Rationale: Arya arrives in Braavos at the start of AFFC ch.7. No TRAVELS_TO edge currently links arya-stark → braavos.

**E-13**
`(arya-stark, LOCATED_AT, house-of-black-and-white)` | Tier 1 | affc-arya-01:155 | "This is the House of Black and White, my child."
Rationale: HoBaW is her primary location for the arc's duration. No LOCATED_AT edge currently links arya → HoBaW.

**E-14**
`(arya-stark, WITNESS_IN, titan-of-braavos)` — NEEDS_VOCAB: WITNESS_IN takes an event as the third term, not a place. The correct form would be WITNESS_IN an event that takes place at the titan. Since the "passing beneath the Titan" moment is an event, not a location:
Flag: **NEEDS_VOCAB — no edge type captures "character witnesses / passes through a place." LOCATED_AT covers it indirectly. Alternatively: propose event node `event-arya-passes-titan` and wire `(arya-stark, WITNESS_IN, event-arya-passes-titan)` + `(event-arya-passes-titan, LOCATED_AT, titan-of-braavos)`.** Withhold for now; raise to Matt.

**E-15**
`(house-of-black-and-white, LOCATED_AT, braavos)` | Tier 1 | affc-arya-01:111 | "On their left appeared a rocky knoll with a windowless temple of dark grey stone at its top."
Rationale: HoBaW has no LOCATED_AT edge to braavos. The node is in `graph/nodes/houses/` which is unusual for a place; note the type may need review.

### D. FINGER KNIFE wiring

**E-16**
`(arya-stark, OWNS, finger-knife)` | Tier 1 | affc-cat-of-the-canals-01:65 | "Once in a great while that would make somebody angry, but when it did she had her finger knife."

**E-17**
`(finger-knife, GIFTED_TO, arya-stark)` — NEEDS_VOCAB: same issue as iron-coin. The knowledge that Red Roggo taught her to use it (not gift it) means this is more an instruction edge. Use:
`(arya-stark, WIELDS, finger-knife)` | Tier 1 | affc-cat-of-the-canals-01:65 | "She kept it very sharp, and knew how to use it too."

**E-18**
`(finger-knife, WIELDED_IN, event-arya-kills-insurance-merchant)` — event = the assassination of the insurance broker at the Purple Harbor in ADWD ch.65 (the ugly little girl chapter).
| Tier 1 | adwd-the-ugly-little-girl-01:247 | "Her blade flashed out, smooth and quick, one deep slash through the velvet and he never felt a thing."
Rationale: The finger knife is the instrument of her first official FM assassination (the coin-switch-into-purse trick). Flag: event node needed.

### E. MYRISH MIRROR wiring

**E-19**
`(arya-stark, OWNS, myrish-mirror)` | Tier 1 | affc-arya-02:297 | "She found the Myrish mirror the next day, and every morn and every night she sat before it with a candle on each side of her, making faces."

**E-20**
`(arya-stark, WIELDS, myrish-mirror)` — NEEDS_VOCAB: WIELDS is for weapons. The mirror is a training tool. No suitable edge type covers "uses a tool." Flag: **NEEDS_VOCAB: USES or TRAINS_WITH.** Withhold; capture via OWNS + quote.

---

## QUOTE ATTACHMENTS

These go to the `## Quotes` section of the indicated node.

### titan-of-braavos node

**Q-1** — Full physical description (best single-passage description in the corpus):
> Node: `titan-of-braavos`
> Source: affc-arya-01:53
> Quote: "His legs bestrode the gap, one foot planted on each mountain, his shoulders looming tall above the jagged crests. His legs were carved of solid stone, the same black granite as the sea monts on which he stood, though around his hips he wore an armored skirt of greenish bronze. His breastplate was bronze as well, and his head in his crested halfhelm. His blowing hair was made of hempen ropes dyed green, and huge fires burned in the caves that were his eyes. One hand rested atop the ridge to his left, bronze fingers coiled about a knob of stone; the other thrust up into the air, clasping the hilt of a broken sword."

**Q-2** — The roar (already partially in wiki node; book-citation upgrade):
> Node: `titan-of-braavos`
> Source: affc-arya-01:57–59
> Quote: "Then the Titan gave a mighty roar. The sound was as huge as he was, a terrible groaning and grinding, so loud it drowned out even the captain's voice and the crash of the waves against those pine-clad ridges. A thousand seabirds took to the air at once."

**Q-3** — Arya's scale reckoning:
> Node: `titan-of-braavos`
> Source: affc-arya-01:55
> Quote: "Her neck craned upward. Baelor the Blessed would not reach his knee. He could step right over the walls of Winterfell."

### house-of-black-and-white node

**Q-4** — The weirwood-and-ebony doors (most iconic visual in the arc):
> Node: `house-of-black-and-white`
> Source: affc-arya-01:123
> Quote: "At the top she found a set of carved wooden doors twelve feet high. The left-hand door was made of weirwood pale as bone, the right of gleaming ebony. In their center was a carved moon face; ebony on the weirwood side, weirwood on the ebony. The look of it reminded her somehow of the heart tree in the godswood at Winterfell. The doors are watching me, she thought."

**Q-5** — Interior: statues, black pool, candle-smell:
> Node: `house-of-black-and-white`
> Source: affc-arya-01:131–133
> Quote: "The temple seemed much larger within than it had without. [...] Statues of them stood along the walls, massive and threatening. Around their feet red candles flickered, as dim as distant stars. [...] She could smell the candles. The scent was unfamiliar, and she put it down to some queer incense, but as she got deeper into the temple, they seemed to smell of snow and pine needles and hot stew."

**Q-6** — The black pool:
> Node: `house-of-black-and-white`
> Source: affc-arya-01:135
> Quote: "In the center of the temple she found the water she had heard; a pool ten feet across, black as ink and lit by dim red candles."

**Q-7** — Candle-smell evokes Winterfell (interior sensory detail; strongest affective quote in arc):
> Node: `house-of-black-and-white`
> Source: affc-arya-02:73
> Quote: "Winterfell, she might have said. I smell snow and smoke and pine needles. I smell the stables. I smell Hodor laughing, and Jon and Robb battling in the yard, and Sansa singing about some stupid lady fair. I smell the crypts where the stone kings sit, I smell hot bread baking, I smell the godswood. I smell my wolf, I smell her fur, almost as if she were still beside me."

### kindly-man node

**Q-8** — The skull-face reveal (kindly man's signature moment):
> Node: `kindly-man`
> Source: affc-arya-01:195
> Quote: "The priest lowered his cowl. Beneath he had no face; only a yellowed skull with a few scraps of skin still clinging to the cheeks, and a white worm wriggling from one empty eye socket. 'Kiss me, child,' he croaked, in a voice as dry and husky as a death rattle."

**Q-9** — The kindliest old man (the reveal's resolution):
> Node: `kindly-man`
> Source: affc-arya-01:199
> Quote: "The yellow skull was melting too, and the kindliest old man that she had ever seen was smiling down at her. 'No one has ever tried to eat my worm before,' he said. 'Are you hungry, child?'"

### needle node

**Q-10** — The identity monologue (already partially in needle node wiki-quotes, but this is the verbatim book text with chapter:line — upgrades to Tier 1 book provenance):
> Node: `needle`
> Source: affc-arya-02:161
> Quote: "Needle was Robb and Bran and Rickon, her mother and her father, even Sansa. Needle was Winterfell's grey walls, and the laughter of its people. Needle was the summer snows, Old Nan's stories, the heart tree with its red leaves and scary face, the warm earthy smell of the glass gardens, the sound of the north wind rattling the shutters of her room. Needle was Jon Snow's smile."
> Note: Already appears in `needle.node.md ## Quotes` from wiki-source (tier-2 non-navigable). This is the verbatim book text; attach as Tier 1 cite with `affc-arya-02:161`.

**Q-11** — The hiding:
> Node: `needle`
> Source: affc-arya-02:167
> Quote: "'You'll be safe here,' she told Needle. 'No one will know where you are but me.' She pushed the sword and sheath behind the step, then shoved the stone back into place, so it looked like all the other stones. As she climbed back to the temple, she counted steps, so she would know where to find the sword again. One day she might have need of it. 'One day,' she whispered to herself."

**Q-12** — The gods-wanted-it moment (Needle's theological weight):
> Node: `needle`
> Source: affc-arya-02:163
> Quote: "The gods wanted me to have it. Not the Seven, nor Him of Many Faces, but her father's gods, the old gods of the north. The Many-Faced God can have the rest, she thought, but he can't have this."

### iron-coin node (new node, seed quotes)

**Q-13** — Coin description at point of use:
> Node: `iron-coin`
> Source: asos-arya-13:255
> Quote: "She pressed it into his hand, the small black iron coin that Jaqen H'ghar had given her, so worn the man whose head it bore had no features."

**Q-14** — Valar morghulis exchange:
> Node: `iron-coin`
> Source: asos-arya-13:259–261
> Quote: "Arya crossed her arms against her chest. 'Valar morghulis,' she said, as loud as if she'd known what it meant. 'Valar dohaeris,' he replied, touching his brow with two fingers. 'Of course you shall have a cabin.'"

### wall-of-faces (NOTE: no node exists for this yet — propose one)
The "wall of a thousand faces" / chamber of skins in ADWD ch.65 is a load-bearing location inside the HoBaW. It could be a sub-location node (`object-wall-of-faces` or `place.location` sub-node) or captured as a quote on the HoBaW node. Recommend: add quotes to `house-of-black-and-white` node for now; defer node-mint to Matt.

**Q-15** — Wall of faces reveal:
> Node: `house-of-black-and-white`
> Source: adwd-the-ugly-little-girl-01:183–185
> Quote: "A thousand faces were gazing down on her. They hung upon the walls, before her and behind her, high and low, everywhere she looked, everywhere she turned. She saw old faces and young faces, pale faces and dark faces, smooth faces and wrinkled faces, freckled faces and scarred faces, handsome faces and homely faces, men and women, boys and girls, even babes, smiling faces, frowning faces, faces full of greed and rage and lust, bald faces and faces bristling with hair. Masks, she told herself, it's only masks, but even as she thought the thought, she knew it wasn't so. They were skins."

---

## HARVEST (food / description rows)

Format: `chapter:line / kind / note`

### ASOS Arya XIII (asos-arya-13)
*(No food moments in this chapter — the chapter is the inn fight + river escape. The Hound's wine from the inn is a prop not a food moment.)*

### AFFC Arya I (affc-arya-01)
1. `affc-arya-01:25 / drink / fire wine — sailors on Titan's Daughter pour Arya "thimble cups of fire wine" on the crossing`
2. `affc-arya-01:73 / drink + atmosphere / "as she got deeper into the temple, they seemed to smell of snow and pine needles and hot stew" — candle-scent evokes home-food (stew); Winterfell food memory`

### AFFC Arya II (affc-arya-02)
3. `affc-arya-02:47 / prayer-as-food-context / Arya prays at dawn "before they broke their fast, kneeling around the still, black pool" — the black pool as pre-fast ritual anchor`
4. `affc-arya-02:67 / food-general / Umma's HoBaW kitchen meals: fish spiced with sea salt and cracked peppercorns, eels cooked with chopped garlic, occasional saffron — "Hot Pie would have liked it here" — strongest positive food sentence in arc`
5. `affc-arya-02:67 / food-list / Shellfish species from Braavos lagoon: clams, cockles, mussels, muskfish, frogs, turtles, mud crabs, leopard crabs, climber crabs, red eels, black eels, striped eels, lampreys, oysters — all appear on the carved wooden table at HoBaW meals`
6. `affc-arya-02:91 / food-paranoia / Arya at supper stares at "a slice of pale white meat" wondering if it's human flesh; kindly man: "It is pork, child, only pork" — hospitality-as-dread inversion`
7. `affc-arya-02:155 / drink + social / Arya tosses her silver fork into the canal — fork was a gift from a sailor on Titan's Daughter; the fork's origin from sea-voyage gift-exchange (hospitality)`
8. `affc-arya-02:197 / test/food / The worm: Arya "plucked the grave worm from his eye to eat it, but it melted like a shadow in her hand" — failed consumption as courage test`

### AFFC Cat of the Canals I (affc-cat-of-the-canals-01)
9. `affc-cat-of-the-canals-01:47 / condiment-intel / "I know what Blind Beqqo puts in the hot sauce he uses on his oysters" — Cat's information-gathering framed as food knowledge; oysters + hot sauce as trade secret`
10. `affc-cat-of-the-canals-01:55 / food-work / Cat helps Umma on moon-black nights: chopping big white mushrooms, boning fish — kitchen labor as dual-identity marker`
11. `affc-cat-of-the-canals-01:67 / fish-codfish / Tagganaro smacks Quill with a codfish — comic hospitality-via-fish; codfish as prop`
12. `affc-cat-of-the-canals-01:73 / oyster-sale / Mate on green galley "wolfed half a dozen oysters" while telling pirate story — oyster-as-social-lubricant, sailor-hospitality moment`
13. `affc-cat-of-the-canals-01:81 / oyster-brothel / Merry buys a dozen oysters every time Cat comes by the Happy Port — recurring hospitality transaction; oysters = friendship currency between Cat and Merry`
14. `affc-cat-of-the-canals-01:91 / cockle-sale / Black Pearl buys three cockles from Cat, pays in silver (ten times value) — highest-status food transaction in the arc; courtesan hospitality`
15. `affc-cat-of-the-canals-01:101 / condiment / "I should have hot sauce. Beqqo does, and he sells three times as many oysters as Brusco" — Cat's business insight via condiment gap`
16. `affc-cat-of-the-canals-01:119 / mussels-social / Tagganaro buys mussels from Cat and sucks them from their shells while urging her to work with him instead — mussels-as-negotiation; Casso the seal gets a cockle too`
17. `affc-cat-of-the-canals-01:131 / oyster-mummers / Mummers on the Ship descend to buy oysters from Cat's barrow; mummers as regular customers`
18. `affc-cat-of-the-canals-01:143 / food-contempt / Dareon brags: "Yesterday I ate herring with the whores, but within the year I'll be having emperor crab with courtesans" — class-ambition via food register; herring vs. emperor crab`
19. `affc-cat-of-the-canals-01:155 / oyster-vinegar / At Happy Port: "Yna, fetch some bread and vinegar" — oysters served with bread and vinegar at the brothel; HoBaW-hospitality vs. brothel-hospitality contrast`
20. `affc-cat-of-the-canals-01:157 / oyster-sale-daily-close / Cat leaves Happy Port with "a plump purse of coins and a barrow empty but for salt and seaweed" — the end-of-day rhythm; selling ALL oysters is the work-measure`
21. `affc-cat-of-the-canals-01:181 / post-ritual-meal / After bathing in lemonwater to wash off Cat's smell, Arya goes to Umma: "a piece of nice fried cod for her, and some mashed yellow turnips. She wolfed it down" — the warm meal as reward after de-personing ritual; most vivid food-as-comfort moment`
22. `affc-cat-of-the-canals-01:247 / warm-milk-punishment / Kindly man orders "warm milk for our friend Arya" after she admits killing Dareon — the blinding draught`
23. `affc-cat-of-the-canals-01:251 / warm-milk-ingested / "When the milk came, Arya drank it down. It smelled a little burnt and had a bitter aftertaste." — exact sensory description of the blinding-draught milk`

### ADWD The Blind Girl I (adwd-the-blind-girl-01)
24. `adwd-the-blind-girl-01:19 / smell-kitchen / "Hot peppers and fried fish, she decided, sniffing down the hall, and bread fresh from Umma's oven" — blind girl navigates by kitchen smell; food as sensory landmark`
25. `adwd-the-blind-girl-01:21 / breakfast / "sardines, fried crisp in pepper oil and served so hot they burned her fingers. She mopped up the leftover oil with a chunk of bread torn off the end of Umma's morning loaf and washed it all down with a cup of watered wine" — most detailed single-meal description in the arc; sensory rendering (texture, heat, oil, sting on scrape)`
26. `adwd-the-blind-girl-01:175 / tavern-hospitality / At Pynto's: "a cup of watered wine, a chunk of stinky cheese, and half of an eel pie" — Pynto's charitable hospitality to blind Beth; the eel pie is a named Braavosi dish`
27. `adwd-the-blind-girl-01:195 / blinding-cup / "That evening Umma served salt-crusted crabs for supper. When her cup was presented to her, the blind girl wrinkled her nose and drank it down in three long gulps. Then she gasped and dropped the cup. Her tongue was on fire" — the ongoing milk-draught (bitter cup) administered as a spice-fire this evening; recovery via bread: "A heel of bread was pressed into her hand"`

### ADWD The Ugly Little Girl I (adwd-the-ugly-little-girl-01)
28. `adwd-the-ugly-little-girl-01:113 / onion-broth / The insurance broker: "a cup of onion broth cooling at his elbow" — his signature food; the short guard tastes the broth before the old man drinks`
29. `adwd-the-ugly-little-girl-01:145 / tasting-broth-guard / "At the soup shop, the short one always tasted the onion broth first. The old man waited until the broth had cooled before he took a sip, long enough to be sure his guardsman had suffered no ill effects." — food as poison-anxiety; the soup shop tasting ritual`
30. `adwd-the-ugly-little-girl-01:197 / lemon-drink / After the face-change ritual: "Drink this," and pressed a cup into her hand. She drank it down at once. It was very tart, like biting into a lemon." — the ritual drink of the face-change ceremony; lemon as memory-trigger (Sansa's lemon cakes)`
31. `adwd-the-ugly-little-girl-01:197 / lemon-memory / "A thousand years ago, she had known a girl who loved lemon cakes. No, that was not me, that was only Arya." — the lemon-drink triggers a Sansa/Arya identity-displacement memory; food-as-identity-marker`

---

## STRUCTURAL NOTES FOR PROPOSER

1. **NEEDS_VOCAB flags (3):**
   - `SOURCE_OF` or `GAVE` — to wire jaqen-hghar as source of the iron-coin without losing the object node
   - `USES` / `TRAINS_WITH` — to wire arya→myrish-mirror (WIELDS is wrong for a non-weapon)
   - `PASSES_THROUGH` or event-based solution — to wire arya's threshold-crossing of the Titan without creating a false LOCATED_AT (she doesn't live there, she sails through)

2. **Event nodes needed before several edges can be written:**
   - `event-arya-departs-westeros` (Saltpans, coin use, ASOS ch.75)
   - `event-arya-arrives-hobaw` (AFFC ch.7, second coin use)
   - `event-arya-hides-needle` (AFFC ch.23, identity-retention moment)
   - `event-arya-kills-insurance-merchant` (ADWD ch.65, first FM assassination)

3. **HoBaW node type anomaly:** `house-of-black-and-white` is currently in `graph/nodes/houses/` but is a place (temple), not a house in the dynastic sense. May need a `place.location` type re-filing. Flag for Matt.

4. **Happy Port and Pynto's:** Both are named recurring locations in Cat's Braavos life. Neither appears to exist in the location nodes. They are sub-locations within Braavos (wharfside district). Borderline on whether to propose as nodes vs. harvest queue. Recommendation: Harvest queue only — they are atmospheric settings, not load-bearing for traversal at this stage.
