# Session 14 — Pipeline Flexibility Note (2026-04-25)

**Session type:** Documentation / clarification (very short)

## What happened

Matt asked, in passing while preparing to close this session and open a fresh one to start Track B, that the README and the agent's persistent memory should both reflect that the 5-pass extraction pipeline is **not set in stone**. Passes 2–6 (Wiki Ingester → Voice Analyzer → Foreshadowing → Theory → Discovery) are the *current* plan, but their scope, ordering, and even existence are open while Pass 1 is still being run and refined.

The motivation: as Pass 1 runs across all five books and Track B (wiki infobox parser) starts producing output, both will surface signals that should feed back into how later passes are structured. Matt didn't want a future-session agent — or himself in a future session — treating the pipeline table as a contract. He wants future redesigns of Passes 2+ to feel normal, not like a deviation from plan.

This is consistent with the existing `DECIDED: Track B Before v3 Schema Review` rationale from Session 13, which already acknowledges that Track B output may reshape the Pass 1 schema. The pipeline-not-fixed note generalizes that same reasoning to all later passes.

## Changes made

1. **README.md** — Added a callout under the "Extraction Pipeline" section (right after "Pass 1 is the foundation…"):

   > **The pipeline is not set in stone.** Passes 2–6 are the current plan, but their scope, ordering, and even existence are open while Pass 1 is still in progress. As we learn what Pass 1 outputs actually support (and what they're missing), later passes will be redesigned, merged, split, or dropped. Treat the table above as a working sketch, not a contract.

2. **Memory** — New file `memory/project_pipeline_not_fixed.md` (type: project) with rule + Why + How-to-apply lines. Linked from `MEMORY.md`. Key behavioral guidance: future-pass work should be framed as "current sketch, open to redesign," and Pass 1 gaps should be treated as inputs to redesigning later passes, not as Pass 1 bugs.

## What was decided / what surprised

Nothing strictly new was decided — this session formalizes a stance that was already implicit in the Track B sequencing rationale. The surprise was just that this stance hadn't been explicitly documented for future-session agents. Saving the memory closes that gap.

## What's next

Matt will close this session and open a fresh one to begin Track B work. The continue prompt for Track B orchestration planning is `progress/continue-prompts/2026-04-25-track-b-orchestration-planning.md` (PLAN-ONLY, output: `working/runbooks/wiki-pass2-orchestration.md`). After that runbook lands, parser implementation per `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`.

No continue prompts created or deleted this session. No extraction waves run. No new TODOs surfaced beyond what the Track B continue prompts already cover.
