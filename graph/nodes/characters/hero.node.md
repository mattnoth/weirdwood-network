---
name: Hero
type: character.human
slug: hero
aliases: []
confidence: tier-1
wiki_source: https://awoiaf.westeros.org/index.php/Hero
bucket_id: characters-house-targaryen-d-j
prompt_version: v1
node_version: 1
pass_origin: pass2-wiki
first_available:
  book: ADWD
  chapter: 50
  source: cite_ref
  pov: Jon X
---

## Identity

Hero is an Unsullied soldier sworn to Daenerys Targaryen (track_b: Title, Allegiances).

## Origins

Born in Essos (track_b: Born). Of Essos culture (track_b: Culture).

## Allegiances

`SWORN_TO` Unsullied (track_b: Allegiances). `SWORN_TO` House Targaryen (track_b: Allegiances).

## Narrative Arc

Hero serves among the Unsullied in Meereen. He is noted in the context of Daenerys's military forces during the conflicts in Slaver's Bay.

## Edges

- HOLDS_TITLE: Unsullied (cite: track_b_row.relationships.Title)
- SWORN_TO: Unsullied (cite: track_b_row.relationships.Allegiances)
- SWORN_TO: House Targaryen (cite: track_b_row.relationships.Allegiances)
- CULTURE_OF: Essos (cite: track_b_row.relationships.Culture)
- BORN_AT: Essos (cite: track_b_row.relationships.Born)

## Notes

The pass1_mentions for "Hero" are false positives — they match the common word "hero" in contexts about the Age of Heroes and other unrelated usages.
