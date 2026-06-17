---
session: 103
date: 2026-06-16
model: Opus 4.8 (1M context) orchestrator + 4 parallel Sonnet 4.6 general-purpose advisors
title: "Fable cleanup — nomenclature decided (3 terms, not 6)"
commit: (this endsession commit)
---

# Session 103 — Vocabulary canon: three terms, not six

## Purpose

S102 left three next-move decisions for Matt (#1 PRECEDES/FOLLOWS ordering edges,
#2 causal TRIGGERS, #3 Fable cleanup). Opened via `/continue next-move-decisions`,
put the three to Matt. He picked **#3 Fable cleanup**, then narrowed to its
**nomenclature half** (the repo-reorg half he set aside — and it's largely overtaken
by S99/S101 hygiene anyway).

## The pivot — six terms rejected

The standing proposal (`working/nomenclature-reform-proposal.md`, 2026-06-12) defined
**six** canonical terms (Pass / Track / Step / Gate / Tier / Run) plus a ~175–250-edit
retroactive doc sweep. When I framed an AskUserQuestion option as "approve the §1 six-term
scheme," Matt stopped me: *"I feel like six is too many, I don't even know what they mean.
I didn't mean to indicate that was the vocabulary."* He asked me to **fan out subagents** on
the real question: *"how can I keep the vocabulary consistent across this project, and give
it necessary info?"*

(I reverted the CLAUDE.md edit I'd made treating the option-selection as approval — lesson:
a selected AskUserQuestion option label is not a content sign-off.)

## The advisory fan-out (4 lenses, parallel general-purpose)

| Lens | Verdict |
|---|---|
| **Minimalist** | 3 terms — Pass/Track/Tier. Drop Step/Gate/Run *as coined terms* (lowercase English). Rule of thumb: *"Is this a thing, or me doing a thing? Things get a Word; doing gets a sentence."* |
| **Empirical** (measured living docs) | The collisions are mostly already tidied. High-frequency terms (Pass 344, Tier 233, Stage 143, Run 156 = 66% of usage) are each effectively monosemous in living docs. **Only genuine live ambiguity = Track** (numbered work-lane vs lettered backfill). Plate = dead clutter. Six terms is heavy machinery for ~1 real problem. |
| **Mechanism architect** | The crux is the **subagent gap** — spawned subagents never load CLAUDE.md/memory. Canon in `reference/glossary.md`; CLAUDE.md stub; **push** (orchestrator pastes into subagent prompts) + **pull** (pointer in agent defs); grep linter deferred. |
| **ROI skeptic** | Do ~15% of the proposal. The one *data* hazard is "Tier" overloading. The 175–250-edit sweep re-creates the S102 "timestamp diffs bury the real change" mistake in prose form — spend the session on edges. Forward-only "no new terms" rule beats a retroactive sweep. |

Strong convergence: **six is overkill; the real problems are narrow** (Tier overload = data
risk; Track ambiguity); **the sweep is not worth it**; **the mechanism is glossary + CLAUDE
stub + subagent push/pull**.

## What Matt decided (term-by-term refinement)

Matt didn't take the advisors' set wholesale — we refined live:
- Confirmed **step** (lowercase) as the one default word for ordered sub-units — explicitly
  to stop the Stage→Plate→wave→Phase proliferation (he asked what "you sequence work a lot"
  meant; I grounded it in the five different words five efforts had used for the same concept).
- Confirmed keeping **Track** (kill the lettered idiom) over swapping to a fresh word.
- Confirmed **Tier = confidence 1–5 only**, unrelated to work — "good call."

Final canon: **Pass** (grandfathered numbered corpus sweeps) · **Track** (named workstream) ·
**step** (lowercase sub-unit) · **Tier** (confidence 1–5 only).

## What shipped (all additive, +33/−3, no code/graph change)

- `reference/glossary.md` (NEW) — canonical forward vocab + retired-term decode + the
  consistency mechanism + queued follow-ups.
- `CLAUDE.md` — `## Vocabulary` stub with the "paste terms into naming/sequencing subagents"
  instruction (the answer to "give it necessary info" — closes the subagent gap via push).
- `worklog.md` — Active Decision entry + Current State line updated.
- `working/nomenclature-reform-proposal.md` — superseded preamble (won't be re-read as live).
- memory `feedback_vocabulary_canon` + MEMORY.md index line.
- `working/todos.md` — scheme marked DONE; **2 narrow follow-ups queued** (rename live
  non-confidence "Tier"→class/level — the only data-error fix; pull-channel pointer in ~8
  live agents). The 200-edit sweep deliberately NOT queued.

## Decisions

- **Vocabulary = 3 terms + `step`, not 6.** Full retroactive sweep DECLINED as churn-for-tidiness
  (history glossary decodes old docs; move forward). Tier reserved for confidence exclusively
  (the one rule with teeth — it's stamped on edge data).
- **Mechanism: one source of truth + push/pull propagation, linter deferred.** Reuses the
  project's existing vocab-lockdown + drift-detection patterns rather than new infra.
- **Repo-reorg half of Fable cleanup NOT taken up** (Matt's scope choice).

## What's next

Decisions #1 (PRECEDES/FOLLOWS — vocab-add + grouping basis) and #2 (causal TRIGGERS pilot)
remain, both Matt's. Board roadmap order #1 → #2. Continue prompt updated to carry them.
