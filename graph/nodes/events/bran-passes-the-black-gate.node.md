---
name: "Bran passes the Black Gate"
type: event.incident
slug: bran-passes-the-black-gate
aliases: ["Sam opens the Black Gate", "crossing beneath the Wall", "Bran passes beneath the Nightfort"]
confidence: tier-1
era: war-of-the-five-kings
containers: [bran]
pass_origin: s130-bran-br5
node_version: 1
evidence_chapters:
  - ASOS Bran IV
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-witnessed
  date_confidence: tier-2
sort_keys:
  ac_year: 300
  book_order: 3
  chapter_number: 57
  chapter_label: "ASOS Bran IV"
  composite: "0300.3.057"
  reading_order: "3.057"
  basis: "year+chapter"
---

## Identity

At the abandoned [Nightfort](nightfort), [Bran](bran-stark)'s party reaches the [Black Gate](black-gate) — a weirwood door, old as the Wall, that only a Sworn Brother of the Night's Watch who has said his words can open. [Samwell Tarly](samwell-tarly), a sworn brother, speaks the oath and the gate opens (*"Then pass," the door said*), letting the party cross beneath the Wall into the lands beyond. Sam's presence is structurally load-bearing: without a sworn brother the gate stays shut.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S130 BRAN track / BR5. The [party-split](bran-s-party-splits-from-rickon) ENABLES this crossing (the northward journey leads here). [Samwell Tarly](samwell-tarly) ENABLES the passage — only a sworn brother's oath opens the gate, so his presence is required. Roles Tier-1: Bran, Sam AGENT_IN. This crossing ENABLES [meeting Coldhands](bran-meets-coldhands).)

## Quotes

> “Only a man of the Night’s Watch can open it, he said. A Sworn Brother who has said his words.”

— The oath requirement that makes Sam structurally required. Bran POV, ASOS Bran IV (`sources/chapters/asos/asos-bran-04.md:217`)

> "Then pass," the door said.

— The Black Gate opens after Sam speaks the words. Bran POV, ASOS Bran IV (`sources/chapters/asos/asos-bran-04.md:317`)

> "I am the sword in the darkness," Samwell Tarly said. "I am the watcher on the walls. I am the fire that burns against the cold, the light that brings the dawn, the horn that wakes the sleepers. I am the shield that guards the realms of men."

— Sam recites the Night's Watch oath to open the gate — the words that prove him a sworn brother. Bran POV, ASOS Bran IV (`sources/chapters/asos/asos-bran-04.md:315`)
