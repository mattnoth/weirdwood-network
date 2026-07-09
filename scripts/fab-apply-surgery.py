#!/usr/bin/env python3
"""Reusable fresh-verify surgery for the F&B batch apply (S201).

Reads a spec of FOLD / RENAME ops and applies them across whichever apply-unit owns each
`old` slug. Auto-locates the unit via each candidates.json `_meta.new_node_slugs`.

  FOLD   old -> new : old CREATE is dropped (target already exists in-graph OR is another
                      CREATE). Remove old from new_node_slugs, retarget edges target==old -> new,
                      DELETE the old .node.md file.
  RENAME old -> new : old CREATE keeps existing but under a new slug. Replace old->new in
                      new_node_slugs, retarget edges target==old -> new, rename the .node.md file
                      + rewrite its frontmatter `slug:`.

Spec JSON: [{"action":"FOLD"|"RENAME","old":"<slug>","new":"<slug>"}, ...]

Usage:
  python3 fab-apply-surgery.py --spec <spec.json>            # dry-run
  python3 fab-apply-surgery.py --spec <spec.json> --apply
"""
import argparse, glob, json, os, re, sys

APPLY_ROOT = "/Users/mnoth/source/asoiaf-chat/working/fire-and-blood/apply"
SMOKE = {"fab-aegons-conquest-03", "fab-heirs-of-the-dragon-15-p01",
         "fab-heirs-of-the-dragon-15-p02", "fab-sons-of-the-dragon-05-p01"}


def find_unit(old):
    for cp in glob.glob(os.path.join(APPLY_ROOT, "*", "candidates.json")):
        unit = cp.split("/")[-2]
        if unit in SMOKE:
            continue
        if old in json.load(open(cp))["_meta"].get("new_node_slugs", []):
            return unit, cp
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    spec = json.load(open(a.spec))
    print("=== fab-apply-surgery — %s (%d ops) ===" % ("APPLY" if a.apply else "DRY-RUN", len(spec)))
    ok = True
    for op in spec:
        act, old, new = op["action"], op["old"], op["new"]
        unit, cp = find_unit(old)
        if not unit:
            print("  !! %s %s: OLD SLUG NOT FOUND in any unit's new_node_slugs" % (act, old)); ok = False; continue
        c = json.load(open(cp))
        retarget = [e["id"] for e in c["edges"] if e.get("target") == old]
        of = os.path.join(APPLY_ROOT, unit, "nodes", old + ".node.md")
        print("  %-6s [%s] %s -> %s | edges=%s | node_file=%s"
              % (act, unit, old, new, retarget, os.path.exists(of)))
        if not a.apply:
            continue
        # apply
        nns = c["_meta"]["new_node_slugs"]
        if act == "FOLD":
            c["_meta"]["new_node_slugs"] = [s for s in nns if s != old]
        elif act == "RENAME":
            c["_meta"]["new_node_slugs"] = [new if s == old else s for s in nns]
        for e in c["edges"]:
            if e.get("target") == old:
                e["target"] = new
        json.dump(c, open(cp, "w"), indent=1, ensure_ascii=False)
        if act == "FOLD":
            if os.path.exists(of):
                os.remove(of)
        elif act == "RENAME":
            nf = os.path.join(APPLY_ROOT, unit, "nodes", new + ".node.md")
            body = re.sub(r"^slug:\s*.+$", "slug: " + new, open(of).read(), count=1, flags=re.M)
            open(nf, "w").write(body)
            os.remove(of)
    if not ok:
        sys.exit("some ops failed to locate — fix the spec")
    print("APPLIED" if a.apply else "DRY-RUN done")


if __name__ == "__main__":
    main()
