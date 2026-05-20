---
session: 57
date: 2026-05-18
model: Opus 4.7
mission: Stage 4 — HAIKU-CUTOVER STEP 1.5 (Qualifier Vocab Lock-Down)
status: complete
duration: ~3h
---

# Session 57 — Stage 4 Qualifier Vocab Lock-Down

## What this session set out to do

Lock the qualifier vocabulary for the Stage 4 prose-edge classifier — close the second freestyle surface (the `notes` field) before the Haiku smoke. Three-tier framing was already locked in Session 56: Tier 1 (REQUIRED enum), Tier 2 (OPTIONAL enum), Tier 3 (no enum). This session's job was to do the per-edge-type verdicts and pick an encoding strategy.

## How it unfolded

### Phase 1 — Three-source data survey

Started with the canonical three data sources from the plan:

1. **21 completed Sonnet batches** (`working/wiki/pass2-buckets/*/prose-edges/*.edges.jsonl`) — 4,152 emit_edges across 891 JSONL files. **Punchline: `notes` is empty in 4,138 / 4,152 (99.7%).** This was the surprise of the session. The drift problem qualifier-vocab is fighting hasn't actually manifested on Sonnet — it's preventive for Haiku. Only 14 emits carried any notes content, mostly tier-2-confidence justifications, not qualifier values.
2. **Pass 1 corpus — full-text grep across 344 extraction files** — qualifier-bearing English (half-brother ×44, half-sister ×9, widow* ×238, betrothed ×335, ward ×259, fostered ×47, hostage ×381, former-[title] ×115, vow ×369, bastard son ×103).
3. **Wiki infobox `qualifier` field** (`working/wiki/data/infobox-data.jsonl`) — already-parsed qualifier-bearing rows: HOLDS_TITLE 256 rows (formerly ×62, claimant ×57, historical ×35), PARENT_OF 133 (rumored ×34, disputed ×20, officially ×16, adopted ×4), SWORN_TO 100 (formerly ×45, in death ×11, deserted ×3, by_marriage ×2), LOVER_OF 48 (rumored ×36, paramour ×4), SPOUSE_OF 23 (salt wife ×5, dissolved ×3, annulled ×1).

### Phase 2 — Mid-session corrections from Matt

Matt pushed back at two critical moments that reshaped the session:

**Correction 1 — "Has Pass 1 been used systematically?"** I'd done a grep-level pass on Pass 1 (counting half-brother, widow, etc.) but hadn't structurally parsed the `## Relationships Observed` tables. Matt asked: "we have rich relationship data in Pass 1 — has that been used?" I admitted no, only at grep level. Built `/tmp/parse_rels.py` to extract 7,398 four-column rows (`Character A | Relationship | Character B | Evidence`) from all 344 extractions, then bucketed by candidate edge type via regex on the relationship phrase. 4,805 distinct relationship phrases — a corpus the project hadn't tapped at this resolution.

That gave per-bucket empirical phrase distributions that directly informed Tier-1 enum choices. Most notably, LOVER_OF showed former ×19, secret ×7, paramour ×7 in the relation column itself — confirming the qualifier enum from Pass 1 directly, not just from wiki.

**Correction 2 — "Is that the only table worth noting?"** After I had a draft set of 16 verdicts ready, Matt prompted: "There is spatial movement as well." I'd cherry-picked just one of Pass 1's 17 schema sections. Audited the others:
- **`## Spatial Layout & Movement`** — Phase column (Opening / Departure / Assembly / Advance / Confrontation / Dispersal / Arrival). Overlaps with `temporal` field; not a new qualifier surface.
- **`## Events & Actions`** — numbered narrative sequences with rich method-language (crossbow / longsword / axe / dagger). Confirms KILLS method enum, no new categories.
- **`## Information Revealed`** — `How Revealed` column (X states it / internal thought / recalls / observes / Y says it). Confirms KNOWS source-of-knowledge enum, no new categories.
- **`## Dialogue of Note`** — free-text only, no enum surface.
- **`## Hospitality & Guest Right`** — **the find.** Pass 1 itself enumerates hospitality types in the `Type` column: 680 rows across 344 chapters, 80 distinct values but **top-10 = 88% of rows**: `shelter_offered` ×235, `feast_given` ×85, `hospitality_violated` ×52, `gift_exchange` ×46, `safe_conduct` ×27, `guest_right_invoked` ×24, `refusal_to_host` ×15, `shelter_denied` ×15, `hospitality_offered` ×14, `bread_and_salt` ×10. Pass 1 had been doing the enumeration work; I just missed it. **GUEST_OF moved from Tier-3 to Tier-2.**

Lesson worth capturing: when Pass 1's schema itself enumerates a column (Hospitality `Type`, Information Revealed `How Revealed`), that is direct empirical evidence of an enumerable edge qualifier — worth an explicit audit per section before locking.

### Phase 3 — Q2 corrected: zero freeform

The plan and continue prompt had four open questions for Matt. The interesting one was Q2: "Tier-3 `notes` discipline — cap at 100 chars? Required as non-queryable?" I'd structured this as an options menu. Matt rejected the framing and called for **zero freeform** — delete the `notes` field entirely from the edge schema across all tiers.

His reasoning was sharper than mine: notes was the open drift surface qualifier-vocab is supposed to close. Leaving it open for Tier-3 reintroduces the very surface we're trying to seal. Narrative-context loss is the price of closed-vocabulary safety on Haiku.

He also pushed: "why won't they get an enum?" — pressing the assumption that 130-ish types are genuinely fuzzy. I re-examined a half-dozen Tier-3 candidates (LOVES, FORESHADOWS, PERCEIVED_AS, FEARS, MOURNS, FOUNDED) and confirmed they genuinely don't have enumerable qualifier surfaces in either the corpus or wiki — only the LOVER_OF / GUEST_OF / HOLDS_TITLE family does. Tier-3 stayed populated, but with the more aggressive rule (no notes either).

### Phase 4 — Encoding strategy delegated to fresh agent

The four encoding strategies (Option A: new column in every architecture.md table; Option B: separate qualifier table per subsection; Option C: standalone file) all had defensible cases. Matt: "spawn fresh agent, have it decide honestly." Delegated to a general-purpose agent with the plan + architecture.md + classifier prompt + validator script as inputs.

Agent's verdict was **Option C** (`reference/edge-qualifier-vocab.md`) with five-point reasoning that held up:
1. Signal-to-noise — Option A pollutes 133 Tier-3 rows with placeholder dashes
2. Two-pass-modification safety — STEP 1.6 (qualifier) and STEP 3 (type-contract) would both edit the same tables in Option A; Option C separates them entirely
3. Validator parsing — easier to load a single dedicated file than to scan 15 subsection tables for a sparse column
4. Classifier discoverability — one extra file beats 149 rows of mostly-dashes
5. Bounded source-of-truth split — 16 of 149 types in the new file is a small, named, one-directional reference

Pattern worth repeating: any architectural-fork question where the orchestrator has been doing prep work that biases their judgment is a candidate for fresh-context delegation.

## Final verdicts

**Tier 1 (8 types — REQUIRED enum):**
- `SIBLING_OF` → `{full, half, step, milk, unknown}`
- `SPOUSE_OF` → `{current, former, annulled, widowed, salt_wife, unknown}`
- `PARENT_OF` → `{biological, adopted, claimed, rumored, disputed, unknown}`
- `WARD_OF` → `{formal, informal, hostage, unknown}`
- `HOLDS_TITLE` → `{current, former, claimed, contested, historical, unknown}`
- `VOWS_TO` → `{active, kept, broken, fulfilled, unknown}`
- `MANIPULATES` → `{via_bribe, via_flattery, via_false_information, via_threat, via_seduction, unknown}` (Session 55 confirm)
- `SWORN_TO` → `{current, former, deserted, by_marriage, claimed, unknown}`

**Tier 2 (9 types — OPTIONAL enum):**
- `BETROTHED_TO` → `{current, broken, fulfilled, secret, unknown}`
- `LOVER_OF` → `{current, former, secret, paramour, rumored, unknown}`
- `KILLS` → `{in_combat, in_duel, by_arrow, by_blade, by_ambush, by_proxy, by_creature, unknown}`
- `CONTRACTED_WITH` → `{assassination, mercenary_service, ransom, safe_passage, construction, marriage_brokerage, espionage, unknown}`
- `DECEIVES` → `{by_lie, by_disguise, by_omission, by_false_witness, by_silence, unknown}`
- `REVEALS_TO` → `{voluntary, coerced, accidental, under_torture, unknown}`
- `ATTACKS` → `{in_anger, unprovoked, in_self_defense, on_command, by_creature, unknown}`
- `KNOWS` → `{confirmed, suspected, told_by, witnessed, overheard, unknown}`
- `GUEST_OF` → `{shelter, feast, bread_and_salt, safe_conduct, gift_exchange, refused, unknown}`

**Tier 3 (132 types):** All others. No qualifier, no notes.

**Count check:** 8 + 9 + 132 = 149 ✓ (matches architecture.md master vocab)

## Open caveat — flagged by Matt at session close

> "I feel like there may be more qualifiers that come up as we are locking this stuff down."

Matt's instinct here is worth preserving. The 17 enumerable types are the ones surfaced by THIS session's data audit. STEP 1.6 (the encoding session) and STEP 3 (the validator extension) will exercise the qualifier schema against real classifier output — that's the natural moment when missed enums surface. The encode session should treat the 17 as a v1 cut, not a permanent freeze. If a wave-2 enum emerges during encoding (or during the eventual Haiku smoke), append to `reference/edge-qualifier-vocab.md` rather than re-running the full audit.

## Artifacts produced

- `working/qualifier-vocab/decisions.md` — full verdict matrix with rationale and data sources per type, methodology note, open-questions Q1–Q5 with decisions, schema implications for STEP 1.6 + STEP 3.
- `working/session-results/2026-05-18-stage4-qualifier-vocab-locked.md` — session summary, counts, methodology notes.
- `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-encode.md` — self-contained STEP 1.6 handoff with the 17 enums verbatim.
- `working/todos.md` — STEP 1.5 marked [x]; new STEP 1.6 inserted; STEP 3 description updated to reference the new vocab file.

## DO NOTs honored

- Did not touch `reference/architecture.md` (STEP 1.6 owns the one cross-reference line).
- Did not touch `.claude/agents/prose-edge-classifier.md` (STEP 1.6 owns the schema update + lookup step).
- Did not modify the validator script (STEP 3 owns).
- Did not retrofit / re-classify the 21 Sonnet batches — they remain the freeform control arm for the eventual Haiku comparison.
- Did not auto-run `/endsession` (Matt explicitly authorized at session close).

## What's next

STEP 1.6 (encode) → STEP 2 ([LINK] sub) and STEP 3 (validator + qualifier-enum enforcement + type-contract checks + `notes`-rejection) and STEP 4 (suspicious-edges flagger) — most can run in parallel. STEP 5 (Haiku smoke) is gated on all four.
