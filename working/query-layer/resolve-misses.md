# Resolve-Miss Report — mined from live chat-UI telemetry

Generated: 2026-07-04T20:31:51.917Z
Date range covered: 2026-07-03 .. 2026-07-04 (2 days)
Turns scanned: 20
`resolve` call sites found: 34
Distinct normalized phrases: 24

## Auth / data-access outcome: OK

Blobs store reached read-only via the `@netlify/blobs` SDK (same stack as `read-logs.ts`). No writes or deletes were issued against the store.

## Logging-gap finding — read before trusting the outcome column

The persisted `TurnLog.toolTrace` (chat.ts / agent.ts `AgentResult.toolTrace`) stores **`{tool, input}` only** — never the tool's result. `resolve()`'s actual return (hit/fuzzy/miss, score, candidate slugs) is therefore **not captured anywhere in the log record**; the live SSE `receipt` event carries it but only reaches the browser, never Blobs. This script recovers the true outcome **deterministically** by re-running the production `resolve()` (web/src/lib/resolve.ts) against the CURRENT `web/data/` bundle for every logged phrase — not by inferring it from trace shape. Two caveats follow from that: (1) if the graph/alias-map has changed since a given turn ran, the outcome shown here is the outcome AS OF THE CURRENT BUNDLE, not necessarily what the live app actually returned that day; (2) a `resolve` call followed immediately by a `read_node`/`walk_chain` on a DIFFERENT slug than the top candidate here (the model picked its own candidate from the list, or moved on to a different phrase) isn't flagged — this report only re-derives resolve()'s own answer, not what the model did with it. **Recommendation:** log the resolve() result (or at minimum matchType + topSlug + score) directly in TurnLog going forward — see `## Recommendation` below.

## Ranked queue (misses first, then fuzzy low-to-high score, then exact)

| Phrase | Outcome | Top candidate | # candidates | Frequency | Example question(s) |
|---|---|---|---|---|---|
| Purple Wedding feast seventy-seven courses | MISS | — | 0 | 1 | "Give me some lavishly described meals " |
| Roose Bolton betrays Robb Stark | MISS | — | 0 | 1 | "Why did Roose Bolton betray Robb stark? Why did he even allow his bastard to be …" |
| murders at Winterfell during the wedding feast | MISS | — | 0 | 1 | "How is it fraying around them? " |
| Joffrey and Margaery wedding seventy-seven dishes | fuzzy (0.55) | `wedding-ceremony-at-the-great-sept-of-baelor` | 1 | 1 | "Give me some lavishly described meals " |
| Roose Bolton and Ramsay Bolton meeting | fuzzy (0.6) | `roose-bolton` | 5 | 1 | "Roose and Ramsey meet in the books?" |
| Daenerys feast in Meereen | fuzzy (0.717) | `dany-mounts-drogon-and-flees-meereen` | 1 | 1 | "Give me some lavishly described meals " |
| Bolton hold on the North | fuzzy (0.717) | `roose-named-warden-of-the-north` | 1 | 1 | "How is it fraying around them? " |
| royal wedding feast | fuzzy (0.767) | `wedding-feast-at-the-red-keep` | 4 | 1 | "Give me some lavishly described meals " |
| feast in the Great Hall | fuzzy (0.767) | `great-hall-red-keep` | 5 | 1 | "Give me some lavishly described meals " |
| Arya travels to Braavos | fuzzy (0.767) | `arya-departs-for-braavos` | 1 | 1 | "How did Arya end up in bravos? " |
| feast at Winterfell | fuzzy (1) | `feast-in-honor-of-king-roberts-visit-to-winterfell` | 5 | 1 | "Give me some lavishly described meals " |
| Arya in Braavos | fuzzy (1) | `arya-departs-for-braavos` | 5 | 1 | "What did she fine there " |
| Red Wedding | exact | `red-wedding` | 1 | 4 | "How many people died at the red wedding "; "Why did Roose Bolton betray Robb stark? Why did he even allow his bastard to be …"; "What citation are you talking about? " |
| Robert's Rebellion | exact | `roberts-rebellion` | 1 | 3 | "Why did Robert's Rebellion start?" |
| Roose Bolton | exact | `roose-bolton` | 1 | 3 | "What is there status at the end of the book "; "Why did Roose Bolton betray Robb stark? Why did he even allow his bastard to be …"; "How is it fraying around them? " |
| Ramsay Bolton | exact | `ramsay-snow` | 1 | 3 | "What is there status at the end of the book "; "Roose and Ramsey meet in the books?"; "Why did Roose Bolton betray Robb stark? Why did he even allow his bastard to be …" |
| Hodor | exact | `hodor` | 1 | 2 | "Who is Hodor, in one sentence?" |
| Brienne of Tarth | exact | `brienne-tarth` | 1 | 1 | "Who did brienne meet in book four? How do we know catelyn is stone heart?" |
| Lady Stoneheart | exact | `catelyn-stark` | 1 | 1 | "Who did brienne meet in book four? How do we know catelyn is stone heart?" |
| Purple Wedding | exact | `purple-wedding` | 1 | 1 | "Give me some lavishly described meals " |
| Arya Stark | exact | `arya-stark` | 2 | 1 | "How did Arya end up in bravos? " |
| Jon Snow | exact | `jon-snow` | 1 | 1 | "Who are Jon Snow's parents?" |
| Tywin Lannister | exact | `tywin-lannister` | 1 | 1 | "Who is Tywin Lannister?" |
| House of Black and White | exact | `house-of-black-and-white` | 1 | 1 | "What did she fine there " |

## Recommendation

Add `resolveOutcomes: Array<{phrase, matchType, topSlug, score, candidateCount}>` (or fold matchType/topSlug/score into each `toolTrace` entry) to `TurnLog` in chat.ts, populated from `harvestResult`'s already-available `dispatchTool` return for `resolve` calls specifically. That turns this proxy re-derivation into a direct read and removes both caveats above.
