# Smoke Test Judge Report — THK Dunk I (v4)

**VERDICT: PROMOTE-READY**

The extraction is mechanically sound, schema-complete, and ready for production. All 8 checklist items pass. One minor observation on optional-qualifier capture noted below, but it reflects appropriate thoroughness per the v4 "expansiveness" mandate, not a defect.

---

## Checklist Results

### 1. LOCKED VOCAB HELD? ✅ PASS
- **Count:** 73 rows in Relationships Observed table
- **Violations:** 0
- All relationship types are from the controlled UPPER_CASE set (v4 prompt lines 186–201). No free-text pseudo-labels detected.
- Examples:
  - `SAME_AS`, `SIBLING_OF (full)`, `PARENT_OF (biological)` — kinship types ✓
  - `KILLS (in_combat)`, `DEFEATS`, `ATTACKS (in_anger)` — conflict types ✓
  - `DECEIVES (by_disguise)`, `DECEIVES (by_lie)`, `REVEALS_TO` — knowledge types ✓
  - `MEMBER_OF`, `COMMANDS`, `BANISHES` — authority types ✓

### 2. QUALIFIERS CAPTURED? ✅ PASS
- **Required qualifiers:** All present where applicable
  - `SIBLING_OF (full)` — 7 instances (Baelor/Maekar, Daeron/Aerion, Aerion/Egg, Aemon/Egg, etc.)
  - `PARENT_OF (biological)` — 6 instances (Maekar→Daeron/Aerion/Egg/Aemon, Baelor→Valarr, Daeron II→all four sons)
  - `WARD_OF (informal)` — Dunk/Ser Arlan (line 491)
  - `VOWS_TO (active)` — Dunk/Baelor (line 546)
  - `SWORN_TO (current)` — Maekar/Daeron II (line 558)
- **Optional qualifiers:** Actively captured where text-evident
  - `KILLS (in_combat)` / `KILLS (in_duel)` — 3 instances (Maekar→Baelor in combat; Beesbury killed in melee; Bracken slew Blackwood in duel)
  - `ATTACKS (in_anger)` — 2 instances (Aerion→Tanselle, Dunk→Aerion) ✓
  - `DECEIVES (by_lie)` / `DECEIVES (by_disguise)` — 2 instances (Daeron lied to Maekar; Egg disguised as stableboy) ✓

### 3. FORWARD-ONLY? ✅ PASS
- No inverse/mirror duplicates emitted
- Head rule correctly applied: semantic agent in Column A, not grammatical subject
  - Line 530: `Maekar | KILLS (in_combat) | Baelor` — Maekar is the semantic agent (wielded the mace), NOT the grammatical subject of "was killed." No inverse `Baelor | KILLED_BY | Maekar` ✓
  - Line 545: `Baelor | RESCUES | Dunk` — not mirrored as `Dunk | RESCUED_BY | Baelor` ✓
- Symmetric types (SAME_AS, SIBLING_OF, COUSIN_OF) emitted once in either order ✓

### 4. ISOLATION CLEAN? ✅ PASS
- No cross-novella knowledge (TSS/TMK not cited)
- No main-series facts (e.g., "this foreshadows Robert's Rebellion" — NOT present)
- No analytical edge types (FORESHADOWS, PARALLELS, ECHOES, CONTRASTS, FULFILLS, PROPHESIED_BY — all absent from Relationships table) ✓
- No spatial/possession/title/event-role edges (LOCATED_AT, WIELDS, HOLDS_TITLE, AGENT_IN — absent) ✓
- All facts scoped to THK text only
- Harvest sidecar correctly points (does not extract) forward-looking items like "prophecy" and "foreshadow-hook" ✓

### 5. NO INTERPRETIVE-QUALIFIER LEAK? ✅ PASS
- **Evidence cells:** All contain verbatim quotes or plain factual descriptions
  - No `symbolic`, `ironic`, `represents`, `thematically`, `narrative weight`, `(implicit)`
  - Example: Line 486: `"It's short for Aegon. My brother Aemon named me Egg."` — bare fact, no interpretive gloss
- **Raw Entity List:** No banned interpretive language detected
  - One sanctioned flag: `House Daffy (uncertain — verify)` on line 714 — correctly used for first-appearance uncertainty, not interpretation ✓
- **Event & Action entries:** Clean, factual, no editorializing (e.g., Event 27 states the fact: "Maekar kills Baelor with his mace" without "accidental" or "tragic" qualifiers) ✓

### 6. IDENTITY REVEALS → SAME_AS? ✅ PASS
- All major in-text identity reveals captured:
  - Line 486: `Egg | SAME_AS | Aegon Targaryen` — "It's short for Aegon. My brother Aemon named me Egg." ✓
  - Line 489: `Prince Daeron | SAME_AS | the dreaming lordling at the inn` — revealed when Daeron arrives with royal party ✓
  - Line 490: `Prince Baelor | SAME_AS | the black knight in Valarr's armor` — revealed when he lifts his visor (line 1309) ✓
  - Line 487: `Dunk | SAME_AS | Ser Duncan the Tall` — his self-invented knightly name ✓
  - Line 488: `Ser Arlan of Pennytree | SAME_AS | the old man` — burial-scene reveal ✓

### 7. HARVEST SIDECAR? ✅ PASS
- **Format compliance:** All 35 lines follow `{BOOK} / {anchor} / {kind} / {note}` structure
- **Kind values:** All from specified enum (`targaryen-history`, `prophecy`, `food`, `hospitality`, `cross-identity`, `foreshadow-hook`, `causal-spine`, `description`, `other`) ✓
- **No pre-flagging:** Entries are breadcrumbs pointing at saga-important details, not categorized entities
  - Example line 1: `THK / the bald stableboy "Egg" / cross-identity / Egg revealed in-text as Prince Aegon Targaryen...` — points to the reveal, does not extract or pre-categorize ✓
- **Causal spine breadcrumbs:** Lines 8–9, 29–34 clearly map within-novella cause→effect chains without typing them as edges (per prompt line 165–168) ✓

### 8. COMPLETENESS? ✅ PASS
- **All 12 Raw Entity List headers present and in order:**
  1. Characters (71 names, lines 573–644)
  2. Locations (33 locations, lines 646–684)
  3. Houses (27 houses, lines 686–720)
  4. Factions & Organizations (4 entries, lines 721–725)
  5. Religions & Faiths (3 entries, lines 727–730)
  6. Cultures & Peoples (5 entries, lines 732–738)
  7. Artifacts & Objects (25 entries, lines 740–764)
  8. In-world Texts & Songs (4 entries, lines 766–772)
  9. Magic & Phenomena (6 entries, lines 774–780)
  10. Wars & Conflicts (6 entries, lines 782–790)
  11. Titles & Offices (9 entries, lines 792–808)
  12. Other (5 entries, lines 810–814)

- **Final-third spot-check (trial of seven, Baelor's death, aftermath):**
  - **Events & Actions:** Events 17–29 (lines 311–397) comprehensively cover trial setup, recruitment (Hardyng, Beesbury, Rhysling, Lyonel, Raymun's knighting), Steffon's betrayal, Baelor's entry, the melee, Aerion's defeat, Maekar's mace strike, and aftermath offer of Egg as squire ✓
  - **Spatial Layout:** Lines 409–413 capture Assembly (defenders form line at south, accusers from north), Confrontation (charge and melee scatter across mud), Pursuit (Dunk drags Aerion to viewing stand), Dispersal (Baelor's body to funeral pyre), Departure (Dunk and Egg ride for Dorne) ✓
  - **Relationships Observed:** Trial participants and outcomes well-represented (e.g., Maekar KILLS Baelor, Dunk DEFEATS Aerion, Baelor RESCUES Dunk, Baelor VOWS_TO Dunk) ✓
  - **Dialogue of Note:** Key final-section speeches captured (Valarr's rebuke line 472, Maekar's argument lines 473–474, Dunk's "ARE THERE NO TRUE KNIGHTS AMONG YOU?" line 465) ✓
  - **Information Revealed:** Major trial and succession facts logged (lines 427–437) ✓

---

## Structural Integrity

✅ No truncation, no checkpoint restart seams, no duplicate sections.

- File flows coherently from opening (Arlan's burial) through trial to closing (departure for Dorne)
- Tables are complete and logically organized
- No mid-table restarts or orphaned rows
- Output totals 818 lines; the extraction was the second longer run (~107k output tokens) and shows good coverage commensurate with the 31,669-word source

---

## Strain Points & Observations

### 1. **Optional-qualifier proliferation (minor, not a defect)**
   The extraction captures optional qualifiers on ATTACKS, KILLS, DECEIVES freely: `ATTACKS (in_anger)`, `KILLS (in_combat)`, `KILLS (in_duel)`, `DECEIVES (by_lie)`, `DECEIVES (by_disguise)`. This is correct per the v4 prompt (lines 210–223: "actively capture these too"). However, it signals that the extractor is working at a high level of detail — every ATTACKS/KILLS instance gets a qualifier, not just the ambiguous ones. This is appropriate for a 32K-word unit where "more room" is budgeted (line 79 of the prompt: "Be slower and more thorough"), but it's worth noting that the normalized edge layer will need to handle the density of variant types downstream.

### 2. **One inferred relationship flagged, appropriately**
   Line 549: `Ser Manfred Dondarrion | DECEIVES (by_lie) | Dunk | "No. I know him not. Nor you, boy" — denying a master he served (inferred)`. The extractor flags the inference that Manfred is lying by denying knowledge of Dunk. The text shows Dunk recalling that Manfred once served at Lord Florent's seat (Dunk's destination on Arlan's travels), but it does not explicitly state that Manfred knew Dunk. The `(inferred)` flag is appropriate — this is a judgment call about whether denying knowledge of an orphan squire counts as deception or legitimate ignorance. The extractor chose to extract it but marked it `(inferred)`, which is correct handling of a borderline case.

### 3. **Identity-reveal disambiguation via Witness role**
   The extraction captures Witness roles for identity-reveal events (e.g., line 252: "Witness: Dunk" when Egg is caught riding Thunder in armor). This shows the extractor correctly interpreted the prompt's exception rule (line 92–101) — in-text identity reveals are allowed, and the extraction logs them as both the SAME_AS edge and as events where the reveal occurs. This is mechanically sound and supports cross-identity matching use cases (memory `user_asoiaf_design_values`).

---

## Verdict

**The extraction is production-ready.** It is schema-complete, vocab-locked, qualifier-rich, and isolation-clean. The five in-text identity reveals are captured correctly. Qualifiers are text-driven, not speculative. No analytical edges leak. No interpretive language contaminates the data. The final third of the source (trial, Baelor's death, aftermath) is comprehensively extracted. The harvest sidecar correctly points at saga hooks without pre-categorizing.

**Recommended action:** Accept for production pass.
