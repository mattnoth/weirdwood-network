---
name: "Doran reveals the Fire and Blood pact"
type: event.incident
slug: doran-reveals-fire-and-blood-pact
aliases: ["Doran reveals the fire and blood pact", "Doran discloses the Targaryen marriage pact", "the fire and blood whisper", "Doran tells Arianne of the secret pact", "Doran's pact reveal"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s120-essos-e5-track
node_version: 1
evidence_chapters:
  - AFFC The Princess in the Tower
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
  narrative_first: "affc-41"
---

## Identity

After [Arianne's imprisonment](arianne-collapses-and-is-captured) in the wake of the failed Queenmaker plot, [Prince Doran Martell](doran-martell) finally discloses to her the marriage pact he sealed in secret years before: Dorne was promised to the Targaryen cause, and Arianne herself had been betrothed to Viserys Targaryen — long dead now, killed by "a pot of molten gold." His years of apparent passivity, his refusal to offer her any suitor she might accept, were all calculated to protect the secret. He reveals that [Quentyn](quentyn-martell) has already been sent on "a long and perilous voyage" to Essos to carry the pact forward — to win [Daenerys Targaryen](daenerys-targaryen) and her dragons. Doran presses an onyx dragon piece into Arianne's palm and whispers the Targaryen words, "Fire and blood," marking Dorne's true allegiance. The scene is the climax of AFFC's Dorne arc and the exposition hinge that closes the Queenmaker thread while opening the Essos thread — though the [reveal is posterior to Quentyn's already-underway quest](death-of-quentyn-martell), so the two threads are kin by Doran's pact rather than a single causal chain.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S120 essos-e5 track. CAUSED by [Arianne's capture](arianne-collapses-and-is-captured) (Tier-2 — her imprisonment is what forces Doran to reveal the long-kept secret). [Doran](doran-martell) is the disclosing agent (AGENT_IN, Tier-1); [Arianne](arianne-martell) load-bearingly perceives the reveal (WITNESS_IN, Tier-1 — she receives the onyx dragon and hears the whisper). The deep upstream cause — Doran's original pact-making/sending of Quentyn — is undated and unmodeled by design.)

## Quotes

> "Vengeance." His voice was soft, as if he were afraid that someone might be listening. "Justice." Prince Doran pressed the onyx dragon into her palm with his swollen, gouty fingers, and whispered, "Fire and blood."

— Doran's reveal, AFFC The Princess in the Tower (`sources/chapters/affc/affc-the-princess-in-the-tower-01.md:325`)

> "The pact was sealed in secret. I meant to tell you when you were old enough . . . when you came of age, I thought, but . . ."

— AFFC The Princess in the Tower (`sources/chapters/affc/affc-the-princess-in-the-tower-01.md:297`)

> "Your brother went with Cletus Yronwood, Maester Kedry, and three of Lord Yronwood's best young knights on a long and perilous voyage, with an uncertain welcome at its end. He has gone to bring us back our heart's desire."

— Doran names Quentyn's quest as the pact's active arm (`sources/chapters/affc/affc-the-princess-in-the-tower-01.md:321`)
