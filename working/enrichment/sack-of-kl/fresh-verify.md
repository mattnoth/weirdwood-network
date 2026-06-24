# Fresh Verification — Sack of King's Landing Enrichment Dip
Generated: 2026-06-24 | Verifier: independent adversarial pass

---

## Edge 1
**wildfire-plot --[ENABLES]--> aerys-commands-the-city-burned | T1 | asos-jaime-05.md:53**

Checked line 53: "So His Grace commanded his alchemists to place caches of wildfire all over King's Landing." The caches were placed in order to execute the burn-order. The burn-order is only executable because the caches exist. ENABLES (partial precondition) is the correct type — the wildfire placement is the literal material precondition that makes Aerys's order actionable.

Line checked: asos-jaime-05.md:53 — verbatim support confirmed.

**VERDICT: CONFIRM**

---

## Edge 2
**belis --[AGENT_IN]--> wildfire-plot | T1 | asos-jaime-05.md:55**

Checked line 55: "with Rossart, Belis, and Garigus coming and going night and day" + "Everything was done in the utmost secrecy by a handful of master pyromancers." Belis is named as one of the three master pyromancers executing the cache-placement.

Line checked: asos-jaime-05.md:55 — verbatim support confirmed.

**VERDICT: CONFIRM**

---

## Edge 3
**garigus --[AGENT_IN]--> wildfire-plot | T1 | asos-jaime-05.md:55**

Same passage as Edge 2. Garigus named alongside Rossart and Belis as master pyromancers placing caches.

Line checked: asos-jaime-05.md:55 — verbatim support confirmed.

**VERDICT: CONFIRM**

---

## Edge 4
**qarlton-chelsted --[VICTIM_IN]--> wildfire-plot | T1 | asos-jaime-05.md:55**

Checked line 55: "He did all he could to dissuade him... When that failed he took off his chain of office and flung it down on the floor. Aerys burnt him alive for that." Chelsted opposed the plot and was killed because of it. VICTIM_IN is defensible — he was harmed as a direct consequence of the wildfire plot (specifically his opposition to it). The cite covers both his role as opponent and his fate.

Note: Chelsted's first name "Qarlton" is not stated in this passage; it's established elsewhere. The slug should be verifiable from wiki/other sources. Not flagging this as a text issue — the surname "Chelsted" is verbatim in the cite.

Line checked: asos-jaime-05.md:55 — verbatim support confirmed.

**VERDICT: CONFIRM**

---

## Edge 5
**aerys-ii-targaryen --[KILLS]--> qarlton-chelsted | T1 | asos-jaime-05.md:55**

Checked line 55: "Aerys burnt him alive for that." Clear and direct. Aerys is the agent; Chelsted is the victim; the method is burning alive. T1 is correct.

Line checked: asos-jaime-05.md:55 — verbatim support confirmed.

**VERDICT: CONFIRM**

---

## Edge 6
**jaime-lannister --[KILLS]--> belis | T1 | asos-jaime-05.md:63**

Checked line 63: "Days later, I hunted down the others and slew them as well. Belis offered me gold, and Garigus wept for mercy." "Slew them" = killed both Belis and Garigus. Belis is confirmed dead by Jaime's hand.

Line checked: asos-jaime-05.md:63 — verbatim support confirmed.

**VERDICT: CONFIRM**

---

## Edge 7
**jaime-lannister --[KILLS]--> garigus | T1 | asos-jaime-05.md:63**

Same passage as Edge 6. Garigus explicitly named: "Garigus wept for mercy. Well, a sword's more merciful than fire, but I don't think Garigus much appreciated the kindness I showed him." Confirms Garigus killed.

Line checked: asos-jaime-05.md:63 — verbatim support confirmed.

**VERDICT: CONFIRM**

---

## Edge 8
**roland-crakehall --[WITNESS_IN]--> slaying-of-aerys-ii-the-kingslaying | T1 | asos-jaime-02.md:297**

Checked line 297: "Ser Elys Westerling and Lord Crakehall and others of his father's knights burst into the hall in time to see the last of it." "The last of it" refers to Jaime's killing of Aerys — they arrived in time to witness the killing's conclusion. Line 299 then names him: "Roland Crakehall told him." This passes the WITNESS_IN gate — physically present and perceiving the event (even if only the final moment). T1 is defensible.

Caveat: "the last of it" could mean they saw Jaime standing over the dying/dead king, not the killing stroke itself. But that is still witnessing the event. Standard WITNESS_IN requires "present + perceiving" not "saw the blow land."

Line checked: asos-jaime-02.md:297 — verbatim support confirmed. "Roland" confirmed at line 299.

**VERDICT: CONFIRM**

---

## Edge 9
**tywin-presents-bodies-to-robert --[SUB_BEAT_OF]--> sack-of-kings-landing | T1 | asos-tyrion-06.md:187**

Checked line 187: "We had come late to Robert's cause. It was necessary to demonstrate our loyalty. When I laid those bodies before the throne, no man could doubt that we had forsaken House Targaryen forever." The bodies-presentation is framed by Tywin as part of demonstrating loyalty in the context of the Sack. It is an immediate aftermath action, part of the Sack's event cluster. SUB_BEAT_OF is appropriate.

Line checked: asos-tyrion-06.md:187 — verbatim support confirmed.

**VERDICT: CONFIRM**

---

## Edge 10
**tywin-lannister --[AGENT_IN]--> tywin-presents-bodies-to-robert | T1 | asos-tyrion-06.md:187**

Checked line 187: "When I laid those bodies before the throne..." Tywin speaking in first person. Direct agency, T1 confirmed.

Line checked: asos-tyrion-06.md:187 — verbatim support confirmed.

**VERDICT: CONFIRM**

---

## Edge 11
**robert-baratheon --[WITNESS_IN]--> tywin-presents-bodies-to-robert | T1 | agot-eddard-02.md:71**

Checked line 71: "He remembered the angry words they had exchanged when Tywin Lannister had presented Robert with the corpses of Rhaegar's wife and children as a token of fealty." This passage establishes Robert was the *recipient* — "presented Robert with the corpses" — meaning Robert was present when the bodies were laid before the throne. WITNESS_IN (present + perceiving) applies.

Claim "condoned" is not strictly supported by the quote — Robert and Ned *exchanged angry words* about it; Robert called it "war" not murder. Robert accepted it politically, but "condoned" overstates. The edge claim says "received+condoned" — the cite doesn't support "condoned." However, the edge type is WITNESS_IN, not CONDONES, so the edge itself is sound; the claim annotation is loose but doesn't corrupt the edge.

Line checked: agot-eddard-02.md:71 — verbatim support confirmed for WITNESS_IN. The word "condoned" in the claim description is imprecise but the edge type is correct.

**VERDICT: CONFIRM** (note: edge description's "condoned" is editorial overreach, but the WITNESS_IN type+target+tier are all correct)

---

## Edge 12
**tywin-presents-bodies-to-robert --[ENABLES]--> coronation-of-robert-i-baratheon | T2 | asos-tyrion-06.md:187**

Checked line 187: "It was necessary to demonstrate our loyalty. When I laid those bodies before the throne, no man could doubt that we had forsaken House Targaryen forever. And Robert's relief was palpable. As stupid as he was, even he knew that Rhaegar's children had to die if his throne was ever to be secure."

The ENABLES claim: Tywin's loyalty-demonstration "removed the barrier to a secure coronation." The text says it demonstrated Lannister loyalty and that Robert's relief was palpable — but it does not say this was a precondition for the *coronation itself*. The coronation followed the Sack; the bodies-presentation is one early event after the Sack. The causal link from bodies-presentation to coronation is Tywin's own rationalization for the murders, not a narrative statement that the coronation required this act.

Two problems:
1. **Over-distal:** The text supports ENABLES/MOTIVATES at best a secured alliance, not specifically the coronation event node.
2. **Redundancy risk:** If `sack-of-kings-landing --[CAUSES]--> coronation-of-robert-i-baratheon` already exists, this ENABLES from a sub-beat adds very little and creates a redundant causal path at T2.
3. **Agency confusion:** Tywin's self-serving framing ("It was necessary") is being treated as an objective causal fact. It's Tywin's interpretation that the murders were required; Robert's own quoted reaction ("I see no babes. Only dragonspawn") suggests he approved rather than that the murders unlocked his coronation.

The edge overclaims the causal mechanism. T2 is appropriate (it's an inference), but the edge type should be weaker than ENABLES.

**VERDICT: ADJUST** — change type from ENABLES to MOTIVATES (Tywin's framing is his stated motivation, not a mechanical precondition); or drop to T3 to reflect its interpretive nature. Alternatively consider replacing with `tywin-presents-bodies-to-robert --[SIGNALS_LOYALTY_TO]--> robert-baratheon` if that edge type exists, or reject entirely if `sack CAUSES coronation` already covers the causal chain.

---

## Edge 13
**jaime-found-seated-on-the-iron-throne --[SUB_BEAT_OF]--> slaying-of-aerys-ii-the-kingslaying | T1 | asos-jaime-02.md:303**

Checked line 303: "'Proclaim who you bloody well like,' he told Crakehall. Then he climbed the Iron Throne and seated himself with his sword across his knees, to see who would come to claim the kingdom. As it happened, it had been Eddard Stark."

This is the immediate aftermath of the killing — Jaime seats himself on the throne *after* slaying Aerys and Rossart. It is part of the same continuous scene. SUB_BEAT_OF the kingslaying is a reasonable modeling choice. The event is distinct from the killing itself but immediately follows and is narratively bound to it.

Line checked: asos-jaime-02.md:303 — verbatim support confirmed.

**VERDICT: CONFIRM**

---

## Edge 14
**jaime-lannister --[AGENT_IN]--> jaime-found-seated-on-the-iron-throne | T1 | asos-jaime-02.md:303**

Checked line 303: "he climbed the Iron Throne and seated himself." Jaime is the agent. T1 confirmed.

**VERDICT: CONFIRM**

---

## Edge 15
**eddard-stark --[WITNESS_IN]--> jaime-found-seated-on-the-iron-throne | T1 | agot-eddard-02.md:151**

Checked line 151: "Jaime wore the white cloak of the Kingsguard over his golden armor. I can see him still. Even his sword was gilded. He was seated on the Iron Throne, high above his knights, wearing a helm fashioned in the shape of a lion's head."

Ned explicitly describes seeing Jaime seated on the Iron Throne — he rode the length of the hall and stopped in front of the throne. Line 155 further confirms: "I stopped in front of the throne, looking up at him." This is unambiguously a WITNESS_IN: Ned was present, had direct visual perception of this event, and remembers it vividly.

Critical gate addressed: Ned did NOT witness the killing of Aerys (Aerys was already dead on the floor when Ned arrived — confirmed at line 151: "Aerys was dead on the floor"). But he DID witness this specific event node (jaime-found-seated-on-the-iron-throne), which is the correct target. The edge is correctly scoped to the throne-scene, not the killing.

Line checked: agot-eddard-02.md:151, 155 — verbatim support confirmed.

**VERDICT: CONFIRM**

---

## Edge 16
**jaime-found-seated-on-the-iron-throne --[LOCATED_AT]--> iron-throne | T1 | agot-eddard-02.md:151**

Checked line 151: "He was seated on the Iron Throne." Unambiguous location. T1 confirmed.

**VERDICT: CONFIRM**

---

## Edge 17
**wildfire-plot --[ENABLES]--> wildfire-trap-on-the-blackwater | T1 | acok-tyrion-11.md:107**

Checked acok-tyrion-11.md:107: "Another cache of Lord Rossart's was found, more than three hundred jars. Under the Dragonpit!" This confirms Rossart's surviving caches were discovered during Tyrion's tenure. Checked acok-tyrion-13.md:19: "He saw another of the hulks he'd stuffed full of King Aerys's fickle fruits engulfed by the hungry flames." This confirms Tyrion used the recovered Aerys-era wildfire at the Battle of the Blackwater.

The causal chain is: Aerys's wildfire-plot → caches placed → caches survive → Tyrion finds the Dragonpit cache → loads hulks → uses at Blackwater.

ENABLES is the correct type: the wildfire-plot created the material (caches) that Tyrion recovered and deployed. Without the original plot, there would be no Rossart caches to find. This is a genuine partial precondition, not mere correlation.

However, the T1 tier needs scrutiny. The causal link requires inference across ~15 years and two separate narrative threads. The text does NOT say "Tyrion used Aerys's caches at the Blackwater" in a single statement — it requires connecting the Dragonpit find (acok-tyrion-11:107) with the "King Aerys's fickle fruits" (acok-tyrion-13:19) and the wildfire-plot narrative (asos-jaime-05). This multi-step inference across chapters is T2, not T1. T1 requires a single unambiguous textual statement; this is a well-supported cross-chapter deduction.

**VERDICT: ADJUST** — drop tier from T1 to T2. The causal connection is real and the text strongly supports it, but it requires inference across two chapters in different books. The edge type (ENABLES) and targets are correct.

---

## Edge 18
**murder-of-elia-martell-and-rhaegars-children --[MOTIVATES]--> doran-reveals-fire-and-blood-pact | T2 | affc-the-princess-in-the-tower-01.md:325**

Checked line 325: "'Vengeance.' His voice was soft... 'Justice.' Prince Doran pressed the onyx dragon into her palm... and whispered, 'Fire and blood.'" This is Doran's reveal of the secret Targaryen pact to Arianne.

The claim is that the 283 AC murder of Elia and Rhaenys/Aegon is the deep motive behind this reveal. The text at line 325 does not name Elia or the murders — Doran says "Vengeance" and "Justice" without specifying target. The surrounding context (lines 321–325) is about Quentyn's mission to bring back "our heart's desire," which is established elsewhere to be a Targaryen alliance/restoration.

Two issues:
1. **Proximate vs. distal MOTIVATES:** The immediate context in this scene is that Arianne has just been captured after the failed Myrcella plot, and Doran is explaining the larger plan to her. The trigger for *this scene's reveal* is Arianne's capture collapsing his secret (he must explain now). The murder of Elia in 283 AC is the *root cause* of Doran's Targaryen sympathies, but MOTIVATES between two events typically implies the first event is what drives the second. A 17-year gap is survivable if the edge is clearly labeled as the root motive — T2 is right for that.
2. **Proximate trigger conflict:** If `arianne-collapses-and-is-captured --[CAUSES]--> doran-reveals-fire-and-blood-pact` already exists in the graph, this edge adds the background motivation layer. Both can coexist: one is the proximate trigger (CAUSES), the other is the sustaining motive (MOTIVATES). These are not redundant — they model different causal layers.
3. **"Fire and blood" unambiguously links to the Targaryen cause** rooted in Elia's murder. The "Vengeance. Justice. Fire and blood." trio is established Dorne-revenge rhetoric throughout AFFC/ADWD.

The edge is defensible as a T2 MOTIVATES (distal/thematic motive, not proximate trigger). The concern about the proximate trigger is real but does not invalidate this edge — they model different things.

**VERDICT: CONFIRM** — with note: if `arianne-captured CAUSES doran-reveals-pact` already exists, this edge should have a comment distinguishing it as "distal root motive" vs. that edge's "proximate trigger" to prevent graph-reader confusion.

---

## Quote Verbatim Check

Reviewing quoted/cited substrings against actual text:

- Edge 4/5 cite "Aerys burnt him alive for that" — verbatim at asos-jaime-05.md:55. CONFIRMED.
- Edge 8 cite "burst into the hall in time to see the last of it" — verbatim at asos-jaime-02.md:297. CONFIRMED.
- Edge 11 cite references agot-eddard-02.md:71 — the actual event (presenting corpses) is described in that passage but the exact phrase "presented Robert with the corpses" is a paraphrase of "when Tywin Lannister had presented Robert with the corpses of Rhaegar's wife and children." CONFIRMED as verbatim substring.
- Edge 15 cite agot-eddard-02.md:151 — "He was seated on the Iron Throne" is verbatim in that line. CONFIRMED.
- Edge 17 cite acok-tyrion-13.md:19 "King Aerys's fickle fruits" — verbatim at that line. CONFIRMED.
- Edge 18 cite affc-the-princess-in-the-tower-01.md:325 "'Vengeance.' ... 'Justice.' ... 'Fire and blood.'" — verbatim at line 325. CONFIRMED.

No quote failures detected.

---

## Tally

- CONFIRM: 15
- ADJUST: 2 (edges 12, 17)
- REJECT: 0
