---
session: 130
date: 2026-06-22
title: BRAN spine build — causal arc mint (the 5th & last approved container)
model: Opus 4.8 orchestrator + Sonnet-class general-purpose subagents (2 research dips + 2 fresh-verify)
track: containers / causal-arc-mint
---

# Session 130 — BRAN spine build

## Purpose

Build the BRAN causal spine from `working/bran-decomposition.md` (the S129 read-only dip = the spec).
BRAN was the **5th and last** of Matt's approved containers (`{essos, wo5k, north, aegon, bran}`) and the
only **greenfield** one — Spine 2 (the entire flight → journey-north → greenseer arc) had **0 event nodes**.
This session lit it end-to-end using the same arc-mint machine proven on NORTH (S125/S126) and AEGON (S128).

## What was built

**8 beat-nodes minted + 35 edges** (12 causal/agency Tier-2 + 23 role Tier-1), in 2 batches:

- **Batch A** (off the two existing anchors): BR3 `bran-and-rickon-survive-the-sack-in-the-crypts`
  (off the built `sack-of-winterfell` hub), BR1 `bran-s-coma-and-the-three-eyed-crow` (off the built fall
  spine), BR2 `jojen-reed-names-bran-a-warg`. 11 edges.
- **Batch B** (the journey, top-down from the terminus): BR4 `bran-s-party-splits-from-rickon`,
  BR5 `bran-passes-the-black-gate` + `bran-meets-coldhands`, BR6 `bran-reaches-the-cave-of-the-three-eyed-crow`,
  BR7 `bran-becomes-a-greenseer` (CONTAINER TERMINUS). 24 edges.

The full spine walks end-to-end: `--full-chain bran-becomes-a-greenseer` returns 9 hops
(sack → crypts → split → Black Gate → Coldhands → cave → greenseer); the coma chain joins the built fall spine.
Container `bran` 5 → 13 nodes. Graph 8,587 → 8,595 nodes, 22,441 → 22,476 edges. 0 new edge types (locked
vocab 132). 62 orphans unchanged. 0 citation drift across all 35 edges.

## Build-step 0 findings (two stale-spec corrections)

1. **`brynden-rivers` aliases were already present** (node_version 2: Bloodraven / the three-eyed crow /
   the last greenseer / Lord Brynden / Lord Rivers) and the resolver already resolved all common names.
   The S129 dip + continue prompt both claimed **empty aliases** requiring backfill + `weirwood refresh`.
   Per CLAUDE.md rule #9, trusted live state → the alias-backfill step was a **no-op**.
2. The "suspicious" `sack-of-winterfell --[PRECEDES]--> purple-wedding` edge the dip flagged as a likely
   wiki-ingestion artifact is in fact a legitimate **`derived-chronology` Tier-3** edge (299 AC → 300 AC)
   from the deterministic PRECEDES backbone — **not** an artifact. No fix.
3. Applied: tagged `bran-s-direwolf-kills-the-assassin` → `[bran, wo5k]`; retagged `sack-of-winterfell`
   → `[wo5k, north, bran]`.

## Design adjudications (the value of running the dips + fresh-verify)

- **BR1 waking-fold:** folded `bran-wakes-from-his-coma` into BR1 as the terminus rather than a separate
  node — the waking owns no distinct outgoing causal edge (it's the resolution of the same continuous
  dream-sequence). Mechanical test held: split only if the beat earns its own outgoing edge.
- **BR4 Luwin correction (key):** the spec assumed "Luwin's dying counsel TRIGGERS the split." The Batch-B
  research dip found the text does **not** support this — Luwin's dying lines are a dismissal + a mercy
  request; **Osha and the Reeds decide the split**. So BR3→BR4 is **ENABLES** (no named spark), not
  TRIGGERS. The BR3 node prose was corrected to match.
- **Journey topology:** all beat→beat links are **ENABLES** (continuous-journey preconditions) EXCEPT the
  single **CAUSES** BR6→BR7 (the paste + instruction genuinely transform Bran). Fresh-verify confirmed this
  is the one justified CAUSES in the chain.
- **Agency preserved (no collapse):** Osha's feigned defection (ENABLES + AGENT_IN), Jojen's greendreams
  (MOTIVATES), Bran wargs Hodor to fight the wights (AGENT_IN), Sam's oath opens the Black Gate (ENABLES —
  structurally load-bearing), Coldhands as Bloodraven's instrument (AGENT_IN the escort, never a causal driver).
- **Wight-attack fold:** folded into BR6 as an obstacle sub-beat (no downstream edge; the meeting is the
  load-bearing beat). Fresh-verify called it reasonable-but-borderline — splittable later if enrichment wants
  the warg-Hodor-in-combat moment as its own queryable beat.
- **Slug traps avoided:** all greenseer/crow edges target the character `brynden-rivers`, never the
  `three-eyed-crow` species node; wolf references use `summer`, never the orphan `brans-direwolf` slug.
- **BR1 Bloodraven-identity caveat (recorded, accepted):** the `brynden-rivers MOTIVATES coma` edge's
  identity (crow = Bloodraven) rests on ADWD-level canon, not the AGOT cite-chapter (which shows only "a
  three-eyed crow"). The MOTIVATES model is sound and the identity is correct; this is the lone edge whose
  target identity is established outside its cited chapter.

## Verification

Both batches independently fresh-verified by separate subagents against the local cache:
**12/12 causal/agency edges CONFIRM.** Batch A caught + fixed 1 cite drift (curly-quote / dialogue
discontinuity — patched 3 evidence_quotes to exact source substrings). All 35 edges pass `verify-edge-quotes`
(0 drift). `verified_by` flipped pending → `fresh-subagent-confirmed-s130`.

## Harvest

16 of the 20 `bran-dip` harvest rows consumed: 12 anchor quotes attached to the new beat-node `## Quotes`
blocks, + a **book-citation overlay onto the wiki-sourced `brynden-rivers` node** (his ADWD "half-corpse and
half-tree" cave-form appearance — adwd-bran-02:191/:193, adwd-bran-03:115 — previously wiki-only; plus a
book cite on his self-id quote, adwd-bran-03:19). The high-value Tier-2→Tier-1 provenance upgrade per
`feedback_book_citation_overlay_value`. 4 rows left open for a dedicated harvest pass (Old Nan Long-Night
foreshadowing, weirwood-paste food node, cave floor-bones place, the becoming-a-weirwood foreshadowing) +
the research subagents' own batchA/batchB rows.

## Matt's decisions this session

- **Next track:** low-value remainders first (AEGON Euron/Victarion downstream wire, NORTH N6
  Stannis-marches-south, Bran greenseer-enrichment / Rickon-Skagos), **then enrichment dips** (the
  arc-enrichment second-pass track — `project_arc_enrichment_track`).
- Ran `/endsession` with explicit permission.

## Scripts

- `scripts/mint_bran_spine_batchA_s130.py` (BR3/BR1/BR2)
- `scripts/mint_bran_spine_batchB_s130.py` (BR4/BR5/BR6/BR7)
- Backups: `graph/edges/_regrounding/edges-pre-bran-spine-batch{A,B}-2026-06-22.jsonl`
