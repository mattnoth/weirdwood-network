# Lens 3 — Object/Artifact Depth + Descriptive Anchors
## Brienne → Lady Stoneheart arc (AFFC)

> Output of LENS 3 (descriptive / quote / object depth) enrichment pass.
> Orchestrator (Opus) line-checks, dedups, decides — do NOT mint directly.
> All line numbers are from the chapter files under sources/chapters/affc/.

---

## NEW NODE PROPOSALS

### `hound-helm`
- **type:** object.artifact
- **slug:** hound-helm
- **aliases:** ["the Hound's helm", "snarling dog helm", "hound's head helm", "dog's head helm"]
- **justification:** The snarling dog greathelm is the misattribution engine for the entire arc. Sandor wore it as his signature piece; Elder Brother placed it atop the grave-cairn as a marker; Rorge found and looted it, then wore it to commit the Saltpans atrocity, causing the entire realm to blame the wrong man; Brienne fights Rorge at the inn while he wears it (the helm is pressed against her cheek at the kill); Lem Lemoncloak then claims it off Rorge's corpse and wears it when he hangs Brienne's party. Three different wearers in three chapters = a named prop with a distinct, consequential history. The arc cannot be traversed without it.
- **tier:** tier-1

### `stranger-horse`
- **type:** object.creature (or simply flag on the Stranger/Driftwood node if one already exists)
- **slug:** stranger-horse (aka driftwood-horse at Quiet Isle)
- **aliases:** ["Stranger", "Driftwood"]
- **justification:** Sandor Clegane's warhorse. The Elder Brother explicitly identifies "Stranger" as Sandor's destrier, left behind at the Quiet Isle where the brothers renamed him Driftwood. The horse's presence is proof of the Hound's passage and confirms his death to Brienne. It is a named creature with consequential plot function; if the graph already has a node, discard this proposal.
- **tier:** tier-1
- **note:** Verify whether a `stranger-horse` or `driftwood-horse` node already exists before minting.

---

## EDGE PROPOSALS

### A. THE HOUND'S HELM — wiring its chain of custody

**1. Elder Brother places helm on Sandor's grave**

`sandor-clegane --OWNED--> hound-helm | tier-1 | affc-brienne-06:191 | "I covered him with stones to keep the carrion eaters from digging up his flesh, and set his helm atop the cairn to mark his final resting place." | Establishes Sandor's ownership and the Elder Brother's act of marking the cairn with it — this is the genesis of the misidentification chain.`

`elder-brother-quiet-isle --OWNS--> hound-helm | tier-2 | affc-brienne-06:191 | "set his helm atop the cairn to mark his final resting place. That was a grievous error." | He placed it and considers himself responsible for the error; transient custodianship.`

**2. Rorge loots the helm from the grave**

`hound-helm --LOOTED_BY--> rorge | tier-1 | raid-on-saltpans (wiki node) / affc-brienne-07:265 | "beneath the dark hood of the lead rider Brienne glimpsed an iron snout and rows of steel teeth, snarling." | Text describes Rorge wearing it at the inn; wiki confirms he found it on Sandor's grave-cairn (Quiet Isle).`

**3. Rorge wields it at Saltpans + the inn**

`hound-helm --WIELDED_IN--> raid-on-saltpans | tier-1 | raid-on-saltpans (wiki) | (wiki node body: "Led by Rorge, who is still wearing the Hound's helm") | The helm is the instrument of misattribution during the Saltpans raid.`

`hound-helm --WIELDED_IN--> inn-fight-at-crossroads | tier-1 | affc-brienne-07:265–293 | "beneath the dark hood of the lead rider Brienne glimpsed an iron snout and rows of steel teeth, snarling." | Rorge wears it at the inn fight where Brienne kills him.`

> NOTE: `inn-fight-at-crossroads` may need to be proposed as a new event node (event.battle) — the affc-brienne-08 fight at the inn is where Rorge is killed, Biter mauls Brienne, and Gendry kills Biter. It is distinct from the earlier ASOS inn fight where Sandor killed three Mountain's men. Check baseline for whether this node exists; if not, flag for Lens 1/orchestrator to mint.

**4. Brienne kills Rorge — Oathkeeper pressed against the helm**

`brienne-tarth --WIELDED_IN--> inn-fight-at-crossroads (via oathkeeper) | tier-1 | affc-brienne-07:293 | "she leapt to meet his rush, both hands on her sword hilt. His headlong charge brought him right onto her point, and Oathkeeper punched through cloth and mail and leather and more cloth, deep into his bowels and out his back, rasping as it scraped along his spine." | Oathkeeper wielded at the inn fight — the kill of Rorge.`

`oathkeeper --WIELDED_IN--> inn-fight-at-crossroads | tier-1 | affc-brienne-07:293 | (same quote above) | Oathkeeper is the weapon used to kill Rorge.`

**5. Lem Lemoncloak claims the helm off Rorge's corpse**

`hound-helm --LOOTED_BY--> lem-lemoncloak | tier-1 | affc-brienne-08:97 | "From his shoulders rose a steel dog's head, its teeth bared in a snarl." (and affc-brienne-08:214: "It was Rorge I killed. He took the helm from Clegane's grave, and you stole it off his corpse.") | Lem wears the helm when Brienne is brought before Stoneheart and at the hanging scene. The chain of custody is explicit.`

`hound-helm --WIELDED_IN--> brienne-brought-before-lady-stoneheart | tier-1 | affc-brienne-08:211 | "I suppose I am. Seeing as how m'lady went and killed the last one." | Lem wears the helm during the Brotherhood tribunal and the hanging.`

**6. Helm's misattribution engine — PERCEIVED_AS / REPUTED_AS**

`sandor-clegane --REPUTED_AS--> mad-dog-of-saltpans | tier-1 | affc-brienne-05:209 | "The Mad Dog of Saltpans, I have heard him called." | Septon Meribald's naming. The public reputation attaches to Sandor because of the helm, not his actions.`

`rorge --PERCEIVED_AS--> sandor-clegane | tier-1 | affc-brienne-06:185 | "The man who raped and killed at Saltpans was not Sandor Clegane, though he may be as dangerous." | Elder Brother's correction to Brienne; establishes that the realm perceived Rorge-in-the-helm as Sandor.`

`randyll-tarly --DECEIVES--> brotherhood-without-banners | tier-1 | affc-brienne-05:134–136 | "Lord Randyll is putting it about that they did in hopes of turning the commons against Beric and his brotherhood." | Tarly deliberately misattributes the Saltpans raid to the Brotherhood, compounding the helm's misattribution.`

---

### B. OATHKEEPER — new WIELDED_IN edges not in baseline

`oathkeeper --WIELDED_IN--> fight-at-the-whispers | tier-1 | affc-brienne-04:307–319 | "Oathkeeper was alive in her hands. She had never been so quick. The blade became a grey blur." | Brienne kills Timeon and Pyg with Oathkeeper at the Whispers. Shagwell is killed with a dagger.`

> Baseline note: baseline confirms `brienne KILLS shagwell/pyg/timeon` but doesn't wire Oathkeeper into the fight-at-the-whispers event. Check whether `fight-at-the-whispers` is a named event node.

**Oathkeeper seized by Brotherhood**

`oathkeeper --HELD_BY--> brotherhood-without-banners | tier-1 | affc-brienne-08:257–258 | "In his hand was Oathkeeper. He slid the sword from its scabbard and placed it in front of Lady Stoneheart." | The Brotherhood confiscates Oathkeeper as evidence of Lannister allegiance when judging Brienne.`

`catelyn-stark --PERCEIVED_AS--> oathkeeper (as traitor-weapon) | NEEDS_VOCAB: "Stoneheart NAMES the sword Oathbreaker / False Friend — she perceives it as treachery-forged; this is a named renaming act, not a simple PERCEIVED_AS of an artifact. Closest fit: REPUTED_AS with catelyn-stark as source, or a note-edge." | affc-brienne-08:297 | "No, she says. Call it Oathbreaker, she says. It was made for treachery and murder. She names it False Friend." | Load-bearing: Stoneheart's renaming of the sword is the pivot of the tribunal.`

---

### C. STRANGER (Sandor's horse)

`sandor-clegane --OWNS--> stranger-horse | tier-1 | affc-brienne-06:191 | "You may have seen a big black stallion in our stables. That was his warhorse, Stranger." | Elder Brother's direct identification.`

`stranger-horse --HELD_BY--> elder-brother-quiet-isle | tier-1 | affc-brienne-06:191 | "A blasphemous name. We prefer to call him Driftwood, as he was found beside the river." | The Quiet Isle keeps the horse; consequential because Brienne saw him earlier in the stable and didn't understand the implication.`

---

### D. PLACE-ANCHORING — LOCATED_AT / REGION_OF / TRAVELS_TO

**The Whispers**

`whispers --LOCATED_AT--> crackclaw-point | tier-1 | affc-brienne-03:344–345 | "Puts me in mind o' Crackclaw Point. Up north o' here, 'tis a wild land o' hills and bogs [...] The Whispers." | Nimble Dick places it explicitly.`

`fight-at-the-whispers --LOCATED_AT--> whispers | tier-1 | affc-brienne-04:173–174 | "The castle came upon them without warning [...] 'The Whispers,' said Nimble Dick." | The Whispers is where Brienne kills Pyg, Timeon, and Shagwell.`

`brienne-tarth --TRAVELS_TO--> whispers | tier-1 | affc-brienne-04:173 | "The castle came upon them without warning. [...] 'The Whispers,' said Nimble Dick." | Brienne's journey to the Whispers seeking Sansa/Dontos.`

**Quiet Isle**

`quiet-isle --REGION_OF--> riverlands | tier-1 | affc-brienne-06:12 | "Saltpans is just across the water," said Septon Meribald, pointing north across the bay." | Places Quiet Isle in relation to Saltpans at the bay mouth; the Trident context locks it to the riverlands.`

`sandor-clegane --DIED_AT--> quiet-isle | tier-1 | affc-brienne-06:185–191 | "He begged me for the gift of mercy [...] The Hound died there, in my arms." | Elder Brother buries Sandor at the Quiet Isle.`

`sandor-clegane --BURIED_AT--> quiet-isle | tier-1 | affc-brienne-06:185 | "I buried him myself. I can tell you where his grave lies, if you wish. I covered him with stones to keep the carrion eaters from digging up his flesh." | Direct statement.`

`elder-brother-quiet-isle --HEALS--> sandor-clegane | tier-2 | affc-brienne-06:187 | "I bathed his fevered brow with river water, and gave him wine to drink and a poultice for his wound, but my efforts were too little and too late." | Elder Brother attempted to heal Sandor before he died; the attempt failed.`

> NOTE: baseline says `elder-brother-quiet-isle HEALS brienne` — this is the complementary edge (heals Sandor, too late).

**Saltpans**

`raid-on-saltpans --LOCATED_AT--> saltpans | tier-1 | affc-brienne-06:77 | "At Saltpans, they had found only death and desolation." | Confirms Brienne's witness of the aftermath.`

`rorge --AGENT_IN--> raid-on-saltpans | tier-1 | affc-brienne-08:215 | "It was Rorge I killed. He took the helm from Clegane's grave, and you stole it off his corpse." | Brienne names Rorge explicitly as the Saltpans raider.`

`biter --AGENT_IN--> raid-on-saltpans | tier-2 | raid-on-saltpans (wiki) | (wiki: "One band of fleeing Brave Companions is led by Rorge, who has his constant companion Biter at his side.") | Biter accompanied Rorge; wiki-sourced.`

`brave-companions --AGENT_IN--> raid-on-saltpans | tier-1 | raid-on-saltpans (wiki) | (wiki: "Some time before the Brave Companions leave Harrenhal [...] One band of fleeing Brave Companions is led by Rorge") | The raiding party is a Brave Companions remnant.`

**Crossroads Inn (the inn-fight)**

`brienne-tarth --TRAVELS_TO--> inn-at-the-crossroads | tier-1 | affc-brienne-07:71–77 | "The inn's yard was a sea of brown mud [...] The clang of steel was louder here" | Brienne arrives at the inn, meets Willow and Gendry.`

`inn-fight-at-crossroads --LOCATED_AT--> inn-at-the-crossroads | tier-1 | affc-brienne-07:271–293 | "She stepped out into the rain, Oathkeeper in hand." | The fight with Rorge/Biter takes place in the inn yard.`

**Maidenpool**

`randyll-tarly --RULES--> maidenpool | tier-1 | affc-brienne-03:45 | "This Tarly, he's a hard man, but a braver lord than Mooton [...] Tarly hunted down the worst o' them." | The farmer confirms Tarly's de facto rule at Maidenpool.`

`brienne-tarth --TRAVELS_TO--> maidenpool | tier-1 | affc-brienne-03 (the chapter) | (entire chapter set at Maidenpool) | Brienne's visit to Maidenpool is a structural stop in the arc.`

**Crackclaw Point**

`crackclaw-point --REGION_OF--> riverlands | tier-1 | affc-brienne-03:341 | "Crackclaw Point. Up north o' here, 'tis a wild land o' hills and bogs." | Nimble Dick's description places it north of Maidenpool, eastern riverlands.`

`brienne-tarth --TRAVELS_TO--> crackclaw-point | tier-1 | affc-brienne-04:102–103 | "That look a bloody ruin t' you? That's the Dyre Den, where old Lord Brune keeps his seat. Road ends here, though." | Brienne journeys deep into Crackclaw following Nimble Dick.`

---

### E. CHARACTER RELATIONSHIP EDGES — new or missing wires

**Gendry**

`gendry --KILLS--> biter | tier-1 | affc-brienne-08:53 | "He's dead. Gendry shoved a spearpoint through the back of his neck." | Long Jeyne's direct statement to Brienne.`

> NOTE: baseline says `gendry KILLS biter (exists)` — confirm this edge is already in graph before proposing. This may be a baseline edge.

`gendry --MEMBER_OF--> brotherhood-without-banners | tier-2 | affc-brienne-08:71 | "M'lady means for you to answer for your crimes." (Gendry speaks as a Brotherhood member leading Brienne to Stoneheart) | Gendry is embedded with the Brotherhood at the crossroads inn and helps deliver Brienne to Stoneheart. His membership is implicit but strongly evidenced.`

`gendry --COMPANION_OF--> willow-heddle | tier-2 | affc-brienne-07:135–137 | "No," said the boy smith. "Yes," said the girl Willow. They glared at one another." | Gendry and Willow are co-custodians of the orphaned children at the inn; close working companions.`

**Septon Meribald**

`meribald --TRAVELS_TO--> quiet-isle | tier-1 | affc-brienne-06:37 | "Septon Meribald. It has been nigh upon a year. You are welcome." | Elder Brother's greeting confirms Meribald is a regular visitor.`

`meribald --COMPANION_OF--> brienne-tarth | tier-1 | affc-brienne-05:173–174 | "It was a queer procession: Ser Hyle on a chestnut courser and Brienne on her tall grey mare, Podrick Payne astride his swayback stot, and Septon Meribald walking beside them." | Meribald accompanies Brienne's party from Maidenpool to Saltpans and the crossroads inn.`

`meribald --GUEST_OF--> willow-heddle | tier-1 | affc-brienne-07:59 | "When Masha Heddle owned this inn she always had a honey cake for me. Sometimes she even let me have a bed." | Meribald identifies the inn as a longstanding place of hospitality for him; also confirmed when he feeds the children there.`

`dog-meribald --COMPANION_OF--> meribald | tier-1 | affc-brienne-05:239 | "Dog keeps me safe upon the roads, even in such trying times as these. Neither wolf nor outlaw dare molest me when Dog is at my side." | The relationship is stated explicitly; Dog is described as belonging to himself, but travels with Meribald.`

**Hyle Hunt**

`hyle-hunt --COMPANION_OF--> brienne-tarth | tier-2 | affc-brienne-05:173 | "It was a queer procession: Ser Hyle on a chestnut courser and Brienne on her tall grey mare, Podrick Payne astride his swayback stot." | Hyle joins the party from Maidenpool onward.`

`hyle-hunt --VICTIM_IN--> brienne-brought-before-lady-stoneheart | tier-1 | affc-brienne-08:277–279 | "Hyle Hunt had been beaten so badly that his face was swollen almost beyond recognition. He stumbled as they shoved him, and almost fell." | Hyle is one of the three captives judged by Stoneheart.`

**Thoros of Myr**

`thoros-of-myr --COMPANION_OF--> brienne-tarth | tier-2 | affc-brienne-08:155–174 | "I am Thoros, late of Myr [...] Their supper in the septry was as strange a meal as Brienne had ever eaten" — no wait, this is the cave scene. | Thoros tends Brienne in the cave and acts as her informal advocate with the Brotherhood.`

`thoros-of-myr --MEMBER_OF--> brotherhood-without-banners | tier-1 | affc-brienne-08:158–160 | "We were king's men when we began [...] I only know the road is dark." | Self-identification with the Brotherhood; baseline may already wire this.`

**Elder Brother → Sandor causal chain**

`elder-brother-quiet-isle --INFORMS--> brienne-tarth | tier-1 | affc-brienne-06:169–191 | "Your Dornishman did not lie [...] but I fear you did not understand him. [...] The man you hunt is dead." | The Elder Brother corrects Brienne on Arya vs Sansa, the Hound's death, and the helm's history — pivoting the whole arc.`

`elder-brother-quiet-isle --INFORMS--> brienne-tarth (re: arya-stark) | tier-1 | affc-brienne-06:169 | "You are chasing the wrong wolf, my lady. Eddard Stark had two daughters. It was the other one that Sandor Clegane made off with, the younger one." | The Arya revelation.`

**Catelyn-Stark / Lady Stoneheart**

`catelyn-stark --COMMANDS_IN--> brienne-brought-before-lady-stoneheart | tier-1 | affc-brienne-08:331 | "Lady Stoneheart lowered her hood and unwound the grey wool scarf from her face." (and her "Hang them" pronouncement) | Stoneheart presides over and commands the hanging verdict.`

`catelyn-stark --VOWS_TO--> brienne-tarth | tier-2 | affc-brienne-01:283 | "Kneeling between the bed and wall, she held the blade and said a silent prayer [...] He trusted me with his sword. He trusted me with his honor." | This is Brienne's vow *to* Catelyn, but the reciprocal framing in the arc is that Catelyn's ghost/Stoneheart holds Brienne to a vow. Reverse: `brienne-tarth --VOWS_TO--> catelyn-stark` (may be in baseline — check).`

`catelyn-stark --SUSPECTED_OF--> brienne-tarth (betrayal) | tier-1 | affc-brienne-08:297–299 | "No, she says. Call it Oathbreaker, she says. It was made for treachery and murder. She names it False Friend. Like you." | Stoneheart accuses Brienne of betrayal — the SUSPECTED_OF edge type fits (unproven actor→suspected act).`

**Nimble Dick Crabb**

`nimble-dick-crabb --AGENT_IN--> fight-at-the-whispers | tier-1 | affc-brienne-04:253 | "She knew that nose. She knew those eyes. Pyg, his friends had called him." (and Shagwell kills Crabb immediately) | Crabb is killed by Shagwell at the Whispers — first casualty of the fight.`

`nimble-dick-crabb --KILLED_BY--> shagwell | tier-1 | affc-brienne-04:255 | "Shagwell dropped from the weirwood, braying laughter. [...] Shagwell whirled the spiked ball once around his head and brought it down in the middle of Crabb's face. There was a sickening crunch." | Direct text.`

`nimble-dick-crabb --BURIED_AT--> whispers | tier-1 | affc-brienne-04:346 | "Brienne sheathed Oathkeeper, gathered up Dick Crabb, and carried him to the hole. [...] 'He was a Crabb. This is his place.'" | Brienne buries Crabb under the weirwood at the Whispers.`

**Brienne's shield**

`brienne-tarth --OWNS--> lothston-shield | tier-2 | affc-brienne-01:79 | "The shield was the one Ser Jaime had taken from the armory at Harrenhal. Brienne had found it in the stables with her mare." | Jaime provisioned Brienne with the Lothston shield from Harrenhal's armory. (If `lothston-shield` doesn't exist as a node, the edge can reference the description; this is a lower-priority object proposal.)` 

> NEEDS_VOCAB candidate for shields that don't kill anyone — `GIFTED_TO` would work:
`lothston-shield --GIFTED_TO--> brienne-tarth | tier-2 | affc-brienne-01:79 | "The shield was the one Ser Jaime had taken from the armory at Harrenhal. Brienne had found it in the stables with her mare, along with much else." | Jaime provisioned it, though Brienne notes she "lost mine own shield" and this replaced it. GIFTED_TO fits intent.`

---

### F. DESCRIPTIVE / REPUTED_AS EDGES

`brienne-tarth --REPUTED_AS--> maid-of-tarth | tier-1 | affc-brienne-03:93 | "This is Brienne the Beauty, the Maid of Tarth, who slew King Renly and half his Rainbow Guard." | Hyle Hunt names her epithets in public. Reputation-node: if "maid-of-tarth" is just an alias, attach as REPUTED_AS with the contemptuous framing.`

`brienne-tarth --PERCEIVED_AS--> renly-baratheon-lookalike | NEEDS_VOCAB: the Gendry=Renly resemblance is a cross-character descriptive observation. No edge type fits a visual resemblance. Flag for harvest instead.`

---

## HARVEST

> Wide-bar captures — chapter:line / kind / note

**Food / hospitality / starvation**
- affc-brienne-01:53 / food / Ser Creighton shares trout grilled over campfire + Brienne eats; she pays for goat supper at Old Stone Bridge inn
- affc-brienne-01:107 / food / breakfast: roast squirrel, acorn paste, pickles (hedge knights' camp)
- affc-brienne-01:259 / food / goat roasting on spit at Old Stone Bridge inn, Brienne orders for self + both hedge knights; drinks goat's milk not ale
- affc-brienne-02:111 / food / dwarf holy brother offers Brienne his seat at Seven Swords; she buys him hot crab stew + fresh bread + wine; he eats her leftovers too; food as hospitality
- affc-brienne-02:162–163 / food / Stinking Goose: greasy wine with hair floating in it
- affc-brienne-03:139 / food / Lord Tarly does justice in fishmarket; a baker fined 50 stags for mixing sawdust in flour (food adulteration as crime)
- affc-brienne-04:93–94 / food / cold wet camp without fire: Brienne gnaws salt beef strip while Nimble Dick tells stories
- affc-brienne-05:175 / food-list / Meribald's donkey carries: seeds/nuts/dried fruit, oaten porridge, flour, barley bread, three wheels of yellow cheese, salt cod, salt mutton, salt, onions, carrots, turnips, two sacks of beans, four of barley, nine sacks of oranges — comprehensive smallfolk relief supply
- affc-brienne-05:271–273 / food / cold camp in dunes: breakfast of salt cod + orange slices; Pod finds no driftwood, mudflats at low tide
- affc-brienne-06:140–141 / food / Quiet Isle supper: crusty bread still warm, fresh-churned butter, honey from septry hives, thick crab-mussel-fish stew — best meal Brienne has eaten; the brothers make mead + ale + cider
- affc-brienne-07:95 / food / crossroads inn: only horse meat to eat; no whores; children are hungry
- affc-brienne-07:160–161 / food / Meribald's last oranges distributed to inn children; he grieves their absence till spring; boy who never had an orange
- affc-brienne-08:179–180 / food / cave food: cold greasy stew, hard bread, harder cheese; Brienne says never eaten anything half so good (starvation context)
- affc-brienne-08:91 / food / onion broth with carrot given to fever-Brienne; she chokes on the carrot

**Physical descriptions (persons)**
- affc-brienne-01:33–39 / description / Brienne's self-description: broad shoulders, broader hips, long legs, thick arms, more muscle than bosom, big hands, enormous feet, freckled horsey face, teeth too big for her mouth, brittle yellow hair the color of dirty straw
- affc-brienne-01:49–51 / description / Ser Creighton Longbough: big belly straining doeskin jerkin, shaggy untrimmed beard old-gold color; Ser Illifer the Penniless: sixty+, pinched narrow face, patched roughspun mantle, rust-spotted mail
- affc-brienne-01:183–184 / description / Ser Shadrich "the Mad Mouse": wiry, fox-faced, sharp nose, shock of orange hair, rangy chestnut courser, no more than five foot two; cocksure manner
- affc-brienne-03:107–108 / description / Ser Hyle Hunt: shaggy brown hair, hazel eyes, little scar by left ear, cleft chin, crooked nose, plain honest face (that Brienne later revises)
- affc-brienne-05:179 / description / Septon Meribald: seamed windburnt face, thick grey hair, wrinkles at eye corners, six feet tall but stooped, huge leathery hands with red knuckles and dirt under nails, biggest feet Brienne has ever seen — bare and black and hard as horn; hasn't worn a shoe in twenty years
- affc-brienne-05:239 / description / Meribald's Dog: huge shaggy creature, ten stone of dog at least, friendly; knows the mudflat road as well as Meribald
- affc-brienne-06:61 / description / Stranger/Driftwood: big black stallion, kicking at stall door, trumpeting; Brother Gillam lost an ear to the horse; kicked Brother Rawney and broke his shinbone
- affc-brienne-06:109–110 / description / Elder Brother: not elder at all — straight, tall, vigorous; large square head, shrewd eyes, veined red nose, stubbly scalp and jaw; "looks more like a man made to break bones than to heal one"
- affc-brienne-07:119–121 / description / Gendry: black hair mop falling past ears, dark stubble, heavy shoulders and muscular right arm, bare chest under leather apron; blue eyes brimming with anger — Brienne notes he resembles young Renly but squarer jaw, bushier brows, brawnier (Robert's build, not Renly's)
- affc-brienne-08:97 / description / Lem Lemoncloak: brawny, broken nose healed badly, brown hair, bearded; stained yellow cloak; wears the Hound's helm

**Physical descriptions (objects/places)**
- affc-brienne-01:283 / description / Oathkeeper drawn at candlelight: "Gold glimmered yellow in the candlelight and rubies smoldered red. When she slid Oathkeeper from the ornate scabbard, Brienne's breath caught in her throat. Black and red the ripples ran, deep within the steel. Valyrian steel, spell-forged." — premier physical description of Oathkeeper in Brienne's arc
- affc-brienne-02:41 / description / Brienne's replacement shield: described as painted scene — castle in autumn wood with fox, sparrows, and shadow of boar in foliage (not heraldic, pictorial)
- affc-brienne-04:173 / description / The Whispers: ancient tumbledown castle, abandoned and overgrown at cliff's edge; triangular footprint with square towers at corners; rotted gates; portcullis teeth sunk deep in mud; forest growing up from foundations; weirwood in the yard with dark red leaves; sound of waves through sea-caves beneath creates "whispering"
- affc-brienne-06:107 / description / Elder Brother's cave dwelling ("Hermit's Hole"): woolen carpets, tapestried walls, tall beeswax candles, driftwood furniture all polished gold in candlelight — driftwood table, settle, chest, bookcases, chairs; all cunningly joined
- affc-brienne-07:51–55 / description / Inn name-history per Meribald: Two Crowns (Jaehaerys) → Bellringer Inn → Clanking Dragon (Long Jon Heddle's iron three-headed dragon sign, torn down by Lord Darry for resemblance to Daemon Blackfyre's sigil) → River Inn (when Trident ran beneath back door and guests could fish from windows) → crossroads inn
- affc-brienne-07:74–76 / description / Crossroads inn physical: three stories, white stone walls, turrets and chimneys, south wing on heavy wooden pilings above dead ground, thatch-roofed stable and bell tower on north side, surrounded by low wall of broken white stones overgrown with moss
- affc-brienne-08:239 / description / Lady Stoneheart's appearance in the cave: grey-cloaked and hooded, bronze circlet with iron swords (crown), eyes "glimmering under her hood" — then revealed: dry brittle white hair, mottled green-grey brow with brown blooms of decay, flesh clinging in ragged strips from eyes to jaw, some rips crusted with blood, others gaping to show skull beneath

**Memorable quotes (verbatim load-bearing)**
- affc-brienne-01:283 / quote / "You'll be defending Ned Stark's daughter with Ned Stark's own steel." — Jaime to Brienne (recalled in her prayer); the founding promise of her mission
- affc-brienne-04:55–56 / quote / Brienne on honor: "'The point is honor,' she said." — response to Nimble Dick mocking Ser Galladon for not using his magic sword; concise statement of her code
- affc-brienne-05:293–305 / quote / Septon Meribald's "broken men" sermon: extended set-piece on war, desertion, and what it means to break. Load-bearing passage for ASOIAF's treatment of smallfolk in wartime. Chapter line 293–305.
- affc-brienne-06:185 / quote / "The man who raped and killed at Saltpans was not Sandor Clegane, though he may be as dangerous. The riverlands are full of such scavengers. I will not call them wolves. Wolves are nobler than that . . . and so are dogs, I think." — Elder Brother; key reversal quote
- affc-brienne-07:293 / quote / Brienne kills Rorge: "she leapt to meet his rush, both hands on her sword hilt. His headlong charge brought him right onto her point, and Oathkeeper punched through cloth and mail and leather and more cloth, deep into his bowels and out his back, rasping as it scraped along his spine." — the kill with Oathkeeper; full physical precision
- affc-brienne-07:293 / quote / "'Sapphires,' she whispered at him, as she gave her blade a hard twist that made him shudder." — the callback to Jaime's gambit that saved her from the Brave Companions; she says it to Rorge as he dies behind the Hound's helm
- affc-brienne-08:307 / quote / Biter eating her: "Biter's mouth tore free, full of blood and flesh. He spat, grinned, and sank his pointed teeth into her flesh again. This time he chewed and swallowed. He is eating me, she realized" — the horror of the Biter attack; precedes Gendry's kill
- affc-brienne-08:327–329 / quote / Stoneheart's ultimatum: "'She wants her son alive, or the men who killed him dead [...] All she asks from you is Jaime Lannister.'" — the choice that ends the chapter

**Foreshadowing / Chekhov's guns**
- affc-brienne-01:99–101 / foreshadowing / Brienne "never slept easily in the presence of men. Even in Lord Renly's camps, the risk of rape was always there." — the Highgarden wager not yet explained; sets up the Highgarden backstory reveal in brienne-03
- affc-brienne-06:79 / foreshadowing / Elder Brother mentions "six rubies found" from the Trident (Rhaegar's breastplate), "all waiting for the seventh" — long-standing Chekhov's gun in the series
- affc-brienne-06:191–192 / foreshadowing / "I fear he has his former master's nature." (re: Stranger/Driftwood) — Sandor's horse embodies his violence; the Elder Brother's description foreshadows Sandor's survival (the horse was "found beside the river," not buried)
- affc-brienne-07:265 / foreshadowing / Brienne glimpses "an iron snout and rows of steel teeth, snarling" on the lead rider in the lightning flash — the visual realization of the Hound's helm on Rorge, building to the fight
- affc-brienne-08:97 / foreshadowing / Lem wears the Hound's helm — "From his shoulders rose a steel dog's head, its teeth bared in a snarl." — the helm passes from Rorge to Lem; structural callback to Brienne's fight scene

**Hospitality violations**
- affc-brienne-08:103–105 / guest-right violation / Long Jeyne tells Brienne: "Guest right don't mean so much as it used to [...] Not since m'lady come back from the wedding. Some o' them swinging down by the river figured they was guests too." — explicit invocation and dismissal of guest right by the Brotherhood under Stoneheart; the inn-as-guest-right site being violated echoes Red Wedding
- affc-brienne-07:77–80 / hospitality / Saltpans castle bars its gates to Brienne, Meribald, etc.: a woman shouts down that they want no strangers; the castle holdfast fails its hospitality duty as it had during the raid (Ser Quincy Cox analogy)

**Brotherhood/Stoneheart vengeance campaign**
- affc-brienne-07:11–35 / description / corpses strung in trees along the road to the crossroads: arms/badges listed — axes (Byrch/Cerwyn), arrows (Norridge/Sarsfield), salmon (Mooton), pine tree (Mollen), oak leaf (Oakheart), beetles (Bettley), bantams (Swyft), boar's head (Vikary), tridents (Condon/Manderly); salt packed in mouths as reference to Saltpans raid — full enumeration for the vengeance-hangings
- affc-brienne-08:197–200 / character / Thoros of Myr's self-assessment: "I remember justice. It had a pleasant taste. [...] Justice was what we were about when Beric led us, or so we told ourselves. We were king's men, knights, and heroes . . . but some knights are dark and full of terror, my lady. War makes monsters of us all." — Thoros's explicit acknowledgment of the Brotherhood's moral collapse under Stoneheart

---

## SUMMARY

Proposed 1 high-priority new artifact node (`hound-helm`) and 1 potential creature node (`stranger-horse`), plus ~35 edge proposals covering: the helm's full chain of custody (Sandor → Elder Brother's error → Rorge → Brienne kill → Lem claim), Oathkeeper's WIELDED_IN wires at the Whispers fight and inn fight, place-anchoring for Whispers/Crackclaw/Quiet Isle/Maidenpool/Saltpans, new character relationship edges for Gendry/Meribald/Hyle/Thoros/Nimble Dick, and the Saltpans misattribution engine (Rorge AGENT_IN, Sandor REPUTED_AS, Tarly DECEIVES). Harvest section captures 25+ food/description/quote/foreshadowing pointers for later attachment passes.
