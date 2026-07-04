# Query Operations — the contract (v1)

> Part of the **query-layer Track** (S189 design: `working/query-layer/design.md`), step 1
> (session A). This document names every operation the Weirwood query surface exposes or
> intends to expose, its inputs/outputs/semantics, and how it behaves under each of the two
> **profiles**. It is the reference the CLI, the chat tools, and (later) the site's "how it
> works" page all point back to. **Tier** = confidence 1–5 only; a **Track** is this named
> body of work; lowercase **step** = an ordered piece of it — see `reference/glossary.md`.
>
> **Status of this document: v1.** It describes CURRENT behavior (verified against the live
> `web/src/lib/` TS engine and `scripts/graph-query.py` / `scripts/event_alias_resolver.py`
> on 2026-07-04), not aspirational behavior. Known-bad current behavior (G-numbered gaps from
> the design doc) is documented, not silently fixed — fixes land in later steps and update
> this doc + the golden cases together.

---

## 0. The two profiles

Every operation below is evaluated under one or both of:

- **full** — the in-repo / CLI surface. Reads the live graph on disk (`graph/nodes/`,
  `graph/edges/edges.jsonl`, `reference/`), unbounded walks, every op available. Used by
  Claude Code sessions, dip subagents, audits. No iteration cap, no size cap other than
  documented per-op caps (e.g. `path`'s bridge cap).
- **bounded** — the public chat surface (`web/src/lib/` behind the Netlify Edge function).
  Reads a slimmed, pre-built, in-memory bundle (`web/data/{nodes,edges,alias-map}.json`,
  ~8.7 MB). Hard caps exist because a public LLM loop must terminate cheaply and read
  citably:
  - walk depth: **2** hops per direction from the queried node
  - **≤12** links per direction (upstream / downstream) in a causal chain
  - ENABLES preconditions: a separate side-channel, **≤24**, deduped by source→target
  - **6** tool-call iterations per chat turn (`MAX_TOOL_ITERATIONS`)
  - only a subset of ops are ported to this profile at all (see the table in §1 and each
    op's "bounded" subsection)

Where the two profiles legitimately diverge (depth/caps, ported-vs-not), that is a
**documented profile difference**, not a bug. Where they claim the same behavior and give
different answers, that is drift — the golden cases in `spec/cases/` exist to catch it.

---

## 1. Operation inventory

| op | full (Python) | bounded (TS/chat) | status |
|---|---|---|---|
| [`resolve`](#resolve) | ✅ `event_alias_resolver.resolve()` | ✅ `resolve()` | both, live |
| [`read`](#read) | ✅ positional node-report mode | ✅ `readNode()` | both, live |
| [`neighbors`](#neighbors) | ✅ `--neighbors` | ✅ `neighbors()` | both, live |
| [`chain`](#chain-causal) (causal) | ✅ `--causal-chain` | ✅ `walkChain()` | both, live (profile-capped) |
| [`chain --full`](#chain---full) (+ENABLES) | ✅ `--full-chain` | ◐ `walkChain()`'s `enables` side-channel | both, profile-documented difference |
| [`expand-beats`](#expand-beats) | ✅ `--expand-beats` modifier | ❌ | **PLANNED — step 6** |
| [`path`](#path) | ✅ `--path` (2-hop bridges, cap 50) | ❌ | **PLANNED — step 6** |
| [`participants`](#participants) | ✅ `--event-participants` | ❌ | **PLANNED — step 6** |
| [`container`](#container) | ✅ `--container` | ❌ | **PLANNED — step 6a** |
| [`family`](#family) | ✅ `--family-tree` / `family_tree()` | ✅ `familyTree()` | both, live — Python port shipped (step 1 close-out) |
| [`health`](#health--census) | ✅ `--health` | ❌ | full-profile only (by design) |
| [`search`](#search) | ✅ `search.py` / `weirwood query search` | ✅ `searchQuotes()` | **SHIPPED — step 5b**, the headline capability |
| [`list`](#list) | ✅ `list_nodes.py` / `weirwood query list` | ✅ `listNodes()` | **SHIPPED — step 5d** |
| [`corpus-search` / `passage`](#corpus-search--passage) | ✅ `corpus_search.py` / `weirwood query corpus-search` | ❌ (deferred S172; `passage` still gated) | **SHIPPED — step 5e** (Python full-profile ONLY; no bundle/chat exposure by design) |
| [`mentions`](#mentions) | ✅ `mentions.py` / `weirwood query mentions` | ❌ | **SHIPPED — step 8b** (reads LIVE graph/index/, may be stale — see G13; a preview-repair build + report exist at `working/query-layer/`) |
| [`theme`](#theme) | ✅ `themes.py` / `weirwood query theme` | ✅ `theme()`/`listThemes()` | **SHIPPED — step 8a** |
| [`braid` / `fork-hubs` / `join-hubs`](#braid--fork-hubs--join-hubs) | ✅ `braid.py` | ❌ | **SHIPPED — step 7**, full-profile only by design |

---

## 2. CLI subcommand front door (`weirwood query <subcommand> ...`)

The design contract names `weirwood query chain <slug>`-style subcommands as the CLI's front
door. `cli.py` (step 1 close-out) adds this as an **additive translation layer** at the top of
`main()`: each subcommand below is translated into its equivalent legacy flag invocation before
argparse ever sees it, so every existing legacy-flag invocation keeps working byte-for-byte
unchanged. Extra flags (`--json`, `--expand-beats`, etc.) pass through after the subcommand's
own positional args.

| subcommand | equivalent legacy flag |
|---|---|
| `read <slug>` | `<slug>` (bare positional) |
| `neighbors <slug>` | `--neighbors <slug>` |
| `path <a> <b>` | `--path <a> <b>` |
| `health` | `--health` |
| `participants <hub>` | `--event-participants <hub>` |
| `chain <slug>` | `--causal-chain <slug>` |
| `full-chain <slug>` | `--full-chain <slug>` |
| `container <name>` | `--container <name>` |
| `family <slug>` | `--family-tree <slug>` |
| `resolve <phrase>` | *(no legacy-flag equivalent)* — delegates to `weirwood_query.resolve.resolve()`, printed in the same format as `scripts/event_alias_resolver.py --lookup` |
| `fork-hubs [--min-out N] [--include-enables]` | *(no legacy-flag equivalent — new op, step 7)* |
| `join-hubs [--min-in N] [--include-enables]` | *(no legacy-flag equivalent — new op, step 7)* |
| `braid <slugA> <slugB> [more...] [--include-enables]` | *(no legacy-flag equivalent — new op, step 7)* |
| `search <query> [--type CATEGORY] [--limit N]` | *(no legacy-flag equivalent — new op, step 5b)* |
| `list --type CATEGORY [--has-quotes] [--container NAME] [--limit N] [--offset N]` | *(no legacy-flag equivalent — new op, step 5d)* |
| `corpus-search <query> [--book BOOK] [--mode phrase\|tokens] [--limit N]` | *(no legacy-flag equivalent — new op, step 5e; CLI/full-profile only)* |

---

## `resolve`

**Purpose:** turn a natural-language phrase ("the Red Wedding", "Tywin", "Robb Stark's
death") into one or more candidate graph node slugs.

**Inputs:** `phrase: string`.

**Outputs:** an ordered list of candidates, each carrying at minimum `{slug, category}`,
ranked best-first. Empty list = miss.

### Semantics (bounded / TS — `resolve()` in `web/src/lib/resolve.ts`)

1. Clean the phrase (`cleanPhrase` — trust-boundary guard; `null`/empty/whitespace-only →
   `[]` immediately, no exception).
2. Normalize (`normalize()`: lowercase, trim, strip **one** leading article `a`/`an`/`the`,
   collapse whitespace — does **not** strip quotes/apostrophes/hyphens; keys in
   `alias-map.json` were produced by the identical normalizer, so this step must stay in
   lockstep with the Python `normalize()` it ports).
3. **Exact stage:** look up the normalized phrase in `alias-map.json`. A hit returns
   **every** candidate node under that phrase (not just the first), each stamped
   `score: 1.0, matchType: "exact"`, ranked by **prominence** (`degree + 4·quoteCount` over
   the whole graph, computed only across the hit candidates) so a content-rich node
   (e.g. Maester Aemon) outranks an empty bare-name stub sharing the phrase
   (e.g. the bare `aemon-targaryen` bucket).
4. **Fuzzy stage** (only on an exact miss): tokenize the query (stop-words removed —
   articles/prepositions/interrogatives/auxiliaries/possessive `'s`). For every phrase key
   in the alias map, compute `base = token_overlap(query, key) / |query_tokens|`; discount by
   a **candidate-length penalty** `min(1.0, |query_tokens| / |candidate_tokens|)` — a no-op
   whenever the candidate phrase is no longer than the query, so it only ever discounts a
   candidate phrase LONGER than the query (step 4c / G10, S190 — see below). Then, per
   candidate slug, add a **+0.05 slug-token bonus** for every query token also found in the
   candidate's own slug (kebab-split), capped at 1.0. Keep candidates whose FINAL score
   (post-penalty, post-bonus) is **≥ 0.5**. Best score per slug wins across all matching
   phrase keys. Result capped at **5** candidates, sorted by `(score desc, prominence desc)`,
   `matchType: "fuzzy"`.
5. A miss at both stages → `[]`.

**Fixed in step 4 (S190) — this doc's v1 recorded these as open bugs; they are now resolved.
Golden cases in `resolve.json` were flipped to pin the corrected behavior (with a `note`
crediting the fix); the removed-bug notes below are retained as changelog, not open items:**
- **G19 (step 4a):** `"Robb Stark's death"` previously had no exact key in `alias-map.json`
  and fell to the fuzzy stage (landing on the right node, `robb-is-killed`, but via
  `matchType: "fuzzy"`). Fix: `build_alias_table.py` now folds victim-phrase entries
  (VICTIM_IN-derived) into the all-node index that `build_chat_bundle.py`'s
  `build_alias_map()` consumes — the phrase is now an **exact** key in both profiles.
- **G2 (step 4b):** `"lemon cakes"` previously missed the intended food node entirely (fuzzy
  stage returned unrelated low-score foods, best 0.55). Fix: `build_alias_table.py` now
  generates deterministic **plural** (`lemon cake` → `lemon cakes`, small irregulars list +
  regular -s/-es rules), **possessive** (`"X's Y"` ↔ `"Y X"`), and **leading-article**
  (`"the X"` ↔ `"X"`) variants from every short (≤4-word) name-shaped alias/name/slug entry
  at build time. Plural/possessive are scoped to common-noun-shaped node categories (foods,
  objects, artifacts, materials, texts, titles, concepts, religions) — proper-noun/titled
  categories (characters, houses, locations, chapters, factions, events, and unset-category
  event-table entries) are excluded from plural/possessive to avoid nonsense transforms
  (pluralizing a character name or a multi-word event title); leading-article variants stay
  universal (safe for any name — this is the transform behind "the Red Witch" → `melisandre`
  etc.). Variants sit at the LOWEST merge priority — a real alias/name/slug entry always wins
  a collision; generated-variant collisions are logged (not guessed) to
  `working/query-layer/variant-collisions-s190.md`. `"lemon cakes"` is now an exact hit.
- **G10 (step 4c):** bare first-name/surname queries (e.g. `"Tywin"` alone) previously could
  rank a **different character above the intended one** — e.g. `"Tywin"` put
  `tyrion-lannister` above `tywin-lannister` because every fully-overlapping candidate phrase
  tied at score 1.0 regardless of the candidate phrase's own length, so the whole-graph
  prominence tie-break alone decided (and `tyrion-lannister`'s prominence, 462, beat
  `tywin-lannister`'s, 218). Fix: the candidate-length penalty above (identical formula in
  `resolve.py` and `resolve.ts`). `"Tywin"` now resolves top-ranked to `tywin-lannister`
  (score 0.55, `matchType: "fuzzy"`) — `tyrion-lannister`'s only matching phrase (`"lord
  tywin's bane"`, 3 tokens) is penalized below the 0.5 floor and drops out of the candidate
  list. The same mechanism also fixes the full-profile `"House Targaryen"` fuzzy-stage tie
  against a 13-token book-title node (see `resolve-house-targaryen-full-profile-length-debias`
  golden case).

### Semantics (full / Python — `event_alias_resolver.resolve()`)

Same three-source alias table (wiki redirects + event frontmatter + all-node frontmatter)
plus **two sources the bundle does not carry**: victim-phrase templates (`"X's death"` /
`"death of X"` generated from an event's own victim role) and `"The_*"` wiki redirect pages.
Returns `(slug, status, candidates)` where `status` is one of:
- `hit` — unambiguous exact match (event alias table)
- `hit-character` — exact match to a full character name
- `candidates` — fuzzy or ambiguous-but-scored match (see `candidates` list)
- `ambiguous` — phrase is in the known collision table (no single top slug)
- `miss` — no match at any level

This four/five-way status enum has **no bounded-profile equivalent** — the TS `resolve()`
collapses everything to `exact` / `fuzzy` / `[]`. `ambiguous` in particular has no TS
analogue today (an ambiguous phrase currently just returns unranked fuzzy candidates,
if any clear the 0.5 floor, or `[]`). Reconciling the status vocabulary is in scope for
step 4's resolver hardening but is **not yet done** — v1 of this doc records the mismatch,
it does not resolve it.

### Caps
No profile-specific cap on `resolve` itself beyond `MAX_FUZZY_CANDIDATES = 5` (both
profiles conceptually; Python's constant may differ — see `_fuzzy_candidates` in
`event_alias_resolver.py` for the exact value in effect before step 4 harmonizes them).

---

## `read`

**Purpose:** the node dossier — name, type, curated identity prose, quotes, chronology
anchors.

**Inputs:** `slug: string`.

**Outputs (bounded):** `NodeRecord | null` — `{name, type, identity, quotes[], composite?,
reading_order?}`. `quotes[]` is `{text, attribution, cite}`. Returns `null` for an invalid
slug (regex trust-boundary check) or a slug absent from the bundle. No exception path.

**Outputs (full):** a richer report dict: `{node: {slug, name, type, file_path, aliases,
top_level_alias}, edges: [...], inbound: [...], inbound_total, summary}` — `edges` are
parsed from the node file's **legacy `## Edges` markdown section**, not `edges.jsonl` (see
§ "G16" note below); `inbound` streams up to `inbound_limit` (default 20) reverse references
found by grep-scanning other node files' `## Edges` sections.

**Profile divergence, explicit:**
- The full-profile `read` surfaces `## Edges` markdown prose and inbound-reference search —
  a materially different (and currently the *only* markdown-`## Edges`-reading) code path
  from every other full-profile op, which reads `edges.jsonl`. This is **G16**: two edge
  serializations, unreconciled. `read`'s positional mode keeps printing `## Edges` prose
  (labeled as display prose, not structured edges) after step 1's consolidation — it is not
  being unified with `edges.jsonl` in this pass.
- The bounded profile's `identity` + `quotes` are the curated, citable content the chat is
  restricted to quoting from; `## Narrative Arc` prose is **dropped from the bundle
  entirely** (G9) — not present in `NodeRecord` at all today. Step 6c decides whether it gets
  inlined or fetched on demand.
- `containers:` frontmatter (the 5-container bag-retrieval tags) does **not** ship in the
  bounded bundle at all — `container` has no bounded-profile equivalent yet (see below).

---

## `neighbors`

**Purpose:** every edge touching a node, split by direction (outgoing/incoming), grouped by
edge type — the "relational, no-walk" view.

**Inputs:** `slug: string`.

**Outputs:** `{slug, outgoingCount, incomingCount, outgoing: {edge_type: [link...]},
incoming: {edge_type: [link...]}}`. Each `link` carries `{source, edge_type, target,
source_name?, target_name?, source_type?, target_type?, evidence_quote, ref, tier}`
(bounded) — the full-profile CLI prints an equivalent human-readable grouping plus a JSON
mode with the same fields under different key names (`source_slug`/`target_slug`/
`evidence_ref`/`confidence_tier` vs. the bounded profile's `source`/`target`/`ref`/`tier` —
**a field-naming difference between the two implementations that step 1's consolidation
should either document permanently or unify**; v1 records it as a known naming mismatch,
not yet reconciled).

**Dedup:** identical `type|source|target` edges collapse to one link (a duplicate edge row
is not a second connection) — verified live in both the TS implementation and its test
suite; the full-profile CLI does not appear to dedupe identically and is a candidate for a
parity fix inside step 1's consolidation.

**Invalid slug:** empty groups, `outgoingCount: incomingCount: 0`, no throw (bounded,
verified). Full-profile: node-not-found message + `slug_prefix_suggestions` hint (a UX the
bounded profile has no equivalent of).

---

## `chain` (causal)

**Purpose:** the causal consequence-chain in and out of an event/action node — "what led to
this" (upstream) and "what this led to" (downstream).

**Inputs:** `slug: string`; optional `maxDepth` (bounded: default **2**; full: unbounded BFS
by default, no cap).

**Edge types walked:** `CAUSES`, `TRIGGERS`, `MOTIVATES` only. `PRECEDES` (pure chronology,
no causal claim) and `ENABLES` (precondition, not consequence) are excluded from the causal
spine in both profiles — `ENABLES` surfaces as a separate structure (see `chain --full`
below), `PRECEDES` does not surface in `chain` at all today.

**Outputs (bounded):** `{slug, upstream: ChainLink[], downstream: ChainLink[], enables:
ChainLink[]}`. Each `ChainLink` = `{source, edge_type, target, source_name?, target_name?,
source_type?, target_type?, evidence_quote, ref, tier, depth}`. `depth` is 1-indexed BFS
distance from the queried node.

**Ordering (bounded — S185 fix, verified live):** links within `upstream` and `downstream`
are sorted into **story-time reading order**, not BFS hop-depth order. Each event node
carries a `composite` sort key (`{ac_year:04d}.{book}.{chapter:03d}`, when dated) and/or a
`reading_order` fallback (`{book}.{chapter:03d}`); undated nodes are placed via a
book-opening-year proxy so they interleave near the right point; a node with neither sorts
last. An undated **chain root**'s own outgoing link borrows its target's chrono key as proxy
(so the root's immediate effect never sinks below a deeper, dated descendant). The
full-profile CLI's `--causal-chain` prints upstream sorted `(-depth, source_slug)` and
downstream sorted `(depth, target_slug)` — **BFS/depth order, not story-time** — this is a
live, documented full/bounded ordering divergence, not yet ported to Python (step 1's
`traverse.py` is the first place Python could pick up the story-time sort per the design
doc's "end-state" row: `chain (causal) | ✅ unbounded | ✅ capped+sorted | both; Python gains
the story-time sort`).

**Caps (bounded only):** `maxDepth` default 2; **≤12 links per direction**
(`MAX_LINKS_PER_DIRECTION`); BFS returns links breadth-first up to the cap, so a dense hub's
walk truncates rather than exploding the panel — there is no `truncated` flag on `ChainResult`
today (unlike `FamilyTreeResult`), which is a gap worth flagging for step 6/9's parity pass.

**Full-profile:** no depth cap, no per-direction link cap; walks the entire causal component
transitively. On a hub node (e.g. the Red Wedding) this can return 50+ edges — a graph dump,
by design, for an in-repo agent that wants the whole shape.

**Invalid slug:** `{slug, upstream: [], downstream: [], enables: []}`, no throw (bounded,
verified).

---

## `chain --full`

**Purpose:** the causal chain **plus** `ENABLES` preconditions walked as part of the same
transitive walk (full profile) — "what had to be true" in addition to "what caused what."

**Full-profile semantics:** identical to `chain`, but `edge_types` includes `ENABLES`
alongside `CAUSES`/`TRIGGERS`/`MOTIVATES`; rendered inline in the same upstream/downstream
walk labeled `(precondition)`.

**Bounded-profile semantics — profile-documented divergence, not a gap:** `walkChain()`
never walks `ENABLES` transitively into the spine (it would flood a hub with tangents — see
the code comment in `graph.ts`). Instead it returns a **separate side-channel** array
`enables: ChainLink[]`: every `ENABLES` edge whose **target** is a node already touched by
the causal spine (queried node + everything upstream/downstream), deduped by
`source→target`, capped at **≤24** (`MAX_ENABLES`; measured ≤8 in practice on the live
graph). This is intentionally a *shallower, non-transitive* precondition set — one hop into
the spine, not `--full-chain`'s full transitive walk — so the model can reveal "preconditions
behind a toggle" in one round-trip without a second tool call. **This is the profile
difference the design doc calls out at D-B: same conceptual op, deliberately different depth
under the cap regime — a test asserting bounded `enables` should never assert the full-chain
transitive count.**

---

## `expand-beats`

**Status: PLANNED — step 6 (b).** Not yet ported to the bounded profile.

**Full-profile semantics (`--expand-beats` modifier on `--causal-chain`/`--full-chain`):**
for every node touched by the causal walk, also finds its `SUB_BEAT_OF` children (event
hub → reified sub-beat) and each beat's participant role edges (`AGENT_IN`, `VICTIM_IN`,
`COMMANDS_IN`, `WITNESS_IN`, `WIELDED_IN`), so a chain node that reads sparse (a hub with no
direct role edges) shows its real richness via its sub-beats. Output adds a `beats: {node:
[{beat, roles: [(role_type, participant)]}]}` map alongside the normal chain result.

---

## `path`

**Status: PLANNED — step 6 (b).** Not yet ported to the bounded profile.

**Full-profile semantics (`--path A B`):** (a) direct edges between A and B in either
direction, plus (b) 2-hop bridges — nodes that are neighbors of both A and B (excluding A
and B themselves), ranked by combined edge count on both legs, capped to the top
`BRIDGE_CAP` (50 in the current script) for display. Each bridge reports the edge types and
dominant direction (`out`/`in`/`both`) on each leg.

**Recommended bounded-profile target (per design doc §5 step 6b):** port as a chat tool —
"how are X and Y connected" is a real archetype query the design doc flags as worth a tool,
unlike `participants`/`expand-beats` which can stay dossier-side (full-profile only).

---

## `participants`

**Status: PLANNED — step 6 (b).** Not yet ported to the bounded profile.

**Full-profile semantics (`--event-participants HUB`):** unions the participant role edges
(`AGENT_IN`/`VICTIM_IN`/`COMMANDS_IN`/`WITNESS_IN`/`WIELDED_IN`) across every `SUB_BEAT_OF`
child of a hub event and presents them as if directly attached to the hub — the reification
pattern's read-side (an n-ary event hub's actual participants live one hop down, on its
reified sub-beats, not on the hub itself). Errors distinctly: hub not found (with
slug-prefix suggestions) vs. hub found with zero beats (clean "not mined yet" message) vs.
beats found with zero role edges.

---

## `container`

**Status: PLANNED — step 6 (a).** Not yet in the bounded bundle or profile.

**Full-profile semantics (`--container NAME`):** bag-retrieval — every node whose
`containers:` frontmatter array includes `NAME`, **unordered** (explicitly not the ordered
causal walk; the docstring/CLI help text says to use `--causal-chain`/`--full-chain` for the
arc). The **only** full-profile mode that never touches `edges.jsonl` — it's a pure
frontmatter scan over `graph/nodes/`. Container set is currently 5 (`essos`, `wo5k`, `north`,
`aegon`, `bran` — settled S122); `containers` is a tag, never an umbrella node.

**Bounded-profile gap:** `containers:` frontmatter is **not present anywhere in the bundle**
today (verified: no `containers` field in `NodeRecord`, no references in `web/src/lib/*.ts`)
— this is a bundle-projection gap the design doc calls out explicitly (§4 op table: `container
| ✅ | ❌ (containers not in bundle) | both (step 6a)`), distinct from "not yet coded"; the
builder (`build_chat_bundle.py`/`build-chat-export.py`) needs to add the field before a TS
`container()` can exist at all.

---

## `family`

**Purpose:** the lineage/genealogy walk around a node — descendants, ancestors, and spouses
— as a flat member set plus the `PARENT_OF`/`SPOUSE_OF` bonds among members. A distinct
shape from `chain`: parentage, not consequence.

**Inputs:** `slug: string`; optional `generationsUp` (default **2**), `generationsDown`
(default **4**).

**Outputs:** `{root, rootName?, generationsUp, generationsDown, members: FamilyMember[],
parentBonds: FamilyBond[], spouseBonds: SpouseBond[], memberCount, truncated}`.
- `FamilyMember`: `{slug, name, type?, generation, hasNode, degree, quoteCount,
  prominence}`. `generation` is signed relative to root (0 = root, negative = ancestors,
  positive = descendants). `hasNode: false` means a `PARENT_OF`/`SPOUSE_OF` edge names a slug
  with no backing node file — `name` falls back to a humanized slug (`"aerion-targaryen-x"` →
  `"Aerion Targaryen X"`).
- `prominence = degree + 4·quoteCount` (same proxy used by `resolve`'s exact-tie-break):
  ranks story-weighty kin (Dany, Rhaegar, Aemon) above historical filler / bare stubs.
- `truncated: true` means the size cap (**96**, `MAX_FAMILY_MEMBERS`) stopped the walk before
  it exhausted the lineage — the API reports this rather than silently dropping kin.

**Deep main-line spine (verified live, non-obvious behavior):** the breadth BFS alone
(bounded by `generationsDown`) cannot reach a distant dynasty's book-era descendants — Aegon
I → Daenerys is 12 `PARENT_OF` hops, far past the default `generationsDown=4` horizon. When
the caller uses the **default** `generationsDown` (or anything ≥ it), `familyTree` threads a
**narrow main-line spine**: it finds the most-prominent descendants beyond the breadth
horizon (top 24 by prominence, `DEEP_SPINE_ANCHORS`) and walks each one's shortest `PARENT_OF`
path back to an already-included node, adding only that spine (not full sibling breadth) at
each deep generation — capped at depth 14 (`DEEP_SPINE_MAX_DEPTH`). **A caller passing an
explicit tight window (e.g. `generationsDown: 1`, below the default) opts OUT of the deep
spine entirely** and gets exactly the requested shallow window, verified live: `familyTree(
"aegon-i-targaryen", data, {generationsUp:1, generationsDown:1})` does NOT contain
`daenerys-targaryen`, while the default-parameter call does.

**Spouses:** attached at the **same generation as their partner** (snapshotted before
cascading, so a spouse's own spouse doesn't chain in).

**Invalid slug — verified non-obvious behavior, NOT symmetric with `neighbors`/`chain`:**
`familyTree()` on a slug with **no** node record does **not** return an empty member list —
it returns a **single-member tree containing a synthetic stub** for the queried slug itself
(`hasNode: false`, `degree: 0`, `quoteCount: 0`, `prominence: 0`, humanized-slug `name`,
`generation: 0`). `memberCount: 1`, `truncated: false`. This differs from `resolve` (`[]` on
invalid input) and from `neighbors`/`walkChain` (empty groups/arrays on invalid input) —
`familyTree`'s "invalid slug" case is actually "slug matches the regex trust-boundary but has
no backing node," which the function treats as "a person we've heard of via an edge but never
built a node for," not as a rejected input. The literal validate.ts trust-boundary rejection
(e.g. a slug containing `/` or `..`) is the one case that DOES return the fully-empty
`FamilyTreeResult` shown at the top of `graph.ts`'s `familyTree` doc comment. Golden case
`family.json` encodes both: a `../etc/passwd`-shaped reject vs. a well-formed-but-nonexistent
slug.

**Full-profile status:** **shipped.** `family` was the **first parity target** named in the
design doc (step 1, "Port `familyTree` TS→Python (same caps as constants; the first parity
op)"), and the port is now live: `weirwood_query.traverse.family_tree(slug, edges, nodes)` is a
line-for-line port of `graph.ts::familyTree` (same BFS, same caps, same deep main-line spine,
same trust-boundary gate via a verbatim `SLUG_RE` port of `validate.ts::isValidSlug`). CLI
invocation:

```
python3 -m weirwood_query.cli --family-tree <slug>       # legacy flag surface
python3 -m weirwood_query.cli family <slug>               # subcommand front door
```

Both print the JSON result (there is no text-mode rendering for `family` — it is JSON-only,
matching the original flag's behavior). The CLI builds the `nodes` map itself via
`traverse.build_family_nodes_map()` (reads every `graph/nodes/**/*.node.md` for
name/type/quote-count — the same fields `web/data/nodes.json`'s bundle build derives from the
same source files, so `prominence` and the deep-spine anchor selection match the TS side on
live data). All 6 `family.json` golden cases now run (and pass) under the Python runner
(`spec/run_cases.py`), not just the deno one — see that script's `try_family` for how it feeds
bundle-derived edges+nodes so the pinned TS-verified values (e.g. `aegon-i-targaryen`'s
`memberCount: 96`) hold on the Python side too.

---

## `health` / `census`

**Status:** full-profile only, by design — this is an in-repo diagnostic op, not a
user-facing query. **PLANNED to stay full-profile-only** (no bounded-profile target; the
design doc's op table lists it "Python only (full profile)").

**Full-profile semantics (`--health`):** graph-wide stats — node count, edge count,
edge-type distribution, top-N nodes by degree (`DEGREE_TOP_N = 20`), orphan/dangling-edge
counts. Read-only diagnostic used by audits and the reachability census (design doc §2a/§0).

---

## `search`

**Status: SHIPPED — step 5b (2026-07-04).** Answers descriptive/thematic/quote-hunting
questions ("describe some detailed meals", "what do people say about honor") that
`resolve`+`chain` cannot — those require an entity slug up front; `search` is content-first.

**Substrate:** every `## Quotes` line + every `## Identity` paragraph across `graph/nodes/`
(excluding `_conflicts/`) — 13,714 docs (6,057 quote + 7,657 identity) as of the 2026-07-04
build. Chapter full-text search is the separate, CLI-only `corpus-search` op (below).

**Mechanism:** a build-time tokenized inverted index (`graph/query/build/build_search_index.py`
— deterministic, no LLM, no embeddings, see design doc D-C) with request-time BM25 scoring:

```
idf(t)      = ln(1 + (N - df(t) + 0.5) / (df(t) + 0.5))
tf_sat(t,d) = tf(t,d) * (k1 + 1) / (tf(t,d) + k1 * (1 - b + b * (len(d) / avgdl)))
score(q,d)  = sum over t in q of idf(t) * tf_sat(t,d)
k1 = 1.5, b = 0.75  (standard Okapi BM25 defaults)
```

Tokenization is the shared `normalize.py` / `normalize.ts` word-pattern + stop-word set
(word-chars, lowercased), with a minimum token length of 2 — the query side and the
build-time doc side MUST use the identical rule or postings lookups silently miss (see
`search.py`/`search.ts`'s own header comments; `search.ts` imports `STOP` directly from
`normalize.ts` rather than keeping a second copy).

**Two index artifacts** (`build_search_index.py`'s two on-disk FORMATS — see that module's
docstring for the exact wire shapes):
- `working/wiki/data/search-index.json` — the FULL format (friendly dict-of-dicts, text
  inline; ~6.7 MB) consumed by the Python full-profile engine (`weirwood_query/search.py`).
- `web/data/search-index.json` — the COMPACT bundle format (array-based, delta-encoded
  postings, `text` NOT carried — reconstructed from `nodes.json` at request time; ~2.38 MB
  as of the 2026-07-04 build, within the ≤2.5 MB budget) shipped in the chat bundle and wired
  into `build_chat_bundle.py`'s manifest as a `search-index.json` size entry.

**Inputs:** `query: string`, optional `type` filter — the graph/nodes/ TYPE-DIRECTORY name
(e.g. `foods`; NOT the dotted frontmatter `type:` scalar like `object.food` — the two
vocabularies differ, see `build_search_index.py`'s comment on why), optional `limit`
(default 12, both profiles).

**Outputs:** ranked `{slug, type, text, cite, score}` — `type` is the category described
above; `cite` is a `chapter:line` string when the underlying quote carries one, else `null`
(identity-blurb hits never carry a cite; `read <slug>` is the provenance path for those).

**CLI:** `weirwood query search "lemon cakes" [--type foods] [--limit N] [--json]`.
**TS export contract:** `searchQuotes(query: string, opts?: {type?: string; limit?: number}):
SearchResult[]` in `web/src/lib/search.ts` (exported from `mod.ts`/`types.ts`) — NOT yet
wired as a chat tool in `agent.ts` (a separate follow-up agent's job per this Track's hard
gate); the exact `{slug, type, text, cite, score}` contract is kept stable for that wiring.

**Golden cases:** `spec/cases/search.json` (6 cases, profile "both") — "lemon cakes" (food
node reachable, invariant-mode since `lemon`/`lemon-cake` compete closely for rank 1),
"seventy-seven courses" (exact top = `purple-wedding` with a navigable book cite), "guest
right" (exact top = the `guest-right` custom node itself, not an incidental mention), a
`--type` filter case, and two no-result edge cases (nonsense query, whitespace-only query).

---

## `list`

**Status: SHIPPED — step 5d (2026-07-04).** Trivial browse — "list every node of type X"
(optionally filtered to quote-bearing nodes), paged.

**Inputs:** `type: string` (required — the graph/nodes/ category directory name; there is no
"list everything" mode), optional `has_quotes: boolean`, optional `container: string`
(full-profile only — see Profile difference below), `limit`/`offset` for pagination.

**Outputs:** `{category, total, offset, limit, items: [{slug, name, quote_count}]}` — `total`
counts every filter-matching node BEFORE paging (so `total - offset - len(items)` tells the
caller how many more remain). An unknown/empty category returns `total: 0, items: []`, not an
error (mirrors `container()`'s "no matches" convention — a typo is a query mistake, not a
system fault).

**Profile difference:** the full-profile Python `list_nodes()` supports a `--container NAME`
filter (reuses `traverse._node_containers`'s bag-retrieval parsing, scoped to one category).
The bounded/TS `listNodes()` has **no container filter** — `containers:` frontmatter is not
in the bundle yet (design doc step 6a, not done). Documented profile difference, not a bug.

**CLI:** `weirwood query list --type foods [--has-quotes] [--container NAME] [--limit N]
[--offset N] [--json]`.
**TS export:** `listNodes(data, opts): ListResult` in `web/src/lib/list.ts` — no chat tool
(gated on evals per the design doc).

**Golden cases:** `spec/cases/list.json` (2 cases, profile "both") — an exact full-listing
pin against the `customs` category (37 nodes total; chosen because it is free of the
duplicate-slug collisions found in `foods` during this step — see the spawned data-hygiene
follow-up task, `graph/query/spec/run_cases.py`/`spec_cases_test.ts` comments), and the
unknown-category-returns-empty case.

---

## `corpus-search` / `passage`

**Status: `corpus-search` SHIPPED — step 5e (2026-07-04); `passage` still DESIGNED-BUT-GATED,
NOT built.** `corpus-search` was deferred once already (S172) pending "a build-time inverted
index" (the mechanism `search` above now uses for the curated layer) — `corpus-search` itself
is a live, uncached scan, not index-backed, since chapter full-text search is explicitly
CLI-only and never needs to fit an edge-function CPU budget.

**`corpus-search` semantics (Python full-profile, CLI-ONLY — no bundle/chat exposure, per the
design doc's explicit instruction):** grep-class search over `sources/chapters/**/*.md`
(371 files), case-insensitive, line-by-line. Two modes:
- `phrase` (default): whole-phrase substring match (whitespace-collapsed on both sides).
- `tokens`: every whitespace/punctuation-stripped token of the query must appear on the
  line, any order (looser recall for topic-level matches).

**Inputs:** `query: string`, optional `book` (a `sources/chapters/` subdirectory name, e.g.
`agot`), `mode` (`phrase` default or `tokens`), `limit` (default 20).

**Outputs:** `{query, mode, book, total, limit, matches: [{cite, book, text}]}` — `cite` is a
`sources/chapters/<book>/<file>.md:<line>` string (1-indexed line number), the same format
node quotes already carry.

**CLI:** `weirwood query corpus-search "lamprey pie" [--book agot] [--mode phrase|tokens]
[--limit N] [--json]`. No TS port, no chat tool, no golden cases — this op never leaves the
CLI (`weirwood_query/corpus_search.py`'s own module docstring restates the gate).

**`passage` (edge-side, still gated, NOT built this step):** a static-asset fetch of chapter
text (`web/public/chapter/<slug>.json` or similar) consumed by `/api/node` or a chat tool at
request time — network I/O falls outside the Edge function's 50 ms CPU budget, unlike
in-memory bundle lookups. **Explicitly gated on Matt** before it ships to the public chat
(the session-C advisory-board fan-out decides `read_passage`-to-chat vs. CLI-only, per the
design doc §8). This step does not build `passage` — it only ships the CLI-only
`corpus-search` half.

---

## `mentions`

**Status: SHIPPED — step 8b (2026-07-04).** `weirwood_query/mentions.py` /
`weirwood query mentions <slug>` reads the LIVE `graph/index/chapters/` tree — the same data
`scripts/build-mention-index.py` writes today, which is real but **partially stale** (its
entity resolution predates the current hardened `all-node-alias-lookup.json` table). This op
does NOT repair that data (`graph/index/` is behind the no-graph-mutation gate) — it is a
read-only reader, exactly like `search.py`/`themes.py` read whatever their own builders last
wrote.

A **preview repair** exists alongside it (query-layer step 8b's other deliverable):
`graph/query/build/build_mention_index_preview.py` re-runs the SAME mention-extraction
algorithm over the SAME Pass-1 extractions, but resolves against the hardened
`all-node-alias-lookup.json` table instead — writing to
`working/query-layer/mention-index-preview/` (never to `graph/index/`). The measured delta,
sample diffs, and the reviewed apply command live in
`working/query-layer/mention-index-repair-report.md`. When the preview tree exists on disk,
`mentions()` compares its own live count against the preview count and returns a
`staleness_note` field when they differ, rather than silently trusting a possibly-wrong
number.

**Intended purpose:** "which chapters mention X" — full-profile only; bounded exposure
optional, not built this v1 (no evals showed a chat-side need yet).

No golden cases ship for `mentions` in this v1 — its data source is a live index the golden-
case discipline isn't a natural fit for (the "expected" mention counts would drift every time
`graph/nodes/`/`extractions/` change, unlike the other pinned ops).

---

## `theme`

**Status: SHIPPED — step 8a (2026-07-04).** `graph/query/build/build_theme_index.py` builds a
deterministic theme→members table (seed themes: meals & feasts, hospitality, dress &
materials, maesters & healing, songs & tales) — membership by node-type wholesale rules +
whole-word/whole-phrase keyword matching over names/aliases/identity/quotes text (never a raw
substring match — see that module's docstring for the false-positive class avoided, e.g.
"harp" inside "Harpy's"). This is the "trigger table"'s routing half (D8), scoped narrowly —
not a general tagging system, and not the settled 5-container axis (`container`, above) which
stays event-only.

Two profiles: `weirwood_query/themes.py` / `weirwood query theme [name] [--category CAT]`
(full; no name lists every theme + member_count) and `web/src/lib/themes.ts`'s `theme()` /
`listThemes()` (bounded, reads `web/data/theme-index.json` shipped in the bundle — 28.1 KB,
measured this session, negligible against the ~12.4 MB total).

**Golden cases:** `spec/cases/theme.json` (5 cases, profile "both") — `lemon-cake` in "meals &
feasts", `guest-right` in "hospitality", case-insensitive name matching, the `category` filter,
and the unknown-theme-name error path.

---

## `braid` / `fork-hubs` / `join-hubs`

**Status: SHIPPED — step 7 (session, 2026-07-04).** The S117 charter
(`graph/convergence-maps/README.md`) is now implemented in
`graph/query/weirwood_query/braid.py`, full-profile-only by design (pure DAG analysis over
causal(+`ENABLES`) edges; no chat port — matches the design doc's op table:
`braid / fork-hubs / join-hubs | ❌ (charter only) | ❌ | Python only (step 7)`). This op
family does **not** write to `graph/convergence-maps/` yet — these are read-only reports;
the charter's "named convergence map" output files remain a separate, Matt-gated deliverable
(unblocked by this step, not built by it).

**Inputs / outputs:**
- `fork-hubs [--min-out N] [--include-enables] [--json]` — divergence hubs: nodes whose
  **direct** outgoing causal (or causal+ENABLES) degree is `>= min_out` (default 2), ranked
  by out-degree descending, ties broken by slug. Each hub also reports `downstream_reach`
  (the size of its transitive downstream set) as context, since direct fan-out and
  transitive reach can diverge sharply (see the hairnet note below).
- `join-hubs [--min-in N] [--include-enables] [--json]` — the in-degree analog:
  convergence points, `upstream_reach` reported alongside.
- `braid <slugA> <slugB> [more...] [--include-enables] [--json]` — for 2+ endpoint slugs,
  walks each one's transitive upstream/downstream causal reach and reports: **shared
  ancestors** (nodes upstream of every strand — a common divergence point), **shared
  descendants** (nodes downstream of every strand — a convergence point), and, per strand
  pair, an **offset/shared-middle** set (nodes upstream of one strand and downstream of
  another — the "shared spine, different entry/exit" shape). Each strand's full
  `causal_chain()` result is included under `per_strand[slug]`.

**Decisions made where the charter under-specified (documented in `braid.py`'s module
docstring in full; summarized here):**
1. Default edge set is `CAUSAL_EDGE_TYPES` (matches `chain`'s default); `--include-enables`
   widens to `FULL_CHAIN_EDGE_TYPES`, mirroring the existing `chain`/`chain --full` split.
2. `fork-hubs`/`join-hubs` rank by **direct** degree, not transitive reach — a decidable,
   O(E) definition matching the charter's own tooling-sketch wording ("ranked by downstream
   fan-out"). This means the hairnet node itself (`sansa-receives-the-poisoned-hairnet`,
   direct CAUSES out-degree **1**, but a downstream causal-chain reach of ~20 nodes) does
   **not** top the `fork-hubs` ranking by direct out-degree — nodes like
   `battle-of-the-blackwater` (out=4) or `jaime-reveals-the-truth-of-tysha` (out=3, reach 11)
   do. `braid`'s shared-ancestor/descendant report is where the hairnet's real role (a
   one-hop-removed shared ancestor of multiple downstream terminal events) actually surfaces
   — verified live: `braid assassination-of-tywin-lannister death-of-joffrey-baratheon`
   returns `sansa-receives-the-poisoned-hairnet` as the sole shared ancestor.
3. `braid`'s "shared ancestors"/"shared descendants" are the intersection **across all**
   given strands (N-ary); pairwise offset/shared-middle sets are reported per strand-pair
   separately, since an all-strand offset intersection is often empty once N > 2 while
   pairwise crossings remain informative.
4. No hard-stop enforcement inside `braid`/`join-hubs` (they are read-only reports, not a
   chain-building tool) — a caller distinguishes "a meaningful two-cause convergence" from
   "a graph-wide super-hub" by eye, using the reported degree/reach numbers as context.

**Golden cases:** `spec/cases/braid.json`, tagged `profile: "full"` (Python-runner-only by
design — the deno case runner registers these as `ignore: true` tests, per its own
docstring's handling of full-profile-only cases, so `deno task test` stays at the same pass
count). Invariant-style asserts (membership + degree floors), not exact dumps, per the
mission's "the graph grows" note. Run via `PYTHONPATH=graph/query python3
graph/query/spec/run_cases.py`.

---

## Appendix — open naming/shape mismatches this v1 records but does not resolve

These are real, verified differences between the full and bounded implementations that are
**not** profile-capability differences (like depth caps) — they're accidental drift from two
independent implementations, flagged for step 1's consolidation to either fix or formally
ratify as permanent:

1. **Field naming:** bounded uses `source`/`target`/`ref`/`tier`/`evidence_quote`; full's JSON
   mode uses `source_slug`/`target_slug`/`evidence_ref`/`confidence_tier`/`evidence_quote`
   (this one already matches). `resolve`'s candidate shape: bounded `{slug, category, score,
   matchType, prominence}` vs. full's `{slug, score, match_type, node_category, node_type}`
   (`match_type` snake_case vs. `matchType` camelCase; `node_category` vs. `category`; no
   `prominence` field in the Python candidate shape at all — prominence-based tie-break is
   TS-only today).
2. **`resolve` status enum:** full has 5 statuses (`hit`/`hit-character`/`candidates`/
   `ambiguous`/`miss`); bounded has none — it returns a candidate list or `[]`, with
   `matchType: "exact"|"fuzzy"` per-candidate instead of a top-level status. `ambiguous` in
   particular has no bounded equivalent.
3. **`chain` link ordering:** bounded sorts causal chains by story-time (S185); full's CLI
   sorts upstream/downstream by depth then slug — a real behavioral divergence today, not
   just a caps difference (see `chain` section above).
4. **`neighbors` dedup:** verified present (tested) in bounded; not verified/confirmed
   identical in full — candidate parity-audit item for step 1.
5. **`ChainResult` has no `truncated` flag** (unlike `FamilyTreeResult`) even though its
   per-direction link cap can silently truncate a dense hub's walk — a gap worth closing
   when `chain` and `family` are reconciled under one engine.
6. **G16 — two edge serializations:** `read`'s positional full-profile mode reads node-file
   `## Edges` markdown; every other full-profile op reads `edges.jsonl`; nothing cross-checks
   them today.

---

## Appendix — session log

- **2026-07-04 (S189, step 1 / session A):** v1 written. Grounded against the live TS engine
  (`web/src/lib/{resolve,graph,normalize,types,mod,data,read-node}.ts` + `graph_test.ts` +
  `resolve_test.ts`) and the live Python scripts (`scripts/graph-query.py`,
  `scripts/event_alias_resolver.py`), with direct runtime probes against the real bundle
  (`web/data/`) for `resolve`, `neighbors`, `chain`, `family` — not inferred from the design
  doc's prose alone. Confirms G19 (victim-phrase bundle gap) and G2 (`lemon cakes` miss) live;
  surfaces one behavior not previously documented anywhere: `familyTree` on a well-formed but
  non-existent slug returns a **1-member synthetic-stub tree**, not an empty tree — distinct
  from `resolve`/`neighbors`/`walkChain`'s empty-on-invalid convention.
- **2026-07-04 (S189, step 1 close-out):** `family` port landed — `traverse.family_tree` now
  gates on a verbatim `SLUG_RE` port of `validate.ts::isValidSlug` (previously only checked
  falsy, silently under-rejecting `../etc/passwd`-shaped input), `cli.py --family-tree` now
  loads and passes the nodes map (`traverse.build_family_nodes_map()`) instead of calling
  `family_tree` edges-only, and all 6 `family.json` golden cases run under `run_cases.py`
  (previously bounded-only). Subcommand front door (`weirwood query family <slug>`, `chain`,
  `resolve`, etc.) added as an additive translation layer in `cli.py::main()` — legacy flags
  unchanged.
- **2026-07-04 (S189, step 7):** `braid`/`fork-hubs`/`join-hubs` shipped
  (`graph/query/weirwood_query/braid.py`), un-deferring the S117 convergence-map charter.
  Full-profile only, no chat port, no writes to `graph/convergence-maps/` (that remains a
  separate Matt-gated deliverable). Verified live: `fork-hubs --min-out 3` surfaces
  `jaime-reveals-the-truth-of-tysha` (out=3, reach=11) and the 3 out=4 hubs
  (`battle-of-the-blackwater`, `kingsmoot-on-old-wyk`,
  `murder-of-elia-martell-and-rhaegars-children`); `gregor-confesses-and-kills-oberyn` clears
  at `--min-out 2` (the charter's own Oberyn-fork example). `braid
  assassination-of-tywin-lannister death-of-joffrey-baratheon` returns
  `sansa-receives-the-poisoned-hairnet` as the sole shared ancestor — confirming the design
  doc's verification anchor. 5 golden cases added (`spec/cases/braid.json`, `profile: "full"`)
  + `run_cases.py` extended with `try_fork_hubs`/`try_join_hubs`/`try_braid`; all pass.
  `deno task test` stays 66/66 (full-profile-only cases register as `ignore: true`, per the
  existing runner's own handling — no TS file touched). Legacy pytest suites
  (`test_graph_query_edges.py`, `test_graph_query_hardening.py`) untouched, still 48/48.
- **2026-07-04 (S189, step 5a/b/d/e — session B, the search substrate):** `search`/`list`/
  `corpus-search` shipped. Build-time inverted index (`build/build_search_index.py`) over
  13,714 quote+identity docs (17,520 unique tokens), two formats: FULL
  (`working/wiki/data/search-index.json`, ~6.7 MB, text inline) and COMPACT
  (`web/data/search-index.json`, ~2.38 MB — array-based docs/doc_lengths, delta-encoded flat
  postings, IDF rounded to 4 decimals; the naive dict-of-dicts-both-copies approach measured
  ~6.7 MB / ~4.1 MB before this compaction). BM25 (k1=1.5, b=0.75), documented once, both
  engines implement the identical formula. `weirwood_query/search.py` + `web/src/lib/search.ts`
  (exports `searchQuotes(query, opts?): SearchResult[]`, the exact contract a follow-up
  chat-tool-wiring session will consume); `weirwood_query/list_nodes.py` +
  `web/src/lib/list.ts`; `weirwood_query/corpus_search.py` (CLI-only, no TS port, per the
  design doc's explicit gate). Discovered `nodes.json` had no per-node category field
  (needed for `--type`/`list`'s category filter, distinct from the frontmatter `type:`
  scalar) — added `category` to `build_chat_bundle.py`'s `load_nodes()` and `NodeRecord`
  (the only nodes/edges/alias-map bundle change this session; edges.json and alias-map.json
  are byte-identical before/after). Verified spot-checks: "lemon cakes" → `lemon-cake`/`lemon`
  food nodes reachable top-3; "seventy-seven courses" → `purple-wedding` exact top with a
  navigable Sansa-POV cite; "guest right" → the `guest-right` custom node itself ranks first.
  8 new golden cases (`spec/cases/search.json` ×6, `spec/cases/list.json` ×2, profile "both"),
  registered in both `spec_cases_test.ts` and `run_cases.py` — all pass on both runtimes.
  `deno task test`: 75/75 (was 67/67). `run_cases.py`: 25 passed / 1 skipped (unrelated
  pre-existing neighbors-full-profile placeholder) — was 17/1. `pytest tests/`: 1322
  passed / 3 pre-existing fails (unchanged baseline). Found — but did NOT fix, per the
  no-graph-mutation gate — a pre-existing data-hygiene issue: at least 4 slugs
  (`sweetsleep`, `peach`, `porridge`, `sourleaf`) exist as separate node files under two
  different `graph/nodes/` category directories each, causing `build_chat_bundle.py`'s
  slug-keyed dict to silently let one category's version clobber the other's in the shipped
  bundle; spawned a follow-up task to survey and propose fixes (G18-style, gated on Matt).
  `weirwood-refresh.sh` gained a 4th builder step (`build_search_index.py`); the bundle
  quartet (`build_chat_bundle.py`) stays a separate manual pre-deploy step, unchanged.
