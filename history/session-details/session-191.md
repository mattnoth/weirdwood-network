---
session: 191
date: 2026-07-04
track: graph/meta (query-layer Track, FINAL session) + chat-UI deploy
model: Fable 5 (orchestrator) + Sonnet subagents (3-lens fixture board, Tier-A doc sweep, fixture builder, suite builder)
api_spend: ~$0.03 live verification turn (Opus, post-deploy) + subagent tokens
---

# Session 191 — The query-layer finale: traversal suite, shim retirement, and the deploy

## Shape of the session

The S190 handoff scripted this as a Fable-ORCHESTRATED finale: boards for every fork,
Sonnet builders, Matt overruling on read at exactly two D-G checkpoints. That's how it
ran — until the monthly spend limit killed the last subagent mid-report and the
orchestrator finished solo. Mid-session, Matt queued a priority steer (tool logging +
deploy readiness first, side-window rendering after), which folded in cleanly, and by
session end he had asked for — and gotten — the actual production deploy, making this
both the Track's close and the chat-UI's biggest live update since S183.

## The fixture board (checkpoint #1)

Three Sonnet lenses ran in parallel on the mini-graph fixture design:

- **Coverage engineer** — the load-bearing catches: `family_tree()` reads `SPOUSE_OF`
  (the step card said "MARRIED", which isn't in the vocabulary — dead edges averted), and
  `event_participants` vs `--expand-beats` use DIFFERENT role-edge sets
  (`PARTICIPANT_ROLE_TYPES` has ATTENDS/LOCATED_AT but not WITNESS_IN;
  `ROLE_EDGE_TYPES` the reverse). The fixture deliberately straddles both sets so the
  divergence is pinned, not papered over.
- **Storyteller** — "The Salt Debt": House Quorwyn, eel-tax hubris, the shared "Eel King"
  nickname (gen-2 Myrcella's joke title curdling into gen-4 Ormund's insult = the
  ambiguous alias with an in-story REASON), and the orphan food nodes with real comedy
  value (Lord Quorwyn's good boot — the left one).
- **Adversarial tester** — 18 code-cited traps (cycle termination semantics, self-loop
  double-count in neighbors, dangling-hub fail-fast vs beats-no-roles fail-soft,
  remarriage bond dedup, deep-spine boundary isolation) plus the session's security find:
  `find_node_file()` walks `..` on `.exists()` and only `family_tree` validates slugs.

Synthesis took the storyteller's saga on the coverage engineer's skeleton with the
adversarial traps quarantined in story-shaped corners (the eel-market feud literally goes
in causal circles; Maester Crell's lost chronicle is the dangling target). 35 nodes/39
edges vs the card's ~25/~40 — Matt approved the overage as proposed, plus the path-escape
guard, plus full Tier B.

**Guard nuance:** a strict `_is_valid_slug` guard in `find_node_file` would have BROKEN
247 real node files whose slugs carry uppercase timestamp suffixes
(`…-2026-05-01T20-34-52`, a Pass-2 artifact). The landed guard blocks only
path-dangerous input (`/`, `\`, `..`) — zero behavior change for on-disk slugs.

## Checkpoint #2 and the suite

The op-semantics table (`working/query-layer/boards/op-semantics-s191.md`) froze one line
per op — all recorded spec, nothing new. Matt froze it as tabled. The suite builder
(Sonnet) wrote 104 tests over the fixture (18 resolve / 35 traverse / 9 braid / 38
spec-cases-as-pytest / 4 corpus smoke) — and hit the MONTHLY SPEND LIMIT at its
final-report step. Its files had all landed and passed; only the report was lost.
Later in the session (post-limit), the agent was resumed from its transcript and
delivered the report: **zero fixture-data edits** (the one unreconstructable fact),
zero pinned engine bugs, and two documented deviations — the ENABLES-divergence
assertion belongs on `salt-debt-massacre` (not the battle), and the deep-spine test
roots at Quor (Tomm must be depth 5). Its report also surfaced that
**braid(node, its-own-descendant) is NOT all-empty** — `shared_ancestors` carries the
common upstream cone — which corrected a shorthand line in the frozen table (amended,
`cfebd60969`).

One collateral: the suite builder's `graph/query/tests/__init__.py` made that directory a
second top-level `tests` package and broke ALL legacy-suite collection (29 errors).
Deleted — pytest needs no `__init__.py` there, and basenames don't collide.

## The drift-alarm re-proof earned its keep

Breaking `resolve-red-wedding-exact` (slug → `purple-wedding`) failed the deno runner but
PASSED both Python runners. Root cause: `run_cases.py`'s resolve handler only compared
`expect.top.slug`, never `expect.candidates[0].slug` — for that case shape, the Python
half of the alarm was a no-op. Fixed (the slug is profile-independent even though the
status enums aren't); after the fix all three runners fail on the break and pass on
restore. The re-proof step existed precisely to catch this class of hole.

## Tier B (shim retirement)

All three board conditions met in-session, so: the 89 shim-loaded tests migrated to
package imports (`test_graph_query_edges` got a tiny `_GQ` namespace recomposing the
shim's compute+print glue; `test_event_alias_resolver` a SimpleNamespace over
package + builder symbols — test bodies untouched, count parity 39+9+41 proven vs HEAD);
`backfill-epithet-aliases.py` repointed; `weirwood graph`/`resolve` became permanent
short aliases over the engine; READMEs updated; the 3 shims deleted. The fresh-verify
subagent was impossible (spend cap), replaced by deterministic checks: test-count parity
vs HEAD, zero remaining `load_script` references, full suite green.

## Matt's priority steer: logging + deploy

His queued questions: (1) does logging capture the new tools? (2) what does the "chain
walked" window show for them? Answers: toolTrace already recorded every call's
name+input, and S190's `outcome` slice covered resolve/search/list/theme — but full
result capture for review was missing. Extended `outcomeFor()` to EVERY tool
(matchType/topSlug/resultCount + first-10 `slugs` for the row-returning tools). The
receipts rail: `app.js ingestReceipt` has no case for search_quotes/list_nodes/theme —
those receipts silently drop (data reaches the browser; rendering is the gap). Deferred
by Matt: deploy first, side-window after.

**The real deploy gap found:** `netlify.toml`'s build command only ran the core bundle
builder, but `web/src/lib/data.ts` imports `search-index.json` + `theme-index.json` at
build time — the new tools deployed whatever sat on local disk (works by accident,
breaks on a clean checkout). The build command now runs all three `graph/query/build/`
builders; verified end-to-end locally.

## The deploy (Matt: "Can you run those commands for me?")

Pushed, deployed (1m 4s build, 4,400 assets), then the DEPLOY.md verification turn —
deliberately the S188 killer question class: "What meals are served in the books? Name
two." **3 tool calls (`theme → read_node → read_node`), $0.0324, zero unverified cites**,
a genuinely good answer (bowl of brown vs. Illyrio's black cherries — opposite ends of
the social scale). The raw blob confirmed model `claude-opus-4-8` and the new outcome
slices, including the theme call's 10-slug inventory. The ∞-loop failure mode is dead in
production.

## Incidents & notes

- **Monthly spend limit** hit mid-session (killed the suite builder's report; blocked all
  further subagent fan-out). Orchestrator finished Tier B + close-out solo. Next session
  should assume limited or no fan-out until the limit resets.
- **Class-5 dup-slugs still un-landed** — Matt's `vigilant-chebyshev` worktree session has
  no commit; the reconciliation file sits untracked. The live bundle still serves the
  alphabetically-later copy for colliding slugs (e.g. food `porridge` over the gaoler).
- Fixture data quirk (test-data only): two alias keys stored with a literal leading
  "the" are unreachable via normal queries (normalize strips one leading article).
- The vocab-count trail needed archaeology: 167 → +SUSPECTED_OF (S116) → +WITNESS_IN
  (S117) → +HONORED_AT (S134) = 170. The todos note claiming 169 had itself gone stale.
