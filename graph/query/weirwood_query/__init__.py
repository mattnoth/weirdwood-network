"""weirwood_query — the Weirwood Network's single Python query engine.

Consolidates scripts/graph-query.py, scripts/event_alias_resolver.py, and
scripts/build-chat-export.py's shared infrastructure (query-layer design.md,
step 1). NOT pip-installed — callers add `<repo>/graph/query` to
`sys.path` / `PYTHONPATH` (see this package's parent-resolution convention in
load.REPO_ROOT, derived from `Path(__file__).resolve()`, never cwd).

Modules:
  model         — Node / Edge dataclasses
  load          — ONE loader: frontmatter, edges.jsonl, alias tables, node index
  normalize     — ONE normalizer/tokenizer (mirrors web/src/lib/normalize.ts)
  resolve       — phrase -> slug resolution (exact -> ambiguous -> character -> fuzzy)
  traverse      — neighbors, causal/full chain, expand-beats, path,
                  event-participants, container, family_tree
  braid         — fork-hubs / join-hubs / braid (S117 convergence-map charter, step 7)
  search        — BM25-ish content search over quotes/identity blurbs (step 5b)
  list_nodes    — browse surface over one node category (step 5d)
  corpus_search — CLI-only grep-class full-text scan over sources/chapters/ (step 5e)
  report        — the legacy node-inspection report (`## Edges` prose + inbound refs)
  cli           — `weirwood query …` argparse entry point
"""

from . import (
    braid,
    corpus_search,
    list_nodes,
    load,
    model,
    normalize,
    report,
    resolve,
    search,
    traverse,
)

__all__ = [
    "braid",
    "corpus_search",
    "list_nodes",
    "load",
    "model",
    "normalize",
    "report",
    "resolve",
    "search",
    "traverse",
]
