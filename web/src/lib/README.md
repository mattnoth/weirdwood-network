# Retrieval tools (`web/src/lib/`) — TO BUILD (retrieval-core chunk)

Deno/TypeScript ports of the read-only graph queries the demo agent does by hand
(`working/demo-asoiaf-loremaster.md`), reading the static bundle in `web/data/`
(shapes in [`web/README.md`](../../README.md)). These are imported by the Edge
function and exposed to Claude as tools.

Port the logic from `scripts/graph-query.py` + `scripts/event_alias_resolver.py`
— do NOT shell out to Python (Netlify Edge runs Deno).

| Tool | Signature | Returns | Source to port |
|---|---|---|---|
| `resolve` | `resolve(phrase)` | `[{slug, category}]` | `event_alias_resolver.py` (exact → fuzzy/substring fallback) |
| `walk_chain` | `walkChain(slug)` | `{upstream[], downstream[]}` typed-edge links | `graph-query.py --causal-chain` (CAUSES/TRIGGERS/MOTIVATES; +ENABLES for full) |
| `neighbors` | `neighbors(slug)` | edges grouped by type (the NO-CHAIN view) | `graph-query.py --neighbors` |
| `read_node` | `readNode(slug)` | `{name, type, identity, quotes}` | `nodes.json` lookup |
| `search_chapters` *(fast-follow)* | `searchChapters(query)` | `[{chapter, line, text}]` | grep over bundled chapter text — **needs a build-time inverted index** to stay under the 50 ms CPU budget (don't raw-scan 4 MB per call) |
| `read_passage` *(fast-follow)* | `readPassage(chapter, lineRange)` | book text at a cite | bundled chapter files, bounded line span |

**Receipts contract:** each retrieval tool returns structured typed-edge JSON
`{source, edge_type, target, evidence_quote, ref}` on a channel SEPARATE from the
streamed prose — the receipts panel renders from that return, NOT by parsing the
narration (design §3 note).

**Bounding (the tool layer is the trust boundary):** validate/allowlist every
tool input; cap `read_passage` line span; treat returned book text as untrusted
data, never as instructions.
