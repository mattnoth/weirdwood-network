---
name: "Exile of Jon Connington"
type: event.incident
slug: exile-of-jon-connington
aliases: ["exile of Jon Connington", "Connington stripped and exiled", "Aerys exiles Jon Connington"]
confidence: tier-1
era: roberts-rebellion
pass_origin: s133-rr-enrich
node_version: 1
evidence_chapters:
  - ADWD The Griffin Reborn I
occurred:
  ac_year: 283
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-retrospective
  date_confidence: tier-2
sort_keys:
  ac_year: 283
  book_order: null
  chapter_number: null
  chapter_label: null
  composite: "0283.0.000"
  reading_order: null
  basis: "year-only"
---

## Identity

After [Jon Connington](jon-connington) led the Targaryen host at the [Battle of the Bells](battle-of-the-bells) and failed to kill Robert Baratheon, [Aerys II Targaryen](aerys-ii-targaryen) stripped him of his titles and exiled him — an act the king framed as punishment for failure but which Connington's later retrospective characterizes as "a mad fit of ingratitude and suspicion." The exile is the causal hinge of the AEGON container arc: a disgraced Connington later finds his way to the Golden Company and raises [Young Griff](aegon-revealed-to-the-golden-company), making his own exile the precondition of Young Aegon's comeback. The exile is the direct effect of the Battle of the Bells (CAUSES, Tier-1) and in turn ENABLES the reveal of Young Aegon to the Golden Company.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S133 RR enrichment pass. [Battle of the Bells](battle-of-the-bells) CAUSES exile-of-jon-connington (Tier-1). exile-of-jon-connington ENABLES [aegon-revealed-to-the-golden-company](aegon-revealed-to-the-golden-company) (Tier-1; the exile is what puts Connington in position to serve as Aegon's guardian in exile). [Jon Connington](jon-connington) VICTIM_IN (Tier-1); [Aerys II](aerys-ii-targaryen) COMMANDS_IN as orderer (Tier-1).)

## Quotes

> "After the Battle of the Bells, when Aerys Targaryen had stripped him of his titles and sent him into exile in a mad fit of ingratitude and suspicion"

— ADWD The Griffin Reborn I (`sources/chapters/adwd/adwd-the-griffin-reborn-01.md:57`)

> "I failed the father," he said, "but I will not fail the son."

— Jon Connington, ADWD The Griffin Reborn I (`sources/chapters/adwd/adwd-the-griffin-reborn-01.md:71`)
