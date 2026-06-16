# Design Opinion: Event Dating — Canon Fidelity & Uncertainty Representation

**Lens:** Canon fidelity and uncertainty representation only. No opinion on graph traversal performance, storage formats, or query patterns.
**Date:** 2026-06-15
**Reviewer:** Claude (independent)

---

## Executive Summary

Matt's proposed `occurred` block is a solid skeleton but has three structural gaps that will produce pollution under real conditions: it cannot encode competing dates for the same event; it cannot distinguish "circa / fuzzy span" from "genuine duration"; and `basis` conflates provenance (where the date came from) with reliability (how much to trust that source). All three need explicit slots before any dates are written to nodes. Additionally, **relative ordering should be the PRIMARY representation for most of the corpus** — absolute AC years are a secondary annotation that should be added cautiously and only when the source clears a high bar.

---

## 1. Evaluating the Proposed Schema

### Matt's draft

```yaml
occurred:
  ac_year: 88
  ac_year_end: ~
  precision: exact|year|decade|century|era|relative-only
  basis: wiki-year-page|twoiaf|fan-timeline|inferred-prose
  confidence: tier-1..5
```

### What works

- **`precision`** is the most important field here and the enum is directionally right.
- **`confidence`** is consistent with the rest of the schema (tier-1..5 already means something to every agent in this project).
- **`basis`** naming the provenance source is good — it means a future script can mechanically downgrade or flag dates from less reliable sources.

### Gap 1: No slot for competing / disputed dates

Many events have two different dates depending on which source you trust. Robert's Rebellion start date is one of the sharpest examples: wiki year-pages put Lyanna's disappearance in 282 AC, but cross-checking with character ages and reignal years produces 281 AC or a straddle across both. The current schema has one `ac_year`. If you write 282, you silently discard the competing 281. A consumer agent will treat 282 as settled fact.

**What's missing:** a `dispute` sub-object that can hold an alternate year and its own basis + confidence, so the dispute is surfaced rather than resolved by fiat.

### Gap 2: `ac_year` + `ac_year_end` conflates two distinct things

A war that runs from 282 AC to 283 AC is a genuine span (two endpoints, both known). "Circa 88 AC, ±5 years" is uncertainty (one fuzzy point). These look the same in the current schema — both would be represented as `ac_year: 83` / `ac_year_end: 93`. A consumer agent cannot tell whether it is looking at "this event lasted ten years" or "we don't know within a ten-year window." That distinction is load-bearing: "the war lasted a decade" is a fact worth stating; "we're not sure of the decade" is a warning not to state anything.

**What's missing:** an `uncertainty_radius` (or `ac_year_low` / `ac_year_high`) for fuzzy single-point events, kept separate from `ac_year` / `ac_year_end` which should only be used for genuine start / end dates of durations.

### Gap 3: `basis` mixes provenance with reliability tier

`wiki-year-page` is a provenance label, but it doesn't capture the quality of that provenance. The wiki year-pages are fan-compiled and sometimes wrong — the chronology-events.jsonl index you already have demonstrates this: the index records mentions, not occurrences (a year-page mentioning a character does not mean the character was born or acted in that year). `twoiaf` is also fan-compiled (written by GRRM + GRRMsanctioned, but still contains in-universe myths as if they were history).

These need both a provenance label AND a reliability note. A two-level encoding works better:

- `basis_source` — where the date comes from: `narrative-prose`, `appendix`, `twoiaf`, `fire-and-blood`, `wiki-year-page`, `world-of-ice-and-fire-app`, `fan-timeline`, `inferred`
- `basis_reliability` — how much to trust that source for dates: `primary-source` (prose), `secondary-source` (appendix, twoiaf written as authoritative), `tertiary-fan` (wiki year-pages, fan timelines), `inferred-only`

`tertiary-fan` dates should automatically cap out at confidence tier-3 regardless of what the wiki confidently states.

---

## 2. Concrete Frontmatter: Encoding "Suspected 88 AC" vs. "Book 2 Ch 5"

### Case A — Hard narrative anchor (tier-1)

This is a chapter citation: the event occurs on the page. It is verifiable, not interpretive.

```yaml
occurred:
  anchor_type: narrative
  book: acok
  chapter: 58
  pov: davos-01
  notes: "Battle depicted in this chapter; no AC year stated in prose"
  ac_year: ~
  ac_year_precision: ~
  confidence: tier-1
  basis_source: narrative-prose
  basis_reliability: primary-source
```

Consumer agent reads `anchor_type: narrative` and may quote the chapter as the date. It may NOT infer or state an AC year — `ac_year` is null.

### Case B — Suspected year (tier-3 guess)

"Suspected 88 AC" from a wiki year-page mention.

```yaml
occurred:
  anchor_type: estimated-ac
  ac_year: 88
  ac_year_precision: year       # we're saying a specific year, not a decade
  uncertainty_radius: ~         # no explicit ± given; absence = ±0 within stated year
  confidence: tier-3
  basis_source: wiki-year-page
  basis_reliability: tertiary-fan
  inferred_from: "wiki:88_AC page mentions Maekar's accession; this event placed by proximity"
  dispute: ~
```

Consumer agent sees `confidence: tier-3` + `basis_reliability: tertiary-fan`. It must hedge: "possibly 88 AC" or "sources suggest 88 AC, unverified." It may not state "88 AC" as fact.

### Case C — Disputed date with two competing values

```yaml
occurred:
  anchor_type: estimated-ac
  ac_year: 282
  ac_year_precision: year
  confidence: tier-3
  basis_source: wiki-year-page
  basis_reliability: tertiary-fan
  inferred_from: "wiki:282_AC places Lyanna's disappearance and Robert's Rebellion start"
  dispute:
    ac_year: 281
    confidence: tier-3
    basis_source: inferred
    basis_reliability: inferred-only
    inferred_from: "Character ages at AGOT cross-reference implies 281 AC start; see fan-timeline discussion"
    notes: "GRRM acknowledged timeline inconsistencies in Robert's Rebellion dating"
```

Consumer agent sees `dispute` is populated and must flag the disagreement rather than choosing one value.

### Case D — Genuine span (a war with known start + end)

```yaml
occurred:
  anchor_type: span
  ac_year: 282
  ac_year_end: 283
  ac_year_precision: year       # both endpoints at year-level precision
  confidence: tier-2
  basis_source: twoiaf
  basis_reliability: secondary-source
  span_notes: "War lasted approximately one year; specific month/day unknown"
  dispute: ~
```

The `ac_year_end` here means "this event genuinely lasted until 283 AC." It is not fuzzy; it is a duration.

### Case E — Fuzzy single-point (circa, no exact year known)

```yaml
occurred:
  anchor_type: estimated-ac
  ac_year: 8000        # conventional number used in-world; explicitly mythologized
  ac_year_precision: era
  uncertainty_radius: 2000     # ±2000 years; scholarly range within in-world tradition
  confidence: tier-4
  basis_source: twoiaf
  basis_reliability: secondary-source
  inferred_from: "TWOIAF states 'approximately eight thousand years ago'; maester-tradition claim, not independent verification"
  notes: "In-world accounts of Long Night date are explicitly mythologized; GRRM has not committed to a specific number"
  dispute: ~
```

### Case F — Relative-only (no AC year possible)

```yaml
occurred:
  anchor_type: relative
  ac_year: ~
  ac_year_precision: relative-only
  relative_to: "robert-i-baratheon-death"
  relative_position: before
  relative_offset_notes: "Several months before Robert's death, during the same journey south from Winterfell"
  confidence: tier-1
  basis_source: narrative-prose
  basis_reliability: primary-source
```

---

## 3. Where Absolute AC Years Become Unsafe to Mint

Draw a hard line here. The following categories of event should remain `relative-only` or `anchor_type: narrative` indefinitely. Minting an AC year for them creates pollution with no offsetting benefit.

### 3a. Deep-history / mythological events (NEVER mint AC year)

These include: Long Night, Age of Heroes, Pact of the Isle of Faces, Andal Invasion (broad sweep), building of the Wall, War for the Dawn. The in-world dates for these are explicitly transmitted through maester tradition, which the books treat as imperfect oral history. GRRM has given different figures in different interviews. The wiki year-pages for these events often list BCE/BC-equivalent estimates that carry four-figure uncertainty. Minting `ac_year: -8000` treats a mythological tradition as a measurement.

**Policy:** Deep-history events get `anchor_type: mythological`, `ac_year_precision: era`, and a mandatory note that the figure is in-universe tradition, not independently verifiable.

### 3b. Events datable only by inference from character ages

This is the single largest source of wiki fan-timeline error. The ASOIAF wiki's year-page dates frequently rest on the chain: "Joffrey is 13 at AGOT start → AGOT starts 298 AC → therefore Joffrey was born 285 AC." But GRRM has stated character ages are not internally consistent across the series. Any date derived from this chain is `basis_reliability: inferred-only` and caps at tier-3.

**Policy:** No `confidence: tier-1` or `tier-2` for any date that rests solely on character-age arithmetic. Must cite a prose statement ("in the year of the false spring") or appendix year to get tier-2.

### 3c. "Possibly" events from wiki year-pages

The chronology-events.jsonl already shows the wiki explicitly flagging some events with "(Possibly)": "Gregor Clegane is knighted by Rhaegar Targaryen. Gregor has two possible years in which he was knighted: 281 AC or 282 AC." The wiki is doing the honest thing by writing "Possibly" — the graph must preserve that hedge, not collapse it.

**Policy:** Any wiki year-page entry marked "(Possibly)" or "(Likely)" must translate to `confidence: tier-3` maximum, with a `dispute` block if two years are given.

### 3d. Events from Dunk & Egg novellas dated by fan extrapolation

The D&E timeline is primarily known from internal relative references (Dunk is X years old by Egg's ascension, etc.). Fan timelines have worked this backward to AC years but GRRM has not published a canonical D&E date table. These dates are `basis_reliability: tertiary-fan`.

### 3e. Events whose only source is the chronology-events.jsonl mention index

A year-page mentioning an entity does NOT mean that entity's defining event occurred in that year. The existing `chronology-events.jsonl` is a mention index, not an occurrence index. **No date should be minted solely from this index.** The index is a research lead, not evidence.

---

## 4. Position: Relative Ordering Is Safer as the Primary Representation

**Yes, unambiguously.** For most of the corpus, PRECEDES / FOLLOWS (narrative sequence edges) should be the primary temporal representation, with absolute AC years as a secondary optional annotation minted only where the evidentiary bar is cleared.

### The case for relative ordering as primary

**It is derived from verifiable sources.** Narrative sequence is observable from chapter order and POV structure — both of which are already encoded in the graph as `meta.chapter` nodes. AGOT Ch. 1 precedes AGOT Ch. 2. No interpretation required.

**It is what the graph actually needs for agent traversal.** The stated real project goal is graph quality for agents answering questions like "what events preceded Ned's execution that made it possible?" or "what did Robb do between the Red Wedding foreshadowing events?" Those questions need ordering, not years.

**It is stable.** Fan timelines get revised when GRRM releases new material or issues a correction. A PRECEDES edge between two event nodes is never invalidated by GRRM saying "I got the years wrong in Robert's Rebellion."

**AC years are not stable even within canon.** GRRM has explicitly acknowledged timeline errors. App dates contradict prose. TWOIAF dates contradict AGOT appendix dates for the same events. The wiki year-pages reflect which of these sources the fan community trusted most at the time of writing, which is a social fact, not a canon fact.

### When absolute AC years ARE worth minting

Mint an AC year only when at least one of these is true:
1. Prose explicitly states a year ("in the year 298 after Aegon's Conquest")
2. An appendix states a year AND no other source contradicts it
3. TWOIAF or Fire and Blood states a year for pre-conquest history AND that figure is consistent across the text (no internal contradictions)

In practice, this means most in-series events (298-300 AC range) get AC years because appendices and chapter dates are relatively consistent. Most pre-Conquest historical events stay relative-only or get decade/century-precision with high `uncertainty_radius`. Everything before ~100 BC stays `anchor_type: mythological`.

### The relative-ordering edge types to use

The schema already has narrative-position for chapter citations. For event-to-event temporal ordering, add:

```
PRECEDES (event → event)  — A happened before B, derivable from narrative
FOLLOWS (event → event)   — inverse, emit on the later node
CONCURRENT_WITH (symmetric) — events overlapping in time, same narrative window
CAUSED (event → event)    — causal succession, stronger claim than mere temporal order
```

These are tier-1 when derived from chapter sequence. They degrade gracefully: a consumer agent that doesn't have AC years can still answer ordering questions.

---

## Final Three-Sentence Recommendation

**Adopt relative ordering (PRECEDES / FOLLOWS) as the primary temporal representation for all events, with `anchor_type: narrative` chapter citations as the evidentiary backbone.** Mint AC years only when prose or appendix explicitly states a year, encode all such dates in the full `occurred` block with `basis_source`, `basis_reliability`, `uncertainty_radius`, and a populated `dispute` sub-object whenever two competing dates exist in the literature. For deep-history (pre-Conquest), mythological events, and any date derived solely from fan timelines or the `chronology-events.jsonl` mention index, leave `ac_year` null and mark `anchor_type: relative` or `anchor_type: mythological` — a consumer agent reading a null AC year is correctly informed that no date is known, which is far less harmful than a fabricated precision that reads as fact.
