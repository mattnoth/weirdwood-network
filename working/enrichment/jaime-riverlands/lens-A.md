# Lens A — Spine + Secondary Character Sub-Arcs — A2.6 Jaime / Riverlands proposal (S159)

Chapters read in full: affc-jaime-04, affc-jaime-05, affc-jaime-06, affc-jaime-07. Also skimmed
affc-jaime-01 (Oathkeeper / vigil) and affc-jaime-02 (march context). Dedup verified against
edges.jsonl (siege-of-riverrun hub: 13+ in-edges confirmed; emmon-frey HOLDS_TITLE lord-of-riverrun
confirmed live; addam-marbrand has infobox-only edges, no event-role edges in current graph).

---

## Proposed NEW nodes

### 1. `edmure-yields-riverrun`
- **type:** event.incident
- **body:** Edmure Tully, after being privately coerced by Jaime's trebuchet threat (affc-jaime-06),
  hauls down the direwolf of Stark in token of surrender on the next day, opening Riverrun's gates
  bloodlessly. The castle passes to Emmon Frey and the crown's forces. This is the resolution beat
  of the siege-of-riverrun hub, which currently has cOut=0.
- **anchor quote:** "Edmure had waited most of the day before hauling down the direwolf of Stark in
  token of surrender." — affc-jaime-07:39

### 2. `blackfish-escapes-riverrun`
- **type:** event.incident
- **body:** Brynden "the Blackfish" Tully, rather than yield to the conquerors, slips under the
  Water Gate boom in the dark and swims downriver alone. He is never recaptured in the published
  books. The escape occurs simultaneously with the castle changing hands and is not known to Jaime
  until the following morning.
- **anchor quote:** "a black fish in a black river floating quietly downstream" — affc-jaime-07:39

### 3. `jaime-burns-cerseis-letter`
- **type:** event.incident
- **body:** At Riverrun after the siege, Jaime receives a snow-day letter from Cersei (delivered by
  Vyman the maester): Qyburn's terse cover note + Cersei's fervent plea "Come at once. Help me.
  Save me. I need you now as I have never needed you before. I love you." Without sending any reply,
  Jaime hands the letter to Peck and says "Put this in the fire." The marquee Jaime↔Cersei rupture
  in AFFC.
- **anchor quote:** "Put this in the fire." — affc-jaime-07:295

### 4. `jaime-coerces-edmure-with-trebuchet-threat`
- **type:** event.incident
- **body:** In his tent at Riverrun, Jaime privately tells Edmure (who has just been freed from
  Ryman Frey's gallows) that unless he yields the castle, Jaime will trebuchet Edmure's unborn child
  into the keep. The scene is witnessed by Peck, Pia, and a singer (Ryman's old harper). This is
  the mechanistic cause of edmure-yields-riverrun.
- **anchor quote:** "You'll want your child, I expect. I'll send him to you when he's born. With a
  trebuchet." — affc-jaime-06:325

---

## Proposed NEW edges

### Edges for `edmure-yields-riverrun`

| source | edge | target | Tier | qualifier | quote + cite | rationale |
|--------|------|--------|------|-----------|-------------|-----------|
| edmure-tully | AGENT_IN | edmure-yields-riverrun | 1 | — | "hauling down the direwolf of Stark in token of surrender" affc-jaime-07:39 | Edmure performs the act |
| jaime-lannister | COMMANDS_IN | edmure-yields-riverrun | 1 | — | "You required me to surrender my castle, not my uncle." affc-jaime-07:21 | Jaime as commander who produced the surrender |
| edmure-yields-riverrun | LOCATED_AT | riverrun | 1 | — | "hauling down the direwolf of Stark in token of surrender" affc-jaime-07:39 | Castle is the locus |
| edmure-yields-riverrun | SUB_BEAT_OF | siege-of-riverrun | 1 | — | "hauling down the direwolf of Stark in token of surrender" affc-jaime-07:39 | The surrender is the resolution beat of the siege |
| jaime-coerces-edmure-with-trebuchet-threat | ENABLES | edmure-yields-riverrun | 1 | — | "You'll want your child, I expect. I'll send him to you when he's born. With a trebuchet." affc-jaime-06:325 | The coercion is the precondition; Edmure still makes the choice |
| jaime-coerces-edmure-with-trebuchet-threat | MOTIVATES | edmure-tully | 1 | — | "You'll want your child, I expect. I'll send him to you when he's born. With a trebuchet." affc-jaime-06:325 | Routes Edmure's decision through MOTIVATES→character per ENABLES contract |
| edmure-yields-riverrun | ENABLES | jaime-orders-siege-equipment-and-gallows-burned | 2 | — | "By the next morning little remained of the Frey encampment but flies, horse dung, and Ser Ryman's gallows" affc-jaime-07:167 | Surrender precondition for the post-siege dismantling order — causal in-edge that lights the currently islanded gallows-burned node |

### Edges for `blackfish-escapes-riverrun`

| source | edge | target | Tier | qualifier | quote + cite | rationale |
|--------|------|--------|------|-----------|-------------|-----------|
| brynden-tully | AGENT_IN | blackfish-escapes-riverrun | 1 | — | "a black fish in a black river floating quietly downstream" affc-jaime-07:39 | He performs the escape |
| blackfish-escapes-riverrun | LOCATED_AT | riverrun | 1 | — | "a black fish in a black river floating quietly downstream" affc-jaime-07:39 | Originates at Riverrun |
| blackfish-escapes-riverrun | SUB_BEAT_OF | siege-of-riverrun | 1 | — | "it had been the next morning before Jaime had been informed that the Blackfish was not amongst the prisoners" affc-jaime-07:39 | Occurs during the castle changing hands |
| edmure-yields-riverrun | ENABLES | blackfish-escapes-riverrun | 1 | — | "In the confusion of the castle changing hands, it had been the next morning before Jaime had been informed that the Blackfish was not amongst the prisoners." affc-jaime-07:39 | The surrender creates the confusion that masks the escape — precondition, not cause |
| addam-marbrand | PARTICIPATES_IN | blackfish-escapes-riverrun | 1 | — | "Ser Addam Marbrand was leading the search on the south side of the river" affc-jaime-07:45 | Addam leads the post-escape search; first book-cited event-role edge for this node |

### Edges for `jaime-burns-cerseis-letter`

| source | edge | target | Tier | qualifier | quote + cite | rationale |
|--------|------|--------|------|-----------|-------------|-----------|
| jaime-lannister | AGENT_IN | jaime-burns-cerseis-letter | 1 | — | "Put this in the fire." affc-jaime-07:295 | Jaime issues the order; the rupture is his act |
| cersei-lannister | VICTIM_IN | jaime-burns-cerseis-letter | 1 | — | "Come at once, she said. Help me. Save me." affc-jaime-07:291 | Her plea is refused and destroyed |
| jaime-burns-cerseis-letter | LOCATED_AT | riverrun | 1 | — | "He read it in the window seat" affc-jaime-07:291 | Occurs at Riverrun castle |
| edmure-yields-riverrun | ENABLES | jaime-burns-cerseis-letter | 2 | — | "He read it in the window seat, bathed in the light of that cold white morning." affc-jaime-07:291 | Siege must end first (Jaime stays at Riverrun after surrender); structural precondition |
| jaime-burns-cerseis-letter | MOTIVATES | jaime-lannister | 1 | — | "Put this in the fire." affc-jaime-07:295 | **[BORDERLINE]** The burning is an act expressing a decision — the MOTIVATES runs from the refusal-event back to Jaime's ongoing character arc; reviewers may prefer to represent this purely as AGENT_IN without a reflexive edge. Flagged for gate. |

### Edges for `jaime-coerces-edmure-with-trebuchet-threat`

| source | edge | target | Tier | qualifier | quote + cite | rationale |
|--------|------|--------|------|-----------|-------------|-----------|
| jaime-lannister | AGENT_IN | jaime-coerces-edmure-with-trebuchet-threat | 1 | — | "You'll want your child, I expect. I'll send him to you when he's born. With a trebuchet." affc-jaime-06:325 | Jaime delivers the threat |
| edmure-tully | VICTIM_IN | jaime-coerces-edmure-with-trebuchet-threat | 1 | — | "You'll want your child, I expect. I'll send him to you when he's born. With a trebuchet." affc-jaime-06:325 | Edmure is the direct recipient |
| jaime-lannister | MANIPULATES | edmure-tully | 1 | via_threat | "You'll want your child, I expect. I'll send him to you when he's born. With a trebuchet." affc-jaime-06:325 | Jaime uses Edmure's unborn child as leverage to extract the surrender; `via_threat` is the explicit qualifier; text fully supports it |
| jaime-coerces-edmure-with-trebuchet-threat | LOCATED_AT | riverrun | 1 | — | "Pia was standing by the flap of the tent with her arms full of clothes." affc-jaime-06:325 | Occurs in Jaime's pavilion in the siege camp at Riverrun |
| siege-of-riverrun | ENABLES | jaime-coerces-edmure-with-trebuchet-threat | 2 | — | "You've seen our numbers, Edmure. You've seen the ladders, the towers, the trebuchets, the rams." affc-jaime-06:325 | The siege position (trebuchets, overwhelming force) is the context that makes the threat credible |

### Secondary-cast edges lighting islanded hubs

| source | edge | target | Tier | qualifier | quote + cite | rationale |
|--------|------|--------|------|-----------|-------------|-----------|
| karyl-vance | PARTICIPATES_IN | siege-of-riverrun | 1 | — | "Lord Piper and both Lords Vance came to speak for the repentant lords of the Trident, whose loyalties would shortly be put to the test." affc-jaime-06:131 | Karyl Vance as riverlord participating in the war council; no existing event-role edge for this node |
| clement-piper | PARTICIPATES_IN | siege-of-riverrun | 1 | — | "Lord Piper and both Lords Vance came to speak for the repentant lords of the Trident" affc-jaime-06:131 | Lord Piper attends war council; lights his node |
| addam-marbrand | COMMANDS_IN | siege-of-riverrun | 1 | — | "Ser Addam, inspect our perimeter with an eye for any weaknesses." affc-jaime-05:179 | Addam has perimeter/scout command under Jaime; no existing COMMANDS_IN for this node |
| genna-lannister | PARTICIPATES_IN | siege-of-riverrun | 1 | — | "Lord Emmon Frey joined them, with his wife. Lady Genna claimed her stool with a look that dared any man there to question her presence. None did." affc-jaime-06:131 | Lady Genna is present as a principal at the war council — this edge should already exist from the historical-anchor run; flagged as **[BORDERLINE]** dedup risk — verify before minting. |

### Causal wiring: Ryman Frey dismissed → hanged

| source | edge | target | Tier | qualifier | quote + cite | rationale |
|--------|------|--------|------|-----------|-------------|-----------|
| jaime-orders-siege-equipment-and-gallows-burned | PRECEDES | ryman-frey-is-hanged | **[BORDERLINE — no node exists for ryman's hanging]** | — | This is a TWOW-adjacent event that occurs AFTER the affc-jaime-07 chapters; Ryman is hanged off-page by the Brotherhood. Flagging only; do not mint unless Lens B/C/D confirm the node exists. |

---

## Dropped / considered-but-rejected

1. **`genna-lannister PARTICIPATES_IN siege-of-riverrun`** — The historical-anchor run (w1) almost certainly already emitted this; the quote at affc-jaime-06:131 ("Lord Emmon Frey joined them, with his wife") was also used for emmon-frey's PARTICIPATES_IN. Kept it as BORDERLINE above but would not be surprised if this is a dedup kill.

2. **`emmon-frey RULES riverrun`** — baseline.md notes this exists; confirmed via `emmon-frey HOLDS_TITLE lord-of-riverrun` (wiki-infobox, live). Do not re-propose. A book-cited HOLDS_TITLE with qualifier `current` from affc-jaime-07:53 ("Riverrun is mine") would be novel evidence-quality, but the edge already exists. Skip.

3. **`edwyn-frey COMMANDS_IN siege-of-riverrun`** — Edwyn inherits Ryman's command post-dismissal (affc-jaime-06:279 "I am giving you your father's command"), but `edwyn-frey PARTICIPATES_IN siege-of-riverrun` already exists from the historical-anchor run. Upgrading PARTICIPATES_IN to COMMANDS_IN would require the orchestrator to overwrite; flagged here as a note but not a new edge.

4. **`jaime-lannister MANIPULATES ryman-frey`** — Jaime hits Ryman and dismisses him (affc-jaime-06:259 "Jaime hit him"). That is ASSAULTS, not MANIPULATES, and the dyad ASSAULTS edge between jaime and ryman-frey may already exist. The dismissal is administrative, not manipulation-via-tool. Dropped.

5. **`daven-lannister COMMANDS_IN siege-of-riverrun`** — already exists (confirmed in edges.jsonl). Dropped.

6. **Blackfish SUSPECTED_OF aided by riverlords** — affc-jaime-07:45 "Vance and Piper and their ilk were more like to help the Blackfish escape than clap him into fetters." This is Jaime's suspicion, not text-proven. The SUSPECTED_OF edge type is Tier-2, never Tier-1. Could propose `karyl-vance SUSPECTED_OF blackfish-escapes-riverrun` but the text framing is general ("their ilk") not specific; the inference is too diffuse to justify a named suspect edge on a single character. Dropped.

7. **Harrenhal command edges** — affc-jaime-03/04 covers Jaime at Harrenhal restoring order (Pia's situation, Lorch beheading). Baseline DO-NOT explicitly says "Touch Harrenhal only for Jaime's command tenure if a clean book-cited edge exists; do NOT re-cut the tangle." No clean new causal edge exists that would not re-engage the tangle. Dropped entirely.

8. **`jaime-lannister BREAKS_VOW`** — Jaime references his oath to Catelyn not to fight Tullys/Starks multiple times (affc-jaime-06:105 "When Lady Catelyn freed me, she made me swear not to take arms again against the Starks or Tullys"). He resolves the siege without personally taking up arms. Whether he "broke" the vow is interpretive and theory-adjacent. Dropped.

9. **`jaime-burns-cerseis-letter MOTIVATES jaime-lannister` (reflexive)** — flagged as BORDERLINE above. The burning event expresses a state of motivation but a MOTIVATES edge from event→character where the character both agents and is motivated is unusual schema-wise. Gate should decide.

10. **Tom of Sevenstreams** — appears at affc-jaime-07 (singer, former Ryman Frey's man, stays at Riverrun for Lady Genna). He is a character node but his role is non-causal ambient here; no new structural edges that aren't just ATTENDS-level. Dropped for this lens.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|-------------|------|
| food | AFFC | affc-jaime-06:309 | Jaime orders wine and food for Edmure in the bath: "Peck, wine for Lord Tully. Are you hungry, my lord?" — hospitality scene in the siege camp |
| food | AFFC | affc-jaime-06:309 | "Little Lew hollowed out a loaf of stale bread to make a trencher" — camp provisioning detail |
| food | AFFC | affc-jaime-05:161 | "He's even got himself a bloody singer. Our aunt brought Whitesmile Wat from Lannisport" / "Ryman Frey's great rectangular pavilion" with sounds of drinking — siege-camp feast/wine culture |
| food | AFFC | affc-jaime-05:113 | "So long as there are fish in the rivers, we won't starve" — siege provisioning; nets set for fish in Red Fork / Tumblestone |
| food | AFFC | affc-jaime-07:49 | "the Blackfish had left Riverrun amply provisioned, just as he had claimed" — Blackfish's defensive provisioning strategy |
| food | AFFC | affc-jaime-04:111 | feast at Darry: "bean-and-bacon soup", "river pike baked in a crust of herbs and crushed nuts", "venison to come, and capons stuffed with leeks and mushrooms" — detailed course menu |
| food | AFFC | affc-jaime-04:213 | "fat sausages spit and sizzle above the flames" — sparrows' cookfire meal at Darry yard |
| food | AFFC | affc-jaime-05:147 | river scene: crossbowmen share a hare with Jaime at cookfire — field-life food |
| food | AFFC | affc-jaime-06:93 | "We came on some, the day before last" (hanged men, stripped, crabapples in mouths) — dark counterpoint to food: outlaws' message-bodies |
| quote | AFFC | affc-jaime-07:291 | Load-bearing verbatim: "Come at once, she said. Help me. Save me. I need you now as I have never needed you before. I love you. I love you. I love you. Come at once." — Cersei's letter; for cersei-lannister node ## Quotes |
| quote | AFFC | affc-jaime-07:295 | "A snowflake landed on the letter. As it melted, the ink began to blur." — physical description of the burning-letter moment; for jaime-burns-cerseis-letter node body |
| quote | AFFC | affc-jaime-06:325 | "With a trebuchet." — standalone line after threat speech; marquee quote for jaime-coerces-edmure-with-trebuchet-threat node |
| description | AFFC | affc-jaime-05:157 | "Riverrun, rising from the narrow point where the Tumblestone joined the Red Fork. The Tully castle looked like a great stone ship with its prow pointed downriver." — canonical physical description for riverrun node ## Description |
| description | AFFC | affc-jaime-06:11 | Brynden Tully at the drawbridge: "His ringmail was grim and grey. Over it he wore greaves, gorget, gauntlets, pauldron, and poleyns of blackened steel" + "brooch that fastened Ser Brynden Tully's cloak was a black fish, wrought in jet and gold" — physical description for brynden-tully node |
| description | AFFC | affc-jaime-07:279 | "The yard below was covered by a thin white blanket, growing thicker even as he watched. The merlons on the battlements wore white cowls." — first-snow-in-the-riverlands atmospheric detail; connects to winter's arrival sub-theme |
| description | AFFC | affc-jaime-05:162 | Siege logistics: "We've thrown a boom across the Red Fork, downstream of the castle. Manfryd Yew and Raynard Ruttiger have charge of its defense" — the boom across the Red Fork; relevant to blackfish-escape method |
| foreshadowing | AFFC | affc-jaime-07:249 | Jaime dreams of a silent sister with Joanna Lannister's face in the Great Sept; affc-jaime-07:265–267 (the stump / "Count your hands, child") — potential foreshadowing / Joanna ghost appearance; for foreshadowing pass |
| description | AFFC | affc-jaime-07:173 | "Come, let's drink some more of Hoster Tully's good red wine" — wine ritual with Ser Ilyn; Hoster's wine cellar now Jaime's; hospitality/trophy detail |
