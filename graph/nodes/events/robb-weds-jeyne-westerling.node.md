---
name: "Robb weds Jeyne Westerling"
type: event.wedding
slug: robb-weds-jeyne-westerling
aliases: ["robb-marries-jeyne-westerling", "robb-breaks-his-frey-marriage-pact", "robbs-marriage-to-jeyne-westerling", "robb-stark-weds-jeyne-westerling"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s107-causal-track
node_version: 1
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-scene
  date_confidence: tier-2
sort_keys:
  ac_year: 299
  book_order: null
  chapter_number: null
  chapter_label: null
  composite: "0299.0.000"
  reading_order: null
  basis: "year-only"
---

## Identity

After taking the Crag by storm and being wounded, Robb Stark is nursed by Jeyne Westerling, daughter of Lord Gawen Westerling. When the Greatjon brings him news that Winterfell has fallen and his brothers Bran and Rickon are reportedly dead, Jeyne comforts him; Robb lies with her and weds her the next day to preserve her honor. The marriage breaks the solemn pact Robb had sworn to House Frey — to wed one of Lord Walder's daughters in exchange for the crossing at the Twins. The Freys riding with Robb depart in fury. The broken oath is the spark that turns Walder Frey from grudging ally into the architect of vengeance: it triggers the conspiracy that becomes the Red Wedding.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S107 causal-arc track — Robb Stark AGENT_IN, Jeyne Westerling AGENT_IN, LOCATED_AT the Crag; this beat TRIGGERS the [Red Wedding conspiracy](red-wedding-conspiracy). Tier-2 causal link.)

## Quotes

> I took an arrow in the arm just before Ser Rolph yielded us the castle. It seemed nothing at first, but it festered. Jeyne had me taken to her own bed, and she nursed me until the fever passed. And she was with me when the Greatjon brought me the news of . . . of Winterfell. Bran and Rickon.

— Robb to Catelyn Stark, ASOS Catelyn II (`sources/chapters/asos/asos-catelyn-02.md:143`)

> "Not only have you broken your oath, but you've slighted the honor of the Twins by choosing a bride from a lesser house."

— Catelyn Stark to Robb, ASOS Catelyn II (`sources/chapters/asos/asos-catelyn-02.md:165`)

> "Fifty. A dozen knights." His voice was glum, as well it might be. When the marriage contract had been made at the Twins, old Lord Walder Frey had sent Robb off with a thousand mounted knights and near three thousand foot.

— The strategic cost of the broken Frey oath, quantified: Jeyne's dower of fifty swords against the host Walder Frey had originally pledged. Robb to Catelyn Stark, ASOS Catelyn II (`sources/chapters/asos/asos-catelyn-02.md:139`)

> "We wed without his consent, I fear, and this marriage puts him in dire peril. The Crag is not strong. For love of me, Jeyne may lose all."
>
> — sources/chapters/asos/asos-catelyn-02.md:131 · Robb to Catelyn on the cost to the Westerlings — the marriage's peril for Jeyne's family.  _(capture: harvest pass, quote)_

> "And you are to wed one of his daughters, once the fighting is done," she finished. "His lordship has graciously consented to allow you to choose whichever girl you prefer."
> — Catelyn Stark relaying the terms of the Frey crossing-pact to Robb, AGOT Catelyn IX (`sources/chapters/agot/agot-catelyn-09.md:241`). The betrothal vow Robb later breaks by wedding Jeyne — the origin of the slight that becomes the Red Wedding trigger. Book-cite. The dyadic layer (`robb-stark CONTRACTED_WITH walder-frey`, `robb-stark BREAKS_VOW house-frey`) already exists; this is the promise's navigable Tier-1 origin cite.

## Foreshadowing

> "Grey Wind doesn't like her uncle either. He bares his teeth every time Ser Rolph comes near him." [...] A chill went through her. "Send Ser Rolph away. At once."

— The direwolf as treachery-detector: Grey Wind bares his teeth at Ser Rolph Spicer, foreshadowing the Spicer/Westerling betrayal of Robb. Robb and Catelyn Stark, ASOS Catelyn II (`sources/chapters/asos/asos-catelyn-02.md:189`)

> "Any man Grey Wind mislikes is a man I do not want close to you. These wolves are more than wolves, Robb. ... I think perhaps the gods sent them to us. Your father's gods, the old gods of the north. Five wolf pups, Robb, five for five Stark children."

— Catelyn on the direwolves as old-gods omens; load-bearing direwolf-bond foreshadowing. Catelyn Stark to Robb, ASOS Catelyn II (`sources/chapters/asos/asos-catelyn-02.md:199`)
