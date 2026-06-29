// Unit tests for normalize() + tokenize() — no bundle needed (pure functions).

import assert from "node:assert/strict";
import { intersectionSize, normalize, tokenize } from "./normalize.ts";

Deno.test("normalize: lowercases, strips one leading article, collapses whitespace", () => {
  assert.equal(normalize("The Red Wedding"), "red wedding");
  assert.equal(normalize("  Red   Wedding  "), "red wedding");
  assert.equal(normalize("A Storm of Swords"), "storm of swords");
  assert.equal(normalize("Death of Tywin"), "death of tywin");
});

Deno.test("normalize: keeps hyphens and quote/apostrophe characters", () => {
  // Slugs-as-phrases keep hyphens; some alias keys retain literal quotes.
  assert.equal(normalize("Ned's execution"), "ned's execution");
  assert.equal(normalize("war-of-the-usurper"), "war-of-the-usurper");
  assert.equal(normalize('"Aegon Targaryen"'), '"aegon targaryen"');
});

Deno.test("normalize: strips only the FIRST leading article", () => {
  // "the" inside the phrase survives; only a leading article is removed.
  assert.equal(normalize("the death of the Hand"), "death of the hand");
});

Deno.test("tokenize: drops stop words and interrogatives", () => {
  assert.deepEqual([...tokenize("who killed Eddard Stark")].sort(), [
    "eddard",
    "killed",
    "stark",
  ]);
  assert.deepEqual([...tokenize("death of Tywin")].sort(), ["death", "tywin"]);
});

Deno.test("intersectionSize: counts shared tokens", () => {
  assert.equal(intersectionSize(tokenize("death of tywin"), tokenize("tywin's death")), 2);
  assert.equal(intersectionSize(tokenize("red wedding"), tokenize("purple wedding")), 1);
});
