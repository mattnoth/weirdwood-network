Check the status of the Weirwood Network's fleet orchestrator and surface anything that needs your attention.

This command runs in a fresh Claude Code session — the assumption is you don't have project context loaded yet and want a quick read on what's happening with any in-progress orchestration. The fleet orchestrator (when it exists, see `working/agent-fleet-specs/fleet-runtime-architecture.md`) writes state to disk continuously; this command reads those state files and synthesizes a one-page report.

**You (Claude) should:**

1. **Quick orient.** Read `CLAUDE.md` (project overview) and `worklog.md` (Current State section only — first 100 lines) to understand the project shape. Don't load the full worklog; load just enough to render a status.

2. **Check fleet daemon state.** Read `working/fleet-stats/orchestrator-state.json` if it exists. If not, the daemon isn't running — say so explicitly with the command to start it (`weirwood fleet start` once that exists; otherwise say "fleet daemon not yet implemented").

3. **Compute heartbeat freshness.** From `orchestrator-state.json::last_heartbeat_at`, compute time elapsed. Flag stale (>5 min) heartbeats with a warning.

4. **Read recent stage activity.** Glob `working/fleet-stats/stage-*-summary-*.md` and read the most recent. Surface its topline + verdict.

5. **Check blocking questions.** Read `working/wiki/pass2-buckets/questions-for-matt.jsonl` (the canonical channel) and filter to rows with `blocking: true` AND `resolved_at: null`. List each with full text. These are the things waiting on Matt.

6. **Tail the log.** Read the last 50 lines of `working/fleet-stats/orchestrator.log` if it exists.

7. **Cost check.** Aggregate `cost_usd` columns from any `working/fleet-stats/stage-*.csv` files for the current orchestration run. Compare to a budget if `working/fleet-stats/budget.json` exists.

8. **Render a one-page report** in this format:

```
═══════════════════════════════════════════════════════════
  FLEET STATUS — <UTC timestamp>
═══════════════════════════════════════════════════════════

Started: <when> (<duration ago>)
Last heartbeat: <X seconds ago> <✓ HEALTHY / ⚠ STALE / 🚫 NOT RUNNING>
Tmux session: fleet (attach with `tmux attach -t fleet`)

CURRENT STAGE: <stage> — <agent> — wave <N>/<total>
  Active agents: <count>
  Estimated completion: <time>

COMPLETED STAGES THIS RUN:
  ✓ Stage 0 — Foundation (12s, $0)
  ✓ Stage 1 — Quality Audits (1h 02m, $34.20)

BLOCKING QUESTIONS: <count> <✓ if zero / ⚠ if any>
  [if any, list with question_id, type, snippet of text, and "answer with:" suggestion]

RECENT ACTIVITY (tail of log):
  [last 5-10 lines]

ANOMALIES: <count>
  [if any, list]

COST SO FAR: $<X.XX>

RECOMMENDED ACTION: <one of: monitor / answer-questions / pause / resume / no-action / investigate>
═══════════════════════════════════════════════════════════
```

9. **Offer follow-up verbs.** After the report, add a short menu the user can invoke as conversational follow-ups:

```
What next? You can ask me to:
  • show question Q-<id> — full text + context for one blocking question
  • answer Q-<id> with <resolution> — record an answer (edits questions-for-matt.jsonl)
  • show stage <N> — full latest summary for a specific stage
  • diff — what's changed since I last checked (uses `working/fleet-stats/.last-checked-<user>` timestamp)
  • dag — render the stage DAG with progress markers
  • cost trajectory — extrapolate remaining cost from current burn rate
  • spot <agent> <target> — run one agent invocation manually for spot-check
  • dry-run-next-stage — show what the orchestrator will do next + cost estimate
  • health — disk space, log sizes, zombie process check
  • pause / resume / stop — orchestrator lifecycle commands
  • continue-prompt for <reason> — generate a continue prompt for a future session
  • divert <plan> — propose a course change (skip stage, insert manual step, abort and replan)
```

**Do NOT** use the orchestrator-state file as the only source of truth — cross-check against actual on-disk state. If the state file says "stage-2 wave-47 in progress" but no stage-2 process is running (heartbeat stale + no recent log activity), the daemon may have crashed.

**Do NOT** modify any state files except `working/wiki/pass2-buckets/questions-for-matt.jsonl` (when the user asks you to record an answer). Even then, append-only edit semantics: only set the `resolved_at` and `resolution` fields on existing rows; don't touch other fields, don't reorder, don't delete.

**Do NOT** restart the orchestrator daemon yourself. Restarts go through `weirwood fleet start/resume/stop`. If the user asks for a restart, give them the exact shell command.

**Today's reality (until the orchestrator exists):**

The fleet orchestrator daemon is not yet implemented (see `working/agent-fleet-specs/fleet-runtime-architecture.md` § "Implementation order"). When this command runs today, the state files won't exist. In that case:

1. Render a fallback report based on EXISTING orchestration state:
   - Mechanical extraction stats from `working/extraction-stats/extraction-stats-*.csv`
   - Wiki Pass 2 manifests from `working/wiki/pass2-buckets/*/manifest.json`
   - Questions in `working/wiki/pass2-buckets/questions-for-matt.jsonl`
2. State explicitly that the fleet daemon isn't running and what existing-orchestration state you're reporting on instead.
3. Don't pretend the daemon exists.

This degrades gracefully: the command is useful TODAY (against existing state) and will be useful TOMORROW (against the fleet daemon's state) without changes.

**Tone:** brief, scannable, no bureaucratic preamble. The user opens this in a fresh session because they want to know "what's happening" in 10 seconds. Don't make them read a wall of text.
