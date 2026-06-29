// walkChain(slug) + neighbors(slug) — the typed-edge graph queries.
//
// Ports scripts/graph-query.py: --causal-chain (walkChain) and --neighbors.
// Both read the bundle edges.json (short keys: {type, source, target, quote,
// ref, tier, relation}) and emit receipts-shaped links the panel renders
// directly. Invalid slugs yield empty results (trust boundary, validate.ts).

import type {
  ChainLink,
  ChainResult,
  Edge,
  GraphData,
  NeighborLink,
  NeighborsResult,
} from "./types.ts";
import { isValidSlug } from "./validate.ts";

// Edge types that carry causal consequence (vs PRECEDES = pure chronology).
// Walking all three reconstructs a narrative-arc chain no single edge holds.
const CAUSAL_EDGE_TYPES: ReadonlySet<string> = new Set(["CAUSES", "TRIGGERS", "MOTIVATES"]);
// ENABLES is a precondition, not a consequence — excluded by default, added by
// the full-chain walk so a spine reads end-to-end through its preconditions.
const FULL_CHAIN_EDGE_TYPES: ReadonlySet<string> = new Set([
  ...CAUSAL_EDGE_TYPES,
  "ENABLES",
]);

function toChainLink(e: Edge, depth: number): ChainLink {
  return {
    source: e.source,
    edge_type: e.type,
    target: e.target,
    evidence_quote: e.quote ?? null,
    ref: e.ref ?? null,
    tier: e.tier ?? null,
    depth,
  };
}

/**
 * BFS-walk causal edges transitively from `start`.
 *   direction "down": follow edges where source === current (effects)
 *   direction "up":   follow edges where target === current (causes)
 * Cycle-safe: each node is expanded once, so every edge is emitted once even
 * across diamonds. Returns links in breadth-first order, depth 1 = adjacent.
 */
function walkCausal(
  start: string,
  edges: Edge[],
  direction: "up" | "down",
  edgeTypes: ReadonlySet<string>,
): ChainLink[] {
  const [keyHere, keyNext]: [keyof Edge, keyof Edge] = direction === "down"
    ? ["source", "target"]
    : ["target", "source"];

  const adj = new Map<string, Edge[]>();
  for (const e of edges) {
    if (!edgeTypes.has(e.type)) continue;
    const here = e[keyHere] as string;
    let bucket = adj.get(here);
    if (!bucket) adj.set(here, bucket = []);
    bucket.push(e);
  }

  const visited = new Set<string>([start]);
  const result: ChainLink[] = [];
  const frontier: Array<[string, number]> = [[start, 0]];
  while (frontier.length > 0) {
    const [node, depth] = frontier.shift()!;
    for (const e of adj.get(node) ?? []) {
      result.push(toChainLink(e, depth + 1));
      const nxt = e[keyNext] as string;
      if (nxt && !visited.has(nxt)) {
        visited.add(nxt);
        frontier.push([nxt, depth + 1]);
      }
    }
  }
  return result;
}

/**
 * Walk the causal chain both directions from `slug`: upstream antecedents and
 * downstream consequences. `opts.full` additionally follows ENABLES
 * preconditions (graph-query.py --full-chain). Empty result for an invalid slug.
 */
export function walkChain(
  slug: string,
  data: GraphData,
  opts: { full?: boolean } = {},
): ChainResult {
  const full = opts.full ?? false;
  if (!isValidSlug(slug)) {
    return { slug: String(slug), full, upstream: [], downstream: [] };
  }
  const types = full ? FULL_CHAIN_EDGE_TYPES : CAUSAL_EDGE_TYPES;
  return {
    slug,
    full,
    upstream: walkCausal(slug, data.edges, "up", types),
    downstream: walkCausal(slug, data.edges, "down", types),
  };
}

function toNeighborLink(e: Edge): NeighborLink {
  return {
    source: e.source,
    edge_type: e.type,
    target: e.target,
    evidence_quote: e.quote ?? null,
    ref: e.ref ?? null,
    tier: e.tier ?? null,
  };
}

function groupByType(edges: Edge[]): Record<string, NeighborLink[]> {
  const out: Record<string, NeighborLink[]> = {};
  for (const e of edges) {
    (out[e.type] ??= []).push(toNeighborLink(e));
  }
  return out;
}

/**
 * All edges touching `slug`, split OUTGOING (slug is source) / INCOMING (slug is
 * target) and grouped by edge_type — the relational NO-CHAIN view
 * (graph-query.py --neighbors). Empty result for an invalid slug.
 */
export function neighbors(slug: string, data: GraphData): NeighborsResult {
  if (!isValidSlug(slug)) {
    return { slug: String(slug), outgoingCount: 0, incomingCount: 0, outgoing: {}, incoming: {} };
  }
  const outgoing: Edge[] = [];
  const incoming: Edge[] = [];
  for (const e of data.edges) {
    if (e.source === slug) outgoing.push(e);
    if (e.target === slug) incoming.push(e);
  }
  return {
    slug,
    outgoingCount: outgoing.length,
    incomingCount: incoming.length,
    outgoing: groupByType(outgoing),
    incoming: groupByType(incoming),
  };
}
