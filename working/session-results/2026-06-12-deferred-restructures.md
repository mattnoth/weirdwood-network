# Session 93 — Deferred structural restructures: Wyman fake execution + Jaime street brawl

**Date:** 2026-06-12
**Model:** Opus 4.7 (orchestrator + applied all writes; no agent fan-out)
**Continue prompt:** `progress/continue-prompts/2026-06-12-deferred-structural-restructures.md`
**Started from:** Matt away, authorized "go with your gut" after answering the 4 open questions

## What this session did

Applied the two structural restructures S91 queued for ratification — both bigger than rename: each required minting a new parent event, dealing with type-field decisions, and re-attaching role-edges. Plus the vocab addition that the Wyman arc forced.

## Vocab change

**Added `event.deception` to the entity-type vocab** — `reference/architecture.md:118` + `reference/schema-legend.md:295`. Cost: 2-line documentation update. No TYPE_DIR_MAP change needed (events all route to `graph/nodes/events/`). No validator change needed (no global event-subtype validator exists). Drift-detection rule N/A (this is hand-minted, not bulk LLM).

Definition (architecture.md): *"Named discrete act-of-deceiving as event-hub — a single staged moment (or tight sequence) whose purpose is to propagate a false belief to a specific audience. Distinct from `event.conspiracy` (ongoing covert scheme over months/years) and from the `DECEIVES` edge (dyadic deceiver→deceived). Use when the deception is itself the event: who staged it, who was the audience, what false belief was planted, what the payoff was. Often nested INSIDE an `event.conspiracy` (e.g., Wyman's staged execution is a beat within the Grand Northern Conspiracy)."*

Canonical examples listed in the schema row (seeds for future promotion): Wyman's mummer's farce (this session), Cersei's false-attack claim re Jaime's street brawl, Theon's burned "Stark boys" charade, Jeyne Poole as "Arya Stark."

## Wyman arc — `wyman-manderly-stages-fake-execution-of-davos` (event.deception)

**Pre-research:** The original subagent decision packet had 2-3 sub-beats. After reading the AWOIAF wiki page `Wyman_Manderly.json`, the canonical arc has **four** distinct beats:

1. Public arrest in the Merman's Court (ADWD Davos III) — ALREADY EXISTED
2. Public execution order to Ser Marlon Manderly (ADWD Davos III) — RENAMED
3. Substitute criminal beheaded; head/hands tarred by Ser Bartimus, mounted above Seal Gate (ADWD Davos IV) — MINTED NEW
4. Frey witnesses attest at Cersei's small council; Cersei deceived; Iron Throne returns Wylis Manderly (AFFC Cersei IV) — MINTED NEW

Wyman's own line — *"the mummer's farce is almost done. My son is home."* (ADWD Davos IV) — names the whole operation. The Wylis-return (the political payoff) is captured as the **terminal beat's** consequence, not a separate sub-beat node (it's an outcome, not a deception act).

### Files touched
- **MINTED** `graph/nodes/events/wyman-manderly-stages-fake-execution-of-davos.node.md` (event.deception, parent hub)
- **MINTED** `graph/nodes/events/execution-of-davos-lookalike-at-white-harbor.node.md` (event.execution, beat 3)
- **MINTED** `graph/nodes/events/frey-witnesses-attest-davos-dead-at-small-council.node.md` (event.deception, beat 4)
- **RENAMED** `lord-wyman-orders-execution` → `wyman-publicly-orders-davos-execution` via `scripts/rename-event-node.py --apply`. 5 edge rows updated (4 source/target + 1 superseded_by). Body H1 + mint-prose rewritten with real content (Bug 3 patch). One stale `plate5_superseded_note` free-text patched separately.
- **EDITED** `wyman-publicly-arrests-davos-at-white-harbor.node.md` body — replaced stale "queued for restructure review" parenthetical with sibling-beat references to all 3 other beats and the parent hub.

### Edges minted (6 rows)
1. `SUB_BEAT_OF`  `wyman-publicly-arrests-davos-at-white-harbor` → parent  (book-curator, ADWD Davos III)
2. `SUB_BEAT_OF`  `wyman-publicly-orders-davos-execution` → parent  (book-curator, ADWD Davos III)
3. `SUB_BEAT_OF`  `execution-of-davos-lookalike-at-white-harbor` → parent  (book-curator, ADWD Davos IV; plate5_evidence_note for off-page substitute)
4. `SUB_BEAT_OF`  `frey-witnesses-attest-davos-dead-at-small-council` → parent  (book-curator, AFFC Cersei IV; plate5_evidence_note for summary-register report)
5. `DECEIVES`  `wyman-manderly` → `cersei-lannister`, qualifier="by_false_witness" (book-curator, AFFC Cersei IV) — the Frey witnesses are Wyman's unwitting false-witness instrument
6. `CONSPIRES_WITH`  `wyman-manderly` → `stannis-baratheon` (book-curator, ADWD Davos IV) — Tier-3 (no qualifier per vocab); rickon-stark return clause and via-davos-envoy mechanism captured in `rationale` field

All 6 rows tagged `candidate_kind=curator-s93-{restructure-subbeat | deception-arc}`, `typed_by=curator-s93`, `confidence_tier=1`.

The pre-existing S91 pilot `DECEIVES wyman-manderly → house-frey` (line 4760, `qualifier="staged-arrest"`) is preserved — it has a non-enum qualifier ("staged-arrest" is not in the by_lie/by_disguise/by_omission/by_false_witness/by_silence/unknown enum) but is from S91 curator-pilot batch. Flagged in look-at-twice.

## Jaime arc — `attack-on-ned-stark-in-the-streets-of-kings-landing` (event.battle)

**Pre-research:** AWOIAF has **no discrete event page** for this brawl. `Eddard_Stark.json` calls it a "melee" — eight men die — and treats it as a beat in Ned's biography. This convinced me to skip the parent/SUB_BEAT_OF layer the original subagent proposed and just **rename the survivor child directly** to the canonical hub name. One ~30-second melee should be one node, not two.

### Approach
- Picked `jaime-lannister-ambushes-ned-s-party` as the SURVIVING child (7 role edges; sibling had 5).
- Renamed → `attack-on-ned-stark-in-the-streets-of-kings-landing` (event.battle, was event.incident). 8 source/target rows + 1 superseded_by row updated by the rename script.
- Rewrote body: type-field changed, full descriptive prose added (Jaime's "I'm looking for my brother" motive, sheathe-and-order cinematic pivot, four named guard deaths, Ned's broken leg, structural causal link to Cersei's downstream lie).
- Aliases preserve both old slugs + both old names + 5 surface variants.

### Sibling merge — sheathes-stub edges
The deleted sibling `jaime-sheathes-his-sword-but-orders-ned-s-men-killed.node.md` had 5 role edges. Vs the survivor:
- **Repointed (1):** `COMMANDS_IN jaime-lannister` — unique to the sheathes side; repointed to the renamed hub.
- **Dropped as duplicates (4):** `AGENT_IN house-lannister`, `VICTIM_IN jory-cassel/heward/wyl` — all already existed on the survivor with the same source+edge_type. Marked `merged_from_sheathes_sibling: true, merged_at: 2026-06-12` on the repointed row only; the dropped 4 are gone from `edges.jsonl`.
- **Deleted** `graph/nodes/events/jaime-sheathes-his-sword-but-orders-ned-s-men-killed.node.md`.

### Edges minted (2 rows)
1. `DECEIVES`  `jaime-lannister` → `eddard-stark`, qualifier="by_omission" (book-curator, AGOT Eddard IX) — captures the sheathe-and-order cinematic pivot. The qualifier is defensible: Jaime omits his real intent via the sheathe gesture; Ned reads the sheathe as de-escalation for the half-second before "kill his men" lands. (Alternative reading: deception target is Robert/the court, not Ned — Jaime preserving plausible deniability via not striking with his own blade. I went with Ned as target per the original subagent rec, but the wider-court reading is real.)
2. `TRIGGERS`  parent → `cersei-claims-ned-s-men-attacked-first` (book-curator, AGOT Eddard X) — narrative causal link between the truth-event and Cersei's downstream cover-story lie. `plate5_evidence_note` since no single quote spans both chapters.

## Final counts

| Metric | Before | After | Δ |
|---|---|---|---|
| `graph/nodes/events/` files | 583 | 585 | +2 (Wyman: +3 mints; Jaime: −1 sibling merge) |
| `graph/edges/edges.jsonl` rows | 4,760 | 4,764 | +4 (+6 Wyman, +2 Jaime, −4 deduped) |
| Edge types active | 112 | 112 | 0 |
| Orphan endpoints | 115 | 115 | 0 (no new orphans introduced) |
| `event-alias-lookup.json` phrases | 922 | 954 | +32 |
| Ambiguous alias collisions | 1 | 1 | 0 (pre-existing `conquest-of-dorne`) |

## Verification

- `python3 scripts/graph-query.py --health` → SUMMARY: 8,518 nodes, 4,764 edges, 115 orphan endpoints, 112 edge types
- `python3 scripts/graph-query.py --event-participants wyman-manderly-stages-fake-execution-of-davos` → 4 beats, 6 role edges via traversal, 5 distinct participants (marlon-manderly, house-manderly, wyman-manderly + `lord-wyman-manderly` collision, davos-seaworth). **TRAVERSAL WORKS END-TO-END.**
- `python3 scripts/graph-query.py --neighbors attack-on-ned-stark-in-the-streets-of-kings-landing` → 2 outgoing (LOCATED_AT king-s-landing + TRIGGERS Cersei lie) + 8 incoming (3 AGENT_IN + 1 COMMANDS_IN + 4 VICTIM_IN). All edges resolved.
- **Alias-chain probes: 16/16 HIT** (after stripping leading "the " — the resolver convention). Probes covered every minted alias including the new sub-beat names + the parent + the renamed Jaime hub + every Jaime-sibling surface form.
- `grep -E "(lord-wyman-orders-execution|jaime-sheathes-...|jaime-lannister-ambushes-ned-s-party)" graph/edges/edges.jsonl | grep -v aliases | wc -l` → **0 stale source/target/superseded_by references** in edges.jsonl.
- 3 stale index files removed: `graph/index/events/{jaime-lannister-ambushes-ned-s-party,jaime-sheathes-his-sword-but-orders-ned-s-men-killed,lord-wyman-orders-execution}.index.json`.

## Look-at-twice items for Matt

1. **`lord-wyman-manderly` collision** — the Wyman parent's beat-union traversal returns BOTH `wyman-manderly` AND `lord-wyman-manderly` for the COMMANDS_IN role. The `lord-wyman-manderly` form is a pre-existing alternate-slug collision in the graph (not introduced by S93; visible on the arrest beat's pre-existing role edge from S87 Plate-3 mints). The renamed `wyman-publicly-orders-davos-execution` correctly uses `wyman-manderly`. Candidate for slug-merge cleanup in a future pass; not blocking.
2. **S91 pilot `DECEIVES wyman→house-frey` qualifier** — uses `"staged-arrest"` which is NOT in the DECEIVES enum (`by_lie | by_disguise | by_omission | by_false_witness | by_silence | unknown`). My new Wyman→Cersei DECEIVES uses the enum-conforming `by_false_witness`. The S91 edge predates this audit and is curator-tagged; leave it or normalize? Two options: (a) leave + audit-flag in todos; (b) retype to `by_omission` (Wyman omits his real intent from House Frey by performing public arrest as theatre).
3. **`SUB_BEAT_OF` empty-evidence_quote** — beats 3 and 4 of the Wyman arc carry `plate5_evidence_note` instead of a verbatim quote (substitute beheading is reported off-page; Frey small-council is summary-register in AFFC Cersei IV). Falls in the same Contract-6-exemption class as the 32 empty-quote SUB_BEAT_OF rows from Plate 5. Carry under that existing followup, not S93-specific.
4. **`event.deception` type — first canonical instance pair** — Wyman's parent and Frey small-council beat are the two seed `event.deception` nodes. The type is documented with 4 example seeds in `architecture.md:118` (Wyman + Cersei's false-attack claim + Theon's burned boys + Jeyne-as-Arya). If Matt wants a vocab dip, future passes can promote the other 3 examples — but only as a deliberate decision, not bulk auto-promotion.
5. **Jaime `DECEIVES` target choice** — I picked `eddard-stark` as the deception target with `qualifier="by_omission"`. The alternative read is `robert-baratheon` (Jaime preserves plausible deniability for what he tells Robert later). The Cersei-claim TRIGGERS edge captures Robert as the downstream-deception audience structurally; the Jaime DECEIVES is the in-the-moment gesture. If Matt prefers, this could be retyped to target Robert with `by_omission`, but the in-moment read is what the original subagent packet specified.

## What's next

- HANDOFFs 1 / 2 / 3 from session start (infobox-merge ship → graph cleanup → Mode 3 dip) — all still gated on Matt's dry-run report + curation marks; nothing in S93 changes those gates.
- This restructure session was the only parallel-safe unblocked track; it is now done.
- Endsession will be triggered by Matt only — per standing rule (`feedback_endsession_requires_permission`), I do NOT auto-/endsession.

## Hard-rule audit (continue-prompt rules)

| Rule | Held? | Note |
|---|---|---|
| DO NOT re-run any rename without `--dry-run` first | ✓ | Both renames dry-run'd then applied |
| DO NOT auto-/endsession | ✓ | Stopping at writeup + worklog entry; awaiting Matt |
| DO ask Matt about open questions before mints | ✓ | Asked 4 questions; Matt dismissed (chat); answered via additional research → permission granted |
| DO preserve old slugs as last entry in aliases | ✓ | All renames include old-slug as the final alias entry |
| DO add Bug 3 plate5_superseded_note patch after each rename | ✓ | 2 stale notes patched (1 Wyman, 1 Jaime) |
| DO use INLINE-form aliases (Bug 1) | ✓ | All `aliases:` are inline-list form |
