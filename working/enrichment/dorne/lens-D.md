# Lens D — Cross-arc causal wiring — A1.5 Dorne proposal (S156)

## Summary

Dedup confirmed: `murder-of-elia... MOTIVATES doran-martell` does NOT exist (only `...MOTIVATES oberyn-martell` and `...MOTIVATES doran-reveals-fire-and-blood-pact`). No `CLAIMS iron-throne` edges exist anywhere. `the-queenmaker-plot` has cIn=4 (all AGENT_IN / VICTIM_IN, no causal upstream). `myrcella-is-maimed-by-darkstar` has cOut=0. `death-of-quentyn-martell` has cOut=0.

Proposing 7 new edges across 4 cross-arc seams. No new nodes needed.

---

## Proposed NEW nodes

None. All proposed edges connect already-built nodes.

---

## Proposed NEW edges

### Seam 1: Dorne ↔ Sack-of-KL — `murder-of-elia... MOTIVATES doran-martell`

**D-1**
`murder-of-elia-martell-and-rhaegars-children` **MOTIVATES** `doran-martell` | Tier-1 |
Quote: `"He butchered my good sister, smashed her babe's head against a wall. I only pray that now he is burning in some hell, and that Elia and her children are at peace."` `adwd-the-watcher-01:39`
Rationale: Doran's only unprompted public statement about Elia names the murder as the blood debt at the heart of his patience — "This is the justice that Dorne has hungered for." The murder of his sister is explicitly the wound Doran has nursed for seventeen years, the same motive substrate that drives the pact, the long-game, and his refusal to spend Dornish lives cheaply. MOTIVATES→character is correct (the event drives an actor's disposition). Tier-1 because the quote is direct first-person attribution in the chapter, not inference. This is the missing Sack-of-KL ↔ Dorne seam: `murder-of-elia MOTIVATES oberyn` already exists; `murder-of-elia MOTIVATES doran` is the parallel wire that the graph currently lacks, leaving Doran's long-game without its stated root cause.

---

### Seam 2: Dorne ↔ Iron Throne — `myrcella-baratheon CLAIMS iron-throne`

**D-2**
`myrcella-baratheon` **CLAIMS** `iron-throne` | Tier-2 |
Quote: `"She is older than her brother. By law the Iron Throne should pass to her."` `affc-the-captain-of-guards-01:283`
Rationale: Tyene lays out the Dornish-law argument in full in this chapter (Myrcella > Tommen under the principle that Dorne agreed to Dornish law at the Daeron-Myriah marriage; Myrcella is in Dorne; ergo the throne is hers by law). The same argument is repeated by Arianne in the Soiled Knight chapter. This is the plot's whole premise — the Queenmaker plot exists *because* Myrcella has this claim. Tier-2 because Dornish law is disputed by Westerosi custom ("By Dornish law" / "The Seven Kingdoms have never had a ruling queen" — Doran's own qualifier at line 285). The claim is real but not universally acknowledged = Tier-2 per architecture. The edge wires the Queenmaker arc into the Iron Throne node, which has cIn of 3 and currently has no connection to the entire Dorne arc despite the arc being defined by an Iron Throne succession argument. No `CLAIMS iron-throne` edges exist anywhere in the graph; this is the first.

---

### Seam 3: Dorne ↔ Iron Throne — `the-queenmaker-plot SEEKS iron-throne`

**D-3**
`the-queenmaker-plot` **SEEKS** `iron-throne` | Tier-1 |
Quote: `"That means the Iron Throne by rights is yours. Your brother is only a little boy, you must not blame him."` `affc-the-queenmaker-01:117`
Rationale: The Queenmaker plot's explicit stated purpose is to place Myrcella on the Iron Throne. This is Arianne's own words to Myrcella at the crowning attempt. SEEKS (claimant/pursuer → sought object/office) is the correct type for an event-node's goal. Gap 1 in baseline.md explicitly calls out `the-queenmaker-plot` having no GOAL edge (cIn=0 on upstream cause, no outward goal edge either). This wires the plot to what it is actually pursuing.

---

### Seam 4: Dorne ↔ AEGON container — Doran's long-game motive substrate

**D-4**
`murder-of-elia-martell-and-rhaegars-children` **MOTIVATES** `doran-reveals-fire-and-blood-pact` | Tier-2 |

DEDUP CHECK REQUIRED: Line 22703 of edges.jsonl shows this edge ALREADY EXISTS (typed by `curator-sack-kl-enrichment`, run_id `sack-kl-enrichment-s142`). **DO NOT re-mint. Marked as found-during-dedup.**

---

### Seam 5: Maiming → Diplomatic damage control

**D-5**
`myrcella-is-maimed-by-darkstar` **MOTIVATES** `doran-martell` | Tier-2 |
Quote: `"Ser Balon must arrive at Sunspear, and when he does he will expect to see Princess Myrcella . . . and Ser Arys, his Sworn Brother. What shall we tell him, Arianne?"` `affc-the-princess-in-the-tower-01:229`
Rationale: In the "Princess in the Tower" chapter Doran's entire conversation with Arianne is structured around the *diplomatic emergency* the maiming has created. He explicitly says the situation may produce war ("if Myrcella should perish whilst in my care . . . it will mean war"). In "The Watcher" he deploys Balon Swann, Nymeria, Obara, and Tyene in direct response to the maiming's fallout: the cover story (Darkstar did it), the hunt for Gerold Dayne, Nymeria escorting Myrcella back, Tyene placed near the Faith. The maiming event creates the damage Doran must manage, and the chapter shows him actively managing it. MOTIVATES→character (event drives Doran's orchestrated response), Tier-2 because the causal chain is one short step of inference (the maiming creates a crisis, the crisis compels action) rather than an explicit statement of motive.

**[BORDERLINE NOTE]** The maiming TRIGGERS the damage-control need, but Doran's multi-pronged response in adwd-the-watcher-01 is clearly framed as his reaction *to* Myrcella's scarred face arriving back at court. The MOTIVATES framing is slightly weaker than CAUSES (the maiming didn't *produce* a new decision-node, it drove Doran's contingency response). Flag for gate review — could alternatively be `myrcella-is-maimed-by-darkstar CAUSES doran-dispatches-sand-snakes` but that event hub does not exist. MOTIVATES→doran-martell is cleaner and within-scope.

---

### Seam 6: Sand Snake missions wired to their ADWD destinations (cOut gaps)

The adwd-the-watcher-01 chapter explicitly dispatches three Sand Snakes on named missions: Obara to High Hermitage (hunt Darkstar), Nymeria to escort Myrcella back to KL, Tyene to cultivate the High Sparrow. None of these TRAVELS_TO edges exist (confirmed: nymeria-sand has 4 out-edges, none TRAVELS_TO; obara-sand has 5 out-edges, none TRAVELS_TO; tyene-sand has 4 out-edges, none TRAVELS_TO). However, these are **mission dispatch edges**, not cross-arc seams, and properly belong to Lens A or Lens B (per-character/event wiring). I flag them here for the synthesis orchestrator and decline to claim them as Lens D's cross-arc seams.

**D-6** [LOW PRIORITY — for synthesis consideration]
`nymeria-sand` **TRAVELS_TO** `kings-landing` | Tier-1 |
Quote: `"That task will be yours, Nymeria."` `adwd-the-watcher-01:227`
Rationale: Doran explicitly assigns Nymeria to escort Myrcella to KL. TRAVELS_TO wires her into the capital arc. Flag for synthesis — Lens D notes it but does not claim it as a primary cross-arc seam.

**D-7** [LOW PRIORITY — for synthesis consideration]
`obara-sand` **TRAVELS_TO** `high-hermitage` | Tier-1 |
Quote: `"Obara, you will lead him to High Hermitage to beard Darkstar in his den."` `adwd-the-watcher-01:227`
Rationale: Doran assigns Obara to lead Balon Swann to High Hermitage to hunt Gerold Dayne. TRAVELS_TO grounds the mission. Flag for synthesis.

---

## Dropped / considered-but-rejected

**`murder-of-elia MOTIVATES doran-reveals-fire-and-blood-pact`** — Already exists (line 22703, run `sack-kl-enrichment-s142`). Deduped.

**`arianne-martell CLAIMS iron-throne`** — Wrong agent. Arianne is not claiming the throne for herself; she is making the claim *on Myrcella's behalf*. The claimant is Myrcella (D-2). Arianne's role is AGENT_IN the-queenmaker-plot, which already exists.

**`the-queenmaker-plot MOTIVATES arianne-martell`** — Backwards. The plot doesn't motivate Arianne; Arianne's motive (fear of disinheritance + desire to free Sand Snakes) is what produces the plot. The upstream MOTIVATES already exists: `arrest-of-the-sand-snakes MOTIVATES arianne-martell` (line 22314). Her inheritance-fear motive is node-prose.

**`myrcella-is-maimed-by-darkstar CAUSES <diplomatic-crisis>`** — No event hub for the diplomatic crisis exists. The downstream is routed through MOTIVATES doran-martell (D-5) rather than minting a new event node.

**`doran-martell SEEKS vengeance`** — The `doran-martell SEEKS elia-martell` edge already exists (line 1520, "seeks vengeance for" — pass1-derived). Adding a second SEEKS→vengeance node would be redundant.

**`death-of-quentyn-martell` downstream seams** — cOut=0, but all legitimate downstreams involve TWOW material (Arianne's TWOW chapters, the Dornish reaction). No published-text evidence in the 5 in-scope chapters supports a downstream causal edge from Quentyn's death. Correctly terminal in current scope.

**Doran's patience as ENABLES the pact** — `arianne-collapses-and-is-captured CAUSES doran-reveals-fire-and-blood-pact` already exists in the spine. Adding Doran's patience as an ENABLES precondition would create a redundant causal loop. The patience is character-trait node-prose, not a graph edge.

**`myrcella-baratheon ENABLES the-queenmaker-plot`** — False. Myrcella doesn't enable the plot; the plot acts upon her without her consent (she's confused and asks "did something bad happen to Tommen?"). Her role is correctly VICTIM_IN (existing).

**Arianne's intercepted-letter discovery as MOTIVATES** — The letter she found in her father's solar (convincing her Doran meant to disinherit her for Quentyn) is the deepest upstream motive for the Queenmaker plot. Arianne describes it in affc-the-soiled-knight-01:249 and affc-the-princess-in-the-tower-01:281. However: (a) there is no `arianne-reads-doran-letter` event node, and minting new event nodes is not in Lens D's scope; (b) the motive is character-internal, correctly placed in Arianne's node prose; (c) Lens A likely covers this. Flagged for synthesis — if an event node for the letter-discovery already exists or is minted by another lens, `that-event MOTIVATES arianne-martell` would be Tier-1 clean.

**`the-queenmaker-plot SEEKS iron-throne` redundancy concern** — This overlaps with D-2 (`myrcella CLAIMS iron-throne`), but they're complementary: D-2 names the legal claimant; D-3 names the conspiratorial mechanism. Both are needed for the graph to be traversable from the plot-event to the political target. Proposed both.

---

## Harvest

| kind | book | chapter:line | note |
|---|---|---|---|
| food | affc | affc-the-captain-of-guards-01:153 | Doran's dinner under the orange trees at Water Gardens — purple olives, flatbread, cheese, chickpea paste, sweet strongwine. |
| food | affc | affc-the-captain-of-guards-01:11 | Blood oranges overripe on the Water Gardens pink marble terrace — tart-sweet smell fills the air; load-bearing motif for the opening scene. |
| food | affc | affc-the-princess-in-the-tower-01:47 | Arianne's prison meal: "kid had been roasted with lemon and honey…grape leaves stuffed with a mélange of raisins, onions, mushrooms, and fiery dragon peppers." |
| food | adwd | adwd-the-watcher-01:51 | Seven-course feast: egg-and-lemon soup, stuffed long green peppers, lamprey pies, honey-glazed capons, giant whiskerfish from the Greenblood, savory snake stew (seven kinds of snake + dragon peppers + blood oranges + venom), sherbet, spun-sugar skulls with sweet custard + plum + cherry inside. Full Dornish register. |
| food | adwd | adwd-the-watcher-01:43 | Dornish strongwine "dark as blood and sweet as vengeance" — Doran drinks only his own wine "well laced with poppy juice." |
| food | affc | affc-the-soiled-knight-01:21 | Snake chunks grilled on a brazier outside a shop, turned with wooden tongs; "best snake sauce had a drop of venom in it, along with mustard seeds and dragon peppers." |
| food | affc | affc-the-queenmaker-01:239 | Rest halt: "dates and cheese and olives, and lemonsweet to drink." Garin eats olives and spits stones at Drey. Myrcella splits an orange with Spotted Sylva. |
| description | affc | affc-the-queenmaker-01:31 | Darkstar physical description: "aquiline nose, high cheekbones, a strong jaw…thick hair fell to his collar like a silver glacier, divided by a streak of midnight black…eyes seemed black…but they were purple. Dark purple. Dark and angry." |
| description | affc | affc-the-captain-of-guards-01:217 | Sunspear tower descriptions: "slender Spear Tower, a hundred-and-a-half feet tall and crowned with a spear of gilded steel that added another thirty feet"; Tower of the Sun "with its dome of gold and leaded glass"; the Sandship "looking like some monstrous dromond that had washed ashore." |
| description | adwd | adwd-the-watcher-01:17 | Areo Hotah's appearance at the feast: "shirt of copper scales mirror-bright"; the chest of ebony with silver clasps; Gregor's skull on black marble pedestal. |
| description | adwd | adwd-the-watcher-01:191 | Physical description of Sand Snakes at the feast: Obara "angry mannish look… breeches and calf-length linen tunic, cinched with copper suns"; Nymeria "gown of yellow silk so sheer the candles shone right through it"; Tyene "cream and green, with long lace sleeves, so modest and so innocent." |
| quote | affc | affc-the-princess-in-the-tower-01:325 | Load-bearing verbatim: `"Vengeance." … "Justice." … "Fire and blood."` — Doran's three-word revelation to Arianne. Already cited at line 22703; confirm as node ## Quotes entry for `doran-reveals-fire-and-blood-pact`. |
| quote | affc | affc-the-princess-in-the-tower-01:243 | `"I have worked at the downfall of Tywin Lannister since the day they told me of Elia and her children."` — Doran to Arianne; strong evidence anchor for murder-of-elia MOTIVATES doran-martell (D-1, secondary quote). |
| quote | adwd | adwd-the-watcher-01:39 | `"He butchered my good sister, smashed her babe's head against a wall."` — Doran's public statement naming the blood debt (D-1 primary quote). |
| quote | adwd | adwd-the-watcher-01:189 | `"I am not blind, nor deaf. I know that you all believe me weak, frightened, feeble. … I was the grass. Pleasant, complaisant, sweet-smelling, swaying with every breeze. … But it is the grass that hides the viper from his enemies."` — Doran's "grass and viper" speech; key character node quote. |
| quote | affc | affc-the-soiled-knight-01:275 | Arys's sworn vow to Arianne: `"My sword, my life, my honor, all belong to her … and to you, my heart's delight."` — load-bearing for VOWS_TO + the oath-breaking arc. |
| foreshadowing | affc | affc-the-captain-of-guards-01:135 | Hotah's premonition: "One day, he sensed, the two of them would fight; on that day Oakheart would die, with the captain's longaxe crashing through his skull." — fulfilled in affc-the-queenmaker-01:289. Strong Chekhov's gun. |
| hospitality | adwd | adwd-the-watcher-01:225 | Doran explicitly invokes guest right: "Ser Balon is a guest beneath my roof. He has eaten of my bread and salt. I will not do him harm." — bread-and-salt hospitality protection asserted by name. |
| hospitality | affc | affc-the-captain-of-guards-01:49 | Water Gardens hospitality tradition: Princess Daenerys (Targaryen bride) invited children of grooms and cooks to share the pools — egalitarian water hospitality extended across class lines, persisting as tradition. |
