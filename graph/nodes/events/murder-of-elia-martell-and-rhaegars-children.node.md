---
name: "Murder of Elia Martell and Rhaegar's children"
type: event.assassination
slug: murder-of-elia-martell-and-rhaegars-children
aliases: ["murder-of-elia-and-her-children", "deaths-of-rhaegars-children", "gregor-and-amory-murder-the-targaryen-children"]
confidence: tier-1
wiki_source: "https://awoiaf.westeros.org/index.php/Sack_of_King's_Landing"
era: roberts-rebellion
pass_origin: s106-causal-track
node_version: 1
occurred:
  ac_year: 283
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-recollection
  date_confidence: tier-2
victim: ["elia-martell", "rhaenys-targaryen-daughter-of-rhaegar", "aegon-targaryen-son-of-rhaegar"]
agents: ["gregor-clegane", "amory-lorch"]
orderer: tywin-lannister
sort_keys:
  ac_year: 283
  book_order: null
  chapter_number: null
  chapter_label: null
  composite: "0283.0.000"
  reading_order: null
  basis: "year-only"
---

## Identity

During the Sack, Lannister men murdered Rhaegar Targaryen's family in the Red Keep: Ser Gregor Clegane raped and killed Princess Elia Martell and smashed the infant Prince Aegon, while Ser Amory Lorch killed the young Princess Rhaenys with "half a hundred thrusts." Lord Tywin Lannister had ordered Rhaegar's children dead — laying the bodies before the throne to prove House Lannister's break with the Targaryens — but, by his own account, did **not** command the rape of Elia or the brutality toward Rhaenys; that was the executors exceeding the order. The atrocity infuriates House Martell and seeds Oberyn's vengeance, and it estranges Eddard Stark from Robert. This beat is the keystone for the **agency-collapse distinction**: orderer (Tywin, COMMANDS_IN) and executors (Gregor/Amory, AGENT_IN) are modeled separately rather than collapsed.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S106 causal-arc track — Gregor Clegane & Amory Lorch AGENT_IN; Tywin Lannister COMMANDS_IN (ordered the deaths, not the brutality); Elia, Rhaenys, and Aegon VICTIM_IN; the beat MOTIVATES Eddard Stark and is SUB_BEAT_OF the [Sack of King's Landing](sack-of-kings-landing); LOCATED_AT King's Landing.)

## Quotes

> I grant you, it was done too brutally. Elia need not have been harmed at all, that was sheer folly. By herself she was nothing.” “Then why did the Mountain kill her?” “Because I did not tell him to spare her.

— Tywin Lannister to Tyrion, ASOS Tyrion VI (`sources/chapters/asos/asos-tyrion-06.md:187`)

> Ned had named that murder; Robert called it war. When he had protested that the young prince and princess were no more than babes, his new-made king had replied, "I see no babes. Only dragonspawn."

> "Lord Tywin's soldiers had torn him from his mother's breast and dashed his head against a wall."

— Eddard Stark recounting the death of infant Prince Aegon, AGOT Eddard II (`sources/chapters/agot/agot-eddard-02.md:73`) — Ned's eyewitness-adjacent account (received); complements Gregor Clegane's later confession at the trial; navigable book-cite overlay.

— Eddard recalling the quarrel with Robert, AGOT Eddard II (`sources/chapters/agot/agot-eddard-02.md:71`)

> Princess Elia of Dorne pleading for mercy as Rhaegar's heir was ripped from her breast and murdered before her eyes.

— Daenerys Targaryen's received memory (Viserys's stories), AGOT Daenerys I (`sources/chapters/agot/agot-daenerys-01.md:37`) — Dany's inherited image of the murder, transmitted through Viserys's narrative of the Sack

> "It was Lord Tywin who presented my sister's children to King Robert all wrapped up in crimson Lannister cloaks."

— Oberyn Martell to Tyrion, ASOS Tyrion IX (`sources/chapters/asos/asos-tyrion-09.md:411`) — the visual proof of Tywin's deliberate staging: Lannister livery wrapped around murdered royal children to announce fealty; the primary cite for Tywin's agency in the presentation even if not the killing order. Also attaches to `tywin-presents-bodies-to-robert`.
