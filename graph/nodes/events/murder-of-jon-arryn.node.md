---
name: "Murder of Jon Arryn"
type: event.assassination
slug: murder-of-jon-arryn
aliases: ["murder of Jon Arryn", "death of Jon Arryn", "poisoning of Jon Arryn"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s133-rr-enrich
node_version: 1
evidence_chapters:
  - AGOT Eddard VII
  - ASOS Sansa VII
occurred:
  ac_year: 298
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
sort_keys:
  ac_year: 298
  book_order: 1
  chapter_number: 31
  chapter_label: "AGOT Eddard VII"
  composite: "0298.1.031"
  reading_order: "1.031"
  basis: "year+chapter"
---

## Identity

The inciting mystery of the entire saga. [Jon Arryn](jon-arryn), Hand of the King, was poisoned with the tears of Lys — a rare, clear, traceless poison. A letter from [Lysa Arryn](lysa-arryn) to her sister Catelyn blamed the Lannisters, pulling [Eddard Stark](eddard-stark) to King's Landing and triggering the whole chain of events in AGOT. The ASOS reveal (Lysa's confession to Littlefinger at the Eyrie) exposes [Lysa Arryn](lysa-arryn) as the direct administrator of the poison, acting at the instigation of [Petyr Baelish](petyr-baelish). [Cersei Lannister](cersei-lannister) was the prominent false-misdirection target named in Lysa's letter. This event is NOT part of Robert's Rebellion (it occurs 298 AC, roughly 15 years after RR's close); it is a standalone hub anchoring the War of the Five Kings' proximate trigger-chain.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S133 RR enrichment pass. [Jon Arryn](jon-arryn) VICTIM_IN (Tier-1); [Lysa Arryn](lysa-arryn) AGENT_IN (direct poisoner, per her own confession; Tier-1); [Petyr Baelish](petyr-baelish) COMMANDS_IN as instigator (upgraded from SUSPECTED_OF at S148 — Lysa's dying confession "You told me to put the tears in Jon's wine" proves the instigation; reaffirmed S211); [Cersei Lannister](cersei-lannister) SUSPECTED_OF as false-misdirection target (Tier-2 — the in-world suspicion was real even though she is innocent); [Tyrion Lannister](tyrion-lannister) SUSPECTED_OF (Tier-2, added S211 — Catelyn/Lysa's false public accusation at the Eyrie, load-bearing for the whole ACOK Eyrie arc).)

## Quotes

> "The tears of Lys, they call it. A rare and costly thing, clear and sweet as water, and it leaves no trace."

— AGOT Eddard VII (`sources/chapters/agot/agot-eddard-07.md:311`)

> "You told me to put the tears in Jon's wine, and I did. For Robert, and for us!"

— Lysa Arryn, ASOS Sansa VII (`sources/chapters/asos/asos-sansa-07.md:287`)
