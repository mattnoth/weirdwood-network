# Continue — ESSOS container: decomposition dip → build junctures (major-arc backlog #2)

> **Recommended model:** Sonnet 4.6 (orchestration + research/verify subagents). This is a BIG build — a whole
> continent-thread, too large for one arc. Treat it as a CONTAINER: it earns its own **decomposition research dip**
> first (the WO5K template), THEN you build its ranked junctures one at a time, dip-gated, via the proven arc-mint
> machine. Do NOT try to mint the whole thing in one pass.

> **State trust (CLAUDE.md rule #9):** `worklog.md` is authoritative. As of S118: nodes **8,562** · edges **22,342** ·
> live edge types **132** · vocab **169** · harvest queue **0 open / 12 parked / 112 done**. The AFFC causal-arc spine
> phase is COMPLETE (all 4 fumbles built S114–S117). S118 was a hygiene session (ATTENDS cleanup + harvest) — no arc work.

## Vocabulary to paste into subagents (they don't load CLAUDE.md)
Pass (numbered corpus sweep) · Track (named workstream) · step (lowercase ordered piece) · Tier (confidence 1–5 ONLY).
Source: `reference/glossary.md`.

---

## step 1 — the ESSOS decomposition dip (read-only research → `working/essos-decomposition.md`)

Mirror `working/wo5k-decomposition.md`. A research subagent (reading the LOCAL book + wiki cache — **never fetch**)
enumerates and **magnitude-ranks** Essos's load-bearing causal junctures + the first-class Westeros↔Essos bridges.
Output a ranked, buildable juncture list (each: the beat(s), candidate edge(s), local upstream root, dedup-check of
existing nodes, verbatim quote pointers). Do NOT mint anything in this step.

**Essos spine (Dany thread) — candidate junctures to enumerate/rank:**
- Drogo's death + Dany's failed resurrection of him (Mirri Maz Duur) → **the dragons hatch on Drogo's pyre** (the
  prime mover of the whole Essos arc).
- Slaver's Bay campaign: **fall of Astapor** (the Unsullied / "Dracarys") → **Yunkai** → **conquest/occupation of
  Meereen** → the stalemate + the Sons of the Harpy insurgency.
- Drogon's flight from the pit (Daznak's) → Dany lost on the Dothraki sea (ADWD endpoint).
- The Quentyn-to-Meereen thread (his quest → the dragons → his death) — joins the Dorne "Fire and blood" pact.

**First-class Westeros↔Essos BRIDGES (Matt: bridges are first-class, S112) — these are the high-value cross-book joins:**
- **Robert's assassination order → Daenerys.** MINT `robert-orders-daenerys-assassination` (only the Ned-cancels-it
  version exists in-graph; the order itself is unmodeled — harvest row 149, agot-eddard-08:13 "I want them dead, mother
  and child both"). Its downstream: the wine-merchant attempt → **Drogo's westward vow** (harvest row 150,
  agot-daenerys-06:179) → motivates the Dothraki-cross-the-sea thread.
- **Illyrio ↔ Varys conspiracy** (harvest row 151, agot-arya-03:89-93 "If one Hand can die, why not a second?"). An
  edge (`CONSPIRES_WITH`) anchoring the Pentoshi-magisters' long game.
- **Jorah informs for Varys/Robert** — DEMOTED to an `INFORMS`/`SPIES_ON` dyad (information channel, NOT a causal arc;
  harvest row 152, agot-daenerys-07:147).
- **Euron commissions Victarion to fetch Daenerys** — node **already minted in-place S116**
  (`euron-commissions-victarion-to-fetch-daenerys`, downstream dark). The Essos arc connects its spine here
  (cross-book auto-join — just tag the attach-point).
- **The Quentyn / Dorne "Fire and blood" pact** — Doran's onyx-dragon reveal (parked harvest row 209). The Dorne→Essos
  marriage-pact bridge; joins the Dorne arc (S117) to Quentyn's Meereen quest.

**Unblocks these PARKED harvest rows** (flip to `open` as their home nodes get built): 149 (Robert's order), 150
(Drogo's vow), 151 (Varys-Illyrio), 152 (Jorah-channel), 204 (Golden Company/fAegon), 209 (Fire-and-blood pact),
210 (Arianne↔Viserys betrothal). They're `parked (blocked: arc — Essos)` in `working/harvest-queue.md`.

## step 2 — build the top-ranked junctures, ONE at a time, dip-gated (the arc-mint machine)

The machine (proven 11× — RR/Bran/Sack/PW/B1/B2/B3/Tywin/Blackwater/J3/4×AFFC) is documented in the **archived**
`progress/continue-prompts/archive/2026-06-18-causal-arc-execution.md` — restore/reference it. Per juncture:

1. **research subagent** (dedup-check existing nodes FIRST — Essos has many wiki nodes already; verbatim quotes;
   edge proposals VERIFIED vs `edges.jsonl`, not node prose).
2. **orchestrator** trims + mints via a `scripts/mint_*_arc.py` (backup to `_regrounding/` + re-run guard).
3. **node aliases = natural SPACED phrases, not kebab** (S109 resolver lesson).
4. targeted **index + alias-resolver rebuild** (a node was added → required; `weirwood refresh` / the rebuild scripts).
5. **fresh-subagent verify** each interpretive/causal edge vs LOCAL cache (`verified_by: pending` until CONFIRM;
   verifier adjudicates CAUSES vs TRIGGERS). Run `scripts/verify-edge-quotes.py` on any edge carrying a verbatim quote.
6. `--causal-chain` **smoke test** + **root-check (machine step 5b)**: root at the **LOCAL antecedent**, not the deepest
   hairnet ancestor; declare genuinely-standalone threads explicitly (Drogo's death is a plausible standalone prime mover,
   like Balon's in S116).
7. **harvest** — paste the harvest snippet (`working/harvest-queue.md` header) into every text-reading subagent.

## Guardrails / rules (FIRM)
- **Verify before inventing edge types.** Run `scripts/build-edge-type-counts.py` and check `reference/architecture.md`;
  if a needed relation isn't in the locked vocab, reuse an existing type or file a worklog Active Decision — **never
  invent silently** (S118 lesson: `GARRISONS`/`HELD_AT` weren't in vocab → used `PARTICIPATES_IN`).
- **Unproven agency uses `SUSPECTED_OF` (Tier-2), never asserted as fact** (e.g. who poisoned whom).
- **Cross-book auto-join** is automatic via shared nodes + `--causal-chain` — no umbrella/parent hubs (chain-as-arc,
  S105/S106). Tag each juncture's local upstream attach-point.
- Verification is FIRM (Matt): causal edges checked by **fresh subagents vs LOCAL cache**; Matt gates at policy, not per-edge.

## DO NOT
Re-fetch the wiki (local cache only) · invent edge types (verify vocab first) · use kebab aliases (SPACED phrases only) ·
assert unproven agency as fact (`SUSPECTED_OF`, Tier-2) · mint the whole container in one pass (decompose first, build
junctures one at a time) · run `/endsession` without explicit permission.
