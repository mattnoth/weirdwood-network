// Retrieval-core public surface. The Edge function (function chunk) imports from
// here: load the bundle once at cold start, then bind it with createTools().
//
//   import { loadGraphData, createTools } from "./src/lib/mod.ts";
//   const tools = createTools(await loadGraphData());
//   tools.resolve("death of Tywin");           // -> [{slug, category, …}]
//   tools.walkChain("assassination-of-tywin-lannister");
//
// All tools are read-only and pure over the loaded GraphData.

export type {
  AliasCandidate,
  AliasMap,
  ChainLink,
  ChainResult,
  Edge,
  FamilyBond,
  FamilyMember,
  FamilyTreeResult,
  GraphData,
  ListItem,
  ListResult,
  NeighborLink,
  NeighborsResult,
  NodeQuote,
  NodeRecord,
  NodesMap,
  ResolveCandidate,
  SearchIndex,
  SearchIndexDocRow,
  SearchResult,
  SpouseBond,
} from "./types.ts";

export { loadGraphData } from "./data.ts";
export { normalize, tokenize } from "./normalize.ts";
export { cleanPhrase, isValidSlug } from "./validate.ts";
export { resolve } from "./resolve.ts";
export { familyTree, neighbors, walkChain } from "./graph.ts";
export { readNode } from "./read-node.ts";
export { searchQuotes } from "./search.ts";
export { listNodes } from "./list.ts";

import type {
  ChainResult,
  FamilyTreeResult,
  GraphData,
  ListResult,
  NeighborsResult,
  NodeRecord,
  ResolveCandidate,
  SearchResult,
} from "./types.ts";
import { resolve } from "./resolve.ts";
import { familyTree, neighbors, walkChain } from "./graph.ts";
import { readNode } from "./read-node.ts";
import { searchQuotes } from "./search.ts";
import { listNodes } from "./list.ts";

/** The read-only retrieval tools, bound to a loaded bundle. */
export interface Tools {
  resolve(phrase: string): ResolveCandidate[];
  walkChain(slug: string): ChainResult;
  neighbors(slug: string): NeighborsResult;
  familyTree(slug: string): FamilyTreeResult;
  readNode(slug: string): NodeRecord | null;
  /** Content-first retrieval over quotes/identity blurbs (query-layer step
   *  5b). NOT yet wired as a chat tool in agent.ts — that decision is a
   *  separate follow-up (out of this Track's scope); exposed here so an
   *  in-repo caller (or that follow-up work) has one place to bind it. */
  searchQuotes(query: string, opts?: { type?: string; limit?: number }): SearchResult[];
  /** Browse surface (query-layer step 5d). Same "not a chat tool yet" note
   *  as searchQuotes — gated on evals per the design doc. */
  listNodes(opts: { type: string; hasQuotes?: boolean; limit?: number; offset?: number }): ListResult;
}

/** Bind GraphData into the read-only tools the Edge function exposes to Claude. */
export function createTools(data: GraphData): Tools {
  return {
    resolve: (phrase) => resolve(phrase, data),
    walkChain: (slug) => walkChain(slug, data),
    neighbors: (slug) => neighbors(slug, data),
    familyTree: (slug) => familyTree(slug, data),
    readNode: (slug) => readNode(slug, data),
    searchQuotes: (query, opts) => searchQuotes(query, data, opts),
    listNodes: (opts) => listNodes(data, opts),
  };
}
