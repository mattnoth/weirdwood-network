// node.ts — node lookup endpoint for the chat-UI (S177).
//
// Browser GETs /api/node?slug=X to fetch node data (name, type, quotes).
// Returns a NodeRecord or 404 if not found. Lightweight, no model call.

import { createTools, loadGraphData } from "../../src/lib/mod.ts";

// Load the curated graph once at cold start.
const graph = await loadGraphData();
const tools = createTools(graph);

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

  return new Response(JSON.stringify(node), {
    status: 200,
    headers: { "content-type": "application/json" },
  });
};
