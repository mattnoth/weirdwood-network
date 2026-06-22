---
name: "Death of Khal Drogo"
type: event.death
slug: death-of-khal-drogo
aliases: ["death of Khal Drogo", "Drogo's death", "Drogo dies", "the khal dies", "Daenerys smothers Drogo", "Dany ends Drogo's life", "the mercy killing of Drogo", "death of Drogo", "who killed Khal Drogo"]
confidence: tier-1
era: roberts-reign
containers: [essos]
pass_origin: s119-essos-root-track
node_version: 1
evidence_chapters:
  - AGOT Daenerys IX
occurred:
  ac_year: 298
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

[Mirri Maz Duur's ritual](drogo-blood-magic-ritual) leaves [Khal Drogo](drogo) alive but empty — his eyes open but unseeing, blind and beyond reach, the wound on his breast healed into a grey and hideous scar while the man within is gone. His khalasar has scattered; forty thousand riders are reduced to a hundred. [Daenerys Targaryen](daenerys-targaryen), unwilling to leave her sun-and-stars a mindless husk, takes a feather cushion from the tent, kisses him a final time, and presses it down across his face — a mercy killing by her own hand ("If I look back I am lost"). Drogo's death is the immediate trigger for the funeral pyre on which the [dragons hatch](dragon-hatching-on-drogo-pyre): Dany builds the pyre for his body, places the petrified eggs around him, binds Mirri to the wood, and walks into the flames.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S119 essos-root track. [Daenerys](daenerys-targaryen) is the agent of the mercy-killing (AGENT_IN, Tier-1); [Drogo](drogo) is the subject (VICTIM_IN, Tier-1). Caused by [Mirri Maz Duur's ritual](drogo-blood-magic-ritual) (CAUSES, Tier-2). The death CAUSES the [dragon hatching on Drogo's pyre](dragon-hatching-on-drogo-pyre) (Tier-2 — fresh-verify adjusted from TRIGGERS, since Dany's pyre-building and walking into the fire mediate between the death and the hatching).)

## Quotes

> His eyes were wide open but did not see, and she knew at once that he was blind. When she whispered his name, he did not seem to hear. The wound on his breast was as healed as it would ever be, the scar that covered it grey and red and hideous.

— Daenerys finds Drogo's husk, AGOT Daenerys IX (`sources/chapters/agot/agot-daenerys-09.md:163`)

> She knelt, kissed Drogo on the lips, and pressed the cushion down across his face.

— AGOT Daenerys IX (`sources/chapters/agot/agot-daenerys-09.md:213`)
