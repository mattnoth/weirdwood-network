---
session: 195
date: 2026-07-06
track: graph (hygiene)
model: Fable 5 (orchestrator + solo reviewer after the spend wall) + 3 Sonnet review subagents (1 completed, 1 delivered-then-died, 1 died empty)
api_cost: ~2 Sonnet review batches' worth; $0 after the spend wall (all deterministic Python + in-context work)
---

# Session 195 — Quote re-grounding to 0 FAIL (node + edge scopes) + dossier residue purge

## What this session was

The Matt-sequenced closer of the S192-picked sequence (S193 quote-minting → S194
receipts/node-UX → S195 re-grounding). Two debts: 185/803 book-cited node `## Quotes`
entries failing verbatim verification (found by S193's first-ever graph-wide check) and
the 58-row edge-quote mismatch backlog from the May-2026 Stage-4 bulk runs. Plus the
S194 addendum: dossier body prose had gone user-visible, exposing internal-provenance
markers and doubled quote attributions.

## The pipeline that did it

Python-first exactly as designed, with one Matt steer mid-session ("use cheap sub
agents wherever possible and sure eyeball it" — which both greenlit the apply and
swapped the planned solo-Fable disposition for Sonnet reviewers):

1. **Fresh baselines** (never trust a prior report): node 185 FAIL confirmed; edge
   turned out to be 59 mismatches (not the backlog's 58) + 185 OK_WIDENED + 1,008
   `badref`. The badref population was a discovery: those are **file-level
   `evidence_ref`s with no line number** — a never-scoped class, not drift. Left
   untouched, surfaced in todos as a future deterministic line-backfill.
2. **`scripts/propose_quote_regrounding.py`** — difflib token-run matching against the
   cited chapter, rare-token inverted-index fallback to sibling chapters, and
   marker-verbatim extraction only (proposed text is a char-for-char source span;
   retyping is structurally impossible). The "attribution-inclusive full span" upgrade
   was the big quality win: when a spliced quote's fragments sit ≤14 tokens apart in
   source (the gap being `," said X, "`), propose the whole verbatim span including
   the attribution — 46 rows kept their complete quotes instead of being truncated
   (e.g. `“There is a power in living wood,” said Jojen Reed, … “a power strong as
   fire.”`).
3. **Dry-validation gate** — every proposal re-checked against the *real* verifier
   logic before staging was even reviewed. This caught two proposer bugs during
   development: (a) token-level "exact" isn't string-exact (punctuation drift like
   `them;` vs `them,` passes tokens, fails the verifier) → proposed_text is ALWAYS the
   extracted span; (b) the edge verifier windows ±2 around the cite while the node
   verifier reads forward — edge cites must be span-centered. After the fixes: 387/387
   non-park proposals passed dry-validation.
4. **Review layer** — 206 text-changing rows to 3 Sonnet batches; 181 deterministic
   edge line-repoints skipped review by design. 3 hand-fixes done by Fable directly
   (the S123 exemplar `"Those are brave men. Let's go kill them."` splice; two
   paraphrase-not-quote edge rows including `ned-claims-the-execution`, whose
   "quote" was a narrator summary, replaced with Ned's verbatim "If it must be done,
   I will do it" line).
5. **`scripts/apply_quote_regrounding.py`** — merges staging + verdicts + overrides,
   re-validates every final pair again at apply time, rewrites node quote blocks
   (raw-line state machine mirroring the engine's `parse_quotes`) and edges.jsonl
   (backup first). Refuses to write anything that fails re-validation.

## Incident 1 — the monthly spend limit killed 2 of 3 reviewers mid-run

Batch 2 completed (69/69 accept + 2 attribution fixes). Batch 3 hit the wall at its
final *report* step — but its verdict file had already landed on disk (57 accept /
9 adjust / 2 park), the exact S191 suite-builder pattern: file-writes-then-report
means a spend death after the write loses nothing. Batch 1 died with nothing written.
Recovery: Fable re-reviewed batch 1's 69 rows solo in-context (they had all already
been read during the disposition survey), zero further API spend. Lesson re-confirmed:
have subagents write output files BEFORE their report step.

## Incident 2 — reviewer index error, caught by the re-verify step

Batch 2's two `attribution_fix` entries carried wrong indices (78/90 instead of
92/111) — the reviewer described `cersei-plots-against-margaery` and `fall-of-astapor`
but pointed at `bran-passes-the-black-gate` and `catelyn-seizes-the-moment…`, earlier
rows in the same events/ directory. The apply stamped Cersei's attribution onto Bran's
quote. **The post-apply verifier re-run caught it immediately** (2 fresh FAILs with
tell-tale cross-contaminated cites); repaired surgically (git-restore the two damaged
files, re-apply their own rows, hand-apply the two fixes to the right nodes), and the
review file was annotated (`misplaced_attribution_fix`) rather than silently edited.
Precedent for the standing pattern: verdict `accept` is index-insensitive and safe;
any verdict that CARRIES data (adjusted text, attribution fixes) is index-sensitive —
future review prompts should require the agent to echo the row's slug alongside the
index so the apply script can cross-check.

Also instructive: one batch-3 adjust (Gentle Mother hymn) failed re-validation not
because the reviewer erred on content but because the hymn is blank-line-separated
verse spanning 7 physical lines — no span containing the full stanza can EVER pass the
5-line verifier window. The proposer's trimmed span was already maximal. The
re-validation gate turned what would have been a regression into a documented revert.

## Results

- **Node: 803/803 PASS (was 618) — 0 FAIL.** Edge: MISMATCH 59 → 2, both documented
  parks; OK_WIDENED 185 → 39 (all dialogue spans wider than ±2 lines that pass the
  default gate; left as-is by design).
- **2 parks for Matt** (edges kept per the no-retirement gate): `tommen-baratheon
  MOURNS joffrey-baratheon` — the cited passage says the opposite and predates
  Joffrey's death, so the EDGE looks wrong, not just its quote; and the
  petyr-baelish/hairnet ASOS Sansa VI retrospective with a scene/chronology mismatch.
- **Dossier residue: shipped provenance markers 70 nodes → 0** across 3 cleanup rounds
  (`scripts/s195_dossier_residue_cleanup.py`); each round's survivors were new shapes
  (case variants, italic-wrapped tags, "overlay for <gloss>:" forms, one H3 heading
  the line-loop skipped). Internal ledger sections (`## Book citations`, Notes)
  deliberately untouched — they never ship and their bookkeeping voice is the record.
- **60 doubled attributions normalized** (`— ADWD Chapter 66 (Tyrion XII), path` →
  `— ADWD Tyrion XII (\`path\`)`) — the shape app.js `cleanQuote` collapses, killing
  the doubled render data-side as the S194 addendum asked. Scene glosses ("Red
  Wedding") preserved, redundant pov-roman glosses dropped.
- Close-out: refresh (8,110 timestamp restamps reverted / 18 real deltas kept), bundle
  + 6,693 node assets rebuilt, pytest 1447/0 · run_cases 37/0 · deno 100/0 (golden
  cases unchanged — text repairs don't move quote counts), census re-run (1,659
  quote-bearing nodes, unchanged).

## Deliberately NOT done

- Tier-hedge phrases in shipped prose ("Tier 2 — wiki hedges…") — left as the
  provenance-is-the-point voice; Matt overrules on read.
- The 1,008 file-level edge refs — surfaced in todos 10(b), not scheduled.
- `abduction-of-lyanna` dossier prose embeds a `../../edges/edges.jsonl` markdown link
  that can't resolve in the UI — cosmetic, noted in todos.
- No deploy (Matt-gated); everything rides the next manual
  `npx netlify deploy --prod --build`.
