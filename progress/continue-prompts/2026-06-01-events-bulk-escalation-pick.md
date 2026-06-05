# Events Haiku Bulk — Escalation Path Pick (post-audit-NO-GO)

> **Recommended model:** Opus 4.7 (decision shape + planning); Sonnet 4.6 if Matt has already picked the path and the work is mechanical (filter script writing, formalize-edges edit).
>
> **Trust `worklog.md` over this prompt** if they disagree (CLAUDE.md #9).

## Prerequisite — read these first

1. `worklog.md` Session 81 entry — current state and verdict.
2. `working/audits/events-haiku-bulk-2026-05-29/cross-model-audit.md` — full audit report (banner block at top has the fresh-eyes corrections; §6 lists the 5 escalation paths).
3. `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/step-01-status.md` — chain halt state.

## Where things stand

- The 7-step Events v2.0 promotion chain is **halted at step 1**.
- Drift audit (Sonnet judges Haiku on stratified 50-row sample, seed=531, $0.93 spent) returned: **triple 48 %, pair 56 %, 22/50 rejected by Sonnet** — below all three gates.
- Fresh-eyes pressure-test (general-purpose subagent, cold read of all 22 REJECTs) corrected the framing:
  - ~11 of 22 REJECTs are clear V5-correct rejections of Haiku drift (Rule 4a / V5-R2 / Rule 12 violations — `hint_raw` promoted to fact, co-presence treated as relationship).
  - ~3-4 are clear Sonnet over-rejections (`judge_idx 2, 6, 14, 16` — Edmure-on-the-march, Jaime "when he came to Harrenhal", Ramsay sends-riders-to-Roose, Haldon+Duck co-riders).
  - Adjusted triple ≈ 56-70 % — at or below the 70 % gate. **No-Go stands but is borderline.**
  - Methodology bugs: none.
  - S77 (not S69 as the audit originally cited) was the smoke session; it measured *hand-read precision on fresh candidates*, not *Sonnet-judges-Haiku-emits-only*. The two are not comparable; the apparent contradiction is measurement-shape, not drift.

## Decision Matt needs to make

Pick one of these 5 escalation paths from `cross-model-audit.md §6`:

### (A) Re-run Events bulk on Sonnet 4.6
- Same 16,502 candidates, swap model.
- Estimated cost: **~$340** (10× per-row vs Haiku). 16+ hours wall-clock.
- Contradicts memory `project_stage4_haiku_not_sonnet`. Matt's call whether the precision floor changes that.
- Lowest risk on output quality; highest dollar cost.

### (B) Promote only the long-tail types from Haiku output
- Drop everything in {TRAVELS_TO, TRAVELS_WITH, LOCATED_AT, COMMANDS, OPPOSES} — ~22 sample rows × scaling ≈ ~700 emits dropped.
- Keep ~900 long-tail emits where the audit showed n=1 buckets agreeing reasonably.
- Statistically underpowered (most long-tail types n=1 in the sample); some risk that other types have hidden failure modes the sample missed.
- Cheapest defensible path; lowest yield.

### (C) Sonnet-filter the rejection-bearing types
- Re-run Sonnet (`claude -p` cwd=/tmp, same prompt) on the ~700 Haiku rows in TRAVELS_TO/WITH/LOCATED_AT/COMMANDS/OPPOSES.
- Drop the rejects (~70 % of those rows expected), keep Sonnet's emits where it retypes; keep agreements as-is.
- Estimated cost: **~$2-5** (700 rows at Sonnet's ~$0.005/row from this audit).
- Smaller blast radius than (A); preserves Haiku where it agreed; fixes the failure-mode concentration.
- **Audit recommended this as the right-shape escalation.**

### (D) Tighten Haiku prompt to v6 + re-run
- Add specific anti-patterns for the 5 named failure modes (memory-as-fact, mention-as-location, co-presence-as-TRAVELS_WITH, looking-at-as-LOCATED_AT, approaching-as-TRAVELS_TO).
- Re-launch full bulk on Haiku with new SHA.
- Risk: V5 already named most of these failure modes (Rule 4a, V5-R2, Rule 12) and Haiku ignored them. Stronger prose may not move the precision needle reliably.
- Cost: ~$34 again for the bulk; ~$0.93 for the re-audit.

### (E) Abandon Events bulk for v2.0
- Push v2.0 to wait for the Dialogue bulk (originally planned as v2.1).
- Cheapest short-term; loses the audit signal and the $34 already spent.

## What to do once Matt picks

- **(A)** rebuild the runner kickoff for Sonnet; relaunch via `scripts/stage4-events-bulk-run.sh` with `--model sonnet`. The wrapper already supports model swaps.
- **(B)** write a tiny filter script (~30 lines) that strips named-type rows from `_events-haiku-bulk/*/*.edges.jsonl` into a `*.long-tail.jsonl` companion file; then proceed to step 2 of the original chain.
- **(C)** write a small Sonnet-filter script: read named-type Haiku emits, batch through `claude -p` Sonnet cwd=/tmp, keep agreements + retypes, drop rejects. Reuse `stage4-tail-classifier.py`'s `render_classify_prompt` + `invoke_claude` per the audit-script pattern.
- **(D)** draft v6 precision rules (focused anti-pattern block), recompute prompt SHA, smoke ~50 rows on Haiku before full bulk.
- **(E)** archive `_events-haiku-bulk/`, mark the v2.0 chain superseded, switch the next-session focus to Dialogue setup.

Once the path is picked, **update the chain README + downstream step prompts** at `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/` to reflect the new shape — or supersede the chain if (E).

## Hard rules carried forward

- **Never modify `graph/edges/edges.jsonl` without Matt's before/after sign-off.**
- **Never re-launch the Events bulk classifier without Matt's explicit go** (`feedback_no_extraction_without_asking`).
- **Drift-detection is mandatory** for any re-run (memory: `feedback_drift_detection_mandatory`).
- **Default `--dry-run`** on any new audit/filter script.
- The `_events-haiku-bulk/` source artifact is frozen; do not modify it. Any filter operates on a copy or writes alongside.

## Files in play

**Source artifact (frozen):**
- `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk/{book}/{book}-tail.edges.jsonl` — 1,617 typed edges.

**Audit (this session's output):**
- `scripts/events-drift-audit.py` (sha `576cc815649c`) — throwaway, do not generalize.
- `working/audits/events-haiku-bulk-2026-05-29/audit-sample-50.jsonl`
- `working/audits/events-haiku-bulk-2026-05-29/audit-sample-50-judged.jsonl`
- `working/audits/events-haiku-bulk-2026-05-29/cross-model-audit.md`

**Chain dir (halted):**
- `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/README.md`
- `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/01-drift-audit.md` (DONE)
- `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/02-06-*.md` (PENDING — likely need rewrites once path is picked)
- `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/step-01-status.md` (NO-GO captured)
