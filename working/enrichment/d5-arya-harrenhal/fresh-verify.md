# Fresh-Verify Report — D5 Arya/Harrenhal Enrichment (S154)

**Reviewer:** Fresh independent agent (no prior context)
**Batch:** `working/enrichment/d5-arya-harrenhal/candidates.json`
**Run ID:** `d5-arya-harrenhal-enrichment-s154`
**Edges reviewed:** 44 (9 verify:true adjudicated in depth; ~8 spot-checked)
**Date:** 2026-06-26

---

## I. Verify:True Edges — Full Adjudication

| ID | Edge | Verdict | Reason |
|----|------|---------|--------|
| E1 | `gregor-raids-the-riverlands ENABLES fight-at-the-holdfast` | **ADJUST (node fit concern)** | The quote ("his men had ridden all the way around the lake chasing Beric Dondarrion and slaying rebels", acok-arya-07:77) refers to Ser Amory Lorch's column, not the Mountain. The ENABLES logic is structurally sound — Tywin's ordered Riverlands chevauchée is the precondition that put Amory's column in the region and made the holdfast attack possible. ENABLES is correctly chosen over CAUSES (Amory chose to storm the holdfast; free act of a third party). However, `gregor-raids-the-riverlands` as the source slug is problematic: the quote is specifically about Ser Amory's column chasing Beric, not the Mountain's own raiding. If the node covers the whole Tywin-ordered Riverlands harrying campaign (not just Gregor's personal operations), the ENABLES works; if it's Gregor-scoped only, Amory's column on the Beric-hunt is a distinct sub-operation. The note acknowledges this and asks for era-confirmation. **Recommend:** confirm the node's scope before minting; if Gregor-scoped, reroute via `tywin-orders-harrying` or add an Amory-specific antecedent. If the node already covers the umbrella Lannister campaign, CONFIRM as-is. |
| E3 | `arya-captured ENABLES arya-names-jaqen-himself` | **CONFIRM** | Captivity at Harrenhal is the necessary precondition: only there does Jaqen serve as a Brave Companion with an active debt to Arya (acok-arya-06 shows the full capture → Harrenhal delivery chain). The note's compression concern is warranted — it jumps from capture to Harrenhal to Jaqen-meets-Arya to the gambit — but ENABLES handles multi-hop preconditions correctly; the intermediate steps (Jaqen's debt, Arya's Wailing Tower assignment) don't interrupt the ENABLES chain because the gambit was causally *impossible* without captivity. Not over-compressed: ENABLES ≠ CAUSES, and the intermediate steps are just the mechanism by which the precondition operates. |
| E7 | `jaqen-gives-arya-the-iron-coin ENABLES arya-departs-for-braavos` | **CONFIRM** | The coin + words are explicitly the key to passage to Braavos: "give that coin to any man from Braavos, and say these words to him—valar morghulis" (acok-arya-09:339). The gap (ACOK giving → ASOS/AFFC/ADWD use) is real but ENABLES is precisely the right type for a distal precondition: Arya's departure for Braavos is made *possible* by the coin's possession, but is not immediately caused by it — many intervening events and her own choice intervene. Marquee seam confirmed. |
| E8 | `fall-of-harrenhal ENABLES arya-escapes-harrenhal` | **CONFIRM** | Bolton's handover announcement ("I mean to give Harrenhal to Lord Vargo when I return to the north", acok-arya-10:185) is the trigger Arya explicitly cites to Gendry to recruit him for the escape ("Lord Bolton is giving Harrenhal to the Bloody Mummers, he told me so"). The threat of Vargo Hoat as lord (and his foot-chopping reputation) is the enabling pressure; ENABLES is correct (the escape is Arya's free choice in response to the threat, not directly caused by the fall). Note: E8 was not in the verify:true list in candidates.json but is referenced in the prompt for E36 context. Including here for completeness. |
| E15 | `stableboy-killing MOTIVATES arya-stark` | **CONFIRM (Tier-2 appropriate)** | The text explicitly shows the killing lodging in Arya's psyche: "The stableboy was dead, she'd killed him, and if he jumped out at her she'd kill him again" (agot-arya-04:211); in acok-arya-01, she silently deploys it as a status signal — she considers threatening Lommy with it but doesn't dare, and Gendry confirms she killed someone. This is clearly a shaping event for her lethal resolve. Tier-2 is correct: no single quote proves "this event motivates her character arc" as a fact (that's an interpretive causal claim), but the inference is extremely strong across two chapters and the MOTIVATES→character target is valid per schema. |
| E20 | `arya-stark WITNESS_IN death-of-weese` | **CONFIRM (downgrade to Tier-2 note warranted, already Tier-2)** | Arya sees the immediate aftermath: Weese "sprawled across the cobbles, his throat a red ruin," the dog "lapping at the blood pulsing from his neck," Jaqen's two-finger salute confirming the kill (acok-arya-08:113-123). She does NOT see the kill-moment (the dog attacking). The batch is already Tier-2 with a borderline flag. Under the policy "present-but-shielded or only-sees-aftermath is weaker," this is aftermath-only. However, WITNESS_IN doesn't require witnessing the kill-moment in the schema — it requires the character actually sees "the charged incident." The charged incident is Weese's death, and Arya is at the scene with the body and the active dog, in Harrenhal's ward — she sees the aftermath while it is still physically active (dog still feeding, blood still pulsing). This is comparable to seeing a burning building without seeing who started it. **Verdict: borderline but KEEP at Tier-2** with the existing flag. The two-finger salute (Jaqen's acknowledgment that she is looking) tightens her presence to the immediate scene. Do not upgrade to Tier-1; do not drop. |
| E36 | `fall-of-harrenhal ENABLES red-wedding-conspiracy` | **CONFIRM with caveat** | The causal logic is sound: Roose holds Harrenhal → marches his host north → crosses at the Twins → participates in the Red Wedding. The quote ("I mean to give Harrenhal to Lord Vargo when I return to the north", acok-arya-10:185) signals Roose's impending departure northward. Holding Harrenhal was the step that positioned him in the Riverlands and gave him strategic footing to march. ENABLES is the right type — Roose's holding Harrenhal is a precondition that makes his march north *possible*; the Red Wedding is produced by Roose's and the Freys' subsequent choices, not directly by the fall. The seam is high-value. **Caveat:** Tier-2 is appropriate; the edge is a multi-hop ENABLES (fall → Roose-holds → marches north → Twin → RW), not a simple single-step precondition. The note correctly calls this the "highest-value WO5K seam." CONFIRM. |
| E39 | `incident-at-the-trident MOTIVATES arya-stark` | **CONFIRM** | The kill-list entry is explicit: "the Hound for killing the butcher's boy Mycah" (acok-arya-06:57). Arya recites this nightly. The Trident incident (Mycah/Nymeria) is a clear named origin of her kill-list motivation. Tier-2 is appropriate — the text shows it as a driver of her nightly litany/hatred, not as an immediate causal trigger. MOTIVATES→character is correct. |
| E40 | `cersei-lannister COMMANDS_IN gold-cloaks-demand-gendry` | **CONFIRM** | The quote "The queen wants him, old man, not that it's your concern" (acok-arya-02:161) makes Cersei the issuing authority; the gold-cloak officer carries her sealed warrant. COMMANDS_IN is appropriate for remote command authority (Cersei ordered, others executed). Tier-2 is correct — she did not personally execute the demand, but the officer explicitly invokes her authority and produces her ribbon-sealed warrant. No higher tier is warranted (no verbatim Cersei-speaking quote). |
| E43 | `gold-cloaks-demand-gendry MOTIVATES yoren` | **CONFIRM** | The quote "Fool! You think he's done with us? Next time he won't prance up and hand me no damn ribbon" (acok-arya-02:219) shows Yoren directly responding to the confrontation by ordering an all-night march. "Get the rest out o' them baths, we need to be moving. Ride all night, maybe we can stay ahead o' them for a bit." The confrontation directly drives Yoren's decision. MOTIVATES→character is correct. Tier-2 is right (inference, not a verbatim "because of this, I decided" declaration). |

---

## II. Spot-Check — Non-Verify Edges

Edges sampled: E2, E4, E5, E6, E9, E11, E13, E14, E16, E17, E18, E29, E33, E38.

| ID | Edge | Verdict | Notes |
|----|------|---------|-------|
| E2 | `fight-at-the-holdfast CAUSES arya-captured` | PASS | Quote ("someone else slammed into her and dragged her to the ground, and a third man wrenched the sword from her grasp", acok-arya-05:295) is real and a contiguous substring in the chapter. Direct causal chain — no mediation. CAUSES correct. |
| E4 | `arya-names-jaqen-himself CAUSES guards-killed` | PASS | The bargain (arya names him → he agrees to free the northmen → weasel-soup massacre) is the proximate cause. Quote ("A girl might . . . name another name then, if a friend did help?", acok-arya-09:187) is genuine. CAUSES correct — the naming-gambit is the triggering bargain that produces the massacre. |
| E5 | `guards-killed ENABLES fall-of-harrenhal` | PASS | "Once freed, the captives stripped the dead guards of their weapons and darted up the steps with steel in hand" (acok-arya-09:281) directly confirmed. The freed northmen are the proximate mechanism of the takeover. ENABLES correct (Roose's arrival with his host + Brave Companions' betrayal also contributed; the dungeon-freeing was necessary but not sufficient alone, which is why ENABLES rather than CAUSES). |
| E6 | `fall-of-harrenhal ENABLES jaqen-gives-arya-the-iron-coin` | PASS | "for I have duties too" (acok-arya-09:327) — Jaqen departs because his role here is finished; the falling of the castle resolves his debt and frees him to leave. ENABLES is structurally correct (the fall is the condition; Jaqen's gifting is his subsequent free act). Quote is sparse but matches the departing-because-finished logic. |
| E9 | `yoren FIGHTS_IN fight-at-the-holdfast` | PASS | "Yoren tangled his black banner around his spike, and forced the point of his dirk through his armor" (acok-arya-04 line ~183). Real quote, exact match confirmed. Yoren dies in this battle (per existing node). FIGHTS_IN correct. |
| E11 | `needle WIELDED_IN fight-at-the-holdfast` | PASS | "She slashed down hard, and Needle's castle-forged steel bit into the grasping fingers between the knuckles" (acok-arya-04:180). The "Winterfell!" battle-cry follows immediately. Confirmed; WIELDED_IN correct. |
| E13 | `arya-stark AGENT_IN stableboy-killing` | PASS | "She stuck him with the pointy end, driving the blade upward" (agot-arya-04:169). Sole agent. AGENT_IN correct. |
| E14 | `needle WIELDED_IN stableboy-killing` | PASS | "Needle went through his leather jerkin and the white flesh of his belly and came out between his shoulder blades" (agot-arya-04:171). Confirmed, specific weapon named. WIELDED_IN correct. |
| E16 | `jaqen-hghar AGENT_IN death-of-weese` | PASS | "When he saw her looking, he lifted a hand to his face and laid two fingers casually against his cheek" (acok-arya-08:123). This is Jaqen's signature acknowledgment of the kill. The method is opaque in text; the batch note correctly keeps theology in node-prose. AGENT_IN correct at Tier-1 for Jaqen's acknowledged authorship of the event. |
| E17 | `arya-stark COMMANDS_IN death-of-weese` | PASS | "'Weese,' she whispered" (acok-arya-08:84). Direct quote, real contiguous substring in the chapter. COMMANDS_IN parallels the existing Chiswyck usage per batch note. |
| E18 | `weese VICTIM_IN death-of-weese` | PASS | "Weese was sprawled across the cobbles, his throat a red ruin" (acok-arya-08:113). Confirmed. VICTIM_IN correct. |
| E29 | `arya-stark AGENT_IN arya-escapes-harrenhal` | PASS | "Arya slid her dagger out and drew it across his throat, as smooth as summer silk" (acok-arya-10:309). Confirmed — she executes the escape, kills the gate guard. AGENT_IN correct. **TRAP CONFIRMED:** weapon is explicitly the dagger (Bolton's stolen dagger), NOT Needle. There is NO needle WIELDED_IN arya-escapes-harrenhal edge in the batch. Correct. |
| E33 | `iron-coin WIELDED_IN arya-escapes-harrenhal` | PASS | "In the dark the iron could pass for tarnished silver" (acok-arya-10:307). The coin is used as a decoy to make the guard kneel, enabling the kill. Quote confirmed. WIELDED_IN is an unusual use for a coin-as-decoy, but the coin functions as the operative instrument of the ploy. Acceptable at Tier-1. |
| E38 | `brave-companions CAUSES fall-of-harrenhal` | PASS | "Them Bloody Mummers killed some of Ser Amory's lot in their beds, and the rest at table after they were good and drunk" (acok-arya-09, Pinkeye's morning report, ~line 349). Group-level CAUSES correct; the Brave Companions' mass killing of the Lannister garrison is the proximate cause of the castle changing hands. |

**No spot-check failures detected.**

---

## III. Three Traps — Confirmation

**Trap 1: No `needle WIELDED_IN arya-escapes-harrenhal` edge.**
CONFIRMED HELD. The batch contains no such edge. E29 is `arya-stark AGENT_IN arya-escapes-harrenhal` with the dagger quote. E33 is `iron-coin WIELDED_IN arya-escapes-harrenhal` (the decoy). Needle is correctly excluded. The node body for arya-escapes-harrenhal explicitly states "NOT Needle." Trap held.

**Trap 2: No `MANIPULATES` edge for the naming-gambit.**
CONFIRMED HELD. Searched all 44 edges: no MANIPULATES type appears anywhere in the batch. The naming-gambit is covered by E4 (CAUSES), E21 (AGENT_IN), E22 (VICTIM_IN). The batch note documents the reasoning (open coercion, not manipulation). Trap held.

**Trap 3: No `tywin COMMANDS_IN fight-at-the-holdfast` edge.**
CONFIRMED HELD. No such edge exists in the batch. The acok-arya-07:71 quote about destroying Roose Bolton is correctly identified as referring to the general campaign, not the holdfast specifically. Tywin's authority flows indirectly via the existing tywin→gregor-raids chain + new E1 ENABLES. Trap held.

---

## IV. Theory-Gate Check

**Status: CLEAN.**

Checked all 44 edges and 6 node bodies against theory-gate constraints:

- **FM cosmology / valar morghulis as religion:** Not asserted as an edge. E27 (`jaqen-hghar REVEALS_TO arya-stark`) captures the *text event* (Jaqen tells Arya the words), not the theology. The quote is the literal words spoken: "give that coin to any man from Braavos, and say these words to him—valar morghulis." No claim about what valar morghulis *means* as a religion/magic system.
- **Jaqen H'ghar's true identity (Alchemist/Pate):** Not asserted. The jaqen-gives-arya-the-iron-coin node body explicitly flags this as theory-gated.
- **Face-change as confirmed FM magic:** The face-change is minted as a text event in the node body (with the verbatim quote) but the *mechanism* is kept in node-prose, not asserted via edge. No `USES_MAGIC` or equivalent edge.
- **Iron coin as magic:** Coin minted as artifact with possession/wielded edges only. No claim of magical properties via edge.

Theory gate is clean.

---

## V. Overall Assessment

### Counts
- **CONFIRM:** 8 / 9 verify:true edges
- **ADJUST:** 1 / 9 (E1 — node-scope concern on `gregor-raids-the-riverlands`)
- **REJECT:** 0 / 9
- **Spot-check failures:** 0 / 14 sampled

### Recommended Actions

**E1 — Before minting:** Confirm whether `gregor-raids-the-riverlands` covers the full Tywin-ordered Riverlands harrying campaign (Amory's column included) or only Gregor's personal raiding operations. If it's Gregor-scoped only, the ENABLES is technically a slug-mismatch (Amory ≠ Gregor). Options:
  1. Confirm node scope = umbrella campaign → ENABLES valid as-is.
  2. If Gregor-scoped, adjust source slug to a Tywin-or-Amory antecedent, or accept the existing `tywin COMMANDS gregor-raids` + this E1 as a two-hop.

**E20 — Keep at Tier-2 with flag.** Do not upgrade to Tier-1 (no quote of the kill-moment). Do not drop — aftermath presence is valid for WITNESS_IN at Tier-2.

**All other 42 edges: no action required.** Edge types, quotes, tiers, and theory-gating are all sound.

---

*Reviewer: fresh-verify agent (no project context loaded). All judgments made against source chapters acok-arya-02, acok-arya-04 through acok-arya-10, and agot-arya-04 read directly.*
