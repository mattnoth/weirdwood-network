---
slug: stone-men-attack-the-shy-maid
containers: [aegon]
type: event.incident
name: "Stone men attack the Shy Maid"
status: minted-plate3
minted_at: 2026-06-07T20:47:21.390929+00:00
evidence_chapters:
  - ADWD Tyrion V
sort_keys:
  ac_year: null
  book_order: 5
  chapter_number: 19
  chapter_label: "ADWD Tyrion V"
  composite: null
  reading_order: "5.019"
  basis: "chapter-only"
---

# Stone men attack the Shy Maid

Event node minted by Plate 3 full-corpus scan for: Stone men attack the Shy Maid

## Edges
(populated by Plate 3 role-edge staging; merge at Plate 5)

## Greyscale — Jon Connington's infection vector (S161 book-cite overlay)
This attack is **where Jon Connington (Griff) contracted greyscale**: he went into the Rhoyne to pull
the sinking Tyrion out, and was infected. (The greyscale-scare seam — `jon-connington AFFLICTED_BY
greyscale` + `greyscale MOTIVATES jon-connington`, his death-clock — was built S147.) The S161
fresh-verify rejected an `ENABLES greyscale` edge here as grammatically broken (event→disease), so the
seam is recorded as navigable book-cited prose instead.

> "It was Lemore who forced the water from your lungs after Griff had pulled you up. You were as cold as ice, and your lips were blue."

— Haldon to Tyrion, ADWD Tyrion VI (`sources/chapters/adwd/adwd-tyrion-06.md:21`)

## Notes
Node minted by `edge-reify-backfill.py --batch` during Plate 3 mini-batch run.
Staging only — do NOT promote to graph/nodes/events/ until Plate 5 gated merge.
