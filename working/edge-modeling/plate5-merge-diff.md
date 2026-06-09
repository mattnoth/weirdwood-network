# Plate 5 Merge — Before/After Diff

**Date:** 2026-06-09
**Backup:** `graph/edges/_regrounding/edges-pre-reification-2026-06-09.jsonl`
**Applied by:** Session 87 (Opus 4.7, autonomous after Matt's explicit go-ahead — 5 decisions Q1-Q4 captured ahead of execution).

## Top-level counts

| Item | Before | After | Δ |
|---|---:|---:|---:|
| `graph/edges/edges.jsonl` rows | 3,811 | 4,757 | **+946** |
| `graph/nodes/events/` files | 371 | 583 | **+212** |
| `graph/nodes/_conflicts/` files | 247 | 253 | +6 (1 aerys + 5 collision losers) |

(Mint phase wrote 217 new event nodes to `events/`; 5 existing event nodes were quarantined to `_conflicts/` by the 4 high-conf collision merges. Net +212.)

## Per-phase deltas (in merge order)

### Plate 0 normalizer — 10 edge-direction flips
- 10/10 applied (cressen↔melisandre KILLS, arya↔sandor CAPTURES, tyrion↔shae BETRAYS, +7 others)
- 1 mutual-kill flagged (donal-noye↔mag-mar-tun-doh-weg) — left as-is per Q4=a; follow-up TODO to add reverse direction

### Plate 0 Aerys merge — 3 phantom repoints + 1 quarantine
- 3/3 edges repointed `aerys-targaryen` → `aerys-ii-targaryen`
- `graph/nodes/characters/aerys-targaryen.node.md` → `graph/nodes/_conflicts/`

### Plate 2.5 schema fixes — 27 event-type retypes
- 27/27 wiki nodes retyped (event.battle → event.wedding/feast/coronation/trial/assassination/execution/conspiracy per S86 vocab expansion)

### Plate 2.5 drift retypes — 12 chapter articles
- 10/12 applied
- 2/12 already done (`a-storm-of-swords-prologue`, `a-storm-of-swords-epilogue` had already been retyped by a prior session)
- Total handled: 12/12

### Plate 2.5 collision merges — 4 high-confidence applied, 2 skipped
- 4/4 high-conf merges (battle-at-the-mummers-ford, battle-at-the-red-fork, battle-in-the-whispering-wood, battle-on-the-green-fork)
- 5 losing nodes quarantined to `graph/nodes/_conflicts/`
- 0 edges repointed (the losing nodes had no edges; they were stubs)
- Skipped per Q4=a: `conquest-of-dorne` (medium — `cleanup-decisions-resolved.md` says don't merge, reclassify book→object.text), `tourney-at-maidenpool` (low — needs wiki check)

### Plate 4 cluster — 51 SUB_BEAT_OF + 2 DUPLICATE_OF
- 51/51 SUB_BEAT_OF edges appended (mint → wiki canonical event)
- 2/3 DUPLICATE_OF applied: `the-wedding-ceremony` → `wedding-of-ramsay-bolton-and-arya-stark`; `wedding-ceremony` → `wedding-of-tyrion-lannister-and-sansa-stark` (mint nodes not written; 7 role edges repointed to wiki targets)
- 1/3 DUPLICATE_OF skipped: `mutiny-plan-reviewed` — target `a-storm-of-swords-prologue` is being retyped to `meta.chapter`, repointing role edges (AGENT_IN/VICTIM_IN) there would violate Contract 10. Mint kept as standalone hub.

### Plate 3 event-node mints — 217 nodes
- 217/219 minted to `graph/nodes/events/`
- 2/219 skipped (the 2 DUPLICATE_OF applied)
- One-time schema transform: `title:` → `name:` rewrite (S86 canonical surface field, unifies with wiki-derived event nodes)

### Plate 3 role edges — 897 appended (of 914 staged)
- **897 appended** to `edges.jsonl`
- **5 dropped** (Q1=a): targets in `siege-of-storm-s-end-recalled` (one of 2 fuzzy-match queue items)
- **12 dropped** (Q2=a): unresolvable LOCATED_AT targets (castle-sept, dragon-pit-meereen, great-pit-of-daznak, lhazareen-town, mouth-of-the-mander, small-hall-red-keep, the-ford, throne-room-red-keep, winterfell-battlements, winterfell-godswood)
- **22 LOCATED_AT remapped** (Q2=a): the-eyrie→eyrie, king-s-landing→kings-landing, the-wall→wall, the-twins→twins, the-greenblood→greenblood, the-septry→septry, castle-darry→darry, crossroads-inn→inn-at-the-crossroads
- **7 repointed** for the 2 applied DUPLICATE_OF mint targets

Role-edge breakdown by type (final, post-filter):
- AGENT_IN: 338 (essentially all kept)
- VICTIM_IN: 317
- COMMANDS_IN: 158
- LOCATED_AT: 73 (91 staged − 6 hub-queue/dup drops − 12 unresolvable = ~73 after all filters)
- WIELDED_IN: 10

### Plate 3 supersede stamps — 55 applied
- 55/55 stamped with `superseded_by: <hub-slug>`
- Includes 1 swapped-key match (`CAPTURES sandor↔arya` — flipped by Plate 0 normalizer, then matched on swapped key; tagged `plate5_supersede_via_swap: true`)
- Convention preserved: existing edge rows NOT deleted; downstream consumers filter on `superseded_by`

### S77 LOVES drops — 2/2
- `tyrion-lannister ↔ cersei-lannister LOVES` (both directions) dropped per S77 carryover (confirmed false from S77 conflict-pairs review)

### S77 ASSAULTS retypes — 21 to ATTACKS, 11 kept
- **Retyped to ATTACKS** (non-sexual physical assault): jaime→bran, shaggydog→luwin, viserys→dany, dany→eroeh, haggo→mirri, cersei→ned, grenn→jon, joffrey→mycah, biter→arya, rorge→arya, mandon→tyrion, robert→joffrey, tyrion→jaime, brienne→vargo, biter→brienne, cersei→blue-bard, hobber→sam, horas→sam, glendon→jon, victarion→ralf, duck→lorent-caswell
- **Kept as ASSAULTS** (sexual-violence canon or in-story abuse vignette): drogo→dany, robert→cersei, joffrey→sansa, theon→kyra, marillion→sansa, petyr→sansa, tywin→tysha, gregor→pia, burton-humble→kerwin, four-storms→kerwin, handsome-man→her-little-flower

### S77 OWNS → BONDED_TO direwolf/dragon — no-op
- 0 such rows found in `edges.jsonl`

## Validator results (post-merge)

### Type-contract validator
- Input: 4,757 rows
- **Kept: 4,725** (4,719 clean + 6 flagged + 0 retyped)
- **Dropped: 32** (0.7%) — all SUB_BEAT_OF edges with empty `evidence_quote`
  - Root cause: Plate 4 Opus Pass-B emissions ran in inference-only mode without quoted evidence (rationale-only). They carry `plate5_evidence_note: "SUB_BEAT_OF structural classification..."` post-merge. Validator's Contract 6 (empty evidence_quote → drop) does not exempt structural classification edges.
  - **NOT actually dropped from edges.jsonl** — the validator is read-only audit; the rows remain. They're flagged for follow-up.
- 6 pre-existing flagged warnings (UNCLE_OF/LOVER_OF/COUSIN_OF/HEIR_TO/SIBLING_OF/PARENT_OF with non-character endpoints) — predate Plate 5, unchanged

### Field-name fix applied in-place
- During post-merge validator review, found Plate 4 cluster staging used field `quoted_evidence` instead of canonical `evidence_quote`. Renamed in-place on all 51 SUB_BEAT_OF rows: 19 retained their quote text, 32 left empty (per above).

### Orphan-edges audit (read-only walk of `## Edges` display bullets — predates Plate 5)
- Pre-existing audit baseline (2026-05-12): 1,896 cat1 / 289 cat2
- Post-merge (2026-06-09): 1,679 cat1 / 289 cat2 — net 217 fewer cat1 orphans
- Note: this audit walks node-display bullets (NOT `edges.jsonl`); display bullets have not been regenerated this session — see follow-up TODO below.

### Red Wedding smoke test ✓
- `python3 scripts/graph-query.py --neighbors red-wedding` returns 8 SUB_BEAT_OF incoming edges
- 2-hop traversal (red-wedding ← SUB_BEAT_OF ← catelyn-is-killed) surfaces correctly-tagged role edges: AGENT_IN (house-frey), VICTIM_IN (catelyn-stark), COMMANDS_IN (walder-frey), LOCATED_AT (twins) — all with verbatim book quotes from Plate 3 Sonnet reify pass.
- Reification end-to-end working as designed.

## Follow-up TODOs (out of scope this session)

1. **Display-bullet regeneration** — no canonical `scripts/build-node-display-edges.py` exists; node `## Edges` bullets are pre-Plate-5 state. Canonical authority is `edges.jsonl` (graph-query.py reads from there). Display bullets are a human-readable convenience; downstream may want a regenerator.
2. **32 SUB_BEAT_OF edges without quoted evidence** — Plate 4 Pass-B/Pass-C inference-only emissions. Options: (a) re-run with explicit-quote requirement, (b) backfill quotes from the rationale (semantic shift), (c) add SUB_BEAT_OF to Contract 6 exemption list (structural-edge category). Decision deferred.
3. **109 hub-review-queue entries** still in `working/edge-modeling/plate3-full/hub-review-queue.jsonl` — 75 borderline-single-agent, 32 non-harming-multi-agent, 2 fuzzy-match. Defaults applied = none minted. Revisit if any deserve promotion.
4. **2 deferred collision merges** (`conquest-of-dorne`, `tourney-at-maidenpool`) — pending the cleanup-decisions analysis (don't-merge for the former; needs wiki check for the latter).
5. **donal-noye ↔ mag-mar-tun-doh-weg mutual-kill** — add reverse KILLS direction in a small follow-up.
6. **Post-Plate-5 backfill tracks A/B/C** — see `working/edge-modeling/post-plate5-backfill-design.md`. ~$25-75 total, ~300-850 edges touched, sequenced post-Plate-5.

## Files modified

- `graph/edges/edges.jsonl` (the gated write)
- `graph/nodes/events/` (+217 new mints)
- `graph/nodes/_conflicts/` (+6: 1 aerys + 5 collision losers)
- 27 event nodes' frontmatter `type:` retyped (Plate 2.5 schema fixes)
- 10 chapter nodes' frontmatter `type:` retyped (Plate 2.5 drift)
- `graph/edges/_regrounding/edges-pre-reification-2026-06-09.jsonl` (backup)
- `scripts/plate5-merge.py` (NEW, ~440 lines)
- `working/edge-modeling/plate5-merge-diff.md` (this file)
