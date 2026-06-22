---
name: "Robb proclaimed King in the North"
type: event.ceremony
slug: robb-proclaimed-king-in-the-north
aliases: ["the King in the North", "Robb crowned King in the North", "northern lords proclaim Robb king", "the King in the North proclamation", "Greatjon proclaims Robb king", "Robb declared King in the North", "the North secedes"]
confidence: tier-1
era: war-of-the-five-kings
containers: [wo5k, north]
pass_origin: s113-causal-track
node_version: 1
evidence_chapters:
  - AGOT Catelyn XI
occurred:
  ac_year: 298
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

At the war council convened at [Riverrun](riverrun) in the aftermath of [Eddard Stark's execution](execution-of-eddard-stark), the [Greatjon Umber](greatjon-umber) rose and declared that neither Renly nor Stannis Baratheon had any right to rule the North, drew his greatsword, and named [Robb Stark](robb-stark) "The King in the North." Lord [Rickard Karstark](rickard-karstark) and Lady [Maege Mormont](maege-mormont) immediately followed, kneeling and laying their blades at Robb's feet; then the river lords — Blackwood, Bracken, and Mallister, houses who had never bent the knee to Winterfell — rose and took up the cry. The proclamation revived a form of northern independence and a title not heard in the realm for more than three hundred years, since Aegon the Conqueror united the Seven Kingdoms. Robb did not formally accept; the crown was imposed upon him by collective lordly acclamation, rooted in grief over Ned's murder and the rejection of Lannister rule under Joffrey. It marks the North's entry into the War of the Five Kings as a secessionist kingdom.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S113 causal-arc track. Caused by the [execution of Eddard Stark](execution-of-eddard-stark) (CAUSES, Tier-2) — the lords' stated grounds for rejecting Joffrey and declaring independence. [Robb Stark](robb-stark) is the subject of the proclamation (AGENT_IN, Tier-1). Ned's execution also drives Robb personally (execution-of-eddard-stark MOTIVATES robb-stark, Tier-2). Extends the B3 Ned's-downfall chain one hop downstream; the WO5K causal mesh beyond this stays deferred per the hard-stop policy.)

## Quotes

> "Why should they rule over me and mine, from some flowery seat in Highgarden or Dorne? What do they know of the Wall or the wolfswood or the barrows of the First Men? ... Why shouldn't we rule ourselves again? It was the dragons we married, and the dragons are all dead!" He pointed at Robb with the blade. "There sits the only king I mean to bow my knee to, m'lords," he thundered. "The King in the North!"
>
> And he knelt, and laid his sword at her son's feet.

— Greatjon Umber, AGOT Catelyn XI (`sources/chapters/agot/agot-catelyn-11.md:209`)

> Maege Mormont stood. "The King of Winter!" she declared, and laid her spiked mace beside the swords. And the river lords were rising too, Blackwood and Bracken and Mallister, houses who had never been ruled from Winterfell ... bending their knees and shouting the old words that had not been heard in the realm for more than three hundred years, since Aegon the Dragon had come to make the Seven Kingdoms one ...
>
> "THE KING IN THE NORTH!"

— AGOT Catelyn XI (`sources/chapters/agot/agot-catelyn-11.md:215`)

> "You cannot mean to hold to Joffrey, my lord," Galbart Glover said. "He put your father to death."

— Galbart Glover, AGOT Catelyn XI (`sources/chapters/agot/agot-catelyn-11.md:155`)

> "My lady, they murdered my lord father, your husband," he said grimly. He unsheathed his longsword and laid it on the table before him, the bright steel on the rough wood. "This is the only peace I have for Lannisters."

— Robb Stark refusing Catelyn's plea for a negotiated peace, AGOT Catelyn XI (`sources/chapters/agot/agot-catelyn-11.md:179`)

> He had pledged himself to marry a daughter of Walder Frey, but she saw his true bride plain before her now: the sword he had laid on the table.

— Catelyn Stark's foreboding (foreshadows the Frey betrothal Robb will break, and the Red Wedding), AGOT Catelyn XI (`sources/chapters/agot/agot-catelyn-11.md:205`)
