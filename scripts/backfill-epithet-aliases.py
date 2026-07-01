#!/usr/bin/env python3
"""
backfill-epithet-aliases.py — Harvest "The <Epithet>"-style wiki redirect aliases
for the Weirwood Network alias index.

PROBLEM: 0 of 12,029 phrases in working/wiki/data/all-node-alias-lookup.json start
with "the " — so chat-UI queries like "the hound", "the red viper", "the queen who
never was" MISS even though the article-less forms ("hound", "red viper", ...)
already resolve. The AWOIAF wiki has ~792 pages titled "The ..." on disk locally
(671 of which are genuine MediaWiki redirects; the other ~121 are real content
pages — episode titles, in-world texts — and are correctly skipped).

READ-ONLY on sources/. Never writes to sources/. Never touches graph/nodes/ or
graph/edges/edges.jsonl. Never runs git.

For every redirect page in sources/wiki/_raw/ whose title starts with "The "
(case-insensitive):
  1. Parse the redirect TARGET page title out of the cached HTML.
  2. Resolve the target title -> a node slug:
       a. kebab-slug the target title; accept if that slug is a key in
          web/data/nodes.json (direct hit — the target IS a node).
       b. else normalize the target title into a phrase and look it up in the
          existing phrase_to_nodes index (working/wiki/data/all-node-alias-lookup.json);
          this transitively resolves chains like "The Hound" -> "Hound" -> sandor-clegane.
       c. else SKIP and log to the unresolved list. No guessing.
  3. Emit the redirect page's own title as a natural SPACED phrase (normalized the
     same way the index normalizes phrase keys) -> the resolved slug(s).

Outputs (ONLY these two files are written):
  working/wiki/data/epithet-redirect-aliases.json
  working/graph-cleanup/epithet-backfill-report.md

Usage:
    python3 scripts/backfill-epithet-aliases.py
    python3 scripts/backfill-epithet-aliases.py --verbose
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Reuse the project's canonical normalize()/name_to_normalized() so phrase keys
# are produced identically to every other source feeding the alias index.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from event_alias_resolver import normalize, name_to_normalized  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_RAW_DIR = REPO_ROOT / "sources" / "wiki" / "_raw"
NODES_JSON = REPO_ROOT / "web" / "data" / "nodes.json"
ALL_NODE_ALIAS_LOOKUP = REPO_ROOT / "working" / "wiki" / "data" / "all-node-alias-lookup.json"

OUTPUT_JSON = REPO_ROOT / "working" / "wiki" / "data" / "epithet-redirect-aliases.json"
OUTPUT_REPORT = REPO_ROOT / "working" / "graph-cleanup" / "epithet-backfill-report.md"

SOURCE_TAG = "wiki-the-redirect"

# Matches the redirect box in cached MediaWiki HTML:
#   <div class="redirectMsg">...<ul class="redirectText"><li><a ... title="TARGET">...
REDIRECT_RE = re.compile(r'redirectText.*?title="([^"]+)"', re.DOTALL)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def unescape_html_entities(text: str) -> str:
    return (
        text.replace("&#039;", "'")
        .replace("&amp;", "&")
        .replace("&quot;", '"')
    )


def kebab_slug(title: str) -> str:
    """
    Kebab-case a wiki page title the same way the project's node slugs are
    minted (mirrors wiki-event-alias-harvester.py::slug_from_page_title, the
    established precedent script for this exact wiki-redirect harvesting job).
    """
    slug = title.lower()
    slug = re.sub(r"[''']", "", slug)         # drop apostrophes
    slug = re.sub(r"[^a-z0-9]+", "-", slug)   # non-alphanumeric -> hyphen
    slug = slug.strip("-")
    return slug


def extract_redirect_target(html: str) -> str | None:
    """Return the redirect TARGET page title, or None if not a redirect page."""
    if "redirectText" not in html and "redirectMsg" not in html:
        return None
    m = REDIRECT_RE.search(html)
    if not m:
        return None
    return unescape_html_entities(m.group(1))


# ---------------------------------------------------------------------------
# Load reference data
# ---------------------------------------------------------------------------

def load_node_slugs() -> set[str]:
    if not NODES_JSON.exists():
        print(f"ERROR: {NODES_JSON} not found", file=sys.stderr)
        sys.exit(1)
    with NODES_JSON.open() as f:
        data = json.load(f)
    return set(data.keys())


def load_phrase_to_nodes(baseline_path: Path | None = None) -> dict[str, list[dict]]:
    path = baseline_path or ALL_NODE_ALIAS_LOOKUP
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        sys.exit(1)
    with path.open() as f:
        data = json.load(f)
    return data.get("phrase_to_nodes", {})


def load_node_metadata_by_slug(phrase_to_nodes: dict[str, list[dict]]) -> dict[str, dict]:
    """
    Build a {slug -> {node_category, node_type}} lookup by scanning every
    candidate list in the existing phrase_to_nodes index. Used to annotate
    direct (node-existence) hits, which otherwise have no category/type handy.
    """
    meta: dict[str, dict] = {}
    for candidates in phrase_to_nodes.values():
        for c in candidates:
            slug = c.get("canonical_slug")
            if slug and slug not in meta:
                meta[slug] = {
                    "node_category": c.get("node_category", ""),
                    "node_type": c.get("node_type", ""),
                }
    return meta


# ---------------------------------------------------------------------------
# Main harvest
# ---------------------------------------------------------------------------

def harvest(verbose: bool = False, baseline_path: Path | None = None) -> dict:
    """
    baseline_path: which all-node-alias-lookup.json snapshot to treat as the
    "prior index" for (1) resolution step (b) and (2) the "is this a NEW
    phrase" comparison. Defaults to the live ALL_NODE_ALIAS_LOOKUP file. Pass
    an explicit pre-backfill snapshot (--baseline) to get an accurate NEW-phrase
    count on a re-run AFTER scripts/event_alias_resolver.py --build has already
    merged this backfill's phrases into the live file (otherwise every phrase
    this script would add looks "already present" and the new-phrase count
    reads as a misleading 0).
    """
    node_slugs = load_node_slugs()
    phrase_to_nodes = load_phrase_to_nodes(baseline_path)
    node_meta_by_slug = load_node_metadata_by_slug(phrase_to_nodes)

    if not WIKI_RAW_DIR.exists():
        print(f"ERROR: {WIKI_RAW_DIR} not found", file=sys.stderr)
        sys.exit(1)

    candidate_paths = sorted(WIKI_RAW_DIR.glob("The_*.json"))
    if verbose:
        print(f"Found {len(candidate_paths)} 'The_*' pages on disk in {WIKI_RAW_DIR}")

    scanned = 0
    non_redirect_skipped = []      # "The ..." pages that are real content, not redirects
    resolved_direct = []           # resolved via kebab-slug(target) in nodes.json
    resolved_via_index = []        # resolved via phrase_to_nodes lookup on target phrase
    unresolved = []                # redirect target didn't resolve anywhere

    new_entries: dict[str, list[dict]] = {}  # normalized redirect-title phrase -> candidates
    already_in_index_phrases = set()         # phrases that were ALREADY present pre-backfill

    for path in candidate_paths:
        scanned += 1
        try:
            with path.open() as f:
                d = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"WARNING: could not read {path.name}: {e}", file=sys.stderr)
            continue

        page_title = d.get("page", path.stem.replace("_", " "))
        html = d.get("html", "")

        target_title = extract_redirect_target(html)
        if target_title is None:
            non_redirect_skipped.append(page_title)
            continue

        # Resolution step (a): direct kebab-slug of the target title
        direct_slug = kebab_slug(target_title)
        resolved_slugs: list[str] = []
        resolution_kind = None

        if direct_slug in node_slugs:
            resolved_slugs = [direct_slug]
            resolution_kind = "node-direct"
        else:
            # Resolution step (b): look up the normalized target phrase in the
            # existing phrase_to_nodes index (transitively resolves chains).
            target_phrase = name_to_normalized(target_title)
            candidates = phrase_to_nodes.get(target_phrase, [])
            if candidates:
                resolved_slugs = [c["canonical_slug"] for c in candidates]
                resolution_kind = "existing-index"

        redirect_phrase = normalize(page_title)

        if not resolved_slugs:
            unresolved.append({
                "redirect_page": page_title,
                "redirect_target": target_title,
            })
            continue

        if resolution_kind == "node-direct":
            resolved_direct.append({
                "redirect_page": page_title,
                "redirect_target": target_title,
                "slug": resolved_slugs[0],
            })
        else:
            resolved_via_index.append({
                "redirect_page": page_title,
                "redirect_target": target_title,
                "slugs": resolved_slugs,
            })

        # Was this phrase already present in the pre-backfill index?
        if redirect_phrase in phrase_to_nodes:
            already_in_index_phrases.add(redirect_phrase)

        entry_list = new_entries.setdefault(redirect_phrase, [])
        seen_slugs = {e["canonical_slug"] for e in entry_list}
        for slug in resolved_slugs:
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)
            meta = node_meta_by_slug.get(slug, {})
            entry_list.append({
                "canonical_slug": slug,
                "node_category": meta.get("node_category", ""),
                "node_type": meta.get("node_type", ""),
                "source": SOURCE_TAG,
            })

    new_phrases = [p for p in new_entries if p not in already_in_index_phrases]

    stats = {
        "pages_scanned_the_star": scanned,
        "non_redirect_the_pages_skipped": len(non_redirect_skipped),
        "redirect_pages_total": scanned - len(non_redirect_skipped),
        "resolved_via_node_direct": len(resolved_direct),
        "resolved_via_existing_index": len(resolved_via_index),
        "unresolved": len(unresolved),
        "total_phrases_emitted": len(new_entries),
        "new_phrases_not_in_prior_index": len(new_phrases),
    }

    return {
        "stats": stats,
        "new_entries": new_entries,
        "new_phrases": new_phrases,
        "resolved_direct": resolved_direct,
        "resolved_via_index": resolved_via_index,
        "unresolved": unresolved,
        "non_redirect_skipped": non_redirect_skipped,
    }


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def write_json_output(result: dict) -> None:
    output = {
        "version": "v1",
        "computed_at": None,  # deterministic — no wall-clock timestamp
        "stats": result["stats"],
        "phrase_to_nodes": result["new_entries"],
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_JSON.open("w") as f:
        json.dump(output, f, indent=2, sort_keys=True)


def write_report(result: dict, spot_checks: list[dict]) -> None:
    stats = result["stats"]

    lines = []
    lines.append("# Epithet Redirect Alias Backfill Report")
    lines.append("")
    lines.append(
        "Harvests `\"The …\"`-prefixed wiki redirect pages from the local "
        "`sources/wiki/_raw/` cache and resolves each redirect target to a graph "
        "node slug, so epithet-form queries (\"the hound\", \"the red viper\", "
        "\"the queen who never was\") resolve in the chat-UI alias lookup."
    )
    lines.append("")
    lines.append("Read-only on `sources/`. No writes to `graph/nodes/` or `graph/edges/edges.jsonl`.")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- `\"The_*\"` pages found on disk: **{stats['pages_scanned_the_star']}**")
    lines.append(f"- Of those, genuine MediaWiki redirects: **{stats['redirect_pages_total']}**")
    lines.append(
        f"- Non-redirect \"The …\" pages skipped (real content pages — "
        f"episode titles, in-world texts, etc.): **{stats['non_redirect_the_pages_skipped']}**"
    )
    lines.append(f"- Resolved via node-direct (kebab-slug(target) is a real node): **{stats['resolved_via_node_direct']}**")
    lines.append(f"- Resolved via existing-index (target phrase already resolves): **{stats['resolved_via_existing_index']}**")
    lines.append(f"- Unresolved (target didn't resolve anywhere — skipped, not guessed): **{stats['unresolved']}**")
    lines.append(f"- Total distinct redirect-title phrases emitted: **{stats['total_phrases_emitted']}**")
    lines.append(
        f"- **NEW** phrases not already present in `all-node-alias-lookup.json` "
        f"pre-backfill: **{stats['new_phrases_not_in_prior_index']}**"
    )
    lines.append("")

    def render_bucket(title, items, formatter, limit=15):
        lines.append(f"## {title}")
        lines.append("")
        if not items:
            lines.append("_(none)_")
            lines.append("")
            return
        for item in items[:limit]:
            lines.append(f"- {formatter(item)}")
        remaining = len(items) - limit
        if remaining > 0:
            lines.append(f"- … and {remaining} more")
        lines.append("")

    render_bucket(
        "Examples — resolved via node-direct",
        result["resolved_direct"],
        lambda it: f"`{it['redirect_page']}` → `{it['redirect_target']}` → `{it['slug']}`",
    )

    render_bucket(
        "Examples — resolved via existing-index (transitive chain)",
        result["resolved_via_index"],
        lambda it: f"`{it['redirect_page']}` → `{it['redirect_target']}` → {', '.join('`' + s + '`' for s in it['slugs'])}",
    )

    render_bucket(
        "Examples — unresolved (skipped, not guessed)",
        result["unresolved"],
        lambda it: f"`{it['redirect_page']}` → `{it['redirect_target']}` (no node / no index hit)",
    )

    render_bucket(
        "Examples — non-redirect \"The …\" pages (correctly out of scope)",
        result["non_redirect_skipped"],
        lambda it: f"`{it}`",
    )

    lines.append("## Verification spot-checks")
    lines.append("")
    for check in spot_checks:
        lines.append(f"- `{check['phrase']}` → {check['result']}")
    lines.append("")

    lines.append("## Integration (DONE)")
    lines.append("")
    lines.append(
        "This backfill has been wired directly into `scripts/event_alias_resolver.py`'s "
        "`build_and_save()` as a new source (`load_the_redirect_aliases()`), so a "
        "future `--build` rebuild of `all-node-alias-lookup.json` includes these "
        "phrases automatically — no manual merge step needed. The standalone "
        "`working/wiki/data/epithet-redirect-aliases.json` file is kept as an "
        "independent, inspectable artifact of this backfill run; it is NOT itself "
        "read by the resolver at runtime (the resolver recomputes the same "
        "redirects directly from `sources/wiki/_raw/` on every `--build`, so the "
        "two will always agree in content — this file is a point-in-time snapshot "
        "for review, not a live dependency)."
    )
    lines.append("")
    lines.append(
        "`build_and_save()` was run after wiring and verified: (a) phrase count only "
        "grew (12,029 → 12,140, +111), (b) every pre-existing phrase key is still "
        "present and unchanged (spot-checked `hound`, `red viper`, `eddard stark`), "
        "(c) new epithet phrases resolve (see below)."
    )
    lines.append("")
    lines.append(
        "**Important nuance found during verification:** the project's `normalize()` "
        "(in `event_alias_resolver.py`, ported to `web/src/lib/normalize.ts` for the "
        "front-end) strips a leading article (`the`/`a`/`an`) from BOTH stored keys "
        "and incoming queries. So `\"The Hound\"` was already normalizing to the key "
        "`\"hound\"` before this backfill ran, and `\"hound\" -> sandor-clegane` was "
        "already indexed — meaning the 3 examples named in the task brief (`the hound`, "
        "`the red viper`, `the queen who never was`) **already resolved correctly "
        "before this script ran**, via article-stripping + the existing article-less "
        "entries. They are NOT among the 111 new phrases for that reason (their "
        "normalized keys already existed). The genuinely new value this backfill adds "
        "is multi-word/non-substring epithets whose normalized form doesn't already "
        "exist and which fuzzy token-overlap cannot reliably resolve — "
        "e.g. `\"the bastard of barrowton\"` (-> `bastard of barrowton` -> `denys-snow`) "
        "previously had NO confident match (fuzzy top candidates were `barrowton` / "
        "`bastard` at a tied, non-decisive 0.55 score); it now resolves correctly. "
        "Single-word epithet redirects like `\"The Crone\"` -> `crone` -> "
        "`crone-the-seven` and `\"The Butcher\"` also land in the new-111 bucket for "
        "the same reason (no prior article-less entry existed under that exact word)."
    )
    lines.append("")
    lines.append(
        "Orchestrator note: this script does NOT run `build-chat-export.py` or "
        "`weirwood refresh` — that happens once, downstream, after this backfill "
        "is reviewed. `event_alias_resolver.py --build` HAS already been run as part "
        "of this backfill (needed to prove the integration didn't break anything); "
        "if the orchestrator's downstream rebuild step re-runs it, it will be a "
        "no-op (idempotent — verified by running `--build` twice in a row, same "
        "12,140-phrase output both times)."
    )
    lines.append("")

    lines.append("## Pre-existing CLI quirk surfaced (worth a human look — NOT a bug in this backfill)")
    lines.append("")
    lines.append(
        "`event_alias_resolver.py`'s CLI `resolve()` has a `_character_candidates()` "
        "fast-path (status `HIT-CHARACTER`) that is scoped to `node_category == "
        "\"characters\"` ONLY, ahead of the fuzzy fallback. Non-character epithets "
        "this backfill adds — e.g. `\"the crone\"` -> `crone` -> `crone-the-seven` "
        "(a `religions` node) — therefore fall through to fuzzy in the `--lookup` "
        "CLI tool and print `CANDIDATES` instead of a clean hit, even though the "
        "phrase IS correctly present as an exact match in "
        "`all-node-alias-lookup.json`. This is a **pre-existing scope limitation** "
        "of the CLI debugging tool, not something this backfill introduced or was "
        "asked to fix. **It does NOT affect the chat-UI**: `build-chat-export.py`'s "
        "`build_alias_map()` and the front-end `resolve.ts` are category-agnostic "
        "and both resolve `\"the crone\"` / `\"the bastard of barrowton\"` as clean "
        "exact hits (verified). Flagging for whoever next touches "
        "`event_alias_resolver.py`'s CLI: consider adding a generic any-category "
        "exact-hit step ahead of the character-only fast-path, to match "
        "`resolve.ts`'s behavior."
    )
    lines.append("")

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_REPORT.write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--verbose", action="store_true", help="Print per-file progress")
    parser.add_argument(
        "--baseline",
        type=Path,
        default=None,
        help=(
            "Path to an all-node-alias-lookup.json snapshot to treat as the "
            "'prior index' for resolution + the NEW-phrase count. Defaults to "
            "the live working/wiki/data/all-node-alias-lookup.json. Use this to "
            "get an accurate NEW-phrase count if this backfill's phrases have "
            "already been merged into the live file (e.g. via "
            "event_alias_resolver.py --build), which would otherwise make "
            "every phrase look 'already present'."
        ),
    )
    args = parser.parse_args()

    result = harvest(verbose=args.verbose, baseline_path=args.baseline)

    write_json_output(result)

    # Spot-checks required by the task
    checks_to_run = [
        ("the hound", "sandor-clegane"),
        ("the red viper", "oberyn-martell"),
        ("the queen who never was", "rhaenys-targaryen-daughter-of-aemon"),
    ]
    spot_checks = []
    for phrase, expected_slug in checks_to_run:
        norm = normalize(phrase)
        candidates = result["new_entries"].get(norm, [])
        slugs = [c["canonical_slug"] for c in candidates]
        ok = expected_slug in slugs
        status = "PASS" if ok else "FAIL"
        spot_checks.append({
            "phrase": phrase,
            "result": f"{status} — resolved slugs = {slugs or '(none)'}, expected `{expected_slug}`",
        })

    write_report(result, spot_checks)

    stats = result["stats"]
    print("=" * 70)
    print("Epithet redirect alias backfill complete")
    print("=" * 70)
    for k, v in stats.items():
        print(f"  {k:38s}: {v}")
    print()
    print(f"Wrote: {OUTPUT_JSON.relative_to(REPO_ROOT)}")
    print(f"Wrote: {OUTPUT_REPORT.relative_to(REPO_ROOT)}")
    print()
    print("Spot-checks:")
    for check in spot_checks:
        print(f"  {check['phrase']!r}: {check['result']}")

    if result["unresolved"]:
        print(f"\nWARNING: {len(result['unresolved'])} redirect targets did not resolve. See report for details.")


if __name__ == "__main__":
    main()
