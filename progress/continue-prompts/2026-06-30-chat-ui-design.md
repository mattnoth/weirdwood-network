# SESSION 175 — Chat-UI alpha: DESIGN polish + review (fresh-context session) · graph/meta track

> **This is Session 175.** Stamp your worklog entry `### Session 175` (meta track, `worklog.md`) at endsession.
>
> The chat-UI alpha BUILD is **code-complete + dry-validated** (Foundation S171 ·
> retrieval-core S172 · function S173 · front-end S174). S174 ended with a live
> design review of "the chain walked" panel; Matt wants to continue DESIGN work in
> a **fresh session** to keep context clean. **Recommended model:** Sonnet 4.6
> (static HTML/CSS/JS design polish — no new backend reasoning).

## Read first
- `web/public/index.html` + `app.css` + `app.js` ← what you're polishing.
- `web/public/theme/tokens.css` ← the ONE-FILE theme layer; keep styling token-driven.
- `working/chat-ui/alpha-design.md` §5 (persona/UI) + §6 (look/theme + receipts).
- worklog `### Session 174` ← the build + the design-review state below.

## Where it stands (don't redo)
- **"The chain walked" panel** is the centerpiece (Matt: loves it, DON'T gut it).
  Nodes are **deduped** (each appears once, joined by its typed edge).
- **Two layouts, live-toggleable** (Band/Spine toggle in the chain header, choice
  persists in `localStorage`):
  - **Band** — full-width horizontal flow; click node → quotes panel, click edge →
    evidence line. (Matt's horizontal lean.)
  - **Spine** — vertical rail in the right side panel; click-to-expand inline.
- One renderer drives featured + live; receipts come from a per-turn model so a
  layout flip just re-reads it. SSE client + failure-mode UX done. All dry-validated.
- **Run the preview:** `cd web/public && python3 -m http.server 8766` (or use the
  Launch preview). Featured Tywin exchange renders with zero API spend.

## Open design items (resolve with Matt)
1. **Default chain layout** — Band (portfolio "wow") vs Spine (density) vs keep the toggle.
2. **Matt's remaining review notes** — he said "some reviews I want to make"; he had
   only given the horizontal direction when S174 ended. ASK for the rest first.
3. **Live slug→name** — on LIVE answers, chain node labels come from slugs (read a
   touch plain, e.g. "Assassination of tywin lannister"). Featured uses proper names.
   Optional: resolve slug→name (or title-case) for live.
4. **Weirwood backdrop opacity** — currently `--weirwood-opacity: 0.06` (very faint);
   Matt may want a nudge to ~0.10–0.12. One-line token change.
5. Anything else Matt raises — this is his design-review session.

## LOCKED — do NOT reopen
Netlify Edge (Deno/TS) · model `claude-opus-4-8` · Option A tool-use · curated-MVP ·
repo PRIVATE → Netlify (publishing CLOSED) · the SSE contract (render what the
function emits) · no mocked AI prose.

## After design is settled — the two GATED ship steps (real API $ — Matt's go-ahead)
1. **Capture a REAL featured transcript** to replace `app.js`
   `FEATURED_PLACEHOLDER_ANSWER` (a design fixture). Matt's lean: pre-generate REAL
   & rotate among several seed questions. Run the live fn (`netlify dev`), capture
   the genuine model answer + real receipts, bake in. NO hand-written prose.
2. **Deploy** — `netlify dev` proof → deploy private repo to Netlify + set
   `ANTHROPIC_API_KEY` in Netlify env. On success, update memory
   `project_real_goal_graph_for_agents` with the live URL.

## DO NOT
run live API / `netlify dev` / deploy without Matt's go-ahead · mint graph
edges/nodes · auto-run `/endsession`.

## After ship — PARKED graph tracks resume
granular-dip planning (`working/granular-dip-plan.md`, D2 opener) → arc/character
dips. D&E Pass-1 + SIFT remain parked.
