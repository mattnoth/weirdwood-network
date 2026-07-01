# Continue: Graph parentage-correctness track (edge dedup + resolve ranking)

> **Track:** graph-data correctness (graph track, global S-numbering → `worklog.md`).
> Born S178 out of the chat-UI family-tree feature, which EXPOSED that the graph's parentage layer
> is noisy. Feature code is done + read-only; this track fixes the underlying DATA.
>
> **Recommended model:** Sonnet 4.6 for the deterministic Python (audit + apply scripts) + the
> `resolve.ts` ranking change. The **agentic batch review** (below) runs fresh subagents against the
> LOCAL wiki + chapter cache — Haiku/Sonnet subagents, gated by policy, NOT reviewed edge-by-edge.
>
> **HARD RULE:** no node/edge mint or delete until the review clears. Agents propose, Matt decides
> at the POLICY level (he can't hand-review 88+ — S178 confirmed). Never write to `sources/`.
> Rebuild derived artifacts after any approved mutation.

## START HERE next session — COLD READ, then validate the plan, THEN proceed

Matt's instruction: **do not trust this prompt's claims on faith — cold-read the situation first,
confirm the plan is solid, then execute.** (S178 made one wrong claim — "Maester Aemon has no node"
— that a cold read caught. Assume other specifics may drift too.)
1. Re-derive the numbers yourself: count >2-parent nodes, spot-check 3–4 buckets (Aemon, Daenerys,
   a Stark, a non-Targaryen) against `web/data/edges.json` + `web/data/nodes.json`. Confirm the
   two-bug framing (duplicate-stub vs single-person-noise) still holds.
2. Confirm the disambiguated nodes really do already carry the correct parentage (so dedup is
   delete-only, not create) — the Aemon case proved it; verify it generalises before scaling.
3. Only once the plan checks out, proceed to Step 1 below. If the cold read contradicts this prompt,
   flag it and re-plan — don't paper over it.

## The problem (evidence: `working/family-tree-genealogy-audit.md` — read it first)

88 of 1,015 parented nodes have **>2 PARENT_OF parents** (impossible for one person). This ONE
signal mixes TWO bugs — do not treat "88" as a work order:

1. **Duplicate parentage onto an empty bare-name stub.** The correct disambiguated nodes exist and
   are wired right, but the same parent→child facts were ALSO recorded to a redundant bare bucket.
   Verified: `aemon-targaryen` (0 quotes) carries 6 parents = the union of three real Aemons, each
   of whom has a correct node (`aemon-targaryen-son-of-maekar-i` = Maester Aemon, 16 quotes; etc.).
   → Fix = **delete the redundant stub edges** (the good node already has them).
2. **Spurious parent edges on a single real person** (Joffrey, Petyr Baelish, Aegon I — the
   two-Aerions bug). → Fix = **prune the wrong edges**, case by case (needs judgement/LLM).

## Approach — DECIDED with Matt (S178): Python first, then AGENTIC BATCH REVIEW

Two phases. Python does the mechanical proposal (cheap, deterministic, high-recall); fresh subagents
do the judgement the Targaryen same-name tangle needs (Matt: "the Targ ancestral tree has a lot of
the same names — that makes it hard to distinguish; no way I can analyze them all"). Matt gates by
policy on SUMMARIES, not edge lists (`feedback_subagent_verify_not_matt`,
`feedback_capture_quotes_during_research` — grab load-bearing quotes while in the text).

**Step 1 — deterministic dedup proposal (Python, READ-ONLY).** Write
`scripts/audit-parent-conflation.py`: for every >2-parent node, classify each incoming/outgoing
PARENT_OF edge as
  (a) REDUNDANT: a disambiguated variant node exists AND already carries the same (parent, child)
      fact → propose deleting the stub edge (high confidence, low judgement); OR
  (b) SUSPECT: no cleaner target / single-person edge-noise → route to Step 2 for agentic review.
Emit `working/graph-cleanup/parent-edge-proposal.jsonl` (edge, class, evidence wiki `ref`, proposed
action, confidence). Print a summary table. NO mutation.

**Step 2 — agentic batch review against the LOCAL cache (wiki + CHAPTERS).** For the SUSPECT class
(and a sample of REDUNDANT as a check), fan out fresh subagents — each takes a batch of candidate
edges and verifies against BOTH `sources/wiki/_raw/<Page>.json` AND the book chapters in
`sources/chapters/` (the parentage claim's truth, e.g. which Aemon/Daenerys/Brandon a father edge
belongs to). Subagent returns a verdict per edge (keep / delete / reassign-to-slug) + the
disambiguating evidence (wiki ref or chapter:line quote). Batch sequentially or in small waves near
quota (`feedback_sequential_near_spend_caps`); write-only-named-files; drift-check schema. Matt
reviews the SUMMARY + policy, not individual edges.

**Step 3 — apply (only after review clears):** delete/reassign the approved edges in the graph edge
store, then rebuild the chat bundle (`scripts/build-chat-export.py`) + indexes/alias resolver
(`weirwood refresh`). Re-run the Aegon family tree — empty-stub duplicates gone, main line correct.

**Step 4 — resolver ranking (small, independent, ship anytime):** in `web/src/lib/resolve.ts`, when
multiple candidates tie/overlap, rank by node **prominence** (degree + 4·quoteCount — the same
signal `familyTree` now computes) so an empty bare stub can NEVER outrank a content-rich node.
Requires exposing per-node degree/quoteCount to the resolver (precompute into the bundle in
`build-chat-export.py`, or compute at load). Add a test: "aemon targaryen" ranks
`aemon-targaryen-son-of-maekar-i` above `aemon-targaryen`.

**Step 5 — epithet alias backfill (cheap):** redirect pages were captured (`sources/wiki/_raw/
Maester_Aemon.json` exists). Derive missing epithet aliases (e.g. "Aemon the Dragonknight" →
`aemon-targaryen-son-of-viserys-ii`, currently → None) from redirect titles → target slug; add to
node `aliases:` (natural SPACED phrases, not kebab — see `project_node_alias_spaced_phrases`),
rebuild alias map.

**Option B (authoritative re-derive from infoboxes)** stays on the table as the someday-do-it-right
rebuild; don't start it without a decision — it's a bigger track.

## What's already TRUE (do not redo)

- `familyTree()` traversal + prominence signal shipped + tested (28 lib tests pass). Read-only.
- Alias layer already resolves "Maester Aemon"→son-of-maekar-i, "Egg"→aegon-v. Gaps are ranking +
  missing epithets, per Steps 4–5.

## Key files
- `working/family-tree-genealogy-audit.md` (diagnosis) · `web/src/lib/graph.ts` (familyTree +
  prominence) · `web/src/lib/resolve.ts` · `scripts/build-chat-export.py` (bundle/alias builder) ·
  the graph edge store under `graph/` + `web/data/edges.json` (built artifact).
