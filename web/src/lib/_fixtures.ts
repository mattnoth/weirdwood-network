// Shared test fixtures: the real bundle, loaded once (top-level await), plus the
// pre-walked featured-tywin.json the live walk is asserted against.

import { DEFAULT_DATA_DIR, loadGraphData } from "./data.ts";
import type { GraphData } from "./types.ts";

export const data: GraphData = await loadGraphData();

export interface FeaturedChainLink {
  source: string;
  source_name: string;
  edge_type: string;
  target: string;
  target_name: string;
  evidence_quote: string;
  evidence_ref: string;
  tier: number;
}

export interface Featured {
  slug: string;
  question: string;
  title: string;
  chain: FeaturedChainLink[];
}

export const featured: Featured = JSON.parse(
  await Deno.readTextFile(new URL("featured-tywin.json", DEFAULT_DATA_DIR)),
);

/** The featured slug both required assertions pivot on. */
export const TYWIN_SLUG = "assassination-of-tywin-lannister";
