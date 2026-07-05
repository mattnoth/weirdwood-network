# SESSION 192 — Short Fable cleanup + next-steps planning (post-query-layer)

> **This is Session 192.** Stamp your worklog entry `### Session 192` at endsession.
> (If another graph/meta session lands first, renumber — check `worklog.md`.)
> Matt-proposed shape (S191 endsession): "a short fable clean up and next steps planning."

**Recommended model: Fable, SOLO** — no subagent fan-out: the monthly spend limit was hit
in S191; assume it may still bind. Planning is the reasoning-heavy half; the cleanup half
is trivial. Keep it SHORT — this is a half-session, not a Track.

**Track:** meta. **State you inherit:** the query-layer Track is COMPLETE (S189 design →
S190 build → S191 finale) and the new chat build is DEPLOYED LIVE (researcher persona,
search/list/theme tools, routing table, full per-call outcome logging — verified). Read
`worklog.md` S191 + STATUS first; trust worklog over this prompt.

## Part 1 — cleanup (~30 min, do first)

1. **Class-5 dup-slugs — the biggest loose end.** Matt's `vigilant-chebyshev` worktree
   session never landed (no commit; `working/query-layer/hygiene-proposal-s190-reconciliation.md`
   still untracked). The live bundle serves the alphabetically-later copy for the 7
   colliding slugs (e.g. food `porridge` shadows the gaoler's 4 edges). ASK Matt: land it
   this session (the reconciliation file is the approval surface — his checkboxes +
   amendments 1-3 + the 5d coin-flip), fold it into this session, or explicitly re-park.
   Applying = graph mutation → needs his explicit go (checkbox read counts). Post-apply:
   `weirwood refresh` + bundle rebuild + redeploy, AND the ungated code hardening
   (load_nodes/build_search_index fail loudly on dup slugs; find_node_file deterministic
   order + collision warning).
2. **`cwd_is_tmp` environmental failure** — the only red in pytest (1445 pass otherwise).
   Fix the env assumption or mark `xfail(reason="environmental")` so the suite reads
   fully green. Matt queued this class of fix already (todos § Small Fixes).
3. **Tiny debris (batch, no discussion):** the fixture's doubled-article alias keys
   (`"the salt debt"`/`"the quiet mile"` unreachable — drop the stored article, adjust the
   test comment); decide the reconciliation file's disposition (commit as record vs leave
   for Matt's session).

## Part 2 — next-steps planning (the real value)

Re-rank the parked queue and mint AT MOST ONE live continue prompt for the winner
(memory: one live prompt rule). The candidates, with their standing state:

- **Side-window receipts for search/list/theme** — Matt-deferred behind the deploy, now
  next in his own sequencing ("we can work on the display of the side window after").
  Design decision needed: likely a "sources consulted" card rendering quote hits with
  citations (`app.js ingestReceipt` has no case for the 3 new tools; full results already
  reach the browser via the receipt SSE event).
- **8d SERVED_AT trigger check** — Q21-class evidence now accumulates in live logs
  (`web/scripts/read-logs.ts`); check whether dish↔event connection still fails post
  search/theme. Trigger fires → write the vocab proposal (still triple-gated).
- **Granular dips** — `working/granular-dip-plan.md` ranked list exists (S168; opener =
  D2 Hand's Tourney); PARKED for Matt's review since the chat-UI pivot.
- **D&E Pass-1 un-park** — `worklog-dunk-egg.md` + `progress/continue-prompts/2026-06-29-dunk-egg-pass1-smoke.md`
  (smoke un-run; Matt parked it 2026-06-23 "revisit when fresh").
- **Alpha-tester notes round** — the deployed build is the biggest chat change since
  S183; Matt populating logs = free eval data.
- **Theme-page-cap gap** (3/5 Q11 dishes beyond the 25-row cap) — small, someday.
- **SIFT** — stays parked (memory `project_sift_deferred`) unless Matt says otherwise.

Present the ranking with a recommendation; Matt picks. Don't start the winner's work in
this session (session-purpose discipline — memory `feedback_session_purpose_discipline`).

## Hard gates

No graph/nodes|edges|index mutation without Matt's explicit go (class-5 apply INCLUDED —
his checkbox read is the go surface). No prod deploy without his go (post-class-5 rebuild
would need one). `sources/` read-only; never fetch the wiki; don't touch `scr`; don't
run /endsession without permission. Vocabulary: **Pass** / **Track** / lowercase
**step** / **Tier** = confidence 1–5 only.
