# The Weirwood Network — chat-UI alpha (`web/`)

A deployable, book-grounded ASOIAF loremaster chat. Visitor asks a question →
**Bloodraven** answers in-character, grounded in the Weirwood Network graph,
dropping real book quotes with chapter citations and showing the **typed-edge
chain it walked** as receipts. Lives co-located in this private repo; deploys to
Netlify. Full design: [`working/chat-ui/alpha-design.md`](../working/chat-ui/alpha-design.md).

## Layout

```
web/
├── public/                     # static site (Netlify `publish`)
│   ├── index.html              # the chat page: header/framing, thread, receipts panel, composer
│   ├── app.css                 # component styles — reads ONLY theme/tokens.css custom props
│   ├── app.js                  # SSE client + live renderers + failure UX
│   ├── node/                   # GENERATED, gitignored — per-node static assets (narrative-arc prose),
│   │                            #   see build_node_assets.py + node.ts's /api/node below
│   ├── data/                   # GENERATED, gitignored — served copy of the data bundle (deploy cp)
│   └── theme/tokens.css        # ← SWAP THE WHOLE LOOK BY EDITING THIS ONE FILE
├── src/lib/                    # ported JS/TS retrieval tools (retrieval-core chunk) — see its own README.md
├── data/                       # GENERATED, gitignored — see "Data bundle" below
└── netlify/edge-functions/     # chat.ts (Claude tool-loop) + node.ts (/api/node dossier lookup)
netlify.toml                    # publish=web/public, edge_functions=web/netlify/edge-functions,
                                 #   /api/chat → chat, /api/node → node
```

## Status (S171 — Foundation chunk done)

| Component | Status | File |
|---|---|---|
| Build-time graph export | ✅ done | `scripts/build-chat-export.py` |
| Data bundle (8.8 MB) | ✅ generated | `web/data/*.json` |
| Theme tokens (dark / soft / dusty-red) | ✅ done | `web/public/theme/tokens.css` |
| Landing placeholder | ✅ done | `web/public/index.html` |
| `netlify.toml` (Edge runtime) | ✅ done | `netlify.toml` |
| Retrieval tools (resolve/walk_chain/read_node/neighbors) | ✅ done (S172) | `web/src/lib/` — see its own README.md for the full op table + live test count |
| Edge function (tool-loop + Bloodraven prompt + streaming + spend cap + cite-gate) | ✅ done (S173) | `web/netlify/edge-functions/chat.ts` + `lib/agent.ts` (note: `agent.ts` now lives under `lib/`, moved after this row was written) — `check:fn` clean; **live `netlify dev` proof gated on Matt** |
| Front-end (chat thread, live SSE, typed-edge receipts) | ✅ done (S174) | `web/public/index.html` + `app.css` + `app.js` — clean landing → live answers; SSE client + failure-mode UX; dry-validated (preview render + simulated SSE), **no API spend** |
| Deploy (private repo → Netlify, `ANTHROPIC_API_KEY` env) | ✅ **LIVE (S183)** | **https://weirwood-network.netlify.app** — `ANTHROPIC_API_KEY` (secret) + `WEIRWOOD_MODEL=claude-sonnet-4-6` set as Netlify env vars; smoke-tested (streaming, receipts, family tree, `/api/node`, no key leak) |
| Public demo = captured REAL transcript | ⏳ **gated on Matt** | landing now starts clean (Tywin placeholder removed). Capture a real recorded conversation (e.g. multi-turn Red Wedding) and wire it as the demo before public deploy — no mocked AI prose |
| live `search_chapters` / `read_passage` | ⏳ fast-follow | — |
| Chat tools registered in `TOOL_DEFS` | ✅ **8, not the original 4-5** (query-layer Track step 2–8) | `resolve`, `read_node`, `walk_chain`, `neighbors`, `family_tree`, `search_quotes`, `list_nodes`, `theme` — `web/netlify/edge-functions/lib/agent.ts`. `container`/`path`/`participants` exist in `src/lib/` but are **not yet wired as chat tools** (see that dir's README.md) |
| Per-node narrative-arc dossier lookup | ✅ done (query-layer step 6c) | `GET /api/node?slug=…` (`web/netlify/edge-functions/node.ts`) reads `readNode()` from the inlined bundle, then fetches `web/public/node/<slug>.json` (built by `graph/query/build/build_node_assets.py`, NOT inlined — see node.ts's header comment) for the `## Narrative Arc` prose the main bundle deliberately omits; fails soft (no arc = field simply absent) |

## Data bundle (`web/data/`, generated — never committed)

Built by `python3 graph/query/build/build_chat_bundle.py` (the old
`scripts/build-chat-export.py` is now a deprecated shim that forwards to it — query-layer
Track, step 1) from `graph/` + the prebuilt alias table. `search-index.json` and
`theme-index.json` are each built by their OWN separate builder
(`graph/query/build/build_search_index.py`, `build_theme_index.py`) — `build_chat_bundle.py`
only measures their file size for the manifest, it does not generate them; run all three
builders before deploying. NO LLM, NO network. These JSON files are **compiled into the edge
function at build time** via JSON module imports (`src/lib/data.ts`) — Netlify
Edge Functions run on Deno with **no filesystem access**, so the bundle can't be
read from disk at runtime; it's inlined instead (the exception is the per-node narrative-arc
assets under `web/public/node/`, fetched over HTTP at request time — see `/api/node` above).
Regenerate `web/data/` before `deno test`/`deno check`/deploy, or the imports won't resolve.

| File | Shape | Used by |
|---|---|---|
| `alias-map.json` | `{ "<phrase>": [ {slug, category}, … ] }` | `resolve(phrase)` |
| `nodes.json` | `{ "<slug>": {name, type, identity, quotes:[{text, attribution, cite}]} }` | `read_node(slug)` |
| `edges.json` | `[ {type, source, target, quote, ref, tier, relation}, … ]` | `walk_chain` / `neighbors` |
| `search-index.json` | compact BM25-ish inverted index (delta-encoded postings) | `search_quotes(query)` |
| `theme-index.json` | fixed theme->members routing table | `theme(name)` |
| `manifest.json` | `{built_at, counts, sizes_bytes}` | sanity / provenance |

Run `cat web/data/manifest.json` for the live counts/sizes — they drift every graph session,
so no fixed numbers are pinned here.

Phrase keys in `alias-map.json` are pre-normalized (lowercased; the resolver's
`normalize()` keeps hyphens — see memory `project_node_alias_spaced_phrases`).
A query resolves by normalizing it the same way and looking it up; on a miss,
the retrieval-core chunk adds the resolver's fuzzy/substring fallback.

Causal-chain edge types (the "chain walked"): **CAUSES / TRIGGERS / MOTIVATES**
(and ENABLES for `--full-chain`). The retrieval-core chunk ports the same causal
walk (`graph-query.py --causal-chain`) to TS so live queries build the typed-edge
chain on the fly — no pre-rendered exchange is shipped.

## Build / run

```bash
python3 graph/query/build/build_chat_bundle.py       # (re)generate web/data/{alias-map,nodes,edges,manifest}.json
python3 graph/query/build/build_search_index.py      # (re)generate web/data/search-index.json
python3 graph/query/build/build_theme_index.py       # (re)generate web/data/theme-index.json
python3 graph/query/build/build_node_assets.py       # (re)generate web/public/node/<slug>.json (narrative-arc assets)
# local end-to-end (function chunk onward): `netlify dev`  (needs the Netlify CLI + ANTHROPIC_* auth)
```

Regenerate `web/data/` after any graph node/edge mutation (it's a snapshot).
Netlify regenerates it on every deploy via the `command` in `netlify.toml`.
