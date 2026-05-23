#!/usr/bin/env python3
"""
Temporary script to classify Glover family candidates.
Processes all 5 input files and writes edges to output files.
"""
import json
import sys
from pathlib import Path

BASE_PATH = Path("/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-glover")
CANDIDATES_DIR = BASE_PATH / "prose-edge-candidates-enriched"
EDGES_DIR = BASE_PATH / "prose-edges-haiku"

# Create output directory
EDGES_DIR.mkdir(parents=True, exist_ok=True)

# Files to process
FILES = [
    "benton-glover",
    "erena-glover",
    "ethan-glover",
    "galbart-glover",
    "gawen-glover",
]

def classify_edge(candidate):
    """Classify a single candidate edge."""
    source = candidate["source_slug"]
    target = candidate["target_slug"]
    target_type = candidate["target_type"]
    evidence_para = candidate.get("evidence_paragraph", "")
    valid_types = candidate.get("valid_edge_types", [])
    evidence_section = candidate.get("source_section", "")

    # Decision logic by pattern

    # Sibling relationships (explicit "along with his/her [sibling]")
    if "along with his sister" in evidence_para or "along with her brother" in evidence_para:
        if target_type == "character.human" and "SIBLING_OF" in valid_types:
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source,
                "target_slug": target,
                "edge_type": "SIBLING_OF",
                "qualifier": "unknown",  # Without explicit full/half/step indication
                "evidence_snippet": evidence_para[:150],
                "evidence_section": evidence_section,
                "confidence_tier": 1
            }

    # Captivity relationships ("captured by", "held captive by")
    if "captured" in evidence_para.lower() or "held captive" in evidence_para.lower():
        # If target is organization (ironborn, faction), it could be PRISONER_OF or CAPTURES
        if target_type == "organization.faction" and "PRISONER_OF" in valid_types:
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source,
                "target_slug": target,
                "edge_type": "PRISONER_OF",
                "evidence_snippet": evidence_para[:150],
                "evidence_section": evidence_section,
                "confidence_tier": 1
            }
        # If target is character, could be relationship with captor
        if target_type == "character.human" and ("held captive" in evidence_para or "captive" in evidence_para):
            if "GUARDS" in valid_types or "PRISONER_OF" in valid_types:
                # "held captive by X" means X guards/imprisons the source
                # But we emit on source's node, so source → X via PRISONER_OF
                if "PRISONER_OF" in valid_types:
                    return {
                        "decision": "emit_edge",
                        "candidate_kind": "source_target",
                        "evidence_kind": "wiki-entity",
                        "source_slug": source,
                        "target_slug": target,
                        "edge_type": "PRISONER_OF",
                        "evidence_snippet": evidence_para[:150],
                        "evidence_section": evidence_section,
                        "confidence_tier": 1
                    }

    # Custodial relationships ("under the care of")
    if "under the care of" in evidence_para:
        if target_type == "character.human" and "GUARDS" in valid_types:
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source,
                "target_slug": target,
                "edge_type": "GUARDS",
                "evidence_snippet": evidence_para[:150],
                "evidence_section": evidence_section,
                "confidence_tier": 1
            }

    # Imprisonment at location ("held captive at", "imprisoned at") - CHECK THIS FIRST
    if target_type == "place.location" and ("held captive at" in evidence_para.lower() or "imprisoned at" in evidence_para.lower()):
        if "IMPRISONED_AT" in valid_types:
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source,
                "target_slug": target,
                "edge_type": "IMPRISONED_AT",
                "evidence_snippet": evidence_para[:150],
                "evidence_section": evidence_section,
                "confidence_tier": 1
            }

    # General location relationships (after checking for imprisoned_at)
    if target_type in ["place.location", "place.region"]:
        # "taken to X", "at X", "atop X", "stop at X"
        if any(verb in evidence_para.lower() for verb in ["taken to", "at ", "atop", "stop at"]):
            if "LOCATED_AT" in valid_types:
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source,
                    "target_slug": target,
                    "edge_type": "LOCATED_AT",
                    "evidence_snippet": evidence_para[:150],
                    "evidence_section": evidence_section,
                    "confidence_tier": 1
                }

    # Escorting/traveling with ("escorted her")
    if "escorted" in evidence_para and target_type == "character.human":
        if "TRAVELS_WITH" in valid_types:
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source,
                "target_slug": target,
                "edge_type": "TRAVELS_WITH",
                "evidence_snippet": evidence_para[:150],
                "evidence_section": evidence_section,
                "confidence_tier": 2
            }

    # "Search for a wet nurse" / seeking role - wet nurse is title type
    if "search for a wet nurse" in evidence_para.lower() and target_type == "title":
        # This is seeking someone to fill a role, not an edge to the role itself
        # Reject as just-mention
        return {
            "decision": "reject_just_mention",
            "candidate_kind": "source_target",
            "source_slug": source,
            "target_slug": target,
            "reason": "no-fitting-type-vocab-locked"
        }

    # Default: reject as just-mention if nothing matched
    return {
        "decision": "reject_just_mention",
        "candidate_kind": "source_target",
        "source_slug": source,
        "target_slug": target,
        "reason": "no-fitting-type-vocab-locked"
    }

def main():
    for filename in FILES:
        input_path = CANDIDATES_DIR / f"{filename}.candidates.jsonl"
        output_path = EDGES_DIR / f"{filename}.edges.jsonl"

        if not input_path.exists():
            print(f"Warning: {input_path} not found", file=sys.stderr)
            continue

        decisions = []
        with open(input_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    candidate = json.loads(line)
                    decision = classify_edge(candidate)
                    decisions.append(decision)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error in {filename}: {e}", file=sys.stderr)
                    continue

        # Write output
        if decisions:
            with open(output_path, 'w') as f:
                for decision in decisions:
                    f.write(json.dumps(decision) + '\n')
            print(f"[done] {filename}.candidates.jsonl → {len([d for d in decisions if d['decision'] == 'emit_edge'])} emit_edge, {len([d for d in decisions if d['decision'] == 'reject_just_mention'])} reject_just_mention, 0 escalate — wrote {output_path}")
        else:
            print(f"No candidates in {filename}", file=sys.stderr)

if __name__ == "__main__":
    main()
