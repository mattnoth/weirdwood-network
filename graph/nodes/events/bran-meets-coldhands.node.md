---
name: "Bran meets Coldhands"
type: event.incident
slug: bran-meets-coldhands
aliases: ["Coldhands meets the party beyond the Wall", "Bran's escort north of the Wall begins"]
confidence: tier-1
era: war-of-the-five-kings
containers: [bran]
pass_origin: s130-bran-br5
node_version: 1
evidence_chapters:
  - ADWD Bran I
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-witnessed
  date_confidence: tier-2
sort_keys:
  ac_year: 300
  book_order: 5
  chapter_number: 5
  chapter_label: "ADWD Bran I"
  composite: "0300.5.005"
  reading_order: "5.005"
  basis: "year+chapter"
---

## Identity

Beyond the Wall, [Bran](bran-stark)'s party joins [Coldhands](coldhands), the cloaked rider on the great elk who names their destination — *"A friend. Dreamer, wizard, call him what you will. The last greenseer."* Coldhands is the instrument of [Brynden Rivers](brynden-rivers): he escorts the party north toward the cave, fights off threats, but cannot enter the cave himself. He guides; he does not drive (the journey's purpose is Bloodraven's, not his).

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S130 BRAN track / BR5. [Passing the Black Gate](bran-passes-the-black-gate) ENABLES this meeting (crossing beyond the Wall is the precondition). Roles Tier-1: Bran, Coldhands AGENT_IN. Coldhands is modeled as Bloodraven's instrument — AGENT_IN the escort, NOT a causal driver. This meeting ENABLES [reaching the cave](bran-reaches-the-cave-of-the-three-eyed-crow).)

## Quotes

> "A friend. Dreamer, wizard, call him what you will. The last greenseer."

— Coldhands names their destination (Brynden Rivers). Bran POV, ADWD Bran I (`sources/chapters/adwd/adwd-bran-01.md:211`)
