---
session: 179
title: Graph parentage-cleanup — dedup deletes + epithet aliases + resolver ranking
date: 2026-07-01
track: graph-data correctness (graph track)
model: Opus 4.8 (handoff recommended Sonnet 4.6)
api_cost: subagents only (3 fresh general-purpose/script-builder reviews); no live chat-UI $
graph_writes: 138 PARENT_OF edge deletes; alias index regenerated; no node mint/delete
harvest_queue: 0 open rows
---

# Session 179 — Graph parentage-cleanup

## Purpose

Execute the `graph-parentage-cleanup` track born S178: the chat-UI family-tree feature
exposed that the graph's parentage layer is noisy — **88 of 1,015 parented nodes carry
>2 PARENT_OF parents** (impossible for one person). The handoff mandated a **cold read
first** (S178 had made one wrong claim a cold read caught), then a Python classifier →
agentic batch review → apply-after-review, plus resolver prominence-ranking and
epithet-alias backfill.

## The cold read overturned the handoff's framing (twice validated)

**Re-derivation.** Recomputed from `graph/edges/edges.jsonl` + `web/data/nodes.json`:
88 distinct-parent anomalies / 89 by edge-count (the +1 is `tyrion-lannister`, which has
an exact-duplicate `tywin→tyrion` row). The handoff's two-bug framing
(duplicate-onto-bare-stub vs single-person edge-noise) was **incomplete**. The real
decomposition of the 347 edges:

- `REDUNDANT_CHILD_STUB` (124) — a disambiguated variant already carries the parent; the
  edge into the bare bucket double-counts. Delete-only.
- `DUPLICATE_PARENT_NODE` (dominant SUSPECT cause the handoff missed) — one real parent
  under TWO slugs (maiden/married `elenda-caron`=`elenda-baratheon`; Greyjoy mother
  `sunderly`=`lady-sunderly-...`; the "two Aerions"). A cross-identity problem, not
  "prune spurious edges."
- `GENUINE_EXTRA_PARENT` — a genuinely wrong/extra edge; only ~8 nodes, not the ~53 the
  handoff budgeted the review for.

Key nuance: the "bare node" is often a **real content-rich character** (daenerys-targaryen
qc23, brandon-stark qc7 = Ned's brother) carrying its correct 2 parents PLUS conflation
noise — so dedup must be per-edge (delete `P→bare` iff a variant carries `P`), never
"delete all edges into the bare node."

## The fresh reviews earned their keep

Per Matt ("have a cold review sub agent do a fresh review"), two independent read-only
general-purpose subagents pressure-tested the re-plan before any mutation:

1. **Taxonomy review** caught a **destructive false-merge**: my first classifier's
   highest-qc-wins canonical rule would have merged the *correct* father of Aegon the
   Conqueror (`aerion-targaryen-son-of-daemion`, qc0) INTO `aerion-targaryen` (qc8 =
   Aerion the Monstrous, a different person 200 years apart), destroying the real node.
   Also flagged house-nodes-as-parents (`sunderly`="Redirect to: House Sunderly") and a
   4th mode (exact-dup edges). → I revised the classifier with deterministic guards:
   exact-dup dedup; `house-<slug>` detection → `HOUSE_AS_PARENT`; refuse-merge when a
   bare high-qc namesake would win canonical over a disambiguated variant →
   `WRONG_NAMESAKE`; conflation buckets → `NODE_SPLIT`.

2. **Deletion-safety + alias review** answered Matt's two questions with 100% checks
   (not samples): all 138 AUTO-APPLY deletes are non-lossy (every child keeps its correct
   ≤2 parents; edge-only, git-recoverable), and — the alias caveat — the deletes orphan
   no name because the nodes persist. It surfaced the "the "-prefix alias claim, which I
   then found was a **false alarm** for the runtime: the chat-UI's `normalize()` strips
   one leading article, so "the hound"→"hound" already resolved. The real alias win is
   narrower (epithets that don't reduce to a known short form).

## What shipped

- **138 provably-safe PARENT_OF deletes** (`scripts/apply-parent-conflation.py`, dry-run
  verified then `--apply`): 124 REDUNDANT + 13 HOUSE_AS_PARENT + 1 EXACT_DUP. PARENT_OF
  1688→1550; >2-parent nodes 88→50. Euron/Victarion now Quellon+Lady Sunderly; Tyrion
  tywin+joanna; bare Aemon an empty bucket.
- **Epithet-alias backfill** (`scripts/backfill-epithet-aliases.py`, built by
  script-builder): harvests "The …" wiki redirect pages → target slug; wired as a new
  additive source in `event_alias_resolver.py::build_and_save()`. +111 new phrases
  (12,029→12,140), additive-only, idempotent (e.g. "the bastard of barrowton"→denys-snow).
- **Resolver prominence ranking** (`web/src/lib/resolve.ts`+`types.ts`): exact + fuzzy
  candidates tie-break on `degree + 4·quoteCount`, so "aemon targaryen" ranks Maester
  Aemon (112) above the empty bucket (4). New test; 35/35 lib+edge tests pass.
- **Single bundle rebuild** (`build-chat-export.py`): edges 23330→23192, aliases
  12029→12140.

## Deferred (routed to their own tracks — NOT touched; review said don't auto-apply)

- `DUPLICATE_PARENT_NODE` (32) + `WRONG_NAMESAKE` (36) → 2nd agentic pass / node-merge track.
- 8 conflation buckets (brandon/rickon/rhaella/elaena/rhaenys/rickard/sansa/joffrey —
  joffrey = keep-all-3, presumed-vs-biological father) → node-split track.
- **merge⇒preserve-name-as-alias** rule must be baked into the node-merge tooling
  (not currently handled; "elenda caron" points only at its own stub).
- 2 remaining exact-dup edges outside the over-set (`oppo`, `penny` ← hop-bean).

## Incidental find

The epithet harvest surfaced a mistyped node `list-of-characters-created-for-the-cyanide-game`
(typed `character.human`, actually a non-canon video-game list-article) that "the butcher"/
"the collector" now alias. Per `project_video_game_entities_excluded` it should be deleted.
Spawned a background task chip.

## Artifacts

`working/graph-cleanup/`: `parent-edge-proposal.jsonl` (347 rows), `parent-node-summary.jsonl`,
`cold-review-verdict.md`, `deletion-safety-and-alias-review.md`, `epithet-backfill-report.md`.
Scripts: `audit-parent-conflation.py`, `apply-parent-conflation.py`, `backfill-epithet-aliases.py`.
