# Session 196 — Fable design review of the Fire & Blood plan + companion track; v2 docs applied

**Date:** 2026-07-06
**Model:** Fable (claude-fable-5)
**Track:** graph (design-only — no builds, no graph mutation)

## What this session was

Matt fired the prepared handoff (`working/fire-and-blood/fable-review-handoff.md`): an adversarial design review of the Fire & Blood node-first enrichment plan and its wiki-prose disambiguation companion, widened this turn to *apply* the accepted recommendations into the design docs so a cheaper agent can execute them.

**The full review narrative lives in `working/fire-and-blood/fable-review.md`** — verdict, factual corrections C1–C5, per-decision rulings on all 10 open items, 8 ranked risks, completeness findings, companion assessment. This detail file records only what's not in the review: how the load-bearing findings were verified.

## Verification highlights (read-the-code-not-the-claim moments)

- **Ran the live resolver:** `weirwood query resolve "Aegon Targaryen"` → confident `HIT` on `aegon-targaryen`, then read the node: zero edges, boilerplate-only, `wiki_source` = the wiki's *disambiguation page* (confirmed via `page-categories.jsonl` category `Disambiguation pages`; same for bare Aemon/Baelon/Daeron/Jaehaerys/Rhaena). This inverted the doc's §5.1 risk model — confident wrong-match, not duplicate-minting, is the primary failure.
- **Read `mint_enrichment.py`:** nodes are skip-if-exists (line ~262), not overwritten — v1's §5.3 data-loss premise was wrong; the real gap is silent UPDATE-drop. Also caught the fail-fast `sys.exit` on any unfound quote → the OCR-noise operational hazard (row-level quarantine added in v2).
- **Read live nodes:** `rhaenyra-targaryen` is not a stub (~90 lines of wiki-cited prose under a boilerplate Identity line); `aegon-targaryen-son-of-baelon` has no `## Identity` section at all. Three node shapes now drive both tracks' merge-writer specs.
- **Checked `edges.jsonl`:** 23,099 rows; born/died years are NOT edges (companion doc's "verified" claim was false). Found the correct deterministic source instead: MediaWiki categories (`"84 AC births"` / `"85 AC deaths"`) in `page-categories.jsonl`.
- **Grepped `Rfab` anchors:** 1,634 nodes carry wiki citations into specific F&B sections (221 for Heirs of the Dragon) → the free per-unit candidate-pack idea (§5.0).
- **Checked `worklog-dunk-egg.md`:** the `claude -p`-under-`longrun.sh` extraction pattern has never completed a unit (DE-1 auth-blocked) — F&B's "reuse the D&E shape" inherits unproven glue; smoke stage 1 doubles as its first proof.

## Decisions (all recorded in the docs; Matt's go still gates everything)

Go-with-changes on node-first. All 10 §11 items ruled (see review §3). Sequencing: companion track FIRST, restructured to emit a machine-readable disambiguation pack + trap-node blocklist the F&B reconciler consumes. New schema batch staged for one Active Decision when Matt approves: `fab` book code, `evidence_kind: book-fab`, edge fields `in_universe_source`/`disputed` (+ disputed⇒≤tier-2 invariant), `disambiguation_hub` frontmatter flag.

## Artifacts

- `working/fire-and-blood/fable-review.md` (new — review of record)
- `working/fire-and-blood/fire-and-blood-enrichment-design.md` → v2 (execution-ready)
- `working/node-enrichment-wiki-prose/design.md` → v2 (execution-ready)
