# Wiki Pass 2 — Orchestration Runbook

> **STATUS — PARTIALLY SUPERSEDED (2026-04-27).** The "agent emits everything" pipeline assumed throughout this doc is replaced for Stage 3 onward by the **Python-first / Agent-prose-only** pipeline in `wiki-pass2-pipeline.md`. The orchestration mechanics here (bundle structure, validator architecture, conflict handling, bucket fingerprints) still apply. The agent's role narrows: Stage 3a Python emits frontmatter + edges deterministically; Stage 3b agent fills prose body only and is forbidden from emitting edges or modifying frontmatter. Read `wiki-pass2-pipeline.md` first; use this doc as the orchestration-mechanics reference.
>
> **Mode:** Design document. PLAN-ONLY output of session triggered by `progress/continue-prompts/2026-04-25-track-b-orchestration-planning.md`.
>
> **Scope:** How to run Pass 2 (wiki → graph nodes) at scale across the 17,657 cached wiki pages. Sibling design to `scripts/extract.sh` / `weirwood`.
>
> **Out of scope:** The wiki-ingester agent prompt itself (downstream); Pass 3+; relational-DB design.

---

## 0. Premise

Pass 2 is the **agentic** layer of wiki ingestion. It sits on top of Track B (deterministic Python parser, see `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`) and produces structured node files in `graph/nodes/`.

Two layers, distinct concerns:

| Layer | Mechanism | Output | Volume |
|-------|-----------|--------|--------|
| Track B (deterministic) | One Python script, no agent | `working/wiki-parsed/infobox-data.jsonl` (one row per page) + per-page cite_ref tables | All ~17,657 pages — single batch |
| Pass 2 (agentic) | Claude agents over Track B output + raw HTML + Pass 1 extractions | `graph/nodes/{type}/<entity>.node.md` files | A curated subset — see §1 triage |

This runbook is about Pass 2. Track B is its prerequisite and its primary input.

---

## 1. Work Decomposition

### 1.1 Deterministic vs. agentic — boundary

**Deterministic (Track B + extensions, no agent):**
- Infobox field → edge tuple (Father, Mother, Spouse, Allegiance, Overlord, Seat, Founder, …).
- `cite_ref-R{book}{n}` regex → per-page first-appearance map.
- "Books" infobox `(POV)/(appears)/(mentioned)` → book-level fallback for `first_available`.
- Aliases from infobox.
- Entity-type *suggestion* from infobox-field signature (Father+Mother+Spouse → `character.human`, Sigil+Seat+Words → `organization.house`, etc.).
- Triage signals: page length, infobox richness, cite_ref count, wiki category set.
- **L1 page-index (mandatory deliverable)** — Track B emits `working/wiki-parsed/page-index.jsonl`, one row per page with `{page, entity_type_guess, categories[], cite_ref_books[], has_infobox, byte_size}`. This is the queryable index that triage (L2), per-bucket manifests (L3), and any later review-tier query build on. Re-querying any tier greps this file rather than re-parsing 17k HTML blobs. Without L1, every later layer re-derives categories from raw HTML — non-starter at this scale.

**Agentic (Claude, Pass 2):**
- **Promote/skip decision** when triage is ambiguous.
- **Disambiguation** (Aegon I vs. II vs. V; Brandon-the-Builder vs. Brandon-Stark-the-elder vs. Bran).
- **Prose synthesis** — turn a 12k-word wiki page into a ≤500-word node body without losing canonical facts.
- **Confidence-tier assignment per claim** when the wiki page mixes Tier 1 canon, Tier 2 inference, and Tier 3 fan consensus (common on character pages with long "speculation" sections).
- **Cross-reference with Pass 1** — does Pass 1 disagree with the wiki? If so, mark conflict for curation queue rather than overwriting.
- **Retroactive-significance flagging** — `significance_unlocked` is a judgment call, not a regex.

**Rule for the boundary:** if a Python regex over a single page can produce the field reliably (validation against a hand-graded sample shows ≥95%), it lives in Track B. Anything requiring narrative reading or cross-page judgment is agentic.

### 1.2 Triage as a separate stage

Pass 2 is preceded by a **triage stage** that is itself mostly deterministic:

```
Track B output → Triage → Pass 2 buckets
```

Triage answers: *which pages get the agent treatment, and in what bucket?* Inputs are deterministic signals (length, infobox, cite_refs, categories, overlap with Pass 1 raw entity lists). Output is a manifest:

```
working/wiki-parsed/triage-manifest.jsonl
{
  "page": "Eddard_Stark",
  "tier": "core",        # core | secondary | reference-only | skip
  "bucket": "characters-stark",
  "reason": "POV character, 78 cite_refs, full infobox, in Pass 1 raw entity list"
}
```

Tiers (working definitions — confirm in implementation):
- **core** — POV characters, major houses, named locations appearing in Pass 1, primary artifacts. Processed first.
- **secondary** — Named entities with infobox + ≥3 cite_refs OR appearing in Pass 1. Processed after core. **Never skipped — only postponed.** A bucket that doesn't fit a session's budget stays on the queue for the next session; it does not get dropped.
- **reference-only** — Pages whose deterministic data (relationships, first_available) is captured by Track B but that don't need an agentic node body. Stored as a stub node, no agent run.
- **skip** — Stubs, redirects, meta-pages, OOC pages. Logged and ignored.
- **theory / speculative** — Pages whose body is mostly fan inference or speculation (e.g., long "Quotes by/about" + "Speculation" sections). Tagged at triage so a later theory-focused phase can find them quickly without re-scanning.

**Triage is not single-session.** Triage itself is incremental: pages can move tiers as Pass 1 progresses (a character not in AGOT extractions today may appear in ASOS later, promoting them from `secondary` to `core`). The triage manifest is *re-runnable* and additive — a later run upgrades tier assignments without losing prior bucket history.

#### Bucket disjointness — each page belongs to exactly one bucket

The data model only works under this rule. The validator's `expected_nodes` check, the coherence checker's no-duplicate-name rule, and the launcher's atomic `tmp/ → graph/nodes/` rename all assume a page maps to exactly one `bucket_id`. Cross-bucket *references* (e.g., the Lannister character bucket needing to link to House Lannister in a houses bucket) flow through edges, never by listing the same page in two manifests.

Auto-derivation (§1.3) will produce multi-category candidates for ~3-8% of pages. Tiebreakers, applied in order:

1. **Most-specific category wins.** "House Stark members" beats "Northmen" beats "Characters."
2. **First-listed wiki category wins.** When specificity ties, the order of `<a href="/Category:...">` links in the cached HTML decides.
3. **Alphabetical bucket id.** Final tiebreaker for adversarial cases.

Triage records the assignment reason on the page's row as `bucket_assignment_reason: tiebreaker-{1|2|3}` so a future audit can grep auto-assigned pages without re-running triage.

#### 1.2.1 Categories come from HTML, not on-disk subdirectories

The cached wiki layout in `sources/wiki/{characters,locations,events,artifacts}/` is mostly empty — only `houses/` is populated (633 of 17,576 pages). 16,943 pages live in `_uncategorized/`, including Eddard_Stark, Jon_Snow, Winterfell, Ghost — exactly the entities the example buckets in §1.3 (`characters-stark`, `direwolves`, `north-locations`) draw from. The on-disk subdirectory layout is **not** the source of category truth.

Categories come from the cached HTML itself: the `<a href="/Category:...">` links that appear in the navigation strip at the bottom of every wiki page. Track B parses these into the `categories[]` field of the L1 page-index. Triage and bucket derivation read `page-index.jsonl`; they never list `sources/wiki/<subdir>/` to enumerate entity types.

`sources/wiki/_category-reports/` is empty and not used by any orchestration step. Earlier drafts referenced it as a triage signal — those references have been removed.

Beyond the four/five processing tiers, every page also gets one or more **internal working categories** stored alongside its triage row. These are *not* the entity-type taxonomy from architecture.md — they are operational tags for later traversal:

- `has-theory-section`, `has-speculation`, `has-tv-only-content`, `large-page` (>5k words), `stub-rich-infobox` (small body but full infobox), `disambiguation-page`, `pre-agot` (D&E / pre-series), `post-canon-only` (Fire&Blood, TWOIAF), `cross-cited-by-N-pages`, `mentioned-in-pass1`.

Working categories let a future phase grep for `has-theory-section` to find Pass 5 inputs without re-classifying 17k pages, or grep `large-page` to find candidates where summarization quality should be spot-checked, etc. They are written once during triage and left alone.

This split matters because it lets the bulk of pages (the long tail) get value from Track B without paying agent cost, and lets later phases find what they need without re-deriving classifications.

**Why this over alternatives:** Naïvely running the agent over all 17,657 pages is wasteful — most pages are 1-paragraph stubs with no narrative content. A pure category-based filter (e.g., "only Characters") is too coarse — many useful pages live in `_uncategorized/`. Triage gives explicit buckets driven by signals we can already compute, with the bar adjustable in one place.

### 1.3 Batch unit

Within a tier, the natural batch unit is **per-bucket**, where a bucket is a thematic+size-bounded grouping. Candidates:

- House-clusters: `House Stark + sworn houses + bannermen` (~25 pages).
- Region-clusters: `The North (region + locations)` (~80 pages).
- Character-clusters by house or culture: `Lannister characters` (~60 pages).
- Singleton large pages: very long character pages (Tyrion, Daenerys, Jon) get their own bucket — context budget alone justifies isolation.
- Topical: `Faith of the Seven (religion + clergy + sacred sites)`.

Size target per bucket: 10-30 pages, total content ≤ ~150k input tokens so a single agent can hold the bucket in working context with cache reuse.

#### Bucket derivation v1 — auto-draft, hand-edit, then `--accept`

Auto-derive a draft from the L1 page-index, then hand-edit before launch. The v1 rule is intentionally simple:

- **One bucket per wiki category with 5-30 members.**
- **Categories with >30 members are split alphabetically** (`stark-bannermen-a-m`, `stark-bannermen-n-z`).
- **Categories with <5 members are merged into a sibling bucket** (parent category, or geographically/thematically adjacent — auto-derivation picks the smallest sibling that keeps the merged bucket under 30 members).
- **Pages with no usable categories** fall into a `singletons-<entity-type-guess>` bucket and stay there until reviewed.
- **Multi-category pages** are assigned per the disjointness tiebreakers in §1.2.

Output: `working/wiki-pass2/draft-buckets.jsonl`, one row per bucket with `{bucket_id, source_categories[], pages[], total_bytes, page_count, tier_default, oversized}`. The user reviews the draft (diff with prior run if re-running), then re-invokes triage with `--accept` to commit per-bucket manifests at `working/wiki-pass2/<bucket>/manifest.json`.

Re-running triage **without** `--accept` regenerates the draft only; nothing in `working/wiki-pass2/<bucket>/manifest.json` mutates. This makes triage iteration safe — Matt can re-run as many drafts as he likes before committing.

Refine the v1 rule after the first scaled run if seam quality is poor. Until then, the rule lives in `scripts/wiki-pass2-triage.py` as constants at the top of the file.

#### Bucket size budget — gate, not just target

Verified against cache: `House_Stark.json` alone is ~646 KB (~160k tokens) — exceeding the 150k-token bucket target on its own. `Jon_Snow.json` is 305 KB (~76k); `Tyrion_Lannister.json` is 261 KB (~65k). Page-size variance across the cache is 12-700×. The target is enforced as a **gate**, not an aspiration:

- Triage computes `total_bytes` per bucket from the L1 page-index (`byte_size` field).
- Buckets where the *largest single page* exceeds 600 KB raw HTML (~150k tokens) are flagged `oversized: true` in the draft.
- Oversized singleton-mega-pages get their own **bucket-of-one** with `chunk_strategy: section-by-section` recorded in the manifest. The wiki-ingester prompt is responsible for handling chunked input on these; the validator does not enforce single-pass synthesis when `chunk_strategy != single-pass`.
- The triage script never auto-merges oversized pages with siblings. The user must explicitly `--accept` a bucket-of-one — this is intentional friction, since chunked synthesis costs more per page and benefits from a moment of human review.

### 1.4 Confidence-tier defaults

The wiki-ingester agent assigns a confidence tier per claim. To anchor those assignments, triage tags each bucket with a `tier_default` derived from a category-driven mapping. The agent uses this as the starting point and overrides per-claim only with explicit justification.

v1 mapping (regex over wiki category names):

| Wiki category pattern | `tier_default` | Notes |
|------------------------|----------------|-------|
| `*Theory*`, `*Speculation*`, `*Fan theory*` | Tier 4 | Plausible speculation. Per-claim Tier 1 requires a chapter citation. |
| `*Battle*`, `*Character*`, `*House*`, `*Location*`, `*Castle*`, `*Region*`, `*City*`, `*Kingdom*` | Tier 1 | Verified canon. Per-claim Tier 2-4 requires the source page to mark the claim with a "Speculation" subsection. |
| `*Religion*`, `*Magic*`, `*Prophecy*` | Tier 2 | Strong inference. The magic system is explicitly partial in canon, so most pages mix Tier 1 facts (rituals, named practitioners) with Tier 2 inferences (mechanism). |
| `*Cadet branch*`, `*Bastard*`, `*Order*` | Tier 1 | Generally well-attested via houses pages and infoboxes. |
| `*Quote*`, `*Song*`, `*Saying*` | Tier 1 | Direct text content. |
| (no matching category) | Tier 2 | Default for uncategorized. The wiki-ingester is expected to call this out per claim. |

The mapping lives in `scripts/wiki-pass2-triage.py` as a regex table at the top of the file (sibling to the v1 derivation rule from §1.3). When the table changes, this section must change with it — they are explicitly coupled. The wiki-ingester agent prompt references this section for the per-claim override protocol.

Refine after the first scaled run if the defaults consistently miscalibrate against spot-check expectations.

---

## 2. Concurrency Model

### 2.1 Mirror weirwood, not deviate

The extraction pipeline's concurrency is:
- Multiple iTerm tabs (parallelism unit = terminal).
- Each tab runs `claude -p --dangerously-skip-permissions` once per chapter, sequentially, in a "wave" of 5.
- Cross-tab coordination via filesystem (`is_complete` check), not IPC.
- Soft-stop via `/tmp/extraction-stop` marker.
- Per-book stats CSV per pass-version.

**Pass 2 inherits all of this.** A "wave" for wiki = a sequence of buckets a single tab processes. A "chapter" for wiki = a bucket (not an individual page — see §1.3 rationale). The launcher script is `scripts/wiki-pass2.sh` (sibling to `extract.sh`), exposed via a `wiki` subcommand on the existing `weirwood` zsh function (not a separate binary).

Mapping:

| Extraction (Pass 1)         | Wiki Pass 2                    |
|-----------------------------|--------------------------------|
| Book (`agot`, `acok`, …)    | Tier (`core`, `secondary`)     |
| Chapter file (`agot-bran-01`) | Bucket (`stark-bannermen`)   |
| Wave (5 chapters)           | Wave (3-5 buckets)             |
| `extractions/mechanical/<book>/` | `graph/nodes/` + `working/wiki-pass2/<bucket>/manifest.json` |
| `extraction-stats-{book}-pass1-v3.csv` | `wiki-pass2-stats-{tier}-v1.csv` |

Wave size of 3-5 *buckets* (not pages) is smaller than Pass 1's 5-chapter waves because each bucket is a multi-page agentic call. Buckets are the chapter-equivalent.

#### Wave formation

Waves are formed at launch time from the incomplete-bucket queue, not assigned at triage. The launcher walks the queue in **tier order** (`core` first, then `secondary`); within a tier, by `bucket_id` alphabetical order. Wave size is 3-5 buckets per terminal tab. Cross-tier mixing happens only when a tier finishes mid-wave: the partial wave is filled from the next tier's queue rather than being launched short.

Rationale: tier order encodes priority; alphabetical order within tier makes wave assignments reproducible across launches and easy to reason about during incident response. Mid-wave cross-tier filling is cheap (one extra row in the wave's ledger) and avoids idle tabs at tier boundaries.

#### 2.1.1 Agent input contract

The agent receives a single file: `working/wiki-pass2/<bucket>/bucket_input.json`, composed by the launcher before it invokes `claude -p`. The agent never reads the raw cache, the Track B JSONL, or Pass 1 extractions directly — everything it needs is pre-staged.

Schema:

```json
{
  "bucket_id": "characters-stark",
  "tier": "core",
  "tier_default": "tier-1",
  "prompt_version": "v1",
  "chunk_strategy": "single-pass",
  "pages": [
    {
      "page": "Eddard_Stark",
      "raw_html_path": "sources/wiki/_raw/Eddard_Stark.json",
      "track_b_row": { /* full row from infobox-data.jsonl */ },
      "page_index_row": { /* full row from page-index.jsonl */ },
      "pass1_mentions": [
        {"chapter": "agot-eddard-01", "line": 42, "context": "..."}
      ]
    }
  ]
}
```

Why launcher-composed:
- **Reproducible.** Same bucket + same prompt version + same Track B output → byte-identical input bundle. Resumption is deterministic.
- **Scoped.** Agent cannot accidentally pull in pages outside its bucket; the validator's "no orphan references" rule depends on this.
- **Cache-friendly.** Each agent invocation gets a clean, pre-staged context that the prompt cache can re-use across re-runs of the same bucket.

`chunk_strategy: section-by-section` (set on oversized buckets per §1.3) instructs the agent to process each page's HTML one section at a time and synthesize incrementally rather than holding the full page in working context.

### 2.2 Subagents inside a parent agent — when?

**Default: no subagents.** One Claude invocation per bucket, fresh context. Same model as extraction (use `claude -p`, no orchestrator agent).

**Exception worth considering (don't pre-decide):** disambiguation buckets where multiple candidate entities share a name and need cross-comparison. There a parent dispatching short subagent calls per candidate may pay off. Defer until we hit the case in practice.

**Why no parent-orchestrator pattern by default:** The terminal-tab model already gives parallelism. Subagents inside a parent burn parent context for queue management — for our workload that's pure overhead. The tab model also makes resumption trivial (filesystem state, no in-memory queue to recover).

### 2.3 Tab count

Same heuristic as extraction: enough to keep API throughput high but few enough to stay under per-org rate limits. Start at 2 tabs, scale to 4 if stats show idle headroom and no rate-limit halts. The launcher accepts `-t <terminals> -w <waves_per_terminal>` identical to `extract.sh`.

---

## 3. Drift Prevention

Wiki ingestion has a higher drift risk than chapter extraction because:
- Inputs are 10× more numerous (17k vs. 344).
- Page length variance is 100× (stub → 15k words).
- Confidence-tier judgment is real (vs. Pass 1 where everything is Tier 1 by default).
- Cross-page coherence matters (House Stark on `Eddard_Stark.json` should match House Stark on `Robb_Stark.json`).

### 3.1 Schema validator (gate)

A Python script `scripts/wiki-pass2-validator.py` runs after each bucket completes. **The validator is invoked by the launcher (`wiki-pass2.sh::cmd_run`) after `claude -p` returns — never by the agent.** The agent only writes to `tmp/`; atomic rename from `tmp/` into `graph/nodes/` happens inside the launcher, contingent on validator pass. This separation keeps the agent prompt small (no file-move logic) and keeps the gate enforceable from outside the agent's control flow.

Validates every emitted `*.node.md`:

- Frontmatter required fields present: `name`, `type`, `first_available`, `confidence`, `wiki_source`.
- `type` is in the architecture.md hierarchy.
- `first_available` parses to a known book/chapter.
- All claims in the body cite a source (chapter ref, wiki ref, or Pass 1 extraction).
- No claim with `confidence < tier-1` is unflagged.

Bucket fails validation → wave continues but bucket is logged `status=validation-failed`, agent transcript saved, **no nodes are written** (atomic rename from `tmp/` only on validation pass). Curation queue gets the diff.

**Why atomic rename:** Partial node files on disk would corrupt downstream queries. The validator is the gate; until it passes, output stays in `tmp/`.

### 3.2 Spot-check sampling

Every Nth bucket (configurable, default 10), the runbook mandates a manual spot-check: pick 3 random emitted nodes, diff against the source wiki page, log discrepancies in `working/wiki-pass2/spot-checks.md`. Three consecutive bad spot-checks → halt the run, flag for prompt review.

**Why required, not optional:** Pass 1 had a manual schema review at the end of AGOT v3 that surfaced the 4-vs-12 category gap. Pass 2 is too long-running to defer review to the end; the in-line spot-check forces continuous calibration.

### 3.3 Cross-bucket coherence check

After all buckets in a tier complete, run `scripts/wiki-pass2-coherence.py`:
- For every entity referenced as an edge target, the target node exists or is in the deferred queue.
- House membership: every character with `Allegiance: House X` resolves to the same `house-stark.node.md`.
- Aliases unique: no two nodes claim the same `name` field unless explicitly marked `SAME_AS`.

Failures here are usually disambiguation bugs and go to curation queue, not auto-resolved.

### 3.4 Hash-fingerprinted inputs

Each bucket manifest stores a SHA-256 of (a) the agent prompt version, (b) the bucket's input page set, (c) the Track B JSONL row hashes. A re-run with the same fingerprint short-circuits to "already done." A change to the prompt invalidates *all* buckets that used it — explicit, not silent.

---

## 4. Process Metadata Schema

### 4.1 CSV file location and shape

Path: `working/extraction-stats/wiki-pass2-stats-{tier}-v{N}.csv` — same directory as Pass 1 stats so existing tooling (`scripts/extraction-status.sh` analog) can transfer. One CSV per tier per prompt version.

Columns (mirrors `extraction-stats-{book}-pass1-v3.csv` shape; extensions marked **NEW**):

```
bucket,tier,wave,status,start_time,end_time,duration_s,
input_tokens,cache_creation_tokens,cache_read_tokens,output_tokens,total_tokens,
cost_usd,
pages_in_bucket,           # NEW — number of wiki pages processed in this bucket
nodes_emitted,             # NEW — count of *.node.md files written
validation_status,         # NEW — pass | fail | partial
notes                      # NEW — short free-text (rate-limit, validator failure, etc.)
```

The first 13 columns are byte-for-byte identical to the extraction CSV — drop-in compatible with any roll-up reporting that already exists. The four wiki-specific columns are appended at the end so column-positional readers ignoring trailing fields keep working.

### 4.2 Status codes

Mirror extract.sh:

| Code | Meaning |
|------|---------|
| `pending` | Manifest exists, bucket has not yet run this version |
| `in-progress` | Agent invocation underway (set by launcher before `claude -p`, cleared on completion or orphan recovery — see §5.4) |
| `ok` | Bucket completed and validated |
| `fail` | Agent invocation errored (network, claude CLI failure) |
| `skip-done` | Manifest fingerprint matches; skipped |
| `skip-rate-limit` | Bucket was queued when rate limit hit, never ran |
| `validation-failed` | Agent succeeded but validator rejected output |
| `partial` | NEW — some pages in bucket succeeded, some failed gracefully (or reconciliation queued only the missing/new pages — see §5.1.1) |
| `version-stale` | NEW — fingerprint mismatch from prompt-version bump; awaits explicit `reset` per §5.1.1 case 4 |

### 4.3 Per-bucket transcript log

Same pattern as `/tmp/extraction-{ch}.log`: every bucket's full agent output kept in `/tmp/wiki-pass2-{bucket}.log` for the duration of the run. Successful bucket logs are purged on next launch; failed bucket logs are copied to `working/wiki-pass2/failures/<bucket>-<timestamp>.log` for post-mortem.

### 4.3.1 Status output

`weirwood wiki status [tier]` produces an ASCII table — analog of `weirwood agot` (status). One row per bucket in tier order, then `bucket_id` order:

```
bucket                      tier      wave  status              nodes  last_run
-------------------------   --------  ----  ------------------  -----  --------------------
characters-stark            core      1     ok                  18     2026-04-26 14:22:01
direwolves                  core      1     validation-failed   0      2026-04-26 14:25:13
houses-tully                core      2     pending             —      —
locations-the-north         core      2     in-progress         5      2026-04-26 14:31:05
…
```

Roll-up footer (always shown, even when filtered to a single tier):

```
core:        14/47 buckets ok, 2 failed, 31 pending
secondary:    0/120 buckets ok, 0 failed, 120 pending
total cost so far:     $42.18
conflicts:             3   (working/wiki-pass2/conflicts.jsonl)
contradictions:        7   (working/wiki-pass2/pass1-contradictions.jsonl)
unresolved questions: 12   (working/wiki-pass2/questions-for-matt.jsonl)
```

Without `[tier]`, both tiers print. Without any state on disk yet (first ever invocation), the command prints "no triage manifest found — run `weirwood wiki triage` first" and exits 0.

---

## 5. Resumption — On-Disk State Machine

### 5.0 Bucket discovery — two-tier truth

On launch, the launcher discovers buckets from `working/wiki-pass2/*/manifest.json` first (canonical state). The triage manifest at `working/wiki-parsed/triage-manifest.jsonl` is consulted only for buckets without on-disk manifests; missing manifests are generated before the wave starts.

**Two-tier truth model:**

| Source | What it owns | Mutated by |
|--------|--------------|------------|
| `working/wiki-parsed/triage-manifest.jsonl` | **Membership** — which pages belong to which bucket, the tier assignment, the tiebreaker reason | `scripts/wiki-pass2-triage.py --accept` only |
| `working/wiki-pass2/<bucket>/manifest.json` | **Status** — where in the lifecycle the bucket is (`pending|in-progress|complete|failed|partial`) | The launcher only |

A re-run of triage adds or updates membership but never overwrites a bucket's status manifest. Status changes flow only through the launcher. If membership and status disagree (a re-triage adds a page to a `complete` bucket), the launcher downgrades that manifest to `partial` per §5.1.1 and queues the new pages.

### 5.1 Truth source: filesystem

A bucket is **complete** iff:
1. `graph/nodes/<type>/<entity>.node.md` exists for every promoted entity in the bucket's manifest, AND
2. `working/wiki-pass2/<bucket>/manifest.json` has `status: complete` and matching fingerprint.

The launcher discovers incomplete buckets the same way `extract.sh::find_incomplete_waves` discovers incomplete waves: scan filesystem, derive state, no DB.

**Routing rule:** `<type>` in the path above is the architecture.md *parent type* (Character, Place, Organization, Concept, Object, Event, Species, Title), lowercased and pluralized to match the existing `graph/nodes/` directory tree from CLAUDE.md (`characters/`, `places/` or `locations/`, `houses/`, `factions/`, `religions/`, `artifacts/`, `prophecies/`, `theories/`, `texts/`, `battles/`, `wars/`, `species/`, `titles/`). The fine-grained leaf type (`character.direwolf`, `place.region`, `organization.faction`) is recorded in the node's frontmatter `type:` field, **not** in the directory path.

Examples:

- `Eddard_Stark` (`character.human`) → `graph/nodes/characters/eddard-stark.node.md`
- `Ghost` (`character.direwolf`) → `graph/nodes/characters/ghost.node.md`
- `Winterfell` (`place.location`) → `graph/nodes/locations/winterfell.node.md`
- `House_Stark` (`organization.house`) → `graph/nodes/houses/house-stark.node.md`
- `Faceless_Men` (`organization.faction`) → `graph/nodes/factions/faceless-men.node.md`

This matches the existing directory convention in CLAUDE.md and avoids per-leaf-type subdirectories that would multiply on every taxonomy expansion.

#### 5.1.1 Reconciliation rules — filesystem is canonical

The two truth sources from §5.0 (manifest JSON + on-disk node files) can disagree — e.g., the user manually deletes `graph/nodes/characters/eddard-stark.node.md` while the manifest still says `complete`, or a re-triage extends a bucket's `expected_nodes` after the bucket already ran. The reconciliation rule:

**Filesystem is canonical.** On launch, before wave formation, the launcher walks every bucket marked `complete`:

1. Check that every entry in `expected_nodes` exists on disk under the routing rule from §5.1.
2. **Missing nodes →** manifest auto-downgraded to `partial`. Only the missing entities are queued for re-run; existing nodes are left alone.
3. **All present but fingerprint mismatch — input-change source** (e.g., re-triage added new pages, or a re-crawl changed Track B input rows): manifest auto-downgraded to `partial`; only the new/changed pages are queued. Existing nodes stay.
4. **All present but fingerprint mismatch — prompt-version source** (the agent prompt was bumped): launcher does NOT auto-re-run. It logs the bucket as `version-stale` in stats and refuses to touch it. The user must explicitly invoke `wiki-pass2.sh reset --version vN` (per §5.4) to archive the v_old output before a v_new run can proceed. This avoids silently mixing v1 + v2 output in the same `graph/nodes/` tree.
5. **All present, fingerprint matches** → manifest stays `complete`; bucket skipped this launch.

Distinguishing input-change vs. prompt-version mismatch matters because the user expects re-triage to "just work" (case 3), but a prompt bump is a graph-wide event that deserves explicit acknowledgment (case 4).

Reconciliation never mutates `graph/nodes/`. Only manifest JSON is rewritten. The reconciliation pass is logged so a stats roll-up can flag "N buckets downgraded from complete to partial this launch" or "N buckets version-stale, awaiting reset" — both signal something the user should look at.

### 5.2 Bucket manifest schema

```json
{
  "bucket_id": "characters-stark",
  "tier": "core",
  "fingerprint": "<sha256>",
  "prompt_version": "v1",
  "input_pages": ["Eddard_Stark", "Catelyn_Stark", "Robb_Stark", ...],
  "expected_nodes": ["eddard-stark.node.md", ...],
  "status": "pending|in-progress|complete|failed",
  "started_at": null,
  "completed_at": null,
  "validation_report": "path/to/validator-output.json"
}
```

Manifests are generated up-front from triage output and live in `working/wiki-pass2/<bucket>/manifest.json`. The launcher mutates them; agents do not.

#### Per-bucket on-disk layout

```
working/wiki-pass2/<bucket>/
├── manifest.json              # bucket lifecycle state (canonical schema above)
├── bucket_input.json          # agent input bundle (composed by launcher; see §2.1.1)
├── tmp/                       # in-flight node output, awaiting the validator gate
│   └── <entity>.node.md
└── validator-report.json      # last validator run output (overwritten each run)
```

Failure logs go to `working/wiki-pass2/failures/<bucket>-<timestamp>.log` (per §4.3) — outside the per-bucket directory, so a `reset` of one bucket's state does not drop its prior failure logs.

#### `update_worklog()` target line shape

The launcher's `update_worklog()` (mirror of `extract.sh::update_worklog`) targets these checklist lines, seeded in `worklog.md` under "Extraction Pipeline":

```
- [ ] Wiki Pass 2 v1 — core ({done}/{total} buckets)
- [ ] Wiki Pass 2 v1 — secondary ({done}/{total} buckets)
```

The matcher regex anchors on `Wiki Pass 2 v{N} — {tier}` and rewrites the trailing `({done}/{total} buckets)`. Total counts get filled in once triage commits the per-bucket manifests; until then both lines read `(0/0 buckets)`. When all buckets in a tier are `ok`, the line flips to `[x]` and the trailing count freezes at `(N/N buckets)`.

If a future Pass 2 v2 ships, two new lines (`Wiki Pass 2 v2 — core …`) get seeded; the v1 lines stay (frozen as historical record), matching the worklog convention used by Pass 1 v1/v2/v3.

### 5.3 Soft-stop

Identical to extraction: `/tmp/wiki-pass2-stop` (distinct from extraction's stop file so the two can coexist). Tabs check between buckets, not mid-bucket. Marker cleared automatically on next launch.

### 5.4 Re-run semantics

- Re-running with same prompt version + same Track B output → no-ops on complete buckets, processes incomplete only.
- Prompt version bump → all buckets at old version invalidated (manifest fingerprint mismatch). User must run `wiki-pass2.sh reset --version v{N}` (see below) to archive existing v{N} output before re-launch.
- Track B output change (new wiki crawl, parser fix) → buckets touching changed pages invalidate, rest stand.

#### Orphan `in-progress` manifests

A `kill -9` mid-bucket (or a hard machine reboot) leaves the manifest at `status: in-progress` and partial node files in `tmp/`. The fingerprint covers prompt + inputs, not in-flight state — so without an explicit rule, the launcher would either re-run (wasteful) or refuse (blocking).

Rule: on launch, before wave formation, every `in-progress` manifest is checked against `started_at`:

- **`started_at` older than 60 minutes** → assume the prior process is dead. `tmp/*.node.md` is wiped, manifest downgraded to `pending`, bucket re-queued. Logged as orphan recovery in stats.
- **`started_at` within 60 minutes** → assume another tab owns it; skipped this launch (prevents racing tabs).

Threshold is configurable via `--orphan-threshold-min N` on `wiki-pass2.sh run` / `launch`.

For pathological cases — manifest stuck `in-progress` but `tmp/` contains partial work the user wants to inspect rather than discard — an explicit subcommand:

```
wiki-pass2.sh unstick <bucket>
```

Wipes `tmp/`, resets manifest to `pending`. Refuses to run if `tmp/` contains node files newer than `started_at` (sign of in-flight work); user adds `--force` to override.

#### Reset command

Re-running with a bumped prompt version invalidates all prior buckets. At Pass 2 scale (~5,000-10,000 nodes, ~100-200 bucket manifests), manual `mv` is a footgun — easy to forget bucket manifests, leave stale fingerprints, mix v1+v2 nodes in one tree. The launcher provides:

```
wiki-pass2.sh reset --version v1 [--archive-dir <path>]
```

Behavior:

- Identifies every `*.node.md` under `graph/nodes/` whose frontmatter `prompt_version` matches `v1`. Moves them to `graph/archives/wiki-pass2-v1-<timestamp>/` (or the user-supplied `--archive-dir`), preserving the parent-type subdirectory layout.
- Identifies every bucket whose `manifest.json` has `prompt_version: v1`. Moves the per-bucket directory (`manifest.json`, `bucket_input.json`, `tmp/`, `validator-report.json`) into the same archive directory under `wiki-pass2-state/`.
- Leaves untouched: `working/wiki-parsed/` (Track B output is still valid input), `working/wiki-pass2/conflicts.jsonl`, `working/wiki-pass2/pass1-contradictions.jsonl`, `working/wiki-pass2/questions-for-matt.jsonl`, `working/wiki-pass2/failures/` (audit trail must survive resets), `graph/nodes/_conflicts/` (same reason).
- Prints a summary: files moved, bucket count, archive path, what was preserved.
- Refuses to run without `--version`; refuses if the archive directory already exists (caller must rename / move it first to avoid silent merging).
- `--dry-run` prints the same summary without moving anything.

Pass 1's archival pattern (`extractions/archives/agot-v2/`) was a manual `mv`. Pass 2's volume requires automation; this subcommand is the automation.

---

## 6. Failure Modes

| Failure | Detection | Action |
|---------|-----------|--------|
| Rate limit (rejected) | JSON `status:rejected` + `rateLimitType` (same as extract.sh) | Halt remaining buckets in tab; mark `skip-rate-limit`; tab exits cleanly |
| Claude CLI error / network | Non-zero exit from `claude -p` | Mark bucket `fail`, save transcript, continue to next bucket |
| Malformed wiki page (unparseable) | Track B already flagged at parse time | Skip at triage, never reaches Pass 2 |
| Schema validation failure | `wiki-pass2-validator.py` returns non-zero | Mark `validation-failed`, hold output in `tmp/`, continue wave |
| Disambiguation ambiguity | Agent emits node with `confidence: tier-3` + `disputed: true` field | Validator passes it; node lands in `graph/nodes/` but is also referenced from `curation/candidates.md` for Matt review |
| Cross-bucket conflict (two nodes claim same name) | `wiki-pass2-coherence.py` after tier complete | Both nodes flagged; curation queue entry; no auto-resolve |
| Empty / stub output (agent over-summarized) | Validator: body length < threshold | `validation-failed`; transcript reviewed manually |
| Spot-check failure (3 in a row) | Manual review log | **Halt run.** Stop file created, prompt review demanded before relaunch |
| Hallucinated relationship not in Track B JSONL | Validator cross-checks every edge against Track B output | `validation-failed` if claimed edge has no Track B trace and no chapter citation |

### Halt-vs-skip-vs-continue rules

- **Halt the entire run** (set stop file): rate-limit reset >2h away; spot-check threshold breach; coherence check finds systemic failure (>5% of nodes).
- **Skip-and-continue:** any single bucket failure that doesn't pattern-match a systemic issue. Curation queue + log.
- **Mark and continue with output:** disambiguation flagged with `disputed: true`. The graph absorbs the uncertainty rather than blocking on it.

The principle inherited from extraction: **never silently corrupt output**. Better to skip a bucket and fix it later than write half-validated nodes that pollute the graph.

---

## 6.5 Walk-Away Safety

Pass 2 is meant to run unattended for long stretches. The orchestration must guarantee no work is silently lost or overwritten while Matt is away.

**Hard rules — implementation must enforce all of these:**

- **No overwrite of existing node files.** Every agent write goes to `working/wiki-pass2/<bucket>/tmp/`. Promotion to `graph/nodes/` is atomic-rename, and only if (a) the destination does not exist OR (b) the manifest fingerprint matches and the new content is byte-equivalent. Mismatched fingerprint with existing node → write to `graph/nodes/_conflicts/<entity>-<bucket>-<timestamp>.node.md` and append a row to `working/wiki-pass2/conflicts.jsonl`. Never silently replace.
- **No destructive re-run.** A re-launch never deletes prior nodes, prior manifests, prior stats, or prior failure logs. "Reset" is an explicit, separate command — never the default of any launcher subcommand.
- **No partial output on disk.** The validator gate from §3.1 is the only path from `tmp/` to `graph/nodes/`. A killed process leaves files in `tmp/` (recoverable) but never half-validated nodes in the graph proper.
- **All decisions traced.** Every node carries `wiki_source`, `bucket_id`, and `prompt_version` in frontmatter. A user reading any node six months later can reproduce its lineage.
- **Session-killable mid-run.** Soft-stop (`/tmp/wiki-pass2-stop`) plus the per-bucket atomicity above means a `weirwood wiki stop` followed by closing the laptop loses at most one bucket's in-flight `tmp/` content (which is auto-discarded next launch via fingerprint mismatch).

**Question queue for async sessions:**

When a bucket or wave surfaces a question that needs Matt's input but isn't blocking, the agent appends a JSONL row to `working/wiki-pass2/questions-for-matt.jsonl`. The run does not stop. Matt drains the queue at his pace; resolved questions migrate to the curation queue or back into prompt updates. This converts stop-start interruptions into batched async review.

Schema (one JSON object per line):

```json
{
  "question_id": "q-2026-04-26-001",
  "bucket_id": "characters-stark",
  "page": "Eddard_Stark",
  "type": "disambiguation",
  "text": "Which 'Brandon Stark' does this passage refer to — the Builder, the Elder, or Bran?",
  "blocking": false,
  "asked_at": "2026-04-26T14:22:01Z",
  "resolved_at": null,
  "resolution": null
}
```

`type` is one of `disambiguation | tier | promotion | other`. The launcher exposes `wiki-pass2.sh questions [--unresolved|--bucket <id>|--type <type>]` for filtered review; a `format` subcommand renders unresolved questions as prose if Matt prefers reading. JSONL beats markdown here because at Pass 2 scale (potentially 5+ questions per bucket × 200 buckets = 1,000 entries) the queue needs structured filtering and a drain-state field — grep alone can't tell resolved from open.

**`_conflicts/` consumer — the conflicts log:**

Every conflict-write under the "no overwrite" rule appends a row to `working/wiki-pass2/conflicts.jsonl`:

```json
{
  "page": "Eddard_Stark",
  "bucket_id": "characters-stark",
  "conflict_path": "graph/nodes/_conflicts/eddard-stark-characters-stark-2026-04-26T14-22-01.node.md",
  "existing_node_path": "graph/nodes/characters/eddard-stark.node.md",
  "existing_prompt_version": "v1",
  "new_prompt_version": "v1",
  "fingerprint_match": false,
  "byte_equivalent": false,
  "detected_at": "2026-04-26T14:22:01Z"
}
```

Without this log, conflict files would accumulate silently in `_conflicts/` — exactly the failure mode the no-overwrite rule is meant to prevent. The log gives `wiki-pass2.sh status` a count and gives a future `wiki-pass2.sh conflicts` subcommand a structured input for prose rendering. The log itself is never auto-pruned; it survives `reset` (audit trail).

**Provisional-by-default node/edge formalization:**

Pass 1 is not complete on 4/5 books. The graph nodes Pass 2 produces are explicitly **provisional v1**: they may be revised after Pass 1 finishes ASOS/AFFC/ADWD and surfaces facts the wiki was wrong or silent about. Implementation implications:

- Every node carries `node_version: 1` in frontmatter. Schema review after Pass 1 completion may bump to `v2`.
- Edge tuples carry `pass_origin: pass2-wiki` so a later pass building edges from chapter text can supersede them without ambiguity.
- The validator does *not* enforce that a node's claims appear in any chapter extraction — Pass 1 is incomplete, so absence is not evidence of error. Cross-check with Pass 1 is a *signal* (logged), not a *gate*.

The contradiction signal is logged to `working/wiki-pass2/pass1-contradictions.jsonl`, one row per detected contradiction:

```json
{
  "node": "eddard-stark.node.md",
  "claim": "Eddard had four children acknowledged before AGOT.",
  "wiki_evidence": "Infobox 'Issue' field lists Robb, Sansa, Arya, Bran, Rickon",
  "pass1_evidence": "agot-eddard-01.extraction.md: Jon Snow present at family dinner, addressed as son",
  "detected_at": "2026-04-26T14:22:01Z",
  "resolved_at": null,
  "resolution": null
}
```

The v2 schema-review session reads this file as direct input — it is the channel by which "Pass 1 is now richer than Pass 2 thought" feeds back into a v2 wiki re-pass. `wiki-pass2.sh status` surfaces the row count. The log survives `reset` (audit trail).

Without this channel, the "all decisions traced" hard rule above silently breaks: contradiction signals would be detectable but unwritten, and the v2 trigger condition ("Pass 1 finished, contradictions accumulated") would have no input.

This wiggle room is intentional: lock in too tightly now and we re-run Pass 2 later. Lock in nothing and the graph is unusable. The middle path is "ship usable v1, mark it as v1, plan for v2."

---

## 7. Storage Decision (Revisit)

### 7.1 Decision: stay on markdown + JSONL + CSV. No relational DB.

| Layer | Format | Why |
|-------|--------|-----|
| Track B parser output | JSONL (`infobox-data.jsonl`) | Streamable, append-friendly, agent-readable line-by-line, no schema migration cost when parser evolves |
| Triage manifests | JSONL (`triage-manifest.jsonl`) + per-bucket JSON | Same |
| Graph nodes | Markdown with YAML frontmatter (`*.node.md`) | Portable, version-controllable, native Claude input, human-readable |
| Process metadata | CSV (`wiki-pass2-stats-*.csv`) | Mirrors Pass 1, drop-in for existing tooling |
| Edge tuples | JSONL (`graph/edges/edges.jsonl`) — to confirm in implementation | Same reasoning as Track B output |

### 7.2 Pass-2-specific access patterns evaluated

The continue prompt asks: do Pass 2's actual access patterns demand a DB?

| Access pattern | Markdown+JSONL handling | Painful? |
|----------------|------------------------|----------|
| "Find all nodes referencing House Stark" | Grep `graph/nodes/` | No — fast at this scale |
| "Resolve `Eddard_Stark` → node file" | Slug map: `working/wiki-parsed/slug-to-node.json` | No |
| "Find first appearance of entity X" | Read its node frontmatter | No |
| "All edges of type SWORN_TO involving House X" | Grep on edges JSONL | No at our edge count |
| "All characters serving House X across multiple hops" | **Painful** — needs traversal | **Yes — but Pass 2 doesn't need this.** This is a Pass 3+ / query-time concern |
| "All Stark descendants in N generations" | Same — multi-hop | Same — not a Pass 2 access pattern |

**Conclusion:** every Pass 2 *write-time* access pattern is satisfied by JSONL + grep + a small slug map. The painful patterns are *read-time* graph queries that come later. JSONL → graph DB migration cost is small (a single ETL script), so we deferring DB until those queries actually exist is cheap reversibility.

### 7.3 Trigger to revisit

Adopt a graph DB if **any** of:
- A query in a downstream pass (3+) needs ≥2-hop traversal and wall-time exceeds ~5s on grep.
- The edges JSONL exceeds ~500k rows and full-table scan becomes a bottleneck.
- A consumer (UI, MCP server, fan-fic generator) requires real-time queries.

When that happens: SQLite + recursive CTEs first (zero-infrastructure), Neo4j only if recursive CTEs aren't enough.

**Why not adopt now anyway:** infrastructure not yet free. Markdown is what every existing agent reads natively. A DB now means a dual-write story (markdown + DB) until everything migrates, and that dual-write is where bugs live.

---

## Open Questions Surfaced

These need resolution **before** implementation but not in this runbook:

1. **Subagents-in-parent vs. tabs** — default is tabs. Revisit only if disambiguation buckets prove painful.
2. ~~**Bucket curation**~~ — **CLOSED 2026-04-25.** v1 rule landed in §1.3: auto-derive from L1 page-index categories with size-based split/merge, draft → review → `--accept`. Refine after the first scaled run if seam quality is poor.
3. ~~**Confidence-tier driver**~~ — **CLOSED 2026-04-25.** v1 mapping landed in §1.4: category-regex → tier_default; agent overrides per-claim with justification. Refine after the first scaled run if defaults consistently miscalibrate.
4. **Promotion threshold** — what triage signal score promotes a page from `secondary` to `core` or `reference-only` to `secondary`? Implementation will need a concrete formula, not a hand-wave.
5. **Node body length budget** — too-short nodes lose canon, too-long nodes bloat the graph. Pick a target (e.g., 200-500 words) and enforce in validator.
6. **Curation queue surface** — where does Matt's review queue live? Likely `curation/candidates.md` already used by Pass 1, but Pass 2 could overwhelm it. May need a per-pass curation file.
7. **Wiki-cache snapshotting** — if the wiki is recrawled, Track B's output changes. Should `working/wiki-parsed/` be checkpointed under a date stamp so Pass 2 runs are reproducible?

---

## Implementation Sequence

When this runbook becomes code, the sequence is **build → review → prompt → commence → scale**, with explicit session boundaries:

1. **Track B** — Land the deterministic parser per `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md`. L1 page-index (`working/wiki-parsed/page-index.jsonl`) is mandatory.
2. **Build session — scripts only, no agent runs.** Per `progress/continue-prompts/2026-04-25-implement-wiki-pass2-orchestration.md`:
   - `scripts/wiki-pass2-triage.py` (produces `draft-buckets.jsonl`, then per-bucket manifests on `--accept`)
   - `scripts/wiki-pass2-validator.py`
   - `scripts/wiki-pass2-coherence.py`
   - `scripts/wiki-pass2.sh` (subcommands: `run`, `status`, `launch`, `check`, `reset`, `unstick`, `questions`, `triage`)
   - `scripts/weirwood.zsh` extended with `wiki` subcommand (no new file)
   - README.md updated.
   - Non-agentic verification only: validator on fixtures, triage on real cache, reset dry-run, etc. **No `claude -p` invocation.**
3. **Script-review session** — Independent fresh-agent read of the scripts. Continue prompt created at the end of the build session. Verdict + issues list before any agent run.
4. **Patch session (optional)** — Apply review patches to scripts, if needed.
5. **Wiki-ingester agent prompt session** — Write `.claude/agents/wiki-ingester.md`. Schema must match the validator. The validator is a hard contract; the prompt is written against it.
6. **Commence session — first smoke test.** Single small bucket end-to-end (e.g., `direwolves`, ~6 pages). Real `claude -p` invocation, real nodes in `graph/nodes/`. Halt and review before scaling.
7. **Schema review of smoke output.** Analog of Pass 1's AGOT v3 review. Adjust prompt or validator if needed before scaling.
8. **Run tier `core`** — Spot-check after every 10 buckets per §3.2.
9. **Run tier `secondary`** — Only after `core` is reviewed and locked.

Steps 2-4 do not invoke the agent. Step 6 is the first agent invocation. The session boundaries are intentional: each transition (build → review, review → prompt, prompt → commence) is a checkpoint where the user can halt without sunk-cost regret.

---

## Appendix: Mapping Table for Quick Reference

The shell entry point stays `weirwood`. Wiki Pass 2 is a subcommand on the same wrapper, not a sibling binary:

| Pass 1 (extract.sh) artifact | Pass 2 (wiki-pass2.sh) analog |
|------------------------------|-------------------------------|
| `weirwood agot 2 3` | `weirwood wiki core 2 3` |
| `weirwood acok` (status) | `weirwood wiki core` (status) |
| `weirwood stop` | `weirwood wiki stop` (separate stop file `/tmp/wiki-pass2-stop`) |
| `extract.sh status agot` | `wiki-pass2.sh status core` |
| `extract.sh run agot --wave 4` | `wiki-pass2.sh run core --wave 4` |
| `is_complete()` (line count + section grep) | `is_bucket_complete()` (manifest fingerprint + node files exist + validator pass) |
| `extractions/mechanical/{book}/` | `graph/nodes/` (output) + `working/wiki-pass2/{bucket}/` (state) |
| `working/extraction-stats/extraction-stats-{book}-pass1-v3.csv` | `working/extraction-stats/wiki-pass2-stats-{tier}-v1.csv` |

**README** must be updated when the wiki launcher lands: add a "Wiki Pass 2" section parallel to the existing extraction section, document `weirwood wiki ...`, the question-queue file, and the walk-away-safe behaviors.
