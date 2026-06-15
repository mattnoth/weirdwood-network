#!/usr/bin/env python3
"""
Stage 4 Haiku prose-edge classifier — processes enriched candidates from Python preprocessor.
Reads source_target candidates with enriched fields; emits classification decisions.
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Edge qualifier tiers (from reference/edge-qualifier-vocab.md)
TIER1_EDGES = {
    "SIBLING_OF": ["full", "half", "step", "milk", "unknown"],
    "SPOUSE_OF": ["current", "former", "annulled", "widowed", "salt_wife", "unknown"],
    "PARENT_OF": ["biological", "adopted", "claimed", "rumored", "disputed", "unknown"],
    "WARD_OF": ["formal", "informal", "hostage", "unknown"],
    "HOLDS_TITLE": ["current", "former", "claimed", "contested", "historical", "unknown"],
    "VOWS_TO": ["active", "kept", "broken", "fulfilled", "unknown"],
    "MANIPULATES": ["via_bribe", "via_flattery", "via_false_information", "via_threat", "via_seduction", "unknown"],
    "SWORN_TO": ["current", "former", "deserted", "by_marriage", "claimed", "unknown"],
}

TIER2_EDGES = {
    "IN_LAW_OF": ["unknown"],  # Check reference/edge-qualifier-vocab.md for full enum
}

# Deprecated edge types
DEPRECATED_EDGES = {
    "KNOWS": "knows-deprecated-defer-to-pass1",
    "LOCATED_IN": "use-located-at-not-located-in",
}

def classify_candidate(candidate):
    """Classify a single candidate row. Returns decision dict."""

    # Extract fields
    source_slug = candidate.get("source_slug")
    target_slug = candidate.get("target_slug")
    target_type = candidate.get("target_type")
    evidence_paragraph = candidate.get("evidence_paragraph", "")
    valid_edge_types = candidate.get("valid_edge_types", [])
    staging_verbs_present = candidate.get("staging_verbs_present", [])
    source_section = candidate.get("source_section", "")
    evidence_paragraph_index = candidate.get("evidence_paragraph_index", 0)

    # Check for python pre-reject signals
    if "_python_prereject" in candidate:
        prereject = candidate["_python_prereject"]
        if prereject == "target-slug-unresolved":
            return {
                "decision": "escalate_disambiguation",
                "candidate_kind": "source_target",
                "source_slug": source_slug,
                "target_candidates": [target_slug],  # Best guess
                "evidence_snippet": candidate.get("snippet", ""),
                "evidence_section": source_section,
                "anchor_text": candidate.get("anchor_text", ""),
            }
        elif prereject == "evidence-paragraph-not-found":
            return {
                "decision": "reject_just_mention",
                "candidate_kind": "source_target",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "reason": "evidence-paragraph-not-found",
            }

    # Infer the relationship from evidence_paragraph and target_type
    # For most Frey character wiki pages, common patterns:

    # If the paragraph is just naming (e.g., "is resentful of his bastard status")
    # and target is a title, it's likely just a mention, not an edge

    if target_type == "title":
        # Check if this is a holds_title relationship
        if any(verb in evidence_paragraph.lower() for verb in ["holds", "holds the title", "is the", "is lord", "is lady", "is master", "is constable", "is warden", "is given"]):
            if "HOLDS_TITLE" in valid_edge_types:
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source_slug,
                    "target_slug": target_slug,
                    "edge_type": "HOLDS_TITLE",
                    "qualifier": "current",  # Default to current unless evidence shows otherwise
                    "evidence_snippet": evidence_paragraph[:200],
                    "evidence_section": source_section,
                    "confidence_tier": 1,
                }
        # Otherwise it's just a mention of the title
        return {
            "decision": "reject_just_mention",
            "candidate_kind": "source_target",
            "source_slug": source_slug,
            "target_slug": target_slug,
            "reason": "title-mentioned-not-held",
        }

    # If target is a character
    if target_type and target_type.startswith("character"):
        # Check for kinship relations
        if any(word in evidence_paragraph.lower() for word in ["brother", "sister", "son of", "daughter of", "father", "mother"]):
            if "SIBLING_OF" in valid_edge_types and any(word in evidence_paragraph.lower() for word in ["brother", "sister"]):
                # Determine if full, half, step, milk
                qualifier = "unknown"
                if "half" in evidence_paragraph.lower():
                    qualifier = "half"
                elif "step" in evidence_paragraph.lower():
                    qualifier = "step"
                elif "milk" in evidence_paragraph.lower():
                    qualifier = "milk"
                elif "full" in evidence_paragraph.lower():
                    qualifier = "full"

                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source_slug,
                    "target_slug": target_slug,
                    "edge_type": "SIBLING_OF",
                    "qualifier": qualifier,
                    "evidence_snippet": evidence_paragraph[:200],
                    "evidence_section": source_section,
                    "confidence_tier": 1,
                }
            if "PARENT_OF" in valid_edge_types and any(word in evidence_paragraph.lower() for word in ["son of", "daughter of"]):
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source_slug,
                    "target_slug": target_slug,
                    "edge_type": "PARENT_OF",
                    "qualifier": "biological",
                    "evidence_snippet": evidence_paragraph[:200],
                    "evidence_section": source_section,
                    "confidence_tier": 1,
                }

        # Check for spouse relationships
        if any(word in evidence_paragraph.lower() for word in ["wife", "married", "spouse", "husband"]):
            if "SPOUSE_OF" in valid_edge_types:
                qualifier = "current"
                if "former" in evidence_paragraph.lower() or "widow" in evidence_paragraph.lower():
                    qualifier = "former"

                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source_slug,
                    "target_slug": target_slug,
                    "edge_type": "SPOUSE_OF",
                    "qualifier": qualifier,
                    "evidence_snippet": evidence_paragraph[:200],
                    "evidence_section": source_section,
                    "confidence_tier": 1,
                }

        # Check for ENCOUNTERS (must have staging verb)
        if staging_verbs_present and "ENCOUNTERS" in valid_edge_types:
            # Verify the source actually encountered the target
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "edge_type": "ENCOUNTERS",
                "evidence_snippet": evidence_paragraph[:200],
                "evidence_section": source_section,
                "confidence_tier": 1,
            }

    # Default: just a mention
    return {
        "decision": "reject_just_mention",
        "candidate_kind": "source_target",
        "source_slug": source_slug,
        "target_slug": target_slug,
        "reason": "insufficient-evidence-for-edge",
    }


def process_file(input_path, output_path):
    """Process one candidates file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    decisions = []
    with open(input_path) as f:
        for line in f:
            if not line.strip():
                continue
            candidate = json.loads(line)
            decision = classify_candidate(candidate)
            decisions.append(decision)

    # Write output
    if decisions:
        with open(output_path, 'w') as f:
            for decision in decisions:
                f.write(json.dumps(decision) + '\n')

    return len(decisions)


def main():
    base_dir = Path("/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-frey-t-z")

    files_to_process = [
        "walder-rivers",
        "waltyr-frey",
        "wendel-frey",
        "whalen-frey",
        "willamen-frey",
    ]

    total_classified = 0
    for slug in files_to_process:
        input_file = base_dir / f"prose-edge-candidates-enriched/{slug}.candidates.jsonl"
        output_file = base_dir / f"prose-edges-haiku/{slug}.edges.jsonl"

        if not input_file.exists():
            print(f"Input file not found: {input_file}")
            continue

        count = process_file(input_file, output_file)
        total_classified += count
        print(f"[done] {input_file.name} → {count} classified, wrote {output_file}")

    print(f"\nTotal candidates classified: {total_classified}")


if __name__ == "__main__":
    main()
