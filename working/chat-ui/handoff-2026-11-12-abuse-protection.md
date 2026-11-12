# Handoff — chat-UI API-credit spike + abuse protection (2026-11-12)

Self-contained resume prompt for a local session. (Kept in `working/chat-ui/`, not
`progress/continue-prompts/`, per the one-live-prompt hygiene policy.)

## Situation
- Matt's Anthropic API credit hit its limit. Usage spike on **Nov 9 2026** from the public chat-UI
  (`https://weirwood-network.netlify.app`). Who used it is currently **unknowable from the app**.
- Why: `chat.ts` `TurnLog` records question/prose/toolTrace/usage/cost/model/timestamp — **no IP,
  user-agent, or session id**. No login/access gate. Console log line has no IP either.
- The daily cap (`DAILY_SPEND_CAP_USD = 50`, Netlify Blobs) is **best-effort and fails OPEN**:
  `readDailySpend()` returns 0 on any Blobs error/missing store → cap silently off. $50/day on
  Opus 4.8 ($5/$25 per MTok) is enough to drain credit over several days.

## Already done (branch `claude/gifted-brown-07ezfe`, pushed; NOT merged to main, NOT deployed)
1. `web/netlify/edge-functions/chat.ts`: `MODEL` default `claude-opus-4-8` → `claude-sonnet-5-5`
   ($2/$10 per MTok, ~60% cheaper). Code is compatible (adaptive thinking; no tool_choice/temperature/prefill).
2. `web/netlify/edge-functions/lib/agent.ts` `PRICING`: added `claude-opus-5-5` (4/20),
   `claude-sonnet-5-5` (2/10), `claude-sonnet-5` (2/10), `claude-haiku-5-5` (0.1/0.5). Without this,
   unknown models fall back to Opus rates and the cap over-counts ~2.5x.
3. `working/todos.md` → Small Fixes: HIGH item for the protections below.
- Deno not installed in the cloud container → **tests not run**. Run `cd web && deno task test` (27 expected green) and `deno task check:fn`.

## Deploy facts (DEPLOY.md)
- Site has **no git CD** (`repo_url` unset). Push ≠ deploy. Deploy from repo ROOT: `npx netlify deploy --prod --build`.
- Prod model is governed by env var `WEIRWOOD_MODEL` (overrides code default). Env changes need a redeploy.
- siteId `1479d1f0-8152-430f-9ac5-4ba28e4330b6`. Logs: `web/scripts/read-logs.ts [YYYY-MM-DD]` (needs `NETLIFY_SITE_ID` + `NETLIFY_AUTH_TOKEN` PAT). Logs retained 30 days (`sweep-logs.ts`).

## Matt's local steps (do first)
1. `git fetch origin claude/gifted-brown-07ezfe && git checkout claude/gifted-brown-07ezfe`
2. `npx netlify env:list --context production` (see current `WEIRWOOD_MODEL`)
3. `npx netlify env:set WEIRWOOD_MODEL claude-sonnet-5-5 --context production`
4. `npx netlify deploy --prod --build`; smoke-test "who killed Tywin?" (check `done.costUsd`).
5. Read Nov 9 logs: `read-logs.ts 2026-11-09` — look for bot-like/repeated/scripted questions, turn volume, cost.
6. Anthropic Console: set monthly spend limit; Usage by day/key to confirm Nov 9; rotate `ANTHROPIC_API_KEY` if leak suspected.
7. Netlify dashboard → Logs → Edge Functions for request IPs around Nov 9.

## TODO: build the protections (not yet written; no edits made)
Design (settled; edit `chat.ts`, small tests in `agent_test.ts` if logic is pure):
1. **IP hash in TurnLog**: new `ipHash` field. IP from `context.ip` (handler currently names it `_context`), fallback header `x-nf-client-connection-ip`. SHA-256 of `salt + ip` via `crypto.subtle`, keep 16 hex chars; salt from env `WEIRWOOD_IP_SALT` (set it in Netlify). Add to the console `[turn]` line and `failedTurn(...)`. `mine-resolve-misses.ts` TurnLog type mirror: add optional field.
2. **Per-IP rate limit** in Blobs, one key per hash per day: `rl/<YYYY-MM-DD>/<ipHash>` → `{n, t:[recent epoch ms]}`. Limits ~5 per rolling minute, ~25 per day (env-tunable). Best-effort (read-modify-write races are acceptable here). Rate-limited requests: console.log only (do NOT write a log blob — abusers would spam storage); respond with the existing SSE `status` `cost-cap-tripped` so the UI shows its "answered enough for today" message (front-end `web/public/app.js:1386` only knows existing states; or add a `rate-limited` entry there). Note `sweep-logs.ts` only deletes `log/` — extend it to `rl/` or accept the tiny growth.
3. **Fail-closed cap**: `readDailySpend()` → `number | null` (null = unreadable/no store). "Strict mode" = `ANTHROPIC_API_KEY` is set (deployed); local dev runs keyless on OAuth and must keep working. In strict mode, null → refuse the turn. Same strictness if `getStore()` returns null.
4. **Lower cap**: `DAILY_SPEND_CAP_USD` from 50 → default **10** (Sonnet), make it env-overridable (`WEIRWOOD_DAILY_CAP_USD`).
5. Optional: shared passcode/invite gate if Matt wants invite-only.
- After building: `deno task test`, `deno task check:fn`, then deploy (steps 3–4 above), update `worklog.md` (new S-number; graph + shared track numbering) and tick the todos.md item. Cost of the protections themselves: ~zero (one extra Blobs read+write per request).

## Don'ts
- Don't read/act on the root `scratch` file. Don't re-fetch the wiki. Don't merge/push to `main` without Matt's say.
