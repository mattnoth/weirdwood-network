# SESSION 185 — Wire the composite chronology sort key into the live render + deterministic date backfill

> **This is Session 185.** Stamp your worklog entry `### Session 185` at endsession.
> **Recommended model:** Sonnet 4.6 (deterministic TS wiring + a Python bundle change; the backfill sub-step uses Haiku, NOT Fable).

## Background (what S184 did)

The live chat UI (https://weirwood-network.netlify.app) renders causal chains **out of chronological order** (e.g. "what led to Robert's Rebellion" shows a forward `MOTIVATES` edge to Robert's Dany-assassination order ~15y later; a Bran chain shows the ADWD cave before AGOT Bran 2). S184 proved this is a **traversal/render** bug, not bad data: a temporal-inversion scan over all 170 causal edges found **0** cause-after-effect inversions. The deployed walker `walkChain()` in `web/src/lib/graph.ts` sorts by graph hop-**depth**, never chronology, and merges upstream+downstream.

S184 shipped (committed) `scripts/build-event-sort-keys.py`, which stamped a derived `sort_keys:` block onto all 744 event nodes:
```yaml
sort_keys:
  ac_year: 300
  book_order: 5
  chapter_number: 35
  chapter_label: "ADWD Bran III"
  composite: "0300.5.035"    # story-time key: {ac_year:04d}.{book_order}.{chapter:03d}
  reading_order: "5.035"
  basis: "year+chapter"       # year+chapter | year-only | chapter-only | none
```
`composite` is the story-time sort key (null when the event has no `ac_year` — 282/744 are undated). `reading_order` is the fallback.

## This session's goal — finish the render fix, deterministically

### Step 1 — carry `sort_keys` into the web bundle
The deployed `web/data/nodes.json` / `edges.json` currently strip temporal fields. Find the bundle builder (grep for the script that writes `web/data/` — likely `scripts/build-chat-export.py`) and include each event node's `composite` + `reading_order` (at minimum `composite`) on the node record. Rebuild the bundle. Verify the field appears in `web/data/nodes.json`.

### Step 2 — sort `walkChain` by chronology, and stop merging up/down
In `web/src/lib/graph.ts`, `walkChain()` returns `{upstream, downstream, enables}` currently ordered by `depth`. Change the ordering to sort by the node's `composite` (fallback `reading_order`; nodes with neither sort last, stably). **Keep `upstream` and `downstream` as separate rendered lists** — the front-end (`web/public/app.js`) must not concatenate them into one "what led to" list (that's what surfaced the forward MOTIVATES edge as a cause). Keep `deno task test` green; add/adjust a regression test that asserts the Bran chain sorts AGOT→ADWD.
- **COORDINATE:** `web/src/lib/graph.ts` + `graph_test.ts` had UNCOMMITTED Matt edits during S184 — check `git status`/`git log` first; do not clobber his in-flight work. If his edits are still uncommitted, ask before touching the file.

### Step 3 (can be a separate session) — deterministic date backfill
Raise the 33% dated-event coverage WITHOUT Fable:
- **Deterministic first:** many event wiki pages carry a date. Read the LOCAL cache `sources/wiki/_raw/<Page>.json` (NEVER re-fetch — hard rule) for each undated event's `wiki_source`; regex-extract "NNN AC" / date ranges from infobox/prose. Write `occurred.ac_year` where confidently found.
- **Haiku for the residue** — cheap bulk dating from prose where the wiki has no clean field. Confirm with Matt before launching any extraction pass (`feedback_no_extraction_without_asking`).
- **Do NOT use Fable for this** — dating is not a reasoning-hard task (S184 decision).
- Start with `working/event-chronology-backfill-queue.md` (the 50 undated events on causal chains — highest value).
- After any `ac_year` writes, **re-run `scripts/build-event-sort-keys.py`** to refresh the composite keys, then rebuild the bundle.

## Success criteria
- Bundle carries `composite`; `walkChain` sorts by it; up/down stay separate; the Bran & Rebellion chains render chronologically on a draft deploy; tests green.
- (If step 3 done) dated-event coverage up measurably; sort keys + bundle regenerated.

## DO NOT
- Do not re-fetch the wiki (read `sources/wiki/_raw/` only).
- Do not use Fable for dating (Haiku for residue; deterministic first).
- Do not clobber Matt's uncommitted `graph.ts`/web edits — coordinate.
- Do not run any extraction/Haiku pass without Matt's explicit OK.
- Do not run `/endsession` without explicit permission.

## Also queued (not this track)
- Relational/quote ordering: "who is connected to Jon Snow" returns quotes out of order — likely prompt-side, a chat-UI note. Route through the alpha-tester-notes track.
- Matt has more alpha-tester notes to feed in (`2026-07-01-chat-ui-alpha-tester-notes.md`, Matt-gated).
