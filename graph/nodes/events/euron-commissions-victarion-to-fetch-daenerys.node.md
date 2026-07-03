---
name: "Euron commissions Victarion to fetch Daenerys"
type: event.incident
slug: euron-commissions-victarion-to-fetch-daenerys
aliases: ["Euron commissions Victarion to fetch Daenerys", "Euron sends Victarion to Slaver's Bay", "Victarion's dragon-quest", "Euron's mission to fetch the dragon queen", "Euron gives Victarion the dragonhorn"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s116-enrichment
node_version: 1
evidence_chapters:
  - AFFC The Reaver I
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
sort_keys:
  ac_year: 300
  book_order: null
  chapter_number: null
  chapter_label: null
  composite: "0300.0.000"
  reading_order: null
  basis: "year-only"
---

## Identity

In the wake of the [taking of the Shields](taking-of-the-shields), King [Euron Greyjoy](euron-greyjoy) summons his brother [Victarion](victarion-greyjoy) privately at Lord Hewett's castle and gives him a charge: sail the [Iron Fleet](iron-fleet) across the world to [Slaver's Bay](slavers-bay), find the dragon queen [Daenerys Targaryen](daenerys-targaryen), and bring her — and her dragons — back to wed Euron and complete the conquest of Westeros he promised at the [kingsmoot](kingsmoot-on-old-wyk). Euron frames it as a dare ("Live a thrall or die a king. Do you dare to fly?"). Victarion accepts, drawing his own blood on it — but secretly resolves to take Daenerys for himself, the grudge from his [murdered salt wife](victarion-admits-euron-s-role-in-his-wife-s-death) turning the mission into a betrayal-in-waiting. **This is the Essos-bridge seed:** a terminal AFFC node whose downstream — Victarion's entire ADWD Slaver's Bay voyage — is left dark, to be wired by a later Essos-container pass (pre-placed here so the cross-book chain auto-joins).

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S116 enrichment pass. CAUSED by the [taking of the Shields](taking-of-the-shields) (the victory gives Euron the fleet, momentum, and the private moment to dispatch Victarion — CAUSES, Tier-2; the [kingsmoot](kingsmoot-on-old-wyk) is the distal enabler one hop further up the chain). [Euron Greyjoy](euron-greyjoy) is the orderer (COMMANDS_IN, Tier-1); [Victarion Greyjoy](victarion-greyjoy) undertakes it (AGENT_IN, Tier-1). Victarion's grudge ([victarion-admits-euron-s-role…](victarion-admits-euron-s-role-in-his-wife-s-death) MOTIVATES victarion-greyjoy) seeds his secret intent to betray the charge.)

## Quotes

> "The choice is yours, brother. Live a thrall or die a king. Do you dare to fly? Unless you take the leap, you'll never know."

— Euron Greyjoy, AFFC The Reaver I (`sources/chapters/affc/affc-the-reaver-01.md:281`)

> "I could sail the Iron Fleet to hell if need be." When Victarion opened his hand, his palm was red with blood. "I'll go to Slaver's Bay, aye. I'll find this dragon woman, and I'll bring her back." But not for you. You stole my wife and despoiled her, so I'll have yours. The fairest woman in the world, for me.

— Victarion Greyjoy, AFFC The Reaver I (`sources/chapters/affc/affc-the-reaver-01.md:285`)
