# LENS 1 — Downstream-causal / Consequence
## Unit: assassination-of-tywin-lannister
## Session 139 enrichment pass · Chapters asos-tyrion-08/09/10/11

---

## A. CAUSAL / MOTIVATIONAL PROPOSALS

### A1 — Shae's betrayal at trial as second CAUSES into tyrion-kills-shae-in-tywins-bed

**The spine already carries:**
`jaime-reveals-the-truth-of-tysha CAUSES tyrion-kills-shae-in-tywins-bed`

That wires the Tysha revelation as a cause. But Shae's testimony — her public sexual humiliation of Tyrion, calling him "my giant of Lannister" to the hall's laughter — is a distinct, independent converging cause that drives Tyrion's fury when he finds her in Tywin's bed. The strangling is causally overdetermined; the spine should carry both inputs.

**Proposal:**
`shae-testifies-against-tyrion-at-trial --[CAUSES]--> tyrion-kills-shae-in-tywins-bed`
- Tier: 1
- Rationale: Shae's testimony produces the "my giant of Lannister" moment of mass mockery that Tyrion explicitly re-echoes at the moment of strangling ("Did you ever like my touch?" / "More than anything, my giant of Lannister" → "That was the worst thing you could have said, sweetling."). Her betrayal is the direct emotional cause; the Tysha reveal reactivates it. Two converging causes, same target.
- Verbatim quote (asos-tyrion-09, the trigger of Tyrion's confession that opens the trial-by-combat path): `"With my mouth and . . . other parts, m'lord. All my parts. He used me every way there was, and . . . he used to make me tell him how big he was. My giant, I had to call him, my giant of Lannister."` — asos-tyrion-09:39
- And the echo at moment of killing: `"More than anything," she said, "my giant of Lannister." / That was the worst thing you could have said, sweetling.` — asos-tyrion-11:205–207
- **TARGET NODE IS NEW** — see Section C for mint proposal: `shae-testifies-against-tyrion-at-trial`

---

### A2 — Shae's testimony as TRIGGERS into Tyrion's confession speech / trial-by-combat demand

The spine has `trial-of-tyrion-lannister TRIGGERS gregor-confesses-and-kills-oberyn`. But the spine does not wire what produces Tyrion's outburst that pivots the trial to combat. Shae's testimony is the immediate spark for Tyrion's confession-speech which ends in his trial-by-combat demand:

**Proposal:**
`shae-testifies-against-tyrion-at-trial --[TRIGGERS]--> trial-of-tyrion-lannister`
- Tier: 1
- Rationale: It is specifically after Shae's testimony ("Get this lying whore out of my sight, and I will give you your confession" — asos-tyrion-10:49) that Tyrion abandons any hope of acquittal and demands trial by combat. Shae's testimony is the final intolerable witness that flips his strategy. TRIGGERS fits: it is the immediate spark; the trial had been ongoing without this single tactical pivot.
- Verbatim quote: `"Get this lying whore out of my sight," said Tyrion, "and I will give you your confession."` — asos-tyrion-10:49
- Note: This edge points FROM new node `shae-testifies-against-tyrion-at-trial` INTO existing node `trial-of-tyrion-lannister`. It is a sub-sequence within the trial — the testimony is the final straw, not the cause of the whole trial. TRIGGERS preserves that narrowness.
- **SOURCE NODE IS NEW** — same mint as A1.

---

### A3 — murder-of-elia-martell-and-rhaegars-children MOTIVATES oberyn-martell (for championing Tyrion)

The spine has no wiring explaining why Oberyn accepts to be Tyrion's champion. His motive is explicit and stated at length: he wants Gregor Clegane to confess to murdering Elia and her children on the field of combat.

**Proposal:**
`murder-of-elia-martell-and-rhaegars-children --[MOTIVATES]--> oberyn-martell`
- Tier: 1
- Rationale: Oberyn's choice to champion Tyrion is entirely explained by his desire to confront Gregor Clegane — the man who raped and murdered Elia. His repeated chant during the duel ("You raped her. You murdered her. You killed her children.") and his stated goal of extracting a confession are the textual proof. The MOTIVATES edge captures that his free choice — championing Tyrion — routes through this prior event as its driver.
- Verbatim quote (Oberyn accepting): `"He does, my lord." Prince Oberyn of Dorne rose to his feet. "The dwarf has quite convinced me."` — asos-tyrion-10:75
  and (stating motivation during combat): `"Princess Elia was my sister." / [...] "You raped her. You murdered her. You killed her children."` — asos-tyrion-10:187–191
- Note: MOTIVATES targets a CHARACTER (oberyn-martell), not an event. This is the correct type by the agency rule. The event that motivates him is the source.
- Both nodes EXIST in baseline: `murder-of-elia-martell-and-rhaegars-children` · `oberyn-martell`

---

### A4 — murder-of-elia-martell-and-rhaegars-children ENABLES gregor-confesses-and-kills-oberyn

Oberyn's obsession with hearing Gregor confess is what causes him to delay the killing blow, orbit Gregor demanding he "say her name," and — fatally — lean in too close. Without the prior murder, Oberyn would kill efficiently; the murder's unresolved injustice is the enabling condition that makes Oberyn's death possible.

**Proposal:**
`murder-of-elia-martell-and-rhaegars-children --[ENABLES]--> gregor-confesses-and-kills-oberyn`
- Tier: 2
- Rationale: Gregor is able to kill Oberyn only because Oberyn prolongs the fight to extract a confession — a delay rooted entirely in his need for Gregor to admit to murdering Elia. "Come to hear you confess" / "I will hear you say it." Oberyn's tactical mistake (gloating instead of finishing) is caused by this prior event. ENABLES is correct: the murder created the psychic condition; a third party (Gregor's grab) produces Oberyn's death. Tier 2 because the causal route runs through Oberyn's psychology, which is interpretive.
- Verbatim quote: `"I came to hear you confess." [...]  "If you die before you say her name, ser, I will hunt you through all seven hells," he promised.` — asos-tyrion-10:196, 242
- Both nodes EXIST.

---

### A5 — Jaime's guilt over the Tysha lie MOTIVATES jaime-lannister (for freeing Tyrion)

The spine has `jaime-lannister AGENT_IN jaime-frees-tyrion-from-the-black-cells` but no edge explaining WHY Jaime does it. The chapter is explicit: Jaime acknowledges it was "a debt I owed you," and when Tyrion presses, the Tysha lie is the answer. Jaime forced Tyrion to participate in Tysha's gang-rape by lying, and this guilt-debt is the stated motive.

**Proposal:**
`jaime-reveals-the-truth-of-tysha --[MOTIVATES]--> jaime-lannister`
- Tier: 1
- Rationale: Jaime says the rescue was "a debt I owed you" (asos-tyrion-11:63–64); when Tyrion demands to know what debt, Jaime names Tysha. This is the textual motive for freeing Tyrion — not mere brotherly love, but guilt specifically arising from the Tysha incident. The reveal event IS the motive event simultaneously — Jaime confesses it in the act of freeing him.
- Verbatim quote: `"Thank you, Brother," Tyrion said. "For my life." / "It was . . . a debt I owed you." Jaime's voice was strange.` — asos-tyrion-11:61–63
  and: `"Tysha," he said softly.` — asos-tyrion-11:75 (the answer to what debt)
- Both nodes EXIST. Note: the existing edge `jaime-reveals-the-truth-of-tysha MOTIVATES tyrion-lannister` correctly captures Tyrion's motivation; this edge captures Jaime's.

---

### A6 — tywin-lannister AGENT_IN jaime-reveals-the-truth-of-tysha

The baseline has Jaime as AGENT_IN for the reveal event — but the Tysha lie itself was Tywin's command to Jaime. Tywin is the originating agent of the deception that Jaime now reveals, making him a (historical) agent of the event in question.

**Proposal:**
`tywin-lannister --[AGENT_IN]--> jaime-reveals-the-truth-of-tysha`
- Tier: 1
- Rationale: Jaime explicitly states "That was a lie that Father commanded me to tell" (asos-tyrion-11:79). Tywin ordered the original lie; Jaime's reveal of it is the undoing of Tywin's command. Tywin is co-agent of the event (the event subsumes both the lie's original imposition and its revelation). AGENT_IN is appropriate for the instigating authority.
- Verbatim quote: `"She was no whore. I never bought her for you. That was a lie that Father commanded me to tell."` — asos-tyrion-11:79
- Both nodes EXIST.

---

### A7 — assassination-of-tywin-lannister TRIGGERS tyrion-lannister-flees-into-exile (NEW NODE)

The spine has `assassination-of-tywin-lannister CAUSES cersei-rearms-the-faith-and-forgives-the-debt` as the only downstream edge. But Tyrion's own flight into exile (via the sewers, Varys's galley, into the Free Cities) is an immediate and direct downstream consequence of the assassination — the very act forces him to flee. The escape was already in motion (Varys's plan), but the assassination is the point of no return; Tyrion cannot stop now.

**Proposal:**
`assassination-of-tywin-lannister --[TRIGGERS]--> tyrion-lannister-flees-into-exile`
- Tier: 1
- Rationale: The assassination is the act that makes return impossible and forces immediate flight. Tyrion explicitly recognizes this: "Do me a kindness now, and die quickly. I have a ship to catch." (asos-tyrion-11:265). TRIGGERS is correct — the assassination is the immediate spark; the flight follows directly.
- Verbatim quote: `"Do me a kindness now, and die quickly. I have a ship to catch."` — asos-tyrion-11:265
- **TARGET NODE IS NEW** — see Section C for mint proposal: `tyrion-lannister-flees-into-exile`

---

### A8 — varys-smuggles-tyrion-out-of-kings-landing ENABLES tyrion-lannister-flees-into-exile (NEW-NEW)

Varys's tunnel-and-galley infrastructure is the door-opener for Tyrion's flight. Without it, Tyrion kills Tywin and has no escape route.

**Proposal:**
`varys-smuggles-tyrion-out-of-kings-landing --[ENABLES]--> tyrion-lannister-flees-into-exile`
- Tier: 1
- Rationale: Varys provides the exact mechanism — the tunnels below the Tower of the Hand, the galley waiting in the bay, agents in the Free Cities. "A galley is waiting in the bay. Varys has agents in the Free Cities who will see that you do not lack for funds." (asos-tyrion-11:57). ENABLES is correct: Varys opens the door; Tyrion and the assassination produce the flight.
- Verbatim quote: `"You're going down into the sewers, and from there to the river. A galley is waiting in the bay. Varys has agents in the Free Cities who will see that you do not lack for funds . . ."` — asos-tyrion-11:57
- **BOTH NODES ARE NEW** — see Section C.

---

### A9 — varys AGENT_IN varys-smuggles-tyrion-out-of-kings-landing (NEW SOURCE)

`varys --[AGENT_IN]--> varys-smuggles-tyrion-out-of-kings-landing`
- Tier: 1
- Rationale: Standard role-edge for event participant. Varys is the named agent who prepares and executes the smuggling.
- Source node exists. Target node is NEW (Section C).

---

### A10 — tyrion-lannister AGENT_IN tyrion-lannister-flees-into-exile (NEW TARGET)

`tyrion-lannister --[AGENT_IN]--> tyrion-lannister-flees-into-exile`
- Tier: 1
- Source node exists. Target node is NEW (Section C).

---

### A11 — tyrion-lannister-flees-into-exile LOCATED_AT free-cities (NEW SOURCE)

`tyrion-lannister-flees-into-exile --[LOCATED_AT]--> free-cities`
- Tier: 1
- Rationale: Varys explicitly sends him toward the Free Cities. `free-cities` node exists in locations.
- Source node NEW (Section C). Target exists.

---

### A12 — Cersei's false accusation ENABLES the trial / arrest of Tyrion

The baseline has `cersei-lannister AGENT_IN tyrion-accused-of-poisoning-joffrey`. But the text in asos-tyrion-08:323 shows Cersei giving the direct arrest command immediately after Joffrey dies: "Arrest my brother. He did this, the dwarf." The accusation precedes the formal trial; it is what opens it.

**Proposal:**
`cersei-lannister --[CAUSES]--> tyrion-accused-of-poisoning-joffrey`
- Tier: 1
- Rationale: The existing edge is AGENT_IN (correct as a role edge), but this is also a CAUSES relationship: Cersei's accusation is the direct cause of Tyrion's arrest and the formal charge. Both edges can coexist. CAUSES adds the causal layer the AGENT_IN edge doesn't carry.
- Verbatim quote: `"Arrest my brother," she commanded him. "He did this, the dwarf. Him and his little wife. They killed my son. Your king. Take them! Take them both!"` — asos-tyrion-08:323
- Both nodes EXIST.

---

### A13 — shae BETRAYS tyrion-lannister

Shae's testimony is an act of betrayal against Tyrion. The graph should carry this relational edge regardless of whether the `shae-testifies` event node is minted.

**Proposal:**
`shae --[BETRAYS]--> tyrion-lannister`
- Tier: 1
- Rationale: Shae testifies against Tyrion with fabricated accusations, explicitly lying about their relationship and his alleged plots. This is textbook BETRAYS.
- Verbatim quote: `"They plotted it together," she said, this girl he'd loved.` — asos-tyrion-10:31
- Both nodes EXIST.

---

### A14 — varys BETRAYS tyrion-lannister (at trial)

Varys testifies against Tyrion at trial, corroborating evidence that helps convict him, despite previously having been in a semi-cooperative relationship with Tyrion.

**Proposal:**
`varys --[BETRAYS]--> tyrion-lannister`
- Tier: 2
- Rationale: "How do I question a little bird? I should have had the eunuch's head off my first day in King's Landing. Damn him." — Tyrion explicitly reads Varys's testimony as betrayal. Varys later explains he was watched, but the act was still a betrayal at the time. Tier 2 because Varys had structural reasons (survival, his own game) rather than malice.
- Verbatim quote: `Powdered, primped, and smelling of rosewater, the Spider rubbed his hands one over the other all the time he spoke. Washing my life away, Tyrion thought, as he listened to the eunuch's mournful account of how the Imp had schemed...` — asos-tyrion-09:323
- Both nodes EXIST.

---

### A15 — cersei-lannister MANIPULATES shae (to testify)

Shae explicitly says the queen "made her" do it: "I never meant those things I said, the queen made me." Cersei manipulated Shae into testimony.

**Proposal:**
`cersei-lannister --[MANIPULATES]--> shae`
- Tier: 1
- Rationale: Direct textual statement of Cersei's agency over Shae's testimony.
- Verbatim quote: `"I never meant those things I said, the queen made me. Please. Your father frightens me so."` — asos-tyrion-11:197
- Both nodes EXIST.

---

### A16 — cersei-lannister MANIPULATES varys (to testify)

Implied but weaker — Varys says he was "watched night and day" and "dared not help you." The queen's surveillance is the coercive instrument.

**Proposal — LOW CONFIDENCE, see Section D below.** Not proposing as main tier-1 edge; moved to rejected.

---

### A17 — shae DECEIVES trial-of-tyrion-lannister (court/hall)

Shae's testimony is false — she fabricates an elaborate story about Tyrion's plot to become king.

**Proposal:**
`shae --[DECEIVES]--> trial-of-tyrion-lannister`
- Tier: 1
- Rationale: She lied to the court (the event is the deceived party here, or alternatively the judges). DECEIVES from shae into the trial event captures the act.
- Verbatim quote: `"They plotted it together," she said, this girl he'd loved. "The Imp and Lady Sansa plotted it after the Young Wolf died."` — asos-tyrion-10:31
- Note: the target here is an event node — this is non-standard. Alternative: `shae DECEIVES tywin-lannister` (the presiding judge). Either way the underlying relation is the same. Flagging for Matt.

---

### A18 — pycelle BETRAYS tyrion-lannister (at trial)

Pycelle testifies that Tyrion stole his poisons, framing him as the poisoner.

**Proposal:**
`pycelle --[BETRAYS]--> tyrion-lannister`
- Tier: 1
- Rationale: Pycelle directly accuses Tyrion at trial: "The Imp Tyrion Lannister stole them from my chambers, when he had me falsely imprisoned." / "You used it all to kill the noblest child the gods ever put on this good earth." The accusation is retaliatory and framing.
- Verbatim quote: `"The Imp Tyrion Lannister stole them from my chambers, when he had me falsely imprisoned."` — asos-tyrion-09:247
- Both nodes EXIST (pycelle node confirmed in characters/).

---

### A19 — cersei-lannister COMMANDS_IN shae-testifies-against-tyrion-at-trial

Cersei orchestrated the witness lineup including Shae as "one final witness."

**Proposal:**
`cersei-lannister --[COMMANDS_IN]--> shae-testifies-against-tyrion-at-trial`
- Tier: 1
- Rationale: `"Almost," said Cersei. "I beg your leave to bring one final witness before you, on the morrow."` — asos-tyrion-09:329. The "final witness" is Shae. Cersei is commanding Shae's appearance.
- Verbatim quote: `"Almost," said Cersei. "I beg your leave to bring one final witness before you, on the morrow."` — asos-tyrion-09:329
- SOURCE exists; TARGET is NEW (Section C).

---

### A20 — cersei-lannister CAUSES jaime-frees-tyrion-from-the-black-cells (indirect but real)

Cersei's insistence on Tyrion's execution (overriding Tywin's plan to send him to the Wall) is what motivates Jaime to act preemptively to free Tyrion. Without Cersei pushing for immediate execution, Jaime might have done nothing.

**Proposal — LOW CONFIDENCE.** Moved to Section D (rejected-myself). The spine already routes through `gregor-confesses-and-kills-oberyn CAUSES jaime-frees-tyrion` and `tywin-lannister AGENT_IN trial-of-tyrion-lannister`. Adding Cersei's role here over-complicates the causal chain and is inferential.

---

## B. LOCATION / ROLE EDGES (non-causal, clean up coverage)

### B1 — oberyn-martell AGENT_IN gregor-confesses-and-kills-oberyn

The baseline has `oberyn-martell VICTIM_IN gregor-confesses-and-kills-oberyn` (from baseline line 42). Oberyn is ALSO an agent — he chose to champion, fought, poisoned Gregor, and named his sister repeatedly. He is both victim and agent.

**Proposal:**
`oberyn-martell --[AGENT_IN]--> gregor-confesses-and-kills-oberyn`
- Tier: 1
- Rationale: He is the active combatant who drives the event as much as Gregor. AGENT_IN and VICTIM_IN are not mutually exclusive.
- Both nodes EXIST.

---

### B2 — shae AGENT_IN trial-of-tyrion-lannister

Shae is a participant-witness in the trial, not merely a background figure.

**Proposal:**
`shae --[AGENT_IN]--> trial-of-tyrion-lannister`
- Tier: 1
- Rationale: She is named, sworn in, and testifies.
- Both nodes EXIST.

---

### B3 — varys AGENT_IN trial-of-tyrion-lannister

**Proposal:**
`varys --[AGENT_IN]--> trial-of-tyrion-lannister`
- Tier: 1
- Rationale: Varys testifies as a formal witness for a full day's proceedings.
- Both nodes EXIST.

---

### B4 — pycelle AGENT_IN trial-of-tyrion-lannister

**Proposal:**
`pycelle --[AGENT_IN]--> trial-of-tyrion-lannister`
- Tier: 1
- Rationale: Pycelle testifies with his jars of poisons.
- Both nodes EXIST.

---

### B5 — oberyn-martell AGENT_IN trial-of-tyrion-lannister

**Proposal:**
`oberyn-martell --[AGENT_IN]--> trial-of-tyrion-lannister`
- Tier: 1
- Rationale: He sits as one of three judges.
- Both nodes EXIST.

---

### B6 — mace-tyrell AGENT_IN trial-of-tyrion-lannister

**Proposal:**
`mace-tyrell --[AGENT_IN]--> trial-of-tyrion-lannister`
- Tier: 1
- Rationale: He sits as one of three judges: "Lord Mace Tyrell in a gold mantle over green" — asos-tyrion-09:171.
- Both nodes EXIST (mace-tyrell node confirmed in baseline character list).

---

### B7 — assassination-of-tywin-lannister CAUSES cersei-lannister REGENCY (no target node exists)

After Tywin's death, Cersei becomes regent for Tommen. There is no `cersei-takes-regency` or `cersei-rules-as-regent` event node. This is downstream of the assassination, but the target doesn't exist.

**Proposal — DEFERRED.** Cannot propose without an existing target node. Flagged as a mint candidate for a future session: `cersei-takes-regency-for-tommen` event.

---

### B8 — jaime-frees-tyrion-from-the-black-cells LOCATED_AT black-cells

Already in baseline (line 35). **SKIP — already exists.**

---

### B9 — varys AGENT_IN varys-smuggles-tyrion-out-of-kings-landing
Already captured in A9 above.

---

### B10 — gregor-clegane AGENT_IN gregor-confesses-and-kills-oberyn
Already in baseline (line 31). **SKIP.**

---

## C. MINT-NODE PROPOSALS

### MINT-1: shae-testifies-against-tyrion-at-trial

```
slug: shae-testifies-against-tyrion-at-trial
type: event.testimony
containers: [wo5k]
```
- Rationale: Shae's testimony is a load-bearing beat that (a) triggers Tyrion's trial-by-combat demand (A2), (b) is a converging cause into tyrion-kills-shae-in-tywins-bed (A1), and (c) anchors four other edges (A2, A19, B2, A17). It is grounded in a distinct scene occupying the opening of asos-tyrion-10 with a verbatim scripted sequence.
- Key evidence quote: `"They plotted it together," she said, this girl he'd loved. [...] "he used to make me tell him how big he was. My giant, I had to call him, my giant of Lannister."` — asos-tyrion-10:31, 39
- Located at: red-keep (throne room, same as trial)

---

### MINT-2: varys-smuggles-tyrion-out-of-kings-landing

```
slug: varys-smuggles-tyrion-out-of-kings-landing
type: event.incident
containers: [wo5k]
```
- Rationale: Distinct operational event: Varys doses the guards, routes Tyrion through the fourth-level dungeons and tunnel below the Tower of the Hand, and arranges a galley. It is a necessary step between `jaime-frees-tyrion-from-the-black-cells` and `tyrion-lannister-flees-into-exile`. Without this node, the ENABLES chain is broken.
- Key evidence quote: `"You're going down into the sewers, and from there to the river. A galley is waiting in the bay."` — asos-tyrion-11:57
- Located at: red-keep (underground tunnels / dungeons)

---

### MINT-3: tyrion-lannister-flees-into-exile

```
slug: tyrion-lannister-flees-into-exile
type: event.incident
containers: [wo5k]
```
- Rationale: Tyrion boarding the galley and departing King's Landing for the Free Cities is the key downstream beat from the assassination. It initiates the ADWD arc (Tyrion in Essos). Multiple downstream edges land here (A7, A8, A10, A11). The baseline already notes "a Varys-smuggles-Tyrion / Tyrion-flees-into-exile beat" as a mint candidate.
- Key evidence quote: `"Do me a kindness now, and die quickly. I have a ship to catch."` — asos-tyrion-11:265
- Located at: free-cities (destination) / kings-landing (origin)

---

## D. LOW-CONFIDENCE / REJECTED-MYSELF

### D1 — cersei-lannister MANIPULATES varys (to testify)
Rejected. Varys says he was "watched, night and day" and "dared not help you" — but the mechanism is surveillance/pressure, not active manipulation by Cersei. Varys may have had his own reasons. Tier is too speculative for the edge vocabulary. He later helps Jaime, showing he wasn't fully Cersei's instrument. Skip.

### D2 — cersei-lannister CAUSES jaime-frees-tyrion-from-the-black-cells
Rejected. Cersei's push for execution is the pressure that galvanizes Jaime, but the spine already routes adequately: gregor-kills-oberyn → Tyrion condemned → Jaime acts. Adding Cersei as CAUSES here creates a parallel strand without adding clarity. Jaime's motive is Tysha guilt (A5), not solely a reaction to Cersei.

### D3 — tywin-lannister CAUSES jaime-reveals-the-truth-of-tysha
Tempting but wrong direction. Tywin caused the original LIE, not the reveal. The reveal is Jaime undoing Tywin's order. Wiring `tywin CAUSES jaime-reveals-the-truth-of-tysha` would confuse cause of the lie with cause of its undoing. What's correct is `tywin-lannister AGENT_IN jaime-reveals-the-truth-of-tysha` (A6 above — the historical command makes him co-agent of the event that is now the unmasking of it). The CAUSES version is rejected.

### D4 — assassination-of-tywin-lannister CAUSES power-vacuum-in-king's-landing
The power vacuum is real but there is no existing target node, and the concept is diffuse enough that minting "power-vacuum" as an event node is unduly speculative and hard to verify sharply. Deferred / rejected for now.

### D5 — ellaria-sand VICTIM_IN gregor-confesses-and-kills-oberyn
Oberyn's paramour witnesses his death and is shattered by it. However VICTIM_IN requires participation in the event as a harmed party, not just witnessing. Ellaria is a witness and mourner, not a victim in the graph sense. Rejected.

### D6 — cersei-lannister COMMANDS_IN assassination-of-tywin-lannister
Rejected. Cersei did not command or desire Tywin's death. She wanted Tyrion dead, not Tywin. The assassination was a wholly autonomous act by Tyrion. No textual basis.

---

## HARVEST

Items encountered while reading, pointed for later extraction. POINT, don't extract.

### Food & Drink (maximally captured)
- asos-tyrion-08:133 / food / Purple Wedding feast course 1: "creamy soup of mushrooms and buttered snails, served in gilded bowls" — Tyrion finishes quickly; Sansa takes one spoonful and pushes away
- asos-tyrion-08:145 / food / Course 2: "pastry coffyn filled with pork, pine nuts, and eggs" — Sansa eats no more than a bite
- asos-tyrion-08:153 / food / Feast courses: "sweetcorn fritters and hot oatbread baked with bits of date, apple, and orange" + "gnawed on the rib of a wild boar"
- asos-tyrion-08:155 / food / Course succession: "trout cooked in a crust of crushed almonds" then "roast herons and cheese-and-onion pies" then "crabs boiled in fiery eastern spices, trenchers filled with chunks of chopped mutton stewed in almond milk with carrots, raisins, and onions, and fish tarts fresh from the ovens"
- asos-tyrion-08:157 / food / "Peacocks were served in their plumage, roasted whole and stuffed with dates" — during The Rains of Castamere
- asos-tyrion-08:171 / food / "blandissory, a mixture of beef broth and boiled wine sweetened with honey and dotted with blanched almonds and chunks of capon"
- asos-tyrion-08:171 / food / "buttered pease, chopped nuts, and slivers of swan poached in a sauce of saffron and peaches" — Tyrion notes "Not swan again" (callback to Blackwater eve)
- asos-tyrion-08:171 / food / "skewers of blood sausage brought sizzling to the tables"
- asos-tyrion-08:203 / food / "roundels of elk stuffed with ripe blue cheese" — being served when Rowan's knight stabs the Dornishman
- asos-tyrion-08:205 / food / "leche of brawn, spiced with cinnamon, cloves, sugar, and almond milk" — Tyrion toying with it when Joffrey demands the dwarf jousters
- asos-tyrion-08:281 / food / "slice of hot pigeon pie... covered with a spoon of lemon cream" placed in front of Tyrion (the pie Joffrey dies over)
- asos-tyrion-08:291 / food / Joffrey eats from the pigeon pie directly with his hand, washes it down with wine — the death sequence: "jammed his other into Tyrion's pie" / "it's good. Dry, though. Needs washing down"
- asos-tyrion-08:129 / drink / Joff's golden wedding chalice holds dark Arbor red; "a whole flagon" poured in
- asos-tyrion-08:235 / drink / Joffrey pours the chalice over Tyrion's head — wine-soaking as humiliation
- asos-tyrion-09:57 / food / Black cells food: "porridge and apples to break his fast, with a horn of ale" — breakfast in confinement
- asos-tyrion-09:163 / food / Day of third trial session breakfast: "boiled eggs, burned bacon, and fried bread" — Tyrion dresses in his finest
- asos-tyrion-09:319 / food / Tyrion flings porridge bowl at the wall in rage before third day of trial
- asos-tyrion-10:11 / food / "stabbed listlessly at a greasy grey sausage" — can't eat before final day of trial, belly full of bile
- asos-tyrion-10:101 / food / Pre-combat breakfast (after a full night's sleep): "fried bread, blood sausage, applecakes, and a double helping of eggs cooked with onions and fiery Dornish peppers" — notable contrast with pre-trial nausea
- asos-tyrion-10:103 / drink / Oberyn drinks a cup of red wine while donning his armor; Tyrion questions whether he should drink before battle
- asos-tyrion-10:247 / food+drink / Tyrion vomits his pre-combat breakfast ("bacon and sausage and applecakes, and that double helping of fried eggs cooked up with onions and fiery Dornish peppers") when Gregor smashes Oberyn's skull — direct reversal of the hopeful breakfast
- asos-tyrion-11:43 / food / Tyrion jokes about wanting "food" for his last night — "Will there be food?" at news of execution
- asos-tyrion-11:57 / food-adjacent / Varys dosed the guards' wine with sweetsleep to enable the escape
- asos-tyrion-11:79 / drink-absent / No food/drink in the black cells scene — conspicuous absence during the most intense confrontation

### Physical Descriptions
- asos-tyrion-11:25 / description / Jaime's appearance after Harrenhal: "gaunt, his hair hacked short... left a hand at Harrenhal"
- asos-tyrion-11:197 / object / Shae is wearing "a chain about her throat. A chain of linked golden hands, each holding the next" — the Hand's chain of office; significant object
- asos-tyrion-10:167–168 / description / Gregor Clegane in armor: "heavy plate over chainmail... boiled leather and a layer of quilting. A flat-topped greathelm was bolted to his gorget. The crest atop it was a stone fist." Surcoat: yellow with three black dogs of Clegane, then painted over with seven-pointed star.
- asos-tyrion-10:173 / description / Oberyn's armor: "greaves, vambraces, gorget, spaulder, steel codpiece. Elsewise Oberyn was clad in supple leather and flowing silks. Over his byrnie he wore his scales of gleaming copper." Helm: "high golden helm with a copper disk mounted on the brow, the sun of Dorne. The visor had been removed."

### Objects / Artifacts of interest
- asos-tyrion-08:265–271 / object / Widow's Wail (Joffrey's Valyrian steel sword) used to slice the pie; Margaery redirects him to Ser Ilyn. Ser Ilyn draws what Sansa recognizes as Ice (reforged). "Ser Ilyn's greatsword was as long and wide as Ice, but it was too silvery-bright." — Sansa clutches Tyrion's arm: "What has Ser Ilyn done with my father's sword?" — STRONG foreshadowing beat for Ice/Oathkeeper/Widow's Wail arc.
- asos-tyrion-10:123–124 / object / Oberyn's poisoned spear — "turned ash eight feet long... a slender leaf-shaped spearhead narrowing to a wicked spike... When Oberyn spun the haft between the palms of his hand, they glistened black. Oil? Or poison?" — the spear IS the manticore-venom delivery vehicle (manticore-venom node exists)
- asos-tyrion-11:197 / object / The Hand's chain of office — Shae is wearing it; Tyrion strangles her with it. HIGH-VALUE artifact moment — connects `hand-of-the-king` (title node) to the murder weapon.
- asos-tyrion-11:211 / object / Crossbow on the wall of Tywin's bedchamber — Tyrion takes it down; uses it to shoot Tywin. "A lion-headed mace, a poleaxe, and a crossbow had been hung on the walls."

### Foreshadowing
- asos-tyrion-08:275 / foreshadowing / Sansa recognizes Ice reforged into Ser Ilyn's sword at the wedding feast — the sword's transformation is shown before it's named; powerful planted detail
- asos-tyrion-10:157–159 / foreshadowing / Tyrion recognizes the tunnel juncture below the Tower of the Hand as the place "Shae told me of, when Varys first led her to my bed" — the very passage Varys used for Shae becomes the escape route after Shae's betrayal (structural irony, foreshadow of the reunion)
- asos-tyrion-09:387 / foreshadowing / Oberyn: "Your father may not live forever" — direct foreshadowing of Tywin's death, spoken during the Oberyn night-visit scene

### Other notable finds
- asos-tyrion-10:83 / notable / Tyrion's satisfaction at his trial-by-combat gambit is explicitly political — he calculates that either Oberyn winning (inflames Tyrells vs Dornish) or Gregor winning (inflames Dorne over Oberyn's death) damages his enemies. Rare moment where Tyrion frames the entire arc as political chess.
- asos-tyrion-08:19–26 / notable / Tyrion's in-chapter deduction that Joffrey sent the catspaw to kill Bran — this is the Purple Wedding framing chapter, excellent motive cross-reference
- asos-tyrion-09:405 / notable / Oberyn's quote: "There has been none for Elia, Aegon, or Rhaenys. Why should there be any for you?" — his motive stated explicitly to Tyrion the night before championing him
- asos-tyrion-11:265–269 / notable / "Lord Tywin Lannister did not, in the end, shit gold." — the famous closing line; also the text confirms Tywin's bowels "loosened in the moment of death" — he was literally on the privy when he died (the death location is the privy tower of the Tower of the Hand)
- asos-tyrion-09:153 / notable / Tyrion considers the Wall as his escape ("a brothel in a nearby village"), pre-Shae-testimony — last moment he thought he might survive via confession before Shae destroys that option
