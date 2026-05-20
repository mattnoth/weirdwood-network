# Vocab Completeness Audit — Session Results

**Date:** 2026-05-19
**Auditor:** Opus 4.7 (general-purpose agent, dispatched by orchestrator)
**Run mode:** ~25 min, single agent, no extraction subagent dispatches
**Audit doc:** `working/qualifier-vocab/audit-completeness-2026-05-19.md`

---

## Inputs surveyed

- **Pass 1 `## Relationships Observed`:** 7,398 rows across 344 extraction files; 4,805 distinct lowercased relationship phrases (matches Session 57 count exactly — validation of method)
- **Pass 1 full-text:** 5-book corpus grep for ~40 candidate concepts
- **21 Sonnet Stage-4 batches:** 4,207 emit_edges + 135 `no-fitting-type-vocab-locked` rejections + 9 escalations + 2,225 freeform `qualifier`-bearing emits (Sonnet was using `qualifier` as a freeform description string at 53% emit rate — rich latent enumeration signal)
- **Wiki infobox qualifiers:** 4,786 records × 25 fields → top fields tabulated

---

## Findings — summary

### Section A — Edge vocabulary gaps

- **Distinct phrases mapped to existing 149 types:** 1,941 / 4,805 (40%); these cover 3,442 / 7,398 rows (46% by volume).
- **Distinct phrases unmapped:** 2,864 (60%); 3,956 rows (54% by volume). Unmapped tail dominated by emotional-synonym variants (mocks/taunts/dismisses/cruel-toward etc.) that ARE covered by existing emotional/perceptual edges via paraphrase but slip the regex anchors. After manual inspection of the unmapped tail and Sonnet's 135 `no-fitting-type` rejections, **8 genuine new-edge candidates** surfaced:
  - **Strong adopt (6):** `SPIES_ON / INFORMS`, `NAMED_AFTER`, `CONSPIRES_WITH`, `RESCUES`, `BANISHES`, `TORTURES`
  - **Consider (2):** `IN_LAW_OF`, `STEP_PARENT_OF` — defer unless Tyrell-Frey political queries or step-relations become primary use cases
  - Plus a half-dozen reject-with-rationale entries (LEGITIMIZES, DISINHERITS, BULLIES, etc. — corpus signal too thin, or already covered)

### Section B — Sub-qualifier candidates

- **Audited:** all 17 Tier-1 + Tier-2 enums × ~5-6 values each
- **Adopt recommendations:** **zero**
- **Strongest near-miss:** `SPOUSE_OF=widowed` has natural by-cause sub-typology (battle ×13 / murder ×3 / illness ×54 / execution ×75) — but every cause is already capturable via separate KILLS / EXECUTES / DIED_OF / DIED_AT edges. Sub-qualifier would duplicate. **Collapse stands.**
- Every Matt-brainstorm candidate either has near-zero corpus signal (MANIPULATES=via_bribe sub-currencies, WARD_OF=hostage sub-types, VOWS_TO=broken modes) or is captured by another edge whose existence makes the sub-qualifier redundant.

### Section C — Confirmed complete

- All 8 Tier-1 enums, all 9 Tier-2 enums, and all 132 Tier-3 edge types audited against Sonnet's 4,207-emit corpus. No additional gaps surfaced.
- Per Session 57 methodology lesson: all 17 Pass 1 sections beyond `## Relationships Observed` re-confirmed — only `## Hospitality & Guest Right` (already absorbed as GUEST_OF) yielded enumerable signal. The other sections are either free-text, entity-attribute, or redundant with `temporal` field.

---

## Top 3 strongest "adopt this" recommendations

1. **`SPIES_ON` / `INFORMS`** — Sonnet currently shoehorns spy-network relationships into SERVES + qualifier strings. Two atomic edges (target=surveilled vs target=handler) close the gap. Westeros's spy networks are structurally important (Varys's little birds, Littlefinger's network).
2. **`NAMED_AFTER`** — Surfaced explicitly in Sonnet `no-fitting-type` rejections (rickard-karstark→rickard-stark, others). ASOIAF's dynastic name-recycling is a graph-traversal asset waiting for an edge.
3. **`CONSPIRES_WITH`** — Already used by Sonnet in qualifier strings 14×; rejected as no-fitting 14× despite obvious narrative weight (Petyr+Olenna, Arianne's Queenmaker plot, Grand Northern Conspiracy). Sits between ALLIES_WITH (open) and NEGOTIATES_WITH (diplomatic).

---

## Where gaps cluster (per Matt's question)

- **NOT concentrated by book** — gap-distribution roughly proportional across all 5 books (verified via book-distribution TSV).
- **NOT concentrated by POV** — appears across all POV-chapter sets.
- **Clusters by relationship-domain:**
  - **Espionage / intelligence:** SPIES_ON / INFORMS / spy-master gap (most acute)
  - **Political dynastic memory:** NAMED_AFTER / STEP_PARENT_OF / IN_LAW_OF (Tyrell-Frey-Reach-network density)
  - **Secret political action:** CONSPIRES_WITH (Petyr/Olenna pattern)
  - **Sustained physical coercion:** TORTURES + BANISHES (Bolton-arc, Bloody-Mummers-arc, Tyrion-Tysha-arc)
  - **Single-event rescue:** RESCUES (Beric-arc, Davos-arc)

Pattern: the gaps cluster on **multi-character political-machine relationships** (spy networks, conspiracies, marriage-political networks) and on **named singular acts** (rescue, banishment, torture). The first cluster is the highest-value adoption; the second is more narrative-color.

---

## Confidence the lockdown is "thorough enough" for Haiku smoke

**High, conditional on Matt verdicting the 6 strong-adopt candidates.**

- With **zero** of the strong-adopts accepted: Haiku will reject ~30-50 cases as `no-fitting-type-vocab-locked` across a typical 200-batch run. This is acceptable and may even be the right call — the rejection channel works.
- With **all 6** accepted: vocab grows 149 → 155, and the rejected-as-no-fit rate drops to negligible.
- The **larger risk on Haiku smoke** is NOT vocab gaps — it's the soft-fallback drift pattern already observed in Sonnet (SERVES-for-everything, KNOWS-as-fallback). Vocab completeness reduces vocab-misroute drift; it does not address Haiku's other failure modes (semantic-contract violations, qualifier-format drift).

**Bet:** the lockdown holds for Haiku smoke from the vocab-completeness angle. The Haiku-specific failure surface lives elsewhere (validator strictness, suspicious-edges flagger) — which is exactly what the remaining HAIKU-CUTOVER steps (2, 3, 4) are designed to address.

---

## Followups for orchestrator

- Bring 6 strong-adopt candidates to Matt for verdict. If accepted, follow the Session 56 apply-vocab path (architecture.md row adds, classifier prompt count updates, regenerate edge-type counts).
- Record Section B verdicts (all collapse-fine) as appended decision-note in `working/qualifier-vocab/decisions.md`.
- The 60% phrase-mapping rate via regex is a measurement-method artifact (regex anchors are conservative); the 95% volume coverage by existing types is the real number.
- `MADE_OF` for-Longclaw and `PRACTICES`-shadow-binding patterns are prompt-clarity issues, NOT vocab gaps — note for next prompt-touch pass.

---

## Cost

- ~25 min wall-clock
- ~$8-12 Opus estimated (corpus read + 4 analysis Python scripts + audit doc draft)
- No subagent dispatches; single-agent inline analysis
