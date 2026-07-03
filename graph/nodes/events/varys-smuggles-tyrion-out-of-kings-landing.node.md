---
name: "Varys smuggles Tyrion out of King's Landing"
type: event.incident
slug: varys-smuggles-tyrion-out-of-kings-landing
aliases: ["Tyrion's escape into exile", "Varys spirits Tyrion away"]
confidence: tier-1
containers: [wo5k]
era: current-narrative
pass_origin: s139-tywin-death-enrich
node_version: 1
evidence_chapters:
  - ASOS Tyrion XI
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
sort_keys:
  ac_year: 300
  book_order: 3
  chapter_number: 78
  chapter_label: "ASOS Tyrion XI"
  composite: "0300.3.078"
  reading_order: "3.078"
  basis: "year+chapter"
---

## Identity

After [Jaime Lannister](jaime-lannister) freed him from the black cells, [Tyrion Lannister](tyrion-lannister) was led by [Varys](varys) — who had dosed the gaolers' wine with sweetsleep and disguised himself in a septon's robe — down through the dungeons and secret passages of the [Red Keep](red-keep), bound for the sewers, the river, and a galley waiting in Blackwater Bay to carry him to the Free Cities. Tyrion's detour to kill [Shae](shae) and [Tywin](tywin-lannister) happened mid-escape; Varys then continued spiriting him out. The escape that launches Tyrion's exile arc (Pentos, Illyrio, the road to Daenerys). A SUB_BEAT_OF the Tywin-death sequence; forward-wires into the ADWD Essos arc.

## Edges

(Role/causal edges live in `graph/edges/edges.jsonl`, S139 Tywin-death enrichment. [Jaime frees Tyrion](jaime-frees-tyrion-from-the-black-cells) ENABLES this; [Varys](varys) + [Tyrion](tyrion-lannister) AGENT_IN; LOCATED_AT [red-keep](red-keep).)

## Quotes

> "You're going down into the sewers, and from there to the river. A galley is waiting in the bay. Varys has agents in the Free Cities who will see that you do not lack for funds . . . but try not to be conspicuous. Cersei will send men after you, I have no doubt. You might do well to take another name."

— Jaime relaying Varys's plan, ASOS Tyrion XI (`sources/chapters/asos/asos-tyrion-11.md:57`)
