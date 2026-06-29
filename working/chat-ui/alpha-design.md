# Weirwood chat-UI alpha — working design / implementation plan

> **Status: DISCUSSION, nothing locked.** This is a working design from a brainstorming session (S168, 2026-06-29),
> written so a fresh session can pick the thread up. Every "decision" below is a *current lean* or an *open
> question* — treat it as a starting point for Matt to react to, not a committed spec. Where it says "Matt wants",
> that's a stated preference; where it says "open", it's genuinely undecided.
>
> Companion files: `working/chat-ui/bloodraven-persona-notes.md` (the voice), `working/demo-asoiaf-loremaster.md`
> (the PROVEN retrieval pattern this productizes), `history/archive/sketches/chat-ui-architecture.md` (the OLD full
> vision — far heavier than this alpha; mine it for ideas, don't treat as the plan). Memory:
> `project_real_goal_graph_for_agents` (updated S168 — chat-UI alpha is a live track for Matt's job portfolio).

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
- **Full book text:** `sources/chapters/<book>/<book>-<pov>-<nn>.md` — all 344 chapters, line-numbered, **gitignored**
  (copyrighted). This is what enables *live* quote-finding beyond curated quotes.

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
  to lean on graph vs raw text; the "chain walked" receipts fall out of the tool-call trace.
- **Cons:** agentic loop = more tokens + more latency per answer; needs streaming + a function runtime that tolerates
  multi-second multi-tool turns (Netlify sync functions are ~10s — may need a streaming/background function or Edge);
  bundling 344 chapters of text into the deploy artifact (size + the book text living in the function bundle).
- **Open:** exact tool set; whether to shell out to the existing `.py` scripts or reimplement traversal in the
  function's language; how to bound the loop (max tool iterations / `task_budget`); how big the chapter bundle is.

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
- **Cost / abuse guard:** add a simple per-day or per-IP cap in the function so a visitor can't run up the bill. A
  portfolio piece fielding hundreds of questions is a few dollars.
- **Local dev:** same code runs locally with the key in a `.env`; deploy is just wiring the function + env var.

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
*"Lord Tywin Lannister did not, in the end, shit gold."* (`asos-tyrion-11:269`). Seed example prompts in the input
("why did Robert's Rebellion start?", "what led to the Red Wedding?").

### UI elements discussed
- Chat thread (user bubble + Bloodraven reply with blockquotes + cites).
- **"Chain walked" receipts panel — make it MORE ROBUST (Matt, S168): show the typed EDGES, not just node chips.**
  Render the actual relationship between each link — `poisoned-hairnet —[ENABLES]→ death-of-joffrey —[CAUSES]→
  trial-of-tyrion …` — so the typed graph traversal is visible (CAUSES / ENABLES / MOTIVATES / TRIGGERS labels on
  the connectors). This is the proof-of-realness and a strong portfolio signal — it shows a genuine typed knowledge
  graph underneath, not an LLM freestyling. Consider per-link expansion (click a link → its evidence quote + cite).
  A small visual node-graph rendering of the walked chain is a natural extension.
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

## 7. Copyright posture (settled enough — not a blocker)

Matt: "not advertising this, the wiki uses quotes from the books all the time." Agreed — this is a non-monetized,
low-profile fan project quoting cited passages, same as the AWOIAF wiki does on every page. **Do not over-engineer
this.** One footer line is enough: *"a fan project · quotes © George R.R. Martin, used for commentary · will honor
any takedown request."* (It's commentary/research fair-use territory, not "parody" specifically.) The book text is
gitignored from the public repo; it would be bundled into the (private) function deploy.

---

## 8. Rough build plan (Option A path) — sequence, not a commitment

1. **Graph data export** — a one-time script that flattens what the function needs into deploy-bundleable form:
   node files (or a nodes JSON), `edges.jsonl`, alias maps, and the chapter text. Decide bundle shape + size.
2. **Retrieval tools** — implement `resolve / walk_chain / neighbors / read_node / search_chapters / read_passage`
   (port `graph-query.py` + `event_alias_resolver.py` logic, or shell to them if the runtime allows).
3. **The function** — Claude tool-runner loop + Bloodraven system prompt (persona notes baked in) + streaming +
   the per-day cost cap + the `ANTHROPIC_API_KEY` env var.
4. **Chat page** — simple, themeable (token file), streams the reply, renders blockquotes + cites + the receipts
   panel, pre-loads the Tywin featured exchange, seeds example prompts.
5. **Local run** — verify Bloodraven answers against the real graph + live chapter search before deploying.
6. **Netlify deploy** — function + page + env var; link from Matt's profile.
7. **(Later)** embeddings only if grep recall is weak; the visual node-graph; full mattnoth.com integration; more
   personas.

**Effort:** the curated-quote-only version is ~a day; adding the live `search_chapters`/`read_passage` tools + the
agentic loop is more (the chapter bundle + the loop runtime/streaming work) — but it's the capability Matt most
wants, so it's in scope.

---

## 8b. Future evolution — the self-curating quote loop (Matt, S168) — drop the book text over time

A key long-game insight that shapes the build: the live `search_chapters` tool isn't just a feature, it's a
**discovery engine for what to curate.** The loop:

1. The chat answers questions; when it has to **search the book text live** for a quote (because the quote wasn't
   already curated onto a node/edge), **log that hit** — a harvest-style pointer (`chapter:line` / the quote / the
   node it belonged to), exactly like `working/harvest-queue.md` does for research finds.
2. Periodically (after enrichment passes + chat smoke-tests), a **harvest/mint pass** consumes those pointers and
   attaches the quotes to the right nodes' `## Quotes` (the existing harvest machine — memory `feedback_harvest_queue`).
3. Over time the **curated quote layer absorbs the load-bearing quotes** — the ones visitors actually pull.
4. Once curated coverage is high enough, the chat can rely on the graph's quotes and **stop needing the full book
   text bundled in the deploy** — and eventually the verbatim text can leave the repo entirely. The live-search tool
   makes itself progressively unnecessary.

**Build implication:** instrument `search_chapters` / `read_passage` from day one to **emit a log of live quote
fetches** (a queue/telemetry feed), so this curation loop has data to run on later. Cheap to add now, expensive to
retrofit. This is also the cleanest answer to the "we're shipping the copyrighted book text" discomfort — it's a
temporary scaffold that the curated graph grows to replace.

## 9. Open questions for the fresh session to resolve with Matt

- **Retrieval shape:** Option A (tool-use agent, live grep — current lean) vs B (RAG-lite)? Confirm.
- **Theme:** lean is set (modern/simple, dark default, soft weirwood-tree background — not hard black/red); open
  parts are the exact palette values + how the weirwood tree is rendered (SVG / CSS / image).
- **Model:** Sonnet 4.6 (cost) vs Opus 4.8 (prose) — smoke-test the persona on both.
- **Runtime:** can a Netlify Function host a multi-tool streaming agentic turn within its limits, or do we need
  Edge / background / a different host? (Investigate Netlify Functions streaming + timeout.)
- **Chapter bundle:** size of 344 chapters as a function-bundled asset; any need to compress/index.
- **Standalone deploy first, fold into mattnoth.com later** — confirmed direction, but the integration details
  (submodule vs copy, page wiring) are deferred.
- **Scope of the alpha:** ship curated-quotes-only first and add live search as a fast-follow, or build live search
  into v1? (Matt leans toward wanting the live search.)

---

## 10. How to resume (fresh context)

Start a new session and: read this file + `working/chat-ui/bloodraven-persona-notes.md` +
`working/demo-asoiaf-loremaster.md`, skim memory `project_real_goal_graph_for_agents`. Then pick up at §9 (resolve
the open questions with Matt) before building. **Recommended model for the build session:** Opus 4.8 (or Sonnet 4.6
for the mechanical scaffolding). Nothing here is locked — confirm with Matt before committing to the architecture.
