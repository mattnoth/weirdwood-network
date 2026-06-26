# Fresh-Verify: Arya / Braavos — House of Black and White arc
**Reviewer:** independent fresh-verify pass (S150 enrichment dip)
**Date:** 2026-06-26
**Chapters read:** asos-arya-13, affc-arya-01, affc-arya-02, affc-cat-of-the-canals-01, adwd-the-blind-girl-01, adwd-the-ugly-little-girl-01
**Scope:** 11 edge IDs specifically flagged for interpretive review + 1 retirement candidate; spot-check of plain role/quote edges noted inline.

---

## Verdicts on flagged edges

### SP3 — `arya-becomes-cat-of-the-canals ENABLES killing-of-dareon`
**CONFIRM (with note).**
The Cat identity is the mechanism that puts Arya on the wharves, specifically at the Happy Port, where she encounters Dareon. The kill is entirely Arya's own choice — the kindly man never ordered it, and the resulting punishment makes clear this was unauthorized. ENABLES is the correct type: the cover identity opens the door; a free human choice walks through it. The cited line (affc-arya-02:311, Brusco assignment) is accurate as a "door-opener" anchor.

One note: the Dareon encounter in affc-cat-of-the-canals-01 is what triggers the kill, not a direct consequence of the Brusco assignment itself. The Brusco line is the right conceptual anchor (the identity = the precondition), though a reviewer might prefer citing the Happy Port passage (affc-cat-of-the-canals-01:139–163) as more proximate evidence. This is a citation finesse, not a type error. Edge stands.

---

### SP4 — `killing-of-dareon CAUSES blinding-of-arya` (Tier 1)
**ADJUST — retype to TRIGGERS, or accept CAUSES with a key qualification in the note.**

The chapter text at adwd-the-blind-girl-01:141 does say: *"The kindly man had told her that they would have taken her eyes from her anyway, to help her to learn to use her other senses, but not for half a year."*

This is a real complication. The blinding was **inevitable** (part of standard blind-acolyte training), and Dareon's death **accelerated** it by ~six months. That is not the same as CAUSES in the strict sense — the blinding would have happened without the killing; the killing shortened the timeline.

The note as drafted ("blinding is the FM punishment for killing Dareon") is accurate as shorthand for how the narrative presents it: the warm milk arrives the night Cat confesses the kill, and the blindness is framed in the text as the direct consequence. But the qualifying sentence proves the mechanism is acceleration-not-causation.

Recommended resolution: Keep CAUSES but update the note to read: "Dareon's unauthorized killing triggers immediate blinding — six months ahead of the training schedule the FM had already planned. The causal link is the timing acceleration, not the blinding itself (which was inevitable)." This is defensible as Tier 1 CAUSES because the specific timing-and-framing of this blinding is caused by the kill; only the eventual blinding was inevitable.

Alternatively, type as TRIGGERS (the kill is the immediate spark for the blinding action). Either is cleaner than the current note, which overstates the causal relationship.

---

### SP6 — `arya-trains-blind-and-regains-her-sight ENABLES arya-assassinates-the-insurance-broker`
**CONFIRM.**
The sequence is explicit: Arya regains sight at the end of adwd-the-blind-girl-01 (the tallow candle). In adwd-the-ugly-little-girl-01, she has sight and the plague-face priest assigns the kill. The kindly man's "we will see if you are truly worthy" (line 83) plus the whole chapter structure make clear that having passed the blind-training curriculum is the FM's precondition for giving her a sanctioned kill. ENABLES is correct — the training-and-sight-restoration qualifies her; the kill is then assigned. Not CAUSES (she doesn't automatically kill anyone; the FM makes a separate decision to assign the task). The cited quote (line 83) fits.

---

### OBJ5 — `iron-coin ENABLES arya-departs-for-braavos` (Tier 1)
**CONFIRM.** The ASOS chapter is unambiguous: Ternesio Terys returns her money, she produces the iron coin, he replies "Valar dohaeris" and immediately grants a cabin (asos-arya-13:253–261). Without the coin she has only inadequate silver; the captain had already declined her passage. The coin is the genuine precondition — not just an instrument but the threshold object that unlocks the journey.

**OBJ3 redundancy flag:** OBJ3 (`iron-coin WIELDED_IN arya-departs-for-braavos`) and OBJ5 (`iron-coin ENABLES arya-departs-for-braavos`) are NOT true doubles. They model different relationships: OBJ5 says the coin is the precondition for the journey event (structural / logical); OBJ3 says it was used/deployed within the journey event (instantiation). Both can coexist. However, the WIELDED_IN semantics are slightly redundant given ENABLES already implies the coin's use. Flag for Matt's discretion — if WIELDED_IN is reserved for in-event deployment (like OBJ3 for the HoBaW doors, OBJ4), keeping both is internally consistent. If ENABLES subsumes WIELDED_IN for the same event, drop OBJ3. Not a blocking issue.

---

### OBJ1 — `iron-coin GIFTED_TO arya-stark` (direction)
**CONFIRM — direction is correct.**
GIFTED_TO is defined as artifact -> recipient. The coin flows from Jaqen to Arya; the edge direction `iron-coin GIFTED_TO arya-stark` correctly models artifact → recipient. The cited quote (asos-arya-13:255) confirms Jaqen gave it to her. No inversion needed.

---

### SEAM2 — `dareon MOTIVATES arya-stark` (Tier 1)
**CONFIRM.**
The text directly establishes Arya's Ned's-justice ethos as the operative motivation. The passage at adwd-the-blind-girl-01:141 — *"Dareon had been a deserter from the Night's Watch; he had deserved to die"* — gives her internal justification explicitly. Additionally in affc-cat-of-the-canals-01:141–163, the narrative shows Arya's anger at seeing Dareon shirk his vows and her internal framing of the kill as a just execution. MOTIVATES is the right type: Dareon (specifically, his desertion) drives Arya's decision. Tier 1 is justified — the text gives her explicit reasoning.

Note on MOTIVATES target: MOTIVATES should target a character (Arya-stark), which is satisfied. The implied event target is the killing-of-dareon — not the direct target of the edge, but the downstream event. This is correct modeling: `dareon MOTIVATES arya-stark` + `arya-stark AGENT_IN killing-of-dareon` together encode the full chain without collapsing it.

---

### SEAM3 — `kill-list-recitation-before-sleep CONTRASTS faceless-men` (Tier 1)
**CONFIRM — with theory-gate note.**
The structural opposition is real and well-grounded. affc-arya-02:11–19 opens with the kill-list prayer and immediately has the kindly man confront Arya about it: "Is that why you have come to us? To learn our arts, so you may kill these men you hate?" He then explains that the FM kill only those "marked by Him of Many Faces" — exactly the contrast the edge encodes. The CONTRASTS type is apt: the kill-list represents personal vendetta and fixed identity; the FM demand is to surrender all hate and become no one. The node `kill-list-recitation-before-sleep` is well-conceived as a recurring narrative object that now gets its first outbound edge.

Theory-gate: The node and edge do not assert FM cosmology as fact — they model the dramatic tension between two ethical frameworks. No gate triggered.

---

### RL13 — `waif AGENT_IN blinding-of-arya` (Tier 2)
**CONFIRM at Tier 2 — but the note needs tightening.**
The text distinguishes two moments:
1. **Initial dose:** affc-cat-of-the-canals-01:247 — the kindly man orders "warm milk for our friend Arya." He orders it; the waif presumably fetches it (consistent with the waif's role). The text does not name the waif as the one who actually brings this first cup.
2. **Ongoing regime:** adwd-the-blind-girl-01:79 — *"Each night at supper the waif brought her a cup of milk and told her to drink it down."* This is explicit and repeated: the waif administers the daily blinding draught.

RL11 (`kindly-man AGENT_IN blinding-of-arya`) is already in the set for the ordering act. RL13 (`waif AGENT_IN`) at Tier 2 is defensible for the ongoing administration — the waif is the person who physically delivers and enforces the blinding. The two-agent model (COMMANDS_IN for the kindly man, AGENT_IN for both) is slightly muddled but the waif's AGENT_IN role is textually grounded in ADWD. Keep RL13 at Tier 2 with a clearer note: "The waif administers the daily blinding draught (ongoing milk regime, ADWD:79); the initial order is the kindly man's (RL11). Tier-2 for the waif reflects her role as executor, not principal."

One cleanup: RL11 currently types the kindly man as AGENT_IN, but the more precise type for the kindly man's role may be COMMANDS_IN (he orders the milk, he doesn't personally deliver it). However, since the initial dose attribution is ambiguous (we can't confirm the waif carried that specific cup), AGENT_IN for the kindly man is acceptable under the ordering-as-agency interpretation. Flag for Matt but do not block.

---

### RL18 — `kindly-man COMMANDS_IN arya-assassinates-the-insurance-broker`
**ADJUST — attribution is defensible but partially misattributed.**
Reading adwd-the-ugly-little-girl-01 carefully:
- The **plague-face priest** issues the first directive: "Give a certain man a certain gift" (lines 71–83). He is the one who poses the task as the price for a face.
- The **kindly man** then takes over as the day-to-day handler: he explains the target's business (lines 97–135), tells Arya to "Kill him. Kill only him" (implicit at line 163), confirms the method ("that coin"), and confirms the kill at the end ("Soon after that man's heart gave out").

The current edge attributes COMMANDS_IN solely to the kindly man. This is not wrong — the kindly man IS the presiding authority who confirms, briefs, and validates the kill. But the plague-face priest gives the formal assignment. If the graph has no plague-face-priest node (candidates.json confirms it was dropped as a single-use unnamed node), then COMMANDS_IN to the kindly man is the best available attribution and is defensible. However, the note should acknowledge the attribution gap: "The FM assignment is given by a plague-face priest (unnamed, not graphed); the kindly man serves as the day-to-day handler who briefs the target, confirms the method, and validates the kill."

Tier 1 may be slightly high for the kindly man specifically as commander — consider Tier 2 given the shared/distributed authority. This is a judgment call; edge survives as ADJUST.

---

### Node type audit — `killing-of-dareon` vs `arya-assassinates-the-insurance-broker`

**`killing-of-dareon` as `event.incident` — CONFIRM.**
The text is explicit that this is unauthorized. The kindly man's entire response (adwd-the-blind-girl-01:143–148) frames it as Arya taking "god's powers on herself" outside the FM process. This is NOT a Faceless Men assignment — it is a vigilante alley kill. `event.incident` is correct; `event.assassination` would be wrong.

**`arya-assassinates-the-insurance-broker` as `event.assassination` — CONFIRM.**
This is the canonical FM-sanctioned contracted kill: properly assigned, properly executed, the girl earns her face. `event.assassination` is appropriate.

---

### REV4 — `arya-stark DECEIVES kindly-man` (Tier 1)
**CONFIRM — direction is correct.**
affc-arya-02:15: "I don't whisper any names," she said — an explicit lie, immediately caught. The kindly man sees through her at every turn. The edge models Arya's attempt (not her success). Direction `arya-stark -> kindly-man` is correct: Arya is the deceiver, the kindly man is the target of the attempted deception. Tier 1 is justified — the lying/catching dynamic is one of the arc's central repeated beats.

---

### Retirement candidate RC1 — `arya-stark TUTORS kindly-man` (affc-arya-02:23)
**RETIRE — YES, direction is definitively wrong.**

Reading affc-arya-02 around line 23:
- Lines 13–33: The kindly man initiates a confrontation about Arya's whispered names. He challenges her, she initially lies, he identifies the lie and keeps pressing. He is teaching her (that he can see lies, that the FM don't kill for personal vendetta).
- Line 211: The kindly man says "She will teach you" (referring to the waif) — and then "the two of you shall learn together, each from the other." This is the closest thing to mutual tutoring, but the frame is the kindly man deploying the waif to teach Arya.

At no point around line 23 does Arya teach or tutor the kindly man. He is the teacher throughout. The existing `kindly-man TEACHES arya-stark` edge at the same line is the correct direction. The reversed `arya-stark TUTORS kindly-man` edge is a clear direction error and should be RETIRED.

---

## Summary

| Verdict | Count | IDs |
|---------|-------|-----|
| CONFIRM | 8 | SP3, SP6, OBJ5, OBJ1, SEAM2, SEAM3, REV4, node-type-audit (both) |
| ADJUST | 3 | SP4, RL18, RL13 (note tightening) |
| REJECT | 0 | — |
| RETIRE | 1 | RC1 (`arya-stark TUTORS kindly-man`) |

---

## Theory-leakage flags
**None detected.** No edges assert Faceless Men cosmology as fact, "valar morghulis" as literal prophecy, Jaqen H'ghar identity claims, or TWOW/Mercy content. The kill-list and FM edges model observable narrative behavior, not in-universe theology.

---

## OBJ3/OBJ5 redundancy
Minor — both edges for the iron coin at the departure event can coexist under the ENABLES/WIELDED_IN distinction. Flag for Matt's discretion; not a blocking issue.

---

## Biggest concern
**SP4 note accuracy.** The claim that the blinding IS the punishment for killing Dareon is how the narrative presents it in the moment, but the adwd-the-blind-girl-01:141 text explicitly says the FM planned to blind her in six months anyway. The current note propagates the in-universe framing without flagging the complication. A reader of the edge note will incorrectly believe the blinding would not have occurred but for the kill. Adjust the note to capture the "accelerated-not-caused" nuance, or retype to TRIGGERS.
