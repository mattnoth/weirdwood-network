# SESSION 200 — Fire & Blood APPLY-GO: first real mint (4 smoke units) → then bulk
> **This is Session 200.** Stamp your worklog entry `### Session 200` at endsession.
> **Recommended model:** **Fable** — first-ever real graph writes of the F&B track; disposition
> surgery + dispute-adjudication judgment + §8 pipeline shakedown justify the depth. The BULK
> extraction afterwards is Opus `claude -p`, **Matt-fired from iTerm** (`feedback_no_extraction_without_asking`).

## State (S199 close — trust worklog.md over this if they diverge, CLAUDE.md rule 9)
ALL §7 pre-bulk gates are GREEN (S199): two-stage smoke ✅; out-of-sample accept validation
**0 wrong / 66 rows** ✅; dispute-axis audit v1 FAIL 26.9% → dispute-proximity quarantine built →
v2 **PASS 0.0%/0.0%** ✅; CREATE fresh-verify caught a semantic dupe in 3 of 4 units (permanent
per-unit step). Tests 63/63 (`scripts/test-fab-reconcile.py`). 4 units reconciled `--smoke` under
`working/fire-and-blood/smoke/v1/recon-{heirs-15-p01,heirs-15-p02,sons-05-p01,after}/`.
NOTHING minted yet. Record of everything: `working/fire-and-blood/smoke/v1/EVAL-stage2-reconciler-tuning.md`.

## The task — §8 apply, unit by unit (design `fire-and-blood-enrichment-design.md` §8)
**Get Matt's explicit apply-go FIRST (in-session, before any write)** — this prompt existing is not permission (`feedback_no_graph_mutation_without_goahead`).
0. **Re-reconcile all 4 units WITHOUT `--smoke`** (fresh out-dirs) so auto-accept actually routes
   (smoke held 15 discriminator + 130 exact accepts to review). Diff the non-smoke matched.jsonl
   against the smoke would-accept lists in `EVAL-oos-accept-validation.md` — must match; any NEW
   accept not in the validated set gets eyeballed before apply.
1. **Land the staged batch:** `working/fire-and-blood/architecture-batch-s198.md` → architecture.md
   (evidence_kind `book-fab`, `in_universe_source`, `disputed`, tier invariant) + the 3-line mint
   patch (`in_universe_source`/`disputed` passthrough) + this session's mint lockstep diffs are
   already in the tree. One worklog Active Decision covers the batch.
2. **Apply dispositions to the smoke outputs before mint:**
   - Folds (CREATE→UPDATE onto existing): `aegons-second-coronation`→`aegons-coronations`;
     `baelon-avenges-aemon-on-tarth`→`myrish-bloodbath`; `accession-melee-at-maidenpool`→
     `tourney-for-king-viserys-is-accession`; `death-of-alyn-stokeworth`→`harren-the-reds-rebellion`;
     `daemon-slays-craghas-crabfeeder`→fold into `war-for-the-stepstones` OR mint with PART_OF (Matt's call).
   - Renames: `birth-of-aegon`→`birth-of-aegon-ii-targaryen`; `birth-of-maegor-targaryen`→`birth-of-maegor-i-targaryen`.
   - Add on CREATE: `summoning-of-vaegon` CAUSES → `great-council-of-101-ac`; PART_OF/CAUSES edges
     for granular conquest events back to `field-of-fire`/`conquest-of-dorne` (S199 stage-1 note).
   - Graph hygiene: strip junk `"Lorath"` alias off `jaqen-hghar`.
3. **Adjudicate the 19 dispute-held rows** (`dispute-review.jsonl` × 4 units): fresh subagent
   reads each held row ±context → verdict tag-as-disputed(+in_universe_source, tier-2) / clear
   (false hold — flat fact) / drop. Feed results back as edge edits before mint. The audit v2
   says ~10/19 are false holds ("mushroom" non-attributive) — expect roughly half to clear.
4. **Per-unit §8 order:** git checkpoint commit → `mint_enrichment.py --candidates …` →
   `fab_merge_node.py --merge-plan …` (summary MUST show 0 skipped UPDATE payloads) →
   `finalize_enrichment.py` if verdicts exist → after all 4 units: `weirwood refresh`.
5. **Verify:** spot queries (`weirwood query` on rhaenyra/daemon/corlys + one CREATE slug);
   identity swaps landed (18 boilerplate targets upgraded); edges.jsonl delta sane; run
   `scripts/test-fab-reconcile.py` still 63/63. Rebuild-derived-artifacts rule satisfied by refresh.
6. **Hand Matt the bulk block** (35 remaining units, Matt-fired, ~5h sequential; use
   `stage4-run-forever.sh`-style patience per `working/fire-and-blood/fire-and-blood-extraction.py`
   `--resume`; observability = `run-summary.jsonl` per §7a: quote-located% ≥90, disputed_rate ≈0
   on a Dance unit = prompt failure, `created` spike = resolver failure, `dispute_held` spike = OK on gossip units).

## Read first
- `working/fire-and-blood/smoke/v1/EVAL-stage2-reconciler-tuning.md` (S199 record: every fix/gate/disposition)
- `working/fire-and-blood/fire-and-blood-enrichment-design.md` §8 (apply order), §7a (observability)
- `working/fire-and-blood/build-spec-s198.md` (amended interfaces: run_id keeps -pMM; new sidecars)
- `working/fire-and-blood/architecture-batch-s198.md` (the staged schema batch)

## Open questions for Matt: craghas fold-vs-PART_OF (step 2); everything else decided S199.
## DO NOT
- Do NOT write graph/nodes/ or edges.jsonl before Matt's explicit in-session apply-go.
- Do NOT run extraction yourself (Matt fires bulk from iTerm). Do NOT touch the extraction prompt.
- Do NOT skip the per-unit git checkpoint, the fresh-verify/adjudication, or `weirwood refresh`.
- Do NOT touch the parked strip-boilerplate track (parked behind F&B FULL apply — all packs, not just these 4).
- Do NOT auto-run /endsession.
