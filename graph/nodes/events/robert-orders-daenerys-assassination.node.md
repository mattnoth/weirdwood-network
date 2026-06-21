---
name: "Robert orders Daenerys's assassination"
type: event.assassination
slug: robert-orders-daenerys-assassination
aliases: ["Robert orders Daenerys killed", "Robert orders the assassination of Daenerys", "the order to kill Daenerys", "Robert's assassination order", "I want them dead mother and child both", "the small council votes to kill Daenerys", "Robert orders the Targaryen girl killed", "the order to murder the Targaryen children"]
confidence: tier-1
era: roberts-reign
pass_origin: s119-essos-root-track
node_version: 1
evidence_chapters:
  - AGOT Eddard VIII
occurred:
  ac_year: 298
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

In a session of the small council at [King's Landing](kings-landing), [King Robert Baratheon](robert-baratheon), on learning from [Varys](varys) that [Daenerys Targaryen](daenerys-targaryen) is pregnant with [Khal Drogo](drogo)'s child, orders her death — "I want them dead, mother and child both, and that fool [Viserys](viserys-targaryen) as well." [Eddard Stark](eddard-stark), then Hand of the King, refuses to countenance the murder of a child and a pregnant girl, calls it dishonorable, and resigns the Handship in protest when Robert will not relent. The council nonetheless approves the king's will, and the order goes out through Varys's channels — its first execution is the [wine merchant's poisoning attempt](the-wine-merchant-attempts-to-poison-dany) at Vaes Dothrak. This is the prime mover of the Westeros→Essos thread: the order (and the attempt that follows) is what wakes the dragon in Drogo and pushes him toward his vow to cross the poison water. Ned's later, futile attempt to [call the killers off](ned-orders-daenerys-s-assassination-cancelled) is a direct response to this same order.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S119 essos-root track. Standalone root of the Essos thread — no causal upstream by design [Robert acts on learning of the pregnancy; the pregnancy is not a modeled event]. [Robert Baratheon](robert-baratheon) is the orderer (AGENT_IN, Tier-1); [Daenerys](daenerys-targaryen) is the target (VICTIM_IN, Tier-1). The order CAUSES the [wine merchant's attempt](the-wine-merchant-attempts-to-poison-dany) (Tier-2). [Ned's later countermand](ned-orders-daenerys-s-assassination-cancelled) is the *object* of cancellation, not a causal consequence — fresh-verify (S119) declined a CAUSES edge there; its true cause is Robert's deathbed change of heart, which is unmodeled.)

## Quotes

> "The whore is pregnant!" The king's fist slammed down on the council table loud as a thunderclap. ... "I want them dead, mother and child both, and that fool Viserys as well. Is that plain enough for you? I want them dead."

— King Robert Baratheon, AGOT Eddard VIII (`sources/chapters/agot/agot-eddard-08.md:13`)
