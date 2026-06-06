# Plate 4 — Disposition of the 1,617 Haiku bulk emits

> **Recommended model:** Opus for the bucketing-review decision (the source FAILED its drift gate; this is a judgment call). Sonnet for any filter `claude -p` pass that follows the decision.
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9).
> **Context docs:** `working/edge-modeling/edge-modeling-reification-design.md` §3 (D6) + `SESSION-LOG.md` (Plate 0 normalizer report).
> **PRECONDITIONS:**
> - Plate 0a (head-direction normalizer) exists at `scripts/edge-direction-normalizer.py` (commit 5bc168b4d). Promote-as-is rows MUST pass through it first.
> - Plate 1c locked the vocab at 165 with `AGENT_IN`/`VICTIM_IN` for event-target validation.

## Why

The gated 1,617-row Events Haiku bulk lives at `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk/`. It FAILED the S74 drift gate (48% triple-level agreement vs 70% gate; 56% pair vs 85%) — a subject-selection drift failure that corrupts binary edges too. The prior bucketing was sample-derived. The bulk is currently un-promoted and gated awaiting Matt's escalation pick (S80/S81 — see worklog ~`Events edge enrichment (Stage 4)` line and `working/audits/events-haiku-bulk-2026-05-29/analysis.md`).

This plate decides per-row disposition under the reify lens:
- Edges that should become **role edges on event hubs** route to Plate 3 (reify candidates).
- Edges that survive as plain binary relations get normalized (Plate 0a) then promoted (Plate 5).
- Drift / inverted / mis-typed rows get dropped.

## Steps

1. **Fresh bucketing review** (Opus):
   - Re-classify the 1,617 rows under the reify/canonicalize/keep lens (NOT the prior wiki-comention lens).
   - State whether the classification is per-row or sample-extrapolated; if extrapolated, do a real per-row pass.
   - Expected buckets (validate, don't trust the prior counts):
     - `canon-structural` — `FIGHTS_IN`/`LOCATED_AT`/`COMMANDS_IN` style structural edges on existing event nodes. Promote.
     - `keep-binary` — true binary relations (e.g. `PARENT_OF` style). Promote.
     - `canon-dyadic-act` — Sonnet-filter borderline; promote survivors.
     - `reify@occasion` — should become role edges on a hub. **Route to Plate 3.**
     - `reify-hard` — needs minting a new hub. **Route to Plate 3.**
     - `keep-role-edge` — already role-shaped under the new vocab. Promote.
     - `unbucketed-drift` — drop.
2. **Normalize before promote**: run EVERY promote-candidate through the Plate 0a normalizer (`scripts/edge-direction-normalizer.py`). Any row whose direction flips is NOT "promote as-is" — it was carrying the inversion bug. Either flip and promote, or hold for review depending on the flip's confidence.
3. **Compose the action** and write to staging (NOT canonical):
   - `PROMOTE`: keep-binary + canon-structural + keep-role-edge survivors (post-normalize).
   - `SONNET-FILTER`: canon-dyadic-act (and ambiguous structural) → `claude -p` pass → promote survivors.
   - `HOLD`: reify candidates → feed Plate 3's hub backfill (write to `working/edge-modeling/plate3-from-haiku.jsonl` so Plate 3 can ingest).
   - `DROP`: unbucketed drift.
4. **Output**: `working/edge-modeling/haiku-bulk-disposition.jsonl` + a per-bucket summary in `working/edge-modeling/haiku-bulk-disposition.md` for Matt.

## Done-criteria

- Per-row disposition for all 1,617 rows.
- Promote-set has passed the normalizer (zero inverted rows promoted as-is).
- Reify candidates routed to Plate 3.
- Drift drops counted; reason recorded per row.

## Out of scope

- Merging to `edges.jsonl` (Plate 5).
- Touching the original Haiku bulk artifacts under `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk/`. Read-only on those.

## Files this session may create/modify

- CREATE `working/edge-modeling/haiku-bulk-disposition.jsonl`
- CREATE `working/edge-modeling/haiku-bulk-disposition.md`
- CREATE `working/edge-modeling/plate3-from-haiku.jsonl` (handoff to Plate 3)
- APPEND `## Plate 4 — Haiku bulk disposition (Session N)` to `SESSION-LOG.md`
- DO NOT modify canonical `graph/` files.
