#!/usr/bin/env python3
"""Stream Claude assistant output to stderr during extraction.

Reads stream-json from stdin (via tee), prints assistant text blocks
to stderr with a │ prefix so they appear inside the [2/3] Extracting
section without polluting the captured stdout JSON.
"""

import json
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        continue
    t = obj.get('type')
    if t == 'assistant' and 'message' in obj:
        for block in obj['message'].get('content', []):
            if block.get('type') == 'text':
                for chunk in block['text'].splitlines():
                    print(f'  │ {chunk}', file=sys.stderr, flush=True)
            elif block.get('type') == 'tool_use':
                print(f'  │ [tool_use: {block.get("name")}]',
                      file=sys.stderr, flush=True)
