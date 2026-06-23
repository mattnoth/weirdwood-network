---
name: "Edmure taken hostage at the Twins"
type: event.incident
slug: edmure-taken-hostage-at-the-twins
aliases: ["capture of Edmure Tully", "Edmure taken captive at the Twins", "Edmure Tully held hostage"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s134-rw-enrich
node_version: 1
evidence_chapters:
  - ASOS Catelyn VII
  - ASOS Tyrion VI
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

[Edmure Tully](edmure-tully) — the bridegroom whose wedding to [Roslin Frey](roslin-frey) was the bait for the Red Wedding — was taken captive rather than killed during the massacre and held hostage by [Walder Frey](walder-frey). His captivity became the lever that paralysed the Tully war effort: as [Tywin Lannister](tywin-lannister) notes, "so long as Walder Frey holds Edmure Tully hostage, the Blackfish dare not mount a threat." Edmure's hostage status is what later ENABLES the [siege of Riverrun](siege-of-riverrun) to end in surrender. A beat of the [Red Wedding](red-wedding).

## Edges

(Role/causal edges live in `graph/edges/edges.jsonl`, S134 RW enrichment. [Edmure Tully](edmure-tully) VICTIM_IN (Tier-1); [Walder Frey](walder-frey) AGENT_IN + [House Frey](house-frey) AGENT_IN (Tier-1); SUB_BEAT_OF [Red Wedding](red-wedding) (Tier-1); ENABLES [siege-of-riverrun](siege-of-riverrun) (Tier-1, fresh-verify).)

## Quotes

> "Riverrun remains, but so long as Walder Frey holds Edmure Tully hostage, the Blackfish dare not mount a threat."

— Tywin Lannister, ASOS Tyrion VI (`sources/chapters/asos/asos-tyrion-06.md:53`)
