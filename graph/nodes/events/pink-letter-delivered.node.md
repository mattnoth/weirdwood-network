---
name: "The Pink Letter arrives at Castle Black"
type: event.incident
slug: pink-letter-delivered
aliases: ["the Pink Letter arrives", "Jon receives the Pink Letter", "the reading of the Bastard Letter", "the Pink Letter is delivered", "Jon reads Ramsay's letter"]
confidence: tier-1
era: war-of-the-five-kings
containers: [north]
pass_origin: s126-north-n4
node_version: 1
evidence_chapters:
  - ADWD Jon XIII
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-witnessed
  date_confidence: tier-2
sort_keys:
  ac_year: 300
  book_order: 5
  chapter_number: 70
  chapter_label: "ADWD Jon XIII"
  composite: "0300.5.070"
  reading_order: "5.070"
  basis: "year+chapter"
---

## Identity

In ADWD Jon XIII, the steward Clydas delivers a scroll addressed only to "Bastard," sealed in hard pink wax — the so-called Pink Letter, authored by [Ramsay Bolton](ramsay-snow) (the [bastard-letter](bastard-letter) artifact). It declares [Stannis Baratheon](stannis-baratheon) dead, taunts Jon over [Mance Rayder](mance-rayder) caged at [Winterfell](winterfell), demands hostages, and threatens to cut out Jon's heart. Reading it transforms Jon's plans: at the Shieldhall he announces he will ride south on Winterfell — "I ride to Winterfell alone, unless …" — and the free folk roar to follow him. This open breach of the Watch's neutrality is the spark; within minutes [Bowen Marsh](bowen-marsh) and the conspirators fall on him. This event is the receiving/reading beat at Castle Black, distinct from the `bastard-letter` artifact (the letter object itself).

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S126 NORTH track / N4. This delivery TRIGGERS [Jon is stabbed repeatedly](jon-is-stabbed-repeatedly) (Tier-2 — Jon's Shieldhall march announcement, his response to the letter, is the specific spark that makes the conspirators act). [Jon Snow](jon-snow) is the AGENT_IN, the one who reads it and converts it into the march decision (Tier-1). Ramsay's agency belongs to the artifact authorship, not this receiving event.)

## Quotes

> And the letter was sealed with a smear of hard pink wax.

— The letter's arrival at Castle Black, addressed only to "Bastard." Jon POV, ADWD Jon XIII (`sources/chapters/adwd/adwd-jon-13.md:227`)

> "The Night's Watch will make for Hardhome. I ride to Winterfell alone, unless …"

— Jon's Shieldhall march announcement, his response to the Pink Letter. Jon POV, ADWD Jon XIII (`sources/chapters/adwd/adwd-jon-13.md:295`)
