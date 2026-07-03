---
name: "Burning of the Seven at Dragonstone"
type: event.incident
slug: burning-of-the-seven-at-dragonstone
aliases: ["Stannis burns the Seven", "the burning of the gods at Dragonstone"]
confidence: tier-1
era: current-narrative
pass_origin: s155-stannis-enrich
node_version: 1
evidence_chapters:
  - ACOK Davos I
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
sort_keys:
  ac_year: 299
  book_order: 2
  chapter_number: 11
  chapter_label: "ACOK Davos I"
  composite: "0299.2.011"
  reading_order: "2.011"
  basis: "year+chapter"
---

# Burning of the Seven at Dragonstone

At Dragonstone's gates, before hundreds of the assembled host, [Melisandre](melisandre) burns the seven
wooden idols of the [Faith of the Seven](faith-of-the-seven) — Maid and Mother, Warrior and Smith, Crone,
Father and Stranger — praying once each in Asshai'i, High Valyrian, and the Common Tongue. Then
[Stannis](stannis-baratheon) plunges into the pyre and wrenches a sword free of the burning wood; the
queen's men proclaim it [Lightbringer](lightbringer), "the red sword of heroes." [Selyse](selyse-florent)
echoes the responses; [Davos](davos-seaworth), watching, "felt ill … and not only from the smoke." It is
the public act of [Stannis's conversion to R'hllor](rhllor) and his break with the Faith.

This node is the **R'hllor conversion engine** the spine entirely lacked: it lights
[Lightbringer](lightbringer)'s 0-edges-graph-wide island (`stannis WIELDS` + the sword `WIELDED_IN` the
burning) and anchors the new `stannis WORSHIPS rhllor` + `melisandre ADVISES stannis` edges.

**Theory-gated (node-prose, NOT edges):** that this sword IS the prophesied Lightbringer, that Stannis is
Azor Ahai reborn / the prince that was promised, and the whole R'hllor cosmology — all evidence-only.
Davos privately judges *"That sword was not Lightbringer"* (the heatless false-Lightbringer reading); the
text event is the burning + the drawing, not the prophecy.

## Quotes

> The red woman walked round the fire three times, praying once in the speech of Asshai, once in High Valyrian, and once in the Common Tongue.

> In ancient books of Asshai it is written that there will come a day after a long summer when the stars bleed and the cold breath of darkness falls heavy on the world. In this dread hour a warrior shall draw from the fire a burning sword.

> The Seven have never brought me so much as a sparrow. It is time I tried another hawk, Davos. A red hawk.
