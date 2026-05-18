---
session: 55
date: 2026-05-18
model: Opus 4.7
duration: ~5h (continuous)
purpose: Stage 4 vocab-lock decisions for Haiku cutover prep
launched_from: progress/continue-prompts/2026-05-18-stage4-haiku-cutover.md
---

# Session 55 — Stage 4 Vocab Lock Decisions + Pass 1 Staleness Incident

## Session purpose

The Stage 4 v1 bulk run on Sonnet (mission `2026-05-14-stage4-v1-bulk-sonnet`) had ~$2,800 / ~340h projected remaining at 75/1,089 batches done. The continue prompt's three-step plan was: (1) lock the vocab so the classifier has a fully-closed decision surface, (2) establish a Sonnet reject-quality baseline on complex pages, (3) re-test Haiku with the locked vocab. This session covered Step 1 + ancillary architecture-of-agents discussion. An incident mid-session (stale Pass 1 belief) consumed ~30 min and produced documentation/guardrail fixes.

## What happened, in order

### Phase 1 — Vocab-gap pull + normalization

Wrote `scripts/stage4-vocab-gap-analysis.py` to normalize the 68 rows in `working/wiki/pass2-buckets/questions-for-matt.jsonl`. Found 16 distinct schema variants across rows (heavy drift — three different field names competing for "proposed type": `proposed_edge_type` / `pattern` / `proposed_type` / `proposed_types[]`). Normalizer collapsed all variants into a single canonical view. Output: `working/agent-fleet-specs/stage4-vocab-gaps-normalized.jsonl` + `stage4-vocab-gaps-rollup.md`. Final counts: 10 stale-resolved (proposed type already in canon — workers filed before adoption), 37 truly open gaps, 7 untyped (deprecated abbreviated schema).

### Phase 2 — Decision bucketing

Per Matt's "split by confidence" output shape: I recommended on obvious cases (clear semantic gap or clear reverse-direction violation), surface-only on borderline. Buckets:

- **A — Stale-resolved (12 rows):** ATTENDS, BETROTHED_TO, COUSIN_OF, DEPICTED_IN, GIFTED_TO, KNIGHTED_BY/BESTOWS_KNIGHTHOOD_ON, MADE_OF, MILK_BROTHER_OF, NURSED_BY/WET_NURSE_OF, UNCLE_OF/NEPHEW_OF. Close as duplicates.
- **B — Recommended ACCEPT (5 types):** AFFLICTED_BY, DIED_OF (medical-state edges), COMPANION_OF (friendship distinct from ALLIES_WITH/LOVES), PARTICIPATES_IN (non-combat event involvement, fills gap between FIGHTS_IN and ATTENDS), OFFICIATES (ritual officiant — Melisandre/wedding, kingsmoot chair).
- **C — Recommended HARD-REJECT (9 rows):** CHILD_OF, HOST_OF/HOSTED_BY, RESURRECTED_BY, SERVED_BY/EMPLOYS, DEFEATED_BY, GUARDIAN_OF (use FOSTERED_BY) — all reverse-direction violations of existing one-sided types. RELATED_TO, KINSMAN_OF, LIAISED_WITH (use LOVER_OF) — too generic.
- **D — Surface only (22 rows across 12 proposed types):** ASSAULTS/ATTACKS, COURTS, NAMED_AFTER, GREAT_UNCLE_OF/DAUGHTER_IN_LAW_OF/STEP_PARENT_OF, D.5 commerce cluster, PROPOSED_AS_BRIDE, CROWNS_QUEEN_OF_LOVE_AND_BEAUTY, REPUTED_AS, PETITIONED, USES_AS_SIGIL, PRACTICES.

Wrote decision doc at `working/agent-fleet-specs/stage4-vocab-lock-2026-05-18.md`.

### Phase 3 — Matt's first pass through D bucket

Matt accepted B wholesale, deferred to my call on C, and walked D verdicts one by one. Key responses:
- D.1 ASSAULTS — wanted "something for assault, unfortunately there's a lot of rape in ASOIAF." Initial framing: ATTACKS = creature (eagle/skinchanger), ASSAULTS = person-on-person.
- D.2 COURTS — "there has to be some kind of edge like that." ACCEPT.
- D.3 NAMED_AFTER — "not super important, names get reused." REJECT.
- D.4 Extended kinship — "if derivable, okay. Don't overload one-hop." REJECT all three.
- D.5 — pushed back on PURCHASED_FROM (Duncan/Pate is character-defining) and BUILT (BUILT-the-Wall vs FOUNDED-Night's-Watch distinction). Asked if CAPTAIN_OF exists (it didn't).
- D.6 PROPOSED_AS_BRIDE — "happens a lot. ACCEPT."
- D.7 CROWNS_QUEEN_OF_LOVE_AND_BEAUTY — "Lyanna Stark." ACCEPT.
- D.8 REPUTED_AS — pushed back on my reject. "We don't have ANYTHING in this existing schema for this?"
- D.9 PETITIONED — accepted REJECT in favor of NEGOTIATES_WITH.
- D.10 USES_AS_SIGIL — "are sigils on entities then? This is a pretty big gap." Pushed back.
- D.11 PRACTICES — ACCEPT.

### Phase 4 — `qualifier` field clarification

Matt asked what a `qualifier` field is. Explained: lives on each edge row in JSONL output (per `.claude/agents/prose-edge-classifier.md` line 66). Free-text, optional, edge-instance-specific. Lands as bracketed text in promoted node files. Examples from architecture: SPOUSE_OF "current/former/annulled"; SIBLING_OF "full/half/step"; WIELDS "[formerly]".

Matt asked: "okay, so edges basically have a schema as well?" — yes. Three layers:
1. Conceptual edge metadata (architecture.md § "Edge Metadata") — type / source / target / first_available / confidence / evidence / notes / temporal / symmetric.
2. Classifier wire format (`.claude/agents/prose-edge-classifier.md` required-fields table) — adds candidate_kind, evidence_kind, evidence_snippet, evidence_section, paragraph_index, confidence_tier (int 1-3), direction (comention), evidence_chapter/quote/extraction_file (pass1_relationship).
3. On-disk node markdown line format — what edges look like once promoted. `KILLS: aerys-ii-targaryen (cite: jaime-i-agot) [during Sack of King's Landing, breaks Kingsguard vow]` — bracketed text = qualifier.

### Phase 5 — `[LINK]` placeholder discussion

Matt spotted `[LINK]` in a candidate row's snippet: `"...intends to outrun the [LINK] and strike the first blow..."` (for `barristan-ii-the-winds-of-winter → widower`). Confirmed: deterministic placeholder inserted by `scripts/wiki-pass2-build-cross-refs.py:94`. Marks the exact position in source prose where the wikilink appeared; actual anchor text lives in separate `anchor_text` field. The classifier mentally substitutes — but Haiku may not. Filed as a Step 2 todo: burn the substitution into the data so the cognitive step disappears.

Matt connected this to the broader pattern: "these are the kinds of things we need to make locked kinda deal right? similarly to the questions in the text file?" Yes — multiple prompt-comprehension surfaces benefit from the same lockdown discipline. Surfaced 5 distinct lock surfaces for Haiku-cutover prep:
1. Edge-type vocab (in progress this session)
2. `[LINK]` substitution (data-side lock; ~10-line script edit + regenerate candidates)
3. Type-contract validation (validator extension)
4. Suspicious-edges worklist (post-emit flagger for soft-fallback patterns)
5. Haiku smoke test (with all above in place)

Added these as 5 numbered todos under "Stage 4 — Haiku Cutover Prep" in `working/todos.md`.

### Phase 6 — Second-opinion agent dispatch on remaining D items

After Matt asked to spawn a sub-agent for a fresh take, dispatched general-purpose (Sonnet) with full reading list (architecture.md, classifier prompt, decision doc, rollup) + open D items.

Agent overrode three of my prior leans:
- **PURCHASED_FROM → ACCEPT** (transactional event has graph value; Dunk/Pate shield is character-defining; non-artifact transactions like ship-passage have no OWNS target)
- **BUILT → ACCEPT** (FOUNDED scopes to orgs; BUILT-the-Wall is character→place.location, no fitting type)
- **REPUTED_AS → ACCEPT** (PERCEIVED_AS requires a specific perceiver; collective reputation has none; constrain target to `concept.*`)
- **CAPTAIN_OF → ACCEPT** (new; missed by my pass) — Davos/Black Betha, Victarion/Iron Victory, Asha/Black Wind

Agent also caught a stale FIGHTS_IN description (architecture.md row says "battle or war"; classifier prompt says "battle, war, or tournament" — inconsistency causes COMPETES_IN gap-filing to look real). Fix needed.

### Phase 7 — ATTACKS/ASSAULTS reconciliation

Matt and agent had different framings:
- Matt's: ATTACKS = creature-only; ASSAULTS = person-on-person (incl. sexual, with qualifier)
- Agent's: ATTACKS = generic physical non-lethal; ASSAULTS = sexual specifically

After explaining the "is there nothing for entity-attacked-entity?" gap (KILLS requires death; DUELS is formal; POISONS is method-specific; OPPOSES is political — none cover "X attacked Y"), Matt decided: split into ATTACKS (generic, covers creature and person→person physical) + ASSAULTS (sexual violence specifically). "Feels icky but there it is."

### Phase 8 — STALE PASS 1 BELIEF INCIDENT

Mid-discussion of CREW_OF, I argued part of the trade-off was "Pass 1 book evidence for ACOK/ASOS/ADWD hasn't been classified yet." Matt halted immediately: "no, all five books' mechanical passes have been done. This has happened before."

Dispatched general-purpose (Sonnet) for root-cause investigation. Findings:

**Ground truth:** All 5 books complete (344/344 .extraction.md files: AGOT 73, ACOK 70, ASOS 82, AFFC 46, ADWD 73, completed 2026-05-06).

**Three stale sources contradicted the worklog:**
1. The continue prompt itself — line 33 reads "Status from memory: AGOT done, AFFC done, ACOK 20/70, ASOS pending, ADWD pending." The phrase "Status from memory" is a smoking gun — drafter serialized in-session memory into a persistent artifact without verifying against worklog.
2. Memory file `project_pass1_prompt_v3_canonical.md` — 13 days stale, frozen at ACOK chain-explosion incident (Session 33). Pre-dated 2026-05-06 completion by ~13 days.
3. MEMORY.md index line propagating the stale counts.
4. CLAUDE.md pipeline table row 4 — still said "In progress | v2 schema, AGOT in progress, 4 books remaining."

**Root cause:** orchestrator had 2-vs-1 contradiction (continue prompt + memory said incomplete; worklog said complete). Resolved by trusting the more **task-proximal** sources over the more **authoritative** one. Stale sources had higher narrative coherence — they agreed with each other, spoke directly to Stage 4 context, used concrete numbers. The worklog's correct state was a flat checklist that didn't shout.

### Phase 9 — Fixes applied (via dispatched general-purpose agent)

6 fixes:
1. Memory file `project_pass1_prompt_v3_canonical.md` — completion section updated to all-5-complete; quality-standards "do not mix v2/v3" replaced with "Pass 1 is closed."
2. MEMORY.md index line for that memory updated.
3. Continue prompt `2026-05-18-stage4-haiku-cutover.md` "Status from memory" passage replaced with verified-against-worklog text + explanatory note.
4. CLAUDE.md pipeline table row 4 changed to "✅ Done | v3 schema, all 5 books complete (344/344 as of 2026-05-06)."
5. CLAUDE.md Orchestration Rule 9 added: when continue-prompts and worklog conflict on project state, trust worklog and flag the contradiction explicitly. Root cause precedent cited.
6. New memory file `memory_staleness_policy.md` — trust hierarchy (file counts > worklog > todos > continue prompts > memory entries) + Session 55 precedent. MEMORY.md index updated.

Verification grep confirmed 0 problematic stale claims remain across CLAUDE.md / continue-prompts / memory / todos / worklog. Three residual matches were all expected (explanatory notes citing the historical error).

### Phase 10 — Agent vs skill architecture discussion

Matt asked about turning the second-opinion-vocab-reviewer pattern into a reusable agent/skill. Explained both mechanisms:
- **Subagent definitions** (`.claude/agents/<name>.md`): frontmatter + body becomes pre-loaded "birth context" for the agent. Per-invocation `prompt` arg slots specific task in.
- **Skills** (`.claude/commands/*.md` or `.claude/skills/*.md`): user-invocable via `/<name>`; can spawn agents internally.

Designed a `vocab-decision-reviewer` agent shape (Read-only tools; Sonnet model; pre-loaded reads of architecture.md + classifier prompt + questions-jsonl + rollup; per-invocation prompts pass the specific items). Matt: "skip — let's write a continue prompt and /endsession for fresh context." Captured the idea but didn't write the agent.

## Decisions locked this session

**16 new edge types approved** (132 → 148):
- Kinship & Family: PROPOSED_AS_BRIDE
- Political & Authority: (none added)
- Factional & Diplomatic: CONTRACTED_WITH
- Military & Conflict: ATTACKS, ASSAULTS, PARTICIPATES_IN
- Knowledge & Information: AFFLICTED_BY, DIED_OF (or new Medical subsection)
- Emotional & Perceptual: COMPANION_OF, REPUTED_AS
- Possession & Ownership: PURCHASED_FROM, BUILT, CAPTAIN_OF
- Magic & Supernatural: PRACTICES
- Cultural & Religious: OFFICIATES
- Hospitality & Custom: CROWNS_QUEEN_OF_LOVE_AND_BEAUTY
- Kinship: COURTS

**2 description modifications:**
- FIGHTS_IN: fix to say "battle, war, or tournament"
- MANIPULATES: add qualifier-mechanism note ("via bribe", "via flattery", "via false information")

**Rejected:** NAMED_AFTER, GREAT_UNCLE_OF/DAUGHTER_IN_LAW_OF/STEP_PARENT_OF (derivable), BRIBES standalone (qualifier on MANIPULATES instead), CREW_OF (agent's call — low signal; non-captain crew rejected as no-fitting-type), USES_AS_SIGIL (defer heraldry track; sigils as frontmatter not edges), 9 Bucket-C reverse-direction violations.

**One open question:** CREW_OF — agent recommended REJECT, Matt asked "why reject — sub qualifier or implicit via MEMBER_OF?" I responded with the three-path trade-off (loosen MEMBER_OF; accept CREW_OF as sibling to CAPTAIN_OF; reject) and leaned Path B. Matt didn't lock — flagged in continue prompt for the apply session.

## What's pending (not done this session)

The decisions are made but **not applied to architecture.md or the classifier prompt yet**. Pending apply work:
- Edit architecture.md to add 16 new rows + 2 description modifications
- Update `.claude/agents/prose-edge-classifier.md`: switch gap-filing default to "vocab FINAL — reject as `no-fitting-type-vocab-locked`, do NOT file vocabulary-gap questions"; add new types to the category-expansion paragraph; bump vocabulary count to 148; update reverse-direction both-sided list
- Write a Python script to append `resolved_at` + `resolution` fields to all 31 closed gap rows in `questions-for-matt.jsonl`
- Decide CREW_OF
- Then HAIKU-CUTOVER STEP 1 is done; Step 2 (burn `[LINK]` substitution) is next

→ continue: `progress/continue-prompts/2026-05-18-stage4-vocab-lock-apply.md`

## Files written this session

- `scripts/stage4-vocab-gap-analysis.py` — NEW (normalizer for 16-variant questions JSONL)
- `working/agent-fleet-specs/stage4-vocab-gaps-normalized.jsonl` — NEW
- `working/agent-fleet-specs/stage4-vocab-gaps-rollup.md` — NEW
- `working/agent-fleet-specs/stage4-vocab-lock-2026-05-18.md` — NEW (decision doc; Bucket D verdicts pending apply)
- `working/todos.md` — added "Stage 4 — Haiku Cutover Prep" section with 5 numbered todos
- `~/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/memory_staleness_policy.md` — NEW
- `~/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/MEMORY.md` — 2 index lines updated/added
- `~/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/project_pass1_prompt_v3_canonical.md` — completion counts corrected
- `CLAUDE.md` — pipeline table row 4 updated; Orchestration Rule 9 added
- `progress/continue-prompts/2026-05-18-stage4-haiku-cutover.md` — "Status from memory" passage corrected
- `history/session-details/session-055.md` — THIS FILE
- `progress/continue-prompts/2026-05-18-stage4-vocab-lock-apply.md` — handoff for apply work

## Lessons

1. **The "Status from memory" anti-pattern is real and just bit us.** Any continue prompt that says "Status from memory" — or any future variant where the drafter admits they didn't verify — is a red flag. CLAUDE.md Rule 9 now codifies the worklog-wins-when-they-disagree behavior. Memory staleness policy file adds the trust hierarchy explicitly.

2. **Schema lockdown discipline applies to more than vocab.** The `[LINK]` substitution, type-contract checks, suspicious-edges flagging are all the same shape of problem: eliminate decisions the model can fumble, OR mechanically validate the output. Stage 4 Haiku prep covers all five.

3. **Second-opinion-agent pattern is valuable.** Dispatched Sonnet agent overrode three of my leans (PURCHASED_FROM, BUILT, REPUTED_AS) and surfaced one I'd missed entirely (CAPTAIN_OF). Worth formalizing later as a `vocab-decision-reviewer` agent (captured as backlog).

4. **Split-by-confidence output shape worked, but my "obvious" threshold was miscalibrated.** I called PURCHASED_FROM and BUILT as lean-reject when both were actually borderline. Matt pushed back on both; second-opinion agent flipped me on both. When in doubt, lean toward surface-only.
