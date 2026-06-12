# Canonical Design Document Proposal — 2026-06-11 (Step 1d)

> Goal (Matt, verbatim intent): a new contributor, a fresh agent, or Matt after two weeks away reads
> the design doc(s) and understands what this system IS and WHY — without archaeology.
> This file = inventory + proposal. Matt picks; the consolidation build happens in a later session.

## 1. Inventory — where design intent lives today

~28 design-ish documents found. **8 are current design, ~12 are stale/superseded design, the rest are
records or procedures.** Legend: **D**=design (why/what), **R**=runbook (how-to), **REC**=record (decision log).

| File | Holds | Kind | Freshness |
|---|---|---|---|
| `reference/architecture.md` (668 ln) | Data model: types, ~96+ edge types, tiers, naming, frontmatter, Pass-1 schema | D | **Current** (Jun 8). The anchor doc. |
| `reference/design-philosophy.md` (133 ln) | The WHY: Unix philosophy, anti-patterns, worse-is-better | D | Current; low churn; canonical-quality already |
| `reference/edge-qualifier-vocab.md` (60 ln) | Qualifier enums, 3-tier rules (S57 lock) | D | Current spec annex to architecture |
| `reference/agents.md` (127 ln) | Agent inventory + hard rules | D/REC | **Partially stale** ("ACOK…pending"; Stage-4 framing pre-pivot) |
| `reference/pass-1-mechanical-extraction.md` (196 ln) | Pass-1 design + rationale | D | Current (pass done; doc accurate) |
| `reference/alias-resolver-design.md` (148 ln) | S86 alias/display decisions, unimplemented | D | Current, queued work |
| `reference/model-strategy.md` (65 ln) | Model-per-task costing | D | **Stale-ish** (pre-Haiku rules, pre-`claude -p` discovery) |
| `reference/extraction-commands.md`, `package-install-policy.md`, `foreshadowing-events.md`, `pov-characters.md` | Procedures / data references | R | Current; feeders, not design |
| `working/edge-modeling/edge-modeling-reification-design.md` (553 ln) | **Canonical edge strategy**: D1–D8 decisions, glossary, plates | D+REC | Current design, but plates 0–5 executed — half is spent session-prompt scaffolding |
| `working/edge-modeling/post-plate5-backfill-design.md` (224 ln) | Tracks A/B/C backfill | D | Current, planned work |
| `working/edge-modeling/SESSION-LOG.md` + plate summaries/diffs | Execution records | REC | Records; never edited |
| `working/stage4-pass1-derived-edges-design.md` (70 ln) | S65 pivot rationale; provenance story for book-pass1 spine | D | Superseded by execution; rationale still load-bearing |
| `working/agent-fleet-specs/agent-pipeline-plan.md` (192 ln) | 24-agent fleet | D | **Stale — never executed** |
| `working/agent-fleet-specs/fleet-orchestration-plan.md` (412 ln) | Fleet concurrency/budgets | D | **Stale — never executed** |
| `working/agent-fleet-specs/fleet-runtime-architecture.md` (624 ln) | Fleet daemon runtime | D | **Stale — never executed; daemon deferred** |
| `working/agent-fleet-specs/mission-protocol.md` (294 ln) | Missions-vs-sessions, watcher | D | **Dormant since ~S48**, draft v0 |
| `working/agent-fleet-specs/stage4-vocab-lock-*.md`, `working/qualifier-vocab/decisions.md` + plan/audit | Vocab-lock decision trail | REC | Done; encoded into edge-qualifier-vocab.md |
| `working/runbooks/wiki-pass2-orchestration.md` (709 ln) | **Disguised design doc**: decomposition theory, concurrency model, drift prevention — for a completed run | D+R | Design content current as *doctrine*, run is done |
| `working/runbooks/wiki-pass2-pipeline.md` (229 ln) | Stage-3 Python pipeline (canonical example of the philosophy) | D+R | Current; pipeline shipped |
| `working/runbooks/edge-modeling-audit-loop.md` (89 ln) | Reporter/auditor loop | R | Current, live discipline |
| `working/runbooks/` others (mechanical-extraction-howto, pass1-auto-advance, stage4-events-haiku-bulk, general-watcher, 2 `-DONE` files) | Procedures | R | Done/NO-GO'd/dormant — stale to varying degrees |
| `working/tier3-promotion-plan.md`, `edge-vocabulary-gaps.md` | Old plans/logs | REC | Stale/empty |
| `history/archive/` (stage3b-design-review, sketches/chat-ui-architecture, diagrams) | Retired sketches | REC | Already retired — no action |

Not design but load-bearing context: `CLAUDE.md` (orchestration), `worklog.md` (state), `working/todos.md`
(queue), `history/` (records). These *point at* the canonical set; they don't compete with it.

**The core problem in one line:** the WHAT (architecture.md) is canonical and healthy, but the WHY-and-HOW-IT-FITS
(pipeline history, edge strategy, destination features) lives in 5 working/ docs, 3 dead fleet specs, a
709-line runbook, and 91 worklog sessions.

## 2. Candidate structures

### Option A — `reference/design/` set of four + philosophy (RECOMMENDED)

Canonical set (everything else feeds these or points at them):

1. **`reference/architecture.md`** — data model spec. **Stays exactly where it is** (rule 6 sync contract,
   dozens of inbound references from agents/CLAUDE.md/memory). No move, no rewrite.
2. **`reference/design/pipeline.md`** (~250 ln, new) — the system's production story: Pass 1 → wiki cache →
   Pass 2 stages → Stage-4 pivot → reification plates → infobox merge → Modes/passes 3–6 planned. One section
   per stage: what it is, WHY it's shaped that way, status tag (`shipped / live / planned / deprecated / retired-unexecuted`),
   pointer to its runbook/record. Absorbs: stage4-pass1-derived-edges-design, model-strategy, pass-1 doc's
   rationale, fleet-plan disposition (one honest paragraph: designed S22-26, never executed, retired).
3. **`reference/design/edge-strategy.md`** (~250 ln, new) — the reification + provenance story: the five edge
   layers (book-pass1 spine, LLM tail, reified events, hospitality, infobox Tier-2), "a wrong cited edge is
   graph pollution," tier semantics, lockdown/validation stack, D1–D8 decisions distilled, comention saga in
   five lines, backfill Tracks A/B/C. Absorbs: edge-modeling-reification-design (decision content, not spent
   plate prompts), post-plate5-backfill-design.
4. **`reference/design/features.md`** (~150 ln, new) — what this is FOR: graph-for-agent-traversal goal,
   dialog/Mode-3, query shapes, spoiler-gating deferral, theories/prophecies gap, curation flow
   (agents propose, Matt decides). **The Step-3b destination-features outline being written tonight is the
   seed of this file.**
5. **`reference/design-philosophy.md`** — stays as-is (already canonical, low churn). The WHY behind 2–4.

Feeders: `agents.md` (refreshed, points into pipeline.md), runbooks (HOW-TO only; design sections of
wiki-pass2-orchestration distilled into pipeline.md), worklog (state), records in `history/`.

**Trade-offs:** selective load — an edge session loads architecture + edge-strategy (~900 ln), never pays for
features/pipeline; rule-6 sync burden stays confined to architecture.md; each canonical doc has one topic =
one writer per consolidation session (single-writer invariant). Cost: 4 files to keep honest instead of 1,
and a one-line "canonical set" map needed in CLAUDE.md.

### Option B — single `DESIGN.md` with chapters

One ~1,200–1,500-line file: Vision / Data model pointer / Pipeline / Edge strategy / Features. Zero ambiguity
about where design lives; trivially discoverable. **Costs:** every design-touching session loads all of it
(~15–20k tokens vs ~5k for one Option-A file); two parallel sessions can't both update it (single-writer);
architecture.md still has to live outside it (rule 6), so it's never truly "one document" anyway.

### Option C — minimal: architecture.md + one `reference/SYSTEM-DESIGN.md`

Two canonical docs; SYSTEM-DESIGN.md covers pipeline+edges+features in compressed form (~500 ln). Cheapest
to build (~2 sessions) and to load. **Costs:** compression loses the WHY (the thing Matt is missing today);
edge strategy alone has D1–D8 + five provenance layers — at ~150 lines it becomes a pointer farm back into
working/, which is the archaeology problem restated.

**Recommendation: Option A.** It matches how sessions actually load context (selective), respects rule 6
without contortion, and each file is small enough to stay honest. B is the fallback if Matt prefers
one-file discoverability over token cost.

## 3. Disposition table (Option A) — every inventoried doc

| Doc | Disposition |
|---|---|
| `reference/architecture.md` | **Canonical #1** — unchanged, stays put |
| `reference/design-philosophy.md` | **Canonical #5** — unchanged |
| `reference/edge-qualifier-vocab.md` | Stays — spec annex, linked from architecture + edge-strategy |
| `reference/agents.md` | Feeder — refreshed (fix stale Pass-1/Stage-4 claims), points to pipeline.md |
| `reference/pass-1-mechanical-extraction.md` | Rationale absorbed into pipeline.md → file becomes pass spec pointer (or stays as detailed annex; cheap either way) |
| `reference/alias-resolver-design.md` | Absorbed into edge-strategy.md §display/aliases once implemented; until then stays, linked as "queued design" |
| `reference/model-strategy.md` | Absorbed into pipeline.md (one model-policy section, updated) → retired to history/ with stale tag |
| `reference/extraction-commands.md`, `package-install-policy.md`, `foreshadowing-events.md`, `pov-characters.md` | Stay — runbook/data feeders |
| `working/edge-modeling/edge-modeling-reification-design.md` | Decision content absorbed into edge-strategy.md → file gets superseded-stamp header pointing there, moves to history/archive/ |
| `working/edge-modeling/post-plate5-backfill-design.md` | Absorbed into edge-strategy.md §backfill → stamp + retire when tracks ship (live until then) |
| `working/edge-modeling/SESSION-LOG.md`, plate reports, merge diffs | Records — never edited; folder eventually archived wholesale |
| `working/stage4-pass1-derived-edges-design.md` | Absorbed (pivot rationale) into pipeline.md → retired to history/ with stale tag |
| `working/agent-fleet-specs/` all four design docs | **Retired-unexecuted** → history/archive/ with stale-tag preamble; pipeline.md carries the one-paragraph honest summary. Mission-protocol noted as dormant draft, revivable |
| `working/agent-fleet-specs/stage4-vocab-lock*`, `working/qualifier-vocab/*` | Records → archive wholesale; edge-qualifier-vocab.md is the living spec |
| `working/runbooks/wiki-pass2-orchestration.md` | Design doctrine (decomposition/concurrency/drift) distilled into pipeline.md; file stays as historical runbook with pointer header |
| `working/runbooks/wiki-pass2-pipeline.md`, `edge-modeling-audit-loop.md`, `mechanical-extraction-howto.md` | Stay as runbooks (HOW-TO feeders) |
| `working/runbooks/` stale ones (stage4-events-haiku-bulk, general-watcher, pass1-auto-advance, `-DONE` files) | Stamp DONE/NO-GO header → runbooks/archive/ |
| `working/tier3-promotion-plan.md`, `edge-vocabulary-gaps.md` | Stale-tag → history/ |
| `history/archive/` sketches (chat-ui, stage3b review, diagrams) | Already retired — no action |
| `CLAUDE.md` | Gains a 5-line "Canonical design set" map; pipeline-status table fixed (already on punch list) |

## 4. Build estimate

| Session | Work | Effort |
|---|---|---|
| 1 | `edge-strategy.md` (richest source material: reification design + post-plate5 + provenance layers) | 1 subagent session |
| 2 | `pipeline.md` (synthesis across worklog/history-audit/runbooks — history-audit.md §A already did the archaeology) | 1 subagent session |
| 3 | `features.md` seeded from tonight's Step-3b outline + goal memory | 0.5 session |
| 4 | Disposition sweep: stamps, moves to history/, pointer headers, agents.md refresh, CLAUDE.md map | 0.5–1 session (mostly mechanical) |

**Total: ~3–4 focused subagent sessions** (realistically two orchestrator evenings). The fable-audit folder
(history-audit, graph-deep-dive, synthesis) is the pre-digested source for most of it — build soon while it's fresh.
