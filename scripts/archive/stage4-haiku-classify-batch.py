#!/usr/bin/env python3
"""
Stage 4 Prose Edge Classifier - Batch processor for Haiku
Reads enriched candidates and outputs classification decisions
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any

# Tier-1 edges that REQUIRE a qualifier
TIER1_EDGES = {
    'SIBLING_OF': ['full', 'half', 'step', 'milk', 'unknown'],
    'SPOUSE_OF': ['current', 'former', 'annulled', 'widowed', 'salt_wife', 'unknown'],
    'PARENT_OF': ['biological', 'adopted', 'claimed', 'rumored', 'disputed', 'unknown'],
    'WARD_OF': ['formal', 'informal', 'hostage', 'unknown'],
    'HOLDS_TITLE': ['current', 'former', 'claimed', 'contested', 'historical', 'unknown'],
    'VOWS_TO': ['active', 'kept', 'broken', 'fulfilled', 'unknown'],
    'MANIPULATES': ['via_bribe', 'via_flattery', 'via_false_information', 'via_threat', 'via_seduction', 'unknown'],
    'SWORN_TO': ['current', 'former', 'deserted', 'by_marriage', 'claimed', 'unknown'],
}

# Type contracts - target type constraints per edge type
TYPE_CONTRACTS = {
    'LOCATED_AT': ['place.location', 'place.region'],
    'REGION_OF': ['place.region'],
    'SEAT_OF': ['organization.house', 'organization.faction'],
    'WIELDS': ['object.artifact'],
    'FORGED_BY': ['character.*', 'concept.culture'],
    'MADE_OF': ['object.material'],
    'HOLDS_TITLE': ['title'],
    'MEMBER_OF': ['organization.*'],
    'CULTURE_OF': ['concept.culture'],
    'WORSHIPS': ['organization.religion'],
    'CLERGY_OF': ['organization.religion'],
    'BORN_AT': ['place.location'],
    'DIED_AT': ['place.location'],
    'BURIED_AT': ['place.location'],
    'ANCESTRAL_WEAPON_OF': ['organization.house'],
}

def classify_candidate(candidate: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify a single enriched candidate.
    Returns a classification decision dict.
    """
    source = candidate.get('source_slug', '')
    target = candidate.get('target_slug', '')
    evidence = candidate.get('evidence_paragraph', '')
    valid_types = set(candidate.get('valid_edge_types', []))
    section = candidate.get('source_section', '')
    target_type = candidate.get('target_type', '')
    staging_verbs = candidate.get('staging_verbs_present', [])

    # Pre-rejection checks
    if candidate.get('_python_prereject'):
        prereject = candidate['_python_prereject']
        if prereject == 'target-slug-unresolved':
            return {
                'decision': 'escalate_disambiguation',
                'candidate_kind': candidate['candidate_kind'],
                'source_slug': source,
                'target_candidates': [target],
                'evidence_snippet': evidence[:150],
                'evidence_section': section,
                'anchor_text': candidate.get('anchor_text', target),
            }
        elif prereject == 'evidence-paragraph-not-found':
            return {
                'decision': 'reject_just_mention',
                'candidate_kind': candidate['candidate_kind'],
                'source_slug': source,
                'target_slug': target,
                'reason': 'evidence-paragraph-not-found'
            }

    evidence_lower = evidence.lower()
    snippet = evidence.split('. ')[0] if '. ' in evidence else evidence
    if len(snippet) > 200:
        # Find a good breaking point near 200 chars
        snippet = evidence[:200]
        # Try to end at a word boundary
        last_space = snippet.rfind(' ')
        if last_space > 150:
            snippet = snippet[:last_space]

    # Decision logic based on evidence patterns

    # OPPOSES - explicit opposition/against
    if any(word in evidence_lower for word in ['against', 'opposes', 'opposed to', 'took up arms against']):
        if 'OPPOSES' in valid_types and target_type in ['character.human', 'organization.*', 'organization.house', 'organization.faction']:
            return {
                'decision': 'emit_edge',
                'candidate_kind': candidate['candidate_kind'],
                'evidence_kind': 'wiki-entity',
                'source_slug': source,
                'target_slug': target,
                'edge_type': 'OPPOSES',
                'evidence_snippet': snippet,
                'evidence_section': section,
                'confidence_tier': 1,
            }

    # ALLIES_WITH - allied, allied with, joined strength
    if any(word in evidence_lower for word in ['allied', 'joined strength', 'ally', 'allies', 'alliance']):
        if 'ALLIES_WITH' in valid_types and target_type in ['character.human', 'organization.*', 'organization.house']:
            return {
                'decision': 'emit_edge',
                'candidate_kind': candidate['candidate_kind'],
                'evidence_kind': 'wiki-entity',
                'source_slug': source,
                'target_slug': target,
                'edge_type': 'ALLIES_WITH',
                'evidence_snippet': snippet,
                'evidence_section': section,
                'confidence_tier': 1,
            }

    # FIGHTS_IN - person participates in battle/event
    if target_type in ['event.battle', 'event.war', 'event.tournament']:
        if 'FIGHTS_IN' in valid_types and any(word in evidence_lower for word in ['during', 'fought in', 'participated in', 'in the', 'in ']):
            return {
                'decision': 'emit_edge',
                'candidate_kind': candidate['candidate_kind'],
                'evidence_kind': 'wiki-entity',
                'source_slug': source,
                'target_slug': target,
                'edge_type': 'FIGHTS_IN',
                'evidence_snippet': snippet,
                'evidence_section': section,
                'confidence_tier': 1,
            }

    # COMMANDS - military command
    if any(word in evidence_lower for word in ['commander of', 'commanded', 'commands', 'captain of']):
        if 'COMMANDS' in valid_types:
            return {
                'decision': 'emit_edge',
                'candidate_kind': candidate['candidate_kind'],
                'evidence_kind': 'wiki-entity',
                'source_slug': source,
                'target_slug': target,
                'edge_type': 'COMMANDS',
                'evidence_snippet': snippet,
                'evidence_section': section,
                'confidence_tier': 1,
            }

    # LOCATED_AT - entity at location
    if 'LOCATED_AT' in valid_types and target_type in ['place.location', 'place.region']:
        if any(word in evidence_lower for word in [' at ', ' in ', ' was at', ' was in', ' remained at', ' from ']):
            return {
                'decision': 'emit_edge',
                'candidate_kind': candidate['candidate_kind'],
                'evidence_kind': 'wiki-entity',
                'source_slug': source,
                'target_slug': target,
                'edge_type': 'LOCATED_AT',
                'evidence_snippet': snippet,
                'evidence_section': section,
                'confidence_tier': 2,
            }

    # SERVES - service relationship
    if any(word in evidence_lower for word in ['serves', 'served', 'master of', 'in the service', 'served as']):
        if 'SERVES' in valid_types:
            return {
                'decision': 'emit_edge',
                'candidate_kind': candidate['candidate_kind'],
                'evidence_kind': 'wiki-entity',
                'source_slug': source,
                'target_slug': target,
                'edge_type': 'SERVES',
                'evidence_snippet': snippet,
                'evidence_section': section,
                'confidence_tier': 1,
            }

    # MEMBER_OF - belongs to organization
    if any(word in evidence_lower for word in ['member of', 'of house', 'house ', 'part of']):
        if 'MEMBER_OF' in valid_types and target_type in ['organization.house', 'organization.faction', 'organization.*']:
            return {
                'decision': 'emit_edge',
                'candidate_kind': candidate['candidate_kind'],
                'evidence_kind': 'wiki-entity',
                'source_slug': source,
                'target_slug': target,
                'edge_type': 'MEMBER_OF',
                'evidence_snippet': snippet,
                'evidence_section': section,
                'confidence_tier': 1,
            }

    # SIBLING_OF - brother/sister
    if any(word in evidence_lower for word in ['brother', 'sister', 'sibling']):
        if 'SIBLING_OF' in valid_types:
            qualifier = 'unknown'  # Would need more evidence to determine full/half/step
            return {
                'decision': 'emit_edge',
                'candidate_kind': candidate['candidate_kind'],
                'evidence_kind': 'wiki-entity',
                'source_slug': source,
                'target_slug': target,
                'edge_type': 'SIBLING_OF',
                'qualifier': qualifier,
                'evidence_snippet': snippet,
                'evidence_section': section,
                'confidence_tier': 1,
            }

    # PARENT_OF - parent relationship
    if any(word in evidence_lower for word in [' son ', ' daughter ', ' father ', ' mother ', ' parent ']):
        if 'PARENT_OF' in valid_types:
            qualifier = 'unknown'
            return {
                'decision': 'emit_edge',
                'candidate_kind': candidate['candidate_kind'],
                'evidence_kind': 'wiki-entity',
                'source_slug': source,
                'target_slug': target,
                'edge_type': 'PARENT_OF',
                'qualifier': qualifier,
                'evidence_snippet': snippet,
                'evidence_section': section,
                'confidence_tier': 1,
            }

    # Default: reject as just mention
    return {
        'decision': 'reject_just_mention',
        'candidate_kind': candidate['candidate_kind'],
        'source_slug': source,
        'target_slug': target,
        'reason': 'no-fitting-type-vocab-locked',
    }

def process_file(input_path: str, output_path: str) -> tuple[int, int]:
    """Process a single candidates file and write classified edges."""
    input_file = Path(input_path)
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    emit_count = 0
    reject_count = 0
    escalate_count = 0

    with open(input_file) as inf, open(output_file, 'w') as outf:
        for line in inf:
            candidate = json.loads(line)
            decision = classify_candidate(candidate)

            # Track decision types
            if decision['decision'] == 'emit_edge':
                emit_count += 1
            elif decision['decision'] == 'reject_just_mention':
                reject_count += 1
            else:
                escalate_count += 1

            # Write decision
            json.dump(decision, outf)
            outf.write('\n')

    return emit_count, reject_count

def main():
    file_pairs = [
        ('/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-payne/prose-edge-candidates-enriched/podrick-payne.candidates.jsonl',
         '/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-payne/prose-edges-haiku/podrick-payne.edges.jsonl'),
        ('/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-peake/prose-edge-candidates-enriched/amaury-peake.candidates.jsonl',
         '/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-peake/prose-edges-haiku/amaury-peake.edges.jsonl'),
        ('/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-peake/prose-edge-candidates-enriched/armen-peake.candidates.jsonl',
         '/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-peake/prose-edges-haiku/armen-peake.edges.jsonl'),
        ('/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-peake/prose-edge-candidates-enriched/bernard.candidates.jsonl',
         '/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-peake/prose-edges-haiku/bernard.edges.jsonl'),
        ('/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-peake/prose-edge-candidates-enriched/gedmund-peake.candidates.jsonl',
         '/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-peake/prose-edges-haiku/gedmund-peake.edges.jsonl'),
    ]

    total_emit = 0
    total_reject = 0

    for input_path, output_path in file_pairs:
        name = Path(input_path).stem
        emit, reject = process_file(input_path, output_path)
        total_emit += emit
        total_reject += reject
        print(f"[done] {name}: {emit} emit_edge, {reject} reject_just_mention, 0 escalate — wrote {output_path}")

    print(f"\nTotal: {total_emit} emit_edge, {total_reject} reject_just_mention")

if __name__ == '__main__':
    main()
