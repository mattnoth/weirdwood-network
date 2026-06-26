# Fresh-Verify: S151 Cheap-L2 Enrichment
**Reviewer:** fresh-verify subagent (adversarial, did not propose)
**Date:** 2026-06-26
**Scope:** interpretive / causal / gated edges + 4 new nodes
**Local cache only** — no web fetches

---

## Edge Verdict Table

| edge_id | verdict | reason | recommended change |
|---------|---------|--------|--------------------|
| B1-A6 | CONFIRM | adwd-davos-04 line 175: Manderly explicitly pledges heavy horse, warships, and allegiance east of the White Knife *if* Stannis is king — "I can deliver King Stannis the allegiance of all the lands east of the White Knife." The conspiracy is the political structure that makes that delivery possible. ENABLES (not CAUSES) is the right edge; Stannis's decision to march is independent, but northern support is a genuine enabling condition. T2 correct. | None. |
| B1-A7 | CONFIRM | The pie-vengeance is explicitly narrated inside the same chapter (adwd-the-prince-of-winterfell-01) as the conspiracy's reprisal in action: same actors (Manderly), same watchword ("the North remembers"), same anti-Frey motive. SUB_BEAT_OF captures a meaningful, on-page subordinate relation — the pies are *one step* inside the broader deception strategy, not merely thematic adjacency. T2 appropriate (the pies' content is implied, not confirmed). | None. |
| B1-A9 | CONFIRM | T2 is the correct tier and the note is clear: "never textually confirmed." adwd-a-ghost-in-winterfell-01 line 89 confirms the three Freys' names (Rhaegar, Jared, Symond) and that they were Manderly's guests and then vanished. The chapter does NOT textually confirm they are in the pies; it only confirms Manderly's contempt and their absence. VICTIM_IN at T2 with note encodes the strong-implication-only reading correctly. Keep all three — dropping them would erase a graph-navigable lead for the theory. | None. Drop would be over-correction. |
| B1-A10 | CONFIRM | Same rationale as B1-A9. | None. |
| B1-A11 | CONFIRM | Same rationale as B1-A9. | None. |
| B2-E06 | ADJUST | affc-cersei-10 line 307-309 CONTRADICTS the edge as stated. Qyburn says "your champion stands ready … there is no man in all the Seven Kingdoms who can hope to stand against him" — but Cersei's *immediate* response is "I have a champion no man can defeat, but **I am forbidden to make use of him**." She **cannot** demand trial by combat for herself under the Faith's rules (only a Sworn Brother of the Kingsguard can serve as a queen's champion, and Robert Strong is not yet a Sworn Brother at this narrative moment). The creation of Robert Strong does NOT enable Cersei's trial-by-combat decision in affc-cersei-10; it enables it in ADWD (after Strong is inducted into the Kingsguard per adwd-cersei-02). The target event slug `cersei-resolves-on-trial-by-combat` must refer to her later ADWD decision, not the affc-cersei-10 moment where she is explicitly blocked. If the target event is the ADWD resolution, the chapter cite is wrong (should be adwd-cersei-02, not affc-cersei-10), and the quote needs updating. | ADJUST: Change `"book": "affc", "chapter": "affc-cersei-10"` → `"book": "adwd", "chapter": "adwd-cersei-02"`. Update quote to Robert Strong's Kingsguard induction scene. Confirm the target event node is the ADWD trial-by-combat decision. If no separate ADWD resolution event exists, the edge may need to hold until that event is minted. |
| B3-E7 | CONFIRM | affc-brienne-06 line 191: "The Hound died there, in my arms." is an explicit on-page disclosure by the Elder Brother to Brienne. It is a distinct factual claim from the other two REVEALS_TO edges (the first corrects Arya's identity, the second names Stranger as Sandor's horse). This edge captures only the death-report, not the persona-death vs person-death interpretation. It does NOT encode the gravedigger=Sandor inference — the Elder Brother's statement is ambiguous by design and the edge is evidence-only. CONFIRM. | None. |
| B4-E04 | CONFIRM | agot-eddard-15 lines 135-157: Varys provides (a) intelligence on daughters, (b) the Wall-offer bargain, (c) the Sansa's-head ultimatum ("The choice, my dear lord Hand, is entirely yours."). This is clearly the proximate cause of Ned's confession — the visit supplies the terms, the threat, and the only path forward Ned can see. ENABLES is the correct framing (Ned retains formal choice; Varys does not physically force the confession). T1. | None. |
| B4-E05 | ADJUST | `via_threat` is accurate for the closing ultimatum (Sansa's head), confirmed on-page. However, Varys's operation in this chapter is a compound of false information (the Wall-promise is either sincere or a manipulation; Ned's fate reveals it was the latter) AND emotional manipulation (invoking Rhaenys, invoking Jon) AND the explicit threat. The qualifier `via_threat` captures the closing move but not the full manipulation. More importantly, the existing `varys DECEIVES eddard-stark` (S137, agot-eddard-15, T2) does cover the deception dimension. This MANIPULATES edge is usefully distinct (MANIPULATES ≠ DECEIVES — MANIPULATES is coercive pressure on a live actor, not false information). `via_threat` is the *dominant* qualifier for this chapter and correctly distinguishes this edge from the DECEIVES edge. CONFIRM the edge; ADJUST the note to acknowledge the compound method. | ADJUST note only: add "compound method: Sansa-head ultimatum (dominant) + emotional pressure (Rhaenys story). The distinct false-promise (Wall-offer) is already captured in the existing varys DECEIVES eddard-stark edge (S137)." No edge_type or qualifier change needed — via_threat is defensible as the dominant mode. |
| B4-E06 | CONFIRM | agot-eddard-15 line 75: "Your older girl is still betrothed to Joffrey. Cersei keeps her close … The younger girl escaped Ser Meryn and fled. I have not been able to find her." This is a factual intelligence disclosure — not a deception (Varys gives Ned true information here). Distinct from the existing DECEIVES edge (which captures Varys's pretense of serving Ned). T2 is right because Varys's motives for sharing this information remain ambiguous (steering Ned to confess vs. genuine care). | None. |
| B7-01 | CONFIRM | asos-jaime-05 line 63: "Then I slew Aerys, before he could find someone else to carry his message to the pyromancers." The text is explicit: Jaime killed Aerys *in order to stop the burn-message reaching the pyromancers*. He already killed Rossart (the pyromancer carrying out the order) first. The wildfire did not burn. PREVENTS is the correct edge type — the action halted the causal chain. T1. | None. |

---

## Gated-Boundary Audit

### 1. Robert Strong IS Gregor — PASS

The `creation-of-robert-strong.node.md` explicitly gates the identity claim:

> "**Gated identity (NOT asserted in the graph):** the books strongly imply but never confirm that Robert Strong is the reanimated Gregor … Per the theories-track gate, the `gregor-clegane` and `robert-strong` nodes stay **separate** — this event encodes the structural relationship … WITHOUT a `SAME_AS`/`RESURRECTS` identity edge."

No SAME_AS or RESURRECTS edge exists in the candidate set between gregor-clegane and robert-strong. The node aliases also do not equate them. **PASS.**

### 2. The gravedigger IS Sandor — PASS

The B3 edges (B3-E1, B3-E2, B3-E4, B3-E6, B3-E7) are all scoped to the node `gravedigger` or the horse `stranger-horse` with LOCATED_AT / HEALS / ENCOUNTERS / REVEALS_TO edges. No identity edge (SAME_AS) is asserted between `gravedigger` and `sandor-clegane`. The Elder Brother's death-account (B3-E7) is encoded as a REVEALS_TO edge — what the Elder Brother says, not what is true about identity. **PASS.**

### 3. Frey pies contain Freys — PASS

The `manderly-bakes-the-frey-pies.node.md` is correctly framed:

> "The implication (universally read, never textually confirmed) is that the three missing Freys are in the pies."

All three VICTIM_IN edges (B1-A9/A10/A11) carry `"tier": 2` and notes reading "Strong implication … never textually confirmed." No edge asserts confirmation. **PASS.**

---

## Drops / Adjusts to Apply in Finalize

**B2-E06 — ADJUST (substantive):**
The edge `creation-of-robert-strong ENABLES cersei-resolves-on-trial-by-combat` cites `affc-cersei-10` and quotes Qyburn saying "your champion stands ready." But affc-cersei-10 shows Cersei explicitly cannot use Robert Strong yet — he is not a Kingsguard sworn brother at that moment. The creation of Robert Strong enables Cersei's trial-by-combat only after he is inducted into the Kingsguard in ADWD.
- Change `book` → `adwd`; `chapter` → `adwd-cersei-02`
- Update `quote` to the Kingsguard-induction scene
- Confirm `cersei-resolves-on-trial-by-combat` is the ADWD decision node (if it is AFFC only, the target event slug itself needs clarification or a new event node)

**B4-E05 — ADJUST (note only, no verdict change):**
Add to `note`: "Varys's compound method: Sansa-head ultimatum (dominant / on-page T1) + emotional pressure (Rhaenys story). The false-promise dimension (Wall-offer) is already encoded in the existing varys DECEIVES eddard-stark edge (S137, T2). via_threat is the dominant and distinguishing qualifier for this edge."

---

## Summary Tally

| Verdict | Count | Edge IDs |
|---------|-------|----------|
| CONFIRM | 8 | B1-A6, B1-A7, B1-A9, B1-A10, B1-A11, B3-E7, B4-E04, B4-E06, B7-01 |
| ADJUST  | 2 | B2-E06 (substantive: wrong chapter cite), B4-E05 (note clarification only) |
| REJECT  | 0 | — |

**Gated-boundary: PASS × 3** (Robert Strong identity, gravedigger identity, Frey pie content — all correctly gated in node prose and edges).

**Critical issue for finalize:** B2-E06's chapter cite is wrong and the edge logic is inverted at the cited moment — Cersei is *blocked* from using Robert Strong in affc-cersei-10, not enabled. Must resolve to the ADWD Kingsguard-induction cite before shipping.
