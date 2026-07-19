# Extraction Quality Audit — The Mystery Knight (TMK)
**Audit Date:** 2026-07-19  
**Auditor:** Mechanical QA agent (cold review)  
**Extraction Runs:** TMK Dunk-01 parts 1–9 (9 scene splits via claude -p, Opus)  
**Smoke Status:** No prior smoke test (THK/TSS smoke passed; TMK relies on inherited prompt v4)

---

## VERDICT
**PASS-WITH-CONCERNS**

The TMK extraction run is mechanically sound on 6 of 7 audit criteria. **Critical finding:** relationship vocabulary is being misapplied to tournament epithets (treating "the Gallows Knight" and "the Knight of the Pussywillows" as identity reveals when they are temporary honorifics, not concealed identities). This violates the prompt's controlled-vocabulary spec and should be corrected before Stage 4 ingestion. All other structural and content rules passed cleanly. **Root cause:** the SAME_AS/ALIAS_OF boundary is ambiguous in the prompt when a character is called by a descriptive epithet in-unit.

---

## DETAILED FINDINGS

### 1. LOCKED VOCABULARY — PASS
- **All 9 parts:** 100% of Relationship column cells use controlled UPPER_CASE types from the prompt's curated edge-vocabulary set (DEFEATS, SERVES, KILLS, CAPTURES, SAME_AS, ALIAS_OF, etc.)
- **No free-text relationships:** zero instances of invented pseudo-labels like "contempt toward," "bonded to," or "acts as body-double for"
- **No NEEDS_VOCAB gaps:** every real relationship fit an existing type; no gap-hatches needed
- **Qualifiers applied:** required qualifiers present where applicable (e.g., `WARD_OF (hostage)`, `KILLS (by_blade)`, `DECEIVES (by_lie)`, `PARENT_OF (biological)`)
- **Example:** p05 line 266: `Ser Uthor Underleaf | DEFEATS | Dunk | "Uthor's iron fist took him square between his eyes"` ✓

### 2. FORWARD-ONLY DIRECTION — PASS
- **Semantic agent rule enforced:** Column A consistently holds the actor (killer, parent, deceiver, etc.), never the passive recipient
- **No double-emission of symmetric types:** SIBLING_OF, SPOUSE_OF, SAME_AS recorded once in either order ✓
- **Reverse types absent:** no NEPHEW_OF, CHILD_OF, STEP_CHILD_OF, or other inverse forms detected
- **Example:** p09 line 259: `Brynden Rivers | CAPTURES | Daemon Blackfyre II | "his men ... pulled him off his horse, and clasped him into golden fetters"` — agent (Rivers) in Column A ✓

### 3. ISOLATION & TRAINING-KNOWLEDGE LEAK — PASS
- **Part-mode execution verified:** each of p01, p05, p09 (deep sample) contains ONLY text that appears in its own source file or is explicitly Dunk's recalled internal narration
- **No main-saga bleed:** characters from AGOT/ACOK/etc. not invented into the text; cross-series knowledge not injected
- **Intra-unit recall allowed correctly:** p05 references "Ser Arlan used to say" (Dunk's memory ✓), p06 recalls Ashford Meadow joust (text explicitly references it ✓), p09 depicts the Redgrass Field vision (in-narration ✓)
- **Example from p01 source review:** Dunk's recollection of Bloodraven's appearance (white skin, red eye, winestain mark, lost eye to Bittersteel) — all stated in p01's septon sermon and Dunk's narrative thought, not external knowledge injection

### 4. NO INTERPRETIVE LEAK — PASS
- **Banned qualifiers absent:** zero instances of `symbolic`, `implicit`, `ironic`, `foreshadows`, `represents`, `thematically`, `narrative weight`, `(implicit)` across all 9 files
- **Table cells factual only:** no editorial commentary explaining extractor's choice instead of stating facts
- **Evidence sentences clean:** examples: "He had not liked his flinty eyes" → captures perception, not editorialism ✓
- **Raw Entity List bare-name rule enforced:** all 12 categories list entity names only; no parenthetical hedging except `(inferred)` and `(uncertain — verify)`

### 5. IDENTITY REVEALS → SAME_AS — **PARTIAL PASS (1 major issue, 1 cross-part coordination note)**

**Issue A: Tournament Epithets Misclassified as Identity Reveals**

Two parts treat tournament-derived epithets (not concealed identities) as SAME_AS:
- **p05 line 287:** `Dunk | SAME_AS | the Gallows Knight` (evidence: herald's tournament epithet for his hanged-man shield)
- **p05 line 290:** `Glendon Ball | SAME_AS | the Knight of the Pussywillows` (evidence: herald's mocking tourney nickname)
- **p06 line 269:** `Dunk | SAME_AS | the Gallows Knight` (repeated from p05)
- **p06 line 271:** `Glendon Ball | SAME_AS | the Knight of the Pussywillows` (repeated from p05)

**Why this violates the prompt:**
The prompt defines SAME_AS for in-text identity reveals: "the bald stableboy 'Egg' is revealed in-text to be Aegon Targaryen" or "the old man is named Ser Arlan of Pennytree." These are hidden ↔ true identities. A tournament epithet is neither:
- Not hidden: "the Gallows Knight" is how he's announced by the herald publicly
- Not a true identity: it's a descriptive honor derived from his shield, not an alternate name he goes by
- Not a reveal: the reader and characters already knew his device; the epithet is just a stylized way to announce jousters

Proper example of a VALID identity reveal in the data:
- **p05 line 289:** `Glendon Flowers | SAME_AS | Glendon Ball` with evidence "I am Glendon Ball, not Glendon Flowers" — Glendon protests the herald's use of the bastard surname and states his true surname ✓ (this IS an identity correction)

**Remediation:** Remove the four epithet SAME_AS edges (p05 lines 287, 290; p06 lines 269, 271). These don't belong in Relationships at all — they're descriptive tournament nicknames, not character-identity data. If future design needs to capture "epithets used in the text," add a new optional-qualifier relationship type, but don't force-fit them into SAME_AS.

---

**Note B: Cross-Part Identity Duplication (minor coordination point, not a defect)**

Valid SAME_AS edges are recorded in multiple parts when each part's text independently contains the reveal:
- `Dunk | SAME_AS | Ser Duncan the Tall` appears in p01 (Egg: "This is Ser Duncan the Tall"), p05 (text: "Ser Duncan"), p06 (text: "Duncan the Tall")
- `Bloodraven | SAME_AS | Lord Brynden Rivers` appears in p03, p09

This is expected behavior when a part-mode run doesn't coordinate across parts. **Not a defect** — Stage 4's edge pipeline includes deduplication logic. Downstream will merge identical edges from different parts.

---

### 6. COMPLETENESS — PASS
- **All 12 Raw Entity List category headers present** in all 9 files, exactly as specified in the prompt, in correct order
- **Empty categories correctly marked "None"** (e.g., p01 Factions & Organizations, Cultures & Peoples, Religions & Faiths)
- **No renamed or omitted categories**
- **Section-checkpointing observed:** for long units like p05 (tournament sequences), physical environment, characters present, events all richly populated (not skimmed)

### 7. SEAM QUALITY — PASS
- **Each part extracts only its own text:** p01 covers Stoney Sept departure through road encounter; p05 tournament morning through evening; p09 pre-dawn tilt through afternoon judgment
- **No cross-part event absorption:** each unit's "Events & Actions" list stays within its narrative span
- **No forward/backward reference contamination:** mentions of "six days later" or "the wedding feast" are framed as recalled context, not absorbed into present events
- **Timeline coherence:** full run forms a continuous single-chapter narrative (9 parts = 1 chapter, "Dunk I")

---

## CROSS-PART CONSISTENCY CHECK (sample)

**Character naming:** Same character tagged consistently across parts where they appear:
- Dunk → Ser Duncan the Tall (p01, p05, p06, p09) ✓
- Egg → Aegon (consistent use of both names per reveal; p02–p09 after p01 intro) ✓
- Bloodraven → Brynden Rivers (introduced p02, used interchangeably p03, p07, p09) ✓
- Ser John the Fiddler → Daemon Blackfyre II (identity revealed p07, used both p08–p09) ✓

**No major naming drift detected** (e.g., Peake not tagged as "the sour lord" in one part and "Lord Gormon" in another — tags are consistent).

---

## "OTHER" BUCKET DISCIPLINE — PASS

Spot-check of Raw Entity List "Other" category (intended as a true catch-all for items not fitting the 11 named categories):

- **p01 "Other":** "Great Spring Sickness," "the drought," "Lord Butterwell's wedding" — all legitimately don't fit Artifacts/Locations/Wars (seasonal/abstract events mentioned in narration) ✓
- **p05 "Other":** "The tourney at Whitewalls," "The company of dwarfs" — again, event-references that don't fit canonical categories ✓
- **p09 "Other":** "None" — appropriate; all entities fit the 11 main categories ✓

No abuse of "Other" as a dumping ground for laziness. Proper restraint shown.

---

## CITE RESOLUTION — PASS

Every Relationships table cell's Evidence column contains a **short verbatim quote string** (clause-level, not line-numbered). Stage 4's deterministic locator can find these:
- p01 line 258: `"This is Ser Duncan the Tall, and I'm his squire."` ✓
- p05 line 266: `"Uthor's iron fist took him square between his eyes"` ✓
- p09 line 259: `"Lord Bloodraven's men surrounded him, pulled him off his horse, and clasped him into golden fetters"` ✓

No hand-authored line numbers; extraction correctly follows the "clean findable verbatim" guideline.

---

## DIREWOLF / DRAGON HANDLING (per architecture.md convention #8) — PASS

Named mounts and creatures:
- **Thunder** (Dunk's warhorse) — tagged as Artifact, not character ✓
- **Rain** (Egg's palfrey) — tagged as Artifact ✓
- **Maester** (the pack mule) — tagged as Artifact ✓
- **Dragons** — none present as characters in TMK; mentioned only as heraldic symbols or objects (dragon's egg as Artifact) ✓

Proper restraint; plot-load-bearing mounts correctly categorized as objects.

---

## STRAIN POINTS & RECOMMENDATIONS

1. **Epithet SAME_AS issue (BLOCKER for Stage 4 ingestion):**
   - **Files affected:** p05, p06 (4 edges)
   - **Fix:** Remove `Dunk | SAME_AS | the Gallows Knight` (both parts) and `Glendon Ball | SAME_AS | the Knight of the Pussywillows` (both parts)
   - **Effort:** sed-cleanup only (no re-extraction needed)
   - **Timing:** Pre-Stage 4

2. **Cross-part coordination (FYI, not a defect):**
   - Identity reveals correctly recorded in multiple parts where text justifies them
   - Stage 4 deduplication will handle merges
   - No action needed

3. **Potential future prompt refinement (not urgent):**
   - Add explicit boundary guidance to v4/v5: "SAME_AS is for hidden-identity reveals only. Tournament epithets, descriptive nicknames, and public honorifics do NOT qualify. Use the character's canonical name/title instead."
   - Consider adding an optional `CALLED_BY` type for non-identity descriptive names if future projects need epithet tracking

---

## SUMMARY

**Quality Grade: PASS-WITH-CONCERNS → PASS after remediation**

The extraction run demonstrates strong mechanical discipline:
- ✓ Controlled vocabulary enforced (zero free-text)
- ✓ Forward-only directionality respected
- ✓ Part-isolation maintained (no cross-saga leakage)
- ✓ No interpretive qualifiers
- ✓ All 12 entity categories present and complete
- ✓ Seam quality (no part bleeding across boundaries)
- ✓ Clean cite resolution

**One defect found and isolated:** 4 relationships (2 unique types, 2 parts) misclassify tournament epithets as identity reveals. **Remediation:** remove those 4 edges via sed; no re-extraction required. After cleanup, the run is **Stage-4-ready**.

**No other issues detected.**

---

**Recommended Next Step:**
1. Confirm and remove the 4 epithet SAME_AS edges (sed batch edit)
2. Run a quick schema validator on the cleaned files to confirm edge syntax
3. Pass to Stage 4 (edge classification + reification)

The prompt (v4) performed well; the extraction tool (Opus via claude -p) handled part-mode isolation correctly. This run can serve as a model for future D&E and main-saga part-split extractions.
