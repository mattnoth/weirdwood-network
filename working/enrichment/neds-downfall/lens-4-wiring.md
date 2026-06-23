# Lens 4 — Existing-node ↔ Existing-node Causal Wiring
## Ned's Downfall enrichment dip (S137)

Generated 2026-06-23. PROPOSE-ONLY — do not mint, do not ingest. Opus orchestrator synthesizes.

---

## PROPOSED EDGES

---

### EDGE L4-01
**`ned-discovers-the-truth-of-joffrey-s-parentage` --ENABLES--> `cersei-orders-ned-s-arrest`**

- Tier: 2
- Cite: `sources/chapters/agot/agot-eddard-12.md:169`
- Verbatim quote: `"When you play the game of thrones, you win or you die. There is no middle ground."`
- Justification: The discovery is the precondition that forced Cersei's hand. After Ned confronted her in the godswood (agot-eddard-12) and declared "When the king returns from his hunt, I intend to lay the truth before him" (line 159), Cersei chose to preempt him by ordering his arrest rather than flee. The ENABLES type is correct here rather than CAUSES because a human actor's decision intervened — Cersei chose arrest over exile. She had the option to flee; she chose to fight. This routes through her agency, not a forced material consequence. NOT agency-collapse: the discovery node is a pure revelation event, not a constitutive part of the arrest. The arrest follows the discovery by at least one chapter interval (eddard-12 → eddard-14), confirming temporal order. NOT an incidental co-location ENABLES: Cersei's explicit response in the godswood ("And what of my wrath, Lord Stark?" — line 165) shows she was immediately calculating her move in response to the discovery.
- Confidence: HIGH

---

### EDGE L4-02
**`ned-discovers-the-truth-of-joffrey-s-parentage` --MOTIVATES--> `cersei-lannister`**  
*(the decision to order the arrest rather than flee)*

- Tier: 2
- Cite: `sources/chapters/agot/agot-eddard-12.md:159`
- Verbatim quote: `"When the king returns from his hunt, I intend to lay the truth before him. You must be gone by then. You and your children, all three, and not to Casterly Rock."`
- Justification: This is the complementary agency-routing edge to L4-01. Ned's declaration that he will expose Joffrey's parentage MOTIVATES Cersei to choose preemptive arrest over flight. The node `cersei-lannister` is in baseline (she is a character node). MOTIVATES is appropriate because the edge routes specifically through Cersei's decision-making (the choice between "exile" and "fight"), which is the exact semantics MOTIVATES is designed for. This does NOT create agency-collapse with L4-01 because L4-01 is event→event (ENABLES) and this is event→character (MOTIVATES), expressing two complementary facets of the same causal chain at different semantic levels.
- Confidence: HIGH

---

### EDGE L4-03
**`varys-confirms-cersei-s-role-in-robert-s-death` --MOTIVATES--> `ned-confesses-to-treason`**

- Tier: 2
- Cite: `sources/chapters/agot/agot-eddard-15.md:131`
- Verbatim quote: `"Cersei is no fool. She knows a tame wolf is of more use than a dead one."`
- Additional cite: `sources/chapters/agot/agot-eddard-15.md:135`
- Verbatim quote (Varys's pitch): `"Tell the queen that you will confess your vile treason, command your son to lay down his sword, and proclaim Joffrey as the true heir."`
- Additional cite: `sources/chapters/agot/agot-eddard-15.md:147`
- Verbatim quote (the lever): `"And your daughter's life, my lord? How precious is that?"`
- Justification: The Varys cell-visit node currently has 0 outgoing edges. In the black-cells scene (agot-eddard-15), Varys confirms Cersei's role in Robert's death (via Lancel/strongwine), then uses that knowledge as a credibility foundation before pivoting to the pitch that Ned confess to save Sansa. The MOTIVATES type is correct: the confession is Ned's own choice, a human decision, not forced. Varys persuades; Ned decides. The cell visit causally upstream of the confession — there is no other narrative explanation offered for why Ned eventually confessed, and the chapter (agot-eddard-15) ends with Varys's explicit ultimatum about Sansa's life. The confession follows in agot-arya-05 at the Great Sept. Temporal order is confirmed: agot-eddard-15 (chapter 59) → agot-arya-05 (chapter 66). NOT agency-collapse: `varys-confirms-cersei-s-role-in-robert-s-death` is a discrete revelation event, not constitutive of the confession itself.
- Confidence: HIGH

---

### EDGE L4-04
**`gold-cloaks-betray-ned` --ENABLES--> `cersei-orders-the-sleeping-guards-executed`**

- Tier: 2
- Cite: `sources/chapters/agot/agot-eddard-14.md:121`
- Verbatim quote: `"With a single sharp thrust, the nearest gold cloak drove his spear into Tomard's back. Fat Tom's blade dropped from nerveless fingers as the wet red point burst out through his ribs, piercing leather and mail. He was dead before his sword hit the floor."`
- Justification: The gold-cloak betrayal is the moment of physical dominance; the executing of Ned's sleeping household guards follows as a direct consequence of that moment of total control. Once the gold cloaks turned and Ned's men (Tomard, Varly, Cayn) were killed or arrested, Cersei could order the elimination of the remaining Stark household who were off-guard. ENABLES is the correct type: the betrayal (gold-cloaks turn) creates the precondition (no Stark resistance left) that allows the sleeping-guards execution to proceed. It does not CAUSE it directly — Cersei still had to issue the order. NOT temporal inversion: the throne-room betrayal is the opening blow; the sleeping-guard executions are the aftermath (Sansa IV describes bodies being found on the tower stair, agot-sansa-04:19). NOT agency-collapse: `gold-cloaks-betray-ned` is a distinct event (the throne-room betrayal) while `cersei-orders-the-sleeping-guards-executed` is a separate event (the Tower of the Hand aftermath massacre).
- Confidence: HIGH

---

### EDGE L4-05
**`arrest-of-eddard-stark` --ENABLES--> `sansa-stark-held-hostage-in-kings-landing`**

- Tier: 2
- Cite: `sources/chapters/agot/agot-sansa-04.md:43`
- Verbatim quote: `"To keep you safe, my sweet one," Queen Cersei had told her. "Joffrey would never forgive me if anything happened to his precious."`
- Additional cite: `sources/chapters/agot/agot-sansa-06.md:39`
- Verbatim quote: `"Mother says I'm still to marry you, so you'll stay here, and you'll obey."`
- Justification: **Cross-arc seam edge.** Sansa's detention is a direct downstream consequence of the arrest. Before the arrest, Ned had arranged for Sansa (and Arya) to sail on the Wind Witch out of Braavos. The arrest aborted that escape and left Sansa in Lannister custody at Maegor's Holdfast, where she was used as a hostage/leverage device against both Ned's confession and Robb's campaign. This is a cross-arc seam: the arrest (Ned's Downfall cluster) flows directly into the WO5K cluster (Joffrey's reign, Sansa-as-hostage, Lannister leverage over the north). ENABLES is correct: the arrest is the precondition that made Sansa's captivity possible (she was about to leave the city). NOT CAUSES because Cersei still made the active choice to keep Sansa rather than release her. CHECK: does `sansa-stark-held-hostage-in-kings-landing` exist in baseline? — Baseline does not explicitly list it. **FLAG: if this node does not exist, this is the highest-priority MINT candidate.** It is strongly implied by the existing node inventory (Sansa's plight is the operational substrate of the WO5K Lannister leverage) but not enumerated in baseline.md. Propose as a candidate mint if it is not already a node; the ENABLES edge follows if/when the node is confirmed.
- Confidence: HIGH (edge logic), PENDING (node existence check)
- Node status: NEW NODE NEEDED — `sansa-stark-held-hostage-in-kings-landing` — must verify or propose mint before ingesting this edge.

---

### EDGE L4-06
**`ned-confesses-to-treason` --ENABLES--> `sansa-stark`** *(specifically: her survival past the Sept)*

- Tier: 2
- Cite: `sources/chapters/agot/agot-eddard-15.md:131`
- Verbatim quote: `"Cersei is no fool. She knows a tame wolf is of more use than a dead one."`
- Additional cite: `sources/chapters/agot/agot-arya-05.md:161`
- Verbatim quote (Joffrey at the Sept): `"My mother bids me let Lord Eddard take the black, and Lady Sansa has begged mercy for her father."`
- Justification: The confession was explicitly premised on Sansa's safety — Varys made the offer in those exact terms (agot-eddard-15:147: "your daughter's life"). The confession node already has COMMANDS_IN cersei-lannister. This proposed edge routes the confession OUTWARD to `sansa-stark` as an ENABLES: the confession is what preserved Sansa's immediate utility as hostage/bride and prevented Cersei from treating her as a threat. WITHOUT the confession, Sansa would have had no leverage (her mother's plea + Ned's public submission together were the mechanism for the "mercy" Joffrey then ignored). The ENABLES type is correct — it's a precondition for Sansa's survival path, not a guaranteed cause of it (Joffrey overrode the plan anyway by ordering the execution). Character node `sansa-stark` is in baseline.
- Confidence: MEDIUM (the causal path is real but the overriding of the plan by Joffrey means "enabled" is softer than usual — Sansa's survival ultimately came from other factors after the execution)

---

### EDGE L4-07
**`ned-orders-janos-slynt-to-arrest-cersei` --PREVENTS--> `cersei-orders-ned-s-arrest`**  
*(attempted; failed)*

- Tier: 2
- Cite: `sources/chapters/agot/agot-eddard-14.md:115`
- Verbatim quote: `"You leave me no choice," Ned told Cersei Lannister. He called out to Janos Slynt. "Commander, take the queen and her children into custody. Do them no harm, but escort them back to the royal apartments and keep them there, under guard."`
- Justification: Ned's order-to-Slynt is the countermove intended to PREVENT Cersei's arrest order from being executed. This is a causal PREVENTS relationship in the same temporal moment: if Slynt had obeyed, Cersei's arrest order would have been neutralized. The PREVENTS type is appropriate for a failed blocking action. NOT agency-collapse: `ned-orders-janos-slynt-to-arrest-cersei` is already listed as a distinct event node (a SUB_BEAT_OF arrest-of-eddard-stark), and `cersei-orders-ned-s-arrest` is a separate node. The attempted PREVENTS relationship between them is structurally non-constitutive — one is an attempt to block the other, not a part of it. Temporal order: both occur in the throne-room sequence in agot-eddard-14, with Ned's order coming as the counter to Cersei's, so the PREVENTS relationship is contemporaneous/counterfactual, which is precisely the use case for PREVENTS. Confidence notes: this edge correctly models the failed countermove logic — it's a real causal relationship even though the outcome was the opposite of what was intended.
- Confidence: HIGH

---

### EDGE L4-08
**`execution-of-eddard-stark` --ENABLES--> `robb-stark-war-of-the-five-kings-campaign`**

- Tier: 2
- Cite: `sources/chapters/agot/agot-sansa-06.md:153`
- Verbatim quote: `"Your brother defeated my uncle Jaime. My mother says it was treachery and deceit. She wept when she heard."`
- Justification: **Cross-arc seam edge.** The execution is already wired CAUSES robb-proclaimed-king-in-the-north. This proposes a further downstream link to the active military campaign node for Robb's WO5K arc, if that node exists separately from the proclamation. The execution is the terminal trigger: before the execution, Robb was marching south to negotiate/rescue Ned; after the execution, the campaign's goal became vengeance/independence. `robb-proclaimed-king-in-the-north` is already wired (see baseline). Check whether `robb-stark-war-of-the-five-kings-campaign` (or equivalent — `robb-stark-s-campaign`, `war-of-the-five-kings`) is a distinct minted node. If so, ENABLES is correct (the execution is the precondition that locked in Robb's military path). If the WO5K arc node is `war-of-the-five-kings` directly, prefer TRIGGERS (proximate spark).
- Confidence: HIGH (edge logic) / PENDING (target slug must be verified — node name uncertain)
- Node status: Must verify exact slug. If `war-of-the-five-kings` exists as a node, use: `execution-of-eddard-stark --TRIGGERS--> war-of-the-five-kings`

---

### RENLY'S OFFER — ANALYSIS (no edge proposed)

**Renly's throne-room offer** (agot-eddard-13:163-179) — Renly offered Ned 100 swords to seize Joffrey and Cersei the night Robert lay dying; Ned refused. Baseline flags this as a candidate mint with no event node found.

Causal analysis:
- If the node exists: Ned's refusal of Renly's offer ENABLES the scenario where Ned had insufficient force at the throne-room betrayal. An ENABLES or PREVENTS edge is structurally valid (the refusal prevented a force-seizure that might have worked).
- However: the Renly-offer node is flagged as NOT YET MINTED. No edge can be proposed to a non-existent node.

**Recommendation: MINT candidate.** Proposed slug: `renly-offers-ned-swords-to-seize-joffrey`. After minting, propose:
- `renly-offers-ned-swords-to-seize-joffrey --[declined]-- eddard-stark` (role: AGENT_IN with refusal outcome)
- `eddard-stark --PREVENTS--> renly-offers-ned-swords-to-seize-joffrey` (Ned's refusal, modeled as his agency blocking the plan)
- The refusal then chains to: the refusal ENABLES `gold-cloaks-betray-ned` (Ned went to the throne room with only his household guard, no Renly swords, giving the betrayal room to work)

This is a high-value causal chain but gated on the mint decision. Flag to Opus orchestrator.

---

### LITTLEFINGER-BETRAYS-NED FORWARD LINK — ANALYSIS (no additional edge proposed)

Baseline notes that `littlefinger-betrays-ned` has only 2 edges and NO forward CAUSES, but is already `SUB_BEAT_OF arrest-of-eddard-stark` (constitutive). 

Review: The betrayal IS constitutive of the arrest — it is the physical mechanism of the arrest (Littlefinger's dagger at Ned's throat is the arrest in action). Adding a forward CAUSES edge from `littlefinger-betrays-ned` to `arrest-of-eddard-stark` would be agency-collapse (S120 policy): a constitutive sub-beat cannot CAUSE the event it constitutes. 

However, there IS a non-redundant forward link available: **`littlefinger-betrays-ned` --MOTIVATES--> `petyr-baelish`** (the betrayal reveals/expresses Littlefinger's character calculus and motivates his later power moves in WO5K, e.g. his role in escalating tensions, his manipulation of Lysa). This is very weak for THIS dip — it's more of a character-arc edge than a event-causal edge. Not proposing it here.

No non-constitutive, non-redundant forward edge from `littlefinger-betrays-ned` identified for this dip. Consistent with the lens prompt's note to "leave it" if no clean non-redundant link exists.

---

## HARVEST ROWS

`agot-eddard-12.md:37` / food / Littlefinger mentions lunch with Lady Tanda, "roast me a fatted calf. If it's near as fatted as her daughter"— social/hospitality context, physical description of Lady Tanda's daughter implied

`agot-eddard-12.md:15` / food / "a stoppered flask" of milk of the poppy — Pycelle delivers it; recurring hospitality-as-manipulation motif (see also agot-eddard-13:57)

`agot-eddard-12.md:107` / description / Cersei in the godswood: "Her curling blond hair moved in the wind, and her eyes were green as the leaves of summer" — first-class physical description of Cersei; notable because she comes "dressed simply, in leather boots and hunting greens" (line 101)

`agot-eddard-12.md:141` / quote / Cersei's wedding-night confession: "The night of our wedding feast, the first time we shared a bed, he called me by your sister's name. He was on top of me, in me, stinking of wine, and he whispered Lyanna." — load-bearing quote for Robert/Lyanna backstory and Cersei's hatred of Robert; attach to `cersei-lannister` node ## Quotes or `robert-baratheon` node

`agot-eddard-12.md:169` / quote / "When you play the game of thrones, you win or you die. There is no middle ground." — the canonical Cersei line; attach verbatim to `cersei-lannister` ## Quotes

`agot-eddard-13.md:65` / quote / Robert's dying words re: Daenerys: "The girl. Daenerys. Only a child, you were right … that's why, the girl … the gods sent the boar … sent to punish me …" — foreshadowing/guilt; attach to `death-of-robert-baratheon` or `robert-baratheon` node

`agot-eddard-13.md:85` / food / Robert's final request: "Serve the boar at my funeral feast. Apple in its mouth, skin seared crisp. Eat the bastard. Don't care if you choke on him." — hospitality/food; the dying king's last meal order; darkly comic; attach to `death-of-robert-baratheon`

`agot-eddard-13.md:271` / quote / Littlefinger on the City Watch: "They follow the man who pays them." — canonical Littlefinger line about the gold cloaks; the dagger-spinning moment (line 267: "There's your answer"); attach to `petyr-baelish` ## Quotes

`agot-eddard-13.md:271` / quote / Littlefinger on Ned's honor: "You wear your honor like a suit of armor, Stark. You think it keeps you safe, but all it does is weigh you down and make it hard for you to move." — load-bearing Littlefinger character/theme quote; attach to `petyr-baelish` ## Quotes

`agot-eddard-15.md:103` / quote / Varys on Robert: "If there was one soul in King's Landing who was truly desperate to keep Robert Baratheon alive, it was me … I could not protect him from his friends." — key Varys motivation statement; attach to `varys` ## Quotes

`agot-eddard-15.md:111` / quote / Varys on the wine/boar: "It was not wine that killed the king. It was your mercy." — load-bearing quote on `varys-confirms-cersei-s-role-in-robert-s-death`; attach as evidence_quote on that node

`agot-eddard-15.md:115` / quote / Varys on Cersei's reasoning: "Robert was becoming unruly, and she needed to be rid of him to free her hands to deal with his brothers." — key motivation quote for Cersei's role in Robert's death; attach to `cersei-lannister` or `death-of-robert-baratheon`

`agot-sansa-04.md:23` / food / Sansa and Jeyne's meals during captivity: "hard cheese and fresh-baked bread and milk to break their fast, roast chicken and greens at midday, and a late supper of beef and barley stew" — food detail during Lannister captivity; hospitality-as-control motif

`agot-sansa-04.md:109` / quote / Cersei to Sansa (revealing Sansa betrayed Ned's plan to flee): "Why else should you have come to me and told me of your father's plan to send you away from us, if not for love?" — load-bearing quote establishing that Sansa's prior information to Cersei precipitated events; attach to `sansa-stark` ## Quotes; potential mint candidate for a `sansa-warns-cersei-of-ned-s-departure-plan` event node

`agot-arya-05.md:11-14` / description / Arya catching a pigeon: "a plump one, speckled brown, busily pecking at a crust that had fallen between two cobblestones" — food/survival detail; Arya's life in Flea Bottom

`agot-arya-05.md:43` / food / Flea Bottom pot-shop description: "huge tubs of stew had been simmering for years, and you could trade half your bird for a heel of yesterday's bread and a 'bowl o' brown,' and they'd even stick the other half in the fire and crisp it up for you" — vivid food/poverty description; Flea Bottom social texture

`agot-sansa-06.md:15` / quote / Sansa's witness of execution: "she saw the gold cloaks fling him down, saw Ser Ilyn striding forward, unsheathing Ice from the scabbard on his back" — verbatim witness quote; attach to `execution-of-eddard-stark` as evidence_quote (Sansa-POV); also confirms Ice's role

`agot-sansa-06.md:153` / quote / Joffrey to Sansa re: Robb: "After my name day feast, I'm going to raise a host and kill your brother myself. That's what I'll give you, Lady Sansa. Your brother's head." — foreshadowing of the WO5K from Joffrey's POV; attach to `joffrey-baratheon` ## Quotes; potential foreshadowing harvest

`agot-sansa-06.md:165` / description/foreshadowing / Sansa on the battlements: "All it would take was a shove, she told herself. He was standing right there, right there, smirking at her with those fat wormlips." — Sansa's first homicidal thought toward Joffrey; character-arc foreshadowing

---

## NEEDS_VOCAB FLAGS

None. All proposed edges use vocabulary from the locked set (ENABLES, MOTIVATES, PREVENTS, SUB_BEAT_OF).

---

## MINT CANDIDATES (flagged for Opus orchestrator)

1. **`sansa-stark-held-hostage-in-kings-landing`** — high-confidence candidate; directly evidenced by agot-sansa-04 and agot-sansa-06; the node captures Cersei's use of Sansa as leverage against both Ned's confession and Robb's campaign; currently a gap in the existing node inventory per baseline review.

2. **`renly-offers-ned-swords-to-seize-joffrey`** — candidate per baseline.md §"Nodes that may NOT have a home yet"; agot-eddard-13:163-179; Ned's refusal is a significant counterfactual hinge in the betrayal cluster.

3. **`sansa-warns-cersei-of-ned-s-departure-plan`** — emergent from harvest; agot-sansa-04:109 ("Why else should you have come to me and told me of your father's plan to send you away from us, if not for love?"); this act by Sansa is a hidden upstream cause of the timing of Ned's arrest (Cersei knew Ned was trying to get the girls out of the city, which informed her decision to move). Not in baseline. May or may not warrant its own event node — raise to orchestrator.
