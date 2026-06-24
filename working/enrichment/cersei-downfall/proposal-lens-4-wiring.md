# Lens 4 proposal — existing-node↔existing-node causal wiring
# Cersei's downfall enrichment · Session 140

Generated 2026-06-23

---

## NEW NODES

### maggy-the-frogs-prophecy
- **slug:** `maggy-the-frogs-prophecy`
- **type:** `prophecy`
- **one-line identity:** Maggy the Frog's blood-magic foretelling to young Cersei: she will be queen
  until one "younger and more beautiful" casts her down, her three children will die crowned, and
  the *valonqar* (High Valyrian: "little brother") will wrap his hands about her throat.
- **anchor quote + chapter:line:**
  > "Aye." Malice gleamed in Maggy's yellow eyes. "Queen you shall be . . . until there comes
  > another, younger and more beautiful, to cast you down and take all that you hold dear."
  — `affc-cersei-08.md:243`

  > "Gold shall be their crowns and gold their shrouds," she said. "And when your tears have drowned
  > you, the valonqar shall wrap his hands about your pale white throat and choke the life from you."
  — `affc-cersei-08.md:251`

---

## EDGES

### 1. maggy-the-frogs-prophecy --[PROPHESIED_BY]--> maggy-the-frog
| Field | Value |
|---|---|
| Tier | 1 |
| chapter:line | `affc-cersei-08.md:243` |
| quote | `"Aye." Malice gleamed in Maggy's yellow eyes. "Queen you shall be . . . until there comes another, younger and more beautiful, to cast you down and take all that you hold dear."` |
| rationale | Maggy is the named source of this prophecy via blood-magic ritual at the Lannisport tourney (~276 AC). PROPHESIED_BY is the correct relational anchor from prophecy to its issuer. |

---

### 2. maggy-the-frogs-prophecy --[MOTIVATES]--> cersei-lannister
| Field | Value |
|---|---|
| Tier | 1 |
| chapter:line | `affc-cersei-08.md:329` |
| quote | `"And you wish to forestall this prophecy?" … "Can it be forestalled?" … "Oh, yes. Never doubt that." … "I think Your Grace knows how."` |
| rationale | Cersei explicitly consults Qyburn on how to forestall the "younger and more beautiful" prophecy. The text confirms the prophecy is an active psychological driver motivating her to destroy Margaery. MOTIVATES → character (Cersei), not event. |

---

### 3. maggy-the-frogs-prophecy --[MOTIVATES]--> cersei-plots-against-margaery
**CORRECTION:** Per the agency rules, MOTIVATES targets a CHARACTER only. This edge is invalid.
→ Use edge 2 above (prophecy MOTIVATES cersei-lannister) which already captures the psychological driver; the event-chain flows through Cersei as the motivated agent.

---

### 4. cersei-lannister --[FEARS]--> tyrion-lannister   *(prophecy-grounded)*
| Field | Value |
|---|---|
| Tier | 1 |
| chapter:line | `affc-cersei-09.md:267` |
| quote | `"Tyrion is the valonqar," she said. "Do you use that word in Myr? It's High Valyrian, it means little brother."` |
| rationale | Cersei identifies Tyrion as the valonqar — the entity prophesied to choke the life from her. Her FEARS of Tyrion throughout AFFC are prophecy-grounded. She explicitly names the word and its meaning here. This edge is grounded separately from the prophecy→MOTIVATES chain and reflects a distinct relational fact about Cersei's psychology toward Tyrion. |

> **Note:** Verify that `cersei-lannister --FEARS--> tyrion-lannister` is not already in the graph from another pass before minting. If FEARS already exists, add the evidence quote as a second cite_ref on the existing edge instead.

---

### 5. cersei-lannister --[SUBJECT_OF_PROPHECY]--> maggy-the-frogs-prophecy
| Field | Value |
|---|---|
| Tier | 1 |
| chapter:line | `affc-cersei-08.md:243` |
| quote | `"Queen you shall be . . . until there comes another, younger and more beautiful, to cast you down and take all that you hold dear."` |
| rationale | Cersei is the named subject of all four Maggy prophecy clauses (queenship, children's deaths, *valonqar*). SUBJECT_OF_PROPHECY is the vocabulary's designated type for this relationship. |

---

### 6. wedding-of-tommen-i-baratheon-and-margaery-tyrell --[ENABLES]--> cersei-plots-against-margaery
| Field | Value |
|---|---|
| Tier | 2 |
| chapter:line | `affc-cersei-03.md:149` |
| quote | `"Queen you shall be . . . until there comes another, younger and more beautiful, to cast you down and take all that you hold dear." … She glanced past Tommen, to where Margaery sat laughing with her father.` |
| rationale | The Tommen-Margaery wedding is the structural door-opener (ENABLES): once Margaery becomes Tommen's queen she is positioned inside the Red Keep with daily influence over the king, which is precisely what Cersei fears as the "younger and more beautiful" threat. Cersei begins actively plotting *because* Margaery is now queen. ENABLES (precondition/door-opener) is correct here — the wedding does not itself cause the plot, but makes it necessary and possible. The prophecy-invocation at this wedding scene (line 149 is set during the Tommen wedding feast) grounds the link. |

---

### 7. littlefinger-brokers-tyrell-lannister-alliance --[ENABLES]--> wedding-of-tommen-i-baratheon-and-margaery-tyrell
| Field | Value |
|---|---|
| Tier | 2 |
| chapter:line | `wedding-of-tommen-i-baratheon-and-margaery-tyrell.node.md:Origins` (wiki-corroborated) |
| quote | `"The Stark girl brings Joffrey nothing but her body, sweet as that may be. Margaery Tyrell brings fifty thousand swords and all the strength of Highgarden."` — Petyr Baelish, ACOK Tyrion VIII (`acok-tyrion-08.md:113`) |
| rationale | The Tyrell-Lannister alliance brokered by Littlefinger at Bitterbridge is the upstream precondition that brings Margaery into the Baratheon marriage chain (first to Joffrey, then to Tommen). Without that alliance Margaery is never in King's Landing. This is a clean cross-arc ENABLES chain: Littlefinger's brokering → Tommen's wedding → Cersei's plot. The Tommen wedding node's own Origins section confirms the causal sequence. Evidence anchor is in ACOK (Tyrion VIII), not AFFC, but the node's prose documents it. Tier-2 because the direct quote is in a prior book. |

---

### 8. cersei-fills-in-the-arrest-warrants --[SUB_BEAT_OF]--> cersei-plots-against-margaery
| Field | Value |
|---|---|
| Tier | 1 |
| chapter:line | `affc-cersei-10.md:77` |
| quote | `She had written in the names herself: Ser Tallad the Tall, Jalabhar Xho, Hamish the Harper, Hugh Clifton, Mark Mullendore, Bayard Norcross, Lambert Turnberry, Horas Redwyne, Hobber Redwyne, and a certain churl named Wat, who called himself the Blue Bard.` |
| rationale | Filling in the arrest warrants is a *constitutive step* of the plot-against-Margaery, not a causally distinct downstream event. Cersei drafts the warrants as the mechanistic follow-through once the confession is extracted and Margaery is accused. SUB_BEAT_OF is the correct type (not CAUSES, which would imply a distinct downstream state; not CAUSES from plot, because agency-collapse would apply). This wires the currently islanded event into the arc. |

---

### 9. osney-kettleblack-confesses-to-high-sparrow --[CAUSES]--> cersei-fills-in-the-arrest-warrants
| Field | Value |
|---|---|
| Tier | 1 |
| chapter:line | `affc-cersei-10.md:27` |
| quote | `"The accuser is a knight of your own household. Ser Osney Kettleblack has confessed his carnal knowledge of the queen to the High Septon himself, before the altar of the Father."` |
| rationale | Osney's confession to the High Sparrow triggers the arrest of Margaery and the public accusation. Cersei *immediately* (same chapter, line 77) writes in the ten names on the blank warrants Tommen has already sealed. The confession creates the legal pretext that makes the mass arrests possible. This CAUSES edge wires `cersei-fills-in-the-arrest-warrants` into the causal chain upstream. Combined with edge 8 (SUB_BEAT_OF the plot), the formerly islanded warrant-event now sits inside the arc. |

---

### 10. cersei-is-stripped-and-imprisoned --[FORESHADOWS]--> walk-of-atonement
| Field | Value |
|---|---|
| Tier | 1 |
| chapter:line | `affc-cersei-10.md:249` |
| quote | `Inside the cell three silent sisters held her down as a septa named Scolera stripped her bare. She even took her smallclothes.` |
| rationale | The stripping and imprisonment in the sept is the narrative precursor that directly foreshadows the Walk of Atonement (which occurs in ADWD). Cersei is stripped here in the cell; the Walk is the public naked procession that is held out as her only way out of captivity. The imprisonment establishes the narrative arc that resolves in the Walk. FORESHADOWS is correct: the cell-stripping prefigures and anticipates the street-stripping. Dedup note: `walk-of-atonement` exists as a `custom` node (per LENS-CONTEXT.md confirmed baseline). |

---

### 11. cersei-lannister --[FEARS]--> maggy-the-frogs-prophecy
| Field | Value |
|---|---|
| Tier | 1 |
| chapter:line | `affc-cersei-01.md:173` |
| quote | `It is blood I need, not water. Tyrion's blood, the blood of the valonqar. The torches spun around her. Cersei closed her eyes, and saw the dwarf grinning at her. No, she thought, no, I was almost rid of you. But his fingers had closed around her neck, and she could feel them beginning to tighten.` |
| rationale | Cersei's visceral fear of the Maggy prophecy is distinct from the SUBJECT_OF_PROPHECY relation and from MOTIVATES. Here, FEARS captures her recurring terror of the valonqar clause in particular. The prophecy haunts her nightmares across all 10 AFFC Cersei chapters. FEARS is in the locked vocab and is the clearest expression of her relationship to the prophecy as a source of dread. |

---

## CROSS-ARC SEAMS — considered and ruled on

### Proposed but rejected: battle-of-the-blackwater --[ENABLES]--> cersei-plots-against-margaery (via two hops)
The Blackwater victory is two ENABLES hops upstream of the plot (Blackwater → Tyrell KL presence → Tommen wedding → plot). Proposing a direct edge skips the intermediate events and collapses distinct causal steps. The path is already capturable by graph traversal via edges 7 and 6 above. **REJECTED — covered by two-hop traversal.**

### Proposed but rejected: death-of-joffrey-baratheon --[ENABLES]--> cersei-plots-against-margaery
Joffrey's death opens the Tommen-Margaery wedding slot, but the Tyrell alliance (brokered by Littlefinger) is the true upstream gating condition. The path is: Blackwater/Alliance → Tommen wedding → plot. Joffrey's death is a co-contributor but the Tommen wedding node already captures this in its Origins. Adding the Joffrey death → plot edge directly would double-count what edge 7+6 already wire. **REJECTED — covered by the existing path.**

### Proposed but deferred: murder-of-the-old-high-septon (potential new node)
Osney confesses at `affc-cersei-10.md:243`: "She's the queen I fucked, the one sent me to kill the old High Septon. He never had no guards. I just come in when he was sleeping and pushed a pillow down across his face." This is a confirmed event with a clear agent (osney-kettleblack, directed by cersei-lannister) and victim (the unnamed predecessor High Septon, referenced at `affc-cersei-06.md:59` as "the old one who died in his sleep"). Proposing as a new event node is valid but falls to another lens (topic-lens, not cross-arc seam). The CROSS-ARC seam here is: `osney-kettleblack-confesses-to-high-sparrow` naming the murder is what escalates Cersei's arrest beyond adultery charges to *murder+treason*. **DEFERRED to another lens/session; note the cross-arc intensifier: the murder accusation is what gives the High Sparrow grounds to detain Cersei for trial rather than just for questioning.**

### cersei-rearms-the-faith --[ENABLES]--> osney-kettleblack-confesses-to-high-sparrow
This seam is tempting: Cersei's rearming gives the High Sparrow power; once he has power, Osney's confession carries weight enough to result in her arrest. However, the confession is sent *by Cersei herself* (she orders Osney to confess); the causal chain runs through cersei-plots-against-margaery, not around it. The rearming is upstream of the *capture*, not the *confession*. The existing edge `cersei-rearms-the-faith CAUSES cersei-is-captured-in-the-sept` already covers this. **REJECTED — covered by existing spine edge.**

---

## HARVEST

- `affc-cersei-08.md:205` / description / Maggy's tent interior: "cinnamon and nutmeg. Pepper, red and white and black. Almond milk and onions. Cloves and lemongrass and precious saffron, and stranger spices, rarer still." — vivid spice inventory, hospitality-adjacent object detail
- `affc-cersei-08.md:243` / quote / full Maggy prophecy text verbatim — load-bearing quote already attached above, but also suitable for node `## Quotes` section on `maggy-the-frog.node.md` if not already there (it IS in the wiki quotes section there)
- `affc-cersei-10.md:49` / quote / Cersei's false relief: "Maggy the Frog should have been in motley too, for all she knew about the morrow... No golden shrouds, no valonqar, I am free of your croaking malice at last." — ironic dramatic foreshadowing; excellent foreshadowing-scanner target
- `affc-cersei-10.md:265` / food+drink / prison deprivation: "She had smashed the chamber pot, so she had to squat in a corner to make her water... when Moelle appeared again she ate the bread and fish and demanded wine to wash it down. No wine appeared" — food/drink register of imprisonment
- `affc-cersei-03.md:153` / food+drink / Tommen wedding feast: "Only seven courses were served. Butterbumps and Moon Boy entertained the guests between dishes" — modest post-Purple-Wedding wedding feast detail
- `affc-cersei-04.md:119` / quote / "The pealing of the bells was louder in the yard. He was only a High Septon. How long must we endure this?" — Cersei on the bells tolling for the old High Septon (the one Osney killed), mordant foreshadowing
- `affc-cersei-06.md:235` / foreshadowing / "If the new High Septon continued to annoy her... Next time, I will choose their master for them. Baelor's Hand had little to teach Cersei Lannister where such matters were concerned." — Cersei contemplating killing the High Sparrow as she killed the previous one; ironic dramatic foreshadowing of her own imprisonment
- `affc-cersei-09.md:223` / quote / "Piss on your prophecy, old woman. The little queen may be younger than I, but she has never been more beautiful, and soon she will be dead." — Cersei's triumphalist delusion mid-plan, immediately before everything goes wrong
- `affc-cersei-10.md:267` / food / imprisonment diet: "Septa Moelle brought her a bowl of some watery grey gruel… she ate the bread and fish and demanded wine" — prison food register, Cersei's abasement through food
- `affc-cersei-08.md:97` / food / Small Council wine: "The gold, I think. I find Dornish wines as sour as the Dornish." — Arbor gold preference, revealing hospitality politics

---

## NOTES

**On the prophecy node itself:** A single `maggy-the-frogs-prophecy` node captures all four clauses (queen/younger-queen/children-deaths/valonqar). Do NOT split into sub-nodes; the prophecy is one continuous bloodmagic utterance. The text refers to it as a single event: Maggy speaks, Cersei listens.

**On MOTIVATES-vs-CAUSES for the prophecy edge:** The prompt suggested `prophecy MOTIVATES cersei-plots-against-margaery` but MOTIVATES must target a CHARACTER per agency rules. The correct wiring is: prophecy MOTIVATES cersei-lannister (edge 2), and cersei-lannister AGENT_IN cersei-plots-against-margaery (already in graph). The psychological chain is preserved; no new edge type is needed.

**On cersei-fills-in-the-arrest-warrants islanding:** Two edges fix this: edge 8 (SUB_BEAT_OF the plot) and edge 9 (confession CAUSES the warrants). Together they fully anchor the event. No CAUSES from warrants outward is proposed because the warrants' downstream effect (arrests) is the CAUSES relation that the arrest node should own — that edge can be proposed by another lens.

**On the Blackwater cross-arc seam depth:** The two-hop chain (edges 7 + 6) is clean and testable by graph traversal. A direct edge from Blackwater → cersei-plots-against-margaery would skip intermediate nodes and compress a two-year causal gap. The two-hop path is more historically faithful.

**On walk-of-atonement (edge 10):** The `walk-of-atonement` is confirmed as an existing `custom` node in LENS-CONTEXT.md. The FORESHADOWS edge points FROM the imprisonment event TO the walk, modeling the cell-stripping as narrative setup for the public walk. The proposer notes this is AFFC→ADWD cross-book foreshadowing, which is within scope for this type.

**Dedup passes run against:** All 8 events named in LENS-CONTEXT.md "DO NOT re-propose" list, plus all neighbors retrieved in baseline.md. No proposed edges duplicate existing ones.
