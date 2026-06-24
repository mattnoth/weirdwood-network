---
name: "Ned confesses to treason"
type: event.incident
slug: ned-confesses-to-treason
aliases: ["ned-confesses-to-treason", "eddard-stark-s-false-confession", "ned-s-confession-at-baelor", "ned-confesses-his-treason", "the-confession-of-eddard-stark", "ned-proclaims-joffrey-the-true-heir"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s108-causal-track
node_version: 1
occurred:
  ac_year: 298
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-direct
  date_confidence: tier-2
---

## Identity

On the steps of the Great Sept of Baelor, the imprisoned Eddard Stark publicly confesses a treason he did not commit — proclaiming Joffrey the one true heir and denouncing Stannis — in exchange for a promised mercy: his life on the Wall and his daughter Sansa's safety. The false confession is Cersei's design, brokered through Varys in the black cells. The confession is the immediate public set-piece that gives Joffrey his stage; Joffrey then breaks the bargain and orders Ned's execution against his mother's and the court's counsel. A sub-beat within the execution event, and the proximate trigger of it.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S108 causal-arc track — Eddard Stark AGENT_IN (speaks the forced confession); Cersei Lannister COMMANDS_IN (Tier-2, designed the confession-for-the-Wall deal, brokered via Varys); LOCATED_AT the Great Sept of Baelor; SUB_BEAT_OF the [execution of Eddard Stark](execution-of-eddard-stark). This confession TRIGGERS the execution. Causal links Tier-2.)

## Quotes

> "I am Eddard Stark, Lord of Winterfell and Hand of the King," he said more loudly, his voice carrying across the plaza, "and I come before you to confess my treason in the sight of gods and men."

— AGOT Arya V (`sources/chapters/agot/agot-arya-05.md:149`)

> "I betrayed the faith of my king and the trust of my friend, Robert. I swore to defend and protect his children, yet before his blood was cold, I plotted to depose and murder his son and seize the throne for myself. Let the High Septon and Baelor the Beloved and the Seven bear witness to the truth of what I say: Joffrey Baratheon is the one true heir to the Iron Throne, and by the grace of all the gods, Lord of the Seven Kingdoms and Protector of the Realm."

— Eddard Stark's public false confession at the steps of the Great Sept of Baelor, AGOT Arya V (`sources/chapters/agot/agot-arya-05.md:153`) — book-cite overlay (S134 harvest-consume); the full text of the forced confession (Arya's POV)

> "Tell the queen that you will confess your vile treason, command your son to lay down his sword, and proclaim Joffrey as the true heir. … I believe she will allow you to take the black and live out the rest of your days on the Wall …"

— Varys, brokering Cersei's deal, AGOT Eddard XV (`sources/chapters/agot/agot-eddard-15.md:135`)

> "The next visitor who calls on you could bring you bread and cheese and the milk of the poppy for your pain … or he could bring you Sansa's head. The choice, my dear lord Hand, is entirely yours."

— Varys, the coercion behind the confession, AGOT Eddard XV (`sources/chapters/agot/agot-eddard-15.md:157`)
