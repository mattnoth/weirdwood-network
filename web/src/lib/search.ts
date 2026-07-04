// searchQuotes(query) — content-first retrieval over node quotes + identity
// blurbs (query-layer Track, step 5b; design.md D-C, "the headline
// capability").
//
// Ports `graph/query/weirwood_query/search.py` against the SAME compact
// `search-index.json` shipped in the bundle (built by
// `graph/query/build/build_search_index.py` — see that module's docstring
// for the exact wire format and the BM25-ish formula this file implements
// verbatim: idf(t) * tf_saturation(t,d), k1=1.5, b=0.75). The compact format
// never carries `text`/full doc content inline (the dominant size trim that
// keeps the bundle under budget) — this file reconstructs display text from
// `data.nodes` (`.quotes[qidx].text` for a quote doc, `.identity` for an
// identity doc), which the caller already has loaded as part of GraphData.
//
// Tokenization: the SAME word pattern + stop-word set `normalize.ts` uses
// (imports `STOP` directly), but keeping term FREQUENCY (not `tokenize()`'s
// de-duped Set) — BM25 needs doc-side tf, and the query side needs the same
// token-identity rule so postings lookups don't silently miss. Any change to
// this tokenization rule must be mirrored in build_search_index.py AND
// search.py (see those files' own header comments) or the three engines
// silently diverge.
//
// No LLM in the loop, ever — pure data.

import type { GraphData, SearchIndexDocRow, SearchResult } from "./types.ts";
import { STOP } from "./normalize.ts";

const K1 = 1.5;
const B = 0.75;
const DEFAULT_LIMIT = 12;
const MIN_TOKEN_LEN = 2;

const WORD = /[\p{L}\p{N}_]+/gu;

const KIND_QUOTE = 0;
const KIND_IDENTITY = 1;

/** Tokenize a query: same word-splitting + stop-word rule as the build,
 * de-duplicated (only token IDENTITY matters on the query side of BM25 —
 * `tf` is a doc-side-only concept in the formula). */
function queryTokens(query: string): string[] {
  const seen = new Set<string>();
  const out: string[] = [];
  for (const m of query.toLowerCase().matchAll(WORD)) {
    const t = m[0];
    if (STOP.has(t) || t.length < MIN_TOKEN_LEN) continue;
    if (!seen.has(t)) {
      seen.add(t);
      out.push(t);
    }
  }
  return out;
}

/** Decode build_search_index.py's format_compact() flat delta encoding:
 * [deltaDocId0, tf0, deltaDocId1, tf1, ...] -> Map<docId, tf>. */
function decodePostings(flat: number[]): Map<number, number> {
  const out = new Map<number, number>();
  let running = 0;
  for (let i = 0; i < flat.length; i += 2) {
    running += flat[i];
    out.set(running, flat[i + 1]);
  }
  return out;
}

/** Reconstruct a doc's display text from the loaded node bundle — the
 * compact index never carries `text` inline (see module header comment). */
function hydrateText(row: SearchIndexDocRow, data: GraphData): string | null {
  const [slug, , kindCode, qidx] = row;
  const rec = data.nodes[slug];
  if (!rec) return null;
  if (kindCode === KIND_IDENTITY) return rec.identity ?? null;
  if (kindCode === KIND_QUOTE && qidx !== null && qidx >= 0 && qidx < rec.quotes.length) {
    return rec.quotes[qidx].text ?? null;
  }
  return null;
}

/**
 * Rank quotes + identity blurbs against `query`, BM25-ish. Returns up to
 * `opts.limit` (default 12) `{slug, type, text, cite, score}` results,
 * best-first (ties broken by doc_id ascending — deterministic). `opts.type`
 * filters to one node category (e.g. "foods" — the graph/nodes/
 * type-directory name; see `SearchIndexDocRow`'s comment) BEFORE ranking, so
 * `limit` counts only matching-category hits.
 *
 * Empty/whitespace query, or a query whose every token is a stop word / too
 * short, returns `[]` — no exception on bad input (mirrors resolve()'s
 * cleanPhrase trust-boundary convention).
 */
export function searchQuotes(
  query: string,
  data: GraphData,
  opts?: { type?: string; limit?: number },
): SearchResult[] {
  const tokens = queryTokens(query);
  if (tokens.length === 0) return [];

  const index = data.searchIndex;
  if (!index) return [];
  const { idf, doc_lengths: docLengths, avgdl, docs, postings } = index;
  const limit = opts?.limit ?? DEFAULT_LIMIT;
  const typeFilter = opts?.type;

  // Build {docId -> tf} per query token once (not per candidate doc).
  const postingsByToken = new Map<string, Map<number, number>>();
  const candidateDocIds = new Set<number>();
  for (const t of tokens) {
    const decoded = decodePostings(postings[t] ?? []);
    postingsByToken.set(t, decoded);
    for (const docId of decoded.keys()) candidateDocIds.add(docId);
  }

  let candidates = [...candidateDocIds];
  if (typeFilter !== undefined) {
    candidates = candidates.filter((docId) => docs[docId][1] === typeFilter);
  }

  const scored: Array<[number, number]> = []; // [score, docId]
  for (const docId of candidates) {
    const doclen = docLengths[docId] ?? 0;
    const denomConst = K1 * (1 - B + B * (avgdl ? doclen / avgdl : 0));
    let total = 0;
    for (const t of tokens) {
      const tf = postingsByToken.get(t)?.get(docId);
      if (!tf) continue;
      const tfSat = (tf * (K1 + 1)) / (tf + denomConst);
      total += (idf[t] ?? 0) * tfSat;
    }
    if (total > 0) scored.push([total, docId]);
  }

  scored.sort((a, b) => b[0] - a[0] || a[1] - b[1]);

  const results: SearchResult[] = [];
  for (const [score, docId] of scored.slice(0, limit)) {
    const row = docs[docId];
    const [slug, category, , , cite] = row;
    results.push({
      slug,
      type: category,
      text: hydrateText(row, data),
      cite: cite ?? null,
      score: Math.round(score * 10000) / 10000,
    });
  }
  return results;
}
