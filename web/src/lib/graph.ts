// walkChain(slug) + neighbors(slug) — the typed-edge graph queries.
//
// Ports scripts/graph-query.py: --causal-chain (walkChain) and --neighbors.
// Both read the bundle edges.json (short keys: {type, source, target, quote,
// ref, tier, relation}) and emit receipts-shaped links the panel renders
// directly. Invalid slugs yield empty results (trust boundary, validate.ts).

import type {
  ChainBeat,
  ChainLink,
  ChainResult,
  Edge,
  FamilyBond,
  FamilyMember,
  FamilyTreeResult,
  GraphData,
  NeighborLink,
  NeighborsResult,
  NodesMap,
  SpouseBond,
} from "./types.ts";
import { isValidSlug } from "./validate.ts";

// Edge types that carry causal consequence (vs PRECEDES = pure chronology).
// Walking all three reconstructs a narrative-arc chain no single edge holds.
const CAUSAL_EDGE_TYPES: ReadonlySet<string> = new Set(["CAUSES", "TRIGGERS", "MOTIVATES"]);

// Role edges surfaced by expand-beats (query-layer step 6b) — ports
// `weirwood_query.traverse.ROLE_EDGE_TYPES` VERBATIM. Deliberately a
// DIFFERENT set from `participants()`'s PARTICIPANT_ROLE_TYPES (that one
// additionally has ATTENDS/LOCATED_AT but omits WITNESS_IN) — the two ops
// were ported from two distinct constants in the Python source and must stay
// that way, not unified, to match traverse.py exactly.
const BEAT_ROLE_EDGE_TYPES: ReadonlySet<string> = new Set([
  "AGENT_IN",
  "VICTIM_IN",
  "COMMANDS_IN",
  "WITNESS_IN",
  "WIELDED_IN",
]);
// ENABLES is a precondition, not a consequence. It is NEVER walked into the
// causal spine (it would flood a hub with tangents). Instead walkChain returns
// the ENABLES edges that precondition spine nodes as a SEPARATE `enables` array,
// so the UI can reveal the precondition web behind a "show preconditions" toggle
// without a second model round-trip, and the model still narrates the clean spine.

// The displayed "chain walked" is a tight, readable spine, NOT the whole causal
// component. An uncapped transitive walk over a hub like the Red Wedding returns
// 50+ edges with repeated nodes and unrelated tangents — a graph dump, not a
// chain. These bounds keep it to the spine the prose actually narrates.
const DEFAULT_MAX_DEPTH = 2; // hops from the queried node, each direction
const MAX_LINKS_PER_DIRECTION = 12; // hard cap so a dense hub can't explode the panel
const MAX_ENABLES = 24; // cap the precondition web behind the toggle (measured ≤8 in practice)

// ---- Chronological ordering of a causal chain (S185) ----
//
// A causal chain must READ in story-time order (AGOT → ADWD), not graph hop-depth.
// Each event node carries a `composite` sort key `{ac_year:04d}.{book}.{chapter:03d}`
// (dated events) and/or a `reading_order` fallback `{book}.{chapter:03d}` (undated).
// These two formats are NOT lexically comparable ("0298.1.018" vs "1.015"), so we
// normalize BOTH into the composite space before comparing: an undated event's
// reading_order gets a synthesized year from its book, so it interleaves with dated
// events at roughly the right point (an undated ADWD event still sorts after a dated
// AGOT one). A node with neither key sorts last (stably).
const BOOK_YEAR: Readonly<Record<string, string>> = {
  // Approx AC year each book opens in — only used to place UNDATED events relative
  // to dated ones; within a book the year is constant so it never affects order.
  "1": "0298", // AGOT
  "2": "0299", // ACOK
  "3": "0299", // ASOS
  "4": "0300", // AFFC
  "5": "0300", // ADWD
};
const NO_KEY = "￿"; // sorts after every real key

/** A single lexically-comparable story-time key for a node: its `composite` if it
 *  has one, else a composite synthesized from `reading_order` (book → AC-year),
 *  else NO_KEY (sorts last). */
function chronoKey(slug: string, nodes: NodesMap): string {
  const rec = nodes[slug];
  if (!rec) return NO_KEY;
  if (rec.composite) return rec.composite;
  const ro = rec.reading_order;
  if (ro) {
    const book = ro.split(".")[0];
    return `${BOOK_YEAR[book] ?? "9999"}.${ro}`;
  }
  return NO_KEY;
}

/** A link's story-time sort key: the SOURCE node's chronology, then the TARGET's
 *  (ties on the cause break by the effect). One correction for UNDATED nodes: a
 *  cause is never later than its effect, so an undated source borrows its (dated)
 *  target's key as its proxy. Without this, an undated chain ROOT (e.g. the broad
 *  `roberts-rebellion` event, which carries no date) sends its own outgoing link to
 *  NO_KEY — sinking it BELOW deeper dated links and printing an effect above its
 *  cause. Fully-dated links are unaffected (effS === source key). */
function linkSortKey(link: ChainLink, nodes: NodesMap): string {
  const s = chronoKey(link.source, nodes);
  const t = chronoKey(link.target, nodes);
  const effS = s !== NO_KEY ? s : t; // undated cause ≤ its effect → use the effect's key
  return effS + "|" + t;
}

/** Sort chain links into story-time reading order (see `linkSortKey`). Stable, so
 *  links that share a key keep their BFS order; links with no datable endpoint sink
 *  to the end. */
function sortChainLinks(links: ChainLink[], nodes: NodesMap): ChainLink[] {
  return links
    .map((l, i) => ({ l, i, k: linkSortKey(l, nodes) }))
    .sort((a, b) => (a.k < b.k ? -1 : a.k > b.k ? 1 : a.i - b.i))
    .map((x) => x.l);
}

/** Look up a slug's display name + type from the nodes map (undefined if no record). */
function nameOf(slug: string, nodes: NodesMap): string | undefined {
  return nodes[slug]?.name;
}
function typeOf(slug: string, nodes: NodesMap): string | undefined {
  return nodes[slug]?.type;
}

function toChainLink(e: Edge, depth: number, nodes: NodesMap): ChainLink {
  return {
    source: e.source,
    edge_type: e.type,
    target: e.target,
    source_name: nameOf(e.source, nodes),
    target_name: nameOf(e.target, nodes),
    source_type: typeOf(e.source, nodes),
    target_type: typeOf(e.target, nodes),
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
  nodes: NodesMap,
  maxDepth: number,
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
    if (depth >= maxDepth) continue; // bound the spine — do not expand past maxDepth
    for (const e of adj.get(node) ?? []) {
      if (result.length >= MAX_LINKS_PER_DIRECTION) return result;
      result.push(toChainLink(e, depth + 1, nodes));
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
 * The SUB_BEAT_OF children of `node` (a hub event), each annotated with its
 * role edges (query-layer step 6b, "expand-beats"). Ports
 * `weirwood_query.traverse._beats_for_node()` verbatim: children sorted by
 * slug, each child's roles sorted as (role_type, participant) pairs.
 */
function beatsForNode(node: string, edges: Edge[]): ChainBeat[] {
  const children = edges
    .filter((e) => e.type === "SUB_BEAT_OF" && e.target === node)
    .map((e) => e.source)
    .sort();
  return children.map((child) => {
    const roles: Array<[string, string]> = edges
      .filter((e) => e.target === child && BEAT_ROLE_EDGE_TYPES.has(e.type))
      .map((e): [string, string] => [e.type, e.source])
      .sort((a, b) => (a[0] === b[0] ? (a[1] < b[1] ? -1 : a[1] > b[1] ? 1 : 0) : (a[0] < b[0] ? -1 : 1)));
    return { beat: child, roles };
  });
}

/**
 * Walk the causal chain both directions from `slug`: upstream antecedents and
 * downstream consequences. Also collects ENABLES edges that precondition nodes
 * in the causal chain (for progressive-disclosure toggle). When
 * `opts.expandBeats` is set (query-layer step 6b), also attaches, for every
 * node touched by the chain (queried node + upstream + downstream) that has
 * SUB_BEAT_OF children, its beats + role edges — ports the Python
 * `--expand-beats` modifier verbatim. Empty result for an invalid slug.
 */
export function walkChain(
  slug: string,
  data: GraphData,
  opts: { maxDepth?: number; expandBeats?: boolean } = {},
): ChainResult {
  const maxDepth = opts.maxDepth ?? DEFAULT_MAX_DEPTH;
  if (!isValidSlug(slug)) {
    return { slug: String(slug), upstream: [], downstream: [], enables: [] };
  }

  // Walk the causal spine (CAUSES/TRIGGERS/MOTIVATES only), then order each
  // direction by story-time (S185) so the chain reads AGOT → ADWD, not by graph
  // hop-depth. upstream and downstream stay SEPARATE lists — the UI renders "what
  // led to" and "what followed" apart, so a downstream consequence can never
  // surface inside the causes.
  const upstream = sortChainLinks(
    walkCausal(slug, data.edges, "up", CAUSAL_EDGE_TYPES, data.nodes, maxDepth),
    data.nodes,
  );
  const downstream = sortChainLinks(
    walkCausal(slug, data.edges, "down", CAUSAL_EDGE_TYPES, data.nodes, maxDepth),
    data.nodes,
  );

  // Every node the causal spine touches (the queried node + both directions).
  const spineNodes = new Set<string>([slug]);
  for (const link of [...upstream, ...downstream]) {
    spineNodes.add(link.source);
    spineNodes.add(link.target);
  }

  // The precondition web: ENABLES edges whose TARGET is a spine node (something
  // that had to be true for a spine node to occur). Returned separately so the UI
  // can reveal it behind a toggle; deduped by source->target, capped so a dense
  // hub cannot flood the panel.
  const enables: ChainLink[] = [];
  const seen = new Set<string>();
  for (const edge of data.edges) {
    if (edge.type !== "ENABLES") continue;
    if (!spineNodes.has(edge.target)) continue;
    const key = `${edge.source} ${edge.target}`;
    if (seen.has(key)) continue;
    seen.add(key);
    enables.push(toChainLink(edge, 1, data.nodes));
    if (enables.length >= MAX_ENABLES) break;
  }

  const result: ChainResult = { slug, upstream, downstream, enables };

  if (opts.expandBeats) {
    // Edge-discovery order (matches traverse.py's `chain_nodes`, NOT a sorted
    // set) — root first, then each upstream+downstream link's endpoints in
    // walk order, first-seen-wins.
    const orderedNodes: string[] = [slug];
    const seenNodes = new Set<string>([slug]);
    for (const link of [...upstream, ...downstream]) {
      for (const n of [link.source, link.target]) {
        if (!seenNodes.has(n)) {
          seenNodes.add(n);
          orderedNodes.push(n);
        }
      }
    }
    const beats: Record<string, ChainBeat[]> = {};
    for (const n of orderedNodes) {
      const b = beatsForNode(n, data.edges);
      if (b.length > 0) beats[n] = b;
    }
    result.beats = beats;
  }

  return result;
}

function toNeighborLink(e: Edge, nodes: NodesMap): NeighborLink {
  return {
    source: e.source,
    edge_type: e.type,
    target: e.target,
    source_name: nameOf(e.source, nodes),
    target_name: nameOf(e.target, nodes),
    source_type: typeOf(e.source, nodes),
    target_type: typeOf(e.target, nodes),
    evidence_quote: e.quote ?? null,
    ref: e.ref ?? null,
    tier: e.tier ?? null,
  };
}

function groupByType(edges: Edge[], nodes: NodesMap): Record<string, NeighborLink[]> {
  const out: Record<string, NeighborLink[]> = {};
  // Dedup identical type|source|target edges: the same neighbour listed twice
  // under one relationship (e.g. two WARGS_INTO → Ghost) is display noise, not a
  // second connection. Keep the first occurrence.
  const seen = new Set<string>();
  for (const e of edges) {
    const key = `${e.type}|${e.source}|${e.target}`;
    if (seen.has(key)) continue;
    seen.add(key);
    (out[e.type] ??= []).push(toNeighborLink(e, nodes));
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
  // Group + dedup, then count from the deduped groups so the count reflects what
  // the panel actually shows (a duped neighbour is not a second connection).
  const outgoingGroups = groupByType(outgoing, data.nodes);
  const incomingGroups = groupByType(incoming, data.nodes);
  const countLinks = (g: Record<string, NeighborLink[]>) =>
    Object.values(g).reduce((a, b) => a + b.length, 0);
  return {
    slug,
    outgoingCount: countLinks(outgoingGroups),
    incomingCount: countLinks(incomingGroups),
    outgoing: outgoingGroups,
    incoming: incomingGroups,
  };
}

// ---- familyTree(slug): the lineage/genealogy walk ----
//
// A dynasty/lineage question ("the Targaryen family tree from Aegon") is a
// DISTINCT shape from the causal spine: it walks parentage, not consequence.
// Answering it with generic neighbors() fan-out floods the model with titles /
// succession / birthplace edges and blows the tool-iteration bound before any
// lineage is assembled (the loop-bound-hit case). familyTree walks PARENT_OF
// (source = parent, target = child) both directions in ONE call and attaches
// spouses, so it is always a single tool round-trip.

const GENEALOGY_DOWN_DEFAULT = 4; // full-breadth descendant generations below the root
const GENEALOGY_UP_DEFAULT = 2; // ancestor generations above the root
// Hard cap so a sprawling dynasty cannot flood the panel. Holds the near-root
// breadth set (BFS closest-first) PLUS a threaded deep main-line spine (below);
// sized so both fit for the deepest real dynasty (Aegon I → the book era).
const MAX_FAMILY_MEMBERS = 96;

// Deep main-line spine. The breadth BFS above stops at generationsDown, and a
// depth bound alone never reaches the book era — Aegon I → Daenerys is 12 hops,
// and walking every generation at full breadth explodes. So beyond the breadth
// horizon we thread ONLY the PARENT_OF paths to the most story-weighty deep
// descendants: a narrow "main line" that follows succession + cadet splits (the
// Blackfyre line, etc.) down to the book generation, dropping obscure extended
// kin. Prominence = degree + 4·quoteCount, the same proxy the render highlights.
const DEEP_SPINE_MAX_DEPTH = 14; // the book era sits ~12–13 generations below Aegon I
const DEEP_SPINE_ANCHORS = 24; // # of most-prominent deep descendants to thread paths to

/** "aerion-targaryen-son-of-daemion" → "Aerion Targaryen Son Of Daemion" — a
 *  readable fallback when a PARENT_OF/SPOUSE_OF edge names a slug with no node. */
function humanizeSlug(slug: string): string {
  return slug
    .split("-")
    .map((w) => (w.length > 0 ? w[0].toUpperCase() + w.slice(1) : w))
    .join(" ");
}

/**
 * Walk the lineage around `slug`: descendants (down, via PARENT_OF source→target)
 * and ancestors (up), with spouses attached at each member's generation. Returns
 * a flat member set + the PARENT_OF / SPOUSE_OF bonds among those members — the
 * panel lays it out as a tree, the model reads it as parentage. BFS is
 * closest-first and capped at MAX_FAMILY_MEMBERS (sets `truncated`). Empty result
 * for an invalid slug.
 */
export function familyTree(
  slug: string,
  data: GraphData,
  opts: { generationsUp?: number; generationsDown?: number } = {},
): FamilyTreeResult {
  const generationsUp = opts.generationsUp ?? GENEALOGY_UP_DEFAULT;
  const generationsDown = opts.generationsDown ?? GENEALOGY_DOWN_DEFAULT;
  const empty: FamilyTreeResult = {
    root: String(slug),
    generationsUp,
    generationsDown,
    members: [],
    parentBonds: [],
    spouseBonds: [],
    memberCount: 0,
    truncated: false,
  };
  if (!isValidSlug(slug)) return empty;

  // Adjacency over PARENT_OF (child edges keyed by parent, parent edges by child)
  // and SPOUSE_OF (symmetric); plus a whole-graph degree count (prominence proxy).
  // Build once.
  const childrenOf = new Map<string, Edge[]>(); // parent slug -> PARENT_OF edges
  const parentsOf = new Map<string, Edge[]>(); // child slug  -> PARENT_OF edges
  const spousesOf = new Map<string, Edge[]>(); // slug        -> SPOUSE_OF edges
  const degree = new Map<string, number>(); // slug -> total edges touching it
  for (const e of data.edges) {
    degree.set(e.source, (degree.get(e.source) ?? 0) + 1);
    degree.set(e.target, (degree.get(e.target) ?? 0) + 1);
    if (e.type === "PARENT_OF") {
      (childrenOf.get(e.source) ?? childrenOf.set(e.source, []).get(e.source)!).push(e);
      (parentsOf.get(e.target) ?? parentsOf.set(e.target, []).get(e.target)!).push(e);
    } else if (e.type === "SPOUSE_OF") {
      (spousesOf.get(e.source) ?? spousesOf.set(e.source, []).get(e.source)!).push(e);
      (spousesOf.get(e.target) ?? spousesOf.set(e.target, []).get(e.target)!).push(e);
    }
  }

  // generation[slug]: 0 = root, +down = descendants, -up = ancestors. First
  // assignment wins (BFS closest-first), so a member reached both ways keeps the
  // shorter hop. A cap stops the walk; `truncated` records that it was clipped.
  const generation = new Map<string, number>([[slug, 0]]);
  let truncated = false;
  const capReached = () => generation.size >= MAX_FAMILY_MEMBERS;

  // BFS descendants (down): follow PARENT_OF from parent to child.
  const down: Array<[string, number]> = [[slug, 0]];
  while (down.length > 0) {
    const [node, gen] = down.shift()!;
    if (gen >= generationsDown) continue;
    for (const e of childrenOf.get(node) ?? []) {
      if (generation.has(e.target)) continue;
      if (capReached()) {
        truncated = true;
        break;
      }
      generation.set(e.target, gen + 1);
      down.push([e.target, gen + 1]);
    }
  }

  // BFS ancestors (up): follow PARENT_OF from child to parent.
  const up: Array<[string, number]> = [[slug, 0]];
  while (up.length > 0) {
    const [node, gen] = up.shift()!;
    if (-gen >= generationsUp) continue;
    for (const e of parentsOf.get(node) ?? []) {
      if (generation.has(e.source)) continue;
      if (capReached()) {
        truncated = true;
        break;
      }
      generation.set(e.source, gen - 1);
      up.push([e.source, gen - 1]);
    }
  }

  // Thread the deep main-line spine: reach the book-era descendants the breadth
  // BFS can't (it stops at generationsDown). Additive — only ADDS the paths to the
  // most prominent deep kin, never drops a breadth member already collected. Gated
  // to the full/deep view: a caller asking for a tight window (generationsDown below
  // the default, e.g. a local 1-gen view) gets exactly that window, no deep threads.
  if (generationsDown >= GENEALOGY_DOWN_DEFAULT && !capReached()) {
    // Shortest-path tree over ALL descendants (bounded depth), for path threading.
    const descDepth = new Map<string, number>([[slug, 0]]);
    const descParent = new Map<string, string>(); // child -> its shortest-path parent
    const dq: Array<[string, number]> = [[slug, 0]];
    while (dq.length > 0) {
      const [node, d] = dq.shift()!;
      if (d >= DEEP_SPINE_MAX_DEPTH) continue;
      for (const e of childrenOf.get(node) ?? []) {
        if (descDepth.has(e.target)) continue;
        descDepth.set(e.target, d + 1);
        descParent.set(e.target, node);
        dq.push([e.target, d + 1]);
      }
    }
    // Anchors = the most prominent descendants BEYOND the breadth horizon; thread
    // each one's path back toward the root until it joins an already-included node.
    const promOf = (s: string) => (degree.get(s) ?? 0) + 4 * (data.nodes[s]?.quotes?.length ?? 0);
    const deepAnchors = [...descDepth.keys()]
      .filter((s) => descDepth.get(s)! > generationsDown && !generation.has(s))
      .sort((a, b) => promOf(b) - promOf(a))
      .slice(0, DEEP_SPINE_ANCHORS);
    for (const anchor of deepAnchors) {
      const path: string[] = []; // anchor → … up to the first already-included node
      let n: string | undefined = anchor;
      while (n && !generation.has(n)) {
        path.push(n);
        n = descParent.get(n);
      }
      // Add top-down so a partially-added path keeps parents before children.
      let hitCap = false;
      for (const s of path.reverse()) {
        if (generation.has(s)) continue;
        if (capReached()) {
          truncated = true;
          hitCap = true;
          break;
        }
        generation.set(s, descDepth.get(s)!);
      }
      if (hitCap) break;
    }
  }

  // Attach spouses at the same generation as their partner (snapshot the member
  // set first so a spouse's spouse doesn't cascade). Co-parent PARENT_OF bonds
  // are picked up below since both endpoints are now members.
  for (const member of [...generation.keys()]) {
    for (const e of spousesOf.get(member) ?? []) {
      const spouse = e.source === member ? e.target : e.source;
      if (generation.has(spouse)) continue;
      if (capReached()) {
        truncated = true;
        break;
      }
      generation.set(spouse, generation.get(member)!);
    }
  }

  // Collect the bonds whose BOTH endpoints are members.
  const parentBonds: FamilyBond[] = [];
  const spouseSeen = new Set<string>();
  const spouseBonds: SpouseBond[] = [];
  for (const e of data.edges) {
    if (e.type === "PARENT_OF") {
      if (generation.has(e.source) && generation.has(e.target)) {
        parentBonds.push({
          parent: e.source,
          child: e.target,
          ref: e.ref ?? null,
          tier: e.tier ?? null,
        });
      }
    } else if (e.type === "SPOUSE_OF") {
      if (!generation.has(e.source) || !generation.has(e.target)) continue;
      const [a, b] = e.source < e.target ? [e.source, e.target] : [e.target, e.source];
      const key = `${a} ${b}`;
      if (spouseSeen.has(key)) continue;
      spouseSeen.add(key);
      spouseBonds.push({ a, b, ref: e.ref ?? null, tier: e.tier ?? null });
    }
  }

  // Member records: sort by generation (ancestors first, then root, then down).
  // Each carries a prominence proxy (degree + 4·quoteCount) so the render can
  // highlight the story-weighty people among the historical filler.
  const members: FamilyMember[] = [...generation.entries()]
    .sort((x, y) => x[1] - y[1])
    .map(([s, gen]) => {
      const rec = data.nodes[s];
      const quoteCount = rec?.quotes?.length ?? 0;
      const deg = degree.get(s) ?? 0;
      return {
        slug: s,
        name: rec?.name ?? humanizeSlug(s),
        type: rec?.type,
        generation: gen,
        hasNode: rec !== undefined,
        degree: deg,
        quoteCount,
        prominence: deg + 4 * quoteCount,
      };
    });

  return {
    root: slug,
    rootName: data.nodes[slug]?.name,
    generationsUp,
    generationsDown,
    members,
    parentBonds,
    spouseBonds,
    memberCount: members.length,
    truncated,
  };
}
