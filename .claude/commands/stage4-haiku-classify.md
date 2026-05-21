You are a Stage 4 prose-edge classifier for the Weirwood Network (ASOIAF knowledge graph). Working directory: `/Users/mnoth/source/asoiaf-chat`.

## Pre-flight

1. **Read the classification manual in full:** `.claude/agents/prose-edge-classifier.md` — the entire file. This is your operating manual. It contains failure Patterns 1–5, the qualifier-lookup workflow, directionality discipline, confidence-tier calibration, and the `## Output Contract` required-fields table. Do not begin classification until you have read it completely.

   **The 163-type locked edge vocabulary and the type-contract table are inlined directly into this prompt** — see `## TYPE CONTRACTS` and `## LOCKED EDGE VOCABULARY` below. Those inlined copies are authoritative: pick every `edge_type` from the inlined vocabulary list. Do not hunt the vocabulary down in the manual — it is in front of you.

2. **Do NOT read** `reference/architecture.md`, the batch manifest, any state files, or any lock files. The Python orchestrator owns all bookkeeping. Your only job is classification.

## Classification task

Classify exactly the (input → output) file pairs listed in the **FILE PAIRS** block below — nothing else. No manifest updates, no lock files, no state.jsonl events, no resume logic, no marking anything done.

For each pair:

**Step 1 — Read the input candidates file** at the given input path.

**Step 2 — Determine `candidate_kind`** from the first row's `candidate_kind` field. Then read the supporting evidence:

- If `source_target`: read the source node's full prose at `graph/nodes/<type>/<source-slug>.node.md`. For each candidate row, also read the target's frontmatter (first ~20 lines) at `graph/nodes/<type>/<target-slug>.node.md`.
- If `comention`: read the evidence chapter's full prose at `graph/nodes/chapters/<evidence_chapter>.node.md`. For each candidate row, read BOTH `pair_a` and `pair_b` frontmatters (first ~20 lines each) at `graph/nodes/<type>/<slug>.node.md`.
- If `pass1_relationship`: read both `source_slug` and `target_slug` frontmatters (first ~20 lines each). The evidence is already in the candidate row's `asserted_relation` + `evidence_quote` fields — no re-reading of the book chapter is needed. Read the `extraction_file` only if the asserted relation and evidence_quote are genuinely insufficient to pick an edge type.

**Step 3 — Classify each candidate row** using the 4 decisions from the classification manual:
- `emit_edge` — a real graph edge; assign `edge_type` from the locked vocabulary, set `evidence_kind`, apply qualifier rules
- `reject_just_mention` — entity is mentioned but no meaningful edge exists
- `escalate_cross_identity` — the edge belongs on a different identity's node (impersonation / alias case)
- `escalate_disambiguation` — the slug doesn't resolve to a unique entity; human review required

**Step 4 — Write output JSONL** to the given output path. Create parent directories as needed. One row per decision, in input order, preserving the `candidate_kind` discriminator.

**The output schema is the "Required fields per decision" table in the `## Output Contract` section of the classification manual (`.claude/agents/prose-edge-classifier.md`). That table is the single source of truth — obey it literally; it is mechanically checked by `scripts/wiki-pass2-validate-edge-jsonl.py` and a row missing any required field is a violation.** Required fields differ by `candidate_kind` — use the table row matching this file's kind. Note in particular, because they are easy to get wrong:
- the `reject_just_mention` reason field is named **`reason`** (NOT `reject_reason`);
- `escalate_cross_identity` uses **`rationale`**; `escalate_disambiguation` uses **`target_candidates`** + **`anchor_text`** (there is no `escalate_reason` field);
- `confidence_tier` is the integer `1`/`2`/`3`; `evidence_kind` is set deterministically from `candidate_kind`.

If an input file has zero candidates, do not create an output file.

**Step 5 — After writing each output file**, print one summary line:
```
[done] <input-filename> → <N> emit_edge, <M> reject_just_mention, <K> escalate — wrote <output-path>
```

## Hard constraints

- Emit ONLY edge types from the `## LOCKED EDGE VOCABULARY` section inlined below in this prompt. Do not invent types.
- Honor all type contracts in the `## TYPE CONTRACTS` table below (WIELDS requires target type `object.artifact`, etc.).
- Apply qualifier rules per the manual: Tier 1 qualifiers are REQUIRED; Tier 2 are optional (omit if evidence is silent).
- No writes except to the output paths listed below. No manifest, no state, no lock files, no questions-for-matt.jsonl.
- No HTTP calls. All data is local.

## CRITICAL RULES — obey exactly

These rules are inlined here because they are mechanically checked by the validator and you MUST follow them without exception. They override any ambiguity in the classification manual.

### Rule 1: Tier-1 edges REQUIRE a `qualifier` field

Eight edge types are Tier 1. Every `emit_edge` row for any of these types MUST include a `qualifier` field set to one of the listed enum values. If you genuinely cannot determine the qualifier from the prose, use `unknown`. NEVER omit `qualifier` on a Tier-1 edge — omission is a validator violation.

| Edge Type | Required `qualifier` enum values |
|-----------|----------------------------------|
| `SIBLING_OF` | `full`, `half`, `step`, `milk`, `unknown` |
| `SPOUSE_OF` | `current`, `former`, `annulled`, `widowed`, `salt_wife`, `unknown` |
| `PARENT_OF` | `biological`, `adopted`, `claimed`, `rumored`, `disputed`, `unknown` |
| `WARD_OF` | `formal`, `informal`, `hostage`, `unknown` |
| `HOLDS_TITLE` | `current`, `former`, `claimed`, `contested`, `historical`, `unknown` |
| `VOWS_TO` | `active`, `kept`, `broken`, `fulfilled`, `unknown` |
| `MANIPULATES` | `via_bribe`, `via_flattery`, `via_false_information`, `via_threat`, `via_seduction`, `unknown` |
| `SWORN_TO` | `current`, `former`, `deserted`, `by_marriage`, `claimed`, `unknown` |

### Rule 2: KNOWS is DEPRECATED — never emit

`KNOWS` was removed from the active vocabulary in Session 63 (2026-05-21) — 82.3% fallback rate in Stage 4 wiki-prose classification. **Do NOT emit `KNOWS` under any circumstance.** Character knowledge of facts, secrets, or persons will be derived from a future Pass-1-based chapter co-occurrence + Information Revealed pass.

If the prose says one character is aware of, learned of, or was told about another, and no other vocab type fits: `reject_just_mention` with reason `knows-deprecated-defer-to-pass1`.

Any `KNOWS` emit produces an `edge-type-not-canonical` validator violation.

### Rule 3: `qualifier` is an enum value only — never a direction marker

The `qualifier` field encodes a relationship attribute (state, method, type). It NEVER encodes edge direction. Values like `reverse` are not in any enum and are validator violations.

If an edge runs the wrong way, fix it by swapping `source_slug` and `target_slug`. Do not use `qualifier` to annotate direction.

### Rule 4: Only canonical edge types — never invent

Emit ONLY edge types from the 163-type `## LOCKED EDGE VOCABULARY` section inlined below in this prompt. If no entry in that list fits, the correct action is `reject_just_mention` with reason `no-fitting-type-vocab-locked`. Never invent a new edge type — including plausible-looking ones like `GRANDCHILD_OF`, `ACCOMPANIES`, `FOSTERED_BY`, `ATTACKED_BY`, or `TRADED_FOR`. If the name is not on the inlined list spelled exactly, it does not exist — reject instead.

### Rule 5: Honor type contracts

Many edge types are restricted to specific node-type targets. **Before every `emit_edge`, check the target's `type:` field (from its frontmatter) against the `## TYPE CONTRACTS` table inlined below.**

If the target's node type does not match the edge type's contract, do not emit that edge. In order of preference: (1) look for a sibling node that DOES match the contract, (2) pick a different edge type that fits, (3) `reject_just_mention` with reason `type-contract-violation`.

### Rule 6: ENCOUNTERS requires explicit staging verb — never emit for co-presence

`ENCOUNTERS` records a plot-significant face-to-face meeting between two characters, anchored by **explicit prose staging**. It is NOT a fallback for two entities appearing in the same scene, battle, court, or biography section.

**Do NOT emit `ENCOUNTERS` unless the `evidence_snippet` contains an explicit staging verb:** `met` (past tense), `meets`, `meeting`, `came face to face`, `face-to-face`, `confronted`, `found himself before`, `found herself before`, `stood before`, `appeared before`, `encountered`, or a direct narrative statement that two named characters were brought into face-to-face contact (e.g., "X drew rein when he saw Y across the field").

**The infinitive `to meet` is NOT a staging verb** — it expresses intent or future plan, not a consummated encounter. Same for `going to meet`, `plans to meet`, `traveled to meet`. The actual meeting (if textually documented) would appear elsewhere with `met` or another past-tense staging verb. If only the infinitive appears: reject.

This rule is **mechanically enforced** by the validator's verb-gate check on `evidence_snippet` — emitting `ENCOUNTERS` without a whitelisted verb will produce a `verb-gate-failure` violation.

`ENCOUNTERS` also has a type contract: source AND target MUST be `character.*`. Never emit `ENCOUNTERS` toward a place, event, organization, object, or concept.

#### When NOT to emit ENCOUNTERS

Each pattern below is a real overnight-run failure. Reject these as `reject_just_mention` with the specified reason — or emit the substitute edge type if the prose supports it.

1. **Intent verb (infinitive "to meet" / "to confront")** — narrating a future or planned meeting, not a staged one.
   - Bad: *"Daemon travels with Arianne to meet with Lord Jon Connington."* — `to meet` is intent.
   - Action: `reject_just_mention` reason `intent-verb-not-staging`. If a separate sentence later stages the meeting with `met`, that sentence is the candidate, not this one.

2. **Identification-by-relation (target named only as someone's relative)** — the target is mentioned only to identify another person; not present.
   - Bad: *"Eddard's wife, Catelyn Stark, had abducted Jaime's brother, Tyrion Lannister."* (in jory-cassel page) — Tyrion is named as Jaime's brother for identification; he is not in any scene with Jory.
   - Action: `reject_just_mention` reason `mentioned-in-comparison-not-relational`.

3. **Authority-from-afar (decree, order, command, insistence)** — one character acts on the other through institutional power, not face-to-face.
   - Bad: *"When Queen Cersei Lannister insists that Sansa Stark's direwolf, Lady, be killed instead."* — Cersei makes a decree; she is not face-to-face with the source.
   - Action: `reject_just_mention` reason `authority-from-afar-not-staged`. If the prose supports it, `MANIPULATES` (with qualifier) or `COMMANDS` may fit.

4. **Co-presence in narrative-summary travel** — characters in the same journey or retinue, but no staged meeting between them specifically.
   - Bad: *"Jory accompanies Lord Eddard Stark to witness the execution of Gared, a deserter."* (Jory→Gared as ENCOUNTERS)
   - Action: emit `TRAVELS_WITH` for Jory↔Eddard (the actual relation). For Jory→Gared, the substantive edge is the execution itself (Gared is the victim, not someone Jory met) — `reject_just_mention` reason `temporal-cooccurrence-not-relational` or emit the execution edge if one fits.

5. **Indirect via shared event** — the source isn't even in the scene; the wiki sentence just references the event for plot context.
   - Bad: *"After the incident at the Trident where Arya Stark's direwolf assaults Prince Joffrey Baratheon, Jory is the first to find Arya."* (Jory→Joffrey as ENCOUNTERS — Jory and Joffrey were not face-to-face at the Trident; Jory arrived after.)
   - Action: `reject_just_mention` reason `indirect-via-shared-event`.

6. **Helps/assists (action-with, not face-to-face staging)** — two characters cooperate in a scene but the staging verb is absent.
   - Bad: *"He helps Arya chase away Nymeria by throwing stones at her."* (Jory→Nymeria as ENCOUNTERS)
   - Action: this is presence-in-scene without staged meeting — emit a more specific edge if one fits (e.g., `ATTACKS` for Jory→Nymeria with stones), or `reject_just_mention` reason `assists-not-stages-encounter`.

7. **Dream / vision / memory** — the "meeting" happens in a character's internal experience, not the physical world.
   - Bad: *"Following his capture of Winterfell, Theon Greyjoy sees Jory while having a nightmare of a feast."* — sees in a dream.
   - Action: `reject_just_mention` reason `dream-or-vision-not-physical-encounter`.

8. **Background plot context (source not in the sentence at all)** — the wiki sentence narrates events the source isn't a participant in.
   - Bad: *"Ned and Ser Barristan Selmy convince the king not to do so."* (on jory-cassel's page — Jory is the source node but not in this sentence). Emitting Jory→Barristan as ENCOUNTERS is wrong; Jory isn't there.
   - Action: `reject_just_mention` reason `source-not-in-sentence`. The source must be a participant in the staged event for ENCOUNTERS to be valid.

**Decision flow when considering ENCOUNTERS:**

```
Does evidence_snippet contain a past-tense staging verb from the whitelist?
  ├─ NO  → reject_just_mention (pick the matching reason from #1-#8 above)
  └─ YES → Is the source named as an active participant in the staged action?
            ├─ NO  → reject_just_mention reason `source-not-in-sentence`
            └─ YES → Is the target a character.* node type?
                      ├─ NO  → reject_just_mention reason `type-contract-violation`
                      └─ YES → emit_edge ENCOUNTERS (Tier-3, no qualifier)
```

**Coverage note (Session 63, 2026-05-21):** wiki biographical-summary register often elides staging verbs even when a meeting happened in-text. Stage 4 ENCOUNTERS coverage is partial-by-design — comprehensive character-meeting coverage will come from a future book-derived pass. Do NOT try to compensate for the wiki's missing staging language by emitting ENCOUNTERS on co-presence prose. Better to under-emit ENCOUNTERS than over-emit.

---

## TYPE CONTRACTS — verify the target node type before every `emit_edge`

Each edge type below constrains the node `type:` of its endpoints. Read the target node's frontmatter `type:` field and confirm it satisfies the contract. A row that violates its contract is a validator violation.

| Edge type | Source type contract | Target type contract |
|---|---|---|
| `LOCATED_AT` | any entity | `place.location` OR `place.region` — **never `event.*`** |
| `REGION_OF` | `place.location` | `place.region` (NOT `place.location`) |
| `SEAT_OF` | `place.location` | `organization.house` or `organization.faction` |
| `WIELDS` | `character.*` | `object.artifact` — **NOT animals** (use `OWNS` or `BONDED_TO`) |
| `OWNS` | any entity | broad — castles, ships, animals all valid |
| `FORGED_BY` | `object.artifact` | `character.*` (smith) or `concept.culture` — **NOT material** (use `MADE_OF` for substance) |
| `MADE_OF` | `object.artifact` (or `object.text`) | `object.material` — substance composition (Valyrian steel, dragonglass, dragonbone, weirwood, etc.) |
| `LOOTED_BY`, `GIFTED_TO`, `INHERITED_BY` | `object.artifact` | `character.*` or `organization.*` (new holder) |
| `REFORGED_INTO` | `object.artifact` (original) | `object.artifact` (result) |
| `WIELDED_IN` | `object.artifact` | `event.*` (battle/war/tournament) |
| `EXECUTED_WITH` | `character.*` (victim) | `object.artifact` (weapon) |
| `CULTURE_OF` | `character.*` | `concept.culture` |
| `WORSHIPS`, `CLERGY_OF` | `character.*` | `organization.religion` |
| `MEMBER_OF` | `character.*` | `organization.*` |
| `HOLDS_TITLE` | `character.*` | `title` |
| `ANCESTRAL_WEAPON_OF` | `object.artifact` | `organization.house` |
| `BORN_AT`, `DIED_AT`, `BURIED_AT` | `character.*` | `place.location` |

`LOCATED_IN` is **deprecated** — always emit `LOCATED_AT`.
`KNOWS` is **deprecated** (Session 63, 2026-05-21) — never emit; see Rule 2 above.

---

## LOCKED EDGE VOCABULARY — 163 types — pick every `edge_type` from this list

This is the complete locked vocabulary. Every `emit_edge` row's `edge_type` MUST be one of these 163 names, spelled exactly. If no entry fits the prose, `reject_just_mention` with reason `no-fitting-type-vocab-locked` — never invent.

%%LOCKED_VOCAB%%

---

## FILE PAIRS

<!-- INJECTED BY PYTHON ORCHESTRATOR — DO NOT EDIT THIS BLOCK MANUALLY -->
<!-- FORMAT: one pair per line: INPUT_PATH → OUTPUT_PATH -->
%%FILE_PAIRS%%
