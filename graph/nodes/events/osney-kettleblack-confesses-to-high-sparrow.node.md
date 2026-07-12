---
name: "Osney Kettleblack confesses to the High Sparrow"
type: event.incident
slug: osney-kettleblack-confesses-to-high-sparrow
aliases: ["Osney confesses to the High Sparrow", "Osney Kettleblack betrays Cersei", "Osney names Cersei to the Faith", "the confession that backfires on Cersei", "Osney's confession"]
confidence: tier-1
era: war-of-the-five-kings
containers: [wo5k]
pass_origin: s114-causal-track
node_version: 1
evidence_chapters:
  - AFFC Cersei X
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
sort_keys:
  ac_year: 300
  book_order: 4
  chapter_number: 44
  chapter_label: "AFFC Cersei X"
  composite: "0300.4.044"
  reading_order: "4.044"
  basis: "year+chapter"
---

## Identity

To destroy Queen [Margaery Tyrell](margaery-tyrell), [Cersei Lannister](cersei-lannister) sends [Ser Osney Kettleblack](osney-kettleblack) — her own lover — to the [High Septon](high-sparrow) at the [Great Sept of Baelor](great-sept-of-baelor) to confess that he has bedded the queen and her cousins, a scripted false accusation meant to deliver Margaery into the Faith's hands. The scheme backfires catastrophically. The High Sparrow does not simply accept the confession; he holds Osney and puts him to the Faith's scourge, and under the lash Osney recants the part about Margaery and tells a far more dangerous truth — that the queen who bedded him and sent him to smother the *previous* High Septon in his sleep was Cersei herself. The confession Cersei engineered to ruin Margaery becomes the evidence the armed Faith uses to seize and imprison Cersei. It is the pivot of her self-caused downfall.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S114 causal-arc track. CAUSED by [Cersei's plot against Margaery](cersei-plots-against-margaery) (Tier-2) — Cersei scripts and orders the confession. This event TRIGGERS [Cersei's capture in the sept](cersei-is-captured-in-the-sept) (Tier-2) — Osney's tortured true confession is the immediate grounds for her arrest. [Osney Kettleblack](osney-kettleblack) is the confessor (AGENT_IN, Tier-1); the [High Septon](high-sparrow) extracts and receives it under the Faith's authority (COMMANDS_IN, Tier-1); [Cersei Lannister](cersei-lannister) is undone by it (VICTIM_IN, Tier-1).)

## Quotes

> "The accuser is a knight of your own household. Ser Osney Kettleblack has confessed his carnal knowledge of the queen to the High Septon himself, before the altar of the Father."

— Septa Moelle presenting the scripted confession Cersei intended against Margaery, AFFC Cersei X (`sources/chapters/affc/affc-cersei-10.md:27`)

> No, you must take yourself to the Great Sept of Baelor this very night and speak with the High Septon. When a man’s sins are so black, only His High Holiness himself can save him from hell’s torments. Tell him how you bedded Margaery and her cousins.

— Cersei scripting [Osney Kettleblack](osney-kettleblack)'s false confession: the scheme that will ultimately backfire on her, AFFC Cersei IX (`sources/chapters/affc/affc-cersei-09.md:311`)

> "Aye." The chains rattled softly as Osney twisted in his shackles. "That one there. She's the queen I fucked, the one sent me to kill the old High Septon. He never had no guards. I just come in when he was sleeping and pushed a pillow down across his face."

— Osney's tortured true confession naming Cersei, AFFC Cersei X (`sources/chapters/affc/affc-cersei-10.md:243`)

## Foreshadowing

> "The thing is, the best lies have some truth in 'em … to give 'em flavor, as it were. And you want me to go tell how I fucked a queen …"

— Osney Kettleblack to Cersei, unwittingly hinting at the truth (he has slept with Cersei, not Margaery) just before agreeing to the false confession script; the "truth in 'em" proves prophetic when the scourge extracts it, AFFC Cersei IX (`sources/chapters/affc/affc-cersei-09.md:333`)

