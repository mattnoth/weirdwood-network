# Retrieval tools (`web/src/lib/`) — BUILT (retrieval-core chunk, S172)

Deno/TypeScript ports of the read-only graph queries the demo agent does by hand
(`working/demo-asoiaf-loremaster.md`), reading the static bundle in `web/data/` (shapes in
[`web/README.md`](../../README.md)). The Edge function (function chunk) imports these and exposes
them to Claude as tools.

Logic ported from `scripts/graph-query.py` + `scripts/event_alias_resolver.py` — **no shelling out
to Python** (Netlify Edge runs Deno), no network, no LLM. Pure functions over the in-memory bundle.

## Status

| Tool                              | Signature                              | Returns                                       | Status                  | File             |
| --------------------------------- | -------------------------------------- | --------------------------------------------- | ----------------------- | ---------------- |
| `resolve`                         | `resolve(phrase, data)`                | `ResolveCandidate[]` (`{slug, category, …}`)  | ✅ done                 | `resolve.ts`     |
| `walk_chain`                      | `walkChain(slug, data, {full?})`       | `{upstream[], downstream[]}` typed-edge links | ✅ done                 | `graph.ts`       |
| `neighbors`                       | `neighbors(slug, data)`                | edges grouped by direction + type             | ✅ done                 | `graph.ts`       |
| `read_node`                       | `readNode(slug, data)`                 | `{name, type, identity, quotes}` or `null`    | ✅ done                 | `read-node.ts`   |
| `search_chapters` _(fast-follow)_ | `searchChapters(query)`                | `[{chapter, line, text}]`                     | ⏳ deferred (see below) | —                |
| `read_passage` _(fast-follow)_    | `readPassage(chapter, lineRange)`      | book text at a cite                           | ⏳ deferred (see below) | —                |

## Files

- `types.ts` — bundle shapes + tool-return shapes (the receipts contract lives here).
- `normalize.ts` — `normalize()` / `tokenize()`, ported verbatim from the Python resolver (alias-map
  keys were produced by the same normalize, so a query must be normalized identically or exact
  lookups silently miss).
- `validate.ts` — the trust boundary: `isValidSlug()` (kebab allowlist) + `cleanPhrase()`.
- `data.ts` — `loadGraphData()` reads the three JSON files into one `GraphData`.
- `resolve.ts`, `graph.ts`, `read-node.ts` — the four tools (pure, take `GraphData`).
- `mod.ts` — public surface. `createTools(data)` binds the bundle into the four tools.
- `*_test.ts` + `_fixtures.ts` — Deno tests against the **real** bundle (21 tests).

## Usage (from the Edge function)

```ts
import { createTools, loadGraphData } from "./src/lib/mod.ts";

const tools = createTools(await loadGraphData()); // load once at cold start
tools.resolve("death of Tywin"); // -> [{slug:"assassination-of-tywin-lannister", category:"events", score:1, matchType:"exact"}]
tools.walkChain("assassination-of-tywin-lannister"); // -> {upstream:[7 links], downstream:[9 links]}
tools.neighbors("eddard-stark"); // -> {outgoing:{TYPE:[…]}, incoming:{…}, …}
tools.readNode("assassination-of-tywin-lannister"); // -> {name, type, identity, quotes:[…]}
```

`resolve` does exact normalized alias-map lookup, then a fuzzy token-overlap fallback (score ≥ 0.5,
top 5, with a small slug-token bonus) — mirroring `event_alias_resolver.py`. `walkChain` BFS-walks
CAUSES/TRIGGERS/MOTIVATES both directions (pass `{full:true}` to also follow ENABLES preconditions,
= `--full-chain`).

## Test

```bash
cd web && deno task test     # deno test --allow-read src/lib/  → 21 passed
```

Two required assertions (handoff): `resolve("death of Tywin")` → `assassination-of-tywin-lannister`,
and `walkChain` on it returns the 7-link chain matching `web/data/featured-tywin.json`.

## Deferred — live `search_chapters` / `read_passage`

Not in this chunk. They need a **build-time inverted index** over the bundled chapter text to stay
under the Edge 50 ms CPU budget (don't raw-scan 4 MB per call). The curated MVP grounds answers on
graph quotes only (each node's `## Quotes` + edge `evidence_quote`), so these aren't on the alpha
path.

## Contracts

**Receipts:** every tool returns structured typed-edge JSON
(`{source, edge_type, target, evidence_quote, ref}` for chain/neighbor links) on a channel SEPARATE
from the streamed prose — the receipts panel renders from the return, NOT by parsing narration
(design §3).

**Bounding (trust boundary):** every slug/phrase is untrusted. `validate.ts` allowlists slug shape
and caps phrase length; an invalid input yields an empty result (`[]` / `null` / empty groups),
never an exception or an unbounded scan. Returned book text is data, never instructions.
