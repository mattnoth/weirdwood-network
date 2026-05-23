# Session 66 — Stage 4 Pass-1-derived edge spine: built, resolution-wall broken, two bugs hunted (2026-05-23)

**Model:** Opus 4.7 (orchestrator) + script-builder ×3 on Sonnet 4.6 (the builds).
**Purpose:** Execute the `stage4-pass1-derived-edges` continue track — build the deterministic spine that turns our own Pass 1 `## Relationships Observed` tables into typed, citation-bearing graph edges at zero LLM cost.

---

## Outcome in one line

The deterministic spine is built, tested (278 green), validator-clean, conform-clean, and committed (`047e49b3b`). It emits **2,818 typed, ~99%-cited `book-pass1` edges**. The headline finding: **resolution, not typing, was always the wall** — and breaking it (alias enrichment + collision-aware disambiguation) is what carried the yield from 1,035 → 2,818.

---

## What was built

Three scripts (all reuse the proven parser/slug/alias helpers from the older `wiki-pass2-build-pass1-relationship-candidates.py` + the typer from `stage4-pass1-hint-inventory.py`):

- `scripts/stage4-pass1-edge-candidates.py` — parse → resolve → type → corroboration-flag. Walks all 344 extractions, types via the exact/prefix/keyword map, conforms every output type against the locked vocab (0 drift), routes Tier-1-qualifier-required types to a needs-qualifier tail.
- `scripts/stage4-pass1-evidence-locator.py` — fuzzy-matches each (paraphrased) evidence cell against the chapter prose to attach a **verbatim quote + `file:line`**; chapter-level fallback when no good match.
- `scripts/stage4_name_resolver.py` — the new piece. A 5-rung collision-aware resolution ladder: exact → alias → firstname-unique → context-present (one candidate present in the chapter) → context-prior (backlink-count ≥3× runner-up). Plus a generic-term stoplist and a title-prefix name-key.

Output: `working/wiki/pass2-buckets/pass1-derived/{book}/*.{edges,candidates}.jsonl` + `_tail/` (untyped-but-resolved, citation-staged for the LLM step) + `*.needs-qualifier.jsonl`. Eight `working/wiki/data/pass1-derived-*` audit reports.

---

## Two design decisions made with Matt mid-session

1. **Already-known edges: keep all, but make dupes self-describing.** The old pass dropped 660 rows whose pair already had a wiki edge. Matt's call: keep them (the wiki is mostly canonical — a wiki edge signals importance), but his tech-debt concern reshaped the design: instead of blind duplicates, every edge carries `corroborates_known_edge` + the matched `wiki_edge_type`. A corroborating edge is now an *intentional* primary-source citation attachable to the existing wiki edge, and a **book-vs-wiki type disagreement** (e.g. our `MEMBER_OF` vs wiki `SWORN_TO` for Yoren→Night's Watch; our `PROTECTS` vs wiki `SIBLING_OF` for Jaime→Cersei) is now a recorded, queryable signal rather than noise.
2. **Unresolved pairs → needs-node report, never silent.** Project never-drop ethos.

---

## The recalibration (honest)

The "~50% of edges for free" framing from the design doc was measured on **hint-typing alone** (the hint-inventory script never resolved slugs). For an actual edge, both endpoints must be real nodes — and **5,141 of 7,398 rows (69%) failed resolution**, overwhelmingly because the alias-resolver had no first-name forms (`Tyrion` 493 drops, `Daenerys` 357, `Cersei` 323). The typer was fine; resolution was the bottleneck.

Fix: a supplementary first-name alias layer (`pass1-derived-firstname-aliases.json` — additive, NOT a mutation of `alias-resolver.json`) + the context-disambiguation rungs. Yield arc: **1,035 → 2,466 (alias enrichment) → 2,717 (generic-term fix) → 2,818 (title-prefix fix)**, ambiguous-queued 1,492 → 924. Final honest score: 7,398 rows → 2,818 edges = **38%**, not 50%. Real win, but a quality + traceability + moderate-efficiency win, not an LLM-elimination win.

---

## Two systematic bugs the green tests did NOT catch — only spot-audit did

Both surfaced by eyeballing random samples of the risky resolution rungs, not by the unit tests (which were green throughout). This is the drift-detection / lockdown discipline earning its keep.

1. **Generic role-words → concept nodes (87 edges, 3.5%).** Vague references ("the maester", "a septa", "Lady") resolved to whatever node literally bore that name. e.g. `maester -PROTECTS-> robert-arryn` (really Maester Colemon). Fix: a `GENERIC_TERMS` stoplist; a bare generic term → `unresolved-generic` (logged), never force-resolved. Side effect: removing generics from candidate pools let some previously-ambiguous names resolve uniquely, so the count went *up*.
2. **Title-first-token collapse → `ser-pounce` the CAT (341 edges, 12.6%).** The firstname-index keyed on the literal first token, so nodes whose *names* start with an honorific got indexed under the title; any unresolved "Ser X" reference collapsed onto first-token "ser" → the only such node, Tommen's kitten "Ser Pounce". `arya-stark -HATES-> ser-pounce`, `mance-rayder -RESENTS-> ser-pounce`, etc. — 308 of the 341. Fix: a `name_key()` that strips leading honorifics symmetrically (node-indexing + query-lookup), so "Ser Boros" keys on `boros`, "Khal Drogo" on `drogo`. Post-fix: ser-pounce = 0; the 6 remaining title-first-token edges are all legit (princess-myrcella, a ship, a location, two minor Lord Ryswells).

A blind 20-edge random sample after the fixes read **20/20 correct**.

---

## Verification ledger

- 278 unittests green (151 hint-inventory + prior + 55 pipeline + 47 resolver + 8 generic + 17 title = the running total).
- `wiki-pass2-validate-edge-jsonl.py` on samples across all 5 books: 0 violations. (Note: the validator predates `book-pass1`; the edges pass because the agent added `candidate_kind`/`evidence_book`/`confidence_tier` to satisfy the existing `(emit_edge, pass1_relationship)` contract without modifying the validator. A first-class book-pass1 schema mode is a future item.)
- Conform: 0 vocab drift across 7,398 rows.
- Locator: ~99% verbatim, ~1% chapter-level fallback.

---

## What didn't get done (deliberately)

- **LLM tail NOT run** — it's the untyped-but-resolved rows (citation-staged in `_tail/`), much smaller than the 3,638 design estimate after resolution culled it. Model = Sonnet, smoke first, needs Matt's explicit OK (it's an extraction).
- **Recovery backlog NOT worked** — 924 ambiguous-queued + 387 unresolved names are deterministic recovery fuel.
- **wiki-comention deprecate-stamp NOT done** (design step 4).
- **Throwaway-script cleanup: HOLD** (Matt's choice).
- **Validator book-pass1 mode + resolution-status propagation to edges** — propagation was done (Fix 2); first-class validator schema deferred.

All next-session work is captured in `progress/continue-prompts/2026-05-23-stage4-pass1-tail-and-recovery.md`.
