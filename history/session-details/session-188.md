---
session: 188
date: 2026-07-04
track: meta/graph
model: Opus 4.8
api_cost: 1 live loremaster turn on the local weirwood-live server (~few cents); read-only logs read; no graph writes
---

# Session 188 — Graph traversal & query-surface analysis: two new top-level docs

## Purpose

Matt opened on `/remote-control`, then asked me to read the live chat-UI usage logs and
answer a pointed observation: *why does every question — even "describe some detailed meals" —
resolve to an event and walk a causal chain?* That question opened a full analysis of the
graph's **retrieval/query surface**, which became two new top-level living documents:
`GRAPH-QUERY-ROADMAP.md` (forward-looking traversal/query design) and `GRAPH-STATE.md`
(current-state snapshot). No code was changed; the deliverable is the analysis + the two docs.

## What was investigated (and the key findings)

### 1. Why the chat-UI feels event-biased — root-caused to the retrieval surface
Not a model preference. The chat has exactly **5 tools** (resolve/read_node/walk_chain/
neighbors/family_tree), **no content search**, and `walk_chain` carries the only `MANDATORY`
framing in the prompt. Two independent bias drivers:
- **G3:** `walk_chain`'s MANDATORY/MUST framing bleeds into non-causal questions.
- **G10:** when exact resolve misses and falls back to fuzzy (token-overlap ≥ 0.5 + a
  per-slug-token bonus), the math structurally favors long-slugged **event** nodes
  (`assassination-of-tywin-lannister`) over terse ones (`beef`). "events (fuzzy)" in the
  receipts is the visible tell.
Root cause under both = **G2 alias holes** (`lemon cake` resolves, `lemon cakes` does not).

### 2. Corrected my own misreads (grounded against the repo)
- Food IS a first-class node type (110/113 shipped, each with identity + quotes) — my first
  "nowhere to land" framing was wrong. The graph has 21 node types.
- The bundle ships ~all nodes (8,473 of 8,727; the 254 missing = the `_conflicts` staging
  bucket) BUT each node is SLIMMED to `{name, type, identity, quotes}` — the `## Narrative Arc`
  and `## Edges` prose is DROPPED (G9). Real cited descriptive content is stranded out of the
  bundle.
- `resolve` = DNS-style name→slug lookup over `alias-map.json` (12,139 phrases); it does not
  traverse or answer. It's the quietest failure point.

### 3. The traversal machinery + the query-mode DIVERGENCE
Read the enrichment/narrative-arc era (S82–S167). The graph has a real designed traversal
grammar: causal chain (CAUSES/TRIGGERS/MOTIVATES + ENABLES), event reification into hubs +
role edges, containers (5 tags: essos/wo5k/north/aegon/bran). Crucially, `graph-query.py` has
**~11 query modes**; the chat-UI ported only **~5**. Never ported: `--container` (theme
bag-retrieval), `--expand-beats`, `--path`, `--event-participants`. `--container` alone would
partially answer thematic questions. Two implementations of one surface, drifted apart.

### 4. The descriptive-layer census (the hard finding)
Measured quote-density + edge-degree per node type off the bundle:
- Events are wired (event.incident: 70% w/quote, 4.75 avg degree, 1% islanded).
- The descriptive layer is **quote-thin AND orphaned**: food 96% islanded, materials 91%,
  customs 96%, artifacts 82%, texts 94%, species 90%, even locations 61%.
- Quotes concentrate on characters (73% of 6,053), events 12%, whole descriptive layer 3%.
- All 5 containers tag ONLY event nodes — zero foods/locations/characters. The thematic index
  is event-only.

### 5. WHY the descriptive layer is orphaned (arc-by-arc, S133–S167)
Every dip ran a "descriptive-object" lens, so food/dress/hospitality WAS hunted — but its
output went to the **harvest queue**, and harvest-drain only (a) attached quotes to existing
nodes (→ characters hold 73% of quotes) or (b) minted isolated `object.food` nodes with a
quote but **no edges**. The harvest contract was "capture the quote," never "wire the node."
Hence food = 51% w/quote (harvest worked) but 96% islanded (wiring was never in scope). The fix
is a cheap wiring step (descriptive edge grammar), not a re-read of the corpus.

### 6. Backlog salvage (swept worklog Ideas&Backlog + todos.md)
Un-done items relevant to the theme: the charter'd-but-unbuilt **"braid"/convergence-map**
query primitives (`--braid`/`--fork-hubs`/`--join-hubs`; `graph/convergence-maps/` = README
only) → roadmap D7; the unshipped **trigger table** (the index's routing half) → D8; the
deferred **Python food-keyword grep**; **TWOIAF** on disk (1.5 MB) never Pass-1-extracted;
prophecy layer (4 nodes, 0 edges).

### 7. LIVE reproduction on the deployed UI (the exhibit)
Brought up the local `weirwood-live` server and asked *"Describe some detailed meals and feasts
from the books."* The receipts panel showed **~13 consecutive `resolve` calls**, every hit
`(fuzzy)` or `no match` (5× no-match on reasonable phrasings), never a single `read_node`/
`walk_chain`, ending in `loop-bound-hit`: *"The search was bounded. The loremaster reached its
limit of graph steps."* Every gap fired at once (G1 no-search → the flailing · G2 alias holes ·
G10 fuzzy→events · §2a orphan food ring). This is the portfolio-grade "here's the problem"
exhibit.

## Key framing decided this session

**Two apertures onto one graph; essential vs. incidental shrink.** The chat-UI traverses the
same graph as a full agent but through a smaller aperture (3 in-memory JSON blobs, 5 tools,
6-iteration bound, no content search). That shrink is TWO things:
- **Essential (keep, permanent):** no-filesystem edge runtime, bounded spend on a public URL,
  latency, quote-only grounding + cite-gate.
- **Incidental (fix, just unfinished):** 5-of-11 modes, no content search, slim projection
  (G9), alias holes (G2). None required by the runtime — a content index is *build-time*.
The live failure is the two compounding: the incidental shrink caused the flailing, the
essential shrink guillotined it. One content-search tool answers the meals question in a single
step and never approaches the bound — proof that widening the incidental shrink is the whole
fix.

## Interview/portfolio thread (Matt-raised)

Matt wants the graph-traversal scripts organized so they read as a first-class part of the
graph (not scratch in `working/`) — "the query interface the graph ships with." This is a live
interview framing. Captured as roadmap §4 (unify the two implementations into one documented
query API; Python CLI + chat-UI as thin adapters).

## Deliverables

- `GRAPH-QUERY-ROADMAP.md` (top level) — traversal/query design: live-evidence exhibit + two-
  apertures framing (§0), census-grounded gaps G1–G10, directions D1–D8, prior-art §8, script-
  org/interview §4, open questions.
- `GRAPH-STATE.md` (top level) — census (§2a), harvest-mechanism root cause (§2b), chat-UI live
  status, parked tracks, backlog salvage (§4b).

Both are living docs to be refined this session + next.
