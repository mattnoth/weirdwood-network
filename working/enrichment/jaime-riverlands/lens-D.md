# Lens D — Existing-Node↔Existing-Node Causal Wiring — A2.6 Jaime / Riverlands proposal (S159)

Lens D: cross-arc seam causal wiring. Targets: (1) siege-of-riverrun resolution spine (cOut=0);
(2) Cersei-letter rupture (cross-arc to Cersei's-downfall); (3) WO5K-board seam.
All three AFFC Jaime chapters read in full (affc-jaime-05, -06, -07).

---

## Proposed NEW nodes

*Note: The three marquee event nodes (`edmure-yields-riverrun`, `blackfish-escapes-riverrun`,
`jaime-burns-cerseis-letter`) are Lens A mints per the shared brief. Lens D references them as
targets/sources and marks all edges on them as **[depends-on-Lens-A-mint]**.*

---

## Proposed NEW edges

### 1 — Riverrun-siege resolution spine

**1a.** siege-of-riverrun ENABLES edmure-yields-riverrun | Tier-2 | [depends-on-Lens-A-mint] |
"In the confusion of the castle changing hands, it had been the next morning before Jaime had been
informed that the Blackfish was not amongst the prisoners." affc-jaime-07:39 |
The siege is the structural precondition for the surrender — without the encirclement, coercion,
and supply pressure the yield event cannot occur. ENABLES (not CAUSES) because Edmure's free
decision to open the gates is the proximate act.

**1b.** jaime-lannister MOTIVATES edmure-tully | Tier-1 | qualifier: via_threat |
"I'll send him to you when he's born. With a trebuchet." affc-jaime-06:325 |
The trebuchet-threat against Edmure's unborn child is what breaks Edmure's resistance and produces
the surrender decision. MOTIVATES (→character) correctly routes the human choice. This is distinct
from and complements any MANIPULATES edge Lens A/B might propose.

*Note: if another lens already proposes `jaime-lannister MANIPULATES edmure-tully via_threat`,
this MOTIVATES edge is still valid — MANIPULATES describes Jaime's tactic, MOTIVATES describes
the causal direction on Edmure's decision. Both can coexist.*

**1c.** edmure-yields-riverrun ENABLES blackfish-escapes-riverrun | Tier-1 | [depends-on-Lens-A-mint] |
"In the confusion of the castle changing hands, it had been the next morning before Jaime had been
informed that the Blackfish was not amongst the prisoners." affc-jaime-07:39 |
The surrender and the castle-changing-hands created the confusion that enabled the Blackfish's
escape to go undetected until morning. ENABLES is exactly right: Edmure's surrender is a
precondition that opened the window; the Blackfish's own swimming ability and planning (raising
the Water Gate three feet) is the proximate act (affc-jaime-07:37).

**1d.** blackfish-escapes-riverrun CONTEMPORARY_WITH edmure-yields-riverrun | Tier-1 |
[depends-on-Lens-A-mint] |
"Edmure had waited most of the day before hauling down the direwolf of Stark in token of surrender.
In the confusion of the castle changing hands, it had been the next morning before Jaime had been
informed that the Blackfish was not amongst the prisoners." affc-jaime-07:39 |
The escape happened during the same night as the surrender (Brynden swam after dark, discovered
next morning). CONTEMPORARY_WITH captures the temporal overlap without asserting causal priority
— the escape and surrender are distinct acts that happened in the same brief window. This pairs
with 1c above: ENABLES provides the causal seam, CONTEMPORARY_WITH provides the temporal tag.
*Mark BORDERLINE — the graph may not need both; prefer 1c if forced to choose.*

**[BORDERLINE] 1e.** edmure-yields-riverrun ENABLES emmon-frey RULES riverrun | Tier-2 |
[depends-on-Lens-A-mint] |
"'You have a garrison of two hundred.'" affc-jaime-07:49 / Lady Genna: "This is your seat." affc-jaime-07:51 |
The surrender directly enables Emmon Frey's installation as lord. ENABLES (not CAUSES) because
Emmon's actual ruling authority is also contingent on the king's decree. Mark BORDERLINE because
`emmon-frey RULES riverrun` may already exist (baseline lists Emmon as PARTICIPATES_IN the siege
and holds title); verify dedup. The node-to-node form is: `edmure-yields-riverrun ENABLES
emmon-frey` is wrong schema — correct form: `edmure-yields-riverrun CAUSES emmon-frey HOLDS_TITLE
riverrun`. But CAUSES on an existing dyad (emmon-frey HOLDS_TITLE riverrun) doesn't reify cleanly
— rephrase as `edmure-yields-riverrun ENABLES emmon-frey` with a note that the instrument is
Tommen's decree; let synthesis decide form. LOW PRIORITY — the HOLDS_TITLE relationship is already
separately encoded; this edge only matters if the causal chain from surrender → installation is
needed for traversal.

---

### 2 — The Cersei-letter rupture (cross-arc seam)

**2a.** cerseis-imprisonment MOTIVATES jaime-lannister | Tier-2 | [depends-on-Lens-A-mint for
`jaime-burns-cerseis-letter`] |
"Come at once, she said. Help me. Save me. I need you now as I have never needed you before.
I love you. I love you. I love you. Come at once." affc-jaime-07:291 |
The Cersei plea-letter (Qyburn's relay, written during her Faith imprisonment) is what produces
Jaime's decision moment. Model honestly: Cersei's imprisonment is what MOTIVATES her to write the
letter. This is the upstream link in the causal chain. MOTIVATES → jaime-lannister for the refusal
side is edge 2b below.

*This edge sits on an existing node (`cerseis-imprisonment`) — verify it exists in the graph from
the S140 Cersei's-downfall arc. If `cerseis-imprisonment` is the slug, this is a cross-arc seam
edge. Mark as cross-arc seam.*

**2b.** jaime-burns-cerseis-letter MOTIVATES jaime-lannister | Tier-1 | [depends-on-Lens-A-mint] |
"'Does my lord wish to answer?' the maester asked, after a long silence." / "'No,' he said. 'Put
this in the fire.'" affc-jaime-07:293-295 |
The act of receiving and burning the letter is the proximate cause of Jaime's refusal to ride to
Cersei's aid. MOTIVATES → character is correct: the event drives Jaime's decision. Do NOT model
this as `jaime-burns-cerseis-letter CAUSES jaime-refuses-cersei` (that collapses agency) — there
is no separate `jaime-refuses-cersei` node and minting one may be over-engineering. The
MOTIVATES(→jaime-lannister) with the letter-burning as source captures the character-decision root
without asserting a downstream event. The quote is split across two lines — use the single-line
refusal: "No," he said. "Put this in the fire." affc-jaime-07:295.

*Verbatim single-line quote:* "Put this in the fire." affc-jaime-07:295

**2c.** cerseis-imprisonment ENABLES jaime-burns-cerseis-letter | Tier-2 | [depends-on-Lens-A-mint] |
"Qyburn's words were terse and to the point, Cersei's fevered and fervent." affc-jaime-07:291 |
Cersei's imprisonment (the Faith's arrest, S140 Cersei-downfall arc) is the precondition that
causes her to send the desperate plea. ENABLES because a free third-party act (Cersei writing,
Qyburn relaying) produces the letter. This is the cross-arc seam: the Cersei-downfall arc
(S140) flows into the Jaime-Riverlands arc here at the letter. BORDERLINE: the graph may model
this relationship through character-level edges already (CONSPIRES_WITH, DISTRUSTS etc.); this
is the EVENT-level seam. Flag for fresh-verify.

**[BORDERLINE] 2d.** cerseis-imprisonment MOTIVATES cersei-lannister | Tier-1 |
"Come at once, she said. Help me. Save me. I need you now as I have never needed you before.
I love you. I love you. I love you. Come at once." affc-jaime-07:291 |
Cersei's imprisonment motivates her to write the plea — MOTIVATES(→character). This is a
character-motivation edge on the S140 arc's node, not strictly a Lens D cross-arc edge, but
it's the upstream motivational link. BORDERLINE: may already exist in the S140 arc. Defer to
fresh-verify; do not propose if the S140 arc already covers it. LOW PRIORITY.

---

### 3 — WO5K-board seam

**3a.** edmure-yields-riverrun SUB_BEAT_OF wo5k | Tier-2 | [depends-on-Lens-A-mint] |
"The war was all but won. Dragonstone had fallen and Storm's End would soon enough, he could not
doubt, and Stannis was welcome to the Wall." affc-jaime-07:203 |
The Riverrun surrender is the last major Riverlands holdout falling — Jaime explicitly frames
it as completing the Iron Throne's pacification. SUB_BEAT_OF wo5k is the structural claim.
BORDERLINE: check whether the `siege-of-riverrun` itself already carries `PART_OF wo5k` (baseline
says it does: "PART_OF wo5k"). If the siege is already wo5k-tagged, the surrender (as a
SUB_BEAT_OF siege-of-riverrun and the siege is PART_OF wo5k) may be reachable by traversal
without a direct edge. Propose it but mark BORDERLINE for synthesis to decide if redundant.

**3b.** red-wedding ENABLES edmure-yields-riverrun | Tier-2 | [depends-on-Lens-A-mint] |
"Edmure had waited most of the day before hauling down the direwolf of Stark in token of surrender."
affc-jaime-07:39 |
The Red Wedding captured Edmure and made him the primary hostage lever. The baseline already shows
`red-wedding ENABLES siege-of-riverrun` and `edmure-taken-hostage ENABLES siege-of-riverrun`.
The yield event itself is the downstream of the same chain: Edmure's hostage status (product of
red-wedding) is what Jaime exploits with the trebuchet threat. ENABLES is correct.
This is the WO5K seam: red-wedding's consequences flow through to the Riverrun resolution.
BORDERLINE: check if `edmure-taken-hostage ENABLES edmure-yields-riverrun` is more precise (it
may be, since the hostage status is the direct precondition, not the wedding itself). Propose
both forms and let synthesis pick the cleaner link.

**[BORDERLINE] 3c.** edmure-taken-hostage ENABLES edmure-yields-riverrun | Tier-1 |
[depends-on-Lens-A-mint] |
"Your wife may whelp before that. You'll want your child, I expect. I'll send him to you when he's
born. With a trebuchet." affc-jaime-06:325 |
Edmure's status as hostage (captured at the Red Wedding, held by the Freys) is the direct
structural precondition for the trebuchet-threat coercion that produces the surrender. ENABLES
(not CAUSES) because Jaime's threat + Edmure's decision are the proximate agents. This is cleaner
than 3b above — prefer this if forced to choose. Tier-1 because the text directly shows hostage
status being exploited.

---

### 4 — Jaime's bloodless-resolution intent

**4a.** jaime-lannister MOTIVATES jaime-lannister | Tier-2 | ← REJECTED, see Dropped section.

**4b.** jaime-vow-to-catelyn MOTIVATES jaime-lannister | Tier-2 |
"If the Blackfish would not listen, he would have no choice but to break the vow he'd made to
Catelyn Stark." affc-jaime-05:157 |
Jaime's vow to Catelyn (not to take arms against Starks or Tullys) actively shapes his strategic
choices at Riverrun — he tries diplomacy first, then coercion, precisely to avoid breaking the
vow. MOTIVATES(→character) is the correct type. The vow is a pre-existing constraint driving
his decision architecture throughout these chapters. Check whether `jaime-vow-to-catelyn` is a
node (or `catelyn-stark-frees-jaime` / `jaime-swears-to-catelyn`); slug TBD by synthesis — the
vow event itself may need minting by Lens A/B. Mark **[depends-on-node-existence]**.

---

### 5 — Ryman Frey dismissal → Ryman's death seam

**5a.** [BORDERLINE] jaime-lannister AGENT_IN ryman-freys-dismissal | Tier-1 |
"You are dismissed, ser." / "Go away." affc-jaime-06:275 |
Jaime dismisses Ryman Frey from command, which leads directly to Ryman traveling south with a
small escort and being hanged by outlaws. This is a CHAIN: dismissal → small escort → outlaws
ambush. Whether this counts as CAUSES or ENABLES depends on whether we view Jaime as proximately
responsible for Ryman's death. CONSERVATIVE CHOICE: do not assert `jaime CAUSES ryman-freys-death`
— that collapses too many intervening agents (Beric/Stoneheart, the outlaws). At most:
`jaime AGENT_IN ryman-freys-dismissal` (if that event node exists) and note the downstream.
BORDERLINE, LOW PRIORITY — Ryman is a minor node and the death-by-outlaws is already in the
Beric/Stoneheart thread.

---

## Dropped / considered-but-rejected

**Self-MOTIVATES edge (jaime-lannister MOTIVATES jaime-lannister):** Not a valid graph pattern —
MOTIVATES requires a source node distinct from the character being motivated. Dropped.

**siege-of-riverrun CAUSES edmure-yields-riverrun:** Over-asserts. The siege is a precondition,
not a direct cause — Edmure's free choice (coerced by the trebuchet threat) is proximate. ENABLES
is the honest type (edge 1a above).

**`edmure-yields-riverrun TRIGGERS blackfish-escapes-riverrun`:** Too strong. The escape doesn't
follow immediately from the surrender as the "very next beat" — the Blackfish planned in advance
(Water Gate raised, swimming under the boom), and the escape was discovered the next morning.
ENABLES + CONTEMPORARY_WITH (edges 1c, 1d) captures it better.

**`jaime-lannister CAUSES cerseis-imprisonment`:** Not supported. Cersei's imprisonment is by the
Faith, not Jaime. Dropped.

**`jaime-burns-cerseis-letter CAUSES cersei-lannister`:** Not a valid pattern — CAUSES needs an
event target. Dropped.

**`red-wedding CAUSES edmure-yields-riverrun`:** Too distal. The red-wedding is 2+ causal steps
away; the chain runs through edmure-taken-hostage. Use ENABLES at the closer link. Dropped in
favor of 3b/3c.

**`siege-of-riverrun MOTIVATES brynden-tully`:** The Blackfish's defiance is an existing
characterization, not a new edge. His motivation is his Stark-loyalty and refusal to yield — the
text doesn't introduce a new motivating event here. "I'll die warm, if you please, with a sword
in hand running red with lion blood." (affc-jaime-06:63) shows defiance but the MOTIVATES source
would be personal honor/loyalty, not a specific event node. Skip — no clean event source.

**`blackfish-escapes-riverrun MOTIVATES brynden-tully`:** Circular — the escape IS Brynden's act,
can't MOTIVATE him toward itself. Dropped.

**Jaime-as-valonqar reading:** GATED. Not proposed.

**Show-canon beats (Jaime meeting Stoneheart):** TWOW/show-only. Not proposed.

**Harrenhal node-tangle:** Baseline explicitly DO-NOT. Not touched.

**`jaime-burns-cerseis-letter FORESHADOWS` something:** Foreshadowing is a Pass 4 scope. Not
proposed here.

**Ryman Frey dismissed → Ryman hanged causal edge:** Considered and marked BORDERLINE (5a above).
The chain (Jaime dismisses → Ryman travels with small escort → outlaws ambush) has too many
intervening agents to assert CAUSES cleanly. Dropping the causal form; keeping AGENT_IN on the
dismissal event if the node exists.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|-------------|------|
| food/drink | AFFC | affc-jaime-05:45 | Pia mulling wine, "stirring the kettle with a spoon"; Daven gets warm wine on golden platter |
| food/drink | AFFC | affc-jaime-05:61 | Daven drains cup, asks squire to fill it again: "I have a thirst" |
| food/drink | AFFC | affc-jaime-05:105 | Siege provisioning: "We have fish in the rivers, we won't starve" — fish keeping the camp fed, nets in the boom |
| food/drink | AFFC | affc-jaime-05:109 | "The Blackfish expelled all the useless mouths from Riverrun … He has enough stores to keep man and horse alive for two full years." — siege provisioning / garrison stores |
| food/drink | AFFC | affc-jaime-05:113 | Frey provisioning failure: "The Freys are hauling food and fodder down from the Twins, but Ser Ryman claims he does not have enough to share, so we must forage for ourselves" |
| food/drink | AFFC | affc-jaime-06:309 | Jaime orders bathwater and food for Edmure: "Lew, heat some bathwater for my guest. Pia, find him some clean clothing … Peck, wine for Lord Tully. Are you hungry, my lord?" |
| food/drink | AFFC | affc-jaime-07:49 | Siege aftermath: "the Blackfish had left Riverrun amply provisioned, just as he had claimed" — garrison had full stores |
| food/drink | AFFC | affc-jaime-07:173 | Jaime and Ilyn drink after night training: "Come, let's drink some more of Hoster Tully's good red wine" |
| food/drink | AFFC | affc-jaime-07:177 | Ritual wine-drinking with Ser Ilyn: "The wine was a deep red, sweet and heavy. It warmed him going down." |
| food/drink | AFFC | affc-jaime-07:207 | Garrison departs: "Each man was allowed three days' food and the clothing on his back" |
| food/drink | AFFC | affc-jaime-06:245 | Lady Genna asks for wine; Jaime pours "one-handed" from a flagon |
| food/drink | AFFC | affc-jaime-06:309 | Edmure given bath, clean clothes, wine, food by Jaime's squires — hospitality-as-coercion beat |
| quote | AFFC | affc-jaime-06:325 | Load-bearing trebuchet threat verbatim: "I'll send him to you when he's born. With a trebuchet." — attach to edmure-yields-riverrun + jaime-lannister node Quotes |
| quote | AFFC | affc-jaime-07:291 | Cersei's letter verbatim: "Come at once, she said. Help me. Save me. I need you now as I have never needed you before. I love you. I love you. I love you. Come at once." — attach to jaime-burns-cerseis-letter + cersei-lannister node Quotes |
| quote | AFFC | affc-jaime-07:295 | Jaime refuses: "No," he said. "Put this in the fire." — attach to jaime-burns-cerseis-letter node Quotes |
| quote | AFFC | affc-jaime-07:39 | Blackfish escape mechanism: "a black fish in a black river floating quietly downstream" — poetic; attach to blackfish-escapes-riverrun node Quotes |
| description | AFFC | affc-jaime-05:157 | Riverrun physical: "Riverrun, rising from the narrow point where the Tumblestone joined the Red Fork. The Tully castle looked like a great stone ship with its prow pointed downriver. Its sandstone walls were drenched in red-gold light" |
| description | AFFC | affc-jaime-05:159 | Ryman's gallows: "A great grey gallows loomed above the tents, as tall as any trebuchet. On it stood a solitary figure with a rope about his neck. Edmure Tully." |
| description | AFFC | affc-jaime-05:175 | Lannister siege equipment: "Two other towers stood completed, half-covered with raw horsehide. Between them sat a rolling ram; a tree trunk with a fire-hardened point suspended on chains beneath a wooden roof." |
| description | AFFC | affc-jaime-07:277-279 | Snow arriving at Riverrun: "It was snow, drifting through the window … The yard below was covered by a thin white blanket, growing thicker even as he watched. The merlons on the battlements wore white cowls." — winter-arrival register |
| description | AFFC | affc-jaime-07:291 | Letter arriving: "A snowflake landed on the letter. As it melted, the ink began to blur." — the snow-melting-on-the-letter image; attach to jaime-burns-cerseis-letter |
| foreshadowing | AFFC | affc-jaime-07:249-265 | Joanna-ghost dream in the Great Sept — the woman who is not Cersei who tells Jaime "Count your hands, child." Load-bearing identity/prophecy beat; flag for Pass 4 foreshadowing-scanner |
| hospitality | AFFC | affc-jaime-05:189-191 | Lady Genna arrives at Jaime's tent: "She held out her arms and left him no choice but to embrace her" — family reunion hospitality beat |
| hospitality | AFFC | affc-jaime-06:309 | Jaime bathes, clothes, feeds, and wines Edmure before the coercive negotiation — hospitality-as-strategy |
| misc | AFFC | affc-jaime-07:129 | Ryman Frey's death: "Hanged with all his party. The outlaws caught them two leagues south of Fairmarket." — Beric/Stoneheart thread pointer; Edwyn names "this woman Stoneheart" (affc-jaime-07:127) |
| misc | AFFC | affc-jaime-05:121 | Signal fires: "My scouts report fires in the high places at night. Signal fires, they think … as if there were a ring of watchers all around us." — Brotherhood network pointer |
