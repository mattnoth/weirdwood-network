---
name: "Roose Bolton named Warden of the North"
type: event.incident
slug: roose-named-warden-of-the-north
aliases: ["Roose Bolton named Warden of the North", "Roose Bolton becomes Warden of the North", "Tywin names Roose Bolton Warden of the North", "Roose Bolton appointed Warden of the North", "the wardenship of the North"]
confidence: tier-1
era: war-of-the-five-kings
containers: [north]
pass_origin: s125-north-n5
node_version: 1
evidence_chapters:
  - ASOS Jon XI
  - ASOS Tyrion VI
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: reported-offpage
  date_confidence: tier-2
sort_keys:
  ac_year: 299
  book_order: 3
  chapter_number: 54
  chapter_label: "ASOS Tyrion VI"
  composite: "0299.3.054"
  reading_order: "3.054"
  basis: "year+chapter"
---

## Identity

In the aftermath of the [Red Wedding](red-wedding), [Tywin Lannister](tywin-lannister) names [Roose Bolton](roose-bolton) Warden of the North — the crown's reward for Bolton's betrayal of [Robb Stark](robb-stark). The appointment is never staged on the page: it is one negotiated clause of the Lannister–Frey–Bolton settlement that bought the betrayal (Tywin lists it to [Tyrion](tyrion-lannister) alongside the Frey marriages and the grant of Riverrun), and it is later relayed as accomplished fact to [Jon Snow](jon-snow) by [Stannis Baratheon](stannis-baratheon) at the Wall. The wardenship hands Roose the legal authority to hold the North; it is the event that opens the entire Bolton political spine — the marriage of [Ramsay](ramsay-snow) to a false [Arya Stark](wedding-of-ramsay-bolton-and-arya-stark), the Dreadfort's campaign to bring the surviving northern bannermen to heel, and the Bolton hold on [Winterfell](winterfell) that [Stannis](stannis-moves-to-the-wall) marches to break.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S125 NORTH track / N5 — the Bolton-thread entry. [The Red Wedding](red-wedding) CAUSES this appointment (Tier-2 — Tywin's explicit reward "for betraying your brother"); [Tywin Lannister](tywin-lannister) is the AGENT_IN, the one who confers the office (Tier-1). Roose is the beneficiary — there is no recipient role in the locked vocabulary. A proposed `MOTIVATES roose-bolton` (the wardenship driving Roose's consolidation of the North) was **dropped at fresh-verify** because the available cite was Tywin describing his own plan, not Roose acting on the office; it is deferred to a later NORTH enrichment pass that can ground it on a Roose-action quote. Terminus is downstream at the Ramsay marriage / Bolton hold, not wired here.)

## Quotes

> "Tywin Lannister has named Roose Bolton his Warden of the North, to reward him for betraying your brother."

— Stannis Baratheon to Jon Snow, ASOS Jon XI (`sources/chapters/asos/asos-jon-11.md:129`)

> "Lancel and Daven must marry Frey girls, Joy is to wed one of Lord Walder's natural sons when she's old enough, and Roose Bolton becomes Warden of the North and takes home Arya Stark."

— Tywin Lannister to Tyrion, framing the wardenship as a clause of the settlement that bought the betrayal, ASOS Tyrion VI (`sources/chapters/asos/asos-tyrion-06.md:207`)

> "We shall allow the Dreadfort to fight the ironborn for a few years, and see if he can bring Stark's other bannermen to heel."

— Tywin Lannister, the program the wardenship sets Roose into, ASOS Tyrion VI (`sources/chapters/asos/asos-tyrion-06.md:215`)
