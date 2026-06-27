# Lens A — Spine + Secondary-Character Sub-arcs — A1.5 Dorne proposal (S156)

## Proposed NEW nodes

---

**slug:** `garin-orphan-of-the-greenblood`
**name:** Garin (orphan of the Greenblood)
**type:** `character.human`
**summary:** Arianne's milk brother and childhood companion, one of the five conspirators in the Queenmaker plot. An orphan of the Greenblood (Rhoynar river people), swarthy and long-nosed, with a gold tooth Arianne bought him. His mother was Arianne's wet nurse. After the plot's failure, Doran sentences him to two years in Tyrosh.
**anchor quote + chapter:line:** "Here is gay Garin of the orphans, who makes me laugh," said Arianne. "His mother was my wet nurse." — `affc-the-queenmaker-01:137`

**BUG FLAG:** The existing edge `arianne CONSPIRES_WITH garin-the-great` points to the legendary Rhoynar prince Garin the Great (dead ~1,000 years), not this character. That edge must be re-pointed to `garin-orphan-of-the-greenblood` after this node is minted. This is a wrong-target bug.

---

**slug:** `arys-oakheart-charges-to-his-death` *(event — consider minting)*
**name:** Arys Oakheart Charges to His Death
**type:** `event.death`
**summary:** At the Greenblood, with the ambush sprung and escape impossible, Ser Arys Oakheart put spurs to his horse and charged alone into Areo Hotah's guardsmen rather than yield. He was feathered with crossbow bolts and his horse brought down; he struggled to his knees and was decapitated by Hotah's longaxe. The charge was his chosen end — he had one last longing look at Arianne before riding.
**anchor quote + chapter:line:** "Ser Arys Oakheart gave her one last longing look, then put his golden spurs into his horse and charged." — `affc-the-queenmaker-01:281`

**Rationale for minting:** This event is already partially covered by `areo-hotah KILLS arys-oakheart` (deduped), but that dyadic edge has no upstream cause slot and no MOTIVATES-or-agency layer. If minted, this event owns: `MOTIVATES→arys-oakheart` (the shame/love/chosen-death triad), a distinct `AGENT_IN` role for Arys (he chose the charge), and the `TRIGGERED_BY areo-hotah-springs-the-ambush` seam. Propose; gate is downstream.

---

## Proposed NEW edges

> Format: source_slug [EDGE_TYPE] target_slug | Tier | qualifier | verbatim quote + chapter:line | rationale

---

### Gap 1 — Plot motive + goal

**1.**
`doran-intercepted-letter` → does not exist as a node; route via MOTIVATES to character instead.

`the-queenmaker-plot` [CAUSES] `areo-hotah-springs-the-ambush` — already in spine, DO NOT re-propose.

**1a.**
`arianne-martell` [SEEKS] `iron-throne` | Tier-3 | — | "By rights should sit the Iron Throne" — Arianne articulating Myrcella's claim as her own goal for the plot | `affc-the-soiled-knight-01:209`
- Rationale: The plot's aim is Myrcella's Iron Throne claim under Dornish primogeniture. No SEEKS edge from Arianne to the iron-throne currently exists (confirmed gap). Quote captures Arianne's articulation of the plot's goal to Arys: "Myrcella by rights should sit the Iron Throne."
- Full line: "But not better than Myrcella. She loves the boy as well. I know she will not let him come to any harm. Storm's End is his by rights, since Lord Renly left no heir and Lord Stannis is attainted. In time, Casterly Rock will pass to the boy as well, through his lady mother. He will be as great a lord as any in the realm . . . but Myrcella by rights should sit the Iron Throne."
- Quote to use: "Myrcella by rights should sit the Iron Throne." — `affc-the-soiled-knight-01:209`

**1b.**
`arianne-martell` [CLAIMS] `iron-throne` | Tier-3 | — | "By law the Iron Throne should pass to her." — Tyene Sand articulating the claim, which Arianne is acting on | `affc-the-captain-of-guards-01:283`
- Rationale: The plot's whole premise is Myrcella's primogeniture claim. The CLAIMS edge should go from `myrcella-baratheon` not `arianne-martell`. See 1c below.

**1c.**
`myrcella-baratheon` [CLAIMS] `iron-throne` | Tier-2 | — | "She is older than her brother," explained Tyene, as if he were some fool. "By law the Iron Throne should pass to her." — `affc-the-captain-of-guards-01:283`
- Rationale: This is the plot's foundational premise — Myrcella's primogeniture claim under Dornish law. No such CLAIMS edge currently exists (gap confirmed in baseline). Tier-2 because the claim is in-universe asserted but disputed/unresolved.

**1d.**
`doran-martell` [MOTIVATES] `arianne-martell` | Tier-1 | — | "I read your letter. 'One day you will sit where I sit and rule all Dorne,' you wrote him." — `affc-the-princess-in-the-tower-01:281`
- [BORDERLINE] — direction is tricky. The letter MOTIVATES Arianne's grievance that drives the plot. But a MOTIVATES edge requires source = actor or event, target = character. Here the intercepted letter (an event/object) spurs Arianne. Model as: the disinheritance-belief MOTIVATES arianne. The character Doran is not directly the actor in a MOTIVATES sense; it's his letter/act. Propose as-is (Doran's action → Arianne), but flag for orchestrator. Alternative: `doran-martell` [RESENTS] isn't right direction. Better:

**1d (revised):**
`arianne-martell` [RESENTS] `doran-martell` | Tier-1 | — | "Why did you decide to disinherit me? Was it the day that Quentyn was born, or the day that I was born? What did I ever do to make you hate me so?" — `affc-the-princess-in-the-tower-01:281`
- Rationale: Already-wired: `arianne RESENTS doran` IS in the dedup list (`arianne ... RESENTS doran` listed in Already-wired Court/kin section). **DO NOT propose — DEDUPED.**

**1e.**
`the-queenmaker-plot` [MOTIVATES] `arianne-martell` | Tier-1 | — | **[BORDERLINE]** — This direction is wrong per the vocab: MOTIVATES target must be a character driven BY the source; here the plot IS Arianne's act, not something that drives her. Skip; route through the letter-grievance motive below.

**1f — the intercepted-letter motive (the real Gap 1 gap):**
`arianne-martell` [SEEKS] `dorne` | Tier-1 | — | "I want my rights. Dorne." — `affc-the-princess-in-the-tower-01:245`
- Rationale: Arianne explicitly states her motivation when confronting Doran: she wants Dorne itself (her birthright). The intercepted letter (her discovery at age 14 that Doran wrote Quentyn "one day you will sit where I sit") MOTIVATES her drive; the best available edge is SEEKS→dorne (the thing she is trying to preserve/claim). This is the deep motive behind the Queenmaker plot, currently unwired.

**1g — the letter as plot enabler:**
`arianne-martell` [MOTIVATES] `the-queenmaker-plot` | Tier-1 | — | **[BORDERLINE]** — MOTIVATES target must be a character, NOT an event. This is the sequence-trap: an event can't be the MOTIVATES target. Per the vocab contract, the disinheritance-grievance MOTIVATES Arianne (the actor), and Arianne then AGENT_IN the plot. The letter-grievance→plot chain must route through Arianne. No separate MOTIVATES→event edge is valid.
- **Skip.** Already covered by `arianne AGENT_IN the-queenmaker-plot` (deduped) + the MOTIVATES chain through her character.

---

### Gap 1 (clean proposal set):

**E1.**
`myrcella-baratheon` [CLAIMS] `iron-throne` | Tier-2 | — | "By law the Iron Throne should pass to her." `affc-the-captain-of-guards-01:283` | The Queenmaker plot's foundational legal premise: Myrcella's Dornish-primogeniture claim to the Iron Throne. Unwired.

**E2.**
`arianne-martell` [SEEKS] `dorne` | Tier-1 | — | "I want my rights. Dorne." `affc-the-princess-in-the-tower-01:245` | Arianne's explicit statement of her deep motive: she is fighting for Dorne itself (her birthright), which she believes Doran is giving to Quentyn. This is the upstream driver of the Queenmaker plot.

**E3.**
`arianne-martell` [IGNORANT_OF] `doran-reveals-fire-and-blood-pact` | Tier-1 | — | "Someone told me. She could have secrets too." / "I was promised … The pact was sealed in secret." `affc-the-princess-in-the-tower-01:273–325` | Arianne launched the Queenmaker plot precisely because she did not know Doran's secret long-game (the betrothal-to-Viserys pact, now redirected to Dany via Quentyn). Her ignorance of the pact is the causal condition that makes the plot possible. IGNORANT_OF is the cleanest structural fit — she is unaware of the very thing her father is doing. [BORDERLINE: IGNORANT_OF is typically used for a character being unaware of an event; here the event is Doran's revelation/pact, which she learns of only after the plot fails. The edge is structurally sound but the direction is character→event that hasn't-yet-been-revealed-to-her. Flag for orchestrator.]

---

### Gap 2 — Arys Oakheart sub-arc

**E4.**
`arianne-martell` [MANIPULATES] `arys-oakheart` | Tier-1 | qualifier: `via_seduction` | "I fucked him, Father. You did command me to entertain our noble visitors, as I recall." `affc-the-princess-in-the-tower-01:219` | Arianne explicitly confirms to Doran she used the seduction as instrument; her own retrospective confirms the tool layer beyond the LOVER_OF that already exists. This is the marquee missing edge per baseline Gap 2.

**E5.**
`arys-oakheart` [BREAKS_VOW] `tommen-baratheon` | Tier-1 | — | "I swore an oath!" / "To Joffrey, not to Tommen." `affc-the-soiled-knight-01:203–205` | Arys acknowledges his vow to the Crown and articulates the oath he is breaking by joining the conspiracy. The vow-recipient is the reigning king (Tommen); Arianne's "To Joffrey, not to Tommen" is her rhetorical attempt to dissolve the obligation, but the vow target in BREAKS_VOW should be the institution/current holder of the oath: Tommen. [BORDERLINE: Kingsguard vows are sworn to the king; Joffrey is dead and Tommen is the new king. The text explicitly names both. Tommen is the current monarch and thus the current vow-recipient. Flag for orchestrator — alternative target is the Kingsguard oath itself, but no node for that exists.]

**E6.**
`arys-oakheart` [VOWS_TO] `myrcella-baratheon` | Tier-1 | qualifier: `to_protect` | "No one shall ever harm Myrcella whilst I live." `affc-the-soiled-knight-01:43` | Arys states his protective vow to Doran directly. VOWS_TO requires a qualifier; `to_protect` captures the content. This edge is what BREAKS_VOW (E5) makes tragic: he abandons his king-oath but maintains his princess-protection vow (his charge to Myrcella). [Check dedup: baseline says `arys GUARDS/LOVES/PROTECTS/VOWS_TO myrcella` — VOWS_TO myrcella IS already in the dedup list. **DO NOT propose — DEDUPED.**]

**E6 (revised) — the shame-driven motivational arc:**
`arys-oakheart` [FEARS] `arianne-martell` | Tier-2 | — | "I have learned too much from you already." / "I am afraid." / "Now you mock me." `affc-the-soiled-knight-01:81–144` | [BORDERLINE] — This is a more interpretive edge. Arys fears his own shame/guilt induced by Arianne, not Arianne herself. Better modeled as MOTIVATES below. **Skip.**

**E7 — Arys's chosen-death agency:**
`arys-oakheart-charges-to-his-death` [AGENT_IN] `arys-oakheart` | — wrong direction. AGENT_IN: entity→event. Try:
`arys-oakheart` [AGENT_IN] `arys-oakheart-charges-to-his-death` | Tier-1 | — | "Ser Arys Oakheart gave her one last longing look, then put his golden spurs into his horse and charged." `affc-the-queenmaker-01:281` | Only valid if the event node `arys-oakheart-charges-to-his-death` is minted. Propose conditionally.

**E8.**
`arianne-martell` [MANIPULATES] `arys-oakheart` | Tier-1 | qualifier: `via_seduction` — this is E4. Listed once above.

**E9 — the guilt/shame as motive:**
`murder-of-elia-and-her-children` [MOTIVATES] `arys-oakheart` | — [BORDERLINE] — No, this is not supported by the text. Arys is not motivated by Elia's murder; he is motivated by his love of Arianne and his shame over breaking his Kingsguard oath. Skip.

**E9 (actual):**
`the-queenmaker-plot` [ENABLES] `arys-oakheart-charges-to-his-death` | Tier-2 | — | "Ser Arys Oakheart gave her one last longing look, then put his golden spurs into his horse and charged." `affc-the-queenmaker-01:281` | The ambush (itself caused by the plot being discovered) is the precondition that puts Arys in the impossible situation where he chooses to charge. ENABLES fits: the plot + its betrayal → the ambush → the impossible moment → Arys's free choice to charge rather than yield. Only valid if event node is minted.

---

### Gap 2 (clean proposal set):

**E4 (confirmed).**
`arianne-martell` [MANIPULATES] `arys-oakheart` | Tier-1 | qualifier: `via_seduction` | "I fucked him, Father. You did command me to entertain our noble visitors, as I recall." `affc-the-princess-in-the-tower-01:219` | Arianne's retrospective confession to Doran confirming the seduction was instrumental (she "entertained" him to secure his cooperation in the plot). Highest-value new edge per baseline Gap 2.

**E5 (confirmed).**
`arys-oakheart` [BREAKS_VOW] `tommen-baratheon` | Tier-1 | — | "I swore an oath!" `affc-the-soiled-knight-01:203` | Arys explicitly says he swore an oath; the oath is his Kingsguard vow to the Crown, with Tommen as current king-recipient. Joining the Queenmaker plot is the breaking. [BORDERLINE: text names both Joffrey and Tommen; flag for orchestrator.]

**E6-new.**
`arys-oakheart-charges-to-his-death` [MOTIVATES] `arys-oakheart` | Tier-2 | — | **[BORDERLINE]** — direction error: MOTIVATES target is always a character. This would mean the event motivates Arys, which is backwards. Skip.

**E6-correct.**
`arianne-martell` [MOTIVATES] `arys-oakheart` | Tier-2 | — | "I swear, no man will steal your birthright whilst I still have the strength to lift a sword. I am yours. What would you have of me?" `affc-the-soiled-knight-01:275` | Arianne's persuasion of Arys — she successfully motivates him to join the plot and ultimately to charge at the ambush. The MANIPULATES edge (E4) covers the seduction tool; this MOTIVATES covers the ideological persuasion layer (the primogeniture argument, the marriage promise, the appeal to his knightly duty). Two edges, different mechanisms. [BORDERLINE: some overlap with MANIPULATES via_seduction. Orchestrator to decide if both are needed or if MANIPULATES covers the chain.]

---

### Gap 3 — Conspirator web

**E10.**
`andrey-dalt` [AGENT_IN] `the-queenmaker-plot` | Tier-1 | — | "'Your Grace,' he said, 'and I should be greatly honored if Your Grace would do the same.'" + "Whatever name Your Grace prefers, I am her man." `affc-the-queenmaker-01:125–129` | Drey explicitly swears himself to Myrcella-as-queen and participates in the crowning attempt. `andrey-dalt core_in=0` confirmed gap.

**E11.**
`andrey-dalt` [CONSPIRES_WITH] `arianne-martell` | Tier-1 | — | "Arianne Martell arrived with Drey and Sylva just as the sun was going down." `affc-the-queenmaker-01:13` | Drey rides with Arianne to Shandystone as part of the conspiracy. Confirmed part of the five-friends conspirator web.

**E12.**
`sylva-santagar` [AGENT_IN] `the-queenmaker-plot` | Tier-1 | — | "My dearest Spotted Sylva" / "My queen, I am your man" (Garin); Sylva kneels and pledges: "My lady liege." `affc-the-queenmaker-01:104–105` | Spotted Sylva explicitly kneels before Myrcella and pledges her as queen. `sylva-santagar` is unwired (gap confirmed).

**E13.**
`sylva-santagar` [CONSPIRES_WITH] `arianne-martell` | Tier-1 | — | "Arianne Martell arrived with Drey and Sylva just as the sun was going down." `affc-the-queenmaker-01:13` | Sylva rides with Arianne to Shandystone as part of the conspiracy.

**E14.**
`garin-orphan-of-the-greenblood` [AGENT_IN] `the-queenmaker-plot` | Tier-1 | — | "My queen, I am your man." Garin dropped to both knees. `affc-the-queenmaker-01:107` | Garin explicitly pledges himself to Myrcella as queen; he is at Shandystone ahead of the group and assists throughout.

**E15.**
`garin-orphan-of-the-greenblood` [CONSPIRES_WITH] `arianne-martell` | Tier-1 | — | "Garin had arrived a few hours earlier" / "he was Arianne's milk brother, and they had been inseparable since before they learned to walk." `affc-the-queenmaker-01:13,23` | Garin is Arianne's milk brother (also see `affc-the-queenmaker-01:137` "His mother was my wet nurse") and a co-conspirator at Shandystone.

**E16.**
`garin-orphan-of-the-greenblood` [MILK_BROTHER_OF] `arianne-martell` | Tier-1 | — | "His mother was my wet nurse." `affc-the-queenmaker-01:137` | Garin's mother nursed Arianne; the MILK_BROTHER_OF edge captures this Rhoynar kinship tie, the basis of their lifelong closeness.

**E17.**
`tyene-sand` [CONSPIRES_WITH] `arianne-martell` | Tier-2 | — | "for the most part they had been a company of five" / "She and Tyene had learned to read together, learned to ride together" `affc-the-princess-in-the-tower-01:69` | Tyene is named as the fifth member of the childhood conspirator group ("a company of five"). She is NOT physically at Shandystone (she was imprisoned before the ride); but Arianne confirms she was Tyene's closest co-conspirator. Tier-2: she's not at Shandystone but is part of the five. [BORDERLINE: Tyene's arrest precedes the queenmaker ride; she may not technically be an AGENT_IN the queenmaker plot specifically. CONSPIRES_WITH is a broader relationship edge that fits better than AGENT_IN here.]

**E18 — the five-companions structure:**
`andrey-dalt` [CONSPIRES_WITH] `garin-orphan-of-the-greenblood` | Tier-2 | — | "for the most part they had been a company of five" `affc-the-princess-in-the-tower-01:69` | [BORDERLINE] — The five-friends web is confirmed prose but the dyadic sub-edges (Drey↔Garin, Drey↔Sylva, Garin↔Sylva) may be over-minting. Propose only if the gap-filling value is high; orchestrator decides. List as lower-priority.

---

### Gap 5 — Conspirator dispersal (downstream-dark terminus)

**E19.**
`doran-martell` [MARRIES_OFF] `sylva-santagar` | Tier-1 | — | "Lady Sylva received no punishment from me, but she was of an age to marry. Her father has shipped her to Greenstone to wed Lord Estermont." `affc-the-princess-in-the-tower-01:217` | Doran's punishment for Sylva: her father ships her off to Greenstone. Doran is the arranger (he decides/permits; her father executes it at Doran's implicit direction as part of the conspirator disposal). [BORDERLINE: technically "her father" ships her; Doran says he gave "no punishment," but the effect is Doran-orchestrated dispersal. The MARRIES_OFF type fits Doran as the authority figure whose dispositions cause the marriage. Orchestrator flag.]

**E20.**
`andrey-dalt` [TRAVELS_TO] `norvos` | Tier-1 | — | "Ser Andrey has been sent to Norvos to serve your lady mother for three years." `affc-the-princess-in-the-tower-01:217` | Drey's post-conspiracy punishment: sent to Norvos to serve Lady Mellario. Light dispersal edge.

**E21.**
`garin-orphan-of-the-greenblood` [TRAVELS_TO] `tyrosh` | Tier-1 | — | "Garin will spend his next two years in Tyrosh." `affc-the-princess-in-the-tower-01:217` | Garin's post-conspiracy dispersal sentence.

**E22.**
`andrey-dalt` [VICTIM_IN] `arrest-of-the-sand-snakes` | Tier-2 | — | **[BORDERLINE]** — The "arrest-of-the-sand-snakes" event in the spine covers the Sand Snakes (Obara/Nym/Tyene); Drey/Garin/Sylva are captured at the Greenblood by Hotah separately. They're sent to Ghaston Grey, not imprisoned in the Spear Tower. The event name is "arrest-of-the-sand-snakes" which may not cover the conspirator capture. **Skip** — different event, not the sand-snakes arrest. The dedup event doesn't cover them.

**E23.**
`gerold-dayne` [TRAVELS_TO] `high-hermitage` | Tier-2 | — | "Darkstar had escaped him, the most dangerous of all her little group of plotters. He had outraced all his pursuers and vanished into the deep desert, with blood upon his blade." `affc-the-princess-in-the-tower-01:19` | Darkstar flees to High Hermitage (his castle, as the heir of House Dayne of High Hermitage, already `RULES high-hermitage`). The text says "deep desert" not explicitly High Hermitage, but his castle is there and "vanished into the deep desert" is the only available quote. [BORDERLINE: "deep desert" is directionally right but the text doesn't name High Hermitage explicitly as the destination. Flag for orchestrator.]

---

### Gap 4 — Informer mystery (SUSPECTED_OF only, text-grounded)

**E24.**
`arys-oakheart` [SUSPECTED_OF] `the-queenmaker-plot` | — wrong type. SUSPECTED_OF means a character suspected of being the agent/cause of an event. Here it would be: who is suspected of INFORMING?

No event node `betrayal-of-the-queenmaker-plot` or similar exists. The informer-mystery is best represented as:

`arys-oakheart` [SUSPECTED_OF] the betrayal — but without an event node for "the betrayal/tip-off," this edge has no clean target. 

**[DO NOT PROPOSE]** — The text presents the informer mystery as genuinely unresolved. Arianne cycles through suspects: Darkstar (she dismisses — why would he maim Myrcella if he was the betrayer?), Arys (she wonders: did his guilt win out?), and the reader is left without a clear answer. Doran says only "I am the Prince of Dorne. Men seek my favor." SUSPECTED_OF edges here would require a target event node (the betrayal) that doesn't exist. The orchestrator should decide whether to mint a `betrayal-of-the-queenmaker-plot` event node; the informer-mystery SUSPECTED_OF edges would hang on it. This is a borderline reification question. For now: **no SUSPECTED_OF proposals** without the event node — doing so would be proposing into thin air.

*Harvest note:* The text offers `arianne-martell` [SUSPECTED_OF] `arys-oakheart` (did he betray the plot to atone?) and `gerold-dayne` as a dismissed suspect. These are Tier-3 suspects at best. Park for the orchestrator.

---

## Bug fix flag

**`arianne CONSPIRES_WITH garin-the-great`** — this edge (per baseline Gap 3) points to the legendary Garin the Great, a Rhoynar prince dead ~1,000 years. The intended target is `garin-orphan-of-the-greenblood` (proposed above). This is a wrong-target bug. Once `garin-orphan-of-the-greenblood` is minted, the edge must be re-pointed: `arianne-martell CONSPIRES_WITH garin-orphan-of-the-greenblood`.

---

## Dropped / considered-but-rejected

- **`arys-oakheart BREAKS_VOW house-oakheart`** — the Kingsguard vow is sworn to the Crown/king, not to his house. Dropped; tommen-baratheon is the correct vow-recipient (E5).
- **`arianne-martell SEDUCES arys-oakheart`** — no SEDUCES type exists in the locked vocab. Handled via MANIPULATES via_seduction (E4). Dropped.
- **`gerold-dayne KILLS arys-oakheart`** — per dedup: `areo-hotah KILLS arys-oakheart` is already wired. Darkstar kills no one in the queenmaker chapter — he maims Myrcella and flees. Dropped.
- **`arianne-martell WITNESS_IN arys-oakheart-charges-to-his-death`** — Arianne does witness Arys's charge and death ("She heard Myrcella shrieking") but the WITNESS_IN guidance requires the character to "actually SEES it." The text says "Ser Arys Oakheart gave her one last longing look, then put his golden spurs into his horse and charged" — she does see the charge. However, the event node itself is proposed-but-not-yet-minted. Deferred: only valid if the event node is minted. Also: she collapses into shock and is "on her hands and feet in the sand, shaking and sobbing" after; the text is ambiguous about whether she sees the axe-blow itself. [BORDERLINE, deferred.]
- **`arys-oakheart SUSPECTED_OF betrayal-of-the-queenmaker-plot`** — the informer mystery: Arianne wonders if Arys betrayed the plot, but the text is unresolved and there is no target event node. Per HARD RULES and the SUSPECTED_OF contract, do not assert an informer the text leaves unproven. Dropped pending orchestrator decision on event-node reification.
- **`the-queenmaker-plot CAUSES iron-throne (some instability event)`** — too speculative; no such event in the dedup spine. Dropped.
- **`arianne-martell RESENTS doran-martell`** — already wired (dedup). Dropped.
- **`arys VOWS_TO myrcella-baratheon`** — already wired (dedup): `arys GUARDS/LOVES/PROTECTS/VOWS_TO myrcella`. Dropped.
- **`doran-martell SENDS_AWAY / BANISHES andrey-dalt`** — no BANISHES type in vocab. The dispersal is captured by TRAVELS_TO (E20). Dropped.
- **`tyene-sand AGENT_IN the-queenmaker-plot`** — Tyene was imprisoned before the queenmaker ride. She is part of the five-friends conspiracy circle but not physically present at Shandystone or the Greenblood. CONSPIRES_WITH is the right edge (E17), not AGENT_IN. Dropped.

---

## Harvest

| kind | book | chapter:line | note |
|---|---|---|---|
| food | AFFC | affc-the-soiled-knight-01:21 | Snake grilled over a brazier, turned with wooden tongs; "the best snake sauce had a drop of venom in it, along with mustard seeds and dragon peppers" — Dornish street food, shadow city |
| food | AFFC | affc-the-soiled-knight-01:22 | Myrcella "had taken to Dornish food as quick as she had to her Dornish prince" — food/character preference note |
| food | AFFC | affc-the-captain-of-guards-01:11 | Blood oranges overripe and fallen, bursting on the pink marble of the Water Gardens — the iconic Dornish fruit; Doran notes them in his first line |
| food | AFFC | affc-the-captain-of-guards-01:153 | Doran eats: bowl of purple olives, flatbread, cheese, chickpea paste, and a cup of sweet heavy strongwine — his evening meal at the Water Gardens |
| food | AFFC | affc-the-captain-of-guards-01:165 | Doran breaks fast with "a blood orange and a plate of gull's eggs diced with bits of ham and fiery peppers" before the journey to Sunspear |
| food | AFFC | affc-the-queenmaker-01:239 | Myrcella splits an orange with Spotted Sylva; "Garin ate olives and spit the stones at Drey" — conspirators at rest during the queenmaker ride |
| food | AFFC | affc-the-queenmaker-01:155 | Arianne offers Myrcella at Shandystone: "We have dates and cheese and olives, and lemonsweet to drink" |
| food | AFFC | affc-the-captain-of-guards-01:157 | Hotah remembers wintercake "rich with ginger and pine nuts and bits of cherry, with nahsa to wash it down, fermented goat's milk served in an iron cup and laced with honey" — Norvoshi food memory |
| food | AFFC | affc-the-princess-in-the-tower-01:47 | Arianne's prison meal: "kid roasted with lemon and honey. With it were grape leaves stuffed with a mélange of raisins, onions, mushrooms, and fiery dragon peppers" — Dornish prison rations (notably generous) |
| food | AFFC | affc-the-princess-in-the-tower-01:59 | Arianne's imprisoned comforts include "figs or olives or peppers stuffed with cheese" on request |
| drink | AFFC | affc-the-queenmaker-01:37 | The conspirators at Shandystone "passed a skin of summerwine from hand to hand . . . all but Darkstar, who preferred to drink unsweetened lemonwater" — character detail (Darkstar's austerity) |
| drink | AFFC | affc-the-captain-of-guards-01:153 | Doran drinks "the sweet, heavy strongwine that he loved" — his characteristic drink |
| description | AFFC | affc-the-queenmaker-01:31 | Darkstar physical description: "aquiline nose, high cheekbones, a strong jaw . . . thick hair fell to his collar like a silver glacier, divided by a streak of midnight black . . . his eyes were purple. Dark purple. Dark and angry." |
| description | AFFC | affc-the-captain-of-guards-01:217 | Sunspear's three towers: "First the slender Spear Tower, a hundred-and-a-half feet tall and crowned with a spear of gilded steel that added another thirty feet to its height; then the mighty Tower of the Sun, with its dome of gold and leaded glass; last the dun-colored Sandship" |
| description | AFFC | affc-the-captain-of-guards-01:25 | Obara Sand's appearance: "big-boned woman near to thirty, with the close-set eyes and rat-brown hair of the Oldtown whore who'd birthed her. Beneath a mottled sandsilk cloak of dun and gold, her riding clothes were old brown leather, worn and supple." |
| description | AFFC | affc-the-captain-of-guards-01:171 | Nymeria Sand on horseback: "slender as a willow. Her straight black hair, worn in a long braid bound up with red-gold wire, made a widow's peak above her dark eyes . . . milk-pale skin" — full physical description |
| description | AFFC | affc-the-captain-of-guards-01:251–252 | Tyene Sand description: "clinging gown of pale blue samite with sleeves of Myrish lace that made her look as innocent as the Maid herself . . . Hair was gold as well, and her eyes were deep blue pools" |
| description | AFFC | affc-the-captain-of-guards-01:235 | Arianne at the outer ward: "a mane of jet-black ringlets that fell to the small of her back, and around her brow was a band of copper suns . . . beneath her jeweled girdle and loose layers of flowing purple silk and yellow samite she had a woman's body, lush and roundly curved" |
| description | AFFC | affc-the-soiled-knight-01:57 | Arianne's seduction scene: "An ornate snake coiled around her right forearm, its copper and gold scales glimmering when she moved. It was all she wore." — vivid object + body description |
| quote | AFFC | affc-the-captain-of-guards-01:39 | Hotah's vow: "Serve. Obey. Protect. Simple vows for simple men" — load-bearing characterization of Areo Hotah; his defining motto |
| quote | AFFC | affc-the-queenmaker-01:299 | "Someone told." Hotah shrugged. "Someone always tells." — the arc's marquee closing line, on the informer betrayal |
| quote | AFFC | affc-the-princess-in-the-tower-01:325 | Doran's "fire and blood" reveal: "Vengeance. Justice. Fire and blood." — the pact's thematic declaration; also `affc-the-princess-in-the-tower-01:243` "I have worked at the downfall of Tywin Lannister since the day they told me of Elia and her children." |
| quote | AFFC | affc-the-soiled-knight-01:113 | Arianne to Arys: "Abed, unclad, we are our truest selves, a man and a woman, lovers, one flesh, as close as two can be. Our clothes make us different people." — character voice, Arianne's philosophy |
| quote | AFFC | affc-the-soiled-knight-01:155 | Arys: "I will not be remembered as Ser Arys the Unworthy. I will not soil my cloak." — his key internal conflict line, later proved ironic |
| foreshadowing | AFFC | affc-the-captain-of-guards-01:135 | Hotah foreshadows his own killing of Arys: "One day, he sensed, the two of them would fight; on that day Oakheart would die, with the captain's longaxe crashing through his skull." |
| hospitality | AFFC | affc-the-captain-of-guards-01:241 | Doran's farewell to the Water Gardens children before departing for Sunspear — he takes time to say goodbye to his favorites despite his pain; hospitality/warmth character note |
| object | AFFC | affc-the-soiled-knight-01:57 | The ornate copper-and-gold serpent arm coil Arianne wears as her only garment in the seduction scene — artifact detail worth a node? (no armor, purely ornamental) |
| object | AFFC | affc-the-queenmaker-01:289 | Hotah's longaxe: "Hotah's longaxe took his right arm off at the shoulder, spun away spraying blood, and came flashing back again in a terrible two-handed slash that removed the head of Arys Oakheart" — weapon in action |
