# Lens B — Whodunit / Hidden Agency / SUSPECTED_OF — A2.5 WO5K-battles proposal (S163, PASS 1)

Lens B focus: hidden agency, deliberate choices, and honest whodunit. Chapters read: agot-catelyn-08,
agot-catelyn-09, agot-catelyn-10, agot-catelyn-11 (full text, line numbers, verbatim quotes throughout).

---

## CAPTURES-Edge Audit (HIGH PRIORITY — flagged in baseline.md)

The two suspicious existing edges, adjudicated against the chapter text:

| Edge | What the text says | Verbatim quote + chapter:line | Verdict |
|------|--------------------|-------------------------------|---------|
| `roose-bolton CAPTURES jaime-lannister` (tier-1) | Roose Bolton commands the foot host sent down the kingsroad to confront Tywin on the Green Fork (cat-08: "Roose Bolton… the eastern host will be all that stands between Lord Tywin and Winterfell"). He is explicitly NOT with Robb's cavalry in the Whispering Wood. The capture happens in the Wood, described in cat-10. Roose is entirely absent from cat-10 and cat-11's Whispering Wood narrative. | cat-08:179 "Roose Bolton… That man scares me." — establishes Bolton leads the Green Fork host; cat-09:257 "The larger part of the northern host… remained upon the east bank under the command of Roose Bolton." — confirms he went east, not south with Robb. | **WRONG — BUG DROP.** Roose was at the Green Fork, not the Whispering Wood. This edge is a misattribution. The correct CAPTURES edge should point to `robb-stark` (or the event hub — see below). Recommend: drop `roose-bolton CAPTURES jaime-lannister`; mint `robb-stark CAPTURES jaime-lannister` if a direct dyad is wanted (but the event hub `battle-of-the-whispering-wood` with `jaime VICTIM_IN` + `robb AGENT_IN/COMMANDS_IN` is the cleaner fix). |
| `catelyn-stark CAPTURES jaime-lannister` (tier-1) | Catelyn is not in the Whispering Wood during the battle. She waits on the ridge with 30 guards (cat-10:15). The battle occurs below her. She does not participate in the capture. After the battle, Robb returns with Jaime already a prisoner — "A mob of men followed him up the slope… Between them they dragged Ser Jaime Lannister." She then *orders* his disposition: "Take him away and put him in irons." Robb commands it. | cat-10:101 "A mob of men followed him up the slope, dirty and dented and grinning, with Theon and the Greatjon at their head. Between them they dragged Ser Jaime Lannister." cat-10:117 "Take him away and put him in irons," Catelyn said. | **WRONG — BUG DROP.** Catelyn did not capture Jaime; she received him already captured and issued a disposal order. The order is editorial/custodial, not the act of capture. This edge is a category error — conflating command-authority over a prisoner with the act of taking him. Recommend: drop `catelyn-stark CAPTURES jaime-lannister`. If a Catelyn↔Jaime dyad is wanted for this moment, `catelyn-stark IMPRISONS jaime-lannister` is defensible (she orders his chaining), but even that is thin because Robb immediately echoes the command and has ultimate authority. The cleaner encoding is: `jaime-lannister PRISONER_OF robb-stark` (if not already present) and the event-hub role `jaime VICTIM_IN battle-of-the-whispering-wood`. |

**Summary verdict:** Both CAPTURES edges are wrong. Roose was at the Green Fork. Catelyn received the prisoner and issued a disposal order. Neither constitutes a capture. The actual captors are Robb's host — operationally Robb as commander, with the Greatjon and Theon among those physically dragging Jaime up the slope.

---

## Proposed NEW nodes

### `battle-of-the-whispering-wood`
- **slug:** `battle-of-the-whispering-wood`
- **type:** `event.battle`
- **name:** Battle of the Whispering Wood
- **body:** A night ambush in the wooded valley of the Whispering Wood in the Riverlands, in which Robb Stark's cavalry of ~6,000 trapped and destroyed three-quarters of Jaime Lannister's horse. Robb split the valley shut at both ends (Maege Mormont's warhorn signaling from the east, Greatjon Umber from the west, Karstarks sealing the north). Bowmen hidden in trees opened the slaughter. Jaime, unhelmeted and restless, rode into the trap and was taken captive; three of Lord Karstark's sons and Daryn Hornwood died trying to stop Jaime from fighting through to Robb. The victory enabled the Battle of the Camps by leaving Jaime's three siege-camp hosts leaderless and unaware.
- **anchor quote:** `agot-catelyn-10:101` — "A mob of men followed him up the slope, dirty and dented and grinning, with Theon and the Greatjon at their head. Between them they dragged Ser Jaime Lannister."
- **note on quarantined twin:** baseline.md flags a wiki node in `graph/nodes/_conflicts/battle-of-the-whispering-wood.node.md`. The live node should be minted in `graph/nodes/events/` independently.

---

## Proposed NEW edges

(Deduped against baseline.md live web. Existing roles on `battle-of-the-camps`: robb/jaime/brynden COMMANDS_IN, jon-umber/grey-wind/forley-prester/tytos-blackwood FIGHTS_IN, edmure/andros-brax VICTIM_IN, hoster-tully WITNESS_IN — NOT re-proposed. Existing 2 causal edges in cluster: execution-of-eddard-stark CAUSES robb-proclaimed-king-in-the-north + execution MOTIVATES robb-stark — NOT re-proposed.)

### Causal spine (THE HIGH-VALUE GAP)

| source_slug | EDGE_TYPE | target_slug | Tier | qualifier | verbatim quote + chapter:line | rationale |
|-------------|-----------|-------------|------|-----------|-------------------------------|-----------|
| `battle-on-the-green-fork` | ENABLES | `battle-of-the-whispering-wood` | Tier-2 | — | cat-10:31 "Jaime does not know… No bird has reached him, my archers have seen to that." (Brynden's screening made the surprise possible because Tywin's army was drawn north by the Green Fork feint) | The Green Fork feint drew Tywin's host north, leaving Jaime's cavalry unsupported and unwarned. Robb then chose to spring the night trap — ENABLES (not CAUSES) per contract. |
| `battle-of-the-whispering-wood` | ENABLES | `battle-of-the-camps` | Tier-2 | — | cat-11:117 "Theon Greyjoy was seated on a bench… 'The Lannisters must have thought the Others themselves were on them when that wolf of Robb's got in among them.'" (and cat-10:131 "No one can fault Lannister on his courage… When he saw that he was lost…") | Jaime's capture left three Lannister siege-camp hosts leaderless and unaware; the Battle of the Camps followed directly. The text in cat-11 confirms the Camps as the next beat after the Wood. ENABLES per contract. |
| `battle-of-the-camps` | ENABLES | `robb-proclaimed-king-in-the-north` | Tier-2 | — | cat-11:143 "Word of the victory at Riverrun had spread to the fugitive lords of the Trident, drawing them back." | The twin victories + relief of Riverrun assembled the lords who proclaimed Robb king. The proclamation was their free choice — ENABLES per contract. |
| `siege-of-riverrun` | ENABLES | `battle-of-the-camps` | Tier-3 | — | cat-10:35 "Twelve thousand foot, scattered around the castle in three separate camps, with the rivers between… Two or three thousand horse." | The siege's three-camp dispersal geometry (forced by the rivers) made the camps vulnerable to Robb's sequential assault. The text is explicit that the rivers forced the dispersal — "There is no other way to besiege Riverrun, yet still, that will be their undoing." A precondition, not a cause. **[BORDERLINE]** — the siege didn't produce the Camps, it created the geometry that made the Camps possible; worth flagging for gate review. |

### Whispering Wood event-hub roles (NEW node `battle-of-the-whispering-wood`)

| source_slug | EDGE_TYPE | target_slug | Tier | qualifier | verbatim quote + chapter:line | rationale |
|-------------|-----------|-------------|------|-----------|-------------------------------|-----------|
| `robb-stark` | COMMANDS_IN | `battle-of-the-whispering-wood` | Tier-1 | — | cat-10:71 "Raid him here… When he comes after you, we will be waiting—here." (Robb designed and commanded the ambush) | Robb devised the trap (cat-10:71), rode into the valley leading his men (cat-10:85 "Winterfell!"), and returned as victor. COMMANDS_IN is correct. |
| `robb-stark` | AGENT_IN | `battle-of-the-whispering-wood` | Tier-1 | — | cat-10:85 "Winterfell!" she heard Robb shout as the arrows sighed again. He moved away from her at a trot, leading his men downhill." | Robb physically fought in the battle. Dual role: COMMANDS_IN + AGENT_IN. |
| `jaime-lannister` | VICTIM_IN | `battle-of-the-whispering-wood` | Tier-1 | — | cat-10:101 "Between them they dragged Ser Jaime Lannister. They threw him down in front of her horse." | Jaime was captured at the battle — the definitive victim/prisoner outcome. |
| `grey-wind` | AGENT_IN | `battle-of-the-whispering-wood` | Tier-1 | — | cat-10:93 "she heard his direwolf, snarling and growling, heard the snap of those long teeth, the tearing of flesh, shrieks of fear and pain from man and horse alike." | Grey Wind fought in the battle and directly caused casualties. Also applicable: FIGHTS_IN. |
| `grey-wind` | FIGHTS_IN | `battle-of-the-whispering-wood` | Tier-1 | — | cat-10:93 (same as above) | Dual role — FIGHTS_IN is the combatant tag, AGENT_IN acknowledges the decisive role. |
| `brynden-tully` | COMMANDS_IN | `battle-of-the-whispering-wood` | Tier-1 | — | cat-10:31 "Robb had given the Blackfish three hundred picked men, and sent them ahead to screen his march… I'll stake my life on that. No bird has reached him, my archers have seen to that." | The Blackfish screened the march, blinded Jaime's outriders, and engineered the surprise. His strategic contribution was decisive. |
| `jon-umber` | FIGHTS_IN | `battle-of-the-whispering-wood` | Tier-1 | — | cat-10:83 "HAAroooooooooooooooooooooooo came the answer from the far ridge as the Greatjon winded his own horn." | Greatjon commanded the western ridge force and fought. Also mentioned in cat-11:145 losing two sons at the Whispering Wood (Karstark, not Umber — see Karstark below). |
| `rickard-karstark` | FIGHTS_IN | `battle-of-the-whispering-wood` | Tier-1 | — | cat-10:83 "Lord Karstark's warhorns added their own deep, mournful voices to the dark chorus." | Karstark sealed the northern end of the valley; his two sons Torrhen and Eddard died there (cat-11:145). |
| `maege-mormont` | AGENT_IN | `battle-of-the-whispering-wood` | Tier-1 | — | cat-10:77 "the call of Maege Mormont's warhorn, a long low blast that rolled down the valley from the east, to tell them that the last of Jaime's riders had entered the trap." | Mormont held the eastern signal-horn position — the trigger that launched the ambush. Her warhorn blast = the battle's opening action. |
| `maege-mormont` | FIGHTS_IN | `battle-of-the-whispering-wood` | Tier-1 | — | cat-10:77 (same) | Dual role — she commanded the eastern force. |
| `galbart-glover` | FIGHTS_IN | `battle-of-the-whispering-wood` | Tier-2 | — | cat-10:37 "The Kingslayer has us three to one," said Galbart Glover." (present at the pre-battle council; implied combatant) | Glover was part of the cavalry that crossed the Twins and fought at the Wood. Text does not give him a named role in the battle itself, only in the build-up (cat-10:37) and the after-action (cat-10:127). **[BORDERLINE]** — present, but no battle-action line. |
| `jason-mallister` | FIGHTS_IN | `battle-of-the-whispering-wood` | Tier-2 | — | cat-10:45 "Lord Jason Mallister had brought his power out from Seagard to join them as they swept around the headwaters of the Blue Fork and galloped south" | Mallister joined the cavalry force that fought at the Wood. Not given a named act in the battle itself. **[BORDERLINE]** |
| `battle-of-the-whispering-wood` | LOCATED_AT | `whispering-wood` | Tier-1 | — | cat-10:11 "The woods were full of whispers." (opening line of the chapter; the place node `whispering-wood` already exists per baseline) | Standard location anchor. |

### Whispering Wood → battle-of-the-camps seam (supporting the causal spine)

| source_slug | EDGE_TYPE | target_slug | Tier | qualifier | verbatim quote + chapter:line | rationale |
|-------------|-----------|-------------|------|-----------|-------------------------------|-----------|
| `jaime-lannister` | VICTIM_IN | `battle-of-the-camps` | Tier-2 | — | cat-11:61 "And we've brought you Jaime Lannister, in irons. Riverrun is free again, Father." | Jaime's capture (Wood) caused the Camps to be fought without a commander — he is both Wood victim and the Camps' causal absence. If already present on the Camps node, skip. **[BORDERLINE — dedup check needed]** |

### Robb's plan (cat-08) and Frey crossing (cat-09) — decision edges

| source_slug | EDGE_TYPE | target_slug | Tier | qualifier | verbatim quote + chapter:line | rationale |
|-------------|-----------|-------------|------|-----------|-------------------------------|-----------|
| `robb-stark` | MOTIVATES | `battle-of-the-whispering-wood` | Tier-2 | — | cat-08:151 "once we're below the Neck, I'd split our host in two. The foot can continue down the kingsroad, while our horsemen cross the Green Fork at the Twins." | Robb's decision at Moat Cailin to split the host — sending horse west to relieve Riverrun — is the originating choice that enables the Whispering Wood. MOTIVATES→character is wrong (target must be a character); but MOTIVATES can't point to an event. The correct encoding is the causal spine: Robb's choice is the *agent* in COMMANDS_IN on the battle. DROPPING this row — no valid edge type for "choice → event" that isn't CAUSES/ENABLES/TRIGGERS. The choice IS encoded via Robb COMMANDS_IN on the battle node. |
| `walder-frey` | CONTRACTED_WITH | `robb-stark` | Tier-1 | — | cat-09:241 "you are to wed one of his daughters, once the fighting is done" | The Frey betrothal contract as the price of crossing. **DEDUP WARNING:** baseline.md notes the "B1 Red-Wedding-upstream spine" and "Frey-betrothal foreshadow already lives on king-in-the-north." Skip if already present. Noting here for completeness; do NOT re-mint if present. **[DROPPING — likely already built; baseline says it's there]** |

---

## SUSPECTED_OF edges

**None proposed.** The Whispering Wood and Battle of the Camps are clean military victories. Robb designed and executed the ambush. Jaime rode into it without a helmet (restless, impatient — as Brynden predicted). There is no planted-but-unproven agency in these chapters that warrants a SUSPECTED_OF edge. The deliberate-Bolton-sacrifice question is PASS 3 (Duskendale) as instructed; it does not appear in these chapters.

One moment that briefly reads as possible whodunit: did Walder Frey deliberately delay to let Edmure lose before granting the crossing? ("Late again," cat-09:19.) But the text frames this as characteristic tardiness / calculated neutrality, not as covert Lannister agency. The Frey-betrothal foreshadowing is already built on king-in-the-north per baseline. No SUSPECTED_OF warranted.

---

## Dropped / considered-but-rejected

| item | reason |
|------|--------|
| `roose-bolton COMMANDS_IN battle-of-the-whispering-wood` | Bolton commanded the Green Fork foot host (cat-08:179, cat-09:257). He was not present at the Whispering Wood. Wrong battle. |
| `catelyn-stark COMMANDS_IN battle-of-the-whispering-wood` | Catelyn waited on the ridge with her guard, explicitly excluded from the battle. cat-10:15: "She had thirty men around her, charged to keep her unharmed." Not a commander. |
| `catelyn-stark WITNESS_IN battle-of-the-whispering-wood` | LENS-SHARED.md is explicit: "Catelyn waits OUTSIDE the wood and only HEARS it, so she is NOT a witness to the battle itself." She sees Jaime only for an instant before the battle and does not see the fighting. Excluded by the shared rules. |
| `theon-greyjoy FIGHTS_IN battle-of-the-whispering-wood` | Theon is mentioned in Robb's battle guard in cat-10:53, and in cat-10:101 ("with Theon and the Greatjon at their head" dragging Jaime up). He fought, but he's an attendant-figure. **[BORDERLINE — could propose]** Chose not to add to avoid over-proposing thin roles; synthesis can add if the Theon↔Wood connection is wanted. |
| `daryn-hornwood VICTIM_IN battle-of-the-whispering-wood` | Daryn Hornwood died trying to stop Jaime's fighting breakthrough. cat-10:129 "Daryn Hornwood as well." Legitimate candidate but his node may not exist in the graph. Flagging for synthesis — if `daryn-hornwood` node exists, add VICTIM_IN. |
| `torrhen-karstark VICTIM_IN battle-of-the-whispering-wood` | Died in the battle (cat-10:129). Same node-existence caveat as Daryn Hornwood. Flag for synthesis. |
| `eddard-karstark VICTIM_IN battle-of-the-whispering-wood` | Died in the battle (cat-10:129, "Eddard"). Same caveat. |
| Frey betrothal edge (`walder-frey CONTRACTED_WITH robb-stark`) | Baseline says the B1 Red-Wedding-upstream spine and Frey-betrothal foreshadow are already built on `king-in-the-north`. Dropped to avoid duplication; dedup kills it. |
| `robb-stark BETROTHED_TO frey-daughter` | Same — already in the built web. |
| Robb's strategic plan as a graph node | Robb's split-host decision at Moat Cailin is a choice, not an event. It is encoded through COMMANDS_IN on the battle node. No event node warranted. |
| `catelyn-stark MOTIVATES robb-stark` (toward the battle) | Catelyn coaches Robb repeatedly in cat-08 ("Be certain, or go home") and cat-09 ("A child sees an obstacle"). This is load-bearing characterization but the dyad is almost certainly saturated (catelyn 119 core-out edges). Dropped as a dyad-web item likely already present. |
| Green Fork internals | Baseline: "Do not rebuild it." Not proposed. |
| Oxcross / Westerlands (PASS 2 items) | Out of scope. |
| Duskendale / Fords / Bolton deliberate retreat (PASS 3) | Out of scope. Note: if the Bolton-sacrifice question surfaces later, the Green Fork battle already has 29 edges; the PASS 3 dip should look for a `roose-bolton SUSPECTED_OF deliberate-defeat-at-green-fork` type reading. Noted for PASS 3. |
| `cleos-frey VICTIM_IN battle-of-the-whispering-wood` | Theon mentions "three Lannisters besides Jaime, Lord Tywin's own nephews, two of his sister's sons and one of his dead brother's" (cat-10:137). Cleos Frey is among the Lannister captives taken, but the text is in cat-10 (after the Wood / as part of the Camps aftermath accounting). Node may exist; flag for synthesis if `cleos-frey` is present. |
| Jon Arryn fostering at Dragonstone (cat-09:211) | Lord Frey reveals Jon Arryn planned to foster his son with Stannis, not Tywin — a plot-relevant reveal (contradicts Lysa's claim to Catelyn). This is a PASS-3 or theory-layer item touching the murder of Jon Arryn chain. PASS-1 scope only; flagged for PASS 3. |

---

## Harvest

| kind | book | chapter:line | note |
|------|------|--------------|------|
| food | AGOT | agot-catelyn-08:25 | "wagons heavy-laden with hardbread and salt beef" — the march provisioning of Robb's host at Moat Cailin |
| food | AGOT | agot-catelyn-08:63 | "There was ale and cheese on the table" — Catelyn and Robb's private parley at Moat Cailin |
| food | AGOT | agot-catelyn-09:137 | "surrounded by twenty living sons… she understood just what he had meant" — Walder Frey's feast-hall atmosphere; the great hall of the east castle, the abundance of Frey kin |
| hospitality / food | AGOT | agot-catelyn-09:155 | "he beckoned Catelyn forward and planted a papery dry kiss on her hand" — formal hospitality ritual at the Twins |
| food | AGOT | agot-catelyn-09:191 | Lord Walder's aside about Lord Tywin eating beans and breaking wind — comic food reference in a tense negotiation |
| food | AGOT | agot-catelyn-09:195 | "Sweet words I get from my wife… I'll wager she gives me a son by this time next year" — indirect food/hospitality (the wife's "honey" metaphor) |
| quote (load-bearing) | AGOT | agot-catelyn-10:11 | "The woods were full of whispers." — opening line; atmosphere quote for battle-of-the-whispering-wood node prose |
| quote (load-bearing) | AGOT | agot-catelyn-10:25 | "'The Kingslayer is restless, and quick to anger,' her uncle Brynden had told Robb. And he had wagered their lives and their best hope of victory on the truth of what he said." — the Blackfish's gambit in one sentence |
| quote (load-bearing) | AGOT | agot-catelyn-10:43 | "Patience." (Ser Brynden's one-word answer to "what does Ser Jaime lack?") — perfect quote for Brynden node or battle node |
| quote (load-bearing) | AGOT | agot-catelyn-10:73 | "Here was a hush in the night, moonlight and shadows, a thick carpet of dead leaves underfoot, densely wooded ridges sloping gently down to the streambed…" — vivid physical description of the battle ground |
| quote (load-bearing) | AGOT | agot-catelyn-10:77 | "the call of Maege Mormont's warhorn, a long low blast that rolled down the valley from the east, to tell them that the last of Jaime's riders had entered the trap." — the battle's trigger moment |
| quote (load-bearing) | AGOT | agot-catelyn-10:79 | "And Grey Wind threw back his head and howled." — the direwolf's battle-cry, load-bearing for grey-wind node |
| physical description | AGOT | agot-catelyn-10:65 | "the moonlight had silvered his armor and the gold of his hair, and turned his crimson cloak to black. He was not wearing a helm." — Jaime's moonlit appearance as he rides into the trap |
| physical description | AGOT | agot-catelyn-10:89 | "an instant, the smallest part of a heartbeat, when all Catelyn saw was the moonlight on the points of their lances, as if a thousand willowisps were coming down the ridge, wreathed in silver flame." — the Greatjon's charge, vivid description |
| quote (load-bearing) | AGOT | agot-catelyn-10:101 | "Between them they dragged Ser Jaime Lannister. They threw him down in front of her horse." — the capture; also "The Kingslayer," Hal announced, unnecessarily." |
| quote (load-bearing) | AGOT | agot-catelyn-10:113 | "He's more use alive than dead. And my lord father never condoned the murder of prisoners after a battle." — Robb's character; Ned's value on prisoner conduct |
| quote (load-bearing) | AGOT | agot-catelyn-11:61 | "Riverrun is free again, Father." — the relief declaration; load-bearing for battle-of-the-camps node |
| quote (load-bearing) | AGOT | agot-catelyn-11:63 | "the torches came in a wave, I could hear the cries floating across the river… sweet cries… when that siege tower went up, gods… would have died then, and glad" — Hoster Tully watching the Battle of the Camps from the battlements |
| food / medicine | AGOT | agot-catelyn-11:55 | "Maester Vyman makes me dreamwine, milk of the poppy… I sleep a lot" — Hoster Tully's palliative care; dreamwine + milk of the poppy named together |
| food | AGOT | agot-catelyn-11:117 | "Theon Greyjoy was seated on a bench in Riverrun's Great Hall, enjoying a horn of ale" — post-battle celebratory drinking at Riverrun |
| quote (load-bearing / King in the North) | AGOT | agot-catelyn-11:209 | "There sits the only king I mean to bow my knee to, m'lords… The King in the North!" — Greatjon's proclamation; first utterance of the refrain |
| quote (load-bearing / King in the North) | AGOT | agot-catelyn-11:217 | "THE KING IN THE NORTH!" — the hall's closing refrain; load-bearing for robb-proclaimed-king-in-the-north node |
| plot-intelligence reveal | AGOT | agot-catelyn-09:211 | Lord Walder reveals Jon Arryn planned to foster his son Robert with Stannis (not Tywin/Cersei) — contradicts Lysa's stated motive for fleeing to the Eyrie; potential Jon Arryn murder chain thread. Flag for PASS-3 / theory layer. |
| physical description | AGOT | agot-catelyn-11:19 | Lord Tytos Blackwood's appearance: "bright yellow armor… inlaid with jet in elaborate vine-and-leaf patterns… a cloak sewn from raven feathers" — vivid for Blackwood node |
| physical description | AGOT | agot-catelyn-08:17 | Lord Wyman Manderly: "near sixty years, he had grown too stout to sit a horse… fingers were fat as sausages" — physical description for Manderly node |
