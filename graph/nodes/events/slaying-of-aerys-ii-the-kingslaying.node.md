---
name: "The Kingslaying — Jaime slays Aerys II"
type: event.assassination
slug: slaying-of-aerys-ii-the-kingslaying
aliases: ["jaime-kills-aerys", "the-kingslaying", "death-of-aerys-ii-targaryen"]
confidence: tier-1
wiki_source: "https://awoiaf.westeros.org/index.php/Sack_of_King's_Landing"
era: roberts-rebellion
pass_origin: s106-causal-track
node_version: 1
occurred:
  ac_year: 283
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-recollection
  date_confidence: tier-2
victim: aerys-ii-targaryen
agents: ["jaime-lannister"]
---

## Identity

During the Sack of King's Landing, Ser Jaime Lannister of the Kingsguard slew the alchemist Rossart and then King Aerys II Targaryen at the foot of the Iron Throne — first cutting down the man carrying the king's burn-order to the pyromancers, then the king himself before he could send another. The act, which earned Jaime the lifelong epithet "Kingslayer," was a violation of his Kingsguard vow committed to prevent Aerys from immolating the city. It is the defining beat of Jaime's arc and the immediate consequence of Aerys's order to fire the wildfire caches.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S106 causal-arc track — Jaime AGENT_IN, Aerys II VICTIM_IN; the beat is TRIGGERED by [Aerys's burn-order](aerys-commands-the-city-burned) and is SUB_BEAT_OF the [Sack of King's Landing](sack-of-kings-landing); LOCATED_AT King's Landing.)

## Quotes

> "When I came on Rossart, he was dressed as a common man-at-arms, hurrying to a postern gate. I slew him first. Then I slew Aerys, before he could find someone else to carry his message to the pyromancers."

— Jaime to Brienne, ASOS Jaime V (`sources/chapters/asos/asos-jaime-05.md:63`)
