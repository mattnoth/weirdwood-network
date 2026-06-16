# combat-at-the-tower-of-joy — Structural Attachment Notes

**Produced:** 2026-06-15

## Hub state before this run

- 1 outgoing edge already present: `PART_OF → roberts-rebellion` (wiki-sourced)
- 0 incoming edges
- `LOCATED_AT` was missing; `FIGHTS_IN` for all 10 combatants was missing

## Edges emitted (11 total)

| Type | Count |
|---|---|
| LOCATED_AT | 1 |
| FIGHTS_IN | 10 |

## Provenance split

| Tier | Evidence kind | Count | Notes |
|---|---|---|---|
| tier-1, book-pass1 | chapter quote | 6 | Ned + Howland (line 93 survivor quote); Martyn Cassel (line 93 death quote); Arthur Dayne, Oswell Whent, Gerold Hightower (line 15 named individually) |
| tier-2, book-pass1 | chapter quote | 4 | Theo Wull, Ethan Glover, Mark Ryswell, Willam Dustin — named in line 13 companion list from Ned's dream (second-hand/recalled narration → tier-2) |
| tier-1, book-pass1 | chapter quote | 1 | LOCATED_AT tower-of-joy (line 15: "They waited before the round tower, the red mountains of Dorne at their backs") |

All quotes are verbatim substrings of `sources/chapters/agot/agot-eddard-10.md`.

## Slug corrections

- Task prompt used `william-dustin` — no node exists for that slug. Correct slug is `willam-dustin` (one 'l'), which resolves to character Willam Dustin. Used `willam-dustin`.

## Skipped / unresolved

- `william-dustin` — typo variant; resolved to `willam-dustin` (see above)
- No other unresolved participants. All 10 combatants (7 Stark companions + 3 Kingsguard) have confirmed nodes.

## Skipped edges

- `PART_OF → roberts-rebellion` — already exists (verified via `--neighbors combat-at-the-tower-of-joy`); not duplicated.

## Source files consulted

- `graph/nodes/events/combat-at-the-tower-of-joy.node.md` — hub node
- `sources/chapters/agot/agot-eddard-10.md` — Eddard X fever dream (primary book source for all edges)
- `scripts/graph-query.py` — slug resolution for all 10 participants + `tower-of-joy` location
