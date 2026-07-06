---
name: "Brienne brought before Lady Stoneheart"
type: event.capture
slug: brienne-brought-before-lady-stoneheart
aliases: ["Brienne captured by the Brotherhood", "the sword or the noose", "Brienne condemned by Lady Stoneheart", "Brienne's trial in the hollow hill", "sword or noose ultimatum"]
confidence: tier-1
era: war-of-the-five-kings
containers: [wo5k]
pass_origin: s115-causal-track
node_version: 1
evidence_chapters:
  - AFFC Brienne VIII
occurred:
  ac_year: 300
  precision: approximate
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
sort_keys:
  ac_year: 300
  book_order: 4
  chapter_number: 43
  chapter_label: "AFFC Brienne VIII"
  composite: "0300.4.043"
  reading_order: "4.043"
  basis: "year+chapter"
---

## Identity

Wounded at the crossroads inn, [Brienne of Tarth](brienne-tarth) is taken captive by the [Brotherhood Without Banners](brotherhood-without-banners) together with [Podrick Payne](podrick-payne) and [Hyle Hunt](hyle-hunt), and carried bound to the Brotherhood's hollow-hill cave. There she is brought before [Catelyn Stark](catelyn-stark) — now [Lady Stoneheart](catelyn-rises-as-lady-stoneheart) — who, seeing the Lannister-gilded sword Oathkeeper at Brienne's hip, names her an oathbreaker turned to the lions. Through a northman who reads her ruined whisper, Stoneheart gives Brienne a choice: take the sword and slay the Kingslayer, [Jaime Lannister](jaime-lannister), or hang as a betrayer — "the sword or the noose." When Brienne will not choose, Stoneheart croaks two words — "Hang them" — and the chapter closes with the noose tightening as Brienne screams a word. The capture is driven by the [Stoneheart-led Brotherhood's vengeance campaign](catelyn-rises-as-lady-stoneheart).

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S115 causal-arc track. This event is CAUSED by [Catelyn rises as Lady Stoneheart](catelyn-rises-as-lady-stoneheart) (Tier-2). The [Brotherhood Without Banners](brotherhood-without-banners) is AGENT_IN; [Catelyn Stark](catelyn-stark) (as Lady Stoneheart) is COMMANDS_IN — she pronounces the sword-or-noose judgment; [Brienne of Tarth](brienne-tarth), [Podrick Payne](podrick-payne), and [Hyle Hunt](hyle-hunt) are VICTIM_IN. NOT to be confused with `brienne-arrested` (the ASOS Harrenhal cell). Terminus of the AFFC Brienne→Stoneheart arc — the chapter-ending cliffhanger has no resolved downstream beat.)

## Quotes

> Lady Catelyn’s fingers dug deep into her throat, and the words came rattling out, choked and broken, a stream as cold as ice.

— Brienne is brought before Lady Stoneheart, AFFC Brienne VIII (`sources/chapters/affc/affc-brienne-08.md:327`)

> The northman said, "She says that you must choose. Take the sword and slay the Kingslayer, or be hanged for a betrayer. The sword or the noose, she says. Choose, she says. Choose."

— Stoneheart's ultimatum, read aloud, AFFC Brienne VIII (`sources/chapters/affc/affc-brienne-08.md:327`)

> There was a long silence. Then Lady Stoneheart spoke again. This time Brienne understood her words. There were only two. "Hang them," she croaked.

— Stoneheart condemns Brienne, Podrick, and Hyle, AFFC Brienne VIII (`sources/chapters/affc/affc-brienne-08.md:331`)
