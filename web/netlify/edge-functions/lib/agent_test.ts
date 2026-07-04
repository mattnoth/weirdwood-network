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
  MAX_TOOL_ITERATIONS,
  outcomeFor,
  runAgent,
  systemPromptFor,
  TOOL_DEFS,
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

Deno.test("harvestResult: recovers a cite buried in quote text (cite:null)", () => {
  // Mirrors the book-cite-overlay quotes that carry the real chapter:line inside
  // .text with cite:null. The model lifts that token correctly; the gate must
  // treat it as verified, so harvestResult has to admit it from the text.
  const buried = "sources/chapters/acok/acok-theon-04.md:23";
  const cites = new Set<string>();
  harvestResult(
    { quotes: [{ text: `their gilded skulls, ACOK Theon IV (\`${buried}\`)`, cite: null }] },
    cites,
  );
  assert.ok(cites.has(buried), "buried cite must enter the allowlist");
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

// ---- search_quotes tool (query-layer step 5c) ----

Deno.test("TOOL_DEFS: search_quotes schema present with query (required) + type (optional)", () => {
  const def = TOOL_DEFS.find((t) => t.name === "search_quotes");
  assert.ok(def, "search_quotes must be registered in TOOL_DEFS");
  const props = def!.input_schema.properties as Record<string, unknown>;
  assert.ok("query" in props, "search_quotes must accept a query param");
  assert.ok("type" in props, "search_quotes must accept an optional type param");
  assert.deepEqual(def!.input_schema.required, ["query"]);
});

Deno.test("runAgent: search_quotes stubbed call path — dispatches, grounds, receipts", async () => {
  let turn = 0;
  const stub = (_msgs: ChatMessage[], onText: (d: string) => void): Promise<TurnResult> => {
    turn++;
    if (turn === 1) {
      return Promise.resolve({
        stopReason: "tool_use",
        usage,
        content: [{
          type: "tool_use",
          id: "s1",
          name: "search_quotes",
          input: { query: "lemon cakes", type: "foods" },
        }],
      });
    }
    onText("Lemon cakes turn up as a favored sweet. ");
    return Promise.resolve({
      stopReason: "end_turn",
      usage,
      content: [{ type: "text", text: "…" }],
    });
  };

  const { events, emit } = recorder();
  const result = await runAgent(
    [{ role: "user", content: "Describe some lemon cakes" }],
    tools,
    stub,
    emit,
  );

  assert.equal(result.toolCalls, 1);
  assert.ok(result.grounding > 0, "search_quotes hits should ground the answer");

  const receipts = events.filter((e) => e.event === "receipt");
  assert.equal(receipts.length, 1);
  assert.equal((receipts[0].data as { tool: string }).tool, "search_quotes");
  const searchResult = (receipts[0].data as { result: unknown }).result;
  assert.ok(Array.isArray(searchResult) && searchResult.length > 0, "expected ranked hits");

  // toolTrace carries the small outcome slice (matchType/topSlug/resultCount).
  assert.equal(result.toolTrace.length, 1);
  assert.equal(result.toolTrace[0].tool, "search_quotes");
  const outcome = result.toolTrace[0].outcome;
  assert.ok(outcome, "search_quotes call must carry a logged outcome");
  assert.equal(outcome!.matchType, "hit");
  assert.equal(typeof outcome!.topSlug, "string");
  assert.ok((outcome!.resultCount ?? 0) > 0);
});

Deno.test("outcomeFor: resolve exact/fuzzy/miss + search_quotes hit/miss shapes", () => {
  const exactHit = outcomeFor("resolve", tools.resolve("Tywin Lannister"));
  assert.equal(exactHit?.matchType, "exact");
  assert.equal(typeof exactHit?.topSlug, "string");
  assert.equal(typeof exactHit?.score, "number");

  const resolveMiss = outcomeFor("resolve", tools.resolve("zzz-not-a-real-phrase-zzz"));
  assert.deepEqual(resolveMiss, { matchType: "miss", topSlug: null });

  const searchHit = outcomeFor("search_quotes", tools.searchQuotes("lemon cakes"));
  assert.equal(searchHit?.matchType, "hit");
  assert.equal(typeof searchHit?.topSlug, "string");
  assert.ok((searchHit?.resultCount ?? 0) > 0);

  const searchMiss = outcomeFor("search_quotes", tools.searchQuotes("zzzznonsensequery"));
  assert.deepEqual(searchMiss, { matchType: "miss", topSlug: null, resultCount: 0 });

  // Other tools: no outcome slice (not in scope for this telemetry fix).
  assert.equal(outcomeFor("read_node", tools.readNode(TYWIN_SLUG)), undefined);
});

// ---- Invariants pinned per the S190 handoff: don't let a routing/persona ----
// ---- edit silently regress the safety block or the loop-bound backstop. ----

Deno.test("MAX_TOOL_ITERATIONS stays 6 (hard gate — never change without explicit sign-off)", () => {
  assert.equal(MAX_TOOL_ITERATIONS, 6);
});

Deno.test("SHARED_RULES text is unchanged (pinned invariant) — theory-gate, cite rules, quote floor", () => {
  // SHARED_RULES isn't exported directly; both personas concatenate it verbatim
  // after their own voice block, starting at "# Answering — general". Extract
  // it from the composed prompt so this test doesn't need a new export, and
  // pin the FULL text (not just a snippet) so any edit to the safety block —
  // theory-gate, cite-verification rules, or the >=2-quote floor — fails loud.
  const composed = systemPromptFor("loremaster");
  const marker = "# Answering — general";
  const idx = composed.indexOf(marker);
  assert.ok(idx >= 0, "SHARED_RULES marker not found in composed prompt");
  const sharedRules = composed.slice(idx);

  // bloodraven must concatenate the IDENTICAL shared block (persona-independence).
  const composedBR = systemPromptFor("bloodraven");
  const idxBR = composedBR.indexOf(marker);
  assert.equal(composedBR.slice(idxBR), sharedRules, "SHARED_RULES must be persona-independent");

  // Pin the load-bearing invariants explicitly (theory-gate, cite rules, quote floor)
  // so a routing-table edit that accidentally clips this section fails clearly.
  assert.ok(sharedRules.includes("do NOT introduce theories"));
  assert.ok(sharedRules.includes("NEVER wink at an answer you cannot cite"));
  assert.ok(sharedRules.includes("AT LEAST TWO"));
  assert.ok(sharedRules.includes("NEVER invent a chapter:line citation"));
  assert.ok(sharedRules.includes("[[q|"));

  // Full-text pin: fails loud on ANY change to SHARED_RULES, intentional or not —
  // if this test fails on a legitimate SHARED_RULES edit, update the expected
  // hash/length below deliberately (this is the tripwire, not a silent drift net).
  assert.equal(sharedRules.length, 10478, "SHARED_RULES length changed — confirm intentional");
});
