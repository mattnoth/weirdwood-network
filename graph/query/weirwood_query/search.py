"""search.py — content-first retrieval over node quotes + identity blurbs
(query-layer Track, step 5b; design.md D-C, "the headline capability").

Answers descriptive/thematic/quote-hunting questions ("describe some detailed
meals", "what do people say about honor") that `resolve`+`chain` cannot reach
— those require an entity slug up front; `search` is content-first, scoring
free text against the build-time inverted index (`build/build_search_index.py`,
step 5a) with BM25-ish ranking (formula documented in that module's docstring
— this module implements the SAME formula, reading the SAME `idf`/`postings`/
`doc_lengths`/`avgdl` tables that build wrote, never re-deriving them).

Two on-disk index formats exist (see build_search_index.py's docstring):
  - "full"    — working/wiki/data/search-index.json (dict-of-dicts, text inline)
  - "compact" — web/data/search-index.json (array-based, delta-encoded
                postings; `text` not carried, reconstructed from a nodes-map)
`category` (the graph/nodes/ type-directory name, e.g. "foods" — the value
`--type`/`node_type` filters against) IS carried inline in both formats; only
display `text` needs a nodes-map to reconstruct in the compact format.

This module's `search()` accepts EITHER format transparently
(`_normalize_index` detects `index["format"]` and decodes compact -> the same
internal shape "full" already is), so the same function serves both the CLI
(reads the full-format working/ copy) and any future in-repo caller of the
compact bundle copy. The compact format's `text` reconstruction requires a
`nodes_map` (slug -> node record with `.identity` / `.quotes[]`) — supply the
live graph's nodes.json-shaped dict, or leave doc text as `None` if
unavailable (score/slug/category/cite are still returned; only the display
text is missing).

No LLM in the loop. Ever.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .load import REPO_ROOT
from .normalize import STOP_WORDS

WORKING_INDEX_FILE = REPO_ROOT / "working" / "wiki" / "data" / "search-index.json"
BUNDLE_INDEX_FILE = REPO_ROOT / "web" / "data" / "search-index.json"

DEFAULT_LIMIT = 12
MIN_TOKEN_LEN = 2

_KIND_BY_CODE = {0: "quote", 1: "identity"}


def _query_tokens(query: str) -> list[str]:
    """Tokenize a query with the exact same rule build_search_index.py used
    to tokenize docs (word-chars, lowercased, stop-words removed, min length
    2) — NOT normalize.tokenize()'s de-duped set, since a repeated query term
    doesn't need repeat-counting for the query side of BM25 (only doc-side tf
    matters in the formula), but the token IDENTITY rule must match exactly
    or postings lookups silently miss."""
    raw = re.findall(r"\w+", query.lower())
    seen: list[str] = []
    seen_set: set[str] = set()
    for t in raw:
        if t in STOP_WORDS or len(t) < MIN_TOKEN_LEN:
            continue
        if t not in seen_set:
            seen_set.add(t)
            seen.append(t)
    return seen


def load_index(path: Path = WORKING_INDEX_FILE) -> dict[str, Any] | None:
    """Load a search-index.json (either format) from disk. Returns None if
    the file doesn't exist (caller decides whether that's fatal — mirrors
    load.py's alias-table loaders' "empty dict if missing" convention, except
    search has no sensible empty-index default, so this returns None rather
    than a would-be-misleading empty dict)."""
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _decode_compact_postings(flat: list[int]) -> list[tuple[int, int]]:
    """Reverse build_search_index.py's format_compact() flat delta encoding:
    [deltaDocId0, tf0, deltaDocId1, tf1, ...] -> [(doc_id0, tf0), (doc_id1, tf1), ...]."""
    pairs: list[tuple[int, int]] = []
    running = 0
    for i in range(0, len(flat), 2):
        running += flat[i]
        pairs.append((running, flat[i + 1]))
    return pairs


def _normalize_index(index: dict[str, Any]) -> dict[str, Any]:
    """Return an index in the internal working shape regardless of on-disk
    format: `postings: {token: [(doc_id, tf), ...]}`, `doc_lengths: {doc_id:
    length}`, `docs: {doc_id: {slug, category, kind, qidx, text, cite}}`
    (`text` is `None` for a compact-format index — see `_hydrate_text`)."""
    if index.get("format") == "compact":
        postings = {tok: _decode_compact_postings(flat) for tok, flat in index["postings"].items()}
        doc_lengths = {i: length for i, length in enumerate(index["doc_lengths"])}
        docs = {}
        for doc_id, row in enumerate(index["docs"]):
            slug, category, kind_code, qidx, cite = row
            docs[doc_id] = {
                "slug": slug, "category": category, "kind": _KIND_BY_CODE[kind_code],
                "qidx": qidx, "text": None, "cite": cite,
            }
        return {
            "n_docs": index["n_docs"], "avgdl": index["avgdl"], "idf": index["idf"],
            "postings": postings, "doc_lengths": doc_lengths, "docs": docs,
        }

    # "full" format (or untagged legacy) — already in the friendly shape,
    # just convert string doc_id keys back to ints and postings pairs to tuples.
    postings = {
        tok: [(int(doc_id), tf) for doc_id, tf in pairs]
        for tok, pairs in index["postings"].items()
    }
    doc_lengths = {int(k): v for k, v in index["doc_lengths"].items()}
    docs = {int(k): dict(v) for k, v in index["docs"].items()}
    return {
        "n_docs": index["n_docs"], "avgdl": index["avgdl"], "idf": index["idf"],
        "postings": postings, "doc_lengths": doc_lengths, "docs": docs,
    }


def _hydrate_text(doc: dict[str, Any], nodes_map: dict[str, Any] | None) -> str | None:
    """Reconstruct display `text` for a doc whose format didn't carry it
    inline (the compact bundle format). `nodes_map` is a slug -> node-record
    dict shaped like nodes.json (`.identity`, `.quotes[].text`)."""
    if doc.get("text") is not None:
        return doc["text"]
    if not nodes_map:
        return None
    rec = nodes_map.get(doc["slug"])
    if rec is None:
        return None
    if doc["kind"] == "identity":
        return rec.get("identity")
    qidx = doc.get("qidx")
    quotes = rec.get("quotes") or []
    if qidx is not None and 0 <= qidx < len(quotes):
        return quotes[qidx].get("text")
    return None


def _bm25_score(
    query_tokens: list[str],
    doc_id: int,
    idf: dict[str, float],
    postings_by_token: dict[str, dict[int, int]],
    doc_lengths: dict[int, int],
    avgdl: float,
    *,
    k1: float = 1.5,
    b: float = 0.75,
) -> float:
    """score(q,d) = sum over t in q of idf(t) * tf_sat(t,d) — see
    build_search_index.py's module docstring for the formula derivation.
    `postings_by_token[t]` is a {doc_id: tf} dict for token t (built once per
    query in `search()`, not per doc)."""
    doclen = doc_lengths.get(doc_id, 0)
    denom_const = k1 * (1 - b + b * (doclen / avgdl if avgdl else 0.0))
    total = 0.0
    for t in query_tokens:
        tf = postings_by_token.get(t, {}).get(doc_id)
        if not tf:
            continue
        tf_sat = tf * (k1 + 1) / (tf + denom_const)
        total += idf.get(t, 0.0) * tf_sat
    return total


def search(
    query: str,
    index: dict[str, Any] | None = None,
    *,
    index_path: Path = WORKING_INDEX_FILE,
    node_type: str | None = None,
    limit: int = DEFAULT_LIMIT,
    nodes_map: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Rank docs (quotes + identity blurbs) against `query`, BM25-ish.

    Returns up to `limit` `{slug, type, text, cite, score}` dicts, best-first
    (ties broken by doc_id ascending — deterministic, matches the build's
    walk order so re-running an identical query gives an identical order).
    The returned `type` field is the doc's `category` (graph/nodes/
    type-directory name, e.g. "foods") — see build_search_index.py's own
    comment on why this differs from the frontmatter `type:` scalar.
    `node_type` filters to one category (e.g. "foods") — applied BEFORE
    ranking so `limit` counts only matching-category hits, not filtered-out
    ones.

    Empty/whitespace query, or a query whose every token is a stop word / too
    short, returns `[]` (mirrors resolve()'s cleanPhrase trust-boundary
    convention — no exception on bad input).
    """
    if index is None:
        index = load_index(index_path)
    if index is None:
        return []

    norm = _normalize_index(index)
    query_tokens = _query_tokens(query)
    if not query_tokens:
        return []

    idf = norm["idf"]
    doc_lengths = norm["doc_lengths"]
    avgdl = norm["avgdl"]
    docs = norm["docs"]

    # Build {doc_id: tf} per query token once (not per candidate doc).
    postings_by_token: dict[str, dict[int, int]] = {}
    candidate_doc_ids: set[int] = set()
    for t in query_tokens:
        pairs = norm["postings"].get(t, [])
        postings_by_token[t] = dict(pairs)
        candidate_doc_ids.update(doc_id for doc_id, _ in pairs)

    if node_type is not None:
        candidate_doc_ids = {
            doc_id for doc_id in candidate_doc_ids
            if docs.get(doc_id, {}).get("category") == node_type
        }

    scored: list[tuple[float, int]] = []
    for doc_id in candidate_doc_ids:
        s = _bm25_score(query_tokens, doc_id, idf, postings_by_token, doc_lengths, avgdl)
        if s > 0:
            scored.append((s, doc_id))

    scored.sort(key=lambda p: (-p[0], p[1]))

    results: list[dict[str, Any]] = []
    for score, doc_id in scored[:limit]:
        doc = docs[doc_id]
        results.append({
            "slug": doc["slug"],
            "type": doc["category"],
            "text": _hydrate_text(doc, nodes_map),
            "cite": doc.get("cite"),
            "score": round(score, 4),
        })
    return results
