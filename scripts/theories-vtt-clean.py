#!/usr/bin/env python3
"""theories-vtt-clean.py — S214 theories wave 1, step: transcript cleaning.

Strips WEBVTT headers/timestamps/cue metadata from the ASX caption files in
working/theories/videos/transcripts/ and writes one plain-text paragraph
stream per video to working/theories/videos/transcripts-clean/<id>.txt.

All 15 wave-1 files are uploaded (non-rolling) captions — no <c> styling
tags, no repeated rolling lines — verified 2026-07-12 before writing this.
A consecutive-duplicate-line guard is kept anyway as cheap insurance.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "working/theories/videos/transcripts"
DST = REPO / "working/theories/videos/transcripts-clean"

TIMESTAMP_RE = re.compile(r"^\d{2}:\d{2}:\d{2}\.\d{3} --> ")
HEADER_RE = re.compile(r"^(WEBVTT|Kind:|Language:)")


def clean(path: Path) -> str:
    out: list[str] = []
    prev = None
    for ln in path.read_text().splitlines():
        s = ln.strip()
        if not s or HEADER_RE.match(s) or TIMESTAMP_RE.match(s) or s.isdigit():
            continue
        if s == prev:
            continue
        out.append(s)
        prev = s
    return " ".join(out)


def main():
    DST.mkdir(parents=True, exist_ok=True)
    for f in sorted(SRC.glob("*.en.vtt")):
        vid = f.name.split(".")[0]
        text = clean(f)
        (DST / f"{vid}.txt").write_text(text + "\n")
        print(f"{vid}: {len(text):,} chars")


if __name__ == "__main__":
    main()
