---
session: 183
title: Chat-UI alpha deployed live on Netlify — the edge-runtime debugging chain
date: 2026-07-01
track: meta (chat-UI deploy)
model: Opus 4.8 (handoff recommended Sonnet 4.6)
api_spend: 2 live Sonnet 4.6 prod smoke queries (~$0.10, under the $5/day cap); no graph writes
harvest_queue: 0
commit: 9ba0d204b4
---

# Session 183 — Publishing the chat-UI alpha

## Goal

Take the fully-built, green (36/36 tests) chat-UI alpha and put it live on Netlify as
Matt's job-portfolio demo. The build was done (S171–S182); this was a deploy/ops session
with "a little glue code." It turned into a five-bug edge-runtime debugging chain.

## The approach that paid off: draft-first

The cold-subagent advice (unbiased read on CLI vs UI deploy) was decisive: **Netlify CLI,
draft-deploy-before-prod.** Every fix below was caught on a draft deploy (or a local
`netlify build`) and verified on a keyless preview URL *before* spending a prod deploy or
any API dollars. `/api/node` (the keyless dossier endpoint) turned out to be the perfect
canary — it reads the same graph bundle as the chat endpoint via `loadGraphData()` but needs
no API key, so a single `curl` against it proved (or disproved) the bundle-load path for free.

## The five deploy-breakers, in the order they surfaced

1. **Stale `featured-tywin.json` cp** (the one the handoff flagged). `netlify.toml`'s build
   command ended with `&& cp web/data/featured-tywin.json …`. S175 had deleted that featured-
   landing placeholder; nothing produces or consumes the file anymore. On deploy the `cp`
   would hit a missing source → non-zero exit → failed build. Confirmed by grepping the build
   script (no "featured") and app.js (only comments). Fixed: command is now just the python build.

2. **`npm:` specifiers don't resolve on Netlify Edge.** First draft deploy died:
   `Could not resolve "npm:@anthropic-ai/sdk@^0.106.0"` / `"npm:@netlify/blobs@^8"` —
   "npm module support in edge functions is an experimental feature." Netlify's own docs
   confirm the reliable path is **esm.sh URL imports** (Deno-native). Switched both imports in
   `chat.ts`. The 36 tests don't import `chat.ts` (they stub the client via `agent.ts`), so no
   test impact.

3. **Helper + test packaged as routes.** The bundler listed `agent`, `agent_test`, `chat`,
   `node` as functions. Netlify treats every *top-level* file in the edge-functions dir as a
   route; subdirectory files are shared code. Moved `agent.ts` + `agent_test.ts` into
   `lib/` (git mv, fixed relative-import depth, updated chat.ts's `./agent.ts` → `./lib/agent.ts`).
   `netlify build` then packaged only `chat` + `node`.

4. **Netlify Edge has NO filesystem** — the big one. Second draft deploy: landing 200 but
   `/api/node` 502'd. Edge logs were unambiguous:
   `Error: Reading or writing files with Edge Functions is not supported yet` at
   `data.ts:12 readJson → loadGraphData`. `Deno.readTextFile` is blocked outright on the edge —
   not a bundling-inclusion gap, a hard platform limit. Rewrote `loadGraphData` to **inline the
   8.7 MB bundle via JSON module imports** (`import … with { type: "json" }`), casting through
   `unknown` so tsc skips a deep structural check of the 3.8 MB literals. Empirically tsc handled
   it fine (tests still ran in ~1.4 s). Dropped the now-unused `dataDir` param + `DEFAULT_DATA_DIR`.
   Third draft deploy: `/api/node` returned 200 with real Tywin data.

5. **`node:assert` type-check broke locally** (a byproduct of debugging, not a deploy issue).
   While chasing #4 I removed the stale `node_modules`; that exposed deno 2.9's byonm mode —
   the presence of `web/package.json` makes deno resolve `node:assert` types via `@types/node`
   from node_modules, which wasn't there. (It had only ever been present as a transitive of the
   old `npm:` SDK cache.) `deno install` didn't pull it. Fix: `nodeModulesDir: "auto"` in
   `deno.json` — deno resolves node types itself. `deno task test` green with full type-check,
   36/36. This is local-toolchain only; Netlify's edge bundler doesn't run `deno test`.

## The model trap

`chat.ts:32` reads `WEIRWOOD_MODEL ?? "claude-opus-4-8"` — so prod **defaults to Opus**, not
Sonnet. The portfolio demo wants Sonnet 4.6 (and its lower cost under the daily cap). So prod
needs **two** env vars, not one: `ANTHROPIC_API_KEY` (secret) + `WEIRWOOD_MODEL=claude-sonnet-4-6`.
Confirmed live by the cost math on the smoke query: $0.0531 for 6,435 in / 2,252 out is exactly
Sonnet's $3/$15-per-M; Opus would have been ~$0.088.

## Secret handling

The key came from the gitignored `web/.env`, captured into a shell var (never a literal in any
printed command), set via `netlify env:set … --secret --context production` (the `--secret` flag
requires a non-dev context), and the command output was filtered through `grep -ivE "$KEY"` before
display, then `unset`. Verified no leak by grepping the served `index.html`, `app.js`, and both SSE
responses for `sk-ant` and the actual value — zero hits. The key lives only in the edge function's
server-side env.

## Prod smoke results

- Landing 200; `/api/node` dossiers 200 with real quotes + wiki-links.
- `/api/chat` causal query ("Why did Robert's Rebellion start?"): 5 tool calls, 24 token frames,
  cite-check `validCount:3 unverified:[]`, `done stopState:end_turn`, no errors.
- Lineage query: `family_tree` tool fired, 171 grounding hits, tree reaches the book era
  (Aegon the Conqueror → Jaehaerys → Aegon V → Aerys → Rhaegar → Daenerys — the S182 deep spine).
- No key leak (grep-verified).

## Decisions / notes for future sessions

- **CLI deploys run from the working tree, not git.** The live site is correct, but the 9-file
  diff had to be committed (done, `9ba0d204b4`) before any future git-based auto-deploy in the
  Netlify UI will reproduce it.
- Auto-deploy-on-push deferred; `netlify link` is done so it's a trivial add later.
- Custom GoDaddy domain deferred (Matt); default `*.netlify.app` for now.
- **Do not reintroduce `Deno.readTextFile` in the edge functions** — the bundle is inlined via
  JSON imports for a reason; a filesystem read 502s every request.
- Next: Matt has alpha-tester notes to triage (S184).
