---
session: 60
date: 2026-05-19
model: Opus 4.7
title: Stage 4 Haiku — Sonnet-Mission Revert, Normalizer Built, No-Silent-Drop Pipeline
type: conductor / design + incident
---

# Session 60 — Stage 4 Haiku: Normalizer + No-Silent-Drop Pipeline

Conductor session. Launched from `/continue 2026-05-19-stage4-haiku-run-batches`.
Heavily steered — Matt interrupted ~7 times to redirect; the session converged on
building the deterministic normalizer and designing the no-silent-drop pipeline
rather than running bulk batches.

## Opening — "usage is up a lot, did batches run?"

STEP 0 of the continue prompt was to read the 8-batch wave's `run-summary.json`.
It had run at Session-59 close: chunk-15, concurrency-8, **40/40 files, 0 failed,
0 rate-limit events, 5.6 min wall, $3.66** ($0.092/file). Clean.

Total Haiku batch API spend to date ≈ **$8.51** (batch-0020 smoke ~$4.85 + the
8-wave $3.66). Nothing was running at session start. Conclusion surfaced to Matt:
the Haiku batch cost is small — any usage spike is the **Opus conductor/watcher
sessions**, not the Haiku workers.

One caveat recorded: every batch in the 8-wave was 5 files = a single chunk, so
the chunk-15 cap never bound. chunk-size is still untested at scale; only
batch-0020 (30 files) is a real multi-chunk datapoint.

## Incident — the Sonnet mission had been touched

Matt flagged that the git status showed the Sonnet mission modified
(`state.jsonl` + 2 deleted locks) and asked why. Forensic trace:

- The `state.jsonl` diff = 5 appended lines from an **abandoned Session-59
  attempt to run Haiku as a worker inside the Sonnet mission**. Worker
  `20260519-141654` claimed `batch-0020-haiku-smoke` into Sonnet's ledger, ran 3
  of 30 files, then early-exited; worker `20260519-142205` claimed `batch-0057`.
- This is exactly the failure the Session-59 worklog documents ("Haiku cannot
  drive the Sonnet worker's batch-bookkeeping") — the residue was just never
  cleaned up.
- **No Sonnet output was overwritten** — every `prose-edges/*.edges.jsonl` was
  git-clean; the 3 files the stray `file_done` events named still had May-16
  mtimes. The Haiku output that did get produced was correctly in the separate
  `prose-edges-haiku/` dirs.
- The current Python orchestrator (`scripts/stage4-haiku-run.py`) does NOT touch
  the Sonnet mission — verified against its own docstring and a grep of all its
  writes.

Resolution: `git checkout` restored `state.jsonl` + the 2 lock files. Sonnet
mission clean.

**Terminology correction:** Matt called out the word "harness" as confusing —
it was an old generic term I'd leaned on. Dropped. The project pattern is
orchestrator/watcher (Opus) + workers (Haiku); the Haiku version differs only by
3 Python levels wrapping the worker (orchestrator / normalizer / pre-loading).

## The normalizer — built, over-reached, re-scoped

Built `scripts/stage4-haiku-normalize-edge-types.py` — a deterministic
edge-type-name normalizer. The locked 159-type vocab makes a closed-set
fuzzy-match possible (`TRAVELED_TO` → `TRAVELS_TO`).

**First build over-reached.** It produced a hardcoded *alias table* that
conflated two different things: true morphological variants (same word, wrong
tense) AND semantic synonym substitutions (`ATTACKED_BY` → `KILLED_BY`,
`SUPERVISES` → `COMMANDS`, `USES` → `WIELDS`). Of 40 rewrites, only 19 were
genuine normalizations; 21 were semantic remaps. Caught in dry-run review.

Two reasons that's unacceptable: (1) it writes factually wrong edges
(attacked ≠ killed); (2) we are about to measure Haiku's drift rate against
Sonnet — if the normalizer silently launders semantic mistakes into clean
canonical types, it destroys the signal we are measuring.

Re-scoped: the alias table holds **only** morphological variants — same English
word, differing by inflection or a literal typo. Anything cross-lemma routes to
a report-only bucket. Final alias table = 6 entries. 19 morphological rows were
applied to the existing Haiku output.

## Parser bug — vocab was 161, not 159

The validator's `load_canonical_vocab()` reported 161 canonical types. Traced to
the heuristic scraping two backticked tokens out of *description prose*:
`FOSTERED_BY` (a permitted reverse-direction form of `WARD_OF`) and `LOCATED_IN`
(architecture.md's own words: "Deprecated synonym ... normalize on read").
Fixed the parser to count only table-row edge types → correct **159**.
`LOCATED_IN` → `LOCATED_AT` added to the normalizer (architecture explicitly
blesses it). `FOSTERED_BY` is direction-unsafe to rewrite blindly — routed to the
unresolved log instead.

## The no-silent-drop pipeline (Matt's design steer)

Matt's recurring concern: no edge should be silently dropped when there is no
exact vocab match. The pipeline that emerged (6 stages):

1. **Prevention** — inline the 159-vocab into the classify prompt.
2. **Classify (Haiku)** — emits edges.
3. **Deterministic normalizer (Python)** — morphological fixes; residual → log.
4. **Second Haiku residual-resolution pass** — maps logged residuals to
   canonical-or-explicit-reject; its residual → log, tagged `haiku-residual`.
5. **Validator** — flags append to the log.
6. **Targeted Opus review** — runs last, reads ONLY the log + printed vocab.

Two artifacts make this work, both built this session:
- **`unresolved-edges-log.jsonl`** — persistent, multi-stage append log (the
  `stage` field lets normalizer / Haiku-residual / validator all write to it).
  22 rows after this session.
- **`locked-edge-vocab-159.md`** — the printed, self-contained 159-vocab
  reference. Matt's instruction: the final Opus review should "go straight to the
  edge names" — open one prompt, see the problem edge and the full 159-type menu
  side by side, pick. No reading architecture.md or the classification manual.
  Regenerable via `--dump-vocab`.

## Sequencing decision

Matt chose **prevention first**: inline the vocab into the classify prompt before
the residual-resolution pass — Haiku invents fewer types across the whole
~1017-batch bulk, shrinking the residual at the source.

## Next session

`progress/continue-prompts/2026-05-19-stage4-haiku-normalize-and-residual.md` —
STEP 1 prevention, STEP 2 residual pass, STEP 3 targeted Opus review, STEP 4
validator-to-log, then the run/compare/harden/scale loop.
