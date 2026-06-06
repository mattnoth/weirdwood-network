# Edge & Event-Modeling — Diagnosis & Recommendation

_Analysis of `EDGE_INVENTORY_REPORT.md` (Weirwood Network / asoiaf-chat, commit `f04dbc8a2`, 2026-06-04). All citations are to that report unless prefixed otherwise._

---

## Recommendation in one paragraph

**Reify the death/violence family (`KILLS`, `KILLED_BY`, `KILLED_WITH`, `EXECUTES`, `EXECUTED_WITH`, `POISONS`, `SACRIFICES`, `DIED_AT`), the ceremony family (the wedding/tourney behind `MARRIES_OFF`, `PROPOSED_AS_BRIDE`, `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY`, `OFFICIATES`), the siege/assault sub-events (`BESIEGES`, and `ATTACKS`/`ASSAULTS`/`TORTURES` _when_ an instigator or instrument is named), the conspiracy (`CONSPIRES_WITH`), and the guest-right violation occasion (`VIOLATES_GUEST_RIGHT`) into fine-grained event nodes — extending the event-node mechanism the project _already uses for battles/wars/tournaments_ (§Exec 12, §6.7) downward to individual killings, weddings, and massacres.** Each event node becomes the n-ary hub; participants hang off it by role; and a deterministic projector _materializes_ the single highest-frequency dyad (agent→patient) back into `edges.jsonl` so 1-hop traversal queries keep working and are now **consistent because they are generated from one source of truth rather than independently guessed.** This is the synthesis of the brief's two fix-families (§1.6): reification supplies the canonical form, the projection is the canonical head-selection output. **Canonicalize** the genuinely-dyadic-but-direction-prone relations (`COMMANDS`, `SERVES`, `TUTORS`, `TEACHES`, `HEALS`, `CAPTURES`, `RESCUES`, `BETRAYS`, `DECEIVES`, plus all of the Emotional/Perceptual block) by **enforcing the per-type head rule architecture.md already declares in its Directionality column** — the rule exists, it is simply not applied. **Leave alone** the true binaries (`PARENT_OF`, `SIBLING_OF`, `SPOUSE_OF`, the kinship shortcuts, `MEMBER_OF`, `SWORN_TO`, `LOCATED_AT`, the spatial block). **Single biggest root cause of the "hallucination-look":** there is no _enforced_ head-selection anywhere upstream — the Pass-1 `| Character A | Relationship | Character B |` table (`mechanical-extractor.md:176-178`) carries no head rule, and the deterministic `python-map` typer then anchors `source` on the **grammatical subject of the matched sentence** (§Exec 7, §4.4.4), which is exactly the §1.8 trap. The same multi-chapter event, narrated from different POVs, lands a different grammatical subject in the source column each time. That is underdetermination injected at the extraction layer, not model hallucination.

---

## 1. Diagnosis

### 1.1 What is actually producing the inconsistency

The report's headline artifacts are all one mechanism seen from different angles. Framed as **underdetermination** (§1.4 of the brief), not error:

1. **No enforced canonical form exists, but a _latent_ one does.** The brief asks whether a head-selection rule exists "anywhere." The precise answer is sharper than the report's "NO canonical head-selection rule exists in the Pass-1 extractor prompt" (§Exec 4): a per-type head rule **does** exist — `architecture.md`'s **Directionality column** declares `KILLS = Killer → Killed`, `COMMANDS = Commander → Subordinate`, `TUTORS = Tutor → Student`, etc. (Appendix A). It is a complete, machine-applicable head specification. The defect is that **nothing enforces it.** Pass-1 emits free text with no direction convention; the `python-map` then fills `source`/`target` from **table column position**, which the Pass-1 model filled from **POV narrative emphasis / grammatical subject.** So the canonical form is written down and then overridden by surface syntax. This is a more actionable finding than "no rule exists," because the fix for the canonicalize bucket is largely "apply the column you already wrote."

2. **The §1.8 trap is confirmed in the data, deterministically.** `cressen KILLS melisandre` (Cressen "ran afoul of Melisandre and died"); `tyrion BETRAYS shae` (Shae betrayed Tyrion); `arya CAPTURES sandor` (Sandor captured Arya) (§4.4.4). In each, the `asserted_relation` **self-witnesses** the inversion ("Killed by", "Betrayed by", "Conflicted captor-dependent"). The report's own attribution is exact: *"the python-map typer takes the grammatical subject of the matched sentence, regardless of whether that subject is the semantic agent"* (§4.4.4). This is grammatical-subject leakage piped straight into the data model — the precise failure the brief flags as "very likely a root cause, not a symptom."

3. **The divergent-collapse is the same trap across POV chapters.** The Red Wedding (§4.4.1) is one n-ary event projected onto incompatible heads: `roose-bolton BETRAYS robb-stark` (python-map, Catelyn VII) vs `walder-frey BETRAYS robb-stark` (sonnet, same chapter) vs `lothar-frey CONSPIRES_WITH roose-bolton` (sonnet, epilogue). Robb has **no `KILLS` row at all**; Catelyn's killer is the knife-wielder `raymund-frey` while Robb's killer-slot is the political agent `roose-bolton`. `VIOLATES_GUEST_RIGHT` appears with **7 subject × 8 target choices across 5 chapters with no event-id joining them** (§4.4.1). Each row independently picked a defensible projection of a head-less event; nothing reconciles them because there is no canonical form and no hub to anchor on.

4. **The project already named this — and flinched.** The S58 batch-0020 Opus audit (§6.2) is the project's own un-theorized diagnosis: *"the graph lacks fine-grained event nodes (individual weddings, feasts, sieges), so the classifier has no correct target and improvises."* The chosen mitigation was `reject_just_mention` with `no-event-node-available` (`prose-edge-classifier.md:172-173`, §5.5) — i.e. **drop the edge rather than mint the hub.** That converts a head-selection problem into silent data loss. The Purple Wedding (§4.4.3) is the cost: the only encoded fact about Joffrey's death is **Tyrion's false confession** (`tyrion POISONS joffrey, "Claims to have poisoned (unverified)"`); Olenna, Littlefinger, and the strangler are entirely absent. The historical truth was unrepresentable, so it went unrepresented.

5. **The Aerys II slug split (§4.4.2) is a second, independent root cause** worth separating from head-selection: entity-resolution failure. `KILLS jaime-lannister → aerys-targaryen` while every other Jaime↔Aerys edge resolves to `aerys-ii-targaryen`; both node files exist, so traversing the canonical Mad King node never reaches the regicide. This is not underdetermination — it is a deterministic resolver miss, and it is independently fixable (and already fixed in the gated Haiku bulk). I flag it because the brief asks for the root cause and this one would survive any amount of head-selection work.

### 1.2 My binary-vs-event re-classification, and where I disagree with the report

I ran the §1.7 diagnostic (>2 participants / carries own properties / negatable-as-a-unit) independently. I concur with the report's broad split (~76 binary / ~82 event-like) and with its top-12 n-ary candidates (§3.4). Disagreements, with reasoning:

- **`DUELS` — report implies event-like; I classify it as canonicalizable binary.** A duel is symmetric, two-participant, and rarely carries an independent instigator. Its only event-ish property is location/outcome, which is low-value here (4 rows). Reifying it mints near-empty hubs. **Keep binary (symmetric); canonicalize by slug order.** (Minor.)
- **`ATTACKS` / `ASSAULTS` / `TORTURES` — report classes as n-ary; I classify as _conditionally_ event-like.** The bulk of these rows are genuinely 2-ary (creature-on-warg, person-on-person, Ramsay-on-Theon). The n-ary tell fires **only when the `on_command` qualifier or a named instrument is present** (Appendix A: `ATTACKS` enum includes `on_command`; the Mountain-at-Tywin's-command case). **Disposition: canonicalize by default, reify the row only when evidence names an instigator/instrument.** This avoids over-minting hubs for the 32 `ASSAULTS` / 22 `ATTACKS` rows that are simple dyads.
- **Captivity family (`PRISONER_OF`, `IMPRISONED_AT`, `GUARDS`) — report lumps all 5 captivity types as n-ary needing reification (§3.4 #9); I split them.** `CAPTURES` and `IMPRISONS` are **events** (reify: captor + captive + location + war-context). But `PRISONER_OF` and `IMPRISONED_AT` are **derived states**, best left as binary _projections of_ the capture event, not separate hubs. Reifying the state as well as the event double-models. **Disposition: reify `CAPTURES`/`IMPRISONS` as the event; keep `PRISONER_OF`/`IMPRISONED_AT`/`GUARDS` as binary state edges materialized from it.**
- **The 278 multi-type pairs (§4.4.5) are NOT an n-ary problem and must NOT be reified.** `tyrion → jaime` carrying 13 distinct edge types (ASSAULTS, LOVES, MOURNS, RESENTS, …) is a **temporal-snapshot** problem, not a head-less-event problem. The report itself notes the project's correct answer here is per-edge `(book_order, chapter_number)` temporal scoping (Session 76, §6.4). I **agree with the report** that reification is the wrong tool for this case, and I want to state it explicitly so the recommendation is not misread as "reify everything." Temporal scoping stays; reification is orthogonal.
- **`SPIES_ON` / `INFORMS` (§3.4 #11) — report calls n-ary (spy+surveilled+handler); I classify as adequately-handled binary.** The handler/surveilled split into two reverse-paired edges (`SPIES_ON` person→surveilled, `INFORMS` person→handler) is the project's reverse-pair pattern (§3.5) **working correctly** — both third roles are reachable. This is a standing relationship, not an instantaneous event; a hub adds little. **Keep binary.**

Where the report is exactly right and I add nothing: the **death/killing family** is the canonical reify target (method-as-qualifier — `KILLS` enum `in_combat`/`by_proxy`/`by_arrow` per Appendix A — is the schema confessing it is cramming instrument and instigator onto a 2-ary edge); the **ceremony family**; `CONSPIRES_WITH` (the only type whose own description says "two or more parties," §Exec 3); and `BESIEGES` (a war sub-event that should be an `event.*` node, exactly as the S58 audit found for the storming-of-the-Crag, §6.2).

### 1.3 Where the inconsistency originates (the causal chain)

```
Pass-1 mechanical-extractor (Opus, POV-bound, chapter-isolated)
  → free-text | Char A | Relationship | Char B | table, NO head rule, NO event rows
  → grammatical subject of the POV sentence lands in column A
        │
        ▼
stage4-pass1-edge-candidates.py (python-map)
  → column A == source, column B == target  (head locked by word order)
  → architecture.md Directionality column NEVER consulted
        │
        ▼
stage4-tail-classifier.py (LLM)
  → can only TYPE or REJECT; CANNOT swap endpoints (Rule 5; JSON schema has no swap field)
  → so a mis-headed row is either typed-as-is (inversion persists) or rejected (data lost)
        │
        ▼
edges.jsonl  → divergent heads, inversions, missing event-ids, dropped n-ary roles
```

The chapter-isolation rule (`mechanical-extractor.md:20-28`, §5.2) guarantees the divergence: the Red Wedding spans ASOS Catelyn VII → Arya XII → Epilogue, and each chapter is extracted independently, so the same massacre is encoded three times with three heads and no cross-chapter event-id. **This is structural, not stochastic** — it would reproduce on a re-run.

---

## 2. Disposition Table

`disposition ∈ {Reify, Canonicalize, Keep-binary, Conditional}`. Rationale tied to §1.7 tests: **[P]** >2 participants, **[A]** carries own properties (time/place/instrument/outcome), **[N]** negatable/qualifiable as a unit.

| Edge type / family | My classification | Disposition | Rationale (§1.7) | Conf. | Depends on report gap? |
|---|---|---|---|---|---|
| `KILLS`, `KILLED_BY`, `KILLED_WITH`, `EXECUTES`, `EXECUTED_WITH`, `POISONS`, `DIED_AT` | event | **Reify** (death event hub; materialize agent→patient dyad) | [P] killer+victim+instigator+instrument+location; [A] method-as-qualifier is the tell; [N] "the killing that was ordered but never happened" | High | No |
| `SACRIFICES` | event | **Reify** (ritual event; adds `recipient-deity`/`purpose` role wholly missing today) | [P][A][N]; "sacrificed-to" axis unrepresentable on an edge (§3.6) | High | No |
| Wedding behind `SPOUSE_OF`/`MARRIES_OFF`/`PROPOSED_AS_BRIDE`/`OFFICIATES` | event (+ `SPOUSE_OF` is the resulting binary state) | **Reify the wedding event**; **Keep `SPOUSE_OF` binary** | [P] bride+groom+arranger+officiant+venue; `PROPOSED_AS_BRIDE` desc admits 3-party (§3.4) | High | No |
| `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` | event | **Reify onto the tournament node** | [P] champion+recipient+tourney+witnesses; "chains to political consequences" (§3.4) | High | No |
| `BESIEGES` | event | **Reify** (siege sub-event of a war; reuse `event.battle`) | [P][A][N]; S58 storming-of-the-Crag precedent (§6.2) | High | No |
| `CONSPIRES_WITH` | event/standing-plot | **Reify** (conspiracy hub; conspirator role-edges) | [P] "two or more parties" in its own description (§Exec 3) | High | No |
| `VIOLATES_GUEST_RIGHT` | event-attached | **Reify onto the hospitality-violation event** (Red Wedding) | [P] 7×8 subject/target spray with no join (§4.4.1) | High | No |
| `CAPTURES`, `IMPRISONS` | event | **Reify** (capture/imprisonment event) | [P][A]; captor+captive+location+war | Med | Partly — vol. of multi-role rows |
| `PRISONER_OF`, `IMPRISONED_AT`, `GUARDS` | derived state | **Keep binary** (materialize from capture event) | fails [P]; a state, not a hub — _disagree with report's lump_ | Med | No |
| `ATTACKS`, `ASSAULTS`, `TORTURES` | conditional | **Conditional**: canonicalize by default; reify the row iff instigator/instrument named | [P] only when `on_command`/instrument present | Med | **Yes** — needs instigator-frequency count |
| `COMMANDS`, `SERVES`, `ADVISES`, `APPOINTS`, `DEPOSES`, `RULES` | binary (direction-prone) | **Canonicalize** (enforce declared head) | dyadic; inversion bug is the issue, not arity | High | No |
| `TUTORS`, `TEACHES`, `HEALS`, `RESCUES`, `BETRAYS`, `DECEIVES`, `DECEIVED_BY`, `MANIPULATES` | binary (direction-prone) | **Canonicalize** (enforce declared head; hint-lexicon flip) | dyadic; self-witnessing inversions (§4.4.4) | High | No |
| `DUELS` | binary (symmetric) | **Keep binary / canonicalize by slug** | fails [P]; _disagree with report's event lean_ | Med | No |
| Emotional/Perceptual block (`LOVES`,`HATES`,`FEARS`,`MOURNS`,`RESENTS`,`TRUSTS`,`DISTRUSTS`,`RESPECTS`,`PROTECTS`,`PERCEIVED_AS`) | binary (POV-directional) | **Keep binary; canonicalize** (perceiver→perceived; POV is the head, by design §6.6/§6.8) | dyadic, fixed role; head = POV character | High | No |
| `SPIES_ON`, `INFORMS` | binary (reverse-pair) | **Keep binary** (_disagree with report's n-ary call_) | reverse-pair already exposes the third role (§3.5) | Med | No |
| Kinship: `PARENT_OF`, `SIBLING_OF`, `SPOUSE_OF`, `UNCLE_OF`/`NEPHEW_OF`, `COUSIN_OF`, `MILK_BROTHER_OF`, `NURSED_BY`/`WET_NURSE_OF`, `STEP_*`, `IN_LAW_OF`, `HEIR_TO`, `ANCESTOR_OF`, `CADET_BRANCH_OF` | true binary | **Keep binary** (untouched) | fails all three; `PARENT_OF` is the §1.7 archetype; data is clean (§4.4.9) | High | No |
| Spatial: `LOCATED_AT`, `BORN_AT`, `BURIED_AT`, `SEAT_OF`, `REGION_OF`, `TRAVELS_TO` | binary | **Keep binary** (`TRAVELS_TO` origin → optional metadata, not a hub) | dyadic; place edges | High | No |
| Possession: `WIELDS`, `OWNS`, `MADE_OF`, `FORGED_BY`, `ANCESTRAL_WEAPON_OF`, `CAPTAIN_OF`, `CREW_OF`, `BONDED_TO` | binary | **Keep binary** (`WIELDED_IN`/`GIFTED_TO` link to event hubs where one exists) | dyadic possession states | High | No |
| Factional/Political binaries: `MEMBER_OF`, `SWORN_TO`, `ALLIES_WITH`, `OPPOSES`, `HOLDS_TITLE`/`HELD_BY`, `FOUNDED`, `NEGOTIATES_WITH` | binary | **Keep binary** | dyadic; reverse-pairs already handle traversal | High | No |
| Identity: `SAME_AS`, `ALIAS_OF`, `DISGUISED_AS`, `IMPERSONATES` | binary (resolution) | **Keep binary** (orthogonal — identity layer, §6.6) | dyadic by construction | High | No |
| Causal/Plot: `CAUSES`, `TRIGGERS`, `ENABLES`, `MOTIVATES`, `PREVENTS` | binary-between-events | **Keep binary** — and **reuse for the causation decision** (§4) | event→event/actor; already the right shape | High | No |
| Narrative/Prophecy/Evidentiary blocks | binary | **Keep binary** | analytical edges, dyadic | High | No |

**Multi-type pairs (278) and contradictory-arc edges:** **not in scope for reification** — addressed by the existing temporal-scoping work (§6.4), which I endorse.

---

## 3. Target Schema

The graph's notation is **JSONL edge rows** + **YAML-frontmatter Markdown nodes** (§4.2, §2.2). The reified shape reuses existing conventions: event nodes already exist as `type: event.battle|war|tournament` (§2.1). I extend the `event.*` family downward and add a **small, closed role-edge set** rather than per-killing vocab (respecting the project's anti-sprawl instinct, §3.7).

### 3.1 Fine-grained event node (the hub)

New leaf types under `Event` (mirrors existing `event.battle`):

```yaml
---
name: "The Red Wedding"
type: event.massacre          # new leaves: event.death, event.killing, event.wedding,
slug: red-wedding             #   event.execution, event.sacrifice, event.siege,
aliases: []                   #   event.massacre, event.conspiracy, event.capture
confidence: tier-1
node_version: 1
pass_origin: pass1-event-reification
part_of: war-of-the-five-kings   # optional; mirrors PART_OF battle→war
occurred: { book: asos, chapter: asos-catelyn-07 }   # event time (frontmatter, not an edge)
outcome: "Northern host destroyed; Robb and Catelyn Stark killed"
---
```

Event-node **slug identity** is deterministic (entity resolution, §5.4): `slug = kebab(primary_title)` where `primary_title` is taken from the gated Haiku bulk's `**<title>**` field when present (§4.6), else synthesized as `{event-type}-{primary-victim-or-honoree}-{book}`. A multi-chapter event (Red Wedding spans 3 chapters) resolves to **one** slug via title-normalization + participant-overlap dedup.

### 3.2 Role-edges (closed set — 6 new types, reusing existing where possible)

The hub is the `target`; participants are `source`. **Reuse what already exists**: `LOCATED_AT person/event→place`, `PART_OF battle→war`, `FIGHTS_IN`/`PARTICIPATES_IN`/`ATTENDS`/`OFFICIATES person→event`, `WIELDED_IN artifact→event` are all already in the vocab (Appendix A) and already point at event nodes. **Add only the roles the schema cannot currently express:**

| New role-edge | Direction | Replaces today's lossy projection |
|---|---|---|
| `AGENT_IN` | actor → event | the "killer" slot of `KILLS` |
| `VICTIM_IN` | patient → event | the "killed" slot of `KILLS`/`KILLED_BY` |
| `INSTIGATED` | commander → event | `KILLS qualifier=by_proxy`, `ATTACKS qualifier=on_command` (the lost instigator) |
| `INSTRUMENT_IN` | weapon → event | `KILLED_WITH`/`EXECUTED_WITH` (already artifact→event-ish; fold in) |
| `DIRECTED_AT` | recipient-deity / purpose → event | `SACRIFICES` "sacrificed-to" axis (today unrepresentable, §3.6) |
| `CONSPIRATOR_IN` | plotter → conspiracy event | the symmetric `CONSPIRES_WITH` spray |

Worked example — the Red Wedding as a hub (replaces the scattered rows in §4.4.1):

```jsonl
{"edge_type":"INSTIGATED","source_slug":"walder-frey","target_slug":"red-wedding","evidence_ref":"...asos-catelyn-07.md:..."}
{"edge_type":"INSTIGATED","source_slug":"roose-bolton","target_slug":"red-wedding","evidence_ref":"..."}
{"edge_type":"AGENT_IN","source_slug":"raymund-frey","target_slug":"red-wedding","qualifier":"by_blade"}
{"edge_type":"VICTIM_IN","source_slug":"robb-stark","target_slug":"red-wedding"}
{"edge_type":"VICTIM_IN","source_slug":"catelyn-stark","target_slug":"red-wedding"}
{"edge_type":"AGENT_IN","source_slug":"hosteen-frey","target_slug":"red-wedding"}
{"edge_type":"VICTIM_IN","source_slug":"lucas-blackwood","target_slug":"red-wedding"}
{"edge_type":"LOCATED_AT","source_slug":"red-wedding","target_slug":"the-twins"}
{"edge_type":"PART_OF","source_slug":"red-wedding","target_slug":"war-of-the-five-kings"}
{"edge_type":"VIOLATES_GUEST_RIGHT","source_slug":"red-wedding","target_slug":"robb-stark"}
```

"Who violated guest-right at the Red Wedding?" is now `red-wedding ←VICTIM_IN/←INSTIGATED` neighborhood, not a union over 8 unjoined rows.

### 3.3 The materialized dyad (the canonical head-selection OUTPUT)

To preserve 1-hop query ergonomics (the reason the project added reverse edges, §3.5), a **deterministic projector** generates the primary dyad from the hub — it is no longer guessed:

```
for each event hub E with a single primary AGENT_IN a and primary VICTIM_IN v:
    emit  {edge_type: <type-from-event-class>, source: a, target: v,
           typed_by: "event-projection", evidence_event: E.slug, confidence_tier: 1}
# event.death/killing → KILLS ;  event.execution → EXECUTES ;
# event.wedding → SPOUSE_OF (bride↔groom) ;  event.sacrifice → SACRIFICES
```

Because every `KILLS` row is now **generated from the hub's role assignment**, the divergent-head problem is gone by construction: there is exactly one projection, and it is reproducible. Secondary roles (instigator, instrument, co-victims) remain reachable through the hub at 2 hops — acceptable, because today they are unreachable at any number of hops. `confidence_tier` (currently uniformly 1, §Exec 10) can finally do work: hub-asserted roles = tier 1, machine-projected dyads = tier 2, so consumers can distinguish witnessed from derived.

### 3.4 Canonical head rule (for the Canonicalize bucket)

For every direction-prone binary, **the head is the participant playing the agentive role named in `architecture.md`'s Directionality column** — it is already declared per type (`KILLS=Killer→Killed`, `COMMANDS=Commander→Subordinate`, `TUTORS=Tutor→Student`, …). The machine-applicable rule:

```
1. Look up the type's declared (agent_role → patient_role) from architecture.md Directionality.
2. Determine which endpoint is the agent from the EVIDENCE SEMANTICS, never word order:
   a. Scan asserted_relation / hint for a REVERSE-SIGNALLING pattern from a fixed lexicon:
      "killed by", "betrayed by", "captured by", "tutored by", "X of <subject>" (possessive-
       patient: "Captor of", "Killer of" → the named party is PATIENT, current source is AGENT),
       passive "was <verbed> by". On match → FLIP source/target.
   b. If no signal and direction is ambiguous → REJECT (do not guess). [matches Rule 13 intent]
3. NEVER anchor on the grammatical subject of evidence_quote.  [§1.8 — this is the active bug]
Tie-breakers: symmetric types (SIBLING_OF, ALLIES_WITH, DUELS, …) → order endpoints by slug,
  emit once; the reverse is implied. POV/perception types → source is always the POV character.
```

This is implementable today as a deterministic post-`python-map` normalizer keyed on the `asserted_relation`/`hint` lexicon the report shows already self-witnesses the bug (§Exec 7).

---

## 4. Causation Modeling Decision (instigator vs executor — §1.5)

**Decision: one event node carrying distinct role-edges (`AGENT_IN` for the executor, `INSTIGATED` for the commander) — NOT two event nodes joined by a causal edge — as the default. Reserve the two-node causal form for the rare case where the ordering is itself an independently-attested, separately-narrated event, and link it with the _existing_ `CAUSES`/`ENABLES` vocabulary.**

Justification against the project's stated query goals (§6.1 — "traversed by agents to answer who-did-what / connection questions"):

- **It matches the reification the project already does.** A battle node already collects all participants via `FIGHTS_IN`; a killing node collecting executor + instigator via `AGENT_IN`/`INSTIGATED` is the identical pattern one level finer. Consistency with the existing 371 event nodes is worth more than theoretical purity.
- **It preserves the project's hard-won anti-collapse rule.** Stage-4 GATE 2 forbids `tywin KILLS brandon` ("A orders B to do X to C is NOT an A→C edge," §5.4). The hub honors this automatically: instigator and victim are **both spokes off the hub, never directly connected.** "Who ordered Robb's death?" = `red-wedding ←INSTIGATED`; "who struck the blow?" = `←AGENT_IN`. Both answerable, neither conflated.
- **Two-nodes-per-act would mint empty ordering-nodes.** The prose rarely gives the ordering its own scene with its own evidence_quote; you would synthesize `the-ordering-of-X` hubs with one inbound edge and no narrative body. That is the over-modeling the project's "collapse, not split" precedent (§2.4, Free Folk = one node) exists to prevent.
- **When the antecedent IS a real event, the causal edge is still available.** Tywin's planning of the Red Wedding, if it ever earns its own node, links `tywin-plot → red-wedding` via `CAUSES`/`ENABLES` (Appendix A, already in vocab). So the two-node form is not lost — it is reserved for when it is earned, exactly as `event.battle` nodes are minted only for named battles.

**Query trade-off, stated honestly:** one-node-multi-role makes "what did Tywin _cause_" a role-scan over hubs Tywin instigated (easy) but makes a pure causal chain ("ordering → killing → war") a multi-hop over heterogeneous edge types (harder) until/unless the antecedent is reified. Given the project's queries are participant-centric ("who killed/betrayed/mourns X"), not causal-chain-centric, this is the right side to optimize.

---

## 5. Pipeline Remediation

Cleaning data without fixing the generator just reintroduces variance (brief §2.5). Concrete changes, upstream to downstream:

### 5.1 Pass-1 mechanical-extractor (`mechanical-extractor.md`)

The extractor is deliberately POV-bound and analysis-free (§5.2) — do **not** ask it to do semantic head-selection it structurally cannot (it sees one POV chapter). Instead:

- **Promote the gated Haiku bulk's Events table into Pass-1 proper.** The bulk already emits an `**<title>** — <description>` event format that **clusters multi-target killings under one title** (`**Jaime's kills are revealed**` → 3 KILLS targets, §4.6). Add a `## Events Observed` table to the Pass-1 schema: `| Event title | Event type | Participants (role: name; …) | Evidence |`. This captures the n-ary structure at the source instead of forcing a subject/object pair. The `**title**` is the seed event-id.
- **Keep `## Relationships Observed` for the genuinely-binary relations**, but add one instruction: *"For the Character A / Character B columns, place the entity performing the action (per the relationship verb) in column A. If the sentence is passive or A is the one acted upon, still put the actor in A. Do not copy the grammatical subject of the sentence."* This is a cheap nudge; the deterministic normalizer (5.3) is the real enforcement.

### 5.2 Stage-4 tail-classifier (`stage4-tail-classifier.py`) — give it an event exit

The classifier can currently only TYPE or REJECT (§5.3), which is why the S58 audit's only mitigation was `reject` (§6.2). **Add a third decision shape** so an n-ary occasion routes to a hub instead of being dropped:

```json
{"idx": N, "decision": "emit_event_role",
 "event_type": "event.death|event.wedding|...",
 "event_title": "<verbatim **title** or synthesized>",
 "role": "AGENT_IN|VICTIM_IN|INSTIGATED|INSTRUMENT_IN|DIRECTED_AT|CONSPIRATOR_IN"}
```

Update the prompt: replace the dead-end in Rule 12 / the co-presence trap (*"if the occasion has no event node, reject"*, §5.5) with *"if the occasion is a typed event (killing, wedding, siege, sacrifice, conspiracy), emit_event_role against the event hub — create the hub if absent. Reject only true co-presence with no event."* This directly converts the project's biggest data-loss source into data capture. Keep Rule 5 (no endpoint swap) for the binary path; the new path doesn't need swapping because roles are explicit.

### 5.3 New deterministic validators/normalizers (post-LLM, alongside `stage4-type-contract-validator.py`, §5.6)

- **Head-direction normalizer** (new): apply the §3.4 hint-lexicon. Flip rows whose `asserted_relation` reverse-signals ("Killed by", "Betrayed by", "Captor of"); REJECT the ambiguous. This alone fixes the confirmed inversions (`cressen KILLS melisandre`, `arya CAPTURES sandor`, §4.4.4) deterministically and at near-zero cost.
- **Event-hub identity validator** (new): event slug = deterministic from normalized title; dedup hubs across chapters by title-normalization + participant-overlap so the Red Wedding's 3 chapters collapse to one node (§5.4 entity-resolution requirement of the brief).
- **Projector** (new, §3.3): generate the materialized primary dyads from hubs; stamp `typed_by:"event-projection"`, `confidence_tier:2`, `evidence_event`.
- **Extend type-contract validator**: add a contract rejecting any `KILLS`/`EXECUTES`/`POISONS`/`SACRIFICES` row that names an instigator OR instrument in its quote but has no corresponding hub — forces n-ary rows through the hub path rather than flattening.

### 5.4 Entity resolution for hubs

Reified events need stable IDs (brief §2.5). Reuse the existing 371 event nodes as the seed namespace (Red Wedding, Blackwater already exist, §Exec 12) — **attach to the existing node rather than mint a duplicate.** For new fine-grained events, slug from `**title**`; run the existing `duplicate-detector` → `cross-identity-detector` chain (§2.3) over event nodes too, so `event.massacre` "red-wedding" and any `red-wedding-massacre` variant collapse via `SAME_AS`.

---

## 6. Migration Plan

**Sequencing: deterministic bug-fixes → schema → pipeline → backfill → validate.** Binary types are untouched throughout.

**Phase 0 — free deterministic wins (no schema change, fully reversible):**
- Heal the **Aerys II slug split** (§4.4.2): repoint `aerys-targaryen` → `aerys-ii-targaryen` (the gated Haiku bulk already has the corrected edge). Pure win.
- Run the **head-direction normalizer** (§5.3) over the existing 3,811 rows. Flips the confirmed inversions; rejects the ambiguous. Backup first — the project already keeps `_regrounding/` backups (§4.1), reuse that mechanism.

**Phase 1 — schema:** add `event.*` leaf types (3.1) and the 6 role-edges (3.2) to `architecture.md` (and keep `edge-qualifier-vocab.md` in sync — the report flags they already drift, §3.1). No data touched yet.

**Phase 2 — pipeline:** ship the `emit_event_role` decision shape, the projector, and the new validators (§5). From here, _new_ extraction produces hubs natively.

**Phase 3 — backfill (the rewrite logic):**
1. Cluster existing death/ceremony/siege/conspiracy rows + the gated Haiku bulk's `**title**` clusters into candidate hubs (seed from the 371 existing event nodes).
2. For each cluster: create/attach hub; convert the scattered `KILLS`/`BETRAYS`/`VIOLATES_GUEST_RIGHT`/etc. rows into `AGENT_IN`/`VICTIM_IN`/`INSTIGATED` role-edges; run the projector to regenerate the canonical primary dyad.
3. Leave all binary-family rows (kinship, spatial, possession, factional, emotional) **untouched.**

**Reversible vs lossy:**
- Phase 0 and the dyad projection are **reversible** (backup retained; projection is regenerable from hubs).
- Reification is **lossy in one direction only**: collapsing scattered rows into a hub discards the _original divergent head choice_ — which is exactly the noise we want gone. The evidence_quote/evidence_ref on each role-edge is preserved, so no _evidence_ is lost.

**What breaks downstream (per the report's description of consumption):**
- `edges.jsonl` consumers that assumed person→person rows now also see person→event role-edges — but the file **already contains** person→event edges (`FIGHTS_IN`, `ATTENDS`, `OFFICIATES`, §Appendix A) and `graph/index/events/` already exists (§Exec 12), so any correct consumer already tolerates event targets. `scripts/graph-query.py` traverses generically (§1.4) — low risk, but **report gap**: the traversal code isn't shown.
- The per-node `## Edges` **markdown display lists** (§2.2, §7.5) must be regenerated — they're already documented as not auto-synced with the JSONL, so a regeneration step exists conceptually; confirm a regenerator script exists.
- Queries that previously got the _instigator_ in the `KILLS` source slot (e.g. `stannis KILLS renly`, §4.4.6, where Stannis is really the instigator and Melisandre's shadow the executor) will **change answer** — `stannis` moves to `INSTIGATED`, and the executor role becomes fillable. This is a correctness improvement but it _is_ a behavior change for any query relying on the old conflation.

**Can the binary types be left entirely untouched?** Yes — that is the point of the split. `PARENT_OF` and the kinship/spatial/possession/factional blocks never enter the migration. The whole effort is scoped to the ~82 event-like types, and within those, concentrated on the death/ceremony/siege/conspiracy families.

---

## 7. Tradeoffs & Alternatives Rejected

**Cost of the recommendation (reify-hub + materialized-dyad):**
- Structural complexity: new node leaves, 6 new edge types, a projector, hub entity-resolution. Real but bounded — it extends an existing mechanism (event nodes) rather than inventing one.
- Query ergonomics: secondary roles (instigator/instrument) move from "lost" to "2 hops." Net positive, but not free for callers that want them at 1 hop.
- Rendering: the per-node display lists get busier (event hubs with many spokes). Regeneration cost.

**Alternative A — Canonicalize everything, reify nothing (the cheaper option I rejected).** Impose one head rule on `KILLS` (e.g. always the most-agentive named participant) and never mint fine-grained hubs. **Rejected because** it is still lossy in the way the project cannot afford: the instigator, instrument, co-victims, and "sacrificed-to" axis stay unrepresentable, so the Purple Wedding stays a lie (§4.4.3) and "who orchestrated the Red Wedding" stays unanswerable. It would make the data _consistent_ but still _wrong/empty_ for the project's flagship cross-identity / who-did-what queries (§6.1). Canonicalization is the right tool for the ~30 direction-prone _binary_ types, and I keep it there — but it cannot carry the n-ary families.

**Alternative B — Pure reification, no materialized dyad.** Cleaner conceptually. **Rejected because** "who killed X" becomes a mandatory 2-hop (X→event→killer), which is precisely the 2-hop the project repeatedly engineered _around_ by adding reverse edges (§3.5, UNCLE_OF/IN_LAW_OF rationale). The materialized dyad is the concession to the project's demonstrated traversal preferences.

**Alternative C — keep deferring (the status quo: `reject` when no event node).** Rejected: it is the current behavior and it is actively losing canonical facts (§4.4.3, §6.2). The project already diagnosed this and stopped at the diagnosis.

---

## 8. Report Gaps — what would change this call

Specific facts not in the report that could move a disposition or sizing:

1. **Instigator/instrument frequency in `KILLS`/`ATTACKS` evidence_quotes.** If <~5% of rows actually name a distinct instigator or instrument, the ROI of `INSTIGATED`/`INSTRUMENT_IN` roles drops and the `ATTACKS`/`ASSAULTS` "Conditional" disposition collapses to "Keep-binary." This is the single highest-leverage gap. _Would flip:_ the conditional rows, and the depth of reification for the death family.
2. **`**title**` clustering quality across chapters in the Haiku bulk.** The recommendation leans on `**title**` as the event-id seed (§3.1, §5.1). The report shows it works _within_ a chapter (§4.6) but not whether the Red Wedding's three chapters produce title-compatible strings. If titles don't align cross-chapter, hub dedup falls back to participant-overlap heuristics (more error-prone). _Would change:_ entity-resolution effort in Phase 3.
3. **Whether `scripts/graph-query.py` and any agent consumers special-case person→person vs person→event traversal.** Report says traversal is "generic" (§1.4) but does not show the code. _Would change:_ the "what breaks" assessment in §6.
4. **Existence of a `## Edges` display-list regenerator script.** §7.5 says the lists are not auto-synced; if there is no regenerator, Phase 3 carries extra tooling cost.
5. **Count of distinct fine-grained events implied** (how many unique killings/weddings/sieges across the corpus + Haiku bulk). Sizes the node-mint and the Phase 3 effort. The report gives edge counts (102 KILLS, 145 in bulk) but not de-duplicated event counts.
6. **Whether `confidence_tier` is read anywhere today.** §3.3 proposes using tier 2 to mark machine-projected dyads. All rows are currently tier 1 (§Exec 10) and the report doesn't say any consumer branches on tier. If something does, the projector's tier stamp needs coordination.

A targeted second inventory pass answering (1) and (2) would be warranted before committing Phase 3 scope; Phases 0–2 are safe to start without it.
