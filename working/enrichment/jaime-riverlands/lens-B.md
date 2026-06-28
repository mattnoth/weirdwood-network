# Lens B — WHODUNIT / HIDDEN-AGENCY + SUSPECTED_OF — A2.6 Jaime / Riverlands proposal (S159)

## Proposed NEW nodes

### `edmure-yields-riverrun`
- **slug:** edmure-yields-riverrun
- **type:** event.incident
- **summary:** Edmure Tully, coerced by Jaime's trebuchet threat, surrenders Riverrun to the Lannisters by hauling down the Stark direwolf banner. He waits most of a day before yielding, deliberately allowing time for the Blackfish to escape. The castle passes to House Frey/Lannister without a storming.
- **anchor quote:** "a black fish in a black river floating quietly downstream" `affc-jaime-07:39` (Jaime's reconstruction of how the escape happened while "Edmure had waited most of the day before hauling down the direwolf of Stark in token of surrender")
- **note on anchor:** The surrender itself is not a single clean quote-line; the most direct reference is at `affc-jaime-07:39` where Jaime reflects on the timing Edmure allowed. The surrender is a confirmed narrative fact.

### `blackfish-escapes-riverrun`
- **slug:** blackfish-escapes-riverrun
- **type:** event.incident
- **summary:** Ser Brynden Tully refuses to yield or take the black. During the night of the surrender, Edmure raises the Water Gate portcullis just three feet under water, leaving a gap invisible from outside. Brynden swims out under the boom in the dark river rather than be taken prisoner.
- **anchor quote:** "We raised the portcullis on the Water Gate. Not all the way, just three feet or so. Enough to leave a gap under the water, though the gate still appeared to be closed. My uncle is a strong swimmer." `affc-jaime-07:37`

### `jaime-burns-cerseis-letter`
- **slug:** jaime-burns-cerseis-letter
- **type:** event.incident
- **summary:** Cersei's plea-for-help letter (written through Qyburn, urging Jaime to come at once) reaches Jaime at Riverrun. He reads it in the window seat, then hands it to Peck with the single order "Put this in the fire." This is his definitive refusal to ride to Cersei's aid — the marquee Jaime↔Cersei rupture.
- **anchor quote (Cersei's letter):** "Come at once, she said. Help me. Save me. I need you now as I have never needed you before. I love you. I love you. I love you. Come at once." `affc-jaime-07:291`
- **anchor quote (refusal):** "No," he said. "Put this in the fire." `affc-jaime-07:295`

---

## Proposed NEW edges

| # | source_slug | EDGE_TYPE | target_slug | Tier | qualifier / note | verbatim quote + chapter:line | rationale |
|---|------------|-----------|-------------|------|-------------------|-------------------------------|-----------|
| 1 | jaime-lannister | MANIPULATES | edmure-tully | Tier-1 | qualifier: `via_threat` | "You'll want your child, I expect. I'll send him to you when he's born. With a trebuchet." `affc-jaime-06:325` | The trebuchet threat is the direct coercive mechanism that produces Edmure's surrender. Jaime escalates from military ultimatum to a personal threat against the unborn child — this is the specific act that breaks Edmure's resistance. `MANIPULATES via_threat` is the correct type. |
| 2 | jaime-lannister | DECEIVES | edmure-tully | Tier-2 | — | "Well enough to sit here till the end of days if need be, whilst you starve inside your walls." `affc-jaime-06:93` | Jaime explicitly lies about provisions at the parley with the Blackfish (same lie he would have repeated to Edmure). The Blackfish sees through it ("The end of your days, perhaps" :95). This is deliberate misrepresentation of military strength to extract a surrender. Tier-2 because the primary lie is at the Blackfish parley but the deceptive intent carries into the Edmure negotiation. **[BORDERLINE]** — the Blackfish, not Edmure, is the direct target of this lie. Include as Tier-2 if the gate considers it meaningful deception of Edmure downstream. |
| 3 | jaime-lannister | AGENT_IN | edmure-yields-riverrun | Tier-1 | — | "You've seen our numbers, Edmure. You've seen the ladders, the towers, the trebuchets, the rams." `affc-jaime-06:325` | Jaime is the direct agent who coerces the surrender in the bath-tent parley. |
| 4 | edmure-tully | VICTIM_IN | edmure-yields-riverrun | Tier-1 | — | "Edmure had waited most of the day before hauling down the direwolf of Stark in token of surrender." `affc-jaime-07:39` | Edmure is the party coerced into surrendering his ancestral seat. |
| 5 | edmure-yields-riverrun | SUB_BEAT_OF | siege-of-riverrun | Tier-1 | — | "In the confusion of the castle changing hands, it had been the next morning before Jaime had been informed that the Blackfish was not amongst the prisoners." `affc-jaime-07:39` | The surrender is a moment within the siege, resolving it. |
| 6 | edmure-yields-riverrun | CAUSES | blackfish-escapes-riverrun | Tier-1 | — | "We raised the portcullis on the Water Gate. Not all the way, just three feet or so." `affc-jaime-07:37` | Edmure raises the submerged gate gap as part of his surrender terms — he yields the castle, not his uncle. The surrender event directly enables/creates the escape mechanism. CAUSES is appropriate: the surrender is what Edmure negotiates to provide the cover and timing for the escape. |
| 7 | edmure-tully | AGENT_IN | blackfish-escapes-riverrun | Tier-1 | — | "Fish swim. Even black ones." `affc-jaime-07:29` | Edmure orchestrates the escape mechanism (the submerged portcullis gap). He is the agent, not merely a bystander. |
| 8 | brynden-tully | AGENT_IN | blackfish-escapes-riverrun | Tier-1 | — | "My uncle is a strong swimmer. After dark, he pulled himself beneath the spikes." `affc-jaime-07:37` | Brynden is the one who physically executes the escape. |
| 9 | blackfish-escapes-riverrun | SUB_BEAT_OF | siege-of-riverrun | Tier-1 | — | "the Blackfish was not amongst the prisoners" `affc-jaime-07:39` | The escape is a beat within the siege's resolution. |
| 10 | vance-karyl | SUSPECTED_OF | blackfish-escapes-riverrun | Tier-2 | — | "Vance and Piper and their ilk were more like to help the Blackfish escape than clap him into fetters." `affc-jaime-07:45` | Jaime explicitly suspects the riverlords (naming Vance and Piper) of abetting the escape rather than pursuing the Blackfish. This is unproven in-text — Jaime decides NOT to enlist them in the search. Tier-2 SUSPECTED_OF is the honest model; the text does not prove it. |
| 11 | lord-piper | SUSPECTED_OF | blackfish-escapes-riverrun | Tier-2 | — | "Vance and Piper and their ilk were more like to help the Blackfish escape than clap him into fetters." `affc-jaime-07:45` | Same passage; Piper is named alongside Vance. Jaime's suspicion is explicit; proof is absent. Tier-2. |
| 12 | jaime-lannister | AGENT_IN | jaime-burns-cerseis-letter | Tier-1 | — | "No," he said. "Put this in the fire." `affc-jaime-07:295` | Jaime is the one who orders/executes the letter's destruction. |
| 13 | cersei-lannister | AGENT_IN | jaime-burns-cerseis-letter | Tier-2 | — | "Come at once, she said. Help me. Save me. I need you now as I have never needed you before." `affc-jaime-07:291` | Cersei authors the letter (through Qyburn as conduit — "Qyburn's words were terse and to the point, Cersei's fevered and fervent"). She initiates the plea that Jaime burns. Tier-2 because Qyburn is the conduit and Cersei's direct authorship is implied rather than explicitly stated. **[BORDERLINE]** |
| 14 | jaime-burns-cerseis-letter | MOTIVATES | jaime-lannister | Tier-1 | — | "A snowflake landed on the letter. As it melted, the ink began to blur." `affc-jaime-07:294` | The act of burning, not answering, is Jaime's deliberate choice — it motivates his continuing refusal to return to Cersei's side. MOTIVATES→character (him) is the correct edge; over-asserting a CAUSES to an event would collapse his free choice. |
| 15 | jaime-lannister | DECEIVES | genna-lannister | Tier-1 | — | "Beside a stream," he lied. "When this war is done, I will find the place and send him home." `affc-jaime-05:213` | Jaime lies twice to Aunt Genna and Emmon about Ser Cleos's death and burial — first about the manner of death ("outlaws"), then about where he was buried. The lie is explicit in the narration ("he lied"). |
| 16 | jaime-lannister | DECEIVES | emmon-frey | Tier-1 | — | "We were set upon by outlaws. Ser Cleos scattered them, but it cost his life." The lie came easy; he could see that it pleased them. `affc-jaime-05:207` | Jaime lies to both Genna and Emmon in the same conversation. Separate edge for Emmon as recipient. Could collapse to one DECEIVES edge with both as targets, but the schema takes one target per edge. Separate rows. |
| 17 | jaime-lannister | DECEIVES | brynden-tully | Tier-1 | — | "Well enough to sit here till the end of days if need be, whilst you starve inside your walls." He told the lie as boldly as he could and hoped his face did not betray him. `affc-jaime-06:93` | Jaime explicitly misrepresents provisioning strength to the Blackfish at the parley. The text marks it as a lie ("He told the lie as boldly as he could"). |
| 18 | cersei-lannister | MANIPULATES | jaime-lannister | Tier-2 | qualifier: `via_threat` | "Very well. If it is battlefields you want, battlefields I shall give you." `affc-jaime-01:199` | In the Great Sept scene (affc-jaime-01), Cersei attempts to manipulate Jaime into becoming Hand — first through emotional appeal and sexual pressure, then when refused, switches to a veiled threat ("battlefields I shall give you"). Tier-2 because Jaime is not deceived — he refuses — and the manipulation fails. **[BORDERLINE]** — the qualifier `via_threat` may be too strong for "battlefields I shall give you" which is more of a pique-driven departure than a structured threat. Could downgrade to `via_flattery` / `unknown` for the preceding pleading, or drop entirely. Flag for gate. |
| 19 | jaime-lannister | IGNORANT_OF | blackfish-escapes-riverrun | Tier-1 | — | "it had been the next morning before Jaime had been informed that the Blackfish was not amongst the prisoners." `affc-jaime-07:39` | Jaime does not learn of the escape until after the fact. IGNORANT_OF records a load-bearing gap: the escape exploits precisely the "confusion of the castle changing hands." |

---

## Dropped / considered-but-rejected

**Did the riverlords actively help the Blackfish escape (beyond suspicion)?**
The text at `affc-jaime-07:45` records Jaime's suspicion that "Vance and Piper and their ilk were more like to help the Blackfish escape than clap him into fetters." But the garrison "to a man swore they knew nothing" (`affc-jaime-07:199`) and Jaime credits this — "he thought not." Edmure's testimony makes clear the escape was arranged entirely by Edmure (the submerged portcullis gap) and executed by Brynden alone, with no mention of external riverlord help. The honest modeling is: riverlord complicity = SUSPECTED_OF (proposed above for Vance and Piper), not a CONSPIRES_WITH or ENABLES edge. Asserting stronger agency would over-reach what the text supports.

**`edwyn-frey SUSPECTED_OF ryman-freys-death`**
Edwyn states flatly: "My brother had a hand in this, I'll wager. He allowed the outlaws to escape after they murdered Merrett and Petyr" (`affc-jaime-07:133`). This is Edwyn accusing Black Walder, not a text-supported suspicion about Edwyn. The text attributes the killing to outlaws (Stoneheart/Dondarrion). Walder Rivers immediately denies Edwyn's claim (`affc-jaime-07:135`). Modeling Edwyn as SUSPECTED_OF would be asserting the text's most partisan reading as graph truth. Dropped.

**`black-walder-frey SUSPECTED_OF ryman-freys-death`**
Edwyn directly suspects Black Walder of tipping the outlaws to Ryman's route. This is tempting as a SUSPECTED_OF — but it is one character's bitter accusation, unsupported elsewhere in the text, and Walder Rivers explicitly rebuts it. The accusation is evidence of intra-Frey conflict, not of a graph-worthy suspicion about Black Walder's agency in Ryman's death. Dropped (lens D's cross-arc scope, if anyone's).

**`cersei-lannister MANIPULATES jaime-lannister` via seduction (affc-jaime-01 Great Sept scene)**
Cersei appears in the Great Sept dressed as a servant to plead with Jaime sexually ("I need you. I need my other half. In me. Please, Jaime. Please." `affc-jaime-01:195`). This is clearly attempted `via_seduction` manipulation. DEDUP check: the dyad web already includes CONSPIRES_WITH and the emotional web (LOVER_OF / DISTRUSTS etc.). The question is whether a separate MANIPULATES via_seduction captures new information. Judgment: the Great Sept scene is the opening of Jaime's internal rupture from Cersei, and the manipulation attempt is real. Retained as edge #18 above (the threat-beat), but the seduction beat is BORDERLINE and folded into the same edge with `via_threat` qualifier noted. The gate may split it. Filed here for transparency.

**Did Jaime genuinely intend to trebuchet the child (is it a bluff)?**
The text is deliberately ambiguous — Jaime thinks "With a trebuchet, Jaime thought. If his aunt had been there, would she still say Tyrion was Tywin's son?" (`affc-jaime-06:327`) — suggesting even he recognizes the threat as Tywin-like brutality. But the text never resolves whether it was a bluff. Modeling this ambiguity as a `DECEIVES` edge (bluff = false information) would assert more than the text supports. The `MANIPULATES via_threat` is correct regardless of intent — the threat is real whether or not it would have been carried out. No separate DECEIVES edge for the trebuchet threat proposed.

**`lady-sybell-westerling CONSPIRES_WITH tywin-lannister`**
Lady Sybell acknowledges Tywin's "understanding" with her ("as your lord father bid me" `affc-jaime-07:79` re: ensuring Jeyne carries no child). This pre-existing conspiracy (Sybell was Tywin's agent in Robb's camp) is real and load-bearing. But: (a) the DEDUP list includes Jaime↔Tyrion↔Tywin web as saturated; (b) this conspiracy predates AFFC and is more properly an ASOS beat; (c) Tywin is dead in this arc. Noted but not proposed — this is a gap in the Robert's-Rebellion/WO5K arc, not Jaime's Riverlands command. Defer to cross-arc lens or future dip.

**`jaime-lannister DECEIVES edmure-tully` (re: Blackfish's fate promise)**
Jaime promises Edmure that Brynden can take the black (`affc-jaime-06:57`). The Blackfish escapes instead. This is not a lie Jaime told — the Blackfish refused the offered terms, so the promise was never accepted. Not a DECEIVES edge.

**`ryman-frey MANIPULATES brynden-tully` via threat (the gallows performance)**
Ryman's daily gallows theater is an attempt to coerce Ser Brynden into surrendering. The Blackfish explicitly dismisses it: "My nephew is marked for death no matter what I do. So hang him and be done with it." (`affc-jaime-06:31`). The manipulation fails and is described as a "mummer's show." The edge would be MANIPULATES via_threat, but: (a) it fails completely; (b) Ryman is not a node in scope for this dip (he's dispatched mid-arc). Dropped — the failure is narrative context, not a graph edge gap.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|--------------|------|
| food/drink | AFFC | affc-jaime-05:45 | Pia mulling wine for Jaime and Daven; "stirring the kettle with a spoon"; Peck serves on golden platter |
| food/drink | AFFC | affc-jaime-05:61 | Daven's thirst; "Fill that full again, and I'll call you hero too. I have a thirst" |
| food/drink | AFFC | affc-jaime-05:111 | Siege provisioning: Freys hauling food from Twins but "Ser Ryman claims he does not have enough to share" — besiegers foraging and starving; half the men sent for food don't return |
| food/drink | AFFC | affc-jaime-05:105 | River-fishing keeps besiegers fed: "So long as there are fish in the rivers, we won't starve" + "I gave them nets as well, to fish. It helps keep us fed." |
| food/drink | AFFC | affc-jaime-05:109 | Blackfish's stores: "enough to keep man and horse alive for two full years" — also Jaime-06:95 confirms "Our own supplies are ample" |
| food/drink | AFFC | affc-jaime-06:309 | Jaime orders bathwater and clean clothes for Edmure, then: "Lew, heat some bathwater for my guest. Pia, find him some clean clothing… Peck, wine for Lord Tully. Are you hungry, my lord?" |
| food/drink | AFFC | affc-jaime-06:331 | Singer plays while Edmure eats: "I'll leave you to enjoy your food. Singer, play for our guest whilst he eats." |
| physical description | AFFC | affc-jaime-05:157 | Riverrun's approach: "rising from the narrow point where the Tumblestone joined the Red Fork. The Tully castle looked like a great stone ship with its prow pointed downriver. Its sandstone walls were drenched in red-gold light" |
| physical description | AFFC | affc-jaime-06:201 | The boom across the river and three siege camps; Ryman's "great grey gallows" — "as tall as any trebuchet" |
| physical description | AFFC | affc-jaime-07:39 | The Water Gate escape mechanism: portcullis raised three feet underwater, gap invisible from outside |
| load-bearing quote | AFFC | affc-jaime-06:325 | The full trebuchet speech — Jaime's "I'll pull your walls down, and divert the Tumblestone over the ruins… I'll send him to you when he's born. With a trebuchet." — candidate for jaime-lannister node ## Quotes |
| load-bearing quote | AFFC | affc-jaime-07:295 | "No," he said. "Put this in the fire." — candidate for jaime-lannister or jaime-burns-cerseis-letter node ## Quotes |
| load-bearing quote | AFFC | affc-jaime-07:291 | Cersei's letter verbatim: "Come at once, she said. Help me. Save me. I need you now as I have never needed you before. I love you. I love you. I love you. Come at once." |
| physical description | AFFC | affc-jaime-07:277 | Snow drifting through the window at Riverrun, snowflake melting on the letter; "The yard below was covered by a thin white blanket, growing thicker even as he watched." |
| load-bearing quote | AFFC | affc-jaime-07:39 | "a black fish in a black river floating quietly downstream" — vivid candidate for blackfish-escapes-riverrun node ## Quotes |
| load-bearing quote | AFFC | affc-jaime-05:207 | Jaime's lie about Cleos: "The lie came easy; he could see that it pleased them." — meta-narration of deliberate deception |
| food/drink | AFFC | affc-jaime-05:241 | Genna asks for wine; Jaime pours "one-handed" — moment of Jaime's new physical limitation indexed to hospitality act |
| hospitality | AFFC | affc-jaime-06:309 | Full hospitality sequence for Edmure: bath, clean clothes, wine, food, singer — offered to a man who is effectively Jaime's prisoner; the civility is tactical |
| food/drink | AFFC | affc-jaime-07:173 | "Come, let's drink some more of Hoster Tully's good red wine" — Jaime and Ser Ilyn after sparring, drinking from the Tully cellar |
| food/drink | AFFC | affc-jaime-07:177 | Wine ritual with Ilyn: "The wine was a deep red, sweet and heavy. It warmed him going down." — Tully wine as the liquid setting for Jaime's confession-to-Ilyn monologue |
| physical description | AFFC | affc-jaime-06:11 | Blackfish's appearance: "craggy face, deeply lined and windburnt beneath a shock of stiff grey hair" + "ringmail… greaves, gorget, gauntlets, pauldron, and poleyns of blackened steel, none half so dark as the look upon his face" |
| food/drink | AFFC | affc-jaime-07:219 | Lord Emmon addresses Riverrun's assembled people "as stableboys and serving girls and smiths listened in a sullen silence and a light rain fell down upon them all" — garrison receiving a three-hour speech; the food-and-provisioning context of Emmon's new stewardship |
