// Input validation — the tool layer is the trust boundary (design §3 / lib README).
// Every slug and phrase the model hands a retrieval tool is untrusted. We
// allowlist shapes here rather than throwing into the model loop: an invalid
// input yields an empty result, never an exception or an unbounded scan.

// Node slugs are kebab-case: lowercase alphanumerics + hyphens. Bounded length
// stops pathological inputs from driving large lookups.
const SLUG_RE = /^[a-z0-9][a-z0-9-]{0,199}$/;

/** True if `slug` is a well-formed node slug (kebab-case, ≤ 200 chars). */
export function isValidSlug(slug: unknown): slug is string {
  return typeof slug === "string" && SLUG_RE.test(slug);
}

const MAX_PHRASE_LEN = 200;

/**
 * Coerce an untrusted phrase to a safe string, or null if unusable.
 * Caps length so token-overlap scoring can't be driven by a huge input.
 */
export function cleanPhrase(phrase: unknown): string | null {
  if (typeof phrase !== "string") return null;
  const trimmed = phrase.trim();
  if (!trimmed) return null;
  return trimmed.slice(0, MAX_PHRASE_LEN);
}
