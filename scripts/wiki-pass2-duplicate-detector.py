#!/usr/bin/env python3
"""Duplicate detector for Weirwood Network.

Scans graph/nodes/**/*.node.md (excluding _conflicts/, _unclassified/) and surfaces
candidate duplicates in three categories: shared-wiki-source, alias-bridge, slug-similarity.

Outputs:
  - working/wiki-pass2/duplicate-candidates.jsonl  (one candidate per line, sorted by confidence)
  - working/audits/duplicate-detector-stats-<UTC-DATE>.md  (summary)

Read-only on the graph. The downstream cross-identity-detector agent decides SAME_AS vs distinct.
"""

from __future__ import annotations
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
NODES_DIR = ROOT / "graph" / "nodes"
OUT_JSONL = ROOT / "working" / "wiki-pass2" / "duplicate-candidates.jsonl"
TODAY_UTC = datetime.now(timezone.utc).strftime("%Y-%m-%d")
STATS_MD = ROOT / "working" / "audits" / f"duplicate-detector-stats-{TODAY_UTC}.md"
QUESTIONS_JSONL = ROOT / "working" / "wiki-pass2" / "questions-for-matt.jsonl"

EXCLUDED_DIRS = {"_conflicts", "_unclassified"}

# Stop tokens commonly inserted/removed in slug variants
STOPLIST = {"of", "the", "a", "an"}


# ---------------- frontmatter parsing ----------------

def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm_text = text[3:end].strip("\n")
    return parse_yaml_block(fm_text)


def parse_yaml_block(s: str) -> dict:
    """Tiny YAML subset parser for node frontmatter."""
    data: dict = {}
    lines = s.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        m = re.match(r"^([A-Za-z_][\w_]*)\s*:\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val == "":
            i += 1
            items_list = []
            nested = {}
            while i < len(lines):
                nl = lines[i]
                if not nl.strip():
                    i += 1
                    continue
                if not nl.startswith(" ") and not nl.startswith("\t"):
                    break
                stripped = nl.strip()
                if stripped.startswith("- "):
                    items_list.append(strip_quotes(stripped[2:].strip()))
                else:
                    mm = re.match(r"^([A-Za-z_][\w_]*)\s*:\s*(.*)$", stripped)
                    if mm:
                        nested[mm.group(1)] = strip_quotes(mm.group(2).strip())
                i += 1
            if items_list:
                data[key] = items_list
            elif nested:
                data[key] = nested
            else:
                data[key] = None
        else:
            if val == "[]":
                data[key] = []
            else:
                data[key] = strip_quotes(val)
            i += 1
    return data


def strip_quotes(v: str) -> str:
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("\"", "'"):
        return v[1:-1]
    return v


# ---------------- normalization ----------------

def kebab(s: str) -> str:
    if not s:
        return ""
    s = s.lower().strip()
    s = re.sub(r"['’‘]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def strip_articles_kebab(slug: str) -> str:
    parts = [p for p in slug.split("-") if p and p not in STOPLIST]
    return "-".join(parts)


def levenshtein(a: str, b: str, cap: int = 4) -> int:
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if abs(la - lb) >= cap:
        return cap
    if la > lb:
        a, b = b, a
        la, lb = lb, la
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i] + [0] * lb
        min_in_row = cur[0]
        for j in range(1, lb + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
            if cur[j] < min_in_row:
                min_in_row = cur[j]
        if min_in_row >= cap:
            return cap
        prev = cur
    return prev[lb]


def top_type(t: str) -> str:
    return t.split(".", 1)[0] if t else ""


_ROMAN = re.compile(r"^[ivxlcdm]+$")


def is_ordinal_token(tok: str) -> bool:
    if tok.isdigit():
        return True
    if _ROMAN.match(tok):
        return True
    return False


def differs_only_by_ordinal(a: str, b: str) -> bool:
    pa, pb = a.split("-"), b.split("-")
    if len(pa) != len(pb):
        return False
    diffs = [(x, y) for x, y in zip(pa, pb) if x != y]
    if len(diffs) != 1:
        return False
    x, y = diffs[0]
    return is_ordinal_token(x) and is_ordinal_token(y)


def differs_by_disambig_segment(a: str, b: str) -> bool:
    for marker in ("son-of-", "daughter-of-", "the-elder", "the-younger", "wife-of-",
                   "husband-of-", "father-of-", "mother-of-"):
        if marker in a and marker in b:
            prefix_a = a.split(marker, 1)[0]
            prefix_b = b.split(marker, 1)[0]
            if prefix_a == prefix_b:
                return True
    return False


# ---------------- main scan ----------------

def main() -> int:
    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    STATS_MD.parent.mkdir(parents=True, exist_ok=True)
    QUESTIONS_JSONL.parent.mkdir(parents=True, exist_ok=True)

    nodes: list[dict] = []
    malformed: list[tuple[str, str]] = []

    files: list[Path] = []
    for root, dirs, fnames in os.walk(NODES_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for fn in fnames:
            if fn.endswith(".node.md"):
                files.append(Path(root) / fn)

    files.sort()
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            malformed.append((str(path), f"read-error: {e}"))
            continue
        fm = parse_frontmatter(text)
        if not fm:
            malformed.append((str(path), "no-frontmatter"))
            continue
        slug = fm.get("slug")
        name = fm.get("name")
        ntype = fm.get("type")
        aliases = fm.get("aliases") or []
        wiki_source = fm.get("wiki_source")
        if not slug or not name:
            malformed.append((str(path), "missing-slug-or-name"))
            continue
        if not isinstance(aliases, list):
            aliases = []
        nodes.append({
            "path": str(path),
            "slug": str(slug),
            "name": str(name),
            "type": str(ntype) if ntype else "",
            "aliases": [str(a) for a in aliases],
            "wiki_source": str(wiki_source) if wiki_source else "",
        })

    # ---------------- build indexes ----------------

    alias_index: dict[str, list[str]] = defaultdict(list)
    wiki_index: dict[str, list[str]] = defaultdict(list)

    for n in nodes:
        if n["wiki_source"]:
            wiki_index[n["wiki_source"]].append(n["slug"])
        name_keb = kebab(n["name"])
        if name_keb:
            alias_index[name_keb].append(n["slug"])
        for a in n["aliases"]:
            ak = kebab(a)
            if ak:
                alias_index[ak].append(n["slug"])

    by_slug: dict[str, dict] = {n["slug"]: n for n in nodes}

    # ---------------- collect candidates ----------------

    candidates: list[dict] = []
    seen_pair: set[tuple[str, str]] = set()

    def pair_key(a: str, b: str) -> tuple[str, str]:
        return (a, b) if a < b else (b, a)

    # Category 1: shared-wiki-source
    for url, slugs in wiki_index.items():
        if len(slugs) < 2:
            continue
        unique = sorted(set(slugs))
        for i in range(len(unique)):
            for j in range(i + 1, len(unique)):
                a, b = unique[i], unique[j]
                k = pair_key(a, b)
                if k in seen_pair:
                    continue
                seen_pair.add(k)
                candidates.append({
                    "category": "shared-wiki-source",
                    "node_a": a,
                    "node_b": b,
                    "wiki_source": url,
                    "confidence": "high",
                })

    # Category 2: alias-bridge
    for ak, slug_list in alias_index.items():
        unique = sorted(set(slug_list))
        if ak in by_slug and ak not in unique:
            unique.append(ak)
            unique.sort()
        if len(unique) < 2:
            continue
        for i in range(len(unique)):
            for j in range(i + 1, len(unique)):
                a, b = unique[i], unique[j]
                k = pair_key(a, b)
                if k in seen_pair:
                    continue
                ta = by_slug[a]["type"] if a in by_slug else ""
                tb = by_slug[b]["type"] if b in by_slug else ""
                if ta and tb and top_type(ta) != top_type(tb):
                    continue
                seen_pair.add(k)
                candidates.append({
                    "category": "alias-bridge",
                    "node_a": a,
                    "node_b": b,
                    "shared_alias_normalized": ak,
                    "confidence": "medium",
                })

    # Category 3a: slugs equal after stripping articles
    by_stripped: dict[str, list[str]] = defaultdict(list)
    for slug in by_slug:
        by_stripped[strip_articles_kebab(slug)].append(slug)

    for stripped, slugs in by_stripped.items():
        if len(slugs) < 2:
            continue
        unique = sorted(set(slugs))
        for i in range(len(unique)):
            for j in range(i + 1, len(unique)):
                a, b = unique[i], unique[j]
                if a == b:
                    continue
                k = pair_key(a, b)
                if k in seen_pair:
                    continue
                ta, tb = by_slug[a]["type"], by_slug[b]["type"]
                if ta and tb and top_type(ta) != top_type(tb):
                    continue
                seen_pair.add(k)
                candidates.append({
                    "category": "slug-similarity",
                    "node_a": a,
                    "node_b": b,
                    "edit_distance": levenshtein(a, b, cap=4),
                    "name_a": by_slug[a]["name"],
                    "name_b": by_slug[b]["name"],
                    "type_a": by_slug[a]["type"],
                    "type_b": by_slug[b]["type"],
                    "confidence": "low",
                    "subkind": "article-stripped-equal",
                })

    # Category 3b: pairwise Levenshtein bucketed by first char
    by_first: dict[str, list[str]] = defaultdict(list)
    for slug in by_slug:
        if slug:
            by_first[slug[0]].append(slug)
    for first_char, group in by_first.items():
        group.sort()
        for i in range(len(group)):
            a = group[i]
            for j in range(i + 1, len(group)):
                b = group[j]
                if abs(len(a) - len(b)) > 3:
                    continue
                d = levenshtein(a, b, cap=4)
                if d == 0 or d >= 4:
                    continue
                k = pair_key(a, b)
                if k in seen_pair:
                    continue
                ta, tb = by_slug[a]["type"], by_slug[b]["type"]
                if ta and tb and top_type(ta) != top_type(tb):
                    continue
                if differs_only_by_ordinal(a, b):
                    continue
                if differs_by_disambig_segment(a, b):
                    continue
                seen_pair.add(k)
                candidates.append({
                    "category": "slug-similarity",
                    "node_a": a,
                    "node_b": b,
                    "edit_distance": d,
                    "name_a": by_slug[a]["name"],
                    "name_b": by_slug[b]["name"],
                    "type_a": by_slug[a]["type"],
                    "type_b": by_slug[b]["type"],
                    "confidence": "low",
                })

    # ---------------- sort + write ----------------

    conf_rank = {"high": 0, "medium": 1, "low": 2}
    cat_rank = {"shared-wiki-source": 0, "alias-bridge": 1, "slug-similarity": 2}
    candidates.sort(key=lambda c: (conf_rank[c["confidence"]], cat_rank[c["category"]],
                                    c["node_a"], c["node_b"]))

    with OUT_JSONL.open("w", encoding="utf-8") as f:
        for c in candidates:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    if malformed:
        with QUESTIONS_JSONL.open("a", encoding="utf-8") as q:
            for path, reason in malformed:
                q.write(json.dumps({
                    "type": "node-malformed",
                    "path": path,
                    "reason": reason,
                    "raised_by": "duplicate-detector",
                    "raised_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                }) + "\n")

    # ---------------- spot-check known cross-identity ----------------

    cross_identity_known = [
        ("theon-greyjoy", "reek"),
        ("sansa-stark", "alayne-stone"),
        ("arya-stark", "cat-of-the-canals"),
        ("jaqen-h-ghar", "kindly-man"),
    ]
    cross_identity_present_pairs = [(a, b) for a, b in cross_identity_known
                                    if a in by_slug and b in by_slug]
    cross_identity_slugs: set[str] = set()
    for a, b in cross_identity_known:
        cross_identity_slugs.add(a)
        cross_identity_slugs.add(b)
    cross_identity_in_candidates = sum(
        1 for c in candidates
        if c["node_a"] in cross_identity_slugs or c["node_b"] in cross_identity_slugs
    )

    cat_counts: dict[str, int] = defaultdict(int)
    for c in candidates:
        cat_counts[c["category"]] += 1

    write_stats(
        nodes_count=len(nodes),
        cat_counts=dict(cat_counts),
        top10=candidates[:10],
        cross_identity_present_pairs=cross_identity_present_pairs,
        cross_identity_in_candidates=cross_identity_in_candidates,
        malformed_count=len(malformed),
        files_count=len(files),
        wiki_index_size=len(wiki_index),
        alias_index_size=len(alias_index),
    )

    print(f"nodes scanned: {len(nodes)}")
    print(f"candidates: {len(candidates)} "
          f"(shared-wiki-source={cat_counts.get('shared-wiki-source', 0)}, "
          f"alias-bridge={cat_counts.get('alias-bridge', 0)}, "
          f"slug-similarity={cat_counts.get('slug-similarity', 0)})")
    print(f"malformed nodes: {len(malformed)}")
    print(f"cross-identity present pairs: {len(cross_identity_present_pairs)}")
    print(f"  output: {OUT_JSONL}")
    print(f"  stats:  {STATS_MD}")
    return 0


def write_stats(*, nodes_count, cat_counts, top10, cross_identity_present_pairs,
                cross_identity_in_candidates, malformed_count, files_count,
                wiki_index_size, alias_index_size):
    lines = []
    lines.append(f"# Duplicate Detector Stats - {TODAY_UTC}")
    lines.append("")
    lines.append("Read-only audit of `graph/nodes/**/*.node.md` (excluding `_conflicts/`, `_unclassified/`).")
    lines.append("Output JSONL: `working/wiki-pass2/duplicate-candidates.jsonl`.")
    lines.append("")
    lines.append("## Scan summary")
    lines.append("")
    lines.append(f"- Node files discovered: {files_count}")
    lines.append(f"- Nodes successfully indexed: {nodes_count}")
    lines.append(f"- Malformed nodes (logged to `questions-for-matt.jsonl`): {malformed_count}")
    lines.append(f"- Distinct `wiki_source` URLs: {wiki_index_size}")
    lines.append(f"- Distinct normalized aliases / names: {alias_index_size}")
    lines.append("")
    lines.append("## Candidates by category")
    lines.append("")
    lines.append("| Category | Count | Confidence |")
    lines.append("|---|---|---|")
    lines.append(f"| shared-wiki-source | {cat_counts.get('shared-wiki-source', 0)} | high |")
    lines.append(f"| alias-bridge | {cat_counts.get('alias-bridge', 0)} | medium |")
    lines.append(f"| slug-similarity | {cat_counts.get('slug-similarity', 0)} | low |")
    total = sum(cat_counts.values())
    lines.append(f"| **total** | **{total}** | |")
    lines.append("")
    lines.append("## Top 10 candidates by confidence")
    lines.append("")
    if not top10:
        lines.append("_No candidates produced._")
    else:
        for i, c in enumerate(top10, 1):
            extra = ""
            if c["category"] == "shared-wiki-source":
                extra = f"shared wiki: `{c['wiki_source']}`"
            elif c["category"] == "alias-bridge":
                extra = f"alias-key: `{c['shared_alias_normalized']}`"
            else:
                extra = (f"edit-distance={c.get('edit_distance', '?')}; "
                         f"`{c.get('name_a', '')}` ({c.get('type_a', '')}) vs "
                         f"`{c.get('name_b', '')}` ({c.get('type_b', '')})")
            lines.append(f"{i}. **{c['confidence']}** - `{c['node_a']}` <-> `{c['node_b']}` "
                         f"[{c['category']}] - {extra}")
    lines.append("")
    lines.append("## Cross-identity spot-check")
    lines.append("")
    if cross_identity_present_pairs:
        lines.append("Confirmed present as separate nodes (handled by future `cross-identity-detector` agent):")
        lines.append("")
        for a, b in cross_identity_present_pairs:
            lines.append(f"- `{a}` and `{b}`")
    else:
        lines.append("None of the canonical cross-identity slug pairs found.")
    lines.append("")
    lines.append(f"Candidate rows touching cross-identity slugs: {cross_identity_in_candidates}")
    lines.append("")
    lines.append("## Estimated false-positive rate per category")
    lines.append("")
    lines.append("| Category | Heuristic FP rate | Rationale |")
    lines.append("|---|---|---|")
    lines.append("| shared-wiki-source | <5% | Same source URL is near-deterministic evidence both nodes parse the same wiki page; only false-positive class is intentional duplicate-from-different-bucket retention. |")
    lines.append("| alias-bridge | 30-50% | Cross-identity disguises (Theon/Reek, Sansa/Alayne) and canonical alias splits live here; the cross-identity-detector decides per pair. |")
    lines.append("| slug-similarity | 70-90% | Mostly namesakes (cousins/dynasties), houses with similar surnames, and ordinal numerals; cross-identity-detector rejects the bulk. |")
    lines.append("")
    lines.append("## Notes / patterns")
    lines.append("")
    lines.append("- Type mismatches (e.g., `character.*` vs `place.*`) are dropped before emission.")
    lines.append("- Pairs differing only in a Roman/Arabic ordinal token (e.g., `aegon-i-targaryen` vs `aegon-ii-targaryen`) are dropped - distinct dynasts, never duplicates.")
    lines.append("- Pairs disambiguated by `son-of-X` / `daughter-of-Y` / `wife-of-X` suffixes with the same prefix are dropped - explicitly-named namesakes.")
    lines.append("- `_conflicts/` and `_unclassified/` directories were excluded from the scan per the contract.")
    STATS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
