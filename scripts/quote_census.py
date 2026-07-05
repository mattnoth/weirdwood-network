#!/usr/bin/env python3
"""quote_census.py — deterministic quote-coverage census + ranked mint worklist.

S193 quote-minting track, step 0 (Python-before-agent). Finds every graph node
that lacks curated `## Quotes` content and ranks the gap by how visible the
node is to the live chat:

  (a) graph degree            — edges.jsonl in+out edge count
  (b) POV character           — the ~26 POV-character nodes (hardcoded slug set)
  (c) theme-index membership  — the nodes the chat's `theme` tool routes users at
                                (working/wiki/data/theme-index.json, full profile)
  (d) marquee event hub       — event nodes with degree >= MARQUEE_DEGREE

"Has quotes" = the node's `## Quotes` section contains at least one `> ` line
(same shape `weirwood_query.load.parse_quotes` consumes). A bare header with
no blockquote counts as quote-less — the dossier renders "No curated book
quotes on this node yet" either way.

Score (transparent, documented in the output header):
    score = min(degree, DEGREE_CAP)
          + THEME_BOOST * theme_count
          + POV_BOOST   * is_pov
          + MARQUEE_BOOST * is_marquee_event_hub

Outputs (re-runnable; overwrite in place):
  - working/quote-census/quote-census-full.jsonl   — every node, all signals
  - working/quote-census/quote-worklist.md         — ranked quote-less top slice
                                                     + coverage stats by category

No LLM in the loop; byte-stable given an unchanged graph (sorted walks,
no timestamps in output).

Usage:
    python3 scripts/quote_census.py [--top N]
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NODES_DIR = REPO / "graph" / "nodes"
EDGES_FILE = REPO / "graph" / "edges" / "edges.jsonl"
THEME_INDEX = REPO / "working" / "wiki" / "data" / "theme-index.json"
INDEX_DIR = REPO / "graph" / "index"
OUT_DIR = REPO / "working" / "quote-census"

DEGREE_CAP = 150
THEME_BOOST = 60
POV_BOOST = 150
MARQUEE_BOOST = 75
MARQUEE_DEGREE = 40

# POV-character node slugs (all five published novels; prologue/epilogue POVs
# included where a character node exists).
POV_SLUGS = {
    "bran-stark", "catelyn-stark", "daenerys-targaryen", "eddard-stark",
    "jon-snow", "arya-stark", "tyrion-lannister", "sansa-stark",
    "theon-greyjoy", "davos-seaworth", "jaime-lannister", "samwell-tarly",
    "brienne-tarth", "cersei-lannister", "aeron-greyjoy",
    "victarion-greyjoy", "asha-greyjoy", "areo-hotah", "arys-oakheart",
    "arianne-martell", "quentyn-martell", "jon-connington",
    "barristan-selmy", "melisandre", "kevan-lannister", "merrett-frey",
    "varamyr", "cressen", "chett", "pate-novice",
}

_FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def parse_frontmatter(text: str) -> dict[str, str]:
    m = _FM_RE.match(text)
    fields: dict[str, str] = {}
    if not m:
        return fields
    for line in m.group(1).splitlines():
        km = re.match(r"^(\w[\w_]*):\s*(.*)$", line)
        if km:
            fields[km.group(1)] = km.group(2).strip().strip('"')
    return fields


def has_curated_quotes(text: str) -> bool:
    """True iff `## Quotes` exists and holds at least one `> ` blockquote line."""
    m = re.search(r"^## Quotes\s*$", text, re.M)
    if not m:
        return False
    body = text[m.end():]
    nxt = re.search(r"^## ", body, re.M)
    if nxt:
        body = body[: nxt.start()]
    return any(l.lstrip().startswith(">") and l.lstrip(">").strip()
               for l in body.splitlines())


def load_degrees() -> Counter:
    deg: Counter = Counter()
    with EDGES_FILE.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get("decision", "emit_edge") != "emit_edge":
                continue
            s, t = row.get("source_slug"), row.get("target_slug")
            if s:
                deg[s] += 1
            if t:
                deg[t] += 1
    return deg


def load_themes() -> dict[str, list[str]]:
    themes: dict[str, list[str]] = defaultdict(list)
    data = json.loads(THEME_INDEX.read_text())
    for theme_name, blob in data.get("themes", {}).items():
        for member in blob.get("members", []):
            themes[member["slug"]].append(theme_name)
    return {k: sorted(v) for k, v in themes.items()}


def index_mention_count(category: str, slug: str) -> int:
    p = INDEX_DIR / category / f"{slug}.index.json"
    if not p.exists():
        return 0
    try:
        d = json.loads(p.read_text())
    except json.JSONDecodeError:
        return 0
    return int(d.get("stats", {}).get("appearances_total", 0) or 0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=200,
                    help="rows in the ranked worklist table")
    args = ap.parse_args()

    degrees = load_degrees()
    themes = load_themes()

    rows = []
    for path in sorted(NODES_DIR.rglob("*.node.md")):
        rel = path.relative_to(NODES_DIR)
        if rel.parts[0] == "_conflicts":
            continue
        category = rel.parts[0]
        text = path.read_text()
        fm = parse_frontmatter(text)
        slug = fm.get("slug") or path.name.removesuffix(".node.md")
        name = fm.get("name") or slug
        deg = degrees.get(slug, 0)
        node_themes = themes.get(slug, [])
        is_pov = slug in POV_SLUGS
        is_marquee = category == "events" and deg >= MARQUEE_DEGREE
        score = (min(deg, DEGREE_CAP)
                 + THEME_BOOST * len(node_themes)
                 + (POV_BOOST if is_pov else 0)
                 + (MARQUEE_BOOST if is_marquee else 0))
        rows.append({
            "slug": slug,
            "name": name,
            "category": category,
            "type": fm.get("type", ""),
            "has_quotes": has_curated_quotes(text),
            "degree": deg,
            "themes": node_themes,
            "is_pov": is_pov,
            "is_marquee_event_hub": is_marquee,
            "index_mentions": index_mention_count(category, slug),
            "score": score,
            "node_path": str(path.relative_to(REPO)),
        })

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with (OUT_DIR / "quote-census-full.jsonl").open("w") as fh:
        for r in sorted(rows, key=lambda r: (-r["score"], r["slug"])):
            fh.write(json.dumps(r, sort_keys=True) + "\n")

    # Coverage stats by category
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_cat[r["category"]].append(r)

    quoteless = [r for r in rows if not r["has_quotes"]]
    quoteless.sort(key=lambda r: (-r["score"], r["slug"]))

    lines = [
        "# Quote-Mint Worklist (ranked, re-runnable)",
        "",
        "> Generated by `scripts/quote_census.py` — re-run after each minting",
        "> slice; this file is overwritten in place. Ranking =",
        f"> `min(degree,{DEGREE_CAP}) + {THEME_BOOST}*theme_count + {POV_BOOST}*POV + {MARQUEE_BOOST}*marquee-event-hub(degree>={MARQUEE_DEGREE})`.",
        "> `idx` = appearances_total from the entity index (mention pointers",
        "> available); foods also have `working/query-layer/food-grep-candidates.md`.",
        "",
        "## Coverage by category",
        "",
        "| category | nodes | with quotes | coverage |",
        "|---|---|---|---|",
    ]
    for cat in sorted(by_cat):
        cat_rows = by_cat[cat]
        n = len(cat_rows)
        q = sum(1 for r in cat_rows if r["has_quotes"])
        lines.append(f"| {cat} | {n} | {q} | {q / n:.1%} |")
    total = len(rows)
    total_q = sum(1 for r in rows if r["has_quotes"])
    lines.append(f"| **all** | {total} | {total_q} | {total_q / total:.1%} |")

    lines += [
        "",
        f"## Top {args.top} quote-less nodes by score",
        "",
        "| # | slug | category | deg | themes | POV | hub | idx | score |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(quoteless[: args.top], 1):
        lines.append(
            f"| {i} | `{r['slug']}` | {r['category']} | {r['degree']} "
            f"| {', '.join(r['themes']) or '—'} "
            f"| {'✓' if r['is_pov'] else ''} "
            f"| {'✓' if r['is_marquee_event_hub'] else ''} "
            f"| {r['index_mentions']} | {r['score']} |"
        )
    lines.append("")
    (OUT_DIR / "quote-worklist.md").write_text("\n".join(lines))

    print(f"nodes: {total}  with-quotes: {total_q} ({total_q / total:.1%})  "
          f"quote-less: {len(quoteless)}")
    print(f"worklist: {OUT_DIR / 'quote-worklist.md'}")
    missing_pov = POV_SLUGS - {r["slug"] for r in rows}
    if missing_pov:
        print(f"WARNING: POV slugs with no node file: {sorted(missing_pov)}")


if __name__ == "__main__":
    main()
