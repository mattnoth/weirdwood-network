// Retrieval-core public surface. The Edge function (function chunk) imports from
// here: load the bundle once at cold start, then bind it with createTools().
//
//   import { loadGraphData, createTools } from "./src/lib/mod.ts";
//   const tools = createTools(await loadGraphData());
//   tools.resolve("death of Tywin");           // -> [{slug, category, …}]
//   tools.walkChain("assassination-of-tywin-lannister");
//
// All four tools are read-only and pure over the loaded GraphData.

export type {
  AliasCandidate,
  AliasMap,
  ChainLink,
  ChainResult,
  Edge,
  GraphData,
  NeighborLink,
  NeighborsResult,
  NodeQuote,
  NodeRecord,
  NodesMap,
  ResolveCandidate,
} from "./types.ts";

export { DEFAULT_DATA_DIR, loadGraphData } from "./data.ts";
export { normalize, tokenize } from "./normalize.ts";
export { cleanPhrase, isValidSlug } from "./validate.ts";
export { resolve } from "./resolve.ts";
export { neighbors, walkChain } from "./graph.ts";
export { readNode } from "./read-node.ts";

import type {
  ChainResult,
  GraphData,
  NeighborsResult,
  NodeRecord,
  ResolveCandidate,
} from "./types.ts";
import { resolve } from "./resolve.ts";
import { neighbors, walkChain } from "./graph.ts";
import { readNode } from "./read-node.ts";

/** The four retrieval tools, bound to a loaded bundle. */
export interface Tools {
  resolve(phrase: string): ResolveCandidate[];
  walkChain(slug: string, opts?: { full?: boolean }): ChainResult;
  neighbors(slug: string): NeighborsResult;
  readNode(slug: string): NodeRecord | null;
}

/** Bind GraphData into the four read-only tools the Edge function exposes to Claude. */
export function createTools(data: GraphData): Tools {
  return {
    resolve: (phrase) => resolve(phrase, data),
    walkChain: (slug, opts) => walkChain(slug, data, opts),
    neighbors: (slug) => neighbors(slug, data),
    readNode: (slug) => readNode(slug, data),
  };
}
