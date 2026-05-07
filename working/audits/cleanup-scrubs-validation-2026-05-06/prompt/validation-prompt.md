# Validation prompt — paste into a fresh Claude Code session AFTER the cleanup orchestrator reports done

This is the independent-audit prompt for the work spec'd in `progress/continue-prompts/2026-05-06-handoff-cleanup-and-direction.md` (or its archived location). Read-only audit. Surfaces defects to Matt; does not fix them.

---

```
Validate the cleanup-and-scrubs work that the prior orchestrator just
completed. You are an independent auditor — do NOT trust the prior
agent's summary, verify everything against actual file state.

Source of truth (the spec the orchestrator was supposed to execute):

  /Users/mnoth/source/asoiaf-chat/progress/continue-prompts/2026-05-06-handoff-cleanup-and-direction.md

If that path doesn't exist, look in:

  /Users/mnoth/source/asoiaf-chat/progress/continue-prompts/archive/

(The orchestrator may have archived it as part of Phase 4 housekeeping.)

Read it end to end first, including the § 0.5 DECISION lines so you
know which conditional branches the orchestrator should have taken
(Q3, Q4, Q5, Q6, Q7, Q8, Q12).

You are READ-ONLY. Do NOT edit any files. Do NOT run sub-agents that
write. If you find a defect, surface it to me — don't fix it.

Audit checklist (report PASS / FAIL / N/A per item, with a one-line
note on any FAIL):

A. Scrub A — D&D framing
   1. <Q1-directory> exists.
   2. <Q1-directory>/chat-ui-architecture.md exists, starts with the
      "STALE SKETCH (archived 2026-05-06)" preamble line.
   3. /Users/mnoth/source/asoiaf-chat/working/chat-ui-architecture.md
      no longer exists at the original path.
   4. working/diagrams.md handled per Q4: if Q4=a, file still exists
      and Diagrams #1 and #12 are no longer chat-UI-framed; if Q4=b,
      file moved into <Q1-directory> with preamble; if Q4=c, decision
      logged.
   5. working/todos.md lines 106-108 edited per Q5+Q6: confirm by
      re-grepping for "PROMINENT — Chat UI scope" (should be 0 hits),
      and Q5/Q6 branches landed correctly.
   6. README.md was NOT edited by Scrub A (Scrub B handles its only
      edit). Verify by checking that README.md changes in `git diff`
      only touch the line 220 copyright clause.

B. Scrub B — Copyright rule removal (run this independent grep)
   grep -rEni "copyright|copyrighted" --include="*.md" \
     --exclude-dir=sources \
     --exclude-dir=working/worklog-archives \
     --exclude-dir=working/session-details \
     --exclude-dir=archive \
     --exclude-dir=<Q1-basename> \
     /Users/mnoth/source/asoiaf-chat

   Expected: zero hits except possibly the (now-archived) handoff
   file itself. Anything else is a FAIL — note the file and line.

   Also verify each of the 10 specific edits from § 3 by string
   anchor in the current file content:
   - CLAUDE.md: "## Critical Rule: Copyrighted Content" → 0 hits
   - README.md: ", and verifies `.gitignore` still protects" → 0 hits
   - STATUS.md: per Q3 (file deleted, or "(copyrighted content
     protection)" parenthetical removed)
   - .claude/commands/endsession.md: "**Verify .gitignore**" → 0 hits
   - worklog.md: ".gitignore protecting copyrighted content" → 0 hits
   - 2026-05-05-dialogue-meals continue prompt: "Never commit
     copyrighted source files" → 0 hits
   - working/runbooks/book-integration-done.md: "no copyrighted
     content is staged" → 0 hits
   - working/scratch-design-review-stage3b.md: "(gitignored
     copyrighted content)" → 0 hits
   - /Users/mnoth/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/feedback_never_commit_books.md
     → file does NOT exist
   - /Users/mnoth/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/MEMORY.md
     → no line containing "feedback_never_commit_books.md"
   - project_real_goal_graph_for_agents.md: "copyright-isolation
     move" → 0 hits

C. Independent D&D-framing re-grep
   grep -rEni "D&D|friend group|shared password|chat UI|chat-ui" \
     --include="*.md" \
     --exclude-dir=sources \
     --exclude-dir=working/worklog-archives \
     --exclude-dir=working/session-details \
     --exclude-dir=archive \
     --exclude-dir=<Q1-basename> \
     /Users/mnoth/source/asoiaf-chat

   Expected hits (all OK): the (now-archived) handoff file, false
   positive in sources/chapters/agot-jon-09.md if --exclude-dir for
   sources didn't catch it. Anything else is a FAIL.

D. Untouched-zones audit (use `git status` + `git diff --stat`)
   1. Zero modifications under sources/.
   2. Zero modifications under working/worklog-archives/.
   3. Zero modifications under working/session-details/ EXCEPT a
      newly created session-037.md (only if the orchestrator decided
      one was warranted — pure-execution sessions don't need one).
   4. Zero modifications under progress/continue-prompts/archive/
      EXCEPT the handoff file moving INTO it (that's an add, not an
      edit).
   5. .gitignore unchanged.
   6. .claude/settings.json + .claude/settings.local.json unchanged
      (per Q9).

E. Phase-2/3/4 deliverables (conditional)
   1. If Q8=a, working/model-fit-audit-2026-05-06.md exists and
      contains a markdown table with the columns specified in § 7
      Phase 2.
   2. Citation-validator output exists at the location specified by
      Q10 (or the standard dated location, e.g.,
      working/audits/citation-issues-2026-05-06.md).
   3. worklog.md has a session entry for this session AND the Q11
      Dunk & Egg decision is reflected in Current State.
   4. working/todos.md has two new items capturing the hook
      follow-ups from § 0 (PreToolUse hook on archives, PreToolUse
      hook on sources/).
   5. The handoff file is either still at
      progress/continue-prompts/2026-05-06-handoff-cleanup-and-direction.md
      OR moved into progress/continue-prompts/archive/. Either is OK.

F. Decision-line integrity
   Open the handoff file (in its current location). Confirm every
   "DECISION (required):" line in § 0.5 is filled in (not blank).
   The orchestrator was supposed to abort if any were blank — if any
   are still blank but the work was nonetheless executed, that's a
   process FAIL worth surfacing even if the work itself is fine.

Output: a single audit report with one line per item (A1, A2, ...
F), each marked PASS / FAIL / N/A. End with a one-paragraph summary:
overall status, total FAILs, and the most important FAIL (if any) to
fix first. If everything passes, say so plainly.
```
