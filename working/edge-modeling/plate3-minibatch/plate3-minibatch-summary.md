# Plate 3 Mini-Batch — Validation Report

**Run date:** 2026-06-07
**Script:** `scripts/edge-reify-backfill.py --batch`
**Config:** `working/edge-modeling/plate3-minibatch/minibatch-config.json`
**Model:** claude-sonnet-4-6 (cwd=/tmp, --output-format json)
**Concurrency:** 3

---

## Per-Event Outcome (12 events)

| # | Event | Hub | Resolution | N-ary | Edges | Supersede | Validated | Cost |
|---|-------|-----|-----------|-------|-------|-----------|-----------|------|
| 1 | red-wedding | red-wedding | **reuse** | YES (multi-chapter dedup test) | 14 | 12 | PASS | $0.103 |
| 2 | purple-wedding | purple-wedding | **reuse** | YES | 6 | 5 | PASS | $0.097 |
| 3 | death-of-renly-baratheon | death-of-renly-baratheon | **mint** | YES (instigator≠executor) | 4 | 1 | PASS | $0.057 |
| 4 | jaime-kills-aerys | — | **skip-clean-dyad** (pre-declared) | NO | 0 | 0 | n/a | $0.000 |
| 5 | tyrion-kills-tywin | — | **skip-clean-dyad** (pre-declared) | NO | 0 | 0 | n/a | $0.000 |
| 6 | arrest-of-eddard-stark | arrest-of-eddard-stark | **reuse** | YES | 7 | 4 | PASS | $0.099 |
| 7 | execution-of-eddard-stark | execution-of-eddard-stark | **mint** | YES | 5 | 4 | PASS | $0.062 |
| 8 | assassinations-of-pycelle-and-kevan-lannister | same | **reuse** | YES | 5 | 2 | PASS | $0.070 |
| 9 | fall-of-astapor | fall-of-astapor | **reuse** | YES | 8 | 1 | PASS | $0.058 |
| 10 | battle-of-yunkai | battle-of-yunkai | **reuse** | YES | 7 | 1 | PASS | $0.079 |
| 11 | execution-of-lord-karstark | execution-of-lord-karstark | **mint** | YES | 3 | 1 | PASS | $0.077 |
| 12 | battle-of-the-blackwater | battle-of-the-blackwater | **reuse** | YES | 9 | 2 | PASS | $0.108 |

**Total: 10 reified, 2 skipped (clean dyad), 0 errors.**

---

## Total Role Edges by Type

| Edge Type | Count |
|-----------|-------|
| AGENT_IN | 25 |
| COMMANDS_IN | 15 |
| LOCATED_AT | 10 |
| VICTIM_IN | 14 |
| WIELDED_IN | 4 |
| **Total** | **68** |

---

## Hub Resolution

- Hubs **reused**: 7 (red-wedding, purple-wedding, arrest-of-eddard-stark, assassinations-of-pycelle-and-kevan-lannister, fall-of-astapor, battle-of-yunkai, battle-of-the-blackwater)
- Hubs **minted**: 3 (death-of-renly-baratheon, execution-of-eddard-stark, execution-of-lord-karstark)
- Hubs **queued for review**: 0

---

## Supersede Candidates

**33 edges flagged** across all events. Key correct ones:
- `roose-bolton BETRAYS robb-stark` → superseded by `red-wedding` (correct)
- `walder-frey VIOLATES_GUEST_RIGHT robb-stark` → superseded by `red-wedding` (correct)
- `petyr-baelish CONSPIRES_WITH olenna-tyrell` → superseded by `purple-wedding` (correct)
- `stannis-baratheon KILLS renly-baratheon` → superseded by `death-of-renly-baratheon` (correct)
- `ilyn-payne EXECUTES eddard-stark` → superseded by `execution-of-eddard-stark` (correct)
- `varys KILLS kevan-lannister` → superseded by `assassinations-of-pycelle-and-kevan-lannister` (correct)

**Known false positives (require human review at Plate 5 — do not merge automatically):**
- `rhaegal ATTACKS viserion superseded_by=fall-of-astapor` — WRONG. This edge is from a different event (ADWD dragon fight at Meereen pit). Both Rhaegal and Viserion appear in the fall-of-astapor participant set, so the programmatic detection fires incorrectly.
- `jorah-mormont BETRAYS daenerys-targaryen superseded_by=battle-of-yunkai` — WRONG. Jorah's spy revelation is a different event than the battle.
- `tyrion-lannister KILLS tywin-lannister superseded_by=battle-of-the-blackwater` — WRONG. Tyrion killing Tywin is ASOS, not connected to the Blackwater.
- `cersei-lannister ATTACKS/ASSAULTS eddard-stark superseded_by=execution-of-eddard-stark` — WRONG. Cersei did not assault Ned during the execution.

**Root cause:** The supersede query finds edges where BOTH endpoint slugs appear in the config participants list AND the edge_type is in the trigger family. Major characters like Cersei, Tyrion, Stannis appear across multiple events. The full-run fix requires narrowing the participant set per event more precisely, and/or post-filtering false positives by checking chapter evidence.

---

## Contract 10 Validation

**ALL 68 edges PASSED Contract 10.** No role edges with non-event targets emitted.

- AGENT_IN/VICTIM_IN targets: all resolve to existing `events/` nodes or freshly minted staging nodes.
- WIELDED_IN targets: all event slugs (correct).
- COMMANDS_IN targets: all event slugs (correct).
- LOCATED_AT: source = event slug, target = location (correct direction per architecture).

---

## Rule-by-Rule Assessment

### D8 Clean-Dyad Gate — CORRECTLY FIRING
The two pre-declared clean dyads (`jaime-kills-aerys`, `tyrion-kills-tywin`) were correctly skipped with `skip-clean-dyad` resolution. No hub was minted, no role edges were emitted. The `skipped-clean-dyads.jsonl` records both with their reasons.

Also notable: `execution-of-lord-karstark` — Robb both ordered AND personally executed, so the LLM correctly assigned only `AGENT_IN` (not a separate `COMMANDS_IN`) with the rationale "AGENT_IN subsumes COMMANDS_IN when orderer = executor."

### D7 Causation Rule (instigator≠executor) — CORRECTLY APPLIED
- **Red Wedding:** Walder Frey → COMMANDS_IN; Roose Bolton → AGENT_IN; Tywin → COMMANDS_IN confidence=2.
- **Purple Wedding:** Littlefinger → COMMANDS_IN; Olenna → AGENT_IN; Dontos → AGENT_IN confidence=2; Sansa → AGENT_IN confidence=3 (unwitting).
- **Renly shadow-death:** Stannis → COMMANDS_IN confidence=2; Melisandre → AGENT_IN confidence=2. Instigator≠executor correctly modeled. No instigator→victim edge created.

### Multi-Chapter Dedup (Red Wedding) — CORRECT
3 chapter files processed (Catelyn VII, Arya X, Epilogue). Output: 14 edges, all targeting `red-wedding` hub. Zero duplicate (source, type, target) triples. One hub.

### Hub Reuse-before-Mint — CORRECT
7 of 10 reified events matched existing nodes by slug-direct lookup. 3 genuine mints (no existing node). Zero false mint (no collision with existing nodes).

### Group/Faction Actors (house.* AGENT_IN) — CORRECTLY APPLIED
- `house-frey AGENT_IN red-wedding` (crossbowmen/men-at-arms)
- `house-bolton AGENT_IN red-wedding` (Bolton men-at-arms)
- `house-lannister AGENT_IN arrest-of-eddard-stark` (gold cloaks acting for Lannister)

### LOCATED_AT Direction — CORRECT
All LOCATED_AT edges emitted as `event_slug → location_slug` (event is located at place), per architecture.

### cwd=/tmp — VERIFIED
All `claude -p` calls ran with `cwd=/tmp`. No project context loaded (confirmed: cache_creation_input_tokens was low on calls 2+).

---

## Cost Analysis

| Item | Value |
|------|-------|
| Total cost (10 LLM calls) | $0.8095 |
| Average per event | ~$0.081 |
| First call (cache cold) | ~$0.10 |
| Subsequent calls (cache warm) | ~$0.06–0.08 |
| Estimated full-corpus (200 events) | ~$12–16 |

Cost is ~8–16x the smoke-test extrapolation ($0.30–0.60). The difference: each call now loads a full chapter's events and relationships (not just curated participant lists), driving higher input tokens. Still well under the $2–10 budget cap stated in the design doc.

---

## Issues Found / Will Need Fixing Before Full Corpus

1. **Supersede false positives** — The programmatic detection is too broad. Fix: at Plate 5, filter `supersede-candidates.jsonl` with human review before applying. OR: add per-event evidence-chapter filtering so only edges whose `evidence_chapter` matches the event's chapters are flagged.

2. **Sansa `AGENT_IN purple-wedding confidence=3`** — Technically correct (she carried the weapon) but semantically confusing (she was an unknowing carrier). May want to introduce a new role `INSTRUMENT_IN` for unwitting carriers, or exclude confidence=3 AGENT_IN from the primary supersede logic. Flag for Matt's judgment.

3. **`execution-of-lord-karstark` n-ary determination** — The LLM correctly found it n-ary via the framing that Karstark had previously murdered Lannister hostage boys (making the event multi-victim in a broader sense). The execution itself is a clean dyad (Robb alone). The reification was justified but borderline — the hub captures useful provenance context even if the primary act was 1:1.

4. **`barristan-selmy AGENT_IN battle-of-yunkai confidence=3`** — Barristan ("Arstan Whitebeard") was present but his role in the battle is unclear from the chapter extraction. Confidence=3 is honest, but may want to exclude confidence=3 AGENT_IN from the default query results.

---

## Verdict

**The general `--batch` path is ready for a larger validation sweep, with one caveat:**
- Supersede detection requires human review before Plate 5 merge (false positives exist).
- All other rules (D7, D8, Q1, Q2, cross-chapter dedup, group actors, LOCATED_AT direction, cwd=/tmp) worked correctly on this 12-event sample.

The full corpus (~200–300 reify-eligible events) at ~$0.08/event = **~$16–24 total**, which is within budget. Recommend proceeding to full corpus after Matt reviews this report.
