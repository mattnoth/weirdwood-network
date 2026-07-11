---
session: 211
date: 2026-07-11
model: Fable 5 (claude-fable-5) orchestrator · Sonnet 4.6 proposers ×3 · Haiku 4.5 verifiers ×3
track: graph
---

# Session 211 — Highest-value menu → edge-vocab retrofit Part B → promotion sweep → the routing-gap find

## Shape of the session

Opened per the S210 handoff: reconstructed the last-10-sessions high-priority items
(Matt's ask), presented the ranked highest-value menu, Matt picked **option 1 (edge-vocab
retrofit Part B)** with "cheaper subagents where possible" — then, with context to spare,
rolled straight into **option 3 (node-type promotion sweep)**, a deploy, and two
unplanned finds. Four commits, three prod deploys.

## Part B — the dip machine at its cheapest

Deterministic prep first (`working/edge-retrofit-s211/scan-candidates.py`): 41 knighting +
75 suspicion passage packets with existing-pair exclusion sets baked in. 3 Sonnet
proposers (SHARED-RULES: quote-grounding hard requirement, whodunit honesty rules,
harvest capture) → 34 raw candidates, all book-quote-grounded, zero invented slugs →
3 Haiku adversarial verifiers: 31C/2A/1P.

**The adjudication was where the session earned its keep.** Three of the six
non-trivial calls were *history collisions the verifiers couldn't see*:
- Vance/Piper SUSPECTED_OF the Blackfish escape — re-proposals of S159 fresh-verify
  REJECTS E14/E15 (found the original verdict file; dropped).
- Petyr SUSPECTED_OF murder-of-jon-arryn — re-proposal of the edge S148 deliberately
  retired for COMMANDS_IN (the Haiku verifier independently converged: PROBLEM
  `proven-not-suspected`). Root cause both times: **stale node prose** documenting
  edge states that were later adjudicated away — both fixed this session.
- Corlys/death-of-aegon-ii — the proposer flagged rather than proposed; primary-text
  read (fab-hour-of-the-wolf-20 confession + conviction) → orchestrator-added
  `AGENT_IN` tier-1, while Larys's tier-2 SUSPECTED_OF stands per S202/S203.

Plus one upgrade: Tyrion SUSPECTED_OF plot-to-free-jaime → **COMMANDS_IN tier-1**
(his own POV proves the four-false-guardsmen scheme, acok-tyrion-06). Final batch:
**30 edges** (18 SUSPECTED_OF tier-2 · 10 KNIGHTED_BY tier-1 · 1 AGENT_IN · 1
COMMANDS_IN), quotecheck 30/30, minted on Matt's go → edges.jsonl **26,382**.

## Promotion sweep (piggybacked)

Promote-only-where-slug-AND-content-agree: **12 retypes** (7 battle→war via the S207
Blackfyre-rebellion precedent; 2 murders→assassination via comparables
[joffrey/tywin/renly]; 2 arrests→capture; winterfell-murders→death), **5 documented
holds** — the interesting one being `abduction-of-lyanna` staying `incident` because
`event.capture` would assert the abduction reading of R+L. Harm-gate interaction
checked BEFORE applying (war ∉ HARM_EVENT_SUBTYPES; no VICTIM_IN on the war
promotions). Surgical per-node index patches, no 8.4k refresh churn. Record:
`working/edge-retrofit-s211/PROMOTION-SWEEP-s211.md`.

## The routing-gap find (the sleeper)

Post-deploy verify probe "Who knighted Gregor Clegane?" → the live agent answered
**"the text here does not reveal"** while `gregor-clegane KNIGHTED_BY
rhaegar-targaryen` sat in the deployed bundle. Blob toolTrace showed why: resolve →
read_node (dossier: no edges) → search_quotes (sees node quotes, not edge evidence) —
**the routing table had no row for relationship-fact questions**, so typed-edge facts
were unreachable unless a question phrased as "how are X and Y connected". This
predates S211 and silently nullified much of the typed-edge layer's chat value.

Fix: a "Who did X to Y / relationship facts" routing row + a stronger neighbors tool
description in `agent.ts` SHARED_RULES (length pin updated 12489→13212 with dated
comment, per the S203 precedent). Redeployed; the same probe now answers in 2 tool
calls citing the new edge verbatim, 0 unverified cites. **Lesson: a live-probe verify
turn after graph-layer ships is worth its $0.05 — bundle-presence ≠ answer-reachability.**

## Numbers

- Edges 26,352 → **26,382**; SUSPECTED_OF 23→41; knighting edges 16→26.
- Event types: incident 306→301, battle 280→273, war 56→63; all 22 live types sanctioned.
- Suites at close: gate 4/4 · pytest 1458 (bundle goldens re-armed post-deploy) · deno 100.
- 3 prod deploys (`6a52c19f` graph batch · `6a52c2f2` routing fix · `6a52c383` prose fixes).
- Harvest: 3 → 17 open (14 new pointers; under the ~30 bar).
- Subagent spend: ~590k tokens Sonnet (proposers) + ~300k Haiku (verifiers).

## Records

`working/edge-retrofit-s211/` — SHARED-RULES.md · VERIFY-RULES.md · packets/ ·
proposals/ · verify/ · candidates.json · ADJUDICATION-s211.md · PROMOTION-SWEEP-s211.md.
