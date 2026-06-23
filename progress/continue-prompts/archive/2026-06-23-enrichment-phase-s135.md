# SESSION 135 — Enrichment phase: third major-arc dip
> **This is Session 135.** Stamp your worklog entry `### Session 135` at endsession (in `worklog.md` — graph track).
> **Recommended model:** Sonnet 4.6 fan-out/verify subagents + Opus 4.8 orchestrator (same machine as S133/S134).
> **Parallel-safe** with the D&E Pass-1 track (`2026-06-29-dunk-egg-pass1-smoke.md`, separate window, no shared files — stage only your own files by explicit path; never `git add -A`).

## Where we are
The **enrichment phase is the primary track**, descending: major arcs → sub-plots → characters (one dip/session, Matt S131).
Two major-arc dips shipped: **Robert's Rebellion pass 1 (S133)** and **Red Wedding pass 1 (S134)**. Ledger:
`working/arc-enrichment-backlog.md` (pass-COUNT per unit). Machine + rules: memory `project_arc_enrichment_track`.

**STANDING POLICY now in effect (DECIDED S134 — already in worklog Active Decisions):**
- The enrichment-dip board is **4 lenses**: (1) downstream-causal/consequence · (2) secondary-character sub-arcs +
  SUSPECTED_OF/WITNESS substrate · (3) descriptive/quote/object depth · (4) **existing-node↔existing-node causal-wiring**
  (the cross-arc seam lens — it earned its keep in S134, producing both Red Wedding island-fixes). **Always include lens 4.**
- A graph-wide causal-wiring TRACK is **PARKED** (do NOT launch it this phase — it waits for a settled graph; guardrails in
  Active Decisions). Don't confuse the standing per-dip lens (use it) with the parked graph-wide track (don't run it).

## STEP 1 — pick the third arc (descent level 1)
Let a quick **demand-dip or a fresh 3-advisor board** pick (Matt's S133 preference — don't just choose). Candidates at pass 0:
**Essos/Daenerys spine** (heavyweight; Advisor-C flagged theory-trap — gate carefully; also unblocks 4 PARKED Essos harvest
rows 156–159), **Sack of King's Landing** (tight; bridges RR↔AEGON↔Cersei; atrocity/SUSPECTED_OF nodes exist to wire),
**WO5K container** (needs many passes — Karstark/Frey/Bolton/Riverlands/westerlands), **Purple Wedding** (whodunit/poisoner
SUSPECTED_OF layer), **Tywin's death**, **Blackwater**, **Ned's downfall**, **Cersei's downfall**, **Brienne→Stoneheart**.

## STEP 2 — run the S133/S134-proven machine
Shared dedup `baseline.md` (use `graph-query.py --neighbors / --event-participants / --causal-chain` to dump the cluster +
flag causal-island nodes for lens 4) → fan out the **4 fresh Sonnet lenses** PROPOSE-only (paste vocab + the harvest snippet
+ the line-check rule) → Opus synthesizes + **line-checks every quote against the files** → mint via
`scripts/mint_<arc>_enrichment.py` (`mint_arc_lib.precheck_slugs`, backup to `_regrounding/`, re-run guard) →
`verify-edge-quotes.py --run-id <id>` (fix any non-contiguous quote spans → 0 drift) → `bash scripts/weirwood-refresh.sh` →
**independent fresh-verify** (a fresh agent that did NOT propose; adversarial — down-tier/REJECT inference & agency-collapse;
apply verdicts to edges.jsonl) → `--causal-chain`/`--full-chain` smoke test → consume the easy harvest refills → increment the
ledger pass count + add a Session-135 worklog entry.

## Harvest queue state (for the harvest on-ramp, optional)
**17 open RW rows** (S134 RW-lens refills — descriptive/food/edge candidates) + 4 PARKED Essos rows (156–159, unblock when the
Essos arc is built). Consume the open RW rows if the dip is Red-Wedding-adjacent, else leave for a future harvest pass.

## Red Wedding PASS-2 candidates (deferred S134 — only if you revisit RW, NOT the default)
Frey-pies/GNC revenge layer; the Riverrun-siege downstream cluster; the bedding sub-beats; the Manderly-Wylis-hostage thread;
a post-RW Arya kill-list node (the `robb-killed MOTIVATES kill-list` edge needs a NEW post-RW node — lens-4 flagged it).

## DO NOT
Refetch wiki / any HTTP · mass-mint · CAUSES between sibling/sequence beats (agency-collapse) · launch the parked graph-wide
causal-wiring track · pull TWOW-unwritten or gated-theory READINGS into the causal map (build Tier-1/2 substrate only) · run
extractions without asking · `/endsession` without explicit permission · `git add -A` (parallel D&E track — stage by path).

## Open question for Matt (carry-over, low priority)
The 58-mismatch whole-graph quote-regrounding cleanup (pre-existing May-2026 bulk runs) — queue as its own session sometime?
