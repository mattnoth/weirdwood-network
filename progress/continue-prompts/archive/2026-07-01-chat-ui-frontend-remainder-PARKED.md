# PARKED: Chat-UI family-tree — frontend remainder (resume when Matt reopens frontend)

> **Status: PARKED at end of S178.** Matt paused frontend ("split the front end for a second") to
> attack the underlying graph-data correctness first (see the LIVE prompt
> `progress/continue-prompts/graph-parentage-cleanup.md`). Resume THIS only when he reopens frontend.
>
> **Recommended model:** Sonnet 4.6 — frontend/CSS only. RESTART the dev server after any `agent.ts`
> edit (Deno won't hot-reload the prompt). ASCII delimiters only in JS/TS (`node --check`/`deno
> check` before reload). Bump `?v=` in `index.html` on CSS/JS edits.

## DONE in S178 (shipped, read-only, 28 lib tests pass) — do NOT redo

- **Genealogy traversal**: `familyTree(slug)` in `web/src/lib/graph.ts` — BFS over PARENT_OF (both
  directions) + SPOUSE_OF, capped 64, `truncated` flag; wired `mod.ts` → `agent.ts` `family_tree`
  tool + prompt steering. Fixed the loop-bound-hit on lineage queries (one tool call now).
- **Render**: a left-to-right SVG descendant tree drawn INTO the chat answer (`familyTreeDiagram` in
  `app.js`), auto-centred on the root; every person clickable → existing `/api/node` dossier; the
  rail also shows a generation-ladder card. Persona is DROPPED for lineage answers (plain caption).
- **Prominence** on every member (`degree + 4·quoteCount`) — data is in the `family_tree` result;
  NOT yet wired into the live render's styling (see remainder #2).

## REMAINDER (frontend, when reopened)

1. **Pop-out / expand view** (Matt asked for this). The in-chat tree is cramped; add an "expand ⤢"
   affordance that opens the tree in a large overlay (reuse the dossier overlay pattern; put the
   tree modal at `z-index: 15` so a node-click dossier at 20 still layers on top). Rebuild a fresh
   `familyTreeDiagram(result)` into the modal (its click handlers won't survive a clone) and
   re-centre on the root via rAF.
2. **Wire prominence highlighting into the live render** (Matt asked: highlight important people —
   Dany, Rhaegar, Viserys, Daemon, Egg, Maester Aemon — + stronger clickability affordance). The
   styling is ALREADY prototyped in **`web/dev/family-tree-fixture.html`** (a standalone real-node
   SVG page, no API — open it to iterate CSS): tiers `tier-major/notable/minor` from
   `P_MAJOR=40 / P_NOTABLE=12`, accent fill + prominence dot on majors, minors recede. Port the
   `<style>` block + the tier-class logic from the fixture into `app.css` + `familyTreeDiagram`.
3. **Fuzzy-resolve robustness** (surfaced S178). In one live run the model appended the house
   ("Aegon the Conqueror Targaryen") → fuzzy 3-way scatter instead of the exact `aegon-i` hit.
   Overlaps with the graph track's resolver-prominence-ranking step — coordinate so they don't
   collide. Also `"targaryen dynasty"` → None (missing alias → should be house-targaryen).

## Data caveat (why the Targaryen demo looks wrong)
The tree is faithful, but Targaryen parentage edges are noisy (duplicate stubs + edge-noise) — see
`working/family-tree-genealogy-audit.md` and the LIVE graph-parentage-cleanup track. Clean families
(Starks under Ned) render perfectly. Fix the graph first, then the Targaryen demo will be correct.

## Key files
`web/public/{app.js,app.css,index.html}` · `web/dev/family-tree-fixture.html` (styling sandbox) ·
`web/src/lib/graph.ts` · `web/netlify/edge-functions/agent.ts` (RESTART after edits).
