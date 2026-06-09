#!/usr/bin/env python3
"""plate5-merge.py — Gated merge of all staged edge-modeling work into the canonical graph.

This is the FIRST plate that writes to graph/edges/edges.jsonl. It:
  1. Backs up edges.jsonl to graph/edges/_regrounding/edges-pre-reification-<ISO date>.jsonl
  2. Applies in order:
     - Plate 0 normalizer flips (10) + Aerys merge (3 repoints, 1 node quarantined)
     - Plate 2.5 schema fixes: 27 event-type retypes + 12 drift retypes + 4 high-conf collisions
     - Plate 3: 219 minted event nodes (title→name on mint), 914 role edges (filtered to 898 via
       location alias map + skip-rules), 55 supersede stamps
     - Plate 4 cluster: 51 SUB_BEAT_OF edges + 2 of 3 DUPLICATE_OF (third skipped — wiki target
       is being retyped to meta.chapter, violates Contract 10)
     - S77 cleanups: drop 2 LOVES rows + retype 22 ASSAULTS → ATTACKS (10 stay ASSAULTS;
       sexual-violence canon)
  3. Produces working/edge-modeling/plate5-merge-diff.md with before/after counts

Run with --dry-run (default) to preview. Run with --apply to write.
"""
import argparse
import json
import os
import shutil
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDGES_PATH = ROOT / "graph/edges/edges.jsonl"
NODES_ROOT = ROOT / "graph/nodes"
EVENTS_DIR = NODES_ROOT / "events"
CONFLICTS_DIR = NODES_ROOT / "_conflicts"
REGROUNDING_DIR = ROOT / "graph/edges/_regrounding"

EM = ROOT / "working/edge-modeling"
DIFF_OUT = EM / "plate5-merge-diff.md"

# --- Staged-input file paths ---
NORMALIZER_CANDS = EM / "normalizer-candidates.jsonl"
AERYS_CANDS = EM / "aerys-merge-candidates.jsonl"
SCHEMA_FIXES = EM / "plate2.5-schema-fixes/event-type-corrections.jsonl"
DRIFT_CANDS = EM / "drift-reclassify-candidates.jsonl"
COLLISION_CANDS = EM / "collision-merge-candidates.jsonl"
PLATE3_MINTS_DIR = EM / "plate3-full/minted-event-nodes"
PLATE3_ROLE_EDGES = EM / "plate3-full/role-edges-staging.jsonl"
PLATE3_SUPERSEDE = EM / "plate3-full/supersede-candidates.jsonl"
PLATE4_CLUSTER = EM / "plate4-wiki-cluster/cluster-edges-staging.jsonl"

UTC_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# --- Per-session decision constants ---

# Q1=a applied: drop 5 role edges targeting the 2 fuzzy-match queue items
HUB_QUEUE_SLUGS_TO_DROP = {"siege-of-storm-s-end-recalled"}

# Q2=a applied: location alias map (8 confirmed-safe rewrites; rest skip)
LOCATION_FIX_MAP = {
    "the-eyrie": "eyrie",
    "king-s-landing": "kings-landing",
    "the-wall": "wall",
    "the-twins": "twins",
    "the-greenblood": "greenblood",
    "the-septry": "septry",
    "castle-darry": "darry",
    "crossroads-inn": "inn-at-the-crossroads",
}
# Unresolvable LOCATED_AT target slugs (skipped at merge time, logged in diff):
LOCATION_SKIP_SLUGS = {
    "castle-sept", "dragon-pit-meereen", "great-pit-of-daznak",
    "lhazareen-town", "mouth-of-the-mander", "small-hall-red-keep",
    "the-ford", "throne-room-red-keep", "winterfell-battlements",
    "winterfell-godswood",
}

# Q3=a applied: 22 ASSAULTS rows to retype to ATTACKS (10 stay ASSAULTS — sexual-violence canon).
# Keyed by (source_slug, target_slug, evidence_chapter) for exact match.
ASSAULTS_TO_RETYPE = {
    # (source, target) — physical/non-sexual, retype to ATTACKS
    ("jaime-lannister", "bran-stark"),
    ("shaggydog", "luwin"),
    ("viserys-targaryen", "daenerys-targaryen"),
    ("daenerys-targaryen", "eroeh"),
    ("haggo", "mirri-maz-duur"),
    ("cersei-lannister", "eddard-stark"),
    ("grenn", "jon-snow"),
    ("joffrey-baratheon", "mycah"),
    ("biter", "arya-stark"),
    ("rorge", "arya-stark"),
    ("mandon-moore", "tyrion-lannister"),
    ("robert-baratheon", "joffrey-baratheon"),
    ("tyrion-lannister", "jaime-lannister"),
    ("brienne-tarth", "vargo-hoat"),
    ("biter", "brienne-tarth"),
    ("cersei-lannister", "blue-bard"),
    ("hobber-redwyne", "samwell-tarly"),
    ("horas-redwyne", "samwell-tarly"),
    ("glendon-hewett", "jon-snow"),
    ("victarion-greyjoy", "ralf-the-limper"),
    ("duck", "lorent-caswell"),
}
# These 11 stay ASSAULTS (true sexual-violence canon or in-story abuse vignette):
# drogo→daenerys, robert→cersei, joffrey→sansa, theon→kyra, marillion→sansa,
# petyr→sansa, tywin→tysha, gregor→pia, burton-humble→kerwin, four-storms→kerwin,
# handsome-man→her-little-flower (House of Black and White acolyte's backstory).

# Q4=a applied: skip these 2 collision candidates (per cleanup-decisions-resolved.md)
COLLISION_SKIP_CONFIDENCE = {"medium", "low"}

# 2 LOVES rows to drop (S77 carryover)
LOVES_TO_DROP = {
    ("tyrion-lannister", "cersei-lannister", "LOVES"),
    ("cersei-lannister", "tyrion-lannister", "LOVES"),
}

# 1 of 3 DUPLICATE_OF skipped: wiki target is in drift-reclassify-candidates
DUPLICATE_OF_SKIP_MINTS = {"mutiny-plan-reviewed"}


# ============================================================================
# Helpers
# ============================================================================

def load_jsonl(path):
    """Load a JSONL file into a list of dicts."""
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def edge_key(d):
    """Canonical key for matching edges across files."""
    return (d.get("edge_type"), d.get("source_slug"), d.get("target_slug"),
            d.get("evidence_chapter"), d.get("evidence_ref"))


def all_node_slugs():
    """Set of every node slug in graph/nodes/**."""
    return {p.stem.replace(".node", "") for p in NODES_ROOT.rglob("*.node.md")}


def event_node_slugs():
    """Set of slugs in graph/nodes/events/."""
    return {p.stem.replace(".node", "") for p in EVENTS_DIR.glob("*.node.md")}


# ============================================================================
# Merge phases
# ============================================================================

class MergeReport:
    """Accumulates per-phase deltas for the final diff report."""

    def __init__(self):
        self.phases = []  # list of (phase_name, dict of counters)
        self.notes = []  # free-text notes
        self.before = {}
        self.after = {}

    def add(self, phase, **counters):
        self.phases.append((phase, counters))

    def note(self, msg):
        self.notes.append(msg)


def backup_edges(dry_run):
    """Step 1: Backup edges.jsonl to _regrounding/."""
    REGROUNDING_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = REGROUNDING_DIR / f"edges-pre-reification-{UTC_DATE}.jsonl"
    if not dry_run:
        shutil.copy2(EDGES_PATH, backup_path)
    return backup_path


def apply_plate0_normalizer(edges, report):
    """Step 2a: Apply 10 normalizer flips. Edges is a list of edge dicts (mutated)."""
    flips = load_jsonl(NORMALIZER_CANDS)
    flipped_keys = {edge_key(d) for d in flips if d.get("normalizer_action") == "flipped"}
    # The flipped rows in normalizer-candidates already have the AFTER source/target swapped
    # vs edges.jsonl, but the key by (edge_type, source, target, evidence_chapter, evidence_ref)
    # would match the AFTER state, not the BEFORE state. Build before-keys instead.
    before_keys = set()
    for d in flips:
        if d.get("normalizer_action") == "flipped":
            # The BEFORE state has source/target swapped from the row as written
            # (rows in normalizer-candidates are written in "kept" orientation,
            # for "flipped" the candidate row IS the AFTER state per the diff doc).
            before_keys.add(
                (d["edge_type"], d["target_slug"], d["source_slug"],
                 d.get("evidence_chapter"), d.get("evidence_ref"))
            )

    flip_count = 0
    for e in edges:
        k = (e.get("edge_type"), e.get("source_slug"), e.get("target_slug"),
             e.get("evidence_chapter"), e.get("evidence_ref"))
        if k in before_keys:
            e["source_slug"], e["target_slug"] = e["target_slug"], e["source_slug"]
            e.setdefault("plate5_normalizer", "flipped at plate5")
            flip_count += 1

    report.add("Plate 0 normalizer", flipped=flip_count, expected=10)
    if flip_count != 10:
        report.note(f"⚠️ normalizer: expected 10 flips, applied {flip_count}")


def apply_aerys_merge(edges, report, dry_run):
    """Step 2a': Repoint 3 phantom aerys-targaryen edges; quarantine the empty node."""
    aerys_rows = load_jsonl(AERYS_CANDS)
    # Each row has {original, rewritten}
    # Match by 'original' key, rewrite source/target per 'rewritten'
    repoint_count = 0
    for row in aerys_rows:
        orig = row["original"]
        rw = row["rewritten"]
        orig_key = edge_key(orig)
        for e in edges:
            if edge_key(e) == orig_key:
                # Repoint
                e["source_slug"] = rw["source_slug"]
                e["target_slug"] = rw["target_slug"]
                e.setdefault("plate5_aerys_merge", "phantom-redirect")
                repoint_count += 1
                break

    # Quarantine the empty aerys-targaryen node
    src = NODES_ROOT / "characters" / "aerys-targaryen.node.md"
    dst = CONFLICTS_DIR / "aerys-targaryen.node.md"
    quarantined = False
    if src.exists():
        if not dry_run:
            CONFLICTS_DIR.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
        quarantined = True

    report.add("Plate 0 Aerys merge", repointed=repoint_count, expected=3,
               quarantined_node=int(quarantined))


def apply_plate2_5_schema_fixes(report, dry_run):
    """Step 2c': 27 event-type retypes in node frontmatter."""
    fixes = load_jsonl(SCHEMA_FIXES)
    applied = 0
    skipped = []
    for row in fixes:
        path = ROOT / row["node_path"]
        if not path.exists():
            skipped.append(row["slug"])
            continue
        text = path.read_text()
        old_type_line = f"type: {row['current_type']}"
        new_type_line = f"type: {row['new_type']}"
        if old_type_line not in text:
            skipped.append(row["slug"] + " (no current type match)")
            continue
        text = text.replace(old_type_line, new_type_line, 1)
        if not dry_run:
            path.write_text(text)
        applied += 1
    report.add("Plate 2.5 schema fixes (event sub-types)",
               applied=applied, expected=27, skipped=len(skipped))
    if skipped:
        report.note(f"Schema-fix skipped slugs: {skipped[:5]}{'...' if len(skipped) > 5 else ''}")


def apply_plate2_5_drift(report, dry_run):
    """Step 2c'': 12 drift retypes (event.battle → meta.chapter on chapter nodes)."""
    cands = load_jsonl(DRIFT_CANDS)
    applied = 0
    already_done = 0
    missing = 0
    for row in cands:
        slug = row.get("slug") or row.get("node_slug")
        new_type = row.get("proposed_type") or row.get("new_type")
        current = row.get("current_type", "event.battle")
        matches = list(NODES_ROOT.rglob(f"{slug}.node.md"))
        if not matches:
            missing += 1
            continue
        path = matches[0]
        text = path.read_text()
        old_line = f"type: {current}"
        new_line = f"type: {new_type}"
        if old_line in text:
            text = text.replace(old_line, new_line, 1)
            if not dry_run:
                path.write_text(text)
            applied += 1
        elif new_line in text:
            already_done += 1
    report.add("Plate 2.5 drift retypes (chapter articles)",
               applied=applied, already_done=already_done, missing=missing,
               total_handled=applied + already_done, expected=12)


def apply_plate2_5_collisions(edges, report, dry_run):
    """Step 2c''': 4 high-conf collision merges. Move losing node(s) to _conflicts/, repoint edges."""
    cands = load_jsonl(COLLISION_CANDS)
    merges_applied = 0
    edges_repointed = 0
    nodes_quarantined = 0
    skipped = []
    for row in cands:
        if row["confidence"] in COLLISION_SKIP_CONFIDENCE:
            skipped.append(f"{row['canonical_slug']} ({row['confidence']})")
            continue
        canonical = row["canonical_slug"]
        for loser_slug in row["merge_slugs"]:
            # Repoint all edges pointing to or from the loser
            for e in edges:
                if e.get("source_slug") == loser_slug:
                    e["source_slug"] = canonical
                    e.setdefault("plate5_collision_repoint", f"from {loser_slug}")
                    edges_repointed += 1
                if e.get("target_slug") == loser_slug:
                    e["target_slug"] = canonical
                    e.setdefault("plate5_collision_repoint", f"to {canonical}")
                    edges_repointed += 1
            # Quarantine loser node
            matches = list(NODES_ROOT.rglob(f"{loser_slug}.node.md"))
            if matches:
                src = matches[0]
                dst = CONFLICTS_DIR / src.name
                if not dry_run:
                    CONFLICTS_DIR.mkdir(parents=True, exist_ok=True)
                    if dst.exists():
                        # Rare; append slug to avoid clobber
                        dst = CONFLICTS_DIR / f"{loser_slug}-collision.node.md"
                    shutil.move(str(src), str(dst))
                nodes_quarantined += 1
        merges_applied += 1
    report.add("Plate 2.5 collision merges (high-conf only)",
               merges=merges_applied, expected=4,
               edges_repointed=edges_repointed,
               nodes_quarantined=nodes_quarantined,
               skipped=len(skipped))
    if skipped:
        report.note(f"Collision skipped (per Q4=a): {skipped}")


def mint_plate3_event_nodes(report, dry_run, duplicate_of_skipped_mints):
    """Step 2b (mint phase): write 219 minted event nodes with title→name rewrite.
    Skip the mints flagged DUPLICATE_OF (their role edges get repointed instead).
    """
    minted = 0
    skipped_dup_count = 0
    written_slugs = set()
    for f in sorted(PLATE3_MINTS_DIR.glob("*.node.md")):
        slug = f.stem.replace(".node", "")
        if slug in duplicate_of_skipped_mints:
            skipped_dup_count += 1
            continue
        text = f.read_text()
        # title: → name: (S86 schema unification)
        text = text.replace("\ntitle: ", "\nname: ", 1)
        dst = EVENTS_DIR / f.name
        if not dry_run:
            EVENTS_DIR.mkdir(parents=True, exist_ok=True)
            dst.write_text(text)
        minted += 1
        written_slugs.add(slug)
    report.add("Plate 3 event-node mints",
               minted=minted, expected=219, skipped_duplicate_of=skipped_dup_count)
    return written_slugs


def append_plate3_role_edges(edges, report, duplicate_of_repoints, minted_slugs):
    """Step 2b (role edges): append 914 role edges with filters applied.
    - Drop 5 edges targeting siege-of-storm-s-end-recalled (Q1=a)
    - Apply location alias map for LOCATED_AT (Q2=a)
    - Drop unresolvable LOCATED_AT targets (Q2=a)
    - Repoint role-edge targets for DUPLICATE_OF mints
    - Drop role edges whose source/target is a duplicate-of-skipped mint
    """
    rows = load_jsonl(PLATE3_ROLE_EDGES)
    appended = 0
    dropped_hub_queue = 0
    dropped_loc_orphan = 0
    located_at_remapped = 0
    repointed_duplicate_of = 0

    for r in rows:
        target = r["target_slug"]
        source = r["source_slug"]

        # Drop role edges pointing to the 5 fuzzy-match queue items
        if target in HUB_QUEUE_SLUGS_TO_DROP:
            dropped_hub_queue += 1
            continue

        # DUPLICATE_OF mint repoint: if target is a mint flagged DUPLICATE_OF, repoint
        if target in duplicate_of_repoints:
            r = dict(r)
            r["target_slug"] = duplicate_of_repoints[target]
            r["plate5_duplicate_of_repoint"] = target
            repointed_duplicate_of += 1
            target = r["target_slug"]

        # LOCATED_AT remap or drop
        if r["edge_type"] == "LOCATED_AT":
            if target in LOCATION_FIX_MAP:
                r = dict(r)
                r["target_slug"] = LOCATION_FIX_MAP[target]
                r["plate5_location_remap"] = target
                located_at_remapped += 1
                target = r["target_slug"]
            elif target in LOCATION_SKIP_SLUGS:
                dropped_loc_orphan += 1
                continue
            # else: target already resolves; pass through

        # Match plate3 emit-schema to edges.jsonl schema by reusing the same fields.
        # plate3 rows already include all required fields. Tag with merged_at.
        r.setdefault("decision", "emit_edge")
        r.setdefault("candidate_kind", "plate3-reified")
        r["plate5_merged_at"] = datetime.now(timezone.utc).isoformat()
        edges.append(r)
        appended += 1

    report.add("Plate 3 role edges",
               appended=appended, staged=914,
               dropped_hub_queue=dropped_hub_queue,
               dropped_location_orphan=dropped_loc_orphan,
               located_at_remapped=located_at_remapped,
               repointed_duplicate_of=repointed_duplicate_of)


def mark_plate3_supersedes(edges, report):
    """Step 2b': stamp `superseded_by: <hub-slug>` on 55 existing edges.

    Tries swapped (source↔target) keys as fallback, because Plate 0 normalizer flips ran
    before this phase — semantically-equivalent edges may now have swapped endpoints.
    """
    cands = load_jsonl(PLATE3_SUPERSEDE)
    stamped = 0
    for c in cands:
        ck = edge_key(c)
        ck_swapped = (c.get("edge_type"), c.get("target_slug"), c.get("source_slug"),
                      c.get("evidence_chapter"), c.get("evidence_ref"))
        hub = c.get("superseded_by")
        if not hub:
            continue
        for e in edges:
            ek = edge_key(e)
            if ek == ck or ek == ck_swapped:
                e["superseded_by"] = hub
                e["plate5_superseded_note"] = c.get("supersede_note", "")[:200]
                if ek == ck_swapped:
                    e["plate5_supersede_via_swap"] = True
                stamped += 1
                break
    report.add("Plate 3 supersede stamps",
               stamped=stamped, expected=55)


def apply_plate4_cluster(edges, report):
    """Step 2c: 51 SUB_BEAT_OF + 2 of 3 DUPLICATE_OF (1 skipped).
    Returns: (duplicate_of_repoints map, set of mint slugs skipped per DUPLICATE_OF).
    """
    rows = load_jsonl(PLATE4_CLUSTER)
    sub_beat_appended = 0
    duplicate_of_repoints = {}  # mint_slug → wiki_slug
    duplicate_of_skipped_mints = set()
    duplicate_of_applied = 0
    duplicate_of_skipped = 0

    for r in rows:
        if r["edge_type"] == "SUB_BEAT_OF":
            r = dict(r)
            r["decision"] = "emit_edge"
            r["candidate_kind"] = "plate4-wiki-cluster"
            r["plate5_merged_at"] = datetime.now(timezone.utc).isoformat()
            edges.append(r)
            sub_beat_appended += 1
        elif r["edge_type"] == "DUPLICATE_OF":
            mint = r["source_slug"]
            wiki = r["target_slug"]
            if mint in DUPLICATE_OF_SKIP_MINTS:
                duplicate_of_skipped += 1
                continue
            duplicate_of_repoints[mint] = wiki
            duplicate_of_skipped_mints.add(mint)
            duplicate_of_applied += 1

    report.add("Plate 4 SUB_BEAT_OF edges",
               appended=sub_beat_appended, expected=51)
    report.add("Plate 4 DUPLICATE_OF applied",
               applied=duplicate_of_applied, expected=2, skipped=duplicate_of_skipped)
    if duplicate_of_skipped:
        report.note(
            "DUPLICATE_OF skipped: mutiny-plan-reviewed (target a-storm-of-swords-prologue "
            "is being retyped to meta.chapter, would violate Contract 10 on AGENT_IN/VICTIM_IN)"
        )
    return duplicate_of_repoints, duplicate_of_skipped_mints


def apply_s77_loves_drops(edges, report):
    """Step 3a: drop 2 cersei↔tyrion LOVES rows."""
    before = len(edges)
    keepers = []
    dropped = 0
    for e in edges:
        et = e.get("edge_type")
        ss = e.get("source_slug")
        ts = e.get("target_slug")
        if (ss, ts, et) in LOVES_TO_DROP:
            dropped += 1
            continue
        keepers.append(e)
    report.add("S77 LOVES drops (cersei↔tyrion)",
               dropped=dropped, expected=2)
    edges[:] = keepers


def apply_s77_assaults_retype(edges, report):
    """Step 3b: retype 22 ASSAULTS → ATTACKS where not sexual-violence canon."""
    retyped = 0
    kept = 0
    for e in edges:
        if e.get("edge_type") != "ASSAULTS":
            continue
        pair = (e.get("source_slug"), e.get("target_slug"))
        if pair in ASSAULTS_TO_RETYPE:
            e["edge_type"] = "ATTACKS"
            e["plate5_assaults_retype"] = "S77 cleanup — non-sexual physical assault"
            retyped += 1
        else:
            kept += 1
    report.add("S77 ASSAULTS retypes",
               retyped=retyped, expected=22,
               kept_as_assaults=kept)


# ============================================================================
# Report writing
# ============================================================================

def write_diff_report(report, before_counts, after_counts, backup_path):
    """Emit working/edge-modeling/plate5-merge-diff.md."""
    DIFF_OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Plate 5 Merge — Before/After Diff",
        "",
        f"**Date:** {UTC_DATE}",
        f"**Backup:** `{backup_path.relative_to(ROOT)}`",
        "",
        "## Top-level counts",
        "",
        "| Item | Before | After | Δ |",
        "|---|---:|---:|---:|",
    ]
    for k in sorted(before_counts.keys() | after_counts.keys()):
        b = before_counts.get(k, 0)
        a = after_counts.get(k, 0)
        delta = a - b
        sign = "+" if delta > 0 else ""
        lines.append(f"| {k} | {b:,} | {a:,} | {sign}{delta:,} |")
    lines += ["", "## Per-phase deltas", ""]
    for phase, counters in report.phases:
        lines.append(f"### {phase}")
        lines.append("")
        for k, v in counters.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
    if report.notes:
        lines += ["## Notes", ""]
        for n in report.notes:
            lines.append(f"- {n}")
        lines.append("")
    DIFF_OUT.write_text("\n".join(lines))


# ============================================================================
# Main
# ============================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="Actually write changes. Default is --dry-run.")
    args = ap.parse_args()
    dry_run = not args.apply

    print(f"\n=== plate5-merge.py — {'APPLY' if not dry_run else 'DRY-RUN'} ({UTC_DATE}) ===\n",
          file=sys.stderr)

    # Load current edges
    edges = load_jsonl(EDGES_PATH)
    before_edge_count = len(edges)
    before_event_node_count = len(list(EVENTS_DIR.glob("*.node.md")))

    before_counts = {
        "graph/edges/edges.jsonl rows": before_edge_count,
        "graph/nodes/events/ files": before_event_node_count,
    }
    report = MergeReport()

    # Step 1: Backup
    backup_path = backup_edges(dry_run)
    print(f"[1] Backup → {backup_path}", file=sys.stderr)

    # Step 2a: Plate 0 normalizer
    apply_plate0_normalizer(edges, report)
    print(f"[2a] Plate 0 normalizer applied", file=sys.stderr)

    # Step 2a': Aerys merge
    apply_aerys_merge(edges, report, dry_run)
    print(f"[2a'] Aerys merge applied", file=sys.stderr)

    # Step 2c': Plate 2.5 schema fixes (event sub-types)
    apply_plate2_5_schema_fixes(report, dry_run)
    print(f"[2c'] Plate 2.5 schema fixes applied", file=sys.stderr)

    # Step 2c'': Plate 2.5 drift retypes
    apply_plate2_5_drift(report, dry_run)
    print(f"[2c''] Plate 2.5 drift retypes applied", file=sys.stderr)

    # Step 2c''': Plate 2.5 collision merges
    apply_plate2_5_collisions(edges, report, dry_run)
    print(f"[2c'''] Plate 2.5 collision merges applied", file=sys.stderr)

    # Step 2c: Plate 4 cluster (run BEFORE plate 3 minting so DUPLICATE_OF skips propagate)
    duplicate_of_repoints, duplicate_of_skipped_mints = apply_plate4_cluster(edges, report)
    print(f"[2c] Plate 4 cluster applied", file=sys.stderr)

    # Step 2b (mint phase)
    minted_slugs = mint_plate3_event_nodes(report, dry_run, duplicate_of_skipped_mints)
    print(f"[2b mint] Plate 3 mints written", file=sys.stderr)

    # Step 2b (role-edge phase)
    append_plate3_role_edges(edges, report, duplicate_of_repoints, minted_slugs)
    print(f"[2b roles] Plate 3 role edges appended", file=sys.stderr)

    # Step 2b': Mark supersedes
    mark_plate3_supersedes(edges, report)
    print(f"[2b'] Supersede stamps applied", file=sys.stderr)

    # Step 3a: S77 LOVES drops
    apply_s77_loves_drops(edges, report)
    print(f"[3a] S77 LOVES drops applied", file=sys.stderr)

    # Step 3b: S77 ASSAULTS retypes
    apply_s77_assaults_retype(edges, report)
    print(f"[3b] S77 ASSAULTS retypes applied", file=sys.stderr)

    # Write merged edges.jsonl
    after_edge_count = len(edges)
    after_event_node_count = before_event_node_count + len(minted_slugs)
    if not dry_run:
        with open(EDGES_PATH, "w") as f:
            for e in edges:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")

    after_counts = {
        "graph/edges/edges.jsonl rows": after_edge_count,
        "graph/nodes/events/ files": after_event_node_count,
    }

    # Write diff report
    write_diff_report(report, before_counts, after_counts, backup_path)
    print(f"\n[done] Diff → {DIFF_OUT.relative_to(ROOT)}", file=sys.stderr)

    # Summary on stderr
    print(f"\nedges.jsonl: {before_edge_count:,} → {after_edge_count:,} ({after_edge_count - before_edge_count:+,})",
          file=sys.stderr)
    print(f"events/ nodes: {before_event_node_count:,} → {after_event_node_count:,} ({after_event_node_count - before_event_node_count:+,})",
          file=sys.stderr)

    if dry_run:
        print("\n*** DRY-RUN — no files modified. Re-run with --apply to write. ***\n",
              file=sys.stderr)


if __name__ == "__main__":
    main()
