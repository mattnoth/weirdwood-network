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
  ChainBeat,
  ChainLink,
  ChainResult,
  ContainerItem,
  ContainerResult,
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
  ParticipantRecord,
  ParticipantsResult,
  PathBridge,
  PathDirectEdge,
  PathResult,
  ResolveCandidate,
  SearchIndex,
  SearchIndexDocRow,
  SearchResult,
  SpouseBond,
  ThemeIndex,
  ThemeMember,
  ThemeResult,
  ThemeSummary,
} from "./types.ts";

export { loadGraphData } from "./data.ts";
export { normalize, tokenize } from "./normalize.ts";
export { cleanPhrase, isValidSlug } from "./validate.ts";
export { resolve } from "./resolve.ts";
export { familyTree, neighbors, walkChain } from "./graph.ts";
export { readNode } from "./read-node.ts";
export { searchQuotes } from "./search.ts";
export { listNodes } from "./list.ts";
export { listThemes, theme } from "./themes.ts";
export { container } from "./container.ts";
export { path } from "./path.ts";
export { participants } from "./participants.ts";

import type {
  ChainResult,
  ContainerResult,
  FamilyTreeResult,
  GraphData,
  ListResult,
  NeighborsResult,
  NodeRecord,
  ParticipantsResult,
  PathResult,
  ResolveCandidate,
  SearchResult,
  ThemeResult,
  ThemeSummary,
} from "./types.ts";
import { resolve } from "./resolve.ts";
import { familyTree, neighbors, walkChain } from "./graph.ts";
import { readNode } from "./read-node.ts";
import { searchQuotes } from "./search.ts";
import { listNodes } from "./list.ts";
import { listThemes, theme } from "./themes.ts";
import { container } from "./container.ts";
import { path } from "./path.ts";
import { participants } from "./participants.ts";

/** The read-only retrieval tools, bound to a loaded bundle. */
export interface Tools {
  resolve(phrase: string): ResolveCandidate[];
  walkChain(slug: string, opts?: { maxDepth?: number; expandBeats?: boolean }): ChainResult;
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
  /** theme->members routing table lookup (query-layer step 8a). Same
   *  "not a chat tool yet" note as searchQuotes/listNodes. */
  theme(name: string, opts?: { category?: string }): ThemeResult;
  /** Discovery surface: every theme name + member count. */
  listThemes(): ThemeSummary[];
  /** Bag-retrieval over the `containers:` tag (query-layer step 6a). Same
   *  "not a chat tool yet" note as searchQuotes/listNodes/theme — no chat
   *  tool wired in agent.ts (out of this Track's scope; see mod.ts header). */
  container(name: string): ContainerResult;
  /** Direct edges + 2-hop bridges between two nodes (query-layer step 6b).
   *  Not yet wired as a chat tool in agent.ts — a separate follow-up
   *  session's job, same as searchQuotes/listNodes/theme (out of this
   *  Track's hard gate). */
  path(slugA: string, slugB: string): PathResult;
  /** Union of participant role edges across a hub event's SUB_BEAT_OF
   *  children (query-layer step 6b). Dossier-side only by design — the
   *  design doc recommends no chat tool for this op (participants/beats can
   *  stay dossier-side; `path` is the one worth a tool per the evals). */
  participants(hubSlug: string): ParticipantsResult;
}

/** Bind GraphData into the read-only tools the Edge function exposes to Claude. */
export function createTools(data: GraphData): Tools {
  return {
    resolve: (phrase) => resolve(phrase, data),
    walkChain: (slug, opts) => walkChain(slug, data, opts),
    neighbors: (slug) => neighbors(slug, data),
    familyTree: (slug) => familyTree(slug, data),
    readNode: (slug) => readNode(slug, data),
    searchQuotes: (query, opts) => searchQuotes(query, data, opts),
    listNodes: (opts) => listNodes(data, opts),
    theme: (name, opts) => theme(name, data, opts),
    listThemes: () => listThemes(data),
    container: (name) => container(name, data),
    path: (slugA, slugB) => path(slugA, slugB, data),
    participants: (hubSlug) => participants(hubSlug, data),
  };
}
