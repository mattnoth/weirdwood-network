---
name: "Stannis's march on Winterfell"
type: event.incident
slug: stannis-march-on-winterfell
containers: [north]
aliases: ["Stannis marches on Winterfell", "the march on Winterfell", "Stannis's march from Deepwood Motte", "the march through the wolfswood"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s131-north-n6-remainder
node_version: 1
evidence_chapters:
  - ADWD The King's Prize (Asha I)
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

After winning [the fight by Deepwood Motte](fight-by-deepwood-motte) and the [battle beneath the Wall](battle-beneath-the-wall), [Stannis Baratheon](stannis-baratheon) leads his host out of Deepwood Motte and marches roughly a hundred leagues southeast through the wolfswood toward [Winterfell](winterfell), meaning to break [Roose Bolton](roose-bolton) and claim the North. The northern mountain clans (Wull, Norrey, Liddle, Flint) swell his ranks; his captive [Asha Greyjoy](asha-greyjoy) rides fettered in the baggage train, to be displayed in chains at Winterfell. Autumn snows turn the march into a crawl. The NORTH-theater campaign that bridges Stannis's victory at the Wall to his army's eventual snowbound stall — and terminates, in published text, short of the unwritten battle for Winterfell.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S131 NORTH N6 remainder pass. ENABLED by [the fight by Deepwood Motte](fight-by-deepwood-motte) — the victory that gives Stannis the castle, the mountain clans, and the staging ground (ENABLES, Tier-2). [Stannis Baratheon](stannis-baratheon) leads it (AGENT_IN); [Asha Greyjoy](asha-greyjoy) is the fettered captive carried along (VICTIM_IN). ENABLES the army's [stall at the crofters' village](stannis-s-army-stalls-at-crofters-village) downstream. NOT wired to the unwritten Battle of Ice / `battle-of-winterfell` — the NORTH container terminates here.)

## Quotes

> The king's host departed Deepwood Motte by the light of a golden dawn, uncoiling from behind the log palisades like a long, steel serpent emerging from its nest.

— ADWD The King's Prize (`sources/chapters/adwd/adwd-the-kings-prize-01.md:11`)

> Asha Greyjoy rode in the baggage train, in a covered wayn with two huge iron-rimmed wheels, fettered at wrist and ankle … His Grace King Stannis was taking no chances on his prize escaping captivity.

— ADWD The King's Prize (`sources/chapters/adwd/adwd-the-kings-prize-01.md:19`)
