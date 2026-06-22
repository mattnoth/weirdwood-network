# Continue-Prompts Triage Manifest

**Generated:** 2026-06-22 (refreshed after S127)  
**Rule:** `worklog.md` is the authoritative state file. When a prompt's claims contradict it, the prompt is marked STALE or DONE — the prompt's *content* is left unchanged per the hard rule above.  
**Status vocabulary:** LIVE | DONE | STALE-superseded-by-\<what\> | MERGED-into-worklog | HALTED-gated-on-\<what\>

---

## Active Prompts (sorted: LIVE → HALTED → STALE → DONE)

> **Hygiene policy (FIRM — Matt, recurring: "two continue prompts is confusing"):** the live dir holds the **ONE actionable next track** — not a menu. DONE/STALE prompts AND parked tracks (gated-on-Matt or lower-priority backlog) all `git mv` to `archive/` (kept, organized, recoverable). A parked track's context lives in `worklog.md` / `working/todos.md`; restore its prompt from `archive/` when it becomes the next thing. Never present multiple co-equal "next" prompts at session close.

| Filename | Date | Track | Status | Recommended Model | Note |
|----------|------|-------|--------|-------------------|------|
| `2026-06-26-aegon-spine-build.md` | 2026-06-26 | AEGON spine build (graph track) | **LIVE** | Sonnet 4.6 | **New S127.** WRITES to graph — builds the AEGON causal spine from `working/aegon-decomposition.md` §5. **2 mints total** (`golden-company-sails-for-westeros`, `aegon-revealed-to-the-golden-company`); everything else is edge/role/tag wiring on existing nodes. Ranked: A2 sail-west→landing (1 mint, the CAUSES that lights the 6-node fan) → A4 Varys-assassinations→KL-attach (0 mints) → A3 Stormlands-campaign (0 mints; PART_OF is the right sibling structure) → A1 conspiracy-seed→reveal (1 mint + the `varys CONSPIRES_WITH illyrio` dyad). **Build-step 0 = fix the 2 mis-filed `PART_OF war-of-five-kings` edges + delete the suspicious `landing PRECEDES hizdahr-wedding` edge.** D1 dyad resolved dyad-only. Same arc-mint machine as NORTH/WO5K. |

---

## Archive (`archive/` subfolder — 44 files)

> **`2026-06-25-aegon-container-decomposition.md`** — archived S127. **DONE (S127):** the read-only AEGON decomposition dip ran → `working/aegon-decomposition.md` (8-section structure = NORTH template; junctures A1–A4). AEGON is entirely causally dark (all PART_OF/role scaffolding, 0 causal edges). **Scaffolding correction:** verified **6** PART_OF children, not the handoff's "8+". Top-3 = A2 sail-west (11/12, 1 mint) · A4 Varys-assassinations (11/12, 0 mints) · A3 Stormlands-campaign (9/12, 0 mints); **2 mints total**. D1 Varys↔Illyrio resolved **dyad-only**. 12 harvest pointers added. 0 graph writes (read-only contract held). Superseded as live by the AEGON spine build.
> **`2026-06-24-north-spine-build-n3-n4.md`** — archived S126. **DONE (S126):** built NORTH N3 (LC election → Slynt execution; minted `jon-elected-lord-commander`) + N4 (free folk → Pink Letter → stabbing; minted `jon-allows-free-folk-through-the-wall` + `pink-letter-delivered`) **+ executed the `mutiny-at-castle-black`→`jon-is-stabbed-repeatedly` merge** (loser→`same_as` redirect, survivor absorbed the tier-1 wiki Origins; junk PRECEDES dropped). +3 nodes / +9 edges −1 junk (22,424→22,432); agency-preserving topology (fresh-verify REJECTED any blunt free-folk→stabbing CAUSES — all routes through `MOTIVATES bowen-marsh` + the Pink-Letter TRIGGERS); 2 cites re-pointed at fresh-verify. Container north 13→17; **NORTH spine-complete (both termini wired).** Superseded as live by the AEGON decomp dip.
> **`2026-06-23-north-spine-build.md`** — archived S125. **DONE (S125):** built the NORTH top-3 (N5 Roose-Warden + N2 Stannis-at-the-Wall [enrich-not-mint: `battle-beneath-the-wall` already is the rout, so only the `stannis-moves-to-the-wall` bridge was minted] + N1 great-ranging-wire). +2 nodes / +13 edges (22,411→22,424); every causal edge fresh-verified (dropped N5 MOTIVATES; retyped N2 bridge→battle; downgraded attack→battle Tier-3; corrected N1 mutiny source to the Fist). Container north 2→13; WO5K→NORTH seam traverses end-to-end. Dedup resolved (canonical=`jon-is-stabbed-repeatedly`, merge deferred to N4). Harvest consume-pass ran (queue 0 open). Superseded as live by the N3+N4 build.
> **`2026-06-23-north-container-decomposition.md`** — archived S124. **DONE (S124):** the read-only NORTH decomposition dip ran → `working/north-decomposition.md` (603 lines; trigger-tree + scorecard + ranked build order). NORTH is greenfield, two spines (Jon's Watch arc + Bolton/Stannis political thread); 13 key junctures = 4 HIT-but-dark / 6 MISS / 2 partial. Top-3 = N5 Roose-Warden (11/12, 1 mint) · N2 Stannis-defeats-wildlings (11/12, 2 mints) · N1 great-ranging-wire (10/12, 0 mints). Superseded as the live prompt by the NORTH spine build.
> **`2026-06-22-chat-ui-personality-design.md`** — archived S123 (parked, recoverable). **PARKED:** Matt deprioritized the chat-UI persona/voice design ("side thing, will come back to it"). The design task is unchanged and self-contained — restore to live when Matt wants the front-end track. Not started.
> **`2026-06-22-wo5k-remainder-build.md`** — archived S123. **DONE (S123):** built all 4 WO5K-remainder junctures (Q5 + J2+J9 + J7 + J4) — +6 nodes / +27 edges (22,384→22,411), every causal/agency edge fresh-verified, 0 citation drift, 0 invented edge types. WO5K container now spine-complete; emergent cross-arc spine `balon-declares → … → robb-is-killed`. Verify-driven corrections: Q5 sack→capture, J7 source exec→murders + terminus=conspiracy, J2+J9 broker CAUSES→ENABLES, J4 −1 mint −2 edges. Next graph track = NORTH/AEGON/Bran (Matt picks; each needs its own decomp dip).
> **`2026-06-21-container-shape-analysis.md`** — archived S122. **DONE (S122):** ran the 4-lens container-split fan-out (API healthy; the S121 529 outage had blocked it). The fan-out REFUTED the proposal's 6-set — Matt's SET = **5 containers** (`essos, wo5k, north, aegon` + `bran` by Matt's override; `riverlands`/`kl-faith` fold to wo5k as downstream branches; iron-islands/dorne fold via seam tags). Stamps applied (`--container` wo5k 2→24). Superseded as the live prompt by the WO5K-remainder build.
> **`2026-06-21-essos-container-decomposition.md`** — archived S121. **STALE-superseded-by-`2026-06-21-container-shape-analysis.md`.** Was the 3-step (hardening → fan-out → build) plan; Step 1 HARDENING shipped in full S121 (graph-query flags + `containers:` field + littlefinger mint + wedding join-hub refactor + docs). Steps 2–3 were reframed: Matt split the container-SET decision into its own dedicated SHAPE-analysis session (shape > names). Kept for history; superseded banner added to the file head.
> **`2026-06-21-graph-hygiene-and-harvest.md`** — archived S118. **DONE (S118 maintenance):** step 1 ATTENDS relation-cleanup (7 edges retyped — 6 `PARTICIPATES_IN` + 1 `WITNESS_IN`, 2 retargeted; 0 new nodes [`tragedy-at-summerhall` already existed], 0 new vocab [`GARRISONS`/`HELD_AT` not in vocab]) + step 2 harvest consume-pass (26 rows → 21 attached / 3 parked / 2 flip-only; queue 0 open). Superseded as the live prompt by the Essos container decomposition.
> **`2026-06-18-causal-arc-execution.md`** — archived S117. **DONE (AFFC causal-arc spine phase, S112–S117):** the planned major-arc backlog track shipped all 4 AFFC arcs (#1 Cersei S114 · #3 Brienne→Stoneheart S115 · #2 Kingsmoot→Euron + first enrichment pass S116 · #4 Dorne/Myrcella S117). Holds the canonical **arc-mint machine** + policy/guardrails — restore/reference it for the Essos build. Superseded as the live prompt by the S117 maintenance pass → S118 hygiene → Essos.

Archive files are **DONE**, **STALE-superseded**, or **PARKED** (gated/backlog — recoverable; restore when next). Summary:

| Group | Files | Status |
|-------|-------|--------|
| `2026-06-20-harvest-pass.md` | 1 file | **DONE S110** — consumed all 28 `working/harvest-queue.md` rows into the graph (quotes/appearance/food/place/object + 1 ADVISES edge + milk-of-poppy retype), fresh-verified 23/24, flipped all rows to `done`. Proved the queue→graph half of the harvest mechanism. The harvest pass is **recurring/on-demand** — re-run when the queue re-accumulates (no standing live prompt; convention in memory `feedback_harvest_queue` + worklog NEXT TRACK). |
| `2026-06-17-causal-edges-and-spark-nodes.md` | 1 file | **DONE S105** — pure-analysis strategy delivered (`working/causal-arc-strategy-2026-06-18.md`) + second smoke-test arc (Bran's fall) built + 4-lens advisory board run. Superseded by the causal-arc-execution live track. |
| `2026-06-16-next-move-decisions.md` | 1 file | **DONE S104** — both remaining decisions resolved: #1 `PRECEDES` ordering edges SHIPPED (174); #2 causal pilot SHIPPED (2 `CAUSES` edges). Superseded by the causal-edges+spark-nodes live track. |
| `2026-06-15-arc-wave1-mint.md` | 1 file | **STALE-superseded-by-chain-as-arc (S106)** — its `event.conspiracy` umbrella-parent model is reversed by the S105/S106 chain-as-arc decision (arcs = causal chains queried via `--causal-chain`, NO parent hubs). Kept for historical reference only; do NOT restore as-is. The Red-Wedding/Joffrey arcs it drafted are now candidates for the chain-as-arc machine. (Prompt body unchanged per the manifest hard rule; staleness tracked here.) See memory `project_narrative_arc_reification`. |
| `2026-06-05-edge-modeling-plate-4-haiku-disposition.md` | 1 file | **PARKED S99** — post-Plate-5 backfill Track B (1,617 Haiku bulk re-bucketing); lower-priority backlog, de-prioritized by S96 dip. Context: `working/todos.md` Track B. |
| `2026-06-15-historical-anchor-wave2.md` | 1 file | **DONE S100** — wave 2 shipped: 4 WO5K hubs attached (siege-of-riverrun/battle-of-the-camps/battle-of-oxcross/melee-at-bitterbridge), +43 edges (21,950→21,993), validated + minted. `siege-of-storms-end` deferred (dup cluster). Wave 3 (deep-lore wiki-only) optional/low. |
| `2026-06-15-script-consolidation.md` | 1 file | **DONE S99** — Session 1 (pacer/orchestration) S98 + Session 2 (archive 30 one-offs/wrappers, `weirwood graph/resolve/refresh` aliasing, README universal-index refresh, design §0 fully BUILT) S99. |
| Stage-4 comention + events + design prompts (2026-05-02 → 2026-06-08) | 10 files | Archived S97 — DONE/STALE (comention deprecated S65; events absorbed into Track B; repo-audit done S92; alias-and-display was a chat export). Incl. the `2026-05-31-events-v2-promotion-chain/` folder. |
| Wiki Pass 2 Stage 1-3 prompts (2026-04-26 to 2026-04-27) | 6 files | DONE — wiki Pass 2 Stages 1-3 shipped (Sessions 20-27; 7,563+ nodes) |
| Tier 3 Pass E Phase 2 (2026-05-01) | 1 file | DONE — Path B promotion campaign complete (S28) |
| Pass 1 remaining books (2026-05-02 to 2026-05-04) | 4 files | DONE — all 5 books 344/344 (S30-S36) |
| Bug fix: chain/race bug (2026-05-04) | 1 file | DONE — extraction pipeline bugs fixed (S33) |
| Post-Pass-1 cleanup + direction (2026-05-06) | 1 file | DONE — cleanup executed; Stage 4 direction set |
| Missing-node backfill / wiki prose backfill (2026-05-12) | 2 files | DONE — node layer confirmed whole (S72 false-alarm resolution) |
| Events Haiku bulk monitor (2026-05-27) | 1 file | DONE — bulk run complete (S80); monitor no longer needed |

---

## Open threads right now (ONE live track — the AEGON spine build)

> The live dir holds ONE track: the AEGON spine build (writes to graph). The read-only AEGON decomp dip ran S127
> → `working/aegon-decomposition.md` (prompt archived). NORTH went spine-complete S126. The chat-UI persona track
> was parked S123 (Matt: "side thing, will come back to it") — in `archive/`, recoverable.

**LIVE (graph): `2026-06-26-aegon-spine-build.md`** — builds the AEGON causal spine from
`working/aegon-decomposition.md` §5. **2 mints total** (`golden-company-sails-for-westeros`,
`aegon-revealed-to-the-golden-company`); everything else is edge/role/tag wiring. Ranked A2→A4→A3→A1.
**Build-step 0 = fix the 2 mis-filed `PART_OF war-of-five-kings` edges + delete the suspicious
`landing PRECEDES hizdahr-wedding` edge.** D1 Varys↔Illyrio resolved dyad-only. Same arc-mint machine as NORTH/WO5K. (**Sonnet 4.6**)

**Queued behind it:** Bran (greenfield flight-to-the-north spine — its own decomp dip first). Building AEGON
also discharges the parked Varys/Illyrio (D1) + Jorah (D2) dyads. SET = `{essos✓, wo5k✓, north✓, aegon◐, bran}`.

*Parked/stale in `archive/` (recoverable, not deleted): arc-wave1-mint (**STALE — parent-hub model superseded by chain-as-arc**; its drafted Red-Wedding/Joffrey arcs are candidates for the chain machine), edge-modeling-plate-4 Track B (backlog).*
*Done & archived (no longer live): causal-edges-and-spark-nodes strategy (S105), next-move-decisions (S104), Track 3 dating leftovers (S102), historical-anchor #9 wave 2 (S100), script-consolidation S1+S2 (S98/S99), Mode 3 dip + graph-cleanup (S96), infobox-merge-ship (S94).*
