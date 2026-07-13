#!/usr/bin/env python3
"""theories-reground.py — S214 theories wave 1, step: re-grounding.

Every extracted evidence beat (working/theories/extractions/<id>.jsonl) is
matched against OUR chapter corpus (sources/chapters/) — ASX is the map, the
books are the truth. No beat mints on the video's authority alone.

Matcher lineage: norm()/build_corpus() are lifted from
scripts/upgrade-wiki-quote-cites.py (S213) so a matched cite passes
verify_node_quotes.py by construction. Two deterministic layers:

  1. exact — the beat's spoken_quote, normalized, appears exactly once
     corpus-wide (containment over wrap-joined lines).
  2. window — captions drift at the edges; try contiguous token windows of
     the quote (longest first, >= MIN_NORM_LEN normalized chars, >= 8 tokens)
     and accept the longest window with a UNIQUE corpus hit.

Statuses written per beat to working/theories/regrounding/<id>.jsonl:
  matched          — unique hit; carries cite + the verbatim corpus lines
  ambiguous        — quote appears 2+ places (stock phrases); needs a human/agent pick
  no-match         — had a spoken_quote but nothing unique found → agent residue
  needs-agent      — groundable domain but no spoken_quote (paraphrase only) → agent residue
  not-groundable   — show/grrm/twoiaf/community domain; kept for prose, never an edge cite
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CHAPTERS = REPO / "sources/chapters"
EXTRACTIONS = REPO / "working/theories/extractions"
OUTDIR = REPO / "working/theories/regrounding"

GROUNDABLE = {"book", "dunk-egg", "fab"}
MIN_NORM_LEN = 40       # window layer: below this, containment is too accidental
MIN_EXACT_LEN = 12      # exact layer: short ASX fragments OK — uniqueness is the filter
MIN_WINDOW_TOKENS = 8


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    return re.sub(r"\s+", " ", s).strip().lower()


def build_corpus():
    corpus = []
    for f in sorted(CHAPTERS.rglob("*.md")):
        book = f.parent.name
        lines = f.read_text().splitlines()
        parts, offsets, pos = [], [], 0
        for ln in lines:
            nl = norm(ln)
            offsets.append(pos)
            parts.append(nl)
            pos += len(nl) + 1
        corpus.append((book, str(f.relative_to(REPO)), " ".join(parts), offsets, lines))
    return corpus


def pos_to_line(offsets, i):
    lo, hi = 0, len(offsets) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if offsets[mid] <= i:
            lo = mid
        else:
            hi = mid - 1
    return lo


def find_hits(corpus, nq: str, cap: int = 2):
    """Up to `cap` corpus hits of normalized string nq."""
    hits = []
    for book, rel, blob, offsets, lines in corpus:
        start = 0
        while True:
            i = blob.find(nq, start)
            if i == -1:
                break
            lo = pos_to_line(offsets, i)
            hi = pos_to_line(offsets, i + max(len(nq) - 1, 0))
            verbatim = " ".join(lines[lo:hi + 1]).strip()
            hits.append({"file": rel, "book": book, "line": lo + 1, "verbatim": verbatim})
            if len(hits) >= cap:
                return hits
            start = i + 1
    return hits


def window_match(corpus, tokens):
    """Longest contiguous token window with a unique corpus hit."""
    n = len(tokens)
    for size in range(n - 1, MIN_WINDOW_TOKENS - 1, -1):
        for start in range(0, n - size + 1):
            w = " ".join(tokens[start:start + size])
            if len(w) < MIN_NORM_LEN:
                continue
            hits = find_hits(corpus, w, cap=2)
            if len(hits) == 1:
                return w, hits[0]
    return None, None


def ground_beat(corpus, beat):
    domain = beat.get("source_domain", "unknown")
    if domain not in GROUNDABLE:
        return {"status": "not-groundable"}
    quote = beat.get("spoken_quote")
    if not quote:
        return {"status": "needs-agent"}
    nq = norm(quote)
    if len(nq) >= MIN_EXACT_LEN:
        hits = find_hits(corpus, nq, cap=2)
        if len(hits) == 1:
            return {"status": "matched", "layer": "exact", **hits[0]}
        if len(hits) > 1:
            return {"status": "ambiguous", "layer": "exact",
                    "hits": [f"{h['file']}:{h['line']}" for h in hits]}
    w, hit = window_match(corpus, nq.split(" "))
    if hit:
        return {"status": "matched", "layer": "window", "window": w, **hit}
    return {"status": "no-match"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos", nargs="*", help="video ids (default: every extraction file)")
    args = ap.parse_args()

    OUTDIR.mkdir(parents=True, exist_ok=True)
    corpus = build_corpus()
    print(f"corpus: {len(corpus)} chapter files")

    files = ([EXTRACTIONS / f"{v}.jsonl" for v in args.videos] if args.videos
             else sorted(EXTRACTIONS.glob("*.jsonl")))
    for f in files:
        rows = [json.loads(ln) for ln in f.read_text().splitlines() if ln.strip()]
        out, counts = [], Counter()
        for r in rows:
            if r.get("kind") != "beat":
                continue
            res = ground_beat(corpus, r)
            counts[res["status"]] += 1
            out.append({"beat_id": r["beat_id"], "stance": r.get("stance"),
                        "source_domain": r.get("source_domain"),
                        "spoken_quote": r.get("spoken_quote"),
                        "paraphrase": r.get("paraphrase"), **res})
        vid = f.stem
        (OUTDIR / f"{vid}.jsonl").write_text(
            "".join(json.dumps(o, ensure_ascii=False) + "\n" for o in out))
        print(f"{vid}: {dict(counts)}")


if __name__ == "__main__":
    main()
