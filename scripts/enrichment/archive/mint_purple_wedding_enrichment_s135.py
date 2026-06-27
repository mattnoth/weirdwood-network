#!/usr/bin/env python3
"""Mint Purple Wedding enrichment pass 1 (S135) — third major-arc enrichment dip.

Synthesis of 4 fresh Sonnet lenses (downstream-causal / secondary-char+SUSPECTED_OF /
descriptive-object-depth / existing-node↔existing-node causal-wiring) over the built
Purple Wedding cluster. PROPOSE-only lenses → orchestrator (Opus) synthesized +
line-checked every cite against the source files → this mint set.

Mints 16 edges, NO new nodes (the proposed silver-hairnet + alayne-stone-identity
nodes are DEFERRED to a future Vale/object dip — this pass is edge-only). The 4-lens
proposal carried 9 causal/agency/suspicion candidates; an INDEPENDENT fresh-verify
(sonnet-fresh-verify-s135) CONFIRMED 6 and REJECTED 3 (see bottom). Final set:

  6 causal/agency/suspicion (verified=sonnet-fresh-verify-s135):
    - littlefinger-brokers-tyrell-lannister-alliance ENABLES joffrey-sets-sansa-aside-...
    - petyr-baelish MOTIVATES olenna-tyrell                              (the framing-motive)
    - death-of-joffrey-baratheon ENABLES wedding-of-tommen-...-margaery  (downstream seam)
    - death-of-joffrey-baratheon TRIGGERS littlefinger-smuggles-sansa-...
    - tyrion-lannister SUSPECTED_OF death-of-joffrey-baratheon           (whodunit layer)
    - sansa-stark SUSPECTED_OF death-of-joffrey-baratheon
 10 role/structural/object (Tier-1 facts, verified=None):
    - killing-of-dontos-hollard SUB_BEAT_OF purple-wedding
    - 5 WITNESS_IN death-of-joffrey (sansa, tyrion, margaery, tommen, loras)
    - joffrey-baratheon OWNS widows-wail · OWNS wedding-chalice
    - strangler WIELDED_IN death-of-joffrey · wedding-chalice WIELDED_IN death-of-joffrey

REJECTED at fresh-verify (3 — proposed + line-checked OK, but refuted on causal grounds):
  - joffrey-sets-sansa-aside ENABLES death-of-joffrey — too distal / collapses Olenna's
    agency; the motive is already carried by `petyr MOTIVATES olenna` + Olenna AGENT_IN.
  - killing-of-dontos-hollard ENABLES littlefinger-smuggles-sansa — TEMPORAL INVERSION:
    Dontos is shot AFTER Sansa is already aboard the galley; the kill can't enable the escape.
  - littlefinger-smuggles-sansa ENABLES wedding-of-petyr-baelish-and-lysa-arryn — incidental
    co-location; the Petyr-Lysa wedding was planned independently of Sansa's presence.

Rejected / re-routed at synthesis (logged, not minted):
  - betrothal ENABLES tyrell-plot-revealed — WRONG TARGET: `tyrell-plot-revealed` is
    the plot to spirit Sansa to Highgarden to wed WILLAS, not the kill-Joffrey conspiracy.
    The murder-motive seam re-routed to ENABLES death + petyr MOTIVATES olenna instead.
  - tyrion-accused SUSPECTED_OF tyrion (lens1) — backwards direction; use actor→event form.
  - sansa-receives-hairnet DECEIVES sansa (lens1) — event→person DECEIVES, schema-loose.
  - widows-wail OWNS joffrey / wedding-chalice OWNS joffrey — backwards; flipped to joffrey OWNS.
  - widows-wail WIELDED_IN death — the sword was present but did not kill (poison did); dropped.
  - tyrion-accused MOTIVATES bronn — tenuous (cite shows Bronn's Stokeworth supper, not motive).
  - olenna WITNESS_IN death — redundant with her AGENT_IN (she engineered it).
  - new nodes silver-hairnet-of-sansa-stark, sansa-assumes-alayne-stone-identity — DEFERRED.

Safeguards mirror mint_red_wedding_enrichment_s134.py: backup, re-run guard, slug pre-check.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
BACKUP = REPO / "graph" / "edges" / "_regrounding" / "edges-pre-purple-wedding-enrichment-2026-06-23.jsonl"

RUN_ID = "purple-wedding-enrichment-s135"
PRODUCED_AT = "2026-06-23T00:00:00+00:00"


def common():
    return {
        "decision": "emit_edge",
        "candidate_kind": "enrichment-curator-arc",
        "evidence_kind": "book-pass1",
        "typed_by": "curator-pw-enrichment",
        "schema_version": "pass1-derived-v1",
        "produced_at": PRODUCED_AT,
        "run_id": RUN_ID,
    }


# (source, edge_type, target, tier, book, chap_id, line, quote, asserted, verified_or_None)
EDGES_SPEC = [
    # ════════ CAUSAL / AGENCY / CROSS-ARC (7) — verified=pending → fresh-verify ════════
    ("littlefinger-brokers-tyrell-lannister-alliance", "ENABLES",
     "joffrey-sets-sansa-aside-and-agrees-to-wed-margaery", 2,
     "acok", "acok-tyrion-08", 113,
     "The Stark girl brings Joffrey nothing but her body, sweet as that may be. Margaery Tyrell "
     "brings fifty thousand swords and all the strength of Highgarden.",
     "The Tyrell-Lannister alliance Littlefinger brokered is the precondition for Joffrey setting "
     "Sansa aside to wed Margaery — the substitution that placed Margaery in Joffrey's power. ENABLES "
     "(the council still chose to proceed).",
     "sonnet-fresh-verify-s135"),
    ("petyr-baelish", "MOTIVATES", "olenna-tyrell", 2,
     "asos", "asos-sansa-06", 187,
     "she let her lord son bluster while she asked pointed questions about Joffrey's nature.",
     "Littlefinger seeded Olenna's decision: at Highgarden his men 'spread disturbing tales' about "
     "Joffrey's nature and he 'planted the notion' of the plot. Agency-routing edge — his framing "
     "motivated her choice to act; she retains agency.",
     "sonnet-fresh-verify-s135"),
    ("death-of-joffrey-baratheon", "ENABLES",
     "wedding-of-tommen-i-baratheon-and-margaery-tyrell", 2,
     "asos", "asos-sansa-06", 193,
     "but he did not need Joffrey. We shall have another wedding soon, wait and see. Margaery will "
     "marry Tommen.",
     "Littlefinger states on-page that Joffrey's death is the enabling condition for Tommen's "
     "accession and the Tommen-Margaery wedding (the marquee downstream node, previously 0 causal-in).",
     "sonnet-fresh-verify-s135"),
    ("death-of-joffrey-baratheon", "TRIGGERS",
     "littlefinger-smuggles-sansa-out-of-kings-landing", 2,
     "asos", "asos-sansa-05", 47,
     "Hush, you'll be the death of us. I did nothing. Come, we must away, they'll search for you. Your "
     "husband's been arrested.",
     "Joffrey's death (and the arrest that follows) is the immediate trigger for Dontos to spirit "
     "Sansa out of the city that same night.",
     "sonnet-fresh-verify-s135"),

    # ════════ SUSPECTED_OF — the whodunit layer (2) — verified=pending ════════
    ("tyrion-lannister", "SUSPECTED_OF", "death-of-joffrey-baratheon", 2,
     "asos", "asos-tyrion-08", 323,
     "\"Arrest my brother,\" she commanded him. \"He did this, the dwarf. Him and his little wife. They "
     "killed my son.",
     "In-world false suspicion: Cersei's public accusation at the feast brands Tyrion the killer — the "
     "founding act of the realm-wide belief. The true agents (Olenna/Littlefinger) are wired AGENT_IN/"
     "COMMANDS_IN; this models who is BLAMED, not who did it. Node stays event.assassination.",
     "sonnet-fresh-verify-s135"),
    ("sansa-stark", "SUSPECTED_OF", "death-of-joffrey-baratheon", 2,
     "asos", "asos-sansa-05", 135,
     "Your disappearance will make them suspect you in Joffrey's death.",
     "Littlefinger predicts (and Tyrion's own reasoning confirms, asos-tyrion-09:61) that Sansa will be "
     "suspected because she fled and wore the hairnet — the second framed innocent. Models suspicion, "
     "not guilt.",
     "sonnet-fresh-verify-s135"),

    # ════════ STRUCTURAL — integrate the Dontos-silencing beat (1) ════════
    ("killing-of-dontos-hollard", "SUB_BEAT_OF", "purple-wedding", 1,
     "asos", "asos-sansa-05", 127,
     "Three men stepped to the gunwale, raised crossbows, fired. One bolt took Dontos in the chest as "
     "he looked up, punching through the left crown on his surcoat.",
     "Dontos is shot dead on the escape galley the same night — the silencing beat of the Purple "
     "Wedding plot. The node existed islanded (0 SUB_BEAT_OF); this integrates it into the cluster.",
     None),

    # ════════ WITNESS_IN death-of-joffrey (5) — Tier-1 on-page presence ════════
    ("sansa-stark", "WITNESS_IN", "death-of-joffrey-baratheon", 1,
     "asos", "asos-sansa-06", 15,
     "Whenever she closed her eyes she saw Joffrey tearing at his collar, clawing at the soft skin of "
     "his throat, dying with flakes of pie crust on his lips and wine stains on his doublet.",
     "Sansa was at the feast and watched Joffrey die; the image haunts her on the voyage out.",
     None),
    ("tyrion-lannister", "WITNESS_IN", "death-of-joffrey-baratheon", 1,
     "asos", "asos-tyrion-08", 305,
     "As he did, the boy's eyes met Tyrion's. He has Jaime's eyes. Only he had never seen Jaime look so "
     "scared.",
     "Tyrion (POV) watches Joffrey die at close range — eye contact established as the king expires.",
     None),
    ("margaery-tyrell", "WITNESS_IN", "death-of-joffrey-baratheon", 1,
     "asos", "asos-tyrion-08", 297,
     "\"He's choking,\" Queen Margaery gasped.",
     "Margaery, beside Joffrey at the pie-cutting, is the first to diagnose the death up close.",
     None),
    ("tommen-baratheon", "WITNESS_IN", "death-of-joffrey-baratheon", 1,
     "asos", "asos-tyrion-08", 301,
     "Prince Tommen was screaming and crying.",
     "Tommen was present at the feast and witnessed his brother's death.",
     None),
    ("loras-tyrell", "WITNESS_IN", "death-of-joffrey-baratheon", 1,
     "asos", "asos-tyrion-08", 321,
     "\"My lady?\" said Ser Loras Tyrell, uncertain.",
     "Loras, Kingsguard on the dais, is present through the death and the accusation that follows it.",
     None),

    # ════════ OBJECT EDGES — wire the cluster's artifacts (4) — Tier-1 ════════
    ("joffrey-baratheon", "OWNS", "widows-wail", 1,
     "asos", "asos-sansa-04", 93,
     "Lord Tywin waited until last to present the king with his own gift: a longsword.",
     "Tywin gifts the Valyrian-steel longsword (reforged from Ice) to Joffrey at the wedding-morning "
     "gift-giving; Joffrey names it Widow's Wail. First edge on the widows-wail node.",
     None),
    ("joffrey-baratheon", "OWNS", "wedding-chalice", 1,
     "asos", "asos-sansa-04", 81,
     "Lord Mace Tyrell came forward to present his gift: a golden chalice three feet tall, with two "
     "ornate curved handles and seven faces glittering with gemstones.",
     "Mace Tyrell gifts the seven-faced golden wedding chalice to Joffrey; he claims it at once. First "
     "edge on the wedding-chalice node.",
     None),
    ("strangler", "WIELDED_IN", "death-of-joffrey-baratheon", 1,
     "asos", "asos-sansa-05", 43,
     "No murder. He choked on his pigeon pie.\" Dontos chortled. \"Oh, tasty tasty pie. Silver and stones, "
     "that's all it was, silver and stone and magic.",
     "The Strangler — the amethyst-crystal poison palmed from Sansa's hairnet — is the actual murder "
     "instrument. First edge on the strangler node.",
     None),
    ("wedding-chalice", "WIELDED_IN", "death-of-joffrey-baratheon", 1,
     "asos", "asos-tyrion-08", 295,
     "The chalice slipped from his hand and dark red wine went running across the dais.",
     "The poisoned wine was delivered via the wedding chalice; it slips from Joffrey's hand as he dies "
     "— the delivery vessel of the dose.",
     None),
]


def make_edge_row(spec):
    (src, etype, tgt, tier, book, chap_id, line, quote, asserted, verified) = spec
    row = {
        "edge_type": etype,
        "source_slug": src,
        "target_slug": tgt,
        **common(),
        "evidence_book": book,
        "evidence_chapter": chap_id,
        "evidence_ref": f"sources/chapters/{book}/{chap_id}.md:{line}",
        "evidence_quote": quote,
        "confidence_tier": tier,
        "asserted_relation": asserted,
    }
    if verified is not None:
        row["verified_by"] = verified
    return row


def main():
    all_slugs = set()
    for (src, _, tgt, *_rest) in EDGES_SPEC:
        all_slugs.add(src)
        all_slugs.add(tgt)
    resolved, missing = precheck_slugs(all_slugs)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed — non-existent targets: {missing}")
    print(f"Slug pre-check OK: {len(resolved)} existing slugs resolved.")

    raw_lines = EDGES.read_text(encoding="utf-8").splitlines()
    existing_lines = [ln for ln in raw_lines if ln.strip()]
    if any(RUN_ID in ln for ln in existing_lines):
        sys.exit(f"ABORT: run_id '{RUN_ID}' already present — already minted.")
    print(f"Re-run guard OK: run_id '{RUN_ID}' not present.")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EDGES, BACKUP)
    print(f"Backup written → {BACKUP}")

    new_rows = [make_edge_row(spec) for spec in EDGES_SPEC]
    lines_before = len(existing_lines)
    all_out = existing_lines + [json.dumps(r, ensure_ascii=False) for r in new_rows]
    EDGES.write_text("\n".join(all_out) + "\n", encoding="utf-8")
    lines_after = len(all_out)

    type_counts = {}
    for spec in EDGES_SPEC:
        type_counts[spec[1]] = type_counts.get(spec[1], 0) + 1

    print("\n── SUMMARY ──")
    print(f"Edges appended ({len(new_rows)}):")
    for etype, cnt in sorted(type_counts.items()):
        print(f"  {etype}: {cnt}")
    print(f"edges.jsonl: {lines_before} → {lines_after} lines (+{len(new_rows)})")
    print(f"Backup: {BACKUP}")


if __name__ == "__main__":
    main()
