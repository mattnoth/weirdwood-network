Start (or continue) an interactive watcher session for a mission.

## How it works

The watcher is NOT a subagent invocation — it's an interactive Claude Code session that adopts the watcher role by reading `.claude/agents/watcher.md`. This command emits the kickoff prompt that turns your main session into a watcher.

## With argument: mission slug (substring match)

Find the matching mission file under `working/agent-fleet-specs/missions/` whose filename contains the argument as a substring.

- `/watcher case-collision-top-10` → looks for `*case-collision-top-10*.md`
- `/watcher case-collision` → may match multiple; surfaces candidates and asks

If exactly one file matches, output the kickoff with that file's path substituted. If multiple match, list candidates and ask which.

## No argument

List the contents of `working/agent-fleet-specs/missions/` (excluding `done/`) — i.e., active mission files — and ask which the watcher is for.

## Output (the kickoff)

After resolving the mission path, output:

```
You are the watcher for a mission. Read these in order:

1. `.claude/agents/watcher.md` — your role spec (briefing-assistant model: you read worker state from disk, answer my questions, proactively flag escalation conditions when I check in; you do NOT dispatch workers).
2. `<resolved-mission-path>` — the mission you're watching.

After reading both, report:
- Mission scope in one paragraph
- Number of workers expected + where their outputs will land
- Escalation conditions you'll proactively flag
- Any ambiguities in the mission file you'd like me to resolve up front

Then wait for my questions.
```

The user copies this output and pastes it as the first message in a fresh Opus 4.7 Claude Code session. (Or, if this command is run inside the watcher's own intended session, just follow the kickoff directly.)

## Hard rules for this command

- Do NOT actually launch a watcher (no Agent tool calls). This command only produces the kickoff text.
- Do NOT modify any files.
- If the resolved mission file has `Status: done` or `Status: archived`, warn the user before proceeding.

Argument: $ARGUMENTS
