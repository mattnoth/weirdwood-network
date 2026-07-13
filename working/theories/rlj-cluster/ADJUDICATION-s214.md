# R+L=J cluster — orchestrator adjudication (S214)

**Fresh-verify:** 2 independent Haiku adversarial verifiers over 14 proposed edges →
**12 CONFIRM / 2 ADJUST / 0 REJECT** (`verify-T1-T7.jsonl`, `verify-T8-T14.jsonl`).

## Adjudications (Fable orchestrator)

| edge | verdict | action |
|------|---------|--------|
| T6 (daenerys → rlj, HotU blue flower) | verifier flagged stacked vision-symbolism | KEPT, **tier-3 → tier-4** + note; first use of intra-theory tier variance (node tier-3, weakest edge tier-4) |
| T8 (abduction-of-lyanna → rlj) | verifier: SUPPORTS inverted — quote states the official account the theory re-argues | **DROPPED as edge**; kept as labelled premise prose in the node body (neither SUPPORTS nor CONTRADICTS) |
| T9 (crowning → rlj) | verifier: quote (crypt statue) mismatched the source event node | **REQUOTED** to the crowning's own line (`agot-eddard-15.md:45` "He could see it still: a crown of winter roses, blue as frost."); statue quote stays body prose |
| all others | CONFIRM | as proposed |

**Final: 13 edges** (8 → `r-plus-l-equals-j` [7 SUPPORTS + 1 CONTRADICTS], 5 →
`knight-of-the-laughing-tree-theories`), 1 new node, 1 stub enrichment.

## Gates

- quotecheck 13/13 ALL FOUND (post-adjudication re-run)
- slug pre-check 10 existing + 1 new; re-run guard clean; mint dedup 0
- **DRY-RUN MINT GREEN** (edges → scratchpad copy; 13 appended, 0 dup-skipped)
- theory-gate: both targets are `concept.theory`; all edges tier-3/4; no tier-1/2
- chat surface untouched (SHARED_RULES no-theories guardrail intact)

## Incident (tooling, logged)

`mint_enrichment.py` validation mode (`--edges/--backup` pointed off-graph) still
wrote the NEW NODE file into the real `graph/nodes/theories/` — docstring promises
"write nowhere near the live graph". Reverted immediately (file deleted; live
edges.jsonl untouched at 26,740). Fix candidate: a `--nodes-root` override for
validation runs. → todos.

## Schema notes (for Matt's review)

- `claim:` frontmatter added to both node files (README schema; proposer had it
  body-only).
- New frontmatter fields in play for `concept.theory`: `claim`, `status`
  (open | show-confirmed | jossed), `origin`, `video_sources`, `pass_origin` —
  architecture.md needs a sync line at mint time (orchestration rule 6).
- CITED_BY deferred (no out-of-world source node type) — provenance in frontmatter.
- KotLT keeps wiki-artifact name "Knight of the Laughing Tree/Theories" for stub-
  convention consistency; display-name cleanup is a separate decision.

## Pending Matt

MINT GATE: no graph mutation without Matt's explicit go (S213 grant was
session-scoped). On go: mint via `scripts/mint_enrichment.py --candidates
working/theories/rlj-cluster/candidates.json --nodes-dir working/theories/rlj-cluster/nodes`
+ apply `enrich/knight-of-the-laughing-tree-theories.node.md` over the stub +
`weirwood refresh` (new node + aliases) + architecture.md sync.
