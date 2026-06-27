Run the end-of-session checklist for the Weirwood Network project. Do each step in order:

0. **Harvest queue check (do this FIRST, before the worklog entry) — AUTOMATIC, no Matt prompt needed.** Count open rows: `grep -c '^| open ' working/harvest-queue.md`. **If ≥ ~30 open rows, you MUST either (a) DRAIN it this session** (route rows → disjoint node-dirs → parallel Sonnet attachers → fresh-verify a sample → flip to `done`; the S152/S139 machine) **OR (b) stage a dedicated harvest-drain as the live continue prompt for the NEXT session.** Never just let it grow — Matt should not have to notice the balloon himself (this rule exists because S153–S156 silently let it reach 120). Enrichment dips ALWAYS land ~25–40 new rows, so this trips roughly every dip. Record the open-row count + what you did in the worklog entry. (Drain machinery + history: `working/arc-enrichment-backlog.md` harvest section; memory `feedback_harvest_queue`.)

1. **Write session detail file (only if warranted)** — Session-details files are **as-needed**, not every session. Write `history/session-details/session-NNN.md` ONLY IF the session contains: design discussion, architecture decisions, novel problem-solving, an incident worth a postmortem, or substantial reasoning that doesn't fit in a worklog entry. Pure-execution sessions (extraction waves, batch operations, hygiene/cleanup) skip this step — the worklog entry is sufficient. When you do write one, it's the **human-facing** full narrative: what was explored, what was tried, what was rejected, coverage numbers, reasoning. Not for agents.

2. **Update your track's worklog** — **Graph/meta sessions** → `worklog.md` (global `### Session N`). **D&E Pass-1 sessions** → `worklog-dunk-egg.md` (`### Session DE-N`); a D&E session does NOT touch the `worklog.md` Session Log (only update `worklog.md` if you changed **shared** state — e.g. a project-wide Active Decision, which always lives there). Add a **concise** session log entry (~20-30 lines max) to the Session Log section. This is **agent-facing** — future sessions load this file, so keep it tight. Format:

   ```
   ### Session N — Short Title (YYYY-MM-DD)
   **Detail:** `history/session-details/session-NNN.md`
   **Changes made:** (bullet list of files changed and what changed — facts, not narrative)
   **Decisions:** (one paragraph of key decisions, compressed)
   **What's next:** (bullet list of next actions, with continue prompt paths if they exist)
   ```

   Also update the Current State checkboxes and Extraction Pipeline checklist if any items were completed or status changed.

3. **Manage continue prompts** — *Keep the LIVE directory small (only genuinely active tracks). Done/stale prompts are ARCHIVED, never deleted — "keep everything" applies, just organized.*
   - **Create** new ones ONLY for genuinely mid-flight tracks. Write to `progress/continue-prompts/{date}-{short-description}.md` with enough context for a fresh agent to pick up the work. **Lead the prompt's H1 title with the next session number** — `# SESSION <N+1> — <title>` (N = the session you just wrote this endsession), and add a `> **This is Session <N+1>.** Stamp your worklog entry `### Session <N+1>` at endsession.` line right under it. (This matches the `# SESSION <N+1>` stamp inside the handoff block in step 9. It's primarily so the fired session knows its own number for the worklog stamp — chat auto-titling from prompt content is unreliable, treat the title as a bonus, not the goal.) Reference the path from the worklog entry's "What's next" section. **Also link it from todos.md** — add a `→ continue:` line under the relevant todo item so `/continue` can find it by priority. **One prompt per track** — never leave two prompts covering the same work; supersede/merge instead (Matt: "I don't want to keep two continue prompts saved for later").
   - **Archive** (do NOT delete) any continue prompt that was completed OR superseded this session: `git mv progress/continue-prompts/<file> progress/continue-prompts/archive/`. Remove its `→ continue:` line from todos (and check the todo item if fully done). The live `progress/continue-prompts/` dir holds only LIVE + HALTED-gated tracks; everything done/stale lives in `archive/`, organized.
   - **Contradiction check:** if any surviving LIVE prompt's project-state claims contradict `worklog.md` (CLAUDE.md rule #9), fix the prompt or archive it — never leave a stale/contradictory prompt in the live set (this session's arc-wave1 vs worklog ordering was exactly this failure).
   - **Refresh the manifest:** update `progress/continue-prompts/README.md` so its status column matches reality — LIVE/HALTED rows for the live dir, archived rows moved to the Archive section. The manifest is the single index — it must not lag.

4. **Update progress files** — If extraction waves ran, update the relevant `progress/pass1-{book}.md` file. (Do NOT read or triage the top-level scratch file — that's Matt's private notes; per CLAUDE.md, only touch it if Matt explicitly asks in the current turn.)

5. **Update working/todos.md** — If new TODOs surfaced during the session, add them to the appropriate section.

6. **Archive worklog if > 5 entries** — Count session entries in worklog.md Session Log. If more than 5, move the oldest entries to `history/worklog-archives/archiveNNN.md` until exactly 5 remain. Each archive file holds exactly 5 entries; if the current `archiveNNN.md` is already full, start a new one (`archive(NNN+1).md`). The worklog keeps Current State, Active Decisions, Ideas & Backlog, Principles, and the 5 most recent session entries. **This step applies to `worklog.md` only.** The D&E log (`worklog-dunk-egg.md`) does NOT archive to `history/worklog-archives/` — if it ever exceeds 5 entries, spill the oldest to an `## Archived sessions` section at the foot of that same file.

7. **Verify extraction archive rules** — If extractions ran this session:
   - **Check:** Do old archives (v1, v2, etc. in `extractions/archives/`) still exist? They should NOT be deleted.
   - **Check:** Did new extractions land in canonical `extractions/mechanical/{book}/`? They should NOT be in archive folders.
   - **If violated:** Flag the issue before committing. Archives are permanent; new output is canonical-only.

8. **Show session summary** — Print a brief summary of what was accomplished and what the next session should pick up.

9. **Write handoff file(s) AND print the literal copy-paste in chat.** The long-form context (full task description, success criteria, DO-NOTs, slug lists) goes to a file at `progress/continue-prompts/<date>-<short-slug>.md` — that's where the next session's agent reads from. BUT the literal copy-paste commands Matt needs to fire the next session MUST ALSO appear inline in chat at session close, so he doesn't have to open the file to know what command to run.

   **Stamp the next session number first (always) — INSIDE the copy-pastable block.** The FIRST line inside the handoff code block, directly above the opening `━━━ HANDOFF` bar, is `# SESSION <N+1>`, where N is the session number you just wrote to the worklog this session (e.g. if this session is S127, the first line is `# SESSION 128`). It lives inside the same fenced block as the handoff so it copy-pastes together — primarily so the fired session knows its own number for the `### Session <N+1>` worklog stamp; it also gives the next chat's title a shot at carrying the number (auto-titling is unreliable — treat the title as a bonus, not the goal). One stamp covers all blocks if multiple tracks are queued (put it once, at the top of the first block).

   **What to print inline (always):** the Shape A or Shape B block below — it contains the literal `/continue <slug>` / `/watcher <substring>` / `/worker <substring> <wave-id>` command(s) plus model recommendation. Short — typically 4-12 lines per block. Multi-line handoff *prose* (long task descriptions, slug lists, success criteria) stays in the file, NOT in chat — those belong to the future agent, not to Matt-at-session-close.

   **What goes only in the file:** task description prose, success criteria, slug lists, DO-NOTs, sub-step instructions, slug-mapping tables, anything > 12 lines. The file is what `/continue` reads when fired.

   Also print one summary line per file written: `Wrote handoff: progress/continue-prompts/<date>-<slug>.md (Shape A | Shape B | session-task)` — gives Matt the path for reference, separate from the copy-paste block.

   **One file per independent work track.** Parallel-safe tracks each get their own file so Matt can pick them up independently. The dependency between them (parallel-safe vs sequential) is noted in each file's prose.

   File shape per track — pick A or B based on what's queued:

   ### Shape A — Mission (watcher + workers)
   When the next work is a mission (multiple parallel workers + a watcher reading their state), output ONE handoff block per role. Always include model recommendation.

   ```
   # SESSION <N+1>
   ━━━ HANDOFF — WATCHER (window 1) ━━━
   Model: Opus 4.7
   In a fresh Claude Code session, type:
       /watcher <mission-substring>
   …then paste the kickoff it emits as your first message.

   Mission file: working/agent-fleet-specs/missions/<date>-<slug>.md
   Open questions for Matt: {bullet list or "none"}
   DO NOT: dispatch workers (you orchestrate them in separate sessions); modify worker output; auto-run /endsession.
   ━━━

   ━━━ HANDOFF — WORKERS (windows 2-N) ━━━
   Model: Sonnet 4.6 (Haiku 4.5 if mission explicitly OKs simpler tasks)
   For each worker slug in the mission's wave, open a fresh Claude Code session and type:
       /worker <mission-substring> <worker-slug>
   …then paste the kickoff it emits as your first message. One worker per session.

   Worker slugs for wave 1: {comma-separated list from mission file}
   Worker slugs for wave 2 (after wave 1 settles): {comma-separated list}
   DO NOT: refetch wiki; write to graph/nodes/; touch other workers' scratch dirs; auto-run /endsession.
   ━━━
   ```

   ### Shape B — Single worker / session-task
   When the next work is a single deterministic task (no watcher needed, no parallel workers), output one block. Always include model recommendation.

   ```
   # SESSION <N+1>
   ━━━ HANDOFF — SINGLE-SESSION TASK ━━━
   Model: {Sonnet 4.6 | Haiku 4.5 | Opus 4.7} — {one-line reason}
   In a fresh Claude Code session, paste:
   ---
   {self-contained task description: goal, steps, scripts to run, success criteria, what to write to worklog/todos at the end}
   ---

   Read first: {path to canonical reference, if relevant}
   Open questions for Matt: {bullet list or "none"}
   DO NOT: {one-line list of guardrails — e.g., "do not run /endsession without permission"}
   ━━━
   ```

   ### Multiple tracks queued
   If multiple independent tracks are queued for the next session(s), output one block per track with a clear label. Mark which tracks can run in parallel (different windows) vs which must be sequential.

   ### No follow-up work
   If nothing is queued, say so explicitly rather than emit an empty block.

   ### Hard rules
   - The block(s) must be self-contained — a fresh Claude with no carry-over context should be able to start work from this paste alone.
   - Always include a model recommendation — never leave it implicit.
   - Prefer slash commands (`/watcher`, `/worker`, `/continue`) over raw kickoff prose where one exists.

10. **Commit and push** — Stage THIS session's work and commit to `main` (the project's established convention — every prior endsession committed directly to main), then `git push`.
    - Stage explicitly by path — do NOT blanket `git add -A`. Include the files you created/modified this session (graph edges + backups, scripts, tests, docs, worklog **or `worklog-dunk-egg.md`** for your track, todos, continue prompts, session-details, worklog-archives). EXCLUDE pre-existing/stray untracked files you did not create, and NEVER add the gitignored `scratch` / `scr` files. **Parallel-track safety:** if another track is mid-flight in the same working tree (uncommitted files you didn't create — e.g. another session's `graph/` writes), stage ONLY your own files by explicit path; never `git add -A`.
    - Commit message: a one-line `SNN: <summary>` subject + a short bullet body of what changed. End with the required trailer:
      `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`
    - `git push`. Report the pushed commit hash + branch.
    - If anything is uncommittable or you're unsure whether a stray file should be included, stage what's clearly yours, commit that, and flag the leftover rather than guessing.
    - (Memory entries under `~/.claude/.../memory/` live outside the repo and are not committed — that's expected.)
