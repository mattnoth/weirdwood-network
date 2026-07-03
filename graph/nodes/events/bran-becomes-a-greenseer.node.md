---
name: "Bran becomes a greenseer"
type: event.incident
slug: bran-becomes-a-greenseer
aliases: ["Bran eats the weirwood paste", "Bran opens his third eye", "Bran's first greensight"]
confidence: tier-1
era: war-of-the-five-kings
containers: [bran]
pass_origin: s130-bran-br7
node_version: 1
evidence_chapters:
  - ADWD Bran III
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-witnessed
  date_confidence: tier-2
sort_keys:
  ac_year: 300
  book_order: 5
  chapter_number: 35
  chapter_label: "ADWD Bran III"
  composite: "0300.5.035"
  reading_order: "5.035"
  basis: "year+chapter"
---

## Identity

[Leaf](leaf) feeds [Bran](bran-stark) a weirwood paste; [Brynden Rivers](brynden-rivers) instructs him to *go into the roots*. Bran eats, opens the third eye, slips into the weirwood net and sees his father [Eddard](eddard-stark) in the Winterfell godswood — his first greenseer vision. This is the container's hard terminus as of ADWD: the making of the last greenseer, from the tower window to the weirwood throne. (This greensight is categorically distinct from the warg-sight third eye that opened in the crypts — do not conflate.)

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S130 BRAN track / BR7 — CONTAINER TERMINUS. [Reaching the cave](bran-reaches-the-cave-of-the-three-eyed-crow) CAUSES this transformation (the paste + instruction transform Bran — the one CAUSES in the journey chain). Roles Tier-1: [Bran](bran-stark) AGENT_IN ("He ate" — his own choice); [Leaf](leaf) AGENT_IN (administers the paste); [Brynden Rivers](brynden-rivers) AGENT_IN (instructs). TERMINUS — the TWOW expansion of Bran's visions is out of scope.)

## Quotes

> "Your blood makes you a greenseer," said Lord Brynden. "This will help awaken your gifts and wed you to the trees."

— Bloodraven on the weirwood paste. Bran POV, ADWD Bran III (`sources/chapters/adwd/adwd-bran-03.md:157`)

> It tasted of honey, of new-fallen snow, of pepper and cinnamon and the last kiss his mother ever gave him.

— The weirwood-paste sensation. Bran POV, ADWD Bran III (`sources/chapters/adwd/adwd-bran-03.md:163`)

> "Close your eyes," said the three-eyed crow. "Slip your skin, as you do when you join with Summer. But this time, go into the roots instead."

— Bloodraven's greenseer instruction. Bran POV, ADWD Bran III (`sources/chapters/adwd/adwd-bran-03.md:167`)
