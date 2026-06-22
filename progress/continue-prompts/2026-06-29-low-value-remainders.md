# SESSION 131 — Low-value container remainders (then enrichment dips)

> **This is Session 131.** Stamp your worklog entry `### Session 131` at endsession.

> **Recommended model:** Sonnet 4.6 (Opus 4.8 orchestrator + Sonnet-class `general-purpose` subagents: research dip + independent fresh-verify). Same arc-mint machine as the NORTH (S125/S126), AEGON (S128), BRAN (S130) builds.

## Context
**All 5 approved containers are spine-complete** (essos / wo5k / north / aegon / bran). This track mops up the **low-value remainders** Matt deferred during the container builds. Matt's S130 directive: **low-value remainders first, THEN enrichment dips** (the arc-enrichment 2nd-pass track — see memory `project_arc_enrichment_track` + `working/arc-enrichment-backlog.md`).

These are small, mostly single-POV cleanups of already-built containers. Each is a tiny arc (0–2 mints + a few edges) — run them dip-gated in small batches, fresh-verify the causal edges, don't mass-mint. **Pick the highest-value remainder that a quick dip shows actually has demand; skip any that a dip shows is pure-sequence or wiki-only deep-lore.**

## The remainder backlog (pick + scope at session start)
1. **AEGON Euron/Victarion downstream wire** — the Iron Fleet's dragon-quest voyage to fetch Daenerys (the `euron-commissions-victarion-to-fetch-daenerys` bridge node exists, S116). Single-POV (Victarion ADWD), low cross-POV reach. Check whether Victarion's voyage beats have nodes; likely 1–2 mints + ENABLES wire. Also the parked E6 (Euron→Victarion) note from the Essos decomp.
2. **NORTH N6 — Stannis marches south** (the march from the Wall toward Winterfell, the "Battle of Ice" approach). Lower-value (TWOW-adjacent, partly unwritten). Verify what's in-saga (ADWD) vs unwritten before minting; the `battle-of-winterfell` node is the TWOW Battle of Ice (decoy — keep OUT). Also the optional Theon/Jeyne escape from Winterfell (ADWD).
3. **Bran greenseer-enrichment / Rickon-Skagos deferral** — Bran's deeper cave-visions are TWOW (out of scope, gated). Rickon's Skagos thread is unwritten (defer). The in-scope piece is light enrichment of the built BR-beats (the 4 still-open `bran-dip` harvest rows: Old Nan Long-Night foreshadowing agot-bran-04:41, weirwood-paste food node adwd-bran-03:149, cave floor-bones place adwd-bran-02:183, becoming-a-weirwood foreshadowing adwd-bran-03:119) + the research subagents' batchA/batchB harvest rows.

## After the remainders: enrichment dips
Once the remainders are cleared, the next direction is **enrichment dips** — the arc-enrichment 2nd-pass track (memory `project_arc_enrichment_track`, backlog `working/arc-enrichment-backlog.md`): second-pass deepening of a built spine (side-arcs / revelation-events / descriptive-depth) via fan-out lenses + verify-lines + fresh-verify. Cadence = spine-first-then-circle-back. The `SUSPECTED_OF` edge type (unproven actor→event) is available. This is the standing next-direction, not a one-shot.

## The machine (per arc — unchanged)
research dip (dedup via `event_alias_resolver.py --lookup`, eyeball ≥0.6, before minting; line-checked quotes; edge proposal VERIFIED vs `edges.jsonl` not node prose) → orchestrator mints via a `scripts/mint_*.py` script (backup + re-run guard; exact-source-substring quotes to avoid curly-quote citation mismatches) → node aliases as natural SPACED phrases → `weirwood refresh` (node ADD requires it) → **independent fresh-subagent verify** (causal `verified_by: pending-*` until CONFIRM; verifier adjudicates CAUSES/TRIGGERS/ENABLES/MOTIVATES + agency-collapse) → `--causal-chain`/`--full-chain` smoke → `verify-edge-quotes` (0 drift required) → flip verified_by to confirmed.

## Vocabulary (PASTE into every naming/sequencing subagent — they do NOT load CLAUDE.md)
Edge types = locked set: CAUSES / TRIGGERS / ENABLES / MOTIVATES / CONSPIRES_WITH / SUSPECTED_OF (+ roles AGENT_IN / VICTIM_IN / COMMANDS_IN / WITNESS_IN / GUARDS / WIELDED_IN). "Pass" = corpus sweep · "Track" = named workstream · lowercase "step" = ordered piece · "Tier" = confidence 1–5 ONLY. No new capitalized terms.

## Open question for Matt (at session start)
Which remainder to build first (AEGON Euron/Victarion vs NORTH N6 vs Bran enrichment), or skip straight to enrichment dips? Default if unspecified: do a quick demand-dip across the three, build the one that fumbles a plausible arc-question, defer the rest.

## DO NOT
Refetch wiki / any HTTP call · mint CAUSES between sibling/sequence beats (granularity overclaim) · pull TWOW-unwritten or gated-theory material into the causal map (Bran's deeper visions, the Battle of Ice, Rickon's Skagos) · mass-mint · `/endsession` without explicit permission.
