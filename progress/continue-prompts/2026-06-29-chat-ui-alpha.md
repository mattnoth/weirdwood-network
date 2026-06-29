# SESSION 170 — Weirwood chat-UI alpha (build track)

> **This is Session 170.** If you log to `worklog.md`, stamp your entry `### Session 170` (meta track). (This is app
> work, a new sub-track — the number is for the worklog stamp; not a graph-enrichment dip.)
> **Recommended model:** Opus 4.8 (design/architecture + build judgment; Sonnet 4.6 fine for mechanical scaffolding).
> **This is a fresh-context handoff.** S168 scoped this with Matt; **S169 ran a 6-lens adversarial design review and
> folded the findings into `working/chat-ui/alpha-design.md`** (it did NOT build anything). The design is now
> decision→build-ready — read it fresh; it carries a §0 status table and the review corrections.
> **Matt's explicit instruction: a *fresh* session builds this — not the scoping/review sessions.** That's you.

## What this is
Build a deployable **ASOIAF loremaster chat** for Matt's **job-application portfolio** (linkable from his profile):
a visitor asks a question, **Bloodraven** answers in-character, grounded in the Weirwood Network graph, dropping
**real book quotes with chapter citations**, and showing the **typed-edge chain it walked** as receipts. The wow is
that it doesn't bluff and can **find quotes live by reading the chapter text**, not just curated node quotes.

## STEP 0 — read first (the design is already written)
- **`working/chat-ui/alpha-design.md`** ← the full working design (corpus, retrieval architecture options, model
  connection, persona, theme, build plan, open questions). START HERE. **S169 review folded in:** §0 status table;
  §7 deploy-boundary OPEN DECISION (the book text is git-TRACKED, NOT gitignored — decide before any public move);
  a new §8 **step-0 runtime+persona spike** that GATES the build; structured typed-edge receipts + no-chain fallback;
  prompt-caching + a global daily spend ceiling; silent-turn/empty/error UX states; expanded §9 opens.
  **Begin with the §8 step-0 spike — do not build the export/tools until runtime + model are decided.**
- `working/chat-ui/bloodraven-persona-notes.md` — the voice (use as-is per Matt; bake into the system prompt).
- `working/demo-asoiaf-loremaster.md` — the PROVEN retrieval recipe this productizes (run it to feel the target).
- memory `project_real_goal_graph_for_agents` (chat-UI alpha is a live track), `project_arc_enrichment_track`
  (the chains keep getting richer), `feedback_show_commands`, `feedback_no_extraction_without_asking`.
- `history/archive/sketches/chat-ui-architecture.md` — the OLD heavy vision; mine for ideas, do NOT treat as the plan.

## Matt's stated preferences (from S168 — confirm before locking, nothing is nailed down)
- **Host:** Netlify (mattnoth.com is already there); serverless function holds `ANTHROPIC_API_KEY` server-side,
  browser never sees it. Standalone deploy first; fold into mattnoth.com later.
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
- **Copyright:** not a blocker (not advertised; wiki quotes the books everywhere). One footer disclaimer line only.
- **Model:** open — smoke-test the Bloodraven persona on `claude-sonnet-4-6` (cost) vs `claude-opus-4-8` (prose);
  use adaptive thinking; stream the reply. Add a per-day/IP cost cap in the function.

## Your job
1. Read STEP 0 (esp. the sharpened design + §0/§9). 2. **Do the §8 step-0 spike FIRST (the gate):** (a) prove a
streaming multi-tool turn fits the Netlify runtime — Edge/Deno vs sync function (Background Functions can't stream);
(b) smoke-test the Bloodraven persona on Sonnet 4.6 vs Opus 4.8 over the API with a stubbed multi-tool turn, decide
the model; (c) decide the §7 deploy text-boundary. 3. Resolve the rest of the §9 open questions with Matt. 4. Build
per design §8: build-time `--json` export (NOT python shell-out) → retrieval tools (incl. `search_chapters`/
`read_passage`, with structured typed-edge output + bounded inputs) → the function (tool-runner loop + persona +
streaming + a global spend ceiling) → the themeable chat page (static featured Tywin exchange + typed-edge receipts
+ tool-gathering trace) → local run → Netlify deploy. Ship the curated-quotes MVP slice first; live search is the
fast-follow (still the v1 goal). 5. **Confirm with Matt before committing to the architecture and before any deploy.**

## DO NOT
re-fetch the wiki · run Pass-1 extractions · mint enrichment edges/nodes (this is app work, not graph work) ·
treat the old `chat-ui-architecture.md` as the plan · over-engineer the copyright posture · push the book text to a
PUBLIC repo/artifact (it is currently git-TRACKED and the repo is private — resolve the §7 deploy-boundary decision
BEFORE any public move; the old "it's gitignored" claim was false and is corrected in the design) · auto-run `/endsession`.

## The Claude API
Use the `claude-api` skill for all API/SDK/model details (model IDs, tool-runner loop, streaming, pricing) — do not
code the Claude calls from memory.
