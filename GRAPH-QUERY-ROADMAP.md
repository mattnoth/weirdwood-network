# Graph Query & Traversal — Roadmap / Gaps / Ideas

> **→ S189 (2026-07-04): the master design landed at `working/query-layer/design.md`.**
> That doc is now the **plan of record** for the query-layer track — it confirms/revises
> every gap below (verdicts on G1–G10, new gaps G11–G19), takes the decisions (D-A…D-I),
> and sequences the work into executable step cards. THIS doc remains the diagnosis/history
> record; don't extend §3/§4 here — extend the design doc.
>
> **Status: LIVING SPITBALL DOC.** Started 2026-07-04. Being built and refined across
> this session and the next. Nothing here is decided unless a line says DECIDED.
> Sections marked **[grounded]** are verified against the repo; **[spitball]** are ideas.
>
> **Purpose:** figure out how people will actually *reach into* this graph — beyond the
> event-and-traversal shape it was built for — what's missing, what scripts/tools would
> help, and how to organize the traversal layer so it reads as a first-class part of the
> graph (portfolio / interview framing), not scratch work in `working/`.
>
> **Companion doc:** `GRAPH-STATE.md` = the current-state snapshot (counts, enrichment
> coverage, what's shipped/parked). THIS doc is forward-looking traversal/query design.
> Some overlap is intentional.

---

## 0. The reframe that kicked this off

The chat-UI feels like *every* question resolves to an event and walks a causal chain —
even a question like "describe some detailed meals." Root cause is **not** the model
preferring events. It's the **retrieval surface**:

- Every turn is forced through `resolve → node`, and `walk_chain` carries the most
  emphatic `MANDATORY / you MUST` language in the whole system prompt, so it over-fires.
- There is **no content-first way in** — no quote search, no thematic aggregation. If a
  question isn't "tell me about this *named* node," it has to degrade into the traversal
  machinery.

Enrichment history explains the tilt: enrichment dips + narrative-arc containers poured
almost everything into **events and their causal wiring** (CAUSES / TRIGGERS / MOTIVATES).
The descriptive/entity layers (food, customs, dress, hospitality, materials) got captured
as **quotes hanging off nodes**, but never got a *query mode* of their own.

### LIVE EVIDENCE — the failure, reproduced on the deployed UI (2026-07-04)
Ran *"Describe some detailed meals and feasts from the books"* against the live loremaster
(local `weirwood-live` server, real model). The receipts panel showed the model fire **~13
`resolve` calls in a row**, brute-forcing phrasings because it has no content-search tool:
- feast-at-Winterfell / Red-Wedding-feast / King's-Landing-feast / purple + Joffrey wedding
  feast / Night's-Watch feast → **every hit `(fuzzy)`, all events/weddings/factions** (G10).
- "Tyrion eating meal food" / "Lord Commander's feast Castle Black" / "Sansa Stark lemon cakes
  meal" / "Tyrion dinner supper eating" / "Catelyn arrival Twins feast food" → **5× `no match`**
  on reasonable phrasings (G2).
- "lemon cakes" → foods `(fuzzy)` — the ONE time it reached the food layer, but those nodes are
  96% islanded (§2a) so there was nowhere to go.
- **Zero exact hits. Zero `read_node`. Zero `walk_chain`. No quote. No answer.** It exhausted its
  step budget on resolve and hit the loop bound: *"The search was bounded. The loremaster reached
  its limit of graph steps for this question."*

This single turn fires **every gap at once** (G1 no-search → the flailing · G2 alias holes → the
no-matches · G10 fuzzy→events · §2a orphan food ring) and ends in a `loop-bound-hit`. It's the
compounding of the two shrinks: the *incidental* shrink (no content search, alias holes) caused
the flailing; the *essential* shrink (the 6-iteration bound) guillotined it. **One content-search
tool answers this in a single step and never approaches the bound** — the proof that widening the
incidental shrink is the whole fix. (This receipts screenshot is a portfolio-grade "problem"
exhibit.)

### Two apertures onto one graph — essential vs. incidental shrink
The chat-UI traverses the SAME graph as a full agent (Claude Code w/ Bash+Grep over 8,700 files),
but through a far smaller aperture: **3 in-memory JSON blobs** (no filesystem at the edge), **5
pure-function tools** (of `graph-query.py`'s ~11 modes), a **6-iteration loop bound**, and **no
content search**. That shrink is TWO different things with opposite verdicts:
- **Essential (keep — permanent):** no-filesystem edge runtime, bounded spend on a public URL,
  predictable latency, quote-only grounding + cite-gate. Can't ship a public LLM-over-graph
  without these.
- **Incidental (fix — just unfinished):** 5-of-11 modes ported, no content search, the slim
  node projection dropping Narrative Arc (G9), alias holes (G2). **None required by the runtime**
  — a content index is *build-time* (sidesteps the request CPU budget), `--container` is a cheap
  in-memory filter. Every roadmap gap lives here.

Framing: the keyhole has a **permanent frame** (essential) and **boards over the rest**
(incidental). The gaps ARE the boards.

### Who will actually use this (design targets)
The graph was built on one implicit user: *"asks about a named thing/event → we traverse."*
Real usage is wider:

| Archetype | Wants | Served today? |
|---|---|---|
| **Traversal** — "why did X happen", "who is Y" | node lookup + chain/neighbors | ✅ yes |
| **Quote-hunter mega-fan** — "best lines about X" | ranked quotes by content | ❌ no |
| **Thematic / non-event** — "how is hospitality shown", "describe the feasts" | aggregate across many nodes | ❌ no |
| **Researcher / evidence-seeker** — "I claim X, find the passages that back it" | claim → supporting quotes | ❌ no |

Three of four archetypes need **content-first retrieval**, which the graph has zero
surface for. That's a missing *paradigm*, not a missing tool.

---

## 1. Grounded census (what's actually there) **[grounded 2026-07-04]**

**21 node types** in `graph/nodes/` — the graph is NOT "characters + events":

| type | count | | type | count | | type | count |
|---|---|---|---|---|---|---|---|
| characters | 3916 | | locations | 1098 | | houses | 556 |
| titles | 542 | | events | 744 | | artifacts | 295 |
| _conflicts | 254 | | factions | 191 | | species | 188 |
| texts | 161 | | **foods** | **113** | | religions | 63 |
| materials | 58 | | concepts | 57 | | theories | 45 |
| customs | 37 | | medical | 35 | | languages | 26 |
| prophecies | 4 | | chapters | 344 | | _unclassified | 0 |

**Chat-UI bundle** (`web/data/`, built 2026-07-04):
- 8,473 nodes shipped, 23,099 edges, 12,139 alias phrases.
- Quote layer: **1,595 / 8,473 nodes carry quotes (~19%); 6,053 quotes total.**
- Shipped node shape: `{ name, type, identity, quotes }`. Descriptive content DOES ride along.
- Foods: **110 / 113 shipped** (3 dropped — reason unknown, see G7).

**Chat retrieval tools** (`web/netlify/edge-functions/lib/agent.ts`): exactly 5 —
`resolve`, `read_node`, `walk_chain`, `neighbors`, `family_tree`. **No content/quote search.**
`walk_chain` and `family_tree` both carry `MANDATORY` blocks; nothing steers descriptive Qs.

**Traversal scripts:** `scripts/graph-query.py` (main), plus `graph-conflict-pairs.py`,
`graph-cleanup-*.py` — all mixed into the general `scripts/` bin with one-off tooling.

### 1b. What "resolve" actually is **[grounded]**
`resolve(phrase)` is **name resolution — like DNS**. It turns a human phrase ("lemon cakes",
"death of Tywin") into the graph's internal node ID (**slug**). It does NOT walk the graph
and does NOT answer anything — it's just the front-door lookup that finds *which node* you
mean. Its lookup table is `alias-map.json` (12,139 phrase→slug entries). Only AFTER resolve
returns a slug do the real retrieval tools run (`read_node` / `walk_chain` / `neighbors` /
`family_tree`). This is why `lemon cake` opens the door but `lemon cakes` hits a wall — the
resolver's table has one phrasing and not the other. **Resolve is the single most important
tool and the quietest failure point**: when it misses, nothing downstream can recover, and
the model silently falls back to memory or grabs a nearby node.

### 1c. "Is the whole graph shipped?" — mostly, but slimmed **[grounded]**
Two different senses:
- **Node inventory:** yes — 8,473 of 8,727 files ship; the 254 missing are exactly the
  `_conflicts` staging bucket. The skeleton is complete.
- **Per-node content:** NO — each node ships as `{name, type, identity, quotes}` only. The
  `## Narrative Arc` and `## Edges` prose sections are dropped (edges ride separately). See
  **G9** — real cited descriptive content is stranded out of the bundle.

### 1d. The traversal machinery — edge grammar + query modes **[grounded from worklogs S82–S167]**
The graph isn't a bag of nodes; it has a designed **traversal grammar** built during the
enrichment era. Worth stating because it's the actual asset the query layer sits on.

**Edge grammar (how you move through the graph):**
- **Causal chain:** `CAUSES` / `TRIGGERS` / `MOTIVATES` — the story-time spine. `ENABLES` is a
  *weaker-than-causal* precondition (walked separately, shown behind a toggle). This is the
  `--causal-chain` / `--full-chain` axis.
- **Event reification (S82–84, S105/106):** n-ary events are reified into **event-node hubs**;
  participants attach via **role edges** — `AGENT_IN` / `VICTIM_IN` / `COMMANDS_IN` /
  `FIGHTS_IN` / `WITNESS_IN` / `ATTENDS`. "Chain-as-arc, NO umbrella parents" — an arc is a
  CAUSES/TRIGGERS/MOTIVATES chain you *walk*, not a parent node. `SUB_BEAT_OF` nests fine
  detail under a hub (the `--expand-beats` axis).
- **Lineage:** `PARENT_OF` / `SPOUSE_OF` — the family_tree axis.
- **Containers (S121–122):** `containers:` is a frontmatter **array tag** (NOT a node) — 5
  settled: `essos` / `wo5k` / `north` / `aegon` / `bran`. Enables **bag-retrieval**: "give me
  everything in the Essos arc." This is a whole *thematic* traversal axis.

**Query-mode inventory — and the DIVERGENCE (the important find):** the traversal logic exists
**twice** — `scripts/graph-query.py` (Python, ~11 modes) and `web/src/lib/*` (TS, ported S172).
They have drifted apart, and **the chat exposes only ~5 of the Python modes**:

| mode | graph-query.py | chat-UI | note |
|---|---|---|---|
| resolve / read-node / neighbors | ✅ | ✅ | |
| `--causal-chain` (+`--full-chain`/enables) | ✅ | ✅ `walk_chain` | |
| **`--container`** (bag-retrieval by theme) | ✅ | ❌ | **partially solves G4/D4 — never ported** |
| **`--expand-beats`** (SUB_BEAT_OF + roles) | ✅ | ❌ | fine-detail expansion |
| **`--path`** (how are A & B connected) | ✅ | ❌ | "connection between two nodes" |
| **`--event-participants`** | ✅ | ❌ | who was involved in an event |
| family_tree | ❌ | ✅ | built fresh in TS (S178) — Python lacks it |

**Implication:** part of the "graph feels event-only" problem is that **the richest traversal
modes were never exposed to the chat.** `--container` alone would let "describe the meals of
the Essos arc" retrieve a *bag* instead of coercing to one event. Porting the divergent modes
(and unifying the two impls per §4) is lower-effort than net-new capability — the logic exists.

---

## 2. Gaps identified so far

- **G1 — No content-first retrieval.** 6,053 quotes, no way to search them by content.
  Blocks quote-hunter, thematic, and researcher archetypes entirely. *(highest leverage)*
- **G2 — Silent resolve failures from alias holes.** Node exists + is rich, but natural
  phrasing doesn't open it. **Proof:** `lemon cake` resolves; `lemon cakes` (plural, the
  universal usage) → nothing. Likely a large invisible failure class (plurals, natural
  variants, epithets). When resolve misses, the model falls back to memory or grabs a
  nearby event — exactly the symptom that started this.
- **G3 — `walk_chain` over-fires.** `MANDATORY/MUST` framing bleeds into non-causal Qs.
- **G4 — No thematic/cross-cutting aggregation.** "Describe the meals" spans dozens of
  food nodes; nothing gathers across a type or theme.
- **G5 — Enrichment imbalance (suspected).** Events + causal wiring deeply enriched;
  descriptive layers likely thin. NEEDS a quote-density-per-type census to confirm.
- **G6 — No browse/enumerate surface.** `resolve` is the only door; you can't list "all
  foods" or "all customs" to discover what's queryable.
- **G7 — What the bundle drops.** RESOLVED: the bundle ships 8,473 of 8,727 node files;
  the missing 254 are *exactly* the `_conflicts` staging bucket (correctly excluded). So
  the node *inventory* is essentially complete. NOT a gap. (Earlier "3 foods dropped" was
  a miscount.)
- **G8 — Quote layer is concentrated (~19% of nodes).** Uneven substrate for quote-hunting.
- **G9 — The bundle ships a SLIM projection of each node, not the whole node.** Each shipped
  node = `{ name, type, identity, quotes }` only. The node markdown's **`## Narrative Arc`**
  and **`## Edges`** sections are DROPPED from node prose (edges ship separately in
  `edges.json`). This matters: much descriptive/cited content lives in Narrative Arc bullets
  — e.g. `acorn-paste`'s Narrative Arc line about the full "starvation register" (bugs,
  worms, frog, blackberries, cited) does NOT ship; only the identity blurb + the one deduped
  Quote do. So the chat literally cannot see content the graph holds. Audit how much cited
  descriptive text is stranded in Narrative Arc sections.
- **G10 — The fuzzy resolve fallback is structurally event-biased.** When exact alias lookup
  misses, `resolve` falls back to token-overlap (`resolve.ts` `fuzzyCandidates`, score ≥ 0.5)
  plus a per-slug-token bonus. Event nodes have long multi-word slugs/aliases
  (`assassination-of-tywin-lannister`, `tourney-at-harrenhal`) → far more token surface for a
  vague query to overlap → they outscore terse nodes (`beef`, `hodor`). **The UI's visible
  tell is a resolve receipt reading `<slug> · events (fuzzy)`** — that literally means "your
  phrase wasn't in the alias table, so I guessed, and the guess leaned event." This is a
  SECOND, independent driver of the event-bias, on top of G3 (`walk_chain` MANDATORY framing).
  Fixing G2 (alias coverage) shrinks how often fuzzy fires at all; re-weighting fuzzy by node
  prominence/type could de-bias what it returns when it does fire.

---

## 3. Directions (spitball — not decided) **[spitball]**

- **D1 — Quote/passage search tool.** Search the 6,053 shipped quotes by keyword/theme
  (later: embeddings). New chat tool e.g. `search_quotes(query)`. Directly unlocks G1 +
  three archetypes. Reads the same bundle the UI already ships. *(headline candidate)*
- **D2 — Alias-coverage audit + backfill.** Deterministic first: pluralization, natural
  phrasing, epithets → feed `resolve`. Cheap, high-impact on G2.
- **D3 — Scope `walk_chain` tighter** + add explicit tool-selection guidance for
  descriptive/thematic questions in the system prompt. Cheap, addresses G3.
- **D4 — Thematic aggregation / `list_by_type` / tag-gather** tool for G4/G6.
- **D5 — Quote-density census per type** (Python) → target enrichment where thin (G5/G8).
- **D6 — A cross-type "collection"/tag layer** so themes (food, hospitality, dress) cut
  across node types (a "meal" pulls foods + customs + location + character quotes).
- **D7 — Build the charter'd "braid" primitives (already designed, never built).** S117 wrote a
  charter (`graph/convergence-maps/README.md`) for `--braid` / `--fork-hubs` / `--join-hubs` —
  finding where causal chains diverge (shared start), converge (shared end), and offset (shared
  middle). `graph/convergence-maps/` holds only the README; 0 modes exist. Gated on "denser
  causal layer" — that gate is now PASSED. This is a designed traversal capability sitting on the
  shelf; it makes the "chain walked" showpiece far richer (the hairnet as a divergence hub).
- **D8 — Ship the trigger table (the unshipped index half).** Principle #5 = "the index routes,
  the graph traverses." The routing/trigger schema was never built. A content/quote search index
  (D1) is really this same missing routing layer — build them together.

---

## 4. Script organization — the traversal layer as part of the graph **[spitball / interview]**

**Problem:** the "how you query the graph" logic is scattered and reads as scratch —
`scripts/graph-query.py` next to cleanup one-offs, plus a *second*, separate implementation
of the same traversal ideas inside the chat-UI (`agent.ts` tools). Two implementations of
one conceptual query surface, neither presented as a deliverable.

**Idea:** promote graph traversal/query into a **first-class, co-located, documented layer**
— so the graph ships *with* its query interface, the way a database ships with its access
API. Candidate homes (undecided): `graph/query/`, a top-level `query/`, or a small packaged
Python module. Portfolio-legible framing: *"here is the knowledge graph, and here is the
documented interface for traversing it — the same surface the chat-UI speaks."*

**Sub-ideas to chew on:**
- One documented query API (the "shapes" — resolve, read, walk, neighbors, family,
  search, aggregate) with the Python CLI and the chat-UI tools both as thin adapters over it.
- The query layer becomes the demo-able artifact in the interview: not just "I built a
  graph," but "I built a queryable graph and here's the retrieval surface."

---

## 5. Adjacent must-finish (do NOT conflate with the above)

- **Chronology composite keys (S185).** Finish wiring `sort_keys` into the bundle + date
  backfill. This is a *traversal-ordering* fix, not a *query-mode* fix. Separate track.

---

## 6. Process guardrails for whatever we build

- **Audit = read-only report + gated fix queue.** An "audit that fixes as it goes"
  collides with the standing rule *no graph mutation without go-ahead* (S184: 744 nodes
  stamped straight from a dry-run). Keep survey and apply separate; make the queue
  trivially approvable, don't let it write.
- **Census before reasoning-model.** The deterministic half (counts, coverage, alias
  holes) is Python. Only spend a reasoning model (Fable/Opus) on the design half. Per the
  backfill-ladder rule: deterministic → Haiku → Fable-only-for-genuine-reasoning.

---

## 8. Prior art — already built or deferred (don't reinvent) **[grounded from worklogs]**

Mining the worklogs (S172–S183) shows several of these threads are **already scoped** — some
built, some explicitly parked. This changes "invent" into "un-defer / finish."

- **Content search is a KNOWN deferred fast-follow, not a new idea.** S172 built the
  retrieval core but **DEFERRED `searchChapters` / `readPassage`** with a specific reason:
  *"need a build-time inverted index to stay under the Edge 50 ms CPU budget; the curated MVP
  grounds on graph quotes only."* → **This IS D1.** The design intent already exists; the
  blocker is a build-time inverted index (over chapter text and/or the 6,053 node quotes).
  All 347 chapter files are on disk (`sources/chapters/`), so the substrate is there.
- **The resolver already had two passes (S179):** prominence ranking (`degree + 4·quoteCount`
  tie-break, so an empty stub can't outrank a rich node) + epithet-alias backfill
  (`scripts/backfill-epithet-aliases.py`, "The …" wiki-redirects → 12,029→12,140 phrases).
  So G2/G10 fixes *extend* existing tooling, they don't start from zero.
- **"Fuzzy-resolve on marquee names" is ALREADY a named parked track** (S177/S183 STATUS:
  "Deferred: fuzzy-resolve resolver track"). Symptom logged there: "Aegon the Conqueror" /
  "Targaryen dynasty" fuzzy-match to the wrong Aegon instead of an exact hit — pure alias-map
  gaps. Our G2 + G10 ARE that track; this doc gives it the fuller diagnosis.
- **Two implementations of one traversal surface, confirmed:** `scripts/graph-query.py` +
  `scripts/event_alias_resolver.py` (Python CLI) were *ported* to `web/src/lib/*` (Deno/TS)
  in S172. §4's "unify into one documented query API" is exactly the drift this creates.
- **Live track this connects to:** "feed in Matt's alpha-tester notes"
  (`progress/continue-prompts/2026-07-01-chat-ui-alpha-tester-notes.md`). The event-bias you
  noticed is itself an alpha-tester observation — it belongs to that track.
- **Relevant standing principle (worklog #5):** *"The index routes. The graph traverses.
  Both are needed."* A content/quote search tool is really a second **index** (route by
  content, not by name) — it fits the existing mental model, doesn't fight it.

**Net:** the roadmap is less "build new paradigm from scratch" and more **"un-defer the
inverted-index search (D1) + finish the parked fuzzy-resolve track (G2/G10) + de-bias the
fallback + tune walk_chain (G3)."** Most of it is already named; little is truly greenfield.

---

## 7. Open questions for Matt

1. Where should the traversal layer live — `graph/query/`, top-level `query/`, or a
   packaged module? (determines the "part of the graph" framing)
2. Is `search_quotes` (content-first) the headline new capability to build first?
3. Interview framing — is the pitch "graph + documented queryable interface"? That raises
   the bar on the query layer being demo-able and documented, not just functional.

---

## Appendix — session log for this doc
- **2026-07-04 (this session):** created. Grounded census done; corrected the "food has
  nowhere to land" misread (food IS a node type, 110 shipped). Found the `lemon cakes`
  plural resolve failure. Gaps G1–G9 + directions D1–D6 logged. Clarified what `resolve` is
  (DNS-style name→slug lookup, §1b). Established the bundle ships ~all nodes minus
  `_conflicts`, but each node is SLIMMED to identity+quotes — Narrative Arc prose stranded
  (§1c, G9). Fuzzy-fallback event-bias found + logged (G10). Read worklogs S172–S183 and
  added §8 prior-art: content-search (D1) is a KNOWN deferred fast-follow (S172, blocked on a
  build-time inverted index); resolver already had 2 passes (S179); "fuzzy-resolve marquee
  names" is an already-parked track (S177). Most of the roadmap is un-defer, not greenfield.
- **2026-07-04 (cont.):** read deeper worklogs (S82–S167 enrichment/narrative-arc era). Added
  §1d — the traversal machinery (edge grammar: causal chain + role edges + reification +
  containers) AND the **query-mode divergence** (Python `graph-query.py` has ~11 modes; chat
  exposes ~5 — `--container`/`--expand-beats`/`--path`/`--event-participants` never ported;
  `--container` alone partially solves G4). Split out the current-state material into a new
  companion doc **`GRAPH-STATE.md`**. Spitball ongoing.
- **2026-07-04 (cont.):** added D7 (charter'd-but-unbuilt "braid"/convergence primitives) + D8
  (unshipped trigger table) from the backlog sweep. Then REPRODUCED the failure live on the
  deployed UI (§0 "LIVE EVIDENCE"): the meals question fired ~13 fuzzy/no-match resolves →
  loop-bound-hit, no answer — every gap firing at once. Added the **"two apertures / essential
  vs. incidental shrink"** framing (§0): which gaps are fixable (incidental) vs. permanent
  runtime constraints (essential).
- **2026-07-04 (S189, master-design session):** this doc's forward-looking half is superseded
  by **`working/query-layer/design.md`** (see banner). S189 verifications recorded there:
  victim-phrase aliases ("Robb Stark's death") are ABSENT from the shipped `alias-map.json`
  (the §4b suspicion is a confirmed portability gap); the `graph/index/` layer (48 MB) is read
  by nothing in the query path and is stale for harvest-minted nodes; the deeper root cause
  behind the mode divergence is the absence of any shared contract/parity mechanism (new G11).
