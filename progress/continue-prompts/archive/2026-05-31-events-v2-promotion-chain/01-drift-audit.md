# Step 1 — Drift-detection cross-model audit (Events Haiku bulk)

> **Recommended model:** Sonnet 4.6 for the re-classification work; Opus 4.7 for interpreting the agreement-rate numbers + the go/no-go judgment. **Read-and-write** allowed (writing audit artifacts, sample files, reports). **Do NOT promote** anything to `graph/edges/`.
>
> **Trust `worklog.md` over this prompt** if they disagree (CLAUDE.md #9).

## Prerequisite

- Events Haiku bulk run is **complete** — 1,617 typed edges across 5 books in `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk/`.
- Analysis report exists at `working/audits/events-haiku-bulk-2026-05-29/analysis.md`. Read §§ 1-6 of that report before starting.

## Why this step exists

Memory rule `feedback_drift_detection_mandatory.md`: every Stage 4+ bulk run gets a cross-model audit before any promotion. The validation gates during the run watched reject-rate floors; this step adds the missing precision check on the **emits themselves**.

We need confidence that Haiku's typed edges agree with a stronger judge on a stratified sample. If they don't, the v1.3 → v2.0 layering would inject noise.

## What to do

1. **Pick a stratified sample of ~50 emits** from `_events-haiku-bulk/{book}/*.edges.jsonl`:
   - 10 from each of the 5 books (proportional to book emit counts, not flat — agot has fewer emits than asos, weight accordingly).
   - Stratify across edge types: ≥3 from each of TRAVELS_WITH, COMMANDS, TRAVELS_TO, LOCATED_AT, SERVES, REVEALS_TO; the remainder random across the long tail.
   - Seed the random draw (e.g., `seed=531`) so the sample is reproducible.
   - Write the sample to `working/audits/events-haiku-bulk-2026-05-29/audit-sample-50.jsonl`.

2. **Re-classify each sample row with a fresh judge — Option B (`claude -p` subprocess), DECIDED.** Written as a small **throwaway ~150-line single-purpose script** at `scripts/events-drift-audit.py` (do NOT generalize this into a reusable drift-audit framework — future drift audits have different vocabs/samplers/prompts; a single-purpose script is correct, a framework is overbuild). The script:
   - Loads the v5-precision-rules prompt via canonical extraction (`scripts/build-edge-type-counts.py` for the locked vocab, prompt body from the same source the bulk classifier used — `prompt_sha=d31ca56c4768`).
   - Fires `claude -p` per row (or batched ~10/call) with `cwd=/tmp` and Sonnet 4.6 as the judge.
   - `--dry-run` default (per the project's cost-gate convention; matches `stage4-tail-classifier.py`); requires `--apply` to actually spend.
   - Writes the metadata header (see step 3 below) plus per-row `(edge_type | reject)` decisions to `audit-sample-50-judged.jsonl`.

   **Why Option B, why script-not-Agent (this is the load-bearing reasoning — don't substitute):**
   - **Prompt-loading parity.** An Agent subagent in this session inherits ~28k tokens of project CLAUDE.md + the parent's tool surface — context the Haiku-cwd=/tmp bulk run never saw. That contaminates the audit: it measures setup-vs-setup, not model-vs-model.
   - **Tool access biases the judge.** A Sonnet subagent with Read/Grep is a *stronger* judge than Haiku had access to (could consult architecture.md, look up neighbor edges, read the chapter file mid-decision). That biases agreement *downward* artificially. Only `cwd=/tmp` enforces parity with Haiku's bulk-run conditions.
   - **Drift-detection memory rule** (`feedback_drift_detection_mandatory`): same agent + cache reset ≠ same output schema; reproducibility requires the cwd-isolated subprocess, not the in-context Agent.
   - **Cost is NOT the reason.** ~50 rows × ~$0.0003/row = pennies; the 49% `cwd=/tmp` saving matters for 16k-row bulks, not a 50-row audit. Don't lean on the cost argument when surfacing to Matt — lean on parity.

   Option A (Agent subagent) buys one thing B doesn't: a session-visible transcript Matt can eyeball. Step 4 below (manual inspection of 5 high-disagreement rows) covers that need without contaminating the rest of the audit.

3. **Compute agreement rates** (in the same `events-drift-audit.py` script):
   - **Triple-level**: same `(source_slug, edge_type, target_slug)` → agreement.
   - **Pair-level**: same `(source_slug, target_slug)` regardless of type → agreement.
   - **Reject-vs-emit**: if Haiku emitted and judge rejects (or vice versa), tag as "disagree-shape".
   - Compute per-edge-type agreement too — surface any edge type with <50% agreement separately.

   **Provenance metadata — REQUIRED** (per memory `feedback_verify_dataset_provenance`; the audit is itself un-auditable without it). Every output file (sample, judged, report) must carry a header with:
   - `judge_model` (e.g. `claude-sonnet-4-6`)
   - `judge_prompt_sha` (must equal `d31ca56c4768` — same as Haiku's bulk run; if not, stop and ask Matt)
   - `judge_cwd` (must be `/tmp`)
   - `sample_seed` (e.g. `531`)
   - `timestamp` (ISO 8601 UTC)
   - `judged_count` / `judged_cost_usd`
   - `chain_step` (`01-drift-audit`)
   - `script_path` + `script_sha` (so the script-version that produced the audit is recoverable)

4. **Sample-inspect 5 high-disagreement rows manually.** Sometimes the judge is wrong; we want to know which side is the drift before reading the number.

5. **Write the audit report** to `working/audits/events-haiku-bulk-2026-05-29/cross-model-audit.md`. Include:
   - Sample selection methodology + seed.
   - Re-classifier setup (Option A or B), prompt sha, model.
   - Agreement-rate table (overall + per edge type).
   - The 5 manually-inspected high-disagreement cases with verdict.
   - **Go/No-Go recommendation** against the gates below.

## Gates (publish in the report)

- **Go**: triple-level ≥70% AND pair-level ≥85% AND no edge type with <50% triple agreement and >5 samples.
- **No-Go**: anything else → escalate to Matt with the specific failure pattern; do NOT proceed to step 2.
- **Borderline (70-75% triple)**: surface to Matt with the manual-inspection findings; Matt decides.

## Deliverables for step 2

- `scripts/events-drift-audit.py` — the throwaway audit script (committed; serves as the audit-script-of-record).
- `working/audits/events-haiku-bulk-2026-05-29/audit-sample-50.jsonl` — sample selection with metadata header.
- `working/audits/events-haiku-bulk-2026-05-29/audit-sample-50-judged.jsonl` — Sonnet-judge decisions per row.
- `working/audits/events-haiku-bulk-2026-05-29/cross-model-audit.md` — the report with agreement-rate table + manual-inspection notes + Go/No-Go.
- `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/step-01-status.md` — one-page "ran on date, agreement = X%, Matt's verdict = Y, proceed to step 2 = yes/no".

## Hard rules

- **Do NOT modify** anything under `graph/`.
- **Do NOT re-launch** the Events bulk classifier.
- **Do NOT** use the bulk-run output as input to itself — that's circular.
- **Always confirm with Matt before invoking `claude -p` subprocesses** that will incur cost (per `feedback_no_extraction_without_asking.md`). The script defaults to `--dry-run`; require `--apply` + explicit Matt-go for actual spend.
- **Do NOT generalize `events-drift-audit.py` into a reusable framework.** It's a 150-line throwaway. Future drift audits will have different prompts/vocabs/samplers and want their own scripts. Resist the urge.
- **Do NOT use an Agent subagent for the judge step.** The whole point of `cwd=/tmp` is prompt-loading parity with Haiku's bulk-run conditions; an Agent subagent inherits ~28k tokens of project CLAUDE.md + tools Haiku never had access to, contaminating the audit. The Agent route is reserved for step 4 (manual high-disagreement inspection), where session context is desirable.

## Why we picked this gate (for posterity)

The validation gates during the bulk run (reject_rate floor=0.7) caught drift on rejection patterns but didn't validate emit-precision. The 70% triple / 85% pair floors are calibrated from the S69 smoke runs: Sonnet vs Haiku on Events scored ~85% AGOT / ~90% ACOK strict on 2 fresh samples — so we expect ≥85% pair / ≥70% triple here too. Below those, we're in territory where the Haiku output isn't trustworthy enough to ship.
