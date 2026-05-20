#!/usr/bin/env bash
# stage4-haiku-smoke-finish.sh — Drive the Haiku worker until batch-0020-haiku-smoke
# is fully classified. The Haiku worker exits early (~3 files/invocation), so this
# re-fires it; the worker's state.jsonl resume-check skips already-done files.
#
# STOPS the instant the smoke batch is `done` — it must never fire a worker that
# would then claim a live-queue batch. Capped at 15 iterations + stuck-detection.

set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

MANIFEST=working/missions/2026-05-14-stage4-v1-bulk-sonnet/batch-manifest.jsonl
STATE=working/missions/2026-05-14-stage4-v1-bulk-sonnet/state.jsonl
WORKER=.claude/commands/worker-stage4.md
COSTLOG=/tmp/haiku-smoke-costs.jsonl
: > "$COSTLOG"

smoke_status() {
  python3 -c "
import json
for l in open('$MANIFEST'):
    if l.strip():
        d=json.loads(l)
        if d.get('batch_id')=='batch-0020-haiku-smoke':
            print(d['status']); break
"
}
files_done() {
  python3 -c "
import json
n=0
for l in open('$STATE'):
    if 'batch-0020-haiku-smoke' in l:
        try:
            if json.loads(l).get('event')=='file_done': n+=1
        except: pass
print(n)
"
}

prev_done=-1
for i in $(seq 1 15); do
  st=$(smoke_status)
  if [[ "$st" == "done" ]]; then
    echo "ITER $i: batch-0020-haiku-smoke is done — stopping."
    break
  fi
  done_now=$(files_done)
  if [[ "$i" -gt 1 && "$done_now" == "$prev_done" ]]; then
    echo "ITER $i: no progress since last iteration ($done_now files done) — stuck, stopping."
    break
  fi
  prev_done=$done_now
  echo "ITER $i: status=$st, ${done_now}/30 files done — firing Haiku worker..."

  claude -p --dangerously-skip-permissions --model claude-haiku-4-5 \
    --verbose --output-format stream-json \
    "$(cat "$WORKER")" > "/tmp/haiku-smoke-iter-$i.jsonl" 2>&1

  python3 -c "
import json
for l in open('/tmp/haiku-smoke-iter-$i.jsonl'):
    l=l.strip()
    if not l: continue
    try:
        o=json.loads(l)
        if o.get('type')=='result':
            print(json.dumps({'iter':$i,'cost_usd':o.get('total_cost_usd'),
                              'dur_ms':o.get('duration_ms'),'is_error':o.get('is_error')}))
    except: pass
" | tee -a "$COSTLOG"
  sleep 5
done

echo
echo "=== Haiku smoke completion run finished ==="
echo "Final smoke-batch status: $(smoke_status)  |  files done: $(files_done)/30"
python3 -c "
import json
rows=[json.loads(l) for l in open('$COSTLOG') if l.strip()]
print(f'Invocations: {len(rows)}  Total cost: \${sum(r[\"cost_usd\"] or 0 for r in rows):.4f}')
"
