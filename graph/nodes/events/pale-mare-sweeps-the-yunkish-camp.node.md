---
name: "The Pale Mare Sweeps the Yunkish Camp"
type: event.incident
slug: pale-mare-sweeps-the-yunkish-camp
aliases: ["the pale mare in the Yunkish camp", "the bloody flux outbreak", "the pale mare sweeps the siege camp"]
confidence: tier-1
era: war-of-the-five-kings
containers: [essos]
pass_origin: s161-tyrion-essos-enrich
node_version: 1
evidence_chapters:
  - ADWD Tyrion XI
  - ADWD Tyrion XII
sort_keys:
  ac_year: null
  book_order: 5
  chapter_number: 58
  chapter_label: "ADWD Tyrion XI"
  composite: null
  reading_order: "5.058"
  basis: "chapter-only"
---

## Identity

The [bloody flux](bloody-flux) — the "pale mare" — tears through the Yunkish siege camp outside
[Meereen](meereen). It carries off [Yezzan zo Qaggaz](yezzan-zo-qaggaz) and the overseer
[Nurse](nurse) (whom [Tyrion](tyrion-lannister) quietly finishes with poisoned-mushroom soup under cover
of the plague). The chaos — Yezzan dying, his heirs fleeing, no one to count slaves — opens the escape
window through which Tyrion, Penny and Jorah slip away to
[join the Second Sons](tyrion-joins-the-second-sons).

## Edges
(Edges in `graph/edges/edges.jsonl`, S161 Tyrion/Essos enrichment. `yezzan VICTIM_IN`, `LOCATED_AT meereen`;
`yezzan AFFLICTED_BY/DIED_OF bloody-flux` (lights the 0-edge flux node); `... ENABLES
tyrion-joins-the-second-sons`. Nurse's true death is the existing `tyrion KILLS nurse` dyad.)

## Quotes

> "Two days ago Nurse had been hale and healthy. Two days ago Yezzan had not heard the pale mare's ghostly hoofbeats."

— ADWD Tyrion XI (`sources/chapters/adwd/adwd-tyrion-11.md:25`)
