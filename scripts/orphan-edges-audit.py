#!/usr/bin/env python3
"""orphan-edges-audit.py — Full-corpus orphan-edge auditor for the Weirwood Network.

Read-only on the graph. Walks every node's `## Edges` section, resolves each
edge target slug via the slug index and the alias-resolver, and classifies
unresolved edges into:
  - Category 1: target genuinely missing (no node, no alias)
  - Category 2: alias-mismatch (resolves via alias-resolver — graph layer should consult it)
  - Stale-data legacy: religion-bleed leftovers (WORSHIPS: religions / Mixed / Old gods / etc.)
  - Edge-format issues: BORN_AT/DIED_AT/BURIED_AT with date strings as targets

Writes the report to working/audits/orphan-edges-<UTC-date>.md and a full TSV
of Cat 1 misses to working/audits/orphan-edges-<UTC-date>-cat1-full.tsv.

Usage:
    python3 scripts/orphan-edges-audit.py
"""
import json
import os
import re
import sys
from collections import defaultdict, Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODES_ROOT = ROOT / "graph/nodes"
ALIAS_RESOLVER = ROOT / "working/wiki/data/alias-resolver.json"
BACKLINKS = ROOT / "working/wiki/data/backlink-counts.json"

UTC_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")
# Override with explicit date if argv[1] supplied (deterministic for re-runs)
if len(sys.argv) > 1:
    UTC_DATE = sys.argv[1]

OUTPUT = ROOT / f"working/audits/orphan-edges-{UTC_DATE}.md"
TSV_OUT = ROOT / f"working/audits/orphan-edges-{UTC_DATE}-cat1-full.tsv"

# Skip these subdirs per audit charter
SKIP_DIRS = {"_conflicts", "_unclassified"}

# Locked edge taxonomy (from reference/architecture.md)
LOCKED_EDGE_TYPES = {
    # Kinship & Family
    "PARENT_OF", "SIBLING_OF", "SPOUSE_OF", "BETROTHED_TO", "LOVER_OF",
    "WARD_OF", "ANCESTOR_OF", "HEIR_TO", "CADET_BRANCH_OF",
    # Political & Authority
    "RULES", "OVERLORD_OF", "SWORN_TO", "COMMANDS", "SERVES", "ADVISES",
    "HOLDS_TITLE", "SUCCEEDS", "CLAIMS", "APPOINTS", "DEPOSES",
    # Factional & Diplomatic
    "MEMBER_OF", "FOUNDED", "ALLIES_WITH", "OPPOSES", "MANIPULATES",
    "BETRAYS", "NEGOTIATES_WITH",
    # Military
    "FIGHTS_IN", "COMMANDS_IN", "KILLS", "EXECUTES", "CAPTURES",
    "PRISONER_OF", "BESIEGES", "DEFEATS", "DUELS",
    # Knowledge
    "KNOWS", "IGNORANT_OF", "SEEKS", "REVEALS_TO", "DECEIVES",
    "HOARDS", "INVESTIGATES", "TEACHES",
    # Emotional
    "PERCEIVED_AS", "TRUSTS", "DISTRUSTS", "RESPECTS", "FEARS",
    "LOVES", "HATES", "MOURNS", "PROTECTS", "RESENTS",
    # Spatial / Temporal
    "LOCATED_AT", "SEAT_OF", "TRAVELS_TO", "BORN_AT", "DIED_AT",
    "BURIED_AT", "CONTEMPORARY_WITH", "REGION_OF",
    # Possession
    "WIELDS", "OWNS", "ANCESTRAL_WEAPON_OF", "FORGED_BY",
    # Identity
    "ALIAS_OF", "DISGUISED_AS", "SAME_AS", "IMPERSONATES",
    # Cultural / Religious
    "CULTURE_OF", "WORSHIPS", "SACRED_TO", "CLERGY_OF", "RELIGION_OF",
    # Narrative
    "FORESHADOWS", "PARALLELS", "SUBVERTS", "ECHOES", "CONTRASTS",
    # Prophecy
    "FULFILLS", "APPEARS_TO_FULFILL", "SUBVERTS_PROPHECY",
    "PROPHESIED_BY", "SUBJECT_OF_PROPHECY",
    # Evidentiary
    "SUPPORTS", "CONTRADICTS", "CITED_BY",
    # Causal
    "CAUSES", "PREVENTS", "ENABLES", "MOTIVATES", "TRIGGERS",
    # Hospitality
    "GUEST_OF", "VIOLATES_GUEST_RIGHT", "GRANTS_SAFE_CONDUCT",
    # Common written-by extension
    "WRITTEN_BY",
}

# Religion-bleed legacy values (parser fixed in Session 27 but data not re-emitted)
RELIGION_BLEED_VALUES = {
    "religions", "old gods", "mixed", "mixed religions", "various",
    "gods of ghis", "dothraki",
}

# Match the slug convention used by wiki-pass2-emit-deterministic.py
def kebab(text):
    if not text:
        return ""
    text = re.sub(r"\[[^\]]*\]", "", text)
    text = re.sub(r"\([^)]*\)", "", text)
    text = text.strip().rstrip(".,;:")
    text = text.strip(" \"'`")
    text = text.lower()
    text = text.replace("'", "").replace("'", "").replace("'", "")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text


# Date detection - target slug looks like just a year/range
DATE_RE = re.compile(
    r"^\d+(-\d+)?-ac$|^\d+(-\d+)?-bc$|^\d+(-\d+)?$|"
    r"^c-\d+-ac$|^pre-\d+-ac$|"
    r"^\d+-ac-or-\d+-ac$|^\d+-ac-or-before$|^\d+-ac-or-after$|"
    r"^\d+-bc.*\d+-ac$|"
    r"^\d+-(or|to)-\d+-ac$"
)


def is_date_target(slug):
    return bool(DATE_RE.match(slug))


# --- Build slug index ---
print("Building slug index...", file=sys.stderr)
slug_index = {}
for type_dir in NODES_ROOT.iterdir():
    if not type_dir.is_dir() or type_dir.name in SKIP_DIRS:
        continue
    for path in type_dir.glob("*.node.md"):
        slug = path.stem.replace(".node", "")
        slug_index[slug] = path
print(f"  {len(slug_index)} nodes indexed", file=sys.stderr)


# --- Load alias-resolver ---
print("Loading alias-resolver...", file=sys.stderr)
with ALIAS_RESOLVER.open() as f:
    resolver = json.load(f)
alias_index = resolver.get("alias_to_canonical", {})
print(f"  {len(alias_index)} aliases", file=sys.stderr)


# --- Load backlink counts (for prioritizing Cat 1) ---
print("Loading backlink counts...", file=sys.stderr)
backlinks = {}
if BACKLINKS.exists():
    with BACKLINKS.open() as f:
        backlinks = json.load(f).get("backlinks", {})
print(f"  {len(backlinks)} entries", file=sys.stderr)


def in_count_for(slug):
    entry = backlinks.get(slug)
    return entry.get("in_count", 0) if entry else 0


# Edge line regex: matches "- TYPE[ (qual)]: target..."
EDGE_LINE_RE = re.compile(r"^- ([A-Z_]+)(?:\s*\(([^)]*)\))?\s*:\s*(.+?)\s*$")


def parse_edges_section(filepath):
    with filepath.open() as f:
        content = f.read()
    fm_match = re.search(r"^slug:\s*(.+?)\s*$", content, re.MULTILINE)
    source_slug = fm_match.group(1) if fm_match else filepath.stem.replace(".node", "")

    edges_match = re.search(r"^## Edges\s*$(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL)
    if not edges_match:
        return source_slug, None
    edges_block = edges_match.group(1)
    edges = []
    for line in edges_block.splitlines():
        if not line.strip():
            continue
        if not line.lstrip().startswith("-"):
            continue
        m = EDGE_LINE_RE.match(line)
        if not m:
            edges.append(("__MALFORMED__", None, line.rstrip()))
            continue
        edge_type, qualifier, target_text = m.groups()
        # Strip trailing (cite: ...) or (track_b: ...) or (wiki:...)
        target_clean = re.sub(r"\(cite:[^)]*\)\s*$", "", target_text).strip()
        target_clean = re.sub(r"\(track_b:[^)]*\)\s*$", "", target_clean).strip()
        target_clean = re.sub(r"\(wiki:[^)]*\)\s*$", "", target_clean).strip()
        # Strip [bracketed] qualifiers
        target_for_slug = re.sub(r"\[[^\]]*\]", "", target_clean).strip()
        edges.append((edge_type, target_clean, target_for_slug))
    return source_slug, edges


# Title-like detection
TITLE_LIKE_PATTERNS = [
    r"^warden-of-", r"^lord-of-", r"^lady-of-", r"^master-of-",
    r"^prince-of-", r"^princess-of-", r"^king-of-", r"^queen-of-",
    r"^hand-of-the-king", r"^lord-commander-", r"^high-",
    r"^grand-", r"^archmaester-?$", r"^lord-paramount-",
    r"^keeper-of-", r"^protector-of-", r"^defender-of-",
    r"^heir-to-", r"^maester-of-", r"^captain-of-",
    r"^ser$", r"^lady$", r"^lord$", r"^prince$", r"^princess$",
    r"^king$", r"^queen$", r"^khal$", r"^khaleesi$", r"^maester$",
    r"^archmaester$", r"^captain$", r"^castellan$", r"^septon$",
]
TITLE_RE = re.compile("|".join(TITLE_LIKE_PATTERNS))


def is_title_like(slug):
    return bool(TITLE_RE.match(slug))


# Walk all nodes
orphan_targets_cat1 = Counter()
orphan_target_examples_cat1 = defaultdict(list)
orphan_targets_cat2 = Counter()
orphan_target_examples_cat2 = defaultdict(list)
stale_religion_examples = []
date_bleed_examples = []
unknown_edge_types = Counter()
malformed_lines = []
title_orphans = Counter()

total_nodes = 0
total_edges = 0
edges_resolved = 0
nodes_with_no_edges_section = 0

for type_dir in sorted(NODES_ROOT.iterdir()):
    if not type_dir.is_dir() or type_dir.name in SKIP_DIRS:
        continue
    for filepath in sorted(type_dir.glob("*.node.md")):
        total_nodes += 1
        source_slug, edges = parse_edges_section(filepath)
        if edges is None:
            nodes_with_no_edges_section += 1
            continue
        for edge_type, target_clean, target_for_slug in edges:
            if edge_type == "__MALFORMED__":
                malformed_lines.append((source_slug, str(filepath), target_for_slug))
                continue
            total_edges += 1

            if edge_type not in LOCKED_EDGE_TYPES:
                unknown_edge_types[edge_type] += 1
                continue

            if not target_for_slug:
                malformed_lines.append((source_slug, str(filepath), f"{edge_type}: <empty>"))
                continue

            target_slug = kebab(target_for_slug)

            # Stale religion-bleed
            if edge_type == "WORSHIPS":
                lower_target = target_for_slug.lower().strip()
                if lower_target in RELIGION_BLEED_VALUES:
                    stale_religion_examples.append({
                        "source": source_slug, "edge_type": edge_type,
                        "target_text": target_for_slug, "target_slug": target_slug,
                    })
                    continue

            # Date-bleed
            if edge_type in ("BORN_AT", "DIED_AT", "BURIED_AT") and is_date_target(target_slug):
                date_bleed_examples.append({
                    "source": source_slug, "edge_type": edge_type,
                    "target_text": target_for_slug, "target_slug": target_slug,
                })
                continue

            # Direct slug match
            if target_slug in slug_index:
                edges_resolved += 1
                continue
            # Alias-resolver fallback (Cat 2)
            canonical = alias_index.get(target_slug)
            if canonical and canonical in slug_index:
                orphan_targets_cat2[(target_slug, canonical)] += 1
                if len(orphan_target_examples_cat2[(target_slug, canonical)]) < 5:
                    orphan_target_examples_cat2[(target_slug, canonical)].append({
                        "source": source_slug, "edge_type": edge_type,
                        "target_text": target_for_slug,
                    })
                continue
            # Cat 1 — genuinely missing
            orphan_targets_cat1[target_slug] += 1
            if len(orphan_target_examples_cat1[target_slug]) < 5:
                orphan_target_examples_cat1[target_slug].append({
                    "source": source_slug, "edge_type": edge_type,
                    "target_text": target_for_slug,
                })
            if is_title_like(target_slug):
                title_orphans[target_slug] += 1


# --- Compute totals ---
total_cat1_edges = sum(orphan_targets_cat1.values())
total_cat2_edges = sum(orphan_targets_cat2.values())
total_stale = len(stale_religion_examples)
total_date_bleed = len(date_bleed_examples)
total_orphans = total_cat1_edges + total_cat2_edges + total_stale + total_date_bleed
total_title_unique = len(title_orphans)
total_title_edges = sum(title_orphans.values())

cat1_rows = []
for target_slug, count in orphan_targets_cat1.items():
    cat1_rows.append({
        "target_slug": target_slug, "edge_count": count,
        "in_count": in_count_for(target_slug),
        "examples": orphan_target_examples_cat1[target_slug],
        "is_title": is_title_like(target_slug),
        "is_date": is_date_target(target_slug),
    })
cat1_rows.sort(key=lambda r: (-r["in_count"], -r["edge_count"], r["target_slug"]))

cat2_rows = []
for (target_slug, canonical), count in orphan_targets_cat2.items():
    cat2_rows.append({
        "target_slug": target_slug, "canonical": canonical,
        "edge_count": count,
        "examples": orphan_target_examples_cat2[(target_slug, canonical)],
    })
cat2_rows.sort(key=lambda r: -r["edge_count"])


# --- Write report ---
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
lines = []
P = lines.append
P(f"# Orphan Edges Audit — {UTC_DATE}")
P("")
P(f"**Nodes scanned:** {total_nodes}")
P(f"**Total edges checked:** {total_edges}")
P(f"**Edges that resolve cleanly:** {edges_resolved}")
P(f"**Orphan / problematic edges found:** {total_orphans}")
P("")
P("**Breakdown:**")
P(f"- Category 1 (target genuinely missing): {total_cat1_edges} edges across {len(cat1_rows)} unique missing targets")
P(f"- Category 2 (alias-mismatch — resolves via alias-resolver): {total_cat2_edges} edges across {len(cat2_rows)} unique alias slugs")
P(f"- Stale-data legacy (religion-bleed leftovers): {total_stale}")
P(f"- Edge-format issues (BORN_AT / DIED_AT / BURIED_AT date-bleed): {total_date_bleed}")
P(f"- Title-like missing targets (subset of Cat 1): {total_title_edges} edges, {total_title_unique} unique title slugs")
P("")
P(f"**Other observations:**")
P(f"- Unknown edge types encountered (schema-drift; deferred to schema-drift-auditor): {sum(unknown_edge_types.values())} occurrences across {len(unknown_edge_types)} types")
P(f"- Malformed edge lines: {len(malformed_lines)}")
P(f"- Nodes with no `## Edges` section: {nodes_with_no_edges_section}")
P("")

# --- Stale religion ---
P("---\n")
P("## Stale-data legacy: religion-bleed leftovers\n")
P("Location nodes still carrying legacy `WORSHIPS` edges with religion-field "
  "category labels as targets (e.g., `religions`, `Mixed`, `Old gods`) instead "
  "of actual religion entities. Parser fix landed in Session 27; these nodes "
  "have not been re-emitted. **Batch-fix recommendation: re-emit affected "
  "location nodes from the corrected parser output.**\n")
P("| Source node | Edge type | Target text | Target slug |")
P("|---|---|---|---|")
for ex in sorted(stale_religion_examples, key=lambda e: e["source"]):
    P(f"| `{ex['source']}` | {ex['edge_type']} | {ex['target_text']} | `{ex['target_slug']}` |")
P("")

# --- Date-bleed ---
P("---\n")
P("## Edge-format issues: BORN_AT / DIED_AT / BURIED_AT date-bleed\n")
if total_date_bleed == 0:
    P("**Zero date-bleed edges found.** The Session 27 parser fix is fully reflected in the data.")
else:
    P(f"**{total_date_bleed} edges still treat dates/year-ranges as the target slug.** "
      "These nodes were not part of the Session 27 re-emission wave and need a follow-up re-promote.")
    P("")
    P("Up to 50 examples (sorted by source):")
    P("")
    P("| Source node | Edge type | Target text | Target slug |")
    P("|---|---|---|---|")
    for ex in sorted(date_bleed_examples, key=lambda e: e["source"])[:50]:
        P(f"| `{ex['source']}` | {ex['edge_type']} | {ex['target_text']} | `{ex['target_slug']}` |")
P("")

# --- Title-like ---
P("---\n")
P("## Title-like missing targets\n")
P("Edges referencing title slugs that have no corresponding node "
  "(`warden-of-the-north`, `lord-of-dragonstone`, `ser`, `prince`, etc.). "
  "The `title` entity type exists; ~89 title nodes are populated but the "
  "broad title vocabulary used in `HOLDS_TITLE` edges is largely unpopulated.\n")
P(f"**{total_title_unique} unique title slugs referenced; {total_title_edges} total edge references.**\n")
P("**Recommendation:** stand up a Title Pass that promotes the most-referenced title slugs to actual nodes.\n")
P("Top 30 title slugs by edge-count:\n")
P("| Target slug | Edges referencing | in_count |")
P("|---|---|---|")
for slug, count in title_orphans.most_common(30):
    P(f"| `{slug}` | {count} | {in_count_for(slug)} |")
P("")

# --- Category 1 ---
P("---\n")
P("## Category 1: target genuinely missing\n")
P(f"Sorted by `in_count` desc, then by edge_count. Top 100 of {len(cat1_rows)} unique missing targets shown.\n")
P("Severity: **HIGH** for top entries (high in_count → many references → recovery candidate). **LOW** for long-tail singletons.\n")
P("| # | Target slug | Edges in graph | Cross-ref in_count | Title-like | Example source / edge_type / target text |")
P("|---|---|---|---|---|---|")
for idx, row in enumerate(cat1_rows[:100], 1):
    ex = row["examples"][0] if row["examples"] else {"source": "?", "edge_type": "?", "target_text": "?"}
    title_flag = "yes" if row["is_title"] else ""
    example_str = f"`{ex['source']}` / {ex['edge_type']} / {ex['target_text']}"
    P(f"| {idx} | `{row['target_slug']}` | {row['edge_count']} | {row['in_count']} | {title_flag} | {example_str} |")
P("")
if len(cat1_rows) > 100:
    P(f"_(Long tail: {len(cat1_rows) - 100} additional missing targets. See `{TSV_OUT.relative_to(ROOT)}` for the complete list.)_\n")

# --- Category 2 ---
P("---\n")
P("## Category 2: alias-mismatch (resolvable via alias-resolver)\n")
P(f"These targets fail direct slug-match but DO resolve via the alias-resolver. "
  f"**{total_cat2_edges} edges across {len(cat2_rows)} unique alias slugs** are affected.\n")
P("Severity: **MED** — slug-format-drift, not a graph gap. Recommend the graph "
  "layer consult the alias-resolver after a direct-slug miss.\n")
P("Top 50 by edge count:\n")
P("| Target slug attempted | Resolves to canonical | Edges affected | Example |")
P("|---|---|---|---|")
for row in cat2_rows[:50]:
    ex = row["examples"][0] if row["examples"] else {"source": "?", "edge_type": "?", "target_text": "?"}
    example_str = f"`{ex['source']}` / {ex['edge_type']} / {ex['target_text']}"
    P(f"| `{row['target_slug']}` | `{row['canonical']}` | {row['edge_count']} | {example_str} |")
P("")
if len(cat2_rows) > 50:
    P(f"_(Tail: {len(cat2_rows) - 50} additional alias-mismatch slugs.)_\n")

# --- Category 3 ---
P("---\n")
P("## Category 3: redirect-resolution (wiki redirect chain)\n")
P("**Not separately classified in this run.** The Session 27 cleanup leaves the "
  "most actionable signal in Cat 1 / Cat 2 / stale / date-bleed; redirect-resolution "
  "is a future pass.\n")
P("If a follow-up wants to mine Cat 3 specifically, the procedure: take Cat 1 "
  "entries with `in_count >= 5`, look up each `<Page_Name>.json` in `sources/wiki/_raw/`, "
  "and check whether the cached HTML body matches `<div class=\"redirectMsg\">…</div>`. "
  "If so, the target slug should be remapped to the redirect target.\n")

# --- Unknown edge types ---
if unknown_edge_types:
    P("---\n")
    P("## Unknown edge types (deferred to schema-drift-auditor)\n")
    P("Per the conflict protocol, these edges were skipped (their targets were not classified).\n")
    P("| Edge type | Occurrences |")
    P("|---|---|")
    for et, count in unknown_edge_types.most_common():
        P(f"| `{et}` | {count} |")
    P("")

# --- Malformed lines ---
if malformed_lines:
    P("---\n")
    P("## Malformed `## Edges` lines\n")
    P(f"{len(malformed_lines)} bullet lines did not match the `- TYPE: target` pattern. Sample (up to 30):\n")
    P("| Source node | Filename | Raw line |")
    P("|---|---|---|")
    for source, fp, raw in malformed_lines[:30]:
        raw_safe = raw.replace("|", "\\|")[:120]
        P(f"| `{source}` | `{Path(fp).name}` | `{raw_safe}` |")
    P("")

# --- Summary ---
P("---\n")
P("## Summary\n")
P(f"Of {total_edges} edges across {total_nodes} nodes, {edges_resolved} resolve "
  f"cleanly. {total_orphans} are orphan or stale, dominated by Cat 1 ({total_cat1_edges} "
  f"edges, {len(cat1_rows)} unique slugs). Date-bleed status: "
  f"{'complete' if total_date_bleed == 0 else f'{total_date_bleed} stragglers remain'}. "
  f"Religion-bleed leftovers: {total_stale}. Title-like targets are a structural gap: "
  f"{total_title_unique} title slugs referenced by {total_title_edges} edges with no node. "
  f"Cat 2 alias-mismatches ({total_cat2_edges} edges) are not gaps — they're handled the "
  f"moment the graph layer consults `working/wiki/data/alias-resolver.json` after a "
  f"direct-slug miss.\n")

# --- Recommendations ---
P("## Recommended actions\n")
P("Prioritized:\n")
i = 1
P(f"{i}. **HIGH — Re-emit the religion-bleed location nodes.** Stale-data leftovers "
  f"are the only category where data is actively wrong. Sources: "
  f"{', '.join(sorted(set(e['source'] for e in stale_religion_examples)))}.\n")
i += 1
if total_date_bleed > 0:
    sources = sorted(set(e['source'] for e in date_bleed_examples))
    P(f"{i}. **HIGH — Re-emit the {total_date_bleed} date-bleed BORN_AT/DIED_AT nodes.** "
      f"{len(sources)} unique source nodes affected. Sample: "
      f"{', '.join(sources[:10])}{' …' if len(sources) > 10 else ''}.\n")
    i += 1
P(f"{i}. **HIGH — Recovery list for Cat 1 top 50.** Promote highest-in_count missing "
  "targets into Tier 3 recovery. See Cat 1 table.\n")
i += 1
P(f"{i}. **MED — Wire alias-resolver into the graph query layer.** All {total_cat2_edges} "
  f"Cat 2 mismatches resolve once lookup consults `alias-resolver.json` on direct-slug miss. "
  f"Avoids touching {len(cat2_rows)} source nodes.\n")
i += 1
P(f"{i}. **MED — Stand up a Title Pass.** Promote the top {min(30, total_title_unique)} "
  "title slugs (warden-of-the-north, lord-of-dragonstone, hand-of-the-king, "
  "ser, prince, princess, king, queen, etc.) to actual `title` nodes.\n")
i += 1
P(f"{i}. **LOW — Defer Cat 1 long tail** (in_count <= 1). Natural backlog; revisit "
  "after Pass 1 chapter extractions add their own missing-target signal.\n")
i += 1
P(f"{i}. **LOW — Run schema-drift-auditor** on the {len(unknown_edge_types)} non-locked edge types observed.\n")

OUTPUT.write_text("\n".join(lines))

# Cat 1 long-tail TSV
with TSV_OUT.open("w") as f:
    f.write("rank\ttarget_slug\tedge_count\tin_count\tis_title\tis_date\texample_source\texample_edge_type\texample_target_text\n")
    for idx, row in enumerate(cat1_rows, 1):
        ex = row["examples"][0] if row["examples"] else {"source": "", "edge_type": "", "target_text": ""}
        f.write(f"{idx}\t{row['target_slug']}\t{row['edge_count']}\t{row['in_count']}\t"
                f"{int(row['is_title'])}\t{int(row['is_date'])}\t"
                f"{ex['source']}\t{ex['edge_type']}\t{ex['target_text']}\n")

print(f"\nReport: {OUTPUT}", file=sys.stderr)
print(f"Cat1 TSV: {TSV_OUT}", file=sys.stderr)
print(f"\nTotals:", file=sys.stderr)
print(f"  nodes scanned: {total_nodes}", file=sys.stderr)
print(f"  edges checked: {total_edges}", file=sys.stderr)
print(f"  edges resolved cleanly: {edges_resolved}", file=sys.stderr)
print(f"  cat1 (genuinely missing): {total_cat1_edges} edges / {len(cat1_rows)} unique slugs", file=sys.stderr)
print(f"  cat2 (alias-mismatch): {total_cat2_edges} edges / {len(cat2_rows)} unique slugs", file=sys.stderr)
print(f"  stale religion-bleed: {total_stale}", file=sys.stderr)
print(f"  date-bleed: {total_date_bleed}", file=sys.stderr)
print(f"  unknown edge types: {len(unknown_edge_types)}", file=sys.stderr)
print(f"  malformed lines: {len(malformed_lines)}", file=sys.stderr)
