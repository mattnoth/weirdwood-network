"""
classify-comention-adwd-41-45.py

Deterministic classifier for comention candidates in ADWD chapters 41-45.

Input:
  working/wiki/pass2-buckets/meta-chapters-adwd/comention-candidates/
    a-dance-with-dragons-chapter-{41..45}.candidates.jsonl

Output:
  working/wiki/pass2-buckets/meta-chapters-adwd/prose-edges-haiku/
    a-dance-with-dragons-chapter-{41..45}.comention-edges.jsonl

Classification logic is fully deterministic — all decisions are encoded
below based on close reading of the snippet evidence and ASOIAF canon.
Default: reject_just_mention (temporal-cooccurrence-not-relational).
Emit edges only for pairs where the snippet clearly establishes a graph
relationship per the Weirwood Network schema (architecture.md).

Chapter-by-chapter rationale
------------------------------
Chapter 41 (Theon/Reek at Winterfell):
  Two source paragraphs:
  - Crypts backstory paragraph: mentions aerys-ii, brandon-stark,
    catelyn-stark, dorne, eddard-stark, lyanna-stark, rickard-stark,
    riverrun, roberts-rebellion, tower-of-joy, willam-dustin. All are
    historical co-mentions inside a crypt-thoughts passage — pure temporal
    co-occurrence, no relational edges established.
  - Snowball/feast paragraph: barbrey-dustin, harwood-stout, hother-umber,
    house-bolton, house-stark, the-dornishmans-wife, wyman-manderly,
    barrowton, rills, weirwood, rickard-ryswell. Lords all co-attending
    the Winterfell feast — temporal co-presence at an event, no specific
    pairwise relationships inferable from the snippet alone.
  - Misc: jeyne-poole/sour-alyn (both locked away / near Bolton forces —
    snippet shows they are simply mentioned in the same paragraph about
    Theon's thoughts); ramsay-snow/sour-alyn (Ramsay sent Alyn to guard
    the room — the snippet truncates before making the custody relation
    explicit, only "sour-alyn" appears among those near the door; reject).
  ALL REJECT.

Chapter 42 (Asha at Deepwood Motte / Stannis march):
  One dominant paragraph: Stannis's host marching from Deepwood Motte
  toward Winterfell. Asha is chained and carried in the baggage train
  under guard by Alysane Mormont. This clearly establishes:
    - alysane-mormont GUARDS asha-greyjoy (custodian → subject)
  All other pairs (alysane/stannis, asha/winterfell, deepwood/wolfswood,
  etc.) are pure march co-presence — temporal.
  The balon-greyjoy/justin-massey and ironborn/justin-massey pairs come
  from a separate snippet where Asha reflects on past knee-bendings
  (historical musing) — temporal.
  EMIT: alysane-mormont GUARDS asha-greyjoy (1 edge).
  ALL OTHERS REJECT.

Chapter 43 (Daenerys in Meereen / Dornish envoys):
  Two source paragraphs:
  - Daario/Yunkai and Daenerys/Yunkai: political context, Dany
    negotiating or aware of Yunkai — temporal co-mention.
  - Dornish envoys paragraph: Daario introduces Dany to Quentyn
    Martell, Gerris Drinkwater, and Archibald Yronwood, described as
    three Dornishmen who have traveled together to bring gifts to the
    queen. The three traveled as a company from Dorne to Meereen.
    This clearly establishes TRAVELS_WITH for all three pairings:
      quentyn-martell + gerris-drinkwater
      quentyn-martell + archibald-yronwood
      gerris-drinkwater + archibald-yronwood
  - All other pairs in this paragraph (involving arianne-martell,
    oberyn-martell, viserys-targaryen, willem-darry, dorne) are
    historical/contextual references about Dornish political ties to
    Targaryens — not active relationships of the traveling trio.
  - house-martell/quaithe: Quaithe's prophecy is recalled by Dany —
    temporal/prophetic co-mention.
  EMIT: 3 TRAVELS_WITH edges. ALL OTHERS REJECT.

Chapter 44 (Jon at Castle Black — Alys Karstark arrives, Selyse arrives,
             Tycho Nestoris):
  Multiple source paragraphs, all with truncated ~199-char snippets:
  - Aemon/Gilly/Samwell paragraph: Tycho asks after Aemon, Gilly, Sam —
    historical/status inquiry. No relational edges, all temporal.
  - Alys Karstark paragraph: Alys arrives at Castle Black fleeing Arnolf
    (her treacherous uncle) and Cregan (her betrothed). The snippet shows
    only that these names appear in the same paragraph; the relational
    context (Arnolf is uncle, Cregan is betrothed) is established in
    canon but the truncated snippet does not explicitly surface the
    relationship verb. Per conservative policy (flag for human review
    rather than inferring from off-text knowledge), reject.
    Note: arnolf/alys and cregan/alys BETROTHED_TO / UNCLE_OF are valid
    canonical edges but belong in the wiki-infobox-derived layer, not
    derived from this truncated chapter-summary snippet.
  - Battle-in-the-Whispering-Wood paragraph: daryn-hornwood,
    harrion-karstark, jaime-lannister, roose-bolton co-mentioned as
    prisoners/participants of that battle — temporal historical.
  - Selyse / Axell / Shireen / Patchface / Tycho arriving at Castle
    Black: all co-mentioned in the same arrival paragraph — temporal
    co-presence, no specific pairwise relationship beyond traveling
    together in the queen's retinue. The "traveling together" inference
    is valid but the snippet's evidence_chapter is a Jon chapter
    (jon-snow is the POV); the arriving retinue is not described as
    explicitly "traveling together" to Castle Black — they arrive.
    ENCOUNTERS would require explicit staging verb per schema rules.
    Reject all as temporal.
  - Free-folk / Hardhome / others / mother-mole paragraph: temporal.
  - Iron Bank / Lannister / Stannis paragraph: political discussion,
    temporal.
  - Common-tongue / old-tongue / Wun Wun / Patrek paragraph: temporal.
  - Sellsword / Val / Winterfell paragraph: temporal.
  ALL REJECT.

Chapter 45 (Arya in Braavos):
  - arya-stark / nymeria-direwolf: Snippet explicitly says Arya wakes
    up "after entering into Nymeria again" — canonical warging/skinchange
    event. WARGS_INTO (arya-stark → nymeria-direwolf). Clear emit.
  - All other arya/braavos/house-of-black-and-white/skinchanger pairs:
    temporal setting co-mentions.
  - dareon / many-faced-god: Arya killed Dareon; co-mention of the
    Many-Faced God in the same paragraph is contextual, not relational.
  - elephant-ship / goodheart / free-folk / hardhome / sealord: ships
    mentioned in news Arya hears — temporal.
  - kindly-man / lys / pentos / high-valyrian / waif: training scene,
    languages learned — temporal.
  EMIT: arya-stark WARGS_INTO nymeria-direwolf (1 edge). ALL OTHERS REJECT.
"""

import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Repository root (relative to this script in scripts/)
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent

INPUT_DIR = REPO_ROOT / "working/wiki/pass2-buckets/meta-chapters-adwd/comention-candidates"
OUTPUT_DIR = REPO_ROOT / "working/wiki/pass2-buckets/meta-chapters-adwd/prose-edges-haiku"

CHAPTERS = [41, 42, 43, 44, 45]
BOOK_SLUG_PREFIX = "a-dance-with-dragons-chapter-"


# ---------------------------------------------------------------------------
# Emit-edge decisions
# Each entry: (chapter, pair_a, pair_b) → edge_dict override fields.
# pair_a / pair_b must match the candidates JSONL exactly (alphabetical order
# as produced by the candidate builder).
#
# Fields populated here:
#   source_slug, target_slug, direction, edge_type, confidence_tier
# Fields auto-filled from candidate:
#   evidence_chapter, evidence_snippet, evidence_section,
#   evidence_paragraph_index
# Fixed fields:
#   decision="emit_edge", candidate_kind="comention",
#   evidence_kind="wiki-chapter-summary"
# ---------------------------------------------------------------------------
EMIT_DECISIONS = {
    # ------------------------------------------------------------------
    # Chapter 42: Asha is carried in baggage train "under guard by"
    # Alysane Mormont — custodian→subject relationship.
    # GUARDS schema: Custodian → Subject-of-custody. Tier-3 (no qualifier).
    # ------------------------------------------------------------------
    (42, "alysane-mormont", "asha-greyjoy"): {
        "source_slug": "alysane-mormont",
        "target_slug": "asha-greyjoy",
        "direction": "a_to_b",
        "edge_type": "GUARDS",
        "confidence_tier": 3,
    },

    # ------------------------------------------------------------------
    # Chapter 43: Quentyn, Gerris, and Archibald traveled together from
    # Dorne to Meereen as the Dornish envoy company ("three Dornishmen").
    # TRAVELS_WITH schema: Symmetric. Tier-3 (no qualifier).
    # All three pairings from the candidate file:
    # ------------------------------------------------------------------
    (43, "archibald-yronwood", "gerris-drinkwater"): {
        "source_slug": "archibald-yronwood",
        "target_slug": "gerris-drinkwater",
        "direction": "symmetric",
        "edge_type": "TRAVELS_WITH",
        "confidence_tier": 3,
    },
    (43, "archibald-yronwood", "quentyn-martell"): {
        "source_slug": "archibald-yronwood",
        "target_slug": "quentyn-martell",
        "direction": "symmetric",
        "edge_type": "TRAVELS_WITH",
        "confidence_tier": 3,
    },
    (43, "gerris-drinkwater", "quentyn-martell"): {
        "source_slug": "gerris-drinkwater",
        "target_slug": "quentyn-martell",
        "direction": "symmetric",
        "edge_type": "TRAVELS_WITH",
        "confidence_tier": 3,
    },

    # ------------------------------------------------------------------
    # Chapter 45: Arya wakes after "entering into Nymeria again" —
    # explicit skinchange/warg event.
    # WARGS_INTO schema: Warg → Vessel. Direction a_to_b. Tier-3.
    # ------------------------------------------------------------------
    (45, "arya-stark", "nymeria-direwolf"): {
        "source_slug": "arya-stark",
        "target_slug": "nymeria-direwolf",
        "direction": "a_to_b",
        "edge_type": "WARGS_INTO",
        "confidence_tier": 3,
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_reject(candidate: dict) -> dict:
    return {
        "decision": "reject_just_mention",
        "candidate_kind": "comention",
        "pair_a": candidate["pair_a"],
        "pair_b": candidate["pair_b"],
        "evidence_chapter": candidate["evidence_chapter"],
        "reason": "temporal-cooccurrence-not-relational",
    }


def make_emit(candidate: dict, override: dict) -> dict:
    # Pull best evidence paragraph (first one)
    ep = candidate["evidence_paragraphs"][0] if candidate["evidence_paragraphs"] else {}
    record = {
        "decision": "emit_edge",
        "candidate_kind": "comention",
        "evidence_kind": "wiki-chapter-summary",
        # override fields:
        "source_slug": override["source_slug"],
        "target_slug": override["target_slug"],
        "direction": override["direction"],
        "edge_type": override["edge_type"],
        "evidence_chapter": candidate["evidence_chapter"],
        "evidence_snippet": ep.get("snippet", ""),
        "evidence_section": ep.get("section", ""),
        "evidence_paragraph_index": ep.get("paragraph_index", 0),
        "confidence_tier": override["confidence_tier"],
    }
    return record


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def classify_file(chapter_num: int) -> tuple[int, int]:
    """
    Classify one chapter's candidates file. Returns (n_emit, n_reject).
    """
    slug = f"{BOOK_SLUG_PREFIX}{chapter_num}"
    in_path = INPUT_DIR / f"{slug}.candidates.jsonl"
    out_path = OUTPUT_DIR / f"{slug}.comention-edges.jsonl"

    if not in_path.exists():
        print(f"  WARNING: input not found: {in_path}", file=sys.stderr)
        return 0, 0

    candidates = []
    with in_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                candidates.append(json.loads(line))

    if not candidates:
        print(f"  {slug}: 0 candidates — skipping output file")
        return 0, 0

    n_emit = 0
    n_reject = 0
    output_lines = []

    for cand in candidates:
        pair_a = cand["pair_a"]
        pair_b = cand["pair_b"]
        key = (chapter_num, pair_a, pair_b)

        if key in EMIT_DECISIONS:
            record = make_emit(cand, EMIT_DECISIONS[key])
            n_emit += 1
        else:
            record = make_reject(cand)
            n_reject += 1

        output_lines.append(json.dumps(record, ensure_ascii=False))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        fh.write("\n".join(output_lines) + "\n")

    return n_emit, n_reject


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_emit = 0
    total_reject = 0

    for ch in CHAPTERS:
        slug = f"{BOOK_SLUG_PREFIX}{ch}"
        n_emit, n_reject = classify_file(ch)
        total_emit += n_emit
        total_reject += n_reject
        print(f"{slug} → {n_emit} emit_edge, {n_reject} reject_just_mention")

    print()
    print(f"Total: {total_emit} emit_edge, {total_reject} reject_just_mention "
          f"({total_emit + total_reject} candidates processed)")


if __name__ == "__main__":
    main()
