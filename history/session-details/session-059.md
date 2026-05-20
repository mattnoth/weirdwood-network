---
session: 59
date: 2026-05-19
model: Opus 4.7 (orchestrator)
purpose: Fire the Stage 4 Haiku smoke — which evolved into building a separate Haiku worker and planning a Python re-architecture.
---

# Session 59 — Stage 4 Haiku Worker: Smoke → Separate Worker → Re-architecture Plan

## Starting point

Opened as the watcher for the `2026-05-19-stage4-haiku-smoke-fire` mission. The handoff: verify the batch-0020 Opus audit completed, read its Section 5 verdict, then fire the Haiku smoke.

## The audit that never ran

The batch-0020 Opus audit's output file did not exist and no audit process was running. Re-launched it as a background agent. (Later in the session Matt pasted terminal scrollback revealing why the original failed: it was launched from `/Users/mnoth/source` instead of `/Users/mnoth/source/asoiaf-chat`, so `cat` couldn't find the continue prompt → empty `-p` argument → `claude` errored instantly. It never started.)

The re-run finished in ~5 min. **Verdict: "needs prompt change first."** A stratified 50-emit sample of batch-0020's KNOWS edges found 0 correct. Root cause: KNOWS is the frictionless emit. Fix: **R1** — a Pattern-5 KNOWS STOP rule + a `KNOWS → character.*` type contract. R2/R3 are companion rules.

## R1/R2/R3 applied

A Sonnet agent applied R1 (Pattern 5 + KNOWS type-contract row), R2 (co-presence centralized rule), R3 (qualifier self-check) to `.claude/agents/prose-edge-classifier.md`.

## The harness problem

The plan was to fire the smoke through the existing Sonnet worker (`stage4.sh` + `worker-stage4.md`). It can't be used: that worker prompt makes the LLM do all batch bookkeeping and writes output to the same paths as the Sonnet control arm. Matt cut through the over-engineering — archive the Sonnet output, run Haiku, compare. Archived batch-0020's 30 Sonnet edge files; registered a fresh `batch-0020-haiku-smoke` id to sidestep the worker's resume-check.

The smoke run then exposed the real finding: **Haiku cannot drive the Sonnet worker harness.** Two invocations, two failure modes — invocation 1 did 3/30 files then early-exited; invocation 2 skipped the resumable batch, claimed the wrong (live-queue) batch, and stopped to ask the human a question. Haiku's *classification* on the 3 files it did was clean (0 KNOWS-fallback — R1 working); its *agentic operation of the bookkeeping* failed.

## The separate Haiku worker

Built a Haiku worker, kept fully separate from the Sonnet specs (Matt's hard constraint):
- `scripts/stage4-haiku-run.py` — Python orchestrator: all bookkeeping (batch selection, chunking, parallel invocation via `--concurrency`, rate-limit detection, provenance snapshot, results/run-summary JSON). Output → `prose-edges-haiku/`.
- `.claude/commands/stage4-haiku-classify.md` — thin classify-only prompt.

batch-0020 runs: chunk-3 sequential $2.99 / 28.5 min; chunk-10 ×3 parallel (post-hardening) **$1.86 / 5.7 min, 30/30, 0 failures** — Haiku completed full 10-file chunks.

## Drift catalogue + hardening

Validator on the chunk-3 run: 46 violations (16%), dominated by `qualifier-required-missing` ×38. A hardening pass inlined a `## CRITICAL RULES` section into the classify prompt (Tier-1 qualifier-enum table, KNOWS STOP, qualifier≠direction, no-invented-types, type contracts).

Hardened chunk-10 run: **fixed** `qualifier-required-missing` (38→0) and cut `KNOWS` (60→16), but **exposed** `edge-type-not-canonical` ×26 (Haiku invents type-name variants — `TRAVELED_TO` for `TRAVELS_TO`) and `type-contract-violation` ×21. Net ~17.5%. Lesson proven twice: **Haiku obeys rules whose data is inlined; it ignores rules that point at the manual.**

## Cost analysis

chunk-3 Haiku cost ~$3/batch — basically Sonnet's price, because each chunk re-reads the classifier-manual context. chunk-10 cut it to $1.86. The deeper lever: the worker reads files via tool calls — each is a turn re-sending context. The Sonnet worker quietly violated the project's `python-before-agent` rule the whole time; Haiku's failure merely *exposed* a pre-existing inefficiency. Fix: pre-loading architecture — Python reads files and injects content into the prompt; Haiku does pure text-in/text-out.

## Model-provenance scare

Matt worried a Sonnet control-arm batch had secretly run on Opus. Investigated: all 32 Sonnet-mission run-logs say `claude-sonnet-4-6`; cost outliers are Sonnet-priced ($8.65 batch with 206K output ≠ Opus economics). Real gap surfaced: model is recorded ONLY in run-logs — not in `timing.jsonl`, `results/`, or the manifest. Conclusion: control arm is all-Sonnet; the early-batch script churn (sleep, files-per-batch) is just imperfectly recorded.

## Decisions

- **Haiku is the Stage 4 bulk worker; Sonnet is off the table** (cost — ~1017 batches). Memory `project_stage4_haiku_not_sonnet` saved. The vocab lockdown's whole purpose was to make Haiku viable.
- **The Haiku worker stays separate** from the Sonnet worker — separate scripts, output dir (`prose-edges-haiku/`), mission dir (`2026-05-19-stage4-haiku/`).
- **Speed-first; imperfect output acceptable** — Opus watcher catches residual drift live, mechanical-extraction enrichment backstops quality. Harden the prompt once, don't perfect it.
- **Next: Python re-architecture** to minimize Haiku's job (pre-loading, Python writes output, inline vocab, type-normalizer — Python-first, model only for residual), then an expanded smoke on Sonnet-done batches, then scale to the queue.

## State at session close

- 8-batch Haiku wave running in background (first 8 queued batches, chunk-15, concurrency-8) — task `b2pg0630m`. Next session reads `working/missions/2026-05-19-stage4-haiku/run-summary.json` for its results.
- Continue prompt: `progress/continue-prompts/2026-05-19-stage4-haiku-run-batches.md`.
