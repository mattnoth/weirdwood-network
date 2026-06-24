# Lens 3 — Object / Descriptive / Quote Depth
## Sack of King's Landing arc — S142

---

## VERIFICATION LOG (slug checks before proposing)

All slugs confirmed present in graph:

| Slug | File found |
|------|------------|
| `wildfire` | `graph/nodes/artifacts/wildfire.node.md` |
| `wildfire-plot` | `graph/nodes/events/wildfire-plot.node.md` |
| `iron-throne` | `graph/nodes/artifacts/iron-throne.node.md` |
| `qarlton-chelsted` | `graph/nodes/characters/qarlton-chelsted.node.md` |
| `belis` | confirmed in `edges.jsonl` (infobox edges exist) |
| `garigus` | confirmed in `edges.jsonl` (infobox edges exist) |
| `rossart` | confirmed in `edges.jsonl` (AGENT_IN wildfire-plot) |
| `jaime-lannister` | confirmed (AGENT_IN slaying-of-aerys-ii-the-kingslaying) |
| `aerys-ii-targaryen` | confirmed (COMMANDS_IN wildfire-plot) |
| `slaying-of-aerys-ii-the-kingslaying` | confirmed |
| `aerys-commands-the-city-burned` | confirmed |
| `wildfire-plot` | confirmed — already has AGENT_IN rossart, COMMANDS_IN aerys |
| `murder-of-elia-martell-and-rhaegars-children` | confirmed |

**Pre-dedup check:** `wildfire WIELDED_IN battle-of-the-blackwater` already exists. No WIELDED_IN from wildfire to any sack-era event. No AGENT_IN belis/garigus to wildfire-plot. No VICTIM_IN qarlton-chelsted. No edges from iron-throne to the kingslaying. Crimson-cloaks prose is in iron-throne node's ## Origins but has no book-cite overlay and no edge.

---

## PROPOSED EDGES / NODES

### PROPOSAL 1 — belis AGENT_IN wildfire-plot

**Edge:** `belis --AGENT_IN--> wildfire-plot`
**Tier:** 1
**Ref:** `asos-jaime-05.md:53–63`
**Verbatim quote (line-checked):**
> "Everything was done in the utmost secrecy by a handful of master pyromancers. They did not even trust their own acolytes to help … with Rossart, Belis, and Garigus coming and going night and day, he became suspicious."
> … "I slew him first. Then I slew Aerys … Days later, I hunted down the others and slew them as well. Belis offered me gold, and Garigus wept for mercy."

**Rationale:** Belis is named by Jaime as one of the three pyromancers executing the wildfire-plot cache placement. The baseline flags only Rossart as wired; Belis and Garigus are listed as gaps. This is a clean AGENT_IN from book-direct testimony.

---

### PROPOSAL 2 — garigus AGENT_IN wildfire-plot

**Edge:** `garigus --AGENT_IN--> wildfire-plot`
**Tier:** 1
**Ref:** `asos-jaime-05.md:53–63` (same passage as above)
**Verbatim quote (line-checked):**
> "with Rossart, Belis, and Garigus coming and going night and day"
> "I hunted down the others and slew them as well … Garigus wept for mercy. Well, a sword's more merciful than fire, but I don't think Garigus much appreciated the kindness I showed him."

**Rationale:** Same as Proposal 1. Garigus is the third named pyromancer active in the plot. Both are islanded from the wildfire-plot event; these two edges complete the three-agent trio at the core of the conspiracy.

---

### PROPOSAL 3 — qarlton-chelsted VICTIM_IN wildfire-plot

**Edge:** `qarlton-chelsted --VICTIM_IN--> wildfire-plot`
**Tier:** 1
**Ref:** `asos-jaime-05.md:55`
**Verbatim quote (line-checked):**
> "Chelsted, that was his name, Lord Chelsted … He did all he could to dissuade him. He reasoned, he jested, he threatened, and finally he begged. When that failed he took off his chain of office and flung it down on the floor. Aerys burnt him alive for that, and hung his chain about the neck of Rossart, his favorite pyromancer."

**Rationale:** Chelsted's death is directly caused by his resistance to the wildfire-plot. VICTIM_IN is the right type — he is targeted and killed within the context of the plot event. He already has infobox edges (HOLDS_TITLE, DIED_AT kings-landing) but no event link. This is his single load-bearing story role.

---

### PROPOSAL 4 — wildfire WIELDED_IN aerys-commands-the-city-burned

**Edge:** `wildfire --WIELDED_IN--> aerys-commands-the-city-burned`
**Tier:** 1
**Ref:** `asos-jaime-05.md:61` + `asos-jaime-02.md:291`
**Supporting quotes (line-checked):**
- Jaime (ASOS Jaime V): *"I want him dead, the traitor … Rossart says they are inside the walls! He's gone to make them a warm welcome."* — Aerys sends Rossart to ignite the caches; the caches are the wildfire.
- (asos-jaime-05.md:57): *"The traitors want my city … but I'll give them naught but ashes. Let Robert be king over charred bones and cooked meat."*

**Rationale:** The `aerys-commands-the-city-burned` event is the moment Aerys gives the ignition order — the wildfire substance is the instrument of that command. The baseline notes this gap explicitly: "the wildfire-plot is NOT wired to [aerys-commands-the-city-burned]." WIELDED_IN is the right type (an object used in an event). The existing `wildfire WIELDED_IN battle-of-the-blackwater` is a separate instance (Blackwater) and must NOT be conflated.

---

### PROPOSAL 5 — wildfire-plot ENABLES aerys-commands-the-city-burned

**Edge:** `wildfire-plot --ENABLES--> aerys-commands-the-city-burned`
**Tier:** 1
**Ref:** `asos-jaime-05.md:53–61`
**Rationale:** The cache-placement conspiracy is the **enabling precondition** for Aerys being able to issue the burn-order at all — without the cached wildfire under the city, his command to Rossart would be hollow. ENABLES is the right causal type (necessary precondition, not direct cause). This closes the gap the baseline flags as the single clearest structural hole: "wildfire-plot is NOT wired to aerys-commands-the-city-burned." Note: wildfire-plot already has `PART_OF roberts-rebellion` and `MOTIVATES slaying-of-aerys`; this completes the chain *wildfire-plot → ENABLES → aerys-commands-city-burned → TRIGGERS → slaying-of-aerys*.

---

## ATTACHABLE QUOTES (no new edge needed; target node already exists)

### Quote A — on `wildfire` node (book-cite overlay for the cache-locations)

The `wildfire` node already has wiki prose about the caches but no navigable chapter cite. Attach to `wildfire` ## Book Citations:

> "So His Grace commanded his alchemists to place caches of wildfire all over King's Landing. Beneath Baelor's Sept and the hovels of Flea Bottom, under stables and storehouses, at all seven gates, even in the cellars of the Red Keep itself."

— Jaime Lannister, ASOS Jaime V (`sources/chapters/asos/asos-jaime-05.md:53`)

**Note:** This same quote already appears in `wildfire-plot` ## Book Citations (added S133). The wildfire *object* node has no book cites at all — this overlay upgrades its ## Quotes section from wiki-only to Tier-1 navigable. Do not duplicate the edge; just attach the quote.

---

### Quote B — on `iron-throne` node (Jaime seated / the glitter scene)

The `iron-throne` node records the fact of Jaime sitting it (in Origins § The Mad King) but carries no navigable book cite. This is the most iconic physical description of Jaime + the Iron Throne in the same moment:

> "Jaime wore the white cloak of the Kingsguard over his golden armor. I can see him still. Even his sword was gilded. He was seated on the Iron Throne, high above his knights, wearing a helm fashioned in the shape of a lion's head. How he glittered!"

— Eddard Stark (POV), AGOT Eddard II (`sources/chapters/agot/agot-eddard-02.md:151`)

And Jaime's own account of the moment (book-cite overlay):

> "Then he climbed the Iron Throne and seated himself with his sword across his knees, to see who would come to claim the kingdom. As it happened, it had been Eddard Stark."

— Jaime Lannister (POV), ASOS Jaime II (`sources/chapters/asos/asos-jaime-02.md:303`)

Attach both to `iron-throne` ## Book Citations or ## Quotes. These are the only first-person accounts of the throne-sitting episode — Ned's perspective and Jaime's own.

---

### Quote C — on `murder-of-elia-martell-and-rhaegars-children` node (crimson Lannister cloaks)

The baseline confirms the node is "rich" but carries no verbatim quote about the presentation of the bodies. Oberyn's testimony provides the definitive line:

> "It was Lord Tywin who presented my sister's children to King Robert all wrapped up in crimson Lannister cloaks."

— Oberyn Martell to Tyrion, ASOS Tyrion IX (`sources/chapters/asos/asos-tyrion-09.md:411`)

And Tywin's own admission (indirect but confessional):

> "When I laid those bodies before the throne, no man could doubt that we had forsaken House Targaryen forever."

— Tywin Lannister to Tyrion, ASOS Tyrion VI (`sources/chapters/asos/asos-tyrion-06.md:187`)

Attach both to `murder-of-elia-martell-and-rhaegars-children` ## Quotes as book-cite overlays.

---

### Quote D — on `murder-of-elia-martell-and-rhaegars-children` node (Gregor's confession)

The on-page confession from the trial by battle, which is also the single verbatim perpetrator admission:

> "Elia of Dorne," they all heard Ser Gregor say … "I killed her screaming whelp. Then I raped her. Then I smashed her fucking head in."

— Gregor Clegane, ASOS Tyrion X (`sources/chapters/asos/asos-tyrion-10.md:247`)

**Note:** This is Tier-1 book provenance for the Gregor-is-perpetrator claim, which the node currently carries only via wiki cite. Attach to ## Quotes.

---

### Quote E — on `slaying-of-aerys-ii-the-kingslaying` node (the gilded sword / blood)

Ned's visual record of the kingslaying's immediate aftermath, confirming Jaime's golden (not white) armor and the bloodied blade:

> "Aerys was dead on the floor, drowned in his own blood. His dragon skulls stared down from the walls … Jaime wore the white cloak of the Kingsguard over his golden armor … Even his sword was gilded … His golden sword was across his legs, its edge red with a king's blood."

— Eddard Stark, AGOT Eddard II (`sources/chapters/agot/agot-eddard-02.md:151–155`)

Attach to `slaying-of-aerys-ii-the-kingslaying` ## Quotes. This is the only eyewitness (non-Jaime) physical description of the moment.

---

## HARVEST

Load-bearing details passed over during research — point, don't extract; a later pass attaches.

| Location | Kind | Note |
|----------|------|------|
| `asos-jaime-05.md:109` | food / meal | Bolton's dinner with Jaime and Brienne: "cheese, bread, cold meat, and fruit"; Jaime drinks red wine, Brienne water, Bolton hippocras (Elmar serves) |
| `asos-jaime-05.md:117` | food / notable detail | Bolton eating prunes throughout the dinner: "took a prune and ate it with small sharp bites"; "He chose another prune"; "He spit a prune pit into his hand" — running motif, distinctive characterization |
| `asos-jaime-05.md:183` | food / meal | Bolton's roast: "a slice off the roast … dark and bloody"; Jaime cannot cut it one-handed |
| `asos-jaime-02.md:53–85` | food / meal (war-time) | Inn of the Kneeling Man: horsemeat steaks (charred), fried onions in bacon grease, stale oatcakes, ale (Jaime + Cleos), cider (Brienne); later midnight meal of oatcakes, salt fish, blackberries — hardship register |
| `asos-tyrion-10.md:101` | food / pre-battle meal | Tyrion's breakfast before trial by combat: "fried bread, blood sausage, applecakes, and a double helping of eggs cooked with onions and fiery Dornish peppers" — vomited at chapter's end |
| `asos-tyrion-09.md:57–58` | food / prison diet | Tyrion's prison meals: "porridge and apples … horn of ale"; previous night: "boiled eggs, burned bacon, and fried bread" |
| `asos-jaime-05.md:79–81` | food / captivity | Jaime's Harrenhal captivity diet: "Worms and piss and grey vomit" (Jaime's joke); guards say "Hardbread and water and oat porridge, he don't hardly eat it" |
| `asos-jaime-02.md:291` | object / atmosphere | Aerys pacing alone in throne room "picking at his scabbed and bleeding hands" — the Iron Throne's physical damage to Aerys, vivid pre-kingslaying detail |
| `asos-tyrion-06.md:186–191` | confession / causal | Tywin's frank account of giving Gregor no orders to spare Elia ("I did not tell him to spare her. I doubt I mentioned her at all"), and Amory's behavior with Rhaenys ("asked him afterward why it had required half a hundred thrusts to kill a girl of … two? Three?") — brutal confessional prose, Tier-1 evidence for COMMANDS_IN edge granularity |
| `asos-jaime-02.md:246–263` | backstory / Cersei-Jaime | Jaime's Kingsguard investiture origin story — joined for love of Cersei, not honor; Cersei's scheme to keep him close; "Is it a rock you want? Or me?" |
| `agot-eddard-02.md:74` | description / babes | "It was said that Rhaegar's little girl had cried as they dragged her from beneath her bed to face the swords. The boy had been no more than a babe in arms, yet Lord Tywin's soldiers had torn him from his mother's breast and dashed his head against a wall." — Ned's version, differs in details from Oberyn/Tyrion accounts; foreshadowing of AGOT-to-ASOS discrepancy |
| `asos-tyrion-10.md:123` | object / Oberyn's spear | Physical description of Oberyn's spear weapon: "turned ash eight feet long … The last two feet of that was steel: a slender leaf-shaped spearhead narrowing to a wicked spike" — load-bearing for the trial-by-combat scene |
