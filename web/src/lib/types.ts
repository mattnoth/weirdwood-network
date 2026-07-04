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
  /** The graph/nodes/ type-directory name (e.g. "foods") — added query-layer
   *  step 5d for listNodes()'s `--type` filter. DIFFERENT from `type` (the
   *  dotted frontmatter scalar, e.g. "object.food"); see
   *  build_chat_bundle.py's load_nodes() docstring for why the two
   *  vocabularies aren't 1:1. Optional so pre-existing synthetic test
   *  fixtures (walkChain/neighbors specs that don't exercise listNodes)
   *  don't need updating; always present on real bundle data. */
  category?: string;
  identity: string;
  quotes: NodeQuote[];
  /** Chronological sort anchors (event nodes only; absent otherwise). Written by
   *  build-chat-export.py from the node's `sort_keys:` block. `composite` is the
   *  story-time key `{ac_year:04d}.{book_order}.{chapter:03d}` (present only when the
   *  event is dated); `reading_order` is the reading-order fallback `{book_order}.{chapter:03d}`.
   *  walkChain() orders a causal chain by these instead of graph hop-depth. */
  composite?: string;
  reading_order?: string;
  /** The `containers:` frontmatter array (query-layer step 6a) — the settled
   *  bag-retrieval tag set (e.g. "essos", "wo5k", "north", "aegon", "bran").
   *  Present only on the ~139 nodes that carry ≥1 container tag (added to
   *  `build_chat_bundle.py`'s `load_nodes()`, reusing
   *  `weirwood_query.traverse._node_containers`'s normalization verbatim, for
   *  parity with the full-profile `container` op). Absent everywhere else —
   *  does NOT bloat the other ~8,300 nodes with an empty `[]`. */
  containers?: string[];
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

/** One doc row in `search-index.json`'s compact `docs` array — see
 *  `graph/query/build/build_search_index.py`'s module docstring for the
 *  exact wire shape. `kindCode` 0 = "quote", 1 = "identity". `category` is
 *  the graph/nodes/ type-directory name (e.g. "foods") — the SAME vocabulary
 *  `search()`'s `type` filter/return field uses, distinct from `NodeRecord.type`
 *  (the dotted frontmatter scalar, e.g. "object.food"). */
export type SearchIndexDocRow = [
  slug: string,
  category: string,
  kindCode: number,
  qidx: number | null,
  cite: string | null,
];

/** `search-index.json` (compact format) — the build-time BM25-ish inverted
 *  index over node quotes + identity blurbs (query-layer step 5a). `postings`
 *  values are FLAT delta-encoded arrays: `[deltaDocId0, tf0, deltaDocId1,
 *  tf1, ...]` — decode by running-summing the deltas (see `search.ts`'s
 *  `decodePostings`). `idf` and `doc_lengths` are keyed/indexed by the same
 *  doc_id space as `docs`. */
export interface SearchIndex {
  format: "compact";
  n_docs: number;
  avgdl: number;
  min_token_len: number;
  docs: SearchIndexDocRow[];
  doc_lengths: number[];
  idf: Record<string, number>;
  postings: Record<string, number[]>;
}

/** One member row in a theme's list — see `ThemeIndex`'s comment. */
export interface ThemeMember {
  slug: string;
  category: string;
  name: string;
}

/** `theme-index.json` (bundle format) — the build-time theme->members
 *  routing table (query-layer step 8a). `matched_via` is dropped from the
 *  bundle copy (debugging-only field, see `build_theme_index.py`'s
 *  `format_bundle()`) — the full-profile copy at `working/wiki/data/
 *  theme-index.json` keeps it. */
export interface ThemeIndex {
  format: "bundle";
  themes: Record<string, { member_count: number; members: ThemeMember[] }>;
}

/** The whole in-memory bundle. The curated graph fits in memory — no lazy-loading. */
export interface GraphData {
  aliasMap: AliasMap;
  nodes: NodesMap;
  edges: Edge[];
  /** Optional so pre-existing synthetic test fixtures (walkChain/neighbors
   *  specs built by hand, not via loadGraphData()) don't need updating;
   *  always present on real bundle data. searchQuotes() requires it — a
   *  fixture with no searchIndex simply can't call that op. */
  searchIndex?: SearchIndex;
  /** Optional for the same reason as searchIndex — theme() requires it. */
  themeIndex?: ThemeIndex;
}

// ---- Tool return shapes (the receipts contract) ----

/**
 * One searchQuotes() hit — a ranked quote or identity blurb. `type` is the
 * node's category (graph/nodes/ type-directory name, e.g. "foods" — see
 * `SearchIndexDocRow`'s comment), NOT `NodeRecord.type`. `cite` is a
 * `chapter:line` string when the underlying quote carries one, else `null`
 * (identity-blurb hits never carry a cite — the dossier's `read_node(slug)`
 * is the provenance path for those). This is the EXACT export contract a
 * follow-up session wires into a chat tool — keep `{slug, type, text, cite,
 * score}` stable.
 */
export interface SearchResult {
  slug: string;
  type: string;
  text: string | null;
  cite: string | null;
  score: number;
}

/** A resolve() candidate: a node the phrase might name, with how it matched. */
export interface ResolveCandidate {
  slug: string;
  category: string;
  /** 1.0 for an exact alias-map hit; token-overlap score (≥ 0.5) for a fuzzy hit. */
  score: number;
  matchType: "exact" | "fuzzy";
  /** Node prominence = degree + 4·quoteCount (same proxy familyTree uses). Ties
   *  within a score are broken by this so a content-rich node outranks an empty
   *  bare-name stub (e.g. "aemon targaryen" → Maester Aemon, not the empty bucket). */
  prominence: number;
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

/** One SUB_BEAT_OF child of a chain node, with its participant role edges
 *  (query-layer step 6b — `expand-beats`). Ports
 *  `weirwood_query.traverse._beats_for_node()`. */
export interface ChainBeat {
  beat: string;
  /** [role_type, participant_slug] pairs, sorted (role_type, participant). */
  roles: Array<[string, string]>;
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
  /** Present only when `opts.expandBeats` was requested (query-layer step 6b).
   *  slug -> its SUB_BEAT_OF children + their role edges, for every node
   *  touched by the chain (queried node + upstream + downstream) that HAS
   *  beats — a chain node that reads sparse (a hub with no direct role
   *  edges) shows its real richness via its reified sub-beats. Ports the
   *  Python `--expand-beats` modifier's `beats` map verbatim. */
  beats?: Record<string, ChainBeat[]>;
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

/** One person in a familyTree() walk — a graph node OR a bare name a PARENT_OF/
 *  SPOUSE_OF edge references that has no node of its own. */
export interface FamilyMember {
  slug: string;
  /** Display name: the node's name, else a humanized slug fallback. */
  name: string;
  type?: string;
  /** Generation relative to the root: 0 = root, negative = ancestors above,
   *  positive = descendants below. */
  generation: number;
  /** True when a node record exists for this slug — the UI makes it clickable
   *  (opens the dossier); false renders as plain text. */
  hasNode: boolean;
  /** Total edges touching this node in the whole graph (how connected it is). */
  degree: number;
  /** Curated book quotes attached to this node (how much content it carries). */
  quoteCount: number;
  /** Composite importance = degree + 4·quoteCount. A proxy for story-weight: the
   *  characters who actually appear (Dany, Rhaegar, Aemon, Egg) score high,
   *  historical filler and bare-surname stubs score near zero. The render uses it
   *  to highlight the people worth clicking. */
  prominence: number;
}

/** A PARENT_OF bond kept in the tree (both endpoints are members). */
export interface FamilyBond {
  parent: string;
  child: string;
  ref: string | null;
  tier: number | null;
}

/** A SPOUSE_OF bond kept in the tree (both endpoints are members), deduped a<b. */
export interface SpouseBond {
  a: string;
  b: string;
  ref: string | null;
  tier: number | null;
}

/** familyTree() return: the lineage around a root, as a flat member set + the
 *  PARENT_OF / SPOUSE_OF bonds among those members. The panel lays it out as a
 *  tree; the model reads it as "X is parent of Y". A distinct shape from the
 *  causal spine (walkChain) — genealogy, not consequence. */
export interface FamilyTreeResult {
  root: string;
  rootName?: string;
  generationsUp: number;
  generationsDown: number;
  members: FamilyMember[];
  parentBonds: FamilyBond[];
  spouseBonds: SpouseBond[];
  memberCount: number;
  /** True when a size cap stopped the walk before it exhausted the lineage. */
  truncated: boolean;
}

/** One row in a listNodes() page. */
export interface ListItem {
  slug: string;
  name: string;
  quoteCount: number;
}

/** One direct edge between the two `path()` endpoints (either direction). */
export interface PathDirectEdge {
  edge_type: string;
  source: string;
  target: string;
  evidence_quote: string | null;
  ref: string | null;
  tier: number | null;
}

/** One 2-hop bridge node in a `path()` result: a node that neighbors BOTH
 *  endpoints. `aDir`/`bDir` are "out" | "in" | "both" — the dominant
 *  direction of the edges on that leg (relative to the endpoint). */
export interface PathBridge {
  bridge: string;
  aTypes: string[];
  bTypes: string[];
  aDir: "out" | "in" | "both";
  bDir: "out" | "in" | "both";
  aEdgeCount: number;
  bEdgeCount: number;
}

/** path(a, b) return: direct edges between A and B, plus 2-hop bridges
 *  (nodes that neighbor both), ranked by combined edge count and capped
 *  (query-layer step 6b). Ports `weirwood_query.traverse.path()`. */
export interface PathResult {
  slugA: string;
  slugB: string;
  directEdges: PathDirectEdge[];
  totalBridges: number;
  bridgesShown: number;
  bridges: PathBridge[];
}

/** One participant role edge in an `participants()` result — a SUB_BEAT_OF
 *  child's role edge, presented as if directly attached to the hub. */
export interface ParticipantRecord {
  roleType: string;
  sourceSlug: string;
  beatSlug: string;
  evidenceQuote: string | null;
  tier: number | null;
}

/** participants(hub) return: the union of participant role edges across
 *  every SUB_BEAT_OF child of `hub` (query-layer step 6b). Ports
 *  `weirwood_query.traverse.event_participants()`. `error` is set (with no
 *  `beats`/`participants`) when the hub slug has no node record. */
export interface ParticipantsResult {
  hubSlug: string;
  beatCount: number;
  beats?: string[];
  participantCount: number;
  participants: ParticipantRecord[];
  error?: string;
  message?: string;
}

/** One node in a container() bag-retrieval result. */
export interface ContainerItem {
  slug: string;
  type: string;
  name: string;
  /** The node's full `containers:` array (a node can carry more than one tag —
   *  e.g. a node in both "wo5k" and "essos"), not just the queried name. */
  containers: string[];
}

/** container(name) return: every node whose `containers:` frontmatter array
 *  includes `name` (query-layer step 6a) — UNORDERED bag-retrieval, distinct
 *  from the ordered causal walk (`chain`/`walkChain`). Ports
 *  `weirwood_query.traverse.container()`'s semantics against the bounded
 *  bundle's `NodeRecord.containers` field. */
export interface ContainerResult {
  container: string;
  count: number;
  nodes: ContainerItem[];
}

/** listNodes() return: a browse page over one node category (query-layer
 *  step 5d). `total` counts every filter-matching node BEFORE paging, so
 *  `total - offset - items.length` tells the caller how many more remain. */
export interface ListResult {
  category: string;
  total: number;
  offset: number;
  limit: number;
  items: ListItem[];
}

/** theme() return: one theme's member list (query-layer step 8a). An unknown
 *  theme name returns `member_count: 0, members: [], error: "unknown theme",
 *  knownThemes: [...]` rather than throwing — mirrors listNodes()'s
 *  "unknown category -> empty result" convention, but also surfaces the
 *  known-theme list since a typo has no other discovery path here. */
export interface ThemeResult {
  theme: string;
  memberCount: number;
  members: ThemeMember[];
  error?: string;
  knownThemes?: string[];
}

/** One row in listThemes()'s discovery listing. */
export interface ThemeSummary {
  name: string;
  memberCount: number;
}
