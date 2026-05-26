# Stage 4 Pass-1-derived — Staging Layer Manifest

**Purpose:** The staging tree `working/wiki/pass2-buckets/pass1-derived/` is **gitignored and
regenerable**. It holds many run-layers from many sessions. This manifest says which layers are
**CURRENT**, which are **SUPERSEDED** (kept for provenance — never deleted), and which are
**PROPOSALS** awaiting a decision — so an archived run is never mistaken for a current layer.

**Last updated:** 2026-05-25 (Session 71, autonomous). **Rule:** nothing here is deleted; superseded
runs are labeled, not removed. The ONE committed ground-truth layer is `graph/edges/edges.jsonl`.

---

## The only committed edge layer (ground truth)

| Path | Rows | Status |
|---|---|---|
| `graph/edges/edges.jsonl` (+ `README.md`) | 3,842 | **CURRENT — committed v1.** Everything below is gitignored scratch that feeds or tests this. |

---

## CURRENT — v1 lineage (gitignored, regenerable; produced the committed layer)

| Path | Rows | Role |
|---|---|---|
| `{agot,acok,asos,affc,adwd}/*.edges.jsonl` | 2,834 | Deterministic **spine** (Pass-1 "Relationships Observed" → typed edges). `*.candidates.jsonl` alongside = pre-type candidates. |
| `_tail/` | — | Untyped-but-resolved residual rows (spine leftovers) → input to the LLM tail. |
| `_tail-typed/` | 2,385 | **S67 Sonnet LLM tail** (`typed_by: sonnet`). Canonical tail. **DO NOT overwrite** — smoke runs must use `--output-dir` to a scratch dir. |
| `_needs-qualifier/`, `_tail-needs-qualifier/` | — | Qualifier-pending rows (Tier-1 types needing a qualifier). |
| `_formalized/` | — | **S70 formalize build artifacts:** `edges.jsonl`/`edges-v1.jsonl` (final), `quarantine-*.jsonl`, `dropped-endpoints.jsonl`, `tail-violations.jsonl`, `*-report.md`. This is where spine+tail+hospitality merged → the 3,842 committed. |

Lineage: spine 2,834 + tail 2,385 + hospitality 529 → formalize (gate/dedup/precision-filter) → **3,842**.

---

## CURRENT — enrichment candidate pool (gitignored)

| Path | Role |
|---|---|
| `_extra-tables/{book}/*.extra-tables.jsonl` | The recall-expansion candidates: `candidate_kind` ∈ `pass1_events` (16,572) / `pass1_dialogue` (4,422) / `pass1_info` (5,162) / `pass1_food` (620). 100% carry `evidence_ref`. This is the enrichment input pool. |
| `_extra-tables-escalated/` | Escalated extra-tables rows (flagged during candidate generation). |

---

## CURRENT — active enrichment-decision work (Session 71, 2026-05-25)

| Path | Role |
|---|---|
| `_fresh-relocate-4242/` | **Fresh 400-row stratified sample** (seed 4242, Events+Dialogue), re-located with **locator v2** (both-named window preference). 2.2% overlap with the old sample. Input to smoke5. |
| `_smoke5-haiku/` | **Patched-pipeline re-smoke** (locator v2 + prompt overhaul GATE1/2/3 + 13 gated types + evidence-grounding). The current measurement of whether enrichment clears the bar. |

Scripts backing this session: `stage4-quote-relevance-filter.py`, `stage4-type-contract-validator.py`
(now w/ COMMANDS/MOTIVATES/empty-quote contracts), improved `stage4-pass1-evidence-locator.py`
(locator v2 + `locate_quality`), `stage4-fresh-relocate-sample.py`, `stage4-refine-v1-edges.py`.

---

## PROPOSAL — pending Matt's OK (Session 71; NOT applied to the committed layer)

| Path | Role |
|---|---|
| `_v1-refine/edges-v1.1-candidate.jsonl` | **v1.1 candidate:** v1 minus 10 type-contract schema-errors (quarantined in `v1.1-type-contract-dropped.jsonl`, ~5 re-typable later) + 1,950 `_qr_warning` soft-flags. `graph/edges/edges.jsonl` is UNCHANGED until approved. Report: `working/wiki/data/pass1-derived-v1-refine-proposal.md`. |
| `_quote-filter-dryrun/` | Read-only QR-filter dry-run over v1 (kept/dropped). Analysis only. |

---

## SUPERSEDED — historical smokes (KEPT for provenance; NOT inputs to anything current)

> These are prior measurements. Do not read them as current quality. None feeds the committed layer.

| Path | What it was | Result |
|---|---|---|
| `_smoke-dialogue/`, `_smoke-events-info/` | S69 Sonnet table-mining smokes | ~60-66% strict, verdict SYSTEMATIC |
| `_smoke2-haiku/`, `_smoke2-sonnet/` | S70 post-lockdown head-to-head (same 200 rows) | Haiku 76% / Sonnet 78% |
| `_smoke3-haiku/` | S70 Rule-11-patched Haiku | ~70% (failed ≥80% gate) |
| `_relocate-smoke/` | S71 relocated smoke3 200 rows (locator v2) → smoke4 input | — |
| `_smoke4-haiku/` | S71 locator+gate smoke (pre-prompt-overhaul) | 60% — superseded by smoke5 |

Reviews/reports for the above live in tracked `working/wiki/data/pass1-derived-*` +
`prompt-review-opus-{1,2}.md`. Smoke logs: `working/wiki/data/smoke2-logs/`.
