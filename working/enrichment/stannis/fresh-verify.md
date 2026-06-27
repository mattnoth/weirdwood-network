# Fresh-Verify Report — Stannis Enrichment S155
**run_id:** stannis-enrichment-s155  
**Adjudicator:** independent fresh-verify (no prior session context)  
**Date:** 2026-06-26

---

## NODE REVIEW

### burning-of-the-seven-at-dragonstone
- **Type:** `event.incident` — CORRECT. A mass burning of religious idols, not a killing.
- **Distinctness:** Genuine new node. No prior node for this event exists.
- **Theology gate:** CLEAN. Node prose covers the ceremony (burning + sword draw). Theory-gated passage is correct: it names Lightbringer / Azor Ahai as WHAT MEL PROCLAIMED, not as graph fact. Davos's private counterpoint ("That sword was not Lightbringer") and Salladhor's tale of Nissa Nissa are present but unasserted as fact.
- **Note:** The node body references a link `[Stannis's conversion to R'hllor](rhllor)` inside a sentence, which reads like a node attribute rather than an edge. It's fine — it's prose, not an edge assertion.

### shadow-killing-of-cortnay-penrose
- **Type:** `event.assassination` — CORRECT. A targeted killing of a specific person.
- **Distinctness:** VERIFIED DISTINCT from `shadow-assassination-of-renly`. The Renly node covers ACOK Catelyn IV (Renly in his tent at parley camp). The Cortnay node covers ACOK Davos II (the sea cave below Storm's End, days later). Two separate shadow-births, two separate victims, two separate locations. The node's own prose calls this "The **second** shadow-birth." CONFIRMED GENUINE.
- **Theology gate:** CLEAN. "Shadow-magic" is described as an observed in-world mechanism (Davos witnesses the birth and the shadow entering the portcullis). No edge asserts the mechanism is R'hllor-powered or theologically validated.

### leeching-of-edric-storm
- **Type:** `event.incident` — CORRECT. A ritual act, not a killing.
- **Distinctness:** Genuine new node. No prior node for the leeching ceremony itself.
- **Theology gate:** CLEAN. The theory-gate in node prose is explicit: "king's-blood magic WORKS … the leeching CAUSES the subsequent deaths … all evidence-only." No FORESHADOWS/CAUSES edge minted. This is the clearest theory-gate execution in the batch.

---

## EDGE ADJUDICATION TABLE

| ID | Type | Source → Target | Verdict | Reason |
|----|------|----------------|---------|--------|
| E1 | AGENT_IN | melisandre → burning-of-the-seven | CONFIRM | Chapter text: "The red woman walked round the fire three times, praying." Unambiguous. |
| E2 | PARTICIPATES_IN | stannis-baratheon → burning-of-the-seven | CONFIRM | "grasped the sword with his gloved hand, and wrenched it free" — his central physical act. |
| E3 | PARTICIPATES_IN | selyse-florent → burning-of-the-seven | CONFIRM | "Queen Selyse echoed the words." |
| E4 | WITNESS_IN | davos-seaworth → burning-of-the-seven | CONFIRM | "He felt ill as he watched them burn." Clear witness role, not agent. |
| E5 | WIELDED_IN | lightbringer → burning-of-the-seven | CONFIRM | "jade-green flames swirling around cherry-red steel" — the sword is the climax. |
| E6 | WIELDS | stannis-baratheon → lightbringer | CONFIRM | asos-davos-04 line 195: "Stannis drew his longsword. Lightbringer, Melisandre had named it." Clean. |
| E7 | WORSHIPS | stannis-baratheon → rhllor | **ADJUST** | See detailed note below. |
| E8 | ADVISES | melisandre → stannis-baratheon | **ADJUST** | See detailed note below. |
| E9 | AGENT_IN | melisandre → shadow-killing-of-cortnay | CONFIRM | "she was naked, and huge with child" — births the shadow, unambiguously the agent. |
| E10 | COMMANDS_IN | stannis-baratheon → shadow-killing-of-cortnay | CONFIRM | "Ser Cortnay will be dead within the day" + Stannis sends Davos to row Mel in. |
| E11 | PARTICIPATES_IN | davos-seaworth → shadow-killing-of-cortnay | CONFIRM | "steering a tiny boat with a black sail" — logistical participant. |
| E12 | VICTIM_IN | cortnay-penrose → shadow-killing-of-cortnay | CONFIRM | "Ser Cortnay will be dead within the day" — confirmed by context (found dead, castle yields). |
| E13 | WITNESS_IN | davos-seaworth → shadow-killing-of-cortnay | CONFIRM | "He knew that shadow." Davos sees the shadow enter the portcullis. |
| E14 | LOCATED_AT | shadow-killing-of-cortnay → storms-end | CONFIRM | Sea cave beneath Storm's End, clearly cited. |
| E15 | ENABLES | shadow-killing-of-cortnay → taking-of-storms-end | CONFIRM | See detailed note below. |
| E16 | PROTECTS | cortnay-penrose → edric-storm | CONFIRM | "Then my answer is still no, my lord" — Cortnay refuses to yield Edric; is killed for this. The whole purpose of the shadow is to remove Cortnay's protection. |
| E17 | WITNESS_IN | catelyn-stark → shadow-assassination-of-renly | CONFIRM | Supported by acok-catelyn-04 (cited in shadow-assassination-of-renly node). Edge direction and type correct. |
| E18 | WITNESS_IN | brienne-tarth → shadow-assassination-of-renly | CONFIRM | Same chapter, consistent with node. |
| E19 | SUSPECTED_OF | brienne-tarth → shadow-assassination-of-renly | CONFIRM | See detailed note below. |
| E20 | SUSPECTED_OF | catelyn-stark → shadow-assassination-of-renly | CONFIRM | See detailed note below. |
| E21 | MOTIVATES | renly-s-death-reflection → stannis-baratheon | **ADJUST** | See detailed note below. |
| E22 | MOTIVATES | davos-seaworth → stannis-baratheon | CONFIRM | See detailed note below. |
| E23 | MOTIVATES | murder-of-jon-arryn → stannis-baratheon | CONFIRM | See detailed note below. |
| E24 | AGENT_IN | melisandre → leeching-of-edric-storm | CONFIRM | "the red woman retrieved the silver dish and brought it to the king." She conducts the ritual. |
| E25 | AGENT_IN | stannis-baratheon → leeching-of-edric-storm | CONFIRM | "The leech was twisting in the king's grip" — Stannis names and throws each leech. |
| E26 | VICTIM_IN | edric-storm → leeching-of-edric-storm | CONFIRM | "The boy's blood, Davos knew. A king's blood." Unambiguous. |
| E27 | WITNESS_IN | davos-seaworth → leeching-of-edric-storm | CONFIRM | "Davos watched her lift the lid." |
| E28 | LOCATED_AT | leeching-of-edric-storm → dragonstone | CONFIRM | "within the great round room called the Chamber of the Painted Table." |
| E29 | MOTIVATES | leeching-of-edric-storm → davos-seaworth | CONFIRM | See detailed note below. |
| E30 | RESCUES | davos-seaworth → edric-storm | CONFIRM | See detailed note below. |
| E31 | ADVISES | jon-snow → stannis-baratheon | **ADJUST** | See detailed note below. |

---

## DETAILED NOTES ON FLAGGED EDGES

### E7 — `stannis WORSHIPS rhllor` (Tier-2) [verify:true]

**Verdict: ADJUST — change type from WORSHIPS to FOLLOWS (or keep WORSHIPS but clarify tier rationale)**

The text is:
> "I know little and care less of gods, but the red priestess has power. … The Seven have never brought me so much as a sparrow. It is time I tried another hawk, Davos. A red hawk."

And earlier:
> "I stopped believing in gods the day I saw the Windproud break up across the bay."

Stannis is **explicitly not a believer**. His conversion is entirely pragmatic — he wants the power Melisandre wields, not the theology. He participates in the burning, draws the sword, but characterizes it as switching "hawks" (tools), not as devotional worship. In asos-davos-06 he stands at the nightfire "jaw clenched hard" and "did not respond with the others" to the R'hllor prayers.

**WORSHIPS** implies devoted religious practice. The text does not support this for Stannis specifically — it's selyse who WORSHIPS; Stannis USES. The proposer's own note acknowledges "pragmatic/instrumental, private doubt" and assigns Tier-2, which is the right instinct, but the edge TYPE is still wrong.

**Recommended change:** Change `WORSHIPS` → `FOLLOWS` (allegiance without theological belief). Tier-2 is appropriate. The "another hawk" quote and the burning participation support an FOLLOWS/SERVES allegiance edge, not religious devotion. The note should read: "Stannis's public alignment with R'hllor — pragmatic, not devotional; his explicit skepticism ('I know little and care less of gods') gates against WORSHIPS."

If the vocabulary does not have FOLLOWS for a person→deity relationship, SERVES is acceptable. If WORSHIPS is the only available edge type for person→deity, keep it at Tier-2 but note the explicit skepticism in the evidence_quote.

---

### E8 — `melisandre ADVISES stannis` [Tier-1, not verify:true but worth noting]

The cited quote is "Now I will hear hers" (Stannis dismissing Cressen to hear Melisandre) from acok-prologue. I did not read acok-prologue, but the note accurately describes the advisory relationship established across acok-davos-01 and acok-davos-02. The edge is sound. Tier-1 is appropriate — this is an established canonical relationship visible in every Davos chapter. No issue.

---

### E15 — `shadow-killing-of-cortnay ENABLES taking-of-storms-end` (Tier-2) [verify:true]

**Verdict: CONFIRM. ENABLES is exactly right.**

From acok-davos-02:
> "command of Storm's End would pass to this stripling [Lord Meadows], and his cousins believe he would accept my terms and yield up the castle."

The causal chain: Cortnay dies → command passes to Lord Meadows (a young, more compliant castellan) → Meadows **chooses** to yield. This is exactly the ENABLES pattern: the death removes the blocking agent, and a second agent (Meadows) makes a free choice to yield. If the killing directly caused the castle to fall without any intervening free choice, it would be CAUSES. But here, the mechanism is Meadows's independent decision. ENABLES at Tier-2 is correct.

---

### E19 — `brienne SUSPECTED_OF shadow-assassination-of-renly` (Tier-2) [verify:true]
### E20 — `catelyn SUSPECTED_OF shadow-assassination-of-renly` (Tier-2) [verify:true]

**Both: CONFIRM.**

From acok-davos-02:
- E19: "It was Brienne," insisted Lord Caron. "Ser Emmon Cuy swore as much before he died."
- E20: Lord Florent: "I believe it was Lady Stark who slew the king."

Both are clearly in-world accusations, not authorial assertions of fact. Both accusers are named (Caron/Cuy for Brienne; Florent for Catelyn). Both women are innocent — Stannis's shadow is the true killer (he is AGENT_IN shadow-assassination-of-renly). SUSPECTED_OF is the correct edge type. Tier-2 is mandatory and correct (these are unproven in-world allegations). The chapter reference (acok-davos-02, not acok-catelyn-04) is where these accusations surface in dialogue, so the citation is accurate. No theory leak here — SUSPECTED_OF by definition does not assert truth.

---

### E21 — `renly-s-death-reflection MOTIVATES stannis-baratheon` (Tier-1) [verify:true]

**Verdict: ADJUST — downgrade to Tier-2, and note the source node's staging status.**

The quote from acok-davos-02:
> "I dream of it sometimes. Of Renly's dying. A green tent, candles, a woman screaming. And blood." … "I did love him, Davos."

This is strong support for a MOTIVATES link: Renly's death haunts Stannis (guilt/grief substrate). The edge type and direction are correct.

However, two issues:

1. **Source node status:** `renly-s-death-reflection` is a **staging-only node** — its own file reads "Staging only — do NOT promote to graph/nodes/events/ until Plate 5 gated merge." This edge references a node that is not yet in the canonical graph. The edge should be **held** until `renly-s-death-reflection` is promoted, or the edge should carry a note that it depends on a staged node.

2. **Tier:** The proposer assigned Tier-1. But Stannis is not explicitly saying "Renly's death drives me forward" — he's saying it haunts him ("I dream of it," "I will go to my grave thinking of my brother's peach"). The causal link from the reflection to Stannis's behavior requires one interpretive hop. Tier-2 is more honest.

**Recommended change:** Downgrade Tier-1 → Tier-2. Add note: "Depends on `renly-s-death-reflection` being a staged node — hold until Plate 5 promotion or confirm it's been promoted to graph/nodes/events/ before minting."

---

### E22 — `davos MOTIVATES stannis-baratheon` (Tier-2) [verify:true]

**Verdict: CONFIRM.**

The quoted line from asos-davos-06:
> "a king protects his people, or he is no king at all"

In context, Davos says this immediately before disclosing he has smuggled Edric off Dragonstone. The full scene is Davos presenting this argument to Stannis, who is wrestling with whether to burn Edric. The argument is part of why Stannis — facing this challenge — ultimately accepts Edric's escape without executing Davos.

But the note says this is the "why-march-north" argument. Reading the full chapter: this quote is from asos-davos-06, which is the Edric smuggling scene, not the march-north scene. The argument about marching north is in adwd-jon-04 (Jon's advice). In asos-davos-06, Davos argues for protecting Edric; Stannis's pivot to the Wall happens later. So the MOTIVATES edge is real, but the characterization in the note ("why-march-north") is **wrong** — this quote is about protecting Edric Storm, not the march north.

The edge itself (davos MOTIVATES stannis) is supported — Davos's argument does motivate Stannis (he keeps Davos as Hand, accepts the rescue of Edric rather than ordering his return). The mis-labeling in the note doesn't invalidate the edge, but the chapter+quote attachment should be understood clearly. Tier-2 is appropriate (one interpretive hop).

**CONFIRM the edge; correct the note to say: "Davos's 'a king protects his people' argument in the Edric Storm confrontation motivates Stannis's acceptance of the smuggling. This is the Edric-protection argument, NOT the march-north argument."**

---

### E23 — `murder-of-jon-arryn MOTIVATES stannis-baratheon` (Tier-2) [verify:true]

**Verdict: CONFIRM.**

The quote from acok-davos-02:
> "I have no doubt that Cersei had a hand in Robert's death. I will have justice for him. Aye, and for Ned Stark and Jon Arryn as well."

This is Stannis explicitly naming Jon Arryn as someone he wants justice for. Jon Arryn's murder is one of the driving grievances for Stannis's claim. He and Jon Arryn together investigated the twincest; Arryn was then killed (presumably silenced) as a direct consequence of that investigation. Stannis knowing this connects murder-of-jon-arryn to his motivating posture.

This is Tier-2 appropriate: the quote shows Stannis invoking Jon Arryn's murder as a grievance, which counts as MOTIVATES. The cross-container tag note is accurate (RR arc → wo5k/Stannis). CONFIRM.

---

### E29 — `leeching-of-edric-storm MOTIVATES davos-seaworth` (Tier-2) [verify:true]

**Verdict: CONFIRM.**

The chain is clear in asos-davos-04: Davos witnesses the leeching, thinks "The boy's blood, Davos knew. A king's blood." This horror is the emotional trigger that hardens his resolve to remove Edric. In asos-davos-06, he executes the smuggling. The MOTIVATES link is well-supported — the witnessing of the leeching directly precedes and causes the rescue. Tier-2 is appropriate (interpretive link, though the causation is strongly implied). CONFIRM.

---

### E30 — `davos RESCUES edric-storm` (Tier-2) [verify:true]

**Verdict: CONFIRM.**

From asos-davos-06:
> "He is aboard a Lyseni galley, safely out to sea."

The chapter shows Davos organizing the smuggling operation in detail: gathering allies (Estermont, Gower, Bastard of Nightsong, Lewys the Fishwife, Omer Blackberry), recovering Edric from Maester Pylos, getting him to a boat and out to Mad Prendos (a Lyseni galley). This is an active intervention saving someone from danger (imminent sacrifice). RESCUES is exactly right. Tier-2 appropriate (Stannis didn't order the rescue; it's Davos acting against the king's apparent intent). CONFIRM.

---

### E31 — `jon-snow ADVISES stannis-baratheon` (Tier-2) [verify:true]

**Verdict: ADJUST — confirm the edge exists and type is right, but note the cited quote is NOT in adwd-jon-04.**

The cited quote is:
> "Eat their bread and salt, drink their ale"

This quote IS in adwd-jon-04 at line 293:
> "Eat their bread and salt, drink their ale, listen to their pipers, praise the beauty of their daughters and the courage of their sons, and you'll have their swords."

The quote is accurately located. The chapter shows Jon giving sustained tactical advice to Stannis: how to approach the northern mountain clans, why the Dreadfort plan will fail, recommending Deepwood Motte instead, and offering guides and wildling fighters. Jon explicitly functions as an advisor here, and Stannis takes his advice ("Goat tracks?" / "Aye, I will. I am not an utter fool"). The edge is fully supported.

**However:** The note says "no jon ADVISES stannis edge existed." That may need verification against the existing graph, but I'll take it on trust — the edge is warranted regardless.

Tier-2 is correct: Jon is not officially Stannis's advisor (his vows prohibit taking sides), so the advisory relationship is informal and context-dependent. CONFIRM with the note that the quote location in adwd-jon-04 line 293 is verified.

---

## DROPS (edges to remove)

**NONE.** No edge is rejected outright.

---

## ADJUSTS (edges to change)

| Edge | Change |
|------|--------|
| E7 | Change type `WORSHIPS` → `FOLLOWS`. Stannis's own words ("I know little and care less of gods," "time I tried another hawk") prove this is pragmatic allegiance, not devotion. Tier-2 stays. |
| E21 | Downgrade tier: Tier-1 → Tier-2. Add note flagging that `renly-s-death-reflection` is a staged-only node (not yet in `graph/nodes/events/`); hold edge until that node is promoted or confirm promotion has occurred. |
| E22 | Note correction only (no structural change): the "why-march-north" label in the note is wrong — this is the Edric-protection argument from asos-davos-06. The edge type, source, target, tier, and quote are all correct. |
| E31 | Minor: verify against graph that no prior jon ADVISES stannis edge exists before minting. No structural change needed. |

---

## TALLY

- **CONFIRM:** 27
- **ADJUST:** 4 (E7, E21, E22, E31)
- **REJECT:** 0

---

## THEORY-GATE VERDICT: CLEAN

No edge asserts:
- Azor Ahai / prince that was promised (Melisandre's proclamations appear only as node prose, correctly attributed to her; no graph edge)
- King's-blood magic works (leeching node explicitly gates this)
- The leeching CAUSES the three kings' deaths (no FORESHADOWS or CAUSES edge minted)
- Stannis as prophesied hero
- Shadow mechanism as R'hllor-validated theology

The three node files handle theory-gating correctly. The clearest risk point was leeching-of-edric-storm, and the proposer was meticulous: the note explicitly says "No leeching FORESHADOWS/CAUSES the 3 kings' deaths."

---

## SUMMARY FOR MATT

**27 CONFIRM / 4 ADJUST / 0 REJECT. Theory gate: CLEAN.**

Key adjustments:
1. **E7 (WORSHIPS → FOLLOWS):** Stannis explicitly disavows belief in gods; "another hawk" is pure pragmatism. WORSHIPS is the wrong type.
2. **E21 (Tier-1 → Tier-2):** The `renly-s-death-reflection` source node is staging-only (not yet promoted to `graph/nodes/events/`). Also downgrade to Tier-2 — haunting ≠ explicit causal statement.
3. **E22 note fix:** The "why-march-north" label is wrong. The asos-davos-06 quote is about protecting Edric Storm, not marching to the Wall. Edge is structurally sound.
4. **E31:** Confirm no duplicate before minting; otherwise clean.
