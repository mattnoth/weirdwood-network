// chat.ts — the only backend for the Weirwood chat-UI alpha (function chunk, S173).
//
// Browser POSTs to /api/chat (mapped in netlify.toml). This Netlify Edge Function
// (Deno) holds ANTHROPIC_API_KEY server-side, runs a Claude tool-use loop over the
// S172 retrieval tools (agent.ts), and streams the reply back as SSE. The browser
// never sees the key.
//
// Runtime decision (S171): Edge Functions. The 50 ms CPU limit excludes time spent
// waiting on the Claude API, with a 40 s response-header window — the right fit for
// a streaming multi-tool turn. SDK + Blobs imported via esm.sh URLs — Netlify's
// edge bundler can't resolve `npm:` specifiers (experimental), esm.sh is Deno-native.
//
// Auth (design §4): new Anthropic() resolves ANTHROPIC_API_KEY → ANTHROPIC_AUTH_TOKEN
// → an `ant auth login` OAuth profile. Deployed: set ANTHROPIC_API_KEY in Netlify env.
// Local: leave it unset and run on Matt's subscription. Key-present is the only diff.

import Anthropic from "https://esm.sh/@anthropic-ai/sdk@0.106.0";
import type { Context } from "https://edge.netlify.com";
import { createTools, loadGraphData } from "../../src/lib/mod.ts";
import {
  type ChatMessage,
  type ContentBlock,
  estimateCostUsd,
  type Persona,
  runAgent,
  type RunTurn,
  systemPromptFor,
  TOOL_DEFS,
} from "./lib/agent.ts";

// ---- Locked config (S171). Swap the model via this ONE constant. ----
// Deploy default stays Opus (committed → deploy-safe, no edit-and-revert risk).
// Local dev overrides via WEIRWOOD_MODEL — web/scripts/dev.ts sets it to Sonnet. (S175)
const MODEL = Deno.env.get("WEIRWOOD_MODEL") ?? "claude-opus-4-8"; // local: WEIRWOOD_MODEL=claude-sonnet-4-6
const MAX_TOKENS = 4096; // a chat reply, not a document; bounds per-request cost
const DAILY_SPEND_CAP_USD = 50; // global ceiling — the load-bearing cost control (raised 5→50 for Opus)
const MAX_HISTORY_MESSAGES = 24; // cap conversation length the browser can replay

// Load the curated graph once at cold start (~8.8 MB, fits in memory — lib README).
// Top-level await: the module won't serve a request until the bundle is in.
const graph = await loadGraphData();
const tools = createTools(graph);

// System prompt as a cacheable block, per persona (stable prefix → prompt caching).
// Each persona's text is a fixed string, so it still caches as a prefix.
function systemBlocks(persona: Persona) {
  return [
    {
      type: "text" as const,
      text: systemPromptFor(persona),
      cache_control: { type: "ephemeral" as const },
    },
  ];
}

const encoder = new TextEncoder();
function sseFrame(event: string, data: unknown): Uint8Array {
  return encoder.encode(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`);
}

// ---- Durable daily spend cap (Netlify Blobs; best-effort) ----
// The global ceiling is the load-bearing control — per-IP counters are bypassable.
// Local dev has no Blobs context: degrade gracefully (cap not enforced) rather than 500.

function spendKey(): string {
  return `spend-${new Date().toISOString().slice(0, 10)}`; // spend-YYYY-MM-DD (UTC)
}

async function getStore() {
  try {
    const { getStore } = await import("https://esm.sh/@netlify/blobs@8");
    return getStore("weirwood-chat");
  } catch {
    return null;
  }
}

async function readDailySpend(): Promise<number> {
  const store = await getStore();
  if (!store) return 0;
  try {
    const raw = await store.get(spendKey());
    return raw ? Number(raw) || 0 : 0;
  } catch {
    return 0;
  }
}

async function addDailySpend(usd: number): Promise<void> {
  const store = await getStore();
  if (!store) return;
  try {
    const current = Number(await store.get(spendKey())) || 0;
    await store.set(spendKey(), String(current + usd));
  } catch {
    // best-effort: a write miss just under-counts; the cap stays advisory
  }
}

/** One turn's usage record. Structured receipts + the assembled prose only — never
 *  raw assistant content blocks (thinking / tool_use). `toolTrace` is the replayable
 *  chain (the resolve/read_node/walk_chain slugs), so a broken answer can be re-walked
 *  against the graph later. */
interface TurnLog {
  question: string;
  prose: string;
  toolTrace: unknown;
  toolCalls: number;
  grounding: number;
  unverifiedCites: string[];
  usage: unknown;
  costUsd: number;
  stopState: string;
  model: string;
  persona: string;
  timestamp: string;
}

/** Persist one turn to a UNIQUE date-partitioned Blobs key — a plain write, NEVER
 *  read-modify-write (that pattern races and would drop turns under concurrency).
 *  Always mirrors a compact line to the function log so an absent/throwing Blobs
 *  context still leaves a record. Logging must NEVER fail a turn — all swallowed. */
async function logTurn(rec: TurnLog): Promise<void> {
  // Compact console mirror first, so it survives even if the Blobs write throws.
  try {
    console.log(
      `[turn] ${rec.timestamp} q=${JSON.stringify(rec.question.slice(0, 120))} ` +
        `tools=${rec.toolCalls} grounding=${rec.grounding} ` +
        `unverified=${rec.unverifiedCites.length} stop=${rec.stopState} cost=$${rec.costUsd}`,
    );
  } catch { /* never fail a turn on logging */ }
  try {
    const store = await getStore();
    if (!store) return;
    const key = `log/${new Date().toISOString().slice(0, 10)}/${crypto.randomUUID()}`;
    await store.set(key, JSON.stringify(rec));
  } catch { /* never fail a turn on logging */ }
}

/** A refused or failed turn carries no usage — record the question + why it ended,
 *  zeros elsewhere, so cost-cap trips and api-errors are countable in the logs (not
 *  just a bare console.error). Cost of these turns is ~nil; the value is observability. */
function failedTurn(question: string, stopState: string, persona: Persona): TurnLog {
  return {
    question,
    prose: "",
    toolTrace: null,
    toolCalls: 0,
    grounding: 0,
    unverifiedCites: [],
    usage: { input: 0, output: 0 },
    costUsd: 0,
    stopState,
    model: MODEL,
    persona,
    timestamp: new Date().toISOString(),
  };
}

/** The visitor's question: the text of the final user turn (string content, or the
 *  concatenated text blocks of a structured one). Empty string if none. */
function lastUserText(messages: ChatMessage[]): string {
  for (let i = messages.length - 1; i >= 0; i--) {
    const m = messages[i];
    if (m.role !== "user") continue;
    if (typeof m.content === "string") return m.content;
    if (Array.isArray(m.content)) {
      return m.content
        .filter((b): b is { type: "text"; text: string } =>
          (b as { type?: string }).type === "text"
        )
        .map((b) => b.text)
        .join(" ");
    }
  }
  return "";
}

// ---- Request parsing ----

interface IncomingBody {
  messages?: Array<{ role?: unknown; content?: unknown }>;
}

/** Coerce the posted body into a clean user/assistant transcript, or null if
 *  unusable. The model never trusts client text for tool inputs (the tools are
 *  the trust boundary), but we still bound shape and length here. */
function parseMessages(body: IncomingBody): ChatMessage[] | null {
  if (!body || !Array.isArray(body.messages) || body.messages.length === 0) return null;
  const out: ChatMessage[] = [];
  for (const m of body.messages.slice(-MAX_HISTORY_MESSAGES)) {
    const role = m.role === "assistant" ? "assistant" : m.role === "user" ? "user" : null;
    if (!role) return null;
    // Accept a plain string, or pass through prior assistant content blocks
    // (tool_use / thinking) verbatim so a multi-turn replay keeps the loop valid.
    if (typeof m.content === "string") {
      out.push({ role, content: m.content.slice(0, 8000) });
    } else if (Array.isArray(m.content)) {
      out.push({ role, content: m.content as ContentBlock[] });
    } else {
      return null;
    }
  }
  if (out.length === 0 || out[out.length - 1].role !== "user") return null;
  return out;
}

function makeClient(): Anthropic {
  const key = Deno.env.get("ANTHROPIC_API_KEY");
  // Pass the key when present (deployed); otherwise construct bare so the SDK's
  // own resolution (AUTH_TOKEN / OAuth profile) runs for local `netlify dev`.
  return key ? new Anthropic({ apiKey: key }) : new Anthropic();
}

// ---- Handler ----

export default async function handler(request: Request, _context: Context): Promise<Response> {
  if (request.method !== "POST") {
    return new Response("Method Not Allowed", { status: 405 });
  }

  let messages: ChatMessage[] | null;
  let persona: Persona = "loremaster"; // default voice; "bloodraven" is the toggle
  try {
    const raw = await request.json();
    messages = parseMessages(raw);
    if (raw?.persona === "bloodraven") persona = "bloodraven";
  } catch {
    messages = null;
  }
  if (!messages) {
    return Response.json({
      error: "Body must be { messages: [{role, content}, …] } ending in a user turn.",
    }, { status: 400 });
  }

  // Cost guard: pre-check the global daily ceiling before spending a token.
  if ((await readDailySpend()) >= DAILY_SPEND_CAP_USD) {
    await logTurn(failedTurn(lastUserText(messages), "cost-cap-tripped", persona));
    const stream = new ReadableStream({
      start(controller) {
        controller.enqueue(sseFrame("status", { state: "cost-cap-tripped" }));
        controller.enqueue(sseFrame("done", { ok: false }));
        controller.close();
      },
    });
    return new Response(stream, { headers: sseHeaders() });
  }

  const client = makeClient();

  // One model turn over the streaming API: emit text deltas, return the final message.
  const runTurn: RunTurn = async (msgs, onText) => {
    const stream = client.messages.stream({
      model: MODEL,
      max_tokens: MAX_TOKENS,
      system: systemBlocks(persona),
      thinking: { type: "adaptive" },
      // TOOL_DEFS are plain objects in the SDK-free agent.ts; the cast lands them
      // on the SDK's Tool type at this one boundary.
      tools: TOOL_DEFS as unknown as Anthropic.Tool[],
      // deno-lint-ignore no-explicit-any -- agent.ts uses a minimal local block shape
      messages: msgs as any,
    });
    for await (const event of stream) {
      if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
        onText(event.delta.text);
      }
    }
    const final = await stream.finalMessage();
    return {
      content: final.content as unknown as ContentBlock[],
      stopReason: final.stop_reason,
      usage: { input: final.usage.input_tokens, output: final.usage.output_tokens },
    };
  };

  const body = new ReadableStream({
    async start(controller) {
      const emit = (event: string, data: unknown) => {
        try {
          controller.enqueue(sseFrame(event, data));
        } catch {
          // controller closed (client disconnected) — stop emitting
        }
      };
      try {
        const result = await runAgent(messages!, tools, runTurn, emit);
        const costUsd = estimateCostUsd(result.usage, MODEL);
        await addDailySpend(costUsd);
        // Usage logging (S186): network I/O, off the 50ms CPU budget, never fails a turn.
        await logTurn({
          question: lastUserText(messages!),
          prose: result.prose,
          toolTrace: result.toolTrace,
          toolCalls: result.toolCalls,
          grounding: result.grounding,
          unverifiedCites: result.unverifiedCites,
          usage: result.usage,
          costUsd: Math.round(costUsd * 10000) / 10000,
          stopState: result.stopState,
          model: MODEL,
          persona,
          timestamp: new Date().toISOString(),
        });
        emit("done", {
          ok: true,
          stopState: result.stopState,
          toolCalls: result.toolCalls,
          grounding: result.grounding,
          unverifiedCites: result.unverifiedCites,
          usage: result.usage,
          costUsd: Math.round(costUsd * 10000) / 10000,
        });
      } catch (err) {
        // api-error / timeout failure-mode (design §9): a user-safe message, no key leakage.
        emit("error", { message: "The weirwood is silent. Try again shortly." });
        emit("status", { state: "api-error" });
        emit("done", { ok: false });
        console.error("chat.ts turn failed:", err);
        await logTurn(failedTurn(lastUserText(messages!), "api-error", persona));
      } finally {
        try {
          controller.close();
        } catch { /* already closed */ }
      }
    },
  });

  return new Response(body, { headers: sseHeaders() });
}

function sseHeaders(): HeadersInit {
  return {
    "content-type": "text/event-stream; charset=utf-8",
    "cache-control": "no-cache, no-transform",
    "connection": "keep-alive",
  };
}
