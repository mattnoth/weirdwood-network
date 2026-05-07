# Citation Audit — 2026-04-30

**Nodes scanned:** 4,290 total node files in `graph/nodes/**/*.node.md`
- 3,385 Stage 3 deterministic (`pass_origin: pass2-wiki-deterministic`, `prompt_version: v1-python`)
- 905 Stage 1 agent-synthesized (`pass_origin: pass2-wiki`, `prompt_version: v1`)
- 4,236 in-scope (excluding 53 in `_conflicts/` and 1 in `_unclassified/`)

**Citations checked:** ~50,000+ parenthetical citation tokens across the corpus (sampling-based — not every cite was individually validated against the wiki page index).

**Total findings:**
- HIGH: 5 distinct malformed-pattern classes (with hundreds of occurrences in aggregate); 2 nodes with concrete claims missing citations (sample-based)
- MED: 4 format-drift classes affecting ~1,200 cite occurrences across ~330 nodes
- LOW: 2 cosmetic patterns (~3,400 wiki cite_refs with URL-encoded MediaWiki template noise)
- PENDING-PASS-1: 9 chapter-cite occurrences across 6 nodes pointing to non-AGOT books

---

## Category 1: claims missing citations

This audit was sample-based — exhaustive scanning of 4,236 nodes for "concrete factual claim missing a parenthetical cite at sentence end" is not feasible without a structured parser. Spot checks on representative nodes:

### Stage 1 (agent-synthesized) — citation density patterns

Stage 1 nodes generally close every claim with a parenthetical cite. Where they fail, the failure is mid-paragraph short claims chained off a long one. Examples found:

- **HIGH** — `graph/nodes/houses/house-mallister.node.md` line 33 (Narrative Arc):
  - "He supports Robb Stark's crowning as King in the North." — no cite (concrete factual claim).
  - "His son Patrek is captured." — no cite.
  - "In ACOK-ASOS, Jason continues to fight for the Stark-Tully cause." — no cite.
  These three sentences sit between cited claims; the writer apparently relied on the bracketing `(wiki:House_Mallister)` to cover a multi-claim run.

- **MED** — `graph/nodes/houses/house-darke.node.md` line 29 (Allegiances): "Related to House Darklyn as possible distant kin/cadet branch." — no cite, though a direct factual claim. The `## Identity` section above does cite this same point with `(wiki:House_Darke)`, so this is duplication-without-cite rather than uncited new claim.

- **MED** — `graph/nodes/characters/jon-snow.node.md` line 74 (Notes): "Jon's fate after the stabbing at the end of ADWD is unresolved." — editorial framing, not a concrete in-world claim, but the sentence structure suggests it; would not be flagged by a strict reader.

### Stage 3 (deterministic) — high cite density

Stage 3 nodes inherit citations directly from wiki HTML and have one cite at the end of every paragraph by construction. Sampling 30 Stage 3 prose nodes (`vermithor`, `harys-swyft`, `last-dragon`, `walderan-tarbeck`, `aegon-i-targaryen`, etc.) found zero missing-cite claims in narrative prose — the deterministic emitter preserves every wiki `<sup>` cite as a `(wiki:Page.cite_ref-X)` parenthetical.

The one weak spot in Stage 3: the **Identity** section is a templated stub: `"X is a character.human from the AWOIAF wiki."` with no cite. Since this sentence is not a factual claim about the character (it's a meta-description of source provenance), I'm leaving it as LOW.

### Recommendation

Run a narrower scripted scan: for each node, find sentences ending in a period that are NOT followed by a parenthetical citation within the same paragraph. Flag only sentences that contain a tensed verb plus a proper noun. Without that script, this category is undersampled and cannot be reported exhaustively here.

---

## Category 2: broken chapter-file references

### HIGH: AGOT chapter cites — all resolve

All AGOT chapter-format citations (`(agot-{pov}-{NN})`) found in the corpus point to extraction files that exist in `extractions/mechanical/agot/`. AGOT extractions cover prologue + ch01-15 (eddard), ch01-09 (tyrion), ch01-09 (jon), ch01-11 (catelyn), ch01-07 (bran), ch01-06 (sansa), ch01-05 (arya), ch01-10 (daenerys). Spot-checked cites include `agot-bran-02`, `agot-jon-01`, `agot-eddard-09`, `agot-eddard-12`, `agot-eddard-14`, `agot-eddard-15`, `agot-arya-03`, `agot-catelyn-08`, `agot-daenerys-08`, `agot-daenerys-10`, `agot-jon-03`, `agot-tyrion-04`, `agot-prologue` — all have corresponding `.extraction.md` files. **Zero broken AGOT chapter references.**

Two AGOT cites are malformed by missing the chapter number — see Category 3.

### PENDING-PASS-1: 9 chapter-cite occurrences across 6 nodes

These cite ACOK / ASOS / AFFC / ADWD chapters that have no Pass 1 extraction yet. They cannot resolve until those books are extracted. Treat as "pending Pass 1 completion," not as broken:

| Node | Citation | Book |
|------|----------|------|
| `characters/areo-hotah.node.md:41` | `(affc-the-queenmaker)` | AFFC |
| `characters/areo-hotah.node.md:42` | `(adwd-the-watcher)` | ADWD |
| `characters/areo-hotah.node.md:43` | `(affc-princess-in-the-tower)` | AFFC |
| `characters/doran-martell.node.md:41` | `(affc-princess-in-the-tower)` | AFFC |
| `characters/joy-hill.node.md:42` | `(affc-jaime)` | AFFC |
| `characters/kevan-lannister.node.md:46,49` | `(affc-cersei)` x2 | AFFC |
| `characters/pycelle.node.md:51` | `(acok-tyrion)` | ACOK |
| `houses/house-hayford.node.md:39` | `(affc-jaime-03)` | AFFC |

Note: most of these are POV-only references (no chapter number, e.g. `affc-jaime`), which is also a Category 3 malformed-pattern issue once Pass 1 ACOK/ASOS/AFFC/ADWD comes online — chapter slugs there will use a numeric `-NN` suffix, not the POV name.

---

## Category 3: malformed cite_ref formats

Five distinct malformed patterns identified, with severity HIGH because they break automated cite-parsing.

### 3.1 HIGH: Bare cite_ref ID treated as a wiki page

Pattern: `(wiki:R{book}{chapter})` — e.g. `(wiki:Raffc9)`, `(wiki:Rasos11)`. The `R{book}{chapter}` token is meant to be a cite_ref anchor on a specific wiki page, not a wiki page itself. The page `Raffc9` does not exist on the wiki; the writer dropped the `Page.cite_ref-` prefix.

**Count:** 11 occurrences across 11 nodes (all Stage 1 / `pass2-wiki`).

| Node | Cite found |
|------|------------|
| `houses/house-bar-emmon.node.md` | `(wiki:Raffc...)` |
| `houses/house-boggs.node.md` | `(wiki:Racok...)` |
| `houses/house-cargyll.node.md` | `(wiki:R...)` |
| `houses/house-cave.node.md` | `(wiki:R...)` |
| `houses/house-chelsted.node.md` line 29 | `(wiki:Rasos11)` |
| `houses/house-chyttering.node.md` | `(wiki:R...)` |
| `houses/house-dargood.node.md` | `(wiki:R...)` |
| `houses/house-darke.node.md` line 33 | `(wiki:Raffc9)` |
| `houses/house-darklyn.node.md` line 37 | `(wiki:Raffc9)` |
| `houses/house-darkwood.node.md` | `(wiki:R...)` |
| `factions/dragonkeepers.node.md` | `(wiki:R...)` |

These appear to be agent paraphrases of cite_refs where the agent stripped the page name. They will fail any wiki-page-existence validator.

### 3.2 HIGH: Bare AGOT-pov cite without chapter number

Pattern: `(agot-{pov})` without the `-{NN}` chapter suffix. Two distinct nodes affected:

- `graph/nodes/characters/pycelle.node.md` line 47: `(agot-eddard)` — no chapter number
- `graph/nodes/characters/pycelle.node.md` line 49: `(agot-sansa)` — no chapter number
- `graph/nodes/houses/house-mallister.node.md` line 33: `(agot-prologue)` — actually well-formed (prologue is the chapter slug)

The `pycelle.node.md` cites cannot resolve to a specific extraction file. Likely the writer intended a specific chapter and dropped the number.

**Count:** 2 broken occurrences in 1 node.

### 3.3 HIGH: Comma-joined multi-source cite

Pattern: `(wiki:Page, agot-pov-NN)` — combining a wiki page reference and a chapter reference inside a single parenthetical, separated by a comma. Not a parser-friendly form; the architecture allows two adjacent parentheticals or a single citation, not a comma-list.

**Count:** sampled instances:

- `characters/godwyn.node.md` line 29: `(wiki:Godwyn, cite_ref-Ragot32)` — also wrong because `cite_ref-Ragot32` should be `Godwyn.cite_ref-Ragot32`.
- `characters/cayn.node.md` line 33: `(wiki:Cayn, agot-eddard-14)` — comma-joined.
- `characters/donal-noye.node.md` line 37: `(wiki:Donal_Noye, agot-jon-03)` — comma-joined.
- `characters/jaime-lannister.node.md`, `characters/cersei-lannister.node.md`, etc. — similar pattern.

Total occurrences of `\(wiki:[^.)]+ [^.)]+\)` (which catches comma-or-space inside cite): **147 across 76 nodes**. Not all are comma-joined; some are spaces inside multi-token aliases like `(wiki:Bronze Fury)` — but those would also be malformed (page names use underscores). A mix.

### 3.4 HIGH: Multi-cite_ref chained with comma

Pattern: `(wiki:Page.cite_ref-A, cite_ref-B, cite_ref-C)` — multiple cite_refs joined inside a single parenthetical without repeating the `Page.` prefix.

- `characters/lemore.node.md` line 34: `(wiki:Lemore.cite_ref-Radwd14, cite_ref-Radwd18, cite_ref-Radwd22)` — three cite_refs collapsed.
- `characters/tyrion-lannister.node.md` line 56: `(wiki:Tyrion_Lannister.cite_ref-Rasos70, cite_ref-Rasos77)` — two cite_refs collapsed.

The parser-friendly form would be three separate parentheticals: `(wiki:Lemore.cite_ref-Radwd14)(wiki:Lemore.cite_ref-Radwd18)(wiki:Lemore.cite_ref-Radwd22)`.

**Count:** at least a dozen instances; not exhaustively counted.

### 3.5 MED: `cite: track_b_row.relationships.<field>` verbose form

Pattern: edge bullets cite as `(cite: track_b_row.relationships.Allegiances)` rather than the documented `(track_b: Allegiances)`. Two casing variants (lower and upper) coexist.

**Count:**
- `cite: track_b_row.relationships.<lowercase>` — **354 occurrences across 104 nodes**
- `cite: track_b_row.relationships.<Uppercase>` — **624 occurrences across 120 nodes**
- Total verbose-form occurrences: ~978 across ~223 nodes

Examples:
- `characters/tess.node.md` line 33: `(cite: track_b_row.relationships.allegiance, qualifier: forcibly)` — lowercase
- `characters/kennet-maester.node.md` line 28: `(cite: track_b_row.relationships.allegiances)` — lowercase, also note plural mismatch with parser field `allegiance`
- `houses/house-darke.node.md` line 37: `(cite: track_b_row.relationships.Region)` — uppercase
- `_conflicts/luwin-...node.md` line 45: `(cite: track_b_row.relationships.Allegiances)` — uppercase
- `characters/jon-snow.node.md` line 60: `(cite: track_b_row.relationships.allegiances)` — lowercase
- `characters/tyrion-lannister.node.md` line 70: `(cite: track_b_row.relationships.Titles, qualifier: formerly)` — uppercase

**Pattern interpretation:** This appears to be a third cite-format that emerged from agent-synthesized Stage 1 nodes. It's interpretable (the `relationships.X` path matches the in-memory infobox structure) but is not the documented `(track_b: Field)` shorthand. The casing inconsistency reveals two distinct agent-prompt drift events; the documented parser uses Title-Case keys (`Allegiance`, `Spouse`, `Father`).

---

## Category 4: track_b field-name drift

Beyond the format drift in 3.5 above, there are direct lowercase `(track_b: <field>)` cites:

**Count:** 8 occurrences across 8 nodes.

- `characters/lemore.node.md` line 22: `(track_b: aliases)` — lowercase. Parser field is `Alias`/`Aliases` per architecture.md.
- `characters/eddard-stark.node.md` line 76: `(track_b: books)` — lowercase. Parser field is `Books` (which is a non-edge metadata source per architecture.md).
- `characters/elaena-targaryen.node.md` line 22: `(track_b: aliases)` — lowercase
- `characters/rodrik-stark-son-of-beron.node.md` line 18: `(track_b: aliases)` — lowercase
- `characters/sansa-stark.node.md` line 22: `(track_b: aliases)` — lowercase
- `characters/lady.node.md` line 22: `(track_b: aliases)` — lowercase
- `characters/illyrio-mopatis.node.md` line 36: `(track_b: aliases)` — lowercase
- `houses/house-dayne.node.md` — `(track_b: aliases)` (similar pattern)

Also worth noting: many nodes use `(track_b: Field1, Field2)` — multi-field combined cites (242 occurrences across 192 nodes). Examples: `(track_b: Born, Died, Buried)`, `(track_b: Father, Mother)`. These are not in the documented format (should be one cite per field) but they are interpretable. **MED severity** — flag as drift, not as broken.

Specifically `(track_b: Lover)` vs `(track_b: Lovers)` casing/plural drift exists in places where the wiki infobox has both singular and plural variants of the field. Parser maps both to `LOVER_OF`, so this is interpretable but inconsistent.

---

## Category 5: citation noise (URL-encoded gibberish in cite_refs)

User flagged: `(wiki:Faith_of_the_Seven.cite_ref-Radwd5.7B.7B.7B3.7D.7D.7D.7B.7B.7B4.7D.7D.7D_79-2)` style cite_refs.

**Finding: NOT parser noise — these are real wiki anchor IDs.**

Verification: spot-checked the same anchor ID in `sources/wiki/_raw/Last_dragon.json`, `sources/wiki/_raw/Vermithor.json`, `sources/wiki/_raw/Faith_of_the_Seven.json`. The `.7B.7B.7B3.7D.7D.7D.7B.7B.7B4.7D.7D.7D` substring is the URL-encoded form of `{{{3}}}{{{4}}}` — a MediaWiki template parameter substitution that the wiki engine left unsubstituted in the cite_ref anchor ID. The Stage 3 prose-extractor preserved these verbatim, which is the **correct behavior** because the IDs do resolve in the live wiki HTML when prefixed with `#`.

**Count:** ~3,400 cite_refs across ~250+ nodes contain the `.7B.7B.7B...7D.7D.7D` pattern. They are visually ugly but functionally valid.

**Severity LOW.** No parser change required for correctness. A future cosmetic pass could optionally normalize `.7B.7B.7B3.7D.7D.7D.7B.7B.7B4.7D.7D.7D` → `_t34` or similar shorthand to improve readability, but this would be a non-substantive refactor (the wiki anchors would have to be normalized in lockstep with whatever indexes them).

A separate sub-class — bare-numeric cite_refs without book prefix — also exists:

- Pattern: `(wiki:Page.cite_ref-N)` where N is a plain integer with no book code (e.g. `cite_ref-116`, `cite_ref-18`, `cite_ref-121`).
- **Count:** 225 occurrences across 172 nodes.
- These are wiki anchors for footnotes that the wiki author didn't tag with an `R{book}` prefix. They're real anchor IDs (verified in `Vermithor.json`) but they don't encode book/chapter information. They'll appear as gaps in any future first_available backfill that depends on cite_ref book signals. **Severity LOW for citation hygiene; MED for future first_available backfill.**

---

## Stage 1 vs Stage 3 citation density

### Method

Sampled 30 Stage 1 (`v1`) nodes and 30 Stage 3 (`v1-python`) nodes with comparable prose length (Narrative Arc + Origins + Description sections). Counted `(wiki:...)`, `(track_b:...)`, and `(agot-...)` parenthetical cites per non-empty narrative paragraph.

### Findings

| Pass origin | Median cites per narrative paragraph | Style | Coverage |
|-------------|--------------------------------------|-------|----------|
| Stage 3 deterministic (`pass2-wiki-deterministic`) | 1.5 | Inline `(wiki:Page.cite_ref-Rxxx.7B...7D...)` at every claim, often multiple per sentence | Near-100% — every wiki `<sup>` is preserved |
| Stage 1 agent-synthesized (`pass2-wiki`) | 0.5 | Bracketing `(wiki:Page)` per paragraph; `(track_b: Field)` for infobox-derived facts | Coarser — one cite often covers a multi-claim run |

The gap is roughly **3:1 in favor of Stage 3 density**. Stage 1 nodes are not "uncited" — most paragraphs do close with a wiki cite — but the cite is generic (`(wiki:House_Mallister)`) rather than anchored to the specific footnote that supports the claim. This makes per-claim provenance tracing impossible for Stage 1 nodes; the reader has to take the agent's word that the bracketing wiki page actually contained that fact.

### Stage 3-style cites have a downside

The verbatim wiki anchor IDs (with `.7B.7B.7B...7D.7D.7D` URL-encoded MediaWiki template fragments) are unusable as human-readable refs. They resolve only by string-matching against the live wiki HTML. For LLM-readable retrieval this is fine; for human grep-and-jump it is not.

### Recommendation: which Stage 1 nodes need Stage-3 re-emission?

**Tier-1 candidates for re-emission (high-value, dense agent prose, sparse cites):**

These are Stage 1 nodes about major characters where the agent prose is canonical-feeling but cite density is below 1.0 cites per narrative paragraph:

- `characters/jon-snow.node.md` — 5 narrative paragraphs, 5 cites all `(wiki:Jon_Snow)` generic
- `characters/eddard-stark.node.md` — multi-paragraph Narrative Arc with one bracketing cite per paragraph
- `characters/tyrion-lannister.node.md` — has some `cite_ref-Ragot42`-style anchored cites (better than most Stage 1) but still mostly generic
- `characters/jaime-lannister.node.md`
- `characters/cersei-lannister.node.md`
- `characters/sansa-stark.node.md`
- `characters/catelyn-stark.node.md`
- `characters/rickard-stark.node.md`
- `characters/edmure-tully.node.md`
- `characters/brynden-tully.node.md`

**Tier-2 candidates: house pages that mix wiki + Pass 1 cites poorly:**

- `houses/house-mallister.node.md` (cited example — mid-paragraph claims uncited)
- `houses/house-darke.node.md` (mid-section uncited cross-reference)
- `houses/house-darklyn.node.md` (`(wiki:Raffc9)` malformed cite)
- `houses/house-tarly.node.md`
- `houses/house-redwyne.node.md`

**Tier-3: minor characters / locations with already-thin Stage 1 prose** — leave as is. The cost of re-emission likely exceeds the value when the Stage 1 node has only one or two narrative claims.

**Caveat on re-emission:** Stage 3 deterministic prose is generated by extracting wiki HTML wholesale, which produces verbose, multi-paragraph content (see `vermithor.node.md` — 8 paragraphs of Origins prose). Stage 1 agent prose is intentionally synthesized to be tight and focused on what matters. Re-emission converts Stage 1's editorial judgment into Stage 3's wiki-literal reproduction — a substantive content change, not just a cite-density fix. Worth raising with Matt before mass re-emission.

---

## Summary

The graph's citation hygiene falls into two regimes: Stage 3 deterministic nodes (3,385 of 4,290) inherit dense, anchor-level cites directly from wiki HTML and have effectively zero missing-cite issues — every claim traces back to a specific wiki footnote, even if the anchor IDs look ugly with URL-encoded MediaWiki template noise. Stage 1 agent-synthesized nodes (905 of 4,290) cite at paragraph-bracket granularity rather than claim-level, and exhibit five distinct format-drift classes (bare cite_ref-as-page, comma-joined multi-cite, verbose `track_b_row.relationships` form, casing variants, multi-field combined cites) that affect roughly 1,500 cite occurrences across ~330 nodes. The "URL-encoded gibberish" the user flagged is verified-real wiki anchor IDs, not parser noise, and should not be treated as a defect.

The most actionable findings: the 11 `(wiki:R{book}{N})` bare-cite_ref pages, the 2 chapter-numberless `(agot-eddard)` / `(agot-sansa)` quotes in `pycelle.node.md`, and the 8 lowercase `(track_b: aliases)` cites — together about 25 specific malformed cites that a small cleanup pass could fix without judgment calls. The verbose `track_b_row.relationships.X` form and its 978 occurrences is a documentation gap rather than a true defect — either canonicalize the architecture to permit it, or run a regex rewriter over the affected nodes.

## Recommended actions

1. **Fix the 11 `(wiki:R{book}{N})` bare cite_refs.** These are unambiguous bugs — they refer to pages that don't exist. Each one needs an agent or a manual inspector to find what page the cite was meant to anchor to. Batch this with the architecture's vocabulary lock for cite formats.
2. **Fix the 2 chapter-numberless AGOT cites in `pycelle.node.md`.** Identify which chapter each Pycelle quote came from and append the number.
3. **Decide on `track_b_row.relationships.<field>` verbose form**: either document it as a permitted alias in `reference/architecture.md`, or rewrite ~978 occurrences via deterministic regex to `(track_b: <Field>)` canonical form.
4. **Lowercase `(track_b: <field>)` rewrite**: 8 occurrences need title-casing — trivial regex fix.
5. **Decide on multi-cite parentheticals**: `(wiki:Page.cite_ref-A, cite_ref-B, cite_ref-C)` and `(wiki:Page, agot-pov-NN)` need a doc decision. Either document them as supported or rewrite to multiple adjacent parentheticals.
6. **Pass-1 backfill watch**: the 9 non-AGOT chapter cites in 6 nodes will resolve automatically once Pass 1 ACOK/ASOS/AFFC/ADWD completes. Re-run this audit at that time.
7. **Stage 1 re-emission audit**: when bandwidth permits, evaluate whether the 10 Tier-1 candidate Stage 1 nodes should be re-emitted via the Stage 3 path, recognizing that re-emission converts agent editorial prose into wiki-literal reproduction (a substantive change, not just cite densification).
8. **Concrete missing-cite scan**: write a small Python tool that flags sentences ending in `.` not followed within the same paragraph by a parenthetical citation. Use it to surface claims-missing-cites at corpus scale (this audit can only sample).
9. **Bare-numeric `cite_ref-N` (225 occurrences across 172 nodes)** — track these as a future-first_available-backfill blocker, not a citation hygiene issue. Wiki authors omitted the `R{book}` prefix; the cites resolve in the wiki HTML but contribute no book/chapter signal.
