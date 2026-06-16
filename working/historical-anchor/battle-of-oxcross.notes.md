# battle-of-oxcross — Historical Anchor Notes

**Hub:** `battle-of-oxcross` (event.battle; ACOK — recalled second-hand)
**Date:** 2026-06-15
**Spec version:** post-plate-5 followup #9, wave 1

## Edges Emitted (7 total)

| Edge type | Source slug | Target slug | Evidence kind | Tier |
|-----------|-------------|-------------|---------------|------|
| LOCATED_AT | battle-of-oxcross | oxcross | wiki-historical-anchor | 2 |
| COMMANDS_IN | robb-stark | battle-of-oxcross | book-pass1 | 2 |
| VICTIM_IN | stafford-lannister | battle-of-oxcross | book-pass1 | 2 |
| AGENT_IN | rickard-karstark | battle-of-oxcross | book-pass1 | 2 |
| AGENT_IN | grey-wind | battle-of-oxcross | book-pass1 | 2 |
| VICTIM_IN | stevron-frey | battle-of-oxcross | book-pass1 | 2 |
| VICTIM_IN | martyn-lannister | battle-of-oxcross | book-pass1 | 2 |

## Counts

- **LOCATED_AT:** 1
- **COMMANDS_IN:** 1
- **VICTIM_IN:** 3 (stafford-lannister, stevron-frey, martyn-lannister)
- **AGENT_IN:** 2 (rickard-karstark, grey-wind)
- **FIGHTS_IN:** 0
- **ATTENDS:** 0

- **Book-grounded (tier-2):** 6 edges (all recalled/second-hand narration — Tyrion's speech to Sansa in acok-sansa-03:153 is the richest single source, covering Robb, Stafford, Karstark, Grey Wind, Martyn; Stevron from acok-catelyn-05:249)
- **Wiki-only (tier-2):** 1 edge (LOCATED_AT — village name from wiki node body)

## Pre-existing edges skipped

- `PART_OF → war-of-the-five-kings` already exists (1 outgoing edge confirmed via graph-query). Not re-emitted per spec.

## Unresolved participants

None — all six named participants resolved to existing nodes:
- `robb-stark` (character.human) ✓
- `stafford-lannister` (character.human) ✓
- `rickard-karstark` (character.human) ✓
- `grey-wind` (character.direwolf) ✓
- `stevron-frey` (character.human) ✓
- `martyn-lannister` (character.human) ✓
- `oxcross` (place.location) ✓

## Participants mentioned in wiki node body but skipped (no named node or insufficient specificity)

- **Lymond Vikary** — named in wiki node body as "dead, missing or wounded"; no node found (not in known candidates list; skipped per spec rule — no node, no edge)
- **Roland Crakehall (lord)** — same situation; skipped
- **Antario Jast** — same; skipped
- **Daven Lannister** — mentioned in Aftermath (reformed remnants at Lannisport), not a battle participant; skipped

## Provenance notes

All battle-of-oxcross edges are tier-2 by nature: the battle is NOT witnessed on-page by any POV character — it is recalled second-hand by:
- Tyrion speaking to Sansa (acok-sansa-03:153) — richest passage, covers Robb, Stafford, Karstark, Grey Wind, Martyn
- Edmure speaking to Catelyn (acok-catelyn-05:249) — Stevron's death
- Catelyn/Renly's host (acok-catelyn-05:33) — "His Grace won a great victory at Oxcross. Ser Stafford Lannister is dead"
- Catelyn-07:187 — "Ser Stafford Lannister was slain at Oxcross, I am told"

No tier-1 edges warranted. Even verbatim quotes are reports/recollections, not on-page action.

## Role assignment rationale

- **Robb Stark → COMMANDS_IN** (not FIGHTS_IN): Robb directed the operation — sent men to cut horse lines, released Grey Wind, sent cavalry after the rout. His role was command; no quote describes him personally fighting.
- **Grey Wind → AGENT_IN** (not FIGHTS_IN): Grey Wind's being loosed among the horses was the signature act that decided the battle. AGENT_IN captures "performed a signature act" per spec; FIGHTS_IN would imply conventional combat.
- **Stafford Lannister → VICTIM_IN**: killed at the battle.
- **Rickard Karstark → AGENT_IN**: personally drove a lance through Stafford's chest — the defining killing act.
- **Stevron Frey → VICTIM_IN**: wounded during the battle, died shortly after.
- **Martyn Lannister → VICTIM_IN**: captured as a highborn hostage.
