---
session: 204
date: 2026-07-10
model: Fable 5 (orchestrator) + Sonnet 4.6 (10 proposers) + Haiku 4.5 (10 fresh-verifiers)
track: fire-and-blood (graph)
---

# Session 204 — The F&B causal spine

## Goal

Wire the ~300-node Targaryen-history event layer causally. At session start the layer had
**9 causal edges** and 294 causally-dark nodes; the S203 live probe had shown
`walk_chain(death-of-queen-rhaenyra)` returning EMPTY — the chat UI's chain panel was bare
for the entire Dance. Inputs staged by S203: 53 causal-spine harvest seeds, 38 zero-edge
stubs, ~90 minted Dance events.

## The machine (novel this session)

A three-layer machine, all instructions in `working/fire-and-blood/causal-spine-s204/`:

1. **Deterministic prep** (`build-manifest.py`, `build-packets.py`): fab-layer inventory
   (pass_origin + era + book-fab-edge-touched — the third signal was load-bearing: the
   marquee wiki shells like `battle-of-the-gullet` carry no `era:` and pre-date
   `pass_origin`), per-node causal census, seed→slug token-overlap candidates, per-section
   work packets. Found and fixed two seed errors before dispatch (row 225's "Battle in the
   Gullet" was mis-attributed to a Maegor-era unit — the snippet "battle was joined" matched
   the Faith Militant's Stonebridge; real location 17-p02:25).
2. **10 Sonnet proposers** (one per section group, `SHARED-RULES.md` pasted): typed
   CAUSES/TRIGGERS/MOTIVATES/ENABLES/PART_OF edges with verbatim quotes, wired stubs,
   minted missing chain anchors. Proposer tier per `feedback_enrichment_board_causal_lens`
   (Sonnet ≈ Opus for proposal; orchestration is the bottleneck).
3. **10 Haiku fresh-verifiers** (`VERIFY-RULES.md`, adversarial, one per proposal file):
   **249 CONFIRM / 19 ADJUST / 2 REJECT**. Every non-CONFIRM orchestrator-adjudicated with
   the text open (`orchestrator-adjudications.md` — the full decision log). Assembly via
   `assemble-candidates.py` (locked-vocab check, live-graph + cross-proposal dedup,
   mint-identical quote locator).

**Haiku catches that mattered:** a battle "MOTIVATES" a birth (quote grounded the naming
decision — child born 7 days earlier); Larys typed `AGENT_IN` the poisoning when the text
says "the hand that poisoned the Arbor red will never be known" (→ the S203 `SUSPECTED_OF`
already covered it — dropped as dup); `CAUSES` where Criston Cole's threat mediated Aegon's
acceptance ("My sister is the heir, not me") → ENABLES; the E14 Great-Council edge grounded
only in Gyldayn's hellhorns *foreshadowing* line → ENABLES. Orchestrator rejected one
verifier suggestion (A-E11: MOTIVATES→character is the documented disposition form; no
resignation-event mint needed).

## Incident — monthly spend limit

Mid-session the account hit its monthly spend cap; 6 in-flight agents died (3 batch-3
proposers + 3 verifiers). Two of the "failed" verifiers had already written **complete**
output files before dying — validated by coverage check (verdict ids == proposal ids) and
kept. After Matt raised the limit, the 4 genuinely-lost agents were relaunched verbatim.
No work was duplicated or lost. Lesson: check output files before re-running "failed"
subagents — the failure timestamp is the agent's death, not the deliverable's.

## Live-probe supplements (3 small packs after the main mint)

The success-criteria probes caught three gaps the packet structure had hidden:
1. `fight-above-shipbreaker-bay` ↔ `death-of-lucerys-velaryon` unlinked (the fight and the
   death were separate proposer concerns) → `TRIGGERS`, "Arrax fell, broken…".
2. `peace-with-the-sealord-of-braavos` stub unwired — orchestrator under-listed it in the
   I2122 dispatch prompt (the packet had it; the prompt's explicit list won). Wired to
   `manfryd-mooton` + the existing `celtigars-new-taxes-on-kings-landing`.
3. `viserys-names-rhaenyra-heir` had 0 downstream after dropping the two weak
   faction-MOTIVATES edges → `ENABLES coronation-of-rhaenyra` grounded in Beesbury's
   council argument (16-p01:75), threading the succession decree into the whole Dance spine.

## Results

- **258 edges + 41 event nodes** minted (packs: `apply/fab-causal-spine-s204/`,
  candidates.json + 3 supplements). Edges.jsonl 25,035 → **25,293**; events 993 → **1,034**.
- Type mix: 70 MOTIVATES / 62 ENABLES / 36 CAUSES / 35 TRIGGERS / 10 PART_OF / 9 SUB_BEAT_OF
  / role edges — ENABLES-heavy as the agency-preserving rubric intends.
- Layer: causal edges 9 → **212**; causally-dark 294 → **126**; zero-edge stubs 38 → **0**.
- All 53 seeds consumed (2 honestly flagged as commentary/too-thin, not forced).
- Marquee chains (all 0 at start): death-of-queen-rhaenyra 7 · death-of-aegon-ii 9 ·
  murder-of-prince-jaehaerys (hub minted) 6 · storming-of-the-dragonpit 10 ·
  battle-of-the-gullet 3 · viserys-names-rhaenyra-heir 9 · death-of-maegor-i 7.
- Anchor mints include: death-of-viserys-i, green-council-conceals-death-of-viserys,
  coronation-of-aegon-ii, murder-of-prince-jaehaerys (Blood & Cheese), the-sowing,
  death-of-helaena-targaryen, accord-of-storms-end, death-of-rhaenys-targaryen,
  the-dragons-wroth, death-of-aenys/maegor, death-of-dalton-greyjoy.
- Gates: fab-semantic-gate 4/4 PASS · 153 fab-reconcile · 1,457 pytest · 100 deno · no
  golden shifts.
- **Deployed to prod** (Matt's go): commit `74e1404c19` pushed, `netlify deploy --prod
  --build`, live-verified with a paid probe ("Why did Rhaenyra die?" → 3 tool calls, 3/3
  cites verified incl. the "You fed his mother to your dragon" quote, $0.037 logged).

## Residue (logged in todos)

- Suspected dup: `lord-rogars-war` vs `third-dornish-war` (E14 targeted the latter only).
- Mistyped: `maidens-day-ball` / `regency-of-aegon-iii` carry `event.battle`;
  `archon-of-tyrosh-war-of-the-ninepenny-kings` is `event.war` used as a person.
- Backwards wiki edge: `assault-on-harrenhal DEFEATS blacks` (Track B Result parse).
- Unminted flagged beats: Prince Daeron's death at Second Tumbleton (3 conflicting
  accounts), Prince Gaemon birth/death pair.
- Harvest queue at 66 open rows (48 S204 + 10 canonicalized pre-S204 strays + 8 older) →
  drain staged as the next session's live prompt; cross-era seams queued right behind it.
