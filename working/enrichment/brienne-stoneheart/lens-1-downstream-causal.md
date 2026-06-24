# Lens 1 — Downstream Causal / Consequence Chains
## Brienne → Stoneheart arc (AFFC)

> Written by: LENS 1 (downstream-causal/consequence)
> Date: 2026-06-24
> Source chapters: affc-brienne-01 through affc-brienne-08; asos-epilogue; graph/nodes/events/raid-on-saltpans.node.md

---

## PROPOSED EDGES

### A. Wire the islanded `raid-on-saltpans`

**A1.** `rorge --AGENT_IN--> raid-on-saltpans` | tier-1 | affc-brienne-07:48 | *"These are the men who raided Saltpans."* + node body (affc20) confirms Rorge led the band. The in-chapter text ties Rorge directly to the inn fight: he wears the Hound's helm ("beneath the dark hood of the lead rider Brienne glimpsed an iron snout and rows of steel teeth, snarling" affc-brienne-07:265) and the node body names him as leader of the Saltpans raid.
- Source line for the helm attribution: affc-brienne-07:265 — *"beneath the dark hood of the lead rider Brienne glimpsed an iron snout and rows of steel teeth, snarling."*
- Source line for the node naming Rorge as raider: raid-on-saltpans.node.md line 29 — *"One band of fleeing Brave Companions is led by Rorge, who has his constant companion Biter at his side."*

`rorge --AGENT_IN--> raid-on-saltpans` | tier-1 | affc-brienne-07:265 | *"beneath the dark hood of the lead rider Brienne glimpsed an iron snout and rows of steel teeth, snarling"* | Rorge wears the Hound's helm leading the inn attack; node body identifies him as leader of the Saltpans raid band.

**A2.** `biter --AGENT_IN--> raid-on-saltpans` | tier-1 | raid-on-saltpans.node.md:29 | *"One band of fleeing Brave Companions is led by Rorge, who has his constant companion Biter at his side."* | Biter is Rorge's inseparable companion and co-participant in the raid.

**A3.** `brave-companions --AGENT_IN--> raid-on-saltpans` | tier-1 | raid-on-saltpans.node.md:25 | *"Using Harrenhal as their base, the brutal Brave Companions raid the riverlands on behalf of first Lord Tywin Lannister and then Lord Roose Bolton."* | Rorge and Biter are fleeing Brave Companions; the raid is a direct sequel to their service.

**A4.** `raid-on-saltpans --LOCATED_AT--> saltpans` | tier-1 | affc-brienne-07:77 | *"At Saltpans, they had found only death and desolation."* | The event's location is definitional.

**A5.** `sandor-clegane --PERCEIVED_AS--> raid-on-saltpans` — NEEDS_VOCAB: The causal relationship is that the false attribution of the raid to Sandor is the *reputational engine* of Brienne's hunt. The nearest vocabulary options are REPUTED_AS (character → character) or the realm blames Sandor for the raid. No edge type cleanly models "entity X is falsely blamed for event Y." The fact is:
- Sandor is REPUTED_AS the perpetrator of the Saltpans atrocity (this works as a character attribute).
- Brienne SEEKS sandor-clegane (already in graph) because she believes he perpetrated the raid.
- The causal link between the raid and Brienne's hunt is mediated by the false reputation.

Proposed workaround — two edges that together encode the engine:
- `sandor-clegane --REPUTED_AS--> mad-dog-of-saltpans` — NEEDS_VOCAB: "Mad Dog of Saltpans" is an epithet/alias, not a slug. The alias should be added to the `sandor-clegane` node's `aliases:` field, not as an edge. FLAG to orchestrator: add alias "Mad Dog of Saltpans" to sandor-clegane node.
- `raid-on-saltpans --CAUSES--> brienne-seeks-sandor-hunt` — NEEDS_VOCAB: There is no existing event node for "Brienne's hunt for Sandor." The CAUSES chain runs: raid → false attribution → Brienne seeks Sandor. This is better handled as a MOTIVATES edge (Stoneheart's vengeance arc covers the broader campaign). See E1 below.

**A6. Randyll Tarly false-rumor edge — direct DECEIVES:**
`randyll-tarly --DECEIVES--> smallfolk` — NEEDS_VOCAB: The target "smallfolk" has no node. Better encoded as:
`randyll-tarly --SUSPECTED_OF--> raid-on-saltpans` is wrong (he didn't do the raid).

Cleanest encoding: REPUTED_AS edge on the brotherhood. The node body (line 35) says Tarly "spreads rumors that blame the raid on Beric Dondarrion's brotherhood without banners." This is a DECEIVES relationship, but the target is a diffuse "smallfolk/public opinion" with no slug. FLAG to orchestrator: Tarly's rumor campaign is a documented political act; propose new edge type or note in harvest.

**A7. The key causal line from the raid to the brotherhood's blackened name:**
`raid-on-saltpans --CAUSES--> brotherhood-without-banners-blackened-reputation` — NEEDS_VOCAB: No event node for the brotherhood's reputational damage exists. However, the wiki node body (line 55) says: *"Meanwhile, the influence of the vengeful Lady Stoneheart has changed the brotherhood into a band that kills in large numbers. They use the inn to capture assumed offenders and hang them along nearby roads, often shoving pieces of salt into their mouths as reference to the raid on Saltpans."* This is a downstream consequence of BOTH the raid (Saltpans as motivating reference) AND Stoneheart's rise. This is captured better in Section B.

---

### B. De-dead-end `catelyn-rises-as-lady-stoneheart` and `brienne-brought-before-lady-stoneheart`

**B1. The Brotherhood's vigilante turn — Stoneheart MOTIVATES the hangings:**
`catelyn-rises-as-lady-stoneheart --CAUSES--> brotherhood-without-banners-hanging-campaign`

No event node exists for the hanging campaign. However, the chapter text gives a direct quote describing the causal change:

affc-brienne-07:43 — *"Who they were did not concern Brienne half so much as who had hanged them. The noose was the preferred method of execution for Beric Dondarrion and his band of outlaws, it was said."*

More explicit in the wiki node body (line 55): *"Meanwhile, the influence of the vengeful Lady Stoneheart has changed the brotherhood into a band that kills in large numbers."*

PROPOSED: Mint a new event node for the hanging campaign, then chain it.

**NEW NODE PROPOSAL:**
- slug: `brotherhood-hanging-campaign`
- type: event.incident
- one-line: The Brotherhood Without Banners under Lady Stoneheart begins mass-hanging Freys, Lannister-adjacent men, and anyone accused of Saltpans-connected atrocities; salt is stuffed in victims' mouths as reference to the raid.

If that node is minted:
`catelyn-rises-as-lady-stoneheart --CAUSES--> brotherhood-hanging-campaign` | tier-1 | affc-brienne-07:43 | *"Who they were did not concern Brienne half so much as who had hanged them. The noose was the preferred method of execution for Beric Dondarrion and his band of outlaws, it was said."*

And:
`raid-on-saltpans --ENABLES--> brotherhood-hanging-campaign` | tier-1 | affc-brienne-07:17 | *"Someone had shoved a jagged white rock between his teeth. A rock, or . . . 'Salt,' said Septon Meribald."* | The salt-in-mouth ritual references Saltpans directly; the raid is the pretext/symbol the Brotherhood adopts for its executions.

**B2. The hanging-tree "sword or noose" choice — DOWNSTREAM ASSESSMENT:**
The text of `affc-brienne-08` ends at line 349: *"She screamed a word."* This is a deliberate narrative cliffhanger. What follows (ADWD and TWOW-preview material) involves Brienne returning with Jaime in tow, but this is NOT resolved in AFFC. The downstream of the sword-or-noose choice is **forward-dangling into a later book with no existing node.**

**FLAG TO ORCHESTRATOR (forward-dangling):** `brienne-brought-before-lady-stoneheart` has 0 outgoing edges and correctly so in AFFC. The downstream node "Brienne betrays Jaime / leads him to Stoneheart" belongs in ADWD/TWOW. Do NOT invent it here. The only honest edge from this node available in-text is:

`brienne-brought-before-lady-stoneheart --CAUSES--> brienne-brought-before-lady-stoneheart` — obviously wrong. No in-AFFC outgoing causal edge is possible for this node.

Proposed in-text outgoing edge that IS grounded:
`catelyn-stark --COMMANDS_IN--> brienne-brought-before-lady-stoneheart` already exists (per baseline). No new edge.

What IS evidenced at `brienne-brought-before-lady-stoneheart`:
- Pod and Hyle are also victims. The baseline already has them as VICTIM_IN.
- Stoneheart demands Brienne kill Jaime or hang. This is a MOTIVATES-like thing but the target is Brienne (a character), and what it motivates is the ADWD-era action. Cannot be grounded in AFFC text for a downstream event.

**B3. Stoneheart's vengeance motivation:**
`catelyn-stark --MOTIVATES--> catelyn-rises-as-lady-stoneheart` — NEEDS_VOCAB check: MOTIVATES targets a CHARACTER, and catelyn-stark IS a character. But catelyn-stark and catelyn-rises-as-lady-stoneheart share identity (the rise IS catelyn-stark's undeath). This would be an agency-collapse violation (a beat that IS the character does not CAUSE the character's state).

Cleaner: The vengeance motivation is already embedded in the node's description. No edge needed.

**B4. Actual CAUSES chain from the epilogue — ASOS epilogue proves the vengeance pattern:**
The epilogue (asos-epilogue.md) shows Merrett Frey being hanged. The Brotherhood explicitly states they are avenging Robb Stark / the Red Wedding. Quote at line 155: *"That Young Wolf never will," said the one-eyed outlaw.* And line 159: *"'We know some about murder, though.' 'Not murder.' His voice was shrill. 'It was vengeance...'"*

PROPOSED:
`catelyn-rises-as-lady-stoneheart --CAUSES--> merrett-frey-hanging` — NEW NODE needed.

**NEW NODE PROPOSAL:**
- slug: `merrett-frey-hanging`
- type: event.death
- one-line: Merrett Frey is hanged by the Brotherhood Without Banners at Oldstones while attempting to ransom Petyr "Pimple" Frey; Lady Stoneheart is the unspeaking judge.

`catelyn-rises-as-lady-stoneheart --CAUSES--> merrett-frey-hanging` | tier-1 | asos-epilogue:177 | *"Merrett Frey opened his mouth to plead, but the noose choked off his words. His feet left the ground, the rope cutting deep into the soft flesh beneath his chin."* | The Brotherhood acts under Stoneheart's command; she nods assent; Merrett's hanging is a direct downstream consequence of her rise and vengeance campaign.

Also:
`catelyn-stark --COMMANDS_IN--> merrett-frey-hanging` | tier-1 | asos-epilogue:175 | *"Lady Catelyn's eyes never left him. She nodded."* | Stoneheart's nod is the direct command that triggers the hanging.

`house-frey --VICTIM_IN--> merrett-frey-hanging` | tier-1 | asos-epilogue:117 | *"You'd never dare hang a Frey."* | Merrett is a Frey; the hanging is explicitly framed as vengeance against the Freys.

`merrett-frey --VICTIM_IN--> merrett-frey-hanging` | tier-1 | asos-epilogue:177 | *"Merrett Frey opened his mouth to plead, but the noose choked off his words."*

`petyr-pimple-frey --VICTIM_IN--> merrett-frey-hanging` | tier-2 | asos-epilogue:99 | *"Petyr Pimple was hanging from the limb of an oak, a noose tight around his long thin neck."* | Petyr is also hanged before Merrett arrives; both are victims of the same Brotherhood action. NOTE: `petyr-pimple-frey` is likely not a node — FLAG to orchestrator for slug check; may need mint.

`red-wedding --MOTIVATES--> catelyn-stark` | tier-1 | asos-epilogue:155-159 | *"That Young Wolf never will," said the one-eyed outlaw.* / *"It was vengeance, we had a right to our vengeance."* | The Brotherhood's stated purpose is avenging the Red Wedding; MOTIVATES targets a character (catelyn-stark), whose drive under undeath is the vengeance campaign. AGENCY CHECK: MOTIVATES(red-wedding → catelyn-stark) = the event motivates the person's actions ✓.

---

### C. Gendry's inn-smith role and the Biter kill

**C1.** `gendry --KILLS--> biter` — per baseline this ALREADY EXISTS. Confirmed in-text: affc-brienne-08:53 — *"He's dead. Gendry shoved a spearpoint through the back of his neck."*

CONFIRMED EXISTING. No re-proposal.

**C2. The inn fight as downstream of the raid:**
`raid-on-saltpans --CAUSES--> encounter-at-crossroads-inn-affc`

No event node for this encounter exists (distinct from any ACOK encounter node). The affc-brienne-07 inn fight (Rorge's band vs. Brienne) is the direct consequence of Rorge escaping Saltpans and heading north.

**NEW NODE PROPOSAL:**
- slug: `inn-fight-affc`
- type: event.battle
- one-line: Rorge's surviving Saltpans band attacks the crossroads inn; Brienne kills Rorge, Biter mauls Brienne before being killed by Gendry; Lem's Brotherhood arrives and captures Brienne, Pod, and Hyle.

`raid-on-saltpans --CAUSES--> inn-fight-affc` | tier-1 | affc-brienne-07:131 | *"Sandor Clegane was last seen in Saltpans, the day of the raid. Afterward he rode west, along the Trident."* + affc-brienne-07:265 (*"beneath the dark hood of the lead rider Brienne glimpsed an iron snout and rows of steel teeth, snarling"*) | The Saltpans band's westward flight culminates in the inn attack; the Hound's-helm raider IS Rorge from Saltpans.

`brienne-tarth --KILLS--> rorge` | tier-1 | affc-brienne-07:293 | *"and Oathkeeper punched through cloth and mail and leather and more cloth, deep into his bowels and out his back, rasping as it scraped along his spine."* — NOTE: per baseline, brienne already KILLS rorge. CONFIRMED EXISTING. No re-proposal.

`brienne-tarth --VICTIM_IN--> inn-fight-affc` | tier-1 | affc-brienne-07:295 | *"Biter crashed into her, shrieking."*

`gendry --PARTICIPANT_IN--> inn-fight-affc` — NEEDS_VOCAB: PARTICIPATES_IN (correct form). `gendry --PARTICIPATES_IN--> inn-fight-affc` | tier-1 | affc-brienne-08:53 | *"He's dead. Gendry shoved a spearpoint through the back of his neck."*

`inn-fight-affc --CAUSES--> brienne-brought-before-lady-stoneheart` | tier-1 | affc-brienne-08:71 | *"'till you stand before m'lady.' . . . 'M'lady means for you to answer for your crimes.'"* | The Brotherhood's arrival at the inn aftermath leads directly to the capture that leads to the Stoneheart confrontation.

**C3. Gendry at the inn — wiring him to this location:**
`gendry --TRAVELS_TO--> inn-at-the-crossroads` | tier-1 | affc-brienne-07:119 | *"'I'm just a smith.'"* (Gendry is working the forge at the inn). Actually affc-brienne-07:133 gives the inn identification: *"If the gods are good, that smoke rising beyond the hanged men will be from its chimneys."* And Gendry's presence is confirmed at line 119.

Simpler: `gendry --LOCATED_AT--> inn-at-the-crossroads` | tier-2 | affc-brienne-07:119 | *"'I'm just a smith.'"* | Gendry is established at the inn as its working smith.

---

### D. Saltpans false-reputation engine — additional wiring

**D1. The helm transfer chain — the object that drives the false attribution:**
The Hound's helm travels: Sandor's grave (Elder Brother places it atop cairn) → Rorge picks it up → Rorge uses it in Saltpans raid → Lem takes it off Rorge's corpse → Lem wears it when Brotherhood captures Brienne.

These helm-transfer edges need an artifact node. Per baseline: "NO hound-helm node — candidate mint."

**NEW NODE PROPOSAL:**
- slug: `hound-helm`
- type: artifact
- one-line: Sandor Clegane's distinctive steel dog's-head helmet; placed by the Elder Brother on Sandor's grave; taken by Rorge who wears it during the Saltpans raid (causing the false attribution); later claimed by Lem Lemoncloak.

If minted:
`elder-brother-quiet-isle --BESTOWS_KNIGHTHOOD_ON--> hound-helm` — WRONG TYPE. No good edge type for "placed artifact on a grave." NEEDS_VOCAB. Skip the grave-placement edge.

`rorge --WIELDS--> hound-helm` — NEEDS_VOCAB: WIELDS normally applies to weapons. A helm is worn/used, not wielded. Closest fit is WIELDS (as equipment in conflict). Proposing with caveat.
`rorge --WIELDS--> hound-helm` | tier-1 | affc-brienne-07:265 | *"beneath the dark hood of the lead rider Brienne glimpsed an iron snout and rows of steel teeth, snarling"* | Rorge wears the Hound's helm, which causes the false attribution.

`hound-helm --CAUSES--> raid-on-saltpans-false-attribution` — NEEDS_VOCAB: No event node for "false attribution." Better to express as:

`sandor-clegane --REPUTED_AS--> rorge` — WRONG. REPUTED_AS doesn't mean "is falsely blamed for what Rorge did."

Best encoding without NEEDS_VOCAB: The alias "Mad Dog of Saltpans" on sandor-clegane's node captures the false reputation. The causal story is: Rorge wears the helm → helm is recognized → Sandor is blamed. This drives Brienne's SEEKS sandor-clegane (already in graph). No single edge type cleanly captures "helm causes misidentification." FLAG to orchestrator.

**D2. Randyll Tarly spreads the counter-rumor:**
`randyll-tarly --INFORMS--> brienne-tarth` | tier-1 | affc-brienne-05:127 | *"Sandor Clegane was last seen in Saltpans, the day of the raid. Afterward he rode west, along the Trident."* | Tarly's men (via Ser Hyle/cousin Alyn) pass the Saltpans-Hound attribution to Brienne, directly driving her SEEKS sandor-clegane.

(Note: Technically this is Hyle relaying Alyn's report, but it flows from Tarly's intelligence network. INFORMS from randyll-tarly to brienne-tarth is the functional truth.)

---

### E. Septon Meribald and the Elder Brother as information brokers

**E1. Elder Brother REVEALS the truth about Sandor and the helm:**
`elder-brother-quiet-isle --REVEALS_TO--> brienne-tarth` (re: Sandor's death and helm theft) | tier-1 | affc-brienne-06:185 | *"The man who raped and killed at Saltpans was not Sandor Clegane, though he may be as dangerous. The riverlands are full of such scavengers."* | This revelation redirects Brienne's hunt from Sandor to Rorge, enabling the inn fight.

`elder-brother-quiet-isle --REVEALS_TO--> brienne-tarth` (re: Arya, not Sansa, with Sandor) | tier-1 | affc-brienne-06:169 | *"You are chasing the wrong wolf, my lady. Eddard Stark had two daughters. It was the other one that Sandor Clegane made off with, the younger one."* | This revelation reorients Brienne's entire quest.

(Note: these may be two separate REVEALS_TO edges or one, depending on graph granularity. Flagging both as high-value since they redirect the arc's whole trajectory.)

**E2. Elder Brother HEALS Brienne:**
`elder-brother-quiet-isle --HEALS--> brienne-tarth` — per baseline this ALREADY EXISTS. No re-proposal.

---

### F. Hyle Hunt wiring

**F1.** `hyle-hunt --COMPANION_OF--> brienne-tarth` | tier-1 | affc-brienne-05:173 | *"They left the next morning, as the sun was coming up."* | Hyle Hunt joins Brienne's party from Maidenpool onward through the arc. Already partially in baseline? Check baseline: "COMPANION_OF pod/hyle/jaime" — hyle already exists.

CONFIRMED EXISTING per baseline. No re-proposal.

**F2.** `hyle-hunt --VICTIM_IN--> brienne-brought-before-lady-stoneheart` — Per baseline, hyle-hunt is VICTIM_IN. CONFIRMED EXISTING.

---

## SUMMARY OF NEW NODES PROPOSED

| Slug | Type | Justification |
|------|------|---------------|
| `brotherhood-hanging-campaign` | event.incident | The Brotherhood's Stoneheart-driven mass-hanging operation (salt in mouths, reference to Saltpans); no node exists; baseline identifies it as a gap |
| `inn-fight-affc` | event.battle | Rorge's band vs. Brienne at crossroads inn (affc-brienne-07/08); distinct from any ACOS-era inn fight node |
| `merrett-frey-hanging` | event.death | ASOS epilogue; Merrett + Petyr Pimple hanged by Brotherhood under Stoneheart's command at Oldstones |
| `hound-helm` | artifact | Sandor's dog's-head helm; the false-attribution engine; travels Sandor→Elder Brother→Rorge→Lem |
| `petyr-pimple-frey` | character | Merrett's great half-nephew, first hanged at Oldstones (asos-epilogue:99); minor but needed for merrett-frey-hanging VICTIM_IN edges |

---

## FORWARD-DANGLING FLAGS (do not mint)

1. **`brienne-brought-before-lady-stoneheart` outgoing edges** — The downstream (Brienne's screamed word; what she chooses; Jaime encounter) is ADWD/TWOW material. AFFC ends on the cliffhanger. No in-AFFC event node should be minted for the downstream of this choice.

2. **Lem Lemoncloak wearing the Hound's helm** — Lem takes the helm off Rorge's corpse (wiki node body line 59: *"Lem claims the hound helm for himself"*). This happens after the inn fight but Lem is already in the graph (baseline: "lem-standfast"). Edge `lem-standfast --WIELDS--> hound-helm` is valid if hound-helm is minted. FLAG for orchestrator.

---

## HARVEST

Collected while reading the chapters. These are POINTERS only — not edges; a later harvest pass attaches them.

### Food / Hospitality / Drink

- affc-brienne-01:53 — trout shared by hedge knights at campfire (HOSPITALITY: Creighton/Illifer offer trout to Brienne); affc-brienne-01:263 — goat on spit at Old Stone Bridge inn; goat's milk for Brienne
- affc-brienne-01:107 — roast squirrel, acorn paste, and pickles (hedge knight breakfast); affc-brienne-02:116 — hot crab stew at Seven Swords, Duskendale (dwarf gives Brienne his seat); bread, wine
- affc-brienne-02:178 — hardbread, cheese, flour from cook (Brienne's road supplies)
- affc-brienne-03:175 — Meribald's donkey load: salt cod, oranges (weakness), barley bread, beans, carrots, turnips, flour, three wheels of yellow cheese — explicit charity-food for the poor riverlands; affc-brienne-05:107 — greasy sausages + fried bread + flagon of boiled water + watered wine (Stinking Goose)
- affc-brienne-06:141 — Quiet Isle feast: crusty bread, butter, honey, fish stew (crabs, mussels, three kinds of fish), mead and cider; noted as "one of the strangest meals" Brienne ever ate
- affc-brienne-07:95 — horse meat at the crossroads inn (all Willow/Jeyne have to offer)
- affc-brienne-07:161 — porridge + salt cod + orange slices + two wheels of cheese: Meribald feeds the orphan children at the inn; oranges noted as a LUXURY and his "last till spring"
- affc-brienne-08:131 — underground cave: bread, cheese, cold greasy stew, soured milk gone, honey gone; "food grows scant" (Brotherhood's resource poverty)
- asos-epilogue:51 — Merrett's wine "thick and sweet, so dark it was almost black" (nervous drinking); asos-epilogue:11 — *"Between rains, floods, fire, and war, they had lost two harvests and a good part of a third. An early winter would mean famine all across the riverlands."* (food-scarcity/famine signal — BIG HARVEST FLAG)

### Broken Men / Societal Devastation

- affc-brienne-05:293 — Septon Meribald's broken-men sermon (long, load-bearing; "the broken man lives from day to day, from meal to meal, more beast than man") — FORESHADOWING/THEMATIC flag; connects to Sandor's own arc
- affc-brienne-07:35 — hanging corpses with heraldic badges: axes (Byrch/Cerwyn), arrows (Norridge/Sarsfield), salmon (Mooton), pine trees (Mollen), oak leaves (Oakheart), beetles (Bettley), bantams (Swyft), boar's heads (Vikary), tridents (Condon/Manderly) — visual catalog of broken men from a dozen armies

### Physical Descriptions

- affc-brienne-06:61-66 — Stranger/Driftwood, the great black stallion at the Quiet Isle (kicks, bites ear off brother; lame gravedigger tends him) — MAJOR NOTE: the gravedigger at line 79 who is "bigger than Brienne" and "lame" and has a dog sniff him and he scratches its ear — this is the SANDOR-IS-ALIVE signal (AFFC). Verbatim quote: affc-brienne-06:79 — *"a brother bigger than Brienne was struggling to dig a grave. From the way he moved, it was plain to see that he was lame. As he flung a spadeful of the stony soil over one shoulder, some chanced to spatter against their feet."* And: *"When Dog went to sniff him he dropped his spade and scratched his ear."* — FORESHADOWING flag: this is almost certainly Sandor in disguise; the Elder Brother's account of "burying" Sandor is notably oblique.

### Notable Quotes

- affc-brienne-06:185 — Elder Brother: *"The man who raped and killed at Saltpans was not Sandor Clegane, though he may be as dangerous. The riverlands are full of such scavengers. I will not call them wolves. Wolves are nobler than that . . . and so are dogs, I think."* — LOAD-BEARING quote; should attach to both elder-brother-quiet-isle node and sandor-clegane node.
- asos-epilogue:109 — *"We had a rope," said yellow cloak. "That's right enough."* — encapsulates Brotherhood under Stoneheart's ethos.
- affc-brienne-08:105 — *"Guest right don't mean so much as it used to . . . Not since m'lady come back from the wedding."* (Long Jeyne Heddle) — VIOLATES_GUEST_RIGHT edge candidate for Stoneheart-era Brotherhood, if such an edge is ever warranted.

### Foreshadowing

- affc-brienne-06:79 — Gravedigger scene (Sandor-is-alive signal; see above)
- affc-brienne-07:259 — Meribald's great wolf pack on the Trident: *"a stalking shadow grim and grey and huge . . . she has been known to bring aurochs down all by herself"* — almost certainly Nymeria's pack; major FORESHADOWING flag for wolf-pack/Arya arc.
- affc-brienne-01:283 — Oathkeeper described: *"Black and red the ripples ran, deep within the steel. Valyrian steel, spell-forged."* — evidence_quote for oathkeeper artifact node.

---

## 2-LINE SUMMARY

Proposed 12 new/amended edges wiring the islanded `raid-on-saltpans` (Rorge + Biter + brave-companions AGENT_IN; located-at saltpans; causal chain to the inn fight and the Brotherhood's hanging campaign), 4 new edges from `catelyn-rises-as-lady-stoneheart` downstream (hanging campaign CAUSES; Merrett-Frey hanging CAUSES/COMMANDS_IN), and 5 new event/artifact node candidates (brotherhood-hanging-campaign, inn-fight-affc, merrett-frey-hanging, hound-helm, petyr-pimple-frey). Flagged `brienne-brought-before-lady-stoneheart` outgoing edges as forward-dangling into ADWD (cliffhanger; nothing mintable in AFFC) and the gravedigger scene as a high-value Sandor-is-alive foreshadowing signal not yet in the graph.
