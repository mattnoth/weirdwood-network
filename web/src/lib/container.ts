// container(name) — bag-retrieval over the `containers:` frontmatter tag
// (query-layer Track, step 6a; design.md's settled 5(+)-container axis:
// essos/wo5k/north/aegon/bran, plus whatever else frontmatter carries —
// this op does not hardcode the set, it reads whatever `NodeRecord.containers`
// ships).
//
// Ports `graph/query/weirwood_query/traverse.py::container()` against the
// bundle's `nodes.json` (which now carries a `containers` field per node —
// see build_chat_bundle.py's load_nodes(), step 6a). UNORDERED bag-retrieval:
// explicitly NOT the causal walk (`chain`/`walkChain`) — a container is a tag
// on nodes belonging to one narrative arc/region, not a graph traversal.
//
// No LLM in the loop, ever — pure data.

import type { ContainerItem, ContainerResult, GraphData } from "./types.ts";

/**
 * Every node whose `containers:` array includes `name` (case-insensitive),
 * sorted by (type, slug) — same ordering convention as the Python
 * `container()`'s sort, where `type` is the frontmatter `type:` scalar (e.g.
 * "character.pov"), NOT the graph/nodes/ category directory (`NodeRecord.type`
 * carries the same scalar the Python `fields.get("type", "")` reads — see
 * build_chat_bundle.py's load_nodes()). An unknown/empty container name
 * returns `count: 0, nodes: []`, not an error (mirrors `listNodes()`'s /
 * `theme()`'s "no matches" convention — a typo is a query mistake, not a
 * system fault).
 */
export function container(name: string, data: GraphData): ContainerResult {
  const target = name.trim().toLowerCase();
  const nodes: ContainerItem[] = [];

  for (const [slug, rec] of Object.entries(data.nodes)) {
    const containers = rec.containers;
    if (!containers || containers.length === 0) continue;
    const lower = containers.map((c) => c.toLowerCase());
    if (!lower.includes(target)) continue;
    nodes.push({
      slug,
      type: rec.type ?? "",
      name: rec.name,
      containers,
    });
  }

  nodes.sort((a, b) => {
    if (a.type !== b.type) return a.type < b.type ? -1 : 1;
    return a.slug < b.slug ? -1 : a.slug > b.slug ? 1 : 0;
  });

  return { container: name, count: nodes.length, nodes };
}
