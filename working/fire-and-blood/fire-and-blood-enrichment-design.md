# Fire & Blood — Node-First Enrichment Pass — Design Document

> **Version: v2 — post-Fable-review (2026-07-06).** v1 was reviewed by Fable the same day (`working/fire-and-blood/fable-review.md` — read it for the rulings' rationale, ranked risks, and the factual corrections C1–C5). This v2 applies the review: the §11 decisions are RESOLVED (Matt's final go still gates the build), §5 is rewritten around the verified resolver/mint behavior, and new sections cover rollback, contradictions, and observability. **Written to be executable by a cheaper agent** — each component below has inputs, outputs, algorithm, and acceptance criteria.
>
> **Purpose:** a long-running **Opus 4.8** extraction pass over *Fire & Blood* that upgrades the graph's existing (wiki-derived) Targaryen-history layer to Tier-1 book-cited provenance, and mints net-new nodes for figures/events the book introduces.
>
> **Framing decided with Matt (2026-07-06):** *node-first enrichment*, not a full mechanical Pass-1. Confirmed GO-WITH-CHANGES by Fable review. This doc is still **design-only** — no splitter build, no extraction, no graph mutation until Matt's explicit go (`feedback_no_graph_mutation_without_goahead`).
>
> **Motivation:** *House of the Dragon* is airing; people are searching for these characters. The dynasty layer is where book-grounded provenance is thinnest, so this pass has high portfolio value for the chat-UI alpha (`project_real_goal_graph_for_agents`).

---

## §0 — Component status (keep in sync as things ship)

| # | Component | Path (proposed) | Status |
|---|-----------|-----------------|--------|
| 1 | epub → chapter splitter | `scripts/fire-and-blood-splitter.py` | **DESIGN** |
| 2 | Split chapter files | `sources/chapters/fab/` | **DESIGN** |
| 3 | Node-first enrichment prompt | `working/fire-and-blood/prompts/fab-enrichment-v1.md` | **DESIGN** |
| 4 | Long-run worker | `working/fire-and-blood/fire-and-blood-extraction.py` | **DESIGN** |
| 5 | Per-unit candidate packs (deterministic, from `Rfab` anchors) | `scripts/fab-build-candidate-packs.py` → `working/fire-and-blood/candidate-packs/` | **DESIGN — new in v2 (§5.0)** |
| 6 | Name→slug reconciler (UPDATE vs CREATE) + quote pre-validation | `scripts/fab-reconcile-candidates.py` | **DESIGN** |
| 7 | **Node merge writer (UPDATE path — NEW capability, not a mint patch)** | `scripts/fab_merge_node.py` | **DESIGN — new in v2 (§5.3)** |
| 8 | Contradiction diff (F&B vs wiki-infobox edges) | part of reconciler → `working/fire-and-blood/contradictions-report.md` | **DESIGN — new in v2 (§5.4)** |
| 9 | Verify / drift gate | reuse fresh-verify subagents + schema validator (extended: dispute-axis strata, §7) | **DESIGN** |
| 10 | Apply (edges + CREATE nodes) | reuse `scripts/mint_enrichment.py` + `finalize_enrichment.py` + `weirwood refresh` | **REUSE** — mint needs only the `book-fab` evidence_kind + `fab` chapter dir; **UPDATE nodes go through #7, never through mint** (mint is skip-if-exists, verified — see §5.3) |
| — | *External dependency:* disambiguation pack | `working/wiki/data/same-name-clusters.json` (built by the **companion track**, `working/node-enrichment-wiki-prose/design.md`) | **DESIGN — companion runs FIRST (§10)** |

Nothing here is built. `README = existence-truth`: this table is the anti-drift gate — flip a row to ✅ only when the artifact exists and is smoke-passed.

---

## §1 — Goal & the key insight

**The dynasty layer already exists — in three shapes, not one.** Most F&B figures already have nodes from Pass 2 wiki ingestion, and **1,634 nodes carry `Rfab*` wiki cite anchors** (the wiki's own citations INTO Fire & Blood), so the graph's F&B footprint is large but its provenance is Tier-2 non-navigable. Verified node shapes (Fable review C2):

- **(a) True stub** — boilerplate `## Identity` (*"X is a character.human from the AWOIAF wiki."*), no other prose. ~2,753 character nodes carry the boilerplate line.
- **(b) Rich wiki node** — boilerplate Identity line **but ~90 lines of real wiki-cited prose below it** (Origins / Appearances / Narrative Arc / Quotes). Example: `graph/nodes/characters/rhaenyra-targaryen.node.md`. The prose is good and its `(wiki:…cite_ref-Rfab…)` anchors ARE the Tier-2 provenance layer — it must be preserved, not replaced.
- **(c) No-Identity node** — no `## Identity` section at all; body starts at `## Origins` with real prose. Example: `aegon-targaryen-son-of-baelon`. (~545 character nodes.)

Every edge on these nodes is wiki-infobox-derived (16,757 `evidence_kind: wiki-infobox` rows in `edges.jsonl`) — Tier-2, non-navigable. So this pass is **~70% UPDATE, ~30% CREATE**:

1. **UPDATE** existing nodes with (a) book-grounded prose (a new `## Fire & Blood` section + Identity-line swap where boilerplate — see §5.3), and (b) **book cite_refs** on facts/edges — upgrading Tier-2 wiki claims to **Tier-1 openable book provenance** (`feedback_book_citation_overlay_value`: *"this is huge"* — do it even when the wiki node already states the fact).
2. **CREATE** nodes for figures/events F&B introduces that never got a wiki stub (minor lords, specific battles/councils, dragons, small events in the Dance, the regency). New mints stamp `era:` (§5.5) and, for events, `occurred.ac_year` where the text dates them.
3. **WIRE** book-cited controlled-vocab edges (kinship, political, military, the Dance's whodunit-adjacent causal spine) with verbatim `evidence_quote`.
4. **HARVEST** (sidecar, point-don't-extract) food/description/hospitality/prophecy/foreshadow/causal-spine breadcrumbs for later passes (`feedback_harvest_queue`, `feedback_capture_quotes_during_research`).

**Non-goals:** no theory readings (gated — `project_theories_track_deferred`), no `first_available` reasoning (deferred — `project_first_available_deferred`), no analytical edge types (FORESHADOWS/PARALLELS) minted in this pass.

### §1.1 — Provenance & confidence: F&B is an in-universe maester's history — **RESOLVED (§11 #9)**

**Matt's flag (2026-07-06):** *Fire & Blood* is written **in-universe by Archmaester Gyldayn**, who compiles and openly weighs **partisan, contradictory sources**: Grand Maester Munkun's *True Telling*, Grand Maester **Orwyle**'s account, Septon Eustace, and above all the court fool **Mushroom's Testimony**. Whole passages are *"Mushroom claims X, but Septon Eustace writes Y, and the truth may never be known."* The conflicting-accounts texture *is* the point of F&B and is a first-class extraction target.

**Confidence rule (RESOLVED — claim-by-claim, real schema fields):**

- F&B is real published GRRM canon — the floor for anything it asserts is **Tier 2** (Tiers 3–5 are fan-theory space).
- **Uncontested Gyldayn narration** (stated flatly, no hedge) → **Tier 1**. There is no POV text for 1–136 AC; F&B *is* the primary canonical source for this era.
- **Hedged / single-partisan / explicitly-disputed claims** → **Tier 2, capped**, carrying two **real optional edge fields** (not note strings):
  - `in_universe_source`: enum `mushroom | eustace | munkun | orwyle | gyldayn-synthesis | court-record | unattributed` — `orwyle` and `unattributed` added by review; bare "some say / it is said" is `unattributed`, NOT `gyldayn-synthesis` (that value means Gyldayn explicitly weighing sources).
  - `disputed: true`
  - **Validator invariant:** `disputed: true` ⇒ `confidence_tier` ≤ tier-2 (reject any tier-1 + disputed row).
- When two accounts genuinely conflict, **capture both** as separate claims/edges, each tagged to its source — never silently pick a winner.
- In **node prose**, disputed claims carry the attribution inline in the text ("According to Mushroom, …") — no prose-level metadata fields.
- Every F&B cite also carries `evidence_kind: book-fab` (§5.2), so downstream queries can always filter "this came from the maester-historian layer."
- **Blanket per-source ceiling REJECTED** (Fable ruling): Gyldayn synthesizes across sources; even Mushroom sometimes reports uncontested fact; a source-level cap discards exactly the texture being captured.

**Schema touch:** `in_universe_source` + `disputed` land in architecture.md §Edge Metadata (same change-batch as the `fab` book code + `book-fab` evidence_kind; one Active Decision). This slots beside the staged `occurred.dispute` sub-map (architecture.md:504) and follows the SUSPECTED_OF tier-cap precedent.

---

## §2 — The source and its quirks

`sources/raw/fire-and-blood.epub` (784 KB). Calibre-style epub: 27 `index_split_*.html` files + `toc.ncx` (authoritative navMap) + `content.opf`. **~263,900 words / ~356K tokens of content** — roughly half a mainline book.

**Structure** — ~24 named history sections (Aegon's Conquest → The Lysene Spring), 1–136 AC. **No POV structure** — third-person maester-historian narration (Gyldayn), so this is the D&E-shaped case (`dunk-egg-splitter`), not the POV-shaped case (`chapter-splitter`).

**The "voodoo" conversion left artifacts** (Matt bought on Amazon, hand-converted). Verified in the raw HTML:

- A **leaked build path** `out/B07C6TBTV3/book.pdf` prepended to most section bodies. Must be stripped.
- **OCR substitution errors**: `Jaehaerys | Targaryen` (`|` for `I`), `che Dragon` (`ch` for `th`), `than many maesters` (`than`/`that`). These corrupt *names and load-bearing words*.
- **Duplicated running headers** (section title printed twice at each section head).
- HTML file boundaries **do not align** with TOC section boundaries → **the splitter must cut on `toc.ncx` navMap anchors, not raw file boundaries.**

**Consequences:**
- The extraction prompt (§4) is told the text is OCR-noisy: prefer canonical spellings in the *roster*, never propagate a garbled token as a canonical name, flag garbled load-bearing tokens — **but quotes are copied verbatim from the file even when garbled** (§4, §5.2 — the quote→line locator greps the noisy file; a "fixed" quote is an unfindable quote).
- The split output gets a QA gate (§3.5) **including a deterministic OCR-frequency scan** so we know how noisy each unit is before extraction.

### Unit inventory (raw HTML files → rough budgets)

| HTML file | Words | ~Tokens | Lead section (NCX) |
|-----------|-------|---------|--------------------|
| 003 | 8,206 | 11K | Aegon's Conquest |
| 004 | 7,764 | 10K | Reign of the Dragon (Wars of Aegon I) |
| 005 | 19,745 | 27K | Three Heads Had the Dragon / **The Sons of the Dragon** |
| 006 | 5,199 | 7K | Prince into King (Jaehaerys ascension) |
| 007 | 7,567 | 10K | The Year of the Three Brides — 49 AC |
| 008 | 12,664 | 17K | A Surfeit of Rulers |
| 009 | 6,264 | 8K | A Time of Testing |
| 010 | 4,656 | 6K | Birth, Death, and Betrayal |
| 011 | 7,674 | 10K | Jaehaerys & Alysanne (Dragonstone) |
| 012 | 16,597 | 22K | Jaehaerys & Alysanne — Triumphs & Tragedies |
| 013 | 2,236 | 3K | The Long Reign |
| 014 | 23,501 | 32K | The Long Reign (cont.) |
| 015 | 18,268 | 25K | **Heirs of the Dragon** (Dance prelude) |
| 016 | 12,619 | 17K | Dying of the Dragons — Blacks & Greens / A Son for a Son |
| **017** | **26,979** | **36K** | Dying of the Dragons — Red Dragon & Gold / Rhaenyra Triumphant |
| 018 | 16,039 | 22K | Dying of the Dragons — Rhaenyra Overthrown |
| 019 | 7,274 | 10K | Dying of the Dragons — Short Sad Reign of Aegon II |
| 020 | 7,867 | 11K | Aftermath — The Hour of the Wolf |
| 021 | 10,394 | 14K | Under the Regents — The Hooded Hand |
| 022 | 11,412 | 15K | Under the Regents — War, Peace, Cattle Shows |
| 023 | 6,481 | 9K | Under the Regents — Voyage of Alyn Oakenfist |
| 024 | 15,661 | 21K | The Lysene Spring & End of Regency |
| 025 | 7,855 | 11K | **Lineages and Family Tree** (genealogy tables) |

The big ones (**014 ~32K, 017 ~36K, 005/015 ~25-27K**) are the Dance-of-the-Dragons dense core; they get **sub-split with a tighter ~10K cap** (§3.3, ruling #2). The **Lineages appendix (025)** is a special case — a *validation corpus*, not an edge source (§3.4, ruling #4).

---

## §3 — Source prep: the splitter (`fire-and-blood-splitter.py`)

Mirror `scripts/dunk-egg-splitter.py` (whole-work, no POV) + borrow the parts machinery from `scripts/dunk-egg-scene-splitter.py`. **New capability: it reads epub HTML, not `.txt`** — adds an HTML→clean-text front end (strip tags via stdlib `html.parser`; no new deps).

### 3.1 Book abbreviation — `fab` (RESOLVED, §11 #8)

**`fab` accepted.** Decisive extra argument found in review: the wiki's own F&B citations are anchored `Rfab<section_slug>` — the graph's existing Tier-2 provenance layer already uses this code, so `fab` cite_refs line up with the anchors they upgrade. *Adding the code is a schema touch — architecture.md §"File Naming" updates in lockstep (CLAUDE.md rule #6), one Active Decision batched with §1.1's fields and `book-fab`.*

### 3.2 Boundaries, cleanup, frontmatter

1. **Cut on `toc.ncx` navMap** (authoritative section titles + `src` anchors), not HTML file boundaries.
2. **Clean-text front end:** strip tags; **strip the `out/B07C6TBTV3/book.pdf` header**; drop page-number lines and duplicated running headers; normalize whitespace. **Do NOT auto-"fix" OCR letter-substitutions** (too risky for names) — leave them; the prompt + reconciler handle canonical spellings, quotes stay verbatim-to-file.
3. **Line-numbered-stable markdown output** — cite_refs are `fab-<slug>-NN:LINE`; the deterministic quote-locator in `mint_enrichment.py` greps quote→line, so files must not shift after extraction begins.
4. **FREEZE RULE (new in v2, ruling #6):** once the QA gate (§3.5) passes and Matt approves, `sources/chapters/fab/` is **frozen — append-never-modify**, like every other chapter dir. A re-split after any extraction has run is a provenance-breaking event and requires restarting the affected units. (This is why paragraph-ids were rejected as overengineering: the freeze + verbatim quotes make line anchors durable.)
5. **Frontmatter (per unit):**
   ```yaml
   book: FAB
   collection: fire-and-blood
   section_number: N            # NCX order
   section_title: "Heirs of the Dragon—A Question of Succession"
   part: 1                      # 1 unless sub-split
   era: dance-of-dragons        # deterministic from the section→era map (§5.5)
   first_available: pre-agot    # DEFERRED field — set static, do NOT reason per-section
   file_name: fab-heirs-of-the-dragon-15.md
   ```
   `first_available`: F&B spans 1–136 AC, all pre-AGOT; static `pre-agot` (`project_first_available_deferred`).

### 3.3 Naming & sub-splitting (RESOLVED, §11 #2)

- Base name: **`fab-<section-slug>-NN.md`** (NN = NCX section order, zero-padded).
- Oversized sections (> ~15K tokens) sub-split on paragraph boundaries → **`fab-<section-slug>-NN-pMM.md`** (reuse the scene-splitter's part convention + `queue-parts.jsonl`).
- Target unit budget **~8–12K source tokens**; **the four Dance-core files (005/014/015/017) use a tighter ~10K cap** — they are the densest named-cast + disputed-claims stretches and benefit most from headroom. Expected: ~23 sections → **~34–40 extraction units** (v1 said 30–34; the tighter Dance cap adds a few — linear cost, accepted).

### 3.4 Special case — the Lineages/Family Tree appendix (025) — RESOLVED (§11 #4): validation corpus, NOT edge source

The genealogy is **already in the graph** — the infobox merge shipped dense PARENT_OF/SPOUSE_OF/SIBLING_OF coverage (16,757 wiki-infobox edges). And the appendix is OCR'd tables, where one garbled name corrupts a kinship edge that everything downstream traverses. So:

- **Parse deterministically** (Python table/tree parse) → candidate kinship triples.
- **Diff against existing kinship edges** in `edges.jsonl`. Three buckets:
  - **confirm** (triple already present) — no action; log count.
  - **new** (triple absent) — route to `working/fire-and-blood/lineages-review.jsonl` with an OCR-suspicion flag. **Never auto-mint kinship from OCR'd tables.**
  - **conflict** (same source+type, different target) — route to the contradictions report (§5.4).
- **No Opus pass.** The appendix's real value is *error-catching* (wiki-vs-book disagreements, OCR tells), not new edges.

### 3.5 QA gate (before any extraction) — extended in v2

After split, a deterministic check + cheap read-only spot-check:

1. **Python heuristics (whole corpus):** PDF-path header count = 0; duplicated-header count = 0; per-unit word count vs NCX-section expectation (±10%); no text dropped/duplicated across boundaries (adjacent-unit boundary lines are unique); **OCR-frequency scan** — count `|` inside alphabetic tokens, `\bche\b`/`\bcbe\b`, mixed-case-mid-word, etc. → per-unit noise score written to `working/fire-and-blood/ocr-scan.md` (extraction ordering + verify-arm attention can use it).
2. **Spot-check:** sample 3–4 units (include the noisiest per the scan), Haiku subagent or Matt eyeballs.
3. Matt approves → **freeze** (§3.2.4). Only then does extraction start.

---

## §4 — The extraction unit: node-first enrichment prompt (`fab-enrichment-v1.md`)

A **new prompt**, distinct from both `mechanical-extractor.md` (20-table POV inventory — overkill for a history book) and D&E `pass1-prompt-v4.md` (Pass-1 shaped). It **borrows v4's locked-vocab discipline + harvest sidecar + self-containment** (subagents/`claude -p` don't load CLAUDE.md — paste the vocab and all rules, per `feedback_vocabulary_canon` and the v4 precedent) and **adds node-prose**.

Per unit, Opus emits **one proposal file** → `extractions/fire-and-blood/fab-<slug>-NN.enrichment.md`:

```markdown
# FAB — <section title> (part M)

## Entity Roster
(Every named entity in this unit, by natural name — NO slugs. The reconciler resolves
names→existing slugs in §5. The Disambiguator column is MANDATORY for any first-name-
only or same-name-prone entity: give the fullest identification THE TEXT ITSELF supports.)
| Name (as in book) | Type guess | Disambiguator (parent/spouse/regnal/epithet, from text) | New-to-me? | Canonical-spelling note (if OCR-garbled) |

## Node Prose
(BOOK-GROUNDED biography/description. Budget rule: 2–5 sentences for the unit's ~10–15
entities of substance; ONE line for minor entities; nothing for pure mentions. Each
load-bearing claim carries a verbatim quote anchor. Factual, not interpretive. Disputed
claims carry the attribution INLINE in the prose: "According to Mushroom, …")
### <Name>
<prose>  — quote: "<verbatim ≤15-word anchor>"

## Relationships Observed   (controlled vocabulary — book-cited edges)
| Source (name) | EDGE_TYPE [(qualifier)] | Target (name) | in_universe_source | disputed | evidence_quote (verbatim) |
- EXACTLY one UPPER_CASE type from the LOCKED vocab (pasted below).
- Qualifiers required for the 8 Tier-1 types; optional for the 9 Tier-2 types
  (reference/edge-qualifier-vocab.md — pasted).
- in_universe_source ∈ {mushroom, eustace, munkun, orwyle, gyldayn-synthesis,
  court-record, unattributed} — ONLY when the text hedges or names its source; blank
  for plain narration. disputed = true whenever in_universe_source is set OR accounts
  conflict; blank otherwise.
- In-text identity/regnal reveals → SAME_AS / ALIAS_OF.
- Non-fit → `NEEDS_VOCAB: <plain description>` (routes to vocab-gap tooling; do NOT invent a type).
- Hard-excluded: KNOWS (deprecated), analytical types (FORESHADOWS/PARALLELS/…),
  spatial/possession/title relations that belong in their own rows.

## Events of Note   (candidate event nodes for the Dance / councils / battles)
| Event (name) | type (event.*) | year (AC, if the text states/implies it; else blank) | agent | patient | instrument | location | outcome | quote |

## Harvest sidecar  → append breadcrumbs to {HARVEST_PATH}
FAB / <verbatim anchor> / <kind> / <one-line note>
kind ∈ {targaryen-history, prophecy, food, description, hospitality,
        cross-identity, foreshadow-hook, causal-spine, other}
```

**Prompt rules (self-contained):**
- **OCR tolerance:** the text is machine-converted and noisy. In the *roster*, prefer canonical spellings and note the garble; never propagate a garbled token as a canonical name; flag (don't guess) garbled load-bearing tokens. **But every `evidence_quote` and quote anchor is copied VERBATIM from the file, garbles included** — a downstream locator greps the noisy file for your exact string; a "corrected" quote is an unfindable quote (v2, review R2).
- **No slug resolution** — emit natural names only; the deterministic reconciler (§5) does UPDATE-vs-CREATE. (Opus can't hold 8,700+ slugs; forcing slug guesses causes drift.)
- **Verbatim quotes, no line numbers** — the downstream locator finds lines (D&E v4 convention).
- **Checkpoint per section** — don't defer tables to the end; a mid-unit wall shouldn't lose work.
- **Attribution & dispute (F&B-specific, §1.1):** hedges/named sources (`"Mushroom claims"`, `"Septon Eustace writes"`, `"some say"`, `"the truth is not known"`) → set `in_universe_source` + `disputed`. **Hedge scope:** a hedge governs the whole passage it introduces, not just its own sentence — if the surrounding ±10 lines frame the claim as one account among several, tag it. If two accounts conflict, emit **both** rows, each tagged — never silently pick a winner. Plain uncontested narration gets neither field (→ Tier-1).
- **first_available:** copy the static frontmatter value verbatim; do not reason.
- **Final self-audit** before finishing (all sections present, no meta-commentary in cells, vocab-only edge types, Disambiguator column filled for same-name-prone entities, no cross-unit leakage).

---

## §5 — Deterministic reconciliation (`fab-reconcile-candidates.py`)

*Python before Agent* (`feedback_python_before_agent`): the LLM proposed by name; a deterministic pass resolves identity, validates quotes, and routes. Turns each `.enrichment.md` into (a) a `candidates.json` for `mint_enrichment.py` (CREATE nodes + all edges) and (b) a `merge-plan.json` for `fab_merge_node.py` (UPDATE prose, §5.3).

### 5.0 Per-unit candidate packs (`fab-build-candidate-packs.py`) — NEW in v2

**The wiki already tells us which nodes each F&B section touches.** Node prose carries cite anchors of the form `cite_ref-Rfab<section_slug>…` — **1,634 nodes** have at least one; **221 nodes** cite "heirs of the dragon" alone. Build once, deterministically:

- **Input:** `graph/nodes/**/*.node.md` (grep `cite_ref-Rfab` anchors), NCX section list.
- **Algorithm:** normalize each anchor's section slug → map to the split unit(s) covering that section → emit per-unit `working/fire-and-blood/candidate-packs/fab-<slug>-NN.json`: `{expected_slugs: [...], per_slug: {name, aliases, type}}`.
- **Consumers:** (a) the reconciler — an expected-slug match is a strong prior in disambiguation scoring; (b) the worker — a compact roster hint (names only, ≤2K tokens) pasted into the unit prompt so Opus spells canonical names correctly against OCR noise.
- **Acceptance:** pack exists for every unit; `heirs-of-the-dragon` pack contains `rhaenyra-targaryen`, `daemon-targaryen`, `criston-cole`; no pack exceeds 2K tokens in hint form.

### 5.1 Name → slug resolution — MATCH-first, **hardened** (RESOLVED, §11 #5; review R1)

**The default is MATCH an existing node; CREATE is the rare exception.** But v1 under-specified the *worse* failure: the live resolver returns a **confident exact HIT for "Aegon Targaryen"** — onto `aegon-targaryen`, a zero-edge node minted from the wiki's *disambiguation page* (verified 2026-07-06). Duplicate-minting fractures the graph; confident wrong-match **corrupts it silently**. So resolution is:

**Inputs:** roster rows (name + Disambiguator column), alias table (`weirwood query resolve`), the **disambiguation pack** `working/wiki/data/same-name-clusters.json` (from the companion track — cluster registry + per-slug discriminators: parents, born/died years, era, key title), the **trap-node blocklist**, the unit's candidate pack (§5.0), the unit's frontmatter `era`.

**Trap-node blocklist (deterministic, built once):** nodes whose `wiki_source` page carries the MediaWiki category `Disambiguation pages` in `working/wiki/data/page-categories.jsonl` (bare `aegon-targaryen`, `aemon-targaryen`, `baelon-targaryen`, `daeron-targaryen`, `jaehaerys-targaryen`, `rhaena-targaryen`, …). **A blocklisted node is NEVER an UPDATE target and never a confident match** — any hit on one is routed as ambiguous.

**Routing per roster/edge entity:**
1. **Exact/alias hit, NOT blocklisted, NOT in a same-name cluster → UPDATE** (the common case — Criston Cole, Balerion, Hugh Hammer, Nettles all resolve clean; verified).
2. **Hit on a blocklisted node, OR name is in a same-name cluster → discriminator scoring** against every cluster member: match the roster row's Disambiguator (parent/spouse/regnal/epithet) + the unit's era + candidate-pack membership against each candidate's edges and pack discriminators. **Auto-accept only when the top candidate is supported by ≥2 independent discriminators AND the runner-up has none** (decisive margin). Otherwise → review file `working/fire-and-blood/reconcile-review.jsonl` (one JSONL row per case: name, unit, Disambiguator, scored candidates with their evidence — reviewable by a cheap agent or Matt at a glance).
3. **No hit, confidently empty → CREATE** — with guards: **never auto-create from a bare first name** (an unresolvable "Aegon" is a review case, not a new node); CREATE requires a full/unique name AND no cluster collision. Log to `working/fire-and-blood/created-nodes.jsonl`; run the `duplicate-detector` agent over each unit's new batch before mint as the safety net.

**Smoke policy:** during the two smoke units (§7), buckets 2's auto-accept is DISABLED (everything scored goes to review) — thresholds get tuned on what the review reveals, then validated on ≥2 fresh units before the bulk run (`feedback_fresh_review_and_out_of_sample`).

### 5.2 Quote pre-validation + cite_ref build — extended in v2 (review R2)

`mint_enrichment.py` is **fail-fast: one unfound quote aborts the entire unit's mint** (`authoritative_line` → `sys.exit`). With OCR-noisy source this WILL fire. So the reconciler pre-validates:

- For every quote (edge evidence + prose anchors): run the **same `norm()`+grep** as mint (single-line, then two-line join) against the unit file.
- **Located** → row proceeds; `evidence: fab-<slug>-NN:LINE`, `evidence_kind: book-fab`, `confidence: tier-1` (or tier-2 + `in_universe_source`/`disputed` per §1.1).
- **Not located** → the row is **quarantined** to `working/fire-and-blood/quotes-review.jsonl` (row-level, unit proceeds). Typical fix is trivial (extractor normalized an OCR garble) — a cheap agent patches the quote against the file text and re-runs the reconciler; only genuinely absent quotes get dropped.
- `mint_enrichment.py` therefore only ever receives pre-located quotes; its fail-fast becomes a true invariant check, not an operational hazard.
- Extend mint's `evidence_kind` via `_meta` (already supported: `common()` reads `meta.evidence_kind`) — set `"evidence_kind": "book-fab"` in each unit's `candidates.json` `_meta`. **No mint code change needed for this.**

### 5.3 UPDATE merge semantics — RESOLVED (§11 #1): **new merge writer, Option A+**

**Correction (Fable review C1):** `mint_enrichment.py` does NOT overwrite existing nodes — it **skips them** (`SKIP node (exists)`). So the v1 data-loss framing was wrong; the real gap is that **UPDATEs would be silently dropped**. The UPDATE path is a **new script**, `scripts/fab_merge_node.py`:

- **Input:** per-unit `merge-plan.json`: `[{slug, identity_line (optional), fab_section_md, run_id}]`.
- **Algorithm per node:**
  1. Read the existing node file. **Never touch:** frontmatter fields (except `node_version` +1), existing `## Edges`, and ALL existing prose sections (the rich wiki prose on shape-(b) nodes is good and its wiki cite anchors are the Tier-2 layer — preserve).
  2. **Identity handling by node shape (§1):** boilerplate Identity line (exact regex `^.+ is a [a-z][a-z.]* from the AWOIAF wiki\.$`) → **replace that one line** with the book-grounded identity line. Real (non-boilerplate) Identity → leave it; skip the swap. **No `## Identity` section** → insert one (with the new line) immediately after frontmatter.
  3. **Append** a `## Fire & Blood` section (create or extend) containing the unit's prose block, each claim with its `(fab-<slug>-NN:LINE)` cite, opened with an idempotency marker `<!-- fab-enriched: <run_id> -->`.
  4. **Idempotency:** if the marker for this `run_id` is already present → skip (re-run safe).
  5. Write via temp-file + atomic rename.
- **Edges never touch node files** — all edges go to `edges.jsonl` via mint (§5.2), exactly like every enrichment dip since S158.
- **Option B (full Identity rewrite + edge-merge) REJECTED for bulk** — it would displace shape-(b) nodes' good wiki prose. Promoting specific high-traffic principals (Rhaenyra, Daemon, Aegon II, Alicent, Criston) to hand-curated rewrites happens **after** the run as ordinary curation dips.
- **Acceptance (smoke):** run on copies of one node of each shape (a)/(b)/(c); verify frontmatter byte-identical except node_version; wiki prose untouched; boilerplate line swapped on (a)+(b)-boilerplate; section inserted on (c); second run = no-op.

### 5.4 Contradiction diff + duplicate policy — NEW in v2 (review R7)

- **Duplicate-with-better-evidence is INTENDED:** a proposed F&B edge whose (type, source, target[, qualifier]) already exists as `wiki-infobox` is still emitted — that IS the Tier-1 overlay (`feedback_book_citation_overlay_value`); queries prefer max-tier evidence. Do not "dedup" these.
- **Conflicts are flagged:** after resolution, diff proposed F&B kinship/allegiance/title/succession edges against existing `wiki-infobox` edges on the same source node. Same (source, type) with a **different target** (or a `disputed` F&B tag against a flat wiki claim) → `working/fire-and-blood/contradictions-report.md`, grouped by node, for review. This is where "F&B contradicts the infobox" surfaces instead of silently accreting.

### 5.5 `era:` + `occurred:` stamping — NEW in v2

- **CREATE nodes stamp `era:`** (architecture.md forward-only convention). Deterministic section→era map baked into the reconciler: conquest sections (003–004) → `targaryen-conquest`; 005–014 + 020–024 → `targaryen-rule`; 015–019 → `dance-of-dragons`. Zero LLM cost.
- **CREATE `event.*` nodes with a `year (AC)` value** from the Events table get an `occurred:` block: `ac_year`, `precision: year`, `basis_source: narrative-prose`, `basis_reliability: primary-source`, `date_confidence: tier-1` (uncontested) / `tier-2` (hedged). This is strictly better provenance than the existing wiki-year-page/tertiary-fan datings.

---

## §6 — Long-running harness

Reuse the D&E track's exact shape (`worklog-dunk-egg.md` → generic `longrun.sh` ← per-track worker). **No new supervisor** — `scripts/longrun.sh` is the canonical one.

> **⚠️ Maturity note (v2, review R6):** the `claude -p`-worker-under-`longrun.sh` *extraction* pattern has **never completed a unit** — D&E Pass-1 is still at smoke-attempted/auth-blocked (DE-1/DE-2). F&B's stage-1 smoke (§7) doubles as this pattern's first end-to-end proof; expect harness bugs at smoke-time, not bulk-time, and if the D&E smoke lands first, fold in its lessons before building the F&B worker.

### 6.1 Worker (`fire-and-blood-extraction.py`)
Implements the `longrun.sh` **exit-code contract**: `0` all-done · `2` rate-limit wall · `10` iteration-ok-more-remain · other = crash. Flags mirror D&E: `--build-queue` · `--smoke --only <unit>` · `--prompt-version v1` · `--skip-existing` (resume). One unit per iteration, atomic claim + `--skip-existing` so a relaunch never re-does a finished unit. Model **hardcoded `claude-opus-4-8`** (node-prose quality genuinely needs it — the `feedback_model_selection_at_session_start` reasoning-depth carve-out). Prompt-version is **pinned for the whole bulk run** — a mid-run prompt bump means either accepting heterogeneous output or re-running done units; neither silently. Telemetry → `working/telemetry/fire-and-blood.jsonl` via `pace.emit_telemetry_row`, **plus a per-unit summary row** (§7a observability).

### 6.2 Launch & pacing
```
weirwood run start fire-and-blood        # → longrun.sh → the worker
```
Env (from `scripts/longrun.sh`), seed from `pace.py report --track fire-and-blood` after the smoke:
- `LONGRUN_SLEEP_BETWEEN` — between successful units (default 1200s; these units are large — start ~1200–1800s).
- `LONGRUN_WALL_SLEEP` — after a rate-limit wall (default 3600s).
- `LONGRUN_CRASH_SLEEP` / `LONGRUN_MAX_CRASHES` — defaults (300s / 5).
- `LONGRUN_LOG` — tee to `working/fire-and-blood/logs/`.

### 6.3 ⚠️ Operational constraint — run from iTerm, not from inside Claude Code
A nested `claude -p` spawned **from inside a Claude Code session 401s** (host OAuth isn't inherited — the durable finding behind `feedback_no_extraction_without_asking`; reproduced by the D&E track, DE-1). **Matt launches this pass himself from a logged-in iTerm.** The smoke command will be a single copy-paste line (`feedback_one_handoff_per_block`). Claude preps and gates; it cannot launch.

---

## §7 — Verification & drift gates (mandatory — not optional)

Every bulk LLM run carries: schema validator + cross-model audit + verdict-gates-apply (`feedback_drift_detection_mandatory`, `feedback_subagent_verify_not_matt`, `feedback_fresh_review_and_out_of_sample`). Matt does **not** review edges one by one.

1. **Mechanical schema validator** — every proposed node/edge conforms: types in architecture.md TYPE_DIR_MAP, edge labels in locked vocab, qualifier rules per `edge-qualifier-vocab.md`, cite_ref well-formed, quote present at the cited line, `in_universe_source` in enum, **`disputed: true` ⇒ tier ≤ 2** (the §1.1 invariant), `era` in enum on new mints.
2. **Fresh-verify subagent, stratified sample** per unit — re-reads the F&B chapter text + wiki cache, confirms each sampled edge/prose claim; **verdict gates apply** (`finalize_enrichment.py` consumes `verdicts.json`). Cheaper model (Haiku) for the audit arm. **v2 addition — the sample is stratified on the dispute axis:** it must include N tagged-disputed claims AND N untagged-Tier-1 claims *from Dance units specifically*, checking hedge-scope within ±10 lines. Both failure directions are counted: missed hedges (tier inflation) and over-tagging (tier deflation, which would gut the Tier-1 upgrade that is the pass's point). Either direction >10% on the smoke gates the bulk run.
3. **Out-of-sample stability** — validate the accept-filter (incl. §5.1 auto-accept thresholds) on ≥2 fresh units, not the unit it was tuned on.
4. **Two-stage smoke (RESOLVED, §11 #7):**
   - **Stage 1 — `fab-aegons-conquest-03`** (small, clean): proves splitter output, worker/harness plumbing (first-ever completed run of this pattern — §6 note), reconciler + candidate-pack wiring, merge-writer on real nodes (dry-run targets). Judge: mechanics.
   - **Stage 2 — `fab-heirs-of-the-dragon-15`** (dense Dance prelude): the ambiguity/dispute/quality stress test — same-name routing, disputed tagging, node-prose quality, UPDATE/CREATE mix. Judge: quality.
   - Both gated on Matt's go before bulk (`feedback_no_graph_mutation_without_goahead`: a good dry-run earns confidence in the *design*, not permission to *apply*).

### §7a — Observability (NEW in v2)

Per-unit summary JSONL (`working/fire-and-blood/run-summary.jsonl`), one row per unit at reconcile time: `{unit, entities_rostered, matched, ambiguous_to_review, created, edges_by_type, quotes_total, quotes_located_pct, quotes_quarantined, needs_vocab_count, disputed_rate}`. These are the gate's inputs and the drift alarm — e.g. a unit with quote-location <90% is an OCR hotspot (check `ocr-scan.md`); a Dance unit with `disputed_rate ≈ 0` is a prompt failure; a spike in `created` is a resolver failure. The gate reviews this table, not raw output.

---

## §8 — Apply & integrate (all gated on Matt's explicit go)

**Order per unit-batch:** checkpoint → mint (CREATE nodes + ALL edges) → merge (UPDATE prose) → finalize (verdicts) → refresh.

1. **Rollback checkpoint (NEW in v2):** `git add -A && git commit` on the repo before each apply batch (graph is git-tracked; this is the cheapest complete rollback). Per-unit `run_id` = `fab-<slug>-NN-<date>` gives: mint's existing re-run guard (unit-level idempotency for edges), the merge writer's marker (node-level idempotency), and a **revert recipe** — restore the mint's edges backup (`graph/edges/_regrounding/edges-pre-…`) + `git checkout` of the touched node files. A half-completed bulk run is therefore resumable (`--skip-existing`) AND unwindable (per run_id), unit by unit.
2. `python3 scripts/mint_enrichment.py --candidates working/fire-and-blood/<unit>/candidates.json` — atomic quote-verified edge append + CREATE-node write (`_meta.evidence_kind: "book-fab"`).
3. `python3 scripts/fab_merge_node.py --merge-plan working/fire-and-blood/<unit>/merge-plan.json` — UPDATE prose merges (§5.3). Its summary MUST report `merged / created-elsewhere / skipped`; **any UPDATE payload that ends up skipped is a hard error** (that's the silent-drop failure, review R3).
4. `python3 scripts/finalize_enrichment.py --verdicts .../verdicts.json` — apply fresh-verify verdicts.
5. `weirwood refresh` — rebuild entity/character/alias/search/theme indexes so new nodes are **discoverable** (`project_rebuild_derived_artifacts_after_node_mutation`); also required after merge-writer runs (Identity text is searchable).
6. **Chat-bundle rebuild is a separate, manual pre-deploy step** (`web/data/*`, per `DEPLOY.md`) — do it when the alpha is next deployed. Note the new `sources/chapters/fab/` files enter the web bundle then (receipts-rail navigation to F&B cites comes free).

---

## §9 — Cost & time (order-of-magnitude) — v2 adjusted

- **Source:** ~356K content tokens → **~34–40 units** after the tighter Dance-core sub-split.
- **Input:** prompt (~6K) + source (~8–12K) + candidate-pack roster hint (≤2K) per unit ≈ **~0.6–0.8M input tokens** total.
- **Output:** node prose (budget-ruled, §4) + edges + quotes ≈ **10–18K/unit → ~0.4–0.7M output tokens**.
- **$ band:** on Opus-4.8 list pricing this is **roughly a few tens of dollars, one-time** — *confirm current rates at launch*. The Haiku verify arm ≈ noise.
- **Ballooning modes (named — review E):** (a) whole-unit re-extraction to fix quotes — **capped by §5.2's row-level quarantine** (fix quotes cheaply, never re-extract for them); (b) sub-split creep in the Dance core (accepted, linear); (c) **review-bucket human/agent time — the real bottleneck**, and exactly what the companion pack + Disambiguator column shrink. If §5.2 didn't exist, budget 1.5–2×; with it, the estimate holds.
- **Wall-clock:** ~34–40 units × (~few-min/unit + `LONGRUN_SLEEP_BETWEEN`) → an overnight-ish background run under `longrun.sh`, wall-resilient.

---

## §10 — Sequencing (v2 — re-ordered per rulings #7/#10)

1. ~~Fable reviews this doc~~ **DONE 2026-07-06** → rulings applied (this v2). **Matt reads `fable-review.md` + this doc → go/no-go on the plan.**
2. **Companion track deterministic step runs FIRST** (`working/node-enrichment-wiki-prose/design.md` v2): emits the disambiguation pack + trap-node blocklist F&B's reconciler consumes, and the Identity lines that make review legible. Pure Python, cheap, independently valuable. (F&B splitter build may proceed in parallel — no dependency; F&B *extraction* gates on the pack existing.)
3. Update `architecture.md` in ONE batch (add `fab` code; `evidence_kind: book-fab`; edge fields `in_universe_source` + `disputed` + the tier invariant) + worklog Active Decision.
4. Build `fire-and-blood-splitter.py` (script-builder) → split → **QA gate incl. OCR scan (§3.5)** → Matt approves → **freeze** `sources/chapters/fab/`.
5. Build `fab-build-candidate-packs.py` (§5.0) + `fab-reconcile-candidates.py` (§5.1–5.2, 5.4–5.5) + `fab_merge_node.py` (§5.3, smoke on copied nodes) + write `fab-enrichment-v1.md` prompt + `fire-and-blood-extraction.py` worker; wire `weirwood run`.
6. **Smoke stage 1** (`aegons-conquest`, from iTerm, Matt) → judge mechanics → fix loop.
7. **Smoke stage 2** (`heirs-of-the-dragon`) → judge quality + disputed-tagging + reconciler routing (auto-accept disabled; review everything) → tune thresholds → validate on ≥2 fresh units.
8. Tune `LONGRUN_SLEEP_BETWEEN` from `pace.py`; **bulk run** under `longrun.sh` (prompt version pinned).
9. Reconcile → verify (§7 gates, per §7a summary table) → **Matt's apply go** → checkpoint → `mint` → `merge` → `finalize` → `weirwood refresh` (§8).
10. Deterministic Lineages-appendix **validation diff** (§3.4) → review buckets → contradictions report triage.
11. **Harvest-queue drain scheduled** as part of run close-out (~30–40 units of sidecar lines; don't let it re-balloon — the S153–S156 lesson).
12. Post-run curation dips: hand-promote Dance principals' Identity rewrites (Option B, §5.3); chat-bundle rebuild at next deploy.

---

## §11 — Decisions — RESOLVED by Fable review 2026-07-06 (Matt's overall go still gates the build)

| # | Decision | Ruling (one line — rationale in `fable-review.md` §3) |
|---|----------|-------------------------------------------------------|
| 1 | UPDATE merge semantics | **A+ via NEW `fab_merge_node.py`** (additive section + boilerplate-line swap + insert-if-absent + idempotency marker); B rejected for bulk (rich wiki prose must survive); B-by-hand for principals post-run. v1's "mint overwrites" premise was factually wrong — mint skips (C1). |
| 2 | Unit granularity | 8–12K accepted; **~10K cap for 005/014/015/017**; 15K threshold OK; **freeze rule** added. |
| 3 | Node-prose vs slim | **Keep Node Prose with the budget rule** (2–5 sentences × ~10–15 substantial entities; one-liners below). UI-composes-prose rejected — the prose is the portfolio product. |
| 4 | Lineages appendix | **Deterministic parse as VALIDATION corpus** — diff vs existing kinship edges; never auto-mint from OCR'd tables; conflicts → contradictions report. No Opus. |
| 5 | Reconciler ambiguity | **Tiered auto-accept:** clean non-cluster exact/alias hits only; cluster/blocklist hits need ≥2 independent discriminators + decisive margin; else review. Auto-accept disabled during smoke; thresholds tuned out-of-sample. |
| 6 | cite_ref granularity | **Section-level line anchors** + the freeze rule. Paragraph ids rejected (overengineering; verbatim quotes are the durable anchor). |
| 7 | Smoke unit | **Two-stage:** 003 Aegon's Conquest (mechanics — also first-ever proof of the longrun+`claude -p` pattern) then 015 Heirs of the Dragon (quality/ambiguity). |
| 8 | `fab` abbreviation | **Accepted** — bonus: matches the wiki's own `Rfab*` cite-anchor prefix. architecture.md lockstep update. |
| 9 | Provenance/confidence | **Claim-by-claim; REAL edge fields** `in_universe_source` (enum + `orwyle` + `unattributed`) + `disputed`; validator invariant disputed⇒≤tier-2; blanket per-source ceiling rejected; prose attribution inline. |
| 10 | Sequencing vs companion | **Companion FIRST**, restructured to emit the machine-readable disambiguation pack (+trap blocklist) the reconciler consumes — that's what makes the de-risk real rather than reviewer-comfort. |

---

## Appendix — reused infrastructure (exact paths)

| Purpose | Reuse | Notes |
|---------|-------|-------|
| Splitter template | `scripts/dunk-egg-splitter.py`, `scripts/dunk-egg-scene-splitter.py` | add epub-HTML front end |
| Supervisor | `scripts/longrun.sh` | exit-code contract 0/2/10/crash; env-configured sleeps; **pattern unproven for `claude -p` extraction — smoke 1 is its first proof (§6 note)** |
| Pacing/telemetry | `scripts/pace.py` | `report --track fire-and-blood` → sleep baseline; `emit_telemetry_row` |
| Claim/resume | `scripts/claim-chapter.py` pattern | atomic claim + heartbeat + stale detection |
| Locked edge vocab | `reference/architecture.md` §Edge Types, `reference/edge-qualifier-vocab.md` | paste into prompt |
| Harvest sidecar + SAME_AS reveals + self-containment | D&E `working/dunk-egg-pass1/prompts/pass1-prompt-v4.md` | borrow patterns |
| Apply (edges + CREATE) | `scripts/mint_enrichment.py`, `scripts/finalize_enrichment.py` | **skip-if-exists on nodes (verified)** — UPDATE prose goes through NEW `fab_merge_node.py`; `evidence_kind: book-fab` via `_meta` (no code change) |
| Refresh | `weirwood refresh` (`scripts/weirwood-refresh.sh`) | entity/char/alias/search/theme indexes |
| Query/resolve | `weirwood query resolve`, `graph/query/build/build_alias_table.py`, `build_search_index.py` | name→slug reconciliation — **hardened per §5.1 (trap blocklist + cluster routing); a bare resolver HIT is not sufficient** |
| Same-name discriminators | companion track's `working/wiki/data/same-name-clusters.json` + `page-categories.jsonl` (`Disambiguation pages`, `NN AC births/deaths`) | new dependency (v2) |
| Verify | fresh-verify subagents + `verdicts.json` gate | mandatory drift gate; dispute-axis strata added (§7.2) |
| Post-CREATE safety net | `duplicate-detector` agent | run per unit batch before mint |
