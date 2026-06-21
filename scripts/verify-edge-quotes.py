#!/usr/bin/env python3
"""Verify that each edge's evidence_quote actually appears at its evidence_ref line.

The deterministic half of citation-checking (Python-before-agent): catches the
"reconstructed-not-read" failure mode — a plausible quote attached to a line that
doesn't contain it. Normalizes smart/straight quotes, ellipsis, and dashes; handles
ellipsis-condensed quotes by requiring each fragment to appear in the cited window.
A fuzzy/paraphrase adjudication subagent is only needed for the rows this FLAGS.

Usage:
  python3 scripts/verify-edge-quotes.py                      # check ALL edges with a quote+ref
  python3 scripts/verify-edge-quotes.py --run-id <id>        # only one mint run
  python3 scripts/verify-edge-quotes.py --edge-type WITNESS_IN
  python3 scripts/verify-edge-quotes.py --window 3 --verbose

Exit code 1 if any MISMATCH (CI-friendly); 0 otherwise. BADREF (file/line missing)
and OK_WIDENED (quote found but the cited line number is off) are reported but do not
fail the run by default (use --strict to fail on those too).
"""
import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"

_TRANS = {
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "…": "...", "—": "--", "–": "-", " ": " ",
}


def normalize(s: str) -> str:
    for a, b in _TRANS.items():
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def resolve_ref(ref: str):
    """'sources/chapters/affc/x.md:291' -> (lines:list, lineno:int) or (None,None)."""
    if not ref or ":" not in ref:
        return None, None
    path, _, line = ref.rpartition(":")
    p = REPO / path
    if not p.exists() or not line.isdigit():
        return None, None
    return p.read_text(encoding="utf-8").splitlines(), int(line)


def window_blob(lines, lineno, w):
    lo = max(0, lineno - 1 - w)
    hi = min(len(lines), lineno + w)
    return normalize(" ".join(lines[lo:hi]))


def check_edge(row, window):
    ref, quote = row.get("evidence_ref"), row.get("evidence_quote")
    if not ref or not quote:
        return "skip", ""
    lines, lineno = resolve_ref(ref)
    if lines is None:
        return "badref", f"file/line not resolvable: {ref}"
    nq = normalize(quote)
    frags = [f.strip() for f in nq.split("...") if len(f.strip()) >= 8] or [nq]
    blob = window_blob(lines, lineno, window)
    missing = [f for f in frags if f not in blob]
    if not missing:
        return "ok", ""
    # widen once before declaring a mismatch (cited line may be slightly off)
    blob_wide = window_blob(lines, lineno, max(window, 8))
    missing_wide = [f for f in frags if f not in blob_wide]
    if not missing_wide:
        return "ok_widened", f"matched within +-8 lines (cited line {lineno} slightly off)"
    return "mismatch", f'not found near {ref}: "{missing_wide[0][:70]}"'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id")
    ap.add_argument("--edge-type")
    ap.add_argument("--source")
    ap.add_argument("--window", type=int, default=2)
    ap.add_argument("--strict", action="store_true", help="fail on BADREF/OK_WIDENED too")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--edges-file", default=str(EDGES))
    args = ap.parse_args()

    rows = []
    for ln in Path(args.edges_file).read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        r = json.loads(ln)
        if args.run_id and r.get("run_id") != args.run_id:
            continue
        if args.edge_type and r.get("edge_type") != args.edge_type:
            continue
        if args.source and r.get("source_slug") != args.source:
            continue
        rows.append(r)

    tally = {"ok": 0, "ok_widened": 0, "mismatch": 0, "badref": 0, "skip": 0}
    problems = []
    for r in rows:
        verdict, detail = check_edge(r, args.window)
        tally[verdict] += 1
        label = f'{r.get("source_slug")} --[{r.get("edge_type")}]--> {r.get("target_slug")}'
        if verdict in ("mismatch", "badref") or (verdict == "ok_widened"):
            problems.append((verdict, label, detail))
        elif args.verbose and verdict == "ok":
            print(f"  ok        {label}")

    print(f"\nChecked {len(rows)} edges  |  "
          f"ok {tally['ok']} · ok_widened {tally['ok_widened']} · "
          f"MISMATCH {tally['mismatch']} · badref {tally['badref']} · skip(no quote/ref) {tally['skip']}")
    for verdict, label, detail in problems:
        print(f"  [{verdict.upper()}] {label}\n           {detail}")

    fail = tally["mismatch"] > 0 or (args.strict and (tally["badref"] or tally["ok_widened"]))
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
