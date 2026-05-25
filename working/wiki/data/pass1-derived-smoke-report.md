# Stage 4 Pass-1-Derived — Dialogue + Events/Info/Food Smoke Report

> Generated: Session 69 (2026-05-24/25). Decision input for the ~$270 full-run call.
> Smokes: Sonnet via `claude -p`, 200 rows each, output in gitignored scratch dirs
> (`pass1-derived/_smoke-dialogue/`, `pass1-derived/_smoke-events-info/`).
> Canonical `_tail-typed/` (2,385 S67 edges) was NOT touched (verified by row-count).

## TL;DR — verdict

**Do NOT approve the $270 full run on the current prompt + generator.** Both smokes
type at a healthy *rate* but mediocre *precision* (~60-66% strict), with **systematic,
fixable** defects. The smokes did exactly their job. Reject discipline is good
(~89-91%) — the pipeline knows what NOT to emit; the problem is *what it does emit*.

Three $0-to-fix problem classes → fix → re-smoke (~$4) → then decide the full run.

## What ran + measured cost

| Smoke | rows | typed | rejected | $/run | $/row | wall-clock |
|-------|------|-------|----------|-------|-------|-----------|
| Dialogue | 200 | 144 (72%) | 56 | $1.68 | $0.0084 | ~27 min |
| Events/Info/Food | 200 | 123 (61.5%) | 77 | $1.89 | $0.0095 | ~30 min |

**Full-run re-baseline:** 32,194 untyped rows × ~$0.009/row ≈ **$270-290** (not the
~$100 first quoted — the Events fan-out produced 20,321 pairs from 7,128 rows).
**Wall-clock reality:** ~5-7 min per 40-row batch → 32,194 rows = ~805 batches =
**~3-4 days sequential.** A full run needs the parallel `run-forever` wrapper, not a
single chain. So the decision is "$270 **and** a managed multi-day parallel run."

## Quality (both smokes independently audited by prose-edge-reviewer)

| | Dialogue (144) | Events/Info/Food (123) |
|---|---|---|
| Strict precision (correct) | ~60% (87) | ~66% (81) |
| Weak (defensible, thin) | ~28% (41) | ~22% (27) |
| Wrong | ~11% (16) | ~12% (15) |
| Reject precision | ~89% | ~91% |
| Direction-error rate | low | **~7%** |
| Fan-out spurious-pair rate | n/a (pairs are clean) | **~18%** |
| Bare/garbled slugs emitted | several | **~15% of edges** |

The strong types in BOTH: `SIBLING_OF`, `SPOUSE_OF`, `PARENT_OF`, `KILLS`, `DUELS`,
`VOWS_TO`, `DISTRUSTS`, `REVEALS_TO`, `BANISHES`, `BETRAYS`, `CONSPIRES_WITH`,
`FIGHTS_IN`. These are worth keeping. The damage is concentrated in a few types +
the generator.

## The three fixable problem classes

### 1. Classifier prompt over-types specific edge types (all tables, $0 prompt fix)
- **`INFORMS`** — defined as spy→handler ongoing reporting; used as generic "told
  someone something." **~100% wrong** in both smokes.
- **`ADVISES`** — collapsed into "any helpful/forceful speech act" (rebukes,
  arguments, objections). ~30% inflated.
- **`MANIPULATES`** — applied to *overt* threats/provocation; definition requires the
  target be *unknowing*. Several direction errors too.
- **`SUPPORTS`** — evidentiary/theory-layer type misused for interpersonal political
  backing (category error).
- **`ALIAS_OF`** — misused for title forms of address ("King Robert", "Ser …").
- **Uniform Tier-1** on 100% of edges — zero confidence diversity; many are clearly
  Tier-2/3 inferences.
- *Fix:* restrict the permitted vocab for these passes to relationship-revealing types
  + add explicit anti-patterns + tier-assignment guidance. **(design decision — Matt)**

### 2. Events/Info candidate generator — direction + fan-out + slug quality ($0 Python)
- **Fan-out spurious pairs ~18%:** first-actor→all-others fan-out invents edges between
  co-mentioned entities with no real relationship (e.g. `qhorin TRAVELS_WITH ghost`).
- **Direction errors ~7%:** "first-named = actor" fails on passive constructions
  (e.g. `varys MANIPULATES sansa` when Varys is threatening *Ned* via Sansa).
- **Bare/garbled slugs ~15%:** `ser`, `lord`, `king`, `maester`, bare `mormont`
  (Jeor vs Jorah), `marsh-king`, `jorah-stark`, and `alayne` (Sansa's alias) emitted
  at Tier-1 instead of escalated.
- *Fix:* direction-validation step + a slug-quality gate that routes bare
  titles/surnames/demonyms/known-aliases to disambiguation/cross-identity instead of
  emitting. **This is the SAME endpoint-pollution class as the 529 Hospitality edges**
  (`all-for-joffrey` etc.) — do the endpoint filter ONCE for everything.

### 3. Provenance bug — `candidate_kind` hardcoded ($0 one-line fix)
`build_emit_edge_row` (scripts/stage4-tail-classifier.py:502) stamps every emit
`candidate_kind: "pass1_relationship"` regardless of source table — so Dialogue/
Events/Info/Food provenance is lost on the edge. Must preserve the input row's
`candidate_kind` before any real run.

## Table productivity (Events/Info/Food)
- **Events & Actions** — most productive; clean movement/conflict/kinship edges.
- **Information Revealed** — noisiest; multi-entity disclosure rows maximize fan-out
  spurious pairs. Reviewer recommends **deferring it** from the first full run.
- **Food & Drink** — lowest signal; "who ate with whom" rarely graph-worthy. Reviewer
  recommends a **separate audit pass**, not the bulk run.

## Recommended path (ordered; nothing spent until step 5)
1. **[$0, design — Matt's call]** Restrict classifier vocab + add anti-patterns for
   INFORMS/ADVISES/MANIPULATES/SUPPORTS/ALIAS_OF + tier guidance.
2. **[$0, Python]** Generator: direction-validation + slug-quality escalation gate
   (= the endpoint filter; also cleans the 529 Hospitality edges' endpoints).
3. **[$0]** Fix the `candidate_kind` provenance hardcode.
4. **[~$4]** Re-smoke Dialogue + Events (drop Info, hold Food) → confirm strict
   precision ≥ ~80%.
5. **[decision]** Approve the full run (scoped: Events + Dialogue first; Info deferred;
   Food separate) at the measured rate — and only via the parallel `run-forever`
   wrapper given the multi-day wall-clock. Drift-detection mandatory.

## Decisions for Matt
- **A.** Restricted-vocab approach for the typing prompt (which types to keep/drop)?
- **B.** Table scope for the first full run: Events + Dialogue only, Info deferred,
  Food separate-audit? (reviewer's rec)
- **C.** After fixes + re-smoke confirms ≥80% precision, approve the (scoped) full run?

## Housekeeping
- Uncommitted: build-agent changes + my `--output-dir`/resolve/`_rel` edits to the 2
  scripts + their tests (189+84 tests green). The `candidate_kind` + slug-gate fixes
  are NOT yet done. Matt checkpoints.
- Scratch smoke output retained for inspection under `pass1-derived/_smoke-*` (gitignored).
