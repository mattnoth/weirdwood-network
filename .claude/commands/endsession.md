Run the end-of-session checklist for the Weirwood Network project. Do each step in order:

1. **Write session detail file** — Create `working/session-details/session-NNN.md` (use the next session number from worklog.md). This is the **human-facing** full narrative: everything that happened, what was explored, what was tried, what was rejected, coverage numbers, reasoning behind decisions, the full conversation arc. Write this for a person documenting the process, not for an agent. **Scale depth to the session type:** Design sessions, architecture decisions, and novel problem-solving deserve full narrative. Execution-heavy sessions (running extraction waves, batch operations) should focus on what was *decided* and what *surprised* — not narrate every repetitive operation. A session that ran 50 mechanical extractions needs a paragraph on the results and any anomalies, not a play-by-play.

2. **Update worklog.md** — Add a **concise** session log entry (~20-30 lines max) to the Session Log section. This is **agent-facing** — future sessions load this file, so keep it tight. Format:

   ```
   ### Session N — Short Title (YYYY-MM-DD)
   **Detail:** `working/session-details/session-NNN.md`
   **Changes made:** (bullet list of files changed and what changed — facts, not narrative)
   **Decisions:** (one paragraph of key decisions, compressed)
   **What's next:** (bullet list of next actions, with continue prompt paths if they exist)
   ```

   Also update the Current State checkboxes and Extraction Pipeline checklist if any items were completed or status changed.

3. **Manage continue prompts** —
   - **Create** new ones if work tracks are mid-flight. Write to `progress/continue-prompts/{date}-{short-description}.md` with enough context for a fresh agent to pick up the work. Reference the path from the worklog entry's "What's next" section. **Also link it from todos.md** — add a `→ continue:` line under the relevant todo item so `/continue` can find it by priority.
   - **Delete** any continue prompts that were completed this session. Also remove the `→ continue:` line from the corresponding todo in todos.md (and check the todo item itself if the work is fully done).

4. **Update progress/** — If scratch notes accumulated, add them to `progress/scratch-notes.md` tagged with source. If extraction waves ran, update the relevant `progress/pass1-{book}.md` file.

5. **Update working/todos.md** — If new TODOs surfaced during the session, add them to the appropriate section.

6. **Archive if needed** — If the Session Log section of worklog.md exceeds ~150 lines, archive older sessions to `working/worklog-archives/archiveNNN.md`. The worklog keeps Current State, Active Decisions, Ideas & Backlog, Principles, and only the most recent 1-2 session entries.

7. **Verify .gitignore** — Confirm sources/raw/ and sources/chapters/ are still in .gitignore. Run `git status` and flag if any copyrighted content is showing as untracked.

8. **Show session summary** — Print a brief summary of what was accomplished and what the next session should pick up.
