# ADJUDICATION — Jon Snow resurrection cluster (S219)

**Run:** `jonsnow-resurrection-theories-s219` · Fable orchestrator · Sonnet proposer · 2 Haiku adversarial fresh-verifiers
**Verdict: STAGED — 16 edges (13 → NEW `jon-snow-resurrection` + 2 SUPPORTS/1 CONTRADICTS → existing `azor-ahai-theories`), 1 new node. Mint-gated on Matt.**

## Machine trace

1. Substrate: 22 byte-verified beats (`substrate.jsonl`, theory "Jon's resurrection, second life, and Azor Ahai destiny") — grown from ~16 by the S219 byte-fail redo pool.
2. Proposer: 16 edges, Z7/Z8/Z9 dedup enforced (grep of all 14 existing azor edges; 2 near-misses vs Z6 excluded: B63/B81 same affc-samwell-04:21 line).
3. Deterministic quotecheck: **16/16 ALL FOUND**.
4. Fresh-verify: V1 (refute-lens) **16/16 CONFIRM + NODE PASS** · V2 (semantics/boundary-lens) **16/16 CONFIRM + NODE PASS**. Zero adjustments required — cleanest wave-2 verdict.
5. Scratch dry-run mint: 16 appended / 0 dup-skips; node written to scratch root only.

## Orchestrator rulings

- **JR1 + JR8 (proposer-found, extra-substrate):** ACCEPTED. Both byte-verified, both confirmed by both verifiers; JR1 is the natural subject-link (Jon's dying word "Ghost", sourced from `jon-is-stabbed-repeatedly` per the layer rule). Precedent note: proposer additions remain legitimate when they pass the same quotecheck + adversarial gates as substrate rows.
- **Mechanic-vs-candidacy split upheld:** resurrection mechanics on the new node; AA-candidacy readings routed to `azor-ahai-theories` (JR14/15/16). V2 specifically audited the boundary — zero duplication, the node text explicitly holds out the identity claim.
- **Tier distribution:** 8× t3 (direct in-world precedents: Orell/Varamyr/Haggon/Thoros/Stoneheart/legend texts) + 8× t4 (visions, foreshadowing, structural parallels). No t5 needed.
- **B42 (wolf blood) cut** by proposer for claim-stacking on R+L=J — upheld; restorable as t5 later if wanted.
- No CONTRADICTS forced onto the new node: the Bloodstone-Emperor counter-legend never grounded (TWOIAF-only; confirmed by redo worker-1's logged attempts).

## Substrate-integrity notes (feed forward)

- 6 beats carried `verbatim_quote: null` out of the substrate assembler (deterministic-matcher rows whose quote lived in a different field) — proposer independently re-extracted + byte-verified all 6; assembler gap noted, harmless this run because quotecheck gates everything downstream.
- B64's paraphrase misdescribed its own quote ("descended from Aerys" vs the actual Nissa Nissa passage) — used for what it actually says.
