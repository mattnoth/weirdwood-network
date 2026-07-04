# SESSION 185 — Finish the chronology render fix + turn on usage logging (deterministic; no Fable)

> **This is Session 185.** Stamp your worklog entry `### Session 185` at endsession.
> **Recommended model:** Sonnet 4.6 (deterministic TS + Python wiring; Haiku — NOT Fable — for the optional date-backfill sub-step).

## Background (what S184 established)

The live chat UI (https://weirwood-network.netlify.app) renders causal chains **out of chronological order** (e.g. "what led to Robert's Rebellion" shows a forward `MOTIVATES` edge to Robert's Dany-assassination order ~15y later; a Bran chain shows the ADWD cave before AGOT Bran 2). S184 proved this is a **traversal/render** bug, not bad data:
- The deployed walker is `walkChain()` in `web/src/lib/graph.ts` (TS reimpl — NOT `scripts/graph-query.py`). It sorts by graph hop-**depth**, never chronology, and merges upstream+downstream into one list.
- A temporal-inversion scan over all 170 causal (CAUSES/TRIGGERS/MOTIVATES) edges found **0** cause-after-effect inversions → the causal layer is directionally sound.
- The deployed `web/data/edges.json` carries only 7 fields — temporal signal was stripped at bundle build.

S184 shipped (committed) `scripts/build-event-sort-keys.py`, stamping a `sort_keys:` block onto all 744 event nodes:
```yaml
sort_keys:
  composite: "0300.5.035"   # story-time key: {ac_year:04d}.{book_order}.{chapter:03d} — null if undated
  reading_order: "5.035"    # reading-order fallback
  basis: "year+chapter"
  # + ac_year, book_order, chapter_number, chapter_label
```

This session has **two independent, both-shippable-in-one-deploy** improvements (A + B), plus optional deterministic follow-ups (C, D).

---

## Step A — Wire the sort key into the live render (THE bug fix)

**A1 — bundle.** The deployed `web/data/*.json` strips temporal fields. Find the bundle builder (grep for what writes `web/data/` — likely `scripts/build-chat-export.py`) and include each event node's `sort_keys.composite` + `reading_order` on the node record. Rebuild. Verify the field appears in `web/data/nodes.json`.

**A2 — `walkChain`.** In `web/src/lib/graph.ts`, `walkChain()` returns `{upstream, downstream, enables}` ordered by `depth`. Change ordering to sort by the node's `composite` (fallback `reading_order`; nodes with neither sort last, stably). **Keep `upstream` and `downstream` as SEPARATE rendered lists** — the front-end (`web/public/app.js`) must not concatenate them into one "what led to" list (that concat is what surfaced the forward MOTIVATES edge as a cause). Keep `deno task test` green; add a regression test asserting the Bran chain sorts AGOT→ADWD.

> **COORDINATE:** `web/src/lib/graph.ts` + `graph_test.ts` had UNCOMMITTED Matt edits during S184. Check `git status`/`git log` first; if his edits are still uncommitted, ask before touching the file — do not clobber his in-flight work.

---

## Step B — Turn on usage logging (independent, ~10 lines; starts the data clock)

**Why now:** logging is the SUBSTRATE for the whole future Fable program (see Downstream). Its value compounds with time, so turn it on now — by the time Fable is used heavily, weeks of real chains have accumulated to prioritize from. Zero dependency on Step A; ships in the same deploy.

Full spec (from the S184 logging advisor — follow exactly):
- Reuse the existing `getStore("weirwood-chat")` in `web/netlify/edge-functions/chat.ts`.
- **Write each turn to a UNIQUE key:** `` `log/${new Date().toISOString().slice(0,10)}/${crypto.randomUUID()}` `` (date-partition prefix + UUID leaf). **NEVER read-modify-write** — the daily spend counter (`readDailySpend`/`addDailySpend`) uses read-modify-write and RACES under concurrency; do NOT copy that pattern for logs or you'll lose turns.
- **Value** = JSON of what the `done` event already assembles: `question` (last user turn), the assembled `prose` answer, the **chain node IDs / refs** (so a broken chain is deterministically replayable later), `toolCalls`, `grounding`, `unverifiedCites`, `usage`, `costUsd`, `stopState`, `model`, ISO `timestamp`.
- **Location:** inside the existing `try` in the stream's `start()`, right AFTER `addDailySpend(costUsd)`. It's network I/O, not CPU — it does NOT touch the 50 ms edge CPU budget. Wrap in its own `try/catch` and swallow failures (**logging must never fail a turn**).
- **Fallback:** also mirror a compact one-line record to `console.log` (Netlify function logs) so an absent/throwing Blobs context still leaves a record.
- Do **NOT** log raw assistant content blocks (thinking/tool_use) — store the assembled `prose` string + the structured receipts only.
- **Read-back:** a small local script using `@netlify/blobs` — `store.list({ prefix: "log/YYYY-MM-DD/" })` then `get` each key. Fine at portfolio scale (single-digit turns/day → just eyeball them).
- Do **NOT** stand up Log Drains / Axiom / an external DB / a Google Sheet — overkill; Blobs + grep is the right size.

**Privacy posture** (public-ish portfolio site; questions are about fictional Westeros):
- Add a one-line footer note (e.g. "questions may be logged to improve the graph").
- Do **NOT** store IP or request headers (not needed for defect-hunting; not-collecting beats promising-to-protect).
- Add a 30-day retention sweep — date-prefixed keys make "delete anything older than 30 days" a trivial `list` + `delete` loop (a tiny script run occasionally).

---

## Step C — Deterministic date backfill (OPTIONAL; can be its own later session)

Raise the 33% dated-event coverage WITHOUT Fable:
- **Deterministic first:** many event wiki pages carry a date. Read the LOCAL cache `sources/wiki/_raw/<Page>.json` (NEVER re-fetch — hard rule) for each undated event's `wiki_source`; regex-extract "NNN AC" / date ranges from infobox/prose; write `occurred.ac_year` where confidently found.
- **Haiku for the residue** — cheap bulk dating from prose. **Confirm with Matt before launching any extraction pass** (`feedback_no_extraction_without_asking`).
- Start with `working/event-chronology-backfill-queue.md` (the 50 undated events on causal chains — highest value).
- After any `ac_year` writes, **re-run `scripts/build-event-sort-keys.py`**, then rebuild the bundle (Step A1).

## Step D — Same-year intra-chapter inversion scan (deterministic, quick)

S184's scan found 0 inversions at YEAR granularity; the composite key is now chapter-resolution, so close the caveat: for causal edges whose source & target share `ac_year`, compare the full `composite` (book_order, chapter_number) and flag source-after-target. Report the count (likely a handful). **Propose, don't auto-flip** — route genuine ones to review.

---

## Success criteria
- Bundle carries `composite`; `walkChain` sorts by it; upstream/downstream stay separate; the Bran & Rebellion chains render chronologically on a **draft deploy**; `deno task test` green.
- Logging: each live turn writes a `log/DATE/uuid` Blobs record; a local read-back script prints question + chain; footer note added; no IP stored.

## DO NOT
- Do not re-fetch the wiki (read `sources/wiki/_raw/` only).
- Do not use Fable for dating (Haiku for residue; deterministic first).
- Do not copy the spend-counter's read-modify-write pattern for logging (it races).
- Do not clobber Matt's uncommitted `graph.ts`/web edits — coordinate.
- Do not run any extraction/Haiku pass without Matt's explicit OK.
- Do not run `/endsession` without explicit permission.

---

## Downstream — the Fable program (NOT this session; captured so it's not lost)

**Logging (Step B) is the GATE.** Once real usage accumulates, Fable's role = **FIND**, cheap tools **FILL**. Matt's plan: use Fable a lot *after* logging is live, pointed by the logs. Guidance from the S184 boards:
- **Best use = grounded gap-finder / completeness critic.** Feed Fable a *bounded slice* — one built arc as its actual nodes + edges + evidence quotes + the schema/vocab — and ask "what's **missing / wrong / thin** a deep ASOIAF reader would notice?" This turns Fable's in-weights world-knowledge into a targeted enrichment worklist. (Cold "how do I improve the graph" = generic; bounded+grounded = specific and actionable.)
- **Also:** cross-arc seam detection (hand it 2 arcs → existing-node↔existing-node links that span them — the "4th causal-wiring lens" the per-topic enrichment lenses miss); per-chain coherence review on the chains the logs show users actually walk.
- **Pattern:** per-CHAIN/cluster, not per-edge; **interpretive edge types only** (structural ~12k SWORN_TO/HOLDS_TITLE/PARENT_OF never touched); Fable **PROPOSES to a candidates/backlog file, never auto-writes** (enrichment is gated/pollution-sensitive); tag any resulting mutation with a `run_id` (reversible on the monolithic `edges.jsonl`); validate out-of-sample + fresh-verify before any scaled run; run **ONE calibration arc** before spending more of the weekly cap.
- Fable is **NOT** for dating/backfill (that's Step C's deterministic→Haiku ladder).

## Also queued (not this track)
- Relational/quote ordering: "who is connected to Jon Snow" returns quotes out of order — likely prompt-side; route through the alpha-tester-notes track.
- Matt has more alpha-tester notes (`2026-07-01-chat-ui-alpha-tester-notes.md`, Matt-gated).
