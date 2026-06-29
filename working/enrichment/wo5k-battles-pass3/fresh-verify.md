# Fresh-Verify Report — WO5K Battles Pass 3 (S166 edges)

**Verifier:** independent adversarial agent, no prior context  
**Date:** 2026-06-28  
**Scope:** 7 pending edges (A1, A2, A6, B9, B10, C1, C2) + node prose sanity + slug sanity  
**Method:** read chapter files from local cache only; never fetched  

---

## E1 — A1: `tywin-lannister MANIPULATES sybell-spicer` (via_bribe, tier-1)

**VERDICT: CONFIRM**

**Quote verbatim at cited location?** YES — `affc-jaime-07.md:79`: "I made certain of that, as your lord father bid me." — confirmed exact.

**Strongest supporting passage:**  
`affc-jaime-07.md:79–83`. Sybell says "as your lord father bid me" (she acts on Tywin's direction); Jaime immediately lists the reward package: "House Westerling has its pardon, and your brother Rolph has been made Lord of Castamere. What else would you have of us?" (:81). She then presses for more: "Your lord father promised me worthy marriages for Jeyne and her younger sister. Lords or heirs, he swore to me" (:83). This is a buyer/seller transaction in which Tywin set the terms and Sybell performed. Jaime's gloss: "Tywin Lannister was not a man to overlook such details" (:80). The direction is unmistakably Tywin → Sybell.

**Strongest contradicting passage:**  
One might argue the EXISTING `sybell-spicer CONSPIRES_WITH tywin-lannister` edge already encodes this relationship and that they were co-conspirators as peers, not a principal-agent hierarchy. However: Sybell calls Tywin "your lord father" and frames herself as executing his bid; the reward package was his to dispense (pardon, a lordship, marriage matches — none within Sybell's power to grant). The asymmetry is clear. MANIPULATES + via_bribe is not redundant with CONSPIRES_WITH: the former names the power vector; the latter names the alliance.

**One-line reason:** The text unambiguously establishes Tywin as the directing party and Sybell as the paid instrument; MANIPULATES + via_bribe is the correct edge type and correctly directional.

---

## E2 — A2: `sybell-spicer BETRAYS robb-stark` (tier-1)

**VERDICT: CONFIRM**

**Quote verbatim at cited location?** YES — same quote, same line (:79).

**Strongest supporting passage:**  
`affc-jaime-07.md:71–85`. Sybell lived under Robb's protection at the Crag (her husband Lord Gawen Westerling hosted Robb; Jeyne nursed him back to health). She benefited from his hospitality and marriage to her daughter, then covertly ensured no Stark heir could survive him — on his enemy's orders. This is betrayal in both the moral and the BETRAYS edge-type sense (guest/protector relation violated by covert subversion). Robb is the victim named by the act: "as your lord father bid me" in response to whether Jeyne carries his child.

**Strongest contradicting passage:**  
Sybell is not presented as a person under Robb's fealty or formal obligation (she is an in-law, not a sworn vassal). One could argue this is CONSPIRES_AGAINST or ACTS_AGAINST rather than BETRAYS. But BETRAYS applies when a personal-trust relationship is violated covertly — Robb trusted his wife's family; they sabotaged his dynastic survival. The edge is well-typed.

**One-line reason:** Sybell subverted the Stark marriage from within, on the enemy's instruction, while under Robb's implicit protection — BETRAYS is the correct type and victim is correctly named.

---

## E3 — A6: `grey-wind FORESHADOWS jeyne-westerling-kept-barren` (tier-2)

**VERDICT: UNCERTAIN — lean toward CONFIRM with caveat**

**Quote verbatim at cited location?** YES — `asos-catelyn-02.md:189`: "He bares his teeth every time Ser Rolph comes near him." — exact.

**Strongest supporting passage:**  
`asos-catelyn-02.md:189–205`. Grey Wind's hostility is specifically to Ser Rolph Spicer — Sybell's brother, not Jeyne, and not the Westerling family generally. Catelyn reads the warning as supernatural and demands Robb send Rolph away. Robb eventually agrees to find him a pretext ("I will find some duty for Ser Rolph, some pretext to send him away"). Rolph is then dispatched by Robb to deliver Martyn Lannister to the Golden Tooth (asos-catelyn-05:29) — removing him from Robb's side. The text DOES create a sustained wolf-warning-about-Spicer-treachery pattern, and the Spicer betrayal (via Sybell) is later confirmed. The FORESHADOWS direction (Grey Wind → the event) is a reader-craft edge, standard for this type.

**Strongest contradicting passage:**  
Grey Wind's hostility is to Rolph, not Sybell — the foreshadow is at one remove (the wolf suspects the uncle, the actual betrayer is the mother). The target event (`jeyne-westerling-kept-barren`) is the specific act of keeping Jeyne barren, not the broader Spicer betrayal. Grey Wind's snarl does not directly foreshadow barrenness per se; it foreshadows treachery by a Spicer. A more precise target would be something like `spicer-family-betrays-robb` (which may not exist as a hub). This creates a slight mismatch between the wolf's object (Rolph) and the edge's target (Sybell's act). The foreshadow is real but the target node is imprecise.

**One-line reason:** The wolf-warning-about-Spicer-treachery reading is load-bearing in-text and Catelyn explicitly elevates it to supernatural significance; the mismatch (Rolph vs. Sybell) is tolerable at tier-2 but worth noting — the edge survives, weakened.

**Recommended adjustment:** Add a note that the foreshadow resolves on the Spicer family as a unit (Rolph → Sybell → betrayal), not solely the barrenness mechanism. Tier-2 is appropriate.

---

## E4 — B9: `roose-bolton SUSPECTED_OF battle-at-duskendale` (tier-2)

**VERDICT: CONFIRM — stronger than the proposer claims**

**Quote verbatim at cited location?** YES — `asos-catelyn-04.md:91`: "Why would they go to Duskendale?" — exact. Also at the same line: "A third of my foot, lost for Duskendale?"

**Strongest supporting passage:**  
The text at `asos-catelyn-04.md:91` establishes Robb's bafflement: he never authorized the march ("Why would they go?"), and the loss is catastrophic ("A third of my foot"). The stronger evidence the proposer missed: `asos-jaime-05.md:129`, where Roose Bolton himself says to Jaime: "I gave him all the Karhold men still with me and sent him off with Glover." — Roose admits he PERSONALLY SENT Glover (and Karstark) to Duskendale. This is not merely circumstantial. Roose dispatched the army he knew would walk into Tywin's trap — confirmed by Tywin's own planning at `asos-tyrion-01.md:213`: "I've sent Lord Tarly to meet them, while Ser Gregor drives up the kingsroad to cut off their retreat. Tallhart and Glover will be caught between them." The dead were all non-Bolton bannermen (Glover, Tallhart, Karstark men). Roose's own Dreadfort contingent marched separately. The SUSPECTED_OF reading is strongly supported: Roose sent the non-Bolton foot into a trap he must have known existed (Tywin was actively springing it from KL while Roose held Harrenhal with its news network).

At `asos-catelyn-06:293`, Roose covers himself: "A folly, but Glover was heedless after he learned that Deepwood Motte had fallen. Grief and fear will do that to a man." This self-exculpatory framing is itself suspicious — Roose deflects onto Glover's emotional state rather than acknowledging he ordered the march.

**Strongest contradicting passage:**  
Roose's cover story (Glover's grief-driven heedlessness) is not definitively refuted in the 5 books. No character in the text accuses Roose of deliberately setting the trap. The wiki's "Background" section says Roose ordered the march but frames it without accusation of intent. The published text never provides the explicit smoking-gun (Roose admitting or being accused of deliberate sabotage).

**One-line reason:** Roose personally sent Glover & Tallhart to Duskendale (confirmed by his own words at asos-jaime-05:129) while the Lannister trap was already being sprung; the non-Bolton casualty pattern is load-bearing; SUSPECTED_OF is accurate and warranted, potentially undersells how damning the in-text evidence is.

**Note:** The proposer's cited quote ("Why would they go?") is good, but the stronger anchor is asos-jaime-05:129 where Roose himself says he sent them. Consider adding that cite to the edge.

---

## E5 — B10: `roose-bolton SUSPECTED_OF fighting-at-the-fords-of-the-trident` (tier-2)

**VERDICT: UNCERTAIN — lean toward DROP**

**Quote verbatim at cited location?** YES — `asos-catelyn-06.md:281`: "I blame myself. I delayed too long before leaving Harrenhal." — exact.

**Strongest supporting passage:**  
`asos-catelyn-06.md:281`: Roose's account identifies that the men lost were "Norrey, Locke, and Burley men chiefly, with Ser Wylis Manderly and his White Harbor knights as rear guard" — all non-Bolton bannermen, while his own Dreadfort contingent crossed first and survived. His "two-thirds of my strength" figure means 2/3 of his army crossed safely (his men); the rear-guard that was caught was the Stark-loyal component. The pattern of non-Bolton casualties parallels the Duskendale situation.

**Strongest contradicting passage:**  
Unlike Duskendale, Roose did NOT personally order the Ruby Ford rear-guard to their deaths. The sequence is: (a) high river forced small-boat crossing; (b) Aenys Frey left several days before Roose (so the timing issue pre-dates Roose's departure); (c) Roose was caught on the wrong bank when Gregor attacked — genuinely unable to help. The phrase "I delayed too long before leaving Harrenhal" is the only in-text hook for deliberate intent, and it is ambiguous — Roose may simply mean the rains caught him. Critically, there is NO "Why would they go to Duskendale?"-style bafflement moment from Robb or any character suggesting the Ruby Ford disposition was anomalous. Robb's reaction at :287 is "You did well, my lord" — not suspicion. The in-text evidence for deliberate rear-guard sacrifice at the Ruby Ford reduces to: (a) the casualties were non-Bolton, and (b) Roose's self-blame may be performed. That is pattern-inference, not load-bearing in-text suspicion.

**One-line reason:** The Ruby Ford suspicion rests on structural inference (non-Bolton casualties + performed self-blame) with no in-text "why would they go?" moment and no character voicing the suspicion — this is theory-adjacent; DROP or reduce to a note.

---

## E6 — C1: `battle-at-duskendale ENABLES red-wedding-conspiracy` (tier-2)

**VERDICT: CONFIRM**

**Quote verbatim at cited location?** YES — `asos-catelyn-04.md:91`: "A third of my foot, lost for Duskendale?" — exact.

**Strongest supporting passage:**  
`asos-catelyn-04.md:91` establishes the magnitude: a third of Robb's infantry destroyed in one battle. ENABLES captures a precondition (not a cause): the Duskendale loss materially degraded the host that would march to the Twins, removing a deterrent to Frey/Bolton betrayal. The edge mirrors the existing `karstark-host-deserts-robb ENABLES red-wedding-conspiracy` precedent — both edges model the same mechanism (attrition of Stark-loyal forces → conspiracy becomes viable). ENABLES is the honest type: Duskendale did not cause the Red Wedding; it made the betrayal safer/decisive.

**Strongest contradicting passage:**  
The Red Wedding conspiracy was a political/family decision (Frey honor-grudge + Bolton ambition + Tywin's coordination) that predated and was independent of the army's size. Even with a third more infantry, the Freys controlled the Twins (the chokepoint) and Roose commanded the northern rear-guard. A fuller host might not have changed the outcome. ENABLES implies a meaningful precondition, which the text supports via Robb's own despair ("A third of my foot") — but ENABLES risks implying more counterfactual determinism than the text asserts.

**One-line reason:** The attrition of a third of Robb's foot is book-confirmed, materially relevant to the conspiracy's military feasibility, and the ENABLES type with tier-2 correctly scopes the claim — CONFIRM.

---

## E7 — C2: `fighting-at-the-fords-of-the-trident ENABLES red-wedding-conspiracy` (tier-2)

**VERDICT: CONFIRM — with caveat on double-counting**

**Quote verbatim at cited location?** YES — `asos-catelyn-06.md:281`: "Two-thirds of my strength was on the north side when the Lannisters attacked those still waiting to cross." — exact.

**Strongest supporting passage:**  
The Ruby Ford fight is temporally proximate (it happens en route to the Twins, shortly before the Red Wedding). The losing side: non-Bolton rear-guard driven into the river. The surviving host that marched to the Twins was numerically weaker and disproportionately composed of Bolton-loyal Dreadfort men. This is NOT identical to Duskendale: Duskendale = loss of Robb's central infantry in the Crownlands weeks earlier; Ruby Ford = loss of the rear-guard immediately before the Twins. They are distinct battlefield events with distinct casualty profiles.

**Strongest contradicting passage:**  
The Ruby Ford losses (rear-guard caught crossing) are much harder to quantify as a standalone precondition. Roose estimates "two-thirds of my strength" on the north bank (safe), "those still waiting to cross" suffering losses. The wiki estimates roughly 2,000 men lost. The net force Roose brought to the Twins was "some five hundred horse and three thousand foot" (`asos-catelyn-06:297`). The Duskendale loss (~1,000+ dead, Glover/Tallhart/Karstark shattered) is arguably the larger and more strategically visible attrition. However, Duskendale and Ruby Ford are causally distinct: different battles, different dates, different sectors of Robb's host. ENABLES is independently honest for each.

**On double-counting:** The two ENABLES edges are NOT double-counting — they model separate events that both contributed to the same precondition (a thinned Stark-loyal host). This is analogous to having both a karstark-desertion ENABLES and a duskendale ENABLES: each names a distinct mechanism. The graph allows multiple ENABLES pointing to the same target when the preconditions are independently real.

**One-line reason:** The Ruby Ford loss is a genuine, distinct, book-confirmed attrition event immediately preceding the Red Wedding; ENABLES is honest and not double-counting with C1.

---

## Node Sanity: `jeyne-westerling-kept-barren.node.md`

**VERDICT: CLEAN — does NOT over-assert mechanism**

Read at `/Users/mnoth/source/asoiaf-chat/graph/nodes/events/jeyne-westerling-kept-barren.node.md` and `/Users/mnoth/source/asoiaf-chat/working/enrichment/wo5k-battles-pass3/nodes/jeyne-westerling-kept-barren.node.md` (both identical).

The node body says: "The **specific means** Sybell used are never stated in the published books." — this is exactly correct. No moon-tea, no fertility-potion, no mechanism is asserted. The node correctly gates on what the book says: "I made certain of that, as your lord father bid me." Node prose is clean; mechanism is NOT asserted.

**PASS.**

---

## Slug Sanity

**`battle-at-duskendale`:**  
Wiki page `Battle_at_Duskendale.json` confirms: this is the WO5K battle (299 AC) in which Lord Randyll Tarly shatters Robett Glover and Helman Tallhart near Duskendale — the correct ASOS event. The historical `defiance-of-duskendale` / `sack-of-duskendale` are distinct (involving Aerys II's capture decades earlier). Slug is correctly scoped.

**`fighting-at-the-fords-of-the-trident`:**  
Wiki page `Fighting_at_the_fords_of_the_Trident.json` confirms: this is the ASOS Roose/Gregor Ruby-Ford fight (299 AC, en route to the Twins). NOT the `battle-of-the-fords` (the ACOK Edmure/Tywin Green-Fork/Red-Fork battles in 298 AC). Slug is correctly scoped.

**BOTH PASS.**

---

## Recommendation

### KEEP (CONFIRM)
- **A1** (`tywin MANIPULATES sybell`, via_bribe, tier-1) — CONFIRM. Evidence is unambiguous; edge type and direction correct.
- **A2** (`sybell BETRAYS robb`, tier-1) — CONFIRM. Book-confirmed; correctly typed.
- **A6** (`grey-wind FORESHADOWS jeyne-westerling-kept-barren`, tier-2) — CONFIRM with note. Quote exact; wolf-warning is load-bearing in-text. Add note that the foreshadow resolves on the Spicer family (uncle Rolph → mother Sybell → betrayal), not solely the barrenness mechanism.
- **B9** (`roose SUSPECTED_OF battle-at-duskendale`, tier-2) — CONFIRM, stronger than claimed. The proposer's cited anchor is good but the stronger evidence is asos-jaime-05:129 where Roose admits he personally sent Glover to Duskendale. Consider adding cite_ref to that passage.
- **C1** (`battle-at-duskendale ENABLES red-wedding-conspiracy`, tier-2) — CONFIRM.
- **C2** (`fighting-at-the-fords-of-the-trident ENABLES red-wedding-conspiracy`, tier-2) — CONFIRM. Distinct precondition from C1; not double-counting.

### DROP
- **B10** (`roose SUSPECTED_OF fighting-at-the-fords-of-the-trident`, tier-2) — **DROP / REFUTE**. The Ruby Ford suspicion rests on structural inference only (non-Bolton rear-guard + performed self-blame). No character voices the suspicion; no "why would they go?" bafflement; Robb says "you did well." The in-text basis does not rise to SUSPECTED_OF without theory-adjacent inference. If retained at all, downgrade to a note on the B6 `roose COMMANDS_IN fighting-at-the-fords-of-the-trident` edge rather than a first-class SUSPECTED_OF edge.

### Node/slug adjustments
- `jeyne-westerling-kept-barren.node.md`: **PASS** — clean, no mechanism over-assertion.
- Slug `battle-at-duskendale`: **PASS** — correct WO5K event.
- Slug `fighting-at-the-fords-of-the-trident`: **PASS** — correct ASOS Ruby-Ford event.

### Additional note for B9 (A1 corroboration)
Edge B9's `evidence_quote` is currently anchored on Robb's "Why would they go to Duskendale?" (asos-catelyn-04:91). The stronger smoking-gun is Roose's own words: "I gave him all the Karhold men still with me and sent him off with Glover" (asos-jaime-05:129). Recommend adding a second `cite_ref` for that passage as corroborating evidence.
