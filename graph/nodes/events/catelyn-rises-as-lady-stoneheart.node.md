---
name: "Catelyn rises as Lady Stoneheart"
type: event.incident
slug: catelyn-rises-as-lady-stoneheart
aliases: ["Lady Stoneheart revealed", "Catelyn Stark resurrected", "Catelyn rises as Stoneheart", "Beric's last kiss revives Catelyn", "Lady Stoneheart takes the Brotherhood"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s115-causal-track
node_version: 1
evidence_chapters:
  - ASOS Epilogue
  - AFFC Brienne VIII
occurred:
  ac_year: 299
  precision: approximate
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

Days after the [Red Wedding](red-wedding), the [Brotherhood Without Banners](brotherhood-without-banners) recovered [Catelyn Stark](catelyn-stark)'s corpse from the Trident — three days drowned, her throat slashed ear to ear. When [Thoros](thoros) refused the kiss of life as too long delayed, [Beric Dondarrion](beric-dondarrion) pressed his own lips to hers and passed the last flame of his life into her, and she rose: mute and ravaged, her flesh curdled white, her face raked to the skull. As Lady Stoneheart she displaced Beric at the head of the Brotherhood — "Lord Beric's fire has gone out of this world" — turning Beric's justice-seeking band into a vengeance cult that hangs Freys and Lannister men along the riverlands. Her transformation is the direct downstream consequence of [Catelyn is killed](catelyn-is-killed) at the Red Wedding, and the engine of the [capture and condemnation of Brienne](brienne-brought-before-lady-stoneheart).

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S115 causal-arc track. This event is CAUSED by [Catelyn is killed](catelyn-is-killed) (Tier-2) and in turn CAUSES [Brienne brought before Lady Stoneheart](brienne-brought-before-lady-stoneheart) (Tier-2). [Beric Dondarrion](beric-dondarrion), [Thoros](thoros), and the [Brotherhood Without Banners](brotherhood-without-banners) are AGENT_IN; [Catelyn Stark](catelyn-stark) is VICTIM_IN — the corpse acted upon. This is the cross-book hinge of the Brienne→Stoneheart arc: it roots at the already-built Red Wedding chain via `catelyn-is-killed`.)

## Quotes

> When she lowered her hood, something tightened inside Merrett's chest, and for a moment he could not breathe. *No. No, I saw her die.* . . . The flesh had gone pudding soft in the water and turned the color of curdled milk. Half her hair was gone and the rest had turned as white and brittle as a crone's. . . . But her eyes were the most terrible thing. Her eyes saw him, and they hated.

— Merrett Frey beholds the risen Catelyn, ASOS Epilogue (`sources/chapters/asos/asos-epilogue.md:169`)

> "The Freys slashed her throat from ear to ear. When we found her by the river she was three days dead. Harwin begged me to give her the kiss of life, but it had been too long. I would not do it, so Lord Beric put his lips to hers instead, and the flame of life passed from him to her. And . . . she rose."

— Thoros recounts the resurrection to Brienne, AFFC Brienne VIII (`sources/chapters/affc/affc-brienne-08.md:311`)

> "Lord Beric's fire has gone out of this world, I fear. A grimmer shadow leads us in his place."

— on Lady Stoneheart's command of the Brotherhood, AFFC Brienne VIII (`sources/chapters/affc/affc-brienne-08.md:159`)
