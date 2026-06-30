---
session: 176
title: Chat-UI alpha — DESIGN evaluation against live conversations
date: 2026-06-30
track: meta (graph/meta)
model: Opus 4.8 (handoff recommended Sonnet 4.6; ran on session Opus)
api_spend: small — live Sonnet 4.6 turns for design iteration (a handful of cents); no graph writes
---

# Session 176 — Chat-UI alpha: design evaluation

First fresh-context **design** session after the four S171–S174 build chunks + the S175
placeholder removal. The chat-UI alpha is code-complete and runs LIVE locally (Deno dev
server `web/scripts/dev.ts` + key in `web/.env`). Goal: evaluate and polish the design
against **real live conversations**, working from Matt's notes.

## How it ran (the loop)
Stood the live server up under the **preview MCP** (added a `weirwood-live` config to
`.claude/launch.json`, autoPort, default model Sonnet 4.6 for cheap iteration). Drove real
queries through the browser and via `curl` to the Edge function, read the actual prose +
the rendered chain, and iterated. The session was heavily interactive — Matt steered in
real time, including several mid-flight reversals that reshaped the plan.

## What Matt surfaced (in order)
1. **Persona switching.** Wants to switch personas; a neutral "Loremaster" (zero
   personality) alongside the characterful "Bloodraven". Discovered the live backend already
   speaks **Bloodraven**, while the page chrome labelled it "the loremaster" — a mismatch.
2. **"See the edges" / show off the graph.** Built three `show_widget` mockups (A annotated
   spine · B graph map · C node dossier). Matt picked **A** (annotated spine) for the chain
   and **C** (node dossier) for the click-through.
3. **The chain panel was a dump.** A live run revealed the real problem: `walk_chain` with
   `full=true` did an **uncapped** transitive walk → ~50 edges / ~110 node-rows, nodes
   repeating ("Siege of Riverrun" ×6), ENABLES noise, BFS order, tangents (Jon stabbed, Pink
   letter). Meanwhile the **prose answer was good**. So the answer distilled a clean spine;
   the panel showed the undistilled mess.
4. **Prose first; quotes in the prose.** "Prose should come first on any screen." Quotes
   inside the prose must be well-chosen and in-context — the model sometimes dumped an
   out-of-context block quote ("…tywin lannister did not shit gold"). The Claude-Code chats
   he'd had were much better.
5. **Keep the detail, display it differently.** A key reversal: he does NOT want the chain
   hard-pruned to 8 links — he wants the rich detail KEPT, shown better; nodes hoverable;
   every node interactive (not just the one the model read).
6. **About page.** Page should open straight to chat; move the "what is this" blurb to its
   own About view.

## The advisory board (Matt's suggestion)
Fanned out **4 design advisors** (Agent tool, parallel) on the open question of how to
display the rich causal chain + how prose/quotes/voice relate. Three returned (the 4th,
interaction-design, hung without reporting — its lens was covered by the others). They
**converged**:
- **Dedup at the data layer** (each node once; many edges → multiple connectors + a `·N`
  degree badge) — kills the ×6 repeat.
- **Progressive disclosure** — clean CAUSES/TRIGGERS/MOTIVATES spine by default; the full
  ENABLES web dimmed behind one **"show preconditions (+N)"** toggle. THIS is how the detail
  is kept without the wall.
- **Vertical layered spine, not boxes-and-arrows** (arrows die at 320px / mobile).
- **Hover = peek, click = full node dossier; mobile (no hover) = tap-to-expand accordion.**
- **Bloodraven as the DEFAULT voice** (2 of 3 said so explicitly) — a characterful voice
  *forces narrative cohesion*, so a quote only lands when the throughline earns it; flat
  "just answer" prose has no such pressure and staples evidence on afterward (that stapling
  IS the out-of-context dump). Flat Loremaster, if shipped, inherits the SAME evidence
  discipline ("neutral register", not "no rules").
- **The marquee move:** click a causal claim in the prose → its exact edge lights up in the
  chain with its citation. (Stretch.)

This **overrode Matt's earlier lean** toward Loremaster-default; he accepted: **Bloodraven
default**, build order green-lit.

## What shipped this session
- **Prose quality FIXED** — an "Evidence discipline" block in the system prompt (setup-then-
  quote, one quote/beat, ≤~20 words, no standalone block-quotes, quote-must-do-a-job),
  fixed the "Ask your questions…" opener leaking into answers, and added a mandatory-walk
  rule for causal questions. Verified by curl: in-context set-up quotes, no dumps, walk fires.
- **Backend walk tamed + enriched** — `walkChain` depth-capped (2) + link cap (12),
  causal-only default, and links now carry `source_name/target_name/source_type/target_type`
  (slug→name). Tests updated. Verified: "what led to the Red Wedding" → 8 clean named links.
- **Frontend** — re-rendered the chain to the Mockup-A annotated spine (node cards + type +
  inline edge evidence + `cleanQuote()` stripping `(wiki:…)` markup + repeat-slim + bounded
  scroll); fixed the failed-turn-wipes-chain bug (`lastGoodChain` persistence).
- **About page** — page opens to chat; blurb → toggled About view. Verified.
- **Prose-first on mobile** + retired the full-width Band-on-top (it sat above the prose).
- **Backdrop opacity** 0.06 → 0.11. **Dev caching** fixed (no-store + `?v=` asset versioning).

## Deferred to Session 177 (the chain-display REBUILD, green-lit)
Dedup spine + "show preconditions (+N)" toggle (keep the detail, progressive) → hover-peek +
click-dossier on every node (add a `/api/node` lookup) → stretch prose↔edge highlight.
Full spec + state in `progress/continue-prompts/2026-06-30-chat-ui-design.md`.

## Notes / gotchas
- **Model variance:** Sonnet sometimes skips `walk_chain` and answers from memory → empty
  chain panel. The mandate-walk prompt rule mitigates; `curl` (single message) walks
  reliably, the browser carries history that biases toward answering from memory.
- The interim Mockup-A spine rendering is in the tree but NOT visually verified end-to-end
  (variance kept the browser from walking); the Phase-2 rebuild replaces most of it anyway.
- All S176 work is **uncommitted in the working tree** at the time of writing this detail
  (committed at endsession).
