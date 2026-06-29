# Edge function (`web/netlify/edge-functions/`) — BUILT (function chunk, S173)

`chat.ts` — the only backend. Browser POSTs to `/api/chat` (mapped in `netlify.toml`); this function
holds `ANTHROPIC_API_KEY` server-side, runs a **Claude tool-use loop** over the `web/src/lib/`
retrieval tools, and **streams** the reply back as SSE. The browser never sees the key.

## Status (S173)

| Component                                                           | Status               | Where                                         |
| ------------------------------------------------------------------- | -------------------- | --------------------------------------------- |
| Tool loop + cite-gate + cost/grounding (SDK-free, testable)         | ✅ done              | `agent.ts`                                    |
| Netlify handler: SDK client, SSE response, spend cap, request parse | ✅ done              | `chat.ts`                                     |
| Stubbed-client loop tests (real bundle, no API spend)               | ✅ 6 green           | `agent_test.ts` (`deno task test` → 27 total) |
| `deno check` of `chat.ts` (SDK + Netlify types)                     | ✅ clean             | `deno task check:fn`                          |
| Live `netlify dev` "who killed Tywin?" proof                        | ⏳ **gated on Matt** | spends real API $ — see below                 |

**Split:** `agent.ts` is the pure half — the Bloodraven prompt, the four tool defs, the streaming
tool-loop, the cite gate, the cost estimate — with **no SDK import**, so `deno test --allow-read`
drives it with a stubbed model offline. `chat.ts` is the thin Netlify shell: the real Anthropic
client, the SSE `Response`, request parsing, and the durable spend cap. The `RunTurn` seam is what
the stub swaps for the SDK.

**Model:** `claude-opus-4-8`, swappable via the one `MODEL` constant in `chat.ts`
(`claude-sonnet-4-6` = cheaper fallback). Adaptive thinking on, streaming. SDK pinned
`npm:@anthropic-ai/sdk@^0.106.0`.

## SSE contract (what the front-end chunk renders)

`POST /api/chat` with `{ messages: [{role:"user"|"assistant", content:string|blocks}, …] }` (must
end on a `user` turn). Response is `text/event-stream`; events:

| `event:`     | `data`                                                                   | Render as                                                                                                   |
| ------------ | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| `token`      | `{text}`                                                                 | append to the streaming prose bubble                                                                        |
| `receipt`    | `{tool, input, result}`                                                  | a typed-edge receipt card (panel renders from `result`, **not** by parsing prose)                           |
| `cite-check` | `{unverified:[], validCount}`                                            | dev/QA signal; warn if `unverified` non-empty                                                               |
| `status`     | `{state}`                                                                | failure/empty states: `no-grounding`, `loop-bound-hit`, `unverified-cites`, `api-error`, `cost-cap-tripped` |
| `error`      | `{message}`                                                              | a user-safe error line                                                                                      |
| `done`       | `{ok, stopState, toolCalls, grounding, unverifiedCites, usage, costUsd}` | end of turn; close the stream                                                                               |

The receipts channel is **separate from the prose** by construction — receipts are emitted from the
tool _returns_, never scraped from narration (design §3).

## Run / validate

```bash
cd web
deno task test       # 27 green (21 lib + 6 agent loop) — offline, no API spend
deno task check:fn   # type-check chat.ts against the SDK + Netlify edge types
# LIVE proof (real API $ — run only with Matt's go-ahead):
#   netlify dev   then POST {"messages":[{"role":"user","content":"who killed Tywin?"}]} to /api/chat
```

## Build notes (from the S171 spike + claude-api skill)

- **Runtime:** Netlify Edge Function (Deno). Native streaming; 40 s response-header window; the 50
  ms CPU limit excludes time spent waiting on the Claude API, so a multi-tool turn fits. Import the
  SDK via `npm:@anthropic-ai/sdk`.
- **Auth (design §4):** `new Anthropic()` resolves `ANTHROPIC_API_KEY` → `ANTHROPIC_AUTH_TOKEN` → an
  `ant auth login` OAuth profile. **Deployed:** set `ANTHROPIC_API_KEY` in Netlify env. **Local:**
  leave it unset and run on Matt's Claude subscription (the OAuth profile) — identical code,
  key-present is the only dev/prod diff.
- **Model:** `claude-opus-4-8` (S171 decision; swappable via ONE config constant —
  `claude-sonnet-4-6` is the cheaper fallback). Adaptive thinking on, streaming.
- **Tool loop:** `client.beta.messages.toolRunner({...})` with `betaZodTool`, OR a manual
  `client.messages.stream()` loop for per-token control + the separate typed-edge receipts channel.
  Cap tool iterations + `max_tokens`.
- **Prompt:** Bloodraven system prompt — bake in `working/chat-ui/bloodraven-persona-notes.md`
  verbatim (golden lines + anti-patterns). Hand the model FULL beat-level grounding (each node's
  quotes + the typed chain) so it narrates the chain richly — the S171 smoke-test under-delivered
  only because its grounding was compressed. Put the stable prefix (persona + tool defs) first for
  prompt caching.
- **Cite-verification gate:** before presenting, verify each emitted `chapter:line` cite exists (via
  `read_node`/`read_passage`) — never show a quote at a fake cite. Keep "quotable book lines"
  separate from "context" in the prompt so the model doesn't quote grounding prose as a book line (a
  slip seen in the smoke-test).
- **Cost guard:** a GLOBAL daily spend ceiling in durable state (Netlify Blobs/KV) + per-request
  `max_tokens` + iteration bounds + an Anthropic-side billing alert. (Per-IP counters are bypassable
  — the global ceiling is the load-bearing control.)
- **Live-quote telemetry (design §8b):** instrument `search_chapters`/`read_passage` to log every
  live quote fetch from day one (harvest-style pointer) — cheap now, expensive to retrofit.
  (Deferred with live search to the fast-follow.)
- **Failure-mode UX:** explicit states for no-grounding / loop-bound-hit / API-error / timeout /
  cost-cap-tripped (design §9).
