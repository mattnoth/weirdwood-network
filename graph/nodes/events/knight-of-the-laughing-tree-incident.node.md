---
name: "Knight of the Laughing Tree incident"
type: event.incident
slug: knight-of-the-laughing-tree-incident
aliases: ["Knight of the Laughing Tree incident", "the mystery knight at Harrenhal", "Laughing Tree incident"]
confidence: tier-1
era: roberts-rebellion
pass_origin: s133-rr-enrich
node_version: 1
evidence_chapters:
  - ASOS Bran II
occurred:
  ac_year: 281
  precision: year
  basis_source: book-chapter
  basis_reliability: second-hand-oral
  date_confidence: tier-2
sort_keys:
  ac_year: 281
  book_order: 3
  chapter_number: 25
  chapter_label: "ASOS Bran II"
  composite: "0281.3.025"
  reading_order: "3.025"
  basis: "year+chapter"
---

## Identity

At the [Tourney at Harrenhal](tourney-at-harrenhal) a mystery knight appeared in mismatched patchwork armour bearing a shield painted with a weirwood-faced laughing tree. The [little crannogman Howland Reed](howland-reed) had been set upon and beaten by three squires the day before; the mystery knight challenged the three knights those squires served, unhorsed all three, and demanded only "teach your squires honor" as ransom for their armour and horses. [King Aerys II](aerys-ii-targaryen) was furious and dispatched his son [Prince Rhaegar](rhaegar-targaryen) to unmask the knight, but when Rhaegar came he found only the painted shield hanging abandoned in a tree. The knight's identity remains ungated in the published text, though the surrounding narrative strongly implies insider knowledge among the Stark-Reed circle. The incident is a direct sub-beat of the Tourney at Harrenhal and seeds the Lyanna-Rhaegar strand of the Robert's Rebellion arc.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S133 RR enrichment pass. The incident is a [SUB_BEAT_OF](tourney-at-harrenhal) the Tourney at Harrenhal (Tier-1). [Knight of the Laughing Tree](knight-of-the-laughing-tree) FIGHTS_IN (Tier-1); [Howland Reed](howland-reed) VICTIM_IN (the beaten crannogman; Tier-1); [Aerys II](aerys-ii-targaryen) WITNESS_IN (angered spectator who orders the unmasking; Tier-1); [Rhaegar Targaryen](rhaegar-targaryen) AGENT_IN (sent to unmask; Tier-1). [Lyanna Stark](lyanna-stark) SUSPECTED_OF the mystery-knight identity (Tier-2, GATED — identity not confirmed in published canon).)

## Quotes

> "The little crannogman was walking across the field, enjoying the warm spring day and harming none, when he was set upon by three squires. They were none older than fifteen, yet even so they were bigger than him, all three."

— ASOS Bran II (`sources/chapters/asos/asos-bran-02.md:179`)

> "The king was wroth, and even sent his son the dragon prince to seek the man, but all they ever found was his painted shield, hanging abandoned in a tree."

— ASOS Bran II (`sources/chapters/asos/asos-bran-02.md:229`)
