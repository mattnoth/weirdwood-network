# Edge-Modeling — Alignment Auditor (fresh-session validator prompt)

**What this is:** A reusable prompt for a **fresh session** (orchestrator-style, like the one
that authored the design doc) that judges whether execution is **staying on course** with the
master plan. It consumes (a) the design doc's intent and (b) the Repo Reporter's factual report,
and renders a verdict that **gates the next plate**.

**How to use:** Run it **after** the Repo Reporter (`audit-repo-reporter-prompt.md`) has appended
its facts to `working/edge-modeling/SESSION-LOG.md`. Fill the `SET THIS` block, paste the rest.
Best run as a **different session from the executor** (fresh eyes — the project's out-of-sample /
fresh-review principle).

**Downloadable artifact** — self-contained; depends on the design doc + the latest audit-log entry.

---

```markdown
# Edge-Modeling Alignment Audit — Plate <N>

> **Recommended model:** Opus. This is judgment work — interpreting drift, weighing whether a
>   deviation is benign or course-altering, deciding go/no-go. Do NOT downgrade to a cheaper
>   model; the whole point is an independent senior reviewer.
> **Trust worklog.md over any prompt** (CLAUDE.md rule #9). If worklog and the design doc
>   disagree on state, say so explicitly and trust worklog.
> **Role:** JUDGE ALIGNMENT, gate the next plate. You do not execute work or fix code; you
>   render a verdict and, if needed, prescribe corrective actions.

## SET THIS before running
- PLATE_JUST_RUN: <0 | 1 | 2 | 3 | 4 | 5>
- The Repo Reporter has appended its Plate <N> facts to working/edge-modeling/SESSION-LOG.md: <yes/no>
  (if no, STOP — run the Reporter first; you judge facts, you don't gather them.)

## Read first (intent + facts)
1. `working/edge-modeling/edge-modeling-reification-design.md` — the PLAN. Internalize:
   §3 design decisions (D1–D7), §5 plate table, §6 sequencing, §7 the prompt for PLATE_JUST_RUN
   (its done-criteria + out-of-scope + declared files), §8 reversibility, §9 open decisions.
2. The latest `working/edge-modeling/SESSION-LOG.md` entry (the Reporter's facts for this plate).
3. The latest `worklog.md` entry.
4. Spot-check. You MAY read the repo to verify a Reporter claim you doubt — base the verdict on
   the design doc's intent, not on re-deriving every fact yourself. BUT independently recompute the
   three load-bearing numbers rather than trusting the Reporter's (or a self-report's) figure:
   (i) `wc -l graph/edges/edges.jsonl` (staging discipline); (ii) `canonical_type_count` via
   `scripts/build-edge-type-counts.py` — NOT a grep of "165"; (iii) the flip count in
   `normalizer-candidates.jsonl`. If your recount disagrees with the logged number (e.g. a
   self-report said 10 flips but you count 11), reconcile it in the verdict — small discrepancies
   are often a header/comment line, but say so explicitly rather than passing it through.

## Judge — answer each, with a citation to the design doc and the report
1. **Done-criteria met?** Walk the PLATE_JUST_RUN prompt's explicit done-criteria one by one.
   Each: MET / PARTIAL / NOT MET, with the supporting fact from the report.
2. **Sequencing respected?** (§6)
   - Did anything in Plate 3 run before D2 was resolved (Plate 2) and the schema landed (Plate 1c)?
   - Did the Aerys merge (Plate 0b) precede any reification (Plate 3)? Reifying onto a phantom
     slug relocates the bug — this ordering is load-bearing.
   - Did Plate 4 promote-candidates pass through the Plate-0 normalizer first (D6)?
3. **Staging discipline (the #1 drift risk).** For PLATE ∈ {0,1,2,3,4}: confirm `edges.jsonl`
   was NOT written. Only Plate 5 may. If the Reporter flagged a canonical write, this is an
   AUTOMATIC NO-GO — the work must be moved to staging and the write reverted from backup.
4. **Design decisions honored?**
   - D1: vocab grew by exactly +2 (AGENT_IN, VICTIM_IN), not +4; no COMMANDER_OF/INSTRUMENT_IN.
   - D2: the replace-vs-project decision is recorded AND applied uniformly in any staged edges.
   - D3: event nodes were minted where needed; Red Wedding is ONE deduped hub, not 3.
   - D5: cost was reported as the legacy Sonnet path (not "$0") for existing-data backfill.
   - D7: causation modeled as one node + COMMANDS_IN orderer; no instigator→victim collapse.
5. **Reversibility preserved?** (§8) Backups exist where a write occurred; staging is throwaway;
   no `sources/`/`extractions/` deletions; superseded edges marked, not removed.
6. **Scope creep / drift?** Did the session do work outside the plate's declared scope or touch
   undeclared files (Reporter's scope check)? Did it bolt on extra tasks (purpose-discipline)?
7. **Goal alignment (the deeper check).** Step back from the checklist: does the work as executed
   actually move toward the project's real goal — *graph quality for agent traversal*, answering
   "who killed X" / "who was behind the Red Wedding" consistently? Or did it satisfy the letter
   of the plate while the underdetermination problem (§1) remains? Name any way the execution is
   technically-compliant-but-misaligned.

## Verdict (required, decisive — not a menu)
Render ONE:
- **ON COURSE** — done-criteria met, no material drift. Next plate is cleared to launch. State
  which plate is next (§6) and any pre-flight reminders.
- **DRIFT — CORRECT BEFORE PROCEEDING** — specific, fixable deviations. List each with the exact
  corrective action and which file/staging artifact to fix. Re-audit after correction.
- **NO-GO** — a sequencing violation, a premature canonical write, or a decision (D2/D7) applied
  wrong. State the rollback (from §8) and what must be redone. Block all downstream plates.

Be decisive. If a deviation is benign, say so and don't block. If it's course-altering, block
and say exactly why. Cite the design doc for every judgment.

## Output
APPEND to `working/edge-modeling/SESSION-LOG.md` under the Reporter's Plate <N> facts:

```
## Alignment Audit — Plate <N> — <date>
### Done-criteria: MET / PARTIAL / NOT MET (per item)
### Sequencing / Staging / Decisions / Reversibility / Scope: pass-fail with citations
### Goal-alignment note
### VERDICT: ON COURSE | DRIFT | NO-GO
### Next action: <launch Plate N+1 | corrective steps | rollback>
```

Also update `worklog.md` with the one-line verdict (so live state reflects the gate).

## Out of scope
- Executing the next plate. Fixing code yourself (prescribe; don't patch).
- Re-running the Reporter's mechanical gathering (you judge; it gathers).
```
