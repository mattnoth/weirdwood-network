#!/usr/bin/env python3
"""s207-event-retype.py — S207 event-layer schema-drift reconciliation (Part A).

Matt-approved this session (AskUserQuestion): HYBRID disposition.
  1. SANCTION 5 off-schema subtypes into architecture.md (done separately) — these are KEPT:
       death, capture, ceremony, decree, council
  2. RETYPE every OTHER off-schema subtype down to an existing sanctioned leaf (RETYPE_MAP).
  3. FIX 25 clean `event.war`-mistyped-as-`event.battle` slugs -> event.war (WAR_FIX_SLUGS).
  4. HOLD 4 for review (NOT touched here — reported only):
       great-spring-sickness, hour-of-the-wolf, lysene-spring, anarchy-in-the-reach

Also fixes the auto-generated stub prose line ("... is a event.<old> from the AWOIAF wiki")
so the node body stays consistent with the retyped frontmatter.

Files are git-tracked, so git IS the backup (no separate copy). `git diff` = the change set;
`git checkout -- <file>` reverts. Scope is strictly graph/nodes/events/*.node.md.

Usage:
  python3 scripts/s207-event-retype.py            # dry-run (default): full manifest, no writes
  python3 scripts/s207-event-retype.py --apply    # rewrite the node files
"""
import argparse
import glob
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS = os.path.join(REPO, "graph", "nodes", "events")

# The 16 leaves already in architecture.md's Type Reference Table + the 5 sanctioned this
# session. Nodes already carrying one of these are in-schema and untouched (except war-fix).
SANCTIONED_NOW = {"death", "capture", "ceremony", "decree", "council"}
IN_SCHEMA = {
    "battle", "war", "tournament", "wedding", "feast", "coronation", "trial",
    "assassination", "execution", "conspiracy", "deception", "incident",
    "appointment", "exile", "birth", "investiture",
} | SANCTIONED_NOW

# off-schema subtype -> sanctioned target leaf
RETYPE_MAP = {
    # junk / catch-all -> incident (the sanctioned "bounded multi-beat event" leaf)
    "other": "incident",
    "voyage": "incident", "negotiation": "incident", "uprising": "incident",
    "surrender": "incident", "betrothal": "incident", "betrayal": "incident",
    "treaty": "incident", "progress": "incident", "escape": "incident",
    "flight": "incident", "disaster": "incident", "plague": "incident",
    "famine": "incident", "dismissal": "incident", "resignation": "incident",
    "deposition": "incident", "construction": "incident", "abduction": "incident",
    "sighting": "incident", "shipwreck": "incident", "scandal": "incident",
    "revelation": "incident", "migration": "incident", "discovery": "incident",
    "disappearance": "incident", "departure": "incident", "confrontation": "incident",
    "concealment": "incident",
    "coming-of-age": "ceremony",  # Jaehaerys reaching his majority — a ceremonial milestone
    # clean 1:1 to a more specific existing/sanctioned leaf
    "marriage": "wedding",
    "siege": "battle", "raid": "battle", "occupation": "battle",
    "assassination_attempt": "assassination",
    "banishment": "exile",
    "succession": "investiture",
    "funeral": "ceremony",     # ceremony sanctioned this session
    "reform": "decree",        # decree sanctioned this session
    "imprisonment": "capture",  # capture sanctioned this session
}

# 25 unambiguous multi-battle conflicts currently mistyped event.battle -> event.war
WAR_FIX_SLUGS = {
    "aegons-conquest", "aegon-the-uncrowneds-rebellion", "conquest-of-dorne",
    "dance-of-the-dragons", "daughters-war", "fair-isle-rebellion",
    "first-blackfyre-rebellion", "first-dornish-war", "fourth-dornish-war",
    "first-turtle-war", "fourth-blackfyre-rebellion", "harren-the-reds-rebellion",
    "greyjoys-rebellion", "jonos-arryns-rebellion", "lyonel-baratheons-rebellion",
    "nymerias-war", "nights-watch-rebellion-of-50-ac", "roberts-rebellion",
    "second-blackfyre-rebellion", "second-dornish-war", "second-spice-war",
    "shadow-war", "sistermens-rebellion", "thousand-years-war",
    "third-blackfyre-rebellion",
}

# The 4 slugs Matt held for review, then dispositioned this session (AskUserQuestion):
#   plague / post-Dance reckoning / Lysene captivity interlude -> incident (none are combat);
#   anarchy-in-the-reach -> war (its own prose: "an open war of succession").
REVIEW_FIX = {
    "great-spring-sickness": "incident",
    "hour-of-the-wolf": "incident",
    "lysene-spring": "incident",
    "anarchy-in-the-reach": "war",
}
HOLD_FOR_REVIEW = set()  # emptied — all 4 dispositioned above

TYPE_RE = re.compile(r'^(type:\s*["\']?)event\.([a-z_-]+)(["\']?\s*)$', re.M)


def current_subtype(text):
    m = TYPE_RE.search(text)
    return m.group(2) if m else None


def retype_text(text, new_sub, old_sub):
    """Rewrite the frontmatter type line + the auto-stub prose 'is a event.<old>' line."""
    text = TYPE_RE.sub(lambda m: f"{m.group(1)}event.{new_sub}{m.group(3)}", text, count=1)
    # stub prose: "... is a event.battle from the AWOIAF wiki." / "is an event.other ..."
    text = re.sub(rf"\bis an? event\.{re.escape(old_sub)}\b",
                  f"is a event.{new_sub}", text)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="rewrite node files (default: dry-run)")
    args = ap.parse_args()

    retypes = []   # (slug, old, new, rule)
    held = []      # (slug, old)
    for f in sorted(glob.glob(os.path.join(EVENTS, "*.node.md"))):
        slug = os.path.basename(f)[: -len(".node.md")]
        text = open(f, encoding="utf-8").read()
        old = current_subtype(text)
        if old is None:
            continue

        new = None
        rule = None
        if slug in HOLD_FOR_REVIEW:
            held.append((slug, old))
            continue
        if slug in REVIEW_FIX:
            new, rule = REVIEW_FIX[slug], "review-fix"
        elif slug in WAR_FIX_SLUGS:
            new, rule = "war", "war-fix"
        elif old in RETYPE_MAP:
            new, rule = RETYPE_MAP[old], "subtype-retype"

        if new is None or new == old:
            continue
        retypes.append((slug, old, new, rule))
        if args.apply:
            open(f, "w", encoding="utf-8").write(retype_text(text, new, old))

    # ---- manifest ----
    print("=== S207 event retype — %s ===" % ("APPLY" if args.apply else "DRY-RUN"))
    war = [r for r in retypes if r[3] == "war-fix"]
    sub = [r for r in retypes if r[3] == "subtype-retype"]

    print("\n[1] war-mistype fixes (event.battle -> event.war): %d" % len(war))
    for slug, o, n, _ in war:
        print("    %-45s %s -> %s" % (slug, o, n))

    print("\n[2] subtype retypes -> sanctioned leaf: %d" % len(sub))
    by_target = {}
    for slug, o, n, _ in sub:
        by_target.setdefault(f"{o}->{n}", []).append(slug)
    for k in sorted(by_target, key=lambda x: (-len(by_target[x]), x)):
        print("    %-24s x%d" % (k, len(by_target[k])))

    rev = [r for r in retypes if r[3] == "review-fix"]
    print("\n[3] review-fix (Matt-dispositioned held nodes): %d" % len(rev))
    for slug, o, n, _ in rev:
        print("    %-45s %s -> %s" % (slug, o, n))

    print("\n[4] HELD for review (untouched): %d" % len(held))
    for slug, o in held:
        print("    %-45s (event.%s)" % (slug, o))

    print("\nTOTAL nodes retyped: %d  (war %d + subtype %d)" % (len(retypes), len(war), len(sub)))
    if not args.apply:
        print("\nDRY-RUN — no files written. Re-run with --apply.")


if __name__ == "__main__":
    main()
