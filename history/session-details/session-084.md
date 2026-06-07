# Session 84 — Edge-Modeling Plate 3: Audit Loop, Pipeline Validation, and the Overnight Rate-Wall Incident

**Date:** 2026-06-06 → 2026-06-07 (overnight)
**Model:** Opus 4.7 orchestrator; `script-builder` (Sonnet) for all pipeline/cleanup/hardening tracks; `general-purpose` (Opus) for the independent alignment audit.
**Predecessor:** Session 83 (Plates 0+1+2 shipped, D2 resolved). This session executed the audit-loop design, built + validated the Plate 3 reification pipeline, and attempted the full sweep.

---

## 1. What this session set out to do

Coming out of S82's cleanroom analysis and S83's Plates 0–2, the edge-modeling reification project needed: (a) a standing audit mechanism so multi-session execution doesn't drift, (b) the Plate 3 backfill pipeline that actually reifies n-ary events onto event-node hubs, and (c) resolution of the two open questions Plate 2 surfaced (reify-all vs selective; fuzzy-reuse vs mint-floor).

## 2. The audit loop (codified)

Designed as a two-artifact loop, deliberately separating **facts** from **judgment**:

- **Reporter** (`working/edge-modeling/audit-repo-reporter-prompt.md`) — an in-repo agent that gathers ground truth (counts, diffs, validator runs) and appends a self-verifying entry (with a "Validator checks (bash)" block + "Flag drift if…" tripwires, a convention borrowed from the S83 hand-written log) to `working/edge-modeling/SESSION-LOG.md`.
- **Auditor** (`working/edge-modeling/audit-alignment-auditor-prompt.md`) — a **fresh** session (different from the executor — the non-negotiable fresh-eyes principle) that judges the facts against the design doc's intent and renders ON-COURSE / DRIFT / NO-GO, independently recomputing the load-bearing numbers rather than trusting the log.
- Runbook: `working/runbooks/edge-modeling-audit-loop.md` (Execute → Report → Audit → Gate; hard gates; baseline numbers).

The loop proved itself immediately: an independent Opus auditor blessed the Plates 0–2.5 block as **ON COURSE**, and in doing so resolved the lingering 10-vs-11 normalizer-flip discrepancy (it's **10**; the 11th was the flagged mutual-kill, correctly held, not flipped) and confirmed zero canonical writes.

## 3. D8 — reify on n-ary STRUCTURE, not event TYPE

Matt's question — "is there a node for the death of Aerys? does this balloon the node count?" — exposed an imprecision in the plan. The disposition table said "reify the killing family," which would wrap a clean one-on-one killing (Jaime/Aerys) in a hub that just re-encodes a 2-party fact. The fix (decision **D8**, recorded in design doc §3):

- **Clean dyad** (single agent + single patient, no instigator, not a shared named occasion) → **stays a direct edge**, direction-fixed by Plate 0. No hub.
- **N-ary event** (instigator≠executor, multiple killers/victims, named set-piece) → reify.

Empirically, **0 of the 102 current KILLS rows carry an instigator signal** — almost all are clean dyads. Combined with the Plate 2.5 inventory (the famous set-pieces already have nodes: `sack-of-kings-landing`, `red-wedding`, `assassination-of-tywin-lannister`, `purple-wedding`), this shrinks node-minting to near-zero. The "8,316 needs-mint floor" from S83 was an artifact of reify-all; selective reification (Q1) plus reuse-before-mint (Q2) keeps it small.

Also corrected: the **D3 RE-EXAMINED** note — S83's claim that Tywin's privy death and the Purple Wedding "have no hub" was wrong; both nodes exist, they just lack chapter linkage. The real Plate-3 need is a chapter-rebind step, not mass minting.

## 4. Plate 3 pipeline: build → validate → fix → harden

- **Build + smoke** (`scripts/edge-reify-backfill.py`): the Red Wedding smoke produced a correct hub — Roose Bolton → AGENT_IN (personal killer), Walder/Lothar/Tywin → COMMANDS_IN (orderers), victims → VICTIM_IN, Twins → LOCATED_AT. D7 honored, no instigator→victim collapse, Contract 10 pass, hub reused not minted. ~$0.06/call.
- **Mini-batch (12 events, $0.81):** validated the *selection* logic the smoke couldn't — the D8 gate correctly **skipped** Jaime/Aerys and Tyrion/Tywin as clean dyads; multi-chapter Red Wedding deduped to one hub; 7 hubs reused / 3 minted; group/faction AGENT_IN worked.
- **Bug caught (the value of the mini-batch):** supersede detection had false positives — it flagged `tyrion KILLS tywin` as superseded by Battle of the Blackwater (both are Blackwater participants) without checking chapter overlap. Fixed by requiring `edge.evidence_chapter ∈ event's chapter set`; supersede count 33→12, re-validated (false positives gone, true positives kept).
- **Hardening (code-only):** fail-fast on the rate wall (exit ≤~90s, no retry-loop burn), incremental per-event flush, a `processed-events.jsonl` ledger, `--resume` (verified 0 duplicates via dry-run + a mock-wall test).

## 5. Incident — the overnight rate-wall burn (postmortem)

An unattended full sweep was launched late; it passed the supersede re-validation and started the corpus run, then was **killed ~6 minutes in by the overnight rate-limit wall.** Crucially, before the fail-fast fix existed, the runner sat in **retry/backoff loops against the wall for hours**, consuming Matt's usage window while producing nothing, before being terminated. Disk evidence: `plate3-full/` last-written 22:56, only 37 minted nodes + 11 review-queue entries, no role edges, no summary.

**Root cause:** long unattended `claude -p` sweeps + a runner that retry-looped instead of failing fast.
**Lesson (now enforced):** any long `claude -p` pass must fail-fast on the wall and be resumable; prefer attended runs in resumable chunks. This is the same family as the S76 "bare worker sat idle all night" lesson and the project's existing `stage4-run-forever` philosophy.

When Matt asked "is something running?", an OS-level check (no live `claude -p`/python processes, no registered task) confirmed **nothing was running** — the overnight agents had all terminated; the morning relaunch had produced zero output and was explicitly killed.

## 6. Revised scope/cost

The full-corpus dry-run enumerated **~2,056 trigger-family candidate events** — far above the earlier 200-300 estimate. Many will be skipped as clean dyads by the D8 gate, but each non-trivially-deterministic candidate still needs one `claude -p` call, so real cost is **~$50-160** (vs the $16-24 previously quoted). Decision: **don't run all 2,056 blind** — run a cost-bounded calibration chunk first, read the actual reify/skip ratio + measured cost, then extrapolate. The runner is resumable, so chunking is free.

## 7. Staged cleanups (parallel tracks, zero graph writes)

- **Drift reclassify (Track A):** 12 `event.battle` nodes that are really TWoW/ASOS chapter articles → propose `meta.chapter`; 0 affected edges, 0 ambiguous.
- **Collision merge (Track B):** 6 near-duplicate event-node groups; 4 high-confidence auto-merges (wiki-redirect stubs carrying `same_as`), 1 medium (`conquest-of-dorne` vs `the-conquest-of-dorne` — the latter is the in-world *book*; reclassify to `object.text`, don't merge), 1 low (`tourney-at/of-maidenpool` — needs the AWOIAF page title). 0 affected edges.
- **Event-node inventory (Plate 2.5):** `scripts/event-node-inventory.py` → `event-node-inventory.md` + `event-node-reuse-lookup.json` (1,033 keys, 359 reuse-eligible, 12 drift flagged). This is the reuse lookup that makes Q2 reuse-before-mint possible.

## 8. State at session close

- **Graph untouched:** `edges.jsonl`=3811, 0 nodes minted into `graph/`, `git status graph/` clean.
- **Everything is staged** in `working/edge-modeling/` (incl. `plate3-full/` partial: 37 minted nodes + 11 review-queue).
- **Plate 3 full sweep is HELD/incomplete** — pipeline ready + resumable; awaiting an attended run (calibration chunk first).
- After the sweep: Reporter → fresh Auditor → human review of `hub-review-queue.jsonl` + `supersede-candidates.jsonl` → Plate 5 (the single gated merge, with before/after sign-off, folding in the staged cleanups + Plate 4 + the 3 S77 core-cleanups).

## 9. Things rejected / decided along the way

- Rejected: launching another long unattended background sweep (the overnight lesson). Attended + resumable chunks instead.
- Rejected: running the audit loop on Plates 0–2.5 as a self-report substitute — kept the independent fresh-session Auditor.
- Decided: `house.*` allowed as AGENT_IN for group actors ("Bolton men-at-arms" → `house-bolton AGENT_IN`).
- Decided: no `MUTUAL_KILL` vocabulary for the donal-noye↔mag flagged row — two directed KILLS edges already express it; it reifies to one death-event if ever needed.
