#!/usr/bin/env python3
"""stage4-quote-relevance-filter.py — Name-aware quote-relevance filter for Stage 4 edges.

An edge PASSES if its evidence_quote contains at least one name-token for the SOURCE
entity AND at least one name-token for the TARGET entity.  Otherwise it is DROPPED.

Token index is built from:
  - The slug itself (split on hyphens)
  - alias-resolver.json  (alias_to_canonical — all aliases pointing to each canonical slug)
  - pass1-derived-firstname-aliases.json  (firstname_to_slug)
  - pass1-derived-supplementary-aliases.json  (alias_to_canonical)

Matching is case-insensitive, whole-word (regex \\b).  Tokens <=2 chars and tokens in the
stoplist (GENERIC_TERMS from stage4_name_resolver + common function words) are silently
ignored for matching purposes.

SANITY: "arya-stark LOVES jon-snow" with evidence_quote="Jon told Arya" MUST pass because
"Jon" matches a token for jon-snow and "Arya" matches a token for arya-stark.

CLI usage:
    python3 scripts/stage4-quote-relevance-filter.py \\
        --input path/to/edges.jsonl \\
        [--kept   path/to/kept.jsonl] \\
        [--dropped path/to/dropped.jsonl] \\
        [--report  path/to/report.md] \\
        [--quote-field evidence_quote]   # default: evidence_quote

The script NEVER writes to --input; NEVER writes into graph/edges/ or any canonical dir.

Importable:
    from scripts.stage4_quote_relevance_filter import (
        build_slug_token_index, build_stoplist, quote_relevance_pass
    )
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Repo / data paths (resolved at module load)
# ---------------------------------------------------------------------------

_REPO = Path(__file__).resolve().parent.parent
_WIKI_DATA = _REPO / "working" / "wiki" / "data"
_ALIAS_RESOLVER    = _WIKI_DATA / "alias-resolver.json"
_FIRSTNAME_ALIASES = _WIKI_DATA / "pass1-derived-firstname-aliases.json"
_SUPP_ALIASES      = _WIKI_DATA / "pass1-derived-supplementary-aliases.json"

# ---------------------------------------------------------------------------
# Load GENERIC_TERMS stoplist from stage4_name_resolver (importlib, hyphen-safe)
# ---------------------------------------------------------------------------

def _load_name_resolver() -> object:
    mod_path = _REPO / "scripts" / "stage4_name_resolver.py"
    spec = importlib.util.spec_from_file_location("stage4_name_resolver", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_stoplist() -> frozenset[str]:
    """Return the combined token stoplist.

    Merges GENERIC_TERMS from stage4_name_resolver with a small set of
    common English function words that must never count as a name match.
    """
    try:
        nr = _load_name_resolver()
        generic_terms: frozenset[str] = nr.GENERIC_TERMS
    except Exception as exc:
        print(f"[warn] Could not load GENERIC_TERMS from stage4_name_resolver: {exc}",
              file=sys.stderr)
        generic_terms = frozenset()

    # Common English function words / titles that must NEVER match an entity
    _EXTRA_STOPWORDS: frozenset[str] = frozenset({
        "the", "a", "an", "of", "and", "or", "in", "at", "to", "for",
        "is", "was", "had", "has", "have", "be", "been", "by",
        "his", "her", "him", "she", "he", "they", "them", "their",
        "it", "its", "we", "our", "i", "my",
        "that", "this", "with", "from", "as", "on", "not", "but",
        # Titles (also in GENERIC_TERMS but repeated for clarity)
        "king", "queen", "lord", "lady", "ser",
        # Direction words sometimes near names
        "said", "told", "asked",
    })

    return generic_terms | _EXTRA_STOPWORDS


# ---------------------------------------------------------------------------
# Slug tokeniser
# ---------------------------------------------------------------------------

def _slug_tokens(slug: str) -> list[str]:
    """Split a kebab slug into individual lowercase tokens."""
    return [t for t in slug.split("-") if t]


def _is_useful_token(tok: str, stoplist: frozenset[str]) -> bool:
    """Return True if tok is a valid matching token (len > 2, not in stoplist)."""
    return len(tok) > 2 and tok.lower() not in stoplist


# ---------------------------------------------------------------------------
# Alias file loaders
# ---------------------------------------------------------------------------

def _load_alias_resolver(path: Path) -> dict[str, str]:
    """Load alias-resolver.json -> {alias_slug: canonical_slug}."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("alias_to_canonical", {})
    except Exception as exc:
        print(f"[warn] Could not load alias-resolver from {path}: {exc}", file=sys.stderr)
        return {}


def _load_firstname_aliases(path: Path) -> dict[str, str]:
    """Load pass1-derived-firstname-aliases.json -> {firstname_tok: canonical_slug}."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("firstname_to_slug", {})
    except Exception as exc:
        print(f"[warn] Could not load firstname-aliases from {path}: {exc}", file=sys.stderr)
        return {}


def _load_supplementary_aliases(path: Path) -> dict[str, str]:
    """Load pass1-derived-supplementary-aliases.json -> {alias_slug: canonical_slug}."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("alias_to_canonical", {})
    except Exception as exc:
        print(f"[warn] Could not load supplementary-aliases from {path}: {exc}", file=sys.stderr)
        return {}


# ---------------------------------------------------------------------------
# Index builder
# ---------------------------------------------------------------------------

def build_slug_token_index(
    slugs: Optional[list[str]] = None,
    *,
    alias_resolver_path: Path = _ALIAS_RESOLVER,
    firstname_aliases_path: Path = _FIRSTNAME_ALIASES,
    supp_aliases_path: Path = _SUPP_ALIASES,
    stoplist: Optional[frozenset[str]] = None,
) -> dict[str, frozenset[str]]:
    """Build a slug -> frozenset[matching_token] index.

    For every slug S the index accumulates:
      1. Tokens from the slug itself (split on hyphens)
      2. Tokens from every alias-key that resolves to S (from all three alias files)
      3. Firstname-alias keys that resolve to S (the key token itself)

    Only tokens that pass _is_useful_token (len > 2, not in stoplist) are kept.

    Args:
        slugs: If provided, only build index entries for these slugs.
               If None, build from all slugs seen across alias files.
        alias_resolver_path, firstname_aliases_path, supp_aliases_path: override paths.
        stoplist: Pre-built stoplist; if None, calls build_stoplist().

    Returns:
        {slug: frozenset[lowercase_token]}
    """
    if stoplist is None:
        stoplist = build_stoplist()

    # Load all alias maps
    a2c_main = _load_alias_resolver(alias_resolver_path)
    fn2slug  = _load_firstname_aliases(firstname_aliases_path)
    a2c_supp = _load_supplementary_aliases(supp_aliases_path)

    # Collect all canonical slugs we need to index.
    all_canonicals: set[str] = set()
    if slugs is not None:
        all_canonicals.update(slugs)
    else:
        all_canonicals.update(a2c_main.values())
        all_canonicals.update(fn2slug.values())
        all_canonicals.update(a2c_supp.values())

    # For each canonical slug, accumulate matching tokens
    index: dict[str, set[str]] = {s: set() for s in all_canonicals}

    def _add_tokens(canonical: str, source_slug: str) -> None:
        """Add useful tokens from source_slug into canonical's token set."""
        if canonical not in index:
            return
        for tok in _slug_tokens(source_slug):
            if _is_useful_token(tok, stoplist):
                index[canonical].add(tok.lower())

    # 1. Tokens from each canonical slug itself
    for slug in all_canonicals:
        _add_tokens(slug, slug)

    # 2. Tokens from alias keys (alias-resolver + supplementary)
    for alias_slug, canonical in a2c_main.items():
        if canonical in index:
            _add_tokens(canonical, alias_slug)

    for alias_slug, canonical in a2c_supp.items():
        if canonical in index:
            _add_tokens(canonical, alias_slug)

    # 3. Firstname aliases — the key IS the single-token firstname.
    #    Register the key token as a matching token for the canonical slug.
    for firstname_tok, canonical in fn2slug.items():
        if canonical not in index:
            if slugs is None:
                index[canonical] = set()
            else:
                continue
        if _is_useful_token(firstname_tok, stoplist):
            index[canonical].add(firstname_tok.lower())
        # Also seed the canonical slug's own tokens (idempotent)
        _add_tokens(canonical, canonical)

    # Convert to frozensets
    return {s: frozenset(toks) for s, toks in index.items()}


# ---------------------------------------------------------------------------
# Core filter predicate
# ---------------------------------------------------------------------------

def _tokens_present_in_quote(tokens: frozenset[str], quote: str) -> list[str]:
    """Return the list of tokens that appear in quote as whole words (case-insensitive)."""
    q_lower = quote.lower()
    hits: list[str] = []
    for tok in tokens:
        if re.search(r'\b' + re.escape(tok) + r'\b', q_lower):
            hits.append(tok)
    return hits


def quote_relevance_pass(
    row: dict,
    slug_token_index: dict[str, frozenset[str]],
    stoplist: frozenset[str],
    *,
    quote_field: str = "evidence_quote",
) -> tuple[bool, str]:
    """Test whether an edge row passes the quote-relevance filter.

    An edge PASSES if its evidence_quote contains >=1 name-token for the
    SOURCE entity AND >=1 name-token for the TARGET entity.

    Returns:
        (True,  reason_string)  — PASS
        (False, reason_string)  — DROP
    """
    src   = (row.get("source_slug") or "").strip()
    tgt   = (row.get("target_slug") or "").strip()
    quote = (row.get(quote_field) or "").strip()

    if not src or not tgt:
        return False, "MISSING_ENDPOINT: source or target slug is empty"

    if not quote:
        return False, "NO_QUOTE: evidence_quote is empty"

    def _get_tokens(slug: str) -> tuple[frozenset[str], bool]:
        """Return (tokens, is_fallback).  is_fallback=True when slug not in index."""
        if slug in slug_token_index:
            toks = slug_token_index[slug]
            if toks:
                return toks, False
        # Fallback: slug's own tokens minus stoplist
        fallback = frozenset(
            t.lower() for t in _slug_tokens(slug)
            if _is_useful_token(t, stoplist)
        )
        return fallback, True

    src_tokens, src_fallback = _get_tokens(src)
    tgt_tokens, tgt_fallback = _get_tokens(tgt)

    # Slugs that produce zero usable tokens are UNMATCHABLE -> DROP
    if not src_tokens:
        return False, f"UNMATCHABLE_SOURCE: {src!r} has no usable tokens"
    if not tgt_tokens:
        return False, f"UNMATCHABLE_TARGET: {tgt!r} has no usable tokens"

    src_hits = _tokens_present_in_quote(src_tokens, quote)
    tgt_hits = _tokens_present_in_quote(tgt_tokens, quote)

    src_matched = bool(src_hits)
    tgt_matched = bool(tgt_hits)

    if src_matched and tgt_matched:
        detail = f"src_hit={src_hits[0]!r}, tgt_hit={tgt_hits[0]!r}"
        if src_fallback or tgt_fallback:
            detail += " (fallback)"
        return True, f"PASS: {detail}"

    if not src_matched and not tgt_matched:
        return False, f"UNMATCHED_BOTH: src={src!r} tgt={tgt!r}"
    if not src_matched:
        return False, f"UNMATCHED_SOURCE: {src!r}"
    return False, f"UNMATCHED_TARGET: {tgt!r}"


# ---------------------------------------------------------------------------
# JSONL I/O helpers
# ---------------------------------------------------------------------------

def _read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with open(path, encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                rows.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                print(f"[warn] {path}:{lineno}: JSON parse error: {exc}", file=sys.stderr)
    return rows


def _write_jsonl(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Report generator
# ---------------------------------------------------------------------------

def _build_report(
    input_path: Path,
    total: int,
    kept_rows: list[dict],
    dropped_rows: list[dict],
    quote_field: str,
) -> str:
    kept    = len(kept_rows)
    dropped = len(dropped_rows)
    drop_rate = (dropped / total * 100) if total else 0.0

    lines: list[str] = [
        "# Quote-Relevance Filter Report",
        "",
        f"**Input:** `{input_path}`  ",
        f"**Total:** {total}  **Kept:** {kept}  **Dropped:** {dropped}  "
        f"**Drop rate:** {drop_rate:.1f}%",
        "",
        "---",
        "",
        "## Dropped Rows",
        "",
    ]

    if not dropped_rows:
        lines.append("_No rows dropped._")
    else:
        lines.append("Format: `src --EDGE--> tgt | \"<quote excerpt>\" | reason`")
        lines.append("")
        for row in dropped_rows:
            src = row.get("source_slug", "?")
            tgt = row.get("target_slug", "?")
            et  = row.get("edge_type", "?")
            quote_raw    = (row.get(quote_field) or "").strip()
            quote_excerpt = quote_raw[:80].replace("\n", " ")
            reason = row.get("_filter_reason", "?")
            lines.append(f"- `{src} --{et}--> {tgt}` | \"{quote_excerpt}\" | {reason}")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Quote-relevance filter for Stage 4 edges.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input",       required=True, help="Input JSONL file (read-only)")
    parser.add_argument("--kept",        default=None,  help="Write kept rows here")
    parser.add_argument("--dropped",     default=None,  help="Write dropped rows here")
    parser.add_argument("--report",      default=None,  help="Write markdown report here")
    parser.add_argument("--quote-field", default="evidence_quote",
                        help="JSON field containing the evidence quote (default: evidence_quote)")
    args = parser.parse_args(argv)

    input_path = Path(args.input)

    # Safety: never write to graph/edges/ or overwrite input
    _REPO_EDGES = _REPO / "graph" / "edges"
    for out_path_str in [args.kept, args.dropped, args.report]:
        if out_path_str is None:
            continue
        out_p = Path(out_path_str).resolve()
        if out_p == input_path.resolve():
            sys.exit(f"ERROR: output path must not be the same as --input: {out_p}")
        try:
            out_p.relative_to(_REPO_EDGES)
            sys.exit(f"ERROR: output path must not be inside graph/edges/: {out_p}")
        except ValueError:
            pass

    # Build index
    print("Building slug-token index…", file=sys.stderr)
    stoplist = build_stoplist()
    rows     = _read_jsonl(input_path)
    all_slugs = list({r.get("source_slug", "") for r in rows} |
                     {r.get("target_slug", "") for r in rows})
    slug_token_index = build_slug_token_index(
        slugs=all_slugs, stoplist=stoplist
    )
    print(f"  Index covers {len(slug_token_index)} slugs", file=sys.stderr)

    # Filter
    kept_rows: list[dict] = []
    dropped_rows: list[dict] = []

    for row in rows:
        passed, reason = quote_relevance_pass(
            row, slug_token_index, stoplist, quote_field=args.quote_field
        )
        if passed:
            kept_rows.append(row)
        else:
            annotated = dict(row)
            annotated["_filter_reason"] = reason
            dropped_rows.append(annotated)

    total    = len(rows)
    kept     = len(kept_rows)
    dropped  = len(dropped_rows)
    drop_rate = (dropped / total * 100) if total else 0.0

    # Write outputs
    if args.kept:
        _write_jsonl(kept_rows, Path(args.kept))
        print(f"Kept rows    -> {args.kept}", file=sys.stderr)

    if args.dropped:
        _write_jsonl(dropped_rows, Path(args.dropped))
        print(f"Dropped rows -> {args.dropped}", file=sys.stderr)

    if args.report:
        report_md = _build_report(
            input_path, total, kept_rows, dropped_rows, args.quote_field
        )
        rp = Path(args.report)
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(report_md, encoding="utf-8")
        print(f"Report       -> {args.report}", file=sys.stderr)

    # Summary
    print(f"\nQuote-relevance filter summary")
    print(f"  Input:     {input_path} ({total} rows)")
    print(f"  Kept:      {kept}")
    print(f"  Dropped:   {dropped}")
    print(f"  Drop rate: {drop_rate:.1f}%")


if __name__ == "__main__":
    main()
