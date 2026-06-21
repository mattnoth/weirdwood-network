# Continue — ESSOS container: build remaining junctures (E3 next, then E5) — major-arc backlog #2

> **Recommended model:** Sonnet 4.6 (orchestration + research/verify subagents). The ESSOS container is
> decomposed and its first 3 junctures are built; this prompt resumes the build of the remaining ranked
> junctures, one at a time, dip-gated, via the proven arc-mint machine. Do NOT mint the rest in one pass.

> **State trust (CLAUDE.md rule #9):** `worklog.md` is authoritative. As of **S119**: nodes **8,567** ·
> edges **22,365** · edge types **132** · vocab **169**. The ESSOS **decomposition is DONE**
> (`working/essos-decomposition.md` — 8 ranked junctures E1–E8) and **E4 + E1 + E2 are BUILT + verified**
> (the whole Daenerys spine was causally dark at S119 start; it now walks from Robert's assassination
> order → the dragon birth, and Astapor → the Hizdahr marriage).

## Vocabulary to paste into subagents (they don't load CLAUDE.md)
Pass (numbered corpus sweep) · Track (named workstream) · step (lowercase ordered piece) · Tier (confidence 1–5 ONLY).
Source: `reference/glossary.md`.

## What's already built (do NOT rebuild — dedup-check first)
- **E4** (bridge): `robert-orders-daenerys-assassination CAUSES the-wine-merchant-attempts-to-poison-dany CAUSES drogo-westward-vow`. (Standalone root; `ned-orders-daenerys-s-assassination-cancelled` deliberately has NO causal upstream — its cause is Robert's unmodeled deathbed change of heart.)
- **E1** (dragon birth): `drogo-westward-vow ENABLES drogo-blood-magic-ritual CAUSES death-of-khal-drogo CAUSES dragon-hatching-on-drogo-pyre`; `mirri-maz-duur SACRIFICES rhaego`; `the-wine-merchant-attempts-to-poison-dany MOTIVATES drogo`.
- **E2** (Slaver's Bay): `fall-of-astapor ENABLES battle-near-yunkai ENABLES siege-of-meereen`; `siege-of-meereen MOTIVATES daenerys-targaryen` + `CAUSES sons-of-the-harpy-kill-twenty-nine`; `sons-of-the-harpy-kill-twenty-nine MOTIVATES daenerys-targaryen` + `TRIGGERS wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen`.

## NEXT — E3 (Meereen stalemate → Daznak's Pit → Drogon flees → Dany lost on the Dothraki sea)

The ADWD terminus of Dany's published arc. Scored 11/12 in the decomposition. **~3 mints + 4–5 edges.**
Roots at E2's terminus `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` (the wedding's fighting-pit
reopening is the concession that brings Drogon back into the arena). Per the arc-mint machine:

**Mints (dedup-check each first via `event_alias_resolver.py --lookup` + `ls graph/nodes/events/ | grep`):**
- `drogon-returns-to-daznak-pit` (event.incident; ADWD Daenerys IX — Drogon descends on the pit, kills Barsena, the spearman attacks, chaos).
- `dany-mounts-drogon-and-flees-meereen` (event.incident; ADWD Daenerys IX; evidence pointer adwd-daenerys-09:55 "North they flew … nothing beneath them but grass").
- `dany-lost-on-dothraki-sea` (event.incident; ADWD Daenerys X — barefoot in the grass, the Dothraki sea; the published terminus).

**Existing Daznak nodes to wire (all EXIST, all causally dark) — dedup, don't re-mint:**
`hizdahr-orders-drogon-killed`, `drogon-kills-more-attackers`, `unnamed-spearman-attacks-drogon`,
`quentyn-orders-the-attack` (the last is E5's, not E3). Consider `SUB_BEAT_OF drogon-returns-to-daznak-pit`
for the existing pit-incident nodes.

**Proposed spine (the research+verify subagent must adjudicate types — esp. wedding→Daznak):**
`wedding-of-hizdahr CAUSES/ENABLES drogon-returns-to-daznak-pit TRIGGERS dany-mounts-drogon-and-flees-meereen CAUSES dany-lost-on-dothraki-sea`.
The decomposition flagged `wedding→Daznak` as mediated (the pit-reopening concession, not the wedding
itself) — let the verifier pick CAUSES vs ENABLES, as it did for E2's Astapor link.

## THEN — E5 (Doran's "Fire and blood" pact → Quentyn's quest → death of Quentyn Martell)

Closes the S117 Dorne arc cross-book into Essos. **~2 mints + 3–4 edges.** Scored 10/12.
- Mint `doran-reveals-fire-and-blood-pact` (event.incident; AFFC Princess-in-the-Tower:325 "Fire and blood" — already a parked harvest row 209) and `death-of-quentyn-martell` (event.death; ADWD Dragontamer/Barristan).
- Root at the S117-built `arianne-collapses-and-is-captured` (her imprisonment forces Doran's reveal).
- `quentyn-orders-the-attack` EXISTS (0 causal) → `TRIGGERS death-of-quentyn-martell`.
- `doran-reveals-fire-and-blood-pact` gets `doran-martell AGENT_IN` + `arianne-martell WITNESS_IN` (she load-bearingly sees the onyx-dragon reveal — text-anchor gate passes).
- **Unblocks parked harvest rows 204 (Golden Company/fAegon), 209 (Fire-and-blood pact), 210 (Arianne↔Viserys betrothal).**

## Lower-priority remainder (after E3/E5)
- **E6** (Euron→Victarion downstream): `euron-commissions-victarion-to-fetch-daenerys` (EXISTS, 1 upstream CAUSES from `taking-of-the-shields`, S116) → wire its dark downstream voyage (`slaver-galley-willing-maiden-captured` → `slavers-killed-rowers-freed`, both exist). Low salience (single POV).
- **E7** (Illyrio/Varys): a `CONSPIRES_WITH` dyad on the character nodes + `arya-stark WITNESS_IN` — NOT a causal event arc. Verify dyad-vs-event-node shape first.
- **E8** (Jorah informant): `INFORMS`/`SPIES_ON` dyad — NOT a causal arc.

## The arc-mint machine (reuse for every juncture)
1. **Research subagent** (read-only, LOCAL cache): dedup-check each candidate node (`event_alias_resolver.py --lookup` + grep `graph/nodes/events/`); gather VERBATIM `file:line` quotes; propose nodes + role/causal edges. **VERIFY claims against `edges.jsonl` / `graph-query.py --neighbors`, NOT stale node `## Edges` prose.** PASTE the harvest snippet (`working/harvest-queue.md` header) into the prompt.
2. **Orchestrator** trims + mints via a `scripts/mint_essos_<juncture>_arc.py` (model on `scripts/mint_essos_e2_slavers_bay_arc.py`; backup `edges.jsonl` → `_regrounding/` + re-run guard). Write beat-node `.md` files directly (prose + `## Quotes` + **SPACED aliases, never kebab**).
3. **Rebuild** indexes (`build-entity-indexes.py --type events --slug <s>`) + `event_alias_resolver.py --build` (a node was added → required).
4. **Fresh-subagent verify** each causal/agency edge vs LOCAL cache (adjudicate CAUSES/TRIGGERS/ENABLES/MOTIVATES; `verified_by: pending` until CONFIRM, then stamp `subagent-local-source-check-<date>`). For a small wire (like E2) you can run research+verify as ONE pass before minting. **Re-pin every `evidence_ref` line against the actual chapter file — Sonnet drifts line numbers.**
5. **Smoke-test** `graph-query.py --causal-chain <terminus>` + natural-phrase discoverability; **root-check (5b)**: root at the LOCAL antecedent or declare standalone in the worklog with a reason (NOTE: `--causal-chain` does NOT walk ENABLES, so an ENABLES hinge reads as a segment break — that's correct, not a bug).
6. **Harvest sweep** — paste the harvest snippet into every text-reading subagent.

## Guardrails (FIRM)
- **Verify before inventing edge types** (`scripts/build-edge-type-counts.py` + `reference/architecture.md`); reuse existing or file a worklog Active Decision — never invent silently. E4/E1/E2 used only locked-vocab types.
- **Unproven agency → `SUSPECTED_OF` (Tier-2), never asserted as fact.** Causal edges cap Tier-2; role edges Tier-1.
- **Verification is FIRM (Matt):** causal edges checked by fresh subagents vs LOCAL cache; Matt gates at policy, not per-edge.

## Flagged refinements (NOT blocking — → todos)
- Mint a `sons-of-the-harpy-insurgency` **condition** node + demote `sons-of-the-harpy-kill-twenty-nine` to a `TRIGGERS` sub-beat of it (the incident node is currently overloaded as both occupation-consequence and marriage-driver — E2 verifier's biggest concern).
- `battle-of-yunkai` is a redirect-stub dup of `battle-near-yunkai` (small-fixes).

## Harvest pass DUE
Queue is over the trigger (~30 open — the S119 decomp+verify+E2 subagents pushed rows). Several are Essos
quotes for E3/E5 nodes not yet built (parked-by-arc — they home when those nodes are minted). Run a
harvest-consume pass before or alongside E3.

## DO NOT
Re-fetch the wiki (local cache only) · invent edge types (verify vocab first) · use kebab aliases (SPACED
phrases only) · assert unproven agency as fact (`SUSPECTED_OF`, Tier-2) · mint the whole container in one
pass (one juncture at a time, dip-gated) · run `/endsession` without explicit permission.
