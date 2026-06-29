// readNode() tests against the real bundle.

import assert from "node:assert/strict";
import { readNode } from "./read-node.ts";
import { data, TYWIN_SLUG } from "./_fixtures.ts";

Deno.test("readNode: returns name/type/identity/quotes for a known node", () => {
  const node = readNode(TYWIN_SLUG, data);
  assert.ok(node, "expected the Tywin assassination node");
  assert.equal(node!.name, "Assassination of Tywin Lannister");
  assert.equal(node!.type, "event.assassination");
  assert.ok(node!.identity.length > 0, "identity prose should be present");
  assert.ok(Array.isArray(node!.quotes));
  assert.ok(node!.quotes.length > 0, "this node carries curated quotes");
  // Quote shape is the receipts-ready {text, attribution, cite}.
  const q = node!.quotes[0];
  assert.ok("text" in q && "attribution" in q && "cite" in q);
});

Deno.test("readNode: missing slug returns null", () => {
  assert.equal(readNode("no-such-node-anywhere", data), null);
});

Deno.test("readNode: invalid slug returns null, no throw", () => {
  assert.equal(readNode("Bad Slug!", data), null);
  // deno-lint-ignore no-explicit-any
  assert.equal(readNode(null as any, data), null);
});
