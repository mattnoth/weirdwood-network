# Bolt-On cluster — orchestrator adjudication (S216)

**Machine:** Sonnet proposer → 2 Haiku adversarial fresh-verifiers (edges: 4C/2A/2R · prose: CLEAR) → Fable adjudication → quotecheck → dry-run. **STAGED — no mint (Matt S214 standing).**

## Adjudications (Fable orchestrator)

| edge | verdict | action |
|---|---|---|
| B3 (Roose "secret of a long life") | ADJUST | KEPT, tier-3→tier-4 — supernatural-longevity reading is an interpretive step |
| B4 ("pale grey mask") | REJECT — cherry-picked | **DROPPED**: the passage grotesques EVERY wedding guest (mastiff/vulture/gargoyle/fox/bull); the body already documents the passage under Evidence Against with full context — the defect was that a SUPPORTS edge existed at all |
| B6 (Coldhands wight physiology) | REJECT — zero Roose connection | **DROPPED**; body keeps it as the labelled imported-analogy prose it always was |
| B8 (flaying culture) | ADJUST — thematic scaffolding | **DROPPED to prose** per the T8 premise-prose precedent (theme ≠ evidence) |
| B1, B2, B5, B7 | CONFIRM | as proposed; B1(SUPPORTS)/B2(CONTRADICTS) same-source pair adjudicated coherent, not double-dipping — B1 = the union mechanism exists, B2 = Old Nan's own punchline rules out "a Bolton" |

**Final: 5 edges** (4 SUPPORTS + 1 CONTRADICTS; 1× tier-3, 3× tier-4, 1× tier-3 CONTRADICTS) → `roose-bolton-theories` (ENRICH of the live stub, node tier-4, status open). Display name claim-style "Roose Bolton is a skin-stealing immortal" per the ratified KotLT precedent.

## Gates

- quotecheck 5/5 ALL FOUND (post-adjudication re-run)
- prose fresh-verify CLEAR (all six discipline categories; 8/8 spot-checked quotes verbatim)
- dry-run mint GREEN on scratch (5 appended, 0 dup; enrich-only — no new node; live graph untouched)
- tier audit: no tier-1/2 anywhere

## Notes

- Standout: B2 — the strongest CONTRADICTS in the theory layer so far (Old Nan's text explicitly names the Night's King "a Stark", killing the theory's founding Bolton-ancestor framing in its own source story); the source video never raises it.
- Proposer self-caught a spliced-quote defect (B7) via its own byte-verify before handoff.

MINT GATE: pending Matt. On go: `scripts/mint_enrichment.py --candidates working/theories/bolton-cluster/candidates.json` + apply `enrich/roose-bolton-theories.node.md` over the stub + refresh + architecture.md sync (shared batch).
