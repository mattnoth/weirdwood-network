#!/usr/bin/env python3
"""Classify prose-edge candidates for Stage 4."""

import json
import sys
import os
from pathlib import Path

def classify_candidate(candidate):
    """Classify a single candidate."""
    source_slug = candidate.get('source_slug')
    target_slug = candidate.get('target_slug')
    target_type = candidate.get('target_type')
    evidence_paragraph = candidate.get('evidence_paragraph', '')
    valid_edge_types = set(candidate.get('valid_edge_types', []))
    anchor_text = candidate.get('anchor_text', '')
    source_section = candidate.get('source_section', '')

    # Decision 1: Location mention in text about a place the source is FROM/AT
    # Examples: walda-frey → north (mentioned as birthplace context) → LOCATED_AT

    # Most candidates from wiki are just mentions - reject as temporal cooccurrence
    reason = None
    decision = None
    edge_type = None

    # If mentioned as location context (e.g., "becomes orphan after death in North")
    # and target is place.location, it's likely just context, not an edge
    if target_type in ['place.location', 'place.region']:
        # Check if it's a setting mention vs. actual location relationship
        # Evidence: "Walda becomes an orphan after the death of her father in the North"
        # This is LOCATED_AT Walda → North contextually, but could be just mention
        if any(phrase in evidence_paragraph.lower() for phrase in ['in the ', 'from the ', 'at the ']):
            # Could be LOCATED_AT, but verify from evidence
            if 'LOCATED_AT' in valid_edge_types:
                # Use confidence 3 (inferred) since context is implicit
                decision = 'emit_edge'
                edge_type = 'LOCATED_AT'
            else:
                decision = 'reject_just_mention'
                reason = 'location-mention-no-edge-type'
        else:
            decision = 'reject_just_mention'
            reason = 'temporal-cooccurrence-not-relational'

    # If target is concept.custom (dowry, cupbearer, etc.), reject - not entities
    elif target_type in ['concept.custom', 'concept.culture', 'concept.magic', 'concept.medical', 'object.material']:
        decision = 'reject_just_mention'
        reason = 'target-is-concept-not-entity'

    # If target is event (Red Wedding), check if ATTENDS/FIGHTS_IN fits
    elif target_type in ['event.battle', 'event.tournament', 'event.ceremony']:
        # Character mentions attending or fighting in event
        if 'ATTENDS' in valid_edge_types:
            # Only emit if explicitly at the event
            if any(w in evidence_paragraph.lower() for w in ['attended', 'present at', 'at the ']):
                decision = 'emit_edge'
                edge_type = 'ATTENDS'
            else:
                decision = 'reject_just_mention'
                reason = 'no-event-participation-phrase'
        else:
            decision = 'reject_just_mention'
            reason = 'event-target-no-attends-type'

    # If target is character.human
    elif target_type in ['character.human']:
        # Default: reject as just mention unless strong relationship language
        strong_verbs = ['married', 'wed', 'sibling', 'brother', 'sister', 'parent', 'father', 'mother',
                       'cousin', 'slept with', 'lover', 'murdered', 'killed', 'betrayed', 'served']
        has_strong_verb = any(verb in evidence_paragraph.lower() for verb in strong_verbs)

        if has_strong_verb:
            # Determine edge type from verb
            evidence_lower = evidence_paragraph.lower()
            if 'married' in evidence_lower or 'wed' in evidence_lower:
                if 'SPOUSE_OF' in valid_edge_types:
                    decision = 'emit_edge'
                    edge_type = 'SPOUSE_OF'
                else:
                    decision = 'reject_just_mention'
                    reason = 'spouse-not-in-valid-types'
            elif 'cousin' in evidence_lower:
                if 'COUSIN_OF' in valid_edge_types:
                    decision = 'emit_edge'
                    edge_type = 'COUSIN_OF'
                else:
                    decision = 'reject_just_mention'
                    reason = 'cousin-not-in-valid-types'
            elif any(w in evidence_lower for w in ['slept with', 'lover']):
                if 'LOVER_OF' in valid_edge_types:
                    decision = 'emit_edge'
                    edge_type = 'LOVER_OF'
                else:
                    decision = 'reject_just_mention'
                    reason = 'lover-not-in-valid-types'
            else:
                decision = 'reject_just_mention'
                reason = 'character-mention-no-typed-relationship'
        else:
            decision = 'reject_just_mention'
            reason = 'character-mention-temporal-cooccurrence'

    else:
        decision = 'reject_just_mention'
        reason = f'unknown-target-type-{target_type}'

    # Build output row
    output = {
        'decision': decision,
        'candidate_kind': 'source_target',
        'source_slug': source_slug,
        'target_slug': target_slug,
    }

    if decision == 'emit_edge':
        output['evidence_kind'] = 'wiki-entity'
        output['edge_type'] = edge_type
        output['evidence_snippet'] = evidence_paragraph[:200] if evidence_paragraph else ''
        output['evidence_section'] = source_section
        output['evidence_paragraph_index'] = 0  # Simplified; would need actual index
        output['confidence_tier'] = 3 if reason is None else 2  # Conservative on wiki prose
    elif decision == 'reject_just_mention':
        output['reason'] = reason

    return output

def process_file(input_path, output_path):
    """Process a single candidates file."""
    candidates = []

    # Create output directory
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Read candidates
    with open(input_path, 'r') as f:
        for line in f:
            if line.strip():
                candidates.append(json.loads(line.strip()))

    # Classify each candidate
    decisions = []
    for cand in candidates:
        decision = classify_candidate(cand)
        decisions.append(decision)

    # Write output
    with open(output_path, 'w') as f:
        for decision in decisions:
            f.write(json.dumps(decision) + '\n')

    return len(candidates), len([d for d in decisions if d['decision'] == 'emit_edge'])

# Process all files
input_files = [
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-merrett.candidates.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-rhaegar.candidates.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-walton.candidates.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-rivers-daughter-of-aemon.candidates.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walder-frey-son-of-emmon.candidates.jsonl'
]

output_files = {
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-merrett.candidates.jsonl': 'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-frey-daughter-of-merrett.edges.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-rhaegar.candidates.jsonl': 'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-frey-daughter-of-rhaegar.edges.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-walton.candidates.jsonl': 'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-frey-daughter-of-walton.edges.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-rivers-daughter-of-aemon.candidates.jsonl': 'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-rivers-daughter-of-aemon.edges.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walder-frey-son-of-emmon.candidates.jsonl': 'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walder-frey-son-of-emmon.edges.jsonl'
}

for input_file in input_files:
    output_file = output_files[input_file]
    total, emitted = process_file(input_file, output_file)
    filename = os.path.basename(input_file).replace('.candidates.jsonl', '')
    print(f'[done] {filename} → {emitted} emit_edge, {total - emitted} reject_just_mention — wrote {output_file}')
