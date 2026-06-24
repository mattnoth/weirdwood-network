# Lens 2 — Secondary-character sub-arcs + SUSPECTED_OF/WITNESS substrate
## Cersei's-downfall enrichment (S140)
## Proposed by: Lens 2 agent

---

## NEW NODES

### 1. `murder-of-the-old-high-septon`
- **Type:** event.incident
- **Identity:** Osney Kettleblack smothers the previous High Septon on Cersei's orders, enabling the High Sparrow's election
- **Anchor quote (affc-cersei-10.md:243):** `"That one there. She's the queen I fucked, the one sent me to kill the old High Septon. He never had no guards. I just come in when he was sleeping and pushed a pillow down across his face."`
- **Note on timing in text:** The murder is revealed in ch.10; Cersei's reference to the old High Septon's death appears as early as ch.4 (the bells, "He was only a High Septon") and ch.6 where Cersei privately considers getting rid of the new one as she did the last. The killing preceded the story's start — it is a backstory event surfaced by Osney's confession.

### 2. `cersei-sends-osney-to-seduce-margaery`
- **Type:** event.conspiracy
- **Identity:** Cersei commissions Osney Kettleblack to seduce Margaery Tyrell as the frame for the treason charge
- **Anchor quote (affc-cersei-04.md:357):** `"Pluck the little rose for me, and you will not find me to be ungrateful."`
- **Note:** This is the originating act of Cersei's frame conspiracy against Margaery; distinct from the spine node `cersei-plots-against-margaery` (which covers the broader conspiracy), this is the specific seduction-commission sub-event.

### 3. `qyburn-tortures-blue-bard-into-false-confession`
- **Type:** event.incident
- **Identity:** Qyburn tortures the Blue Bard (Wat) through the night until he produces a false confession naming Margaery's lovers
- **Anchor quote (affc-cersei-09.md:199):** `"By dawn the singer's high blue boots were full of blood, and he had told them how Margaery would fondle herself as she watched her cousins pleasuring him with their mouths."`

### 4. `creation-of-robert-strong`
- **Type:** event.incident
- **Identity:** Qyburn conducts forbidden experiments on Gregor Clegane's dying body, producing the resurrected champion Robert Strong
- **Anchor quote (affc-cersei-07.md:124–125):** `"What he lacks in gallantry he will give you tenfold in devotion. He will protect your son, kill your enemies, and keep your secrets, and no living man will be able to withstand him." / "They will sing of him, I swear it." Lord Qyburn's eyes crinkled with amusement. "Might I ask about the armor?"`
- **Note:** The chapter confirms Qyburn's ongoing work on the Mountain (ch.2: "Do what you will with him … confine your studies to the black cells. When he dies, bring me his head.") and its culmination into the promised unkillable champion is explicit by ch.7's armor order.

---

## EDGES

### Kettleblack web

**E1.**
`cersei-lannister --[SUSPECTED_OF]--> murder-of-the-old-high-septon`
| Tier: 2 | affc-cersei-10.md:243 | `"She's the queen I fucked, the one sent me to kill the old High Septon."` | Osney's confession names Cersei as the one who sent him; the act itself is Osney's, Cersei's role is unproven beyond a tortured confession — SUSPECTED_OF is correct per agency rules.

**E2.**
`osney-kettleblack --[AGENT_IN]--> murder-of-the-old-high-septon`
| Tier: 2 | affc-cersei-10.md:243 | `"I just come in when he was sleeping and pushed a pillow down across his face."` | Osney confesses to the physical act.

**E3.**
`murder-of-the-old-high-septon --[ENABLES]--> cersei-rearms-the-faith-and-forgives-the-debt`
| Tier: 2 | affc-cersei-06.md:189 | `"those doors had given way, and the sparrows came pouring into the Great Sept with their leader on their shoulders and their axes in their hands"` | Removing the old High Septon enabled the High Sparrow's election, which is the precondition for Cersei's deal to rearm the Faith. Rationale: the Sparrow's leverage depends on his authority, which required the old incumbent's death.

**E4.**
`cersei-lannister --[AGENT_IN]--> cersei-sends-osney-to-seduce-margaery`
| Tier: 1 | affc-cersei-04.md:357–361 | `"Pluck the little rose for me, and you will not find me to be ungrateful." ... "Tommen is not Aegon the Unworthy ... I mean for Margaery to lose her head, not you."` | Cersei directly commissions the seduction scheme.

**E5.**
`osney-kettleblack --[AGENT_IN]--> cersei-sends-osney-to-seduce-margaery`
| Tier: 1 | affc-cersei-04.md:399 | `"I am your man."` | Osney accepts the commission.

**E6.**
`cersei-sends-osney-to-seduce-margaery --[CAUSES]--> cersei-plots-against-margaery`
| Tier: 1 | affc-cersei-04.md:411 | `"I was made for this, she told herself. It was the sheer elegance of it that pleased her most."` | The seduction scheme is the first concrete step in Cersei's conspiracy against Margaery; it causes the broader plot to crystallize.
- **NOTE:** This edge would connect the new node to the existing spine node. If the orchestrator prefers to keep `cersei-sends-osney-to-seduce-margaery` as a SUB_BEAT_OF `cersei-plots-against-margaery` rather than CAUSES, that is also defensible — the seduction-commission is constitutive of the plot. Flagging for orchestrator decision.

**E7.**
`cersei-lannister --[LOVER_OF]--> osney-kettleblack`
| Tier: 1 | affc-cersei-04.md:344–347 | `"You've had me." / "Only once." He grabbed her left breast again and gave it a clumsy squeeze that reminded her of Robert.` | Text confirms a prior sexual encounter; Cersei's manipulation of Osney throughout is explicitly erotic. The "once" confirms consummation.

**E8.**
`osmund-kettleblack --[WITNESS_IN]--> cersei-sends-osney-to-seduce-margaery`
| Tier: 1 | affc-cersei-05.md:79–107 | `"Ser Osmund fell in beside her on the steps ... 'How is your little brother faring, pray?' Ser Osmund looked uneasy. 'Ah … well enough, only …'"` | Osmund is explicitly the go-between reporting on Osney's progress; he knows the full scheme.

**E9.**
`cersei-fills-in-the-arrest-warrants --[CAUSES]--> osney-kettleblack-confesses-to-high-sparrow`
| Tier: 1 | affc-cersei-09.md:311 + affc-cersei-10.md:27 | `"No, you must take yourself to the Great Sept of Baelor this very night and speak with the High Septon"` (ch.9:311) / `"Ser Osney Kettleblack has confessed his carnal knowledge of the queen to the High Septon himself"` (ch.10:27) | Cersei's plan sends Osney to confess; the arrest warrants are her parallel activation of the same plan. The ISLANDED `cersei-fills-in-the-arrest-warrants` should be wired into the causal chain here. Cersei fills the warrants *after* Osney's confession triggers the machinery — so: warrants are CAUSED BY the confession, not the other way around.
- **CORRECTION on direction:** The confession (ch.10) precedes the scene where Cersei fills the warrants (also ch.10, after the throne room scene). The causal chain is: `osney-kettleblack-confesses-to-high-sparrow --TRIGGERS--> cersei-is-captured-in-the-sept` (already exists). The `cersei-fills-in-the-arrest-warrants` is a parallel response to Osney's confession — it is CAUSED BY the confession: `osney-kettleblack-confesses-to-high-sparrow --CAUSES--> cersei-fills-in-the-arrest-warrants`. Proposing that direction.

**E10 (revised E9).**
`osney-kettleblack-confesses-to-high-sparrow --[CAUSES]--> cersei-fills-in-the-arrest-warrants`
| Tier: 1 | affc-cersei-10.md:73–77 | `"There are some warrants that I need you to sign." For the king's sake, the queen had left the names off the arrest warrants. Tommen signed them blank, and pressed his seal into the warm wax happily … Ser Osfryd Kettleblack arrived as the ink was drying. Cersei had written in the names herself: Ser Tallad the Tall …"` | Osney's confession exposed the named men as Margaery's alleged lovers; Cersei uses that list to fill the warrants immediately after the throne room hearing. This wires the ISLANDED node into the causal chain.

### Qyburn sub-arc

**E11.**
`qyburn --[AGENT_IN]--> qyburn-tortures-blue-bard-into-false-confession`
| Tier: 1 | affc-cersei-09.md:191 | `"Qyburn said, 'Your Grace, mayhaps this poor man only played for Margaery whilst she entertained other lovers.' … Lord Qyburn ran a hand up the Blue Bard's chest. 'Does she take your nipples in her mouth during your love play?' He took one between his thumb and forefinger, and twisted."` | Qyburn personally conducts the torture.

**E12.**
`blue-bard --[VICTIM_IN]--> qyburn-tortures-blue-bard-into-false-confession`
| Tier: 1 | affc-cersei-09.md:173–199 | `"Iron shackles held him hard against the cold stone wall." … "By dawn the singer's high blue boots were full of blood"` | The Blue Bard is the torture victim.

**E13.**
`cersei-lannister --[COMMANDS_IN]--> qyburn-tortures-blue-bard-into-false-confession`
| Tier: 1 | affc-cersei-09.md:167–168 | `"Lord Orton, summon my guards and take this creature to the dungeons." … "Let him sing for Lord Qyburn."` | Cersei orders the arrest and hands the Blue Bard to Qyburn.

**E14.**
`qyburn-tortures-blue-bard-into-false-confession --[CAUSES]--> cersei-confronts-and-arrests-the-blue-bard`
| — **REJECT** | These are the same event; the smashing of the lute IS the arrest — the torture follows immediately in the same scene. SUB_BEAT_OF, not CAUSES. Do not propose.

**E14 (substituted).**
`qyburn-tortures-blue-bard-into-false-confession --[ENABLES]--> cersei-plots-against-margaery`
| Tier: 1 | affc-cersei-09.md:213 | `"I prefer this song to the other … Osney is the plum that makes the pudding."` | The false confession from the Blue Bard gives Cersei the witness testimony she needs to make the plot actionable. ENABLES (door-opener / precondition for the Osney-confession step).

**E15.**
`qyburn --[AGENT_IN]--> creation-of-robert-strong`
| Tier: 1 | affc-cersei-02.md:219 | `"The Mountain is yours. Do what you will with him, but confine your studies to the black cells."` + affc-cersei-07.md:124 | `"What he lacks in gallantry he will give you tenfold in devotion. He will protect your son, kill your enemies, and keep your secrets, and no living man will be able to withstand him."` | Qyburn is the active agent performing the resurrection/reanimation.

**E16.**
`gregor-clegane --[VICTIM_IN]--> creation-of-robert-strong`
| Tier: 1 | affc-cersei-02.md:205–209 | `"his veins have turned black from head to heel … It is a wonder that the man is still alive … 'The Mountain is yours. Do what you will with him'"` | Gregor is the subject of Qyburn's experiments.

**E17.**
`creation-of-robert-strong --[ENABLES]--> cersei-is-stripped-and-imprisoned` (downstream fix — see NOTES)
| Tier: 1 | affc-cersei-10.md:307–309 | `"Hope remains. Your Grace has the right to prove your innocence by battle. My queen, your champion stands ready. There is no man in all the Seven Kingdoms who can hope to stand against him."` | Robert Strong is Cersei's potential champion at trial — the only reason Cersei has any route out of imprisonment. This wires `cersei-is-stripped-and-imprisoned`'s dead-end downstream. The node ENABLES a possible escape path from the imprisonment (the trial-by-battle option Cersei ultimately pursues in ADWD).

### Taena Merryweather sub-arc

**E18.**
`taena-merryweather --[INFORMS]--> cersei-lannister`
| Tier: 1 | affc-cersei-03.md:173–177 | `"There is something you must know. Your maid is bought and paid for. She tells Lady Margaery everything you do." … "Have her followed. Margaery never meets with her directly. Her cousins are her ravens … Put your own man in the gallery on the morrow"` | Taena proactively delivers intelligence about Senelle's spy role; this is a turning point in Cersei's plot.

**E19.**
`taena-merryweather --[CONSPIRES_WITH]--> cersei-lannister`
| Tier: 1 | affc-cersei-09.md:247–253 | `"'Which one is the innocent?' / 'Alla.' / 'The shy one?' / 'So she seems, but there is more of sly than shy in her. Leave her to me, my sweet.' / 'Gladly.'"` | Taena actively co-designs the evidence scheme against Margaery, taking the Alla Tyrell angle.

**E20.**
`orton-merryweather --[AGENT_IN]--> cersei-confronts-and-arrests-the-blue-bard`
| Tier: 1 | affc-cersei-09.md:163–165 | `"Lord Orton, summon my guards and take this creature to the dungeons." / Orton Merryweather's face was damp with fear.` | Orton, as justiciar, physically executes the arrest.

### Lancel thread

**E21.**
`lancel-lannister --[WITNESS_IN]--> cersei-is-captured-in-the-sept`
| Tier: 1 | affc-cersei-10.md:243–244 | `"That one there. She's the queen I fucked, the one sent me to kill the old High Septon."` | Osney's full confession (which implicates Cersei and is delivered to the High Sparrow) triggers the capture. Lancel is present in the sept as a Warrior's Son — he is at affc-cersei-08.md:147: `"there he stood with the other pious fools"` among the Warrior's Sons who accompany Septon Raynard to court. However, the text does not place Lancel *specifically* at Cersei's capture scene. **RETRACT** — insufficient text anchor to place Lancel as WITNESS_IN at the capture.

**E21 (substituted).**
`lancel-lannister --[MEMBER_OF]--> the-faith`
| Tier: 1 | affc-cersei-08.md:147 | `"there was Lancel. She had thought Qyburn must be japing when he had told her that her mooncalf cousin had forsaken castle, lands, and wife and wandered back to the city to join the Noble and Puissant Order of the Warrior's Sons, yet there he stood with the other pious fools."` | Lancel joins the Warrior's Sons, aligning himself with the Faith that will later arrest Cersei.

**E22.**
`lancel-lannister --[BETRAYS]--> cersei-lannister`
| Tier: 2 | affc-cersei-02.md:85–87 | `"He had been much more amusing when he was trying to be Jaime. What has this mewling fool told the High Septon? And what will he tell his little Frey when they lie together in the dark? If he confessed to bedding Cersei, well, she could weather that … If he sings of Robert and the strongwine, though …"` | Cersei explicitly fears Lancel's confession. His joining the Faith confirms the threat is real; the betrayal is completed when Osney's testimony exposes the pattern. Tier 2 because the text shows fear/anticipation, not confirmed betrayal within these chapters.

### Maggy the Frog / prophecy substrate

**E23.**
`maggy-the-frog --[MOTIVATES]--> cersei-lannister`
| Tier: 1 | affc-cersei-08.md:328–340 | `"I must be strong. What I must do I do for Tommen and the realm. It was a pity that Maggy the Frog was dead … 'If she tries I will have my brother kill her.'" / "Knowing what needed to be done was one thing … she would have had Margaery doing all these things as well."` | Cersei explicitly connects Maggy's prophecy about the "younger queen" to her decision to destroy Margaery. The prophecy MOTIVATES Cersei (the character) in the causal chain — this is textbook MOTIVATES usage.

---

## HARVEST

- affc-cersei-01.md:25 — food/drink: "lemon water" Cersei drinks on discovering her father's death ("Jocelyn was trembling like a leaf … Cersei took a sip: water, mixed with lemon squeezings, so tart she spit it out")
- affc-cersei-01.md:113–114 — physical description: three Kettleblacks described together ("Ser Osney had faint scratches on his cheek where another of Tyrion's whores had clawed him")
- affc-cersei-02.md:32–33 — description/object: High Septon's crown given by Tywin, and ironic note that the present High Septon was "Tyrion's making" / food at Kevan's supper: "beets and bread and bloody beef with a flagon of Dornish red"
- affc-cersei-02.md:206 — object: Qyburn finds a Gardener-dynasty gold coin (Hand sigil) under Rugen's chamber pot — evidence of Tyrell/Imp plot, never followed up by the graph
- affc-cersei-03.md:17–18 — food: "two boiled eggs, a loaf of bread, and a pot of honey" — finds bloody chick inside first egg, refuses it; orders "hot spiced wine"
- affc-cersei-03.md:147–148 — wedding feast details: "Only seven courses were served. Butterbumps and Moon Boy entertained … musicians played … The only singer was some favorite of Lady Margaery's … called himself the Blue Bard." First appearance of Blue Bard at Tommen's wedding.
- affc-cersei-03.md:252–253 — wildfire/fire description: Tower of the Hand burning with wildfire — green flames, "Fifty pots had been placed inside"
- affc-cersei-04.md:127–128 — Cersei's strategic thinking on Taena: "under it, she smelled ambition" — good PERCEIVED_AS material
- affc-cersei-04.md:339–341 — Cersei/Osney physical detail: "She let him touch her breasts through the silk of her gown … You've had me. / Only once." — confirms LOVER_OF consummation
- affc-cersei-05.md:297–312 — Cersei/Falyse supper: food = "hippocras … herb-crusted pike, and ribs of wild boar … hot-baked bread, buttered beets" — note Cersei "had become very fond of boar since Robert's death"
- affc-cersei-06.md:265–266 — quote: High Sparrow's proposition to Cersei: "The Faith Militant reborn … that would be the answer to three hundred years of prayer, Your Grace." Key verbatim for rearms-the-faith event.
- affc-cersei-07.md:141–148 — Taena shares Cersei's bed, first confirmed; Cersei's memories of Robert's sexual assault in context of comparing with Taena (foreshadowing/psychology material)
- affc-cersei-08.md:197–260 — Maggy the Frog prophecy — full text rendered in Cersei's dream; verbatim of three questions and answers; valonqar prophecy exact wording: "the valonqar shall wrap his hands about your pale white throat and choke the life from you" — load-bearing for theories track
- affc-cersei-09.md:173–175 — description/torture: Blue Bard's blue hair ("washed in rosewater"), blue calfskin boots, "brown" natural hair color (contrast detail)
- affc-cersei-09.md:339–340 — physical: Osney's sexual coercion of Cersei: "He thrust his fingers inside the bodice of her gown and yanked, and the silk parted with a ripping sound"
- affc-cersei-10.md:135 — description: Margaery's cell, "eight feet long and six feet wide, no furnishings but a straw-stuffed pallet and a bench for prayer, a ewer of water, a copy of The Seven-Pointed Star, and a candle"
- affc-cersei-10.md:249–251 — quote/capture: "Inside the cell three silent sisters held her down as a septa named Scolera stripped her bare. She even took her smallclothes." — confirms Scolera's role, silent sisters present

---

## NOTES

**Dedup checks:**
- `osney-kettleblack`, `osmund-kettleblack`, `osfryd-kettleblack`, `qyburn`, `taena-merryweather`, `orton-merryweather`, `lancel-lannister`, `blue-bard`, `high-sparrow`, `maggy-the-frog` all confirmed as existing nodes in baseline — no re-minting needed.
- `robert-strong` exists as a character node per the baseline. The creation-event is NEW.
- `high-septon` (title node) exists. The old High Septon who was murdered is not an individually named character node — he is referenced by title only in the text ("the old High Septon"). If the orchestrator wants to model him as a character node, the text's only identifier is "the old High Septon" / "his predecessor" in Cersei's references. Propose leaving unmodeled as separate character unless needed.

**Considered and rejected:**
- `cersei-lannister --LOVER_OF--> taena-merryweather`: The text is explicit that Cersei felt nothing ("It was no good … It had never been any good with anyone but Jaime," affc-cersei-07.md:267–269). Taena's role is an intimacy exchange, not a genuine love relationship; Cersei uses it instrumentally. The edge would be misleading. Kept as HARVEST note instead.
- `cersei-lannister --KILLS--> senelle`: Cersei gives Senelle to Qyburn ("I gave you Senelle," affc-cersei-05.md:217), who confirms she is "quite exhausted" (affc-cersei-08.md:305). No explicit death confirmed in text. Qyburn uses her for experiments. KILLS is unwarranted; SUSPECTED_OF (via Qyburn) would work but is marginal.
- `cersei-lannister --KILLS--> lady-falyse`: Same pattern — given to Qyburn affc-cersei-07.md:235. "No longer capable of ruling Stokeworth" (affc-cersei-08.md:305). No death confirmed within these chapters. Dropped.
- `cersei-lannister --SUSPECTED_OF--> murder-of-old-high-septon` edge already in E1 as best possible given agency rules.
- Loras Tyrell sending / Dragonstone siege: Out of scope for this lens (not secondary characters in the Cersei-downfall arc).

**Key causal wiring summary this lens proposes:**
1. `murder-of-the-old-high-septon` wired in (backstory event, new node)
2. `cersei-fills-in-the-arrest-warrants` de-islanded: receives CAUSES edge from `osney-kettleblack-confesses-to-high-sparrow`
3. `cersei-is-stripped-and-imprisoned` dead-end fixed: `creation-of-robert-strong --ENABLES--> cersei-is-stripped-and-imprisoned` (offers the only escape route from the imprisonment)
4. Maggy prophecy → Cersei psychology engine: `maggy-the-frog --MOTIVATES--> cersei-lannister`
