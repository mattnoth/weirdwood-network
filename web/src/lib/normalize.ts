// Phrase normalization + tokenization.
//
// Ported verbatim from scripts/event_alias_resolver.py (normalize + tokenize).
// The alias-map.json keys were produced by that same normalize(), so a query
// MUST be normalized identically here or exact lookups silently miss. Critically
// this keeps hyphens and does NOT strip quotes/apostrophes (memory
// project_node_alias_spaced_phrases): some keys retain literal quote chars.

const LEADING_ARTICLE = /^(the|a|an)\s+/;
const WHITESPACE = /\s+/g;

/**
 * Normalize a natural-language phrase to a lookup key.
 *   1. lowercase + trim
 *   2. strip ONE leading article (a / an / the)
 *   3. collapse internal whitespace to single spaces
 * No kebab-casing, no quote stripping — keys are normalized phrases, not slugs.
 */
export function normalize(phrase: string): string {
  let p = phrase.toLowerCase().trim();
  p = p.replace(LEADING_ARTICLE, "");
  p = p.replace(WHITESPACE, " ").trim();
  return p;
}

// Stop words excluded from token-overlap scoring. Mirrors the Python set:
// articles/prepositions + interrogatives/auxiliaries, so "who killed X" and
// "X's death" share only the entity tokens.
const STOP: ReadonlySet<string> = new Set([
  "of",
  "the",
  "a",
  "an",
  "at",
  "in",
  "on",
  "by",
  "to",
  "and",
  "for",
  "s",
  "who",
  "what",
  "where",
  "when",
  "how",
  "which",
  "whom",
  "did",
  "does",
  "do",
  "is",
  "was",
  "were",
  "are",
  "has",
  "have",
  "had",
]);

// Python uses re.findall(r"\w+", ...) which is Unicode-aware on str; the closest
// JS equivalent is a Unicode property class (covers accented names).
const WORD = /[\p{L}\p{N}_]+/gu;

/** Split a phrase into a set of meaningful tokens (lowercased, stop words removed). */
export function tokenize(phrase: string): Set<string> {
  const tokens = new Set<string>();
  for (const m of phrase.toLowerCase().matchAll(WORD)) {
    const t = m[0];
    if (!STOP.has(t)) tokens.add(t);
  }
  return tokens;
}

/** Cardinality of the intersection of two sets. */
export function intersectionSize(a: Set<string>, b: Set<string>): number {
  let n = 0;
  // iterate the smaller set for speed
  const [small, big] = a.size <= b.size ? [a, b] : [b, a];
  for (const x of small) if (big.has(x)) n++;
  return n;
}
