# TSS Extraction Judgment — v4

## Verdict

**PROMOTE-READY**

The extraction is mechanically sound, fully isolated, and complete to the end. All 54 relationship rows use locked controlled vocabulary. Late tables (Spatial Layout, Events 20–22, the final departure) are fully captured, not skimped. Identity reveals are properly tagged as SAME_AS. Harvest sidecar contains 21 proper breadcrumbs with no analytical extraction. No rule violations detected.

---

## Checklist Results

### 1. LOCKED VOCAB HELD — **PASS**
- **54 total relationship rows**; **0 violations**
- Every cell in the Relationship column is UPPER_CASE and from the prompt's controlled set
- Examples: `SAME_AS`, `SWORN_TO (current)`, `KILLS (in_duel)`, `ATTACKS (unprovoked)`, `PARENT_OF (biological)`, `SPOUSE_OF (widowed)`, `WARD_OF (hostage)`
- No free-text pseudo-labels, no invented types, no `NEEDS_VOCAB:` flags needed

### 2. QUALIFIERS CAPTURED — **PASS**
- All **7 required qualifiers** present where applicable:
  - `SIBLING_OF (full/half)` — lines 441, 443, 444, 447, 448
  - `SPOUSE_OF (current/widowed)` — lines 420, 431, 432
  - `PARENT_OF (biological/claimed)` — lines 421, 422, 430, 439, 440, 445, 446, 449, 450
  - `WARD_OF (hostage)` — line 438
  - `SWORN_TO (current/former)` — lines 407, 433, 434, 437
- Many **optional qualifiers** actively captured:
  - `KILLS (in_duel, by_arrow, by_blade)` — lines 412, 451–453, 456–458
  - `ATTACKS (unprovoked, in_anger)` — lines 413–414
  - `IN_LAW_OF (by_marriage_of_sibling)` — lines 428–429
- No `unknown` overuse; method/condition is evident from text

### 3. FORWARD-ONLY — **PASS**
- No inverse/mirror rows detected
- Column A correctly places the semantic agent, not grammatical subject or POV:
  - `Dunk KILLS Ser Lucas` (Dunk is killer, not victim) — line 412 ✓
  - `Bloodraven KILLS Daemon Blackfyre` (Bloodraven is killer) — line 451 ✓
  - `Egg RESCUES Dunk` (Egg is rescuer, not rescued) — line 417 ✓
- All entries emit once in agent direction; symmetric types (`SIBLING_OF`, `SPOUSE_OF`) emit once in either order without duplication

### 4. ISOLATION CLEAN — **PASS**
- No cross-unit leakage (no THK details, no TMK previews)
- No "dramatic irony" or "reader knows from elsewhere" commentary
- Identity reveals within TSS text only:
  - Egg revealed as Aegon Targaryen by narration + Dunk's signet ring show — line 366 ✓
  - Bloodraven revealed as Brynden Rivers by Septon Sefton's narration — line 370 ✓
  - Addam Osgrey as deceased past love revealed via Rohanne's dialogue with Dunk — captured in relationships ✓
- No analytical edge types (`FORESHADOWS`, `PARALLELS`, `PROPHESIED_BY`, etc.)
- No embedded Pass-4/5 interpretation

### 5. NO INTERPRETIVE-QUALIFIER LEAK — **PASS**
- Banned words scanned across all tables and Raw Entity List: **0 instances**
  - No `symbolic`, `ironic`, `foreshadows`, `represents`, `(implicit)` anywhere
  - No editorial explanations in table cells
- Raw Entity List entries are bare names only (e.g., "Dunk (Ser Duncan the Tall)" for humans; "The drought" for phenomena — all clean)
- Parenthetical qualifiers appear only in Relationships (controlled vocab enums) and isolated metadata flags (`(inferred)`, `(uncertain — verify)` — none present in this extraction)

### 6. IDENTITY REVEALS → SAME_AS — **PASS**
- **Egg ↔ Aegon Targaryen** (line 405):
  - Evidence: "Aegon of House Targaryen was the fourth and youngest son of Maekar… Egg might be a hedge knight's squire" (in-text reveal via narration + dragon signet disclosure)
  - Both names appear in Raw Entity List (lines 474–475) ✓
- **Bloodraven ↔ Brynden Rivers** (line 406):
  - Evidence: "Brynden Rivers was the Hand's true name." (Septon Sefton's dialogue in TSS)
  - Both names appear in Raw Entity List (lines 498–499) ✓
- No false-positive in-text reveals; no THK reveals re-captured (e.g., "the old man" ≠ Ser Arlan is NOT claimed as a TSS reveal — correct, as TSS doesn't perform that reveal)

### 7. HARVEST SIDECAR — **PASS**
- **21 TSS-specific breadcrumb lines** (lines 36–56 of harvest file)
- All follow format: `TSS / <verbatim anchor> / {kind} / <one-line note>`
- No entity pre-flagging; purely pointers for later harvest pass
- Valid `kind` enum usage (all ∈ {targaryen-history, prophecy, food, description, hospitality, cross-identity, foreshadow-hook, causal-spine}):
  - cross-identity: 3 entries (Egg, Bloodraven, identity via signet) ✓
  - targaryen-history: 5 entries (Great Bastards, Redgrass Field, Great Spring Sickness, Aerys, Eustace rebellion) ✓
  - prophecy: 2 entries (High Septon's pronouncement, Aerys's prophetic obsession) ✓
  - food: 1 entry (blackberries in cream) ✓
  - hospitality: 2 entries (Coldmoat wine, explicit denial of guest right) ✓
  - description: 2 entries (Egg's shaved head, chequy lion carved gate) ✓
  - causal-spine: 5 entries (Bennis→dam→battle, Wat's Wood burn→battle, blood price→trial, rebellion→water grant→conflict, Wall journey) ✓
  - foreshadow-hook: 1 entry (Wall climbing curiosity) ✓
- No analytical extraction bleed; breadcrumbs are saga-connection signposts only

### 8. COMPLETENESS — **PASS**
- All 12 Raw Entity List category headers present, in order, with content or "None":
  1. Characters (104 entries) ✓
  2. Locations (39 entries) ✓
  3. Houses (29 entries) ✓
  4. Factions & Organizations (7 entries) ✓
  5. Religions & Faiths (2 entries) ✓
  6. Cultures & Peoples (3 entries) ✓
  7. Artifacts & Objects (21 entries) ✓
  8. In-world Texts & Songs (2 entries) ✓
  9. Magic & Phenomena (5 entries) ✓
  10. Wars & Conflicts (4 entries) ✓
  11. Titles & Offices (7 entries) ✓
  12. Other (7 entries) ✓
- **Late-chapter spot checks** (final third: stable scene, departure, crossing at crossroads):
  - Event 21 (line 333): Dunk cuts Rohanne's braid — captures final stable scene ✓
  - Event 22 (line 340): Turning north to the Wall — captures final departure decision ✓
  - Artifact entries for white cloak (line 178), ivory spider brooch (line 179), Rohanne's braid (line 180) — all late gifts captured ✓
  - Spatial Layout final phase (line 357): "Departure: Dunk, Egg / Ride out of Coldmoat across the drawbridge into the rain" — covers the ending ✓
  - Dialogue of Note (line 394): "I hear it's tall" — the final line, captured ✓
- Late tables not skimped; Events continue through Event 22 (the turning north); no "running out of room" pattern

---

## Structural Integrity

**PASS**

- No truncation detected (narrative ends at line 1809–1810 of source; extraction ends at Event 22 / turning north)
- No mid-table restarts or fragmentation
- Markdown tables properly formatted
- Section headers in correct order per prompt schema
- No meta-commentary in cell content

---

## Strain Points

1. **Minor: Crow cage placement** — The iron crow cage at the crossroads frames both opening and closing of the novella (Events 1 and 22, Locations line 135). Currently listed in "Other" category (line 711) rather than Artifacts. Given its narrative prominence, it *could* belong in Artifacts (like the banners), but "Other" is defensible since it's a setting/landmark, not a tool or carried object. **No defect; judgment call is reasonable.**

2. **Minor: Relationship evidence for background/prior events** — Several relationships cite Dunk's dialogue/narration recounting prior service (e.g., "He taught me chivalry and the arts of war" for Ser Arlan tutoring). These cite events outside TSS scope but are voiced *within* TSS text by characters present (acceptable per prompt exception: "in-unit identity reveals and recountings"). **No isolation violation; correctly handled.**

---

## Summary

The TSS extraction is **mechanically and structurally sound**. All 54 relationships use locked vocabulary with proper qualifiers. Isolation is clean (no cross-novella leakage, no analytical types). Identity reveals are captured as SAME_AS with in-text evidence. Harvest sidecar contains 21 saga-connection breadcrumbs with proper kinds, no pre-flagging. All 12 Raw Entity List categories populated. Late-chapter content (stable scene, departure, final dialogue) is fully captured. No early-pass failures re-manifest. Minor borderline judgment call on crow cage placement (Other vs. Artifact) does not constitute a defect.

**Recommendation: Ship v4 to the D&E Pass 1 production run.**
