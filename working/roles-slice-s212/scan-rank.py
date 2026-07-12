#!/usr/bin/env python3
"""Roles slice S212 — deterministic prep: zero-role event list + ranking + packets.

Regenerates the zero-role event list (events with NO incoming role edge —
AGENT_IN / VICTIM_IN / WITNESS_IN / COMMANDS_IN / PARTICIPATES_IN / FIGHTS_IN /
ATTENDS / OFFICIATES), ranks them deterministically by a signal score, and
builds passage packets for the top ~50 for Sonnet proposers.

Pure read-only prep: no graph writes. Template: working/edge-retrofit-s211/scan-candidates.py

Outputs (working/roles-slice-s212/):
  ranked-all.json          every zero-role event + metrics + score, sorted
  packets/packets-1.json   top-50 events, chunk 1 of 4 (13 entries)
  packets/packets-2.json   chunk 2 of 4 (13 entries)
  packets/packets-3.json   chunk 3 of 4 (12 entries)
  packets/packets-4.json   chunk 4 of 4 (12 entries)
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
PACKETS_DIR = OUT / "packets"
PACKETS_DIR.mkdir(exist_ok=True)

ROLE_TYPES = {
    "AGENT_IN", "VICTIM_IN", "WITNESS_IN", "COMMANDS_IN",
    "PARTICIPATES_IN", "FIGHTS_IN", "ATTENDS", "OFFICIATES", "HONORED_AT",
}

TOP_N = 50
BODY_CAP = 8000
TRUNC_MARKER = "\n\n...[TRUNCATED — body exceeds 8000 char cap]...\n"


def load_edges():
    """Return by_slug (slug -> [(edge_type, other_slug, direction)]) and the
    set of event slugs that receive at least one incoming role edge."""
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
                # role edge points Person->Event: event is the target
                role_covered.add(tg)
    return by_slug, role_covered


def frontmatter_block(text):
    """Return (frontmatter_text, body_text) split on the leading --- ... ---."""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return "", text
    return m.group(1), m.group(2)


def frontmatter_field(fm_text, field):
    m = re.search(rf"^{field}:\s*(\S.*)$", fm_text, re.M)
    return m.group(1).strip() if m else None


def parse_type(fm_text):
    val = frontmatter_field(fm_text, "type")
    return val if val else "?"


def parse_containers(fm_text):
    val = frontmatter_field(fm_text, "containers")
    if not val:
        return []
    val = val.strip()
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        return [c.strip().strip('"').strip("'") for c in inner.split(",") if c.strip()]
    # fallback: bare scalar
    return [val.strip().strip('"').strip("'")]


def count_quotes(body_text):
    return sum(1 for ln in body_text.splitlines() if ln.lstrip().startswith(">"))


def count_prose_lines(body_text):
    return sum(1 for ln in body_text.splitlines() if ln.strip())


def edge_summary(by_slug, slug, cap=40):
    edges = by_slug.get(slug, [])
    rows = [f"{d}:{t}:{o}" for (t, o, d) in edges]
    return rows[:cap] + ([f"...(+{len(rows) - cap} more)"] if len(rows) > cap else [])


def degree(by_slug, slug):
    return len(by_slug.get(slug, []))


def cap_body(body_text):
    body_text = body_text.strip("\n")
    if len(body_text) <= BODY_CAP:
        return body_text
    return body_text[:BODY_CAP] + TRUNC_MARKER


def main():
    by_slug, role_covered = load_edges()

    event_paths = sorted(
        p for p in (REPO / "graph/nodes/events").glob("*.node.md")
        if "_conflicts" not in p.parts
    )

    total_scanned = 0
    zero_role = []

    for p in event_paths:
        total_scanned += 1
        text = p.read_text()
        fm_text, body_text = frontmatter_block(text)
        slug = frontmatter_field(fm_text, "slug") or p.name[:-8]

        if slug in role_covered:
            continue

        ntype = parse_type(fm_text)
        containers = parse_containers(fm_text)
        quotes = count_quotes(body_text)
        prose_lines = count_prose_lines(body_text)
        deg = degree(by_slug, slug)

        score = deg * 10 + quotes * 5 + (20 if containers else 0) + min(prose_lines, 40)

        zero_role.append({
            "slug": slug,
            "node_type": ntype,
            "file": str(p.relative_to(REPO)),
            "degree": deg,
            "quotes": quotes,
            "containers": containers,
            "prose_lines": prose_lines,
            "score": score,
        })

    zero_role.sort(key=lambda r: (-r["score"], r["slug"]))

    (OUT / "ranked-all.json").write_text(json.dumps({
        "_meta": {
            "session": "S212",
            "slice": "roles",
            "total_event_nodes_scanned": total_scanned,
            "zero_role_count": len(zero_role),
            "role_types": sorted(ROLE_TYPES),
        },
        "events": zero_role,
    }, indent=1))

    top = zero_role[:TOP_N]

    # split top into 4 contiguous chunks: 13/13/12/12
    chunk_sizes = [13, 13, 12, 12]
    assert sum(chunk_sizes) == TOP_N or sum(chunk_sizes) >= len(top), \
        "chunk sizing must cover the top slice"
    chunks = []
    idx = 0
    for size in chunk_sizes:
        chunks.append(top[idx:idx + size])
        idx += size

    for chunk_num, chunk in enumerate(chunks, start=1):
        packets = []
        for row in chunk:
            slug = row["slug"]
            path = REPO / row["file"]
            text = path.read_text()
            fm_text, body_text = frontmatter_block(text)
            packets.append({
                "slug": slug,
                "node_type": row["node_type"],
                "file": row["file"],
                "containers": row["containers"],
                "existing_edges": edge_summary(by_slug, slug),
                "body": cap_body(body_text),
            })
        out_file = PACKETS_DIR / f"packets-{chunk_num}.json"
        out_file.write_text(json.dumps({
            "_meta": {
                "session": "S212",
                "slice": "roles",
                "chunk": chunk_num,
                "slugs": [row["slug"] for row in chunk],
            },
            "packets": packets,
        }, indent=1))

    # --- report ---
    print(f"Event nodes scanned: {total_scanned}")
    print(f"Zero-role event count: {len(zero_role)}")
    print()
    header = f"{'rank':>4}  {'score':>5}  {'deg':>4}  {'quo':>4}  {'subtype':<22}  slug"
    print(header)
    print("-" * len(header))
    for i, row in enumerate(top, start=1):
        print(f"{i:>4}  {row['score']:>5}  {row['degree']:>4}  {row['quotes']:>4}  "
              f"{row['node_type']:<22}  {row['slug']}")


if __name__ == "__main__":
    sys.exit(main())
