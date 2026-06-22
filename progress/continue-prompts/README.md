# Continue-Prompts Triage Manifest

**Generated:** 2026-06-22 (refreshed after S122)  
**Rule:** `worklog.md` is the authoritative state file. When a prompt's claims contradict it, the prompt is marked STALE or DONE — the prompt's *content* is left unchanged per the hard rule above.  
**Status vocabulary:** LIVE | DONE | STALE-superseded-by-\<what\> | MERGED-into-worklog | HALTED-gated-on-\<what\>

---

## Active Prompts (sorted: LIVE → HALTED → STALE → DONE)

> **Hygiene policy (FIRM — Matt, recurring: "two continue prompts is confusing"):** the live dir holds the **ONE actionable next track** — not a menu. DONE/STALE prompts AND parked tracks (gated-on-Matt or lower-priority backlog) all `git mv` to `archive/` (kept, organized, recoverable). A parked track's context lives in `worklog.md` / `working/todos.md`; restore its prompt from `archive/` when it becomes the next thing. Never present multiple co-equal "next" prompts at session close.

| Filename | Date | Track | Status | Recommended Model | Note |
|----------|------|-------|--------|-------------------|------|
| `2026-06-22-chat-ui-personality-design.md` | 2026-06-22 | Chat-UI personality / voice design (front-end track) | **LIVE** | Sonnet 4.6 | **New S122, Matt-opened.** Design the persona/voice the chat UI uses to answer ASOIAF questions over the graph. DESIGN session (no graph mutation). Draft 2–3 candidate personas + sample transcripts → settle open questions (voice register, persona identity, spoiler stance, citation/Tier behavior, tone, boundaries, audience) with Matt → write `working/chat-ui/personality-spec.md`. **Genuinely independent of the graph-build track** — different domain (front-end vs graph internals), runs in its own window any order. (`chat-ui-architecture.md` is a STALE sketch — not spec.) |

---

## Archive (`archive/` subfolder — 39 files)

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

## Open threads right now (ONE live track + an open graph-container pick)

> The live dir holds ONE track: the chat-UI front-end design. The graph-build track is **between containers** —
> WO5K-remainder shipped S123, and the next container (NORTH / AEGON / Bran) is **Matt's pick**, so no live
> graph prompt exists yet (writing one before the pick would be a premature menu). When Matt picks, a decomp-dip
> prompt is written for that container (template: `working/wo5k-decomposition.md` / `working/essos-decomposition.md`).

**LIVE (front-end): `2026-06-22-chat-ui-personality-design.md`** — Matt wants to start designing the **personality/voice
the chat UI uses** to answer ASOIAF questions over the graph. DESIGN session (no graph mutation): draft 2–3 candidate
personas + sample transcripts, settle the open questions (voice register / persona identity / spoiler stance / citation+Tier
behavior / tone / boundaries / audience) with Matt, write `working/chat-ui/personality-spec.md`. (**Sonnet 4.6**)

**GRAPH track — between containers (no live prompt):** WO5K is spine-complete (S123: Q5+J2+J9+J7+J4 built).
Remaining containers per the S122 SET `{essos✓, wo5k✓, north, aegon, bran}`: **NORTH** (Theon/Reek + Bolton +
Stannis-marches), **AEGON** (Golden Company landing; fix the `PART_OF war-of-the-five-kings` edge-hygiene bug first),
**Bran** (greenfield flight-to-the-north spine). Each needs its own decomp dip first; **Matt picks which**. (**Sonnet 4.6**)

*Parked/stale in `archive/` (recoverable, not deleted): arc-wave1-mint (**STALE — parent-hub model superseded by chain-as-arc**; its drafted Red-Wedding/Joffrey arcs are candidates for the chain machine), edge-modeling-plate-4 Track B (backlog).*
*Done & archived (no longer live): causal-edges-and-spark-nodes strategy (S105), next-move-decisions (S104), Track 3 dating leftovers (S102), historical-anchor #9 wave 2 (S100), script-consolidation S1+S2 (S98/S99), Mode 3 dip + graph-cleanup (S96), infobox-merge-ship (S94).*
