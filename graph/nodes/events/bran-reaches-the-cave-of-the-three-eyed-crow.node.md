---
name: "Bran reaches the cave of the three-eyed crow"
type: event.incident
slug: bran-reaches-the-cave-of-the-three-eyed-crow
aliases: ["arrival at the greenseer's cave", "the wight attack at the cave mouth", "Bran reaches Bloodraven"]
confidence: tier-1
era: war-of-the-five-kings
containers: [bran]
pass_origin: s130-bran-br6
node_version: 1
evidence_chapters:
  - ADWD Bran II
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-witnessed
  date_confidence: tier-2
---

## Identity

On the final approach to the [cave](cave-of-the-three-eyed-crow), wights rise from the snow; [Bran](bran-stark) wargs [Hodor](hodor) to fight, and [Leaf](leaf) and the children of the forest drive the dead back with fire and bring the party inside. There [Bran](bran-stark) meets [Brynden Rivers](brynden-rivers) — the last greenseer, enthroned in weirwood roots — who tells him *"You will never walk again, Bran, but you will fly."* The wight attack is folded in as the obstacle sub-beat; the load-bearing moment is the arrival and the meeting.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S130 BRAN track / BR6. [Meeting Coldhands](bran-meets-coldhands) ENABLES reaching the cave (his escort brings them). Roles Tier-1: [Bran](bran-stark) AGENT_IN (wargs Hodor to fight — agency preserved); [Leaf](leaf) AGENT_IN (the fire-rescue); [Coldhands](coldhands) AGENT_IN (brings them, fights the wights but cannot enter); [Meera](meera-reed) AGENT_IN (spears a wight); [Brynden Rivers](brynden-rivers) AGENT_IN (receives them). All greenseer/crow edges target `brynden-rivers`, NOT the `three-eyed-crow` species node. This arrival CAUSES [Bran becoming a greenseer](bran-becomes-a-greenseer).)

## Quotes

> "I have been many things, Bran. Now I am as you see me, and now you will understand why I could not come to you... except in dreams."

— Bloodraven's first words to Bran inside the cave. Bran POV, ADWD Bran II (`sources/chapters/adwd/adwd-bran-02.md:197`)

> "You will never walk again, Bran," the pale lips promised, "but you will fly."

— Bloodraven's promise — the structural echo of the coma-crow's "fly or die." Bran POV, ADWD Bran II (`sources/chapters/adwd/adwd-bran-02.md:205`)
