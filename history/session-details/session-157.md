---
session: 157
date: 2026-06-27
track: graph
model: Opus 4.8 orchestrator + Sonnet 4.6 subagents (lenses / fresh-verify / harvest attachers)
type: enrichment dip + PROCESS-DRIFT postmortem
---

# Session 157 — A1.6 Euron dip, and a process-drift postmortem

The execution facts (the +37-edge Euron dip, 0 new nodes, fresh-verify 36C/1A/0R, the harvest
drain 149→0, +16 food nodes) live in the `worklog.md` S157 entry and the
`working/enrichment/euron/` artifacts. This detail file exists for the **process incident** Matt
surfaced mid-session — the durable lesson, not the dip.

## The incident
Matt stopped the dip after the lenses ran: *"clearly there are several areas of drift... whereas
previously these enrichments were going perfectly."* Two specific drifts:

1. **Disposable mint-script proliferation.** ~33 per-dip `mint_*_enrichment_sNNN.py` + `finalize_*`
   scripts (plus the older `mint_*_arc.py` pile) had accumulated in `scripts/`. Matt: *"I cannot
   stand disposable script clutter... why aren't there generic/reusable scripts?"*
2. **The harvest queue stopped being drained.** It had ballooned **0 → 120 open** across S153–S156
   while Matt wasn't looking; the enrichment agents had stopped *touching* (draining) it and only
   *fed* it. Matt suspected the new **SIFT** track had tangled it up.

## What the forensics found
- **Scripts:** NOT rogue — the per-dip mint script is prescribed by the machine doc
  (`arc-enrichment-backlog.md` step 3) and goes back to **S106** (the early "perfect" dips used them
  too). The real problem is **copy-paste debt**: each is ~95% identical boilerplate; the S106 dip
  wrote one and every dip since copied-and-modified it instead of factoring the shared parts out.
  `mint_arc_lib.py` was a half-step that never got finished. → Queued **S158** to build one
  parameterized `mint_enrichment.py` + `finalize_enrichment.py` (the 33 examples are both the spec
  and the regression test — validate by replaying a dip's `candidates.json` byte-identical).
- **Harvest:** the drain was **never in the global `/endsession` checklist.** It lived as a numbered
  step *inside the continue prompt* — the old `2026-06-18-causal-arc-execution.md` had *"step 6:
  harvest sweep before finishing"* + *"a consume-pass is due first."* Across ~40 hand-offs the prompt
  template eroded: S155–S157 kept the *push* half ("drop rows in the queue") and silently dropped the
  *drain* half. Matt's hypothesis ("it was being put into each continue prompt") was exactly right.
- **SIFT:** mechanically innocent — it is walled off (`never writes working/harvest-queue.md`,
  Stage 2 not even running). It did NOT cause the balloon. The likely link was *attention drift*
  (SIFT was built in the same S155/S156 window the manual drain lapsed in). Deferred anyway, by Matt's
  call, to keep the harvest/SIFT redundancy from confusing things.

## Why steps like that lapse (the generalizable lesson)
Four forces, all pulling the same way — worth remembering for any future process step:
1. **It lived in a copied template, not enforced code.** Each session hand-rewrites the next
   session's continue prompt; a step that's prose in a copied-and-trimmed doc is one careless
   condensation away from gone. No single decision deleted the harvest drain — it eroded.
2. **Skipping it fires no alarm.** Skip "run the mint script" → the dip visibly fails. Skip the
   harvest drain → the dip *succeeds*, the queue just silently swells. **Steps whose omission has a
   delayed, invisible cost erode first.** The pain showed up 4 sessions from the cause.
3. **It benefits the future, not the current session.** Draining the queue helps whoever comes next;
   under context pressure an agent optimizing "finish my dip" deprioritizes the altruistic chore.
4. **No owner, no trigger.** "A later harvest pass will get it" had no trigger and no owner, so it
   kept being deferred until Matt became the trigger.

**The fix is to move the step up the enforcement ladder:** prose-in-a-copied-prompt → fixed-checklist
step → mechanical trigger → harness hook. This session moved the harvest drain to **`endsession.md`
step 0 + a one-line `grep` trigger** (count the queue; if ≥30, drain or stage) + the machine doc +
memory `feedback_harvest_queue`. It no longer depends on any continue prompt remembering it. If it
lapses *again*, that's the signal to promote it to a real harness hook.

## Artifacts changed
- Process: `.claude/commands/endsession.md` (new step 0), `arc-enrichment-backlog.md` (machine step 4
  trigger), memory `feedback_harvest_queue` (updated) + `project_sift_deferred` (new), worklog Active
  Decisions (SIFT DEFERRED S157), `working/todos.md` § Dormant (SIFT).
- Dip: `mint_euron_enrichment_s157.py` + `finalize_euron_s157.py`, `working/enrichment/euron/*`,
  edges 23,132→23,169.
- Harvest: `working/harvest-queue.md` (149→0 open), +16 `object.food` nodes, ~80 node-prose attaches.
- Queued: `progress/continue-prompts/2026-08-27-script-consolidation.md` (S158).
