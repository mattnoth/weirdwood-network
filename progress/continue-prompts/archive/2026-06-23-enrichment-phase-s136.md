# SESSION 136 — Enrichment phase: fourth major-arc dip
> **This is Session 136.** Stamp your worklog entry `### Session 136` at endsession (in `worklog.md` — graph track).
> **Recommended model:** Sonnet 4.6 fan-out/verify subagents + Opus 4.8 orchestrator (same machine as S133/S134/S135).
> **D&E Pass-1 is PARKED** (Matt, 2026-06-23 — concurrency was too confusing). You are NOT running two tracks; this is the only live track. Still: stage only your own files by explicit path; never `git add -A`.

## Where we are
The **enrichment phase is the primary track**, descending: major arcs → sub-plots → characters (one dip/session, Matt S131).
**Three** major-arc dips shipped: **Robert's Rebellion (S133)**, **Red Wedding (S134)**, **Purple Wedding (S135)**. Ledger:
`working/arc-enrichment-backlog.md` (pass-COUNT per unit). Machine + rules: memory `project_arc_enrichment_track`.

**STANDING POLICY (DECIDED S134 — in worklog Active Decisions):**
- The enrichment-dip board is **4 lenses**: (1) downstream-causal/consequence · (2) secondary-character sub-arcs +
  SUSPECTED_OF/WITNESS substrate · (3) descriptive/quote/object depth · (4) **existing-node↔existing-node causal-wiring**
  (the cross-arc seam lens). **Always include lens 4.**
- A graph-wide causal-wiring TRACK is **PARKED** (do NOT launch it this phase). Don't confuse the per-dip lens 4 (use it)
  with the parked graph-wide track (don't run it).

## STEP 1 — pick the fourth arc (descent level 1)
Let a quick **3-advisor board** pick (Matt's S133 preference — don't just choose; it worked cleanly for S135). The S135
board's own guidance on the remaining candidates:
- **READY now** (spine built, low theory risk): **Sack of King's Landing** (tight; bridges RR↔AEGON↔Cersei; atrocity/
  SUSPECTED_OF nodes exist — Tywin's calculated timing, the wildfire-cache discovery), **Ned's downfall** (series-defining,
  thinnest causal wiring of any AGOT event per advisor A; `littlefinger-betrays-ned` minted but role-thin; closes the WO5K
  dead-end), **Blackwater** (clean, battle-centric, 0 theory entanglement; Sandor-desertion + Sansa thread; advisor C's #1
  for tractability).
- **BUILD-FIRST, don't enrich yet** (advisor C flagged the spines as partly un-built): **Tywin's-death** (`death-of-tywin`
  hub orphaned), **Cersei's-downfall** (walk-of-shame / arrest nodes may not exist). Run a spine-build session before an
  enrichment dip on these.
- **GATE CAREFULLY:** Essos/Daenerys (theory-trap — Azor Ahai / prophecy reads stay GATED; raw spine is clean but the
  secondary threads brush theory immediately).

## STEP 2 — run the S133/S134/S135-proven machine
Shared dedup `baseline.md` (`graph-query.py --neighbors / --event-participants / --causal-chain` to dump the cluster +
flag causal-island nodes for lens 4) → fan out **4 fresh Sonnet lenses** PROPOSE-only (paste the locked vocab + the harvest
snippet + the **line-check rule**: every quote must be a VERBATIM CONTIGUOUS span, INCLUDING any internal dialogue quote
marks — S135 lost 4 quotes to stripped `"`s) →
**SPLIT THE BAR (board-decided S135 — paste this into every lens prompt):** the edge bar is TIGHT (high-confidence,
fresh-verifiable) but the **harvest bar is LOW and WIDE-OPEN** — capture EVERY food/meal (gruel and grim prison rations
count, not just feast-grade), every physical/clothing description, every notable quote, every foreshadowing beat; **pre-dedup
is NOT your job**, over-capture is the goal. Drop it even if unsure it belongs. (Matt wants A LOT of harvest rows.) →
Opus synthesizes + **line-checks every quote against the files** (watch for
mis-targeted nodes: S135's lenses conflated two different "Tyrell plots") → mint via `scripts/mint_<arc>_enrichment_s136.py`
(`mint_arc_lib.precheck_slugs`, backup to `_regrounding/`, re-run guard; copy the S135 script as the template) →
`verify-edge-quotes.py --run-id <id>` (fix non-contiguous spans → 0 drift) → `bash scripts/weirwood-refresh.sh` →
**independent fresh-verify** (a fresh Sonnet that did NOT propose; adversarial — down-tier/REJECT inference, agency-collapse,
**temporal inversions** [S135 caught a kill cited as enabling an already-complete escape], incidental-co-location ENABLES;
apply verdicts) → `--causal-chain`/`--full-chain` smoke test → consume easy harvest refills → increment the ledger pass
count + add a Session-136 worklog entry.

## Carry-over pass-2 seams surfaced in S135 (NOT the default — only if relevant / a future Purple-Wedding or Dorne dip)
- **Dornish-succession seam (Matt-flagged S135):** `the-queenmaker-plot` has 0 causal-in (modeled as a prime-mover). The
  real motive traces `gregor-confesses-and-kills-oberyn → arrest-of-the-sand-snakes → MOTIVATES arianne-martell → [AGENT_IN]
  queenmaker-plot`. A clean pass-2 edge would be `arrest-of-the-sand-snakes MOTIVATES the-queenmaker-plot` (makes the chain
  walk Oberyn's-death → the plot end-to-end). Verify cite before minting.
- **Purple Wedding pass-2 candidates:** the deferred `silver-hairnet-of-sansa-stark` artifact node + `sansa-assumes-alayne-
  stone-identity` Vale node; the Kettleblack triple-agent web (Oswell-as-oarsman reveal); feast `object.food` nodes.

## Harvest queue state
**54 open rows** (14 added S135 — Purple Wedding feast food, the death-throes quote, the Olenna palm moment, Kettleblack
oarsman, Pycelle naming the poison) / 16 parked / 254 done. **Matt loves food/meal descriptions — capture ALL of them,
even mundane/bad meals (gruel etc.), not just feast-grade.** Consume the open rows if the dip is adjacent, else leave for a
harvest pass.

## DO NOT
Refetch wiki / any HTTP · mass-mint · CAUSES between sibling/sequence beats (agency-collapse) · launch the parked graph-wide
causal-wiring track · pull TWOW-unwritten or gated-theory READINGS into the causal map (Tier-1/2 substrate only) · enrich an
un-built spine (build Tywin's-death / Cersei's-downfall first) · run extractions without asking · `/endsession` without
explicit permission · un-park D&E without Matt saying so · `git add -A`.

## Open question for Matt (carry-over, low priority)
The 58-mismatch whole-graph quote-regrounding cleanup (pre-existing May-2026 bulk runs) — queue as its own session sometime?
