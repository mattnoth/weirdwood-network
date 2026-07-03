---
name: "Tyrion's sortie at the King's Gate"
type: event.battle
slug: tyrion-s-sortie-at-the-king-s-gate
aliases: ["Tyrion leads the sortie", "the King's Gate sortie"]
confidence: tier-1
containers: [wo5k]
era: current-narrative
pass_origin: s138-bw-enrich
node_version: 1
evidence_chapters:
  - ACOK Tyrion XIII
  - ACOK Tyrion XIV
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
sort_keys:
  ac_year: 299
  book_order: 2
  chapter_number: 60
  chapter_label: "ACOK Tyrion XIII"
  composite: "0299.2.060"
  reading_order: "2.060"
  basis: "year+chapter"
---

## Identity

After [Sandor Clegane](sandor-clegane) refused to lead another sortie into the fire, [Tyrion Lannister](tyrion-lannister) personally led a mounted sortie out the sally port of the King's Gate, dispersing the battering-ram party and routing Stannis's men along the burning riverfront ("So come with me and kill the son of a bitch!"). The sortie carried him onto the bridge of ships, where [Ser Mandon Moore](mandon-moore) attempted to murder him. A SUB_BEAT_OF the [Battle of the Blackwater](battle-of-the-blackwater).

## Edges

(Role/causal edges live in `graph/edges/edges.jsonl`, S138 BW enrichment. SUB_BEAT_OF battle-of-the-blackwater; [Tyrion Lannister](tyrion-lannister) AGENT_IN; caused by [Sandor's refusal](sandor-clegane-deserts-the-kingsguard); ENABLES [the attack on Tyrion](a-knight-attacks-tyrion-s-shield).)

## Quotes

> "You won't hear me shout out Joffrey's name," he told them. "You won't hear me yell for Casterly Rock either. This is your city Stannis means to sack, and that's your gate he's bringing down. So come with me and kill the son of a bitch!"

— Tyrion Lannister to the gold cloaks, ACOK Tyrion XIII (`sources/chapters/acok/acok-tyrion-13.md:87`)
