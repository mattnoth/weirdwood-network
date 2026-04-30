# Worklog Archive 003 — Sessions 8-15

> Archived from `worklog.md` at the end of Session 17 (2026-04-25). Contains the full session log entries for Sessions 8 through 15 (2026-04-24 through 2026-04-25). Loaded only when historical context is needed.

---

### Session 15 — README Continue/Endsession Documentation (2026-04-25)
**Detail:** `working/session-details/session-015.md`
**Changes made:**
- `README.md` — added "Continue Prompts and `/continue`" subsection (explains `progress/continue-prompts/`, both invocations of the slash command, and the `→ continue:` linkage from `todos.md`) and a one-paragraph "`/endsession`" subsection (points at `.claude/commands/endsession.md`)

**Decisions:** Verified `.claude/commands/endsession.md` is clear and current — no changes needed. Documentation-only session; no code, no extractions, no continue prompts created or deleted.

**What's next:**
- Track B unchanged: run `progress/continue-prompts/2026-04-25-track-b-orchestration-planning.md` (PLAN-ONLY), then parser per `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`, then v3 schema review, then collaborator onboarding, then scale v3 to ACOK/ASOS/AFFC/ADWD.

---

### Session 14 — Pipeline-Not-Fixed Note (2026-04-25)
**Detail:** `working/session-details/session-014.md`
**Changes made:**
- `README.md` — added callout under "Extraction Pipeline": Passes 2–6 are a working sketch, not a contract; scope/order/existence open while Pass 1 in progress
- `memory/project_pipeline_not_fixed.md` — NEW project memory (type: project) capturing the same stance with Why + How-to-apply lines for future sessions
- `memory/MEMORY.md` — added index entry for the new memory

**Decisions:** Pipeline flexibility was already implicit in Session 13's "Track B Before v3 Schema Review" rationale; this session generalizes it. Future-pass work should be framed as "current sketch, open to redesign," and Pass 1 gaps should be treated as inputs to redesigning later passes, not as Pass 1 bugs. No new tracks opened, no continue prompts created or deleted, no extractions run.

**What's next:** Fresh session to start Track B — `progress/continue-prompts/2026-04-25-track-b-orchestration-planning.md` (PLAN-ONLY runbook output), then parser implementation per `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`.

### Session 13 — Remote Added, Track B Sequencing, Orchestration Planning, Collaborator Prep (2026-04-25)
**Detail:** `working/session-details/session-013.md`
**Changes made:**
- `git remote add origin https://github.com/mattnoth/weirdwood-network.git`
- `README.md` — added skip-ahead note for users with `sources/raw/`, `sources/chapters/`, `sources/wiki/` already populated
- `worklog.md` — new DECIDED: "Track B (Wiki Parser) Before v3 Schema Review"
- `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md` — prepended "Why Track B Before v3 Schema Review" rationale
- `progress/continue-prompts/2026-04-25-track-b-orchestration-planning.md` — NEW, PLAN-ONLY orchestration design prompt (output: `working/runbooks/wiki-pass2-orchestration.md`)
- `progress/scratch-notes.md` — added 3 entries: "Relational DB Decision — Defer", "Collaborator Onboarding — Schema Lock-In Before Handoff", "Foreshadowing Pass Prep — Expand Event List & Chekhov's Guns"
- `working/todos.md` — orchestration-planning todo (top of Wiki/Pass 2 Prep), parser todo gated on runbook, schema review sequenced-after-Track B; new Collaboration section (schema lock-in, GitHub app revisit, collaborator quick-ref doc); new foreshadowing reference-expansion todo

**Decisions:** Worklog kept at current size (Session Log ~91 lines, under 150 threshold; bulk is persistent context). Track B sequenced before v3 schema review — the wiki parser surfaces schema signals (entity boundaries, edge vocabulary, `cite_ref` reliability, redundancy) that an isolated review cannot. Schema-first risks re-running 272 chapters; Track-B-first costs queued work. **No relational DB** — JSONL + markdown handles current access patterns; Neo4j only relevant when traversal queries become painful (1-2 passes away). Migration cost from JSONL forward is low. **Collaborator onboarding constraint:** schema must be ironclad before handoff (collaborator has less ASOIAF depth, can't lore-check the schema). Pass 4 (foreshadowing) needs expanded event list and Chekhov's gun *pattern library* before running — filed long-lead so it's not forgotten.

**What's next:**
- Next session: run `progress/continue-prompts/2026-04-25-track-b-orchestration-planning.md` (PLAN-ONLY, output runbook)
- Then implement parser per `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`
- Then v3 schema review (informed by Track B output)
- Then schema lock + collaborator onboarding (with collaborator quick-ref doc + GitHub app)
- Then scale v3: ACOK (0/70), ASOS (0/82), AFFC (0/46), ADWD (0/73)

### Session 12 — AGOT v3 Complete, Rate-Limit Detection, Commit Catchup (2026-04-25)
**Detail:** `working/session-details/session-012.md`
**Changes made:**
- `scripts/extract.sh` — rate-limit detection: checks JSON for `status:rejected`, halts wave immediately, marks remaining chapters as `skip-rate-limit`; replaced `tail -3` preview with structured extraction summary; added emoji indicators (✅ ❌ 🚫 ⏭️ 🔄 ⚠️); removed raw JSON dump on failures
- `extractions/mechanical/agot/` — all 73 chapters now v3 complete (26 chapters extracted this session, finishing waves 8, 10, 12-15)
- 3 commits landed: infrastructure (sessions 8-11), extraction tooling, AGOT v3 extractions + archives
- Memory updated: extraction rule strengthened to absolute prohibition on agent-triggered extractions

**Decisions:** Rate-limit detection halts the wave (not the terminal) — stop-file handles cross-wave halting. Emoji in terminal output only, never in extraction content. Structured summary (line count, table rows, events, relationships) replaces raw preview. All historical stat CSVs (v1, v2, v3) kept. One minor schema gap: eddard-01 missing `### Other` header — cosmetic, not blocking.

**What's next:**
- ACOK v3 extraction: `weirwood acok` to see starting point, then `weirwood acok <tabs> <waves>` to run (0/70, user triggers)
- Track B (wiki infobox parser) remains independent: `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`
- Schema review of AGOT v3 output quality (next session)

### Session 11 — Extract.sh Instrumentation: Worklog Auto-Update & Versioned CSV (2026-04-24)
**Detail:** `working/session-details/session-011.md`
**Changes made:**
- `scripts/extract.sh` — stats CSV now per-book versioned (`working/extraction-stats/extraction-stats-{book}-pass1-v3.csv`); new `update_worklog()` function auto-updates `worklog.md` checklist after each wave
- `scripts/extraction-status.sh` — updated to use per-book CSV path
- `working/extraction-stats.csv` — split: v2 rows (Apr 23) back to v2 CSV, v3 rows (Apr 24) to new v3 CSV
- `worklog.md` — updated AGOT v3 progress to 30/73 (was stale at 0/73)

**Decisions:** PASS/VERSION hardcoded at script top (not CLI flags) — prompt version changes are rare and deliberate. Worklog update uses filesystem truth via `is_complete`, not CSV row counts. Stats CSVs versioned per book/pass/version so they archive with their extraction run.

**What's next:**
- Continue AGOT v3 extraction (30/73 done, waves 7-15 remaining)
- Track B (wiki infobox parser) remains independent: `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`

### Session 10 — Prompt Update v3, Archive Prior Extractions, Process Lessons (2026-04-24)
**Detail:** `working/session-details/session-010.md`
**Changes made:**
- `.claude/agents/mechanical-extractor.md` — Raw Entity List expanded to 12 categories (10 named + Other catch-all), added strict formatting rules (all headers required, no merging/renaming, "None" for empty)
- `reference/architecture.md` — Pass 1 schema table updated to reflect 12 categories
- `extractions/archives/agot-v2/` — archived 73 AGOT v2 extractions (4-category format)
- `extractions/archives/acok-v2/` — archived 50 ACOK v2 extractions (4-category format)
- `extractions/mechanical/agot/` and `acok/` — now empty, ready for v3 runs
- `cspell.json` — created project-level cSpell dictionary for ASOIAF terms
- 3 new memory entries (no-extraction-without-asking, check-existing-knowledge-first, knowledge-index-deferred)

**Decisions:** Extractions must go through `weirwood` pipeline only, never background subagents. Raw Entity List locked at 12 categories with strict no-rename/no-merge formatting rules. All prior extractions archived; v3 starts fresh. Trust wiki organization as authority for entity type categories. `Other` catch-all handles edge cases without agent improvisation. Behavioral rules for checking existing knowledge saved; structural index deferred.

**What's next:**
- Run AGOT extraction via `weirwood agot` with v3 prompt (Matt will trigger manually)
- After AGOT v3 validates, run ACOK and remaining books
- Track B (wiki infobox parser) remains independent: `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`

### Session 9 — /continue Command, Todo-Prompt Linking, Session Backfill (2026-04-24)
**Detail:** `working/session-details/session-009.md`
**Changes made:**
- Created `.claude/commands/continue.md` — priority-aware `/continue` slash command
- Updated `working/todos.md` — added `→ continue:` references linking two todo items to their continue prompts
- Updated `.claude/commands/endsession.md` — added depth-scaling guidance for session details, continue prompt lifecycle (create + cleanup), removed handoffs.md references
- Updated `CLAUDE.md` — removed handoffs.md, pass1-agot.md, taxonomy-candidates.md from directory tree
- Created `working/session-details/session-000.md` through `session-007.md` — backfilled all pre-documentation sessions
- Deleted 7 stale files: `progress/handoffs.md`, `progress/pass1-agot.md`, `progress/README.md`, `working/progress.md`, `working/taxonomy-candidates.md`, `working/extraction-stats-agot-pass1-v1.csv`, `scratch`
- Deleted completed continue prompt: `2026-04-24-backfill-session-details.md`

**Decisions:** Todos.md is the priority authority; continue prompts link from todos via `→ continue:` lines (one-directional). handoffs.md retired — redundant with todos + continue prompts. Session detail depth should scale to session type (design = full narrative, execution = decisions + surprises). Endsession owns the continue prompt lifecycle (create new, delete completed).

**What's next:**
- Track A: Update extractor Raw Entity List 4→10 categories, finish ACOK + start ASOS (`progress/continue-prompts/2026-04-24-track-a-extraction-prompt-update.md`)
- Track B: Write wiki infobox parser script, design Pass 2 (`progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`)

### Session 8 — Architecture Refactor, Edge/Entity Taxonomy, Wiki Discovery (2026-04-24)

**Detail:** `working/session-details/session-008.md`

**Changes made:**
- `reference/architecture.md` → pure agent schema reference (removed directory tree, current state, project overview)
- Entity types: flat list → hierarchical taxonomy with inheritance (18 leaf types across 8 parent categories)
- Edge types: 26 → ~80 across 14 categories (normalized from v1's 127 ad-hoc types + wiki infobox fields)
- Edge taxonomy is for graph layer only — Pass 1 stays free-text
- Wiki `cite_ref` anchors discovered: `R{book}{chapter}` encoding gives chapter-level `first_available`
- Wiki infobox → edge type mapping table added to architecture.md
- CLAUDE.md: pipeline status updated, directory tree refreshed
- Coverage analysis: Raw Entity List has 4 categories, needs 10. Magic/Species/War severely under-indexed.
- ACOK confirmed at 50/70 (same prompt gap as AGOT)

**Decisions:** architecture.md is agent-only; `house` is its own type under Organization; AGOT/ACOK don't need re-runs (supplementary index instead); prompt update before any further extraction; wiki confidence-tier mapping is a Pass 2 problem; two independent work tracks (A: extraction, B: wiki/Pass 2).

**What's next:**
- **Track A** (continue prompt: `progress/continue-prompts/2026-04-24-track-a-extraction-prompt-update.md`): Update extractor Raw Entity List 4→10 categories, then finish ACOK + start ASOS
- **Track B** (continue prompt: `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`): Write wiki infobox parser script, then design Pass 2
- Tracks converge at graph building
