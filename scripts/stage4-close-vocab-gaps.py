#!/usr/bin/env python3
"""
Stage 4 — close vocab-gap rows in questions-for-matt.jsonl.

For every row in `working/wiki/pass2-buckets/questions-for-matt.jsonl`,
append `resolved_at` + `resolution` fields per the Session 54/55 vocab-lock
decision doc (`working/agent-fleet-specs/stage4-vocab-lock-2026-05-18.md`).

Idempotent: rows that already carry a non-null `resolved_at` are skipped.
Output is written atomically: write to .tmp, then rename.

Run from repo root:
    python3 scripts/stage4-close-vocab-gaps.py            # rewrites in place
    python3 scripts/stage4-close-vocab-gaps.py --dry-run  # no writes; prints first 3 mapped diffs to stderr

The decision map is keyed primarily on row index (1-based, matching cat -n).
Indices are stable in this append-only JSONL. As a defensive cross-check, the
script verifies row content (question_id, proposed_type, source/target slugs)
against an expected fingerprint before applying — exits non-zero if anything
drifted.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
QUESTIONS = REPO / "working/wiki/pass2-buckets/questions-for-matt.jsonl"

# --- Resolution lookup table -------------------------------------------------
#
# Keyed by row index (1-based). Each entry:
#   "resolution": str          # the text written into the row's resolution field
#   "fingerprint": dict        # subset of fields used to defensively confirm the row hasn't shifted
#
# Index ranges checked against the file as read 2026-05-18.

# Convenience constants — all derived from architecture.md verdicts (Sessions 54/55).
A_STALE = "resolved-pre-adopted; type {t} added Session {n}"
A_STALE_PAIR = "resolved-pre-adopted; both {a} and {b} canonical (added Session {n})"

# Bucket-C reject reasons:
C_REVERSE = "rejected-reverse-direction; use {canonical} on the {endpoint}'s node"
C_GENERIC = "rejected-too-generic; {note}"

# Bucket-B accepts:
B_ACCEPT = "accepted-as-{t}; added Session 55 (second wave, 2026-05-18)"

# Bucket-D verdicts:
D_ACCEPT = "accepted-as-{t}; added Session 55 (second wave, 2026-05-18)"
D_REJECT = "rejected-{reason}"

# Non-vocab/infrastructure rows that already have resolutions or distinct dispositions
NONVOCAB_ALREADY = "pre-resolved; not a vocab-gap"
NONVOCAB_INFRA = "logged-infrastructure-only; not a vocab decision (Session 55 verdict: noted in todos for separate parser/type-classification work)"
NONVOCAB_CROSS_ID = "deferred-cross-identity; Session 55 deferred SAME_AS merges to a separate cross-identity pass (not part of Stage 4 vocab lock)"


DECISIONS: dict[int, dict] = {
    # Row 1-7: pre-existing resolved rows (will be skipped by idempotency check),
    # but we record their fingerprints to ensure the file hasn't drifted.
    1: {"fingerprint": {"question_id": "q-2026-04-26-001", "page": "Nymeria"}, "resolution": None, "already_resolved": True},
    2: {"fingerprint": {"question_id": "q-2026-04-26-001", "page": "Dragonkeepers"}, "resolution": None, "already_resolved": True},
    3: {"fingerprint": {"question_id": "q-2026-04-26-001", "page": "Sansa Stark"}, "resolution": None, "already_resolved": True},
    4: {"fingerprint": {"question_id": "q-2026-04-27-001", "page": "Colemon"}, "resolution": None, "already_resolved": True},
    5: {"fingerprint": {"question_id": "q-2026-04-27-001", "page": "House Mallister"}, "resolution": None, "already_resolved": True},

    # Row 6 — Tommard Heddle / parser bug for SPOUSE_OF; NOT a vocab gap (type=other).
    6: {
        "fingerprint": {"question_id": "q-2026-05-01-butterwell-001", "page": "Tommard Heddle"},
        "resolution": "logged-parser-bug-not-vocab; SPOUSE_OF link-vs-text parser bug noted for separate parser fix (Session 55 verdict)",
    },

    # Row 7 — Caltrops reclassification; type=other, not a vocab gap.
    7: {
        "fingerprint": {"question_id": "q-2026-05-01-001", "page": "Caltrops"},
        "resolution": "accepted-as-organization.faction; agent reclassification confirmed (Session 55 verdict — group of conspirators, not a war)",
    },

    # Row 8 — GIFTED_TO; already canonical pre-Stage-4 (architecture.md row 286).
    8: {
        "fingerprint": {"question_id": "q-2026-05-13-longclaw-001", "proposed_edge_type": "GIFTED_TO"},
        "resolution": "resolved-pre-adopted; GIFTED_TO is canonical (architecture.md row 286, pre-Stage-4)",
    },

    # Row 9 — MADE_OF; canonical pre-Stage-4 (architecture.md row 283).
    9: {
        "fingerprint": {"question_id": "q-2026-05-13-longclaw-002", "proposed_edge_type": "MADE_OF"},
        "resolution": "resolved-pre-adopted; MADE_OF is canonical (architecture.md row 283, pre-Stage-4)",
    },

    # Row 10 — DEFEATED_BY; reverse of DEFEATS (one-sided).
    10: {
        "fingerprint": {"question_id": "q-2026-05-14-characters-house-ambrose-001", "proposed_edge_type": "DEFEATED_BY"},
        "resolution": "rejected-reverse-direction; use DEFEATS on the victor's node (one-sided per Session 55 reverse-direction discipline)",
    },

    # Row 11 — USES_AS_SIGIL; rejected too-generic (better as metadata).
    11: {
        "fingerprint": {"question_id": "q-2026-05-14-characters-house-baelish-001", "proposed_edge_type": "USES_AS_SIGIL"},
        "resolution": "rejected-too-narrow; heraldic-sigil adoption is better captured as node metadata on the house, not as an edge (Session 55 verdict)",
    },

    # Row 12 — Melisandre untyped (shadow-children / glamors / nightfires).
    12: {
        "fingerprint": {"question_id": "q-2026-05-14-characters-house-baratheon-of-dragonstone-012"},
        "resolution": "accepted-as-PRACTICES (target = concept.magic; matched from untyped row via shadow-magic pattern; Session 55 verdict)",
    },

    # Row 13 — Melisandre wedding officiant (untyped).
    13: {
        "fingerprint": {"question_id": "q-2026-05-14-characters-house-baratheon-of-dragonstone-013"},
        "resolution": "accepted-as-OFFICIATES (matched from untyped row via wedding-officiant pattern; Session 55 verdict)",
    },

    # Row 14 — ATTENDS proposal; already canonical (Session 54).
    14: {
        "fingerprint": {"question_id": "q-2026-05-14-characters-house-baratheon-of-dragonstone-014"},
        "resolution": "resolved-pre-adopted; ATTENDS added Session 54 (2026-05-15)",
    },

    # Row 15 — PURCHASED_FROM / SOLD_TO / TRANSACTS_WITH compound proposal.
    15: {
        "fingerprint": {"source_slug": "henly-ashford", "target_slug": "duncan-the-tall"},
        "resolution": "accepted-as-PURCHASED_FROM (leading type in proposed list; SOLD_TO is reverse-direction one-sided per Session 55, TRANSACTS_WITH is too-generic — both rejected as sub-elements)",
    },

    # Row 16 — DESCENDED_FROM (untyped row 16; Blackfyre descendants).
    16: {
        "fingerprint": {"question_id": "q-2026-05-14-batch-0004-vocab-gap-001"},
        "resolution": "rejected-reverse-direction; ANCESTOR_OF exists (ancestor → descendant). DESCENDED_FROM is one-sided per Session 55 reverse-direction discipline — use ANCESTOR_OF on the ancestor's node",
    },

    # Row 17 — ATTENDS reinforcement (untyped row 17).
    17: {
        "fingerprint": {"question_id": "q-2026-05-14-batch-0004-vocab-gap-002"},
        "resolution": "resolved-pre-adopted; ATTENDS added Session 54 (2026-05-15)",
    },

    # Row 18 — UNCLE_OF / NEPHEW_OF; both canonical Session 54.
    18: {
        "fingerprint": {"question_id": "q-2026-05-15-batch-0006-vocab-gap-001"},
        "resolution": "resolved-pre-adopted; both UNCLE_OF and NEPHEW_OF canonical (added Session 54, 2026-05-15)",
    },

    # Row 19 — ATTENDS reinforcement (kingsmoot).
    19: {
        "fingerprint": {"question_id": "q-2026-05-15-batch-0006-vocab-gap-002"},
        "resolution": "resolved-pre-adopted; ATTENDS added Session 54 (2026-05-15)",
    },

    # Row 20 — Bracken sisters / Gregor (sexual violence, untyped).
    20: {
        "fingerprint": {"question_id": "q-2026-05-15-batch-0006-vocab-gap-003"},
        "resolution": "accepted-as-ASSAULTS (sexual violence specifically; matched from untyped row via Gregor/Bracken pattern; Matt's Session 55 verdict per ATTACKS-vs-ASSAULTS scope split)",
    },

    # Row 21 — SERVED_BY / EMPLOYS (reverse of SERVES).
    21: {
        "fingerprint": {"pattern": "SERVED_BY or EMPLOYS (master→servant directed edge)"},
        "resolution": "rejected-reverse-direction; use SERVES on the server's node (one-sided per Session 55 reverse-direction discipline)",
    },

    # Row 22 — BETROTHED_TO; canonical pre-Stage-4 (architecture.md row 154).
    22: {
        "fingerprint": {"pattern": "BETROTHED_TO (failed or completed betrothal attempt)"},
        "resolution": "resolved-pre-adopted; BETROTHED_TO is canonical (architecture.md row 154, pre-Stage-4)",
    },

    # Row 23 — PETITIONED.
    23: {
        "fingerprint": {"pattern": "PETITIONED (character petitioned a lord/king for action)"},
        "resolution": "rejected-too-narrow; use NEGOTIATES_WITH for petition-style approaches (Session 55 verdict)",
    },

    # Row 24 — COUSIN_OF; canonical Session 55 first wave.
    24: {
        "fingerprint": {"question_id": "vocab-gap-20260515-001", "proposed_edge_type": "COUSIN_OF"},
        "resolution": "resolved-pre-adopted; COUSIN_OF added Session 55 first wave (2026-05-16)",
    },

    # Row 25 — HOST_OF (reverse of GUEST_OF).
    25: {
        "fingerprint": {"question_id": "vocab-gap-20260515-002", "proposed_edge_type": "HOST_OF"},
        "resolution": "rejected-reverse-direction; use GUEST_OF on the guest's node (one-sided per Session 55 reverse-direction discipline)",
    },

    # Row 26 — BRIBES.
    26: {
        "fingerprint": {"question_id": "q-2026-05-14-batch-0008-vocab-gap-001", "proposed_edge_type": "BRIBES"},
        "resolution": "rejected-as-standalone-type; BRIBES collapses into MANIPULATES with qualifier-mechanism note (FIGHTS_IN/MANIPULATES description mods, Session 55 verdict)",
    },

    # Row 27 — BUILT.
    27: {
        "fingerprint": {"question_id": "q-2026-05-14-batch-0008-vocab-gap-002", "proposed_edge_type": "BUILT"},
        "resolution": "accepted-as-BUILT; added Session 55 second wave (2026-05-18)",
    },

    # Row 28 — LIAISED_WITH.
    28: {
        "fingerprint": {"question_id": "q-2026-05-15-batch-0009-vocab-gap-001", "proposed_edge_type": "LIAISED_WITH"},
        "resolution": "rejected-too-generic; use LOVER_OF (architecture.md description covers rumored/attested affairs outside marriage — Session 55 verdict)",
    },

    # Row 29 — COURTED.
    29: {
        "fingerprint": {"question_id": "q-2026-05-15-batch-0009-vocab-gap-002", "proposed_edge_type": "COURTED"},
        "resolution": "accepted-as-COURTS (filed as past-tense alias 'COURTED'); COURTS added Session 55 second wave (2026-05-18)",
    },

    # Row 30 — KINSMAN_OF.
    30: {
        "fingerprint": {"question_id": "q-2026-05-15-batch-0009-vocab-gap-003", "proposed_edge_type": "KINSMAN_OF"},
        "resolution": "rejected-too-generic; if kinship degree is unknown, reject the candidate rather than emit a near-meaningless generic kinship edge (Session 55 verdict)",
    },

    # Row 31 — GUARDIAN_OF (reverse of WARD_OF; FOSTERED_BY is the canonical reverse).
    31: {
        "fingerprint": {"question_id": "q-2026-05-15-batch-0011-vocab-gap-001", "proposed_edge_type": "GUARDIAN_OF"},
        "resolution": "rejected-reverse-direction; use FOSTERED_BY (explicitly-permitted reverse of WARD_OF per architecture.md row 156)",
    },

    # Row 32 — cross-identity (Gregor / Robert Strong).
    32: {
        "fingerprint": {"question_id": "q-2026-05-15-batch-0010-cross-id-001", "kind": "cross-identity"},
        "resolution": NONVOCAB_CROSS_ID,
    },

    # Row 33 — COMPETES_IN; rejected duplicate of FIGHTS_IN (Session 55 description mod).
    33: {
        "fingerprint": {"question_id": "q-2026-05-15-batch-0010-vocab-gap-001", "proposed_edge_type": "COMPETES_IN"},
        "resolution": "rejected-duplicate-of-FIGHTS_IN; Session 55 extended FIGHTS_IN description to 'battle, war, or tournament as a combatant' — tournament-combatant cases are now FIGHTS_IN, not a new type",
    },

    # Row 34 — ATTENDS reinforcement.
    34: {
        "fingerprint": {"pattern": "ATTENDS", "batch_id": "batch-0012"},
        "resolution": "resolved-pre-adopted; ATTENDS added Session 54 (2026-05-15)",
    },

    # Row 35 — UNCLE_OF / NEPHEW_OF reinforcement.
    35: {
        "fingerprint": {"pattern": "UNCLE_OF / NEPHEW_OF"},
        "resolution": "resolved-pre-adopted; both UNCLE_OF and NEPHEW_OF canonical (added Session 54, 2026-05-15)",
    },

    # Row 36 — SLAIN_BY_WEAPON / KILLED_WIELDING (KILLED_WITH absorbs).
    36: {
        "fingerprint": {"pattern": "SLAIN_BY_WEAPON / KILLED_WIELDING"},
        "resolution": "resolved-pre-adopted; KILLED_WITH added Session 54 — covers 'slain by Orphan-Maker' pattern exactly per architecture.md row 220 ('Combat death attributed to a specific named artifact')",
    },

    # Row 37 — ATTACKS.
    37: {
        "fingerprint": {"question_id": "q-2026-05-16-characters-house-dayne-of-high-hermitage-001", "proposed_edge_type": "ATTACKS"},
        "resolution": "accepted-as-ATTACKS; added Session 55 second wave (2026-05-18) — scoped as generic person→person or creature→person physical violence (Matt's call on ATTACKS-vs-ASSAULTS split)",
    },

    # Row 38 — MILK_BROTHER_OF.
    38: {
        "fingerprint": {"question_id": "q-2026-05-16-batch-0014-vocab-gap-001", "proposed_edge_type": "MILK_BROTHER_OF"},
        "resolution": "resolved-pre-adopted; MILK_BROTHER_OF added Session 55 first wave (2026-05-16)",
    },

    # Row 39 — NURSED_BY / WET_NURSE_OF.
    39: {
        "fingerprint": {"question_id": "q-2026-05-16-batch-0014-vocab-gap-002"},
        "resolution": "resolved-pre-adopted; both NURSED_BY and WET_NURSE_OF canonical (added Session 55 first wave, 2026-05-16)",
    },

    # Row 40 — CHILD_OF (reverse of PARENT_OF).
    40: {
        "fingerprint": {"question_id": "q-2026-05-16-batch-0014-vocab-gap-003", "proposed_edge_type": "CHILD_OF"},
        "resolution": "rejected-reverse-direction; use PARENT_OF on the parent's node (one-sided per Session 55 reverse-direction discipline)",
    },

    # Row 41 — RESURRECTED_BY (reverse of RESURRECTS).
    41: {
        "fingerprint": {"question_id": "q-2026-05-16-batch-0014-vocab-gap-004", "proposed_edge_type": "RESURRECTED_BY"},
        "resolution": "rejected-reverse-direction; use RESURRECTS on the resurrector's node (one-sided per Session 55 reverse-direction discipline)",
    },

    # Row 42 — KNIGHTED_BY / BESTOWS_KNIGHTHOOD_ON.
    42: {
        "fingerprint": {"question_id": "q-2026-05-16-batch-0014-vocab-gap-005"},
        "resolution": "resolved-pre-adopted; both KNIGHTED_BY and BESTOWS_KNIGHTHOOD_ON canonical (added Session 55 first wave, 2026-05-16)",
    },

    # Row 43 — HOSTED_BY / HOST_OF.
    43: {
        "fingerprint": {"question_id": "q-2026-05-16-batch-0014-vocab-gap-006"},
        "resolution": "rejected-reverse-direction; use GUEST_OF on the guest's node (one-sided per Session 55 reverse-direction discipline)",
    },

    # Row 44 — CROWNS_QUEEN_OF_LOVE_AND_BEAUTY.
    44: {
        "fingerprint": {"question_id": "q-2026-05-16-batch-0014-vocab-gap-007", "proposed_edge_type": "CROWNS_QUEEN_OF_LOVE_AND_BEAUTY"},
        "resolution": "accepted-as-CROWNS_QUEEN_OF_LOVE_AND_BEAUTY; added Session 55 second wave (2026-05-18)",
    },

    # Row 45 — DEPICTED_IN.
    45: {
        "fingerprint": {"question_id": "q-2026-05-16-batch-0016-vocab-gap-001", "proposed_edge_type": "DEPICTED_IN"},
        "resolution": "resolved-pre-adopted; DEPICTED_IN added Session 55 first wave (2026-05-16)",
    },

    # Row 46 — COUSIN_OF (Frey).
    46: {
        "fingerprint": {"question_id": "q-2026-05-16-characters-house-frey-a-e-001", "proposed_edge_type": "COUSIN_OF"},
        "resolution": "resolved-pre-adopted; COUSIN_OF added Session 55 first wave (2026-05-16)",
    },

    # Row 47 — GREAT_UNCLE_OF.
    47: {
        "fingerprint": {"question_id": "q-2026-05-17-characters-house-hardyng-001", "proposed_edge_type": "GREAT_UNCLE_OF"},
        "resolution": "rejected-derivable; great-uncle is derivable from UNCLE_OF + PARENT_OF chain at query time (Session 55 verdict — extended kinship rejected)",
    },

    # Row 48 — PROPOSED_AS_BRIDE.
    48: {
        "fingerprint": {"question_id": "q-2026-05-17-characters-house-harlaw-of-the-tower-of-glimmering-001", "proposed_edge_type": "PROPOSED_AS_BRIDE"},
        "resolution": "accepted-as-PROPOSED_AS_BRIDE; added Session 55 second wave (2026-05-18)",
    },

    # Row 49 — CREW_OF.
    49: {
        "fingerprint": {"question_id": "q-2026-05-17-characters-house-harlaw-002", "proposed_edge_type": "CREW_OF"},
        "resolution": "accepted-as-CREW_OF; added Session 55 second wave (2026-05-18) — sibling to CAPTAIN_OF; both target object.artifact vessel",
    },

    # Row 50 — NAMED_FOR.
    50: {
        "fingerprint": {"question_id": "q-2026-05-17-characters-house-harlaw-001", "proposed_edge_type": "NAMED_FOR"},
        "resolution": "rejected-too-generic; commemorative naming is plot-irrelevant for most cases and graph value is low (Session 55 verdict — collapses with NAMED_AFTER)",
    },

    # Row 51 — RELATED_TO.
    51: {
        "fingerprint": {"question_id": "q-2026-05-17-characters-house-harroway-001", "proposed_edge_type": "RELATED_TO"},
        "resolution": "rejected-too-generic; if kinship degree is unknown, reject the candidate rather than emit a near-meaningless generic kinship edge (Session 55 verdict)",
    },

    # Row 52 — CONTRACTED_WITH.
    52: {
        "fingerprint": {"question_id": "q-2026-05-17-characters-house-harte-001", "proposed_edge_type": "CONTRACTED_WITH"},
        "resolution": "accepted-as-CONTRACTED_WITH; added Session 55 second wave (2026-05-18)",
    },

    # Row 53 — DAUGHTER_IN_LAW_OF.
    53: {
        "fingerprint": {"question_id": "q-2026-05-17-characters-house-hightower-a-j-001", "proposed_edge_type": "DAUGHTER_IN_LAW_OF"},
        "resolution": "rejected-derivable; in-law relationships are derivable from SPOUSE_OF + PARENT_OF chains at query time (Session 55 verdict — extended kinship rejected)",
    },

    # Row 54 — infrastructure (manfred-hightower-aegons-conquest mis-typed).
    54: {
        "fingerprint": {"question_id": "q-2026-05-17-characters-house-hightower-a-j-002", "type": "infrastructure"},
        "resolution": NONVOCAB_INFRA,
    },

    # Row 55 — STEP_PARENT_OF.
    55: {
        "fingerprint": {"question_id": "q-2026-05-17-characters-house-hightower-a-j-001", "proposed_edge_type": "STEP_PARENT_OF"},
        "resolution": "rejected-derivable; step-parent is derivable from SPOUSE_OF + PARENT_OF chains at query time (Session 55 verdict — extended kinship rejected)",
    },

    # Row 56 — DIED_OF (Donnel/Shivers).
    56: {
        "fingerprint": {"question_id": "q-2026-05-17-characters-house-hightower-a-j-002", "proposed_edge_type": "DIED_OF"},
        "resolution": "accepted-as-DIED_OF; added Session 55 second wave (2026-05-18) — Knowledge & Information subsection alongside HEALS",
    },

    # Row 57 — COMMISSIONED (subsumed by BUILT).
    57: {
        "fingerprint": {"question_id": "q-2026-05-17-characters-house-hightower-j-w-001", "proposed_edge_type": "COMMISSIONED"},
        "resolution": "accepted-as-BUILT; COMMISSIONED collapses into BUILT (Session 55 second wave, 2026-05-18 — covers patron-of-construction)",
    },

    # Row 58 — MEMORIALIZED_IN.
    58: {
        "fingerprint": {"question_id": "q-2026-05-17-characters-house-hightower-j-w-002", "proposed_edge_type": "MEMORIALIZED_IN"},
        "resolution": "rejected-too-generic; commemorative naming is plot-irrelevant for most cases and graph value is low (Session 55 verdict — pairs with NAMED_FOR rejection)",
    },

    # Row 59 — REPUTED_AS.
    59: {
        "fingerprint": {"question_id": "vgap-patrice-hightower-magic-20260517", "proposed_type": "REPUTED_AS"},
        "resolution": "accepted-as-REPUTED_AS; added Session 55 second wave (2026-05-18)",
    },

    # Row 60 — COURTS.
    60: {
        "fingerprint": {"question_id": "q-2026-05-17-characters-house-hunter-001", "proposed_edge_type": "COURTS"},
        "resolution": "accepted-as-COURTS; added Session 55 second wave (2026-05-18)",
    },

    # Row 61 — ASSAULTS (Owen Inchfield / Brienne).
    61: {
        "fingerprint": {"question_id": "q-2026-05-17-characters-house-inchfield-001", "proposed_edge_type": "ASSAULTS"},
        "resolution": "accepted-as-ASSAULTS; added Session 55 second wave (2026-05-18) — scoped specifically for sexual violence per Matt's ATTACKS-vs-ASSAULTS split",
    },

    # Row 62 — NAMED_AFTER.
    62: {
        "fingerprint": {"proposed_type": "NAMED_AFTER", "source_slug": "rickard-karstark"},
        "resolution": "rejected-too-generic; commemorative naming is plot-irrelevant for most cases and graph value is low (Session 55 verdict)",
    },

    # Row 63 — COMPANION_OF.
    63: {
        "fingerprint": {"question_id": "q-2026-05-18-characters-house-mallister-001", "proposed_edge_type": "COMPANION_OF"},
        "resolution": "accepted-as-COMPANION_OF; added Session 55 second wave (2026-05-18)",
    },

    # Row 64 — PARTICIPATES_IN.
    64: {
        "fingerprint": {"question_id": "q-2026-05-18-characters-house-manderly-001", "proposed_edge_type": "PARTICIPATES_IN"},
        "resolution": "accepted-as-PARTICIPATES_IN; added Session 55 second wave (2026-05-18)",
    },

    # Row 65 — DIED_OF (Medrick Manderly / Winter Fever).
    65: {
        "fingerprint": {"question_id": "q-2026-05-18-characters-house-manderly-002", "proposed_edge_type": "DIED_OF"},
        "resolution": "accepted-as-DIED_OF; added Session 55 second wave (2026-05-18) — Knowledge & Information subsection alongside HEALS",
    },

    # Row 66 — AFFLICTED_BY.
    66: {
        "fingerprint": {"question_id": "q-2026-05-18-characters-house-massey-001", "proposed_edge_type": "AFFLICTED_BY"},
        "resolution": "accepted-as-AFFLICTED_BY; added Session 55 second wave (2026-05-18) — Knowledge & Information subsection alongside HEALS",
    },

    # Row 67 — infrastructure (trial-of-seven mis-typed).
    67: {
        "fingerprint": {"question_id": "q-20260518T131905-characters-house-massey-001", "type": "infrastructure"},
        "resolution": NONVOCAB_INFRA,
    },

    # Row 68 — Mandon Moore non-lethal physical attack (Tyrion slash, Sansa beating).
    # Both examples are non-sexual physical violence → ATTACKS per Matt's Session 55 ATTACKS-vs-ASSAULTS split.
    68: {
        "fingerprint": {"batch_id": "batch-0073", "source_slug": "mandon-moore", "proposed_type": "ASSAULTS"},
        "resolution": "accepted-as-ATTACKS; filed as ASSAULTS but Session 55 scoped ATTACKS for generic person→person physical violence and ASSAULTS specifically for sexual violence — Mandon's slash of Tyrion and beating of Sansa are non-sexual → ATTACKS (added Session 55 second wave, 2026-05-18)",
    },
}


def _lookup(row: dict, key: str):
    """Look up a field on the row; if not present at top level, fall back to row['context'][key]."""
    if key in row and row[key] is not None:
        return row[key]
    ctx = row.get("context")
    if isinstance(ctx, dict) and key in ctx:
        return ctx[key]
    return None


def fingerprint_matches(row: dict, fingerprint: dict) -> tuple[bool, list[str]]:
    """Return (matches, mismatch_keys). Empty fingerprint matches anything.
    Field lookups fall through to row['context'][key] when not at top level."""
    mismatches = []
    for k, expected in fingerprint.items():
        actual = _lookup(row, k)
        if actual != expected:
            mismatches.append(f"{k}: expected {expected!r}, got {actual!r}")
    return (len(mismatches) == 0, mismatches)


def load_rows() -> list[dict]:
    rows: list[dict] = []
    with QUESTIONS.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="Print first 3 mapped diffs to stderr; do not write")
    args = p.parse_args()

    rows = load_rows()
    total = len(rows)
    print(f"Loaded {total} rows from {QUESTIONS.relative_to(REPO)}", file=sys.stderr)

    # Verify the file matches what we mapped against
    expected_total = max(DECISIONS.keys())
    if total != expected_total:
        print(
            f"WARNING: file has {total} rows but decision map was built against {expected_total} rows. "
            "Check for newly-appended rows; they will be left untouched.",
            file=sys.stderr,
        )

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    # Force fixed date per the task spec (2026-05-18T<HH:MM:SS>):
    today = "2026-05-18"
    now_iso = f"{today}T{datetime.now(timezone.utc).strftime('%H:%M:%S')}"

    skipped_already = 0
    skipped_no_decision = 0
    closed = 0
    fingerprint_failures: list[tuple[int, list[str]]] = []
    bucket_summary: dict[str, int] = {}
    diff_samples: list[tuple[int, dict, dict]] = []  # (row_no, before, after)

    updated_rows: list[dict] = []

    for i, row in enumerate(rows, start=1):
        # Idempotent skip: already-resolved rows
        if row.get("resolved_at"):
            skipped_already += 1
            updated_rows.append(row)
            continue

        decision = DECISIONS.get(i)
        if decision is None:
            skipped_no_decision += 1
            updated_rows.append(row)
            continue

        ok, mismatches = fingerprint_matches(row, decision["fingerprint"])
        if not ok:
            fingerprint_failures.append((i, mismatches))
            updated_rows.append(row)
            continue

        resolution = decision.get("resolution")
        if resolution is None:
            # Row already resolved at the source (per the pre-existing resolved fields); leave untouched.
            updated_rows.append(row)
            skipped_already += 1
            continue

        new_row = dict(row)
        new_row["resolved_at"] = now_iso
        new_row["resolution"] = resolution

        bucket = row.get("bucket_id") or row.get("batch_id") or row.get("batch") or row.get("source_batch") or "unknown"
        bucket_summary[bucket] = bucket_summary.get(bucket, 0) + 1
        closed += 1

        if len(diff_samples) < 3:
            diff_samples.append((i, row, new_row))

        updated_rows.append(new_row)

    if fingerprint_failures:
        print(
            f"ERROR: {len(fingerprint_failures)} fingerprint mismatches — file content has drifted from the decision map. Refusing to write.",
            file=sys.stderr,
        )
        for row_no, mismatches in fingerprint_failures[:10]:
            print(f"  row {row_no}:", file=sys.stderr)
            for m in mismatches:
                print(f"    {m}", file=sys.stderr)
        return 2

    print(f"Skipped (already resolved): {skipped_already}", file=sys.stderr)
    print(f"Skipped (no decision in map): {skipped_no_decision}", file=sys.stderr)
    print(f"Closing this run: {closed}", file=sys.stderr)

    # Dry-run preview
    if diff_samples:
        print("\n--- First 3 mapped rows (before / after) ---", file=sys.stderr)
        for row_no, before, after in diff_samples:
            print(f"\n  Row {row_no}:", file=sys.stderr)
            print(f"    BEFORE resolved_at = {before.get('resolved_at')!r}", file=sys.stderr)
            print(f"    BEFORE resolution  = {before.get('resolution')!r}", file=sys.stderr)
            print(f"    AFTER  resolved_at = {after['resolved_at']!r}", file=sys.stderr)
            print(f"    AFTER  resolution  = {after['resolution']!r}", file=sys.stderr)

    if args.dry_run:
        print("\n[DRY RUN] No file written.", file=sys.stderr)
    else:
        tmp = QUESTIONS.with_suffix(QUESTIONS.suffix + ".tmp")
        with tmp.open("w") as f:
            for r in updated_rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        os.replace(tmp, QUESTIONS)
        print(f"\nWrote {len(updated_rows)} rows to {QUESTIONS.relative_to(REPO)}", file=sys.stderr)

    # Bucket-count summary to stdout
    print("\n# Bucket-count summary (rows closed this run)")
    if not bucket_summary:
        print("(no rows closed)")
    else:
        for bucket, count in sorted(bucket_summary.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  {count:>4}  {bucket}")
    print(f"\nTotal closed this run: {closed}")
    print(f"Total skipped (already resolved or no-decision): {skipped_already + skipped_no_decision}")
    print(f"File total rows: {total}")

    # Identify any vocab-gap rows that the script did NOT close
    unmapped_or_unresolved: list[int] = []
    for i, row in enumerate(updated_rows, start=1):
        if row.get("resolved_at"):
            continue
        unmapped_or_unresolved.append(i)
    if unmapped_or_unresolved:
        print(f"\nRows still unresolved ({len(unmapped_or_unresolved)}):")
        for i in unmapped_or_unresolved:
            r = updated_rows[i - 1]
            qid = r.get("question_id") or r.get("question_type") or r.get("pattern") or "<no id>"
            print(f"  row {i:>3}: {qid}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
