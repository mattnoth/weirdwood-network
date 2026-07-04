// node.ts — node lookup endpoint for the chat-UI (S177).
//
// Browser GETs /api/node?slug=X to fetch node data (name, type, quotes).
// Returns a NodeRecord or 404 if not found. Lightweight, no model call.
//
// Narrative-Arc enrichment (query-layer Track, step 6c / D-F): the inlined
// bundle (`web/data/nodes.json`) deliberately drops `## Narrative Arc` prose
// (measured step 0: inlining it would nearly TRIPLE the bundle). Instead,
// `graph/query/build/build_node_assets.py` emits one static JSON asset per
// qualifying node to `web/public/node/<slug>.json` — a build OUTPUT the Edge
// Function's filesystem-free runtime cannot read directly (Deno.readTextFile
// throws on Edge Functions, same reason data.ts inlines the main bundle via
// JSON module imports instead of reading files). A per-node asset can't be
// import-inlined the same way (there are thousands, and only the requested
// one is ever needed per request), so this fetches it over HTTP from the
// SAME origin that served this very request — network I/O falls outside the
// Edge Function's 50ms CPU budget, unlike an in-memory bundle lookup. This
// works identically in prod (Netlify serves web/public/ as the publish dir)
// and in local dev (scripts/dev.ts's serveDir() serves web/public/ at the
// same port /api/node runs on) since both derive the origin from the
// incoming request's own URL — no separate "site base URL" env var needed.
// Fails SOFT: any fetch failure (404, network hiccup, missing asset) simply
// omits narrativeArc from the response — today's response shape is a strict
// subset, never a broken one.

import { createTools, loadGraphData } from "../../src/lib/mod.ts";

// Load the curated graph once at cold start.
const graph = await loadGraphData();
const tools = createTools(graph);

/** Fetch web/public/node/<slug>.json relative to `origin` (the same host that
 *  served the incoming request). Returns null on ANY failure — a missing
 *  asset (no Narrative Arc section for this node), a 404, or a network
 *  error are all treated identically: "no arc content available", not an
 *  error surfaced to the caller. Never throws. */
async function fetchNarrativeArc(
  slug: string,
  origin: string,
): Promise<{ narrative_arc: string; cites?: string[] } | null> {
  try {
    const res = await fetch(new URL(`/node/${encodeURIComponent(slug)}.json`, origin));
    if (!res.ok) return null;
    const asset = await res.json();
    if (typeof asset?.narrative_arc !== "string") return null;
    return { narrative_arc: asset.narrative_arc, cites: asset.cites };
  } catch {
    return null; // fail-soft: a missing asset degrades to today's response
  }
}

export default async (req: Request): Promise<Response> => {
  const url = new URL(req.url);
  const slug = url.searchParams.get("slug");

  if (!slug) {
    return new Response(JSON.stringify({ error: "slug parameter required" }), {
      status: 400,
      headers: { "content-type": "application/json" },
    });
  }

  const node = tools.readNode(slug);
  if (!node) {
    return new Response(JSON.stringify({ error: "node not found", slug }), {
      status: 404,
      headers: { "content-type": "application/json" },
    });
  }

  const arc = await fetchNarrativeArc(slug, url.origin);
  // deno-lint-ignore no-explicit-any
  const body: any = { ...node };
  if (arc) {
    body.narrativeArc = arc.narrative_arc;
    if (arc.cites) body.narrativeArcCites = arc.cites;
  }

  return new Response(JSON.stringify(body), {
    status: 200,
    headers: { "content-type": "application/json" },
  });
};
