# Session 25 — Stage 3 Prep: Priority + Stage 3a + Edge Vocabulary Lockdown

**Date:** 2026-04-27
**Continue prompt entering session:** `progress/continue-prompts/2026-04-27-wiki-pass2-stage3-prep.md`
**Continue prompt leaving session:** `progress/continue-prompts/2026-04-27-wiki-pass2-stage3-finish.md` (NEW — see end of doc)

## What this session was

Execution-heavy with three architectural mid-course corrections. The continue prompt's nominal scope was "build the priority script + Stage 3a + mid-stage review + wiki-ingester v2 + validator update, then stop." We got ~60% of the way there before Matt called the session. The remaining 40% — full Stage 3a `--apply`, mid-stage review, wiki-ingester v2 prose-only rewrite, validator edge byte-equality enforcement — carries to the next session via a new continue prompt.

The interesting parts were not the script-building (which went smoothly via script-builder subagent) but three places we hit a sharper question and adjusted the design rather than barreling through:

1. **Tier-C `entity` promotion to Tier B** — the prioritize script's first run flagged 9 real-content pages (House Brune, House Shett, etc.) that fell into Tier C because they lacked an infobox AND lacked cite_refs. The continue prompt's tier definitions would have deferred them to Stage 4. Matt overruled: real content with no infobox is too valuable to defer; promote to Tier B, accept that the `## Edges` section will be empty for those pages.

2. **Night's Watch typed as `organization.house`** — the test bucket emission surfaced this as a 1-line note ("faithful to parser output, downstream-fixable"). Matt escalated: don't let it into the data layer at all. Triggered a full parser re-run with `ENTITY_TYPE_OVERRIDES` and an audit of the whole `organization.house` set, which surfaced 21 mistyped pages (Kingsguard, Faceless Men, Maesters, Golden Company, etc.).

3. **Edge vocabulary lock + future polish phase** — Matt asked whether the edge taxonomy was being protected from drift, and where it came from in the first place. Confirmation that it was empirically derived from wiki infobox field frequencies (not invented) was reassuring but not enough; the lock needed to be documented in 4 places so a future agent doesn't drift it. Also surfaced that "edge polish" — collapsing semantically-equivalent variants — needs to be an explicit future agent-reasoning phase, not a Stage 3a/3b concern.

## Stage 3 pipeline state at end of session

```
[priority script]   ✅ wiki-pass2-prioritize.py written, applied to 472 manifests
                      Tier A: 624, Tier B: 2,691, Tier C: 57 (all redirects)
                      Mixed-tier buckets (A+B+C all non-empty): 7
                      Tier C-entity → Tier B promotion patched
                            ↓
[Stage 3a Python]   ⚠️  wiki-pass2-emit-deterministic.py written + 1-bucket test
                      Full --apply across 472 buckets NOT YET RUN
                      Dry-run projects 3,315 skeletons (A=624 B=2,691)
                      Mean edges/skeleton: 4.60 (post vocab additions)
                            ↓
[mid-stage review]  ⏳ NOT STARTED
                            ↓
[wiki-ingester v2]  ⏳ NOT STARTED
                            ↓
[validator update]  ⏳ NOT STARTED — edge byte-equality enforcement pending
                            ↓
[Stage 3b launch]   🛑 GATE — requires Matt's explicit go-ahead
```

## Files touched

### New scripts
- `scripts/wiki-pass2-prioritize.py` (NEW, 25K) — labels every page in 472 secondary manifests with `priority_tier` (A/B/C) and (Tier C only) `page_kind`. Idempotent, dry-run-safe.
- `scripts/wiki-pass2-emit-deterministic.py` (NEW) — Stage 3a deterministic skeleton emitter. Reads infobox-data.jsonl + per-bucket priority labels. Emits `working/wiki-pass2/<bucket>/tmp/<slug>.node.md` with frontmatter + thin Identity + full `## Edges` section.

### Edited
- `scripts/wiki-infobox-parser.py` — added `ENTITY_TYPE_OVERRIDES` dict (21 page-name → `organization.faction` overrides for orders/guilds/companies that use the {{House}} infobox template); added `fathers`, `cultures`, `battles` (plural variants) to `FIELD_EDGE_MAP`; added `written by` → new `WRITTEN_BY` edge type. Module-level docstring expanded with "edge vocabulary lock" callout.
- `scripts/wiki-pass2.sh` (`cmd_run`) — reads `prior_status` before flipping bucket to `in-progress`; if prior was `fail` or `validation-failed`, `rm -rf`s `tmp/` so the bucket starts on a blank canvas. Closes a long-standing footgun.
- `reference/architecture.md` — Edge Type Mapping table gained `WRITTEN_BY` row and `Battles` plural variant note. New 6-paragraph "vocabulary lock" callout block above the table covering: parser is single source of truth, no script invents edges, currently-unmapped fields ranked by frequency, edge-polish-is-future rule, procedure for adding new edge types (architecture.md FIRST, then parser, then re-run).
- `working/wiki-parsed/{infobox-data.jsonl, page-index.jsonl, parse-stats.md}` — regenerated by parser re-run; 21 entity-type flips, 3 plural-edge additions, 1 new edge type.
- `working/wiki-pass2/*/manifest.json` — 472 secondary manifests gained `priority` field (additive).
- `working/wiki-parsed/priority-summary.json` — NEW (regenerated each `--apply` run).
- `working/wiki-pass2/houses-other-h-w/tmp/*.node.md` — 14 test-bucket skeletons emitted to verify Stage 3a script.
- `working/todos.md` — gained 4 entries under "Session 22 Followups": book-chapter-pages defer-bucket plan, vocabulary-lock note attached to "Edge taxonomy gaps", new "Edge polish phase (FUTURE)" entry, new "Non-ASCII qualifier normalization (graph layer)" entry. Existing "Launcher should auto-wipe stale tmp/" entry checked off.

### Created (continue prompts)
- `progress/continue-prompts/2026-04-27-wiki-pass2-stage3-finish.md` (NEW — handoff for next session, replaces the partly-completed stage3-prep prompt)

### Archived
- `progress/continue-prompts/2026-04-27-wiki-pass2-stage3-prep.md` → `progress/continue-prompts/archive/` (DoD ~60% complete; superseded by stage3-finish)

## Numbers worth recording

- **Stage 1 actual cost** (recap): $95.33 / 37 buckets / 855 nodes = $2.58/bucket, $0.111/node
- **Stage 3a Python cost:** local (parser run 15.8s; prioritize ~few seconds; emit ~few seconds for full corpus dry-run)
- **Stage 3b projected cost:** 624 Tier-A pages × $0.111/node = **~$70**, well under the "$200 / 2 days" guard from the continue prompt
- **Tier distribution (after Tier-C-entity promotion):** A=624 (18.5%), B=2,691 (79.8%), C=57 (1.7%)
- **Mean edges/skeleton:** 4.57 → 4.60 after adding `written by`/`fathers`/`cultures`/`battles` mappings
- **Empirical lock check:** 22 distinct edge_type values in corpus, all uppercase, all from `FIELD_EDGE_MAP`. Lock holds.
- **Tier C kind distribution:** all 57 are `redirect` (after promoting `entity` to Tier B). Cleanest possible Tier C.
- **Pages routed to `battles` mega-bucket but lost during alphabetical 30-cap split:** 335 of 349 book-chapter wiki pages. Surfaced this session, not fixed (deferred to triage-script-bug TODO).

## The three mid-course corrections in detail

### Correction 1: Tier-C-entity → Tier B promotion

**How it surfaced:** The prioritize script's first dry-run produced 624 / 2,682 / 66 across A/B/C. The Tier C breakdown was 57 redirects + 9 entity. The 9 entity pages were real-content houses/people lacking an infobox: House Brune, House Shett, House Shell, etc. The continue prompt's tier rules ("Tier C: no infobox AND no cite_refs → defer") would have left them out of Stage 3 entirely.

**Decision:** Promote them to Tier B. They get a Stage 3a Python skeleton, but `## Edges` will be empty (no infobox to mine). Tier B grew 2,682 → 2,691; Tier C dropped 66 → 57.

**Why:** "real content with no infobox is too valuable to defer." The `entity` page_kind is the catch-all; if it ever fires, it's signaling that the page is not a redirect/disambig/list/year/stub, i.e., the page has narrative content — exactly what we don't want to lose.

**Patch:** `scripts/wiki-pass2-prioritize.py:assign_priority_tier` — after `detect_page_kind`, if kind is `entity`, return `("B", None, None)` instead of `("C", "entity", None)`.

### Correction 2: 21 mistyped "houses" → `organization.faction`

**How it surfaced:** Stage 3a's dry-run stats listed `organization.house: 633`, and a single test-bucket skeleton inspection showed `Night's Watch` typed as `organization.house`. I (the agent) reported it as a 1-line side note; Matt escalated.

**Investigation:** Grepping `infobox-data.jsonl` for `entity_type = organization.house` AND page name NOT starting with `House `, surfaced 21 entries: Night's Watch, Kingsguard, Queensguard, Rainbow Guard, Faceless Men, Faith Militant, Warrior's Sons, Holy Hundred, Kingswood Brotherhood, Brotherhood of Winged Knights, Order of the Green Hand, Maesters, Alchemists' Guild, Bearded priests, Dragonkeepers, Golden Company, Windblown, Brazen Beasts, Black council, Band of Nine, City Watch of King's Landing.

**Why mistyped:** The wiki uses the `{{House}}` infobox template for these too — same HTML structure → parser's `classify_by_page_name` sees "House X" or matching infobox signature → types as `organization.house`. The parser doesn't currently distinguish based on `name.startswith("House ")` strictly; it falls through to template-based signatures.

**Decision:** Add an `ENTITY_TYPE_OVERRIDES` map in the parser. All 21 → `organization.faction`. Finer-grained split (`organization.order` for sworn brotherhoods, `organization.guild` for Maesters/Alchemists, `organization.company` for Golden Company/Windblown, etc.) DEFERRED to the future edge-polish/entity-polish review phase. Reason: more granular taxonomy is a meaningful design decision; not the right thing to make under deadline.

**Re-run cascade:** parser (~16s) → prioritize --apply (~few seconds) → emit dry-run. Confirmed `nights-watch.node.md` now shows `type: organization.faction`.

### Correction 3: Edge vocabulary lock + edge-polish-is-future

**How it surfaced:** Matt asked: "we don't want to be picking up / inventing a LOT of edges. There is a pre made list and there *should* be some sort of memory of record of a discussion where the large list of edges started, and how it was important to mostly lock it down so as to not get edges that are the same thing but phrased slightly differently."

**Investigation:** Confirmed the locked vocabulary is `reference/architecture.md` § "Wiki Infobox Fields → Edge Type Mapping" (the table) and its implementation in `scripts/wiki-infobox-parser.py:FIELD_EDGE_MAP`. The 22 edge_type values currently in the corpus all match. The lock was working.

**But:** the lock wasn't *documented* as a hard rule. A future agent (or future-Matt) could plausibly add a new edge_type to a script without going through the architecture.md table. Or could decide a Stage 3b agent should "merge equivalent edges inline" because that seems efficient.

**Decision (4-place documentation):**
1. `reference/architecture.md` — large callout block above the table covering: parser is single source of truth, no script invents edges, currently-unmapped fields list with frequencies, edge-polish-is-future rule, procedure (architecture.md FIRST → parser → re-run).
2. `scripts/wiki-infobox-parser.py` — `FIELD_EDGE_MAP` block comment expanded with "vocabulary lock for the project" framing.
3. `scripts/wiki-pass2-emit-deterministic.py` — module docstring gained "Edge vocabulary lock" section explicitly stating Stage 3a is pure pass-through.
4. `working/todos.md` — added "Edge polish phase (FUTURE)" entry: agent-reasoning phase AFTER all wiki ingestion completes. The 22 edge types may consolidate further then.

**Sub-correction:** While answering Matt's question I checked the parse-stats unmapped-fields list, found `written by` (172) was in the existing TODO but not in the map, and three plural variants (`fathers` 21, `cultures` 9, `battles` 9) were missing from the map even though their singulars were present. Added all 4 to FIELD_EDGE_MAP, re-ran parser. Mean edges/skeleton ticked 4.57 → 4.60. The system's gap-finding works: parse-stats.md auto-regenerates the unmapped-fields ranking every parser run.

## What surprised, what didn't

**Surprise:** 335 of 349 book-chapter wiki pages got dropped during the alphabetical 30-cap split of the `battles` mega-bucket. Triage misclassified them as `event.battle`, then the splitter only emitted ~270 pages across 9 splits, silently losing the rest. Only 14 ASOS chapter pages stranded in `battles-a` survived. Matt's plan: keep all 349, defer to a future bucket that may feed Track A. Captured as TODO.

**Surprise:** Mean edges/skeleton at the secondary tier (4.60) is lower than Stage 1's core (5.83). Secondary entities are slightly lighter on infobox fields, as expected — but the gap is smaller than I'd anticipated. Tier B is mostly characters with 4-5 standard kinship/allegiance edges.

**Surprise (good):** Idempotency held everywhere. Two runs of `--apply` on prioritize produced byte-identical manifests (modulo `computed_at`). emit-deterministic re-runs produced byte-identical files. The parser is similarly deterministic.

**Not surprising:** The prioritize and emit scripts came together cleanly via script-builder subagent. The hard work was the 4-place documentation of the edge-vocabulary lock, not the code.

## Process notes for future-me

1. **Don't bury parser-output bugs as 1-line notes.** "Night's Watch typed as organization.house — faithful to parser output, downstream-fixable" was technically correct but Matt rightly escalated. If a parser misclassification can be fixed in <30 min by adding an override dict, do it inline, don't defer.

2. **The system's gap-finder is `parse-stats.md`.** Every parser run regenerates the unmapped-fields ranking. When asked "are we missing edges?", read that file before speculating.

3. **Single script-builder pass is fine for mechanical scripts.** Considered splitting "pure logic spec" + "implementation" into two subagent calls per Matt's suggestion; decided against because the spec was precise and the bias risk low. Worked out.

4. **The continue prompt's DoD is the contract, not a wishlist.** This session ran ~60% of the prep prompt's DoD. Rather than push through, we paused at a clean handoff point. The next session's continue prompt is tightly scoped to the remaining 40% rather than re-stating the original full scope.

## Open questions carried to next session

- **Full Stage 3a `--apply` launch:** approved? (3,315 skeletons across 472 buckets; ~few minutes wall time; no agent cost)
- **Bucket-mixing rule for the 7 mixed-tier buckets:** process whole bucket at the highest priority tier, or split into per-tier sub-buckets? (Defaults to whole-bucket processing in current scripts.)
- **Cross-Pass-1 coverage gap:** AGOT is the only Pass-1-complete book. Tier A "in Pass 1" path fires only against AGOT until ACOK/ASOS/AFFC/ADWD finish. Acceptable for v1?
- **Wiki-ingester v2 prose-only rewrite:** do this BEFORE running Stage 3a `--apply`? Or run 3a first to generate skeletons, then rewrite the agent prompt against those concrete skeletons? Sequencing call.
