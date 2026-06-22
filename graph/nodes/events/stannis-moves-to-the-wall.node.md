---
name: "Stannis Baratheon sails north to the Wall"
type: event.incident
slug: stannis-moves-to-the-wall
aliases: ["Stannis moves to the Wall", "Stannis sails north to the Wall", "Stannis answers the Night's Watch plea", "Stannis Baratheon comes to the Wall", "Stannis relieves the Wall"]
confidence: tier-2
era: war-of-the-five-kings
containers: [wo5k, north]
pass_origin: s125-north-n2
node_version: 1
evidence_chapters:
  - ASOS Davos V
  - ASOS Davos VI
  - ASOS Jon XI
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

Beaten at the [Blackwater](battle-of-the-blackwater) and [retreated to Dragonstone](stannis-retreats-to-dragonstone) with a broken host, [Stannis Baratheon](stannis-baratheon) is at his lowest ebb — "the King of the Painted Table," holding little more than two castles and an uneasy alliance with [Salladhor Saan](salladhor-saan). It is from this diminished position that [Davos Seaworth](davos-seaworth), having intercepted the [Night's Watch](nights-watch)'s plea for aid, argues the case that reshapes Stannis's war: a king protects his people, or he is no king at all. Stannis sails north and brings his knights down upon [Mance Rayder](mance-rayder)'s host at the [Wall](the-wall), shattering the wildling assault and turning the contest for the Iron Throne, for the first time, toward the defense of the realm itself.

This node is the **WO5K → NORTH seam** — the bridge by which the southern war crosses into the northern theatre. Stannis's arrival is what makes the wildlings' [defeat at the Wall](battle-beneath-the-wall) and [Mance's capture and execution](mance-rayder-brought-to-execution) possible, and his presence at Castle Black becomes the gravity well around which the rest of Jon's Lord-Commander era turns.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S125 NORTH track / N2 — the NORTH pivot. [The retreat to Dragonstone](stannis-retreats-to-dragonstone) ENABLES this pivot (Tier-2 — the lowest-ebb position is the precondition that makes the Wall plea legible as opportunity, not its efficient cause). This movement CAUSES the wildlings' defeat at [battle-beneath-the-wall](battle-beneath-the-wall) (Tier-2 — **scoped to the rout**: Stannis's arrival and charge cause the wildlings' DEFEAT, not the battle's occurrence, which was Stannis-independent). The battle in turn CAUSES [Mance's capture and execution](mance-rayder-brought-to-execution). [Stannis Baratheon](stannis-baratheon) is the AGENT_IN. No duplicate node was minted for "Stannis routs the wildlings" — `battle-beneath-the-wall` already is that event. The NORTH spine walks: retreat ENABLES bridge CAUSES battle CAUSES execution.)

## Quotes

> "And I know that a king protects his people, or he is no king at all."

— Davos Seaworth's argument to Stannis, ASOS Davos VI (`sources/chapters/asos/asos-davos-06.md:203`)

> "Stannis might be the King of Westeros in name, but in truth he was the King of the Painted Table. He held Dragonstone and Storm's End, and had an ever-more-uneasy alliance with Salladhor Saan, but that was all. How could the Watch have looked to him for help? They may not know how weak he is, how lost his cause."

— Davos on Stannis's diminished state, the precondition for the pivot, ASOS Davos V (`sources/chapters/asos/asos-davos-05.md:283`)

> "Whilst your brothers have been struggling to decide who shall lead them, I have been speaking with this Mance Rayder."

— Stannis to Jon at the Wall, having sailed north and relieved the siege, ASOS Jon XI (`sources/chapters/asos/asos-jon-11.md:155`)

> "I know you held the gate here," King Stannis said. "If not, I would have come too late."

— Stannis to Jon, acknowledging the relief his arrival brought and the desperate defense that bought the time. ASOS Jon XI (`sources/chapters/asos/asos-jon-11.md:57`)
