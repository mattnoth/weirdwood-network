---
name: "Death of Robert I Baratheon"
type: event.assassination
slug: death-of-robert-baratheon
aliases: ["death-of-robert-baratheon", "death-of-robert-i-baratheon", "robert-baratheon-killed-by-the-boar", "robert-s-boar-hunt-death", "the-kings-boar-hunt", "killing-of-king-robert", "robert-gored-by-the-boar"]
confidence: tier-1
era: war-of-the-five-kings
containers: [wo5k]
pass_origin: s108-causal-track
node_version: 1
occurred:
  ac_year: 298
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-recall
  date_confidence: tier-2
sort_keys:
  ac_year: 298
  book_order: null
  chapter_number: null
  chapter_label: null
  composite: "0298.0.000"
  reading_order: null
  basis: "year-only"
---

## Identity

King Robert I Baratheon is mortally gored by a boar while hunting in the kingswood (~298 AC). The architecture's canonical example of `event.assassination` ("Death of Robert I via boar hunt"): the goring is a hunting accident, but a weaponized one. Cersei Lannister had her cousin and cupbearer Lancel keep the king's wineskin full of fortified strongwine, so that a drunk, slow Robert "missed his thrust." Robert lingers a day, names Eddard Stark Protector of the Realm in his last letter, then dies — removing Ned's only royal shield and opening the succession crisis that destroys him. This is the proximate event that the graph previously left causally dark; it is the hinge between Ned's discovery of Joffrey's parentage and Ned's arrest and execution.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S108 causal-arc track — Robert Baratheon VICTIM_IN (the king gored); Lancel Lannister AGENT_IN (Tier-2, kept the king's strongwine flowing on Cersei's instruction); Cersei Lannister COMMANDS_IN (Tier-2, engineered the death via the wine). This beat CAUSES the [arrest of Eddard Stark](arrest-of-eddard-stark). The separate [Varys confirms Cersei's role in Robert's death](varys-confirms-cersei-s-role-in-robert-s-death) beat records the later in-world revelation, not the death itself. Causal links Tier-2.)

## Quotes

> "A boar." Lord Renly was still in his hunting greens, his cloak spattered with blood. … "A devil," the king husked. "My own fault. Too much wine, damn me to hell. Missed my thrust."

— AGOT Eddard XIII (`sources/chapters/agot/agot-eddard-13.md:35`)

> "Oh, indeed. Cersei gave him the wineskins, and told him it was Robert's favorite vintage." … "It was not wine that killed the king. It was your mercy."

— Varys, AGOT Eddard XV (`sources/chapters/agot/agot-eddard-15.md:111`)

> "I will give Lyanna your love, Ned. Take care of my children for me."

— Robert Baratheon's last words to Eddard Stark, AGOT Eddard XIII (`sources/chapters/agot/agot-eddard-13.md:107`) — book-cite overlay (S134 harvest-consume); the dying king's final breath, naming Lyanna and asking Ned to guard his children
