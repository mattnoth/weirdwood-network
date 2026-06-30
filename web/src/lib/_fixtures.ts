// Shared test fixtures: the real graph bundle, loaded once (top-level await).
// The engine tests (resolve / read-node / walk-chain / agent loop) pivot on a real,
// permanent graph node as their example entity.

import { loadGraphData } from "./data.ts";
import type { GraphData } from "./types.ts";

export const data: GraphData = await loadGraphData();

/** The real graph node the engine tests pivot on (a rich causal chain to walk). */
export const TYWIN_SLUG = "assassination-of-tywin-lannister";
