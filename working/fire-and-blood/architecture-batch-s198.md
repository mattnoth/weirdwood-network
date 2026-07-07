# architecture.md change batch — Fire & Blood (staged S198)

> **GATED.** This is the ONE architecture.md change-batch for the F&B track (design ruling #6 / §10.3). It lands
> **WITH the first F&B apply**, NOT at build time, and needs Matt's go. When it lands, log ONE Active Decision in
> `worklog.md`. S197 already landed the `disambiguation_hub`/`redirect_to` slice — this is the remainder.
> Four edits + one mint patch + the validator invariant. Nothing here is applied yet.

## Edit 1 — File Naming (architecture.md ~line 15–17): add the `fab` book code
After the existing book/novella codes, add:

> Fire & Blood: `fab`. **Not POV-structured** (third-person maester-historian narration by Gyldayn) — so F&B
> chapter files are named by SECTION, not POV: `fab-<section-slug>-NN[-pMM].md` where `NN` = the epub HTML file
> number (zero-padded 2-digit) and `-pMM` is an optional sub-split part. Split by `scripts/fire-and-blood-splitter.py`
> per `working/fire-and-blood/unit-map.json` (the epub `toc.ncx` is unreliable). 23 sections → 39 unit files.

## Edit 2 — cite_ref format (architecture.md ~line 610): F&B anchor form
Add a note beside the `R{book_abbrev}{chapter_number}` format:

> Fire & Blood cite anchors are section-slug-based, not chapter-number-based: `Rfab<section_slug>` (e.g.
> `cite_ref-Rfabheirs_of_the_dragon_-_a_question_of_succession`). This is the wiki's own F&B citation prefix —
> the graph's existing 1,634 `Rfab*`-anchored nodes are the Tier-2 provenance layer this pass upgrades. Book-cited
> F&B edges use `evidence_ref: sources/chapters/fab/<unit>.md:LINE` (line-anchored, like all other chapters).

## Edit 3 — evidence_kind: add `book-fab`
Wherever the evidence_kind discriminator values are enumerated (edge provenance; `mint_enrichment.py` DEFAULTS +
the prose-edge-classifier's `wiki-entity`/`wiki-chapter-summary`/`book-pass1` set), add:

> `book-fab` — an edge (or node-prose cite) grounded in *Fire & Blood* book text via the enrichment pass. Tier-1
> when Gyldayn narrates it flatly; Tier-2 + `in_universe_source`/`disputed` when hedged/partisan (see below).
> Distinguishes the maester-historian layer so queries can filter book-vs-wiki provenance.

## Edit 4 — Edge Metadata table (architecture.md ~line 546): two optional fields + invariant
Add two rows to the Edge Metadata table:

| Field | Purpose | Example |
|-------|---------|---------|
| `in_universe_source` | Optional; F&B (`book-fab`) edges only. The in-world source of a hedged/partisan claim. Enum: `mushroom \| eustace \| munkun \| orwyle \| gyldayn-synthesis \| court-record \| unattributed`. Set ONLY when the text hedges or names a partisan source; blank on plain Gyldayn narration. `unattributed` = bare "some say / it is said"; `gyldayn-synthesis` = Gyldayn explicitly weighing named sources. | `mushroom` |
| `disputed` | Optional bool; F&B edges only. `true` when the claim is hedged, single-partisan, or two accounts conflict (each conflicting account emitted as its own edge, each tagged). | `true` |

**Validator invariant (new):** `disputed: true ⇒ confidence_tier ≤ 2` — reject any tier-1 + disputed row. Same
tier-cap pattern as `SUSPECTED_OF` (architecture.md:413) and the staged `occurred.dispute` sub-map (:506).
Rationale: F&B is in-universe history compiled by Archmaester Gyldayn from partisan, contradictory sources
(Munkun's *True Telling*, Orwyle, Septon Eustace, Mushroom's *Testimony*); uncontested narration is the primary
canonical source for 1–136 AC (Tier-1, no POV text exists for that era), but anything hedged/disputed is capped
Tier-2. Blanket per-source ceilings were rejected (Fable review §3 #9) — Gyldayn synthesizes, and even Mushroom
sometimes reports uncontested fact.

## Mint patch (3 lines — `scripts/mint_enrichment.py`, `make_edge_row`)
So book-fab edges carry the two new fields (currently dropped):
```python
    if e.get("in_universe_source"):
        row["in_universe_source"] = e["in_universe_source"]
    if e.get("disputed"):
        row["disputed"] = True
```
(Insert beside the existing `qualifier`/`verify` passthroughs.) The reconciler already writes these into
candidates.json; without this patch mint silently omits them. Land it in the same commit as edits 1–4.

## Worklog Active Decision (log when this lands)
> **F&B schema batch (S198→apply):** added `fab` book code (section-named chapter files), `evidence_kind:
> book-fab`, edge fields `in_universe_source` (enum) + `disputed` (bool), validator invariant `disputed ⇒
> tier ≤ 2`, and the 3-line mint passthrough. One batch, per CLAUDE.md rule #6 (schema ↔ architecture.md lockstep).
