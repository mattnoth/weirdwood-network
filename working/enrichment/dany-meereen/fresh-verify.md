# Fresh-Verify: Dany/Meereen Enrichment Dip
Date: 2026-06-24
Verifier role: independent skeptic (did NOT propose these edges)

---

## B7 — `sons-of-the-harpy-insurgency` MOTIVATES `daenerys-targaryen` [tier-2]
Ref: adwd-daenerys-04.md:67

**ADJUST — narrow the target.**
The passage clearly supplies the motivating reasoning: Dany explicitly reasons that "if a husband could help end the slaughter, then she owed it to her dead to marry." The insurgency is the engine, the in-text motive is on the page. However, the target node `daenerys-targaryen` is an entity, not an action — MOTIVATES should point at an event node. Adjust target to `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` (the decision/action being motivated). The current wording reads as MOTIVATES the person, not the choice.

---

## B8 — `sons-of-the-harpy-insurgency` ENABLES `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` [tier-2]
Ref: adwd-daenerys-04.md:141

**CONFIRM.**
The 90-day peace condition is the structural precondition Dany sets: "Give me ninety days and ninety nights without a murder, and I will know that you are worthy of a throne." The insurgency (and Hizdahr's claimed ability to stop it) is literally the enabling bargain — no insurgency, no leverage for the peace-condition, no marriage. The causal chain is one step (insurgency → peace-condition → wedding), not over-distal. Tier-2 is appropriate.

---

## B9 — `hizdahr-zo-loraq` SUSPECTED_OF `sons-of-the-harpy-insurgency` [tier-2]
Ref: adwd-the-kingbreaker-01.md:277

**CONFIRM.**
Line 277: "Why would they do that if you were not one of them?" — Barristan's direct accusation that Hizdahr commanded the Sons. The question is put to Hizdahr's face; he does not answer. The text records genuine in-text suspicion of an unproven claim. The insurgency itself is not flatly proven to be Hizdahr's doing. SUSPECTED_OF is the correct edge type. Tier-2 is defensible (Barristan is a skilled observer, the argument is strong, but it is still suspicion not confirmation).

---

## B10 — `hizdahr-zo-loraq` SUSPECTED_OF `sons-of-the-harpy-kill-twenty-nine` [tier-2]
Ref: adwd-the-kingbreaker-01.md:277

**CONFIRM — and yes, retire the COMMANDS_IN edge.**
Same line: Barristan's "Why would they do that if you were not one of them?" is the basis for suspicion of command authority over the Sons' specific attacks. Hizdahr does not confess. The act is not proven. SUSPECTED_OF (tier-2) correctly models this.

Advisory on the existing `hizdahr COMMANDS_IN sons-of-the-harpy-kill-twenty-nine` (tier-3): that edge asserts proven command authority over a specific kill event, which is NOT supported by the text — it is exactly what Barristan is accusing but cannot prove. The tier-3 COMMANDS_IN should be RETIRED and replaced by this SUSPECTED_OF. Keeping both would let the graph simultaneously treat the act as suspected and commanded, which is contradictory. Retire the COMMANDS_IN.

---

## B11 — `poisoned-locusts` WIELDED_IN `drogon-returns-to-daznak-pit` [tier-2]
Ref: adwd-daenerys-09.md:109

**CONFIRM.**
The text at adwd-daenerys-09.md:109 places the bowl of honeyed locusts in the Daznak box ("Hizdahr had stocked their box with flagons of chilled wine and sweetwater … a big bowl of honeyed locusts"). Hizdahr urges Dany to try them (line 111); she declines. Strong Belwas eats them by the handful. The poisoned locusts are physically present and deployed at the Daznak pit event. WIELDED_IN is appropriate.

---

## B12 — `hizdahr-zo-loraq` SUSPECTED_OF `poisoned-locusts` [tier-2]
Ref: adwd-the-kingbreaker-01.md:257

**CONFIRM.**
Line 257: "You urged Her Grace to try the locusts but never tasted one yourself." Barristan directly confronts Hizdahr with this behavioral evidence. The in-text suspicion is explicit, the act is unproven (Hizdahr denies it, offers alternative explanation about hot spices). SUSPECTED_OF at tier-2 is correct.

---

## B13 — `sons-of-the-harpy` SUSPECTED_OF `poisoned-locusts` [tier-3]
Ref: adwd-the-queensguard-01.md:155

**CONFIRM.**
The confectioner (Hizdahr's) is revealed at line 155 to be a catspaw: "The Sons of the Harpy took his daughter and swore she would be returned unharmed once the queen was dead." The Sons coerced the confectioner to poison the queen; the confectioner is identified as the mechanism, the Sons as the principals. SUSPECTED_OF is appropriate because the catspaw chain is established by Skahaz's intelligence, not by a trial or confession from the Sons themselves. Tier-3 is defensible given it's one intelligence source (Skahaz, who has his own agenda against Hizdahr).

---

## B14 — `quentyn-martell` SUSPECTED_OF `poisoned-locusts` [tier-3]
Ref: adwd-the-discarded-knight-01.md:57

**REJECT.**
This is a misattribution. The passage at line 57 is Barristan entertaining the hypothesis that the locusts were meant to kill HIZDAHR (not Dany), and that a Dornish poisoner might have targeted Hizdahr so Dany would be free to take a Dornish husband. The text reads: "Who can say that the locusts were meant for Daenerys? It was the king's own box. What if he was meant to be the victim all along?"

Quentyn is not named as a suspect — the text floats an anonymous "Dornish poisoner" hypothesis. Quentyn's motive would be to free Dany from Hizdahr, not to poison Dany. The edge `quentyn-martell SUSPECTED_OF poisoned-locusts` implies Quentyn was trying to poison Dany, which is the OPPOSITE of Barristan's thought. The passage should not be read as implicating Quentyn in the poisoning of Dany. REJECT. If anything, the Barristan passage supports a hypothetical that Hizdahr was the intended target, which is a different claim entirely (and still purely speculative, not graphable without a separate event node for a Dornish-plot-against-Hizdahr hypothesis).

---

## B16 — `daenerys-targaryen` VICTIM_IN `poisoned-locusts` [tier-2]
Ref: adwd-the-queens-hand-01.md:295

**CONFIRM.**
Line 295: "In return he gave her poisoned locusts." This is Barristan's framing of Hizdahr's action. The intended target is clearly Dany. The fact that she did not eat them (Belwas ate them instead) does not negate that she was the intended victim. VICTIM_IN correctly captures intended victimhood. Tier-2 is appropriate given the strong circumstantial case in the text.

---

## D1 — `doran-reveals-fire-and-blood-pact` MOTIVATES `quentyn-orders-the-attack` [tier-1]
Ref: adwd-the-spurned-suitor-01.md:71

**ADJUST — tier down to tier-2.**
The in-text motive is clear: "This is what I have to do. For Dorne. For my father." The fire-and-blood pact is Quentyn's stated reason for coming to Meereen, and now that the marriage route is foreclosed, the pact's obligation drives him to attempt dragon-theft. The MOTIVATES relationship is textually sound. However, tier-1 implies verified-canon certainty. Quentyn says "for Dorne, for my father" but does not explicitly say "the pact requires me to steal a dragon" — he is generalizing from the mission mandate. The causal link from the specific pact-reveal to the specific dragon-theft decision is slightly inferential. Tier-2 is more defensible.

---

## D2 — `dany-mounts-drogon-and-flees-meereen` ENABLES `quentyn-orders-the-attack` [tier-2]
Ref: adwd-the-spurned-suitor-01.md:127

**CONFIRM.**
Timeline check: adwd-the-spurned-suitor-01.md is chapter 68 (Quentyn's second POV), and adwd-the-dragontamer-01.md (chapter 69) is when the attack happens. The Spurned Suitor chapter shows Quentyn AFTER Dany has fled, negotiating with the Tattered Prince. Line 127: "Your bride flew off on a dragon." The Tattered Prince explicitly names Dany's flight as the reason the marriage plan collapsed. The attack attempt (adwd-the-dragontamer-01.md) comes in the very next chapter. The temporal order is correct: Dany flees → marriage foreclosed → Quentyn seeks dragon-theft as alternative → attack. ENABLES is the right edge type. Tier-2 is correct.

---

## D4 — `dragon-hatching-on-drogo-pyre` ENABLES `fall-of-astapor` [tier-2]
Ref: asos-daenerys-01.md:257

**ADJUST — ENABLES is defensible but the cited line does not support it directly; flag the causal chain length.**
The cited line (asos-daenerys-01.md:257) is Jorah advising that "Dragons will be as great a wonder in Astapor as they were in Qarth" — it predicts that the dragons will open doors at Astapor, which is the advisor's speculation pre-Astapor, not a post-hoc confirmation. The chain is: dragon-hatching → dragons exist → dragons used as leverage/payment for Unsullied → Unsullied + dragons take Astapor. This is agency-collapse risk: the pyre hatching is distal (three steps removed from the fall). However, the causal chain is unbroken and explicitly laid out in the text (the Astapor arc). If no intermediate event nodes exist for the Unsullied purchase, ENABLES is an acceptable compressed edge. Recommend noting the intermediate steps in evidence notes. Tier-2 is fine, but consider whether `dragon-hatching-on-drogo-pyre ENABLES unsullied-purchase` and `unsullied-purchase ENABLES fall-of-astapor` would be more precise if those event nodes exist.

---

## D5 — `dany-mounts-drogon-and-flees-meereen` CAUSES `second-siege-of-meereen` [tier-2]
Ref: adwd-the-queensguard-01.md:159

**ADJUST — CAUSES is too strong; prefer ENABLES or TRIGGERS.**
The line at 159 is Skahaz explaining: "Daenerys gone, Yurkhaz dead. In place of one old lion, a pack of jackals. Bloodbeard … that one has no taste for peace. And there is more. Worse. Volantis has launched its fleet against us." This is strong evidence that Dany's flight destabilized the peace and removed the deterrent. However, the Volantene fleet is named as an additional cause, and Yurkhaz's death (caused by the dragon's appearance at Daznak) is equally part of the destabilization. Dany's flight is a necessary but not sufficient cause. CAUSES implies tight proximate causation; TRIGGERS or ENABLES would better fit a contributing/unlocking cause among several. Adjust edge type to TRIGGERS. Tier-2 is fine.

---

## C_qf1 — `quaithe` FORESHADOWS `dany-mounts-drogon-and-flees-meereen` [tier-2]
Ref: adwd-daenerys-02.md:139

**ADJUST — tier down to tier-3.**
The line: "Soon comes the pale mare, and after her the others. Kraken and dark flame, lion and griffin, the sun's son and the mummer's dragon." The "pale mare" is the flux epidemic spreading from Astapor (confirmed by the text). The "others" are a list of threats/visitors. Dany's flight on Drogon is not directly named in this prophecy — the phrase "dark flame" might retroactively fit (Drogon is described as black and red), but this requires interpretation. The prophecy foreshadows threats and arrivals in Meereen generally; mapping it specifically to Dany's flight on Drogon requires inferential work. Tier-2 implies strong prophetic pointing; this is more ambient/interpretive. Tier-3 is more honest. Keep FORESHADOWS, adjust tier to 3.

---

## C_qf2 — `quaithe` FORESHADOWS `second-siege-of-meereen` [tier-3]
Ref: adwd-daenerys-02.md:139 — same quote

**ADJUST — "the others" reading is partially supported but requires clarification.**
"After her the others. Kraken and dark flame, lion and griffin, the sun's son and the mummer's dragon." Skahaz at adwd-the-queensguard-01.md:159-161 confirms Volantis has launched its fleet — Volantis has lion symbolism (the Volantene fleet). "Kraken" could read as the Ironborn. The list in the prophecy does seem to enumerate threats that converge on Meereen. FORESHADOWS at tier-3 is acceptable, but the edge should note that "the others" is the basis for the second-siege reading, and it is the weakest prophetic link in the set — multiple entities are named and the mapping to the specific event node `second-siege-of-meereen` is an editorial choice. CONFIRM the edge exists at tier-3, but flag the interpretive dependency in evidence notes. No change needed.

**CONFIRM at tier-3** (as proposed).

---

## A_grkb — `groleo` KILLED_BY `yunkai` [tier-1]
Ref: adwd-the-discarded-knight-01.md:65

**ADJUST — killer is Bloodbeard (a sellsword captain), not Yunkai directly; edge target is defensible but slightly imprecise.**
Bloodbeard is a sellsword in the employ of Yunkai — he delivers Groleo's severed head as a hostage reprisal. The Yunkai'i council of masters ordered the hostage execution ("Blood must pay for blood") per the parchment read aloud at line 83. Bloodbeard is the proximate killer, Yunkai the ordering authority. KILLED_BY `yunkai` is organizationally correct (Yunkai ordered and authorized it) but a more precise graph would have `groleo KILLED_BY bloodbeard` plus `bloodbeard ACTS_FOR yunkai` or similar. If `bloodbeard` has no node yet, KILLED_BY `yunkai` at tier-1 is acceptable as a compressed attribution. Recommend noting Bloodbeard as the proximate actor in evidence_quote. Tier-1 is correct (this is unambiguous canon).

---

## Summary

| ID | Verdict | Issue |
|----|---------|-------|
| B7 | ADJUST | Target should be the event node (wedding), not the person |
| B8 | CONFIRM | — |
| B9 | CONFIRM | — |
| B10 | CONFIRM + advisory | Retire the existing tier-3 COMMANDS_IN edge |
| B11 | CONFIRM | — |
| B12 | CONFIRM | — |
| B13 | CONFIRM | — |
| B14 | REJECT | Misattribution — passage implicates Dornish plot against Hizdahr, not Quentyn poisoning Dany |
| B16 | CONFIRM | — |
| D1 | ADJUST | Tier-1 → tier-2 (explicit motive but slight inferential step to dragon-theft specifically) |
| D2 | CONFIRM | Timeline verified correct |
| D4 | ADJUST | Note causal chain length; consider intermediate event nodes if they exist |
| D5 | ADJUST | CAUSES → TRIGGERS (contributing cause among several, not sole proximate) |
| C_qf1 | ADJUST | Tier-2 → tier-3 (Drogon-flight mapping requires interpretation) |
| C_qf2 | CONFIRM | tier-3 as proposed; note interpretive dependency in evidence |
| A_grkb | ADJUST | Note Bloodbeard as proximate killer; KILLED_BY yunkai is acceptable compressed attribution |

**Counts:** 8 CONFIRM / 7 ADJUST / 1 REJECT

**Not-clean CONFIRMs:** B7, B10 (advisory), B14, D1, D4, D5, C_qf1, A_grkb
