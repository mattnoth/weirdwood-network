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
#   4. graph/query/build/build_search_index.py     (quote+identity BM25 inverted index,
#      query-layer step 5a — writes working/wiki/data/search-index.json AND
#      web/data/search-index.json; the chat bundle itself (build_chat_bundle.py, the
#      nodes/edges/alias-map/manifest quartet) is NOT rebuilt here — that stays a
#      manual pre-deploy step per DEPLOY.md, same as before this builder existed)
#   5. graph/query/build/build_theme_index.py      (theme->members routing table,
#      query-layer step 8a — writes working/wiki/data/theme-index.json AND
#      web/data/theme-index.json)
#
# --check ALSO warns (does not rebuild) when graph/index/ (the mention-index
# rollups `mentions` reads) is stale vs graph/nodes/ — query-layer step 8b/G13.
# This is a SEPARATE staleness class from the resolver/search-index check above
# (graph/index/ is built by scripts/build-mention-index.py + build-entity-
# indexes.py, not by anything weirwood-refresh rebuilds — it is behind the
# no-graph-mutation gate, so this is warn-only, same as the rest of --check).

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

NODES_DIR="$REPO_ROOT/graph/nodes"
RESOLVER_ARTIFACT="$REPO_ROOT/working/wiki/data/event-alias-lookup.json"
MENTION_INDEX_DIR="$REPO_ROOT/graph/index/chapters"

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

    # Mention-index staleness (query-layer step 8b/G13) — warn-only, separate
    # from the exit-1 checks above: graph/index/ is mutation-gated, so this
    # check never rebuilds, it only surfaces the gap (see
    # working/query-layer/mention-index-repair-report.md for the measured
    # size of the gap and the reviewed apply command).
    mention_rc=0
    if [[ ! -d "$MENTION_INDEX_DIR" ]]; then
        echo "STALE (mention-index): $MENTION_INDEX_DIR missing entirely." >&2
        mention_rc=1
    else
        newest_node_vs_mentions="$(find "$NODES_DIR" -name '*.node.md' -newer "$MENTION_INDEX_DIR/_summary.json" -print -quit 2>/dev/null)"
        if [[ -n "$newest_node_vs_mentions" ]]; then
            echo "STALE (mention-index): at least one node is newer than graph/index/chapters/_summary.json." >&2
            echo "                       e.g. $newest_node_vs_mentions" >&2
            echo "                       graph/index/ is mutation-gated (Matt's go required to rebuild)." >&2
            echo "                       See working/query-layer/mention-index-repair-report.md." >&2
            mention_rc=1
        else
            echo "OK: mention-index (graph/index/chapters/) is newer than every node."
        fi
    fi
    exit "$mention_rc"
fi

# ---------------------------------------------------------------------------
# default : rebuild everything.
# ---------------------------------------------------------------------------
echo "weirwood refresh — rebuilding all derived artifacts"
echo ""

rc=0

echo "[1/5] Entity indexes (${#ENTITY_TYPES[@]} types via build-entity-indexes.py)"
for t in "${ENTITY_TYPES[@]}"; do
    if python3 scripts/build-entity-indexes.py --type "$t" --all >/dev/null 2>&1; then
        echo "      ok: $t"
    else
        echo "      FAILED: $t" >&2
        rc=1
    fi
done

echo "[2/5] Character indexes (build-character-indexes.py --all)"
if python3 scripts/build-character-indexes.py --all >/dev/null 2>&1; then
    echo "      ok: characters"
else
    echo "      FAILED: characters" >&2
    rc=1
fi

echo "[3/5] Event alias resolver (graph/query/build/build_alias_table.py --build)"
if PYTHONPATH="$REPO_ROOT/graph/query${PYTHONPATH:+:$PYTHONPATH}" \
    python3 graph/query/build/build_alias_table.py --build >/dev/null 2>&1; then
    echo "      ok: event-alias-lookup.json"
else
    echo "      FAILED: event alias resolver" >&2
    rc=1
fi

echo "[4/5] Search index (graph/query/build/build_search_index.py)"
if PYTHONPATH="$REPO_ROOT/graph/query${PYTHONPATH:+:$PYTHONPATH}" \
    python3 graph/query/build/build_search_index.py >/dev/null 2>&1; then
    echo "      ok: search-index.json (working/wiki/data/ + web/data/)"
else
    echo "      FAILED: search index" >&2
    rc=1
fi

echo "[5/5] Theme index (graph/query/build/build_theme_index.py)"
if PYTHONPATH="$REPO_ROOT/graph/query${PYTHONPATH:+:$PYTHONPATH}" \
    python3 graph/query/build/build_theme_index.py >/dev/null 2>&1; then
    echo "      ok: theme-index.json (working/wiki/data/ + web/data/)"
else
    echo "      FAILED: theme index" >&2
    rc=1
fi

echo ""
if [[ "$rc" -eq 0 ]]; then
    echo "Done — all derived artifacts rebuilt."
else
    echo "Done WITH FAILURES — see messages above (exit $rc)." >&2
fi
exit "$rc"
