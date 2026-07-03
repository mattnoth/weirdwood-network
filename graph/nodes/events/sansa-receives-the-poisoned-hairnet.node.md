---
name: "Sansa receives the poisoned hair net"
type: event.deception
slug: sansa-receives-the-poisoned-hairnet
aliases: ["dontos-gives-sansa-the-hairnet", "the-silver-hairnet-with-the-strangler"]
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
false_belief: "The silver hair net set with black amethysts from Asshai is a magic charm that will carry Sansa safely home."
payoff: "One amethyst is the strangler; the net delivers the poison to Joffrey's wedding feast, and Sansa is the unwitting carrier."
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

Ser Dontos Hollard gives Sansa Stark a silver hair net strung with black amethysts from Asshai and insists she wear it to King Joffrey's wedding feast, telling her it is magic that will take her home. In truth one of the stones is the strangler, and Dontos is an unwitting courier for Petyr "Littlefinger" Baelish, who designed the delivery. The missing stone — later found absent from the net the night Joffrey dies — is the poison that killed the king. This beat is the instrument-delivery hinge of the Purple Wedding; the plot's true authors (Littlefinger, Olenna) are modeled on the death node, not here.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S106 causal-arc track — Dontos AGENT_IN, Sansa VICTIM_IN, Littlefinger COMMANDS_IN (Tier-2, revealed in his later confession); the beat CAUSES the [death of Joffrey](death-of-joffrey-baratheon) and is SUB_BEAT_OF the [Purple Wedding](purple-wedding); LOCATED_AT the Red Keep.)

## Quotes

> "There was murder in them!" "Softly, my lady, softly. No murder. He choked on his pigeon pie." ... "You poisoned him. You did. You took a stone from my hair . . ."

— Sansa confronting Dontos, ASOS Sansa V (`sources/chapters/asos/asos-sansa-05.md:41`)

> Black amethysts from Asshai. One of them was missing. ... There was a dark smudge in the silver socket where the stone had fallen out.

— ASOS Sansa V (`sources/chapters/asos/asos-sansa-05.md:23`)
