---
name: "Assassination of Tywin Lannister"
type: event.assassination
slug: assassination-of-tywin-lannister
aliases: ["death of Tywin", "death of Tywin Lannister", "Tyrion kills Tywin", "Tyrion shoots Tywin", "Tyrion kills his father", "Tywin killed on the privy", "killing of Tywin Lannister", "Tywin shot with a crossbow"]
confidence: tier-1
era: war-of-the-five-kings
containers: [wo5k]
wiki_source: "https://awoiaf.westeros.org/index.php/Assassination_of_Tywin_Lannister"
bucket_id: battles-a
prompt_version: v1-python
node_version: 2
pass_origin: pass2-wiki-deterministic
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
sort_keys:
  ac_year: 300
  book_order: null
  chapter_number: null
  chapter_label: null
  composite: "0300.0.000"
  reading_order: null
  basis: "year-only"
---

## Identity

Tyrion Lannister kills his father, Lord Tywin, with a crossbow as Tywin sits on the privy in the Tower of the Hand (300 AC). Freed from his death-cell by Jaime and stung by Jaime's confession of the [truth of Tysha](jaime-reveals-the-truth-of-tysha), Tyrion climbs the secret shaft to Tywin's bedchamber, strangles [Shae in Tywin's bed](tyrion-kills-shae-in-tywins-bed) with the Hand's gold chain, takes the crossbow from the wall, and finds his father on the privy. When Tywin dismisses Tysha one last time as a whore — "Wherever whores go" — Tyrion looses the bolt. Tywin's death removes the Lannister patriarch and architect of the regime at the height of his power, the proximate consequence of the [trial of Tyrion](trial-of-tyrion-lannister) for Joffrey's murder. (Node repaired S109: retyped from the wrong `event.battle` to `event.assassination`; junk misparsed-infobox display edges removed; natural-phrase aliases added so "death of Tywin" resolves here.)

## Edges

(Role/causal edges live in `graph/edges/edges.jsonl`, S109 causal-arc track — Tyrion Lannister AGENT_IN (looses the crossbow bolt); Tywin Lannister VICTIM_IN; LOCATED_AT the [Tower of the Hand](tower-of-the-hand); PART_OF the [War of the Five Kings](war-of-the-five-kings) (pre-existing structural). Caused by the [Tysha revelation](jaime-reveals-the-truth-of-tysha); the chain reaches back through the [freeing](jaime-frees-tyrion-from-the-black-cells) and [Gregor's killing of Oberyn](gregor-confesses-and-kills-oberyn) to the [trial of Tyrion](trial-of-tyrion-lannister). Causal links Tier-2.)

## Quotes

> “Wherever whores go.” Tyrion’s finger clenched. The crossbow whanged just as Lord Tywin started to rise. The bolt slammed into him above the groin and he sat back down with a grunt.

— Tyrion XI, ASOS (`sources/chapters/asos/asos-tyrion-11.md:257`)

> Lord Tywin Lannister did not, in the end, shit gold.

— Tyrion XI, ASOS (`sources/chapters/asos/asos-tyrion-11.md:269`)

> It all goes back and back, Tyrion thought, to our mothers and fathers and theirs before them. We are puppets dancing on the strings of those who came before us, and one day our own children will take up our strings and dance on in our steads.

— Tyrion, the night before the killing — a meditation on dynastic causation that foreshadows his patricide breaking the chain, ASOS Tyrion X (`sources/chapters/asos/asos-tyrion-10.md:159`)
