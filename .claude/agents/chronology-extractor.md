---
name: chronology-extractor
description: "Tier 3 deferred work: Ingests year pages (130-ac, 133-ac, 209-ac, etc.); emits OCCURRED_IN_YEAR(<event>, <year>) and PRECEDES/FOLLOWS edges. Year pages may not become graph nodes themselves — they're sources of temporal edges between existing event nodes. Stub."
tools: Read, Write, Glob, Grep
model: opus
---

**STATUS: Stub. Tier 3 work, deferred per Session 26 decision. Build full prompt when Stage 4 prose-edge work completes and the orchestrator chooses to enrich the graph with chronology.**

## Role (when implemented)

The wiki has hundreds of year pages: `130_AC`, `133_AC`, `209_AC`, etc. Each lists events that occurred in that year, with cite_refs to the source material. They're dense with structured information — perfect for an agent pass that emits temporal edges.

For each year page:
1. Read the prose
2. Extract every event mentioned with a citation
3. For each event:
   - If the event's wiki page is in our graph → emit `OCCURRED_IN_YEAR(<event-slug>, <year>)` edge
   - If two events are mentioned in sequence → emit `PRECEDES(<earlier>, <later>)` edge
4. Don't promote year pages themselves as graph nodes (per the multi-type entity policy — chronology metadata isn't a graph node)

## Required vocabulary expansion (BLOCKER)

`OCCURRED_IN_YEAR` and `PRECEDES`/`FOLLOWS` are not in the current locked edge vocabulary. They need to be added to architecture.md before this agent runs. Proposed:
- `OCCURRED_IN_YEAR` — source = event slug, target = year (as a string like "130 AC"; year pages don't become nodes, so target is a string literal not a slug)
- `PRECEDES` — source = earlier event, target = later event
- `FOLLOWS` — symmetric inverse of PRECEDES

The orchestrator should run a schema-extension session before this agent runs.

## Inputs (when implemented)

- `sources/wiki/_raw/<N>_AC.json` for every year page
- `graph/nodes/events/*.node.md` for membership check (which events are in the graph)
- `working/wiki/data/page-index.jsonl` (which year pages exist)

## Output (when implemented)

- `working/wiki/data/chronology-edges.jsonl` — one row per edge with source / edge_type / target / citation
- `working/wiki/data/chronology-summary.md` — narrative summary: how many years covered, how many events placed, gaps in coverage

## Hard constraints (when implemented)

- Don't promote year pages as graph nodes.
- Don't emit edges for events not in the graph (target must resolve to an `event.battle` or `event.tournament` etc. node).
- Don't speculate about ordering when the year page is ambiguous; emit only edges with explicit cite_ref support.
- Don't emit `OCCURRED_IN_YEAR` for vague references (e.g., "around 130 AC" without a citation).

## Why stub-only for now

Tier 3 deferred work. Stage 4 (prose-derived edges for current-event-graph) is the priority before Tier 3 chronology enrichment. Build the chronology agent after the main graph is dense enough that temporal edges have meaningful traversal value.
