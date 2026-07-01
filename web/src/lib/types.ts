// Shared types for the retrieval-core tools.
//
// These mirror the build-time bundle shapes in `web/data/` (documented in
// `web/README.md`) and the structured returns the tools hand back to the Edge
// function. The receipts panel renders from these returns, NOT from parsing the
// model's prose (design §3) — so the typed-edge fields here are the contract.

// ---- Bundle shapes (as written by scripts/build-chat-export.py) ----

/** One entry in `alias-map.json`: a normalized phrase maps to ≥1 candidate node. */
export interface AliasCandidate {
  slug: string;
  category: string;
}

/** `alias-map.json` — `{ "<normalized phrase>": [{slug, category}, …] }`. */
export type AliasMap = Record<string, AliasCandidate[]>;

/** One quote attached to a node in `nodes.json`. */
export interface NodeQuote {
  text: string;
  attribution: string;
  cite: string;
}

/** One node record in `nodes.json` (keyed by slug). */
export interface NodeRecord {
  name: string;
  type: string;
  identity: string;
  quotes: NodeQuote[];
}

/** `nodes.json` — `{ "<slug>": NodeRecord }`. */
export type NodesMap = Record<string, NodeRecord>;

/** One edge in `edges.json` (short wire keys; see slim_edge in the build script). */
export interface Edge {
  type: string;
  source: string;
  target: string;
  quote: string | null;
  ref: string | null;
  tier: number | null;
  relation: string | null;
}

/** The whole in-memory bundle. The curated graph fits in memory — no lazy-loading. */
export interface GraphData {
  aliasMap: AliasMap;
  nodes: NodesMap;
  edges: Edge[];
}

// ---- Tool return shapes (the receipts contract) ----

/** A resolve() candidate: a node the phrase might name, with how it matched. */
export interface ResolveCandidate {
  slug: string;
  category: string;
  /** 1.0 for an exact alias-map hit; token-overlap score (≥ 0.5) for a fuzzy hit. */
  score: number;
  matchType: "exact" | "fuzzy";
}

/**
 * One typed-edge link in a walked chain. This is the receipts unit — the panel
 * renders {source, edge_type, target, evidence_quote, ref} directly.
 */
export interface ChainLink {
  source: string;
  edge_type: string;
  target: string;
  /** Display names + types looked up from the nodes map (slug → record). The
   *  receipts panel renders these so live chains read "Red Wedding", not the raw
   *  slug "red-wedding". Absent only when the slug has no node record. */
  source_name?: string;
  target_name?: string;
  source_type?: string;
  target_type?: string;
  evidence_quote: string | null;
  ref: string | null;
  tier: number | null;
  /** BFS distance from the queried node (1 = adjacent). */
  depth: number;
}

/** walkChain() return: causal antecedents (upstream) + consequences (downstream) + preconditions. */
export interface ChainResult {
  slug: string;
  upstream: ChainLink[];
  downstream: ChainLink[];
  /** ENABLES edges that precondition nodes in the causal spine. Returned with the
   *  spine (one round-trip) so the UI can reveal the preconditions behind a toggle
   *  while the model narrates only the clean causal spine. */
  enables: ChainLink[];
}

/** One edge in the neighbors() relational view (no chain walk). */
export interface NeighborLink {
  source: string;
  edge_type: string;
  target: string;
  source_name?: string;
  target_name?: string;
  source_type?: string;
  target_type?: string;
  evidence_quote: string | null;
  ref: string | null;
  tier: number | null;
}

/** neighbors() return: edges touching a node, split by direction, grouped by type. */
export interface NeighborsResult {
  slug: string;
  outgoingCount: number;
  incomingCount: number;
  /** edge_type -> links where slug is the source. */
  outgoing: Record<string, NeighborLink[]>;
  /** edge_type -> links where slug is the target. */
  incoming: Record<string, NeighborLink[]>;
}
