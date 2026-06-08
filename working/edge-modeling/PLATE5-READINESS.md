# Plate 5 Readiness — What would land in `graph/` if merged today

**As of:** 2026-06-08 (post-Plate-3 + Plate-4-cluster + human-triage)

Plate 5 is the **single irreversible step** in the edge-modeling sequence. It takes
every staged artifact across Plates 0/1/2.5/3/4-cluster + the S77 carryover
cleanups and writes them into `graph/`. Requires Matt's before/after sign-off.

**Nothing in this doc has been applied.** `graph/edges/edges.jsonl` = 3,811
(unchanged since Session 76). `git status graph/` = clean.

---

## Inventory of staged changes by plate

### Plate 0 — deterministic edge corrections ($0, S83)
- **10 edge-direction flips** staged at
  `working/edge-modeling/normalizer-candidates.jsonl` +
  `working/edge-modeling/normalizer-diff.md`
- **3 phantom-Aerys repoints** (3 edges where `aerys-targaryen` → `aerys-ii-targaryen`)
  at `working/edge-modeling/aerys-merge-candidates.jsonl`
- **1 mutual-kill case** flagged for human review at
  `working/edge-modeling/flagged-for-review.jsonl`
- **Net spine impact**: 3,811 + 0 (corrections only, no count change)

### Plate 1 — doc + schema additions ($0, S83)
- `AGENT_IN`, `VICTIM_IN`, `COMMANDS_IN` widened in
  `reference/architecture.md` (vocab 163 → 165)
- Contract 10 added to `scripts/stage4-type-contract-validator.py`
  (AGENT_IN/VICTIM_IN target MUST be event.*)
- `.claude/agents/mechanical-extractor.md` updated (head rule + Events sub-bullets)
- **Net spine impact**: 0 (schema only; future runs use this)

### Plate 2 — D2 design decision ($0, S83)
- D2 RESOLVED → **Replace** (no materialized agent→patient dyad on
  reified events; use 2-hop traversal via event hub)
- Recorded in `working/edge-modeling/edge-modeling-reification-design.md` §3
- **Net spine impact**: 0 (design only)

### Plate 2.5 — staged cleanups (S84)
- **12 drift-reclassify candidates** (chapter articles misfiled as
  `event.battle` → should be `meta.chapter`):
  `working/edge-modeling/drift-reclassify-candidates.jsonl`
  - Affects 0 edges (just retypes the nodes)
- **4 high-conf collision-merge candidates** (near-dup event groups):
  `working/edge-modeling/collision-merge-candidates.jsonl`
  - Would merge ~4 event-node pairs, repoint their edges
- **Net spine impact**: 0 edge count change, ~4 nodes merged, 12 nodes retyped

### Plate 3 — Plate-3 reification (S84 + autonomous 2026-06-07)
- **219 minted event-nodes** in
  `working/edge-modeling/plate3-full/minted-event-nodes/`
  - 1 reuse-matched an existing wiki event (`sack-of-winterfell`)
  - 218 are new event-nodes (chapter-beat granularity)
- **914 role edges** (AGENT_IN/VICTIM_IN/COMMANDS_IN/LOCATED_AT) in
  `working/edge-modeling/plate3-full/role-edges-staging.jsonl`
- **55 supersede candidates** in
  `working/edge-modeling/plate3-full/supersede-candidates.jsonl`
  - Existing `KILLS`/`BETRAYS`/etc edges flagged as replaceable by the new event hubs
- **109 hub-review-queue entries** (borderline, awaiting your triage) at
  `working/edge-modeling/plate3-full/hub-review-queue.jsonl`
  - 75 borderline-single-agent (per D8, these should stay as direct dyads)
  - 32 non-harming-multi-agent (likely DROP — micro-beats)
  - 2 fuzzy-match candidates
  - **Triage list:** `working/edge-modeling/plate3-full/HUB-REVIEW-TRIAGE-LIST.md`
- **Net spine impact (if all promoted)**: +914 role edges, +218 new event-nodes,
  -55 superseded edges (replaced by 2-hop via hub) = net +859 edges, +218 nodes
- **But:** the wiki-vs-chapter taxonomy mismatch means most mints are
  chapter-beat granularity, NOT canonical historical events. Decision needed on
  whether to promote them as same-tier with wiki events or as a sub-tier.

### Plate 4 (cluster) — wiki-vs-chapter bridge (today)
- **54 cluster edges** at
  `working/edge-modeling/plate4-wiki-cluster/cluster-edges-staging.jsonl`
  - 51 SUB_BEAT_OF (mint → wiki canonical event)
  - 3 DUPLICATE_OF (mint is the same as wiki event; should merge nodes)
- Provenance: 12 haiku-pass-a / 33 opus-pass-b / 7 sonnet-pass-c / 2 human-triage
- Reconciled per-mint decisions at
  `working/edge-modeling/plate4-wiki-cluster/wiki-cluster-RECONCILED.jsonl`
- **Validated:** 18/18 spot-checked = 100% precision
- **Net spine impact (if applied)**: +51 SUB_BEAT_OF edges, 3 mint→wiki node merges
- Cost: $34.74 (Pilot $0.50 + Pass A $5.09 + Pass B $21.91 + Pass C partial $7.24)

### S77 carryover cleanups (still pending Matt sign-off)
- **Drop 2 mis-typed edges**: `cersei↔tyrion LOVES` (×2). Net spine: -2.
- **Retype ~22 edges**: `ASSAULTS` → `ATTACKS` (per architecture.md
  ASSAULTS=sexual-only rule)
- **Retype direwolf/dragon ownership**: `OWNS` → `BONDED_TO` (small count, Events-bulk output)
- **Net spine impact**: -2 edges, ~22 retypes

---

## If you signed off on EVERYTHING today

| Item | Before | After | Delta |
|---|---:|---:|---:|
| `graph/edges/edges.jsonl` count | 3,811 | ~4,724 | +913 |
| `graph/nodes/events/` count | 371 | ~582 | +211 |
| Edge-type vocab | 163 | 165 (+`SUB_BEAT_OF`, `DUPLICATE_OF`?) | +2 to +4 |
| Node retypes (drift) | 0 | 12 (battle → chapter) | 12 |
| Node merges (collisions + DUPLICATE_OF) | 0 | 7 (4 collision + 3 dup) | 7 |
| Schema bugs to fix | (varies) | feast-honor type=battle→ceremony | |

**Caveat**: that "everything signed off" number assumes you accept the chapter-beat
mints as new event-nodes in the same tier. If you prefer dual-taxonomy
(`event_tier: canonical | pass1-beat`), the merge changes meaningfully —
chapter-beats go to a sibling directory and the SUB_BEAT_OF edges link layers.
**That design decision is unresolved.** See continue prompt
`progress/continue-prompts/2026-06-08-alias-and-display-design.md`.

---

## Issues SURFACED today (need fix before next Plate 4 cluster run)

1. **`feast-in-honor-of-king-roberts-visit-to-winterfell` is mistyped** as
   `event.battle` in the wiki ingestion. It's a feast, not a battle. This
   schema bug caused it to appear as a top-3 candidate for **7 of 23**
   human-triage cases (all false positives). Fix: re-type to `event.feast` /
   `event.ceremony` at the wiki layer.

2. **Narrowing function over-weights mass-participant events.**
   `feast-in-honor-...` has Robert/Ned/Cersei/Tyrion/Jaime/Joffrey/Sansa/Arya/
   Bran etc. all in its wiki-link tokens — overlap with any chapter mint with
   ANY Stark/Lannister participants. Need IDF-style downweighting on
   high-frequency participants when scoring candidates.

3. **Historical pre-series events appearing as candidates** for current-arc mints
   (`battle-above-the-gods-eye` Dance of Dragons, `battle-on-the-river-slayne`
   Coming of Andals). Should add a soft filter: if wiki event's era is
   "historical" vs "current-narrative", deprioritize for current mints.

4. **Real events missing from the wiki layer** (Pass-1 captures them but no
   canonical wiki node exists):
   - "Capture of Tyrion Lannister at the crossroads inn" (AGOT)
   - "Holdfast fight where Yoren is killed" (ACOK Arya IV)
   - "Robert's assassination by boar (Cersei orchestrated)" (AGOT)
   - "Winterfell murders during Stannis approach" (ADWD Theon)
   - "Tyrion's Vale clansmen attack" (AGOT Tyrion IV)
   - Slaver's Bay events (Hizdahr hostage exchanges, etc.)
   Worth a NEW wiki-derived event-node creation pass eventually.

---

## What to do at Plate 5 itself (when you're ready)

When you decide to actually do Plate 5:

1. Write `scripts/plate5-merge.py` (does not exist yet)
2. Run with `--dry-run` first — shows exactly what would change
3. Show you a before/after diff per file affected
4. Require explicit `--apply` flag to write
5. Auto-commit changes to git with a `Plate 5: ` message prefix
6. Update `worklog.md` with a Plate 5 entry recording the deltas

Suggested merge order (most-conservative first, so failures stop early):
1. Plate 0 corrections (deterministic, easy to verify)
2. Plate 2.5 node retypes + collision merges
3. S77 cleanups (small, easy to verify)
4. Plate 4 SUB_BEAT_OF + DUPLICATE_OF (new edge type, isolated)
5. Plate 3 minted event-nodes + role edges (biggest delta; do last)

---

## Open design questions blocking Plate 5

- **Dual-taxonomy vs single-taxonomy** for Plate-3 mints — see
  `progress/continue-prompts/2026-06-08-alias-and-display-design.md`
- **109 hub-review-queue items** need your triage (which to mint vs drop)
- **3 deferred mints from 23-mint triage** (tyrion-processes-the-assassination-attempt;
  tyrion-s-battle-dream; unnamed-spearman-attacks-drogon) need a follow-up call
- **The 4 wiki schema fixes flagged above** (feast type, narrowing IDF,
  historical-event filter, missing-node candidates) — should run before any
  re-classification pass
