#!/usr/bin/env python3
"""propose_quote_regrounding.py — S195 Python repair-proposer for drifted quotes.

Covers BOTH scopes of the quote re-grounding cleanup:
  * node `## Quotes` entries that fail scripts/verify_node_quotes.py
  * edge evidence_quote rows that verify-edge-quotes.py flags MISMATCH,
    plus deterministic line repoints for its OK_WIDENED class

For each failing row it fuzzy-locates the best candidate span in the cited
chapter (token-run matching via difflib), falling back to sibling chapters of
the same book (rare-token prefilter). Proposals are MARKER-EXTRACTED — the
proposed text is a verbatim contiguous substring of the source file, never
retyped — so the standing S123 "never splice across attributions" rule is
satisfied by construction.

Classes (per the S195 continue prompt):
  a  exact-elsewhere   — full quote found verbatim at another line → repoint cite
  b  near-match        — longest clean contiguous verbatim sub-span proposed
  c  spliced           — same repair as (b); quote was stitched/condensed
  d  no-source         — no plausible window anywhere → propose drop-or-park

Output: ONE staging file working/quote-census/s195-regrounding-staging.json
with every proposal + before/after. Nothing is written to graph/ here —
apply is a separate Matt/Fable-dispositioned step.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "graph" / "query"))
from weirwood_query.load import parse_quotes  # noqa: E402

NODES_DIR = REPO / "graph" / "nodes"
CHAPTERS = REPO / "sources" / "chapters"
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
OUT = REPO / "working" / "quote-census" / "s195-regrounding-staging.json"

CITE_RE = re.compile(r"(sources/chapters/[a-z0-9/_-]+?\.md):(\d+)")
NODE_WINDOW = 5      # verify_node_quotes.py: cited line .. +4
EDGE_WINDOW = 2      # verify-edge-quotes.py default: +-2
MIN_SPAN_TOKENS = 6  # below this a proposed sub-span is judged implausible


# ---------- normalization (superset of both verifiers') ----------

def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    return re.sub(r"\s+", " ", s).strip().lower()


MARKUP_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")      # [text](target) -> text
MARKUP_WIKIREF = re.compile(r"\(wiki:[^)]*\)")           # (wiki:...) cite blobs
MARKUP_EM = re.compile(r"(\*\*?)(.+?)\1")                # *em* / **strong**


def strip_markup(s: str) -> str:
    s = MARKUP_WIKIREF.sub("", s)
    s = MARKUP_LINK.sub(r"\1", s)
    s = MARKUP_EM.sub(r"\2", s)
    return s


PUNCT_EDGE = re.compile(r"^[\W_]+|[\W_]+$")


def core(tok: str) -> str:
    """Comparison form of a token: normalized, edge punctuation stripped."""
    return PUNCT_EDGE.sub("", norm(tok))


# ---------- source-file token model ----------

class SourceFile:
    """Chapter file as a token stream with char offsets back to raw text."""

    def __init__(self, relpath: str):
        self.relpath = relpath
        self.raw = (REPO / relpath).read_text(encoding="utf-8")
        self.lines = self.raw.splitlines()
        # flat text = lines joined with \n (offsets into self.raw are fine
        # because splitlines/join preserves char positions for \n files)
        self.tokens: list[str] = []        # core forms
        self.spans: list[tuple[int, int]] = []  # (start,end) char offsets in raw
        self.token_line: list[int] = []    # 1-based line number per token
        offset = 0
        for lineno, line in enumerate(self.lines, 1):
            for m in re.finditer(r"\S+", line):
                c = core(m.group(0))
                if c:
                    self.tokens.append(c)
                    self.spans.append((offset + m.start(), offset + m.end()))
                    self.token_line.append(lineno)
            offset += len(line) + 1

    def extract(self, ti: int, tj: int) -> str:
        """Verbatim source substring covering tokens [ti, tj], newlines->space."""
        a = self.spans[ti][0]
        b = self.spans[tj][1]
        return re.sub(r"\s+", " ", self.raw[a:b]).strip()


_SF_CACHE: dict[str, SourceFile] = {}


def sf(relpath: str) -> SourceFile | None:
    if relpath not in _SF_CACHE:
        p = REPO / relpath
        if not p.exists():
            return None
        _SF_CACHE[relpath] = SourceFile(relpath)
    return _SF_CACHE[relpath]


# ---------- corpus rare-token index (for sibling/corpus fallback) ----------

def build_token_index() -> tuple[dict[str, set[str]], Counter]:
    idx: dict[str, set[str]] = defaultdict(set)
    df: Counter = Counter()
    for p in sorted(CHAPTERS.rglob("*.md")):
        rel = str(p.relative_to(REPO))
        seen = set()
        for m in re.finditer(r"\S+", p.read_text(encoding="utf-8")):
            c = core(m.group(0))
            if c and c not in seen:
                seen.add(c)
                idx[c].add(rel)
        for c in seen:
            df[c] += 1
    return idx, df


TOKEN_IDX: dict[str, set[str]] = {}
TOKEN_DF: Counter = Counter()


def candidate_files(qtokens: list[str], cited: str, limit: int = 8) -> list[str]:
    """Files sharing the quote's rarest tokens; same-book files first."""
    rare = sorted(set(qtokens), key=lambda t: TOKEN_DF.get(t, 0))
    rare = [t for t in rare if 0 < TOKEN_DF.get(t, 99999) <= 40][:8]
    score: Counter = Counter()
    for t in rare:
        for f in TOKEN_IDX.get(t, ()):
            score[f] += 1
    book = cited.split("/")[2] if cited.count("/") >= 3 else ""
    ranked = sorted(
        score.items(),
        key=lambda kv: (-kv[1], 0 if f"/{book}/" in kv[0] else 1, kv[0]),
    )
    return [f for f, n in ranked[:limit] if n >= 2]


# ---------- matching ----------

def quote_tokens(text: str) -> list[str]:
    return [c for c in (core(t) for t in strip_markup(text).split()) if c]


def best_run(qtok: list[str], src: SourceFile) -> tuple[int, int, int]:
    """Longest contiguous common token run. Returns (q_start, s_start, length)."""
    sm = SequenceMatcher(None, qtok, src.tokens, autojunk=False)
    m = sm.find_longest_match(0, len(qtok), 0, len(src.tokens))
    return m.a, m.b, m.size


def full_span(qtok: list[str], src: SourceFile, window: int):
    """Attribution-inclusive repair: if the quote's matched fragments sit close
    together in the source (gap = a short inline attribution / tiny splice),
    propose the FULL verbatim source span first-to-last matched token. Keeps
    the whole quote instead of truncating to the longest fragment.
    Returns (s_i, s_j, coverage) or None."""
    sm = SequenceMatcher(None, qtok, src.tokens, autojunk=False)
    blocks = [b for b in sm.get_matching_blocks() if b.size >= 3]
    if len(blocks) < 2:
        return None
    si = blocks[0].b
    sj = blocks[-1].b + blocks[-1].size - 1
    matched = sum(b.size for b in blocks)
    gap = (sj - si + 1) - matched
    cov = matched / max(1, len(qtok))
    if gap <= 14 and cov >= 0.70 and span_fits_window(src, si, sj, window):
        return si, sj, cov
    return None


def coverage_blocks(qtok: list[str], src: SourceFile) -> int:
    """Total matched tokens across all blocks (for exact-elsewhere detection)."""
    sm = SequenceMatcher(None, qtok, src.tokens, autojunk=False)
    return sum(b.size for b in sm.get_matching_blocks())


def span_fits_window(src: SourceFile, si: int, sj: int, window: int) -> bool:
    return src.token_line[sj] - src.token_line[si] < window


def context_lines(src: SourceFile, lineno: int, n: int = 2) -> str:
    lo, hi = max(0, lineno - 1 - n), min(len(src.lines), lineno + n)
    return "\n".join(f"{i+1}: {src.lines[i]}" for i in range(lo, hi) if src.lines[i].strip())


def propose(quote_text: str, cited_file: str, window: int, centered: bool = False) -> dict:
    """Core proposer: returns proposal dict for one failing quote.

    centered=True cites the span's middle line (edge verifier windows are
    +-w around the cite); False cites the first line (node windows run
    cite..+4 forward).
    """
    qtok = quote_tokens(quote_text)
    files = [cited_file] + [f for f in candidate_files(qtok, cited_file) if f != cited_file]
    best = None  # (size, -file_rank, q_i, s_i, file)
    for rank, f in enumerate(files):
        src = sf(f)
        if src is None:
            continue
        qi, si, size = best_run(qtok, src)
        if best is None or size > best[0]:
            best = (size, rank, qi, si, f)
        if size == len(qtok):
            break  # can't beat exact
    if best is None or best[0] < MIN_SPAN_TOKENS:
        return {
            "class": "d-no-source",
            "note": f"no contiguous run >= {MIN_SPAN_TOKENS} tokens in cited file "
                    f"or {len(files)-1} candidate siblings",
        }
    size, _, qi, si, f = best
    src = sf(f)
    sj = si + size - 1
    # trim span to fit the verifier window if needed
    while not span_fits_window(src, si, sj, window) and sj > si:
        sj -= 1
    size_fit = sj - si + 1
    if size_fit < MIN_SPAN_TOKENS:
        return {"class": "d-no-source", "note": "best run does not fit verifier window"}
    matched = size_fit
    note = None
    if size_fit < len(qtok):
        fs = full_span(qtok, src, window)
        if fs is not None and (fs[1] - fs[0] + 1) > size_fit:
            si, sj, cov = fs
            matched = round(cov * len(qtok))
            note = "attribution-inclusive full span (keeps whole quote)"
    text = sf(f).extract(si, sj)
    # cosmetic: drop an unbalanced leading/trailing double-quote char
    for plain, curly_open, curly_close in (('"', "“", "”"),):
        n = text.count(plain) + text.count(curly_open) + text.count(curly_close)
        if n % 2 == 1:
            if text[0] in (plain, curly_open):
                text = text[1:].lstrip()
            elif text[-1] in (plain, curly_close):
                text = text[:-1].rstrip()
    first, last = src.token_line[si], src.token_line[sj]
    line = first + (last - first) // 2 if centered else first
    exact = matched >= len(qtok) and note is None
    cls = "a-exact-elsewhere" if exact else (
        "c-spliced" if coverage_blocks(qtok, src) > matched + 2 or note else "b-near-match")
    # proposed_text is ALWAYS the marker-extracted source span — token-level
    # "exact" tolerates punctuation drift the string verifiers do not
    return {
        "class": cls,
        "proposed_text": text,
        "proposed_cite": f"{f}:{line}",
        "match_tokens": matched,
        "quote_tokens": len(qtok),
        "coverage": round(matched / max(1, len(qtok)), 2),
        "relocated": f != cited_file,
        **({"note": note} if note else {}),
        "context": context_lines(src, line),
    }


# ---------- node scope ----------

def quotes_body(text: str) -> str:
    m = re.search(r"^## Quotes[ \t]*\n", text, re.M)
    if not m:
        return ""
    body = text[m.end():]
    nxt = re.search(r"^## ", body, re.M)
    return body[: nxt.start()] if nxt else body


def node_check(cite: str, quote_text: str) -> bool:
    m = CITE_RE.search(cite)
    if not m:
        return False
    fpath, line = REPO / m.group(1), int(m.group(2))
    if not fpath.exists():
        return False
    src = fpath.read_text().splitlines()
    if line < 1 or line > len(src):
        return False
    window = norm(" ".join(s for s in src[line - 1: line - 1 + NODE_WINDOW] if s.strip()))
    if norm(quote_text) in window:
        return True
    return norm(quote_text.strip().strip('"“”').strip()) in window


def node_rows() -> list[dict]:
    rows = []
    for path in sorted(NODES_DIR.rglob("*.node.md")):
        if "_conflicts" in path.parts:
            continue
        slug = path.name.removesuffix(".node.md")
        body = quotes_body(path.read_text())
        if not body:
            continue
        for q in parse_quotes(body):
            cite = q.get("cite")
            if not cite or node_check(cite, q["text"]):
                continue
            m = CITE_RE.search(cite)
            cited_file = m.group(1) if m else None
            row = {
                "scope": "node",
                "slug": slug,
                "node_file": str(path.relative_to(REPO)),
                "old_text": q["text"],
                "attribution": q.get("attribution"),
                "old_cite": cite,
            }
            if cited_file is None:
                row.update({"class": "d-no-source", "note": f"malformed cite {cite!r}"})
            else:
                row.update(propose(q["text"], cited_file, NODE_WINDOW))
            rows.append(row)
    return rows


# ---------- edge scope ----------

def edge_normalize(s: str) -> str:
    for a, b in {"‘": "'", "’": "'", "“": '"', "”": '"',
                 "…": "...", "—": "--", "–": "-", " ": " "}.items():
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def edge_window_blob(lines: list[str], lineno: int, w: int) -> str:
    lo, hi = max(0, lineno - 1 - w), min(len(lines), lineno + w)
    return edge_normalize(" ".join(lines[lo:hi]))


def edge_check(row: dict) -> tuple[str, str | None]:
    """Re-implementation of verify-edge-quotes.py check_edge (returns verdict, ref_file)."""
    ref, quote = row.get("evidence_ref"), row.get("evidence_quote")
    if not ref or not quote:
        return "skip", None
    path, _, line = ref.rpartition(":")
    p = REPO / path
    if not p.exists() or not line.isdigit():
        return "badref", None
    lines, lineno = p.read_text(encoding="utf-8").splitlines(), int(line)
    nq = edge_normalize(quote)
    frags = [f.strip() for f in nq.split("...") if len(f.strip()) >= 8] or [nq]
    if all(f in edge_window_blob(lines, lineno, EDGE_WINDOW) for f in frags):
        return "ok", path
    if all(f in edge_window_blob(lines, lineno, max(EDGE_WINDOW, 8)) for f in frags):
        return "ok_widened", path
    return "mismatch", path


def find_exact_line(quote: str, relpath: str) -> int | None:
    """Line where every >=8-char fragment of the quote sits in a +-EDGE_WINDOW blob."""
    src = sf(relpath)
    if src is None:
        return None
    nq = edge_normalize(quote)
    frags = [f.strip() for f in nq.split("...") if len(f.strip()) >= 8] or [nq]
    for lineno in range(1, len(src.lines) + 1):
        if not src.lines[lineno - 1].strip():
            continue
        blob = edge_window_blob(src.lines, lineno, EDGE_WINDOW)
        if all(f in blob for f in frags):
            return lineno
    return None


def edge_rows() -> list[dict]:
    rows = []
    for i, ln in enumerate(EDGES.read_text(encoding="utf-8").splitlines()):
        if not ln.strip():
            continue
        r = json.loads(ln)
        verdict, ref_file = edge_check(r)
        if verdict not in ("mismatch", "ok_widened"):
            continue
        row = {
            "scope": "edge",
            "edge_line": i + 1,
            "source_slug": r.get("source_slug"),
            "edge_type": r.get("edge_type"),
            "target_slug": r.get("target_slug"),
            "run_id": r.get("run_id"),
            "old_text": r.get("evidence_quote"),
            "old_cite": r.get("evidence_ref"),
            "verdict": verdict,
        }
        if verdict == "ok_widened":
            lineno = find_exact_line(r["evidence_quote"], ref_file)
            if lineno is not None:
                row.update({
                    "class": "a-exact-elsewhere",
                    "proposed_text": r["evidence_quote"],
                    "proposed_cite": f"{ref_file}:{lineno}",
                    "note": "deterministic line repoint (verifier OK_WIDENED)",
                })
            else:
                row.update({"class": "d-no-source",
                            "note": "OK_WIDENED but no single line passes at default window"})
        else:
            # try a straight fragment-search in the cited file first
            lineno = find_exact_line(r["evidence_quote"], ref_file) if ref_file else None
            if lineno is not None:
                row.update({
                    "class": "a-exact-elsewhere",
                    "proposed_text": r["evidence_quote"],
                    "proposed_cite": f"{ref_file}:{lineno}",
                    "note": "all fragments found at another line of the cited file",
                })
            else:
                row.update(propose(r["evidence_quote"], ref_file,
                                   EDGE_WINDOW * 2 + 1, centered=True)
                           if ref_file else
                           {"class": "d-no-source", "note": "unresolvable ref"})
        rows.append(row)
    return rows


# ---------- main ----------

def main() -> None:
    global TOKEN_IDX, TOKEN_DF
    print("building corpus token index ...", flush=True)
    TOKEN_IDX, TOKEN_DF = build_token_index()

    print("scanning node scope ...", flush=True)
    nrows = node_rows()
    print(f"  {len(nrows)} failing node quotes")
    print("scanning edge scope ...", flush=True)
    erows = edge_rows()
    print(f"  {len(erows)} edge rows (mismatch + ok_widened)")

    rows = nrows + erows
    tally = Counter((r["scope"], r["class"]) for r in rows)
    summary = {f"{s}/{c}": n for (s, c), n in sorted(tally.items())}
    OUT.write_text(json.dumps(
        {"session": "S195", "summary": summary, "rows": rows},
        indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"wrote {OUT.relative_to(REPO)} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
