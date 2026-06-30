# SESSION 176 — Chat-UI alpha: DESIGN evaluation (fresh context) · graph/meta track

> **This is Session 176.** Stamp your worklog entry `### Session 176` at endsession.
>
> Fresh-context handoff. The chat-UI alpha BUILD is code-complete (S171–S174); local LIVE
> running (Deno dev server + `web/.env` key) is DONE and committed (S175); the **Tywin
> placeholder is fully removed (S175)** — the landing now opens to a clean composer. THIS
> session = evaluate + polish the design with real live conversations, working from **Matt's
> design notes + enrichment ideas** (he has these ready to share at session start — ask for them).
>
> **Recommended model:** Sonnet 4.6 (HTML/CSS/JS polish + watching live runs — no heavy backend reasoning).

## RUN IT — local live works now (no Netlify CLI, no python-for-live)
Deno is installed at `~/.deno/bin/deno` (NOT on PATH — use the full path). The local dev
server is `web/scripts/dev.ts` — a stand-in for `netlify dev` that serves `public/` AND routes
`POST /api/chat` into the real edge function (`chat.ts`). The Anthropic key is in `web/.env`
(gitignored — NEVER print it, NEVER paste a key into chat).

- **LIVE** (real model; ~2.5¢ per Opus turn):
  ```
  cd web && WEIRWOOD_MODEL=claude-opus-4-8 ~/.deno/bin/deno run -A --node-modules-dir=auto --env-file=.env scripts/dev.ts
  ```
  (swap `WEIRWOOD_MODEL=claude-sonnet-4-6` for cheap iteration — chain/receipt rendering is identical)
- **DEMO** (no key, no cost; replays a fixture):
  ```
  cd web && WEIRWOOD_DEMO=1 ~/.deno/bin/deno run -A scripts/dev.ts
  ```
- Open **http://127.0.0.1:8766/** . Inspect/kill the server: `lsof -nP -iTCP:8766 -sTCP:LISTEN` / `pkill -f scripts/dev.ts`.
- `npm run dev` from `web/` = the python static-only preview (no backend) — fine for pure CSS/layout work.

## What the harness session set up (don't redo)
- `web/scripts/dev.ts` — LIVE + DEMO dev server (NEW).
- `web/package.json` — npm aliases for the static preview (NEW; harmless — the app itself is Deno + a Python build step).
- `web/.gitignore` — ignores `.env`, `node_modules` (NEW).
- `web/.env` — holds the Anthropic API key (gitignored). **Verified live:** Opus answered
  "What led to the Red Wedding?" for **$0.0248**, `walk_chain` returned **12 links** (rich),
  real prose + real book quotes streamed.
- `web/netlify/edge-functions/chat.ts` — MODEL is now env-overridable:
  `Deno.env.get("WEIRWOOD_MODEL") ?? "claude-opus-4-8"`. **Deploy default (Opus) UNCHANGED.**

## FINDINGS (carry forward)
- **Subscription auth does NOT work** with the SDK. chat.ts:12–14 claims local runs on Matt's
  Claude subscription with no key — that is FALSE; the public `@anthropic-ai/sdk` needs an
  explicit key/token and can't use the Claude Code OAuth. A web app always needs an API key
  (so does deploy; key now lives in `web/.env`). → small DOC FIX: correct that comment.
- **Live slug→name:** live `walk_chain` links carry only slugs; the front-end `pretty()`s them
  → "Death of joffrey baratheon". Resolve slug→proper-name (or title-case) for live labels. (Item #4.)

## THE DEMO (Matt's plan — Tywin placeholder REMOVED S175)
- The Tywin placeholder (fixture JSON + hand-written prose + landing auto-load + its build-script
  generation) is GONE (S175). The landing opens clean; `dev.ts` DEMO mode now streams an honest
  "run LIVE" notice (no fixture read, no fake prose). The DEMO scaffold is kept for the real
  recording below.
- Matt wants a **multi-turn Red Wedding conversation** as the public demo. His three questions:
  1. "What led to the Red Wedding?"
  2. "More detail on this character's motives." (follow-up — thread turn-1 history so "this character" resolves)
  3. "What were the ramifications of the red wedding?"
- Model = **record once → replay free forever** (so public visitors don't spend Matt's credits and
  the showpiece is deterministic). Build the capture: tee the LIVE SSE to disk (or a deliberate
  capture), then wire `dev.ts` DEMO to replay the recording (turn chosen by history length).
- Capture on **Opus 4.8** (deploy model, best prose). **No hand-written prose** (Matt firm).

## OPEN DESIGN ITEMS — the actual eval (resolve with Matt, live in the UI)
1. **Chain enrichment — "see the edges."** Matt: the chain is cool but could be enriched; he
   wants to literally SEE the edges/relationships more. He chose **"mock a few, let me pick."**
   Build 2–3 mockups (use the `visualize` / show_widget tool): (a) **inline edge-evidence**
   (book quote + cite shown on each link), (b) **branches/neighbors** (side-edges off the spine),
   (c) a **node-link graph view** (boxes + arrows). Let him choose, then build it into the chain.
2. **Default chain layout** — Band (full-width "wow") vs Spine (side-rail density) vs keep the
   toggle. Both built, deduped, localStorage-persisted.
3. **BUG — failed/empty turn wipes the featured chain.** `app.js` `ask()` runs `turn=freshTurn()`
   BEFORE the fetch, so a failed or empty turn blanks the showpiece. Fix: keep the last good
   chain until a *successful* new one replaces it.
4. **Live slug→name polish** — resolve slug→proper-name (or title-case) for live chain labels.
5. **Weirwood backdrop opacity** — `--weirwood-opacity: 0.06` (very faint); Matt may want
   ~0.10–0.12. One-line token in `tokens.css`.

## Read first
- `web/public/index.html` + `app.css` + `app.js` ← what you polish.
- `web/public/theme/tokens.css` ← ONE-FILE theme; keep styling token-driven (warm dark ground,
  bone text, dusty red `--c-accent #c2664c`; edge colours `--c-edge-causes/triggers/motivates/enables`).
- `working/chat-ui/alpha-design.md` §5 (persona/UI) + §6 (look/receipts).

## LOCKED — do NOT reopen
Netlify Edge (Deno/TS) · deploy model `claude-opus-4-8` · Option A tool-use · curated-MVP ·
repo PRIVATE → Netlify (publishing CLOSED) · SSE contract (render what the function emits) ·
no mocked AI prose · **a web app needs an API key — there is no subscription path** · key lives in `web/.env`.

## After design settles — GATED ship steps (Matt's go-ahead)
1. Capture the real multi-turn RW demo (above) → wire DEMO replay to it.
2. Deploy private repo → Netlify + set `ANTHROPIC_API_KEY` in Netlify env. On success, update
   memory `project_real_goal_graph_for_agents` with the live URL.

## DO NOT
deploy without Matt's go-ahead · mint graph edges/nodes · auto-run `/endsession` · reopen the LOCKED list.
