---
name: "Abduction of Lyanna Stark"
type: event.incident
slug: abduction-of-lyanna
aliases: ["abduction of Lyanna Stark", "Rhaegar takes Lyanna", "Rhaegar carries off Lyanna"]
confidence: tier-1
wiki_source: "https://awoiaf.westeros.org/index.php/Robert's_Rebellion"
era: roberts-rebellion
pass_origin: s104-causal-track
node_version: 1
occurred:
  ac_year: 282
  precision: year
  basis_source: wiki-page
  basis_reliability: secondary-canon
  date_confidence: tier-2
sort_keys:
  ac_year: 282
  book_order: null
  chapter_number: null
  chapter_label: null
  composite: "0282.0.000"
  reading_order: null
  basis: "year-only"
---

## Identity

The abduction of Lyanna Stark by Prince Rhaegar Targaryen near Harrenhal at the start of 282 AC — the inciting act of Robert's Rebellion. Following Rhaegar's crowning of Lyanna as queen of love and beauty at the [Tourney at Harrenhal](wiki:Tourney_at_Harrenhal) ("the moment when all smiles died"), Rhaegar took Lyanna, betrothed of Robert Baratheon. Her brother Brandon Stark rode to King's Landing to demand her return, setting the chain of events that became the rebellion in motion.

## Edges

(causal edges wired by the S104 causal-edges track — CAUSES the execution of Brandon and Rickard Stark, via Brandon's ride to King's Landing)

## Origins

> At the coming of the new year, Lyanna Stark was abducted by Prince Rhaegar Targaryen near Harrenhal. Her brother, Brandon Stark, was on his way to Riverrun to wed Catelyn Tully, when the news reached him. Brandon rode at once to King's Landing with his companions.

— [Robert's Rebellion](wiki:Robert's_Rebellion), AWOIAF

## Quotes

> Instead of crowning his wife, the Dornish princess Elia Martell, Rhaegar rode past her and crowned Lyanna Stark of Winterfell instead. Eddard Stark would later recall this moment as "the moment when all smiles died".

— [Robert's Rebellion](wiki:Robert's_Rebellion), AWOIAF (the crowning at Harrenhal that preceded the abduction)

## Evidence — contested agency (abduction vs. elopement)

> The graph holds this event under its in-world name ("abduction") and models the dominant realm-narrative
> via [`rhaegar-targaryen SUSPECTED_OF abduction-of-lyanna`](../../edges/edges.jsonl) (Tier-2 — the
> in-world suspicion, NOT an assertion of force). The R+L=J reading (that Lyanna went willingly) is a GATED
> theory; the opposing on-page testimony is recorded here as substrate, not asserted.

**The dominant in-world framing — abduction and rape (Robert's war-narrative):**

> "Robert was betrothed to marry her, but Prince Rhaegar carried her off and raped her," Bran explained.

— Bran Stark, AGOT Bran VII (`sources/chapters/agot/agot-bran-07.md:79`)

> "And Rhaegar … how many times do you think he raped your sister? How many hundreds of times?"

— Robert Baratheon to Eddard Stark, AGOT Eddard II (`sources/chapters/agot/agot-eddard-02.md:79`) — Robert's rawest statement of the abduction-as-rape framing, the engine of his hatred

**The opposing testimony — a love the realm called a crime:**

> Her brother Rhaegar had died for the woman he loved.

— Daenerys Targaryen, AGOT Daenerys VIII (`sources/chapters/agot/agot-daenerys-08.md:187`) — a biased source (his sister), but the on-page counter-frame to the abduction narrative; pairs with the existing `rhaegar-targaryen LOVES lyanna-stark` and `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` edges.
