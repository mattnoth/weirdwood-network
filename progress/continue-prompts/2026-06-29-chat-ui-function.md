# SESSION 173 — Weirwood chat-UI alpha · FUNCTION chunk (`chat.ts`)

> **This is the 3rd of ~4 build chunks** for the deployable Bloodraven loremaster chat
> (S168 scoped → S169 design review → S170 publishing settled → S171 Foundation → **S172 built the
> retrieval-core** `web/src/lib/`, 21 Deno tests green). Stamp your worklog entry `### Session 173`
> (meta track, `worklog.md`).
> **Recommended model:** Sonnet 4.6 — writing `chat.ts` is mechanical TS (SDK tool-loop + streaming +
> the persona prompt). NOTE: the ONLY way to truly prove this chunk is a local `netlify dev` run,
> which calls the real Claude API and **spends real $** — confirm with Matt before running it
> (no-extraction-without-asking spirit). Build + static-validate first; gate the live smoke on Matt.
> **Context discipline:** this is the function only. The front-end (chat page, receipts panel,
> static Tywin render) + deploy are the NEXT session. Don't bleed forward.

## What's already done (don't redo)
- **Retrieval-core (S172):** `web/src/lib/` — `resolve` / `walkChain` / `neighbors` / `readNode`,
  pure over the in-memory bundle. Import the bound set:
  `import { createTools, loadGraphData } from "../../src/lib/mod.ts";` then
  `const tools = createTools(await loadGraphData());`. Tools return receipts-shaped typed-edge JSON.
  Run `cd web && deno task test` to see them green.
- **Foundation (S171):** `netlify.toml` (Edge runtime; `/api/chat` → `chat`), `web/data/` bundle,
  theme, landing placeholder.
- **Decisions LOCKED (design §0 + §9 + the edge-functions README) — do NOT reopen:** runtime =
  Netlify Edge (Deno/TS); model = **`claude-opus-4-8`** in prod, swappable via ONE config constant
  (`claude-sonnet-4-6` = cheaper fallback); retrieval = Option A (tool-use agent); scope =
  curated-MVP first (graph quotes only; live search deferred).

## STEP 0 — read first
- **`web/netlify/edge-functions/README.md`** ← THE function-chunk spec (runtime, auth, model, tool
  loop, cite-gate, cost guard, failure UX). START HERE — it's near-complete; this prompt just frames it.
- **`web/src/lib/README.md`** ← the tool API you'll wire as Claude tools.
- **`working/chat-ui/alpha-design.md`** §3 (Option A tool loop), §4 (model/auth), §8 (build plan),
  §9 (open questions + failure-mode UX).
- **`working/chat-ui/bloodraven-persona-notes.md`** ← bake into the system prompt verbatim (golden
  lines + anti-patterns). `working/demo-asoiaf-loremaster.md` ← the richness bar to match.
- **claude-api skill** ← SDK specifics (streaming, tool-use, prompt caching, `toolRunner`).

## Your job (the Edge function only) — `web/netlify/edge-functions/chat.ts`
1. **Tool loop:** expose `resolve` / `walk_chain` / `neighbors` / `read_node` to Claude (SDK
   `toolRunner` with `betaZodTool`, OR a manual `messages.stream()` loop for per-token control +
   the separate receipts channel). Cap tool iterations + `max_tokens`.
2. **Bloodraven system prompt:** persona notes verbatim; hand the model FULL beat-level grounding
   (each node's quotes + the typed chain) so it narrates richly — the S171 smoke under-delivered
   only because grounding was compressed. Stable prefix (persona + tool defs) first for caching.
3. **Streaming:** SSE back to the browser. Function holds `ANTHROPIC_API_KEY` server-side (browser
   never sees it). Local dev: leave key unset → runs on Matt's OAuth profile (key-present is the
   only dev/prod diff).
4. **Receipts channel:** emit the typed-edge JSON the tools return on a channel SEPARATE from the
   prose (the panel renders from it, not from parsing narration).
5. **Cite-verification gate:** before presenting, verify each emitted `chapter:line` cite exists
   (via `read_node`) — never show a quote at a fake cite. Keep "quotable book lines" separate from
   "context" in the prompt.
6. **Cost guard:** GLOBAL daily spend ceiling in durable state (Netlify Blobs/KV) + per-request
   `max_tokens` + iteration bounds. (Per-IP is bypassable; the global ceiling is load-bearing.)
7. **Failure-mode UX:** explicit states for no-grounding / loop-bound-hit / API-error / timeout /
   cost-cap-tripped (design §9).

**Proving test (design §0):** local `netlify dev` answers **"who killed Tywin?"** at demo richness,
streaming, with a populated receipts channel — **run only with Matt's go-ahead** (real API spend).
Static-validate everything you can without spending: `deno check`, tool-loop unit/dry tests with a
stubbed client, the cite-gate logic.

**DEFER to the front-end chunk:** the chat page, the receipts panel render, the static Tywin
exchange render. **DEFER (fast-follow):** live `search_chapters` / `read_passage` + their telemetry.

## End-of-chunk
Flip the edge-functions README + `web/README.md` status table + design §0 (function-chunk rows),
write the **front-end-chunk** continue prompt (chat page + receipts panel + static Tywin render +
deploy), and log `### Session 173`.

## DO NOT
build the front-end or deploy this chunk · run live API calls without Matt's go-ahead · shell out to
Python from the function · re-fetch wiki · mint graph edges/nodes · reopen the locked
runtime/model/scope decisions · auto-run `/endsession`.
