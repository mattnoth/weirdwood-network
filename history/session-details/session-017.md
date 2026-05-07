# Session 17 — Wiki Pass 2 Orchestration: Patch + Self-Review + Build-Prompt Restructure

**Date:** 2026-04-25
**Mode:** Patch session — apply the 21 review decisions from Session 16 to the runbook + Track B prompt + implement prompt.
**Continue prompt run:** `progress/continue-prompts/2026-04-25-patch-wiki-pass2-orchestration.md` (deleted at end of session).

## Goal

Apply the 21 decisions logged in `working/runbooks/wiki-pass2-orchestration-review.md` to the relevant files. No re-review, no implementation. Then self-review the patched runbook end-to-end. Then update the build-scripts continue prompt to reflect a workflow change Matt asked for: build session does smoke test + self-review post-smoke-test, then a separate fresh-agent script-review session before scaling.

## Patch execution

All 21 decisions applied as logged. No deviations from the review's `**Decision:**` blocks. Patches landed across:

- **Runbook** (19 of the 21 decisions): §1.1 L1 page-index added to deterministic list; §1.2 disjointness rule + tiebreakers; §1.2.1 NEW (HTML categories, dropping `_category-reports/`); §1.3 v1 derivation rule + budget gate; §1.4 NEW (confidence-tier defaults regex table); §2.1 wave-formation rule; §2.1.1 NEW (agent input contract with `bucket_input.json` schema); §3.1 launcher-as-validator-caller; §4.3.1 NEW (status output spec); §5.0 NEW (bucket discovery, two-tier truth); §5.1 routing rule + examples; §5.1.1 NEW (reconciliation, filesystem canonical); §5.2 per-bucket on-disk layout + `update_worklog()` target line; §5.4 orphan/unstick + reset command; §6.5 three JSONL channels (`questions-for-matt.jsonl`, `conflicts.jsonl`, `pass1-contradictions.jsonl`); Open Questions Q2 + Q3 marked closed.
- **Track B prompt:** L1 page-index added as deliverable item 5 (mandatory). Schema specified.
- **Implement prompt:** DoD item 5 fixed (extend `weirwood.zsh`, no new file); reset DoD item added.

## Self-review of the patched runbook

Re-read end-to-end. Caught four coherence issues my own patches introduced or surfaced:

1. **§5.1.1 vs §5.4 contradiction.** §5.1.1 step 3 said "fingerprint mismatch → auto-downgrade to pending and re-run." But §5.4 says prompt-version-bump fingerprint mismatch requires explicit `reset --version`. These contradicted. Fix: §5.1.1 now distinguishes case 3 (input-change source — auto-handle, partial re-run of new pages) from case 4 (prompt-version source — set `version-stale`, refuse to touch, demand explicit `reset`).

2. **Status code table missing entries.** `in-progress` was referenced throughout §5.4 but not in the §4.2 status code table; `version-stale` was newly introduced by the §5.1.1 fix above. Both added.

3. **Implementation Sequence stale.** §"Implementation Sequence" still listed step 4 = "write wiki-ingester prompt" and step 7 = "smoke test direwolves" — both deferred under the workflow change. Rewrote as: Track B → build (no agent) → script-review → wiki-ingester prompt → commence (smoke) → schema review → scale. Eight steps, each transition is a checkpoint.

4. **Stale `weirwood-wiki` references.** Two prose references to a sibling `weirwood-wiki` script existed (§2.1 prose, §6.5 walk-away rule); the appendix and the patch decisions all said "subcommand on existing `weirwood`, no new binary." Both prose mentions corrected.

Self-review took ~10 minutes. Bias risk (same agent who wrote the patches did the review) acknowledged — the next checkpoint is the fresh-agent script-review session that follows the build session.

## Workflow change discussion (mid-session)

Matt clarified after the initial patches landed: the build session should still run a smoke test, and then self-review the scripts post-smoke-test. The fresh-agent review session that follows reads the (smoke-tested + self-reviewed) scripts cold. This restored my earlier-removed smoke test step. Net flow:

1. Track B parser
2. Build session: write scripts → smoke test on `direwolves` → self-review post-smoke-test
3. Fresh-agent script-review session
4. Wiki-ingester prompt session (refines whatever minimal prompt the smoke test used)
5. Commence: scale beyond the smoke bucket
6. Tier core, then tier secondary

Each transition is an explicit session boundary so Matt can halt without sunk-cost regret.

## Files touched

- `working/runbooks/wiki-pass2-orchestration.md` — 21 decisions + 4 self-review fixes.
- `working/runbooks/wiki-pass2-orchestration-review.md` — "Patches Applied" trailer (21-row mapping + workflow change note).
- `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md` — L1 page-index item 5.
- `progress/continue-prompts/2026-04-25-implement-wiki-pass2-orchestration.md` — DoD reshape, smoke test restored, self-review-post-smoke-test added, out-of-scope clarified to "no scaling beyond smoke bucket."
- `worklog.md` — Wiki Pass 2 v1 — core / — secondary checklist lines seeded (so `update_worklog()` has lines to mutate); Session 17 entry.
- `working/todos.md` — patch todo checked off; implement todo rewritten.
- `progress/continue-prompts/2026-04-25-patch-wiki-pass2-orchestration.md` — DELETED.
- `progress/continue-prompts/2026-04-25-review-wiki-pass2-orchestration.md` — DELETED.

## Surprises / process notes

- **Self-review value.** The four issues caught on self-review were all real (not nitpicks). Two were contradictions I introduced; two were stale text the patch decisions implicitly invalidated but didn't explicitly call out. Lesson: when applying a long patch list, the patches can leave the document internally inconsistent in ways no individual patch decision flags. Always re-read end-to-end after applying.
- **Communication friction mid-session.** Matt's "smoke test removed, replaced with non-agentic verification" prompted a "wait what?" — I'd over-interpreted the earlier "review the scripts in another session before we finally commence" as "no agent runs at all in the build session." Net effect was a small back-and-forth to restore the smoke test plus add explicit self-review-post-smoke-test. Useful refinement; would have been costlier to discover at the build session start.
- **No new continue prompts created.** This was a pure patch session; the build session continues from the existing implement prompt (now patched).
