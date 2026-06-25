#!/usr/bin/env python3
"""Line-check every candidate quote against its cited chapter file.
For each edge: open the file, search a window (+/- WINDOW lines) around the cited
line for the (normalized) quote substring. Report PASS (with the line it was
actually found on) or FAIL."""
import json, re, sys, pathlib

ROOT = pathlib.Path("/Users/mnoth/source/asoiaf-chat")
WINDOW = 8

def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()

def main():
    data = json.loads((ROOT / "working/enrichment/dany-meereen/candidates.json").read_text())
    edges = data["edges"]
    npass = nfail = 0
    for e in edges:
        ref = e["ref"]
        path_str, line_str = ref.rsplit(":", 1)
        line = int(line_str)
        f = ROOT / path_str
        if not f.exists():
            print(f"FAIL {e['id']:8} FILE-MISSING {path_str}")
            nfail += 1
            continue
        lines = f.read_text().splitlines()
        lo = max(0, line - 1 - WINDOW)
        hi = min(len(lines), line - 1 + WINDOW + 1)
        window_text = norm(" ".join(lines[lo:hi]))
        q = norm(e["quote"])
        if q in window_text:
            # find which line it lands on
            found = "?"
            for i in range(lo, hi):
                if q in norm(lines[i]):
                    found = i + 1
                    break
            flag = "" if found == line else f"  (cited {line}, found {found})"
            print(f"PASS {e['id']:8} {e['source']} -{e['type']}-> {e['target']}{flag}")
            npass += 1
        else:
            print(f"FAIL {e['id']:8} {e['source']} -{e['type']}-> {e['target']}  ref={ref}")
            print(f"        quote: {e['quote'][:90]}")
            nfail += 1
    print(f"\n{npass} PASS / {nfail} FAIL  of {len(edges)} edges")

if __name__ == "__main__":
    main()
