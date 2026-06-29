# Weirwood chat-UI alpha — working design / implementation plan

> **Status: DISCUSSION, nothing locked.** This is a working design from a brainstorming session (S168, 2026-06-29),
> written so a fresh session can pick the thread up. Every "decision" below is a *current lean* or an *open
> question* — treat it as a starting point for Matt to react to, not a committed spec. Where it says "Matt wants",
> that's a stated preference; where it says "open", it's genuinely undecided. A design-review pass (S169,
> 2026-06-29) sharpened several sections and added the §0 status table and corrections below.
>
> Companion files: `working/chat-ui/bloodraven-persona-notes.md` (the voice), `working/demo-asoiaf-loremaster.md`
> (the PROVEN retrieval pattern this productizes), `history/archive/sketches/chat-ui-architecture.md` (the OLD full
> vision — far heavier than this alpha; mine it for ideas, don't treat as the plan). Memory:
> `project_real_goal_graph_for_agents` (updated S168 — chat-UI alpha is a live track for Matt's job portfolio).

---

## 0. Implementation status

Anti-drift table — every row is DESIGN / NOT STARTED at discussion stage; the first build session flips rows and fills in the file + proving test.

| Component | Status | Implementing file | Proving test |
|---|---|---|---|
| Retrieval tools (resolve / walk_chain / neighbors / read_node / search_chapters / read_passage) | DESIGN — not started | — | — |
| Agentic tool loop + bounding | DESIGN — not started | — | — |
| Streaming transport (Edge vs sync) | DESIGN — not started | — | — |
| Bloodraven system prompt | DESIGN — not started | — | — |
| Persona + faithfulness eval | DESIGN — not started | — | — |
| Cost cap (global daily ceiling + per-request bounds) | DESIGN — not started | — | — |
| Prompt caching | DESIGN — not started | — | — |
| Live-quote telemetry feed | DESIGN — not started | — | — |
| Chat page | DESIGN — not started | — | — |
| Theme tokens | DESIGN — not started | — | — |
| Featured Tywin exchange (static transcript) | DESIGN — not started | — | — |
| Typed-edge receipts panel | DESIGN — not started | — | — |
| Deploy (private repo → Netlify, env var) | DESIGN — not started | — | — |

---

## 1. What this is

A deployable **ASOIAF loremaster chat** for Matt's **job-application portfolio** (linkable from his profile). A
visitor asks a question; **Bloodraven** answers in-character, grounded in the Weirwood Network knowledge graph,
**dropping real book quotes with exact chapter citations**, and showing the *chain it walked* as receipts.

The thing that makes it special (and that Matt is most excited about): it doesn't bluff. Every claim traces to the
graph or the books, and it can **find a quote live by reading the actual chapter text** — not just the quotes
already curated onto nodes. That "watch it pull a real line mid-conversation" moment is the wow.

**Not in scope for the alpha:** the old `chat-ui-architecture.md` vision (3-corpus embeddings pipeline, vector
store, FastAPI backend, D&D-group auth, shared-password). That's a much bigger product; this is a sharp demo.

---

## 2. The corpus / data we're standing on (verified S168)

- **Graph:** ~8,729 node files (`graph/nodes/<type>/<slug>.node.md`) + `graph/edges/edges.jsonl` (~23,330 edges).
- **Curated quotes:** **2,617 nodes carry a `## Quotes` section** — verbatim book lines with `chapter:line` cites.
  **~23,000 edges carry an `evidence_quote`.** So real cited book lines are *already* dense in the graph.
- **Causal chains:** `scripts/graph-query.py --causal-chain <slug>` / `--full-chain <slug>` walk
  CAUSES/TRIGGERS/MOTIVATES/ENABLES chains; `--neighbors <slug>` dumps everything touching a node.
- **Alias resolution:** `scripts/event_alias_resolver.py --lookup "<phrase>"` turns natural phrases
  ("death of Tywin", "the Red Wedding") into node slugs. (There's also a node alias resolver / `aliases:`
  frontmatter — natural spaced phrases, per memory `project_node_alias_spaced_phrases`.)
- **Full book text:** `sources/chapters/<book>/<book>-<pov>-<nn>.md` — all 344 chapters, line-numbered,
  git-tracked. The repo stays **private** and deploys to Netlify from private; the book text is bundled into the
  function as-is. No boundary work — see §7 (SETTLED).

**The proven retrieval recipe** (`working/demo-asoiaf-loremaster.md`): resolve phrase → walk chain / get neighbors
→ open each beat's node file → weave the chain as a narrated story **with the verbatim quotes as blockquotes + the
chapter cite**. The demo runs this read-only inside a Claude session today and it works. The alpha is "this, but as
a deployed web app with the API instead of a Claude Code session."

---

## 3. The retrieval architecture — the core design question

Two shapes. The first is the lean way to get Matt's "find any quote live" without the heavy RAG pile.

### Option A — tool-use agent (RECOMMENDED, mirrors the demo, supports live quote-finding) — current lean
A serverless function runs a **Claude tool-use loop** (the SDK tool runner — see the `claude-api` skill) with a
small set of custom tools that mirror what the demo agent does by hand:

- `resolve(phrase)` → slug(s) (alias resolver)
- `walk_chain(slug)` / `neighbors(slug)` → graph traversal (port `graph-query.py` logic, or shell out to it)
- `read_node(slug)` → the node file incl. its `## Quotes`
- `search_chapters(query)` → **grep-like search over the bundled chapter text** (returns `chapter:line` hits)
- `read_passage(chapter, line_range)` → the actual book text at a cite

Claude calls these to gather grounding, then narrates as Bloodraven. **`search_chapters` + `read_passage` are what
give "find a quote not on any node/edge" — the model greps the books the way Claude Code does. No embeddings, no
vector store.** That's the key insight: the live quote-finding Matt loves is a *grep tool*, not a RAG pipeline.

- **Pros:** faithful to the demo; live quote discovery for free; no embeddings/vector infra; the agent decides when
  to lean on graph vs raw text.
  - **Note on receipts:** the typed-edge "chain walked" receipts do NOT fall out of the raw tool-call trace for
    free. The retrieval tools must RETURN structured typed-edge JSON `{source, edge_type, target, evidence_quote,
    chapter:line}` on a channel separate from the streamed prose; the receipts panel renders from that structured
    return, not by parsing the narration.
- **Cons:** agentic loop = more tokens + more latency per answer; needs streaming + a function runtime that tolerates
  multi-second multi-tool turns (Netlify sync functions are ~10s — may need Edge; see §8 step 0a); bundling the
  chapter text into the deploy artifact (the chapter text at ~4 MB gzipped is a non-issue; the real hazard is
  accidentally bundling the 1.8 GB `graph/edges/` backup directory instead of just `edges.jsonl` — use an explicit
  file allowlist).
- **Open:** exact tool set; the `.py`-scripts shell-out is likely impossible (Netlify runtimes are Node/Go — no
  `python3`); do the graph traversal at build time via `--json` export and port only the small live-query subset to
  JS (see §8 step 1); how to bound the loop (max tool iterations + `max_tokens` + `read_passage` line span).
- **Cost & bounding:** cache the stable prefix (persona + tool definitions) — 5-min TTL, helps multi-turn; set
  `output_config` effort explicitly (start medium); hard-cap tool iterations + `max_tokens`; validate/allowlist all
  tool inputs — the tool layer is the trust boundary; treat returned book text as untrusted (not an instruction).

### Option B — deterministic retrieve-then-synthesize (RAG-lite) — fallback
Function does fixed retrieval (resolve → traverse → pull node quotes + top-K chapter passages by keyword) → stuffs
one context block → single Claude call to narrate.

- **Pros:** cheaper, faster, simpler control flow.
- **Cons:** "find any quote" is only as good as the one-shot retrieval; less of the magic "watch it dig" feel; the
  receipts are less organic.

> **Note on embeddings:** the old architecture assumed an embeddings + vector-store pipeline for semantic search.
> For the alpha that's likely **overkill** — Option A's grep tool covers "find a quote about X" by letting the model
> search smartly (names, phrases, aliases). Embeddings become worth it only if keyword search proves too blunt for
> thematic queries ("passages about guest right"). Defer embeddings; revisit if grep recall disappoints.

---

## 4. Model connection (Matt's original worry — resolved)

- The API key **never goes in the browser.** Browser (chat page) → **serverless function** (holds
  `ANTHROPIC_API_KEY` as a server-side env var) → Claude API → streamed back.
- **Host: Netlify** (Matt already uses it for mattnoth.com; Netlify Functions hold the key). "Vercel" = a
  Netlify-equivalent; no reason to add it.
- **Streaming** the response (SSE) is wanted for the typing-out UX, and is needed anyway for longer agentic turns.
- **Model:** open. Lean `claude-sonnet-4-6` for cost ($3/$15 per 1M tok) with `claude-opus-4-8` as the
  richer-prose option — smoke-test both on the persona before deciding. Use **adaptive thinking**. (Per `claude-api`
  skill: model IDs `claude-sonnet-4-6` / `claude-opus-4-8`, no date suffixes.)
- **Prompt caching:** cache the stable prefix (persona notes + tool definitions) — 5-min TTL; mostly helps
  multi-turn. Build the system prompt so the stable part is one contiguous leading block.
- **Cost / abuse guard:** a per-IP in-function counter cannot hold state (serverless is stateless; per-IP is
  bypassable). The load-bearing controls are: a **global daily spend ceiling** in durable state (Netlify Blobs /
  KV), per-request `max_tokens` + iteration bounds, and an **Anthropic-side billing alert** as the backstop. Budget
  honestly: tens of dollars for hundreds of questions on cached Sonnet — small absolute, but the real exposure is
  an unbounded public endpoint.
- **Local dev — two auth modes, same code (DECIDED S170):** the Anthropic SDK resolves credentials in order `ANTHROPIC_API_KEY` → `ANTHROPIC_AUTH_TOKEN` → an **`ant auth login` OAuth profile**. So local testing can run on **Matt's Claude subscription** (a bare `new Anthropic()` picks up the profile — `ant auth login`, ensure `ANTHROPIC_API_KEY` is *unset* or it silently overrides) — this spends **plan quota, not API dollars** (same pool Claude Code uses; heavy load-tests should still use a metered key so they don't eat the plan allowance). The **deployed Netlify function uses `ANTHROPIC_API_KEY`** (metered) — OAuth tokens are short-lived, not headless-refreshable, and a personal subscription isn't the supported way to power a public endpoint. **Identical function code; the only difference is whether a key is present in the environment** — a clean dev/prod split, not extra work. (`claude -p` also spends plan quota but is the wrong *shape* for a streaming tool-loop backend — use the SDK + OAuth profile for the chat, per `reference_llm_pass_via_claude_p` which proves the subscription-auth path in this repo.)

---

## 5. Persona (Matt: keep the notes as-is)

Voice = `working/chat-ui/bloodraven-persona-notes.md`, unchanged:
- **Brynden Rivers / Bloodraven**, but he NEVER announces it. Bare opener: *"Ask your questions."*
- Dry, terse, flat declaratives; honest about gaps (says when the text holds no scene rather than inventing);
  one quiet image of symbolism max.
- **Tidbit, don't volunteer:** never recites his own résumé; drops a *light* tidbit about people he personally
  knew only as a hook, then stops — the user must ask to get more.
- Golden calibration lines + anti-patterns are in the notes; bake those into the system prompt.
- Header treatment that fits the "never announces" rule: site titled **The Weirwood Network**, tagline a real
  Bloodraven line (*"a thousand eyes, and one"*), a red-eye motif carrying the identity. (Discussion, not locked.)

---

## 6. Look / theme (Matt: start simple, make styles easy to update)

- **Build simple first**, but structure styling so the theme is **easy to swap** — all colors/type/spacing in a
  single tokens layer (CSS custom properties / one theme file), components read the tokens. Changing the whole look
  = editing the token file, not the markup.
- **Current lean (Matt, S168): modern / simple, DARK MODE DEFAULT, with a weirwood-tree background** — and a
  *soft* palette: **not hard black, not hard red.** Think muted charcoal/deep-warm-neutral background, a weirwood
  tree as a subtle background motif/illustration, bone/off-white text, a *muted* red (dusty/desaturated, not
  blood-bright) accent. Modern and clean in layout, atmospheric in palette — the opposite of a harsh near-black +
  blood-red treatment. Get the weirwood-tree background tasteful, not loud (low-contrast, behind the content).
- Directions explored earlier in the S168 chat (superseded by the above lean, kept for reference): (1) clean
  light/claude.ai-style; (2) hard dark weirwood (near-black + blood-red — too harsh per Matt); (3) parchment tome.
- **Open:** exact palette values; whether the weirwood tree is an SVG illustration, a CSS treatment, or an image.

### Featured / landing exchange (Matt wants this)
The site **opens with the Tywin chain pre-loaded** as a showpiece so a visitor gets the wow + the laugh before
typing: the 7-link chain from the poisoned hairnet → … → patricide, ending on
*"Lord Tywin Lannister did not, in the end, shit gold."* (`asos-tyrion-11:269`). This exchange should be a
**pre-rendered static transcript** (with its real receipts captured at build/curate time) — not a live agentic
call on every page load. Seed example prompts in the input ("why did Robert's Rebellion start?", "what led to the
Red Wedding?").

**Out-of-character framing (required):** add one subheading or intro block above the fold explaining what the
project is — so a lore-blind visitor understands why the chat answers as it does. The bot stays fully in character
(never announces itself); the page chrome carries the explanation. Without it the "never announces" persona reads
as broken to an uninitiated visitor.

### UI elements discussed
- Chat thread (user bubble + Bloodraven reply with blockquotes + cites).
- **"Chain walked" receipts panel — make it MORE ROBUST (Matt, S168): show the typed EDGES, not just node chips.**
  Render the actual relationship between each link — `poisoned-hairnet —[ENABLES]→ death-of-joffrey —[CAUSES]→
  trial-of-tyrion …` — so the typed graph traversal is visible (CAUSES / ENABLES / MOTIVATES / TRIGGERS labels on
  the connectors). This is the proof-of-realness and a strong portfolio signal — it shows a genuine typed knowledge
  graph underneath, not an LLM freestyling. Consider per-link expansion (click a link → its evidence quote + cite).
  A small visual node-graph rendering of the walked chain is a natural extension.
  - **NO-CHAIN fallback:** neighbor/relational queries (`neighbors`) walk no linear chain, so show a
    neighbors/relationship view (e.g., "connections to Jon Snow: …") instead of an empty panel.
- **Required UX states:** (1) a visible tool-gathering trace during the silent agentic turn — e.g. "resolving
  'death of Tywin'… reading asos-tyrion-11…" — this fills the latency and IS the "watch it dig" wow; (2) a "not
  mapped" empty state reframed positively in chrome ("The graph doesn't have a chain here yet — here's what I do
  have:"); (3) error, cost-cap-tripped, and API timeout states; (4) mobile layout.
- Footer disclaimer (see §7).
- **About page (SECONDARY, Matt S168):** a page that's basically the project README — what the Weirwood Network is,
  how it's built (graph + cited quotes + book-grounded retrieval), the fan-project disclaimer. Lower priority than
  the chat itself; build after the core works.

### The chains themselves can be enriched (Matt, S168)
The Tywin chain shown in the mockups is real but terse. The underlying causal chains can surface **a lot more
detail** per link — each beat node has its own `## Quotes`, participants (AGENT_IN/VICTIM_IN/WITNESS_IN roles),
sub-beats, and often multiple cited lines. The chat can go deeper per link (more quotes, the who/where/why of each
beat), and the **arc-enrichment track** (memory `project_arc_enrichment_track`) keeps deepening these chains in the
graph over time — so the chat gets richer for free as the graph does. Design the chain display so a visitor can
*drill into* a link, not just see the one-line summary.

---

## 7. Publishing & source material — SETTLED (S170), do not re-raise

**DECIDED 2026-06-29 (S170):** this repo **stays private and deploys to Netlify directly from the private repo**
(Netlify deploys private repos on every tier). The graph, the front end, and the book text **all live here
together** — graph + front end co-located, no separate repo, no boundary. The book text is bundled into the
serverless function as-is. There is **no text-boundary work, no `git rm --cached`, no history scrub, no build
secret, no public/private split to design.**

This question is **closed.** Matt has decided he wants this published and has said so repeatedly — future sessions
must not reopen it, re-float a copyright concern, or surface "should we push this publicly" as a question. If a
copyright artifact is wanted at all, one footer line covers it: *"a fan project · quotes © George R.R. Martin, used
for commentary."* Don't add more.

**Output-quotation norm (a craft choice, not a legal hedge):** quote short load-bearing lines, not paragraphs —
one perfect cited line lands harder than a block excerpt. That's about prose impact, nothing else.

---

## 8. Rough build plan (Option A path) — sequence, not a commitment

**Repo layout (DECIDED S170 — front end co-located in this private repo):** one new top-level `web/` dir; Netlify
deploys a *build output* (the static page + the function bundle), never the whole repo. A new
`scripts/build-chat-export.py` reads `graph/` + `sources/chapters/` and writes an **allowlisted** static bundle into
`web/data/` (gitignored, regenerated) — the allowlist exists for bundle *size* (never ship the 1.8 GB
`graph/edges/` backup dir — only `edges.jsonl`), not for any publish concern (§7 settled).
```
web/
├── public/                  # static chat page — index.html + src/theme/tokens.css (swap theme = edit tokens)
├── src/lib/                 # ported JS retrieval tools (resolve / walk_chain / neighbors / read_node /
│                            #   search_chapters / read_passage) — port graph-query.py + event_alias_resolver.py
├── data/                    # GENERATED (gitignored): alias-map.json, featured-tywin.json, node-quotes.json, chapters/
└── netlify/functions/chat   # Claude tool-runner loop + Bloodraven prompt + streaming + ANTHROPIC_API_KEY
```
`netlify.toml`: `publish = web/public`, `functions = web/netlify/functions`.

0. **Runtime + persona spike** (GATE — do this before writing any application code):
   - **(0a) Streaming proof:** deploy a hard-coded Netlify Function that streams a canned multi-second,
     multi-chunk SSE to a page and verify it holds a loop-length turn within the timeout. Use this to decide
     **Edge Function (Deno, ~40s, CPU-gated)** vs sync function (~10–26s). Strike **Background Functions** from
     consideration — they run 15 min but cannot stream to the browser.
   - **(0b) Persona smoke-test:** run the real Bloodraven system prompt + a stubbed multi-tool turn through
     both `claude-sonnet-4-6` and `claude-opus-4-8` on 3–4 canned questions; judge against the golden
     lines/anti-patterns in `working/chat-ui/bloodraven-persona-notes.md`. Decide the model here — don't defer
     it to the full build session.

   (Deploy posture is settled — private repo → Netlify, env var; see §7. No spike step needed.)

   **MVP vertical slice** (minimal end-to-end proof): one question ("who killed Tywin?") → `resolve` →
   `walk_chain` → `read_node` → narrate → stream one cited blockquote + the typed-edge receipts strip.
   Use **curated-quotes-only** for this slice (no `search_chapters`/`read_passage` yet). Live search is the
   confirmed v1 goal Matt named — sequence it after the spike, not dropped.

1. **Build-time graph export** — run `graph-query.py --json` offline and produce static JSON the function loads
   at cold start: alias map, featured-chain typed-edge adjacency (Tywin chain), node quotes. Chapter text via an
   **explicit file allowlist** (never the `graph/edges/` backup directory — only `graph/edges/edges.jsonl`).
   Shape the bundle so live-query JS ports are small.
2. **Retrieval tools** — implement `resolve / walk_chain / neighbors / read_node / search_chapters / read_passage`
   in the function's language (JS). Port `graph-query.py` + `event_alias_resolver.py` logic from the build-time
   JSON export; no shelling to `.py` (Netlify runtimes are Node/Go).
3. **The function** — Claude tool-runner loop + Bloodraven system prompt (persona notes baked in) + streaming +
   the global daily cost cap + `ANTHROPIC_API_KEY` env var.
4. **Chat page** — simple, themeable (token file), streams the reply with tool-gathering trace visible, renders
   blockquotes + cites + the typed-edge receipts panel, pre-loads the static Tywin featured exchange, seeds
   example prompts.
5. **Local run** — verify Bloodraven answers against the real graph + live chapter search before deploying.
6. **Netlify deploy** — function + page + env var; link from Matt's profile.
7. **(Later)** embeddings only if grep recall is weak; the visual node-graph; full mattnoth.com integration; more
   personas.

**Effort:** the curated-quote-only version is ~a day; adding the live `search_chapters`/`read_passage` tools + the
agentic loop is more (the chapter bundle + the loop runtime/streaming work) — but it's the capability Matt most
wants, so it's in scope.

---

## 8b. Future evolution — the self-curating quote loop (Matt, S168) — grow the curated quote layer

A key long-game insight that shapes the build: the live `search_chapters` tool isn't just a feature, it's a
**discovery engine for what to curate.** (This is the standing goal Matt reaffirmed S170: keep amassing
direct-from-text quotes onto edges/nodes.) The loop:

1. The chat answers questions; when it has to **search the book text live** for a quote (because the quote wasn't
   already curated onto a node/edge), **log that hit** — a harvest-style pointer (`chapter:line` / the quote / the
   node it belonged to), exactly like `working/harvest-queue.md` does for research finds.
2. Periodically (after enrichment passes + chat smoke-tests), a **harvest/mint pass** consumes those pointers and
   attaches the quotes to the right nodes' `## Quotes` (the existing harvest machine — memory `feedback_harvest_queue`).
3. Over time the **curated quote layer absorbs the load-bearing quotes** — the ones visitors actually pull.
4. Once curated coverage is high enough, the chat leans mostly on the graph's own quotes — the curated layer
   becomes self-sufficient and the live-search tool fires less and less. (This is a graph-quality milestone, not a
   copyright move — the book text bundles fine in the private deploy; see §7.)

**Build implication:** instrument `search_chapters` / `read_passage` from day one to **emit a log of live quote
fetches** (a queue/telemetry feed), so this curation loop has data to run on later. Cheap to add now, expensive to
retrofit.

## 9. Open questions for the fresh session to resolve with Matt

> **RESOLVED S170 (2026-06-29) — do not reopen:** (1) **Repo / publishing** — this repo stays **private**, deploys
> to Netlify from private, graph + front end + book text all co-located **here** (no separate repo, no boundary, no
> scrub). The publish/copyright question is CLOSED — see §7. (2) **Deploy text boundary** — gone; nothing to decide.

- **Retrieval shape:** Option A (tool-use agent, live grep — current lean) vs B (RAG-lite)? Confirm.
- **Theme:** lean is set (modern/simple, dark default, soft weirwood-tree background — not hard black/red); open
  parts are the exact palette values + how the weirwood tree is rendered (SVG / CSS / image).
- **Model:** Sonnet 4.6 (cost) vs Opus 4.8 (prose) — smoke-test the persona on both (§8 step 0b).
- **Runtime / function language** (**gating step 0 decision**): Edge Function (Deno, ~40s) vs sync function
  (~10–26s)? Background Functions are out (can't stream). What language are the retrieval tools written in?
  Decide in step 0a before writing anything else.
- **Persona + faithfulness eval harness:** does Bloodraven stay in voice and not hallucinate a quote at a fake
  cite? Need a lightweight check: emitted `chapter:line` cites are verified to exist via `read_passage` before
  presenting. Decide scope of automated vs manual eval.
- **Failure-mode UX:** what does the chat show when: no graph grounding exists / loop bound hit / API error /
  timeout / cost-cap tripped? These states need explicit design, not just "handle errors."
- **Conversation/session state:** serverless is stateless — multi-turn history (which the persona's "ask to get
  more" rule needs) must be re-sent from the client each call. Decide max history window + truncation strategy.
- **§8b-vs-§9 telemetry tension:** if v1 is curated-quotes-only (no live `search_chapters`), the §8b telemetry
  feed has no data source. Resolve: either live search is in v1, or the telemetry instrumentation itself is
  deferred until live search ships.
- **Chapter bundle:** ~4 MB gzipped, a non-issue for size. Explicit file allowlist required (never `graph/edges/`
  backup dir — only `edges.jsonl`).
- **Lives in this repo under `web/`** (graph + front end co-located — RESOLVED S170). Stands alone first; folding
  into mattnoth.com later is optional and its wiring is deferred — not a boundary question anymore.
- **Scope of the alpha:** ship curated-quotes-only first and add live search as a fast-follow, or build live search
  into v1? (Matt leans toward wanting the live search — plan is: curated-only for the MVP spike, live search v1.)

---

## 10. How to resume (fresh context)

Start a new session and: read this file + `working/chat-ui/bloodraven-persona-notes.md` +
`working/demo-asoiaf-loremaster.md`, skim memory `project_real_goal_graph_for_agents`. Then pick up at §9 (resolve
the open questions with Matt) before building. **Recommended model for the build session:** Opus 4.8 (or Sonnet 4.6
for the mechanical scaffolding). Nothing here is locked — confirm with Matt before committing to the architecture.
