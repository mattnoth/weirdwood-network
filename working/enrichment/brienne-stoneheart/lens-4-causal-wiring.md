# Lens 4 — Causal Wiring (Cross-Arc Seams)
## Brienne → Lady Stoneheart arc (AFFC)
Generated: 2026-06-24

---

## VERIFICATION LOG

All source slugs exist confirmed via `graph-query.py --neighbors`:
- `brave-companions` ✓ | `rorge` ✓ | `biter` ✓ | `sandor-clegane` ✓
- `elder-brother-quiet-isle` ✓ | `randyll-tarly` ✓ | `brotherhood-without-banners` ✓
- `beric-dondarrion` ✓ | `thoros` ✓ | `catelyn-stark` ✓ | `gendry` ✓
- `raid-on-saltpans` ✓ | `capture-of-harrenhal` ✓
- `catelyn-rises-as-lady-stoneheart` ✓ | `brienne-brought-before-lady-stoneheart` ✓
- `inn-at-the-crossroads` ✓ | `saltpans` ✓ | `maidenpool` ✓ | `quiet-isle` ✓
- `willow-heddle` ✓ | `jeyne-heddle` ✓ | `lem` ✓ | `meribald` ✓
- `oathkeeper` ✓ (0 edges — needs wiring) | `battle-at-the-burning-septry` ✓

---

## PROPOSED EDGES

### SEAM A — Brave Companions dissolution → Raid on Saltpans

**A1.** `brave-companions --ENABLES--> raid-on-saltpans`
- tier: tier-1
- ref: affc-brienne-04.md:273 (Timeon's direct account)
- quote: "We all went our own ways, after we left Harrenhal. Urswyck and his lot rode south for Oldtown. Rorge thought he might slip out at Saltpans."
- rationale: The Brave Companions' dissolution at Harrenhal (post-`capture-of-harrenhal`) dispersed their remnants; Rorge's band specifically fled toward Saltpans with the stated intent of finding a ship, which placed them in position to commit the raid. This is the direct distal precondition. Both endpoints verified.

**A2.** `capture-of-harrenhal --ENABLES--> raid-on-saltpans`
- tier: tier-1
- ref: graph/nodes/events/raid-on-saltpans.node.md:25 (wiki body, Origins section)
- quote: "Abandoned by almost all of the Brave Companions, Vargo is killed by Ser Gregor Clegane after the capture of Harrenhal."
- rationale: The capture of Harrenhal by Lannister forces ended Vargo Hoat's hold and caused the Brave Companions to scatter; without that dissolution there is no Rorge-band at Saltpans. Cross-arc seam: Lannister/Harrenhal arc → Brienne arc. INFERENCE FLAG: the wiki node body states this but the AFFC text (Timeon, affc-brienne-04:273) confirms the causal chain directly. Both endpoints verified.

**A3.** `rorge --AGENT_IN--> raid-on-saltpans`
- tier: tier-1
- ref: affc-brienne-08.md:215
- quote: "It was Rorge I killed. He took the helm from Clegane's grave, and you stole it off his corpse."
- rationale: Rorge led the Saltpans raid wearing the Hound's helm; Brienne confirms his identity and agency in ch8. The node currently has 0 AGENT_IN edges for this event. Both endpoints verified.

**A4.** `biter --AGENT_IN--> raid-on-saltpans`
- tier: tier-1
- ref: graph/nodes/events/raid-on-saltpans.node.md:29 (wiki body)
- quote: "One band of fleeing Brave Companions is led by Rorge, who has his constant companion Biter at his side."
- rationale: Biter is Rorge's constant companion in the raid; the wiki body and Brienne's AFFC fight at the inn (where Biter attacks after Rorge dies, affc-brienne-07:295) both establish joint agency. Both endpoints verified.

**A5.** `raid-on-saltpans --LOCATED_AT--> saltpans`
- tier: tier-1
- ref: graph/nodes/events/raid-on-saltpans.node.md:67 (Quotes section)
- quote: "At Saltpans, they had found only death and desolation."
- rationale: Structural location edge entirely absent from the islanded node. Both endpoints verified.

---

### SEAM B — Sandor's Grave-Helm → Rorge → False Reputation

**B1.** `elder-brother-quiet-isle --ENABLES--> raid-on-saltpans`
- tier: tier-1
- ref: affc-brienne-06.md:185
- quote: "I covered him with stones to keep the carrion eaters from digging up his flesh, and set his helm atop the cairn to mark his final resting place. That was a grievous error."
- rationale: The Elder Brother placed Sandor's distinctive helm on the grave-cairn, which Rorge's band found on their way to Saltpans. Without the helm on the cairn, Rorge does not wear it; without the helm, the realm does not mistake the raid for Sandor's work. This is the accidental door-opener for the false-reputation engine. Both endpoints verified.
- NOTE: The Elder Brother explicitly calls this "a grievous error," framing it as inadvertent causation — exactly the ENABLES (distal door-opener) register, not CAUSES.

**B2.** `raid-on-saltpans --MOTIVATES--> brienne-tarth`
- tier: tier-1
- ref: affc-brienne-05.md:127
- quote: "Sandor Clegane was last seen in Saltpans, the day of the raid. Afterward he rode west, along the Trident."
- rationale: The false attribution of the Saltpans raid to the Hound is what causes Brienne to redirect her search from Sansa/Dontos → the Hound. Hyle Hunt's report at the Stinking Goose (affc-brienne-05:127) directly pivots her quest. MOTIVATES targets a character only — this is well-formed. Both endpoints verified.

**B3.** `randyll-tarly --DECEIVES--> brotherhood-without-banners`
- tier: tier-1
- ref: affc-brienne-05.md:135
- quote: "Lord Randyll is putting it about that they did in hopes of turning the commons against Beric and his brotherhood."
- rationale: Randyll Tarly spreads rumors blaming the Saltpans raid on Beric's Brotherhood to damage their popular support. The wiki node (raid-on-saltpans.node.md:35) confirms this as Tarly's deliberate political tactic. The target is the brotherhood as an organization; smallfolk are the intermediate vectors but the Brotherhood is the entity defamed. Both endpoints verified.
- NOTE: DECEIVES is the right edge here — Tarly is crafting a false narrative aimed at discrediting the Brotherhood, not a direct deception of individuals. Alternative read: MANIPULATES → smallfolk, but the Brotherhood is the target of the reputational attack. DECEIVES fits better.

**B4.** `randyll-tarly --INFORMS--> brienne-tarth`
- tier: tier-1
- ref: affc-brienne-05.md:127
- quote: "Sandor Clegane was last seen in Saltpans, the day of the raid. Afterward he rode west, along the Trident."
- rationale: Hyle Hunt's Stinking Goose briefing relays Tarly's intelligence network's report to Brienne, redirecting her hunt. The information originates in Tarly's garrison network at Maidenpool (affc-brienne-03:163 establishes Tarly at Maidenpool; Hunt is his household knight). Both endpoints verified.

---

### SEAM C — Brotherhood Transformation (Beric → Stoneheart)

**C1.** `catelyn-rises-as-lady-stoneheart --MOTIVATES--> brotherhood-without-banners`
- tier: tier-1
- ref: affc-brienne-08.md:323
- quote: "She wants her son alive, or the men who killed him dead. She wants to feed the crows, like they did at the Red Wedding. Freys and Boltons, aye."
- rationale: Stoneheart's resurrection transformed the Brotherhood from Beric's outlaw-justice band (trials, redemption, ransom) into a vengeance cult targeting Freys, Boltons, and perceived Lannister agents. Her COMMANDS edge already exists; this MOTIVATES edge captures the causal shift in the Brotherhood's PURPOSE that COMMANDS does not — it is directed at the collective organization, not a specific event. MOTIVATES targets a character — "organization" is technically not a character. NEEDS_VOCAB check: the Brotherhood is an organization.faction. However, the baseline already shows catelyn-stark COMMANDS brotherhood-without-banners. MOTIVATES is close but strictly limited to characters. Use CAUSES instead: `catelyn-rises-as-lady-stoneheart --CAUSES--> [brotherhood-changes-mission]` — but that event node does not exist.
- **REVISED PROPOSAL:** `catelyn-stark --MOTIVATES--> lem` (the agent who physically runs the vengeance operations, embodies the new Brotherhood) — see C2.
- **This edge as stated: FLAG for orchestrator — MOTIVATES → faction is borderline. Propose as CAUSES with note.**

**C2.** `catelyn-stark --MOTIVATES--> lem`
- tier: tier-1
- ref: affc-brienne-08.md:323
- quote: "She wants her son alive, or the men who killed him dead. She wants to feed the crows, like they did at the Red Wedding."
- rationale: Lem Lemoncloak is the Brotherhood's operational enforcer under Stoneheart (he runs the hangings, he commands the inn party, he claims the Hound's helm). Catelyn-as-Stoneheart's vengeance drive directly motivates Lem's actions throughout the AFFC arc. Both endpoints verified (catelyn-stark ✓, lem ✓).

**C3.** `beric-dondarrion --ENABLES--> catelyn-rises-as-lady-stoneheart`
- tier: tier-1
- ref: affc-brienne-08.md:311
- quote: "Lord Beric put his lips to hers instead, and the flame of life passed from him to her. And . . . she rose."
- rationale: This edge may already exist — checking: graph-query confirms beric-dondarrion AGENT_IN catelyn-rises-as-lady-stoneheart. The ENABLES angle (beric's accumulated resurrection capacity, accumulated through repeated Thoros resurrections, enables the final kiss-of-life transfer) is already captured by AGENT_IN. SKIP — covered.

**C4.** `red-wedding --MOTIVATES--> catelyn-stark`
- tier: tier-1
- ref: affc-brienne-08.md:323
- quote: "She wants her son alive, or the men who killed him dead. She wants to feed the crows, like they did at the Red Wedding."
- rationale: The Red Wedding's atrocity is the explicit motive source for all of Stoneheart's vengeance actions. Already: catelyn-is-killed SUB_BEAT_OF red-wedding; catelyn-stark VICTIM_IN catelyn-is-killed. But there is no edge wiring red-wedding as the MOTIVATING event for catelyn-stark's actions as Stoneheart. Both endpoints verified (red-wedding ✓, catelyn-stark ✓).
- NOTE: This is a cross-arc seam: the Red Wedding arc (ASOS) directly MOTIVATES the AFFC Brienne arc's entire antagonist dynamic.

---

### SEAM D — Oathkeeper's Chain of Custody

**D1.** `oathkeeper --WIELDS--> brienne-tarth`  
*(direction: brienne-tarth WIELDS oathkeeper)*
- tier: tier-1
- ref: affc-brienne-01.md:283
- quote: "When she slid Oathkeeper from the ornate scabbard, Brienne's breath caught in her throat. Black and red the ripples ran, deep within the steel. Valyrian steel, spell-forged."
- rationale: Brienne wields Oathkeeper throughout the entire AFFC arc; the sword node has 0 edges. This is the most basic wiring. Direction: `brienne-tarth WIELDS oathkeeper`. Both endpoints verified.

**D2.** `oathkeeper --GIFTED_TO--> brienne-tarth`  
*(direction: jaime-lannister GIFTED_TO brienne-tarth oathkeeper)*  
Reformulated: `jaime-lannister --BESTOWS_KNIGHTHOOD_ON--> brienne-tarth` is wrong register. Use:
- `brienne-tarth --OWNS--> oathkeeper`
- tier: tier-1
- ref: affc-brienne-01.md:283
- quote: "Kneeling between the bed and wall, she held the blade and said a silent prayer to the Crone . . . 'You'll be defending Ned Stark's daughter with Ned Stark's own steel,' Jaime had promised."
- rationale: Jaime gave Brienne Oathkeeper with the oath. The GIFTED_TO edge goes `jaime-lannister --GIFTED_TO--> oathkeeper` or more precisely `jaime-lannister --GIFTED_TO--> brienne-tarth` with oathkeeper as the mechanism. Since GIFTED_TO takes (giver→receiver) and the object is the artifact itself: propose `jaime-lannister --GIFTED_TO--> oathkeeper` is the wrong shape. The clearest available: `brienne-tarth OWNS oathkeeper`. Both endpoints verified.

**D3.** Oathkeeper as evidence against Brienne: the sword's lion-pommel ruby eyes reveal its Lannister provenance at Stoneheart's tribunal.
- `oathkeeper --SUSPECTED_OF--> brienne-tarth` — wrong shape.
- This is better modeled as: `catelyn-stark --DISTRUSTS--> brienne-tarth` (already exists likely) or the sword being evidence.
- STRUCTURAL NOTE for orchestrator: the oathkeeper scene at affc-brienne-08:257 — the northman lays oathkeeper before Stoneheart and its Lannister iconography is the evidence of treachery — is more of an evidence/quote attachment than a new edge type. Flagging for harvest queue. SKIP proposing a broken-shape edge.

---

### SEAM E — Brienne's arc dead-end (the hanging)

**E1.** `brienne-brought-before-lady-stoneheart --TRIGGERS--> [hanging event]`
- PROBLEM: There is no node for the hanging itself ("Hang them"). The end-state of the AFFC arc (the elm-tree hangings of Brienne, Pod, and Hyle) has no event node.
- PROPOSAL TO ORCHESTRATOR: Mint `brienne-pod-hyle-hanged` (event.incident). Edges would be: CAUSES <- brienne-brought-before-lady-stoneheart; VICTIM_IN <- brienne-tarth, podrick-payne, hyle-hunt; COMMANDS_IN <- catelyn-stark; AGENT_IN <- lem, brotherhood-without-banners. This is LENS 4's clearest structural gap — the arc's final event is missing. Cannot propose the edges without the node.

**E2.** `brienne-brought-before-lady-stoneheart --MOTIVATES--> brienne-tarth`
- tier: tier-1
- ref: affc-brienne-08.md:327-329
- quote: "She says that you must choose. Take the sword and slay the Kingslayer, or be hanged for a betrayer. The sword or the noose, she says. Choose, she says. Choose."
- rationale: The sword-or-noose ultimatum at the hanging tree motivates Brienne's screamed word at chapter's end (affc-brienne-08:349: "She screamed a word.") — the unseen word that presumably summons Jaime to the Riverlands (TWOW setup). MOTIVATES a character is well-formed. Both endpoints verified.

---

### SEAM F — Gendry → Inn → Brotherhood

**F1.** `gendry --MEMBER_OF--> brotherhood-without-banners`
- tier: tier-1  
- ref: affc-brienne-07.md:252 + 08.md:53
- quote: "Someone is coming." "Friends," said Gendry, unconcerned." [affc-brienne-07:252]; "He's dead. Gendry shoved a spearpoint through the back of his neck." [affc-brienne-08:53]
- rationale: Gendry knows Rorge's band are coming (affc-brienne-07:252) and acts to protect the inn, then kills Biter after the fight — he operates as a Brotherhood-affiliated agent guarding the inn. The MEMBER_OF edge already exists per graph-query (gendry -> brotherhood-without-banners shows). SKIP — already exists.

**F2.** `gendry --KILLS--> biter`
- SKIP — already exists per graph-query (gendry KILLS biter ✓).

**F3.** `gendry --GUEST_OF--> willow-heddle`
- tier: tier-1
- ref: affc-brienne-07.md:135
- quote: "No," said the boy smith. "Yes," said the girl Willow. They glared at one another. Then Willow stomped her foot. "They have food, Gendry. The little ones are hungry.""
- rationale: Gendry is resident smith at the crossroads inn run by Willow Heddle; GUEST_OF captures the hospitality/shelter relationship. Both endpoints verified.
- NOTE: GUEST_OF is technically "hospitality extended by host." Willow-heddle is co-host (alongside Jeyne-heddle). This is a borderline use — "resident smith" is closer to COMPANION_OF or just colocation. FLAG for orchestrator. Possible alternate: omit; it's not high-yield.

**F4.** `willow-heddle --GUEST_OF--> brienne-tarth`
- WRONG DIRECTION. Brienne is the guest, Willow is the host.
- CORRECT: `brienne-tarth --GUEST_OF--> willow-heddle`
- tier: tier-1
- ref: affc-brienne-07.md:91
- quote: "Willow . . . Will you be wanting beds?" / "Beds, and ale, and hot food to fill our bellies."
- rationale: Brienne and party are explicitly received as guests by Willow Heddle at the crossroads inn. Both endpoints verified.

---

### SEAM G — Randyll Tarly governance seam (Maidenpool ↔ Brotherhood)

**G1.** `randyll-tarly --EXECUTES--> brotherhood-without-banners`
- SKIP — already exists per graph-query (randyll-tarly EXECUTES brotherhood-without-banners ✓).

**G2.** `randyll-tarly --INFORMS--> brienne-tarth` (re: Saltpans + Hound location)
- Already proposed as B4 above.

**G3.** `randyll-tarly --SUSPECTED_OF--> raid-on-saltpans`
- WRONG — Tarly is not suspected of the raid. He responds to it. Drop.

---

### SEAM H — Meribald / Quiet Isle / Saltpans chain

**H1.** `meribald --TRAVELS_TO--> saltpans`
- tier: tier-1
- ref: affc-brienne-06.md:13
- quote: "Saltpans is just across the water. The brothers will ferry us over on the morning tide."
- rationale: Meribald leads the party to Saltpans via the Quiet Isle ferry; this is the journey that establishes the Saltpans aftermath for Brienne. Both endpoints verified.
- NOTE: Low structural yield — this is a travel edge, not a causal seam. Flagging as optional. The causal chain for this lens is already covered by higher-priority edges above.

**H2.** `elder-brother-quiet-isle --REVEALS_TO--> brienne-tarth`
- tier: tier-1
- ref: affc-brienne-06.md:169-191
- quote: "Your Dornishman did not lie . . . but I fear you did not understand him. You are chasing the wrong wolf, my lady . . . The man you hunt is dead. I buried him myself."
- rationale: The Elder Brother reveals two critical facts to Brienne: (1) Sandor is dead, (2) the girl with him was Arya not Sansa. Both pivot her quest. REVEALS_TO is well-formed (source=revealer, target=receiver). Both endpoints verified.

**H3.** `elder-brother-quiet-isle --HEALS--> sandor-clegane`
- tier: tier-1
- ref: affc-brienne-06.md:191
- quote: "I bathed his fevered brow with river water, and gave him wine to drink and a poultice for his wound, but my efforts were too little and too late. The Hound died there, in my arms."
- rationale: The Elder Brother tended Sandor's wound, even if the healing failed. HEALS captures the act of healing (not necessarily successful). Both endpoints verified.

---

### SEAM I — Red Wedding Cross-Arc Wire (the root cause)

**I1.** `red-wedding --CAUSES--> catelyn-rises-as-lady-stoneheart`
- CHECK: Already exists? catelyn-is-killed SUB_BEAT_OF red-wedding; catelyn-is-killed CAUSES catelyn-rises-as-lady-stoneheart. So the chain exists through catelyn-is-killed. A direct red-wedding → catelyn-rises edge would be redundant with the existing two-hop chain. SKIP.

**I2.** `house-frey --MOTIVATES--> catelyn-stark` (Stoneheart's specific targeting)
- tier: tier-1
- ref: affc-brienne-08.md:323
- quote: "She wants her son alive, or the men who killed him dead. She wants to feed the crows, like they did at the Red Wedding. Freys and Boltons, aye."
- rationale: House Frey's Red Wedding murder of Catelyn is the specific motivation for Stoneheart's vengeance campaign against them. MOTIVATES targets a character (catelyn-stark) — well-formed. Both endpoints verified (house-frey ✓, catelyn-stark ✓).
- NOTE: This is a cross-arc seam: the Red Wedding arc (Frey arc) MOTIVATES the Brienne/Stoneheart arc antagonist. Higher value than the redundant I1.

---

## HARVEST QUEUE

(pointers only — do not extract, note location for later harvest pass)

- affc-brienne-05:175 / FOOD / Septon Meribald's donkey load itemized: "seeds and nuts and dried fruit, oaten porridge, flour, barley bread, three wheels of yellow cheese from the inn by the Fool's Gate, salt cod . . . salt mutton for Dog . . . salt. Onions, carrots, turnips, two sacks of beans, four of barley, and nine of oranges."
- affc-brienne-07:51 / FOOD/INN / crossroads inn described from Septon Meribald's history (Two Crowns, Bellringer, Clanking Dragon, River Inn names)
- affc-brienne-07:96 / DESCRIPTION / "horse meat" at the crossroads inn — war-time subsistence note
- affc-brienne-06:141 / FOOD / Quiet Isle supper: "loaves of crusty bread still warm from the ovens, crocks of fresh-churned butter, honey from the septry's hives, and a thick stew of crabs, mussels, and at least three different kinds of fish"
- affc-brienne-06:113 / DESCRIPTION / Elder Brother on Rhaegar's rubies washing up at Quiet Isle: "Six have been found. We are all waiting for the seventh."  — foreshadowing/prophecy pointer
- affc-brienne-05:259-305 / SERMON / Septon Meribald's broken-men sermon — extended verbatim; high-value social/thematic quote for PARALLELS or notes layer
- asos-epilogue:59 / DESCRIPTION / "A man in patched, faded greens was sitting crosslegged atop a weathered stone sepulcher, fingering the strings of a woodharp. The music was soft and sad."  — Tom of Sevenstreams; the song is "Jenny's Song"
- affc-brienne-08:257-260 / QUOTE / Oathkeeper presented to Stoneheart: "In the light from the firepit the red and black ripples in the blade almost seem to move, but the woman in grey had eyes only for the pommel: a golden lion's head, with ruby eyes that shone like two red stars." — attach as evidence_quote to oathkeeper node

---

## SUMMARY

Lens 4 identified **14 net-new edge proposals** across five cross-arc seams: (A) Brave Companions dissolution → Saltpans wiring (capture-of-harrenhal ENABLES raid-on-saltpans; brave-companions ENABLES raid-on-saltpans; rorge + biter AGENT_IN raid-on-saltpans; raid-on-saltpans LOCATED_AT saltpans); (B) Sandor's grave-helm chain (elder-brother-quiet-isle ENABLES raid-on-saltpans; raid-on-saltpans MOTIVATES brienne-tarth; randyll-tarly DECEIVES brotherhood-without-banners; randyll-tarly INFORMS brienne-tarth); (C) Brotherhood transformation (red-wedding MOTIVATES catelyn-stark; catelyn-stark MOTIVATES lem; house-frey MOTIVATES catelyn-stark); (D) Oathkeeper wiring (brienne-tarth WIELDS/OWNS oathkeeper; elder-brother-quiet-isle REVEALS_TO brienne-tarth; elder-brother-quiet-isle HEALS sandor-clegane); (E) the hanging event node is the arc's largest structural gap — `brienne-pod-hyle-hanged` must be minted to de-dead-end brienne-brought-before-lady-stoneheart. The highest-priority single fix is wiring `raid-on-saltpans` (currently 1 outgoing, 0 incoming) with rorge/biter AGENT_IN + brave-companions ENABLES + LOCATED_AT saltpans.
