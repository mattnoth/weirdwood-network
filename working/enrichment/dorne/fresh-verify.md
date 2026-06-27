# Dorne / Queenmaker — Fresh Verify Report
**Session:** S156  
**Run-id:** dorne-enrichment-s156  
**Verifier:** fresh-verify subagent (no prior context)  
**Date:** 2026-06-27  
**Chapters read:** all five in-scope chapter files (affc-the-captain-of-guards-01, affc-the-soiled-knight-01, affc-the-queenmaker-01, affc-the-princess-in-the-tower-01, adwd-the-watcher-01)

---

## Verdict Table

| ID | Type | Source → Target | Verdict | Reason |
|----|------|-----------------|---------|--------|
| E1 | CLAIMS | myrcella-baratheon → iron-throne | **ADJUST** | Edge is sound; tier and type need refinement — see E1 note |
| E2 | SEEKS | arianne-martell → dorne | **CONFIRM** | "I want my rights" / "I want Dorne" — two explicit quotes in affc-princess-in-the-tower. Solid T1. |
| E3 | MANIPULATES via_seduction | arianne-martell → arys-oakheart | **CONFIRM** | "Her seduction of Ser Arys had required half a year" is unambiguous authorial statement of instrumental seduction. T1 well-warranted. |
| E4 | DECEIVES by_lie | arianne-martell → arys-oakheart | **CONFIRM** | Arianne explicitly tells Doran: "I told him that once Myrcella was the queen she would give us leave to marry." She is a princess who knows a Kingsguard cannot marry (the chapter makes this explicit: "the vows she knew he could not break"). Knowing-false promise confirmed. T2 appropriate. |
| E5 | BREAKS_VOW | arys-oakheart → tommen-baratheon | **ADJUST** | Quote verified ("I swore an oath! / To Joffrey, not to Tommen") — but see E5 note on target |
| E6 | ATTACKS | arys-oakheart → areo-hotah | **CONFIRM** | "put his golden spurs into his horse and charged" — Arys charges directly at Hotah and the armed poleboat. Quote confirmed. T1. |
| E7 | AGENT_IN | garin-of-the-orphans → the-queenmaker-plot | **CONFIRM** | Garin knelt to Myrcella at the crowning scene; arranged the poleboat; confirmed co-conspirator. T1. |
| E8 | CONSPIRES_WITH | garin-of-the-orphans → arianne-martell | **CONFIRM** | "His mother was my wet nurse" confirmed, milk-kinship is the personal tie; conspired throughout. T1. |
| E9 | MILK_BROTHER_OF | garin-of-the-orphans → arianne-martell | **CONFIRM** | Same quote. T1. |
| E10 | MEMBER_OF | garin-of-the-orphans → orphans-of-the-greenblood | **CONFIRM** | "of the orphans of the Greenblood" confirmed; Garin self-identifies. T1. |
| E11 | AGENT_IN | andrey-dalt → the-queenmaker-plot | **CONFIRM** | "Drey went to one knee before her" confirmed in affc-queenmaker. T1. |
| E12 | CONSPIRES_WITH | andrey-dalt → arianne-martell | **CONFIRM** | "Arianne Martell arrived with Drey and Sylva" confirmed; Drey rode with her to Shandystone. T1. |
| E13 | AGENT_IN | sylva-santagar → the-queenmaker-plot | **CONFIRM** | "Spotted Sylva knelt beside him" confirmed at the crowning scene. T1. |
| E14 | CONSPIRES_WITH | sylva-santagar → arianne-martell | **CONFIRM** | Same quote as E12; Sylva rode with Arianne. T1. |
| E15 | MARRIES_OFF | doran-martell → sylva-santagar | **ADJUST** | Quote confirmed ("Her father has shipped her to Greenstone to wed Lord Estermont") but arranger attribution is wrong — see E15 note |
| E16 | TRAVELS_TO | andrey-dalt → norvos | **CONFIRM** | "sent to Norvos to serve your lady mother" confirmed. T1. |
| E17 | TRAVELS_TO | garin-of-the-orphans → tyrosh | **CONFIRM** | "Garin will spend his next two years in Tyrosh" confirmed. T1. |
| E18 | MANIPULATES via_false_information | doran-martell → arianne-martell | **CONFIRM** | Doran confesses: "Because I knew that you would spurn him." He deliberately paraded repellent suitors to conceal the secret betrothal. T1 confirmed; via_false_information is accurate. |
| E19 | OPPOSES | gerold-dayne → the-queenmaker-plot | **ADJUST** | Darkstar is indeed AGENT_IN the plot AND scorns its method — but OPPOSES needs a qualifier caveat. See E19 note. |
| E20 | DECEIVES by_lie | arianne-martell → balon-swann | **CONFIRM** | "Darkstar did it" — Arianne states this directly at the council. T2 appropriate (she is complicit in the lie, not its sole architect). Quote confirmed in adwd-the-watcher. |
| E21 | DECEIVES by_lie | doran-martell → balon-swann | **CONFIRM** | "It is all true" — Doran endorses the cover story; Hotah's narration: "Is it his gout that hurts him, or the lie?" confirms this is a known lie. T2 appropriate. |
| E22 | MOTIVATES | murder-of-elia-martell-and-rhaegars-children → doran-martell | **CONFIRM** | Doran's feast speech names Elia's murder: "He butchered my good sister, smashed her babe's head against a wall." First-person grief statement naming Elia as root of 17-year patience. T1 warranted. NB: A near-duplicate already exists (`murder-of-elia MOTIVATES doran-reveals-fire-and-blood-pact` at E22703 in edges.jsonl from sack-kl-enrichment-s142). That existing edge goes event→event; this one goes event→character — different and complementary, not a duplicate. |
| E23 | WIELDS | areo-hotah → hotahs-longaxe | **CONFIRM** | "ash-and-iron wife" confirmed; described as carried ~30 years since Norvoshi novitiate. T1. |
| E24 | WIELDED_IN | hotahs-longaxe → areo-hotah-springs-the-ambush | **CONFIRM** | "stepped Areo Hotah, longaxe in hand" confirmed at the ambush reveal. T1. |
| E25 | KILLED_WITH | arys-oakheart → hotahs-longaxe | **CONFIRM** | "removed the head of Arys Oakheart" confirmed. T1. (NB: direction odd — arys is victim not agent, but KILLED_WITH victim→weapon appears to be the graph's convention for this type; defer to existing schema.) |
| E26 | LOCATED_AT | doran-martell → water-gardens | **CONFIRM** | "left Sunspear for the peace and isolation of the Water Gardens" confirmed in affc-the-captain-of-guards. T1. |
| E27 | REGION_OF | water-gardens → dorne | **CONFIRM** | Clearly located in Dorne; "three leagues of coast road" from Sunspear confirmed in-text. T2 appropriate for geographic inference. |
| E28 | LOCATED_AT | ellaria-sand → water-gardens | **CONFIRM** | "happily ensconced at the Water Gardens" confirmed in affc-princess-in-the-tower. T1. |
| E29 | REGION_OF | ghaston-grey → sea-of-dorne | **CONFIRM** | "crumbling old castle perched on a rock in the Sea of Dorne" confirmed verbatim. T1. |
| E30 | REGION_OF | sea-of-dorne → dorne | **CONFIRM** | Geographic inference, T2 appropriate. |
| E31 | IMPRISONED_AT | arianne-martell → spear-tower | **CONFIRM** | "delivered her to the Spear Tower" confirmed in affc-princess-in-the-tower. T1. |
| E32 | LOCATED_AT | spear-tower → old-palace | **CONFIRM** | "the slender Spear Tower" confirmed as one of Sunspear's Old Palace towers in affc-the-captain-of-guards. T2 for geographic inference. |
| E33 | IMPRISONED_AT | obara-sand → spear-tower | **CONFIRM** | "confine them in the cells atop the Spear Tower" — Doran's direct order. T1. |
| E34 | IMPRISONED_AT | nymeria-sand → spear-tower | **CONFIRM** | Same order. T1. |
| E35 | IMPRISONED_AT | tyene-sand → spear-tower | **CONFIRM** | Same order. T1. |
| E36 | TRAVELS_TO | gerold-dayne → high-hermitage | **CONFIRM** | "Ser Gerold has fled back to High Hermitage, beyond our reach" confirmed in adwd-the-watcher. T1. |
| E37 | TRAVELS_TO | obara-sand → high-hermitage | **CONFIRM** | "lead him to High Hermitage to beard Darkstar in his den" — Doran's direct order to Obara. T1. |
| E38 | TRAVELS_TO | nymeria-sand → kings-landing | **CONFIRM** | "That task will be yours, Nymeria" — to escort Myrcella + take council seat. T1. |
| E39 | TRAVELS_TO | tyene-sand → kings-landing | **CONFIRM** | "I want you in King's Landing too, but on the other hill" — the High Septon cultivation mission. T1. |

**Counts: 35 CONFIRM / 4 ADJUST / 0 REJECT**

---

## Priority Edge Detailed Notes

### E1 — `myrcella-baratheon CLAIMS iron-throne` (T2)

**Verdict: ADJUST**

The quote ("By law the Iron Throne should pass to her") is from **Tyene**, not Myrcella. This is Tyene's legal argument TO Doran — making the case on Myrcella's behalf. Myrcella herself does not assert the claim verbally or explicitly in any of these chapters; at the crowning scene she is confused ("Did something bad happen to Tommen?").

The edge is **substantively defensible** — the queenmaker plot is wholly premised on Myrcella's Dornish-primogeniture claim, and she is crowned (or attempts to be), which is itself a form of asserting the claim. But the cited quote does not come from Myrcella.

**Recommended adjustment:** Change the cited evidence. The better supporting quote for "Myrcella asserts the claim" is:
- The crowning act itself (affc-the-queenmaker-01): Myrcella allows the crown to be placed on her head — she does not refuse it, and begins responding to "Your Grace."
- Alternatively: attribute to the plot rather than to Myrcella directly; re-quote: "You and your cousins wanted war" / "crowning Myrcella queen, to raise a rebellion against her brother" (Doran's summary of the act, affc-princess-in-the-tower).

**Tier:** T2 is correct — this is asserted under Dornish law, disputed by Westerosi custom, not a successful or recognized claim.

**Type:** CLAIMS is the right type. The graph's existing CLAIMS edges (Viserys, Daenerys, Euron) all use it for throne/succession assertions. This fits the pattern.

---

### E3 — `arianne-martell MANIPULATES arys-oakheart` via_seduction (T1)

**Verdict: CONFIRM**

The affc-princess-in-the-tower text states explicitly: "Her seduction of Ser Arys had required half a year." The Soiled Knight chapter shows the mechanism in operation. Arys himself reflects: "I could never lie to you … why else would I have forsaken all my honor, but for love?" — he treats the seduction as the reason he capitulated. This is genuinely instrumental (she used the relationship to get him to conspire), not merely a love affair. The LOVER_OF edge captures the relationship; MANIPULATES via_seduction adds the "using him as a tool for the plot" layer. Both can and should coexist.

---

### E4 — `arianne-martell DECEIVES arys-oakheart` by_lie (T2)

**Verdict: CONFIRM**

The text: "I told him that once Myrcella was the queen she would give us leave to marry. He wanted me for his wife." This is a distinct act from the seduction: she made a specific promise she knew to be impossible (a princess cannot give a Kingsguard leave to marry — the Soiled Knight chapter explores this at length). Distinct from E3. T2 is appropriate — the promise was the knowingly-false inducement that secured his compliance.

---

### E5 — `arys-oakheart BREAKS_VOW` TARGET ADJUDICATION

**Verdict: ADJUST — re-target to the-iron-throne or keep tommen-baratheon with clearer rationale**

The text is: "I swore an oath! / To Joffrey, not to Tommen." Arianne's retort is rhetorical dissolution of the oath-bond. However:

- Arys took his vow as a **Kingsguard oath** — an institutional oath sworn to **the Iron Throne** and its holder, not to Joffrey personally. The White Book records these as perpetual service obligations.
- Arianne's "To Joffrey, not to Tommen" argument is Arianne's spin, not how Westeros actually treats Kingsguard oaths (they serve the succession, not the individual king).
- Arys explicitly says "I swore an oath" — singular, the Kingsguard oath overall — then Arianne specifically carves out Tommen.
- He conspires to **seat Myrcella on the Iron Throne over Tommen's objection** — the violation is against Tommen's kingship, yes, but also against Myrcella herself (his direct ward) and against the institution.

**Best defensible target:** `tommen-baratheon` remains appropriate as the **reigning king against whose throne Arys conspires** — that is the most concrete, legally-sound breach (you don't break a vow by being disloyal to a previous king; you break it by conspiring against the current one). The Arianne quote about "To Joffrey not to Tommen" is her argument that HE sees the breach differently — which is fine, it's flavor, but the graph edge should record the actual breach, not Arianne's rhetorical move.

**Recommended adjustment:** Add a note that the "To Joffrey, not to Tommen" quote is Arianne's argument, not Arys's own framing. The edge target tommen-baratheon is defensible. The better anchor quote is: "I swore a vow … [protecting Myrcella] … and her rights. Set a crown upon her head" — Arys pledges to crown Myrcella over Tommen. Keep the target but update the evidence_quote to something more unambiguous, e.g., "My sword, my life, my honor, all belong to her" (after Arianne's pitch).

---

### E15 — `doran-martell MARRIES_OFF sylva-santagar` (T1)

**Verdict: ADJUST — re-point source to sylvas-father or drop**

The text is clear: "Her **father** has shipped her to Greenstone to wed Lord Estermont." Doran is the disposing authority for the other conspirators (he explicitly sentences Drey and Garin himself: "Ser Andrey has been sent to Norvos … Garin will spend his next two years in Tyrosh"). For Sylva, he says only that **her father** arranged it. The text does NOT say Doran ordered the marriage; it says "she received no punishment from me" — then notes her father's action as if it were a separate matter.

The note's rationalization ("her father executes it as part of Doran's conspirator-disposal") is reading causation into the text. Doran does not claim credit for this arrangement and explicitly says she received no punishment from him.

**Recommended adjustment:** Either re-source to `sylvas-father MARRIES_OFF sylva-santagar` (requiring a node for Sylva's father, who is named only obliquely) or drop this edge as unwarranted attribution. The safer call is **drop it**: the text doesn't support Doran as the arranger, and manufacturing implicit authority misrepresents the canon.

**Alternative:** Demote to T3 with a `note` clarifying that Doran is the political context for the arrangement but not the named arranger.

---

### E18 — `doran-martell MANIPULATES arianne-martell` via_false_information (T1)

**Verdict: CONFIRM**

The textual support is very strong. Doran confesses: "Because I knew that you would spurn him" (explaining the false-suitor parade). He selected suitors he knew she'd refuse to conceal a secret betrothal pact. The mechanism is explicitly the creation of a false picture of his intent — via_false_information is exactly right. T1 warranted since Doran himself confesses the manipulation on-page.

---

### E19 — `gerold-dayne OPPOSES the-queenmaker-plot` (T1)

**Verdict: ADJUST — the edge is defensible but needs a qualifier**

The text strongly supports this reading. At Shandystone, before the ambush, Darkstar says: "Crowning the Lannister girl is a hollow gesture. She will never sit the Iron Throne. Nor will you get the war you want" — and: "This is how you start a war. Not with a crown of gold, but with a blade of steel." He is explicitly inside the plot (AGENT_IN) yet vocally against its stated method and goal. His maiming of Myrcella at the Greenblood is consistent with his stated alternative (start a war via violence, not via crowning).

The tension with AGENT_IN is real but resolvable: these are not contradictory edges. Darkstar participated in the plot geographically while opposing its political logic — the OPPOSES edge specifically targets the goal/method, not his physical presence.

**Recommended adjustment:** Add a qualifier or note clarifying that OPPOSES captures his rejection of the plot's method/goal (crowning), not his physical non-participation. This is unusual but honest — it's the saboteur-within pattern. A note in the edge like `qualifier: method_not_goal` would help downstream queries not conflate "didn't participate" with "opposed the method."

---

### E20/E21 — Cover-story DECEIVES balon-swann (T2)

**Verdict: CONFIRM (both)**

Both quotes confirmed in adwd-the-watcher: Arianne says "Darkstar did it" at the council; Doran endorses with "It is all true." Hotah's narration: "Is it his gout that hurts him, or the lie?" confirms the authorial signal that this is a known lie. T2 is correct — these are coordinated deceptions with no direct text-witness to Balon's being deceived (yet), but the intention is unambiguous.

---

### E22 — `murder-of-elia-martell-and-rhaegars-children MOTIVATES doran-martell` (T1)

**Verdict: CONFIRM**

The adwd-the-watcher feast scene: "He butchered my good sister, smashed her babe's head against a wall. I only pray that now he is burning in some hell, and that Elia and her children are at peace. This is the justice that Dorne has hungered for." And earlier, in affc-princess-in-the-tower: "I have worked at the downfall of Tywin Lannister since the day they told me of Elia and her children." These are unambiguous first-person statements naming the murder as Doran's root motive for 17 years of patience. T1 is justified.

**Dedup check:** edges.jsonl line 22703 has `murder-of-elia MOTIVATES doran-reveals-fire-and-blood-pact` (event→event, from sack-kl-enrichment-s142). This new E22 is `murder-of-elia MOTIVATES doran-martell` (event→character). They are distinct and complementary — no duplicate.

---

## Standing Checks

### 1. THEORY-GATE Compliance

**PASS — no theory leakage detected.**

Reviewed all 39 edges. None assert:
- Aegon-is-real / fAegon-is-a-Blackfyre (the Aegon/Golden Company context in affc-the-queenmaker is present in the source chapter but no edge was minted asserting his identity)
- The full "fire and blood" as a Dornish-vengeance prophecy (E22 correctly routes to Doran's stated character motive, not the prophetic reading)
- R+L-adjacent Elia/Rhaegar theory (Elia's murder is minted as a historical event node; no edges asserted about her relationship with Rhaegar or Jon Snow's parentage)

The `_meta` note confirms these were gated to node-prose. The edges are evidence-only, motive-level.

### 2. INFORMER Non-Mint Decision

**AGREE — the non-mint was the correct call.**

The source text is unusually explicit about leaving this unresolved. The three relevant passages:

1. **affc-the-queenmaker:** Hotah's shrug: "Someone told. Someone always tells." — this is the entire textual treatment at point of capture.

2. **affc-the-princess-in-the-tower:** Arianne cycles through candidates at length (Darkstar? But his maiming Myrcella contradicts betrayal. Arys? Maybe guilt drove him. Caleotte? Nym's fondness for the Fowler twins? Obara's loose tongue?) — and explicitly reaches NO conclusion. She asks Doran directly; he refuses: "I can think of no reason why I should." 

3. **Doran's position:** "I am the Prince of Dorne. Men seek my favor." He admits he knew, but will not name the informer.

The published text does NOT point hard at any specific informer. Arianne's suspicion of Arys is possible-but-contradicted (he died at the ambush rather than being safe at home — a strange outcome for a betrayer). Darkstar is ruled out by Arianne's own reasoning. The text's "someone always tells" is a structural irony, not a clue.

A SUSPECTED_OF edge in any direction would constitute the graph asserting a conclusion the text leaves open. The non-mint is editorially honest and correct.

---

## Node Warrant Review

**garin-of-the-orphans** (character.human): Well-warranted. He has at minimum 4 edges (E7, E8, E9, E10, E17) and is a named, individually-characterized character who speaks and acts in the chapters. Correct type.

**hotahs-longaxe** (object.artifact): Well-warranted. The "ash-and-iron wife" is Hotah's defining object, named/described in both books (affc-the-captain-of-guards and adwd-the-watcher). E23, E24, E25 all confirmed. Correct type.

**spear-tower** (place.location): Well-warranted. Named repeatedly, three characters imprisoned there (E31, E33, E34, E35), one spatial edge (E32). Correct type. The note "NO container tag, Dorne not an approved container" is appropriate.

---

## Summary Recommendations for the Minting Pass

1. **E1 (CLAIMS):** Update evidence_quote — the cited quote comes from Tyene not Myrcella. Use the crowning-act itself or Doran's summary description as the anchor. Type and tier unchanged.

2. **E5 (BREAKS_VOW):** Keep target tommen-baratheon; update evidence_quote to Arys's actual pledge speech ("My sword, my life, my honor, all belong to her") rather than the Joffrey/Tommen exchange, which is Arianne's rhetorical move.

3. **E15 (MARRIES_OFF):** **DROP** or re-source to sylvas-father. The text says "Her father has shipped her" — Doran explicitly says she received "no punishment from me." Doran-as-arranger is unsupported.

4. **E19 (OPPOSES):** Retain but add qualifier note clarifying "opposes the method/goal (crowning), not the participation." Coexistence with AGENT_IN is intentional and honest.

5. All other 35 edges: CONFIRM as-is. The tier-2 assignments for DECEIVES-balon-swann are appropriate given the prospective nature of the deception (it hasn't been tested against Balon yet at chapter-end).
