# Fresh-Verify: Tywin's Death Arc — Adversarial Edge Review
Date: 2026-06-23
Verifier: independent fresh-verify subagent (no edge proposals seen before this run)
Sources read: asos-tyrion-09.md, asos-tyrion-10.md, asos-tyrion-11.md (full text)

---

## Verdict Table

| # | Edge | Verdict |
|---|------|---------|
| 1 | `oberyn-martell POISONS gregor-clegane` T2 | ADJUST |
| 2 | `manticore-venom WIELDED_IN gregor-confesses-and-kills-oberyn` T2 | REJECT |
| 3 | `murder-of-elia-martell-and-rhaegars-children MOTIVATES oberyn-martell` T1 | ADJUST |
| 4 | `tywin-lannister DECEIVES tyrion-lannister` (by_lie) T1 | ADJUST |
| 5 | `tyrion-kills-shae-in-tywins-bed ENABLES assassination-of-tywin-lannister` T2 | CONFIRM (with note) |
| 6 | `shae-testifies-against-tyrion-at-trial MOTIVATES tyrion-lannister` T2 | ADJUST |
| 7 | `shae-testifies-against-tyrion-at-trial CAUSES tyrion-kills-shae-in-tywins-bed` T2 | ADJUST |
| 8 | `jaime-frees-tyrion-from-the-black-cells ENABLES varys-smuggles-tyrion-out-of-kings-landing` T2 | CONFIRM |
| R1 | `ellaria-sand WITNESS_IN gregor-confesses-and-kills-oberyn` | CONFIRM |
| R2 | `mace-tyrell PARTICIPATES_IN trial-of-tyrion-lannister` | CONFIRM |
| R3 | `oberyn-martell PARTICIPATES_IN trial-of-tyrion-lannister` | CONFIRM |
| S1 | `balon-swann PARTICIPATES_IN trial-of-tyrion-lannister` (ch09:191) | CONFIRM |
| S2 | `varys PARTICIPATES_IN trial-of-tyrion-lannister` (ch09:321) | CONFIRM |
| S3 | `pycelle PARTICIPATES_IN trial-of-tyrion-lannister` (ch09:245) | CONFIRM |

---

## Per-Edge Reasoning

### Edge 1 — `oberyn-martell POISONS gregor-clegane` T2
**Cited line:** asos-tyrion-10:123 — "When Oberyn spun the haft between the palms of his hand, they glistened black. Oil? Or poison? Tyrion decided that he would sooner not know."

**Verdict: ADJUST — lower tier to T3, add qualifier suspected/implied; or retype as SUSPECTED_POISONED.**

The line is Tyrion's internal speculation, hedged explicitly with "Oil? Or poison?" and followed by his deliberate decision not to know. The text never confirms poison. Gregor does not die in this chapter; his slow death from a wound that will not heal (confirmed in AFFC/ADWD) is consistent with poison, but that confirmation is in a later book. Within ASOS alone, poison is inferred circumstantially — the glistening could be oil. The edge type POISONS asserts a completed act; the text only shows a question mark in Tyrion's POV.

Recommended fix: retype to `oberyn-martell SUSPECTED_OF poisoning-gregor-clegane` T3 with qualifier implied_by_wound_progression_confirmed_later, cite_ref ASOS ch71:123; or keep POISONS but drop to T3 and add qualifier implied. Do not keep T2 with POISONS — that overclaims a Tier-2 "implied" reading as near-confirmed.

---

### Edge 2 — `manticore-venom WIELDED_IN gregor-confesses-and-kills-oberyn` T2
**Cited line:** asos-tyrion-10:123 (same line as Edge 1)

**Verdict: REJECT.**

Two problems compound here:

1. **Named substance not in this text.** The word "manticore" does not appear anywhere in asos-tyrion-10 or asos-tyrion-11. The specific venom type (manticore venom) is identified in AFFC Pycelle material, not in ASOS. Attaching that noun to line ch10:123 is a wrong-book conflation — the cited line says only "oil? Or poison?" with no substance named.

2. **Wrong event node.** The event `gregor-confesses-and-kills-oberyn` is the duel's climax (ch10:247 area). Line 123 occurs before the fight even starts, in Tyrion's pre-battle visit to Oberyn's arming chamber. The WIELDED_IN relationship would need to tie to the duel event, but the substance hasn't been named there either.

Reject entirely. If this edge is wanted at all, it belongs in a cross-book enrichment pass with a AFFC cite, not anchored to the ASOS ch10:123 line.

---

### Edge 3 — `murder-of-elia-martell-and-rhaegars-children MOTIVATES oberyn-martell` T1
**Cited line:** asos-tyrion-09:399 — "There has been none for Elia, Aegon, or Rhaenys. Why should there be any for you?"

**Verdict: ADJUST — retype or reframe; Tier is defensible but the cited line is slightly off-target.**

The on-page motivation for Oberyn championing Tyrion is made explicit a few lines later (asos-tyrion-09 line 415-420): "Not as your judge. As your champion." Oberyn offers to be Tyrion's champion in the context of the trial-by-combat against Gregor Clegane — and the reason he wants to fight Gregor specifically is stated repeatedly throughout chapter 10: "Princess Elia was my sister"; "Elia of Dorne. You raped her. You murdered her. You killed her children." The Elia murder is unambiguously Oberyn's stated motive for seeking Gregor.

However, the cited line (ch09:399) is Oberyn speaking cynically about the absence of justice generally. It is a supporting texture line, not the strongest anchor. The clearest on-page anchor for this MOTIVATES edge is ch10:187-191 where Oberyn announces himself in the fight ("Princess Elia was my sister") and the pre-fight scene at lines 161-162 ("Elia and her children have waited long for justice. But this day they shall have it.").

The edge type and tier (T1) are defensible, but MOTIVATES can be strengthened: Oberyn's motive is explicitly revenge/justice for Elia, which manifests as championing Tyrion to get at Gregor. The edge as written puts the murder as motivating oberyn-martell generally, which is too broad — the specific downstream behavior is his decision to champion Tyrion to reach Gregor. Consider splitting or targeting more precisely: `murder-of-elia-martell-and-rhaegars-children MOTIVATES oberyn-martell` is fine as T1 if read as a character-level standing motivation, but upgrade the cite_ref to ch10:161 or ch10:187 for the cleaner text anchor. No change to tier needed if the broader framing is accepted. Cite fix only.

---

### Edge 4 — `tywin-lannister DECEIVES tyrion-lannister` (by_lie) T1
**Cited line:** asos-tyrion-11:79 — "She was no whore. I never bought her for you. That was a lie that Father commanded me to tell."

**Verdict: ADJUST — edge direction and speaker are off. DECEIVES target is correct (Tyrion is deceived), but the agent should be examined.**

The text at ch11:79 is Jaime speaking — "That was a lie that Father commanded me to tell." The deceiving act was performed by Jaime under Tywin's order. Tywin commanded the lie; Jaime executed it. The edge `tywin-lannister DECEIVES tyrion-lannister` captures Tywin's authorship of the deception correctly (he commanded it), but omits Jaime as the instrument.

DECEIVES vs MANIPULATES: DECEIVES is accurate — this is a specific false statement (Tysha was a whore Jaime had bought for him), not an ambient pattern of manipulation. The qualifier `by_lie` is right.

The only issue: the cited speaker is Jaime, not Tywin directly. The edge would be more complete if both `tywin-lannister DECEIVES tyrion-lannister` (T1, as architect) and `jaime-lannister DECEIVES tyrion-lannister` (T1, as instrument, qualifier under_fathers_orders) are minted. As written the edge is not wrong but is incomplete — it captures Tywin's role but misses that the deception was mediated by Jaime. Flag for a companion edge rather than rejecting.

Also note: Tyrion's reaction at lines 85-93 confirms he is the deceived party without question. Tier T1 is correct — directly on-page.

---

### Edge 5 — `tyrion-kills-shae-in-tywins-bed ENABLES assassination-of-tywin-lannister` T2
**Cited line:** asos-tyrion-11:211

**Verdict: CONFIRM — and the causal mechanism is real, not incidental co-location.**

This is the key question: does killing Shae instrumentally enable Tyrion to get the crossbow, or is it just co-location?

Text at lines 209-211: "Afterward he found Lord Tywin's dagger on the bedside table and shoved it through his belt. A lion-headed mace, a poleaxe, and a crossbow had been hung on the walls... but a large wood-and-iron chest had been placed against the wall directly under the crossbow. He climbed up, pulled down the bow..."

The sequence is: Tyrion climbs to the bedchamber via secret passage → finds Shae in his father's bed → kills her → then arms himself with the crossbow hanging in that same room. The crossbow is in the bedchamber. Tyrion's original stated intention for climbing the ladder (at lines 163-175) is "I have business above" — he does not yet name killing Tywin when he decides to climb. He finds Shae first. He kills her. Then he arms himself.

The ENABLES logic is: entering and securing the bedchamber (which includes the Shae killing) is what gives Tyrion access to the crossbow he uses minutes later on Tywin. If he had not gone to the bedchamber, he had no ranged weapon. The killing of Shae is not the "door-opener" per se — climbing into the bedchamber is — but Shae's killing and the crossbow acquisition happen in the same room in direct sequence, and the fight/confrontation with Shae is what occupies the time between entering the room and arming.

This is marginally ENABLES (the bedchamber entry, not the killing specifically, is the enabling act). However, `tyrion-kills-shae-in-tywins-bed` as an event node encompasses the full scene in that room, and the crossbow is acquired immediately after. The ENABLES relationship holds: that scene node, as a whole, is what positions Tyrion with the crossbow that kills Tywin. CONFIRM at T2.

Note: there is a small agency-collapse risk here — the killing of Shae is an emotionally driven act (Tyrion's betrayal grief), and the crossbow acquisition is a separate deliberate decision made after. ENABLES is better than CAUSES, and the edge as written uses ENABLES. Keep it, but annotate that the mechanism is "presence in the bedchamber provides crossbow access" not "the killing of Shae caused the crossbow to be there."

---

### Edge 6 — `shae-testifies-against-tyrion-at-trial MOTIVATES tyrion-lannister` T2
**Cited line:** asos-tyrion-10:49

**Exact line 49:** "Get this lying whore out of my sight," said Tyrion, "and I will give you your confession."

**Verdict: ADJUST — the MOTIVATES target behavior needs specification; as stated the edge is too open-ended.**

The text at ch10:49 shows Shae's testimony triggering Tyrion's demand for a "confession" (actually a non-confession speech about being a dwarf), immediately followed by his trial-by-combat demand. But what is Tyrion MOTIVATED to do? The edge as written has no qualifier target — `MOTIVATES tyrion-lannister` (toward what?).

Looking at the sequence: Shae's testimony → crowd laughing at "my giant of Lannister" → Tyrion demands she be removed and says he'll confess → delivers his dwarf speech → demands trial by combat. The testimony does not mechanically cause the trial-by-combat demand in isolation — Tyrion had been considering trial-by-combat from the opening of ch09 (line 11: "Let the dice fly and pray the Red Viper could defeat Ser Gregor Clegane?"). What Shae's testimony does is push him from ambivalence into the snap decision to demand the trial rather than confess.

The edge is defensible as "MOTIVATES [tyrion-lannister → trial-by-combat-demand / emotional break]" but in its current form `shae-testifies-against-tyrion-at-trial MOTIVATES tyrion-lannister` leaves the motivation target unspecified. Add a qualifier specifying the outcome: `motivates:trial-by-combat-demand` or `motivates:emotional-break-at-trial`. Also the cite is good — line 49 is Tyrion's snap reaction to her testimony. ADJUST: add qualifier.

---

### Edge 7 — `shae-testifies-against-tyrion-at-trial CAUSES tyrion-kills-shae-in-tywins-bed` T2
**Cited line:** asos-tyrion-11:205
**Note:** existing spine edge is `jaime-reveals-the-truth-of-tysha CAUSES tyrion-kills-shae`

**Verdict: ADJUST — CAUSES is too strong for testimony alone; MOTIVATES is the better type, and overdetermination must be acknowledged.**

The question is whether Shae's testimony is a genuine converging cause or whether the Tysha reveal makes it redundant.

The text makes the killing's immediate trigger clear. Tyrion enters the bedchamber (line ~193), confronts Shae, and she says "More than anything... my giant of Lannister" (line 205). His internal reaction: "That was the worst thing you could have said, sweetling." He then strangles her. The phrase "my giant of Lannister" is what she said in her testimony (ch10:39) that the whole court laughed at. Its reuse in the bedroom triggers the killing.

So there is a real causal thread from testimony → the repeated phrase → the killing. However, the Tysha reveal (ch11:75-93) happened in the dungeon corridor just before Tyrion climbed the ladder. That reveal reframed every relationship Tyrion has with women/love/betrayal. The killing of Shae flows from a convergence: Tysha reveal (he was lied to about love once before) + Shae's betrayal at trial + the repeated phrase "my giant."

CAUSES is too strong for either cause in isolation. The spine edge `jaime-reveals-the-truth-of-tysha CAUSES tyrion-kills-shae` makes the same overclaim. Both events are contributing causes. The correct framing for the testimony is MOTIVATES (it primed his rage and the phrase is the direct trigger) rather than CAUSES (which implies sufficient causation). If the spine edge already asserts CAUSES from the Tysha reveal, then this second CAUSES edge creates overdetermination rather than convergence.

Recommended fix: retype to `shae-testifies-against-tyrion-at-trial MOTIVATES tyrion-kills-shae-in-tywins-bed` T2, and add qualifier `contributing_cause:testimony_phrase_repeated_triggers_killing`. Also recommend reviewing the spine edge for the same overclaim: `jaime-reveals-the-truth-of-tysha` probably should also be MOTIVATES or have a companion note that both causes converge.

---

### Edge 8 — `jaime-frees-tyrion-from-the-black-cells ENABLES varys-smuggles-tyrion-out-of-kings-landing` T2
**Cited line:** asos-tyrion-11:57

**Exact line 57:** "Asleep. The other three as well. The eunuch dosed their wine with sweetsleep, but not enough to kill them. Or so he swears. He is waiting back at the stair, dressed up in a septon's robe. You're going down into the sewers, and from there to the river. A galley is waiting in the bay."

**Verdict: CONFIRM.**

ENABLES vs CAUSES: correct choice. Jaime (with Varys's logistical setup) physically releases Tyrion from the black cells. Varys's smuggling operation (sewers → river → galley) was pre-arranged and waiting — Varys didn't react to Jaime's rescue; he organized it. Jaime's act of physically opening the cell is the necessary gate: without it, the prepared escape route is inaccessible. ENABLES is exactly right — Jaime's action is a necessary precondition for Varys's route to be used, but the smuggling operation itself is Varys's work.

The cited line is accurate: line 57 in ch11 is Jaime briefing Tyrion on the escape plan (Varys in septon's robe, sewer route, waiting galley). Text-anchor is solid. T2 is appropriate given the direct on-page description with no inference needed. CONFIRM.

---

## Tier-1 Role Edges — Adversarial Check

### R1 — `ellaria-sand WITNESS_IN gregor-confesses-and-kills-oberyn`
**Cited line:** asos-tyrion-10:247

**Verdict: CONFIRM — text-anchor gate passes.**

Line 247 (the area around the skull-crush): "There was a sickening crunch. Ellaria Sand wailed in terror, and Tyrion's breakfast came boiling back up."

This is unambiguous. Ellaria is physically present, she sees what happens, and her reaction (wailing in terror) directly confirms she witnessed the killing. Earlier at line 169 she is introduced at the scene: "Even Prince Oberyn's paramour paled at the sight of him." At line 203 she speaks: "Oberyn is toying with him." She is present throughout the fight and witnesses the climax. WITNESS_IN is confirmed.

---

### R2 — `mace-tyrell PARTICIPATES_IN trial-of-tyrion-lannister`
### R3 — `oberyn-martell PARTICIPATES_IN trial-of-tyrion-lannister`
**Cited line:** asos-tyrion-09:15

**Verdict: CONFIRM both.**

Line 15 is Ser Kevan explaining the judicial panel: "he has asked Lord Tyrell and Prince Oberyn to sit in judgment with him." Confirmed as co-judges. Their presence and participation as judges throughout ch09 and ch10 is pervasive — both speak, both react, both are named repeatedly. PARTICIPATES_IN as judges is accurate. T1 is appropriate (directly stated). No issues.

---

### Spot-Check S1 — `balon-swann PARTICIPATES_IN trial-of-tyrion-lannister` (ch09:191)

Line 191: "the first man ushered in was Ser Balon Swann of the Kingsguard." He speaks at length (lines 191-198). He is sworn in, testifies. CONFIRM. Cited line is accurate.

---

### Spot-Check S2 — `varys PARTICIPATES_IN trial-of-tyrion-lannister` (ch09:321)

Line 321: "Lord Varys," the herald said, "master of whisperers." He testifies throughout (lines 321-326+). CONFIRM. Cited line is the herald's introduction at the moment he takes the stand.

---

### Spot-Check S3 — `pycelle PARTICIPATES_IN trial-of-tyrion-lannister` (ch09:245)

Line 245: "Then they brought forth Grand Maester Pycelle..." He testifies at length with his jar display. CONFIRM. Cited line is accurate.

---

## Note on Line-Count Offset

The source files use a format where every blank line counts as a line. The "line numbers" cited in the edge proposals appear to align with the actual line numbers in the file as read by `awk NR==N` — spot checks on lines 49, 57, 79, 123, 191, 205, 245, 321 all returned the expected text. No systematic offset detected. One cite to watch: ch09:399 (Edge 3) is the "There has been none for Elia" line — confirmed present at line 399 in the file.

---

## Summary Count

- **CONFIRM:** 6 (Edges 5, 8, R1, R2/R3, S1, S2, S3)
- **ADJUST:** 5 (Edges 1, 3, 4, 6, 7)
- **REJECT:** 1 (Edge 2 — manticore-venom WIELDED_IN, wrong substance/wrong book/wrong cite)

**C:6 / A:5 / R:1**
