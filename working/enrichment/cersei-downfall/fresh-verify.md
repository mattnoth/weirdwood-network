# Fresh Verify — Cersei Downfall Enrichment (run_id cersei-downfall-enrichment-s140)

Verifier: adversarial independent session, 2026-06-23
Source files checked: affc-cersei-03.md, affc-cersei-08.md, affc-cersei-09.md, affc-cersei-10.md

---

## Verdicts

### PROPHECY cluster

**Edge 1** — `maggy-the-frogs-prophecy --PROPHESIED_BY--> maggy-the-frog | T1 | affc-cersei-08:243`
**CONFIRM.**
Line 243 has Maggy's voice delivering the prophecy directly ("Aye. Queen you shall be . . . until there comes another, younger and more beautiful, to cast you down and take all that you hold dear."). Unambiguous source attribution.

---

**Edge 2** — `maggy-the-frogs-prophecy --MOTIVATES--> cersei-lannister | T1 | affc-cersei-08:243`
**CONFIRM.**
MOTIVATES targets Cersei (a character node) — type is valid. The cite at line 243 is the delivery of the prophecy; the explicit motivation link fires at lines 327–341 in the same chapter (Qyburn asks "And you wish to forestall this prophecy?" / Cersei: "More than anything" / "I knew it all along, she thought. Even in the tent."). Citing line 243 is reasonable as the prophecy's source; the motivation it generates is confirmed in the same scene. No failure mode here.

---

**Edge 3** — `cersei-lannister --SUBJECT_OF_PROPHECY--> maggy-the-frogs-prophecy | T1 | affc-cersei-08:243`
**CONFIRM.**
Lines 241–243 show young Cersei asking "I will be queen, though?" and receiving the answer directly addressed to her. Subject-of is unambiguous.

---

**Edge 4** — `maggy-the-frogs-prophecy --FORESHADOWS--> cersei-is-captured-in-the-sept | T2 | affc-cersei-08:243`
**CONFIRM** (FLAGGED caveat does not invalidate; T2 is correct).

The proposal is flagged because the proximate captor is the Faith/Osney's reversed confession, not Margaery directly. This is accurate. However:

1. The prophecy at line 243 says "cast you down and take all that you hold dear." Cersei at cersei-10:49 reads her own capture as the fulfillment: "The younger queen whose coming she'd foretold was finished, and if that prophecy could fail, so could the rest." This passage confirms the text treats the capture as prophecy fulfillment, making FORESHADOWS textually grounded.
2. FORESHADOWS does not require a single proximate agent — it points to an outcome, not a mechanism. "Cast you down" → Cersei imprisoned in the Sept is a clean match.
3. T2 (Tier 2) correctly captures that the causal chain is mediated; Margaery's exposure triggers the Sparrow's leverage, not a direct Margaery action.

No change needed. The flagged note is accurate but does not constitute a failure mode for this edge type.

---

### MURDER of old High Septon

**Edge 5** — `osney-kettleblack --AGENT_IN--> murder-of-the-old-high-septon | T1 | affc-cersei-10:243`
**CONFIRM.**
Exact text at line 243: *"She's the queen I fucked, the one sent me to kill the old High Septon. He never had no guards. I just come in when he was sleeping and pushed a pillow down across his face."* Osney's own confession under duress and later repeated to the High Septon. T1 justified — it is a direct first-person admission in POV text.

---

**Edge 6** — `cersei-lannister --COMMANDS_IN--> murder-of-the-old-high-septon | T2 | affc-cersei-10:247`
**CONFIRM.** COMMANDS_IN is correct; T2 is slightly conservative but defensible.

Line 247 (Cersei's internal monologue while fleeing): *"I'll rid myself of this High Septon just as I did the other."* This is Cersei's own POV thought, explicitly claiming she disposed of the prior High Septon the same way — confirming she ordered Osney's action. Combined with Osney's confession at line 243 naming her as the one who sent him, the evidence for COMMANDS_IN rather than SUSPECTED_OF is solid. T1 could also be argued (own-POV internal admission = canon), but T2 is acceptable given the phrasing is retrospective/inferential rather than a direct order shown on-page.

---

**Edge 7** — `murder-of-the-old-high-septon --ENABLES--> cersei-rearms-the-faith-and-forgives-the-debt | T2 | affc-cersei-10:247`
**CONFIRM** with note on mediation.

The flagged distal concern is real: the actual causal chain is `murder → High Sparrow elected → Cersei rearms Faith`. The election of the High Sparrow is a mediated step not represented as its own node in this edge. However:

- ENABLES tolerates distal causation when the mechanism is clear and the prior event was a genuine prerequisite.
- Without the murder of the old High Septon, the High Sparrow would not have been elevated, and Cersei would not have had the leverage/motivation context for the rearmament deal.
- T2 correctly flags the indirection.

The edge is defensible. A cleaner alternative would be to add an intermediate event node (high-sparrow-election) and chain `murder ENABLES election ENABLES rearmament`. If the graph later models the High Sparrow election as a node, this ENABLES edge should be split. For now, CONFIRM at T2.

---

### DE-ISLAND warrants

**Edge 8** — `cersei-confronts-and-arrests-the-blue-bard --ENABLES--> cersei-fills-in-the-arrest-warrants | T1 | affc-cersei-10:77`
**CONFIRM.**
cersei-09:199 shows Qyburn's torture session producing the names (Tallad, Turnberry, Jalabhar Xho, Redwyne twins, Osney Kettleblack, Clifton). cersei-10:77 shows Cersei filling those same names into the arrest warrants. The supply of names from the Blue Bard's torture is the direct prerequisite for the named warrants. The Redwyne twins appear on both lists but are later selectively exonerated (cersei-10:81), which shows Cersei was curating the list from Wat's testimony — further confirming the causal link. T1 is justified.

---

### DEAD-END downstream fix

**Edge 9** — `cersei-is-stripped-and-imprisoned --CAUSES--> cersei-resolves-on-trial-by-combat | T1 | affc-cersei-10:313`
**CONFIRM.**
Line 313: *"Even in her exhausted, frightened state, the queen knew she dare not trust her fate to a court of sparrows. Nor could she count on Ser Kevan to intervene . . . It will have to be a trial by battle. There is no other way."* The imprisonment is the direct precondition that forces this resolution. CAUSES (not ENABLES) is correct — the imprisonment is the precipitating event, not merely a door-opener.

---

**Edge 10** — `cersei-lannister --AGENT_IN--> cersei-resolves-on-trial-by-combat | T1 | affc-cersei-10:313`
**CONFIRM.**
"It will have to be a trial by battle. There is no other way." Cersei is unambiguously the agent making the decision. T1 correct.

---

**Edge 11** — `qyburn --ADVISES--> cersei-lannister | T1 | affc-cersei-10:307`
**CONFIRM.**
Line 307: *"Hope remains. Your Grace has the right to prove your innocence by battle. My queen, your champion stands ready. There is no man in all the Seven Kingdoms who can hope to stand against him. If you will only give the command . . ."* Qyburn actively counsels the trial-by-battle path and introduces Robert Strong as champion. ADVISES is the right edge type. T1 justified.

---

### SECONDARY substrate

**Edge 12** — `qyburn --TORTURES--> blue-bard | T1 | affc-cersei-09:191`
**CONFIRM.**
Line 191: *"The razor flashed, the singer shrieked. On his chest a wet red eye wept blood."* Plus the sustained session from ~line 175 through line 199 (boots full of blood by dawn). Direct on-page depiction, own-POV chapter. T1 correct.

---

**Edge 13** — `taena-merryweather --INFORMS--> cersei-lannister | T1 | affc-cersei-03:173`
**CONFIRM.**
Line 173: *"There is something you must know. Your maid is bought and paid for. She tells Lady Margaery everything you do."* Taena volunteers intelligence about Senelle's espionage. INFORMS is exact. T1 correct.

---

**Edge 14** — `taena-merryweather --CONSPIRES_WITH--> cersei-lannister | T1 | affc-cersei-09:251`
**CONFIRM.**
Line 251: Taena is in the bath with Cersei, jointly planning which of Margaery's cousins (Alla) to spare and turn as a witness against the others ("Leave her to me, my sweet."). This is active co-planning of a conspiracy against Margaery, not merely informing. CONSPIRES_WITH is the right type. T1 justified.

---

**Edge 15** — `lancel-lannister --MEMBER_OF--> warriors-sons | T1 | affc-cersei-08:147`
**CONFIRM.**
Line 147: *"her mooncalf cousin had forsaken castle, lands, and wife and wandered back to the city to join the Noble and Puissant Order of the Warrior's Sons, yet there he stood with the other pious fools."* Direct on-page membership. T1 correct.

---

## Summary

**15 CONFIRM / 0 ADJUST / 0 REJECT**

All 15 edges hold against the source text. Notes on the three flagged edges:

- **Edge 4 (FORESHADOWS)**: The flagged caveat (proximate captor = Faith, not Margaery) is accurate but does not invalidate the edge. cersei-10:49 confirms the text itself treats the capture as prophecy fulfillment.
- **Edge 6 (COMMANDS_IN)**: T1 defensible given Cersei's own-POV admission at line 247; T2 is conservative but acceptable.
- **Edge 7 (distal ENABLES)**: Real mediation gap (High Sparrow election not modeled as intermediate node). If that event is later added to the graph, this edge should be split. T2 correctly flags the indirection.
