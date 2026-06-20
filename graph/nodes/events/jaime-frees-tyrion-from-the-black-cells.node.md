---
name: "Jaime frees Tyrion from the black cells"
type: event.incident
slug: jaime-frees-tyrion-from-the-black-cells
aliases: ["Jaime frees Tyrion", "Jaime opens Tyrion's cell", "freeing of Tyrion Lannister", "Tyrion's escape from the dungeons", "Varys's plan to free Tyrion", "Jaime rescues Tyrion"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s109-causal-track
node_version: 1
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

Three hours past midnight, the night before Tyrion is to be beheaded, Jaime Lannister enters his brother's black cell and frees him. The escape is orchestrated by Varys, who drugged the four turnkeys with sweetsleep and waits below in a septon's robe to lead Tyrion down through Maegor's dungeons to the sewers and a galley bound for the Free Cities. This is the hinge that turns Tyrion from a condemned prisoner into a free agent — and, because of what Jaime confesses in the corridor immediately after (the [truth of Tysha](jaime-reveals-the-truth-of-tysha)), from a man fleeing for his life into one bent on revenge.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S109 causal-arc track — Jaime Lannister AGENT_IN (opens the cell, hands over the keys); Varys COMMANDS_IN (orchestrated the escape: drugged the turnkeys, arranged the galley); LOCATED_AT the [black cells](black-cells). Caused by [Gregor's killing of Oberyn](gregor-confesses-and-kills-oberyn) (the trial-by-combat condemnation that put Tyrion under sentence of death) and in turn CAUSES the [Tysha revelation](jaime-reveals-the-truth-of-tysha). Causal links Tier-2.)

## Quotes

> "You won't need last words. I'm rescuing you." Jaime's voice was strangely solemn.

— Tyrion XI, ASOS (`sources/chapters/asos/asos-tyrion-11.md:45`)

> "Asleep. The other three as well. The eunuch dosed their wine with sweetsleep, but not enough to kill them. Or so he swears. He is waiting back at the stair, dressed up in a septon's robe. You're going down into the sewers, and from there to the river."

— Jaime, ASOS Tyrion XI (`sources/chapters/asos/asos-tyrion-11.md:57`)
