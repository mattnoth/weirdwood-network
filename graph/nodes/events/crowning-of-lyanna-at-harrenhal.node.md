---
name: "Crowning of Lyanna at Harrenhal"
type: event.incident
slug: crowning-of-lyanna-at-harrenhal
aliases: ["crowning of Lyanna", "queen of love and beauty crowning", "Rhaegar crowns Lyanna", "the laurel of winter roses"]
confidence: tier-1
era: roberts-rebellion
pass_origin: s134-rr-enrich
node_version: 1
evidence_chapters:
  - AGOT Eddard XV
occurred:
  ac_year: 281
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-retrospective
  date_confidence: tier-2
sort_keys:
  ac_year: 281
  book_order: 1
  chapter_number: 59
  chapter_label: "AGOT Eddard XV"
  composite: "0281.1.059"
  reading_order: "1.059"
  basis: "year+chapter"
---

## Identity

At the [Tourney at Harrenhal](tourney-at-harrenhal) in 281 AC, [Prince Rhaegar Targaryen](rhaegar-targaryen) won the joust — unhorsing Brandon Stark, Bronze Yohn Royce, Arthur Dayne, and finally Ser Barristan Selmy to claim the champion's crown. As tourney champion he chose the queen of love and beauty: he "urged his horse past his own wife, the Dornish princess [Elia Martell](elia-martell), to lay the queen of beauty's laurel in [Lyanna Stark](lyanna-stark)'s lap" — a crown of blue winter roses. The moment is one of the most charged in the saga's backstory: passing over his own wife to honor Lyanna (already betrothed to [Robert Baratheon](robert-baratheon)) is the public spark of the Rhaegar-Lyanna strand that ignites Robert's Rebellion. "All the smiles died." The deeper meaning of the choice — and what passed between Rhaegar and Lyanna afterward — is GATED (R+L theory); this node records only the on-page ceremony.

## Edges

(Role/structural edges live in `graph/edges/edges.jsonl`, S134 RR enrichment. This node is a [SUB_BEAT_OF](tourney-at-harrenhal) the Tourney at Harrenhal (Tier-1). [Rhaegar Targaryen](rhaegar-targaryen) AGENT_IN (the crowner; Tier-1); [Lyanna Stark](lyanna-stark) HONORED_AT (the honoree, queen of love and beauty; Tier-1); [Elia Martell](elia-martell) WITNESS_IN (the wife pointedly passed over; Tier-1). Replaces the retired off-vocab `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` edge.)

## Quotes

> "Ned remembered the moment when all the smiles died, when Prince Rhaegar Targaryen urged his horse past his own wife, the Dornish princess Elia Martell, to lay the queen of beauty's laurel in Lyanna's lap. He could see it still: a crown of winter roses, blue as frost."

— AGOT Eddard XV (`sources/chapters/agot/agot-eddard-15.md:45`)
