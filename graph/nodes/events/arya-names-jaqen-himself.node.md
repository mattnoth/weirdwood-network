---
name: "Arya names Jaqen himself (the naming-gambit)"
type: event.incident
slug: arya-names-jaqen-himself
aliases: ["the naming gambit", "Arya names Jaqen H'ghar"]
confidence: tier-1
era: current-narrative
pass_origin: s154-d5-arya-harrenhal-enrich
node_version: 1
evidence_chapters:
  - ACOK Arya IX
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
sort_keys:
  ac_year: 299
  book_order: 2
  chapter_number: 48
  chapter_label: "ACOK Arya IX"
  composite: "0299.2.048"
  reading_order: "2.048"
  basis: "year+chapter"
---

# Arya names Jaqen himself (the naming-gambit)

The pivot of the Harrenhal arc. With one death still owed her and the Bloody Mummers' arrival threatening
everyone, [Arya](arya-stark) needs the caged northern prisoners freed — far beyond a single whispered
name. So in the godswood she spends her last death on the assassin himself: *"It's Jaqen H'ghar."* Forced
to choose between his own death and a bargain, [Jaqen](jaqen-hghar) — more distraught than he had been in
the burning barn — offers to free the northmen if she will un-say his name. She does, and he acts at once.

The gambit is the **leverage-reversal** that `CAUSES` the weasel-soup dungeon massacre
([guards-killed](guards-killed)), which in turn enables the [fall of Harrenhal](fall-of-harrenhal). It is
the cleverest move in the arc and was previously unwired (guards-killed had no causal antecedent). NB this
is **open coercion, not MANIPULATES** (Jaqen knows exactly what she is doing); the leverage is captured by
`jaqen-hghar VICTIM_IN` + the `CAUSES guards-killed` hop, plus the existing `arya COMMANDS_IN guards-killed`.

## Quotes

> Arya put her lips to his ear. "It's Jaqen H'ghar."

> Jaqen's smile came and went. "A girl might . . . name another name then, if a friend did help?"
