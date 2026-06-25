# AEGON Enrichment Pass 1 — Fresh-Verify Report
> Reviewer: independent fresh-verify agent (did NOT propose these edges)
> Date: 2026-06-25
> Candidates file: `working/enrichment/aegon/candidates.json` (37 edges, 3 new nodes)
> Chapters read in full: adwd-the-lost-lord-01, adwd-the-griffin-reborn-01, adwd-epilogue, adwd-tyrion-04, adwd-tyrion-05, adwd-tyrion-06

---

## Verdict Table

| id | edge | verdict | reasoning / exact change if ADJUST |
|----|------|---------|--------------------------------------|
| G1 | jon-connington AFFLICTED_BY greyscale | **CONFIRM** | Line 237 exact: "The nail on his middle finger had turned as black as jet." Discovery scene confirmed on-page. First-use of AFFLICTED_BY noted; no concern. |
| G2 | greyscale MOTIVATES jon-connington | **ADJUST** | See detailed analysis below. Keep, but adjust tier and note. |
| V2 | varys DECEIVES golden-company | **ADJUST** | See below. Quote at line 89 is Connington recounting Varys's words, not Varys acting in this chapter. Target and quote are correct but the edge note overstates: Varys planted the story *before* this chapter; JonCon merely reflects on it here. The edge is still defensible (the deception is ongoing and acknowledged), but tier should be 2, not 1 — the evidence is reported speech, not witnessed action. Change: `"tier": 1 → "tier": 2`. |
| V5 | varys REVEALS_TO kevan-lannister | **CONFIRM** | Line 297 exact: "Aegon has been shaped for rule since before he could walk." The terminal reveal of Aegon's SURVIVAL (not identity) to dying Kevan. Theory-gate clean — Varys never asserts Aegon IS Rhaegar's son as fact; he says "he is here," which is the claimant's SURVIVAL. CONFIRM. |
| JC1 | jon-connington DECEIVES golden-company | **CONFIRM** | Line 89: "Even the men who'd ridden with him might not recognize the exile lord Jon Connington… Connington had drunk himself to death in Lys after being driven from the company in disgrace for stealing from the war chest." On-page. Connington's POV confirms he is actively maintaining this cover. CONFIRM. |
| R1 | jon-connington AGENT_IN aegon-revealed-to-the-golden-company | **CONFIRM** | Line 127: "My lords, I give you Aegon Targaryen, firstborn son of Rhaegar." JonCon performs the reveal explicitly. CONFIRM. |
| R2 | aegon-targaryen-young-griff PARTICIPATES_IN aegon-revealed-to-the-golden-company | **CONFIRM** | Line 175: "Then put your hopes on me." Aegon speaks and is the subject of the reveal. CONFIRM. |
| R3 | harry-strickland PARTICIPATES_IN aegon-revealed-to-the-golden-company | **CONFIRM** | Line 223: "The last to do so was Homeless Harry Strickland, blistered feet and all." He presides as captain-general and lays his sword last. CONFIRM. |
| R4 | tristan-rivers PARTICIPATES_IN aegon-revealed-to-the-golden-company | **CONFIRM** | Line 215: "Prince Aegon, we are your men." Asks the deciding sail-west question directly. CONFIRM. |
| R5 | laswell-peake PARTICIPATES_IN aegon-revealed-to-the-golden-company | **CONFIRM** | Line 213: "some of us still have friends in the Reach." Speaks in favor of sailing west at the war council. CONFIRM. |
| R6 | lysono-maar PARTICIPATES_IN aegon-revealed-to-the-golden-company | **CONFIRM** | Line 147: "the Targaryen girl has not started for the west." Opens the intelligence briefing. His role is confirmed. CONFIRM. |
| D1 | harry-strickland OPPOSES golden-company-sails-for-westeros | **CONFIRM** | Line 165: "One broken contract is stain enough upon the honor of the company." He also resists the sail-west proposal throughout (lines 183, 191, 200–205). CONFIRM. |
| D2 | golden-company NEGOTIATES_WITH yunkai | **ADJUST** | See detailed analysis below. |
| T1 | jon-connington COMMANDS_IN taking-of-griffins-roost | **CONFIRM** | Line 31: "And quick as that, Griffin's Roost was his again." JonCon leads the assault and rides up the throat personally (line 29: "Griff rode up the throat on a white courser"). CONFIRM. |
| T2 | franklyn-flowers COMMANDS_IN taking-of-griffins-roost | **CONFIRM** | Line 25: "Franklyn Flowers was able to use the brush for concealment and lead his men within twenty yards of the gates." Ground assault commander confirmed. CONFIRM. |
| T3 | tristan-rivers COMMANDS_IN taking-of-crows-nest | **CONFIRM** | Line 93: "Ser Tristan Rivers had set off simultaneously for the seat of House Morrigen at Crow's Nest." Direct textual confirmation. CONFIRM. |
| T4 | laswell-peake COMMANDS_IN taking-of-rain-house | **CONFIRM** | Line 93: "Laswell Peake for Rain House, the stronghold of the Wyldes." Direct textual confirmation. CONFIRM. |
| T5 | marq-mandrake COMMANDS_IN taking-of-greenstone | **CONFIRM** | Line 143: "Word's reached the camp from Marq Mandrake. The Volantenes put him ashore on what turned out to be Estermont… He's taken Greenstone." CONFIRM. Note: the text is "He's taken Greenstone" — the node correctly names Greenstone. Mandrake ended up on Estermont island rather than his original objective, but he commands the Greenstone taking. |
| T6 | gorys-edoryen COMMANDS_IN landing-of-the-golden-company | **CONFIRM** | Line 93: "under the command of the company's Volantene paymaster, Gorys Edoryen." Explicitly commands the rear guard and landing camp. CONFIRM. |
| T7 | black-balaq COMMANDS_IN landing-of-the-golden-company | **ADJUST** | Line 13: "Black Balaq commanded one thousand bows." This establishes command of the archers, not the landing itself. Balaq's role is as the archer-commander deployed from the landing point outward — he commands his own force, not the landing hub that Edoryen commands. The cite is the opening line of the griffin-reborn chapter, before the taking of Griffin's Roost, so "one thousand bows" = the overall archer command for the whole operation. The proposed hub is `landing-of-the-golden-company`. ADJUST: change note to clarify Balaq commands the archer contingent deployed from the landing; this is still a valid COMMANDS_IN because his archers are the operationally central force that enables all the simultaneous takings. Keep the edge. Alternatively, COMMANDS_IN could be changed to a lighter type — but the chapter opens by naming him as the commander of a distinct force unit within the operation, which COMMANDS_IN captures correctly. **Keep, no type change. Note fix only.** |
| S1 | aegon-targaryen-young-griff COMMANDS_IN siege-of-storms-end-300 | **CONFIRM** | Line 201: "I mean to lead it." Aegon insists on personally leading the Storm's End assault over JonCon's objection. The siege is planned, not yet executed at chapter end, but Aegon's command decision is unambiguous and on-page. CONFIRM. |
| H1 | yandry TRAVELS_WITH aegon-targaryen-young-griff | **CONFIRM** | Line 55 (tyrion-04): "a pair of Dornish orphans come home to Mother Rhoyne." Yandry poles the boat containing Aegon throughout the Rhoyne journey. On-page throughout tyrion-04/05/06. CONFIRM. |
| H2 | ysilla TRAVELS_WITH aegon-targaryen-young-griff | **CONFIRM** | Line 13 (tyrion-05): "Ysilla had the tiller." She steers, cooks, and is present throughout. CONFIRM. |
| H3 | haldon TRAVELS_WITH aegon-targaryen-young-griff | **CONFIRM** | Line 145 (tyrion-04): "Haldon corrected their mistakes." He tutors Aegon aboard the Shy Maid throughout. CONFIRM. |
| H4 | lemore TRAVELS_WITH aegon-targaryen-young-griff | **CONFIRM** | Line 119 (tyrion-04): "Young Griff went off with Septa Lemore to be instructed in the mysteries of the Faith." She is his companion, guardian, and Faith tutor throughout. CONFIRM. |
| H5 | rolly-duckfield TRAVELS_WITH aegon-targaryen-young-griff | **CONFIRM** | Line 91 (tyrion-04): "Time to raise some bruises. Swords today, I think." Duck spars with Aegon daily aboard the Shy Maid. His presence throughout is confirmed. CONFIRM. |
| H6 | rolly-duckfield PROTECTS aegon-targaryen-young-griff | **CONFIRM** | Line 187 (griffin-reborn): "Before them went Ser Rolly Duckfield, a snow-white cloak streaming from his shoulders." He has been named to the Kingsguard and rides as Aegon's sworn protector. CONFIRM. |
| H7 | rolly-duckfield TEACHES aegon-targaryen-young-griff | **CONFIRM** | Line 97 (tyrion-04): "Ser Rolly's greater size and strength would quickly overwhelm his charge." Duck trains Aegon at arms daily. CONFIRM. Note: "teaches" captures arms training as distinct from Haldon's intellectual tutelage and Lemore's Faith instruction — appropriate specialization. |
| O1 | illyrio-mopatis GIFTED_TO aegon-targaryen-young-griff | **CONFIRM** | Line 61 (lost-lord): "three huge square-cut rubies on a chain of black iron, a gift from Magister Illyrio." CONFIRM. The convention GIFTED_TO (giver→recipient) is correctly applied: illyrio→aegon. |
| O2 | aegon-targaryen-young-griff OWNS illyrios-ruby-chain | **CONFIRM** | Line 61 (lost-lord): "At his throat he wore three huge square-cut rubies on a chain of black iron." Aegon wears/possesses the chain. CONFIRM. |
| O3 | yandry CAPTAIN_OF shy-maid | **CONFIRM** | Line 83 (tyrion-04): "Yandry took them out into the center of the river." Plus line 55: he and Ysilla are "Dornish orphans come home to Mother Rhoyne" who own the boat. He pilots and poles. CONFIRM. Note: the cite should arguably also ref Yandry "pull[ing] up the anchor" (line 65) as owner/operator action, but line 83 is sufficient. |
| O4 | ysilla CREW_OF shy-maid | **CONFIRM** | Line 13 (tyrion-05): "Ysilla had the tiller." She steers, cooks, and is integral to day-to-day boat operation. CONFIRM. |
| O5 | varys WIELDS varys-crossbow | **CONFIRM** | Line 277 (epilogue): "clutching a crossbow in soft powdered hands." Exact quote confirmed. CONFIRM. |
| O6 | varys-crossbow WIELDED_IN assassinations-of-pycelle-and-kevan-lannister | **CONFIRM** | Line 277 (epilogue): same passage — Varys appears holding the crossbow in Pycelle's chambers immediately after Kevan is shot with a quarrel. CONFIRM. |
| O7 | varys-crossbow PARALLELS tywins-crossbow | **CONFIRM** | See detailed analysis below. |
| K1 | assassinations-of-pycelle-and-kevan-lannister PREVENTS kevan-reconciles-the-realm | **See kevan-reconciles-the-realm section below.** | |
| K2 | kevan-lannister AGENT_IN kevan-reconciles-the-realm | **See kevan-reconciles-the-realm section below.** | |

---

## Detailed Analysis: High-Scrutiny Edges

### G2 — `greyscale MOTIVATES jon-connington` (tier 2)

**Text check:**
- Line 21 (lost-lord): "I do not have time enough for caution." — JonCon's words to Lemore before the reveal. This is BEFORE he discovers his greyscale in this chapter.
- Line 237-239 (lost-lord): The greyscale discovery comes in the final paragraphs after the reveal and sail-west decision. "Death, he knew, but slow. I still have time."

**Key finding:** The phrase "I still have time" (line 239) is JonCon reflecting on the death-clock in relation to all his goals — reclaiming Griffin's Roost, putting Rhaegar's son on the Iron Throne. Line 131 (griffin-reborn) confirms the ongoing motivation: "I should hack them off… He dare not let the greyscale become known." Throughout griffin-reborn he privately measures time against the disease.

**Verdict: CONFIRM with one adjustment.** The phrase "I do not have time enough for caution" (line 21) is cited in the note but NOT cited in the edge data — the edge cites line 239 ("Death, he knew, but slow. I still have time."). This is correct: line 239 is the discovery moment from which motivation flows. The concept→person MOTIVATES model is defensible here: the precedent is `maggy-the-frogs-prophecy MOTIVATES cersei`, and greyscale operates similarly as a death-clock that shapes JonCon's urgency throughout the arc. Unlike a prophecy, greyscale is a physical disease, but it functions identically as a time-limiting motivator for decisions (haste over caution at line 21; the Storm's End decision at griffin-reborn). The tier-2 rating is appropriate (Connington does not say "because of greyscale I am doing this" — it is inferred from context, not stated). 

**Final verdict: CONFIRM as written.** The quote and line are correct. The note's cross-reference to line 21 is editorial context, not the cite — that's fine.

---

### D2 — `golden-company NEGOTIATES_WITH yunkai` (tier 2)

**Text check:**
- Line 135 (lost-lord): "The Yunkishmen… offers twice what Myr was paying us, plus a slave for every man in the company, ten for every officer, and a hundred choice maidens all for me."
- Line 141: "You refused him," said Griff. — "I told him I would think on his proposal." Harry Strickland's response.
- Line 143: "A blunt refusal would have been unwise."

**Assessment:** The Yunkai envoy made an offer. Strickland did NOT accept, did NOT refuse — he said "I would think on his proposal." This is exactly the definition of an open negotiation: an offer was extended and received, the recipient engaged non-committally. NEGOTIATES_WITH is the right edge type for "engaged but never concluded." The concern would be if the offer was flatly refused — it was not. Strickland explicitly kept the door open for strategic reasons.

**Verdict: CONFIRM.** The engagement is real (offer received, deliberated over in the war council, used as context for Aegon's override). NEGOTIATES_WITH correctly captures an engagement that did not conclude. The edge is not overstated.

---

### O7 — `varys-crossbow PARALLELS tywins-crossbow` (tier 2)

**Text check:**
- Line 293 (epilogue): "I thought the crossbow fitting. You shared so much with Lord Tywin, why not that?"

**Assessment:** Varys explicitly names the echo on-page. He calls the crossbow "fitting" and invokes the shared-with-Tywin parallel directly. Both Tywin and Kevan are Lannister patriarchs, both killed by crossbow by intimates (Tyrion / Varys). The literary parallel is not inferred — it is stated by a character on the page. PARALLELS is in the locked vocab. Tier 2 is correct (literary parallel rather than causal or factual claim). This is not over-reach; it is the clearest case of an on-page-named parallel in the entire arc.

**Verdict: CONFIRM.**

---

### V2 / V5 / JC1 — DECEIVES / REVEALS_TO redundancy check + theory gate

**Theory gate check:**
- V5 (`varys REVEALS_TO kevan-lannister`): The quote is "Aegon has been shaped for rule since before he could walk." Varys speaks of Aegon's preparation for rule and asserts "He is here" (line 295: "No"). He says Aegon "has been shaped for rule" — this is a statement about the CLAIMANT's training, not an assertion that he IS Rhaegar's biological son. Theory-gate: CLEAN. Varys never says "this is really Rhaegar's son" — he says the boy exists and has been prepared. The on-page content of the reveal is about survival and preparation, not identity verification.

**Redundancy check V2 / JC1:**
- V2 (`varys DECEIVES golden-company`): Varys deceived the GC by planting the thief/drunk story about Connington.
- JC1 (`jon-connington DECEIVES golden-company`): Connington enacts the cover — presents as "Griff."
These are distinct: different actors, different mechanisms, different objects of deception (the GC believes Connington is dead/disgraced AND believes Griff is just a sellsword). Both edges are warranted. No redundancy.

**V2 tier downgrade:** The quote "We want no songs about the gallant exile" (line 89) is JonCon recalling what Varys said to him in the past. It is reported speech, not a scene with Varys present. The deception was enacted before this chapter. Tier 1 ("directly verified canon") is too strong — this is mediated through JonCon's memory. **ADJUST: V2 tier 1 → tier 2.**

**JC1 tier:** Line 89: "Even the men who'd ridden with him might not recognize the exile lord Jon Connington…" This is JonCon's own POV observing that his deception is actively working. The cover is maintained in the present tense of this chapter. Tier 1 is defensible for JC1 (the deception is ON-PAGE active, not reported speech). **CONFIRM JC1 tier 1.**

---

### T1-T7 / S1 — Simultaneous Columns Check

**Causal chain check:** The baseline warns to verify that no CAUSES-chain runs between the simultaneous takings. All 7 T-edges are COMMANDS_IN to separate taking-event targets (taking-of-griffins-roost, taking-of-crows-nest, taking-of-rain-house, taking-of-greenstone, landing-of-the-golden-company). None of these edges imply one taking CAUSED another — they are all PART_OF the landing and all happened simultaneously (confirmed line 93: "Ser Tristan Rivers had set off simultaneously"). No agency-collapse, no spurious causal chain minted. CONFIRM structure.

**Commander assignments verified:**
- JonCon + Flowers → Griffin's Roost ✓ (T1 + T2)
- Rivers → Crow's Nest ✓ (T3, line 93)
- Peake → Rain House ✓ (T4, line 93)
- Mandrake → Greenstone ✓ (T5, line 143 — note: accidental landing on Estermont island, but he commanded the Greenstone taking)
- Edoryen → landing (rear guard) ✓ (T6, line 93)
- Balaq → archer command (T7, line 13) — deployed from landing, commands all archers. Valid COMMANDS_IN to landing hub.
- Aegon → Storm's End siege (S1) ✓ (line 201: "I mean to lead it")

All confirmed against text.

---

### H1-H7 — Household Edges

All five TRAVELS_WITH edges (H1-H5) are confirmed against text. Duck, Lemore, Haldon, Yandry, Ysilla are all documented as present on the Shy Maid throughout the Rhoyne journey with Aegon. The H6 PROTECTS (Duck's Kingsguard white cloak, griffin-reborn line 187) and H7 TEACHES (sword practice, tyrion-04 line 97) are both confirmed. No over-claims detected. No redundancy concern — TEACHES ≠ TRAVELS_WITH; both are warranted.

One note on H3 (haldon TRAVELS_WITH): the edge note says "already TUTORS; this is the journey co-presence." This is correct framing. TUTORS and TRAVELS_WITH are distinct edge types — keeping both is appropriate.

---

## The `kevan-reconciles-the-realm` Node: KEEP or DROP?

### Text check
Line 285 (epilogue): "you were threatening to undo all the queen's good work, to reconcile Highgarden and Casterly Rock, bind the Faith to your little king, unite the Seven Kingdoms under Tommen's rule."

This is Varys's direct on-page statement of what Kevan was doing and why the assassination was necessary to prevent it.

### Is this over-reach?

**Arguments for DROP (as warned in candidates.json):**
1. The node was minted *solely* to resolve a 0-outgoing dead-end on `assassinations`. That is a graph-plumbing motivation, not a story-substance motivation.
2. "Kevan reconciles the realm" is not an event that HAPPENED — it is an event that was PREVENTED. The node represents a counterfactual future state.
3. The AEGON decomposition explicitly flagged "do NOT re-model KL politics." Minting an event-node for a projected Kevan regency project is modeling KL politics.
4. The existing `assassinations MOTIVATES landing` (in the spine) already captures the directional logic: Varys kills Kevan/Pycelle to create chaos → chaos opens space for Aegon. Adding a counterfactual `kevan-reconciles-the-realm` node as an intermediary doesn't add navigable evidence — it adds a phantom event.

**Arguments for KEEP:**
1. The text is unambiguous — Varys specifically articulates what Kevan was doing (reconciling Highgarden and CR, binding the Faith, uniting under Tommen). This is an on-page characterization of an ongoing political project.
2. PREVENTS is in the locked vocab. `assassinations PREVENTS kevan-reconciles-the-realm` is the most direct reading of Varys's stated motive.
3. A prevented-event node is distinguishable from a counterfactual: Kevan's reconciliation project was REAL AND ONGOING (he held a small council meeting in the epilogue's opening pages focused on exactly this — managing Tyrell tensions, deciding on Dorne, Cersei's trial). The assassination interrupted a real in-progress effort, not a hypothetical.

**Decision: REJECT the node and K1/K2, with a narrower substitute.**

The stronger argument is DROP. The graph already encodes the necessary logic:
- `landing-of-the-golden-company MOTIVATES assassinations-of-pycelle-and-kevan-lannister` (Varys kills to keep KL destabilized for Aegon's benefit)
- This MOTIVATES edge already points from the landing to the assassinations, capturing Varys's motive.

The `kevan-reconciles-the-realm` node is a phantom event node that exists purely to give the assassinations hub an outgoing edge. It re-models KL politics (the AEGON decomposition's explicit warning). The counterfactual structure (what WOULD have happened without the assassination) is not what the graph models — we model what DID happen.

**Better substitute (if the 0-outgoing dead-end matters):** Add `assassinations-of-pycelle-and-kevan-lannister ENABLES chaos-in-kings-landing` or wire `ENABLES` to an existing `wo5k` event that captures KL destabilization. Alternatively, accept the 0-outgoing on assassinations as a terminus — it's the end of the ADWD timeline, and the downstream effects (Cersei's resurgence, Dany convergence) are TWOW-gated.

**Verdict: REJECT `kevan-reconciles-the-realm` node and both K1 / K2 edges.**
- Rationale: phantom counterfactual event node; graph-plumbing motivation; re-models KL politics (explicitly warned against); 0-outgoing dead-end is acceptable for a chapter-terminal event; existing spine edges already encode Varys's motive logic.
- If the outgoing dead-end proves to be a real query problem later, revisit with a clean `ENABLES` edge to an existing node (not a new phantom event).

---

## Proposed Addition: `tyrion-lannister MANIPULATES aegon-targaryen-young-griff`

**Edge:** tyrion-lannister MANIPULATES aegon-targaryen-young-griff | tier 2 | qualifier `via_false_information` | adwd-tyrion-06

**Text verification:**

The cyvasse-goad scene in adwd-tyrion-06 in full:

Line 147: Tyrion's argument culminates: "You do not need to win. All you need to do is raise your banners, rally your supporters, and hold, until Daenerys arrives to join her strength to yours."

Lines 148-155 (the clincher):
> "But," Prince Aegon said, "without Daenerys and her dragons, how could we hope to win?"
> "You do not need to win," Tyrion told him...
> "I told you, I know our little queen. Let her hear that her brother Rhaegar's murdered son is still alive..."
> Smiling, he seized his dragon, flew it across the board. "I hope Your Grace will pardon me. Your king is trapped. Death in four."
> The prince stared at the playing board. "My dragon—"
> "—is too far away to save you. You should have moved her to the center of the battle."
> "But you said—"
> **"I lied. Trust no one. And keep your dragon close."**

Line 155: "I lied." — Tyrion explicitly admits he lied.

**What exactly did Tyrion lie about?** He said earlier (line 103): "I would not do that if I were you. It is a mistake to bring your dragon out too soon." Then after Aegon followed this advice (keeping the dragon back), Tyrion moved HIS dragon to win. The admission "I lied" refers to the cyvasse advice — but the admission doubles as meta-commentary on the ENTIRE argument Tyrion made for sailing west.

**Was Aegon manipulated?** Yes — Aegon was already persuaded to sail west by Tyrion's argument (lines 133-147), then kicked over the board in fury but acted on the advice. The narrative confirms Aegon takes up the cause in griffin-reborn. Tyrion also says explicitly: "Trust no one. And keep your dragon close" — framing himself as someone who uses false information.

**Does MANIPULATES + `via_false_information` fit the vocab?** MANIPULATES is in the locked vocab. The qualifier `via_false_information` maps cleanly to "I lied." The edge captures: Tyrion uses deliberately constructed false/strategic information (both the sail-west argument AND the cyvasse advice) to move Aegon to act in a way that serves Tyrion's (uncertain) purposes.

**Agency-collapse check:** Is Aegon's free choice still the proximate cause? YES — Aegon chooses to follow Tyrion's advice. MANIPULATES is the correct type precisely because the target acts on false/strategic information unknowingly. Aegon does not know Tyrion is deceiving him; the "I lied" reveal comes after the decision is already made. No agency-collapse concern.

**Theory-gate check:** This edge is about HOW Tyrion moves Aegon (via a cyvasse game using false information), not about Aegon's identity. The target is `aegon-targaryen-young-griff` (the claimant). Theory-gate: CLEAN.

**Quote (exact, for the edge):**
> "But you said—" / "I lied. Trust no one. And keep your dragon close." — adwd-tyrion-06, line 155

**Verdict: CONFIRM the proposed addition.**
- MANIPULATES is right (Aegon acts on false information without knowing it)
- `via_false_information` is the right qualifier
- Tier 2 is correct (Tyrion admits the lie but the causal chain from lie → decision is inferred)
- The existing `tyrion-lannister MOTIVATES golden-company-sails-for-westeros` is event-level; this proposed edge is person-to-person (HOW Tyrion moved Aegon, not the event-level outcome). They are complementary, not redundant.
- Recommend the note clarify that "I lied" refers explicitly to the cyvasse advice but also frames the entire sail-west persuasion as strategic manipulation.

---

## Theory-Gate Compliance Statement

**CLEAN.** Reviewed all 37 minted edges + the 3 nodes:

1. No edge asserts `aegon-targaryen-young-griff` IS the son of Rhaegar as a verified fact. The R1 reveal quote ("My lords, I give you Aegon Targaryen, firstborn son of Rhaegar") is Connington's in-universe claim — it is correctly attached as a REVEALS/AGENT_IN edge, not a graph-level identity assertion.
2. No edge targets `aegon-targaryen-son-of-rhaegar` (the murdered infant). All edges correctly target `aegon-targaryen-young-griff` (the claimant).
3. V5 (`varys REVEALS_TO kevan`) is about Aegon's SURVIVAL and preparation, not identity verification. Varys says "He is here" and describes his training — not "he is truly Rhaegar's son."
4. The fAegon babe-swap (Tyrion's dialogue in tyrion-06, lines 112-115: "some tanner's son from Pisswater Bend… Varys gave the Pisswater boy to my lady mother and carried me away") is present in the chapter but correctly dropped at synthesis (it is a claim within Aegon's own speech, not verifiable and identity-gated). No leak.
5. R+L, Azor Ahai, Euron↔Bloodraven: not touched.

---

## Line/Quote Drift Notes

- **V2 (line 89):** Quote verified exactly: "We want no songs about the gallant exile" — confirmed in adwd-the-lost-lord-01 line 89. EXACT MATCH.
- **G2 (line 239):** Quote "Death, he knew, but slow. I still have time." — confirmed in adwd-the-lost-lord-01 line 239. EXACT MATCH.
- **S1 (line 201):** Quote "I mean to lead it" — confirmed in adwd-the-griffin-reborn-01 line 201. EXACT MATCH.
- **O7 (line 293):** Quote "I thought the crossbow fitting. You shared so much with Lord Tywin, why not that?" — confirmed in adwd-epilogue line 293. EXACT MATCH.
- **K1/K2 (line 285):** Quote "to reconcile Highgarden and Casterly Rock, bind the Faith to your little king" — confirmed in adwd-epilogue line 285. EXACT MATCH. (Quoted correctly even though the node is rejected.)
- **T5 (line 143):** Quote "He's taken Greenstone" — confirmed. The candidates.json says line 143 of griffin-reborn, and the actual text at that line is the war-council report of Mandrake's accidental Estermont landing and Greenstone taking. EXACT MATCH.
- **H7 (line 97):** Quote "Ser Rolly's greater size and strength would quickly overwhelm his charge" — confirmed in tyrion-04. The full context makes clear this is sword-training, not actual combat. EXACT MATCH.

No quote drift or fabricated lines detected across all 37 edges.

---

## Summary

**37 edges reviewed. 3 new nodes reviewed.**

| | Count |
|---|---|
| CONFIRM | 30 |
| ADJUST | 3 (V2 tier 1→2; T7 note fix; G2 confirmed as-written after scrutiny) |
| REJECT | 2 (K1 + K2) |
| Node: KEEP | 2 (illyrios-ruby-chain, varys-crossbow) |
| Node: REJECT | 1 (kevan-reconciles-the-realm) |
| Proposed addition: CONFIRM | 1 (tyrion MANIPULATES aegon, via_false_information) |

**ADJUST edges:**
- **V2** (`varys DECEIVES golden-company`): Change tier 1 → tier 2. The evidence is JonCon's reported memory of Varys's words, not a directly-witnessed scene with Varys. The deception is real and ongoing but the cite is mediated.
- **T7** (`black-balaq COMMANDS_IN landing-of-the-golden-company`): Note fix only — clarify that Balaq commands the archer contingent (not the landing hub itself). No type or tier change.

**REJECT:**
- **K1** (`assassinations PREVENTS kevan-reconciles-the-realm`): Phantom counterfactual event target.
- **K2** (`kevan-lannister AGENT_IN kevan-reconciles-the-realm`): Same — depends on the rejected node.
- **`kevan-reconciles-the-realm` node**: Phantom event minted for graph-plumbing, not story-substance. Re-models KL politics (warned against in decomposition). Accept assassinations as a terminus.

**Zero theory-gate violations found.**
**Zero fabricated quotes found.**
