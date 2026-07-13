# A+J=T cluster — orchestrator adjudication (S216)

**Machine:** Sonnet proposer → 2 Haiku adversarial fresh-verifiers (edges: 3C/2A/0R · prose: CLEAR-WITH-NOTES) → Fable adjudication → quotecheck → dry-run. **STAGED — no mint (Matt S214 standing).**

## Adjudications (Fable orchestrator)

| edge | verdict | action |
|---|---|---|
| A1 (Barristan "liberties") | ADJUST | KEPT tier-4 + context note — the surrounding passage is hedge-saturated (kitchen-gossip framing, immediate regret) but the liberties clause itself is Barristan's direct careful assertion, not the gossip layer |
| A2 (cisterns punishment) | ADJUST | **DROPPED to premise prose** — Tywin's early cruelty fits every reading (Joanna's death, dwarf prejudice) equally well; consistent-with ≠ evidence-for (T8/B8 precedent) |
| A3 (dying "no son of mine") | CONFIRM | KEPT tier-4 — the insult-vs-paternity ambiguity is real and the note carries it |
| A4 (Genna "Tyrion is Tywin's son") | CONFIRM | KEPT tier-3 CONTRADICTS — the plain reading asserts legitimacy |
| A5 (Tytos-mistress mirror) | CONFIRM | KEPT tier-4 CONTRADICTS — generational-pattern alternative to the secret-parentage motive |

**Final: 4 edges** (2 SUPPORTS tier-4 + 2 CONTRADICTS [t3+t4]) → `a-plus-j-equals-t` (NEW node, tier-4, status open). Deliberately small: only 9/28 video beats grounded — the cluster's size honestly reflects the theory's thin textual substrate (the CONTRADICTS pair is as strong as anything supporting it, which is the point).

**Prose note applied:** the "three years earlier" temporal ambiguity reworded to precedent framing (verifier's suggested fix).

## Gates

- quotecheck 4/4 ALL FOUND (post-adjudication)
- prose fresh-verify CLEAR-WITH-NOTES (6/6 spot-checks verbatim; the one MINOR fixed in-session)
- dry-run mint GREEN on scratch (4 appended, 0 dup; live untouched)
- tier audit: no tier-1/2

MINT GATE: pending Matt. On go: `scripts/mint_enrichment.py --candidates working/theories/ajt-cluster/candidates.json` + refresh + architecture.md sync (shared batch).
