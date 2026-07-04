"""build/ — builders for QUERY-SERVING artifacts.

These scripts produce derived, rebuildable lookup tables/indexes consumed by
weirwood_query (alias tables, search index, theme index, chat bundle). They
are NOT graph mutation (graph/nodes, graph/edges, graph/index stay read-only)
— outputs land in working/wiki/data/ or web/data/, exactly where the scripts
they absorbed already wrote.
"""
