// path(a, b) — direct edges between two nodes, plus 2-hop bridges (query-layer
// Track, step 6b).
//
// Ports `graph/query/weirwood_query/traverse.py::path()` (absorbed from
// scripts/graph-query.py::cmd_path) against the bundle's `edges.json` (short
// keys: {type, source, target, quote, ref, tier, relation}). Answers "how are
// X and Y connected" — a real archetype query the design doc names as worth a
// chat tool (step 5's routing decision), distinct from the causal spine
// (`chain`/`walkChain`): `path` finds ANY shared neighbor, not just
// cause/effect links.
//
// No LLM in the loop, ever — pure data.

import type { Edge, GraphData, PathBridge, PathDirectEdge, PathResult } from "./types.ts";
import { isValidSlug } from "./validate.ts";

const BRIDGE_CAP = 50;

function toDirectEdge(e: Edge): PathDirectEdge {
  return {
    edge_type: e.type,
    source: e.source,
    target: e.target,
    evidence_quote: e.quote ?? null,
    ref: e.ref ?? null,
    tier: e.tier ?? null,
  };
}

/** Dominant direction of a leg's edges relative to `pivot`: "out" (pivot is
 *  always source), "in" (pivot is always target), or "both". */
function legDirection(pivot: string, legEdges: Edge[]): "out" | "in" | "both" {
  let out = 0, inn = 0;
  for (const e of legEdges) {
    if (e.source === pivot) out++;
    if (e.target === pivot) inn++;
  }
  if (out > 0 && inn > 0) return "both";
  return out > 0 ? "out" : "in";
}

/**
 * Direct edges between `slugA` and `slugB` (either direction), plus 2-hop
 * bridges: nodes that are neighbors of BOTH endpoints (excluding the
 * endpoints themselves), ranked by combined edge count on both legs and
 * capped at `BRIDGE_CAP` (50, matching the Python full-profile CLI). Each
 * bridge reports the edge types and dominant direction on each leg. Invalid
 * slugs yield an empty-shaped result (trust boundary, validate.ts) — no throw.
 */
export function path(slugA: string, slugB: string, data: GraphData): PathResult {
  const empty: PathResult = {
    slugA: String(slugA),
    slugB: String(slugB),
    directEdges: [],
    totalBridges: 0,
    bridgesShown: 0,
    bridges: [],
  };
  if (!isValidSlug(slugA) || !isValidSlug(slugB)) return empty;

  const direct: Edge[] = data.edges.filter((e) =>
    (e.source === slugA && e.target === slugB) || (e.source === slugB && e.target === slugA)
  );

  const neighborsA = new Map<string, Edge[]>();
  const neighborsB = new Map<string, Edge[]>();
  for (const e of data.edges) {
    if (e.source === slugA) {
      (neighborsA.get(e.target) ?? neighborsA.set(e.target, []).get(e.target)!).push(e);
    } else if (e.target === slugA) {
      (neighborsA.get(e.source) ?? neighborsA.set(e.source, []).get(e.source)!).push(e);
    }
    if (e.source === slugB) {
      (neighborsB.get(e.target) ?? neighborsB.set(e.target, []).get(e.target)!).push(e);
    } else if (e.target === slugB) {
      (neighborsB.get(e.source) ?? neighborsB.set(e.source, []).get(e.source)!).push(e);
    }
  }

  const bridgeSlugs = [...neighborsA.keys()].filter(
    (s) => neighborsB.has(s) && s !== slugA && s !== slugB,
  );
  const totalBridges = bridgeSlugs.length;

  const bridges: PathBridge[] = bridgeSlugs
    .sort()
    .map((bridge) => {
      const legA = neighborsA.get(bridge)!;
      const legB = neighborsB.get(bridge)!;
      const aTypes = [...new Set(legA.map((e) => e.type))].sort();
      const bTypes = [...new Set(legB.map((e) => e.type))].sort();
      return {
        bridge,
        aTypes,
        bTypes,
        aDir: legDirection(slugA, legA),
        bDir: legDirection(slugB, legB),
        aEdgeCount: legA.length,
        bEdgeCount: legB.length,
      };
    })
    .sort((x, y) => (y.aEdgeCount + y.bEdgeCount) - (x.aEdgeCount + x.bEdgeCount));

  const displayedBridges = bridges.slice(0, BRIDGE_CAP);

  return {
    slugA,
    slugB,
    directEdges: direct.map(toDirectEdge),
    totalBridges,
    bridgesShown: displayedBridges.length,
    bridges: displayedBridges,
  };
}
