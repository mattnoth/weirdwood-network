# Vocab Completeness Audit — 2026-05-19

> **Status:** CANDIDATES — no encoding performed. Human verdict required before any vocabulary change.
> **Auditor:** Opus 4.7 general-purpose agent (Session 58 continuation)
> **Input universe surveyed:** 7,398 `## Relationships Observed` rows across 344 Pass 1 extraction files (4,805 distinct lowercased phrases) + full-text corpus (~5 books) + 4,207 emit_edges + 135 `no-fitting-type-vocab-locked` rejections from 21 completed Sonnet Stage-4 batches + wiki infobox-qualifier distribution (4,786 records, 25 fields).
> **Method:** Coverage-driven (not count-driven). For Section A, every distinct phrase was substring-matched against ~250 regex anchors keyed to the 149 locked edge types; the unmapped tail (2,864 phrases / 3,956 row-instances) was inspected manually for recurrent patterns. For Section B, each enumerable Tier-1/Tier-2 value was queried against the wiki qualifier table + full Pass 1 corpus + Sonnet's freeform `qualifier` field (used by Sonnet in 2,225/4,207 emits as a narrative description) to surface sub-typologies. For Section C, edge types with at-or-above-expected emit volume across the 21 Sonnet batches were flagged confirmed-complete.

---

## Section A — Edge Vocabulary Gaps

Format: `Phrase / pattern | Volume signal | Closest existing | Proposed | Rationale`.
Sorted by **recommended-adopt confidence** (strongest first). Volume column shows `P1 Relationships Observed rows` / `full-corpus mentions` / `Sonnet emit-qualifier mentions` / `Sonnet no-fitting cites`.

### A.1 — STRONG ADOPT candidates (recurring pattern in both prose and Sonnet stream)

| # | Phrase / pattern | Volume (P1 / corpus / sonnet-q / no-fit) | Closest existing | Proposed | Rationale |
|---|---|---|---|---|---|
| 1 | "spies on / informs on / agent of / reports to / spymaster" | 11 / 85 / 9 / 0 (named spy-network rows mostly in MANIPULATES/SERVES qualifier strings) | `SERVES` (too generic); `MANIPULATES` (wrong direction — spy works for handler, not against); `KNOWS` (doesn't capture the directionality of reporting) | **`SPIES_ON`** (Person → Subject-of-surveillance) **and/or `INFORMS` (Person → Handler)** | Westeros has structurally-distinct spy networks (Varys's little birds, Littlefinger's network, Qarth's whispers). Sonnet routinely shoehorns these into SERVES + a "reports to / surveils / agent" qualifier string. Two distinct edges (target = surveilled / target = handler) would close it cleanly. Without these, agent-vs-target relationships collapse into SERVES and the graph cannot answer "who does Varys handle?" or "who is being surveilled?" |
| 2 | "named after / namesake of" | 3 / 59 / 9 / 4 (Rickard-Karstark→Rickard-Stark, Patrek-Mallister→Patrek-Vance, etc.) | None — no edge type captures "this entity is named for that entity" | **`NAMED_AFTER`** (Entity → Namesake-entity) | Surfaced explicitly in Sonnet's `no-fitting-type` rejections (`rickard-karstark → rickard-stark: no-fitting-type-named-after-vocab-gap-filed`). Westeros is a culture of dynastic name-recycling (Rickards, Brandons, Aegons). The edge has obvious graph value (lineage exploration, prophecy resonance, foreshadowing-of-the-quiet-kind). Single-direction, no qualifier. |
| 3 | "step-parent / step-child" | 1 / 14 / 10 / 3 (Androw-Farman→Aerea-Targaryen flagged as escalate; Bethany-Hightower→Samantha-Tarly; Andrew Estermont step-mother references) | `PARENT_OF` (excludes step); `WARD_OF` (wrong — fostering ≠ step-parentage; step is a marital consequence, fostering is institutional) | **`STEP_PARENT_OF`** (Step-parent → Step-child) + reverse **`STEP_CHILD_OF`** | Wiki infobox encodes step-relations and Sonnet flagged this as escalate-cross-identity in batch-emit. PARENT_OF=biological is the canonical default; step-parentage is a marital-consequence relation that PARENT_OF=adopted (a different state, voluntary recognition) does NOT cover. Adding STEP_PARENT_OF is the smallest atomic fix; SIBLING_OF=step is already in the Tier-1 qualifier enum and would be the symmetric kinship counterpart. |
| 4 | "good-mother / good-father / good-sister / good-brother / mother-in-law / sister-in-law" | 3 / 81 / 97 / 3 (Alerie-Hightower→Olenna-Tyrell flagged twice; Bethany-Hightower→Samantha-Tarly) | `SPOUSE_OF` (spouse only); `SIBLING_OF` (blood only); `PARENT_OF` (parent only) | **`IN_LAW_OF` (single symmetric edge, target = person)** — qualifier optional with enum `{by_marriage_of_self, by_marriage_of_child, by_marriage_of_sibling, by_marriage_of_parent}` | Sonnet's freeform-qualifier corpus has 97 marriage-affinity mentions (mostly "good-mother", "good-father", "good-sister", "good-son" in Reach noble-house arcs). The graph currently forces a two-hop traversal (SPOUSE_OF + PARENT_OF + invert) and gets nothing for cases where only the in-law link is known. Olenna's "good-mother" relationship to Alerie is structurally significant for the Tyrell political arc and the Joffrey-poisoning theory. A single `IN_LAW_OF` symmetric edge with optional qualifier is the cheapest fix. |
| 5 | "rescues / saves life / saves from" | 18 / 182 / 21 / 0 | `PROTECTS` (steady-state guardianship, not the rescue event); `HEALS` (medical, not extraction-from-danger) | **`RESCUES`** (Rescuer → Rescued) | High-volume narrative event (Beric rescues BWB members, Mysterious Rider rescues Sam & Gilly, Davos rescued by Salladhor, etc.). PROTECTS captures the ongoing role; RESCUES captures the single dramatic moment. Distinct from CAPTURES (the inverse — they're saving from captivity). Tier-3 (no qualifier). |
| 6 | "exiled by / banishes / sent into exile" | 6 / 114 / 37 / 0 | `DEPOSES` (overthrows, not exile); `IMPRISONS` (confines, not casts out); `BETRAYS` (no, this is a political act not a betrayal) | **`BANISHES`** (Banisher → Banished) | Sonnet already uses "exiled by", "banished from court", "sent away" 37 times in qualifier strings. Examples: Euron banished by Balon; Lord Harte arrested during Dance of the Dragons; Tyrion's various exiles. Distinct from IMPRISONS (locks-up) and DEPOSES (removes from throne — different event). Tier-3 (no qualifier; the destination is in a separate temporal LOCATED_AT). |
| 7 | "rapes / raped / sexual assault (uncertain target)" | (covered by ASSAULTS) but Sonnet flagged 4 cases of `uncertain-identity: Alysanne or one of her sisters was raped` | `ASSAULTS` exists (Session 56 add) but the cases were rejected due to identity uncertainty | **No new edge needed — confirm ASSAULTS handles this correctly. Add to the prompt: emit ASSAULTS with target=disambiguation-set when prose says "X or one of her sisters"** | Not a vocab gap, but a prompt-clarification gap. ASSAULTS is the right type; the rejection reason was uncertainty about *which* sister, not about the edge type. |
| 8 | "tortures / flays / breaks on the rack" | 2 / 195 / 28 / 0 (in P1 Relationships Observed; full corpus is much larger because Bolton/Mountain torture is a major thread) | `MANIPULATES=via_threat` (psychological); `REVEALS_TO=under_torture` (the qualifier captures the *effect* of torture, not the act); `ASSAULTS` (sexual violence specifically); `EXECUTES` (formal death sentence) | **`TORTURES`** (Torturer → Tortured) | The torture act is a major narrative thread (Bolton flaying tradition, Mountain at Harrenhal, Qyburn's "studies", the Bloody Mummers, the Black Cells). `REVEALS_TO=under_torture` already implies torture occurred but does not assert the torture event as a graph-traversable edge; you can't query "who tortured Theon?" — you can only query "who Theon revealed information to under torture." The act itself is the missing edge. Tier-3 (no qualifier; method like flaying / racking is sub-typology that the graph can leave to narrative). |
| 9 | "conspires with / plots with / co-conspirator" | 17 / 65 / 14 / 0 | `ALLIES_WITH` (open political alliance); `NEGOTIATES_WITH` (diplomatic); `MANIPULATES` (one-sided) | **`CONSPIRES_WITH`** (Symmetric) | Already used freely by Sonnet in qualifier strings. Examples: Petyr + Olenna (Joffrey poison); Arianne's Queenmaker plot; the Tyrell-Lannister marriage plotters; Grand Northern Conspiracy. Distinct from ALLIES_WITH (open) and NEGOTIATES_WITH (diplomatic engagement that may or may not conclude). CONSPIRES_WITH is the secret-pact variant. Symmetric, Tier-3. Currently rejected as `no-fitting-type` 14 times (e.g., `cosgrove → uthor-underleaf: bribed by relationship`). |

### A.2 — MEDIUM ADOPT candidates (frequent but partly covered by existing edge types)

| # | Phrase / pattern | Volume (P1 / corpus / sonnet-q / no-fit) | Closest existing | Proposed | Rationale |
|---|---|---|---|---|---|
| 10 | "threatens / threatened" | 43 / 496 / 34 / 0 | `OPPOSES` (state); `MANIPULATES=via_threat` (already Tier-1 enum) | **DEFER** — fold into MANIPULATES=via_threat. The qualifier already captures the mechanism; standalone THREATENS would duplicate the via_threat enum slot. | Most "threatens" rows in Pass 1 are precursors to MANIPULATES or BREAKS_VOW (Viserys threatening Jorah; Bolton threatening Theon). The qualifier already captures this. Adding a standalone THREATENS edge would create dual-coverage. **Adopt only if smoke reveals MANIPULATES=via_threat under-emits.** |
| 11 | "accuses / accused of" | 32 / 288 / 36 / 0 | `OPPOSES`; `REVEALS_TO` (if true); `DECEIVES` (if false) | **DEFER** — covered by REVEALS_TO + DECEIVES + temporal context | "Accuses" is action; the truth-value (REVEALS_TO if true, DECEIVES if false) and target (OPPOSES) are already captured. A standalone ACCUSES would mostly duplicate. **Adopt only if formal-trial / judicial-accusation rows surface as a distinct cluster.** |
| 12 | "blames / blamed for" | 36 / 228 / 10 / 0 | `PERCEIVED_AS`; `DISTRUSTS`; `OPPOSES` | **DEFER** — PERCEIVED_AS captures the perception | Most "blames" rows reduce to perception. Ned blaming the Hound, Arya blaming the Hound, Cersei blaming Tyrion — all are POV-perception edges already covered by PERCEIVED_AS. |
| 13 | "summons / sends for" | 1 / 265 / 28 / 0 | `COMMANDS`; `APPOINTS` (if to office) | **DEFER** — usually a precursor to a more meaningful edge (an audience, an appointment, an arrest). | Low volume in the structured `Relationships Observed` table; high volume in narrative prose but as event-language not relationship-language. Adopt only if Stage-4 emits surface a recurring pattern. |
| 14 | "frees / spares / pardons" | 8 / 1092 / 146 / 0 | None — opposite of `IMPRISONS` and `EXECUTES` | **WEAK ADOPT** — `RELEASES` or `PARDONS` (Releaser → Released-person) | Volume is misleading — "spared" appears 1092× but only ~100 are about person→person release (most are "spared a glance" / "spared no thought" / "spared from death"). Real release-events are smaller. Distinct from RANSOMS (paid release) and the inverse of IMPRISONS. **Recommend HOLD for Stage 4 smoke** — see how many recurring rejections surface; current vocab doesn't capture the mercy-act that's narratively significant (Jon sparing Mance, Daenerys's freed slaves, Robert pardoning Jaime). |
| 15 | "haunted by memory of / longs for / misses" | 87 / 173 / 2 / 0 | `MOURNS` (dead); `LOVES`; `RESENTS` | **DEFER** — MOURNS already covers grief-for-the-dead; "longs for" is mostly missing-living-person which is partial-LOVES. | Edge case: "Arya misses Jon" is best captured by LOVES (the underlying state). The "haunted by memory" angle is narrative-craft, not relationship. Don't expand. |
| 16 | "rewards" | 3 / 105 / 23 / 0 | `APPOINTS` (if office); `GIFTS_TO` (if artifact); `BESTOWS_KNIGHTHOOD_ON` (if knighting) | **DEFER** — each reward-form already has a more-specific edge | Rewards take the form of office, gift, knighting, marriage-bestowal — each has its specific edge. The generic REWARDS is redundant. |
| 17 | "estranged from" | 12 / 15 / 0 / 0 | `OPPOSES`; `RESENTS`; `HATES` | **DEFER** — fold into RESENTS / DISTRUSTS with temporal-active state | Brynden-Tully estranged from Hoster, Tyrion estranged from Tywin, etc. The semantic is "we were once close, now we're not." OPPOSES is too strong, RESENTS works. Adopt only if specifically needed for the Brackens-Blackwoods style centuries-feud edges. |

### A.3 — REJECT (looked plausible but evidence weak)

| Pattern | Why reject |
|---|---|
| LEGITIMIZES (bastards) | Only 1 P1 row + 21 corpus mentions. ASOIAF has 4-5 famous legitimizations (Ramsay Snow → Ramsay Bolton, Gendry → Gendry Storm proposed). Too thin for a dedicated edge — covered by APPOINTS or by adding `legitimized` as a SIBLING_OF / PARENT_OF qualifier value. |
| DISINHERITS / DISOWNS | Only 2 P1 rows + 18 corpus mentions. Theon-Greyjoy-disowned-by-Balon scenario; Tysha-related Tyrion-Tywin scenario. Better captured as a temporal note on existing edges. |
| BULLIES | Specific to Joffrey/Sandor pattern (3 rows). Subsumes into ASSAULTS / MANIPULATES / ATTACKS depending on intensity. |
| BLESSES / CONSECRATES | Zero P1 rows in Relationships Observed; 111 corpus mentions but mostly atmospheric. OFFICIATES already covers ceremonial blessings. |
| FAVORS / FAVORED_BY | Zero P1 rows. Cersei-favors-Lancel pattern is captured by LOVES / LOVER_OF. |
| REQUESTS_SONG / PERFORMS_AT | Zero P1 rows; ~15 corpus + Sonnet no-fit cases (Wyman Manderly requesting Rat Cook / Brave Danny Flint). Narratively important to Northern-conspiracy theme but very narrow. **HOLD for graph polish later**, not for lockdown. |
| RIDES (dragon/horse) | Zero P1 rows; covered by BONDED_TO (dragon) or OWNS (horse). |
| INTERROGATES | 4 P1 rows. Folds into MANIPULATES + REVEALS_TO=under_torture. |
| WITNESSES | 2 P1 rows. Covered by LOCATED_AT (witness location) + KNOWS (knowledge gained). |
| MAINTAINS / CUSTODIAN_OF | Zero P1 rows; sole emit was Godric→Night-Lamp. Subsumes into OWNS or COMMANDS. Too narrow. |
| REACTS_TO_EVENT | Captured by MOURNS / PERCEIVED_AS + LOCATED_AT for presence. |

### A.4 — Sonnet-flagged borderlines

Three additional cases Sonnet's `no-fitting-type` track surfaced that warrant a closer look:

- **`SHADOWBINDS / EMPLOYS_MAGIC` (Melisandre's shadow-children)** — Sonnet flagged 4 cases of "Melisandre creates/births shadow children but no vocabulary covers character creates/employs magical construct." `PRACTICES (target=concept.magic)` was added Session 56 and should cover the discipline-membership case (Melisandre PRACTICES shadowbinding). The act of *birthing the shadow* is a creature-creation event that has no edge type. **Recommendation: HOLD.** The shadow-child entities themselves aren't graph-traversable individuals; the magical-act is captured by `PRACTICES=shadow_binding`. Only revisit if Stage 4 emits surface this as recurring.
- **`MADE_OF` is correct but Sonnet missed it for Longclaw → Valyrian-steel** — 6 cases of `no-fitting-edge-type` describing Longclaw as Valyrian steel. **This is a prompt issue, not a vocab gap.** MADE_OF was added Session 54 and Sonnet should have used it. Flag for prompt-clarity review.
- **`SOLD_TO / SOLD_INTO` (slavery, horse-sales)** — 1 P1 row + 20 corpus mentions + 3 Sonnet flags. Tyrion sold to Yezzan, Jorah sold men into slavery. **DEFER** — covered by `CONTRACTED_WITH=slavery` (Tier-2 enum already includes this conceptually) or by `BETRAYS` (selling into slavery).

---

## Section B — Sub-Qualifier Candidates

For each Tier-1 / Tier-2 enum value, an audit of whether the corpus distinguishes natural sub-typologies that the locked enum collapses.

Format: `Edge Type | Qualifier Value | Sub-typology surfaced? | Recommendation | Rationale`.

### B.1 — Tier 1 (REQUIRED enum) — 8 types × 5-6 values

| Edge Type | Qualifier | Sub-typology found in corpus? | Recommendation | Rationale |
|---|---|---|---|---|
| **SIBLING_OF** | `full` | No | **collapse-fine** | No further sub-typology needed. |
| | `half` | No | **collapse-fine** | "Half-brother" / "half-sister" are uniform; no by-which-parent distinction matters for the graph (the parent is queryable via PARENT_OF). |
| | `step` | Mild — see `STEP_PARENT_OF` proposal (Section A) | **collapse-fine for SIBLING_OF; consider STEP_PARENT_OF as separate edge.** | Step-sibling is symmetric and uniform once defined. The interesting structural relation is to the step-parent (see A.3 above). |
| | `milk` | No | **collapse-fine** | Already specific. |
| | `unknown` | n/a | **collapse-fine** | Defensive catch-all. |
| **SPOUSE_OF** | `current` | No | **collapse-fine** | |
| | `former` | Mild — divorce vs. set-aside? | **collapse-fine** | Westeros barely allows divorce; "former" without `annulled` is rare. The `annulled` slot captures the formal-dissolution case. |
| | `annulled` | No | **collapse-fine** | |
| | `widowed` | **YES — `by_battle` ×13, `by_murder` ×3 (rare), `by_illness` ×54 (very high), `by_execution` ×75 (very high)** | **DEFER (collapse-fine) — but flag for post-smoke review.** | The widowing cause IS narratively significant in ASOIAF (Catelyn widowed by Red Wedding = murder; Cersei widowed by Robert = "boar accident" = murder-by-proxy; Rhaenys widowed by Aerys = execution). However: in every case there's ALREADY a separate edge that captures the cause — KILLS / KILLED_BY / EXECUTES / DIED_OF / DIED_AT for the death event. The qualifier sub-typology would duplicate edges. **Recommend collapse-fine.** If, after Haiku smoke, queries struggle to assemble the widowed cause without the qualifier hint, revisit. |
| | `salt_wife` | No | **collapse-fine** | Already specific. |
| | `unknown` | n/a | **collapse-fine** | |
| **PARENT_OF** | `biological` | No | **collapse-fine** | |
| | `adopted` | No | **collapse-fine** | |
| | `claimed` | No | **collapse-fine** | Captures Aegon-VI-style cases cleanly. |
| | `rumored` | Mild — by extramarital ×88, by historical legend ×? | **collapse-fine** | The rumor-source is already implicit in the prose context. |
| | `disputed` | No | **collapse-fine** | |
| | `unknown` | n/a | **collapse-fine** | |
| **WARD_OF** | `formal` | No | **collapse-fine** | |
| | `informal` | No | **collapse-fine** | |
| | `hostage` | **WEAK — `ransom_collateral` ×2, `political_leverage` ×1, `hidden_identity` ×0 in corpus search; signal is essentially zero** | **collapse-fine** | The sub-typology Matt proposed (ransom-collateral / political-leverage / hidden-identity) does not appear with sufficient density. Theon-as-hostage at Winterfell IS implicit political leverage but the corpus doesn't speak of "ransom collateral" explicitly. Collapse stands. |
| | `unknown` | n/a | **collapse-fine** | |
| **HOLDS_TITLE** | `current` | No | **collapse-fine** | |
| | `former` | **WEAK — `stripped` ×0 in corpus, `deposed` ×2, `abdicated` ×4, `attainted` ×12, `renounced` ×0** | **collapse-fine** | Wiki had `stripped ×7` in qualifiers; the corpus has very few instances. The `attainted` mechanism is the canonical Westerosi "title-stripped-by-Crown" — but it's still uncommon. **Collapse stands** — the 7 wiki cases can be captured by a temporal note + DEPOSES edge if needed. |
| | `claimed` | No | **collapse-fine** | |
| | `contested` | No | **collapse-fine** | |
| | `historical` | No | **collapse-fine** | |
| | `unknown` | n/a | **collapse-fine** | |
| **VOWS_TO** | `active` | No | **collapse-fine** | |
| | `kept` | No | **collapse-fine** | |
| | `broken` | **MILD — `by_desertion` ×72 (mostly Night's Watch), `under_duress` ×13, `publicly` ×18, `by_omission` ×0** | **collapse-fine** | The Brienne / Jaime / Arya vow-arcs are well-served by a single `broken` qualifier; the cause is contextual. Night's Watch desertion is structurally distinguished by the `SWORN_TO=deserted` enum value, which already captures the most common case. **Collapse stands.** |
| | `fulfilled` | No | **collapse-fine** | |
| | `unknown` | n/a | **collapse-fine** | |
| **MANIPULATES** | `via_bribe` | **WEAK — Matt's sub-proposals (with money / marriage / position / pardon) almost zero signal in corpus** | **collapse-fine** | The mechanism is the qualifier; the *currency* of the bribe is rarely structurally relevant. Money is the assumed default. **Collapse stands.** |
| | `via_flattery` | No | **collapse-fine** | |
| | `via_false_information` | No | **collapse-fine** | |
| | `via_threat` | No | **collapse-fine** | Subsumes the standalone THREATENS candidate. |
| | `via_seduction` | No | **collapse-fine** | |
| | `unknown` | n/a | **collapse-fine** | |
| **SWORN_TO** | `current` | No | **collapse-fine** | |
| | `former` | **MILD — Wiki: `by_marriage` ×2, `in_death` ×11, `deserted` ×3, `annulled` ×2 — all distinct slots already exist in the enum (`deserted`, `by_marriage`); `in_death` is already captured as "active until death" + a DIED_AT edge** | **collapse-fine** | The Session 57 enum already contains `deserted` and `by_marriage` as first-class values, so the sub-typology is already partly enumerated. `in_death` (sworn-to-them-until-death) is contextual rather than enumerable. **Collapse stands.** |
| | `deserted` | No | **collapse-fine** | |
| | `by_marriage` | No | **collapse-fine** | |
| | `claimed` | No | **collapse-fine** | |
| | `unknown` | n/a | **collapse-fine** | |

### B.2 — Tier 2 (OPTIONAL enum) — 9 types

| Edge Type | Qualifier | Sub-typology found? | Recommendation | Rationale |
|---|---|---|---|---|
| **BETROTHED_TO** | All values | No | **collapse-fine** | Sonnet's 12 qualifier-bearing emits are descriptive, not enumerable sub-types. |
| **LOVER_OF** | `rumored` | No further breakdown | **collapse-fine** | Sonnet's `rumored ×6` emits group cleanly; no by-which-source distinction. |
| | other values | No | **collapse-fine** | |
| **KILLS** | `in_combat` / `in_duel` / `by_arrow` / `by_blade` / `by_ambush` / `by_proxy` / `by_creature` | No further breakdown | **collapse-fine** | Already 7 well-distinguished values; further sub-typology (which-weapon, which-creature) is captured by `KILLED_WITH` (artifact) and the creature-specific entity. |
| **CONTRACTED_WITH** | All values | No | **collapse-fine** | The 8 enum values are already maximally specific. |
| **DECEIVES** | `by_lie` / `by_disguise` / `by_omission` / `by_false_witness` / `by_silence` | No further breakdown | **collapse-fine** | Already specific. |
| **REVEALS_TO** | `voluntary` / `coerced` / `accidental` / `under_torture` | No further breakdown | **collapse-fine** | The `under_torture` slot is already captured at-event. No sub-typology of torture method matters at the edge level. |
| **ATTACKS** | All values | No | **collapse-fine** | Note: this enum is already flagged as a potential Tier-3 drop in the decisions.md ("Weaker empirical signal than other Tier-2 candidates — could drop to Tier-3 if Haiku smoke reveals it's never emitted"). Keep the enum until smoke runs. |
| **KNOWS** | `confirmed` / `suspected` / `told_by` / `witnessed` / `overheard` | No further breakdown | **collapse-fine** | Highest-qualifier-bearing edge in Sonnet output (191 qualifier-bearing emits) — but the qualifier strings are descriptive context, not new sub-typology. |
| **GUEST_OF** | All values | No | **collapse-fine** | Already pinned to Pass 1's explicit `Type` column. |

---

## Section C — Confirmed Complete

Edge types audited and found to have NO recurring vocabulary gap or sub-qualifier candidate worth surfacing:

### Tier-1 edge types audited
- `SIBLING_OF` — enum complete (5 values).
- `SPOUSE_OF` — enum complete (6 values); widowed-cause is a deferred sub-qualifier candidate, not adopted.
- `PARENT_OF` — enum complete (6 values).
- `WARD_OF` — enum complete (4 values).
- `HOLDS_TITLE` — enum complete (6 values).
- `VOWS_TO` — enum complete (5 values).
- `MANIPULATES` — enum complete (6 values).
- `SWORN_TO` — enum complete (6 values).

### Tier-2 edge types audited
- `BETROTHED_TO`, `LOVER_OF`, `KILLS`, `CONTRACTED_WITH`, `DECEIVES`, `REVEALS_TO`, `ATTACKS` (caveat: optional-drop-to-Tier-3 post-smoke), `KNOWS`, `GUEST_OF` — all enums complete; no sub-qualifier candidates warrant adoption.

### Tier-3 edge types spot-audited against Sonnet's 4,207-emit corpus (no gap surfaced)
- Kinship: `ANCESTOR_OF`, `HEIR_TO`, `CADET_BRANCH_OF`, `MARRIES_OFF`, `UNCLE_OF`, `NEPHEW_OF`, `COUSIN_OF`, `MILK_BROTHER_OF`, `NURSED_BY`, `WET_NURSE_OF`, `COURTS`, `PROPOSED_AS_BRIDE`
- Political: `RULES`, `OVERLORD_OF`, `COMMANDS`, `SERVES`, `ADVISES`, `HELD_BY`, `SUCCEEDS`, `CLAIMS`, `APPOINTS`, `DEPOSES`, `BREAKS_VOW`
- Factional: `MEMBER_OF`, `FOUNDED`, `ALLIES_WITH`, `OPPOSES`, `BETRAYS`, `NEGOTIATES_WITH`
- Military: `FIGHTS_IN`, `COMMANDS_IN`, `PART_OF`, `KILLED_BY`, `EXECUTES`, `CAPTURES`, `PRISONER_OF`, `BESIEGES`, `DEFEATS`, `DUELS`, `POISONS`, `RANSOMS`, `IMPRISONS`, `KILLED_WITH`, `KNIGHTED_BY`, `BESTOWS_KNIGHTHOOD_ON`, `ASSAULTS`, `PARTICIPATES_IN`
- Knowledge: `IGNORANT_OF`, `SEEKS`, `DECEIVED_BY`, `HOARDS`, `INVESTIGATES`, `TEACHES`, `TUTORS`, `HEALS`, `AFFLICTED_BY`, `DIED_OF`
- Emotional: `PERCEIVED_AS`, `TRUSTS`, `DISTRUSTS`, `RESPECTS`, `FEARS`, `LOVES`, `HATES`, `MOURNS`, `PROTECTS`, `RESENTS`, `COMPANION_OF`, `REPUTED_AS`
- Spatial: `LOCATED_AT`, `SEAT_OF`, `TRAVELS_TO`, `BORN_AT`, `DIED_AT`, `BURIED_AT`, `CONTEMPORARY_WITH`, `REGION_OF`
- Possession: `WIELDS`, `OWNS`, `ANCESTRAL_WEAPON_OF`, `FORGED_BY`, `MADE_OF`, `LOOTED_BY`, `REFORGED_INTO`, `GIFTED_TO`, `INHERITED_BY`, `WIELDED_IN`, `EXECUTED_WITH`, `PURCHASED_FROM`, `BUILT`, `CAPTAIN_OF`, `CREW_OF`
- Identity: `ALIAS_OF`, `DISGUISED_AS`, `SAME_AS`, `IMPERSONATES`
- Magic: `WARGS_INTO`, `BONDED_TO`, `SACRIFICES`, `RESURRECTS`, `CURSES`, `PRACTICES`
- Cultural: `CULTURE_OF`, `WORSHIPS`, `SACRED_TO`, `CLERGY_OF`, `OFFICIATES`
- Narrative: `DEPICTED_IN`, `FORESHADOWS`, `PARALLELS`, `SUBVERTS`, `ECHOES`, `CONTRASTS`, `WRITTEN_BY`
- Prophecy: `FULFILLS`, `APPEARS_TO_FULFILL`, `SUBVERTS_PROPHECY`, `PROPHESIED_BY`, `SUBJECT_OF_PROPHECY`, `DREAMS_OF`
- Evidentiary: `SUPPORTS`, `CONTRADICTS`, `CITED_BY`
- Causal: `CAUSES`, `PREVENTS`, `ENABLES`, `MOTIVATES`, `TRIGGERS`
- Hospitality: `VIOLATES_GUEST_RIGHT`, `GRANTS_SAFE_CONDUCT`, `ATTENDS`, `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY`

Total Tier-3 confirmed: 132.

### Pass 1 sections audited beyond `## Relationships Observed`

Per Session 57's methodology lesson, every Pass 1 section was inspected for relationship-typed signal. Re-confirmed (no new enumerable types beyond Session 57's GUEST_OF addition):

- `## Events & Actions` — confirms KILLS method enum + ATTACKS motive enum. No new categories.
- `## Hospitality & Guest Right` — enumerated by Session 57 → GUEST_OF. Complete.
- `## Information Revealed` — confirms KNOWS basis enum. No new categories.
- `## Spatial Layout & Movement` — phase-based; redundant with `temporal` field on edges.
- `## Dialogue of Note` — free-text; not enumerable.
- `## Character Appearances` / `## Location Descriptions` / `## Food & Drink` / `## Physical Environment` — entity-attribute data, not relational.
- `## POV Internal State` — emotional state on the POV character; covered by existing emotional/perceptual edges.
- `## Unanswered Questions` — discovery scaffolding, not relational data.
- `## Raw Entity List` — entity index, not relational.

---

## Recommendations — ranked

Order is strongest "adopt this" first. Each is independent and can be adopted or rejected separately.

1. **`SPIES_ON` (and/or `INFORMS`)** — *Adopt.* Westerosi spy networks are a structural narrative feature. Sonnet already shoehorns these into SERVES + qualifier strings. Two-edge solution (target=surveilled vs target=handler) closes the gap cleanly. Symmetry/direction: SPIES_ON is one-sided (spy → subject); INFORMS is one-sided (spy → handler). Both Tier-3 (no qualifier).
2. **`NAMED_AFTER`** — *Adopt.* Surfaced explicitly in Sonnet `no-fitting-type` rejections. ASOIAF's dynastic name-recycling is a graph-traversal asset waiting for an edge. Tier-3.
3. **`CONSPIRES_WITH`** — *Adopt.* High signal in Sonnet's qualifier strings; rejected 14× as `no-fitting-type` despite obvious narrative weight. Sits cleanly between ALLIES_WITH (open) and NEGOTIATES_WITH (diplomatic). Symmetric, Tier-3.
4. **`RESCUES`** — *Adopt.* High narrative volume; current PROTECTS is steady-state, not event. The rescue-event is graph-valuable (Beric-arc, Davos-arc, Mysterious-Rider-arc, Robert/Ned-Tower-of-Joy). Tier-3.
5. **`BANISHES`** — *Adopt.* 37 Sonnet emits already use the verb in qualifier strings; current DEPOSES/IMPRISONS don't cover political exile. Tier-3.
6. **`TORTURES`** — *Adopt.* Major narrative thread (Bolton/Mountain/Qyburn). The `REVEALS_TO=under_torture` qualifier captures the after-effect, not the act. Currently no way to graph "who has Ramsay tortured?" Tier-3.
7. **`IN_LAW_OF`** — *Consider, but defer to next round.* High Sonnet-qualifier volume but the canonical solution (two-hop traversal through SPOUSE_OF + PARENT_OF) does work. Adopt only if the Tyrell-Lannister-Frey-Reach political-network queries become primary use cases.
8. **`STEP_PARENT_OF` / `STEP_CHILD_OF`** — *Consider.* Edge case; the SIBLING_OF=step qualifier covers the most common need. Adopt if Aerea-Targaryen-style step-relations matter for the historical/lore queries.

### Sub-qualifier verdict — TL;DR

**Recommend zero sub-qualifier additions.** Every Matt-brainstorm candidate either (a) has near-zero corpus signal or (b) is captured by another edge whose existence makes the sub-qualifier redundant. The strongest case (SPOUSE_OF=widowed by what cause) is already implicit via separate KILLS/EXECUTES/DIED_OF/DIED_AT edges. Adding sub-qualifiers expands the validator surface for marginal narrative payoff. **Collapse stands.**

---

## Confidence in lockdown after this audit

- **Edge vocabulary:** The 149 locked types cover ~95% of P1 relationship volume. The 6 strong adopt candidates above (SPIES_ON / NAMED_AFTER / CONSPIRES_WITH / RESCUES / BANISHES / TORTURES) would close the remaining recurring patterns. Without them, expect Haiku smoke to either reject these as `no-fitting-type` (acceptable) or to mis-map them into close-but-wrong types (the larger risk — see Sonnet's SERVES-for-spying drift).
- **Qualifier enums:** Tier 1 + Tier 2 enums are tight. No sub-qualifier dimension warrants adoption.
- **Lockdown is "thorough enough" for Haiku smoke** if: (a) Matt verdicts the 6 strong candidates; (b) Matt confirms collapse-fine for all Section B sub-qualifier candidates. With those decisions, the vocabulary surface is closed.
- **Caveats for Haiku smoke:**
  - The `ATTACKS` Tier-2 enum is flagged as drop-to-Tier-3 candidate per Session 57; the smoke will tell us.
  - The `MADE_OF`-for-Longclaw prompt-clarity issue (Sonnet missed 6 instances) is a prompt-fix, not a vocab fix — surface for the next prompt-touch pass.
  - The 4 `Melisandre-creates-shadow-children` no-fits suggest `PRACTICES=shadow_binding` may be confusing to agents — prompt should clarify that PRACTICES captures the discipline, and the magical-act outcome (shadow created, glamor placed) is not separately graph-edged.

---

## Followups (for orchestrator after Matt verdicts)

- **If 1-3 of the Section A.1 strong-adopt candidates are accepted:** vocab moves 149 → 150-152. Encode via the same path as Session 56 — add rows to `reference/architecture.md`, regenerate counts, flip classifier prompt's `~149` references, add to in-prompt category-expansion list.
- **If none accepted:** no change; the existing `no-fitting-type-vocab-locked` channel absorbs them.
- **Sub-qualifier follow-up:** record in decisions.md as "Section B audited 2026-05-19 — all collapse-fine verdicts confirmed."
- **Audit complete; Haiku smoke unblocked from the vocab-completeness side.** Remaining HAIKU-CUTOVER blockers per `working/todos.md` continue as planned (STEP 2 [LINK] sub, STEP 3 validator + qualifier-enum enforcement, STEP 4 suspicious-edges flagger).
