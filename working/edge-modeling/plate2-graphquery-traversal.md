# Plate 2 / 2b — `graph-query.py` traversal check

**Generated:** 2026-06-05, Session 83
**Question:** Can `scripts/graph-query.py` transparently traverse
`person → event → person` so "who killed Robb" works at 2 hops once Plate 3 lands
the role edges (`AGENT_IN`, `VICTIM_IN`) on event-node hubs?

**Verdict — YES, definitively, with no node-type filtering anywhere in the
traversal code.** Reification alone is enough to make 2-hop person→event→person
queries work. No materialized dyad is required to keep the headline query
working.

---

## Evidence — read of the source

### `cmd_path(slug_a, slug_b, edges)` — `scripts/graph-query.py:782–906`

The `--path` command computes 2-hop bridges between two slugs by intersecting
their neighbor sets *over the entire `edges.jsonl` list, untyped*:

```python
# scripts/graph-query.py:794-809
neighbors_a: dict[str, list[dict]] = defaultdict(list)
for e in edges:
    if e.get("source_slug") == slug_a:
        neighbors_a[e["target_slug"]].append(e)
    elif e.get("target_slug") == slug_a:
        neighbors_a[e["source_slug"]].append(e)

neighbors_b: dict[str, list[dict]] = defaultdict(list)
for e in edges:
    if e.get("source_slug") == slug_b:
        neighbors_b[e["target_slug"]].append(e)
    elif e.get("target_slug") == slug_b:
        neighbors_b[e["source_slug"]].append(e)

# Common neighbors (bridges), excluding slug_a and slug_b themselves
bridge_slugs = (set(neighbors_a.keys()) & set(neighbors_b.keys())) - {slug_a, slug_b}
```

There is **no filter on `edge_type`**, **no filter on intermediate node type**,
and **no constraint that the bridge be a character**. Any slug that appears
in both neighbor sets — character, house, location, **event**, artifact,
faction, theory — is reported as a bridge.

The bridge gets a "leg description" via `_format_arrow()` (lines 919-927) which
joins the edge types into a single bar-separated label and prints them. So when
Plate 3 lands `walder-frey AGENT_IN red-wedding` and `robb-stark VICTIM_IN
red-wedding`, the `--path walder-frey robb-stark` invocation will render that
bridge as:

```
walder-frey --[AGENT_IN]--> red-wedding  --[red-wedding]--  red-wedding <-[VICTIM_IN]-- robb-stark
```

### `cmd_neighbors(slug, edges)` — `scripts/graph-query.py:676–755`

Likewise untyped: enumerates all edges where `slug` is `source_slug` or
`target_slug`, groups by `edge_type`. No constraint on the *other* endpoint's
node type. Asking `--neighbors red-wedding` after Plate 3 will list every
participant with their role edge directly.

### What `--path` does *not* do

- It does NOT walk N-hop paths (k > 2). The only multi-hop mode is the 2-hop
  bridge intersection.
- It does NOT exclude intermediates by type. (We checked: no `if intermediate
  in {"character.*"}` style guard anywhere in the function.)
- It does NOT score paths or prefer certain edge types. All bridges are
  returned, ranked by `a_edge_count + b_edge_count`.

The 2-hop limit is the only real constraint — and **reification keeps the
person→person relationship a 2-hop walk** (`person → event → person`), so it
fits exactly within `--path`'s reach.

---

## Evidence — live probe

### Probe 1: existing 2-hop walk through a location node

Two characters who already share a non-character bridge (`winterfell`,
`location.castle`):

```
$ python3 scripts/graph-query.py --path eddard-stark robb-stark
...
2-HOP BRIDGES (14 common neighbors)
...
  eddard-stark --[SEEKS]--> winterfell  --[winterfell]--  robb-stark --[HEIR_TO|RULES]--> winterfell
  eddard-stark <-[TRUSTS]-> luwin  --[luwin]--  robb-stark --[TRUSTS]--> luwin
  ...
```

`winterfell` is a `location.castle` node. The traversal hops through it without
hesitation. This is the *exact same* mechanism that will hop through
`event.battle` once role edges land.

### Probe 2: existing 2-hop walk through a house node

The same query surfaces `house-frey` and `stannis-baratheon` as bridges between
`robb-stark` and `roose-bolton`:

```
$ python3 scripts/graph-query.py --path robb-stark roose-bolton
...
2-HOP BRIDGES (12 common neighbors)
  robb-stark <-[BETRAYS|CONTRACTED_WITH|GUEST_OF|SERVES|VIOLATES_GUEST_RIGHT]-> walder-frey  --[walder-frey]--  roose-bolton --[OPPOSES]--> walder-frey
  ...
  robb-stark <-[ALLIES_WITH|BREAKS_VOW|VIOLATES_GUEST_RIGHT]-> house-frey  --[house-frey]--  roose-bolton <-[ALLIES_WITH|GUEST_OF|VIOLATES_GUEST_RIGHT]-> house-frey
  robb-stark <-[GUEST_OF|OVERLORD_OF]-> hornwood  --[hornwood]--  roose-bolton --[CLAIMS]--> hornwood
  stannis-baratheon --[RESPECTS]--> robb-stark  --[stannis-baratheon]--  roose-bolton <-[OPPOSES]-> stannis-baratheon
```

Note `house-frey` (`house.*`) and `hornwood` (likely `location.*` or `house.*`)
appear as bridges. **No type filtering occurs.**

### Probe 3: event nodes — the *current* state (post-Plate-3 baseline)

```
$ python3 scripts/graph-query.py --neighbors red-wedding
...
OUTGOING (0 edges — red-wedding is source)
  (none)
INCOMING (0 edges — red-wedding is target)
  (none)
SUMMARY: red-wedding  |  0 outgoing, 0 incoming  (0 total)
```

This is the §1 worked example confirmed live: `red-wedding` has zero edges in
`edges.jsonl` today. The `_summary.json` `out_edge_count: 3` and `in_edge_count:
308` come from a *different* layer (the `## Edges` bullets in the node markdown
file, which are not synced with `edges.jsonl` — design doc §1).

```
$ python3 scripts/graph-query.py --path robb-stark battle-of-the-blackwater
SUMMARY: robb-stark → battle-of-the-blackwater  |  0 direct edges, 0 2-hop bridges
```

Same story: event nodes are structural orphans in `edges.jsonl`. Plate 3 fills
the gap.

---

## What this means for D2

The decision in §3 D2 hinges on this exact question. From the design doc:

> The choice between (a) and (c) hinges on whether
> `graph/scripts/graph-query.py` can transparently traverse
> `person → event → person`. If it can, (a) is clean. If it can't, (c)'s
> materialized dyad is required to keep the project's headline query
> ("who killed X", "who betrayed Robb") working.

`--path` transparently traverses any 2-hop bridge regardless of intermediate
type. **Option (a) Replace is sufficient** to keep `--path A B` answering
"who killed/betrayed/captured X" via the hub.

The remaining caveat is presentation only: today `--path eddard-stark robb-stark`
surfaces 14 bridges; after Plate 3, more bridges will appear (every shared
event). That's a *richness* improvement, not a regression. If a UI consumer
wanted to filter for "only person-bridges" or "only event-bridges", it would
need a flag — but the underlying engine already serves both.

---

## Edge cases checked

- **`--neighbors` JSON output** (`_edges_to_neighbor_records`, lines 758-772):
  returns lean records of {edge_type, other_slug, evidence_ref, evidence_quote,
  confidence_tier}. No type filter. AGENT_IN/VICTIM_IN role edges will appear
  alongside KILLS/BETRAYS in the output.
- **`--health`**: structural — counts orphans, degree distribution. Not a
  traversal mode; irrelevant to D2.
- **Single-slug inspection mode** (`build_report`, line 413): renders one node
  with its outbound `## Edges` bullets + inbound cross-references. Hand-written
  bullets; not a traversal.

---

## Summary

| Question | Answer | Evidence |
|---|---|---|
| Does `--path` traverse person→event→person? | **YES** (untyped 2-hop bridge intersection) | `scripts/graph-query.py:794-809` |
| Does it filter by intermediate node type? | **NO** | no type guards in `cmd_path` or `cmd_neighbors` |
| Does it limit to person↔person edges? | **NO** | live probe shows location + house bridges already in use |
| Is the limitation structural or incidental? | Not a limitation — feature works out of the box | live probe through `winterfell`, `house-frey`, `hornwood` |
| Will the headline query "who killed Robb" still work after Plate 3 / option (a) Replace? | **YES** — `--path walder-frey robb-stark` will surface the `red-wedding` bridge with `AGENT_IN`/`VICTIM_IN` legs | code reading + behavior of probes |

**D2 unblocked → choose option (a) Replace.**
