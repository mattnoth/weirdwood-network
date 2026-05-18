# Stage 4 Vocab Lock — Decisions for 2026-05-18

> **Purpose:** lock the master edge vocabulary in preparation for the Haiku smoke run + bulk cutover. Every open `vocabulary-gap` row in `working/wiki/pass2-buckets/questions-for-matt.jsonl` is addressed here. After Matt's review, the classifier prompt switches to "vocab is FINAL — do not file vocabulary-gap questions; reject with reason `no-fitting-type-vocab-locked`."
>
> **Inputs:** `working/wiki/pass2-buckets/questions-for-matt.jsonl` (68 rows; 53 vocab-gap class), `reference/architecture.md` § "Edge Types" (132 canonical types after Session 55), `working/agent-fleet-specs/stage4-vocab-gaps-rollup.md` (normalized rollup), `working/agent-fleet-specs/stage4-vocab-gaps-normalized.jsonl`.
>
> **Bucketing (split-by-confidence per Matt 2026-05-18):**
> - **A (stale)** — proposed type already in canon → close gap rows as duplicates
> - **B (recommend ACCEPT)** — clear semantic gap, no fitting existing type → I propose the architecture.md diff
> - **C (recommend HARD-REJECT)** — reverse-direction violation or duplicate of existing type → close with reason
> - **D (surface only)** — borderline; Matt's call

---

## Bucket A — Stale-resolved (CLOSE as duplicates)

These were filed BEFORE the proposed type was added to canon. No new architecture work; just close the gap rows.

| Proposed type | In canon since | Rows | Disposition |
|---|---|---|---|
| `ATTENDS` | Session 54 (2026-05-15) | 2 | Close as `resolved-pre-adopted` |
| `BETROTHED_TO` | pre-Stage-4 | 1 | Close — already canonical |
| `COUSIN_OF` | Session 55 (2026-05-16) | 2 | Close |
| `DEPICTED_IN` | Session 55 | 1 | Close |
| `GIFTED_TO` | pre-Stage-4 (architecture.md row 276) | 1 | Close |
| `KNIGHTED_BY` / `BESTOWS_KNIGHTHOOD_ON` | Session 55 | 1 | Close — both directions canonical |
| `MADE_OF` | pre-Stage-4 (row 273) | 1 | Close |
| `MILK_BROTHER_OF` | Session 55 | 1 | Close |
| `NURSED_BY` / `WET_NURSE_OF` | Session 55 | 1 | Close — both directions canonical |
| `UNCLE_OF` / `NEPHEW_OF` | Session 54 | 1 | Close — both directions canonical |

**Total: 12 stale gap rows to close.**

---

## Bucket B — Recommended ACCEPT (4 new types, 1 deprecated-synonym note)

### B.1 — `AFFLICTED_BY` + `DIED_OF` (disease/medical-cause edges)

**Filed:** AFFLICTED_BY 1×, DIED_OF 2×. Continue prompt called these out explicitly.

**Examples:**
- `albin-massey → shivers` — "Lord Albin perished during the harsh winter of 59 AC from the Shivers."
- `donnel-hightower → shivers` — "Later that same year, Lord Donnel died from the Shivers."
- `medrick-manderly → winter-fever` — "Lord Desmond and the childless Medrick died of Winter Fever four days apart in 132 AC"

**Why no existing type fits:**
- `KILLED_BY` requires a person-killer (target = `character.*`); disease is `concept.medical`.
- `DIED_AT` is location, not cause.
- The graph value is real: links characters → `concept.medical` nodes (greyscale, shivers, winter fever, spring sickness, milk of the poppy, etc.) → enables "show me all greyscale deaths" / "what diseases killed Westerosi lords."

**Recommendation:** ACCEPT both. `DIED_OF` for died-from; `AFFLICTED_BY` for living-with (Jorah/Shireen/Stannis-greyscale, etc.).

**Architecture.md diff** — append to the Knowledge & Information section (or new "Medical" subsection — but I'd just slot under Knowledge for now to keep the section count steady):

```
| `AFFLICTED_BY` | Character suffers from a named disease, condition, or magical affliction. Target is `concept.medical`. Distinct from `KILLED_BY` (target = person), `DIED_AT` (location), `DIED_OF` (cause-of-death; this is the living state). Examples: Jorah Mormont/greyscale, Shireen Baratheon/greyscale, Stannis/burns. | Character → Medical | — |
| `DIED_OF` | Character's death was caused by a named disease/condition. Target is `concept.medical`. Distinct from `KILLED_BY` (person-killer), `DIED_AT` (location), `EXECUTED_WITH` (judicial weapon). Mirrors `AFFLICTED_BY` for the post-mortem state. Examples: Hoster Tully/Spring Sickness, Albin Massey/Shivers, Medrick Manderly/Winter Fever, the Old King Jaehaerys/Great Spring Sickness. | Character → Medical | — |
```

**Subsection placement note:** these are medical-state edges. The simplest home is **Knowledge & Information** (existing `HEALS` is medical-adjacent), or I can propose a new **Medical & Affliction** subsection if you want them grouped. Either way works. Default to Knowledge & Information unless you say otherwise.

---

### B.2 — `COMPANION_OF` (personal friendship)

**Filed:** 1× explicit (`patrek-mallister → edmure-tully`); referenced in continue prompt as a recurring pattern (patrek/theon/marq-piper/edmure triples).

**Example:**
- `patrek-mallister → edmure-tully` — "He is good friends with Ser Edmure Tully, the heir to Riverrun."

**Why no existing type fits:**
- `ALLIES_WITH` — political alliance; symmetric. The patrek/edmure relationship pre-dates and outlasts any political alignment.
- `TRUSTS` — one-direction; lower bar (places confidence in) and doesn't capture mutual affection.
- `LOVES` — too strong; reserved for romantic / deep familial / Jon-and-Ghost-type bonds.
- `RESPECTS` — too cold.

**Recommendation:** ACCEPT. Symmetric. Common pattern in feudal-noble social networks that the existing vocab misses.

**Architecture.md diff** — append to Emotional & Perceptual:

```
| `COMPANION_OF` | Close personal friendship or camaraderie. Distinct from `ALLIES_WITH` (political alliance), `TRUSTS` (one-direction confidence), `LOVES` (romantic/deep-familial), `RESPECTS` (cold regard). Use when prose explicitly names a friendship ("good friends with", "sworn brothers", "close companion"). Examples: Patrek Mallister & Edmure Tully; Robert & Ned in their youth; the Brienne/Pod relationship; Davos/Salladhor Saan. | Symmetric | — |
```

---

### B.3 — `PARTICIPATES_IN` (non-combat event involvement)

**Filed:** 1× explicit; continue prompt called out the Medrick Manderly/Hour-of-the-Wolf case.

**Example:**
- `medrick-manderly → hour-of-the-wolf` — "During the Hour of the Wolf after the war, Medrick agreed to transport those men taking the black"

**Why no existing type fits:**
- `FIGHTS_IN` — explicitly combat (architecture.md). Type-contract violation if used here.
- `ATTENDS` — non-combatant **guest / witness / audience** at a wedding / feast / tourney / court hearing. Medrick is doing logistical work, not attending.
- `COMMANDS_IN` — too narrow; not all participants command.

**Recommendation:** ACCEPT. Fills the gap between FIGHTS_IN (combat) and ATTENDS (guest/witness) for active-but-non-combat event participation.

**Architecture.md diff** — append to Military & Conflict (despite the name; the type spans military and non-military events):

```
| `PARTICIPATES_IN` | Active non-combat involvement in a named event — logistical, administrative, organizational, or supportive role. Distinct from `FIGHTS_IN` (combatant), `ATTENDS` (guest/witness/audience), `COMMANDS_IN` (command-tier role). Target is `event.*`. Examples: Medrick Manderly transporting men to the Wall during the Hour of the Wolf; quartermasters in named battles; ceremony officiants who aren't officiants in the religious-role sense. | Person → Event | — |
```

---

### B.4 — `OFFICIATES` (officiant at named event)

**Surfaced via untyped row 13** — melisandre officiating Sigorn-Alys wedding.

**Example:**
- `melisandre → wedding-of-sigorn-and-alys-karstark` — Melisandre performs the marriage ceremony at the godswood / nightfire wedding.

**Why no existing type fits:**
- `CLERGY_OF` — character → religion, not character → specific-event.
- `ATTENDS` — guest/witness, not officiant.
- `PARTICIPATES_IN` (proposed above) is administrative; OFFICIATES is the ritual role specifically.

**Recommendation:** ACCEPT. Common pattern: marriage officiants (septons, Red Priests, Old Gods weirwood ceremonies), funeral officiants, kingsmoot chairs (the Damphair), coronations (the High Septon).

**Architecture.md diff** — append to Cultural & Religious:

```
| `OFFICIATES` | Character performs the ritual/religious/ceremonial role at a named event (weddings, funerals, coronations, kingsmoots, namedays, knighting ceremonies). Distinct from `CLERGY_OF` (general clergy status, target = religion) and `ATTENDS` (guest/witness). Target is `event.*` or specific named ceremony node. Examples: Melisandre/wedding-of-sigorn-and-alys-karstark; the High Septon/coronation-of-tommen-i; Aeron Damphair/kingsmoot-of-299-ac. | Character → Event | — |
```

---

### B.5 — Deprecated-synonym note for the canonical-already pairs

Three rows proposed compound types where BOTH halves are already canonical, but the rows used `OR` framing that suggested ambiguity. Document for the worker:

- `KNIGHTED_BY / BESTOWS_KNIGHTHOOD_ON` — both canonical. Emit `KNIGHTED_BY` on the recipient's node; emit `BESTOWS_KNIGHTHOOD_ON` on the dubber's node. NOT one OR the other — both, on their respective endpoints.
- `NURSED_BY / WET_NURSE_OF` — both canonical. Same pattern.
- `UNCLE_OF / NEPHEW_OF` — both canonical. Same pattern.

**Action:** the **classifier prompt's "Reverse-direction edges" section needs to add these three pairs to the "both-sided" list** (architecture.md already lists both, but the prompt's "Reverse-direction emission IS intended for a few types where both directions carry independent meaning" list only contains KILLS/KILLED_BY, UNCLE_OF/NEPHEW_OF, WARD_OF/FOSTERED_BY). Add KNIGHTED_BY/BESTOWS_KNIGHTHOOD_ON and NURSED_BY/WET_NURSE_OF.

---

## Bucket C — Recommended HARD-REJECT (close with reason)

### C.1 — Reverse-direction violations of existing one-sided types

These types proposed reverse directions of types that are explicitly **one-sided** in architecture.md. The agent prompt already says "if your source is [the wrong endpoint], reject_just_mention with reason `reverse-direction-edge-belongs-on-[other]-node`." These should never have been filed as gaps.

| Proposed type | Reverse of canonical | Reason to close |
|---|---|---|
| `CHILD_OF` | `PARENT_OF` (parent → child) | One-sided per architecture.md. Use PARENT_OF on parent's node. |
| `HOST_OF` / `HOSTED_BY` | `GUEST_OF` (guest → host) | One-sided. Use GUEST_OF on guest's node. (2 rows; same answer.) |
| `RESURRECTED_BY` | `RESURRECTS` (resurrector → resurrected) | One-sided per the agent prompt's reverse-direction list. Use RESURRECTS on resurrector's node. |
| `SERVED_BY` / `EMPLOYS` | `SERVES` (server → served) | One-sided. Use SERVES on server's node. |
| `DEFEATED_BY` | `DEFEATS` (victor → defeated) | One-sided. Use DEFEATS on victor's node. |
| `GUARDIAN_OF` | `WARD_OF` / `FOSTERED_BY` | **`FOSTERED_BY` is the explicitly-permitted reverse of WARD_OF** per architecture.md row 156. Use FOSTERED_BY. (The agent that filed GUARDIAN_OF didn't see the reverse-permitted note.) |

**Action:** close all six rows with reason `reverse-direction-of-canonical-type-X`. Update the classifier prompt's Pattern-list to call out these explicitly so they don't get re-filed.

---

### C.2 — Too-generic / duplicates of existing types

| Proposed type | Closest canonical | Why hard-reject |
|---|---|---|
| `RELATED_TO` | none — too generic | Refuse generic kinship. If degree is unknown, reject the candidate as `no-fitting-type` rather than emit RELATED_TO. The graph value of a "related somehow" edge is near zero. |
| `KINSMAN_OF` | none — too generic | Same. If you don't know the kinship degree, don't emit. |
| `LIAISED_WITH` | `LOVER_OF` | `LOVER_OF` description in architecture.md is "Romantic/sexual relationship outside marriage" — covers rumored affairs. Use LOVER_OF. |

---

## Bucket D — Surface only (Matt's call)

For each of these I'll lay out the case + the closest existing types + the trade-off. No recommendation; Matt decides.

### D.1 — `ASSAULTS` / `ATTACKS` (physical violence not resulting in death)

**Filed:** ASSAULTS 2×, ATTACKS 1×, plus the alysanne-bracken untyped row (sexual violence). Pattern is genuinely recurring.

**Examples:**
- `owen-inchfield → brienne-tarth` — "Ser Owen Inchfield and Ser Raymun Fossoway... attempted to have their way with her. Ser Randyll Tarly stopped them." (attempted sexual assault)
- `gerold-dayne → myrcella-baratheon` — "Darkstar succeeds only in slicing off her ear and scarring her face." (attempted murder)
- `alysanne-bracken → gregor-clegane` — Five Bracken sisters raped by Gregor during Burning of the Riverlands (canonical sexual violence)

**Existing types that *almost* fit:**
- `KILLS` — requires death.
- `EXECUTES` — judicial-only.
- `POISONS` — method-specific.
- `DUELS` — formal mutual combat.
- `CAPTURES` — battlefield-taking, not unprovoked violence.

**Open question for Matt:**
1. Single type `ATTACKS`, or split into `ATTACKS` (physical) + `RAPES` (sexual)? The sexual violence pattern is recurring (Brackens, Cersei's walk-of-shame mob, Daenerys/Drogo wedding-night, etc.) and the graph value of being able to query it is high — but the type name is sensitive and how it's labeled matters.
2. Or: file under a softer phrasing like `VICTIMIZES` / `HARMS`?

### D.2 — `COURTS` (suitor relationship, pre-betrothal)

**Filed:** COURTS 1×, COURTED 1×. Pattern: Lysa Arryn's many suitors, Rohanne Webber's suitors, Sansa's suitors before her marriage.

**Examples:**
- `eon-hunter → lysa-arryn` — "Eon is one of Lysa Arryn's suitors after the death of Lord Jon Arryn."
- `cleyton-caswell → rohanne-webber` — "Cleyton Caswell was a suitor who sought to court Rohanne Webber"

**Closest canonical:**
- `BETROTHED_TO` — formally engaged. Suitors aren't betrothed yet.
- `LOVER_OF` — sexual/romantic relationship. Suitors haven't necessarily had one.

**Trade-off:** add `COURTS` (one-direction, suitor → object-of-courtship) → captures the pre-betrothal phase that's plot-significant. Or: reject as "marriage-track relationship without formal status."

### D.3 — `COMMISSIONED` / `MEMORIALIZED_IN` (named-for-honor)

**Filed:** COMMISSIONED 1×, MEMORIALIZED_IN 1×, NAMED_AFTER 1×, NAMED_FOR 1×. Same underlying pattern: a person commissions a building/song/tower in another's honor, OR a person is named after another.

**Examples:**
- `triston-hightower → starry-sept` (commissioner) — "Lord Triston raised the Starry Sept in Robeson's honor"
- `robeson → starry-sept` (honoree) — same prose, other endpoint
- `gwynesse-harlaw → widows-tower-ten-towers` — "the Widow's Tower in her honor"
- `rickard-karstark → rickard-stark` — "Rickard Karstark was named after Lord Rickard Stark"

**Closest canonical:**
- `FOUNDED` — covers the commissioning of buildings/institutions.
- (none for honoree-of-monument or namesake)

**Trade-off:** add `MEMORIALIZED_IN` (person → text/structure named in their honor) + `NAMED_AFTER` (person → person they were named after)? Or: collapse all naming/eponym into `MEMORIALIZED_IN` with target type = structure/text/person? The honoree-of relationship is plot-irrelevant for most cases.

### D.4 — Extended kinship — `GREAT_UNCLE_OF` / `DAUGHTER_IN_LAW_OF` / `STEP_PARENT_OF`

**Filed:** 1× each.

**Trade-off:** these are derivable from existing edges (PARENT_OF + SPOUSE_OF + SIBLING_OF chains) at query time. The argument for explicit types is the same as the UNCLE_OF/COUSIN_OF argument from Session 54-55: one-hop traversal is more reliable than multi-hop joins with possibly-missing intermediate nodes. But the frequency is lower than uncle/cousin.

**Three positions:**
- Add all three (consistency with UNCLE_OF/COUSIN_OF/MILK_BROTHER_OF additions).
- Add `STEP_PARENT_OF` only (highest narrative weight: bethany-tarly/ormund-hightower, etc.); reject the other two.
- Reject all three; derive from chains at query time.

### D.5 — Commerce / contract — `CONTRACTED_WITH` / `PURCHASED_FROM` / `BRIBES` / `BUILT` / `CREW_OF`

**Filed:** 1× each (BUILT/BRIBES are deprecated-schema untypeds with no target slugs — minimal context).

**Trade-off:**
- `CONTRACTED_WITH` ("hired the Faceless Men to assassinate") — could be `APPOINTS` (too narrow) or new type.
- `PURCHASED_FROM` — commerce. Frequency probably low — most narrative-significant transactions are non-commercial.
- `CREW_OF` — being on a ship's crew. `MEMBER_OF` with target = ship is awkward because ships are `object.artifact`, not orgs. Could be `SERVES` (ship's captain) or new.
- `BRIBES` / `BUILT` — too little context to evaluate.

Best to surface and let Matt either pick one or reject the whole bucket.

### D.6 — Other low-frequency / borderline

| Proposed type | Filed | Verdict-leaning |
|---|---|---|
| `PROPOSED_AS_BRIDE` | 1× | Could subsume into `MARRIES_OFF` (arranger's role) with a qualifier "proposed". Surface. |
| `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` | 1× | Too specific. Could be `HONORS` or a qualifier on `ATTENDS`. Surface. |
| `REPUTED_AS` | 1× | "Reputed witch" — could be `PERCEIVED_AS` but target is `concept.magic` not `character.*`. Could add type-loosening to PERCEIVED_AS, or a new type. Surface. |
| `PETITIONED` | 1× | Could be `NEGOTIATES_WITH` (Barba petitioned Aegon III). Surface. |
| `USES_AS_SIGIL` | 1× | Better as metadata on the house node, not an edge. Lean reject. Surface. |
| `WARGS_INTO` 's pair — practices magic on a magic concept | untyped row 12 (Melisandre/shadow-children/glamors) | Distinct from WARGS_INTO. Could be `PRACTICES` (character → concept.magic). New type? Surface. |

---

## What to do after Matt reviews

### Step 1 — Apply Matt's verdicts to architecture.md

For each Bucket-B accept: append the new type row to the relevant section in `reference/architecture.md` (write the new row at the bottom of its subsection, matching the existing markdown table style).

For each Bucket-C reject + each Bucket-A stale: no architecture.md change.

For each Bucket-D verdict: same as B (if accepted) or no change (if rejected).

### Step 2 — Sync the classifier prompt

Update `.claude/agents/prose-edge-classifier.md`:
1. Bump the "Vocabulary lock" section's count from "~125 edge types" to the new count after additions.
2. Add the new types to the Kinship/Political/Military/etc. category-expansion paragraph.
3. **Lock the gap-filing behavior** — change the default from "file vocabulary-gap question + reject_just_mention" to "vocab is FINAL — reject_just_mention with reason `no-fitting-type-vocab-locked`. Do NOT file vocabulary-gap questions for remaining batches."
4. Update the "Reverse-direction edges" both-sided list to include the new both-sided pairs (KNIGHTED_BY/BESTOWS_KNIGHTHOOD_ON, NURSED_BY/WET_NURSE_OF — already in canon but the prompt's both-sided list doesn't enumerate them).

### Step 3 — Close the stale + rejected gap rows in questions-for-matt.jsonl

Write a small Python script that appends a `resolved_at` + `resolution` field to each row in Buckets A and C (and B/D once decided). Don't delete rows — append-only channel per the agent contract.

### Step 4 — Hand off to Step 2 of the continue prompt (Sonnet reject baseline)

Once vocab is locked, the next step is the Sonnet-reject-quality audit on complex pages (wyman-manderly, wylis-manderly, bowen-marsh, taena-merryweather, hallis-mollen). That establishes the baseline that the Haiku smoke must match.

---

## Summary count

- **Bucket A (stale):** 12 rows close, 0 architecture work
- **Bucket B (accept):** 4 new types proposed (AFFLICTED_BY, DIED_OF, COMPANION_OF, PARTICIPATES_IN, OFFICIATES), 1 doc-only note (reverse-pair documentation in classifier prompt)
- **Bucket C (reject):** 9 rows close with reason
- **Bucket D (surface):** 18 rows pending Matt's call across 12 distinct proposed types

After Matt's review, the canonical vocab grows from 132 to (132 + Bucket-B-approved + Bucket-D-approved). Plausible final count: **136-145 edge types**.
