# SESSION 183 — Publish the chat-UI alpha live on Netlify

> **This is Session 183.** Stamp your worklog entry `### Session 183` at endsession.

> **Track:** meta (chat-UI deploy). **Recommended model:** Sonnet 4.6 — ops/deploy + a little glue code.
> This is Matt's job-portfolio demo going LIVE. The whole build is done and tested; this session is
> about getting it deployed, keyed, and smoke-tested on a real Netlify URL — plus a README refresh.

## Publishing is SETTLED — do not re-litigate

Per memory (`project_publish_settled`, `project_real_goal_graph_for_agents`): the repo stays **PRIVATE**
and deploys to **Netlify from private**; graph + front end + book text co-locate under `web/`.
Copyright/publish is CLOSED — do NOT raise it as a concern. Model in production = **Sonnet 4.6**
(`WEIRWOOD_MODEL` / the function's MODEL env override; the API key lives server-side in the Edge
function, the browser never sees it).

## State — the build is DONE, only deploy remains

The alpha is fully built and green (S171–S182): retrieval-core + `/api/chat` + `/api/node` Edge
functions, front-end (chat + typed-edge receipts + family-tree render with the S182 deep main-line
spine), 36/36 deno tests. `netlify.toml` is already wired:
- `publish = "web/public"`, `edge_functions = "web/netlify/edge-functions"`
- build command regenerates the 8.8 MB `web/data/` bundle via `scripts/build-chat-export.py` (python3
  is in Netlify's build image) and copies the featured landing JSON into `web/public/data/`
- routes: `/api/chat` → `chat`, `/api/node` → `node`

## Task — deploy + verify (steps)

1. **Confirm remote is current.** `git status` clean, `git log origin/main -1` == local `main`. (S182
   endsession pushed everything; verify, don't assume.)
2. **Pre-flight the build command locally.** Run the exact `netlify.toml` `command` from repo root and
   confirm it exits 0 and produces `web/data/` + `web/public/data/featured-tywin.json`.
   **KNOWN STALE-RISK:** S175 removed the Tywin featured-landing placeholder, but the build command
   still `cp`s `featured-tywin.json`. Verify what the landing actually loads now — if the featured
   exchange is gone, fix the build command (and any `app.js` fetch of `/data/featured-tywin.json`) so
   deploy doesn't fail on a missing file or ship a dead landing. This is the single most likely deploy
   breakage — check it FIRST.
3. **Connect + deploy.** Either `netlify` CLI (`netlify init` / `netlify deploy --build --prod`) or the
   Netlify web UI connected to the private GitHub repo. Ask Matt which he prefers if it needs his
   account/login — this step needs his Netlify auth, so it may be a "Matt runs it, you guide" step.
4. **Set the server-side secret.** `ANTHROPIC_API_KEY` as a Netlify environment variable (NOT committed;
   the local `web/.env` key does not travel). Confirm `WEIRWOOD_MODEL`/MODEL override resolves to
   `claude-sonnet-4-6` in prod (check `agent.ts`/`chat.ts` env handling).
5. **Smoke-test the live URL.** Load the page, ask one causal query (e.g. "Why did Robert's Rebellion
   start?") and one lineage query ("Targaryen family tree from Aegon the Conqueror down to Daenerys")
   — confirm streaming works, receipts/chain render, the family tree reaches the book era (the S182
   spine), `/api/node` dossiers open, and no key leaks to the browser (check network tab).
6. **Update the root `README.md`** (Matt explicitly asked). It currently describes ONLY the graph
   project — add the deployed chat-UI: what it is (Bloodraven loremaster over the graph), the live URL,
   the `web/` stack (Netlify Edge Functions / Deno / Sonnet 4.6), and how to run it locally
   (`web/scripts/dev.ts` + `web/.env`). `web/README.md` is the existence-truth doc — keep it in sync.

## Key files

`netlify.toml` · `web/netlify/edge-functions/{chat.ts,node.ts,agent.ts}` · `web/scripts/dev.ts` ·
`web/.env` (local key, gitignored) · `scripts/build-chat-export.py` (bundle build) ·
`web/public/{index.html,app.js,app.css}` · `README.md` (root — needs the update) · `web/README.md`.

## Open questions for Matt
- Which deploy path — Netlify CLI from your machine, or connect the private repo in the Netlify UI?
  (Needs your Netlify auth either way.)
- Custom domain, or is the default `*.netlify.app` URL fine for the portfolio demo?

## DO NOT
- Re-open the publish/copyright decision (settled — see above).
- Commit `ANTHROPIC_API_KEY` or `web/.env` anywhere. The key is a Netlify env var only.
- Run any graph-mutation script — this is deploy/ops, the graph is frozen for this track.
- Run `/endsession` without Matt's explicit permission.

## Deferred (NOT this session — separate track)
Fuzzy-resolve robustness (surfaced S178/S182): `"Aegon the Conqueror Targaryen"` scatters and
`"targaryen dynasty"` 3-way-ties. Both are resolver/alias-layer fixes needing out-of-sample validation
across the 12k-alias map OR a graph-data alias mutation — its own focused track, not deploy work.
