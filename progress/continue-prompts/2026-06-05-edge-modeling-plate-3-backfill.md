# Plate 3 — Reify: mine Pass-1 → role edges on event hubs (+ node minting)

> **Recommended model:** Sonnet — pipeline construction (deterministic join + lift) and a Sonnet `claude -p` typing pass for legacy rows lacking role sub-bullets. Scope is resolved (Q1/Q2 below), so no Opus reasoning step is required for this plate.
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9). This is a task-scoped snapshot.
> **Context docs:** `working/edge-modeling/edge-modeling-reification-design.md` §3 (D2/D3/D5/D7) + the §3 "D2 RESOLVED" subsection + the Plate 2 report at `working/edge-modeling/plate2-event-coverage.md`.
> **PRECONDITIONS:**
> - Plate 1c (AGENT_IN/VICTIM_IN in schema + validator) LANDED (commit 5bc168b4d).
> - Plate 2 D2 RESOLVED → **Option (a) Replace** (graph-query.py traverses person→event→person fine; pure 2-hop hub is sufficient; do NOT emit a materialized agent→patient dyad).
> - Plate 0 normalizer outputs staged at `working/edge-modeling/normalizer-candidates.jsonl` (10 flips, 1 flagged) — NOT merged. Plate 5 gates the merge.

## PRE-WORK DECISIONS — RESOLVED (Matt, 2026-06-06)

Plate 2 surfaced two scope findings; both are now decided. Do NOT re-litigate — execute to these.

**Background (from Plate 2):**
1. The §3 D3 claim is **wrong in two of three motivating cases**: Tywin's privy death (`assassination-of-tywin-lannister`) and the Purple Wedding (`purple-wedding`) DO have existing nodes. Only Bran's defenestration genuinely needs minting. (See the design doc's `D3 RE-EXAMINED` note.)
2. Pass-1 yields **8,317 distinct event titles** — reify-all would mint ~8,300 micro-event hubs (mostly narrative beats like "Departure at daybreak"). Non-starter.

**Q1 — RESOLVED: reify-SELECTIVE.** Only events matching a curated trigger list become hubs. The trigger list is **exactly the "Reify" families from the design doc's disposition** — nothing else:
- killings / deaths / executions / poisonings / sacrifices (the death-violence family),
- weddings / ceremonies (incl. crownings, betrothleal set-pieces),
- sieges,
- conspiracies,
- captures / imprisonments,
- guest-right violations.
Everything else (plain travel, arrivals, observations, dialogue beats) stays as ordinary Pass-1 entries and is NOT reified. Rationale: these are precisely the underdetermined-head cases the project set out to fix; a "Departure at daybreak" has one actor and no head ambiguity, so a hub adds nothing. This keeps the graph dense, not confetti.

**Q2 — RESOLVED: run a confidence-gated fuzzy reuse pass BEFORE minting.** For each in-scope event, fuzzy-match its title against existing event-node titles/aliases (use `working/wiki/data/alias-resolver.json` + title-token overlap):
- **Auto-rebind** only on a high-confidence hit (exact alias match, or normalized-slug equality). E.g. `tywin-privy-death` → existing `assassination-of-tywin-lannister`.
- **Queue for review** (do NOT auto-rebind) on a merely-plausible fuzzy hit — token overlap alone is not enough; mis-binding an event is worse than minting a dup.
- **Mint** only when no candidate clears the bar.
Rationale: minting duplicates of nodes that already exist (`purple-wedding`, `assassination-of-tywin-lannister`) creates cross-identity cleanup debt later. Reuse first. Because Q1 makes the candidate set small (a few hundred, not 8,300), this pass is cheap and reviewable.

**Sequencing:** apply Q1's trigger filter FIRST (shrinks the universe), THEN Q2's fuzzy reuse on the survivors, THEN mint the remainder.

**Q1b — REFINEMENT (design-doc D8): reify on n-ary STRUCTURE, not event TYPE.** Within the trigger families, only reify an *instance* that is genuinely n-ary:
- **Clean dyad** (single agent + single patient, no instigator/ordering third party, not a shared named occasion) → DO NOT reify. Keep it as a direct typed edge (`KILLS source→target`), already direction-fixed by Plate 0. No hub, no role edges. (Jaime/Aerys is the archetype — nobody disputes the agent.)
- **N-ary instance** (instigator ≠ executor, multiple killers/victims, or a named set-piece other edges reference) → reify onto a hub as below.
This means D2=Replace touches ONLY the n-ary instances. Empirically almost all 102 KILLS are clean dyads, so expect to reify a SMALL number of contested events, most of which already have nodes. Do NOT mint a hub for a killing that just re-wraps a 2-party fact.

**PRECONDITION — Plate 2.5 Event-Node Inventory must exist.** Use `working/edge-modeling/event-node-reuse-lookup.json` (normalized-title/alias → existing event-node slug) as the reuse lookup for Q2. Reuse-before-mint is mandatory: every reify-target is matched against this lookup before any node is minted.

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

## Full-run engineering notes (from the Plate 3 SMOKE TEST on the Red Wedding, 2026-06-06)

The pipeline `scripts/edge-reify-backfill.py` was built and smoke-tested on the Red Wedding (`--smoke --event red-wedding`). It WORKED: 12 role edges, D7 applied cleanly (Roose Bolton → AGENT_IN as the personal killer; Walder/Lothar/Tywin → COMMANDS_IN as orderers; no instigator→victim collapse), validator Contract 10 passed, hub REUSED (not minted). Cost: ~$0.06 first call, ~$0.002–0.003/event warm → **full corpus ~$0.30–0.60** (well under the $2–10 budget). The full run must additionally handle these, surfaced by the smoke test:

1. **Group/faction actors. (CONFIRMED Matt 2026-06-06 — see `cleanup-decisions-resolved.md` §5.)** "Bolton men-at-arms", "musicians with crossbows" are group actors with no individual slug. AGENT_IN source may be a `house.*` slug (Plate 1c contract already allows house source). Emit e.g. `house-frey AGENT_IN <event>` for group action rather than dropping it.
2. **Cross-chapter dedup (mandatory).** An event spans chapters (Red Wedding: Catelyn VII + Arya X + Epilogue). Gather role candidates from ALL chapters whose events resolve to the same hub slug, then dedup by `(source_slug, role, event_slug)` before emitting. Without this, the same event re-fragments.
3. **Programmatic supersede detection.** The smoke test hand-listed the 9 superseded binaries. The full run needs a deterministic query: for each reified event, find every edge whose endpoints are both participants of that event AND whose `edge_type` is in the reify trigger family → mark `superseded_by: <hub>`. (The smoke list missed e.g. `catelyn-stark KILLS aegon-frey-son-of-stevron` — a clean dyad *inside* the set-piece.)
4. **Orderer-evidence confidence gate.** Indirect "countenanced"/"gave his blessing" evidence (Tywin) → `confidence_tier: 2`, not 1. Only explicit at-event orders get tier 1.
5. **`claude -p` MUST use `cwd=/tmp`.** The smoke call loaded 32k of project-context cache (it did not skip CLAUDE.md). Running with `cwd=/tmp` drops that — saves ~28–32k tokens/cold-call per the `reference_llm_pass_via_claude_p` memory.
6. **LOCATED_AT direction:** event → location (`<event> LOCATED_AT the-twins`), per architecture Entity→Location. State this in the per-row prompt so the LLM doesn't reverse it.
