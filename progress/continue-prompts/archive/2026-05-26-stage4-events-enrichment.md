# Edge enrichment with Events — precision-gated

> **Recommended model:** **Opus 4.7** as conductor (gate decisions, precision review). **Sonnet 4.6** (via script-builder) for the $0 deterministic builds (temporal scoping, conflict-pair correction application, candidate prep). **Haiku 4.5** is the bulk typing worker IF and only when the gate clears (`project_stage4_haiku_not_sonnet`).
>
> **Trust `worklog.md` over this prompt if they disagree** (CLAUDE.md #9). Authoritative state: worklog Session 75 entry + the Session-74/75 Active Decisions. Note: older Stage-4 continue prompts may still say edges=3,842 — STALE; it's **3,811 v1.3**.

> **⚠️ STATUS (updated S76, 2026-05-27):** Step 1 precursors are **DONE** (temporal scoping built — 31/32 conflicts are arcs; conflict-pair review — only 2 `cersei↔tyrion` LOVES are real mis-types; v5 wired). Step 2 is **IN PROGRESS**: Matt relaxed the hard 75% gate to a monitored iterative loop and the Events run launched on Sonnet (75/415 batches, ~82-86% strict, paused on a rate-limit wall). **The live next action is the Haiku-vs-Sonnet model decision** → `progress/continue-prompts/2026-05-27-haiku-events-comparison.md`. Trust `worklog.md` Session 76 over the steps below.

## Why this track exists

Matt wants to **enrich the graph beyond the shipped deterministic core**, step by step, with **Events as the next surface** (2026-05-26, Session 75 — softens the S74 "enrichment NO-GO" to a *deferral*). Memory: `project_enrichment_wanted_events_next`.

But Matt set a gate: enrichment happens **only after "the recommended changes before we do that take effect."** Those precision precursors come first in this track, THEN the Events pass.

## State you inherit

- **Shipped core:** `graph/edges/edges.jsonl` = **3,811** cited deterministic `book-pass1` edges (v1.3, committed). Citations re-grounded S74. 0 orphans, 100% traversable.
- **Events candidates already generated (S69):** ~**20,321 untyped** Events candidate rows live in the `_extra-tables/` staging (see `working/wiki/data/pass1-derived-extra-tables-report.md` + the S69 worklog/archive015 entries). They are locator-anchored to `sources/chapters:line`. Canonical spine untouched by these.
- **Events smoked at ~60-66% strict precision (S69), SYSTEMATIC failures** — fan-out ~18%, direction-error ~7%, bare-slug ~15%. The full bulk was re-baselined to **~$270-290 / 3-4 days** and **NOT launched**.
- **v5 precision rules** are authored + kept (NOT run): `scripts/stage4-tail-classifier.py`, `prompt_version=v5-precision-rules` (R1 direction-lock, R2 evidence-supports-both-endpoints, R3 target-category, R4 state-not-moment, R5 temporal-phase, R6 no-analytical-from-moment).
- **Conflict-pair audit (S75):** `scripts/graph-conflict-pairs.py` → `working/wiki/data/graph-conflict-pairs.{md,jsonl}`. 32 flagged pairs (mostly legitimate temporal arcs; a handful are true mis-attributions, e.g. `catelyn-stark → tyrion-lannister` TRUSTS sourced from a Jaime/Cleos-Frey line).
- **Query tool (S75):** `scripts/graph-query.py` — `--neighbors`/`--path`/`--health` for exercising results.

## Step 1 — Precision precursors (the gate Matt set), all ~$0 deterministic

1. **Apply the true mis-attributions from the conflict-pair queue.** Read `working/wiki/data/graph-conflict-pairs.md`. The 14 same-direction conflicts are the candidates; most are real temporal arcs (KEEP), a few are genuine mis-attributions/wrong-pair/wrong-direction (CORRECT). Show Matt before/after for any edge change; do NOT bulk-delete. This lifts core precision before layering.
2. **Build deterministic temporal scoping** — the high-value structural fix Matt called "shrewd." Every edge carries `evidence_book` + `evidence_chapter`; chapter frontmatter (`sources/chapters/<book>/<file>.md`) carries `chapter_number` (global in-book reading order). Derive a `(book_order, chapter_number)` temporal key per edge and annotate edges with it (book_order: agot<acok<asos<affc<adwd). Then re-run a **temporal-aware conflict audit**: incompatible types in DIFFERENT time windows = resolved arc (not a conflict); only SAME-window incompatibilities are true conflicts. This should shrink the 32 sharply and is the foundation for "when does this edge apply" queries. New script (e.g. `scripts/stage4-edge-temporal-scope.py`) + tests; do not silently mutate `edges.jsonl` without showing Matt.
3. Confirm v5 rules are wired for the Events typing path.

## Step 2 — Events pass (gated; only after Step 1 + a fresh smoke clears)

- **Re-smoke Events on ≥2 fresh OUT-OF-SAMPLE batches with the v5 rules** (drift-detection mandatory — `feedback_drift_detection_mandatory`, `feedback_fresh_review_and_out_of_sample`). Cheap (~$3-4).
- **Gate: ≥75-80% strict precision, stable across both samples.** If it clears, scope the Events run (Haiku worker, run-forever wrapper `scripts/stage4-run-forever.sh`, drift validator + cross-model audit). If it does NOT clear, STOP and report — do not run the bulk.
- Merge typed Events edges into `graph/edges/` via the formalize convention (`scripts/stage4-formalize-edges.py` lineage), with the endpoint/direction filters that the S69 smokes showed are required.

## DO NOT
- Run the ~$270-290 Events bulk **blind** — it failed the 75% gate at ~62-66%. Step 1 + a clearing re-smoke come first.
- Bulk-delete conflict-pair edges (sentiment legitimately coexists across books — temporal scoping resolves most).
- Modify `graph/edges/edges.jsonl` without showing Matt before/after.
- Run `/endsession` without explicit permission.

## Final step
Write `working/session-results/<date>-events-enrichment.md` (gate result + headline numbers + what's next) and update worklog + todos.
