# SESSION 195 — Quote re-grounding cleanup (node + edge scopes)

> **This is Session 195.** Stamp your worklog entry `### Session 195` at endsession.
> (If another graph/meta session lands first, renumber — check `worklog.md`.)
> Matt-sequenced at S193 close: runs AFTER S194 (receipts/node-UX). Two backlog
> halves merged into one session (todos item 10 sub-bullet (b)).

**Recommended model: Fable solo, Python-first** — the triage/relocation is
deterministic; only span selection on the spliced rows is judgment. Optional 1–2
cheap Sonnet batches if the review queue drags, but the S193 pattern (marker-verbatim
extraction, zero API spend, all in-context) should carry it in one session.
**Matt's usage concern (S193 close): keep it cheap** — Python proposes, Fable
dispositions in bulk; no per-row subagent fan-out.

**Track:** graph (hygiene). **State you inherit:** S193 minted 71 verified quotes and
built the tooling this session reuses: `scripts/verify_node_quotes.py` (engine-parser
cite checker, wrap-quote tolerant), `scripts/mint_node_quotes.py` (marker-verbatim
attach). Read `worklog.md` S193 + STATUS first; trust worklog over this prompt.

## The gap

1. **Node scope (found S193, first-ever graph-wide check):** **185 of 803 book-cited
   node `## Quotes` entries fail verification** — 2 pure line-drift (exact text found
   at a different line, deterministic repair), 183 not-found-verbatim (the
   splice/paraphrase class: quotes stitched across dialogue attributions or condensed
   — the S123 checker failure mode, at node scope). Full row list:
   `working/quote-census/node-quote-drift-report.md`.
2. **Edge scope (known since S117-era):** 58 whole-graph `scripts/verify-edge-quotes.py`
   mismatches, concentrated in the May-2026 Stage-4 bulk runs (`pass1-derived-20260523`,
   `tail-llm-20260523*`, `pass1-extra-tables-20260525`). Low severity, same repair
   machinery.

The chat's cite gate hard-rejects drifted cites at answer time, so every drifted row
is a quote the live product silently cannot serve.

## The work

0. **Re-run both verifiers fresh** (`verify_node_quotes.py` whole-graph;
   `verify-edge-quotes.py` scoped per todos item (b)) — don't trust the S193 report
   blindly; S194 may have landed changes.
1. **Python repair-proposer FIRST (no agents):** for each failing row, fuzzy-locate
   the best candidate line in the cited file (token-overlap window scan; also scan
   sibling chapters of the same book when the file itself has no plausible window).
   Classify: (a) exact-elsewhere → auto-repoint the cite line; (b) near-match → propose
   the longest clean CONTIGUOUS verbatim sub-span at the located line (marker-extract,
   never retype); (c) spliced-across-attribution → same, keeping the biggest clean
   fragment; (d) no plausible source → propose drop-or-park. Emit ONE staging file
   with every proposal + before/after.
2. **Fable dispositions the staging file in bulk** (accept/adjust/park per row), then
   an apply script rewrites the node/edge rows marker-verbatim. Never splice across
   attributions (the standing S123 rule).
3. **Re-verify to 0 FAIL** (or documented parks in the staging file); `weirwood
   refresh` + bundle rebuild; suites (pytest / run_cases / deno); golden cases may
   legitimately shift quote counts — update with a note, same as S193's
   `list-customs-has-quotes` 2→5.
4. Worklog S195 entry; re-run `scripts/quote_census.py` so the worklist stays current.

## Hard gates

Text repair only — additive/corrective `## Quotes` + edge `evidence_quote`/`evidence_ref`
edits; **NO new nodes, NO new edge types, NO edge retirement without a per-row note**
(a quote that can't be re-grounded parks the row, it doesn't delete the edge —
surface those for Matt). `sources/` read-only; never fetch the wiki; don't touch
`scr`; deploy is Matt-gated; never auto-run /endsession.
