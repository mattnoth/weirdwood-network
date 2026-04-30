# Fleet Runtime Architecture — Multi-Day Autonomous Orchestration

**Created:** Session 26 (2026-04-28)
**Purpose:** How the agent fleet runs unattended for days at a time — process model, state files, resource cleanup, monitoring from fresh Claude Code sessions, blocking-question detection.

**Companion docs:**
- `working/agent-pipeline-plan.md` — fleet roster (24 agents)
- `working/fleet-orchestration-plan.md` — stage DAG + stats schema + peer review
- `working/design-philosophy.md` — Unix philosophy, single-writer-per-file, etc.

---

## Goals

1. **Multi-day persistence.** The orchestrator runs across many days without Matt's intervention.
2. **Crash-safe.** A power outage, machine reboot, or process kill doesn't lose progress. Resume picks up where it left off.
3. **Monitorable from a fresh Claude Code session.** Matt opens Claude Code with no shared context; runs a skill; gets full status in <60 seconds.
4. **Blocking-question detection.** When an agent files a blocking question, the orchestrator pauses the affected stage and surfaces it; Matt's check pulls it forward.
5. **Resource-tight.** When the orchestrator finishes (or Matt kills it), no orphan processes survive. iTerm tabs the orchestrator opened are explicitly closed.
6. **Self-generating prompts.** When a vocabulary gap or schema question surfaces, the orchestrator can generate ad-hoc agent prompts to address it (or pause and ask Matt).
7. **Multi-pass loop.** Stages can re-trigger each other (Pass 1 completion → re-run cross-book-entity-reconciler → may surface new alias additions → re-run alias-resolver).

---

## Process model

**Critical clarification — the orchestrator daemon is NOT a Claude Code session.** It's a Python process that shells out to `claude --print --agent <name>` (headless Claude CLI invocations) for each agent run. Each agent invocation is a fresh, bounded Claude session that dies when its work completes. The orchestrator's process never holds a Claude conversation — it's pure Python with subprocess calls. **This sidesteps Claude Code session limits entirely** because the orchestrator isn't IN a session; only the per-agent invocations are, and they're short-lived.

This is the same pattern `wiki-pass2.sh` uses for Stage 1's mechanical-extractor calls — each invocation is a separate `claude --print --agent <name>` process. Proven pattern, scales to multi-day runs.

**Three layers:**

```
LAYER 1 — Long-lived orchestrator daemon  (one Python process)
    ├── Reads fleet-config.yaml on start
    ├── Walks the stage DAG
    ├── Writes state continuously to working/fleet-stats/
    ├── Logs to working/fleet-stats/orchestrator.log
    ├── For each agent invocation: subprocess.run(["claude", "--print", "--agent", ...])
    │     captures output, parses status, records stats
    └── Each subprocess is a self-contained bounded Claude session that dies on completion

LAYER 2 — Per-agent workers  (ephemeral headless Claude CLI processes)
    ├── Spawned by Layer 1 via subprocess.run / subprocess.Popen
    ├── Each is `claude --print --agent <name> < prompt-input.json`
    ├── Reads its prompt + inputs from disk (Layer 1 prepared these)
    ├── Writes its output (JSONL/markdown) to disk
    ├── Exits when done; Layer 1 captures stdout/stderr + exit code for stats
    └── Bounded context per invocation — no session-limit issues

LAYER 3 — Monitoring (on-demand, no shared state with Layers 1-2)
    ├── Triggered by Matt opening a fresh Claude Code session and running /check-fleet
    ├── That fresh session reads state files written by Layer 1
    ├── Renders status summary, surfaces blocking questions, supports follow-up verbs
    └── Session ends when Matt finishes monitoring; daemon keeps running

LAYER 4 — Manual stage execution (no daemon, no orchestrator)
    ├── Each stage is also runnable as a standalone shell script (per-stage scripts)
    ├── `weirwood stage stage-1` runs ONE stage's worth of work without the daemon
    ├── Same agent invocations, same stats CSV writes, same artifacts
    └── Lets Matt yank any stage out of the chain for direct control
```

**Layer 1 + Layer 2 + Layer 3 are independent processes** — Matt's interactive Claude Code session (Layer 3) has no link to the orchestrator daemon (Layer 1) except through on-disk state files. The skill loads only the state it needs; doesn't keep a long conversation; closes when done.

**Layer 4 is the "no-daemon escape hatch"** — every stage is liftable. Matt can run any stage manually as a per-stage script even if the daemon doesn't exist. The daemon is a convenience that auto-chains stages with auto-pauses; the per-stage scripts do the actual work.

---

## Persistence: tmux is the answer

The orchestrator daemon runs **inside a tmux session**. Why tmux:

- Survives terminal close, ssh disconnect, machine sleep (with the right config)
- Standard, battle-tested, every Mac has it
- Detach (Ctrl-b d) and reattach (`tmux attach -t fleet`) at will — Matt can attach to see live logs, detach to walk away
- Single command to kill cleanly (`tmux kill-session -t fleet`)
- One session can hold multiple windows for parallel work — though we'll use a single window for simplicity

**Why not nohup / disown:** tmux gives interactive reattach which is much nicer than `tail -f` of a log.

**Why not systemd / launchd:** overkill for a personal project; Matt would have to learn the config; tmux is more transparent.

**Why not a long-running iTerm tab:** if iTerm dies (it does occasionally), the orchestrator dies. tmux is iTerm-independent.

**Optional iTerm integration:** the orchestrator CAN open iTerm tabs for live-view of specific waves (e.g., during Stage 5's Pass 1 catch-up, where mechanical-extractor runs in 3-5 parallel tabs because that's the existing pattern). Those tabs are explicitly closed when their wave completes — `osascript -e 'tell application "iTerm2" to tell current window to close current tab'`. Tab cleanup is the orchestrator's responsibility, not the user's.

---

## State files (everything is on disk)

The orchestrator writes its full state to disk continuously. A fresh Claude Code session can reconstruct the entire pipeline status from these files alone.

**State files (under `working/fleet-stats/`):**

| File | Purpose | Updated by |
|------|---------|------------|
| `orchestrator-state.json` | Current state: which stage is in-progress, which wave, current agent invocations, last heartbeat timestamp | Layer 1 (every ~30 seconds) |
| `orchestrator.log` | Append-only human-readable log of every event | Layer 1 (continuously) |
| `stage-<N>-<name>.csv` | Per-agent invocation stats (matches the fleet-orchestration-plan.md schema) | Layer 1 (after each worker exits) |
| `stage-<N>-summary-<run-id>.md` | Synthesized stage report (written by `fleet-stats-reviewer`) | fleet-stats-reviewer |
| `wave-<N>-<wave-id>.json` | Per-wave manifest (which agents in this wave, their target inputs, their status) | Layer 1 |
| `blocking-questions.jsonl` | Filtered view of `working/wiki-pass2/questions-for-matt.jsonl` showing only `blocking: true` rows | Layer 1 (computed periodically) |
| `last-checkpoint.json` | Resume point if orchestrator crashes | Layer 1 (every wave boundary) |

**`orchestrator-state.json` shape:**

```json
{
  "version": "v1",
  "started_at": "2026-04-28T12:00:00Z",
  "last_heartbeat_at": "2026-04-28T18:42:13Z",
  "pid": 12345,
  "tmux_session": "fleet",
  "current_stage": "stage-2",
  "current_stage_name": "Stage 4 Classification — prose-edge-classifier",
  "current_wave": 47,
  "total_waves": 95,
  "active_agents": [
    {"agent": "prose-edge-classifier", "target": "houses-other-h-w", "started_at": "2026-04-28T18:39:00Z", "pid": 12678}
  ],
  "completed_stages": ["stage-0", "stage-1"],
  "blocking_questions_count": 0,
  "rate_limit_pauses_active": false,
  "next_action": "complete-wave-47-then-advance-to-wave-48"
}
```

The `last_heartbeat_at` is the freshness signal. If a fresh Claude Code session sees that timestamp is more than 5 minutes stale and `current_stage` is not `idle`, the daemon may have crashed.

---

## Monitoring skill (Layer 3)

A new Claude Code skill at `.claude/skills/check-fleet/` (project-level skill).

**Trigger:** Matt opens a fresh Claude Code session, types `/check-fleet`, the skill runs.

**What the skill does:**

1. Reads `working/fleet-stats/orchestrator-state.json`
2. Computes time-since-last-heartbeat
3. Reads `working/fleet-stats/blocking-questions.jsonl`
4. Reads the latest few stage-summary files
5. Reads the tail of `orchestrator.log` (last 100 lines)
6. Renders a one-page status report to the user

**Output to user looks like:**

```
═══════════════════════════════════════════════════════════
  FLEET STATUS — 2026-04-28T18:45:00Z
═══════════════════════════════════════════════════════════

Started: 2026-04-28T12:00:00Z (6h 45m ago)
Last heartbeat: 32 seconds ago ✓ (HEALTHY)
Tmux session: fleet (attach with `tmux attach -t fleet`)

CURRENT STAGE: Stage 2 — prose-edge-classifier
  Wave 47 of 95 (49% complete)
  Active agents: 5 (prose-edge-classifier on 5 buckets)
  Estimated completion: 2026-04-28T22:30:00Z (3h 45m)

COMPLETED STAGES:
  ✓ Stage 0 — Foundation (12s, $0)
  ✓ Stage 1 — Quality Audits (1h 02m, $34.20)

BLOCKING QUESTIONS: 0 ✓

RECENT EVENTS (tail of log):
  18:39:00 - Started prose-edge-classifier on houses-other-h-w
  18:42:13 - heartbeat
  ...

RECOMMENDED ACTION: monitor only. No human input required.
═══════════════════════════════════════════════════════════

To attach for live view: `tmux attach -t fleet`
To stop the orchestrator: `tmux send -t fleet "stop" Enter`
```

**When blocking questions exist:**

```
BLOCKING QUESTIONS: 2 ⚠

  Q1: q-2026-04-28-prose-edge-batch3-007 (asked 2h ago)
    Type: vocabulary-gap
    Bucket: characters-house-frey-a-l
    Question: "Wiki encodes a 'sworn-by-marriage' relationship for House Frey
    that doesn't fit any current edge type. Should we add SWORN_BY_MARRIAGE
    or fold under SWORN_TO with a [marriage] qualifier?"
    Context: 47 instances across 12 nodes

  Q2: ...

ORCHESTRATOR PAUSED stage-2 wave 49 pending these answers.

To answer: edit working/wiki-pass2/questions-for-matt.jsonl, set
`resolution` field; orchestrator will detect and resume.
```

**Skill implementation** (`.claude/skills/check-fleet/SKILL.md`):

```markdown
---
name: check-fleet
description: "Check status of the autonomous fleet orchestrator. Reads state files, surfaces blocking questions, renders one-page status. Run from a fresh Claude Code session."
---

You are checking on the fleet orchestrator.

1. Read /Users/mnoth/source/asoiaf-chat/working/fleet-stats/orchestrator-state.json
2. Read /Users/mnoth/source/asoiaf-chat/working/fleet-stats/blocking-questions.jsonl (may be empty)
3. Read the last 100 lines of /Users/mnoth/source/asoiaf-chat/working/fleet-stats/orchestrator.log
4. Read the latest /Users/mnoth/source/asoiaf-chat/working/fleet-stats/stage-*-summary-*.md (most recent only)
5. Compute time-since-last-heartbeat from orchestrator-state.json::last_heartbeat_at
6. Render the status report in the format documented in working/fleet-runtime-architecture.md § "Monitoring skill"

Do not modify any files. This skill is read-only.

If the orchestrator state file does not exist, report "fleet not running" with instructions to start it: `weirwood fleet start`.

If last_heartbeat_at is more than 5 minutes stale and current_stage != "idle", warn that the daemon may have crashed and recommend `tmux attach -t fleet` to investigate.
```

---

## Shell launcher (extends `scripts/weirwood.zsh`)

New subcommand: `weirwood fleet <action>`.

```bash
weirwood fleet start          # Launches the orchestrator in a new tmux session
weirwood fleet status         # CLI quick status (subset of /check-fleet skill output)
weirwood fleet attach         # tmux attach -t fleet (live view)
weirwood fleet stop           # Graceful shutdown — orchestrator finishes current wave then exits
weirwood fleet kill           # Hard kill (last resort)
weirwood fleet smoke          # Run smoke tests against components without launching the full pipeline
weirwood fleet resume         # Resume from last checkpoint (used after crash)
```

**`weirwood fleet start` does:**

1. Checks for existing `fleet` tmux session — refuses to start if one exists (use `attach` or `stop` first)
2. Reads `scripts/fleet-config.yaml` to determine starting stage (default: stage-0 if no checkpoint, else resume from checkpoint)
3. Launches `tmux new-session -d -s fleet 'python3 scripts/fleet-orchestrator.py --config scripts/fleet-config.yaml --resume-from-checkpoint'`
4. Confirms the session started; prints how to attach
5. Returns control to Matt's shell immediately

**`weirwood fleet stop` does:**

1. Sends a SIGTERM to the orchestrator process (or writes a `stop-requested` flag the orchestrator polls)
2. Orchestrator finishes current wave, writes final state, exits
3. Tmux session ends
4. iTerm tabs the orchestrator opened during the run get closed via the orchestrator's cleanup hook
5. Confirms shutdown to Matt

**Resource cleanup contract:**
- Orchestrator process catches SIGTERM and SIGINT, runs cleanup hook
- Cleanup hook: kill any spawned worker subprocesses, close iTerm tabs the orchestrator opened, write final state file, log shutdown event
- Tmux session exit triggers if the orchestrator process exits (single-process session)

---

## Self-generating prompts (rare, but supported)

When an agent surfaces a need that wasn't anticipated (vocabulary gap, schema question, novel cross-identity case), the orchestrator has three responses:

**Response A (most cases):** File the question to `questions-for-matt.jsonl` as blocking, pause the affected stage, surface in `/check-fleet`. Matt resolves manually.

**Response B (vocabulary gap with strong evidence):** Orchestrator can spawn an ad-hoc `vocabulary-gap-proposer` agent that:
- Reads the gap evidence (≥3 example sentences)
- Proposes the addition to `reference/architecture.md` § "Wiki Infobox Fields → Edge Type Mapping" (writes a markdown diff to `working/curation/proposed-architecture-additions/<id>.md`)
- Pauses pending Matt's review

This is NOT a recursive subagent call — it's the orchestrator-driven pattern (orchestrator spawns the proposer, reads its output, decides what to do).

**Response C (operational only):** Orchestrator can re-trigger an upstream stage if downstream surfaces an upstream problem. Example: if Stage 4 prose-edge-classifier surfaces 100+ vocabulary-gap escalations, that's a signal to pause Stage 4, run `vocabulary-gap-proposer` on the batch, get architecture.md updated, then re-run Stage 4 from where it stopped.

The fleet-config.yaml encodes which responses are allowed for which agents' question types. Conservative default: most go to Response A (ask Matt). Response B/C are explicitly enabled for known-safe cases.

---

## Multi-pass loops

The fleet plan's stage DAG has explicit dependencies but is mostly linear. Real-world iteration may want loops:

```
Pass 1 ACOK completes
    ↓
cross-book-entity-reconciler runs (now has AGOT + ACOK)
    ↓
proposes 50 new aliases
    ↓
Matt reviews; approves 40
    ↓
Python script applies aliases to nodes
    ↓
alias-resolver re-runs (more aliases now resolvable)
    ↓
cross-refs re-build (broken-link rate drops further)
    ↓
back into Stage 4 — re-run prose-edge-classifier on buckets that previously had escalations
    ↓
Stage 4 promote re-runs (idempotent — only emits new-since-last-promote)
```

The orchestrator supports this by:
1. Encoding stage triggers in `fleet-config.yaml` (e.g., "after stage-6, if cross-book-entity-reconciler proposed N≥10 aliases, re-trigger stage-0")
2. Idempotent stage execution — a re-trigger of a previously-completed stage processes only the deltas

This is "soft loops" — Matt can also disable them in config if he wants strict linear progression.

---

## Smoke tests (validate before the multi-day run)

Before launching the full multi-day orchestration, run these in order. Each is small, cheap, and validates one part of the architecture.

| # | Smoke test | What it validates |
|---|------------|-------------------|
| 1 | `weirwood fleet smoke alias-resolver` | Stage 0 foundation: alias-resolver script runs, output schema is valid |
| 2 | `weirwood fleet smoke quality-audit-one` | Stage 1: invoke ONE quality auditor (schema-drift-auditor), verify report writes correctly |
| 3 | `weirwood fleet smoke prose-edge-one-bucket` | Stage 2a: invoke prose-edge-classifier on ONE bucket, verify output JSONL + stats CSV row |
| 4 | `weirwood fleet smoke peer-review-one-bucket` | Stage 3: invoke prose-edge-reviewer on smoke 3's output, verify verdict report |
| 5 | `weirwood fleet smoke stats-summary` | fleet-stats-reviewer: runs on synthetic stage-0 stats, verifies summary report shape |
| 6 | `weirwood fleet smoke monitor-skill` | Layer 3: simulate a partial state, run the skill, verify output rendering |
| 7 | `weirwood fleet smoke crash-resume` | Layer 1: kill the orchestrator mid-stage, run `weirwood fleet resume`, verify checkpoint pickup |
| 8 | `weirwood fleet smoke iterm-cleanup` | Layer 1: orchestrator opens iTerm tab, then cleans it up; verify no orphan tabs |

Pass all 8 smokes before Matt walks away from the multi-day run.

---

## Stages are independently liftable (the key Unix-philosophy benefit)

Each stage is a **self-contained mini-orchestration**: a finite set of agents + Python composers + on-disk inputs + on-disk outputs. The fleet orchestrator chains them, but each stage **does not depend on the orchestrator existing**.

This means:

**Matt can run any stage manually.** Want to run Stage 1 quality audits without the daemon? Open a fresh Claude Code session, ask the orchestrator (you, the main session) to invoke the four quality auditors in parallel. Each auditor reads from disk, writes to disk, exits. No daemon needed. Same artifacts, same stats CSV (manually appended), same reports.

**Matt can yank a stage out of the chain.** If Stage 4 surfaces concerning patterns and Matt wants to interleave a manual review pass before Stage 4 promote — fine. The fleet orchestrator's `fleet-config.yaml` lets him disable any stage; the prerequisites and outputs of every stage are documented; stages downstream just wait for their inputs to materialize, and they don't care whether those inputs came from the orchestrator or from Matt running things by hand.

**Matt can override per-stage parallelism, retries, or wave size.** Run prose-edge-classifier with wave size 1 (sequential, one bucket at a time) for the first 5 buckets, then crank to wave size 5 once the pattern is clear. Each stage is configured independently.

**Each stage has its own README.** The path forward: per-stage runbooks under `working/runbooks/fleet/stage-<N>-<name>.md` that document:
- Inputs (which files must exist before this stage runs)
- Agents involved + which prompt files
- Outputs (what files this stage writes)
- Stats CSV column conventions (same shared schema)
- How to run the stage manually (the Claude Code orchestrator command Matt can paste)
- How to validate the stage's output before promoting

When Matt wants direct control, he reads the stage runbook + invokes manually. When he wants to walk away, the daemon reads the same stage definitions and runs them automatically.

**Why this matters for risk management.** A multi-day autonomous run is a high-trust operation. The "stages are liftable" property means Matt can reduce trust progressively — start with manual stage-by-stage, then automate the stages that proved well-behaved, then leave the daemon running only for stages that have shown reliability across multiple manual runs. Stages that consistently surface novel issues (e.g., voice-analyzer on a new POV character) stay manual longer.

**The contrast.** A monolithic orchestrator design would make this impossible — you'd be all-in on the daemon or nothing. The Unix-style design means the daemon is an optimization, not a requirement.

---

## Resilience: what happens when things go wrong

Failures happen at four scales. The architecture isolates each so a problem at one scale doesn't propagate up.

### Scale 1 — Agent-level (one agent invocation fails)

Each agent invocation is a separate `claude --print --agent <name>` subprocess. Failure modes:
- **Rate limit** — orchestrator detects via `"rateLimitType"` JSON marker; backs off; retries (3 attempts, exponential backoff)
- **Token limit / context overflow** — usually means a bucket is too large; orchestrator marks the bucket `status=size-overflow`, skips for this run, surfaces it for manual chunking
- **Hang / no output** — orchestrator timeout (configurable per-agent, default 15 min) kills the subprocess and retries

A failed agent invocation does NOT stop the wave. Other parallel invocations in the wave keep running. The failed one logs `status=fail` in the stats CSV with `error_message`, and the orchestrator decides retry/skip/escalate based on policy.

### Scale 2 — Wave-level (an entire wave gets blocked)

A wave is N agent invocations running in parallel. If the rate-limit hits affect all of them (the API itself is rate-limiting), the whole wave pauses:
- Orchestrator detects ≥3 rate-limit hits in one wave → wave-pause
- Pauses for the rate-limit reset duration (parsed from error response, default 5 min)
- After pause, retries failed invocations; resumes the wave
- If pause exceeds N hours (config), pauses the entire stage and waits for Matt

Other STAGES are unaffected. Pass 1 catch-up running in `fleet-pass1-acok` tmux session keeps going even if `fleet-stage4` is paused.

### Scale 3 — Stage-level (one stage fails entirely)

Each stage runs in its own tmux session / its own Python process. A stage failure is isolated:
- If `fleet-stage4` exits with error, `fleet-pass1-acok` continues
- The stage's checkpoint file (`working/fleet-stats/last-checkpoint.json`) records where it stopped
- Restarting the stage (`weirwood fleet stage stage-4 --resume`) picks up from the checkpoint — idempotent

### Scale 4 — Orchestrator-level (daemon crashes)

The orchestrator daemon is a Python process. It can crash for OS-level reasons (OOM kill, machine reboot, signal):
- All state is on disk continuously (orchestrator-state.json, log, stats CSVs, checkpoint)
- Restart is one command: `weirwood fleet resume` — reads checkpoint, resumes
- No work is lost beyond what was in-flight at crash time (in-flight invocations are retried)
- Tmux session is the daemon's container; if tmux dies (rare), the daemon dies; same recovery via resume

### The coordinator pattern (optional supervisor)

A lightweight `fleet-coordinator.py` can supervise multiple stage processes:

```
fleet-coordinator (lives in tmux session "fleet-coord")
    ├── spawns:  fleet-stage-1 (tmux: fleet-stage-1) ──┐
    ├── spawns:  fleet-stage-2 (tmux: fleet-stage-2) ──┤
    ├── spawns:  fleet-pass1-acok (tmux: fleet-pass1) ─┤
    ├── reads:   each session's heartbeat            ─┤  parallel work
    ├── if heartbeat stale > 5 min:                  ─┤
    │       attempts to attach + check status        ─┤
    │       if dead: respawn from checkpoint         ─┤
    │       if hung: kill + respawn from checkpoint  ─┘
    │       if persistent: surface to /check-fleet
    └── exits when all spawned stages complete
```

This is the "spin up another process if one dies" pattern Matt asked about. The coordinator is what does the respawning.

**Two modes:**
- **Coordinator-managed (autonomous):** one coordinator supervises multiple stages with auto-respawn. Multi-day unattended.
- **Coordinator-less (manual):** Matt starts each stage himself in its own tmux session. If one dies, he restarts it. Simpler; appropriate when stages are still maturing.

### Concrete failure → recovery cheatsheet

| Failure | Detected by | Auto-recovery | Manual fallback |
|---------|-------------|---------------|-----------------|
| Rate limit on one agent | orchestrator polling | Retry 3× with backoff | None needed |
| Rate limit across wave | `≥3 hits in wave` | Pause wave, resume after reset | Adjust wave size in config |
| Agent hang (>15 min) | orchestrator timeout | Kill + retry | Investigate via tmux attach |
| Stage process exits | coordinator polling | Respawn from checkpoint | `weirwood fleet stage <N> --resume` |
| Daemon crash (OOM, etc.) | tmux session ends | Coordinator respawns OR Matt resumes | `weirwood fleet resume` |
| Persistent agent failure (3 retries fail) | stats CSV `status=fail` rows | None — surface to Matt | Investigate, fix prompt or skip bucket |
| Blocking question filed | orchestrator-state.json flag | Pause stage, surface to skill | Matt answers via `/check-fleet answer Q-ID` |
| Disk full | I/O errors | None — surface | Free space, then `--resume` |
| Anthropic API outage | repeated network errors | Pause indefinitely; re-test every 5 min | Wait for Anthropic |

### What requires Matt's intervention

Most failures auto-recover. Things that genuinely need a human:
- **Persistent agent failure across all retries** — usually means a bug in the agent prompt or a malformed bucket; needs investigation
- **Blocking questions filed by an agent** — only Matt can answer
- **Cost overrun beyond budget** — orchestrator pauses, asks Matt to authorize continued spend
- **Schema-evolution decisions** — when an agent surfaces a vocabulary gap with strong evidence, orchestrator pauses pending Matt's approval

Everything else: the orchestrator handles. Matt's `/check-fleet` shows what's happening; if everything's green, Matt walks away.

### Design rationale

The Unix philosophy in disguise: each process is small, focused, replaceable. A wave-level orchestrator doesn't know about Pass 1 catch-up; a Pass 1 process doesn't know about Stage 4. Failure in one is invisible to the others. The coordinator is just a cheap supervisor — if even the coordinator dies, the underlying state files survive on disk and Matt can manually `weirwood fleet resume <stage>` for each.

The opposite design (single mega-orchestrator running everything in one process) would propagate any failure to everything. We explicitly reject that.

---

## Two orchestration modes — Daemon vs iTerm-scripts (pick per work type)

Multiple ways to drive the fleet. The core artifacts (agent prompts, stats CSV, per-stage scripts, `/check-fleet` skill) are identical across modes; only the orchestration layer differs.

### Mode A — Python daemon (autonomous, multi-day)

Already documented above. One Python process supervises the whole DAG, auto-chains stages, auto-respawns on failure, auto-retries rate-limited agents. tmux session for persistence. Matt walks away.

**Use for:** long batch work where Matt won't be around, well-understood stages with low novelty surprise risk (e.g., promoting Stage 4 prose-edge classifications across 472 buckets after the prompt is well-tested).

### Mode B — iTerm-script orchestration (manual, interactive)

Each stage has a shell script Matt runs by hand from iTerm. The script opens N iTerm tabs (one per parallel agent invocation, like the existing `weirwood wiki core 4 9` mechanical-extraction pattern), each tab runs `claude --print --agent <name>` against its assigned target. Stats logged to disk same as daemon mode. Tab closes (or shows summary) when done.

```
                  weirwood fleet stage <N>
                            │
                            ▼
                    scripts/fleet/stage-N-<name>.sh
                            │
                  ┌─────────┼─────────┐
                  ▼         ▼         ▼
           ┌──────────┐ ┌──────────┐ ┌──────────┐
           │ iTerm    │ │ iTerm    │ │ iTerm    │
           │ tab 1    │ │ tab 2    │ │ tab 3    │
           │ agent X  │ │ agent X  │ │ agent X  │
           │ on bkt A │ │ on bkt B │ │ on bkt C │
           └──────────┘ └──────────┘ └──────────┘
                            │
                            ▼
                    same stats CSV
                    same on-disk artifacts
                    same /check-fleet skill works
```

**Use for:** novel stages where Matt wants to watch (visible scrolling per-tab), short batches he's actively monitoring, the chat UI build phase (interactive iteration), one-off recovery passes (like Tier 1 + Tier 2 recovery did this session — those were essentially mode-B runs of the existing pipeline scripts).

### Both modes share

- Same agent prompts in `.claude/agents/`
- Same stats CSV schema in `working/fleet-stats/stage-<N>-<name>.csv`
- Same per-stage scripts under `scripts/fleet/`
- Same `/check-fleet` slash command (works against the stats files regardless of which mode wrote them)
- Same blocking-question protocol via `working/wiki-pass2/questions-for-matt.jsonl`
- Same artifact format on disk (skeleton/, prose/, prose-edges/, etc.)

The DAEMON is just "run the iTerm-scripts in sequence, automatically, with auto-respawn + auto-retry baked in." The iTerm-scripts are the floor; the daemon is an optimization on top of them.

### Mixing the two modes

Pick per work type:

| Work | Recommended mode | Why |
|------|------------------|-----|
| Pass 1 mechanical extraction (Pass 1 catch-up across 4 books) | **Mode B (iTerm-scripts)** | Already the existing pattern. Matt watches. Wave-based. Multi-day overall but each wave is bounded. |
| Stage 0 foundation scripts (alias-resolver, cross-refs, edge-candidate-generator) | **Mode B** | Pure Python, runs in seconds. No need for daemon. |
| Stage 1 quality audits (4 read-only auditors) | **Mode B** | Short. Matt wants to read the audit reports. |
| Stage 2 prose-edge-classifier across 472 buckets | **Mode A (daemon)** OR **Mode B** | Mode A if Matt's away; Mode B for first 5 buckets to validate the pattern, then Mode A for the remaining 467. |
| Stage 3 peer review | **Mode B** | Short. Matt wants to see the verdicts as they come in. |
| Stage 4 promote (Python only) | **Mode B** | Pure Python, atomic, runs in seconds. |
| Pass 3-6 (long batches) | **Mode A** | Multi-day; auto-chain across passes. |
| UI build fleet | **Mode B** (mostly) | Interactive iteration is the job. |
| Tier 3 chronology | **Mode A or B** | Either works; depends on whether Matt's around. |

**The shell launcher (`scripts/weirwood.zsh`) supports both via the same `weirwood fleet stage <N>` command** — by default it runs in Mode B (foreground iTerm-tabs), with `--daemon` flag to enable Mode A. Matt picks per invocation.

### Per-stage script template (Mode B)

```bash
#!/usr/bin/env bash
# scripts/fleet/stage-N-<name>.sh
#
# Runs ONE stage of the fleet. Mode B (iTerm-tab parallelism).
# Reads stage-N's agent + target manifest from working/fleet-stats/<stage>-config.json.
# Opens N iTerm tabs, one per agent invocation.
# Each tab logs to working/fleet-stats/stage-N-<name>.csv on completion.
# Idempotent — already-completed targets skipped via manifest checks.
#
# Usage:
#   scripts/fleet/stage-N-<name>.sh           # run all targets in waves of $WAVE_SIZE
#   scripts/fleet/stage-N-<name>.sh <bucket>  # run one specific target
#   scripts/fleet/stage-N-<name>.sh --resume  # pick up incomplete targets

set -euo pipefail
STAGE_NUM=N
STAGE_NAME="<name>"
WAVE_SIZE="${WAVE_SIZE:-3}"  # default 3 parallel iTerm tabs

# ... wave loop, manifest read, iTerm tab spawning,
#     stats CSV append, manifest update on completion ...
```

This pattern already exists for mechanical extraction (`weirwood mechanical <book> <wave-size> <wave-count>` etc. in `scripts/weirwood.zsh`). The new fleet stages follow the same shape — one script per stage under `scripts/fleet/`.

### Why both modes matter

The daemon is great when it's working but expensive to debug when it's not. The iTerm-scripts are unbeatable for first-time runs of a stage where Matt wants to see what the agent actually does. The fleet plan is:

1. **First run of any stage: Mode B.** Run the first 1-3 targets in iTerm tabs. Watch the agent's output. Inspect the stats CSV row + artifact output. Verify it's sane.
2. **Routine runs of validated stages: Mode A.** Once the stage is well-understood, the daemon can chain it into the larger DAG with auto-retry and auto-respawn.
3. **Recovery / debug / one-off: Mode B.** Always the escape hatch. Even if the daemon is running, Matt can spin up a single iTerm-tab `claude --print --agent <name>` for spot-checks.

This gives the **per-stage liftability** property explicit operational expression: every stage is a script Matt can run by hand at any time, regardless of daemon state.

---

## What this architecture deliberately does NOT do

- **Web dashboard.** The skill renders a one-page report; that's enough. Web UIs add a build step + a server + auth.
- **Email/Slack notifications.** Matt monitors via the skill on his own cadence; we don't push.
- **Cloud distribution.** Single-machine orchestration. The graph is small enough.
- **Dynamic scaling.** Wave size is configured in fleet-config.yaml, not auto-tuned. If the user-facing rate limit shifts, manual config tweak.
- **Per-agent retry policy customization.** All agents share one retry policy (3 retries, exponential backoff). Bespoke policies per agent are a "we'll see if we need it" item.

---

## Implementation order (concrete next sessions)

This architecture is ~80% design / 20% built. Concrete next-session tasks:

### Session N+1: Foundation + first smoke
- Build `scripts/wiki-pass2-build-alias-resolver.py` (Stage 0 foundation, no agents)
- Run smoke #1 manually (just running the Python script)
- Verify alias-resolver.json output is sane
- Re-run cross-refs with alias resolution; confirm broken-link rate drops as predicted

### Session N+2: Stats infrastructure
- Build `scripts/fleet_stats.py` — Python helper for record_invocation / aggregate_stage
- Run smoke #5 with synthetic data
- Verify stats CSV schema is parseable

### Session N+3: Single-stage orchestration
- Build a minimal `scripts/fleet-orchestrator.py` that runs ONLY stage-1 (the four quality auditors in parallel)
- Smoke tests #2, #6
- This is the first "the orchestrator can drive multi-agent waves" validation

### Session N+4: tmux + skill scaffolding
- Build `weirwood fleet start/status/stop` shell commands
- Build the `/check-fleet` skill
- Smoke test #7 (crash-resume) and #8 (iTerm cleanup)

### Session N+5+: Stage 4 and beyond
- Once Layer 1+3 plumbing works on Stage 1 quality audits, scale up
- Add Stage 0 stages, Stage 2a prose-edge classification, Stage 3 review, Stage 4 promote
- THEN start the multi-day run with confidence

**Until Session N+5, the orchestrator is "in development" — Matt's not walking away for days yet.**

---

## What I can build right now (this session)

In descending order of cost-to-build:

1. **`scripts/wiki-pass2-build-alias-resolver.py`** — Stage 0 foundation script. Pure Python, ~150 lines. **CAN BUILD NOW.** Smoke-testable.

2. **`.claude/skills/check-fleet/SKILL.md`** — the monitoring skill. **CAN BUILD NOW** as a stub that reads the state file once it exists. Real value comes after orchestrator-state.json starts getting written.

3. **`scripts/weirwood.zsh` extension** — `weirwood fleet status` (CLI quick status). **CAN BUILD NOW** as a placeholder; full implementation depends on orchestrator existing.

4. **Smoke test harness** — `weirwood fleet smoke <test>`. **CAN BUILD AS STUB** that runs the alias-resolver test.

5. **`scripts/fleet-orchestrator.py`** — the actual daemon. **TOO BIG FOR ONE SESSION.** ~800-1500 lines, needs careful design across multiple sessions. Stub now; build incrementally.

Recommendation for tonight: build #1 + #2 + #3 + smoke test #1. That gets the foundation in place + the monitoring scaffolding + a real demonstration that Stage 0 works. Stage 0 alone unlocks an immediate broken-link-rate improvement on the existing graph (the alias-resolver fix from earlier in this session — the Brienne_of_Tarth case).
