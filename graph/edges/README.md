# graph/edges/ — Pass-1-derived edge set (v1)

**Landed:** Session 70, 2026-05-25. **Status:** v1 — the first traversable edge layer.

`edges.jsonl` is the formalized, deduped, endpoint-gated, precision-filtered set of
**3,842 typed relationship edges** derived from our own Pass 1 chapter extractions
(`extractions/mechanical/{book}/`). Every edge carries a verbatim source citation
(`evidence_ref` → `sources/chapters/<book>/<chapter>.md:<line>`), so a runtime LLM can
re-verify any edge against the surrounding chapter text.

## Provenance (how each edge was typed)

| `typed_by` | count | source |
|---|---|---|
| `python-map` | 1,982 | deterministic phrase→vocab map of Pass 1 "Relationships Observed" hints (the spine) |
| `sonnet` | 1,411 | S67 LLM tail — Sonnet typed the residual free-text hints |
| `hospitality-table` | 396 | deterministic Hospitality & Guest Right table (`GUEST_OF`) |
| `hospitality-table-violation` | 53 | deterministic Hospitality table (`VIOLATES_GUEST_RIGHT`) |

All edges: `evidence_kind: book-pass1` (primary-text source, not wiki).

## Build lineage

```
spine 2,834 emit + S67 tail 2,385 emit + Hospitality 529   = 5,748 merged
  → endpoint gate (is_low_quality_endpoint)        −109   (junk slugs: bare titles, all-for-joffrey toasts, aliases)
  → S67 tail-violation quarantine                  − 10   (HOLDS_TITLE→place ×6, ENCOUNTERS no-verb ×4)
  → dedup (source,edge_type,target,qualifier)      −1,543 (spine×tail overlap; kept verbatim>tier1>has-ref)
                                                   = 4,086
  → gated-type quarantine                          −234   (INFORMS/ADVISES/MANIPULATES/SUPPORTS/ALIAS_OF — pre-lockdown typing)
  → low-value quarantine                           − 10   (CONTEMPORARY_WITH person↔person)
                                                   = 3,842  ← edges.jsonl
```

Producers: `scripts/stage4-formalize-edges.py` (merge + gate + dedup + `--precision-filter`).
Quarantined rows are preserved (not deleted) in staging
`working/wiki/pass2-buckets/pass1-derived/_formalized/` (gitignored), queued for a future
locked-down re-typing pass.

## Quality — read before trusting blindly

- **Strict precision ≈ 78%** (head-to-head reviewer audit, 2026-05-25). The graph is for
  enrichment + runtime-LLM-verified traversal, not as untouchable ground truth.
- **Dominant residual issue: evidence-quote mis-location.** The *type and pair* are usually
  correct, but the locator sometimes attaches a nearby quote that doesn't itself prove the
  edge. Use `evidence_ref` (the chapter `file:line`) to read full context, not just
  `evidence_quote`.
- **`confidence_tier` is NOT calibrated in v1 — every edge is tier-1.** The core was typed
  before tier-assignment guidance existed. Do not read tier as a confidence signal yet;
  calibration arrives with the locked-down re-typing pass.
- Known error classes still present at a low rate: occasional direction reversals
  (`asha PRISONER_OF sybelle-glover` should be reversed), rumor-as-fact
  (`eddard LOVER_OF ashara-dayne`), resident-vs-guest (`rickon GUEST_OF winterfell`).

## Schema (one JSON object per line)

Key fields: `edge_type`, `source_slug`, `target_slug`, `qualifier` (where required),
`confidence_tier`, `evidence_kind`, `evidence_book`, `evidence_chapter`, `evidence_section`,
`evidence_quote`, `evidence_ref`, `hint_raw`, `asserted_relation`, `typed_by`,
`candidate_kind`, `source_set` (spine|tail|hospitality), `dup_count`, `run_id`,
`schema_version`, `produced_at`. Edge-type vocabulary + directionality: see
`reference/architecture.md`.

## Roadmap

- **v2 — enrichment:** Events + Dialogue tables typed by Haiku (locked-down prompt, Rule 11
  anti-pattern gates), precision-filtered, layered on top.
- **Re-typing:** the 234 quarantined gated-type edges + the direction/locator-suspect tail
  re-typed under the locked-down prompt for tier calibration.
- **Node-frontmatter integration:** surface these edges in `scripts/graph-query.py` and/or
  node files (currently they live only here as a consolidated JSONL).
