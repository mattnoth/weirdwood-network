# SESSION 137 — Enrichment dip #4: Ned's Downfall (board already chose)
> **This is Session 137.** Stamp your worklog entry `### Session 137` at endsession (in `worklog.md` — graph track).
> **Recommended model:** Sonnet 4.6 fan-out/verify subagents + Opus 4.8 orchestrator (same machine as S133/S134/S135).
> **D&E Pass-1 is PARKED** (Matt, 2026-06-23). You are NOT running two tracks. Still: stage only your own files by explicit path; never `git add -A`.

## Where we are
The **enrichment phase is the primary track**, descending: major arcs → sub-plots → characters (one dip/session, Matt S131).
**Three** major-arc dips shipped: **Robert's Rebellion (S133)**, **Red Wedding (S134)**, **Purple Wedding (S135)**.
**S136 was a clarification + board session (no graph writes).** Read the new top section of the ledger before you start —
`working/arc-enrichment-backlog.md` § **"The scope model — why we enrich EVENTS, not 'containers'"** — it's the read-first
framing (we enrich event-arcs because there's no container-scale node to grab; the 3 descent levels; lens 4 does the
cross-container wiring node-by-node).

## STEP 1 — ALREADY DONE (skip the board)
The S136 3-advisor board ran **UNANIMOUS → the target is `execution-of-eddard-stark` (Ned's Downfall).** Do NOT re-run a board.
- Why it won (all 3 advisors): the conspiracy actors + sub-events are *already minted nodes* but the causal links between them
  are simply **absent** — highest yield-per-edge dip, near-zero theory risk. `littlefinger-betrays-ned` has only 2 edges total
  and **no forward CAUSES**. `ned-discovers-the-truth-of-joffrey-s-parentage` has no CAUSES to the arrest. Varys (visits the black
  cells) has 0 edges into the execution. Renly's throne-room offer has no event node. The Janos-Slynt / gold-cloak bribery chain
  is minted but causally unlinked. The throne-room massacre of Stark household guard is unwired.
- Sack-of-KL was REJECTED as a **double-dip** (its core — Jaime's kingslaying, the wildfire plot, the Elia/Aegon murders — was
  wired in the S133 RR pass; ~39 edges already reference its sub-events). Blackwater was the clean #2 (a future dip).
- Board writeups: `working/enrichment/s136-board/advisor-{A,B,C}.md`.

**Current Ned's-downfall causal chain (S136):** 3 upstream + 2 downstream = 5 edges; hub has 2 role edges + 1 beat. The arrest→
execution spine exists; the **betrayal/conspiracy substrate is the gap.** Dump the cluster yourself with
`graph-query.py --neighbors execution-of-eddard-stark` / `--causal-chain` / `--event-participants` + the surrounding nodes
(`arrest-of-eddard-stark`, `littlefinger-betrays-ned`, `ned-discovers-the-truth-of-joffrey-s-parentage`,
`ned-confesses-to-treason`, plus search for gold-cloak / Slynt / Renly-offer / Varys-black-cells nodes) to build `baseline.md`.

## STEP 2 — run the S133/S134/S135-proven machine
Shared dedup `baseline.md` (`--neighbors / --event-participants / --causal-chain` to dump the cluster + flag causal-island
nodes for lens 4) → fan out **4 fresh Sonnet lenses** PROPOSE-only (paste the locked vocab + the harvest snippet + the
**line-check rule**: every quote must be a VERBATIM CONTIGUOUS span, INCLUDING any internal dialogue quote marks — S135 lost 4
quotes to stripped `"`s). The 4 lenses: (1) downstream-causal/consequence · (2) secondary-character sub-arcs +
SUSPECTED_OF/WITNESS substrate · (3) descriptive/quote/object depth · (4) **existing-node↔existing-node causal-wiring** (the
cross-arc seam lens — ALWAYS include it; it's standing policy per S134). →
**SPLIT THE BAR (paste into every lens prompt):** the edge bar is TIGHT (high-confidence, fresh-verifiable) but the **harvest
bar is LOW and WIDE-OPEN** — capture EVERY food/meal (gruel + prison rations count, not just feast-grade), every physical/
clothing description, every notable quote, every foreshadowing beat; **pre-dedup is NOT your job**, over-capture is the goal.
Matt wants A LOT of harvest rows. →
Opus synthesizes + **line-checks every quote against the files** (watch for mis-targeted nodes — e.g. don't conflate
`ned-discovers-the-truth-of-joffrey-s-parentage` with the *arrest* trigger; keep beats distinct) → mint via
`scripts/mint_neds_downfall_enrichment_s137.py` (`mint_arc_lib.precheck_slugs`, backup to `_regrounding/`, re-run guard; copy
`scripts/mint_purple_wedding_enrichment_s135.py` as the template) → `python3 scripts/verify-edge-quotes.py --run-id <id>`
(fix non-contiguous spans → 0 drift) → `bash scripts/weirwood-refresh.sh` →
**independent fresh-verify** (a fresh Sonnet that did NOT propose; adversarial — down-tier/REJECT inference, agency-collapse
[don't promote constitutive beats of the arrest/execution to *causes* of it — S120 policy], **temporal inversions**,
incidental-co-location ENABLES; apply verdicts) → `--causal-chain`/`--full-chain execution-of-eddard-stark` smoke test →
consume easy harvest refills → increment the ledger pass count (add a `Ned's downfall | arc/cluster | 1` row) + add a
Session-137 worklog entry.

## Watch-outs specific to Ned's Downfall
- **WO5K dead-end:** the execution already CAUSES `robb-proclaimed-king-in-the-north` + MOTIVATES robb — a lens-4 opportunity is
  wiring the *betrayal* substrate forward into Joffrey's reign / the WO5K, not re-drawing the arrest→execution spine.
- **Agency:** Littlefinger's betrayal is largely *constitutive* of the arrest (S120 counter-example) — `SUB_BEAT_OF` + role edges,
  be cautious about a CAUSES. Use `SUSPECTED_OF` / `MANIPULATES` / `DECEIVES` for the hidden-architect material (Varys, LF).
- **Theory:** Joffrey's-parentage is on-page fact (Ned proves it) — fair Tier-1/2 substrate. Keep R+L-adjacent reads OUT.

## Harvest queue state
**54 open rows** (per the S136 ledger) / 16 parked / 254 done. **Matt loves food/meal descriptions — capture ALL of them, even
mundane/bad meals (gruel etc.).** Consume the open rows if the dip is adjacent (Ned/black-cells/KL-court rows are), else leave
for a harvest pass.

## DO NOT
Refetch wiki / any HTTP · mass-mint · CAUSES between sibling/sequence beats or constitutive beats (agency-collapse) · re-run the
4th-arc board (it's done — target is Ned's-downfall) · launch the PARKED graph-wide causal-wiring track · pull TWOW-unwritten or
gated-theory READINGS into the causal map (Tier-1/2 substrate only) · run extractions without asking · `/endsession` without
explicit permission · un-park D&E without Matt saying so · `git add -A`.

## Open question for Matt (carry-over, low priority)
The 58-mismatch whole-graph quote-regrounding cleanup (pre-existing May-2026 bulk runs) — queue as its own session sometime?
Also a tiny one surfaced S136: a stray `containers: [jon]` tag on 4 nodes (North-build leak) — fold into a Small-Fixes pass.
