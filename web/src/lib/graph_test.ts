// walkChain() + neighbors() tests against the real bundle.

import assert from "node:assert/strict";
import { neighbors, walkChain } from "./graph.ts";
import { data, TYWIN_SLUG } from "./_fixtures.ts";

Deno.test("walkChain: the default walk is a depth-bounded spine, not the whole component", () => {
  const chain = walkChain(TYWIN_SLUG, data);

  // The default walk is capped at DEFAULT_MAX_DEPTH (2) hops each direction so
  // the "chain walked" panel reads as a tight spine, not a 50-edge graph dump.
  for (const l of [...chain.upstream, ...chain.downstream]) {
    assert.ok(l.depth <= 2, "default walk must not exceed maxDepth=2");
    assert.ok(l.source && l.edge_type && l.target, "link missing source/edge_type/target");
  }

  // Raising maxDepth recovers the deeper transitive chain (proves the cap is the
  // only thing limiting it, not a broken walk).
  const deep = walkChain(TYWIN_SLUG, data, { maxDepth: 10 });
  assert.ok(
    deep.upstream.length > chain.upstream.length,
    "a deeper walk should reach more upstream links than the bounded default",
  );

  // Links remain unique within the bounded walk.
  const key = (l: { source: string; edge_type: string; target: string }) =>
    `${l.source}|${l.edge_type}|${l.target}`;
  const keys = chain.upstream.map(key);
  assert.equal(new Set(keys).size, keys.length, "upstream links must be unique");
});

Deno.test("walkChain: links are enriched with node display names + types", () => {
  const chain = walkChain(TYWIN_SLUG, data);
  const l = [...chain.upstream, ...chain.downstream].find((x) => x.depth === 1);
  assert.ok(l, "expected at least one adjacent link");
  // The receipts panel renders source_name/target_name so live chains show
  // "Assassination of Tywin Lannister", not the raw slug.
  assert.ok(l!.source_name && l!.target_name, "links must carry display names");
  assert.ok(l!.source_type && l!.target_type, "links must carry node types");
});

Deno.test("walkChain: links carry the receipts fields", () => {
  const chain = walkChain(TYWIN_SLUG, data);
  const adjacent = chain.upstream.find((l) => l.depth === 1);
  assert.ok(adjacent, "expected a depth-1 upstream link");
  // depth-1 upstream of the assassination is the Tysha reveal causing it.
  assert.equal(adjacent!.target, TYWIN_SLUG);
  assert.equal(adjacent!.edge_type, "CAUSES");
  assert.ok("evidence_quote" in adjacent! && "ref" in adjacent! && "tier" in adjacent!);
});

Deno.test("walkChain: downstream effects are reachable too", () => {
  const chain = walkChain(TYWIN_SLUG, data);
  assert.ok(chain.downstream.length > 0, "expected downstream consequences");
  // Every downstream link originates from the queried node (depth 1) or a node
  // reached from it; the nearest must have the pivot as source.
  assert.ok(chain.downstream.some((l) => l.source === TYWIN_SLUG && l.depth === 1));
});

Deno.test("walkChain: full-chain follows ENABLES, plain chain does not", () => {
  const plain = walkChain(TYWIN_SLUG, data);
  const full = walkChain(TYWIN_SLUG, data, { full: true });
  const plainTotal = plain.upstream.length + plain.downstream.length;
  const fullTotal = full.upstream.length + full.downstream.length;
  assert.ok(fullTotal >= plainTotal, "full-chain should never be smaller than plain");
  assert.equal(plain.full, false);
  assert.equal(full.full, true);
  // No ENABLES leaks into the strict causal walk.
  assert.ok(![...plain.upstream, ...plain.downstream].some((l) => l.edge_type === "ENABLES"));
});

Deno.test("walkChain: invalid slug returns an empty chain, no throw", () => {
  const chain = walkChain("not a slug!!", data);
  assert.deepEqual(chain.upstream, []);
  assert.deepEqual(chain.downstream, []);
});

Deno.test("neighbors: groups edges by direction and type", () => {
  const n = neighbors(TYWIN_SLUG, data);
  assert.ok(n.outgoingCount > 0 || n.incomingCount > 0, "Tywin node should have edges");
  // Counts equal the sum of each direction's grouped links.
  const sum = (g: Record<string, unknown[]>) => Object.values(g).reduce((a, b) => a + b.length, 0);
  assert.equal(sum(n.outgoing), n.outgoingCount);
  assert.equal(sum(n.incoming), n.incomingCount);
  // Every outgoing link has the pivot as source; every incoming as target.
  for (const links of Object.values(n.outgoing)) {
    for (const l of links) assert.equal(l.source, TYWIN_SLUG);
  }
  for (const links of Object.values(n.incoming)) {
    for (const l of links) assert.equal(l.target, TYWIN_SLUG);
  }
});

Deno.test("neighbors: invalid slug returns empty groups, no throw", () => {
  const n = neighbors("../etc/passwd", data);
  assert.equal(n.outgoingCount, 0);
  assert.equal(n.incomingCount, 0);
  assert.deepEqual(n.outgoing, {});
});
