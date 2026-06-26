# Lens C — Descriptive / Quote / Object Depth
## Sansa / Vale Arc Enrichment Dip

Source chapters: `asos-sansa-06`, `asos-sansa-07`, `affc-sansa-01`, `affc-alayne-01`, `affc-alayne-02`
Run: 2026-06-25

---

## OBJECT / ARTIFACT NODES (or why not)

### 1. Moon Door — EXISTS as `moon-door` (artifact)
Do not create a new node. The node exists with no outbound edges. The gap is relational context:
- Propose `WIELDED_IN` edge: `moon-door` → event node for Lysa Arryn's death (see below — the death event needs minting first; see DEDUP NOTES).
- Propose `LOCATED_AT` edge: `moon-door` LOCATED_AT `eyrie`.

### 2. Marillion's woodharp — NEW NODE probably not warranted
The harp is mentioned three times across the chapters — it plays while Lysa tries to push Sansa through the Moon Door (asos-sansa-07:247), it is left to Marillion in his sky cell (affc-sansa-01:177), and its sound characterizes the arc's dread ambience. It is referred to only as "his woodharp" — no proper name, no unique history or legendary status. The harp is narratively resonant but not an iconic named object like Lady Forlorn or Ice. **Better as a quote attachment to `marillion`.** No new node proposed.

### 3. Sweetrobin's cloth doll — NEW NODE probably not warranted
The doll is central to one scene (asos-sansa-07:121–129) and is torn apart, triggering Robert's shaking fit. It is a character-prop rather than a named, legendary artifact. It illuminates `robert-arryn`'s childishness and fragility. **Better as a quote attachment to `robert-arryn`.** No new node proposed.

### 4. Silver hair net with strangler — EXISTS
Two nodes already exist: `silver-hair-net` (object.artifact) and `strangler` (concept.medical), plus the event node `sansa-receives-the-poisoned-hairnet`. The mention in asos-sansa-06:145–183 is LF's confession of how the hairnet was used. This is high-value evidence for those existing nodes:
- Propose `GIFTED_TO` edge: `silver-hair-net` GIFTED_TO `sansa-stark` — direction giver→recipient means `dontos-hollard` GIFTED_TO `sansa-stark`, but since `silver-hair-net` is the artifact, the cleaner attachment is a quote on `sansa-receives-the-poisoned-hairnet` citing asos-sansa-06:145.
- The quote "make certain you wore your silver hair net" (LF to Sansa) is the first direct in-book confirmation of how the strangler was delivered. ATTACH-TO `sansa-receives-the-poisoned-hairnet` ## Quotes.

### 5. Alayne's dyed-brown hair — NOT an artifact node
This is an identity-concealment device: an ongoing physical state, not an object. It is best modeled as a quote on `sansa-stark` or as descriptive prose on a future cross-identity beat node. No artifact node warranted. Hair-dye origin (Tyroshi wash, affc-alayne-01:25) is a useful provenance note.

### 6. Sweetrobin's cloak / brooch (sky-blue lambswool + crescent moon brooch)
Mentioned in affc-sansa-01:119. Not iconic enough for its own node. Better as a quote attachment to `robert-arryn`.

### 7. Robert Arryn's weirwood throne (High Hall of the Eyrie)
The High Hall is mentioned to contain "a high-backed chair of carved weirwood" for Lord Robert (asos-sansa-07:173). The weirwood chair is an interesting material detail (a weirwood object in a castle without a heart tree), but has no proper name and no legendary provenance. **Not a new node; better as a quote on `eyrie`.** Note: if a `high-hall-of-the-eyrie` node exists or is minted, the quote belongs there.

### 8. Alayne's mockingbird brooch (cloak pin)
Mentioned in affc-alayne-02:179 — "fastening it with an enameled mockingbird that had been a gift from Petyr." This is a gift edge waiting to happen. If `sansa-stark` gets an OWNS edge to a mockingbird-brooch node, it illuminates LF's control-through-identity. However, the object is not named or legendary. **Better as a harvest note.** No node.

---

## PLACE EDGES

All place nodes referenced have been verified to exist unless noted.

### Descent waycastle chain
- `snow-waycastle` EXISTS; `sky-cells` EXISTS (though `sky` as a waycastle distinct from the sky cells may need checking — see below); `stone-waycastle` was NOT found (returned no match). A `stone-waycastle` node may need minting or may exist under a different slug.
- `gates-of-the-moon` EXISTS.
- `fingers` EXISTS.
- `eyrie` EXISTS.
- `giants-lance` EXISTS.
- `drearfort` EXISTS.

**Proposed LOCATED_AT edges (spine event nodes → places):**

These edges connect the arc's key scenes to their correct place nodes. The arc's events are largely set at the Eyrie; the descent chapters add the waycastle chain.

1. `sansa-stark` LOCATED_AT `eyrie` — her place of residence during the Vale arc. (Tier 1, book-provenance, entire arc)
2. `sansa-stark` LOCATED_AT `drearfort` — at the Fingers on arrival (asos-sansa-06). Sub-stop before Eyrie.
3. `wedding-of-petyr-baelish-and-lysa-arryn` LOCATED_AT `drearfort` — the wedding happens at the Fingers tower, outdoors. (asos-sansa-06:245: "trestle tables were set up beneath the small flint tower")
4. `moon-door` LOCATED_AT `eyrie` — artifact needs its place anchor.
5. `marillion` LOCATED_AT `sky-cells` — his imprisonment location (affc-sansa-01: "Mord, take him back to his sky cell").
6. [Lysa's death event — see DEDUP NOTES] LOCATED_AT `eyrie` + specifically the High Hall.

**Descent chain LOCATED_AT proposals (for Alayne II chapter events):**
- The descent scene in affc-alayne-02 passes through `sky-cells` / Sky waycastle → `snow-waycastle` → stone waycastle (slug needs verification). Propose `mya-stone` LOCATED_AT `gates-of-the-moon` as her base. The mule descent itself is a scene, not a graph event node yet, but when a descent event is minted it should carry LOCATED_AT edges to all three waycastles.

**NEEDS_VOCAB:** There is no edge type for "PASSES_THROUGH" or "DEPARTS_FROM" / "ARRIVES_AT." For the mountain descent, LOCATED_AT covers the waycastles as settings. The sequential ordering of waycastles (Sky above Snow above Stone) is currently only encoded in wiki prose; it may warrant PRECEDES edges between waycastle nodes if/when the chronology-extractor track runs.

---

## QUOTE ATTACHMENTS (ATTACH-TO existing nodes)

All quotes are verbatim substrings from the chapter files as read. Chapter:line numbers given.

---

### Q1 — "Only Cat" (Lysa's death / LF's true feeling)
**Quote:** `"I've only loved one woman, I promise you." / Lysa Arryn smiled tremulously. "Only one? Oh, Petyr, do you swear it? Only one?" / "Only Cat." He gave her a short, sharp shove.`
**Source:** asos-sansa-07:297–301
**ATTACH-TO:** `lysa-arryn` ## Quotes AND `petyr-baelish` ## Quotes
**Note:** This is the single most load-bearing quote of the arc — LF's motive confession and the act of murder in three lines. It should also attach to whatever event node models Lysa's death once minted (see DEDUP NOTES).

---

### Q2 — Snow castle / kiss (Petyr kisses Sansa in the garden)
**Quote:** `"Something else would please me more." He stepped closer. "This." / Sansa tried to step back, but he pulled her into his arms and suddenly he was kissing her. Feebly, she tried to squirm, but only succeeded in pressing herself more tightly against him. His mouth was on hers, swallowing her words. He tasted of mint.`
**Source:** asos-sansa-07:95–97
**ATTACH-TO:** `sansa-stark` ## Quotes AND `petyr-baelish` ## Quotes
**Note:** The most intimate / disturbing moment of the arc; the snow-castle scene that precedes Lysa's jealous explosion.

---

### Q3 — Snow castle description (Winterfell in snow)
**Quote:** `The snow fell and the castle rose. Two walls ankle-high, the inner taller than the outer. Towers and turrets, keeps and stairs, a round kitchen, a square armory, the stables along the inside of the west wall. It was only a castle when she began, but before very long Sansa knew it was Winterfell.`
**Source:** asos-sansa-07:41
**ATTACH-TO:** `sansa-stark` ## Quotes
**Note:** The definitive characterization of the snow-castle scene and Sansa's identification with Winterfell. "The taste of Winterfell. The taste of innocence. The taste of dreams." (asos-sansa-07:31) is a companion passage worth attaching at the same node.

---

### Q4 — "The taste of Winterfell" (companion to Q3)
**Quote:** `It was the taste of Winterfell. The taste of innocence. The taste of dreams.`
**Source:** asos-sansa-07:31
**ATTACH-TO:** `sansa-stark` ## Quotes
**Note:** Pure sensory/memory; closes the snow-falling arrival scene.

---

### Q5 — Moon Door / Lysa threatens Sansa
**Quote:** `"Look down," said Lady Lysa. "Look down." / She tried to wrench free, but her aunt's fingers were digging into her arm like claws. Lysa gave her another shove, and Sansa shrieked. Her left foot broke through a crust of snow and knocked it loose. There was nothing in front of her but empty air, and a waycastle six hundred feet below clinging to the side of the mountain.`
**Source:** asos-sansa-07:245–247
**ATTACH-TO:** `moon-door` ## Quotes AND `lysa-arryn` ## Quotes
**Note:** This is Sansa's near-defenestration — the Moon Door's function made visceral. "a waycastle six hundred feet below" names Sky in passing.

---

### Q6 — Marillion singing while Lysa threatens (contextual dread)
**Quote:** `Behind her, Marillion was still playing his woodharp and singing, "Hey-nonny, hey-nonny, hey-nonny-hey."`
**Source:** asos-sansa-07:247
**ATTACH-TO:** `marillion` ## Quotes
**Note:** The juxtaposition of the bawdy song and the attempted murder is the defining characterization of Marillion as an instrument of LF's schemes.

---

### Q7 — LF confesses the hairnet / Olenna
**Quote:** `"I will wager you that at some point during the evening someone told you that your hair net was crooked and straightened it for you."`
**Source:** asos-sansa-06:183
**ATTACH-TO:** `sansa-receives-the-poisoned-hairnet` ## Quotes
**Note:** This is LF's oblique admission that Olenna Tyrell lifted the strangler from the net. Cite evidence for `olenna-tyrell` ← → `strangler` connection.

---

### Q8 — LF explains the players and pieces
**Quote:** `"In King's Landing, there are two sorts of people. The players and the pieces." / "And I was a piece?" She dreaded the answer. / "Yes, but don't let that trouble you. You're still half a child."`
**Source:** asos-sansa-06:137–139
**ATTACH-TO:** `petyr-baelish` ## Quotes AND `sansa-stark` ## Quotes
**Note:** The defining statement of LF's worldview and his framing of Sansa; central to the arc's power dynamic.

---

### Q9 — Alayne's hair / identity
**Quote:** `The wash her aunt had given her changed her own rich auburn into Alayne's burnt brown, but it was seldom long before the red began creeping back at the roots.`
**Source:** affc-alayne-01:25
**ATTACH-TO:** `sansa-stark` ## Quotes
**Note:** Precise, physical description of the disguise's instability — "the red creeping back" as a literal metaphor for Sansa's suppressed identity. Provenance: Tyroshi wash.

---

### Q10 — Mya Stone / the throwing memory (trust)
**Quote:** `"I remember a man throwing me in the air when I was very little. He stands as tall as the sky, and he throws me up so high it feels as though I'm flying. We're both laughing, laughing so much that I can hardly catch a breath, and finally I laugh so hard I wet myself, but that only makes him laugh the louder. I was never afraid when he was throwing me. I knew that he would always be there to catch me." She pushed her hair back. "Then one day he wasn't. Men come and go. They lie, or die, or leave you. A mountain is not a man, though, and a stone is a mountain's daughter. I trust my father, and I trust my mules. I won't fall."`
**Source:** affc-alayne-02:367
**ATTACH-TO:** `mya-stone` ## Quotes
**Note:** The most revealing passage for Mya Stone anywhere in the text — her abandonment by Robert Baratheon encoded in a childhood memory, and her coping philosophy. "a stone is a mountain's daughter" is essential characterization.

---

### Q11 — Harry the Heir reveal (LF's endgame)
**Quote:** `"So those are your gifts from me, my sweet Sansa . . . Harry, the Eyrie, and Winterfell. That's worth another kiss now, don't you think?"`
**Source:** affc-alayne-02:467
**ATTACH-TO:** `sansa-stark` ## Quotes AND `petyr-baelish` ## Quotes
**Note:** LF names Sansa aloud — the only time he does so in these five chapters — and names his plan. Load-bearing for the arc's long-game.

---

### Q12 — "Life is not a song" equivalent — not found in these chapters
The phrase "Life is not a song, sweetling" does not appear verbatim in the five source chapters. It is a well-known LF line but falls outside this chapter set; do not fabricate a cite.

---

### Q13 — Robert's doll destruction / shaking fit
**Quote:** `"Robert, stop that." Instead he swung the doll again, and a foot of wall exploded. She grabbed for his hand but she caught the doll instead. There was a loud ripping sound as the thin cloth tore. Suddenly she had the doll's head, Robert had the legs and body, and the rag-and-sawdust stuffing was spilling in the snow.`
**Source:** asos-sansa-07:127
**ATTACH-TO:** `robert-arryn` ## Quotes
**Note:** The torn doll, the collapsed snow castle, Robert's fit — the scene that triggers Lysa's jealous confrontation. "rag-and-sawdust stuffing" is specific physical detail.

---

### Q14 — Sweetsleep introduction
**Quote:** `"Perhaps a pinch of sweetsleep in his milk, have you tried that? Just a pinch, to calm him and stop his wretched shaking." / "A pinch?" The apple in the maester's throat moved up and down as he swallowed. "One small pinch . . . perhaps, perhaps. Not too much, and not too often, yes, I might try . . ."`
**Source:** affc-alayne-01:87–89
**ATTACH-TO:** `robert-arryn` ## Quotes
**Note:** The first explicit introduction of sweetsleep being administered to Sweetrobin, at LF's instruction. Essential for the poisoning-through-medicine thread. Also attach to `petyr-baelish` ## Quotes as a `SUSPECTED_OF` evidence anchor.

---

### Q15 — Eyrie description (prison, cold white place)
**Quote:** `It will be even worse in winter, she knew. In winter this will be a cold white prison.`
**Source:** affc-alayne-02:153
**ATTACH-TO:** `eyrie` ## Quotes OR `sansa-stark` ## Quotes
**Note:** Sansa's final settled assessment of the Eyrie before the descent. Precise, affectively rich; contrasts directly with her Winterfell nostalgia.

---

## DEDUP NOTES

**Missing event node — Lysa Arryn's death:** There is no existing event node for LF's murder of Lysa through the Moon Door. Suggested slug: `lysa-arryn-thrown-from-moon-door` or `murder-of-lysa-arryn`. This event is referenced extensively in wiki prose (petyr-baelish.prose, lysa-arryn.prose, multiple house nodes) and should be minted. It would receive:
- Quotes Q1, Q5
- `LOCATED_AT eyrie` (specifically the High Hall)
- `moon-door` WIELDED_IN this event
- `petyr-baelish` KILLS / SUSPECTED_OF (depending on edge vocab)
- `marillion` BLAMED_FOR (he is framed; NEEDS_VOCAB — no FRAMED_FOR type exists)

**Node dedup check passed for:**
- `sansa-stark` (aliases include Alayne Stone — correct; do NOT use `alayne` or `alayne-royce` which are different people)
- `robert-arryn` (aliases include Sweetrobin — correct; do NOT use `robin-arryn`)
- `petyr-baelish` (aliases include Littlefinger — correct)
- `lysa-arryn` (aliases include Lysa Tully — correct)
- `marillion` — node exists, character.human
- `moon-door` — exists, object.artifact
- `eyrie` — exists, place.location
- `godswood-of-the-eyrie` — exists, place.location (noted as having no heart tree; present in affc-alayne-02:153)
- `vale-of-arryn` — exists, place.region
- `gates-of-the-moon` — exists, place.location
- `snow-waycastle` — exists
- `sky-cells` — exists (this is the prison; Sky as a waycastle distinct from the sky cells may be the same node — verify)
- `stone-waycastle` — NOT found; may need minting or a different slug lookup
- `fingers` — exists, place.location
- `drearfort` — exists, place.location
- `giants-lance` — exists, place.location
- `mya-stone` — exists
- `silver-hair-net` — exists, object.artifact (concept.medical is a slightly odd type; may warrant reclassification to object.artifact)
- `strangler` — exists, concept.medical

---

## HARVEST

Format: `chapter:line / kind / note`

### asos-sansa-06

- `06:75` / food / "cold salt mutton" — LF's ironic greeting to the Fingers' provisions; preserved meat, first food mentioned at Drearfort
- `06:89` / food+drink / "several casks of wine" offloaded from *Merling King*; Petyr gives Sansa a cup: "an Arbor vintage, she thought. It tasted of oak and fruit and hot summer nights"
- `06:93` / food / Grisel brings "apples and pears and pomegranates, some sad-looking grapes, a huge blood orange" plus "a round of bread . . . and a crock of butter" — first meal ashore at the Fingers
- `06:133` / food / Petyr eats pomegranate seeds with the point of his dagger throughout the conversation; blood orange squeezed into his mouth: "I love the juice but I loathe the sticky fingers"
- `06:135` / food / Sansa chooses a pear over the messy pomegranate: "It was very ripe. The juice ran down her chin." — typical Sansa fastidiousness
- `06:291` / food / Morning tray to the bridal chamber: "morning bread, with butter, honey, fruit, and cream"
- `06:307` / food / Lysa "ate a pear and studied her" / nibbles "the corner of a honeycomb" / "licked honey from her fingers" — Lysa eating sweet, sticky things throughout the confrontation scene
- `06:245` / food+drink / Wedding feast outdoors: "quail, venison, and roast boar, washing it down with a fine light mead" — the wedding menu; also "trestle tables set up beneath the small flint tower"
- `06:245` / drink / Mead served at the wedding feast; Lysa's mead-and-marriage glow noted
- `06:292` / food / Morning after the wedding: Lysa still in bed eating a pear, nibbling honeycomb
- `06:75` / description / "dung fire burning" at the Fingers tower — smell of home; specific fuel type
- `06:81` / description / Interior of Drearfort tower: single room per floor, arrowslits, no windows; "broken longsword and a battered oaken shield" above the hearth with the Titan's head sigil
- `06:83` / description / LF's grandfather's shield: "a grey stone head with fiery eyes, upon a light green field" — House Baelish origin story (Braavosi sellsword heritage)

### asos-sansa-07

- `07:21` / description / Snow falling on the Eyrie: "all color had fled the world outside. It was a place of whites and blacks and greys. White towers and white snow and white statues, black shadows and black trees, the dark grey sky above."
- `07:27` / description / Sansa's dress for the snow-castle scene: "warm dress of blue lambswool. Two pairs of hose for her legs, boots that laced up to her knees, heavy leather gloves, and finally a hooded cloak of soft white fox fur."
- `07:39-41` / description / Snow castle construction sequence — full physical process; towers, walls, armory, stables, godswood twigs, gravestone bark fragments
- `07:97` / description / LF after the kiss: "He tasted of mint." — single most specific sensory detail in the scene
- `07:121` / description / Sweetrobin's appearance: "small for eight, a stick of a boy with splotchy skin and eyes that were always runny. Under one arm he clutched the threadbare cloth doll he carried everywhere." — canonical physical description
- `07:129` / description / Robert's shaking fit onset: "It started with no more than a little shivering, but within a few short heartbeats he had collapsed across the castle, his limbs flailing about violently."
- `07:131` / food / Maester Colemon gives Robert "half a cup of dreamwine" to calm the shaking fit

### affc-sansa-01

- `sansa-01:17` / food+description / Sky cells described from inside by sound: Marillion's singing floats through the wall of empty air; "the sky cells had a wall of empty air, so every chord the dead man played flew free to echo off the stony shoulders of the Giant's Lance"
- `sansa-01:61` / drink / "We shall serve him lies and Arbor gold, and he'll drink them down and ask for more" — LF to Sansa; Arbor gold used to bribe Nestor Royce
- `sansa-01:197` / drink / "A low fire burned in the solar, where a flagon of wine awaited them. Arbor gold. Sansa filled Lord Nestor's cup" — the actual bribery scene; Arbor gold as a recurring motif
- `sansa-01:167` / description / Marillion post-torture: "Someone had bathed him and dressed him in a pair of sky-blue breeches and a loose-fitting white tunic with puffed sleeves, belted with a silvery sash that had been a gift from Lady Lysa. White silk gloves covered his hands, whilst a white silk bandage spared the lords the sight of his eyes." — detailed physical description of the blinded singer
- `sansa-01:183` / description / Mord: "a monstrous man with small black eyes and a lopsided, scarred face. One ear and part of his cheek had been cleaved off in some battle, but twenty stone of pallid white flesh remained. His clothes fit poorly and had a rank, ripe smell." — canonical Mord description with missing ear detail
- `sansa-01:183` / description / Mord's gold teeth: "Sansa saw to her astonishment that the gaoler's teeth were made of gold." — noteworthy physical detail
- `sansa-01:290` / food / Morning: Sweetrobin crawls into Sansa's bed; she puts her arm around him — no food, but: if Lysa's milk-of-mother reference counts as food: `sansa-01:81` — Maester Colemon notes "Lady Lysa would give his lordship her breast whenever he grew overwrought. Archmaester Ebrose claims that mother's milk has many healthful properties." (grim register — she breastfed an eight-year-old)

### affc-alayne-01

- `alayne-01:29` / food / Sweetrobin's breakfast: "big bowl of porridge and honey" — he wanted "three eggs boiled soft, and some back bacon" but there are none; the siege by Lords Declarant has cut off fresh food
- `alayne-01:31-33` / food / Siege ration note: "The Eyrie's granaries held sufficient oats and corn and barley to feed them for a year, but they depended on a bastard girl named Mya Stone to bring fresh foodstuffs up." No eggs, no bacon; Belmore's blockade.
- `alayne-01:51` / food / Porridge spilled on Maester Colemon — "the wooden bowl caught him square in the chest, and its contents exploded upward over his face and shoulders"
- `alayne-01:87-91` / food (GRIM) / LF suggests sweetsleep in Robert's milk: "Perhaps a pinch of sweetsleep in his milk, have you tried that? Just a pinch." — this is the first explicit order to drug Sweetrobin; critical poisoning-through-medicine evidence
- `alayne-01:101-103` / food / "Tell the cook to mull some red wine with honey and raisins" — LF's hospitality order for Lords Declarant; "wine, bread, and cheese" — "The sharp white and the stinky blue" — Petyr rejects stinky blue: "Choose the white."
- `alayne-01:155` / food / Sansa's hospitality prep for Lords Declarant: mulled wine, "wheel of sharp white cheese," bread "enough for twenty" — "Once they eat our bread and salt they are our guests." — host-right invocation
- `alayne-01:163` / food / Lords Declarant receive "bread and cheese and cups of hot mulled wine in silver cups" in the Crescent Chamber
- `alayne-01:197` / food+drink / LF and Nestor drain the Arbor gold flagon in private; the grant-of-Gates-of-the-Moon is sealed over wine
- `alayne-01:25` / description / Alayne's disguise: "The wash her aunt had given her changed her own rich auburn into Alayne's burnt brown, but it was seldom long before the red began creeping back at the roots." Tyroshi dye.
- `alayne-01:157` / description / Alayne chooses her dress for the Lords Declarant meeting: "lambswool, dark brown and simply cut, with leaves and vines embroidered around the bodice, sleeves, and hem in golden thread . . . a simple velvet ribbon in autumn gold" — the "bastard modest" outfit
- `alayne-01:23` / description / Lysa's old gowns given to Alayne: "a wealth of silks, satins, velvets, and furs far beyond anything she had ever dreamed, though the great bulk of it was far too large for her; Lady Lysa had grown very stout"
- `alayne-01:15` / description / Eyrie view from Maiden's Tower: "Icicles twenty feet long draped the lip of the precipice where Alyssa's Tears fell in summer. A falcon soared above the frozen waterfall"
- `alayne-01:19` / description / Physical orientation of the descent: "She could see Sky six hundred feet below, and the stone steps carved into the mountain, the winding way that led past Snow and Stone all the way down to the valley floor."

### affc-alayne-02

- `alayne-02:33-39` / food / Morning: Sweetrobin demands eggs and bacon; there are none; porridge and honey is what's available. "berries and cream, or some warm bread and butter" — offered but no kitchen fire; he refuses porridge.
- `alayne-02:65` / drink (GRIM) / Robert says: "Maester Colemon put something vile in my milk last night, I could taste it. I told him I wanted sweetmilk" — sweetmilk = drugged milk; Robert knows it tastes different; he WANTS it (dependency established)
- `alayne-02:83` / food / "sweetmilk" — Robert wants it, Colemon has refused; Alayne promises to talk to him about it
- `alayne-02:85` / food / LF has promised a feast at Gates of the Moon: "mushroom soup and venison and cakes"
- `alayne-02:87-89` / food / Lemon cakes — Robert loves them; Alayne promises "lemony lemony lemon cakes . . . a hundred . . . and you can have as many as you like"; she later asks LF if he brought lemons as a gift
- `alayne-02:127-133` / drink (GRIM) / Alayne orders sweetsleep for Robert before the descent: "Give his lordship a cup of sweetmilk." Colemon warns: "in time . . . [it] does not leave the flesh." Alayne overrides: "If my father were here, I know he would tell you to keep Lord Robert calm at all costs." — Alayne is now actively complicit in the drugging.
- `alayne-02:171` / description / Mord butchering the winch oxen: "Mord would cut their throats and butcher them before he left, and leave them for the falcons. Whatever part remained when the Eyrie was reopened would be roasted up for the spring feast, if it had not spoiled." — spring/winter food preservation detail
- `alayne-02:193` / description / Sweetrobin's descent outfit: "sky-blue velvet, a chain of gold and sapphires, and a white bearskin cloak. His squires each held an end, to keep the cloak from dragging on the floor."
- `alayne-02:181` / description / Mya Stone physical description: "Slim and sinewy, Mya looked as tough as the old riding leathers she wore beneath her silvery ringmail shirt. Her hair was black as a raven's wing, so short and shaggy that Alayne suspected that she cut it with a dagger. Mya's eyes were her best feature, big and blue." — canonical Mya description; "those are his eyes, and she has his hair too, the thick black hair he shared with Renly" (Robert Baratheon recognition)
- `alayne-02:221` / description / Sky waycastle: "no more than a crescent-shaped wall of old unmortared stone, enclosing a stony ledge and the yawning mouth of a cavern. Inside were storehouses and stables, a long natural hall, and the chiseled handholds that led up to the Eyrie."
- `alayne-02:355` / description / Narrow stone saddle crossing: "a high stone saddle, narrow and icy . . . a yard across, and no more than eight yards long" — the single most dangerous physical section of the descent
- `alayne-02:355` / foreshadowing / "It sounds like a wolf, thought Sansa. A ghost wolf, big as mountains." — the wind on the saddle is read as a direwolf howl; involuntary Stark identity resurgence at the moment of greatest physical danger
- `alayne-02:359` / food / Snow waycastle: "a hot meal of stewed goat and onions" — the first warm food of the descent; shared by Alayne, Mya, Myranda
- `alayne-02:431` / food / LF brings no lemons, but brings a marriage contract; Alayne's disappointment ("Lemons? Did you find some lemons?") is vivid — the lemon cake through-line
- `alayne-02:467` / food (GRIM) / LF drunk-breathed: "She could smell the wine on his breath, the cloves and nutmeg." — mulled wine; the betrothal revelation scene
- `alayne-02:101` / food (GRIM REGISTER) / Maester Colemon described Robert as nursing from Lysa (historical): "Lady Lysa would give his lordship her breast whenever he grew overwrought." — affc-alayne-01:81; included here as the grim register item closest to this track
- `alayne-02:83` / food (GRIM) / "sweetmilk" demanded by Robert — the drugged-milk dependency is fully established by affc-alayne-02; Robert calls it by name and wants it; Colemon is actively warning of cumulative harm ("does not leave the flesh"); Alayne is ordering it administered

---

*End of Lens C — Descriptive / Quote / Object Depth*
