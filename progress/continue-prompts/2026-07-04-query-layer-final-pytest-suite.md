# QUERY-LAYER FINAL SESSION — step 2: the pytest traversal suite (MATT-PAIRED)

> **Next graph/meta session number: check `worklog.md` (S191+).** This is the LAST session of
> the query-layer Track. **PAIR WITH MATT** — the mini-graph fixture content and op-semantics
> sign-off are explicitly his (D-G); do not run this session headless.

**Recommended model: Sonnet 4.6** (idiomatic pytest work; Matt drives fixture/semantics
decisions). No Opus/Fable needed — the design record already holds the judgment calls.

**Track:** graph/meta — the query-layer track (design: `working/query-layer/design.md`,
status header says what's done; worklog S190 = the build record).

## State you inherit (trust worklog.md over this if they disagree — flag contradictions)
- Sessions A+B+C are DONE (S190): `graph/query/` engine live, zero behavior change verified;
  resolver hardened; search/list/theme in both runtimes + the chat; parity table closed;
  braid live; boards decided (design.md §8). All suites green: pytest 1322 pass / 3
  pre-existing documented fails (2× vocab-count 167→170 stale assertions + cwd-is-tmp env),
  deno 98+/0, `run_cases.py` 37+/0/1.
- Golden spec cases (`graph/query/spec/cases/*.json`) carry drift protection already — this
  session builds the DEEP suite on top, not the first net.

## The work (design.md D-G + step-2 card — read them first)
1. **Synthetic mini-graph** `graph/query/tests/fixtures/mini/` (~25 nodes/~40 edges): causal
   diamond, ENABLES segment break, SUB_BEAT_OF beats + role edges, 4-generation family with a
   deep spine, container bag, ambiguous aliases, plural/possessive resolve case, quote-bearing
   descriptive orphans. **Matt co-authors the content — it should be fun.**
2. `graph/query/tests/` — idiomatic pytest (fixtures/parametrize): test_resolve / test_traverse
   / test_search / test_spec_cases (runs the golden cases via pytest — the second half of the
   D-B drift alarm) / test_corpus_smoke (`@pytest.mark.corpus`, skips without the live graph).
3. Repo housekeeping: minimal `pytest.ini` (testpaths `tests/ graph/query/tests/`, `corpus`
   marker); relocate the orphaned `scripts/stage4-formalize-edges-test.py` →
   `tests/test_stage4_formalize_edges.py`.
4. **Shim-retirement Tier B rides here IF Matt wants it** (board plan, design.md §8): migrate
   the 89 shim-loaded tests off `tests/_helpers.load_script` to package imports, repoint
   `backfill-epithet-aliases.py`'s one import, Tier-A doc sweep, then delete the 3 shims.
   Matt's call whether this session or later.
5. Exit: `pytest graph/query/tests` green; one golden case deliberately broken → BOTH runners
   fail (drift alarm re-proven); full suite tallies recorded in the worklog entry.

## Matt-gated items that do NOT run unless he says so (prose, deliberately not fenced)
The hygiene apply (`working/query-layer/hygiene-proposal-s190.md` — per-class checkboxes,
incl. the peach/porridge true-collision renames), the mention-index repair apply (command in
`working/query-layer/mention-index-repair-report.md`), the 8d SERVED_AT pass (trigger = Q21
evidence per the board), any prod deploy (the researcher-persona + routing + new-tools build
is committed but NOT deployed — Matt reviews `web/netlify/edge-functions/lib/agent.ts` and
deploys manually per `DEPLOY.md`), and the 2 stale vocab-count test assertions (167→170,
todos § Small Fixes — trivial, could fold in here with Matt's nod).

## Standing rules
`sources/` read-only; never fetch the wiki; no graph/nodes|edges|index writes without Matt's
go; one live continue prompt; paste Pass/Track/step/Tier vocabulary into subagent prompts;
don't run /endsession without Matt's permission. At close: worklog entry, archive this prompt,
design.md status header flips to TRACK COMPLETE, commit.
