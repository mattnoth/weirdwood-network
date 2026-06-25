# Jon Snow / Wall Enrichment — Fresh Verify
**Session:** S145  
**Reviewer:** independent fresh-verify subagent (no session memory)  
**Date:** 2026-06-25  
**Scope:** `verify: true` edges only — SH1, SH2, SH5, HH3, HH4, C1, C2, C3, C4, C5, G5, G6, ST1. Plus two proposed retirement adjudications.

---

## Verdict Table

| ID | Source → Target | Proposed | Verdict | Change | Reason |
|----|-----------------|----------|---------|--------|--------|
| SH1 | pink-letter-delivered → the-shieldhall-speech | ENABLES T1 | **CONFIRM** | — | Letter is unambiguous precondition. Jon reads it, deliberates ~2 hours, then calls the Shieldhall. Text: *"I think we had best change the plan"* (adwd-jon-13:267) is Jon's direct reaction to the letter before convening the assembly. ENABLES (precondition, not spark) is exactly right. |
| SH2 | the-shieldhall-speech → jon-is-stabbed-repeatedly | TRIGGERS T1 | **CONFIRM** | — | The conspirators' joint exit happens at the moment of maximum commitment — Jon has called for volunteers to march south. The stabbing follows immediately: Wick slashes at adwd-jon-13:319, Marsh stabs at :323, third blade at :325. The speech is the proximate spark. Quote *"Yarwyck and Marsh were slipping out"* (line 299) captures the pivot moment. TRIGGERS is correct. |
| SH5 | jon-allows-free-folk-through-the-wall → the-shieldhall-speech | ENABLES T2 | **CONFIRM** | — | Text at adwd-jon-13:279: *"The wildlings outnumbered the crows by five to one."* This crowd is what gives Jon's call-to-arms its roar and political weight. The decree that let the free folk through is the direct cause of that 5:1 ratio. Without it, the assembly would have been dominated by skeptical crows and the speech would have failed. ENABLES is sound: it's a precondition of the scene's success, not the spark. T2 appropriate (requires one inferential step — that crowd composition is causal). |
| HH3 | hardhome-catastrophe → jon-snow (MOTIVATES) | MOTIVATES T2 | **CONFIRM** | — | adwd-jon-12:271: *"now my war begins"* is Jon's explicit internal resolution after reading the Hardhome letter. Routes agency through Jon correctly. MOTIVATES over CAUSES is the right choice. T2 appropriate. |
| HH4 | hardhome-catastrophe → the-shieldhall-speech | ENABLES T2 | **CONFIRM** | — | adwd-jon-13:283 (Jon's opening line): *"I summoned you to make plans for the relief of Hardhome."* Hardhome is literally the stated reason Jon convenes the assembly. Without the catastrophe, no Shieldhall speech happens. ENABLES is sound. Two causes (pink-letter ENABLES + Hardhome ENABLES) converge: both are genuine independent preconditions (the letter redirected Jon away from leading the ranging himself; Hardhome was the reason he had convened at all). Neither is redundant. T2 appropriate. |
| C1 | othell-yarwyck → jon-is-stabbed-repeatedly | SUSPECTED_OF T2 | **CONFIRM** | — | adwd-jon-13:299: *"Yarwyck and Marsh were slipping out … and all their men behind them."* Four knives are described: Wick (first slash :319, second slash :321), Bowen (belly stab :323), an unnamed third blade (:325, shoulder blades), and a fourth Jon never feels (:325). Yarwyck exits with Marsh's group at the pivotal moment; the coordination of exit + timing is consistent with foreknowledge. SUSPECTED_OF (unproven agency) is the right verb — he is never shown wielding a knife. T2 appropriate. |
| C2 | left-hand-lew → jon-is-stabbed-repeatedly | SUSPECTED_OF T2 | **REJECT** | — | See analysis below. |
| C3 | alf-of-runnymudd → jon-is-stabbed-repeatedly | SUSPECTED_OF T2 | **REJECT** | — | See analysis below. |
| C4 | othell-yarwyck → bowen-marsh (CONSPIRES_WITH) | CONSPIRES_WITH T2 | **ADJUST** | Downgrade to T3 | See analysis below. |
| C5 | jon-allows-free-folk-through-the-wall → othell-yarwyck (MOTIVATES) | MOTIVATES T2 | **CONFIRM** | — | adwd-jon-13:149: *"their disapproval went bone deep"* applies to both Marsh and Yarwyck together; the following lines list specifically Yarwyck's complaints (Borroq, Stonedoor isolation). This is the documented motivational substrate for his conspiracy participation. MOTIVATES through a human (preserving agency) is correct. T2 appropriate. |
| G5 | melisandre → lord-of-bones (MANIPULATES) | MANIPULATES T2 | **CONFIRM** | Cite fix: prefer :87 over :97 | See analysis below. |
| G6 | mance-rayder-brought-to-execution → pink-letter-delivered | ENABLES T2 | **CONFIRM** | — | See analysis below. |
| ST1 | stannis-s-army-stalls-at-crofters-village → pink-letter-delivered | ENABLES T2 | **ADJUST** | Downgrade to T3 | See analysis below. |

---

## Per-Edge Analysis

### SH1 — CONFIRM
**Quote (adwd-jon-13:267):** *"I think we had best change the plan"*  
Jon says this to Tormund immediately after reading the Pink Letter, and "they talked for the best part of two hours" (line 269) before Jon calls for the Shieldhall gathering (line 113 — spoken earlier in chapter chronology; the letter scene is later). The letter is clearly the precondition that transforms a ranging into a political speech. ENABLES: precondition, not the spark. T1 is warranted (directly demonstrated by text).

---

### SH2 — CONFIRM
**Quote (adwd-jon-13:295):** *"… is there any man here who will come stand with me?"*  
**Quote (adwd-jon-13:299):** *"Yarwyck and Marsh were slipping out"*  
The speech's climax (volunteering to march south alone) is what provokes the conspiratorial exit. The stabbing follows within the same scene: Jon exits the Shieldhall, hears shouting from Hardin's Tower (line 305), sees Wun Wun, calls "No blades!" — and Wick slashes him (line 319). The speech is the proximate spark. TRIGGERS T1: confirmed.

Note: the existing edge `pink-letter-delivered TRIGGERS jon-is-stabbed-repeatedly` cited line 295 as its quote. That line IS the speech, not the letter. The new edge SH2 with the same quote is the correct attachment; the old edge is misattributed (see Retirement 1 below).

---

### SH5 — CONFIRM
**Quote (adwd-jon-13:279):** *"The wildlings outnumbered the crows by five to one"*  
This is a genuine structural precondition. The free-folk decree is what produced the wildling majority in the Shieldhall, which is what made the call-to-arms succeed with a roar rather than be shouted down. Without the majority, the speech fails and there is no muster to march south. ENABLES T2: confirmed.

Redundancy check vs HH4: HH4 ENABLES from Hardhome (reason the assembly was called at all); SH5 ENABLES from free-folk decree (what determined crowd composition and made the outcome possible). They are causally distinct — one is about calling the meeting, the other about its success. Neither is redundant.

---

### HH3 — CONFIRM
**Quote (adwd-jon-12:271):** *"now my war begins"*  
This is the final line of the Hardhome chapter, Jon's internal monologue after reading Cotter Pyke's letter. The revelations (dead things in the woods and water, wildlings eating their own dead) crystallize Jon's commitment. MOTIVATES (event→person) routes agency through Jon, preserving his choice to act. T2 appropriate (one hop of inference: that this drives the Shieldhall decision; confirmed by HH4's causal link).

---

### HH4 — CONFIRM
**Quote (adwd-jon-13:283):** *"I summoned you to make plans for the relief of Hardhome"*  
This is Jon's literal opening sentence at the Shieldhall. Hardhome is the *stated* reason for the assembly. The speech would not exist without it. ENABLES T2: the 5:1 wildling crowd is separately explained by SH5 — both edges are valid preconditions converging on the speech node.

---

### C1 — CONFIRM
The stabbing scene names four knives: Wick (attacker, confirmed at :319/:321), Bowen (attacker, confirmed at :323), and then two unnamed blades (third at :325 between shoulders; fourth Jon never feels). Yarwyck is seen exiting with Marsh's cluster at line 299. His exit is coordinated with Marsh's — the group exits together. SUSPECTED_OF (unproven agency, load-bearing) is the right framing. T2 appropriate.

---

### C2/C3 — REJECT (Left Hand Lew / Alf of Runnymudd)

**Text at adwd-jon-13:283:** *"Bowen had Wick Whittlestick, Left Hand Lew, and Alf of Runnymudd beside him."*

This is the seating arrangement at the START of the speech, before Jon reads the Pink Letter. Nothing in the subsequent text names Left Hand Lew or Alf of Runnymudd again. The named stabbers are Wick Whittlestick (two cuts, :319/:321) and Bowen Marsh (belly stab, :323). The third and fourth knives are entirely anonymous ("the third dagger," "the fourth knife" — both passive constructions with no named actor, :325).

**The only basis for C2/C3 is: these two men were seated next to Bowen at the speech.** That is faction proximity, not evidence of participation. It tells us they are Bowen's associates, which is worth zero inferential weight for SUSPECTED_OF — SUSPECTED_OF requires "unproven-but-load-bearing agency," not mere seating proximity to a conspirator. The third and fourth knives could be Yarwyck's builders, other stewards, or anyone in the conspirators' cluster. Naming these two specific individuals from a single seating mention is text-anchor failure.

**REJECT both C2 and C3.** Drop these edges entirely. If desired, a single note can be added to bowen-marsh's node prose about unnamed co-conspirators, but individual SUSPECTED_OF edges require more than seating.

---

### C4 — ADJUST: Downgrade T2 → T3 (retain CONSPIRES_WITH verb)

**Quote (adwd-jon-13:299):** *"Yarwyck and Marsh were slipping out … and all their men behind them."*  
**Prior context (asos-jon-12:53):** *"Thorne and Marsh will sway him, Yarwyck will support Lord Janos"*

The joint exit at line 299 shows Yarwyck and Marsh acting in concert at exactly the moment of the conspiracy. The ASOS precedent (Thorne/Marsh/Yarwyck bloc voting) establishes a pattern of coordinated political action. An existing `othell-yarwyck CONSPIRES_WITH bowen-marsh` edge already exists in the graph (confirmed via `graph-query --neighbors bowen-marsh`: the edge is already there from the Slynt-vote chain).

**Assessment:** CONSPIRES_WITH is not too strong — the text does show active, coordinated, simultaneous action. However, the quote ("slipping out together") shows parallel *behavior* more directly than it shows active *conspiracy* (pre-arranged plot). The distinction is subtle but real: they could be independently reaching the same conclusion at the same moment. The ASOS precedent strengthens the inference but doesn't close it. T3 (reasonable inference, not strongly supported by a single text) is more honest than T2 (strong inference).

**ADJUST: retain CONSPIRES_WITH, downgrade from T2 to T3.**

Note: since this edge already exists in the graph (from the ASOS S132-era arc), this edge from S145 is potentially **duplicate**. The curator should verify before minting — if the edge already exists, skip minting this one or merge the ADWD evidence onto the existing edge.

---

### G5 — CONFIRM (with cite correction)

**Proposed quote (adwd-melisandre-01:97):** *"the ruby seemed to pulse"*  
**Stronger quote (adwd-melisandre-01:87):** *"Melisandre felt the warmth in the hollow of her throat as her ruby stirred at the closeness of its slave."*

Line 87 is superior evidence: it explicitly calls Rattleshirt/Lord of Bones a "slave" and describes the ruby's physical response to his presence. This is the clearest textual basis for MANIPULATES (coercive control via the ruby fetter). Line 97 ("the ruby seemed to pulse") is also valid but less explicit.

MANIPULATES T2 is correct. The ruby fetter is a control mechanism distinct from the glamour-casting (which is G3). Two separate mechanisms, two separate edges. Confirmed.

**Recommend:** update cite_ref to :87 and use the slave quote as evidence_quote for sharper text-anchor.

---

### G6 — CONFIRM

**Quote (adwd-jon-13:231):** *"you sent him to Winterfell to steal my bride"*  
**Structural chain:** mance-rayder-brought-to-execution (event) → glamour allows Mance to survive → Mance goes to Winterfell → Pink Letter taunts about the spearwife mission

This is a multi-hop chain, but ENABLES handles multi-hop preconditions and the chain is sound: if Rattleshirt had not been glamoured to appear as Mance, Mance would have burned (no survival → no Winterfell mission → no Pink Letter content about the mission). The Pink Letter's specific taunts about Mance's mission are what make it a credible threat, not just a boast.

**Is ENABLES right or too distal?** The chain has 3 logical hops (execution-faked → survival → Winterfell mission → letter). Normally 3 hops is over-distal. However, the "execution" event node already represents the *entire glamour-substitution scheme*, not just the burning moment. Given that, the event node ENABLES → letter is really 2 hops (survival enables mission; mission enables letter content), which is within ENABLES range. The pink letter explicitly references Mance's mission as its taunt — the causal link is stated in the source text.

**CONFIRM ENABLES T2.** The hop count is acceptable given the event node's scope.

Not wired through any unwritten battle node. Confirmed clean.

---

### ST1 — ADJUST: Downgrade T2 → T3

**Quote (adwd-jon-13:229):** *"smashed in seven days of battle"*  

The Pink Letter's text claims Stannis was smashed in seven days. At the time of the ADWD narrative, Stannis's army is *stalled* at the crofters' village (confirmed by existing graph: incoming VICTIM_IN from stannis-baratheon with quote "sat snowbound and unmoving, walled in by ice and snow, starving"). The "seven days of battle" claim is **Ramsay's claim in the letter** — it is not confirmed by any chapter text. GRRM left Stannis's fate ambiguous through the end of ADWD.

**ST1 proposes:** the stall ENABLES the letter (the stall is what makes Ramsay's claim *plausible*, therefore enables him to write it).

**Assessment:** This is an interpretive inference about Ramsay's psychology (he can only credibly claim victory because Stannis stalled). The quote cited ("smashed in seven days of battle") is from Ramsay's letter, not a text confirming the stall-to-letter causal connection. The causal logic is: *stall → Bolton victory possible → Ramsay writes taunting letter*. This is reasonable — Ramsay had to have won (or thought he won) to write the letter, and the stall was the precondition for the Bolton army to engage — but it requires accepting that the battle in the Pink Letter happened, which is precisely what is disputed in-universe.

**RED LINE CHECK:** The edge does not wire through an unwritten battle node. The stall node → letter node skips the battle itself, which is correct and clean per the instruction. The inference that the stall ENABLES the letter is logically valid even without knowing who won the battle — Ramsay wrote the letter, and he could only have done so if Stannis was defeated (or seemed so), which the stall made possible.

**However,** the evidence is thin for T2: the stall-to-letter causal chain requires believing (1) the battle happened and (2) Bolton won. Neither is directly confirmed in adwd-jon-13. T3 (reasonable inference, somewhat speculative) is more honest.

**ADJUST: retain ENABLES, downgrade T2 → T3.**

---

## Retirement Adjudications

### Retirement 1: `pink-letter-delivered TRIGGERS jon-is-stabbed-repeatedly`

**Rationale for retirement:** The proposed quote ("is there any man here who will come stand with me?", adwd-jon-13:295) is from the Shieldhall speech, not from the letter. The edge's text-anchor is misattributed — that line is the speech's climax, which is now correctly captured by SH2 (the-shieldhall-speech TRIGGERS jon-is-stabbed-repeatedly).

**Verification:** Reading adwd-jon-13:295: *"The Night's Watch will make for Hardhome. I ride to Winterfell alone, unless … is there any man here who will come stand with me?"* — confirmed, this is the speech, not the letter.

The letter is a genuine precondition (SH1: ENABLES the speech) but is not the proximate cause of the stabbing. The stabbing is triggered by what happens *during and after* the speech (the conspirators' exit, the Wun Wun incident, Jon emerging from the Shieldhall).

**VERDICT: RETIRE.** The edge is both text-anchor-wrong (wrong quote, wrong event attributed as cause) and superseded by the new SH1 + SH2 chain, which more accurately captures the causal flow: letter ENABLES speech TRIGGERS stabbing. Retiring the pink-letter → stabbing direct edge removes a false shortcut that skips the actual mechanism.

---

### Retirement 2: `mance-rayder VICTIM_IN mance-rayder-brought-to-execution`

**Rationale for retirement:** The event should have Rattleshirt (lord-of-bones) as VICTIM_IN, not Mance Rayder, because Mance survived via the glamour substitution.

**Verification (adwd-melisandre-01:259):** *"She burned the Lord of Bones."*  
And earlier at :253–255:  
> "Jon Snow's grey eyes grew wider. 'Mance?'"  
> "'Lord Snow.' Mance Rayder did not smile."  
> "'She burned you.'"  
> "'She burned the Lord of Bones.'"  

This is unambiguous: Mance is alive. The man burned was Rattleshirt (Lord of Bones), glamoured to appear as Mance. The existing `mance-rayder VICTIM_IN mance-rayder-brought-to-execution` edge is factually false in light of this reveal.

**VERDICT: RETIRE.** The edge is factually wrong post-reveal. The new G4 edge (`lord-of-bones VICTIM_IN mance-rayder-brought-to-execution`) correctly replaces it with text anchor adwd-melisandre-01:259. The original evidence (adwd-jon-03 dragging scene) accurately described what *appeared* to happen; now that the glamour reveal is in the graph, the node's VICTIM_IN must be corrected to reflect the actual victim.

Note: the existing T1 edge from adwd-jon-03 ("Bound with rope and noose, dragged by Ser Godry Farring's horse to the fire pit") described the glamoured Rattleshirt correctly appearing as Mance from Jon's POV. The node-level truth (who actually burned) is what matters for graph traversal. Retire the Mance edge; keep the lord-of-bones edge at T1.

---

## Systematic Concerns

1. **C4 duplicate risk:** The `othell-yarwyck CONSPIRES_WITH bowen-marsh` edge appears to already exist in the graph (from the ASOS Slynt-vote arc, confirmed via graph-query). Before minting C4, check `edges.jsonl` for a duplicate. If the edge exists, add the ADWD evidence as a supplemental cite_ref on the existing edge rather than minting a second edge.

2. **G5 cite quality:** Line 87 ("ruby stirred at the closeness of its slave") is stronger evidence for MANIPULATES than line 97 ("ruby seemed to pulse"). The relationship is the same but line 87 makes the coercive/control aspect explicit. Recommend updating the evidence_ref and evidence_quote before minting.

3. **C2/C3 pattern (seating = participation):** This is a systematic bias risk. Seating proximity to a conspirator does not constitute SUSPECTED_OF. Future enrichment passes should be checked for this pattern — only named actors in the stabbing scene itself (Wick Whittlestick, Bowen Marsh, the two anonymous third/fourth knives) should carry SUSPECTED_OF. Left Hand Lew and Alf of Runnymudd are attendees of the Shieldhall, not identified stabbers.

4. **ST1 tier:** The Pink Letter's reliability is itself questioned in-universe ("Might be all a skin o' lies" — Tormund, line 259). Wiring the stall-node causally to the letter at T2 implies more certainty than the text supports. T3 is safer.

5. **No agency-collapse found:** All event→event edges in the verify set correctly use ENABLES rather than CAUSES, and all person-directed causation uses MOTIVATES. The causal chain is properly structured.
