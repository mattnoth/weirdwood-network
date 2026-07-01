---
session: 177
title: Chat-UI alpha — chain-display REBUILD + unified quote system
date: 2026-06-30
track: meta (chat-UI alpha)
model: Opus 4.8 (handoff recommended Sonnet 4.6)
api_spend: small (live Sonnet 4.6 curl/preview verification turns, a few cents)
graph_writes: none
harvest_queue: 0
---

# Session 177 — Chat-UI alpha: chain-display REBUILD + unified quote system

## Context & framing

This session redid a task Sonnet had botched in a prior attempt. Root cause of that
botch (Sonnet's own note, worth keeping): the Edit tool introduced **curly/smart
Unicode quotes** (`"` / `"`) into JS/TS source; Deno's parser choked on them as
`Unexpected character '"'`. Matt reverted that attempt and re-ran on Opus. Lesson
adopted here: write JS/TS with **ASCII delimiters only**, and `deno check` /
`node --check` **before** every browser reload. That discipline caught a real bug
pre-runtime this session (a stray backtick inside the backtick-delimited
`SYSTEM_PROMPT`) — the checker flagged it instead of a silent breakage.

Starting state: S176 had committed the annotated-spine frontend, About page,
depth-capped `walkChain`, and Bloodraven-as-default. An earlier Sonnet S177 attempt
had left **uncommitted** backend edits (an `enables` array in `graph.ts`/`types.ts`)
and an untracked `node.ts` — those survived the revert (revert only touched tracked
`web/public/` files). I verified those backend edits rather than redoing them, but
they **broke** the committed `graph_test.ts` (the `full:true` test), which I fixed.

## Green-lit build (from the continue prompt)

1. Dedup spine + "show preconditions (+N)" toggle (keep detail, progressive).
2. Hover-peek + click-dossier on every node (add `/api/node`).
3. Stretch: prose↔edge highlight (deferred, as the prompt directed).

### Calibration first
Probed the real bundle before setting caps: Red Wedding walk = 8 causal links / 9
spine nodes / **8 enables**; Tywin = 2 enables; Robert's Rebellion / Sack = 0. The
old "Siege of Riverrun ×6 wall" was already gone (S176's depth-2 + causal-only +
12-cap). So the rebuild's real value was the **ENABLES precondition toggle** and
**node dossiers**, not dedup-crisis-fixing. Set `MAX_ENABLES=24` (generous; measured ≤8).

### Backend
`walkChain` now returns the causal spine + a separate capped `enables[]` (ENABLES
edges whose target is a spine node, deduped) in ONE round-trip. **Retired the `full`
param** entirely — the design's explicit reconcile: the UI fetches the fuller ENABLES
set for the toggle; the model always narrates the clean spine (no second round-trip,
no flood). Touched `graph.ts`, `types.ts`, `mod.ts` (signature), `agent.ts` (tool def
+ dispatch + prompt + `harvestResult` now allowlists `enables` cites), `graph_test.ts`
(obsolete `full` test → `enables`-contract test). 22/22 lib tests green.

### Frontend
Retired the band layout; one deduped vertical spine in the rail with `·N` degree
badges and a sticky, default-collapsed "show preconditions (+N)" toggle (ENABLES web
dimmed/indented). Every node is a button → opens a **dossier** (a live `/api/node`
lookup — new keyless edge function `node.ts`, wired into `dev.ts` + `netlify.toml`).
Desktop hover lights a node's edges. Mobile = prose-first, dossier-as-modal.

### Two latent S176 bugs caught during verification
- `el()` only flattened children one level → a nested-array child (e.g. `resolveCard`'s
  mapped list) stringified to `[object HTMLDivElement]`. Fixed with `.flat(Infinity)`.
- `.dossier-overlay { display:flex }` (author CSS) beat the `[hidden]` attribute's
  UA `display:none`, so an empty overlay's backdrop dimmed the whole page even when
  "hidden". Fixed with `.dossier-overlay[hidden] { display:none }`.

## The unified quote system (Matt-driven, mid-session)

Matt reacted to the dossier quotes: *"that's exactly how I want quotes displayed
everywhere, in prose."* Three asks: (a) source = just the chapter ("ASOS Arya 11"),
(b) "second quote has no author" → degrade gracefully, (c) prose styling like the
event. One fork I clarified with an AskUserQuestion: does "in prose" mean restyle
**Bloodraven's spoken answer** quotes too? Answer: **yes** (relaxing the "no cites in
his voice" rule for quotes only).

Design landed:
- `prettyCite(token)` → clean chapter label; folded into `cleanQuote` so baked-in
  file-paths, wiki markup, backticks, and internal `book-cite overlay`/`harvest row`
  provenance tails all clean up wherever a quote renders.
- One shared `bookQuote(text, speaker, source)` in the answer prose, chain edges,
  preconditions, and dossier. Degrades: missing speaker or source drops out.
- Bloodraven wraps spoken quotes in a `[[q|text|speaker|source]]` marker (SYSTEM_PROMPT
  change). A **streaming-safe** `renderProse` (full-buffer re-parse each token; hides an
  incomplete trailing marker) turns them into styled pull-quotes. The existing cite-gate
  validates the in-prose sources — `unverifiedCites=[]` confirmed. **Backward-compatible:**
  no markers → plain prose (observed on a paraphrased Robert's Rebellion answer).
- Iterated on real data: `dirty=0` across 17 Red Wedding quotes; `stripEdgeQuotes` killed
  the double-wrapped `"”` (Matt's "Seaworth" trailing-quote); de-duped source when a quote
  baked the chapter into BOTH its attribution and cite.

## Persona polish

- Forbade "chain"/"link" in Bloodraven's prose (those are the interface's words) and the
  counting-formula opener ("Three links in the chain"). Now leads with substance.
- **Markdown handling — asked a cold subagent.** The model kept writing `**bold**` section
  headers rendering as literal asterisks. Options: render the bold vs. drop it. The cold
  subagent argued **drop it** (Option 2), decisively: bold headers are an AI-assistant tic
  that clashes with the austere record-keeper voice; the styled pull-quotes already supply
  the visual rhythm, so headers add a second competing structure (listicle feel); and
  keeping the renderer markdown-STRICT is itself useful (stray markdown shows as an obvious
  blemish in testing, not silently prettified). Enforced as a HARD prompt rule. Verified:
  no `**`, no headers, no lists, no chain/link.

## Verification

curl (single-message, reliable walk) + preview MCP throughout. Confirmed live: walk fires,
8 enables flow through with names/refs, spine renders with degree badges, preconditions
toggle reveals 8 rows, dossier opens via `/api/node` (17 quotes, no leaks), hover-highlight
works, mobile prose-first, answer prose shows styled sourced pull-quotes, no raw markers, no
double-quote artifact. Final gate: 22/22 lib tests, all edge fns + dev.ts type-check,
`node --check public/app.js` clean.

## What surfaced for next session (refinements)

A live "Show me the Targaryen family tree from Aegon the Conqueror" query exposed:
1. Genealogy queries hit `loop-bound-hit` (model fans out via `neighbors`, exhausts
   `MAX_TOOL_ITERATIONS`; no tree-traversal mode) → thin/empty answer.
2. Fuzzy resolve on marquee names ("Aegon the Conqueror" → fuzzy aegon-i/ii/iii, not an
   exact hit on `aegon-i-targaryen`; "Targaryen dynasty" same) — alias-map gaps.
3. Loop-bound UX — answer area looked empty above the status line.
4. (Bigger) a real family-tree view — genealogy is a distinct shape from the causal spine.
Plus Matt's own design refinements (TBD — he'll bring them). → continue prompt
`2026-07-01-chat-ui-refinements.md`.

## Not done (intentional)
- Stretch prose↔edge highlight — deferred per the continue prompt.
- Deploy — still gated on Matt's go-ahead.
