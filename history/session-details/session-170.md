---
session: 170
title: Chat-UI alpha — publishing posture settled + repo/auth architecture
date: 2026-06-29
track: meta
model: Opus 4.8
type: design/decision (no build)
---

# Session 170 — Chat-UI alpha: publishing settled + repo/auth architecture

A short decision session on top of S169's design review. No code written, no graph mutation.
Matt opened the `/continue chat-ui-alpha` handoff by asking a single architecture question, and the
session resolved into three load-bearing decisions plus a scrub of recurring churn.

## What Matt asked, and what it surfaced

Opening question: *"Will the front end live in this repository, and how will it be organized?"* — a §9 open
question from the design doc. Answering it pulled in two of Matt's own assumptions that turned out to be wrong or
reversible:

1. **"I thought a repo had to be public to deploy via Netlify."** False — Netlify deploys private repos on every
   tier. This was the constraint silently driving the whole §7 "deploy text boundary" worry. Removing it collapsed
   the boundary problem.

2. **The graph and the book text are separable, and only the text is copyright-sensitive.** Verified: both
   `graph/nodes/` (8,729 files) and `sources/chapters/` (347 files) are git-tracked (the design doc was right;
   CLAUDE.md's "chapters GITIGNORED" was stale — `sources/wiki/` too, ~35k tracked). The graph is Matt's own work
   product; the book text is GRRM's.

## The decision (Matt, emphatic)

Offered three boundary options (scrub-and-publish-this-repo / private-app-repo-+-public-graph-mirror /
private-repo-+-in-app-explorer). Matt rejected the framing and gave a blanket directive instead:

> *"I want this repository to stop caring about the source material. Scrub every old reference to not wanting to
> push publicly… I never want to hear about a concern about pushing publically again. I have told agent after agent
> that I want to publish this."*

**Settled (S170):**
- Repo **stays private**, deploys to Netlify **from the private repo**. Graph + front end + book text all
  **co-located in THIS repo** under a new top-level `web/`. No separate repo, no `git rm --cached`, no history
  scrub, no build secret, no public/private split to design.
- Book text bundles into the serverless function as-is. The only surviving "allowlist" is a bundle-*size* guard
  (never ship the 1.8 GB `graph/edges/` backup dir), nothing to do with publishing.
- Publishing/copyright is a **closed question** — future sessions must not re-float it. One optional footer line is
  the only attribution artifact.

The root cause of the churn: the live design doc + a loaded memory carried the old "should we push this / copyright
exposure" anxiety, so it resurfaced session after session and Matt had to override it each time.

## The scrub (durable mechanism so it stops recurring)

Three load-every-session surfaces fixed:
- `working/chat-ui/alpha-design.md` — rewrote §7 (Copyright posture / OPEN text-boundary → "Publishing & source
  material — SETTLED, do not re-raise"), removed §8 step-0c, stripped §8b's copyright-discomfort framing (kept the
  self-curating quote loop as a *graph-quality* goal Matt still wants), updated §0/§2/§9.
- Memory `project_real_goal_graph_for_agents` — copyright flagged closed; fixed the stale "unpublished URL no one
  sees" line (it's a published portfolio piece, just no auth).
- **New memory `project_publish_settled`** + MEMORY.md pointer — its whole job is to make a future agent read
  "closed, don't" before raising it.
- `CLAUDE.md` — corrected the stale GITIGNORED labels on `sources/chapters/` + `sources/wiki/` (the one file that
  loads into *every* session).
- `worklog.md` Active Decisions — recorded the S170 decision with Matt's verbatim instruction.

## Local-auth clarification (the second half of the conversation)

Matt asked whether his Claude **subscription** could power local testing instead of API dollars. Resolved:

- The Anthropic SDK resolves credentials `ANTHROPIC_API_KEY` → `ANTHROPIC_AUTH_TOKEN` → an `ant auth login` OAuth
  profile. So a bare `new Anthropic()` after `ant auth login` (with `ANTHROPIC_API_KEY` unset) runs **local dev on
  Matt's plan quota** — same pool Claude Code spends, zero API dollars.
- **Two billing buckets, not three:** subscription quota (interactive Claude Code · `claude -p` · OAuth-profile
  SDK) vs API credits (`ANTHROPIC_API_KEY`). Matt was confused that `claude -p` might be "free/separate" — it
  isn't; it spends the same plan quota. The Option-1-vs-2 distinction was *architecture fit* (SDK tool-loop vs
  subprocess), never billing.
- **Hard boundary:** deployed Netlify must use the API key — OAuth tokens are short-lived/not headless-refreshable,
  and a personal subscription isn't the supported way to power a public endpoint. Identical function code; the only
  difference is whether a key is present in the env. Clean dev/prod split.
- Folded into design doc §4. (Heavy load-tests should still use a metered key so they don't eat the plan allowance.)

## Repo layout (folded into §8)

One new `web/` dir; Netlify deploys a build *output* (static page + function bundle), never the whole repo. A new
`scripts/build-chat-export.py` reads `graph/` + `sources/chapters/` → allowlisted bundle in `web/data/` (gitignored,
regenerated). Recommended boundary for the alpha = option (a) keep this private repo as the deploy repo.

## State at session end

Design doc is decision→build-ready with §7/§9 resolved, §4 auth modes documented, §8 repo layout concrete. The
remaining §9 opens for the build session: retrieval shape (Option A confirmed as lean), model (smoke-test
Sonnet/Opus), Edge-vs-sync runtime, failure-mode UX, conversation/session state, telemetry-vs-curated-only scope.
Next session = the §8 step-0 spike → MVP vertical slice. No graph work, no harvest (queue at 0).
