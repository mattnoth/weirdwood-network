Run the end-of-session checklist for the Weirwood Network project. Do each step in order:

1. **Write session detail file (only if warranted)** — Session-details files are **as-needed**, not every session. Write `working/session-details/session-NNN.md` ONLY IF the session contains: design discussion, architecture decisions, novel problem-solving, an incident worth a postmortem, or substantial reasoning that doesn't fit in a worklog entry. Pure-execution sessions (extraction waves, batch operations, hygiene/cleanup) skip this step — the worklog entry is sufficient. When you do write one, it's the **human-facing** full narrative: what was explored, what was tried, what was rejected, coverage numbers, reasoning. Not for agents.

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

4. **Triage scratch + progress** —
   (a) Check for a top-level scratch file (`scratch`, `scratch.md`, or `scratch.txt` at repo root). If non-empty, surface each entry to Matt and prompt where it should land: actionable → `working/todos.md`, decision → `worklog.md` Active Decisions, resumable work track → `progress/continue-prompts/`, or discard (already covered elsewhere / no longer relevant). Empty or absent = nothing to do.
   (b) If extraction waves ran, update the relevant `progress/pass1-{book}.md` file.

5. **Update working/todos.md** — If new TODOs surfaced during the session, add them to the appropriate section.

6. **Archive worklog if > 5 entries** — Count session entries in worklog.md Session Log. If more than 5, move the oldest entries to `working/worklog-archives/archiveNNN.md` until exactly 5 remain. Each archive file holds exactly 5 entries; if the current `archiveNNN.md` is already full, start a new one (`archive(NNN+1).md`). The worklog keeps Current State, Active Decisions, Ideas & Backlog, Principles, and the 5 most recent session entries.

7. **Verify .gitignore** — Confirm sources/raw/ and sources/chapters/ are still in .gitignore. Run `git status` and flag if any copyrighted content is showing as untracked.

7b. **Verify extraction archive rules** — If extractions ran this session:
   - **Check:** Do old archives (v1, v2, etc. in `extractions/archives/`) still exist? They should NOT be deleted.
   - **Check:** Did new extractions land in canonical `extractions/mechanical/{book}/`? They should NOT be in archive folders.
   - **If violated:** Flag the issue before committing. Archives are permanent; new output is canonical-only.

8. **Show session summary** — Print a brief summary of what was accomplished and what the next session should pick up.

9. **Output copy/paste handoff block** — At the very end, print a clearly-delimited code block that Matt can paste into a fresh agent conversation as-is. Format:

   ```
   ━━━ HANDOFF FOR NEXT AGENT ━━━
   /continue {prompt-filename-without-.md}

   Context:
   - Active work track: {one-line description}
   - Last session: {session number} — {one-line outcome}
   - Read first: {path to canonical reference, e.g. wiki-pass2-pipeline.md, if relevant}
   - Open questions for Matt: {bullet list, or "none"}
   - DO NOT: {one-line list of things the next agent must avoid — e.g., "do not run /endsession without permission, do not auto-launch agent runs"}
   ━━━
   ```

   The block must be self-contained — a fresh Claude with no carry-over context should be able to start work from this paste alone. If multiple work tracks are in flight, output one block per track with a clear label. If no follow-up work track exists, say so explicitly rather than emit an empty block.
