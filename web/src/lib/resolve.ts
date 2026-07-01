// resolve(phrase) — natural-language phrase -> candidate node slug(s).
//
// Ports the resolution logic of scripts/event_alias_resolver.py against the
// pre-merged bundle alias-map.json (phrase -> [{slug, category}]). The bundle
// already folds the event-alias table + all-node index into one map, so this is
// the two-step the handoff specifies:
//   1. exact normalized lookup in alias-map.json
//   2. fuzzy/substring fallback: token-overlap ≥ 0.5 against every phrase key
//
// No LLM in the loop, ever — pure data.

import type { GraphData, ResolveCandidate } from "./types.ts";
import { intersectionSize, normalize, tokenize } from "./normalize.ts";
import { cleanPhrase } from "./validate.ts";

// A candidate must share at least this fraction of the QUERY's tokens.
// Conservative: a confident wrong match is worse than a MISS (resolver design Q).
const MIN_FUZZY_SCORE = 0.5;
const MAX_FUZZY_CANDIDATES = 5;
// Per slug-token match, nudge a fuzzy score up so slug-named entities outrank
// nickname-only matches at equal phrase scores (mirrors the Python +0.05 bonus).
const SLUG_BONUS = 0.05;

/**
 * Resolve a phrase to ranked candidate nodes.
 *
 * Returns an exact hit's full candidate list (score 1.0, matchType "exact"), or
 * a ranked fuzzy list (token-overlap, matchType "fuzzy"), or `[]` on a miss /
 * invalid input. Each item is `{slug, category, score, matchType}` — a superset
 * of the `{slug, category}` contract.
 */
export function resolve(phrase: string, data: GraphData): ResolveCandidate[] {
  const safe = cleanPhrase(phrase);
  if (safe === null) return [];

  const norm = normalize(safe);

  // 1. Exact alias-map hit — return every candidate node for this phrase,
  //    ranked so a content-rich node outranks an empty bare-name stub (a shared
  //    name like "aemon targaryen" maps to several slugs; without this the flat
  //    1.0 score let insertion order surface the empty bucket).
  const exact = data.aliasMap[norm];
  if (exact && exact.length > 0) {
    const prom = prominenceMap(exact.map((c) => c.slug), data);
    return exact
      .map((c) => ({
        slug: c.slug,
        category: c.category,
        score: 1.0,
        matchType: "exact" as const,
        prominence: prom.get(c.slug) ?? 0,
      }))
      .sort((a, b) => b.prominence - a.prominence); // stable within equal prominence
  }

  // 2. Fuzzy fallback — token-overlap across every phrase key.
  return fuzzyCandidates(norm, data);
}

/**
 * Prominence (degree + 4·quoteCount) for a specific set of candidate slugs — the
 * same story-weight proxy familyTree() uses. Scoped to the candidates (one O(E)
 * pass, only when there's something to rank) rather than the whole graph.
 */
function prominenceMap(slugs: Iterable<string>, data: GraphData): Map<string, number> {
  const deg = new Map<string, number>();
  for (const s of slugs) deg.set(s, 0);
  if (deg.size === 0) return deg;
  for (const e of data.edges) {
    if (deg.has(e.source)) deg.set(e.source, deg.get(e.source)! + 1);
    if (deg.has(e.target)) deg.set(e.target, deg.get(e.target)! + 1);
  }
  const prom = new Map<string, number>();
  for (const s of deg.keys()) {
    const quoteCount = data.nodes[s]?.quotes?.length ?? 0;
    prom.set(s, deg.get(s)! + 4 * quoteCount);
  }
  return prom;
}

function fuzzyCandidates(norm: string, data: GraphData): ResolveCandidate[] {
  const queryTokens = tokenize(norm);
  if (queryTokens.size === 0) return [];

  // slug -> best score; slug -> category (first seen wins, matching the bundle's
  // dedupe-by-slug order in build_alias_map).
  const bestScore = new Map<string, number>();
  const categoryOf = new Map<string, string>();

  for (const [phrase, candidates] of Object.entries(data.aliasMap)) {
    const candTokens = tokenize(phrase);
    if (candTokens.size === 0) continue;
    const overlap = intersectionSize(queryTokens, candTokens);
    const base = overlap / queryTokens.size;
    if (base < MIN_FUZZY_SCORE) continue;

    for (const cand of candidates) {
      const slugTokens = tokenize(cand.slug.replace(/-/g, " "));
      const slugOverlap = intersectionSize(queryTokens, slugTokens);
      let score = base;
      if (slugOverlap > 0) score = Math.min(1.0, score + SLUG_BONUS * slugOverlap);
      if (score > (bestScore.get(cand.slug) ?? 0)) {
        bestScore.set(cand.slug, score);
      }
      if (!categoryOf.has(cand.slug)) categoryOf.set(cand.slug, cand.category);
    }
  }

  const prom = prominenceMap(bestScore.keys(), data);
  return [...bestScore.entries()]
    // score first, then prominence so an empty stub can't tie its way to the top
    .sort((a, b) => (b[1] - a[1]) || ((prom.get(b[0]) ?? 0) - (prom.get(a[0]) ?? 0)))
    .slice(0, MAX_FUZZY_CANDIDATES)
    .map(([slug, score]) => ({
      slug,
      category: categoryOf.get(slug) ?? "",
      score: Math.round(score * 1000) / 1000,
      matchType: "fuzzy" as const,
      prominence: prom.get(slug) ?? 0,
    }));
}
