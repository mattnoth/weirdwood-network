---
name: "Tyrion accused of poisoning Joffrey"
type: event.incident
slug: tyrion-accused-of-poisoning-joffrey
aliases: ["tyrion-arrested-for-joffreys-murder", "cersei-accuses-tyrion-of-regicide"]
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

Immediately upon Joffrey's death at the wedding feast, Cersei Lannister accuses her brother Tyrion of poisoning the king, and Tyrion is seized and imprisoned. This is an **accusation and arrest**, not a factual poisoning by Tyrion — he is framed (the true plot is Littlefinger's, with the Tyrells). The graph models Tyrion here only as the accused/seized party. The accusation is the engine that drives Tyrion to trial.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S106 causal-arc track — Cersei AGENT_IN (the accuser; Tier-2), Tyrion VICTIM_IN (the framed party); the beat is TRIGGERED by the [death of Joffrey](death-of-joffrey-baratheon), CAUSES the [trial of Tyrion](trial-of-tyrion-lannister), and is SUB_BEAT_OF the [Purple Wedding](purple-wedding); LOCATED_AT the Red Keep.)

## Quotes

> "They think Tyrion poisoned Joffrey. Ser Dontos said they seized him."

— Sansa, ASOS Sansa V (`sources/chapters/asos/asos-sansa-05.md:157`)

> Could he truly have killed him? ... If Tyrion did it, they will think I was part of it as well, she realized with a start of fear.

— Sansa, ASOS Sansa V (`sources/chapters/asos/asos-sansa-05.md:53`)
