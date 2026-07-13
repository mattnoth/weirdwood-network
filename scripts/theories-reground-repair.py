#!/usr/bin/env python3
"""theories-reground-repair.py — S214 deterministic post-pass over agent grounding.

Agents (esp. Haiku) return correct verbatim quotes with sloppy line numbers.
Standing rule (S213): the deterministic byte-check outranks agent verdicts.
For every `grounded` row in working/theories/regrounding-agent/<id>.jsonl:

  1. normalize the quote; search the CLAIMED file → repair `line` to the real hit.
  2. not in the claimed file → search the whole corpus; unique hit → repair
     file+line (logged as `relocated`).
  3. nowhere / ambiguous → status flipped to `byte-fail` (drops out of the
     mintable set; a human or fresh agent re-adjudicates).

Rewrites the file in place; prints a per-video summary.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
AGENT_DIR = REPO / "working/theories/regrounding-agent"
CHAPTERS = REPO / "sources/chapters"


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    return re.sub(r"\s+", " ", s).strip().lower()


def norm_loose(s: str) -> str:
    """norm() then drop quote marks — nested-quotation style (corpus curly
    singles vs a transcriber's doubles) defeats strict matching. MATCHING
    only; returned verbatim text is always byte-copied from the corpus."""
    return re.sub(r"\s+", " ", norm(s).replace('"', "").replace("'", "")).strip()


def build_corpus(normfn=norm):
    corpus = []
    for f in sorted(CHAPTERS.rglob("*.md")):
        lines = f.read_text().splitlines()
        parts, offsets, pos = [], [], 0
        for ln in lines:
            nl = normfn(ln)
            offsets.append(pos)
            parts.append(nl)
            pos += len(nl) + 1
        corpus.append((str(f.relative_to(REPO)), " ".join(parts), offsets))
    return corpus


def pos_to_line(offsets, i):
    lo, hi = 0, len(offsets) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if offsets[mid] <= i:
            lo = mid
        else:
            hi = mid - 1
    return lo + 1


def locate(corpus, nq, only_file=None):
    hits = []
    for rel, blob, offsets in corpus:
        if only_file and rel != only_file:
            continue
        i = blob.find(nq)
        if i != -1:
            hits.append((rel, pos_to_line(offsets, i)))
            if blob.find(nq, i + 1) != -1:
                hits.append((rel, -1))  # same-file second hit
        if len(hits) >= 2:
            break
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos", nargs="*", help="video ids (default: all agent files)")
    args = ap.parse_args()

    corpora = [(build_corpus(norm), norm, ""), (build_corpus(norm_loose), norm_loose, "-loose")]
    files = ([AGENT_DIR / f"{v}.jsonl" for v in args.videos] if args.videos
             else sorted(AGENT_DIR.glob("*.jsonl")))
    for f in files:
        rows = [json.loads(ln) for ln in f.read_text().splitlines() if ln.strip()]
        c = Counter()
        for r in rows:
            if r.get("status") not in ("grounded", "byte-fail"):
                continue
            resolved = False
            for corpus, normfn, tag in corpora:
                nq = normfn(r.get("verbatim_quote") or "")
                if len(nq) < 12:
                    continue
                hits = locate(corpus, nq, only_file=r.get("file"))
                if len(hits) == 1:
                    if hits[0][1] != r.get("line"):
                        r["line"] = hits[0][1]
                        c[f"line-repaired{tag}"] += 1
                    else:
                        c[f"ok{tag}"] += 1
                    resolved = True
                    break
                if len(hits) > 1:
                    continue  # ambiguous under this norm; let the next layer try
                hits = locate(corpus, nq)
                if len(hits) == 1:
                    r["file"], r["line"] = hits[0]
                    r["repair"] = f"relocated{tag}"
                    c[f"relocated{tag}"] += 1
                    resolved = True
                    break
            if resolved:
                r["status"] = "grounded"
                r.pop("repair", None) if not r.get("repair", "").startswith("relocated") else None
            else:
                r["status"] = "byte-fail"
                r["repair"] = "not-in-corpus-or-ambiguous"
                c["byte-fail"] += 1
        f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        print(f"{f.stem}: {dict(c)}")


if __name__ == "__main__":
    main()
