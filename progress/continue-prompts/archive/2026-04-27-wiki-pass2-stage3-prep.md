# Continue Prompt — Wiki Pass 2 Stage 3: Python-First Pipeline

**Created:** 2026-04-27 end-of-Session-24
**Goal:** Build the priority-bucket script + Stage 3a deterministic Python emission script, run them, run a mid-stage agent review, then launch Stage 3b agent prose-fill against Tier A only. Tier B is fully emitted by Python; Tier C is deferred.
**Cost envelope:** Python steps are local. Stage 3b agent cost depends on Tier A bucket count (sized by the priority script's distribution; report before launching).

## Read first (canonical refs)

1. **`working/runbooks/wiki-pass2-pipeline.md`** — the canonical pipeline definition. **Read this first; it overrides the older orchestration runbook for Stage 3+.**
2. `reference/architecture.md` — entity types, edge types, infobox-field → edge-type mapping (§ "Wiki Infobox Fields → Edge Type Mapping").
3. `working/runbooks/wiki-pass2-orchestration.md` — orchestration mechanics (bundle, validator, conflicts, fingerprints) — still applies, but its "agent does everything" assumption is replaced by the Python-first pipeline.
4. `.claude/agents/wiki-ingester.md` — agent prompt as it stands; its role narrows to prose-only for Tier A. **Update before launching Stage 3b** (see "Agent prompt update" section below).
5. `working/wiki-parsed/parse-stats.md` — what Track B already parsed.
6. `working/wiki-parsed/page-index.jsonl` (17,657 lines) and `working/wiki-parsed/infobox-data.jsonl` (5,279 lines).
7. `extractions/mechanical/agot/` — Pass 1 outputs (only AGOT complete; ACOK/ASOS/AFFC/ADWD will fold in as Pass 1 completes).
8. `scripts/wiki-pass2-triage.py` — existing triage script.

## Hard rules

- **Python before Agent — default rule going forward.** Whenever a deterministic step can produce part of the output, it runs first. Agents only do what genuinely requires reasoning.
- **`first_available` is not emitted.** The field is reserved for the post-release backfill script.
- **Never drop anything from `sources/` or `working/`.** Tier C pages stay; redirects, stubs, lists stay; bucket bundles stay (see "Bucket preservation" below).
- **Never re-fetch the wiki.** It is local at `sources/wiki/_raw/`. No HTTP, no `WebFetch`, no Playwright. See CLAUDE.md "Critical Rule: The Wiki Is Already Local."
- **Edge discovery for prose is out of scope.** Stage 4 owns that, sequential to Stage 3, never parallel. See `2026-04-27-wiki-pass2-stage4-edge-discovery.md`.

## Build order

### 1. `scripts/wiki-pass2-prioritize.py`

Pure metadata labeling, no emission. Reads `page-index.jsonl`, `infobox-data.jsonl`, and Pass 1 raw entity lists. Writes `priority_tier`, `has_infobox`, and (Tier C only) `page_kind` onto each of the 472 secondary manifests.

**Tier rules** (per `wiki-pass2-pipeline.md`):

| Tier | Definition | Action |
|------|------------|--------|
| **A** | Page name in any Pass 1 raw entity list **OR** ≥5 chapter cite_refs | Stage 3a Python skeleton + Stage 3b agent prose-fill |
| **B** | Has infobox but does NOT meet Tier A criteria | Stage 3a Python skeleton only. **Done.** No agent. |
| **C** | No infobox AND no chapter cite_refs | Defer. Label `has_infobox: false` and `page_kind`. |

**Page-kind detection (Tier C only):** read each cached HTML body in `sources/wiki/_raw/<Page>.json` and apply patterns:
- `redirect` — body is `<p>Redirect to: ...</p>` or page-index has `redirect_target`. **Verify in the first 5 minutes:** check whether the Playwright scraper followed redirects (storing only destination) or stored redirect markup. If the former, all redirects fall to `stub`/`unknown`.
- `disambiguation` — body contains "may refer to:" plus list.
- `list_article` — title matches `^List of `.
- `year_article` — title matches `\d+ AC` or `Year \d+`.
- `stub` — `byte_size` < ~500 bytes body, no infobox, none of the above.
- `entity` — default catch-all for Tier C.

**Tier A and Tier B do NOT get `page_kind`.** Adding `entity` to obvious entities adds zero query value and bloats the schema.

### 2. `scripts/wiki-pass2-emit-deterministic.py` (Stage 3a)

Emits skeleton nodes for **all Tier A and Tier B pages** from infobox + page-index data. No agent.

**Output per page:** `working/wiki-pass2/<bucket_id>/tmp/<slug>.node.md`

**Frontmatter (deterministic):**
- `name`, `type` (from `entity_type_guess`), `slug`, `aliases`
- `confidence: tier-2` (default for secondary; can be overridden by manifest's `tier_default`)
- `wiki_source`, `bucket_id`, `prompt_version: v1-python`, `node_version: 1`, `pass_origin: pass2-wiki-deterministic`
- **No `first_available`.**

**Body (deterministic):**
- `## Identity` — one line: `<Name> is a <type> from <wiki_source>.`
- `## Edges` — full infobox-derived edge list using `reference/architecture.md` § "Wiki Infobox Fields → Edge Type Mapping". Every edge cites `(track_b: <field>)`.

**Bucket isolation note:** Stage 3a Python is NOT bucket-isolated. It reads global `infobox-data.jsonl` and emits per-bucket. The infobox edges include cross-page references (e.g., a character's `Spouse` field names another page that may live in a different bucket). That cross-bucket reference is encoded as a string in the edge target — graph linking happens later. Python doesn't need agent-style bucket isolation because it's not making judgment calls.

### 3. Mid-stage agent review

Between Stage 3a and Stage 3b, run a quality-gate review.

**Purpose:** spot-check the Python script's output before paying agent cost on Stage 3b.

**What:** spawn an agent (general-purpose or a dedicated review agent) to read 15-20 stratified Python-emitted skeletons and compare against `track_b_row.relationships`. Flag:
- Edges in track_b that the script missed (parser gap)
- Edges the script emitted that don't trace to track_b (script bug)
- `entity_type_guess` that look wrong on inspection
- Slug or citation format issues

**Output:** `working/wiki-pass2/stage3a-review.md` — issue list with severity. **Read-only review; no node modifications.**

**Decision:** proceed to Stage 3b / patch the Python script and re-emit / escalate.

### 4. Agent prompt update (before launching Stage 3b)

Update `.claude/agents/wiki-ingester.md` to v2 prose-only role:
- Frontmatter: agent reads it but does NOT modify it (Python owns frontmatter)
- `## Edges`: agent reads it but does NOT modify it (Python owns edges)
- `## Identity`: agent reads the thin one-liner; can extend it in v2 prose-fill OR leave it (decide during prompt update)
- Body sections agent fills in: `## Origins`, `## Allegiances` (narrative), `## Appearances & Description`, `## Narrative Arc`, `## Quotes`, `## Notes`
- Validator update: Stage 3b run validates that `## Edges` is byte-identical between Python skeleton and agent output. Drift = bucket failure.

This is a meaningful prompt rewrite. Treat as its own work item before Stage 3b launch.

### 5. Stage 3b launch (Tier A only)

After Steps 1-4 are done and the review report is clean:
1. Use the existing `weirwood wiki secondary <wave_size> <wave_count>` launcher pattern (multi-terminal sub-agents).
2. Process Tier A buckets only.
3. Tier B is already done by Stage 3a; nothing to launch.
4. Tier C deferred.

## Bucket preservation — hard rule

After Stage 1, all 37 core buckets retained `bucket_input.json`, `manifest.json`, `tmp/<slug>.node.md`, and `validator-report.json`. **This must continue through Stages 3a and 3b.** The launcher already preserves these post-promotion. Do not add any cleanup step. Reasons:
- Stage 4 (edge discovery) reads the bundles, agent prose, and Python emission history to find prose-derived edges.
- Re-runs and audits need bundles intact.
- Post-release `first_available` backfill needs track_b rows from the bundles.

If anything in the launcher or scripts looks like it deletes `tmp/`, `bucket_input.json`, or `validator-report.json` after promotion — stop and ask.

## Things to surface to Matt before launching Stage 3b

- **Tier distribution** — counts and example pages from each tier. Confirm boundaries.
- **Stage 3a output stats** — Tier B node count, mean edges/node, type-guess distribution. Anything that looks bad triggers a Python script patch before Tier A nodes get written.
- **Mid-stage review report** — issues found, severity. Matt approves before Stage 3b launches.
- **Cost estimate for Tier A** — Tier A bucket count × Stage-1 per-node rate ($0.111). If >$200 or >2 days wall time, propose narrower Tier A criteria.
- **Bucket-mixing question** — what happens when one bucket has 8 Tier-A pages and 12 Tier-C pages? Matt's call.
- **Cross-Pass-1 coverage gap** — only AGOT is Pass-1-complete. Tier A's "in Pass 1" criterion fires only against AGOT until ACOK/ASOS/AFFC/ADWD finish. Acceptable for v1; flag it.
- **Redirect detection feasibility** — answer to whether Playwright preserved redirect markup determines whether `redirect` is a usable Tier C value.

## Out of scope (this session only)

- Do **not** process Tier C in any form.
- Do **not** drop, merge, or delete any existing manifests, source pages, wiki cache files, or bucket bundles.
- Do **not** re-process the 855 core nodes.
- Do **not** add `page_kind` to Tier A/B manifests.
- Do **not** touch `first_available` — fully deferred.
- Do **not** do prose-derived edge discovery — that's Stage 4.
- Do **not** run /endsession without Matt's explicit go-ahead.

## DoD for this session

- [ ] `scripts/wiki-pass2-prioritize.py` written, idempotent, dry-run-safe
- [ ] Tier distribution report shown to Matt; boundaries confirmed
- [ ] `scripts/wiki-pass2-emit-deterministic.py` (Stage 3a) written
- [ ] Stage 3a run; per-page node skeletons land in `tmp/`
- [ ] Mid-stage review agent spawned; review report written
- [ ] `.claude/agents/wiki-ingester.md` updated to v2 prose-only role
- [ ] Validator updated to enforce edge byte-equality between skeleton and agent output
- [ ] Tier A bucket list ready for Stage 3b launch
- [ ] **STOP HERE — do not launch Stage 3b without Matt's explicit go-ahead.**

## Reference

- `working/runbooks/wiki-pass2-pipeline.md` — canonical pipeline (read first)
- `working/runbooks/wiki-pass2-orchestration.md` — orchestration mechanics
- `scripts/wiki-pass2.sh` — launcher (extend if needed; don't rewrite)
- `scripts/wiki-pass2-validator.py` — validator (needs the edge-byte-equality check added)
- `scripts/wiki-pass2-coherence.py` — coherence check (no changes needed)
- `2026-04-27-wiki-pass2-stage4-edge-discovery.md` — sequel pass for prose-derived edges
