#!/usr/bin/env python3
"""
Stage 4 prose-edge classifier - classifies candidates from enriched prose candidates files.
Reads source_target candidates and outputs classified edges.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Tier 1 edges that REQUIRE a qualifier
TIER_1_QUALIFIERS = {
    'SIBLING_OF': ['full', 'half', 'step', 'milk', 'unknown'],
    'SPOUSE_OF': ['current', 'former', 'annulled', 'widowed', 'salt_wife', 'unknown'],
    'PARENT_OF': ['biological', 'adopted', 'claimed', 'rumored', 'disputed', 'unknown'],
    'WARD_OF': ['formal', 'informal', 'hostage', 'unknown'],
    'HOLDS_TITLE': ['current', 'former', 'claimed', 'contested', 'historical', 'unknown'],
    'VOWS_TO': ['active', 'kept', 'broken', 'fulfilled', 'unknown'],
    'MANIPULATES': ['via_bribe', 'via_flattery', 'via_false_information', 'via_threat', 'via_seduction', 'unknown'],
    'SWORN_TO': ['current', 'former', 'deserted', 'by_marriage', 'claimed', 'unknown'],
}

# Kinship edges that are commonly found
COMMON_KINSHIP_EDGES = {
    'SIBLING_OF', 'PARENT_OF', 'SPOUSE_OF', 'ANCESTOR_OF', 'UNCLE_OF', 'NEPHEW_OF',
    'COUSIN_OF', 'BETROTHED_TO', 'LOVER_OF', 'WARD_OF', 'MARRIES_OFF', 'IN_LAW_OF',
    'MILK_BROTHER_OF', 'NURSED_BY', 'WET_NURSE_OF', 'COURTS', 'STEP_PARENT_OF',
    'STEP_CHILD_OF', 'PROPOSED_AS_BRIDE', 'HEIR_TO'
}

# Spatial edges
SPATIAL_EDGES = {
    'LOCATED_AT', 'BORN_AT', 'DIED_AT', 'BURIED_AT', 'IMPRISONED_AT', 'TRAVELS_TO',
    'SEAT_OF', 'REGION_OF'
}

# Event-targeted edges
EVENT_EDGES = {'ATTENDS', 'FIGHTS_IN', 'COMMANDS_IN', 'PARTICIPATES_IN', 'PART_OF'}

def classify_candidate(candidate):
    """Classify a single enriched candidate into a decision."""

    source_slug = candidate['source_slug']
    target_slug = candidate['target_slug']
    target_type = candidate['target_type']
    evidence_paragraph = candidate.get('evidence_paragraph', '')
    valid_edge_types = candidate.get('valid_edge_types', [])
    staging_verbs_present = candidate.get('staging_verbs_present', [])
    source_section = candidate.get('source_section', '')

    # Extract paragraph index - default 0
    evidence_paragraph_index = 0

    # Try to infer relationship from evidence_paragraph text
    # This is a simplified classifier - a real one would have more sophisticated logic

    # Check for explicit kinship relationships mentioned in the evidence
    evidence_lower = evidence_paragraph.lower()

    # Half-brother / brother / sister relationships
    if 'half-brother' in evidence_lower and 'SIBLING_OF' in valid_edge_types:
        return {
            'decision': 'emit_edge',
            'candidate_kind': 'source_target',
            'evidence_kind': 'wiki-entity',
            'source_slug': source_slug,
            'target_slug': target_slug,
            'edge_type': 'SIBLING_OF',
            'qualifier': 'half',
            'evidence_snippet': evidence_paragraph[:200],
            'evidence_section': source_section,
            'evidence_paragraph_index': evidence_paragraph_index,
            'confidence_tier': 1,
        }

    if 'brother' in evidence_lower and 'his brother' in evidence_lower and 'SIBLING_OF' in valid_edge_types:
        return {
            'decision': 'emit_edge',
            'candidate_kind': 'source_target',
            'evidence_kind': 'wiki-entity',
            'source_slug': source_slug,
            'target_slug': target_slug,
            'edge_type': 'SIBLING_OF',
            'qualifier': 'full',
            'evidence_snippet': evidence_paragraph[:200],
            'evidence_section': source_section,
            'evidence_paragraph_index': evidence_paragraph_index,
            'confidence_tier': 1,
        }

    if 'goodbrother' in evidence_lower and 'IN_LAW_OF' in valid_edge_types:
        return {
            'decision': 'emit_edge',
            'candidate_kind': 'source_target',
            'evidence_kind': 'wiki-entity',
            'source_slug': source_slug,
            'target_slug': target_slug,
            'edge_type': 'IN_LAW_OF',
            'evidence_snippet': evidence_paragraph[:200],
            'evidence_section': source_section,
            'evidence_paragraph_index': evidence_paragraph_index,
            'confidence_tier': 1,
        }

    if 'nephew' in evidence_lower and 'NEPHEW_OF' in valid_edge_types:
        return {
            'decision': 'emit_edge',
            'candidate_kind': 'source_target',
            'evidence_kind': 'wiki-entity',
            'source_slug': source_slug,
            'target_slug': target_slug,
            'edge_type': 'NEPHEW_OF',
            'evidence_snippet': evidence_paragraph[:200],
            'evidence_section': source_section,
            'evidence_paragraph_index': evidence_paragraph_index,
            'confidence_tier': 1,
        }

    # Spatial relationships
    if target_type in ['place.location', 'place.region']:
        if 'in ' in evidence_lower or 'at ' in evidence_lower:
            if 'LOCATED_AT' in valid_edge_types:
                return {
                    'decision': 'emit_edge',
                    'candidate_kind': 'source_target',
                    'evidence_kind': 'wiki-entity',
                    'source_slug': source_slug,
                    'target_slug': target_slug,
                    'edge_type': 'LOCATED_AT',
                    'evidence_snippet': evidence_paragraph[:200],
                    'evidence_section': source_section,
                    'evidence_paragraph_index': evidence_paragraph_index,
                    'confidence_tier': 2,
                }

    # Event relationships
    if target_type == 'event.battle':
        if 'attends' in evidence_lower and 'ATTENDS' in valid_edge_types:
            return {
                'decision': 'emit_edge',
                'candidate_kind': 'source_target',
                'evidence_kind': 'wiki-entity',
                'source_slug': source_slug,
                'target_slug': target_slug,
                'edge_type': 'ATTENDS',
                'evidence_snippet': evidence_paragraph[:200],
                'evidence_section': source_section,
                'evidence_paragraph_index': evidence_paragraph_index,
                'confidence_tier': 2,
            }
        elif 'FIGHTS_IN' in valid_edge_types:
            return {
                'decision': 'emit_edge',
                'candidate_kind': 'source_target',
                'evidence_kind': 'wiki-entity',
                'source_slug': source_slug,
                'target_slug': target_slug,
                'edge_type': 'FIGHTS_IN',
                'evidence_snippet': evidence_paragraph[:200],
                'evidence_section': source_section,
                'evidence_paragraph_index': evidence_paragraph_index,
                'confidence_tier': 2,
            }

    # Temporal relationships or mentions without clear edge type
    return {
        'decision': 'reject_just_mention',
        'candidate_kind': 'source_target',
        'source_slug': source_slug,
        'target_slug': target_slug,
        'reason': 'temporal-cooccurrence-not-relational',
    }


def process_candidate_file(input_path, output_path):
    """Process a single candidate file and write edges."""

    with open(input_path) as f:
        candidates = [json.loads(line) for line in f if line.strip()]

    # Create output directory
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not candidates:
        print(f"No candidates in {input_path.name}")
        return 0

    with open(output_path, 'w') as f:
        for candidate in candidates:
            decision = classify_candidate(candidate)
            f.write(json.dumps(decision) + '\n')

    print(f"[done] {input_path.name} → {len(candidates)} candidates classified → {output_path.name}")
    return len(candidates)


def main():
    base_dir = Path('/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-frey-m-t')
    candidates_dir = base_dir / 'prose-edge-candidates-enriched'
    output_dir = base_dir / 'prose-edges-haiku'

    files = [
        'raymund-frey.candidates.jsonl',
        'rhaegar-frey.candidates.jsonl',
        'robert-frey-son-of-raymund.candidates.jsonl',
        'ronel-rivers.candidates.jsonl',
        'roslin-frey.candidates.jsonl',
    ]

    total = 0
    for filename in files:
        input_path = candidates_dir / filename
        output_filename = filename.replace('.candidates.jsonl', '.edges.jsonl')
        output_path = output_dir / output_filename

        if input_path.exists():
            count = process_candidate_file(input_path, output_path)
            total += count

    print(f"\nTotal: {total} candidates classified")


if __name__ == '__main__':
    main()
