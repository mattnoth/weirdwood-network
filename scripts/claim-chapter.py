#!/usr/bin/env python3
"""Atomically claim a chapter for extraction.

Called while the CSV lock (mkdir lockdir) is held by the caller.

Usage:
  claim-chapter.py <stats_file> <chapter> <wave> <timestamp> <terminal_id> <book>

Prints one of:
  claim              — chapter was free; started row appended to CSV
  claim-after-stale  — stale claim cleared; started row appended
  skip-already-done  — latest row for chapter+wave is done/skipped-done
  skip-claimed:<tid> — active claim held by <tid> (not stale)
"""

import sys
import csv
import os
from datetime import datetime, timezone

NEW_FIELDS = [
    'chapter', 'book', 'wave', 'status', 'start_time', 'end_time', 'duration_s',
    'input_tokens', 'cache_creation_tokens', 'cache_read_tokens',
    'output_tokens', 'total_tokens', 'cost_usd',
    'last_heartbeat', 'terminal_id', 'retry_at',
]

STALE_HEARTBEAT_SECS = 90    # 3 missed heartbeats (heartbeat every 30s)
STALE_NO_HEARTBEAT_SECS = 1800  # 30 min without any heartbeat


def parse_dt(s):
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s.replace('Z', '+00:00'))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def main():
    stats_file, ch, wave, now, terminal_id, book = sys.argv[1:7]

    try:
        with open(stats_file) as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames or NEW_FIELDS)
            rows = list(reader)
    except FileNotFoundError:
        rows = []
        fieldnames = NEW_FIELDS

    # Find the latest row for this chapter+wave
    latest = None
    for row in rows:
        if row.get('chapter') == ch and str(row.get('wave')) == wave:
            latest = row

    status = latest.get('status', '') if latest else ''

    if status in ('done', 'skipped-done'):
        print('skip-already-done')
        return

    if status in ('started', 'working'):
        hb  = (latest or {}).get('last_heartbeat', '')
        st  = (latest or {}).get('start_time', '')
        tid = (latest or {}).get('terminal_id', 'unknown')
        now_dt = datetime.now(timezone.utc)
        stale = False

        hb_dt = parse_dt(hb)
        if hb_dt is not None:
            stale = (now_dt - hb_dt).total_seconds() > STALE_HEARTBEAT_SECS
        else:
            st_dt = parse_dt(st)
            if st_dt is not None:
                stale = (now_dt - st_dt).total_seconds() > STALE_NO_HEARTBEAT_SECS

        if not stale:
            print(f'skip-claimed:{tid}')
            return

        # Stale — mark existing started/working rows as failed-stale then claim
        for row in rows:
            if (row.get('chapter') == ch and str(row.get('wave')) == wave
                    and row.get('status') in ('started', 'working')):
                row['status'] = 'failed-stale'
        tmp = stats_file + '.claimtmp'
        with open(tmp, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)
        os.replace(tmp, stats_file)
        action = 'claim-after-stale'
    else:
        action = 'claim'

    # Append the 'started' row for this terminal
    blank = {k: '' for k in fieldnames}
    blank.update({
        'chapter': ch, 'book': book, 'wave': wave, 'status': 'started',
        'start_time': now, 'last_heartbeat': now, 'terminal_id': terminal_id,
    })
    with open(stats_file, 'a') as f:
        f.write(','.join(str(blank.get(k, '')) for k in fieldnames) + '\n')
    print(action)


if __name__ == '__main__':
    main()
