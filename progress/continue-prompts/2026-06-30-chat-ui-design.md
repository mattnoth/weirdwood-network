# SESSION 177 — Chat-UI alpha: the chain-display REBUILD (Phase 2) · graph/meta track

> **Stamp your worklog entry `### Session 177`** at endsession (graph/meta track → `worklog.md`).
>
> Fresh-context handoff after a very large S176. The chat-UI **prose layer is fixed** and the
> **About page shipped**. THIS session = rebuild the **"chain walked" display** per the
> advisory-board design (keep-the-detail-but-progressive), then add hover/click node dossiers.
>
> **Recommended model:** Sonnet 4.6 — frontend/CSS + one small backend walk change + one tiny
> endpoint. No heavy reasoning. (Deploy default stays Opus; local dev uses Sonnet for cheap iteration.)

## RUN IT — local live (Deno; key in web/.env; NEVER print the key)
Deno is at `~/.deno/bin/deno` (not on PATH). Two ways:
- **Preview MCP (easiest):** `preview_start` config **`weirwood-live`** in `.claude/launch.json`
  (autoPort, defaults `WEIRWOOD_MODEL=claude-sonnet-4-6`). It runs `web/scripts/dev.ts` on :8766.
- **Manual LIVE:** `cd web && WEIRWOOD_MODEL=claude-sonnet-4-6 ~/.deno/bin/deno run -A --node-modules-dir=auto --env-file=.env scripts/dev.ts` → http://127.0.0.1:8766/
  (swap `claude-opus-4-8` to judge real prose). Kill: `pkill -f scripts/dev.ts`.
- **Reliable test of a turn:** `curl -sN -X POST :8766/api/chat -H 'content-type: application/json' -d '{"messages":[{"role":"user","content":"What led to the Red Wedding?"}]}'`. The browser carries chat history that biases the model toward answering from memory; **curl with a single message reliably walks**.

## DONE in S176 — DO NOT REDO (all in the WORKING TREE, **uncommitted**)
- **Prose quality FIXED** (`agent.ts` SYSTEM_PROMPT): added an **"Evidence discipline"** block (setup-then-quote, one quote/beat, ≤~20 words, no standalone block-quotes, quote-must-do-a-job) + fixed the **"Ask your questions…" opener leaking** into real answers + added a **MANDATORY-walk** rule (model must call walk_chain for causal Qs). Verified by curl: in-context set-up quotes, no dumps, no opener leak.
- **Bloodraven = DEFAULT persona** (decided this session, board-backed). The flat **Loremaster (zero-personality, literal)** is a *later* toggle — **not built yet**; when built it INHERITS the same Evidence Discipline block (neutral register, not "no rules").
- **walk_chain pruned + enriched** (`web/src/lib/graph.ts`): `DEFAULT_MAX_DEPTH=2`, `MAX_LINKS_PER_DIRECTION=12`, causal-only by default; links now carry `source_name/target_name/source_type/target_type` (the slug→name fix). `types.ts` updated; `graph_test.ts` updated (8 tests pass). Verified curl: "what led to the Red Wedding" → **8 clean links** with proper names ("Robb weds Jeyne Westerling →TRIGGERS→ the conspiracy →CAUSES→ Red Wedding", downstream to Roose's wardenship + Catelyn→Stoneheart).
- **Frontend chain re-rendered to the annotated spine (Mockup A)** in `app.js`/`app.css`: node cards w/ type, hub highlight, inline edge evidence (quote+cite+tier always visible), `cleanQuote()` strips `(wiki:…)` markup, repeat-node slim, bounded scroll. ⚠️ **NOT visually verified end-to-end** (Sonnet variance kept the browser from walking; curl confirms the data shape). The Phase-2 rebuild replaces much of this anyway.
- **Bug fixed:** a failed/empty turn no longer wipes the featured chain (`lastGoodChain` persistence in `app.js`).
- **About page DONE + verified:** page opens straight to chat; the "what is this" blurb → a toggled **About view** (header **About** btn ↔ "← Chat"; `#about-back`). `body.about-open` swaps chat ⇄ about.
- **Prose-first on mobile** (CSS `order`). The full-width **"Band" chain-on-top is RETIRED** (it sat above the prose) — chain now lives in the **right rail (desktop) / below (mobile)**. The Band half of the Band/Spine toggle is gone.
- **Backdrop opacity** 0.06 → **0.11** (`tokens.css`).
- **Dev caching fixed:** `dev.ts` serveDir sends `cache-control: no-store`; `index.html` asset links carry `?v=176b`. **Bump `?v=` when you edit CSS/JS** so pre-cached browsers refresh.

## THE DESIGN SPEC — advisory-board synthesis (3 advisors converged, Matt approved)
Rebuild the chain display as:
1. **Dedup at the DATA layer** — each node appears **ONCE**; the many edges that touch it become multiple connectors; show a small **degree badge `·N`**. This kills the "Siege of Riverrun ×6" wall.
2. **Progressive disclosure (the core of "keep the detail, show it better"):** default view = the clean **CAUSES/TRIGGERS/MOTIVATES spine**; the full **ENABLES** precondition web renders **dimmed/indented behind ONE "show preconditions (+N)" toggle** — same view, no layout swap. Matt wants the rich detail KEPT (Robb's campaign, Ned's arc), just one tap away — **NOT hard-pruned**.
   - **Backend need:** the toggle must have the ENABLES data WITHOUT a 2nd model round-trip. Cleanest: have `walkChain` also return an `enables` array (ENABLES links within the bound), or return full(causal+ENABLES) tagged by `edge_type` and let the frontend split. Keep the depth bound + dedup so it stays manageable. (Today `full=true` is discouraged in the prompt because it floods — reconcile: the UI fetches the fuller set, the model still narrates the causal spine.)
3. **Vertical layered spine, NOT boxes-and-arrows** (arrows die at ~320px and on phones). Layout by topological/causal depth.
4. **Interaction:** hover a node → highlight its edges + identity/degree tip; hover an edge → quote+cite+tier; **click a node → full dossier (Mockup C)**. **Mobile (no hover) = tap-to-expand accordion rows.**
5. **Every node interactive** → add a **node-lookup endpoint**: `GET /api/node?slug=` → `readNode(slug)` (+ optionally `neighbors(slug)`) so any chain node opens its card. New edge function `web/netlify/edge-functions/node.ts` + route in `dev.ts` (+ map in `netlify.toml` for deploy, later).
6. **Prose first on every screen** (done on mobile; ensure desktop prose leads, chain in the rail).
7. **Stretch marquee:** click a causal claim in the prose → its exact edge lights up in the chain. Defer until the above is tight.

**Mockups Matt picked (S176, via show_widget):** **Mockup A** (annotated spine) for the chain; **Mockup C** (node dossier) for the click-through.

## BUILD ORDER (green-lit by Matt — run with it, no scope tweak)
1. **Dedup spine + "show preconditions (+N)" toggle** (backend returns spine+enables; frontend dedups + dims the ENABLES branches behind the toggle).
2. **Hover-peek + click-dossier on every node** (add `/api/node` endpoint; wire hover/click; mobile accordion).
3. **Stretch:** prose↔edge highlight binding.

## KEY FILES
- `web/public/index.html`, `app.css`, `app.js` — the chain UI + About view.
- `web/public/theme/tokens.css` — ONE-FILE theme (edge colours `--c-edge-causes/triggers/motivates/enables`; `--weirwood-opacity`).
- `web/src/lib/` — `graph.ts` (walkChain/neighbors), `types.ts`, `read-node.ts`, `mod.ts` (createTools), `*_test.ts`.
- `web/netlify/edge-functions/` — `agent.ts` (SYSTEM_PROMPT + TOOL_DEFS + runAgent), `chat.ts` (handler, MODEL env). Add `node.ts` here.
- `web/scripts/dev.ts` — local dev server (add the `/api/node` route here for local).
- `working/chat-ui/alpha-design.md` — design doc (§5 persona/UI, §6 look/receipts).

## LOCKED — do NOT reopen
Netlify Edge (Deno/TS) · deploy model `claude-opus-4-8` · **Bloodraven DEFAULT** · Option A tool-use ·
curated-MVP · repo **PRIVATE → Netlify** (publishing CLOSED) · SSE contract (render what the function emits) ·
no mocked AI prose · **prose-first on every screen** · **Band-on-top retired** · **keep-detail-via-progressive-disclosure (NOT hard-prune)** · a web app needs an API key — key lives in `web/.env`.

## GOTCHAS
- **Model variance:** Sonnet sometimes skipped `walk_chain` → empty chain panel. A mandate is in the prompt now; **verify the walk fires** (curl reliable; in-browser, reload to clear history which biases toward answering from memory).
- **Browser caching:** bump `?v=` in `index.html` on every CSS/JS edit.
- **Don't commit** unless Matt asks. All S176 work is uncommitted in the working tree — consider a checkpoint commit early if Matt approves.

## DO NOT
deploy without Matt's go-ahead · mint graph edges/nodes · run `/endsession` without permission · reopen the LOCKED list.
