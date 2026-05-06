---
title: Session 36 — Hygiene pass + soft-convention hardening
date: 2026-05-06
model: opus 4.7 (1M)
focus: meta — stale-content audit + project-rule reform
---

# Session 36 — Hygiene + Soft-Convention Hardening

**No extractions, no agent runs, no graph changes this session.** Pure project hygiene + meta-rule reform. Triggered by Matt asking two things on a clean morning: "are there stale continue prompts?" and "did ASOS Pass 1 actually finish?"

## What was found vs. what got reformed

The session started as cleanup ("audit stale things") and morphed into a structural conversation about *why* the project keeps accumulating stale things. The structural insight: most of the rules that should prevent drift live as soft prose conventions in `CLAUDE.md` or `todos.md` preambles, with no enforcement mechanism — and they reliably lose to actual work every session.

### ASOS Pass 1 verification

82 source chapters / 82 extraction files. 1:1 match by name (no `diff` output). Smallest extraction is 248 lines (`asos-davos-03`). No empty or stub files. Worklog Session 35 already confirmed spot-checks across early/mid/late waves were clean v3. Conclusion: ASOS is genuinely complete; Pass 1 is 344/344 across all 5 books.

### Stale continue prompts

5 prompts in `progress/continue-prompts/`. Audit:

- **3 stale** (Pass 1 work tracks, all complete) → archived
- **2 still valid** (Stage 4 prose-edge-classifier, dialogue/meals/mention-index design)

`SESSION-32-HANDOFF.md` (the ACOK launch orchestration handoff from Session 31→32) was also surfaced as fully stale. ACOK is 70/70 done; the file's "Next Step" command is for work that completed weeks ago. Moved to `working/worklog-archives/session-32-handoff.md`.

### Scratch-notes drift

`progress/scratch-notes.md` was originally Matt's one-liner file ("a scratch.txt I made for stuff I wanted to come back to"). At time-of-audit it was 147 lines of session-stamped writeups (Session 22, Session 19, Session 13, etc.) — agents had used it as a session log alongside `worklog.md` and `working/session-details/`. Three of its entries were *referenced* by name from `working/todos.md` (`Foreshadowing Pass Prep`, `Collaborator Onboarding`, `Scheduled Launches Direction Bank`).

Resolution per Matt's call:
- Folded the three referenced entries' essential content directly into the todos.md lines that referenced them (the cross-ref now disappears — todos is self-contained)
- Deleted `progress/scratch-notes.md` entirely
- Cleaned all live references to it in `CLAUDE.md`, `README.md`, `STATUS.md`, `.claude/agents/status-reporter.md`, and `.claude/commands/endsession.md`
- Historical references in `working/session-details/session-NNN.md` and archived continue prompts left untouched (those are frozen historical record)

### Soft convention audit

Matt's question after the scratch-notes cleanup: "are there other soft conventions like this?" Surveyed; found seven, in roughly descending order of drift evidence:

| Convention | Drift evidence |
|---|---|
| "Move completed todos to Done section periodically" (todos.md preamble) | Never happened. todos.md was 264 lines. |
| "Worklog Session Log archive at ~150 lines" (CLAUDE.md + /endsession) | Worklog Session Log was 200+ lines; last archive was Sessions 25-26 (Sessions 27-35 still in main). |
| "Delete continue prompts that were completed this session" (/endsession step 3) | I just archived 3 that had survived multiple sessions. |
| "Two-tier session documentation: every session gets a `session-details/session-NNN.md`" (CLAUDE.md:7) | Sessions 32, 34, 35 don't have detail files; many sessions skip it. |
| "Audit existing agent prompts for model-fit drift" (todos.md item) | Never done — itself a stale todo. |
| "When modifying an agent prompt's schema, update reference/architecture.md" (CLAUDE.md rule 6) | No mechanism. |
| "Confidence tiers — tag everything" (CLAUDE.md Key Conventions) | Behavioral; partially enforced via validators. |

**The pattern:** all of these are "do this when X happens" rules whose execution depends on the agent (a) loading the rule, (b) recognizing the trigger, (c) choosing to act on it instead of moving on to actual work. Conditional steps in `/endsession` do better than soft prose in CLAUDE.md (because /endsession is a checklist), but conditional ones still slip when the agent has to evaluate the trigger and decide.

### Hooks vs. rules — architectural note

Matt's question: "is it double context usage to write a hook and a rule?" Answer surfaced during discussion:

- A **rule** (CLAUDE.md / slash command) is text the agent reads. CLAUDE.md is loaded every session; slash command files load only when invoked. Both cost context bytes once per load.
- A **hook** (in `settings.json`) is harness-executed. It only adds context cost if its output is shown to the agent (and only when it fires).
- Both together is "double cost" only when they say the same thing. Two cases where both genuinely help: (1) hook does enforcement, rule explains why so the agent doesn't fight the hook; (2) hook fires outside slash-command flow, rule covers inside.
- For the conventions discussed this session (worklog archive, todos pruning, scratch triage), rules-in-/endsession alone are sufficient — Matt reliably runs /endsession.

The places where hooks would *earn* context cost in this project (not built this session, just noted): copyrighted-content commit blocking, `--no-verify` blocking, destructive-git-op blocking. Those are enforcement-critical; soft rules are insufficient. Future infrastructure todo.

## Decisions locked

1. **Worklog Session Log holds at most 5 entries** (CLAUDE.md orchestration rule #8 + /endsession step 6). Strict — no "~150 lines" ambiguity. Each archive file holds exactly 5 entries; new `archiveNNN.md` starts when the current is full. Applied this session: Sessions 27, 28, 29 topped off archive006 (which had Sessions 25-26) to 5; Sessions 30 (×2 entries — same number, different content) and 31 started archive007 with 3 entries. Worklog now keeps Sessions 32-36.

2. **Session-details files are as-needed, not every-session** (CLAUDE.md orchestration rule #7 rewritten + /endsession step 1 rewritten). Write only when the session contains design discussion, architecture decisions, novel problem-solving, an incident worth a postmortem, or substantial reasoning that doesn't fit in a worklog entry. Pure-execution sessions skip it. Existing inconsistent coverage is a project-story todo (auxiliary, not blocking).

3. **Top-level `scratch` file is Matt's private space.** Gitignored at the repo root (`/scratch`, `/scratch.md`, `/scratch.txt`). New CLAUDE.md section before Orchestration Rules tells agents not to read, surface, or act on it during normal sessions. The single exception is `/endsession` step 4(a) — the designated triage moment that reads scratch, surfaces entries to Matt, and prompts where each should land.

4. **`/endsession` step 4 expanded with scratch triage subroutine.** When invoked, checks for `scratch` / `scratch.md` / `scratch.txt` at repo root. If non-empty, surfaces entries one at a time and prompts: actionable → `working/todos.md`, decision → `worklog.md` Active Decisions, resumable work track → `progress/continue-prompts/`, or discard.

5. **`progress/scratch-notes.md` retired.** Its purpose is replaced by the top-level `scratch` file (private, gitignored, triaged at /endsession). The old file's content was either folded into `todos.md` (for the three long-form entries that were referenced) or dropped (for the rest, which were either redundant or stale).

6. **`working/todos.md` reorganization deferred** (proposed structure exists in conversation but not executed). The proposed top-level structure: Standing Rules → Ready to do next → In-flight (Stage 4 prep) → Stage 4 to be built → Schema/vocabulary pending → Future passes → Reference files → Infrastructure → Audit follow-ups → Collaboration → Chat UI/Downstream → Project Story/Auxiliary. Plus a parallel `working/todos-archive.md`. Matt paused before approving the actual reorg (`do nothing, what's the git status?`) to focus on commit + endsession. The reorg is a future session task.

## What got committed

Single commit `240fe565`: "Hygiene pass: archive stale prompts, retire scratch-notes, harden conventions" — 15 files, +407/−214 lines. Pushed to `origin/main`.

The commit also picked up the dangling primary-handoff continue prompt (`2026-05-05-dialogue-meals-mention-index-design.md`) which had been untracked since Session 34/35.

## What didn't happen this session (intentional)

- **No todos.md reorg.** Proposed structure exists; Matt paused for the commit. Picks up next session.
- **No model-fit audit.** Elevated to "READY TO DO" in todos.md but not executed.
- **No `working/todos-archive.md` creation.** Will happen during the reorg.
- **No backfill of session-details/.** Filed as auxiliary project-story todo.

## Loose ends and follow-on observations

- The two Session 30 entries in worklog (different titles, same number) were a numbering bug from the actual sessions; preserved as-is in archive007 rather than renumbering history.
- `STATUS.md` is dated 2026-04-23 — over 2 weeks stale; minor scratch-notes/handoffs.md ref updated, but the file itself duplicates a lot of `CLAUDE.md` + worklog Current State and probably wants a refresh-or-retire decision in a future session.
- The "ASOS Pass 1 by Okey on shared Max" data point is interesting evidence for the collaborator-handoff todo — schema held up through a parallel run by a less-deep ASOIAF reader. De-risks Pass 1 schema lock-in.
