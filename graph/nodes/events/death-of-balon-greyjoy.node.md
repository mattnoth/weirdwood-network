---
name: "Death of Balon Greyjoy"
type: event.death
slug: death-of-balon-greyjoy
aliases: ["death of Balon Greyjoy", "Balon Greyjoy's death", "Balon Greyjoy dies", "Balon falls from the bridge", "Balon falls at Pyke", "the death of the Iron King", "assassination of Balon Greyjoy", "murder of Balon Greyjoy", "who killed Balon Greyjoy"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s116-causal-track
node_version: 1
evidence_chapters:
  - AFFC The Prophet I
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

[Balon Greyjoy](balon-greyjoy), King of the Iron Islands, fell to his death while crossing one of the rope-and-plank bridges of [Pyke](pyke) during a storm, dashed upon the rocks below. The news reached his youngest brother, the priest [Aeron Damphair](aeron-greyjoy), on [Great Wyk](great-wyk), carried by riders of [House Goodbrother](house-goodbrother) and [House Sparr](house-sparr). Aeron declared the death the work of the Storm God — "My brother Balon made us great again, which earned the Storm God's wrath" — framing it as the latest blow in the eternal war between sea and sky. The text leaves the agency of the fall ambiguous (storm, accident, or a god's hand); the later fan reading that [Euron](euron-greyjoy) hired a Faceless Man to murder Balon is never asserted in AFFC and is not modeled here. Balon's death is the prime mover of the Iron Islands succession crisis: it instantly reopens the Seastone Chair and removes the only obstacle to Euron's return from exile.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S116 causal-arc track. This is the standalone root of the Kingsmoot → Euron arc — Balon's death is the prime mover, with no causal upstream by design. [Balon Greyjoy](balon-greyjoy) is the subject (VICTIM_IN, Tier-1). The death TRIGGERS [Euron's seizure of the Seastone Chair](euron-seizes-the-seastone-chair) (Tier-2).)

## Quotes

> "The king is dead," he said, as plain as that. Four small words, yet the sea itself trembled when he uttered them.

— a Sparr rider brings Aeron the news, AFFC The Prophet I (`sources/chapters/affc/affc-the-prophet-01.md:63`)

> "His Grace was crossing a bridge at Pyke when he fell and was dashed upon the rocks below." ... "Was the storm raging when he fell?" Aeron demanded of them. "Aye," the youth said, "it was."

— AFFC The Prophet I (`sources/chapters/affc/affc-the-prophet-01.md:69`)

> "The Storm God cast him down," the priest announced. ... "My brother Balon made us great again, which earned the Storm God's wrath."

— Aeron Damphair, AFFC The Prophet I (`sources/chapters/affc/affc-the-prophet-01.md:75`)
