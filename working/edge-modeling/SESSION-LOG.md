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

---

## Plate 2 — verify + D2 resolved (Session 83)

**Both gating unknowns resolved. Plate 3 is unblocked.** Cost: $0 (analysis only). No node minted, no edge touched.

### 2a — Pass-1 event coverage by existing nodes

Script: `scripts/plate2-event-coverage.py`. Report: `working/edge-modeling/plate2-event-coverage.md` + `.json`.

| Metric | Value |
|---|---:|
| Total Pass-1 event ENTRIES (numbered bold-title lines, all 344 files) | **8,384** |
| Distinct titles (de-dup floor — normalized) | **8,317** |
| Distinct titles matching an existing event slug | **1** |
| Distinct titles → needs MINTING (floor) | **8,316** |
| Existing event nodes | 371 |
| Event nodes with ANY chapter linkage | **38 / 371 (10%)** |
| Pass-1 entries in a chapter touched by ≥1 event node (loose upper bound) | 1,937 |

Per-book entry counts: AGOT 1,496 / ACOK 1,655 / ASOS 2,113 / AFFC 1,279 / ADWD 1,841.

**Unexpected finding (1):** the design doc §3 D3 claim "*the Purple Wedding poisoning and Tywin's privy death have no hub*" is **wrong**. Both nodes exist (`purple-wedding`, `assassination-of-tywin-lannister`). What they LACK is Pass-1 chapter linkage in their index — `chapters.in_raw_list = []` because the chapter→event index was built from the Wars & Conflicts column of the Raw Entity List, which only catches historical-event NAMES, not narrative micro-events. Of the 371 nodes, only ~38 have any Pass-1 chapter linkage. D3 is partially correct — fine-grained minting IS needed for ~8k narrative micro-beats — but the named-event case has more existing infrastructure than the design assumed.

**Unexpected finding (2):** Pass-1 entries are overwhelmingly narrative micro-beats ("Departure at daybreak", "Tyrion reflects on killing Tywin", "Bran traverses rooftops toward the broken tower"), not named historical events. Only 1 distinct title matches an event-node slug. The realistic mint floor for Plate 3 is ~8k (one per distinct micro-beat) if EVERY entry is reified — or much smaller if Plate 3 mines selectively for kill/betray/attack/poisoning beats only.

### Spot-checks

| Case | Chapter | Existing node? | Verdict |
|---|---|---|---|
| Bran's defenestration | `agot-bran-02` #17 "Jaime pushes Bran from the window" | **NO** | **NEEDS MINTING** |
| Tywin's privy death | `asos-tyrion-11` #30 "Tyrion shoots Tywin" | YES (`assassination-of-tywin-lannister`) | REUSE (chapter linkage broken — re-bind) |
| Purple Wedding | `asos-tyrion-08` #36-38 "Joffrey begins choking / dies" | YES (`purple-wedding`) | REUSE (chapter linkage broken — re-bind) |

Prompt also mentioned Tywin's death in "ADWD Tyrion" — that's *references* (e.g. `adwd-tyrion-01` #2 "Tyrion reflects on killing Tywin"). The actual kill is in `asos-tyrion-11`.

### 2b — `graph-query.py` traversal check

Report: `working/edge-modeling/plate2-graphquery-traversal.md`.

**Verdict: YES — `--path` transparently traverses `person → event → person`.** `cmd_path()` (`scripts/graph-query.py:794-809`) computes 2-hop bridges by intersecting `neighbors_a` and `neighbors_b` over the WHOLE `edges.jsonl`. No node-type filter; no edge-type filter; intermediate node identity is irrelevant. Live probes confirmed bridges through `location.castle` (`winterfell`), `house.*` (`house-frey`), and generic location (`hornwood`). Plate 3 role edges onto event-node hubs will land in the same traversal mechanism with zero engineering changes.

### D2 RESOLVED — option (a) Replace

Recorded in `edge-modeling-reification-design.md` §3 (new "D2 RESOLVED" subsection after D7).

**Decision:** option (a) Replace. Reification is sufficient. Superseded person→person binaries get marked `superseded_by` (NOT deleted; CLAUDE.md hard rule). No materialized agent→patient dyad.

**Key rationale (one paragraph):** the headline query "who killed X" already works through any 2-hop bridge — including event nodes once role edges land. Option (c) Project would re-introduce the underdetermination problem D2 was designed to kill (which participant gets nominated `source` of the canonical binary?), and solves a problem `graph-query.py` doesn't have. Option (a) keeps the data model honest — events are nodes, not edges-in-disguise.

### Consequence for Plate 3

- Emit role edges onto hubs; STOP. No canonical-dyad sub-step.
- Mark superseded legacy person→person binaries with `superseded_by: <hub_slug>` (mechanism is a Plate 3 / Plate 5 detail).
- Node-minting scope: from 8,316 distinct titles "floor", but Plate 3 should likely be selective (kill/betray/attack/poisoning beats only) rather than reifying every Pass-1 micro-event. Whether to reify ALL or a SELECTIVE subset is now the new lead Plate 3 design question.

### Files touched
- CREATE `scripts/plate2-event-coverage.py`
- CREATE `working/edge-modeling/plate2-event-coverage.md`, `.json`
- CREATE `working/edge-modeling/plate2-graphquery-traversal.md`
- APPEND `## D2 RESOLVED` subsection to `working/edge-modeling/edge-modeling-reification-design.md` §3
- (next: append to worklog.md + this SESSION-LOG.md entry)
- Did NOT touch `graph/edges/edges.jsonl`, `graph/nodes/`, Plate 0 outputs, or Plate 1 doc commits.

---

## Session 83 closing summary (2026-06-05, orchestrator)

### Commits landed this session
1. `5bc168b4d` — Plate 0 + Plate 1 (normalizer + Aerys merge candidates + doc foundation).
2. `03442d0a0` — Plate 2 (event-coverage analysis + traversal probe + D2 RESOLVED) + continue prompts for Plates 3/4/5.

Neither commit touched `graph/edges/edges.jsonl` or `graph/nodes/`. The graph is in the same state it was at session start; everything new is staging or doc.

### What worked
- **Parallel agent fan-out was efficient.** Plate 0 (script-builder, Sonnet) and Plate 1 (general-purpose, Sonnet) ran simultaneously without conflict — different file surfaces, different staging dirs. Combined wall-clock ~10 min vs ~25 min sequential.
- **Pre-flight file/line verification before agent dispatch saved a round-trip.** Confirming `mechanical-extractor.md:176-178`, `aerys-targaryen.node.md`, validator existence up front meant the agent prompts were correct on first try.
- **The design doc's plate structure held.** Each §7 prompt was copy-pasteable and self-contained as advertised; agents didn't need clarifying questions.

### Surprises / partial failures
- **§3 D3 was partially wrong.** The design doc claimed Purple Wedding and Tywin's privy death have no event-node hub. They DO. What's missing is the *chapter-evidence linkage* on those existing nodes (`chapters.in_raw_list = []`). This is good news (less minting needed for the headline cases) but reshapes Plate 3 — the script will need a chapter-rebind step for existing nodes, not just a mint step.
- **Coverage join was much weaker than expected.** Only 1 of 8,317 distinct Pass-1 event titles exact-matched an event-node slug. 10% of existing nodes (38/371) carry any Pass-1 chapter linkage. The "join" path the design assumed (Pass-1 entry → existing event node via chapter membership) is largely broken at the node-index layer. Two responses are possible: (i) a fuzzy-title pass to reuse more existing nodes, or (ii) accept the slug-floor and treat near-everything as minted. This is **open Matt decision Q2 in the Plate 3 continue prompt**.
- **The normalizer's flip count was surprisingly small (10 out of 3,811).** The design doc cited "232 unordered pairs carry the same edge type in both directions" as evidence of widespread inversion. After edge-type-aware filtering (excluding PRISONER_OF, SERVES, COMMANDS, etc., where passive-voice phrases are SEMANTIC, not inversion-cues), only 10 unambiguous flips remained. This is NOT a failure — it's the conservative posture working — but it means the "232 bidir pairs" finding was largely NOT subject-leakage inversions. They were genuine bidirectional relations (mutual support, reciprocal feudal ties, etc.). Worth re-examining whether the design's framing of the live-graph problem was overstated.
- **Causation rule already shipped.** §3 D7's "use COMMANDS_IN for orderer, AGENT_IN for executor; do NOT make a separate causal node" was implicit in the Plate 1 schema decisions; nothing extra to do here.

### Failures (genuine — none this session)
No failed agent runs. No reverted commits. The single "flagged-for-review" row (donal-noye ↔ mag-mar-tun-doh-weg KILLS, both forward + reverse signal) is a legitimately ambiguous mutual-kill at the Battle of Castle Black — flagged for human eye, not script error.

### Newly open Matt decisions (blocks Plate 3)
1. **Reify-all vs reify-selective?** 8,317 distinct event titles is a lot of new hubs. Recommend selective: kill/death/attack/poisoning/wedding/betrayal/capture/escape trigger list. Matches the underdetermination cases the project actually wants to fix.
2. **Fuzzy reuse vs slug-floor mint?** Exact-match found 1 hit. Fuzzy/title-matching (e.g. `tywin-privy-death` ≈ `assassination-of-tywin-lannister`) would likely lift to several hundred. Decide: pay for a fuzzy pass, or accept the floor.

Both questions are documented inline in `progress/continue-prompts/2026-06-05-edge-modeling-plate-3-backfill.md` PRE-WORK DECISION block.

### Newly noticed but DEFERRED
- **§3 D3 in the design doc itself is now stale.** The "Purple Wedding + Tywin's death have no hub" claim should be edited or annotated. Did not do this in-session to keep the design doc as the historical lineage record; Plate 2's "D2 RESOLVED" subsection plus this SESSION-LOG note are the authoritative corrections. A future session may want to add a `D3 RE-EXAMINED` note in §3 to make the correction explicit.
- **`graph/edges/_regrounding/` backup convention** is documented in design doc Plate 5 but not yet exercised this session. First exercise lands in Plate 5.
- **The Plate 1 head rule benefits only FUTURE Pass-1 extractions.** None are planned (worklog says Pass 1 is DONE). The rule is a hedge against any future re-run, but does not retroactively fix the existing 344 extractions. Plate 0's normalizer is the retroactive fix.

### Continue-prompt coverage (per design doc §8)
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-3-backfill.md` — reify backfill + minting; HELD on Matt Q1/Q2.
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-4-haiku-disposition.md` — 1,617-row Haiku bulk re-bucketing; HELD on Matt go.
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-5-merge.md` — gated merge of all staging into canonical `edges.jsonl`; HELD on Plates 3+4 staging + Matt sign-off.

Each carries the required "Recommended model" line, lists its preconditions, and points back to the design doc and SESSION-LOG for context. A fresh Claude Code session should be able to pick any of them up cold.

### What did NOT happen this session (scope discipline)
- No edge in `graph/edges/edges.jsonl` was modified.
- No node in `graph/nodes/` was created, moved, or deleted.
- No Pass-1 extraction was re-run.
- No LLM token spend on the data path (Plates 0-2 were entirely deterministic / doc-only / read-only analysis). Total session cost is the agent meta-LLM cost only — small.
- The Haiku-bulk (1,617 rows) was NOT promoted, normalized, or touched. It's Plate 4's job.

### Trust hierarchy reminder (CLAUDE.md rule #9)
If the design doc's §3 D3 disagrees with this SESSION-LOG on whether Purple Wedding / Tywin's death have hubs: **trust SESSION-LOG + plate2-event-coverage.md**. They reflect actual repo state as of 2026-06-05; the design doc's D3 was written before the coverage probe ran.

## Repo Report — Plate 2.5 (Event-Node Inventory) — 2026-06-06 — read-only

**What ran:** `scripts/event-node-inventory.py` (new; stdlib-only; READ-ONLY on graph/). Built the event-node catalog + fuzzy reuse lookup that gate Plate 3 reuse-before-mint (design doc D8 / Plate 3 precondition).

**Outputs (staging only):**
- `working/edge-modeling/event-node-inventory.md`
- `working/edge-modeling/event-node-reuse-lookup.json`

**Facts:**
- 371 event nodes (292 battle / 32 war / 35 tournament); 359 reuse-eligible.
- 12 suspected category-drift nodes (Winds-of-Winter chapter entries + ASOS prologue/epilogue misfiled as event.battle) — excluded from reuse lookup; flagged for reclassification.
- 1,033 reuse keys; 6 collision keys (near-duplicate event nodes, e.g. battle-at-the-red-fork vs battle-of-the-red-fork) — flagged for merge before minting.
- 279 reify-family edges in edges.jsonl; ~124 (44%) already plausibly map to an existing hub. KILLS reuse coverage 29% (consistent with most KILLS being clean dyads → D8 no-reify).
- Spot check: sack-of-kings-landing, red-wedding, assassination-of-tywin-lannister, purple-wedding all present in lookup.

**graph/ untouched.** No nodes minted, no edges written.

**Flags for the Auditor:**
- [ ] 12 category-drift nodes still typed event.battle (reclassify out before/at Plate 3).
- [ ] 6 collision near-duplicate event nodes (merge before minting to avoid wrong-twin rebind).

**Validator checks (bash):**
```bash
python3 scripts/event-node-inventory.py            # reproduces the summary
jq "keys|length" working/edge-modeling/event-node-reuse-lookup.json 2>/dev/null || python3 -c "import json;print(len(json.load(open(\"working/edge-modeling/event-node-reuse-lookup.json\"))))"
ls graph/nodes/events | wc -l                       # expect 371
wc -l graph/edges/edges.jsonl                       # expect 3811 (unchanged)
```

---

## Alignment Audit — Plates 0–2.5 block — 2026-06-06

> **Role:** Independent fresh-session ALIGNMENT AUDITOR (not the executor). Judges the whole
> pre-Plate-3 block at once: Plates 0, 1, 2, 2.5 + staged cleanups (drift-reclassify,
> collision-merge) + the Plate 3 Red-Wedding smoke test. PLATE_JUST_RUN = "0-through-2.5+cleanups+smoke".
> **Model:** Opus (judgment work, per runbook). **Trust hierarchy:** worklog.md is authoritative;
> it agrees with the design doc + SESSION-LOG on state this block — no contradiction to flag.

### Recomputed load-bearing numbers (run independently, NOT trusted from the report)

| Check | Command | Result | Expected | Verdict |
|---|---|---|---|---|
| Staging discipline | `wc -l graph/edges/edges.jsonl` | **3811** | 3811 | ✅ untouched |
| Graph mutation | `git status --short graph/` | **empty** (zero modified files) | empty | ✅ nothing written |
| Canonical vocab | `build-edge-type-counts.py` → `canonical_type_count` | **165** (not grepped) | 165 | ✅ |
| New vocab present | AGENT_IN / VICTIM_IN in type map | **both PRESENT, count 0** (staged, unemitted) | present | ✅ |
| Anti-sprawl (D1) | COMMANDER_OF / INSTRUMENT_IN in vocab | **both absent** | absent | ✅ +2 not +4 |
| Event nodes | `ls graph/nodes/events \| wc -l` | **371** | 371 | ✅ no minting |
| Phantom Aerys | `aerys-targaryen.node.md` present? | **yes, still present** (May 7) | present | ✅ merge staged-not-applied |
| Drift nodes | 2 spot-checks (`a-storm-of-swords-prologue`, `mercy-...`) | **still `type: event.battle`** | unchanged | ✅ reclassify staged-not-applied |
| Normalizer flips | `normalizer_action` tally over 3811 rows | **10 flipped / 3800 kept / 1 flagged** | 10 | ✅ |

**Flip-count reconciliation (the logged 10-vs-11 ambiguity): it is 10.** `normalizer-candidates.jsonl`
is the full 3,811-row graph annotated in place (one row per edge with a `normalizer_action` field),
NOT a flips-only file. The exact tally is `flipped=10, kept=3800, flagged=1` (sums to 3,811). The
"11" confusion most plausibly arose from adding the 1 flagged mutual-kill row (`donal-noye ↔
mag-mar-tun-doh-weg`, both-directions signal) to the 10 flips, or from conflating the Aerys merge's
3 repointed edges. The flagged row is correctly NOT a flip (it is held for human judgment, not
guessed) — design doc §4 "where direction is ambiguous and unsignaled, flag rather than guess."
Discrepancy is benign and now explained.

### Done-criteria — per plate

**Plate 0 (§7.0):** MET. Normalizer built (`scripts/edge-direction-normalizer.py`); 10 confirmed
inversions flipped incl. all three design-doc §1 self-witnessing cases (cressen/melisandre KILLS,
arya/sandor CAPTURES, tyrion/shae BETRAYS — verified in SESSION-LOG probes); {flipped,kept,flagged}
counts reported; Aerys merge staged (3 edges repointed to `aerys-ii-targaryen`, `aerys-i-targaryen`
untouched). edges.jsonl NOT written (confirmed: still 3811, git clean). ✅

**Plate 1 (§7.1):** MET. Head rule + optional role sub-bullets in `mechanical-extractor.md`; parser
non-breakage verified (`stage4-pass1-extra-tables.py` numbered-item regex skips sub-bullets);
AGENT_IN + VICTIM_IN in architecture.md, COMMANDS_IN widened, WIELDED_IN note; vocab 163→**165
(recomputed, confirmed)**; validator Contract 10 (AGENT_IN/VICTIM_IN → event.* targets). No Pass-1
rerun. ✅

**Plate 2 (§7.2):** MET. Node-existence count produced (8,384 entries / 8,317 distinct / 1 exact
slug-match / 38-of-371 with chapter linkage); graph-query.py `--path` confirmed to traverse
person→event→person untyped/unfiltered (`cmd_path` lines 794–809); **D2 RESOLVED → (a) Replace**,
recorded in design doc §3 + worklog. Honestly surfaced that design §3 D3 was partly wrong (Tywin/
Purple-Wedding nodes DO exist) and appended the **D3 RE-EXAMINED** correction in the design doc — good
self-correction, not drift. ✅

**Plate 2.5 (inventory):** MET. `event-node-inventory.py` (read-only) → 371 nodes, 359 reuse-eligible,
1,033 reuse keys, 12 drift nodes + 6 collision groups flagged. Reuse-before-mint catalog (design D8
precondition) in place. graph/ untouched. ✅

**Staged cleanups (drift-reclassify, collision-merge):** MET as STAGING. drift-reclassify proposes
12 `event.battle → meta.chapter` (Winds-of-Winter chapter articles + ASOS prologue/epilogue), 0
affected edges; collision-merge proposes 6 groups (4 high-conf via existing `same_as` redirects, 1
medium, 1 low needing human judgment), 0 affected edges, SAME_AS-redirect mechanism (no deletion —
CLAUDE.md hard rule honored). Both write candidates + summaries only; **independently confirmed the
12 drift nodes are still `event.battle` on disk** — staged, not applied. ✅

**Plate 3 smoke test (Red Wedding):** MET as a dry-run smoke. 12 role edges on ONE `red-wedding` hub;
validation keep=12/flag=0/drop=0; 9 superseded person→person binaries identified (**independently
confirmed 3 of them — roose-bolton BETRAYS robb-stark, raymund-frey KILLS catelyn-stark, ryman-frey
KILLS dacey-mormont — are real rows in edges.jsonl**); `dry_run: true`, $0, nothing written to graph/.
✅

### Sequencing / Staging / Decisions / Reversibility / Scope

**Sequencing (§6):** PASS. Plate 2 (D2 resolve) + Plate 1c (schema) both landed before the Plate 3
smoke ran — smoke uses AGENT_IN/VICTIM_IN, which exist only because 1c shipped. Aerys merge (0b) is
staged ahead of any reification, and the smoke is a dry-run that wrote nothing — no reification has
yet landed on the phantom slug (the load-bearing ordering is preserved because Plate 5 hasn't run).
Plate 4 has not run, so the D6 "promote-candidates through normalizer first" ordering is not yet
testable — correctly still HELD.

**Staging discipline (the #1 risk):** PASS — the decisive check. `git status --short graph/` is
**empty**; edges.jsonl = 3,811 byte-for-byte; events nodes = 371; phantom Aerys present; drift nodes
still event.battle. Across ALL of Plates 0–2.5 + cleanups + smoke, **zero canonical writes to
graph/edges/edges.jsonl or graph/nodes/.** Only Plate 5 may write, and it hasn't. No automatic NO-GO
condition is present.

**Design decisions honored:** D1 PASS (+2 exactly; COMMANDER_OF/INSTRUMENT_IN absent). D2 PASS
(Replace recorded AND applied in the smoke: superseded binaries marked-for-supersession, no
materialized dyad emitted). D3 PASS (one deduped Red Wedding hub from 2 chapters, not 3 fragments;
D3 RE-EXAMINED correction logged). D7 PASS (smoke gives orderers Walder Frey / Tywin / Lothar
`COMMANDS_IN`, executors `AGENT_IN`, victims `VICTIM_IN`, one node, no instigator→victim collapse).
D8 PASS (Red Wedding is the archetypal n-ary case — instigator≠executor, multiple killers/victims —
exactly what D8 says to reify; clean dyads are explicitly left as direct edges, e.g. the inventory's
29% KILLS reuse coverage matches "most KILLS are clean dyads → no hub"). D5: smoke ran as dry-run
($0) so the legacy-Sonnet cost honesty is not yet exercised — fine for a smoke; must hold at real
Plate 3.

**Reversibility (§8):** PASS. Everything is throwaway staging under `working/edge-modeling/`; no
`sources/`/`extractions/` deletions; supersession via `superseded_by`/SAME_AS markers, not removal;
the one irreversible write (Plate 5) is correctly deferred and unrun.

**Scope creep:** MINOR-BENIGN. The drift-reclassify + collision-merge cleanups and the Plate 2.5
inventory were not in the original §5 plate table (which jumps Plate 2 → Plate 3). However they are
direct, necessary consequences of D8's **"reuse-before-mint is mandatory"** rule and the Plate-2.5
inventory's two explicit Auditor flags (12 drift + 6 collisions "merge before minting to avoid
wrong-twin rebind"). They are staged-only, edge-impact-zero, and gate Plate 3 correctly — this is
plan-faithful elaboration, not bolt-on. The Red-Wedding smoke is named as a Plate 3 done-criterion
(§7.3: "Red Wedding hub populated … as a smoke test") and was run as a dry-run — in scope.

### Goal-alignment note

This block moves **genuinely toward** the real goal (graph quality for agent traversal; consistent
"who killed X" / "who was behind the Red Wedding"). The smoke test is the proof: after Plate 5 merge,
`--path walder-frey robb-stark` will surface the `red-wedding` hub with a `COMMANDS_IN` leg, and
`--path roose-bolton robb-stark` an `AGENT_IN`→`VICTIM_IN` walk — and the divergent legacy binaries
(`roose-bolton BETRAYS robb-stark` vs `walder-frey BETRAYS robb-stark`) get demoted via
`superseded_by` so 1-hop no longer returns the inconsistent projections. That is the underdetermination
fix (§1) actually landing on the canonical example. The work is NOT technically-compliant-but-
misaligned: D8's structure-not-type trigger keeps hubs only where the head was genuinely contested,
so the project is not paying a 2-hop tax on clean dyads. One honest residual: this is all still
**staging + a dry-run** — the alignment is *demonstrated on one event*, not yet *delivered at scale*.
The real Plate 3 (full selective mining over the reify-family, Sonnet legacy path, actual node-mint/
rebind) is where scale-alignment gets tested; the smoke earns confidence but is not the deliverable.

### VERDICT: ON COURSE

Done-criteria met across Plates 0/1/2/2.5 + both staged cleanups + the smoke. The #1 risk (premature
canonical write) is clean: graph/edges/edges.jsonl untouched (3,811), graph/nodes/ unmutated, git
status empty. Every design decision (D1, D2, D3, D7, D8) is honored in the staged artifacts.
Sequencing and reversibility intact. The drift/collision cleanups are plan-faithful (reuse-before-mint
prerequisites), not scope creep. The Red-Wedding smoke demonstrates the headline query fix end-to-end
in dry-run.

### Next action: LAUNCH Plate 3 (full selective backfill) — with pre-flight reminders

1. **Resolve Matt's two open Plate-3 questions first** (documented in
   `progress/continue-prompts/2026-06-05-edge-modeling-plate-3-backfill.md`): Q1 reify-selective
   (trigger list) vs reify-all — **recommend selective**, per D8; Q2 fuzzy-title reuse pass vs
   slug-floor mint — **recommend the confidence-gated fuzzy reuse pass** over the Plate-2.5 lookup,
   per D8 reuse-before-mint.
2. **Apply the 4 high-confidence collision merges (and decide the 1 medium / 1 low) BEFORE minting**,
   so reuse rebinds to the correct canonical twin (e.g. `battle-on-the-green-fork`, not the redirect).
   The 12 drift `event.battle → meta.chapter` reclassifications should also clear before Plate 3 reuse
   so those chapter-articles aren't offered as hubs. Both remain STAGING until the Plate 5 gate, but
   the reuse pass must read the corrected catalog.
3. **State Plate 3 cost honestly as the legacy Sonnet path (~$2–10), not $0** (D5) — the dry-run smoke
   was $0 only because it was a dry-run.
4. **Keep the staging discipline:** Plate 3 writes role-edges-staging + minted-event-nodes to
   `working/edge-modeling/` only. The merge to canonical is Plate 5, Matt-gated.
5. Run the Reporter→Auditor loop again after the real Plate 3 (first at-scale content write).

## Cleanup Decisions RESOLVED — 2026-06-06 (Matt-approved)

Resolved the 3 human-judgment items from Plate 2.5 / collision-merge staging. Authoritative record: `working/edge-modeling/cleanup-decisions-resolved.md`. All verified read-only; **0 affected edges** each; nothing applied (Plate 5 gate executes them).

- **Drift (12):** move graph/nodes/events/* → graph/nodes/chapters/* + retype `meta.chapter`.
- **Collision (4 high-conf):** merge mummers-ford / red-fork / whispering-wood(3-way) / green-fork to their `battle-at/in/on-*` canonical (SAME_AS + redirect, not deleted).
- **conquest-of-dorne:** NOT a merge — wiki confirms `The_Conquest_of_Dorne` is Daeron I's BOOK; reclassify `the-conquest-of-dorne` event.war → **object.text** (→ graph/nodes/texts/). Keep `conquest-of-dorne` as the historical event.
- **maidenpool:** wiki `Tourney_of_Maidenpool` = "Redirect to: Tourney at Maidenpool" → canonical `tourney-at-maidenpool`; merge `tourney-of-maidenpool` in.
- **Plate 3 rule CONFIRMED:** `house.*` permitted as AGENT_IN source for group actors.

**Auditor (Plates 0–2.5 block):** VERDICT ON COURSE — staging discipline clean (edges.jsonl=3811, git status graph/ empty, 371 event nodes, no minting), flip count reconciled to 10 (flagged mutual-kill held), vocab=165 recomputed, goal-aligned. Full Plate 3 backfill cleared to launch.

## Plate 3 Full-Sweep — Status Report — 2026-06-07

**TL;DR:** Plate 3 logic is fully built, debugged, and the runner is now crash-resilient + resumable. The real full LLM sweep has NOT completed (overnight attempt killed by the rate wall ~6 min in). Graph remains untouched. Ready to resume on command. **Cost is larger than first estimated — see "Revised scope/cost."**

### Done
- `scripts/edge-reify-backfill.py` built: `--smoke`, `--batch`, `--all`, `--resume`, `--dry-run`.
- Logic validated on a 12-event mini-batch ($0.81): D8 clean-dyad skip OK (Jaime/Aerys, Tyrion/Tywin skipped), D7 causation OK (instigator->COMMANDS_IN, executor->AGENT_IN, no instigator->victim collapse), multi-chapter dedup OK (Red Wedding 3 chapters -> 1 hub), reuse-before-mint OK (7 reused / 3 minted), group/faction AGENT_IN OK, LOCATED_AT direction OK, Contract 10 68/68 PASS.
- Supersede false-positive bug found + fixed: added chapter-overlap requirement (edge.evidence_chapter must be in the event's chapter set). Mini-batch supersede 33 -> 12; re-validated: 3 named FPs gone, true positive (roose BETRAYS robb -> red-wedding) retained, Karstark routed to skip.
- Runner hardened (2026-06-07, code-only, ~0 usage): FAIL-FAST on rate wall (<= ~90s, no multi-hour retry burn -> exits clean, leaves ledger), incremental per-event flush, processed-events ledger, `--resume` (verified 0 duplicates), progress+cost stdout, richer dry-run stub. Verified via full-corpus dry-run + mock-wall tests.

### NOT done
- The real full sweep. Overnight run was killed ~6 min in by the rate wall (then burned usage in retry loops before the fail-fast fix existed). Produced only 37 staged minted nodes + 11 hub-review-queue entries. No role edges, no summary yet.

### Staged artifacts — working/edge-modeling/plate3-full/
- minted-event-nodes/ : 37 (STAGING; NOT in graph)
- hub-review-queue.jsonl : 11
- role-edges-staging.jsonl / processed-events.jsonl / skipped-clean-dyads.jsonl / supersede-candidates.jsonl : not yet populated (will fill on the real `--resume` run)

### Revised scope/cost (IMPORTANT — flag for Matt)
- The full-corpus dry-run enumerated ~**2,056 trigger-family candidate events** (vs the earlier 200-300 estimate). Many will be skipped as clean dyads by the D8 gate, but each non-trivially-deterministic candidate still needs one claude -p call to decide reify/skip + assign roles.
- Real cost is therefore **uncertain: roughly $50-$160** (~$0.08/event), NOT the previously stated $16-24, depending on how many are deterministically skippable.
- RECOMMENDATION: run a **cost-bounded calibration chunk first** (e.g. one book, or a first ~200 events) with `--resume`, read the actual reify/skip ratio + cost, THEN decide whether to complete all ~2,056. The runner is resumable, so chunking is free.

### Graph integrity
- `wc -l graph/edges/edges.jsonl` = 3811; 0 nodes minted into `graph/`; `git status graph/` clean. Untouched throughout.

### Resume command (attended)
    python3 scripts/edge-reify-backfill.py --all --resume
- Watch the per-10-event progress + running-cost line. Fail-fast leaves the ledger; re-run the same command to continue after a wall.

### After the sweep completes
- Run Reporter (`audit-repo-reporter-prompt.md`) -> fresh Auditor (`audit-alignment-auditor-prompt.md`) on the full output.
- Human-review `hub-review-queue.jsonl` (borderline/medium-fuzzy) and `supersede-candidates.jsonl`.
- Then Plate 5 = the single gated merge into graph/ with before/after sign-off.
