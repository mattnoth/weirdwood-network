# graph/query/ — the query layer

One engine, two profiles, one contract. This is the consolidated Python query engine for the
Weirwood Network graph — it replaced four accidental, non-communicating query surfaces
(`scripts/graph-query.py`, `scripts/event_alias_resolver.py`, the unused `graph/index/`
tables, and the standalone `web/src/lib/*` TS port) with a single documented set of
operations (resolve / neighbors / chain / family / search / list / theme / container / path /
participants / braid / corpus-search / mentions / health), each with pinned semantics and
shared golden test cases. Born query-layer Track, step 1 (S189's master design at
`working/query-layer/design.md`).

**Two profiles, one contract:**
- **full** — this package (`weirwood_query/`), reading the live graph on disk
  (`graph/nodes/`, `graph/edges/edges.jsonl`) plus derived tables it builds under `build/`.
  Used by the CLI (`weirwood query …`) and any local/offline tooling.
- **bounded** — the TS port at `web/src/lib/` (own README there), reading a pre-built static
  JSON bundle (`web/data/`) with no filesystem access, for the Netlify Edge chat function's
  50 ms CPU budget. Same operation semantics, same golden cases, deliberately a **strict
  subset** where the full profile has ops (`corpus-search` is CLI-only by design; `passage`
  is designed-but-gated — see that README).

Where the two profiles diverge (status-enum shape, uncapped vs depth-bounded chain walks,
etc.), `spec/operations.md` records it explicitly — it does not paper over the difference.

## Directory map

```
graph/query/
├── README.md                 # this file
├── weirwood_query/           # the full-profile engine package
│   ├── cli.py                 # `weirwood query <subcommand>` — argparse + legacy-flag surface
│   ├── load.py                 # disk I/O: load_edges(), node-index loaders, alias-table loaders
│   ├── model.py                 # shared dataclasses/type shapes
│   ├── normalize.py             # normalize()/tokenize() — ported verbatim to web/src/lib/normalize.ts
│   ├── resolve.py                # phrase -> slug resolution (exact / character / fuzzy)
│   ├── traverse.py               # neighbors/path/health/event_participants/causal_chain/container/family_tree
│   ├── braid.py                  # fork-hubs / join-hubs / braid (convergence-map primitives)
│   ├── search.py                  # content-first quote/identity-blurb search (BM25-ish)
│   ├── list_nodes.py               # browse-one-category op
│   ├── themes.py                    # theme -> members lookup (fixed named-theme table)
│   ├── corpus_search.py              # full chapter-text scan — CLI-only, no bundle/chat exposure
│   ├── mentions.py                    # graph/index/ mention-count lookup (may be stale — see G13)
│   └── report.py                       # legacy single-node inspection report (the original mode)
├── build/                      # derived-artifact builders (run before CLI/bundle use)
│   ├── build_alias_table.py     # phrase->slug lookup + collision table (resolve.py consumes it)
│   ├── build_chat_bundle.py      # web/data/{alias-map,nodes,edges,manifest}.json
│   ├── build_search_index.py      # web/data/search-index.json (BM25-ish inverted index)
│   ├── build_theme_index.py        # web/data/theme-index.json + the full-profile theme table
│   ├── build_node_assets.py         # web/public/node/<slug>.json (narrative-arc dossier assets)
│   └── build_mention_index_preview.py  # repair/preview tool for the mentions() staleness check
└── spec/
    ├── operations.md            # THE op reference — inputs/outputs/semantics/caps per op, both profiles
    ├── run_cases.py              # Python golden-case runner (full/both-profile cases)
    └── cases/*.json               # the golden cases themselves (shared with the TS test suite)
```

## How to invoke

**Shell function (preferred, if `weirwood.zsh` is sourced in your shell):**
```bash
weirwood query <slug>                          # node inspection
weirwood query resolve "the Red Wedding"       # phrase -> slug
weirwood query neighbors eddard-stark
weirwood query chain assassination-of-tywin-lannister [--expand-beats]
weirwood query full-chain <slug>               # chain + ENABLES preconditions
weirwood query family eddard-stark
weirwood query path arya-stark jaqen-hghar
weirwood query container wo5k
weirwood query search "lemon cakes" [--type foods]
weirwood query list --type foods [--has-quotes]
weirwood query theme "hospitality"
weirwood query braid <slugA> <slugB> [more...]
weirwood query health
```
(`weirwood.zsh`'s `query` case runs `PYTHONPATH=graph/query python3 -m weirwood_query.cli "$@"`
— see below if you don't have it sourced.)

**Direct invocation (no shell function needed):**
```bash
cd /path/to/asoiaf-chat
PYTHONPATH=graph/query python3 -m weirwood_query.cli <subcommand-or-legacy-flag> <args>
```
`PYTHONPATH=graph/query` is required — `weirwood_query` is not installed as a package, it's
imported straight off the repo tree. Every invocation in this doc and in `operations.md`
assumes that prefix.

**Two argv surfaces, same engine — `cli.py`'s subcommand front door translates the newer
`weirwood query <subcommand> <args>` form into the original legacy flags
(`--neighbors`/`--causal-chain`/etc.) before argparse ever sees it; both forms are supported
forever, byte-identical output either way.** `--json` on any subcommand emits machine-readable
JSON instead of the formatted text report.

**The shims note:** `scripts/graph-query.py` and `scripts/event_alias_resolver.py` still exist
as thin **compat shims** — they re-export this package's functions and preserve the exact old
CLI surface + byte-identical stdout, so nothing that imported them (tests, other scripts)
broke when the engine moved here. They print a deprecation banner to stderr. Do not add new
logic to them; new work lands in `weirwood_query/`. Prefer `weirwood query` (or the direct
`python3 -m weirwood_query.cli` invocation above) for anything new.

## How the drift alarm works

Every operation has **golden test cases** in `spec/cases/*.json`, each tagged with a
`profile` (`bounded` / `full` / `both`) saying which engine(s) it's checked against. Two
runners consume the same case files so the two profiles can't silently diverge:

- **`spec/run_cases.py`** (Python) — runs every `full`/`both`-tagged case against this
  package directly. Not a pytest suite (deliberately deferred — see `operations.md`'s header);
  run it directly and read the pass/fail/skip tally:
  ```bash
  PYTHONPATH=graph/query python3 graph/query/spec/run_cases.py
  ```
  It SKIPS (never crashes the run) when a callable doesn't exist yet or a case's shape can't
  be interpreted — a skip is expected mid-build, not a failure signal once the engine is
  complete.
- **`web/src/lib/spec_cases_test.ts`** (Deno) — runs every `bounded`/`both`-tagged case
  against the live TS port + the real `web/data/` bundle:
  ```bash
  cd web && deno task test
  ```

If a case is tagged `both`, passing on one runner and failing on the other means the two
profiles have drifted — that's the signal this dual-runner setup exists to catch. When you
change resolver/traversal logic, mirror the change in **both** `weirwood_query/*.py` and the
matching `web/src/lib/*.ts` file, then re-run both commands before calling it done.

## Reference docs

- **`spec/operations.md`** — the op-by-op reference: inputs, outputs, exact semantics for
  both profiles, known cross-profile mismatches (recorded, not hidden), and caps/limits.
  Read this before changing any op's behavior.
- **`working/query-layer/design.md`** — the design record: why this package exists, the
  decisions made at each fork, and the step-by-step build plan. Read this for the *why*;
  read `operations.md` for the *what*, this file for the *where or how to invoke*.
- **`web/src/lib/README.md`** — the bounded-profile (TS) side: same ops, module-by-module,
  its own test count and usage example.

## Session log (query-layer Track)

- **step 9** (2026-07-04) — doc-truth sweep: fixed `web/src/lib/README.md`'s stale
  `walkChain` signature and test count, `graph/edges/README.md`'s stale edge count, added
  this file, added a cheap `--explain` flag to `resolve`'s CLI path. See
  `spec/operations.md`'s own appendix for the itemized before/after counts.
