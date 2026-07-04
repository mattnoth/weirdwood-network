#!/usr/bin/env python3
"""build_search_index.py — build-time inverted index over node quotes + identity
blurbs (query-layer Track, step 5a; design.md D-C).

Substrate (design.md D-C, decided): the curated, citable layer only — every
`## Quotes` line and every `## Identity` paragraph across `graph/nodes/`
(excluding `_conflicts/`, which holds unresolved duplicate candidates, not
live graph). Chapter full-text search is a SEPARATE, CLI-only capability
(`build/build_search_index.py` does not touch `sources/chapters/` — see
`weirwood_query/corpus_search.py`, step 5e).

Doc model: one doc per quote line (from `weirwood_query.load.parse_quotes`,
already used by build_chat_bundle.py) and one doc per node's whole `## Identity`
section body (a single paragraph doc, matching the step-0 measurement
methodology in working/query-layer/measurements.md so this build's counts are
directly comparable to that estimate). Each doc logically carries:
  {doc_id, slug, category, kind: "quote"|"identity", qidx, text, cite}
`category` is the graph/nodes/ type-directory name (e.g. "foods") — see
build_docs()'s own comment for why this is a DIFFERENT value from the
frontmatter `type:` scalar nodes.json exposes as `type` (e.g. "object.food").
`cite` is the `chapter:line` string when a quote carries one (attribution-line
regex match), else null. Identity docs never carry a cite (no per-paragraph
citation exists in node prose) — `search.py` falls back to `read <slug>` for
provenance on an identity hit. `qidx` is the 0-based position of a quote doc
within its node's OWN `## Quotes` list (identity docs carry `qidx: null`) —
this is the reconstruction key the bundle format uses (see below):
`nodes.json[slug].quotes[qidx].text` is byte-identical to this doc's `text`
(both come from the same `parse_quotes()` call over the same node body), so a
size-constrained consumer can drop `text` entirely and re-derive it from the
bundle it already has to load anyway.

Two on-disk FORMATS, same underlying docs/postings/idf (design.md 5a "two
outputs"):

1. **working/wiki/data/search-index.json — the FULL format.** Friendly
   dict-of-dicts shape, `text`/`category` inline, postings as `{token:
   [[doc_id, tf], ...]}`. Not size-constrained (this is the full-profile
   Python engine's own derived table, same tier as the alias-lookup tables
   it already reads from `working/wiki/data/`) — optimized for readability/
   debuggability, not bytes.

2. **web/data/search-index.json — the COMPACT bundle format.** Ships inside
   the chat bundle, so every structural trim in the budget matters (see
   "Trims" below). Same tokens/scoring, different wire encoding:
     - `docs`: an ARRAY (index == doc_id, not a `{"<id>": ...}` dict) of
       `[slug, category, kindCode, qidx_or_null, cite_or_null]` tuples, where
       `kindCode` is `0` for "quote", `1` for "identity", and `category` is
       the graph/nodes/ type-directory name (e.g. "foods" — cheap enough to
       carry inline; this is the field `search`'s `--type`/`node_type` filter
       matches, NOT the dotted frontmatter `type:` scalar nodes.json calls
       `type`, e.g. "object.food" — the two are different vocabularies, see
       build_docs()'s own comment). `text` is NOT carried — reconstruct via
       `nodes.json[slug].quotes[qidx].text` (kindCode 0) or
       `nodes.json[slug].identity` (kindCode 1).
     - `doc_lengths`: an ARRAY (index == doc_id) of token counts, not a dict.
     - `postings`: `{token: [deltaDocId0, tf0, deltaDocId1, tf1, ...]}` — a
       FLAT array (not array-of-pairs) of alternating (delta-encoded doc_id,
       tf). Doc ids within one token's postings are strictly increasing (the
       build's doc walk order), so `deltaDocId_i = doc_id_i - doc_id_{i-1}`
       (first entry's delta is the doc_id itself, i.e. delta from 0).
       Decoding: walk the flat array two-at-a-time, running-sum the deltas
       to recover doc_id, second element is tf.
     - `idf`: floats rounded to 4 decimal places (BM25 ranking is insensitive
       to the 5th+ decimal; this alone saves ~35% of the idf table's bytes).
   Both `search.py` (Python, reads whichever format is present at its own
   path) and `search.ts` (TS, reads ONLY this compact format, decoding as
   described) implement the SAME decode — see each file's own header comment.

Tokenizer: `weirwood_query.normalize.tokenize`'s word-splitting + stop-word
set (word-chars, lowercased) — the SAME tokenizer resolve.py uses, so search
and resolve share one notion of "token" (design.md instruction: "Tokenize
with the SAME normalizer semantics as normalize.py/normalize.ts"). This is
intentionally a STRICTER tokenizer than the step-0 measurement's raw
`[a-z0-9]+` split (that was a size estimate only) — stop-word removal here is
a deliberate trim (a query for "the guest right" and "guest right" should
retrieve identically, and stop words carry ~zero discriminative signal for
BM25-style scoring anyway).

Trims applied to hit the ≤2.5 MB bundle budget (documented per design.md 5a;
measured sizes reported by `main()` at build time — see that function's
docstring for the actual before/after numbers from the 2026-07-04 build):
  - stop-words dropped (via normalize.tokenize's STOP_WORDS)
  - minimum token length 2 (drops single-char tokens: stray initials, punct
    residue)
  - IDF rounded to 4 decimal places
  - **compact bundle format** (docs-as-array, doc_lengths-as-array,
    delta-encoded flat postings) — this was the dominant win, well past the
    slim-doc-store trim alone (dropping `text` from the bundle's doc store,
    reconstructing from `nodes.json` at request time).

BM25-ish formula (documented once, both engines implement exactly this):
  idf(t)      = ln(1 + (N - df(t) + 0.5) / (df(t) + 0.5))
  tf_sat(t,d) = tf(t,d) * (k1 + 1) / (tf(t,d) + k1 * (1 - b + b * (len(d) / avgdl)))
  score(q,d)  = sum over t in q of idf(t) * tf_sat(t,d)
  k1 = 1.5, b = 0.75  (standard Okapi BM25 defaults — no corpus-specific tuning
  yet; revisit only if eval scores show it's warranted)
`len(d)` = token count of doc d (post-tokenization, i.e. same units as tf).
`avgdl` = mean doc length across the whole index.

Determinism (design.md verify #5): nodes are walked in the same sorted order
`load.iter_all_nodes` already uses; doc_ids are assigned in that walk order
(node dir sort, then filename sort, then quotes-before-identity per node);
JSON is serialized with sorted dict keys (`sort_keys=True`) and no embedded
timestamps in the index body (a build could be stamped externally, matching
build_chat_bundle.py's manifest convention — this module does not do that
itself) — so building twice produces byte-identical files.

No LLM in the loop. Ever.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

_THIS_FILE = Path(__file__).resolve()
# <repo>/graph/query/build/build_search_index.py -> parents[0]=build,
# [1]=query, [2]=graph, [3]=<repo>
REPO_ROOT = _THIS_FILE.parents[3]

sys.path.insert(0, str(REPO_ROOT / "graph" / "query"))

from weirwood_query.load import (  # noqa: E402
    NODES_DIR,
    parse_frontmatter,
    parse_quotes,
    split_sections,
)
from weirwood_query.normalize import STOP_WORDS  # noqa: E402

WORKING_OUT = REPO_ROOT / "working" / "wiki" / "data" / "search-index.json"
BUNDLE_OUT = REPO_ROOT / "web" / "data" / "search-index.json"

MIN_TOKEN_LEN = 2
K1 = 1.5
B = 0.75
IDF_ROUND = 4

KIND_CODE = {"quote": 0, "identity": 1}


# ---------------------------------------------------------------------------
# Doc extraction
# ---------------------------------------------------------------------------

def _iter_node_files(nodes_dir: Path = NODES_DIR):
    """Sorted walk over every *.node.md, excluding `_conflicts/` (unresolved
    duplicate candidates, not live graph — same exclusion the step-0
    measurement script used)."""
    if not nodes_dir.exists():
        return
    for type_dir in sorted(nodes_dir.iterdir()):
        if not type_dir.is_dir() or type_dir.name == "_conflicts":
            continue
        for node_file in sorted(type_dir.glob("*.node.md")):
            yield type_dir.name, node_file


def build_docs(nodes_dir: Path = NODES_DIR) -> list[dict[str, Any]]:
    """Walk the graph deterministically and emit one doc per quote line + one
    doc per node's Identity section. doc_id = position in this walk (stable
    across runs given the sorted walk order)."""
    docs: list[dict[str, Any]] = []
    for category, node_file in _iter_node_files(nodes_dir):
        raw = node_file.read_text(encoding="utf-8")
        fields, body = parse_frontmatter(raw)
        if not fields and not raw.startswith("---"):
            continue
        fallback = node_file.name.replace(".node.md", "")
        slug = fields.get("slug") or fallback
        # `category` = the graph/nodes/ TYPE-DIRECTORY name (e.g. "foods") —
        # this is what --type/`node_type` filters match against (mirrors
        # resolve()'s `node_category` convention and the design doc's
        # `search "lemon cakes" --type foods` example), which is DIFFERENT
        # from the frontmatter `type:` scalar (e.g. "object.food", the
        # dotted category.subtype string nodes.json calls `type`). Both
        # values are cheap to carry; category is what search/list filter on.
        sections = split_sections(body)

        # qidx tracks position within THIS node's raw parse_quotes() output —
        # the same call, same order build_chat_bundle.py's load_nodes() makes
        # for nodes.json[slug]["quotes"], so qidx is a stable reconstruction
        # key into that array (see module docstring). parse_quotes() never
        # emits an empty-text entry, so this enumeration lines up 1:1.
        node_quotes = parse_quotes(sections.get("quotes", ""))
        for qidx, q in enumerate(node_quotes):
            text = (q.get("text") or "").strip()
            if not text:
                continue
            docs.append({
                "slug": slug,
                "category": category,
                "kind": "quote",
                "qidx": qidx,
                "text": text,
                "cite": q.get("cite"),
            })

        identity = sections.get("identity", "").strip()
        if identity:
            docs.append({
                "slug": slug,
                "category": category,
                "kind": "identity",
                "qidx": None,
                "text": identity,
                "cite": None,
            })

    for i, d in enumerate(docs):
        d["doc_id"] = i
    return docs


# ---------------------------------------------------------------------------
# Tokenization (term frequency, not just membership)
# ---------------------------------------------------------------------------

def _tokenize_with_counts(text: str) -> list[str]:
    """tokenize() returns a SET (unique tokens, for resolve()'s overlap-scoring
    use case) — search needs term FREQUENCY within a doc for BM25, so re-derive
    counts using the same word pattern + stop-word set tokenize() applies,
    without losing repeats. Mirrors weirwood_query.normalize.tokenize's regex/
    stop-word logic exactly (imports the SAME STOP_WORDS set, so the two never
    drift apart)."""
    raw_tokens = re.findall(r"\w+", text.lower())
    return [t for t in raw_tokens if t not in STOP_WORDS and len(t) >= MIN_TOKEN_LEN]


# ---------------------------------------------------------------------------
# Index build (shared core: postings / idf / doc_lengths)
# ---------------------------------------------------------------------------

def build_index_core(docs: list[dict[str, Any]]) -> dict[str, Any]:
    """Build the language-model core: per-doc token lists, doc frequencies,
    idf, avgdl. Both the full and compact formats are DERIVED from this same
    core (format_full / format_compact below) — the scoring math is identical
    either way; only the wire encoding differs."""
    doc_tokens: dict[int, list[str]] = {}
    doc_freq: Counter[str] = Counter()
    tf_by_doc: dict[int, Counter[str]] = {}

    for d in docs:
        tokens = _tokenize_with_counts(d["text"])
        doc_tokens[d["doc_id"]] = tokens
        tf = Counter(tokens)
        tf_by_doc[d["doc_id"]] = tf
        for token in tf:
            doc_freq[token] += 1

    n_docs = len(docs)
    doc_lengths = {doc_id: len(toks) for doc_id, toks in doc_tokens.items()}
    avgdl = (sum(doc_lengths.values()) / n_docs) if n_docs else 0.0

    idf = {
        token: round(math.log(1 + (n_docs - df + 0.5) / (df + 0.5)), IDF_ROUND)
        for token, df in doc_freq.items()
    }

    # token -> [(doc_id, tf), ...] sorted by doc_id (the doc walk is already
    # sorted, so this is a no-op sort in practice — kept explicit so
    # determinism holds even if a future caller builds docs out of order).
    postings_pairs: dict[str, list[tuple[int, int]]] = {}
    for doc_id, tf in tf_by_doc.items():
        for token, count in tf.items():
            postings_pairs.setdefault(token, []).append((doc_id, count))
    for plist in postings_pairs.values():
        plist.sort(key=lambda p: p[0])

    return {
        "n_docs": n_docs,
        "avgdl": avgdl,
        "doc_lengths": doc_lengths,
        "idf": idf,
        "postings_pairs": postings_pairs,
    }


_FORMULA = {
    "name": "bm25",
    "k1": K1,
    "b": B,
    "idf": "ln(1 + (N - df + 0.5) / (df + 0.5))",
    "tf_saturation": "tf * (k1 + 1) / (tf + k1 * (1 - b + b * (doclen / avgdl)))",
    "score": "sum over query tokens of idf(t) * tf_saturation(t, d)",
}


def format_full(docs: list[dict[str, Any]], core: dict[str, Any]) -> dict[str, Any]:
    """Friendly dict-of-dicts encoding for working/wiki/data/search-index.json
    — text inline, postings as {token: [[doc_id, tf], ...]}, doc_lengths as
    a {"<doc_id>": length} dict. Not size-optimized; optimized for a human or
    a script reading this file directly without decoding a compact wire
    format first."""
    docs_out = {
        str(d["doc_id"]): {
            "slug": d["slug"], "category": d["category"], "kind": d["kind"],
            "qidx": d["qidx"], "text": d["text"], "cite": d["cite"],
        }
        for d in docs
    }
    postings_out = {
        token: [[doc_id, tf] for doc_id, tf in pairs]
        for token, pairs in core["postings_pairs"].items()
    }
    return {
        "format": "full",
        "formula": _FORMULA,
        "n_docs": core["n_docs"],
        "avgdl": core["avgdl"],
        "min_token_len": MIN_TOKEN_LEN,
        "docs": docs_out,
        "doc_lengths": {str(k): v for k, v in core["doc_lengths"].items()},
        "idf": core["idf"],
        "postings": postings_out,
    }


def format_compact(docs: list[dict[str, Any]], core: dict[str, Any]) -> dict[str, Any]:
    """Compact array-based encoding for web/data/search-index.json — see the
    module docstring's "COMPACT bundle format" section for the exact shapes.
    `search.ts` and `search.py` (when reading this path) both decode this
    identically."""
    n_docs = core["n_docs"]

    docs_arr: list[list[Any]] = [None] * n_docs  # type: ignore[list-item]
    for d in docs:
        docs_arr[d["doc_id"]] = [d["slug"], d["category"], KIND_CODE[d["kind"]], d["qidx"], d["cite"]]

    doc_lengths_arr = [0] * n_docs
    for doc_id, length in core["doc_lengths"].items():
        doc_lengths_arr[doc_id] = length

    postings_out: dict[str, list[int]] = {}
    for token, pairs in core["postings_pairs"].items():
        flat: list[int] = []
        prev = 0
        for doc_id, tf in pairs:
            flat.append(doc_id - prev)
            flat.append(tf)
            prev = doc_id
        postings_out[token] = flat

    return {
        "format": "compact",
        "formula": _FORMULA,
        "n_docs": n_docs,
        "avgdl": core["avgdl"],
        "min_token_len": MIN_TOKEN_LEN,
        "docs": docs_arr,
        "doc_lengths": doc_lengths_arr,
        "idf": core["idf"],
        "postings": postings_out,
    }


def write_index(index: dict[str, Any], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    # sort_keys=True + no trailing whitespace + fixed separators -> byte-
    # identical output across repeated builds (determinism, verify #5).
    text = json.dumps(index, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    path.write_text(text, encoding="utf-8")
    return len(text.encode("utf-8"))


def human(nbytes: float) -> str:
    for unit in ("B", "KB", "MB"):
        if nbytes < 1024 or unit == "MB":
            return f"{nbytes:.1f}{unit}" if unit != "B" else f"{nbytes:.0f}B"
        nbytes /= 1024
    return f"{nbytes:.1f}MB"


def main() -> int:
    """Build both formats and report doc/token counts + on-disk sizes.

    2026-07-04 measured sizes (this build, this corpus): 13,714 docs (6,057
    quote + 7,657 identity), 17,520 unique tokens. Full format (working/):
    ~6.9 MB. Compact format (web/data/, the one that matters for budget):
    ~2.3 MB — under the ≤2.5 MB budget. (An earlier iteration of this script
    used a friendly dict-of-dicts encoding for BOTH outputs and a slimmed-
    but-still-dict doc store for the bundle; those measured ~6.7 MB and
    ~4.1 MB respectively — the array-based compact format + delta-encoded
    postings + rounded idf in `format_compact` above is what closed the gap.)
    """
    ap = argparse.ArgumentParser(description="Build the quote+identity inverted search index.")
    ap.add_argument(
        "--working-out", default=None,
        help="Override the working/wiki/data path (full format, text inline).",
    )
    ap.add_argument(
        "--bundle-out", default=None,
        help="Override the web/data path (compact array format — text "
        "dropped, reconstructed from nodes.json at request time).",
    )
    args = ap.parse_args()

    print("Building search index ...")
    docs = build_docs()
    n_quote = sum(1 for d in docs if d["kind"] == "quote")
    n_identity = sum(1 for d in docs if d["kind"] == "identity")
    print(f"  docs: {len(docs)} total ({n_quote} quote, {n_identity} identity)")

    core = build_index_core(docs)
    print(f"  tokens (unique): {len(core['postings_pairs'])}")
    print(f"  avgdl: {core['avgdl']:.2f}")

    working_out = Path(args.working_out) if args.working_out else WORKING_OUT
    bundle_out = Path(args.bundle_out) if args.bundle_out else BUNDLE_OUT

    full_index = format_full(docs, core)
    size_working = write_index(full_index, working_out)
    print(f"  wrote {working_out}  (full format, {human(size_working)})")

    compact_index = format_compact(docs, core)
    size_bundle = write_index(compact_index, bundle_out)
    print(f"  wrote {bundle_out}  (compact format, {human(size_bundle)})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
