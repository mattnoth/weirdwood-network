# Lens 3 — Descriptive / Quote / Object Depth
## Blackwater enrichment dip (S138)
Generated: 2026-06-23

---

## DEDUP STATUS CONFIRMED
- `wildfire` node EXISTS (`graph/nodes/artifacts/wildfire.node.md`) — substantial wiki prose. No book-level WIELDED_IN edge or Blackwater-specific book quotes.
- `fury`, `black-betha`, `lady-marya`, `queen-alysanne`, `dragonsbane`, `swordfish-ship`, `pride-of-driftmark`, `kingslander`, `white-hart`, `stag-of-the-sea`, `lord-steffon`, `sceptre`, `harridan`, `devotion`, `piety`, `prayer`, `bold-laughter`, `courageous`, `cat-galley`, `red-raven-ship`, `sea-demon`, `lady-harra`, `brightfish`, `dogs-nose`, `seahorse`, `godsgrace-ship` — all exist in `graph/nodes/artifacts/`. **None have any WIELDED_IN edges** (Edges sections are empty).
- `ice` node EXISTS (`graph/nodes/artifacts/ice.node.md`) — wiki-sourced, empty Edges.
- No chain-boom node exists.
- `wildfire-plot` is the Aerys/283 AC node — must NOT be used here.

---

## PROPOSED NODES

### NODE-1: `blackwater-chain-boom`
- **slug:** `blackwater-chain-boom`
- **name:** "The Chain Boom of the Blackwater"
- **type:** `object.artifact`
- **identity:** A massive iron chain stretched across the mouth of the Blackwater Rush, commissioned by Tyrion Lannister to trap Stannis's fleet. Raised by winches operated from twin stone towers on opposite banks; the decisive tactical weapon of the battle.
- **Home edge:** `blackwater-chain-boom WIELDED_IN battle-of-the-blackwater` | Tier 1 | ACOK Davos III line 57: "Something flashed down low where the dark water swirled around the base of the tower. It was sunlight on steel, and it told Davos Seaworth all he needed to know. A chain boom . . ."
- **Second edge:** `tyrion-lannister BUILT blackwater-chain-boom` | Tier 1 | ACOK Tyrion XIII line 27: "Bronn would have whipped the oxen into motion the moment Stannis's flagship passed under the Red Keep; the chain was ponderous heavy, and the great winches turned but slowly, creaking and rumbling."
- **Rationale:** No chain node exists. This is the decisive material object of the battle — it traps the fleet after wildfire spreads. Explicitly distinguishable from `wildfire` (separate mechanism, separate moment). Bronn is credited with the winch operation (earns "Ser Bronn of the Blackwater"), Tyrion with commissioning it.

### NODE-2: `song-gentle-mother`
- **slug:** `song-gentle-mother`
- **name:** "Gentle Mother (song)"
- **type:** `object.text`
- **identity:** A prayer-hymn to the Mother, one of the Seven. Sung by Sansa Stark under duress in her bedchamber during the Battle of the Blackwater, with Sandor Clegane's dagger at her throat.
- **Home edge:** `song-gentle-mother WIELDED_IN battle-of-the-blackwater` — NEEDS_VOCAB: no clean WIELDED_IN for songs; could use `DEPICTED_IN` or `SUBJECT_OF_PROPHECY` doesn't fit. **Best fit: attach as `## Quotes` on `sansa-stark` + `sandor-clegane` nodes; the song itself earns its own text node but its "use" edge is unclear from locked vocab.** Propose `song-gentle-mother ECHOES battle-of-the-blackwater` (thematic resonance — mercy vs carnage) as candidate edge. `ECHOES` is available.
- **Rationale:** The song is a distinct named cultural object with a verbatim text preserved in the chapter; its performance is the emotional hinge of Sansa-Sandor VII. "Gentle Mother, font of mercy" is 8 lines preserved in full.
- **chapter:line** ACOK Sansa VII lines 109–123 (full song text — see QUOTE ATTACHMENTS section).

---

## PROPOSED EDGES

### EDGE-1: Ships WIELDED_IN battle-of-the-blackwater (bulk)
Each ship node has an empty Edges section. These are all textually attested as fighting in or at the battle.

| SRC | TYPE | TGT | Tier | Chapter:line | Quote (verbatim) | Rationale |
|-----|------|-----|------|-------------|------------------|-----------|
| `fury` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :15 | "From her decks Stannis Baratheon had commanded the assault on Dragonstone sixteen years before, but this time he had chosen to ride with his army, trusting Fury and the command of his fleet to his wife's brother Ser Imry" | Stannis's fleet flagship; led the attack |
| `black-betha` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :11 | "Black Betha rode the flood tide, her sail cracking and snapping at each shift of wind." | Davos's flagship; POV ship for Davos III |
| `lady-marya` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :11 | "Wraith and Lady Marya sailed beside her, no more than twenty yards between their hulls." | Allard's ship, directly named as fighting alongside Black Betha |
| `queen-alysanne` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :91 | "Queen Alysanne was locked between Lady of Silk and Lady's Shame, her crew fighting the boarders rail-to-rail." | Named fighting ship; destroyed by wildfire |
| `dragonsbane` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :91 | "Stag of the Sea split one of Joffrey's galleys clean in two, but Dog's Nose was afire and Queen Alysanne was locked between Lady of Silk and Lady's Shame, her crew fighting the boarders rail-to-rail." / Dragonsbane: line :121 "the captain of Dragonsbane had driven her between two quays, ripping out her bottom" | Named in battle; used as foot of the ship-bridge |
| `swordfish-ship` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :125 | "It was Swordfish, her two banks of oars lifting and falling. She had never brought down her sails, and some burning pitch had caught in her rigging." | Triggers the wildfire explosion; pivotal role |
| `pride-of-driftmark` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :121 | "Lord Velaryon's Pride of Driftmark was trying to turn, but the demon ran a lazy green finger across her silvery oars and they flared up like so many tapers." | Named; burned in wildfire |
| `stag-of-the-sea` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :91 | "Stag of the Sea split one of Joffrey's galleys clean in two" | Named in combat |
| `lord-steffon` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :47 | "Fury herself would center the first line of battle, flanked by the Lord Steffon and the Stag of the Sea" | Named in first battle line |
| `kingslander` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :93 | "Directly ahead, Davos saw the enemy's Kingslander drive between Faithful and Sceptre." | Lannister ship named in combat action |
| `white-hart` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :115 | "Matthos's shout alerted him to the danger from port; one of the Lannister galleys was coming about to ram. 'Hard to starboard,' Davos shouted. His men used their oars to push free of the barge, while others turned the galley so her prow faced the onrushing White Hart." | Lannister ship named; boarded by Davos |
| `sceptre` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :93 | "Directly ahead, Davos saw the enemy's Kingslander drive between Faithful and Sceptre." | Named in combat; Stannis's fleet |
| `harridan` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :41 | "Harridan and Seahorse had slipped into their places now" | Named in formation |
| `devotion` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :85 | "Prayer landed two dozen yards upstream and Piety was slanting toward the bank" / Devotion named at :41, :75 "Bowmen on the roof of the northern tower were firing down at Prayer and Devotion." | Named in battle action |
| `piety` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :85 | "Prayer landed two dozen yards upstream and Piety was slanting toward the bank when the defenders came pounding down the riverside" | Named in combat |
| `prayer` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :87 | "Davos recognized the dog's-head helm of the Hound. A white cloak streamed from his shoulders as he rode his horse up the plank onto the deck of Prayer, hacking down anyone who blundered within reach." | Named; Sandor boards it |
| `bold-laughter` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :111 | "Another, not much smaller, found Bold Laughter. The Velaryon galley exploded like a child's toy dropped from a tower, spraying splinters as long as a man's arm." | Destroyed by trebuchet stone |
| `courageous` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :71 | "He could see smoke rising from three different spots on Dragonsbane, nearest the bank. By then a second flight was on its way, and arrows were falling as well" / Courageous: line :121 "Cat was taking on men from the fast-sinking Courageous." | Named as sinking |
| `cat-galley` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :121 | "Cat was taking on men from the fast-sinking Courageous." | Named in battle |
| `red-raven-ship` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :121 | "Red Raven, rammed, was slowly listing." | Named; damaged in battle |
| `sea-demon` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :47 | "On the port and starboard wings were the hundreds: Lady Harra, Brightfish, Laughing Lord, Sea Demon, Horned Honor, Ragged Jenna, Trident Three, Swift Sword, Princess Rhaenys, Dog's Nose, Sceptre, Faithful, Red Raven, Queen Alysanne, Cat, Courageous, and Dragonsbane." | Named in first battle line |
| `lady-harra` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :47 | "On the port and starboard wings were the hundreds: Lady Harra, Brightfish, Laughing Lord, Sea Demon..." | Named in first battle line |
| `dogs-nose` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :91 | "Dog's Nose was afire" | Named; destroyed |
| `seahorse` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :41 | "Harridan and Seahorse had slipped into their places now" | Named in formation |
| `godsgrace-ship` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :67 | "The boy's toys included the ponderous Godsgrace, he saw, the old slow Prince Aemon, the Lady of Silk and her sister Lady's Shame, Wildwind, Kingslander, White Hart, Lance, Seaflower." / Tyrion XIII line :9 "Fury, her proud bow smashed in by a boulder, was engaged with Godsgrace." | Named; engaged with Fury |

**WIELDED_IN note on `faithful`:** Named at Davos III :47 and :93 ("Faithful was rammed and was starting to list") — node exists as `faithful.node.md`. Add WIELDED_IN.

### EDGE-2: `wildfire` WIELDED_IN `battle-of-the-blackwater`
| SRC | TYPE | TGT | Tier | Chapter:line | Quote | Rationale |
|-----|------|-----|------|-------------|-------|-----------|
| `wildfire` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Tyrion XIII :13 | "The kiss of wildfire turned proud ships into funeral pyres and men into living torches." | The wildfire node has extensive wiki prose about the battle but NO book-text WIELDED_IN edge wiring it to the event. This is the key missing graph link. |

### EDGE-3: `ice` WIELDED_IN / `ilyn-payne` context at Blackwater
- `ice` is present in the Queen's Ballroom during the battle (Ilyn Payne carries it unsheathed).
- ACOK Sansa VI :115: "She had not even seen Ser Ilyn return to the hall, but suddenly there he was, striding from the shadows behind the dais as silent as a cat. He carried Ice unsheathed. Her father had always cleaned the blade in the godswood after he took a man's head, Sansa recalled, but Ser Ilyn was not so fastidious. There was blood drying on the rippling steel, the red already fading to brown."
- **Proposed edge:** `ice WIELDED_IN battle-of-the-blackwater` | Tier 1 | ACOK Sansa VI :115 (quote above) | Ice is present with drawn blood as a death-threat instrument during the battle — Cersei's last resort against the highborn women including Sansa. This is a direct causal participant role in the battle context.
- **Also:** `ilyn-payne AGENT_IN battle-of-the-blackwater` | Tier 1 | ACOK Sansa VI :11 "She could see it in the pale eyes of Ser Ilyn Payne, who stood by the back door still as stone" — he is stationed specifically for the battle endgame (kill the queen's guests if the city falls).

### EDGE-4: `blackwater-chain-boom` edges (from NODE-1 above, restated for clarity)
| SRC | TYPE | TGT | Tier | Chapter:line | Quote |
|-----|------|-----|------|-------------|-------|
| `blackwater-chain-boom` | WIELDED_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :57 | "Something flashed down low where the dark water swirled around the base of the tower. It was sunlight on steel, and it told Davos Seaworth all he needed to know. A chain boom . . . and yet they have not closed the river against us. Why?" |
| `tyrion-lannister` | BUILT | `blackwater-chain-boom` | Tier 1 | ACOK Tyrion XIII :27 | "Bronn would have whipped the oxen into motion the moment Stannis's flagship passed under the Red Keep; the chain was ponderous heavy, and the great winches turned but slowly, creaking and rumbling. The whole of the usurper's fleet would have passed by the time the first glimmer of metal could be seen beneath the water." |
| `bronn` | AGENT_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Tyrion XIII :27 | "Bronn would have whipped the oxen into motion the moment Stannis's flagship passed under the Red Keep" | (Bronn operates the chain winch — his defining role at Blackwater, earns knighthood as "Ser Bronn of the Blackwater") |

### EDGE-5: `garlan-tyrell` role edges
- Garlan wears Renly's armor at the battle; the "Renly's ghost" rout is confirmed (Sansa VII :141-145, Dontos speech). No node for the rout event yet (see baseline gap #5). Edge to PROPOSE once event node exists.
- Interim: `garlan-tyrell FIGHTS_IN battle-of-the-blackwater` | Tier 1 | ACOK Sansa VII :145 | "It was Lord Renly! Lord Renly in his green armor, with the fires shimmering off his golden antlers! Lord Renly with his tall spear in his hand! They say he killed Ser Guyard Morrigen himself in single combat, and a dozen other great knights as well."
  - NOTE: Dontos calls it "Lord Renly" but it is Garlan; the quote is Dontos's words about "Renly" — the actual Garlan identification comes from wiki/prior chapters. The quote is correct as Dontos speaking but references "Renly" (= Garlan in disguise). Use with care — best attached to `garlan-tyrell` node with note that Dontos attributes it to Renly.

### EDGE-6: `mandon-moore` role + `podrick-payne` KILLS edge
| SRC | TYPE | TGT | Tier | Chapter:line | Quote |
|-----|------|-----|------|-------------|-------|
| `mandon-moore` | ATTACKS | `tyrion-lannister` | Tier 1 | ACOK Tyrion XIV :67 | "The point slashed just beneath his eyes, and he felt its cold hard touch and then a blaze of pain." |
| `podrick-payne` | KILLS | `mandon-moore` | Tier 1 | ACOK Tyrion XV :141 | (Pod's voice confirms, Tyrion asks "Dead? You're, certain? Dead?" and Pod says "Drowned.") — best quote from Tyrion XIV :73: "Ser Mandon Moore vanished with a shout and a splash." |
| `mandon-moore` | FIGHTS_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Tyrion XIV :13 | "Ser Mandon Moore took the place to his right, flames shimmering against the white enamel of his armor, his dead eyes shining passionlessly through his helm." |
| `tyrion-lannister` | COMMANDS_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Tyrion XIII :87 | "This is your city Stannis means to sack, and that's your gate he's bringing down. So come with me and kill the son of a bitch!" |

### EDGE-7: `tyrion-lannister` AFFLICTED_BY — his wound/disfigurement
| SRC | TYPE | TGT | Tier | Chapter:line | Quote |
|-----|------|-----|------|-------------|-------|
| `tyrion-lannister` | AFFLICTED_BY | `battle-of-the-blackwater` | Tier 1 | ACOK Tyrion XV :95 | "The gash was long and crooked, starting a hair under his left eye and ending on the right side of his jaw. Three-quarters of his nose was gone, and a chunk of his lip." |

- NOTES: `AFFLICTED_BY` takes a disease/condition, not an event. Better framing: the wound is from Mandon Moore's attack during the battle. Propose instead: `tyrion-lannister VICTIM_IN battle-of-the-blackwater` | Tier 1 | same cite. (VICTIM_IN is available in vocab; "victim" here = recipient of violence, applicable).

### EDGE-8: Stannis fleet commanders
| SRC | TYPE | TGT | Tier | Chapter:line | Quote |
|-----|------|-----|------|-------------|-------|
| `imry-florent` | COMMANDS_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :13 | "Ser Imry had decreed that they would enter the river on oars alone, so as not to expose their sails to the scorpions and spitfires on the walls of King's Landing." |
| `davos-seaworth` | FIGHTS_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :99 | "Ramming speed!" Davos shouted." |
| `stannis-baratheon` | COMMANDS_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Tyrion XIII :21 | "He'd never had his brother Robert's thirst for battle. He would command from the rear, from the reserve, much as Lord Tywin Lannister was wont to do." |
| `sandor-clegane` | FIGHTS_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Davos III :87 | "Davos recognized the dog's-head helm of the Hound. A white cloak streamed from his shoulders as he rode his horse up the plank onto the deck of Prayer, hacking down anyone who blundered within reach." |
| `balon-swann` | FIGHTS_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Tyrion XIV :45 | "He raised his mace to point downriver. Bits of brain and bone clung to its head." |
| `sansa-stark` | WITNESS_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Sansa VII :59 | "The southern sky was aswirl with glowing, shifting colors, the reflections of the great fires that burned below." (Sansa witnesses from her bedchamber window) |
| `cersei-lannister` | WITNESS_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Sansa VI :47 | "The hulks have gone up, Y'Grace. The whole Blackwater's awash with wildfire. A hundred ships burning, maybe more." (Cersei in Maegor's Holdfast receiving battle reports) |
| `guyard-morrigen` | DIED_AT | `battle-of-the-blackwater` | Tier 1 | ACOK Sansa VII :145 | "They say he killed Ser Guyard Morrigen himself in single combat, and a dozen other great knights as well." (Garlan/Renly kills him) |
| `hallyne` | AGENT_IN | `battle-of-the-blackwater` | Tier 1 | ACOK Tyrion XIII :31 | "Hallyne said that sometimes the substance burned so hot that flesh melted like tallow." (Hallyne's guild supplies/manages the wildfire operation) |

---

## QUOTE ATTACHMENTS

### QA-1: Attach to `tyrion-lannister` — `## Quotes` — "Those are brave men…"
- **chapter:line:** ACOK Tyrion XIV :51
- **Verbatim:** "Those are brave men," he told Ser Balon in admiration. "Let's go kill them."
- **slot:** `## Quotes`

### QA-2: Attach to `tyrion-lannister` — `## Quotes` — battle-cry speech before sortie
- **chapter:line:** ACOK Tyrion XIII :87
- **Verbatim:** "You won't hear me shout out Joffrey's name," he told them. "You won't hear me yell for Casterly Rock either. This is your city Stannis means to sack, and that's your gate he's bringing down. So come with me and kill the son of a bitch!"
- **slot:** `## Quotes`

### QA-3: Attach to `sandor-clegane` — `## Quotes` — refusal / water/wine
- **chapter:line:** ACOK Tyrion XIII :71
- **Verbatim:** "Bugger the King's Hand." Where the Hound's face was not sticky with blood, it was pale as milk. "Someone bring me a drink." A gold cloak officer handed him a cup. Clegane took a swallow, spit it out, flung the cup away. "Water? Fuck your water. Bring me wine."
- **slot:** `## Quotes`

### QA-4: Attach to `sandor-clegane` — `## Quotes` — "I only know who's lost. Me."
- **chapter:line:** ACOK Sansa VII :73
- **Verbatim:** The Hound laughed. "I only know who's lost. Me."
- **slot:** `## Quotes`

### QA-5: Attach to `sansa-stark` — `## Quotes` — "Gentle Mother" song text (full)
- **chapter:line:** ACOK Sansa VII :109–123
- **Verbatim:**
  > Gentle Mother, font of mercy,
  > save our sons from war, we pray,
  > stay the swords and stay the arrows,
  > let them know a better day.
  > Gentle Mother, strength of women,
  > help our daughters through this fray,
  > soothe the wrath and tame the fury,
  > teach us all a kinder way.
- **slot:** `## Quotes` on `sansa-stark` AND `song-gentle-mother` node (if created)

### QA-6: Attach to `cersei-lannister` — `## Quotes` — Ilyn Payne / "not suffer him to judge me"
- **chapter:line:** ACOK Sansa VI :119
- **Verbatim:** "He's here for us, he says," the queen said. "Stannis may take the city and he may take the throne, but I will not suffer him to judge me. I do not mean for him to have us alive."
- **slot:** `## Quotes`

### QA-7: Attach to `cersei-lannister` — `## Quotes` — the tears/weapons speech
- **chapter:line:** ACOK Sansa VI :23
- **Verbatim:** "Tears," she said scornfully to Sansa as the woman was led from the hall. "The woman's weapon, my lady mother used to call them. The man's weapon is a sword. And that tells us all you need to know, doesn't it?"
- **slot:** `## Quotes`

### QA-8: Attach to `cersei-lannister` — `## Quotes` — seducing Stannis's horse
- **chapter:line:** ACOK Sansa VI :43
- **Verbatim:** "Were it anyone else outside the gates, I might hope to beguile him. But this is Stannis Baratheon. I'd have a better chance of seducing his horse."
- **slot:** `## Quotes`

### QA-9: Attach to `wildfire` — book-quote edge evidence — wildfire-as-demon
- **chapter:line:** ACOK Davos III :137
- **Verbatim:** "Fifty feet high, a swirling demon of green flame danced upon the river. It had a dozen hands, in each a whip, and whatever they touched burst into fire."
- **slot:** `## Quotes` on `wildfire` node (augments existing wiki quotes with Tier-1 book provenance)

### QA-10: Attach to `wildfire` — "Like dragonfire" / Aegon comparison
- **chapter:line:** ACOK Tyrion XIII :15
- **Verbatim:** "The low clouds caught the color of the burning river and roofed the sky in shades of shifting green, eerily beautiful. A terrible beauty. Like dragonfire. Tyrion wondered if Aegon the Conqueror had felt like this as he flew above his Field of Fire."
- **slot:** `## Quotes` on `wildfire` node (book-text Tier-1 cite; upgrades wiki's description of wildfire appearance at battle)

### QA-11: Attach to `tyrion-lannister` — `## Quotes` — the battle-fever passage
- **chapter:line:** ACOK Tyrion XIV :39
- **Verbatim:** "The battle fever. He had never thought to experience it himself, though Jaime had told him of it often enough. How time seemed to blur and slow and even stop, how the past and the future vanished until there was nothing but the instant, how fear fled, and thought fled, and even your body."
- **slot:** `## Quotes`

### QA-12: Attach to `tyrion-lannister` — `## Quotes` — wound reveal
- **chapter:line:** ACOK Tyrion XV :95
- **Verbatim:** "The gash was long and crooked, starting a hair under his left eye and ending on the right side of his jaw. Three-quarters of his nose was gone, and a chunk of his lip."
- **slot:** `## Quotes`

### QA-13: Attach to `mandon-moore` — `## Quotes` — "dead empty eyes" physical description
- **chapter:line:** ACOK Tyrion XIV :67
- **Verbatim:** "There on the deck of the next ship, across a widening gulf of black water, stood Ser Mandon Moore, a hand extended. Yellow and green fire shone against the white of his armor, and his lobstered gauntlet was sticky with blood"
- **slot:** `## Quotes`

### QA-14: Attach to `battle-of-the-blackwater` (hub) — `## Quotes` — wildfire wall from Sansa's window
- **chapter:line:** ACOK Sansa VII :59
- **Verbatim:** "The southern sky was aswirl with glowing, shifting colors, the reflections of the great fires that burned below. Baleful green tides moved against the bellies of the clouds, and pools of orange light spread out across the heavens. The reds and yellows of common flame warred against the emeralds and jades of wildfire, each color flaring and then fading, birthing armies of short-lived shadows to die again an instant later."
- **slot:** `## Quotes` on hub — Sansa's visual perspective from Maegor's; the clearest "civilian witness" description in the text

### QA-15: Attach to `blackwater-chain-boom` (NODE-1) — raise moment
- **chapter:line:** ACOK Davos III :145
- **Verbatim:** "The chain. Gods save us, they've raised the chain."
- **slot:** `## Quotes` (load-bearing: the moment of recognition)
- **Second quote same node:** ACOK Davos III :147: "Where the river broadened out into Blackwater Bay, the boom stretched taut, a bare two or three feet above the water. Already a dozen galleys had crashed into it, and the current was pushing others against them."

### QA-16: Attach to `sandor-clegane` — physical description during battle
- **chapter:line:** ACOK Tyrion XIII :53
- **Verbatim:** "A shadow detached itself from the shadow of the wall, to become a tall man in dark grey armor. Sandor Clegane wrenched off his helm with both hands and let it fall to the ground. The steel was scorched and dented, the left ear of the snarling hound sheared off. A gash above one eye had sent a wash of blood down across the Hound's old burn scars, masking half his face."
- **slot:** `## Quotes` (clothing/armor description; distinctive helmet detail — ear sheared off)

### QA-17: Attach to `sandor-clegane` — bedchamber scene physical appearance
- **chapter:line:** ACOK Sansa VII :67
- **Verbatim:** "Outside, a swirling lance of jade light spit at the stars, filling the room with green glare. She saw him for a moment, all black and green, the blood on his face dark as tar, his eyes glowing like a dog's in the sudden glare. Then the light faded and he was only a hulking darkness in a stained white cloak."
- **slot:** `## Quotes` (visual description; the white cloak stained by battle = his final night in King's Landing)

### QA-18: Attach to `tyrion-lannister` — Tyrion's horse and armor description before sortie
- **chapter:line:** ACOK Tyrion XIII :83
- **Verbatim:** "His big red stallion wore crinet and chamfron. Crimson silk draped his hindquarters, over a coat of mail. The high saddle was gilded. Podrik Payne handed up helm and shield, heavy oak emblazoned with a golden hand on red, surrounded by small golden lions."
- **slot:** `## Quotes` (physical description — armor/mount at Blackwater)

### QA-19: Attach to `garlan-tyrell` — "Renly's ghost" description
- **chapter:line:** ACOK Sansa VII :145
- **Verbatim:** "It was Lord Renly! Lord Renly in his green armor, with the fires shimmering off his golden antlers! Lord Renly with his tall spear in his hand!"
- **slot:** `## Quotes` on `garlan-tyrell` with note: Dontos's words; "Lord Renly" = Garlan Tyrell in Renly's armor. The armor's description (green + golden antlers, tall spear) is the load-bearing physical detail.

### QA-20: Attach to `ice` — Sansa VI blood-on-the-blade moment
- **chapter:line:** ACOK Sansa VI :115
- **Verbatim:** "He carried Ice unsheathed. Her father had always cleaned the blade in the godswood after he took a man's head, Sansa recalled, but Ser Ilyn was not so fastidious. There was blood drying on the rippling steel, the red already fading to brown."
- **slot:** `## Quotes` on `ice` node — Tier-1 book citation of Ice's physical description + its emotional resonance to Sansa (her father's sword, now wielded by his executioner as threat against her during the battle)

### QA-21: Attach to `tyrion-lannister` — "Halfman" war cry
- **chapter:line:** ACOK Tyrion XIV :37
- **Verbatim:** "His arm was red to the elbow, glistening in the light off the river. When his horse reared again, he shook his axe at the stars and heard them call out 'Halfman! Halfman!'"
- **slot:** `## Quotes`

---

## HARVEST

Wide pointer list — one line each. `chapter:line / kind / note`

**FOOD / DRINK — Tyrion XII (the dinner before battle)**
- `acok-tyrion-12:49` / food / Full menu: "creamy chestnut soup, crusty hot bread, and greens dressed with apples and pine nuts. Then came lamprey pie, honeyed ham, buttered carrots, white beans and bacon, and roast swan stuffed with mushrooms and oysters." — Tyrion + Cersei's last-supper-before-siege dinner
- `acok-tyrion-12:51` / food / Cersei eats apple speared on dagger point; salad with apples untouched
- `acok-tyrion-12:59` / food / "Lady Tanda to thank for the pig" — honeyed ham is a gift-bribe from Lady Tanda
- `acok-tyrion-12:77` / food / Swan "too rich for his taste" — food preference character note
- `acok-tyrion-12:115` / food / blackberry tarts (dessert; "I love all sorts of tarts" double-entendre)
- `acok-tyrion-12:117` / hospitality / Cersei "sets a tasty table" despite being adversaries — hospitality as political performance

**FOOD / DRINK — Sansa VI (Queen's Ballroom battle-feast)**
- `acok-sansa-06:11` / drink / Arbor gold wine — Cersei drinking heavily; "a golden vintage from the Arbor, fruity and rich"; eyes described as "wildfire" (metaphor)
- `acok-sansa-06:23` / food / Course 2: "salad of apples, nuts, and raisins" — "all the food was flavored with fear"; multiple guests not eating
- `acok-sansa-06:61` / food / Course 3: "crabclaw pies" — no further description
- `acok-sansa-06:61` / food / Course 4: "mutton roasted with leeks and carrots, served in trenchers of hollowed bread" — Lollys eats too fast, vomits
- `acok-sansa-06:61` / drink / Lord Gyles drinks constantly; passes out face-first in his trencher
- `acok-sansa-06:75` / food / Course 5: "goat cheese served with baked apples" — "scent of cinnamon filled the hall" — last course before battle news arrives
- `acok-sansa-06:101` / drink / Cersei forces Sansa to drink "cloyingly sweet, but very strong" sweet plum wine to loosen her tongue
- `acok-sansa-06:103` / drink / Sansa commanded to "drain the cup" — coercive drinking as interrogation/intimidation
- `acok-sansa-07:23` / drink / Maester Frenken administers dreamwine to hysterical guests (also dreamwine referenced at Tyrion XII via Shae in Lollys's care)

**FOOD / DRINK — grim/no-food register**
- `acok-sansa-06:23` / no-food / Multiple guests unable to eat despite fine courses; Lord Gyles coughs more than eats; Lollys gets sick
- `acok-sansa-07:137` / drink / Dontos staggering in drunk to announce victory — "happy drunk"

**PHYSICAL DESCRIPTION — armor/clothing**
- `acok-tyrion-13:53` / clothing / Sandor's helm: "dark grey armor… the left ear of the snarling hound sheared off. A gash above one eye had sent a wash of blood"
- `acok-tyrion-13:83` / clothing / Tyrion's battle gear: red stallion with crinet + chamfron, crimson silk, gilded saddle, oak shield with golden hand on red surrounded by small golden lions
- `acok-tyrion-14:13` / clothing / Mandon Moore: "white enamel of his armor, his dead eyes shining passionlessly through his helm. He rode a coal-black horse barded all in white, with the pure white shield of the Kingsguard"
- `acok-sansa-07:67` / clothing / Sandor at night: "all black and green, the blood on his face dark as tar… only a hulking darkness in a stained white cloak"
- `acok-sansa-07:129` / clothing / Sandor's discarded cloak: "the white wool stained by blood and fire" — Sansa takes it; key object (his departure from KL)
- `acok-tyrion-13:39` / clothing / Joffrey's helm: "golden circlet of kingship adorned his battle helm"
- `acok-sansa-06:29` / clothing / Cersei's gown: "low-cut gown of deep green velvet that brought out the color of her eyes. Her golden hair tumbled across her bare shoulders, and around her waist was a woven belt studded with emeralds"
- `acok-davos-03:39` / clothing / Davos: "jerkin of boiled leather and a pothelm at his feet were his only armor" — contrast to glittering highborn captains
- `acok-tyrion-14:45` / clothing / Balon Swann after battle: "Every bit of Ser Balon was spattered with gore and smudged by smoke. He raised his mace to point downriver. Bits of brain and bone clung to its head."
- `acok-sansa-07:145` / clothing / Garlan's "Renly" armor: "green armor, with the fires shimmering off his golden antlers! Lord Renly with his tall spear in his hand!"
- `acok-tyrion-13:11` / clothing / Ser Mandon Moore's Kingsguard presence noted; Tyrion XIV :13 has the armor detail

**PHYSICAL DESCRIPTION — wildfire / fire / visual**
- `acok-davos-03:107` / description / "emerald serpents rose burning and hissing from the stern of Queen Alysanne" — first wildfire appearance
- `acok-davos-03:137` / description / "Fifty feet high, a swirling demon of green flame danced upon the river. It had a dozen hands, in each a whip" — full demon image
- `acok-davos-03:125` / description / Swordfish on fire: "she trailed a head of yellow flame. Her ungainly iron ram, fashioned after the likeness of the fish from which she took her name"
- `acok-tyrion-13:15` / description / Sky roofed in green; "A terrible beauty. Like dragonfire."
- `acok-davos-03:131` / description / Wildfire rupture: "green gushing from a thousand broken jars, poison from the entrails of a dying beast, glistening, shining, spreading across the surface of the river"
- `acok-sansa-07:59` / description / Sansa's window view: "Baleful green tides moved against the bellies of the clouds… emeralds and jades of wildfire… birthing armies of short-lived shadows"
- `acok-davos-03:147` / description / Chain raised + burning wall: "a wall of red-hot steel, blazing wood, and swirling green flame stretched before him. The mouth of the Blackwater Rush had turned into the mouth of hell."
- `acok-davos-03:137` / description / "For an instant she seemed to be stroking the river with two banks of long bright torches" — Pride of Driftmark's burning oars
- `acok-tyrion-13:19` / description / "A fountain of burning jade rose from the river, the blast so bright he had to shield his eyes. Plumes of fire thirty and forty feet high danced upon the waters"

**FORESHADOWING / CHARACTER BEATS**
- `acok-davos-03:83` / foreshadowing / Melisandre sent back to Dragonstone — she has no part at Blackwater; "Stannis had shipped her back to Dragonstone with his bastard nephew Edric Storm"
- `acok-davos-03:83` / foreshadowing / Lord Bryce Caron says Melisandre's victory would not be Stannis's; Stannis won't take glory that's not his — character note (rigid pride)
- `acok-tyrion-13:41` / foreshadowing / Antler Men thrown from trebuchets by Joffrey — note Joffrey's cruelty, Tyrion's use of them as ammunition, Cersei's arrangement context
- `acok-tyrion-14:37` / foreshadowing / "battle fever" — Tyrion's first experience; told by Jaime; inner transformation moment
- `acok-tyrion-14:67` / foreshadowing / "Ser Mandon was holding out his left hand, why" — moment of realization before the cut; mystery of why Moore tried to kill him (Cersei's order suspected but never confirmed in-text)
- `acok-tyrion-15:97` / foreshadowing / Tyrion concludes Cersei paid Mandon Moore — "Cersei must have paid him to see that I never came back from the battle." (his inference, not confirmed)
- `acok-tyrion-15:107` / character / Tyrion learns he's no longer Hand; Tywin has taken the Tower of the Hand — the power shift
- `acok-tyrion-15:97` / character / "It was not as if his face had ever been fit to look at" — first moment Tyrion accepts his new face; begins book-3+ identity
- `acok-sansa-06:87` / music / Singer performs: Jonquil and Florian, Prince Aemon the Dragonknight and his queen, Nymeria's ten thousand ships — three songs named as mood-setters in the ballroom

**NOTABLE OBJECTS / ITEMS**
- `acok-sansa-07:129` / object / Sandor's abandoned white cloak — taken by Sansa, "twisted up tight, the white wool stained by blood and fire" — should this become an artifact node? (the cloak is metonymically his Kingsguard membership; he tears it off before leaving)
- `acok-tyrion-13:87` / object / Tyrion's axe — his weapon during the sortie; "Tyrion unsheathed his axe" — not a named weapon; harvest note only
- `acok-davos-03:75` / object / Chain description in detail: "three links of a huge chain snaking out from a hole no bigger than a man's head" visible above waterline; the towers had "a single door, set a good twenty feet off the ground" — physical construction detail for chain-boom node

**HOSPITALITY / PROTOCOL NOTES**
- `acok-sansa-06:31` / hospitality / Cersei explains WHY she hosts the women during battle: political calculus — survivors will tell tales of her courage; classic "hospitality as performance"
- `acok-sansa-06:87` / hospitality / Singer + jugglers + Moon Boy performing during the siege — entertainment as nervous distraction

---

## NOTES

1. **Sandor's cloak as artifact:** The abandoned white cloak (ACOK Sansa VII :129) is a strong candidate for an `object.artifact` node — it's physically described, emotionally significant (Sansa sleeps under it, it's his Kingsguard departure marker), and referenced later in the series. Flagging for Matt's decision. Slug would be `sandor-clegane-white-cloak` or `hound-white-cloak`. HOME EDGE: `sandor-clegane OWNS hound-white-cloak`, `hound-white-cloak WIELDED_IN battle-of-the-blackwater`.

2. **`lady-of-silk` and `lady-s-shame` ships:** Named in battle (ACOK Davos III :67 and :91) — "Lady of Silk and her sister Lady's Shame" — but do not appear to have artifact nodes. Quick check recommended before proposing. If they don't exist, they're Lannister fleet ships named in the battle.

3. **`brightfish`, `lord-steffon`, `ragged-jenna`, `swift-sword`, `horned-honor`, `trident-three`**: Named in Davos III :47 first battle line. Some likely have nodes (brightfish.node.md confirmed exists); others uncertain. All are attested at the battle. A Python batch-check could produce WIELDED_IN proposals for the confirmed-node ones.

4. **`song-gentle-mother` vocab problem:** No WIELDED_IN for songs feels right. The song is performed AT the battle (in Sansa's chamber as Sandor is deserting). The closest available type is `ECHOES` (thematic) or just attaching the full text as a quote on Sansa + Sandor nodes without a separate song-→-event edge. Matt should decide if `song-gentle-mother` warrants its own `object.text` node or is just quote-level.

5. **Mandon Moore mystery:** Tyrion's conclusion that Cersei paid Mandon Moore is his inference — the text does not confirm it. Edge `cersei-lannister CONSPIRES_WITH mandon-moore` would be Tier 3 (compelling inference) at best. The facts in text: Moore attacks Tyrion; Pod kills Moore (drowned); Tyrion infers Cersei ordered it. Caution on certainty level.

6. **Chain-boom book citation upgrade:** The wildfire node already has good wiki prose about the chain but NO book quotes. ACOK Tyrion XIII :27 (the chain/winch description) and Davos III :145 ("The chain. Gods save us, they've raised the chain.") are Tier-1 upgrades to the existing Tier-2 wiki node description.

7. **Swordfish's iron ram description:** ACOK Davos III :125: "Her ungainly iron ram, fashioned after the likeness of the fish from which she took her name" — this physical description (distinctive ram) should go on `swordfish-ship` node as a `## Quotes` attachment.
