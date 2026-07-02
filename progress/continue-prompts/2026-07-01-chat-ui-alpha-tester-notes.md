# SESSION 184 — Chat-UI alpha: triage & apply alpha-tester notes

> **This is Session 184.** Stamp your worklog entry `### Session 184` at endsession.

> **Track:** meta (chat-UI). **Recommended model:** Sonnet 4.6 — front-end/glue + light graph-query work.
> The alpha is LIVE and Matt has collected feedback from alpha testers. This session triages
> those notes into fixes and lands the quick wins.

## State — the alpha is DEPLOYED and working

Live: **https://weirwood-network.netlify.app** (deployed S183). Stack: static front-end + Netlify
Edge Functions (Deno/TS) running a Claude tool-loop on **Sonnet 4.6**; the ~8.7 MB curated-graph
bundle is compiled into the edge function via JSON imports (Netlify Edge has no filesystem — do
NOT reintroduce `Deno.readTextFile`); `ANTHROPIC_API_KEY` + `WEIRWOOD_MODEL` are Netlify env vars.
36/36 deno tests green. `netlify.toml` wired; `netlify` CLI installed + linked to site `weirwood-network`.

## Task — triage Matt's alpha-tester notes, then fix

**Matt will paste the tester notes at session start.** Do NOT assume their content. Steps:

1. **Read the notes Matt provides.** Bucket each item: **(a) bug** (broken behavior), **(b) UX/visual**
   (layout, wording, receipts, family-tree render), **(c) content/answer-quality** (persona, grounding,
   wrong/thin answers → graph-data or prompt issue), **(d) graph gap** (missing node/edge/alias — may
   route to a graph-mutation track, NOT this session). Show Matt the buckets + a recommended fix order
   before editing.
2. **Fix the quick wins** (front-end `web/public/{app.js,app.css,index.html}`, prompt tweaks in
   `web/netlify/edge-functions/lib/agent.ts`, retrieval tweaks in `web/src/lib/`). Keep `deno task test`
   green; add tests for any logic change.
3. **Verify locally** — `deno task test`, and for anything observable, `netlify deploy --build` (DRAFT,
   no `--prod`) → hit the draft URL to confirm before promoting. `/api/node` is a keyless smoke.
4. **Deploy** — once Matt approves, `netlify deploy --build --prod`. Re-smoke the live URL (streaming,
   receipts, family tree to book era, `/api/node`, no key leak).
5. **Stage graph-data gaps** — anything needing node/edge/alias mutation goes to a NOTE for a separate
   graph track (the graph is frozen for the chat-UI track); don't run graph-mutation scripts here.

## Key files
`web/public/{index.html,app.js,app.css,theme/tokens.css}` · `web/netlify/edge-functions/{chat.ts,lib/agent.ts,node.ts}` ·
`web/src/lib/*.ts` (retrieval core + tests) · `scripts/build-chat-export.py` (bundle) · `netlify.toml`.

## Deploy mechanics (from S183 — proven)
- Draft: `netlify deploy --build` → unique `*--weirwood-network.netlify.app` URL. Prod: add `--prod`.
- Env vars already set (production context): `ANTHROPIC_API_KEY` (secret) + `WEIRWOOD_MODEL=claude-sonnet-4-6`.
- CLI deploys from the WORKING TREE — commit before any future git auto-deploy.

## Open questions for Matt
- Any tester note that's really a graph-data gap (missing character/edge) — fix now or defer to a graph track?
- Custom GoDaddy domain yet, or keep `*.netlify.app`?

## DO NOT
- Reintroduce filesystem reads in the edge functions (`Deno.readTextFile` → 502; the bundle is inlined via JSON imports).
- Reopen publish/copyright (settled). Commit `ANTHROPIC_API_KEY`/`web/.env` (Netlify env only).
- Run graph-mutation scripts (chat-UI track; graph is frozen here).
- Run `/endsession` without Matt's explicit permission.

## Deferred (separate track, NOT this session unless a tester note forces it)
**Fuzzy-resolve robustness** (S178/S182): `"Aegon the Conqueror Targaryen"` scatters; `"targaryen dynasty"`
3-way-ties. Resolver/alias-layer fix needing out-of-sample validation across the 12k-alias map OR a
graph-data alias mutation — its own focused track.
