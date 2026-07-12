#!/usr/bin/env python3
"""S213 roles round 2 — apply adjudication decisions and assemble the final
mint-ready candidates.json + parked.json. Decisions documented in
ADJUDICATION-s213.md. Read-only on graph/; writes only into this folder."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent

DROP = {
    "R2-12",  # rodrik-cassel not shown in the event (mediating away from the fighting)
    "R3-11",  # rickard-karstark bounty = indirect incentive, not command; dead by event time
}

JAIME_QUOTE = "“Yes.” Cersei beckoned to Jaime. “Lord Commander, escort His Grace and his little queen to their pillows, if you would.”"
CERSEI_QUOTE = "They will have him stumbling and shuffling like a fool by the time they’re done, Cersei thought resentfully as she watched."

PATCH = {
    # quote swap: original quote showed the order only; this line is the on-page
    # tasking Jaime accepts ("As you command") before escorting the couple.
    "R2-03": {"quote": JAIME_QUOTE,
              "note": "tasked at the feast to escort the king and queen to the bedding; accepts and performs it — logistical/supportive, not guest-only"},
    # reclassify: text says Lady Alerie made all the arrangements, so
    # organizer-Cersei was overstated; presence at the feast is on-page.
    "R2-04": {"type": "ATTENDS", "quote": CERSEI_QUOTE,
              "note": "present at the feast as regent/mother of the groom, watching the dancing; organizer role belongs to Lady Alerie per the same chapter"},
    # tier downgrade: retreat is off-page; Salladhor Saan's report is secondhand.
    "R3-08": {"tier": "tier-2",
              "note": "the retreat itself happens off-page between ACOK and ASOS; Salladhor Saan's on-page report (secondhand => tier-2) confirms Stannis withdrew to Dragonstone"},
    # reclassify per verifier: quote shows personal arrival + dragon combat;
    # Davos Darklyn is the loyalist field commander.
    "R4-02": {"type": "FIGHTS_IN",
              "note": "loyalist/king's side; arrives personally on Balerion and turns the battle by fighting — field command belonged to Davos Darklyn"},
}

candidates, wiki_only, no_node, flags = [], [], [], []
for i in range(1, 5):
    d = json.loads((OUT / f"proposals/proposals-chunk{i}.json").read_text())
    for r in d["candidates"]:
        if r["id"] in DROP:
            continue
        r = dict(r)
        r.update(PATCH.get(r["id"], {}))
        candidates.append(r)
    wiki_only += d.get("wiki_only", [])
    no_node += d.get("no_node", [])
    flags += [f"[chunk{i}] {f}" for f in d.get("flags", [])]

# final integrity: every kept quote must be an exact single-line substring
bad = []
for r in candidates:
    chap = Path("sources/chapters") / r["book"] / (r["chapter"] + ".md")
    if not chap.exists():
        bad.append((r["id"], "missing-chapter"))
        continue
    if not any(r["quote"] in line for line in chap.read_text().splitlines()):
        bad.append((r["id"], "quote-not-single-line-substring"))
if bad:
    print("INTEGRITY FAILURES:", bad)
    raise SystemExit(1)

(OUT / "candidates.json").write_text(json.dumps({
    "_meta": {"slice": "roles round 2 (S213)", "source": "4 Sonnet proposer chunks, "
              "Haiku fresh-verified, adjudicated per ADJUDICATION-s213.md",
              "candidates": len(candidates)},
    "candidates": candidates,
}, indent=1))
(OUT / "parked.json").write_text(json.dumps({
    "parked_wiki_only": wiki_only,
    "no_node": no_node,
}, indent=1))
print(f"kept candidates: {len(candidates)} (dropped {len(DROP)})")
print(f"parked wiki_only: {len(wiki_only)}; no_node: {len(no_node)}; flags carried: {len(flags)}")
from collections import Counter
print(Counter(r["type"] for r in candidates))
