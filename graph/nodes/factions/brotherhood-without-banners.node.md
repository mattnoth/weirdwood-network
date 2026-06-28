---
name: "Brotherhood Without Banners"
type: organization.faction
slug: brotherhood-without-banners
aliases: ["the brotherhood", "Beric's men", "the outlaws"]
confidence: tier-1
wiki_source: "https://awoiaf.westeros.org/index.php/Brotherhood_Without_Banners"
bucket_id: tier2-recovery
prompt_version: v1-python
node_version: 1
pass_origin: pass2-wiki-deterministic
---

## Identity

The Brotherhood Without Banners is a rebel outlaw company operating in the riverlands during the War of the Five Kings. The group formed from the survivors of the force Lord Beric Dondarrion led south from King's Landing at Eddard Stark's command to execute Ser Gregor Clegane for raiding the riverlands. Ambushed at the Mummer's Ford by Gregor's men and a Lannister host, Beric was mortally wounded and the royalist banner was lost. When Thoros of Myr reflexively administered the last kiss, Beric unexpectedly returned to life. The surviving two-score men, no longer bearing a royal banner, coalesced around Beric into a self-declared protectorate of the smallfolk, styling themselves defenders of the realm in the name of the late King Robert I Baratheon even after his death. As Beric himself told Sandor Clegane: "Robert is slain, but his realm remains. And we defend her."

Throughout the War of the Five Kings the brotherhood operates from hidden bases in the riverlands — including the hollow hill — conducting trials of accused men (sometimes by trial by combat), sheltering smallfolk, and harrying Lannister foraging parties and other aggressors. Beric is repeatedly resurrected by Thoros following each death. The group takes in Arya Stark for a time and maintains a network of informants and sympathizers, including Lady Ravella Smallwood of Acorn Hall who provides them hospitality and intelligence. At the conclusion of ASOS, Beric sacrifices his final life to resurrect the slain Catelyn Stark via the last kiss. Catelyn, now known as Lady Stoneheart, assumes command of the brotherhood, redirecting its focus from protecting smallfolk toward systematic vengeance against House Frey and those responsible for the Red Wedding.

Under Lady Stoneheart's leadership the brotherhood's character shifts markedly. Stoneheart's followers use the inn at the crossroads as a base, capturing travelers and hanging assumed enemies — often with pieces of salt forced into their mouths as a reference to the raid on Saltpans. Questions circulate about whether the hanged were guilty of actual crimes or merely fought for the wrong side. The brotherhood is blamed (falsely, by Lord Randyll Tarly's deliberate propaganda) for the Saltpans atrocity, which was actually committed by Rorge's company wearing a hound's-helm disguise. By AFFC House Frey and crown loyalists regard the brotherhood as the primary outlaw threat in the riverlands, while Brienne of Tarth, Podrick Payne, and Ser Lyle Crakehall are eventually captured by Lem Lemoncloak's contingent and brought before Stoneheart for judgment.

## Edges

<!-- No infobox entry found for the Brotherhood Without Banners page itself in infobox-data.jsonl. -->
<!-- Edges below are derived from cross-reference evidence in source nodes. -->

<!-- Membership (characters whose infoboxes carry SWORN_TO → Brotherhood without banners) -->
- `SWORN_TO` ← Beric Dondarrion (founder and leader until ASOS epilogue)
- `SWORN_TO` ← Thoros of Myr (priest of R'hllor; repeatedly resurrects Beric)
- `SWORN_TO` ← Anguy (the Archer)
- `SWORN_TO` ← Lem Lemoncloak
- `SWORN_TO` ← Beardless Dick
- `SWORN_TO` ← Dennet / Dennett
- `SWORN_TO` ← Boy (adopted by Sharna and her husband)
- `SWORN_TO` ← Catelyn Stark / Lady Stoneheart (assumed command after ASOS epilogue)
- `SWORN_TO` ← Brienne of Tarth (captured, forced into service, AFFC)

<!-- Leadership transition -->
- `SUCCEEDS` → Catelyn Stark succeeds Beric Dondarrion as effective commander (ASOS epilogue)

<!-- Geographic / operational base -->
- `OPERATES_IN` → Riverlands (primary theater of operations)

<!-- Conflict participation -->
- `FIGHTS_IN` → War of the Five Kings
- `FIGHTS_IN` → Battle at the Mummer's Ford (founding engagement)
- `FIGHTS_IN` → Battle at the burning septry

<!-- Opposition -->
- `OPPOSES` → House Lannister
- `OPPOSES` → House Frey (especially after Red Wedding, under Stoneheart)
- `OPPOSES` → Mountain's men (Gregor Clegane's raiders)

## Quotes

> "We're looking for a dog that ran away … He answers to the name Sandor Clegane. Thoros says he was making for the Twins. We found the ferrymen who took him across the Trident, and the poor sod he robbed on the kingsroad … He would have had a child with him. A skinny girl, about ten."

— A brotherhood singer (Merrett Frey's captor) describing the post-Red-Wedding pursuit of [Sandor Clegane](sandor-clegane) and [Arya Stark](arya-stark), ASOS Epilogue (`sources/chapters/asos/asos-epilogue.md:135`)

## Notes

**Signal-fire network around Riverrun (AFFC)** — Ser Daven Lannister reports to Jaime: *"My scouts report fires in the high places at night. Signal fires, they think … as if there were a ring of watchers all around us. And there are fires in the villages as well."* — AFFC Jaime V, `sources/chapters/affc/affc-jaime-05.md:121` · Sourced evidence of the Brotherhood's surveillance network encircling the Riverrun siege camp; the ring-of-watchers phrasing establishes organized intelligence-gathering, not mere bandit presence.
