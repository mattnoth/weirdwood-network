# Fresh Verify — Sansa / Vale Enrichment (S148)

**Verifier:** independent fresh agent (read-only, did not mint these edges)
**Date:** 2026-06-25
**Method:** read all 6 source chapters; ran `graph-query.py --neighbors` on key nodes to check redundancy and existing state.

**Status note:** all 34 edges and 3 nodes are already minted in the graph (the graph-query tool confirms their presence). This review should gate any post-hoc adjustments or retirements in a finalize pass.

---

## Edge Verdicts

### Spine / Precondition chain (SP)

| ID | Edge | Verdict | Rationale |
|----|------|---------|-----------|
| **SP1** | `littlefinger-smuggles-sansa ENABLES sansa-adopts-the-alayne-stone-identity` | **CONFIRM** | The escape necessitates the cover — if Sansa stayed in KL there would be no need for "Alayne Stone." Quote (line 105) is LF constructing the cover story at the Fingers, which is downstream of the smuggle. ENABLES (precondition, not proximate cause) is correct. |
| **SP2** | `littlefinger-smuggles-sansa ENABLES wedding-of-petyr-baelish-and-lysa-arryn` | **CONFIRM** | The extraction is the occasion of the long-deferred wedding — Lysa rides to the Fingers to meet them. Quote (line 41): "The Lady Lysa and I are to be wed" — LF announces it just after landfall. ENABLES (precondition without strict necessity) is right; a wedding could theoretically have happened without the extract, but the smuggle is what triggers the rendezvous timing. Acceptable. |
| **SP3** | `wedding-of-petyr-baelish-and-lysa-arryn ENABLES death-of-lysa-arryn` | **ADJUST** | See detailed analysis below. Keep ENABLES, but the note should be clarified. The proximate trigger is not the marriage per se but Lysa's jealous rage — however, the marriage placed Lysa in LF's power at the Eyrie, which is the structural precondition that made the murder both safe and strategically useful. ENABLES (not CAUSES) is the right call. The quote "My sweet silly jealous wife" at line 297 is LF's sneer just before he shoves her — it evokes the jealousy trigger but the line is not itself the precondition. **Adjust the note slightly**: the cited line doesn't establish a precondition — it's the murder scene. Better supporting line would be the marriage itself (asos-sansa-06, line 229: "Now... I've brought my own septon"). But quote-accuracy is pre-checked. The edge TYPE/DIRECTION is correct; note clarification only, not a type change. No schema change needed. |
| **SP4** | `death-of-lysa-arryn CAUSES lord-nestor-and-the-knights-call-for-marillion-s-death` | **CONFIRM** | Direct: Lysa's death creates the situation requiring Marillion's framing. Nestor's hearing at affc-sansa-01 line 185 ("He should have followed Lady Lysa out the Moon Door") is the lords calling for his death — that's DIRECT causation. CAUSES is correct, not over-distal. |
| **SP5** | `death-of-lysa-arryn CAUSES lords-declarant-confront-littlefinger` | **CONFIRM** | Text at affc-alayne-01 line 21: "The six had gathered at Runestone after Lysa Arryn's fall, and there made a pact together." Direct causation is explicitly stated in the text. CAUSES is correct. |

### Lysa death event hub (L)

| ID | Edge | Verdict | Rationale |
|----|------|---------|-----------|
| **L1** | `petyr-baelish KILLS lysa-arryn` | **CONFIRM** | POV-confirmed kill (asos-sansa-07 line 301: "He gave her a short, sharp shove"). Tier 1 is right. |
| **L2** | `petyr-baelish AGENT_IN death-of-lysa-arryn` | **CONFIRM** | Executor role on the event hub. Same quote. No issue. |
| **L3** | `lysa-arryn VICTIM_IN death-of-lysa-arryn` | **CONFIRM** | Line 303: "Lysa stumbled backward, her feet slipping on the wet marble. And then she was gone." Correct. |
| **L4** | `sansa-stark WITNESS_IN death-of-lysa-arryn` | **CONFIRM** | Sansa is the POV witness. Line 303 confirms she observes the fall. She had just been dragged to the Moon Door herself, is kneeling at a pillar — unambiguous eyewitness. |
| **L5** | `marillion WITNESS_IN death-of-lysa-arryn` | **CONFIRM** | Line 305: "Marillion gasped" — he sees the shove. Confirmed eyewitness; this is the textual basis for his framing. |
| **L6** | `moon-door WIELDED_IN death-of-lysa-arryn` | **ADJUST** | See detailed analysis below. The edge is acceptable but the cited quote is weak. |

### Identity adoption event (AI)

| ID | Edge | Verdict | Rationale |
|----|------|---------|-----------|
| **AI1** | `sansa-stark AGENT_IN sansa-adopts-the-alayne-stone-identity` | **CONFIRM** | Sansa actively adopts the persona; line 105 quote is LF's opening construction of it, and line 127 ("It will be like playing a game, won't it?") confirms Sansa's willing acceptance. AGENT_IN is right. |
| **AI2** | `petyr-baelish AGENT_IN sansa-adopts-the-alayne-stone-identity` | **CONFIRM** | LF architects and presents the identity (line 215: "My lady, allow me to present you Alayne Stone"). He is the event's architect. AGENT_IN correct. |
| **AI3** | `petyr-baelish DECEIVES lysa-arryn` | **CONFIRM** | LF presents Sansa to Lysa as his bastard daughter; Lysa responds "A bastard? Petyr, have you been wicked?" — she believes the cover. DECEIVES is correct. Tier 1 warranted (on-page, direct). |

### Lords Declarant event (LD)

| ID | Edge | Verdict | Rationale |
|----|------|---------|-----------|
| **LD1** | `lords-declarant AGENT_IN lords-declarant-confront-littlefinger` | **CONFIRM** | Line 21: "made a pact together, vowing to defend Lord Robert, the Vale, and one another." The faction is the collective actor. Correct. |
| **LD2** | `lords-declarant OPPOSES petyr-baelish` | **CONFIRM** | Line 21: spoke of "misrule" and "false friends and evil counselors" aimed at LF. Direct. OPPOSES is the right dyadic edge for a faction-level opposition. |
| **LD3** | `yohn-royce PARTICIPATES_IN lords-declarant-confront-littlefinger` | **CONFIRM** | Line 203: "We did not come for your signature. Nor do we mean to bandy words with you, Littlefinger" — Bronze Yohn is the de facto leader and chief speaker. PARTICIPATES_IN correct. |
| **LD4** | `lyn-corbray PARTICIPATES_IN lords-declarant-confront-littlefinger` | **CONFIRM** | Line 273: "He drew his longsword." Corbray is physically present and draws Lady Forlorn. PARTICIPATES_IN correct. |
| **LD5** | `nestor-royce PARTICIPATES_IN lords-declarant-confront-littlefinger` | **CONFIRM** | Line 195: "Nestor Royce, who hesitated before walking around the table to take the empty chair beside Lord Petyr." Nestor physically participates but sides with LF — still PARTICIPATES_IN (the edge type is neutral on alignment). Correct. |

### War-trigger chain (W)

| ID | Edge | Verdict | Rationale |
|----|------|---------|-----------|
| **W1** | `petyr-baelish COMMANDS_IN murder-of-jon-arryn` | **ADJUST** (keep, but see retirement note below) | See detailed analysis below. |
| **W2** | `lysa-arryn REVEALS_TO sansa-stark` | **CONFIRM** | Line 287: "And I wrote Catelyn and told her the Lannisters had killed my lord husband, just as you said" — Lysa confesses the founding crime to LF in Sansa's presence. Sansa overhears. REVEALS_TO correctly captures that Sansa learns this. Tier 1 appropriate; this is direct text. |
| **W3** | `petyr-baelish REVEALS_TO sansa-stark` | **CONFIRM** | Line 183 (asos-sansa-06): "I will wager you that at some point during the evening someone told you that your hair net was crooked and straightened it for you." LF discloses the hairnet poisoning mechanism (Olenna lifted the stone) to Sansa. REVEALS_TO is correct. |
| **W4** | `petyr-baelish REVEALS_TO sansa-stark` | **CONFIRM** | affc-alayne-02 line 467: "So those are your gifts from me, my sweet Sansa . . . Harry, the Eyrie, and Winterfell." LF lays out the full long-game plan. REVEALS_TO is correct. |
| **W5** | `murder-of-jon-arryn ENABLES lysa-accuses-tyrion-of-poisoning-jon-arryn` | **CONFIRM** | This is a high-value structural fix. Line 287 quote ("And I wrote Catelyn and told her the Lannisters had killed my lord husband") confirms the false accusation is downstream of the murder. Without the murder, there is no letter, no accusation. ENABLES is correct (proximate cause is Lysa acting, so ENABLES rather than CAUSES is right). |

### Harry / betrothal (HB)

| ID | Edge | Verdict | Rationale |
|----|------|---------|-----------|
| **HB1** | `harrold-hardyng BETROTHED_TO sansa-stark` | **CONFIRM** | affc-alayne-02 line 441: "You are promised to Harrold Hardyng, sweetling." Explicit, unambiguous. Tier 1. |
| **HB2** | `petyr-baelish MARRIES_OFF sansa-stark` | **CONFIRM** | Line 433: "I have made a marriage contract for you." LF is the arranger. MARRIES_OFF captures the power relation correctly. |

### Lyn Corbray conspiracy (LC)

| ID | Edge | Verdict | Rationale |
|----|------|---------|-----------|
| **LC1** | `petyr-baelish CONSPIRES_WITH lyn-corbray` | **CONFIRM** | See detailed analysis below. |

### Nestor manipulation (NM)

| ID | Edge | Verdict | Rationale |
|----|------|---------|-----------|
| **NM1** | `petyr-baelish DECEIVES nestor-royce` | **CONFIRM** | affc-sansa-01 line 33: "you and I need only say he lies. Whom do you imagine Lord Nestor will believe?" — LF engineers the false frame. DECEIVES is right (Nestor is deceived into believing Marillion killed Lysa). |
| **NM2** | `petyr-baelish MANIPULATES nestor-royce` via_bribe | **CONFIRM** | Line 245: "You see the wonders that can be worked with lies and Arbor gold?" — the hereditary grant of the Gates of the Moon + Arbor gold is LF using non-deceptive leverage (Nestor isn't fooled about what he's getting — he knows he's being bought, as confirmed by "I will not say I had not hoped for this"). MANIPULATES (via_bribe) is distinct from DECEIVES: here the instrument is inducement not false belief. The two edges are genuinely non-redundant. |
| **NM3** | `marillion DECEIVES nestor-royce` | **CONFIRM** | Line 173: Marillion delivers the false confession under coercion. The deceiving actor is Marillion (even though LF scripted it). DECEIVES is correct for Marillion as the proximate deceiver of Nestor. |
| **NM4** | `sansa-stark DECEIVES nestor-royce` | **CONFIRM** | Line 135: Sansa gives the false eyewitness account. This is her first active lie in the game — a key Sansa character edge. Confirmed by the full passage at affc-sansa-01:131-135. DECEIVES is correct. |

### Support cast (SC)

| ID | Edge | Verdict | Rationale |
|----|------|---------|-----------|
| **SC1** | `lothor-brune AGENT_IN littlefinger-smuggles-sansa-out-of-kings-landing` | **CONFIRM** | asos-sansa-05 line 117: "Ser Lothor Brune stood beside him with a torch." Brune executes the extraction (and the Dontos killing). AGENT_IN correct. |
| **SC2** | `lothor-brune GUARDS sansa-stark` | **CONFIRM** | asos-sansa-06 line 287: "Lord Petyr said watch out for you." Brune intervenes against Marillion's assault. GUARDS is correct. |
| **SC3** | `robert-arryn WARD_OF petyr-baelish` qualifier `formal` | **ADJUST** | See detailed analysis below. |

---

## Detailed Analysis of Flagged Edges

### W1: `petyr-baelish COMMANDS_IN murder-of-jon-arryn` — Upgrade/Retirement Verdict

**Recommendation: CONFIRM the COMMANDS_IN. RETIRE the co-existing `petyr-baelish SUSPECTED_OF murder-of-jon-arryn`.**

**Reasoning:**

The text at asos-sansa-07 line 287 is a first-person confession from Lysa to LF, in his presence, not mediated by any narrator filter:

> "You told me to put the tears in Jon's wine, and I did. For Robert, and for us!"

This is not in-world suspicion by a third party — it is Lysa naming LF as the order-giver directly to his face, in real time, in a scene where he does not deny it. In-universe, this is the closest the text gets to a direct admission: Lysa is the executor (captured as `lysa-arryn AGENT_IN murder-of-jon-arryn`), and LF is named as the one who ordered her to act.

`COMMANDS_IN` (an authoritative order from a principal to an executor, in the context of an event) is semantically correct and distinguishable from `SUSPECTED_OF` (in-world suspicion without confession). The confession removes the in-world epistemic uncertainty that `SUSPECTED_OF` encodes.

The graph currently has BOTH edges on the same quote. That is the problem: `SUSPECTED_OF` encodes "people think X did this, but it's unproven within the world." After Lysa's confession to LF himself, the in-world uncertainty collapses — for LF, not for the rest of Westeros. Since the graph models canonical knowledge (not POV-gated uncertainty), and Lysa's confession is on-page direct evidence rather than narrator inference, `COMMANDS_IN` supersedes `SUSPECTED_OF`.

**Action: retire `petyr-baelish SUSPECTED_OF murder-of-jon-arryn` in finalize.** The `cersei-lannister SUSPECTED_OF murder-of-jon-arryn` edge is entirely separate (based on Ned Stark's in-world suspicion in AGOT) and must NOT be touched.

---

### SP3: `wedding-of-petyr-baelish-and-lysa-arryn ENABLES death-of-lysa-arryn` — ENABLES vs CAUSES

**Verdict: CONFIRM as ENABLES.**

The proximate cause of Lysa's death is a chain: (snow-castle kiss) → (Lysa's jealous rage) → (Lysa attempts to throw Sansa through Moon Door) → (LF sees an opportunity) → (LF shoves Lysa). The human choice at the end of that chain is LF's, so CAUSES would be agency-collapse.

ENABLES is justified because the marriage is the structural precondition that:
1. Made LF Lysa's husband and Lord Protector — giving him both motive-to-remove and physical proximity/access to the Moon Door moment.
2. Gave LF the position from which the murder was both survivable (he has institutional control) and worthwhile (he inherits the protectorship).

Without the marriage, LF could not have credibly survived pushing Lysa through the Moon Door — he'd have had no authority, no ability to frame Marillion, no Nestor Royce to bribe. The wedding is a genuine structural precondition (ENABLES), not the immediate trigger (not CAUSES). This is correct as minted.

**Note flag (non-breaking):** The cited quote "My sweet silly jealous wife" (line 297) is the murder scene, not a precondition marker. It is verbatim and line-accurate (pre-checked), but the note's framing ("The proximate trigger is Lysa's jealous rage; the marriage is the precondition") is accurate analysis, even if the quote itself doesn't do that work directly. No change to edge type or direction needed.

---

### SC3: `robert-arryn WARD_OF petyr-baelish` qualifier `formal` — Qualifier verdict

**Verdict: ADJUST qualifier from `formal` to `de facto`.**

The cited text at affc-alayne-01 line 71 is: "Until your sixteenth name day, I rule the Eyrie." This is LF's statement of his Lord Protector authority over Sweetrobin's minority — but that is a regency/guardianship, not a feudal wardship in the classic sense.

A "formal" wardship in ASOIAF is typically a feudal arrangement where a lord explicitly takes a noble child into his household as ward (often with custody of lands). Here, Robert is not "given to ward" by anyone — he remains in his own castle (the Eyrie), in his own seat, with LF installed over him by virtue of Lysa's marriage. This is more accurately a **regency** or **de facto guardianship** — LF has the power of a ward-lord but the legal instrument is "Lord Protector" (a title Lysa granted), not a wardship instrument.

The graph has two WARD_OF edges for robert-arryn → petyr-baelish. The Bronze Yohn quote at line 219 ("I mean to take the boy with me to Runestone") is explicitly framed as the lords wanting to take Robert INTO ward (suggesting he is NOT currently under a formal ward arrangement but under LF's protectorship). A `de facto` or `protectorate` qualifier would be more accurate.

**Adjust qualifier to `de_facto` (or drop qualifier and add a note clarifying the Lord-Protector basis).**

---

### L6: `moon-door WIELDED_IN death-of-lysa-arryn` — artifact-as-instrument verdict

**Verdict: CONFIRM with note caveat.**

The Moon Door is the physical means of Lysa's death — she is shoved backward through it, and the 600-foot fall kills her. Treating it as an instrument artifact in WIELDED_IN is semantically defensible: it is not a conventional weapon, but it functions as the lethal means (analogous to a cliff or a drop — the Moon Door is what turns the shove into a death).

The cited quote (line 295: "Sansa crawled from the Moon Door on hands and knees") is the aftermath of Sansa's near-death — it establishes the Moon Door's role in the scene but does not itself describe Lysa's death. The actual Moon Door line for Lysa's death is at line 303 ("Lysa stumbled backward, her feet slipping on the wet marble. And then she was gone") which is after she is shoved through it. The pre-check cleared quote accuracy so this passes, but the quote chosen is for Sansa's perspective, not the actual fatal use.

**Semantic verdict:** WIELDED_IN is a defensible edge type for an architectural feature used as the locus of a killing. The Moon Door node gets its first outbound edge, which is high value. CONFIRM, but the finalize note should clarify that WIELDED_IN here means "environmental instrument" not "hand-held weapon."

---

### NM1 vs NM2 — Redundancy check

**Verdict: CONFIRM both as genuinely non-redundant.**

- **NM1** (`petyr-baelish DECEIVES nestor-royce` via staged Marillion confession): the mechanism is false belief — LF constructs a false account (Marillion-did-it) that Nestor comes to believe. This is epistemic deception.

- **NM2** (`petyr-baelish MANIPULATES nestor-royce` via_bribe, hereditary grant of Gates): the mechanism is inducement — LF offers a real benefit (hereditary hereditary keep) that buys Nestor's cooperation. As the text makes clear, Nestor is not wholly deceived about being bought ("I will not say I had not hoped for this") — he is motivated, not primarily misled. This is behavioral manipulation via incentive.

Two distinct instruments, two distinct edge types, same target. Non-redundant. Both CONFIRM.

---

### LC1: `petyr-baelish CONSPIRES_WITH lyn-corbray` — symmetric vs asymmetric

**Verdict: CONFIRM as CONSPIRES_WITH.**

affc-alayne-01 line 343: "With gold and boys and promises, of course." — LF explains that Corbray will feign implacable hostility in exchange for payment.

The question is whether CONSPIRES_WITH (symmetric covert collusion between knowing parties) is right, vs MANIPULATES (using someone who doesn't know they're being used). The text is decisive: Corbray is a **knowing paid agent** playing a scripted role — he knows the enmity is feigned. This is not manipulation of an unknowing person; it is a mutual conspiracy in which both parties know the arrangement.

CONSPIRES_WITH (symmetric covert collusion between aware parties) is exactly right. MANIPULATES would be wrong here (Corbray isn't being misled). CONFIRM.

The existing graph has `lyn-corbray OPPOSES petyr-baelish` (from affc-sansa-01 line 209, where the apparent hostility is on display) — that's the *performed* opposition, which is accurate to observers in-world. The new `petyr-baelish CONSPIRES_WITH lyn-corbray` is the *actual* relationship, hidden from observers. Both edges are correct and complementary, not redundant.

---

## Node Verdicts

| Node | Verdict | Rationale |
|------|---------|-----------|
| `death-of-lysa-arryn` | **CONFIRM** | POV-confirmed, series-significant event (the keystone of the Vale arc). Warrants its own event hub. Drives 2 outgoing CAUSES and 6 incoming role edges — exactly the kind of node that earns reification. |
| `sansa-adopts-the-alayne-stone-identity` | **CONFIRM** | The Alayne identity is the defining transformation of Sansa's AFFC arc. Having it as an event node with ENABLES incoming (from the smuggle) and AGENT_IN edges (LF + Sansa) is structurally clean. `alayne-stone` / `alayne-baelish` alias hygiene is important — the mint correctly notes that alayne-baelish is LF's MOTHER, not this persona; this node carries the Sansa persona. |
| `lords-declarant-confront-littlefinger` | **CONFIRM** | A distinct, datable in-chapter incident with named participants, specific outcomes (one-year reprieve, Nestor's defection visible), and multiple PARTICIPATES_IN edges. It is not merely a wiki background fact — it is a dramatic scene spanning affc-alayne-01. Warrants reification. The faction node `lords-declarant` gets its primary outbound edge cluster from this. |

---

## Theory Leakage Check

No theory leakage detected. The following were correctly excluded:
- **Sweetsleep / Sweetrobin slow poisoning** (gated reading; text frames LF's "pinch of sweetsleep" instruction at affc-alayne-01 line 87 as a calming measure, not a confirmed murder plot; left as ## Quotes / harvest only — correct).
- **LF-as-Sansa's-future-husband speculation** — not asserted.
- **Lysa's death as pre-planned from the wedding** — the ENABLES edge correctly stops at precondition and does not assert premeditation.

---

## Agency-Collapse Check

No agency-collapse violations detected in the minted edges. Specific verifications:
- SP3 uses ENABLES (not CAUSES) for wedding → death, correctly routing through the human-choice trigger.
- W5 uses ENABLES for murder-of-jon-arryn → Lysa's accusation (Lysa's choice to write the letter is the proximate cause, so ENABLES is right).
- SP4 uses CAUSES for death → Nestor hearing: the hearing is directly and mechanically caused by the death creating a crime to investigate, with no substantial free-choice step in between. CAUSES is acceptable here.

---

## SUMMARY

**34 edges: 30 CONFIRM / 3 ADJUST / 0 REJECT**
**3 nodes: 3 CONFIRM / 0 REJECT**

### Adjustments (3)

1. **SP3** (wedding ENABLES death-of-lysa): edge type CONFIRM as ENABLES; **note only** — the cited quote ("My sweet silly jealous wife," line 297) is from the murder scene, not the precondition event. The analytical note is accurate, but the quote doesn't directly establish the precondition. No schema change; annotate in finalize.

2. **L6** (moon-door WIELDED_IN death-of-lysa): CONFIRM the edge; the cited quote (line 295, Sansa's aftermath crawl) is chronologically before the shove but quotes the Moon Door scene. Add a finalize note clarifying that WIELDED_IN = environmental instrument, not hand-held weapon.

3. **SC3** (robert-arryn WARD_OF petyr-baelish, qualifier `formal`): **change qualifier from `formal` to `de_facto`** — LF's authority is the Lord Protector regency granted by Lysa, not a feudal wardship instrument. "Formal" over-implies a deed of wardship that doesn't exist in the text.

### W1 retirement recommendation

**RETIRE `petyr-baelish SUSPECTED_OF murder-of-jon-arryn`.** The Lysa confession at line 287 (already cited on both edges) removes the in-world epistemic uncertainty that `SUSPECTED_OF` encodes. `COMMANDS_IN` on the same evidence is the correct upgrade — Lysa names LF as the order-giver to his face, and he does not deny it. Keeping both edges on the same quote is logically incoherent: the source that would sustain SUSPECTED_OF is the same source that makes COMMANDS_IN warranted.

The `cersei-lannister SUSPECTED_OF murder-of-jon-arryn` edge (AGOT provenance, different quote) is **not touched** — it encodes Ned Stark's in-world suspicion before any confession existed.

### No rejections

All 34 edges survived. The pre-synthesis dropped list (candidates.json `dropped_at_synthesis`) correctly excluded the genuinely problematic candidates (agency-circular events, over-distal seams, theory-gated readings, MANIPULATES Sansa semantic mis-fit). The mint is clean.
