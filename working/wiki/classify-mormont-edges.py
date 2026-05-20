#!/usr/bin/env python3
"""
Classify prose edge candidates for Jeor and Jorah Mormont.
This is a helper script to systematically process the large volume of candidates.
"""

import json
import sys
from pathlib import Path

# Read the candidates files
jeor_candidates_path = Path("/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-mormont/prose-edge-candidates/jeor-mormont.candidates.jsonl")
jorah_candidates_path = Path("/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-mormont/prose-edge-candidates/jorah-mormont.candidates.jsonl")

# Output paths
jeor_output_path = Path("/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-mormont/prose-edges-haiku/jeor-mormont.edges.jsonl")
jorah_output_path = Path("/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-mormont/prose-edges-haiku/jorah-mormont.edges.jsonl")

# Create output directories
jeor_output_path.parent.mkdir(parents=True, exist_ok=True)
jorah_output_path.parent.mkdir(parents=True, exist_ok=True)

def classify_candidate(candidate):
    """Classify a single candidate edge."""
    source = candidate["source_slug"]
    target = candidate["target_slug"]
    section = candidate["source_section"]
    snippet = candidate["snippet"]

    # Categories for automatic rejection (just mentions):
    # Objects, materials, substances that are descriptions
    reject_targets = {
        # Materials
        "gold", "silver", "steel", "valyrian-steel", "bronze", "iron", "copper", "leather", "cloth", "wool",
        # Substances
        "lemon", "beer", "wine", "food", "meat", "bread", "water",
        # Decorative elements
        "bear",  # when referring to bearclaw decorations
        # Generic concepts
        "knight", "steward", "ranger", "squire",
        # Concepts
        "iron-throne", "wall", "north", "south", "east", "west",
    }

    # Likely just mentions based on section
    if section == "## Appearances & Description" and target in reject_targets:
        return {
            "decision": "reject_just_mention",
            "candidate_kind": candidate["candidate_kind"],
            "source_slug": source,
            "target_slug": target,
            "reason": "appearance-description-not-relational"
        }

    # Locations and spatial relationships
    location_targets = {
        "castle-black", "wall", "beyond-the-wall", "fist-of-the-first-men",
        "lord-commanders-tower", "king's-tower", "shadow-tower", "crasters-keep",
        "frostfangs", "milkwater", "skirling-pass", "giants-stair", "craster's-keep",
        "red-keep", "kings-landing", "qarth", "pentos", "vaes-tolorro", "asshai",
        "dothraki-sea", "daznak's-pit", "free-cities", "meereen", "house-of-the-undying",
        "port-of-qarth", "seven-kingdoms", "further-east", "beyond-the-wall",
    }

    if target in location_targets and "resid" in snippet.lower() or "at" in snippet.lower():
        return {
            "decision": "emit_edge",
            "candidate_kind": candidate["candidate_kind"],
            "evidence_kind": "wiki-entity",
            "source_slug": source,
            "target_slug": target,
            "edge_type": "LOCATED_AT",
            "evidence_snippet": snippet[:200],
            "evidence_section": section,
            "evidence_paragraph_index": 0,
            "confidence_tier": 1
        }

    # Character relationships
    character_targets = {
        "benjen-stark", "jon-snow", "samwell-tarly", "tyrion-lannister",
        "robb-stark", "eddard-stark", "alliser-thorne", "othor", "jafer-flowers",
        "jaremy-rykker", "joffrey-baratheon", "pycelle", "renly-baratheon",
        "robert-i-baratheon", "denys-mallister", "qhorin-halfhand", "craster",
        "barristan-selmy", "daenerys-targaryen", "drogo", "belwas",
        "stannis-baratheon", "mance-rayder", "rhaegal", "viserion", "drogon",
        "barristan-selmy", "lynesse-hightower", "house-glover", "xaro-xhoan-daxos",
        "bowen-marsh", "cotter-pyke", "maege-mormont", "jorah-mormont",
    }

    # Check for weapons/artifacts
    weapon_targets = {
        "longclaw", "mormonts-raven", "ghost", "direwolf", "dragonglass",
    }

    if target == "longclaw" and source in ["jeor-mormont", "jorah-mormont"]:
        if "possesses" in snippet.lower() or "wields" in snippet.lower() or "ancestral" in snippet.lower():
            return {
                "decision": "emit_edge",
                "candidate_kind": candidate["candidate_kind"],
                "evidence_kind": "wiki-entity",
                "source_slug": source,
                "target_slug": target,
                "edge_type": "WIELDS",
                "evidence_snippet": snippet[:200],
                "evidence_section": section,
                "evidence_paragraph_index": 0,
                "confidence_tier": 1
            }

    if target == "mormonts-raven" and "accompanied" in snippet.lower():
        return {
            "decision": "emit_edge",
            "candidate_kind": candidate["candidate_kind"],
            "evidence_kind": "wiki-entity",
            "source_slug": source,
            "target_slug": target,
            "edge_type": "OWNS",
            "evidence_snippet": snippet[:200],
            "evidence_section": section,
            "evidence_paragraph_index": 0,
            "confidence_tier": 1
        }

    # Default: reject as just mention
    return {
        "decision": "reject_just_mention",
        "candidate_kind": candidate["candidate_kind"],
        "source_slug": source,
        "target_slug": target,
        "reason": "insufficient-relational-evidence"
    }

# Process Jeor candidates
jeor_decisions = []
with open(jeor_candidates_path) as f:
    for line in f:
        candidate = json.loads(line)
        decision = classify_candidate(candidate)
        jeor_decisions.append(decision)

# Write Jeor output
with open(jeor_output_path, 'w') as f:
    for decision in jeor_decisions:
        f.write(json.dumps(decision) + '\n')

print(f"Processed {len(jeor_decisions)} Jeor candidates")
print(f"  Emit: {sum(1 for d in jeor_decisions if d['decision'] == 'emit_edge')}")
print(f"  Reject: {sum(1 for d in jeor_decisions if d['decision'] == 'reject_just_mention')}")

# Process Jorah candidates
jorah_decisions = []
with open(jorah_candidates_path) as f:
    for line in f:
        candidate = json.loads(line)
        decision = classify_candidate(candidate)
        jorah_decisions.append(decision)

# Write Jorah output
with open(jorah_output_path, 'w') as f:
    for decision in jorah_decisions:
        f.write(json.dumps(decision) + '\n')

print(f"Processed {len(jorah_decisions)} Jorah candidates")
print(f"  Emit: {sum(1 for d in jorah_decisions if d['decision'] == 'emit_edge')}")
print(f"  Reject: {sum(1 for d in jorah_decisions if d['decision'] == 'reject_just_mention')}")

print("\nDone!")
