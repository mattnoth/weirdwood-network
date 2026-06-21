#!/usr/bin/env python3
"""Mint the AGOT "Essos root" causal arc (S119 essos-root track).

ESSOS container decomposition (working/essos-decomposition.md), top-ranked
junctures E4 + E1 built together as ONE contiguous chain (E4's terminus,
drogo-westward-vow, is E1's root). This is the prime-mover root of the whole
Essos thread -- the Westeros->Essos bridge (Robert's assassination order) plus
the dragon-birth arc (Drogo's death + the pyre). Built per the proven arc-mint
machine; causal edges Tier-2 verified_by pending until a fresh-subagent CONFIRM.

New beat-nodes (written as .node.md, not here):
  - robert-orders-daenerys-assassination  (event.assassination; AGOT Eddard VIII)
  - drogo-westward-vow                     (event.ceremony; AGOT Daenerys VI)
  - drogo-blood-magic-ritual               (event.incident; AGOT Daenerys VIII-IX)
  - death-of-khal-drogo                    (event.death; AGOT Daenerys IX)
  - dragon-hatching-on-drogo-pyre          (event.incident; AGOT Daenerys X)
Repaired existing bare Plate-3 nodes (spaced aliases + occurred + clean body):
  - the-wine-merchant-attempts-to-poison-dany
  - ned-orders-daenerys-s-assassination-cancelled

Causal spine (chain-as-arc, NO umbrella parent; Tier-2, verified_by pending):
  robert-orders-daenerys-assassination --CAUSES--> the-wine-merchant-attempts-to-poison-dany
  robert-orders-daenerys-assassination --CAUSES--> ned-orders-daenerys-s-assassination-cancelled  [verifier: adjudicate; cancellation = negation of the order]
  the-wine-merchant-attempts-to-poison-dany --CAUSES--> drogo-westward-vow
  drogo-westward-vow --CAUSES--> drogo-blood-magic-ritual   [MEDIATED: vow -> Lhazar slave-raid (to fund ships) -> Drogo wounded -> ritual; verifier: CAUSES vs ENABLES]
  drogo-blood-magic-ritual --CAUSES--> death-of-khal-drogo
  death-of-khal-drogo --TRIGGERS--> dragon-hatching-on-drogo-pyre
Agency (Tier-2, pending verify):
  the-wine-merchant-attempts-to-poison-dany --MOTIVATES--> drogo
  mirri-maz-duur --SACRIFICES--> rhaego   (magic dyad; Rhaego is the life the ritual paid)

Role edges (Tier-1):
  robert-baratheon  --AGENT_IN-->  robert-orders-daenerys-assassination
  daenerys-targaryen --VICTIM_IN-> robert-orders-daenerys-assassination
  drogo             --AGENT_IN-->  drogo-westward-vow
  mirri-maz-duur    --AGENT_IN-->  drogo-blood-magic-ritual
  drogo             --VICTIM_IN--> drogo-blood-magic-ritual
  rhaego            --VICTIM_IN--> drogo-blood-magic-ritual
  daenerys-targaryen --AGENT_IN--> death-of-khal-drogo   (she smothers him)
  drogo             --VICTIM_IN--> death-of-khal-drogo
  daenerys-targaryen --AGENT_IN--> dragon-hatching-on-drogo-pyre   (walks into the fire)
  mirri-maz-duur    --VICTIM_IN--> dragon-hatching-on-drogo-pyre   (burned on the pyre)

CAUSES vs TRIGGERS: death->hatching is TRIGGERS (immediate spark -- Drogo's death
is the direct occasion for the pyre; Dany builds it for his body and walks in).
ritual->death is CAUSES (mediated -- the husk-state leaves Dany no choice but the
mercy-killing; her decision intervenes). order->attempt is CAUSES (the order is
executed through Varys's channels at Vaes Dothrak). attempt->vow is CAUSES (Drogo's
rage at the threat to wife and son drives the vow, mediated by his decision).

ROOT-CHECK (machine 5b): the arc's earliest beat, robert-orders-daenerys-assassination,
is a STANDALONE root by design -- Robert acts on learning of Daenerys's pregnancy,
which is not a modeled event. Declared intentional (like Balon's death, S116). The
dragon-birth half (E1) is rooted at drogo-westward-vow (E4's terminus), so E1 is NOT
self-contained -- the cross-half join is wired here, avoiding the S114 missed-root bug.

HARD-STOP: arc terminates at dragon-hatching-on-drogo-pyre. The downstream Slaver's
Bay campaign (fall-of-astapor -> Meereen -> Sons of the Harpy, decomposition E2/E3)
is its own juncture, built later. Staying causal-dark beyond the hatching is correct.

Re-run safe: refuses to append if run_id already present.
"""
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-essos-root-arc-2026-06-21.jsonl"

RUN_ID = "causal-arc-essos-root-20260621"
PRODUCED_AT = "2026-06-21T00:00:00+00:00"
# Fresh-subagent verify ran 2026-06-21 (S119): 5 CONFIRM, 1 REJECT (order->cancel
# dropped -- the order is the OBJECT of the cancellation, not its cause), 2 ADJUST
# (vow->ritual CAUSES->ENABLES; death->hatching TRIGGERS->CAUSES). Surviving causal
# edges carry the CONFIRM stamp below.
VERIFIED = "subagent-local-source-check-2026-06-21"
COMMON = {
    "decision": "emit_edge",
    "candidate_kind": "causal-curator-arc",
    "evidence_kind": "book-pass1",
    "typed_by": "curator-causal-arc",
    "schema_version": "pass1-derived-v1",
    "produced_at": PRODUCED_AT,
    "run_id": RUN_ID,
}

# slugs
ORDER = "robert-orders-daenerys-assassination"
WINE = "the-wine-merchant-attempts-to-poison-dany"
CANCEL = "ned-orders-daenerys-s-assassination-cancelled"
VOW = "drogo-westward-vow"
RITUAL = "drogo-blood-magic-ritual"
DEATH = "death-of-khal-drogo"
HATCH = "dragon-hatching-on-drogo-pyre"
ROBERT = "robert-baratheon"
DANY = "daenerys-targaryen"
DROGO = "drogo"
MIRRI = "mirri-maz-duur"
RHAEGO = "rhaego"

# (src, etype, tgt, tier, book, chapter, line, quote, asserted, verified)
EDGES_SPEC = [
    # --- causal spine (Tier-2, pending verify) ---
    (ORDER, "CAUSES", WINE, 2, "agot", "agot-eddard-08", 13,
     "I want them dead, mother and child both, and that fool Viserys as well. Is that plain enough for you? I want them dead.",
     "Robert's small-council order to kill the pregnant Daenerys is carried out through Varys's channels; its first execution is the poisoned-wine attempt at Vaes Dothrak. Order -> sanctioned attempt, mediated by the agent network => CAUSES Tier-2.",
     VERIFIED),
    # [REJECTED by fresh-verify 2026-06-21: order->cancel was CAUSES, but the order
    #  is the OBJECT of the cancellation, not its cause -- the cancellation's true
    #  cause is Robert's deathbed change of heart (unmodeled). Edge dropped.]
    (WINE, "CAUSES", VOW, 2, "agot", "agot-daenerys-06", 153,
     "The Usurper has woken the dragon now, she told herself … and her eyes went to the dragon's eggs resting in their nest of dark velvet.",
     "The poisoning attempt enrages Drogo at the threat to his wife and unborn son; he answers it with his public vow to cross the poison water and take the Iron Throne. Attempt -> vow, mediated by Drogo's decision => CAUSES Tier-2.",
     VERIFIED),
    (VOW, "ENABLES", RITUAL, 2, "agot", "agot-daenerys-08", 39,
     "\"He fell from his horse,\" Haggo said, staring down.",
     "The westward vow commits Drogo's khalasar to the march that includes the Lhazareen slave-raid, where Drogo takes the wound that festers and drives Daenerys to Mirri's blood magic. Fresh-verify 2026-06-21 ADJUSTED CAUSES->ENABLES: the wound came from a contingent battle with Khal Ogo (agot-daenerys-07:31), so the vow sets the conditions for the chain but does not mechanically cause the ritual. ENABLES Tier-2 -- the E4->E1 hinge.",
     VERIFIED),
    (RITUAL, "CAUSES", DEATH, 2, "agot", "agot-daenerys-09", 163,
     "His eyes were wide open but did not see, and she knew at once that he was blind. When she whispered his name, he did not seem to hear.",
     "Mirri's sabotaged ritual does not heal Drogo -- it leaves him a breathing, mindless husk. Unwilling to leave her sun-and-stars in that state, Daenerys ends his life. Ritual-as-cause -> death, mediated by Dany's mercy-killing decision => CAUSES Tier-2.",
     VERIFIED),
    (DEATH, "CAUSES", HATCH, 2, "agot", "agot-daenerys-10", 73,
     "The sun was going down when she called them back to carry his body to the pyre. ... They laid him down on his cushions and silks, his head toward the Mother of Mountains.",
     "Drogo's death is the occasion for the funeral pyre on which the dragons hatch: Dany builds the pyre for his body, sets the petrified eggs around him, binds Mirri to the wood, and walks into the flames. Fresh-verify 2026-06-21 ADJUSTED TRIGGERS->CAUSES: too many deliberate steps (pyre-building, egg-placement, Dany entering the fire) mediate between the death and the hatching for an immediate spark. CAUSES Tier-2.",
     VERIFIED),
    # --- agency (Tier-2, pending verify) ---
    (WINE, "MOTIVATES", DROGO, 2, "agot", "agot-daenerys-06", 179,
     "I will take my khalasar west to where the world ends, and ride the wooden horses across the black salt water as no khal has done before.",
     "The attempt on his wife and unborn son is what mobilizes Drogo: his vow of westward conquest is his personal answer to the Usurper's poison. Event -> actor => MOTIVATES Tier-2 (carries Drogo's agency, distinct from the attempt->vow CAUSES edge).",
     VERIFIED),
    (MIRRI, "SACRIFICES", RHAEGO, 2, "agot", "agot-daenerys-09", 115,
     "I drew him forth myself. He was scaled like a lizard, blind, with the stub of a tail and small leather wings like the wings of a bat. ... He had been dead for years.",
     "Mirri Maz Duur's blood magic takes the life of Daenerys's unborn son Rhaego as the price for the spell -- her vengeance for the sack of her temple. \"Only death can pay for life.\" Ritual killing with supernatural purpose, sacrificer -> victim => SACRIFICES Tier-2.",
     VERIFIED),
    # --- role edges (Tier-1): beat robert-orders ---
    (ROBERT, "AGENT_IN", ORDER, 1, "agot", "agot-eddard-08", 13,
     "I want them dead, mother and child both, and that fool Viserys as well.",
     "Robert Baratheon is the one who gives the assassination order at the small council. Role edge => AGENT_IN Tier-1.",
     None),
    (DANY, "VICTIM_IN", ORDER, 1, "agot", "agot-eddard-08", 13,
     "The whore is pregnant! ... I want them dead, mother and child both.",
     "Daenerys (with her unborn child) is the target of the order. Role edge => VICTIM_IN Tier-1.",
     None),
    # --- role edges (Tier-1): beat drogo-westward-vow ---
    (DROGO, "AGENT_IN", VOW, 1, "agot", "agot-daenerys-06", 179,
     "This I vow, I, Drogo son of Bharbo. This I swear before the Mother of Mountains, as the stars look down in witness.",
     "Khal Drogo is the vow-maker who swears the westward oath. Role edge => AGENT_IN Tier-1.",
     None),
    # --- role edges (Tier-1): beat drogo-blood-magic-ritual ---
    (MIRRI, "AGENT_IN", RITUAL, 1, "agot", "agot-daenerys-08", 193,
     "The maegi nodded solemnly. \"As you speak, so it shall be done. Call your servants.\"",
     "Mirri Maz Duur performs the blood-magic ritual. Role edge => AGENT_IN Tier-1.",
     None),
    (DROGO, "VICTIM_IN", RITUAL, 1, "agot", "agot-daenerys-08", 151,
     "She went to Drogo burning on his mat, and gazed long at his wound. \"Ask or tell, it makes no matter. He is beyond a healer's skills.\"",
     "Drogo is the subject of the failed healing ritual. Role edge => VICTIM_IN Tier-1.",
     None),
    (RHAEGO, "VICTIM_IN", RITUAL, 1, "agot", "agot-daenerys-09", 115,
     "I drew him forth myself. ... When I touched him, the flesh sloughed off the bone, and inside he was full of graveworms and the stink of corruption.",
     "Rhaego, the unborn son, dies as the ritual's blood price. Role edge => VICTIM_IN Tier-1.",
     None),
    # --- role edges (Tier-1): beat death-of-khal-drogo ---
    (DANY, "AGENT_IN", DEATH, 1, "agot", "agot-daenerys-09", 213,
     "She knelt, kissed Drogo on the lips, and pressed the cushion down across his face.",
     "Daenerys performs the mercy-killing, smothering Drogo with a cushion. Role edge => AGENT_IN Tier-1.",
     None),
    (DROGO, "VICTIM_IN", DEATH, 1, "agot", "agot-daenerys-09", 213,
     "She knelt, kissed Drogo on the lips, and pressed the cushion down across his face.",
     "Drogo is the one who dies. Role edge => VICTIM_IN Tier-1.",
     None),
    # --- role edges (Tier-1): beat dragon-hatching-on-drogo-pyre ---
    (DANY, "AGENT_IN", HATCH, 1, "agot", "agot-daenerys-10", 117,
     "I am Daenerys Stormborn, daughter of dragons, bride of dragons, mother of dragons, don't you see?",
     "Daenerys builds the pyre, places the eggs, walks into the fire, and wakes the dragons. Role edge => AGENT_IN Tier-1.",
     None),
    (MIRRI, "VICTIM_IN", HATCH, 1, "agot", "agot-daenerys-10", 91,
     "The godswife did not cry out as they dragged her to Khal Drogo's pyre and staked her down amidst his treasures. Dany poured the oil over the woman's head herself.",
     "Mirri Maz Duur is bound to the pyre and burned alive as part of the rite. Role edge => VICTIM_IN Tier-1.",
     None),
]


def make_row(spec):
    src, etype, tgt, tier, book, chap, line, quote, asserted, verified = spec
    row = {
        "edge_type": etype,
        "source_slug": src,
        "target_slug": tgt,
        **COMMON,
        "evidence_book": book,
        "evidence_chapter": chap,
        "evidence_ref": f"sources/chapters/{book}/{chap}.md:{line}",
        "evidence_quote": quote,
        "confidence_tier": tier,
        "asserted_relation": asserted,
    }
    if verified is not None:
        row["verified_by"] = verified
    return row


def main():
    lines = EDGES.read_text(encoding="utf-8").splitlines()
    if any(RUN_ID in ln for ln in lines):
        sys.exit(f"ABORT: run_id {RUN_ID} already present in {EDGES} — already minted.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)

    new_rows = [make_row(s) for s in EDGES_SPEC]

    with open(EDGES, "a", encoding="utf-8") as f:
        for row in new_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    n_causal = sum(1 for s in EDGES_SPEC if s[1] in ("CAUSES", "TRIGGERS", "MOTIVATES", "SACRIFICES", "ENABLES"))
    n_role = len(EDGES_SPEC) - n_causal
    print(f"Backed up -> {BACKUP.name}")
    print(f"Appended {len(new_rows)} edges ({n_causal} causal/agency Tier-2 pending-verify + {n_role} role Tier-1).")
    print(f"edges.jsonl now: {len(lines) + len(new_rows)} lines (was {len(lines)}).")


if __name__ == "__main__":
    main()
