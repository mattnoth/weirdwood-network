---
name: Lady
type: character.direwolf
slug: lady
aliases:
  - "the sister they had lost"
confidence: tier-2
wiki_source: https://awoiaf.westeros.org/index.php/Lady
bucket_id: direwolves
prompt_version: v1
node_version: 1
pass_origin: pass2-wiki
first_available:
  book: AGOT
  chapter: 1
  source: cite_ref
  pov: Prologue
---

## Identity

Lady is a direwolf bonded to Sansa Stark (track_b: Owner). She is the litter-mate of Grey Wind, Nymeria, Summer, Shaggydog, and Ghost. Born in 298 AC in the north. Died in 298 AC at Darry. Buried in the lichyard at Winterfell (track_b: Born, Died, Buried). Known posthumously as "the sister they had lost" in Summer's wolf-dream perspective (track_b: aliases).

## Origins

Lady was discovered with her litter-mates in the snow near their dead mother by the Stark children north of Winterfell (wiki:Lady).

## Allegiances

`OWNS`: Sansa Stark owns Lady (track_b: Owner).

## Appearances & Description

Lady is described as the gentlest and most well-behaved of the direwolf litter. No distinctive physical features are noted beyond the species norm. She has golden eyes, as seen in Sansa's dreams (wiki:Lady).

## Narrative Arc

**AGOT:** Lady's life is brief. After Nymeria bites Prince Joffrey to defend Arya, Nymeria is chased away and cannot be found. Queen Cersei demands a direwolf die in Nymeria's place. King Robert reluctantly agrees, and Lord Eddard Stark executes Lady himself rather than let Ser Ilyn Payne do it. Eddard sends Lady's bones north to be buried in the lichyard at Winterfell (wiki:Lady, agot chapters 15–16).

**Post-death:** Lady's death reverberates through Sansa's chapters across all five books. Sansa dreams of running with Lady, only to wake and remember she is dead. Sansa thinks "If Lady was here, I would not be afraid." Through Summer's wolf dreams, the pack senses the missing sister. According to George R. R. Martin, the loss of her wolf has left Sansa "a little adrift" (wiki:Lady, acok-4/18/32/36/52/62/64, asos-6/9/59/68, adwd-4/69).

## Quotes

> "She could smell out falsehood, she could, but she was dead, Father had killed her, on account of Arya." — thoughts of Sansa Stark (wiki:Lady)

> "If Lady was here, I would not be afraid." — thoughts of Sansa Stark (wiki:Lady)

> "His tail drooped when he remembered her." — Summer's perspective on the lost sister (wiki:Lady)

## Edges

- OWNS: Sansa Stark (track_b: Owner)
- DIED_AT: Darry (track_b: Died) [298 AC]
- BURIED_AT: Winterfell (track_b: Buried) [298 AC]

## Notes

- The track_b parser classified Lady as `character.human`; corrected to `character.direwolf` per architecture.md convention #8.
- The "Lady" page on the wiki has a disambiguation notice. The pass1_mentions for "Lady" include many false positives (the word "lady" appears constantly in ASOIAF text). Pass 1 cross-references should be treated as unreliable for this entity.
- Lady's death and its thematic resonance with Sansa's arc is deferred to Pass 4+.
