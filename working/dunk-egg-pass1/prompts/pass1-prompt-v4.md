# Pass-1 Mechanical Extraction Prompt — v4 (Dunk & Egg variant)

> **Version:** `v4` — authoritative version id is the **filename** (`prompts/pass1-prompt-v4.md`); the
> worker resolves a prompt by `--prompt-version`. Smoke variants are sibling files: `pass1-prompt-v4b.md`,
> `pass1-prompt-v4c.md`, … (copy this file, tweak, bump the suffix). Only ONE version is promoted to the
> full run (pinned in the weirwood track command); the rest stay as smoke history.
> **Status:** DRAFT for Matt's review (S131/132). NOT yet wired into a worker. NOT run.
> **Scope:** Dunk & Egg novellas only (THK / TSS / TMK). A hardened descendant of the v3
> `mechanical-extractor.md` prompt. If it proves out, it can be back-ported to a general v4.
> **Hard constraint — output table STRUCTURE is FROZEN vs v3.** The Stage-4 edge pipeline parses
> `## Relationships Observed`, `## Events & Actions`, and the 12-category `## Raw Entity List`
> by exact header. **Do not add/rename/reorder tables or the 12 category headers.** New v4 content is
> *guidance, context, and sidecar output* — never a structural change.
> **One paired-change EXCEPTION (rule #6):** v4 locks the Relationship column to the controlled edge
> vocabulary. That does NOT change the table's shape, but it does bring the prompt in line with
> `architecture.md:687` (which already names the Pass-1 extractor a vocab emitter) and **supersedes the
> stale `architecture.md:161` free-text note** — §161 must be corrected when v4 ships. Recorded as an
> Active Decision (see run-plan). This is a doc-correctness fix, not a schema redesign.

---

## Why v4 exists (read this, orchestrator)

The v3 prompt ran all 5 books well, but it was written to be loaded by a **Claude Code subagent**
that *also* reads `CLAUDE.md`, `reference/architecture.md`, and the agent definition. The D&E run is
**`claude -p` in a bare `/tmp` cwd** (≈49% cheaper — skips the project context load; memory
`reference_llm_pass_via_claude_p`). That means **none of the project's standing rules are in context.**
So v4 **self-contains** every rule the extractor needs, and it folds in three years of lessons:

1. **The reactively-patched v3 rules are now front-loaded, not buried** (the Head rule, no
   meta-commentary in cells, dramatic-irony isolation, "None" in empty categories — each was added
   *after* an early book pass got it wrong).
2. **Harvest + capture-quote pointers are baked in** (memory `feedback_harvest_queue`,
   `feedback_capture_quotes_during_research`) — these normally live in CLAUDE.md, which `claude -p`
   never sees, so they MUST travel in the prompt or the saga-connection breadcrumbs are lost.
3. **D&E-specific handling** for concealed identity (Egg = Aegon), the Bloodraven evidence substrate,
   and the no-Pass-1-yet status of these novellas.
4. **"More room" exploitation** — only 3 units, so we can afford to be slower, more exhaustive, and to
   self-checkpoint. Budget is not the constraint here; completeness is.

---

## THE PROMPT (everything below the line is what the worker sends)

═══════════════════════════════════════════════════════════════════════════════

You are a **mechanical extraction agent** for the Weirwood Network — a structured ASOIAF knowledge
graph. You are processing **one unit of a Tales of Dunk & Egg novella**. Produce a single structured
extraction file. This is **Pass 1**: you capture *facts*, exhaustively; later passes do analysis.

### Files you will be given (read in this order)
1. `{ARCH_PATH}` — the architecture spec (entity types, edge types, confidence tiers, naming). Read the
   entity-type and edge-type sections so your `## Raw Entity List` categories and relationship labels
   match the live schema.
2. `{SOURCE_PATH}` — the novella unit to extract. **This is your entire world.** (see Isolation, below)
3. Write your extraction to `{OUT_PATH}`. Overwrite if it exists. Follow the schema **exactly**.

If `{HARVEST_PATH}` is given, you also append breadcrumb lines there (see *Harvest sidecar*, below).

### Vocabulary (canonical — you will not see CLAUDE.md, so it is restated here)
- **Pass** = a numbered corpus-wide sweep (you are doing Pass 1). **Track** = a named workstream.
  **step** (lowercase) = an ordered piece of a track. **Tier** = a confidence rating **1–5 only** —
  never a label for work. Do not coin new capitalized terms in your output.

---

### Your role — facts, not interpretation
Extract what the text **states or directly shows**. If the text *implies* something, you may record it
but tag it `(inferred)`. Never theorize, never editorialize, never guess at foreshadowing — that is
Pass 4/5/6 work. **The one inviolable rule: never invent a fact that is not in this unit's text.**
Capturing too much *real* detail is good; inventing *one* detail is a defect.

### Be expansive — GRRM hides things in the mundane
Food, heraldry, weather, architecture, clothing, a throwaway line about hair colour, the order people
sit at a table — these are where Chekhov's guns hide. If it is in the text, log it. A three-sentence
meal description earns a full Food & Drink row. This is **D&E**, where the whole mystery engine is
small concrete details (a shaved head, a pull from a dragon's egg, a borrowed shield) — under-capturing
here is the costliest possible error. **Because there are only three novellas, you have room to be
slower and more thorough than a normal chapter pass. Use it.**

### Chapter Isolation — CRITICAL (this is where early passes failed)
**Treat this unit as if no other text exists** — not other novellas, not the five main books, not your
own broad ASOIAF knowledge.
- Do NOT cite other chapters/books/novellas to frame what this unit reveals.
- Do NOT flag "dramatic irony" or "the reader knows from elsewhere." If a character believes X and you
  *know* X is false from the wider saga, record only that the character believes X.
- The `Known To (Reader Only?)` column means: revealed to the reader *within this unit* vs. known to
  characters *within this unit* — NOT what a reader has learned elsewhere.
- If you catch yourself typing "this foreshadows…", "later we learn…", "the reader knows…" — **stop and
  delete it.** That is not Pass 1.

> **The one allowed exception — IN-TEXT identity reveals.** D&E runs on concealed identity. When the
> text *itself* introduces a character under one name and *then reveals within this same unit* who they
> truly are (the classic: the bald stableboy "Egg" is revealed in-text to be Aegon Targaryen; "the old
> man" is named Ser Arlan of Pennytree), capture **both** the alias and the revealed identity, and
> record the alias→identity link in `## Relationships Observed` with the controlled type `SAME_AS`
> (or `ALIAS_OF` / `IMPERSONATES` if the text fits those better — see the LOCKED vocabulary section) and
> the verbatim in-text evidence. This is NOT outside knowledge — it is
> a reveal the text performs on the page. If the text never reveals the true identity, record only the
> alias. (Cross-identity matching is a first-class use case for this graph — memory
> `user_asoiaf_design_values`.)

### Confidence tier convention
Everything you extract is **Tier 1 (verified canon)** by default — no per-row tier tags. Only two
markers ever appear: `(inferred)` for a strong-but-unstated implication, and `(uncertain — verify)`
for a first-appearance you are unsure about. Nothing else gets a tier annotation.

### Direwolves and dragons are CHARACTERS
Any animal with individual identity and narrative agency is a character, not a creature. For D&E this
matters less than the main saga, but watch for it (named horses with real narrative weight — Thunder,
Chestnut, Sweetfoot — are *objects/mounts*, NOT characters, unless the text gives them genuine agency;
use judgment, and when a named mount is plot-load-bearing, log it under Artifacts & Objects).

### first_available (spoiler gating) — DO NOT REASON IT OUT
Copy the `first_available` value from the unit's YAML frontmatter verbatim (D&E units carry
`first_available: pre-agot`). Do **not** infer or compute a value — that field has a known parser-bug
history and is being backfilled deterministically later. Just mirror the frontmatter.

---

## "More room" — three things you do that a normal chapter pass skips

1. **Section-checkpoint as you go.** A D&E unit is long. Work the text front-to-back in narrative
   segments; after each segment, make sure every table that segment touched is updated *before* moving
   on. The classic long-generation failure is rich early tables and skeletal late ones — defeat it by
   not deferring any table to the end.
2. **Verbatim quotes for the cite-locator.** For `## Dialogue of Note` and for any load-bearing claim,
   record a **short verbatim quote string exactly as it appears** (a clause is enough). **Do NOT write
   line numbers** — a downstream deterministic locator finds them; hand-authored locators caused a real
   bug class. Your job is a clean, *findable*, verbatim string. (Memory
   `feedback_capture_quotes_during_research`: any load-bearing quote you pass over gets attached.)
3. **Final self-audit before you finish.** After writing, re-read your own output once against this
   checklist and fix gaps:
   - All 12 `### Raw Entity List` headers present, in order, each with entries or the literal word
     `None`.
   - No table cell contains meta-commentary (explaining your *choice* instead of stating a *fact*).
   - `## Relationships Observed` Column A is the **semantic agent**, never the grammatical subject and
     never the POV character (see Head rule below).
   - No cross-unit / outside-knowledge leakage anywhere.
   - Every concealed-identity reveal the text performed is captured as a `same_as` relationship.

---

## Harvest sidecar — drop breadcrumbs, do NOT analyze (only if `{HARVEST_PATH}` is given)

While you read, you will notice things that are **real and saga-important but do not belong in this
unit's factual inventory** — most importantly **Bloodraven / Brynden Rivers** material (D&E is the
designated evidence substrate for the Bloodraven enrichment work — memory
`project_bloodraven_enrichment_dip`), Targaryen-history hooks, and Targaryen-prophecy seeds. You do
**not** extract or interpret these (that would violate isolation). You **point** at them for a later
harvest pass, one line each, appended to `{HARVEST_PATH}`:

```
THK / <short verbatim anchor> / bloodraven / Brynden Rivers named as Hand; "..." — one-line note
```

Format per line: `{BOOK} / {short verbatim anchor} / {kind} / {one-line note}`. `kind` ∈
{`bloodraven`, `targaryen-history`, `prophecy`, `food`, `description`, `hospitality`, `cross-identity`,
`foreshadow-hook`, `causal-spine`, `other`}. **Point, don't extract.** If `{HARVEST_PATH}` is not
provided, skip this section entirely. Do not let harvesting bleed analytical commentary back into the
extraction tables.

> **`causal-spine` — the within-novella cause→effect chain.** A D&E novella is self-contained, so its
> local causal spine is visible (e.g. *Dunk strikes Aerion → Dunk is arrested → a trial of seven is
> called → Baelor dies in it*). Drop these as `causal-spine` pointers — `<event A> → <event B>`, one per
> link. **Do NOT assert them as graph edges and do NOT type them** `CAUSES`/`TRIGGERS`/etc. — causal
> typing is a separate arc-mint pass that independently fresh-verifies every link (the agency-collapse
> and CAUSES-vs-ENABLES calls are too load-bearing to make inline). You are *pointing* at the spine for
> that pass; the per-event `Outcome`/`Instigator` slots already hold the mechanical proximate cause.

---

## Controlled relationship vocabulary — LOCKED (the big v4 change; supersedes the old free-text habit)

Earlier passes wrote the `## Relationships Observed` Relationship column in free text, which produced
invented pseudo-labels (`implicit_hostility`, `bonded to`, `contempt toward` — dozens of synonyms for
the same thing). That free-text approach predates the controlled vocabulary. **It is now locked.** The
project's master edge vocabulary is the single source of truth for *every* emitter, the Pass-1 extractor
included — and a deterministic normalizer + vocab-gap tooling runs downstream, so a clean controlled
label here is strictly better than a free-text one a later stage has to re-guess.

**RULE: the Relationship column MUST be exactly one UPPER_CASE type from the character-to-character set
below.** Not a sentence, not a synonym, not a snake_case invention. Read `{ARCH_PATH}` "Edge Types
(Relationship Categories)" for each type's precise meaning and directionality — but the closed set you
choose from is right here:

- **Kinship:** `PARENT_OF` `SIBLING_OF` `SPOUSE_OF` `BETROTHED_TO` `LOVER_OF` `WARD_OF` `ANCESTOR_OF`
  `HEIR_TO` `MARRIES_OFF` `UNCLE_OF` `COUSIN_OF` `MILK_BROTHER_OF` `NURSED_BY`
  `COURTS` `PROPOSED_AS_BRIDE` `STEP_PARENT_OF` `IN_LAW_OF`
- **Authority & service:** `RULES` `OVERLORD_OF` `SWORN_TO` `COMMANDS` `SERVES` `ADVISES` `SUCCEEDS`
  `CLAIMS` `APPOINTS` `DEPOSES` `VOWS_TO` `BREAKS_VOW` `BANISHES`
- **Factional & diplomatic:** `MEMBER_OF` `ALLIES_WITH` `OPPOSES` `MANIPULATES` `BETRAYS`
  `NEGOTIATES_WITH` `CONTRACTED_WITH` `CONSPIRES_WITH`
- **Conflict (person↔person):** `KILLS` `EXECUTES` `CAPTURES` `PRISONER_OF` `DEFEATS` `DUELS` `POISONS`
  `RANSOMS` `IMPRISONS` `GUARDS` `ATTACKS` `ASSAULTS` `KNIGHTED_BY` `RESCUES` `TORTURES`
- **Knowledge & information:** `REVEALS_TO` `DECEIVES` `INVESTIGATES` `TEACHES` `TUTORS` `HEALS` `SEEKS`
  `IGNORANT_OF` `SPIES_ON` `INFORMS`
- **Emotional & perceptual:** `PERCEIVED_AS` `TRUSTS` `DISTRUSTS` `RESPECTS` `FEARS` `LOVES` `HATES`
  `MOURNS` `PROTECTS` `RESENTS` `COMPANION_OF` `REPUTED_AS` `ENCOUNTERS`
- **Identity & disguise:** `ALIAS_OF` `DISGUISED_AS` `SAME_AS` `IMPERSONATES`
- **Cultural & magic (person-centric):** `WORSHIPS` `CLERGY_OF` `WARGS_INTO` `BONDED_TO` `SACRIFICES`
  `RESURRECTS` `CURSES` `NAMED_AFTER`

**Required qualifier (append in parentheses).** Seven of these types MUST carry a qualifier enum value —
`SIBLING_OF` (`full`/`half`/`step`/`milk`), `SPOUSE_OF` (`current`/`former`/`annulled`/`widowed`/`salt_wife`),
`PARENT_OF` (`biological`/`adopted`/`claimed`/`rumored`/`disputed`), `WARD_OF` (`formal`/`informal`/`hostage`),
`VOWS_TO` (`active`/`kept`/`broken`/`fulfilled`), `MANIPULATES` (`via_bribe`/`via_flattery`/`via_false_information`/`via_threat`/`via_seduction`),
`SWORN_TO` (`current`/`former`/`deserted`/`by_marriage`/`claimed`). Write it as `SIBLING_OF (half)`,
`WARD_OF (hostage)`, etc. **Optional-qualifier types — actively capture these too** (the method/condition is usually right there
in the text and carries real narrative signal; use `unknown` only when genuinely indeterminate, and only
the bare type if the relationship has no qualifier dimension):
  - `KILLS` → `in_combat`/`in_duel`/`by_arrow`/`by_blade`/`by_ambush`/`by_proxy`/`by_creature`
  - `ATTACKS` → `in_anger`/`unprovoked`/`in_self_defense`/`on_command`/`by_creature`
  - `DECEIVES` → `by_lie`/`by_disguise`/`by_omission`/`by_false_witness`/`by_silence`
  - `REVEALS_TO` → `voluntary`/`coerced`/`accidental`/`under_torture`
  - `LOVER_OF` → `current`/`former`/`secret`/`paramour`/`rumored`
  - `BETROTHED_TO` → `current`/`broken`/`fulfilled`/`secret`
  - `CONTRACTED_WITH` → `assassination`/`mercenary_service`/`ransom`/`safe_passage`/`construction`/`marriage_brokerage`/`espionage`
  - `IN_LAW_OF` → `by_marriage_of_self`/`by_marriage_of_child`/`by_marriage_of_sibling`/`by_marriage_of_parent`

Write the same way: `KILLS (by_ambush)`, `DECEIVES (by_disguise)`, `LOVER_OF (paramour)`. Full enums +
edge cases: `reference/edge-qualifier-vocab.md`. (This
`(qualifier)` parenthetical is the ONE sanctioned exception to the no-parentheticals rule — it is
structured data, not editorial commentary.)

**Forward direction only — never emit an inverse.** The graph derives every reverse relationship by
traversal (`KILLS`⇒killed-by, `PARENT_OF`⇒child-of, `UNCLE_OF`⇒nephew-of, `DECEIVES`⇒deceived-by). So
emit each fact ONCE, in the direction where **Column A is the semantic agent** (the Head rule): the
killer, the parent, the uncle, the deceiver. Do NOT emit a row and its mirror, and do NOT reach for a
reverse-named type — they are excluded from the set above on purpose. Genuinely **symmetric** types
(`SIBLING_OF`, `SPOUSE_OF`, `COUSIN_OF`, `ALLIES_WITH`, `OPPOSES`, `CONSPIRES_WITH`, `SAME_AS`, …) emit
once in either order.

**Two hard exclusions (these are what keep Pass 1 honest):**
1. **`KNOWS` is DEPRECATED — never emit it.** "X knows Y" is not a relationship here; character knowledge
   is captured in `## Information Revealed` instead.
2. **Never emit an analytical / cross-text type** — `FORESHADOWS`, `PARALLELS`, `ECHOES`, `CONTRASTS`,
   `SUBVERTS`, `FULFILLS`, `PROPHESIED_BY`, etc. Those are Pass 4/5 work and require knowledge from
   *outside* this unit — emitting one is an isolation violation. Spatial (`LOCATED_AT`, `TRAVELS_TO`),
   possession (`WIELDS`, `OWNS`), title (`HOLDS_TITLE`), and event-role (`AGENT_IN`, `FIGHTS_IN`) types
   also do NOT go in this table — their facts live in the Locations / Artifacts / Events tables.

**Genuine non-fit → flag a vocab gap, do NOT invent.** If a real character-to-character relationship
fits *none* of the types above, write the Relationship cell as `NEEDS_VOCAB: <plain description>` (e.g.
`NEEDS_VOCAB: acts as body-double for`). This routes to the downstream vocab-gap log (where new types
get added — "edge types are cheaper than lost information") instead of polluting the set with a fake one.
Reach for `NEEDS_VOCAB` rarely — the set above covers the vast majority — but never force a bad fit.

---

## OUTPUT SCHEMA — FROZEN (identical to v3; reproduced so you need no other file)

Write to `{OUT_PATH}`:

```markdown
# {Book} — {POV Character} {Chapter Number}

## Chapter Metadata
- **book:** {THK|TSS|TMK}
- **chapter_number:** {from frontmatter}
- **pov_character:** {name}
- **pov_chapter_number:** {e.g., "Dunk I"}
- **first_available:** {copy from frontmatter — do not infer}
- **location_primary:** {main setting}
- **location_secondary:** {other locations}
- **approximate_timeline:** {relative positioning within THIS unit only}
- **time_markers:** {every temporal reference as stated: time of day, days elapsed, seasons, "a fortnight past", etc.}
- **chapter_summary:** {3–5 factual sentences, this unit only}
- **unit_part:** {if this unit is a split part, e.g. "2 of 7"; else "whole"}

## Physical Environment
- **Weather:** …
- **Season indicators:** …
- **Time of day:** …
- **Lighting:** …
- **Sounds:** …
- **Smells:** …
- **Notable sensory details:** …

## Characters Present
| Character | Role in Chapter | First Appearance? | Notes |
|-----------|----------------|-------------------|-------|

## Character Appearances
| Character | Hair | Eyes | Build/Height | Scars/Marks | Clothing/Armor | Weapons Worn | Distinguishing Features | Age (if stated) |
|-----------|------|------|-------------|-------------|----------------|-------------|------------------------|-----------------|

## Characters Referenced
| Character | Context of Reference | Referenced By |
|-----------|---------------------|---------------|

## Locations
| Location | Role | First Appearance? |
|----------|------|-------------------|

## Location Descriptions
| Location | Defensive Features | Architecture/Layout | Interior Details | Scale | Condition | Surrounding Terrain/Geography | Notable Sensory Details |
|----------|--------------------|--------------------|-----------------| ------|-----------|------------------------------|------------------------|

## Artifacts & Objects of Significance
| Artifact | Context | First Appearance? | Current Holder/Location |
|----------|---------|-------------------|------------------------|

## Food & Drink
| Meal/Occasion | Food Items Described | Drink | Who Is Eating/Drinking | Where | Preparation/Presentation Notes |
|--------------|---------------------|-------|----------------------|-------|-------------------------------|

## Hospitality & Guest Right
| Event | Type | Host | Guest(s) | Details |
|-------|------|------|----------|---------|

## Events & Actions
1. **{Event}** — {factual description}
   - Agent: {executor — the one who performed the act}
   - Patient: {recipient/target}
   - Instrument: {artifact/weapon used, if any}
   - Location: {place}
   - Instigator: {orderer/commander, if different from Agent}
   - Witness: {character whose load-bearing perception of a charged event matters — ONLY when the text shows they actually SAW it (present-but-shielded does not count)}
   - Outcome: {brief — "death", "victory", "escape", …}
   (role sub-bullets are OPTIONAL; use when an event has multiple participants. These slots map to the
    graph's reification roles — Agent→AGENT_IN, Patient→VICTIM_IN, Instrument→WIELDED_IN,
    Instigator→COMMANDS_IN, Witness→WITNESS_IN — so capture them cleanly; Stage 4 reifies straight from them.)

## Spatial Layout & Movement
| Phase | Who | Position / Movement | Relative To | Notes |
|-------|-----|---------------------|-------------|-------|
(Phase vocab: Opening, Advance, Retreat, Scout, Ambush, Siege, Assembly, Dispersal, Pursuit,
 Confrontation, Arrival, Departure, Patrol, Concealment. Use when movement matters — e.g. the Trial of Seven.)

## Information Revealed
| Information | How Revealed | Known To (Characters) | Known To (Reader Only?) |
|-------------|-------------|----------------------|------------------------|

## Dialogue of Note
| Speaker | Listener | Quote/Paraphrase | Context |
|---------|----------|------------------|---------|

## POV Character's Internal State
- **Emotional state:**
- **Primary preoccupation:**
- **Key decisions made:**
- **Self-deception flags:**

## Relationships Observed
| Character A | Relationship | Character B | Evidence |
|-------------|-------------|-------------|----------|

## Unanswered Questions
| Question | Raised By | Context |
|----------|-----------|---------|

## Raw Entity List
**You MUST include all 12 category headers below, exactly as written, even if empty. Write "None"
under empty categories. Do not rename, merge, split, or omit any header.**
**Bare names only.** This is a flat index for downstream parsing — list the entity name, nothing else.
No parentheticals except the two sanctioned flags (`(inferred)`, `(uncertain — verify)`). NOT
`War of the Ninepenny Kings (implicit context)`, NOT `Hand of the King (implicit via Lord X)` — just the
name. If something is only implied and not named in the text, either omit it or list the name with
`(inferred)`.

### Characters
### Locations
### Houses
### Factions & Organizations
### Religions & Faiths
### Cultures & Peoples
### Artifacts & Objects
### In-world Texts & Songs
### Magic & Phenomena
### Wars & Conflicts
### Titles & Offices
### Other
```

---

## THE RULES (consolidated — each one is a scar from an early book pass)

1. **Comprehensive & expansive.** Every named entity, every description, meal, weather note, movement.
2. **Factual & accurate.** Record what the text says, not what you think it means. Never invent.
3. **Presence vs mention.** Distinguish `active/present` from `mentioned/recalled`.
4. **Track first appearances.** Flag `(uncertain — verify)` when unsure.
5. **Dramatic irony is NOT your concern.** No "reader knows from elsewhere." Scoped to this unit.
6. **Don't skip boring details.** The meal, the hair colour, the sigil — that is where the guns hide.
7. **Summaries factual & brief.** 3–5 sentences, no literary analysis.
8. **One unit per extraction.** No cross-unit references — later passes connect them.
9. **No meta-commentary in tables — and no interpretive qualifiers.** Cells hold *facts*. Never use a
   cell to explain your extraction choice ("symbolic weight is implicit…", "shows unease but not
   stated…"). If you cannot state a clean fact, leave the cell empty.
   **Evidence-driven ban (this is the #1 recurring defect in the 5-book passes).** Do NOT write these
   editorial words anywhere in a table cell, an Events entry, or the Raw Entity List:
   `symbolic` · `ironic` / `bitterly ironic` · `foreshadows` · `represents` / `representing` ·
   `thematically` · `narrative weight` · `(implicit)` / `(implicitly)`. They are interpretation, not
   extraction. Examples of the leak to avoid: `blood oranges (pervasive symbolic object)` → just
   `blood oranges`; `Iron Throne — symbolic center of power struggle` → `Iron Throne`; a "Context" cell
   reading `bitter/ironic final line` → state what was said, not how it lands. The only sanctioned
   parentheticals are `(inferred)`, `(uncertain — verify)`, and — in the Relationship column only — a
   controlled `(qualifier-enum)` value (see the LOCKED vocabulary section). Nothing else in parentheses.
10. **Direwolves/dragons are characters; plot-mounts are objects.** (See note above.)
11. **HEAD RULE — `## Relationships Observed`.** Column A is **always the semantic agent**, never the
    grammatical subject of the source sentence and never the POV character. Passive ("X was killed by
    Y") → Y in Column A. Ordered acts ("Lord Z had the knight strike X") → the EXECUTOR (knight) in
    Column A; the orderer (Z) goes in the Events & Actions Instigator slot, not Column A. Surface syntax
    must never leak into the data model — the same event is phrased a dozen ways. **The Relationship
    column is a LOCKED controlled type** (see the LOCKED vocabulary section), never free text.
12. **In-text identity reveals → `SAME_AS`** (D&E exception above). Capture alias and true name both.
13. **Self-audit before finishing** (the 5-point checklist under "More room").

═══════════════════════════════════════════════════════════════════════════════

## Appendix — what changed from v3 (for Matt's review; NOT sent to the model)

| # | Change | Why / source |
|---|--------|--------------|
| 1 | Self-contained vocab + isolation + never-invent (no reliance on CLAUDE.md/architecture being in context) | `claude -p` cwd=/tmp loads none of it (`reference_llm_pass_via_claude_p`) |
| 2 | Harvest sidecar instruction (Bloodraven/Targaryen/prophecy breadcrumbs) | `feedback_harvest_queue` + `project_bloodraven_enrichment_dip` — CLAUDE.md rule the model never sees |
| 3 | Verbatim-quote capture for cite-locator; **explicit "do NOT hand-author line numbers"** | `feedback_capture_quotes_during_research` + the `:11` locator bug class |
| 4 | IN-TEXT identity-reveal exception → `same_as` (Egg→Aegon, the old man→Ser Arlan) | D&E concealed-identity engine; `user_asoiaf_design_values` cross-identity use case |
| 5 | `first_available` = copy frontmatter, do NOT infer | known parser-bug class; field is deferred |
| 6 | "More room" block: section-checkpointing + final self-audit | counters the long-generation skimped-late-tables failure (a 32K-word unit is ~8× a chapter) |
| 7 | Head rule + no-meta-commentary promoted to numbered, front-loaded rules | were reactive patches in v3, easy to miss |
| 8 | `unit_part` metadata line | supports the split-into-parts option (harmless "whole" if not split) |
| 9 | Named-mount disambiguation (Thunder/Chestnut = objects, not characters) | avoids over-promoting D&E's many horses to character nodes |
| 10 | **Evidence-driven:** banned-qualifier list (`symbolic`/`ironic`/`foreshadows`/`represents`/`(implicit)`) in rule 9 + "bare names only" on the Raw Entity List | a real audit of the 5-book extractions: this qualifier-leak is the #1 recurring rule-9 defect (e.g. `blood oranges (pervasive symbolic object)`). Isolation, by contrast, audited clean — so no extra isolation rules added |
| 11 | **LOCKED relationship vocabulary** — Relationship column MUST be one controlled UPPER_CASE type from the curated character-to-character set; free text banned | folds in the post-pass infrastructure (the controlled edge vocab + normalizers + vocab-gap tooling). `architecture.md:687` already names the Pass-1 extractor a vocab emitter; the free-text `:161` note is the stale fossil (predates the vocab). Models follow a hard closed-set far better than "prefer these" (Matt) |
| 12 | **`NEEDS_VOCAB:` gap-hatch + required & deepened optional-qualifier capture + `KNOWS` ban + analytical-type ban** | honors `architecture.md:159` ("edge types cheaper than lost info") so forcing never drops a real relation; pre-loads all 7 required + 8 optional qualifier enums (the optional ones — `KILLS (by_ambush)`, `DECEIVES (by_disguise)`, `REVEALS_TO (under_torture)` — are high D&E signal and text-evident); `KNOWS` deprecated S63; banning `FORESHADOWS`/`PARALLELS`/etc. keeps the vocab-forcing from re-opening the isolation hole |
| 13 | **Events sub-bullets aligned to reification roles** (added `Witness`; Agent→AGENT_IN … Witness→WITNESS_IN) | the S82–87 reification + S117 `WITNESS_IN` work — Stage 4 reifies event hubs straight from these slots |
| 14 | **Forward-direction-only rule** + pruned reverse types (`NEPHEW_OF`/`STEP_CHILD_OF`/`WET_NURSE_OF` removed) | inverse-edge knowledge applied correctly: the graph derives reverses by traversal, so emit once in the agent direction. *Shrinks* the prompt, prevents double-emission, reinforces the Head rule |
| 15 | **`causal-spine` harvest breadcrumb** (point at within-novella cause→effect; do NOT type or assert) | feeds the arc-mint pass (which fresh-verifies every causal link) without making unverified causal claims inline. **Deliberately NOT included:** causal-edge emission, convergence-points, narrative-arcs — graph-layer / multi-event / cross-book constructs invisible under chapter-isolation; the arc machine owns them post-hoc |

**Table structure is byte-identical to v3** — no new/renamed tables or categories, so no downstream
parser change. **The one paired change (rule #6):** locking the Relationship column realigns to
`architecture.md:687` and **supersedes the stale `:161` free-text note**, which must be corrected when
v4 ships (a doc-correctness fix; tracked as an Active Decision in the run-plan).
