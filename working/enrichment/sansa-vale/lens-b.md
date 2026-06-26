# Sansa / Vale Arc — Lens B: Whodunit / Revelation + SUSPECTED_OF Layer

**Produced:** 2026-06-25
**Source chapters:** asos-sansa-06, asos-sansa-07, affc-sansa-01, affc-alayne-01, affc-alayne-02
**Lens:** Hidden agency and revelation structure — who really did what, who is framed, what secret is disclosed and to whom.
**Status:** PROPOSAL ONLY — do not mint until reviewed.

---

## REVELATION / WHODUNIT EDGES

### 1. Death of Lysa Arryn — POV-confirmed kill

**Edge A — the act itself:**

- source_slug: `petyr-baelish`
- edge_type: `KILLS`
- target_slug: `death-of-lysa-arryn`
- Quote: `"Only Cat." He gave her a short, sharp shove.`
- chapter:line: `asos-sansa-07.md:301`
- Tier: 1
- Rationale: POV-confirmed on-page killing; no ambiguity. Sansa is in the room, witnesses every step. KILLS is correct — not AGENT_IN, not SUSPECTED_OF.

**Edge B — Sansa as witness:**

- source_slug: `sansa-stark`
- edge_type: `WITNESS_IN`
- target_slug: `death-of-lysa-arryn`
- Quote: `"Only Cat." He gave her a short, sharp shove. Lysa stumbled backward, her feet slipping on the wet marble. And then she was gone.`
- chapter:line: `asos-sansa-07.md:301–303`
- Tier: 1
- Rationale: Sansa is the sole POV witness to the murder. She is in the High Hall, close enough to have been shoved herself moments before.

**Edge C — Lysa as victim:**

- source_slug: `lysa-arryn`
- edge_type: `VICTIM_IN`
- target_slug: `death-of-lysa-arryn`
- Quote: `"Only Cat." He gave her a short, sharp shove. Lysa stumbled backward, her feet slipping on the wet marble. And then she was gone.`
- chapter:line: `asos-sansa-07.md:301–303`
- Tier: 1
- Rationale: Direct victim of the event.

**Edge D — Marillion as second witness (important: he saw it too):**

- source_slug: `marillion`
- edge_type: `WITNESS_IN`
- target_slug: `death-of-lysa-arryn`
- Quote: `Marillion gasped, "You . . . you . . ."`
- chapter:line: `asos-sansa-07.md:305`
- Tier: 1
- Rationale: Marillion's gasp and ellipsis confirm he saw the shove. This is precisely what makes him dangerous — and why he must be coerced. His witnessing is the causal basis for the framing arc.

---

### 2. Murder of Jon Arryn — Lysa's confession upgrades SUSPECTED_OF to COMMANDS_IN

The S133 enrichment established `petyr-baelish SUSPECTED_OF murder-of-jon-arryn` (Tier-2) sourced to `asos-sansa-07.md:287`. The same passage contains Lysa's direct confession naming LF as the instigator. The text states clearly: *"You told me to put the tears in Jon's wine, and I did."* This is not in-world suspicion — it is one principal's on-page statement to the other principal. The question for curation: does this upgrade petyr's SUSPECTED_OF to COMMANDS_IN?

**Assessment:** The text supports it. Lysa says LF told her to do it ("you told me"). LF does not deny it; his only response is "That's past and done" and a warning not to speak in front of Marillion. The prose frames this as a revelation of a settled fact between them, not a mad accusation. COMMANDS_IN is the correct edge at Tier-2 (not Tier-1 because the attribution comes from one co-conspirator addressing the other in a private moment — the epistemics are strong but not fully symmetric; the text does not show LF explicitly confirming "yes, I gave you the order").

**Proposed upgrade:**

- source_slug: `petyr-baelish`
- edge_type: `COMMANDS_IN`
- target_slug: `murder-of-jon-arryn`
- Quote: `"You told me to put the tears in Jon's wine, and I did. For Robert, and for us!"`
- chapter:line: `asos-sansa-07.md:287`
- Tier: 2
- Rationale: Lysa's confession, addressed directly to LF, names him as the order-giver for Jon Arryn's poisoning. LF's non-denial in context ("Lysa, my wife was mad" is said to third parties — here he only says "that's past and done"). This is the strongest upgrade the text will support short of LF's own admission. Remains Tier-2 because it is one party's statement to the other, not LF confessing independently. **Flag for curation: propose retiring the S133 SUSPECTED_OF and replacing with this COMMANDS_IN. The S133 SUSPECTED_OF rationale was already quoting this same line but classifying it as Tier-2 contested — COMMANDS_IN is the more precise type for "one party ordered the other to act."**

**REVEALS_TO edges from the confession scene:**

**Edge E — Lysa reveals to LF (self-confirming the order):**

- source_slug: `lysa-arryn`
- edge_type: `REVEALS_TO`
- target_slug: `petyr-baelish`
- Quote: `"You told me to put the tears in Jon's wine, and I did. For Robert, and for us!"`
- chapter:line: `asos-sansa-07.md:287`
- Tier: 1
- Rationale: Lysa, in a breakdown, names the poisoning openly to LF. The "reveals" is to the co-conspirator, confirming the shared crime. Tier-1 because this is a POV-captured utterance.
- Note: The target should ideally be the event `murder-of-jon-arryn`, but REVEALS_TO is a person-to-person edge type per the vocabulary. Model as `lysa-arryn REVEALS_TO petyr-baelish` (re-surfacing the crime) + cite the event node in evidence.

**Edge F — Lysa reveals (inadvertently) to Sansa:**

- source_slug: `lysa-arryn`
- edge_type: `REVEALS_TO`
- target_slug: `sansa-stark`
- Quote: `"You told me to put the tears in Jon's wine, and I did. For Robert, and for us! And I wrote Catelyn and told her the Lannisters had killed my lord husband, just as you said."`
- chapter:line: `asos-sansa-07.md:287`
- Tier: 1
- Rationale: Sansa is in the room and hears the confession. This is a POV chapter — Sansa now knows the truth of Jon Arryn's murder and the false letter. This is the moment Sansa learns the full founding crime of the series. The revelation is inadvertent (Lysa is not addressing Sansa), but Sansa receives it.

**Edge G — Lysa reveals the false accusatory letter to Sansa:**

- source_slug: `lysa-arryn`
- edge_type: `REVEALS_TO`
- target_slug: `sansa-stark`
- Quote: `"And I wrote Catelyn and told her the Lannisters had killed my lord husband, just as you said."`
- chapter:line: `asos-sansa-07.md:287`
- Tier: 1
- Rationale: Lysa confirms she authored the letter to Catelyn falsely blaming the Lannisters — the letter that started the war. Sansa witnesses this. This upgrades `lysa-accuses-tyrion-of-poisoning-jon-arryn` with direct authorial confirmation. Wire to `lysa-accuses-tyrion-of-poisoning-jon-arryn` as a companion note.

---

### 3. Hairnet / Purple Wedding — LF's confession to Sansa

Existing graph already has `petyr-baelish COMMANDS_IN death-of-joffrey-baratheon` (S96) sourced to asos-sansa-06:183. The REVEALS_TO dimension is not yet modeled.

**Edge H — LF reveals the hairnet plan to Sansa:**

- source_slug: `petyr-baelish`
- edge_type: `REVEALS_TO`
- target_slug: `sansa-stark`
- Quote: `"I will wager you that at some point during the evening someone told you that your hair net was crooked and straightened it for you."`
- chapter:line: `asos-sansa-06.md:183`
- Tier: 1
- Rationale: LF tells Sansa directly that the poisoning was accomplished via the hairnet she wore — pointing at Olenna Tyrell as the hand that lifted the stone. This is the on-page revelation of the mechanism. Not yet in the graph as a REVEALS_TO edge (COMMANDS_IN exists but that is a role on the event, not a person-to-person knowledge transfer).

**Edge I — LF reveals Olenna's role to Sansa:**

- source_slug: `petyr-baelish`
- edge_type: `REVEALS_TO`
- target_slug: `sansa-stark`
- Quote: `"Sansa raised a hand to her mouth. 'You cannot mean . . . she wanted to take me to Highgarden, to marry me to her grandson . . .' / 'Gentle, pious, good-hearted Willas Tyrell.'"`
- chapter:line: `asos-sansa-06.md:185–187`
- Tier: 1
- Rationale: This exchange makes explicit that Olenna Tyrell was the hand that removed the stone from the hairnet. LF confirms by implication without flat-stating it ("Lady Olenna was not about to let Joff harm her precious darling granddaughter"). Sansa now understands who did it.
- Note: The quote spans dialogue attribution. Use the narrower LF attribution line: `"Gentle, pious, good-hearted Willas Tyrell. Be grateful you were spared, he would have bored you spitless. The old woman is not boring, though, I'll grant her that."` (asos-sansa-06.md:187) as the unambiguous LF confirmation of Olenna's involvement.

**Revised single-quote for Edge I:**

- Quote: `"The old woman is not boring, though, I'll grant her that. A fearsome old harridan, and not near as frail as she pretends."`
- chapter:line: `asos-sansa-06.md:187`
- Rationale: LF's characterization of Olenna, in direct answer to Sansa's "you cannot mean . . ." reaction to the hairnet implication, is the effective on-page revelation of Olenna as the agent. Tier-1 because this is a POV-chapter direct exchange.

**DEDUP NOTE on Joffrey death edges:** `petyr-baelish COMMANDS_IN death-of-joffrey-baratheon` (S96/S135) and `petyr-baelish SUSPECTED_OF death-of-joffrey-baratheon` — check whether a SUSPECTED_OF was minted for LF. Scan shows only `tyrion-lannister SUSPECTED_OF` and `sansa-stark SUSPECTED_OF` from S135. LF got COMMANDS_IN (S96). No dedup issue. These REVEALS_TO edges are additive.

---

### 4. Harry-the-Heir Plan — LF reveals long-game to Sansa

**Edge J — LF reveals the Harry plan and the Sansa reveal:**

- source_slug: `petyr-baelish`
- edge_type: `REVEALS_TO`
- target_slug: `sansa-stark`
- Quote: `"when they come together for his wedding, and you come out with your long auburn hair, clad in a maiden's cloak of white and grey with a direwolf emblazoned on the back . . . why, every knight in the Vale will pledge his sword to win you back your birthright. So those are your gifts from me, my sweet Sansa . . . Harry, the Eyrie, and Winterfell."`
- chapter:line: `affc-alayne-02.md:467`
- Tier: 1
- Rationale: LF explicitly states the long-game to Sansa — use Harry to consolidate the Vale, then reveal Sansa's true identity to rally the Vale lords, then reclaim Winterfell. This is the clearest statement of the manipulation strategy in all five chapters.

**Edge K — LF MANIPULATES Sansa via the betrothal:**

- source_slug: `petyr-baelish`
- edge_type: `MANIPULATES`
- target_slug: `sansa-stark`
- qualifier: `via_betrothal_to_harry`
- Quote: `"You are promised to Harrold Hardyng, sweetling, provided you can win his boyish heart . . . which should not be hard, for you."`
- chapter:line: `affc-alayne-02.md:441`
- Tier: 1
- Rationale: LF has secretly brokered a betrothal for Sansa (as Alayne) to Harrold Hardyng, without Sansa's knowledge or consent, as an instrument of his Vale strategy. He frames it as a gift; structurally it is a manipulation (she is a piece being moved). MANIPULATES + qualifier is the correct edge. The target is Sansa-as-person, not the Harry plan event.

**Edge L — PROPOSED_AS_BRIDE (Sansa to Harry):**

- source_slug: `sansa-stark`
- edge_type: `PROPOSED_AS_BRIDE`
- target_slug: `harrold-hardyng`
- Quote: `"This is only a betrothal. The marriage must needs wait until Cersei is done and Sansa's safely widowed."`
- chapter:line: `affc-alayne-02.md:437`
- Tier: 1
- Rationale: LF has arranged a betrothal contract with Lady Waynwood for Alayne Stone (Sansa) to marry Harrold Hardyng. The formal betrothal is confirmed on-page. PROPOSED_AS_BRIDE is the correct type (unpopulated vocabulary type — first instance).

---

### 5. Lyn Corbray — staged quarrel

**Edge M — LF MANIPULATES Lyn Corbray:**

- source_slug: `petyr-baelish`
- edge_type: `MANIPULATES`
- target_slug: `lyn-corbray`
- qualifier: `via_gold_and_staged_enmity`
- Quote: `"Ser Lyn will remain my implacable enemy. He will speak of me with scorn and loathing to every man he meets, and lend his sword to every secret plot to bring me down." [Alayne:] "And how shall you reward him for this service?" / "With gold and boys and promises, of course."`
- chapter:line: `affc-alayne-01.md:339–343`
- Tier: 1
- Rationale: LF reveals to Sansa that Lyn Corbray's "implacable enmity" is staged — Corbray is secretly in LF's pay, performing hostility to give the Lords Declarant a visible opponent and lend LF's position the appearance of vulnerability. The quarrel at the parley (drawing Lady Forlorn) is manufactured theater. This is a textbook MANIPULATES edge.

**Edge N — LF REVEALS_TO Sansa the Corbray arrangement:**

- source_slug: `petyr-baelish`
- edge_type: `REVEALS_TO`
- target_slug: `sansa-stark`
- Quote: `"Ser Lyn will remain my implacable enemy. He will speak of me with scorn and loathing to every man he meets, and lend his sword to every secret plot to bring me down."`
- chapter:line: `affc-alayne-01.md:339`
- Tier: 1
- Rationale: LF explicitly tells Sansa the Corbray arrangement after the Lords Declarant depart. Sansa has just realized it herself ("That was when her suspicion turned to certainty" — affc-alayne-01.md:341) and LF confirms it.

---

### 6. Lord Nestor — bought with the Gates of the Moon

**Edge O — LF MANIPULATES Nestor Royce:**

- source_slug: `petyr-baelish`
- edge_type: `MANIPULATES`
- target_slug: `nestor-royce`
- qualifier: `via_hereditary_grant_of_gates_of_the_moon`
- Quote: `"Our lies will profit him."`
- chapter:line: `affc-sansa-01.md:37`
- Tier: 1
- Rationale: LF grants Nestor Royce hereditary tenure of the Gates of the Moon — signed as Lord Protector, not by Lysa — specifically to buy his loyalty against the Lords Declarant. LF explains the mechanism to Sansa: the grant is tied to LF's position, so Nestor's title evaporates if LF is removed, making him an ally by structural self-interest. LF explicitly frames it as manipulation ("his lies will profit him"). Cross-ref: `lord-nestor-and-the-knights-call-for-marillion-s-death` (existing node) — Nestor's visible compliance is a downstream product of this manipulation.

---

## SUSPECTED_OF (unproven agency only)

No new SUSPECTED_OF edges are warranted from these five chapters. The key agency questions are all resolved in-text:

- Lysa's death: POV-confirmed KILLS (above).
- Jon Arryn's murder: Lysa confesses on-page; LF's role is named by Lysa directly. The S133 SUSPECTED_OF for LF should be upgraded to COMMANDS_IN (see above).
- Joffrey's death: Already COMMANDS_IN + AGENT_IN for LF and Olenna. The text adds REVEALS_TO dimension but no new uncertain agency.
- Marillion: He is a coerced instrument, not an independent agent — no SUSPECTED_OF.

The one edge where SUSPECTED_OF might be considered is whether Gilwood Hunter really did murder his father (affc-alayne-01.md:335: "Gilwood Hunter will be murdered by his brothers. Most likely by young Harlan, who arranged Lord Eon's death"). But this is LF's unconfirmed prediction about a third-party event and lies entirely outside the Sansa/Vale arc task scope.

---

## FRAMING (Marillion)

### The Coerced False Confession Arc

The framing of Marillion for Lysa's murder spans three chapters and is worth modeling as a sequence of DECEIVES edges from LF to the Vale lords, with Marillion as instrument.

**Edge P — LF DECEIVES the Vale lords (via Marillion's coerced confession):**

- source_slug: `petyr-baelish`
- edge_type: `DECEIVES`
- target_slug: `nestor-royce`
- qualifier: `via_marillion_false_confession`
- Quote: `"We have come to an agreement, Marillion and I. Mord can be most persuasive. And if our singer disappoints us and sings a song we do not care to hear, why, you and I need only say he lies. Whom do you imagine Lord Nestor will believe?"`
- chapter:line: `affc-sansa-01.md:33`
- Tier: 1
- Rationale: LF explicitly describes the deception mechanism to Sansa before Nestor arrives. DECEIVES + qualifier is the correct type. The target is Nestor Royce as the deceived party (principal of the Vale). Model Nestor as the representative target; a note can indicate the broader audience (all Vale lords who hear the testimony).

**Edge Q — Marillion performs the false testimony (coerced):**

- source_slug: `marillion`
- edge_type: `DECEIVES`
- target_slug: `nestor-royce`
- qualifier: `false_confession_lysa_death`
- Quote: `"I loved her so, I could not bear to see her in another's arms . . . a madness seized me . . ."`
- chapter:line: `affc-sansa-01.md:173`
- Tier: 1
- Rationale: Marillion delivers a false confession in the High Hall, witnessed by Lord Nestor and other lords. The coercion mechanism (Mord, finger injuries, sky cell) is referenced obliquely but the confession itself is on-page verbatim. Note: Marillion's agency here is compromised — he is not a free actor — but the DECEIVES edge still attaches to him as the speaking subject. LF's COMMANDS_IN on this action is modeled via Edge P.

**Edge R — Sansa DECEIVES Nestor (per LF's direction):**

- source_slug: `sansa-stark`
- edge_type: `DECEIVES`
- target_slug: `nestor-royce`
- qualifier: `false_eyewitness_account_lysa_death`
- Quote: `"'I saw . . . I was with the Lady Lysa when . . .' A tear rolled down her cheek. That's good, a tear is good. '. . . when Marillion . . . pushed her.' And she told the tale again, hardly hearing the words as they spilled out of her."`
- chapter:line: `affc-sansa-01.md:135`
- Tier: 1
- Rationale: Sansa gives a false eyewitness account implicating Marillion before Lord Nestor's party. The text makes explicit that she knows it is a lie, knows how to use the tear strategically, and "told the tale again, hardly hearing the words." This is a fully conscious deception under duress. Note: Sansa's coerced status should be captured in the asserted_relation — she acts under extreme threat (LF's "else you and I must leave the Eyrie by the same door Lysa used," affc-sansa-01.md:61).

**Edge S — LF frames Marillion as a new proposed event node:**

The act of framing Marillion has no dedicated event node yet. Lens A should be proposing `death-of-lysa-arryn`; a companion event `framing-of-marillion-for-lysa-s-death` may be warranted. Do NOT mint here — flag for curation.

NEEDS_VOCAB note: There is no `FRAMES` or `FALSE_ACCUSATION` edge type in the vocabulary. The combination of `DECEIVES` (LF→lords, Sansa→lords, Marillion→lords) plus the structural role edges adequately covers the framing without requiring a new type. COMMANDS_IN (LF→Marillion's coercion) could be modeled if a framing-event node exists to be the target.

---

## DEDUP NOTES

1. **petyr-baelish SUSPECTED_OF murder-of-jon-arryn (S133):** Propose to RETIRE this edge and replace with `petyr-baelish COMMANDS_IN murder-of-jon-arryn` (Tier-2, same source quote). The existing SUSPECTED_OF rationale already quoted `asos-sansa-07.md:287`; COMMANDS_IN is the more precise classification given "you told me to" is one party naming the order directly to the other. Matt should decide whether to upgrade or keep both (COMMANDS_IN for the order, SUSPECTED_OF for the question of whether he acted on independent motivation vs. broader conspiracy).

2. **petyr-baelish COMMANDS_IN death-of-joffrey-baratheon (S96):** Already exists and is correct. The REVEALS_TO edges proposed here (H, I) are additive — they model the knowledge-transfer to Sansa, not the act itself. No dedup needed.

3. **sansa-receives-the-poisoned-hairnet:** Existing node. Edges H and I reference this event as context but do not duplicate any existing edges on it. The existing CAUSES edge (hairnet → Joffrey death) and WITNESS_IN are separate from the person-to-person REVEALS_TO being proposed.

4. **lord-nestor-and-the-knights-call-for-marillion-s-death:** Existing node. Edge P (LF DECEIVES Nestor) and Edge Q (Marillion false confession) are the causal upstream of this existing node. Check whether that existing node has any incoming CAUSES/TRIGGERS edges; if not, `marillion DECEIVES nestor-royce (false_confession)` → `lord-nestor-and-the-knights-call-for-marillion-s-death` is a TRIGGERS candidate (not proposed here — leave for Lens A or a causal lens).

5. **wedding-of-petyr-baelish-and-lysa-arryn:** Existing node. No proposed edges directly target it in this proposal.

6. **lysa-accuses-tyrion-of-poisoning-jon-arryn:** Existing node. Edge G (Lysa's confession on the false letter) provides direct authorial confirmation of this event's origin. The existing node is enriched by noting that `asos-sansa-07.md:287` contains Lysa's own admission she wrote the letter at LF's direction. No dedup required — the existing node documents the accusation, not the confession. Suggest adding `asos-sansa-07.md:287` as a citation/enrichment to that node.

---

## HARVEST

Notable finds while reading these chapters that are not the primary task — drop as pointers for later passes:

- `asos-sansa-06.md:75` / **food** / LF's estate: "gulls' eggs and seaweed soup," salt mutton; wine (Arbor vintage); pomegranate seeds, blood orange, apples, pears, grapes, bread; the entire feast after the wedding (quail, venison, roast boar, mead, "Milady's Supper" sung by Marillion). High hospitality-register scene — first major food passage in the Vale arc.

- `asos-sansa-07.md:297–303` / **load-bearing quote** / The Moon Door murder: `"Only Cat." He gave her a short, sharp shove.` — most important five words in the chapter; should be attached to the `death-of-lysa-arryn` node as primary evidence_quote.

- `asos-sansa-07.md:287` / **load-bearing quote** / Jon Arryn founding crime: `"You told me to put the tears in Jon's wine, and I did. For Robert, and for us! And I wrote Catelyn and told her the Lannisters had killed my lord husband, just as you said."` — the full confession; already captured in S133 but the letter-authorship clause ("I wrote Catelyn") is the evidentiary nail on `lysa-accuses-tyrion-of-poisoning-jon-arryn`.

- `asos-sansa-07.md:275` / **load-bearing quote / foreshadowing** / The moon-tea abortion: `"I would have given him a son too, but they murdered him with moon tea, with tansy and mint and wormwood, a spoon of honey and a drop of pennyroyal. It wasn't me, I never knew, I only drank what Father gave me . . ."` — Lysa reveals Lord Hoster Tully forced her to abort LF's child. Evidence for a Hoster Tully node enrichment and for the LF/Lysa backstory. Relates to `working/persona-bloodraven.md` note about kin dynamics.

- `affc-sansa-01.md:117` / **narrative frame** / Sansa's internal rationalization: `"She was mad and dangerous. She murdered her own lord husband, and would have murdered me if Petyr had not come along to save me."` — shows Sansa already constructing the false narrative as truth; character psychology edge for a voice-analysis pass (Pass 3).

- `affc-alayne-01.md:87–88` / **sweetsleep / food** / `"Perhaps a pinch of sweetsleep in his milk, have you tried that? Just a pinch, to calm him and stop his wretched shaking."` — LF suggests sweetsleep for Robert Arryn; Colemon is alarmed. First introduction of the sweetsleep-poisoning thread for Robert. High-value for a future Sweetrobin-arc pass; the repeated doses are mentioned in affc-alayne-02 too. Cross-ref: `affc-alayne-02.md:127–149` — "a cup of sweetmilk" = the sweetsleep dose; Colemon says "this must be the last. For half a year, or longer." Slow-poisoning of the sickly heir is in progress on-page.

- `affc-alayne-01.md:335–343` / **load-bearing quote** / Corbray arrangement revealed: `"Ser Lyn will remain my implacable enemy . . . With gold and boys and promises, of course."` — the fullest explicit statement of LF's manipulation of Corbray; already captured in Edges M/N above, but the "boys" line is a character detail about Corbray worth attaching to a Lyn-Corbray node.

- `affc-alayne-02.md:467` / **load-bearing quote** / The grand plan: `"Harry, the Eyrie, and Winterfell."` — three-word summary of LF's endgame as stated to Sansa. Primary evidence for any node representing LF's political strategy.

- `affc-alayne-02.md:181` / **physical description** / Mya Stone: `"those are his eyes, and she has his hair too, the thick black hair he shared with Renly"` — Sansa identifies Mya Stone as Robert Baratheon's daughter by appearance. Cross-identity / kinship edge candidate for a Mya Stone node.
