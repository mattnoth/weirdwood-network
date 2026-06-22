# SESSION 130 — BRAN spine build (causal arc mint)

> **This is Session 130.** Stamp your worklog entry `### Session 130` at endsession.

> **Recommended model:** Sonnet 4.6 (Opus 4.8 orchestrator + Sonnet-class `general-purpose` subagents: 1–2 research dips + 1 independent fresh-verify). Same arc-mint machine as the NORTH (S125/S126) and AEGON (S128) spine builds.

## Goal
Build the BRAN causal spine from **`working/bran-decomposition.md`** (the S129 read-only dip — read it first; it IS the spec). The container `bran` is **greenfield**: Spine 1 (the fall) is partially built and forks into WO5K; **Spine 2 (the entire flight → journey-north → greenseer arc) is 0 event nodes.** This build lights it.

## Read first (in order)
- `working/bran-decomposition.md` — the full spec: §1 verified graph-state, §2 trigger-tree, §3 scorecard (BR1–BR7), §5 **ranked build order**, §6 seams, §7 nodes-to-mint table, §8 harvest. **Build in §5 rank order.**
- `working/aegon-decomposition.md` + the S128 worklog entry — the machine in action (build-step 0 housekeeping → ranked arcs → fresh-verify).
- `working/causal-arc-strategy-2026-06-18.md` — the agency-collapse check + CAUSES-vs-TRIGGERS rule + the **pre-mint dedup gate** (run every candidate slug through `event_alias_resolver.py --lookup`, eyeball ≥0.6, before minting).

## Build-step 0 (housekeeping — do FIRST, before any arc)
1. **Tag the untagged Spine-1 seam:** `bran-s-direwolf-kills-the-assassin` → add `containers: [bran, wo5k]` (it owns the CAUSES fork into the WO5K Tyrion chain; currently untagged).
2. **Retag the flight pivot:** `sack-of-winterfell` → `[wo5k, north, bran]` (add `bran`; ATTACH Bran's flight, do NOT rebuild the Theon thread).
3. **Backfill `brynden-rivers` aliases** (empty today): add "Bloodraven", "Lord Bloodraven", "Lord Brynden", "Three-eyed crow", "The last greenseer" → then run `weirwood refresh` (alias change requires a resolver rebuild — without it the greenseer node is query-invisible by its common names).
4. **Flag, do NOT fix:** the suspicious cross-theater `sack-of-winterfell --[PRECEDES]--> purple-wedding` edge (likely a wiki-ingestion artifact; review, decide at build).
5. **Slug discipline:** new wolf role edges target `summer` (NOT the orphan `brans-direwolf` slug the catspaw edges use). All greenseer/crow edges target `brynden-rivers` (NOT the `three-eyed-crow` **species** node — slug trap).

## Ranked build (from `working/bran-decomposition.md` §5 — ~8–9 mints; recommend 2 batches)
**Batch A (off the two existing anchors):**
- **Rank 1 — BR3** `sack-of-winterfell CAUSES bran-and-rickon-survive-the-sack-in-the-crypts` (mint; acok-bran-07:47/:147) — opens Spine 2 off the built sack hub. Model Osha's side-switch (AGENT_IN) + Luwin's dying counsel as the TRIGGERS into BR4.
- **Rank 2 — BR1** `jaime-pushes-bran-from-the-tower TRIGGERS bran-s-coma-and-the-three-eyed-crow` (mint; agot-bran-03:107) [+ optional `bran-wakes-from-his-coma` :125, or fold as terminus] — roots the greenseer gift off the built fall spine. The crow = Bloodraven (light MOTIVATES/role on `brynden-rivers`, NOT a separate scene node).
- **Rank 7 — BR2** `jojen-reed-names-bran-a-warg` (mint; acok-bran-05:97/:113) — lowest causal load (a RECOGNITION, model `ENABLES`/recognition not CAUSES). Node-to-exist; slot in parallel to Spine 1.

**Batch B (the journey spine, top-down from the terminus):**
- **Rank 3 — BR7** `bran-becomes-a-greenseer` (mint; adwd-bran-03:157/:167) — the CONTAINER TERMINUS, Q=2. Bran AGENT_IN; leaf + brynden-rivers instruct. Co-build with BR6.
- **Rank 4 — BR5** `bran-passes-the-black-gate` (asos-bran-04:317) + `bran-meets-coldhands` (adwd-bran-01:211) — dual-POV (Sam). `samwell-tarly ENABLES` the gate (only a sworn brother opens it).
- **Rank 5 — BR6** `bran-reaches-the-cave-of-the-three-eyed-crow` (adwd-bran-02:195/:205; wight-attack a sub-beat at :91) — `leaf AGENT_IN` rescue, `bran-stark AGENT_IN` (wargs Hodor).
- **Rank 6 — BR4** `bran-s-party-splits-from-rickon` (acok-bran-07:207) — connective; `jojen-reed MOTIVATES` via greendreams.

**Granularity discipline:** lean coarse where sub-beats add no causal value (the §4 granularity-overclaim rule). The §7 mint table lists 8–9 nodes; the build decides exact count (BR1-wake fold, BR5/BR6 split). **Run the pre-mint dedup gate on every slug.**

## The machine (per arc)
research dip (dedup + line-checked quotes + edge proposal, VERIFY vs `edges.jsonl` not node prose) → orchestrator mints via a `scripts/mint_bran_*.py` script (backup + re-run guard) → node aliases as natural SPACED phrases → targeted index + alias rebuild → **independent fresh-subagent verify** (causal `verified_by: pending` until CONFIRM; verifier adjudicates CAUSES/TRIGGERS/ENABLES + agency-collapse) → `--causal-chain`/`--full-chain` smoke test → citation-check (`verify-edge-quotes`, 0 drift required).

## Harvest (20 `bran-dip` rows already in `working/harvest-queue.md`)
These are the `## Quotes` / `## Appearances & Description` source material for the new beat nodes — ground every minted BR-beat with its Tier-1 anchor quote from this set (the AEGON/NORTH pattern). The Bloodraven appearance/place rows (adwd-bran-02:191/:193, adwd-bran-03:115) upgrade `brynden-rivers` after step-0 alias backfill. Consume/flip rows as you attach. PUSH the harvest snippet into any text-reading subagent (they don't load CLAUDE.md).

## Spoiler / tier discipline (HARD)
Map only WHAT HAPPENS (fall, coma, warging, flight, journey, cave, paste, greenseer) at Tier 1–2. Route **Night-King / greenseer-cosmology / time-travel / hodor-origin / Bloodraven-succession** speculation to the GATED theories track — NEVER a causal node or edge. The textual fact (reaches cave, eats paste, sees through trees) is in scope; what it *means* is not.

## Vocabulary (PASTE into every naming/sequencing subagent — they do NOT load CLAUDE.md)
Edge types = locked set: CAUSES / TRIGGERS / ENABLES / MOTIVATES / CONSPIRES_WITH (+ roles AGENT_IN / VICTIM_IN / COMMANDS_IN / WITNESS_IN / GUARDS / WIELDED_IN). "Pass" = corpus sweep · "Track" = named workstream · lowercase "step" = ordered piece · "Tier" = confidence 1–5 ONLY. No new capitalized terms.

## Dyad note
`working/dyad-queue.md` D3 (Bran↔Jojen greendreaming bond) is a relationship dyad, NOT part of this causal build — consume on demand in a later enrichment pass. The greendreams attach as MOTIVATES edges on BR4/BR5 directly; the spine roots fine without the dyad.

## At session end (S130 endsession)
Update worklog (S130 entry; **archive the oldest Session-Log entry per rule #8** — after this endsession, archive026 holds 3/5 [S122–S124], so S125 archives next). Archive this prompt. Open question for Matt: BRAN was the last of the 5 approved containers — next graph track is the **low-value remainders** (AEGON Euron/Victarion downstream wire; NORTH N6 Stannis-marches-south; the Bran greenseer enrichment / Rickon-Skagos deferral) OR a new direction (theories track? chat-UI persona? — both parked).

## DO NOT
- Refetch wiki / any HTTP call · rebuild the NORTH/WO5K Theon-sack nodes (ATTACH only) · mint CAUSES between sibling/sequence beats (granularity overclaim) · collapse the agency beats (Osha's side-switch, Luwin's counsel, Jojen's greendreams, Bran wargs Hodor — model them) · pull greenseer-cosmology theories into the causal map · wire greenseer edges to the `three-eyed-crow` species node (use `brynden-rivers`) · `/endsession` without explicit permission.
