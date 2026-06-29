# SESSION 171 — Weirwood chat-UI alpha (build track)

> **This is Session 171.** If you log to `worklog.md`, stamp your entry `### Session 171` (meta track). (This is app
> work, a sub-track — the number is for the worklog stamp; not a graph-enrichment dip.)
> **Recommended model:** Opus 4.8 (design/architecture + build judgment; Sonnet 4.6 fine for mechanical scaffolding).
> **This is a fresh-context handoff.** S168 scoped this; S169 ran a 6-lens design review; **S170 SETTLED the
> publishing/repo/auth architecture** (private repo + co-located `web/`; book text bundles as-is; no boundary work)
> and folded it into `working/chat-ui/alpha-design.md`. The design is now decision→build-ready — read it fresh
> (§0 status table; §4 auth modes; §7 publishing SETTLED; §8 repo layout + step-0 gate; §9 remaining opens).
> **Matt's explicit instruction: a *fresh* session builds this — not the scoping/review sessions.** That's you.
> **PUBLISHING IS A CLOSED QUESTION (S170) — do NOT re-raise copyright / "should we push this publicly." See memory
> `project_publish_settled`.** Repo stays private + deploys from private; that's decided.

## What this is
Build a deployable **ASOIAF loremaster chat** for Matt's **job-application portfolio** (linkable from his profile):
a visitor asks a question, **Bloodraven** answers in-character, grounded in the Weirwood Network graph, dropping
**real book quotes with chapter citations**, and showing the **typed-edge chain it walked** as receipts. The wow is
that it doesn't bluff and can **find quotes live by reading the chapter text**, not just curated node quotes.

## STEP 0 — read first (the design is already written)
- **`working/chat-ui/alpha-design.md`** ← the full working design (corpus, retrieval architecture options, model
  connection, persona, theme, build plan, open questions). START HERE. **Folded in (S169+S170):** §0 status table;
  **§4 local-auth modes** (subscription OAuth profile locally = plan quota / API key on deploy); **§7 Publishing
  SETTLED** (private repo + co-located `web/`, book text bundles as-is — NO boundary/scrub work); **§8 repo layout**
  (`web/` + `scripts/build-chat-export.py`) + the **step-0 runtime+persona spike** that GATES the build; structured
  typed-edge receipts + no-chain fallback; prompt-caching + a global daily spend ceiling; UX states; §9 remaining opens.
  **Begin with the §8 step-0 spike — do not build the export/tools until runtime + model are decided.**
- `working/chat-ui/bloodraven-persona-notes.md` — the voice (use as-is per Matt; bake into the system prompt).
- `working/demo-asoiaf-loremaster.md` — the PROVEN retrieval recipe this productizes (run it to feel the target).
- memory `project_real_goal_graph_for_agents` (chat-UI alpha is a live track), `project_arc_enrichment_track`
  (the chains keep getting richer), `feedback_show_commands`, `feedback_no_extraction_without_asking`.
- `history/archive/sketches/chat-ui-architecture.md` — the OLD heavy vision; mine for ideas, do NOT treat as the plan.

## Matt's stated preferences (from S168 — confirm before locking, nothing is nailed down)
- **Host / repo (SETTLED S170):** Netlify, deploying from **this private repo**; front end co-located under a new
  `web/` (graph + book text stay here, bundle into the function as-is). Standalone deploy first; fold into
  mattnoth.com later. **Local dev runs on Matt's Claude subscription** (`ant auth login` OAuth profile, `ANTHROPIC_API_KEY`
  unset → bare SDK client = plan quota, no API $); **deployed function uses `ANTHROPIC_API_KEY`** server-side, browser
  never sees it. Identical function code; key-present is the only dev/prod diff. (Design §4.)
- **Persona:** Bloodraven, notes as-is (bare "Ask your questions." opener; never announces he's Bloodraven; terse).
- **Corpus:** graph (nodes + curated `## Quotes` + cited edges) AS the spine, PLUS **live full-text quote-finding**
  over the 344 chapters — Matt specifically loves "find a quote not on any node/edge." Lean = a tool-use agent with
  a **grep-like `search_chapters` tool** (NO embeddings/vector store needed for the alpha). See design §3 Option A.
- **Instrument live quote fetches from day one (design §8b — the self-curating loop):** log every time the chat has
  to `search_chapters`/`read_passage` for a quote not already curated (harvest-style pointer). Later mint passes
  attach those quotes to nodes; over time the curated layer absorbs them and the **bundled book text can be dropped**
  (and eventually leave the repo). Cheap to add now, expensive to retrofit — bake the logging in.
- **Theme:** modern / simple, **dark-mode default**, **soft palette — NOT hard black, NOT hard red**, with a subtle
  **weirwood-tree background** (tasteful, low-contrast, behind content). Muted dusty-red accent, bone text. Build
  styling so the theme is **easy to swap** (one tokens/CSS-variables layer).
- **Featured landing exchange:** site opens with the **Tywin chain** pre-loaded (poisoned hairnet → … → patricide,
  ending on *"Lord Tywin Lannister did not, in the end, shit gold."* `asos-tyrion-11:269`) — Matt finds it funny +
  it's the wow. Seed example prompts in the input.
- **"Chain walked" panel — make it ROBUST:** show the **typed edges** (CAUSES / ENABLES / MOTIVATES labels on the
  connectors), not just node chips; allow drilling into a link for its evidence quote + cite. This is the
  proof-of-realness. The chains can be enriched with much more detail per link (each beat has its own quotes/roles).
- **About page (SECONDARY):** a README-style "what is the Weirwood Network" page; build after the chat works.
- **Copyright/publishing: CLOSED (S170) — do NOT re-raise.** Private repo, book text bundles as-is, one optional
  footer line is the only artifact. If you catch yourself drafting a "should we expose the text" question, stop.
- **Model:** open — smoke-test the Bloodraven persona on `claude-sonnet-4-6` (cost) vs `claude-opus-4-8` (prose);
  use adaptive thinking; stream the reply. Add a per-day/IP cost cap in the function.

## Your job
1. Read STEP 0 (esp. the sharpened design + §0/§9). 2. **Do the §8 step-0 spike FIRST (the gate):** (a) prove a
streaming multi-tool turn fits the Netlify runtime — Edge/Deno vs sync function (Background Functions can't stream);
(b) smoke-test the Bloodraven persona on Sonnet 4.6 vs Opus 4.8 with a stubbed multi-tool turn, decide the model
(run this on the subscription locally — §4 — to avoid API $). 3. Resolve the rest of the §9 open questions with Matt.
4. Build
per design §8: build-time `--json` export (NOT python shell-out) → retrieval tools (incl. `search_chapters`/
`read_passage`, with structured typed-edge output + bounded inputs) → the function (tool-runner loop + persona +
streaming + a global spend ceiling) → the themeable chat page (static featured Tywin exchange + typed-edge receipts
+ tool-gathering trace) → local run → Netlify deploy. Ship the curated-quotes MVP slice first; live search is the
fast-follow (still the v1 goal). 5. **Confirm with Matt before committing to the architecture and before any deploy.**

## DO NOT
re-fetch the wiki · run Pass-1 extractions · mint enrichment edges/nodes (this is app work, not graph work) ·
treat the old `chat-ui-architecture.md` as the plan · **re-raise copyright/publishing as a concern or open question
(SETTLED S170 — private repo, book text bundles as-is; see `project_publish_settled`)** · auto-run `/endsession`.

## The Claude API
Use the `claude-api` skill for all API/SDK/model details (model IDs, tool-runner loop, streaming, pricing) — do not
code the Claude calls from memory.
