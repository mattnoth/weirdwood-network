#!/usr/bin/env python3
"""
Stage 4 Haiku prose-edge classifier for Karstark characters.
Processes enriched candidates and emits classification decisions.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Tier-1 edges that require `qualifier` field
TIER_1_EDGES = {
    "SIBLING_OF": ["full", "half", "step", "milk", "unknown"],
    "SPOUSE_OF": ["current", "former", "annulled", "widowed", "salt_wife", "unknown"],
    "PARENT_OF": ["biological", "adopted", "claimed", "rumored", "disputed", "unknown"],
    "WARD_OF": ["formal", "informal", "hostage", "unknown"],
    "HOLDS_TITLE": ["current", "former", "claimed", "contested", "historical", "unknown"],
    "VOWS_TO": ["active", "kept", "broken", "fulfilled", "unknown"],
    "MANIPULATES": ["via_bribe", "via_flattery", "via_false_information", "via_threat", "via_seduction", "unknown"],
    "SWORN_TO": ["current", "former", "deserted", "by_marriage", "claimed", "unknown"],
}

def classify_candidate(candidate):
    """
    Classify a single source_target candidate.
    Returns decision dict or None if no output needed.
    """
    source = candidate["source_slug"]
    target = candidate["target_slug"]
    target_type = candidate.get("target_type", "")
    evidence_para = candidate.get("evidence_paragraph", "")
    valid_types = candidate.get("valid_edge_types", [])
    staging_verbs = candidate.get("staging_verbs_present", [])
    prereject = candidate.get("_python_prereject", None)
    section = candidate.get("source_section", "## Unknown")
    snippet = candidate.get("snippet", "").lower()

    # Handle pre-rejection cases
    if prereject:
        if prereject == "target-slug-unresolved":
            return {
                "decision": "escalate_disambiguation",
                "candidate_kind": "source_target",
                "source_slug": source,
                "target_candidates": [target],
                "evidence_snippet": candidate.get("snippet", "")[:200],
                "evidence_section": section,
                "anchor_text": candidate.get("anchor_text", ""),
            }
        elif prereject == "evidence-paragraph-not-found":
            return {
                "decision": "reject_just_mention",
                "candidate_kind": "source_target",
                "source_slug": source,
                "target_slug": target,
                "reason": "evidence-paragraph-not-found",
            }

    # Spatial relation detection
    if target_type in ["place.location", "place.region"]:
        # LOCATED_AT, TRAVELS_TO, BORN_AT, DIED_AT, etc.
        if "travel" in evidence_para.lower() or "goes to" in evidence_para.lower() or "journeys to" in evidence_para.lower():
            if "TRAVELS_TO" in valid_types:
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source,
                    "target_slug": target,
                    "edge_type": "TRAVELS_TO",
                    "evidence_snippet": evidence_para[:180],
                    "evidence_section": section,
                    "confidence_tier": 2,
                }

        # Default spatial: LOCATED_AT
        if "LOCATED_AT" in valid_types:
            # Check if it's a birth/death context
            if "born" in evidence_para.lower() and "BORN_AT" in valid_types:
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source,
                    "target_slug": target,
                    "edge_type": "BORN_AT",
                    "evidence_snippet": evidence_para[:180],
                    "evidence_section": section,
                    "confidence_tier": 2,
                }
            elif "died" in evidence_para.lower() and "DIED_AT" in valid_types:
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source,
                    "target_slug": target,
                    "edge_type": "DIED_AT",
                    "evidence_snippet": evidence_para[:180],
                    "evidence_section": section,
                    "confidence_tier": 2,
                }
            else:
                # Generic presence - many such mentions are temporal co-occurrence
                if "at" not in evidence_para.lower() or "on" not in evidence_para.lower():
                    # No strong spatial language - likely just a mention
                    return {
                        "decision": "reject_just_mention",
                        "candidate_kind": "source_target",
                        "source_slug": source,
                        "target_slug": target,
                        "reason": "temporal-cooccurrence-not-relational",
                    }
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source,
                    "target_slug": target,
                    "edge_type": "LOCATED_AT",
                    "evidence_snippet": evidence_para[:180],
                    "evidence_section": section,
                    "confidence_tier": 2,
                }

    # Character-to-character relations
    elif target_type in ["character.human", "character.other"]:
        # Check for KILLED_BY - look for "killed" in the snippet (which is near the link)
        if "killed" in snippet:
            if "KILLED_BY" in valid_types:
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source,
                    "target_slug": target,
                    "edge_type": "KILLED_BY",
                    "evidence_snippet": evidence_para[:180],
                    "evidence_section": section,
                    "confidence_tier": 2,
                }

        # Check for ENCOUNTERS (requires staging verb)
        if staging_verbs:
            if "ENCOUNTERS" in valid_types:
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source,
                    "target_slug": target,
                    "edge_type": "ENCOUNTERS",
                    "evidence_snippet": evidence_para[:180],
                    "evidence_section": section,
                    "confidence_tier": 2,
                }

        # Skip SIBLING_OF from prose - kinship should come from infobox edges
        # Prose mentions of "my brother X" are typically used to describe appearance, not to establish the kinship

        # TRAVELS_WITH for retinue/court presence - check snippet for accompaniment language
        if any(word in snippet for word in ["accompan", "travels", "guard", "retinue", "brother", "sister"]):
            if "TRAVELS_WITH" in valid_types:
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source,
                    "target_slug": target,
                    "edge_type": "TRAVELS_WITH",
                    "evidence_snippet": evidence_para[:180],
                    "evidence_section": section,
                    "confidence_tier": 2,
                }

        # Default: no fitting type for character-character mention without context
        return {
            "decision": "reject_just_mention",
            "candidate_kind": "source_target",
            "source_slug": source,
            "target_slug": target,
            "reason": "no-fitting-type-vocab-locked",
        }

    # Event relations
    elif target_type in ["event.battle", "event.siege", "event.war", "event.tournament", "event.ceremony"]:
        # FIGHTS_IN, PARTICIPATES_IN, ATTENDS
        if ("fight" in evidence_para.lower() or "battle" in evidence_para.lower() or
            "siege" in evidence_para.lower() or "war" in evidence_para.lower()):
            if "FIGHTS_IN" in valid_types:
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source,
                    "target_slug": target,
                    "edge_type": "FIGHTS_IN",
                    "evidence_snippet": evidence_para[:180],
                    "evidence_section": section,
                    "confidence_tier": 2,
                }
            elif "PARTICIPATES_IN" in valid_types:
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source,
                    "target_slug": target,
                    "edge_type": "PARTICIPATES_IN",
                    "evidence_snippet": evidence_para[:180],
                    "evidence_section": section,
                    "confidence_tier": 2,
                }

        if "ATTENDS" in valid_types:
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source,
                "target_slug": target,
                "edge_type": "ATTENDS",
                "evidence_snippet": evidence_para[:180],
                "evidence_section": section,
                "confidence_tier": 2,
            }

        return {
            "decision": "reject_just_mention",
            "candidate_kind": "source_target",
            "source_slug": source,
            "target_slug": target,
            "reason": "no-fitting-type-vocab-locked",
        }

    # Org/House relations
    elif target_type in ["organization.house", "organization.faction", "organization.order"]:
        if "house" in evidence_para.lower() or "sworn" in evidence_para.lower():
            if "SWORN_TO" in valid_types:
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source,
                    "target_slug": target,
                    "edge_type": "SWORN_TO",
                    "qualifier": "unknown",
                    "evidence_snippet": evidence_para[:180],
                    "evidence_section": section,
                    "confidence_tier": 2,
                }
            elif "MEMBER_OF" in valid_types:
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source,
                    "target_slug": target,
                    "edge_type": "MEMBER_OF",
                    "evidence_snippet": evidence_para[:180],
                    "evidence_section": section,
                    "confidence_tier": 2,
                }

        return {
            "decision": "reject_just_mention",
            "candidate_kind": "source_target",
            "source_slug": source,
            "target_slug": target,
            "reason": "no-fitting-type-vocab-locked",
        }

    # Default fallback
    return {
        "decision": "reject_just_mention",
        "candidate_kind": "source_target",
        "source_slug": source,
        "target_slug": target,
        "reason": "no-fitting-type-vocab-locked",
    }


def process_file(input_path, output_path):
    """Process a single input file and write classified output."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    candidates = []
    with open(input_path) as f:
        for line in f:
            if line.strip():
                candidates.append(json.loads(line))

    if not candidates:
        print(f"[skip] {input_path.name} → empty file")
        return 0, 0, 0, 0

    emit_count = 0
    reject_count = 0
    escalate_count = 0

    with open(output_path, 'w') as outf:
        for candidate in candidates:
            decision = classify_candidate(candidate)
            if decision:
                outf.write(json.dumps(decision) + "\n")

                if decision["decision"] == "emit_edge":
                    emit_count += 1
                elif decision["decision"] == "reject_just_mention":
                    reject_count += 1
                else:
                    escalate_count += 1

    return emit_count, reject_count, escalate_count, len(candidates)


def main():
    bucket_dir = Path("working/wiki/pass2-buckets/characters-house-karstark")
    input_dir = bucket_dir / "prose-edge-candidates-enriched"
    output_dir = bucket_dir / "prose-edges-haiku"

    files = [
        "alys-karstark.candidates.jsonl",
        "arnolf-karstark.candidates.jsonl",
        "arthor-karstark.candidates.jsonl",
        "cregan-karstark.candidates.jsonl",
        "eddard-karstark.candidates.jsonl",
    ]

    total_emits = 0
    total_rejects = 0
    total_escalates = 0
    total_candidates = 0

    for filename in files:
        input_path = input_dir / filename
        output_path = output_dir / filename.replace(".candidates.jsonl", ".edges.jsonl")

        if not input_path.exists():
            print(f"[skip] {filename} → not found", file=sys.stderr)
            continue

        emits, rejects, escalates, total = process_file(input_path, output_path)
        total_emits += emits
        total_rejects += rejects
        total_escalates += escalates
        total_candidates += total

        print(f"[done] {filename} → {emits} emit_edge, {rejects} reject_just_mention, {escalates} escalate — wrote {output_path}")

    print(f"\n=== SUMMARY ===")
    print(f"Total candidates: {total_candidates}")
    print(f"Emit edges: {total_emits}")
    print(f"Reject mentions: {total_rejects}")
    print(f"Escalations: {total_escalates}")


if __name__ == "__main__":
    main()
