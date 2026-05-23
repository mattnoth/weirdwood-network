#!/usr/bin/env python3
"""Classify prose-edge candidates correctly."""

import json
import os

def emit_edge(source_slug, target_slug, edge_type, evidence_paragraph, evidence_section, confidence_tier=1, qualifier=None):
    """Create an emit_edge decision."""
    output = {
        'decision': 'emit_edge',
        'candidate_kind': 'source_target',
        'evidence_kind': 'wiki-entity',
        'source_slug': source_slug,
        'target_slug': target_slug,
        'edge_type': edge_type,
        'evidence_snippet': (evidence_paragraph[:150] + '...') if len(evidence_paragraph) > 150 else evidence_paragraph,
        'evidence_section': evidence_section,
        'evidence_paragraph_index': 0,
        'confidence_tier': confidence_tier
    }
    if qualifier:
        output['qualifier'] = qualifier
    return output

def reject_mention(source_slug, target_slug, reason):
    """Create a reject_just_mention decision."""
    return {
        'decision': 'reject_just_mention',
        'candidate_kind': 'source_target',
        'source_slug': source_slug,
        'target_slug': target_slug,
        'reason': reason
    }

def classify(candidate):
    """Classify one candidate."""
    source = candidate.get('source_slug')
    target = candidate.get('target_slug')
    target_type = candidate.get('target_type', '')
    evidence = candidate.get('evidence_paragraph', '')
    section = candidate.get('source_section', '')
    valid_types = set(candidate.get('valid_edge_types', []))
    anchor = candidate.get('anchor_text', '')

    # Special cases based on observed patterns

    # COUSIN_OF: explicitly mentioned by name as cousin
    if 'COUSIN_OF' in valid_types and any(w in evidence.lower() for w in ['cousin', 'cousins']):
        return emit_edge(source, target, 'COUSIN_OF', evidence, section)

    # SPOUSE_OF: married/wed explicitly mentioned
    if 'SPOUSE_OF' in valid_types and any(w in evidence.lower() for w in ['married', 'wed', 'weds', 'spouse']):
        # Determine qualifier from evidence
        qual = 'unknown'
        if 'former' in evidence.lower() or 'widow' in evidence.lower():
            qual = 'former'
        elif 'widowed' in evidence.lower():
            qual = 'widowed'
        return emit_edge(source, target, 'SPOUSE_OF', evidence, section, qualifier=qual)

    # LOVER_OF: slept with, affair, etc
    if 'LOVER_OF' in valid_types and any(w in evidence.lower() for w in ['slept with', 'lover', 'affair']):
        return emit_edge(source, target, 'LOVER_OF', evidence, section)

    # LOCATED_AT: location reference for position (page, squire at location)
    if target_type in ['place.location']:
        if any(w in evidence.lower() for w in [' at ', ' page ', ' squire ', ' lord of ', ' lady of ']):
            if 'LOCATED_AT' in valid_types:
                return emit_edge(source, target, 'LOCATED_AT', evidence, section, confidence_tier=2)

    # ATTENDS: attending event/wedding explicitly
    if target_type in ['event.battle', 'event.ceremony', 'event.tournament']:
        if 'ATTENDS' in valid_types:
            if any(w in evidence.lower() for w in [' at the ', ' wedding', ' feast', ' attended', 'seated at']):
                return emit_edge(source, target, 'ATTENDS', evidence, section, confidence_tier=2)
        # Reject: at event but not explicitly attending
        return reject_mention(source, target, 'event-mention-no-attendance-evidence')

    # Default: character/concept mentions are just mentions
    if target_type in ['character.human']:
        # Check for strong relationship indicators that weren't caught above
        if any(w in evidence.lower() for w in ['father', 'mother', 'parent', 'brother', 'sister', 'sibling', 'father of', 'daughter of', 'son of']):
            # Family relationships should have been handled by another pass
            return reject_mention(source, target, 'family-relationship-complex')
        # Generic co-mention
        return reject_mention(source, target, 'character-temporal-cooccurrence')

    # Location/region mentions are usually just context
    if target_type in ['place.location', 'place.region']:
        if 'LOCATED_AT' not in valid_types:
            return reject_mention(source, target, 'location-mention-not-located-at')
        # If LOCATED_AT is valid but no explicit position language, reject
        if not any(w in evidence.lower() for w in [' at ', ' in the ', ' in ', ' located']):
            return reject_mention(source, target, 'location-mention-no-position-verb')

    # Concepts/customs are not entities
    if target_type in ['concept.custom', 'concept.culture', 'object.material']:
        return reject_mention(source, target, 'target-not-entity')

    # Default rejection
    return reject_mention(source, target, 'no-relationship-found')

def process_file(input_path, output_path):
    """Process one candidates file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    decisions = []
    with open(input_path, 'r') as f:
        for line in f:
            if line.strip():
                cand = json.loads(line.strip())
                dec = classify(cand)
                decisions.append(dec)

    with open(output_path, 'w') as f:
        for dec in decisions:
            f.write(json.dumps(dec) + '\n')

    return len(decisions), sum(1 for d in decisions if d['decision'] == 'emit_edge')

# Process all files
files = {
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-merrett.candidates.jsonl':
        'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-frey-daughter-of-merrett.edges.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-rhaegar.candidates.jsonl':
        'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-frey-daughter-of-rhaegar.edges.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-walton.candidates.jsonl':
        'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-frey-daughter-of-walton.edges.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-rivers-daughter-of-aemon.candidates.jsonl':
        'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-rivers-daughter-of-aemon.edges.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walder-frey-son-of-emmon.candidates.jsonl':
        'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walder-frey-son-of-emmon.edges.jsonl'
}

for inp, out in files.items():
    total, emitted = process_file(inp, out)
    fname = os.path.basename(inp).replace('.candidates.jsonl', '')
    rejected = total - emitted
    print(f'[done] {fname} → {emitted} emit_edge, {rejected} reject_just_mention — wrote {out}')
