#!/usr/bin/env python3
"""Roles slice S213 round 2 — deterministic prep: next ~50 ranked zero-role events.

Round-2 rules (continue prompt 2026-07-11-roles-slice-round2.md):
  - Do NOT re-rank. The ORDER is frozen from S212's ranked-all.json.
  - Eligibility IS re-scanned fresh: an event drops out if it now carries any
    incoming role edge (S212's +236 minted edges absorbed the round-1 top-50
    and may have absorbed others).
  - Take the next TOP_N still-zero-role events in frozen rank order; build the
    same passage packets for Sonnet proposers.
  - Fresh degree/quote counts are recorded alongside (for the early-stop
    eyeball: median fresh degree < ~4 => cut), but the frozen score orders.

Pure read-only prep: no graph writes. Template: working/roles-slice-s212/scan-rank.py

Outputs (working/roles-slice-s213/):
  round2-selection.json    the selected events + frozen rank + fresh metrics
  packets/packets-N.json   4 contiguous chunks (13/13/12/12)
"""
import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
S212 = REPO / "working/roles-slice-s212"
PACKETS_DIR = OUT / "packets"
PACKETS_DIR.mkdir(exist_ok=True)

ROLE_TYPES = {
    "AGENT_IN", "VICTIM_IN", "WITNESS_IN", "COMMANDS_IN",
    "PARTICIPATES_IN", "FIGHTS_IN", "ATTENDS", "OFFICIATES", "HONORED_AT",
}

TOP_N = 50
# EARLY-STOP CUT (S213, applied per the round-2 rule): the batch tripped the
# floor (median fresh degree 3.0 < ~4). Knee sits at frozen score 50 — below
# it the rows go quote-zero/thin and include junk nodes (`marriage`,
# `great-council`, `tourney-at-ashford-meadow`, all degree<=1, quotes 0).
# Packets are built only for rows with frozen score >= CUT_SCORE;
# round2-selection.json keeps all selected rows for the record.
CUT_SCORE = 50
BODY_CAP = 8000
TRUNC_MARKER = "\n\n...[TRUNCATED — body exceeds 8000 char cap]...\n"


def load_edges():
    by_slug = defaultdict(list)
    role_covered = set()
    with open(REPO / "graph/edges/edges.jsonl") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            t = e.get("edge_type")
            s = e.get("source_slug")
            tg = e.get("target_slug")
            if not t or not s or not tg:
                continue
            by_slug[s].append((t, tg, "out"))
            by_slug[tg].append((t, s, "in"))
            if t in ROLE_TYPES:
                role_covered.add(tg)
    return by_slug, role_covered


def frontmatter_block(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return "", text
    return m.group(1), m.group(2)


def count_quotes(body_text):
    return sum(1 for ln in body_text.splitlines() if ln.lstrip().startswith(">"))


def edge_summary(by_slug, slug, cap=40):
    edges = by_slug.get(slug, [])
    rows = [f"{d}:{t}:{o}" for (t, o, d) in edges]
    return rows[:cap] + ([f"...(+{len(rows) - cap} more)"] if len(rows) > cap else [])


def cap_body(body_text):
    body_text = body_text.strip("\n")
    if len(body_text) <= BODY_CAP:
        return body_text
    return body_text[:BODY_CAP] + TRUNC_MARKER


def main():
    by_slug, role_covered = load_edges()

    frozen = json.loads((S212 / "ranked-all.json").read_text())
    frozen_events = frozen["events"]  # already sorted by S212 score

    selected = []
    absorbed = []
    missing_file = []
    for frozen_rank, row in enumerate(frozen_events, start=1):
        slug = row["slug"]
        # Round-1 coverage: frozen ranks 1-50 were S212's packets. Any that are
        # still zero-role yielded nothing mintable there (adjudicated 0-role or
        # parked wiki_only) — re-proposing them is banned. Round 2 = ranks 51+.
        if frozen_rank <= 50:
            continue
        if slug in role_covered:
            absorbed.append(slug)
            continue
        path = REPO / row["file"]
        if not path.exists():
            missing_file.append(slug)
            continue
        text = path.read_text()
        fm_text, body_text = frontmatter_block(text)
        fresh_deg = len(by_slug.get(slug, []))
        selected.append({
            "slug": slug,
            "node_type": row["node_type"],
            "file": row["file"],
            "containers": row["containers"],
            "frozen_rank": frozen_rank,
            "frozen_score": row["score"],
            "fresh_degree": fresh_deg,
            "quotes": count_quotes(body_text),
            "prose_lines": row["prose_lines"],
            "_body": cap_body(body_text),
        })
        if len(selected) >= TOP_N:
            break

    (OUT / "round2-selection.json").write_text(json.dumps({
        "_meta": {
            "session": "S213",
            "slice": "roles round 2",
            "order_source": "working/roles-slice-s212/ranked-all.json (frozen, not re-ranked)",
            "frozen_zero_role_total": len(frozen_events),
            "absorbed_by_s212_edges": len(absorbed),
            "missing_files": missing_file,
            "selected": len(selected),
            "round1_ranks_excluded": "frozen ranks 1-50 (S212 packets; still-zero-role ones adjudicated 0-role or parked)",
            "early_stop_cut": {
                "tripped_on": "median fresh degree 3.0 < ~4 floor",
                "cut_rule": f"frozen score >= {CUT_SCORE} (knee: below it rows go quote-zero/thin + junk nodes)",
                "packets_built_for": sum(1 for r in selected if r["frozen_score"] >= CUT_SCORE),
            },
            "role_types": sorted(ROLE_TYPES),
        },
        "events": [{k: v for k, v in r.items() if k != "_body"} for r in selected],
    }, indent=1))

    kept = [r for r in selected if r["frozen_score"] >= CUT_SCORE]
    n_chunks = 4
    base, extra = divmod(len(kept), n_chunks)
    chunk_sizes = [base + (1 if i < extra else 0) for i in range(n_chunks)]
    chunks = []
    idx = 0
    for size in chunk_sizes:
        chunks.append(kept[idx:idx + size])
        idx += size

    for chunk_num, chunk in enumerate(chunks, start=1):
        packets = [{
            "slug": r["slug"],
            "node_type": r["node_type"],
            "file": r["file"],
            "containers": r["containers"],
            "existing_edges": edge_summary(by_slug, r["slug"]),
            "body": r["_body"],
        } for r in chunk]
        (PACKETS_DIR / f"packets-{chunk_num}.json").write_text(json.dumps({
            "_meta": {
                "session": "S213",
                "slice": "roles round 2",
                "chunk": chunk_num,
                "slugs": [r["slug"] for r in chunk],
            },
            "packets": packets,
        }, indent=1))

    # --- report (early-stop signals included) ---
    print(f"Frozen zero-role list (S212): {len(frozen_events)}")
    print(f"Absorbed by S212 minted edges (now roled, skipped): {len(absorbed)}")
    print(f"Selected for round 2: {len(selected)}")
    degs = [r["fresh_degree"] for r in selected]
    bodies = [len(r["_body"]) for r in selected]
    print(f"Fresh degree: median {statistics.median(degs)}, min {min(degs)}, max {max(degs)}")
    print(f"Body chars: median {int(statistics.median(bodies))}, "
          f"<800-char bodies: {sum(1 for b in bodies if b < 800)}")
    print()
    header = (f"{'r2rank':>6} {'frzrank':>7} {'score':>5} {'deg':>4} {'quo':>4} "
              f"{'bodyc':>6}  {'subtype':<22}  slug")
    print(header)
    print("-" * len(header))
    for i, r in enumerate(selected, start=1):
        print(f"{i:>6} {r['frozen_rank']:>7} {r['frozen_score']:>5} {r['fresh_degree']:>4} "
              f"{r['quotes']:>4} {len(r['_body']):>6}  {r['node_type']:<22}  {r['slug']}")


if __name__ == "__main__":
    sys.exit(main())
