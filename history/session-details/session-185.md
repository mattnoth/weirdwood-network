# Session 185 — Chronology sort-key wiring + a three-agent working tree

**Date:** 2026-07-03
**Model:** Sonnet 4.6
**Track:** meta (chat-UI)
**API spend:** none — deterministic TS/Python only; no live chat, no LLM passes, no subagents.

## Goal

Finish the S184 render fix: the live chat UI rendered causal chains out of
chronological order (a Bran chain showed the ADWD cave before AGOT Bran 2; "what led
to Robert's Rebellion" surfaced a forward MOTIVATES edge ~15y later). S184 proved
this was a **render/traversal** bug, not bad data, and shipped `sort_keys:` on all
744 event nodes. This session wires those keys into the live path (Step A) and adds
a same-year inversion scan (Step D). Steps B (logging) and C (date backfill) were
carved off — see "Three-agent tree" below.

## The comparability problem (the one real design decision)

The continue prompt said "sort `walkChain` by the node's `composite` (fallback
`reading_order`)". Implemented literally as a string sort, this is **wrong**, and the
exact reported Bran chain is the counterexample:

- `composite` = `"{ac_year:04d}.{book}.{chapter:03d}"` — e.g. `"0298.1.018"` (dated events)
- `reading_order` = `"{book}.{chapter:03d}"` — e.g. `"1.015"` (undated events)

These two formats are **not lexically comparable**. In the `jaime-pushes-bran`
downstream chain, `bran-s-direwolf-kills` (chapter 15) carries only `reading_order`
`"1.015"`, while `bran-s-coma` (chapter 18) carries `composite` `"0298.1.018"`. A
naive `a < b` string sort compares `"0298.1.018"` against `"1.015"` → `'0' < '1'` →
the *later* coma event sorts *first*. The bug would survive the "fix".

**Solution:** normalize both into the composite space before comparing. An undated
event's `reading_order` gets a synthesized 4-digit year from a small book→AC-year map
(`{1:0298, 2:0299, 3:0299, 4:0300, 5:0300}`), so `"1.015"` → `"0298.1.015"`, which
compares correctly against real composites and interleaves undated events at roughly
the right chronological point (an undated ADWD event still sorts after a dated AGOT
one; a dated historical flashback still sorts by its true low year). Nodes with
neither key sort last, stably. Implemented as `chronoKey()` + `sortChainLinks()` in
`graph.ts`; the sorter keys on the link's source composite, then target, so ties on
the cause break by the effect. The synthesis map only affects *undated* events'
cross-book placement — within a book the year is constant so it never changes order.

A regression test pins exactly this mixed-key case (direwolf ch.15 before coma ch.18)
plus a synthetic AGOT→ADWD Bran chain whose edges are listed ADWD-first so a
hop-depth/insertion order would reproduce the reported bug.

## The render split

The committed `app.js` did `addChainLinks([...upstream.reverse(), ...downstream])` —
one merged spine. The prompt (correctly) flagged that merge as what let a downstream
consequence surface among the causes. Rewrote the render to keep `upstream` and
`downstream` as two separately-labelled sections ("What led to this" / "What
followed"), each independently story-time-ordered, with the queried event as the
pivot each runs to/from. Hover-highlight now spans both flows; the dead
`addChainLinks` helper was removed. `deno.json`'s fmt scope is `src/` +
`netlify/edge-functions/` only, so `public/` browser assets (app.js/app.css) are not
under fmt governance — the lib TS files were formatted to stay clean.

## Step D — same-year intra-chapter inversion scan

Deterministic, read-only. Closes the S184 caveat (0 inversions at *year* granularity;
composite is now chapter-resolution). Of 53 same-year causal edges with both
composites, **0 are genuine cause-after-effect inversions**. 5 flag falsely — every
one has a target composite of `{year}.0.000`, i.e. the target event is dated but has
no chapter anchor (book_order/chapter absent), a composite artifact, not a direction
bug. The causal layer is sound at chapter resolution. Report:
`working/s185-step-d-inversion-scan.md`. The 5 chapter-anchor gaps are a Step C
follow-on (backfill an `evidence_chapters` anchor), not edge flips.

## Three-agent working tree (the process story)

Mid-session, files I never touched — `chat.ts`, `agent.ts`, `agent_test.ts`,
`web/scripts/read-logs.ts`, `web/scripts/sweep-logs.ts` — appeared fully implementing
**Step B (usage logging)**, labelled "S186" in their comments. One of my edits to
`agent.ts` failed with "modified since read" rather than clobbering. A **parallel
S186 session** was implementing logging concurrently; a third **styling agent** was
live in `app.css`/`app.js`/`index.html` (confirmed by editor-side "modified by a
linter/user" reminders). So: S185 = chronology (me), S186 = logging, styling = a third
agent — three agents in one working tree.

Verified (read-only) that S186's logging is spec-correct: unique `log/DATE/uuid` key,
never read-modify-write (the daily-spend counter's racy pattern explicitly avoided),
console mirror written first, its own try/catch, placed after `addDailySpend`, stores
structured receipts + prose only (no raw content blocks). Did not touch it.

**Why the commit was deferred.** My `graph.ts` now returns `upstream` in ascending
story-time. The *committed* `app.js` still does `reverse()+concat`. Committing
`graph.ts` without my (uncommitted) `app.js` render change would produce an
inconsistent committed state — a deploy from it would render upstream
reverse-chronological. And `app.js`/`app.css`/`index.html` are contested with the
styling agent; `chat.ts`/`agent.ts` are S186's. So the whole S185 commit waits for a
**coordinated final commit** once all three agents settle (Matt's explicit offer:
"write a prompt to the next agent I run end session on"). Nothing was staged.

## State at close

- Step A: code-complete, `deno check` (lib + edge fn) clean, 39/39 tests green,
  bundle rebuilt with composites (261 composite / 307 reading_order). **Uncommitted.**
- Step B: done by S186 (verified, untouched). **Uncommitted.**
- Step C: not run (optional, gated on Matt's OK for any Haiku pass).
- Step D: done, report written.
- The one unverified piece: the two-section chronological render needs a live turn /
  draft deploy to eyeball (a running `weirwood-live` server on :8766 belongs to S186 —
  not hijacked). Folds into the coordinated deploy.
