# The Query Layer — Master Design (S189)

> **Status: TRACK COMPLETE — S191 (2026-07-04).** Every step landed: S190 shipped
> steps 0/1/3/4/5/6/7/8a–c/9 + all 5 advisory boards (§8); **S191 (the Fable-orchestrated
> finale) landed step 2** — the mini-graph fixture (`graph/query/tests/fixtures/mini/`,
> the board-designed "Salt Debt" saga, Matt-approved) + the traversal suite
> (`graph/query/tests/`, 116 tests) + pytest.ini + the two D-G Matt checkpoints
> (fixture content, op-semantics table `working/query-layer/boards/op-semantics-s191.md`)
> + **shim retirement Tier B** (the 89 shim-loaded tests migrated to package imports;
> `scripts/graph-query.py` / `event_alias_resolver.py` / `build-chat-export.py` DELETED;
> netlify.toml build command repointed to the `graph/query/build/` builders) + the
> drift-alarm re-proof (one golden case deliberately broken → ALL THREE runners fail —
> and the re-proof caught + fixed a run_cases hole where resolve `candidates[0].slug`
> was never compared). Suites at close: pytest 1445 (1 env-fail cwd-is-tmp, 1 skip),
> run_cases 37/0/1, deno 99/0/1. Still Matt-gated (riders, not Track work): 8d SERVED_AT
> pass, hygiene class-5 dup-slugs (his worktree session), prod deploy of the new chat build.
> Execution record: worklog S190+S191 + the appendix entries at the foot of this doc.
> Originally produced Session 189 (2026-07-04, Matt-mandated
> master-design session). This document is the execution plan for the **query-layer track**:
> it supersedes the *directions* half (§3/§4) of `GRAPH-QUERY-ROADMAP.md` as the plan of
> record — the roadmap remains the diagnosis/history record. Grounded in four fresh code/data
> surveys run this session (Python CLI, TS/chat surface, scripts+tests inventory, graph census)
> plus direct spot-checks; every claim marked **[verified S189]** was checked against the live
> repo this session, not inherited from S188.
>
> **How to use this doc:** §5 is a sequence of step cards a mechanical agent can execute
> one-per-session. §3 is the decision record — each major fork lists the options weighed so
> Matt can overrule at the fork, not just at the end. §2 is the grounded evidence. Read §0–§1
> for the shape; skip to §5 to work.
>
> **Vocabulary:** this is a **Track** (the query-layer track) made of lowercase **steps**.
> **Tier** = confidence 1–5 only. Paste these terms into any subagent prompt (subagents don't
> load CLAUDE.md).
>
> **AMENDED same session (S189b — Matt's review):** (1) home is **`graph/query/`** (D-A
> overruled); (2) the **pytest traversal suite is DEFERRED TO LAST** — built over the finished
> layer, nothing half-finished left behind (D-G amended; automated drift protection does NOT
> wait — the golden spec cases ship inside the build sessions as verification artifacts);
> (3) **project-first, not interview-first** — docs/tests serve the project; portfolio value
> falls out, it is not a design driver; (4) execution model = **Fable-orchestrated sessions**
> fanning out Sonnet/Haiku subagents (see §5 "Execution model"), and the remaining §8 forks go
> to an **advisory-board fan-out**, Matt overrules on read.

---

## 0. TL;DR

**The reframe (where this doc departs from S188):** the project doesn't have *a query layer
with gaps* — it has **four accidental query surfaces** that grew independently and share no
contract:

1. `scripts/graph-query.py` (~9 CLI modes, reads the live graph),
2. `scripts/event_alias_resolver.py` (resolution + its own derived lookup tables, its own
   YAML parser, its own normalizer),
3. `graph/index/` — **48 MB of built entity/chapter indexes that nothing in the query path
   reads** (built S38–S72, never wired in),
4. `web/src/lib/*` (the TS port: 5 of the modes + one mode Python lacks, over a slimmed
   bundle, behind 5 chat tools).

Every S188 gap (G1–G10) is a symptom of that structure. Fixing them one-by-one inside it
just mints a fifth drift surface. So the plan is **contract-first**: define one documented
query surface (named operations + semantics + shared golden test cases), consolidate the
Python side into one package under `graph/query/` (Matt, S189b), make the CLI and the chat
tools thin adapters over that contract — *then* land the new capabilities (content search, resolver
hardening, mode ports, descriptive routing) inside it, each gated by an eval harness that
measures whether retrieval actually got better.

**First move:** orchestrated **session A** (steps 0+1+7: scaffold `graph/query/`, zero
behavior change, braid primitives) — see §5 "Execution model".

**What this builds toward:** the graph ships with one documented query surface — one
contract, thin adapters (CLI, chat, optionally MCP), cross-language parity tests, and
telemetry-driven retrieval evals. The project needs this to answer its own questions; any
external legibility falls out for free.

---

## 1. Destination — the end-state this Track builds

When the Track is done:

- **One contract.** `graph/query/README.md` + `graph/query/spec/operations.md` name every operation
  (resolve, read, neighbors, chain, path, participants, container, family, search, list,
  mentions, theme, braid, health), its inputs/outputs, and its **two profiles**:
  - **full profile** (CLI / in-repo agents): live graph on disk, unbounded walks, all ops;
  - **bounded profile** (public chat): slim bundle, documented caps (depth 2, 12
    links/direction, 6 tool iterations), a subset of ops.
  Divergence between implementations becomes *documented profile difference* or *test
  failure* — never silent drift.
- **One Python engine.** `graph/query/weirwood_query/` — single loader, single frontmatter
  parser, single normalizer; `graph-query.py` and the resolver's lookup logic absorbed; the
  CLI (`weirwood query …`) is a thin shell over it. Traversal code lives apart from the build/
  pipeline bin (`scripts/` keeps ingest/build/mutation tooling).
- **Cross-language parity by fixtures.** `graph/query/spec/cases/*.json` golden cases (input →
  expected output) run by BOTH pytest and `deno test`. The TS port can't drift silently again.
- **A traversal pytest suite Matt co-designed** — **built LAST, over the finished layer**
  (S189b: deferred until everything else in this Track is done; the golden cases above are
  produced during the build sessions and carry the drift protection in the meantime). Sits
  alongside the existing 26-file `tests/` suite, which stays where it is.
- **Content-first retrieval.** A build-time inverted index over the 6,053 node quotes +
  identity blurbs; `search` as a CLI mode and a `search_quotes` chat tool; the chat's system
  prompt routes descriptive/thematic questions to it. The S188 live failure ("describe some
  detailed meals" → 13 fuzzy/no-match resolves → loop-bound, no answer) becomes a
  one-tool-call answer.
- **A hardened resolver** with deterministic variant expansion (plurals, possessives,
  victim phrases — which currently never reach the bundle **[verified S189]**), a de-biased
  fuzzy fallback, and a **telemetry loop**: the live per-turn logs (shipped S186) are mined
  for resolve misses, which feed the alias table. Real users repair the resolver.
- **An eval harness** — a fixed retrieval question set with scored runs before/after every
  step. "Better" is a number, not a vibe.
- **The descriptive layer reachable** — via search + list/theme routing immediately (no graph
  mutation), and via a small deterministic wiring/index-repair pass (gated) after.
- Braid/convergence primitives built in the engine (the S117 charter, un-deferred).
- Optional adapters: an MCP server; the site's "how it works" page fed by the same spec.

Explicitly NOT in the destination (see §7): embeddings, spoiler gating, theories layer,
TWOIAF ingestion, F&B, a graph database, prophecy minting, granular dips.

---

## 2. Grounded findings (what the S189 surveys established)

### 2a. The four surfaces, precisely

**`scripts/graph-query.py`** — modes: positional `<slug>` node report (reads the **legacy
`## Edges` markdown**, not edges.jsonl — the only mode that does), `--neighbors`, `--path`
(2-hop bridges, cap 50), `--health`, `--event-participants` (hub → SUB_BEAT_OF children →
role edges), `--causal-chain` (CAUSES/TRIGGERS/MOTIVATES, unbounded BFS), `--full-chain`
(+ENABLES, labeled "(precondition)"), `--expand-beats` modifier, `--container` (frontmatter
bag-retrieval; the only mode that never loads edges). All modes O(E)-rescan per invocation;
full load ≈ 0.5 s — plenty fast, no caching needed at this scale. **No tier filtering
anywhere** (tier is passed through, never filtered). No general N-hop mode.

**`scripts/event_alias_resolver.py`** — 5 alias sources (wiki redirects, event frontmatter,
all-node frontmatter, victim-phrase templates, "The_*" redirect pages), priority-ordered
collision handling, 3-tier resolve (exact → ambiguous → character → fuzzy ≥ 0.5 token
overlap + slug bonus). Its own regex frontmatter parser (graph-query has a different,
pyyaml-based one). Known code-visible weaknesses: no plural/possessive normalization, no
candidate-length penalty (short queries score 1.0 against long phrases — **this is G10's
mechanism**), victim phrases require a death keyword in the event's own slug/name and a
≥4-char victim token.

**`graph/index/`** — 8,155 files, 48 MB: per-entity indexes (chapters mentioning it,
appearance counts, edge counts) for all 21 categories + per-chapter mention indexes +
per-directory `_summary.json` (top-by-appearances, top-by-in-edges). **Read by nothing in
the query path.** And partially stale: harvest-minted food nodes have empty indexes
(`acorn-paste`: 0 appearances, 0 chapters **[verified S189]**) because the mention-resolution
predates those nodes' aliases.

**`web/src/lib/` + `agent.ts`** — 5 tools (resolve, read_node, walk_chain, neighbors,
family_tree). `walkChain`: depth 2, ≤12 links/direction, ENABLES as a separate side-channel
(≤24), story-time sort (the S185 fix — **the render-order bug is fixed in lib**). `familyTree`
is TS-only (Python has no genealogy mode). Bundle = 8.7 MB inlined JSON (nodes slimmed to
`{name,type,identity,quotes,composite?,reading_order?}`; **containers and per-node aliases do
not ship**; `## Narrative Arc` prose dropped). `MAX_TOOL_ITERATIONS = 6`. `search_chapters`/
`read_passage` explicitly deferred at S172 pending "a build-time inverted index" (their words
— the design intent for step 5 already exists). 41 deno tests run against the real bundle.

### 2b. Verdicts on the S188 gap list (G1–G10)

| gap | verdict | note |
|---|---|---|
| G1 no content search | **CONFIRM — the headline** | step 5; S172 already named the mechanism (build-time inverted index) |
| G2 alias holes | **CONFIRM + sharpen** | fix at *table-build time*, not query time; plus the telemetry loop (new). `lemon cakes` MISS re-verified against the live bundle **[verified S189]** |
| G3 walk_chain over-fires | **CONFIRM** | cheap prompt fix, but fold into a full routing-table rewrite (step 5c), not a one-word patch |
| G4 no thematic aggregation | **REFRAME** | don't tag descriptive nodes into the settled 5 containers; serve it with search + `list` + a build-time theme index (step 8a). Container tags stay event-only |
| G5 enrichment imbalance | **CONFIRMED, then PARKED** | census done (S188 §2a); the *quote-enrichment* fix is a data track, not a query-layer step |
| G6 no browse surface | **CONFIRM** | trivial `list` op, step 5d |
| G7 bundle drops nodes | already RESOLVED (not a gap) | `_conflicts` only |
| G8 quote concentration | **PARK** | data track; the search index makes what exists reachable |
| G9 slim projection | **CONFIRM, decide by measurement** | step 6c: measure the Narrative-Arc size delta first, then inline vs. fetch-on-demand |
| G10 fuzzy event-bias | **CONFIRM + mechanism found** | asymmetric scoring (no candidate-length penalty). Deterministic fix, step 4c |

### 2c. New gaps S188 didn't see (the "find what's missing" mandate)

- **G11 — No contract or parity mechanism.** The root cause of the Python↔TS divergence is
  structural: nothing pins the implementations together. Porting modes without fixing this
  reproduces the drift. (This gap reorders the whole plan: contract first.)
- **G12 — Intra-Python triplication.** Three frontmatter parsers (graph-query pyyaml+fallback,
  resolver regex, build-chat-export's own), two normalizers, two slug functions, duplicated
  loaders. Unification isn't just Python↔TS; it's Python↔Python.
- **G13 — The built index layer is unrouted AND stale.** 48 MB of `graph/index/` answers
  "which chapters mention X" today — the query surface never exposes it, and its
  entity-resolution predates the harvest-minted descriptive nodes (empty food indexes
  **[verified S189]**). The "trigger table" (D8) isn't missing so much as *half-built and
  unplugged*.
- **G14 — No telemetry loop.** Per-turn usage logs exist (S186, Netlify Blobs) and record
  every resolve miss made by real users. Nothing mines them. This is the cheapest source of
  truth about what phrasings the resolver needs.
- **G15 — No eval harness.** No fixed question set, no score, no way to say a retrieval
  change helped. (S96's Mode-3 dip did this once, manually, and it drove the best fix of that
  era — institutionalize it.)
- **G16 — Two edge serializations, unreconciled.** The node-file `## Edges` markdown vs.
  `edges.jsonl`. graph-query's positional mode reads the former; everything else the latter;
  no cross-check exists. The engine should read edges.jsonl only and treat node `## Edges`
  as display prose (with a one-off consistency audit).
- **G17 — Doc drift on the query surface itself.** `web/src/lib/README.md` documents a
  `full?` option walkChain doesn't have; README test counts say 27, actual 41;
  `graph/edges/README.md` says 3,811 edges (live: 23,099). Violates the repo's own
  README=existence-truth convention.
- **G18 — Data hygiene traps for a strict engine [census S189]:** 5 YAML-broken node files
  (malformed doubled-quote aliases — invisible to every parser); 91 edges with dangling
  endpoints (67 distinct phantom slugs, mostly collective-noun Pass-1 references like
  `gold-cloaks`); 28 exact-duplicate edge rows; 6,923 nodes carrying empty `aliases: []`
  stubs (84% of "has aliases" is noise). Small, mechanical, and worth fixing *before* the
  engine bakes in tolerance for them.
- **G19 — The victim-phrase index never reached the chat.** "Robb Stark's death" resolves in
  the Python resolver but MISSES in `web/data/alias-map.json` **[verified S189]** — the S96
  fix's marquee case silently doesn't exist in the deployed product. (GRAPH-STATE §4b asked
  for exactly this verification; answer: it's a real portability gap.)

### 2d. Who the layer serves (sharpened)

The S188 archetype table (traversal / quote-hunter / thematic / researcher) holds. Two
missing design targets that change decisions:

- **The in-repo agent** — Claude Code sessions are historically the *heaviest* query users
  (every dip runs graph-query dozens of times: dedup checks, spine verification, container
  lookups). The full profile is for them; keep it unbounded and scriptable, don't let chat
  constraints leak into it.
- **The docs-first reader** — anyone (future session, collaborator, reviewer) who reads the
  layer's contract before running it. The contract/README/parity fixtures are first-class
  because the *project* depends on them staying true — not as presentation (S189b:
  project-first, not interview-first).

---

## 3. Design decisions (options weighed → call)

### D-A. Where the query layer lives — **DECIDED (Matt, S189b): `graph/query/`**
- *Option 1 — top-level `query/`*: my original pick (separation from the scripts bin, data
  stays data). **Overruled.**
- *Option 2 — `graph/query/`* ✅ **CHOSEN by Matt** — the graph ships with its query surface,
  co-located. One clarification to keep the rules clean: the **no-graph-mutation gate applies
  to the DATA dirs** (`graph/nodes/`, `graph/edges/`, `graph/index/`, `graph/convergence-maps/`
  outputs) — `graph/query/` is code and evolves under normal code review, not the mutation gate.
- *Option 3 — `scripts/query/` subdir*: rejected (keeps the layer inside the scratch-bin +
  inherits the import-coupling minefield).
- All paths in this doc read `graph/query/…` accordingly.

### D-B. How to unify Python and TS
- *Option 1 — one language everywhere*: rejected. Python can't run on Netlify Edge; Deno
  can't be the in-repo scripting default without churning every workflow. The two-runtime
  reality is permanent (it's the "essential shrink").
- *Option 2 — codegen TS from Python*: over-engineering for ~10 operations.
- *Option 3 — **two implementations, one contract*** ✅ **CHOSEN.** A spec doc naming ops +
  semantics + profile caps, and **shared golden cases** (`graph/query/spec/cases/*.json`) executed
  by both pytest and deno. Where profiles legitimately differ (depth caps), the case files
  encode the profile. Drift → red test.
- **Overrule point:** how strict the parity gate is (every op vs. just the shared ops).
  Recommend: every op that exists in both.

### D-C. Content search — substrate and mechanism
- *Substrate:* **quotes + identity blurbs first** ✅ (6,053 quotes / 1,595 nodes + 8,473
  identity paragraphs — this is the curated, citable layer; it's what the chat is allowed to
  quote anyway). Chapter full-text search becomes a **CLI-first** capability (local
  filesystem, no edge constraint) in the same step, with the edge-side `read_passage`
  designed but gated (see step 5e).
- *Mechanism:* **build-time inverted index + BM25-ish scoring at request** ✅. Deterministic,
  $0, tiny (est. 0.5–1.5 MB for the quote layer), fits the Edge 50 ms CPU budget because
  tokenize-query + posting-list lookup is microseconds at this corpus size. Exactly the
  mechanism S172 named when deferring.
- *Embeddings:* **parked.** Anthropic has no embeddings API; a second vendor (Voyage etc.)
  adds a key, a cost, and a build dependency for marginal gain on this corpus — keyword+alias
  matching covers the archetype queries. Revisit only if step 3 evals show semantic-miss
  failures keyword can't reach.
- **Overrule point:** substrate order (quotes-first vs chapters-first) and whether
  `read_passage` ships to the public chat at all.

### D-D. The chat aperture
Keep the **essential shrink** exactly as is (no-filesystem bundle, bounded iterations,
quote-only grounding, cite gate) — it's what makes a public LLM-over-graph shippable. Widen
only the **incidental shrink** (tools, index coverage, projection). Concretely: keep
`MAX_TOOL_ITERATIONS = 6`; with search + routing, the meals question needs ~2. Add one
resilience rule to the prompt: *after 2 consecutive failed resolves, switch to
`search_quotes`* — that alone kills the 13-resolve flail even on alias misses.

### D-E. The descriptive/orphan layer — what actually fixes it
The S188 diagnosis ("capture worked, wiring was never in scope") is right; the S188 *remedy
sketch* (edge grammar, e.g. `SERVED_AT`) is only third-best. Order of leverage:
1. **Retrieval-first, zero mutation** ✅ (step 5): search + `list`/`theme` ops make every
   orphan food/custom/material node *reachable by content today*. The quote layer is already
   51%-dense on foods — the content exists.
2. **Index repair, deterministic, cheap** ✅ (step 8b): re-run the mention-index resolution
   with the current alias table so harvest-minted nodes stop showing 0 appearances; expose
   `mentions` as an op. Plus the Matt-steered **Python food-keyword grep** (backlog, gate now
   passed) as a *pointer generator* feeding harvest — not an LLM sweep.
3. **Edge grammar, gated, last** (step 8d): a small vocabulary addition (`SERVED_AT`
   food→event is the strongest candidate; `PRACTICES` may already cover customs via target
   widening) routed through `reference/architecture.md` + a worklog Active Decision + Matt's
   explicit go, executed as a bounded Haiku pass over nodes that already carry located
   quotes. Genuinely valuable for traversal ("what was served at the Purple Wedding"), but
   it's the expensive third of the fix, not the first.
- **Overrule point:** whether 3 happens at all this Track, and the exact new-type list.

### D-F. The slim projection (G9)
Decide by measurement, not taste (step 6c measures the `## Narrative Arc` size delta):
- if the delta keeps the bundle comfortably under ~15 MB → **inline** the prose for nodes
  that have it (simplest; the bundle is already inlined JSON);
- else → **per-node static assets** fetched on demand: build emits `web/public/node/<slug>.json`,
  and `read_node`/`/api/node` fetch it at request time (network I/O doesn't count against the
  50 ms CPU budget; the same trick later serves `read_passage` from chapter files).
- **Overrule point:** the size threshold and whether the dossier endpoint should carry it
  even if the chat tool stays slim.

### D-G. The pytest suite — **AMENDED (Matt, S189b): DEFERRED TO LAST**

Matt: the suite is not the priority and must not become a half-finished state — build it
**after everything else in this Track is done**, over the finished layer, with him involved.
What does NOT wait: the **golden spec cases** (`graph/query/spec/cases/`) are produced inside
the build sessions as verification artifacts — they carry the Python↔TS drift protection from
day one. The existing `tests/` suite also keeps running against the shims throughout (the
no-regression net for the scaffold). Everything below describes the suite *as it will be
built at the end*:
Survey facts: 26 test files in `tests/`, pytest-as-runner over mostly unittest-style classes,
no conftest/pytest.ini/CI, no fixtures dir (inline dicts + tmp_path), one orphaned test
(`scripts/stage4-formalize-edges-test.py`) pytest never discovers, and a documented
convention of "pytest 1231 pass / 3 documented fails" as the health line.
- *Plan:* the **new** traversal suite lives at `graph/query/tests/`, idiomatic pytest
  (fixtures/parametrize), three layers:
  1. **synthetic mini-graph** (`graph/query/tests/fixtures/mini/`) — a hand-authored ~25-node,
     ~40-edge graph exercising every traversal shape: a causal diamond, an ENABLES segment
     break, SUB_BEAT_OF beats with role edges, a 4-generation family with a deep spine, a
     container bag, ambiguous aliases, a plural/possessive resolve case, quote-bearing
     descriptive orphans. Checked in, human-readable, *fun to design* — *this is the piece
     Matt co-authors.*
  2. **golden parity cases** (`graph/query/spec/cases/`) — run by pytest AND deno (D-B).
  3. **real-graph smoke** — `@pytest.mark.corpus` tests against the live graph (Tywin chain,
     Aegon family — mirroring the TS pivots), skipped when the graph isn't present.
- Plus repo-level housekeeping: add a minimal `pytest.ini` (testpaths `tests/ graph/query/tests/`,
  the `corpus` marker), move/rename the orphaned formalize-edges test, leave the legacy
  unittest style alone (churn for zero information).
- **Not delegated:** fixture content + op semantics sign-off are PAIR-WITH-MATT work.

### D-H. Scripts reorg — extraction, not upheaval
- *Option 1 — full `scripts/` re-taxonomy into subdirs*: rejected. The survey mapped ~20
  dynamic same-directory loads, 4 sibling imports, `tests/_helpers.py` hard-coding
  `SCRIPTS_DIR`, and `weirwood.zsh` path assumptions — a bulk move is high-blast-radius,
  low-yield archaeology of mostly-spent pipeline scripts.
- *Option 2 — **extract only the query layer; classify the rest in docs*** ✅ **CHOSEN.**
  Move/absorb the 3 query-surface files (graph-query, event_alias_resolver, build-chat-export)
  into `graph/query/` with compat shims at the old paths (the survey shows exactly one static
  importer to preserve: `backfill-epithet-aliases.py` imports `event_alias_resolver`).
  `scripts/README.md` gets the survey's 5-way classification (QUERY→ pointer to `graph/query/`,
  BUILD, MUTATION, INGEST, UTILITY) so the bin is *legible* without being churned.
- **Overrule point:** whether the archive-worthy one-offs (session-numbered `harvest_s152_*`,
  `aegon_*`, spent `LIVE?` flags) also get swept to `scripts/archive/` in the same pass
  (cheap, but touches history — Matt's call).

### D-I. Evals and telemetry as first-class steps
Not in any prior plan. Two cheap, standing mechanisms:
- **Eval harness** (step 3): a fixed ~20-question set (the 10 Mode-3 dip questions + the
  meals question + the S177 marquee-resolve failures + one question per archetype), a runner
  (offline stubbed-loop where possible, local `weirwood-live` for live runs — never the prod
  URL), and a scored report (resolved? grounded? answered? tool calls used? loop-bound?).
  Run at baseline and after every retrieval-touching step.
- **Telemetry miner** (step 4d): a read-only script over the Netlify Blobs per-turn logs
  extracting resolve misses/fuzzy-fallbacks with frequency → ranked alias-backfill queue.
  Closes the loop with real usage.

---

## 4. Target architecture

```
graph/query/
├── README.md                  # THE documented query surface (the layer's own docs)
├── weirwood_query/            # the Python reference engine (importable package)
│   ├── __init__.py
│   ├── model.py               # Node / Edge dataclasses; the ~9-field canonical edge set
│   ├── load.py                # ONE loader: nodes+frontmatter, edges.jsonl, alias table, index
│   ├── normalize.py           # ONE normalizer/tokenizer (parity with web/src/lib/normalize.ts)
│   ├── resolve.py             # exact → ambiguous → character → fuzzy (de-biased)
│   ├── traverse.py            # neighbors, causal/full chain, expand-beats, path,
│   │                          #   event-participants, container, family (NEW in Python)
│   ├── search.py              # inverted-index search over quotes/identity (step 5)
│   ├── themes.py              # list, mentions (graph/index), theme index (step 8)
│   ├── braid.py               # fork-hubs, join-hubs, braid (step 7)
│   ├── report.py              # health, reachability census, --explain support
│   └── cli.py                 # `weirwood query …` (argparse; every op a subcommand)
├── build/                     # builders for QUERY-SERVING artifacts only
│   ├── build_alias_table.py   # absorbs event_alias_resolver --build + variant expansion
│   ├── build_search_index.py  # step 5
│   ├── build_theme_index.py   # step 8a
│   └── build_chat_bundle.py   # absorbs scripts/build-chat-export.py (projection = contract)
├── spec/
│   ├── operations.md          # op semantics + the two profiles + caps
│   └── cases/*.json           # golden cases, run by pytest AND deno test
└── tests/                     # the Matt-paired traversal suite (D-G)
    ├── fixtures/mini/         # the synthetic mini-graph
    ├── test_resolve.py  test_traverse.py  test_search.py  test_spec_cases.py
    └── test_corpus_smoke.py   # @pytest.mark.corpus
```

Graph-*building* stays in `scripts/` (mint/finalize/backfill/pass2/stage4 families untouched).
`web/src/lib/` stays the TS adapter; it gains `spec_cases_test.ts` (runs `graph/query/spec/cases/`)
and, in later steps, `search.ts` + the new tool defs in `agent.ts`. `weirwood.zsh` gains
`weirwood query` and `weirwood refresh` grows the new builders (per the standing
rebuild-derived-artifacts rule).

### The operation table (spec preview)

| op | Python today | TS/chat today | end-state |
|---|---|---|---|
| `resolve` | ✅ (resolver) | ✅ | both; hardened table (step 4) |
| `read` | ✅ (positional mode) | ✅ slim | both; projection decision step 6c |
| `neighbors` | ✅ | ✅ | both |
| `chain` (causal) | ✅ unbounded | ✅ capped+sorted | both; Python gains the story-time sort |
| `chain --full` (ENABLES) | ✅ | ◐ (side-channel) | both (profile-documented difference OK) |
| `expand-beats` | ✅ | ❌ | both (step 6) |
| `path` | ✅ 2-hop | ❌ | both (step 6) |
| `participants` | ✅ | ❌ | both (step 6) |
| `container` | ✅ | ❌ (containers not in bundle) | both (step 6a) |
| `family` | ❌ | ✅ | both — port TS→Python (step 1, parity target) |
| `health` / `census` | ✅ / ❌ | ❌ | Python only (full profile) |
| `search` (quotes+identity) | ❌ | ❌ | both (step 5) — the headline |
| `list` (by type/filter) | ❌ | ❌ | both (step 5d) |
| `corpus-search` / `passage` | ❌ | ❌ deferred S172 | Python step 5e; chat gated |
| `mentions` (chapter index) | ❌ (index unread) | ❌ | Python step 8b; chat optional |
| `theme` | ❌ | ❌ | both (step 8a) |
| `braid` / `fork-hubs` / `join-hubs` | ❌ (charter only) | ❌ | Python only (step 7) |

---

## 5. Execution plan — step cards

> Conventions for every step: **Sonnet 4.6 unless stated** (mechanical work; the
> cheapest-viable rule). **DO-NOTs (global, apply to all steps):** no `graph/` mutation
> without Matt's explicit go (a green dry-run is not permission); `sources/` is read-only;
> never fetch the wiki; no LLM bulk pass without Matt's OK; web deploys are MANUAL per
> `DEPLOY.md` (git push ships nothing); keep the locked edge vocabulary — any new type
> routes through `reference/architecture.md` + a worklog Active Decision; one live continue
> prompt at a time; paste the Pass/Track/Tier/step glossary into every subagent prompt.
> After any step that changes node files or derived tables: run the relevant builders
> (`weirwood refresh` family) and `pytest` + `cd web && deno task test`.

### Execution model (S189b — Matt): Fable-orchestrated sessions, not nine serial ones

Matt's steer: **Fable is the orchestrator**, fanning out Sonnet/Haiku subagents for the
mechanical work; every session must land COMPLETE and verified — no half-finished states.
The step cards below stay the specs; they BUNDLE into three orchestrated sessions:

- **Session A — the engine.** steps 0 + 1 + 7. Fable holds the contract in-head and
  adjudicates; parallel Sonnet subagents split the package (loader/resolve/traverse/report/cli
  are separable modules); Haiku subagents run the mechanical verification (old-CLI vs new-CLI
  output diffs across EVERY mode on ~20 real slugs); an independent Sonnet fresh-verifier
  checks the familyTree TS→Python port against `web/src/lib/graph.ts` semantics. Braid (step 7)
  rides along only if the engine lands with room to spare — completeness beats scope.
- **Session B — retrieval.** steps 3 + 4 + 5. Eval baseline FIRST (the "before" numbers),
  then resolver hardening + search index + routing rewrite + loremaster researcher-frame
  persona reframe (5c, S189c) + `list`, eval re-run LAST.
  Fable owns the two judgment calls (fuzzy re-scoring, the routing decision table — the
  persona-adjacent prompt text still gets Matt's read before any deploy); Sonnet builds;
  Haiku generates/checks alias variants and greps; independent verifiers run the parity cases
  both runtimes. Exit: meals question ≤3 tool calls, zero causal-question regression.
- **Session C — reach + close-out.** steps 6 + 8a–c + side-step H + 9, PLUS the
  **advisory-board fan-out** on the remaining forks (below). Hygiene stays propose→Matt→apply.
- **Final session (deferred by Matt): the pytest traversal suite** (D-G) — built over the
  finished layer, with Matt. Nothing else in the Track waits on it.

**Advisory-board fan-out for the open forks (S189b):** instead of holding forks for
Matt-in-the-loop, fan out a cheap Sonnet board per fork (the S133 finding: a Sonnet board
converges ~90% with a max-effort Opus proposer — orchestration, not model tier, is the
bottleneck): read_passage to the public chat? SERVED_AT vocab proposal now or after 8a–c?
MCP adapter in or parked? shim retirement timing? Fable synthesizes board output into
decisions-with-rationale in this doc; Matt overrules on read.

### step 0 — pre-measurements (fold into session A; listed for completeness)
- **Goal:** three numbers later steps depend on.
- **Work:** (a) count nodes with a `## Narrative Arc` section + total bytes of those sections
  (grep/python over `graph/nodes/`) → feeds D-F; (b) size estimate of a quote inverted index
  (unique-token count over the 6,053 quotes + identities); (c) snapshot the reachability
  census (orphan-% per type — the S189 census script can be re-run) as the baseline metric.
- **Output:** `working/query-layer/measurements.md`. **Success:** three numbers with the
  commands that produced them. **Model:** Haiku or Sonnet. Read-only.

### step 1 — scaffold `graph/query/`: one engine, zero behavior change  ← **FIRST MOVE (session A)**
- **Goal:** the package + CLI exist; old entry points still work; nothing behaves differently.
- **Work:**
  1. Create the §4 tree. Implement `model.py`/`load.py`/`normalize.py` by *consolidating* the
     three existing parsers/normalizers (pyyaml-with-fallback wins; resolver's `normalize()`
     wins as the normalizer since the TS port mirrors it).
  2. Absorb `graph-query.py`'s modes into `traverse.py`/`report.py` + `cli.py`. Absorb the
     resolver's *resolution* half into `resolve.py`; its *table build* into
     `build/build_alias_table.py`. Move `build-chat-export.py` → `build/build_chat_bundle.py`.
  3. **Port `familyTree` TS→Python** (same caps as constants; the first parity op).
  4. Compat shims at old paths: `scripts/graph-query.py`, `scripts/event_alias_resolver.py`
     (must keep `from event_alias_resolver import normalize, name_to_normalized` working —
     `backfill-epithet-aliases.py` imports it), `scripts/build-chat-export.py` → thin
     re-exec/re-export wrappers printing a deprecation pointer.
  5. Update `weirwood.zsh` (`weirwood query`, keep `weirwood graph`/`resolve` aliased),
     `weirwood-refresh.sh` (call the new builders), `scripts/README.md` (QUERY section →
     pointer). Engine reads **edges.jsonl only**; the legacy `## Edges` markdown is display
     prose (G16) — the positional node report keeps printing it but labels it as node prose.
  6. Keep the existing `tests/test_graph_query_*` + `test_event_alias_resolver.py` green
     against the shims (they are the no-regression net for the move).
- **Success criteria:** `weirwood query chain assassination-of-tywin-lannister` ≡ old output;
  full pytest suite green; `deno task test` green (bundle rebuilt byte-identical or
  field-identical from `build_chat_bundle.py`); shims warn but work.
- **DO-NOTs:** no behavior changes (resist fixing G10 here); no graph writes; don't delete
  the old files until Matt approves the shim period ending.
- **Model:** Sonnet. **Size:** 1 session. **Parallel-safe:** no (everything depends on it).

### step 2 — the traversal pytest suite  **[DEFERRED TO LAST — Matt, S189b; PAIR WITH MATT]**
- **Runs as the FINAL session of the Track**, after steps 1–9 land — not before (no
  half-finished suite left behind). What does NOT wait: `spec/operations.md` v1 and the
  golden cases for resolve/neighbors/chain/family are produced inside sessions A/B as
  verification artifacts, plus `web/src/lib/spec_cases_test.ts` to run them — the drift
  alarm exists from session A onward.
- **Goal (when it runs):** D-G realized: mini-graph fixtures, corpus smoke marks, pytest.ini.
- **Work:** design the mini-graph WITH Matt (content, names, which traversal shapes);
  pytest.ini + `corpus` marker; relocate `scripts/stage4-formalize-edges-test.py` →
  `tests/test_stage4_formalize_edges.py`.
- **Success:** `pytest graph/query/tests` green; one golden case deliberately broken → both
  runners fail (drift alarm re-proven over the finished layer).
- **Model:** Sonnet, Matt driving fixture/semantics decisions. **Depends:** everything.

### step 3 — eval harness + baseline
- **Goal:** D-I's harness; the "before" numbers.
- **Work:** `working/query-layer/evals/questions.md` (~20 fixed questions: the 10 Mode-3 dip
  Qs from `working/session-results/2026-06-14-mode3-dip-results.md`, the meals question, the
  S177 marquee resolves — "Aegon the Conqueror", "Targaryen dynasty" —, "Robb Stark's death",
  "lemon cakes", one per archetype incl. a hospitality thematic and a researcher claim-check);
  a runner script (offline stubbed agent-loop reusing `agent_test.ts` infra where possible;
  live runs only against local `weirwood-live`, never prod; **no API spend without Matt's
  OK** — the stubbed loop needs none); scored report (resolve outcome, grounding, answered,
  tool calls, loop-bound). Run baseline; commit the report.
- **Success:** a table of 20 rows with today's (bad) numbers, reproducible by one command.
- **Model:** Sonnet. **Depends:** step 1. **Parallel-safe with step 2.**

### step 4 — resolver hardening (G2 / G10 / G19 / G14)
- **Goal:** the front door stops silently failing; the fuzzy fallback stops favoring events.
- **Work:**
  a. **Victim-phrase export fix (G19):** make `build_alias_table.py` merge victim phrases
     into the all-node table the bundle consumes; verify "robb stark's death" resolves in
     `web/data/alias-map.json` after rebuild.
  b. **Variant expansion at build:** plurals (s/es + a small irregulars list), possessives
     ("X's Y"), leading-article variants — generated into the table, so Python and TS get
     them for free with zero request-time cost. Collision-checked by the existing priority
     order; log every generated-variant collision to a review file rather than guessing.
  c. **Fuzzy de-bias (G10):** add candidate-length normalization (penalize |candidate|≫|query|)
     + keep prominence tie-break. Encode the "beef vs assassination-of-tywin" case as a
     golden test. Port the same scoring change to `resolve.ts` (parity case).
  d. **Telemetry miner (G14):** read-only script over the Blobs logs (via
     `web/scripts/read-logs.ts` conventions) → `working/query-layer/resolve-misses.md`
     ranked by frequency; its top rows feed (b)'s next iteration.
- **Success:** eval resolve-rows flip to HIT; alias-table diff reviewed (report, not
  auto-apply — the table is a derived artifact, rebuildable, so this is NOT graph mutation,
  but the diff still gets eyeballed); parity cases green both runtimes.
- **DO-NOTs:** no node-frontmatter alias writes in this step (that's graph mutation —
  variants live in the *derived table*); no prod deploy without Matt.
- **Model:** Sonnet. **Depends:** steps 1–3. **Serial with step 5** (both touch the table/
  bundle builders; run 4 before 5).

### step 5 — content search + routing (G1 / G3 / G4 / G6) — **the headline**
- **Goal:** the meals question answers in ≤3 tool calls with citations.
- **Work:**
  a. `build/build_search_index.py`: tokenized inverted index over all node quotes +
     identity blurbs (doc = quote or identity, carrying slug/type/cite); IDF precomputed;
     ships into the bundle (measure size; est. ≤1.5 MB).
  b. `search.py` + CLI (`weirwood query search "lemon cakes" --type foods`) and the TS twin
     `search.ts`; chat tool `search_quotes {query, type?}` returning ranked
     `{slug, type, text, cite}` (capped ~12).
  c. **System-prompt routing rewrite (G3):** replace the per-tool MANDATORY blocks with one
     decision table — who/what → resolve+read; why/consequence → walk_chain (MANDATORY only
     here); lineage → family_tree; describe/thematic/quotes → search_quotes; connection →
     path (when ported). Plus the resilience rule: 2 failed resolves → search_quotes.
     **Also (Matt, S189c): reframe the LOREMASTER_VOICE persona around its actual user — a
     researcher / thought-experimenter working on the series** ("you are assisting someone
     doing research and thought experiments on the books") rather than a bare encyclopedic
     register; hypothesis: the researcher frame licenses fuller, more exploratory answers.
     Constraint: the SHARED_RULES safety block (theory-scope guardrail, cite rules) is
     persona-independent by design — the reframe touches voice only, never those rules.
     Draft in the repo, **Matt reviews before deploy** (persona-adjacent); an A/B eval row
     (same questions, old vs new persona) rides the step-5 eval re-run.
  d. `list` op both runtimes (`list --type foods --has-quotes`), paged; chat tool optional
     (decide after evals — search may subsume browse for the chat).
  e. **Corpus search, CLI-only:** `weirwood query corpus-search "lamprey pie"` over
     `sources/chapters/` (grep-class + line cites). The edge-side `read_passage` (static-asset
     fetch of chapter files, network I/O outside the CPU budget) is DESIGNED here,
     **gated on Matt** for shipping.
- **Success:** eval re-run — meals/thematic/quote-hunter rows flip to answered; no regression
  on causal rows; bundle size within budget; parity cases green.
- **DO-NOTs:** no deploy without Matt; keep the cite-gate untouched (search results carry
  cites through the existing `[[q|…]]` machinery).
- **Model:** Sonnet (prompt-table wording: Matt sign-off). **Depends:** step 4 (table/bundle
  builders stable). **Size:** 1–2 sessions.

### step 6 — close the port gap + projection (the S188 mode-divergence list)
- **Goal:** the chat sees the graph's real shape; the bundle stops dropping load-bearing fields.
- **Work:**
  a. **containers → bundle** + `container` op in TS (+ optional chat tool or fold into
     `list {container}`) — the bag-retrieval axis, finally public.
  b. Port `path`, `participants`, `expand-beats` to TS; add chat tools only where evals show
     need (recommend: `path` yes — "how are X and Y connected" is a real archetype query;
     participants/beats can stay dossier-side).
  c. **G9 decision by step-0 measurement:** inline `narrative_arc` in the bundle if small,
     else per-node static assets consumed by `/api/node` + `read_node`. Either way the
     dossier shows cited Narrative-Arc prose.
- **Success:** parity table (§4) has no ❌ left except deliberate full-profile-only ops;
  evals re-run clean; bundle size documented.
- **Model:** Sonnet. **Depends:** step 5. **Parallel-safe with step 7.**

### step 7 — braid / convergence primitives (the S117 charter, un-deferred)
- **Goal:** `fork-hubs`, `join-hubs`, `braid A B [C…]` in the engine; first convergence maps.
- **Work:** pure DAG analysis over causal+ENABLES edges per the charter
  (`graph/convergence-maps/README.md`); outputs JSON+markdown per named braid into
  `graph/convergence-maps/` (files there are *derived analysis*, not node/edge data — but
  still get Matt's go before the first write, per the no-mutation posture); CLI only, no chat
  port; the hairnet divergence hub + the Oberyn fork as the two showcase maps.
- **Success:** `weirwood query fork-hubs --min-out 3` ranks the known hubs; the two maps
  render; unit tests on the mini-graph's causal diamond.
- **Model:** Sonnet. **Depends:** step 1 only. **Parallel-safe** with 4–6 (read-only).

### step 8 — descriptive-layer routing + repair (D-E realized)
- **Goal:** the orphan ring is reachable by every door that doesn't require new edges; the
  gated edge option is prepared, not presumed.
- **Work:**
  a. `build/build_theme_index.py`: deterministic theme→members table (seed themes: meals &
     feasts, hospitality, dress & materials, maesters & healing, songs & tales; membership by
     node type + keyword rules over names/identities/quotes); `theme` op both runtimes; this
     IS the trigger-table's routing half (D8), scoped to what's provably useful.
  b. **Mention-index repair (G13):** re-run `build-mention-index.py` resolution with the
     current alias table so harvest-era nodes light up; expose `mentions <slug>` reading
     `graph/index/`; add index freshness to `weirwood refresh --check`.
  c. **Food-grep seeder** (backlog item, Matt-steered, deterministic): keyword sweep over
     344 chapters → `chapter:line` candidate rows into the harvest queue. POINT, don't
     extract.
  d. **[GATED — design only until Matt's go]** descriptive edge grammar: propose `SERVED_AT`
     (food→event) + evaluate widening `PRACTICES` to `concept.custom`; route through
     architecture.md + Active Decision; then a bounded Haiku pass over quote-located food
     nodes, L1 gate, fresh-verify sample. **Needs: vocab decision + LLM-pass OK + mutation OK.**
- **Success:** "what do we know about meals in the north?" answerable via theme+search+mentions
  with zero new edges; food indexes non-empty; (d) remains a written proposal until greenlit.
- **Model:** Sonnet; (d) Haiku when/if approved. **Depends:** steps 1, 5.

### step 9 — adapters, docs, polish
- **Goal:** the layer presents as the deliverable it is.
- **Work:** doc-truth sweep (G17: lib README walkChain signature, test counts,
  edges/README stale counts) per the design-doc-status convention; `graph/query/README.md`
  final pass; optional `--explain` flag (CLI prints which table/index answered — receipts
  parity with the UI); optional MCP server (`graph/query/mcp_server.py`, thin over the
  package — in/out per the session-C board fan-out); feed the "how it works" page
  (todos MEDIUM) from `spec/operations.md`.
- **Model:** Sonnet. **Depends:** everything. **Parallel-safe internally.**

### gated side-step H — data hygiene (G18) **[propose → Matt approves → apply]**
Fix the 5 YAML-broken node files (quoting repair), decide the 91 dangling-endpoint edges
(recommend: keep, but the engine *reports* them via `health`; the 67 phantom collective-noun
slugs are Pass-1 references, not errors to delete), dedup the 28 duplicate edge rows.
Mechanically trivial; **every part of it is graph mutation → proposal file first.** Can run
any time after step 1. Model: Sonnet.

### pointer — chronology "Step C" (NOT this Track)
The S185 wiki-date backfill of ~50 undated causal events (deterministic scrape → Haiku
residue) remains its own parked item, gated on Matt's Haiku OK. The query layer consumes
`sort_keys` but does not block on it. Listed here only so it isn't re-lost.

---

## 6. Sequence at a glance (amended S189b — orchestrated bundles)

```
SESSION A (Fable-orchestrated): step 0 + step 1 (scaffold graph/query/) [+ step 7 braid if room]
     │        spec/operations.md v1 + first golden cases land here (drift alarm live)
SESSION B (Fable-orchestrated): step 3 (eval baseline) → step 4 (resolver) → step 5 (search
     │        + routing + list) → eval re-run.   ← the headline session
SESSION C (Fable-orchestrated): step 6 (ports/projection) + step 8a–c (theme/mentions/food-grep)
     │        + side-step H (hygiene, propose→Matt→apply) + step 9 (docs/adapters)
     │        + ADVISORY-BOARD FAN-OUT on the open forks (read_passage / SERVED_AT / MCP / shims)
FINAL SESSION (deferred by Matt): step 2 — the pytest traversal suite, over the finished
              layer, WITH Matt. Nothing else waits on it.
```
Gated items ride outside the bundles: 8d (SERVED_AT pass — vocab decision + Matt's LLM OK),
H's apply half (Matt's go), any prod deploy (manual, Matt). Every retrieval-touching session
ends with an eval re-run and both existing test suites green. Rough scale: 3 orchestrated
sessions + the final suite session — Fable conducts, Sonnet/Haiku execute.

---

## 7. Out of scope / parked (deliberately, with reasons)

- **Embeddings / semantic search** — no Anthropic embeddings API; second vendor not
  justified until keyword evals fail (D-C).
- **Quote/enrichment rebalancing (G5/G8)** — a data track (harvest/dips), not a query-layer
  step; the search index makes existing quotes reachable, which is this Track's job.
- **TWOIAF / F&B ingestion, prophecy minting, theories layer** — data tracks, separately
  gated (theories explicitly Matt-gated).
- **Graph DB migration** — census confirms full-load ≈ 0.5 s at 23k edges; markdown+JSONL is
  nowhere near its limit. SOMEDAY item stays SOMEDAY.
- **Spoiler gating / `first_available`** — deferred by standing decision; the spec notes
  where a tier/spoiler filter would slot (a `where` clause on ops) and stops there.
- **A long-running query server** — the CLI is fast enough; the edge function is the server.
- **Full scripts/ re-taxonomy** — rejected at D-H; extraction + documentation instead.
- **D&E, SIFT, granular dips, concurrent enrichment** — parked by Matt; untouched.

---

## 8. Open forks — status after Matt's S189b review

**Answered by Matt:**
1. **Home:** `graph/query/` (D-A updated).
2. **Pytest suite:** deferred to the Track's final session; Matt pairs on it then.
3. **Interview framing:** dropped as a design driver — project-first throughout.
4. **Execution model:** Fable-orchestrated sessions with Sonnet/Haiku fan-out (§5/§6).

**DECIDED by the S190 advisory-board fan-out (full deliberations: `working/query-layer/boards/`;
Matt overrules on read):**
- **`read_passage` → CLI-only for now.** `corpus-search` shipped CLI-side (step 5e); public-chat
  passage fetch stays designed-but-gated. Flip conditions: (1) a Matt-approved per-session/day
  verbatim-text quota exists (chat-UI/product track owns it), (2) a live smoke measures per-turn
  cost/context. Rationale: the spend cap bounds dollars and the cite gate bounds fabrication, but
  nothing bounds extraction-by-iteration over ~11 MB of chapter text.
- **`SERVED_AT` vocab proposal → WAIT for 8a–c evidence** (3:1; traversal-purist dissent
  recorded). Settle metric now IN the eval set: **Q21 "What was served at the Purple Wedding?"**
  — currently answers in 2 tool calls via search/theme. If post-8a–c it still can't connect
  dish↔event context, that triggers writing the proposal. (8d itself stays triple-gated: vocab
  decision + LLM-pass OK + mutation OK.)
- **MCP adapter → PARKED** (unanimous). No real consumer today; a 5th parity surface; the
  consolidated engine makes it cheap to build when wanted. Un-park trigger: a real external MCP
  client (Claude Desktop / out-of-repo agent) actually needs graph access.
- **Shim retirement → two-tier plan.** Tier A (anytime, cheap): sweep ~6 live docs to the
  `weirwood query` spelling. Tier B (file deletion) gated on ALL of: the final Matt-paired
  pytest session lands equivalent coverage for the 89 shim-loaded tests; the one static importer
  (`backfill-epithet-aliases.py`) repoints (one line); Tier A done. No calendar/telemetry gate —
  local scripts have no invocation telemetry, a time gate would be theater.
- **(Bonus, Matt-steered live in S190) Persona reframe → researcher/wiki-reader frame** drafted
  by the board and wired as LOREMASTER_VOICE (draft in repo; SHARED_RULES safety text preserved
  + test-pinned). **Matt RULED on the three open knobs (S190, in-session):** (1) the flat
  register is DELIBERATE — "it's the base persona; there can be more later" (no dry-enthusiasm
  loosen; additional personas are the future mechanism, not register drift); (2) connective
  reasoning stays tool-grounded (agree with the skeptic — connections only when a tool returned
  them); (3) NO live A/B eval — deploy and judge by feel (the A/B row in the eval harness stays
  empty/retired). Deploy itself remains manual per DEPLOY.md.

**Still Matt-gated regardless of board output:** any graph mutation apply (side-step H, 8d),
any LLM bulk pass (8d Haiku), any prod deploy.

---

## Appendix — session log for this doc
- **2026-07-04 (S189):** created. Four survey subagents (Python CLI modes; TS lib + agent +
  bundle; scripts+tests inventory ×2; graph census) + direct spot-checks. New gaps G11–G19
  added; G1–G10 verdicts recorded (§2b); victim-alias bundle gap and empty food indexes
  verified live. Decisions D-A…D-I taken with alternatives. Step cards 0–9 + gated side-step
  H written. Companion updates: pointer banners/appendix entries in `GRAPH-QUERY-ROADMAP.md`
  and `GRAPH-STATE.md`; `working/todos.md` Track 7 repointed here.
- **2026-07-04 (S189b — Matt's review, same session):** amendments applied: home →
  `graph/query/` (D-A); pytest suite deferred to the Track's FINAL session (D-G/step 2) with
  golden spec cases carrying drift protection from session A; interview framing dropped as a
  driver (project-first); execution model rewritten to three Fable-orchestrated sessions
  (A engine / B retrieval / C reach+close-out) with Sonnet/Haiku fan-out; remaining forks
  routed to a session-C advisory-board fan-out. §6/§8 rewritten accordingly.
- **2026-07-04 (S190 — the orchestrated BUILD):** sessions A+B+C executed in one Fable-orchestrated
  sitting (Sonnet builders; deterministic diff scripts took the Haiku-verify slots). SHIPPED:
  steps 0 (measurements: narrative-arc inline = +198% bundle → D-F resolved to per-node static
  assets; quote index est 2.03 MB; orphan baseline 24.74%), 1 (the `graph/query/` engine, zero
  behavior change — 36/36 CLI cases byte-identical, shims, spec v1 + drift alarm), 7 (braid),
  3 (eval harness Q1–Q21 + frozen baseline), 4 (G19/variants/G10 → 16/20 exact, zero
  regressions; telemetry miner + TurnLog outcome fix), 5 (BM25 search both runtimes + list +
  corpus-search CLI + search_quotes + routing decision table + researcher-persona draft),
  6 (containers/path/participants/expand-beats ports; G9 static assets; parity table closed),
  8a–c (theme index/op; mention-repair PREVIEW-only — apply Matt-gated; food-grep seeder),
  9 (doc-truth G17, graph/query/README, --explain), side-step H (PROPOSAL only; 2 census claims
  didn't reproduce; 7 cross-category slug collisions found). Evals settled the 5d fork: search ≠
  browse → list_nodes+theme chat tools → **Q11 meals ∞→2 tool calls**. All 5 boards run →
  decisions recorded in §8. Remaining: step 2 (final, Matt-paired) + the Matt-gated applies.
- **2026-07-04 (S189c — Matt, at endsession):** loremaster persona reframe added to step 5c —
  frame the persona around a researcher/thought-experimenter user to open up responses; voice
  only, SHARED_RULES safety block untouched; A/B eval row added. Execution handoff changed
  from per-bundle continue prompts to ONE rolled Fable-orchestrator prompt (A→B→C in order,
  stop at a clean bundle boundary when context runs low, mint the remainder prompt there):
  `progress/continue-prompts/2026-07-04-query-layer-orchestrated-build.md`.
- **2026-07-04 (S191 — the Fable-orchestrated FINALE; Track CLOSED):** step 2 landed over the
  finished layer. 3-lens fixture board (coverage/story/adversarial, Sonnet) → the "Salt Debt"
  mini-graph (35 nodes/39 edges, House Quorwyn; causal diamond + 2-hop ENABLES break +
  SUB_BEAT_OF hub straddling the two role-edge sets + 5-generation deep-spine family with
  remarriage/marry-in/single-parent traps + 2 disjoint container bags + "the Eel King"
  ambiguous alias + causal cycle/self-loop/dangling-slug traps + 3 quote-bearing orphan food
  nodes) — Matt checkpoint #1 approved as proposed. Traversal suite: 116 tests at
  `graph/query/tests/` (fixture smoke / resolve / traverse / braid / spec-cases-as-pytest /
  corpus smoke, `corpus` marker auto-deselects without the graph); op-semantics table frozen
  (Matt checkpoint #2). Housekeeping: pytest.ini; the orphaned formalize-edges test relocated
  + made pytest-honest; vocab assertions 167→170 (the +3: SUSPECTED_OF S116, WITNESS_IN S117,
  HONORED_AT S134). Hardening: find_node_file path-escape guard (narrow — 247 legacy
  timestamp-suffixed slugs keep resolving). Tier A doc sweep (12 live-usage swaps) + **Tier B
  shim retirement** (89 tests → package imports with test-count parity proven vs HEAD; the 3
  shims DELETED; netlify.toml/DEPLOY.md/READMEs/zsh aliases repointed). Drift-alarm re-proof:
  broke resolve-red-wedding-exact → deno FAILED but both Python runners PASSED — found the
  run_cases resolve handler never compared `candidates[0].slug`; fixed → all three runners
  fail on the break, all green on restore. Mid-session Matt priority-steer folded in: per-call
  tool OUTCOME logging extended to every chat tool (+ slugs inventory for search/list/theme)
  and the netlify build command now regenerates ALL FIVE bundle files (search-index +
  theme-index were previously deploy-by-accident). NOT in this Track's power: prod deploy
  (manual, Matt), 8d, class-5 dup-slugs (Matt's worktree session). The spend ceiling killed
  the suite-builder subagent AFTER its files landed; orchestrator finished solo.
