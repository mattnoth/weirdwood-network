# SESSION 191 — query-layer FINALE: Fable-ORCHESTRATED — the traversal suite + Track close-out

> **This is Session 191.** Stamp your worklog entry `### Session 191` at endsession.
> (If another graph/meta session lands first, renumber — check `worklog.md`.)
> **Matt's steer (S190 endsession, verbatim intent): "go hard on the next section to follow
> this up well" — Fable as ORCHESTRATOR, cheaper agents (Sonnet/Haiku) for the work, advisory
> boards for the forks.** This closes the query-layer Track.

**Recommended model: Fable (ORCHESTRATOR)** — Sonnet builders, Haiku/deterministic scripts for
mechanical verification, Sonnet advisory boards for every genuine fork (the S133 finding:
board orchestration beats model tier). Matt is present and overrules boards on read — his
D-G sign-off points (mini-graph fixture content, op semantics) become board-proposals-he-reads,
not blocking pair-programming; ASK him only at those two checkpoints.

**Track:** graph/meta — the query-layer track, FINAL session.

## Read first (orchestrator only — do not fan this out)
1. `working/query-layer/design.md` — status header (what's done), D-G (the suite spec, step-2
   card), §8 (board decisions incl. the shim-retirement two-tier plan).
2. `worklog.md` Current State + the S190 entry. Trust worklog over this prompt; flag conflicts.
3. `graph/query/README.md` + `graph/query/spec/operations.md` — the contract the suite tests.

## State you inherit
S190 shipped everything except step 2: the engine (zero behavior change), the contract +
golden cases both runtimes (45+, the drift alarm), hardened resolver (17/21 exact), search/
list/theme in the chat (Q11 meals ∞→2 calls), braid, G9 static assets, boards decided,
hygiene 1–4 + mention-index APPLIED (`0408819e20`). Suites: pytest 1322 pass / 3 pre-existing
fails (2× vocab-count 167→now-170 stale assertions + cwd-is-tmp env), deno 98/0/1,
run_cases 37/0/1. **Class-5 dup-slugs = Matt's separate worktree session** — check
`working/query-layer/hygiene-proposal-s190-reconciliation.md` + git log for its landing state
before touching those 7 slug pairs; if it has landed, rebase your reads on its result.

## Mission (bundle, land COMPLETE — no half-finished states)
1. **The mini-graph fixture** (`graph/query/tests/fixtures/mini/`, ~25 nodes/~40 edges):
   causal diamond, ENABLES segment break, SUB_BEAT_OF beats + role edges, 4-generation family
   with deep spine, container bag, ambiguous aliases, plural/possessive resolve case,
   quote-bearing descriptive orphans. **Board-then-Matt:** fan out a small design board for
   the fixture's content/shape (it should be fun + exercise every traversal shape), synthesize
   a proposal, get Matt's read BEFORE building tests on it (D-G checkpoint #1).
2. **The suite** (`graph/query/tests/`, idiomatic pytest — fixtures/parametrize):
   test_resolve / test_traverse (chains, path, participants, beats, containers, family, braid)
   / test_search (search/list/theme) / test_spec_cases (runs `spec/cases/*.json` via pytest —
   the second half of the drift alarm) / test_corpus_smoke (`@pytest.mark.corpus`, real-graph
   pivots: Tywin chain, Aegon family; skips when the graph is absent). Op-semantics sign-off =
   Matt checkpoint #2 (present as a short table, he reads).
3. **Housekeeping:** minimal `pytest.ini` (testpaths `tests/ graph/query/tests/`, `corpus`
   marker); relocate `scripts/stage4-formalize-edges-test.py` → `tests/test_stage4_formalize_edges.py`;
   fix the 2 stale vocab-count assertions (167→170, todos § Small Fixes — pytest goes fully
   green except the environmental cwd-is-tmp; ask Matt's nod, it's a 2-char fix he already queued).
4. **Shim retirement Tier B** (board plan, design.md §8) — IF Matt confirms in-session:
   migrate the 89 shim-loaded tests off `tests/_helpers.load_script` to package imports,
   repoint `backfill-epithet-aliases.py`'s one import, Tier-A doc sweep (~6 files to the
   `weirwood query` spelling), then delete the 3 shims. Run a fresh-verify subagent over the
   migration diff (nothing silently dropped).
5. **Track close-out:** deliberately break one golden case → BOTH runners fail (drift alarm
   re-proven over the finished layer) → restore; design.md status header → TRACK COMPLETE;
   `GRAPH-QUERY-ROADMAP.md` + `GRAPH-STATE.md` pointer banners updated; worklog S191 + fresh
   continue-prompt state (probably NO live query-layer prompt after this — the Track ends;
   what remains is Matt-gated: 8d SERVED_AT + prod deploy).

## Orchestration notes
- Parallel-safe fan-out: fixture-board ∥ housekeeping (3) ∥ Tier-A doc sweep; the suite (2)
  serializes behind the fixture; Tier B behind the suite. Boards for any fork that surfaces.
- Paste the canonical vocabulary into every subagent prompt: **Pass** = numbered corpus sweep;
  **Track** = named work chunk; lowercase **step** = ordered piece of a Track; **Tier** =
  confidence 1–5 ONLY. Paste the relevant DO-NOTs below too (subagents don't load CLAUDE.md).

## Hard gates
No `graph/nodes|edges|index` mutation without Matt's go (the mini-graph FIXTURE lives under
`graph/query/tests/fixtures/` — that's code/test data, not the graph; fine). No 8d pass. No
prod deploy (manual per `DEPLOY.md`; the S190 chat build is still awaiting Matt's deploy).
`sources/` read-only; never fetch the wiki; don't touch `scr`; don't run /endsession without
Matt's permission. BEWARE the rate-limit ceiling — be prepared to continue after reset.
