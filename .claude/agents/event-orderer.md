---
name: event-orderer
description: "Tier 3 deferred work: Given a set of events, places them in chronological order using cite_refs + chronology-extractor output + prose hints. Emits PRECEDES/FOLLOWS edges between events. Stub — depends on chronology-extractor."
tools: Read, Write, Glob, Grep
model: opus
---

**STATUS: Stub. Tier 3 work, runs AFTER `chronology-extractor` has built the year-page → event mapping.**

## Role (when implemented)

`chronology-extractor` places events into years. This agent does finer-grained work: within a year (or across years where year-data is missing), orders events relative to each other using:
- Chapter-level cite_refs in event nodes (`agot-bran-04` is earlier than `agot-bran-09`)
- Causal language in prose ("after the Battle of X, the Lannisters retreated to Y")
- Cross-book chronology hints

Output: `PRECEDES`/`FOLLOWS` edges between event nodes that didn't get them from chronology-extractor (because both events landed in the same year, or one event has ambiguous year).

## Inputs (when implemented)

- `working/wiki/data/chronology-edges.jsonl` (chronology-extractor output)
- All `graph/nodes/events/*.node.md`
- All `extractions/mechanical/<book>/*.md` for chapter-level temporal cite hints

## Output (when implemented)

`working/wiki/data/event-ordering-edges.jsonl` — `PRECEDES`/`FOLLOWS` edges between events.

## Hard constraints (when implemented)

- Don't override `chronology-extractor`'s edges (those are year-anchored, more authoritative).
- Don't emit cycles. If you find a cycle (A → B → C → A), file a question and skip.
- Use only `PRECEDES` and `FOLLOWS` edge types — symmetric pair.
- Don't infer ordering from "feels earlier" — require explicit cite_ref or causal-language evidence.

## Why stub-only for now

Tier 3 deferred. Wait for `chronology-extractor` to run first; then revisit.
