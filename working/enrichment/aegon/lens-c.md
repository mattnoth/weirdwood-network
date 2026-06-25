# AEGON Enrichment — Lens C: Descriptive / Quote / Object Depth

> **Lens:** Object nodes, artifact edges, afflictions, descriptive prose, quote attachments, food harvest.
> **PROPOSE only — no graph writes.**
> **Theory gate respected:** No identity claims on Aegon. All new edges → `aegon-targaryen-young-griff`.
> **Produced:** 2026-06-25, S147.
> **Sources read:** `adwd-the-lost-lord-01.md`, `adwd-the-griffin-reborn-01.md`, `adwd-tyrion-03.md`, `adwd-tyrion-04.md`, `adwd-tyrion-05.md`, `adwd-tyrion-06.md`, `adwd-epilogue.md`.

---

## Dedup verification log

| Item | Status | Note |
|---|---|---|
| `greyscale` node | **HIT** — `graph/nodes/medical/greyscale.node.md` (tier-2, wiki-sourced) | Node exists; 0 incoming + 0 outgoing edges. Rich prose but no character edges. |
| `shy-maid` node | **HIT** — `graph/nodes/artifacts/shy-maid.node.md` | Exists; 0 outgoing, 1 incoming (LOCATED_AT from stone-men-attack). No CAPTAIN_OF/CREW_OF wired. |
| `golden-skulls` node | **HIT** — `graph/nodes/artifacts/golden-skulls.node.md` | Exists; 0 edges. Node prose is rich (Bittersteel tradition, Myles Toyne, hiding skulls during landing). |
| `illyrios-chests` node | **HIT** — `graph/nodes/artifacts/illyrios-chests.node.md` | Exists; 0 edges. The rubies/chain are separate from Illyrio's chests (those are armor + court clothing). |
| cyvasse node | **NONE found** — no `cyvasse.node.md` in `graph/nodes/artifacts/` | Only references in chapter-nodes and material nodes (carnelian, jade). No dedicated artifact node. |
| ruby/dragon-chain node | **NONE found** | No artifact node for Illyrio's gift (3 rubies on black iron chain). |
| `jon-connington AFFLICTED_BY greyscale` | **DARK** — 0 edges on either node | Neither `greyscale` nor `jon-connington` has any AFFLICTED_BY edge. |
| `yandry CAPTAIN_OF shy-maid` | **DARK** — 0 such edges | Yandry has no CAPTAIN_OF; Ysilla has no CREW_OF. |
| `black-balaq OWNS goldenheart-bow` | **DARK** | No goldenheart-bow artifact node; no OWNS on black-balaq. |
| `tywins-crossbow` | **HIT** — `graph/nodes/artifacts/tywins-crossbow.node.md` | The Tywin-assassination crossbow. Varys's crossbow in the epilogue is a **different weapon**. `tywins-crossbow` covers ASOS; Varys's crossbow is ADWD-epilogue, separate artifact. |
| `griffins-roost` location | **HIT** — `graph/nodes/locations/griffins-roost.node.md` | Exists. |
| food items (beans, eggs, bacon, fried bread) | **NONE in foods/** | No `bean`, `egg`, `bacon`, `fried-bread` nodes. `bread.node.md` exists but not `fried-bread`. |

---

## Proposed nodes

| slug | type | source cite | why queryable |
|---|---|---|---|
| `illyrios-ruby-chain` | object.artifact | `adwd-the-lost-lord-01.md:61` | The three square-cut rubies on black iron chain are Illyrio's gift to Aegon before the reveal — a deliberate object of dynastic meaning ("Red and black. Dragon colors."). Queryable as "what gift did Illyrio give Aegon?"; the GIFTED_TO edge binds `illyrio-mopatis` → `aegon-targaryen-young-griff` via a concrete artifact. Distinct from `illyrios-chests` (armor/clothing). NEW-NODE. |
| `varys-crossbow` | object.artifact | `adwd-epilogue.md:269` | Varys shoots Kevan with a crossbow — a deliberate parallel to Tyrion's patricide (Varys even names it: "I thought the crossbow fitting. You shared so much with Lord Tywin, why not that?"). The weapon of the KL-endgame assassination is a distinct artifact from `tywins-crossbow` (different scene, ADWD-epilogue). WIELDED_IN the `assassinations-of-pycelle-and-kevan-lannister` event. Queryable as "what weapon did Varys use?". NEW-NODE. |

**CONSIDER but not recommending:**

| slug | why skipped |
|---|---|
| `cyvasse` (game/artifact) | The cyvasse set on the Shy Maid is used as a framing device (Tyrion's goad), but cyvasse appears all over the books. A generic game node adds little unless it carries the specific ADWD Tyrion–Aegon scene quote — better handled as a quote attachment on the `aegon-targaryen-young-griff` or `tyrion-lannister` node. Skip minting a new node; harvest the scene quote. |
| `goldenheart-bow` | Black Balaq's bow is mentioned at `adwd-the-griffin-reborn-01.md:19` ("great bows of goldenheart treasured by Black Balaq himself and his fifty Summer Islanders. Only a dragonbone bow could outrange one made of goldenheart."). This is a distinctive artifact type but the passage attributes the bows collectively to the Summer Islander contingent, not as a single named weapon. Better as a quote attachment on `black-balaq` node + harvest item. Skip minting. |
| `children-of-varys` (a.k.a. the little birds) | Tempting as an object of the assassination scene (the children's daggers), but the children are unnamed agents in the epilogue, not a queryable artifact. NEEDS_VOCAB: for their role (agents of Varys — no node to attach AGENT_IN to). Harvest only. |

---

## Proposed edges

### E1: `jon-connington AFFLICTED_BY greyscale` — **HIGHEST PRIORITY**

- **source --TYPE--> target:** `jon-connington --AFFLICTED_BY--> greyscale`
- **tier:** 1 (explicit, observed by POV)
- **source cite:** `adwd-the-lost-lord-01.md:237`
- **quote:** "The nail on his middle finger had turned as black as jet, he saw, and the grey had crept up almost to the first knuckle. The tip of his ring finger had begun to darken too, and when he touched it with the point of his dagger, he felt nothing."
- **status:** HIT (`greyscale` node exists; `jon-connington` node exists; edge DARK)
- **rationale:** This is the arc's death-clock. JonCon contracted greyscale saving Tyrion from the stone men at the Bridge of Dream (adwd-tyrion-05); by `adwd-the-griffin-reborn-01` it has spread to the second knuckle. The AFFLICTED_BY edge is the direct substrate for the lens-d causal wiring: greyscale MOTIVATES JonCon's haste → siege of Storm's End decision. Without this edge, the `greyscale` node sits orphaned with 0 edges and the Jon-Con death-clock is invisible to graph traversal.

**Secondary greyscale edge:**

- **source --TYPE--> target:** `jon-connington --AFFLICTED_BY--> greyscale` (corroborating cite from the concealment chapter)
- **corroborating quote:** "He dare not let the greyscale become known. Queer as it seemed, men who would cheerfully face battle and risk death to rescue a companion would abandon that same companion in a heartbeat if he were known to have greyscale." — `adwd-the-griffin-reborn-01.md:141`
- **note:** Same edge; this second quote goes to `## Quotes` on the `greyscale` node as a book-cite upgrade of the wiki quote already there (the wiki node quotes almost the same text but without exact chapter:line cite).

---

### E2: `illyrio-mopatis GIFTED_TO aegon-targaryen-young-griff` (via the ruby chain)

- **source --TYPE--> target:** `illyrio-mopatis --GIFTED_TO--> aegon-targaryen-young-griff`
- **tier:** 1
- **source cite:** `adwd-the-lost-lord-01.md:61`
- **quote:** "At his throat he wore three huge square-cut rubies on a chain of black iron, a gift from Magister Illyrio. Red and black. Dragon colors."
- **status:** NEW-NODE (`illyrios-ruby-chain` needs minting first); HIT on both character nodes
- **note:** The edge should carry `via: illyrios-ruby-chain` in its evidence notes, though the GIFTED_TO relation connects the two characters even without the artifact node. Propose BOTH the node mint AND the edge; the edge is the load-bearing piece.

**Also propose:** `aegon-targaryen-young-griff OWNS illyrios-ruby-chain`

- **source --TYPE--> target:** `aegon-targaryen-young-griff --OWNS--> illyrios-ruby-chain`
- **tier:** 1, `adwd-the-lost-lord-01.md:61`
- **quote:** (same — he is wearing them at his throat at the reveal scene)

---

### E3: `yandry CAPTAIN_OF shy-maid` + `ysilla CREW_OF shy-maid`

- **source --TYPE--> target:** `yandry --CAPTAIN_OF--> shy-maid`
- **tier:** 2 (inferred from who commands the tiller + owns the boat)
- **source cite:** `adwd-tyrion-04.md:83` ("He is a sweet boat. Her draft was so shallow…"; Yandry takes the tiller, operates the poleboat; Ysilla cooks and tends; the Shy Maid is theirs to keep or abandon — "Their part in this is done.")
- **quote (CAPTAIN_OF basis):** "Yandry took them out into the center of the river, where the current was strongest." — `adwd-tyrion-04.md:83`; and `adwd-the-lost-lord-01.md:229`: "Give Yandry and Ysilla our thanks. Their part in this is done." (confirms the boat is theirs, JonCon is releasing them)
- **status:** HIT (both `yandry`, `ysilla`, and `shy-maid` nodes exist; edges DARK)
- **note:** CAPTAIN_OF requires target to be object.artifact — `shy-maid` is typed object.artifact. HIT.
- **rationale:** Makes the Shy Maid queryable as "whose boat is the Shy Maid?" and "who captains Aegon's disguise transport?" The `shy-maid` node has 0 edges besides the event's LOCATED_AT; these are the foundational ownership/operator edges the node needs.

**Secondary CREW_OF edges:**

- `ysilla --CREW_OF--> shy-maid` — tier 1; `adwd-tyrion-04.md:51` ("Yandry and Ysilla shared one cabin… Ysilla was turning the biscuits.")
- `haldon --CREW_OF--> shy-maid` — tier 2 (he has a cabin, is a regular passenger-crew); quote "Haldon's cabin was the largest of the four" — `adwd-tyrion-04.md:143`
- `lemore --CREW_OF--> shy-maid` — tier 2; same source, her own cabin
- `rolly-duckfield --CREW_OF--> shy-maid` — tier 2; sleeps in the hold; quote "Ser Rolly Duckfield possibly sleeps in the hold" (wiki node); `adwd-tyrion-03.md:87` — Haldon says "our shy maid will not wait for man nor dwarf"

**Note on slug:** Per dedup log, `rolly-duckfield` is the slug; pass-1 edges may use `duck`. Target the correct slug.

---

### E4: `varys WIELDS varys-crossbow` + `varys-crossbow WIELDED_IN assassinations-of-pycelle-and-kevan-lannister`

- **source --TYPE--> target:** `varys --WIELDS--> varys-crossbow`
- **tier:** 1
- **source cite:** `adwd-epilogue.md:269`
- **quote:** "Then something slammed him in the chest between the ribs, hard as a giant's fist … A quarrel was sunk almost to the fletching in his chest."
- **status:** NEW-NODE (`varys-crossbow` needs minting); HIT on `varys` and `assassinations-of-pycelle-and-kevan-lannister`

- **source --TYPE--> target:** `varys-crossbow --WIELDED_IN--> assassinations-of-pycelle-and-kevan-lannister`
- **tier:** 1
- **source cite:** `adwd-epilogue.md:277` (Varys sets the crossbow down after shooting)
- **quote:** "The eunuch set the crossbow down."
- **status:** NEW-NODE (target HIT)

**Rationale:** The crossbow is a deliberate narrative parallel to Tywin's murder. Varys names the parallel explicitly: "I thought the crossbow fitting. You shared so much with Lord Tywin, why not that?" (`adwd-epilogue.md:293`). The `varys-crossbow` node + WIELDED_IN edge makes the parallel queryable (graph-query: artifacts used by Varys / artifacts WIELDED_IN the assassination event / parallels to `tywins-crossbow`). Without the node, this iconic object is invisible to traversal.

---

### E5: `black-balaq COMMANDS_IN landing-of-the-golden-company` (archer-command role)

- **source --TYPE--> target:** `black-balaq --COMMANDS_IN--> landing-of-the-golden-company`
- **tier:** 1
- **source cite:** `adwd-the-griffin-reborn-01.md:11`
- **quote:** "Black Balaq commanded one thousand bows … for the long voyage he had insisted that Homeless Harry Strickland break Balaq's command into ten companies of one hundred men and place each company upon a different ship."
- **status:** HIT (both nodes exist; edge DARK)
- **rationale:** Black Balaq's archers are operationally central to every taking in the Stormlands campaign. The chapter makes this explicit: "For this, two hundred proved sufficient" to take Griffin's Roost; Black Balaq personally brings down the third raven. He is the GC's tactical air-cover. COMMANDS_IN is in vocab and is the right type (he commands in a named event). This makes `black-balaq` reachable from the landing HUB.

---

## Quote attachments

### QA1: `aegon-targaryen-young-griff` — `## Quotes` — physical appearance (disguise reveal)

- **node:** `aegon-targaryen-young-griff`
- **section:** `## Quotes`
- **source:** `adwd-the-lost-lord-01.md:61`
- **verbatim quote:**
> "With his hair washed and cut and freshly dyed a deep, dark blue, his eyes looked blue as well. At his throat he wore three huge square-cut rubies on a chain of black iron, a gift from Magister Illyrio. Red and black. Dragon colors."

**Companion quote (his complaint about the dye):**
> "I am sick of this blue dye. We should have washed it out." — `adwd-the-lost-lord-01.md:63`

**And the first appearance description of the silver-gold roots:**
> "Young Griff ran his fingers through his hair." (in context of the dyed-blue-with-roots-showing detail implied but not spelled out at :61 — the roots are more explicitly shown in Tyrion's observation at `adwd-tyrion-05.md:165`: "The blue hair makes your eyes seem blue, that's good. And the tale of how you color it in honor of your dead Tyroshi mother was so touching it almost made me cry.")

- **rationale:** The physical description of Aegon in his disguise is Tier-1 evidence for who he is and how he hides. The `## Quotes` section of his node should carry the reveal description. Currently the node's quote section appears thin (27 total edges, but no description of his physical appearance captured as a node quote).

---

### QA2: `aegon-targaryen-young-griff` — `## Quotes` — the sail-west decision

- **node:** `aegon-targaryen-young-griff`
- **section:** `## Quotes`
- **source:** `adwd-the-lost-lord-01.md:217`
- **verbatim quote:**
> "It is," Aegon replied eagerly. "If my aunt wants Meereen, she's welcome to it. I will claim the Iron Throne by myself, with your swords and your allegiance. Move fast and strike hard, and we can win some easy victories before the Lannisters even know that we have landed. That will bring others to our cause."

- **rationale:** The voice of the sail-west decision in Aegon's own words. The MOTIVATES edge (`aegon-targaryen-young-griff --MOTIVATES--> golden-company-sails-for-westeros`) already exists; attaching this quote makes the evidence_quote for that edge directly readable from the node.

---

### QA3: `aegon-targaryen-young-griff` — `## Quotes` — Tyrion's goad + Aegon's fury

- **node:** `aegon-targaryen-young-griff`
- **section:** `## Quotes`
- **source:** `adwd-tyrion-06.md:125`
- **verbatim quote:**
> "I will not come to my aunt a beggar. I will come to her a kinsman, with an army."

- **second quote (the table-kick):** `adwd-tyrion-06.md:157`:
> Young Griff jerked to his feet and kicked over the board. Cyvasse pieces flew in all directions, bouncing and rolling across the deck of the Shy Maid. "Pick those up," the boy commanded.

- **rationale:** The table-kick is the most iconic object-moment in the arc: Aegon's Targaryen temper erupting over cyvasse. It characterizes him vividly and provides a direct object-in-context scene (the cyvasse board as prop). Both quotes together show the pride that makes him receptive to Tyrion's sail-west goad.

---

### QA4: `jon-connington` — `## Quotes` — the death-clock paragraph

- **node:** `jon-connington`
- **section:** `## Quotes`
- **source:** `adwd-the-lost-lord-01.md:237–241`
- **verbatim quote:**
> "Death, he knew, but slow. I still have time. A year. Two years. Five. Some stone men live for ten. Time enough to cross the sea, to see Griffin's Roost again. To end the Usurper's line for good and all, and put Rhaegar's son upon the Iron Throne."
> — (adwd-the-lost-lord-01.md:239)

- **rationale:** This is the greyscale death-clock in JonCon's own voice. It is also the clearest statement of his MOTIVATES relationship to the whole campaign: he is running a race against his own death. Lens d will wire `greyscale MOTIVATES siege-of-storms-end-300` via jon-connington; this quote is the evidence substrate.

---

### QA5: `greyscale` node — `## Quotes` — the book-cite upgrade for the concealment quote

- **node:** `greyscale`
- **section:** `## Quotes`
- **source:** `adwd-the-griffin-reborn-01.md:141`
- **verbatim quote:**
> "He dare not let the greyscale become known. Queer as it seemed, men who would cheerfully face battle and risk death to rescue a companion would abandon that same companion in a heartbeat if he were known to have greyscale."

- **status:** The wiki node already has this quote (wiki:Greyscale.cite_ref-Radwd61…) but without a navigable chapter:line cite. This attachment upgrades the citation to `adwd-the-griffin-reborn-01.md:141` (Tier-1 book provenance vs. Tier-2 wiki cite_ref). Per book-citation-overlay policy (memory: `feedback_book_citation_overlay_value.md`), do this even when the wiki node already states the fact.

---

### QA6: `golden-skulls` node — `## Quotes` — book-cite upgrade for the Myles Toyne moment

- **node:** `golden-skulls`
- **section:** `## Quotes`
- **source:** `adwd-the-lost-lord-01.md:97`
- **verbatim quote:**
> "Death had robbed him of his ears, his nose, and all his warmth. The smile remained, transformed into a glittering golden grin. All the skulls were grinning, even Bittersteel's on the tall pike in the center."

- **second quote** (JonCon's private vow): `adwd-the-lost-lord-01.md:99`
> "When I return to Westeros, it will not be as a skull atop a pole."

- **source:** `adwd-the-lost-lord-01.md:99`
- **status:** Wiki node has these quotes but with wiki cite_refs only; book cite upgrades both to navigable Tier-1.

---

### QA7: `varys` node — `## Quotes` — the "for the realm / for the children" motive

- **node:** `varys`
- **section:** `## Quotes`
- **source:** `adwd-epilogue.md:281`
- **verbatim quote:**
> "Forgive me if you can. I bear you no ill will. This was not done from malice. It was for the realm. For the children."

- **companion quote (the Aegon motive statement):** `adwd-epilogue.md:293`
> "Doubt, division, and mistrust will eat the very ground beneath your boy king, whilst Aegon raises his banner above Storm's End and the lords of the realm gather round him."

- **rationale:** Both are already in the harvest queue (`aegon-decomp §8`). Attaching both to the `varys` node's `## Quotes` section captures the Varys voice + makes the MOTIVATES evidence immediately readable from the character node. The `adwd-epilogue.md:293` quote is the canonical source for the `landing MOTIVATES assassinations` causal edge (Lens D).

---

### QA8: `shy-maid` node — `## Quotes` + prose upgrade

- **node:** `shy-maid`
- **section:** `## Quotes`
- **source:** `adwd-tyrion-04.md:83`
- **verbatim quote:**
> "The Shy Maid was a sweet boat. Her draft was so shallow she could work her way up even the smallest of the river's vassal streams, negotiating sandbars that would have stranded larger vessels, yet with her sail raised and a current under her, she could make good speed."

- **source 2:** `adwd-the-lost-lord-01.md:11`
- **verbatim quote:**
> "The Shy Maid was tied up in one of the meaner sections of the long, chaotic riverfront, between a listing poleboat that had not left the pier in years and the gaily painted mummers' barge."

- **rationale:** The Shy Maid's identity section is extremely thin ("an artifact from the AWOIAF wiki"). These two passages anchor the boat's character: shabby-looking by design, surprisingly capable. The `## Quotes` section of the node is currently wiki-only. Book-cite upgrade.

---

## Dropped / considered-but-no

| Item | Why dropped |
|---|---|
| **JonCon's DISGUISED_AS "Griff"** | `DISGUISED_AS` is in vocab, but Griff is not a character node — it's a pseudonym, not an entity. The node already carries "Griff" as an alias. The disguise is captured by the alias; no additional edge needed. |
| **Aegon DISGUISED_AS "Young Griff"** | Same logic — "Young Griff" is already an alias on `aegon-targaryen-young-griff`. The disguise is the alias, not a separate entity. DISGUISED_AS is for persona-swaps where the disguise IS a graph node (e.g., Arya as a boy). |
| **Illyrio GIFTED_TO aegon (candied ginger)** | "There is a gift for the boy in one of the chests. Some candied ginger." (`adwd-tyrion-03.md:53`). Touching but food-trivial; the candied ginger is in `illyrios-chests` node prose already. Skip. |
| **Septa Lemore CREW_OF shy-maid** | She is a passenger-guardian, not crew. The Shy Maid is not her boat. CREW_OF should go to Ysilla (confirmed crew member; takes the tiller; manages the boat day-to-day). Lemore is more naturally TRAVELS_WITH or COMPANION_OF. |
| **`golden-company-standard` artifact node** | The GC's "battle standards of cloth-of-gold" and the deliberate hiding of them during the landing (`adwd-the-griffin-reborn-01.md:151` — "show no banners during these first attacks") is interesting deception but is best captured as prose on the `golden-company` node, not a separate artifact mint. The `golden-skulls` node already exists and covers the adjacent tradition. |
| **Griffin's Roost LOCATED_AT edge from aegon** | `aegon-targaryen-young-griff` arrives at Griffin's Roost 4 days after the taking (`adwd-the-griffin-reborn-01.md:187`). A LOCATED_AT edge would say "Aegon is at Griffin's Roost" — true but thin. The taking event is better: the LOCATED_AT lives on the event (which already exists via taking-of-griffins-roost). |
| **Haldon's cyvasse table as object.artifact** | The table belongs to Haldon's cabin (Shy Maid); the cyvasse pieces get kicked by Aegon. Fun detail but not an independently queryable artifact — the scene is the important thing, captured in QA3 quote attachment. Skip minting. |
| **Vinegar/wine soaks as concept.medical treatment** | Interesting (Lemore prescribes vinegar soaks for greyscale; JonCon uses wine instead to conceal the need; `adwd-the-griffin-reborn-01.md:141`). But "vinegar soak" is a treatment note that belongs as prose on the `greyscale` node, not a separate concept. |
| **`griffins-seat` artifact node** | The carved and gilded Griffin Seat in Griffin's Roost great hall (`adwd-the-griffin-reborn-01.md:41`). Iconic but too thin for a queryable node without more downstream edges. Best as prose on `griffins-roost` location node. |

---

## Harvest

*(Point, don't extract — chapter-file:line / kind / one-line note. Append to `working/harvest-queue.md`.)*

| kind | book | ref | note |
|---|---|---|---|
| food | adwd | adwd-the-lost-lord-01.md:121 | JonCon declines wine at the war council: "We will drink water." — character discipline; also indicates Griff's wartime austerity |
| food | adwd | adwd-the-lost-lord-01.md:119 | Strickland offers wine to guests; Watkyn the squire brings it — hospitality framing at a war council |
| food | adwd | adwd-the-griffin-reborn-01.md:81 | Feast after Griffin's Roost falls: "roast meats and fresh-caught fish, washed down with rich red wines from the castle cellars" — victory feast; hospitality in a retaken seat |
| food | adwd | adwd-the-griffin-reborn-01.md:135 | JonCon's first breakfast as restored lord: "Boiled eggs, fried bread, and beans. And a jug of wine. The worst wine in the cellar." — deliberate choice (worst wine = disguise the vinegar soak); iconic grim meal |
| food | adwd | adwd-tyrion-03.md:147 | First supper on the road with Duck and Haldon: "salt pork and cold white beans, washed down with ale" — austere travel rations; pleasant to Tyrion after Illyrio's richness |
| food | adwd | adwd-tyrion-04.md:65 | Ysilla's morning routine: "bacon and biscuits" (some days biscuits and bacon; once a fortnight a fish) — recurring Shy Maid meal pattern; hospitality from the boat's owner |
| food | adwd | adwd-tyrion-04.md:67 | Ysilla's hot biscuits dripping with honey and butter — specifically "best when eaten hot"; Tyrion snatches one; physical detail of how the Shy Maid feeds its passengers |
| food | adwd | adwd-tyrion-04.md:81 | Ysilla "pressing honeyed biscuits on Young Griff" while hitting Duck's hand — maternal feeding; character texture for Ysilla |
| food | adwd | adwd-tyrion-06.md:161 | Ysilla and Yandry return with provisions from Selhorys: "salt and flour, fresh-churned butter, slabs of bacon wrapped in linen, sacks of oranges, apples, and pears" + "a wine cask" + "a pike as large as Tyrion" — restocking after the Sorrows; the pike gets lemon-grilled over the brazier |
| food | adwd | adwd-tyrion-06.md:161 | Ysilla squeezing lemon onto the pike as it spits over the brazier — specific preparation detail; Rhoyne river fish cooked fresh |
| food | adwd | adwd-epilogue.md:197 | Kevan's supper with Cersei and Tommen: "beef-and-barley soup, brace of quail, roast pike near three feet long, with turnips, mushrooms, and plenty of hot bread and butter"; Boros tastes every dish — KL regency hospitality; taster as security detail |
| food | adwd | adwd-epilogue.md:205 | "cream cakes" — Tommen's favorite; KL royal supper; the domestic normalcy before Varys's attack |
| food | adwd | adwd-epilogue.md:187 | Cersei's supper: "hot spiced wine" poured by a freckled novice — post-walk atonement scene; restrained hospitality |
| description | adwd | adwd-the-lost-lord-01.md:107 | GC officers' wealth on their persons: "jeweled swords, inlaid armor, heavy torcs, and fine silks … every man there wore a lord's ransom in golden arm rings. Each ring signified one year's service." — GC cultural detail; gold arm rings as service markers |
| description | adwd | adwd-the-lost-lord-01.md:107 | Marq Mandrake wears "a chain of golden skulls" in addition to arm rings — individual GC officer description; the skulls-as-ornament tradition extends beyond the battle standards |
| description | adwd | adwd-the-lost-lord-01.md:107 | Black Balaq: "white-haired Summer Islander with skin dark as soot … wore a feathered cloak of green and orange, magnificent to behold" — physical description for a `black-balaq` node quote upgrade |
| description | adwd | adwd-the-lost-lord-01.md:107 | Gorys Edoryen: "leopard skin draped across one shoulder, hair as red as blood in oiled ringlets, pointed beard black" — paymaster's striking appearance; node-prose candidate |
| description | adwd | adwd-the-lost-lord-01.md:107 | Lysono Maar: "Lyseni with lilac eyes and white-gold hair … fingernails painted purple, earlobes dripping with pearls and amethysts. At first glance, Griff had almost taken him for a woman." — spymaster's deliberately androgynous presentation |
| description | adwd | adwd-the-lost-lord-01.md:221 | "The sun was reddening the western sky and painting scarlet shadows on the golden skulls atop their spears" — golden-skulls atmospheric image; end-of-war-council visual |
| description | adwd | adwd-the-griffin-reborn-01.md:19 | Bow hierarchy passage: "crossbows … double-curved horn-and-sinew bows of the east. Better than these were the big yew longbows borne by the archers of Westerosi blood, and best of all were the great bows of goldenheart treasured by Black Balaq himself and his fifty Summer Islanders. Only a dragonbone bow could outrange one made of goldenheart." — weapon-type detail; goldenheart bow placement in the hierarchy |
| description | adwd | adwd-the-griffin-reborn-01.md:55 | JonCon on the tower battlements, Rhaegar's remembered words: "'Your father's lands are beautiful,' Prince Rhaegar had said, standing right where Jon was standing now." — book-cite for JonCon's core emotional wound; the moment collapses past/present |
| description | adwd | adwd-tyrion-04.md:77 | Young Griff's eye description: "by lamplight they turned black, and in the light of dusk they seemed purple. His eyelashes were as long as any woman's." — physical description for `aegon-targaryen-young-griff` node (hair + eyes + eyelashes) |
| description | adwd | adwd-tyrion-05.md:11 | Shy Maid moving through fog "like a blind man groping his way down an unfamiliar hall" — opening image for the stone-men chapter; atmospheric |
| description | adwd | adwd-tyrion-05.md:127 | JonCon's description of stone-men + greyscale progression: "The mortal form of greyscale began in the extremities … the flesh stiffened and grew cold and the victim's skin took on a greyish hue, resembling stone … Blindness was common when the stone reached the face. In the final stages the curse turned inward, to muscles, bones, and inner organs." — medical detail from Tyrion's POV; book-cite upgrade for `greyscale` node prose |
| foreshadowing | adwd | adwd-tyrion-06.md:13 | "He dreamt that they were one and the same [his lord father and the Shrouded Lord], and when his father wrapped stone arms around him and bent to give him his grey kiss, he woke …" — Tyrion's dream fuses Tywin + the Shrouded Lord; greyscale + patricide foreshadowing / parallel |
| foreshadowing | adwd | adwd-tyrion-06.md:155 | "Trust no one. And keep your dragon close." — Tyrion's advice to Aegon; closing line of the cyvasse goad. Foreshadowing of Aegon's vulnerability without Dany's dragons. |
| foreshadowing | adwd | adwd-epilogue.md:297 | Varys's extended Aegon-upbringing speech: "He has lived with fisherfolk, worked with his hands, swum in rivers and mended nets and learned to wash his own clothes at need. He can fish and cook and bind up a wound, he knows what it is like to be hungry, to be hunted, to be afraid." — the contrasting education speech; also Aegon-is-qualified vs. Tommen-is-not; this is the conspiracy's payoff articulation (already in harvest queue §8 but needs node attachment |
| hospitality | adwd | adwd-the-lost-lord-01.md:131 | Strickland soaking blistered toes in a tub of salt water during the war council — the power meeting with the captain-general literally with his feet in a footbath; his squire Watkyn attends with towels; peculiar "hospitality" of a man who cares more for his blisters than for war |
| hospitality | adwd | adwd-the-griffin-reborn-01.md:187 | JonCon releases Yandry and Ysilla: "Give Yandry and Ysilla our thanks. Their part in this is done. They will not be forgotten when His Grace comes into his kingdom." — a form of hospitality-reciprocity; the poleboat owners who sheltered the prince for years are rewarded with royal gratitude and release |

---

## Summary for the build agent

**2 new nodes to mint:**
1. `illyrios-ruby-chain` (object.artifact) — Illyrio's gift to Aegon, adwd-the-lost-lord-01.md:61
2. `varys-crossbow` (object.artifact) — the assassination weapon, adwd-epilogue.md:269

**Core edges to propose (priority order):**
1. `jon-connington --AFFLICTED_BY--> greyscale` (tier 1; **highest priority** — orphans the greyscale node if not done)
2. `yandry --CAPTAIN_OF--> shy-maid` (tier 2)
3. `ysilla --CREW_OF--> shy-maid` (tier 2)
4. `illyrio-mopatis --GIFTED_TO--> aegon-targaryen-young-griff` via illyrios-ruby-chain (tier 1)
5. `aegon-targaryen-young-griff --OWNS--> illyrios-ruby-chain` (tier 1)
6. `varys --WIELDS--> varys-crossbow` (tier 1)
7. `varys-crossbow --WIELDED_IN--> assassinations-of-pycelle-and-kevan-lannister` (tier 1)
8. `black-balaq --COMMANDS_IN--> landing-of-the-golden-company` (tier 1)
9. `haldon --CREW_OF--> shy-maid`, `rolly-duckfield --CREW_OF--> shy-maid` (tier 2)

**Quote attachments (7 existing nodes enriched):**
- `aegon-targaryen-young-griff` × 3 quotes (disguise, sail-west, cyvasse fury)
- `jon-connington` × 1 quote (death-clock paragraph)
- `greyscale` × 1 quote (book-cite upgrade of concealment passage)
- `golden-skulls` × 2 quotes (book-cite upgrade of Myles/Bittersteel passage + JonCon's vow)
- `varys` × 2 quotes (for-the-realm + Aegon-motive)
- `shy-maid` × 2 quotes (node identity upgrade)

**Harvest:** 26 food/description/foreshadowing/hospitality items pointed for `working/harvest-queue.md`.
