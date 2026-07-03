---
name: "Ironborn invasion of the North"
type: event.incident
slug: ironborn-invasion-of-the-north
aliases: ["Balon's invasion of the North", "the ironborn hosting against the North", "Balon launches the ironborn invasion", "the iron fleet sails on the North"]
confidence: tier-1
era: war-of-the-five-kings
containers: [wo5k, north]
pass_origin: s123-wo5k-j4
node_version: 1
evidence_chapters:
  - ACOK Theon II
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
sort_keys:
  ac_year: 299
  book_order: 2
  chapter_number: 25
  chapter_label: "ACOK Theon II"
  composite: "0299.2.025"
  reading_order: "2.025"
  basis: "year+chapter"
---

## Identity

Having [declared himself king](balon-declares-himself-king), [Balon Greyjoy](balon-greyjoy) launched the ironborn invasion of the lightly-garrisoned North while [Robb](robb-stark)'s army campaigned in the south. From the seat at Pyke he dispatched three thrusts: [Asha](asha-greyjoy) to take Deepwood Motte; [Victarion](victarion-greyjoy) to drive up the Saltspear and Fever River to seize [Moat Cailin](fall-of-moat-cailin) — "the key to the kingdom," which would bottle Robb out of his own land; and [Theon](theon-greyjoy) to [harry the Stony Shore](harrying-of-the-stony-shore) and draw the northern lords from their walls. With the North's fighting men gone south, only "cravens, old men, and green boys" remained to oppose them. The campaign's diversionary cover would let Theon make the unauthorized strike that took [Winterfell](capture-of-winterfell).

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S123 WO5K-remainder track / J4. Caused by [Balon's declaration](balon-declares-himself-king) (Tier-2). [Balon](balon-greyjoy) commands it (COMMANDS_IN, Tier-1); [Asha](asha-greyjoy), [Victarion](victarion-greyjoy), and [Theon](theon-greyjoy) lead the prongs (AGENT_IN, Tier-1). The invasion CAUSES [the fall of Moat Cailin](fall-of-moat-cailin) and [the harrying of the Stony Shore](harrying-of-the-stony-shore) (Tier-2), and — by stripping the North of defenders — ENABLES [the capture of Winterfell](capture-of-winterfell) (Tier-2). A causal hub, not a PART_OF umbrella: the prongs are chained by CAUSES, per the chain-as-arc policy.)

## Quotes

> "Victarion," Lord Balon said to his brother, "the main thrust shall fall to you. ... The Neck is the key to the kingdom. ... Once we hold Moat Cailin, the pup will not be able to win back to the north."

— Balon Greyjoy assigning the Moat Cailin thrust, ACOK Theon II (`sources/chapters/acok/acok-theon-02.md:413`)

> "You are to harry the Stony Shore, raiding the fishing villages and sinking any ships you chance to meet. It may be that you will draw some of the northern lords out from behind their stone walls."

— Balon Greyjoy giving Theon his orders, ACOK Theon II (`sources/chapters/acok/acok-theon-02.md:399`)

> "The lords are gone south with the pup. Those who remained behind are the cravens, old men, and green boys. They will yield or fall, one by one."

— Balon Greyjoy on the undefended North, ACOK Theon II (`sources/chapters/acok/acok-theon-02.md:417`)
