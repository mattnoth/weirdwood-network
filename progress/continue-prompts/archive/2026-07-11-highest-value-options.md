# SESSION 211 — Present highest-value options, then execute one

> **This is Session 211.** Stamp your worklog entry `### Session 211` at endsession.
> **Model:** **Fable 5** (`claude-fable-5`) — Matt chose Fable for this session.
> **Your job this session (Matt's explicit instruction):** at the **START of the
> conversation, PRESENT all the available highest-value options** below as a ranked
> menu (value · effort · demo-wow · risk for each). Then **Matt picks ONE and you work
> through it together.** Do NOT start executing before he picks. If the pick is a big
> track, scope its own plan/continue-prompt before running.

## First steps
Read `worklog.md` (Current State — the STATUS block + Session Log S206–S210), `working/todos.md`
(the **S210 advisory-board follow-ups** block near the top + § Small Fixes edge items + the
node-type promotion item, line ~293–295), `reference/architecture.md` (edge/type vocab), and
`history/session-details/session-210.md`. The chat-UI is live at
https://weirwood-network.netlify.app (Netlify Edge/Deno, Opus; deploys are MANUAL — see `DEPLOY.md`).

## Where things stand (S210 close)
The Fire & Blood / review-bucket track is fully CLOSED. S210 deployed the S205–S209 backlog,
stripped the "from the AWOIAF wiki" boilerplate from 6,481 nodes (drop-everywhere), and — after
a 4-advisor board review — shipped 2 fixes (dossier "From the wiki" → "Overview" relabel; a
corpus-golden staleness guard). Graph: ~8,971 nodes / 26,352 edges. Suites green (pytest 1458 /
deno 100). No live graph track — this session picks the next one.

## The options to present (ranked; adjust with your own read)

**1. Edge-vocab retrofit "Part B" — targeted, precision-first.** `[CONFIRMED wanted, S207;
todos line 295]` Quote-grounded *add/retype* of newer edge types where main-series + F&B text
supports them — **SUSPECTED_OF (the whodunit headline), KNIGHTED_BY/BESTOWS_KNIGHTHOOD_ON,
reification role edges**. Machine: `mint_enrichment.py` → Haiku fresh-verify → finalize
(the enrichment-dip pattern). *Demo-wow:* the board's portfolio advisor ranked this #1 — more
of a reviewer's natural questions (esp. whodunits) land on rich, cited, typed answers instead of
flat neighbor lists. **Honest nuance (verified S210):** the flashy "chain walked" spine renders
ONLY on causal edges (CAUSES/TRIGGERS/MOTIVATES/ENABLES = just **1.8%** of edges, 474/26,352);
Part B's named types are NOT causal, so the win is richer *typed receipts + better analytical
answers*, not literally "more spine." Lower volume, high quality. *Model-fit:* Sonnet proposers
+ Haiku verify. Scope tight (start with SUSPECTED_OF + roles).

**2. Stage 4 staged candidate-pool bulk typing — HIGH VOLUME.** The distinct high-volume edge
effort (this is the one Matt asked about). Stage 4 shipped the canonical edge core (5,219
book-pass1 edges) but left **~32,194 untyped candidate rows STAGED** (Events / Info / Food /
Dialogue pools). Bulk-LLM edge-typing would classify these into thousands of new typed edges.
**Big caveat:** the **Events sub-pool already RAN (S80) and was SHELVED** — 16,502 candidates →
1,617 typed, but it **failed the drift/precision gate (NO-GO borderline, ~56% vs 70%)** and was
NOT merged. Hard rule: **"DO NOT run the ~$270 Events bulk blind — fold in the precision
precursors first."** So this is high-volume but quality-risky and gated; it needs the precision
work before another bulk run. *Model-fit:* Haiku bulk + mandatory drift audit. Detail:
`working/audits/events-haiku-bulk-2026-05-29/`, `working/runbooks/stage4-events-haiku-bulk.md`.

**3. Node-type promotion sweep — cheap, mostly deterministic.** `[MED, todos line 293]` S207
Part A was conservative (ambiguous nodes → `event.incident`; some real events sit under
`incident`/`battle`). Promote to the sanctioned leaf where the node genuinely is one
(`death-of-*`→`event.death`, `capture-of-*`→`event.capture`, etc.; judgment for the rest).
*Board's integrity + engineering advisors said do this FIRST* (bounded, low-risk, closes the
Part A tail) before a scoped Part B. Grep for hardcoded `event.incident` filters before renaming
(mirror the S207 war-mistype fanout check). Low effort.

**4. Board-deferred chat-UI polish (low effort, portfolio-visible).** (a) **search-card leak
path** — `app.js searchCard()` renders identity-search hits without the `isWikiBoilerplate()`
gate; a future emitter regression could surface boilerplate in a live "passages consulted"
transcript. (b) **thin-node blank dossiers** — ~1,169 fully-thin nodes now open to dead-end
cards (empty identity, no quotes, no sections); add a dimmed/non-clickable "thin node" chip
treatment. Both in the S210 board-follow-ups todo block.

**5. (Decided — mention only)** The 120 analytical "the wiki" provenance notes = **leave**
(board consensus: they're the Tier-2 confidence signal; 45/58 are under `## Notes`, not shown in
the dossier). The 2 provenance/build wiki-notes = leave. Don't spend a session here.

**6. (Lower / grab-bag Small Fixes)** dup-merge hygiene (Black Walder Frey, Fist-of-the-First-Men,
Fords-of-the-Trident shells), `valyrian-steel`→`object.material` + HoBaW→`place.location` retypes
(unblock `MADE_OF` edges), stray `containers:[jon]` tag cleanup, family `generationCounts`
tolerance. See § Small Fixes.

## How to run this session
1. Present options 1–6 (a tight ranked menu with value/effort/wow/risk — not walls of text).
2. Matt picks one. If he wants your recommendation: the board split between **1 (Part B,
   demo-wow)** and **3 (promotion sweep, cheap-first)** — 3-then-1 is the low-risk sequence.
3. Execute the pick. If it's a big track (1 or 2), scope a plan + its own continue prompt first;
   confirm before any spend or graph mutation (`feedback_no_graph_mutation_without_goahead`,
   `feedback_no_extraction_without_asking`).

## DO NOT
- Do NOT run the Stage 4 Events bulk (or any bulk edge-typing) blind — it failed the precision
  gate; precision precursors + a drift audit are mandatory first.
- Do NOT start executing before Matt picks an option.
- Do NOT mutate `graph/` or deploy without Matt's explicit go. Do NOT auto-run `/endsession`.
