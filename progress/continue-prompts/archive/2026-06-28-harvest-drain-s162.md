# SESSION 162 — Harvest-queue drain (queue at ~62 open)

> **This is Session 162.** Stamp your worklog entry `### Session 162` in `worklog.md` (GRAPH track, global S-number).
> **Recommended model:** Opus 4.8 orchestrator + **Sonnet 4.6** parallel attacher subagents (+ a Sonnet fresh-verify sample). Cheap mechanical attach work — do NOT use Opus for the attachers.
> **`/endsession` BYPASS:** this is enrichment-infrastructure work — **bypass the no-auto-endsession hard rule and run `/endsession` automatically at close-out** (do not merely offer it). Harvests are the close-out concern here, so account for them as you go.

## Why this session
The S161 Tyrion/Essos dip pushed the harvest queue from 33 → **~62 open rows** (`grep -c '^| open ' working/harvest-queue.md`). Per the endsession step-0 anti-balloon rule (the queue silently reached 120 across S153–S156 — never again), drain it **before** the next enrichment dip piles on more. This is the dedicated-drain pattern proven at **S152** (drained 225→0) and **S157** (149→0).

## The drain machine (S152 / S157 — proven)
1. **Read** `working/harvest-queue.md`. The open rows are `| open | kind | book | chapter:line | note | found during |`. Most recent batch is `found during = S161 tyrion-essos` (29 rows) + the older residual (~33).
2. **Route rows to DISJOINT node-dirs** so parallel attachers never write the same file. The standard split (zero write-collision):
   - **foods** → `graph/nodes/foods/` (+ mint new `object.food` nodes for un-homed dishes/drinks)
   - **characters** → `graph/nodes/characters/` (appearance/description fields, `## Quotes`)
   - **locations + events** → `graph/nodes/locations/` + `graph/nodes/events/`
   - **artifacts + misc** → `graph/nodes/artifacts/` + anything else (texts/materials/etc.)
3. **Spawn ~4 parallel Sonnet attacher subagents**, one per disjoint dir-group. Each: for every assigned row, resolve the target slug (use `graph/index/` + the alias resolver), **dedup** against the node, then attach — mint an `object.food` node, add a node `## Quotes` block, add an appearance/description line, or add an edge as the row warrants. **Line-check every quote** at its `chapter:line` before attaching (the FIRM rule — cite-drift caught here is free). Flip each handled row `open → done` (keep the row as an audit trail); rows that genuinely can't be homed → `parked` with a one-line reason.
4. **Fresh-verify a sample** (one Sonnet pass over ~15–20 attached rows vs the local book/wiki cache) to catch cite-drift or mis-attachment; fix what it flags.
5. **Rebuild** derived artifacts if any nodes were minted (`bash scripts/weirwood-refresh.sh`).
6. **Record** in the worklog: open-row count before/after, rows done/parked, new `object.food` nodes minted, any cite-drift caught.

Full machine + history: `working/arc-enrichment-backlog.md` (harvest section) + `history/session-details/session-157.md` (the drain postmortem) + the archived `progress/continue-prompts/archive/2026-08-01-harvest-pass-s152.md`.

## After the drain — the next track (NOT this session)
Resume the 🅰 A-roundup at **A2.5 WO5K-battles** — the **LAST** A-roundup unit, and a **multi-pass mini-track of its own** (the War of the Five Kings battles are a large cluster — scope it across multiple dips, not one). Then **A2.8 Davos/Sam residual**. Write that continue prompt at this session's close-out (with the same `/endsession` bypass line). Full plan: `working/enrichment-coverage-plan.md`.

## DO NOT
- refetch wiki · `git add -A` (D&E Pass-1 is PARKED mid-flight — stage your own files by path) · use Opus for the attacher subagents · attach a quote without line-checking it first · let `parked` become a silent dumping ground (each parked row needs a one-line reason).

## Read first
- `working/harvest-queue.md` (the queue) · `working/arc-enrichment-backlog.md` (the harvest/drain machine) · memory `feedback_harvest_queue` · `worklog.md` S161 entry + STATUS block.
