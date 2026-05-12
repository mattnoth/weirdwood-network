---
session_number: 51
date: 2026-05-12
title: Watcher-Day Orchestration — Spot-Check, Orphan Audit, Session-Results Convention
model: Opus 4.7 (1M context)
role: watcher + ad-hoc orchestrator
---

# Session 51 — Watcher-Day Orchestration

## Setup

This session ran as a watcher in its own window while Matt opened parallel windows for three task sessions: alias-backfill round 2 (Session 49, Sonnet), case-collision close (Sessions 47 + 49b — Track A landed earlier in the day; Track B started during this watcher's life), and the orphan-batch cleanup (Session 50, Sonnet, the work this watcher itself wrote the continue prompt for).

The watcher prompt is at `working/runbooks/general-watcher.md`. Per its hard rules: read-only by default, no dispatch, no `/endsession` unless Matt fires it. Most of those held — but Matt twice explicitly waived read-only ("fix the 3 orphan edges", "commit first") and the watcher made edits and ran scripts within those scopes.

## Observations the watcher caught

1. **Stale slugs in the alias-backfill prompt.** Before the alias-backfill session began executing step 1, the watcher noticed its three target slugs (`vale-of-arryn`, `aemon-targaryen-maester`, `aemon-targaryen-dragonknight`) didn't all exist — the two Aemons are under the `son-of-*` naming convention (`aemon-targaryen-son-of-maekar-i.node.md`, `aemon-targaryen-son-of-viserys-ii.node.md`). Flagged to Matt before the running session hit the skip-and-file-todo path. The session itself caught this independently and routed to the correct slugs, beating the prompt's projected 70.6%→72-74% resolution rate (actual: 72.9%, +2.3 pp on ~849 newly-resolved mentions).

2. **Track B's protocol deviation.** Case-collision close's continue prompt mandated multi-window + watcher mode for Track B (drift potential HIGH; workers need TYPE_DIR_MAP awareness). Track B instead executed inline in the orchestrator session after the filter step collapsed canonical scope from ~15-20 to 10. Session 49b's worklog entry documents the rationale (filter step solved the drift surface). Defensible but unverified — hence the spot-check below.

3. **Track B node defect rate: 20%.** Spot-check of the 10 new Track B nodes surfaced:
   - 2× `SERVES: ramsay-bolton` (alias-not-canonical; canonical slug is `ramsay-snow`)
   - 1× `MEMBER_OF: bastards-boys` (target node didn't exist)
   - 1× empty `## Edges` block on `ice-dragon` (defensible — legendary creature, few concrete connections)

   The two ramsay-bolton edges were fixed in-place by the watcher (Matt-authorized). The bastards-boys orphan was deferred to a planned orphan-batch cleanup.

## Orphan-edges audit

Ran `scripts/orphan-edges-audit.py 2026-05-12`. Findings:
- Nodes scanned: 7,712 (+150 vs 2026-05-02 prior)
- Cat 1 orphan edges: 1,896 (−67 vs prior — graph got bigger AND cleaner)
- 822 unique missing target slugs

Top non-date orphans were dominated by:
- `blacks` (138 edges) + `greens` (127) — Dance of the Dragons factions, never created
- `age-of-heroes` (43), `crossroads-inn` (39 — alias-mismatch), `dragons` (32 — alias-mismatch), `crypt-of-winterfell` (29)
- `bastards-boys` rank #33 — the spot-check orphan was real but small

Of the 1,896 Cat 1 edges, only ~30 were date-bleed (`*-ac` slugs) per the script's filter. The bulk are real missing-entity orphans.

## Sessions 50 — orphan-batch (handoff drafted by watcher)

Watcher wrote `progress/continue-prompts/2026-05-12-orphan-batch-top-nodes.md` for a fresh Sonnet 4.6 session. Matt initially balked at the file's length ("fucking huge") — I produced a tight paste-ready version inline as well. He launched Session 50 with the paste version.

Session 50 result:
- 7 alias-fixes (crossroads-inn, dragons, joffrey-i-baratheon, tommen-i-baratheon, vale, the-wall, giant) + 8 new nodes (blacks, greens, age-of-heroes, andal-invasion, crypt-of-winterfell, two-betrayers, winter-wolves, bastards-boys)
- Beat my top-10 table — added `the-wall`, `giant`, `andal-invasion`, `winter-wolves` from the residual TSV
- Cat 1 orphan edges 1,896 → 1,673 (−223); clean-resolved 18,831 → 19,055 (+224)
- Diagnosed the prompt's "400-500" projection as in_count-based vs edge_count-based — ~93% hit rate on actual edge_count

## Session-results convention (novel pattern)

Matt's observation that motivated this: during today's 4-window orchestration (watcher + 3 task sessions), the watcher had to ask Matt to copy-paste each task session's final summary 4 separate times. Each copy-paste was friction. The fix:

**Convention:** Every session writes a result file to `working/session-results/<date>-<session-name>.md` as its last step. Watchers check that directory first.

Why per-session files rather than a shared log or worklog:
- **Worklog is too late.** It only gets written at session end (or `/endsession`), so watchers see nothing mid-flight.
- **Worklog is also too historical.** Active result interleaves with the 5-session rolling window of historical entries.
- **Per-file is append-by-different-actors — no merge-conflict surface.** Today's two-window parallel run dodged worklog conflicts only by lucky timing.

Artifacts landed:
- `working/session-results/README.md` (convention doc, format spec, retention)
- `working/runbooks/general-watcher.md` updated (3 edits — first-steps list, signal table, useful-commands block)
- `working/todos.md` — two new entries: "Bake into every future continue prompt" (NEW) + "Future richer session-state.jsonl hookup" (FUTURE)
- `working/session-results/2026-05-12-watcher-day-orchestration.md` (this session's demo result file)

The convention is intentionally minimal — file convention + standard location + watcher prompt update. No daemons, no IPC, no hooks (yet). The FUTURE todo captures the upgrade path to `session-state.jsonl` + PostToolUse hooks if/when the file approach proves insufficient.

## Hard rules respected

- Wiki not refetched
- `sources/` not written
- Historical archive entries not edited (worklog refs to retired continue prompts remain frozen)
- Memory rule: scratch (other than the named carve-out) not read
- `/endsession` not auto-run (this entry exists only because Matt fired the command)

## Commits made

- `bc19163e4` — Sessions 43-49b accumulated (2,587 files)
- `c54719d40` — Session 50 orphan-batch + session-results convention (372 files)
- `4349a62e6` — Session 50 worklog rotation (2 files)

`scratch-do-not-delete.txt` remained untracked across all three commits (root-level scratch sentinel; not covered by `.gitignore` `/scratch[.md|.txt]` patterns but treated as scratch per memory rule).

## What this session did NOT do

- Track A's 60-node spot-check (filed as MED todo; partially absorbed by Session 50's audit-rerun improvement, but residual remains)
- Stage 4 prose-edge-classifier launch (sequential, queued — handoff block in this session's `/endsession` output)
- Backfill of the session-results convention into existing in-flight prompts (filed as todo; apply going forward only)
- Updating Stage 4 continue prompt with session-results write step (filed as todo; will be done before Stage 4 fires)
