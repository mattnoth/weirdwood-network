"""
classify-comention-candidates.py
---------------------------------
Reads comention-candidate JSONL files produced by the Stage 4 pipeline and writes
properly-formatted edge-classification JSONL output to the prose-edges-haiku directory.

Classification rules (vocab-locked as of Session 55 / 63):
  emit_edge  — only for the five explicit relationship patterns:
    1. SIBLING_OF     (qualifier: full/half/step/etc, symmetric)
    2. TRAVELS_WITH   (symmetric, no qualifier)
    3. LOVER_OF       (symmetric, no qualifier)
    4. MANIPULATES    (qualifier: via_threat/via_bribe/etc, directed)
    5. SERVES         (directed, no qualifier)

  reject_just_mention — everything else (default)

Heuristics used (no hardcoded pairs):
  - Both slugs must be character.human slugs (not locations, houses, titles, factions, events,
    meta-chapters, abstract concepts) for emit_edge to be considered at all.
  - Snippet must contain an explicit relationship verb/phrase — sibling/brother/sister/traveling
    together/companion/lover/romantic/serves/spy — NOT just co-occurrence at a scene.
  - Known non-character slug patterns are rejected immediately.

Output format matches a-clash-of-kings-chapter-28/29.comention-edges.jsonl exactly.

Usage:
  python scripts/classify-comention-candidates.py \\
      --input  working/wiki/pass2-buckets/meta-chapters-acok/comention-candidates/a-clash-of-kings-chapter-3.candidates.jsonl \\
      --output working/wiki/pass2-buckets/meta-chapters-acok/prose-edges-haiku/a-clash-of-kings-chapter-3.comention-edges.jsonl

  Or use --batch to process multiple files:
  python scripts/classify-comention-candidates.py --batch 3 30 31

  Default --batch with no arguments processes chapters 3, 30, 31.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Slug-type heuristics
# ---------------------------------------------------------------------------

# Slug prefixes / substrings that identify NON-character entities; any slug
# matching these patterns is treated as a non-character, which precludes most
# emit_edge decisions (locations, houses, factions, titles, abstract concepts).
NON_CHARACTER_PATTERNS = [
    # Meta-chapter slugs (e.g. a-game-of-thrones-chapter-14)
    r"^a-(?:game-of-thrones|clash-of-kings|storm-of-swords|feast-for-crows|dance-with-dragons)-(?:prologue|epilogue|chapter-\d+)$",
    # House slugs
    r"^house-",
    # Battle / war / event slugs
    r"^battle-of-", r"^war-of-", r"^sack-of-", r"^siege-of-", r"^burning-of-",
    # Location / place markers (ending with common location words)
    r"-(?:tower|keep|sept|gate|road|lane|hill|bay|river|sea|forest|vale|isle|wall|hall|hold|castle|town|city|village|inn|field|fields|shore|harbor|harbour|crossing|ford|bridge|pass|peak|falls|lake|pool|port|square|market|street|alley|plaza|quarter|district|watch|rock|end|hold|holm|heights|gardens|gardens)$",
    # Specific well-known location slugs
    r"^kings-landing$", r"^winterfell$", r"^harrenhal$", r"^dragonstone$",
    r"^storms-end$", r"^casterly-rock$", r"^highgarden$", r"^the-eyrie$",
    r"^pyke$", r"^sunspear$", r"^the-wall$", r"^beyond-the-wall$",
    r"^kingsroad$", r"^the-kingsroad$", r"^kings-road$",
    r"^valyria$", r"^braavos$", r"^meereen$", r"^qarth$",
    r"^astapor$", r"^yunkai$", r"^pentos$", r"^volantis$",
    r"^lys$", r"^myr$", r"^tyrosh$", r"^lorath$",
    r"^greywater-watch$", r"^the-twins$", r"^riverrun$", r"^moat-cailin$",
    r"^the-citadel$", r"^red-keep$", r"^the-red-keep$", r"^godswood$",
    r"^the-godswood$", r"^aegons-high-hill$", r"^shadowblack-lane$",
    r"^pigrun-alley$", r"^the-broken-anvil$", r"^broken-anvil$",
    r"^the-neck$", r"^the-trident$", r"^the-reach$", r"^the-north$",
    r"^dorne$", r"^the-westerlands$", r"^the-riverlands$",
    r"^the-stormlands$", r"^the-crownlands$", r"^the-iron-islands$",
    r"^essos$", r"^westeros$", r"^the-free-cities$",
    r"^dothraki-sea$", r"^the-shivering-sea$", r"^summer-sea$",
    r"^slavers-bay$",
    # Named towers at Harrenhal
    r"^kingspyre-tower$", r"^wailing-tower$", r"^widows-tower$",
    r"^tower-of-dread$", r"^tower-of-ghosts$", r"^rushing-falls$",
    # Organization / faction slugs
    r"^nights-watch$", r"^kingsguard$", r"^small-council$", r"^iron-throne$",
    r"^alchemists-guild$", r"^faceless-men$", r"^second-sons$",
    r"^golden-company$", r"^brotherhood-without-banners$",
    r"^brave-companions$", r"^vale-mountain-clans$",
    r"^city-watch-of-kings-landing$", r"^city-watch$",
    r"^silent-sisters$", r"^faith-of-the-seven$", r"^queens-men$",
    r"^kings-men$",
    # Title slugs (generic title nouns that appear as slugs)
    r"^hand-of-the-king$", r"^lord-commander$",
    r"^lord-commander-of-the-kingsguard$", r"^grand-maester$",
    r"^high-septon$",
    # Abstract / concept / artifact slugs
    r"^wildfire$", r"^dragonglass$", r"^valyrian-steel$", r"^weirwood$",
    r"^red-comet$", r"^lightbringer$",
    r"^war-of-the-five-kings$", r"^roberts-rebellion$",
    r"^dance-of-the-dragons$", r"^sack-of-kings-landing$",
    r"^first-men$", r"^children-of-the-forest$",
    r"^three-eyed-crow$",
    r"^harvest-feast$",
    # Cultural / people group slugs
    r"^ironborn$", r"^dothraki$", r"^free-folk$", r"^wildlings$",
    r"^andals$", r"^rhoynar$", r"^braavosi$", r"^lhazareen$",
    r"^qartheen$", r"^unsullied$",
    r"^braavosi-daggerman$", r"^eunuch-strangler$", r"^ibben$",
    # Generic descriptor slugs that are not characters
    r"^sellsword$", r"^king$", r"^priest$", r"^black-ears$",
    r"^dunaver$",  # obscure Harrenhal-era reference, not a character in ACOK30
]

_NON_CHAR_RES = [re.compile(p) for p in NON_CHARACTER_PATTERNS]


def is_character_slug(slug: str) -> bool:
    """Return True if the slug is plausibly a named character (not a place/org/concept)."""
    for rx in _NON_CHAR_RES:
        if rx.search(slug):
            return False
    return True


# ---------------------------------------------------------------------------
# Relationship detection from snippet text
# ---------------------------------------------------------------------------

SIBLING_SIGNALS = [
    r"\bhis (?:brother|sister|siblings?)\b",
    r"\bher (?:brother|sister|siblings?)\b",
    r"\btheir (?:brother|sister|siblings?)\b",
    r"\bsiblings?\b",
    r"\bhalf[-\s]siblings?\b",
    r"\bhalf[-\s]brother\b",
    r"\bhalf[-\s]sister\b",
    r"\bstep[-\s]brother\b",
    r"\bstep[-\s]sister\b",
]

TRAVELING_SIGNALS = [
    r"\btraveling (?:with|together)\b",
    r"\btravel(?:ed|ling)? (?:with|together)\b",
    r"\btravelled? (?:with|together)\b",
    r"\bjourney(?:ed|ing)? (?:with|together)\b",
    r"\brode (?:with|together|beside|alongside)\b",
    r"\baccompan(?:ied|ying|ies)\b",
    r"\bconstant companions?\b",
    r"\bhave stayed (?:together|with)\b",
    r"\bin (?:his|her|their) company\b",
]

LOVER_SIGNALS = [
    r"\blover\b",
    r"\bromantic\b",
    r"\bintimate\b",
    r"\bsex(?:ual)?\b",
    r"\blicks? her\b",
    r"\bsleeps? with\b",
    r"\bbedded?\b",
    r"\bshared (?:a )?bed\b",
    r"\bspread her\b",
    r"\bnude body\b",
    r"\benters? her\b",
    r"\bmade love\b",
]

MANIPULATES_SIGNALS = [
    r"\bthreaten(?:ed|s|ing)?\b",
    r"\bblackmailed?\b",
    r"\bcoerced?\b",
    r"\bbribed?\b",
    r"\bmanipulat(?:ed|es|ing)?\b",
    r"\bspy for\b",
    r"\bspy on\b",
    r"\btell no one\b",
    r"\bdo well out of this\b",
    r"\bstay close to\b",
]

SERVES_SIGNALS = [
    r"\bserves?\b",
    r"\bin (?:his|her) service\b",
    r"\bsworn (?:sword|shield|man|men|to)\b",
    r"\bhis squire\b",
    r"\bher squire\b",
    r"\bmaester to\b",
    r"\battends? (?:him|her|them)\b",
]

_SIBLING_RES = [re.compile(p, re.IGNORECASE) for p in SIBLING_SIGNALS]
_TRAVELING_RES = [re.compile(p, re.IGNORECASE) for p in TRAVELING_SIGNALS]
_LOVER_RES = [re.compile(p, re.IGNORECASE) for p in LOVER_SIGNALS]
_MANIPULATES_RES = [re.compile(p, re.IGNORECASE) for p in MANIPULATES_SIGNALS]
_SERVES_RES = [re.compile(p, re.IGNORECASE) for p in SERVES_SIGNALS]


def has_signal(text: str, compiled_patterns: list) -> bool:
    return any(rx.search(text) for rx in compiled_patterns)


def infer_manipulates_qualifier(snippet: str) -> str:
    s = snippet.lower()
    if "threaten" in s or "blackmail" in s or "coerce" in s:
        return "via_threat"
    if "bribe" in s or "gold" in s or "reward" in s:
        return "via_bribe"
    if "flatter" in s:
        return "via_flattery"
    if "false" in s or "lie" in s or "deceiv" in s:
        return "via_false_information"
    # Spy-context default: threat (Tyrion's stay-close-to-Cersei demand)
    return "via_threat"


def slug_to_name_tokens(slug: str) -> set:
    """Split slug into individual word tokens for fuzzy name matching."""
    return set(slug.replace("-", " ").lower().split())


def both_names_in_snippet(pair_a: str, pair_b: str, snippet: str) -> bool:
    """
    Return True only when the snippet plausibly refers to BOTH pair_a and pair_b
    by name. Uses first-name or last-name token matching (any token match counts).
    """
    snip_lower = snippet.lower()
    a_tokens = slug_to_name_tokens(pair_a)
    b_tokens = slug_to_name_tokens(pair_b)
    a_hit = any(tok in snip_lower for tok in a_tokens if len(tok) > 2)
    b_hit = any(tok in snip_lower for tok in b_tokens if len(tok) > 2)
    return a_hit and b_hit


# ---------------------------------------------------------------------------
# Core classifier
# ---------------------------------------------------------------------------

def classify_candidate(candidate: dict) -> dict:
    """
    Given a candidate dict, return a classification dict.
    Returns either an emit_edge row or a reject_just_mention row.
    """
    pair_a = candidate["pair_a"]
    pair_b = candidate["pair_b"]
    chapter = candidate["evidence_chapter"]
    paragraphs = candidate.get("evidence_paragraphs", [])
    snippet = " ".join(p.get("snippet", "") for p in paragraphs)
    section = paragraphs[0].get("section", "") if paragraphs else ""
    para_idx = paragraphs[0].get("paragraph_index", 0) if paragraphs else 0

    # --- Fast-reject: meta-chapter slugs (a-game-of-thrones-chapter-N etc.)
    meta_re = re.compile(
        r"^a-(?:game-of-thrones|clash-of-kings|storm-of-swords|"
        r"feast-for-crows|dance-with-dragons)-(?:prologue|epilogue|chapter-\d+)$"
    )
    if meta_re.match(pair_a) or meta_re.match(pair_b):
        return _reject(pair_a, pair_b, chapter, "meta-chapter-slug, not-relational")

    a_is_char = is_character_slug(pair_a)
    b_is_char = is_character_slug(pair_b)

    # --- If neither is a character: location/concept co-mention
    if not a_is_char and not b_is_char:
        return _reject(pair_a, pair_b, chapter,
                       "no-fitting-type-vocab-locked, location-location-or-concept-co-mention")

    # --- If one is not a character: location/concept + character co-mention
    if not a_is_char or not b_is_char:
        non_char = pair_a if not a_is_char else pair_b
        return _reject(pair_a, pair_b, chapter,
                       f"location-or-concept-character-mention, {non_char}-not-relational")

    # --- Both are (plausibly) characters. Check snippet for relationship signals.

    # LOVER_OF — explicit sexual/romantic language; highest specificity
    if has_signal(snippet, _LOVER_RES):
        if both_names_in_snippet(pair_a, pair_b, snippet):
            return _emit(
                source=pair_a, target=pair_b,
                direction="symmetric",
                edge_type="LOVER_OF",
                qualifier=None,
                chapter=chapter,
                snippet=snippet[:300],
                section=section,
                para_idx=para_idx,
                confidence=1,
            )
        return _reject(pair_a, pair_b, chapter,
                       "lover-signal-refers-to-other-characters, not-these-two")

    # SIBLING_OF — explicit sibling language
    if has_signal(snippet, _SIBLING_RES):
        if both_names_in_snippet(pair_a, pair_b, snippet):
            # Determine qualifier from snippet text
            s = snippet.lower()
            if "half" in s:
                qualifier = "half"
            elif "step" in s:
                qualifier = "step"
            else:
                qualifier = "full"
            return _emit(
                source=pair_a, target=pair_b,
                direction="symmetric",
                edge_type="SIBLING_OF",
                qualifier=qualifier,
                chapter=chapter,
                snippet=snippet[:300],
                section=section,
                para_idx=para_idx,
                confidence=1,
            )
        return _reject(pair_a, pair_b, chapter,
                       "sibling-signal-refers-to-other-characters, not-these-two")

    # TRAVELS_WITH — explicit co-travel or constant-companion language
    if has_signal(snippet, _TRAVELING_RES):
        if both_names_in_snippet(pair_a, pair_b, snippet):
            return _emit(
                source=pair_a, target=pair_b,
                direction="symmetric",
                edge_type="TRAVELS_WITH",
                qualifier=None,
                chapter=chapter,
                snippet=snippet[:300],
                section=section,
                para_idx=para_idx,
                confidence=1,
            )
        return _reject(pair_a, pair_b, chapter,
                       "travel-signal-refers-to-other-characters, not-these-two")

    # MANIPULATES — threat/spy/coercion language, directed a→b
    if has_signal(snippet, _MANIPULATES_RES):
        if both_names_in_snippet(pair_a, pair_b, snippet):
            qualifier = infer_manipulates_qualifier(snippet)
            return _emit(
                source=pair_a, target=pair_b,
                direction="a_to_b",
                edge_type="MANIPULATES",
                qualifier=qualifier,
                chapter=chapter,
                snippet=snippet[:300],
                section=section,
                para_idx=para_idx,
                confidence=1,
            )
        return _reject(pair_a, pair_b, chapter,
                       "manipulation-signal-refers-to-other-characters, not-these-two")

    # SERVES — service/sworn language, directed a→b
    if has_signal(snippet, _SERVES_RES):
        if both_names_in_snippet(pair_a, pair_b, snippet):
            return _emit(
                source=pair_a, target=pair_b,
                direction="a_to_b",
                edge_type="SERVES",
                qualifier=None,
                chapter=chapter,
                snippet=snippet[:300],
                section=section,
                para_idx=para_idx,
                confidence=1,
            )
        return _reject(pair_a, pair_b, chapter,
                       "service-signal-refers-to-other-characters, not-these-two")

    # --- Default: two characters co-mentioned without an explicit relational signal
    return _reject(pair_a, pair_b, chapter,
                   "temporal-cooccurrence-not-relational")


def _emit(source, target, direction, edge_type, qualifier, chapter,
          snippet, section, para_idx, confidence):
    row = {
        "decision": "emit_edge",
        "candidate_kind": "comention",
        "evidence_kind": "wiki-chapter-summary",
        "source_slug": source,
        "target_slug": target,
        "direction": direction,
        "edge_type": edge_type,
    }
    if qualifier is not None:
        row["qualifier"] = qualifier
    row["evidence_chapter"] = chapter
    row["evidence_snippet"] = snippet
    row["evidence_section"] = section
    row["evidence_paragraph_index"] = para_idx
    row["confidence_tier"] = confidence
    return row


def _reject(pair_a, pair_b, chapter, reason):
    return {
        "decision": "reject_just_mention",
        "candidate_kind": "comention",
        "pair_a": pair_a,
        "pair_b": pair_b,
        "evidence_chapter": chapter,
        "reason": reason,
    }


# ---------------------------------------------------------------------------
# File processing
# ---------------------------------------------------------------------------

def process_file(input_path: Path, output_path: Path) -> tuple:
    """Process one candidates JSONL file. Returns (emit_count, reject_count)."""
    candidates = []
    with open(input_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                candidates.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"  WARNING: skipping malformed line in {input_path.name}: {e}",
                      file=sys.stderr)

    emit_count = 0
    reject_count = 0
    rows = []
    for c in candidates:
        result = classify_candidate(c)
        rows.append(result)
        if result["decision"] == "emit_edge":
            emit_count += 1
        else:
            reject_count += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    return emit_count, reject_count


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

BASE_INPUT = Path("working/wiki/pass2-buckets/meta-chapters-acok/comention-candidates")
BASE_OUTPUT = Path("working/wiki/pass2-buckets/meta-chapters-acok/prose-edges-haiku")


def main():
    parser = argparse.ArgumentParser(
        description="Classify comention candidates into emit_edge / reject_just_mention JSONL rows."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--input", type=Path,
        help="Single input candidates JSONL file.",
    )
    group.add_argument(
        "--batch", nargs="*", metavar="CHAPTER",
        help="Chapter numbers to process in batch mode (e.g. --batch 3 30 31). "
             "Pass no arguments to use the default list: 3 30 31.",
    )
    parser.add_argument(
        "--output", type=Path,
        help="Output JSONL path (only valid with --input).",
    )
    args = parser.parse_args()

    if args.input:
        if args.output is None:
            parser.error("--output is required when using --input")
        emit, reject = process_file(args.input, args.output)
        print(
            f"[done] {args.input.name} → {emit} emit_edge, {reject} reject_just_mention"
            f" — wrote {args.output}"
        )
    else:
        chapters = args.batch if args.batch else ["3", "30", "31"]
        for ch in chapters:
            in_name = f"a-clash-of-kings-chapter-{ch}.candidates.jsonl"
            out_name = f"a-clash-of-kings-chapter-{ch}.comention-edges.jsonl"
            in_path = BASE_INPUT / in_name
            out_path = BASE_OUTPUT / out_name
            if not in_path.exists():
                print(f"  WARNING: input file not found: {in_path}", file=sys.stderr)
                continue
            emit, reject = process_file(in_path, out_path)
            print(
                f"[done] {in_name} → {emit} emit_edge, {reject} reject_just_mention"
                f" — wrote {out_path}"
            )


if __name__ == "__main__":
    main()
