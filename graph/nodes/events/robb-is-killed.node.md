---
slug: robb-is-killed
type: event.death
name: "Robb is killed"
aliases: ["death-of-robb-stark", "murder-of-robb-stark", "robb-stark-is-killed", "the-young-wolf-is-slain"]
status: minted-plate3
minted_at: 2026-06-07T20:25:58.797063+00:00
enriched_at: 2026-06-19T00:00:00+00:00
pass_origin: s107-causal-track
evidence_chapters:
  - ASOS Catelyn VII
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-scene
  date_confidence: tier-2
containers: [wo5k]
sort_keys:
  ac_year: 299
  book_order: 3
  chapter_number: 52
  chapter_label: "ASOS Catelyn VII"
  composite: "0299.3.052"
  reading_order: "3.052"
  basis: "year+chapter"
---

# Robb is killed

The death of Robb Stark, the Young Wolf, at the Red Wedding in the Twins. After the slaughter of his bannermen in the feast hall, Roose Bolton — Robb's own general, turned traitor — drives a longsword through Robb's heart with the words "Jaime Lannister sends his regards." It is the terminus of the Red Wedding conspiracy and the killing the plot was designed to accomplish. This beat is a sub-beat of the [Red Wedding](red-wedding) and the downstream end of the B1 causal arc (Robb's broken Frey pact → the conspiracy → his death).

## Edges

(Role edges live in `graph/edges/edges.jsonl` — Roose Bolton AGENT_IN, Robb Stark VICTIM_IN, Walder Frey COMMANDS_IN, LOCATED_AT the Twins; SUB_BEAT_OF the [Red Wedding](red-wedding); CAUSED by the [Red Wedding conspiracy](red-wedding-conspiracy), S107 causal-arc track, Tier-2.)

## Quotes

> A man in dark armor and a pale pink cloak spotted with blood stepped up to Robb. "Jaime Lannister sends his regards." He thrust his longsword through her son's heart, and twisted.

— Catelyn Stark (narrator), ASOS Catelyn VII (`sources/chapters/asos/asos-catelyn-07.md:135`)
