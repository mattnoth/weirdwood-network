Emit a worker kickoff prompt for a given mission + worker slug.

## How it works

A worker is a separate Claude Code session Matt launches in a parallel window. The session does ONE bounded task (typically reconstructing one slug, classifying one bucket, etc.) and writes outputs to a per-worker scratch directory. This command produces the prompt Matt pastes into that fresh window.

## Arguments

Two arguments expected, space-separated:

- **mission-slug** (substring match) — finds the mission file in `working/agent-fleet-specs/missions/<date>-<slug>.md`. Same substring lookup as `/watcher`.
- **worker-slug** — the specific target slug for this worker (e.g., `free-folk`, `small-council`). Should match one of the entries in the mission file's worker assignment list.

Example: `/worker collision free-folk`

## Behavior

1. Resolve the mission file via substring match. If ambiguous or no match, list candidates / report missing and stop.
2. Read the mission file. Find the section titled "Worker session kickoff" (or similarly-named — the section containing the worker prompt template with `<SLUG>` placeholders).
3. Verify the worker-slug appears in the mission file's worker assignment list. If not, warn the user (but proceed — sometimes mission scope expands).
4. Output the worker kickoff prompt with **`<SLUG>` substituted for the worker-slug argument**.
5. Remind the user:
   - Paste this into a fresh Sonnet 4.6 session (Haiku 4.5 also viable for simpler worker tasks; mission file specifies).
   - One worker per session — don't multiplex.
   - The worker writes to `working/missions/<mission-slug>/worker-<worker-slug>/`.

## No argument or partial arguments

- Zero args → list active mission files; ask user to choose.
- One arg (mission only) → resolve mission, list its worker assignment slugs, ask which worker.

## Hard rules

- Do NOT actually launch the worker (no Agent tool calls). This command only produces the kickoff text.
- Do NOT modify any files (including the mission file).
- If `<SLUG>` does not appear in the mission's kickoff template, the mission file is malformed — report and stop.

Argument: $ARGUMENTS
