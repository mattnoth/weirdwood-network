#!/usr/bin/env python3
"""
audit-parent-conflation.py  —  READ-ONLY diagnostic for the parentage layer.

Every real person has <=2 biological parents. 89 of 1,015 parented nodes in the
graph carry >2 PARENT_OF parents. This script classifies each incoming PARENT_OF
edge on those nodes so a reviewer (Matt / a fleet pass) can approve deletions by
POLICY, not edge-by-edge.

COLD-READ FINDING (S179): the ">2 parents" signal decomposes into THREE causes,
not the two the S178 audit doc named. The dominant SUSPECT cause is a *duplicate
parent NODE* (one real parent under two slugs — maiden vs married name, bare vs
disambiguated, the "two Aerions"), NOT "spurious edges on a single person".

Edge classes emitted (per PARENT_OF edge into a >2-parent node):

  REDUNDANT_CHILD_STUB
      C is a bare-name node AND a disambiguated variant `C-...` exists that
      ALREADY carries this same parent P. The fact belongs on the variant; the
      edge into the bare bucket double-counts. Action: delete edge P->C.
      Confidence HIGH (mechanical, delete-only, the good node already has it).

  DUPLICATE_PARENT_NODE
      Another parent of C shares this parent's identity (slug prefix or same
      first-name token — two parents of one child sharing a first name are
      almost certainly one person double-noded). The child's true parent COUNT
      is fine; one parent is represented twice. Action: merge the duplicate
      parent nodes (cross-identity) / collapse the non-canonical edge.
      Confidence MEDIUM — routed to agentic review to CONFIRM same-person and
      pick the canonical slug (some pairs are both 0-quote stubs).

  GENUINE_EXTRA_PARENT
      Residual parent with no variant match and no duplicate-sibling. A real
      extra/wrong edge (a different-era namesake wired as a parent, a
      grandparent mislabeled, or a legit special case like Joffrey's
      presumed-vs-biological father). Action: agentic review -> keep / prune /
      reassign-to-slug. Confidence LOW.

  KEEP
      One of the (<=2) parents that survive after the above. No action.

Outputs (NO mutation):
  working/graph-cleanup/parent-edge-proposal.jsonl   (one row per edge)
  working/graph-cleanup/parent-node-summary.jsonl    (one row per >2-parent node)
  printed summary table

Run:  python3 scripts/audit-parent-conflation.py
"""
import json, collections, os, sys

EDGES = "graph/edges/edges.jsonl"
NODES = "web/data/nodes.json"
OUT_DIR = "working/graph-cleanup"
EDGE_OUT = os.path.join(OUT_DIR, "parent-edge-proposal.jsonl")
NODE_OUT = os.path.join(OUT_DIR, "parent-node-summary.jsonl")

# tokens that don't identify a person (titles, roles, ordinals, connectors)
STOP = {"lord", "lady", "ser", "king", "queen", "prince", "princess", "of", "the",
        "wife", "son", "daughter", "father", "mother", "brother", "sister",
        "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"}


def name_tokens(slug):
    return [t for t in slug.split("-") if t not in STOP and not t.isdigit()]


def first_token(slug):
    ts = name_tokens(slug)
    return ts[0] if ts else slug


def same_person(a, b):
    """Two parent slugs of the SAME child that look like one person double-noded."""
    if a == b:
        return True
    if a.startswith(b + "-") or b.startswith(a + "-"):
        return True
    # two parents of one child sharing the first name are almost certainly a
    # maiden/married or bare/disambiguated duplicate of a single person.
    return first_token(a) == first_token(b)


DISAMBIG_MARKERS = ("-son-of-", "-daughter-of-", "-the-")


def is_disambiguated(slug):
    """A slug that names a specific person to disambiguate a shared name."""
    if any(m in slug for m in DISAMBIG_MARKERS):
        return True
    return len(slug.split("-")) >= 4


def load():
    parents = collections.defaultdict(list)   # child -> [edge dicts]
    dup_edges = 0                               # exact (src,tgt,type) repeats
    seen = set()
    with open(EDGES) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            if e.get("edge_type") == "PARENT_OF":
                key = (e["source_slug"], e["target_slug"], e["edge_type"])
                if key in seen:
                    dup_edges += 1          # 4th failure mode: exact-dup edge
                    e["_exact_dup"] = True
                seen.add(key)
                parents[e["target_slug"]].append(e)
    nodes = json.load(open(NODES))
    return parents, nodes, dup_edges


def qc(nodes, slug):
    n = nodes.get(slug)
    return len(n.get("quotes", [])) if n else -1  # -1 == node absent


def is_house(nodes, slug):
    """Parent slug is really a House node, not a person (e.g. `sunderly`)."""
    return f"house-{slug}" in nodes


def main():
    parents, nodes, dup_edges = load()
    all_children = set(parents)

    def variants(base):
        return [s for s in all_children if s.startswith(base + "-")]

    over = {c: ps for c, ps in parents.items() if len(ps) > 2}
    os.makedirs(OUT_DIR, exist_ok=True)

    edge_rows = []
    node_rows = []
    class_ct = collections.Counter()

    for child in sorted(over):
        pedges = over[child]
        # parents that a disambiguated variant of this child already carries
        variant_parents = set()
        for v in variants(child):
            for pe in parents[v]:
                variant_parents.add(pe["source_slug"])

        residual = []
        seen_keys = set()
        for pe in pedges:
            p = pe["source_slug"]
            # (0) 4th mode: exact-duplicate PARENT_OF edge -> delete the repeat
            key = (p, child)
            if key in seen_keys:
                edge_rows.append(mkrow(child, pe, "EXACT_DUP_EDGE",
                                       f"delete duplicate edge {p}->{child}", "high", nodes,
                                       note="exact (src,tgt) repeat"))
                class_ct["EXACT_DUP_EDGE"] += 1
                continue
            seen_keys.add(key)
            # (1) redundant onto bare child stub -> variant carries it
            if p in variant_parents:
                edge_rows.append(mkrow(child, pe, "REDUNDANT_CHILD_STUB",
                                       f"delete edge {p}->{child} (carried by a disambiguated variant)",
                                       "high", nodes, note=""))
                class_ct["REDUNDANT_CHILD_STUB"] += 1
            else:
                residual.append(pe)

        # cluster residual parents into person-groups by name heuristic
        clusters = []
        for pe in residual:
            p = pe["source_slug"]
            placed = False
            for cl in clusters:
                if any(same_person(p, q["source_slug"]) for q in cl):
                    cl.append(pe); placed = True; break
            if not placed:
                clusters.append([pe])

        distinct_people = len(clusters)
        node_split = distinct_people > 2   # conflation bucket: >2 real parent-people

        for cl in clusters:
            # (2) house-node-as-parent: a House slug is not a person -> delete edge
            house_members = [pe for pe in cl if is_house(nodes, pe["source_slug"])]
            person_members = [pe for pe in cl if not is_house(nodes, pe["source_slug"])]
            for pe in house_members:
                edge_rows.append(mkrow(child, pe, "HOUSE_AS_PARENT",
                                       f"delete edge {pe['source_slug']}->{child} (House node, not a person)",
                                       "high", nodes, note="parent slug resolves to a House node"))
                class_ct["HOUSE_AS_PARENT"] += 1

            if not person_members:
                continue
            if len(person_members) == 1:
                pe = person_members[0]
                if node_split:
                    edge_rows.append(mkrow(child, pe, "NODE_SPLIT",
                                           f"REVIEW: {child} is a conflation bucket; split before deciding {pe['source_slug']}",
                                           "low", nodes, note="child accretes parents of >2 distinct people"))
                    class_ct["NODE_SPLIT"] += 1
                else:
                    edge_rows.append(mkrow(child, pe, "KEEP", "keep (<=2 true parents)", "high", nodes, note=""))
                    class_ct["KEEP"] += 1
                continue

            # (3) multi-member person cluster = duplicate parent node OR wrong namesake
            top = max(person_members, key=lambda pe: (qc(nodes, pe["source_slug"]), len(pe["source_slug"])))
            top_slug = top["source_slug"]
            sibling_disambig = any(is_disambiguated(pe["source_slug"]) for pe in person_members
                                   if pe["source_slug"] != top_slug)
            # GUARD (the two-Aerions failure): if the highest-qc member is a BARE slug but a
            # sibling is a disambiguated variant, they are likely DIFFERENT people. Never merge.
            if not is_disambiguated(top_slug) and sibling_disambig and qc(nodes, top_slug) > 0:
                for pe in cl:
                    edge_rows.append(mkrow(child, pe, "WRONG_NAMESAKE",
                                           f"REVIEW: bare '{top_slug}' (qc{qc(nodes,top_slug)}) collides with a "
                                           f"disambiguated variant — likely different people, do NOT merge",
                                           "low", nodes, note="bare high-qc namesake vs variant; wiki disambig boundary risk"))
                    class_ct["WRONG_NAMESAKE"] += 1
                continue
            # canonical: prefer a disambiguated variant over a bare slug (NOT raw qc)
            disambig_members = [pe for pe in person_members if is_disambiguated(pe["source_slug"])]
            pool = disambig_members or person_members
            canonical = max(pool, key=lambda pe: (qc(nodes, pe["source_slug"]), len(pe["source_slug"])))["source_slug"]
            for pe in person_members:
                p = pe["source_slug"]
                if p == canonical:
                    edge_rows.append(mkrow(child, pe, "KEEP", "keep (canonical of dup-parent cluster)",
                                           "high", nodes, note="dup-cluster canonical"))
                    class_ct["KEEP"] += 1
                else:
                    edge_rows.append(mkrow(child, pe, "DUPLICATE_PARENT_NODE",
                                           f"merge parent node {p} -> {canonical} (same person, dup node); collapse edge",
                                           "medium", nodes,
                                           note=f"dup of {canonical} (qc {qc(nodes,p)} vs {qc(nodes,canonical)})"))
                    class_ct["DUPLICATE_PARENT_NODE"] += 1

        node_rows.append({
            "child": child,
            "child_qc": qc(nodes, child),
            "n_parents": len(pedges),
            "n_redundant_stub": sum(1 for pe in pedges if pe["source_slug"] in variant_parents),
            "distinct_people_after_dedup": distinct_people,
            "conflation_bucket": node_split,
            "parents": [pe["source_slug"] for pe in pedges],
        })

    with open(EDGE_OUT, "w") as f:
        for r in edge_rows:
            f.write(json.dumps(r) + "\n")
    with open(NODE_OUT, "w") as f:
        for r in node_rows:
            f.write(json.dumps(r) + "\n")

    # ---- summary ----
    print(f"\n>2-parent nodes analyzed: {len(over)}")
    print(f"PARENT_OF edges into them: {sum(len(v) for v in over.values())}")
    print(f"(exact-duplicate PARENT_OF edges seen corpus-wide: {dup_edges})\n")
    AUTO = ["EXACT_DUP_EDGE", "REDUNDANT_CHILD_STUB", "HOUSE_AS_PARENT"]
    REVIEW = ["DUPLICATE_PARENT_NODE", "WRONG_NAMESAKE", "NODE_SPLIT"]
    print("AUTO-APPLY candidates (deterministic, delete-only, review-cleared class shapes):")
    for cls in AUTO:
        print(f"  {cls:24s} {class_ct[cls]}")
    print("REVIEW-REQUIRED (per-pair same-person confirm or node-split judgement):")
    for cls in REVIEW:
        print(f"  {cls:24s} {class_ct[cls]}")
    print(f"  {'KEEP':24s} {class_ct['KEEP']}")

    buckets = [r for r in node_rows if r["conflation_bucket"]]
    print(f"\nconflation-bucket nodes (need node-split track, NOT edge-prune): {len(buckets)}")
    for r in sorted(buckets, key=lambda x: -x["distinct_people_after_dedup"]):
        print(f"    {r['child']:28s} qc={r['child_qc']:3d}  distinct-people={r['distinct_people_after_dedup']}")

    print(f"\nwrote {EDGE_OUT}  ({len(edge_rows)} edge rows)")
    print(f"wrote {NODE_OUT}  ({len(node_rows)} node rows)")
    print("\nNO mutation performed. Review before applying.")


def mkrow(child, pe, cls, action, conf, nodes, note):
    p = pe["source_slug"]
    return {
        "child": child,
        "child_qc": qc(nodes, child),
        "parent": p,
        "parent_qc": qc(nodes, p),
        "parent_node_missing": nodes.get(p) is None,
        "edge_class": cls,
        "proposed_action": action,
        "confidence": conf,
        "evidence_kind": pe.get("evidence_kind"),
        "evidence_ref": pe.get("evidence_ref"),
        "evidence_quote": (pe.get("evidence_quote") or "")[:200],
        "note": note,
    }


if __name__ == "__main__":
    main()
