# Runbook — Edge-Modeling Audit Loop

**Purpose.** Standing procedure for keeping the edge-modeling reification project (see
`working/edge-modeling/edge-modeling-reification-design.md`) on course across multiple sessions.
Every plate that runs is verified by a two-step audit before the next plate launches.

**Why this exists.** The work is multi-session and partly LLM-driven. The project's own rules
require drift detection on bulk runs and *out-of-sample / fresh-eyes* review (memory:
`feedback_drift_detection_mandatory`, `feedback_fresh_review_and_out_of_sample`). A session that
grades its own work can't catch the error class where it misunderstood the goal — so judgment must
come from a separate session.

---

## The artifacts

| File | Role | Who runs it | Model |
|---|---|---|---|
| `working/edge-modeling/edge-modeling-reification-design.md` | Master plan; §7 holds the 6 plate prompts | — | — |
| `working/edge-modeling/audit-repo-reporter-prompt.md` | **Reporter** — gathers FACTS from the repo, writes a self-verifying log entry | in-repo agent (may be the plate executor) | Sonnet |
| `working/edge-modeling/audit-alignment-auditor-prompt.md` | **Auditor** — JUDGES the facts vs. design intent, renders ON-COURSE/DRIFT/NO-GO | a FRESH session (NOT the executor) | Opus |
| `working/edge-modeling/SESSION-LOG.md` | Append-only log both audit prompts write to | (output, not a prompt) | — |

Separation of duties: the Reporter's gathering is mechanical (counts, greps) and may be
self-run; the Auditor's **judgment must be an independent session**. That independence is the
whole point — do not let one context both execute a plate and audit it.

---

## The per-plate loop

```
1. EXECUTE a plate
   - Open a fresh session, paste the plate prompt from design-doc §7
     (or the launchable copy in progress/continue-prompts/).
   - Plate writes outputs to working/edge-modeling/ staging only.
     (Only Plate 5 may write graph/edges/edges.jsonl.)

2. REPORT (facts)
   - Run audit-repo-reporter-prompt.md with PLATE_JUST_RUN set.
   - Appends a "Repo Report — Plate N" entry to SESSION-LOG.md,
     including a "Validator checks (bash)" block + "Flag drift if…" tripwires.

3. AUDIT (judgment) — DIFFERENT SESSION
   - Run audit-alignment-auditor-prompt.md with PLATE_JUST_RUN set.
   - Independently recomputes the load-bearing numbers (does NOT trust the report's figures):
       wc -l graph/edges/edges.jsonl            # staging discipline
       scripts/build-edge-type-counts.py        # canonical_type_count, NOT grep "165"
       flip count in normalizer-candidates.jsonl
   - Appends "Alignment Audit — Plate N" + a VERDICT to SESSION-LOG.md,
     and a one-line verdict to worklog.md.

4. GATE
   - ON COURSE  → launch the next plate.
   - DRIFT      → apply the prescribed corrections, then re-audit.
   - NO-GO      → roll back per design-doc §8; block all downstream plates.
   *** Do not launch plate N+1 until plate N's verdict is ON COURSE. ***
```

## Hard gates (a plate must not launch if…)

- The prior plate's Auditor verdict is not **ON COURSE**.
- `graph/edges/edges.jsonl` row count changed during a Plate 0–4 (only Plate 5 may write it).
- The canonical `canonical_type_count` drifted without a logged schema entry.
- A plate's declared preconditions (design-doc §7) aren't met.
- Anything under `sources/` / `extractions/` was deleted (CLAUDE.md hard rule).

## Baseline (the numbers drift is measured against)

Frozen S82 state: `edges.jsonl` = 3,811 rows (all tier-1); event nodes = 371; canonical edge
vocab = 163 (→ 165 after Plate 1, adding AGENT_IN + VICTIM_IN); Haiku bulk = 1,617 rows.

## Status as of 2026-06-06

- Plates 0, 1, 2 complete (S83). Verified aligned by S83 self-report + an independent recount
  (this session): edges.jsonl untouched (3,811), `canonical_type_count` = 165, D2 RESOLVED
  recorded, zero nodes minted, Aerys merge staged-not-applied.
- **D2 = (a) Replace** is binding (graph-query `--path` traverses person→event→person).
- Plate 3 decisions resolved: **Q1 = selective reification** (trigger list = the "Reify" families
  only, not all ~8,300 Pass-1 events); **Q2 = run a confidence-gated fuzzy reuse pass** before
  minting (rebind to existing hubs like `assassination-of-tywin-lannister` / `purple-wedding`).
- Plate 3 open check: confirm `graph-query.py` 1-hop modes (`--neighbors`, `--edges`) surface
  hub-mediated relations; if not, revisit (c) Project for high-traffic types (mainly KILLS).
- The formal Reporter→Auditor cadence begins at **Plate 3** (first content-creating plate).

## Generalization note

This Reporter(facts) + Auditor(judgment) + append-only-log loop is reusable beyond edge-modeling.
If it proves out here, lift it into a general fleet/mission practice. Scoped to edge-modeling for now.
