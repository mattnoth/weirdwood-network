# Fresh Verify — Ned's Downfall Enrichment (run_id: neds-downfall-enrichment-s137)
Verified: 2026-06-23 | Verifier: independent adversarial subagent | Source read: agot-eddard-12, -13, -14, -15, agot-arya-05

---

## EDGE 1: `ned-discovers-the-truth-of-joffrey-s-parentage` --ENABLES--> `arrest-of-eddard-stark`
**Cited line:** agot-eddard-12.md:159 — "When the king returns from his hunt, I intend to lay the truth before him. You must be gone by then."

**Check:** Line 159 is confirmed: Ned warns Cersei he will tell Robert the truth and gives her a chance to flee. The quote is accurate and present.

**Problem — Agency-collapse / structural overclaim:** The discovery of the truth is not merely an ENABLES precondition for the arrest; it is the *constitutive reason* the confrontation exists at all. More precisely: the claim that discovery ENABLES arrest is too distal and smuggles in a clean causal chain that requires at least two major intervening nodes already in the graph — Robert's death (which removes Ned's protection) and Cersei's decision to seize Joffrey's succession rather than flee. The discovery enables the *warning* and the *threat to tell Robert*, but what directly triggers the arrest is Ned's proclamation of Stannis's right to the throne in the throne room (agot-eddard-14) after Cersei tears up Robert's letter. The arrest is a reaction to that specific defiance, not to the discovery per se.

Additionally: Ned's warning in the godswood explicitly gives Cersei an *exit ramp* — if she had fled, there would be no arrest. The fact that Cersei chose to stay and fight rather than flee is the decisive choice that leads to the arrest. The discovery alone — without Cersei's countermove — would not produce an arrest.

**Ruling: ADJUST.** Down-tier the edge type. ENABLES overclaims the directness. The correct framing is `ned-discovers-the-truth-of-joffrey-s-parentage` --MOTIVATES--> `arrest-of-eddard-stark`, routing through Ned's choice to confront Cersei and then refuse to bend the knee. Alternatively, this edge should be rejected and replaced with a `ned-discovers-the-truth-of-joffrey-s-parentage` --TRIGGERS--> `ned-warns-cersei-to-flee` node + a separate chain. If the graph has no intermediate warning/confrontation node, MOTIVATES is the least overclaiming option. Do not use ENABLES.

---

## EDGE 2: `varys-confirms-cersei-s-role-in-robert-s-death` --ENABLES--> `ned-confesses-to-treason`
**Cited line:** agot-eddard-15.md:135 — "Tell the queen that you will confess your vile treason, command your son to lay down his sword, and proclaim Joffrey as the true heir."

**Check:** Line 135 is confirmed. Varys gives Ned the terms of the deal in the cell: confess, command Robb to stand down, proclaim Joffrey. This is the pitch, not the confession itself. The confession happens in agot-arya-05:149-154, well after this scene.

**Problem — Wrong upstream cause / duplicate causation:** Varys's cell-visit frames the *path to survival*, but the citation offered (line 135) is Varys delivering Cersei's offer, not Varys confirming Robert's murder. The line that confirms Cersei's role in Robert's death is agot-eddard-15.md:111 — "Cersei gave him the wineskins, and told him it was Robert's favorite vintage." That is Edge 3, not this one.

More fundamentally: what ENABLES the confession is Ned's capitulation under the threat to Sansa (agot-eddard-15:147-157: "Your daughter's life, my lord? How precious is that?"). The confession is driven by the Sansa threat, not by the Robert-death confirmation. The graph presumably already has a `cersei-commands-ned-to-confess` (or `cersei-threatens-sansa`) edge; Varys is the *messenger/architect* of that pressure, not an independent enabling precondition. The confirmation of Robert's murder is emotionally relevant (Ned says "Gods forgive me," line 113) but does not causally enable the confession — Ned would still have faced the same choice even without knowing the exact mechanism of Robert's death.

**Ruling: REJECT.** The causal attribution is wrong. Varys confirming Cersei's role in Robert's death does not ENABLE the confession. The confession is enabled by Cersei's threat to Sansa, delivered through Varys. If an edge is warranted here, it should be `varys-threatens-sansa-stark` or `cersei-threatens-sansa-stark` --ENABLES--> `ned-confesses-to-treason`, not this one. The cited Robert-death confirmation is incidental context in the same scene, not a causal precondition.

---

## EDGE 3: `cersei-lannister` --SUSPECTED_OF--> `death-of-robert-baratheon`
**Cited line:** agot-eddard-15.md:111 — "Oh, indeed. Cersei gave him the wineskins, and told him it was Robert's favorite vintage."

**Check:** Line 111 is confirmed. Varys says this to Ned in the cell. The quote is accurate. Varys then adds: "It was not wine that killed the king. It was your mercy" (line 111-112), muddying the causal picture — Varys acknowledges the wine created the conditions (Robert too drunk to fight the boar effectively) but locates the final cause in Ned's mercy (warning Cersei), which triggered her need to act.

**SUSPECTED_OF appropriateness:** Varys presents this as established fact ("Oh, indeed"), based on questioning Lancel. This is stronger than SUSPECTED_OF would normally suggest — Varys presents it as confirmed to Ned. However, this is Varys speaking in a private cell with no corroboration visible to the reader, and the verifiable record in the text is that Lancel served wine from Cersei's wineskins. The chain (Cersei ordered the strong wine to impair Robert → boar killed him → she is guilty of murder) is an inference, not a witnessed fact. SUSPECTED_OF is therefore *correct* as the edge type — it accurately reflects that the text presents Cersei as the plausible architect without a courtroom-level smoking gun.

**Ruling: CONFIRM.** Edge type SUSPECTED_OF is calibrated correctly. Quote verified at line 111.

---

## EDGE 4: `eddard-stark` --PREVENTS--> `renly-offers-ned-swords-to-seize-joffrey`
**Cited line:** agot-eddard-13.md:181 — "He found himself wondering if he had done the right thing by refusing Lord Renly's offer."

**Check:** Line 181 is confirmed: "He found himself wondering if he had done the right thing by refusing Lord Renly's offer."

**New-node framing check:** The offer itself is at agot-eddard-13.md:163-167 (confirmed): Renly offers "a hundred swords" and proposes to "get Joffrey away from his mother and take him in hand… We should seize Myrcella and Tommen as well." Ned refuses at line 169: "Robert is not dead yet…I will not dishonor his last hours on earth by shedding blood in his halls and dragging frightened children from their beds."

**Problem — Wrong edge verb / logic inversion:** The edge `eddard-stark` --PREVENTS--> `renly-offers-ned-swords-to-seize-joffrey` is logically backwards. The *offer* happened first (agot-eddard-13:163-167); what Ned *prevented* was the *execution* of the offer — i.e., the actual seizure of Joffrey, not the offer itself. You cannot prevent something that has already occurred. The edge should read `eddard-stark` --PREVENTS--> `seizure-of-joffrey-by-renly` (a potential event that never happened), not the offer node itself. An offer that was made cannot be prevented by the person who received and refused it.

Furthermore, PREVENTS as a verb implies Ned actively blocked something from happening. What happened is Ned *declined* a proposed action. The more accurate framing would be either:
- A `ned-refuses-renly-s-offer` edge as an event node, with `eddard-stark` --AGENT_IN--> that node; or
- `eddard-stark` --PREVENTS--> `coup-to-seize-joffrey` (the would-have-happened outcome).

**Ruling: REJECT.** The edge target is wrong — Ned cannot PREVENT an offer that has already been made. The intended meaning (Ned's refusal prevented the coup) should be modeled as `eddard-stark` --PREVENTS--> a `seizure-of-joffrey` or `renly-seizes-joffrey` event node, not the offer node itself. Mint a corrected edge or a new event node for the refused coup.

---

## EDGE 5: `petyr-baelish` --DECEIVES--> `eddard-stark`
**Cited line:** agot-eddard-14.md:125 — "His smile was apologetic. 'I did warn you not to trust me, you know.'"

**Check:** Line 125 is confirmed. This is the moment Littlefinger presses the dagger under Ned's chin in the throne room while smiling apologetically.

**DECEIVES appropriateness:** This is unambiguous. Littlefinger promised Ned the gold cloaks (he "arranged" their loyalty per line 271 of agot-eddard-13 and the line 49 reference in agot-eddard-14: "That little task you set me is accomplished"), knowing full well he had actually bought them for Cersei/Joffrey or at minimum that his double-game meant Ned would be betrayed. The "I did warn you" is the textual acknowledgment of deliberate deception. DECEIVES is correct.

**Ruling: CONFIRM.** Quote verified at line 125. DECEIVES is correct.

---

## EDGE 6: `varys` --DECEIVES--> `eddard-stark`
**Cited line:** agot-eddard-15.md:139 — "Oh, I feed him choice whispers, sufficient so that he thinks I am his … just as I allow Cersei to believe I am hers."

**Check:** Line 139 is confirmed. Varys explicitly tells Ned he deceives Littlefinger and Cersei both into thinking they own him. The "just as" construction implies he does the same to Ned — he has been allowing Ned to believe Varys serves him.

**DECEIVES appropriateness:** Solid. The cell visit itself has a dual nature: Varys presents it as acting in the realm's interest, but he explicitly confirms he is managing Ned as one of several puppets. The deception of Ned is implicit but strongly implied by the structure of the speech ("I feed him…just as I allow Cersei…"). Varys's refusal to actually free Ned (line 91) and his direction to simply deliver the confession confirms he is not acting for Ned's benefit.

**Ruling: CONFIRM.** Quote verified at line 139. DECEIVES is correctly applied.

---

## EDGE 7: `pycelle` --DECEIVES--> `eddard-stark`
**Cited line:** agot-eddard-12.md:31 — "Ned had little doubt that he was bound straight for the royal apartments, to whisper at the queen."

**Check:** Line 31 is confirmed. This is Ned's internal observation after Pycelle leaves: Pycelle had said "I thought you had best know" about Tywin's letter — presenting himself as doing Ned a favor — when Ned immediately recognizes this was Cersei's setup (line 31: "as if Cersei had not instructed him to pass along her father's threats").

**DECEIVES appropriateness:** Pycelle pretends to be giving Ned useful intelligence ("I thought you had best know") while actually delivering a veiled threat on Cersei's behalf. Ned correctly reads this as deception (internal monologue at line 31). DECEIVES is appropriate.

**Ruling: CONFIRM.** Quote verified at line 31. DECEIVES is correct — though note the citation is from Ned's interior monologue (not dialogue), so it is inference-from-observation, not a direct statement by Pycelle. This is appropriate for DECEIVES since deception is typically visible only through the victim's perception.

---

## EDGE 8: `renly-baratheon` --AGENT_IN--> `renly-offers-ned-swords-to-seize-joffrey`
**Cited line:** agot-eddard-13.md:167

**Check:** Line 167 is confirmed: "Strike! Now, while the castle sleeps… We must get Joffrey away from his mother and take him in hand… The man who holds the king holds the kingdom."

**Ruling: CONFIRM.** Renly is clearly the proposer/agent. Quote verified at line 167.

---

## EDGE 9: `arya-stark` --WITNESS_IN--> `execution-of-eddard-stark`
**Cited line:** agot-arya-05.md:163

**Check:** Line 163 is confirmed: "High atop the pulpit, Ser Ilyn Payne gestured and the knight in black-and-gold gave a command. The gold cloaks flung Lord Eddard to the marble, with his head and chest out over the edge." Arya is the POV character; she witnesses from the base of Baelor's statue (line 133-135). Lines 165-175 confirm she is present, struggling through the crowd, and hears/witnesses the execution.

**Ruling: CONFIRM.** Arya is the POV witness of this entire scene.

---

## EDGE 10: `varys` --WITNESS_IN--> `execution-of-eddard-stark`
**Cited line:** agot-arya-05.md:163

**Check:** Arya sees Varys at line 141: "she saw Varys the eunuch gliding among the lords in soft slippers and a patterned damask robe." This is before the execution begins. The text then describes the High Septon speaking (line 159), Joffrey's decision (line 161), and Ser Ilyn ascending (line 163). Arya then plunges into the crowd (lines 165-175). The text does not explicitly confirm Varys stayed for the beheading — it only confirms he was present in the initial gathering. Arya's view is blocked by the crowd as she fights through it (line 165: "She landed on a man in a butcher's apron…").

**Mild concern:** The text establishes Varys's presence at the start of the execution-scene gathering (line 141), and at line 163 "Varys came rushing over waving his arms" trying to dissuade Joffrey — confirmed. So Varys is actively present at the moment of Joffrey's command, and the execution follows immediately. His presence as a witness is well supported.

**Ruling: CONFIRM.** Line 163 confirms Varys was present and actively intervening at the moment of the command, making WITNESS_IN appropriate.

---

## EDGE 11: `cersei-lannister` --WITNESS_IN--> `execution-of-eddard-stark`
**Cited line:** agot-arya-05.md:163

**Check:** Line 141 confirms Cersei's presence at the scene: "His queen mother stood beside him in a black mourning gown slashed with crimson." Line 161 states: "My mother bids me let Lord Eddard take the black" — she was present and had already counseled mercy. Line 163: "even the queen was saying something to him" (she is trying to dissuade Joffrey from the execution order).

**Adversarial question — does the text show Cersei TRYING TO STOP Joffrey?** YES, confirmed. Line 161 quotes Joffrey: "My mother bids me let Lord Eddard take the black" — Cersei had already told him to spare Ned. And line 163 confirms she was actively speaking to Joffrey at the moment of the command. The text does show her opposing the execution.

**Ruling: CONFIRM.** Cersei's presence is confirmed at lines 141 and 163. WITNESS_IN is correct. Additional context: she was not a passive witness — she was actively trying to prevent the execution. This enriches the node but does not change the WITNESS_IN type.

---

## EDGE 12: `high-septon` --OFFICIATES--> `ned-confesses-to-treason`
**Cited line:** agot-arya-05.md:159

**Check:** Line 159 is confirmed: "The High Septon knelt before Joffrey and his mother. 'As we sin, so do we suffer,' he intoned… 'This man has confessed his crimes in the sight of gods and men, here in this holy place.'" Line 139 (of arya-05) confirms: "The High Septon himself stood behind him, a squat man, grey with age and ponderously fat, wearing long white robes and an immense crown of spun gold and crystal." He is physically officiating the ceremony at the Great Sept.

**Ruling: CONFIRM.** Quote verified. The High Septon is conducting the formal religious ceremony at which the confession occurs.

---

## EDGE 13: `janos-slynt` --KILLS--> `varly`
**Cited line:** agot-eddard-14.md:123

**Check:** Line 123 is confirmed: "Janos Slynt himself slashed open Varly's throat."

**Ruling: CONFIRM.** Direct, unambiguous text. Quote verified.

---

## EDGE 14: `sandor-clegane` --KILLS--> `cayn`
**Cited line:** agot-eddard-14.md:123

**Check:** Line 123 is confirmed: "Then the Hound was on him. Sandor Clegane's first cut took off Cayn's sword hand at the wrist; his second drove him to his knees and opened him from shoulder to breastbone."

**Ruling: CONFIRM.** Direct text. Quote verified.

---

## EDGE 15: `cayn` --VICTIM_IN--> `gold-cloaks-betray-ned`
**Cited line:** agot-eddard-14.md:123

**Check:** Line 123 is confirmed. Cayn is killed by the Hound in the same scene where Janos Slynt (commander of the gold cloaks) orders/participates in the killing of Ned's guards. Cayn is one of Ned's guards who dies in this betrayal (lines 121-125).

**Ruling: CONFIRM.** VICTIM_IN is appropriate. Cayn dies as a direct victim of the gold-cloak betrayal. Quote verified.

---

## VERDICT SUMMARY

**CONFIRM: 11** (Edges 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
**ADJUST: 1** (Edge 1 — ENABLES → MOTIVATES; too distal, routes through Ned's choice)
**REJECT: 2** (Edge 2 — wrong causal attribution, confession enabled by Sansa threat not Robert-death confirmation; Edge 4 — logical inversion, cannot PREVENTS an event that already occurred)

### Key findings for proposer review:
- **Edge 1** (discovery --ENABLES--> arrest): Down-tier to MOTIVATES; Robert's death and Cersei's decision to fight rather than flee are the more proximate causes.
- **Edge 2** (Varys-confirms-Cersei --ENABLES--> confession): Reject entirely; the enabling precondition for the confession is the Sansa threat (agot-eddard-15:147-157), not the Robert-death confirmation.
- **Edge 4** (Ned --PREVENTS--> Renly's offer): Reject; the offer already happened before Ned refused it. Correct target should be a would-have-been event node (the coup/seizure of Joffrey) or the edge should be reframed as `ned-refuses-renly-s-offer`.
