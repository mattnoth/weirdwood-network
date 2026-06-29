// resolve() tests against the real bundle.

import assert from "node:assert/strict";
import { resolve } from "./resolve.ts";
import { data, TYWIN_SLUG } from "./_fixtures.ts";

Deno.test("resolve: REQUIRED — 'death of Tywin' -> assassination-of-tywin-lannister", () => {
  const hits = resolve("death of Tywin", data);
  assert.ok(hits.length >= 1, "expected at least one candidate");
  assert.equal(hits[0].slug, TYWIN_SLUG);
  assert.equal(hits[0].matchType, "exact");
  assert.equal(hits[0].score, 1.0);
  assert.equal(hits[0].category, "events");
});

Deno.test("resolve: exact lookup is article/case/whitespace insensitive", () => {
  // All normalize to the same key as "death of tywin".
  for (const q of ["Death of Tywin", "  death   of   tywin ", "the death of Tywin"]) {
    const hits = resolve(q, data);
    assert.equal(hits[0]?.slug, TYWIN_SLUG, `query: ${q}`);
  }
});

Deno.test("resolve: a known character phrase resolves to its node", () => {
  const hits = resolve("Eddard Stark", data);
  assert.ok(hits.some((h) => h.slug === "eddard-stark"), "eddard-stark not among candidates");
});

Deno.test("resolve: fuzzy fallback fires on a near-miss phrase", () => {
  // Not an exact alias key, but token-overlap should still surface the event.
  const hits = resolve("Tywin assassination on the privy", data);
  assert.ok(hits.length > 0, "expected fuzzy candidates");
  assert.equal(hits[0].matchType, "fuzzy");
  assert.ok(hits.every((h) => h.score >= 0.5), "all fuzzy scores must clear the 0.5 floor");
});

Deno.test("resolve: invalid / empty input returns []", () => {
  assert.deepEqual(resolve("", data), []);
  assert.deepEqual(resolve("   ", data), []);
  // deno-lint-ignore no-explicit-any
  assert.deepEqual(resolve(null as any, data), []);
});

Deno.test("resolve: pure gibberish returns no candidates", () => {
  assert.deepEqual(resolve("zzzqqq xkcdwobble", data), []);
});
