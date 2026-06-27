# Lens B — Revelation / Agency / Whodunit — D5 Arya/Harrenhal proposal (S154)

> Chapters read in full: agot-arya-05, acok-arya-07, acok-arya-08, acok-arya-09, acok-arya-10.
> Also skimmed: acok-arya-04, acok-arya-05.
> Deduped against: baseline.md 146-edge web.

---

## Proposed NEW nodes

### 1. `death-of-weese` · "Death of Weese" · event.death

Jaqen H'ghar's second death-debt, named by Arya in the bathhouse (acok-arya-08). Weese's own dog — raised by him from a pup — tears his throat out in the yard of Harrenhal while he is still alive. Arya finds him sprawled on the cobblestones, throat a "red ruin." Jaqen acknowledges the kill with a two-finger salute. The method ("dark magic" vs. deliberate instigation) is ambiguous in-world; that ambiguity is the point.

Anchor quote: `"Weese was sprawled across the cobbles, his throat a red ruin, eyes gaping sightlessly up at a bank of grey cloud."` acok-arya-08:113

---

### 2. `naming-gambit` · "The Naming Gambit" · event.deception

The pivotal exchange in the Harrenhal godswood (acok-arya-09): Arya names Jaqen H'ghar himself as her third death, forcing him to negotiate. He offers her a trade — she unnames him in exchange for his help freeing the caged northmen (which produces the `guards-killed` weasel-soup massacre). This is the leverage-reversal beat that CAUSES the fall of Harrenhal. It is currently unwired: `guards-killed` has no incoming causal edges and no node explains the gambit.

Anchor quote: `"Arya put her lips to his ear. 'It's Jaqen H'ghar.'"` acok-arya-09:177

---

### 3. `jaqen-farewell-and-coin` · "Jaqen's Farewell — the Iron Coin and Valar Morghulis" · event.incident

The scene at the end of acok-arya-09, immediately after the guards-killed dungeon massacre: Jaqen kneels beside Arya in the killing ground, explains the debt is paid, then changes his face (the face-change is a TEXT event, not theory). He presses the iron coin into her palm, instructs her to give it to any man from Braavos and say "valar morghulis," and departs. Arya repeats the words. This is the ORIGIN of the iron-coin seam: the coin's `GIFTED_TO arya` edge already exists but cites ASOS (a recollection); the actual giving event has no node.

Anchor quote: `"He lifted her hand and pressed a small coin into her palm."` acok-arya-09:327

Secondary anchor (the words): `"give that coin to any man from Braavos, and say these words to him—valar morghulis."` acok-arya-09:339

---

### 4. `arya-escapes-harrenhal` · "Arya Escapes Harrenhal" · event.incident

The postern-gate escape (acok-arya-10): Arya plans the escape, deceives the stableboy using Roose Bolton's livery and authority, recruits Gendry and Hot Pie, uses Jaqen's iron coin to distract the gate guard, then kills the guard with Bolton's stolen dagger. She pulls open the postern and the three ride out into the rain. This is the downstream terminus of the weasel-soup / fall-of-harrenhal consequence chain and the departure event that the Braavos arc (S150) hangs off from the origin end. It is also needle's second named kill (the stableboy was first).

Anchor quote: `"Arya slid her dagger out and drew it across his throat, as smooth as summer silk."` acok-arya-10:309

Secondary anchor (the coin's role): `"Her fingers dug down beneath her tunic and came out clutching the coin Jaqen had given her. In the dark the iron could pass for tarnished silver."` acok-arya-10:307

---

### 5. `stableboy-killing` · "Needle's First Kill — the Stableboy" · event.death

> **Note:** Lens A is the primary proposer of this node per the brief. Proposing here because it is also the moral-weight revelation that MOTIVATES Arya's later armed ferocity (it is the first time she kills a person, not an animal). If Lens A has minted the node, this section provides only the MOTIVATES edge row; the node itself should be dropped from this lens at synthesis.

The scene is in agot-arya-05, but it is NOT shown — it is only referenced retrospectively. The chapter ends when Yoren seizes Arya at the Sept of Baelor. The stableboy killing must have occurred between the Red Keep escape (agot-arya-04 end) and the Sept scene (agot-arya-05 framing). In the chapter text of agot-arya-05 we have no direct flashback prose of the kill itself — it is retrospective knowledge ("Compared with catching cats, pigeons were easy" and her awareness of Needle are its only traces in this chapter). The text does not give the stableboy a name, nor does it show us the moment in agot-arya-05 itself.

**Coordination note:** If Lens A reads agot-arya-04 for the kill scene (the Red Keep escape chapter), that chapter file contains the actual event. agot-arya-05 is the day-after wandering of Flea Bottom; the killing is backstory by then. I cannot verbatim-quote the killing from agot-arya-05 because the prose doesn't show it. I will NOT propose the node from this lens; I will only propose the downstream MOTIVATES edge if Lens A confirms the node exists.

**Deferred: node not proposed by Lens B. See MOTIVATES edge in edge table.**

---

## Proposed NEW edges

Format: `source_slug [EDGE_TYPE] target_slug | Tier | quote "..." chapter:line | rationale`

---

### Death-of-Weese event hub

| source | edge | target | tier | quote + cite | rationale |
|--------|------|--------|------|-------------|-----------|
| `jaqen-hghar` | `AGENT_IN` | `death-of-weese` | Tier 1 | `"Jaqen H'ghar was leaning up against the side of the Wailing Tower. When he saw her looking, he lifted a hand to his face and laid two fingers casually against his cheek."` acok-arya-08:123 | Jaqen's acknowledgment gesture directly after Weese's death; the two-finger salute = two deaths done |
| `arya-stark` | `COMMANDS_IN` | `death-of-weese` | Tier 1 | `"I have a message." … "Weese," she whispered.` acok-arya-08:83-84 | Arya whispers Weese's name to Jaqen in the bathhouse — this is the naming command that triggers the kill |
| `weese` | `VICTIM_IN` | `death-of-weese` | Tier 1 | `"Weese was sprawled across the cobbles, his throat a red ruin"` acok-arya-08:113 | Weese is the victim |
| `death-of-weese` | `LOCATED_AT` | `harrenhal` | Tier 1 | `"Weese was sprawled across the cobbles"` acok-arya-08:113 | Scene set in Harrenhal yard |
| `death-of-weese` | `SUB_BEAT_OF` | `chiswyck-dies-three-days-later` | Tier 3 | — | **[BORDERLINE — reject]** These are parallel sibling events within the same FM-debt frame, not one being a sub-beat of the other. See Dropped section. |

---

### Naming-gambit event hub

| source | edge | target | tier | quote + cite | rationale |
|--------|------|--------|------|-------------|-----------|
| `arya-stark` | `AGENT_IN` | `naming-gambit` | Tier 1 | `"Arya put her lips to his ear. 'It's Jaqen H'ghar.'"` acok-arya-09:177 | Arya executes the gambit — she is the sole agent |
| `jaqen-hghar` | `VICTIM_IN` | `naming-gambit` | Tier 1 | `"Even in the burning barn … he had not seemed so distraught as he did now."` acok-arya-09:179 | Jaqen is the one named — the target of the leverage |
| `arya-stark` | `MANIPULATES` | `jaqen-hghar` | Tier 1 | `"Jaqen's smile came and went. 'A girl might … name another name then, if a friend did help?'"` acok-arya-09:187 | Jaqen's offer to trade = proof of successful manipulation; qualifier required → `tactical-leverage` |
| `naming-gambit` | `ENABLES` | `guards-killed` | Tier 1 | `"'Come.' 'Now?' She had never thought he would act so quickly."` acok-arya-09:191-193 | The gambit is the immediate precondition: Jaqen acts because Arya has named him; without the un-naming bargain, the dungeon massacre never happens |
| `guards-killed` | `ENABLES` | `fall-of-harrenhal` | Tier 1 | `"Come dawn … Harrenhal had been taken."` acok-arya-09:349 (Pinkeye's report) | Already implied by `guards-killed SUB_BEAT_OF fall-of-harrenhal` in baseline — confirming the directional causal hop is new; the baseline has the SUB_BEAT_OF but not the ENABLES |

> Note on `MANIPULATES` qualifier: the locked vocab says Tier-1 qualifier types include MANIPULATES. Proposed qualifier: `tactical-leverage` — Arya uses the naming as a weapon, not seduction or deception.

---

### Jaqen-farewell-and-coin event hub

| source | edge | target | tier | quote + cite | rationale |
|--------|------|--------|------|-------------|-----------|
| `jaqen-hghar` | `AGENT_IN` | `jaqen-farewell-and-coin` | Tier 1 | `"He lifted her hand and pressed a small coin into her palm."` acok-arya-09:327 | Jaqen performs the gift |
| `arya-stark` | `PARTICIPATES_IN` | `jaqen-farewell-and-coin` | Tier 1 | `"'Valar morghulis,' Arya repeated."` acok-arya-09:341 | Arya is the recipient and learns the words |
| `iron-coin` | `WIELDED_IN` | `jaqen-farewell-and-coin` | Tier 1 | `"He lifted her hand and pressed a small coin into her palm."` acok-arya-09:327 | The coin is the instrument of the gift |
| `jaqen-hghar` | `REVEALS_TO` | `arya-stark` | Tier 1 | `"give that coin to any man from Braavos, and say these words to him—valar morghulis."` acok-arya-09:339 | Jaqen reveals the coin's use and the words to Arya |
| `jaqen-farewell-and-coin` | `ENABLES` | `arya-escapes-harrenhal` | Tier 2 | `"Her fingers dug down beneath her tunic and came out clutching the coin Jaqen had given her."` acok-arya-10:307 | The coin is the physical prop Arya uses to distract the gate guard; without it the escape is much harder |
| `jaqen-farewell-and-coin` | `LOCATED_AT` | `harrenhal` | Tier 1 | — (scene set in Harrenhal courtyard among the dead guards after guards-killed) | Scene location |
| `jaqen-farewell-and-coin` | `ENABLES` | `arya-departs-for-braavos` | Tier 2 | — | **[BORDERLINE]** The coin ENABLES the Braavos departure, but there are multiple intervening years and choices. The ASOS recollection already has the coin wired to departs-for-braavos. Proposing as ENABLES (precondition, not direct cause) — the farewell event is the origin node that the existing wire should anchor to. Synthesis may prefer to re-cite the existing GIFTED_TO edge rather than add a new event-level ENABLES. Flag for Opus. |

---

### Arya-escapes-harrenhal event hub

| source | edge | target | tier | quote + cite | rationale |
|--------|------|--------|------|-------------|-----------|
| `arya-stark` | `AGENT_IN` | `arya-escapes-harrenhal` | Tier 1 | `"Arya slid her dagger out and drew it across his throat, as smooth as summer silk."` acok-arya-10:309 | Arya executes the escape and kills the guard |
| `gendry` | `AGENT_IN` | `arya-escapes-harrenhal` | Tier 1 | `"Gendry nodded."` acok-arya-10:289 | Gendry agrees and participates (brings swords, rides out) |
| `hot-pie` | `AGENT_IN` | `arya-escapes-harrenhal` | Tier 1 | `"Hot Pie's red round face peered out from under a hood."` acok-arya-10:285 | Hot Pie is present with bread and cheese |
| `needle` | `WIELDED_IN` | `arya-escapes-harrenhal` | Tier 2 | — | **[BORDERLINE]** Arya uses Bolton's stolen *dagger* at the postern gate (see quote above), not Needle. Needle is present but the kill weapon is the dagger. Proposing a `bolton-dagger WIELDED_IN arya-escapes-harrenhal` edge instead. Needle not wielded here. |
| `arya-escapes-harrenhal` | `LOCATED_AT` | `harrenhal` | Tier 1 | `"set in an angle of the wall beneath a defensive tower"` acok-arya-10:292 | The escape is through Harrenhal's postern gate |
| `fall-of-harrenhal` | `ENABLES` | `arya-escapes-harrenhal` | Tier 2 | `"'Lord Bolton is giving Harrenhal to the Bloody Mummers, he told me so.'"` acok-arya-10:241 | The fall of Harrenhal + Bolton's impending departure is the REASON Arya acts now; without the political chaos of the takeover, escape is harder and less urgent |
| `arya-escapes-harrenhal` | `ENABLES` | `arya-departs-for-braavos` | Tier 3 | — | Multiple legs and ASOS arcs intervene; this is too loose a causal hop for ENABLES — reject; see Dropped. |

---

### Witness-in and reveal edges for the guards-killed / fall-of-harrenhal

| source | edge | target | tier | quote + cite | rationale |
|--------|------|--------|------|-------------|-----------|
| `arya-stark` | `WITNESS_IN` | `guards-killed` | Tier 1 | `"Arya pressed back against the wall as Rorge began to cut throats."` acok-arya-09:274 | Arya is physically present and watching — she sees the massacre. The prose confirms she sees it (pressed against wall, observing). WITNESS_IN criteria met. |
| `arya-stark` | `WITNESS_IN` | `ser-amory-lorch-executed` | Tier 1 | `"a page named Nan poured wine for Roose Bolton and Vargo Hoat as they stood on the gallery, watching the Brave Companions parade Ser Amory Lorch naked through the middle ward … Shagwell kicked him down into the bear pit."` acok-arya-09:391-392 | Arya is Nan the cupbearer watching from the gallery; she sees Amory paraded and kicked into the pit. Clear WITNESS_IN. |
| `robett-glover` | `WITNESS_IN` | `guards-killed` | Tier 2 | `"Once freed, the captives stripped the dead guards of their weapons and darted up the steps."` acok-arya-09:281 | Glover was in the dungeon cell during the massacre and witnesses it directly |
| `vargo-hoat` | `SUSPECTED_OF` | `fall-of-harrenhal` | Tier 2 | `"A goat has no loyalty. Soon a wolf banner is raised here, I think."` acok-arya-09:299 | Jaqen's aside confirms Vargo Hoat orchestrated the Bolton-switch as a deliberate betrayal of Lannister service; the text shows his role but he is presented as already-decided agent rather than proven conspirator at any one moment |

---

### Stableboy moral-weight edge (contingent on Lens A minting the node)

| source | edge | target | tier | quote + cite | rationale |
|--------|------|--------|------|-------------|-----------|
| `stableboy-killing` | `MOTIVATES` | `arya-stark` | Tier 2 | — | **[CONTINGENT]** If Lens A mints `stableboy-killing`, this MOTIVATES edge captures the moral weight: "the boy was the first" shapes Arya's relationship to violence. No direct quote from agot-arya-05 proves it (the chapter doesn't show the killing); the edge is Tier-2 structural inference. MOTIVATES target = character (Arya), not event — correct usage. Drop if Lens A doesn't mint the node. |

---

### Fall-of-Harrenhal agency — Roose Bolton's hidden hand

| source | edge | target | tier | quote + cite | rationale |
|--------|------|--------|------|-------------|-----------|
| `roose-bolton` | `SUSPECTED_OF` | `fall-of-harrenhal` | Tier 2 | `"A goat has no loyalty. Soon a wolf banner is raised here, I think."` acok-arya-09:299 | Jaqen implies Vargo Hoat's switch was arranged; the text does not prove Roose gave the order but it is load-bearing in-world: Bolton benefits, Vargo reports to him afterward, and the timing (Bolton arrives "before the day's out") implies pre-coordination. The text never shows the command. SUSPECTED_OF is the right type. |

> Already in baseline: `vargo BETRAYS amory` and `roose + vargo COMMANDS_IN ser-amory-lorch-executed`. The above SUSPECTED_OF captures Roose's hidden role in the *fall itself* (not just the execution) — this is the distinction.

---

## Dropped / considered-but-rejected

1. **`death-of-weese SUB_BEAT_OF chiswyck-dies-three-days-later`** — These are sequential events within the same FM-debt structure but are parallel siblings, not parent-child. No `SUB_BEAT_OF` relationship.

2. **`arya-escapes-harrenhal ENABLES arya-departs-for-braavos`** — Too many intervening legs (all of ASOS Arya, the BWB, Saltpans, etc.) for ENABLES to be defensible. The iron-coin is the proper seam connector already wired downstream.

3. **`arya-stark WITNESS_IN naming-gambit`** — Arya is not a passive witness here; she is the AGENT. WITNESS_IN is for load-bearing perception of a charged incident where the character observes but does not act as primary agent. Rejected; AGENT_IN is correct.

4. **`jaqen-hghar TEACHES arya-stark` (the valar morghulis lesson)** — Already exists in baseline (`jaqen TEACHES arya`). Do not re-propose.

5. **`jaqen-hghar KILLS arya-stark`** — Already in baseline. Do not re-propose.

6. **`jaqen-hghar face-change event`** — The face-change itself is TEXT (acok-arya-09:311-315) but it is part of the `jaqen-farewell-and-coin` event hub — no need for a separate node. The face-change is a beat within that event. A `SUB_BEAT_OF` edge could be proposed but would over-granularize a single scene.

7. **Faceless Men cosmology / valar-morghulis-as-religion** — GATED. The phrase `valar morghulis` is a TEXT EVENT (Arya learns the words, uses them at the gate kill). Node-prose only for theology. No edge proposed.

8. **`jaqen=alchemist-at-Oldtown / Jaqen's true identity`** — GATED. The new face is a text event; identity stays node-prose.

9. **`incident-at-the-trident MOTIVATES arya-stark`** — The baseline notes this as a possible light-touch edge (gap #9). It is pre-D5 material (AGOT Trident) and Lens B's scope is Harrenhal. Deferring to synthesis decision; not proposing.

10. **`arya-stark PERCEIVED_AS weasel` / `arya-stark DISGUISED_AS pinkeye`** — Arya's service-name disguises under Pinkeye (as Nan) and under Weese (as Weasel) are identity layers but the `DISGUISED_AS weese` and `DISGUISED_AS yoren` already exist in baseline for the alias layer. `Nan` is a new alias but thin on graph value; node-prose.

11. **`needle WIELDED_IN arya-escapes-harrenhal`** — The kill weapon at the postern is Bolton's stolen *dagger*, not Needle (confirmed by the quote: "Arya slid her dagger out"). Needle is holstered but not used. Not proposing WIELDED_IN for Needle here.

12. **`bolton-dagger` as new artifact node** — The dagger is named only as "Lord Bolton's dagger" / "the dagger" in acok-arya-10:263 and :309. No proper name. An unnamed dagger is below the threshold for a named artifact node. Capture in harvest as a descriptive item.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|-------------|------|
| food | ACOK | acok-arya-07:11 | Arya's drudge rations: "bread every day, and barley stews with bits of carrot and turnip, and once a fortnight even a bite of meat" — thin servitude fare |
| food | ACOK | acok-arya-07:13 | Hot Pie in the kitchens: apple tart theft, beaten with a wooden spoon |
| food | ACOK | acok-arya-07:129 | Chiswyck's story in full: Gregor's men at the alehouse — "keep our horns full … brown piss" ale — the brewer's daughter scene; the brewer's change-making. Grim hospitality-violation + sexual violence + food context |
| food | ACOK | acok-arya-08:91 | Weese's promised capon supper — "the wing off the capon that Weese had spoken of" goes to his bed-woman; Arya gets stale stew; the uneaten last bits are Weese's final meal before his throat is torn out. Dark food irony. |
| food | ACOK | acok-arya-09:1-4 | Hot Pie baking tarts at midnight — "stuffed with chopped nuts and fruit and cheese, the crust flaky and still warm from the oven." Arya filches one. "Eating Ser Amory's tart made Arya feel daring." |
| food | ACOK | acok-arya-09:47 | Vargo Hoat's ox-carts of plunder arrive with "bags of flour, pens of squealing hogs and scrawny dogs and chickens" |
| food | ACOK | acok-arya-09:217-241 | The weasel-soup itself: boiling broth used as weapon-delivery. "The bloody broth isn't bloody ready yet … it needs to simmer. We only now put in the onions." Rorge and Biter carry kettles; Biter grabs "half-charred rabbit right off the spit … honey dripped between his fingers." |
| food | ACOK | acok-arya-09:283 | Biter in the dungeon aftermath: "Biter sat on top of one of the dead men, holding a limp hand as he gnawed at the fingers. Bones cracked between his teeth." — extreme grim register |
| food | ACOK | acok-arya-09:351 | Shagwell's talking heads: `"What did you die of?" one head asked. "Hot weasel soup," replied the second."` — food as punchline / dark humor about the massacre |
| food | ACOK | acok-arya-10:1-17 | Post-fall punishment economy: cook spared "because he'd made the weasel soup"; other Lannister-collaborators executed or stocked. Food-labour as survival currency. |
| food | ACOK | acok-arya-10:161-167 | Roose Bolton orders: "Barley bread, butter, and boar. … hot spice wine … he doesn't want it cold." The supper Arya fetches; she helps Hot Pie crumble in the spices. Bolton eats alone and burns the book. |
| food | ACOK | acok-arya-10:165 | Spice wine recipe note: "took out a kettle, filled it with a heavy, sweet red. Hot Pie was told to crumble in the spices as the wine heated." |
| food | AGOT | agot-arya-05:11-43 | Arya in Flea Bottom: pigeon hunting with stick-sword; "bowl o' brown" pot-shops; the tart pushcart man ("Three coppers"); barley stew with carrot, turnip, apple, "a film of grease swimming on top," lemon cake longing. Richest food-poverty sequence in the arc. |
| food | AGOT | agot-arya-05:43 | The pot-shops "brown" contents: "barley in it, and chunks of carrot and onion and turnip, and sometimes even apple … a film of grease swimming on top. Mostly she tried not to think about the meat. Once she had gotten a piece of fish." |
| hospitality-violation | ACOK | acok-arya-07:53-55 | Lannister men stabbed and hanged over Brave Companions arrival; Vargo and Ser Harys "embraced and kissed and swore to love each other always" under Tywin's watch — forced hospitality pantomime |
| physical-description | ACOK | acok-arya-07:21 | Harrenhal's Kingspyre Tower: "lopsided beneath the weight of the slagged stone that made it look like some giant half-melted black candle" — vivid dragon-fire scar description |
| physical-description | ACOK | acok-arya-07:31 | The scale of Harrenhal: stables for a thousand horses, twenty-acre godswood, Hall of a Hundred Hearths (only ~33-35 hearths by Arya's count), everything "built to an inhuman scale" — load-bearing for the cursed-castle motif |
| physical-description | ACOK | acok-arya-09:47 | "A huge black bear rolled by, caged in the back of a wagon" — the bear that will kill Amory Lorch; first appearance |
| physical-description | ACOK | acok-arya-09:391 | The bear pit execution: Shagwell kicks Amory down, Arya watches from gallery. "The bear is all in black. Like Yoren." Load-bearing quote. |
| physical-description | ACOK | acok-arya-09:311-315 | Jaqen's face-change: "His cheeks grew fuller, his eyes closer; his nose hooked, a scar appeared on his right cheek where no scar had been before. And when he shook his head, his long straight hair, half red and half white, dissolved away to reveal a cap of tight black curls." + "a shiny gold tooth." |
| physical-description | ACOK | acok-arya-10:53 | The iron coin: "a piece of iron no larger than a penny and rusted along the rim. One side had writing on it, queer words she could not read. The other showed a man's head, but so worn that all his features had rubbed off." |
| load-bearing quote | ACOK | acok-arya-07:105 | "She had killed Chiswyck with a whisper, and she would kill two more before she was through. I'm the ghost in Harrenhal." — Arya's first self-articulation as killer-by-proxy; key character-voice moment |
| load-bearing quote | ACOK | acok-arya-09:117 | "Jaqen made me brave again. He made me a ghost instead of a mouse." — Arya's articulation of Jaqen's effect on her character arc |
| load-bearing quote | ACOK | acok-arya-09:345 | `"Jaqen is as dead as Arry," he said sadly, "and I have promises to keep. Valar morghulis, Arya Stark."` — Jaqen names her true identity at farewell |
| load-bearing quote | ACOK | acok-arya-10:311 | `"Valar morghulis," she whispered as he died.` — Arya repeating the words at the gate guard's death; first independent use of the FM phrase |
| load-bearing quote | ACOK | acok-arya-10:213 | `"it felt as though Syrio Forel walked beside her, and Yoren, and Jaqen H'ghar, and Jon Snow"` — the ghost-companions line; character-formation moment |
| foreshadowing | ACOK | acok-arya-09:317 | `"If you would learn, you must come with me." / "Far and away, across the narrow sea."` — Jaqen's first invitation to Braavos/FM training; her refusal deferred to ASOS; the seed of the entire Braavos arc |
| foreshadowing | ACOK | acok-arya-10:155 | Arya salutes the heart tree: `"Valar morghulis," she told the old gods of the north. She liked how the words sounded when she said them.` — rehearsal before the gate-kill use |
| whodunit-note | ACOK | acok-arya-08:119 | Arya's reasoning about Jaqen's method: "Chiswyck had been easy, anyone could push a man off the wallwalk, but Weese had raised that ugly spotted dog from a pup, and only some dark magic could have turned the animal against him." — in-world uncertainty about HOW the kills happen; not a theory edge, but captures the mystery register |
| object | ACOK | acok-arya-10:263 | Bolton's dagger taken by Arya from his solar table: "She rolled it up tight and thrust it through her belt. He'd left his dagger on the table as well, so she took that too, just in case Gendry lost his courage." — unnamed artifact used to kill the gate guard; potential harvest-queue item if an escape-weapons cluster is ever assembled |
| physical-description | ACOK | acok-arya-10:69 | Roose Bolton being leeched: "Leeches clung to the inside of his arms and legs and dotted his pallid chest, long translucent things that turned a glistening pink as they fed." — iconic Bolton characterization |
| food | ACOK | acok-arya-07:97 | Arya's prayer as she mends her shift: counting names "every time she pushed the bone needle through the undyed wool" — intimacy between domestic labor and the kill-list ritual |
