# Edge-Modeling Reification — Session Log

> Append-only narrative of what we did, in date order. Detail decisions and
> resolutions inline so future sessions can pick up without context.

---

## 2026-06-05 — Session 83 kickoff (orchestrator)

**Action taken:** Acted on §9 Decision #1 of `edge-modeling-reification-design.md` —
"Apply Plate 0 + Plate 1 now? (the safe first move)."

**Pre-flight checks (verified before launch):**
- `graph/edges/edges.jsonl` exists at 3,811 edges (per worklog v1.3).
- `graph/edges/_regrounding/` backup directory exists (will reuse).
- `scripts/stage4-type-contract-validator.py` exists (Plate 1c target).
- `scripts/stage4-pass1-extra-tables.py` exists (Plate 1b parser target line 522).
- Phantom `graph/nodes/characters/aerys-targaryen.node.md` exists alongside
  canonical `aerys-ii-targaryen.node.md` (Plate 0b merge target confirmed).
- `mechanical-extractor.md` line 176-178 contains the `## Relationships Observed`
  table with no head rule (Plate 1a insertion site confirmed).
- `mechanical-extractor.md` line 134-135 is `## Events & Actions` (Plate 1b
  insertion site confirmed).

**Launched in parallel (Sonnet, both agents):**
1. **Plate 0** → `script-builder` agent
   - 0a: Build `scripts/edge-direction-normalizer.py` (deterministic head-flip)
   - 0b: Aerys slug merge candidate file
   - Output: `working/edge-modeling/normalizer-candidates.jsonl`,
     `normalizer-diff.md`, `flagged-for-review.jsonl`,
     `aerys-merge-candidates.jsonl`
   - NOT touching `graph/edges/edges.jsonl` (Plate 5 gates the merge).
2. **Plate 1** → `general-purpose` agent
   - 1a: Insert head rule into `.claude/agents/mechanical-extractor.md` after L178
   - 1b: Add OPTIONAL Events & Actions role sub-bullets; verify the parser at
     `scripts/stage4-pass1-extra-tables.py:522` only reads first line of each
     numbered item
   - 1c: `AGENT_IN` + `VICTIM_IN` to `reference/architecture.md`; widen
     `COMMANDS_IN`; add validator target-type contract
   - Vocab 163 → 165.

Both plates are reversible (Plate 0 stages-only, Plate 1 doc-only / git revert).
Plates 2/3/4/5 remain HELD per the design doc's sequencing diagram.

**Next steps after agents return:**
- Verify outputs.
- Write continue prompts for Plates 2, 3, 4, 5 to
  `progress/continue-prompts/` (per §8 of the design doc).
- Update worklog.md.

---

## Plate 1 — doc foundation report (Session 83)

**All three sub-tasks completed. $0, doc-only, fully reversible via git revert.**

### 1a — Pass-1 head rule
Inserted at `.claude/agents/mechanical-extractor.md` **line 188**, immediately after the `## Relationships Observed` table. The rule specifies: Column A is always the SEMANTIC AGENT (not grammatical subject, not POV character); passive sentences use the by-phrase agent; ordered acts use the executor with the orderer going into Events & Actions Instigator slot.

### 1b — Events & Actions role sub-bullets
Sub-bullets inserted at `.claude/agents/mechanical-extractor.md` **line 136** (the `Agent:` sub-bullet line). The six optional roles are: Agent, Patient, Instrument, Location, Instigator, Outcome. A compatibility note at line 143 makes clear entries without sub-bullets remain valid.

**VERIFIED: parser reads only first line — sub-bullets safe.**

Parser analysis (`scripts/stage4-pass1-extra-tables.py:521-537`): `parse_events_section()` iterates all lines in the section and appends a line to `items` only when it matches `_NUMBERED_ITEM_RE = re.compile(r"^\d+\.\s+")`. Sub-bullet lines (starting with spaces + `- Agent:` etc.) do not match this regex and are silently skipped. Zero breakage.

### 1c — Schema additions

- **`AGENT_IN` added** at `reference/architecture.md` **line 237**: "Acts as the agent/executor of an event — the participant who actually performed the act. Source is the executor; target is the event node. Person/House → Event (`event.*`)."
- **`VICTIM_IN` added** at `reference/architecture.md` **line 238**: "Receives the action of an event as the victim or patient — the participant on whom the act was performed. Person/House → Event (`event.*`)."
- **`COMMANDS_IN` widened** at line 214. Old description: "Holds command role in a battle or war (note which side)". New: adds "OR acts as the orderer/instigator of an event where the commander did NOT personally execute the act … Covers both the military-command and the instigator/orderer roles to avoid proliferating near-synonym types."
- **`WIELDED_IN` note** added at line 240: a blockquote clarifies that `WIELDED_IN` (artifact→event) serves the instrument role, `COMMANDS_IN` serves orderer/instigator, and together with `AGENT_IN`/`VICTIM_IN` these four cover all standard participant slots — no `INSTRUMENT_IN` needed.
- **Vocab count** updated at architecture.md line 551: `~163` → `~165` with Session 83 annotation.
- **Validator contract** (`scripts/stage4-type-contract-validator.py`): added `_ROLE_EVENT_TYPES = frozenset({"AGENT_IN", "VICTIM_IN"})` and Contract 10 (after existing Contract 9). Logic: if target resolves to `"events"` → KEEP; if target has no node → FLAG (keep + annotate for future event node minting); if target resolves to any other known category → DROP. Validator loads cleanly (`--help` confirmed).

### Unexpected findings
None. All insertion sites matched their predicted locations. Parser verification was clean-shot — no ambiguity.

---

## Plate 0 — script-builder report (Session 83)

**Both sub-tasks completed. $0, deterministic, no LLM. Outputs in `working/edge-modeling/` only — `graph/edges/edges.jsonl` untouched.**

### 0a — Head-direction normalizer

Script: `scripts/edge-direction-normalizer.py`

**Key design decision:** naive passive-pattern matching on ALL edge types produces false positives. Edge-type semantics govern whether a "by" phrase signals inversion:
- **EXPERIENCE/STATE types** (RESENTS, FEARS, DISTRUSTS, PRISONER_OF, MOURNS, LOVES, HATES, TRUSTS, RESPECTS, DECEIVED_BY, SERVES, COMMANDS, etc.): passive phrases describe the cause/context of the relationship from the source's perspective — NOT evidence of inversion. These are excluded from flip logic.
- **AGENT_POSITIVE types** (KILLS, BETRAYS, ATTACKS, RESCUES, HEALS, TUTORS, CAPTURES, etc.): source is the actor. A passive "by" phrase signals the source was actually the patient — flip.

**Counts:**
| Action | Count |
|--------|-------|
| flipped | 10 |
| kept | 3800 |
| flagged | 1 |
| **total** | **3811** |

**Top flipped types:** RESCUES (2), KILLS (2), BETRAYS (2), HEALS (1), CAPTURES (1), TUTORS (1), ATTACKS (1).

**Verification probes — all 3 PASSED:**
- `cressen → melisandre KILLS` ("Killed by") → flipped to `melisandre → cressen` PASS
- `arya → sandor CAPTURES` ("Conflicted captor-dependent relationship") → flipped to `sandor → arya` PASS
- `tyrion → shae BETRAYS` ("Betrayed by") → flipped to `shae → tyrion` PASS

**Flagged (1):** `KILLS: donal-noye → mag-mar-tun-doh-weg | "Kills/killed by"` — mutual kill (both forward and reverse signal); they killed each other at the Battle of Castle Black.

All 10 flips verified against canon knowledge: gregor kills oberyn, melisandre kills cressen, lynesse betrays jorah, barristan rescues daenerys, brienne rescues jaime (bear pit), goodwin tutors brienne, eagle attacks ghost, shae betrays tyrion, sandor captures arya, aemon heals gared.

### 0b — Aerys slug merge

Script: `scripts/aerys-slug-merge.py`

- Phantom: `aerys-targaryen` (3 edges exact match)
- Canonical: `aerys-ii-targaryen` (11 edges)
- Both node files confirmed as the same person (Mad King Aerys II, 262–283 AC)
- **3 edges rewritten** in `aerys-merge-candidates.jsonl`: jaime→aerys KILLS, jaime→aerys SERVES, lord-redwyne→aerys SERVES
- `aerys-i-targaryen` (different earlier king) NOT touched
- Quarantine recommendation (move phantom to `_conflicts/`) noted in summary; deferred to Plate 5

### Unexpected findings

**PRISONER_OF semantics are NOT inverted:** `PRISONER_OF: source=prisoner, target=captor`. "Captured by" in asserted_relation = source was captured by target = CORRECT direction. Early draft of the script incorrectly flipped these; corrected before final output.

**COMMANDS/SERVES passive phrases are contextual, not inversions:** "Is served by" from daenerys's perspective in a COMMANDS edge = daenerys is the commander receiving service = CORRECT direction. Same for "summoned by" in SERVES. Excluded from flip logic.

**Conservative default held throughout:** "Only flip on positive signal" — no flip without a confirmed reverse cue. 3,800 kept rows show the vast majority of edges had unambiguous forward-direction descriptions.
