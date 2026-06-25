# AEGON Enrichment Pass 1 — LENS B: Whodunit / Revelation / Hidden-Agency
> Produced: 2026-06-25
> Theory gate: OBSERVED. Aegon's identity / Blackfyre / fAegon babe-swap = GATED throughout.
> Sources read: adwd-epilogue.md, adwd-the-lost-lord-01.md, adwd-the-griffin-reborn-01.md, adwd-tyrion-06.md
> Dedup checks run: graph-query.py --neighbors + edges.jsonl greps for varys, rugen, jon-connington, greyscale, golden-company, aegon-targaryen-young-griff.

---

## Proposed edges

### 1. varys IMPERSONATES rugen
- **Source**: `varys` → **Type**: `IMPERSONATES` → **Target**: `rugen`
- **Tier**: 1
- **Book / chapter-file:line**: ADWD, adwd-epilogue.md:277 (primary); corroborating adwd-the-lost-lord-01.md:89
- **Verbatim quote** (primary — Varys in the rookery, inside Maegor's): "He stood in a pool of shadow by a bookcase, plump, pale-faced, round-shouldered, clutching a crossbow in soft powdered hands. Silk slippers swaddled his feet." (adwd-epilogue.md:277) — Varys is physically present inside Maegor's Holdfast, inside Pycelle's chambers, undetected. The Rugen undergaoler identity is what enabled years of access to King's Landing's restricted spaces.
- **Corroborating cite** (the scheme described): adwd-the-lost-lord-01.md:89 — "The shame of the lie still stuck in his craw, but Varys had insisted it was necessary. 'We want no songs about the gallant exile … Those who die heroic deaths are long remembered, thieves and drunks and cravens soon forgotten.'" (Shows Varys as architect of all cover identities in the conspiracy)
- **Graph context**: `rugen HOLDS_TITLE undergaoler` (wiki-infobox, Tier-2) and `varys HOLDS_TITLE undergaoler` (wiki-infobox, Tier-2) both already exist — they encode the positional title but NOT the identity-deception between the two character nodes. IMPERSONATES is the relationship between varys and rugen as a false persona.
- **HIT/NEW-NODE status**: HIT (both `varys` and `rugen` exist as nodes). The `IMPERSONATES` edge itself is **NEW** — not in graph.
- **Rationale**: IMPERSONATES = pretending to be a specific named person. Rugen is not just a title — it is a character node with its own identity. Varys operated under this false name for years in the black cells. This is distinct from DISGUISED_AS (physical appearance change) and from HOLDS_TITLE (positional fact). The IMPERSONATES edge is what closes the arc: it explains *how* Varys was inside the castle to commit the assassinations (he was known to the guards as the undergaoler Rugen, not as Varys the Master of Whisperers, who had "fled"). Tier-1.
- **Dedup note**: No `varys IMPERSONATES rugen` edge exists. The HOLDS_TITLE edges on both nodes are complementary, not redundant.

---

### 2. varys DECEIVES golden-company (re: Connington's honor)
- **Source**: `varys` → **Type**: `DECEIVES` → **Target**: `golden-company`
- **Tier**: 1
- **What Varys deceives them about**: That Jon Connington died a thief and a drunk in Lys — a fabricated disgrace to suppress heroic-exile songs and protect operational secrecy.
- **Book / chapter-file:line**: ADWD, adwd-the-lost-lord-01.md:89
- **Verbatim quote**: "Varys had insisted it was necessary. 'We want no songs about the gallant exile,' the eunuch had tittered, in that mincing voice of his. 'Those who die heroic deaths are long remembered, thieves and drunks and cravens soon forgotten.'"
- **HIT/NEW-NODE**: HIT (both nodes exist). **NEW** edge.
- **Rationale**: This is a distinct, load-bearing deception: Varys deliberately plants a false story about Connington among the Golden Company to keep the conspiracy quiet. This is not the same as the generic conspiracy dyad (`varys CONSPIRES_WITH illyrio`) — it is a *specific* act of DECEIVES directed at a specific target (the GC's institutional memory of Connington) for a named purpose. Tier-1 from JonCon's POV.

---

### 3. varys DECEIVES westeros (re: Aegon's survival)
- **Source**: `varys` → **Type**: `DECEIVES` → **Target**: `kevan-lannister`
- **Tier**: 1
- **What Varys deceives about**: That Aegon died in the Sack of King's Landing — the 15-year concealment of the prince's survival.
- **Book / chapter-file:line**: ADWD, adwd-epilogue.md:293–295
- **Verbatim quote**: "'Aegon?' For a moment he did not understand. Then he remembered. A babe swaddled in a crimson cloak, the cloth stained with his blood and brains. 'Dead. He's dead.' 'No.'"
- **Secondary anchor** (the deception's mechanism): adwd-the-lost-lord-01.md:89 — the Rugen alias + the Connington false-disgrace together sustain the deception. adwd-tyrion-06.md:113 — Aegon himself names the mechanism: "His father sold him to Lord Varys for a jug of Arbor gold… Varys gave the Pisswater boy to my lady mother and carried me away."
- **HIT/NEW-NODE**: HIT (both nodes). **NEW** edge.
- **Rationale**: Kevan represents the realm in this moment — he is the Lord Regent and the POV character receiving the revelation. `DECEIVES kevan-lannister` is load-bearing: it fires the counter-reveal (Kevan says "Dead. He's dead." / Varys says "No.") that is the emotional apex of the deception's exposure. The 15-year DECEIVES relationship is not currently in the graph. Existing `varys DECEIVES eddard-stark` is a *different* specific act (about the assassination cancel order). This one is specifically "Aegon is alive" — the arc's founding lie. Note: this edge is about the *concealment of the prince's survival* (on-page fact), NOT about whether Aegon is the real son of Rhaegar (GATED).
- **Qualifier**: Add `note: "Varys conceals Aegon's survival from the realm for 15+ years"` to distinguish from the eddard-stark DECEIVES.

---

### 4. varys MANIPULATES aegon-targaryen-young-griff
- **Source**: `varys` → **Type**: `MANIPULATES` → **Target**: `aegon-targaryen-young-griff`
- **Tier**: 2
- **Mechanism**: Varys shapes Aegon's entire education and worldview from birth — designing the prince as an instrument of restoration. Aegon is unknowingly the product of Varys's planning (not just raised by JonCon; Varys designed the curriculum).
- **Book / chapter-file:line**: ADWD, adwd-epilogue.md:297
- **Verbatim quote**: "Aegon has been shaped for rule since before he could walk. He has been trained in arms, as befits a knight to be, but that was not the end of his education. He reads and writes, he speaks several tongues, he has studied history and law and poetry. A septa has instructed him in the mysteries of the Faith since he was old enough to understand them. He has lived with fisherfolk, worked with his hands, swum in rivers and mended nets and learned to wash his own clothes at need."
- **HIT/NEW-NODE**: HIT (both nodes). **NEW** edge.
- **Rationale**: MANIPULATES = "target unknowingly used; note mechanism." Aegon does not know that Varys (not just JonCon) is the architect of his upbringing — the education plan is Varys's explicit design per the epilogue monologue. Tier-2 (we hear this from Varys's self-serving speech; the *degree* of Aegon's awareness of Varys's role is uncertain, but the manipulation is Tier-1 on-page). Different from `varys CONSPIRES_WITH illyrio` (that's a mutual partnership) — this is specifically a one-directional use of Aegon as an instrument.
- **Qualifier**: `note: "Varys designed Aegon's education to produce an ideal king; Aegon is the instrument, not a co-planner"`

---

### 5. varys AGENT_IN assassinations-of-pycelle-and-kevan-lannister (ALREADY EXISTS — verify)
- **Check**: `varys AGENT_IN assassinations-of-pycelle-and-kevan-lannister` — **ALREADY EXISTS** (confirmed in neighbors: `assassinations-of-pycelle-and-kevan-lannister` in AGENT_IN outgoing list, adwd-epilogue.md:277). **SKIP — DO NOT re-propose.**

---

### 6. varys CONSPIRES_WITH illyrio-mopatis (ALREADY EXISTS — verify)
- **Check**: Two `varys CONSPIRES_WITH illyrio-mopatis` edges exist (agot-arya-03.md:93; adwd-tyrion-06.md:113). **SKIP — DO NOT re-propose.**

---

### 7. jon-connington DECEIVES golden-company (re: his own identity)
- **Source**: `jon-connington` → **Type**: `DECEIVES` → **Target**: `golden-company`
- **Tier**: 1
- **What he deceives them about**: That he is "Griff," a sellsword; that he died a thief and a drunk (the Varys-fabricated cover). He conceals his true identity as Jon Connington, lord of Griffin's Roost.
- **Book / chapter-file:line**: ADWD, adwd-the-lost-lord-01.md:89
- **Verbatim quote**: "Even the men who'd ridden with him might not recognize the exile lord Jon Connington of the fiery red beard in the lined, clean-shaved face and dyed blue hair of the sellsword Griff. So far as most of them were concerned, Connington had drunk himself to death in Lys after being driven from the company in disgrace for stealing from the war chest."
- **HIT/NEW-NODE**: HIT (both nodes). **NEW** edge.
- **Rationale**: Varys fabricates the cover (`varys DECEIVES golden-company`, edge #2 above); Connington *enacts* it — he actively presents himself as Griff and maintains the lie. This is the *operational* deception, distinct from Varys's authorship. The fact that "most of them" believed Connington was dead is the practical effect. Connington has `SWORN_TO golden-company` (wiki) but no deception edge. DECEIVES is appropriate: deliberate misleading of the target. Tier-1.
- **Note**: DISTINGUISHABLE from Connington's self-deception/rationalization about Stoney Sept; this is outward, deliberate, 12-year concealment.

---

### 8. jon-connington DISGUISED_AS griff
- **Source**: `jon-connington` → **Type**: `DISGUISED_AS` → **Target**: `griff`
- **Tier**: 1
- **Book / chapter-file:line**: ADWD, adwd-the-lost-lord-01.md:61–63 and :89
- **Verbatim quote** (the disguise): "With his hair washed and cut and freshly dyed a deep, dark blue, his eyes looked blue as well." (This is Aegon's dye, but the *same passage* at :89 confirms Connington's disguise): "Griff wondered how many of them knew who he was. Few enough. Twelve years is a long time. Even the men who'd ridden with him might not recognize the exile lord Jon Connington of the fiery red beard in the lined, clean-shaved face and dyed blue hair of the sellsword Griff."
- **HIT/NEW-NODE**: `griff` — **CHECK NEEDED**. Griff is JonCon's alias name, not likely a separate node. If no `griff` node exists, this edge cannot be proposed as written. **ALTERNATIVE**: `jon-connington DISGUISED_AS undergaoler` is wrong (that's Varys). Better: use `jon-connington DECEIVES golden-company` (already proposed as #7) — that covers the practical effect. The DISGUISED_AS form presupposes a "griff" target node. **HOLD this edge pending slug check.**
- **Slug check required**: `python3 scripts/graph-query.py --neighbors griff` — if no node, drop this edge; #7 covers the substance.

---

### 9. jon-connington AFFLICTED_BY greyscale
- **Source**: `jon-connington` → **Type**: `AFFLICTED_BY` → **Target**: `greyscale`
- **Tier**: 1
- **Book / chapter-file:line**: ADWD, adwd-the-griffin-reborn-01.md:141
- **Verbatim quote**: "The nails on all four fingers were black now, though not yet on his thumb. On the middle finger, the grey had crept up past the second knuckle. I should hack them off, he thought, but how would I explain two missing fingers? He dare not let the greyscale become known."
- **Corroborating cite**: adwd-the-lost-lord-01.md:237 — "The nail on his middle finger had turned as black as jet … and the grey had crept up almost to the first knuckle. The tip of his ring finger had begun to darken too, and when he touched it with the point of his dagger, he felt nothing. Death, he knew, but slow. I still have time."
- **HIT/NEW-NODE**: HIT — `greyscale` node EXISTS (concept.medical, 0 edges). `jon-connington` EXISTS. **NEW** edge.
- **Rationale**: The most load-bearing character-condition in the arc. Connington's greyscale is why he cannot afford delay, why he hides the wine-soak ritual from his men, why he refuses marriage despite Haldon's suggestion ("Death is creeping up my arm. No man must ever know, nor any wife"), and why he insists on striking fast at Storm's End rather than waiting. AFFLICTED_BY is the correct type. The `greyscale` node has zero edges — this is a foundational wiring. Tier-1.

---

### 10. jon-connington DECEIVES golden-company (re: greyscale)
- **Source**: `jon-connington` → **Type**: `DECEIVES` → **Target**: `golden-company`
- **Tier**: 1
- **What he deceives about**: His greyscale infection — he hides it via wine-soaks (pretending to want the worst wine in the cellar) because men abandon greyscale companions even at battle's cost.
- **Book / chapter-file:line**: ADWD, adwd-the-griffin-reborn-01.md:141
- **Verbatim quote**: "He dare not let the greyscale become known. Queer as it seemed, men who would cheerfully face battle and risk death to rescue a companion would abandon that same companion in a heartbeat if he were known to have greyscale. I should have let the damned dwarf drown."
- **HIT/NEW-NODE**: HIT (both nodes). **NEW** edge.
- **Rationale**: This is a *separate* DECEIVES from edge #7 (the "Griff" identity deception). One deceives about his *identity*; this one deceives about his *physical condition*. Both are active, deliberate, ongoing concealments. Two distinct qualifier notes needed: "conceals identity as Jon Connington" vs "conceals greyscale infection." The graph can hold both. The cover mechanism (requesting the worst wine in the cellar for vinegar-soaks) is the specific lie-in-action: adwd-the-griffin-reborn-01.md:135 — "'Boiled eggs, fried bread, and beans. And a jug of wine. The worst wine in the cellar.' … asking for a jug of vinegar each morning would give the game away. Wine would need to serve."
- **Qualifier**: `note: "Conceals greyscale infection from the Golden Company via false wine-soak ritual; abandonment feared"`

---

### 11. greyscale MOTIVATES siege-of-storms-end-300
- **Source**: `greyscale` → **Type**: `MOTIVATES` → **Target**: `siege-of-storms-end-300`
- **Tier**: 1
- **Book / chapter-file:line**: ADWD, adwd-the-griffin-reborn-01.md:141 + adwd-the-lost-lord-01.md:21
- **Verbatim quote** (the explicit motivation link): adwd-the-lost-lord-01.md:21 — "I do not have time enough for caution." (Connington to Lemore)
- **Corroborating cite**: adwd-the-griffin-reborn-01.md:173 — "'We did not cross half the world to wait. Our best chance is to strike hard and fast, before King's Landing knows who we are. I mean to take Storm's End.'" (Connington overriding Strickland's caution)
- **HIT/NEW-NODE**: HIT (both nodes exist). **NEW** edge.
- **Rationale**: This is the LENS B's highest-value cross-node causal wiring: JonCon's greyscale death-clock is the direct cause of his haste, and his haste is what drives the Storm's End decision over Strickland's objection to wait. The link is explicit in the text: "I do not have time enough for caution." Without this edge, the *reason* for JonCon's aggression at Storm's End is invisible to the graph. This is an existing-node↔existing-node causal wiring (the highest priority category). Tier-1.

---

### 12. jon-connington AGENT_IN aegon-revealed-to-the-golden-company
- **Source**: `jon-connington` → **Type**: `AGENT_IN` → **Target**: `aegon-revealed-to-the-golden-company`
- **Tier**: 1
- **Book / chapter-file:line**: ADWD, adwd-the-lost-lord-01.md:127
- **Verbatim quote**: "My lords, I give you Aegon Targaryen, firstborn son of Rhaegar, Prince of Dragonstone, by Princess Elia of Dorne … soon, with your help, to be Aegon, the Sixth of His Name, King of Andals, the Rhoynar, and the First Men, and Lord of the Seven Kingdoms."
- **HIT/NEW-NODE**: HIT (`jon-connington` exists; `aegon-revealed-to-the-golden-company` — **check if built in S128**). Per baseline.md, this node EXISTS as of S128. NEW edge.
- **Rationale**: JonCon performs the reveal; he is the single agent who speaks Aegon's true name to the war council. This is the pivotal moment his 15 years of concealment ends (he ends the deception he and Varys maintained). AGENT_IN correctly captures his primary role in the event. The event node currently has `varys MOTIVATES` and `exile-of-jon-connington ENABLES` wired, but JonCon as AGENT_IN is missing (per baseline.md gap table: "jon-con AGENT_IN absent").

---

### 13. varys REVEALS_TO kevan-lannister (Aegon's survival)
- **Source**: `varys` → **Type**: `REVEALS_TO` → **Target**: `kevan-lannister`
- **Tier**: 1
- **What is revealed**: That Aegon Targaryen survived the Sack of KL and is now raising banners at Storm's End
- **Book / chapter-file:line**: ADWD, adwd-epilogue.md:293–297
- **Verbatim quote**: "'Aegon?' For a moment he did not understand. Then he remembered. A babe swaddled in a crimson cloak, the cloth stained with his blood and brains. 'Dead. He's dead.' 'No.' The eunuch's voice seemed deeper. 'He is here. Aegon has been shaped for rule since before he could walk…'"
- **HIT/NEW-NODE**: HIT (both nodes). **NEW** edge.
- **Rationale**: The revelation to Kevan is a discrete, load-bearing event — Varys chooses to *tell* Kevan the truth about Aegon as Kevan is dying. This is the only moment in the text where the 15-year concealment is explicitly lifted to a named Westerosi character. REVEALS_TO is the correct type. Note the poignancy: Varys reveals it to the one man who can no longer act on it. The reveal SERVES the deception's purposes (Kevan is told only when it cannot harm the plan). This edge is distinct from `varys DECEIVES kevan-lannister` (#3, the 15-year lie) — #3 is the ongoing state, #13 is the terminal lift.
- **Qualifier**: `note: "Reveals Aegon's survival to Kevan as Kevan dies from the crossbow bolt; Kevan cannot act on the knowledge"`

---

### 14. tyrion-lannister MANIPULATES aegon-targaryen-young-griff (the "sail west" goad)
- **Source**: `tyrion-lannister` → **Type**: `MANIPULATES` → **Target**: `aegon-targaryen-young-griff`
- **Tier**: 2
- **Mechanism**: Tyrion uses cyvasse as a frame to goad Aegon into abandoning Varys's original plan (wait for Dany) and sailing west immediately. The board game is the manipulation vehicle; the "trust no one" lesson is the cover.
- **Book / chapter-file:line**: ADWD, adwd-tyrion-06.md:131–147
- **Verbatim quote**: "Still, I'd do things differently… If I were you? I would go west instead of east. Land in Dorne and raise my banners… I told you, I know our little queen. Let her hear that her brother Rhaegar's murdered son is still alive, that this brave boy has raised the dragon standard… she will fly to your side as fast as wind and water can carry her." Then: "I lied. Trust no one. And keep your dragon close." (line 155)
- **HIT/NEW-NODE**: HIT (both nodes). **NEW** edge.
- **Rationale**: Tyrion *explicitly* manipulates Aegon, and the text makes this unambiguous — he says "I lied" about the cyvasse move, and the structural parallel is clear: he lied about "don't bring out your dragon too soon" to goad Aegon into doing exactly that (committing the fleet west). `tyrion-lannister MOTIVATES golden-company-sails-for-westeros` ALREADY EXISTS (per baseline.md — "tyrion-lannister MOTIVATES golden-company-sails-for-westeros" in the spine). The *mechanism* of how Tyrion motivates it is MANIPULATES, targeting Aegon specifically. These are complementary, not redundant: the event-level edge (Tyrion MOTIVATES the sailing) is built; the character-level manipulation (how Tyrion moved Aegon) is dark. Tier-2 because Tyrion's ultimate motives for doing this are unclear (does he believe it's right? Is he serving Varys's plan? Is he serving himself?). The manipulation itself is Tier-1 on-page.

---

## Proposed nodes

None. All target entities above exist in the graph. The `griff` slug (edge #8) requires a verify-before-build check; if no `griff` node, drop #8 entirely.

---

## Dropped / considered-but-no

### Theory-gate holds (correctly held)
1. **Aegon's identity / "mummer's dragon" / babe-swap** — NOT proposed. Aegon's claim to be Rhaegar's true son is explicitly the GATED Blackfyre/fAegon theory. Edge #3 (`varys DECEIVES kevan-lannister`) is specifically about the *survival* of the claimant (on-page fact), NOT about whether the claimant is the real son of Rhaegar. The distinction is maintained throughout. All edges target `aegon-targaryen-young-griff` (the claimant), never asserting identity with `aegon-targaryen-son-of-rhaegar` (the historical infant). ✓

2. **SUSPECTED_OF targeting Aegon's identity** — NOT proposed. SUSPECTED_OF is reserved for on-page doubt about a CHARACTER's agency over an EVENT — not for identity questions. Aegon's identity doubt stays in harvest as theory-gated quotes. ✓

3. **R+L, Azor Ahai, Euron↔Bloodraven** — Not touched. ✓

### Considered but dropped for substantive reasons

4. **varys CONSPIRES_WITH illyrio-mopatis (re: Aegon)** — ALREADY EXISTS (×2 edges with different cite refs). Correctly deduped. Dropped.

5. **varys AGENT_IN assassinations-of-pycelle-and-kevan-lannister** — ALREADY EXISTS. Dropped.

6. **varys KILLS kevan-lannister / pycelle** — ALREADY EXISTS. Dropped.

7. **Strickland IGNORANT_OF (Aegon's identity)** — The baseline notes Strickland knew *before* the reveal (adwd-the-lost-lord-01.md:129 — "When did you tell them?" / Strickland: "When we reached the river"). He was not ignorant by the time of the reveal. The other GC officers were also told in advance. No clean IGNORANT_OF edge possible without overclaiming.

8. **harry-strickland DECEIVES aegon / prevents / obstructs** — Strickland's reluctance is not deception; he openly argues for delay. Dropping; no hidden-agency element.

9. **illyrio-mopatis DECEIVES golden-company** — Possible (Illyrio sends the GC on a mission whose full purpose they don't know), but the existing `illyrio-mopatis CONSPIRES_WITH varys` (×2) covers the conspiracy's mutual structure, and the specific text this would cite is mediated through JonCon's resentment of the "fat man's pipes." Illyrio is not a POV character; the deception-of-the-GC is attributed primarily to the Varys/JonCon axis in the chapters read. Deferred rather than NO: would require ACOK/AGOT tunnel scenes or Tyrion-02 more carefully read. Parking here.

10. **jon-connington DISGUISED_AS griff (edge #8)** — HELD pending slug check. If `griff` node does not exist, the edge cannot be built. `jon-connington DECEIVES golden-company` (#7) covers the substance.

11. **varys DISGUISED_AS undergaoler** — CONSIDERED but WRONG TYPE. Varys did not wear a costume as "Undergaoler" in the way he wears wigs or fat-suits in other contexts. He *was* the undergaoler — he held the title. HOLDS_TITLE (already in graph) is correct; DISGUISED_AS would assert a physical disguise layer not evidenced in these chapters. Drop.

12. **kevan-lannister IGNORANT_OF (Aegon's survival)** — Technically true for 15 years, but the more load-bearing edge is the REVEALS_TO (#13) which captures the terminal moment of that ignorance. Redundant once #13 exists.

---

## Harvest

### Verbatim quotes for graph attachment

| kind | book | chapter-file:line | verbatim quote | target node | note |
|------|------|-------------------|----------------|-------------|------|
| quote | ADWD | adwd-epilogue.md:281 | "Ser Kevan. Forgive me if you can. I bear you no ill will. This was not done from malice. It was for the realm. For the children." | `assassinations-of-pycelle-and-kevan-lannister` / `varys` | Core AGENT_IN evidence; already built edge, attach quote |
| quote | ADWD | adwd-epilogue.md:293 | "Doubt, division, and mistrust will eat the very ground beneath your boy king, whilst Aegon raises his banner above Storm's End and the lords of the realm gather round him." | `assassinations-of-pycelle-and-kevan-lannister` (MOTIVATES evidence) | Already in harvest-queue (S128); confirm attached |
| quote | ADWD | adwd-epilogue.md:285 | "you were threatening to undo all the queen's good work, to reconcile Highgarden and Casterly Rock, bind the Faith to your little king, unite the Seven Kingdoms under Tommen's rule. So …" | `assassinations-of-pycelle-and-kevan-lannister` / `kevan-lannister` | Varys's explicit statement of WHAT Kevan was doing that had to stop; the strategic rationale for the murder |
| quote | ADWD | adwd-epilogue.md:297 | "Aegon has been shaped for rule since before he could walk. He has been trained in arms … He has lived with fisherfolk, worked with his hands, swum in rivers and mended nets and learned to wash his own clothes at need. He can fish and cook and bind up a wound, he knows what it is like to be hungry, to be hunted, to be afraid. Tommen has been taught that kingship is his right. Aegon knows that kingship is his duty, that a king must put his people first, and live and rule for them." | `aegon-targaryen-young-griff` node ## Quotes | Varys's design-of-a-king speech; Tier-1 character-shaping evidence |
| quote | ADWD | adwd-the-lost-lord-01.md:89 | "'We want no songs about the gallant exile,' the eunuch had tittered, in that mincing voice of his. 'Those who die heroic deaths are long remembered, thieves and drunks and cravens soon forgotten.'" | `varys` / `jon-connington` | Evidence for the Varys DECEIVES GC edge; voice quote for varys |
| quote | ADWD | adwd-the-lost-lord-01.md:91 | "Let me live long enough to see the boy sit the Iron Throne, and Varys will pay for that slight and so much more." | `jon-connington` node ## Quotes | JonCon's resentment of Varys; already RESENTS varys edge — attach quote to it |
| description | ADWD | adwd-the-griffin-reborn-01.md:141 | "The nails on all four fingers were black now, though not yet on his thumb. On the middle finger, the grey had crept up past the second knuckle. I should hack them off, he thought, but how would I explain two missing fingers? He dare not let the greyscale become known." | `jon-connington` + `greyscale` | Evidence for AFFLICTED_BY greyscale (edge #9); physical description |
| food + description | ADWD | adwd-the-griffin-reborn-01.md:135 | "'Boiled eggs, fried bread, and beans. And a jug of wine. The worst wine in the cellar.' … When the food and wine had been brought up, he barred the door, emptied the jug into a bowl, and soaked his hand in it. Vinegar soaks and vinegar baths were the treatment Lady Lemore had prescribed for the dwarf… asking for a jug of vinegar each morning would give the game away." | `jon-connington` / `greyscale` / food register | FOOD first-class. The false food-request is the greyscale-concealment mechanism; hospitality register (breaking fast at reclaimed Griffin's Roost) + medical detail |
| quote | ADWD | adwd-tyrion-06.md:113 | "That was some tanner's son from Pisswater Bend whose mother died birthing him. His father sold him to Lord Varys for a jug of Arbor gold. He had other sons but had never tasted Arbor gold. Varys gave the Pisswater boy to my lady mother and carried me away." | `aegon-targaryen-young-griff` / `varys` | Aegon recounts the babe-swap story himself (on-page, his own words) — PARK as theory-gated? NO — this is Aegon's BELIEF, not the novel asserting it as fact. Keep as evidence for DECEIVES edges; flag as theory-adjacent |
| quote | ADWD | adwd-tyrion-06.md:115 | "the eunuch smuggled you across the narrow sea to his fat friend the cheesemonger, who hid you on a poleboat and found an exile lord willing to call himself your father" | `varys` / `illyrio-mopatis` / `jon-connington` | Tyrion's summary of the conspiracy's operational structure; good evidence for CONSPIRES_WITH dyad (already built) |
| description | ADWD | adwd-the-lost-lord-01.md:61 | "With his hair washed and cut and freshly dyed a deep, dark blue, his eyes looked blue as well. At his throat he wore three huge square-cut rubies on a chain of black iron, a gift from Magister Illyrio. Red and black. Dragon colors." | `aegon-targaryen-young-griff` | Physical description (Illyrio's rubies; blue dye disguise); already in harvest-queue S128 — confirm |
| quote | ADWD | adwd-epilogue.md:303–305 | "A child emerged from a pool of darkness, a pale boy in a ragged robe, no more than nine or ten. Another rose up behind the Grand Maester's chair. The girl who had opened the door for him was there as well. They were all around him, half a dozen of them, white-faced children with dark eyes, boys and girls together. And in their hands, the daggers." | `assassinations-of-pycelle-and-kevan-lannister` | The little-birds / children as instruments of the assassination; Varys's COMMANDS-little-birds is partially in graph (varys COMMANDS little-matt — but little-matt is misidentified as a riverlands character). The unnamed children here are Varys's network; no existing node to attach to cleanly |
| description | ADWD | adwd-epilogue.md:257 | "The door was opened by a serving girl, a skinny thing in a fur-lined robe much too big for her. Ser Kevan stamped the snow off his boots, removed his cloak, tossed it to her. 'The Grand Maester is expecting me,' he announced. The girl nodded, solemn and silent, and pointed to the steps." | `assassinations-of-pycelle-and-kevan-lannister` | One of the little-birds disguised as a serving girl — the operational infiltration; striking description |
| foreshadowing | ADWD | adwd-tyrion-06.md:131 | "Trust no one, my prince. Not your chainless maester, not your false father, not the gallant Duck nor the lovely Lemore nor these other fine friends who grew you from a bean. Above all, trust not the cheesemonger, nor the Spider, nor this little dragon queen you mean to marry." | `aegon-targaryen-young-griff` | Tyrion's ironic foreshadowing — he tells Aegon the TRUTH (not to trust Varys/Illyrio) while simultaneously manipulating him into the very course those conspirators planned |
| description | ADWD | adwd-the-lost-lord-01.md:125 | "Varys had been adamant about the need for secrecy. The plans that he and Illyrio had made with Blackheart had been known to them alone. The rest of the company had been left ignorant. What they did not know they could not let slip." | `varys` / `illyrio-mopatis` / `golden-company` | Explicit statement of the operational compartmentalization; evidence for DECEIVES GC edges |

---

### Theory-gated (parked)

These quotes capture the on-page identity doubt but assert NOTHING as graph edges. Park for the theories track.

| kind | book | chapter-file:line | verbatim quote | gated theory | note |
|------|------|-------------------|----------------|--------------|------|
| quote (GATED) | ADWD | adwd-tyrion-06.md:113 | "That was some tanner's son from Pisswater Bend whose mother died birthing him. His father sold him to Lord Varys for a jug of Arbor gold. He had other sons but had never tasted Arbor gold. Varys gave the Pisswater boy to my lady mother and carried me away." | fAegon babe-swap / Young Griff identity | Aegon believes/asserts this himself — weight = Tier-3 (single POV statement of unknown reliability). Theory track: is Aegon really Elia's son? |
| quote (GATED) | ADWD | adwd-tyrion-06.md:123 | "Good morrow to you, Auntie. I am your nephew, Aegon, returned from the dead. I've been hiding on a poleboat all my life, but now I've washed the blue dye from my hair and I'd like a dragon, please … and oh, did I mention, my claim to the Iron Throne is stronger than your own?" | fAegon / "mummer's dragon" | Tyrion's mockery encapsulates both the cover story AND the in-world skepticism — the "mummer's dragon" question in miniature. DO NOT graph as SUSPECTED_OF; theory only. |
| quote (GATED) | ADWD | adwd-epilogue.md:67 | "None of us looked long. Tywin said that it was Prince Aegon, and we took him at his word." | fAegon / babe-swap | Kevan's memory: the body identification was never verified — Tywin's say-so only. Key evidence for the babe-swap theory. Theory track. |
| quote (GATED) | ADWD | adwd-tyrion-06.md:131 | "trust not the cheesemonger, nor the Spider … All that mistrust will sour your stomach and keep you awake by night, 'tis true, but better that than the long sleep that does not end." | fAegon / Varys's true motives | Tyrion's warning is consistent with the reading that Varys/Illyrio are using Aegon as a tool (possibly as a Blackfyre pawn). Gated — stays as foreshadowing only. |
