# Family-tree genealogy audit — parentage errors in the graph

_Session 178, chat-UI family-tree feature. READ-ONLY investigation. No nodes/edges minted. Agents propose, Matt decides._

## Correction notice (read first)

An earlier draft of this doc claimed **Maester Aemon has no node** and that the fix was mostly
"split buckets + create missing nodes." **That was wrong.** Maester Aemon has a proper node —
`aemon-targaryen-son-of-maekar-i`, 16 book quotes. All three Aemons have correct, disambiguated,
correctly-wired nodes. The real problem is different (below), and smaller-sounding but subtler.

## TL;DR

The `family_tree` traversal is faithful to the graph. The graph's parentage layer has **widespread
errors**: **88 of 1,015 parented nodes have >2 PARENT_OF parents** — impossible for one person.
But that single signal mixes **two distinct problems**, and the fix is per-case, not uniform:

1. **Duplicate parentage onto a bare-name stub.** Where several people share a name, the correct
   disambiguated nodes exist AND are wired correctly — but the *same* parent→child facts were
   *also* recorded onto a redundant **bare-name bucket**. Example (verified):
   - `aemon-targaryen` (bare, **0 quotes**) has SIX parents: Jaehaerys I + Alysanne, Maekar I +
     Dyanna Dayne, Viserys II + Larra Rogare — the union of three different Aemons.
   - Yet `aemon-targaryen-son-of-maekar-i` (Maester Aemon, 16 quotes), `-son-of-jaehaerys-i`, and
     `-son-of-viserys-ii` all EXIST with the correct parents already.
   - So `Jaehaerys I → aemon-targaryen` AND `Jaehaerys I → aemon-targaryen-son-of-jaehaerys-i`
     both exist. The tree double-counts, and walks into the empty bare stub.
   - Fix = **delete the redundant edges to the bare bucket** (the good node already has them);
     optionally retire the bucket to a pure disambiguation stub. Mostly cleanup, not creation.

2. **Spurious/extra parent edges on a single real person.** Some >2-parent nodes are ONE person
   who accreted wrong edges — grandparents mislabeled as parents, step-parents, or a bad ingest.
   The "needs a disambiguated variant" bucket includes clearly-single characters — **Joffrey
   Baratheon, Petyr Baelish, Aemma Arryn, Aegon I Targaryen** — so this is NOT name-conflation;
   it's edge noise on a real node. Fix = **prune the wrong parent edges**, case by case.

A crude slug-variant heuristic split the 88 as ~35 "a disambiguated node already exists" vs ~53
"no variant found" — but that heuristic is unreliable (it flags Aegon I as needing a variant when
his problem is the two-Aerions edge bug). **Do not treat those counts as a work order.**

## What IS solid

- Clean, non-repeating families render perfectly (Starks under Ned — verified).
- The damage concentrates on repeated dynastic names (Targaryen 26, Stark 19, Tyrell 9, Greyjoy 7,
  Baratheon 6, Frey 5 among the 88).
- Repeated real people appear at wrong depths / with impossible siblings when a tree crosses one of
  these nodes (e.g. Rhaego beside "Maron Martell's son" under a fused `daenerys-targaryen`).

## Shipped this session (read-only, no graph mutation)

- `familyTree()` traversal + LR-tree render + clickable dossier.
- **Prominence** on every member (`degree + 4·quoteCount`): Dany 402, Rhaegar 118, Viserys 102,
  Daemon 68… vs bare-surname stubs ~1. Lets the render foreground real characters in a noisy tree.
  It does NOT fix edges — it makes the important people legible despite the noise.

## Proposed next step — NOT executed, needs Matt's decision

A **read-only** diagnostic script, `scripts/audit-parent-conflation.py`, that for every >2-parent
node classifies it as (1) duplicate-onto-bare-stub [list the redundant edges + the correct target],
or (2) single-person edge noise [list the implausible parent edges], with the wiki `ref` of each
edge as evidence. Output a review table; Matt (or a fleet pass) approves the deletions. No mint
until that review. This is a graph-data track, separate from the chat-UI work.
