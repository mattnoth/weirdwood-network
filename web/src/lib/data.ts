// Bundle loader. The three static JSON files in web/data/ are compiled INTO the
// edge-function bundle at build time via JSON module imports — Netlify Edge
// Functions run on Deno with NO filesystem access (Deno.readTextFile throws
// "Reading or writing files with Edge Functions is not supported yet"), so the
// ~8.7 MB curated graph must be inlined, not read from disk at runtime. The
// python build (scripts/build-chat-export.py) regenerates these files before
// every bundle; a fresh checkout must run it once before `deno test`/`deno check`.
// (S183 — was Deno.readTextFile; that 502'd every edge request.)

import type { AliasMap, Edge, GraphData, NodesMap, SearchIndex, ThemeIndex } from "./types.ts";

// deno-lint-ignore no-import-assertions
import aliasMap from "../../data/alias-map.json" with { type: "json" };
import nodes from "../../data/nodes.json" with { type: "json" };
import edges from "../../data/edges.json" with { type: "json" };
import searchIndex from "../../data/search-index.json" with { type: "json" };
import themeIndex from "../../data/theme-index.json" with { type: "json" };

/**
 * Return the inlined curated graph as one GraphData. Kept async so cold-start
 * call sites (`await loadGraphData()`) are unchanged; the data is already in
 * memory once the module is imported (no I/O, no network — filesystem-free).
 * Cast through `unknown` so tsc skips a deep structural check of the big literals.
 */
// deno-lint-ignore require-await
export async function loadGraphData(): Promise<GraphData> {
  return {
    aliasMap: aliasMap as unknown as AliasMap,
    nodes: nodes as unknown as NodesMap,
    edges: edges as unknown as Edge[],
    searchIndex: searchIndex as unknown as SearchIndex,
    themeIndex: themeIndex as unknown as ThemeIndex,
  };
}
