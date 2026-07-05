# SESSION 194 — Chat-UI side-window receipts + node UX (runs AFTER the quote-minting session)

> **This is Session 194** — it runs AFTER `2026-07-05-quote-minting-dossier-substance.md`
> (Matt-sequenced S192: fill the dossiers first, then make them reachable). Stamp your
> worklog entry accordingly; renumber via `worklog.md` as always.
> Track picked S192: Matt's own sequencing ("we can work on the display of the side
> window after [the deploy]") + his S192 design steer (chain-walker consistency, node
> modals, prose linking, "the styling needs a big boost" — REAFFIRMED end-of-S192:
> "the side panel still looks weird").

**Recommended model: Opus 4.8** (UI design judgment + contained TS/JS; no bulk work —
Sonnet viable for a follow-up polish pass if this session leaves residue).

**Track:** meta (chat-UI). **State you inherit:** query-layer COMPLETE (S189–S191);
class-5 dup-slugs APPLIED + hardened + REDEPLOYED (S192 — live bundle now serves the
right copy for every formerly-colliding slug). Read `worklog.md` S191/S192/S193 + STATUS
first; trust worklog over this prompt.

> **S193 addendum:** the quote-minting session landed — 71 verbatim book quotes on 61
> chat-exposed nodes (quote-bearing nodes 1,598→1,659), search index + bundle rebuilt,
> all suites green. **Matt approved deploy at S193 close but the remote container had
> no Netlify credentials, so the quotes are NOT live yet — this session's deploy (or
> any manual `npx netlify deploy --prod --build` from Matt's linked machine per
> DEPLOY.md) ships them.** Golden case `list-customs-has-quotes` now pins 5 (was 2).

## The work (all in `web/public/` app.js/app.css + maybe `/api/node`)

Matt's S192 steer, verbatim intent: *"the styling needs a big boost, and modals for
nodes would be good. Honestly even showing the markdown is good enough for that entity
on click."*

1. **Receipt cards for the 3 new tools** — `app.js ingestReceipt` has NO case for
   `search_quotes` / `list_nodes` / `theme`; their receipts silently drop even though
   full results reach the browser via the receipt SSE event. Design: a "sources
   consulted" card rendering quote hits with citations (search), and compact
   name-list cards for list/theme. Every node name = a dossier button (see #2).
2. **Neighbors-card unification** — the ONE card on a different interaction pattern
   (app.js `neighborsCard`, ~line 575): each row is a `▶ <details>` disclosure whose
   summary is the node name; the name does NOT open the dossier. Matt: "the expand
   thing just doesn't really make sense with the other tools." Unify: node name opens
   the dossier (like chain spine / family tree); show edge evidence a consistent way.
3. **Styling boost + clickable affordance** — Matt: nodes "weren't obvious as
   clickable." Link affordances (cursor, hover, underline/glyph), general side-window
   polish. The chain walker itself still works (verified S192 — spine nodes are
   dossier buttons; S190/S191 only changed which tools FIRE, so chain cards appear
   less often under the researcher routing).
4. **Dossier: fuller node content** — the modal (`openDossier` → `/api/node`) shows
   identity + quotes today. Matt is happy with "even showing the markdown" — consider
   returning/rendering more of the node body (the per-node static assets from S190's
   G9 work already exist for narrative arcs).
5. **Prose entity-linking, tier 1 (client-only)** — wrap entity names in the answer
   prose with dossier buttons for any slug+name this turn's receipts already carry
   (resolve/read_node/chain/neighbors/list/theme results). Post-stream pass; no server
   or prompt changes. Tier 2 (model-emitted `[[n|slug|Name]]` markers, like the
   existing `[[q|…]]` quote system) is a DESIGN DECISION to present, not to build
   unprompted. Tier 3 (full-graph name map shipped to browser) is out of scope.
6. **About page: the provenance story** — Matt (S192): the quote/citation substance
   "is good for the about." Refresh the About copy to feature what the graph actually
   offers now: navigable book `chapter:line` citations on quotes, tool-grounded
   answers, the cite-verification gate. (Also closes the stale S187 carry-over — the
   About panel still described the old record-keeper voice.)

Verify per the preview workflow (deno tests + `deno task check` + local render); the
prod deploy at the end is **Matt-gated** as always (manual `netlify deploy --prod
--build` per `DEPLOY.md`).

## Hard gates

No graph/nodes|edges|index mutation (this is a web/-only track). No prod deploy
without Matt's go. `sources/` read-only; never fetch the wiki; don't touch `scr`;
never auto-run /endsession. Vocabulary: **Pass** / **Track** / lowercase **step** /
**Tier** = confidence 1–5 only.

## Parked queue at mint time (S192 ranking, for context — do NOT start these)

8d SERVED_AT trigger check (let live logs accumulate first) · alpha-tester notes round
(natural follow-up AFTER this ships) · granular dips (`working/granular-dip-plan.md`,
opener D2 Hand's Tourney) · D&E Pass-1 un-park (`worklog-dunk-egg.md`) ·
theme-page-cap gap · SIFT (parked).
