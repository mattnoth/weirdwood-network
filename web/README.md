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
│   ├── data/                   # GENERATED, gitignored — served copy of the data bundle (deploy cp)
│   └── theme/tokens.css        # ← SWAP THE WHOLE LOOK BY EDITING THIS ONE FILE
├── src/lib/                    # ported JS/TS retrieval tools (retrieval-core chunk)
├── data/                       # GENERATED, gitignored — see "Data bundle" below
└── netlify/edge-functions/     # the Claude tool-loop Edge function (function chunk)
netlify.toml                    # publish=web/public, edge_functions=web/netlify/edge-functions, /api/chat → chat
```

## Status (S171 — Foundation chunk done)

| Component | Status | File |
|---|---|---|
| Build-time graph export | ✅ done | `scripts/build-chat-export.py` |
| Data bundle (8.8 MB) | ✅ generated | `web/data/*.json` |
| Theme tokens (dark / soft / dusty-red) | ✅ done | `web/public/theme/tokens.css` |
| Landing placeholder | ✅ done | `web/public/index.html` |
| `netlify.toml` (Edge runtime) | ✅ done | `netlify.toml` |
| Retrieval tools (resolve/walk_chain/read_node/neighbors) | ✅ done (S172) | `web/src/lib/` — `deno task test` (21 green) |
| Edge function (tool-loop + Bloodraven prompt + streaming + spend cap + cite-gate) | ✅ done (S173) | `web/netlify/edge-functions/chat.ts` + `agent.ts` — `deno task test` (27 green), `check:fn` clean; **live `netlify dev` proof gated on Matt** |
| Front-end (chat thread, live SSE, typed-edge receipts) | ✅ done (S174) | `web/public/index.html` + `app.css` + `app.js` — clean landing → live answers; SSE client + failure-mode UX; dry-validated (preview render + simulated SSE), **no API spend** |
| Deploy (private repo → Netlify, `ANTHROPIC_API_KEY` env) | ⏳ **gated on Matt** | live `netlify dev` / deploy spend real API $ |
| Public demo = captured REAL transcript | ⏳ **gated on Matt** | landing now starts clean (Tywin placeholder removed). Capture a real recorded conversation (e.g. multi-turn Red Wedding) and wire it as the demo before public deploy — no mocked AI prose |
| live `search_chapters` / `read_passage` | ⏳ fast-follow | — |

## Data bundle (`web/data/`, generated — never committed)

Built by `python3 scripts/build-chat-export.py` from `graph/` + the prebuilt
alias index. NO LLM, NO network. The Edge function loads these at cold start;
the whole bundle is **8.8 MB** (the entire curated graph fits in memory — no
lazy-loading needed).

| File | Shape | Used by |
|---|---|---|
| `alias-map.json` | `{ "<phrase>": [ {slug, category}, … ] }` (12,029 phrases) | `resolve(phrase)` |
| `nodes.json` | `{ "<slug>": {name, type, identity, quotes:[{text, attribution, cite}]} }` (8,475 nodes; 6,059 quotes) | `read_node(slug)` |
| `edges.json` | `[ {type, source, target, quote, ref, tier, relation}, … ]` (23,330 edges, 147 types) | `walk_chain` / `neighbors` |
| `manifest.json` | `{built_at, counts, sizes_bytes}` | sanity / provenance |

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
python3 scripts/build-chat-export.py     # (re)generate web/data/
# local end-to-end (function chunk onward): `netlify dev`  (needs the Netlify CLI + ANTHROPIC_* auth)
```

Regenerate `web/data/` after any graph node/edge mutation (it's a snapshot).
Netlify regenerates it on every deploy via the `command` in `netlify.toml`.
