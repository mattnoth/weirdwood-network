# Mission: Stage 4 v1 Bulk Prose-Edge Classification on Sonnet

**Goal:** Run the prose-edge-classifier on **all queued candidate files** for Stage 4 v1, on Sonnet 4.6 (smoke-test-validated 2026-05-13). Three candidate shapes processed: `source_target`, `comention`, `pass1_relationship`. Output is prose-derived edge JSONLs at canonical paths, ready for the promoter to append to node bodies.

**Status:** queued
**Created:** 2026-05-14
**Recommended model:** Sonnet 4.6 (`claude-sonnet-4-6`) for workers; reviewer can be Opus when budget allows.
**Execution mode:** Multi-window. Watcher in dedicated window. N workers in N parallel Claude Code windows (recommended N=5-10 depending on Matt's monitoring bandwidth).

---

## Why this mission

Smoke test verdict (2026-05-13 Session 53b head-to-head): patched Sonnet returned CONCERNS-low (3.9% issue rate, no systematic patterns, correctly filed vocabulary-gap questions). Patched Haiku returned CONCERNS-high (5.4% issue rate, two systematic bugs: `FORGED_BY` for materials, `TRAVELS_TO` for persons). Effective cost after rework: Sonnet ~$500-700, Haiku ~$200-300 but with corruption-shaped errors. Decision: Sonnet.

Stage 4 v1 fills the **63 unpopulated edge types** (out of 121 canonical) — perception, prophecy, magic, causal, narrative, plus the new Session-53 artifact-history types. Today's graph (21,087 edges, all infobox-derived) has zero instances of `FEARS`, `MOURNS`, `FORESHADOWS`, `DREAMS_OF`, `WARGS_INTO`, `RESURRECTS`, `SACRIFICES`, `CURSES`, `MADE_OF`, `GIFTED_TO`, `LOOTED_BY`, `WIELDED_IN`, `INHERITED_BY`, `REFORGED_INTO`, etc. Tier-difference: the difference between "structured feudal wiki" and "graph that knows the story."

---

## Scope

### In (3 candidate shapes, ~170-200k candidate rows total)

| Shape | Source script | Volume | Output path |
|---|---|---|---|
| `source_target` | `scripts/wiki-pass2-build-edge-candidates.py --apply` | 141,067 candidates across 5,686 source slug files | `working/wiki/pass2-buckets/<bucket>/prose-edges/<source-slug>.edges.jsonl` |
| `comention` | `scripts/wiki-pass2-build-comention-candidates.py --apply` | 29,259 candidates across 344 chapter files | `working/wiki/pass2-buckets/meta-chapters-<book>/prose-edges/<chapter-slug>.comention-edges.jsonl` |
| `pass1_relationship` | `scripts/wiki-pass2-build-pass1-relationship-candidates.py --apply` (built same-session) | ~10-17k candidates across ~344 chapter files | `working/wiki/pass2-buckets/extractions-pass1/<book>/prose-edges/<chapter-slug>.pass1-edges.jsonl` |

Total input files: **~6,374**. Estimated total candidates: **~180-187k**.

### Priority order (per Matt's directive)

1. **Characters** (source_target, characters-* buckets) — ~3,500-4,500 source slug files. Highest-value substrate.
2. **Artifacts** (source_target, tier3-pathb-artifacts + other artifact buckets) — ~100-200 source slug files. Smaller but high-density (new artifact-history types).
3. **Chapter-summary comention** (344 files) — chapter-scene edges (perception, capture, prophecy fulfillment).
4. **Pass 1 relationships** (~344 files) — book-prose-derived edges, highest-precision evidence.
5. Other source_target shapes (locations, houses, factions, etc.) — process after the priority-tier completes; lower priority for v1.

### Out (not this mission)

- **Promotion to node bodies** — separate mission after bulk classification + reviewer pass. Uses `scripts/wiki-pass2-promote-prose-edges.py` (to be written).
- **Contradiction sweep** — separate sub-pipeline (Pass 1 vs wiki disagreements). After promotion.
- **Cross-identity follow-on** — `cross-identity-detector` agent processes escalations after bulk run.
- **`graph/nodes/*`** — never modified by workers. The promoter handles all node-body changes.
- **`sources/wiki/_raw/`** — read-only per project rule.

---

## Pre-flight (orchestrator session does these before launching workers)

1. **Verify Pass 1 generator built and ran cleanly.** Confirm:
   ```bash
   ls scripts/wiki-pass2-build-pass1-relationship-candidates.py
   wc -l working/wiki/pass2-buckets/extractions-pass1/*/*.candidates.jsonl | tail -1
   ```
   If absent: build via script-builder (spec in `progress/continue-prompts/2026-05-14-stage4-bulk-sonnet-launch.md`).

2. **Verify vocabulary current.** `reference/architecture.md` should declare ~121 types (Session 53 + 53b additions). Confirm:
   ```bash
   python3 scripts/build-edge-type-counts.py
   # Expected: Canonical types: 121, Drift types: 0
   ```

3. **Verify classifier prompt is patched.** `.claude/agents/prose-edge-classifier.md` should have:
   - "Type discipline" section with type-contract enforcement
   - 121-type vocabulary expansion
   - `MADE_OF`, `LOOTED_BY`, `REFORGED_INTO`, `GIFTED_TO`, `INHERITED_BY`, `WIELDED_IN`, `EXECUTED_WITH` in the Possession & Ownership bullet
   - "Vocab-gap over silent reject" default

4. **Build mission state file.**
   ```bash
   mkdir -p working/missions/2026-05-14-stage4-v1-bulk-sonnet/
   python3 scripts/mission-stage4-init.py  # to be written; generates batch manifest
   ```

5. **Open watcher window.** Run `/watcher` skill or paste watcher prompt (in this file below).

6. **Dispatch N worker windows.** Each gets the worker template (in `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md`).

---

## Worker assignments (batched for parallelism)

Each worker claims a **batch** of input candidate files atomically via filesystem lock-files (mission state dir). Worker template handles claim/process/release/repeat.

**Batch shape:** ~30 input files per batch (balances per-worker work-stream against per-claim overhead). At ~$0.10 average per file on Sonnet → ~$3 per batch.

**Estimated batch count:** ~6,374 / 30 = **~213 batches**.

**Wall-clock projection:**
- Per-batch time on Sonnet: ~30-50 min (depends on file size + candidate count)
- 10 parallel workers: ~213 batches × ~40 min / 10 workers = **~14 hours**.
- 5 parallel workers: ~28 hours.
- Realistic overnight: 8-10 workers for ~14h overnight → completes by morning.

**Per-batch cost on Sonnet:** ~$2-4. Total: **$400-850** range.

---

## Worker lifecycle

```
[claim batch] → [process N files] → [release lock + write batch-results.json] → [exit]
```

Workers do NOT auto-continue to next batch in same session — that risks runaway. Each worker invocation handles one batch and exits. Matt re-fires the same worker prompt in the window to claim next batch. **Optionally** the `/loop` skill on a 60-minute interval auto-restarts the worker — this is the "overnight" play.

Workers emit:
- The classified edges JSONL at canonical paths (per shape)
- A `batch-results.json` to `working/missions/2026-05-14-stage4-v1-bulk-sonnet/results/<batch-id>.json` with: files processed, decision counts, vocabulary-gap questions filed, errors encountered
- Append-only updates to `working/missions/2026-05-14-stage4-v1-bulk-sonnet/state.jsonl` (claim + release events)

---

## Success criteria

- **100% of priority-tier input files have output files.** (Characters + artifacts + chapter-comention + Pass 1 → all four shapes complete.)
- **Reviewer verdict on a stratified 5% sample is CLEAN or CONCERNS-low** (use `prose-edge-reviewer` agent).
- **Zero vocabulary violations** (drift check via `scripts/build-edge-type-counts.py` post-promotion).
- **Zero infobox-edge modifications** — only `## Edges (prose-derived)` subsections touched (validator confirms byte-equality on `## Edges` section).
- **Vocabulary-gap questions filed** — expected count is non-zero. Workers SHOULD surface gaps the prompt's vocab missed.

---

## Watcher hookup

Dedicated Claude Code window runs the watcher with the prompt in `working/agent-fleet-specs/missions/2026-05-14-stage4-v1-bulk-sonnet-watcher-prompt.md` (sibling file). Watcher monitors:

- `working/missions/2026-05-14-stage4-v1-bulk-sonnet/state.jsonl` — append-only claim/release events from workers
- `working/missions/2026-05-14-stage4-v1-bulk-sonnet/results/` — batch-results.json files as workers complete batches
- `working/wiki/pass2-buckets/questions-for-matt.jsonl` — vocabulary-gap and other questions workers file (alert if a gap question appears N times → systematic missing type)
- Output paths to spot-check edge JSONL files for schema integrity

Watcher does NOT dispatch workers. Watcher reports state. Matt dispatches.

---

## Escalation rules

- **Worker stuck for >2× expected batch time** (≥90 min) → watcher flags; Matt manually inspects.
- **Vocabulary-gap of same type filed by ≥3 different workers** → STOP all workers, add type to architecture.md + prompt, restart.
- **Drift detected** (edge type not in vocab emitted) → STOP affected worker, investigate prompt regression, restart only after fix.
- **Per-batch cost exceeds $10** → STOP, investigate token-budget blowup.
- **Reviewer mid-flight sample returns CONCERNS-high or worse** → STOP all workers, audit, decide whether to continue.

---

## Mission completion

When 100% of priority-tier input files have outputs:

1. **Stratified reviewer pass** — `prose-edge-reviewer` on ~5% sample across all 4 shapes.
2. **Run `scripts/build-edge-type-counts.py`** for the post-bulk snapshot. The before/after delta tells us which of the 63 unpopulated types got filled.
3. **Write session-results file** at `working/session-results/<DATE>-stage4-v1-bulk-sonnet-results.md` per convention.
4. **Mission archive**: move this file from `working/agent-fleet-specs/missions/` to `working/agent-fleet-specs/missions/done/`. Add timestamps to mission state. Update worklog session entry.
5. **Hand off to promotion mission** — separate mission for `wiki-pass2-promote-prose-edges.py` writing accepted edges into node bodies under `## Edges (prose-derived)` subheadings.

---

## Reference

- Mission protocol: `working/agent-fleet-specs/mission-protocol.md` (v1 DRAFT)
- Watcher runbook: `working/runbooks/general-watcher.md`
- Worker template: `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md` (sibling)
- Watcher prompt: `working/agent-fleet-specs/missions/2026-05-14-stage4-v1-bulk-sonnet-watcher-prompt.md` (sibling)
- Continue prompt for fresh session: `progress/continue-prompts/2026-05-14-stage4-bulk-sonnet-launch.md`
- Smoke test verdict: `working/session-results/2026-05-13-stage4-prose-edge-classifier-phase1.md` + reviewer Agent ID `ae91d57e1fa09c3ec`
- Classifier prompt (patched): `.claude/agents/prose-edge-classifier.md`
- Vocabulary candidates ledger: `curation/edge-vocabulary-candidates.md`
