---
title: Plate 4 SUB_BEAT_OF validation sample
date: 2026-06-08
validator: Opus (validation pass, post-Haiku/Opus 2-pass classifier)
inputs:
  - working/edge-modeling/plate4-wiki-cluster/cluster-edges-staging.jsonl (46 edges; 43 SUB_BEAT_OF, 3 DUPLICATE_OF)
  - working/edge-modeling/plate3-full/minted-event-nodes/*.node.md
  - working/edge-modeling/plate3-full/role-edges-staging.jsonl
  - graph/nodes/events/*.node.md
sample_size: 15 SUB_BEAT_OF edges (5 tier-1, 5 tier-2, 5 random)
sampling_seed: random.seed(42)
---

## Verdicts

| # | mint_slug | target_wiki | tier | verdict | note |
|---|---|---|---|---|---|
| 1 | wedding-ceremony-in-the-royal-sept | wedding-of-tommen-i-baratheon-and-margaery-tyrell | 1 | correct | Wiki body explicitly names Tommen/Margaery wedding in Great Sept; ACOK/AFFC Cersei III is the ceremony chapter. |
| 2 | bolton-forces-attack | battle-outside-the-gates-of-winterfell | 1 | correct | Wiki body describes Rodrik Cassel marching on Winterfell; Bolton attack is the inciting beat (Theon VI). |
| 3 | anguy-kills-the-rooftop-sentinel | battle-at-the-burning-septry | 1 | correct | Wiki body names Anguy, Kyle, Notch slaying Mummer guards shortly before dawn — exact textual match. |
| 4 | jaime-lannister-is-captured-and-brought-before-catelyn | battle-in-the-whispering-wood | 1 | correct | Wiki body describes Jaime ambushed in Whispering Wood; AGOT Catelyn X is the capture POV. |
| 5 | fleet-forms-battle-lines | battle-of-the-blackwater | 1 | correct | Wiki body names Imry Florent commanding fleet entering river; Davos POV (ACOK Davos III) opens battle. |
| 6 | gendry-captured | fight-at-the-holdfast | 2 | correct | Wiki body explicitly references Gendry/recruits being captured at the holdfast; mint is just the capture beat. |
| 7 | crossbows-kill-more-northmen | red-wedding | 2 | correct | Crossbow volleys from the gallery are canonical Red Wedding mechanics (Catelyn VII). |
| 8 | taena-recounts-renly-s-wedding-night | wedding-of-renly-baratheon-and-margaery-tyrell | 2 | correct | Wiki body has Taena's recounting verbatim ("I helped disrobe him for the bedding…"). |
| 9 | catelyn-is-killed | red-wedding | 2 | correct | Catelyn's throat-cut is the climactic Red Wedding beat. |
| 10 | shadow-assassination-of-renly | siege-of-storms-end-299 | 2 | correct | Wiki body explicitly: "Renly is killed by a shadow" during siege at Storm's End. |
| 11 | gold-cloaks-betray-ned | arrest-of-eddard-stark | 2 | correct | Wiki body has Janos Slynt quote about spearing Tomard during the betrayal. |
| 12 | wedding-ceremony-begins-at-dawn | wedding-of-drogo-and-daenerys-targaryen | 1 | correct | Daenerys II is the wedding ceremony chapter; mint is a fine-grained beat. |
| 13 | arya-frees-the-prisoners | fight-at-the-holdfast | 2 | correct | Wiki body explicitly: "Arya decides to save Jaqen H'ghar, Rorge, and Biter … throws the weapon into the wagon". |
| 14 | a-knight-attacks-tyrion-s-shield | battle-of-the-blackwater | 2 | correct | ACOK Tyrion XIV = Blackwater. Mandon Moore attack on Tyrion during the sortie is canonical; mint phrasing is awkward but event-bucket correct. |
| 15 | mammoth-attacks-gate-below | attack-on-castle-black | 1 | correct | ASOS Jon VIII is the gate-defense beat; mammoth at gate is canonical. |

## Precision by tier

- **Tier 1 (direct-textual, Haiku quoted evidence):** 5/5 = 100%
- **Tier 2 (inference-only, Opus override):** 5/5 = 100%
- **Random:** 5/5 = 100% (3 tier-2, 2 tier-1)

Aggregate sample precision: **15/15 = 100%** (95% CI ≈ 78–100%).

## Failure patterns

None observed in this sample. Notes on the classifier's behavior:

1. **Tier-2 rationales are conservative-honest** — Opus consistently flags "candidate body excerpt does not explicitly quote X" when relying on chapter-alignment + participant-overlap. This is the right shape: high-recall match, transparent about inference.
2. **Mint titles are sometimes generic** ("wedding-ceremony", "a-knight-attacks-tyrion-s-shield") but role-edges + evidence_chapter disambiguate cleanly. The classifier successfully resolved generic mints to specific wiki events using participant overlap.
3. **No chronologically distant pairings observed**; chapter-bucket prefiltering apparently held.

## Recommendation

**(a) Auto-apply tier-1 at Plate 5.** Tier-1 is 5/5 with quoted textual evidence; safe to merge with no human review.

**For tier-2: also auto-apply, with a tag.** Tier-2 was 5/5 in this sample with consistently honest rationales. The risk profile is low because:
- Chapter-bucket prefilter constrains candidates to plausible matches.
- Opus rationales explicitly mark inference vs. quoted evidence.
- Sub-beat scoping is forgiving — even a "wrong specific beat" is usually within the right event family.

Recommend Plate 5 promote all 43 SUB_BEAT_OF with `evidence_strength` tagged from `confidence_tier` (1 = "textual", 2 = "inferential"). No re-run needed. A second 15-edge sample from a future plate-4 batch would be prudent before a fully unattended bulk run, but for this 43-edge batch the human-review cost outweighs the expected error cost.

**Caveats this validator cannot rule out:**
- N=15 sample on 43-edge population; the unsampled 28 edges (esp. tier-2 Red Wedding/Castle-Black hubs which dominate) are statistically similar but not individually checked.
- Did not validate the 3 DUPLICATE_OF edges (out of scope for this task) — these warrant their own quick check before Plate 5 since DUPLICATE_OF collapses two nodes.
