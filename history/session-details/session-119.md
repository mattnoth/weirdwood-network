---
session: 119
date: 2026-06-21
title: ESSOS container — decomposition dip + first 3 junctures (E4 + E1 + E2)
model: Opus 4.8 orchestrator + Sonnet 4.6 general-purpose subagents (1 decomposition-research, 2 fresh edge-verify, 1 E2 research+verify)
track: causal-arc / ESSOS container (major-arc backlog #2)
---

# Session 119 — ESSOS container: decomposition + AGOT root + Slaver's Bay

## Purpose

Open the **ESSOS container** (major-arc backlog #2). Per the handoff, ESSOS is too large for one
arc, so it earns its own **decomposition research dip** (the WO5K template) FIRST, then its ranked
junctures get built one at a time via the proven arc-mint machine. Matt steered mid-session toward
building (noting the conspicuous absence of a Drogo's-death node), so the session went past the
decomposition into three built junctures.

## What happened

### step 1 — the ESSOS decomposition dip (`working/essos-decomposition.md`)

A Sonnet research subagent (read-only, local cache) mirrored `working/wo5k-decomposition.md`: a
trigger-tree, an 8-juncture scorecard (the WO5K 6-axis rubric), sequence-only traps, a ranked build
order, a cross-book attach-point map, and a nodes-to-mint table. I **independently verified its
headline claim against `edges.jsonl`** (the machine's "verify vs edge data, not stale node prose"
rule): **the entire Daenerys thread, AGOT→ADWD, was 100% causally dark** — zero CAUSES/TRIGGERS/
MOTIVATES edges on any Dany-thread node, despite many nodes existing (Plate-3/wiki promotion gave
them role + PART_OF edges only).

The 8 junctures: **E1** dragon-birth · **E2** Astapor→Meereen→Sons-of-the-Harpy · **E3** Meereen
stalemate→Daznak→Dothraki sea · **E4** Robert's order→Drogo's vow (bridge) · **E5** Doran-pact→
Quentyn (bridge) · **E6** Euron→Victarion downstream · **E7** Illyrio/Varys dyad · **E8** Jorah
informant. E7/E8 are dyad-shaped, not causal arcs (model as CONSPIRES_WITH / INFORMS / SPIES_ON, not
event arcs). E2 is the only 0-mint juncture.

### step 2a — E4 + E1 (the AGOT Essos root), built as one contiguous chain

E4 (Robert's order) and E1 (dragon birth) are causally contiguous (E4's terminus `drogo-westward-vow`
roots E1), so I built them together — precedent S106/S107 = two arcs per session. **5 new beat-nodes**
(`robert-orders-daenerys-assassination`, `drogo-westward-vow`, `drogo-blood-magic-ritual`,
**`death-of-khal-drogo`**, `dragon-hatching-on-drogo-pyre`) + **2 bare Plate-3 nodes repaired**
(`the-wine-merchant-attempts-to-poison-dany`, `ned-orders-daenerys-s-assassination-cancelled` —
spaced aliases + `occurred` + clean bodies + `## Quotes`). 18 edges minted, then the FIRM fresh-verify
gate ran.

**Fresh-verify verdicts (the gate earned its keep):**
- **REJECT** `robert-orders-daenerys-assassination CAUSES ned-orders-daenerys-s-assassination-cancelled`.
  The order is the *object* being cancelled, not the cause; the cancellation's real cause is Robert's
  deathbed change of heart (unmodeled). I flagged this as the weakest link at mint time; dropped it.
  → 18 edges became 17.
- **ADJUST** `drogo-westward-vow CAUSES drogo-blood-magic-ritual` → **ENABLES**. The wound came from a
  contingent battle with Khal Ogo (agot-daenerys-07), not mechanically from the vow; the vow sets the
  conditions (the westward march / Lhazar raid) but doesn't cause the ritual. This is the **E4↔E1
  hinge** — and because `--causal-chain` walks only CAUSES/MOTIVATES/TRIGGERS (not ENABLES), the two
  arcs read as separate causal segments, which is the honest outcome.
- **ADJUST** `death-of-khal-drogo TRIGGERS dragon-hatching-on-drogo-pyre` → **CAUSES**. Too many
  deliberate steps (pyre-building, egg-placement, Dany walking into the fire) for an immediate spark.

I corrected the script (drop + 2 retypes + stamp survivors verified), restored the backup, re-ran, and
fixed the node `## Edges` prose to match. **Root-check (5b):** E4's `robert-orders-daenerys-assassination`
is a declared standalone root (Robert acts on learning of the pregnancy — unmodeled), like Balon's
death in S116; E1 roots at the vow via the ENABLES hinge (intentional, documented, not an oversight).

### step 2b — E2 (Slaver's Bay), 0 mints, fresh-verified BEFORE minting

For E2 I ran the research+verify as a single read-only pass *before* minting (no mint-then-restore
churn). It reshaped the decomposition's naive "3 CAUSES" sketch substantially:
- `fall-of-astapor → siege-of-meereen` is **ENABLES, not CAUSES**, and routed **through Yunkai**
  (army-enablement + campaign sequence; Yunkai is a real waypoint). Canonical Yunkai node is
  `battle-near-yunkai` — `battle-of-yunkai` is a redirect stub.
- It surfaced **two strong edges the sketch missed**: `siege-of-meereen MOTIVATES daenerys` (the
  stay-and-rule pivot — "the most important missing edge"; without it nothing explains the occupation)
  and `sons-of-the-harpy-kill-twenty-nine TRIGGERS wedding-of-hizdahr`.
- Final spine (6 edges, all verified-at-mint): `fall-of-astapor ENABLES battle-near-yunkai ENABLES
  siege-of-meereen`; `siege-of-meereen MOTIVATES daenerys` + `CAUSES sons-of-the-harpy-kill-twenty-nine`;
  `sons-of-the-harpy-kill-twenty-nine MOTIVATES daenerys` + `TRIGGERS wedding-of-hizdahr`.

E2 is a standalone military root at `fall-of-astapor` (no causal join from E1 — the "dragons exist →
she sails to Slaver's Bay" gap is deliberately not over-rooted, per the LOCAL-root discipline S117).

## Decisions & judgment calls

- **Built 3 junctures in one session** (vs the handoff's "one at a time") because Matt steered toward
  Drogo's death and E4/E1 are contiguous + E2 is 0-mint. Each still passed the FIRM fresh-verify gate.
- **Verifier had line-number drift** on 2 E2 quotes (a Sonnet habit) — I re-pinned every `evidence_ref`
  against the actual chapter files before minting. (The numbers turned out correct — they were long
  paragraph-lines; the single-line preview just showed the paragraph's opening words.)
- **Did NOT mint a `sons-of-the-harpy-insurgency` condition node.** The verifier's biggest concern: the
  single `sons-of-the-harpy-kill-twenty-nine` incident node is overloaded — it's both the occupation's
  consequence AND the marriage's driver. The cleaner model is a condition node with the killing as a
  TRIGGERS sub-beat. That's a graph-architecture call worth its own consideration, not a mid-build
  decision — flagged for follow-up.

## Counts

nodes 8,562 → 8,567 (+5, all E1/E4) · edges 22,342 → 22,365 (+23: E4+E1 17, E2 6) · 0 new orphans
(62 unchanged) · edge types 132 (no new — locked-vocab only) · indexes + alias-resolver rebuilt.

## Flagged follow-ups

1. Mint `sons-of-the-harpy-insurgency` (condition node) + demote the twenty-nine-killing to a TRIGGERS
   sub-beat (→ todos / a future dip; architecture call).
2. `battle-of-yunkai` redirect-stub dup of `battle-near-yunkai` (small-fixes).
3. Harvest queue over the trigger (~30 open) — decomp+verify+E2 subagents pushed rows; a harvest-consume
   pass is due. Several rows are Essos quotes for E3/E5 nodes not yet built (parked-by-arc).

## Next

E3 (Daznak's Pit → Drogon flees → Dany lost on the Dothraki sea, ~3 mints, ADWD terminus — roots at
E2's `wedding-of-hizdahr-zo-loraq` via the pit-reopening) → then E5 (Doran-pact → Quentyn, closes the
S117 Dorne arc cross-book; unblocks parked harvest rows 204/209/210). Bridges E6/E7/E8 + parked rows
149–152 (now unblockable by E4). Continue prompt: `progress/continue-prompts/2026-06-21-essos-container-decomposition.md`.
