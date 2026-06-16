# Events & Time — Panel Synthesis (2026-06-15)

> For Matt's review. Consolidates a temporal mini-probe + a 4-lens opinion panel on
> whether/how to give event nodes time. No graph changes made; all inputs are read-only.
> Sources: `working/session-results/2026-06-15-temporal-mini-probe.md` +
> `working/design-opinions/2026-06-15-events-time-L{1,2,3,4}-*.md`.

---

## The empirical finding (mini-probe) — the graph fails time, and the data to fix it is on disk

5 in-world temporal questions, consumer-agent grading: **0 correct / 1 partial / 4 failed.**

| Q | Result |
|---|--------|
| What year was the Battle of the Trident? | FAILED — node exists, no year field |
| Sack of KL vs. Trident — which first? | FAILED — both nodes exist, no dates / no ordering edges |
| What was contemporaneous with the WO5K? | PARTIAL — 69 PART_OF members, but none dated |
| What happened in 283 AC? | FAILED — no year→event index |
| Harrenhal tourney → Robert's Rebellion gap? | FAILED — neither node dated |

- **Zero of ~585 event nodes carry any date field today.** The event layer is entirely undated.
- **`chronology-events.jsonl` already holds the answers** — Trident=283 AC, Harrenhal=281 AC verified; 158 event-typed rows. Moderate noise (it's a *mention* index), but the year assignments tested were reliable and corroborate wiki infoboxes.

**So the original dip's "time isn't the bottleneck" no longer fully holds** — the dip never *tested* time. When you test it, it fails 4/5. The gap is real; it just wasn't in the original 10 questions.

---

## Where the panel CONVERGED (high confidence)

1. **Two separate fields, not one.** In-world date (story-world) and narrative reading-position (where the reader meets it) are orthogonal and *diverge maximally for historical events* — the Trident happened 283 AC but is narrated as backstory across all of Book 1. Merging them breaks half of query types. (L1, L3, L4 all explicit.)
2. **Time lives in node frontmatter; ordering edges derive from it.** Add an `occurred:` block to event nodes. Do **NOT** mint `OCCURRED_IN_YEAR` edges (no year-nodes to attach to → dangling scalars). DO auto-generate `PRECEDES`/`FOLLOWS` from dated nodes via Python. (L4 explicit, L3 agrees.)
3. **Relative ordering is the safe primary; absolute AC dates are the risky, gated layer.** PRECEDES/FOLLOWS from chapter sequence are tier-1 and need no interpretation. AC years are contested even within canon (GRRM's acknowledged errors; app vs. prose vs. TWOIAF). (L3 strong, L4 + L1 agree.)
4. **Uncertainty must be STRUCTURED, not stringly.** "suspected 88 AC" must be typed fields an agent can't strip, never a string like "~88 AC" (agents drop text qualifiers when reformulating). This is the project's anti-pollution value applied to time. (L1 enum, L3 full model.)
5. **Chronology ≠ causation.** Dating does NOT fill the dip's causal-edge gap — it *complements* it. Dating makes `PRECEDES` free but never substitutes for `TRIGGERS` (Trident precedes the Sack by date; it *caused* it for reasons no date encodes). (L1, L4 explicit.)
6. **The job is small.** Narrative axis ≈ **95% free** (edges already carry `temporal_key` like `b1-c008`; ~40-line join). In-world AC dates ≈ **44% deterministic** ($0): year-page `<li>` links (122 events) + event infobox Date cell (99) + prose-year regex (39), with a **~31-event LLM tail (~$1)**, ~219 micro-events correctly undated (their anchor *is* narrative position), ~30 genuinely undatable. (L2, file-inspected.)

---

## Where the panel DISAGREED — the one real decision: SEQUENCING

| Lens | Position |
|------|----------|
| **L1 (query utility)** | Fix the **causal-edge gap FIRST** — it's what the dips actually measured (Q10/Q9/Q7). Dates rank #3–4, "not the bottleneck." |
| **L4 (graph modeling)** | **Date events FIRST** — cheapest transform, unblocks free PRECEDES + downstream; then ATTENDS, then TRIGGERS, arcs last. |
| **L2 / probe** | Dates are cheap + foundational → do now. |
| **L3 (canon)** | Order-agnostic; insists relative-ordering is primary whenever dates land. |

**Reading the disagreement:** it's "fix the measured failure (causal)" vs. "lay the cheap substrate (time) that makes the causal pass cheaper." The cost asymmetry largely dissolves it — dating first makes the TRIGGERS pass cheaper (sequencing already done), so they're complementary, not competing. L1's caution is right that *causation* is the higher-value reasoning layer; L4 is right that *time* is the cheap thing that should exist underneath it.

---

## Recommended sequence (synthesis)

1. **Narrative-position backfill** — ~$0, ~95% coverage, ~40 lines of Python. Bank it: nearly free, serves the deferred spoiler-gating need, near-zero risk. `occurred.narrative_first: "{book}-{chapter_number}"` on each event = min reader-encounter across its edges.
2. **In-world date first pass** — ~$0 deterministic (~44%) + auto-derived `PRECEDES`/`FOLLOWS`. Cheap, gives ordering for free, converts several probe partials. **Hard-gate the AC dates with the L3 uncertainty schema** (below). Defer the ~$1 LLM tail until the deterministic pass proves out.
3. **Causal `TRIGGERS`/consequence edges + `ATTENDS`** — the dip-MEASURED gap. Now cheaper: sequencing is done, participant context is richer. Start with the Robert's Rebellion chain (Harrenhal → crowning → abduction → rebellion → Trident → Sack → Tower of Joy).
4. **Narrative-arc reification** — last, as both dips concluded. The pattern works (Red Wedding); it's not where failures are.

Net: dating is steps 1–2 (cheap, now), the causal track L1 wants is step 3 (cheaper *because* of 1–2). Nobody on the panel is wrong; the order that satisfies all four is time-substrate-then-causation.

---

## Recommended schema (merged best-of)

```yaml
occurred:
  # AXIS A — in-world (story-world). GATED. null is a valid, honest answer.
  ac_year: 283            # signed int; negative = BC. null if unknown.
  ac_year_end: null       # genuine SPAN only (a war), NOT uncertainty
  uncertainty_radius: null # ± years for a fuzzy single point (keep separate from ac_year_end)
  precision: year         # exact | year | decade | century | era | relative-only
  basis_source: wiki-year-page   # narrative-prose | appendix | twoiaf | wiki-year-page | inferred
  basis_reliability: tertiary-fan # primary-source | secondary-source | tertiary-fan | inferred-only
  date_confidence: tier-3 # tertiary-fan auto-caps at tier-3
  dispute:                # populated ONLY when ≥2 competing canon dates exist
    ac_year: 281
    basis_reliability: inferred-only
    notes: "GRRM-acknowledged Robert's Rebellion inconsistency"
  # AXIS B — narrative reading-position (where the READER meets it). tier-1, ~free.
  narrative_first: "agot-3"   # {book}-{chapter_number}, min across the event's edges
```

**"suspected 88 AC"** → `ac_year: 88, precision: year, date_confidence: tier-3, basis_reliability: tertiary-fan` → a consumer agent reading tier-3/tertiary-fan must hedge ("possibly 88 AC"), never assert.

**Never mint an AC year for** (leave null / relative-only): deep-history & mythological events (Long Night, Age of Heroes), anything dated only by character-age inference (ages are canonically inconsistent), "possibly X or Y" wiki entries (preserve the hedge), D&E fan-extrapolated dates, and anything resting on the `chronology-events.jsonl` *mention* index alone (a mention ≠ an occurrence). (L3.)

---

## Cheap side-finding worth banking (L2)

The infobox parser **never captured the wiki `Date` table cell** — `infobox-data.jsonl` has **zero** date fields despite 232 event rows, even though the raw HTML in `sources/wiki/_raw/` contains it (verified on `Battle_of_the_Trident.json`). A small parser fix recovers ~99 event dates deterministically. Fold into step 2.

---

## Open questions for Matt
1. **Sequence:** accept time-substrate-first (steps 1–2) then causal (step 3)? Or do you want the causal-edge track first per L1?
2. **AC-date scope:** date *all* datable events, or L1's narrower "pre-series historical events only" (where dates matter most and in-series chapter-anchoring already gives ordering)?
3. **Schema:** adopt the merged `occurred:` block above (two axes + `dispute`/`uncertainty_radius`/`basis_reliability` split), or your leaner original sketch?
4. Want this recorded into `worklog.md` + `working/todos.md` as a track? (I won't `/endsession` without your go-ahead.)
