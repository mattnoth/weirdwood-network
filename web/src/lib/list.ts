// listNodes(opts) — trivial browse surface over the bundle's nodes map
// (query-layer Track, step 5d; design.md G6 "no browse surface").
//
// Ports `graph/query/weirwood_query/list_nodes.py`'s semantics against the
// bundle: `category` (the graph/nodes/ type-directory name, e.g. "foods" —
// see NodeRecord.category's comment) filters which nodes are candidates;
// `hasQuotes` keeps only nodes carrying ≥1 curated quote; results are sorted
// by slug ascending (deterministic) and paged via limit/offset. No chat tool
// wired to this yet — the design doc gates that decision on evals.
//
// PROFILE DIFFERENCE from the Python full-profile `list --container NAME`
// filter: `containers:` frontmatter is not in the bundle yet (design.md step
// 6a, not done) — this bounded profile has no container filter until that
// ships. Documented, not a bug (design.md §0's "documented profile
// difference, not a bug" convention).
//
// No LLM in the loop, ever — pure data.

import type { GraphData, ListItem, ListResult } from "./types.ts";

const DEFAULT_LIMIT = 50;

/**
 * Browse one node category, optionally filtered to quote-bearing nodes,
 * paged. Returns `{category, total, offset, limit, items}` — `total` counts
 * every filter-matching node BEFORE paging (`total - offset - items.length`
 * tells the caller how many more remain). An unknown/empty category returns
 * `total: 0, items: []`, not an error (a category typo is a query mistake,
 * not a system fault — mirrors container()'s "no matches" convention).
 */
export function listNodes(
  data: GraphData,
  opts: { type: string; hasQuotes?: boolean; limit?: number; offset?: number },
): ListResult {
  const { type: category, hasQuotes = false, limit = DEFAULT_LIMIT, offset = 0 } = opts;

  const items: ListItem[] = [];
  for (const [slug, rec] of Object.entries(data.nodes)) {
    if (rec.category !== category) continue;
    if (hasQuotes && rec.quotes.length === 0) continue;
    items.push({ slug, name: rec.name, quoteCount: rec.quotes.length });
  }
  items.sort((a, b) => (a.slug < b.slug ? -1 : a.slug > b.slug ? 1 : 0));

  const total = items.length;
  const page = items.slice(offset, offset + limit);

  return { category, total, offset, limit, items: page };
}
