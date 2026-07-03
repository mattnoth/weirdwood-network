---
name: "Drogo's westward vow"
type: event.ceremony
slug: drogo-westward-vow
aliases: ["Drogo's vow", "Drogo's westward vow", "Drogo vows to cross the sea", "Drogo swears to take the Seven Kingdoms", "the vow before the Mother of Mountains", "Drogo pledges to cross the poison water", "Drogo's oath to invade Westeros", "the stallion who mounts the world vow"]
confidence: tier-1
era: roberts-reign
containers: [essos]
pass_origin: s119-essos-root-track
node_version: 1
evidence_chapters:
  - AGOT Daenerys VI
occurred:
  ac_year: 298
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
sort_keys:
  ac_year: 298
  book_order: 1
  chapter_number: 55
  chapter_label: "AGOT Daenerys VI"
  composite: "0298.1.055"
  reading_order: "1.055"
  basis: "year+chapter"
---

## Identity

Before the assembled khalasar at [Vaes Dothrak](vaes-dothrak), beneath the Mother of Mountains, [Khal Drogo](drogo) swears a great oath in answer to the Usurper's attempt on his wife and unborn son: he will lead his people west across the poison water as no khal has done before, take the Iron Throne for his son [Rhaego](rhaego), and lay the Seven Kingdoms low. The vow comes directly on the heels of the [wine merchant's poisoning attempt](the-wine-merchant-attempts-to-poison-dany) — [Daenerys Targaryen](daenerys-targaryen) reflects, "The Usurper has woken the dragon now" — and it is what commits Drogo's khalasar to the campaign of slave-raiding (against the Lhazareen "Lamb Men") meant to fund ships for the crossing. That campaign is where Drogo takes the wound that festers, leading to [Mirri Maz Duur's ritual](drogo-blood-magic-ritual). The vow is the hinge between the Westeros assassination thread and the Essos dragon-birth arc.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S119 essos-root track. [Drogo](drogo) is the vow-maker (AGENT_IN, Tier-1). The [wine merchant's attempt](the-wine-merchant-attempts-to-poison-dany) CAUSES this vow and MOTIVATES Drogo (Tier-2). The vow in turn ENABLES the [blood-magic ritual](drogo-blood-magic-ritual) — it commits the khalasar to the westward march whose Lhazareen raid is where Drogo takes the festering wound; fresh-verify (S119) adjusted this hinge from CAUSES to ENABLES because the wound came from a contingent battle, so the vow sets conditions rather than mechanically causing the ritual (Tier-2).)

## Quotes

> "I will take my khalasar west to where the world ends, and ride the wooden horses across the black salt water as no khal has done before. I will kill the men in the iron suits and tear down their stone houses. ... This I vow, I, Drogo son of Bharbo. This I swear before the Mother of Mountains, as the stars look down in witness."

— Khal Drogo, AGOT Daenerys VI (`sources/chapters/agot/agot-daenerys-06.md:179`)

> "The Usurper has woken the dragon now," she told herself … and her eyes went to the dragon's eggs resting in their nest of dark velvet.

— Daenerys, just before the vow, AGOT Daenerys VI (`sources/chapters/agot/agot-daenerys-06.md:153`)
