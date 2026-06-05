---
session: 81
date: 2026-05-31  (end-of-session crosses into 2026-06-01 UTC)
model: Opus 4.7 (orchestrator) + general-purpose (fresh-eyes review) + Sonnet 4.6 (judge, via `claude -p`)
title: Events Haiku bulk audit → NO-GO (borderline); fresh-eyes pressure-test corrected the framing
---

# Session 81 — Events Haiku bulk drift audit: chain halted at step 1, fresh-eyes corrected the No-Go framing

## Goal

Run step 1 of the Events v2.0 promotion chain (`progress/continue-prompts/2026-05-31-events-v2-promotion-chain/01-drift-audit.md`): stratified cross-model audit of the Haiku bulk output to gate whether the 1,617 typed edges from `_events-haiku-bulk/` get promoted into `graph/edges/edges.jsonl` as v2.0.

Gates from the prompt: triple-level ≥70 %, pair-level ≥85 %, no >5-sample edge type under 50 %. Below those → No-Go, escalate to Matt, do NOT proceed to step 2.

## Method (decided up front in the chain README)

Option B (`claude -p` subprocess) with a throwaway single-purpose Python script, NOT an Agent subagent — the load-bearing reason is **prompt-loading parity** (an Agent subagent inherits ~28k tokens of project CLAUDE.md plus tools Haiku never had, contaminating the audit), not cost. Wrote `scripts/events-drift-audit.py` (327 lines, sha `576cc815649c`). The script reuses canonical `load_locked_vocab` / `compute_prompt_sha` / `render_classify_prompt` / `invoke_claude` / `parse_batch_response` / `align_batch_output` from `stage4-tail-classifier.py` so the Sonnet judge sees byte-identical preamble + vocab + per-row format as Haiku saw. Custom stratified sampler (≥3 of each of 6 named structural types; remainder proportional by book); 50 rows, seed=531, reproducible.

Hard cost gate: `--dry-run` default; `--apply` required to spend.

## Run

1. **Dry-run** wrote `audit-sample-50.jsonl` (51 lines incl. metadata header). 163-edge locked vocab loaded; prompt SHA computed = `d31ca56c4768` — **byte-identical to the Haiku bulk-run SHA**. Parity confirmed.
2. Matt approved `--apply` via `AskUserQuestion`.
3. 5 batches × 10 rows × Sonnet 4.6 cwd=`/tmp` → **$0.93 total**, all 50 rows judged, wrote `audit-sample-50-judged.jsonl`.

## Result (initial reading — became disputed)

- Triple-level agreement: **48.0 %** (24/50) — floor 70 %.
- Pair-level agreement: **56.0 %** (28/50) — floor 85 %.
- **22/50 Haiku emits (44 %) were rejected outright by Sonnet.**
- Per-type triple: TRAVELS_TO 17 % (1/6), TRAVELS_WITH 0 % (0/4), LOCATED_AT 20 % (1/5), COMMANDS 50 %, SERVES 67 %, REVEALS_TO 67 %.
- Manual inspection of 5 disagreement rows (Asha/Ten Towers from memory, Tyrion mention-of-Pentos in dialogue, Tyrion+Pod co-presence in battle, Jon looking-at-Frostfangs, Sansa-ladder-toward-Fingers): all 5 Sonnet rejections were V5-correct on the face of it.

I wrote `working/audits/events-haiku-bulk-2026-05-29/cross-model-audit.md` with **HARD NO-GO** verdict, root-cause hypothesis (Haiku treating `hint_raw` as evidence on par with `evidence_quote`, violating Rule 4a / V5-R2 / Rule 12), and 5 escalation paths.

## Matt's pushback

> *"I think this Sonnet agent fucked up. I don't want to trust this or make any changes to the results of the run from this Audit. it was shit."*

The contradiction with the S69 smoke tests (~85-90 % Sonnet/Haiku agreement) was real and deserved real diagnosis, not a 48 %-vs-90 % "Haiku obviously drifted at scale" handwave. Spawned a general-purpose subagent for fresh eyes per memory `feedback_fresh_review_and_out_of_sample`. The subagent was instructed:

- Don't read my conclusion document yet.
- Read the v5 rules cold (`stage4-tail-classifier.py` lines 227-441).
- Audit-script methodology check (alignment, parse-vs-REJECT distinction, prompt SHA gate, cost plausibility).
- **Cold-judge 10 Sonnet REJECTs.** Was Sonnet V5-correct, or did it over-reject?
- Locate S69 smoke tests and report what they actually measured.

## Fresh-eyes findings (the real conclusion)

The subagent did the work. Key results:

1. **Audit script has no methodology bugs.** Prompt SHA gate is byte-identical to Haiku's bulk run; `align_batch_output` aligns by model-echoed idx (no off-by-one); parse failures (`jd is None`) correctly distinguished from REJECT (`jd['edge_type'] == 'REJECT'`); $0.93 plausible for 5 × 10-row Sonnet batches with 7-8k preamble.

2. **Cold-read of the 22 Sonnet REJECTs:** judged in depth.
   - ~11 of 22 are **clear V5-correct rejections** — Haiku promoted `hint_raw` to fact (Rule 4a violations), treated co-presence as relationship (Rule 12), promoted "approaches" / "looks at" / "remembers" / "mentions" to TRAVELS_TO / LOCATED_AT (V5-R2 + V5-R1 violations).
   - **~3-4 are clear Sonnet over-rejections** — Matt was partly right:
     - `judge_idx=2` Edmure TRAVELS_WITH Lymond — quote explicitly says "on the march" with a companion list. TRAVELS_WITH carve-out applies. Sonnet wrong.
     - `judge_idx=6` Jaime TRAVELS_TO Harrenhal — quote literally contains "when he came to Harrenhal." Completed past travel. Sonnet wrong.
     - `judge_idx=14` Ramsay REVEALS_TO Roose — quote: Ramsay "dispatched three riders to take word to his lord father." That's REVEALS_TO. Sonnet wrong.
     - `judge_idx=16` Haldon TRAVELS_WITH Duck — co-riders on a journey, defensible.
   - ~7-8 genuinely ambiguous, most leaning V5-defensible-reject under strict reading.

3. **The S69 citation in my audit report was wrong.** Subagent traced the actual smoke session: **S77** (not S69), and the measurement was very different:
   - **S77** measured *hand-read precision by Matt's eye* on the *first 600 fresh candidate rows* of AGOT/ACOK — **both models classifying fresh from candidates**, output ≈ 59-65 emits per book, Matt reading each.
   - "~85 % AGOT / ~90 % ACOK strict" = Matt's hand-read precision.
   - "87.8 % / 84.8 % verdict agreement" = Sonnet-emits-or-rejects matches Haiku-emits-or-rejects on row-by-row basis (where most rows are rejects on both sides — agreement on REJECTs is cheap).
   - **This audit** measured Sonnet *judging Haiku's emits-only*, stratified to *over-weight* the named structural types where the failure modes concentrate.
   - The two measurements aren't comparable. The apparent "smoke said the opposite" contradiction is measurement-shape, not drift.

4. **Adjusted numbers** (crediting all 3-4 over-rejections AND all 7-8 ambiguous to Haiku): adjusted triple agreement ≈ 56-70 %, **at or below the 70 % gate**. No-Go still stands, but it's borderline, not catastrophic.

## Final verdict

**NO-GO (borderline)** — do not promote Events Haiku bulk to `edges.jsonl` v2.0 as-is. Named-type precision (TRAVELS_TO, TRAVELS_WITH, LOCATED_AT especially) is real-and-systematic Haiku drift on Rule 4a / V5-R2 / Rule 12, the failure modes V5 was supposed to prevent. Promoting the bulk would inject systematic noise into the named types that make up the bulk of the run, EVEN AFTER crediting Sonnet's over-rejections.

But: it's *borderline*, not the 48 %-was-a-disaster framing my report carried. Sonnet did over-reject on a meaningful minority of cases. Option (C) in the audit — Sonnet-filter the named-type rows only (~700 rows of TRAVELS_TO/WITH/LOCATED_AT/COMMANDS/OPPOSES, ~$2-5 spend) — is the right-shape escalation. Option (D) (prompt-tighten + re-Haiku) is risky because V5 already named these failure modes and Haiku ignored them.

## Artifacts (all under `working/audits/events-haiku-bulk-2026-05-29/` unless noted)

- `scripts/events-drift-audit.py` (sha `576cc815649c`) — throwaway, single-purpose; reuses canonical prompt-renderer + claude -p invocation.
- `audit-sample-50.jsonl` — 51 lines (metadata + 50 sampled emits, seed=531).
- `audit-sample-50-judged.jsonl` — 51 lines (metadata + 50 judge decisions).
- `cross-model-audit.md` — full audit report; amended with fresh-eyes corrections in a banner block at top.
- `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/step-01-status.md` — chain handoff; amended with fresh-eyes summary.

## Lessons + memory candidates

- **Memory candidate** — *"Drift-audit interpretation needs a fresh-eyes pass before accepting the No-Go."* The `feedback_fresh_review_and_out_of_sample` rule already says this; this session is the second on-record case (the first being the S74 enrichment NO-GO). Don't accept No-Go on the first read of one model judging another — there's always a "did Sonnet over-reject" branch worth exercising.
- **Memory candidate** — *"Drift-audit reports must cite the specific smoke session, not 'the smoke runs' generically."* I cited S69 from the chain prompt without verifying; the actual session is S77. The chain prompt also had S69 (it carried forward from the in-flight monitor's CV). Both should be corrected.
- **Lesson** — The single biggest cause of Haiku's drift in this audit appears to be `hint_raw` being treated as evidence on par with `evidence_quote`. V5 explicitly forbids it (Rule 4a). Haiku ignored it at scale. Stronger prompt tightening probably can't fix this — it's a model-capability ceiling, not a prompt gap. (Subagent's read; I agree.)

## What's next

The 7-step promotion chain is HALTED at step 1. Matt's call on which of these to take in the next session:

- **(A)** Re-run Events bulk on Sonnet 4.6 (~$340 full corpus) — contradicts the `project_stage4_haiku_not_sonnet` memory.
- **(B)** Promote only the long-tail types from Haiku output, drop the structural types.
- **(C)** Sonnet-filter the rejection-bearing types only (~700 rows, ~$2-5).
- **(D)** Tighten Haiku prompt to v6 + re-run (risky — v5 named these failure modes already).
- **(E)** Abandon Events bulk for v2.0; wait for Dialogue.

`progress/continue-prompts/2026-06-01-events-bulk-escalation-pick.md` queued as the next-session entry point.
