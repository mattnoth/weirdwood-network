#!/usr/bin/env python3
"""Validate historical-anchor candidate edges before mint.
Checks: JSON parse, slug resolution (any node dir), book quotes verbatim in chapter,
wiki quotes verbatim in hub node body OR raw wiki cache json. Read-only.
"""
import json, glob, os, re
from pathlib import Path

ROOT = Path('.')
ALL_SLUGS = {p.stem.replace('.node', '') for p in ROOT.glob('graph/nodes/**/*.node.md')}
RAW = ROOT / 'sources/wiki/_raw'


def norm(x):
    x = (x.replace('’', "'").replace('‘', "'")
          .replace('“', '"').replace('”', '"')
          .replace('—', '-').replace('–', '-')
          .replace('\xa0', ' '))
    # strip wiki-link markup [text](wiki:Foo) -> text, and bare (wiki:...) cite refs
    x = re.sub(r'\[([^\]]+)\]\(wiki:[^)]*\)', r'\1', x)
    x = re.sub(r'\(wiki:[^)]*\)', '', x)
    x = re.sub(r'<[^>]+>', '', x)          # strip any html tags (raw json)
    x = re.sub(r'\s+', ' ', x)             # collapse whitespace
    return x


def norm_q(x):
    return norm(x)


def main():
    rows = []
    issues = []
    for fpath in sorted(glob.glob('working/historical-anchor/*.candidates.jsonl')):
        hub = os.path.basename(fpath).replace('.candidates.jsonl', '')
        node_body = ''
        nf = ROOT / f'graph/nodes/events/{hub}.node.md'
        if nf.exists():
            node_body = norm(nf.read_text(encoding='utf-8', errors='replace'))
        for i, line in enumerate(open(fpath, encoding='utf-8'), 1):
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except Exception as ex:
                issues.append((hub, i, 'PARSE', str(ex)))
                continue
            rows.append((hub, i, e))
            s, t = e.get('source_slug'), e.get('target_slug')
            if s not in ALL_SLUGS:
                issues.append((hub, i, 'SLUG-SRC', s))
            if t not in ALL_SLUGS:
                issues.append((hub, i, 'SLUG-TGT', t))
            q = norm(e.get('evidence_quote', '') or '')[:80]
            ek = e.get('evidence_kind')
            ref = e.get('evidence_ref', '')
            if not q:
                issues.append((hub, i, 'EMPTY-QUOTE', e.get('edge_type')))
                continue
            if ek == 'book-pass1':
                fp = ref.split(':')[0] if ref.startswith('sources/') else None
                if not fp or not os.path.exists(fp):
                    issues.append((hub, i, 'BAD-REF', ref))
                elif q not in norm(open(fp, encoding='utf-8', errors='replace').read()):
                    issues.append((hub, i, 'QUOTE-NOT-IN-CHAPTER', f'{ref} :: {q[:50]}'))
            elif ek == 'wiki-historical-anchor':
                # verbatim in node body OR raw wiki json
                page = ref.replace('wiki:', '') if ref.startswith('wiki:') else None
                found = q in node_body
                if not found and page:
                    jf = RAW / f'{page}.json'
                    if jf.exists():
                        found = q in norm(jf.read_text(encoding='utf-8', errors='replace'))
                if not found:
                    issues.append((hub, i, 'WIKI-QUOTE-NOT-VERBATIM', f'{ref} :: {q[:50]}'))
            else:
                issues.append((hub, i, 'BAD-EVIDENCE-KIND', ek))

    from collections import Counter
    print(f"TOTAL edges: {len(rows)}   ISSUES: {len(issues)}\n")
    for x in issues:
        print('  ', x)
    print('\nedge types:', dict(Counter(e['edge_type'] for _, _, e in rows)))
    print('provenance:', dict(Counter(e['evidence_kind'] for _, _, e in rows)))
    print('tiers:', dict(Counter(e.get('confidence_tier') for _, _, e in rows)))
    print('per-hub:', dict(Counter(h for h, _, _ in rows)))


if __name__ == '__main__':
    main()
