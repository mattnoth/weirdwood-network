// Bundle loader. Reads the static JSON in web/data/ into one in-memory GraphData.
// The Edge function calls this once at cold start; the whole curated graph fits
// in memory (~8.8 MB), so there is no lazy-loading and no per-call disk read.

import type { AliasMap, Edge, GraphData, NodesMap } from "./types.ts";

/** Default bundle location: web/data/, relative to this module (web/src/lib/). */
export const DEFAULT_DATA_DIR = new URL("../../data/", import.meta.url);

async function readJson<T>(name: string, base: URL): Promise<T> {
  const url = new URL(name, base);
  return JSON.parse(await Deno.readTextFile(url)) as T;
}

/**
 * Load alias-map.json, nodes.json and edges.json into a single GraphData.
 * Pass `dataDir` (a directory URL, must end in `/`) to read from elsewhere;
 * defaults to the co-located web/data/ bundle.
 */
export async function loadGraphData(dataDir: URL = DEFAULT_DATA_DIR): Promise<GraphData> {
  const [aliasMap, nodes, edges] = await Promise.all([
    readJson<AliasMap>("alias-map.json", dataDir),
    readJson<NodesMap>("nodes.json", dataDir),
    readJson<Edge[]>("edges.json", dataDir),
  ]);
  return { aliasMap, nodes, edges };
}
