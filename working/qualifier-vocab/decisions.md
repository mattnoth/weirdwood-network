# Qualifier Vocabulary Lock-Down — Decisions

> **Status:** DECISIONS LOCKED — 2026-05-18 (Session 57)
> **Parent plan:** `working/qualifier-vocab/plan.md`
> **Continue prompt:** `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-lock.md`
> **Next session:** STEP 1.6 — encode these decisions into `reference/edge-qualifier-vocab.md` + classifier prompt + validator. (Separate from HAIKU-CUTOVER STEP 3 type-contract encoding.)

---

## Data sources surveyed

| Source | Volume | Signal-strength |
|---|---|---|
| 21 completed Sonnet batches | 4,152 emit_edges across 891 `*.edges.jsonl` files | `notes` field empty in **4,138 / 4,152 (99.7%)** — drift is preventive, not observed. The 14 non-empty notes were tier-2-confidence justifications, not qualifier values. |
| Pass 1 corpus — `## Relationships Observed` tables | 7,398 rows from 344 extraction files; 4,805 distinct relationship phrases | Strong qualifier vocabulary in the prose: half-brother ×9, half-sister ×3, milk-brother ×9, widow* ×238, betrothed ×335, ward ×259, fostered ×47, hostage ×381, former-[title] ×115, vow ×369, bastard-son ×103. |
| Pass 1 corpus — `## Hospitality & Guest Right` tables | 680 rows from 344 extraction files; 80 distinct `Type` values but top-10 = 88% of rows | **Pass 1 ALREADY enumerates hospitality.** Top types: `shelter_offered` ×235, `feast_given` ×85, `hospitality_violated` ×52, `gift_exchange` ×46, `safe_conduct` ×27, `guest_right_invoked` ×24, `refusal_to_host` ×15, `shelter_denied` ×15, `hospitality_offered` ×14, `bread_and_salt` ×10. Found mid-session after Matt prompted "other tables worth noting?" |
| Pass 1 corpus — `## Events & Actions` numbered sequences | 344 files | Confirms KILLS method enum: crossbow/longsword/axe/dagger language is the dominant weapon-attribution form. Validates `by_arrow` / `by_blade` / `by_ambush` enum choices. Does not surface new categories beyond the existing enum. |
| Pass 1 corpus — `## Information Revealed` tables | 344 files | Confirms KNOWS source-of-knowledge enum. `How Revealed` column patterns: "X states it", "internal thought", "recalls", "observes", "Y says it" — maps cleanly to `told_by` / `confirmed` / `witnessed`. No new qualifier surface. |
| Pass 1 corpus — full-text grep | 344 files (5 books) | Re-validates the structured-table signal; adds method-language (poisoned ×532, beheaded ×290, stabbed ×147, by arrow ×1293) for KILLS / ATTACKS / DECEIVES enumeration. |
| Wiki infobox `qualifier` field | 5,279 entities; 2,287 qualifier-bearing rows across 25 fields | Already-parsed per-field per-row qualifiers. **HOLDS_TITLE:** formerly ×62, claimant ×57, historical ×35, stripped ×7, self-styled ×4. **PARENT_OF:** rumored ×34, disputed ×20, officially ×16, adopted ×4. **SWORN_TO:** formerly ×45, in death ×11, deserted ×3, by marriage ×2. **LOVER_OF:** rumored ×36, paramour ×4. **SPOUSE_OF:** salt wife ×5, dissolved ×3, annulled ×1. |

---

## Three-tier framing (locked Session 56 — restated)

| Tier | Behavior | Validator |
|---|---|---|
| **1 — REQUIRED enum** | Edge MUST emit a `qualifier` field from a small closed set. Empty / missing → reject. | Reject edges with missing or out-of-enum qualifier. |
| **2 — OPTIONAL enum** | `qualifier` may be omitted; if emitted, must match the enum. | Reject out-of-enum values; accept omission. |
| **3 — no enum** | Edge has NO `qualifier` field. No `notes` field either (see Q2). The edge is just `source / edge_type / target / confidence_tier / evidence_snippet / evidence_kind`. | No qualifier check. Reject any non-empty `qualifier` field. |

---

## Open questions — answered

**Q1 — Backfill strategy for 21 already-emitted Sonnet batches?**
> **DECISION:** Leave as-is. The 4,152 existing emits keep their (mostly empty) notes; no normalizer, no re-classification. Instead, they become the **freeform control arm for the Haiku enum-locked comparison.** When STEP 5 (Haiku smoke) runs against the locked schema, the diff against Sonnet-pre-lock answers an interesting empirical question: *did the freeform `notes` field carry information we lost by deleting it, or was it noise we're better off without?* Backfill TBD after that comparison.

**Q2 — Tier-3 `notes` discipline?**
> **DECISION:** **Zero freeform.** The `notes` field is **deleted from the edge schema entirely** for all three tiers. Tier-1 emits `qualifier` from the enum. Tier-2 emits `qualifier` from the enum OR omits it. Tier-3 emits no qualifier at all. No `notes` field is permitted on any edge. Rationale: notes was the open drift surface qualifier-vocab is supposed to close. Leaving it open for Tier-3 reintroduces the surface we're trying to seal. Narrative-context loss is the price of closed-vocabulary safety on Haiku.

**Q3 — Combine type-contract column with qualifier column in single architecture.md change?**
> **DECISION:** **Two separate passes.** STEP 1.6 (qualifier encoding) and HAIKU-CUTOVER STEP 3 (type-contract encoding) remain distinct sessions. Per Option C below, qualifier data lives in a NEW file (not architecture.md), so this question becomes moot — STEP 1.6 doesn't touch architecture.md tables at all. STEP 3's type-contract change is unblocked by STEP 1.6 entirely.

**Q4 — Encoding strategy A/B/C?**
> **DECISION:** **Option C** (decided by independent fresh-context agent, verdict 2026-05-18). Qualifier enums for Tier-1 (required) and Tier-2 (optional) edge types live in a new file `reference/edge-qualifier-vocab.md` as a single table: `edge_type | tier | enum_values | rationale`. Architecture.md's `## Edge Types` intro gets a one-line cross-reference pointer ("Qualifier enums for tiered types: see `reference/edge-qualifier-vocab.md`"); existing tables are not modified. The classifier prompt and validator both load the new file as a second source of truth alongside architecture.md. This keeps Tier-3 rows (~133 of 149) noise-free, leaves the parallel type-contract architecture.md edit unblocked, and gives the validator a single contained file to parse for enum enforcement.

**Q5 — Symmetric-edge qualifier semantics?**
> **DECISION (locked Session 56, restated here):** Symmetric edges share their qualifier across both endpoints. `SIBLING_OF(a→b, qualifier=half)` implies `SIBLING_OF(b→a, qualifier=half)`. The validator enforces consistency on both emissions if both are present; query layer treats them as one edge.

---

## Verdicts — Tier 1 (REQUIRED enum) — 8 types

| Edge Type | Enum | Rationale | Data source |
|---|---|---|---|
| `SIBLING_OF` | `{full, half, step, milk, unknown}` | Universal Westerosi kinship category. Pass 1 prose: half-brother ×44, half-sister ×9, milk-brother ×9, step- ×0. Step is included as a defensive option (Tommen/Robert via Cersei's prior marriage etc., though rare). | Pass 1 corpus + ASOIAF series knowledge |
| `SPOUSE_OF` | `{current, former, annulled, widowed, salt_wife, unknown}` | Four+1 canonical marital states. Corpus: widow* ×238, first/second/third wife ×92, former wife ×9. Wiki: salt wife ×5, dissolved ×3, annulled ×1, possibly ×6. `salt_wife` captures the Ironborn quaternary marital institution. | Wiki infobox + corpus |
| `PARENT_OF` | `{biological, adopted, claimed, rumored, disputed, unknown}` | Captures legitimacy / certainty states. Wiki: rumored ×34, disputed ×20, officially ×16, possibly ×13, adopted ×4. `biological` is the default; `claimed` covers Aegon-VI-Targaryen-style assertions; `rumored` covers folkloric attestation. WARD_OF/FOSTERED_BY are separate (fostering is not parentage). | Wiki infobox `Fathers`/`Mothers` plural fields + corpus |
| `WARD_OF` | `{formal, informal, hostage, unknown}` | Three distinct fostership states in Westerosi politics. Corpus: ward ×259, fostered ×47, hostage ×381. Hostage-as-ward is the dark form (Theon under Ned); formal = acknowledged fostership (Robert under Jon Arryn); informal = household upbringing without formal compact. | Pass 1 corpus + series knowledge |
| `HOLDS_TITLE` | `{current, former, claimed, contested, historical, unknown}` | Highest-volume qualifier-bearing field in wiki: 256 qualifier rows / 3976 edges. Wiki: formerly ×62, claimant ×57, historical ×35, stripped ×7, self-styled ×4, disputed ×3. `historical` (deep past Targaryens) ≠ `former` (recently-deposed); kept distinct per wiki convention. `claimed` covers all pretender/self-styled cases. | Wiki infobox (strongest signal) |
| `VOWS_TO` | `{active, kept, broken, fulfilled, unknown}` | Distinct lifecycle states of a personal oath. Corpus: vow ×369, broken vow ×13, fulfilled vow ×2, swore ×100. `active` is in-force (default); `kept` = honored over years; `broken` = violated; `fulfilled` = completed (Brienne returning Sansa). High narrative weight in ASOIAF (Brienne, Jaime, Arya, Sandor). | Pass 1 corpus |
| `MANIPULATES` | `{via_bribe, via_flattery, via_false_information, via_threat, via_seduction, unknown}` | **Locked Session 55 — confirmed.** Original mechanism enum that motivated the whole qualifier-vocab project. | Session 55 verdict |
| `SWORN_TO` | `{current, former, deserted, by_marriage, claimed, unknown}` | High-volume feudal allegiance type with rich qualifier surface in wiki. Wiki: formerly ×45, in death ×11, possibly ×9, deserted ×3, by marriage ×2, claimed ×2, annulled ×2. `deserted` captures Night's Watch oath-breakers; `by_marriage` captures fealty-via-spouse (Tully→Stark via Catelyn); `claimed` covers contested vassalage. | Wiki infobox |

---

## Verdicts — Tier 2 (OPTIONAL enum) — 9 types

| Edge Type | Enum | Rationale | Data source |
|---|---|---|---|
| `BETROTHED_TO` | `{current, broken, fulfilled, secret, unknown}` | Most betrothal-text is straightforward state-declaration (no qualifier needed). Optional to capture when narratively important. Corpus: betrothed ×335, broke betroth ×3. Pass 1 also showed `secret` betrothals (Robb-Jeyne-Westerling-style). | Pass 1 corpus + series knowledge |
| `LOVER_OF` | `{current, former, secret, paramour, rumored, unknown}` | Pass 1: former ×19, secret ×7, paramour ×7 in the relation column. Wiki: rumored ×36 (dominant), paramour ×4. `paramour` is the formal Westerosi term for an acknowledged extramarital partner (Ellaria, Bellegere); `rumored` covers the gossip-historical layer (Lyonel Strong / Rhaenyra). | Pass 1 corpus + wiki infobox |
| `KILLS` | `{in_combat, in_duel, by_arrow, by_blade, by_ambush, by_proxy, by_creature, unknown}` | Method matters narratively. Corpus: in combat ×117, in a duel ×4, ambush ×188, by proxy ×7, via creature ×14, beheaded ×290, stabbed ×147. **`POISONS` is a separate edge type — do NOT fold into KILLS method.** `by_creature` covers dragon-burning, wolf-killing, eagle-attack-causing-death. `by_proxy` covers catspaw-style indirect killing. | Pass 1 corpus full-text |
| `CONTRACTED_WITH` | `{assassination, mercenary_service, ransom, safe_passage, construction, marriage_brokerage, espionage, unknown}` | Service-type matters. Corpus: hired ×93, sellsword/mercenary ×398, assassinate ×160, ransom ×132, safe passage ×27. The Faceless Men, Golden Company, smaller free companies, ransom negotiations (Tyrion/Lannister deals), Tycho Nestoris's loans — distinct service categories. | Pass 1 corpus |
| `DECEIVES` | `{by_lie, by_disguise, by_omission, by_false_witness, by_silence, unknown}` | Method matters. Corpus: lie ×647, disguise ×208, false witness ×5. `by_omission` and `by_silence` are distinct narrative devices (Ned's silence on Jon's parentage). | Pass 1 corpus |
| `REVEALS_TO` | `{voluntary, coerced, accidental, under_torture, unknown}` | Disclosure conditions matter for trust/credibility scoring. Corpus: voluntarily ×25, under torture ×57, let slip ×10. | Pass 1 corpus |
| `ATTACKS` | `{in_anger, unprovoked, in_self_defense, on_command, by_creature, unknown}` | Motive context. Corpus: in anger ×23, on command ×19, self-defense ×2, unprovoked ×0 (concept exists; word doesn't). `by_creature` for direwolf/eagle/dragon attacks. Weaker empirical signal than other Tier-2 candidates — could drop to Tier-3 if Haiku smoke reveals it's never emitted. | Pass 1 corpus |
| `KNOWS` | `{confirmed, suspected, told_by, witnessed, overheard, unknown}` | Source-of-knowledge basis. Corpus: confirms ×310, suspect ×219, told by ×169, witnessed ×99, overheard ×47. Pairs with `IGNORANT_OF` for knowledge-asymmetry queries (does Sansa know what Cersei knows about Jaime?). | Pass 1 corpus + Information Revealed table `How Revealed` column |
| `GUEST_OF` | `{shelter, feast, bread_and_salt, safe_conduct, gift_exchange, refused, unknown}` | Pass 1 explicitly types hospitality events. 680 rows across 344 chapters; top categories: shelter_offered ×235, feast_given ×85, gift_exchange ×46, safe_conduct ×27, bread_and_salt ×10. `bread_and_salt` is the formal compact (sacred); `shelter` is the common case; `refused` covers shelter_denied / refusal_to_host. **Violations are captured by the separate `VIOLATES_GUEST_RIGHT` edge — do not fold into GUEST_OF qualifier.** Hostage situations are captured by `PRISONER_OF`, not GUEST_OF. | Pass 1 `## Hospitality & Guest Right` table |

---

## Verdict — Tier 3 (NO qualifier, NO notes) — 132 types

Default tier. All edge types not listed in Tier 1 / Tier 2 above are Tier 3. **Tier-3 edges emit no `qualifier` field and no `notes` field.** The edge stands on its own: `source / edge_type / target / confidence_tier / evidence_snippet / evidence_kind / first_available`.

Tier-3 by subsection:

- **Kinship & Family** (other): `LOVER_OF` is Tier-2 (above); `ANCESTOR_OF`, `HEIR_TO`, `CADET_BRANCH_OF`, `MARRIES_OFF`, `UNCLE_OF`, `NEPHEW_OF`, `COUSIN_OF`, `MILK_BROTHER_OF`, `NURSED_BY`, `WET_NURSE_OF`, `COURTS`, `PROPOSED_AS_BRIDE` — all Tier-3. Rationale: these are factual relationship declarations; qualifier surface is thin or already captured by directionality.
- **Political & Authority** (other): `RULES`, `OVERLORD_OF`, `COMMANDS`, `SERVES`, `ADVISES`, `HELD_BY`, `SUCCEEDS`, `CLAIMS`, `APPOINTS`, `DEPOSES`, `BREAKS_VOW` — Tier-3. Rationale: state-declarations or directional events; no meaningful enum surface beyond what `temporal` would capture.
- **Factional & Diplomatic** (other): `MEMBER_OF`, `FOUNDED`, `ALLIES_WITH`, `OPPOSES`, `BETRAYS`, `NEGOTIATES_WITH` — Tier-3.
- **Military & Conflict** (other): `FIGHTS_IN`, `COMMANDS_IN`, `PART_OF`, `KILLED_BY`, `EXECUTES`, `CAPTURES`, `PRISONER_OF`, `BESIEGES`, `DEFEATS`, `DUELS`, `POISONS`, `RANSOMS`, `IMPRISONS`, `KILLED_WITH`, `KNIGHTED_BY`, `BESTOWS_KNIGHTHOOD_ON`, `ASSAULTS`, `PARTICIPATES_IN` — Tier-3. Rationale: event-pointed edges; the event itself carries narrative weight, not a qualifier.
- **Knowledge & Information** (other): `IGNORANT_OF`, `SEEKS`, `DECEIVED_BY`, `HOARDS`, `INVESTIGATES`, `TEACHES`, `TUTORS`, `HEALS`, `AFFLICTED_BY`, `DIED_OF` — Tier-3.
- **Emotional & Perceptual** (ALL): `PERCEIVED_AS`, `TRUSTS`, `DISTRUSTS`, `RESPECTS`, `FEARS`, `LOVES`, `HATES`, `MOURNS`, `PROTECTS`, `RESENTS`, `COMPANION_OF`, `REPUTED_AS` — Tier-3. Rationale: fuzziness is the essence; any forced enum would lose more than it captures. Pass 1 confirms these phrases vary too widely to bucket.
- **Spatial & Temporal** (ALL): `LOCATED_AT`, `SEAT_OF`, `TRAVELS_TO`, `BORN_AT`, `DIED_AT`, `BURIED_AT`, `CONTEMPORARY_WITH`, `REGION_OF` — Tier-3. Rationale: spatial facts; `temporal` field already captures when-edges.
- **Possession & Ownership** (ALL): `WIELDS`, `OWNS`, `ANCESTRAL_WEAPON_OF`, `FORGED_BY`, `MADE_OF`, `LOOTED_BY`, `REFORGED_INTO`, `GIFTED_TO`, `INHERITED_BY`, `WIELDED_IN`, `EXECUTED_WITH`, `PURCHASED_FROM`, `BUILT`, `CAPTAIN_OF`, `CREW_OF` — Tier-3.
- **Identity & Disguise** (ALL): `ALIAS_OF`, `DISGUISED_AS`, `SAME_AS`, `IMPERSONATES` — Tier-3.
- **Magic & Supernatural** (ALL): `WARGS_INTO`, `BONDED_TO`, `SACRIFICES`, `RESURRECTS`, `CURSES`, `PRACTICES` — Tier-3.
- **Cultural & Religious** (ALL): `CULTURE_OF`, `WORSHIPS`, `SACRED_TO`, `CLERGY_OF`, `OFFICIATES` — Tier-3.
- **Narrative & Literary** (ALL): `DEPICTED_IN`, `FORESHADOWS`, `PARALLELS`, `SUBVERTS`, `ECHOES`, `CONTRASTS`, `WRITTEN_BY` — Tier-3.
- **Prophecy** (ALL): `FULFILLS`, `APPEARS_TO_FULFILL`, `SUBVERTS_PROPHECY`, `PROPHESIED_BY`, `SUBJECT_OF_PROPHECY`, `DREAMS_OF` — Tier-3.
- **Evidentiary** (ALL): `SUPPORTS`, `CONTRADICTS`, `CITED_BY` — Tier-3.
- **Causal & Plot** (ALL): `CAUSES`, `PREVENTS`, `ENABLES`, `MOTIVATES`, `TRIGGERS` — Tier-3.
- **Hospitality & Custom** (other): `GUEST_OF` is Tier-2 (above); `VIOLATES_GUEST_RIGHT`, `GRANTS_SAFE_CONDUCT`, `ATTENDS`, `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` — Tier-3.

**Count check:** Tier 1 (8) + Tier 2 (9) + Tier 3 (132) = 149 ✓ (matches architecture.md master vocab count)

---

## Schema implications (for STEP 1.6 + STEP 3)

The edge schema after STEP 1.6 + STEP 3 lands:

```json
{
  "source_slug": "...",
  "edge_type": "...",          // master vocab from architecture.md (locked, ~149)
  "target_slug": "...",
  "qualifier": "...",           // Tier-1: required from enum; Tier-2: optional from enum; Tier-3: MUST be absent
  "confidence_tier": 1|2|3,
  "evidence_snippet": "...",
  "evidence_kind": "wiki-entity"|"wiki-chapter-summary"|"book-pass1",
  "first_available": "..."
  // NO notes field anywhere — deleted from schema
  // temporal / symmetric: pre-existing, unchanged
}
```

### Required validator changes (STEP 3)

The validator (`scripts/wiki-pass2-validate-edge-jsonl.py`) must:

1. Load `reference/edge-qualifier-vocab.md` and parse the per-edge-type enum table into a `QUALIFIER_ENUM: {edge_type: (tier, frozenset(enum_values))}` lookup.
2. For each `emit_edge` row:
   - If `edge_type` is Tier-1: reject if `qualifier` missing or not in enum.
   - If `edge_type` is Tier-2: accept if `qualifier` absent; reject if present and not in enum.
   - If `edge_type` is Tier-3: reject if `qualifier` is present (any value).
   - Reject if `notes` field is present (any tier; field is deleted from schema).
3. Continue with existing schema checks (canonical edge_type, evidence_snippet shape, evidence_kind ↔ candidate_kind match, etc.).

### Required classifier prompt changes (STEP 1.6)

The prose-edge-classifier prompt (`.claude/agents/prose-edge-classifier.md`) must:

1. Add a step "Look up qualifier enum for this edge type in `reference/edge-qualifier-vocab.md`."
2. Update the emit_edge JSON schema in the prompt:
   - Remove `notes` field entirely.
   - Add `qualifier` field with tier-dependent behavior documented inline.
3. Add a Tier-1 enforcement note: "If you emit a Tier-1 edge without a qualifier, you have made an error — re-read the evidence to determine which enum value applies, or use `unknown` only as a last resort."

---

## Methodology note — Pass 1 section audit

Initial verdict draft surveyed only `## Relationships Observed`. Matt prompted mid-session: "is that the only table worth noting? There is spatial movement as well." Audit of the remaining 16 Pass 1 sections yielded one missed enumerable type: **`GUEST_OF`**, surfaced via the `## Hospitality & Guest Right` table which Pass 1 already types into 80 distinct values dominated by 10 categories (88% coverage). Other sections audited (`## Spatial Layout & Movement`, `## Events & Actions`, `## Information Revealed`, `## Dialogue of Note`) confirmed existing enum choices but did not surface new enumerable types — their qualifier surface was either free-text (Dialogue of Note), redundant with `temporal` (Spatial Layout & Movement, LOCATED_AT phase tags), or already captured (Events & Actions for KILLS method, Information Revealed for KNOWS basis).

Lesson: when Pass 1's schema itself enumerates something (Hospitality `Type` column, Information Revealed `How Revealed` column), that enumeration is direct empirical evidence of an enumerable edge-type qualifier. Hospitality was the only section with structurally-typed enum values beyond `Relationships Observed`. The other 13 sections are free-text or contain values that map to non-qualifier metadata (timestamps, locations, narrative phases).

## Definition of done — this session

- [x] All Tier-1 enums verified against corpus distribution (each Tier-1 type has ≥1 high-volume corpus or wiki signal; coverage is qualitative not strictly numerical since corpus-language doesn't always match the chosen enum-keys directly).
- [x] All Tier-2 enums proposed with rationale + data source.
- [x] Tier-3 enumerated by subsection with one-line group rationale (not per-type, per Matt's "don't death-march" guidance).
- [x] Encoding strategy chosen via independent agent (Option C).
- [x] Open questions Q1–Q5 answered with decisions.
- [x] Schema implications documented for STEP 1.6 + STEP 3 follow-ups.
- [x] `notes` field deletion decision recorded (Matt's call: zero freeform).

---

## What this session does NOT do (per continue prompt)

- Does not write `reference/edge-qualifier-vocab.md` (that's STEP 1.6).
- Does not modify `reference/architecture.md` (only adds a cross-reference pointer in STEP 1.6).
- Does not modify `.claude/agents/prose-edge-classifier.md` (that's STEP 1.6).
- Does not modify `scripts/wiki-pass2-validate-edge-jsonl.py` (that's STEP 3, folded with type-contract validator extension).
- Does not retrofit / re-classify the 21 completed Sonnet batches. Their `notes`-bearing 14 emits remain as the freeform control arm for the eventual Haiku enum-locked comparison.

---

## Followups

- **STEP 1.6 — encode** (next session). Write `reference/edge-qualifier-vocab.md`, update architecture.md with one cross-reference line, update prose-edge-classifier prompt (delete `notes` from emit schema, add `qualifier` field + lookup step).
- **HAIKU-CUTOVER STEP 3 — validator extension** (separate session). Add type-contract enforcement + qualifier-enum enforcement to `scripts/wiki-pass2-validate-edge-jsonl.py`.
- **STEP 5 — Haiku smoke** (after 1.6 + 2 + 3 + 4). Now also diffs qualifier-enum agreement between Haiku and the freeform-Sonnet control arm.

---

## Round 2 — Vocab Completeness Audit (2026-05-19)

> **Audit source:** `working/qualifier-vocab/audit-completeness-2026-05-19.md`
> **Auditor:** Opus 4.7 (Session 58 continuation)
> **Encoder:** Sonnet 4.6 (this session — mechanical translation of adopted candidates into runnable artifacts)
> **Input corpus:** 7,398 `## Relationships Observed` rows across 344 Pass 1 extraction files (4,805 distinct phrases) + 4,207 emit_edges from 21 Sonnet Stage-4 batches + 135 `no-fitting-type-vocab-locked` rejections + wiki infobox-qualifier distribution (4,786 records, 25 fields).

### Verdict matrix

| Section | Count | Verdict |
|---|---|---|
| A.1 STRONG ADOPT candidates | 8 adoptions → 10 new edge types | **ALL ADOPTED** (Matt's directive: "adopt all 8 STRONG") |
| A.2 MEDIUM ADOPT candidates | 8 types | **DEFERRED** — existing edge types partially cover; revisit post-Haiku smoke |
| A.3 REJECT | 11 patterns | **REJECTED** — insufficient corpus signal or subsumed by existing types |
| A.4 Sonnet-flagged borderlines | 3 cases | 2 DEFER (SHADOWBINDS, SOLD_TO); 1 prompt-clarity note (MADE_OF for Longclaw) |

### The 10 new edge types (Round 2 adoptions)

| # | New edge(s) | Type | Subsection | Directionality | Source |
|---|---|---|---|---|---|
| 1 | `SPIES_ON` | Tier-3 | Knowledge & Information | Person → Surveilled-person | Pass 1 corpus + Sonnet no-fit |
| 2 | `INFORMS` | Tier-3 | Knowledge & Information | Person → Handler/Spymaster | Pass 1 corpus + Sonnet no-fit |
| 3 | `NAMED_AFTER` | Tier-3 | Cultural & Religious | Entity → Namesake-entity (one-sided) | wiki (dynastic naming patterns) |
| 4 | `STEP_PARENT_OF` | Tier-3 | Kinship & Family | Step-parent → Step-child | corpus (marital-consequence relation) |
| 5 | `STEP_CHILD_OF` | Tier-3 | Kinship & Family | Step-child → Step-parent (reverse of STEP_PARENT_OF) | corpus |
| 6 | `IN_LAW_OF` | **Tier-2 OPTIONAL enum** | Kinship & Family | Symmetric | Pass 1 corpus (3 rows) + Sonnet freeform (97 mentions) |
| 7 | `RESCUES` | Tier-3 | Military & Conflict | Rescuer → Rescued-person | corpus |
| 8 | `BANISHES` | Tier-3 | Political & Authority | Banisher → Banished-person | corpus |
| 9 | `TORTURES` | Tier-3 | Military & Conflict | Torturer → Tortured-person | corpus |
| 10 | `CONSPIRES_WITH` | Tier-3 | Factional & Diplomatic | Symmetric | corpus |

**IN_LAW_OF qualifier enum (Tier-2 OPTIONAL):** `{by_marriage_of_self, by_marriage_of_child, by_marriage_of_sibling, by_marriage_of_parent, unknown}`

### Sub-qualifier verdict — Round 2

**Zero sub-qualifier additions.** Section B of the audit confirmed all collapse-fine verdicts: every Tier-1 and Tier-2 enum is complete; no sub-typology dimension warrants adoption. The strongest case (SPOUSE_OF=widowed by cause) is already implicit via separate KILLS/EXECUTES/DIED_OF/DIED_AT edges. Audit confirmed: adding sub-qualifiers expands the validator surface for marginal narrative payoff.

### Round count update

| Metric | Round 1 (Session 57) | Round 2 (Session 58) |
|---|---|---|
| Total edge types | 149 | **159** |
| Tier-1 (REQUIRED enum) | 8 | 8 (unchanged) |
| Tier-2 (OPTIONAL enum) | 9 | **10** (IN_LAW_OF added) |
| Tier-3 (no qualifier) | 132 | **141** |
| Enumerable types total | 17 | **18** |
