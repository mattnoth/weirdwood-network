# The Weirwood Network

A structured knowledge graph for A Song of Ice and Fire (ASOIAF). Characters, locations,
events, relationships, and more are extracted from the source texts and the AWOIAF wiki into
a queryable graph of typed, cited edges — **9,225 nodes and 26,740 edges** — with a deployed
chat-UI on top of it.

*(Spoiler gating via `first_available` is designed but **deferred** — the field is optional
in v1 nodes and existing values may be wrong. Don't rely on it yet.)*

## Live Chat Demo — the Loremaster

**→ https://weirwood-network.netlify.app**

A deployed, book-grounded ASOIAF chat built on top of the graph. Ask a question and the
**loremaster** answers in a flat, factual researcher's register, grounded in the Weirwood
Network: it resolves your query to real graph nodes, walks the typed-edge relationships,
quotes the books with citations, and shows you the **chain of edges it walked** as receipts.
Ask for a lineage (*"the Targaryen line from Aegon the Conqueror down to Daenerys"*) and it
renders the family tree; ask a causal question (*"why did Robert's Rebellion start?"*) and it
narrates the CAUSES/TRIGGERS/MOTIVATES chain.

A second in-character **Bloodraven** persona exists in the code but is **parked** — the
toggle is not exposed in the UI, and the loremaster is the only live voice.

**Stack:** static front-end + **Netlify Edge Functions** (Deno/TypeScript) running a Claude
tool-use loop. Production runs **Opus 4.8**, set via the `WEIRWOOD_MODEL` env var (which
overrides the code default). The ~13 MB curated-graph bundle is generated from `graph/` at
build time and compiled into the edge function; the Anthropic API key lives server-side in
the function (the browser never sees it), behind a daily spend cap. Full details and
local-dev instructions: [`web/README.md`](web/README.md). Deploy procedure (there is no
git-CD — pushing ships nothing): [`DEPLOY.md`](DEPLOY.md).

Run it locally:

```bash
# (re)generate the web/data/ bundle — three separate builders, all three needed
python3 graph/query/build/build_chat_bundle.py
python3 graph/query/build/build_search_index.py
python3 graph/query/build/build_theme_index.py

cd web && deno task test   # 102 tests over the retrieval core
# live end-to-end: `netlify dev` (needs the Netlify CLI + an ANTHROPIC_API_KEY in web/.env)
```

## Explore the Graph Locally

The graph is **already built and committed** — 9,225 nodes and 26,740 typed edges under
`graph/`. Nothing needs extracting or fetching to query it. Set up the shell function once:

```bash
echo 'source ~/source/asoiaf-chat/scripts/weirwood.zsh' >> ~/.zshrc
source ~/.zshrc
```

If the repo isn't at `~/source/asoiaf-chat`, point `WEIRWOOD_PROJECT_DIR` at it first:

```bash
export WEIRWOOD_PROJECT_DIR="/path/to/asoiaf-chat"
source "$WEIRWOOD_PROJECT_DIR/scripts/weirwood.zsh"
```

`weirwood query` is the front door to the traversal engine (`graph/query/weirwood_query/`).
Every command takes a **slug** (`eddard-stark`, `house-stark`) — use `resolve` to turn a
natural phrase into one:

```bash
weirwood query resolve "the Red Wedding"     # phrase → slug
weirwood query read eddard-stark             # node: frontmatter, prose, edges
weirwood query neighbors house-stark         # all edges touching a node, grouped by type
weirwood query path jaime-lannister brienne-of-tarth   # direct edges + 2-hop bridges
weirwood query chain roberts-rebellion       # walk CAUSES/TRIGGERS/MOTIVATES transitively
weirwood query family aegon-i-targaryen      # lineage tree
weirwood query health                        # graph-wide stats
```

| Command | What it walks |
|---------|---------------|
| `weirwood query resolve <phrase>` | Natural phrase → node slug |
| `weirwood query read <slug>` | One node: header, prose, outbound + inbound edges |
| `weirwood query neighbors <slug>` | Every edge touching a node, split outgoing/incoming |
| `weirwood query path <a> <b>` | Direct edges between two nodes, plus 2-hop bridges |
| `weirwood query chain <slug>` | Causal chain — CAUSES/TRIGGERS/MOTIVATES, both directions |
| `weirwood query full-chain <slug>` | Follows ENABLES as well; `--expand-beats` expands sub-beats |
| `weirwood query participants <hub>` | Union of role edges across an event hub's sub-beats |
| `weirwood query container <name>` | Bag-retrieval for a container tag (`essos`, `wo5k`, `north`, …) |
| `weirwood query family <slug>` | Family tree rooted at a character |
| `weirwood query health` | Node/edge counts and graph-wide stats |

Add `--json` to any of them for machine-readable output. `weirwood graph …` is a permanent
short alias for the same engine. Full flag surface: `weirwood query --help`. Contract and
parity cases: `graph/query/spec/`.

After any mutation that **adds or renames nodes**, rebuild the derived artifacts (indexes +
alias table) or the new nodes won't resolve:

```bash
weirwood refresh            # rebuild all derived artifacts
weirwood refresh --check    # warn if artifacts are stale vs graph/nodes/
```

## How the Graph Got Built

The graph came out of a sequence of extraction passes over the books and the wiki cache.
Those passes are **history, not a setup step** — the ones that have run are done, and their
outputs are committed. You don't run them to work on this project, and they aren't yours to
launch: they cost real money and need the raw book text, which is gitignored and not
distributed.

- Pipeline sequence and pass-by-pass status → [`CLAUDE.md`](CLAUDE.md)
- Extraction machinery, if a re-run is ever deliberately required → [`working/runbooks/mechanical-extraction-howto.md`](working/runbooks/mechanical-extraction-howto.md)
- Every script, indexed → [`scripts/README.md`](scripts/README.md)

Day-to-day work has since moved past the numbered-pass sweeps into **enrichment dips** —
targeted, arc-by-arc deepening of the built graph. `worklog.md` has the live state.

## Project Structure

```
asoiaf-chat/
├── graph/
│   ├── nodes/                       Entity files (characters, locations, events, …)
│   ├── edges/                       edges.jsonl — the typed-edge layer
│   ├── query/                       THE query layer: weirwood_query/ engine + build/ + spec/
│   └── index/                       Derived entity + chapter indexes (weirwood refresh)
├── web/                             The deployed chat-UI — see web/README.md
│   ├── public/                      Static site (chat page, theme tokens)
│   ├── src/lib/                     Retrieval tools (TS port of the query engine)
│   └── netlify/edge-functions/      chat.ts (Claude tool-loop) + node.ts (dossier lookup)
├── sources/
│   ├── raw/                         Source .txt files (GITIGNORED)
│   ├── chapters/{book}/             Split chapter files (tracked)
│   └── wiki/_raw/                   17,657-page AWOIAF cache (tracked; never re-fetch)
├── extractions/
│   ├── mechanical/{book}/           Pass 1 extraction outputs (344 chapters)
│   └── archives/                    Prior-version extractions
├── scripts/                         Python + shell tooling — README.md is the index
│   ├── weirwood.zsh                 Front-door CLI (query, refresh, run, wiki, extraction)
│   └── chapter-splitter.py          Splits .txt into per-chapter markdown
├── reference/
│   ├── architecture.md              Data model: entity types, edge types, confidence tiers
│   ├── glossary.md                  Canonical vocabulary (Pass / Track / Tier)
│   ├── pov-characters.md            POV lookup table + expected chapter counts
│   └── foreshadowing-events.md      26 events + 15 Chekhov's guns
├── curation/                        Agent-proposed findings awaiting Matt's decision
├── working/                         Active scratchpad: TODOs, runbooks, stats, audits
├── progress/                        Wave logs, continue prompts
├── history/                         Frozen records: session details, worklog archives
├── worklog.md                       Living project state — the authoritative status file
└── CLAUDE.md                        Full orchestrator guide + agent system documentation
```

## Where State Lives

- **`worklog.md`** — the authoritative state file: current state, active decisions, backlog,
  and the last five session entries. When anything else disagrees with it, trust the worklog.
  (`worklog-dunk-egg.md` is authoritative for the separate Dunk & Egg track.)
- **`CLAUDE.md`** — the orchestrator guide: conventions, hard rules, agent roster.
- **`reference/architecture.md`** — the data model. Must stay in sync with agent schemas.
- **`DEPLOY.md`** — how the chat-UI actually ships. There is no git-CD; pushing ships nothing.
