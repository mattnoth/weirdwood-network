#!/usr/bin/env python3
"""fab-dispute-inject.py — deterministic injector for RESOLVED F&B dispute-review rows.

The Fire & Blood reconciler (`scripts/fab-reconcile-candidates.py`) QUARANTINES contested
edges/prose/event rows into `working/fire-and-blood/apply/<unit>/dispute-review.jsonl` and
NEVER emits them to `candidates.json` / `merge-plan.json` (see that script's §7.2 dispute-
proximity quarantine). `scripts/fab-dispute-preclassify.py` re-reads every held row and
pre-classifies it into AUTO_CLEAR / AUTO_DISPUTED / ROMANCE_CLASS / NEEDS_READ, writing
`dispute-preclass.jsonl` (original row + preclass_bucket / preclass_tier /
preclass_in_universe_source / preclass_reason).

This script is the THIRD leg: it takes the deterministically-RESOLVED rows (AUTO_CLEAR /
AUTO_DISPUTED, plus anything a `--verdicts` file adjudicates) and writes them back into the
real mint/merge inputs — `candidates.json` (edges) and `merge-plan.json` (prose bullets) —
so a later `mint_enrichment.py` / `fab_merge_node.py` run actually lands them in the graph.
No LLM, no network. Pure deterministic Python (`feedback_python_before_agent`).

VOCABULARY (locked): **step** (lowercase) = an ordered piece of work. **Tier** = confidence
1-5 ONLY. Edge types come from the locked 170-type vocabulary (never invented here — every
injected edge's `type` is copied verbatim from the row the reconciler already vocab-checked
before quarantining it).

WHAT GETS INJECTED, BY KIND
  kind == "edge"
    Resolve `source`/`target` NAMES -> slugs via the unit's own `matched.jsonl` (the
    reconciler's name->slug UPDATE map), case/space-normalized
    (`weirwood_query.normalize.normalize`, the SAME normalizer the reconciler's Router
    uses). If a name is not in matched.jsonl, fall back to the reconciler's own resolver
    (`weirwood_query.resolve.resolve` — the exact function `fab-reconcile-candidates.py`
    imports and calls; this is "the reconciler's resolver" the task brief names). A name
    that misses BOTH routes to `dispute-inject-leftover.jsonl` — never a dangling edge.

    Builds an edge dict in the EXACT candidates.json shape (id/type/source/target/book/
    chapter/quote/tier/note[/in_universe_source][/disputed]):
      AUTO_CLEAR    -> tier-1, no disputed flag.
      AUTO_DISPUTED -> tier-2, disputed:true, in_universe_source (from
                       preclass_in_universe_source, or the verdict's own
                       in_universe_source when injected via --verdicts).
    KNOWN LIMITATION (not fixable here — read-only script): dispute-review.jsonl edge
    rows never carry the original `qualifier` field (the reconciler's §7.2 quarantine
    branch drops it before holding the row), so injected edges never carry one either.

    Edge ids use a distinct `DISP<n>` scheme (never `E<n>`/`EV<n>-...`, the reconciler's
    own schemes) so injected edges stay auditable at a glance; `<n>` continues past any
    `DISP<n>` ids already in the unit's candidates.json (idempotent re-run support) and is
    checked against every existing id before use.

  kind == "prose"
    The row already carries a resolved `slug` — validated against the live node index
    (`graph/nodes/**/*.node.md`) OR the unit's own matched.jsonl slug set before use; an
    unresolvable slug also routes to leftover.

    Builds a bullet:
      AUTO_CLEAR    -> "- <text> (<unit>:<line>)"
      AUTO_DISPUTED -> "- (Per <Source Label>) <text> (<unit>:<line>)"
    <Source Label> is a light cosmetic transform of the in_universe_source enum value
    ("gyldayn-synthesis" -> "Gyldayn Synthesis", "mushroom" -> "Mushroom") — the enum
    itself (`IN_UNIVERSE_SOURCE_ENUM` in fab-reconcile-candidates.py) is untouched.
    If merge-plan.json already has an entry for that slug, the bullet is APPENDED to its
    `fab_section_md` (skipped if byte-identical to an existing line); otherwise a new
    `{slug, fab_section_md, run_id}` entry is added, reusing the unit's run_id.

  kind == "event"
    NEVER minted, NEVER routed through --policy/--verdicts at all — every event-kind row
    (regardless of its preclass bucket, and regardless of a matching --verdicts entry)
    is written to `dispute-events-deferred.jsonl` (the row + its preclass verdict) for a
    dedicated later human/subagent step. Rationale (task brief, restated): held events
    are often redundant with PARENT_OF-style edges or already-created nodes, and
    auto-minting thin event nodes is out of scope for a purely mechanical script.

INTERFACE
  python3 scripts/fab-dispute-inject.py --unit <unit> [--apply-dir DIR] --policy auto
      [--verdicts FILE] [--dry-run] [--nodes-root DIR]

  --unit          One unit dir name, a comma-separated list, or a glob (e.g.
                   'fab-the-long-reign*'). Also accepts --units as an alias. Default:
                   every non-excluded unit dir under --apply-dir. The 4 units already
                   applied in the S200 smoke batch (EXCLUDED_UNITS, mirrors
                   fab-dispute-preclassify.py's own list) are always skipped, even if
                   named explicitly — their dispute-review data is a historical record
                   of a run that already went through adjudication + apply.
  --policy auto   (default, and the only implemented policy) — inject AUTO_CLEAR +
                   AUTO_DISPUTED rows (kind in {edge, prose}); ROMANCE_CLASS and
                   NEEDS_READ are SKIPPED (left untouched in dispute-preclass.jsonl,
                   awaiting adjudication) unless --verdicts resolves them.
  --verdicts FILE JSONL of hand/subagent adjudication verdicts:
                   {"unit": ..., "row_ref": "..." OR "kind"/"source"/"target"/"edge_type"
                    (or "entity"/"slug" for a prose row), "verdict": "clear"|"disputed"|
                    "drop", "in_universe_source": "..." (optional, disputed only)}
                   A verdict, when it matches a row, takes precedence over that row's
                   preclass_bucket (so it can also override an AUTO_CLEAR/AUTO_DISPUTED
                   row, not just adjudicate a NEEDS_READ/ROMANCE_CLASS one — useful if a
                   later human read overturns a mechanical bucket call). "drop" means
                   "reviewed, and it should NOT be injected" — counted and reported, but
                   never written anywhere (not a leftover — leftover means unresolvable,
                   not rejected).
                   Row-matching key (designed now, verdict files land later): each
                   dispute-preclass.jsonl row has a deterministic `row_ref` computed as
                   "<unit>:<kind>:<line>:<...kind-specific fields...>" — a verdict may
                   supply that exact `row_ref` string, OR the fallback tuple the task
                   brief names for edges (kind="edge", source, target, edge_type) — this
                   script also recognizes the analogous prose-shaped fallback tuple
                   (kind="prose", entity, slug), documented here as an extension since
                   the brief only spelled out the edge case. Event-kind verdicts are
                   never consulted (see kind=="event" above).
  --dry-run       Report what WOULD be injected (counts by kind/bucket, sample
                   edges/bullets, leftover/deferred/dropped counts) WITHOUT writing
                   candidates.json / merge-plan.json — or ANY file. Fully side-effect-free.
  --nodes-root    Override graph/nodes/ (test fixtures point this at a temp dir).

IDEMPOTENCY
  Before appending an edge: skip if an identical (type, source, target, normalized-quote)
  edge already exists in candidates.json — using the SAME `edge_dedup_key` /
  `normalize_quote_for_dedup` that `mint_enrichment.py` itself uses for its own
  skip-if-exists dedup (imported read-only, so "identical" means the same thing
  everywhere in the pipeline). Before appending a bullet: skip if a byte-identical bullet
  line already exists in that slug's fab_section_md (or was already added earlier in the
  SAME run). Injected edges carry `"via": "dispute-inject"` so a re-run's dedup pass (and
  any later audit) can identify them; `mint_enrichment.py` ignores unrecognized edge dict
  keys, so this is a no-op for it. A second run against already-injected output adds
  nothing and does not rewrite files it has no new content for.

Never modifies graph/, the reconciler, mint/merge, the pre-classifier, or the extraction
prompt. Reads (read-only, importlib, never calls main()) `scripts/mint_enrichment.py` for
its dedup-key helpers and `graph/query/weirwood_query/{resolve,normalize}.py` for name
resolution — the SAME modules the rest of the F&B pipeline already depends on.
"""
from __future__ import annotations

import argparse
import fnmatch
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_APPLY_DIR = REPO / "working" / "fire-and-blood" / "apply"
DEFAULT_NODES_ROOT = REPO / "graph" / "nodes"

# The 4 units already applied to the graph in the S200 smoke batch — mirrors
# fab-dispute-preclassify.py's own EXCLUDED_UNITS (kept as a small literal duplicate
# rather than an import chain; keep the two lists in sync if this set ever changes).
EXCLUDED_UNITS = frozenset({
    "fab-aegons-conquest-03",
    "fab-heirs-of-the-dragon-15-p01",
    "fab-heirs-of-the-dragon-15-p02",
    "fab-sons-of-the-dragon-05-p01",
})

VALID_VERDICTS = {"clear", "disputed", "drop"}
DEFAULT_DISPUTED_SOURCE = "gyldayn-synthesis"
INJECTABLE_BUCKETS = {"AUTO_CLEAR", "AUTO_DISPUTED"}


# ---------------------------------------------------------------------------
# Read-only imports of sibling scripts' locked helpers (importlib exec_module,
# never calls their main() — same pattern fab-dispute-preclassify.py uses for the
# reconciler). Keeps "identical edge" / "resolve a name" byte-identical to the rest
# of the F&B pipeline instead of a second, driftable copy.
# ---------------------------------------------------------------------------
def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_MINT = _load_module(REPO / "scripts" / "mint_enrichment.py", "fab_dispute_inject_mint_ro")
edge_dedup_key = _MINT.edge_dedup_key
normalize_quote_for_dedup = _MINT.normalize_quote_for_dedup

if str(REPO / "graph" / "query") not in sys.path:
    sys.path.insert(0, str(REPO / "graph" / "query"))
from weirwood_query.resolve import resolve as _weirwood_resolve  # noqa: E402
from weirwood_query.normalize import normalize  # noqa: E402


# ---------------------------------------------------------------------------
# JSONL helpers
# ---------------------------------------------------------------------------
def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            rows.append(json.loads(raw))
        except json.JSONDecodeError as e:
            print(f"WARNING: {path} line {lineno}: malformed JSON ({e}) — row skipped", file=sys.stderr)
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Name / slug resolution
# ---------------------------------------------------------------------------
def load_matched_map(unit_dir: Path) -> dict[str, str]:
    """{normalize(name): slug} from the unit's matched.jsonl."""
    m: dict[str, str] = {}
    for row in load_jsonl(unit_dir / "matched.jsonl"):
        name, slug = row.get("name"), row.get("slug")
        if name and slug:
            m[normalize(name)] = slug
    return m


_NODE_INDEX_CACHE: dict[str, set[str]] = {}


def node_slug_index(nodes_root: Path) -> set[str]:
    """Cached {slug} set from nodes_root/**/*.node.md (one glob per distinct root)."""
    key = str(nodes_root)
    if key not in _NODE_INDEX_CACHE:
        _NODE_INDEX_CACHE[key] = (
            {p.name[: -len(".node.md")] for p in nodes_root.glob("**/*.node.md")}
            if nodes_root.exists() else set()
        )
    return _NODE_INDEX_CACHE[key]


class NameResolver:
    """matched.jsonl direct lookup, falling back to the reconciler's own resolver
    (`weirwood_query.resolve.resolve`). The shared alias-table lookup/all_node_index/
    collisions are lazy-loaded at most ONCE per resolver instance (resolve() itself does
    no caching — loading per-name would be needlessly slow for a 35-unit batch run)."""

    def __init__(self, matched_map: dict[str, str]):
        self.matched_map = matched_map
        self._lookup = None
        self._all_node_index = None
        self._collisions = None
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        from weirwood_query.load import load_alias_collisions, load_alias_lookup, load_all_node_index
        self._lookup = load_alias_lookup()
        self._all_node_index = load_all_node_index()
        self._collisions = load_alias_collisions()
        self._loaded = True

    def resolve(self, name: str) -> tuple[str | None, str]:
        """Returns (slug_or_None, route_reason)."""
        if not name:
            return None, "empty-name"
        key = normalize(name)
        slug = self.matched_map.get(key)
        if slug:
            return slug, "matched.jsonl"
        self._ensure_loaded()
        slug, status, _candidates = _weirwood_resolve(
            name, lookup=self._lookup, all_node_index=self._all_node_index,
            collisions=self._collisions)
        if status in ("hit", "hit-character") and slug:
            return slug, f"resolver-fallback:{status}"
        return None, "unresolved"


# ---------------------------------------------------------------------------
# --verdicts loading / matching
# ---------------------------------------------------------------------------
def compute_row_ref(unit: str, row: dict) -> str:
    """Deterministic per-row key a verdict file can target explicitly. Designed now
    even though verdict files land later — see module docstring INTERFACE/--verdicts."""
    kind = row.get("kind")
    line = row.get("line")
    if kind == "edge":
        return f"{unit}:edge:{line}:{row.get('edge_type')}:{row.get('source')}:{row.get('target')}"
    if kind == "prose":
        return f"{unit}:prose:{line}:{row.get('slug')}"
    if kind == "event":
        return f"{unit}:event:{line}:{row.get('name')}"
    return f"{unit}:{kind}:{line}"


def load_verdicts(path: Path | None) -> list[dict]:
    if not path:
        return []
    if not path.exists():
        print(f"WARNING: --verdicts file not found: {path}", file=sys.stderr)
        return []
    return load_jsonl(path)


def index_verdicts(rows: list[dict]) -> dict[tuple, dict]:
    """Build a lookup keyed by ("row_ref", unit, row_ref) and/or the kind-shaped
    fallback tuple (edge: kind/source/target/edge_type; prose (extension): kind/entity/
    slug). A verdict with an unrecognized `verdict` value or an unsupported kind (no
    row_ref given) is warned and ignored — never silently misapplied."""
    idx: dict[tuple, dict] = {}
    for v in rows:
        verdict = v.get("verdict")
        if verdict not in VALID_VERDICTS:
            print(f"WARNING: verdict row has unrecognized verdict {verdict!r} (want one of "
                  f"{sorted(VALID_VERDICTS)}) — ignored: {v}", file=sys.stderr)
            continue
        unit = v.get("unit")
        row_ref = v.get("row_ref")
        if row_ref:
            idx[("row_ref", unit, row_ref)] = v
            continue
        kind = v.get("kind", "edge")
        if kind == "edge":
            key = ("tuple", unit, "edge", v.get("source"), v.get("target"), v.get("edge_type"))
        elif kind == "prose":
            key = ("tuple", unit, "prose", v.get("entity"), v.get("slug"))
        else:
            print(f"WARNING: verdict row has no row_ref and an unsupported kind {kind!r} for "
                  f"tuple-fallback matching (edge/prose only) — ignored: {v}", file=sys.stderr)
            continue
        idx[key] = v
    return idx


def find_verdict(unit: str, row: dict, idx: dict[tuple, dict]) -> dict | None:
    v = idx.get(("row_ref", unit, compute_row_ref(unit, row)))
    if v:
        return v
    kind = row.get("kind")
    if kind == "edge":
        return idx.get(("tuple", unit, "edge", row.get("source"), row.get("target"), row.get("edge_type")))
    if kind == "prose":
        return idx.get(("tuple", unit, "prose", row.get("entity"), row.get("slug")))
    return None


def determine_treatment(row: dict, verdict: dict | None) -> dict:
    """{'action': 'inject'|'drop'|'skip', 'tier', 'disputed', 'in_universe_source', 'basis'}.
    A matching verdict takes precedence over the row's own preclass_bucket (see module
    docstring --verdicts). No verdict + bucket not in INJECTABLE_BUCKETS -> 'skip' (left
    untouched, awaiting adjudication — NOT a leftover/drop)."""
    if verdict is not None:
        v = verdict["verdict"]
        if v == "drop":
            return {"action": "drop", "basis": "verdict"}
        if v == "clear":
            return {"action": "inject", "tier": "tier-1", "disputed": False,
                     "in_universe_source": None, "basis": "verdict"}
        # v == "disputed"
        ius = verdict.get("in_universe_source") or row.get("preclass_in_universe_source") or DEFAULT_DISPUTED_SOURCE
        return {"action": "inject", "tier": "tier-2", "disputed": True,
                 "in_universe_source": ius, "basis": "verdict"}

    bucket = row.get("preclass_bucket")
    if bucket == "AUTO_CLEAR":
        return {"action": "inject", "tier": "tier-1", "disputed": False,
                 "in_universe_source": None, "basis": "auto"}
    if bucket == "AUTO_DISPUTED":
        ius = row.get("preclass_in_universe_source") or DEFAULT_DISPUTED_SOURCE
        return {"action": "inject", "tier": "tier-2", "disputed": True,
                 "in_universe_source": ius, "basis": "auto"}
    return {"action": "skip", "basis": "awaiting-adjudication"}


# ---------------------------------------------------------------------------
# Edge / bullet construction
# ---------------------------------------------------------------------------
def build_injected_edge(row: dict, treatment: dict, source_slug: str, target_slug: str,
                        eid: str, unit: str) -> dict:
    edge = {
        "id": eid,
        "type": row["edge_type"],
        "source": source_slug,
        "target": target_slug,
        "book": "fab",
        "chapter": unit,
        "quote": row.get("quote", ""),
        "tier": treatment["tier"],
        "note": f"Fire & Blood: {row.get('source')} {row['edge_type']} {row.get('target')}",
        "via": "dispute-inject",
    }
    if treatment["disputed"]:
        edge["disputed"] = True
        edge["in_universe_source"] = treatment["in_universe_source"]
    return edge


def format_source_label(ius: str | None) -> str:
    if not ius:
        return "an unnamed source"
    return ius.replace("-", " ").title()


def build_bullet(row: dict, treatment: dict, unit: str) -> str:
    text = row.get("text", "")
    line = row.get("line")
    if treatment["disputed"]:
        label = format_source_label(treatment["in_universe_source"])
        return f"- (Per {label}) {text} ({unit}:{line})"
    return f"- {text} ({unit}:{line})"


def assert_disputed_invariant(edges: list[dict]) -> None:
    """Pre-emit mechanical backstop (mirrors fab-reconcile-candidates.py's own P3
    assertion): every injected disputed:true edge must have tier-2 AND a non-empty
    in_universe_source. Fails loudly rather than silently writing an unsourced claim."""
    bad = []
    for e in edges:
        if not e.get("disputed"):
            continue
        m = re.match(r"^tier-(\d+)$", str(e.get("tier", "")))
        tier_num = int(m.group(1)) if m else None
        if tier_num is None or tier_num > 2 or not e.get("in_universe_source"):
            bad.append(e)
    if bad:
        detail = "\n".join(f"  {e.get('id')}: {e.get('source')} {e.get('type')} {e.get('target')} "
                            f"(tier={e.get('tier')!r}, in_universe_source={e.get('in_universe_source')!r})"
                            for e in bad)
        sys.exit("ABORT: dispute-inject disputed-invariant violation — every disputed:true "
                 f"edge must have tier-2 AND a non-empty in_universe_source:\n{detail}")


def next_disp_id(existing_ids: set[str], counter: list[int]) -> str:
    while True:
        counter[0] += 1
        cand = f"DISP{counter[0]}"
        if cand not in existing_ids:
            existing_ids.add(cand)
            return cand


# ---------------------------------------------------------------------------
# Per-unit processing — pure-ish (only I/O is the reads + the final conditional writes),
# easily testable by pointing apply_dir/nodes_root at a fixture tree.
# ---------------------------------------------------------------------------
def process_unit(unit: str, apply_dir: Path, nodes_root: Path, verdict_index: dict[tuple, dict],
                  dry_run: bool) -> dict:
    unit_dir = apply_dir / unit
    preclass_path = unit_dir / "dispute-preclass.jsonl"
    if not preclass_path.exists():
        return {"unit": unit, "skipped": True,
                "reason": "no dispute-preclass.jsonl (run fab-dispute-preclassify.py first)"}

    rows = load_jsonl(preclass_path)
    matched_map = load_matched_map(unit_dir)
    resolver = NameResolver(matched_map)
    nidx = node_slug_index(nodes_root)

    candidates_path = unit_dir / "candidates.json"
    merge_plan_path = unit_dir / "merge-plan.json"
    candidates = json.loads(candidates_path.read_text(encoding="utf-8")) if candidates_path.exists() else None
    merge_plan = json.loads(merge_plan_path.read_text(encoding="utf-8")) if merge_plan_path.exists() else []
    if candidates is None:
        print(f"WARNING: {unit}: no candidates.json found — edge-kind rows will route to leftover",
              file=sys.stderr)

    run_id = None
    if candidates and candidates.get("_meta", {}).get("run_id"):
        run_id = candidates["_meta"]["run_id"]
    elif merge_plan:
        run_id = merge_plan[0].get("run_id")
    if not run_id:
        run_id = f"{unit}-dispute-inject-{date.today().isoformat()}"

    existing_edges = candidates.get("edges", []) if candidates else []
    existing_ids = {e.get("id") for e in existing_edges if e.get("id")}
    existing_edge_keys = {
        edge_dedup_key(e.get("type"), e.get("source"), e.get("target"), e.get("quote", ""))
        for e in existing_edges if e.get("type") and e.get("source") and e.get("target")
    }
    disp_counter = [0]
    for eid in existing_ids:
        m = re.match(r"^DISP(\d+)$", eid or "")
        if m:
            disp_counter[0] = max(disp_counter[0], int(m.group(1)))

    merge_plan_index = {e["slug"]: e for e in merge_plan if e.get("slug")}

    stats: Counter = Counter()
    new_edges: list[dict] = []
    new_bullets_by_slug: dict[str, list[str]] = defaultdict(list)
    leftover_rows: list[dict] = []
    deferred_rows: list[dict] = []
    dropped_rows: list[dict] = []
    skipped_rows: list[dict] = []

    for row in rows:
        kind = row.get("kind")
        stats["rows_total"] += 1

        if kind == "event":
            deferred_rows.append(row)
            stats["events_deferred"] += 1
            continue

        verdict = find_verdict(unit, row, verdict_index)
        treatment = determine_treatment(row, verdict)
        action = treatment["action"]

        if action == "skip":
            skipped_rows.append(row)
            stats["skipped_awaiting_adjudication"] += 1
            continue
        if action == "drop":
            dropped_rows.append(row)
            stats["dropped_by_verdict"] += 1
            continue

        if kind == "edge":
            if candidates is None:
                leftover_rows.append({**row, "leftover_reason": "no candidates.json for unit"})
                stats["leftover_edges"] += 1
                continue
            src_slug, _sr = resolver.resolve(row.get("source", ""))
            tgt_slug, _tr = resolver.resolve(row.get("target", ""))
            if not src_slug or not tgt_slug:
                unresolved = [n for n, s in ((row.get("source"), src_slug), (row.get("target"), tgt_slug)) if not s]
                leftover_rows.append({**row, "leftover_reason": "unresolvable name(s)",
                                       "unresolved_names": unresolved})
                stats["leftover_edges"] += 1
                continue
            key = edge_dedup_key(row["edge_type"], src_slug, tgt_slug, row.get("quote", ""))
            if key in existing_edge_keys:
                stats["edges_already_present"] += 1
                continue
            eid = next_disp_id(existing_ids, disp_counter)
            edge = build_injected_edge(row, treatment, src_slug, tgt_slug, eid, unit)
            new_edges.append(edge)
            existing_edge_keys.add(key)
            stats["edges_injected"] += 1
            stats[f"edges_injected_{treatment['basis']}"] += 1

        elif kind == "prose":
            slug = row.get("slug")
            if not slug or not (slug in nidx or slug in matched_map.values()):
                leftover_rows.append({**row, "leftover_reason": "unresolvable/unknown slug"})
                stats["leftover_prose"] += 1
                continue
            bullet = build_bullet(row, treatment, unit)
            entry = merge_plan_index.get(slug)
            existing_lines = set((entry.get("fab_section_md", "") if entry else "").splitlines())
            if bullet in existing_lines or bullet in new_bullets_by_slug[slug]:
                stats["bullets_already_present"] += 1
                continue
            new_bullets_by_slug[slug].append(bullet)
            stats["bullets_injected"] += 1
            stats[f"bullets_injected_{treatment['basis']}"] += 1

        else:
            print(f"WARNING: {unit}: unrecognized row kind {kind!r} — treated as leftover", file=sys.stderr)
            leftover_rows.append({**row, "leftover_reason": f"unrecognized kind {kind!r}"})
            stats["leftover_unknown_kind"] += 1

    assert_disputed_invariant(new_edges)

    for slug, bullets in new_bullets_by_slug.items():
        entry = merge_plan_index.get(slug)
        if entry is None:
            entry = {"slug": slug, "fab_section_md": "", "run_id": run_id}
            merge_plan.append(entry)
            merge_plan_index[slug] = entry
        existing_text = entry.get("fab_section_md", "")
        addition = "\n".join(bullets)
        entry["fab_section_md"] = f"{existing_text}\n{addition}".strip("\n") if existing_text else addition

    report = {
        "unit": unit,
        "stats": dict(stats),
        "sample_edges": new_edges[:3],
        "sample_bullets": {k: v[:2] for k, v in list(new_bullets_by_slug.items())[:3]},
        "leftover_count": len(leftover_rows),
        "deferred_count": len(deferred_rows),
        "dropped_count": len(dropped_rows),
        "skipped_awaiting_count": len(skipped_rows),
    }

    if dry_run:
        return report

    if new_edges and candidates is not None:
        candidates["edges"] = existing_edges + new_edges
        candidates_path.write_text(json.dumps(candidates, indent=2, ensure_ascii=False) + "\n",
                                    encoding="utf-8")
    if new_bullets_by_slug:
        merge_plan_path.write_text(json.dumps(merge_plan, indent=2, ensure_ascii=False) + "\n",
                                    encoding="utf-8")
    write_jsonl(unit_dir / "dispute-events-deferred.jsonl", deferred_rows)
    write_jsonl(unit_dir / "dispute-inject-leftover.jsonl", leftover_rows)

    return report


# ---------------------------------------------------------------------------
# CLI / batch orchestration
# ---------------------------------------------------------------------------
def iter_target_units(apply_dir: Path, unit_arg: str | None) -> list[str]:
    all_names = sorted(p.name for p in apply_dir.iterdir() if p.is_dir())

    if unit_arg and any(ch in unit_arg for ch in "*?["):
        selected = [n for n in all_names if fnmatch.fnmatch(n, unit_arg)]
        if not selected:
            print(f"WARNING: --unit glob {unit_arg!r} matched no unit dirs under {apply_dir}",
                  file=sys.stderr)
    elif unit_arg:
        wanted = [u.strip() for u in unit_arg.split(",") if u.strip()]
        selected = []
        for w in wanted:
            if w not in all_names:
                print(f"WARNING: --unit requested {w!r} but no such unit dir exists under {apply_dir}",
                      file=sys.stderr)
                continue
            selected.append(w)
    else:
        selected = all_names

    kept = []
    for name in selected:
        if name in EXCLUDED_UNITS:
            print(f"NOTE: {name} is an already-applied smoke unit — permanently excluded", file=sys.stderr)
            continue
        kept.append(name)
    return kept


REPORT_COLUMNS = ["edges_injected", "bullets_injected", "deferred_count", "leftover_count",
                   "dropped_count", "skipped_awaiting_count"]


def print_summary(reports: list[dict], grand: Counter, args) -> None:
    mode = "DRY-RUN (nothing written)" if args.dry_run else "APPLY"
    print(f"\nFire & Blood dispute-inject summary — {mode}, policy={args.policy}")
    print("=" * 100)
    header = (f"{'unit':<46}{'edges':>8}{'bullets':>9}{'ev_def':>8}"
              f"{'leftover':>10}{'dropped':>9}{'awaiting':>10}")
    print(header)
    print("-" * len(header))
    live_reports = [r for r in reports if not r.get("skipped")]
    for r in live_reports:
        s = r["stats"]
        print(f"{r['unit']:<46}{s.get('edges_injected', 0):>8}{s.get('bullets_injected', 0):>9}"
              f"{r['deferred_count']:>8}{r['leftover_count']:>10}{r['dropped_count']:>9}"
              f"{r['skipped_awaiting_count']:>10}")
    print("-" * len(header))
    print(f"{'TOTAL':<46}{grand.get('edges_injected', 0):>8}{grand.get('bullets_injected', 0):>9}"
          f"{grand.get('events_deferred', 0):>8}{grand.get('leftover_edges', 0) + grand.get('leftover_prose', 0) + grand.get('leftover_unknown_kind', 0):>10}"
          f"{grand.get('dropped_by_verdict', 0):>9}{grand.get('skipped_awaiting_adjudication', 0):>10}")
    print()
    skipped_units = [r["unit"] for r in reports if r.get("skipped")]
    if skipped_units:
        print(f"({len(skipped_units)} unit(s) skipped — no dispute-preclass.jsonl): {', '.join(skipped_units)}")
    print(f"rows_total processed: {grand.get('rows_total', 0)}")
    print(f"edges: {grand.get('edges_injected', 0)} injected "
          f"({grand.get('edges_injected_auto', 0)} auto / {grand.get('edges_injected_verdict', 0)} verdict), "
          f"{grand.get('edges_already_present', 0)} already-present (idempotency skip), "
          f"{grand.get('leftover_edges', 0)} leftover (unresolvable)")
    print(f"prose bullets: {grand.get('bullets_injected', 0)} injected "
          f"({grand.get('bullets_injected_auto', 0)} auto / {grand.get('bullets_injected_verdict', 0)} verdict), "
          f"{grand.get('bullets_already_present', 0)} already-present (idempotency skip), "
          f"{grand.get('leftover_prose', 0)} leftover (unresolvable slug)")
    print(f"events: {grand.get('events_deferred', 0)} deferred to dispute-events-deferred.jsonl (never minted here)")
    print(f"dropped by verdict: {grand.get('dropped_by_verdict', 0)}")
    print(f"skipped, awaiting adjudication (NEEDS_READ/ROMANCE_CLASS, no verdict): "
          f"{grand.get('skipped_awaiting_adjudication', 0)}")

    sample_edges = [e for r in live_reports for e in r["sample_edges"]][:8]
    if sample_edges:
        print("\n--- sample injected edges ---")
        for e in sample_edges:
            print(f"  {e['id']}  {e['source']} {e['type']} {e['target']}  tier={e['tier']}"
                  f"{' disputed' if e.get('disputed') else ''}"
                  f"{' src=' + e['in_universe_source'] if e.get('in_universe_source') else ''}")
            print(f"    quote: {e['quote'][:100]!r}")

    sample_bullets = []
    for r in live_reports:
        for slug, bullets in r["sample_bullets"].items():
            for b in bullets:
                sample_bullets.append((r["unit"], slug, b))
    if sample_bullets[:8]:
        print("\n--- sample injected prose bullets ---")
        for unit, slug, b in sample_bullets[:8]:
            print(f"  {unit} :: {slug}\n    {b}")

    if args.dry_run:
        print("\nDRY-RUN — no files were written (candidates.json / merge-plan.json / "
              "dispute-events-deferred.jsonl / dispute-inject-leftover.jsonl all untouched).")
    else:
        print("\nWrote (per unit, only where non-empty): candidates.json (edges appended), "
              "merge-plan.json (bullets appended/added), dispute-events-deferred.jsonl, "
              "dispute-inject-leftover.jsonl")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--unit", "--units", dest="unit", default=None,
                    help="unit dir name, comma-separated list, or glob (e.g. 'fab-the-long-reign*'). "
                         "Default: every non-excluded unit dir under --apply-dir.")
    ap.add_argument("--apply-dir", type=Path, default=DEFAULT_APPLY_DIR,
                    help=f"default: {DEFAULT_APPLY_DIR.relative_to(REPO)}")
    ap.add_argument("--nodes-root", type=Path, default=DEFAULT_NODES_ROOT,
                    help=f"default: {DEFAULT_NODES_ROOT.relative_to(REPO)}")
    ap.add_argument("--policy", choices=["auto"], default="auto",
                    help="auto (default, only implemented policy): inject AUTO_CLEAR + AUTO_DISPUTED "
                         "rows; ROMANCE_CLASS/NEEDS_READ skipped unless --verdicts resolves them.")
    ap.add_argument("--verdicts", type=Path, default=None,
                    help="JSONL of hand/subagent adjudication verdicts (see module docstring)")
    ap.add_argument("--dry-run", action="store_true",
                    help="report only — never writes candidates.json/merge-plan.json or any other file")
    args = ap.parse_args()

    if not args.apply_dir.exists():
        sys.exit(f"ABORT: --apply-dir not found: {args.apply_dir}")

    units = iter_target_units(args.apply_dir, args.unit)
    if not units:
        sys.exit("ABORT: no unit dirs selected (check --unit / --apply-dir)")

    verdict_rows = load_verdicts(args.verdicts)
    verdict_index = index_verdicts(verdict_rows)
    if args.verdicts and verdict_rows:
        print(f"Loaded {len(verdict_rows)} verdict row(s) from {args.verdicts}")

    reports = []
    grand: Counter = Counter()
    for unit in units:
        report = process_unit(unit, args.apply_dir, args.nodes_root, verdict_index, args.dry_run)
        reports.append(report)
        if report.get("skipped"):
            print(f"WARNING: {unit}: {report['reason']} — skipped", file=sys.stderr)
            continue
        grand.update(report["stats"])

    print_summary(reports, grand, args)

    processed = len([r for r in reports if not r.get("skipped")])
    print(f"\nDone. {processed}/{len(units)} unit(s) processed"
          f"{' (dry-run)' if args.dry_run else ''}.")


if __name__ == "__main__":
    main()
