# Session 104 — PRECEDES ordering edges + causal TRIGGERS pilot (the 2 remaining next-move decisions)

**Date:** 2026-06-17
**Model:** Opus 4.8 orchestrator + 1 fresh `general-purpose` verification subagent
**Entry point:** `/continue next-move-decisions` → resolved decisions #1 and #2 from `2026-06-16-next-move-decisions.md`

---

## Purpose

The S102 advisory board left two next-move decisions open, both Matt's: **#1 `PRECEDES`/`FOLLOWS` ordering edges** and **#2 causal `TRIGGERS`/consequence edges**. This session opened by putting both to Matt, then executed both — #1 fully (deterministic), #2 as a curator-guided pilot. Mid-session Matt also changed the working method for interpretive edges (see §4).

---

## 1. Decision #1 — `PRECEDES` ordering edges

**Matt's three sub-calls:**
1. **Vocab:** add `PRECEDES` *only*. `FOLLOWS` is its exact inverse (read by reverse traversal — no need to store both); `OCCURRED_IN_YEAR` is dead (year-page nodes were deleted S102, so it would have no targets). New "Temporal & Sequencing" subsection in `architecture.md`; vocab 166 → **167**.
2. **Basis:** global year-chain, ordered by `occurred.ac_year`, with `narrative_first` as the same-year tiebreaker.
3. **Floater policy:** P2 "bridged" (chosen from a 3-option dry-run: P1 spine-only=36 edges but 73 events unordered; **P2=~170, every event positioned**; P3 full bipartite=1,183, bloaty).

**The modeling fork (why a dry-run was needed):** only **29 of 118** dated events carry `narrative_first`; the rest are "floaters" (year known, intra-year order unknown). The big clusters are mostly floaters (130 AC=12, 298=10, 299=15, 300=12). How aggressively to wire floaters into the chain changes both edge count and whether 73 events get *any* ordering — a real decision, surfaced to Matt with measured counts rather than guessed.

**The same-book correction (mid-run):** the first build (170 edges) produced a *flatly-wrong* edge — `red-wedding → wedding-of-renly` — because `narrative_first` is **reading order**, a proxy for in-world order that **breaks across books** (Renly's wedding happened before the Red Wedding but is narrated retrospectively in AFFC). Of 23 narrative-basis edges, 17 were same-book (reliable) and 6 cross-book (the risk zone). Matt chose **restrict-to-same-book**.

That couldn't be a naive 6-edge deletion: year 299's nf events span agot(3)→acok(10)→asos(5)→affc(1)→adwd(1), so dropping the cross-book links would **orphan ~16 middle-segment events** (incl. Red Wedding) from the timeline. The fix was a **unit model**: each `(year, book)` nf-run is a unit (internally chapter-chained); units within a year are mutually unordered; every year gets one representative event, and each unit's endpoints bridge by cross-year edge to the adjacent years' reps. Side benefit: because *every* year now has a rep, consecutive all-floater historical years (Dance era 129/130/131) are correctly ordered too — a gap the original P2 would have left.

**Result:** 174 edges (17 same-book narrative + 157 cross-year), Tier-3 (inherits the wiki-year-page dating ceiling), `evidence_kind: derived-chronology` (7th kind), `typed_by: python-chronology-chain`, each tagged `order_basis: narrative|cross-year`. Invariants verified: 0 backwards, cross-year strictly increasing, narrative pairs same-year+same-book, 0 cross-book narrative, single weakly-connected component (117/117). Script: `scripts/build-precedes-edges.py` (re-runnable, dry-run default). `red-wedding` now correctly chains `battle-near-yunkai → red-wedding → purple-wedding`.

## 2. Decision #2 — causal pilot (Robert's Rebellion)

The dip's measured gap: `battle-of-the-trident` had participants + a date but **0 consequence edges**. Investigation of the local wiki cache (`Robert's_Rebellion.json`, `Battle_of_the_Trident.json`, `Sack_of_King's_Landing.json`) gave the full causal spine — but found that the *spark half* of the chain (Lyanna's abduction → Brandon/Rickard executions → Aerys's demand → Jon Arryn's defiance) **has no nodes**, so most of it can't be expressed yet.

**Two well-evidenced links exist between coarse battle-level nodes**, emitted as **`CAUSES`** (Tier-2, `candidate_kind: causal-curator-pilot`):
- `battle-of-the-trident → sack-of-kings-landing`
- `sack-of-kings-landing → coronation-of-robert-i-baratheon`

**Key type finding:** `TRIGGERS` ("the *specific spark*") would *overclaim* at this granularity — the Sack's specific spark was Tywin's gate-opening (no node), one beat removed from the Trident. At coarse battle-node granularity the honest type is `CAUSES`. True `TRIGGERS` granularity needs the fine beat-nodes. Matt **deferred** minting the 3 spark nodes to a dedicated track.

## 3. PART_OF inversion bug (flagged, not fixed)

Noticed while reading edges: `roberts-rebellion` carries **9 inverted `PART_OF` edges** (war→battle) alongside the correct battle→war ones. Architecture direction is Battle→War. Out of scope this session — spawned as a background task (`task_e0a62b08`) to audit/drop graph-wide and check the emitter.

## 4. Method change — subagents verify edges, not Matt

Mid-session Matt: *"for remaining questions, use fresh subagents to check our local copy of wiki or books for confirmation — I cannot review individual edges routinely."* This is now a standing rule (memory `feedback_subagent_verify_not_matt`): interpretive/causal edges get an **adversarial fresh-subagent check against the LOCAL cache** (never refetch); Matt gates at policy level and gets summaries, not edge-lists.

Applied immediately to the 2 pilot edges. Verdicts: EDGE 1 **CONFIRM** (verbatim quote, sound direction); EDGE 2 **UNCERTAIN/keep-but-re-cite** — relation holds but the original quote evidenced succession generally, not Sack→Coronation. Re-cited to `Coronation_of_Robert_I_Baratheon` (*"Ser Jaime Lannister… killed Aerys… during the Sack of King's Landing in 283 AC."*). Both stamped `verified_by: subagent-local-source-check-20260617`.

---

## Graph state at close

- `edges.jsonl`: 21,993 → **22,169** (+174 PRECEDES, +2 CAUSES). Edge types: 125 → **127**. Evidence kinds: 6 → **7** (`derived-chronology`). Vocab: 166 → **167**.
- `--health`: 8,518 nodes, 22,169 edges, **62 orphans (unchanged — 0 new)**, fully traversable.
- pytest: **1297 pass / 1 fail** (the pre-existing environmental `cwd-is-tmp`; identical to S102 baseline).
- Backups: `graph/edges/_regrounding/edges-pre-{precedes,causal-pilot,recite}-2026-06-17.jsonl`.
- Edge-only mutation → no index/alias rebuild needed.

## What's next

Causal-edge work can now **scale** (per-edge human review is no longer the gate — fresh subagents verify against local sources). The natural continuation is the deferred **Robert's Rebellion spark-node track**: mint the 3 missing beat-nodes (`abduction-of-lyanna`, `execution-of-brandon-and-rickard-stark`, `aerys-demands-ned-and-robert`) with local-source evidence, rebuild indexes/alias-resolver (node ADD), then wire the full causal chain (now expressible as `TRIGGERS` at beat granularity) under the subagent-verification gate. This is also the narrative-arc-reification pattern applied to a historical arc. Continue: `progress/continue-prompts/2026-06-17-causal-edges-and-spark-nodes.md`.
