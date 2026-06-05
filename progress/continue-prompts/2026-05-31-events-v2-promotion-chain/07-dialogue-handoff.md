# Step 7 — Hand-off to Dialogue bulk run (v2.1 prep)

> **Recommended model:** Opus 4.7 for planning + smoke-test design. The actual Dialogue bulk run will be Haiku-driven (per `project_stage4_haiku_not_sonnet`) but the prep work needs judgment.
>
> **Trust `worklog.md` over this prompt** if they disagree.

## Prerequisite

- **Step 6 status file** shows v2.0 is **committed** to `graph/edges/edges.jsonl`.
- `graph/edges/README.md` Roadmap section calls out Dialogue as the next layer.

## What this step does

This isn't really an "execution" step — it's a planning + smoke-test step that sets up the next bulk run (Dialogue) using everything we learned from Events. The output is a continue-prompt chain for the Dialogue work, parallel to this one.

## Why this step exists

`graph/edges/README.md`'s v2 roadmap was always **Events + Dialogue together**. We split them because shipping Events-only as v2.0 was lower-risk. The Dialogue half is the next layer, slated as v2.1.

Matt's note (2026-05-31): "dialog thing is next after promotion."

The Dialogue source candidate kind is `pass1_dialogue` (or similar — verify against `_extra-tables/` rows). It's structurally the same shape as `pass1_events`: high-recall candidates from Pass 1 dialogue tables, each candidate a potential typed relationship between speaker and addressee (or speaker and subject of speech).

## What to do

1. **Audit the Dialogue candidate pool.** Run a count across `_extra-tables/{book}/*.extra-tables.jsonl`:
   - How many rows have `candidate_kind == "pass1_dialogue"` (or whatever the exact kind name is)?
   - Per-book distribution.
   - Slug-resolution status counts (resolved-exact / resolved-context / tail-llm / unresolved).
   - **Write to** `working/wiki/pass2-buckets/pass1-derived/_dialogue-prep/candidate-pool-stats.md`.

2. **Review Events run learnings that apply to Dialogue:**
   - Vocab lockdown (v5-precision-rules, sha `d31ca56c4768`) — should Dialogue use the same prompt or does it need its own variant?
   - Reject-rate expectation (Events landed at ~90% — Dialogue might be similar or higher; dialogue lines often reveal nothing typed).
   - **Schema gap noted in §5 of analysis:** rejected rows have no `reject_reason`. Fix this in the classifier **before** the Dialogue bulk run, since per Matt this is the "fix-later in Dialogue prep" decision (project README of this chain).
   - Wrapper bug (count_remaining) — already patched (Session 80, 2026-05-31).
   - The recurring parse-fail batch (S79 loose end) — apply the fix queued in `working/todos.md` Stage 4 section (make `classify_failed` a skip-key or one-shot retry).

3. **Design a Dialogue smoke test.** Before any bulk launch:
   - Pick ~50 dialogue candidates stratified across books and speaker-types.
   - Run them through Haiku with v5-precision-rules (or a dialogue-tuned variant).
   - Strict precision read by Opus.
   - Bar to launch bulk: ≥85% strict precision on the smoke sample (same bar as Events S69).

4. **Write a new continue-prompt chain** at `progress/continue-prompts/<date>-dialogue-v2.1-chain/` modeled on this Events chain (README + 6-7 step prompts). The Dialogue chain mirrors steps:
   - Smoke test (new — Events skipped it because we had the S69 sonnet/haiku comparison)
   - Bulk run + monitor (mirrors the Events bulk monitor at `progress/continue-prompts/2026-05-27-events-haiku-bulk-monitor.md`)
   - Cross-model drift audit (mirrors step 1)
   - Extend formalize-edges.py to add DIALOGUE-HAIKU as a 5th source (mirrors step 2)
   - Type-contract validation (mirrors step 3; dialogue introduces edge types like REVEALS_TO, INFORMS, ADVISES, TELLS — many already in events output, but the source semantics differ)
   - Resolver pass (mirrors step 4)
   - Precision audit (mirrors step 5)
   - Promote v2.0 → v2.1 (mirrors step 6)

5. **Surface to Matt**:
   - Candidate pool size + per-book distribution.
   - Smoke-test design + cost estimate.
   - Reject-reason schema fix design (a short doc; classifier should write `reject_reason: <enum>` going forward).
   - Parse-fail fix design.
   - Proposed timeline.
   - **Wait for go before launching anything.**

## Gates

- **Go to Dialogue bulk launch**: smoke-test precision ≥85% strict on stratified sample; schema fixes landed; Matt approves the budget + timeline.
- **No-go**: surface what failed and pause.

## Deliverables

- `_dialogue-prep/candidate-pool-stats.md`
- `progress/continue-prompts/<date>-dialogue-v2.1-chain/` — new chain directory with README + step prompts.
- Classifier-script edits for `reject_reason` and parse-fail handling (committed before launch).
- `step-07-status.md` — closes out this chain, points to the new Dialogue chain.

## Hard rules

- **`feedback_no_extraction_without_asking.md`** — never launch the Dialogue bulk without Matt's explicit go.
- **Drift detection mandatory** — even though we just did this for Events.
- **Vocabulary remains locked.** Dialogue uses the existing 163-type vocabulary; no new edge_type strings without a separate design conversation.
- **Same precision floor as Events** for the smoke (85% strict). Lower bars only with Matt's explicit approval.
