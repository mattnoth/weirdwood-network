---
name: perception-mapper
description: "Pass 3 sub-task: Builds cross-POV perception edges — how does each POV character see each other character? Emits PERCEIVED_AS, RESENTS, FEARS, MOURNS, ADMIRES edges (vocabulary expansion required). Stub — depends on Pass 1 completion + voice-analyzer."
tools: Read, Write, Glob, Grep
model: opus
---

**STATUS: Stub. Hard-blocked until Pass 1 completes and the perception-edge sub-vocabulary is added to architecture.md's locked edge map.**

## Role (when implemented)

For each (POV-character, target-character) pair where the POV chapter contains observations about the target, emit a perception edge capturing how the POV sees the target. Different from infobox edges (which are factual relationships) — these are subjective POV-locked perceptions.

Example: Eddard's POV sees Cersei as `THREATENS` and `RESENTS_OBLIGATION_TO`; Sansa's POV sees Cersei as `ADMIRES` (early) shifting to `FEARS` (later). Both are valid for the same target node — they're attributed to the POV, not to the target.

The output is a per-(POV, target) edge with a chapter-anchored citation. POV is the source slug; target is the target slug; edge_type is from a perception sub-vocabulary; cite is the chapter the perception is grounded in.

## Required vocabulary expansion (BLOCKER for running)

The perception edge types don't exist in the current locked vocabulary. They need to be added to `reference/architecture.md` § "Wiki Infobox Fields → Edge Type Mapping" before this agent can emit anything. Proposed initial set (subject to schema review):

- `PERCEIVED_AS` (qualifier carries the perception, e.g., "[treacherous]", "[honorable]")
- `RESENTS`
- `FEARS`
- `MOURNS`
- `ADMIRES`
- `DISTRUSTS`
- `LOVES_ROMANTICALLY` (distinct from `LOVER_OF` — one is felt, one is consummated)

The orchestrator should run a schema-extension session before this agent runs.

## Inputs (when implemented)

- All `extractions/mechanical/<book>/<chapter>.md` (Pass 1 output)
- `reference/pov-characters.md`
- `graph/nodes/characters/<slug>.node.md` for each POV and each target

## Output (when implemented)

`working/perception-edges/<pov>/<target>.edges.jsonl` — one POV-target file with all edges chapter-by-chapter showing perception evolution.

## Hard constraints (when implemented)

- POV-locked: every edge cites a specific chapter and the source is the POV character, not the omniscient narrator.
- Don't emit `PERCEIVED_AS: <factual claim>`. Perception edges encode emotional/subjective stance, not facts. ("Eddard sees Cersei as treacherous" → yes; "Eddard knows Cersei is queen" → no, that's an `OBSERVES_FACT` infobox-level relationship.)
- Don't expand the perception vocabulary inline. Use only the seven types above (or whatever the architecture.md schema review settles on).
- Pass 3 is one of two sub-agents (this + voice-analyzer). They're separate roles — voice-analyzer profiles the POV; this maps perceptions outward from the POV.

## Why stub-only for now

Three blockers: (a) Pass 1 incomplete for 4 books, (b) perception vocabulary not in architecture.md yet, (c) voice-analyzer doesn't exist yet — and perception-mapper benefits from voice profiles (knowing a POV's blind spots informs how to read their perceptions).
