---
date: 2026-05-18
session: 57
model: Opus 4.7
mission: Stage 4 — HAIKU-CUTOVER STEP 1.5
status: complete
artifact: working/qualifier-vocab/decisions.md
---

# Stage 4 Qualifier Vocab Lock-Down — Session Results

## What this session did

Locked the qualifier vocabulary for the Stage 4 prose-edge classifier — closed the second freestyle surface (the `notes` field) before the Haiku smoke. Decisions captured in `working/qualifier-vocab/decisions.md`.

## Counts

| Bucket | Count | Behavior |
|---|---|---|
| **Tier 1 — REQUIRED enum** | 8 edge types | Validator rejects empty or out-of-enum |
| **Tier 2 — OPTIONAL enum** | 9 edge types | Validator rejects out-of-enum (but accepts omission) |
| **Tier 3 — no enum, no notes** | 132 edge types | Edge has no `qualifier` and no `notes` field |
| **Total** | 149 | Matches architecture.md master vocab count |

### Tier 1 (REQUIRED enum)

`SIBLING_OF`, `SPOUSE_OF`, `PARENT_OF`, `WARD_OF`, `HOLDS_TITLE`, `VOWS_TO`, `MANIPULATES` (Session 55 lock — confirmed), `SWORN_TO`.

### Tier 2 (OPTIONAL enum)

`BETROTHED_TO`, `LOVER_OF`, `KILLS`, `CONTRACTED_WITH`, `DECEIVES`, `REVEALS_TO`, `ATTACKS`, `KNOWS`, `GUEST_OF`.

## Data sources surveyed

| Source | Volume | What it gave us |
|---|---|---|
| 21 completed Sonnet batches | 4,152 emit_edges, 891 JSONL files | **`notes` empty in 99.7%** — confirmed drift is preventive not observed. Validated edge-type frequency distribution. |
| Pass 1 `## Relationships Observed` tables | 7,398 rows across 344 extractions (NEW structural parse this session) | Qualifier vocabulary in narrative voice: half-brother, widow, ward, hostage, former-[title], bastard-son, vow, etc. |
| Pass 1 `## Hospitality & Guest Right` tables | 680 rows across 344 extractions; 80 `Type` values; top-10 = 88% (NEW after mid-session audit) | Already-typed enum from Pass 1 itself: `shelter_offered` ×235, `feast_given` ×85, `gift_exchange` ×46, `safe_conduct` ×27, `bread_and_salt` ×10. **Surfaced `GUEST_OF` as missed Tier-2 candidate.** |
| Pass 1 `## Events & Actions` numbered sequences | 344 extractions | Confirmed KILLS-method enum (crossbow, longsword, axe, dagger language) without surfacing new categories. |
| Pass 1 `## Information Revealed` tables | 344 extractions | Confirmed KNOWS source-of-knowledge enum (`told_by` / `witnessed` / `confirmed`) without new categories. |
| Pass 1 full-text grep | 344 extraction files | Method-language for KILLS / ATTACKS / DECEIVES (poisoned ×532, stabbed ×147, by-arrow ×1293, etc.). |
| Wiki infobox `qualifier` field | 2,287 qualifier-bearing rows across 25 fields | Already-parsed empirical distributions per edge type. Dominant signals: HOLDS_TITLE.formerly ×62, HOLDS_TITLE.claimant ×57, PARENT_OF.rumored ×34, SWORN_TO.formerly ×45, LOVER_OF.rumored ×36. |

## Key decisions

1. **`notes` field deleted entirely** from edge schema across all tiers (Matt: "zero freeform"). Reasoning: the field was the open drift surface this entire track is meant to close. Leaving it open for Tier-3 reintroduces the surface.
2. **Tier-3 edges emit no qualifier and no notes.** Pure: `source / edge_type / target / confidence / evidence_snippet / evidence_kind / first_available`.
3. **21 already-emitted Sonnet batches preserved as the freeform control arm** for the eventual Haiku enum-locked comparison. No normalizer. No re-classification. The 14 notes-bearing emits stay as data for the diff.
4. **Encoding strategy: Option C** (decided by independent fresh-context agent). Qualifier enums live in NEW file `reference/edge-qualifier-vocab.md`; architecture.md tables untouched (only a one-line cross-reference pointer added in STEP 1.6).
5. **Two separate architecture.md passes** for STEP 1.6 (qualifier) and STEP 3 (type-contract) — they no longer collide because qualifier data lives outside architecture.md entirely.
6. **Symmetric edges share qualifier across both endpoints** (locked Session 56 — restated this session).

## Methodology note — Pass 1 structural parse

Initial survey relied on grep-level text searches against Pass 1. Mid-session Matt pushed to do a structural parse of the `## Relationships Observed` tables since they're the canonical source for narrative-voice relationship language. Built `/tmp/parse_rels.py` to extract 7,398 four-column rows (`Character A | Relationship | Character B | Evidence`) and bucket them by candidate edge type via regex on the relationship phrase. This gave per-bucket empirical phrase distributions that directly informed Tier-1 enum choices (e.g., LOVER_OF: former ×19, secret ×7, paramour ×7 in the relation column directly).

The structural parse approach is reusable. The 4,805 distinct relationship phrases across 344 chapters are a corpus the project hasn't tapped at this resolution before. Worth keeping the parser as a script for downstream passes (Pass 3 voice/perception, Pass 5 theory-informed) which will also need to bucket free-text relationship language.

## Methodology note — Pass 1 section audit (mid-session correction)

After initial draft Matt prompted: "is that the only table worth noting? There is spatial movement as well." Audit of the remaining 16 Pass 1 sections revealed that **`## Hospitality & Guest Right` already enumerates hospitality types** (680 rows, top-10 = 88%) — a structurally-typed enum that surfaced `GUEST_OF` as a missed Tier-2 candidate. Other sections audited (`## Spatial Layout & Movement`, `## Events & Actions`, `## Information Revealed`, `## Dialogue of Note`) either confirmed existing enum choices or contained free-text values that don't map to enumerable qualifiers.

Lesson: when Pass 1's schema itself enumerates a column (e.g., the `Type` column in Hospitality, the `How Revealed` column in Information Revealed), that is direct empirical evidence of an enumerable edge qualifier — worth one explicit pass per section before locking. Updated decisions accordingly: 16 → 17 enumerable types.

## Methodology note — encoding agent

The encoding-strategy question (A/B/C) was delegated to a fresh-context agent to avoid orchestrator framing bias. The agent independently picked Option C and its reasoning held up against the orchestrator's pre-existing leanings. Pattern worth repeating for any architectural-fork question where the orchestrator has been doing prep work that biases their judgment.

## What's next

| Step | What | Status | Recommended model |
|---|---|---|---|
| **STEP 1.6** | Encode decisions: write `reference/edge-qualifier-vocab.md`, update classifier prompt schema (delete `notes`, add `qualifier` field + lookup step), add architecture.md cross-ref line. | NEXT | Sonnet 4.6 — mechanical translation |
| **STEP 2** | Burn `[LINK]` substitution into candidate data | Independent | Sonnet 4.6 |
| **STEP 3** | Validator extension — type-contract checks + qualifier-enum enforcement + `notes`-field rejection | Folded together | Sonnet 4.6 |
| **STEP 4** | Suspicious-edges worklist generator | Independent | Sonnet 4.6 |
| **STEP 5** | Haiku smoke test | After 1.6–4 | Haiku 4.5 |

## DO NOTs honored

- Did not touch `reference/architecture.md` (STEP 1.6 owns that change).
- Did not touch `.claude/agents/prose-edge-classifier.md` (STEP 1.6 owns).
- Did not touch validator script (STEP 3 owns).
- Did not retrofit the 21 Sonnet batches.
- Did not run `/endsession` (awaiting explicit permission).
