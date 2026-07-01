---
session: 178
title: Chat-UI family-tree traversal + genealogy-conflation discovery
date: 2026-06-30
track: meta / graph
model: Opus 4.8 (handoff recommended Sonnet 4.6; ran on session Opus)
api_spend: small — live Sonnet 4.6 curl/preview turns for verification (~cents); NO graph writes
harvest_queue: 0 open rows
---

# Session 178 — Family-tree traversal, and the conflation it exposed

## What this session was

Continued the S177 chat-UI refinements pass. Matt's opening artifact was a screenshot of the live
UI hitting `loop-bound-hit` on "Show me the Targaryen dynasty family tree from Aegon the Conqueror"
— the model fanned out through generic `neighbors` (titles, succession, birthplace) and exhausted
`MAX_TOOL_ITERATIONS` before assembling any lineage. That one query drove the whole session.

## What shipped (all read-only over the graph — ZERO nodes/edges minted)

- **`familyTree(slug)` traversal** (`web/src/lib/graph.ts` + `types.ts` + `mod.ts`): BFS over
  `PARENT_OF` (source=parent→target=child, both directions) + `SPOUSE_OF` attached same-generation,
  spanning-tree so the incest DAG draws clean, capped at 64 with a `truncated` flag. One tool call —
  kills the loop-bound. Wired into `agent.ts` as the `family_tree` tool + MANDATORY-for-lineage
  prompt steering, and the persona is DROPPED for lineage answers (a tree is a picture, not a speech
  — the model emits a one-line caption).
- **Render**, two forms: a generation-ladder card in the rail, and (Matt's ask) a real **left-to-right
  SVG descendant tree drawn into the chat answer** (`familyTreeDiagram` in `app.js`), auto-centred on
  the root, every person a clickable node → the existing `/api/node` dossier. First cut was top-down
  and 7600px wide (root centred over its whole span → invisible at scroll-0); flipped to LR (narrow,
  vertical-scroll-natural, names read horizontally).
- **Prominence signal** (`degree + 4·quoteCount`) on every family member, so the render can highlight
  story-weighty characters. Validated: Daenerys 402, Rhaegar 118, Viserys 102, Daemon 68 float above
  historical filler and bare-surname stubs (~1). Exactly the Dany/Rhaegar/Egg/Aemon set Matt named.
- **Static fixture** `web/dev/family-tree-fixture.html` — a standalone real-node SVG page (no API) that
  previews prominence-tier highlighting, so styling can be iterated offline. Built, not browser-verified
  (Matt paused frontend before that).
- 28 lib tests pass (+6 new familyTree/prominence).

## The discovery — and a correction I had to make

The family-tree feature immediately EXPOSED that the graph's parentage layer is badly noisy. From
Aegon the Conqueror the tree "reached" Rhaegar in 4 generations (should be ~15), and "Maron Martell's
son" (an ancient Daenerys × Maron Martell) sat beside Rhaego (Dany × Drogo). Root cause: repeated
dynastic names collapsed onto single **bare-name slugs** carrying the edges of several people at once.
Audit: **88 of 1,015 parented nodes have >2 PARENT_OF parents** (impossible for one person) —
Targaryen 26, Stark 19 (brandon-stark: 13 parents), Tyrell 9, Greyjoy 7…

**The incident worth logging:** I first claimed "Maester Aemon has no node — he's folded into a
generic bucket." Matt pushed back ("Maester Aemon HAS to have a node. There's no way."). He was right
— I had checked the wrong slug (`aemon-targaryen-son-of-maekar` without the `-i`). The real node,
`aemon-targaryen-son-of-maekar-i`, exists with 16 quotes. A cold re-check corrected it. **Lesson baked
into the graph-cleanup continue prompt: next session cold-reads and re-derives the numbers before
executing — do not trust a prior session's specifics on faith.** The corrected diagnosis is that the
disambiguated nodes mostly EXIST and are wired right; the bug is DUPLICATE parentage recorded onto
redundant empty stubs, plus edge-noise on some single real people (Joffrey, Petyr with >2 parents).
So it's mostly delete-only dedup, not node-splitting.

Matt also (rightly) checked: "are you minting nodes???" — No. Everything this session was read-only.

## Decisions

- Genealogy is a distinct traversal shape from the causal spine — its own tool + its own render.
- Persona is dropped for family-tree answers (the chart is the answer). Matt: "ignore the bloodraven
  persona on this, that's what people will want."
- Sigils PARKED (they exist as blazon TEXT in wiki infoboxes — 362/633 houses — not as images; out
  of scope now).
- Graph-parentage cleanup is its own track, DEcided approach: **Python deterministic proposal first,
  then agentic batch review against the LOCAL wiki + chapters** (Matt can't hand-review 88+;
  policy-gated). No mint until the review clears.
- Frontend polish (pop-out modal, wiring the prominence highlight into the live render, fuzzy-resolve)
  PARKED until Matt reopens frontend.

## What's next

Live track: `progress/continue-prompts/graph-parentage-cleanup.md` — cold-read + validate the plan,
then Step 1 (read-only `scripts/audit-parent-conflation.py` classifying the 88), Step 2 (agentic batch
verify vs local wiki+chapters), Step 3 (apply after review + rebuild). Parked: the chat-UI frontend
remainder (`archive/2026-07-01-chat-ui-frontend-remainder-PARKED.md`). Also open: the `aerion-targaryen`
two-Aerions split (task chip) folds into this track.
