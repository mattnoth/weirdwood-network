---
name: "Littlefinger smuggles Sansa out of King's Landing"
type: event.deception
slug: littlefinger-smuggles-sansa-out-of-kings-landing
aliases: ["sansa-escapes-kings-landing", "dontos-leads-sansa-from-the-castle"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s106-causal-track
node_version: 1
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-scene
  date_confidence: tier-2
staged_by: petyr-baelish
audience: sansa-stark
false_belief: "Ser Dontos is Sansa's gallant rescuer ('Florian') acting on his own to take her home."
payoff: "Sansa is spirited away to Littlefinger's keeping aboard the Merling King; Dontos, his use spent, is killed."
sort_keys:
  ac_year: 300
  book_order: null
  chapter_number: null
  chapter_label: null
  composite: "0300.0.000"
  reading_order: null
  basis: "year-only"
---

## Identity

In the chaos following Joffrey's death, Ser Dontos leads Sansa Stark out of the Red Keep to a waiting boat, and from there to the Merling King, where Petyr "Littlefinger" Baelish has Dontos killed and carries Sansa off to the Fingers (later renaming her Alayne Stone). The rescue Sansa believes is Dontos's gallant doing was in fact Littlefinger's design from the start — Dontos a disposable instrument. The escape removes Sansa from the realm's reach and binds her to Littlefinger, a pivot of her whole arc.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S106 causal-arc track — Littlefinger AGENT_IN (architect/executor), Dontos AGENT_IN (the courier who leads her out), Sansa VICTIM_IN (the manipulated extracted party); the beat is SUB_BEAT_OF the [Purple Wedding](purple-wedding); LOCATED_AT the Red Keep.)

## Quotes

> “Ser Dontos the Red was a skin of wine with legs. He could never have been trusted with a task of such enormity. He would have bungled it or betrayed me. No, all Dontos had to do was lead you from the castle . . . and make certain you wore your silver hair net.”

— Petyr Baelish to Sansa, ASOS Sansa VI (`sources/chapters/asos/asos-sansa-06.md:145`)
