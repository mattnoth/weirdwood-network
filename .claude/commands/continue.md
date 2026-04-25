Resume a specific work track from a continue prompt.

## No argument: priority-based selection

If no argument is given:

1. Read `working/todos.md` and scan for unchecked items (`- [ ]`) that have a `→ continue:` reference on the next line. These are the active work tracks with resumption context.
2. List them in the order they appear in todos.md (which reflects priority — items higher in the file are higher priority).
3. Also list any continue prompts in `progress/continue-prompts/` that are NOT referenced from todos.md (orphaned prompts — may be standalone tasks like backfills).
4. Recommend the highest-priority linked item, but ask the user which one to run.

## With argument: substring match

If an argument is given, find the matching continue prompt file in `progress/continue-prompts/`. Match by substring — e.g., "backfill" should match `2026-04-24-backfill-session-details.md`. If the match is ambiguous, list the candidates and ask. If no match, list all available prompts.

## Execution

Once a continue prompt is selected:
1. Read the full continue prompt file
2. Run the normal session startup steps from CLAUDE.md (read architecture.md, worklog.md, todos.md)
3. Execute the work described in the continue prompt
4. When done, follow the `/endsession` checklist

Argument: $ARGUMENTS
