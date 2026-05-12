---
session: 45
date: 2026-05-12
model: claude-opus-4-7 (1M context)
type: design / planning
duration: ~90 min
---

# Session 45 — Mission Protocol Design (Watcher + Workers)

## Why this session happened

Matt opened the session reflecting on a "watcher" agent idea from an earlier multi-session period — an Opus-tier overseer watching cheaper workers (Haiku/Sonnet) on long-running tasks. He'd liked the pattern and wanted to formalize it as something reusable.

Two specific frames he carried in:
1. **Concurrent workers + Opus watcher is a real cost-curve inversion** — cheap workers grinding bucketed work in parallel, expensive watcher only at decision points. Aligns with `feedback_python_before_agent.md` and `feedback_model_selection_at_session_start.md` philosophies.
2. **The fleet plan (`fleet-orchestration-plan.md` + `fleet-runtime-architecture.md`) went too far** — a long-lived daemon, tmux persistence, multi-day autonomous runs. Heavy lift to stand up; most current todos don't need it.

He wanted a thing **between** "Matt fixes it himself" and "the full fleet daemon." His phrase: "an admiral with a few captains doing shit for it, but the journey is something tangible — one todo, or a group of todos."

## The shape that emerged

Through ~5 rounds of clarification:

**A mission** = a bounded piece of orchestrated work. One or a small group of todos, finite lifecycle, archive when done. ~2h wall-clock. No daemon, no chaining.

**Two abstract roles:**
- **Watcher** — reusable agent in `.claude/agents/watcher.md` (not yet written). Opus-locked (no smoke test gate — Matt's call). Reads structured worker signals; pauses to surface escalations to Matt; doesn't modify worker output.
- **Worker** — cheap-tier agents (Sonnet/Haiku) doing bounded tasks in parallel. Existing `.claude/agents/*.md` files serve here, or task-specific new prompts.

**Mission-file metaphor** — admiral/captain/journey — is mission-file prose only, NOT agent-file naming. Matt was explicit about not conflating layers: `watcher.md` is reusable infrastructure; "admiral" is a mission-file role-label for that watcher on a specific run.

## Mission vs session distinction (added mid-session per Matt's pushback)

Matt asked: "why is case-collision a mission but year-page-fix isn't?" Forced an explicit threshold:

| Session | Mission |
|---|---|
| Pure deterministic Python or trivial edits | Multiple concurrent LLM workers |
| One actor, no quality variance | Per-worker output has judgment variance |
| Watcher would add no value | Watcher value justifies scaffolding |
| Examples: year-page fix, alias-backfill, typo | Examples: case-collision reconstruction, prose-edge classification |

Rule of thumb: if a single Python script with `--dry-run` does it, it's a session. If multiple agents whose outputs Matt would spot-check before they propagate, it's a mission.

This distinction got baked into the protocol doc. It's also the answer to a deeper recurring question — "when does orchestration scaffolding earn its weight?" Most todos in the Weirwood project are sessions, not missions.

## Daemon — explicitly deferred

`fleet-orchestration-plan.md` + `fleet-runtime-architecture.md` (Session 26 work) stay in the repo as future-state vision. Pulled forward when:
1. A single mission projects to >24h cumulative wall-time, OR
2. 3+ missions a quarter want to run concurrently with resource isolation, OR
3. End-to-end planning quality justifies auto-chaining stages

None true now. Missions are present-state.

## What "orchestrator script" means (Matt asked for a refresher)

In the fleet plan, `scripts/fleet-orchestrator.py` was a Python process that walks a stage DAG, dispatches `claude --print --agent <name>` subprocess calls, captures stats, handles rate limits. **In v1 missions we don't have one.** The watcher does dispatch + monitor in a single role; no separate Python orchestrator. Orchestrator script reappears with the daemon.

## LangGraph parallel (briefly explored, set aside)

Matt asked if this was LangGraph. Partial yes for the daemon path — DAG, persistent state, automated transitions. The watcher-with-Matt-orchestrating pattern is NOT LangGraph; it's a stripped-down human-in-the-loop dispatcher. If the daemon ever ships, LangGraph would be a reasonable framework. Set aside as "interesting but not relevant to v1."

## Artifacts landed

1. **`working/agent-fleet-specs/mission-protocol.md`** — DRAFT v0. Status: NOT LOCKED. Sections: why this exists, mission-vs-session, roles, mission file schema, worker emission contract, watcher behavior, lifecycle, what v1 deliberately doesn't have, daemon-deferral triggers, 5 open questions, companion docs, next steps.

2. **`working/agent-fleet-specs/missions/2026-05-12-case-collision-top-10.md`** — first concrete mission file, worked example of the schema. Top-10 case-collision pages by backlink count (Small Council 215, King in the North 195, Free Folk 141, Brotherhood Without Banners 141, Narrow Sea 120, Great Ranging 64, Warden of the North 62, Old Gods 61, Hedge Knight 60, Master of Coin 57). Queued, not started.

3. **`next.md` updates** — Tracks 2/3/5 marked DONE (per Matt's "Track A and B done" mid-session report); Track 4 reframed as the mission-protocol smoke test linking to the new mission file; Track 6 added for post-first-mission protocol formalization.

4. **2 memory entries:**
   - `feedback_session_purpose_discipline.md` — don't bolt execution onto planning sessions, even small ones.
   - `project_mission_protocol_v0.md` — pointer to the protocol + the mission/session distinction.

## Episodes worth remembering

### "I tried to slip an execution task in, Matt called it"

Matt said "1,2,3,4 in order" where option 4 was "Pick a quick session-task to clear something while we think." I interpreted "pick" as "pick and execute" and proposed alias-backfill round 2 with full script plan. Matt redirected: "This session began as a planning session on the how with agents... if we are doing the full alias backfill round too let's just do this in a new session."

The instinct to bundle was wrong on two axes:
- **Session purpose dilution** — a planning session that also runs an execution task has a muddier worklog entry.
- **Execution context starvation** — the bundled execution task gets stale context.

Saved as `feedback_session_purpose_discipline.md`. Future planning sessions should end with "queued for separate sessions: X, Y, Z" — not "executing X now while you think."

### "Watcher always Opus, no smoke test"

The model-fit policy memory (`feedback_model_selection_at_session_start.md`) says default to cheapest viable with a smoke test before locking. I proposed Sonnet-vs-Opus smoke test for the watcher as an open question. Matt overruled: "The watcher will always be Opus, no need to smoke test that."

Reading between the lines: the watcher role's value IS the reasoning depth — catching subtle pattern issues, asking the right questions when ambiguous. A cheaper-model watcher that misses escalations defeats the cost-inversion premise. Locked Opus in the protocol doc; removed the smoke-test open question.

### Naming layers

Matt: "I'm not sure if we should refer to the reusable agents like this... they are different than the 'concrete' tasks."

The friction was: I was using "admiral" interchangeably with "the watcher agent." Matt pushed: the abstract reusable agent role (`watcher.md`) and the mission-specific metaphor (admiral) are different layers. Don't conflate.

Resolved: `.claude/agents/watcher.md` uses neutral role names. Mission files use admiral/captain/journey for readability. The mission file declares "Admiral: `.claude/agents/watcher.md`" — that's the join.

### Tracking the running parallel sessions

Mid-session Matt shared a handoff text from another parallel Claude Code session ("TRACK A — Stage 4 prose-edge-classifier"). I had been tracking Tracks 2/3 (from next.md). Matt used "Track A/B" informally to mean the two running things. Mapping never got fully reconciled. I marked Tracks 2/3/5 as done in next.md with a "verify" note. Future endsession workflows: when Matt reports work-track completions from parallel sessions, ask for the exact mapping rather than guess.

## Decisions made

| # | Decision |
|---|----------|
| 1 | Missions are the v1 unit of orchestration. Daemon deferred. |
| 2 | Watcher always Opus 4.7. No smoke-test gate for this role. |
| 3 | Mission protocol is DRAFT (NOT locked). First mission feeds redlines back. |
| 4 | Mission file schema embedded in each file; NO separate reusable protocol doc beyond the DRAFT (avoid over-abstraction before pattern crystallizes). |
| 5 | First mission = case-collision top-10 (10 highest-backlink pages, NOT all 125). |
| 6 | v1 watcher = Matt-as-admiral (no `.claude/agents/watcher.md` yet — promoted after first mission). |
| 7 | Captains in mission #1 = ad-hoc Sonnet workers; prompt embedded in dispatch (no `.claude/agents/case-collision-reconstructor.md` until pattern repeats). |
| 8 | Mission archival: failed missions get a postmortem section, never deleted. |
| 9 | Mission scratch dirs (`working/missions/<slug>/`) retained as audit trail post-archive, NOT cleaned. |
| 10 | Mission files (active + done) committed to git, NOT gitignored. (Lean from open question 5 — confirmed during drafting.) |

## Open questions left explicitly unresolved

1. One watcher prompt or many? (Lean: one reusable with mission-specific config.)
2. Captain-to-captain context: parallel-only, or watcher synthesizes? (Lean: parallel-only; cross-captain dependency = bad mission slicing.)
3. Question resolution mid-mission: Matt manually applies, or watcher relaunches captain? (Lean: Matt manually for v1.)
4. Mission archival to git. (Lean: committed.)
5. Concurrent missions allowed? (Lean: v1 = one at a time.)

## What's queued for separate sessions

- **Alias-backfill round 2** — session-sized, deterministic. Just needs Matt to OK the Aemon-slug fallback rule (verify `aemon-targaryen-maester` and `aemon-targaryen-dragonknight` slugs exist before adding aliases). Expected delta: mention-index resolution 70.6% → ~72-74%.
- **Case-collision top-10 mission** — first real mission. Matt-as-admiral. Validates the protocol. If the pattern holds, follow-up mission(s) for the remaining 115 case-collision pages.
- **Year-page type fix** — has architectural decision embedded (3 options for `event.year` vs `chronology/` dir vs delete); deserves its own session.
- **Mission protocol redline + `watcher.md` agent prompt** (Track 6 in next.md) — after the first mission lands.

## Reflection on the session itself

This was a real architecture session — not big design (e.g., the wiki Pass 2 pipeline redesign), but architectural in the sense that it carves out a new abstraction layer between sessions and the fleet daemon. The interaction pattern was tight: Matt pushed back twice (once on naming, once on scope creep), and both pushbacks improved the artifact.

The risk going forward: if no one runs the first mission, the protocol doc becomes orphaned — design without validation. Track 6 in next.md is the explicit hedge against that; the first real mission must land for the protocol to earn its place. If after 2 weeks no mission has run, that's a signal the protocol over-engineered the problem and we should fold back to sessions-only.
