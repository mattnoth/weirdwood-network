"""braid.py — fork-hub / join-hub / braid analysis over the causal(+ENABLES)
edge layer (query-layer Track, step 7 — un-defers the S117 convergence-map
charter: `graph/convergence-maps/README.md`).

Pure DAG analysis. No LLM, no graph mutation, no chat port (full-profile only
by design — see design.md's operation table and the charter's own "Pure DAG
analysis; no LLM" line).

Three primitives:

  - `fork_hubs(edges, min_out=2, ...)` — divergence hubs: nodes whose OUTGOING
    causal(+ENABLES) degree is >= min_out, ranked by out-degree descending.
    The charter's own tooling sketch names this exactly: "fork nodes
    (out-degree >= 2 in causal edges)".
  - `join_hubs(edges, min_in=2, ...)` — convergence points: the in-degree
    analog. The charter frames these as "exactly the nodes we refuse to chain
    *into*" at the multi-attributed HARD-STOP tier — this function does not
    enforce that stop (it's a read-only report), it just surfaces the in-degree
    ranking so a caller/human can see which nodes the HARD-STOP already
    protects and which softer joins exist beneath it.
  - `braid(slugs, edges, ...)` — for 2+ endpoint (usually terminal-event)
    slugs: walk each one's upstream AND downstream causal trees, then report
    where they overlap: shared ancestors (a common upstream node = a
    divergence point the strands forked FROM), shared descendants (a common
    downstream node = a convergence point the strands feed INTO), and the
    offset/shared-middle overlap (a node reachable both upstream of one
    strand and downstream of another, or present in both strands' full
    causal component — the "shared spine" case). See the charter's three
    named shapes (divergence / convergence / offset) in
    `graph/convergence-maps/README.md`.

Design decisions this module had to make where the charter under-specified
(documented here per the step-7 mission's "where it under-specifies, decide
sensibly and document" instruction — also restated in the braid.py docstring
so a future session doesn't have to re-derive them from the mission prompt):

  1. **Edge set default.** Charter tooling sketch says "--braid" walks "all
     chains" without pinning CAUSAL vs FULL_CHAIN. Decision: default to
     CAUSAL_EDGE_TYPES (CAUSES/TRIGGERS/MOTIVATES) — the same default
     `causal_chain()` uses — with an explicit `--include-enables` /
     `include_enables=True` opt-in to widen to FULL_CHAIN_EDGE_TYPES,
     mirroring the existing `chain` / `full-chain` split so braid's default
     output is directly comparable to a plain `chain` walk.
  2. **What counts as a "shared ancestor" / "shared descendant".** The
     charter's convergence shape explicitly HARD-STOPS before
     multi-attributed termini like `war-of-the-five-kings` — i.e. it does not
     want every braid announcing "everything converges on the big war".
     Decision: `braid()` reports shared ancestors/descendants as a plain set
     intersection (it is a read-only report, not a chain-building tool that
     enforces the hard-stop), but the text/JSON render explicitly labels
     shared nodes with their combined in-degree/out-degree from `join_hubs`/
     `fork_hubs` so a caller can visually distinguish "a meaningful two-cause
     convergence" from "a graph-wide super-hub that everything touches" —
     the same judgment call a human applying the charter's hard-stop would
     make by eye. No node is silently dropped; the render just annotates.
  3. **Offset / shared-middle definition.** The charter's shape 3 ("two
     chains run through a common segment but enter/exit at different
     points") is defined here as: a node present in **both** strand A's full
     reachable set (its upstream union downstream) **and** strand B's full
     reachable set, that is NOT already reported as a shared ancestor (in
     both upstreams) or shared descendant (in both downstreams) — i.e. it's
     upstream of one strand and downstream of the other (or vice versa),
     meaning the strands cross through it in opposite roles. This is the
     residual/third category after ancestors and descendants are removed.
  4. **N-ary braid (3+ endpoints).** The charter's prose only illustrates
     2-endpoint braids, but the mission and tooling sketch both say
     "`braid A B [C…]`". Decision: generalize shared-ancestor/descendant to
     the intersection across ALL given strands (every strand must reach the
     node), and additionally report pairwise offset overlaps per strand pair
     (an N-ary "all strands share this" bar is often empty once N>2, while
     pairwise offsets remain informative) — see `pairwise` in the result.
  5. **Per-strand chain output.** "output a structured result: per-strand
     chains + shared hubs" (mission) — each strand's own causal_chain() dict
     is included verbatim (`per_strand[slug] = causal_chain(slug, ...)`) so
     callers get the full upstream/downstream edge lists for that endpoint,
     not just the summarized overlap sets.
  6. **fork_hubs / join_hubs node filter.** The charter's "the hairnet is a
     divergence hub" example measures fan-out on a single node's DIRECT
     causal out-degree (verified against the live graph: 1 direct CAUSES
     edge from the hairnet node itself, but ~20-29 nodes in its transitive
     downstream — see the worked example in the mission's verification
     section). Decision: `fork_hubs`/`join_hubs` rank by DIRECT degree (not
     transitive reach) — this matches the charter's own tooling-sketch
     wording ("ranked by downstream fan-out") read as direct fan-out, is
     O(E) instead of O(V*E), and gives a decidable, single definition of
     "hub" that `braid()`'s shared-ancestor/descendant report can then
     augment with transitive-reach counts if a caller wants context. Direct
     out-degree ranking surfaces `gregor-confesses-and-kills-oberyn` (out=2)
     and larger structural hubs like `battle-of-the-blackwater` (out=4)
     ahead of the hairnet itself (out=1, but huge transitive reach) — this
     divergence between "direct fan-out" and "transitive reach" is real and
     worth a caller's attention, so `fork_hubs`'s text render also prints
     each hub's transitive downstream-node count alongside its direct
     out-degree.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from .traverse import CAUSAL_EDGE_TYPES, FULL_CHAIN_EDGE_TYPES, _walk_causal, causal_chain, node_header

# ---------------------------------------------------------------------------
# fork_hubs / join_hubs — direct causal(+ENABLES) degree ranking
# ---------------------------------------------------------------------------

DEFAULT_MIN_OUT = 2
DEFAULT_MIN_IN = 2
HUB_TOP_N = 50


def _edge_set(include_enables: bool) -> frozenset[str]:
    return FULL_CHAIN_EDGE_TYPES if include_enables else CAUSAL_EDGE_TYPES


def _direct_degree(edges: list[dict], edge_types: frozenset[str]) -> tuple[dict[str, int], dict[str, int]]:
    """Return (out_degree, in_degree) dicts over the given edge_types,
    counting DIRECT edges only (not transitive reach) — see design decision
    #6 in the module docstring."""
    out_degree: dict[str, int] = defaultdict(int)
    in_degree: dict[str, int] = defaultdict(int)
    for e in edges:
        if e.get("edge_type") not in edge_types:
            continue
        src, tgt = e.get("source_slug"), e.get("target_slug")
        if src:
            out_degree[src] += 1
        if tgt:
            in_degree[tgt] += 1
    return out_degree, in_degree


def fork_hubs(
    edges: list[dict],
    *,
    min_out: int = DEFAULT_MIN_OUT,
    include_enables: bool = False,
    top_n: int = HUB_TOP_N,
) -> dict[str, Any]:
    """Divergence hubs: nodes whose DIRECT outgoing causal(+ENABLES) degree
    is >= min_out, ranked by out-degree descending (ties broken by slug).
    Each entry also carries `downstream_reach` — the size of the node's
    transitive downstream set — as context (see design decision #6)."""
    edge_types = _edge_set(include_enables)
    out_degree, _ = _direct_degree(edges, edge_types)

    hubs = [
        {"slug": slug, "out_degree": deg}
        for slug, deg in out_degree.items()
        if deg >= min_out
    ]
    hubs.sort(key=lambda h: (-h["out_degree"], h["slug"]))
    hubs = hubs[:top_n]

    for h in hubs:
        downstream = _walk_causal(h["slug"], edges, direction="down", edge_types=edge_types)
        h["downstream_reach"] = len({e["target_slug"] for e in downstream})
        h["node_header"] = node_header(h["slug"])

    return {
        "op": "fork-hubs",
        "min_out": min_out,
        "include_enables": include_enables,
        "edge_types": sorted(edge_types),
        "count": len(hubs),
        "hubs": hubs,
    }


def join_hubs(
    edges: list[dict],
    *,
    min_in: int = DEFAULT_MIN_IN,
    include_enables: bool = False,
    top_n: int = HUB_TOP_N,
) -> dict[str, Any]:
    """Convergence points: nodes whose DIRECT incoming causal(+ENABLES)
    degree is >= min_in, ranked by in-degree descending. See the charter's
    framing: these are exactly the multi-attributed nodes the causal-chain
    build refuses to chain INTO past the hard-stop tier — this function
    reports the ranking, it does not enforce the stop (read-only)."""
    edge_types = _edge_set(include_enables)
    _, in_degree = _direct_degree(edges, edge_types)

    hubs = [
        {"slug": slug, "in_degree": deg}
        for slug, deg in in_degree.items()
        if deg >= min_in
    ]
    hubs.sort(key=lambda h: (-h["in_degree"], h["slug"]))
    hubs = hubs[:top_n]

    for h in hubs:
        upstream = _walk_causal(h["slug"], edges, direction="up", edge_types=edge_types)
        h["upstream_reach"] = len({e["source_slug"] for e in upstream})
        h["node_header"] = node_header(h["slug"])

    return {
        "op": "join-hubs",
        "min_in": min_in,
        "include_enables": include_enables,
        "edge_types": sorted(edge_types),
        "count": len(hubs),
        "hubs": hubs,
    }


# ---------------------------------------------------------------------------
# braid(slugs) — overlap analysis across 2+ strands
# ---------------------------------------------------------------------------

def _reach_sets(slug: str, edges: list[dict], edge_types: frozenset[str]) -> tuple[set[str], set[str]]:
    """Return (upstream_nodes, downstream_nodes) — the transitive causal
    reach of `slug` in each direction, NOT including `slug` itself."""
    upstream = _walk_causal(slug, edges, direction="up", edge_types=edge_types)
    downstream = _walk_causal(slug, edges, direction="down", edge_types=edge_types)
    return (
        {e["source_slug"] for e in upstream},
        {e["target_slug"] for e in downstream},
    )


def braid(
    slugs: list[str],
    edges: list[dict],
    *,
    include_enables: bool = False,
) -> dict[str, Any]:
    """Braid 2+ endpoint slugs: find shared ancestors (divergence points),
    shared descendants (convergence points), and offset/shared-middle
    overlap. See design decisions #2-#5 in the module docstring for exactly
    what each category means and how N-ary (3+) braids are handled."""
    edge_types = _edge_set(include_enables)

    if len(slugs) < 2:
        return {
            "op": "braid",
            "error": f"braid requires at least 2 slugs, got {len(slugs)}",
            "slugs": slugs,
        }

    per_strand: dict[str, dict] = {}
    upstream_sets: dict[str, set[str]] = {}
    downstream_sets: dict[str, set[str]] = {}
    full_reach: dict[str, set[str]] = {}

    for slug in slugs:
        up, down = _reach_sets(slug, edges, edge_types)
        upstream_sets[slug] = up
        downstream_sets[slug] = down
        full_reach[slug] = up | down | {slug}
        per_strand[slug] = causal_chain(slug, edges, edge_types=edge_types)

    # Shared ancestors: nodes upstream of EVERY strand (all-strand intersection).
    shared_ancestors = set.intersection(*upstream_sets.values()) if upstream_sets else set()
    # Shared descendants: nodes downstream of EVERY strand.
    shared_descendants = set.intersection(*downstream_sets.values()) if downstream_sets else set()

    # Offset / shared-middle (design decision #3): nodes present in 2+
    # strands' full reach sets, that are NOT already counted as a shared
    # ancestor or shared descendant of ALL strands, restricted to residual
    # pairwise crossings (upstream-of-one / downstream-of-another, or a
    # partial-but-not-universal overlap).
    pairwise: list[dict] = []
    for i in range(len(slugs)):
        for j in range(i + 1, len(slugs)):
            a, b = slugs[i], slugs[j]
            pair_shared_ancestors = upstream_sets[a] & upstream_sets[b]
            pair_shared_descendants = downstream_sets[a] & downstream_sets[b]
            # a's upstream that is b's downstream (b feeds into a's cause tree)
            a_up_b_down = upstream_sets[a] & downstream_sets[b]
            b_up_a_down = upstream_sets[b] & downstream_sets[a]
            offset = (a_up_b_down | b_up_a_down) - pair_shared_ancestors - pair_shared_descendants
            pairwise.append({
                "a": a,
                "b": b,
                "shared_ancestors": sorted(pair_shared_ancestors),
                "shared_descendants": sorted(pair_shared_descendants),
                "offset_shared_middle": sorted(offset),
            })

    def _annotate(nodes: set[str]) -> list[dict]:
        out = []
        for slug in sorted(nodes):
            out.append({"slug": slug, "node_header": node_header(slug)})
        return out

    return {
        "op": "braid",
        "slugs": slugs,
        "include_enables": include_enables,
        "edge_types": sorted(edge_types),
        "shared_ancestors": _annotate(shared_ancestors),
        "shared_descendants": _annotate(shared_descendants),
        "pairwise": pairwise,
        "per_strand": per_strand,
    }
