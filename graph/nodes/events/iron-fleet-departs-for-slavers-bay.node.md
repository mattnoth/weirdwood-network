---
name: "Iron Fleet's voyage to Slaver's Bay"
type: event.incident
slug: iron-fleet-departs-for-slavers-bay
containers: [essos]
aliases: ["Iron Fleet departs for Slaver's Bay", "Victarion sails east for Meereen", "the Iron Fleet's voyage to Meereen", "Victarion's voyage to fetch Daenerys", "the Iron Fleet's Slaver's Bay voyage"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s131-aegon-victarion-remainder
node_version: 1
evidence_chapters:
  - AFFC The Reaver I
  - ADWD The Iron Suitor (Victarion I)
  - ADWD Victarion (Victarion II)
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

Acting on [Euron's charge](euron-commissions-victarion-to-fetch-daenerys), [Victarion Greyjoy](victarion-greyjoy) leads the [Iron Fleet](iron-fleet) across the world to [Slaver's Bay](slavers-bay) to find [Daenerys Targaryen](daenerys-targaryen) and bring her — and her dragons — back to Westeros. He splits the great fleet into three squadrons for the crossing; a storm a day out of Old Volantis scatters and sinks many ships, so only four-and-fifty regroup off the Isle of Cedars (ADWD *The Iron Suitor*), where the red priest [Moqorro](moqorro) is fished from the sea and taken aboard. Pressing east toward Meereen (ADWD *Victarion*), the fleet takes a string of prizes — the *Ghiscari Dawn*, the Myrish cog *Dove*, two galleys, and the slaver galley *Willing Maiden* — freeing the chained rowers and sacrificing captives to the Drowned God along the way. The voyage hub for the whole Victarion ADWD thread; it terminates in-saga with the fleet entering Meereenese home waters (the arrival at the bay is TWOW, out of scope).

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S131 AEGON-Victarion remainder pass. ENABLED by [Euron's commission](euron-commissions-victarion-to-fetch-daenerys) — wires the dangling AFFC bridge node downstream (ENABLES, Tier-2). [Victarion Greyjoy](victarion-greyjoy) commands it (AGENT_IN); the [Iron Fleet](iron-fleet) is the instrument host (AGENT_IN). The scattered voyage beats are grouped here as SUB_BEAT_OF this hub: the four prize-captures, the freeing of the rowers, the seven-girls sacrifice, the crew's call for Moqorro's death, the killing of Maester Kerwin, and Moqorro's reading of the Dragonbinder glyphs.)

## Quotes

> "I could sail the Iron Fleet to hell if need be." When Victarion opened his hand, his palm was red with blood. "I'll go to Slaver's Bay, aye. I'll find this dragon woman, and I'll bring her back."

— Victarion Greyjoy, AFFC The Reaver I (`sources/chapters/affc/affc-the-reaver-01.md:285`)

> Near the end, before the smoking ketch was swallowed by the sea, the cries of the seven sweetlings changed to joyous song, it seemed to Victarion Greyjoy. A great wind came up then, a wind that filled their sails and swept them north and east and north again, toward Meereen and its pyramids of many-colored bricks.

— ADWD Victarion (`sources/chapters/adwd/adwd-victarion-01.md:97`)

> As the sea crashed around him and the deck rose and fell beneath his feet, he had seen Dagon's Feast and Red Tide slammed together so violently that both exploded into splinters. My brother's work, he'd thought.

— Victarion in the first storm a day out of Old Volantis — the voyage's opening loss, which scatters and sinks much of the Iron Fleet, ADWD The Iron Suitor (`sources/chapters/adwd/adwd-the-iron-suitor-01.md:25`) [storm out of Old Volantis — opening loss]
