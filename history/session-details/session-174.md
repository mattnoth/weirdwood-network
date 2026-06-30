---
session: 174
title: Chat-UI alpha — front-end chunk (the last build chunk) + design review
date: 2026-06-29
track: meta
model: Opus 4.8
graph_writes: none
api_spend: none (all validation dry — static-server preview + simulated SSE)
---

# Session 174 — Chat-UI front-end chunk + live design review

The 4th and final build chunk of the chat-UI alpha: the browser UI that talks to
the S173 Edge function. Built against the locked SSE contract, dry-validated with
zero API spend, then turned into a live design-review session with Matt on the
"chain walked" panel.

## What got built

`web/public/` — vanilla, framework-free, token-driven:
- `index.html` — header + out-of-character "How it works" framing (design §5,
  required so a lore-blind visitor understands the never-announces persona), chat
  thread, full-width chain band, sticky receipts column, composer + example chips,
  footer, subtle weirwood backdrop.
- `app.css` — every colour/font/size reads `theme/tokens.css`; zero hard-coded
  values, so the whole look still swaps from the one token file.
- `app.js` — ES module: SSE client, the shared renderers, failure-mode UX.

## The load-bearing architecture call — one renderer, two sources

Matt asked, mid-build, whether the static Tywin exchange was "a way to design how
chats would look dynamically." Yes — and that's the whole point. There is ONE set
of render atoms (typed-edge link rows, node cards, the chain sequence builder);
the only difference between the featured showpiece and a live answer is the data
source (pre-baked `featured-tywin.json` vs the live SSE stream). So the static
render IS the design fixture for the dynamic chat — the entire visual design was
built and validated against the showpiece with zero API spend, and live answers
inherit it for free.

## Three design decisions (Matt)

1. **No mocked AI prose (firm).** Matt vetoed my plan to hand-author a Bloodraven
   narration for the featured answer. The featured chain/beats/quotes are all REAL
   (graph-walked); only the answer *prose* was missing, and hand-writing it is
   exactly the mock he doesn't want. Resolution: the answer is a clearly-marked
   design-fixture placeholder (`FEATURED_PLACEHOLDER_ANSWER`) that MUST be replaced
   with a CAPTURED REAL transcript before the public deploy. Matt's lean for the
   featured content: pre-generate real & rotate among several seed questions (zero
   per-visitor cost, real model output, no abuse exposure on the showpiece). This
   blocked briefly — Matt's call was "stop blocking, use the fixture to design,
   swap in real before ship."

2. **Weirwood backdrop = subtle.** I hand-authored a stylized weirwood SVG (pale
   split trunk, carved weeping face, blood-red five-lobed canopy) to prove the art
   could be done by hand (it can — stylized, not photoreal; a traced photo would
   only add realism that's lost at backdrop opacity). Matt chose subtle backdrop
   (~6% soft-light) over visible-motif or hero. Build UI first, art last.

3. **"The chain walked" — keep it, go horizontal.** Matt loves the receipts panel,
   flagged that horizontal might read easier. The real readability bug he spotted:
   the original per-link rows repeated the shared node (target of link N = source
   of link N+1) down the column. Fix: dedup the nodes (each appears once, joined
   by its typed edge). He asked to see both layouts, so:
   - **Band** — full-width horizontal flow; click node → quotes panel, click edge →
     evidence line. (His horizontal lean; portfolio "wow".)
   - **Spine** — vertical rail in the side panel, click-to-expand inline. (Density;
     answer + chain side-by-side.)
   Live toggle in the chain header, choice persists in `localStorage`. The receipts
   feed was refactored into a per-turn model so a layout flip just re-reads it.

## Validation (all dry, no API)

Static `python3 -m http.server` + the Launch-preview browser:
- Featured render: 7-link deduped chain + 8 beat cards; node-click → quotes;
  edge-click → evidence + cite + tier.
- A SIMULATED live turn (fetch override feeding a canned SSE stream): token deltas
  accumulate into the streaming bubble, receipts rebuild from the turn model
  (resolve + read_node + walk_chain), streaming cursor clears on `done`.
- All failure-mode states render distinct UI (no-grounding, loop-bound-hit,
  unverified-cites, api-error, cost-cap-tripped) + plain `error`.
- Both Band and Spine verified; zero console errors throughout.

## Data path note

`web/data/` is read only by the Edge function and isn't under the publish dir, so
the browser can't fetch it. The featured exchange is served at
`/data/featured-tywin.json`; `netlify.toml`'s build command now `cp`s it into the
gitignored `web/public/data/` at deploy.

## Open / deferred

- Matt wants to continue DESIGN in a fresh session (keep context clean): pick a
  default chain layout (Band vs Spine vs keep toggle), his remaining review notes,
  live slug→name prettification (live chain labels read plain), backdrop opacity.
  Continue prompt: `progress/continue-prompts/2026-06-30-chat-ui-design.md`.
- Two gated ship steps (real API $, Matt's go-ahead): capture the real featured
  transcript; `netlify dev` proof → deploy private repo to Netlify + the env var.
- Live `search_chapters` / `read_passage` remain the fast-follow.

This completes the chat-UI alpha BUILD (code). Foundation S171 → retrieval-core
S172 → function S173 → front-end S174.
