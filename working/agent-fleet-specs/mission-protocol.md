# Mission Protocol — DRAFT v1 (post-first-mission)

**Status:** Iterating. v0 was the working sketch. v1 incorporates lessons from the first real mission (case-collision top-10, 2026-05-12 — `working/agent-fleet-specs/missions/done/2026-05-12-case-collision-top-10.md`). Still not normative; revise on next mission.

**Created:** 2026-05-12 (Session 43+); v1 revision 2026-05-12 (post-first-mission archive)
**Purpose:** How to run an isolated, bounded piece of orchestrated work — one todo or a small group of todos, finite lifecycle, archive when done. The middle ground between "Matt fixes it himself" and "the fleet daemon does it autonomously over days."

---

## Lessons from first mission (case-collision top-10, 2026-05-12)

Four findings, baked into the role descriptions + emission contract below:

1. **Worker = wave-sized, not slug-sized.** 1-worker-per-slug was over-decomposed. Right default: one worker handles a *wave* (~5 bounded items), sequencing them internally in its own context. Cuts dispatch overhead, keeps schema cohesion, lets the worker apply lessons from item N to item N+1 within the same session. Slug-sized workers only when one item is large enough to be its own mission.

2. **Task-specific strategies must be in the worker template upfront**, not added wave-by-wave mid-mission. Wave-1 small-council shipped an empty Edges block because the prompt didn't authorize reverse-lookup; wave-2 prompt added one line and produced rich edges. Generalized: if a strategy works for one worker, the prompt was incomplete for the rest. Pre-write completely; iterate the *template*, not the *individual workers*.

3. **Schema validation is mandatory; freeform prose isn't enough.** Every worker on the first mission drifted somewhere: `status` enum (3 used "complete"), confidence type (2 used strings), field names (`started` vs `started_at`, `created_at` vs `started_at`), timestamps (all 10 used placeholder `T00:00:00Z`). Fix: worker emission contract requires the worker to validate its own `status.json` against an explicit schema before exiting. The Pass-2 pipeline already does this (`scripts/wiki-pass2-validator.py`); the mission protocol inherited the contract but skipped the enforcement.

4. **Watcher is optional, not required.** For bounded missions (≲30 min) run as Agent-subagent workers from a single orchestrator session, the watcher adds no value — the orchestrator sees worker return messages directly. Watcher earns its keep when workers run in genuinely separate Claude Code windows with no orchestrator visibility. **Two execution modes are both first-class:**
   - **Multi-window:** workers in separate Claude Code windows; watcher in its own window briefs Matt. Use for missions that exceed an orchestrator's context window, or run over hours.
   - **Subagent-orchestrated:** workers dispatched as parallel `Agent` calls from a single orchestrator session; no watcher needed. Use for bounded missions (~15-30 min).

   Each mission file should declare which mode it expects.

---

## Why this exists

`fleet-orchestration-plan.md` + `fleet-runtime-architecture.md` describe a long-lived Python daemon walking a multi-stage DAG across the full project. That's the full fleet. It's a real future, but a heavy lift to stand up, and most current todos are smaller than that.

A **mission** is the unit between a one-line edit and the full fleet:
- One todo or a tightly-related group of todos
- Finite scope, finite time horizon (typically <2h wall-clock)
- A small number of concurrent workers, one watcher
- Begins → runs → ends → archives. No persistent state, no daemon, no cron.

The fleet plan stays in the repo as the future-state vision. Missions are the present.

---

## Mission vs session

Not every todo is a mission. Most are just **sessions** — work Matt does (or asks a single agent to do) without scaffolding. The mission scaffolding earns its weight only when worker quality variance is real and a watcher catches things Matt would miss.

| It's a **session** when... | It's a **mission** when... |
|---|---|
| Pure deterministic Python or trivial edits | Multiple concurrent LLM workers |
| One actor, no quality variance | Per-worker output has real judgment variance |
| Watcher would add no value (nothing to escalate) | Watcher value justifies the protocol scaffolding |
| Examples: year-page type fix (10 nodes), alias-backfill (4-6 frontmatter edits), architecture.md typo | Examples: case-collision reconstruction (LLM workers produce Identity prose from cross-refs; quality varies), prose-edge classification across N buckets |

Rule of thumb: if a single Python script with a `--dry-run` flag would do it, it's a session. If multiple agents whose outputs Matt would want to spot-check before they propagate are needed, it's a mission.

---

## Roles

Two abstract roles. Each mission file gives them a metaphor for that specific run; the reusable agent files use the neutral role names.

### Watcher (reusable agent: `.claude/agents/watcher.md` — v1 written Session 45, **briefing-assistant model**)

- Runs in its OWN Claude Code session. Matt opens it in a separate window.
- Reads worker state from disk (JSONL files, `status.json`, output files, dashboards).
- Answers Matt's questions about the parallel work: what's done, what's running, did anything fail, what should run next.
- Proactively flags escalation conditions (per mission file) when Matt checks in — does NOT poll on a timer, does NOT auto-pause.
- **Does NOT dispatch workers, does NOT invoke Agent tool, does NOT modify worker output.** Matt orchestrates the parallel worker sessions himself.
- **Always Opus 4.7** — locked per Matt 2026-05-12. No smoke-test gate for the watcher role. Reasoning quality matters; Opus' tokens are cheap compared to the value of catching a worker going off the rails early.
- **Future:** a "dispatcher-watcher" mode where the watcher DOES orchestrate (uses Agent tool, applies escalation rules autonomously, manages dispatch waves) is filed as a separate agent for future use. Distinct from this briefing-assistant model.

### Worker (parallel agent — either separate Claude Code session OR Agent-tool subagent)

- One worker per execution context (window OR subagent slot). Worker runs its task, emits signals to disk, exits.
- **Default task unit: one wave of work (~5 bounded items), sequenced by the worker internally.** 1-worker-per-item wastes dispatch overhead and fragments schema cohesion; 1-worker-for-everything risks context overflow. Wave-sized is the right middle. Slug-sized workers only when one item is large enough to fill a session by itself.
- Writes signals to disk per the worker emission contract below — INCLUDING the schema-validation step (mandatory; see contract).
- Typically Sonnet or Haiku — cheap because there are many of them. Opus only if the task itself needs deep reasoning per chunk.
- Doesn't read other workers' output. Doesn't supervise. Just does its task and emits its signals.
- **Two valid execution modes, both first-class:**
  - **Multi-window:** Matt opens a fresh Claude Code session per worker, pastes the kickoff. Watcher recommended in a separate window.
  - **Subagent-orchestrated:** Orchestrator session dispatches workers as parallel `Agent` calls. Watcher optional — orchestrator sees return messages directly.
- **The "agent" in `.claude/agents/`** for a worker is OPTIONAL — for repeated patterns, promoting the worker prompt to a `.claude/agents/<task>.md` file is fine.

### Mission file metaphor (user-facing prose only)

In a mission file you may refer to the watcher as the **admiral**, the workers as **workers**, and the run as the **journey**. This is purely for readability of the mission file — the agent files themselves are `watcher.md` and `worker.md` (or task-specific names). Don't conflate the layers.

### Choosing execution mode (subagent vs multi-window)

**Subagent-orchestrated mode OK when:**
- Worker prompt fully inlines schema, types, vocabulary, and task strategy (no "consult X" / "read Y" indirection)
- Task is single-shot per item; stateless reasoning
- Total worker wall-clock < 10 min per worker
- No project context (CLAUDE.md, architecture.md) required at runtime

**Multi-window + watcher when ANY of the following are true:**
- Task requires loading project context (architecture.md TYPE_DIR_MAP, prior decisions, CLAUDE.md rules)
- Worker prompt cannot be made fully self-contained (e.g., must reference multiple inter-related spec files)
- Drift potential is high (multi-step reasoning per item, evolving strategy)
- Wall-clock per worker > 10 min — observability matters
- Matt wants to interrupt mid-flight or check intermediate outputs

**Default if uncertain: multi-window + watcher.** The cost of multi-window is operator overhead (Matt opens windows); the cost of subagent drift is post-mortem analysis time, which is higher.

Session 46's case-collision-batch-2 should have been multi-window — workers needed architecture.md TYPE_DIR_MAP awareness, drift surfaced (event.conflict, object.text framing) that watcher would have caught early.

---

## Mission file schema (v0)

Each mission lives at `working/agent-fleet-specs/missions/<date>-<slug>.md`. Suggested fields:

```markdown
# Mission: <Slug>

**Goal:** Which todo(s) this closes. Link to lines in `working/todos.md` or `next.md`.
**Status:** queued | running | done | archived
**Created:** YYYY-MM-DD
**Wall-clock budget:** ~Nh (when this would no longer be a mission and should escalate)

## Scope
- Concrete inputs (files, slugs, buckets, count of things in play)
- Out-of-scope (things adjacent that are NOT touched this mission)

## Admiral (watcher)
- Agent: `.claude/agents/watcher.md` (or specialized variant)
- Model: opus-4-7 (always — locked)
- Poll cadence: every N worker completions, or every M minutes
- Escalation rules: when does the admiral pause and ask Matt
  - e.g., "≥3 workers file questions-for-matt.jsonl rows"
  - e.g., "any worker emits status=fail"
  - e.g., "reconstruction confidence <0.6 on ≥1 worker output"

## Workers (workers)
- Agent(s) used: `<existing-agent>` or specifies new
- Model: sonnet-4-6 (default) | haiku-4-5 (if task is mechanical)
- Parallelism: N concurrent workers
- Per-worker task size: e.g., "1-2 pages each" or "one bucket"
- Worker dispatch list: explicit (file paths / slugs) or rule-based

## Signals workers emit
- Required files (must exist after each worker completes):
  - `working/missions/<mission-slug>/worker-<id>/output.<ext>` — the actual work product
  - `working/missions/<mission-slug>/worker-<id>/status.json` — `{started_at, completed_at, status, confidence?, notes}`
- Optional files:
  - `working/missions/<mission-slug>/worker-<id>/questions-for-matt.jsonl` — blocking questions
  - `working/missions/<mission-slug>/worker-<id>/conflicts.jsonl` — disagreements with existing graph state

## Success criteria
- Numeric or boolean (e.g., "all 10 case-collision slugs have non-stub Identity sections" / "audit shows 0 broken backlinks for these slugs")
- How to verify (which script, which grep)

## Archive condition
- When this file moves to `missions/done/<date>-<slug>.md`:
  - Worklog Session entry written
  - Success criteria met OR mission explicitly aborted with a postmortem section
  - todos.md updated (boxes checked, follow-ups added)

## DO NOTs
- Standard guardrails: don't auto-run /endsession, don't touch out-of-scope nodes, don't refetch wiki.
- Mission-specific guardrails as needed.

## Outcome (filled in at archive time)
- One paragraph: what shipped, what didn't, any surprises.
```

---

## Worker emission contract

Borrowed from the Pass 2 pipeline (`scripts/wiki-pass2.sh` + `scripts/wiki-pass2-validator.py`) which already proved this pattern works. Workers MUST write to disk; the watcher MUST read from disk. No agent-to-agent calls.

**Per-worker files (one worker's run):**

- `status.json` — final status: `{started_at, completed_at, status: "pass"|"fail"|"partial", confidence?, output_path, notes?}`
- `output.<ext>` — the actual work product (depends on worker's task)
- `questions-for-matt.jsonl` — optional; one row per blocking question. Schema:
  ```json
  {"id": "q-<mission>-<worker>-<n>", "worker": "<id>", "filed_at": "...", "question": "...", "context_files": [...]}
  ```
- `conflicts.jsonl` — optional; one row per detected conflict with existing state.
- `progress.jsonl` — optional but recommended for long-running workers; one row per N% completed.

**Schema validation (mandatory — added v1 post-first-mission):**

Before the worker exits, it MUST validate its own `status.json` against the schema. The first mission proved freeform-prose enforcement is insufficient: every worker drifted on at least one field (status enum, confidence type, field names, timestamps).

Worker kickoff prompts MUST include both the schema and the validation step as the last action before exit. Minimum bar — one of:
- `jsonschema` (Python) validation against an inline schema literal,
- `jq` check verifying all required fields exist with correct types,
- worker re-reads its own `status.json` and asserts on each field by name and type.

Required fields and types (lock):
- `worker_id`: string
- `started_at`, `completed_at`: ISO-8601 UTC, real wall-clock (NOT placeholders like `T00:00:00Z` — capture `datetime.utcnow().isoformat()+"Z"` at session start and exit)
- `status`: one of exactly `"pass"`, `"partial"`, `"fail"` (NOT `"complete"`, NOT `"done"`)
- `confidence`: numeric `0.0-1.0` (NOT strings like `"high"` or `"tier-1"`)
- `source_count`: integer
- `source_files_consulted`: array of strings
- `notes`: string or array of strings

**Mission-wide files (admiral aggregates):**

- `working/missions/<mission-slug>/_dashboard.json` — admiral writes this on each poll: counts of statuses, open questions, last-poll-at. Lets Matt eyeball state in one read.
- `working/missions/<mission-slug>/_admiral-log.md` — admiral's free-form log: which workers it dispatched, which escalations it surfaced, when it paused for Matt.

---

## Watcher behavior (v1 — briefing-assistant, single mission, no daemon)

The watcher runs in its own Claude Code session, parallel to the worker sessions:

1. **Startup.** Matt pastes a kickoff prompt referencing this protocol + the mission file. Watcher reads both; reports mission scope, worker locations, escalation conditions, ambiguities. Waits.
2. **Answer Matt's questions.** When Matt asks "status?" / "did anything fail?" / "should I run next?" / "show me worker-X's output", watcher reads relevant scratch dirs from disk and answers.
3. **Proactive surface on each check-in.** Before answering a question, watcher scans state; if any escalation rule has tripped since last check, it leads with a "Heads-up: <rule>" before answering.
4. **End-of-mission summary.** When Matt asks "are we done?" and success criteria are met, watcher produces an outcome summary template (one paragraph what shipped, confidence distribution, surprises, pattern verdict, recommended archive steps). Matt manually does the archive.

The watcher does NOT:
- Run unattended (no polling timer, no background loop)
- Dispatch workers (Matt does that in separate sessions)
- Modify worker output, mission file body (other than possibly Outcome via Matt's direction), or any canonical artifacts
- Use the Agent tool to launch subagents

If the mission needs multi-hour parallelism with no Matt-attention, that's a fleet-daemon signal — escalate the planning.

---

## Lifecycle

```
queued (file in missions/, no workers dispatched yet)
   ↓
running (watcher session active; workers in flight or recently completed)
   ↓
done (success criteria met; outcome written; not yet archived)
   ↓
archived (file moved to missions/done/<date>-<slug>.md; worklog entry written;
          todos.md updated; per-mission scratch under working/missions/<slug>/
          either retained for audit or cleaned, mission file's call)
```

Failed missions become **archived with a postmortem section** — they don't get deleted. Failed missions are how we learn.

---

## What v1 missions deliberately don't have

- **A standalone orchestrator script.** The watcher is the dispatcher.
- **A cross-mission stats CSV.** Per-mission outcomes live in each mission file's Outcome section.
- **Daemon, tmux, multi-day persistence.** Missions complete inside one session (or one+a-short-resume).
- **Auto-chaining.** Mission B doesn't auto-start when mission A lands. Matt picks the next mission.
- **Rate-limit handling beyond what the agent invocations themselves report.** If we hit the wall, the watcher pauses and surfaces; no auto-resume from a stored reset-time.
- **Cron / schedule integration.** Future-daemon work, not v1.

---

## When we'd pull the daemon forward

The daemon path (`fleet-orchestration-plan.md` + `fleet-runtime-architecture.md`) gets revisited when at least one of these is true:

1. **A single mission projects to >24h cumulative wall-time.** At that point we need crash-resilience and unattended progress — that's daemon territory.
2. **3+ missions a quarter want to run concurrently** with resource isolation we can't get from "spin up another Claude Code session."
3. **End-to-end planning quality reaches a level** where auto-chaining stages (mission A's output triggers mission B) saves real Matt-time vs. re-evaluating priorities by hand each time.

None of those are true now. Stay missions-only. Revisit when one of the conditions trips.

---

## Open questions (this doc evolves as we answer these)

1. **One watcher prompt or many?** Lean: one reusable `.claude/agents/watcher.md` with mission-specific configuration passed via the mission file. The watcher reads its own mission file to know what to do.
2. **Worker-to-worker context.** Sometimes worker B's work depends on worker A's output (e.g., A reconstructs Identity, B verifies against cross-refs). Two patterns possible: sequential workers (slower), or watcher synthesizes A's output into B's input. Lean: keep workers fully parallel; if cross-worker dependency surfaces, that's a sign the mission was sliced wrong.
3. **Question-resolution mid-mission.** When Matt answers a worker's question, who applies the answer — Matt manually, or the watcher relaunches the worker with the answer baked in? Lean: Matt manually for v1; watcher-relaunches in v2 if friction shows up.
4. **Mission archival to git.** `missions/<active>.md` and `missions/done/*` — committed to repo, or gitignored like `next.md`? Lean: committed (the project's story benefits from preserved mission files).
5. **Concurrent missions.** Two missions running in parallel Claude Code sessions — safe? Mostly yes if scopes don't overlap, but no explicit coordination. v1 = at most one mission at a time; concurrent comes later.

---

## Companion docs

- `working/agent-fleet-specs/agent-pipeline-plan.md` — full agent roster (27 agents). Missions pick from this roster for worker assignments.
- `working/agent-fleet-specs/fleet-orchestration-plan.md` — full-fleet daemon plan. Future-state; missions are a smaller-scope subset of these ideas.
- `working/agent-fleet-specs/fleet-runtime-architecture.md` — tmux/daemon/process model. Future-state.
- `next.md` — Matt's roadmap. When a mission file is queued, link to it from next.md as a Track.

---

## Next steps for this doc

- [x] Run the first real mission (`working/agent-fleet-specs/missions/done/2026-05-12-case-collision-top-10.md`) — done 2026-05-12.
- [x] Write postmortem / lessons section — done 2026-05-12 (see top of doc).
- [x] Revise Worker role + emission contract — done 2026-05-12 (wave-sized default, dual execution modes, schema-validation step).
- [ ] Refine `.claude/agents/watcher.md` to reflect optional/multi-window-only role — defer until a multi-window mission surfaces friction. Subagent-orchestrated missions don't need watcher.md changes.
- [ ] Apply v1 lessons to next mission's worker kickoff template: wave-sized worker assignment + reverse-lookup-as-default (for case-collision-style reconstruction) + explicit schema-validation step. Use the next case-collision batch as the first v1 test.
- [ ] Resolve remaining open questions (mid-mission question-resolution, watcher-relaunch ergonomics) as friction surfaces; don't pre-design.
