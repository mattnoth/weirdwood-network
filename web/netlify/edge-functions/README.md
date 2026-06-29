# Edge function (`web/netlify/edge-functions/`) — TO BUILD (function chunk)

`chat.ts` — the only backend. Browser POSTs to `/api/chat` (mapped in
`netlify.toml`); this function holds `ANTHROPIC_API_KEY` server-side, runs a
**Claude tool-use loop** over the `web/src/lib/` retrieval tools, and **streams**
the reply back as SSE. The browser never sees the key.

## Build notes (from the S171 spike + claude-api skill)

- **Runtime:** Netlify Edge Function (Deno). Native streaming; 40 s response-header
  window; the 50 ms CPU limit excludes time spent waiting on the Claude API, so a
  multi-tool turn fits. Import the SDK via `npm:@anthropic-ai/sdk`.
- **Auth (design §4):** `new Anthropic()` resolves `ANTHROPIC_API_KEY` →
  `ANTHROPIC_AUTH_TOKEN` → an `ant auth login` OAuth profile. **Deployed:** set
  `ANTHROPIC_API_KEY` in Netlify env. **Local:** leave it unset and run on Matt's
  Claude subscription (the OAuth profile) — identical code, key-present is the only
  dev/prod diff.
- **Model:** `claude-opus-4-8` (S171 decision; swappable via ONE config constant —
  `claude-sonnet-4-6` is the cheaper fallback). Adaptive thinking on, streaming.
- **Tool loop:** `client.beta.messages.toolRunner({...})` with `betaZodTool`, OR a
  manual `client.messages.stream()` loop for per-token control + the separate
  typed-edge receipts channel. Cap tool iterations + `max_tokens`.
- **Prompt:** Bloodraven system prompt — bake in `working/chat-ui/bloodraven-persona-notes.md`
  verbatim (golden lines + anti-patterns). Hand the model FULL beat-level grounding
  (each node's quotes + the typed chain) so it narrates the chain richly — the S171
  smoke-test under-delivered only because its grounding was compressed. Put the
  stable prefix (persona + tool defs) first for prompt caching.
- **Cite-verification gate:** before presenting, verify each emitted `chapter:line`
  cite exists (via `read_node`/`read_passage`) — never show a quote at a fake cite.
  Keep "quotable book lines" separate from "context" in the prompt so the model
  doesn't quote grounding prose as a book line (a slip seen in the smoke-test).
- **Cost guard:** a GLOBAL daily spend ceiling in durable state (Netlify Blobs/KV) +
  per-request `max_tokens` + iteration bounds + an Anthropic-side billing alert.
  (Per-IP counters are bypassable — the global ceiling is the load-bearing control.)
- **Live-quote telemetry (design §8b):** instrument `search_chapters`/`read_passage`
  to log every live quote fetch from day one (harvest-style pointer) — cheap now,
  expensive to retrofit. (Deferred with live search to the fast-follow.)
- **Failure-mode UX:** explicit states for no-grounding / loop-bound-hit / API-error /
  timeout / cost-cap-tripped (design §9).
