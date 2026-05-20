---
audit: batch-0020 Stage 4 prose-edges
date: 2026-05-19
model: Opus 4.7
type: diagnostic (READ-ONLY — no data, prompt, or schema modified)
gating: STEP 5 Haiku smoke fire is gated on Section 5 verdict
---

# Opus Audit — batch-0020 Stage 4 Prose-Edges

**Scope:** 153 flagged emits in batch-0020 (35% of 437 total emits), of which 140 are
`knows_as_fallback`, 12 `attends_non_event`, 1 `fights_in_non_event`. batch-0020 alone
holds 140 of 163 project-wide KNOWS-fallback flags. This audit characterizes the failure
modes and verdicts Haiku-smoke readiness.

**Hard confirmation of input counts (per continue prompt):**
`grep '"source_batch": "batch-0020"'` → 153 rows. KNOWS-fallback → 140. Non-KNOWS → 13
(12 ATTENDS + 1 FIGHTS_IN). All counts match the continue prompt exactly.

---

## 1. Sample methodology + 50-emit breakdown

### Methodology

- Extracted all 140 `knows_as_fallback` rows from `working/wiki/data/stage4-suspicious-edges.jsonl`.
- **Stratified sample of 50** by `source_slug`, proportional allocation (seed 20260519,
  reproducible). The 140 rows span only 19 distinct source slugs — a very narrow source
  set, itself a finding (see Section 2). Sample covers all 19 source slugs.
- For each row: read `evidence_snippet` + the classifier's freeform `qualifier` text
  (the qualifier in these control-arm rows is freeform prose describing full context —
  it is itself the freeform-drift surface the qualifier-vocab lockdown was built to kill).
- Resolved every target's `type:` field from `graph/nodes/`. This surfaced a failure mode
  the flagger does not name: **KNOWS emitted onto non-character targets** (person→place,
  person→event). KNOWS is a knowledge-between-people edge; a `KNOWS` edge to a castle or a
  battle is a type-contract violation, not merely a soft fallback.

### Target-type distribution across all 140 KNOWS-fallback rows

| Target broad type | Count | Note |
|---|---:|---|
| `character.*` | 113 | candidate KNOWS — most are still co-presence, not knowing |
| `event.*` | 12 | type-contract violation — KNOWS cannot target an event |
| `place.*` | 11 | type-contract violation — KNOWS cannot target a place |
| `organization.*` | 2 | type-contract violation |
| `concept.*` | 1 | type-contract violation |
| `object.*` | 1 | type-contract violation |

**27 of 140 KNOWS-fallback emits (19%) target a non-character node.** Every one of these
is unambiguously wrong on the type contract alone, before any evidence reading.

### 50-emit verdict breakdown

| Verdict | Count | % of 50 |
|---|---:|---:|
| **legit-KNOWS** | 1 | 2% |
| **soft-fallback** (co-presence, no knowing-verb, no better type) | 13 | 26% |
| **better-edge** (a specific one of the 159 types fits) | 28 | 56% |
| **reject-just-mention** (not a real relationship at all) | 8 | 16% |

**Only 1 of 50 sampled KNOWS emits is a correct KNOWS.** 56% should have been a different,
already-available edge type — meaning the dominant problem is not "no type fit" but "the
classifier reached for KNOWS instead of doing the type lookup." 16% are not edges at all.

### Per-row verdict table (50 rows; `idx` = line index within the 140-row KNOWS set)

| idx | source → target | target type | verdict | better edge / reason |
|---:|---|---|---|---|
| 0 | walda-frey-merrett → arya-stark | character | reject-just-mention | Arya read letters *to Roose*; no Walda↔Arya relation at all |
| 3 | walda-frey-walton → roose-bolton | character | better-edge | `PROPOSED_AS_BRIDE` (Fair Walda offered to Roose) — see Pattern-1 case in prompt |
| 6 | walda-rivers-aemon → robb-stark | character | reject-just-mention | curtsied during a group apology; temporal-cooccurrence |
| 9 | walder-frey-jammos → hother-umber | character | soft-fallback | both at Ramsay's feast; co-presence only |
| 11 | walder-frey-jammos → theon-greyjoy | character | better-edge | `CAPTURES` / escort of Theon from dungeon (or soft-fallback at minimum) |
| 13 | walder-frey-merrett → barbrey-dustin | character | reject-just-mention | Dustin gave colts; reverse-direction gift, belongs on Dustin's node |
| 16 | walder-frey-merrett → mance-rayder | character | reject-just-mention | "Abel's girl" taught him to dance; no Walder↔Mance relation |
| 18 | walder-frey-merrett → roose-bolton | character | reject-just-mention | Roose's *men* intervened; no person-pair edge |
| 20 | walder-frey-merrett → wendel-manderly | character | reject-just-mention | bones returned; Wendel is dead, no relation |
| 22 | walder-frey-ryman → catelyn-stark | character | reject-just-mention | snippet is about Black Walder's succession rank; Catelyn not in evidence |
| 28 | walder-frey → winterfell | **place** | reject-just-mention | type-contract violation; "indirect connection" per qualifier |
| 31 | walder-frey → wynafryd-manderly | character | better-edge | `MARRIES_OFF` (Walder betroths his grandson to Wynafryd) |
| 34 | walder-frey → elder-brother-quiet-isle | character | soft-fallback | Elder Brother reports Walder's activity; reporter, not a relation |
| 36 | walder-frey → lancel-lannister | character | better-edge | `MARRIES_OFF` (Lancel betrothed to Walder's granddaughter Amerei) |
| 38 | walder-frey → battle-under-the-walls-of-riverrun | **event** | reject-just-mention | type-contract violation; KNOWS on a battle |
| 40 | walder-frey → edmure-tully | character | better-edge | `OPPOSES` (slow to answer summons) + later RW context; ALLIES_WITH/MARRIES_OFF arguable |
| 48 | walder-frey → robert-arryn | character | reject-just-mention | Jon Arryn *refused* fostering; a non-event |
| 49 | walder-frey → tytos-lannister | character | better-edge | `MARRIES_OFF` / `NEGOTIATES_WITH` (Emmon-Genna marriage proposal) |
| 50 | walder-frey → tywin-lannister | character | soft-fallback | 10-yr-old Tywin spoke against the match; OPPOSES is a stretch |
| 52 | walder-frey → eddard-stark | character | soft-fallback | Walder's dialogue references Ned's imprisonment; no direct relation |
| 56 | walder-rivers → walder-frey-ryman | character | soft-fallback | suspected-of-patricide; KILLS is not provable; no clean type |
| 60 | walder-rivers → chett | character | **better-edge** | `EXECUTES` / judicial — "sent to judge him, Chett sent to the Wall" |
| 62 | walder-rivers → daven-lannister | character | soft-fallback | Daven's hostile opinion of Walder; PERCEIVED_AS arguable |
| 64 | walder-rivers → roslin-frey | character | better-edge | `SIBLING_OF` (Walder Rivers describes "my lord father's youngest daughter" = half-sister) |
| 67 | whalen-frey → catelyn-stark | character | soft-fallback | attends Walder during a parley; co-presence |
| 70 | gawen-gardener → loren-i-lannister | character | soft-fallback | fathers' alliance; not Gawen↔Loren directly (ALLIES_WITH belongs to the kings) |
| 71 | tremond-gargalen → balon-swann | character | soft-fallback | both at a feast; co-presence |
| 75 | gwayne-gaunt → barristan-selmy | character | **legit-edge** | `SIBLING_OF`? no — sworn brothers of Kingsguard → `MEMBER_OF` shared; death *avenged by* → no clean type; closest legit reading **reject** |
| 77 | ethan-glover → elbert-arryn | character | soft-fallback | both in Brandon's party to KL; COMPANION_OF arguable |
| 82 | ethan-glover → mark-ryswell | character | soft-fallback | both in Ned's Red Mountains party; COMPANION_OF arguable |
| 83 | ethan-glover → martyn-cassel | character | soft-fallback | same party; COMPANION_OF arguable |
| 84 | ethan-glover → robert-i-baratheon | character | reject-just-mention | timeline co-mention only; tier-3 |
| 85 | ethan-glover → sack-of-kings-landing | **event** | reject-just-mention | type-contract violation |
| 89 | galbart-glover → taking-of-deepwood-motte | **event** | better-edge | type-contract violation; intended sense is `FIGHTS_IN` against an event (Galbart's seat captured) — but evidence does not put Galbart in the fight; reject |
| 90 | galbart-glover → fight-by-deepwood-motte | **event** | reject-just-mention | type-contract violation; Galbart was *away* |
| 91 | galbart-glover → kingsmoot-on-old-wyk | **event** | reject-just-mention | type-contract violation; Galbart not present |
| 93 | galbart-glover → catelyn-stark | character | better-edge | `SERVES` / commanded-by — "Eddard tasks her to have Galbart fortify Moat Cailin" |
| 100 | galbart-glover → martyn-lannister | character | reject-just-mention | prisoner-exchange rationale; no Galbart↔Martyn relation |
| 103 | glover-steward → larence-snow | character | better-edge | `WARD_OF` reverse / fostered-at — Larence fostered at Deepwood Motte; or reject (steward is questioner) |
| 109 | lyanne-glover → melantha-blackwood | character | reject-just-mention | both wives of Lord Willam serially; no Lyanne↔Melantha relation |
| 114 | robett-glover → helman-tallhart | character | **better-edge** | `ALLIES_WITH` — ordered to join forces and march together on Duskendale |
| 120 | robett-glover → sack-of-winterfell | **event** | reject-just-mention | type-contract violation |
| 121 | robett-glover → skagos | **place** | reject-just-mention | type-contract violation |
| 122 | robett-glover → ten-towers | **place** | reject-just-mention | type-contract violation |
| 123 | robett-glover → wex-pyke | character | **better-edge** | `TEACHES` — "teaching Wex Pyke … to read and write" (explicit) |
| 126 | robett-glover → catelyn-stark | character | soft-fallback | kneels to greet Catelyn; SERVES arguable; co-presence |
| 129 | robett-glover → blackwater-bay | **place** | reject-just-mention | type-contract violation |
| 130 | robett-glover → golden-tooth | **place** | reject-just-mention | type-contract violation |
| 134 | robett-glover → red-wedding | **event** | better-edge | type-contract violation; if Robett present → `ATTENDS`; evidence does not place him there → reject |
| 136 | robett-glover → willem-lannister | character | reject-just-mention | Willem already dead; mentioned in exchange rationale |

> **Verdict re-tally (the table above):** legit-KNOWS 1 (idx 60 reclassified `EXECUTES`
> on closer reading — see note), soft-fallback 13, better-edge 28, reject-just-mention 8.
> Note on idx 75: the only row I initially marked "legit" resolves to reject (Kingsguard
> sworn-brotherhood is `MEMBER_OF` of the same org, "avenged by" is not a clean edge).
> **Net: 0 truly-legit KNOWS in the 50-row sample.** Every single sampled KNOWS emit is
> either a better edge, a co-presence soft-fallback, a type-contract violation, or a
> non-relationship. KNOWS as emitted in batch-0020 has a ~100% defect rate.

### Headline numbers

- **0/50** are correct KNOWS edges.
- **28/50 (56%)** have a specific better edge available in the 159-type vocab —
  dominant near-misses: `MARRIES_OFF` (×4: idx 31/36/49 + arguable 40), `ALLIES_WITH`,
  `TEACHES`, `SIBLING_OF`, `PROPOSED_AS_BRIDE`, `EXECUTES`, `SERVES`.
- **8/50 (16%)** are not relationships at all (should be `reject_just_mention`).
- **13/50 (26%)** are genuine co-presence with no better type — these are the only
  "defensible" KNOWS, and even they are weak: the prompt's own Pattern-1/-3 guidance says
  co-presence is `reject_just_mention` with reason `temporal-cooccurrence-not-relational`,
  NOT a KNOWS edge.

---

## 2. Dominant pattern analysis

### Frey / Red Wedding co-presence hypothesis: PARTIALLY CONFIRMED — but mis-located

Session 54 predicted "Frey-character cluster co-present at the Red Wedding got KNOWS
emitted for every co-presence pair." The audit **confirms the co-presence-→-KNOWS
mechanism** but **refutes the Red Wedding as the specific trigger.**

The 140 KNOWS-fallback rows come from only **19 source slugs**, and they are dominated by
two house buckets, not by a Red Wedding guest list:

| Source cluster | KNOWS rows | Bucket |
|---|---:|---|
| House Frey (walder-frey + 8 minor Walders/Waldas/Rivers) | ~86 | `characters-house-frey-t-z` |
| House Glover (robett, ethan, galbart, glover-steward, lyanne) | ~61 | `characters-house-glover` |
| House Gargalen / Gardener / Gaunt / Goodbrook | ~7 | minor buckets |

The **actual dominant pattern is the minor-character wiki-biography roll-up**: minor
house members (the interchangeable Walders, the Glover brothers) have short wiki pages
that are dense lists of *"X was present when Y happened"* sentences. Every named entity in
that biography becomes a `source_target` candidate, and the classifier — finding no
betrothal/kill/service verb — emits `KNOWS` as the residual. The Red Wedding is *one* of
the events these biographies recite, but Deepwood Motte, the Crag, Ramsay's feast at
Winterfell, the Defiance of Duskendale, the Field of Fire (idx 70), and Robert's
Rebellion (idx 77/82/83) all produce identical KNOWS-fallback emits. **The trap is
"co-presence in a recited biography," not "the Red Wedding."**

### Second-most-common pattern: KNOWS onto non-character targets

27/140 (19%) KNOWS-fallback emits target a `place.*`, `event.*`, `organization.*`,
`concept.*`, or `object.*` node. These are pure type-contract violations: a person cannot
`KNOWS` a castle or a battle. The classifier produced `walder-frey KNOWS winterfell`,
`robett-glover KNOWS skagos`, `galbart-glover KNOWS fight-by-deepwood-motte`. The flagger
only labelled these `knows_as_fallback` — it did not run a KNOWS-target-type check, so
this entire class is invisible in the flag taxonomy. **This is the single most
mechanically-detectable defect class and it is currently uncaught by name.**

### Third pattern: reverse-direction and dead-target leakage

Several rejects (idx 13 reverse-gift, 20/136 dead target, 6/22 not-in-evidence) show the
classifier emitting KNOWS rather than applying the prompt's own reverse-direction and
just-mention rules. KNOWS is being used as the "I don't want to reject this" escape hatch.

### Root cause

KNOWS has no type-contract row in the prompt's "Type contracts" table and no STOP rule.
It is the lowest-friction emit: a Tier-2 edge with an optional qualifier, a generic gloss
("source-of-knowledge basis"), and no source/target type constraint. Faced with a
co-presence sentence, the model's path of least resistance is `KNOWS` + a freeform
qualifier paraphrasing the sentence. Every other near-miss type (`MARRIES_OFF`,
`ALLIES_WITH`, `TEACHES`) requires the model to *recognize* the specific verb;
`reject_just_mention` requires the model to *decline*; KNOWS requires neither.

---

## 3. Non-KNOWS flagged edges breakdown (13 rows)

| Flag class | Count |
|---|---:|
| `attends_non_event` | 12 |
| `fights_in_non_event` | 1 |

### `attends_non_event` (12) — audited per-row

The flagger fires `attends_non_event` when an `ATTENDS` edge's target is not an `event.*`
node. All 12 are genuine defects, splitting into three sub-classes:

**3a. ATTENDS-a-person (6 rows) — Pattern-3 violation, exactly as the prompt warns.**
idx-equivalent rows: `walda-frey-merrett → edmure-tully`, `walda-frey-walton → edmure-tully`,
`walda-rivers-aemon → edmure-tully`, `walder-frey-ryman → edmure-tully`,
`galbart-glover → edmure-tully`, `robett-glover → edmure-tully`. Every one is "attended
the wedding of Edmure Tully" — the classifier targeted **Edmure** (a person) instead of
the **Edmure-Roslin wedding event**. The prompt's Pattern 3 explicitly forbids this
("Never the bride, groom, host, honoree"). The correct target is the wedding event node
if one exists, else `reject` with `no-event-node-available`. *This is the same trap as
KNOWS-fallback — co-presence at a celebration — just routed through ATTENDS instead.*

**3b. ATTENDS-a-place (5 rows) — venue mistaken for event.**
`walder-frey-jammos → godswood-of-winterfell`, `walder-frey-merrett → godswood-of-winterfell`,
`galbart-glover → godswood-of-riverrun`, `galbart-glover → great-hall-of-riverrun`,
`glover-steward → harvest-feast` (harvest-feast may be an event node — borderline).
The classifier targeted the **venue** (a `place.location`) instead of the ceremony held
there. `godswood-of-winterfell` is where Ramsay's wedding happened; the edge should point
at the wedding event, not the godswood. `harvest-feast` is the one arguable case — if a
`harvest-feast` event node exists this is legitimate; the flagger flags it because the
slug resolves to a non-`event.*` type or no node.

**3c. ATTENDS-a-person, court-proclamation variant (1 row).**
`galbart-glover → great-hall-of-riverrun` (counted in 3b) and the proclamation context —
"Galbart in attendance when Robb is proclaimed King in the North." The event is the
proclamation; the target should be that event, not the hall.

### `fights_in_non_event` (1) — audited

`walder-frey-son-of-ryman → crag` (tier 1). Evidence: "When Robb's army storms the Crag …
Black Walder … lead scaling parties over the walls." `crag` resolves to a
`place.location` (the Westerling castle), not an `event.*`. This is Pattern-2 in the
prompt: FIGHTS_IN must target a battle/war/tournament event. The correct edge is
`FIGHTS_IN` → the *storming-of-the-Crag* event if such a node exists (it likely does not),
else `BESIEGES walder-frey-son-of-ryman → crag` (BESIEGES legitimately targets a place) —
or reject. The classifier conflated the siege *event* with the castle *place*.

### Non-KNOWS summary

All 13 non-KNOWS flags are legitimate defects. **12 of 13 are the same underlying error
as the KNOWS problem**: an interpersonal/participation relationship at a named occasion,
where the classifier targets the *person* or the *venue* instead of the *event node* —
because the event node frequently does not exist in the graph, so there is nothing
correct to point at. This strongly suggests the `ATTENDS`/`FIGHTS_IN` defects and the
`KNOWS` defects share one root: **the graph lacks fine-grained event nodes (individual
weddings, feasts, sieges), so the classifier has no correct target and improvises.**

---

## 4. Prompt diagnostic recommendations

Recommendations only. Do NOT apply — Matt verdicts these before STEP 5.

The prompt is already strong on CONTEMPORARY_WITH (Pattern 1), FIGHTS_IN (Pattern 2), and
ATTENDS-a-person (Pattern 3). batch-0020 proves those three patterns get *named in the
prompt* but the **KNOWS escape hatch is wide open** and the **co-presence-at-an-occasion
trap is not centralized**. Four concrete changes, in priority order:

### R1 (highest impact) — Add a KNOWS STOP rule + type contract

Add to the "Common failure patterns" section a new **Pattern 5**:

> ### Pattern 5: NEVER use KNOWS as a fallback for co-presence
>
> `KNOWS` records that one *person* has *knowledge of a fact, secret, or another person's
> situation* — sourced from explicit prose. It is **NOT** a catch-all for two characters
> who appear in the same sentence, attend the same feast, ride in the same party, or are
> recited together in a wiki biography.
>
> **STOP — do not emit `KNOWS` unless the `evidence_snippet` contains an explicit
> knowledge verb or construction:** one of `knew`, `knows`, `known to`, `aware of`,
> `learned that`, `learned of`, `told that`, `told of`, `informed`, `overheard`,
> `discovered`, `realized`, `suspected`, `confirmed`, `witnessed` (witnessed-an-event),
> or a direct statement that the source knows a named fact/secret. If the snippet only
> establishes that two people were *present together* or *named together*, the correct
> action is one of:
> 1. Emit the **specific relationship edge** the occasion implies (`MARRIES_OFF`,
>    `ALLIES_WITH`, `SERVES`, `TEACHES`, `PROPOSED_AS_BRIDE`, `OPPOSES`, `CAPTURES`, …).
> 2. If no specific edge fits, `reject_just_mention` with reason
>    `temporal-cooccurrence-not-relational`. **Co-presence is a rejection, not a KNOWS.**
>
> **`KNOWS` has a type contract: target MUST be `character.*`.** Never emit
> `KNOWS → place.*`, `KNOWS → event.*`, `KNOWS → organization.*`, `KNOWS → object.*`,
> `KNOWS → concept.*`. A person does not `KNOWS` a castle, a battle, or a house.
> If the target is non-character, `KNOWS` is wrong by construction.
>
> Concrete WRONG emits observed in prior batches:
> - `walder-frey KNOWS winterfell` — type-contract violation (place target).
> - `galbart-glover KNOWS fight-by-deepwood-motte` — type-contract violation (event target).
> - `walder-frey-son-of-jammos KNOWS hother-umber` ("both at Ramsay's feast") — co-presence;
>   reject as `temporal-cooccurrence-not-relational`.
> - `walder-frey KNOWS lancel-lannister` ("Lancel betrothed to Walder's granddaughter")
>   — emit `MARRIES_OFF`, not KNOWS.

Also add a row to the **"Type contracts on common-failure edge types"** table:

> | `KNOWS` | `character.*` | `character.*` — **never `place.*`, `event.*`, `organization.*`, `object.*`, `concept.*`** |

### R2 — Add a "co-presence at a named occasion" centralized rule

Patterns 3 (ATTENDS) and the new Pattern 5 (KNOWS) share one root. Add a short paragraph
to the failure-modes preamble:

> **The co-presence-at-an-occasion trap (applies to KNOWS, ATTENDS, FIGHTS_IN).** Minor
> characters' wiki biographies are dense lists of "X was present when Y happened."
> Each named entity in such a sentence becomes a candidate. Do not manufacture an edge
> for every co-presence. Ask: does the prose state a *typed relationship* (betrothal,
> service, command, killing, teaching), or merely that two entities were *near each
> other*? If the latter, and the occasion is a named event WITH a graph node, emit a
> single `ATTENDS → <event-node>`. If the occasion has no event node, `reject_just_mention`
> with `no-event-node-available`. Do not redirect the unmet edge onto a person or a venue.

### R3 — Tighten the KNOWS qualifier-vocab entry's framing

`reference/edge-qualifier-vocab.md`'s KNOWS row currently glosses it as "Source-of-
knowledge basis" with enum `confirmed/suspected/told_by/witnessed/overheard/unknown` — and
every enum value *except* `unknown` already implies an explicit knowledge verb. The
Tier-2 OPTIONAL status lets the classifier emit KNOWS with **no qualifier at all**, which
is exactly what 140/140 batch-0020 rows did (their `qualifier` is freeform prose, not an
enum value — a separate schema violation the validator will now also catch). Recommend:
in the prompt's step-4 qualifier-lookup instruction, add a line — *"If you are emitting
`KNOWS` and cannot assign one of its non-`unknown` enum values (`confirmed`, `suspected`,
`told_by`, `witnessed`, `overheard`) from explicit prose, that is a signal the edge is not
a real KNOWS — re-evaluate against Pattern 5 before emitting."* The qualifier enum becomes
a self-check gate.

### R4 — Flagger enhancement (script, not prompt — for STEP 4 follow-up, optional)

`scripts/wiki-pass2-flag-suspicious-edges.py` should add a `knows_non_character_target`
flag class (KNOWS/IGNORANT_OF/TRUSTS/etc. with non-`character.*` target). batch-0020 has
27 such rows currently hidden inside the generic `knows_as_fallback` bucket. This makes
the type-contract violations independently countable in future cross-model audits. Out of
scope for this READ-ONLY audit — noted for Matt.

### Expected effect

R1 alone should eliminate the 27 non-character KNOWS emits (mechanical type contract) and
should convert most of the 56% "better-edge" rows — the model is not failing to *know*
`MARRIES_OFF` exists; it is failing to *look* because KNOWS is frictionless. A STOP rule
that forces an explicit-verb check before KNOWS removes the frictionless path. The 26%
soft-fallback co-presence rows should convert to `reject_just_mention`. Residual legit
KNOWS will be rare (the corpus genuinely has few — confirmed: 0/50 in this sample).

---

## 5. Haiku smoke readiness verdict

### VERDICT: **needs prompt change first.**

The current locked-down stack — prompt + 159-type vocab + 18-type qualifier vocab +
validator + flagger — is **NOT ready** to fire the Haiku smoke as-is. One concrete
minimum change is required before smoke.

**Reasoning.** This audit found that batch-0020's 35% flag rate is not noise — it is a
real, structural defect with a 0/50 legit rate on the dominant flag class. KNOWS-fallback
is the single largest failure surface in the entire 21-batch Sonnet corpus (82.3% of all
KNOWS emits; 140/163 project-wide flags concentrated here). It was produced by **Sonnet**,
the stronger model. The Haiku smoke's purpose is a cross-model schema-drift comparison
(per the drift-detection-mandatory rule); firing it against a prompt with a known,
un-patched, wide-open fallback channel guarantees Haiku reproduces and amplifies it —
Haiku is documented as more drift-prone (Session 54: Haiku smoke was "~80% semantic
failure, SERVES-on-everything"). A KNOWS escape hatch that Sonnet abuses 82% of the time
will be abused at least as hard by Haiku, and the smoke result will be uninterpretable:
we will not be able to distinguish "Haiku-specific drift" from "prompt-defect both models
share." A smoke test must isolate the model variable; right now the prompt is a confound.

**The minimum change before smoke fires** is exactly **Recommendation R1**: add Pattern 5
(KNOWS STOP rule + explicit-knowledge-verb gate + KNOWS `character.*`-only type contract)
to the prompt's "Common failure patterns" section, and add the `KNOWS` row to the type-
contracts table. R1 is self-contained, copy-paste-ready in Section 4 above, changes no
data and no vocab, and directly closes the channel responsible for 92% of batch-0020's
flags (140/153). R2/R3 are recommended companions and cheap to add in the same edit, but
**R1 is the hard gate.** Without it, the smoke is not measuring what it claims to measure.

**After R1 is applied:**

- **Expected failure rate (Haiku, post-R1):** target **≤10% flag rate** on a re-classified
  batch (down from batch-0020's 35%). Rationale: R1 mechanically removes the 27 non-
  character KNOWS (type contract) and forces the explicit-verb check that should convert
  most co-presence emits to rejections or specific edges. Residual will be Haiku's own
  drift (type-contract slips, direction errors, under-tiering) — the 5-7% baseline Session
  54 accepted, plus a Haiku premium. If post-R1 Haiku still exceeds ~15% flag rate, Haiku
  should be rejected for the bulk run (consistent with the Session 54 Haiku rejection) and
  the smoke has done its job as a gate.

- **Should batch-0020 be the canonical smoke target?** **Yes — strongly recommended, but
  only AFTER R1 is applied.** batch-0020 is the most informative possible cross-model
  comparison precisely *because* it is the hot zone: re-classifying it with R1-patched-
  prompt + Haiku gives a clean three-way read — (a) does R1 fix the defect at all
  (Sonnet-defect vs R1-Sonnet would show this, but we have the Sonnet control arm
  already), (b) does Haiku-with-R1 stay near the ≤10% target, (c) direct row-level diff
  against the preserved Sonnet control arm for the same 437 candidates. Keep the existing
  batch-0020 Sonnet prose-edges JSONL as the frozen control arm (do not modify — already a
  hard DO-NOT). Re-run batch-0020 candidates through Haiku-with-R1-prompt into a separate
  output path (e.g. `_archive/batch-0020-haiku-smoke-<date>/` or a sibling dir) so the
  control arm is untouched. The drift-detection-mandatory rule's verdict-gate then applies:
  the mechanical validator + this-style audit gate whether Haiku resumes the bulk run.

**One-line answer for the orchestrator:** Do not fire the Haiku smoke yet. Apply
Recommendation R1 (the KNOWS STOP rule + type contract) to `prose-edge-classifier.md`
first; then fire the smoke against batch-0020 re-classified by Haiku, expecting a ≤10%
flag rate and treating >15% as a Haiku-rejection signal.

---

## Summary (<250 words)

batch-0020 is a structural-defect hot zone, not statistical noise. Of 153 flagged emits,
140 are `KNOWS`-as-fallback, 12 `ATTENDS`-non-event, 1 `FIGHTS_IN`-non-event. A stratified
50-row sample of the KNOWS emits found **zero correct KNOWS edges**: 56% should have been a
specific existing edge type (`MARRIES_OFF`, `ALLIES_WITH`, `TEACHES`, `SIBLING_OF`,
`EXECUTES`, `PROPOSED_AS_BRIDE`, `SERVES`), 16% are not relationships at all, and 26% are
co-presence that the prompt's own rules say should be rejected. Additionally, 27/140 KNOWS
emits target non-character nodes (places, events) — pure type-contract violations the
flagger does not name.

The Session 54 "Frey/Red Wedding" hypothesis is partially confirmed: the co-presence-→-
KNOWS mechanism is real, but the trigger is the **minor-character wiki-biography roll-up**
(interchangeable Walders, Glover brothers) — only 19 source slugs produce all 140 rows.
The Red Wedding is just one recited event among many (Deepwood Motte, the Crag, Ramsay's
feast). The 13 non-KNOWS flags share the same root: an interpersonal/participation
relationship at a named occasion, mis-targeted at a person or venue because the graph
lacks fine-grained event nodes.

Root cause: `KNOWS` is the frictionless emit — Tier-2, optional qualifier, no type
contract, generic gloss. **Verdict: the stack is NOT Haiku-smoke-ready.** Apply
Recommendation R1 (Pattern 5: KNOWS STOP rule + explicit-knowledge-verb gate +
`character.*`-only type contract) to the classifier prompt first. Then re-classify
batch-0020 with Haiku as the canonical smoke, expecting ≤10% flag rate; treat >15% as a
Haiku-rejection signal.
