# SESSION 134 — Enrichment phase: resolve 2 open decisions → second major-arc dip

> **This is Session 134.** Stamp your worklog entry `### Session 134` at endsession (in `worklog.md` — this is a graph track).
> **Recommended model:** Sonnet 4.6 fan-out/verify subagents + Opus 4.8 orchestrator (same machine as S133).
> **Parallel-safe** with the D&E Pass-1 track (`2026-06-29-dunk-egg-pass1-smoke.md`, separate window, no shared files).

## Where we are
The **enrichment phase is open** (S133). First major-arc dip = **Robert's Rebellion, pass 1 SHIPPED** (+3 nodes / +24 edges;
RR→AEGON, RR→WO5K, RR→Essos bridges now traverse; Jon-Arryn-murder reified; R+L held gated). Ledger:
`working/arc-enrichment-backlog.md` (RR now = pass 1). Machine + sequencing rules: same file + memory
`project_arc_enrichment_track`. Matt's cadence: **one enrichment dip per session**; descent = major arcs → sub-plots →
characters; broad roster, no lead.

## STEP 0 (this session) — RESOLVE 2 OPEN DECISIONS from S133 first (Matt input needed)
Matt fired /endsession before answering these two AskUserQuestion prompts — ask them again at session start:
1. **Causal-wiring scope.** The S133 A/B showed the topic-lens enrichment board systematically MISSES causal edges between
   *already-built* nodes (the two it missed were cross-arc: `roberts-rebellion MOTIVATES robert-orders-daenerys-assassination`,
   `wildfire-plot MOTIVATES slaying-of-aerys`). Options: **(a)** add an in-dip "existing-node↔existing-node causal-wiring"
   4th lens; **(b)** stand up a dedicated graph-wide causal-wiring TRACK (its own pass — the analogue of the S97/S100
   historical-anchor *participant* backfill, but for *causal* edges; cross-arc edges only this reliably catches); **(c)** both;
   **(d)** just note it. Memory: `feedback_enrichment_board_causal_lens`. **Regardless of his answer, ADD the 4th lens to this
   session's board** (it's cheap and the finding is banked).
2. **The off-vocab `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` edge** (rhaegar→lyanna, the Harrenhal crowning, agot-eddard-15:45).
   Provenance = auto-generated Stage-4 tail-LLM (`run_id tail-llm-20260523`), NOT a decision; pre-lockdown off-vocab leakage.
   Options: convert to a `crowning-of-lyanna-at-harrenhal` beat-node (honoree role = NEEDS_VOCAB) / leave tolerated+flagged /
   add a locked ceremonial-honor type via Active Decision. (Harrenhal/KotLT *nodes* were discussed S28/S29 — KotLT stays
   separate from Lyanna, identity gated — but the CROWNS *edge* was never decided.)

## STEP 1 — harvest-consume on-ramp
`working/harvest-queue.md` has **19 open rows** (all S133 RR-dip refills: lens1×5, lens2×9, lens3×5 — descriptive/quote/
foreshadowing depth on RR-cluster + neighboring nodes). Consume them first (attach to existing nodes; verify each cite;
some may be RR-pass-2 attachments). Then dip.

## STEP 2 — second major-arc enrichment
Pick ONE major arc (descent level 1). Candidates at pass 0: **Red Wedding** (densest hub, 12 beats — but more self-contained),
**Essos/Daenerys spine** (heavyweight, but Advisor C flagged it as theory-trap — handle gating carefully), **WO5K** (needs many
passes), **Sack of KL**, **Purple Wedding**, **Tywin's death**, **Blackwater**, **Ned's downfall**, **Cersei's-downfall**,
**Brienne→Stoneheart**, **Dorne/Queenmaker**. Let a quick demand-dip (or a fresh advisory board, Matt's S133 preference) pick.

**The machine (S133-proven):** write a shared dedup `baseline.md` → fan out fresh Sonnet lenses (causal/downstream ·
SUSPECTED_OF/WITNESS substrate · new-nodes/depth · **+ the new existing-node↔existing-node causal-wiring lens**), PROPOSE-only
→ orchestrator synthesizes + line-checks every quote → mint via `scripts/mint_<arc>_enrichment.py` (backup + re-run guard +
`mint_arc_lib.precheck_slugs`) → `verify-edge-quotes.py` (fix smart-quote flags to byte-exact spans → 0 drift) → `weirwood
refresh` → **independent fresh-verify** (a fresh agent, NOT a proposer) → apply verdicts → `--full-chain` smoke test →
consume harvest refills → increment the ledger pass count.

## RR pass-2 candidates (deferred S133 — for when RR is revisited, NOT this session)
`exile-of-viserys-and-daenerys` (RR→Essos root, defer to Essos enrichment); Tower-of-Joy interior (GATED); `murder-of-elia…
MOTIVATES landing-of-the-golden-company` (Tier-2, wants fresh-verify); Trident book-cite overlay (agot-eddard-10:171);
`lyanna LOCATED_AT tower-of-joy`; atrocity-node AGENT_IN re-targeting.

## DO NOT
Refetch wiki / any HTTP · mass-mint · CAUSES between sibling/sequence beats · pull TWOW-unwritten or gated-theory READINGS into
the causal map (R+L=J, KotLT identity, Jon-Arryn culprit-beyond-Lysa stay gated — build Tier-1/2 substrate only) · run
extractions without asking · `/endsession` without explicit permission · `git add -A` (parallel D&E track in the tree —
stage only your own files by explicit path).

## Open question for Matt (also)
Want the 58-mismatch quote-regrounding cleanup queued as its own session sometime? (Low severity, pre-existing May-2026 bulk runs.)
