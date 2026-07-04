# graph/edges/ — Pass-1-derived edge set (v1.3 baseline, since grown by later merges)

**Landed:** Session 70 (v1, 3,842). **Refined:** Session 72 (v1.2, 3,825 — type-contract
re-validation). **Resolver pass:** Session 72 (v1.3, 3,811 — title-person disambiguation).
**Status:** v1.3 lineage below is frozen history — `edges.jsonl` has since grown past it via
later sessions (the wiki-infobox merge, Plates 3–5 event reification, chronology-chain,
hospitality, curator passes, etc.) that are NOT narrated in this file. **Current line count:
run `wc -l graph/edges/edges.jsonl` for the live number** (23,099 as of query-layer Track step
9, 2026-07-04) — do not trust the 3,811 figure below as current; it documents the v1.3
milestone only.

`edges.jsonl` is the formalized, deduped, endpoint-gated, precision-filtered edge set
derived from our own Pass 1 chapter extractions (`extractions/mechanical/{book}/`), since
layered with additional typed-edge production (wiki-infobox merge, event reification, etc. —
see git history for `graph/edges/edges.jsonl` for what landed after v1.3). Every edge carries
a verbatim source citation (`evidence_ref` / `evidence_kind`), so a runtime LLM can re-verify
any edge against the surrounding chapter or wiki text.

## Provenance (how each edge was typed)

| `typed_by` | count | source |
|---|---|---|
| `python-map` | 1,964 | deterministic phrase→vocab map of Pass 1 "Relationships Observed" hints (the spine) |
| `sonnet` | 1,401 | S67 LLM tail — Sonnet typed the residual free-text hints |
| `hospitality-table` | 396 | deterministic Hospitality & Guest Right table (`GUEST_OF`) |
| `hospitality-table-violation` | 50 | deterministic Hospitality table (`VIOLATES_GUEST_RIGHT`) |

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

### v1.2 refinement (Session 72, 2026-05-25)

```
v1 3,842
  → type-contract re-validation (fixed validator + slug_category_index)   −17   = 3,825
       drops: 13 COMMANDS with non-commandable targets (artifact/place/title/species/text/
                 concept — e.g. gregor→lord-tywin[a ship], victarion→iron-throne)
            + 1 MOTIVATES (character source) + 3 VIOLATES_GUEST_RIGHT
       retypes: 3 RULES→COMMANDS (character target)
       KEPT: 16 COMMANDS→faction unit-command edges that the old char-only contract
             would have false-dropped (gunthor→stone-crows, victarion→iron-fleet,
             beric→brotherhood-without-banners, ben-plumm→second-sons, jon→nights-watch, …)
```

Producer: `scripts/stage4-refine-v1-edges.py` (now passes `slug_category_index`, so the
category-based contracts — COMMANDS-unit / CONTRACTED_WITH / MEMBER_OF-flip / HOLDS_TITLE-place
— actually fire). The annotated candidate (with quote-relevance `_qr_warning` soft-flags on
1,944 rows) lives in `working/wiki/pass2-buckets/pass1-derived/_v1-refine/` (gitignored); the
committed layer here keeps the clean schema (advisory `_`-fields stripped).

### v1.3 resolver pass — title-person disambiguation (Session 72, 2026-05-26)

```
v1.2 3,825
  → remap 6 title-person collision slugs → their characters   = 3,813 (−12 dups)
       lord-tywin→tywin-lannister, queen-cersei→cersei-lannister, lord-renly→renly-baratheon,
       princess-myrcella→myrcella-baratheon, lady-olenna→olenna-tyrell, khal-jhaqo→jhaqo
  → CAPTAIN_OF target-not-character drop                       = 3,811 (−2)
       hallis-mollen / areo-hotah "CAPTAIN_OF" a person (mis-typed "captain of the guard")
```

These were ships/artifacts/titles *named after* people (`lord-tywin` = Cersei's dromond) that
captured person references via exact slug match. The resolver now prefers the character when a
title-prefixed name exact-matches a non-character node (`scripts/stage4_name_resolver.py`,
`resolved-title-person` rung, threaded through `stage4-pass1-edge-candidates.py`). The ship
`lady-marya` (Davos's vessel, `CAPTAIN_OF`) is deliberately **kept** as the artifact; the new
`CAPTAIN_OF`/`CREW_OF` target-not-character contract backstops the ship-name class on re-runs.

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
