#!/usr/bin/env python3
"""compile-recover-maps.py — S208. Materialize per-unit recover maps from
curation-decisions.json (+ events-decisions.json when present) against the actual
quarantined (unit,name) universe. Validates every target slug exists; flags unmatched
decision keys (typos) loudly. Writes recover-maps/<unit>.json + a compile report.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

rows = json.loads((HERE / "quarantined-rows.json").read_text(encoding="utf-8"))
cur = json.loads((HERE / "curation-decisions.json").read_text(encoding="utf-8"))
events_path = HERE / "events-decisions.json"
events = json.loads(events_path.read_text(encoding="utf-8")) if events_path.exists() else []

existing = {p.name[: -len(".node.md")] for p in (REPO / "graph" / "nodes").glob("**/*.node.md")}

universe = {(u, n) for u, names in rows.items() for n in names}

maps: dict[str, dict] = defaultdict(dict)
dropped: list = []
unmatched: list = []
bad_slugs: list = []

# layer 1: global
for name, val in cur["global"].items():
    hits = [(u, n) for (u, n) in universe if n == name]
    if not hits:
        unmatched.append(("global", name))
        continue
    for u, n in hits:
        if val == "DROP":
            dropped.append((u, n, "curation-global"))
        else:
            if val != "CREATE" and val not in existing:
                bad_slugs.append((name, val))
                continue
            maps[u][n] = val

# layer 2: per-unit overrides
for key, val in cur["per_unit"].items():
    u, _, name = key.partition("|")
    if (u, name) not in universe:
        unmatched.append(("per_unit", key))
        continue
    if val == "DROP":
        maps[u].pop(name, None)
        dropped.append((u, name, "curation-per-unit"))
    else:
        if val != "CREATE" and val not in existing:
            bad_slugs.append((key, val))
            continue
        maps[u][name] = val

# layer 3: events decisions (subagent triage, list of {unit,name,decision})
# A MAP may target a PENDING mint — a slug an earlier-sorted unit's CREATE will
# produce before the mapping unit runs (the driver runs units in sorted order).
import re as _re0

def _slug0(name: str) -> str:
    s = name.lower().replace("'", "")
    return _re0.sub(r"[^a-z0-9]+", "-", s).strip("-")

pending_creator: dict[str, str] = {}
for r in events:
    if r["decision"] == "CREATE":
        sl = _slug0(r["name"])
        if sl not in pending_creator or r["unit"] < pending_creator[sl]:
            pending_creator[sl] = r["unit"]

ev_counts = defaultdict(int)
for r in events:
    u, name, dec = r["unit"], r["name"], r["decision"]
    if (u, name) not in universe:
        unmatched.append(("events", f"{u}|{name}"))
        continue
    if dec.startswith("MAP:"):
        slug = dec[4:]
        if slug not in existing:
            if slug in pending_creator and pending_creator[slug] < u:
                ev_counts["map-to-pending-mint"] += 1
            else:
                bad_slugs.append((f"{u}|{name}", slug))
                continue
        maps[u][name] = slug
        ev_counts["map"] += 1
    elif dec == "CREATE":
        maps[u][name] = "CREATE"
        ev_counts["create"] += 1
    elif dec.startswith("COLLIDE"):
        ev_counts["collide"] += 1
        dropped.append((u, name, "events-collide-needs-premint"))
    else:  # DROP:*
        ev_counts["drop"] += 1
        dropped.append((u, name, dec[:60]))

if bad_slugs:
    print("ABORT — decision targets that are not existing node slugs:")
    for k, v in bad_slugs:
        print(f"  {k} -> {v}")
    sys.exit(1)

# ---- CREATE slug-collision detection ----
# (a) two CREATE names in different units slugify identically: if they are the SAME
#     occurrence, the later unit must MAP to the first unit's mint; if different
#     occurrences, one needs a manual distinct-slug premint. Units run in sorted
#     order, so the first sorted unit's CREATE lands and later ones would quarantine
#     on routing-bug-create-slug-exists. Resolutions live in curation-decisions.json
#     under "create_collisions": {"<slugified>": "same" | "different"} — "same"
#     auto-flips later units to MAP:<slug>; "different"/absent -> flagged loudly.
# (b) a CREATE whose slugified name already exists as a node: would quarantine.
import re as _re

def _slugify(name: str) -> str:
    s = name.lower().replace("'", "")
    return _re.sub(r"[^a-z0-9]+", "-", s).strip("-")

collision_notes = cur.get("create_collisions", {})
creates_by_slug = defaultdict(list)
for u in maps:
    for n, v in maps[u].items():
        if v == "CREATE":
            creates_by_slug[_slugify(n)].append((u, n))
flagged = []
for slug, insts in sorted(creates_by_slug.items()):
    if slug in existing:
        flagged.append(f"CREATE would collide with EXISTING node: {slug} <- {insts}")
        continue
    if len(insts) > 1:
        note = collision_notes.get(slug)
        if note == "same":
            insts_sorted = sorted(insts)
            for u, n in insts_sorted[1:]:
                # later units map onto the first unit's mint; mint's dedup + the
                # router's update path handle the rest.
                maps[u][n] = slug
                ev_counts["collision-flip-to-map"] += 1
        else:
            flagged.append(f"CREATE slug collision across units ({slug}): {insts} — "
                           f"adjudicate in create_collisions as 'same' or premint a distinct slug")
if flagged:
    print("CREATE COLLISIONS NEEDING ADJUDICATION:")
    for f in flagged:
        print(f"  {f}")
    sys.exit(1)

out_dir = HERE / "recover-maps"
out_dir.mkdir(exist_ok=True)
for old in out_dir.glob("*.json"):
    old.unlink()
n_names = 0
for u in sorted(maps):
    if not maps[u]:
        continue
    (out_dir / f"{u}.json").write_text(
        json.dumps(maps[u], indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    n_names += len(maps[u])

report = {
    "units_with_maps": len([u for u in maps if maps[u]]),
    "mapped_name_instances": n_names,
    "creates": sum(1 for u in maps for n in maps[u] if maps[u][n] == "CREATE"),
    "dropped_instances": len(dropped),
    "events_triage": dict(ev_counts),
    "unmatched_decision_keys": [f"{a}:{b}" for a, b in unmatched],
    "dropped": [f"{u}|{n} ({r})" for u, n, r in dropped],
}
(HERE / "compile-report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"units: {report['units_with_maps']}  mapped name-instances: {n_names} "
      f"(CREATE {report['creates']})  dropped: {len(dropped)}")
print(f"events triage: {dict(ev_counts)}")
if unmatched:
    print(f"UNMATCHED decision keys ({len(unmatched)}) — check for typos:")
    for a, b in unmatched:
        print(f"  [{a}] {b}")
