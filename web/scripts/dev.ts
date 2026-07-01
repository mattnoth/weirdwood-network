// web/scripts/dev.ts — LOCAL dev server (S175). NOT shipped.
//
// A lightweight stand-in for `netlify dev` so the web app can be exercised locally
// WITHOUT the Netlify CLI. It serves web/public/ statically and routes POST
// /api/chat. Two modes:
//
//   LIVE  (default):       routes /api/chat into the real chat.ts handler. Needs a
//                          credential (ANTHROPIC_API_KEY) and calls the model.
//                            ANTHROPIC_API_KEY=sk-ant-… ~/.deno/bin/deno run -A \
//                              --node-modules-dir=auto scripts/dev.ts
//
//   DEMO  (WEIRWOOD_DEMO=1): does NOT call the model and needs NO key. Intended to
//                          replay a REAL recorded conversation over the SAME SSE
//                          contract the live function uses, so the design can be
//                          judged at $0. No conversation has been recorded yet (the
//                          Tywin placeholder was removed), so DEMO currently streams
//                          a short notice telling you to run LIVE. Wire a real
//                          recorded transcript here once one is captured.
//                            WEIRWOOD_DEMO=1 ~/.deno/bin/deno run -A scripts/dev.ts
//
// Model (LIVE only): defaults to Sonnet 4.6 for cheap iteration; the committed
// deploy default (Opus, in chat.ts) is untouched.
//
import { serveDir } from "jsr:@std/http/file-server";
import { fromFileUrl } from "jsr:@std/path";

const DEMO = Deno.env.get("WEIRWOOD_DEMO") === "1";
const PORT = Number(Deno.env.get("PORT") ?? 8766);
const FS_ROOT = fromFileUrl(new URL("../public/", import.meta.url));

// Only the LIVE path needs the model SDK + 8.8 MB graph. In DEMO we skip importing
// chat.ts entirely, so the replay is independent of any credential or the bundle.
let handler: ((req: Request, ctx: never) => Promise<Response>) | null = null;
let nodeHandler: ((req: Request) => Promise<Response>) | null = null;
if (!DEMO) {
  // Set the model BEFORE importing chat.ts: its MODEL const reads this env at
  // module-eval time, and a dynamic import guarantees the env is set first.
  if (!Deno.env.get("WEIRWOOD_MODEL")) Deno.env.set("WEIRWOOD_MODEL", "claude-sonnet-4-6");
  handler = (await import("../netlify/edge-functions/chat.ts")).default;
  // The keyless /api/node lookup (node dossiers). Reads the same bundle; no model.
  nodeHandler = (await import("../netlify/edge-functions/node.ts")).default;
}

// ---- DEMO (no-key) replay --------------------------------------------------
//
// No recorded conversation exists yet (the Tywin placeholder fixture was removed).
// Until a real transcript is captured and wired here, DEMO streams an honest notice
// over the SSE contract rather than any mocked AI prose.

const sleep = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));

const DEMO_NOTICE =
  "Demo replay isn't wired yet — no conversation has been recorded. " +
  "Run the server in LIVE mode (with an API key) to ask real questions.";

function demoReplay(): Response {
  const enc = new TextEncoder();
  const frame = (event: string, data: unknown) =>
    enc.encode(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`);

  const stream = new ReadableStream({
    async start(controller) {
      const emit = (event: string, data: unknown) => controller.enqueue(frame(event, data));
      try {
        await sleep(150);
        const words = DEMO_NOTICE.split(" ");
        for (let i = 0; i < words.length; i++) {
          emit("token", { text: (i ? " " : "") + words[i] });
          await sleep(35);
        }
        emit("done", { ok: true, stopState: "complete", toolCalls: 0, demo: true });
      } finally {
        try {
          controller.close();
        } catch { /* already closed */ }
      }
    },
  });

  return new Response(stream, {
    headers: {
      "content-type": "text/event-stream; charset=utf-8",
      "cache-control": "no-cache, no-transform",
      "connection": "keep-alive",
    },
  });
}

// ---- Server ----------------------------------------------------------------

Deno.serve(
  {
    port: PORT,
    hostname: "127.0.0.1",
    onListen: () =>
      console.log(
        `\n  Weirwood dev → http://127.0.0.1:${PORT}/\n  mode: ${
          DEMO ? "DEMO (replay — no key, no model)" : `LIVE (model: ${Deno.env.get("WEIRWOOD_MODEL")})`
        }\n`,
      ),
  },
  async (req: Request): Promise<Response> => {
    const { pathname } = new URL(req.url);
    if (pathname === "/api/chat") {
      if (DEMO) return demoReplay();
      return await handler!(req, {} as never);
    }
    if (pathname === "/api/node") {
      if (DEMO || !nodeHandler) return Response.json({ error: "node lookup not available in DEMO" }, { status: 503 });
      return await nodeHandler(req);
    }
    // no-store so every reload picks up edited HTML/CSS/JS immediately (dev only).
    return await serveDir(req, { fsRoot: FS_ROOT, quiet: true, headers: ["cache-control: no-store"] });
  },
);
