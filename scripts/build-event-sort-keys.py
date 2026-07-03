#!/usr/bin/env python3
"""build-event-sort-keys.py — derive a composite chronological sort key for every
event node and write an idempotent `sort_keys:` frontmatter block.

DERIVED / REGENERABLE. Re-run after any event dating backfill (occurred.ac_year)
or chapter re-split. Source of truth for the year is occurred.ac_year; this block
mirrors it plus reading-order anchors and the composite.

  composite      story-time primary key  {ac_year:04d}.{book_order}.{chapter:03d}
                 (null when the event has no ac_year — NOT fabricated)
  reading_order  pure reading-order key  {book_order}.{chapter:03d} (null if no chapter)
  basis          year+chapter | year-only | chapter-only | none

Usage:
  python3 scripts/build-event-sort-keys.py            # apply
  python3 scripts/build-event-sort-keys.py --dry-run  # report only
"""
import glob, re, sys, json

DRY = "--dry-run" in sys.argv
BOOK_ORDER = {"AGOT":1,"ACOK":2,"ASOS":3,"AFFC":4,"ADWD":5}

def split_fm(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---": return None
    close = next((i for i in range(1,len(lines)) if lines[i].strip()=="---"), None)
    if close is None: return None
    return lines[1:close], lines[close+1:]

# 1) pov_label -> (book_order, chapter_number)
chap = {}
for p in glob.glob("sources/chapters/*/*.md"):
    parts = split_fm(open(p,encoding="utf-8").read())
    if not parts: continue
    fm = "\n".join(parts[0])
    book = (re.search(r'^book:\s*(\S+)', fm, re.M) or [None,None])[1]
    lab  = (re.search(r'^pov_label:\s*"?([^"\n]+?)"?\s*$', fm, re.M) or [None,None])[1]
    num  = (re.search(r'^chapter_number:\s*(\d+)', fm, re.M) or [None,None])[1]
    if book and lab and num:
        chap[f"{book} {lab}".strip()] = (BOOK_ORDER.get(book,9), int(num))

def compute(fm):
    ym = re.search(r'^occurred:.*?\n\s*ac_year:\s*(\d+)', fm, re.M|re.S)
    ac_year = int(ym.group(1)) if ym else None
    ev = re.findall(r'^\s*-\s*([A-Z]{3,4} .+?)\s*$', fm, re.M)
    anchors = sorted((chap[e][0], chap[e][1], e) for e in ev if e in chap)
    bo, cn, lab = anchors[0] if anchors else (None, None, None)
    reading = f"{bo}.{cn:03d}" if bo else None
    if ac_year is not None:
        composite = f"{ac_year:04d}.{bo or 0}.{(cn or 0):03d}"
        basis = "year+chapter" if bo else "year-only"
    else:
        composite = None
        basis = "chapter-only" if bo else "none"
    return dict(ac_year=ac_year, book_order=bo, chapter_number=cn,
                chapter_label=lab, composite=composite, reading_order=reading, basis=basis)

def yv(v):
    if v is None: return "null"
    return f'"{v}"' if isinstance(v,str) else str(v)

def block(d):
    order = ["ac_year","book_order","chapter_number","chapter_label",
             "composite","reading_order","basis"]
    out = ["sort_keys:"]
    for k in order: out.append(f"  {k}: {yv(d[k])}")
    return out

def strip_existing(fm_lines):
    out, skip = [], False
    for ln in fm_lines:
        if re.match(r'^sort_keys:\s*$', ln): skip = True; continue
        if skip and (ln.startswith(" ") or ln.strip()==""):  # indented child / blank
            if ln.strip()=="" : skip=False; out.append(ln); continue
            continue
        skip = False
        out.append(ln)
    return out

counts = {"year+chapter":0,"year-only":0,"chapter-only":0,"none":0}
rows = {}
written = 0
for path in glob.glob("graph/nodes/events/*.node.md"):
    slug = path.split("/")[-1].replace(".node.md","")
    text = open(path,encoding="utf-8").read()
    parts = split_fm(text)
    if not parts: continue
    fm_lines, body = parts
    d = compute("\n".join(fm_lines))
    counts[d["basis"]] += 1
    rows[slug] = d
    if not DRY:
        new_fm = strip_existing(fm_lines)
        while new_fm and new_fm[-1].strip()=="": new_fm.pop()
        new_fm += block(d)
        open(path,"w",encoding="utf-8").write("---\n"+"\n".join(new_fm)+"\n---\n"+"\n".join(body))
        written += 1

tot = sum(counts.values())
print(("DRY RUN — " if DRY else "APPLIED — ")+f"{tot} event nodes"+(f", {written} written" if not DRY else ""))
for k,v in counts.items(): print(f"  basis={k:14} {v:4}  ({100*v//tot}%)")

# backfill queue: undated events (no ac_year) that sit on causal edges
CAUSAL={"CAUSES","TRIGGERS","MOTIVATES"}
on_causal=set()
for line in open("graph/edges/edges.jsonl",encoding="utf-8"):
    try: e=json.loads(line)
    except: continue
    if e.get("edge_type") in CAUSAL:
        on_causal.add(e.get("source_slug")); on_causal.add(e.get("target_slug"))
queue=sorted(s for s in on_causal if s in rows and rows[s]["ac_year"] is None)
with open("working/event-chronology-backfill-queue.md","w",encoding="utf-8") as f:
    f.write("# Chronology backfill queue — undated events on causal chains\n\n")
    f.write("Event nodes with NO `occurred.ac_year` that are endpoints of a CAUSES/TRIGGERS/MOTIVATES edge.\n")
    f.write("These are the high-value targets for a bounded Fable dating pass (composite sort key stays null until filled).\n\n")
    for s in queue:
        f.write(f"- `{s}`  (basis={rows[s]['basis']}, reading_order={rows[s]['reading_order']})\n")
print(f"\nBackfill queue: {len(queue)} undated events on causal chains -> working/event-chronology-backfill-queue.md")
