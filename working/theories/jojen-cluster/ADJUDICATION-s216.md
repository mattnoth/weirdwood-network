# Jojen Paste cluster — orchestrator adjudication (S216)

**Machine:** Sonnet proposer → 2 Haiku adversarial fresh-verifiers (edges: 8C/1A/0R · prose: CLEAR) → Fable adjudication → quotecheck → dry-run. **STAGED — no mint (Matt S214 standing).**

## Adjudications (Fable orchestrator)

| edge | verdict | action |
|---|---|---|
| J5 ("Only he was, in a way") | ADJUST | KEPT, tier-4→tier-5 — genuinely ambiguous pronoun two books before the key scene; weakest-grade foreshadowing marker |
| J8 (empty alcove) | CONFIRM + caveat | KEPT tier-3, note strengthened: the text confirms ABSENCE only — absence-equals-death is the theory's inference |
| J1–J4, J6, J7, J9 | CONFIRM | as proposed (incl. J6 CONTRADICTS — Bloodraven's stated purpose for the paste — and the two novel source-node types: `weirwood-paste` [foods] and `rat-cook` [legend]) |

**Final: 9 edges** (8 SUPPORTS [5×t3, 1×t4→see J5 t5, 1×t4] + 1 CONTRADICTS t3) → `jojen-paste` (NEW node, tier-4, status open).

## Substrate integrity find (worth noting)

The proposer caught a false-positive grounding in the substrate itself: beat jojen-B33's video paraphrase claimed a Sansa-about-Cersei quote; the matched text (affc-cersei-10.md:173) is actually **Kevan Lannister speaking**. No edge minted; documented in the node's Ungrounded material. Second S216 instance of the machine catching substrate drift (after the Bolt-On B2 punchline find).

## Open questions carried to Matt

- Novel source-node types ratification: a `foods` node (weirwood-paste) and a legend/`texts`-class node (rat-cook) as SUPPORTS sources — both adjudicated sound here (each is the entity the quote is about), flagged for convention ratification.
- J6 CONTRADICTS vs premise-prose was flagged by the proposer; adjudicated KEEP as edge (Bloodraven's stated purpose is genuine on-page counter-evidence, not premise).

## Gates

- quotecheck 9/9 ALL FOUND (post-adjudication)
- prose fresh-verify CLEAR (8/8 spot-checks verbatim; all categories clean; the crescent-moon honesty note commended)
- dry-run mint GREEN on scratch (9 appended, 0 dup; live untouched)
- tier audit: no tier-1/2

MINT GATE: pending Matt. On go: `scripts/mint_enrichment.py --candidates working/theories/jojen-cluster/candidates.json` + refresh + architecture.md sync (shared batch).
