---
name: "Stannis's army stalls at the crofters' village"
type: event.incident
slug: stannis-s-army-stalls-at-crofters-village
containers: [north]
aliases: ["Stannis's army stalls in the blizzard", "the host snowbound at the crofters' village", "Stannis's host snowbound", "the stall at the crofters' village"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s131-north-n6-remainder
node_version: 1
evidence_chapters:
  - ADWD The King's Prize (Asha I)
  - ADWD The Sacrifice (Asha II)
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

Three days short of Winterfell, [Stannis Baratheon's](stannis-baratheon) host halts at an abandoned crofters' village between two frozen lakes, and a relentless blizzard then pins it there — snowbound, starving, the horses slaughtered for meat (eight hundred down to sixty-four), men freezing in the dark. The campaign grinds to a dead stop; the king will not retreat. This is the army's last state in published ADWD: trapped in the snow with Winterfell still ahead and Roose Bolton waiting behind its walls. The downstream — the relief from Braavos (Tycho Nestoris), the Karstark treachery, and the battle itself — lies in unwritten territory.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S131 NORTH N6 remainder pass. ENABLED by [Stannis's march on Winterfell](stannis-march-on-winterfell) — the march put the host in the open wolfswood where the blizzard caught it; the stall's proximate cause is the weather, so ENABLES not CAUSES (Tier-2). [Stannis Baratheon](stannis-baratheon) is the commander whose campaign is trapped and starving (VICTIM_IN). The NORTH container's terminus — nothing downstream is wired, as the relief, the Karstark betrayal, and the Battle of Ice are all unwritten.)

## Quotes

> Somewhere ahead Roose Bolton awaited them behind the walls of Winterfell, but Stannis Baratheon's host sat snowbound and unmoving, walled in by ice and snow, starving.

— ADWD The King's Prize (`sources/chapters/adwd/adwd-the-kings-prize-01.md:261`)

> "We had eight hundred horses when we marched from Deepwood Motte. Last night the count was sixty-four."

— Justin Massey, ADWD The Sacrifice (`sources/chapters/adwd/adwd-the-sacrifice-01.md:139`)

> Any horse that went down was butchered on the spot for meat.

— ADWD The King's Prize (`sources/chapters/adwd/adwd-the-kings-prize-01.md:191`) — hospitality-inversion: the host eats its own mounts

## Foreshadowing

> They had been three days from Winterfell for nineteen days.

— ADWD The Sacrifice (`sources/chapters/adwd/adwd-the-sacrifice-01.md:47`) — the ironic crystallization of the stall: forever "three days away" as the blizzard freezes the campaign in place
