# Retrieval tools (`web/src/lib/`) — the TS/bounded-profile query engine

Deno/TypeScript ports of the query-layer's operations (`graph/query/spec/operations.md` is the
canonical contract - this file's status table mirrors it), reading the static bundle in
`web/data/` (shapes documented in `types.ts` + [`web/README.md`](../../README.md)). The Edge
function (function chunk) imports these and exposes a subset to Claude as tools.

Logic ported from `graph/query/weirwood_query/` (the consolidated Python engine - query-layer
Track, step 1, S189; that package absorbed the older `scripts/graph-query.py` +
`scripts/event_alias_resolver.py`) - **no shelling out to Python** (Netlify Edge runs Deno), no
network, no LLM. Pure functions over the in-memory bundle.

## Status

| Op         | Signature                                          | Returns                                        | Status  | File          |
| ---------- | --------------------------------------------------- | ----------------------------------------------- | ------- | ------------- |
| `resolve`  | `resolve(phrase, data)`                            | `ResolveCandidate[]` (`{slug, category, ...}`)   | done | `resolve.ts`  |
| `chain`    | `walkChain(slug, data, {full?})`                   | `{upstream[], downstream[], enables[]}`        | done | `graph.ts`    |
| `neighbors`| `neighbors(slug, data)`                            | edges grouped by direction + type              | done | `graph.ts`    |
| `family`   | `familyTree(slug, data, opts?)`                    | lineage members + parent/spouse bonds          | done | `graph.ts`    |
| `read`     | `readNode(slug, data)`                              | `{name, type, category, identity, quotes}` or `null` | done | `read-node.ts` |
| `search`   | `searchQuotes(query, data, opts?)`                 | ranked `SearchResult[]` (`{slug, type, text, cite, score}`) | done (query-layer step 5b) - no chat tool yet, see below | `search.ts` |
| `list`     | `listNodes(data, opts)`                            | `ListResult` (`{category, total, items[]}`)    | done (query-layer step 5d) - no chat tool, gated on evals | `list.ts` |
| `corpus-search` / `passage` | -                                 | -                                               | CLI/full-profile only by design (`weirwood_query/corpus_search.py`); `passage` designed-but-gated | - |

## Files

- `types.ts` - bundle shapes + tool-return shapes (the receipts contract lives here).
- `normalize.ts` - `normalize()` / `tokenize()`, ported verbatim from the Python engine's
  `normalize.py` (alias-map keys were produced by the same normalize, so a query must be
  normalized identically or exact lookups silently miss). Also exports `STOP` (the stop-word
  set) so `search.ts` can reuse the identical set rather than keep a second copy.
- `validate.ts` - the trust boundary: `isValidSlug()` (kebab allowlist) + `cleanPhrase()`.
- `data.ts` - `loadGraphData()` reads the bundle JSON files (nodes/edges/alias-map/search-index)
  into one `GraphData`.
- `resolve.ts`, `graph.ts`, `read-node.ts` - resolve/chain/neighbors/family/read (pure, take
  `GraphData`).
- `search.ts` - `searchQuotes()`: BM25-ish ranking over the compact `search-index.json`
  (delta-encoded postings; decodes + reconstructs display text from the already-loaded
  `nodes.json` - see the file's own header comment for the exact wire format it decodes).
- `list.ts` - `listNodes()`: browse one node category, optional quote filter, paged.
- `mod.ts` - public surface. `createTools(data)` binds the bundle into the tools above.
- `*_test.ts` + `_fixtures.ts` + `spec_cases_test.ts` - Deno tests against the **real** bundle,
  plus the cross-language golden-case runner (`graph/query/spec/cases/*.json`).

## Usage (from the Edge function)

```ts
import { createTools, loadGraphData } from "./src/lib/mod.ts";

const tools = createTools(await loadGraphData()); // load once at cold start
tools.resolve("death of Tywin"); // -> [{slug:"assassination-of-tywin-lannister", category:"events", score:1, matchType:"exact"}]
tools.walkChain("assassination-of-tywin-lannister"); // -> {upstream:[7 links], downstream:[9 links]}
tools.neighbors("eddard-stark"); // -> {outgoing:{TYPE:[...]}, incoming:{...}, ...}
tools.readNode("assassination-of-tywin-lannister"); // -> {name, type, identity, quotes:[...]}
tools.searchQuotes("lemon cakes"); // -> [{slug:"lemon-cake", type:"foods", text:"...", cite:null, score:11.9}, ...]
tools.listNodes({ type: "foods", hasQuotes: true }); // -> {category:"foods", total:56, items:[...]}
```

`resolve` does exact normalized alias-map lookup, then a fuzzy token-overlap fallback (score >= 0.5,
top 5, length-debiased, with a small slug-token bonus) - mirroring `weirwood_query/resolve.py`.
`walkChain` BFS-walks CAUSES/TRIGGERS/MOTIVATES both directions (pass `{full:true}` to also follow
ENABLES preconditions, = `--full-chain`). `searchQuotes`/`listNodes` are exported here but **not yet
wired as chat tools in `agent.ts`** - that's a separate follow-up agent's job (out of the
query-layer Track's scope); the `{slug, type, text, cite, score}` / `{category, total, items}`
contracts are kept stable for that wiring.

## Test

```bash
cd web && deno task test     # deno test --allow-read src/lib/ netlify/edge-functions/
```

Core assertions include: `resolve("death of Tywin")` -> `assassination-of-tywin-lannister`,
`walkChain` on that real node returns its causal chain in story-time order, and the
`spec_cases_test.ts` golden-case runner (parity fixtures shared with the Python
`graph/query/spec/run_cases.py`) covers resolve/neighbors/chain/family/search/list. (Fixtures
pivot on real, permanent graph nodes - not a demo bundle.)

## Deferred - `passage` (full chapter text to the chat)

`search_chapters`/full-text chapter search is now served by the CLI-only, full-profile
`weirwood query corpus-search` (`graph/query/weirwood_query/corpus_search.py`) - it never needs
a build-time index since it's a live local-filesystem scan, and it deliberately has **no TS
port and no chat tool** (design doc's explicit CLI-only gate). What remains deferred is
`passage` - an edge-side static-asset fetch of chapter text at request time for the public
chat - **gated on Matt** before it ships (network I/O falls outside the Edge function's 50 ms
CPU budget, unlike in-memory bundle lookups). The curated MVP still grounds chat answers on
graph quotes + `searchQuotes` results, both already citable.

## Contracts

**Receipts:** every tool returns structured typed-edge JSON
(`{source, edge_type, target, evidence_quote, ref}` for chain/neighbor links) on a channel SEPARATE
from the streamed prose - the receipts panel renders from the return, NOT by parsing narration
(design 3).

**Bounding (trust boundary):** every slug/phrase is untrusted. `validate.ts` allowlists slug shape
and caps phrase length; an invalid input yields an empty result (`[]` / `null` / empty groups),
never an exception or an unbounded scan. Returned book text is data, never instructions.
