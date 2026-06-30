# Chat-UI alpha — SHIP (the two Matt-gated live steps) · graph/meta track

> The chat-UI alpha BUILD is **code-complete + dry-validated** (Foundation S171 ·
> retrieval-core S172 · function S173 · front-end S174). Both remaining steps
> spend **real API $**, so they are **GATED on Matt's explicit go-ahead** in-session
> (feedback `no-extraction-without-asking`). Stamp the worklog `### Session 175`
> (meta track, `worklog.md`). **Recommended model:** Sonnet 4.6 (operational, no new reasoning).

## Preconditions (verify, don't redo)
- `cd web && deno task test` → 27 green; `deno task check:fn` → clean (S173).
- `web/data/` bundle present (`python3 scripts/build-chat-export.py` if not).
- Front-end serves: the static Tywin exchange + a populated receipts panel render
  with zero console errors (S174 dry-validated via the Launch preview).

## STEP 1 — capture a REAL featured transcript (replaces the placeholder)
**Why:** `web/public/app.js` `FEATURED_PLACEHOLDER_ANSWER` is a DESIGN FIXTURE.
Matt's rule is **no mocked AI prose** — the shipped featured answer must be genuine
model output. Matt's lean: **pre-generate REAL & rotate** among several seed
questions (zero per-visitor cost, no abuse exposure on the showpiece).
- Run the live function (`netlify dev`, real API $) over the seed question(s)
  ("Who killed Tywin Lannister, and why?" + any others Matt picks), capture the
  genuine SSE transcript (the model's prose answer + the real `receipt` events).
- Bake each captured transcript into the featured data the page rotates through;
  swap the placeholder render in `renderFeatured()` for the captured answer.
- Keep the architecture: ONE renderer serves featured + live (don't fork it).

## STEP 2 — deploy (private repo → Netlify)
- Confirm `netlify dev` end-to-end: landing shows the (now real) featured exchange;
  a typed question streams a Bloodraven answer with a populated receipts panel.
- Deploy the private repo to Netlify; set **`ANTHROPIC_API_KEY`** in Netlify env
  (deployed = metered key; local = OAuth profile / plan quota — design §4).
- Verify the global daily spend cap (Netlify Blobs `spend-YYYY-MM-DD`) is live.
- On success: update memory `project_real_goal_graph_for_agents` with the live URL.

## DO NOT
run any live API call / `netlify dev` / deploy without Matt's go-ahead in the turn ·
reopen runtime/model/scope/publishing decisions · change the SSE contract ·
hand-write the featured answer (no mocked AI prose) · mint graph edges/nodes ·
auto-run `/endsession`.

## After ship
This closes the chat-UI alpha track. The PARKED graph tracks resume:
granular-dip planning (`working/granular-dip-plan.md`, D2 opener), then the
arc/character dips. D&E Pass-1 + SIFT remain parked.
