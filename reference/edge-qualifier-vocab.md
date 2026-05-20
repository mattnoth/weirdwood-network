# Edge Qualifier Vocabulary

> The Weirwood Network edge schema includes an optional `qualifier` field on emit_edge rows. Qualifier vocabulary is three-tiered:
> - **Tier 1 (REQUIRED enum)** — edge MUST emit a qualifier from the listed enum. Validator rejects empty or out-of-enum.
> - **Tier 2 (OPTIONAL enum)** — qualifier may be omitted; if emitted, must match the listed enum. Validator rejects out-of-enum but accepts omission.
> - **Tier 3 (no qualifier)** — DEFAULT for any edge type not listed in the table below. Edge MUST NOT have a `qualifier` field. Validator rejects any non-empty qualifier on Tier-3 edges.
>
> The `notes` field is **deleted from the schema entirely** as of 2026-05-18 (Session 57 lock). Validator rejects any edge carrying a `notes` field.

---

## Tier 1 — REQUIRED qualifier (8 edge types)

| Edge Type | Enum Values | Rationale | Data Source |
|-----------|-------------|-----------|-------------|
| `SIBLING_OF` | `full`, `half`, `step`, `milk`, `unknown` | Universal Westerosi kinship category. Corpus: half-brother ×44, half-sister ×9, milk-brother ×9, step- ×0. Step is included as a defensive option (Tommen/Robert via Cersei's prior marriage etc., though rare). | Pass 1 corpus + ASOIAF series knowledge |
| `SPOUSE_OF` | `current`, `former`, `annulled`, `widowed`, `salt_wife`, `unknown` | Four+1 canonical marital states. Corpus: widow* ×238, first/second/third wife ×92, former wife ×9. Wiki: salt wife ×5, dissolved ×3, annulled ×1, possibly ×6. `salt_wife` captures the Ironborn quaternary marital institution. | Wiki infobox + corpus |
| `PARENT_OF` | `biological`, `adopted`, `claimed`, `rumored`, `disputed`, `unknown` | Captures legitimacy / certainty states. Wiki: rumored ×34, disputed ×20, officially ×16, possibly ×13, adopted ×4. `biological` is the default; `claimed` covers Aegon-VI-Targaryen-style assertions; `rumored` covers folkloric attestation. WARD_OF/FOSTERED_BY are separate (fostering is not parentage). | Wiki infobox `Fathers`/`Mothers` plural fields + corpus |
| `WARD_OF` | `formal`, `informal`, `hostage`, `unknown` | Three distinct fostership states in Westerosi politics. Corpus: ward ×259, fostered ×47, hostage ×381. Hostage-as-ward is the dark form (Theon under Ned); formal = acknowledged fostership (Robert under Jon Arryn); informal = household upbringing without formal compact. | Pass 1 corpus + series knowledge |
| `HOLDS_TITLE` | `current`, `former`, `claimed`, `contested`, `historical`, `unknown` | Highest-volume qualifier-bearing field in wiki: 256 qualifier rows / 3976 edges. Wiki: formerly ×62, claimant ×57, historical ×35, stripped ×7, self-styled ×4, disputed ×3. `historical` (deep past Targaryens) ≠ `former` (recently-deposed); kept distinct per wiki convention. `claimed` covers all pretender/self-styled cases. | Wiki infobox (strongest signal) |
| `VOWS_TO` | `active`, `kept`, `broken`, `fulfilled`, `unknown` | Distinct lifecycle states of a personal oath. Corpus: vow ×369, broken vow ×13, fulfilled vow ×2, swore ×100. `active` is in-force (default); `kept` = honored over years; `broken` = violated; `fulfilled` = completed (Brienne returning Sansa). High narrative weight in ASOIAF (Brienne, Jaime, Arya, Sandor). | Pass 1 corpus |
| `MANIPULATES` | `via_bribe`, `via_flattery`, `via_false_information`, `via_threat`, `via_seduction`, `unknown` | Locked Session 55 — confirmed. Original mechanism enum that motivated the whole qualifier-vocab project. | Session 55 verdict |
| `SWORN_TO` | `current`, `former`, `deserted`, `by_marriage`, `claimed`, `unknown` | High-volume feudal allegiance type with rich qualifier surface in wiki. Wiki: formerly ×45, in death ×11, possibly ×9, deserted ×3, by marriage ×2, claimed ×2, annulled ×2. `deserted` captures Night's Watch oath-breakers; `by_marriage` captures fealty-via-spouse (Tully→Stark via Catelyn); `claimed` covers contested vassalage. | Wiki infobox |

---

## Tier 2 — OPTIONAL qualifier (10 edge types)

| Edge Type | Enum Values | Rationale | Data Source |
|-----------|-------------|-----------|-------------|
| `BETROTHED_TO` | `current`, `broken`, `fulfilled`, `secret`, `unknown` | Most betrothal-text is straightforward state-declaration (no qualifier needed). Optional to capture when narratively important. Corpus: betrothed ×335, broke betroth ×3. Pass 1 also showed `secret` betrothals (Robb-Jeyne-Westerling-style). | Pass 1 corpus + series knowledge |
| `LOVER_OF` | `current`, `former`, `secret`, `paramour`, `rumored`, `unknown` | Pass 1: former ×19, secret ×7, paramour ×7 in the relation column. Wiki: rumored ×36 (dominant), paramour ×4. `paramour` is the formal Westerosi term for an acknowledged extramarital partner (Ellaria, Bellegere); `rumored` covers the gossip-historical layer (Lyonel Strong / Rhaenyra). | Pass 1 corpus + wiki infobox |
| `KILLS` | `in_combat`, `in_duel`, `by_arrow`, `by_blade`, `by_ambush`, `by_proxy`, `by_creature`, `unknown` | Method matters narratively. Corpus: in combat ×117, in a duel ×4, ambush ×188, by proxy ×7, via creature ×14, beheaded ×290, stabbed ×147. `POISONS` is a separate edge type — do NOT fold into KILLS method. `by_creature` covers dragon-burning, wolf-killing, eagle-attack-causing-death. `by_proxy` covers catspaw-style indirect killing. | Pass 1 corpus full-text |
| `CONTRACTED_WITH` | `assassination`, `mercenary_service`, `ransom`, `safe_passage`, `construction`, `marriage_brokerage`, `espionage`, `unknown` | Service-type matters. Corpus: hired ×93, sellsword/mercenary ×398, assassinate ×160, ransom ×132, safe passage ×27. The Faceless Men, Golden Company, smaller free companies, ransom negotiations (Tyrion/Lannister deals), Tycho Nestoris's loans — distinct service categories. | Pass 1 corpus |
| `DECEIVES` | `by_lie`, `by_disguise`, `by_omission`, `by_false_witness`, `by_silence`, `unknown` | Method matters. Corpus: lie ×647, disguise ×208, false witness ×5. `by_omission` and `by_silence` are distinct narrative devices (Ned's silence on Jon's parentage). | Pass 1 corpus |
| `REVEALS_TO` | `voluntary`, `coerced`, `accidental`, `under_torture`, `unknown` | Disclosure conditions matter for trust/credibility scoring. Corpus: voluntarily ×25, under torture ×57, let slip ×10. | Pass 1 corpus |
| `ATTACKS` | `in_anger`, `unprovoked`, `in_self_defense`, `on_command`, `by_creature`, `unknown` | Motive context. Corpus: in anger ×23, on command ×19, self-defense ×2, unprovoked ×0 (concept exists; word doesn't). `by_creature` for direwolf/eagle/dragon attacks. Weaker empirical signal than other Tier-2 candidates — could drop to Tier-3 if Haiku smoke reveals it's never emitted. | Pass 1 corpus |
| `KNOWS` | `confirmed`, `suspected`, `told_by`, `witnessed`, `overheard`, `unknown` | Source-of-knowledge basis. Corpus: confirms ×310, suspect ×219, told by ×169, witnessed ×99, overheard ×47. Pairs with `IGNORANT_OF` for knowledge-asymmetry queries (does Sansa know what Cersei knows about Jaime?). | Pass 1 corpus + Information Revealed table `How Revealed` column |
| `GUEST_OF` | `shelter`, `feast`, `bread_and_salt`, `safe_conduct`, `gift_exchange`, `refused`, `unknown` | Pass 1 explicitly types hospitality events. 680 rows across 344 chapters; top categories: shelter_offered ×235, feast_given ×85, gift_exchange ×46, safe_conduct ×27, bread_and_salt ×10. `bread_and_salt` is the formal compact (sacred); `shelter` is the common case; `refused` covers shelter_denied / refusal_to_host. Violations are captured by the separate `VIOLATES_GUEST_RIGHT` edge — do not fold into GUEST_OF qualifier. Hostage situations are captured by `PRISONER_OF`, not GUEST_OF. | Pass 1 `## Hospitality & Guest Right` table |
| `IN_LAW_OF` | `by_marriage_of_self`, `by_marriage_of_child`, `by_marriage_of_sibling`, `by_marriage_of_parent`, `unknown` | Marriage-affinity relationship. Symmetric. Sonnet's freeform-qualifier corpus has 97 mentions of "good-mother", "good-father", "good-sister", "good-son", "mother-in-law", "sister-in-law" — mostly in Reach noble-house arcs. Qualifier identifies *which marriage* created the affinity: `by_marriage_of_self` (you married their relative), `by_marriage_of_child` (your child married them or their relative), `by_marriage_of_sibling`, `by_marriage_of_parent`. The graph currently forces a two-hop traversal (SPOUSE_OF + PARENT_OF + invert) and gets nothing for cases where only the in-law link is known; `IN_LAW_OF` closes that gap. | Pass 1 corpus (3 P1 rows) + Sonnet freeform qualifier usage (97 mentions) |

---

## Tier 3 — NO qualifier (default for all other edge types)

All edge types NOT listed in Tier 1 or Tier 2 above are Tier 3. These edges emit no `qualifier` field and no `notes` field. The edge stands on its own: `source / edge_type / target / confidence_tier / evidence_snippet / evidence_kind`.

**Count check:** Tier 1 (8) + Tier 2 (10) + Tier 3 (~141) = ~159 total (matches architecture.md master vocab count as of Session 58, 2026-05-19).

---

## Validator rules (for HAIKU-CUTOVER STEP 3)

When `scripts/wiki-pass2-validate-edge-jsonl.py` is extended with qualifier enforcement (STEP 3), it must implement:

1. Load this file and parse the per-edge-type enum table into a `QUALIFIER_ENUM: {edge_type: (tier, frozenset(enum_values))}` lookup.
2. For each `emit_edge` row:
   - If `edge_type` is Tier 1: reject if `qualifier` is missing or not in enum.
   - If `edge_type` is Tier 2: accept if `qualifier` is absent; reject if present and not in enum.
   - If `edge_type` is Tier 3 (not listed above): reject if `qualifier` is present (any value).
   - Reject if `notes` field is present on any edge (field deleted from schema 2026-05-18).
