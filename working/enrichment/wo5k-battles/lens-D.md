# Lens D — Causal Wiring — A2.5 WO5K-battles proposal (S163, PASS 1)

> **Assigned chapters:** agot-catelyn-08 · agot-catelyn-09 · agot-catelyn-10 · agot-catelyn-11
> **Focus:** wire the relief-rise causal spine between existing (and one new) event hubs

---

## Proposed NEW nodes

### `battle-of-the-whispering-wood`
- **slug:** `battle-of-the-whispering-wood`
- **name:** Battle of the Whispering Wood
- **type:** `event.battle`
- **body:** A night ambush in the Whispering Wood near Riverrun in which Robb Stark's cavalry (~6,000 horse, drawn from those who crossed the Twins) surrounded and destroyed three-quarters of the Lannister horse besieging Riverrun, taking Ser Jaime Lannister captive. The Blackfish's screened march and suppressed outriders left Jaime blind to the trap. Grey Wind fought in the van. Jaime killed three of Robb's men before being captured.
- **anchor quote:** `"Raid him here," he said, pointing. "A few hundred men, no more. Tully banners. When he comes after you, we will be waiting"—his finger moved an inch to the left—"here."` — agot-catelyn-10:71
- **supporting quote (battle outcome):** `"The Kingslayer," Hal announced, unnecessarily.` — agot-catelyn-10:102

> **NB on the quarantined wiki twin:** baseline notes a `graph/nodes/_conflicts/battle-of-the-whispering-wood.node.md` is excluded from index/query/resolver. Minting into `graph/nodes/events/` is safe.

---

## Proposed NEW edges

### Causal spine (relief-rise ENABLES chain)

| source_slug | edge_type | target_slug | tier | qualifier | verbatim quote + chapter:line | rationale |
|---|---|---|---|---|---|---|
| `battle-on-the-green-fork` | `ENABLES` | `battle-of-the-whispering-wood` | Tier-1 | — | `"The foot can continue down the kingsroad, while our horsemen cross the Green Fork at the Twins … When Lord Tywin gets word that we've come south, he'll march north to engage our main host, leaving our riders free to hurry down the west bank to Riverrun."` agot-catelyn-08:151 | Robb's stated plan: the Green Fork foot-march is a **deliberate feint** intended to draw Tywin north. Tywin marching north to engage Bolton's host is the precondition that strips Jaime of reinforcement and leaves his cavalry unsupported at Riverrun. ENABLES not CAUSES: Tywin chose to march; Robb chose to spring the trap. The Green Fork engagement opened the window; the Whispering Wood is Robb's free act in that window. |
| `battle-of-the-whispering-wood` | `ENABLES` | `battle-of-the-camps` | Tier-1 | — | `"He is no man for sitting in a tent while his carpenters build siege towers … Twelve thousand foot, scattered around the castle in three separate camps, with the rivers between … there is one thing Ser Jaime lacks … Patience."` agot-catelyn-10:35–43 | The Blackfish's intelligence makes explicit that Jaime's CAVALRY is the mobile force, and that the foot is **scattered in three separate camps with rivers between**. Capturing Jaime + destroying three-quarters of the Lannister horse left the foot fragmented, leaderless, and blind (outriders eliminated). The Camps assault works only because the mobile screen is gone and no commander can consolidate the scattered foot. ENABLES not CAUSES: Robb's host still had to choose and execute the assault on the camps. |
| `battle-of-the-camps` | `ENABLES` | `robb-proclaimed-king-in-the-north` | Tier-1 | — | `"Word of the victory at Riverrun had spread to the fugitive lords of the Trident, drawing them back. Karyl Vance came in … Ser Marq Piper was with him … Lord Jonos Bracken arrived … and many other good men besides"` agot-catelyn-11:143 | The twin victories (Whispering Wood + Camps) and the relief of Riverrun gathered both the northern lords AND the fugitive river lords at Riverrun for the war council. Without that assembly there is no body to proclaim him. The Greatjon's proclamation and the lords' unanimous kneeling is a **free collective choice** — ENABLES not CAUSES. The execution's CAUSES edge (existing, S113) supplies the grievance/motive; this ENABLES supplies the military precondition that gathered the audience. Both coexist cleanly. |

---

### Siege-of-Riverrun seam — **[BORDERLINE]**

| source_slug | edge_type | target_slug | tier | qualifier | verbatim quote + chapter:line | rationale |
|---|---|---|---|---|---|---|
| `battle-of-the-camps` | `ENABLES` | `siege-of-riverrun` | Tier-2 | — | `"and we've brought you Jaime Lannister, in irons. Riverrun is free again, Father."` agot-catelyn-11:61 | **[BORDERLINE] — direction concern.** The Camps battle BROKE the siege (siege resolved). Proposing `battle-of-the-camps ENABLES siege-of-riverrun` would be directionally wrong — the Camps is not what caused the siege to begin. The honest framing is the inverse: the siege is ENDED/resolved by the Camps. However, `ENABLES` is an asymmetric precondition type and there is no `RESOLVES` or `BREAKS` in the locked vocabulary. The cleanest available edges are: (a) propose nothing (the relationship is temporal-resolution, not causal-precondition), or (b) model a `PREVENTS` edge (`battle-of-the-camps PREVENTS ?` — but there's no good target). **My recommendation: do NOT propose a causal edge in this direction. Instead, flag for synthesis: the siege-of-riverrun node could receive a prose note that it was broken by the Camps, without minting a structural ENABLES seam.** The `siege-of-riverrun` node is causally islanded, but its gap is better filled by reification roles (see below) than by a mis-directed causal edge. |

---

### Setup edge for the siege-of-riverrun (origin, not resolution) — **[BORDERLINE]**

| source_slug | edge_type | target_slug | tier | qualifier | verbatim quote + chapter:line | rationale |
|---|---|---|---|---|---|---|
| `battle-under-the-walls-of-riverrun` | `ENABLES` | `siege-of-riverrun` | Tier-2 | — | `"The Kingslayer has destroyed Edmure's host and sent the lords of the Trident reeling in flight … Lord Blackwood and the other survivors are under siege inside Riverrun, surrounded by Jaime's host."` agot-catelyn-09:69–73 | **[BORDERLINE] — new-node risk.** The text names a distinct prior battle: "a battle under the walls of Riverrun" where Edmure was defeated and captured before the siege began. This battle is the precondition that made the siege possible (Edmure's field army destroyed → the castle could be surrounded with no relieving force). This edge is honest; the event also appears in the baseline chapter map. However, `battle-under-the-walls-of-riverrun` may not exist as a live node — baseline names it as a chapter-map item but does not list it in the dedup hot zones. **Flag for synthesis to check whether the node exists; if yes, the ENABLES is clean; if no, do not mint the node (out of PASS 1 scope — it's a setup to the setup).** |

---

### Whispering Wood participant roles (reification of the new node)

| source_slug | edge_type | target_slug | tier | qualifier | verbatim quote + chapter:line | rationale |
|---|---|---|---|---|---|---|
| `robb-stark` | `COMMANDS_IN` | `battle-of-the-whispering-wood` | Tier-1 | — | `"There sits the only king I mean to bow my knee to … The King in the North!"` — this is downstream; for COMMANDS cite: `"Raid him here … When he comes after you, we will be waiting … here."` agot-catelyn-10:71 | Robb designed and commanded the trap. |
| `robb-stark` | `AGENT_IN` | `battle-of-the-whispering-wood` | Tier-1 | — | `"Winterfell!" she heard Robb shout as the arrows sighed again. He moved away from her at a trot, leading his men downhill.` agot-catelyn-10:85 | Robb personally led the downhill charge. |
| `grey-wind` | `AGENT_IN` | `battle-of-the-whispering-wood` | Tier-1 | — | `"she heard his direwolf, snarling and growling, heard the snap of those long teeth, the tearing of flesh, shrieks of fear and pain from man and horse alike."` agot-catelyn-10:93 | Grey Wind fought in the battle. |
| `brynden-tully` | `COMMANDS_IN` | `battle-of-the-whispering-wood` | Tier-1 | — | `"Robb had given the Blackfish three hundred picked men, and sent them ahead to screen his march. 'Jaime does not know … No bird has reached him, my archers have seen to that. We've seen a few of his outriders, but those that saw us did not live to tell of it.'"` agot-catelyn-10:31 | The Blackfish commanded the screen/outrider-suppression operation that blinded Jaime and enabled the trap. COMMANDS_IN for the screening phase; the battle itself is Robb's command but the Blackfish's prep is load-bearing. |
| `jaime-lannister` | `VICTIM_IN` | `battle-of-the-whispering-wood` | Tier-1 | — | `"They threw him down in front of her horse. 'The Kingslayer,' Hal announced, unnecessarily."` agot-catelyn-10:101–102 | Jaime captured; his force destroyed. |
| `jon-umber` | `FIGHTS_IN` | `battle-of-the-whispering-wood` | Tier-1 | — | `"HAAroooooooooooooooooooooooo came the answer from the far ridge as the Greatjon winded his own horn."` agot-catelyn-10:83 | The Greatjon commanded the far ridge line. |
| `rickard-karstark` | `FIGHTS_IN` | `battle-of-the-whispering-wood` | Tier-1 | — | `"North, where the valley narrowed and bent like a cocked elbow, Lord Karstark's warhorns added their own deep, mournful voices to the dark chorus."` agot-catelyn-10:83 | Karstark commanded the northern pinch point. He also lost two sons here (Torrhen and Eddard Karstark). |
| `maege-mormont` | `FIGHTS_IN` | `battle-of-the-whispering-wood` | Tier-1 | — | `"Here was the call of Maege Mormont's warhorn, a long low blast that rolled down the valley from the east, to tell them that the last of Jaime's riders had entered the trap."` agot-catelyn-10:77 | Mormont commanded the eastern horn; her warhorn was the signal. |
| `galbart-glover` | `FIGHTS_IN` | `battle-of-the-whispering-wood` | Tier-1 | — | `"Galbart Glover explained."` agot-catelyn-10:127 | Present at the battle (gives Catelyn the account of Jaime's rally); in Robb's battle group per cat-08. |
| `battle-of-the-whispering-wood` | `LOCATED_AT` | `whispering-wood` | Tier-1 | — | `"The woods were full of whispers."` / `"Theon Greyjoy was seated on a bench … regaling her father's garrison with an account of the slaughter in the Whispering Wood."` agot-catelyn-10:11; agot-catelyn-11:117 | Place named explicitly in cat-11's recap. |
| `jason-mallister` | `FIGHTS_IN` | `battle-of-the-whispering-wood` | Tier-2 | — | `"Lord Jason Mallister had brought his power out from Seagard to join them as they swept around the headwaters of the Blue Fork and galloped south"` agot-catelyn-10:45 | Mallister joined the host before the battle; his trumpets sounded in the trap (cat-10:83 "trumpets of the Mallisters and Freys blew vengeance"). Tier-2 because the text says he joined the march, not that he personally fought, though his trumpeters are explicit. |

---

### Suspicious existing edges — verification flags

**`roose-bolton CAPTURES jaime-lannister` (existing, Tier-1) — LIKELY WRONG.**
Roose Bolton commanded the **foot on the kingsroad** (the Green Fork feint host, per agot-catelyn-08:257: "The larger part of the northern host, pikes and archers and great masses of men-at-arms on foot, remained upon the east bank under the command of Roose Bolton"). He was **nowhere near the Whispering Wood**. The battle where Jaime was captured was fought by Robb's cavalry on the west bank. The correct capture-agent is Robb's host, not Roose. Recommend: flag as `bug_drop` candidate; verify against graph/nodes before proposing correction.

**`catelyn-stark CAPTURES jaime-lannister` (existing, Tier-1) — QUESTIONABLE.**
Catelyn waited outside the wood with thirty guards (agot-catelyn-10:15-16). Robb's forces brought Jaime to her afterward: `"Between them they dragged Ser Jaime Lannister. They threw him down in front of her horse."` (agot-catelyn-10:101). She received the prisoner and gave the order "Take him away and put him in irons" (agot-catelyn-10:117). Catelyn did not capture Jaime; Robb's host did. The existing CAPTURES edge is at best metaphorical (she received / ordered his custody). Recommend: flag for review; possibly retype as `IMPRISONS` or demote to Tier-3 with a note.

---

## Dropped / considered-but-rejected

- **`battle-on-the-green-fork CAUSES battle-of-the-whispering-wood`** — WRONG type. The Green Fork battle is a deliberate feint/diversion, a free strategic choice by Robb. The correct edge is ENABLES. Dropped in favor of ENABLES.

- **`execution-of-eddard-stark CAUSES robb-proclaimed-king-in-the-north`** — ALREADY EXISTS (S113). Not re-proposed. My ENABLES edge (`battle-of-the-camps ENABLES robb-proclaimed`) is additive and complementary: the execution is the *motive*; the battle victory is the *military precondition*.

- **`siege-of-riverrun ENABLES battle-of-the-whispering-wood`** — considered: the siege gave Robb a fixed target to relieve. But this is sequence/co-presence, not causal precondition in the ENABLES sense. Robb would have marched on the Lannisters regardless. Dropped.

- **`robb-stark MOTIVATES robb-proclaimed-king-in-the-north`** — MOTIVATES targets a CHARACTER, not an event. Dropped by definition.

- **`battle-of-the-camps ENABLES siege-of-riverrun` (forward direction)** — WRONG direction. The Camps RESOLVED the siege; it didn't cause it to begin. No `RESOLVES` type exists. Dropped; flagged as BORDERLINE in main table.

- **`walder-frey ENABLES battle-of-the-whispering-wood`** — The Frey crossing (Twins) was a necessary logistical precondition, but the ENABLES edge from `battle-on-the-green-fork` already captures the strategic precondition. Adding a Walder-ENABLES would be a different node type (character→event, not event→event) and is marginal. The Frey betrothal deal is already in the graph (B1 Red-Wedding-upstream spine per baseline). Dropped to avoid over-proliferating the causal chain.

- **`dacey-mormont FIGHTS_IN battle-of-the-whispering-wood`** — Cat-10 lists Dacey Mormont among Robb's battle guard (agot-catelyn-10:53). She was part of the Whispering Wood force but her role is as personal guard to Robb, not an independent command. The text doesn't put her in a named combat role. Borderline; dropped for now; can be added in a later pass.

- **`theon-greyjoy FIGHTS_IN battle-of-the-whispering-wood`** — Theon was among Robb's companions (agot-catelyn-10:53) and gave the Riverrun garrison his firsthand account (cat-11:117). However his role in the battle itself is not command-level. Dropped; Theon's FIGHTS_IN battle-of-the-camps may already exist (check baseline).

- **Karyl Vance / Marq Piper raids (Camps-side)** — The text references them as pre-battle harassment lords (cat-11:143), not as direct Whispering Wood participants. PASS 1 scope; marginal. Dropped.

- **PASS 2/3 material (explicitly out of scope):**
  - Oxcross / Crag / Jeyne Westerling — PASS 2
  - Duskendale / Bolton treason question — PASS 3
  - Frey betrayal causal chain (already in B1 spine)

---

## Harvest

| kind | book | chapter:line | note |
|---|---|---|---|
| food | AGOT | agot-catelyn-08:25 | Camp provisioning: wagons "heavy-laden with hardbread and salt beef" on the march to Moat Cailin |
| food | AGOT | agot-catelyn-08:63 | Ale and cheese on Robb's war-council table at Moat Cailin ("There was ale and cheese on the table. Catelyn filled a horn, sat, sipped") |
| food | AGOT | agot-catelyn-09:137–139 | Lord Walder's hall overflowing with family; feast-hospitality context during the Twins negotiation (hospitality as political leverage) |
| quote-load-bearing | AGOT | agot-catelyn-09:221 | Robb's army crossing the Twins at moonfall: "They crossed at evenfall as a horned moon floated upon the river. The double column wound its way through the gate of the eastern twin like a great steel snake" — vivid; for the Twins or the WW node |
| food/medical | AGOT | agot-catelyn-11:55 | Hoster Tully's palliative care: "Maester Vyman makes me dreamwine, milk of the poppy … I sleep a lot" — dreamwine + milk of the poppy together; Hoster's dying scene |
| description-physical | AGOT | agot-catelyn-10:11–13 | Pre-battle wood: "Moonlight winked on the tumbling waters of the stream … Beneath the trees, warhorses whickered softly and pawed at the moist, leafy ground … the chink of spears, the faint metallic slither of chain mail" — the hush of the Whispering Wood |
| quote-load-bearing | AGOT | agot-catelyn-10:73 | `"Here was a hush in the night, moonlight and shadows, a thick carpet of dead leaves underfoot, densely wooded ridges sloping gently down to the streambed"` — the 'Here' passage; strong atmosphere; attach to battle-of-the-whispering-wood ## Quotes |
| quote-load-bearing | AGOT | agot-catelyn-10:79–81 | Grey Wind's howl: `"And Grey Wind threw back his head and howled. The sound seemed to go right through Catelyn Stark, and she found herself shivering … So this is what death sounds like, she thought."` — node ## Quotes; battle-of-the-whispering-wood |
| quote-load-bearing | AGOT | agot-catelyn-10:88–90 | Greatjon's riders emerging: "an endless line, and as they burst from the wood there was an instant … when all Catelyn saw was the moonlight on the points of their lances, as if a thousand willowisps were coming down the ridge, wreathed in silver flame" — vivid; whispering-wood battle node |
| quote-load-bearing | AGOT | agot-catelyn-11:61 | "Riverrun is free again, Father." — load-bearing; attach to battle-of-the-camps or siege-of-riverrun node ## Quotes |
| quote-load-bearing | AGOT | agot-catelyn-11:63 | Hoster on the battlements watching: "the torches came in a wave, I could hear the cries floating across the river … sweet cries … when that siege tower went up, gods … would have died then, and glad" — watching the Camps battle from the gatehouse; hoster-tully WITNESS_IN battle-of-the-camps may already exist (check baseline — it does, per baseline §3) |
| description-physical | AGOT | agot-catelyn-11:117 | Theon's account of Grey Wind: "I saw him tear one man's arm from his shoulder, and their horses went mad at the scent of him" — Grey Wind description; attach to grey-wind node or battle-of-the-whispering-wood ## Quotes |
| quote-load-bearing | AGOT | agot-catelyn-11:209–211 | Greatjon's King-in-the-North proclamation: `"There sits the only king I mean to bow my knee to, m'lords … The King in the North!"` / `"And he knelt, and laid his sword at her son's feet."` — attach to robb-proclaimed-king-in-the-north node ## Quotes (if not already there) |
| quote-load-bearing | AGOT | agot-catelyn-11:215–221 | The lords' unanimous proclamation including river lords: `"houses who had never been ruled from Winterfell, yet Catelyn watched them rise and draw their blades … 'THE KING IN THE NORTH!'"` — the moment the WO5K launches; node ## Quotes |
| foreshadowing | AGOT | agot-catelyn-09:237–241 | Robb consents to the Frey marriage pact — knowing he must; the betrothal that becomes the Red Wedding trigger. For foreshadowing-events: plant on the Frey betrayal node (PASS 2/3). |
| description-physical | AGOT | agot-catelyn-11:47 | Hoster Tully on the deathbed: "Now he seemed shrunken, the muscle and meat melted off his bones. Even his face sagged … his hair and beard had gone white as snow." — vivid physical description; hoster-tully node ## Descriptions |
| hospitality | AGOT | agot-catelyn-11:143–144 | War council at Riverrun's Great Hall: "four long trestle tables arranged in a broken square" — the gathering of lords; hospitality/council setting; node prose for robb-proclaimed-king-in-the-north |
