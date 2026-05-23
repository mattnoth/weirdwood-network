# Stage 4 Pass-1-derived edges — LLM tail + recovery backlog + deprecate-comention

> **Recommended model:** **Sonnet 4.6** for the LLM tail (it's a small, bounded typing job) and the deterministic recovery work. **Opus 4.7** only for a final validation/weird-result review pass over the combined edges. Do NOT use Opus for per-item typing.
> **Trust worklog.md over this prompt if they differ** (CLAUDE.md #9). Authoritative state: worklog Session 66 + Active Decisions ("Stage 4 pivots to a Pass-1-derived deterministic edge pipeline").

## Where things stand (Session 66, 2026-05-23 — DONE)

The deterministic spine is BUILT, tested (278 green), validator-clean, conform-clean, and committed (`047e49b3b`, not pushed). It emits **2,818 typed, ~99%-cited `book-pass1` edges at zero LLM cost**.

- Scripts: `scripts/stage4-pass1-edge-candidates.py` (parse→resolve→type→corroboration-flag), `scripts/stage4-pass1-evidence-locator.py` (verbatim quote + `file:line`), `scripts/stage4_name_resolver.py` (5-rung collision-aware resolver). Regenerate the whole output in seconds: `python3 scripts/stage4-pass1-edge-candidates.py --apply && python3 scripts/stage4-pass1-evidence-locator.py --apply`.
- Output (gitignored, regenerable): `working/wiki/pass2-buckets/pass1-derived/{book}/`:
  - `*.edges.jsonl` — final typed `book-pass1` edges (the 2,818).
  - `_tail/{book}/*.tail.jsonl` — **untyped-but-resolved rows, citation already attached** → this is the LLM-tail input.
  - `*.needs-qualifier.jsonl` — typed rows whose edge type is Tier-1 (qualifier REQUIRED) but no qualifier was inferred; deferred.
- Tracked audit reports: `working/wiki/data/pass1-derived-{candidates-summary.md, candidates-stats.json, locator-stats.md/json, needs-node.md, ambiguous-review.md, firstname-aliases.json, conform-report.md}`.
- Key recalibration (don't re-hype): **resolution, not typing, was the wall.** 7,398 rows → 2,818 edges = 38% (not the design's "~50%"). The remainder is logged, never silently dropped.

## Recommended sequence (recovery FIRST, then tail — recovery grows both the edge set and the tail before you pay for LLM)

### Track A — Deterministic recovery backlog (no LLM, no permission needed)
Goal: recover more of the 5,141 still-unresolved rows by improving name→slug coverage. Two inputs:
- `working/wiki/data/pass1-derived-needs-node.md` — **387 distinct unresolved names** (after S66 first-name enrichment). Triage: which are real nodes missing an alias vs. genuinely missing nodes vs. multi-name cells ("Robb, Bran, Rickon, her mother" — comma-splitting was deliberately OUT of scope in v1; consider adding it).
- `working/wiki/data/pass1-derived-ambiguous-review.md` — **924 ambiguous-queued rows** (a name matched multiple nodes, none confidently picked). Each row lists the candidate slugs + chapter + POV. Many can be resolved by adding a targeted alias or by tightening the disambiguation (e.g. POV-house affinity).
- Mechanism: add to the **supplementary** `working/wiki/data/pass1-derived-firstname-aliases.json` or extend `scripts/stage4_name_resolver.py` — do NOT mutate `working/wiki/data/alias-resolver.json`. Re-run the two `--apply` scripts. **Spot-audit a random sample of any NEW resolution rung output before trusting it** — the green tests did NOT catch the two S66 misresolution bugs (generic role-words; title-first-token→ser-pounce). Keep the conservative posture: when in doubt, queue, don't guess.

### Track B — LLM tail (NEEDS MATT'S EXPLICIT OK — it's an extraction)
Type the untyped-but-resolved rows in `_tail/`. Per-item input = pair + `hint_raw` + the located evidence sentence (already attached); output = one locked-vocab edge type OR reject-as-untypeable. This is much smaller than the design's 3,638 estimate (resolution culled it; re-count from `_tail/` before launching).
- Model: **Sonnet 4.6**, batched ~50–100 rows/call. **Smoke ~50 first**, eyeball, then proceed.
- Conform inline: run every emitted type through the locked-vocab check (reuse the conform logic in `stage4-pass1-edge-candidates.py`) + `scripts/wiki-pass2-validate-edge-jsonl.py`. Stamp `typed_by: sonnet`, `evidence_kind: book-pass1`, same schema as the deterministic edges.
- Per the no-extraction-without-asking + drift-detection rules: confirm scope + cost with Matt, run via the normal pipeline (not background subagents), validate output schema before scaling.

### Track C — Deprecate-stamp wiki-comention (deterministic, design step 4)
Stamp the 130 done wiki chapter-summary comention files **in-data** (`status: superseded`, `superseded_by: pass1-derived`, `do_not_promote: true`) — NOT dir-archiving (provenance lives in data, not folder names). Find them under `working/wiki/pass2-buckets/*/prose-edges/` from the deprecated comention runs; a small Python stamper is the right tool.

### Track D — First-class book-pass1 validator schema (small, optional)
`scripts/wiki-pass2-validate-edge-jsonl.py` predates `book-pass1`; the S66 edges pass only because extra fields (`candidate_kind`, `evidence_book`, `confidence_tier`) were added to satisfy the existing `(emit_edge, pass1_relationship)` contract. Add a proper `evidence_kind: book-pass1` schema branch that validates `evidence_chapter`/`evidence_quote`/`evidence_ref`/`hint_raw`/`source_resolution_status` etc. directly.

## Open questions for Matt
- Track B (LLM tail) needs your explicit go + a cost ceiling before any run.
- Recovery (Track A) — how aggressive on multi-name cell-splitting and alias additions vs. staying conservative? (Wrong edges are worse than queued ones.)

## DO NOT
- Re-launch the wiki chapter-summary comention bulk (DEPRECATED).
- Mutate `working/wiki/data/alias-resolver.json` (use the supplementary firstname-alias map).
- Use Opus for per-item typing. Refetch wiki. Write `graph/nodes/`. Run the LLM tail without Matt's OK. Run `/endsession` without explicit permission.
- Trust green tests as proof of correctness on bulk resolution output — spot-audit random samples.
