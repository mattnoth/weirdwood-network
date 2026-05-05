#!/usr/bin/env python3
"""Migrate extraction-stats CSV from old schema to new schema.

Old schema (13 cols): chapter,book,wave,status,start_time,end_time,duration_s,
  input_tokens,cache_creation_tokens,cache_read_tokens,output_tokens,total_tokens,cost_usd

New schema (16 cols): adds last_heartbeat,terminal_id,retry_at

Status value migration:
  ok                -> done
  fail              -> failed-error
  skip-done         -> skipped-done
  skip-no-source    -> skipped-no-source
  skip-rate-limit   -> failed-rate

Writes a .bak backup the first time (never overwrites an existing backup).
Uses tempfile + os.replace for atomic writes.
"""

import sys
import csv
import os
import shutil

STATUS_MAP = {
    'ok': 'done',
    'fail': 'failed-error',
    'skip-done': 'skipped-done',
    'skip-no-source': 'skipped-no-source',
    'skip-rate-limit': 'failed-rate',
}

NEW_FIELDNAMES = [
    'chapter', 'book', 'wave', 'status', 'start_time', 'end_time', 'duration_s',
    'input_tokens', 'cache_creation_tokens', 'cache_read_tokens',
    'output_tokens', 'total_tokens', 'cost_usd',
    'last_heartbeat', 'terminal_id', 'retry_at',
]


def migrate(stats_file):
    if not os.path.exists(stats_file):
        return

    with open(stats_file) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        if 'last_heartbeat' in fieldnames:
            print(f"Already migrated: {stats_file}", flush=True)
            return
        rows = list(reader)

    bak = stats_file + '.bak'
    if not os.path.exists(bak):
        shutil.copy2(stats_file, bak)
        print(f"Backup: {bak}", flush=True)

    new_rows = []
    for row in rows:
        new_row = {k: row.get(k, '') for k in NEW_FIELDNAMES}
        old_status = new_row.get('status', '')
        new_row['status'] = STATUS_MAP.get(old_status, old_status)
        new_rows.append(new_row)

    tmp = stats_file + '.migrating'
    with open(tmp, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=NEW_FIELDNAMES)
        writer.writeheader()
        writer.writerows(new_rows)
    os.replace(tmp, stats_file)
    print(f"Migrated {len(new_rows)} rows: {stats_file}", flush=True)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <stats_file>", file=sys.stderr)
        sys.exit(1)
    migrate(sys.argv[1])
