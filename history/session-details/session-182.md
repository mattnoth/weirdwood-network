# Session 182 — Chat-UI: Targaryen family-tree design finish + deep main-line spine

**Model:** Opus 4.8 (handoff recommended Sonnet 4.6 — frontend/CSS). **Track:** meta (chat-UI frontend, global S-numbering).
**Small API $** — a handful of live Sonnet 4.6 verification turns (family-tree queries); no graph-data writes; harvest queue at 0.

## Context

Fired `/continue chat-ui-targaryen-tree-design` (the S181 handoff). Task as scoped: (1) wire the
prototyped prominence-tier highlighting into the live family-tree render, (2) confirm the Targaryen
demo renders cleanly post-parentage-cleanup, (3) test fuzzy-resolve on Targaryen names. Then Matt,
mid-session, added the real design ask: **the tree must reach the book characters** — Rhaegar, Dany,
the Blackfyre rebellion line — not stop in the early dynasty.

## Step 1 — collision review (the handoff's gate)

Independently verified the graph is in S181's claimed state before building UI on it:
- `audit-parent-conflation.py` fresh → exactly 1 node >2 parents (`joffrey-baratheon`, intentional). ✓
- Daenerys/Rhaella/Aegon I each show 2 clean `PARENT_OF` parents. ✓
- `web/data/` bundle matches committed `edges.jsonl` (23099 == 23099, clean tree). ✓

Gate passed — proceeded to frontend work.

## Prominence-tier highlighting (item 1)

Ported the prototyped tiers from `web/dev/family-tree-fixture.html` into the live render:
- `app.js buildTreeSVG`: `FT_P_MAJOR=40`/`FT_P_NOTABLE=12` + `ftTierOf`, tier class on each node, an
  accent prominence-dot on majors, richer `<title>` (prominence/degree/quotes).
- `app.css`: `tier-major`/`tier-notable`/`tier-minor` rules, placed BEFORE `.hub` so the queried root
  always wins on equal specificity. Verified computed CSS is distinct per tier; majors are the marquee
  dynasts, minors recede. Expand modal inherits it (reuses `buildTreeSVG`).

## The deep main-line spine (Matt's design ask — the substantive work)

**Problem.** `familyTree(aegon-i-targaryen)` never reached the book era. TWO independent limits:
`GENEALOGY_DOWN_DEFAULT=4` (Dany is 12 `PARENT_OF` hops down) AND the 64-node breadth cap (BFS spends
the whole budget on the wide early dynasty — Jaehaerys I + Alysanne's 13 kids, etc.). Connectivity was
never the issue: the graph holds a full 12-hop chain Aegon I → … → Aerys II → Rhaegar/Dany.

**Constraint (Matt).** "Do not remove existing nodes on the displayed tree." So the fix must be
*additive* — keep the near-root breadth exactly as shown, thread the deep line on top.

**Design decision — prominence-anchored path threading.** Rejected pure best-first-by-prominence
(can get stuck breadth-first among prominent Dance-era siblings and never reach the tail) in favor of
an **anchor-and-thread** shape, prototyped in a throwaway before touching `graph.ts`:
1. Full-depth `PARENT_OF` BFS from root (bounded `DEEP_SPINE_MAX_DEPTH=14`), recording a shortest-path
   tree-parent for every descendant.
2. Rank descendants beyond the breadth horizon by prominence (`degree + 4·quoteCount`, the same proxy
   the render highlights); take the top `DEEP_SPINE_ANCHORS=24`.
3. For each anchor, thread its path back up until it joins an already-included node; add the path.

This threads exactly the "main lines to the important people" and drops obscure extended kin — the
prominence signal IS "main line." Cap raised 64→96 to hold breadth + spine; breadth is added first so
nothing displayed is ever dropped. Gated on `generationsDown >= GENEALOGY_DOWN_DEFAULT` so an explicit
shallow window (the `down:1` local-view callers/tests) still gets a tight window, no deep threads.

**Verified (Aegon I default tree):** 96 members, reaches gen 13; contains Dany, Rhaegar, Aerys II,
Aegon V (Egg), Maester Aemon, Viserys, AND the full Blackfyre split (Daemon I & II Blackfyre,
Bloodraven, Bittersteel). All 15 spot-checked previously-displayed nodes preserved (additive holds).
Per-generation shape is the target: WIDE near root (g3:19, g4:10 = the preserved breadth), NARROW
through the middle (g5–g11: 3–5 each = the main line, no spiral), WIDE again at the book generation
(g12:11, g13:6 = Dany, Robert/Stannis/Renly, Joffrey, Gendry — the payoff). Live render: 66 drawn
descendant nodes across 14 columns (ancestors/spouses in the 96 aren't in the descendant layout). The
model even narrated it correctly ("…the main Targaryen line down twelve generations to Daenerys, with
all major branches including the Dance of the Dragons, the Blackfyres, and the Great Bastards").

The node is `daemon-i-blackfyre`, not the bare `daemon-blackfyre` Matt named — no action needed, the
prominence anchor picks it up.

## Fuzzy-resolve findings (item 3) — tested, deferred as its own track

Both flagged cases still misbehave, but they're resolver/alias-layer issues, NOT family-tree bugs, and
fixing them is out of scope for a frontend session:
- `"Aegon the Conqueror"` → **exact** hit on `aegon-i-targaryen` (the common live path works).
- `"Aegon the Conqueror Targaryen"` (house appended) → scatters to aegon-iii/young-griff/aegon-v @0.767;
  `aegon-i` ties with every other Aegon (the discriminating "conqueror" and the misleading "targaryen"
  cancel in the token-overlap score). A real fix = token-weighting/substring bonus → needs out-of-sample
  validation across the 12k-alias map (firm rule), not a session-end tweak.
- `"targaryen dynasty"` → 3-way tie (daenerys/house-targaryen/rhaegar @0.550); cleanest fix = a
  `"Targaryen dynasty"` alias on `house-targaryen`, but that's a graph-data mutation + rebuild (out of
  scope per the handoff's DO-NOT). Left as a recommendation.

## Tests

Two `graph_test.ts` updates. The pre-existing "size cap holds" test was already RED at session start
(not from my changes — `graph.ts` untouched until the spine work): S181's cleanup had shrunk Aegon's
tree below the old 64-cap, so `truncated` flipped false. Re-pointed it at the raised 96-cap (Aegon now
overflows again with the spine). Added a deep-spine regression test: reaches Dany/Rhaegar/Egg/Blackfyre,
a deep generation stays narrow (≤8), and the shallow-window opts out. **All 36 deno tests pass.**

## What shipped vs deferred

- SHIPPED: prominence-tier highlighting (live + modal); the deep main-line spine (`graph.ts`); test
  updates. No console errors; no graph-data mutation (traversal logic only); nothing removed from the
  displayed tree.
- DEFERRED: the two fuzzy-resolve cases (own resolver track, needs out-of-sample validation).

## Next

Matt's endsession directive: **work toward publishing the live version** (deploy the chat-UI alpha to
Netlify). Netlify is already wired (`netlify.toml`: publish `web/public`, `/api/chat` + `/api/node`
edge functions, build command regenerates the 8.8 MB bundle). Remaining = connect repo to Netlify, set
`ANTHROPIC_API_KEY` server-side env, verify the build command (note: it still copies
`featured-tywin.json`, which S175 removed the Tywin landing for — check for staleness), deploy, smoke.
Plus: **update the root `README.md`** (still describes only the graph project, not the deployed chat-UI).
Continue prompt: `progress/continue-prompts/2026-07-01-chat-ui-deploy-netlify.md`.
