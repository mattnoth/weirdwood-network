#!/usr/bin/env python3
"""Mint the S151 cheap-L2 enrichment round — FIVE granular sub-plot dips in one session
(Matt S151: "Start with the cheap L2 round. You should be able to do all of that."):

  B1  Frey-pies / Grand Northern Conspiracy   (Red Wedding sub-plot; wo5k->north seam)
  B2  Creation of Robert Strong               (Tywin's-death ∩ Cersei's-downfall)
  B3  Sandor / Quiet-Isle gravedigger evidence (Brienne->Stoneheart sub-plot; GATED identity)
  B4  Black-cells / Varys-visits-Ned          (Ned's-downfall sub-plot)
  B7  Kingslayer -> slaying hub               (Sack-of-KL sub-plot)

Four new event nodes (B1 ×2, B2 ×1, B4 ×1); 38 edges total (see candidates.json).
GATED theory nodes (frey-pies-theories / robert-strong-theories / gravedigger-theories) are
DELIBERATELY NOT wired — theory nodes are conventionally islanded (1/45 has any edge) and the
identity readings stay theory-track-gated; the dead-ends are addressed by the evidence CLUSTER.

Additive only. Misfire RETIREMENTS (elder-brother HEALS sandor on the title node; sandor
OWNS/BONDED_TO the `stranger` RELIGION node) + any fresh-verify drops live in the finalize script.

Reads working/enrichment/cheap-l2-s151/candidates.json; RE-GREPS each quote for the authoritative
line (FAIL-fast if a quote moved). Backup, re-run guard, slug pre-check (new nodes excluded)."""
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
NODES_EVENTS = REPO / "graph" / "nodes" / "events"
CAND = REPO / "working" / "enrichment" / "cheap-l2-s151" / "candidates.json"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-cheap-l2-round-2026-06-26.jsonl"

RUN_ID = "cheap-l2-round-s151"
PRODUCED_AT = "2026-06-26T00:00:00+00:00"

NEW_NODE_SLUGS = {
    "grand-northern-conspiracy",
    "manderly-bakes-the-frey-pies",
    "creation-of-robert-strong",
    "varys-visits-ned-in-the-black-cells",
}


def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def authoritative_line(book, chapter, quote):
    f = REPO / "sources" / "chapters" / book / f"{chapter}.md"
    if not f.exists():
        sys.exit(f"ABORT: chapter file missing: {f}")
    lines = f.read_text(encoding="utf-8").splitlines()
    q = norm(quote)
    for i, ln in enumerate(lines, 1):
        if q in norm(ln):
            return i
    for i in range(len(lines) - 1):
        if q in norm(lines[i] + " " + lines[i + 1]):
            return i + 1
    sys.exit(f"ABORT: quote not found in {chapter}.md -> {quote!r}")


def common():
    return {
        "decision": "emit_edge",
        "candidate_kind": "enrichment-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-cheap-l2-round-s151",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


def make_edge_row(e):
    book, chapter = e["book"], e["chapter"]
    line = authoritative_line(book, chapter, e["quote"])
    row = {
        "edge_type": e["type"],
        "source_slug": e["source"],
        "target_slug": e["target"],
        **common(),
        "evidence_book": book,
        "evidence_chapter": chapter,
        "evidence_ref": f"sources/chapters/{book}/{chapter}.md:{line}",
        "evidence_quote": e["quote"],
        "confidence_tier": e["tier"],
        "asserted_relation": e["note"],
        "candidate_id": e["id"],
        "unit": e.get("unit", ""),
    }
    if e.get("qualifier"):
        row["qualifier"] = e["qualifier"]
    if e.get("verify"):
        row["verified_by"] = "pending"
    return row


# ════════════════════════════ NODE BODIES ════════════════════════════

GNC = """\
---
name: "Grand Northern Conspiracy"
type: event.conspiracy
slug: grand-northern-conspiracy
aliases: ["the Grand Northern Conspiracy", "the northern conspiracy", "the mummer's farce", "the North remembers plot"]
confidence: tier-1
containers: [wo5k, north]
era: current-narrative
pass_origin: s151-cheap-l2-frey-pies
node_version: 1
evidence_chapters:
  - ADWD Davos III
  - ADWD Davos IV
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Grand Northern Conspiracy

The secret pact among northern lords — architected by [Wyman Manderly](wyman-manderly) with
[Robett Glover](robett-glover) — to feign submission to Bolton/Frey rule while covertly working to
restore House Stark. Wyman bends the knee, drinks with the Freys, and promises a granddaughter to
[Rhaegar Frey](rhaegar-frey), all the while plotting their ruin: he stages the
[fake execution of Davos Seaworth](wyman-manderly-stages-fake-execution-of-davos) to deceive the
court, then charges [Davos](davos-seaworth) to smuggle [Rickon Stark](rickon-stark) home from Skagos
as proof of a Stark heir, and secretly pledges his heavy horse and warships to
[Stannis](stannis-baratheon). The mask held him for as long as the Lannisters kept his last son
[Wylis](wylis-manderly) hostage — once Wylis is freed, the farce ends. The conspiracy is the
political engine behind the [Frey pies](manderly-bakes-the-frey-pies) and Stannis's
[march on Winterfell](stannis-march-on-winterfell); its watchword is *"The North remembers."*

## Quotes

> "The north remembers, Lord Davos. The north remembers, and the mummer's farce is almost done. My son is home."

> "It's not a king I need but a smuggler."

> "My son Wendel came to the Twins a guest. He ate Lord Walder's bread and salt, and hung his sword upon the wall to feast with friends. And they murdered him."
"""

PIES = """\
---
name: "Manderly bakes the Frey pies"
type: event.incident
slug: manderly-bakes-the-frey-pies
aliases: ["the Frey pies", "the Manderly pies", "the wedding pies at Winterfell", "the pork pies"]
confidence: tier-2
containers: [wo5k, north]
era: current-narrative
pass_origin: s151-cheap-l2-frey-pies
node_version: 1
evidence_chapters:
  - ADWD The Prince of Winterfell
  - ADWD A Ghost in Winterfell
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Manderly bakes the Frey pies

At the [Ramsay Bolton–"Arya Stark" wedding feast](wedding-of-ramsay-bolton-and-fake-arya) in
Winterfell, [Wyman Manderly](wyman-manderly) furnishes the food and personally serves three enormous
pork pies "as wide across as wagon wheels." Three Frey envoys —
[Rhaegar](rhaegar-frey), [Jared](jared-frey), and [Symond](symond-frey) — had been Wyman's guests at
White Harbor and then vanished on the road to Winterfell. As he is carried drunk from the hall, Wyman
calls for a singer to give them *"a song about the Rat Cook"* — the [legend](rat-cook) of the cook who
baked a king's son into a pie and served him to his father. The implication (universally read, never
textually confirmed) is that the three missing Freys are in the pies. The pies are the
[Grand Northern Conspiracy](grand-northern-conspiracy)'s reprisal for the Red Wedding made literal.

## Quotes

> "The best pie you have ever tasted, my lords. Wash it down with Arbor gold and savor every bite. I know I shall."

> "We should have a song about the Rat Cook," he was muttering, as he staggered past Theon, leaning on his knights. "Singer, give us a song about the Rat Cook."
"""

ROBERT_STRONG = """\
---
name: "Creation of Robert Strong"
type: event.incident
slug: creation-of-robert-strong
aliases: ["the making of Robert Strong", "Qyburn's experiments on Gregor Clegane", "Qyburn's work in the black cells"]
confidence: tier-2
containers: [wo5k]
era: current-narrative
pass_origin: s151-cheap-l2-robert-strong
node_version: 1
evidence_chapters:
  - AFFC Cersei II
  - AFFC Cersei VII
  - ADWD Cersei II
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Creation of Robert Strong

[Gregor Clegane](gregor-clegane), poisoned by [Oberyn](oberyn-martell)'s
[manticore-venom](manticore-venom)-coated spear, lingers in screaming agony for weeks.
[Cersei](cersei-lannister) gives his dying body to the disgraced ex-maester
[Qyburn](qyburn) — expelled from the Citadel for [opening the bodies of the living](necromancy) — to
"study" in the [black cells](black-cells), with free rein and her gold, on the condition that she be
brought Gregor's head for Dorne. Gregor's death is later announced (the head dispatched to Prince
Doran), but no living body is shown. Then a silent giant in white enamelled plate, eight feet tall and
never unhelmed, appears as [Ser Robert Strong](robert-strong) and is named to the
[Kingsguard](kingsguard) — Cersei's champion for her [trial by combat](cersei-resolves-on-trial-by-combat).

**Gated identity (NOT asserted in the graph):** the books strongly imply but never confirm that Robert
Strong is the reanimated Gregor. Strong is never seen to eat, drink, speak, or use the privy; Kevan
Lannister privately suspects "just who this Ser Robert really was." Per the theories-track gate, the
`gregor-clegane` and `robert-strong` nodes stay **separate** — this event encodes the structural
relationship (Gregor's dying body + Qyburn's necromancy + the champion that results) WITHOUT a
`SAME_AS`/`RESURRECTS` identity edge.

## Quotes

> "I wished to understand the nature of death, so I opened the bodies of the living. For that crime the grey sheep shamed me and forced me into exile."

> "The Mountain is yours. Do what you will with him, but confine your studies to the black cells. When he dies, bring me his head."

> "If it please Your Grace, Ser Robert has taken a holy vow of silence," Qyburn said. "He has sworn that he will not speak until all of His Grace's enemies are dead and evil has been driven from the realm."
"""

VARYS_VISIT = """\
---
name: "Varys visits Ned in the black cells"
type: event.incident
slug: varys-visits-ned-in-the-black-cells
aliases: ["Varys visits Ned in the black cells", "Varys persuades Ned to confess", "the gaoler visit to Eddard Stark"]
confidence: tier-1
containers: [wo5k]
era: current-narrative
pass_origin: s151-cheap-l2-ned-black-cells
node_version: 1
evidence_chapters:
  - AGOT Eddard XV
occurred:
  ac_year: 298
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-contemporaneous
---

# Varys visits Ned in the black cells

Imprisoned in the lightless [black cells](black-cells) beneath the Red Keep, [Eddard Stark](eddard-stark)
is visited by [Varys](varys), disguised as a grizzled turnkey reeking of sour wine. Varys brings water,
relays intelligence on Ned's daughters ([Arya](arya-stark) escaped and missing; [Sansa](sansa-stark)
kept close at court, pleading for her father's life), and proposes the bargain: confess to treason
publicly, command [Robb](robb-stark) to lay down his sword, and proclaim
[Joffrey](joffrey-baratheon) — and the queen will let Ned take the black and live out his days on the
[Wall](the-wall). He closes with an explicit threat: the next visitor could bring Ned "Sansa's head."
This visit is the **proximate cause** of Ned's public [confession](ned-confesses-to-treason) — the
mechanism the spine lacked.

## Quotes

> "The next visitor who calls on you could bring you bread and cheese and the milk of the poppy for your pain . . . or he could bring you Sansa's head. The choice, my dear lord Hand, is entirely yours."

> Varys had transformed himself into a grizzled turnkey, reeking of sweat and sour wine.

> "I want you to serve the realm," Varys said. "Tell the queen that you will confess your vile treason, command your son to lay down his sword, and proclaim Joffrey as the true heir."
"""

NODES = [
    ("grand-northern-conspiracy", NODES_EVENTS, GNC),
    ("manderly-bakes-the-frey-pies", NODES_EVENTS, PIES),
    ("creation-of-robert-strong", NODES_EVENTS, ROBERT_STRONG),
    ("varys-visits-ned-in-the-black-cells", NODES_EVENTS, VARYS_VISIT),
]


def main():
    data = json.loads(CAND.read_text())
    edges = data["edges"]

    all_slugs = set()
    for e in edges:
        all_slugs.add(e["source"]); all_slugs.add(e["target"])
    resolved, missing = precheck_slugs(all_slugs - NEW_NODE_SLUGS)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed — non-existent: {sorted(missing)}")
    print(f"Slug pre-check OK: {len(resolved)} existing slugs resolved.")

    raw = EDGES.read_text(encoding="utf-8").splitlines()
    existing = [ln for ln in raw if ln.strip()]
    if any(RUN_ID in ln for ln in existing):
        sys.exit(f"ABORT: run_id '{RUN_ID}' already present — already minted.")
    print(f"Re-run guard OK: run_id '{RUN_ID}' not present.")

    new_rows = [make_edge_row(e) for e in edges]  # FAIL-fast on any unfound quote
    print(f"Line-check OK: all {len(new_rows)} quotes located in source.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)
    print(f"Backup written -> {BACKUP.relative_to(REPO)}")

    created = []
    for slug, node_dir, body in NODES:
        p = node_dir / f"{slug}.node.md"
        if p.exists():
            print(f"  SKIP node (exists): {p.name}")
        else:
            p.write_text(body, encoding="utf-8")
            created.append(slug)
            print(f"  Created node: {p.relative_to(REPO)}")

    out = existing + [json.dumps(r, ensure_ascii=False) for r in new_rows]
    EDGES.write_text("\n".join(out) + "\n", encoding="utf-8")

    tc, uc = {}, {}
    for e in edges:
        tc[e["type"]] = tc.get(e["type"], 0) + 1
        uc[e.get("unit", "")] = uc.get(e.get("unit", ""), 0) + 1
    print("\n── SUMMARY ──")
    print(f"Nodes created ({len(created)}): {', '.join(created) or '(none)'}")
    print(f"Edges appended ({len(new_rows)}):")
    for t, c in sorted(tc.items()):
        print(f"  {t}: {c}")
    print("By unit:")
    for u, c in sorted(uc.items()):
        print(f"  {u}: {c}")


if __name__ == "__main__":
    main()
