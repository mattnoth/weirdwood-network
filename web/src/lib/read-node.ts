// readNode(slug) — the node's name, type, identity prose and curated quotes.
// A direct nodes.json lookup (build-chat-export already shaped the records).
// Returns null for a missing or invalid slug (trust boundary, validate.ts).

import type { GraphData, NodeRecord } from "./types.ts";
import { isValidSlug } from "./validate.ts";

export function readNode(slug: string, data: GraphData): NodeRecord | null {
  if (!isValidSlug(slug)) return null;
  return data.nodes[slug] ?? null;
}
