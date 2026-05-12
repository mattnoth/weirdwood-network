# Handoff — Orphan-Batch: Close Top High-Traffic Missing Slugs

**Created:** 2026-05-12 (Session 49b watcher session)
**Recommended model:** **Sonnet 4.6.** Each node is a small reasoning task (type classification + 1-paragraph Identity from canon + 1-3 edges) over a bounded list. Same shape as case-collision Track A workers, which ran fine on Sonnet. Opus is wasteful; Haiku will drift on the multi-type judgment calls.
**Parallel-safe with:** Stage 4 prose-edge-classifier (`progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`) — disjoint file write-sets. But Matt has elected to run sequentially; if Stage 4 starts before this lands, see "Timing with Stage 4" below.
**Sequential prerequisite:** none.

---

## Why this work, why now

Today's orphan-edges audit (`working/audits/orphan-edges-2026-05-12.md` + `working/audits/orphan-edges-2026-05-12-cat1-full.tsv`) surfaced 822 unique missing target slugs across 1,896 orphan edges. The top ~10 high-traffic non-date orphans account for ~500+ dangling edges by themselves. Two patterns:

- **Genuine missing nodes** — well-known canonical entities the graph never got around to creating (e.g., the Dance of the Dragons factions `blacks`/`greens`)
- **Alias-mismatch** — orphan edge points at a slug that's an alias of a canonical node, but the alias-resolver doesn't know the mapping yet (e.g., `joffrey-i-baratheon` → `joffrey-baratheon`)

Closing the top 10 resolves the largest share of orphan-edge surface area in one focused batch. Stage 4 (prose-edge discovery) wants this done first — running it on a graph with these gaps means edges that *should* attach to a node instead land as orphan-only.

---

## Scope — the top targets

Read `working/audits/orphan-edges-2026-05-12-cat1-full.tsv` as the source of truth. Filter to rank-by-edge-count, skip rows where `is_date=1`, skip rows where target_slug looks like a date pattern (e.g., `\d+-ac`, `\d{3,4}`). The top 10-15 non-date entries by `in_count` (column 4 = inbound edges) are the candidates.

Pre-flight expectation (from today's audit — verify still current):

| Rank | Slug | Edges | Likely fix | Notes |
|---|---|---|---|---|
| 1 | `blacks` | 138 | **CREATE** | Dance of the Dragons faction. `type: organization.faction` (similar to greens). |
| 2 | `greens` | 127 | **CREATE** | Dance of the Dragons faction. `type: organization.faction`. |
| 3 | `age-of-heroes` | 43 | **CREATE** | Historical era. `type: event.era` (verify era is in TYPE_DIR_MAP; if not, use closest fit + flag for schema-drift-auditor). |
| 4 | `crossroads-inn` | 39 | **ALIAS FIX** | Existing `graph/nodes/locations/inn-at-the-crossroads.node.md` already aliases other variants. Add `"crossroads-inn"` (and `"Crossroads inn"`) to its aliases list. |
| 5 | `dragons` | 32 | **ALIAS FIX** | `graph/nodes/species/dragon.node.md` exists. Add `"dragons"` to its aliases. |
| 6 | `crypt-of-winterfell` | 29 | **CREATE** | Location within Winterfell. `type: location.castle` or similar — pick whatever the existing crypt-style nodes use (grep for `BURIED_AT.*crypt`). |
| 7 | `joffrey-i-baratheon` | 22 | **ALIAS FIX** | Canonical `joffrey-baratheon.node.md` exists. Add `"Joffrey I Baratheon"` + `"joffrey-i-baratheon"` to its aliases. |
| 8 | `vale` | 21 | **VERIFY THEN ALIAS FIX** | Session 49 added `"The Vale"` to `vale-of-arryn`. Check the audit example_target_text — if edges say `Vale` bare, add `"Vale"` (lowercase) to aliases too. |
| 9 | `two-betrayers` | 21 | **CREATE** | Dance of the Dragons concept (the two dragonseed riders who switched sides). `type: concept.event-group` or similar — pick based on architecture.md. |
| 10 | `bastards-boys` | 3 (6 backlinks) | **CREATE** | Ramsay Bolton's brutal gang in ADWD. Members already exist as character nodes: damon-dance-for-me, skinner, yellow-dick, sour-alyn, luton, grunt, ben-bones. `type: organization.faction`. |

Plus opportunistic if quick: `tommen-i-baratheon` (8) → ALIAS FIX to `tommen-baratheon`. Anything else from the TSV that's clearly a regnal-numeral alias-mismatch.

**Hard rule on date-pattern slugs:** Do NOT create nodes for `*-ac` targets (e.g., `300-ac-meereen`, `282-ac-ashford`). Those are a separate parser bug (date-bleed in BORN_AT/DIED_AT). Out of scope for this batch.

---

## Steps

### 1. Pre-flight (5 min)

```bash
# Verify the audit TSV exists
ls -la working/audits/orphan-edges-2026-05-12-cat1-full.tsv
# Verify which proposed targets already exist (alias-fix vs create)
for slug in blacks greens age-of-heroes crypt-of-winterfell two-betrayers bastards-boys; do
  hit=$(find graph/nodes -name "${slug}.node.md" -print -quit)
  [ -n "$hit" ] && echo "EXISTS: $slug ($hit)" || echo "MISSING: $slug"
done
for slug in crossroads-inn dragons joffrey-i-baratheon tommen-i-baratheon vale; do
  hit=$(grep -lEi "(^|[\"\\s])${slug}([\"\\s,]|$)" graph/nodes/**/*.node.md 2>/dev/null | head -1)
  [ -n "$hit" ] && echo "ALIAS-CANDIDATE TARGET: $slug found in $hit" || echo "ALIAS-CANDIDATE LOOSE: $slug"
done
```

Confirm the create-vs-alias-fix split matches the table above. If anything in the table is stale (e.g., a node got created between when this prompt was written and now), adjust before proceeding.

### 2. Apply alias fixes (each ~30 seconds)

For each ALIAS FIX target, open the canonical node and append to its `aliases:` list. Match the YAML form (inline `["A", "B"]` vs. block `- A\n- B`). Don't change form.

Example for `inn-at-the-crossroads.node.md`:
```yaml
aliases:
  - "Inn at the Crossroads"
  - ...existing aliases...
  - "crossroads-inn"
  - "Crossroads Inn"
```

### 3. Create new nodes (each ~5 min)

For each CREATE target, write a new node file at `graph/nodes/<type-dir>/<slug>.node.md` following the schema:

```markdown
---
name: "<Display Name>"
type: <type-from-architecture.md-TYPE_DIR_MAP>
slug: <slug>
aliases: ["<obvious aliases>"]
confidence: tier-1|tier-2|tier-3
wiki_source: null
pass_origin: pass2-orphan-batch-2026-05-12
node_version: 1
---

## Identity

<1-paragraph canon-grounded description. For factions: who composed them, when/where active, key events. For locations: where they are, who lives/lived there, what happens there. For eras: rough date range, defining features.>

## Edges

<2-5 outbound edges using the locked 22-type vocabulary. For factions, common patterns: SUPPORTS / OPPOSED_BY / INVOLVED_IN. For locations: PART_OF / LOCATED_IN. For eras: PRECEDES / FOLLOWS.>
```

**Multi-type policy (Session 47, ratified in architecture.md):** If an entity could be more than one type (e.g., free-folk = culture + faction; children-of-the-forest = species + faction), pick the primary type. Other facets emerge via edges, not via a second node.

**Type sources of truth:**
- `reference/architecture.md` TYPE_DIR_MAP table (line ~85+)
- Existing-node convention: if you're not sure between `event.era` and `concept.era`, grep `graph/nodes/events/*.node.md` for `^type: event.era` to see if anyone uses it, then match precedent

### 4. Rebuild derived artifacts

```bash
# Rebuild alias-resolver (picks up any new aliases added in step 2)
python3 scripts/wiki-pass2-build-alias-resolver.py --apply
# Rebuild mention-index (resolves chapter mentions against updated alias-resolver)
python3 scripts/build-mention-index.py --all
```

### 5. Re-run orphan-edges audit + measure delta

```bash
python3 scripts/orphan-edges-audit.py 2026-05-12-post-orphan-batch
```

Expected: Cat 1 orphan-edge count drops by ~400-500 (the inbound edges of the targets you fixed). Cat 2 may shift slightly (alias fixes move edges from Cat 1 → resolved, not into Cat 2). Resolution rate gain: ~2-3 pp on the `_summary.json` resolution_rate_pct.

If the audit shows fewer-than-expected resolved edges:
- Verify your alias additions actually landed in frontmatter (YAML form match)
- Verify your new nodes are findable by slug (file at `graph/nodes/<dir>/<slug>.node.md`, frontmatter `slug:` matches filename)

### 6. Update artifacts

- `working/todos.md` — add a DONE entry under "Mission Protocol & Orchestration" or the closest section:
  ```
  - [x] **DONE — Orphan-batch top-10 cleanup (2026-05-12)** — Created N new nodes (blacks, greens, age-of-heroes, ...) + applied M alias fixes (crossroads-inn → inn-at-the-crossroads, dragons → dragon, joffrey-i → joffrey-baratheon, ...). Cat 1 orphan edges X → Y (−Z). Resolution rate ~A% → ~B%. Audit re-run: `working/audits/orphan-edges-2026-05-12-post-orphan-batch.md`.
  ```
- `worklog.md` — add a Session entry following the standard format (~15 lines). Bump session number from 49b.
- Don't forget: the prior Track A spot-check todo entry (added 2026-05-12) is partially superseded by this batch — leave it, but note in this session's worklog entry that ~X of Track A's residual orphans were absorbed by this work.

---

## Timing with Stage 4

If Matt has not yet started Stage 4 when this lands: nothing to coordinate.

If Stage 4 has started in parallel:
- Stage 4 is likely still in its script-build phase (creating `scripts/wiki-pass2-build-edge-candidates.py`) — no graph conflict
- Make sure this orphan-batch finishes BEFORE Stage 4's candidate-gen step runs (Step 3 in Stage 4's prompt) — otherwise Stage 4 will generate candidates against a stale snapshot and miss the new nodes as valid edge targets
- The Stage 4 prompt explicitly requires Matt-confirmation between phases, so just don't trigger Stage 4 step 3 until this session reports DONE in worklog

---

## DO NOT

- Touch any node with `prompt_version: v1` or `prompt_version: v1-python` outside this batch's scope (carve-out from Stage 1/3 immutability rule: this batch only writes the *new* nodes it's creating + alias-list additions to specifically listed existing nodes).
- Create nodes for date-pattern target slugs (`*-ac`, `\d{3,4}`). Date-bleed is a separate parser-fix track.
- Create nodes for targets where the entity is debatable (e.g., `lads`, `betrothal`, `ship` — these are likely schema-drift or text-extraction noise, not real entities). When in doubt: skip + leave a note in worklog.
- Auto-run `/endsession` — Matt's standing rule, hard.
- Touch `sources/` (read-only).
- Skip step 5 (re-run audit). The whole point of this work is measurable orphan-edge reduction; if you don't measure, the work isn't done.

---

## If something goes wrong

- **TYPE_DIR_MAP doesn't have a clean fit** for `age-of-heroes` or `two-betrayers` → use closest existing type, add a note to `working/todos.md` under "Audit Findings" calling out the schema-drift candidate. Don't invent new types.
- **Alias-resolver script fails** → likely a malformed YAML frontmatter in one of your alias edits. Run `python3 -c "import yaml; yaml.safe_load(open('<file>'))"` against each modified node to localize.
- **Audit re-run shows no improvement** → suggests your edits didn't land where you think they did. Check that you wrote to canonical paths (not `_conflicts/` or `_unclassified/`).

---

## Self-contained for resumption

Files a fresh session should read:
- This file
- `working/audits/orphan-edges-2026-05-12.md` + the `-cat1-full.tsv`
- `reference/architecture.md` (TYPE_DIR_MAP + multi-type policy section added Session 47 + locked 22-type edge vocabulary)
- One sample of each pattern:
  - `graph/nodes/factions/<any>.node.md` (faction shape reference)
  - `graph/nodes/locations/inn-at-the-crossroads.node.md` (alias-merge shape — has multiple alias forms already)
- `working/todos.md` (where this session's DONE entry will go)
- `worklog.md` (most recent 2-3 sessions for format reference)

Estimated wall-clock: 60-90 min for top-10 (alias fixes are quick; node creates are the bulk). If pushing to top-15, add ~30 min.
