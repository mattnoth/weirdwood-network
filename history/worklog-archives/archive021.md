# Worklog Archive 021 — Sessions 97–

> Archived from `worklog.md` per CLAUDE.md rule #8 (5 entries per archive file). Newest-first within the file follows the worklog convention. Session 97 archived 2026-06-16 (Session 102 endsession).

### Session 97 — Historical-anchor #9 wave 1 SHIPPED + Orchestration/Pacer design doc (2026-06-15)
**Detail:** `history/session-details/session-097.md`
**Model:** Opus 4.8 orchestrator + Sonnet 4.6 subagents (8 historical-anchor research + 1 sequencing advisor + 1 design reviewer). **Commit:** uncommitted at endsession (Matt to decide).

**Changes made:**
- `graph/edges/edges.jsonl` **21,829 → 21,950 (+121)**: historical-anchor #9 wave 1 (+118 across 8 isolated R+L=J/Robert's-Rebellion hubs) + 3 Trident COMMANDS_IN (Robert/Rhaegar/Lewyn). Hubs: `tourney-at-harrenhal` 0→25, `the-hands-tourney` 0→33, `battle-of-the-trident` 2→16, `sack-of-kings-landing`, `combat-at-the-tower-of-joy`, `greyjoy-rebellion`, `defiance-of-duskendale`, `tragedy-at-summerhall`. **NEW evidence_kind `wiki-historical-anchor`** (Tier-2 max; 19 edges). Backups in `_regrounding/`.
- NEW scripts: `scripts/historical-anchor-{candidates,validate,mint}.py` + `working/historical-anchor/SPEC.md` + per-hub candidate/notes files. NEW `tests/test_longrun_supervisor.py` (6 tests, longrun exit-10/2/0/crash/resume verified).
- NEW `working/orchestration-pacer-design-2026-06-15.md` — design doc (supervisor/worker/pacer architecture, exit-code contract, telemetry ledger, §1.5 script taxonomy A/B/C/D, §11 Script Org Standard, §13 review amendments, §14 two-session scope). Fresh-reviewed.
- NEW memory `project_rebuild_derived_artifacts_after_node_mutation` (+ MEMORY.md index). NEW continue prompts: `2026-06-15-historical-anchor-wave2.md`, `2026-06-15-script-consolidation.md` (2-session split).
- `worklog.md` (this entry; S92 archived → `archive020.md`), `working/todos.md` (#9 wave1 done, script-consolidation pointer), `working/historical-anchor/`.

**Decisions:**
- **Pivoted from the queued arc-mint to followup #9** (fresh advisor + worklog order both said #9-first; arc mint maps to 0 dip questions). **Arc wave-1 mint stays drafted-but-unminted, still gated on Matt's 3 decisions** (RW-4 role edges / arc boundaries / RECIPIENT_IN). #9 method: curate the main-saga-recalled cluster (the ~300 deep-lore hubs are wiki-only, out of scope), per-hub Sonnet subagent → JSON attach edges → 2-stage verbatim validation → curator drop/fix (6 dropped, 4 fixed). Provenance: book-pass1 tier-1/2 earned by chapter quote; wiki-only → `wiki-historical-anchor` tier-2 max.
- **Script consolidation = design-doc-first** (Matt). Architecture: bash `longrun.sh` wraps a resumable Python worker (emits 0/2/10) + a Python `pace.py` pacer mining past run-stats; `weirwood` CLI front door; per-worker JSONL telemetry (fixes the real CSV-append race). Review found 4 must-fix spec gaps (positive wall-detect-or-crash; atomic state writes; honest thin wall-cadence backfill; shared next-eligible for concurrency → v1 single-worker). **Honest scope = TWO sessions** (pacer, then cleanup).
- **TWOIAF (6th source, on disk unextracted) + F&B (7th, not on disk) backlogged**; use wiki for deep-lore hubs now.

**What's next:**
- → **Script consolidation Session 1 (orchestration/pacer)** — `progress/continue-prompts/2026-06-15-script-consolidation.md` (Sonnet 4.6). Recommended next.
- → historical-anchor #9 wave 2 — `progress/continue-prompts/2026-06-15-historical-anchor-wave2.md` (Sonnet 4.6).
- → narrative-arc wave 1 mint — `progress/continue-prompts/2026-06-15-arc-wave1-mint.md` (Sonnet 4.6) — **GATED on Matt's 3 decisions**.
