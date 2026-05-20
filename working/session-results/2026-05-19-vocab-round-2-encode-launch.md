# Vocab Round 2 Encode — Launch Info

**Launched:** 2026-05-19 (Session 58 continued)
**Launched by:** Opus 4.7 orchestrator
**Worker model:** Sonnet 4.6 (mechanical translation, mirror of STEP 1.6)
**Agent type:** general-purpose
**Run mode:** background

---

## What was launched

Matt verdicted "adopt all 8 STRONG candidates" from the 2026-05-19 vocab completeness audit. This launch encodes those adoptions into runnable artifacts.

## The 8 adoptions — 10 new edge types total

| # | New edge(s) | Type | Subsection (best fit) |
|---|---|---|---|
| 1 | `SPIES_ON` + `INFORMS` | Tier-3, one-sided pair (target=person and target=handler respectively) | Knowledge & Information |
| 2 | `NAMED_AFTER` | Tier-3, one-sided (entity→namesake) | Cultural & Religious OR Identity & Disguise — encoder picks best fit and notes in session-results |
| 3 | `STEP_PARENT_OF` + `STEP_CHILD_OF` | Tier-3, one-sided pair | Kinship & Family |
| 4 | `IN_LAW_OF` | **Tier-2 OPTIONAL enum** (symmetric) with enum `{by_marriage_of_self, by_marriage_of_child, by_marriage_of_sibling, by_marriage_of_parent, unknown}` | Kinship & Family |
| 5 | `RESCUES` | Tier-3, one-sided (rescuer→rescued) | Military & Conflict |
| 6 | `BANISHES` | Tier-3, one-sided (banisher→banished) | Political & Authority |
| 7 | `TORTURES` | Tier-3, one-sided (torturer→tortured) | Military & Conflict |
| 8 | `CONSPIRES_WITH` | Tier-3, symmetric | Factional & Diplomatic |

**Vocab count: 149 → 159.** Tier counts: 8 Tier-1 (unchanged), 10 Tier-2 (was 9 — IN_LAW_OF added), 141 Tier-3.

## Source of truth

- `working/qualifier-vocab/audit-completeness-2026-05-19.md` — full rationale for each new edge type (Section A.1)
- `working/qualifier-vocab/decisions.md` — Round 1 decisions; gets a "Round 2" addendum section appended

## Hard DO-NOTs

- Do NOT modify `working/qualifier-vocab/decisions.md` Round 1 content (lines existing as of Session 57). Append a new "## Round 2 — Vocab Completeness Audit (2026-05-19)" section at the END, recording verdicts.
- Do NOT re-classify or normalize any prose-edges JSONL — control arm stays intact.
- Do NOT run /endsession.
