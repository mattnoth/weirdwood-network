---
name: "Mirri Maz Duur's blood-magic ritual"
type: event.incident
slug: drogo-blood-magic-ritual
aliases: ["Mirri Maz Duur's ritual", "the blood-magic ritual", "Mirri Maz Duur's blood magic", "Mirri's spell to save Drogo", "the ritual to heal Drogo", "Mirri Maz Duur heals Drogo", "only death can pay for life", "the maegi's dark magic on Drogo"]
confidence: tier-1
era: roberts-reign
pass_origin: s119-essos-root-track
node_version: 1
evidence_chapters:
  - AGOT Daenerys VIII
  - AGOT Daenerys IX
occurred:
  ac_year: 298
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

After [Khal Drogo](drogo) is wounded raiding the Lhazareen and the cut festers — he falls from his horse, a sign a khal can no longer rule — [Daenerys Targaryen](daenerys-targaryen) turns in desperation to the captive godswife [Mirri Maz Duur](mirri-maz-duur), a maegi taught blood magic by a bloodmage of the Shadow Lands. Mirri warns the price will be dear ("Some would say that death is cleaner") and performs a dark ritual inside Drogo's tent, slaughtering his stallion and working her magic against [Daenerys's](daenerys-targaryen) explicit consent to the unknown cost. The spell does not restore Drogo: it leaves him a breathing husk, blind and mindless, while the life that paid the price is the unborn [Rhaego](rhaego), drawn from the womb dead and deformed. Mirri's later admission — "Only death can pay for life" — reveals the ritual as her vengeance for the sack of her temple and her people. The ritual is the direct cause of both [Drogo's death](death-of-khal-drogo) and, through it, the [dragons' birth](dragon-hatching-on-drogo-pyre).

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S119 essos-root track. [Mirri Maz Duur](mirri-maz-duur) is the agent (AGENT_IN, Tier-1); [Drogo](drogo) is the subject of the failed healing (VICTIM_IN, Tier-1); [Rhaego](rhaego) dies as the ritual's price (VICTIM_IN, Tier-1). [Mirri](mirri-maz-duur) SACRIFICES [Rhaego](rhaego) (the life paid for Drogo's, Tier-2). Rooted at [Drogo's westward vow](drogo-westward-vow) (which sent him on the march where he was wounded; ENABLES hinge, Tier-2 — fresh-verify adjusted from CAUSES). The ritual CAUSES [Drogo's death](death-of-khal-drogo) (Tier-2).)

## Quotes

> "There is a spell." Her voice was quiet, scarcely more than a whisper. "But it is hard, lady, and dark. Some would say that death is cleaner. I learned the way in Asshai, and paid dear for the lesson. My teacher was a bloodmage from the Shadow Lands."

— Mirri Maz Duur, AGOT Daenerys VIII (`sources/chapters/agot/agot-daenerys-08.md:167`)

> "Only death can pay for life." ... "The price was paid," Dany said. "The horse, my child, Quaro and Qotho, Haggo and Cohollo. The price was paid and paid and paid."

— Mirri Maz Duur and Daenerys, AGOT Daenerys IX (`sources/chapters/agot/agot-daenerys-09.md:127`)
