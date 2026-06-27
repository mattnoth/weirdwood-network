# Continue prompt — SIFT Stage 1 (PARKED — resume after the enrichment campaign)

> **Status: DEFERRED. Do NOT start this on your own.** The whole Sift track is paused until Matt says the
> enrichment phase feels done (worklog.md Active Decisions → "DEFERRED (S157) — the SIFT track is parked"). This
> prompt is parked in `archive/` on purpose — the one *live* continue prompt stays the enrichment track. Only pick
> this up when **Matt explicitly reopens Sift.**

**Recommended model:** Sonnet 4.6 for any engine/lexicon codegen (matches the original build). Haiku
(`claude-haiku-4-5-20251001`) for the Stage 2 bulk pass when it's built. Opus only for review/synthesis.

## Where it stands (parked 2026-06-27, after an Opus review pass)
- **Stage 1 is BUILT, smoke-tested, deterministic.** Engine: `scripts/sift.py`. CLI: `weirwood sift status|run|sample`.
- **Lens:** `working/sift/lenses/oaths.lens.json` — **v2, 74 triggers** (recall-only expansion; exclusions still `[]`).
- **Latest AGOT smoke:** 172 pointers → **133 clusters**, byte-identical re-runs. Output: `working/sift/oaths/agot.pointers.jsonl` + `agot.coverage.json`.
- **Read these to reload context:**
  - Design (authoritative): `working/sift/sift-design.md` (§0 component table + the Opus-review delta notes)
  - Opus review + v2 re-smoke: `working/sift/smoke-test-report-v2.md`
  - v1 builder report: `working/sift/smoke-test-report.md`
  - Pipeline diagram: `working/sift/sift-pipeline-diagram.svg`
- **Opus-review engine deltas already shipped:** `cluster_id`+`cluster_size` (co-located hits → one Stage-2 work
  unit; corrects the v1 "cand_id dedups multi-fire" error), `ptr_id`, machine-readable `<book>.coverage.json`,
  `sift sample` verb, input+output sha256 manifest.

## What's NEXT when Matt reopens it (in order)
1. **Matt reviews lens v2.** Veto any of the 33 recall additions you dislike (table in the recall audit; reversible — delete the v2 trigger block to restore v1, backed up at the original session scratchpad / in git history).
2. **Decide first `exclusions`** — seed stop-phrases from the noisy `'I swear'` rows (≈80% casual), or leave precision entirely to Haiku. This was deliberately left to Matt.
3. **Full-corpus Stage 1:** `python3 scripts/sift.py run --lens oaths` (all 5 books; pure Python, $0, safe/additive).
4. **Build Stage 2 `interpret`** (currently a stub): Haiku, **gated** (prints volume+cost, asks before firing),
   and **cluster-driven — ONE Haiku call per `cluster_id`, never per pointer** (else the NW vow = 9 calls + 9 dup
   candidates). Output = gated candidate rows for Matt's review; **never auto-merge into `graph/nodes/`.**
5. **Codify the track:** add a worklog Active Decision naming *the corpus-sift track* + the `sift`/`lens` vocabulary (still pending per design §0).
6. **Heraldry lens** is queued as the 2nd lens once oaths is proven end-to-end.

## Hard rules (carry forward)
- Read LOCAL only (`sources/chapters/`, `graph/nodes/`) — never fetch the wiki.
- **Edge-minting stays deferred** until the enrichment track frees the edges layer (two tracks writing `edges.jsonl` is the exact serialized-enrichment conflict). Stage 1's cluster map is a *read-only oath index* the enrichment track can use meanwhile.
- Sift never writes `working/harvest-queue.md` (own dir, header lines).
- Stage 2 gated; agents propose, Matt decides.
