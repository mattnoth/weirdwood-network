# Session Results — Watcher Handoff Channel

**Convention introduced:** 2026-05-12 (Session 49b watcher proposal).

This directory holds one result file per session as a watcher-facing handoff signal. When a session completes (or hits a meaningful intermediate milestone), it writes a short summary here so any watching session can synthesize state without waiting on Matt to manually relay.

## Filename convention

`<YYYY-MM-DD>-<session-name>.md`

Examples:
- `2026-05-12-alias-backfill-round-2.md`
- `2026-05-12-orphan-batch-top-nodes.md`
- `2026-05-13-stage4-prose-edge-classifier.md`

`<session-name>` mirrors the continue-prompt filename (without date prefix) where possible, so watchers can match prompt → result.

## File contents (~10-20 lines)

```markdown
# <Session name> — Result

**Date:** <YYYY-MM-DD>
**Continue prompt:** <relative path or "ad hoc">
**Model:** <Opus 4.7 / Sonnet 4.6 / Haiku 4.5>
**Status:** <complete | partial — see notes | blocked>

## What landed
- <bullet — file or scope changed>
- <bullet>

## Headline numbers
- <metric: before → after — e.g., "Cat 1 orphan edges: 1,896 → 1,673 (−223)">

## What's next
- <next track or follow-up>

## Notes
<anything a watcher should flag — drift from the prompt, unresolved questions, scope changes, surprises>
```

## When sessions write here

- **At the end** of every session that has a continue prompt or named task scope
- **Mid-session** if a watcher is observing and the session reaches a clear milestone (e.g., promotion phase done, before script-build phase starts)
- **On blockage** — write `status: blocked` with the open question so the watcher can surface it

## What watchers do with these files

Per `working/runbooks/general-watcher.md`: a watcher's first move when checking on a session is `ls -lt working/session-results/ | head`. If a file exists for the running session, that's the canonical answer — no need to reconstruct from git diff or ask Matt to copy-paste the chat-window summary.

## Relation to other artifacts

- **worklog.md** — durable project history (5 most recent sessions in active file, rest archived). Session-results files are ephemeral — they hand off mid-flight state to watchers, not project-historical record.
- **continue-prompts/** — input side (what to do). session-results/ is the output side (what got done).
- **history/session-details/session-NNN.md** — long-form narrative for design-heavy sessions. Session-results is the terse-summary cousin.
- **working/missions/<mission>/worker-*/output.md** — per-worker outputs *within* a mission. The mission orchestrator session writes ONE session-results file that synthesizes across workers.

## Retention

Files stay until manually archived. If this dir gets noisy (>50 files), move older ones to `working/session-results/archive/<YYYY-MM>/`. No script-driven retention yet — wait until the friction is real.
