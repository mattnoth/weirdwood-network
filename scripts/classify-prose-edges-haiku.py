#!/usr/bin/env python3
"""
Stage 4 prose-edge classifier - careful classification with better validation.
"""

import json
import os
import re

def classify_candidate(src, tgt, tgt_type, evidence, valid_types, section):
    """Classify by carefully matching evidence to target."""

    valid = set(valid_types)
    ev_lower = evidence.lower()
    tgt_name = tgt.replace('-', ' ')  # Convert slug to name

    # Strict check: is the target actually about this candidate?
    # The evidence should mention the target explicitly or discuss the relationship clearly

    # === REJECT: MATERIAL, TITLE, CONCEPT MENTIONS ===
    if tgt_type == 'object.material':
        return reject("material-mention-not-relational")
    if tgt_type == 'title':
        return reject("title-mention-not-relational")
    if tgt_type.startswith('concept.'):
        return reject("concept-mention-not-relational")

    # === EMIT: Clear relationship markers ===

    # SIBLING_OF: explicit "her/his brother/sister" describing the target as the source's sibling
    if tgt_type == 'character.human':
        # Must match at the START of the evidence or very early (within first 200 chars)
        # This assumes the most immediate sibling reference is the main relationship
        first_part = evidence[:300]  # Only search first part of evidence

        first_name = tgt_name.split()[0] if ' ' in tgt_name else tgt_name

        sibling_pattern = r'(her|his|their)\s+([a-z]+\s+)*(brother|sister)[^.]{0,100}?«' + re.escape(tgt_name.replace('-', ' ')) + r'»'
        sibling_pattern_short = r'(her|his|their)\s+([a-z]+\s+)*(brother|sister)[^.]{0,100}?«' + re.escape(first_name.capitalize()) + r'»'

        if re.search(sibling_pattern, first_part, re.IGNORECASE) or re.search(sibling_pattern_short, first_part):
            if 'SIBLING_OF' in valid:
                return emit("SIBLING_OF", evidence, section, tier=1)

        # SERVES: "in the service of" + target name mentioned after
        service_pattern = r'in the service of[^.]*«' + re.escape(tgt_name) + r'»'
        if re.search(service_pattern, evidence, re.IGNORECASE):
            if 'SERVES' in valid:
                return emit("SERVES", evidence, section, tier=1)

        # PROTECTS: "protects" + specific target (e.g., "Meera protects Rickon")
        # Look for "protects" followed eventually by the target name
        if 'protects' in ev_lower:
            protect_pattern = r'protects[^.]*' + re.escape(tgt_name)
            if re.search(protect_pattern, evidence, re.IGNORECASE):
                if 'PROTECTS' in valid:
                    return emit("PROTECTS", evidence, section, tier=2)

        # DREAMS_OF: source dreams about target
        # "Bran dreams of..." or "dreamed of..."
        if any(x in ev_lower for x in ['dreamed of', 'dreams of', 'dreaming of']):
            # Make sure target is mentioned as the dream subject
            dream_pattern = r'dream[s]* of[^.]*«' + re.escape(tgt_name) + r'»'
            if re.search(dream_pattern, evidence, re.IGNORECASE):
                if 'DREAMS_OF' in valid:
                    return emit("DREAMS_OF", evidence, section, tier=2)

    # === LOCATIONS ===
    if tgt_type in ['place.location', 'place.region']:
        # Source "arrives at" / "stays at" target location
        location_pattern = r'(arrived|arrived at|stays at|stay|remain)[^.]*«' + re.escape(tgt_name) + r'»'
        if re.search(location_pattern, evidence, re.IGNORECASE):
            if 'LOCATED_AT' in valid:
                return emit("LOCATED_AT", evidence, section, tier=2)

    # === EVENTS ===
    if tgt_type.startswith('event.'):
        # "participated in" + event name
        participate_pattern = r'(participated in|participat)[^.]*«' + re.escape(tgt_name.replace('-', ' ')) + r'»'
        if re.search(participate_pattern, evidence, re.IGNORECASE):
            if tgt_type == 'event.tournament' and 'FIGHTS_IN' in valid:
                return emit("FIGHTS_IN", evidence, section, tier=1)
            elif 'PARTICIPATES_IN' in valid:
                return emit("PARTICIPATES_IN", evidence, section, tier=2)

        # "grand melee" + target tournament event
        if 'grand melee' in ev_lower and 'tournament' in tgt:
            if 'FIGHTS_IN' in valid:
                return emit("FIGHTS_IN", evidence, section, tier=1)
            elif 'ATTENDS' in valid:
                return emit("ATTENDS", evidence, section, tier=2)

    # === DEFAULT ===
    return reject("no-fitting-type-vocab-locked")


def emit(edge_type, evidence, section, tier=1):
    """Return an emit_edge decision."""
    snippet = evidence[:140] if len(evidence) > 140 else evidence
    return {
        "decision": "emit_edge",
        "candidate_kind": "source_target",
        "evidence_kind": "wiki-entity",
        "edge_type": edge_type,
        "evidence_snippet": snippet,
        "evidence_section": section,
        "evidence_paragraph_index": 0,
        "confidence_tier": tier
    }


def reject(reason):
    """Return a reject_just_mention decision."""
    return {
        "decision": "reject_just_mention",
        "candidate_kind": "source_target",
        "reason": reason
    }


def process_file(input_path, output_path):
    """Process all candidates in input file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(input_path) as f_in, open(output_path, 'w') as f_out:
        for line in f_in:
            if not line.strip():
                continue

            candidate = json.loads(line)
            src = candidate['source_slug']
            tgt = candidate['target_slug']
            tgt_type = candidate.get('target_type', '')
            evidence = candidate.get('evidence_paragraph', '')
            valid_types = candidate.get('valid_edge_types', [])
            section = candidate.get('source_section', '## Unknown')

            # Classify
            decision = classify_candidate(src, tgt, tgt_type, evidence, valid_types, section)

            # Add source/target to all decisions
            decision['source_slug'] = src
            decision['target_slug'] = tgt

            # Write
            f_out.write(json.dumps(decision) + '\n')


if __name__ == '__main__':
    files = [
        ("working/wiki/pass2-buckets/characters-house-reed/prose-edge-candidates-enriched/howland-reed.candidates.jsonl",
         "working/wiki/pass2-buckets/characters-house-reed/prose-edges-haiku/howland-reed.edges.jsonl"),
        ("working/wiki/pass2-buckets/characters-house-reed/prose-edge-candidates-enriched/jojen-reed.candidates.jsonl",
         "working/wiki/pass2-buckets/characters-house-reed/prose-edges-haiku/jojen-reed.edges.jsonl"),
        ("working/wiki/pass2-buckets/characters-house-reed/prose-edge-candidates-enriched/meera-reed.candidates.jsonl",
         "working/wiki/pass2-buckets/characters-house-reed/prose-edges-haiku/meera-reed.edges.jsonl"),
        ("working/wiki/pass2-buckets/characters-house-reyaan/prose-edge-candidates-enriched/bessaro-reyaan.candidates.jsonl",
         "working/wiki/pass2-buckets/characters-house-reyaan/prose-edges-haiku/bessaro-reyaan.edges.jsonl"),
        ("working/wiki/pass2-buckets/characters-house-reyne/prose-edge-candidates-enriched/alastor-reyne.candidates.jsonl",
         "working/wiki/pass2-buckets/characters-house-reyne/prose-edges-haiku/alastor-reyne.edges.jsonl"),
    ]

    for input_path, output_path in files:
        process_file(input_path, output_path)
        basename = input_path.split('/')[-1]
        output_name = output_path.split('/')[-1]
        print(f"[done] {basename} → {output_name}")
