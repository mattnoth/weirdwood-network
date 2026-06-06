I wasn't able to write the file (permission wasn't granted). Per the brief's "write it, or print it in full," here is the complete decision document. If you'd prefer it saved to disk, approve the write or tell me a path you've allowed.

---

# Edge & Event-Modeling — Diagnosis & Recommendation

_Analysis phase. Input: the asoiaf-chat (Weirwood Network) edge-modeling inventory, commit `f04dbc8a2`. Stands on the report alone; repo not consulted._

## Recommendation in one paragraph

**Reify the set-piece, multi-party events the graph already half-models as nodes** (the killing/execution cluster, sieges, sacrifices, the guest-right/Red-Wedding family, the marriage *ceremony*, captivity *events*, conspiracies, the tourney crowning) by anchoring each participant to the existing `event.*` node through **role-typed edges** (agent, victim, instrument, commander, location, outcome). **Canonicalize** the genuinely dyadic *acts* that don't warrant a node (generic `ATTACKS`, `CAPTURES`, `DEFEATS`, `DUELS`, `TRAVELS_TO`, `LOCATED_AT`, the reverse-direction structural pairs) with one machine-applicable head rule. **Leave the ~76 true binaries alone** (`PARENT_OF`, the kin shortcuts, the emotion/perception verbs, spatial endpoints, narrative/prophecy/evidentiary edges). The single biggest root cause of the "hallucination-look" is **not the schema and not model accuracy** — it is **grammatical-subject leakage at the Pass-1 extraction layer** (`| Character A | Relationship | Character B |` with no head rule, `mechanical-extractor.md:176-178`), compounded by the fact that **the n-ary container already exists but is empty**, so the classifier "has nothing correct to point at and improvises" (S58 audit, `...batch-0020-opus-audit.md:244-253`). **This project doesn't need a new paradigm — it needs to finish the one it started**: 371 event nodes exist (`graph/index/events/_summary.json:1-12`), just structurally empty (Red Wedding has 3 outbound edges, §6.10).

## 1. Diagnosis

**1.1 Underdetermination, not invention.** Two structurally different things share the `source → target` shape: dyadic relations with one correct head (`PARENT_OF`) and n-ary events with no natural head (`KILLS`, the Red Wedding). Flattening forces each row to nominate a head; with no canonical form imposed, every row picks a different projection. The Red Wedding proves it: `roose-bolton BETRAYS robb-stark` (python-map), `walder-frey BETRAYS robb-stark` (sonnet, *same chapter*), `lothar-frey CONSPIRES_WITH roose-bolton` (different chapter) — **no link between them** (§4.4.1). `VIOLATES_GUEST_RIGHT` for that one event: **7 subjects × 8 targets across 5 chapters**. Catelyn's killer slot = `raymund-frey` (knife-wielder); Robb's = `roose-bolton` (political agent) — same event, different role nominated as subject.

**1.2 Root cause, two compounding origins.** **(a) Grammatical-subject leakage at extraction — the headline.** Pass-1's table has no A-vs-B rule (§5.2); python-map "takes the grammatical subject rather than the semantic agent" and column position locks direction (§4.4.4). This is the brief's §1.8 trap, *confirmed* by self-witnessing inversions: `cressen KILLS melisandre` (asserted_relation: "Killed by"), `tyrion BETRAYS shae` ("Betrayed by"), `arya CAPTURES sandor`. 232 unordered pairs carry the same type in both directions (§4.5). **(b) The missing reification target** — the S58 audit's own words: the classifier targets the person/venue "because the event node frequently does not exist… so there is nothing correct to point at" (§6.2). The container exists by type, is empty by instance. **No canonical head rule exists anywhere** (§ES-4): Stage-4 Rule 5 forbids endpoint swaps and the output schema has no swap field, so a bad head is **structurally permanent** (§5.3) — the pipeline can reject but never correct.

**1.3 Where I disagree with the report.** (1) **`SPOUSE_OF`/`BETROTHED_TO`/`SWORN_TO` are binary STATES, not events** — the report conflates the standing marital state (dyadic, one shape) with the wedding *ceremony* (n-ary). Keep the state edge; reify the ceremony separately. (2) **`LOCATED_AT` is binary** — the report flags it event-like for its timestamp, but its own rule excludes temporal metadata. (3) **`HEALS`/`RESCUES`/`MANIPULATES`/`BETRAYS` are over-reified** — dyadic acts with a weak optional third role; canonicalize, don't mint a node each. (4) **`KILLS`/`EXECUTES`/`POISONS`/`ASSAULTS` are hybrid** — a battlefield death is dyadic; the Red Wedding murders are an event. Reify at a named occasion, else canonicalize — exactly the trigger the prose-classifier already uses for `ATTENDS`/`FIGHTS_IN` (§5.5).

## 2. Disposition Table

`disposition` ∈ **Reify** · **Reify@occasion/else-Canon** · **Canonicalize** · **Keep binary**. Rationale ties to §1.7 (P1 = >2 participants, P2 = own properties, P3 = negatable-as-unit).

| edge_type(s) | classification | disposition | rationale | conf | gap-dep? |
|---|---|---|---|---|---|
| `KILLS`,`KILLED_BY`,`EXECUTES`,`EXECUTED_WITH`,`KILLED_WITH` | event | **Reify@occasion/else-Canon** | P1+P2+P3; schema splits one killing across 5 types (§ES-2) | High | G4 |
| `BESIEGES` | event | **Reify** | P1+P2+P3; besieger/defender/war/duration/allies | High | no |
| `SACRIFICES` | event | **Reify** | P1+P2; recipient/purpose axis "wholly missing" (§3.4-6) | High | no |
| `VIOLATES_GUEST_RIGHT` | event | **Reify** | P1+P2+P3; 7×8 spray, no event link (§4.4.1) | High | no |
| `CONSPIRES_WITH` | event | **Reify** | P1; only type whose desc says "two or more parties" | High | no |
| `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` | event | **Reify** | P1+P2; "multi-party witness state" at a tourney | High | no |
| `MARRIES_OFF`,`PROPOSED_AS_BRIDE` | event | **Reify** (ceremony) | P1; descriptions admit the silent third (§3.6-6) | High | no |
| `CAPTURES`,`IMPRISONS`,`RANSOMS`,`PRISONER_EXCHANGE_FOR` | event | **Reify@occasion/else-Canon** | P1; captivity split across 5 types | Med | G4 |
| `POISONS`,`ASSAULTS`,`TORTURES` | event | **Reify@occasion/else-Canon** | P1+P2; Purple Wedding needs Olenna+LF+strangler | Med | G1 |
| `ATTACKS`,`DEFEATS`,`DUELS` | event | **Canonicalize** | P2 only; `on_command` → causal edge not node | Med | no |
| `REVEALS_TO`,`DECEIVES`,`DECEIVED_BY` | event | **Canonicalize** | P2; content via qualifier not node | Med | no |
| `SPIES_ON`,`INFORMS` | event | **Canonicalize** (triangle) | P1; keep both edges, fix direction | Med | no |
| `MANIPULATES`,`BETRAYS` | event | **Canonicalize** | weak P1; head=actor, beneficiary→causal edge | Med | no |
| `HEALS`,`RESCUES` | report-event → **binary act** | **Canonicalize** | fails P1/P3 — over-reified by report | Med | no |
| `FIGHTS_IN`,`COMMANDS_IN`,`PARTICIPATES_IN`,`ATTENDS`,`OFFICIATES`,`WIELDED_IN` | event | **Keep (already role edges)** | already point participant→event; reuse these | High | no |
| `RULES`,`HOLDS_TITLE`,`HELD_BY`,`SUCCEEDS`,`CLAIMS`,`APPOINTS`,`DEPOSES`,`BANISHES`,`VOWS_TO`,`BREAKS_VOW` | mixed | **Canonicalize** | dyadic w/ missing role recoverable via siblings | Med | no |
| `SPOUSE_OF`,`BETROTHED_TO`,`SWORN_TO`,`LOVER_OF`,`WARD_OF`,`MEMBER_OF`,`OVERLORD_OF`,`ALLIES_WITH`,`OPPOSES`,`NEGOTIATES_WITH`,`CONTRACTED_WITH` | **binary STATE** (disagree on first 3) | **Keep binary** | standing dyadic state; qualifier ≠ third party | High | no |
| `LOCATED_AT`,`TRAVELS_TO`,`TRAVELS_WITH`,`DISGUISED_AS`,`IMPERSONATES`,`FORGED_BY`,`LOOTED_BY`,`GIFTED_TO`,`INHERITED_BY`,`REFORGED_INTO`,`PURCHASED_FROM`,`BUILT`,`RESURRECTS`,`WARGS_INTO`,`CURSES`,`DREAMS_OF` | mixed → binary/thin | **Canonicalize** | metadata/sibling-recoverable; direction lock | Med | no |
| `PARENT_OF`,`SIBLING_OF`,`ANCESTOR_OF`,`CADET_BRANCH_OF`,`UNCLE_OF`,`NEPHEW_OF`,`COUSIN_OF`,`MILK_BROTHER_OF`,`NURSED_BY`,`WET_NURSE_OF`,`STEP_PARENT_OF`,`STEP_CHILD_OF`,`IN_LAW_OF`,`HEIR_TO` | binary | **Keep binary** | fails P1/P2/P3; data clean, no bidi pairs (§4.4.9) | High | no |
| `LOVES`,`HATES`,`FEARS`,`TRUSTS`,`DISTRUSTS`,`RESPECTS`,`MOURNS`,`RESENTS`,`PROTECTS`,`PERCEIVED_AS`,`REPUTED_AS`,`COMPANION_OF`,`SEEKS`,`IGNORANT_OF`,`HOARDS`,`INVESTIGATES`,`TEACHES`,`TUTORS`,`AFFLICTED_BY`,`DIED_OF` | binary | **Keep binary (canon direction)** | dyadic; only failure is inversion (§4.4.4) | High | no |
| `BORN_AT`,`DIED_AT`,`BURIED_AT`,`IMPRISONED_AT`,`SEAT_OF`,`REGION_OF`,`CONTEMPORARY_WITH`,`WIELDS`,`OWNS`,`ANCESTRAL_WEAPON_OF`,`MADE_OF`,`CAPTAIN_OF`,`CREW_OF`,`PRISONER_OF` | binary | **Keep binary** | endpoint/state; third role on sibling by design | High | no |
| `CULTURE_OF`,`WORSHIPS`,`SACRED_TO`,`CLERGY_OF`,`PRACTICES`,`BONDED_TO`,`NAMED_AFTER`,`ALIAS_OF`,`SAME_AS`,`DEPICTED_IN`,`WRITTEN_BY` | binary | **Keep binary** | clean dyads / identity-resolution | High | no |
| `FORESHADOWS`,`PARALLELS`,`SUBVERTS`,`ECHOES`,`CONTRASTS`,`FULFILLS`,`APPEARS_TO_FULFILL`,`SUBVERTS_PROPHECY`,`PROPHESIED_BY`,`SUBJECT_OF_PROPHECY`,`SUPPORTS`,`CONTRADICTS`,`CITED_BY`,`CAUSES`,`PREVENTS`,`ENABLES`,`MOTIVATES`,`TRIGGERS`,`PART_OF`,`GRANTS_SAFE_CONDUCT`,`KNIGHTED_BY`,`BESTOWS_KNIGHTHOOD_ON`,`GUARDS` | binary | **Keep binary** | analytical/causal/structural dyads | High | no |
| `GUEST_OF` | event | **Canonicalize** (event-link optional) | P1 but qualifier-rich, 404 rows; reify only the *violation* | Med | no |
| `KNOWS` (deprecated) | n/a | **Leave deprecated** | removed S63, filtered on read | High | no |

## 3. Target Schema

Store = property-graph-in-files (Markdown+YAML nodes, JSONL edges). Reify = an `event.*` hub node with **role-typed edges**, extending the convention the graph already uses (`FIGHTS_IN person→battle`, `ATTENDS person→event`, `WIELDED_IN artifact→event`).

**3.1 Role edges (additions), convention participant → event:**
```
AGENT_IN      person  → event   # perpetrator/actor
VICTIM_IN     person  → event   # patient/target
COMMANDER_OF  person  → event   # instigator/orderer  [or reuse COMMANDS_IN]
INSTRUMENT_IN artifact→ event   # or reuse WIELDED_IN
```
Reuse `LOCATED_AT` (event→location), `OFFICIATES`, `ATTENDS`, `FIGHTS_IN`. Non-participant axes go on the node frontmatter: `outcome`, `method`/`qualifier` (reuse the Tier-2 `KILLS` enum), `time`, `recipient`/`purpose`. Lossless — every role survives. It is the associative-entity/junction-table move the project already endorses ("collapse, not split", §2.4).

**3.2 Worked example — Red Wedding** (node already exists, §6.10):
```jsonl
{"edge_type":"COMMANDER_OF","source_slug":"tywin-lannister","target_slug":"red-wedding","evidence_quote":"Jaime Lannister sends his regards"}
{"edge_type":"COMMANDER_OF","source_slug":"walder-frey","target_slug":"red-wedding"}
{"edge_type":"COMMANDER_OF","source_slug":"roose-bolton","target_slug":"red-wedding"}
{"edge_type":"AGENT_IN","source_slug":"roose-bolton","target_slug":"red-wedding"}
{"edge_type":"AGENT_IN","source_slug":"raymund-frey","target_slug":"red-wedding"}
{"edge_type":"VICTIM_IN","source_slug":"robb-stark","target_slug":"red-wedding"}
{"edge_type":"VICTIM_IN","source_slug":"catelyn-stark","target_slug":"red-wedding"}
{"edge_type":"LOCATED_AT","source_slug":"red-wedding","target_slug":"the-twins"}
```
Node frontmatter: `outcome`, `time: "ASOS Catelyn VII"`, `guest_right_violated: true`. "Who was behind it" = one hop into `COMMANDER_OF`; "who died" = `VICTIM_IN`. The 7×8 `VIOLATES_GUEST_RIGHT` spray collapses to one property + roles. **Heals §4.4.1 entirely.**

**3.3 Canonical head rule (Canonicalize types):**
> **HEAD = the most direct semantic AGENT, regardless of grammatical voice or POV.** Performer = `source`, acted-upon = `target`. Passive voice → by-phrase agent is `source` (already stated for KILLS, `stage4:319-324`). Instigator vs executor → executor is head, orderer goes on `COMMANDER_OF`/`CAUSES` (GATE 2 already forbids A→C collapse). **Tie-breakers:** named over collective; physical executor over abstract cause; unresolvable agent → **REJECT**. **Forbidden:** anchoring on the grammatical subject or the POV character (the §1.8 trap, origin of the 232 bidi pairs).

## 4. Causation Modeling Decision

**One event node carrying both roles** (`COMMANDER_OF` + `AGENT_IN`), **not two nodes joined by a causal edge** — exception below. Justification: "who was *behind* Robb's death" is the project's canonical query (§6.1); with roles it's one hop, with two nodes it's a two-hop join that reintroduces the fragmentation we're removing. Infrastructure is single-event-node; minting an "ordering" event per `on_command`/`by_proxy` row (§A.2) has no independent attestation. GATE 2 already refuses the merged A→C edge — roles just give the orderer a home. **Exception:** when the ordering is itself a separately-attested, distinct occasion (a documented council/decree), model it as its own node linked by `CAUSES`/`TRIGGERS`. Minority case.

## 5. Pipeline Remediation

**5.1 Pass-1 extractor (the root cause).** (a) Add an `## Events Observed` table with role columns: `| Event Title | Type | Agent(s) | Patient/Target(s) | Instrument | Location | Instigator | Outcome | Evidence |`, multi-participant rows keyed by a shared **Event Title** — formalizing the Haiku bulk's `**title**` convention (§4.6, "the closest thing to an event-id in any layer today"). Kills the unparseable `Robb Stark and his followers` cells. (b) Add to `## Relationships Observed`: *"Column A is always the SEMANTIC AGENT, never the grammatical subject and never the POV character; for passive sentences put the by-phrase agent in A; record orderers in the Events table's Instigator column, not in A."*

**5.2 python-map + Stage-4.** python-map: stop deriving direction from column position for event-like hints; route to event-assembly. Stage-4 already has GATE 2, V5-R1, Rule 12, the passive-voice rule — add one rule mirroring the prose-classifier (§5.5): *"if the act occurred at a named occasion, emit role edges to the event node; if missing, escalate to event-creation — never redirect onto a person or venue."* Note: the LLM can't swap endpoints (Rule 5), so the head must be correct **before** Stage-4 — the §5.1 fix is load-bearing.

**5.3 Validation.** Reject person→person `KILLS`/`EXECUTES`/`VIOLATES_GUEST_RIGHT`/`SACRIFICES` when an event node exists for that chapter. Repair-flag grammatical-subject leakage: when `asserted_relation` has a passive marker ("Killed by") and direction matches the grammatical subject, flag for inversion. Enforce `AGENT_IN`/`VICTIM_IN` → `event.*`.

**5.4 Event entity-resolution.** Deterministic event slug from Event Title + occasion; **dedup across chapters** (Red Wedding spans 3 chapters → one node, or the fragmentation returns). Fix the `aerys-targaryen` → `aerys-ii-targaryen` slug split first (§4.4.2) — reifying onto a phantom slug relocates the bug. The gated Haiku bulk already has the corrected slug.

## 6. Migration Plan

1. Fix slug splits; confirm the 371 event nodes have stable slugs (category drift exists, §7.2). 2. Backfill role edges from existing scattered binaries where `evidence_chapter` maps to an event; the Haiku bulk's `**title**` grouping is a ready-made clustering signal — consider promoting via the audit's path C (~$2-5, §7.6). 3. Canonicalize the dyadic remainder; invert confirmed bidi bugs.

**Reversible vs lossy:** creating event nodes + role edges is additive/reversible (do first). Collapsing old binaries is lossy — don't delete, mark `superseded_by` (reuse the `pass_origin` supersession concept), keep `_regrounding` backups. **Breaks:** `graph-query.py` traversals assuming person→person `KILLS` become person→event→person (2 hops, severity = G3); the per-node `## Edges` bullet display (not auto-synced to JSONL) needs both representations migrated; visualization gains hub nodes. **Binary types untouched** except a one-time inversion sweep. **Sequence:** schema → pipeline → backfill (additive) → validate → collapse.

## 7. Tradeoffs & Alternatives Rejected

**Cost:** 2-hop traversal, hub-node visualization, new role vocabulary, migration of the killing/marriage/captivity clusters, event dedup. This *reverses* the project's stated instinct ("collapse not split" §2.4, metadata-not-arity §6.4, reverse-edges §3.5) — deliberately.

**Rejected — pure canonicalization (no event nodes).** Cheaper, kills the symptom, but stays lossy (instigator/instrument/co-victims discarded) and **cannot answer the project's own headline query** "everyone involved in the Red Wedding" (§6.1). Fixes the look, fails the mission. Correct for dyadic acts, wrong for set-pieces → hence the hybrid.

**Rejected — reify everything event-like.** Operationally enormous and wrong for dyadic acts (`HEALS`) and misclassified states (`SPOUSE_OF`). Cost with no query payoff.

**Why the cut works:** reify where P1 genuinely holds AND a named occasion exists; canonicalize dyadic acts; keep states. This is the project's own latent design (the `ATTENDS`/`FIGHTS_IN` trigger, §5.5), made explicit.

## 8. Report Gaps — what would change this call

- **G1 — Purple Wedding absent** (§4.4.3): can't validate the `POISONS` reify-shape; if the corpus truly lacks Olenna/LF, `POISONS` drops to Canonicalize.
- **G2 — Appendix B JSONL blocks are empty** (B.2–B.6): claims rest on the body's prose, not raw rows; confirm field shapes before writing the backfill.
- **G3 — `graph-query.py` multi-hop behavior undocumented:** biggest unknown for §6.3; if it can't transparently hop person→event→person, may need a denormalized shadow edge. **Worth a pass.**
- **G4 — No named-occasion-vs-generic count:** sets the Reify-vs-Canon split size for `KILLS`/`CAPTURES`/`POISONS`. **Worth a pass** (group the 102 `KILLS` rows by event-node membership).
- **G5 — Event-node coverage/quality unknown** beyond Red Wedding; if occasions lack nodes, backfill's first cost is node creation (exactly the S58 finding).
- **G6 — `confidence_tier` uniformly 1:** can't prioritize migration by confidence.
- **G7 — Haiku `**title**` consistency unverified:** if stable, a near-free event key; if noisy, needs its own resolver.

---

**Summary:** The fix is to *complete the event-node architecture the project already began* — reify the multi-party set-pieces via role edges, canonicalize the dyadic acts with one agent-based head rule, and leave the true binaries untouched. The headline root cause is grammatical-subject leakage at the Pass-1 extractor plus empty event nodes — both pure underdetermination, not model error — so the highest-leverage single change is the `## Events Observed` table + head rule in `mechanical-extractor.md`, since Stage-4 structurally can't correct a head once set.
