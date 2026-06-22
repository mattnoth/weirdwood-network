---
name: "Theon Greyjoy taken as ward of House Stark"
type: event.incident
slug: theon-greyjoy-taken-as-ward
aliases: ["theon-greyjoy-taken-as-ward", "theon-greyjoy-hostage-of-the-starks", "theon-given-to-eddard-stark", "theon-taken-from-pyke", "theon-as-ward-of-winterfell"]
confidence: tier-1
era: greyjoy-rebellion
containers: [wo5k]
pass_origin: s107-causal-track
node_version: 1
occurred:
  ac_year: 289
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-recall
  date_confidence: tier-2
---

## Identity

After Balon Greyjoy's surrender at the end of the Greyjoy Rebellion (~289 AC), Robert I Baratheon spared Balon's life in return for renewed fealty and took Balon's last surviving son, ten-year-old Theon, as a ward and hostage to ensure his defeated father's good behavior. Theon was borne away from Pyke on Robert's war galley and raised among the Stark children at Winterfell for the next ten years — "a ward in name, a hostage in truth." This beat is the consequence of the rebellion that the graph previously left causally dark: it answers "how did Theon come to be a ward of the Starks?" The downstream of this hostage childhood (Theon's ACOK turn against the Starks) belongs to a separate, larger arc and is deliberately not wired here.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S107 causal-arc track — Theon Greyjoy VICTIM_IN (the hostage), Eddard Stark AGENT_IN (takes him as ward), Robert I Baratheon COMMANDS_IN (Tier-2, decreed the arrangement), LOCATED_AT Pyke; CAUSED by the [Greyjoy Rebellion](greyjoy-rebellion). The standing `theon-greyjoy WARD_OF eddard-stark` dyad records the relationship status; this node records the event. Tier-2 causal link.)

## Quotes

> "I was a boy of ten when I was taken to Winterfell as a ward of Eddard Stark." A ward in name, a hostage in truth.

— Theon Greyjoy, ACOK Theon I (`sources/chapters/acok/acok-theon-01.md:43`)

> ...ten years before, when Robert Baratheon's war galley had borne him away to be a ward of Eddard Stark.

— ACOK Theon I (`sources/chapters/acok/acok-theon-01.md:11`)

> The whole castle, from Lady Stark to the lowliest kitchen scullion, knew he was hostage to his father's good behavior, and treated him accordingly.

— Theon Greyjoy, ACOK Theon I (`sources/chapters/acok/acok-theon-01.md:207`)
