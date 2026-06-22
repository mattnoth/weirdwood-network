---
name: "Littlefinger brokers the Tyrell-Lannister alliance"
type: event.conspiracy
slug: littlefinger-brokers-tyrell-lannister-alliance
aliases: ["Petyr Baelish brokers the Tyrell marriage pact", "the Bitterbridge alliance", "the Tyrell-Lannister marriage alliance", "Littlefinger wins Highgarden for Joffrey"]
confidence: tier-1
era: war-of-the-five-kings
containers: [wo5k]
pass_origin: s123-wo5k-j9
node_version: 1
evidence_chapters:
  - ACOK Tyrion VIII
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

With [Renly dead](shadow-assassination-of-renly) and his Reach host suddenly kingless at [Bitterbridge](fighting-at-bitterbridge), the Lannister small council saw a chance to win [House Tyrell](house-tyrell) before they could harden behind Stannis. [Tyrion Lannister](tyrion-lannister) proposed taking "a lesson from the late Lord Renly" — winning the Tyrell alliance with a marriage, offering [Joffrey](joffrey-baratheon)'s hand to [Margaery Tyrell](margaery-tyrell). [Petyr Baelish](petyr-baelish), pleading that king and Hand were both needed in the city, volunteered to ride in their stead and negotiate. At Bitterbridge and Highgarden he brokered the pact between the Tyrells, [Lord Tywin](tywin-lannister), and Joffrey — bringing "fifty thousand swords and all the strength of Highgarden" to the Lannister cause. That host, marching as Tywin's relief force, would fall on [Stannis](stannis-baratheon)'s flank at the [Blackwater](battle-of-the-blackwater) and rout him.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S123 WO5K-remainder track / J9. ENABLED by [the shadow assassination of Renly](shadow-assassination-of-renly) (Tier-2) — his death frees the Tyrells to be courted. [Tyrion Lannister](tyrion-lannister) conceives the marriage offer and [Petyr Baelish](petyr-baelish) conducts the negotiation (both AGENT_IN, Tier-1). The brokered alliance ENABLES [the Battle of the Blackwater](battle-of-the-blackwater) (Tier-2) — it delivers the Tyrell relief host that wins the battle (enabling the Lannister victory; the battle's occurrence is Stannis's assault). The J2 prong (Stannis absorbing Renly's host) is the other half of the Blackwater's upstream.)

## Quotes

> "It seems to me we should take a lesson from the late Lord Renly. We can win the Tyrell alliance as he did. With a marriage."

— Tyrion Lannister to the small council, ACOK Tyrion VIII (`sources/chapters/acok/acok-tyrion-08.md:73`)

> "They loved Renly, clearly, but Renly is slain. Perhaps we can give them good and sufficient reasons to prefer Joffrey to Stannis . . . if we move quickly."

— Tyrion, on the now-kingless Tyrells, ACOK Tyrion VIII (`sources/chapters/acok/acok-tyrion-08.md:59`)

> "The Stark girl brings Joffrey nothing but her body, sweet as that may be. Margaery Tyrell brings fifty thousand swords and all the strength of Highgarden."

— Petyr Baelish quantifying the alliance, ACOK Tyrion VIII (`sources/chapters/acok/acok-tyrion-08.md:113`)

> "Your Grace, my lord Hand," said Littlefinger, "the king needs both of you here. Let me go in your stead."

— Petyr Baelish volunteering to broker the deal, ACOK Tyrion VIII (`sources/chapters/acok/acok-tyrion-08.md:139`)
