#!/usr/bin/env python3
"""S152 harvest pass — route each open row to a disjoint owner (S139 pattern).

Owners (disjoint node-dir ownership → zero write-collision when run in parallel):
  FOODS  : graph/nodes/foods/                                  (food, drink)
  CHARS  : graph/nodes/characters/, species/                   (appearance, char-voice, char-homed desc/quote/fore)
  EVENTS : events/ locations/ artifacts/ materials/ texts/     (place, object, hospitality, song, event-homed desc/quote/fore)
           medical/ customs/ prophecies/ religions/ factions/
  EDGES  : orchestrator handles → candidates.json              (relationship, edge, seam, witness, node, node-type, gated)

Ambiguous kinds (description/quote/foreshadowing/other) default to CHARS unless their
queue-line is in EVENTS_OVERRIDE (event/place/object/medical/faction-homed) or EDGE_OVERRIDE.
Dir-ownership + handback rule is the safety net: an agent that finds a row's true home in a
foreign dir appends it to handback.md instead of attaching — so a misroute can never collide.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROWS = REPO / "working" / "harvest-pass-s152" / "rows.json"
OUTDIR = REPO / "working" / "harvest-pass-s152"

FOODS_KINDS = {"food", "drink"}
CHARS_KINDS = {"appearance", "character-voice"}
EVENTS_KINDS = {"place", "object", "hospitality", "song", "location", "detail", "guest-right"}
EDGE_KINDS = {"relationship", "edge", "seam", "seam/foreshadowing", "witness", "node", "node-type"}
AMBIG_KINDS = {"description", "quote", "foreshadowing", "other"}

# Ambiguous rows whose true home is an event/place/object/medical/faction/text node (Opus triage):
EVENTS_OVERRIDE = {
    354, 356, 519, 520, 524, 547, 552, 559, 560, 564, 565, 566, 567,
    583, 584, 587, 607, 612, 640, 644, 645, 652, 675, 726, 727, 728, 729, 735,
}
# Ambiguous rows that are genuine edge/gated decisions for the orchestrator:
EDGE_OVERRIDE = {551}  # gravedigger=Sandor gated-identity foreshadowing


def route(r):
    k = r["kind"]
    if k in FOODS_KINDS:
        return "FOODS"
    if k in EDGE_KINDS:
        return "EDGES"
    if k in CHARS_KINDS:
        return "CHARS"
    if k in EVENTS_KINDS:
        return "EVENTS"
    if k in AMBIG_KINDS:
        if r["qline"] in EDGE_OVERRIDE:
            return "EDGES"
        if r["qline"] in EVENTS_OVERRIDE:
            return "EVENTS"
        return "CHARS"
    raise SystemExit(f"Unrouted kind {k!r} at qline {r['qline']}")


def main():
    rows = json.loads(ROWS.read_text())
    for r in rows:
        r["route"] = route(r)
    ROWS.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")

    buckets = {"FOODS": [], "CHARS": [], "EVENTS": [], "EDGES": []}
    for r in rows:
        buckets[r["route"]].append(r)

    for name, rs in buckets.items():
        lines = [f"# S152 harvest — {name} work-list ({len(rs)} rows)\n"]
        # group by chapter for cheap one-open-per-file traversal
        by_chap = {}
        for r in rs:
            by_chap.setdefault(r["chapter"], []).append(r)
        for chap in sorted(by_chap):
            lines.append(f"\n## {chap}")
            for r in by_chap[chap]:
                lines.append(f"- [q{r['qline']}] `{r['cite']}` [{r['kind']}] {r['note']}")
        (OUTDIR / f"route-{name.lower()}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Routing complete:")
    for name, rs in buckets.items():
        print(f"  {name}: {len(rs)}")
    print(f"  TOTAL: {sum(len(v) for v in buckets.values())}")


if __name__ == "__main__":
    main()
