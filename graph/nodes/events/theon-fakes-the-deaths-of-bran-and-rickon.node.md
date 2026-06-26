---
name: "Theon fakes the deaths of Bran and Rickon"
type: event.deception
slug: theon-fakes-the-deaths-of-bran-and-rickon
aliases: ["the false deaths of Bran and Rickon", "the miller's boys charade", "Theon's burned Stark boys"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s149-theon-reek-enrich
node_version: 1
evidence_chapters:
  - ACOK Theon V
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Theon fakes the deaths of Bran and Rickon

After [Bran](bran-stark) and [Rickon](rickon-stark) escape [Winterfell](winterfell) and the hunt
through the wolfswood fails to recover them, [Theon](theon-greyjoy) — unable to admit he has lost
the Stark boys — has *"Reek"* (in fact [Ramsay](ramsay-snow) in the dead servant's guise) murder the
two sons of the miller at the Acorn Water, **flay the skin from their faces and dip their heads in
tar**, and mounts the unrecognizable heads on Winterfell's walls as proof that the heirs of
[Ned Stark](eddard-stark) are dead. It is the moral nadir of Theon's ACOK arc and the textbook
`event.deception` (named as such in the data model). The false deaths propagate north as the news
that breaks [Robb](robb-stark). Only [Maester Luwin](luwin) has the stomach to come near and begs to
sew the heads back on for the crypts.

## Edges
(Edges in `graph/edges/edges.jsonl`, S149 Theon/Reek enrichment. CAUSES-in from
[the failed hunt](trail-followed-north-northwest); CAUSES-out to
[Robb's false news](robb-receives-false-news-of-brans-death); [Theon](theon-greyjoy) +
[Reek](reek) AGENT_IN; [the miller's sons](millers-sons) + [Bran](bran-stark) + [Rickon](rickon-stark)
VICTIM_IN; [Luwin](luwin) WITNESS_IN.)

## Quotes

> The miller's boys had been of an age with Bran and Rickon, alike in size and coloring, and once Reek had flayed the skin from their faces and dipped their heads in tar, it was easy to see familiar features in those misshapen lumps of rotting flesh. People were such fools. If we'd said they were rams' heads, they would have seen horns.

> Only Maester Luwin had the stomach to come near. Stone-faced, the small grey man had begged leave to sew the boys' heads back onto their shoulders, so they might be laid in the crypts below with the other Stark dead.
