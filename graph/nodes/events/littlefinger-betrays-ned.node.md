---
name: "Littlefinger Betrays Ned"
type: event.incident
slug: littlefinger-betrays-ned
aliases:
  - "Littlefinger betrays Ned"
  - "Littlefinger's betrayal of Ned"
  - "Baelish betrays Eddard Stark"
  - "the dagger under Ned's chin"
confidence: tier-1
era: current-narrative
containers: [wo5k]
occurred:
  ac_year: 298
  precision: year
  basis_source: narrative-prose
  basis_reliability: primary-source
  date_confidence: tier-2
  narrative_first: "agot-eddard-14"
pass_origin: curator-causal-arc-s121
node_version: 1
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

The moment Petyr "Littlefinger" Baelish turns on Eddard Stark in the throne room of the Red Keep
(AGOT, Eddard XIV). Having agreed to bribe Janos Slynt's gold cloaks to back Ned against Cersei,
Littlefinger instead uses Ned's own plan against him: when the trap springs and Ned's household guard
are cut down, Littlefinger draws Ned's dagger and holds it to his throat.

This is the **double-cross** at the center of Ned's fall — and it earns its weight precisely because Ned
had been warned, twice, by Littlefinger himself. Littlefinger relied on Ned's gold-cloak plan *as the
mechanism of the betrayal*: Ned thought he had bought the City Watch; Littlefinger had already sold him.

It is modeled as a discrete `event.incident` and as a **constitutive beat of** the arrest
(`SUB_BEAT_OF arrest-of-eddard-stark`) — NOT as a cause of it. Per the S120 granularity policy, a beat
that is a *constitutive action within* an event takes `SUB_BEAT_OF` only, never a causal edge into that
event (the betrayal *is* the arrest happening, not a prior cause of it). The genuinely *prior* causal
antecedent — Littlefinger's pre-arrest bribing of the gold cloaks — could be minted as its own node that
legitimately `ENABLES`/`CAUSES` the arrest, if the arc is ever deepened.

## Participants

- **Petyr Baelish** — `AGENT_IN` (the betrayer; draws the dagger).
- **Eddard Stark** — the betrayed (captured in the dyadic `petyr-baelish BETRAYS eddard-stark` edge).

## Quotes

> As his men died around him, Littlefinger slid Ned's dagger from its sheath and shoved it up under his
> chin. His smile was apologetic. "I did warn you not to trust me, you know."
>
> —AGOT, Eddard XIV (agot-eddard-14.md:125)

## Foreshadowing

The betrayal is planted early. In the Tower of the Hand (AGOT, Eddard V), when Ned thanks Littlefinger
and says "Perhaps I was wrong to distrust you," Littlefinger answers:

> Distrusting me was the wisest thing you've done since you climbed down off your horse.
>
> —AGOT, Eddard V (agot-eddard-05.md:173)

(Note: the famous "When you play the game of thrones, you win or you die" line is **Cersei's**, in the
godswood — AGOT Eddard XII, agot-eddard-12.md:169 — NOT Littlefinger's.)
