# Wiki Pass 2 — Canonical Pipeline (v3, 2026-04-27 — Session 26)

> **This is the canonical reference for Wiki Pass 2.** Stage 1 (core, 37 buckets, agent-driven) is complete and promoted. Stage 2 (review) is complete. **Stage 3 (secondary, 472 buckets) is now complete — fully Python-driven, no LLM agent involved. 3,314 new nodes promoted to `graph/nodes/`.**
>
> v3 supersedes v2's "Stage 3b agent for prose-fill" design. Reasoning: the wiki HTML already contains the prose; a deterministic Python extractor produces it $0/14sec instead of $70/6h. The single-writer-per-file invariant (skeleton owned by Python, prose owned by Python, final node owned by promoter) eliminates the agent-paraphrases-skeleton failure mode entirely.

---

## Default rule: Python before Agent

**Whenever a deterministic Python step can produce part of the output, it runs first.** Agents only do what genuinely requires reasoning (cross-page adjudication, cross-identity detection, contradiction analysis). This applies to Pass 2 and to future passes.

The 37 core nodes from Stage 1 had a 5.83 edges/node mean — that yield is mostly from infobox fields, which are deterministic data. Running an LLM to extract them from 3,000+ secondary pages would have been wasted cost. The wiki encodes a lot of structure "for free" via infoboxes AND via section-headed prose; both can be harvested deterministically.

---

## Pipeline overview (Stage 3 — as actually built)

```
Priority script (one-time, mechanical labeling)               [scripts/wiki-pass2-prioritize.py]
       │
       │  writes priority.tier_a + priority.tier_b + priority.tier_c onto each bucket manifest
       ▼
Stage 3a: Python deterministic skeleton emission              [scripts/wiki-pass2-emit-deterministic.py]
       │  Reads infobox-data.jsonl + page-index.jsonl
       │  Emits skeleton/<slug>.node.md for ALL Tier A + Tier B pages
       │  Frontmatter + thin ## Identity + full ## Edges (from infobox)
       │  $0 cost, ~14 seconds for 3,315 pages
       ▼
Stage 3b: Python deterministic prose extraction               [scripts/wiki-pass2-extract-prose.py]
       │  Reads sources/wiki/_raw/<Page>.json (cached HTML)
       │  Maps wiki h2 sections to schema headings via static table
       │  Preserves h3 subheadings (book boundaries, chronological subsections)
       │  Translates <sup id="cite_ref-..."> → (wiki:Page.cite_ref-X)
       │  Emits prose/<slug>.prose.md (omitted if no mapped sections)
       │  $0 cost, ~14 seconds for all pages
       ▼
Stage 3-promote: Python concatenation + atomic-rename         [scripts/wiki-pass2-promote.py]
       │  For each Tier A + Tier B page:
       │    final_bytes = skeleton_bytes + "\n" + prose_bytes (or skeleton-only if no prose)
       │    type → graph/nodes/<type-dir>/<slug>.node.md (atomic-rename)
       │    Conflict-detect: byte-equal skip, byte-different → _conflicts/
       │  $0 cost, ~1 second for 3,315 pages
       ▼
Stage 3c: Post-emission audit cleanup                         [audit agents + targeted re-promotion]
       │  Read-only audits surface emission-time bugs (date-bleed, type-fallback, malformed YAML, etc.)
       │  Parser fixes go upstream (wiki-infobox-parser.py + emit-deterministic.py)
       │  Re-promotion fixes affected nodes only via scripts/wiki-pass2-repromote-targeted-*.py
       │  Distinct from Stage 4: Stage 3c is corrective (fixes existing emissions);
       │                        Stage 4 is additive (discovers new edges from prose).
       │  See working/audits/ for dated audit reports.
       ▼
Stage 4 (FUTURE — agent-driven, additive): Prose-derived edge discovery
       │  Cross-page edges (Reek=Theon SAME_AS, etc.)
       │  Contradiction surfacing (wiki vs Pass 1)
       │  Cross-identity detection
       │  See progress/continue-prompts/2026-04-27-wiki-pass2-stage4-edge-discovery.md
```

### Stage 3a/3b/3c vs Stage 4 — corrective vs additive boundary

The original Stage 4 plan conflated two different kinds of work: (a) fixing what Stage 3 didn't emit cleanly, and (b) discovering new edges from prose narrative. These have different shapes and risks; treating them separately keeps the pipeline tractable.

**Stage 3a/3b** (DONE) — deterministic skeleton + prose emission. Single-writer-per-file. $0 cost.

**Stage 3c** (CORRECTIVE — in progress whenever audits surface emission bugs) — read-only audits identify systematic emission errors; parser fixes go upstream; targeted re-promotion fixes affected nodes only. Examples from Session 27:
- Type-classifier `place.location` fallback bug → 14 nodes mistyped → parser fix + re-promote
- Religion-field bleed (regions becoming religion edge targets) → 4 nodes → parser fix + re-promote
- BORN_AT/DIED_AT date-bleed → ~1,200 nodes → parser fix + re-promote
- Dragon mistyping (`character.human` → `character.dragon`) → 19 nodes → parser fix + re-promote
- `*-guards` policy decision (faction not house) → 6 nodes → parser fix + re-promote

**Stage 4** (ADDITIVE — pending) — prose-derived edge discovery via hybrid Python + agent pipeline. Cross-identity detection (Reek=Theon SAME_AS), narrative perception edges, edges only inferable from prose context. Never modifies Stage 3a/3b deterministic emissions; emits to `prose-edges/<slug>.edges.jsonl` siblings.

**Key architectural pattern:** single-writer-per-file. Each artifact has exactly one writer; the promoter is the only process that combines them. See `reference/architecture.md` § "Artifact Formats by Consumer".

---

## Tier definitions (set by the priority script)

| Tier | Definition | Action |
|------|------------|--------|
| **A** | Page name appears in any Pass 1 raw entity list **OR** has ≥5 chapter cite_refs | Stage 3a Python skeleton, then Stage 3b agent prose-fill |
| **B** | Has infobox in `infobox-data.jsonl` but does NOT meet Tier A criteria | Stage 3a Python skeleton only. No agent. Done. |
| **C** | No infobox AND no chapter cite_refs | Defer. Label `has_infobox: false` and `page_kind` (enum: redirect / disambiguation / list_article / year_article / stub / entity). Tier A/B do NOT get `page_kind` — adding `entity` to obvious entities adds zero query value. |

**Hard rule:** Never drop anything from sources. Tier C pages stay; redirects, stubs, lists stay. Source data is read-only and additive-only.

---

## Stage 3a — Python deterministic emission

**Script:** `scripts/wiki-pass2-emit-deterministic.py` (to be built)

**Inputs:**
- `working/wiki-parsed/infobox-data.jsonl` (5,279 rows)
- `working/wiki-parsed/page-index.jsonl` (17,657 rows)
- Per-bucket `manifest.json` (with `priority_tier` field set by priority script)

**Output per page:** `working/wiki-pass2/<bucket_id>/tmp/<slug>.node.md`

**Frontmatter (deterministic):**
- `name` — wiki page name
- `type` — from `entity_type_guess` (infobox-field signature)
- `slug` — kebab-case, `[a-z0-9-]` only
- `aliases` — from `track_b_row.aliases`
- `confidence` — `tier-2` (default for secondary; can be overridden by manifest's `tier_default`)
- `wiki_source` — canonical URL
- `bucket_id`, `prompt_version: v1-python`, `node_version: 1`, `pass_origin: pass2-wiki-deterministic`
- **`first_available` is NOT emitted.** Field is owned by post-release backfill script.

**Body (deterministic):**
- `## Identity` — one line: `<Name> is a <type> from <wiki_source>.`
- `## Edges` — full infobox-derived edge list using the mapping in `reference/architecture.md` § "Wiki Infobox Fields → Edge Type Mapping". Every edge cites `(track_b: <field>)`.

That's it for Tier B. Tier A nodes get the same skeleton then go to Stage 3b for prose enrichment.

---

## Mid-stage review (RAN ONCE — Session 26, verdict CLEAN)

**Purpose:** One-time quality gate on Stage 3a Python emission before Stage 3b ran.

**What it did:** A general-purpose agent spot-checked stratified samples of Stage 3a output for edge correctness, type-guess correctness, citation format, slug validity. Cross-checked emitted `## Edges` against `track_b_row.relationships`.

**Verdict (Session 26):** 0 HIGH issues. 4 MED issues, all upstream of Stage 3a (parser bugs, triage misclassifications) — already on `working/todos.md` or deferrable. Stage 3a output approved.

**This step does not run again** unless Stage 3a is re-emitted with schema changes. It was a one-time gate, not a recurring stage.

---

## Stage 3b — Python deterministic prose extraction

**Script:** `scripts/wiki-pass2-extract-prose.py`

**Inputs per page:**
- `sources/wiki/_raw/<Page_Name>.json` — cached MediaWiki-rendered HTML (one-time crawl, never re-fetched)
- Per-bucket `manifest.json` — uses `priority.tier_a[]` + `priority.tier_b[]` to enumerate pages
- Per-bucket `skeleton/<slug>.node.md` (Stage 3a output) — used to pin the slug for prose filename matching

**Output per page:** `working/wiki-pass2/<bucket_id>/prose/<slug>.prose.md` (omitted if zero mapped sections)

**H2 → schema heading mapping (deterministic, case-insensitive):**

| Wiki h2 | Schema heading |
|---------|----------------|
| `Appearance and Character`, `Character and Appearance` | `## Appearances & Description` |
| `History`, `Background`, `Prelude`, `Legend` | `## Origins` |
| `Culture` | `## Culture` |
| `Organization`, `Structure` | `## Organization` |
| `Layout`, `City` | `## Appearances & Description` |
| `Recent Events`, `Battle`, `Siege`, `Synopsis` | `## Narrative Arc` |
| `Aftermath` | `## Aftermath` |
| `Quotes`, `Quotes by <X>`, `Quotes about <X>` | `## Quotes` (preserves h2 as h3 subheading) |
| `Family`, `Behind the Scenes`, `References`, `External Links`, `Theories`, `Historical Members`, `Notable Members`, `Members`, `Household`, `Game of Thrones`, `Character List` | SKIP (publication meta, redundant with edges, structured lists, or non-prose) |

**H3 preservation (critical):** every `<h3>` inside a mapped section is preserved as `### Subheading` in the prose output. This protects book-boundary structure (`### A Game of Thrones`, `### A Clash of Kings`, etc. inside `## Narrative Arc`) and chronological subsections (`### Youth`, `### Robert's Rebellion`, etc. inside `## Origins`) for future spoiler-gating.

**HTML → markdown conversion:**
- `<sup id="cite_ref-NAME-N">` → `(wiki:<PageName>.cite_ref-NAME-N)` inline
- `<a href="/index.php/Page" title="...">text</a>` → `[text](wiki:Page)` inline
- `<b>`/`<strong>` → `**text**`; `<i>`/`<em>` → `*text*`
- `<ul>`/`<ol>`/`<blockquote>`/`<dl><dd>` → standard markdown forms
- HTML entities decoded; whitespace normalized
- Tables, images, infoboxes stripped (already captured in skeleton)

**Stats summary:** `working/wiki-parsed/stage3b-extraction-summary.json`. Latest run (Session 26): 2,988 prose files emitted from 3,315 candidate pages (90.1% hit rate); 327 pages had zero mappable sections (Tier-B redirects, infobox-only stubs, member-list-only pages); mean word count 294, median 105. Top remaining unmapped sections (long tail): `Legacy` (20), structured-list variants (~36 across `Character List` / `Places and terms mentioned` / `Household`).

---

## Stage 3-promote — Python concatenation + atomic-rename

**Script:** `scripts/wiki-pass2-promote.py`

**Inputs per page:**
- `working/wiki-pass2/<bucket_id>/skeleton/<slug>.node.md` (required)
- `working/wiki-pass2/<bucket_id>/prose/<slug>.prose.md` (optional — concat if exists, else skeleton-only)

**Concatenation:** `final_bytes = skeleton_bytes + b"\n" + prose_bytes` (when prose exists), else `skeleton_bytes` verbatim. The single `\n` produces one blank line between `## Edges` (end of skeleton) and `## Origins` (start of prose).

**Type resolution:** reads `type:` from skeleton frontmatter, maps via `TYPE_DIR_MAP` (replicates `wiki-pass2.sh`'s map plus all leaf types: `character.human` → `characters`, `organization.house` → `houses`, `event.battle` → `events`, etc.). Unknown types route to `graph/nodes/_unclassified/`.

**Conflict detection per page:**
1. If destination doesn't exist → atomic-rename from staging tmp.
2. If destination exists and bytes match → skip silently (idempotent re-run).
3. If destination exists and bytes differ → write to `graph/nodes/_conflicts/<slug>-<bucket_id>-<timestamp>.node.md`, append to `working/wiki-pass2/conflicts.jsonl`.

**Stats summary:** `working/wiki-parsed/stage3-promote-summary.json`. Latest run (Session 26): 472 secondary buckets processed, 3,314 new nodes promoted, 0 conflicts, 1 unclassified (`battle-of-the-blackwater-song` — `type='unknown'`). Wall-clock: 0.84 seconds.

**Final graph state after Session 26:** 4,169 nodes total (855 from Stage 1 agent path + 3,314 from Stage 3 Python path) across `characters/` (3,361), `houses/` (315), `events/` (242), `locations/` (151), `titles/` (79), `factions/` (21).

---

## Bucket preservation — hard rule

After every stage, preserve:
- `working/wiki-pass2/<bucket_id>/bucket_input.json` (Stage 1 buckets only — Stage 3 buckets don't have these)
- `working/wiki-pass2/<bucket_id>/manifest.json`
- `working/wiki-pass2/<bucket_id>/skeleton/<slug>.node.md` files (Stage 3a output)
- `working/wiki-pass2/<bucket_id>/prose/<slug>.prose.md` files (Stage 3b output)
- `working/wiki-pass2/<bucket_id>/tmp/<slug>.node.md` files (Stage 1 only — empty for Stage 3 buckets)
- `working/wiki-pass2/<bucket_id>/validator-report.json` (Stage 1 only)

**Reasons:**
- Stage 4 (edge discovery) reads skeleton + prose to find prose-derived edges.
- Re-runs and audits need the artifacts intact.
- Post-release `first_available` backfill needs the bundles' track_b rows + h3 book boundaries preserved in prose.

If anything in the launcher or scripts looks like it deletes `skeleton/`, `prose/`, `bucket_input.json`, or `manifest.json` after promotion — stop and ask.

---

## What's NOT in scope here

- **Stage 4: prose-derived edge discovery.** Cross-page, prose-extracted edges. Sequential to Stage 3, never parallel. See `progress/continue-prompts/2026-04-27-wiki-pass2-stage4-edge-discovery.md`.
- **Spoiler gating.** Deferred; `first_available` backfill happens post-release via dedicated script.
- **Pass 3+ (voice, foreshadowing, theory, discovery).** Separate workstreams.

---

## Reference

- `reference/architecture.md` § "Artifact Formats by Consumer" — the single-writer-per-file invariant + the per-stage artifact taxonomy
- `reference/architecture.md` § "Wiki Infobox Fields → Edge Type Mapping" — the locked deterministic edge vocabulary Stage 3a uses
- `working/runbooks/wiki-pass2-orchestration.md` — orchestration mechanics (Stage 1 launcher, validator, conflicts) — still applies to Stage 1 re-runs
- `working/runbooks/wiki-pass2-tier-handoff.md` — Stage 1/2 history; Stage 3 description there is superseded
- `working/scratch-design-review-stage3b.md` — the Session 26 design review that drove the Stage 3b agent → Python redesign
- `progress/continue-prompts/2026-04-27-wiki-pass2-stage4-edge-discovery.md` — Stage 4 skeleton (NOT YET DESIGNED — placeholder)
- `.claude/agents/wiki-ingester.md` — Stage 1 agent prompt (Stage 3 does not use an agent; this prompt is preserved for Stage 1 re-runs only)
