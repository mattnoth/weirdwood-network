---
name: "Trial of Tyrion Lannister"
type: event.trial
slug: trial-of-tyrion-lannister
aliases: ["tyrions-trial-for-joffreys-murder", "tyrion-demands-trial-by-combat"]
confidence: tier-1
era: war-of-the-five-kings
pass_origin: s106-causal-track
node_version: 1
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-scene
  date_confidence: tier-2
accused: tyrion-lannister
judges: ["tywin-lannister", "mace-tyrell", "oberyn-martell"]
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

Tyrion Lannister is tried in King's Landing for the murder of King Joffrey, before a tribunal of three judges — his father Tywin Lannister, Mace Tyrell, and Oberyn Martell. A parade of witnesses gives damning (and partly false) testimony; convinced he cannot win an honest verdict, Tyrion ultimately demands trial by combat. This is the framing's legal machinery against the innocent-of-this-crime Tyrion; it is a subsequent event to the wedding, not a beat inside it.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S106 causal-arc track — Tyrion VICTIM_IN (defendant), Tywin AGENT_IN (presiding judge); the trial is CAUSED by the [accusation](tyrion-accused-of-poisoning-joffrey); LOCATED_AT the Red Keep. NOT SUB_BEAT_OF the wedding — it follows it.)

## Quotes

> "Nothing but this: I did not do it. Yet now I wish I had." He turned to face the hall, that sea of pale faces. "I wish I had enough poison for you all. ... I am innocent, but I will get no justice here. You leave me no choice but to appeal to the gods. I demand trial by battle."

— Tyrion, ASOS Tyrion X (`sources/chapters/asos/asos-tyrion-10.md:65`)

> I saved you all, Tyrion thought. I saved this vile city and all your worthless lives. There were hundreds in the throne room, every one of them laughing but his father.

— Tyrion, watching the court laugh at "my giant of Lannister," ASOS Tyrion X (`sources/chapters/asos/asos-tyrion-10.md:43`)

> He never heard his father speak the words that condemned him. Perhaps no words were necessary. I put my life in the Red Viper's hands, and he dropped it.

— Tyrion, as the sentence lands after Oberyn's death, ASOS Tyrion X (`sources/chapters/asos/asos-tyrion-10.md:249`)
