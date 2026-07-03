// agent.ts tests: drive the tool loop with a STUBBED model (no SDK, no network,
// no API spend) against the REAL bundle. Validates dispatch, receipts emission,
// grounding/cite harvesting, and the cite-verification gate.
//
//   cd web && deno test --allow-read netlify/edge-functions/

import assert from "node:assert/strict";
import { createTools } from "../../../src/lib/mod.ts";
import { data, TYWIN_SLUG } from "../../../src/lib/_fixtures.ts";
import {
  type ChatMessage,
  estimateCostUsd,
  harvestResult,
  runAgent,
  type TurnResult,
  verifyCites,
} from "./agent.ts";

const tools = createTools(data);

/** Collect SSE events the agent emits. */
function recorder() {
  const events: Array<{ event: string; data: unknown }> = [];
  return { events, emit: (event: string, data: unknown) => events.push({ event, data }) };
}

const usage = { input: 10, output: 10 };

Deno.test("runAgent: resolves → reads → walks → answers, with receipts + grounding", async () => {
  // A real verifiable cite from the graph, baked into the model's final prose so
  // the gate sees one good citation alongside one fabricated one.
  const realNode = tools.readNode(TYWIN_SLUG);
  assert.ok(realNode && realNode.quotes.length > 0);
  const realCite = realNode!.quotes[0].cite;

  let turn = 0;
  const stub = (_msgs: ChatMessage[], onText: (d: string) => void): Promise<TurnResult> => {
    turn++;
    if (turn === 1) {
      return Promise.resolve({
        stopReason: "tool_use",
        usage,
        content: [{
          type: "tool_use",
          id: "t1",
          name: "resolve",
          input: { phrase: "death of Tywin" },
        }],
      });
    }
    if (turn === 2) {
      return Promise.resolve({
        stopReason: "tool_use",
        usage,
        content: [
          { type: "tool_use", id: "t2", name: "read_node", input: { slug: TYWIN_SLUG } },
          { type: "tool_use", id: "t3", name: "walk_chain", input: { slug: TYWIN_SLUG } },
        ],
      });
    }
    // Final turn: stream prose, real cite + one fabricated cite.
    onText("His own son put the bolt in him. ");
    onText(`(${realCite}) `);
    onText("(sources/chapters/fake/fake-99.md:999)");
    return Promise.resolve({
      stopReason: "end_turn",
      usage,
      content: [{ type: "text", text: "…" }],
    });
  };

  const { events, emit } = recorder();
  const messages: ChatMessage[] = [{ role: "user", content: "Who killed Tywin?" }];
  const result = await runAgent(messages, tools, stub, emit);

  // Three tool calls dispatched (resolve, read_node, walk_chain).
  assert.equal(result.toolCalls, 3);
  // read_node quotes + walk_chain links surfaced real evidence.
  assert.ok(result.grounding > 0, "expected grounding from quotes + chain links");
  assert.equal(result.stopState, "end_turn");

  // Receipts emitted from tool returns, one per call.
  const receipts = events.filter((e) => e.event === "receipt");
  assert.equal(receipts.length, 3);
  const tools_seen = receipts.map((r) => (r.data as { tool: string }).tool);
  assert.deepEqual(tools_seen, ["resolve", "read_node", "walk_chain"]);

  // Prose streamed as tokens.
  assert.ok(events.some((e) => e.event === "token"));

  // Loggable turn record (S186): assembled prose + replayable tool trace.
  assert.ok(result.prose.includes("His own son put the bolt in him."));
  assert.deepEqual(
    result.toolTrace.map((t) => t.tool),
    ["resolve", "read_node", "walk_chain"],
  );
  assert.deepEqual(result.toolTrace[1].input, { slug: TYWIN_SLUG });

  // The gate flags ONLY the fabricated cite; the real one passes.
  assert.deepEqual(result.unverifiedCites, ["sources/chapters/fake/fake-99.md:999"]);
  const citeCheck = events.find((e) => e.event === "cite-check");
  assert.ok(citeCheck);
  assert.equal((citeCheck!.data as { validCount: number }).validCount > 0, true);
});

Deno.test("runAgent: no tool calls → no-grounding status", async () => {
  const stub = (_m: ChatMessage[], onText: (d: string) => void): Promise<TurnResult> => {
    onText("The text holds no such scene.");
    return Promise.resolve({
      stopReason: "end_turn",
      usage,
      content: [{ type: "text", text: "…" }],
    });
  };
  const { events, emit } = recorder();
  const result = await runAgent(
    [{ role: "user", content: "Who is Quaithe really?" }],
    tools,
    stub,
    emit,
  );
  assert.equal(result.grounding, 0);
  assert.ok(
    events.some((e) =>
      e.event === "status" && (e.data as { state: string }).state === "no-grounding"
    ),
  );
});

Deno.test("runAgent: hits the iteration ceiling → loop-bound-hit", async () => {
  // A model that always asks for another tool call.
  const stub = (): Promise<TurnResult> =>
    Promise.resolve({
      stopReason: "tool_use",
      usage,
      content: [{ type: "tool_use", id: "x", name: "resolve", input: { phrase: "Jon Snow" } }],
    });
  const { events, emit } = recorder();
  const result = await runAgent([{ role: "user", content: "loop" }], tools, stub, emit);
  assert.equal(result.stopState, "loop-bound-hit");
  assert.ok(
    events.some((e) =>
      e.event === "status" && (e.data as { state: string }).state === "loop-bound-hit"
    ),
  );
});

Deno.test("harvestResult: collects cites from node quotes and chain refs", () => {
  const cites = new Set<string>();
  const g1 = harvestResult(tools.readNode(TYWIN_SLUG), cites);
  const g2 = harvestResult(tools.walkChain(TYWIN_SLUG), cites);
  assert.ok(g1 > 0 && g2 > 0);
  assert.ok(cites.size > 0, "expected real cites in the allowlist");
});

Deno.test("verifyCites: only out-of-allowlist cites are flagged", () => {
  const valid = new Set(["sources/chapters/asos/asos-sansa-05.md:45"]);
  const prose =
    "see asos-sansa-05? sources/chapters/asos/asos-sansa-05.md:45 is real; bad.md:1 is not.";
  assert.deepEqual(verifyCites(prose, valid), ["bad.md:1"]);
});

Deno.test("estimateCostUsd: prices per model", () => {
  const c = estimateCostUsd({ input: 1_000_000, output: 1_000_000 }, "claude-opus-4-8");
  assert.equal(c, 30); // $5 in + $25 out
});
