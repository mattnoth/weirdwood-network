# SESSION 128 — AEGON spine build (causal arc mint)

> **This is Session 128.** Stamp your worklog entry `### Session 128` at endsession.

> **Recommended model:** Sonnet 4.6 (Opus 4.8 orchestrator + Sonnet-class `general-purpose` subagents: 1 API-health probe → research dips → independent fresh-verify). Same arc-mint machine as the NORTH (S125/S126) and WO5K-remainder (S123) builds.
> **This WRITES to the graph** (mints nodes + edges). Local cache only — no HTTP / no wiki refetch.
> **Decomp dip is DONE (S127, read-only):** the full plan is `working/aegon-decomposition.md` (8 sections, junctures A1–A4). READ IT FIRST — it has the trigger-tree, scorecard, exact edges, attach-points, and grounding cites. This prompt is the build kickoff; the dip doc is the spec.

## Goal
Build the AEGON container's causal spine from `working/aegon-decomposition.md` §5 (Ranked Build Order). The container is currently **entirely causally DARK** (all PART_OF/role scaffolding, 0 causal edges). **Total NEW nodes to mint = 2.** Everything else is edge/role/tag wiring on existing nodes.

## BUILD-STEP 0 (housekeeping — do FIRST, before any mint)
Two edge fixes the dip flagged but deliberately did NOT make (read-only contract):
1. **Edge bug:** re-parent / drop the 2 mis-filed `PART_OF war-of-the-five-kings` rows whose source is `landing-of-the-golden-company` and `assassinations-of-pycelle-and-kevan-lannister` (the GC invasion is its own conflict, not part of WO5K). **LEAVE** the legitimate `assassination-of-tywin-lannister PART_OF war-of-the-five-kings`. Verify with `grep '"target_slug": "war-of-the-five-kings"' graph/edges/edges.jsonl | grep -iE 'golden-company|pycelle-and-kevan'`.
2. **Suspicious edge:** delete `landing-of-the-golden-company PRECEDES wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` (cross-theater Meereen artifact — almost certainly bad). Confirm it's the only landing→Meereen edge before deleting.
Back up `edges.jsonl` to `graph/edges/_regrounding/edges-pre-aegon-build-<date>.jsonl` before mutating (the machine's standard guard).

## Ranked build order (from the dip §5 — top-ranked first)
1. **A2 — Golden Company sails west → Landing (spine ignition, 11/12).** Mint `golden-company-sails-for-westeros` [event.incident, `[aegon]`; adwd-the-lost-lord-01:217]. Wire `golden-company-sails-for-westeros CAUSES landing-of-the-golden-company` + `aegon-targaryen-young-griff MOTIVATES golden-company-sails-for-westeros` (+ optional `tyrion-lannister MOTIVATES …` the goad). Do NOT mint a separate broken-Volantis-contract node (fold as prose). This single CAUSES makes the 6-node Stormlands fan reachable.
2. **A4 — Varys assassinations → KL-endgame attach (11/12, 0 mints).** `assassinations-of-pycelle-and-kevan-lannister` exists with 0 in / 0 role edges. Wire `landing-of-the-golden-company MOTIVATES assassinations-of-pycelle-and-kevan-lannister` (Varys acts to clear Aegon's path — motive cite adwd-epilogue:293) + role edges `varys AGENT_IN` / `kevan-lannister VICTIM_IN` / `pycelle VICTIM_IN`. ATTACH (don't rebuild) to the built KL endgame — verify at build whether a Kevan-regency node exists to take a CAUSES/ENABLES.
3. **A3 — Landing → Stormlands campaign → Siege of Storm's End (9/12, 0 mints).** Wire ONLY `landing-of-the-golden-company CAUSES siege-of-storms-end-300` + `jon-connington MOTIVATES siege-of-storms-end-300`. **DO NOT add CAUSES between the 6 sibling takings** — they were simultaneous; PART_OF is the correct + complete structure (granularity-overclaim trap, cf. NORTH §4). Container-retag the 6 takings + `stone-men-attack-the-shy-maid` → add `[aegon]`; `siege-of-storms-end-300` → `[aegon, wo5k]` seam.
4. **A1 — Conspiracy seed → Aegon revealed (10/12).** Mint `aegon-revealed-to-the-golden-company` [event.incident, `[aegon]`; adwd-the-lost-lord-01:127]. Build the **dyad** `varys CONSPIRES_WITH illyrio-mopatis` (symmetric, Tier-2/3, cite agot-arya-03:79/93) — **NOT a tunnel-meeting node** (D1 resolved dyad-only; Arya WITNESS_IN stays parked). Wire `<varys/illyrio character node> MOTIVATES aegon-revealed-to-the-golden-company` + `aegon-revealed-to-the-golden-company TRIGGERS golden-company-sails-for-westeros` (joins A1→A2).

## SLUG / TARGET discipline (the dip's verified fixes)
- VICTIM target is **`pycelle`** (NOT `grand-maester-pycelle` — that slug doesn't exist).
- ALL new AEGON edges target **`aegon-targaryen-young-griff`** — NOT `aegon-targaryen-son-of-rhaegar` (the historical murdered infant; ~9 Aegons exist, don't cross wires).
- A3 Storm's End attaches to **`siege-of-storms-end-300`** (the GC siege), NOT `taking-of-storms-end` (Stannis/WO5K, OUT) and NOT `siege-of-storms-end-299` (Stannis v. Renly, OUT).

## Hard rules (same machine as S123/S125/S126)
- **Arc-mint machine:** research subagent (dedup + verify quote vs LOCAL cache + propose edges; VERIFY against `edges.jsonl`, not node prose) → orchestrator mints via a `scripts/mint_aegon_*.py` script (backup + re-run guard) → node aliases as natural SPACED phrases (not kebab) → targeted index + alias rebuild → **independent fresh-verify subagent** (L2 — REQUIRED for the cross-book/contested CAUSES; causal `verified_by: pending` until CONFIRM) → `verify-edge-quotes` (must show 0 drift) → `--causal-chain` / `--full-chain` smoke test.
- **Spoiler/tier discipline:** Aegon's legitimacy is in-universe CONTESTED. Map only WHAT HAPPENS (reveal, crossing, landing, conquests, assassinations) at Tier 1–2. Route any "is Aegon real / Blackfyre / mummer's dragon" claim to the GATED theories track — NEVER a causal node or edge.
- **Seam discipline:** `siege-of-storms-end-300` + `assassinations-…` are AEGON∩WO5K/KL seams — dual-tag and ATTACH; never re-build WO5K/KL events.
- **Vocabulary (paste into every naming/sequencing subagent — they don't load CLAUDE.md):** edge types = locked set CAUSES / TRIGGERS / ENABLES / MOTIVATES / CONSPIRES_WITH (+ roles AGENT_IN / VICTIM_IN / COMMANDS_IN / WITNESS_IN / GUARDS). "Pass" = corpus sweep · "Track" = named workstream · lowercase "step" = ordered piece · "Tier" = confidence 1–5 ONLY. No new capitalized terms.
- **Harvest push (paste into research/verify subagents):** while in the text, drop `| open | <kind> | <book> | <chapter:line> | <note> | aegon-build |` rows into `working/harvest-queue.md`; POINT don't extract; line-check each cite. Note: 12 aegon-dip rows are already queued (S127) — a harvest consume-pass can attach those grounding quotes onto the new/wired nodes as you build (book-citation overlay is high-value).
- **Never run extractions or large passes without asking; never `/endsession` without explicit permission.**

## Reference
Spec: `working/aegon-decomposition.md` (S127). Template builds: `working/north-decomposition.md` + S125/S126 worklog entries. Dyad queue: `working/dyad-queue.md` (D1 now resolved; D2 Jorah still parked — optional pickup). Scorecard rubric: `working/causal-arc-strategy-2026-06-18.md`. Container map: `working/session-results/2026-06-21-container-SHAPE-map.md`.

## At session end
Update worklog (S128 entry; archive the oldest Session-Log entry per rule #8 — archive026 currently holds 1/5). Archive this prompt. Create the next live track: **Bran decomposition dip** (greenfield flight-to-the-north) OR a low-value AEGON-remainder note, per Matt's pick.
