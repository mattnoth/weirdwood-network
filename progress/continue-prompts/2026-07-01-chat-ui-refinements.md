# SESSION 178 — Chat-UI alpha: REFINEMENTS pass · graph/meta track

> **This is Session 178.** Stamp your worklog entry `### Session 178` at endsession (graph/meta track → `worklog.md`).
>
> Fresh-context handoff after S177 shipped the chain-display rebuild + the unified quote system. THIS session = a **refinements pass** on rough edges Matt surfaced, PLUS **Matt's own design refinements** (he'll bring them at session start — ASK him first before diving into the list below).
>
> **Recommended model:** Sonnet 4.6 — frontend/CSS + small backend (resolver/alias + maybe a genealogy walk); no heavy reasoning. (Deploy default stays Opus; local dev uses Sonnet.)

## RUN IT — local live (Deno; key in `web/.env`; NEVER print the key)
- **Preview MCP (easiest):** `preview_start` config **`weirwood-live`** (autoPort, `WEIRWOOD_MODEL=claude-sonnet-4-6`, runs `web/scripts/dev.ts`).
- **Manual LIVE:** `cd web && WEIRWOOD_MODEL=claude-sonnet-4-6 ~/.deno/bin/deno run -A --node-modules-dir=auto --env-file=.env scripts/dev.ts` → http://127.0.0.1:8766/
- **Reliable turn test:** `curl -sN -X POST :8766/api/chat -H 'content-type: application/json' -d '{"messages":[{"role":"user","content":"..."}]}'`. curl-with-a-single-message reliably walks; the browser carries history that biases toward answering from memory (reload to clear).
- **After editing `agent.ts` (the prompt/tools) you MUST RESTART the server** — Deno does not hot-reload the imported module. `app.js`/`app.css`/`index.html` refresh on browser reload (dev serves `no-store`); bump `?v=` in `index.html` on CSS/JS edits.
- **Before every reload:** `deno check --node-modules-dir=auto <changed .ts>` and `node --check public/app.js`. (S177 lesson: a prior Sonnet attempt broke Deno by writing curly/smart quotes into JS/TS — use ASCII delimiters only.)
- **Tests:** `cd web && ~/.deno/bin/deno test -A --node-modules-dir=auto src/lib/` (22 pass).

## DONE in S177 — do NOT redo (all committed)
- Chain = one deduped vertical spine (band retired) + `·N` degree badges + "show preconditions (+N)" progressive-disclosure toggle (fed by `walkChain`'s `enables[]`, one round-trip; `full` retired).
- Hover-peek (node → lights its edges) + click-dossier on every node via `/api/node` (`web/netlify/edge-functions/node.ts`, wired in `dev.ts` + `netlify.toml`).
- Unified `bookQuote()` renderer everywhere (answer prose + chain edges + preconditions + dossier); `prettyCite()` → "ASOS Arya 11"; `cleanQuote()` strips paths/wiki/backticks/internal `book-cite overlay` tails; Bloodraven emits `[[q|text|speaker|source]]` markers → streaming `renderProse` → styled pull-quotes; cite-gate validates in-prose sources.
- Persona: no "chain"/"link" in prose, no counting-formula opener, NO markdown (bold/headers/lists — hard rule; a cold subagent picked "drop the bold" over "render it").

## THE REFINEMENTS (surfaced by a live "Targaryen family tree from Aegon" query)
Ask Matt which to prioritize; he ALSO has his own design refinements to fold in.

1. **Genealogy / family-tree queries hit the loop bound.** "Show me the Targaryen family tree from Aegon the Conqueror" → the model fanned out through `neighbors` (HOLDS_TITLE, SUCCEEDS, BORN_AT, DIED_AT…), exhausted `MAX_TOOL_ITERATIONS` (agent.ts, =6), and returned `loop-bound-hit` with a thin/empty answer. There is **no genealogy traversal mode** — a dynasty/lineage question is a distinct shape from the causal spine. Options: (a) a dedicated `familyTree(slug)` / lineage walk over parentage + SUCCEEDS edges (check what genealogy edge types exist in the bundle — likely PARENT_OF / CHILD_OF / MARRIED_TO / SUCCEEDS), returned as its own receipt/render; (b) raise/branch the iteration bound for fan-out queries; (c) at minimum, detect the shape and steer the model. Investigate the actual edge vocabulary first (`web/data/edges.json`).
2. **Fuzzy resolve on marquee names.** "Aegon the Conqueror" resolved **fuzzy** → aegon-i/ii/iii (not a confident exact hit on `aegon-i-targaryen`); "Targaryen dynasty" same. The alias map (`web/data/alias-map.json`, built by `scripts/build-chat-export.py` from node `aliases:`) is missing "Aegon the Conqueror" → aegon-i (and dynasty→house). Fix at the DATA layer (add aliases → rebuild bundle) and/or tighten `resolve()` ranking so a strong epithet beats a fuzzy name-prefix scatter. Remember: node `aliases:` must be natural SPACED phrases, not kebab slugs (`project_node_alias_spaced_phrases`).
3. **Loop-bound UX.** On `loop-bound-hit` the answer area looked EMPTY above the status line. Confirm the model still emits a partial answer in that path (agent.ts `runAgent` — the loop-bound branch), and that an empty one reads gracefully (app.js status handling).
4. **(Bigger) a real family-tree view.** Genealogy wants its own visual (a tree, not the causal spine). Scope this as its own step if Matt wants it — likely a new receipt type + render.

## KEY FILES
- `web/public/` — `index.html`, `app.css`, `app.js` (chain UI, dossier, `bookQuote`/`renderProse`/`prettyCite`/`cleanQuote`).
- `web/src/lib/` — `graph.ts` (walkChain/neighbors), `resolve.ts`, `read-node.ts`, `types.ts`, `mod.ts`, `*_test.ts`.
- `web/netlify/edge-functions/` — `agent.ts` (SYSTEM_PROMPT + TOOL_DEFS + runAgent + MAX_TOOL_ITERATIONS), `chat.ts`, `node.ts`.
- `web/scripts/dev.ts` (local routes), `netlify.toml` (deploy routes), `scripts/build-chat-export.py` (bundle + alias-map builder).
- `working/chat-ui/alpha-design.md` — design doc.

## LOCKED — do NOT reopen
Netlify Edge (Deno/TS) · deploy model `claude-opus-4-8` · **Bloodraven DEFAULT** · curated-MVP · repo **PRIVATE → Netlify** (publishing CLOSED) · SSE contract · no mocked AI prose · **prose-first every screen** · **band retired** · **keep-detail-via-progressive-disclosure** · **unified quote display + `[[q|…]]` markers + "ASOS Chapter N" sources** · **no "chain"/"link" + no markdown in Bloodraven's prose** · key lives in `web/.env`.

## DO NOT
deploy without Matt's go-ahead · mint graph edges/nodes · run `/endsession` without permission · reopen the LOCKED list · write smart/curly quotes into JS/TS (ASCII delimiters; `deno check`/`node --check` before reload).
