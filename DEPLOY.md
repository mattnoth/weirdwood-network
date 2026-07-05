# Deploying the chat-UI (Weirwood Network)

How the live site at **https://weirwood-network.netlify.app** ships. Read this
before any deploy — several steps are non-obvious and `git push` alone does nothing.

- **Netlify site:** `weirwood-network` (siteId `1479d1f0-8152-430f-9ac5-4ba28e4330b6`)
- **Linked from:** repo root (`.netlify/state.json`) — run deploy commands from `/Users/mnoth/source/asoiaf-chat`, NOT from `web/`.
- **Source of truth:** root `netlify.toml` (publish `web/public`, edge functions `web/netlify/edge-functions`).

## ⚠️ Gotcha #1 — there is NO git continuous deployment

The site is **not** linked to the GitHub repo (`repo_url` is unset). Pushing to
`main` commits code to GitHub but **ships nothing**. Every production release is a
manual CLI deploy. Commit + push for history, then deploy separately.

## Deploy (the whole procedure)

```bash
# from repo ROOT (not web/):
git add -A && git commit -m "…" && git push origin main   # history only — does NOT deploy
npx netlify deploy --prod --build                          # THIS is what goes live
```

- `--build` runs the `netlify.toml` `[build] command` — the three `graph/query/build/`
  builders (`build_chat_bundle.py` + `build_search_index.py` + `build_theme_index.py`,
  S191) — regenerating **all five `web/data/` bundle files** (~12 MB, gitignored:
  alias-map / nodes / edges / manifest + search-index + theme-index) from the live
  `graph/`. The bundle is compiled into the edge function at build time (Deno edge =
  no fs at runtime). Skip `--build` and you ship a stale or missing bundle. Regenerate
  after ANY graph node/edge mutation.
- Endpoints: `/api/chat` (`chat.ts`, holds the API key, streams SSE) and `/api/node` (`node.ts`, keyless read).

### Verify after deploy
```bash
curl -sN -X POST https://weirwood-network.netlify.app/api/chat \
  -H 'content-type: application/json' \
  -d '{"messages":[{"role":"user","content":"Who is Hodor, in one sentence?"}],"persona":"loremaster"}' \
  | grep -A1 "^event: done"
# then read the newest log blob (see below) and confirm `model` is what you expect.
```
One verification turn costs a few cents (Opus). Worth it to prove model + logging are live.

## ⚠️ Gotcha #2 — the model is an ENV VAR, not (just) the code constant

`chat.ts` defaults `MODEL` to `claude-opus-4-8`, but production is governed by the
`WEIRWOOD_MODEL` env var, which **overrides** the code default. Local dev sets it to
Sonnet via `web/scripts/dev.ts`. To change the live model:

```bash
npx netlify env:set WEIRWOOD_MODEL claude-opus-4-8 --context production
npx netlify deploy --prod --build      # env changes need a REDEPLOY to take effect
```

Check current values: `npx netlify env:list --context production`.
Production env holds `ANTHROPIC_API_KEY` (Functions scope) + `WEIRWOOD_MODEL`.

## Cost monitoring & usage logs

Costs and usage ARE logged — per turn and per day. Where to look:

- **Per-turn records** — Netlify Blobs store `weirwood-chat`, key `log/YYYY-MM-DD/<uuid>`.
  Each holds `question`, `prose`, replayable `toolTrace`, `usage`, **`costUsd`**,
  `stopState`, `model`, `persona`. Every toolTrace entry carries `{tool, input}` plus
  (S191) an `outcome` slice for EVERY tool — matchType hit/miss, headline slug, result
  count, and for search_quotes/list_nodes/theme the first 10 returned slugs — so a log
  review shows what ran AND what came back without re-running anything. Cost-cap trips
  and api-errors are logged too (as `stopState` `cost-cap-tripped` / `api-error`,
  zero usage).
- **Daily spend counter** — same store, key `spend-YYYY-MM-DD`. This drives the cap.
- **Console mirror** — every turn also emits a `[turn] … cost=$…` line to the
  Netlify **Edge Function** logs (dashboard → Logs → Edge functions).
- **Read the logs locally:**
  ```bash
  NETLIFY_SITE_ID=1479d1f0-8152-430f-9ac5-4ba28e4330b6 NETLIFY_AUTH_TOKEN=<personal-access-token> \
    deno run -A --node-modules-dir=auto web/scripts/read-logs.ts [YYYY-MM-DD]
  ```
  `web/scripts/sweep-logs.ts` does a 30-day retention delete (dry-run unless `--apply`).
- **Quick spend check:** `npx netlify blobs:get weirwood-chat spend-YYYY-MM-DD`
- **Cap:** `DAILY_SPEND_CAP_USD` in `chat.ts` (currently **$50**). A pre-turn check
  refuses turns once the day's spend hits it. It's the load-bearing cost control on a
  public URL — raise/lower it deliberately, especially on Opus (5×/25× Sonnet pricing).

## ⚠️ Gotcha #3 — log & spend keys are partitioned by UTC date

`log/YYYY-MM-DD/…` and `spend-YYYY-MM-DD` use **UTC**, not local time. Past ~17:00
Pacific the "today" partition is already tomorrow's date — look under the UTC date
when a fresh turn seems missing.

## See also
- `web/README.md` — build/run details, the data-bundle schema, architecture.
- `web/netlify/edge-functions/chat.ts` — the backend (config constants at the top).
