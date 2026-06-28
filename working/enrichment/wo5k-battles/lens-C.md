# Lens C — Descriptive / Quote / Object-Depth — A2.5 WO5K-battles proposal (S163, PASS 1)

**Chapters read:** agot-catelyn-08, agot-catelyn-09, agot-catelyn-10, agot-catelyn-11
**Lens focus:** Marquee verbatim quotes, vivid description, object/place edges, and a HARVEST-heavy pass.

---

## PRE-WORK: Live-node clarification and suspicious-edge flags

**Node slug correction (critical):** The baseline calls the target node `battle-of-the-whispering-wood`.
The LIVE node in `graph/nodes/events/` is **`battle-in-the-whispering-wood`** (wiki slug, confirmed).
A `_conflicts/battle-of-the-whispering-wood.node.md` exists but is excluded. All proposals below use
`battle-in-the-whispering-wood` as the target. The synthesis should confirm before minting.

**Suspicious edge flags (from baseline):**
- `roose-bolton CAPTURES jaime-lannister` — NOT found in edges.jsonl. May be a wiki node prose claim only,
  not a live edge. If it appears in the wiki node body for Roose, it is wrong: the text shows Roose commanded
  the Green Fork host (cat-08:167, cat-09:257), never the Whispering Wood. Flag for fresh-verify; do not
  re-mint. The live edge is `jaime-lannister PRISONER_OF robb-stark` (confirmed in edges.jsonl from ACOK pass).
- `catelyn-stark CAPTURES jaime-lannister` — exists (ACOK pass, acok-catelyn-07). Technically not wrong
  (she receives him in custody at Riverrun) but is loose — Robb's host captured him; Catelyn ordered him
  put in irons (cat-10:117). Flag for review but do NOT re-propose a clean CAPTURES dyad — the
  `jaime VICTIM_IN battle-in-the-whispering-wood` role edge below is the correct structural assertion.

**Edge-web state (confirmed by edges.jsonl scan):**
- `battle-in-the-whispering-wood`: 5 edges total — 2× SUB_BEAT_OF, PART_OF war-of-five-kings, and
  2× PRECEDES (tier-3 chronology-chain). **Zero participant roles. Zero causal edges.** The node is a shell.
- Causal spine: COMPLETELY EMPTY between the four battle hubs. No ENABLES or CAUSES anywhere in the cluster.
- `hoster-tully WITNESS_IN battle-of-the-camps` — ALREADY EXISTS (historical-anchor-w1); do not re-propose.

---

## Proposed NEW nodes

None. The `battle-in-the-whispering-wood` live node already exists and has sufficient wiki prose. This lens
adds quotes and edges TO it, but does not propose a new node. (The baseline's implied new-node build is
already satisfied by the wiki-sourced node; the synthesis should decide if a node rewrite is needed.)

---

## Proposed NEW edges

### A. The causal spine — HIGHEST PRIORITY (the gap the whole dip targets)

**A1.**
`battle-on-the-green-fork` **ENABLES** `battle-in-the-whispering-wood` | Tier-2 | —
> "He'll stay close to the Trident, they believe, taking the castles of the river lords one by one, until
> Riverrun stands alone. We need to march south to meet him." — and Robb's plan at cat-08:151: split the host,
> foot down the kingsroad to engage Tywin, horse across the Green Fork to relieve Riverrun.
Chapter:line anchor: `agot-catelyn-08:151`
> "the foot can continue down the kingsroad, while our horsemen cross the Green Fork at the Twins"
Rationale: The Green Fork engagement was Robb's deliberate diversion — foot under Roose Bolton "to confront
the huge Lannister army coming north under Lord Tywin" (cat-09:257), freeing the horse to reach Jaime's
position undetected. Robb could not have sprung the Whispering Wood trap while Tywin was free to reinforce
Jaime. This is a textbook ENABLES: the diversion made the ambush POSSIBLE; Robb's cavalry free choice
actually produced it. NOT CAUSES (no forced consequence) — honor the ENABLES contract.

**A2.**
`battle-in-the-whispering-wood` **ENABLES** `battle-of-the-camps` | Tier-1 | —
> "Having had their outriders and scouts eliminated, the Lannister force is unaware of their commander's
> defeat or of Robb's army's approach" (wiki node prose, battle-of-the-camps.node.md; also cat-10 confirms
> the outrider elimination).
Book anchor: `agot-catelyn-10:31`
> "No bird has reached him, my archers have seen to that. We've seen a few of his outriders, but those that
> saw us did not live to tell of it."
Rationale: The wiki node for battle-of-the-camps states explicitly that the Lannister siege-army was
"unaware of their commander's defeat" — Jaime's capture at Whispering Wood is the PRECONDITION that left
the three camps leaderless and blind. The wiki's own Narrative Arc says Jaime was "ambushed and captured…
the Lannister force is unaware" — linking the two events causally. ENABLES (not CAUSES): Robb still had to
choose to attack the camps; the Whispering Wood just made that attack viable. Tier-1 because the text
explicitly states the causal mechanism.

**A3.**
`battle-of-the-camps` **ENABLES** `robb-proclaimed-king-in-the-north` | Tier-2 | —
> "Word of the victory at Riverrun had spread to the fugitive lords of the Trident, drawing them back."
Chapter:line: `agot-catelyn-11:143`
> "Word of the victory at Riverrun had spread to the fugitive lords of the Trident, drawing them back."
Rationale: The war council at Riverrun that proclaims Robb king is convened BECAUSE the Camps victory
assembled the riverland lords (Blackwood, Bracken, Mallister, Vance, Piper, Darry) who had been fugitives
— they return specifically on the news of the relief. `execution-of-eddard-stark CAUSES` the grievance
(already exists, Tier-2); `battle-of-the-camps ENABLES` is the military PRECONDITION that gathered the
assembly. These are additive, not duplicate. Tier-2: mediated by a free lordly decision.

### B. Participant roles on battle-in-the-whispering-wood (the shell node)

All of these are confirmed MISSING from edges.jsonl (only SUB_BEAT_OF / PART_OF / PRECEDES exist).

**B1.**
`robb-stark` **COMMANDS_IN** `battle-in-the-whispering-wood` | Tier-1 | —
> "Winterfell!" she heard Robb shout as the arrows sighed again. He moved away from her at a trot,
> leading his men downhill.
Chapter:line: `agot-catelyn-10:85`
Rationale: Robb personally led the cavalry downhill at the signal; he designed and commanded the ambush.

**B2.**
`robb-stark` **AGENT_IN** `battle-in-the-whispering-wood` | Tier-1 | —
> "I must ride down the line, Mother," he told her. "Father says you should let the men see you before a battle."
Chapter:line: `agot-catelyn-10:47`
[BORDERLINE — this quote establishes his role but not the act itself. Better anchor: his post-battle return
is described at cat-10:97: "Robb came back to her on a different horse… his mailed glove and the sleeve of
his surcoat were black with blood." Use cat-10:97 as the strongest anchor for AGENT_IN.]
Chapter:line anchor: `agot-catelyn-10:97`
> "Robb came back to her on a different horse, riding a piebald gelding in the place of the grey stallion
> he had taken down into the valley."

**B3.**
`grey-wind` **FIGHTS_IN** `battle-in-the-whispering-wood` | Tier-1 | —
> "she heard his direwolf, snarling and growling, heard the snap of those long teeth, the tearing of flesh,
> shrieks of fear and pain from man and horse alike."
Chapter:line: `agot-catelyn-10:93`
Rationale: Catelyn explicitly HEARS Grey Wind attacking from her ridge position. The follow-up in cat-11
provides a complementary description (Theon's account of the wolf tearing a man's arm from his shoulder).
This is book-direct, Tier-1.

**B4.**
`jaime-lannister` **VICTIM_IN** `battle-in-the-whispering-wood` | Tier-1 | —
> "A mob of men followed him up the slope, dirty and dented and grinning, with Theon and the Greatjon at
> their head. Between them they dragged Ser Jaime Lannister. They threw him down in front of her horse."
Chapter:line: `agot-catelyn-10:101`
Rationale: Jaime is the primary victim of the night trap — captured, wounded, brought in chains.

**B5.**
`brynden-tully` **COMMANDS_IN** `battle-in-the-whispering-wood` | Tier-1 | —
> "He had wagered their lives and their best hope of victory on the truth of what he said."
Chapter:line: `agot-catelyn-10:25`
[BORDERLINE — this is Catelyn's thought about Brynden's intelligence report on Jaime. Better anchor:]
> "Raid him here… A few hundred men, no more. Tully banners. When he comes after you, we will be waiting"
Chapter:line: `agot-catelyn-10:71`
Rationale: Robb's plan (outlined by Brynden's scouting) sent Brynden with the lure force of Tully-banner
raiders. The Blackfish designed and led the operational screen. COMMANDS_IN is correct for the van/screen role.

**B6.**
`jon-umber` **FIGHTS_IN** `battle-in-the-whispering-wood` | Tier-1 | —
> "HAAroooooooooooooooooooooooo came the answer from the far ridge as the Greatjon winded his own horn."
Chapter:line: `agot-catelyn-10:83`
Rationale: The Greatjon held the far ridge and led his riders down into the valley; his horn-signal and
charge are explicitly described.

**B7.**
`maege-mormont` **AGENT_IN** `battle-in-the-whispering-wood` | Tier-1 | —
> "Here was the call of Maege Mormont's warhorn, a long low blast that rolled down the valley from the east,
> to tell them that the last of Jaime's riders had entered the trap."
Chapter:line: `agot-catelyn-10:77`
Rationale: Maege Mormont gave the signal horn that sprang the trap — a load-bearing command act, not just
presence. AGENT_IN more appropriate than FIGHTS_IN (her signal is the trigger act; text does not show her
in direct combat in this chapter).

**B8.**
`rickard-karstark` **FIGHTS_IN** `battle-in-the-whispering-wood` | Tier-1 | —
> "North, where the valley narrowed and bent like a cocked elbow, Lord Karstark's warhorns added their own
> deep, mournful voices to the dark chorus."
Chapter:line: `agot-catelyn-10:83`
Rationale: Karstark held the northern choke-point; his warhorns and forces closed the valley shut. The
chapter also confirms his sons Torrhen and Eddard died in this battle (cat-10:129: "He killed them… Lord
Karstark's sons").

**B9.**
`daryn-hornwood` **VICTIM_IN** `battle-in-the-whispering-wood` | Tier-1 | —
> "He mislaid his sword in Eddard Karstark's neck, after he took Torrhen's hand off and split Daryn
> Hornwood's skull open"
Chapter:line: `agot-catelyn-10:133`
Rationale: Daryn Hornwood was killed by Jaime in the battle. DIED_AT whispering-wood already exists
(infobox-merge). VICTIM_IN on the event hub is the role edge — not a duplicate.

**B10.**
`battle-in-the-whispering-wood` **LOCATED_AT** `whispering-wood` | Tier-1 | —
> "Here was a hush in the night, moonlight and shadows, a thick carpet of dead leaves underfoot, densely
> wooded ridges sloping gently down to the streambed"
Chapter:line: `agot-catelyn-10:73`
Rationale: The wiki prose in the node body identifies the location but no live LOCATED_AT edge exists.

### C. Siege-of-Riverrun seam

**C1.**
`battle-in-the-whispering-wood` **ENABLES** `siege-of-riverrun` — **[BORDERLINE / DO NOT PROPOSE]**
The Whispering Wood (Jaime captured) + Camps (siege broken) together ended the AGOT-era siege. But this is
a two-step relationship (needs the Camps as intermediary) and the siege-of-riverrun node has S159 work on
its AFFC resolution. Log for synthesis to decide: a cleaner wire is
`battle-of-the-camps ENABLES siege-of-riverrun[end]` (the camps battle physically broke the siege).
Dropping this; too speculative without clear single-step causation.

### D. The Frey-crossing seam (cat-09 material)

**D1.** [BORDERLINE]
`catelyn-stark` **NEGOTIATES_WITH** `walder-frey` | Tier-1 | —
> "You want to cross," he said. "That's blunt. Why should I let you?"
Chapter:line: `agot-catelyn-09:179`
The negotiation is an explicit scene. However, this is almost certainly in the SATURATED dyad web (Catelyn
119 core-out edges, Walder 66). Flagging as likely already-exists or very low priority. The DEDUP WILL
likely kill this. DO NOT propose as a primary recommendation.

---

## Dropped / considered-but-rejected

- **`catelyn-stark WITNESS_IN battle-in-the-whispering-wood`** — DROPPED. LENS-SHARED.md is explicit:
  "Catelyn waits OUTSIDE the wood and only HEARS it, so she is NOT a witness to the battle itself." She
  is on the ridge with thirty guards; she sees the lance-tips on the far ridge but not the fighting. The
  text is clear: "she could not claim she had seen the battle." WITNESS_IN requires the character actually
  SEES the event. Dropped.

- **`hoster-tully WITNESS_IN battle-of-the-camps`** — ALREADY EXISTS (historical-anchor-w1 run, confirmed
  in edges.jsonl). Do not re-propose.

- **`robb-stark DEFEATS jaime-lannister`** — The text is: "They threw him down in front of her horse"
  (cat-10:101). A DEFEATS dyad is plausible, but with `jaime-lannister PRISONER_OF robb-stark` already
  live (ACOK pass) and `jaime VICTIM_IN battle-in-the-whispering-wood` proposed above, the role-edge on
  the hub is the cleaner representation. The bare dyad would be redundant. Dropped.

- **`jason-mallister FIGHTS_IN battle-in-the-whispering-wood`** — Mentioned in cat-10:45 ("Lord Jason
  Mallister had brought his power out from Seagard to join them") and his trumpets blow at cat-10:83
  ("the trumpets of the Mallisters and Freys blew vengeance"). However: (a) the Mallister forces may have
  held the east with Maege Mormont rather than riding in the main cavalry charge; (b) the Frey trumpets
  also blow (Ser Stevron held the west per the wiki narrative). Given ambiguity and DEDUP pressure,
  dropped. Note for lens A/B (whodunit/causal) if they found clearer text.

- **`galbart-glover FIGHTS_IN / smalljon-umber FIGHTS_IN / dacey-mormont FIGHTS_IN`** — All mentioned in
  Robb's guard (cat-10:53) or the general host. But none receive explicit battle-action lines — Catelyn
  can't see the battle. Only Robb, Greatjon (horn), Maege Mormont (horn), Karstark (horn), Grey Wind
  (heard), and Jaime (captured) are directly evidenced. Dropped as show-only/implied-presence.

- **`robb-stark VOWS_TO walder-frey`** (the betrothal) — Exists in the heavily-saturated Robb/Frey web.
  The marriage pact is the trigger for the B1 Red-Wedding-upstream arc, already built. Do not re-propose.

- **Frey-crossing as a causal node** — Robb's crossing of the Twins is a load-bearing prerequisite for
  reaching the Whispering Wood. However, the crossing is a negotiated passage, not a battle event —
  and no event node for `crossing-the-twins` appears to exist. Note for PASS 2 (Frey arc) if wanted;
  out of PASS-1 scope.

- **Theon Greyjoy FIGHTS_IN battle-in-the-whispering-wood** — Theon is listed in Robb's battle guard
  (cat-10:53: "no less than five of Walder Frey's vast brood, along with older men like Ser Wendel
  Manderly and Robin Flint. One of his companions was even a woman: Dacey Mormont"). The wiki narrative
  (battle-in-the-whispering-wood node) states Theon "kills men in the battle." However, cat-10 itself
  has Theon leading Jaime's captors up the slope (cat-10:101: "Theon and the Greatjon at their head")
  and enthusiastically urging Jaime's execution (cat-10:111). He is clearly present and fighting.
  **[BORDERLINE — upgrade to FIGHTS_IN if the whodunit lens confirms the wiki claim is Tier-1
  book-supported. This lens lacks a single-line verbatim fight-act quote.]**

- **Oxcross / Westerlands raids** — PASS 2. Not touched.

- **The Fords / Duskendale** — PASS 3. Not touched.

- **Suspicion about Roose Bolton deliberately losing the Green Fork** — PASS 3 (Duskendale-scope per
  baseline). Do NOT mint SUSPECTED_OF. Noted for later.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|-------------|------|
| quote | AGOT | agot-catelyn-10:11 | "The woods were full of whispers." — the chapter's opening line; the atmosphere of the night wait. Attach to `battle-in-the-whispering-wood ## Quotes` |
| quote | AGOT | agot-catelyn-10:73 | "Here was a hush in the night, moonlight and shadows, a thick carpet of dead leaves underfoot, densely wooded ridges sloping gently down to the streambed, the underbrush thinning as the ground fell away." — the marquee setting description for the Whispering Wood ambush |
| quote | AGOT | agot-catelyn-10:77 | "Here was the call of Maege Mormont's warhorn, a long low blast that rolled down the valley from the east, to tell them that the last of Jaime's riders had entered the trap." — the trigger moment |
| quote | AGOT | agot-catelyn-10:79 | "And Grey Wind threw back his head and howled." — the direwolf howl at the trap-spring. High-value for `grey-wind` node and `battle-in-the-whispering-wood ## Quotes` |
| quote | AGOT | agot-catelyn-10:81 | "The sound seemed to go right through Catelyn Stark, and she found herself shivering. It was a terrible sound, a frightening sound, yet there was music in it too. For a second she felt something like pity for the Lannisters below. So this is what death sounds like, she thought." — Catelyn's terror-pity at Grey Wind's howl |
| quote | AGOT | agot-catelyn-10:83 | "HAAroooooooooooooooooooooooo came the answer from the far ridge as the Greatjon winded his own horn. To east and west, the trumpets of the Mallisters and Freys blew vengeance." — the multi-horn cacophony at the trap-spring |
| quote | AGOT | agot-catelyn-10:89 | "she saw the Greatjon's riders emerge from the darkness beneath the trees. They were in a long line, an endless line, and as they burst from the wood there was an instant, the smallest part of a heartbeat, when all Catelyn saw was the moonlight on the points of their lances, as if a thousand willowisps were coming down the ridge, wreathed in silver flame." — the marquee visual of the cavalry charge |
| quote | AGOT | agot-catelyn-10:93 | "she heard his direwolf, snarling and growling, heard the snap of those long teeth, the tearing of flesh, shrieks of fear and pain from man and horse alike. Was there only one wolf? It was hard to be certain." — Grey Wind at the kill; vivid audio description; for `grey-wind ## Quotes` |
| quote | AGOT | agot-catelyn-10:95 | "Little by little, the sounds dwindled and died, until at last there was only the wolf. As a red dawn broke in the east, Grey Wind began to howl again." — the aftermath; the wolf howling at dawn |
| quote | AGOT | agot-catelyn-10:65 | "Even at a distance, Ser Jaime Lannister was unmistakable. The moonlight had silvered his armor and the gold of his hair, and turned his crimson cloak to black. He was not wearing a helm." — Jaime first sighted by moonlight; vivid physical description; for `jaime-lannister ## Quotes` |
| quote | AGOT | agot-catelyn-10:103 | "Blood ran down one cheek from a gash across his scalp, but the pale light of dawn had put the glint of gold back in his hair." — Jaime after capture; description of his wound |
| quote | AGOT | agot-catelyn-10:103 | "Lady Stark," he said from his knees. "I would offer you my sword, but I seem to have mislaid it." — Jaime's defiant quip at capture; for `jaime-lannister ## Quotes` |
| quote | AGOT | agot-catelyn-10:105 | "It is not your sword I want, ser. Give me my father and my brother Edmure. Give me my daughters. Give me my lord husband." — Catelyn's response to Jaime; high emotional load |
| quote | AGOT | agot-catelyn-10:113 | "He's more use alive than dead. And my lord father never condoned the murder of prisoners after a battle." — Robb refusing Theon's call to kill Jaime; for `robb-stark ## Quotes` |
| quote | AGOT | agot-catelyn-10:117 | "Take him away and put him in irons" — Catelyn's command; the clean quote for Jaime's captivity order |
| quote | AGOT | agot-catelyn-10:131 | "No one can fault Lannister on his courage. When he saw that he was lost, he rallied his retainers and fought his way up the valley, hoping to reach Lord Robb and cut him down. And almost did." — Galbart Glover on Jaime's final charge; for `jaime-lannister ## Quotes` |
| quote | AGOT | agot-catelyn-11:61 | "Riverrun is free again, Father." — Catelyn to Hoster; the marquee "Riverrun is free" line. Note: in the text Catelyn says this, not a herald; attach to `battle-of-the-camps ## Quotes` and/or `siege-of-riverrun ## Quotes` |
| quote | AGOT | agot-catelyn-11:63 | "I saw. Last night, when it began, I told them … had to see. They carried me to the gatehouse … watched from the battlements. Ah, that was beautiful … the torches came in a wave, I could hear the cries floating across the river … sweet cries … when that siege tower went up, gods … would have died then, and glad, if only I could have seen you children first. Was it your boy who did it? Was it your Robb?" — Hoster Tully watching the Battle of the Camps from the battlements. NOTE: this verbatim quote IS ALREADY ATTACHED as the `hoster-tully WITNESS_IN battle-of-the-camps` evidence_quote in edges.jsonl (historical-anchor-w1). Do not re-attach; logged for awareness only. |
| quote | AGOT | agot-catelyn-11:117 | "The Lannisters must have thought the Others themselves were on them when that wolf of Robb's got in among them. I saw him tear one man's arm from his shoulder, and their horses went mad at the scent of him. I couldn't tell you how many men were thrown—" — Theon's account of Grey Wind at the Whispering Wood, told to Riverrun's garrison. NOTE: this quote is already in `battle-in-the-whispering-wood ## Quotes` (wiki node). Logged for awareness. |
| quote | AGOT | agot-catelyn-11:209-211 | The full Greatjon "King in the North" speech including "There sits the only king I mean to bow my knee to, m'lords" and "And he knelt, and laid his sword at her son's feet." NOTE: already on `robb-proclaimed-king-in-the-north` node with chapter:line citations. Logged for awareness. |
| quote | AGOT | agot-catelyn-11:135 | "We have won a battle, not a war." — Catelyn to Robb after Whispering Wood; for `catelyn-stark ## Quotes` or `battle-in-the-whispering-wood ## Quotes` |
| quote | AGOT | agot-catelyn-11:181 | "a hundred Whispering Woods will not change that. Ned is gone, and Daryn Hornwood, and Lord Karstark's valiant sons, and many other good men besides" — Catelyn's peace speech; names the battle explicitly; for `catelyn-stark ## Quotes` |
| description | AGOT | agot-catelyn-10:13 | Night-march atmosphere: "warhorses whickered softly and pawed at the moist, leafy ground, while men made nervous jests in hushed voices. Now and again, she heard the chink of spears, the faint metallic slither of chain mail" |
| description | AGOT | agot-catelyn-10:27 | Robb among his men before the battle: "Catelyn watched her son as he moved among the men, touching one on the shoulder, sharing a jest with another, helping a third to gentle an anxious horse" |
| description | AGOT | agot-catelyn-10:47 | Robb's armoring: "Olyvar Frey held his horse for him… He strapped Robb's shield in place and handed up his helm. When he lowered it over the face she loved so well, a tall young knight sat on his grey stallion where her son had been." — vivid arming scene |
| description | AGOT | agot-catelyn-10:53 | Robb's battle guard composition: Torrhen and Eddard Karstark, Patrek Mallister, Smalljon Umber, Daryn Hornwood, Theon Greyjoy, five Freys, Ser Wendel Manderly, Robin Flint, Dacey Mormont — full list of names for future FIGHTS_IN proposals |
| description | AGOT | agot-catelyn-10:67 | The three Lannister siege camps disposition: "Twelve thousand foot, scattered around the castle in three separate camps, with the rivers between" — load-bearing for the siege-of-riverrun / battle-of-the-camps topology |
| description | AGOT | agot-catelyn-10:75 | Robb lifts his sword before charging: "Here was her son on his stallion, glancing back at her one last time and lifting his sword in salute." — physical image of the charge |
| description | AGOT | agot-catelyn-10:85 | The hidden archers: "the bowmen Robb had hidden in the branches of the trees let fly their arrows and the night erupted with the screams of men and horses" — key tactical detail |
| description | AGOT | agot-catelyn-10:97 | Robb's post-battle shield: "The wolf's head on his shield was slashed half to pieces, raw wood showing where deep gouges had been hacked in the oak" — physical description |
| description | AGOT | agot-catelyn-11:19 | Tytos Blackwood at Riverrun: "a hard pike of a man with close-cropped salt-and-pepper whiskers and a hook nose. His bright yellow armor was inlaid with jet in elaborate vine-and-leaf patterns, and a cloak sewn from raven feathers draped his thin shoulders." — vivid physical description; for `tytos-blackwood` node |
| description | AGOT | agot-catelyn-11:47 | Hoster Tully's physical decline: "Now he seemed shrunken, the muscle and meat melted off his bones. Even his face sagged … his hair and beard had been brown, well streaked with grey. Now they had gone white as snow." — for `hoster-tully` node physical description |
| food/medical | AGOT | agot-catelyn-11:55 | Hoster's medical treatment: "Maester Vyman makes me dreamwine, milk of the poppy … I sleep a lot" — dreamwine and milk-of-the-poppy given to dying Hoster Tully. Harvest for medical/food pass |
| food | AGOT | agot-catelyn-08:25 | Camp provisions: "wagons heavy-laden with hardbread and salt beef" — the Moat Cailin camp provisioning; for food pass |
| food | AGOT | agot-catelyn-08:63 | Moat Cailin war council: "There was ale and cheese on the table" — Catelyn and Robb share ale and cheese after the lords depart |
| food | AGOT | agot-catelyn-09:37 | After crossing: Theon's quip about the downed ravens: "A few more blackbirds, and we should have enough to bake a pie. I'll save you their feathers for a hat." — Theon's dark humor about shot-down ravens; technically not food but worth harvesting |
| food | AGOT | agot-catelyn-11:117 | Theon enjoying "a horn of ale" while recounting the Whispering Wood to the garrison of Riverrun — victory-drink scene |
| hospitality | AGOT | agot-catelyn-09:137 | Walder Frey hosts Catelyn in the great hall of the east castle, "surrounded by twenty living sons … thirty-six grandsons, nineteen great-grandsons, and numerous daughters, granddaughters, bastards, and grandbastards" — the great Frey hall scene; hospitality/guest-right context |
| foreshadowing | AGOT | agot-catelyn-11:205 | "He had pledged himself to marry a daughter of Walder Frey, but she saw his true bride plain before her now: the sword he had laid on the table." — Catelyn's foreboding; already on `robb-proclaimed-king-in-the-north` node. Note here for awareness; attach to `robb-stark ## Quotes` if not already present. |
| place | AGOT | agot-catelyn-08:27-29 | Moat Cailin physical description: three towers (Gatehouse, Drunkard's, Children's), the bog, the ghostskin-draped tree. Rich descriptive passage for `moat-cailin` node. |
| place | AGOT | agot-catelyn-09:97-99 | The Twins physical description: "a massive arch of smooth grey rock, wide enough for two wagons to pass abreast; the Water Tower rose from the center of the span… two squat, ugly, formidable castles, identical in every respect" — for `the-twins` node. |
| place | AGOT | agot-catelyn-11:15 | Riverrun arrival: the Wheel Tower, its "splash and rumble of the great waterwheel," soldiers and servants shouting from the sandstone walls — for `riverrun` node atmosphere. |
| place | AGOT | agot-catelyn-11:45 | Hoster's triangular solar with its stone balcony "that jutted out to the east like the prow of some great sandstone ship" and the view of both rivers — for `riverrun` node. |
| place | AGOT | agot-catelyn-11:127 | The godswood of Riverrun: "tall redwoods and great old elms" and "a slender weirwood with a face more sad than fierce" — for `godswood-of-riverrun` node. |
| object | AGOT | agot-catelyn-09:253 | The Twins crossing at evenfall: "as a horned moon floated upon the river. The double column wound its way through the gate of the eastern twin like a great steel snake" — vivid image of the army crossing |
