---
name: "The Golden Company sails for Westeros"
type: event.incident
slug: golden-company-sails-for-westeros
aliases: ["the Golden Company sails west", "Aegon decides to sail west", "the Golden Company crosses to Westeros", "the war council votes to invade", "Aegon claims the Iron Throne himself"]
confidence: tier-1
era: war-of-the-five-kings
containers: [aegon]
pass_origin: s128-aegon-a2
node_version: 1
evidence_chapters:
  - ADWD The Lost Lord
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-witnessed
  date_confidence: tier-2
---

## Identity

At the war council in ADWD The Lost Lord, immediately after [Jon Connington](jon-connington) reveals the hidden prince ([Aegon is revealed to the Golden Company](aegon-revealed-to-the-golden-company)), [Aegon Targaryen](aegon-targaryen-young-griff) — goaded by [Tyrion Lannister](tyrion-lannister)'s challenge to prove himself rather than wait on [Daenerys Targaryen](daenerys-targaryen) — declares he will "sail west instead of east." He declines the option to march east to join his aunt in Meereen and sets aside the Volantene/Yunkai sellsword-contract path, choosing instead to claim the Iron Throne by himself. Over the caution of captain-general [Harry Strickland](harry-strickland), the captains of the Golden Company rise one by one, kneel, and lay their swords at his feet. This decision is the pivot of the entire invasion: the crossing to Cape Wrath in the stormlands follows directly from it.

The broken/declined Volantis–Yunkai contract is folded into this beat as a qualifier (a non-decision — "I would think on it"), not a separate node.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S128 AEGON track / A2.) This crossing CAUSES the [Landing of the Golden Company](landing-of-the-golden-company) (Tier-2 — the sail-west decision is the proximate cause of the stormlands landing). [Aegon](aegon-targaryen-young-griff) MOTIVATES it (his "sail west" choice, over Strickland's counsel). [Tyrion Lannister](tyrion-lannister) MOTIVATES it as the goad (he challenges Aegon to invade Westeros without Daenerys's aid). It is TRIGGERED upstream by [Aegon is revealed to the Golden Company](aegon-revealed-to-the-golden-company) (the reveal at the war council precipitates this vote).

## Quotes

> "Prince Aegon," said Tristan Rivers, "we are your men. Is this your wish, that we sail west instead of east?"

— The war council puts the decision to Aegon. ADWD The Lost Lord, Jon Connington POV (`sources/chapters/adwd/adwd-the-lost-lord-01.md:215`)

> "It is," Aegon replied eagerly. "If my aunt wants Meereen, she's welcome to it. I will claim the Iron Throne by myself, with your swords and your allegiance. Move fast and strike hard, and we can win some easy victories before the Lannisters even know that we have landed."

— Aegon's sail-west decision: claim the throne himself rather than wait on Daenerys. ADWD The Lost Lord (`sources/chapters/adwd/adwd-the-lost-lord-01.md:217`)
