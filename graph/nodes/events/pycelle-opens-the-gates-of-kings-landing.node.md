---
name: "Pycelle convinces Aerys to open the gates"
type: event.deception
slug: pycelle-opens-the-gates-of-kings-landing
aliases: ["pycelle-bids-aerys-open-the-gates", "pycelle-betrays-aerys-to-tywin"]
confidence: tier-1
wiki_source: "https://awoiaf.westeros.org/index.php/Sack_of_King's_Landing"
era: roberts-rebellion
pass_origin: s106-causal-track
node_version: 1
occurred:
  ac_year: 283
  precision: year
  basis_source: wiki-page
  basis_reliability: secondary-canon
  date_confidence: tier-2
staged_by: pycelle
audience: aerys-ii-targaryen
false_belief: "Lord Tywin Lannister and his host came to King's Landing as loyal friends of the crown; opening the gates served the king."
payoff: "Aerys admitted Tywin's army into the capital, which then sacked the city."
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

Grand Maester Pycelle, having privately judged Robert's Rebellion lost after Rhaegar's death at the Trident and hoping Lord Tywin Lannister would become the new king, counseled the Mad King Aerys II to open the gates of King's Landing to Tywin's approaching host. The host had not come as a friend: once inside, it sacked the city. The persuasion is a betrayal-from-within — the realm's senior maester using his trusted counsel against the king he served — which is why it is modeled as an `event.deception` rather than mere counsel. It is the enabling hinge of the Sack: without the gates, Tywin's army is outside the walls.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S106 causal-arc track — Pycelle AGENT_IN; the beat CAUSES the [Sack of King's Landing](sack-of-kings-landing) and is SUB_BEAT_OF it; LOCATED_AT King's Landing.)

## Quotes

> Always . . . for years . . . your lord father, ask him, I was ever his true servant . . . ’twas I who bid Aerys open his gates

— Pycelle confessing to Tyrion, ACOK Tyrion VI (`sources/chapters/acok/acok-tyrion-06.md:291`)
