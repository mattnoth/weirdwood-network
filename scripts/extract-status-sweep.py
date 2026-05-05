#!/usr/bin/env python3
"""Sweep stale started/working rows in a stats CSV and rewrite them as failed-stale.

Two staleness thresholds (both must be considered):
  --heartbeat-max-age N  (seconds, default 90)
    If last_heartbeat exists and is older than N seconds, the terminal is dead.
    Three missed heartbeats (heartbeat every 30s) = 90s threshold.

  --row-max-age N  (seconds, default 1800)
    If last_heartbeat is absent AND start_time is older than N seconds,
    the terminal died before writing its first heartbeat.

Uses tempfile + os.replace for atomic writes.
"""

import sys
import csv
import os
import argparse
from datetime import datetime, timezone


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


def is_stale(row, heartbeat_max_age, row_max_age):
    now = datetime.now(timezone.utc)
    hb = parse_dt(row.get('last_heartbeat', ''))
    if hb is not None:
        return (now - hb).total_seconds() > heartbeat_max_age
    # No heartbeat — fall back to start_time + row_max_age
    st = parse_dt(row.get('start_time', ''))
    if st is not None:
        return (now - st).total_seconds() > row_max_age
    return False


def sweep(stats_file, heartbeat_max_age, row_max_age):
    if not os.path.exists(stats_file):
        return

    with open(stats_file) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    changed = 0
    for row in rows:
        if row.get('status') in ('started', 'working'):
            if is_stale(row, heartbeat_max_age, row_max_age):
                row['status'] = 'failed-stale'
                changed += 1

    if changed > 0:
        tmp = stats_file + '.sweeptmp'
        with open(tmp, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        os.replace(tmp, stats_file)
        print(f"Sweep: {changed} stale row(s) → failed-stale in {stats_file}", flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stats_file')
    parser.add_argument('--heartbeat-max-age', type=int, default=90,
                        help='Seconds before a heartbeat is considered stale (default: 90)')
    parser.add_argument('--row-max-age', type=int, default=1800,
                        help='Seconds before a no-heartbeat row is considered stale (default: 1800)')
    args = parser.parse_args()
    sweep(args.stats_file, args.heartbeat_max_age, args.row_max_age)
