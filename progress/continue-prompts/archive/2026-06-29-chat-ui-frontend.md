# SESSION 174 — Weirwood chat-UI alpha · FRONT-END chunk (chat page + receipts + deploy)

> **The 4th and final build chunk** for the deployable Bloodraven loremaster chat.
> S168 scoped → S169 design review → S170 publishing settled → S171 Foundation →
> S172 retrieval-core (`web/src/lib/`) → **S173 built the function** (`chat.ts` + `agent.ts`,
> 27 Deno tests green, `check:fn` clean). This chunk builds the browser UI that talks to
> `/api/chat` and ships it. Stamp your worklog entry `### Session 174` (meta track, `worklog.md`).
> **Recommended model:** Sonnet 4.6 — this is mostly static HTML/CSS/JS (a chat thread, an
> SSE client, a receipts panel, the static Tywin render). No new backend reasoning.

## What's already done (don't redo / don't reopen)
- **Function (S173):** `web/netlify/edge-functions/chat.ts` streams SSE from `/api/chat`. The
  **SSE contract you render against is in `web/netlify/edge-functions/README.md` → "SSE contract"**:
  events `token` (prose delta), `receipt` ({tool,input,result} — render the panel from `result`,
  NOT by parsing prose), `cite-check`, `status` (no-grounding / loop-bound-hit / api-error /
  cost-cap-tripped / unverified-cites), `error`, `done`. POST body = `{ messages: [{role,content}, …] }`
  ending on a user turn.
- **Foundation (S171):** `web/public/index.html` (placeholder), `web/public/theme/tokens.css`
  (**swap the whole look by editing this one file** — keep styling token-driven), `netlify.toml`
  (publish=web/public, /api/chat → chat), `web/data/` bundle (gitignored, rebuilt at deploy).
- **Static landing data (S171):** `web/data/featured-tywin.json` — `{question, title, chain:[…7 links],
  beats:[…], closing}` — render this as a pre-baked "who killed Tywin?" exchange on the landing page
  (no API call). Shape documented in `web/README.md`.
- **LOCKED — do NOT reopen:** Netlify Edge (Deno/TS); model `claude-opus-4-8` (swap via the one
  `MODEL` const in chat.ts); Option A tool-use; curated-MVP (live search deferred); repo stays
  PRIVATE → deploys to Netlify (`project_publish_settled` — never re-raise copyright/publishing).

## STEP 0 — read first
- `web/netlify/edge-functions/README.md` ← the SSE event contract (START HERE for the wire format).
- `working/chat-ui/alpha-design.md` §5 (persona/UI), §6 (look/theme + featured exchange + UI elements
  discussed), §0 (status table — flip the front-end rows + the deploy row when done).
- `web/public/theme/tokens.css` + `web/public/index.html` ← what you're extending.
- `working/demo-asoiaf-loremaster.md` ← the richness/voice bar the exchange should feel like.

## Your job (the browser UI only)
1. **Chat page:** a thread (user bubbles + a streaming Bloodraven bubble). POST to `/api/chat`,
   read the SSE stream, append `token` text live. On `done`, close. Token-driven styling from
   `tokens.css` only.
2. **Receipts panel:** render the typed-edge cards from each `receipt` event's `result` (the
   chain links / node quotes / neighbors) BESIDE the prose — render from the structured return,
   never by scraping narration. Keep provenance/cites in this panel, NOT in Bloodraven's voice.
3. **Static Tywin exchange:** render `featured-tywin.json` as a pre-baked landing transcript
   (question → answer → the 7-link chain as receipts) so the page is alive with zero API spend.
4. **Failure-mode UX (design §9):** wire the `status` states to explicit UI — `no-grounding`,
   `loop-bound-hit`, `api-error`, `cost-cap-tripped`. Show an `error` line plainly.
5. **Deploy:** local-run-approved → deploy private repo to Netlify, set `ANTHROPIC_API_KEY` in
   Netlify env. (`netlify dev` / live deploy spend real API $ — **confirm with Matt before any
   live call or deploy**, per no-extraction-without-asking.)

## Proving test
`netlify dev`: the landing shows the static Tywin exchange immediately; typing a new question
streams a Bloodraven answer with a populated receipts panel. **Run only with Matt's go-ahead**
(real API spend). Everything you can validate dry (markup, the SSE-parsing JS against a recorded
event log, the static render from `featured-tywin.json`) — do first.

## End-of-chunk
Flip `web/README.md` + design §0 front-end + deploy rows; if shipped, update
`project_real_goal_graph_for_agents` memory with the live URL; log `### Session 174`. This
completes the chat-UI alpha track — archive this prompt.

## DO NOT
run live API calls / deploy without Matt's go-ahead · reopen runtime/model/scope/publishing
decisions · change the SSE contract (the function emits it; render what's there) · shell out to
Python from the browser · mint graph edges/nodes · auto-run `/endsession`.
