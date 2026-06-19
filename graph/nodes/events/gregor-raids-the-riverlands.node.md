---
name: "Gregor Clegane raids the Riverlands"
type: event.incident
slug: gregor-raids-the-riverlands
aliases: ["the-mountain-raids-the-riverlands", "lannister-raids-on-the-trident"]
confidence: tier-1
era: war-of-the-five-kings-prelude
pass_origin: s105-causal-track
node_version: 1
evidence_chapters:
  - AGOT Eddard XI
occurred:
  ac_year: 298
  precision: year
  basis_source: book-chapter
  basis_reliability: primary-canon
  date_confidence: tier-2
---

## Identity

In answer to Catelyn Stark's seizure of his son Tyrion, Lord Tywin Lannister sends Ser Gregor Clegane to burn and pillage the riverlands — Sherrer, Wendish Town, and the Mummer's Ford — riding without banners, in the guise of common brigands, to goad House Tully into breaking the king's peace first. This is the first open blood of the conflict that becomes the War of the Five Kings. The villagers' plea brings the raids before Eddard Stark's court at King's Landing.

This node is the **hard-stop terminus** of the Bran's-fall causal chain (S105 decision): the chain extends one defensible hop past Tyrion's capture and stops here — it does NOT assert a direct `CAUSES` edge to `war-of-the-five-kings`, whose causation is multi-attributed.

## Edges

(causal edges wired by the S105 causal-edges track — CAUSED by [Catelyn seizes the moment and arrests Tyrion](catelyn-seizes-the-moment-and-arrests-tyrion) as the coarse event→event summary. The agency is modelled explicitly: the capture **MOTIVATES** Tywin Lannister, who then orders the raids — Tywin **COMMANDS_IN** this event; Gregor Clegane **AGENT_IN** carries them out; LOCATED_AT the riverlands.)

## Quotes

> The west had been a tinderbox since Catelyn had seized Tyrion Lannister. Both Riverrun and Casterly Rock had called their banners, and armies were massing in the pass below the Golden Tooth. It had only been a matter of time until the blood began to flow.

— AGOT Eddard XI (`sources/chapters/agot/agot-eddard-11.md:23`)

> If indeed he'd sent Ser Gregor to burn and pillage — and Ned did not doubt that he had — he'd taken care to see that he rode under cover of night, without banners, in the guise of a common brigand.

— AGOT Eddard XI (`sources/chapters/agot/agot-eddard-11.md:113`)
