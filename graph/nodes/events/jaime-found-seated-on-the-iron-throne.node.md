---
name: "Jaime found seated on the Iron Throne"
type: event.incident
slug: jaime-found-seated-on-the-iron-throne
aliases: ["Jaime on the Iron Throne", "Ned finds Jaime on the throne", "the Kingslayer on the throne"]
confidence: tier-1
era: roberts-rebellion
pass_origin: s142-sack-kl-enrich
node_version: 1
evidence_chapters:
  - ASOS Jaime II
  - AGOT Eddard II
occurred:
  ac_year: 283
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-recollection
sort_keys:
  ac_year: 283
  book_order: 1
  chapter_number: 13
  chapter_label: "AGOT Eddard II"
  composite: "0283.1.013"
  reading_order: "1.013"
  basis: "year+chapter"
---

# Jaime found seated on the Iron Throne

Immediately after [slaying Aerys II](slaying-of-aerys-ii-the-kingslaying),
[Jaime Lannister](jaime-lannister) climbed the Iron Throne and seated himself with his gilded
sword across his knees, "to see who would come to claim the kingdom." It was
[Eddard Stark](eddard-stark) who rode the length of the throne room — between the rows of
dragon skulls, his northmen filling the hall behind him — to find the Kingslayer high above his
knights in a lion-crested helm, his sword's edge red with a king's blood. Jaime laughed, rose,
and claimed he had only been keeping the seat warm for Robert. Ned never asked, and never
forgot: the tableau seeds his lifelong contempt for Jaime. (Ned arrived AFTER Aerys was dead,
so he did not witness the killing itself — only this aftermath scene.)

## Edges
(Edges in `graph/edges/edges.jsonl`, S142 Sack-of-KL enrichment. SUB_BEAT_OF
[the kingslaying](slaying-of-aerys-ii-the-kingslaying); [Jaime](jaime-lannister) AGENT_IN;
[Ned](eddard-stark) WITNESS_IN; LOCATED_AT [the Iron Throne](iron-throne). The existing
`eddard-stark DISTRUSTS jaime-lannister` character edge is the downstream consequence.)

## Quotes

> Then he climbed the Iron Throne and seated himself with his sword across his knees, to see who would come to claim the kingdom. As it happened, it had been Eddard Stark.

— Jaime's recollection, ASOS Jaime II (`sources/chapters/asos/asos-jaime-02.md:303`)

> He was seated on the Iron Throne, high above his knights, wearing a helm fashioned in the shape of a lion's head. How he glittered!

— Ned to Robert, AGOT Eddard II (`sources/chapters/agot/agot-eddard-02.md:151`)
