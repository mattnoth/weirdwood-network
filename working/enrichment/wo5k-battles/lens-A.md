# Lens A — spine + commander/combatant cast — A2.5 WO5K-battles proposal (S163, PASS 1)

---

## Proposed NEW nodes

### `battle-of-the-whispering-wood`
- **slug:** `battle-of-the-whispering-wood`
- **type:** `event.battle`
- **name:** Battle of the Whispering Wood
- **body:** Night ambush in a wooded valley near Riverrun in which Robb Stark's 6,000 cavalry trapped and
  destroyed three-quarters of Jaime Lannister's horse, capturing Jaime himself. Robb's force occupied ridges
  on both sides and at both ends of the valley; the Blackfish's outriders had blinded Jaime's scouts so the
  Lannisters rode into the trap unawares. Grey Wind's howl opened the battle. The victory broke Jaime's
  command, enabling the subsequent Battle of the Camps.
- **anchor quote:** `"The whispering wood let out its breath all at once, as the bowmen Robb had hidden in the
  branches of the trees let fly their arrows and the night erupted with the screams of men and horses."`
  — agot-catelyn-10:85

---

## Proposed NEW edges

### NEW HUB — `battle-of-the-whispering-wood` existence + location

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `battle-of-the-whispering-wood` | `LOCATED_AT` | `whispering-wood` | Tier 1 | — | `"Here was a hush in the night, moonlight and shadows, a thick carpet of dead leaves underfoot, densely wooded ridges sloping gently down to the streambed"` agot-catelyn-10:73 | The battle is definitionally set in the Whispering Wood. |

---

### CAUSAL SPINE (the high-value work)

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `battle-on-the-green-fork` | `ENABLES` | `battle-of-the-whispering-wood` | Tier 2 | — | `"Robb had commanded him to continue the march south, to confront the huge Lannister army coming north under Lord Tywin."` agot-catelyn-09:257 | Robb split the host deliberately: foot + Bolton down the kingsroad to draw Tywin, horse west to strike Jaime. The Green Fork battle (the feint) occupied Tywin, leaving Jaime without reinforcement. This is a military precondition, not a forced consequence — Robb chose to spring the trap — so ENABLES, not CAUSES. |
| `battle-of-the-whispering-wood` | `ENABLES` | `battle-of-the-camps` | Tier 1 | — | `"unaware of their commander's defeat"` — (see cat-11; Hoster's account: "Ah, that was beautiful … the torches came in a wave … when that siege tower went up") agot-catelyn-11:63 | Jaime's capture left the three Lannister siege camps leaderless. The text is explicit: the Camps host attacked an enemy that did not yet know Jaime had fallen. This is the proximate precondition. ENABLES because Robb still had to choose and execute the assault. |
| `battle-of-the-camps` | `ENABLES` | `robb-proclaimed-king-in-the-north` | Tier 2 | — | `"Word of the victory at Riverrun had spread to the fugitive lords of the Trident, drawing them back."` agot-catelyn-11:143 | The two victories (Wood + Camps) re-assembled the river lords at Riverrun, creating the war council where Robb was proclaimed. `execution-of-eddard-stark CAUSES robb-proclaimed-king-in-the-north` already exists (S113) — this edge is the MILITARY precondition on a separate axis. ENABLES because the lords freely chose to proclaim him. |

---

### PARTICIPANT ROLES on `battle-of-the-whispering-wood` (the marquee build)

**Robb Stark — COMMANDS_IN + AGENT_IN**

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `robb-stark` | `COMMANDS_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"'Winterfell!' she heard Robb shout as the arrows sighed again. He moved away from her at a trot, leading his men downhill."` agot-catelyn-10:85 | Robb devised and commanded the trap. |
| `robb-stark` | `AGENT_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"Robb raised his head and pushed his hair back out of his eyes."` / `"This is … Torrhen's blood, perhaps, or …"` agot-catelyn-10:99 | Robb rode down into the valley and fought; blood on his glove confirms personal combat participation. |

**Grey Wind — FIGHTS_IN + AGENT_IN**

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `grey-wind` | `FIGHTS_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"she heard his direwolf, snarling and growling, heard the snap of those long teeth, the tearing of flesh, shrieks of fear and pain from man and horse alike"` agot-catelyn-10:93 | Grey Wind fought actively in the wood. Confirmed by Theon's account: "The Lannisters must have thought the Others themselves were on them when that wolf of Robb's got in among them. I saw him tear one man's arm from his shoulder." agot-catelyn-11:117 |
| `grey-wind` | `AGENT_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"And Grey Wind threw back his head and howled."` agot-catelyn-10:79 | Grey Wind's howl OPENS the battle (Maege's warhorn signals all in; then the wolf howls). Active participant, not bystander. |

**Brynden Tully — COMMANDS_IN + AGENT_IN**

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `brynden-tully` | `COMMANDS_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"'Jaime does not know,' Ser Brynden said when he rode back. 'I'll stake my life on that. No bird has reached him, my archers have seen to that. We've seen a few of his outriders, but those that saw us did not live to tell of it.'"` agot-catelyn-10:31 | The Blackfish led the three hundred picked men who screened the march and eliminated Jaime's outriders, directly enabling the trap. He drew Jaime out (per cat-10:69: "He has ridden out with his knights thrice already, to chase down raiders"). His intelligence and screen were the tactical linchpin. |
| `brynden-tully` | `AGENT_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"Robb had given the Blackfish three hundred picked men, and sent them ahead to screen his march."` agot-catelyn-10:31 | The Blackfish's three-hundred-man force was an integral part of the battle operation (screening and luring). |

**Maege Mormont — FIGHTS_IN**

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `maege-mormont` | `FIGHTS_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"Here was the call of Maege Mormont's warhorn, a long low blast that rolled down the valley from the east, to tell them that the last of Jaime's riders had entered the trap."` agot-catelyn-10:77 | Maege personally sounded the battle-start signal from the east ridge — she is present in the wood, not a distant commander. |

**Jon Umber (the Greatjon) — FIGHTS_IN**

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `jon-umber` | `FIGHTS_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"HAAroooooooooooooooooooooooo came the answer from the far ridge as the Greatjon winded his own horn."` agot-catelyn-10:83 | Greatjon commanded/occupied the far (west) ridge, answering Maege's signal. Present and fighting. |

**Rickard Karstark — FIGHTS_IN**

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `rickard-karstark` | `FIGHTS_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"North, where the valley narrowed and bent like a cocked elbow, Lord Karstark's warhorns added their own deep, mournful voices to the dark chorus."` agot-catelyn-10:83 | Karstark commanded the northern blocking force that sealed the valley. Two of his sons died there. |

**Galbart Glover — FIGHTS_IN**

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `galbart-glover` | `FIGHTS_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"No one can fault Lannister on his courage," Glover said. "When he saw that he was lost, he rallied his retainers and fought his way up the valley, hoping to reach Lord Robb and cut him down."` agot-catelyn-10:131 | Glover is present at the post-battle scene reporting on Jaime's final push — present in the wood as a combatant lord. |

**Jason Mallister — FIGHTS_IN**

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `jason-mallister` | `FIGHTS_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"Lord Jason Mallister had brought his power out from Seagard to join them as they swept around the headwaters of the Blue Fork and galloped south"` agot-catelyn-10:45; `"the trumpets of the Mallisters and Freys blew vengeance"` agot-catelyn-10:83 | Mallister joined the host before the battle and his trumpets sound in the valley. |

**Jaime Lannister — COMMANDS_IN + VICTIM_IN**

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `jaime-lannister` | `COMMANDS_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"Even at a distance, Ser Jaime Lannister was unmistakable. The moonlight had silvered his armor and the gold of his hair, and turned his crimson cloak to black. He was not wearing a helm."` agot-catelyn-10:65 | Jaime led his host into the valley personally; he commanded the Lannister cavalry. |
| `jaime-lannister` | `VICTIM_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"Between them they dragged Ser Jaime Lannister. They threw him down in front of her horse."` agot-catelyn-10:101 | Jaime captured; primary outcome of the battle. |

**Robb Stark DEFEATS Jaime Lannister**

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `robb-stark` | `DEFEATS` | `jaime-lannister` | Tier 1 | — | `"A mob of men followed him up the slope, dirty and dented and grinning, with Theon and the Greatjon at their head. Between them they dragged Ser Jaime Lannister."` agot-catelyn-10:101 | The decisive outcome of the battle: Robb's host defeats and captures Jaime. |

**Named Lannister prisoners/casualties**

Theon's accounting at cat-10:137 names multiple Lannister captives:
> `"we've taken close to a hundred knights captive, and a dozen lords bannermen. Lord Westerling, Lord Banefort, Ser Garth Greenfield, Lord Estren, Ser Tytos Brax, Mallor the Dornishman … and three Lannisters besides Jaime, Lord Tywin's own nephews, two of his sister's sons and one of his dead brother's …"` — agot-catelyn-10:137

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `ser-tytos-brax` | `VICTIM_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"Ser Tytos Brax"` agot-catelyn-10:137 | Named captive; text is explicit. |
| `lord-westerling` | `VICTIM_IN` | `battle-of-the-whispering-wood` | Tier 2 | — | `"Lord Westerling, Lord Banefort, Ser Garth Greenfield, Lord Estren"` agot-catelyn-10:137 | Named among the captured dozen lords. Tier 2 because first names are not given and node resolution may be imprecise. |

**Casualties among Robb's battle guard**

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `torrhen-karstark` | `VICTIM_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"He mislaid his sword in Eddard Karstark's neck, after he took Torrhen's hand off and split Daryn Hornwood's skull open"` agot-catelyn-10:133 | Torrhen Karstark killed by Jaime during Jaime's final charge. |
| `eddard-karstark` | `VICTIM_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"He mislaid his sword in Eddard Karstark's neck"` agot-catelyn-10:133 | Eddard Karstark killed by Jaime. |
| `daryn-hornwood` | `VICTIM_IN` | `battle-of-the-whispering-wood` | Tier 1 | — | `"split Daryn Hornwood's skull open"` agot-catelyn-10:133 | Daryn Hornwood killed by Jaime. |

**Jaime kills Robb's guards (KILLS dyads — Jaime as agent)**

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `jaime-lannister` | `KILLS` | `torrhen-karstark` | Tier 1 | — | `"he took Torrhen's hand off and split Daryn Hornwood's skull open"` / `"He mislaid his sword in Eddard Karstark's neck"` agot-catelyn-10:133 | Jaime personally kills Torrhen Karstark (severed hand → fatal), Eddard Karstark, and Daryn Hornwood during his charge at Robb. Combining into one cite is the most honest — the text lists all three in sequence. |
| `jaime-lannister` | `KILLS` | `eddard-karstark` | Tier 1 | — | `"He mislaid his sword in Eddard Karstark's neck"` agot-catelyn-10:133 | Verbatim. |
| `jaime-lannister` | `KILLS` | `daryn-hornwood` | Tier 1 | — | `"split Daryn Hornwood's skull open"` agot-catelyn-10:133 | Verbatim. |

---

### CAMPS — missing roles (dedup against the 11 existing)

Existing: robb/jaime/brynden COMMANDS_IN, jon-umber/grey-wind/forley-prester/tytos-blackwood FIGHTS_IN,
edmure/andros-brax VICTIM_IN, hoster-tully WITNESS_IN. Do NOT re-propose.

**Tytos Blackwood's sortie freeing Edmure**
> `"It had been Lord Tytos who led the sortie that plucked her brother from the Lannister camp."` — agot-catelyn-11:19

Tytos Blackwood FIGHTS_IN is already live. But his specific RESCUES action is not.

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `tytos-blackwood` | `RESCUES` | `edmure-tully` | Tier 1 | — | `"It had been Lord Tytos who led the sortie that plucked her brother from the Lannister camp."` agot-catelyn-11:19 | The text is explicit and unique. This is distinct from FIGHTS_IN (which already exists). |

**Karyl Vance and Marq Piper — the raiders who masked Robb's approach**

Cat-08:123 establishes that Vance and Piper had been harassing the Lannister advance (and Lord Vance was killed at the Golden Tooth fighting Jaime). The surviving Ser Karyl Vance (who inherited after his father's death) and Ser Marq Piper appear at the war council in cat-11 as refugee river lords who were drawn back by the victory. Do they belong on `battle-of-the-camps`?

The text does NOT anchor either Vance or Piper to the Camps battle itself — they appear at the **aftermath** war council (cat-11:143), not during the fighting. Their raids pre-date the Camps (before Robb arrived). **[BORDERLINE]** — I flag this for the synthesis gate rather than dropping it outright.

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `karyl-vance` | `FIGHTS_IN` | `battle-of-the-camps` | Tier 3 | — | `"Karyl Vance came in, a lord now, his father dead beneath the Golden Tooth"` agot-catelyn-11:143 | **[BORDERLINE]** Karyl Vance's father died fighting Jaime near Riverrun, and Karyl appears at the post-victory council. His pre-Camps raid against Jaime's foragers likely harassed Jaime's line, but the text does not name him as a Camps combatant. Tier 3 structural inference only. |
| `marq-piper` | `FIGHTS_IN` | `battle-of-the-camps` | Tier 3 | — | `"Ser Marq Piper was with him"` agot-catelyn-11:143 | **[BORDERLINE]** Same logic as Vance. No explicit Camps role. Tier 3. |

---

### SIEGE OF RIVERRUN seam

The Whispering Wood + Camps broke the siege. Does `battle-of-the-camps DEFEATS siege-of-riverrun` work? The edge type DEFEATS is (victor → defeated); the `siege-of-riverrun` is an event, not a person. Better options:

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `battle-of-the-camps` | `ENABLES` | `siege-of-riverrun` | Tier 1 | — | `"Riverrun is free again, Father."` agot-catelyn-11:61 | **[BORDERLINE on edge direction]** The Camps ended the siege — but ENABLES implies A makes B possible, not terminates it. The proper logic is: the Camps CAUSED the siege to END, but `siege-of-riverrun` is the event that began, not the "lifting." Consider proposing a separate event `relief-of-riverrun` or use `battle-of-the-camps CAUSES [the-siege-lifting]`. Flagging for synthesis. |

Alternative I prefer: `battle-of-the-whispering-wood ENABLES battle-of-the-camps` → `battle-of-the-camps` (already existing) ends the siege. If the synthesis wants to wire the siege directly, a `battle-of-the-camps ENABLES [lifting-of-siege-of-riverrun]` with a CAUSES edge from camps to the siege-conclusion is the clean path. I am NOT proposing `battle-of-the-camps ENABLES siege-of-riverrun` because the direction is backwards (siege was already in progress; the battle terminates it).

---

### SUSPICIOUS EXISTING EDGES — FLAG

Per baseline.md, two existing edges are suspicious:

1. **`roose-bolton CAPTURES jaime-lannister` (Tier 1) — WRONG.** The four source chapters confirm Roose Bolton was sent down the kingsroad with the FOOT to face Tywin Lannister on the Green Fork (cat-08:257, cat-09:257). He was nowhere near the Whispering Wood. The Whispering Wood was Robb's CAVALRY operation west of the Green Fork. Roose was on the east bank. This edge should be flagged as a bug_drop or reassigned. The capture was by Robb's cavalry host collectively (and Robb receives credit as COMMANDS_IN / AGENT_IN).
   - Quote ruling Roose out: `"The larger part of the northern host, pikes and archers and great masses of men-at-arms on foot, remained upon the east bank under the command of Roose Bolton."` agot-catelyn-09:257

2. **`catelyn-stark CAPTURES jaime-lannister` (Tier 1) — WRONG / MISCHARACTERIZED.** Catelyn waited outside the wood on the ridge with 30 guards. She did not participate in the capture. She received Jaime when he was thrown at her horse's feet. The text: `"They threw him down in front of her horse."` agot-catelyn-10:101. She then gave the order to take him away and put him in irons (cat-10:117), which is command authority, but not "captures." This edge should be flagged as a bug_drop. Catelyn's role here could at most be `COMMANDS_IN` (as the political authority) or `WITNESS_IN` (but she didn't see the battle; she heard it). Neither is `CAPTURES`.

---

### STRATEGIC PLAN — robb-stark splits the host (cat-08 causal seed)

| source | edge | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|------|--------|------|-----------|-----------------------|-----------|
| `robb-stark` | `COMMANDS` | `roose-bolton` | Tier 1 | — | `"Robb had commanded him to continue the march south, to confront the huge Lannister army coming north under Lord Tywin."` agot-catelyn-09:257 | Robb explicitly gives Bolton his orders. Check if this dyad already exists — it may; flag if so. **[CHECK DEDUP — likely exists given roose's 52 edges]** |

---

## Dropped / considered-but-rejected

- **`robb-stark CAPTURES jaime-lannister`** — This dyad almost certainly already exists (see baseline's note on suspicious existing edges, and Jaime's 157-edge saturation). The better frame is `jaime-lannister VICTIM_IN battle-of-the-whispering-wood` + `robb-stark AGENT_IN/COMMANDS_IN`, which I have proposed. The bare CAPTURES dyad is not re-proposed.

- **`grey-wind WARGS_INTO` or warg bond to Robb at the battle** — Theory-gated. The text shows Grey Wind's howl opens the battle and he fights in the wood, but warg-mechanics here are theory reading (grey-wind is not POV). Not proposing.

- **`catelyn-stark WITNESS_IN battle-of-the-whispering-wood`** — The LENS-SHARED note is explicit: `WITNESS_IN` requires the character to ACTUALLY SEE the incident. Catelyn was on the ridge above, trees hid most of the battle, she heard rather than saw it: `"She was high on the ridge, and the trees hid most of what was going on beneath her."` agot-catelyn-10:87. She is NOT a witness by the schema definition. Dropped.

- **`theon-greyjoy FIGHTS_IN battle-of-the-whispering-wood`** — Theon is named as one of Robb's battle guard (cat-10:53: `"Theon Greyjoy, no less than five of Walder Frey's vast brood"`) and appears in the post-battle crowd dragging Jaime (cat-10:101). He is present and his account of the battle in cat-11:117 shows first-person knowledge. However, his dyadic web is likely saturated (not separately checked — flagging as probable but not proposing without dedup confirmation). **If `theon-greyjoy FIGHTS_IN battle-of-the-whispering-wood` does not exist, it is a valid Tier-1 proposal** (`"Theon Greyjoy, no less than five of Walder Frey's vast brood"` agot-catelyn-10:53).

- **`smalljon-umber FIGHTS_IN battle-of-the-whispering-wood`** — Named in Robb's battle guard (cat-10:53: `"Smalljon Umber"`). Valid Tier-1 candidate. Not proposing here as the node may not exist yet; flagging for synthesis.

- **`dacey-mormont FIGHTS_IN battle-of-the-whispering-wood`** — Named in Robb's battle guard (cat-10:53: `"Dacey Mormont, Lady Maege's eldest daughter and heir to Bear Island"`). Valid Tier-1 candidate. Dacey's node existence uncertain; flagging for synthesis.

- **`daryn-hornwood FIGHTS_IN battle-of-the-whispering-wood`** — Daryn Hornwood is named in Robb's battle guard (cat-10:53) and killed in the battle (cat-10:133). He is VICTIM_IN already proposed. Could also be FIGHTS_IN. Leaving as VICTIM_IN for synthesis to add the dual role if desired.

- **`olyvar-frey PARTICIPATES_IN battle-of-the-whispering-wood`** — Olyvar held Robb's horse before the battle (cat-10:47: `"Olyvar Frey held his horse for him"`). He is Robb's squire, likely in the rear area. Not in the valley. Not proposing; purely support role, not combat.

- **Frey trumpets in the valley (cat-10:83: `"the trumpets of the Mallisters and Freys"`)** — The Frey contingent was present (Robb crossed with nine-tenths of his horse from the Twins, including Frey men). However, no individual Frey lord is named as a combatant in the wood. The Frey force is an undifferentiated sub-unit here. Dropped.

- **`battle-of-the-camps` — Marq Piper + Karyl Vance as raiders** — The pre-Camps Lannister/Tully skirmishing is noted in cat-08 (Vance/Piper held the pass; Lord Vance senior died). Their raids before the battle masked Robb's approach. However, these raids predate the battle and are not directly the Camps battle. Borderline proposals remain marked **[BORDERLINE]** above.

- **`battle-on-the-green-fork CAUSES battle-of-the-whispering-wood`** — Rejected per the ENABLES-vs-CAUSES contract. Robb chose to spring the trap; Bolton's engagement with Tywin was a precondition but not a forced consequence. Using ENABLES per shared instructions.

- **`siege-of-riverrun ENABLES battle-of-the-whispering-wood`** — Backwards direction; the siege is what Robb was relieving, not what enabled the Wood. Dropped.

- **`execution-of-eddard-stark MOTIVATES robb-stark` (at the Whispering Wood)** — This dyad ALREADY EXISTS (S113). Not re-proposing.

- **`roose-bolton COMMANDS_IN battle-on-the-green-fork`** — This is the Green Fork battle, already 29 edges, and likely saturated. Possibly missing but outside my lane (Roose wasn't at the Wood); noting it for any lens with the Green Fork as focus. Not proposing here.

- **Any PASS 2/3 material** — Oxcross, the Fords, Duskendale: none reached.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|-------------|------|
| food | AGOT | agot-catelyn-08:17 | Lord Wyman Manderly noted as "grown too stout to sit a horse" / "too many eels" — vivid description linking gluttony to a great lord's military limitation |
| food | AGOT | agot-catelyn-08:25 | Supply wagons described as `"wagons heavy-laden with hardbread and salt beef"` — march rations for the host |
| food | AGOT | agot-catelyn-09:137 | Lord Walder Frey surrounded by family in his great hall — hospitality-meeting context; Catelyn seated with him to negotiate |
| food | AGOT | agot-catelyn-09:195 | Walder Frey: `"Sweet words I get from my wife"` — hospitality language, not food, but relevant to Frey-hall scene |
| food | AGOT | agot-catelyn-11:55 | Hoster Tully dying: `"Maester Vyman makes me dreamwine, milk of the poppy … I sleep a lot"` — medicinal foodstuff/drink for the dying lord |
| food | AGOT | agot-catelyn-11:117 | Theon Greyjoy in the Great Hall `"enjoying a horn of ale"` — victory drink; immediate post-battle scene |
| quote (node) | AGOT | agot-catelyn-10:79 | `"And Grey Wind threw back his head and howled."` — the signal-howl opening the battle; load-bearing for Grey Wind's node Quotes |
| quote (node) | AGOT | agot-catelyn-10:85 | `"'Winterfell!' she heard Robb shout as the arrows sighed again."` — Robb's battle cry; load-bearing for robb-stark node Quotes |
| quote (node) | AGOT | agot-catelyn-10:93 | `"she heard his direwolf, snarling and growling, heard the snap of those long teeth, the tearing of flesh, shrieks of fear and pain from man and horse alike"` — Grey Wind at the kill; vivid description |
| quote (node) | AGOT | agot-catelyn-10:89 | `"a thousand willowisps were coming down the ridge, wreathed in silver flame"` — the moonlit lance-tips of the Greatjon's riders charging; visual of the battle |
| quote (node) | AGOT | agot-catelyn-11:61 | `"Riverrun is free again, Father."` — Catelyn's declaration to Hoster; load-bearing quote for the relief of Riverrun |
| quote (node) | AGOT | agot-catelyn-11:63 | `"the torches came in a wave, I could hear the cries floating across the river … sweet cries … when that siege tower went up, gods … would have died then, and glad"` — Hoster watching the Camps battle from the battlements |
| quote (node) | AGOT | agot-catelyn-11:209 | `"There sits the only king I mean to bow my knee to, m'lords," he thundered. "The King in the North!"` — Greatjon's proclamation; load-bearing for robb-proclaimed-king-in-the-north |
| quote (node) | AGOT | agot-catelyn-11:215 | `"The King of Winter!"` — Maege Mormont's variant; `"ringing from the timbers of her father's hall"` — physical setting of the proclamation |
| description | AGOT | agot-catelyn-10:11 | `"Moonlight winked on the tumbling waters of the stream below as it wound its rocky way along the floor of the valley. Beneath the trees, warhorses whickered softly and pawed at the moist, leafy ground"` — evocative pre-battle setting of the wood |
| description | AGOT | agot-catelyn-10:65 | `"The moonlight had silvered his armor and the gold of his hair, and turned his crimson cloak to black. He was not wearing a helm."` — Jaime riding into the trap; vivid physical description |
| description | AGOT | agot-catelyn-10:73 | `"a thick carpet of dead leaves underfoot, densely wooded ridges sloping gently down to the streambed, the underbrush thinning as the ground fell away"` — the valley floor geography |
| description | AGOT | agot-catelyn-10:97 | `"The wolf's head on his shield was slashed half to pieces, raw wood showing where deep gouges had been hacked in the oak"` — Robb's battered shield post-battle; physical aftermath |
| description | AGOT | agot-catelyn-11:19 | `"His bright yellow armor was inlaid with jet in elaborate vine-and-leaf patterns, and a cloak sewn from raven feathers draped his thin shoulders."` — Tytos Blackwood's distinctive appearance |
| description | AGOT | agot-catelyn-11:47 | Hoster Tully's physical decline: `"Now he seemed shrunken, the muscle and meat melted off his bones. Even his face sagged."` — stark before/after description |
| foreshadowing | AGOT | agot-catelyn-09:241 | `"Also, if your sister Arya is returned to us safely, it is agreed that she will marry Lord Walder's youngest son, Elmar"` / `"And you are to wed one of his daughters"` — the Frey marriage pact; load-bearing for the Red Wedding upstream |
| hospitality | AGOT | agot-catelyn-09:137 | Catelyn received in Lord Walder's great hall — formal hospitality scene with negotiation under roof; twenty sons + grandchildren present |
| hospitality | AGOT | agot-catelyn-11:11 | Robb and company entering Riverrun by boat — `"soldiers and servants shouted down her name, and Robb's, and 'Winterfell!'"` — victory welcome/return scene |
