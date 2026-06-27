# Lens B — Whodunit / Informer Mystery + SUSPECTED_OF — A1.5 Dorne proposal (S156)

> Prepared by: Lens B subagent. Focus: (B) the "someone always tells" informer mystery, the interrogation/captivity
> layer, the Darkstar betrayal-of-intent whodunit, and all SUSPECTED_OF-class evidence edges.

---

## THE INFORMER — Critical Reading

**The text does NOT name the informer.** Doran refuses to say: *"I can think of no reason why I should."*
What the text gives us is:
1. Doran's non-answer: *"I am the Prince of Dorne. Men seek my favor."* (affc-the-princess-in-the-tower-01:185)
2. Arianne's own elimination-of-suspects reasoning (lines 51–53): she rules out Darkstar because *"if Ser Gerold had been the worm in the apple, why would he have turned his sword upon Myrcella?"*; she entertains but does not resolve the Arys hypothesis.
3. Doran's admission that he let the plot proceed after knowing: *"I had to learn the truth."* — implying the informer told him early enough to stage the ambush at leisure.
4. A structural clue: whoever told had knowledge of (a) the destination (the Greenblood, the poleboat rendezvous), (b) the timing, and (c) the disguise operation at the palace (the Rosamund stand-in). This is operationally specific — not just knowledge that a plot existed, but tactical detail.

**The text points at but does not prove any single suspect.** Candidates the text raises or leaves open:
- **Arys Oakheart** — Arianne herself entertains this (line 53): *"Had the white knight's guilt won out over his lust? Had he loved Myrcella more than her and betrayed his new princess to atone for his betrayal of the old?"* — but she reaches no conclusion, and his suicide charge is ambiguous (guilt/shame/love, not necessarily informer's self-punishment). SUSPECTED_OF is supported by text.
- **Maester Caleotte** — The structural informer: he is the prince's eyes inside the palace; he knew about Myrcella's "redspots" ruse because Arys told him directly (affc-the-queenmaker-01:183–187), he was shown to monitor Tyene for poison at the Tower of the Sun (affc-the-captain-of-guards-01:317), and Arianne wonders in prison whether Caleotte is *"drawing a proclamation to name her brother Quentyn heir"* (affc-the-princess-in-the-tower-01:121). He also reported Arys Oakheart's letter-writing habit to Doran: *"Her white knight will be with her … and you know he sends letters to his queen."* (affc-the-captain-of-guards-01:131–132). SUSPECTED_OF is strongly supported by circumstance.
- **Cedra** — The serving girl Arianne later tries to use as a courier. She was "sent to the Water Gardens" by Doran after being caught (affc-the-princess-in-the-tower-01:127). Earlier the chapter notes *"Garin had boasted of bedding her once"* (line 76) — and Garin was one of the conspirators. The text does not say Cedra informed on the plot, but her connection to Garin and her removal by Doran right after Arianne tried to use her creates structural suspicion. The timing is WRONG for the main betrayal (the plot was betrayed before the chapter began; Cedra is caught AFTER the arrest), so Cedra as PRIMARY informer is REJECTED. She is not a SUSPECTED_OF candidate for this specific betrayal.
- **Garin** — Arianne's milk-brother and conspirator, but the text dismisses him as unlikely ("friends of her girlhood, as dear to her as her cousin Tyene. She could not believe they would inform on her…"). His gossip habits are mentioned by Doran (line 301: *"Garin gossips as only the orphans can"*), but this is Doran explaining why he kept his betrothal-pact secret, not naming Garin as the informer.
- **Darkstar** — Arianne herself eliminates him on logical grounds (line 51): if he were the informer and wanted the plot stopped, why try to kill Myrcella? His act at the Greenblood is INCONSISTENT with a betrayer who tipped Doran — it is more consistent with a man trying to trigger a war the plot was deliberately NOT triggering.

**Verdict for graph:** Two SUSPECTED_OF edges are textually defensible:
1. `arys-oakheart SUSPECTED_OF the-queenmaker-plot` (Arianne explicitly suspects him; the timing is right — he was tormented by guilt the entire time; his suicide charge at Hotah could be read as self-punishment for betrayal). Tier-2. [BORDERLINE] — the text neither confirms nor refutes.
2. `caleotte SUSPECTED_OF the-queenmaker-plot` — not stated by Arianne (she never suspects him explicitly in the published text), but the structural evidence is overwhelming: he has the access, Doran's confidence, and is the one character Doran would protect with a non-answer. [BORDERLINE] — this is a reader inference, not an in-text accusation; mark carefully.

**Arys as stronger SUSPECTED_OF candidate than Caleotte in-text:** Arianne actually voices the Arys hypothesis on the page; Caleotte is a reader/structural inference. Both warrant SUSPECTED_OF edges but with different textual grounding.

---

## Proposed NEW nodes

### 1. Conspirator: Andrey Dalt (Drey)
**Slug:** `andrey-dalt`
**Name:** Andrey Dalt
**Type:** character.human
**Body:** Ser Andrey Dalt, called "Drey," heir to Lemonwood in Dorne, one of Arianne Martell's closest companions since childhood. He was one of the five co-conspirators in the Queenmaker plot, knelt to Myrcella as queen at Shandystone, yielded when Hotah sprang the ambush, and was subsequently punished by Doran Martell with three years of service in Norvos.
**Anchor quote:** "I give you Ser Andrey Dalt, the heir to Lemonwood." + "Ser Andrey has been sent to Norvos to serve your lady mother for three years."
**Chapter:line:** `affc-the-queenmaker-01:124` + `affc-the-princess-in-the-tower-01:217`

### 2. Conspirator: Garin of the Orphans
**Slug:** `garin-of-the-orphans`
**Name:** Garin (of the Orphans of the Greenblood)
**Type:** character.human
**Body:** Garin, an orphan of the Greenblood and Arianne Martell's milk-brother (his mother was Arianne's wet nurse), one of her five closest companions and co-conspirators in the Queenmaker plot. He knelt to Myrcella at Shandystone, yielded peacefully when the ambush fell, and was sentenced by Doran to two years in Tyrosh, with coin and hostages taken from his kin among the orphans.
**Anchor quote:** "Here is gay Garin of the orphans, who makes me laugh. His mother was my wet nurse."
**Chapter:line:** `affc-the-queenmaker-01:137`

> **BUG FLAG:** The existing edge `arianne CONSPIRES_WITH garin-the-great` is a WRONG-TARGET BUG. It should point to `garin-of-the-orphans`, not to the legendary Rhoynar prince Garin the Great. The synthesis orchestrator should re-point this edge to the new `garin-of-the-orphans` node.

### 3. Conspirator: Sylva Santagar (Spotted Sylva)
**Slug:** `sylva-santagar`
**Name:** Sylva Santagar ("Spotted Sylva")
**Type:** character.human
**Body:** Lady Sylva Santagar, called "Spotted Sylva" for her freckles, heir to Spottswood, one of Arianne Martell's dearest friends since childhood and a co-conspirator in the Queenmaker plot. She knelt to Myrcella at Shandystone and was present at the Greenblood when the ambush fell. Doran Martell arranged no formal punishment for her but arranged her marriage to Lord Estermont of Greenstone to disperse the conspirators.
**Anchor quote:** "Might I present Lady Sylva Santagar, my queen? My dearest Spotted Sylva."
**Chapter:line:** `affc-the-queenmaker-01:131`

---

## Proposed NEW edges

> Format: `source  [EDGE_TYPE]  target  |  Tier  |  qualifier (if req'd)  |  verbatim quote + chapter:line  |  rationale`

---

### WHODUNIT / INFORMER LAYER

**B-01**
`arys-oakheart  SUSPECTED_OF  the-queenmaker-plot`
| Tier-2 | — |
Quote: *"Someone told. Could it have been Ser Arys? Had the white knight's guilt won out over his lust? Had he loved Myrcella more than her and betrayed his new princess to atone for his betrayal of the old? Was he so ashamed of what he'd done that he threw his life away at the Greenblood rather than live to face dishonor?"*
`affc-the-princess-in-the-tower-01:53`
Rationale: Arianne explicitly voices this hypothesis in the text, making it a genuine in-world suspicion. Arys had the full operational picture (destination, timing, palace cover-story), was consumed by shame throughout, and his suicide charge could be read as either desperation or self-punishment for betrayal. Text neither confirms nor refutes. **[BORDERLINE]** — do not assert as fact.

---

**B-02**
`caleotte  SUSPECTED_OF  the-queenmaker-plot`
| Tier-2 | — |
Quote: *"I am the Prince of Dorne. Men seek my favor."*
`affc-the-princess-in-the-tower-01:185`
Rationale: Doran's refusal to name the informer ("I can think of no reason why I should") protects someone worth protecting — most likely a trusted household member. Caleotte is the structural candidate: Doran's maester, privy to palace comings-and-goings, the one who fielded the "redspots" ruse Arys used (affc-the-queenmaker-01:183–187), Doran's attendant during all political moments, and already noted by Doran to monitor Arys's letter-writing (`affc-the-captain-of-guards-01:131`). Arianne herself never suspects him in the published text — this is a reader/structural inference, not an in-text accusation. **[BORDERLINE]** — structural inference only, Tier-2 ceiling.

---

### ARYS OATH-BREAKING LAYER

**B-03**
`arys-oakheart  BREAKS_VOW  myrcella-baratheon`
| Tier-1 | — |
Quote: *"She is tearing me apart … I swore a vow … not to wed or father children."*
`affc-the-soiled-knight-01:215`
Rationale: Arys explicitly names the vow he is breaking (Kingsguard celibacy oath, sworn to the office) and acknowledges that his affair constitutes its violation. `BREAKS_VOW` per schema: vow-breaker → the vow-recipient. The Kingsguard oath runs to the king/crown, but Arys is specifically assigned to Myrcella and frames his vow in terms of his duty to her protection — she is the most natural recipient node given the arc's scope. The queen (Cersei) is the institutional recipient, but Myrcella is the proximate ward.
> **Note to synthesis:** `arys-oakheart BREAKS_VOW cersei-lannister` (queen/crown as vow-recipient) is arguably more precise institutionally; pick one. I propose Myrcella as she is the arc's victim-ward.

---

**B-04**
`arianne-martell  MANIPULATES  arys-oakheart`
| Tier-1 | qualifier: `via_seduction` |
Quote: *"My lady? Where are you?" "Here." She stepped out from the shadow behind the door. An ornate snake coiled around her right forearm, its copper and gold scales glimmering when she moved. It was all she wore.*
`affc-the-soiled-knight-01:54–57` (cite as line 55)
Rationale: Gap 2 from baseline.md. Arianne's seduction of Arys is the arc's central mechanism — the "Soiled Knight" chapter is entirely about her using sex and emotional manipulation to turn him into a willing instrument of the Queenmaker plot. She is explicit elsewhere about her tactics: *"I fucked him, Father. You did command me to entertain our noble visitors."* (`affc-the-princess-in-the-tower-01:219`). MANIPULATES with qualifier `via_seduction` is the precise type for seduction-as-instrument (per LENS-SHARED.md — NO `SEDUCES` type exists). The LOVER_OF edge already exists; this adds the instrumental using-him-as-a-tool layer.
**Alternate quote (more explicit about the instrumental goal):** *"Set a crown upon her head." … She is tearing me apart.* — but the scene-opening nakedness is the purest MANIPULATES moment.

---

**B-05**
`arianne-martell  DECEIVES  arys-oakheart`
| Tier-1 | — |
Quote: *"I told him that once Myrcella was the queen she would give us leave to marry. He wanted me for his wife."*
`affc-the-princess-in-the-tower-01:223`
Rationale: Arianne admits in the interrogation scene to promising Arys marriage as a reward for participating in the plot. This is a deliberate false promise — Arianne is a princess who knows she cannot marry a Kingsguard (she acknowledges this in the Soiled Knight: "you know I cannot marry you"). She used the marriage promise instrumentally to secure his compliance. DECEIVES (source deceives target) captures this: she fed Arys a known-to-be-false promise to induce action.

---

**B-06**
`arys-oakheart  DISTRUSTS  arianne-martell`
| Tier-2 | — |
Quote: *"We should not be doing this … I am afraid … I fear for my honor, and for yours … This must end … I am my cloak. And this must end."*
`affc-the-soiled-knight-01:70–115` (cite line 101)
Rationale: Throughout the Soiled Knight chapter, Arys oscillates between desire and distrust/shame. He recognizes she is pulling him somewhere: "She is tearing me apart." His repeated "this must end" and his attempt to disengage show that beneath the desire he does not fully trust that her motives are pure. **[BORDERLINE]** — this reads more as conflicted guilt/shame than active distrust of her intentions; DISTRUSTS may be too strong. The edge captures a real pattern but is slightly over-assertive. The synthesis gate should scrutinize.

---

### DARKSTAR BETRAYAL-OF-PLOT-INTENT LAYER

**B-07**
`gerold-dayne  SUBVERTS  the-queenmaker-plot`
| Tier-1 | — |
Quote: *"This is how you start a war. Not with a crown of gold, but with a blade of steel."*
`affc-the-queenmaker-01:91`
Rationale: Darkstar explicitly states at Shandystone that crowning Myrcella is a "hollow gesture" that will not produce the war he wants, and draws his sword to propose killing her instead ("the girl moved"). At the Greenblood he strikes Myrcella — an act that subverts the plot's stated purpose (to crown her and avoid Lannister-Dornish war through a fait accompli). The plot's goal was a *living* crowned Myrcella; Darkstar's act made her a mutilated diplomatic incident. SUBVERTS (undermines/works against a goal/plan) captures this more precisely than BETRAYS (which connotes disloyalty to a person). He was never fully loyal — he disagreed from the start.

---

**B-08**
`gerold-dayne  SUSPECTED_OF  myrcella-is-maimed-by-darkstar`
| Tier-2 | — |
Quote: *"All eyes were on your white knight so no one seems quite certain just what happened, but it would appear that her horse shied away from his at the last instant, else he would have taken off the top of the girl's skull."*
`affc-the-princess-in-the-tower-01:169`
Rationale: The text does not assert a deliberate intent to kill with certainty — "no one seems quite certain just what happened." Doran's phrasing acknowledges ambiguity. Darkstar's own words ("I meant to take her ear … but the girl moved") are not quoted in this chapter, but the maiming itself is fact. The AGENT_IN edge already exists (from baseline). SUSPECTED_OF here captures the contested-intent layer: was the maiming a deliberate war-spark or a botched killing? **[BORDERLINE]** — AGENT_IN is already minted; SUSPECTED_OF may be redundant. Drop if the gate deems AGENT_IN sufficient.

---

**B-09**
`gerold-dayne  HATES  the-queenmaker-plot`
| Tier-2 | — |
Quote: *"Crowning the Lannister girl is a hollow gesture. She will never sit the Iron Throne. Nor will you get the war you want."*
`affc-the-queenmaker-01:87`
Rationale: Darkstar's contempt for the plot's strategy is stated plainly. He views crowning Myrcella as ineffectual and thinks only violence produces war. HATES (strong opposition/contempt) captures his attitude toward the plan itself. **[BORDERLINE]** — HATES is typically person→person in the graph; using it against an event is unusual. Consider OPPOSES instead if the synthesis prefers person→event typing. OPPOSES is in the locked vocabulary.

**Alternative formulation:**
`gerold-dayne  OPPOSES  the-queenmaker-plot`
| Tier-1 | — |
Same quote.
Rationale: OPPOSES may be cleaner than HATES for a person↔plot relationship. Same textual basis. Prefer OPPOSES over HATES here.

---

### DORAN'S SURVEILLANCE / FOREKNOWLEDGE LAYER

**B-10**
`doran-martell  SPIES_ON  the-queenmaker-plot`
| Tier-2 | — |
Quote: *"I am the Prince of Dorne. Men seek my favor."*
`affc-the-princess-in-the-tower-01:185`
Rationale: Doran explicitly acknowledges he knew of the plot before it executed. His phrasing — "Men seek my favor" — implies an informer network, not mere happenstance. This SPIES_ON edge (Doran → the plot as the watched entity) captures his active surveillance posture. Tier-2 because the mechanism is implied, not described — we know the outcome (foreknowledge) but not the surveillance architecture. **[BORDERLINE]** — SPIES_ON typically implies active observation; if the informer came to him voluntarily, INFORMS might be more accurate. But since we don't know who or how, SPIES_ON covers a watched-and-known posture plausibly. The synthesis can re-type as INFORMS(unknown→doran) if preferred.

---

**B-11**
`doran-martell  INFORMS  areo-hotah`
| Tier-1 | — |
Quote: *"Quick and quiet and bloodless, aye. What is your command?" "You will find my brother's daughters, take them into custody, and confine them in the cells atop the Spear Tower."*
`affc-the-captain-of-guards-01:340–341`
Rationale: Doran explicitly commands Hotah with foreknowledge of the plot — he has the operational picture (arrest the Sand Snakes, prepare the ambush at the Greenblood) and transfers those orders to Hotah. INFORMS (Doran → Hotah) captures the intelligence-handoff from prince to captain that enables the ambush. COMMANDS_IN for the ambush already exists per baseline; INFORMS adds the intelligence-briefing layer before the operation.

---

### CONSPIRATOR WEB WIRING

**B-12**
`andrey-dalt  AGENT_IN  the-queenmaker-plot`
| Tier-1 | — |
Quote: *"Yielding seems the wisest course," he called to Arianne, as his sword thumped to the ground.*
`affc-the-queenmaker-01:269`
Rationale: Gap 3 from baseline.md. Drey is one of the five named co-conspirators; knelt to Myrcella as queen ("Your Grace, I give you Ser Andrey Dalt, the heir to Lemonwood … I am her man"), surrendered at the Greenblood. AGENT_IN (active participant in the event) is warranted. The core_in=0 for andrey-dalt flags this as a real gap.

---

**B-13**
`andrey-dalt  CONSPIRES_WITH  arianne-martell`
| Tier-1 | — |
Quote: *"I give you Ser Andrey Dalt, the heir to Lemonwood." "My friends call me Drey," he said, "and I should be greatly honored if Your Grace would do the same." "Whatever name Your Grace prefers, I am her man."*
`affc-the-queenmaker-01:124–129`
Rationale: Drey knelt as a co-conspirator from the Shandystone gathering forward. He was one of the five riders who made up the queenmaking party. CONSPIRES_WITH captures the mutual plotting relationship.

---

**B-14**
`sylva-santagar  AGENT_IN  the-queenmaker-plot`
| Tier-1 | — |
Quote: *"Might I present Lady Sylva Santagar, my queen? My dearest Spotted Sylva." "For my freckles, Your Grace … though they all pretend it is because I am the heir to Spottswood."*
`affc-the-queenmaker-01:131–135`
Rationale: Gap 3. Spotted Sylva is named as a co-conspirator who knelt to Myrcella and rode with the party to the Greenblood. AGENT_IN captures her active participation.

---

**B-15**
`sylva-santagar  CONSPIRES_WITH  arianne-martell`
| Tier-1 | — |
Quote: *"Drey and Spotted Sylva were her dearest friends … Spotted Sylva helped veil the little princess from the sun."*
`affc-the-queenmaker-01:239` (help-veil-Myrcella action)
Rationale: Same conspiratorial relationship as Drey. Sylva is named as one of Arianne's "dearest friends" and an active member of the riding party. CONSPIRES_WITH is appropriate.

---

**B-16**
`garin-of-the-orphans  AGENT_IN  the-queenmaker-plot`
| Tier-1 | — |
Quote: *"My queen, I am your man." Garin dropped to both knees.*
`affc-the-queenmaker-01:107`
Rationale: Bug-fix companion to the new node. Garin knelt to Myrcella as his queen, rode in the queenmaking party, and was first to spot the poleboat — then stepped back when Hotah appeared. His active role = AGENT_IN. This replaces the wrong-target `arianne CONSPIRES_WITH garin-the-great` after that edge is re-pointed.

---

**B-17**
`garin-of-the-orphans  CONSPIRES_WITH  arianne-martell`
| Tier-1 | — |
Quote: *"Here is gay Garin of the orphans, who makes me laugh … His mother was my wet nurse."*
`affc-the-queenmaker-01:137`
Rationale: Garin is Arianne's milk-brother and the conspirator who arranged the poleboat on the Greenblood for the escape. CONSPIRES_WITH is warranted by his role in organizing the escape route.

---

### CONSPIRATOR DISPERSAL LAYER

**B-18**
`doran-martell  MARRIES_OFF  sylva-santagar`
| Tier-1 | — |
Quote: *"Lady Sylva received no punishment from me, but she was of an age to marry. Her father has shipped her to Greenstone to wed Lord Estermont."*
`affc-the-princess-in-the-tower-01:217`
Rationale: Gap 5 from baseline.md. Doran arranges Sylva's marriage to Estermont of Greenstone as a means of dispersing the conspirators without open punishment. MARRIES_OFF (arranger → married-off person) captures this exactly. Tier-1: verbatim quote from the interrogation scene.

---

**B-19**
`andrey-dalt  TRAVELS_TO  norvos`
| Tier-1 | — |
Quote: *"Ser Andrey has been sent to Norvos to serve your lady mother for three years."*
`affc-the-princess-in-the-tower-01:217`
Rationale: Gap 5. Drey's three-year exile to Norvos is Doran's dispersal punishment. TRAVELS_TO is the most accurate type — a forced journey/assignment. Tier-1: directly stated.

---

**B-20**
`garin-of-the-orphans  TRAVELS_TO  tyrosh`
| Tier-1 | — |
Quote: *"Garin will spend his next two years in Tyrosh. From his kin amongst the orphans, I took coin and hostages."*
`affc-the-princess-in-the-tower-01:217`
Rationale: Gap 5. Garin is sent to Tyrosh for two years with hostages taken from his kin among the orphans. TRAVELS_TO. Tier-1.

---

### DORAN'S PATIENCE / MANIPULATION LAYER

**B-21**
`doran-martell  MANIPULATES  arianne-martell`
| Tier-1 | qualifier: `via_false_information` |
Quote: *"Because I knew that you would spurn him. I had to be seen to try to find a consort for you once you'd reached a certain age, else it would have raised suspicions, but I dared not bring you any man you might accept. You were promised, Arianne."*
`affc-the-princess-in-the-tower-01:293`
Rationale: Doran admits to a years-long deliberate deception: he offered Arianne deliberately terrible suitors (Rosby, Beesbury, Grandison) knowing she would refuse them — to conceal the existence of a secret betrothal pact. This is textbook `via_false_information` MANIPULATES (Doran fed her false impressions of his intent to disinherit her, manipulating her ignorance as part of a larger strategy). The MANIPULATES type requires a qualifier: `via_false_information` fits precisely. Tier-1 because Doran confesses it verbatim.

---

**B-22**
`arianne-martell  DISTRUSTS  doran-martell`
| Tier-2 | — |
Quote: *"You do lie well, Father, I will grant you that. You did not so much as blink."*
`affc-the-princess-in-the-tower-01:269`
Rationale: Arianne's distrust of her father is the emotional engine of the entire arc. She explicitly accuses him of lying during the interrogation scene and has carried the disinheritance fear since age fourteen (reading the letter to Quentyn). DISTRUSTS is well-supported. Tier-2 because distrust of this kind is an ongoing disposition, not a single event.

---

**B-23**
`doran-martell  DECEIVES  arianne-martell`
| Tier-1 | — |
Quote: *"I had other plans for you."* … *"The pact was sealed in secret. I meant to tell you when you were old enough … when you came of age, I thought, but … I know. If I kept you ignorant too long, it was only to protect you."*
`affc-the-princess-in-the-tower-01:287–298`
Rationale: Doran admits he deliberately kept Arianne ignorant of the secret betrothal pact for years, and that this ignorance directly caused her to misread his actions (the suitors, Quentyn's mission) and launch the Queenmaker plot. DECEIVES is Tier-1 — Doran's own confession of deliberate concealment from his daughter. (Distinct from MANIPULATES above, which covers the false-suitor mechanism; this covers the larger secret-keeping.)

---

### FEAR / SHAME LAYERS

**B-24**
`arys-oakheart  FEARS  arianne-martell`
| Tier-2 | — |
Quote: *"I am afraid … I fear for my honor, and for yours … She is tearing me apart."*
`affc-the-soiled-knight-01:101–215`
Rationale: Arys is afraid of what Arianne does to his self-control and honor — she dismantles his identity as a white knight every time he is with her. FEARS captures the terrified aspect of his attraction. Tier-2: this is emotional/dispositional, not a specific threat. **[BORDERLINE]** — could be argued as RESPECTS or simply the existing LOVER_OF. However, FEARS in the graph's usage covers "afraid of what X represents to self" and the text is clear Arys was genuinely terrified of his own desire for her.

---

**B-25**
`arys-oakheart  FEARED  gerold-dayne`
| Tier-1 | — |
Quote: *"By tradition the Kingsguard were the finest knights in all the Seven Kingdoms … but Darkstar was Darkstar."*
`affc-the-queenmaker-01:33`
Rationale: The existing edge `arys FEARS areo-hotah` is already in the baseline. The text shows Arys also feared Darkstar — or at least recognized his exceptional danger. Arianne's internal thought about the risk of Darkstar and Arys conflicting ("we will have blood on the sand. Whose, she could not say") implies both regarded each other as deadly threats. **[BORDERLINE]** — this is Arianne's inference about Arys, not Arys's stated fear. Drop if the gate finds it too indirect.

Note: `arys HATES gerold-dayne` already exists (per dedup baseline for gerold-dayne: `HATES arys`). FEARED may be redundant if HATES captures enough of the dyad. Mark as low-priority.

---

### ARYS MANNER-OF-DEATH / SUICIDE-CHARGE LAYER

**B-26**
`arys-oakheart  ATTACKS  areo-hotah`
| Tier-1 | — |
Quote: *"Ser Arys Oakheart gave her one last longing look, then put his golden spurs into his horse and charged."*
`affc-the-queenmaker-01:281`
Rationale: Arys's suicidal charge at Hotah and the armed poleboat is an ATTACK (against hopeless odds). This is distinct from his death (KILLS already exists: Hotah kills Arys). ATTACKS captures his agency in initiating the combat. Tier-1.

---

### COVER-STORY / LIE LAYER

**B-27**
`arianne-martell  DECEIVES  balon-swann`
| Tier-2 | — |
Quote: *"Ser Arys was slain by Gerold Dayne." "Darkstar did it," his little princess said. "He tried to kill Princess Myrcella too. As she will tell Ser Balon."*
`adwd-the-watcher-01:165–169`
Rationale: Arianne proposes and executes the cover story that Darkstar killed Arys Oakheart — the official lie told to Ser Balon Swann. Doran goes along: *"It is all true."* The cover story re-frames Hotah's kill of Arys as Darkstar's deed. DECEIVES: Arianne → Balon Swann. Tier-2 because this is deliberate disinformation with a named target and named mechanism.

---

**B-28**
`doran-martell  DECEIVES  balon-swann`
| Tier-2 | — |
Quote: *"It is all true," said the prince, with a wince of pain. Is it his gout that hurts him, or the lie?*
`adwd-the-watcher-01:173`
Rationale: Doran endorses the cover story ("It is all true") to Balon Swann, making him complicit in the deception. Hotah's internal observation — "Is it his gout that hurts him, or the lie?" — confirms the textual awareness that this is a known untruth. DECEIVES: Doran → Balon Swann. Tier-2.

---

## Dropped / Considered-but-Rejected

1. **Cedra as informer (SUSPECTED_OF the-queenmaker-plot):** REJECTED. Cedra was caught by Doran AFTER the plot was already betrayed and Arianne was imprisoned. She cannot be the primary informer. She is a separate incident (Arianne's failed courier attempt from within the Spear Tower).

2. **Garin as informer (SUSPECTED_OF):** REJECTED. Arianne finds it unbelievable, and Doran's own words about Garin's gossip habits are offered to explain why Doran kept the betrothal secret from Arianne — not as an identification of the plot-informer. No textual basis.

3. **Darkstar as informer (SUSPECTED_OF):** REJECTED by the text itself. Arianne explicitly eliminates him on logical grounds (affc-the-princess-in-the-tower-01:51): *"if Ser Gerold had been the worm in the apple, why would he have turned his sword upon Myrcella?"* Re-proposing him would contradict the text's own reasoning.

4. **Arys BETRAYS arianne-martell:** Considered but REJECTED in favor of SUSPECTED_OF. BETRAYS would assert a fact the text does not prove. The text only shows Arianne entertaining the hypothesis.

5. **`arys LOVED/SERVES myrcella` dedup:** Already in baseline as LOVES, GUARDS, PROTECTS, VOWS_TO. Not re-proposed.

6. **`arianne RESENTS quentyn-martell`:** Text shows her rivalry with Quentyn is mediated through Doran, not direct resentment toward Quentyn. Her anger is aimed at Doran. No explicit RESENTS Quentyn line. Dropped.

7. **`murder-of-elia MOTIVATES doran-martell`:** Flagged per instructions as a Gap 7/Lens D seam — Doran says *"I have worked at the downfall of Tywin Lannister since the day they told me of Elia and her children"* (`affc-the-princess-in-the-tower-01:243`). The edge is absent from the graph (only `...MOTIVATES oberyn` exists). However this is called out as Lens D's seam; flagging rather than proposing it here.

8. **`arys WITNESS_IN myrcella-is-maimed-by-darkstar`:** Arys was dead (decapitated by Hotah) before/during the maiming per the timeline of the Queenmaker chapter. He is NOT a valid WITNESS_IN. The existing `arianne WITNESS_IN` is correctly assigned.

9. **`doran IGNORANT_OF the-queenmaker-plot`:** Would contradict the baseline (Doran knew via informer). Rejected.

10. **`garin-of-the-orphans MILK_BROTHER_OF arianne-martell`:** The edge type exists in the vocabulary. Textual basis: "His mother was my wet nurse" (`affc-the-queenmaker-01:137`) + "Garin had been with them as well that day; he was Arianne's milk brother, and they had been inseparable since before they learned to walk" (affc-the-queenmaker-01:23). This is strong and direct. Consider adding — it's outside my core whodunit lens but closely adjacent. **Proposing it as an add-on:**

**B-29 (add-on)**
`garin-of-the-orphans  MILK_BROTHER_OF  arianne-martell`
| Tier-1 | — |
Quote: *"he was Arianne's milk brother, and they had been inseparable since before they learned to walk"*
`affc-the-queenmaker-01:23`
Rationale: Direct statement. MILK_BROTHER_OF is in the locked vocabulary. Tier-1.

---

## Harvest

| kind | book | chapter:line | note |
|---|---|---|---|
| food | AFFC | affc-the-princess-in-the-tower-01:47 | Arianne's prison midday meal: kid roasted with lemon and honey + grape leaves stuffed with raisins, onions, mushrooms, dragon peppers — she refuses it then eats from hunger |
| food | AFFC | affc-the-captain-of-guards-01:153 | Doran's late supper at the Water Gardens: purple olives, flatbread, cheese, chickpea paste, cup of sweet heavy strongwine |
| food | AFFC | affc-the-captain-of-guards-01:165 | Doran's Water Gardens breakfast before departing: blood orange + gull's eggs diced with ham and fiery peppers |
| food | AFFC | affc-the-queenmaker-01:155 | Shandystone provisions: dates, cheese, olives, lemonsweet to drink |
| food | AFFC | affc-the-queenmaker-01:239 | Riding break on the sands: Myrcella splits an orange with Spotted Sylva; Garin eats olives and spits the stones at Drey |
| food | AFFC | affc-the-soiled-knight-01:21 | Shadow city: man grilling chunks of snake over a brazier with mustard seeds, dragon peppers, venom sauce — Ser Arys notes the smell |
| food | ADWD | adwd-the-watcher-01:51 | Balon Swann feast: 7 courses — egg/lemon soup, long green peppers stuffed with cheese and onions, lamprey pies, honey-glazed capons, whiskerfish from the Greenblood, savory snake stew (7 kinds of snake + dragon peppers + blood oranges + venom), sherbet, spun-sugar skulls with sweet custard + plum + cherry |
| food/hospitality | ADWD | adwd-the-watcher-01:43 | Feast toast in Dornish strongwine ("dark as blood and sweet as vengeance") — Hotah notes who does and does not drink (Fowler twins, Manwoody, Ullers, Wyls all abstain) |
| food | AFFC | affc-the-princess-in-the-tower-01:59 | Arianne in tower: "figs or olives or peppers stuffed with cheese" available on request; bath brought every second day |
| quote | AFFC | affc-the-queenmaker-01:299 | Load-bearing Hotah line: "Someone told." Hotah shrugged. "Someone always tells." — the arc's defining whodunit beat |
| quote | AFFC | affc-the-princess-in-the-tower-01:185 | Doran's non-answer on the informer: "I am the Prince of Dorne. Men seek my favor." |
| quote | ADWD | adwd-the-watcher-01:188–189 | Doran's "grass and viper" speech: "I was the grass. Pleasant, complaisant, sweet-smelling, swaying with every breeze. Who fears to walk upon the grass? But it is the grass that hides the viper from his enemies…" — load-bearing characterization for Doran's strategic persona |
| description | AFFC | affc-the-queenmaker-01:31 | Darkstar's physical description: aquiline nose, high cheekbones, strong jaw, clean-shaven, thick hair falling to collar "like a silver glacier, divided by a streak of midnight black"; eyes "seemed black … but she had looked at them from a closer vantage and she knew that they were purple. Dark purple. Dark and angry." |
| description | AFFC | affc-the-captain-of-guards-01:25 | Obara Sand physical: close-set eyes, rat-brown hair, big-boned woman near thirty, whip on hip, round shield of steel and copper on back |
| description | AFFC | affc-the-captain-of-guards-01:157 | Hotah's memories of Norvos: the three bells (Noom, Narrah, Nyel), taste of wintercake (ginger, pine nuts, cherry, with nahsa — fermented goat's milk in iron cup), mother in dress with squirrel collar, bears dancing down Sinner's Steps |
| description | AFFC | affc-the-captain-of-guards-01:6 | Water Gardens first image: blood oranges past ripe, some fallen on pale pink marble, sharp sweet smell; Doran in rolling chair with goose-down cushions, ebony and iron wheels |
| description | AFFC | affc-the-soiled-knight-01:56–57 | Arianne nude but for the copper-and-gold snake coiled around her right forearm — the seduction scene's visual anchor |
| description | AFFC | affc-the-princess-in-the-tower-01:37 | The Spear Tower cell: Myrish carpets, red wine, books, cyvasse table of ivory and onyx, featherbed, privy with marble seat and herbs, windows east (over sea) and south (over Tower of the Sun) |
| description | ADWD | adwd-the-watcher-01:19 | Hotah's copper scales "mirror-bright" at the feast; Maester Caleotte in new robes with dun/butternut/red stripes; Gregor's skull "bigger than any he'd seen, brow shelf thick and heavy, bone shone white as Ser Balon's cloak" |
| foreshadowing | AFFC | affc-the-soiled-knight-01:27 | Areo Hotah's premonition he will one day fight and kill Arys Oakheart: "On that day Oakheart would die, with the captain's longaxe crashing through his skull" — fulfilled at the Greenblood |
| foreshadowing | AFFC | affc-the-soiled-knight-01:41–42 | Doran warns Arys: "Every night I hear them whispering and sharpening their knives" — pointing to the conspirators Arys doesn't realize he's among |
| hospitality | ADWD | adwd-the-watcher-01:221–228 | Doran invokes guest-right to protect Ser Balon Swann: "Ser Balon is a guest beneath my roof. He has eaten of my bread and salt. I will not do him harm." — explicit guest-right claim |
