# history/ — Frozen Records

This directory holds everything that was once active project state and is now sealed. **Nothing here is ever edited after it is written.** These are records of thought-at-the-time; correcting them would destroy their value as an honest log.

Moves within `history/` are permitted (the S36 hygiene pass relocated several files here). Nothing ever leaves `history/` for deletion or overwriting.

---

## Subdirectories

### [worklog-archives/](worklog-archives/README.md)
Rotated worklog session entries. `worklog.md` in the repo root holds at most 5 sessions; when a 6th arrives the oldest moves here. Each `archiveNNN.md` holds exactly 5 entries in reverse-chronological order. Archives 001–018 cover Sessions 0–86. Two non-archive files (`extraction-progress.md`, `session-32-handoff.md`) also live here from a S36 hygiene pass. See the [README](worklog-archives/README.md) for the full file-by-file index, anomaly notes, and era labels.

### [session-details/](session-details/README.md)
Per-session long-form narratives written for design sessions, incidents, and novel decisions (CLAUDE.md rule 7 — not every session). Sessions 000–086 are covered, with intentional gaps for pure-execution sessions. See the [README](session-details/README.md) for the complete table: file, date, subject, and which project-story chapter covers that era.

### [project-story/](project-story/00-overview.md)
A narrative account of the whole project written in June 2026 after Session 91. Eight files: an [overview](project-story/00-overview.md) with a phase-by-phase timeline, six thematic chapters (scaffolding era, book passes, wiki work, edge layer, infrastructure, reification), and a [glossary](project-story/glossary.md) of internal vocabulary. Start with `00-overview.md`. This series covers the same history as `worklog-archives/` and `session-details/` but organized by topic and written for a reader unfamiliar with the project's internals.

### [todo-archives/](todo-archives/)
Resolved or superseded blocks moved verbatim out of `working/todos.md`. Currently holds one file: `2026-06-11-resolved-blocks.md`, produced during the 2026-06-11 fable-audit todos cleanup. Items here were either fully resolved or collapsed to one-liners in the live todos. Append-only — new dated files per cleanup.

### [archive/](archive/)
Retired design documents and sketches that were once live working files. Two categories:
- Root-level: `stage3b-design-review-2026-04.md` — a second-opinion design review from S26 for the Stage 3b Python pivot decision.
- `sketches/`: `chat-ui-architecture.md` and `diagrams.md` — the D&D-group chat-UI architecture doc written in S26 and retired in S37 when that framing was replaced by "graph for agent traversal." Both carry STALE SKETCH preambles.
