# Fable Audit Synthesis — 2026-06-11

> Orchestrator synthesis of `history-audit.md` + `graph-deep-dive.md`. Accepted by Matt 2026-06-11
> (`working/reply-to-audit-session-2026-06-11.md`): all three wiki-layer verdicts agreed,
> infobox merge greenlit as next track, prose-comention stays dead.

## TL;DR

The project is in much better shape than its documentation says it is. There is a real, validated,
cited knowledge graph — 8,261 nodes, 4,760 edges with verbatim book quotes, 0 orphans, working event
reification. But **85% of nodes are isolated**, and the fix has been sitting on disk, fully parsed,
since April: the wiki **infobox-structural layer** (~20,614 typed relationship rows in
`working/wiki/data/infobox-data.jsonl`). It is 98.4% additive to the book edges, deterministic, $0,
and merging it moves graph connectivity from **14.7% → ~72%**. That is the one true next step.
After it, go to dialog (Mode 3 dip on the merged graph). The prose-comention wiki edges stay dead — correctly.

## The three wiki edge layers — verdicts

| Layer | What it is | Verdict |
|---|---|---|
| **Infobox-structural** | 20,614 relationship rows, already parsed + typed to 23 vocab edge types (SWORN_TO 4,142, HOLDS_TITLE 3,976, PARENT_OF 3,143, CULTURE_OF 3,329, SPOUSE_OF 668…), 92% target-resolvable | **MERGE.** Not salvage — a never-shipped deterministic product. One Python script, ~18–19k edges after noise filtering, $0. |
| **Node-file `## Edges` bullets** | 21,129 display bullets across 4,684 node files | **Do nothing** — same data as the infobox layer (track_b provenance). Merging the layer above supersedes them. |
| **Prose-comention/entity emits** | ~6k Sonnet+Haiku emits in pass2-buckets + 1,617 NO-GO'd Events rows | **Leave deprecated.** Wiki-prose evidence only, no file:line, inconsistent schemas, type-stretches. Re-validating costs more than the curator path already producing better edges from book text. Keep as candidate pool at most. |

## Why it's necessary for the dialog goal

Today an agent traverses a dense, high-quality affect/interaction graph over ~1,200 entities and hits
a wall everywhere else: characters 20% connected, houses 4.5%, locations 5.2%, titles 2.6%.
Concrete walls: "Who are Walder Frey's children?" (book layer: 2 edges; wiki: 8 spouses + 29 children);
"Which houses are sworn to House Tyrell?" — nothing; Varys/Melisandre/Ygritte/Barristan have zero
family/structural edges. Lookup-shaped questions are what dialog users ask first. The merge fills
genealogy, fealty, titles, vital records; the book layer keeps owning lived relationships with quotes.

## Merge guardrails (became the Step-3 spec seeds)

1. **Wiki edges get Tier 2, never Tier 1** — Tier 1 is earned by verbatim book quotes.
   Tag `evidence_kind: wiki-infobox`, `typed_by: python-infobox-map`, cite `wiki:<Page>`.
2. **Quarantine speculative fields** — Jon Snow's infobox lists two "Mothers" (Wylla AND Ashara Dayne);
   naive promotion mints false PARENT_OF edges. Multi-value fields and Unknown/None/Extinct targets (~2.5%) filtered.
3. Fold in two hygiene fixes: the **115 orphan endpoint slugs** in edges.jsonl (alias mismatches like
   `brienne-of-tarth` vs node `brienne-tarth`) and the missing `typed_by`/file:line format on the
   **948 reified role edges**.

## Matt's question: theories/prophecies isolation (answered from data, 2026-06-11)

- **theories/: 45 nodes, exactly 1 connected** — and that one edge (`FEARS` touching
  `death-of-laenor-velaryon-and-harwin-strong-theories`) looks like a misresolution, not a real theory edge.
- **prophecies/: 2 nodes, 0 connected.**
- **Zero wiki `## Edges` bullets in either dir** — theory/prophecy wiki pages have no infoboxes,
  so the infobox merge contributes NOTHING here. This layer is 100% dark and stays dark after the merge.
- **What would connect them:** (a) deterministic low-tier ABOUT/MENTIONS edges minted from the wiki
  theory pages' own prose links (the pages link heavily to the characters/events they discuss — cheap,
  scriptable, Tier 3-4); (b) the designed-but-unbuilt Pass 4/5 surface: FORESHADOWS / evidence edges
  from chapter extractions into theory/prophecy nodes, via `reference/foreshadowing-events.md` +
  a theory-seeds file (still unwritten), with findings landing in `curation/` per the agents-propose rule;
  (c) prophecy nodes are just undercounted — 2 nodes for a series saturated with prophecy means the
  node layer itself needs minting (Azor Ahai, the dragon-has-three-heads, valonqar, etc. exist as
  wiki pages but were typed elsewhere or not promoted as prophecies). Shape of the gap: small node set,
  zero edges, no deterministic source except wiki prose links; everything else is gated analytical work.

## My take, plainly

This project's distinctive achievement isn't the graph — it's the **discipline stack** that produced it:
Python-before-agent, smoke-before-spend, cross-model audits, provenance-in-data, vocab lockdown.
That stack repeatedly overruled both the models and the orchestrator sessions, and it's why the edge
layer is ~78% strict precision with verbatim citations instead of a plausible-looking swamp.
The irony of the wiki-edge saga: ~$250 and five weeks were spent trying to make LLMs extract edges from
wiki *prose*, then deprecated — while the wiki's *structured* data was already parsed, typed to the
project's own vocabulary, and one filter-script away from tripling the edge count for free.
The deprecation was right; the merge was just never sequenced.

**Recommended order (accepted):** (1) infobox merge + hygiene fixes (Python, $0) — spec'd this session,
dry-run for Matt's review, ship in a later session; (2) Mode 3 grounded-agent dip on the MERGED graph —
its failure modes drive whether backfill Tracks A/B/C or the deferred restructures matter;
(3) repo-audit/doc-reconciliation armed with `doc-rot-punch-list.md` (largely executed this session).
Events-Haiku output and Dialogue tail stay shelved unless the dip proves a gap they'd fill.
