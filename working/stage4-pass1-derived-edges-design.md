# Stage 4 — Pass-1-Derived Deterministic Edge Pipeline (Design)

> **Status:** Direction DECIDED + endorsed by Matt, 2026-05-22 (Session 65). Build not started.
> **Recommended build model:** Sonnet 4.6 for the Python (parser/locator/typer-map); Haiku only for the novel-hint tail; Opus 4.7 for periodic validation / schema-drift / weird-result review.

## The breakthrough in one line

**Stop making the LLM *find* relationships in prose. Use the relationships we already extracted.** Our Pass 1 extractions already contain a `## Relationships Observed` table (pair + evidence) per chapter — plus Dialogue / Food & Drink / Information Revealed tables. Python does the mechanical work; the LLM only *labels* the residual free-text hint with a locked-vocab edge type.

## Why this beats the wiki-comention path

| Axis | Wiki chapter-summary comention | **Pass-1-derived (this)** |
|---|---|---|
| Source | secondary (a fan's wiki summary) | **primary (GRRM's text, via our extractions)** |
| LLM job | *hunt* relationships in prose | *map* a known hint → vocab type |
| Volume/cost | 29,259 candidates (biggest Stage-4 sink) | mostly deterministic; tiny LLM tail |
| Failure modes | 5% violations, ENCOUNTERS fails, KNOWS sprawl, type-invention | removed — LLM no longer hunts |
| Citation | wiki summary snippet | **chapter + verbatim quote + `file:line`** |
| API usage | heavy bulk runs, rate-limit walls | collapses to the novel-hint tail |

## Pipeline (4 stages)

1. **PARSER** (Python, deterministic) — read each extraction's relational tables → emit candidates `{source, target, hint, evidence_text, chapter_id, section}`. Primary: `## Relationships Observed`. Also mine: `Dialogue of Note` (who→whom), `Food & Drink` (shared meals), `Information Revealed` (source→target), `Events & Actions`.
2. **LOCATOR** (Python, deterministic) — match the (often paraphrased) evidence + pair against the actual chapter file → return **verbatim quote + `file:line`**. Upgrades citation from chapter-level → exact passage. Dialogue rows match easily (near-verbatim); Relationships rows are paraphrased and lean on the locator.
3. **TYPER** — map `hint` → locked-vocab edge type. **Deterministic phrase→vocab map** for the common cases ("Mourning"→MOURNS, "Antagonized by"→OPPOSES, "Gave X to"→GIFTED); **Haiku only for the novel/ambiguous tail**. Haiku's input is one tiny candidate (pair + hint + snippet) — never the chapter or full extraction.
4. **CONFORM** (Python, inline on write) — normalize edge-type names + validate against vocab + log unresolved. Runs per-batch, not as a deferred cleanup.

## Edge schema (book-derived)

```
source_slug, target_slug, edge_type (locked vocab), qualifier
evidence_kind: book-pass1
evidence_chapter: acok-arya-01            # -> sources/chapters/acok-arya-01.md
evidence_section: "Relationships Observed"
evidence_quote: "<verbatim, from locator>"
evidence_ref: sources/chapters/acok-arya-01.md:NNN   # jump-to-source for the graph AND for us while building
hint_raw: "deep love and longing for"     # provenance/debug
typed_by: python-map | haiku
run_id / schema_version / produced_at      # provenance stamp (self-describing artifact)
```

## Worked example (real, acok-arya-01)

Relationships Observed row:
`Arya | "Deep love and longing for" | Jon Snow | "dreams of him calling her 'little sister'"`
→ candidate → typer maps hint → **edge**:
`arya-stark —LOVES(familial)→ jon-snow` with `evidence_kind: book-pass1`, `evidence_chapter: acok-arya-01`, `evidence_section: Relationships Observed`, `evidence_quote` + `evidence_ref` from the locator.

## Orchestration / fleet (Matt's idea)

- Most stages are deterministic Python → fast, cheap, **no rate-limit risk**.
- A periodic **Opus 4.7 session** for: validation, schema-drift fixes, script refinement, weird-result review, hint-map curation. Not per-batch.
- Could become a fleet-orchestrated start-to-finish process with timers — **but** the usage profile is now tiny (deterministic bulk + small Haiku tail), so the heavy `run-forever` / sleep-tuning / rate-limit apparatus is mostly unnecessary. Matt: *"we may not even need usage like we have been needing."*

## What this changes about prior plans

- **Wiki chapter-summary comention: DEPRECATED.** Stop producing it (~214 remaining chapters cancelled). The 130 already-done files → **stamp in-data** `status: superseded`, `superseded_by: pass1-derived`, `do_not_promote: true`. **NOT dir-archiving** — archiving has been contention-prone because "archived" lives in folder names a fresh session can misread; provenance must live in the data.
- **The bulk-LLM apparatus** (run-forever, sleep tuning, concurrency=4, rate-limit walls) drops to low priority — it existed to manage heavy LLM usage we no longer have.

## Prerequisites / carry-overs from Session 65 findings

- **24 skipped files** (dual-run gap: Frey/Hightower/Tarly, randyll-tarly @177 rows) — likely just regenerate via this pipeline rather than re-run the wiki path.
- **run-summary.json overwrite bug** + **single-instance guard** + **provenance stamp** — still relevant to any LLM step.
- **Comention output drift** (pair_a/pair_b in ~15% of rows) — moot once comention is deprecated, but the conform-on-write step covers the class.

## Open design questions

- How far to mine beyond `Relationships Observed`? Start there, measure recall, expand to Dialogue/Food/Info/Events.
- Locator matching strategy (fuzzy on names+keywords); fallback when no verbatim match (paraphrase + chapter-level cite only).
- Phrase→vocab map coverage: seed from observed hints across all 344 extractions; **measure what % types deterministically** (drives how small the Haiku tail is).
