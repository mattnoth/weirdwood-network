---
name: Gella
type: character.human
slug: gella
aliases: []
confidence: tier-1
wiki_source: "https://awoiaf.westeros.org/index.php/Gella"
bucket_id: characters-house-borrell
prompt_version: v1
node_version: 1
pass_origin: pass2-wiki
---

## Identity

Gella is the granddaughter of Lord Godric Borrell of Sweetsister, through one of his unnamed daughters. (wiki:Gella.cite_ref-Radwd9-1)

## Allegiances

Gella is of House Borrell. `SWORN_TO` House Borrell. (track_b: Allegiance)

She is of the `CULTURE_OF` Sistermen. (track_b: Culture)

## Appearances & Description

Gella is unmarried and said to be homely in appearance. (wiki:Gella.cite_ref-Radwd9-1)

## Narrative Arc

In *A Dance with Dragons*, Gella cooks the local specialty, sister's stew, for her lord grandfather Godric Borrell. (wiki:Gella.cite_ref-Radwd9-1)

## Edges

- SWORN_TO: House Borrell (cite: track_b_row.relationships.Allegiance)
- CULTURE_OF: Sistermen (cite: track_b_row.relationships.Culture)
- ANCESTOR_OF: Godric Borrell → Gella (cite: wiki:Gella.cite_ref-Radwd9-1)

## Notes

The track_b parser encoded the infobox "Mother" field with target "Godric Borrell" as a direct PARENT_OF edge. However, the wiki HTML reads "Mother: Daughter of Godric Borrell" — Gella's mother is an unnamed daughter of Godric, making Godric her maternal grandfather. The correct edge is ANCESTOR_OF (Godric → Gella), not PARENT_OF. The unnamed mother has no wiki page and no node.
