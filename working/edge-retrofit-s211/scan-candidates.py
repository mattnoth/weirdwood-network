#!/usr/bin/env python3
"""Edge-vocab retrofit S211 — deterministic candidate-pool prep.

Scans node prose for (a) knighting language and (b) suspicion language, builds
passage packets for Sonnet proposers. Pure read-only prep: no graph writes.

Outputs (working/edge-retrofit-s211/packets/):
  knighting-packets.json   one packet per node file with knighting language
  suspicion-packets.json   one packet per event node with suspicion language
Each packet: slug, node type, matched passages (with context), existing edges
touching the slug (dedup context), plus the global exclusion sets.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "packets"
OUT.mkdir(exist_ok=True)

KNIGHT_RE = re.compile(
    r"knighted (?:by|him|her|them)|dubbed (?:him |her )?(?:a )?knight"
    r"|received (?:his|her) knighthood|won (?:his|her) knighthood"
    r"|knighthood (?:from|at the hands of)|knights? him on the spot",
    re.I,
)
SUSPECT_RE = re.compile(
    r"suspect(?:ed|s|ion)?|accus(?:ed|es|ation)|blamed?\b|rumou?r(?:ed|s)?"
    r"|whisper(?:ed|s)? that|some (?:say|said|believed)|believed to have"
    r"|never (?:proven|known)|allegedly",
    re.I,
)

ROLE_TYPES = {"AGENT_IN", "VICTIM_IN", "WITNESS_IN", "COMMANDS_IN",
              "PARTICIPATES_IN", "FIGHTS_IN", "ATTENDS", "OFFICIATES"}


def load_edges():
    by_slug = defaultdict(list)
    suspected = set()
    knighted = set()
    with open(REPO / "graph/edges/edges.jsonl") as f:
        for line in f:
            e = json.loads(line)
            t, s, tg = e.get("edge_type"), e["source_slug"], e["target_slug"]
            by_slug[s].append((t, tg, "out"))
            by_slug[tg].append((t, s, "in"))
            if t == "SUSPECTED_OF":
                suspected.add((s, tg))
            if t in ("KNIGHTED_BY", "BESTOWS_KNIGHTHOOD_ON"):
                knighted.add((s, tg))
                knighted.add((tg, s))
    return by_slug, suspected, knighted


def frontmatter_type(text):
    m = re.search(r"^type:\s*(\S+)", text, re.M)
    return m.group(1) if m else "?"


def passages(text, regex, ctx=2):
    lines = text.splitlines()
    hits = [i for i, ln in enumerate(lines) if regex.search(ln)]
    out, used = [], set()
    for i in hits:
        span = range(max(0, i - ctx), min(len(lines), i + ctx + 1))
        if any(j in used for j in span):
            # merge into previous passage
            prev = out[-1]
            add = [lines[j] for j in span if j not in used]
            prev["text"] += "\n" + "\n".join(add)
            used.update(span)
            continue
        used.update(span)
        out.append({"around_line": i + 1,
                    "text": "\n".join(lines[j] for j in span)})
    return out


def edge_summary(by_slug, slug, cap=40):
    edges = by_slug.get(slug, [])
    rows = [f"{d}:{t}:{o}" for (t, o, d) in edges]
    return rows[:cap] + ([f"...(+{len(rows)-cap} more)"] if len(rows) > cap else [])


def main():
    by_slug, suspected, knighted = load_edges()
    knight_packets, suspicion_packets = [], []

    for p in sorted((REPO / "graph/nodes").rglob("*.node.md")):
        if "_conflicts" in p.parts:
            continue
        text = p.read_text()
        slug = p.name[:-8]
        ntype = frontmatter_type(text)
        if ntype == "meta.chapter":
            continue

        kp = passages(text, KNIGHT_RE)
        if kp:
            knight_packets.append({
                "slug": slug, "node_type": ntype,
                "file": str(p.relative_to(REPO)),
                "passages": kp,
                "existing_edges": edge_summary(by_slug, slug),
            })

        if "/events/" in str(p):
            sp = passages(text, SUSPECT_RE)
            if sp:
                covered = sorted(s for (s, tg) in suspected if tg == slug)
                suspicion_packets.append({
                    "slug": slug, "node_type": ntype,
                    "file": str(p.relative_to(REPO)),
                    "passages": sp,
                    "existing_suspected_of": covered,
                    "existing_edges": edge_summary(by_slug, slug),
                })

    (OUT / "knighting-packets.json").write_text(json.dumps({
        "_meta": {"session": "S211", "slice": "knighting",
                  "existing_knight_pairs": sorted(map(list, knighted))},
        "packets": knight_packets}, indent=1))
    (OUT / "suspicion-packets.json").write_text(json.dumps({
        "_meta": {"session": "S211", "slice": "suspected_of",
                  "existing_suspected_pairs": sorted(map(list, suspected))},
        "packets": suspicion_packets}, indent=1))
    print(f"knighting packets: {len(knight_packets)}")
    print(f"suspicion packets: {len(suspicion_packets)}")


if __name__ == "__main__":
    sys.exit(main())
