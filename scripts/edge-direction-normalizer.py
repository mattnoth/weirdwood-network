#!/usr/bin/env python3
"""
edge-direction-normalizer.py

Deterministic head-direction normalizer for graph/edges/edges.jsonl.

The python-map typer anchored source_slug on the grammatical subject of the
Pass-1 sentence, producing inverted edges. Rows self-witness this bug via the
asserted_relation / hint_raw fields (e.g. a KILLS row with asserted_relation
"Killed by" means the source was the victim, not the killer).

This script:
  1. Reads graph/edges/edges.jsonl (3,811 rows).
  2. Tests each row's asserted_relation + hint_raw using edge-type-aware
     reverse-signal logic. Edge-type semantics govern whether a passive
     phrase indicates an inversion or is simply describing the relationship
     from the source's perspective.
  3. On a confirmed reverse signal: swaps source_slug <-> target_slug plus
     any direction-bearing resolution/label fields, records the flip.
  4. On ambiguous (both forward and reverse signals, or contradicting edge
     type): writes to flagged-for-review.jsonl with a reason field.
  5. On no signal: keeps untouched (conservative default).
  6. Outputs THREE files to working/edge-modeling/ (NOT graph/):
       normalizer-candidates.jsonl  -- full rewritten set, one row per original
       normalizer-diff.md           -- human-readable before/after diff
       flagged-for-review.jsonl     -- rows needing manual review

The script does NOT modify graph/edges/edges.jsonl. That merge is Plate 5.

Edge-type semantics (critical to avoid false positives):
  - AGENT-POSITIVE types (KILLS, BETRAYS, ATTACKS, RESCUES, HEALS, TUTORS,
    CAPTURES, EXECUTES, POISONS, SACRIFICES, TORTURES, DECEIVES, MANIPULATES,
    BESTOWS_KNIGHTHOOD_ON): source is the ACTOR. A passive phrase ("killed by",
    "rescued by") in asserted_relation means source is the PATIENT — flip.
  - AUTHORITY-FLOW types (COMMANDS, SERVES, GUARDS): source flows authority
    TO target (commander→subordinate, server→served). "is served by" or
    "commanded by" in asserted_relation means source is the recipient of
    the authority flow — flip.
  - EXPERIENCE/STATE types (RESENTS, FEARS, DISTRUSTS, PRISONER_OF,
    MOURNS, LOVES, HATES, TRUSTS, RESPECTS, COMPANION_OF): source is the
    EXPERIENCER. Passive phrases in asserted_relation often describe the
    CAUSE or CONTEXT of the experience — NOT evidence of inversion.
    Do NOT apply passive-flip logic to these types.

Usage:
    python3 scripts/edge-direction-normalizer.py [--edges PATH] [--out-dir PATH]

Defaults:
    --edges  graph/edges/edges.jsonl
    --out-dir working/edge-modeling
"""

import argparse
import json
import re
from pathlib import Path
from collections import defaultdict


# ---------------------------------------------------------------------------
# Edge-type semantic categories
# ---------------------------------------------------------------------------

# AGENT-POSITIVE: source is the actor/agent. A passive "by" phrase signals
# that the row is inverted (source was actually the patient in the extraction).
AGENT_POSITIVE_TYPES = {
    "KILLS", "BETRAYS", "ATTACKS", "RESCUES", "HEALS", "TUTORS", "TEACHES",
    "CAPTURES", "EXECUTES", "POISONS", "SACRIFICES", "TORTURES", "DECEIVES",
    "MANIPULATES", "BESTOWS_KNIGHTHOOD_ON", "ASSAULTS", "KNIGHTED_BY",
    "APPOINTS", "DEPOSES", "BANISHES", "IMPRISONS",
}

# AUTHORITY-FLOW: COMMANDS semantics = source is the commander (authority holder),
# target is the subordinate. "Served by" in asserted_relation is consistent with
# source being the commander — it does NOT signal an inversion.
# SERVES semantics = source is the server, target is the served. "Summoned by"
# in SERVES means source was summoned by target — that IS a potential inversion,
# but we handle it in the catch-all branch rather than here since the
# asserted_relation rarely inverts COMMANDS/SERVES in practice.
# AUTHORITY_FLOW_TYPES is retained as a no-op category to document the decision.
AUTHORITY_FLOW_TYPES: set = set()  # No special-casing needed; fall through to catch-all

# EXPERIENCE/STATE: source is the experiencer; passive phrases describe the
# cause/origin of the experience, NOT a direction inversion. Never flip these
# on passive signals alone.
EXPERIENCE_STATE_TYPES = {
    "RESENTS", "FEARS", "DISTRUSTS", "PRISONER_OF", "MOURNS", "LOVES",
    "HATES", "TRUSTS", "RESPECTS", "COMPANION_OF", "PERCEIVED_AS",
    "SEEKS", "INVESTIGATES",
    # DECEIVED_BY: source=deceived, target=deceiver. "betrayed by" in
    # asserted_relation describes the deceived party's experience —
    # direction is already correct; do NOT flip.
    "DECEIVED_BY",
    # SERVES: source serves target. "Summoned by / knighted by" in
    # asserted_relation describes how the service began — NOT an inversion.
    # Example: "Jon was summoned by Stannis" explains WHY jon serves stannis,
    # consistent with jon→stannis SERVES being correct.
    "SERVES",
    # COMMANDS: source commands target. "Served by" describes source receiving
    # service, consistent with source being the commander. NOT an inversion.
    "COMMANDS",
}

# RESCUE-specific: RESCUES semantics — rescuer → rescued.
# "rescued by" in asserted_relation means source was rescued BY target = inverted.
# (Handled under AGENT_POSITIVE_TYPES above.)

# ---------------------------------------------------------------------------
# Reverse-signal patterns, grouped by the types they apply to
# ---------------------------------------------------------------------------

# Universal passive "by" reverse signals — apply to AGENT_POSITIVE_TYPES
PASSIVE_BY_PATTERNS = [
    (re.compile(r'\bkilled?\s+by\b'), "passive: killed by"),
    (re.compile(r'\bmurdered?\s+by\b'), "passive: murdered by"),
    (re.compile(r'\bslain\s+by\b'), "passive: slain by"),
    (re.compile(r'\bbetrayed?\s+by\b'), "passive: betrayed by"),
    (re.compile(r'\bcaptured?\s+by\b'), "passive: captured by"),
    (re.compile(r'\battacked?\s+by\b'), "passive: attacked by"),
    (re.compile(r'\bdefeated?\s+by\b'), "passive: defeated by"),
    (re.compile(r'\btortured?\s+by\b'), "passive: tortured by"),
    (re.compile(r'\bsaved?\s+by\b'), "passive: saved by"),
    (re.compile(r'\brescued?\s+by\b'), "passive: rescued by"),
    (re.compile(r'\bteaches?d?\s+by\b|\btaught\s+by\b'), "passive: taught by"),
    (re.compile(r'\bmentored?\s+by\b'), "passive: mentored by"),
    (re.compile(r'\bknighted?\s+by\b'), "passive: knighted by"),
    (re.compile(r'\btrained?\s+by\b'), "passive: trained by"),
    (re.compile(r'\braised?\s+by\b'), "passive: raised by"),
    (re.compile(r'\bbeaten?\s+by\b'), "passive: beaten by"),
    (re.compile(r'\bterrorized?\s+by\b'), "passive: terrorized by"),
    (re.compile(r'\benslave[d]?\s+by\b'), "passive: enslaved by"),
    (re.compile(r'\bcoerced?\s+by\b'), "passive: coerced by"),
    (re.compile(r'\btreated?\s+by\b'), "passive: treated by"),
    (re.compile(r'\bsummoned?\s+by\b'), "passive: summoned by"),
    (re.compile(r'\bhunted?\s+by\b'), "passive: hunted by"),
    (re.compile(r'\bcontrolled?\s+by\b'), "passive: controlled by"),
    # Role-noun patient: "captor-dependent" signals source is the captive,
    # not the captor. Specific to CAPTURES edges.
    (re.compile(r'\bcaptor[- ]dependent\b'), "role-noun patient: captor-dependent"),
]

# Authority-flow-specific patterns — apply to AUTHORITY_FLOW_TYPES (COMMANDS, SERVES)
AUTHORITY_REVERSE_PATTERNS = [
    (re.compile(r'\bserved?\s+by\b'), "authority-reverse: served by"),
    (re.compile(r'\bis\s+served?\s+by\b'), "authority-reverse: is served by"),
]

# Forward signals (used for ambiguity detection in AGENT_POSITIVE_TYPES only)
FORWARD_PATTERNS = [
    re.compile(r'\bkills?\b'),
    re.compile(r'\bbetray[s]?\b'),
    re.compile(r'\bcaptures?\b'),
    re.compile(r'\battacks?\b'),
    re.compile(r'\bdefeats?\b'),
    re.compile(r'\brescues?\b'),
    re.compile(r'\bmentors?\b'),
    re.compile(r'\bknights?\b'),
]

# Known-symmetric types — never flip regardless of what asserted_relation says.
SYMMETRIC_TYPES = {
    "SIBLING_OF", "SPOUSE_OF", "BETROTHED_TO", "LOVER_OF", "ALLIES_WITH",
    "OPPOSES", "DUELS", "BONDED_TO", "CONSPIRES_WITH", "NEGOTIATES_WITH",
    "CONTEMPORARY_WITH", "COMPANION_OF", "SAME_AS", "COUSIN_OF",
    "MILK_BROTHER_OF", "TRAVELS_WITH", "PARALLELS", "CONTRASTS", "ECHOES",
    "PRISONER_EXCHANGE_FOR", "IN_LAW_OF", "ENCOUNTERS",
}

# ---------------------------------------------------------------------------
# Direction-bearing fields that must be swapped along with source/target
# ---------------------------------------------------------------------------
SOURCE_FIELDS = [
    "source_slug",
    "source_label",
    "source_resolution_status",
    "source_set",
]
TARGET_FIELDS = [
    "target_slug",
    "target_label",
    "target_resolution_status",
    "target_set",
]
SWAP_PAIRS = list(zip(SOURCE_FIELDS, TARGET_FIELDS))


# ---------------------------------------------------------------------------
# Core decision function
# ---------------------------------------------------------------------------

def classify_row(row: dict) -> tuple[str, str]:
    """
    Returns (action, reason) where action is:
      "kept"    -- no reverse signal; leave as-is (conservative default)
      "flipped" -- confirmed reverse signal; swap source <-> target
      "flagged" -- ambiguous; needs human review
    """
    edge_type = row.get("edge_type", "")

    # Symmetric types: never flip
    if edge_type in SYMMETRIC_TYPES:
        return ("kept", "symmetric edge type")

    ar = row.get("asserted_relation", "") or ""
    hr = row.get("hint_raw", "") or ""
    combined = (ar + " " + hr).lower().strip()

    # --- EXPERIENCE/STATE types: do NOT flip on passive patterns ---
    # For these types, passive phrases describe the cause/context of the
    # experience from the source's perspective, not a direction inversion.
    if edge_type in EXPERIENCE_STATE_TYPES:
        return ("kept", f"experience/state type — passive phrases do not indicate inversion")

    # --- AUTHORITY-FLOW types: flip only on authority-specific reverse patterns ---
    if edge_type in AUTHORITY_FLOW_TYPES:
        auth_reverse = []
        for pat, label in AUTHORITY_REVERSE_PATTERNS:
            if pat.search(combined):
                auth_reverse.append(label)
        if auth_reverse:
            # Check for forward signals too (ambiguity)
            fwd = [p.pattern for p in FORWARD_PATTERNS if p.search(combined)]
            if fwd:
                reason = (
                    f"ambiguous: authority-reverse signals [{'; '.join(auth_reverse)}] "
                    f"and forward signals [{'; '.join(fwd)}] both fired"
                )
                return ("flagged", reason)
            return ("flipped", f"reverse signal: {'; '.join(auth_reverse)}")
        return ("kept", "no authority-reverse signal")

    # --- AGENT-POSITIVE types: flip on passive "by" patterns ---
    if edge_type in AGENT_POSITIVE_TYPES:
        rev_signals = []
        for pat, label in PASSIVE_BY_PATTERNS:
            if pat.search(combined):
                rev_signals.append(label)

        if not rev_signals:
            return ("kept", "no reverse signal detected")

        # Check for forward signals (ambiguity)
        fwd = [p.pattern for p in FORWARD_PATTERNS if p.search(combined)]
        if fwd:
            reason = (
                f"ambiguous: reverse signals [{'; '.join(rev_signals)}] "
                f"and forward signals [{'; '.join(fwd)}] both fired"
            )
            return ("flagged", reason)

        return ("flipped", f"reverse signal: {'; '.join(rev_signals)}")

    # --- All other types: conservative default ---
    # Only flip if there's a clear passive-by signal AND the edge type is
    # directional by design. If the type isn't in any of the above categories,
    # apply the same AGENT_POSITIVE logic as a catch-all.
    rev_signals = []
    for pat, label in PASSIVE_BY_PATTERNS:
        if pat.search(combined):
            rev_signals.append(label)

    if not rev_signals:
        return ("kept", "no reverse signal (other edge type)")

    # Also check authority-flow reverse patterns for catch-all
    for pat, label in AUTHORITY_REVERSE_PATTERNS:
        if pat.search(combined):
            rev_signals.append(label)

    fwd = [p.pattern for p in FORWARD_PATTERNS if p.search(combined)]
    if fwd:
        reason = (
            f"ambiguous (other type {edge_type}): reverse signals [{'; '.join(rev_signals)}] "
            f"and forward signals [{'; '.join(fwd)}] both fired"
        )
        return ("flagged", reason)

    return ("flipped", f"reverse signal (other type {edge_type}): {'; '.join(rev_signals)}")


def swap_fields(row: dict) -> dict:
    """Swap source and target fields and return a new dict."""
    new_row = dict(row)
    for src_field, tgt_field in SWAP_PAIRS:
        src_val = row.get(src_field)
        tgt_val = row.get(tgt_field)
        if src_val is not None or tgt_val is not None:
            if src_val is not None:
                new_row[tgt_field] = src_val
            elif tgt_field in new_row:
                del new_row[tgt_field]
            if tgt_val is not None:
                new_row[src_field] = tgt_val
            elif src_field in new_row:
                del new_row[src_field]
    return new_row


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--edges",
        default="graph/edges/edges.jsonl",
        help="Path to input edges.jsonl (default: graph/edges/edges.jsonl)",
    )
    parser.add_argument(
        "--out-dir",
        default="working/edge-modeling",
        help="Output directory (default: working/edge-modeling)",
    )
    args = parser.parse_args()

    edges_path = Path(args.edges)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    candidates_path = out_dir / "normalizer-candidates.jsonl"
    diff_path = out_dir / "normalizer-diff.md"
    flagged_path = out_dir / "flagged-for-review.jsonl"

    # --- Read input ---
    rows = []
    with edges_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    print(f"Read {len(rows)} rows from {edges_path}")

    # --- Classify and process ---
    counts = {"flipped": 0, "kept": 0, "flagged": 0}
    flipped_by_type: dict[str, int] = defaultdict(int)
    flagged_rows = []
    candidate_rows = []
    diff_sections = []

    for row in rows:
        action, reason = classify_row(row)

        if action == "flipped":
            new_row = swap_fields(row)
            new_row["normalizer_action"] = "flipped"
            new_row["normalizer_reason"] = reason
            candidate_rows.append(new_row)
            counts["flipped"] += 1
            flipped_by_type[row.get("edge_type", "UNKNOWN")] += 1

            diff_sections.append(
                f"### {row.get('edge_type', '?')} — "
                f"{row.get('source_slug', '?')} → {row.get('target_slug', '?')}\n"
                f"- **BEFORE:** `{row.get('source_slug')}` → `{row.get('target_slug')}` "
                f"(`{row.get('asserted_relation', '')}`)  \n"
                f"- **AFTER :** `{new_row.get('source_slug')}` → `{new_row.get('target_slug')}`  \n"
                f"- **Signal:** {reason}  \n"
            )

        elif action == "flagged":
            new_row = dict(row)
            new_row["normalizer_action"] = "flagged"
            new_row["normalizer_reason"] = reason
            candidate_rows.append(new_row)
            flagged_rows.append(new_row)
            counts["flagged"] += 1

        else:  # kept
            new_row = dict(row)
            new_row["normalizer_action"] = "kept"
            new_row["normalizer_reason"] = reason
            candidate_rows.append(new_row)
            counts["kept"] += 1

    # --- Write candidates ---
    with candidates_path.open("w", encoding="utf-8") as f:
        for r in candidate_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {len(candidate_rows)} rows to {candidates_path}")

    # --- Write flagged ---
    with flagged_path.open("w", encoding="utf-8") as f:
        for r in flagged_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {len(flagged_rows)} flagged rows to {flagged_path}")

    # --- Verification probes ---
    probes = [
        {
            "label": "cressen → melisandre KILLS (asserted: 'Killed by')",
            "expected_after_source": "melisandre",
            "expected_after_target": "cressen",
            "edge_type": "KILLS",
            "orig_source": "cressen",
            "orig_target": "melisandre",
        },
        {
            "label": "arya → sandor CAPTURES (asserted: 'Conflicted captor-dependent relationship')",
            "expected_after_source": "sandor-clegane",
            "expected_after_target": "arya-stark",
            "edge_type": "CAPTURES",
            "orig_source": "arya-stark",
            "orig_target": "sandor-clegane",
        },
        {
            "label": "tyrion → shae BETRAYS (asserted: 'Betrayed by (former lover)')",
            "expected_after_source": "shae",
            "expected_after_target": "tyrion-lannister",
            "edge_type": "BETRAYS",
            "orig_source": "tyrion-lannister",
            "orig_target": "shae",
        },
    ]

    probe_results = []
    for probe in probes:
        matched = [
            c for c in candidate_rows
            if c.get("edge_type") == probe["edge_type"]
            and c.get("normalizer_action") == "flipped"
            and c.get("source_slug") == probe["expected_after_source"]
            and c.get("target_slug") == probe["expected_after_target"]
        ]
        flipped_match = bool(matched)
        probe_results.append((probe["label"], flipped_match))

    # --- Write diff ---
    top_flipped = sorted(flipped_by_type.items(), key=lambda x: -x[1])
    with diff_path.open("w", encoding="utf-8") as f:
        f.write("# Edge Direction Normalizer — Diff Report\n\n")
        f.write(f"Input: `{edges_path}` ({len(rows)} rows)  \n")
        f.write(f"Output: `{candidates_path}`  \n\n")

        f.write("## Summary\n\n")
        f.write("| Action | Count |\n|--------|-------|\n")
        f.write(f"| flipped | {counts['flipped']} |\n")
        f.write(f"| kept | {counts['kept']} |\n")
        f.write(f"| flagged | {counts['flagged']} |\n")
        f.write(f"| **total** | **{sum(counts.values())}** |\n\n")

        f.write("## Per-edge-type breakdown (flipped rows)\n\n")
        f.write("| Edge Type | Flipped Count |\n|-----------|---------------|\n")
        for et, cnt in top_flipped:
            f.write(f"| {et} | {cnt} |\n")
        f.write("\n")

        f.write("## Verification probes\n\n")
        f.write("Known-inverted rows from design doc §1:\n\n")
        for label, passed in probe_results:
            status = "YES — flipped correctly" if passed else "NO — not flipped (DEBUG NEEDED)"
            f.write(f"- **{label}**: {status}\n")
        f.write("\n")

        f.write("## Flipped rows (detailed)\n\n")
        if diff_sections:
            for section in diff_sections:
                f.write(section + "\n")
        else:
            f.write("_No rows were flipped._\n")

    print(f"Wrote diff report to {diff_path}")

    # --- Console summary ---
    print("\n=== NORMALIZER SUMMARY ===")
    print(f"  Flipped : {counts['flipped']}")
    print(f"  Kept    : {counts['kept']}")
    print(f"  Flagged : {counts['flagged']}")
    print(f"  Total   : {sum(counts.values())}")
    print()
    print("Top flipped edge types:")
    for et, cnt in top_flipped[:10]:
        print(f"  {et}: {cnt}")
    print()

    print("=== VERIFICATION PROBES ===")
    for label, passed in probe_results:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {label}")
    print()


if __name__ == "__main__":
    main()
