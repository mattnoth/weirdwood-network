---
name: "Tyrion Joins the Second Sons"
type: event.incident
slug: tyrion-joins-the-second-sons
aliases: ["Tyrion joins the Second Sons", "Tyrion signs the Second Sons' book", "Tyrion enrolls in the Second Sons"]
confidence: tier-1
era: war-of-the-five-kings
containers: [essos]
pass_origin: s161-tyrion-essos-enrich
node_version: 1
evidence_chapters:
  - ADWD Tyrion XII
sort_keys:
  ac_year: null
  book_order: 5
  chapter_number: 67
  chapter_label: "ADWD Tyrion XII"
  composite: null
  reading_order: "5.067"
  basis: "chapter-only"
---

## Identity

Fleeing Yezzan's plague-struck camp, [Tyrion](tyrion-lannister), [Jorah Mormont](jorah-mormont) and
[Penny](penny) cross to the [Second Sons](second-sons). Tyrion talks his way in — signing promissory notes
worth a lordship and a hundred thousand dragons for [Brown Ben Plumm](ben-plumm) — and enrolls in blood in
the company book, his name just below Jorah's. This is the arc's terminus in published canon: it wires the
whole Tyrion-Essos journey into the [siege of Meereen](siege-of-meereen). (Tyrion at once conceives turning
the company's cloaks back to Daenerys, but that execution belongs to *The Winds of Winter* — node-prose only.)

## Edges
(Edges in `graph/edges/edges.jsonl`, S161 Tyrion/Essos enrichment. `tyrion AGENT_IN`, `jorah AGENT_IN`,
`penny PARTICIPATES_IN`, `tybero-istarion PARTICIPATES_IN`, `LOCATED_AT meereen`; `pale-mare-sweeps-the-yunkish-camp
ENABLES`; `... ENABLES siege-of-meereen` (the terminus seam). `tyrion/jorah MEMBER_OF second-sons` are
existing dyads.)

## Quotes

> "I have signed their book. The old way, in blood. I am now a Second Son."

— Tyrion to Penny, ADWD Tyrion XII (`sources/chapters/adwd/adwd-tyrion-12.md:121`)
