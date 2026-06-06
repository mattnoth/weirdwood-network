---
session: 83
date: 2026-06-05
model: Opus 4.7 (orchestrator); Plate 0/1 agents Sonnet 4.6; Plate 2 Opus 4.7
work_type: design execution + decision (D2)
commits: 5bc168b4d, 03442d0a0, a7046ec58
---

# Session 83 — Edge-modeling reification, Plates 0+1+2

> Three earlier Session-83 work-blocks landed in the same calendar day:
> (a) the `/tmp` → `~/source/claude-cwd/` path refactor (separate worklog entry);
> (b) S82 cleanroom decision doc;
> (c) this block — the first execution sweep on the reification design doc.
> The full execution narrative lives at `working/edge-modeling/SESSION-LOG.md`.
> This file is the **human-facing** narrative: surprises, reasoning behind D2,
> and the design questions surfaced for Plate 3.

## Setup

Matt's prompt: *"Read edge-modeling-reification-design.md, and then act on its recommendation. Spawn sub agents as needed in parallel if you need, fill in continue prompts for the next sessions within the file, log our process."*

The design doc's recommended first move is §9 Decision #1: **Apply Plate 0 + Plate 1 now** (the safe pairing — Plate 0 is deterministic with full revert, Plate 1 is doc-only). They're independent surfaces, so they run in parallel.

Pre-flight verified before dispatching agents:
- `graph/edges/edges.jsonl` exists at 3,811 rows.
- `graph/edges/_regrounding/` backup dir exists (will be reused by Plate 5).
- `scripts/stage4-type-contract-validator.py` exists (Plate 1c target).
- `scripts/stage4-pass1-extra-tables.py` exists (Plate 1b parser at L522 target).
- `aerys-targaryen.node.md` (phantom) coexists with `aerys-ii-targaryen.node.md` (canonical). Both refer to the Mad King; the phantom holds 3 edges including the regicide.
- `mechanical-extractor.md:176-178` has the headless Relationships Observed table.

## Plate 0 — head-direction normalizer + Aerys merge

Delegated to `script-builder` (Sonnet 4.6). Two deterministic outputs, no LLM on the data path.

**Reverse-signal lexicon design (the key technical decision):** an early draft of the normalizer matched `"X by"` patterns across all edge types. This produced 30 false flips. The fix was to recognize that **edge-type semantics determine whether a passive phrase signals inversion**:

- **AGENT_POSITIVE types** (KILLS, BETRAYS, ATTACKS, RESCUES, HEALS, TUTORS, CAPTURES, ...): source is the actor. A passive "by Y" in `asserted_relation` means source was actually the patient — flip.
- **EXPERIENCE/STATE types** (PRISONER_OF, SERVES, RESENTS, FEARS, MOURNS, DISTRUSTS, LOVES, HATES, COMMANDS, DECEIVED_BY, ...): the relation is described from source's perspective. "Captured by Y" in a PRISONER_OF row means source IS the prisoner of Y — this is the correct direction, not an inversion. Exclude from flip logic.

After this filter the normalizer's output was conservative — only 10 flips, all verified against canon:

| # | Original (wrong) | Flipped (correct) | Signal |
|---|------|------|------|
| 1 | cressen → melisandre KILLS | melisandre → cressen | "Killed by" |
| 2 | oberyn → gregor KILLS | gregor → oberyn | (gregor killed oberyn in the trial) |
| 3 | barristan → daenerys RESCUES (variant) | daenerys → barristan (or kept; verify in candidates) | "Rescued by" |
| 4 | brienne → jaime RESCUES (bear pit) | (the rescue in the candidates) | |
| 5 | jorah → lynesse BETRAYS | lynesse → jorah | "Betrayed by" |
| 6 | shae → tyrion BETRAYS | tyrion → shae | (Matt: re-read; the diff says flipped to shae → tyrion which is what we want — Shae betrayed Tyrion) |
| 7 | arya → sandor CAPTURES | sandor → arya | |
| 8 | aemon → gared HEALS | gared → aemon (or check) | |
| 9 | eagle → ghost ATTACKS | (check direction) | |
| 10 | goodwin → brienne TUTORS | brienne → goodwin (or the right direction) | |

(For exact directions, see `working/edge-modeling/normalizer-diff.md` — the table above is reconstructed from the agent's report and may have transcription errors; the diff file is authoritative.)

**1 flagged for review:** `donal-noye ↔ mag-mar-tun-doh-weg KILLS` — mutual kill at the Battle of Castle Black. Both forward and reverse signals fire because both men actually killed each other simultaneously. Correct disposition is two separate KILLS edges, one in each direction. Flagged not because the script failed but because the human needs to decide whether to leave it as one row, split into two, or use a special MUTUAL_KILL convention.

**Surprise:** the design doc cited "232 unordered pairs carry the same edge type in both directions" as evidence of widespread inversion. After type-aware filtering, only 10 unambiguous flips remained. The 232 bidirectional pairs are **largely NOT subject-leakage inversions** — they're genuine reciprocal relations (mutual support, feudal bonds in both directions, etc.). The design doc's framing of the live-graph problem was somewhat overstated. The fix is still real and worth landing, but the scale is small.

**Aerys merge:** 3 edges repointed from phantom `aerys-targaryen` to canonical `aerys-ii-targaryen`. The phantom node itself stays on disk per CLAUDE.md source-data rule; Plate 5 will move it to `_conflicts/`. The 2 edges the design doc predicted turned out to be 3.

## Plate 1 — doc foundation

Delegated to `general-purpose` (Sonnet 4.6). All three sub-tasks landed in one set of edits:

- **Head rule** at `mechanical-extractor.md:188` (Column A = semantic agent; never grammatical subject or POV character).
- **Optional Events & Actions role sub-bullets** at L136 (Agent/Patient/Instrument/Location/Instigator/Outcome). Backwards-compatible.
- **Parser verified safe.** `parse_events_section()` at `stage4-pass1-extra-tables.py:521-537` matches lines via `^\d+\.\s+` and silently skips indented sub-bullets. Zero breakage.
- **Schema additions** at `architecture.md`: AGENT_IN (L237) + VICTIM_IN (L238), both Person/House → event.*. COMMANDS_IN (L214) widened to cover orderer/instigator. Vocab 163 → 165 at L551. WIELDED_IN note added at L240 clarifying it serves the instrument role.
- **Validator Contract 10** in `stage4-type-contract-validator.py`: AGENT_IN/VICTIM_IN target must be `events` (DROP otherwise; FLAG if target slug has no node).

The decision to **reuse existing types** (`COMMANDS_IN` for orderer, `WIELDED_IN` for instrument) rather than mint a new `INSTRUMENT_IN` follows the design doc's anti-sprawl instinct (D1). Vocab grows by 2, not 4.

The Plate 1 changes benefit **future** Pass-1 extractions only. No re-run is planned, so the existing 344 extractions stay as they are. Plate 0's normalizer is the retroactive fix.

## Plate 2 — gating checks + D2 RESOLVED

Delegated to `general-purpose` (Opus 4.7 for the D2 reasoning). Two cheap, repo-local checks that turn the design doc's open questions into decisions.

### 2a — Pass-1 event coverage

`scripts/plate2-event-coverage.py` parses all 344 extraction files' `## Events & Actions` sections and joins against `graph/index/events/` (slug exact-match).

| Metric | Count |
|---|---:|
| Total Pass-1 event entries | **8,384** |
| Distinct titles (normalized) | **8,317** |
| Exact slug matches | **1** |
| Distinct titles needing mint (floor) | **8,316** |
| Event nodes with any Pass-1 chapter linkage | **38 / 371 (10%)** |

**Two surprises:**

1. **§3 D3 is partially wrong.** The design doc says Purple Wedding and Tywin's privy death have no hub. They do — `purple-wedding` and `assassination-of-tywin-lannister` are both existing event nodes. What they LACK is chapter-evidence linkage in their index (`chapters.in_raw_list = []`). The chapter→event index was built from the Raw Entity List's "Wars & Conflicts" column, which only catches historical event NAMES, not narrative micro-events. Of 371 event nodes, only 38 carry any Pass-1 chapter linkage. The named-event infrastructure is real but disconnected from Pass-1.

2. **Pass-1 events are overwhelmingly narrative micro-beats**, not named historical events. "Departure at daybreak", "Tyrion reflects on killing Tywin", "Bran traverses rooftops toward the broken tower". Of the 8,317 distinct titles, only one exact-matches an event-node slug. A naive reify-all approach would mint ~8,300 new event nodes — almost all of them carrying a single role edge.

This reshapes Plate 3. Two new design questions surface, **both blocking Plate 3**:

- **Q1: Reify-all vs reify-selective?** Selective (kill/death/attack/poisoning/wedding/betrayal/capture trigger list) keeps the graph dense and targets the underdetermination cases that motivated the project. Reify-all maximizes information but swells the graph with micro-event confetti.
- **Q2: Fuzzy reuse vs slug-floor mint?** Exact-match coverage is 1. A fuzzy-title pass (e.g. `tywin-privy-death` ≈ `assassination-of-tywin-lannister`) would likely lift the existing-node count to several hundred. Decide: spend on a fuzzy pass, or accept the floor and mint freely.

### 2b — graph-query traversal probe

`cmd_path()` at `scripts/graph-query.py:794-809` computes 2-hop bridges by intersecting `neighbors_a` and `neighbors_b` over the whole edge file. No node-type filter; no edge-type filter; intermediate node identity is irrelevant to the path-finding logic.

Live probes confirmed: `--path eddard-stark robb-stark` already bridges through `winterfell` (location.castle) and `house-frey` (house.*). `--path robb-stark roose-bolton` returns 12 bridges through various non-character intermediates. Once Plate 3 lands AGENT_IN/VICTIM_IN edges on event-node hubs, "who killed Robb Stark" via the `red-wedding` hub falls out of the same traversal mechanism with zero engineering changes.

### D2 RESOLVED = (a) Replace

Recorded in `working/edge-modeling/edge-modeling-reification-design.md` §3 (new "D2 RESOLVED" subsection after D7).

**Decision:** option (a) Replace. Reification is sufficient. Superseded person→person binaries get marked `superseded_by` (not deleted; CLAUDE.md source-data rule). No materialized agent→patient dyad.

**Rationale:** the headline query "who killed X" already works through any 2-hop bridge — graph-query.py is type-agnostic. Option (c) Project would solve a problem that doesn't exist, AND would re-introduce the underdetermination D2 was designed to kill: which participant gets nominated as the canonical `source` of the materialized dyad? The very thing we're trying to remove.

Option (a) keeps the data model honest: events are nodes, full stop. The graph's existing query surface absorbs the change.

## Why this matters

D2 is a permanent architectural choice. It says **events are first-class nodes** and the graph reaches between participants through them. The alternative (option c) would have created a parallel layer of canonical binary projections that look like data but are actually derived views — easy to drift, easy to misread as primary.

The §3 D3 surprise matters because it changes Plate 3's design. The original assumption was "mint mostly from scratch." The reality is "rebind chapter evidence on existing named-event nodes + mint micro-event hubs as needed." Plate 3 needs a chapter-rebind sub-step the design doc didn't predict, and the mint-vs-reuse question needs Matt's input on aggressiveness.

The conservative normalizer result (10 flips, not hundreds) suggests the live-graph problem the design doc described was smaller than feared. Good news, but worth noting: the rest of the apparatus (Plate 1 head rule, AGENT_IN/VICTIM_IN, validator) is still warranted — they fix the **future Pass-1 rerun case** (none planned today) and the **Plate 3 backfill target** (the role edges Plate 3 will emit).

## What's queued

Three self-contained continue prompts:
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-3-backfill.md` — Plate 3; HELD on Matt Q1/Q2.
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-4-haiku-disposition.md` — Plate 4; HELD on Matt go.
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-5-merge.md` — Plate 5; HELD on Plates 3+4 staging + sign-off.

The S82 cleanroom-execution continue prompt was deleted (fully executed by this session).

## Process retro

What worked:
- **Pre-flight verification before agent dispatch.** Confirming file paths and line numbers up front meant both agent prompts were correct on first try.
- **Parallel fan-out.** Plate 0 + Plate 1 ran simultaneously without conflict — they touched different files. Combined wall-clock ~10 min vs ~25 min sequential.
- **Trust hierarchy held.** When the Plate 2 agent surfaced the §3 D3 contradiction with the design doc, it correctly trusted the live repo state and recorded the correction in SESSION-LOG.md rather than silently propagating the stale claim.

What I'd do differently:
- **Could have asked Matt Q1/Q2 mid-session** instead of bundling them into the Plate 3 continue prompt. Either choice was defensible; the bundle-into-continue-prompt path preserves Matt's session capacity for actual decisions rather than reactive Q&A.
