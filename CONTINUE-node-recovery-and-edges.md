# CONTINUE — Node Schema Recovery, then Edge Re-validation

> **Next session: Opus 4.7 — "the fixer & finder."** This doc is deliberately **thorough but
> flexible** — it captures the situation + the open questions + a *suggested* order. Reason about
> it; don't execute it rigidly. Matt's framing, 2026-05-25 (mid-Session-71 pivot).
>
> **Trust `worklog.md` over this doc if they disagree** (CLAUDE.md #9).

---

## Why we stopped (the pivot)

Stage-4 edge work surfaced that **a large chunk of the wiki Pass-2 entity schema was never
promoted into `graph/nodes/`.** This is the blocker. Edge formalization is **PAUSED** until the
node layer is whole, because edge type-checking and resolution both ride on the node set.

**Smoking gun:** the v1.1 type-contract validator "dropped" real relationships like
`gunthor COMMANDS stone-crows`, `ben-plumm COMMANDS second-sons`, `victarion COMMANDS iron-fleet`,
`beric COMMANDS brotherhood-without-banners` — **because those factions/military-orgs aren't in
`graph/nodes/characters/`.** They're real entities; the node gap made the validator treat them as
junk. That's the node problem producing false edge-drops in real time. (Do NOT apply that v1.1
candidate — see "Edge state" below.)

---

## THE FINDING — nodes are staged, not lost

- `graph/nodes/` currently holds **8,299** promoted nodes (characters 3,926 / locations 1,097 /
  houses 556 / titles 542 / events 371 / artifacts 282 / factions 191 / … / theories 45 /
  prophecies 2). ~5 categories hold 2/3 of the nodes; the analytical layer (theories/prophecies)
  is nearly empty.
- **`working/wiki/pass2-buckets/*/skeleton/` holds ~7,251 staged `.node.md` files** that were built
  but **never promoted.** This is the "staging nodes ready in the wiki" Matt remembered. They are
  NOT lost.
- Source cache: **17,657** wiki pages in `sources/wiki/_raw/`. So even 8,299 promoted is ~47% of
  pages — much was intentionally deferred (stubs/lists/years), but the ~7,251 skeletons are the
  curated set that should have landed.

**First job is an honest accounting:** reconcile the 7,251 staged skeletons against the 8,299
promoted — how many are net-new vs already-promoted vs dupes? Why did promotion stop (Session ~40s)?
Likely a half-finished Pass-2 promotion run. Recover the net-new; dedupe; don't double-promote.

---

## Suggested work streams (order + fleet-vs-not is the next session's call)

**Stream 1 — NODE ACCOUNTING & PROMOTION (the big one; do first).**
Reasoning-heavy + judgment → recommend a **single Opus session** for the *accounting + plan*, then
fan out subagents only for the mechanical promotion once the reconciliation rules are clear.
- Map: staged-skeleton set vs `graph/nodes/`; what's missing; promotion provenance (which Pass-2
  run stopped). Check `working/wiki/data/` products (`page-index.jsonl`, `page-categories.jsonl`,
  `infobox-data.jsonl`) + the Pass-2 pipeline runbook (`working/runbooks/wiki-pass2-pipeline.md`).
- Promote the net-new skeletons into `graph/nodes/{category}/` with the schema/conventions already
  used. Watch dupes/aliases (the `bronze`→`yohn-royce`, `queen-cersei`→`cersei-lannister` class —
  alias completeness is a shared lever for BOTH node-resolution and edge-quote tokenizing).

**Stream 2 — EDGE RE-VALIDATION (after nodes; NOT a full re-extract).**
Matt's question "will we completely redo the edges?" — **No.** The book→hint→type→pair *extraction*
is sound and stays. With the complete node set, re-run two **deterministic ($0)** steps over the
existing candidates:
  - **Re-resolve** endpoints (more real nodes → fewer junk/unresolved).
  - **Re-type-check** with the type-contract validator now seeing factions/titles/locations as
    valid targets (the COMMANDS→faction false-drops disappear; consider a `COMMANDS`/`LEADS`
    faction-target allowance or retype). The LLM-typed tail mostly holds (more nodes don't change
    an edge's *type*).
Then the held v1.1 dispositions (the curated drop/retype/flag set) get re-derived against truth.

**Stream 3 — FOLDER CLEANUP / REORG (own session[s]).**
`working/wiki/` and `scripts/` are dumps (e.g. dozens of `stage4-*.py`). Reorganize into themed
subdirs ("by epic"). Also: a leftover git worktree `.claude/worktrees/mystifying-burnell-*/` is
clutter. Nothing deleted without care (CLAUDE.md: source is read-only/additive; archives stay).

**Stream 4 — 0.1 scratch check.** Matt: a "scratch→markdown promotion check" is wasting context.
I searched project/local/global `settings.json` (no `hooks` in any) + found no scratch `.md`
artifacts. The `scratch-2.tx` content reached the agent as an **IDE text-selection** surfaced by the
harness, not a repo hook. If a specific hook/command is meant, Matt should point to it; otherwise
this is IDE-selection behavior, not a removable repo mechanism. (scratch stays unread.)

---

## Edge state — DO NOT LOSE (frozen, captured)

- **Committed v1: `graph/edges/edges.jsonl` = 3,842 cited deterministic edges. FROZEN, untouched**
  (md5 verified this session). Stands as the deliverable.
- **v1.1 refinement candidate** built at `working/wiki/pass2-buckets/pass1-derived/_v1-refine/
  edges-v1.1-candidate.jsonl` (3,805 rows) — **NOT applied, and should NOT be** until nodes are
  whole: its 37 drops include false faction-drops (Stream-1 will fix the node-type basis). The
  *curated* dispositions Matt approved (4 sure-drops / 3 RULES→COMMANDS retypes / ECHOES-char↔char
  kept / 5 node-dependent FLAGs) are recorded in `working/wiki/data/pass1-derived-v1.1-applied.md`
  + the proposal `pass1-derived-v1-refine-proposal.md`. Re-derive after Stream 2.
- **Enrichment (Events+Dialogue Haiku) = NOT-YET** — honest out-of-sample ~62% (smoke6); root cause
  = locator hint↔quote decoupling. Lever spec: `progress/continue-prompts/2026-05-25-stage4-locator-grounding.md`.
- **All Stage-4 scripts are UNCOMMITTED** (Matt checkpoints): `stage4-{quote-relevance-filter,
  type-contract-validator,fresh-relocate-sample,refine-v1-edges,produce-v1-1-candidate}.py`,
  improved `stage4-pass1-evidence-locator.py`, modified `stage4-tail-classifier.py` (prompt v4 +
  prompt_sha stamping). 119+ tests green. Decide whether to commit a checkpoint before reorg.

---

## Honest note on how this happened (for the postmortem)
The node-promotion gap should have been caught before edge work. It wasn't surfaced — possibly lost
to worklog archiving across sessions. The lesson belongs in the worklog Active Decisions, not buried.
A `graph/nodes/` count vs `working/wiki/pass2-buckets/*/skeleton/` count is a one-line health check
that would have flagged it.

## Key pointers
- Staged nodes: `working/wiki/pass2-buckets/*/skeleton/*.node.md` (~7,251)
- Promoted: `graph/nodes/{category}/*.node.md` (8,299)
- Pass-2 pipeline runbook: `working/runbooks/wiki-pass2-pipeline.md`
- Wiki data products: `working/wiki/data/{page-index,page-categories,infobox-data}.jsonl`
- Edge layer: `graph/edges/edges.jsonl` + `graph/edges/README.md`
- Staging-layer manifest: `working/wiki/data/pass1-derived-staging-manifest.md`
