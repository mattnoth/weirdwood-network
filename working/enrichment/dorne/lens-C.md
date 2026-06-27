# Lens C — descriptive / quote / object depth — A1.5 Dorne proposal (S156)

---

## Proposed NEW nodes

### 1. `hotahs-longaxe`
- **slug:** `hotahs-longaxe`
- **name:** Areo Hotah's Longaxe
- **type:** `object.artifact`
- **summary:** The ash-and-iron poleaxe Areo Hotah has carried for ~30 years since his novitiate with the bearded priests of Norvos. It is his "ash-and-iron wife" — six feet of mountain ash shaft capped with an axe-head, honed sharp enough to shave with. He sleeps beside it, keeps it oiled and whetted, and calls it his wife (the bearded priests' custom: novices "wed their axe"). It is the instrument of Arys Oakheart's death.
- **anchor quote + chapter:line:** "He slid his hand along the smooth ashen shaft of his axe and wondered if that day was drawing nigh." — `affc-the-captain-of-guards-01:135`
- **secondary quote:** "The head was on a shaft of mountain ash six feet long" — `affc-the-captain-of-guards-01:23`

### 2. `garin-of-the-orphans` (conspirator Garin — distinct from `garin-the-great`)
- **slug:** `garin-of-the-orphans`
- **name:** Garin (orphan of the Greenblood)
- **type:** `character.human`
- **summary:** Arianne Martell's milk-brother and lifelong companion; his mother was Arianne's wet nurse. A swarthy, long-nosed fellow with a jade stud in one ear and a golden tooth Arianne bought him. One of the five Queenmaker conspirators; gathered wood at Shandystone, greeted Myrcella at the Greenblood. Doran sentences him to two years in Tyrosh.
- **anchor quote + chapter:line:** "Garin had been with them as well that day; he was Arianne's milk brother, and they had been inseparable since before they learned to walk." — `affc-the-queenmaker-01:23`

---

## Proposed NEW edges

*(Format: source_slug [EDGE_TYPE] target_slug | Tier-N | qualifier | verbatim quote + chapter:line | rationale)*

---

### Hotah's longaxe — wiring the weapon node

**1.** `areo-hotah` WIELDS `hotahs-longaxe` | Tier-1 | no qualifier for WIELDS |
> "Areo Hotah ran his hand along the smooth shaft of his longaxe, his ash-and-iron wife, all the while watching." — `adwd-the-watcher-01:13` |
Explicit possession + carrying; his defining object.

**2.** `hotahs-longaxe` WIELDED_IN `death-of-arys-oakheart` | Tier-1 | no qualifier |
> "Hotah's longaxe took his right arm off at the shoulder, spun away spraying blood, and came flashing back again in a terrible two-handed slash that removed the head of Arys Oakheart" — `affc-the-queenmaker-01:289` |
Direct instrument of the killing already in the graph; weapon→event reification.

**3.** `hotahs-longaxe` WIELDED_IN `areo-hotah-springs-the-ambush` | Tier-1 | no qualifier |
> "Out into the sunlight stepped Areo Hotah, longaxe in hand." — `affc-the-queenmaker-01:263` |
The longaxe is the instrument of the ambush — he springs it by appearing weapon-in-hand.

---

### Water Gardens — wiring the islanded descriptive node

**4.** `doran-martell` RULES `water-gardens` | Tier-1 | qualifier: n/a (RULES needs no qualifier) |
> "Best send a rider to Ricasso, and have him open my apartments in the Tower of the Sun. Inform my daughter Arianne that I will be there on the morrow." [context: departing the Water Gardens] — `affc-the-captain-of-guards-01:121`  
And more directly: "The Gardens are my haven." — `adwd-the-watcher-01:93` |
Doran treats the Water Gardens as his personal domain and refuge; he maintains apartments there and staffs it with guards.

**5.** `doran-martell` LOCATED_AT `water-gardens` | Tier-1 | no qualifier |
> "Two years ago, when they had left Sunspear for the peace and isolation of the Water Gardens, Prince Doran's gout had not been half so bad." — `affc-the-captain-of-guards-01:127` |
The Gardens are Doran's primary residence for years before the AFFC timeline.

**6.** `water-gardens` REGION_OF `dorne` | Tier-1 | no qualifier |
> "Only three leagues of coast road divided Sunspear from the Water Gardens, yet they were two different worlds." — `affc-the-captain-of-guards-01:219` |
Explicit geographic placement within Dorne, coast road from Sunspear.

**7.** `water-gardens` SEAT_OF `house-martell` | Tier-2 |
> "The Gardens are my haven. Prince Maron raised them as a gift for his Targaryen bride, to mark Dorne's marriage to the Iron Throne." — `adwd-the-watcher-01:93` |
Built by a Martell prince for a Targaryen bride; used as the Martell family's refuge and nursery for highborn children; functions as a secondary seat. Tier-2 because the primary formal seat is Sunspear / Tower of the Sun.

**8.** `water-gardens` LOCATED_AT `dorne` | Tier-1 | no qualifier |
> "Only three leagues of coast road divided Sunspear from the Water Gardens" — `affc-the-captain-of-guards-01:219` |
Spatially anchors the node to the region.

**9.** `myrcella-baratheon` LOCATED_AT `water-gardens` | Tier-1 | no qualifier |
> "When I do I shall take Princess Myrcella with me … You shall go as well." [Doran speaking to Arys, promising to bring Myrcella to the Water Gardens] — `affc-the-soiled-knight-01:49` |
Myrcella is sent to the Gardens for her safety; the ADWD chapter confirms she is there at the time of Balon Swann's visit.

**10.** `arianne-martell` LOCATED_AT `water-gardens` | Tier-2 |
> "You used to ride the shoulders of an older girl … It has not been so long since you were playing in those pools." — `affc-the-princess-in-the-tower-01:313` |
Arianne grew up at the Water Gardens as a child; Tier-2 because the relevant presence is in the past (childhood), not the current arc.

**11.** `ellaria-sand` LOCATED_AT `water-gardens` | Tier-1 | no qualifier |
> "Ellaria and her daughters are happily ensconced at the Water Gardens. Dorea stalks about knocking oranges off the trees with her morningstar, and Elia and Obella have become the terror of the pools." — `affc-the-princess-in-the-tower-01:313` |
Explicit placement during the post-conspiracy arc.

---

### Ghaston Grey — wiring the island-prison node

**12.** `garin-of-the-orphans` IMPRISONED_AT `ghaston-grey` | Tier-1 | no qualifier |
> "They were taken to the Planky Town and will be conveyed by ship to Ghaston Grey, until such time as Prince Doran decides their fate." — `affc-the-princess-in-the-tower-01:27` |
Explicitly sent there by Doran's order post-capture. (Same sentence covers Drey and Sylva — see edges 13–14.)

**13.** `andrey-dalt` IMPRISONED_AT `ghaston-grey` | Tier-1 | no qualifier |
> "They were taken to the Planky Town and will be conveyed by ship to Ghaston Grey, until such time as Prince Doran decides their fate." — `affc-the-princess-in-the-tower-01:27` |
Same order covers all captured conspirators initially; Drey is later redirected to Norvos (edge 13b below).

**[BORDERLINE]** **13b.** `andrey-dalt` TRAVELS_TO `norvos` | Tier-1 | no qualifier |
> "Ser Andrey has been sent to Norvos to serve your lady mother for three years." — `affc-the-princess-in-the-tower-01:217` |
Borderline: this is a dispersal destination, not a causal/narrative-weight edge. But Drey's fate is one of Gap 5's explicit targets. Propose with flag.

**14.** `sylva-santagar` IMPRISONED_AT `ghaston-grey` | Tier-2 |
> "They were taken to the Planky Town and will be conveyed by ship to Ghaston Grey, until such time as Prince Doran decides their fate." — `affc-the-princess-in-the-tower-01:27` |
Tier-2: Sylva is included in the "they" but she is explicitly redirected ("Her father has shipped her to Greenstone to wed Lord Estermont") without a confirmed stay at Ghaston Grey — she may have been diverted before arrival.

**15.** `ghaston-grey` REGION_OF `sea-of-dorne` | Tier-1 | no qualifier |
> "Ghaston Grey was a crumbling old castle perched on a rock in the Sea of Dorne" — `affc-the-princess-in-the-tower-01:29` |
Exact verbatim geographical placement.

**16.** `sea-of-dorne` REGION_OF `dorne` | Tier-2 |
> "Ghaston Grey was a crumbling old castle perched on a rock in the Sea of Dorne" — `affc-the-princess-in-the-tower-01:29` |
The Sea of Dorne is the coastal waters of the Dornish region; Tier-2 (geographic inference from shared name, no explicit statement in these 5 chapters).

**17.** `doran-martell` IMPRISONS `garin-of-the-orphans` | Tier-1 | no qualifier |
> "They were taken to the Planky Town and will be conveyed by ship to Ghaston Grey, until such time as Prince Doran decides their fate." — `affc-the-princess-in-the-tower-01:27` |
Doran is the sentencing authority.

**18.** `doran-martell` IMPRISONS `andrey-dalt` | Tier-1 | no qualifier |
> "Ser Andrey has been sent to Norvos to serve your lady mother for three years." — `affc-the-princess-in-the-tower-01:217` |
Explicitly Doran's sentence; dispatched to Norvos as Doran's punishment.

---

### Conspirator Garin node — wiring

**19.** `garin-of-the-orphans` AGENT_IN `the-queenmaker-plot` | Tier-1 | no qualifier |
> "Garin had arrived a few hours earlier" [at the Shandystone rendezvous, with the conspirators] — `affc-the-queenmaker-01:13` |
Active participant in the plot; greeted Myrcella at the Greenblood; named alongside Drey and Sylva throughout.

**20.** `garin-of-the-orphans` CONSPIRES_WITH `arianne-martell` | Tier-1 | no qualifier |
> "Garin had been with them as well that day; he was Arianne's milk brother, and they had been inseparable since before they learned to walk." — `affc-the-queenmaker-01:23` |
Core conspirator, milk-brother bond.

**21.** `garin-of-the-orphans` MILK_BROTHER_OF `arianne-martell` | Tier-1 | no qualifier |
> "Here is gay Garin of the orphans, who makes me laugh … His mother was my wet nurse." — `affc-the-queenmaker-01:137` |
Explicit statement; load-bearing backstory that explains his conspiratorial loyalty.

**22.** `garin-of-the-orphans` MEMBER_OF `orphans-of-the-greenblood` | Tier-1 | no qualifier |
> "I'm of the orphans of the Greenblood, is what my lady means." — `affc-the-queenmaker-01:141` |
Self-identification; the orphans' faction is already a node (referenced throughout).

---

### Garin the Great bug — flag for synthesis

**[FLAG — NOT A NEW EDGE — existing bug]** The baseline notes: "`arianne CONSPIRES_WITH garin-the-great` is a WRONG-TARGET BUG" — it points to the legendary Rhoynar prince (dead ~1,000 years), not Arianne's milk-brother. Now that `garin-of-the-orphans` is proposed, the synthesis pass should:
1. Redirect `arianne CONSPIRES_WITH garin-the-great` → `arianne CONSPIRES_WITH garin-of-the-orphans`
2. Mint edge 20 above instead.

---

### Old Palace / Spear Tower / Sunspear — thin node wiring

**23.** `arianne-martell` IMPRISONED_AT `spear-tower` | Tier-1 | no qualifier |
> "Arianne expected to be brought before her father's high seat beneath the dome of leaded glass in the Tower of the Sun. Instead, Hotah delivered her to the Spear Tower" — `affc-the-princess-in-the-tower-01:25` |
Her explicit prison during the arc's captivity sequence.

**24.** `doran-martell` LOCATED_AT `old-palace` | Tier-1 | no qualifier |
> "All the rest had eyes only for the chest … in the Old Palace of Sunspear" — `adwd-the-watcher-01:15` |
The feast where Balon Swann presents the Mountain's skull is explicitly in the Old Palace.

**25.** `spear-tower` PART_OF `old-palace` | Tier-1 | no qualifier |
> "First the slender Spear Tower, a hundred-and-a-half feet tall … then the mighty Tower of the Sun, with its dome of gold and leaded glass; last the dun-colored Sandship" — `affc-the-captain-of-guards-01:217` |
The Spear Tower is one of the named towers of Sunspear / the Old Palace compound.

**26.** `obara-sand` IMPRISONED_AT `spear-tower` | Tier-1 | no qualifier |
> "You will find my brother's daughters, take them into custody, and confine them in the cells atop the Spear Tower." — `affc-the-captain-of-guards-01:341` |
Doran's explicit order; covers all three elder Sand Snakes.

**27.** `nymeria-sand` IMPRISONED_AT `spear-tower` | Tier-1 | no qualifier |
> "You will find my brother's daughters, take them into custody, and confine them in the cells atop the Spear Tower." — `affc-the-captain-of-guards-01:341` |
Same order as edge 26.

**28.** `tyene-sand` IMPRISONED_AT `spear-tower` | Tier-1 | no qualifier |
> "you will be content with murder. And you?" [Tyene, on the dais with Doran] and "first secure Tyene, Nymeria, and Obara" — `affc-the-captain-of-guards-01:273, 345` |
Named first in the arrest priority list.

---

### Arys Oakheart sub-arc (Gap 2)

**29.** `arianne-martell` MANIPULATES `arys-oakheart` | Tier-1 | qualifier: `via_seduction` |
> "Her seduction of Ser Arys had required half a year. Though he claimed to have known other women before taking the white, she would never have known that from the way he acted." — `affc-the-princess-in-the-tower-01:227` |
Arianne explicitly used seduction as the instrument to recruit him to the plot; MANIPULATES(via_seduction) is the correct modeling (LEVER_SHARED.md §edge-usage: LOVER_OF already exists, this adds the using-him-as-tool layer).

**30.** `arys-oakheart` BREAKS_VOW `myrcella-baratheon` | Tier-1 | qualifier: (no qualifier for BREAKS_VOW) |
> "I swore an oath!" … "To Joffrey, not to Tommen." / "I am a knight of the Kingsguard." — `affc-the-soiled-knight-01:203–205` |
The Kingsguard vow was sworn to protect the king and the royal family — specifically Myrcella as the princess in his charge. His departure to the Greenblood with the plot is a direct breach. Tier-1 (the text is explicit about his vow-breaking).

**[BORDERLINE]** **31.** `arys-oakheart` BREAKS_VOW `tommen-baratheon` | Tier-1 |
> "I swore an oath! … To Joffrey, not to Tommen." — `affc-the-soiled-knight-01:203–205` |
Borderline: Arys rationalizes that his oath was to Joffrey, but the broader Kingsguard oath is to the crown; the synthesis may prefer to resolve this as edge 30 only. Flag for review.

---

### Ghaston Grey / dispersal (Gap 5)

**32.** `doran-martell` MARRIES_OFF `sylva-santagar` | Tier-1 | no qualifier |
> "Lady Sylva received no punishment from me, but she was of an age to marry. Her father has shipped her to Greenstone to wed Lord Estermont." — `affc-the-princess-in-the-tower-01:217` |
Doran arranged (via her father) the marriage as consequence/disposal of the conspirator.

---

## Dropped / considered-but-rejected

- **`princess-myrcella` (the ship)** — Searched all 5 chapters; no reference to a ship named "Princess Myrcella" appears in any of the 5 in-scope chapters. The baseline flags it as "confirm what it is." Cannot quote it from the chapter text → not proposed.

- **`sea-of-dorne` as a REGION_OF `dorne` standalone edge** — proposed as edge 16 above with Tier-2 caveat; the phrasing in the text doesn't explicitly call it "the sea of Dorne the region" but the geographic logic is sound.

- **Hotah's cheek-scars / branding mark as an artifact node** — The chest-brand (axe-shaped, from the bearded priests) and the face-scars are vivid physical description but do not carry narrative-weight edges in the arc; harvest rows suffice.

- **Gerold Dayne's longsword as object.artifact** — Present in the chapters ("unsheathed his longsword … hone the blade with an oilstone") but Darkstar's personal sword isn't named, isn't called the "black sword of House Dayne of High Hermitage" in the text (that's from wiki/fan gloss, not these chapters). Cannot quote a named weapon. Harvest row only.

- **The spear-and-sun sigil as an artifact node** — The Martell sigil is referenced via the throne inlay ("the Martell spear inlaid in gold upon its back" — `affc-the-captain-of-guards-01:257`) and Obara's copper-sun belt. This is a heraldic emblem, not an artifact with narrative weight of its own. Harvest row.

- **Garin's sentence to Tyrosh as `TRAVELS_TO tyrosh`** — proposed as edge 13b with BORDERLINE flag; it's a dispersal destination. The synthesis can keep or drop.

- **`areo-hotah` BORN_AT `norvos`** — Hotah's Norvoshi origin is thoroughly discussed but the arc's 5 chapters don't assert his birth there specifically ("a callow youth had come from Norvos" — places him as arriving from Norvos, not born there). Ambiguous; not proposed.

- **`water-gardens` BUILT by a Martell ancestor** — Doran says "One of my ancestors had them built to please his Targaryen bride" (adwd) and elsewhere says "Prince Maron raised them" (adwd-the-watcher-01:93). The BUILT edge requires a source node; no `maron-martell` node is in scope for this dip. Flag as harvest.

- **Daenerys Targaryen (the Targaryen bride who filled the Gardens with children)** — The text explicitly names her: "Daenerys was her name. She was sister to King Daeron the Good." This is a historical figure (not Daenerys Stormborn). A `daenerys-of-the-water-gardens NAMED_AFTER …` or a connection between `water-gardens` and Daenerys Targaryen (historical) is tempting but out of scope for the Dorne arc enrichment dip and the node may not exist. Harvest row only.

- **The Viserys betrothal (Arianne promised to Viserys)** — In the Princess in the Tower chapter, Doran reveals Arianne was betrothed to someone who died via "a pot of molten gold" (= Viserys Targaryen). This is a GAP-7 cross-arc seam (Dorne↔AEGON), not a descriptive/object edge. Lens D territory. Note here for cross-lens handoff.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|-------------|------|
| food | AFFC | affc-the-captain-of-guards-01:11 | Blood oranges described as "well past ripe," fallen to burst on the pale pink marble; "sharp sweet smell" fills the air — the Water Gardens' defining sensory image |
| food | AFFC | affc-the-captain-of-guards-01:153 | Doran served "a bowl of purple olives, with flatbread, cheese, and chickpea paste" at the Water Gardens; he eats a bit and then drinks strongwine |
| drink | AFFC | affc-the-captain-of-guards-01:153 | Doran drinks "a cup of the sweet, heavy strongwine that he loved" — explicitly his preferred wine; refills it |
| food | AFFC | affc-the-captain-of-guards-01:165 | Doran breaks his fast with "a blood orange and a plate of gull's eggs diced with bits of ham and fiery peppers" before leaving the Water Gardens |
| food | AFFC | affc-the-queenmaker-01:155 | Arianne offers Myrcella "dates and cheese and olives, and lemonsweet to drink" at Shandystone |
| food | AFFC | affc-the-queenmaker-01:239 | "Myrcella split an orange with Spotted Sylva, whilst Garin ate olives and spit the stones at Drey" — mid-journey rest |
| food | AFFC | affc-the-princess-in-the-tower-01:47 | Arianne's captivity midday meal: "The kid had been roasted with lemon and honey. With it were grape leaves stuffed with a mélange of raisins, onions, mushrooms, and fiery dragon peppers." She initially refuses, then eats from hunger |
| food | AFFC | affc-the-princess-in-the-tower-01:59 | Arianne's captivity food requests: "figs or olives or peppers stuffed with cheese" from old Belandra — Dornish staple foods named |
| food | AFFC | affc-the-soiled-knight-01:21 | Snake grilled over a brazier in the shadow city; "the best snake sauce had a drop of venom in it, along with mustard seeds and dragon peppers" — Hotah/Arys sensory detail; Myrcella loves Dornish food |
| food | ADWD | adwd-the-watcher-01:51 | Feast menu in full: "soup was made with eggs and lemons, the long green peppers stuffed with cheese and onions. There were lamprey pies, capons glazed with honey, a whiskerfish … a savory snake stew, chunks of seven different sorts of snake slow-simmered with dragon peppers and blood oranges and a dash of venom … Sherbet followed … a skull of spun sugar … sweet custard inside and bits of plum and cherry." SEVEN COURSES |
| drink | ADWD | adwd-the-watcher-01:43 | Feast wine = "Dornish strongwine, dark as blood and sweet as vengeance." Hotah doesn't drink at feasts; Doran drinks his own wine "well laced with poppy juice" for the pain |
| venom/food | AFFC | affc-the-queenmaker-01:47 | Darkstar: "I was weaned on venom, Dalt. Any viper takes a bite of me will rue it." — figurative but links to the venom/Dornish toxicology register |
| food | AFFC | affc-the-queenmaker-01:37 | Summerwine passed around the fire at Shandystone; "all but Darkstar, who preferred to drink unsweetened lemonwater" — characterization detail |
| food/drink | AFFC | affc-the-captain-of-guards-01:157 | Hotah's Norvoshi food memory: "wintercake … rich with ginger and pine nuts and bits of cherry, with nahsa to wash it down, fermented goat's milk served in an iron cup and laced with honey" — contrast with Dornish food |
| food | ADWD | adwd-the-watcher-01:55 | Ser Balon's feast eating: "a spoon of soup, a bite of the pepper, the leg off a capon, some fish. He shunned the lamprey pie and tried only one small spoonful of the stew. Even that made his brow break out in sweat." — Westerosi outsider reaction to Dornish food |
| description | AFFC | affc-the-captain-of-guards-01:217 | Sunspear towers: "First the slender Spear Tower, a hundred-and-a-half feet tall and crowned with a spear of gilded steel that added another thirty feet to its height; then the mighty Tower of the Sun, with its dome of gold and leaded glass; last the dun-colored Sandship, looking like some monstrous dromond that had washed ashore and turned to stone." — full compound description for `old-palace` node `## Quotes` |
| description | AFFC | affc-the-captain-of-guards-01:219 | Water Gardens vs Sunspear contrast: "There children frolicked naked in the sun, music played in tiled courtyards, and the air was sharp with the smell of lemons and blood oranges … In place of the pink marble of the Water Gardens, Sunspear was built from mud and straw, and colored brown and dun." — `water-gardens` node `## Quotes` |
| description | ADWD | adwd-the-watcher-01:93 | Doran on Water Gardens history + feel: "Beautiful and peaceful … Cool breezes, sparkling water, and the laughter of children … One of my ancestors had them built to please his Targaryen bride … Daenerys was her name … it was her marriage that made Dorne part of the Seven Kingdoms … Daenerys who filled the gardens with laughing children … she took pity on the children of her grooms and cooks and serving men and invited them to use the pools and fountains too, a tradition that has endured till this day." — essential Water Gardens origin quote |
| description | ADWD | adwd-the-watcher-01:187 | Doran's "grass and viper" speech: "Oberyn was ever the viper. Deadly, dangerous, unpredictable. No man dared tread on him. I was the grass. Pleasant, complaisant, sweet-smelling, swaying with every breeze … it is the grass that hides the viper from his enemies and shelters him until he strikes." — `doran-martell` node `## Quotes`, defines his long-game persona |
| description | AFFC | affc-the-captain-of-guards-01:59 | Doran's gout: "His body was soft and shapeless beneath his linen robes, and his legs were hard to look upon. The gout had swollen and reddened his joints grotesquely; his left knee was an apple, his right a melon, and his toes had turned to dark red grapes, so ripe it seemed as though a touch would burst them." — canonical description for `doran-martell` node `## Quotes` |
| description | AFFC | affc-the-captain-of-guards-01:23 | Hotah's longaxe blocking Obara: "The head was on a shaft of mountain ash six feet long, so she could not go around." — physical spec for `hotahs-longaxe` |
| description | AFFC | affc-the-captain-of-guards-01:39 | Hotah self-description: "Once, long ago, a callow youth had come from Norvos, a big broad-shouldered boy with a mop of dark hair. That hair was white now, and his body bore the scars of many battles." — physical description for `areo-hotah` node |
| description | AFFC | affc-the-captain-of-guards-01:155 | Hotah's axe-care ritual: "Keep your longaxe sharp, the bearded priests had told him, the day they branded him. He always did." + the brand/burning hair detail — `areo-hotah` characterization |
| description | AFFC | affc-the-captain-of-guards-01:157 | Hotah's chest brand: "He smelled the stench of burning hair as the bearded priest touched the brand to the center of his chest … The hair had never grown back over the axe." — physical description |
| description | AFFC | affc-the-soiled-knight-01:199 | Arianne's description of Hotah to Arys: "He is terrible when aroused … They say he sleeps with that great axe beside him." + "The big Norvoshi captain with the scarred face had always made him feel profoundly uneasy." — `areo-hotah` node `## Quotes` |
| description | AFFC | affc-the-queenmaker-01:31 | Darkstar's full physical description: "Ser Gerold Dayne had an aquiline nose, high cheekbones, a strong jaw. He kept his face clean-shaven, but his thick hair fell to his collar like a silver glacier, divided by a streak of midnight black … his eyes … were purple. Dark purple. Dark and angry." — `gerold-dayne` node `## Quotes` |
| description | AFFC | affc-the-queenmaker-01:153 | Darkstar introduces himself: "'No. Men call me Darkstar, and I am of the night.'" — `gerold-dayne` node canonical quote |
| description | AFFC | affc-the-princess-in-the-tower-01:165 | Doran on Darkstar: "Darkstar is the most dangerous man in Dorne." — `gerold-dayne` node `## Quotes` |
| description | AFFC | affc-the-princess-in-the-tower-01:169 | Myrcella's wound: "the slash opened her cheek down to the bone and sliced off her right ear. Maester Caleotte was able to save her life, but no poultice nor potion will ever restore her face." — `myrcella-baratheon` node `## Quotes`, the maiming's permanent consequences |
| description | AFFC | affc-the-princess-in-the-tower-01:37 | Arianne's cell in the Spear Tower: "Her cell was large and airy … Myrish carpets on the floor, red wine to drink, books to read … an ornate cyvasse table … a featherbed … a privy with a marble seat, sweetened by a basketful of herbs." + the two windows (east to sea, other to Tower of the Sun) — `spear-tower` node |
| description | AFFC | affc-the-princess-in-the-tower-01:29 | Ghaston Grey: "a crumbling old castle perched on a rock in the Sea of Dorne, a drear and dreadful prison where the vilest of criminals were sent to rot and die." — `ghaston-grey` node `## Quotes` |
| description | AFFC | affc-the-captain-of-guards-01:257 | Throne room dais in Tower of the Sun: "There were two seats on the dais, near twin to one another, save that one had the Martell spear inlaid in gold upon its back, whilst the other bore the blazing Rhoynish sun that had flown from the masts of Nymeria's ships when first they came to Dorne." — `old-palace` / `tower-of-the-sun` descriptive detail; also heraldic spear-and-sun |
| description | AFFC | affc-the-captain-of-guards-01:249 | Tower of the Sun interior: "the last light of the afternoon was slanting down through thick windows of many-colored glass to dapple the pale marble with diamonds of half a hundred colors." — `old-palace` node |
| sigil | AFFC | affc-the-queenmaker-01:251 | The Martell spear-and-sun reference via the Young Dragon quote: "The arms of House Martell display the sun and spear, the Dornishman's two favored weapons … but of the two, the sun is the more deadly." — `house-martell` node `## Quotes` |
| description | AFFC | affc-the-captain-of-guards-01:235 | Arianne's appearance: "Her hair was a mane of jet-black ringlets that fell to the small of her back, and around her brow was a band of copper suns … she had a woman's body, lush and roundly curved" — `arianne-martell` node |
| cross-arc seam | AFFC | affc-the-princess-in-the-tower-01:325 | Doran's "fire and blood" reveal: "Prince Doran pressed the onyx dragon into her palm with his swollen, gouty fingers, and whispered, 'Fire and blood.'" — `doran-reveals-fire-and-blood-pact` event, key quote for the event node |
| venom/food | AFFC | affc-the-queenmaker-01:17 | Oberyn at Shandystone long ago "caught some vipers and showed Tyene the safest way to milk them for their venom" — venom-harvesting; links Oberyn's knowledge to Tyene's poison skills |
| food | AFFC | affc-the-princess-in-the-tower-01:129 | Arianne after captivity eats "sparingly of the cheese and fruit they'd brought her. She drank a little wine to settle her stomach." — prison-ration recovery detail |
| betrothal seam | AFFC | affc-the-princess-in-the-tower-01:305 | Arianne's secret betrothal to the man killed "by a pot of molten gold" = Viserys Targaryen. Cross-arc seam (Dorne↔AEGON/Viserys). Lens D territory — flagged here for cross-lens handoff. |
| hospitality | ADWD | adwd-the-watcher-01:225 | Doran refuses to harm Ser Balon because guest right: "Ser Balon is a guest beneath my roof. He has eaten of my bread and salt. I will not do him harm." — explicit bread-and-salt guest right invocation |
| hospitality | AFFC | affc-the-princess-in-the-tower-01:229 | Balon Swann's Dornish journey: "once they crossed the mountains into Dorne their progress had been slowed by a round of feasts, hunts, and celebrations at every castle" — Dornish hospitality as strategic tool |
