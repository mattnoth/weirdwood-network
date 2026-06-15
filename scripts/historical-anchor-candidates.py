#!/usr/bin/env python3
"""
historical-anchor-candidates.py — POST-PLATE-5 followup #9 surfacing pass.

Finds isolated / near-isolated HISTORICAL event hubs and matches existing edges in
graph/edges/edges.jsonl whose evidence_quote or asserted_relation names the hub.
Those matched dyads are the attachment candidates: the underlying fact already exists
in the graph but is not connected to its parent historical-event hub.

Read-only. Emits a candidate report to stdout (and optionally JSON via --json).

Mechanic (per Mode 3 dip §6 Q5): e.g. rhaegar-targaryen CROWNS_QUEEN_OF_LOVE_AND_BEAUTY
lyanna-stark is cited with a quote naming Harrenhal, but tourney-at-harrenhal has 0 edges.
We surface that pairing so a verifier can mint the right attach edge (FIGHTS_IN / ATTENDS /
LOCATED_AT / SUB_BEAT_OF) onto the hub.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVENTS_DIR = ROOT / "graph" / "nodes" / "events"
EDGES = ROOT / "graph" / "edges" / "edges.jsonl"

# Historical-event hub signal: type and/or name keywords. We want pre/peri-narrative
# events whose facts come through POV recollection rather than on-page chapter beats.
HIST_TYPES = {"event.tournament", "event.battle", "event.war", "event.coronation"}
HIST_NAME_RE = re.compile(
    r"\b(tourney|tournament|battle|sack|rebellion|war|siege|conquest|dance|"
    r"trident|harrenhal|kingsmoot|greyjoy|blackfyre)\b",
    re.I,
)
# Degree threshold below which a hub is considered under-connected.
ISOLATED_MAX_DEGREE = 2

STOPWORDS = {
    "the", "of", "at", "a", "an", "and", "to", "in", "on", "for", "battle", "tourney",
    "tournament", "event", "war", "lord", "lady", "ser", "king", "queen", "prince",
    "honor", "wedding", "attack", "night", "long", "that", "never", "ends", "dance",
    "first", "second", "third", "great", "old", "new", "house", "siege", "field",
    "sons", "lords", "knights", "men", "north", "south", "good", "young", "little",
}
# A distinctive token must be rarer than this across the whole quote corpus to count
# as a hub-naming signal (filters out ubiquitous words; keeps place/proper nouns).
RARE_DF = 60


def load_frontmatter(path):
    txt = path.read_text(encoding="utf-8", errors="replace")
    if not txt.startswith("---"):
        return {}, txt
    end = txt.find("\n---", 3)
    if end == -1:
        return {}, txt
    fm_block = txt[3:end]
    fm = {}
    aliases = []
    in_aliases = False
    for line in fm_block.splitlines():
        if in_aliases:
            m = re.match(r"\s*-\s*(.+)", line)
            if m:
                aliases.append(m.group(1).strip().strip('"\''))
                continue
            in_aliases = False
        m = re.match(r"(\w+):\s*(.*)", line)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        if k == "aliases":
            if v.startswith("["):
                aliases = [x.strip().strip('"\'') for x in v.strip("[]").split(",") if x.strip()]
            else:
                in_aliases = True
            continue
        fm[k] = v.strip('"\'')
    fm["aliases"] = aliases
    return fm, txt


def hub_match_terms(slug, name, aliases):
    """Surface forms a quote might use to name this event."""
    terms = set()
    for s in [name, slug.replace("-", " ")] + list(aliases):
        s = (s or "").strip().lower()
        if s:
            terms.add(s)
    # distinctive single tokens (drop stopwords) — e.g. "harrenhal", "trident"
    toks = set()
    for t in list(terms):
        for w in re.split(r"[^a-z0-9]+", t):
            if w and w not in STOPWORDS and len(w) > 3:
                toks.add(w)
    return terms, toks


def main():
    as_json = "--json" in sys.argv

    # 1. degree map over all edges
    degree = defaultdict(int)
    edges = []
    with open(EDGES, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            edges.append(e)
            degree[e.get("source_slug")] += 1
            degree[e.get("target_slug")] += 1

    # 1b. document-frequency of every token across the quote+relation corpus,
    #     so we can keep only distinctive (rare) hub-naming tokens.
    token_df = defaultdict(int)
    edge_blobs = []
    for e in edges:
        blob = " ".join([
            str(e.get("evidence_quote", "")),
            str(e.get("asserted_relation", "")),
        ]).lower()
        edge_blobs.append(blob)
        for w in set(re.split(r"[^a-z0-9]+", blob)):
            if w and len(w) > 3 and w not in STOPWORDS:
                token_df[w] += 1

    # 2. identify isolated historical hubs
    hubs = {}
    for path in sorted(EVENTS_DIR.glob("*.node.md")):
        fm, _ = load_frontmatter(path)
        slug = fm.get("slug") or path.stem.replace(".node", "")
        typ = fm.get("type", "")
        name = fm.get("name", slug)
        aliases = fm.get("aliases", [])
        is_hist = typ in HIST_TYPES or HIST_NAME_RE.search(name) or HIST_NAME_RE.search(slug)
        if not is_hist:
            continue
        deg = degree.get(slug, 0)
        if deg > ISOLATED_MAX_DEGREE:
            continue
        terms, toks = hub_match_terms(slug, name, aliases)
        # keep only distinctive tokens: rare across the corpus, and present somewhere
        toks = {t for t in toks if 0 < token_df.get(t, 0) <= RARE_DF}
        if not toks and not any(len(t) > 12 for t in terms):
            # no distinctive single-token signal and no long distinctive phrase
            continue
        hubs[slug] = {
            "slug": slug, "name": name, "type": typ, "degree": deg,
            "aliases": aliases, "terms": terms, "toks": toks, "matches": [],
        }

    # 3. scan edges for quotes/relations that name a hub
    for e, blob in zip(edges, edge_blobs):
        if not blob.strip():
            continue
        for slug, h in hubs.items():
            hit = None
            for term in h["terms"]:
                if len(term) > 8 and term in blob:
                    hit = term
                    break
            if not hit:
                for tok in h["toks"]:
                    if re.search(r"\b" + re.escape(tok) + r"\b", blob):
                        hit = tok
                        break
            if hit:
                # don't re-surface an edge already touching the hub
                if e.get("source_slug") == slug or e.get("target_slug") == slug:
                    continue
                h["matches"].append({
                    "matched_on": hit,
                    "edge_type": e.get("edge_type"),
                    "source": e.get("source_slug"),
                    "target": e.get("target_slug"),
                    "tier": e.get("confidence_tier"),
                    "quote": e.get("evidence_quote", "")[:240],
                    "ref": e.get("evidence_ref")
                          or f'{e.get("evidence_chapter","")}',
                })

    out = [h for h in hubs.values() if h["matches"]]
    out.sort(key=lambda h: (-len(h["matches"]), h["degree"]))

    if as_json:
        for h in out:
            h.pop("terms"); h.pop("toks")
        print(json.dumps(out, indent=2))
        return

    print(f"# Historical-anchor candidates — {len(out)} hubs with attachable dyads")
    print(f"#   (isolated hist hubs scanned: {len(hubs)}; degree<= {ISOLATED_MAX_DEGREE})\n")
    for h in out:
        print(f"## {h['slug']}  [{h['type']}]  degree={h['degree']}  ({len(h['matches'])} candidate edges)")
        print(f"   name: {h['name']}  aliases: {h['aliases']}")
        for m in h["matches"][:12]:
            print(f"   - [{m['matched_on']}] {m['source']} --{m['edge_type']}--> {m['target']}  (T{m['tier']})")
            print(f"       \"{m['quote']}\"")
            print(f"       {m['ref']}")
        if len(h["matches"]) > 12:
            print(f"   ... +{len(h['matches'])-12} more")
        print()


if __name__ == "__main__":
    main()
