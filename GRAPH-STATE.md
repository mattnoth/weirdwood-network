# Weirwood Network — Current State of Things

> **Companion to `GRAPH-QUERY-ROADMAP.md`.** That doc is forward-looking (traversal/query
> gaps + roadmap). THIS doc is a **snapshot of where the graph and the chat-UI stand right
> now** — counts, coverage, what's shipped, what's parked. Some overlap with the roadmap is
> intentional. Started 2026-07-04; refresh as state changes. Sourced from `worklog.md` STATUS
> + archives S82–S187 + live repo census.
>
> **→ S191: the query-layer Track closed.** The query surface described in §3's "chat-UI"
> snapshot now runs through ONE engine (`graph/query/`, `weirwood query …`) with a
> pytest+deno drift alarm and a 116-test traversal suite; the old `scripts/` query shims
> are deleted. See `working/query-layer/design.md` (status header) for the full record.
>
> **Authority note:** `worklog.md` is the live source of truth. If this doc and the worklog
> disagree, the worklog wins — this is a point-in-time snapshot.

---

## 1. The graph, by the numbers **[census 2026-07-04]**

- **~8,727 node files on disk** across **21 node types** (`graph/nodes/`); the bundle ships
  **8,473** (the 254 excluded = the `_conflicts` staging bucket).
- **~23,099 edges** shipped (`graph/edges/edges.jsonl`; peaked ~23,330, net of cleanup passes).
- **Quote layer:** 1,595 nodes carry quotes; **6,053 quotes total** (~19% of nodes).
- **Alias layer:** 12,139 phrase→slug entries (`alias-map.json`).

**Node type distribution** (top): characters 3,916 · locations 1,098 · houses 556 · titles 542 ·
events 744 · artifacts 295 · factions 191 · species 188 · texts 161 · **foods 113** · religions
63 · materials 58 · concepts 57 · theories 45 · customs 37 · medical 35 · languages 26 ·
prophecies 4. Plus chapters 344, `_conflicts` 254 (staging).

**Pipeline status:** Pass 1 (mechanical extraction) DONE — 344/344 chapters, all 5 books, all
Opus. Pass 2 (wiki ingestion) DONE. Indexes built (21 categories). Passes 3–6 (analytical) not
started as sweeps — superseded in practice by the dip-driven enrichment model below.

---

## 2. The enrichment story — how the graph got its shape

The graph started as a flat Pass-1/Pass-2 node layer, then got **deepened by dips** — targeted,
verified enrichment passes over one arc at a time. This is why the graph is **event-and-causal
rich**: nearly all enrichment investment went into wiring event hubs into causal chains.

**Key design decisions (traversal-relevant — detail in `GRAPH-QUERY-ROADMAP.md` §1d):**
- **Event reification** (S82–84): n-ary events → event-node hubs + role edges.
- **Chain-as-arc, NO umbrella parents** (S105/106): an arc is a CAUSES/TRIGGERS/MOTIVATES chain
  you *walk*, queried via `--causal-chain`. Superseded the earlier conspiracy-parent idea.
- **Arc enrichment track** born S116: second-pass deepening (side-arcs, revelation-events,
  descriptive depth); `SUSPECTED_OF` edge for unproven actor→event agency ("whodunit, honestly").
- **Containers** (S121–122): frontmatter array tag; **5 settled** — `essos`, `wo5k`, `north`,
  `aegon`, `bran`.

**Major-arc dips DONE (~27, S133–S167)** — Robert's Rebellion · Red Wedding · Purple Wedding ·
Ned's Downfall · Blackwater · Tywin's Death · Cersei's Downfall · Brienne→Stoneheart · Sack of
KL · Daenerys/Meereen · Jon/Wall · Bran/greenseer · AEGON/Golden Company · Sansa/Vale ·
Theon/Reek · Arya/Braavos · Battle of Castle Black · Arya/Harrenhal · Stannis · Dorne/Queenmaker
· Kingsmoot/Euron · Jaime/Riverlands · Tyrion/Essos · WO5K-battles (3 passes) · Davos/Sam. **The
"A-roundup" of major arcs is CLOSED (S167).**

**Coverage taxonomy** (from `working/enrichment-coverage-plan.md`): Class A = un-enriched L1
arcs (DONE) · Class B = L2 sub-plots (DONE S151) · Class C = character webs (come free with
arcs) · Class D = big event-clusters no single POV owns (partially done — Castle Black S153,
Arya/Harrenhal S154; Hand's Tourney, Greyjoy Rebellion, Riot of KL remain).

**What enrichment did NOT do:** build out the descriptive/entity layers (foods, customs,
materials, dress, hospitality) with the same depth. Those exist as nodes + scattered quotes but
were never given a *traversal mode* or a second enrichment pass. **This is the gap the
`GRAPH-QUERY-ROADMAP.md` is about.**

### 2a. The descriptive-layer census — hard numbers **[deterministic measure 2026-07-04]**

Measured directly off the shipped bundle (quote-density + edge-degree per node type). This is
the authoritative "where is the graph thin" answer — sharper than any worklog prose.

**Events are WIRED and reachable** (enrichment went here):
| type | nodes | % w/quote | avg degree | % islanded (0 edges) |
|---|---|---|---|---|
| event.incident | 160 | 70% | 4.75 | **1%** |
| event.assassination | 20 | 60% | 6.25 | 0% |
| event.conspiracy | 11 | 55% | 6.55 | 0% |
| event.death | 80 | 20% | 4.31 | 0% |
| event.battle | 286 | 38% | 3.55 | 22% |
| character.human | 3,878 | 26% | 6.60 | 3% |

**The descriptive/entity layer is quote-sparse AND massively ISLANDED** (nodes float, unwired):
| type | nodes | % w/quote | avg degree | **% islanded** |
|---|---|---|---|---|
| **object.food** | 110 | 51% | 0.16 | **96%** |
| object.artifact | 295 | 8% | 0.40 | **82%** |
| object.text | 161 | 1% | 0.16 | **94%** |
| object.material | 58 | 0% | 0.17 | **91%** |
| concept.custom | 47 | 4% | 0.06 | **96%** |
| concept.medical | 35 | 9% | 0.17 | **89%** |
| concept.language | 26 | 0% | 0.23 | **92%** |
| species | 188 | 1% | 0.29 | **90%** |
| place.location | 1,065 | 9% | 2.34 | **61%** |

**Three findings that reframe everything:**
1. **The descriptive layer is graph-ORPHANED, not just under-queried.** 96% of food nodes, 91%
   of materials, 96% of customs have **zero edges**. They're islands — reachable only by a
   direct `resolve` hit, never by `neighbors`/`walk_chain`/`--container`. (Food is the *best* of
   them at 51% w/quote — but still 96% islanded.)
2. **Quotes concentrate on CHARACTERS (73% of all 6,053 quotes), events get 12%, and the whole
   descriptive layer gets 3%.** So the quote-hunter archetype is *partly* served — but only for
   characters. Food/custom/material/etc. are quote-starved.
3. **The container/thematic index is 100% events.** All 5 containers (essos 37 · wo5k 58 · north
   32 · aegon 12 · bran 13) tag *only* event nodes — zero foods, locations, characters. So
   `--container essos` returns Essos *events*, never Essos meals or halls. The thematic axis
   exists but is event-only — which is why it only *partially* answers thematic questions.

**Bottom line:** enrichment built a dense, wired, contained EVENT core with quote-rich
CHARACTERS around it. The descriptive/entity layer (food, customs, materials, dress, texts,
species) is a **quote-thin ring of orphan nodes**, wired to nothing and absent from every
thematic index. That ring is exactly what the quote-hunter / thematic / researcher archetypes
reach for — and it's the emptiest part of the graph.

### 2b. WHY the descriptive layer is orphaned — the harvest mechanism **[arc-by-arc, S133–S168]**

Reading every dip S133–S167 explains the census precisely. The descriptive material was NOT
ignored — it was **captured but never wired**. Each dip ran a **4-lens machine**, and one lens
was always **"descriptive-object"** — so food/dress/hospitality detail was actively hunted. But
its output went to the **harvest queue** (`working/harvest-queue.md`) as *pointers*, and the
periodic **harvest-drain** passes did two things, neither of which wires a node:

1. **Attach a quote to an EXISTING node** — mostly characters/events (this is why characters
   hold 73% of quotes).
2. **Mint an isolated `object.food` node** carrying its quote but **no edges**.

Food-node growth traces this exactly: ~75 → 83 (S139) → 88 (S152) → 104 (S162) → 110 (S165) →
113. Every mint added a quote-bearing but **edge-less** node. The harvest machine's contract was
"attach quote" / "mint food node," never "wire this food into the causal or thematic graph."
Hence food = 51% w/quote (harvest worked) but **96% islanded** (wiring was never in scope).

Representative dips (all ran the descriptive lens → harvest, none wired the descriptive nodes):
- **S135 Purple Wedding** — 77-course feast captured (14 harvest rows); Matt set the LOW bar
  ("food/meal descriptions incl. mundane/grim ones like gruel are first-class").
- **S137 Ned's Downfall / S138 Blackwater** — ~165 + 33 food-heavy rows (boar funeral-feast,
  Flea-Bottom bowl-o'-brown, black-cells water/wine-dregs).
- **S156 Dorne** — wide Dornish food register (7-course Balon Swann feast, snake-sauce, blood
  oranges, prison rations).
- **S161 Tyrion/Essos** — Illyrio's feasts, shipboard rations, slave-camp dog stew.
- **Harvest-drains** S139/S152/S157/S162/S165/S168 — parallel Sonnet attachers on disjoint
  node-dirs; minted the isolated food nodes + attached quotes to existing nodes.

**The lesson for rebalancing:** the content was already gathered (the descriptive lens ran every
dip). What's missing is a **wiring step** — an edge grammar for descriptive nodes (e.g.
`SERVED_AT` food→feast-event, `DESCRIBED_IN` →chapter, container tags on food/location nodes) so
the orphan ring joins the graph. This is cheaper than re-reading the text: the quotes and nodes
exist; they just need edges and index membership.

---

## 3. The chat-UI — LIVE

- **Deployed (S183):** https://weirwood-network.netlify.app — Netlify Edge / Deno runtime.
- **Model:** governed by `WEIRWOOD_MODEL` env var (prod currently Opus per DEPLOY memory; was
  Sonnet 4.6 at S183 launch — verify live). Server-side API key; browser never sees it.
- **Persona:** Bloodraven default + Loremaster toggle (S186); ≥2 verbatim book quotes per answer.
- **Retrieval tools (5):** resolve · read_node · walk_chain · neighbors · family_tree.
- **Guardrails:** daily spend cap ($50, was $5 at launch) · cite-verification gate ·
  theory-scope guardrail (no unrevealed-secret winks) · per-turn cost/usage logging to Netlify
  Blobs (`weirwood-chat` store; read via `web/scripts/read-logs.ts`).
- **Build history:** Foundation S171 → retrieval-core S172 → function S173 → front-end S174 →
  design evals S176/S177 (chain-display rebuild + unified `[[q|…]]` quote system) → deploy S183
  → chronology sort_keys S184/S185 → cite-verification false-positive fix S187.
- **Known live issues:** event-bias in tool selection (this session's investigation — see
  roadmap G3/G10); Narrative Arc prose not shipped in the bundle (roadmap G9); resolver alias
  holes (roadmap G2). Out-of-order causal chains were diagnosed as a `walkChain()` render bug
  (sorts by depth), NOT bad data — fix tracked at S185.

---

## 4. What's PARKED (deferred tracks — don't restart unprompted)

- **Granular character/event dips** — planned (S168, `working/granular-dip-plan.md`, opener =
  Hand's Tourney) then PARKED when Matt pivoted to the chat-UI alpha.
- **D&E Pass-1** (Dunk & Egg) — PARKED by Matt (its own `worklog-dunk-egg.md`, DE-N numbering).
- **SIFT corpus-scanner** — Stage 1 Python built, Stage 2 Haiku deferred; parked until after
  enrichment (`working/sift/`).
- **Theories layer** — GATED until Matt says "start theories"; theory *readings* stay gated even
  when the evidence substrate is built (`working/theories-staging/`).
- **`first_available` / spoiler gating** — deferred to post-first-release; backfills via
  deterministic script. Do NOT re-float as an open design question.
- **fuzzy-resolve resolver track** — the alias-coverage/marquee-name work (S177); now diagnosed
  in the roadmap (G2/G10).
- **Concurrent enrichment** — deferred (monolithic `edges.jsonl` blocks parallel mints).

---

## 4b. Backlog salvage — un-done items worth not losing **[swept from worklog + todos.md 2026-07-04]**

A full sweep of `worklog.md` Ideas&Backlog + `working/todos.md` for surfaced-but-never-done
work. Grouped by relevance to the traversal/query/descriptive themes.

**Traversal / query (on-topic for `GRAPH-QUERY-ROADMAP.md`):**
- **Convergence maps / the "braid" layer** — DESIGNED, NEVER BUILT. Charter exists
  (`graph/convergence-maps/README.md`) proposing query primitives `--braid` / `--fork-hubs` /
  `--join-hubs` to find where causal chains diverge/converge/offset (the hairnet as a divergence
  hub). `graph/convergence-maps/` holds only the README; 0 modes in `graph-query.py`. Was gated
  on "denser causal layer" — that gate is now PASSED (all containers spine-complete + enriched).
- **Trigger table** — "the one unshipped piece of the index layer." The index has per-category
  files but no routing/trigger schema. Principle #5 ("the index routes, the graph traverses")
  is half-built — the *routing* half is missing. Relevant to a content/search index (roadmap D1).
- **Resolver Track 7** — the basic alias fix shipped S96 (natural phrasings), but the
  marquee-name / plural cases (our G2/G10) re-emerged S177 and remain. Note: the Python resolver
  indexes death/execution hubs by victim ("Robb Stark's death" → `robb-is-killed`); **VERIFIED
  S189: the TS bundle's alias-map does NOT carry it** ("robb stark's death" / "ned stark's
  execution" → MISS in `web/data/alias-map.json`) — a confirmed portability gap, fix scoped as
  step 4a of `working/query-layer/design.md`.
- **MCP server for programmatic graph access** (LOW backlog) — fits the "query layer as a
  first-class product" / portfolio framing (roadmap §4).

**Descriptive layer (on-topic for the orphan-ring, §2a/§2b):**
- **Python food-keyword grep for full-corpus meal coverage** — DEFERRED, gated post-enrichment
  (gate now passed). Deterministic (dish names + eat/feast/supper/starv*/bread/meat/wine…) over
  all 344 chapters → candidate `chapter:line` rows. Matt's explicit steer: Python, NOT an LLM
  sweep. Pairs with the `object.food` layer — a cheap way to grow + wire the food ring.
- **Prophecy layer** — undercounted (4 nodes, ~0 edges); mint the canon prophecies (Azor Ahai,
  valonqar, dragon-has-three-heads) from existing wiki pages. (Theory *readings* stay gated.)
- **Book-cite overlay sweep** — deterministic-ish pass overlaying navigable book cites onto
  wiki-only marquee quotes (memory: high-value). Upgrades Tier-2 → Tier-1 provenance.
- **TWOIAF ingestion** — `sources/raw/TWOIAF.txt` (1.5 MB) is ON DISK but NEVER Pass-1-extracted.
  Would convert ~300 isolated historical hubs (Doom of Valyria, Blackfyre, the Dance) from
  Tier-2 wiki to book-grounded. Cheapest non-saga source (F&B isn't even on disk).

**Portfolio / legibility (on-topic for the interview framing):**
- **"How it works" / design-philosophy page** — an expanded, portfolio-legible page showing the
  data model (entities→nodes, the trust-tier gap, typed edges, the causal-chain + receipts
  model) *as* the chat works. About page shipped (S176); the fuller design-doc page did not.
- **Portfolio README + demo design** (LOW). **Fanfic / grounded-generation** downstream use (LOW).

**Graph hygiene (off-topic but genuinely un-done — don't lose):**
- `valyrian-steel` mistyped `object.artifact` → should be `object.material` (blocks `MADE_OF`
  edges; S159). Passes 3/4/5 prompts (voice / foreshadowing / theory) never written. Post-Plate-5
  followups (#1 display-bullet regen, #6/#11/#13). Edge-backfill Tracks A/B/C (~$25–75, 300–850
  edges, GATED). Infobox-merge v2.1 per-fact citation backfill. Graph-wide causal-wiring track
  (PARKED). Two PreToolUse hooks (block writes under `sources/` + `history/`). `weirwood refresh
  --check` pre-commit hook.

---

## 5. Live / next tracks

- **chat-UI alpha-tester notes** — `progress/continue-prompts/2026-07-01-chat-ui-alpha-tester-notes.md`.
  The event-bias investigation this session belongs here.
- **GRAPH-QUERY-ROADMAP.md** — this session's spitball on the traversal/query surface; the
  emerging plan is un-defer content-search (D1) + finish fuzzy-resolve (G2/G10) + port the
  divergent Python query modes (`--container` etc.) to the chat + tune walk_chain (G3).
- **Chronology / event-ordering** — there WAS an event-ordering bug: live causal chains rendered
  out of story-time order. Diagnosed S184 as a **`walkChain()` render bug** (it sorted by hop-depth,
  not chronology — NOT bad data; 0 causal temporal inversions in the graph). **Mostly fixed:**
  - **Step A (DONE S185, deployed S186):** `sort_keys.composite`/`reading_order` carried into the
    bundle; `walkChain` sorts each direction by story-time; render split into "What led to this" /
    "What followed". Bran-chain regression test green (39/39). Composite `"0298.1.018"` vs
    reading_order `"1.015"` aren't lexically comparable → undated events get a book→AC-year
    synthesized key.
  - **Step D (DONE S185):** intra-chapter inversion scan → 0 genuine inversions.
  - **Step B (DONE S186, LIVE):** per-turn usage logging (the substrate this whole S188 analysis
    read from).
  - **Step C (OPEN — gated on Matt):** deterministic wiki-date backfill of the ~50 undated causal
    events → Haiku residue (NOT Fable). The one remaining piece of the S185 handoff. Optional;
    gated on Matt's OK for any Haiku pass. `progress/continue-prompts/` chronology prompts archived.

---

## Appendix — session log for this doc
- **2026-07-04:** created as the companion state-snapshot to GRAPH-QUERY-ROADMAP.md. Census +
  enrichment coverage + chat-UI live status + parked tracks captured from worklog S82–S187.
- **2026-07-04 (cont.):** "went all the way in" — ran the deterministic descriptive-layer census
  (§2a: quote-density + islanding per type; the 96%-islanded-food finding, the containers-are-
  event-only finding) AND read every enrichment dip S133–S167 arc-by-arc (§2b: the harvest
  mechanism — descriptive material was captured to the harvest queue and either attached to
  existing nodes or minted as isolated edge-less food nodes, never wired). Root cause of the
  orphan ring identified: harvest had no wiring step.
- **2026-07-04 (cont.):** swept `worklog.md` Ideas&Backlog + `working/todos.md` for
  surfaced-but-never-done work → §4b backlog salvage. Standouts: the charter'd-but-unbuilt
  "braid"/convergence-map query primitives (`graph/convergence-maps/` = README only), the
  unshipped trigger table, TWOIAF (1.5 MB, never extracted), the deferred Python food-grep.
  Added D7 (braid) + D8 (trigger table) to the roadmap.
- **2026-07-04 (S189):** master design for the query-layer track landed at
  **`working/query-layer/design.md`**. State-relevant S189 census updates: total orphan nodes
  27.8% (2,358/8,468); artifacts are edge-*sinks* only (0 out-edges even on Iron Throne /
  Longclaw); 5 YAML-broken node files; 91 dangling edge endpoints; the victim-alias bundle gap
  CONFIRMED (see §4b); `graph/index/foods/*` entries are EMPTY for harvest-minted nodes
  (`acorn-paste`: 0 appearances) — the index layer is unrouted AND stale.
