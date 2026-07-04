#!/usr/bin/env bash
# weirwood-refresh.sh — Rebuild ALL derived-artifact builders in one command.
#
# This is the standard post-node-mutation step (design §11.6). After any graph
# mutation that ADDS or RENAMES nodes, the entity/character indexes and the
# event-alias resolver must be rebuilt so the new nodes are discoverable.
# Edge-only mutations do NOT need this (see design §1.5 / memory
# rebuild-derived-artifacts-after-node-mutation).
#
# Usage (via weirwood.zsh):
#   weirwood refresh            Rebuild all class-C/D derived artifacts
#   weirwood refresh --check    WARN if artifacts are stale vs graph/nodes/ (no rebuild)
#
# Builders run (in order):
#   1. build-entity-indexes.py --type <T> --all   for all 17 entity TYPE_CONFIGS
#   2. build-character-indexes.py --all            (characters are a separate builder)
#   3. graph/query/build/build_alias_table.py --build  (event alias → slug lookup;
#      the query-engine builder — replaces event_alias_resolver.py --build, same output)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

NODES_DIR="$REPO_ROOT/graph/nodes"
RESOLVER_ARTIFACT="$REPO_ROOT/working/wiki/data/event-alias-lookup.json"

# 17 entity types handled by build-entity-indexes.py (characters use the sibling builder).
ENTITY_TYPES=(locations artifacts houses factions titles events religions species \
              texts concepts materials foods theories customs languages medical prophecies)

# ---------------------------------------------------------------------------
# --check : staleness warning (design §13 S8) — does NOT rebuild.
# ---------------------------------------------------------------------------
if [[ "${1:-}" == "--check" ]]; then
    if [[ ! -f "$RESOLVER_ARTIFACT" ]]; then
        echo "STALE: resolver artifact missing ($RESOLVER_ARTIFACT). Run 'weirwood refresh'." >&2
        exit 1
    fi
    # Newest *.node.md mtime under graph/nodes/ vs the resolver artifact mtime.
    newest_node="$(find "$NODES_DIR" -name '*.node.md' -newer "$RESOLVER_ARTIFACT" -print -quit 2>/dev/null)"
    if [[ -n "$newest_node" ]]; then
        echo "STALE: at least one node is newer than the derived artifacts." >&2
        echo "       e.g. $newest_node" >&2
        echo "       Run 'weirwood refresh' to rebuild indexes + alias resolver." >&2
        exit 1
    fi
    echo "OK: derived artifacts are newer than every node — no refresh needed."
    exit 0
fi

# ---------------------------------------------------------------------------
# default : rebuild everything.
# ---------------------------------------------------------------------------
echo "weirwood refresh — rebuilding all derived artifacts"
echo ""

rc=0

echo "[1/3] Entity indexes (${#ENTITY_TYPES[@]} types via build-entity-indexes.py)"
for t in "${ENTITY_TYPES[@]}"; do
    if python3 scripts/build-entity-indexes.py --type "$t" --all >/dev/null 2>&1; then
        echo "      ok: $t"
    else
        echo "      FAILED: $t" >&2
        rc=1
    fi
done

echo "[2/3] Character indexes (build-character-indexes.py --all)"
if python3 scripts/build-character-indexes.py --all >/dev/null 2>&1; then
    echo "      ok: characters"
else
    echo "      FAILED: characters" >&2
    rc=1
fi

echo "[3/3] Event alias resolver (graph/query/build/build_alias_table.py --build)"
if PYTHONPATH="$REPO_ROOT/graph/query${PYTHONPATH:+:$PYTHONPATH}" \
    python3 graph/query/build/build_alias_table.py --build >/dev/null 2>&1; then
    echo "      ok: event-alias-lookup.json"
else
    echo "      FAILED: event alias resolver" >&2
    rc=1
fi

echo ""
if [[ "$rc" -eq 0 ]]; then
    echo "Done — all derived artifacts rebuilt."
else
    echo "Done WITH FAILURES — see messages above (exit $rc)." >&2
fi
exit "$rc"
