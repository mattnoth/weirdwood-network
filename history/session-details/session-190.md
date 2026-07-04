---
session: 190
date: 2026-07-04
track: graph/meta (query-layer)
model: Fable 5 (orchestrator) + Sonnet 4.6 subagents (~15) — Haiku-verify slots replaced by deterministic diff scripts
api_spend: none (live-model eval columns stayed gated/empty)
---

# Session 190 — The query-layer orchestrated build (A + B + C in one sitting)

The largest single session of the project to date: the S189 master design's three orchestrated
bundles all executed in one rolled session, exactly as the S189c handoff intended ("as far as
context sensibly allows"). Context never forced a stop; every bundle landed complete and
verified. Nine commits (`adae223e00` → `0408819e20`) plus the endsession docs commit.

## Orchestration shape (what actually worked)

- Fable held the contract; ~15 Sonnet subagents did every heavy read/build; verification was
  split between **deterministic scripts** (the 36-case CLI baseline diff — byte-level, no model
  needed; the design had budgeted Haiku for this) and **independent fresh-verify subagents**
  (semantics-level, e.g. the familyTree port).
- The baseline-first discipline paid off twice: the 36-case old-CLI capture (taken before any
  code existed) made "zero behavior change" a checkable fact, and the frozen eval baseline made
  every retrieval claim a number ("Q11: ∞ → 2 tool calls" instead of "search works now").
- Fresh-verify earned its cost: the familyTree verifier found a missing `isValidSlug` trust
  boundary and a CLI wiring bug (nodes map never passed → prominence silently degraded, wrong
  member set on Aegon I by 6 slugs) that the builder's own checks missed. The hygiene proposer
  found that two S189 census claims **don't reproduce** (28 duplicate edge rows → 0; 91
  dangling edges → 67) and found 3 extra cross-category slug collisions.
- Incidents, all recovered: the shim agent stalled after 6 tool calls waiting on a phantom
  dependency (resumed with a nudge); the step-4 agent's eval `--report` default filename
  clobbered the frozen baseline (git-restored; `--out` made mandatory); the 8a–c agent ran the
  full refresh script and accidentally rebuilt gated `graph/index/` (caught via git status,
  reverted to zero diff before finishing); a variant generator over-generated garbage twice
  before being scoped to short common-noun categories.

## The design's judgment calls that got settled by measurement

- **Search ≠ browse (the 5d fork).** After search shipped, Q11 ("describe some detailed
  meals") was STILL loop-bound — generic aggregative phrasings never BM25-converge to specific
  dish nodes. That settled the deliberately-deferred "does the chat need list/theme tools"
  question: yes. Wiring them flipped Q11 to 2 tool calls. This is the eval harness doing
  exactly what D-I designed it for.
- **G9 by measurement:** narrative-arc inlining would have tripled the bundle (+198%, step-0
  measurement) → per-node static assets (4,401 files, 9.2 MB, `/api/node` fail-soft fetch).
- **No chat tools for path/participants/beats:** no eval row demanded them; recorded as an
  evals-driven overrule of the design's "recommend path yes" (overrule point left open).

## The boards (5, all Sonnet, Matt overruled on read — he approved all)

read_passage → CLI-only (flip = verbatim-text quota + live smoke). SERVED_AT → wait for 8a–c
evidence, settle metric = Q21 (now 2 calls). MCP → parked unanimously. Shims → keep until the
final pytest session migrates the 89 shim-loaded tests. Persona → researcher/wiki-reader frame
per Matt's live steer; **Matt then ruled in-session:** flat register is deliberate ("it's the
base persona, there can be more later"), connections stay tool-grounded, **no A/B eval — deploy
and judge by feel**. Recorded in design.md §8 + memory `chat-persona-decisions`.

## The approved applies (end of session, Matt: "approve all your recs")

Hygiene class 1 (5 YAML-broken alias lines repaired, content unchanged), classes 2–4 =
no-action-as-recommended, class 5 (7 cross-category dup slugs incl. the true collisions
peach/porridge) handed to Matt's separately-spawned dup-slug session (own worktree,
`vigilant-chebyshev`). Mention-index repair applied: `graph/index/chapters/` ← the preview
(181/344 chapters), refresh rollups → 821 entity indexes gained mention data (`crow-cage` 0→2);
7,657 timestamp-only restamps reverted per the S165 rule. Post-apply audit agent: **CLEAN**.

## Honest residue (known, recorded, not hidden)

- 3 of Q11's 5 target dishes sit beyond the theme tool's 25-row page cap (positions 42/55/64
  in the 117-member meals theme) — pagination or theme-rule refinement, someday.
- `acorn-paste` (the design's own motivating stale-index example) is NOT fixed by the mention
  repair — its mention is an un-bulleted Pass-1 prose line, a format gap affecting 2,464 lines
  corpus-wide. Documented in the repair report as out-of-scope.
- Full-profile bare-name fuzzy ("Tywin" via the event-table path) still surfaces the
  assassination event first in `--explain` output; the bounded profile (what users hit) ranks
  `tywin-lannister` correctly. Tracked by the eval instrument, not chased this session.
- The `--explain` provenance gap: the alias table flattens base/variant/victim sources before
  resolve sees them, so explain can't name which source won (documented in operations.md).
- The 2 stale vocab-count test assertions (167 → now 170) remain the known pytest fails
  (todos § Small Fixes) — trivial, could fold into the final session with Matt's nod.

## What remains of the Track

One session: **step 2, the pytest traversal suite, Matt-paired** (mini-graph fixture is his to
co-author; shim-retirement Tier B can ride along). Then the Track closes. Still Matt-gated:
prod deploy of the new chat build (persona/routing/search/list/theme — committed, NOT
deployed), 8d SERVED_AT (trigger = Q21 evidence post-8a–c).
