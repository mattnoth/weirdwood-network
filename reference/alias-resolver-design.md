# Alias Resolver + Node Display Design

> **Status:** DESIGN — decisions captured 2026-06-08 (Session 86). No code changes in this session. Implementation queued for a follow-on script-builder pass, NOT blocking Plate 5.
>
> **Scope:** Two design questions surfaced at the end of S85 (Plate 4 wiki-cluster bridge), plus 4 structural improvements surfaced by Matt's 23-mint triage. None of these block the Plate 5 merge; all of them improve how the graph SERVES queries.

---

## Q1 — Alias-as-edge-resolver: scope + integration

**Decision: build `scripts/event_alias_resolver.py` as a separate, deterministic lookup-only resolver. Harvest aliases broadly across all node types; apply as a lookup table only.**

### Why a separate script

`scripts/stage4_name_resolver.py` is a 5-rung collision-aware resolver for **person/house/location** entities (firstname-unique, context-present, context-prior). It needs that machinery because "Stark" / "Lord Stark" / "the Tully woman" / "Cat" all resolve to multiple candidates depending on chapter context.

Events don't have that problem. They're typically named with full unambiguous phrases ("the Red Wedding", "Battle of the Blackwater", "Tourney at Harrenhal"). A 30-line deterministic resolver is sufficient:

1. Load `working/wiki/data/event-node-aliases.json` (and any future non-event alias harvests) → build `{phrase → canonical_slug}` dict.
2. For each candidate string from Pass 1: normalize (lowercase, strip articles, kebab-case) → look up.
3. Unambiguous hit → return slug. Ambiguous → return `(None, "ambiguous")` and let the caller decide (drop / queue for review).
4. No LLM in the loop. Ever.

### Scope of the harvest

The wiki redirect graph has alias data for every page type. Current state:
- Event-node aliases: 176 across 113 of 371 event-nodes (built S85 via `scripts/wiki-event-alias-harvester.py`).
- Person/house/location aliases: covered by `working/wiki/data/alias-resolver.json` from Pass 2 Stage 0.

**Recommended extension:** systematic wiki-redirect harvest across ALL node types (characters, houses, locations, factions, artifacts, etc.) — same script pattern as the event harvester, just iterate the full `sources/wiki/_raw/` cache. Cost is $0 (the data is already local). Estimated yield: thousands of additional aliases. The resolver loads the union; lookup cost is O(1) regardless of table size.

### Frequency justifies the work

Mentions of canonical event names in Pass 1 (344 files scanned):

| Phrase | Mentions |
|---|---|
| "battle of" (any) | 293 |
| "red wedding" | 174 |
| "battle of the blackwater" | 109 |
| "siege of" (any) | 96 |
| "sack of" (any) | 65 |
| "battle of the trident" | 34 |
| "tourney at harrenhal" | 17 |
| "purple wedding" | 4 |

These mentions currently never become edge endpoints — Pass-1→graph edge building has no event-name resolver. Wiring this in lets Pass 1 prose mentions become `LOCATED_AT` / `AGENT_IN` / `VICTIM_IN` / `FIGHTS_IN` edges against the canonical event-nodes. Direct value for Plate 5+ traversal.

### Alias vs sub-beat — the substitution test

This was the crux of the design conversation. Aliases and sub-beats are NOT the same thing.

- **Alias** — two surface strings that refer to the SAME event. Test: substituting one for the other in any sentence about the event does not change its truth value.
  - "Red Wedding" ↔ "Wedding at the Twins" ↔ "Slaughter at the Twins" — all alias.
- **Sub-beat** — a string that names a MOMENT WITHIN a larger named event. The string does NOT refer to the whole event.
  - "Lord Walder calls for the bedding" is a 30-second moment inside the Red Wedding. It is one of: bread-and-salt arrival, ceremony, bedding-call, Rains-of-Castamere shift, slaughter begins, Catelyn's throat-cut, Grey Wind killed. Each is a beat; collectively they constitute the event.

Treating sub-beats as aliases collapses temporal granularity inside an event. "What happened before the slaughter started?" stops being graph-answerable.

**Operational rule:**
- Surface variant of the same event → `aliases:` array on the node.
- Moment-within-event → `SUB_BEAT_OF` edge from the beat-node to the parent-event-node. (Formalized as a canonical edge type this session — vocab 165 → 166. Distinct from the pre-existing `PART_OF`, which is the event-in-war containment edge: `battle-of-the-blackwater` → `PART_OF` → `war-of-the-five-kings`. `SUB_BEAT_OF` is finer-grained: a beat within an event hub.)
- The dashes-vs-spaces test catches surface variants only. It does NOT catch granularity differences — `lord-walder-calls-for-the-bedding` is not "lord walder calls for the bedding" as a variant of "red wedding"; it's a sub-beat.

### What's NOT in scope

- No LLM augmentation. If a Pass-1 mention doesn't match any harvested alias, it's a true miss — usually because the phrasing is paraphrased ("Walder's slaughter") and the wiki has no redirect from it. A 70%-precision Haiku layer over a 95%-precision lookup adds graph pollution, not edges — the precision-gate principle, same standard that any future LLM enrichment must meet. (Not invoking a blanket S74 "no enrichment" ban; S74 was a specific gate failure on a specific run, S75 amended to "enrichment wanted, gated on precision." The point here is the lookup is already so precise that the LLM tail has no math to win on.)
- No new edge types. The resolver feeds existing edge builders; what's emitted depends on the candidate's source row, not the resolver.

### Concrete next step

A follow-on session writes `scripts/event_alias_resolver.py` (small, deterministic) + extends the harvester to non-event types + integrates into the Pass-1→graph edge pipeline. Estimated effort: half a session. Not blocking Plate 5.

---

## Q2 — Chat-UI display name policy

**Decision: every node carries `slug:` (kebab-case join key) and `name:` (human-readable). Mint schema rename `title:` → `name:`. Rendering belongs to the consumer (chat UI, agent system prompt, whatever). The graph layer does NOT enforce a display policy.**

### Why minimal

The graph stores both fields. Downstream consumers pick whichever serves them:
- Chat UI: post-process slugs in agent output → human names at render time.
- Agent system prompt: when node frontmatter is in context, the agent naturally pulls the appropriate surface from the surroundings — no enforcement needed.
- Programmatic queries: use slugs everywhere.

There is nothing to enforce at the graph layer. The previous draft's "enforceable at the prompt layer" framing was overengineered.

### The mint-schema fix

Plate-3 mints (under `working/edge-modeling/plate3-full/` and friends) currently carry a `title:` field (e.g., "Lord Walder calls for the bedding") but no `name:`. Wiki-derived nodes carry `name:` ("Red Wedding") but no `title:`. Two schemas in the same `events/` namespace.

**Fix:** rename `title:` → `name:` in `scripts/edge-reify-backfill.py` so future mints use the canonical surface field. Existing 219 staged mints get a one-time rewrite at Plate 5 merge (still in staging; no graph writes have happened).

After this lands, every event-node — wiki-derived or chapter-beat-mint — has the same surface contract: `slug` + `name` + optional `aliases`.

---

## Bonus — 4 structural fixes (all staged for Plate 5 or follow-on)

These surfaced during S85's 23-mint human triage. They're not part of the alias/display design proper but cluster with it as wiki-layer-quality work.

### Fix 1 — Wiki event-type vocabulary expansion (27 corrections staged)

**Root cause:** `scripts/wiki-pass2-triage.py` only knew `event.battle`, `event.tournament`, `event.war`. Every other event subtype defaulted to `event.battle` — including all weddings, coronations, feasts, trials, executions, assassinations. 27 misclassifications staged for correction at `working/edge-modeling/plate2.5-schema-fixes/event-type-corrections.jsonl`.

**Vocabulary expansion (this document):** `event.wedding`, `event.feast`, `event.coronation`, `event.trial`, `event.assassination`, `event.execution`, `event.conspiracy` added as first-class types in `reference/architecture.md`. See updated Type Reference Table.

**Prevention (3 fixes for next session):**
1. Vocabulary expansion in architecture.md — DONE this session.
2. Triage entity-type map update — assign new types from slug/title patterns (e.g., `wedding-of-X` → `event.wedding`). Code change to `scripts/wiki-pass2-triage.py`. Pending.
3. New script `scripts/wiki-event-type-validator.py` — scans every event-node for slug/title-vs-type mismatches; runs as a hook after any wiki-pass2 re-run. Would have caught all 27. Pending.

### Fix 2 — IDF-style downweighting in narrowing function

`scripts/plate4-wiki-cluster.py` currently scores `+1` per shared participant. High-frequency participants (Cersei in ~50 events, Robert in ~30, Tyrion in ~40) produce spurious overlap.

**Fix:** weight participants by `log(total_events / events_containing_this_participant)` — same TF-IDF intuition used in text retrieval. Rare-participant overlap scores high; mass-participant overlap scores low. Catches the S85 false-positive cluster around `feast-in-honor-of-king-roberts-visit-to-winterfell` (over-scored on Cersei/Robert/Tyrion/Joffrey overlap with several unrelated events).

Pending — code change to the narrowing function before any future re-cluster.

### Fix 3 — `era:` frontmatter field (forward-only)

Events like `aegons-conquest`, `roberts-rebellion`, `battle-above-the-gods-eye` (Dance of Dragons) keep appearing as candidates for current-narrative mints. They're chronologically incompatible.

**Decision:** add `era:` to node frontmatter going forward. **Do NOT backfill retroactively.** Suggested enum:

```
era: pre-conquest | age-of-heroes | targaryen-conquest | targaryen-rule
    | dance-of-dragons | roberts-rebellion | current-narrative
```

The narrowing function weights `era=current-narrative` higher when classifying current-narrative mints. Future mint emissions stamp `era` at creation time. See updated Node Frontmatter Conventions in architecture.md.

### Fix 4 — Missing canonical event-nodes — accept chapter-beat tier

S85's triage surfaced 2-3 genuinely missing wiki event-pages (Robert's boar-hunt assassination, Winterfell murders during Stannis's approach — distinct from the Stannis-approach march itself; Tyrion's Vale-clansmen attack). **Decision:** accept the chapter-beat tier as the home for these. No separate workflow to promote chapter-beat mints to "canonical" event-node status — the mint IS the event-node, just minted from chapter prose rather than from a wiki page. Plate 5 merge treats both tiers uniformly.

---

## Cross-references

- `reference/architecture.md` — Type Reference Table (new event subtypes), Node Frontmatter Conventions (`era:`), Display Names section, `ALIAS_OF` row note.
- `working/wiki/data/event-node-aliases.json` — 176 aliases, current; expand via `scripts/wiki-event-alias-harvester.py` to non-event types.
- `working/edge-modeling/plate2.5-schema-fixes/event-type-corrections.jsonl` — 27 schema-fix corrections staged.
- `scripts/stage4_name_resolver.py` — existing person/house/location resolver; do NOT extend with event logic.
- `scripts/plate4-wiki-cluster.py` — narrowing function that needs IDF weighting.
- `progress/continue-prompts/2026-06-05-edge-modeling-plate-5-merge.md` — Plate 5 merge prompt (Sonnet); folds in these decisions.
