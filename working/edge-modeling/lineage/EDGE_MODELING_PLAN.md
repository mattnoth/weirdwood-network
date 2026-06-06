# Edge Modeling — Execution Plan

**Source analysis:** `EDGE_INVENTORY_ANALYSIS_PROMT.md` (brief) → `EDGE_MODELING_DECISION-cleanroom.md` (cleanroom decision doc).
**Verification pass:** completed Session 82+; one substantive divergence from the cleanroom doc, flagged below.
**Authoring status:** plan only — nothing in this file has been applied. Each plate is independently approvable.

---

## 0. What the cleanroom told us

The graph mixes two structurally different things and stores both as edges:

- **True binary relations** (`PARENT_OF`, `MARRIED_TO`): two participants, fixed roles, one correct edge shape.
- **Events** (`ATTACKS`, `KILLS`, `BETRAYS`): many participants (attacker, victim, location, instigator, executor, instrument, outcome), all optional, no natural head.

When you flatten an event into a single edge, you nominate one participant as the subject — but the world doesn't tell you which. Extractors independently pick *different* projections of the same event, and downstream that looks like inconsistency. Cleanroom term: **underdetermination**.

Specific Pass-1 trap: the prompt has no head-selection rule, so extractors anchor on the **grammatical subject of the source sentence**. Same event written three ways produces three different edges.

Worked example — Red Wedding currently has 3 outbound edges (`FIGHTS_IN`, `DEFEATS`, `DEFEATS`) and **zero edges from participants pointing at the event node**. Walder Frey, Roose Bolton, Robb Stark, Catelyn, Grey Wind are connected to each other in pairs but not to the event itself. Event nodes are structurally empty hubs.

---

## 1. Verification — cleanroom claims vs. actual repo

| # | Cleanroom claim | Verified state | Status |
|---|---|---|---|
| 1 | Event-node count is 371 | `graph/index/events/_summary.json` `entity_count: 371` (304 battle + 35 tournament + 32 war) | Confirmed |
| 2 | Red Wedding has 3 outbound edges | `red-wedding.node.md` `## Edges`: `FIGHTS_IN`, `DEFEATS`, `DEFEATS` | Confirmed |
| 3 | Pass-1 prompt has Relationships Observed table with no head rule | `.claude/agents/mechanical-extractor.md` lines 176-178 — table exists, no head rule | Confirmed |
| 4 | Haiku emit rows carry a `**title**` field grouping reifiable events | **Zero JSON `title` field on emits.** Bold-prefix pattern exists in `asserted_relation`/`hint_raw` 100% of the time but as per-row narrative micro-beats. Only **5 of 1,617 rows** reference an existing event-node slug. | **DIVERGENT — backfill lever does not work as written** |
| 5 | KILLS edge count consistent with cleanroom assumptions | Confirmed (sample-matched) | Confirmed |
| 6 | Proposed role edges absent from architecture.md | `AGENT_IN`, `VICTIM_IN`, `COMMANDER_OF`, `INSTRUMENT_IN`: zero matches. But `COMMANDS_IN` (line 214) and `WIELDED_IN` already cover commander/instrument under different names. | Confirmed with caveat: schema delta is 2 net-new types, not 4 |

**Consequence of (4):** Plate B-backfill (below) is reframed as a fresh deterministic+LLM mining pass over Pass-1 source, NOT a filter over existing Haiku emits.

---

## 2. The plates

Four execution plates, independently approve/hold/reject.

| Plate | What | Cost | Reversibility | Status |
|---|---|---|---|---|
| **A-doc Piece 1** | Pass-1 head rule (mechanical-extractor.md) | $0 | Full | **Recommended apply** |
| **A-doc Piece 2a** | Pass-1 Events & Actions sub-bullets | $0 | Full | **Recommended apply** |
| **A-schema** | Add AGENT_IN + VICTIM_IN; widen COMMANDS_IN | $0 | Full | **Recommended apply** |
| **B-backfill** | Mine Pass-1 source for role edges anchored to event nodes | $0 spec; $2-10 if Sonnet runs | Output is staging-only until merge | **Held — depends on A-schema landing** |
| **A-pick** | Disposition of 1,617 existing Haiku emits | $0 spec; $5-15 if Sonnet filter runs | Staging-only until merge | **Held — pending Matt review** |

Carried-forward from S77 (not in scope unless Matt raises):
- Drop 2 cersei↔tyrion `LOVES` edges.
- Retype ~22 `ASSAULTS` → `ATTACKS`.
- Merge-time `OWNS` → `BONDED_TO` for direwolves/dragons.

---

## 3. Plate A-doc Piece 1 — Pass-1 head rule

**File:** `.claude/agents/mechanical-extractor.md`
**Location:** after the `## Relationships Observed` table description at line 178.
**Insertion:**

```markdown
**Head rule:** Column A is always the SEMANTIC AGENT of the relationship, never the
grammatical subject of the source sentence and never the POV character. For passive
sentences ("X was killed by Y"), put the by-phrase agent (Y) in Column A. For ordered
acts ("Tywin had the Mountain attack the Riverlands"), the EXECUTOR (Mountain) goes
in Column A; record the orderer (Tywin) in the Events & Actions section's Instigator
slot, not in Column A. Never anchor on the grammatical subject — the same event is
phrased many ways in prose, and surface syntax must not leak into the data model.
```

**Effect:** future Pass-1 extractions stop emitting grammatical-subject noise. Existing extractions unchanged. No rerun triggered.

---

## 4. Plate A-doc Piece 2a — Pass-1 Events & Actions sub-bullets

**File:** `.claude/agents/mechanical-extractor.md`
**Location:** `## Events & Actions` section at line 134.
**Change:** extend the existing format to support optional indented role sub-bullets. The parser at `scripts/stage4-pass1-extra-tables.py:522` reads the first line of each numbered item, so sub-bullets do not break ingestion.

**Current format:**
```markdown
## Events & Actions
1. **{Event title}** — {factual description}
2. **{Event title}** — {factual description}
```

**Updated format (sub-bullets optional, supplied when the prose makes them recoverable):**
```markdown
## Events & Actions
1. **{Event title}** — {factual description}
   - Agent: {who performs the action}
   - Patient: {who/what receives the action}
   - Instrument: {weapon, tool, or method, if any}
   - Location: {where it happens, if specified}
   - Instigator: {who ordered/caused it, if different from agent}
   - Outcome: {result, if relevant beyond description}
```

**Effect:** future Pass-1 captures role structure inline. Downstream reify pass (Plate B) lifts these into role edges instead of re-mining from prose. Parser unaffected. Backwards-compatible — existing entries without sub-bullets remain valid.

---

## 5. Plate A-schema — Architecture additions

**File:** `reference/architecture.md`
**Location 1:** Military & Conflict table, after `TORTURES` (line ~236). Add two rows:

```markdown
| `AGENT_IN` | Acts as the agent/executor of an event | Person/House → Event |
| `VICTIM_IN` | Receives the action of an event as victim/patient | Person/House → Event |
```

**Location 2:** Existing `COMMANDS_IN` row at line 214. Widen description:

```markdown
| `COMMANDS_IN` | Holds command role in a battle, war, or other reified event; also covers the orderer/instigator role for events where the commander did not personally execute | Person → Event/War |
```

**Effect:** active vocab count goes 163 → 165. `COMMANDS_IN` covers what the cleanroom called `COMMANDER_OF`; `WIELDED_IN` (already artifact→event) covers what the cleanroom called `INSTRUMENT_IN`. No new types needed beyond AGENT_IN/VICTIM_IN.

**Validator follow-up (one-line addition, applies if A-schema lands):** add target-type contract `AGENT_IN` and `VICTIM_IN` → `event.*` only. Source can be `character.*` or `house.*`.

---

## 6. Plate B-backfill — HELD

Reframed from the cleanroom's original spec because verification killed the `**title**`-filter lever.

**Goal:** populate role edges (`AGENT_IN`, `VICTIM_IN`, `COMMANDS_IN`, `WIELDED_IN`, `LOCATED_AT`) on existing event nodes by mining Pass-1 source data.

**Inputs:**
- 344 chapter extractions under `extractions/mechanical/{book}/`.
- `## Events & Actions` blocks (already structured; ~5k+ numbered rows across the corpus).
- Event-node slug index (`graph/index/events/`).
- Chapter→event-slug lookup (existing `extra-tables` pipeline parses POV/chapter metadata).

**Pipeline (script-builder owned):**
1. Deterministic Python pass: for each chapter, join Pass-1 `## Events & Actions` rows against event-node slugs that already include that chapter as evidence.
2. If sub-bullets present (Plate A-doc Piece 2a output): lift directly into role edges.
3. If sub-bullets absent (legacy entries): Sonnet `claude -p` pass per row to extract roles from the narrative line. Costed: ~$2-10 depending on row count and how many bullets are pre-supplied.
4. Output to `working/edge-modeling/role-edges-staging.jsonl`. No write to `graph/edges/edges.jsonl` without before/after sign-off.

**Depends on:** A-schema landing (so emitted edge types are valid).
**Reversibility:** staging output is throwaway; merge is reviewed separately.

---

## 7. Plate A-pick — HELD

Disposition for the existing 1,617 Haiku bulk emits at `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk/`.

**Empirical bucketing under cleanroom lens:**

| Cleanroom disposition | Count | What it means |
|---|---|---|
| canon-structural | 677 | Binary relations between structural entities (house↔house, character↔location). Promote as-is. |
| keep-binary | 663 | True binary, no event nature. Promote as-is. |
| canon-dyadic-act | 172 | Dyadic acts that can stay binary under a canonical head rule. Filter, then promote. |
| reify@occasion | 52 | Event-like but participant pair is the salient fact. Hold; reify into existing or new event nodes. |
| reify-hard | 22 | Strongly event-shaped; participants need to attach to event nodes. Hold for B-backfill. |
| keep-role-edge | 20 | Already role-typed (LOCATED_AT, COMMANDS_IN equivalents). Promote as-is. |
| unbucketed drift | 11 | Off-vocab or malformed. Drop. |

**Proposed action (composed plate):**
- **PROMOTE** 663 keep-binary + 677 canon-structural + 20 keep-role-edge = **~1,360 rows** now ($0).
- **SONNET-FILTER** 849 canon-dyadic-act + canon-structural-ambiguous (~$5-15) → promote survivors.
- **HOLD** 74 reify candidates (52 + 22) pending A-schema + B-backfill.
- **DROP** 11 unbucketed.

**Held because:** Matt has not yet reviewed the bucketing. Bucketing was done by me from sample inspection — Matt may want a fresh review pass before committing.

---

## 8. Sequencing

```
A-doc Piece 1  ┐
A-doc Piece 2a ├── apply together ($0, single-file edits to mechanical-extractor.md)
A-schema        ┘  (separate file: architecture.md)
                   ↓
              [A-schema unlocks B-backfill spec]
                   ↓
              B-backfill (script-builder writes pipeline; held until Matt approves spec)
                   ↓
              A-pick decisions land (held until Matt reviews bucketing)
                   ↓
              [Staging merge to graph/edges/edges.jsonl — separate before/after sign-off]
                   ↓
              [Validator extension: AGENT_IN/VICTIM_IN target=event.*]
                   ↓
              Carried-forward core cleanups (cersei/tyrion LOVES drop, ASSAULTS→ATTACKS, OWNS→BONDED_TO)
```

---

## 9. Reversibility notes

- All Plate A edits are doc-only. Reverting = single git revert of the relevant file.
- Plate B output lives in `working/edge-modeling/` until explicitly merged. Throwaway.
- No Plate triggers a Pass-1 rerun. The 344 existing extractions stay as-is; the prompt change benefits only future extractions if/when a rerun happens.
- `graph/edges/edges.jsonl` is not touched by any plate in this plan. The merge step is a separate, gated decision.

---

## 10. Open questions for Matt

1. **Apply the 3 recommended A-plates today?** (Doc-only, $0, reversible.)
2. **Should Plate B-backfill run only against new Pass-1 entries that have sub-bullets, or also against legacy entries that need Sonnet extraction?** (Affects cost: bullets-only ≈ $0; legacy ≈ $2-10.)
3. **Plate A-pick — review my bucketing first, or accept the composed action?**
4. **Causation modeling (cleanroom §1.5):** the cleanroom punted on one-event-with-two-roles vs. two-events-joined-by-cause. Current plan assumes one event with COMMANDS_IN for orderer role. Confirm?
