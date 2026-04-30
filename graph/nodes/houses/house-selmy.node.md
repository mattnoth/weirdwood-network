---
name: House Selmy
type: organization.house
slug: house-selmy
aliases: []
confidence: tier-1
wiki_source: https://awoiaf.westeros.org/index.php/House_Selmy
bucket_id: houses-stormlands-h
prompt_version: v1-python
node_version: 1
pass_origin: pass2-wiki
first_available:
  book: ADWD
  chapter: 11
  source: cite_ref
---

## Identity

House Selmy is a noble house of marcher lords from Harvest Hall in the Stormlands. They blazon their arms with three stalks of yellow wheat on brown. (wiki:House_Selmy)

## Allegiances

House Selmy is `REGION_OF` Stormlands, `SEAT_OF` Harvest Hall, and `OVERLORD_OF` (reverse) House Baratheon. The lord holds the title Lord of Harvest Hall. (track_b: Region, Seat, Overlord, Title)

## Narrative Arc

Arstan Selmy `RULES` House Selmy as its current head. (track_b: Head) The most famous member is Ser Barristan Selmy, known as "Barristan the Bold," one of the greatest knights in the history of the Seven Kingdoms. Barristan served in the Kingsguard under multiple kings, was dismissed by Joffrey Baratheon, and traveled to Essos to serve Daenerys Targaryen. (wiki:House_Selmy)

Historically, Ser Lyonel Selmy was slain at the Battle of the Redgrass Field during the First Blackfyre Rebellion. (wiki:House_Selmy)

## Edges

- SEAT_OF (reverse): Harvest Hall (track_b: Seat)
- RULES: Arstan Selmy (track_b: Head)
- REGION_OF: Stormlands (track_b: Region)
- HOLDS_TITLE: Lord of Harvest Hall (track_b: Title)
- OVERLORD_OF (reverse): House Baratheon (track_b: Overlord)

## Notes

The track_b parser reports first_available as ADWD ch11, but cite_refs show the house is referenced as early as AGOT ch15 and ch57. The parser likely selected the wrong cite_ref. The track_b value is copied verbatim per instructions.
