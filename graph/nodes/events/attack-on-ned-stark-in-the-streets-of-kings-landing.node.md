---
slug: attack-on-ned-stark-in-the-streets-of-kings-landing
type: event.battle
name: "Attack on Ned Stark in the streets of King's Landing"
aliases: ["Jaime attacks Ned in King's Landing", "Jaime Lannister ambushes Ned's party", "Jaime sheathes his sword but orders Ned's men killed", "slaughter of Ned's Stark household guards", "Jaime's retaliation for Tyrion's capture", "street brawl outside Chataya's brothel", "the King's Landing street melee", "jaime-lannister-ambushes-ned-s-party", "jaime-sheathes-his-sword-but-orders-ned-s-men-killed"]
status: minted-plate3
minted_at: 2026-06-07T17:05:05.563282+00:00
renamed_at: 2026-06-12T00:00:00+00:00
evidence_chapters:
  - AGOT Eddard IX
---

# Attack on Ned Stark in the streets of King's Landing

AGOT Eddard IX. Returning from Chataya's brothel, Ned Stark's party is intercepted in a King's Landing street by Jaime Lannister and at least twenty Lannister men-at-arms in ringmail and golden lion helms. Jaime is openly avenging Catelyn's capture of Tyrion at the crossroads inn — he says explicitly, "I'm looking for my brother."

Jaime confronts Ned personally, pokes him in the chest with his gilded sword, then sheathes it and instead orders his captain Tregar to ensure no harm comes to Lord Stark — but, "still … we wouldn't want him to leave here entirely unchastened, so … kill his men." The sheathe-and-order is the cinematic pivot of the scene: Jaime preserves his personal honor (sheathing his blade rather than striking Ned) while commanding the murder of Ned's guards. Ned screams "No!" and claws for his sword.

Eight men die in the ensuing melee, including Ned's household guards **Jory Cassel** (dragged down and hacked to death), **Heward** (speared in the belly), **Wyl** (pulled from his dying horse), and the Lannister captain **Tregar** (struck in the helm by Ned, shearing his lion crest). Ned's horse falls on him and breaks his leg; he survives wounded. Pycelle treats him during the fever dream of the tower of joy that follows.

The attack is the immediate trigger for Robert's aborted attempt to make peace between House Stark and House Lannister, and is the structural cause of Cersei's downstream deception (`cersei-claims-ned-s-men-attacked-first`, AGOT Eddard X) in which she falsely tells Robert that Ned's men struck first.

This node consolidates two Plate-3 stubs (`jaime-lannister-ambushes-ned-s-party` + `jaime-sheathes-his-sword-but-orders-ned-s-men-killed`) into a single canonical event hub. Both prior slugs are preserved as aliases above. The wiki itself frames the scene as a single "melee" inside Eddard Stark's biography — no discrete AWOIAF event page exists. `event.battle` is the canonical type per `reference/architecture.md:108` ("single combat engagement or plot event involving armed conflict").

## Edges
Role edges in `graph/edges/edges.jsonl`: AGENT_IN (jaime-lannister, house-lannister, tregar), VICTIM_IN (eddard-stark, jory-cassel, heward, wyl), COMMANDS_IN (jaime-lannister), LOCATED_AT (king-s-landing). DECEIVES (jaime-lannister → eddard-stark, qualifier="by_omission") added in the S93 restructure batch to capture the sheathe-and-order pivot. RELATED_TO link to `cersei-claims-ned-s-men-attacked-first` (downstream Cersei deception) appended in the same batch.

## Notes
Renamed S93 (2026-06-12) from `jaime-lannister-ambushes-ned-s-party`. The sibling stub `jaime-sheathes-his-sword-but-orders-ned-s-men-killed` was merged into this node and its node file removed; its 5 role edges were either deduplicated against existing rows on this hub (3 VICTIM_IN + 1 AGENT_IN) or repointed (1 COMMANDS_IN). The "sheathes-sword-while-ordering-kill" cinematic detail is captured in this body + via the new DECEIVES edge rather than as a separate sub-beat node.
