---
name: "The wine merchant attempts to poison Dany"
type: event.assassination
slug: the-wine-merchant-attempts-to-poison-dany
aliases: ["the wine merchant attempts to poison Daenerys", "the poisoned wine attempt", "the wineseller tries to poison Dany", "the assassination attempt at Vaes Dothrak", "the Lyseni wine merchant", "the attempt on Daenerys at the Western Market", "the poisoned Arbor wine"]
confidence: tier-1
era: roberts-reign
pass_origin: s119-essos-root-track
node_version: 2
evidence_chapters:
  - AGOT Daenerys VI
occurred:
  ac_year: 298
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

At the Western Market of [Vaes Dothrak](vaes-dothrak), a smooth Lyseni wine merchant presses a cask of fine Arbor red on [Daenerys Targaryen](daenerys-targaryen) as a gift for [Khal Drogo](drogo) — "One taste, and you will name your child after me." [Jorah Mormont](jorah-mormont), returning from the caravan captain with warning, forces the seller to drink first; the man flings the cask aside and flees, and is run down. The wine is poisoned: this is the first execution of [Robert Baratheon's order](robert-orders-daenerys-assassination) to kill the pregnant Daenerys, carried out through [Varys's](varys) channels. The attempt does not merely fail — it backfires, enraging Drogo and moving him to swear his [westward vow](drogo-westward-vow) to cross the poison water and take the Iron Throne for his son. Daenerys's reaction crystallizes the consequence: "The Usurper has woken the dragon now."

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`. [Robert Baratheon](robert-baratheon) is the orderer (COMMANDS_IN, Tier-1); the wineseller is the agent (AGENT_IN, Tier-1); [Daenerys](daenerys-targaryen) is the target (VICTIM_IN, Tier-1). Caused by [Robert's assassination order](robert-orders-daenerys-assassination) (CAUSES, Tier-2). The attempt CAUSES [Drogo's westward vow](drogo-westward-vow) and MOTIVATES [Drogo](drogo) (Tier-2). Node repaired S119 essos-root track [was a bare Plate-3 skeleton].)

## Appearances & Description

The wine merchant is a small man, slender and handsome, his flaxen hair curled and perfumed after the fashion of Lys — a Lysene fashion note that Jorah later uses to identify him as a spy rather than a legitimate trader. (`sources/chapters/agot/agot-daenerys-06.md:83`) [book-cite overlay; the "fashion of Lys" tells Jorah the man's true origin]

## Quotes

> "A taste for the khaleesi? ... A cask, a cup, a swallow? One taste, and you will name your child after me."

— the Lyseni wine merchant, AGOT Daenerys VI (`sources/chapters/agot/agot-daenerys-06.md:83`)

> She did not realize that Ser Jorah had returned until she heard the knight say, "No." His voice was strange, brusque. "Aggo, put down that cask."

— AGOT Daenerys VI (`sources/chapters/agot/agot-daenerys-06.md:105`)
