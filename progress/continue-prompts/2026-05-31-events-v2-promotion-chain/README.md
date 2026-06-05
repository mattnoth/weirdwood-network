# Events Haiku Bulk → `edges.jsonl` v2.0 Promotion Chain

**Chain start date:** 2026-05-31
**Source artifact:** `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk/` (1,617 typed edges from Events bulk run completed 2026-05-29)
**Target artifact:** `graph/edges/edges.jsonl` v2.0 (currently v1.3 @ 3,811 edges)
**Source analysis:** `working/audits/events-haiku-bulk-2026-05-29/analysis.md` — **read this first.**

## How this chain works

Six self-contained prompts. Each one:
- Declares the **prerequisite** (what step N-1 must have left on disk).
- Declares the **deliverable** (what to leave on disk for step N+1).
- Carries a **gate** — surface results to Matt before proceeding to the next step.
- Declares a **Recommended model**.

Trust `worklog.md` over any prompt if they disagree (CLAUDE.md #9).

## Open questions Matt answered up front (kept here so each step inherits the same context)

- **Full re-merge vs. additive overlay?** → **Full re-merge.** Rebuild via `stage4-formalize-edges.py` with EVENTS-HAIKU as a 4th source; one consolidated `edges.jsonl` v2.0.
- **Ship Events-only as v2.0, or wait for Dialogue?** → **Events-only.** Dialogue lands as v2.1 later.
- **`reject_reason` schema gap fix-now or fix-later?** → **Fix-later**, in the Dialogue run prep.
- **Step 1 judge method (Option A Agent subagent vs Option B `claude -p` subprocess)?** → **Option B**, via a throwaway ~150-line `scripts/events-drift-audit.py`. Driven by prompt-loading parity with Haiku's bulk run, NOT by cost. Subagent context inheritance contaminates the audit. See `01-drift-audit.md` step 2 for the load-bearing reasoning.
- **Fleet-action script for the whole chain?** → **No.** Sequential, gated 5-of-7, single-actor-per-step; a pipeline script would be 90% pause-for-Matt boilerplate, a fleet mission adds parallel-worker scaffolding for zero parallelism payoff. Manual continue-prompts + `step-NN-status.md` handoff is correct. (Pressure-tested by fresh general subagent, 2026-05-31.)

*(If Matt revisits any of these mid-chain, update this README + downstream prompts.)*

## The chain

| # | Prompt | Recommended model | Gate |
|---|--------|-------------------|------|
| 1 | [01-drift-audit.md](01-drift-audit.md) — Cross-model + sample audit | Sonnet 4.6 (audit work) + Opus 4.7 (judgment) | ≥70% triple agreement, ≥85% pair agreement → Matt sign-off |
| 2 | [02-extend-formalize.md](02-extend-formalize.md) — Add EVENTS-HAIKU as 4th source | Opus 4.7 (script edit + dry-run interpretation) | Dry-run stats reviewed → Matt sign-off |
| 3 | [03-type-contract-validation.md](03-type-contract-validation.md) — Run contracts on v2 candidate | Sonnet 4.6 (mechanical) | Drop/retype counts surfaced → Matt sign-off |
| 4 | [04-resolver-pass.md](04-resolver-pass.md) — Title-person collision resolver on v2 | Sonnet 4.6 (mechanical) | Resolver diff surfaced → Matt sign-off |
| 5 | [05-precision-sample-audit.md](05-precision-sample-audit.md) — 200-row reviewer audit | Opus 4.7 (precision judgment) | ≥75% triple-level precision → Matt go/no-go |
| 6 | [06-promote-v2.md](06-promote-v2.md) — Replace `edges.jsonl`, update README, commit | Opus 4.7 (sensitive write) | Before/after counts approved → commit |
| 7 | [07-dialogue-handoff.md](07-dialogue-handoff.md) — Set up Dialogue v2.1 chain (Matt's flagged next thing) | Opus 4.7 (planning) | Smoke-test design + schema fixes approved → spawn Dialogue chain |

## Hard rules across the entire chain

- **Never modify `graph/edges/edges.jsonl` without Matt's before/after sign-off** (carried over from the 2026-05-27 chain).
- **Never re-launch the Events bulk classifier** — the source artifact is complete and frozen.
- **Never write into `sources/`** — all outputs go under `working/` or `graph/`.
- **Drift-detection is mandatory** (memory: `feedback_drift_detection_mandatory.md`).
- **`feedback_no_extraction_without_asking.md`** still applies — no agent-launched LLM passes without Matt's go.

## State markers between steps

Each step writes a short `step-NN-status.md` in this chain directory recording what ran, what was found, what's next. The next step reads that status to confirm prerequisites are met. If a status file is missing or contradicts the prompt, **stop and ask Matt**.
