# Plate 3 — Reify: mine Pass-1 → role edges on event hubs (+ node minting)

> **Recommended model:** Sonnet — pipeline construction (deterministic join + lift) and a Sonnet `claude -p` typing pass for legacy rows lacking role sub-bullets. Opus only if the reify-all-vs-selective scope question (see "PRE-WORK DECISION" below) is still open and needs reasoning.
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9). This is a task-scoped snapshot.
> **Context docs:** `working/edge-modeling/edge-modeling-reification-design.md` §3 (D2/D3/D5/D7) + the §3 "D2 RESOLVED" subsection + the Plate 2 report at `working/edge-modeling/plate2-event-coverage.md`.
> **PRECONDITIONS:**
> - Plate 1c (AGENT_IN/VICTIM_IN in schema + validator) LANDED (commit 5bc168b4d).
> - Plate 2 D2 RESOLVED → **Option (a) Replace** (graph-query.py traverses person→event→person fine; pure 2-hop hub is sufficient; do NOT emit a materialized agent→patient dyad).
> - Plate 0 normalizer outputs staged at `working/edge-modeling/normalizer-candidates.jsonl` (10 flips, 1 flagged) — NOT merged. Plate 5 gates the merge.

## PRE-WORK DECISION (Matt — required before launching this plate)

Plate 2 surfaced two findings that change Plate 3's scope:
1. The §3 D3 claim is **wrong in two of three motivating cases**: Tywin's privy death (`assassination-of-tywin-lannister`) and the Purple Wedding (`purple-wedding`) DO have existing nodes. Only Bran's defenestration genuinely needs minting. The actual mint scope is mostly *narrative micro-beats*, not famous set-pieces.
2. Pass-1 yields **8,317 distinct event titles**. If Plate 3 reifies *every* numbered Events & Actions entry, it mints ~8,300 micro-event nodes. That is almost certainly more than the graph wants.

**Matt's call (Q1):** Reify-all vs reify-selective?
- **Reify-all** — every Pass-1 event becomes a hub. Maximum information capture, but the graph swells dramatically and most hubs will carry one role edge.
- **Reify-selective** — only events that match a curated trigger list (kill/death/attack/poisoning/wedding/betrayal/capture/escape/coronation/oath, etc.) become hubs. Most narrative beats stay as plain Pass-1 entries. Recommended: this matches the underdetermination cases the project actually wants to fix and keeps the graph dense rather than confetti.

**Matt's call (Q2):** Reuse vs mint when a fuzzy-match against an existing event-node title looks plausible?
- The Plate 2 join used exact-slug match (1 hit). A fuzzy/title-matching pass would likely lift the "existing node" count from 1 to several hundred (e.g. `tywin-privy-death` vs `assassination-of-tywin-lannister`). Decide: run the fuzzy pass and reuse, or accept the slug-floor and mint freely.

Until Q1 + Q2 are resolved, **do not run the backfill.** The cost and shape both depend on the answer.

## Why

Once Q1/Q2 land, populate role edges (`AGENT_IN`, `VICTIM_IN`, `COMMANDS_IN`, `WIELDED_IN`, `LOCATED_AT`) on event-node hubs by mining Pass-1 source.

- The Haiku `**title**` field is NOT a usable grouping key (§2 #4 of the design doc — per-row micro-beats; only 5/1617 reference a slug). This is a fresh mining pass over Pass-1 source files, not a filter over the Haiku emits.
- The legacy Pass-1 entries have no role sub-bullets (the Plate 1b sub-bullets only help FUTURE Pass-1 runs, of which none are planned). All current rows go through the legacy Sonnet `claude -p` path. Cost is ~$2-10 (not ~$0) per §3 D5.

## Steps

1. **Node-minting sub-step** (depends on Q1 + Q2): for the events that need a hub, mint fine-grained `event.*` nodes (consider new leaves like `event.death`, `event.assassination`, `event.wedding`, or reuse `event.battle` more liberally — check `reference/architecture.md` event leaves). Deterministic slug from event title + occasion. **DEDUP across chapters** (e.g. the Red Wedding spans 3 chapters → ONE hub).
2. **Deterministic join**: for each chapter, match the in-scope `## Events & Actions` rows to event-node slugs (existing or newly minted) that include that chapter as evidence. Use the parser at `scripts/stage4-pass1-extra-tables.py:521` (`parse_events_section()`) or follow `scripts/plate2-event-coverage.py` for a working baseline.
3. **Lift roles**:
   - If role sub-bullets present (future Pass-1 output — none today): lift directly.
   - If absent (every current row): run a Sonnet `claude -p` pass (cwd=/tmp per `feedback_python_before_agent` memory + `reference_llm_pass_via_claude_p` memory) per row to extract {agent, patient, instrument, location, instigator} from the narrative line.
   - Apply §3 D7 causation rule: executor → `AGENT_IN`; orderer → `COMMANDS_IN`; never collapse instigator→victim (GATE 2 in the Stage-4 prompt already enforces this).
4. **Apply D2 = (a) Replace**: do NOT emit materialized agent→patient binaries. Mark superseded scattered binaries with `superseded_by` (keep them, don't delete — CLAUDE.md source-data rule). The reified hub + role edges are the only authoritative answer.
5. **Output staging only**: write all role edges to `working/edge-modeling/role-edges-staging.jsonl` and minted nodes to `working/edge-modeling/minted-event-nodes/`. Do NOT modify `graph/edges/edges.jsonl` or `graph/nodes/`. Produce a summary + sample for Matt.

## Done-criteria

- Every in-scope Pass-1 event has a hub (existing or minted) and ≥1 role edge.
- **Red Wedding hub populated as smoke test** (§1 of design doc): `roose-bolton AGENT_IN red-wedding`, `walder-frey AGENT_IN red-wedding` (or `COMMANDS_IN` per §3 D7 if Walder ordered rather than executed), `robb-stark VICTIM_IN red-wedding`, `catelyn-stark VICTIM_IN red-wedding`, etc. Validate by reading the staging output.
- Validator (`scripts/stage4-type-contract-validator.py` Contract 10) passes on all staged role edges.

## Out of scope

- Merging to canonical files (Plate 5).
- The Haiku bulk disposition (Plate 4).
- Touching node files outside the minted-nodes staging dir.
- Any Pass-1 rerun.

## Files this session may create/modify

- CREATE `scripts/edge-reify-backfill.py`
- CREATE `working/edge-modeling/role-edges-staging.jsonl`
- CREATE `working/edge-modeling/minted-event-nodes/`
- CREATE `working/edge-modeling/plate3-summary.md`
- DO NOT modify canonical `graph/` files.
- APPEND a section to `working/edge-modeling/SESSION-LOG.md` titled `## Plate 3 — backfill (Session N)`.
