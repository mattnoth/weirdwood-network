---
date: 2026-06-10
agent: script-builder
task: NEW TODO #7 — --event-participants primitive for graph-query.py
status: complete
---

# --event-participants build — overnight agent result

## What was built

**File modified:** `/Users/mnoth/source/asoiaf-chat/scripts/graph-query.py`

**New flag:** `--event-participants <HUB_SLUG>`

**New function:** `cmd_event_participants()` — added just before the CLI section,
following the same structural pattern as `cmd_neighbors()` and `cmd_health()`.

**New constant:** `PARTICIPANT_ROLE_TYPES` — frozenset of the 6 role edge types
to collect from beats: `AGENT_IN`, `COMMANDS_IN`, `VICTIM_IN`, `WIELDED_IN`,
`ATTENDS`, `LOCATED_AT`.

### Key implementation choices

1. **Two-pass over edges.jsonl.** First pass: collect `SUB_BEAT_OF` edges targeting
   the hub to get the beat-child slugs. Second pass: collect every role edge whose
   `target_slug` is in that beat-slug set. Single `load_edges()` call — the list is
   held in memory (~4,757 rows, trivial).

2. **Output grouped by role type.** `defaultdict(list)` keyed on `role_type`, sorted
   alphabetically. Each row shows: `source_slug`, `via beat`, `chapter`, `quote`
   (truncated to 120 chars via the existing `_short_quote()` helper).

3. **JSON output shape.** Top-level keys: `hub_slug`, `hub_node`, `beat_count`,
   `beats` (list), `participant_count`, `participants` (list of flat dicts). No
   nesting beyond the participant list — easy to `jq`-filter.

4. **Hub existence check via `find_node_file()`.** Uses the existing node-file
   lookup (same as `--neighbors`). If the node doesn't exist, returns error JSON or
   error text with slug-prefix suggestions from `slug_prefix_suggestions()`.

5. **Clean no-beats message.** When the hub exists but has 0 SUB_BEAT_OF incoming,
   prints a clear explanation and suggests checking `--neighbors` for any directly-
   attached role edges.

6. **`--event-participants` wired into argparse.** Added to the `new_mode` detection
   guard and dispatched in the `if new_mode:` block. Incompatibility error message
   updated to include the new flag name. Docstring at top of file updated.

7. **No new files, no writes to `graph/`.** Read-only on `edges.jsonl` and
   `graph/nodes/`. Constraint honored.

---

## Smoke test outputs

### Test 1: `--event-participants red-wedding`

```
========================================================================
EVENT PARTICIPANTS: red-wedding
  Red Wedding (event.wedding)
  Beats (8): catelyn-is-killed, crossbows-kill-more-northmen, lord-walder-calls-for-the-bedding, robin-flint-is-killed, robb-is-killed, ser-wendel-manderly-is-killed, the-bedding-ceremony-begins, the-wedding-feast-proceeds

PARTICIPANTS BY ROLE  (29 total role edges)
------------------------------------------------------------------------

  [AGENT_IN]  (10 edges)
    house-frey
      via beat : robin-flint-is-killed
      chapter  : ASOS Catelyn VII
      quote    : "Ringed by Freys whose daggers rise and fall."
    greatjon-umber
      via beat : the-bedding-ceremony-begins
      chapter  : ASOS Catelyn VII
      quote    : "The Greatjon throws Roslin over his shoulder."
    walder-frey
      via beat : lord-walder-calls-for-the-bedding
      chapter  : ASOS Catelyn VII
      quote    : "He claps his spotted hands; his sons pound cups; the musicians stop. Walder asks Robb's permission to bed the newlyweds."
    house-frey
      via beat : ser-wendel-manderly-is-killed
      chapter  : ASOS Catelyn VII
      quote    : "Crossbows kill more northmen — Donnel Locke, Owen Norrey, and half a dozen others fall."
    catelyn-stark
      via beat : the-wedding-feast-proceeds
      chapter  : ASOS Catelyn VII
      quote    : "Catelyn sits between Ser Ryman Frey (drunk, sweating) and Roose Bolton (eating little, sipping hippocras) on the dais."
    ryman-frey
      via beat : the-wedding-feast-proceeds
      chapter  : ASOS Catelyn VII
      quote    : "Catelyn sits between Ser Ryman Frey (drunk, sweating) and Roose Bolton..."
    roose-bolton
      via beat : the-wedding-feast-proceeds
      chapter  : ASOS Catelyn VII
      quote    : "Roose Bolton (eating little, sipping hippocras) on the dais."
    house-frey
      via beat : crossbows-kill-more-northmen
      chapter  : ASOS Catelyn VII
      quote    : "Crossbows kill more northmen — Donnel Locke, Owen Norrey, and half a dozen others fall."
    house-frey
      via beat : catelyn-is-killed
      chapter  : ASOS Catelyn VII
      quote    : "Someone grabs her scalp and cuts her throat."
    roose-bolton
      via beat : robb-is-killed
      chapter  : ASOS Catelyn VII
      quote    : "A man in dark armor and a pale pink cloak spotted with blood steps up and says 'Jaime Lannister sends his regards.' He t..."

  [COMMANDS_IN]  (9 edges)
    walder-frey
      via beat : robin-flint-is-killed
      chapter  : ASOS Catelyn VII
      quote    : "Walder Frey orchestrates massacre of Robb Stark and his followers — Watches the slaughter 'greedily' from his throne."
    walder-frey
      via beat : the-bedding-ceremony-begins
      chapter  : ASOS Catelyn VII
      quote    : "Lord Walder calls for the bedding — He claps his spotted hands; his sons pound cups; the musicians stop. Walder asks Rob..."
    robb-stark
      via beat : lord-walder-calls-for-the-bedding
      chapter  : ASOS Catelyn VII
      quote    : "Walder asks Robb's permission to bed the newlyweds."
    walder-frey
      via beat : ser-wendel-manderly-is-killed
      chapter  : ASOS Catelyn VII
      quote    : "Walder Frey | Orchestrates massacre of | Robb Stark and his followers | Watches the slaughter 'greedily' from his throne..."
    walder-frey
      via beat : the-wedding-feast-proceeds
      chapter  : ASOS Catelyn VII
      quote    : "Walder Frey | Orchestrates massacre of | Robb Stark and his followers | Watches the slaughter 'greedily' from his throne..."
    walder-frey
      via beat : crossbows-kill-more-northmen
      chapter  : ASOS Catelyn VII
      quote    : "Walder Frey | Orchestrates massacre of | Robb Stark and his followers | Watches the slaughter 'greedily' from his throne"
    roose-bolton
      via beat : crossbows-kill-more-northmen
      chapter  : ASOS Catelyn VII
      quote    : "Roose Bolton | Betrays | Robb Stark | Leaves before massacre; implied to be the man who kills Robb"
    walder-frey
      via beat : catelyn-is-killed
      chapter  : ASOS Catelyn VII
      quote    : "Walder Frey orchestrates massacre of Robb Stark and his followers — watches the slaughter 'greedily' from his throne; mo..."
    walder-frey
      via beat : robb-is-killed
      chapter  : ASOS Catelyn VII
      quote    : "Walder Frey | Orchestrates massacre of | Robb Stark and his followers | Watches the slaughter 'greedily' from his throne..."

  [VICTIM_IN]  (10 edges)
    robin-flint
      via beat : robin-flint-is-killed
      chapter  : ASOS Catelyn VII
      quote    : "Robin Flint is killed — Ringed by Freys whose daggers rise and fall."
    roslin-frey
      via beat : the-bedding-ceremony-begins
      chapter  : ASOS Catelyn VII
      quote    : "Roslin is stiff with terror and crying. Both are carried from the hall."
    edmure-tully
      via beat : the-bedding-ceremony-begins
      chapter  : ASOS Catelyn VII
      quote    : "Edmure is stripped by women. Both are carried from the hall."
    edmure-tully
      via beat : lord-walder-calls-for-the-bedding
      chapter  : ASOS Catelyn VII
      quote    : "Edmure is stripped by women. Both are carried from the hall."
    roslin-frey
      via beat : lord-walder-calls-for-the-bedding
      chapter  : ASOS Catelyn VII
      quote    : "The Greatjon throws Roslin over his shoulder. Roslin is stiff with terror and crying."
    ser-wendel-manderly
      via beat : ser-wendel-manderly-is-killed
      chapter  : ASOS Catelyn VII
      quote    : "Rising to his feet with his leg of lamb, a quarrel goes in his open mouth and out the back of his neck. He crashes forwa..."
    donnel-locke
      via beat : crossbows-kill-more-northmen
      chapter  : ASOS Catelyn VII
      quote    : "Donnel Locke, Owen Norrey, and half a dozen others fall."
    owen-norrey
      via beat : crossbows-kill-more-northmen
      chapter  : ASOS Catelyn VII
      quote    : "Donnel Locke, Owen Norrey, and half a dozen others fall."
    catelyn-stark
      via beat : catelyn-is-killed
      chapter  : ASOS Catelyn VII
      quote    : "Catelyn is killed — Someone grabs her scalp and cuts her throat."
    robb-stark
      via beat : robb-is-killed
      chapter  : ASOS Catelyn VII
      quote    : "He thrusts his longsword through Robb's heart and twists."

========================================================================
SUMMARY: red-wedding  |  8 beats, 29 role edges, 13 distinct participants
```

Canonical participants confirmed:
- Walder Frey: COMMANDS_IN on 7 of 8 beats
- Roose Bolton: COMMANDS_IN crossbows beat + AGENT_IN robb-is-killed beat
- House Frey: AGENT_IN on 4 beats
- Catelyn Stark: VICTIM_IN catelyn-is-killed (correct) + AGENT_IN the-wedding-feast-proceeds (known wrong-direction edge from Probe 7 — documented in S88 hub-review queue)
- Robb Stark: VICTIM_IN robb-is-killed + COMMANDS_IN lord-walder-calls-for-the-bedding (known wrong-direction edge from Probe 7)
- Robb-stark as VICTIM_IN is correct; his COMMANDS_IN on the bedding-call is the known Probe 7 wrong-direction edge
- No LOCATED_AT edges surfaced on Red Wedding beats (Twins not attached at beat level)

### Test 2: `--event-participants tourney-at-harrenhal` (isolated node)

```
========================================================================
EVENT PARTICIPANTS: tourney-at-harrenhal
  Tourney at Harrenhal (event.tournament)

  No beats found — this hub has no reified children (no SUB_BEAT_OF edges incoming).
  All role edges must be directly on the hub itself (check --neighbors) or the event has not been mined yet.

========================================================================
SUMMARY: 0 beats, 0 participants
```

Correct — isolated node, no error thrown.

### Test 3: `--event-participants nonexistent-slug`

```
ERROR: hub not found: 'nonexistent-slug'
  No node file found for this slug. Check spelling.
```

Clean error, no crash. (No prefix suggestions surface because "nonexistent" has no
meaningful token overlap with any slug in the graph.)

### Test 4: `--event-participants red-wedding --json | python3 -m json.tool`

Parses as valid JSON (exit 0). Structure:
```json
{
    "hub_slug": "red-wedding",
    "hub_node": "Red Wedding (event.wedding)",
    "beat_count": 8,
    "beats": ["catelyn-is-killed", "crossbows-kill-more-northmen", ...],
    "participant_count": 29,
    "participants": [
        {
            "role_type": "VICTIM_IN",
            "source_slug": "robin-flint",
            "beat_slug": "robin-flint-is-killed",
            "evidence_book": "asos",
            "evidence_chapter": "ASOS Catelyn VII",
            "evidence_quote": "Robin Flint is killed ...",
            "confidence_tier": 1
        },
        ...
    ]
}
```

---

## Surprises and issues encountered

1. **Walder Frey deduplication.** Walder appears as COMMANDS_IN on 7 of 8 beats
   (all except the-bedding-ceremony-begins). The output shows all 7 rows separately
   with their per-beat quotes. This is correct — each row has a distinct beat and
   (sometimes) a distinct quote. A future "deduplicated view" option could group by
   (role_type, source_slug) and show all beats in a single row. Not needed for the
   primitive to be useful.

2. **Known wrong-direction edges surface as expected.** The three Probe 7 wrong-
   direction edges (robb-stark COMMANDS_IN lord-walder-calls-for-the-bedding,
   greatjon-umber AGENT_IN the-bedding-ceremony-begins, catelyn-stark AGENT_IN
   the-wedding-feast-proceeds) all appear. This is correct behavior — the primitive
   unions what's there; curation of wrong-direction edges is tracked separately in
   the S88 hub-review queue (followup #3).

3. **No LOCATED_AT edges on Red Wedding beats.** The Twins is not attached to any
   Red Wedding beat via LOCATED_AT. The hub itself likely has it (check --neighbors
   red-wedding), but at beat level it's absent. Not a bug in this primitive — just
   confirms what Probe 7 found.

4. **`robb-stark` appears as both COMMANDS_IN (wrong-direction) and VICTIM_IN
   (correct).** Both show up in output. This is right — the union doesn't filter.

5. **No test infrastructure exists in the project** (`scripts/test_*.py` absent).
   Per the constraint ("add tests if the project has a test pattern"), no test file
   was created.

---

## Readiness

Ready for Matt to use in a manned session. The 4 smoke tests all pass. The primitive
correctly surfaces the canonical Red Wedding participant set in one command that
replaces the Probe 7 manual grep + loop.

One optional enhancement to consider in a manned session: a `--dedupe` flag that
collapses multiple beats per (role_type, source_slug) pair into a single display
row showing all beat slugs. Useful when a participant like walder-frey appears 7
times. Not needed for correctness.
