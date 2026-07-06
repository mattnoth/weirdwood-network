---
name: "Cersei rearms the Faith Militant and forgives the crown debt"
type: event.incident
slug: cersei-rearms-the-faith-and-forgives-the-debt
aliases: ["Cersei rearms the Faith", "arming the Faith Militant", "restoring the Warrior's Sons", "the crown's debt to the Faith forgiven", "Cersei lets the Faith bear arms again"]
confidence: tier-1
era: war-of-the-five-kings
containers: [wo5k]
pass_origin: s114-causal-track
node_version: 1
evidence_chapters:
  - AFFC Cersei IV
  - AFFC Cersei VI
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
sort_keys:
  ac_year: 300
  book_order: 4
  chapter_number: 18
  chapter_label: "AFFC Cersei IV"
  composite: "0300.4.018"
  reading_order: "4.018"
  basis: "year+chapter"
---

## Identity

Pressed by the crown's crushing debts, [Cersei Lannister](cersei-lannister) first defers repayment of the sums owed to the Holy Faith and the Iron Bank (AFFC Cersei IV), then strikes a fateful bargain with the new [High Septon](high-sparrow) — the so-called High Sparrow — at the [Great Sept of Baelor](great-sept-of-baelor): in exchange for forgiving the entire crown debt to the Faith and for the Faith's blessing of King [Tommen](tommen-baratheon), she grants the High Septon's dearest wish and permits him to restore the two ancient militant orders the Faith had been forbidden to keep since the days of the Targaryen conquest — the [Warrior's Sons](warriors-sons) (the Swords) and the Poor Fellows (the Stars). Cersei imagines she is buying cheap loyalty and ridding herself of a debt; in truth she has handed an armed, independent, fanatic institution to a man she does not control. The rearmed Faith Militant is the instrument that will, within the same book, seize, strip, and imprison her — the central irony of her downfall.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S114 causal-arc track. This act is CAUSED BY the [assassination of Tywin Lannister](assassination-of-tywin-lannister) (Tier-2, S115) — with the father who controlled crown policy dead, the unchecked Queen Regent is free to strike this bargain ("Even her lord father could have done no better") — and in turn CAUSES [Cersei's capture in the sept](cersei-is-captured-in-the-sept) (Tier-2): the rearmed Faith is the institution with the armed authority to seize a queen. [Cersei Lannister](cersei-lannister) and the [High Septon](high-sparrow) are both parties to the deal (AGENT_IN, Tier-1). The Tywin root joins this arc cross-book into the S109 Tywin's-death chain — `--causal-chain cersei-is-stripped-and-imprisoned` walks back to Sansa's poisoned hairnet. The walk of atonement and trial are deferred ADWD beats.)

## Description

Two atmosphere details from Cersei's AFFC Cersei VI visit to the Great Sept that frame the political context of the rearming deal:

**The sparrow encampment on Baelor's plaza (q519):**

> "Their cookfires filled the air with smoke and stinks. Roughspun tents and miserable hovels made of mud and scrap wood besmirched the pristine white marble."

— AFFC Cersei VI (`sources/chapters/affc/affc-cersei-06.md:109`) — the mass of sparrows camped on Baelor's plaza that Cersei walks through to reach the High Sparrow; the physical pressure that makes her bargain feel politically necessary.

**Baelor's statue under the war-dead (q520):**

> "The great marble statue that had smiled serenely over the plaza for a hundred years was waist-deep in a heap of bones and skulls. Some of the skulls had scraps of flesh still clinging to them. A crow sat atop one such, enjoying a dry, leathery feast. Flies were everywhere."

— AFFC Cersei VI (`sources/chapters/affc/affc-cersei-06.md:131`) — the sparrows have piled war-dead around Baelor the Beloved's statue; the visual context for the Faith's leverage.

**The crown's debt figure (q525):**

> "Nine hundred thousand six hundred and seventy-four dragons. Gold that could feed the hungry and rebuild a thousand septs."

— High Septon (High Sparrow) to Cersei, AFFC Cersei VI (`sources/chapters/affc/affc-cersei-06.md:269`) — exact sum forgiven in the rearming bargain; navigable book cite.

**The High Septon's crown sold (q526):**

> "That crown has been sold. So have the others in our vaults, and all our rings, and our robes of cloth-of-gold and cloth-of-silver. Wool will keep a man as warm."

— High Sparrow to Cersei, AFFC Cersei VI (`sources/chapters/affc/affc-cersei-06.md:186`) — the crystal-and-spun-gold crown Tywin gave the old High Septon has been sold; the High Sparrow's deliberate ostentatious-poverty signal.

## Quotes

> "Accordingly, I have decided to defer our repayment of the sums owed the Holy Faith and the Iron Bank of Braavos until war's end." The new High Septon would doubtless wring his holy hands, and the Braavosi would squeak and squawk at her, but what of it?

— Cersei to the small council, AFFC Cersei IV (`sources/chapters/affc/affc-cersei-04.md:187`)

> "The Faith Militant reborn . . . that would be the answer to three hundred years of prayer, Your Grace. The Warrior would lift his shining sword again and cleanse this sinful realm of all its evil. If His Grace were to allow me to restore the ancient blessed orders of the Sword and Star, every godly man in the Seven Kingdoms would know him to be our true and rightful lord."

— the High Septon rising to Cersei's bait, AFFC Cersei VI (`sources/chapters/affc/affc-cersei-06.md:265`)

> "As you wish. This debt shall be forgiven, and King Tommen will have his blessing. The Warrior's Sons shall escort me to him, shining in the glory of their Faith, whilst my sparrows go forth to defend the meek and humble of the land, reborn as Poor Fellows as of old."

— Cersei sealing the bargain that arms the Faith, AFFC Cersei VI (`sources/chapters/affc/affc-cersei-06.md:273`)
