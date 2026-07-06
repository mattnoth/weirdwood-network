---
name: "Death of Quentyn Martell"
type: event.death
slug: death-of-quentyn-martell
aliases: ["death of Quentyn Martell", "burning of Quentyn Martell", "Quentyn burned by Rhaegal", "Frog burned by the dragon", "how Quentyn Martell died"]
confidence: tier-1
era: war-of-the-five-kings
containers: [essos]
pass_origin: s120-essos-e5-track
node_version: 1
evidence_chapters:
  - ADWD The Dragontamer
  - ADWD The Queen's Hand
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
  narrative_first: "adwd-69"
sort_keys:
  ac_year: 300
  book_order: 5
  chapter_number: 69
  chapter_label: "ADWD The Dragontamer"
  composite: "0300.5.069"
  reading_order: "5.069"
  basis: "year+chapter"
---

## Identity

After [Quentyn Martell orders the attack](quentyn-orders-the-attack) on the dragon pit beneath the Great Pyramid — committing his sellsword allies to free Daenerys's chained dragons so he can claim one by Targaryen blood — the plan collapses into fire. While Quentyn is focused on lashing [Viserion](viserion) (the white dragon) into submission, [Rhaegal](rhaegal) (the green) strikes from behind: "Behind you, behind you, behind you!" Quentyn turns into the furnace wind and his whip-hand, then all of him, catches fire. He does not die at once — badly burned, he lingers for days in [Daenerys's](daenerys-targaryen) pyramid before dying just before first light, as [Ser Barristan Selmy](barristan-selmy) confirms. Archibald Yronwood was found cradling his prince's scorched body, his own hands burned from beating out the flames. Barristan's epitaph is terse: "Not all men are meant to dance with dragons." The death ends Doran Martell's Essos gambit and sends Quentyn's bones home to Dorne.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S120 essos-e5 track. TRIGGERED by [Quentyn ordering the attack](quentyn-orders-the-attack) (Tier-2 — the order sets off the fight that excites the dragons). [Quentyn](quentyn-martell) is the subject (VICTIM_IN, Tier-1); [Rhaegal](rhaegal) is the dragon-agent who burns him from behind (AGENT_IN, Tier-1). This segment is causally independent of the [Doran pact-reveal](doran-reveals-fire-and-blood-pact) — chronology forbids linking the reveal to a quest already underway; the two are joined through the shared Martell character nodes, not a causal edge.)

## Quotes

> When he raised his whip, he saw that the lash was burning. His hand as well. All of him, all of him was burning. Oh, he thought. Then he began to scream.

— Rhaegal's fire takes Quentyn, ADWD The Dragontamer (`sources/chapters/adwd/adwd-the-dragontamer-01.md:267`)

> So much of the prince’s flesh had sloughed away that he could see the skull beneath. His eyes were pools of pus. He should have stayed in Dorne. He should have stayed a frog. Not all men are meant to dance with dragons.

— Barristan looks on the dying prince, ADWD The Queen's Hand (`sources/chapters/adwd/adwd-the-queens-hand-01.md:39`)

> "Prince Quentyn died just before first light."

— ADWD The Queen's Hand (`sources/chapters/adwd/adwd-the-queens-hand-01.md:45`)

> "Fire and blood," he whispered, "blood and fire." The blood was pooling at his feet, soaking into the brick floor.

— Quentyn echoes the Targaryen words before the burning — a thematic bookend to Doran's "Fire and blood" whisper at affc-the-princess-in-the-tower-01.md:325, ADWD The Dragontamer (`sources/chapters/adwd/adwd-the-dragontamer-01.md:199`)

## Foreshadowing

> "And horses seldom turn their riders into charred bones and ashes."

— Gerris Drinkwater's dark joke to Quentyn, hours before the burning — the foreshadowing pays off exactly, ADWD The Dragontamer (`sources/chapters/adwd/adwd-the-dragontamer-01.md:77`)
