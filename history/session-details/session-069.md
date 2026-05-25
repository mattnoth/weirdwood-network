---
session: 69
date: 2026-05-24
title: "Stage 4 recall expansion — table-mining smokes, two reviews, held at the spend gate"
model: Opus 4.7 (orchestrator) · Sonnet 4.6 (script-builder, the two smokes, both prose-edge-reviewer audits)
---

# Session 69 — Stage 4 recall expansion: smokes + reviews, held at the $270 gate

## Purpose

Continue the Stage 4 recall-expansion track (`/continue stage4-recall-expansion`). The
prior session (68) had mined the four remaining Pass 1 relational tables and surfaced a
tension: the highest-recall tables (Events & Actions, Information Revealed) are
prose-shaped and need an LLM pass (~$95+ originally estimated), while only Hospitality
gave free deterministic edges. This session's job was to price and de-risk that LLM pass
*before* committing to it, and — per Matt's mid-session decision — to type all four
tables (Dialogue, Events & Actions, Information Revealed, Food & Drink) before formalizing
edges into `graph/edges/`.

## What Matt decided, live, during the session

This was a conversational session — Matt was learning the shape of the work ("my first
graph", working sporadically) and steering as he went. The decisions that landed:

1. **Commit S68** (proper message, not a wip) — done first.
2. **Smoke before spending** — the staged, Python-first approach. "Always whatever we can
   script python to make the LLM jobs easier."
3. **Type all four tables before formalizing**, including Food (a first-class target by
   his design values) and fights (which are Events, so the Events generator covers them).
4. **A full source-chapter re-read is NOT feasible before landing** — get traversal
   working on table-mined edges, enrich later. This is the crucial distinction: *table
   mining* (cheap, built on existing extractions) is in-scope now; a *full book re-read*
   is deferred. He affirmed the additive "build then enrich" model.
5. He stepped away with "run with it… spawn a fresh agent if you need a second eye,"
   authorizing the smokes ($1-2 each) and autonomous execution, with the ~$270 full run
   held for his return.

## A teaching thread worth preserving (the "Events & Actions" confusion)

Matt was confused that the recall-sample ranked **Events & Actions as the #1 recall
table** while the extra-tables report listed it as **"counted-only, 0 edges."** The
reconciliation — and the mental model the whole pivot rests on — is **table shape**:

- Columnar tables (Hospitality: host/guest/qualifier) → Python gets pair *and* type
  deterministically ($0). That's why Hospitality gave 529 free edges.
- Dialogue (speaker/listener columns) → Python gets the *pair* free; type needs an LLM.
- Events/Info/Food (free-text prose) → neither pair nor type is cleanly extractable;
  both need an LLM, *and* a new candidate generator to pull entity pairs out of prose.

So Events & Actions is the highest *recall* table precisely *because* it's a broad
free-text catch-all — which is the same reason it's the *least* cheaply mineable. Highest
value, highest cost, same root cause.

Matt also made a sharp observation that improved the pipeline: the Pass 1 tables are
themselves **lossy** (the extractor chose what dialogue/meals were "of note"), so
table-mining has a ceiling *below* true chapter content — and the citation should point
at the **real chapter line**, not the table. Verification showed the locator
(`stage4-pass1-evidence-locator.py`) already cites `sources/chapters/{book}/{chapter}.md:line`
(quote is just the search key; 98.8% verbatim-matched on the spine). But the S68
extra-tables rows had NOT been through the locator — so anchoring them became a build
requirement this session.

## What was built and run

- **script-builder (Sonnet, background)** extended `scripts/stage4-pass1-extra-tables.py`
  with candidate generators for Events & Actions / Information Revealed / Food & Drink
  (entity-name matching via the resolver, ≥2-entity filter, first-actor fan-out for
  direction), ran the locator over all `_extra-tables` rows for `evidence_ref`
  anchoring, and smoke-enabled `scripts/stage4-tail-classifier.py` to read `_extra-tables`
  rows with the ENCOUNTERS Rule-6 verb-gate added to the prompt + a `--sample-n` stratified
  smoke mode. 189 tests passing.
- **Candidate counts (`--apply`):** 32,194 untyped rows — Dialogue 4,422 / Events 20,321
  / Info 6,653 / Food 798 — plus the 529 deterministic Hospitality edges. The Events
  fan-out (7,128 rows → 20,321 pairs) re-baselined the full-run cost.
- **Two ~200-row smokes** (Sonnet via `claude -p`): Dialogue 144 typed (72%) / 56 rej /
  $1.68; Events/Info/Food 123 typed (61%) / 77 rej / $1.89. ~$0.009/row measured (vs the
  $0.0068 S67 estimate). Each 40-row batch took ~5-7 min → full run ≈ 805 batches ≈
  3-4 days sequential.
- **Two independent prose-edge-reviewer audits** (Sonnet). Both verdicts: **SYSTEMATIC.**

## The two bugs found (both via doing, not via the green tests)

1. **Output-collision hazard:** the tail-classifier *appends* to `OUT_BASE =
   _tail-typed/`, which is the canonical S67 typed-tail (2,385 edges, pending merge). A
   `--apply` smoke would have polluted it. Fixed by adding an `--output-dir` flag (+
   `.resolve()` + a defensive `relative_to` guard after a relative-path crash on the
   first smoke) + a redirect test. Canonical row counts verified unchanged all session.
2. **Provenance bug:** `build_emit_edge_row` (`stage4-tail-classifier.py:502`) hardcodes
   `candidate_kind: "pass1_relationship"` on every emit — so Dialogue/Events/Info/Food
   provenance is lost on the edge. NOT yet fixed (queued in the continue prompt).

Both reinforce the standing "green tests are not correctness" discipline — the build's
189 tests passed while missing both.

## Quality findings (the decision input)

| | Dialogue (144) | Events/Info/Food (123) |
|---|---|---|
| Strict precision | ~60% | ~66% |
| Weak | ~28% | ~22% |
| Wrong | ~11% | ~12% |
| Reject precision | ~89% | ~91% |
| Direction errors | — | ~7% |
| Fan-out spurious pairs | — | ~18% |
| Bare/garbled slugs emitted | several | ~15% |

Three fixable problem classes, all $0:
1. **Prompt over-types** `INFORMS` (~100% wrong — it's a spy→handler type, used
   generically), `ADVISES`, `MANIPULATES` (applied to overt threats; def needs the target
   unaware), `SUPPORTS` (evidentiary type misused interpersonally), `ALIAS_OF` (title
   forms). Uniform Tier-1 on 100% of edges.
2. **Generator** direction-heuristic + fan-out + bare-slug emission — the same
   `all-for-joffrey` endpoint-pollution class flagged on the 529 Hospitality edges. One
   fix (direction-validation + slug-quality escalation gate) cleans both.
3. **The `candidate_kind` provenance hardcode.**

Encouraging: ~90% reject precision (good at knowing what NOT to emit), and the
relationship-revealing types (`SIBLING_OF`, `KILLS`, `VOWS_TO`, `DUELS`, `REVEALS_TO`,
`CONSPIRES_WITH`, `FIGHTS_IN`…) are solid. The pipeline is sound; the freestyle surfaces
just need locking down — exactly the "lockdown before long passes" rule.

Reviewer table-productivity read: Events most productive, Information Revealed noisiest
(defer it from first run), Food lowest-signal (separate small audit).

## Outcome / decision

**Held at the spend gate.** The ~$270 full run was NOT launched. Recommendation: do the
three $0 fixes → re-smoke (~$4) to confirm ≥80% precision → then decide a *scoped* full
run (Events + Dialogue first; Info deferred; Food separate) via the parallel wrapper →
then formalize into `graph/edges/` (the long-pending milestone, which also absorbs the
S66/S67 merge/dedup/resolver-lever work).

Three decisions left for Matt: (A) restricted typing vocabulary + anti-patterns;
(B) first-run table scope; (C) full-run approval after the re-smoke.

## Artifacts

- `STAGE4-SMOKE-REVIEW.md` (repo root) — Matt's plain-language review.
- `working/wiki/data/pass1-derived-smoke-report.md` — technical report.
- `progress/continue-prompts/2026-05-25-stage4-smoke-fixes-and-formalize.md` — next session.
- Smoke output (gitignored): `pass1-derived/_smoke-dialogue/`, `pass1-derived/_smoke-events-info/`.
