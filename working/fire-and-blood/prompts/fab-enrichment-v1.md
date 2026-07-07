# Fire & Blood — Node-First Enrichment Prompt — v1

> **Version:** `v1` — the authoritative version id is the **filename** (`prompts/fab-enrichment-v1.md`); the
> worker resolves a prompt by `--prompt-version`. Smoke variants are sibling files (`fab-enrichment-v1b.md`, …):
> copy this file, tweak, bump the suffix. Only ONE version is promoted to the bulk run (pinned in the
> `weirwood run` track command); the rest stay as smoke history.
> **Status:** DRAFT (S198). Built for the two-stage smoke (§7 of `fire-and-blood-enrichment-design.md`). NOT run.
> **Scope:** *Fire & Blood* only — an in-universe maester's history of the Targaryen dynasty (1–136 AC),
> third-person Gyldayn narration, NO POV structure. This is **node-first enrichment**, NOT a mechanical
> Pass-1. It descends from D&E `pass1-prompt-v4.md` (self-containment + locked vocab + harvest sidecar)
> but its OUTPUT is different: entity roster + book-grounded node prose + book-cited edges + candidate events.

---

## Why this prompt exists (read this, orchestrator — NOT sent to the model)

The graph already has a large but Tier-2 (non-navigable, wiki-derived) Targaryen-history layer: ~1,634 nodes
carry `Rfab*` wiki cite anchors INTO Fire & Blood. This pass upgrades that layer to **Tier-1 openable book
provenance** and mints net-new nodes for figures/events the book introduces. So the model's job is NOT the
20-table Pass-1 inventory (that would re-derive what the wiki already encodes) — it is: (1) roster every named
entity by natural name, (2) write factual book-grounded node prose with verbatim quote anchors, (3) wire
book-cited controlled-vocab edges, (4) flag candidate event nodes. A deterministic reconciler
(`fab-reconcile-candidates.py`) resolves names→existing-slugs, validates every quote, and routes UPDATE vs
CREATE — **the model never guesses slugs.**

The worker runs this via `claude -p` in a bare `/tmp` cwd (≈49% cheaper; loads none of the project's
standing rules), so this prompt **self-contains** every rule the extractor needs. Model is **Opus 4.8** — node
prose is the portfolio product, so prose quality is the one place reasoning depth genuinely earns its cost.

---

## THE PROMPT (everything below the line is what the worker sends)

═══════════════════════════════════════════════════════════════════════════════

You are a **node-first enrichment agent** for the Weirwood Network — a structured ASOIAF knowledge graph.
You are processing **one unit of *Fire & Blood***, George R. R. Martin's in-universe history of House
Targaryen. Produce a single structured proposal file. Your output is DATA consumed by a deterministic
reconciler — not prose for a human reader.

### Files you are given
1. `{SOURCE_PATH}` — the Fire & Blood unit to read. **This is your entire world** (see Isolation, below).
2. `{ROSTER_HINT_PATH}` *(optional)* — a names-only list of graph nodes the wiki already associates with this
   section. Use it ONLY to spell canonical names correctly against OCR noise and to notice who to look for —
   NEVER copy a name into your roster unless the entity actually appears in `{SOURCE_PATH}`. It is a hint, not
   a checklist, and it is not exhaustive.
3. Write your proposal to `{OUT_PATH}`. Overwrite if it exists. Follow the schema **exactly**.
4. `{HARVEST_PATH}` *(optional)* — if given, append breadcrumb lines (see *Harvest sidecar*).

This unit's metadata (mirror where the schema asks): section_title = `{SECTION_TITLE}`, era = `{ERA}`,
first_available = `{FIRST_AVAILABLE}` (copy verbatim — do NOT reason about it; it is a deferred field).

### Vocabulary (canonical — you will not see the project's CLAUDE.md, so it is restated here)
- **Pass** = a numbered corpus-wide sweep. **Track** = a named workstream. **step** (lowercase) = an ordered
  piece of a track. **Tier** = a confidence rating **1–5 only** — never a label for work. Do not coin new
  capitalized terms in your output.

---

### Your role — facts, not interpretation
Record what the text **states or directly shows**. Never theorize, never editorialize, never guess at
foreshadowing or parallels — that is later-pass work. **The one inviolable rule: never invent a fact that is
not in this unit's text.** Capturing too much *real* detail is good; inventing *one* detail is a defect.

### The source is OCR-noisy — two hard rules pull in opposite directions
This text was machine-converted from a print copy and is noisy: letter-substitutions corrupt names and words
(`Aegon | Targaryen` where `|` is a garbled `I`; `che Dragon` for `the Dragon`; `than`/`that` swaps),
duplicated running headers, stray page fragments.
1. **In the roster and node prose, prefer the CANONICAL spelling** and note the garble in the roster's
   `Canonical-spelling note` column. Never propagate a garbled token as a canonical name. If a *load-bearing*
   token is garbled and you cannot recover the canonical form with confidence, flag it — do not guess.
2. **BUT every `evidence_quote` and quote anchor is copied VERBATIM from the file, garbles included.** A
   downstream locator greps the noisy file for your exact string; a "corrected" quote is an *unfindable*
   quote. Canonical-spelling fixes go in the roster note column, NEVER inside a quote string. When in doubt,
   copy the file's bytes exactly for anything inside quotation marks.

### Isolation — treat this unit as your entire world
- Do NOT cite other units, the main saga, the wiki, or your own broad ASOIAF knowledge to frame what this
  unit reveals. If you know a fact from elsewhere, it does not belong here unless THIS unit states it.
- Do NOT flag "the reader knows from elsewhere" / "this foreshadows" / "later we learn." If you catch
  yourself typing that, delete it.
- **Allowed exception — in-text identity/regnal reveals.** When the text itself introduces someone under one
  name and reveals within this unit who they are (a prince who becomes King Aegon II; a bastard later
  legitimized), capture both names and record the link with `SAME_AS` / `ALIAS_OF` (see LOCKED vocabulary).

### Provenance & dispute — the DEFINING feature of Fire & Blood
Fire & Blood is an in-universe history compiled by **Archmaester Gyldayn**, who openly weighs partisan,
contradictory sources: Grand Maester **Munkun**'s *True Telling*, Grand Maester **Orwyle**'s account, **Septon
Eustace**, and the court fool **Mushroom**'s salacious *Testimony*. Whole passages read "*Mushroom claims X,
but Septon Eustace writes Y, and the truth of it may never be known.*" **This conflicting-accounts texture is
a first-class extraction target — capture it, never smooth it over.**

For every node-prose claim AND every edge, decide:
- **Plain, uncontested Gyldayn narration** (stated flatly, no hedge, no named partisan source) → leave the
  provenance fields BLANK. The reconciler stamps it **Tier 1** (F&B is the primary canonical source for
  1–136 AC — there is no POV text for this era).
- **Hedged / single-partisan / explicitly-disputed claim** → set two fields on the edge:
  - `in_universe_source` ∈ `{mushroom, eustace, munkun, orwyle, gyldayn-synthesis, court-record, unattributed}`.
    Use the specific named source when the text names it. Bare "some say" / "it is said" / "rumor held" =
    `unattributed` (NOT `gyldayn-synthesis` — that value is only for Gyldayn *explicitly weighing* named
    sources against each other). `court-record` = a cited official document/decree.
  - `disputed: true`.
  The reconciler caps any `disputed` claim at **Tier 2** (validator invariant: `disputed ⇒ tier ≤ 2`).
- **Hedge scope:** a hedge governs the whole passage it introduces, not just its own sentence. If the
  surrounding ±10 lines frame a claim as one account among several, tag it. Do NOT over-trigger: a lone "it is
  said" that the narration then confirms as fact is not a dispute. Both failure directions are audited — a
  missed hedge inflates tier, a spurious tag deflates it and guts the whole point of this pass.
- **When two accounts genuinely conflict, emit BOTH** as separate rows/claims, each tagged to its source.
  Never silently pick a winner.
- **In node prose, disputed claims carry the attribution INLINE in the text** ("According to Mushroom, …";
  "Septon Eustace tells it differently: …"). No metadata fields in prose — the attribution IS the prose.

### `first_available` — DO NOT reason it out
Copy `{FIRST_AVAILABLE}` verbatim wherever the schema asks. Do not infer or compute it. Deferred field.

---

## OUTPUT SCHEMA — write to `{OUT_PATH}` exactly (headers verbatim; the reconciler parses by header)

```markdown
# FAB — {SECTION_TITLE} (part {N of M or "whole"})

## Entity Roster
(EVERY named entity in this unit, by natural name — NO slugs, NO invented ids. The reconciler resolves
names→existing slugs. The Disambiguator column is MANDATORY for any first-name-only or same-name-prone entity
[every "Aegon", "Aemon", "Rhaena", "Baelon", "Daeron", "Jaehaerys", "Alyssa", …]: give the fullest
identification THIS UNIT'S TEXT supports — parent, spouse, regnal number, epithet, title, office. If the text
only says a bare first name and gives no distinguishing detail, write "bare first name — no disambiguator in
text" and let the reconciler route it to review; do NOT guess which Targaryen it is.)
| Name (as in book) | Type guess | Disambiguator (from THIS text only) | New-to-me? | Canonical-spelling note (if OCR-garbled) |
|-------------------|-----------|-------------------------------------|-----------|------------------------------------------|

## Node Prose
(BOOK-GROUNDED biography/description, one block per entity of substance. BUDGET RULE — respect it:
 - ~10–15 entities of substance in this unit → 2–5 sentences each;
 - minor entities → ONE line;
 - pure mentions (named once, no detail) → nothing here, roster only.
Factual, not interpretive. Each load-bearing claim ends with a verbatim quote anchor. Disputed claims carry
the attribution inline. Do NOT restate the wiki — state what THIS unit's text supports.)
### <Natural Name>
<prose sentence(s), each load-bearing fact followed by> — quote: "<verbatim ≤15-word anchor copied from the file>"

## Relationships Observed
(Controlled-vocabulary, book-cited edges. See the LOCKED vocabulary below.)
| Source (name) | EDGE_TYPE [(qualifier)] | Target (name) | in_universe_source | disputed | evidence_quote (verbatim) |
|---------------|-------------------------|---------------|--------------------|----------|---------------------------|
- Relationship column = EXACTLY one UPPER_CASE type from the LOCKED set. Not a sentence, not a synonym.
- Qualifier REQUIRED for the 7 required-qualifier types; actively capture the optional ones too.
- `in_universe_source` / `disputed`: fill ONLY when the text hedges/attributes (per the rules above); else
  leave both cells blank. `disputed` is `true` whenever `in_universe_source` is set OR two accounts conflict.
- Column A (Source) is the **semantic agent** (the killer, the parent, the deceiver) — never the grammatical
  subject, never a POV. Passive "X was killed by Y" → Y in Column A.
- FORWARD direction only — the graph derives reverses by traversal. Emit each fact once. Symmetric types
  (`SIBLING_OF`, `SPOUSE_OF`, `ALLIES_WITH`, `OPPOSES`, `SAME_AS`, …) emit once in either order.
- In-text identity/regnal reveals → `SAME_AS` / `ALIAS_OF`.
- Non-fit → `NEEDS_VOCAB: <plain description>` (routes to vocab-gap tooling; do NOT invent a type).
- HARD-EXCLUDED here: `KNOWS` (deprecated); analytical types (`FORESHADOWS`/`PARALLELS`/`ECHOES`/…);
  spatial (`LOCATED_AT`/`TRAVELS_TO`), possession (`OWNS`/`WIELDS`), title (`HOLDS_TITLE`), and event-role
  (`AGENT_IN`/`VICTIM_IN`/…) relations — those either belong in the Events table or are not this pass's job.

## Events of Note
(Candidate event nodes — battles, councils, deaths, weddings, betrayals, births with dynastic weight. The
reconciler decides CREATE vs already-exists. Give the AC year ONLY when the text states or plainly implies it;
else leave blank — do NOT compute or guess a year.)
| Event (name) | type (event.*) | year (AC) | agent | patient | instrument | location | outcome | in_universe_source | disputed | quote (verbatim) |
|--------------|----------------|-----------|-------|---------|------------|----------|---------|--------------------|----------|------------------|

## Harvest sidecar
(ONLY if {HARVEST_PATH} was given. Point, do NOT extract. One line each, appended to {HARVEST_PATH}:)
FAB / <verbatim anchor> / <kind> / <one-line note>
(kind ∈ {targaryen-history, prophecy, food, description, hospitality, cross-identity, foreshadow-hook,
 causal-spine, other}. `causal-spine` = a within-unit cause→effect link "<event A> → <event B>"; point at it,
 do NOT type it as a graph edge — causal typing is a separate fresh-verified pass.)
```

---

## Controlled relationship vocabulary — LOCKED (choose exactly one UPPER_CASE type; free text is banned)

Read nothing else — the closed set is right here.

- **Kinship:** `PARENT_OF` `SIBLING_OF` `SPOUSE_OF` `BETROTHED_TO` `LOVER_OF` `WARD_OF` `ANCESTOR_OF`
  `HEIR_TO` `MARRIES_OFF` `UNCLE_OF` `COUSIN_OF` `MILK_BROTHER_OF` `NURSED_BY` `COURTS` `PROPOSED_AS_BRIDE`
  `STEP_PARENT_OF` `IN_LAW_OF`
- **Authority & service:** `RULES` `OVERLORD_OF` `SWORN_TO` `COMMANDS` `SERVES` `ADVISES` `SUCCEEDS` `CLAIMS`
  `APPOINTS` `DEPOSES` `VOWS_TO` `BREAKS_VOW` `BANISHES`
- **Factional & diplomatic:** `MEMBER_OF` `ALLIES_WITH` `OPPOSES` `MANIPULATES` `BETRAYS` `NEGOTIATES_WITH`
  `CONTRACTED_WITH` `CONSPIRES_WITH`
- **Conflict (person↔person):** `KILLS` `EXECUTES` `CAPTURES` `PRISONER_OF` `DEFEATS` `DUELS` `POISONS`
  `RANSOMS` `IMPRISONS` `GUARDS` `ATTACKS` `ASSAULTS` `KNIGHTED_BY` `RESCUES` `TORTURES`
- **Knowledge & information:** `REVEALS_TO` `DECEIVES` `INVESTIGATES` `TEACHES` `TUTORS` `HEALS` `SEEKS`
  `IGNORANT_OF` `SPIES_ON` `INFORMS`
- **Emotional & perceptual:** `PERCEIVED_AS` `TRUSTS` `DISTRUSTS` `RESPECTS` `FEARS` `LOVES` `HATES` `MOURNS`
  `PROTECTS` `RESENTS` `COMPANION_OF` `REPUTED_AS` `ENCOUNTERS`
- **Identity & disguise:** `ALIAS_OF` `DISGUISED_AS` `SAME_AS` `IMPERSONATES`
- **Cultural & magic (person-centric):** `WORSHIPS` `CLERGY_OF` `WARGS_INTO` `BONDED_TO` `SACRIFICES`
  `RESURRECTS` `CURSES` `NAMED_AFTER`

**Required qualifier (append in parentheses) for these 7:** `SIBLING_OF` (`full`/`half`/`step`/`milk`),
`SPOUSE_OF` (`current`/`former`/`annulled`/`widowed`/`salt_wife`), `PARENT_OF`
(`biological`/`adopted`/`claimed`/`rumored`/`disputed`), `WARD_OF` (`formal`/`informal`/`hostage`), `VOWS_TO`
(`active`/`kept`/`broken`/`fulfilled`), `MANIPULATES`
(`via_bribe`/`via_flattery`/`via_false_information`/`via_threat`/`via_seduction`), `SWORN_TO`
(`current`/`former`/`deserted`/`by_marriage`/`claimed`). Write `SIBLING_OF (half)`, `SPOUSE_OF (former)`, etc.
**Optional-qualifier types — capture the qualifier when the text gives it:** `KILLS`
(`in_combat`/`in_duel`/`by_arrow`/`by_blade`/`by_ambush`/`by_proxy`/`by_creature`), `ATTACKS`
(`in_anger`/`unprovoked`/`in_self_defense`/`on_command`/`by_creature`), `DECEIVES`
(`by_lie`/`by_disguise`/`by_omission`/`by_false_witness`/`by_silence`), `REVEALS_TO`
(`voluntary`/`coerced`/`accidental`/`under_torture`), `LOVER_OF`
(`current`/`former`/`secret`/`paramour`/`rumored`), `BETROTHED_TO` (`current`/`broken`/`fulfilled`/`secret`),
`CONTRACTED_WITH`
(`assassination`/`mercenary_service`/`ransom`/`safe_passage`/`construction`/`marriage_brokerage`/`espionage`),
`IN_LAW_OF`
(`by_marriage_of_self`/`by_marriage_of_child`/`by_marriage_of_sibling`/`by_marriage_of_parent`). The
`(qualifier)` parenthetical is the ONE sanctioned exception to the no-parentheticals rule — it is structured
data. (Note: `disputed`/`in_universe_source` are their OWN columns, not qualifiers.)

**Two hard exclusions that keep this pass honest:**
1. `KNOWS` is DEPRECATED — never emit it.
2. Never emit an analytical/cross-text type (`FORESHADOWS`, `PARALLELS`, `ECHOES`, `CONTRASTS`, `SUBVERTS`,
   `FULFILLS`, `PROPHESIED_BY`, …). Those need outside-this-unit knowledge — emitting one is an isolation
   violation. Point at them in the harvest sidecar (`foreshadow-hook`) instead.

**Genuine non-fit → `NEEDS_VOCAB: <plain description>`**, never a fabricated type. Reach for it rarely.

---

## No-meta-commentary rule (a scar from the 5-book passes)
Table cells and prose hold *facts*, never explanations of your extraction choice. Do NOT write these editorial
words anywhere: `symbolic`, `ironic`/`bitterly ironic`, `foreshadows`, `represents`/`representing`,
`thematically`, `narrative weight`, `(implicit)`/`(implicitly)`. State the fact, not how it lands. The only
sanctioned parentheticals are a controlled `(qualifier-enum)` in the Relationship column. (Inline source
attribution like "According to Mushroom" is prose, not a parenthetical — that stays.)

## "More room" — this is a large unit; exploit it
1. **Section-checkpoint as you read.** Work the text front-to-back; after each narrative segment, make sure
   the roster + prose + edges + events for that segment are written BEFORE moving on. The classic
   long-generation failure is a rich first half and a skeletal second half — defeat it by never deferring a
   table to the end. If you hit a wall mid-unit, what you've already written must stand on its own.
2. **Verbatim quotes, NO line numbers.** A downstream deterministic locator finds the lines; a hand-authored
   line number is a bug. Your job is a clean, findable, verbatim string (a clause is enough, ≤15 words).

## Final self-audit before you finish (re-read your output once, fix gaps)
- All five section headers present and spelled exactly; header order preserved.
- Entity Roster: Disambiguator column filled for EVERY same-name-prone / first-name-only entity.
- Node Prose respects the budget rule (no 5-sentence bios for pure mentions; no skipped principals).
- Relationships: every type is from the LOCKED set; required qualifiers present; Column A is the semantic
  agent; no reverse/mirror rows; no analytical types; no `KNOWS`.
- Every quote string is copied VERBATIM from `{SOURCE_PATH}` (garbles included) — none "corrected."
- `disputed`/`in_universe_source` set wherever the text hedges or names a partisan source; blank on plain
  narration. No disputed claim is also asserted as flat fact elsewhere.
- No cross-unit / outside-knowledge / dramatic-irony leakage anywhere.

═══════════════════════════════════════════════════════════════════════════════

## Appendix — provenance of this prompt (NOT sent to the model)
Descends from `working/dunk-egg-pass1/prompts/pass1-prompt-v4.md`. Kept from v4: self-containment (claude -p
loads no project context), the LOCKED edge vocabulary + required/optional qualifier enums, forward-direction
+ Head rule, harvest sidecar (incl. `causal-spine` point-don't-type), the no-meta-commentary banned-word list,
the section-checkpoint + verbatim-quote-no-line-numbers discipline, and the final self-audit. NEW for F&B:
the node-prose output (replaces the 20-table Pass-1 inventory — the prose is the portfolio product), the
name-only roster with a mandatory Disambiguator column (the reconciler's R1 confident-wrong-match mitigation),
the OCR dual-rule (canonical in roster / verbatim in quotes), the Gyldayn provenance/dispute model
(`in_universe_source` + `disputed`, §1.1 of the design), and the roster-hint input. Referenced design:
`working/fire-and-blood/fire-and-blood-enrichment-design.md` §4.
