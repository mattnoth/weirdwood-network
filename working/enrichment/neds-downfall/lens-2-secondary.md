# Lens 2 — Secondary-character substrate + hidden-architect agency + witnesses
# Ned's Downfall enrichment dip (S137)
# PROPOSE-ONLY — do NOT mint. Opus orchestrator synthesizes + line-checks + mints survivors.

---

## DEDUP CONFIRMATION
Baseline lists the following as already existing — not re-proposed here:
- `sansa-stark WITNESS_IN execution-of-eddard-stark` — EXISTS, skip
- `petyr-baelish COMMANDS_IN gold-cloaks-betray-ned` — EXISTS, skip
- `cersei-lannister COMMANDS_IN ned-confesses-to-treason` — EXISTS, skip
- `cersei-lannister COMMANDS_IN cersei-orders-ned-s-arrest` — EXISTS, skip
- `littlefinger-betrays-ned` node EXISTS (petyr-baelish AGENT_IN only, NO forward causal edges — this is a high-value gap)

---

## PROPOSED EDGES

---

### CLUSTER A — Littlefinger as hidden architect

**A1.**
`petyr-baelish --DECEIVES--> eddard-stark`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-13.md:271`
Quote: `"I ought to make you say it, but that would be cruel … so have no fear, my good lord. For the sake of the love I bear for Catelyn, I will go to Janos Slynt this very hour and make certain that the City Watch is yours."`
Justification: Littlefinger presents himself as acting for Ned's benefit and Cat's sake; he is simultaneously (as shown in agot-eddard-14:125) arranging for the Watch to betray Ned in the throne room. The speech is performative cover. DECEIVES is exact: actor→actor, the deception is on-page.
Confidence: HIGH

---

**A2.**
`petyr-baelish --SUSPECTED_OF--> gold-cloaks-betray-ned`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-13.md:271`
Quote: `"I will go to Janos Slynt this very hour and make certain that the City Watch is yours. Six thousand gold pieces should do it. A third for the Commander, a third for the officers, a third for the men."`
Justification: Littlefinger explicitly describes buying the City Watch — but the purchase is framed as being for Ned, while its real use is to deliver the Watch to Cersei. SUSPECTED_OF captures the unproven orchestration of the betrayal (the text shows he bought the Watch; it does not flatly say he arranged the betrayal — that is strongly implied, not stated). Petyr-baelish already has COMMANDS_IN on `gold-cloaks-betray-ned` per baseline, so this SUSPECTED_OF is additive — it models the conspiratorial suspicion layer specifically. CHECK: baseline says `petyr-baelish COMMANDS_IN gold-cloaks-betray-ned` already EXISTS. If COMMANDS_IN already asserts it, SUSPECTED_OF on the same pair may be redundant — FLAG FOR ORCHESTRATOR. Recommend: keep SUSPECTED_OF only if the orchestrator determines COMMANDS_IN and SUSPECTED_OF serve different epistemic layers in the schema; otherwise skip A2.
Confidence: LOW (COMMANDS_IN may cover this)

---

**A3.**
`petyr-baelish --CAUSES--> littlefinger-betrays-ned`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-13.md:271`
Quote: `"I will go to Janos Slynt this very hour and make certain that the City Watch is yours."`
Justification: Littlefinger's action of purchasing Slynt directly CAUSES the situation in which Littlefinger then betrays Ned in the throne room. The bribery is the predicate act. `littlefinger-betrays-ned` has NO forward causal edges (per baseline "ONLY 2 edges total"); this CAUSES fills the wiring gap from the planning scene (Eddard-13) to the execution scene (Eddard-14).
Confidence: HIGH

**NOTE on A3:** The baseline says the only two edges on `littlefinger-betrays-ned` are existing (petyr-baelish AGENT_IN and the scene quote). This edge wires the bribery event as a CAUSES into that node. The orchestrator should also consider whether `ned-orders-janos-slynt-to-arrest-cersei ENABLES littlefinger-betrays-ned` (Ned's order gives Littlefinger the opening — see A5 below).

---

**A4.**
`littlefinger-betrays-ned --CAUSES--> arrest-of-eddard-stark`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-14.md:125`
Quote: `"Littlefinger slid Ned's dagger from its sheath and shoved it up under his chin. His smile was apologetic. 'I did warn you not to trust me, you know.'"`
Justification: The physical knife-to-throat is the immediate cause of Ned's arrest — Littlefinger's personal action is what triggers the capture. This is the missing forward wire from `littlefinger-betrays-ned` (causal island) to `arrest-of-eddard-stark`. Note: `arrest-of-eddard-stark` already has `cersei-orders-ned-s-arrest` and `gold-cloaks-betray-ned` as SUB_BEAT_OF children. The Littlefinger knife-moment is the decisive instant that seals the arrest; it is a CAUSES, not a SUB_BEAT_OF, because it is Littlefinger's individual agency completing the act, not a constitutive sub-component.
Confidence: HIGH

---

**A5.**
`ned-orders-janos-slynt-to-arrest-cersei --ENABLES--> gold-cloaks-betray-ned`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-14.md:115-117`
Quote: `"You leave me no choice," Ned told Cersei Lannister. He called out to Janos Slynt. "Commander, take the queen and her children into custody. Do them no harm, but escort them back to the royal apartments and keep them there, under guard." "Men of the Watch!" Janos Slynt shouted, donning his helm. A hundred gold cloaks leveled their spears and closed.`
Justification: Ned's order to Slynt is the trigger that activates the gold cloaks — Slynt uses Ned's own command as the moment to spring the betrayal. Ned's order ENABLES the treason by providing the occasion. Both nodes exist per baseline.
Confidence: HIGH

---

### CLUSTER B — Varys as hidden actor

**B1.**
`varys --SUSPECTED_OF--> death-of-robert-baratheon`
Tier: 2
Cite: `sources/chapters/agot/agot-eddard-15.md:111`
Quote: `"Oh, indeed. Cersei gave him the wineskins, and told him it was Robert's favorite vintage."`
Justification: Varys reveals that Cersei gave Lancel the strongwine wineskins; Varys already knew this and withheld it. Varys's own framing — "I protected him from his enemies, but I could not protect him from his friends" (agot-eddard-15:103) — is a careful non-denial. SUSPECTED_OF captures the scholarly suspicion that Varys knew and enabled the poisoning without flatly asserting it. The text does NOT say Varys was involved in the wine; it only shows he knew and stayed silent.
Confidence: LOW (suspicion only, nothing in text asserts Varys arranged the wine; text only shows knowledge)

---

**B2.**
`varys --WITNESS_IN--> arrest-of-eddard-stark`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-15.md:85-86`
Quote: `"When they slaughtered my guard, you stood beside the queen and watched, and said not a word." "And would again. I seem to recall that I was unarmed, unarmored, and surrounded by Lannister swords."`
Justification: Varys explicitly confirms he was present and watched the arrest/guard-massacre in the throne room. He is a witness to the central event. No WITNESS_IN edge on Varys is listed in baseline.
Confidence: HIGH

---

**B3.**
`varys --DECEIVES--> eddard-stark`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-15.md:139`
Quote: `"I would sooner wed the Black Goat of Qohor. Littlefinger is the second most devious man in the Seven Kingdoms. Oh, I feed him choice whispers, sufficient so that he thinks I am his … just as I allow Cersei to believe I am hers."`
Justification: Varys confesses to Ned that he has deceived Cersei, Littlefinger, and by implication Ned himself ("and just as you let me believe that you were mine" — Ned's rejoinder). Varys's prison-visit monologue is itself a layered performance: he presents as Ned's ally while pursuing his own agenda. The deception of Ned is the most direct: Varys pushes Ned toward the false confession using the threat against Sansa.
Confidence: HIGH

---

**B4.**
`varys --MOTIVATES--> ned-confesses-to-treason`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-15.md:147,155`
Quote: `"And your daughter's life, my lord? How precious is that?" … "The next visitor who calls on you could bring you bread and cheese and the milk of the poppy for your pain … or he could bring you Sansa's head. The choice, my dear lord Hand, is entirely yours."`
Justification: Varys's black-cell visit is the direct intervention that shifts Ned toward the confession — he is the agent who delivers the Sansa threat that breaks Ned's resistance. `ned-confesses-to-treason` already has `cersei-lannister COMMANDS_IN` per baseline; Varys MOTIVATES is the complementary edge that captures who actually convinced Ned to comply.
Confidence: HIGH

---

### CLUSTER C — Cersei as prime mover

**C1.**
`ned-discovers-the-truth-of-joffrey-s-parentage --TRIGGERS--> cersei-orders-ned-s-arrest`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-12.md:159`
Quote: `"When the king returns from his hunt, I intend to lay the truth before him. You must be gone by then. You and your children, all three …"`
Justification: Ned's godswood confrontation with Cersei — in which he gives her the warning and refuses to stay silent — is the direct trigger for Cersei's decision to act before Robert returns. This is the missing causal link from the causal-island node (per baseline: `ned-discovers-the-truth-of-joffrey-s-parentage` has NO causal link forward to the arrest). Ned's explicit statement that he will reveal the truth to Robert is the precipitant.
Confidence: HIGH

---

**C2.**
`cersei-lannister --SUSPECTED_OF--> death-of-robert-baratheon`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-15.md:111`
Quote: `"Oh, indeed. Cersei gave him the wineskins, and told him it was Robert's favorite vintage."`
Justification: Varys explicitly tells Ned that Cersei provided Lancel the strongwine wineskins. The text establishes her agency in the wine supply; whether it rises to culpable homicide vs. negligent overindulgence is textually ambiguous. SUSPECTED_OF reflects that the text shows her providing the wine without flatly proving intent to kill.
Confidence: HIGH (Varys's statement is a direct attribution; the SUSPECTED_OF qualifier is for epistemic humility about intent, not about who gave the wine)

---

**C3.**
`varys-confirms-cersei-s-role-in-robert-s-death --CAUSES--> varys --MOTIVATES--> ned-confesses-to-treason`
NOTE: This is a chain, not a single edge. FLAG FOR ORCHESTRATOR — not a valid single-edge proposal. Reformulated as:

**C3 (reformulated):**
`varys-confirms-cersei-s-role-in-robert-s-death --ENABLES--> ned-confesses-to-treason`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-15.md:103,111`
Quote: `"If there was one soul in King's Landing who was truly desperate to keep Robert Baratheon alive, it was me. … Cersei gave him the wineskins, and told him it was Robert's favorite vintage."`
Justification: Varys's revelation that Robert's death was engineered — and that Ned's earlier "mercy" in warning Cersei was what sealed Robert's fate — is what breaks Ned's remaining resistance. The confirmation ENABLES the confession by stripping Ned's illusions about fighting the Lannisters. `varys-confirms-cersei-s-role-in-robert-s-death` is a causal island (0 outgoing edges per baseline); this wires it forward.
Confidence: HIGH

---

### CLUSTER D — Witnesses and role-edges on the household guard massacre

**D1.**
`tomard --VICTIM_IN--> gold-cloaks-betray-ned`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-14.md:121`
Quote: `"With a single sharp thrust, the nearest gold cloak drove his spear into Tomard's back. Fat Tom's blade dropped from nerveless fingers as the wet red point burst out through his ribs, piercing leather and mail. He was dead before his sword hit the floor."`
Justification: Tomard (Fat Tom) is explicitly killed in the throne-room betrayal. He is already listed as VICTIM_IN in baseline ("tomard / varly VICTIM_IN") but let me flag: baseline lists Tomard and Varly as VICTIM_IN on `gold-cloaks-betray-ned` — this is already noted there. Confirm before minting. If already EXISTS, skip D1.
Confidence: HIGH (existence check needed — baseline text says "eddard / tomard / varly VICTIM_IN" — so this EXISTS, skip)

**D1 REVISED — Cayn:**
`cayn --VICTIM_IN--> gold-cloaks-betray-ned`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-14.md:123`
Quote: `"Cayn whirled, steel flashing, drove back the nearest spearman with a flurry of blows; for an instant it looked as though he might cut his way free. Then the Hound was on him. Sandor Clegane's first cut took off Cayn's sword hand at the wrist; his second drove him to his knees and opened him from shoulder to breastbone."`
Justification: Cayn is killed in the throne-room betrayal. Baseline lists "tomard / varly VICTIM_IN" on `gold-cloaks-betray-ned` but does NOT list Cayn. Cayn is explicitly named in the chapter as the third guardsman killed. NEW ROLE EDGE needed on the existing node.
Confidence: HIGH

---

**D2.**
`sandor-clegane --AGENT_IN--> gold-cloaks-betray-ned`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-14.md:123`
Quote: `"Then the Hound was on him. Sandor Clegane's first cut took off Cayn's sword hand at the wrist; his second drove him to his knees and opened him from shoulder to breastbone."`
Justification: Sandor Clegane personally kills Cayn during the throne-room betrayal. Baseline says "gold-cloaks / janos-slynt / sandor-clegane AGENT_IN" already EXISTS on `gold-cloaks-betray-ned`. DEDUP: if this EXISTS, skip D2.
Confidence: HIGH (existence check needed — baseline appears to list sandor-clegane AGENT_IN already)

**D2 REVISED — Sandor KILLS:**
`sandor-clegane --KILLS--> cayn`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-14.md:123`
Quote: `"Then the Hound was on him. Sandor Clegane's first cut took off Cayn's sword hand at the wrist; his second drove him to his knees and opened him from shoulder to breastbone."`
Justification: Direct on-page kill. KILLS is in vocab. Sandor is not listed as killing Cayn anywhere in baseline.
Confidence: HIGH
NEW NODE CHECK: `cayn` — mentioned as a household guard of Ned Stark; likely no standalone node. NEW NODE NEEDED: `cayn` (person.guard, Ned Stark's household guard, killed in the throne-room betrayal). Verify slug in graph before minting.

---

**D3.**
`janos-slynt --KILLS--> varly`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-14.md:123`
Quote: `"Janos Slynt himself slashed open Varly's throat."`
Justification: Direct on-page kill by Janos Slynt. KILLS is in vocab. Not in baseline.
Confidence: HIGH
NEW NODE CHECK: `varly` — household guard. Likely no standalone node. NEW NODE NEEDED: `varly` (person.guard, Ned Stark's household guard, killed by Janos Slynt).

---

**D4.**
`gold-cloaks --KILLS--> tomard`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-14.md:121`
Quote: `"With a single sharp thrust, the nearest gold cloak drove his spear into Tomard's back. Fat Tom's blade dropped from nerveless fingers as the wet red point burst out through his ribs, piercing leather and mail. He was dead before his sword hit the floor."`
Justification: A gold cloak (unnamed, acting as unit) kills Tomard. Not in baseline.
Confidence: HIGH
NEW NODE CHECK: `tomard` — the portly guardsman "Fat Tom," explicitly named multiple times in agot-eddard-12 and 14. May have a stub node; verify.

---

**D5.**
`barristan-selmy --WITNESS_IN--> arrest-of-eddard-stark`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-14.md:109`
Quote: `"The Lord Commander of the Kingsguard hesitated. In the blink of an eye he was surrounded by Stark guardsmen, bare steel in their mailed fists."`
Justification: Barristan is present in the throne room at the moment of arrest. He is mentioned as AGENT_IN on `cersei-orders-ned-s-arrest` per baseline; but WITNESS_IN on the broader arrest event is different — he witnesses the whole scene, including the guard massacre. CHECK: baseline has `barristan-selmy AGENT_IN cersei-orders-ned-s-arrest`. WITNESS_IN on `arrest-of-eddard-stark` is a different edge to a different node; propose it.
Confidence: HIGH

---

**D6.**
`janos-slynt --AGENT_IN--> arrest-of-eddard-stark`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-14.md:117`
Quote: `"Men of the Watch!" Janos Slynt shouted, donning his helm. A hundred gold cloaks leveled their spears and closed."`
Justification: Janos Slynt personally commands the Watch at the moment of arrest. He is already AGENT_IN on `gold-cloaks-betray-ned` per baseline, but that is a sub-beat; his role-edge on the parent node (`arrest-of-eddard-stark`) may be missing. Propose for the parent event.
Confidence: HIGH

---

### CLUSTER E — Renly: offer, refusal, flight

**E1.**
`renly-baratheon --AGENT_IN--> renly-s-throne-room-offer` [NEW NODE]
`eddard-stark --AGENT_IN--> renly-s-throne-room-offer` [NEW NODE]
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-13.md:163`
Quote: `"My lord, I have thirty men in my personal guard, and other friends beside, knights and lords. Give me an hour, and I can put a hundred swords in your hand."`
Justification: Renly's offer is a distinct action node that shapes the arrest arc (Ned refuses; Renly flees; Ned is left without support). Baseline flags this as a candidate mint: "Renly's throne-room offer — no event node found." Proposing as NEW NODE: `renly-offers-ned-one-hundred-swords` (event.incident). DEDUP: check for any existing node before minting.
Confidence: HIGH (for the event existence); node itself is a PROPOSED MINT

---

**E2.**
`eddard-stark --PREVENTS--> renly-s-throne-room-offer` [on the new node, modeling the refusal]
NOTE: PREVENTS doesn't fit exactly (Ned's refusal doesn't prevent the offer; it declines it). Reformulated:

**E2 (reformulated):**
`renly-s-throne-room-offer --ENABLES--> arrest-of-eddard-stark`
Tier: 1 (as counterfactual-enabling-by-absence)
Cite: `sources/chapters/agot/agot-eddard-13.md:181`
Quote: `"He found himself wondering if he had done the right thing by refusing Lord Renly's offer. … if Cersei elected to fight rather than flee, he might well have need of Renly's hundred swords, and more besides."`
Justification: Ned's internal reflection identifies the refusal of Renly's offer as a contributing factor to his vulnerability. The offer ENABLES (as a counterfactual — its rejection removes a potential protective layer). This is a border-case: ENABLES usually models "A makes B possible." Here, the absence of the action enables the arrest. LOW confidence as causal wiring; HIGH as context. RECOMMEND: orchestrator assess whether ENABLES is the right verb for a failed/refused intervention.
Confidence: LOW (non-standard use of ENABLES)

---

**E3.**
`renly-baratheon --AGENT_IN--> renly-flees-kings-landing` [NEW NODE candidate]
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-14.md:59`
Quote: `"He took his leave through a postern gate an hour before dawn, accompanied by Ser Loras Tyrell and some fifty retainers. When last seen, they were galloping south in some haste, no doubt bound for Storm's End or Highgarden."`
Justification: Renly's flight is an event that materially shapes Ned's position (Ned had "counted on Renly's support"). It is a discrete plot action with named participants. NEW NODE candidate: `renly-flees-kings-landing` (event.flight, agot-eddard-14). Also: `ser-loras-tyrell --AGENT_IN--> renly-flees-kings-landing`.
Confidence: HIGH (for event existence); node itself is a PROPOSED MINT

---

**E4.**
`renly-flees-kings-landing --ENABLES--> arrest-of-eddard-stark`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-14.md:57-58`
Quote: `"Varys gave him a sorrowful look. 'I fear Lord Renly has left the city.' 'Left the city?' Ned had counted on Renly's support."`
Justification: Renly's absence removes Ned's backup force; it ENABLES the arrest by leaving Ned without adequate political and military support in the small council. This is a conditional-enabling edge (same caveat as E2 — absence enabling). RECOMMEND: orchestrator assess.
Confidence: LOW (enabling-by-absence, non-standard)

---

### CLUSTER F — Witness and role-edges at the execution

**F1.**
`arya-stark --WITNESS_IN--> execution-of-eddard-stark`
Tier: 1
Cite: `sources/chapters/agot/agot-arya-05.md:135-171`
Quote: `"That was when she saw her father. Lord Eddard stood on the High Septon's pulpit outside the doors of the sept, supported between two of the gold cloaks."`
Justification: Arya is in the crowd at the Great Sept of Baelor and watches the execution directly from the plinth of the statue of Baelor the Blessed. Sansa WITNESS_IN already exists per baseline; Arya is explicitly present and sees everything. NOT in baseline.
Confidence: HIGH

---

**F2.**
`joffrey-baratheon --WITNESS_IN--> ned-confesses-to-treason`
Tier: 1
Cite: `sources/chapters/agot/agot-arya-05.md:161`
Quote: `"Prince Joffrey … no, King Joffrey … stepped out from behind the shields of his Kingsguard. 'My mother bids me let Lord Eddard take the black, and Lady Sansa has begged mercy for her father.'"`
Justification: Joffrey is present at the false confession event at the Great Sept and personally pronounces the decision. He COMMANDS_IN execution (already exists per baseline) but his WITNESS_IN on the confession event (which precedes the execution) is a distinct edge.
Confidence: HIGH

---

**F3.**
`high-septon --WITNESS_IN--> ned-confesses-to-treason`
Tier: 1
Cite: `sources/chapters/agot/agot-arya-05.md:139,159`
Quote: `"The High Septon himself stood behind him … 'This man has confessed his crimes in the sight of gods and men, here in this holy place,' he intoned, in a deep swelling voice …"`
Justification: The High Septon physically stands behind Ned at the pulpit during the confession and officiates the proceedings; he speaks to the crowd and then asks Joffrey for the sentence.
Confidence: HIGH
NEW NODE CHECK: `high-septon` (position/character; likely a node exists for the High Septon; check for the AGOT-era High Septon node — the fat man in golden crown and white robes)

---

**F4.**
`sansa-stark --WITNESS_IN--> ned-confesses-to-treason`
Tier: 1
Cite: `sources/chapters/agot/agot-arya-05.md:143,151`
Quote: `"And there in their midst was Sansa, dressed in sky-blue silk … Sansa had hidden her face in her hands."`
Justification: Sansa is present in the cluster of lords and knights before the Sept during the confession, watching. She had already begged Joffrey for mercy (per baseline: `ned-confesses-to-treason` has `cersei-lannister COMMANDS_IN`; Sansa's presence as WITNESS_IN on the confession event itself is missing). Distinct from her WITNESS_IN on the execution.
Confidence: HIGH

---

**F5.**
`varys --WITNESS_IN--> ned-confesses-to-treason`
Tier: 1
Cite: `sources/chapters/agot/agot-arya-05.md:141`
Quote: `"she saw Varys the eunuch gliding among the lords in soft slippers and a patterned damask robe"`
Justification: Varys is physically present at the Sept during the confession scene. From Arya's POV he is identifiable in the crowd; he is also mentioned in the Arya text as "came rushing over waving his arms" when Joffrey orders the execution (line 163).
Confidence: HIGH

---

**F6.**
`varys --WITNESS_IN--> execution-of-eddard-stark`
Tier: 1
Cite: `sources/chapters/agot/agot-arya-05.md:163`
Quote: `"Varys came rushing over waving his arms, and even the queen was saying something to him, but Joffrey shook his head."`
Justification: Varys is present and actively (if ineffectually) trying to stop the execution. He is a named witness.
Confidence: HIGH

---

**F7.**
`cersei-lannister --WITNESS_IN--> execution-of-eddard-stark`
Tier: 1
Cite: `sources/chapters/agot/agot-arya-05.md:163`
Quote: `"even the queen was saying something to him, but Joffrey shook his head"`
Justification: Cersei is present and attempts (verbally) to stop the execution. She is named as watching from the cluster at the Sept.
Confidence: HIGH

---

**F8.**
`sandor-clegane --WITNESS_IN--> ned-confesses-to-treason`
Tier: 1
Cite: `sources/chapters/agot/agot-arya-05.md:141`
Quote: `"Arya recognized the Hound, wearing a snowy white cloak over his dark grey armor, with four of the Kingsguard around him."`
Justification: Sandor Clegane is present in the cluster at the Sept during the confession event.
Confidence: HIGH

---

### CLUSTER G — Sansa as unwitting informant

**G1.**
`sansa-stark --DECEIVES--> cersei-lannister`
NOTE: This is the wrong direction — Sansa is not deceiving Cersei; she is naively informing her. FLAG as non-starter for DECEIVES.

**G1 (reformulated):**
`sansa-stark --ENABLES--> cersei-orders-ned-s-arrest`
Tier: 1
Cite: `sources/chapters/agot/agot-sansa-04.md:111`
Quote: `"Why else should you have come to me and told me of your father's plan to send you away from us, if not for love?" … "Father wouldn't even give me leave to say farewell. … He was going to take me back to Winterfell …"`
Justification: Sansa reveals to Cersei (pre-arrest) that Ned was planning to send the girls home — which confirms to Cersei that Ned was acting and not waiting. Cersei learns from Sansa's visit that Ned's hand is moving. This ENABLES Cersei's decision to accelerate the arrest. Sansa acts without knowledge of the consequences; ENABLES (not CAUSES) captures the structural role without attributing blame.
Confidence: HIGH

---

### CLUSTER H — Vayon Poole and Jeyne Poole

**H1.**
`vayon-poole --AGENT_IN--> gold-cloaks-betray-ned`
Tier: 2
Cite: `sources/chapters/agot/agot-sansa-04.md:13`
Quote: `"She had grown up to the sound of steel in the yard, and scarcely a day of her life had passed without hearing the clash of sword on sword … She heard it as she had never heard it before … There were bodies on the stair of the Tower of the Hand, and the steps were slick with blood."`
Justification: Jeyne Poole reports bodies on the stair of the Tower of the Hand. Vayon Poole (the steward) disappears after the arrest, with the implication he was killed or arrested. However, the text does NOT explicitly state Vayon was at the throne-room betrayal or killed there. The chapter text in agot-sansa-04 shows Vayon's absence (Jeyne's question about her father, the councillors' non-answer). UNCERTAIN — Vayon may have been killed at the Tower of the Hand, not the throne room.
Confidence: LOW (Vayon's fate is ambiguous in the text; do not mint this edge without wiki verification)
FLAG FOR ORCHESTRATOR: check wiki for Vayon Poole's fate.

---

**H2.**
`petyr-baelish --AGENT_IN--> [vayon-poole-disappearance]`
Tier: 2
Cite: `sources/chapters/agot/agot-sansa-04.md:71,77`
Quote: `"I'll find a place for her." "Not in the city," said the queen. … "Tell her that Littlefinger will be taking her to see her father, that ought to calm her down."`
Justification: Littlefinger takes charge of Jeyne Poole's disposition, with the implication that he is complicit in the suppression of Vayon Poole's disappearance. This is strong circumstantial evidence of Littlefinger as an agent in Vayon's fate, but the text does not show it directly.
Confidence: LOW (circumstantial only)
FLAG FOR ORCHESTRATOR: this may belong to a later character-arc track for Jeyne Poole rather than this dip.

---

### CLUSTER I — Pycelle as Cersei's spy

**I1.**
`pycelle --DECEIVES--> eddard-stark`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-12.md:23,31`
Quote: `"There was a raven this morning, a letter for the queen from her lord father. I thought you had best know." … Ned had little doubt that he was bound straight for the royal apartments, to whisper at the queen. I thought you had best know, indeed … as if Cersei had not instructed him to pass along her father's threats.`
Justification: Pycelle ostensibly informs Ned of Tywin's letter "for his benefit," but Ned sees through it — Pycelle is relaying the threat on Cersei's behalf, performing helpfulness while actually serving the queen. This is a DECEIVES edge that is explicit in Ned's observation of Pycelle's behavior.
Confidence: HIGH

---

### CLUSTER J — cersei-orders-the-sleeping-guards-executed (causal island)

**J1.**
`cersei-orders-the-sleeping-guards-executed --ENABLES--> arrest-of-eddard-stark`
Tier: 2
Cite: (no direct quote available in these chapters — the event is referenced in the baseline as a known node, not a chapter-textual event visible to these POVs)
Justification: The execution of Ned's sleeping guards removes the protective layer around the Tower of the Hand before the arrest. Without a specific quote from these seven chapters, I cannot confirm the text. FLAG FOR ORCHESTRATOR: this causal island was noted in baseline but requires a different chapter source (likely an earlier Eddard chapter or another POV) for the verbatim quote. Do NOT mint without quote verification.
Confidence: LOW (no quote available from target chapters)

---

### CLUSTER K — Lancel Lannister as instrument

**K1.**
`lancel-lannister --AGENT_IN--> death-of-robert-baratheon`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-15.md:149`
Quote: `"Oh, indeed. Cersei gave him the wineskins, and told him it was Robert's favorite vintage."`
Justification: Varys identifies Lancel as the squire who provided Robert the wine. Ser Barristan confirms "The elder [squire]" in agot-eddard-13:149: `"The wine was from the king's own skin … His squire would fetch him a fresh skin whenever he required it." "The elder," said Ser Barristan. "Lancel."` Lancel is the instrument of the poisoning, acting as Cersei's tool.
Cite (supplementary): `sources/chapters/agot/agot-eddard-13.md:149`
Quote (supplementary): `"The wine was from the king's own skin … His squire would fetch him a fresh skin whenever he required it." / "The elder," said Ser Barristan. "Lancel."`
Confidence: HIGH
NEW NODE CHECK: `lancel-lannister` — almost certainly exists as a wiki-sourced node; verify slug.

---

**K2.**
`cersei-lannister --COMMANDS_IN--> death-of-robert-baratheon`
Tier: 1
Cite: `sources/chapters/agot/agot-eddard-15.md:111`
Quote: `"Oh, indeed. Cersei gave him the wineskins, and told him it was Robert's favorite vintage."`
Justification: Cersei directly gives Lancel the strongwine wineskins, framing it as Robert's favorite. Whether `death-of-robert-baratheon` already has a `cersei-lannister COMMANDS_IN` edge is unclear from baseline — it was not listed among the existing edges. Propose as a gap.
Confidence: HIGH (text is clear; confidence in edge gap is high)

---

## HARVEST ROWS

`agot-eddard-12.md:15 / food / Pycelle sets a stoppered flask of "the milk of the poppy" on the bedside table for Ned's leg pain`

`agot-eddard-12.md:37 / food / Littlefinger visits and mentions Lady Tanda expects him "to lunch with her" and will "roast me a fatted calf"; jokes about Tanda's daughter being "as fatted"`

`agot-eddard-12.md:101 / description / Cersei arrives at sunset in the godswood: "leather boots and hunting greens" with a "brown cloak," bruise from Robert on her face, yellow-faded, swelling down`

`agot-eddard-12.md:107 / description / Cersei in the godswood: "curling blond hair moved in the wind, and her eyes were green as the leaves of summer"`

`agot-eddard-12.md:101 / quote (load-bearing) / "She came alone, as he had bid her." — confirms Cersei's trust that Ned would not seize her; relevant to DECEIVES or MOTIVATES chain`

`agot-eddard-12.md:129 / quote (load-bearing) / "All three are Jaime's," he said. It was not a question. / "Thank the Gods." — verbatim confession of Joffrey's parentage`

`agot-eddard-12.md:141 / quote / "The night of our wedding feast, the first time we shared a bed, he called me by your sister's name. He was on top of me, in me, stinking of wine, and he whispered Lyanna." — Cersei on Robert's wedding-night betrayal`

`agot-eddard-12.md:169 / quote (load-bearing, foreshadowing) / "When you play the game of thrones, you win or you die. There is no middle ground." — Cersei to Ned; this is the arc's keynote quote`

`agot-eddard-13.md:19 / description / Ned dresses for Robert's deathbed summons: "white linen tunic and grey cloak, trousers cut open down his plaster-sheathed leg, his badge of office, and last of all a belt of heavy silver links. He sheathed the Valyrian dagger at his waist."`

`agot-eddard-13.md:29 / description / Robert's deathbed: "green doublet lay on the floor, slashed open and discarded, the cloth crusted with red-brown stains. The room smelled of smoke and blood and death."`

`agot-eddard-13.md:47 / description / Robert's wound: "The boar must have been a fearsome thing. It had ripped the king from groin to nipple with its tusks. The wine-soaked bandages … were already black with blood, and the smell off the wound was hideous."`

`agot-eddard-13.md:85 / quote / "Serve the boar at my funeral feast. Apple in its mouth, skin seared crisp. Eat the bastard." — Robert's dying request; food + hospitality (dark irony: the boar that killed him to be eaten)`

`agot-eddard-13.md:103 / food-drink / Pycelle gives Robert "the milk of the poppy," Robert drinks deeply; "his black beard was beaded with thick white droplets"`

`agot-eddard-13.md:213 / description / Littlefinger arrives for the midnight meeting: "clad in a blue velvet tunic with puffed sleeves, his silvery cape patterned with mockingbirds"`

`agot-eddard-13.md:271 / quote (load-bearing) / "I ought to make you say it, but that would be cruel … For the sake of the love I bear for Catelyn, I will go to Janos Slynt this very hour and make certain that the City Watch is yours. Six thousand gold pieces should do it." — Littlefinger's performative offer; the gold-cloak bribery in his own words`

`agot-eddard-14.md:11 / description / Dawn scene: "men in mail and leather and crimson cloaks were making the morning ring to the sound of swords" in the yard; Sandor Clegane gallops across "to drive an iron-tipped lance through a dummy's head"`

`agot-eddard-14.md:15 / food / Ned "broke his fast with his daughters and Septa Mordane." Sansa "stared sullenly at her food and refused to eat, but Arya wolfed down everything that was set in front of her."`

`agot-eddard-14.md:83 / description / Throne room scene: Joffrey in "cloth-of-gold doublet and a red satin cape" on the Iron Throne; Sandor in "mail and soot-grey plate and his snarling dog's-head helm" at the foot of the stair`

`agot-eddard-14.md:83 / description / Cersei at throne room: "a gown of sea-green silk, trimmed with Myrish lace as pale as foam … a golden ring with an emerald the size of a pigeon's egg, on her head a matching tiara"`

`agot-eddard-14.md:95 / quote (load-bearing) / Cersei rips Robert's letter: "We have a new king now … Bend the knee, my lord. Bend the knee and swear fealty to my son, and we shall allow you to step down as Hand and live out your days in the grey waste you call home." — Cersei's ultimatum`

`agot-eddard-14.md:125 / quote (load-bearing, already in baseline node) / "Littlefinger slid Ned's dagger from its sheath and shoved it up under his chin. His smile was apologetic. 'I did warn you not to trust me, you know.'" — confirm attach as evidence_quote on littlefinger-betrays-ned if not already done`

`agot-eddard-15.md:13 / description / Ned in the black cell: "The straw on the floor stank of urine. There was no window, no bed, not even a slop bucket. … walls of pale red stone festooned with patches of nitre, a grey door of splintered wood, four inches thick and studded with iron."`

`agot-eddard-15.md:35 / food-drink / Gaoler brings a clay jug of water — Ned's first drink; "The clay was cool and beaded with moisture. Ned grasped it with both hands and gulped eagerly."`

`agot-eddard-15.md:59 / food-drink / Second gaoler (actually Varys in disguise) brings a wineskin: "Wine … Drink, Lord Eddard." — Ned's prison wine; described as "dregs," not poisoned`

`agot-eddard-15.md:63 / description / Varys in disguise: "plump cheeks were covered with a dark stubble of beard … transformed himself into a grizzled turnkey, reeking of sweat and sour wine"`

`agot-eddard-15.md:103 / quote (load-bearing) / "If there was one soul in King's Landing who was truly desperate to keep Robert Baratheon alive, it was me … For fifteen years I protected him from his enemies, but I could not protect him from his friends." — Varys to Ned in the black cell; key evidence for Varys's claims re: his own role`

`agot-eddard-15.md:131 / quote / "Cersei is no fool. She knows a tame wolf is of more use than a dead one." — Varys paraphrasing Cersei's calculation; matches the COMMANDS_IN quote on ned-confesses-to-treason in baseline`

`agot-eddard-15.md:155 / quote (load-bearing) / "The next visitor who calls on you could bring you bread and cheese and the milk of the poppy for your pain … or he could bring you Sansa's head." — Varys's ultimatum that breaks Ned; food used as contrast marker for the threat`

`agot-arya-05.md:11 / food / Arya catches a plump pigeon on the Street of Flour; tries to trade it for a tart from a pushcart man`

`agot-arya-05.md:19 / food / Pushcart man selling tarts: "blueberries and lemons and apricots"; Arya wants one but has no coin`

`agot-arya-05.md:43 / food / Flea Bottom pot-shops: "huge tubs of stew had been simmering for years … trade half your bird for a heel of yesterday's bread and a 'bowl o' brown'" — stew with barley, carrot, onion, turnip, sometimes apple, "a film of grease swimming on top"`

`agot-arya-05.md:43 / food / "Mostly she tried not to think about the meat." — Arya eating the Flea Bottom brown stew; "Once she had gotten a piece of fish."`

`agot-arya-05.md:137 / description / Ned at the Great Sept pulpit: "dressed in a rich grey velvet doublet with a white wolf sewn on the front in beads, and a grey wool cloak trimmed with fur, but he was thinner than Arya had ever seen him, his long face drawn with pain"`

`agot-arya-05.md:139 / description / High Septon at Sept: "a squat man, grey with age and ponderously fat, wearing long white robes and an immense crown of spun gold and crystal that wreathed his head with rainbows whenever he moved"`

`agot-arya-05.md:141 / description / Joffrey at execution: "all crimson, silk and satin patterned with prancing stags and roaring lions, a gold crown on his head"`

`agot-arya-05.md:141 / description / Cersei at execution: "a black mourning gown slashed with crimson, a veil of black diamonds in her hair"`

`agot-arya-05.md:141 / description / Arya identifies "the short man with the silvery cape and pointed beard" as Littlefinger at the Sept — she recognizes him as the man "who had once fought a duel for Mother"`

`agot-arya-05.md:171 / description / Ser Ilyn Payne wields Ice: "As he lifted the blade above his head, sunlight seemed to ripple and dance down the dark metal, glinting off an edge sharper than any razor." — Ice's appearance at the execution`

`agot-sansa-04.md:23 / food / Sansa confined in Maegor's Holdfast: "They were fed—hard cheese and fresh-baked bread and milk to break their fast, roast chicken and greens at midday, and a late supper of beef and barley stew"`

`agot-sansa-04.md:37 / description / Ser Boros Blount: "ugly man with a broad chest and short, bandy legs. His nose was flat, his cheeks baggy with jowls, his hair grey and brittle. Today he wore white velvet, and his snowy cloak was fastened with a lion brooch."`

`agot-sansa-04.md:85 / description / Littlefinger looking at Sansa: "Something about the way the small man looked at her made Sansa feel as though she had no clothes on. Goose bumps pimpled her skin." — predatory quality, important for later arc`

`agot-sansa-04.md:123 / quote / "She reminds me of the mother, not the father. Look at her. The hair, the eyes. She is the very image of Cat at the same age." — Littlefinger on Sansa; key for his later obsession`

`agot-sansa-04.md:179 / food / After writing the letters: Varys uses Ned's seal to stamp them with "pale white beeswax" warmed over a candle`

`agot-sansa-06.md:13 / food / After execution: Sansa cannot eat; "dishes piled up on the table beneath her window, untouched and spoiling, until the servants took them away again" — grief-food motif`

`agot-sansa-06.md:19 / food-drink / Grand Maester Pycelle visits and gives Sansa "a potion of honeywater and herbs and told her to drink a swallow every night. She drank it all right then and went back to sleep."`

`agot-sansa-06.md:65 / food / Sansa before court: "She drank a glass of buttermilk and nibbled at some sweet biscuits as she waited, to settle her stomach."`

`agot-sansa-06.md:15 / quote (load-bearing, foreshadowing) / Sansa sees "the gold cloaks fling him down, saw Ser Ilyn striding forward, unsheathing Ice from the scabbard on his back, saw the moment … the moment when … she had wanted to look away … yet somehow she could not turn her head" — her WITNESS_IN of execution, in her own retrospective POV`

`agot-sansa-06.md:87 / quote / "There are no heroes … Life is not a song, sweetling. You may learn that one day to your sorrow." — Littlefinger to Sansa; Sansa remembers it while watching Janos Slynt nod approvingly in court`

`agot-sansa-06.md:167 / description / Sandor Clegane wipes Sansa's blood: "With a delicacy surprising in such a big man, he dabbed at the blood welling from her broken lip." — his restrained protectiveness; physical description of the act`

---

## NEEDS_VOCAB FLAGS

None. All proposed edge types are within the locked vocabulary (CAUSES, TRIGGERS, ENABLES, MOTIVATES, SUSPECTED_OF, AGENT_IN, VICTIM_IN, COMMANDS_IN, WITNESS_IN, PARTICIPATES_IN, DECEIVES, BETRAYS, KILLS, GUARDS). No new type was required.

---

## NEW NODE FLAGS (summary)

| Proposed slug | Type | Basis | Dedup check needed |
|---|---|---|---|
| `renly-offers-ned-one-hundred-swords` | event.incident | agot-eddard-13:163 | Baseline: candidate mint, no node found |
| `renly-flees-kings-landing` | event.flight | agot-eddard-14:59 | Likely no node; check wiki |
| `tomard` | person.guard | agot-eddard-12, 14 | "Fat Tom" — check for stub |
| `varly` | person.guard | agot-eddard-14:123 | Likely no standalone node |
| `cayn` | person.guard | agot-eddard-14:123 | Likely no standalone node |
| `lancel-lannister` | person.character | agot-eddard-13:149 | Almost certainly exists via wiki pass; verify slug |
| `high-septon` (AGOT-era) | person.religious | agot-arya-05:139 | Check for era-specific node vs. generic title |

---

*End of Lens 2 output.*
