#!/usr/bin/env python3
"""graph-query.py — COMPAT SHIM over the consolidated query engine.

The real implementation now lives in the `weirwood_query` package at
graph/query/weirwood_query/ (query-layer Track, step 1). This file keeps the
exact old CLI surface and byte-identical stdout, and re-exports every symbol
the old module defined so existing imports and tests
(tests/_helpers.load_script("graph-query.py")) keep working unchanged.

NEW front door: `weirwood query <args>` (or
`PYTHONPATH=graph/query python3 -m weirwood_query.cli <args>`).

NODE INSPECTION (original modes):
  python3 scripts/graph-query.py <slug>
  python3 scripts/graph-query.py <slug> --edges-only
  python3 scripts/graph-query.py <slug> --inbound-only
  python3 scripts/graph-query.py <slug> --json

CANONICAL EDGE LAYER (graph/edges/edges.jsonl):
  python3 scripts/graph-query.py --neighbors <slug>
  python3 scripts/graph-query.py --path <slugA> <slugB>
  python3 scripts/graph-query.py --health
  python3 scripts/graph-query.py --event-participants <hub-slug>
  python3 scripts/graph-query.py --edges <path>   # override edges.jsonl location
  python3 scripts/graph-query.py --help

Monkeypatch note: the path globals below (NODES_DIR, CROSS_REFS_FILE,
ALIAS_RESOLVER_FILE, DEFAULT_EDGES_FILE) are honored by the wrapper functions
in this module — each wrapper reads the shim's global at CALL time and threads
it into the package function as an explicit parameter, so tests that set
`gq.NODES_DIR = tmp_path` still work.
"""

import argparse
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Make the engine package importable (graph/query is NOT pip-installed).
_ENGINE_DIR = str(PROJECT_ROOT / "graph" / "query")
if _ENGINE_DIR not in sys.path:
    sys.path.insert(0, _ENGINE_DIR)

from weirwood_query import cli as _cli            # noqa: E402
from weirwood_query import load as _load          # noqa: E402
from weirwood_query import normalize as _normalize  # noqa: E402
from weirwood_query import report as _report      # noqa: E402
from weirwood_query import traverse as _traverse  # noqa: E402

# Path globals — kept as SHIM-level globals so monkeypatching still works.
NODES_DIR = PROJECT_ROOT / "graph" / "nodes"
CROSS_REFS_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "cross-references.jsonl"
ALIAS_RESOLVER_FILE = PROJECT_ROOT / "working" / "wiki" / "data" / "alias-resolver.json"
DEFAULT_EDGES_FILE = PROJECT_ROOT / "graph" / "edges" / "edges.jsonl"

# ---------------------------------------------------------------------------
# Pure re-exports (functions of their arguments only — no hidden path state)
# ---------------------------------------------------------------------------
title_to_slug = _normalize.title_to_slug
parse_frontmatter = _load.parse_frontmatter
_simple_yaml_parse = _load._simple_yaml_parse
parse_edge_line = _report.parse_edge_line
extract_edges = _report.extract_edges_markdown  # old name preserved
load_edges = _load.load_edges                    # takes edges_path explicitly
_short_quote = _traverse._short_quote
_causal_brief = _traverse._causal_brief
_edge_label = _traverse._edge_label
_beats_for_node = _traverse._beats_for_node
_walk_causal = _traverse._walk_causal
_node_containers = _traverse._node_containers
_format_arrow = _cli._format_arrow
print_report = _cli.print_report
print_json = _cli.print_json

# Constants
CAUSAL_EDGE_TYPES = _traverse.CAUSAL_EDGE_TYPES
FULL_CHAIN_EDGE_TYPES = _traverse.FULL_CHAIN_EDGE_TYPES
ROLE_EDGE_TYPES = _traverse.ROLE_EDGE_TYPES
PARTICIPANT_ROLE_TYPES = _traverse.PARTICIPANT_ROLE_TYPES
BRIDGE_CAP = _traverse.BRIDGE_CAP
DEGREE_TOP_N = _traverse.DEGREE_TOP_N


# ---------------------------------------------------------------------------
# Wrappers that thread the shim's path globals through at call time
# ---------------------------------------------------------------------------

def find_node_file(slug: str) -> Path | None:
    return _load.find_node_file(slug, NODES_DIR)


def build_node_index() -> dict[str, Path]:
    return _load.build_node_index(NODES_DIR)


def load_alias_resolver() -> dict[str, str]:
    return _load.load_legacy_alias_resolver(ALIAS_RESOLVER_FILE)


def stream_inbound_refs(target_slug: str, limit: int = 20) -> tuple[list[dict], int]:
    return _load.stream_inbound_refs(target_slug, limit, path=CROSS_REFS_FILE)


def resolve_edge_target(
    target_title: str, alias_map: dict[str, str]
) -> tuple[str, str, str | None]:
    return _report.resolve_edge_target(target_title, alias_map, NODES_DIR)


def slow_alias_search(missing_slug: str) -> list[str]:
    return _report.slow_alias_search(missing_slug, NODES_DIR)


def slug_prefix_suggestions(missing_slug: str, max_results: int = 5) -> list[str]:
    return _traverse.slug_prefix_suggestions(missing_slug, NODES_DIR, max_results)


def _node_header(slug: str) -> str:
    return _traverse.node_header(slug, NODES_DIR)


def _leg_direction(pivot: str, other: str, leg_edges: list[dict]) -> str:
    # Old 3-arg signature preserved; `other` was unused in the old body too.
    return _traverse._leg_direction(pivot, leg_edges)


def _edges_to_neighbor_records(
    edges: list[dict], *, direction: str, pivot: str | None = None
) -> list[dict]:
    # Old signature carried an unused `pivot` kwarg; accepted and dropped.
    return _traverse._edges_to_neighbor_records(edges, direction=direction)


def build_report(
    slug: str,
    *,
    edges_only: bool = False,
    inbound_only: bool = False,
    inbound_limit: int = 20,
) -> dict:
    return _report.build_report(
        slug,
        edges_only=edges_only,
        inbound_only=inbound_only,
        inbound_limit=inbound_limit,
        nodes_dir=NODES_DIR,
    )


# ---------------------------------------------------------------------------
# cmd_* wrappers — compute via traverse.*, print via cli.print_* (both
# absorbed verbatim from this script's pre-shim implementation)
# ---------------------------------------------------------------------------

def cmd_neighbors(slug: str, edges: list[dict], *, json_output: bool = False) -> None:
    result = _traverse.neighbors(slug, edges, nodes_dir=NODES_DIR)
    _cli.print_neighbors(result, json_output=json_output)


def cmd_path(slug_a: str, slug_b: str, edges: list[dict], *, json_output: bool = False) -> None:
    result = _traverse.path(slug_a, slug_b, edges)
    _cli.print_path(result, json_output=json_output)


def cmd_health(edges: list[dict], nodes_dir: Path, *, json_output: bool = False) -> None:
    result = _traverse.health(edges, nodes_dir)
    _cli.print_health(result, json_output=json_output)


def cmd_event_participants(hub_slug: str, edges: list[dict], *, json_output: bool = False) -> None:
    result = _traverse.event_participants(hub_slug, edges, NODES_DIR)
    _cli.print_event_participants(result, json_output=json_output)


def cmd_causal_chain(
    slug: str,
    edges: list[dict],
    *,
    json_output: bool = False,
    edge_types: frozenset[str] = CAUSAL_EDGE_TYPES,
    expand_beats: bool = False,
) -> None:
    result = _traverse.causal_chain(
        slug, edges, edge_types=edge_types, expand_beats=expand_beats
    )
    _cli.print_causal_chain(result, json_output=json_output, expand_beats=expand_beats)


def cmd_container(name: str, *, json_output: bool = False) -> None:
    result = _traverse.container(name, NODES_DIR)
    _cli.print_container(result, json_output=json_output)


# ---------------------------------------------------------------------------
# CLI — old argparse surface kept VERBATIM (no --family-tree here; that is
# a weirwood_query.cli addition, reachable via `weirwood query`)
# ---------------------------------------------------------------------------

def main() -> None:
    print(
        "[graph-query.py] deprecated shim — the engine lives at graph/query/; "
        "prefer `weirwood query <args>`. Output unchanged.",
        file=sys.stderr,
    )
    parser = argparse.ArgumentParser(
        description=(
            "Inspect Weirwood Network graph nodes and edges.\n\n"
            "NODE INSPECTION (original):\n"
            "  graph-query.py <slug> [--edges-only] [--inbound-only] [--json]\n\n"
            "CANONICAL EDGE LAYER:\n"
            "  graph-query.py --neighbors <slug>\n"
            "  graph-query.py --path <slugA> <slugB>\n"
            "  graph-query.py --health\n"
            "  graph-query.py --event-participants <hub-slug>\n"
            "  graph-query.py --causal-chain <slug>\n"
            "  graph-query.py --edges <path>   (override edges.jsonl location)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Positional slug — optional so new modes work without it
    parser.add_argument(
        "slug",
        nargs="?",
        default=None,
        help="Node slug for node inspection (e.g. house-stark, eddard-stark)",
    )

    # --- original flags ---
    parser.add_argument(
        "--edges-only",
        action="store_true",
        help="(node inspection) Print only outbound edges, skip inbound references.",
    )
    parser.add_argument(
        "--inbound-only",
        action="store_true",
        help="(node inspection) Print only inbound references (top 50).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output machine-readable JSON instead of formatted text.",
    )

    # --- new edge-layer flags ---
    parser.add_argument(
        "--neighbors",
        metavar="SLUG",
        default=None,
        help="Show all edges touching SLUG, split into OUTGOING and INCOMING, "
             "grouped by edge_type.",
    )
    parser.add_argument(
        "--path",
        nargs=2,
        metavar=("SLUG_A", "SLUG_B"),
        default=None,
        help="Show direct edges between SLUG_A and SLUG_B, plus 2-hop common "
             "neighbors (bridges).",
    )
    parser.add_argument(
        "--health",
        action="store_true",
        help="Print graph-wide stats: node count, edge count, type distribution, "
             "orphan endpoints, and degree leaders.",
    )
    parser.add_argument(
        "--event-participants",
        metavar="HUB_SLUG",
        default=None,
        dest="event_participants",
        help=(
            "Union the participant role edges (AGENT_IN, COMMANDS_IN, VICTIM_IN, "
            "WIELDED_IN, ATTENDS, LOCATED_AT) across all SUB_BEAT_OF children of "
            "HUB_SLUG and display them as if attached to the hub. Handles reified "
            "event hubs where participants live on beat children, not the parent."
        ),
    )
    parser.add_argument(
        "--causal-chain",
        metavar="SLUG",
        default=None,
        dest="causal_chain",
        help=(
            "Walk CAUSES / TRIGGERS / MOTIVATES edges transitively, both "
            "directions, from SLUG. Returns the upstream causes and downstream "
            "effects — the consequence-chain of a narrative arc that no single "
            "edge holds (e.g. 'what set Tyrion's capture in motion, 3 steps back'). "
            "Excludes ENABLES preconditions by design (use --full-chain for those)."
        ),
    )
    parser.add_argument(
        "--full-chain", "--include-enables",
        metavar="SLUG",
        default=None,
        dest="full_chain",
        help=(
            "Like --causal-chain but ALSO follows ENABLES preconditions (rendered "
            "'(precondition)'), so a spine with ENABLES hinges reads end-to-end "
            "instead of as disconnected segments."
        ),
    )
    parser.add_argument(
        "--expand-beats",
        action="store_true",
        dest="expand_beats",
        help=(
            "Modifier for --causal-chain / --full-chain: also surface each chain "
            "node's SUB_BEAT_OF children and their role edges (AGENT_IN / VICTIM_IN "
            "/ COMMANDS_IN / WITNESS_IN / WIELDED_IN), so an event that reads sparse "
            "in the causal walk shows its real richness."
        ),
    )
    parser.add_argument(
        "--container",
        metavar="NAME",
        default=None,
        help=(
            "Bag-retrieval: list every node whose containers: frontmatter array "
            "contains NAME (unordered). NOT 'show me the arc' — for the ordered "
            "causal walk use --causal-chain / --full-chain."
        ),
    )
    parser.add_argument(
        "--edges",
        metavar="PATH",
        default=None,
        help=f"Override path to edges.jsonl (default: {DEFAULT_EDGES_FILE})",
    )

    args = parser.parse_args()

    # Validate: at most one mode active
    new_mode = (
        args.neighbors
        or args.path
        or args.health
        or args.event_participants
        or args.causal_chain
        or args.full_chain
        or args.container
    )
    old_mode = args.slug is not None

    if new_mode and old_mode:
        parser.error(
            "Cannot combine a positional slug with "
            "--neighbors / --path / --health / --event-participants / "
            "--causal-chain / --full-chain / --container. Use one mode at a time."
        )

    # --expand-beats is a modifier, only valid with a causal walk.
    if args.expand_beats and not (args.causal_chain or args.full_chain):
        parser.error(
            "--expand-beats must be combined with --causal-chain or --full-chain."
        )

    if not new_mode and not old_mode:
        parser.print_help()
        sys.exit(0)

    # ------------------------------------------------------------------
    # NEW EDGE-LAYER MODES
    # ------------------------------------------------------------------
    if new_mode:
        # --container reads node frontmatter, not the edge layer.
        if args.container:
            cmd_container(args.container, json_output=args.json_output)
            sys.exit(0)

        edges_path = Path(args.edges) if args.edges else DEFAULT_EDGES_FILE
        try:
            edges = load_edges(edges_path)
        except FileNotFoundError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            sys.exit(1)

        if args.neighbors:
            cmd_neighbors(args.neighbors, edges, json_output=args.json_output)

        elif args.path:
            cmd_path(args.path[0], args.path[1], edges, json_output=args.json_output)

        elif args.health:
            cmd_health(edges, NODES_DIR, json_output=args.json_output)

        elif args.event_participants:
            cmd_event_participants(
                args.event_participants, edges, json_output=args.json_output
            )

        elif args.causal_chain:
            cmd_causal_chain(
                args.causal_chain, edges, json_output=args.json_output,
                expand_beats=args.expand_beats,
            )

        elif args.full_chain:
            cmd_causal_chain(
                args.full_chain, edges, json_output=args.json_output,
                edge_types=FULL_CHAIN_EDGE_TYPES, expand_beats=args.expand_beats,
            )

        sys.exit(0)

    # ------------------------------------------------------------------
    # ORIGINAL NODE-INSPECTION MODE (unchanged behaviour)
    # ------------------------------------------------------------------
    if args.edges_only and args.inbound_only:
        parser.error("--edges-only and --inbound-only are mutually exclusive.")

    inbound_limit = 50 if args.inbound_only else 20

    report = build_report(
        args.slug,
        edges_only=args.edges_only,
        inbound_only=args.inbound_only,
        inbound_limit=inbound_limit,
    )

    if args.json_output:
        print_json(report)
    else:
        print_report(report, inbound_only=args.inbound_only, edges_only=args.edges_only)

    # Exit code: 1 if node not found
    if report["error"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
