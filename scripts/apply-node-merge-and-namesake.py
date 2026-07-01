#!/usr/bin/env python3
"""
apply-node-merge-and-namesake.py — Session 180, graph-parentage-cleanup phase 2.

Applies the THREE review-cleared fix classes left over after S179's 138 auto-apply
deletes (DUPLICATE_PARENT_NODE / WRONG_NAMESAKE / NODE_SPLIT). Every action below was
independently confirmed against the local wiki cache (`sources/wiki/_raw/`) by three
fresh review passes (`working/graph-cleanup/review-{duplicate-parent-node,
wrong-namesake,node-split}.md`), plus a handful of adjacent latent bugs this script's
author found by direct wiki lookup while cross-checking REASSIGN targets for
pre-existing conflicts (documented inline below, each with its own evidence).

Three action kinds:

  MERGES    Two slugs are the same real person (redirect / duplicate-edge confirmed).
            Every edge on the retired slug is re-pointed to the survivor slug (deduping
            exact repeats), the retired slug's natural name is added as a spaced-phrase
            alias on the survivor (unless flagged skip_alias — see ALAYNE_SKIP_ALIAS),
            and the retired node file is deleted (empty stub, git-recoverable).

  DELETES   A (parent, child) PARENT_OF edge that is flat-out wrong: the parent slug is
            a different, unrelated namesake (wrong era / wrong disambiguation-page
            entry), OR the fact is a pure duplicate of a fact that already lives on a
            disambiguated variant elsewhere in the graph. Deleting loses nothing — the
            correct edge already exists.

  REASSIGNS A (parent, child) edge where the FACT is real but was wrongly resolved to a
            disambiguation-page slug on one side. Re-point that side to the correct
            disambiguated slug. Every reassign target below was checked against
            edges.jsonl first to confirm it does not create a NEW duplicate/conflation
            (see inline notes) — several needed a companion DELETE of a pre-existing
            wrong-slug duplicate at the target to net out to a clean <=2-parent result.

Default is DRY-RUN. Pass --apply to write graph/edges/edges.jsonl and delete the two
retired node files. Prints before/after parent-count checks for every touched child so
a bad interaction is caught before write.

  python3 scripts/apply-node-merge-and-namesake.py            # dry run
  python3 scripts/apply-node-merge-and-namesake.py --apply    # write
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph/edges/edges.jsonl"
NODES_CHAR_DIR = REPO / "graph/nodes/characters"

# ---------------------------------------------------------------------------
# MERGES: (retired_slug, survivor_slug, retired_natural_name, skip_alias)
# ---------------------------------------------------------------------------
MERGES = [
    # elenda-caron.node.md is an empty wiki-stub; Elenda_Caron.json is a literal
    # "Redirect to: Elenda Baratheon." All 6 of its edges are exact duplicates of
    # edges already on elenda-baratheon (verified below) -> pure dedupe, no new edges.
    ("elenda-caron", "elenda-baratheon", "Elenda Caron", False),
    # alayne.node.md is an empty wiki-stub for the 3-way disambiguation page "Alayne"
    # (Alayne Baelish / Alayne Royce / Alayne Stone=Sansa's alias). Its 2 edges both
    # independently assert "Alayne Baelish is Petyr's mother" (confirmed via edges.jsonl
    # direction check, not a Sansa mix-up). skip_alias=True: do NOT add bare "alayne" as
    # an alias on alayne-baelish -- "Alayne" unqualified is far more strongly associated
    # with Sansa's alias identity (Alayne Stone) in reader queries, and no such alias
    # exists today (all-node-alias-lookup.json has zero "alayne" entry) -- adding it
    # here would misroute a much higher-value future query. This is a case-by-case
    # deviation from the blanket merge-alias rule, not a rule change.
    ("alayne", "alayne-baelish", "Alayne", True),
]

# ---------------------------------------------------------------------------
# DELETES: (parent_slug, child_slug, short reason)
# Every row's "true parent already exists" claim was checked mechanically against
# edges.jsonl (variant-of-parent already carries the child) or via direct wiki-page
# fetch (father/mother field), per the three review docs plus this script's own
# REASSIGN pre-checks.
# ---------------------------------------------------------------------------
DELETES = [
    # --- DUPLICATE_PARENT_NODE reject-different-people, redundant-on-variant ---
    ("alys-arryn", "aelor-targaryen", "bare disambig page; alys-arryn-wife-of-rhaegel already carries this child"),
    ("alys-arryn", "aelora-targaryen", "same"),
    ("alys-arryn", "daenora-targaryen", "same"),
    ("daella-targaryen", "aemma-arryn", "bare disambig page; daella-targaryen-daughter-of-jaehaerys-i already carries this child"),
    ("aegon-targaryen", "aerea-targaryen", "bare disambig page (10 Aegons); aegon-targaryen-son-of-aenys-i already carries this child"),
    ("aegon-targaryen", "maegon-targaryen", "bare disambig page; aegon-targaryen-son-of-gaemon already carries this child"),
    ("rhaena-targaryen", "aerea-targaryen", "bare disambig page (3 Rhaenas); rhaena-targaryen-daughter-of-aenys-i already carries this child"),
    ("leo-tyrell", "alla-tyrell", "bare disambig page (4 Leos); leo-tyrell-son-of-victor already carries this child"),
    ("leo-tyrell", "leona-tyrell", "same"),
    ("leo-tyrell", "lorent-tyrell", "same"),
    ("leo-tyrell", "lucas-tyrell", "same"),
    ("edric-stark", "argelle-stark", "distinct real person (Jaehaerys I-era Lord); edric-stark-son-of-cregan already carries this child"),
    ("edric-stark", "arrana-stark", "same"),
    ("edric-stark", "cregard-stark", "same"),
    ("benjen-stark", "bennard-stark", "bare = Jon Snow's uncle (no children per wiki); benjen-stark-lord already carries this child"),
    ("rodrik-stark", "branda-stark", "distinct real person (legendary King in the North); rodrik-stark-son-of-beron already carries this child"),
    ("rodrik-stark", "lyarra-stark", "same"),
    ("baelon-targaryen", "daemon-targaryen", "bare disambig page (3 Baelons); baelon-targaryen-son-of-jaehaerys-i already carries this child"),
    ("baelon-targaryen", "viserys-i-targaryen", "same"),
    ("damon-lannister", "damion-lannister", "bare disambig page (2 Damons); damon-lannister-son-of-jason already carries this child"),
    ("jason-lannister", "joanna-lannister", "distinct real person (Warden of the West, different children); jason-lannister-son-of-gerold already carries this child"),
    ("jason-lannister", "stafford-lannister", "same"),
    ("baelor-targaryen", "matarys-targaryen", "bare disambig page (2 Baelors); baelor-targaryen-son-of-daeron-ii already carries this child"),
    ("baelor-targaryen", "valarr-targaryen", "same"),

    # --- WRONG_NAMESAKE confirmed-different, true parent already on variant ---
    ("aerion-targaryen", "aegon-i-targaryen", "Aerion the Monstrous (Dunk & Egg era) != father of Aegon I; aerion-targaryen-son-of-daemion already carries this child"),
    ("aerion-targaryen", "rhaenys-targaryen", "same"),
    ("aerion-targaryen", "visenya-targaryen", "same"),
    ("alys-karstark", "arsa-stark", "bare = Sigorn of Thenn's GoT-era wife; alys-karstark-wife-of-brandon already carries this child"),
    ("alys-karstark", "beron-stark", "same"),
    ("alys-karstark", "rodwell-stark", "same"),
    ("brandon-stark", "arsa-stark", "bare = Ned's brother (d.282 AC, no issue); brandon-stark-son-of-cregan already carries this child"),
    ("brandon-stark", "beron-stark", "same"),
    ("brandon-stark", "rodwell-stark", "same"),
    ("brandon-stark", "lonnel-snow", "same"),
    ("rickon-stark", "cregan-stark", "bare = Ned & Catelyn's son (b.295 AC, no issue); rickon-stark-son-of-benjen already carries this child"),
    ("rickon-stark", "serena-stark", "bare = Ned & Catelyn's son; rickon-stark-son-of-cregan already carries this child"),
    ("rhaenys-targaryen", "laena-velaryon", "bare = Aegon I's queen (Conquest era); rhaenys-targaryen-daughter-of-aemon already carries this child"),
    ("rhaenys-targaryen", "laenor-velaryon", "same"),
    ("elaena-targaryen", "maegon-targaryen", "bare = Aegon III's daughter; elaena-targaryen-daughter-of-gaemon already carries this child"),
    ("luthor-tyrell", "medwick-tyrell", "bare = Mace Tyrell's father (different children); luthor-tyrell-son-of-moryn already carries this child"),
    ("luthor-tyrell", "olene-tyrell", "same"),
    ("luthor-tyrell", "theodore-tyrell", "same"),

    # --- NODE_SPLIT judgement, no reassignment target exists ---
    ("brandon-stark-shipwright", "brandon-stark", "ancient King in the North's unqualified Issue field mis-resolved; true child ('Brandon the Burner') has no node -- plain delete"),
    ("edrick-stark", "brandon-stark", "ancient King's Issue field literally says 'grandfather of Brandon Stark' -- wrong relation AND wrong person; no node for the true grandchild -- plain delete"),
    ("jon-stark", "rickard-stark", "ancient/different-era King in the North namesake; Rickard's real father is edwyle-stark (already present) -- no reassignment target identified"),
    ("aemon-targaryen-son-of-jaehaerys-i", "rhaenys-targaryen", "this is the father of a DIFFERENT Rhaenys; correct edge aemon-targaryen-son-of-jaehaerys-i -> rhaenys-targaryen-daughter-of-aemon already exists -- pure duplicate stray"),

    # --- found while pre-checking the REASSIGN targets below: the correct fact was
    #     ALREADY present at the reassign target, but wired to a bare/wrong-slug source
    #     instead of the disambiguated one. Deleting these avoids the reassign creating
    #     a brand-new duplicate-parent problem on the target node. Each verified via a
    #     direct wiki infobox Father/Mother field fetch (see docstring). ---
    ("aegon-targaryen", "rhaella-targaryen-daughter-of-aegon", "bare dup of the true father fact; Aegon_Targaryen_(son_of_Aenys_I).json is her wiki-confirmed father, reassigned below"),
    ("rhaena-targaryen", "rhaella-targaryen-daughter-of-aegon", "bare dup of the true mother fact; Rhaena_Targaryen_(daughter_of_Aenys_I).json is her wiki-confirmed mother, reassigned below"),
    ("gaemon-targaryen", "elaena-targaryen-daughter-of-gaemon", "bare dup of the true father fact; Gaemon_Targaryen_(son_of_Aenar).json is her wiki-confirmed father, reassigned below"),
    ("benjen-stark", "rickon-stark-son-of-benjen", "bare dup (Jon Snow's uncle) of the true father fact; Benjen_Stark_(lord).json is his wiki-confirmed father, reassigned below"),
    ("rickon-stark", "sansa-stark-daughter-of-rickon", "bare dup (Ned & Catelyn's son) of the true father fact; Rickon_Stark_(son_of_Cregan).json is her wiki-confirmed father, reassigned below"),
]

# ---------------------------------------------------------------------------
# REASSIGNS: (parent_slug, old_child_slug, new_child_slug, reason)
# Each was pre-checked against edges.jsonl to confirm new_child_slug does not already
# carry an edge from parent_slug (would be a silent duplicate) -- the companion DELETE
# rows above remove the pre-existing wrong-slug version of the same fact at the target.
# ---------------------------------------------------------------------------
REASSIGNS = [
    ("gaemon-targaryen-son-of-aenar", "elaena-targaryen", "elaena-targaryen-daughter-of-gaemon",
     "Elaena_Targaryen_(daughter_of_Gaemon).json Father field = Gaemon Targaryen (son of Aenar)"),
    ("aegon-targaryen-son-of-aenys-i", "rhaella-targaryen", "rhaella-targaryen-daughter-of-aegon",
     "Rhaella_Targaryen_(daughter_of_Aegon).json Father field = Aegon Targaryen (son of Aenys I)"),
    ("rhaena-targaryen-daughter-of-aenys-i", "rhaella-targaryen", "rhaella-targaryen-daughter-of-aegon",
     "Rhaella_Targaryen_(daughter_of_Aegon).json Mother field = Rhaena Targaryen (daughter of Aenys I)"),
    ("benjen-stark-lord", "rickon-stark", "rickon-stark-son-of-benjen",
     "Rickon_Stark_(son_of_Benjen).json Father field = Benjen Stark (lord)"),
    ("rickon-stark-son-of-cregan", "sansa-stark", "sansa-stark-daughter-of-rickon",
     "Sansa_Stark_(daughter_of_Rickon).json Father field = Rickon Stark (son of Cregan)"),
]

# Nodes this script touches that are EXPECTED to still exceed 2 parents afterwards
# (legit special cases -- not a bug).
EXPECTED_OVER_2 = {"joffrey-baratheon": 3}


def load_edges():
    rows = []
    with EDGES.open(encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s:
                rows.append(json.loads(s))
    return rows


def parent_of_snapshot(rows):
    by_child = defaultdict(set)
    for e in rows:
        if e.get("edge_type") == "PARENT_OF":
            by_child[e["target_slug"]].add(e["source_slug"])
    return by_child


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write edges.jsonl + delete retired node files (default: dry run)")
    args = ap.parse_args()

    rows = load_edges()
    before = parent_of_snapshot(rows)

    merge_map = {retired: survivor for retired, survivor, _, _ in MERGES}
    delete_set = {(p, c) for p, c, _ in DELETES}
    reassign_map = {}  # (parent, old_child) -> new_child
    for p, old_c, new_c, _ in REASSIGNS:
        reassign_map[(p, old_c)] = new_c

    # pass 1: apply merge/delete/reassign per-row, recording whether each surviving
    # row was TOUCHED (its key changed, or it was newly created by a rewrite).
    transformed = []  # list of (key, touched, row)
    stats = Counter()
    for e in rows:
        src, tgt, et = e.get("source_slug"), e.get("target_slug"), e.get("edge_type")
        touched = False

        # 1. merges apply to every edge type, either side
        if src in merge_map:
            e = dict(e); e["source_slug"] = merge_map[src]; src = e["source_slug"]
            stats["merge_rewrite"] += 1
            touched = True
        if tgt in merge_map:
            e = dict(e); e["target_slug"] = merge_map[tgt]; tgt = e["target_slug"]
            stats["merge_rewrite"] += 1
            touched = True

        # 2. deletes only meaningful for PARENT_OF (this cleanup's scope)
        if et == "PARENT_OF" and (src, tgt) in delete_set:
            stats["deleted"] += 1
            continue

        # 3. reassigns (PARENT_OF only)
        if et == "PARENT_OF" and (src, tgt) in reassign_map:
            e = dict(e); e["target_slug"] = reassign_map[(src, tgt)]; tgt = e["target_slug"]
            stats["reassigned"] += 1
            touched = True

        transformed.append(((src, tgt, et), touched, e))

    # pass 2: group by key (order-independent, unlike a single streaming pass). A key
    # with >1 row is dropped down to ONE only if at least one copy was touched by this
    # script -- an exact duplicate where EVERY copy is untouched predates this cleanup
    # and is out of scope (a separate, unreviewed global-dedup action). Prefer keeping
    # an untouched copy (the pre-existing edge) over a touched one when both exist.
    by_key = defaultdict(list)
    for key, touched, e in transformed:
        by_key[key].append((touched, e))

    new_rows = []
    for key, group in by_key.items():
        if len(group) == 1:
            new_rows.append(group[0][1])
            continue
        any_touched = any(t for t, _ in group)
        if not any_touched:
            new_rows.extend(e for _, e in group)  # pre-existing dup, untouched -- leave alone
            continue
        untouched = [e for t, e in group if not t]
        keeper = untouched[0] if untouched else group[0][1]
        new_rows.append(keeper)
        stats["post_rewrite_dup_dropped"] += len(group) - 1

    after = parent_of_snapshot(new_rows)

    print("Action counts:")
    print(f"  merges applied (retired slugs)     : {len(MERGES)}")
    print(f"  edge rows rewritten by merge        : {stats['merge_rewrite']}")
    print(f"  deletes applied                     : {stats['deleted']} (expected {len(DELETES)})")
    print(f"  reassigns applied                   : {stats['reassigned']} (expected {len(REASSIGNS)})")
    print(f"  post-rewrite exact-dup dropped       : {stats['post_rewrite_dup_dropped']}")
    print(f"  total edge rows: {len(rows)} -> {len(new_rows)}")

    if stats["deleted"] != len(DELETES):
        print(f"\nABORT: matched {stats['deleted']} delete rows, expected {len(DELETES)}.", file=sys.stderr)
        matched = Counter()
        for e in rows:
            if e.get("edge_type") == "PARENT_OF" and (e["source_slug"], e["target_slug"]) in delete_set:
                matched[(e["source_slug"], e["target_slug"])] += 1
        for p, c, _ in DELETES:
            if matched[(p, c)] != 1:
                print(f"  delete pair ({p} -> {c}) matched {matched[(p, c)]} rows", file=sys.stderr)
        sys.exit(1)

    if stats["reassigned"] != len(REASSIGNS):
        print(f"\nABORT: matched {stats['reassigned']} reassign rows, expected {len(REASSIGNS)}.", file=sys.stderr)
        sys.exit(1)

    # ---- verify every touched child ends with <=2 distinct parents (or EXPECTED_OVER_2) ----
    touched_children = {c for _, c, _ in DELETES} | {c for _, c, _, _ in REASSIGNS} | {nc for _, _, nc, _ in REASSIGNS}
    print("\nPer-child parent-count check (touched nodes):")
    bad = []
    for child in sorted(touched_children):
        n_before = len(before.get(child, set()))
        n_after = len(after.get(child, set()))
        expected_max = EXPECTED_OVER_2.get(child, 2)
        flag = "OK" if n_after <= expected_max else "STILL >2 -- REVIEW"
        if n_after > expected_max:
            bad.append(child)
        print(f"  {child:35s} parents {n_before} -> {n_after}  [{flag}]  {sorted(after.get(child, set()))}")

    if bad:
        print(f"\nABORT: {len(bad)} node(s) still exceed expected parent count after fixes. No write.", file=sys.stderr)
        sys.exit(1)

    if not args.apply:
        print("\nDRY RUN -- no files written. Re-run with --apply to commit.")
        return

    EDGES.write_text("".join(json.dumps(e) + "\n" for e in new_rows), encoding="utf-8")
    print(f"\nWROTE {EDGES.relative_to(REPO)} -- {len(new_rows)} rows.")

    # ---- merge-alias + retired-node-file cleanup ----
    for retired, survivor, natural_name, skip_alias in MERGES:
        survivor_path = NODES_CHAR_DIR / f"{survivor}.node.md"
        if not skip_alias and survivor_path.exists():
            text = survivor_path.read_text(encoding="utf-8")
            if f'"{natural_name}"' not in text and natural_name not in text.split("aliases:", 1)[-1].split("\n", 1)[0]:
                text = text.replace("aliases: []", f'aliases: ["{natural_name}"]', 1)
                survivor_path.write_text(text, encoding="utf-8")
                print(f"  added alias {natural_name!r} to {survivor_path.relative_to(REPO)}")
        elif skip_alias:
            print(f"  SKIPPED alias add for retired {retired!r} (ambiguous bare name, see docstring)")
        retired_path = NODES_CHAR_DIR / f"{retired}.node.md"
        if retired_path.exists():
            retired_path.unlink()
            print(f"  deleted retired node file {retired_path.relative_to(REPO)}")

    print("\nNext: rebuild bundle (build-chat-export.py) + regenerate alias resolver "
          "(event_alias_resolver.py) + indexes (weirwood refresh).")


if __name__ == "__main__":
    main()
