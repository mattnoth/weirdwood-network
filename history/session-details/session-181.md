# Session 181 — Graph parentage-cleanup phase 2: node merges + conflation splits

**Model:** Sonnet 5 (handoff recommended Sonnet 4.6). **Track:** graph (global S-numbering).

## Context

Picked up `/continue graph-parentage-cleanup`, which routed to the S179 handoff at
`progress/continue-prompts/2026-07-01-graph-parentage-node-merge.md`: phase 2 of the
>2-parent-node cleanup, covering the two classes S179's cold-review said must NOT
auto-apply (`DUPLICATE_PARENT_NODE`, `WRONG_NAMESAKE`) plus 8 conflation-bucket nodes
needing node-splits.

## The work

Dispatched three fresh general-purpose subagents (sequential, near-quota-caution) to
independently verify each class against the local wiki cache before any mutation:

1. **DUPLICATE_PARENT_NODE (30 proposed merges)** — the review found almost none were
   genuine same-person duplicates. The classifier's "bare slug + disambiguated variant
   both parent the same child → merge" heuristic is unsafe: AWOIAF uses bare
   "Firstname Lastname" pages as disambiguation pages listing multiple distinct people
   across centuries far more often than as true redirects. Only 2 of 16 distinct pairs
   were real: `elenda-caron→elenda-baratheon` (literal wiki redirect) and
   `alayne→alayne-baelish` (same mother-of-Petyr fact under two slugs, confirmed by
   direct edge-direction inspection, not a Sansa/Alayne-Stone mix-up as initially
   feared). The other 13 pairs were flagged as different people and rerouted to
   per-child deletes.
2. **WRONG_NAMESAKE (36 edges)** — confirmed all 8 name-pairs are genuinely different
   people (the "two Aerions" pattern recurred: Alys Karstark, Brandon Stark, Rickon
   Stark [a genuine cross-child double-conflation — shadows TWO different real Rickons],
   Rhaenys/Elaena Targaryen, Luthor Tyrell). All 36 resolved to pure deletes — the
   correct disambiguated-variant edge already existed in every case. (First dispatch of
   this review spawned its own sub-agents instead of doing the work and returned no
   output file — relaunched with an explicit "do this yourself, no sub-agents"
   instruction; the retry matched the eventual correct file exactly.)
3. **NODE_SPLIT (8 conflation-bucket nodes)** — per-node judgement using wiki infobox
   Father/Mother fields to identify the primary/most-referenced person and their true
   ≤2 parents. `joffrey-baratheon` confirmed as a legitimate 3-parent special case
   (Cersei/Jaime biological, Robert presumed/legal) — kept untouched. The other 7 needed
   a mix of deletes (no target node exists for the true child) and reassigns (a
   disambiguated variant node already exists and should carry the edge instead).

While pre-checking the review's REASSIGN targets against `edges.jsonl`, found that 4 of
the 5 targets already carried a DIFFERENT wrong-slug parent for the exact same fact
(e.g. `rhaella-targaryen-daughter-of-aegon` already had bare `aegon-targaryen` /
`rhaena-targaryen` as parents — the same underlying fact, just resolved to the wrong
slug on that end too). Verified each via a direct wiki infobox fetch and added a
matching DELETE for the stray wrong-slug duplicate so the reassign wouldn't create a
new >2-parent problem on the target.

## Implementation

Wrote `scripts/apply-node-merge-and-namesake.py` — a single explicit, hand-verified
action list (2 merges / 51 deletes / 5 reassigns) rather than a generic re-classifier,
given the small scale and the stakes of getting canonical-selection wrong again. Caught
two bugs in my own first draft before applying:

- **Unscoped global dedup**: my first dedup pass accumulated exact-(source,target,type)
  keys across the ENTIRE 23k-edge corpus, which would have silently dropped any
  pre-existing duplicate edge anywhere in the file — not just ones this cleanup created.
  Rewrote to only dedupe rows this script actually touched (merge-rewritten or
  reassigned), leaving untouched pre-existing state alone.
- **Order-dependent duplicate escaping the fix above**: a single-pass streaming dedupe
  missed a duplicate when the untouched original row appeared AFTER the newly-rewritten
  row in file order (`cassandra-baratheon` ended up with `elenda-baratheon` listed
  twice). Rewrote to a proper two-pass group-by-key dedupe that's order-independent.

Dry-run asserted every touched child ends at ≤2 parents (except the intentional
`joffrey-baratheon` exception) before any write.

## The concurrent-write collision

At session close, discovered a DIFFERENT Claude Code session had claimed the actual
"Session 180" slot in the shared repo: a family-tree pop-out modal + a root-cause fix
to `wiki-infobox-parser.py` (a piped-wikilink bug that was discarding the `title=`
attribute on disambiguation links — the same failure class as this session's
namesake-collision work, but fixed upstream in the parser instead of band-aided in the
edge store). That session committed `2ac772dd2f` directly to `graph/edges/edges.jsonl`.

Because both sessions were operating in the **same working directory** (not separate
git worktrees), the later commit overwrote this session's edge-level edits in the
shared file — there is no merge on a single JSONL file between two independent
processes, just last-write-wins. Verified: `jon-stark→rickard-stark`, an edge this
session had deleted after direct wiki confirmation, was back in the committed state.
This session's node-file work (retiring `alayne.node.md`/`elenda-caron.node.md`, adding
the "Elenda Caron" alias) survived only because it was still sitting as uncommitted
working-tree changes, never touched by the other commit.

The upstream parser fix independently dropped the >2-parent count 50→13 (with zero slug
overlap against this session's specific proposal set, per that session's own check).
Recovered by re-running `audit-parent-conflation.py` fresh against the post-collision
state: the residual 13 nodes were the *exact same already-vetted shapes* — 11
`HOUSE_AS_PARENT` edges (identical pattern to S179's proven-safe auto-class) and the one
already-wiki-verified `rickard-stark`/`jon-stark` fix. Reapplied both directly
(no need to re-run the heavy subagent review — the facts hadn't changed) to reach the
final 50→1 state.

## Lesson

Two Claude Code sessions writing the same shared working tree (not isolated via git
worktrees) can silently clobber each other's uncommitted edits to the same file. Worth
considering git worktrees for any future graph-mutation track that might run
concurrently with another.
